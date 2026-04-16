#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

import fitz


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
SCRIPTS_DIR = current / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from system.common_logger import sys_logger
from system.CAD_coordination import wait_quiescent
from system.CAD_core import (
    cad_zt_oneb,
    close_current_dwg_paradigm,
    copy_file_content_pywin32,
    new_file,
    open_file,
    save_current_dwg_paradigm,
)
from system.licad import C

from print_info_analysis import run_print_info_case
from print_pdf_naming import copy_named_pdfs_from_print_info
from print_runner import _close_document_by_path, _normalize_path, run_print_case


BLANK_RATIO_THRESHOLD = 0.002


def _is_dispatch_source_dwg(path: Path) -> bool:
    name = path.name
    if name.endswith("_打印区域.dwg"):
        return False
    if "__blankfix" in name:
        return False
    return True


def _derive_public_base_name(path: Path) -> str:
    stem = path.stem.strip()
    label = re.sub(r"[\(（][^()（）]*(?:版|修改|修订)[^()（）]*[\)）]\s*$", "", stem).strip()
    label = re.sub(r"[-_－—]?\d+(?:\.\d+)*(?:[_-][A-Za-z0-9]+)*\s*$", "", label).strip()
    label = label.rstrip("-_－— ").strip()
    return label or stem


def _reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True, exist_ok=True)


