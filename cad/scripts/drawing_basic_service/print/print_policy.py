#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional
import json
import sys


MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent
if str(current) not in sys.path:
    sys.path.insert(0, str(current))

from system.licad import C
from system.common_logger import sys_logger
from system.CAD_core import get_layout_names
from scripts.drawing_basic_service.print.print_area_analysis import (
    get_print_area_polylines,
    match_standard_print_by_mode,
)


ROW_FACTOR = 2000.0 / 42000.0
MODEL_LAYOUT_NAME = "model"
PRINT_MODE_BASIC = "basic"
PRINT_MODE_ADAPTIVE = "adaptive"
PRINT_MODE_PURIFIED_ADAPTIVE = "purified_adaptive"
PRINT_MODES = (
    PRINT_MODE_BASIC,
    PRINT_MODE_ADAPTIVE,
    PRINT_MODE_PURIFIED_ADAPTIVE,
)


@dataclass
class PrintJob:
    dwg_path: str
    space_kind: str
    layout_name: str
    owner_btr: str
    handle: str
    lower_left: tuple[float, float]
    upper_right: tuple[float, float]
    short_side: float
    long_side: float
    media: str
    ratio: str
    paper_code: str
    rotation: int
    plot_scale: float
    standard_flag: int
    sequence_no: int = 0
    output_path: str = ""


@dataclass
class PrintPlan:
    dwg_path: str
    output_root: str
    source_stem: str
    mode: str
    jobs_by_space: dict[str, list[PrintJob]]

    @property
    def total_jobs(self) -> int:
        return sum(len(items) for items in self.jobs_by_space.values())

    @property
    def landscape_count(self) -> int:
        return sum(1 for items in self.jobs_by_space.values() for job in items if job.rotation == 0)

    @property
    def portrait_count(self) -> int:
        return sum(1 for items in self.jobs_by_space.values() for job in items if job.rotation == 1)


def _safe_handle(obj: Any) -> str:
    try:
        return str(obj.Handle)
    except Exception:
        return str(id(obj))


def _get_bbox(poly: Any) -> Optional[tuple[float, float, float, float]]:
    try:
        p1, p2 = poly.GetBoundingBox()
        min_x = min(float(p1[0]), float(p2[0]))
        min_y = min(float(p1[1]), float(p2[1]))
        max_x = max(float(p1[0]), float(p2[0]))
        max_y = max(float(p1[1]), float(p2[1]))
        return min_x, min_y, max_x, max_y
    except Exception as exc:
        sys_logger.warning(f"获取打印区域包围盒失败: handle={_safe_handle(poly)} err={exc}")
        return None


def _layout_name_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    try:
        for layout in C.doc.Layouts:
            try:
                mapping[str(layout.Block.Name)] = str(layout.Name)
            except Exception:
                continue
    except Exception as exc:
        sys_logger.warning(f"解析布局/BTR 映射失败: {exc}")
    return mapping


def _sanitize_name(name: str) -> str:
    sanitized = "".join("_" if ch in '<>:"/\\|?*' else ch for ch in name.strip())
    return sanitized or "unknown"


def _contains_bbox(
    outer: tuple[float, float, float, float],
    inner: tuple[float, float, float, float],
    tol: float = 1e-6,
) -> bool:
    return (
        outer[0] <= inner[0] + tol
        and outer[1] <= inner[1] + tol
        and outer[2] >= inner[2] - tol
        and outer[3] >= inner[3] - tol
    )


def normalize_print_mode(mode: str | None) -> str:
    normalized = str(mode or PRINT_MODE_BASIC).strip().lower().replace("-", "_")
    if normalized not in PRINT_MODES:
        raise ValueError(f"不支持的打印模式: {mode}")
    return normalized


def _area_match_mode(mode: str) -> str:
    normalized = normalize_print_mode(mode)
    if normalized == PRINT_MODE_BASIC:
        return PRINT_MODE_BASIC
    return PRINT_MODE_ADAPTIVE


