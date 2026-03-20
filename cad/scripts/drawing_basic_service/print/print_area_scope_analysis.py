#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any


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

from system.licad import C
from system.CAD_core import launch_cad_guardians, open_file
from system.CAD_coordination import wait_quiescent

from print_area_analysis import _bbox_xy, get_pseudo_maximal_polylines
from print_policy import reindex_jobs_by_space


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


def _area_from_bbox(bbox: tuple[float, float, float, float]) -> float:
    return max((bbox[2] - bbox[0]) * (bbox[3] - bbox[1]), 0.0)


def analyze_pseudo_maximal_scopes() -> dict[str, Any]:
    grouped = get_pseudo_maximal_polylines()
    rows_by_space: dict[str, list[dict[str, Any]]] = {}
    all_rows: list[dict[str, Any]] = []

    def _append(space_key: str, layout_name: str, owner_btr: str, polys: list[Any]) -> None:
        rows: list[dict[str, Any]] = []
        for poly in polys:
            bbox = _bbox_xy(poly)
            if bbox is None:
                continue
            handle = str(getattr(poly, "Handle", ""))
            row = {
                "space_key": space_key,
                "layout_name": layout_name,
                "owner_btr": owner_btr,
                "handle": handle,
                "bbox": bbox,
                "area": _area_from_bbox(bbox),
            }
            rows.append(row)
            all_rows.append(row)
        if rows:
            rows_by_space[space_key] = sorted(rows, key=lambda item: item["area"], reverse=True)

    _append("model", "model", "*MODEL_SPACE", grouped.get("model", []))
    for owner_btr, polys in (grouped.get("papers", {}) or {}).items():
        _append(str(owner_btr), str(owner_btr), str(owner_btr), polys)

    largest = max(all_rows, key=lambda item: item["area"], default=None)
    return {
        "total_pseudo_maximal_count": len(all_rows),
        "rows_by_space": rows_by_space,
        "largest_scope": largest,
    }


def _job_inside_scope(job: Any, scope_bbox: tuple[float, float, float, float], tol: float = 1.0) -> bool:
    if isinstance(job, dict):
        x1, y1 = job["lower_left"]
        x2, y2 = job["upper_right"]
    else:
        x1, y1 = job.lower_left
        x2, y2 = job.upper_right
    return (
        x1 >= scope_bbox[0] - tol
        and y1 >= scope_bbox[1] - tol
        and x2 <= scope_bbox[2] + tol
        and y2 <= scope_bbox[3] + tol
    )


def filter_jobs_by_largest_pseudo_scope(
    jobs_by_space: dict[str, list[Any]],
    scope_payload: dict[str, Any],
) -> dict[str, Any]:
    largest = scope_payload.get("largest_scope")
    if not largest:
        return {
            "applied": False,
            "reason": "no_pseudo_maximal_scope",
            "jobs_by_space": jobs_by_space,
            "selected_scope": None,
        }

    selected_layout = str(largest["layout_name"])
    selected_bbox = tuple(largest["bbox"])
    filtered: dict[str, list[Any]] = {}
    for layout_name, jobs in jobs_by_space.items():
        if str(layout_name) != selected_layout:
            continue
        kept = [job for job in jobs if _job_inside_scope(job, selected_bbox)]
        if kept:
            filtered[layout_name] = kept

    if not filtered:
        return {
            "applied": False,
            "reason": "no_jobs_inside_scope",
            "jobs_by_space": jobs_by_space,
            "selected_scope": largest,
        }

    return {
        "applied": True,
        "reason": "largest_pseudo_maximal_scope",
        "jobs_by_space": reindex_jobs_by_space(filtered),
        "selected_scope": largest,
    }


def run_scope_analysis_case(
    *,
    dwg_path: Path,
    output_path: Path | None = None,
    keep_open: bool = False,
) -> dict[str, Any]:
    launch_cad_guardians()

    need_open = _find_document_by_path(dwg_path) is None
    if need_open:
        if not open_file(str(dwg_path)):
            raise RuntimeError(f"打开 DWG 失败: {dwg_path}")
    if not _activate_document_by_path(dwg_path):
        raise RuntimeError(f"未能激活 DWG: {dwg_path}")
    wait_quiescent(min_quiet=0.5, timeout=20.0)

    result = {
        "dwg_path": str(dwg_path),
        **analyze_pseudo_maximal_scopes(),
    }
    if output_path is not None:
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
    parser.add_argument("--output", default="", help="output json path")
    parser.add_argument("--keep-open", action="store_true", help="keep dwg open after analysis")
    args = parser.parse_args()

    output_path = Path(args.output) if args.output else None
    result = run_scope_analysis_case(
        dwg_path=Path(args.dwg),
        output_path=output_path,
        keep_open=args.keep_open,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()
