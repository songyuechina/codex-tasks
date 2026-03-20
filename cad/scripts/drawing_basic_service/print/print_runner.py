#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path


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

from system.common_logger import sys_logger
from system.CAD_core import launch_cad_guardians, open_file
from system.CAD_coordination import wait_quiescent
from system.licad import C

from print_area_content_analysis import analyze_jobs_content
from print_area_scope_analysis import filter_jobs_by_largest_pseudo_scope, run_scope_analysis_case
from print_executor import PrintDefaults, execute_print_plan
from print_policy import (
    PRINT_MODE_BASIC,
    PRINT_MODE_PURIFIED_ADAPTIVE,
    assign_output_paths,
    build_print_plan,
    filter_jobs_by_handles,
    normalize_print_mode,
    plan_to_dict,
    save_plan_json,
)
from print_verifier import verify_generated_pdfs


DEFAULT_CASE = MODULE_DIR / "cases" / "assets" / "混合空间0109.dwg"


def _make_process_token(dwg_path: Path) -> str:
    digest = hashlib.md5(str(dwg_path).encode("utf-8")).hexdigest()[:10]
    return f"case-{digest}"


def _make_run_dirs(dwg_path: Path, output_root: Path) -> tuple[Path, Path, Path]:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_root = output_root / _make_process_token(dwg_path) / stamp
    work_dir = run_root / "work"
    pdf_dir = run_root / "pdf"
    work_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    return run_root, work_dir, pdf_dir


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
        time.sleep(delay)
    return False