def _make_job(
    poly: Any,
    dwg_path: str,
    space_kind: str,
    layout_name: str,
    owner_btr: str,
    *,
    mode: str,
) -> Optional[PrintJob]:
    bbox = _get_bbox(poly)
    if bbox is None:
        return None
    matched = match_standard_print_by_mode(poly, _area_match_mode(mode))
    if not matched:
        sys_logger.warning(f"无法匹配标准图幅，跳过: handle={_safe_handle(poly)}")
        return None

    min_x, min_y, max_x, max_y = bbox
    dx = max_x - min_x
    dy = max_y - min_y
    media, ratio, paper_code, rotation, plot_scale, standard_flag = matched
    return PrintJob(
        dwg_path=dwg_path,
        space_kind=space_kind,
        layout_name=layout_name,
        owner_btr=owner_btr,
        handle=_safe_handle(poly),
        lower_left=(min_x, min_y),
        upper_right=(max_x, max_y),
        short_side=min(abs(dx), abs(dy)),
        long_side=max(abs(dx), abs(dy)),
        media=media,
        ratio=ratio,
        paper_code=paper_code,
        rotation=int(rotation),
        plot_scale=float(plot_scale),
        standard_flag=int(standard_flag),
    )


def _collect_layout_viewports(layout_name: str) -> list[Any]:
    try:
        layout = C.doc.Layouts.Item(layout_name)
    except Exception as exc:
        sys_logger.warning(f"读取布局失败: layout={layout_name} err={exc}")
        return []

    candidates: list[tuple[Any, tuple[float, float, float, float], float]] = []
    for ent in layout.Block:
        if getattr(ent, "ObjectName", "") != "AcDbViewport":
            continue
        bbox = _get_bbox(ent)
        if bbox is None:
            continue
        min_x, min_y, max_x, max_y = bbox
        width = abs(max_x - min_x)
        height = abs(max_y - min_y)
        area = width * height
        if width <= 1.0 or height <= 1.0 or area <= 1.0:
            continue
        candidates.append((ent, bbox, area))

    filtered: list[Any] = []
    for ent, bbox, area in candidates:
        is_container = False
        for other_ent, other_bbox, other_area in candidates:
            if _safe_handle(ent) == _safe_handle(other_ent):
                continue
            if area > other_area and _contains_bbox(bbox, other_bbox, tol=1.0):
                is_container = True
                break
        if not is_container:
            filtered.append(ent)
    return filtered


def _sort_jobs(jobs: list[PrintJob]) -> list[PrintJob]:
    if not jobs:
        return []

    ordered = sorted(jobs, key=lambda item: (-item.lower_left[1], item.lower_left[0]))
    rows: list[list[PrintJob]] = []
    row_anchor_y: Optional[float] = None
    row_short_side = 0.0

    for job in ordered:
        if row_anchor_y is None:
            rows.append([job])
            row_anchor_y = job.lower_left[1]
            row_short_side = job.short_side
            continue

        tolerance = min(row_short_side, job.short_side) * ROW_FACTOR
        if abs(job.lower_left[1] - row_anchor_y) <= tolerance:
            rows[-1].append(job)
            row_short_side = min(row_short_side, job.short_side)
        else:
            rows.append([job])
            row_anchor_y = job.lower_left[1]
            row_short_side = job.short_side

    result: list[PrintJob] = []
    for row in rows:
        result.extend(sorted(row, key=lambda item: item.lower_left[0]))
    return result


def collect_print_jobs(
    dwg_path: str,
    *,
    mode: str = PRINT_MODE_BASIC,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Optional[list[str]] = None,
) -> dict[str, list[PrintJob]]:
    """
    当前默认策略遵循用户最新约定：
    - 若文件同时包含模型空间和布局空间打印区域，默认两者都输出
    - 但排序与执行计划按空间独立
    """
    mode = normalize_print_mode(mode)
    areas = get_print_area_polylines()
    layout_map = _layout_name_map()
    selected_layouts = {name.lower() for name in only_layouts or []}
    jobs_by_space: dict[str, list[PrintJob]] = {}

    if include_model:
        model_jobs = [
            _make_job(poly, dwg_path, "model", MODEL_LAYOUT_NAME, "*MODEL_SPACE", mode=mode)
            for poly in areas.get("model", [])
        ]
        model_jobs = [job for job in model_jobs if job is not None]
        if model_jobs:
            jobs_by_space[MODEL_LAYOUT_NAME] = _sort_jobs(model_jobs)

    if include_layouts:
        layout_names_in_order = get_layout_names(exclude_model=True) or []
        papers = areas.get("papers", {})
        pending_by_layout: dict[str, list[PrintJob]] = {}
        for owner_btr, polylines in papers.items():
            layout_name = layout_map.get(owner_btr, owner_btr)
            if selected_layouts and layout_name.lower() not in selected_layouts:
                continue
            job_list = pending_by_layout.setdefault(layout_name, [])
            for poly in polylines:
                job = _make_job(poly, dwg_path, "layout", layout_name, owner_btr, mode=mode)
                if job is not None:
                    job_list.append(job)

        for layout_name in layout_names_in_order:
            if selected_layouts and layout_name.lower() not in selected_layouts:
                continue
            viewport_jobs = [
                _make_job(vp, dwg_path, "layout", layout_name, f"layout_viewport:{layout_name}", mode=mode)
                for vp in _collect_layout_viewports(layout_name)
            ]
            viewport_jobs = [job for job in viewport_jobs if job is not None]
            if viewport_jobs:
                pending_by_layout.setdefault(layout_name, []).extend(viewport_jobs)

        for layout_name in layout_names_in_order:
            job_list = pending_by_layout.get(layout_name, [])
            if job_list:
                jobs_by_space[layout_name] = _sort_jobs(job_list)

        for layout_name, job_list in pending_by_layout.items():
            if layout_name not in jobs_by_space and job_list:
                jobs_by_space[layout_name] = _sort_jobs(job_list)

    for layout_name, job_list in jobs_by_space.items():
        for index, job in enumerate(job_list, start=1):
            job.sequence_no = index

    return jobs_by_space


