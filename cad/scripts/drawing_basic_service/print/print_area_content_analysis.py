# -*- coding: utf-8 -*-
"""print_area_content_analysis.py

研究“伪打印区域”的内容判定，不直接参与当前稳定打印主流程。

当前目标：
1. 对每个打印区域统计内部内容复杂度
2. 用同一文件内其它打印区域作为参照，识别明显异常简单的区域
3. 给后续“是否跳过该打印区域”提供证据，而不是直接替代当前打印逻辑

当前建议的判定思想：
- 空白区域，优先视为伪打印区域候选
- 仅包含少量几何图形和文字，且复杂度明显低于同文件其它图纸时，视为伪打印区域候选
- 该模块既可以独立输出分析结果，也可以为“净化适配模式”提供要剔除的打印区域句柄列表
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median
from typing import Any, Iterable
import argparse
import json
import sys
import time


current = Path(__file__).resolve()
MODULE_DIR = current.parent
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent
if str(current) not in sys.path:
    sys.path.insert(0, str(current))
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from system.licad import C, retry_on_busy
from system.CAD_core import launch_cad_guardians, open_file
from system.CAD_coordination import wait_quiescent
from system.runtime_guard_bridge import RuntimeGuardTriggered, assert_runtime_guard_ok, render_guard_error
from print_policy import PRINT_MODE_ADAPTIVE, build_print_plan, normalize_print_mode, plan_to_dict


TEXT_OBJECTS = {"AcDbText", "AcDbMText", "AcDbAttribute", "AcDbAttributeDefinition"}
SIMPLE_GEOMETRY_OBJECTS = {
    "AcDbLine",
    "AcDbPolyline",
    "AcDb2dPolyline",
    "AcDbLwPolyline",
    "AcDbArc",
    "AcDbCircle",
}
COMPLEX_OBJECTS = {"AcDbBlockReference", "AcDbHatch", "AcDbSpline", "AcDbDimension"}


@dataclass
class AreaContentMetrics:
    handle: str
    entity_count: int
    text_count: int
    simple_geometry_count: int
    complex_entity_count: int
    block_reference_count: int
    layer_count: int
    text_chars: int
    bbox_fill_ratio: float
    complexity_score: float


@dataclass
class EntitySnapshot:
    handle: str
    bbox: tuple[float, float, float, float]
    obj_name: str
    layer: str
    text_chars: int


def _safe_handle(obj: Any) -> str:
    try:
        return str(obj.Handle)
    except Exception:
        return str(id(obj))


def _bbox_xy(ent: Any) -> tuple[float, float, float, float] | None:
    try:
        p1, p2 = _get_entity_bbox_points(ent)
        min_x = min(float(p1[0]), float(p2[0]))
        min_y = min(float(p1[1]), float(p2[1]))
        max_x = max(float(p1[0]), float(p2[0]))
        max_y = max(float(p1[1]), float(p2[1]))
        return min_x, min_y, max_x, max_y
    except Exception:
        return None


def _contains_bbox(
    outer: tuple[float, float, float, float],
    inner: tuple[float, float, float, float],
    tol: float,
) -> bool:
    return (
        outer[0] <= inner[0] + tol
        and outer[1] <= inner[1] + tol
        and outer[2] >= inner[2] - tol
        and outer[3] >= inner[3] - tol
    )


@retry_on_busy(max_retries=10, base_delay=0.2)
def _get_entity_bbox_points(ent: Any):
    return ent.GetBoundingBox()


@retry_on_busy(max_retries=10, base_delay=0.2)
def _get_collection_count(collection: Any) -> int:
    return int(collection.Count)


@retry_on_busy(max_retries=10, base_delay=0.2)
def _get_collection_item(collection: Any, index: int) -> Any:
    return collection.Item(index)


@retry_on_busy(max_retries=10, base_delay=0.2)
def _get_layout_block_name(layout: Any) -> str:
    return str(layout.Block.Name)


@retry_on_busy(max_retries=10, base_delay=0.2)
def _get_entity_object_name(ent: Any) -> str:
    return str(getattr(ent, "ObjectName", ""))


@retry_on_busy(max_retries=10, base_delay=0.2)
def _get_entity_layer(ent: Any) -> str:
    return str(ent.Layer)


@retry_on_busy(max_retries=10, base_delay=0.2)
def _get_text_string(ent: Any) -> str:
    return str(ent.TextString)


def _iter_collection_entities(collection: Any) -> Iterable[Any]:
    count = _get_collection_count(collection)
    for index in range(count):
        try:
            yield _get_collection_item(collection, index)
        except Exception:
            continue


def _iter_space_entities(owner_btr_name: str) -> Iterable[Any]:
    doc = C.doc
    wait_quiescent(min_quiet=0.2, timeout=10.0)
    if owner_btr_name == "*MODEL_SPACE":
        for ent in _iter_collection_entities(doc.ModelSpace):
            yield ent
        return

    for layout in doc.Layouts:
        try:
            if _get_layout_block_name(layout) == owner_btr_name:
                for ent in _iter_collection_entities(layout.Block):
                    yield ent
                return
        except Exception:
            continue


def collect_space_entity_snapshots(owner_btr_name: str) -> list[EntitySnapshot]:
    snapshots: list[EntitySnapshot] = []
    for ent in _iter_space_entities(owner_btr_name):
        bbox = _bbox_xy(ent)
        if bbox is None:
            continue
        text_chars = 0
        try:
            obj_name = _get_entity_object_name(ent)
        except Exception:
            obj_name = ""
        if obj_name in TEXT_OBJECTS:
            try:
                text_chars = len(_get_text_string(ent))
            except Exception:
                text_chars = 0
        try:
            layer = _get_entity_layer(ent)
        except Exception:
            layer = ""
        snapshots.append(
            EntitySnapshot(
                handle=_safe_handle(ent),
                bbox=bbox,
                obj_name=obj_name,
                layer=layer,
                text_chars=text_chars,
            )
        )
    snapshots.sort(key=lambda item: item.bbox[0])
    return snapshots


def _iter_candidate_snapshots(
    snapshots: list[EntitySnapshot],
    area_bbox: tuple[float, float, float, float],
    area_handle: str,
    tol: float,
) -> Iterable[EntitySnapshot]:
    max_x = area_bbox[2]
    for snap in snapshots:
        if snap.bbox[0] > max_x + tol:
            break
        if snap.handle == area_handle:
            continue
        if _contains_bbox(area_bbox, snap.bbox, tol):
            yield snap


def collect_area_content_metrics_from_bbox(
    area_bbox: tuple[float, float, float, float],
    *,
    owner_btr_name: str,
    area_handle: str = "",
    tol_factor: float = 0.0005,
    snapshots: list[EntitySnapshot] | None = None,
) -> AreaContentMetrics | None:
    short_side = min(area_bbox[2] - area_bbox[0], area_bbox[3] - area_bbox[1])
    tol = max(short_side * tol_factor, 1.0)
    area_size = max((area_bbox[2] - area_bbox[0]) * (area_bbox[3] - area_bbox[1]), 1.0)

    entity_count = 0
    text_count = 0
    simple_geometry_count = 0
    complex_entity_count = 0
    block_reference_count = 0
    text_chars = 0
    layers: set[str] = set()
    cumulative_entity_area = 0.0
    snapshots = snapshots if snapshots is not None else collect_space_entity_snapshots(owner_btr_name)

    for snap in _iter_candidate_snapshots(snapshots, area_bbox, area_handle, tol):
        entity_count += 1
        if snap.layer:
            layers.add(snap.layer)

        if snap.obj_name in TEXT_OBJECTS:
            text_count += 1
            text_chars += snap.text_chars
        elif snap.obj_name in SIMPLE_GEOMETRY_OBJECTS:
            simple_geometry_count += 1
        elif snap.obj_name == "AcDbBlockReference":
            block_reference_count += 1
            complex_entity_count += 1
        elif snap.obj_name in COMPLEX_OBJECTS:
            complex_entity_count += 1

        ent_area = max((snap.bbox[2] - snap.bbox[0]) * (snap.bbox[3] - snap.bbox[1]), 0.0)
        cumulative_entity_area += ent_area

    bbox_fill_ratio = min(cumulative_entity_area / area_size, 1.0)
    complexity_score = (
        text_count * 1.0
        + simple_geometry_count * 0.6
        + complex_entity_count * 2.5
        + block_reference_count * 2.0
        + min(text_chars / 50.0, 4.0)
        + bbox_fill_ratio * 5.0
        + min(len(layers), 8) * 0.4
    )

    return AreaContentMetrics(
        handle=area_handle or "?",
        entity_count=entity_count,
        text_count=text_count,
        simple_geometry_count=simple_geometry_count,
        complex_entity_count=complex_entity_count,
        block_reference_count=block_reference_count,
        layer_count=len(layers),
        text_chars=text_chars,
        bbox_fill_ratio=round(bbox_fill_ratio, 4),
        complexity_score=round(complexity_score, 3),
    )


def collect_area_content_metrics(
    area_obj: Any,
    *,
    owner_btr_name: str,
    tol_factor: float = 0.0005,
) -> AreaContentMetrics | None:
    area_bbox = _bbox_xy(area_obj)
    if area_bbox is None:
        return None
    return collect_area_content_metrics_from_bbox(
        area_bbox,
        owner_btr_name=owner_btr_name,
        area_handle=_safe_handle(area_obj),
        tol_factor=tol_factor,
    )


def classify_pseudo_print_area_candidates(metrics_list: list[AreaContentMetrics]) -> list[dict[str, Any]]:
    if not metrics_list:
        return []

    complexity_baseline = median(item.complexity_score for item in metrics_list)
    entity_baseline = median(item.entity_count for item in metrics_list)
    out: list[dict[str, Any]] = []

    for item in metrics_list:
        reason: list[str] = []
        very_low_complexity = item.complexity_score <= max(complexity_baseline * 0.2, 1.5)
        very_few_entities = item.entity_count <= max(entity_baseline * 0.15, 3)
        simple_content_only = (
            item.complex_entity_count == 0
            and item.block_reference_count == 0
            and item.text_count <= 12
            and item.simple_geometry_count <= 12
        )
        low_fill = item.bbox_fill_ratio <= 0.2

        if item.entity_count == 0:
            reason.append("blank")
        if very_low_complexity:
            reason.append("very_low_complexity")
        if very_few_entities:
            reason.append("very_few_entities")
        if simple_content_only:
            reason.append("simple_geometry_and_text_only")
        if low_fill:
            reason.append("low_bbox_fill")

        pseudo_candidate = (
            item.entity_count == 0
            or (
                very_low_complexity
                and very_few_entities
                and simple_content_only
                and low_fill
            )
        )

        out.append(
            {
                **asdict(item),
                "pseudo_candidate": int(pseudo_candidate),
                "reasons": reason,
                "complexity_baseline": complexity_baseline,
                "entity_baseline": entity_baseline,
            }
        )
    return out


def analyze_job_content_candidates(
    jobs: list[dict[str, Any]],
    *,
    owner_btr_name: str,
    snapshots: list[EntitySnapshot] | None = None,
) -> list[dict[str, Any]]:
    snapshots = snapshots if snapshots is not None else collect_space_entity_snapshots(owner_btr_name)

    metric_objs: list[AreaContentMetrics] = []
    rows: list[dict[str, Any]] = []
    for job in jobs:
        min_x, min_y = job["lower_left"]
        max_x, max_y = job["upper_right"]
        metric = collect_area_content_metrics_from_bbox(
            (min_x, min_y, max_x, max_y),
            owner_btr_name=owner_btr_name,
            area_handle=str(job.get("handle", "")),
            snapshots=snapshots,
        )
        if metric is None:
            continue
        metric_objs.append(metric)
        rows.append(
            {
                **asdict(metric),
                "sequence_no": int(job.get("sequence_no", 0)),
                "paper_code": str(job.get("paper_code", "")),
                "ratio": str(job.get("ratio", "")),
                "output_path": str(job.get("output_path", "")),
            }
        )

    classified = classify_pseudo_print_area_candidates(metric_objs)
    by_handle = {item["handle"]: item for item in classified}
    for row in rows:
        item = by_handle[row["handle"]]
        row["pseudo_candidate"] = item["pseudo_candidate"]
        row["reasons"] = item["reasons"]
        row["complexity_baseline"] = item["complexity_baseline"]
        row["entity_baseline"] = item["entity_baseline"]
    return rows


def _job_get(job: Any, name: str, default: Any = None) -> Any:
    if isinstance(job, dict):
        return job.get(name, default)
    return getattr(job, name, default)


def analyze_jobs_content(jobs_by_space: dict[str, list[Any]]) -> dict[str, Any]:
    rows_by_space: dict[str, list[dict[str, Any]]] = {}
    all_rows: list[dict[str, Any]] = []
    snapshot_count = 0

    for layout_name, jobs in jobs_by_space.items():
        if not jobs:
            continue
        owner_btr_name = str(_job_get(jobs[0], "owner_btr", ""))
        snapshots = collect_space_entity_snapshots(owner_btr_name)
        snapshot_count += len(snapshots)

        job_dicts = [
            {
                "handle": str(_job_get(job, "handle", "")),
                "sequence_no": int(_job_get(job, "sequence_no", 0)),
                "paper_code": str(_job_get(job, "paper_code", "")),
                "ratio": str(_job_get(job, "ratio", "")),
                "output_path": str(_job_get(job, "output_path", "")),
                "lower_left": tuple(_job_get(job, "lower_left", ())),
                "upper_right": tuple(_job_get(job, "upper_right", ())),
                "layout_name": str(_job_get(job, "layout_name", layout_name)),
                "space_kind": str(_job_get(job, "space_kind", "")),
                "owner_btr": owner_btr_name,
            }
            for job in jobs
        ]
        rows = analyze_job_content_candidates(
            job_dicts,
            owner_btr_name=owner_btr_name,
            snapshots=snapshots,
        )
        rows_by_space[layout_name] = rows

        for row in rows:
            page_key = f"{layout_name}-{int(row['sequence_no']):02d}"
            all_rows.append(
                {
                    "page_key": page_key,
                    "layout_name": layout_name,
                    "space_kind": str(row.get("space_kind", "")),
                    "owner_btr": owner_btr_name,
                    **row,
                }
            )

    pseudo_candidates = [row for row in all_rows if int(row.get("pseudo_candidate", 0)) == 1]
    candidate_valid_print_areas = sum(1 for row in all_rows if int(row.get("pseudo_candidate", 0)) == 0)
    lowest12_by_complexity = sorted(all_rows, key=lambda item: item.get("complexity_score", 0.0))[:12]

    return {
        "snapshot_count": snapshot_count,
        "total_areas": len(all_rows),
        "candidate_valid_print_areas": candidate_valid_print_areas,
        "pseudo_candidates": pseudo_candidates,
        "lowest12_by_complexity": lowest12_by_complexity,
        "jobs_by_space": rows_by_space,
    }


def _normalize_path(path: str | Path) -> str:
    return str(Path(path).resolve()).lower()


def _is_name_only_target(target_path: str | Path) -> bool:
    raw = str(target_path)
    return Path(raw).name.lower() == raw.lower()


def _find_document_by_path(target_path: str | Path):
    wanted = _normalize_path(target_path)
    target_name = Path(target_path).name.lower()
    allow_name_fallback = _is_name_only_target(target_path)
    try:
        for doc in C.acad.Documents:
            try:
                doc_name = str(getattr(doc, "Name", "") or "").lower()
                if _normalize_path(doc.FullName) == wanted or (allow_name_fallback and doc_name == target_name):
                    return doc
            except Exception:
                continue
    except Exception:
        return None
    return None


def _activate_document_by_path(target_path: str | Path, retries: int = 8, delay: float = 0.5) -> bool:
    wanted = _normalize_path(target_path)
    target_name = Path(target_path).name.lower()
    allow_name_fallback = _is_name_only_target(target_path)
    for _ in range(retries):
        doc = _find_document_by_path(target_path)
        if doc is None:
            time.sleep(delay)
            continue
        try:
            doc.Activate()
        except Exception:
            time.sleep(delay)
            continue
        time.sleep(delay)
        try:
            active = C.acad.ActiveDocument
            active_name = str(getattr(active, "Name", "") or "").lower()
            if active and (
                _normalize_path(active.FullName) == wanted
                or (allow_name_fallback and active_name == target_name)
            ):
                return True
        except Exception:
            pass
    return False


def _close_document_by_path(target_path: str | Path, save_changes: bool = False) -> bool:
    doc = _find_document_by_path(target_path)
    if doc is None:
        return True
    try:
        doc.Close(bool(save_changes))
        return True
    except Exception:
        return False


def _load_jobs_from_plan_json(plan_json_path: Path) -> dict[str, list[dict[str, Any]]]:
    raw = json.loads(plan_json_path.read_text(encoding="utf-8"))
    return raw["jobs_by_space"]


def run_content_analysis_case(
    *,
    dwg_path: Path,
    output_path: Path,
    plan_json_path: Path | None = None,
    mode: str = PRINT_MODE_ADAPTIVE,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: list[str] | None = None,
    keep_open: bool = False,
) -> dict[str, Any]:
    if not dwg_path.exists():
        raise FileNotFoundError(dwg_path)

    launch_cad_guardians()
    assert_runtime_guard_ok("print_content_analysis:after_launch_guardians")

    need_open = _find_document_by_path(dwg_path) is None
    if need_open:
        if not open_file(str(dwg_path)):
            raise RuntimeError(f"打开 DWG 失败: {dwg_path}")
    if not _activate_document_by_path(dwg_path):
        raise RuntimeError(f"未能激活 DWG: {dwg_path}")
    wait_quiescent(min_quiet=0.5, timeout=20.0)
    assert_runtime_guard_ok("print_content_analysis:after_open_dwg")

    if plan_json_path and plan_json_path.exists():
        jobs_by_space = _load_jobs_from_plan_json(plan_json_path)
    else:
        plan = build_print_plan(
            str(dwg_path),
            output_path.parent / "_tmp_pdf",
            mode=normalize_print_mode(mode),
            include_model=include_model,
            include_layouts=include_layouts,
            only_layouts=only_layouts,
        )
        jobs_by_space = plan_to_dict(plan)["jobs_by_space"]
    assert_runtime_guard_ok("print_content_analysis:before_analyze_jobs")

    analysis = analyze_jobs_content(jobs_by_space)
    result = {
        "dwg_path": str(dwg_path),
        "plan_json_path": str(plan_json_path) if plan_json_path else "",
        "mode": normalize_print_mode(mode),
        **analysis,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if not keep_open and need_open:
        _close_document_by_path(dwg_path, save_changes=False)
    return result


def main() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--dwg", required=True, help="source dwg path")
    parser.add_argument("--plan-json", default="", help="existing print plan json")
    parser.add_argument("--output", default="", help="output json path")
    parser.add_argument("--mode", default=PRINT_MODE_ADAPTIVE, help="basic/adaptive/purified_adaptive")
    parser.add_argument("--layout", action="append", default=None, help="only analyze specified layout, repeatable")
    parser.add_argument("--no-model", action="store_true", help="skip model space when building plan")
    parser.add_argument("--no-layouts", action="store_true", help="skip layout spaces when building plan")
    parser.add_argument("--keep-open", action="store_true", help="keep dwg open after analysis")
    args = parser.parse_args()

    dwg_path = Path(args.dwg)
    plan_json_path = Path(args.plan_json) if args.plan_json else None
    if args.output:
        output_path = Path(args.output)
    elif plan_json_path:
        output_path = plan_json_path.parent / "content_analysis.json"
    else:
        output_path = MODULE_DIR / "cases" / "output" / dwg_path.stem / "content_analysis.json"

    try:
        result = run_content_analysis_case(
            dwg_path=dwg_path,
            output_path=output_path,
            plan_json_path=plan_json_path,
            mode=args.mode,
            include_model=not args.no_model,
            include_layouts=not args.no_layouts,
            only_layouts=args.layout,
            keep_open=args.keep_open,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except RuntimeGuardTriggered as exc:
        print(json.dumps(render_guard_error(exc), ensure_ascii=False, indent=2))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