def _prepare_public_output_dirs(dwg_path: Path, process_stamp: str) -> dict[str, Path]:
    base_name = _derive_public_base_name(dwg_path)
    parent = dwg_path.parent
    pdf_dir = parent / f"{base_name}pdf"
    analysis_dir = parent / f"{base_name}analysis"
    process_base_dir = parent / f"{base_name}prosess"
    process_run_dir = process_base_dir / process_stamp

    _reset_dir(pdf_dir)
    _reset_dir(analysis_dir)
    process_run_dir.mkdir(parents=True, exist_ok=True)
    return {
        "base_name": Path(base_name),
        "pdf_dir": pdf_dir,
        "analysis_dir": analysis_dir,
        "process_base_dir": process_base_dir,
        "process_run_dir": process_run_dir,
    }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_batch_summary(
    *,
    summary_root: Path,
    batch_root: Path,
    mode: str,
    dwg_files: list[Path],
    summary_rows: list[dict[str, Any]],
) -> Path:
    batch_summary_path = batch_root / "batch_summary.json"
    batch_summary_path.write_text(
        json.dumps(
            {
                "input_dir": str(summary_root),
                "output_root": str(batch_root),
                "mode": mode,
                "dwg_count": len(dwg_files),
                "items": summary_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return batch_summary_path


def _close_case_documents(case_paths: set[Path]) -> dict[str, Any]:
    wanted_paths = {_normalize_path(path) for path in case_paths if path}
    wanted_names = {Path(path).name.lower() for path in case_paths if path}
    closed: list[str] = []
    failed: list[dict[str, str]] = []

    if not wanted_paths and not wanted_names:
        return {
            "closed_count": 0,
            "failed_count": 0,
            "remaining_count": 0,
            "closed": closed,
            "failed": failed,
            "remaining": [],
        }

    for _ in range(3):
        pending: list[tuple[Any, str]] = []
        try:
            docs = list(C.acad.Documents)
        except Exception:
            docs = []

        for doc in docs:
            try:
                full_name = _normalize_path(doc.FullName)
            except Exception:
                full_name = ""
            try:
                doc_name = str(getattr(doc, "Name", "") or "").lower()
            except Exception:
                doc_name = ""
            if full_name in wanted_paths or doc_name in wanted_names:
                pending.append((doc, full_name or doc_name))

        if not pending:
            break

        for doc, label in pending:
            try:
                doc.Activate()
            except Exception:
                pass
            try:
                wait_quiescent(min_quiet=0.2, timeout=5.0)
            except Exception:
                pass
            try:
                doc.Close(False)
                closed.append(label)
            except Exception as exc:
                failed.append({"target": label, "error": str(exc)})
        time.sleep(0.5)

    remaining: list[str] = []
    try:
        docs = list(C.acad.Documents)
    except Exception:
        docs = []
    for doc in docs:
        try:
            full_name = _normalize_path(doc.FullName)
        except Exception:
            full_name = ""
        try:
            doc_name = str(getattr(doc, "Name", "") or "").lower()
        except Exception:
            doc_name = ""
        if full_name in wanted_paths or doc_name in wanted_names:
            remaining.append(full_name or doc_name)

    if closed or failed or remaining:
        sys_logger.info(
            f"单 DWG 收尾关图: closed={len(closed)} failed={len(failed)} remaining={len(remaining)}"
        )

    return {
        "closed_count": len(closed),
        "failed_count": len(failed),
        "remaining_count": len(remaining),
        "closed": closed,
        "failed": failed,
        "remaining": remaining,
    }


def _normalize_cad_runtime_after_case() -> dict[str, Any]:
    try:
        ok = bool(cad_zt_oneb())
        payload = {
            "attempted": True,
            "ok": ok,
            "target_state": "one_process_one_blank_tarch",
            "action": "cad_zt_oneb",
        }
        if ok:
            sys_logger.info("单 DWG 收尾后已执行 CAD 归一：cad_zt_oneb")
        else:
            sys_logger.warning("单 DWG 收尾后 CAD 归一返回 False：cad_zt_oneb")
        return payload
    except Exception as exc:
        sys_logger.error(f"单 DWG 收尾后 CAD 归一失败: {exc}")
        return {
            "attempted": True,
            "ok": False,
            "target_state": "one_process_one_blank_tarch",
            "action": "cad_zt_oneb",
            "error": str(exc),
        }


def _render_nonwhite_ratio(pdf_path: Path, scale: float = 0.12) -> list[float]:
    ratios: list[float] = []
    doc = fitz.open(pdf_path)
    try:
        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
            total = max(pix.width * pix.height, 1)
            data = pix.samples
            nonwhite = 0
            for index in range(0, len(data), 3):
                if data[index] < 250 or data[index + 1] < 250 or data[index + 2] < 250:
                    nonwhite += 1
            ratios.append(nonwhite / total)
    finally:
        doc.close()
    return ratios


def detect_blank_pdfs(pdf_paths: list[str], threshold: float = BLANK_RATIO_THRESHOLD) -> list[dict[str, Any]]:
    suspects: list[dict[str, Any]] = []
    for item in pdf_paths:
        pdf_path = Path(item)
        try:
            ratios = _render_nonwhite_ratio(pdf_path)
        except Exception as exc:
            suspects.append(
                {
                    "pdf_path": str(pdf_path),
                    "reason": "render_failed",
                    "error": str(exc),
                }
            )
            continue
        if not ratios:
            suspects.append(
                {
                    "pdf_path": str(pdf_path),
                    "reason": "no_pages",
                    "ratios": ratios,
                }
            )
            continue
        max_ratio = max(ratios)
        if max_ratio <= threshold:
            suspects.append(
                {
                    "pdf_path": str(pdf_path),
                    "reason": "visual_blank",
                    "ratios": ratios,
                    "threshold": threshold,
                }
            )
    return suspects


def _job_index_from_plan(plan_json_path: Path) -> dict[str, dict[str, Any]]:
    raw = _load_json(plan_json_path)
    index: dict[str, dict[str, Any]] = {}
    for jobs in raw.get("jobs_by_space", {}).values():
        for job in jobs:
            output_path = str(Path(job["output_path"]))
            index[output_path] = job
    return index


def _selected_job_rows(plan_json_path: Path, selected_handles: list[str]) -> list[dict[str, Any]]:
    wanted = {str(item) for item in selected_handles}
    if not wanted:
        return []
    rows: list[dict[str, Any]] = []
    raw = _load_json(plan_json_path)
    for jobs in raw.get("jobs_by_space", {}).values():
        for job in jobs:
            if str(job.get("handle", "")) in wanted:
                rows.append(job)
    return rows


def _ratio_to_visual_width(ratio: str) -> int:
    text = str(ratio or "").strip()
    match = re.search(r"1\s*:\s*([0-9]+(?:\.[0-9]+)?)", text)
    if not match:
        return 100
    try:
        denominator = float(match.group(1))
    except Exception:
        return 100
    # 用户给出的口径存在重复示例，这里按两档处理：
    # 1:1 / 1:1.5 / 1:2.5 / 1:5 这类大比例图，线宽取 1；
    # 其余常见 1:25 / 1:50 / 1:100 / 1:150 这类缩尺图，线宽取 100。
    return 1 if denominator <= 5.0 else 100


def _set_entity_visual_style(entity: Any, width_value: int) -> None:
    try:
        entity.Color = 1
    except Exception:
        pass
    try:
        entity.Lineweight = int(width_value)
    except Exception:
        pass

    obj_name = str(getattr(entity, "ObjectName", "") or "")
    if obj_name in {"AcDbPolyline", "AcDb2dPolyline", "AcDb3dPolyline", "Polyline"}:
        for attr_name in ("ConstantWidth", "GlobalWidth"):
            try:
                setattr(entity, attr_name, float(width_value))
                return
            except Exception:
                continue


def _make_print_area_visual_copy(
    *,
    source_dwg: Path,
    plan_json_path: Path,
    selected_handles: list[str],
) -> str:
    jobs = _selected_job_rows(plan_json_path, selected_handles)
    if not jobs:
        return ""

    target_dwg = source_dwg.with_name(f"{source_dwg.stem}_打印区域{source_dwg.suffix}")
    try:
        _close_document_by_path(target_dwg, save_changes=False)
    except Exception:
        pass
    shutil.copy2(source_dwg, target_dwg)
    try:
        os.chmod(target_dwg, 0o666)
    except Exception:
        pass

    if not open_file(str(target_dwg)):
        raise RuntimeError(f"打开打印区域显示副本失败: {target_dwg}")
    wait_quiescent(min_quiet=0.5, timeout=20.0)

    doc = C.raw_doc
    touched = 0
    for job in jobs:
        handle = str(job.get("handle", ""))
        if not handle:
            continue
        try:
            entity = doc.HandleToObject(handle)
        except Exception:
            continue
        width_value = _ratio_to_visual_width(str(job.get("ratio", "")))
        _set_entity_visual_style(entity, width_value)
        touched += 1

    try:
        doc.Regen(1)
    except Exception:
        pass
    save_current_dwg_paradigm()
    _close_document_by_path(target_dwg, save_changes=False)
    sys_logger.info(f"打印区域显示副本已生成: {target_dwg} touched={touched}")
    return str(target_dwg)


def _make_blank_fix_copy(source_dwg: Path, repaired_dwg: Path) -> bool:
    repaired_dwg.parent.mkdir(parents=True, exist_ok=True)
    sys_logger.info(f"开始创建空白补救副本: {repaired_dwg}")
    if not new_file(str(repaired_dwg), close_after=False):
        return False
    wait_quiescent(min_quiet=0.5, timeout=20.0)
    if not copy_file_content_pywin32(str(source_dwg), str(repaired_dwg), explode=True):
        return False
    wait_quiescent(min_quiet=0.5, timeout=20.0)
    try:
        close_current_dwg_paradigm("save")
    except Exception:
        pass
    time.sleep(1.0)
    return repaired_dwg.exists()


def _copy_final_outputs(
    *,
    source_dwg: Path,
    output_dir: Path,
    original_job_index: dict[str, dict[str, Any]],
    original_existing: list[str],
    blank_pdf_paths: set[str],
    repaired_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    selected_handles: list[str] = []
    unresolved: list[dict[str, Any]] = []

    repaired_job_index: dict[tuple[str, int], dict[str, Any]] = {}
    repaired_existing: set[str] = set()
    if repaired_summary:
        repaired_plan_json = Path(repaired_summary["plan_json"])
        repaired_job_index = {
            (str(job["layout_name"]), int(job["sequence_no"])): job
            for job in _job_index_from_plan(repaired_plan_json).values()
        }
        repaired_existing = set(
            repaired_summary.get("verification", {}).get("existing", [])
            or repaired_summary.get("execution", {}).get("generated_files", [])
            or []
        )

    for original_pdf in original_existing:
        original_key = str(Path(original_pdf))
        job = original_job_index.get(original_key)
        if not job:
            continue

        chosen_pdf = original_key
        if original_key in blank_pdf_paths:
            repaired_job = repaired_job_index.get((str(job["layout_name"]), int(job["sequence_no"])))
            repaired_pdf = None
            if repaired_job:
                candidate = str(Path(repaired_job["output_path"]))
                if candidate in repaired_existing and Path(candidate).exists():
                    repaired_pdf = candidate
            if repaired_pdf:
                chosen_pdf = repaired_pdf
            else:
                unresolved.append(
                    {
                        "layout_name": job["layout_name"],
                        "sequence_no": int(job["sequence_no"]),
                        "original_output_path": original_key,
                        "reason": "blank_pdf_not_replaced",
                    }
                )
                continue

        target_name = f"{source_dwg.stem}-{job['layout_name']}-{int(job['sequence_no']):02d}.pdf"
        target_path = output_dir / target_name
        shutil.copy2(chosen_pdf, target_path)
        copied.append(str(target_path))
        selected_handles.append(str(job["handle"]))

    return {
        "copied_count": len(copied),
        "final_output_paths": copied,
        "selected_handles": selected_handles,
        "unresolved_outputs": unresolved,
    }


def run_directory_dispatch(
    *,
    dwg_files: list[Path],
    summary_root: Path,
    output_root: Path,
    mode: str,
    project_name: str = "",
    subproject_name: str = "",
    drawing_no_prefix: str = "",
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: list[str] | None = None,
) -> dict[str, Any]:
    batch_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    batch_root = output_root / f"batch-{batch_stamp}"
    batch_root.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict[str, Any]] = []
    for dwg_path in dwg_files:
        sys_logger.info(f"开始处理: {dwg_path}")
        case_started_at = datetime.now()
        row: dict[str, Any] | None = None
        primary_work_dwg: Path | None = None
        case_cleanup_paths: set[Path] = {dwg_path}
        try:
            public_dirs = _prepare_public_output_dirs(dwg_path, batch_stamp)
            runs_root = public_dirs["process_run_dir"] / "runs"
            analysis_output = public_dirs["analysis_dir"] / "print_info_analysis.json"
            row = {
                "dwg_path": str(dwg_path),
                "mode": mode,
                "include_model": bool(include_model),
                "include_layouts": bool(include_layouts),
                "only_layouts": list(only_layouts or []),
                "started_at": case_started_at.strftime("%Y-%m-%d %H:%M:%S"),
                "final_pdf_dir": str(public_dirs["pdf_dir"]),
                "analysis_dir": str(public_dirs["analysis_dir"]),
                "process_dir": str(public_dirs["process_run_dir"]),
            }
            print_summary = run_print_case(
                dwg_path,
                runs_root,
                mode=mode,
                include_model=include_model,
                include_layouts=include_layouts,
                only_layouts=only_layouts,
                keep_open=False,
            )
            primary_work_dwg = Path(print_summary["work_dwg"])
            case_cleanup_paths.add(primary_work_dwg)
            row["initial_run_root"] = print_summary["run_root"]
            row["initial_print_summary"] = str(Path(print_summary["summary_path"]))
            row["initial_started_at"] = print_summary.get("started_at", "")
            row["initial_finished_at"] = print_summary.get("finished_at", "")
            row["initial_elapsed_seconds"] = float(print_summary.get("elapsed_seconds", 0.0) or 0.0)
            row["initial_stage_durations"] = print_summary.get("stage_durations", {}) or {}
            row["initial_total_jobs"] = int((print_summary.get("plan") or {}).get("total_jobs", 0) or 0)
            verification = print_summary.get("verification") or {}
            existing = verification.get("existing", []) or []
            row["initial_existing_count"] = int(verification.get("existing_count", 0) or 0)
            row["initial_failure_count"] = int((print_summary.get("execution") or {}).get("failure_count", 0) or 0)
            row["initial_zero_size_count"] = int(verification.get("zero_size_count", 0) or 0)
            row["initial_page_mismatch_count"] = int(
                ((verification.get("page_verification") or {}).get("page_size_mismatch_count", 0) or 0)
            )

            blank_suspects = detect_blank_pdfs(existing)
            row["blank_pdf_count"] = len(blank_suspects)
            row["blank_pdf_suspects"] = blank_suspects

            repaired_summary: dict[str, Any] | None = None
            if blank_suspects and include_model:
                repaired_dir = public_dirs["process_run_dir"] / "blank-fix"
                repaired_dwg = repaired_dir / f"{dwg_path.stem}__blankfix.dwg"
                case_cleanup_paths.add(repaired_dwg)
                row["blank_fix_applied"] = True
                row["repaired_dwg_path"] = str(repaired_dwg)
                row["blank_fix_created"] = _make_blank_fix_copy(dwg_path, repaired_dwg)
                if row["blank_fix_created"]:
                    repaired_summary = run_print_case(
                        repaired_dwg,
                        runs_root,
                        mode=mode,
                        include_layouts=False,
                    )
                    case_cleanup_paths.add(Path(repaired_summary["work_dwg"]))
                    row["repaired_run_root"] = repaired_summary["run_root"]
                    row["repaired_print_summary"] = str(Path(repaired_summary["summary_path"]))
                else:
                    row["repaired_run_root"] = ""
                    row["repaired_print_summary"] = ""
            elif blank_suspects:
                row["blank_fix_applied"] = False
                row["blank_fix_skipped_reason"] = "model_space_not_selected"
            else:
                row["blank_fix_applied"] = False

            plan_json_path = Path(print_summary["plan_json"])
            content_json_raw = print_summary.get("content_analysis_json", "")
            content_json_path = Path(content_json_raw) if content_json_raw else None
            analysis = run_print_info_case(
                dwg_path=Path(print_summary["work_dwg"]),
                output_path=analysis_output,
                source_dwg_path=dwg_path,
                plan_json_path=plan_json_path,
                content_json_path=content_json_path,
                mode=mode,
                include_model=include_model,
                include_layouts=include_layouts,
                only_layouts=only_layouts,
            )
            row["analysis_json"] = str(analysis_output)
            row["analysis_excel"] = str(Path(analysis["excel_path"]))
            row["analysis_total_jobs"] = int(analysis["total_jobs"])
            row["analysis_with_title_count"] = int(analysis["with_title_count"])
            row["analysis_with_drawing_no_count"] = int(analysis["with_drawing_no_count"])
            row["analysis_with_project_count"] = int(analysis["with_project_count"])

            final_copy = _copy_final_outputs(
                source_dwg=dwg_path,
                output_dir=public_dirs["pdf_dir"],
                original_job_index=_job_index_from_plan(plan_json_path),
                original_existing=existing,
                blank_pdf_paths={str(Path(item["pdf_path"])) for item in blank_suspects},
                repaired_summary=repaired_summary,
            )
            final_blank_suspects = detect_blank_pdfs(final_copy["final_output_paths"])
            if final_blank_suspects:
                blank_names = {Path(item["pdf_path"]).name for item in final_blank_suspects}
                kept_paths: list[str] = []
                kept_handles: list[str] = []
                for pdf_path, handle in zip(final_copy["final_output_paths"], final_copy["selected_handles"]):
                    if Path(pdf_path).name in blank_names:
                        try:
                            Path(pdf_path).unlink(missing_ok=True)
                        except Exception:
                            pass
                        continue
                    kept_paths.append(pdf_path)
                    kept_handles.append(handle)
                final_copy["final_blank_filtered"] = final_blank_suspects
                final_copy["final_blank_filtered_count"] = len(final_blank_suspects)
                final_copy["final_output_paths"] = kept_paths
                final_copy["selected_handles"] = kept_handles
                final_copy["copied_count"] = len(kept_paths)
            else:
                final_copy["final_blank_filtered"] = []
                final_copy["final_blank_filtered_count"] = 0
            row.update(final_copy)

            row["print_area_visual_dwg"] = _make_print_area_visual_copy(
                source_dwg=dwg_path,
                plan_json_path=plan_json_path,
                selected_handles=row["selected_handles"],
            )
            if row["print_area_visual_dwg"]:
                case_cleanup_paths.add(Path(row["print_area_visual_dwg"]))

            if row["final_blank_filtered_count"] > 0 and row["selected_handles"]:
                analysis = run_print_info_case(
                    dwg_path=Path(print_summary["work_dwg"]),
                    output_path=analysis_output,
                    source_dwg_path=dwg_path,
                    plan_json_path=plan_json_path,
                    content_json_path=content_json_path,
                    mode=mode,
                    include_model=include_model,
                    include_layouts=include_layouts,
                    only_layouts=only_layouts,
                    requested_handles=set(row["selected_handles"]),
                )
                row["analysis_total_jobs"] = int(analysis["total_jobs"])
                row["analysis_with_title_count"] = int(analysis["with_title_count"])
                row["analysis_with_drawing_no_count"] = int(analysis["with_drawing_no_count"])
                row["analysis_with_project_count"] = int(analysis["with_project_count"])

            try:
                named_copy = copy_named_pdfs_from_print_info(
                    print_info=analysis,
                    output_dir=public_dirs["pdf_dir"] / "named",
                    pdf_paths=row.get("final_output_paths", []) or [],
                    selected_handles=row.get("selected_handles", []) or [],
                    project_name=project_name,
                    subproject_name=subproject_name,
                    drawing_no_prefix=drawing_no_prefix,
                )
            except Exception as exc:
                named_copy = {
                    "named_pdf_dir": str(public_dirs["pdf_dir"] / "named"),
                    "named_pdf_count": 0,
                    "named_pdf_paths": [],
                    "named_pdf_items": [],
                    "named_pdf_unresolved": [{"reason": "named_pdf_copy_failed", "error": str(exc)}],
                }
                sys_logger.warning(f"按打印信息命名 PDF 副本失败: dwg={dwg_path} err={exc}")
            row.update(named_copy)

            if row["initial_total_jobs"] == 0 and row["analysis_total_jobs"] == 0:
                row["status"] = "completed_no_valid_print_areas"
                row["no_valid_print_areas"] = True
                row["completion_reason"] = "purified_adaptive 下未识别到有效打印区域"
            elif row["initial_total_jobs"] > 0 and row["copied_count"] == 0:
                row["status"] = "failed"
                row["no_valid_print_areas"] = False
                row["completion_reason"] = "已生成打印计划，但未形成最终可交付 PDF"
            else:
                row["status"] = "success"
                row["no_valid_print_areas"] = False
                row["completion_reason"] = ""
            summary_rows.append(row)

        except Exception as exc:
            row = {
                "dwg_path": str(dwg_path),
                "mode": mode,
                "status": "failed",
                "error": str(exc),
                "final_pdf_dir": "",
                "analysis_dir": "",
                "process_dir": "",
            }
            summary_rows.append(row)
            sys_logger.error(f"批量任务单文件失败: dwg={dwg_path} err={exc}")
        finally:
            if primary_work_dwg:
                try:
                    _close_document_by_path(primary_work_dwg, save_changes=False)
                except Exception:
                    pass
            cleanup = _close_case_documents(case_cleanup_paths)
            if row is not None:
                row["cleanup_closed_count"] = cleanup["closed_count"]
                row["cleanup_failed_count"] = cleanup["failed_count"]
                row["cleanup_remaining_count"] = cleanup["remaining_count"]
                row["post_case_runtime_reset"] = _normalize_cad_runtime_after_case()
                case_finished_at = datetime.now()
                row["finished_at"] = case_finished_at.strftime("%Y-%m-%d %H:%M:%S")
                row["elapsed_seconds"] = round((case_finished_at - case_started_at).total_seconds(), 3)
            else:
                _normalize_cad_runtime_after_case()
            _write_batch_summary(
                summary_root=summary_root,
                batch_root=batch_root,
                mode=mode,
                dwg_files=dwg_files,
                summary_rows=summary_rows,
            )

    return {
        "input_dir": str(summary_root),
        "output_root": str(batch_root),
        "mode": mode,
        "dwg_count": len(dwg_files),
        "items": summary_rows,
        "summary_json": str(
            _write_batch_summary(
                summary_root=summary_root,
                batch_root=batch_root,
                mode=mode,
                dwg_files=dwg_files,
                summary_rows=summary_rows,
            )
        ),
    }


def main() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="", help="directory containing dwg files")
    parser.add_argument("--dwg", default="", help="single dwg file path")
    parser.add_argument("--output-root", default="", help="batch output root")
    parser.add_argument("--mode", default="purified_adaptive", help="print mode")
    parser.add_argument("--project-name", default="", help="project name used for named pdf copies")
    parser.add_argument("--subproject-name", default="", help="subproject name used for named pdf copies")
    parser.add_argument("--drawing-no-prefix", default="", help="prefix added before drawing number in named pdf copies")
    parser.add_argument("--layout", action="append", default=None, help="only print/analyze specified layout, repeatable")
    parser.add_argument("--no-model", action="store_true", help="skip model space")
    parser.add_argument("--no-layouts", action="store_true", help="skip layout spaces")
    args = parser.parse_args()

    if bool(args.input_dir) == bool(args.dwg):
        raise SystemExit("必须且只能提供 --input-dir 或 --dwg 之一")
    if args.layout and args.no_layouts:
        raise SystemExit("--layout 与 --no-layouts 不能同时使用")

    if args.dwg:
        dwg_path = Path(args.dwg)
        dwg_files = [dwg_path]
        summary_root = dwg_path.parent
    else:
        input_dir = Path(args.input_dir)
        dwg_files = sorted(path for path in input_dir.glob("*.dwg") if _is_dispatch_source_dwg(path))
        summary_root = input_dir

    output_root = Path(args.output_root) if args.output_root else summary_root / "print-agent-output"
    result = run_directory_dispatch(
        dwg_files=dwg_files,
        summary_root=summary_root,
        output_root=output_root,
        mode=args.mode,
        project_name=args.project_name,
        subproject_name=args.subproject_name,
        drawing_no_prefix=args.drawing_no_prefix,
        include_model=not args.no_model,
        include_layouts=not args.no_layouts,
        only_layouts=args.layout,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