def _close_document_by_path(target_path: str | Path, save_changes: bool = False) -> bool:
    doc = _find_document_by_path(target_path)
    if doc is None:
        return True
    try:
        doc.Close(bool(save_changes))
        return True
    except Exception as exc:
        sys_logger.warning(f"关闭工作 DWG 失败: {exc}")
        return False


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def run_print_case(
    dwg_path: Path,
    output_root: Path,
    *,
    mode: str = PRINT_MODE_BASIC,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: list[str] | None = None,
    dry_run: bool = False,
    keep_open: bool = False,
    safety_delay: int = 60,
    wps_threshold: int = 6,
) -> dict:
    if not dwg_path.exists():
        raise FileNotFoundError(dwg_path)
    mode = normalize_print_mode(mode)

    launch_cad_guardians()

    run_root, work_dir, pdf_dir = _make_run_dirs(dwg_path, output_root)
    process_token = _make_process_token(dwg_path)
    process_source_stem = f"plot-{process_token}"
    work_dwg = work_dir / f"work-{process_token}{dwg_path.suffix}"
    shutil.copy2(dwg_path, work_dwg)

    if not open_file(str(work_dwg)):
        raise RuntimeError(f"打开 DWG 失败: {work_dwg}")
    if not _activate_document_by_path(work_dwg):
        raise RuntimeError(f"未能激活工作 DWG: {work_dwg}")
    wait_quiescent(min_quiet=0.5, timeout=20.0)

    scope_analysis_payload: dict | None = None
    scope_analysis_path: Path | None = None
    scope_filter_summary: dict | None = None
    if mode == PRINT_MODE_PURIFIED_ADAPTIVE:
        scope_analysis_payload = run_scope_analysis_case(
            dwg_path=work_dwg,
            output_path=None,
            keep_open=True,
        )
        scope_analysis_path = _write_json(run_root / "scope_analysis.json", scope_analysis_payload)

    plan = build_print_plan(
        str(work_dwg),
        pdf_dir,
        mode=mode,
        source_stem=process_source_stem,
        include_model=include_model,
        include_layouts=include_layouts,
        only_layouts=only_layouts,
    )
    content_analysis_path: Path | None = None
    if mode == PRINT_MODE_PURIFIED_ADAPTIVE:
        content_payload = {
            "dwg_path": str(work_dwg),
            "mode": mode,
            **analyze_jobs_content(plan.jobs_by_space),
        }
        content_analysis_path = _write_json(run_root / "content_analysis.json", content_payload)
        pseudo_handles = {str(item["handle"]) for item in content_payload.get("pseudo_candidates", [])}
        if pseudo_handles and scope_analysis_payload:
            scope_filter_result = filter_jobs_by_largest_pseudo_scope(
                plan.jobs_by_space,
                scope_analysis_payload,
            )
            scope_filter_summary = {
                "applied": bool(scope_filter_result["applied"]),
                "reason": scope_filter_result["reason"],
                "selected_scope": scope_filter_result["selected_scope"],
            }
            if scope_filter_result["applied"]:
                plan.jobs_by_space = scope_filter_result["jobs_by_space"]
                assign_output_paths(
                    plan.jobs_by_space,
                    output_root=pdf_dir,
                    source_stem=plan.source_stem,
                )
        if pseudo_handles:
            plan.jobs_by_space = filter_jobs_by_handles(plan.jobs_by_space, pseudo_handles)
            assign_output_paths(
                plan.jobs_by_space,
                output_root=pdf_dir,
                source_stem=plan.source_stem,
            )

    plan_json = save_plan_json(plan, run_root / "print_plan.json")

    summary = {
        "run_root": str(run_root),
        "work_dwg": str(work_dwg),
        "process_token": process_token,
        "mode": mode,
        "plan_json": str(plan_json),
        "plan": plan_to_dict(plan),
        "content_analysis_json": str(content_analysis_path) if content_analysis_path else "",
        "scope_analysis_json": str(scope_analysis_path) if scope_analysis_path else "",
        "scope_filter": scope_filter_summary,
    }

    if not dry_run and plan.total_jobs > 0:
        all_jobs = [job for jobs in plan.jobs_by_space.values() for job in jobs]
        execution = execute_print_plan(
            plan,
            defaults=PrintDefaults(
                safety_delay=safety_delay,
                wps_close_threshold=wps_threshold,
            ),
        )
        verification = verify_generated_pdfs(execution.generated_files, jobs=all_jobs)
        summary["execution"] = {
            "total_jobs": execution.total_jobs,
            "success_count": execution.success_count,
            "failure_count": execution.failure_count,
            "generated_files": execution.generated_files,
            "failures": execution.failures,
        }
        summary["verification"] = verification
    else:
        summary["execution"] = None
        summary["verification"] = None

    summary_path = run_root / "print_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    summary["summary_path"] = str(summary_path)

    if not keep_open:
        try:
            _close_document_by_path(work_dwg, save_changes=False)
        except Exception:
            pass

    return summary


def main() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--dwg", default=str(DEFAULT_CASE), help="source dwg path")
    parser.add_argument("--output-root", default=str(MODULE_DIR / "cases" / "output"), help="output root directory")
    parser.add_argument("--mode", default=PRINT_MODE_BASIC, help="basic/adaptive/purified_adaptive")
    parser.add_argument("--layout", action="append", default=None, help="only print specified layout, repeatable")
    parser.add_argument("--no-model", action="store_true", help="skip model space")
    parser.add_argument("--no-layouts", action="store_true", help="skip layout spaces")
    parser.add_argument("--dry-run", action="store_true", help="analyze only, do not print")
    parser.add_argument("--keep-open", action="store_true", help="keep dwg open after run")
    parser.add_argument("--safety-delay", type=int, default=60, help="wait seconds between landscape and portrait")
    parser.add_argument("--wps-threshold", type=int, default=6, help="close WPS every N successful plots")
    args = parser.parse_args()

    result = run_print_case(
        Path(args.dwg),
        Path(args.output_root),
        mode=args.mode,
        include_model=not args.no_model,
        include_layouts=not args.no_layouts,
        only_layouts=args.layout,
        dry_run=args.dry_run,
        keep_open=args.keep_open,
        safety_delay=args.safety_delay,
        wps_threshold=args.wps_threshold,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