def reindex_jobs_by_space(jobs_by_space: dict[str, list[PrintJob]]) -> dict[str, list[PrintJob]]:
    normalized: dict[str, list[PrintJob]] = {}
    for layout_name, job_list in jobs_by_space.items():
        ordered = _sort_jobs(list(job_list))
        for index, job in enumerate(ordered, start=1):
            job.sequence_no = index
        if ordered:
            normalized[layout_name] = ordered
    return normalized


def assign_output_paths(
    jobs_by_space: dict[str, list[PrintJob]],
    *,
    output_root: str | Path,
    source_stem: str,
) -> None:
    output_root_path = Path(output_root)
    for layout_name, jobs in jobs_by_space.items():
        layout_dir = output_root_path / _sanitize_name(layout_name)
        for job in jobs:
            filename = f"{source_stem}-{_sanitize_name(layout_name)}-{job.sequence_no:02d}.pdf"
            job.output_path = str(layout_dir / filename)


def filter_jobs_by_handles(
    jobs_by_space: dict[str, list[PrintJob]],
    excluded_handles: set[str] | None = None,
) -> dict[str, list[PrintJob]]:
    excluded_handles = {str(item) for item in (excluded_handles or set())}
    filtered: dict[str, list[PrintJob]] = {}
    for layout_name, jobs in jobs_by_space.items():
        kept = [job for job in jobs if str(job.handle) not in excluded_handles]
        if kept:
            filtered[layout_name] = kept
    return reindex_jobs_by_space(filtered)


def build_print_plan(
    dwg_path: str,
    output_root: str | Path,
    *,
    mode: str = PRINT_MODE_BASIC,
    source_stem: str | None = None,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Optional[list[str]] = None,
) -> PrintPlan:
    dwg = Path(dwg_path)
    output_root_path = Path(output_root)
    output_stem = source_stem or dwg.stem
    mode = normalize_print_mode(mode)
    jobs_by_space = collect_print_jobs(
        str(dwg),
        mode=mode,
        include_model=include_model,
        include_layouts=include_layouts,
        only_layouts=only_layouts,
    )
    assign_output_paths(
        jobs_by_space,
        output_root=output_root_path,
        source_stem=output_stem,
    )

    return PrintPlan(
        dwg_path=str(dwg),
        output_root=str(output_root_path),
        source_stem=output_stem,
        mode=mode,
        jobs_by_space=jobs_by_space,
    )


def plan_to_dict(plan: PrintPlan) -> dict[str, Any]:
    return {
        "dwg_path": plan.dwg_path,
        "output_root": plan.output_root,
        "source_stem": plan.source_stem,
        "mode": plan.mode,
        "total_jobs": plan.total_jobs,
        "landscape_count": plan.landscape_count,
        "portrait_count": plan.portrait_count,
        "jobs_by_space": {
            layout_name: [asdict(job) for job in jobs]
            for layout_name, jobs in plan.jobs_by_space.items()
        },
    }


def save_plan_json(plan: PrintPlan, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(plan_to_dict(plan), ensure_ascii=False, indent=2), encoding="utf-8")
    return target
