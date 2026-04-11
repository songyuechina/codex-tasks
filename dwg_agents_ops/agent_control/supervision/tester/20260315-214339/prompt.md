# Supervised Task Packet
role: tester
title: print-test-supervision

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦测试结论与阻塞，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。

## Objective
基于给定结果，用不超过6行说明这次打印验证已经覆盖什么、还缺什么。

## Context
不要搜索其他路径；只基于主控提供的上下文回答。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.

## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/print_executor.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os
import sys
import time


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
LIBRARY_DIR = current / "library"
if str(LIBRARY_DIR) not in sys.path:
    sys.path.insert(0, str(LIBRARY_DIR))

from system.common_logger import sys_logger
from system.licad import C
from system.CAD_core import set_space_mode, switch_to_layout
from system.CAD_coordination import wait_quiescent
from cad_control import activate_window_by_title, minimize_all_windows

from print_policy import PrintJob, PrintPlan


@dataclass
class PrintDefaults:
    device: str = "DWG To PDF.pc3"
    ctb: str = "monochrome.ctb"
    safety_delay: int = 60
    wps_close_threshold: int = 6
    model_window_compensation: float = 25.0


@dataclass
class PrintExecutionSummary:
    total_jobs: int
    success_count: int
    failure_count: int
    generated_files: list[str]
    failures: list[dict[str, str]]


def _wait_for_pdf_ready(pdf_path: str | Path, timeout: float = 90.0) -> bool:
    target = Path(pdf_path)
    deadline = time.time() + timeout
    while time.time() < deadline:
        if target.exists():
            try:
                if target.stat().st_size > 0:
                    with target.open("rb"):
                        pass
                    return True
            except OSError:
                pass
        time.sleep(0.5)
    return False


def export_model_window_lisp_fit(
    point_a,
    point_b,
    pdf_fullpath: str,
    *,
    device: str,
    media: str,
    ctb: str,
    rotation: int,
    xiubukuan: float = 25.0,
) -> bool:
    del xiubukuan
    doc = C.doc
    x1, y1 = float(point_a[0]), float(point_a[1])
    x2, y2 = float(point_b[0]), float(point_b[1])
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    orientation = "Portrait" if int(rotation) == 1 else "Landscape"
    output_path = str(pdf_fullpath).replace("\\", "/")

    try:
        set_space_mode(1)
        wait_quiescent(min_quiet=0.5, timeout=10.0)
    except Exception:
        pass

    if os.path.exists(pdf_fullpath):
        try:
            os.remove(pdf_fullpath)
        except OSError:
            pass

    command = (
        '(command "-plot" '
        f'"Yes" "Model" "{device}" "{media}" "Millimeters" '
        f'"{orientation}" "No" "Window" "{min_x},{min_y}" "{max_x},{max_y}" '
        f'"Fit" "Center" "Yes" "{ctb}" "Yes" "As displayed" '
        f'"{output_path}" "No" "Yes")'
    )
    doc.SendCommand(command + "\n")
    ok = _wait_for_pdf_ready(pdf_fullpath)
    if not ok:
        sys_logger.error(f"模型空间打印失败: {pdf_fullpath}")
    return ok


def export_layout_window_lisp_fit(
    point_a,
    point_b,
    pdf_fullpath: str,
    layout_name: str,
    *,
    device: str,
    media: str,
    ctb: str,
    rotation: int,
) -> bool:
    doc = C.doc
    set_space_mode(0)
    if not switch_to_layout(layout_name):
        sys_logger.error(f"切换布局失败: {layout_name}")
        return False
    wait_quiescent(min_quiet=0.5, timeout=10.0)
    time.sleep(1.0)

    if os.path.exists(pdf_fullpath):
        try:
            os.remove(pdf_fullpath)
        except OSError:
            pass

    orientation = "Portrait" if int(rotation) == 1 else "Landscape"
    output_path = str(pdf_fullpath).replace("\\", "/")
    commands = [
        "._-plot",
        "Yes",
        layout_name,
        device,
        media,
        "Millimeters",
        orientation,
        "No",
        "Window",
        f"{point_a[0]},{point_a[1]}",
        f"{point_b[0]},{point_b[1]}",
        "Fit",
        "Center",
        "Yes",
        ctb,
        "Yes",
        "No",
        "No",
        "No",
        output_path,
        "No",
        "Yes",
    ]

    try:
        doc.SendCommand("\x1b\x1b")
    except Exception:
        pass
    time.sleep(0.2)

    for item in commands:
        send_str = str(item)
        if " " in send_str and "," not in send_str and not send_str.startswith("."):
            send_str = f'"{send_str}"'
        doc.SendCommand(send_str + "\n")
        time.sleep(0.15)

    ok = _wait_for_pdf_ready(pdf_fullpath)
    if not ok:
        sys_logger.error(f"布局打印失败: layout={layout_name} file={pdf_fullpath}")
    return ok


def cleanup_wps_windows() -> None:
    try:
        import win32con
        import win32gui
    except ImportError:
        return

    for _ in range(3):
        found = False

        def callback(hwnd, _extra):
            nonlocal found
            title = win32gui.GetWindowText(hwnd)
            if "WPS Office" not in title or not win32gui.IsWindowVisible(hwnd):
                return
            found = True
            try:
                minimize_all_windows()
                time.sleep(0.5)
                activate_window_by_title("WPS Office", click_titlebar=True)
                time.sleep(0.5)
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            except Exception:
                pass

        win32gui.EnumWindows(callback, None)
        if not found:
            break
        time.sleep(0.5)

    try:
        activate_window_by_title("AutoCAD", click_titlebar=False)
        time.sleep(1.0)
    except Exception:
        pass


def _run_job(job: PrintJob, defaults: PrintDefaults) -> bool:
    output_path = Path(job.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if job.space_kind == "model":
        return export_model_window_lisp_fit(
            job.lower_left,
            job.upper_right,
            str(output_path),
            device=defaults.device,
            media=job.media,
            ctb=defaults.ctb,
            rotation=job.rotation,
            xiubukuan=defaults.model_window_compensation,
        )
    return export_layout_window_lisp_fit(
        job.lower_left,
        job.upper_right,
        str(output_path),
        job.layout_name,
        device=defaults.device,
        media=job.media,
        ctb=defaults.ctb,
        rotation=job.rotation,
    )


def execute_print_plan(plan: PrintPlan, defaults: Optional[PrintDefaults] = None) -> PrintExecutionSummary:
    defaults = defaults or PrintDefaults()
    generated_files: list[str] = []
    failures: list[dict[str, str]] = []
    success_count = 0

    for layout_name, jobs in plan.jobs_by_space.items():
        landscapes = [job for job in jobs if job.rotation == 0]
        portraits = [job for job in jobs if job.rotation == 1]

        for batch in (landscapes, portraits):
            for job in batch:
                try:
                    ok = _run_job(job, defaults)
                except Exception as exc:
                    ok = False
                    sys_logger.error(f"打印异常: layout={layout_name} handle={job.handle} err={exc}")
                if ok:
                    success_count += 1
                    generated_files.append(job.output_path)
                    time.sleep(1.5)
                    if defaults.wps_close_threshold > 0 and success_count % defaults.wps_close_threshold == 0:
                        cleanup_wps_windows()
                else:
                    failures.append(
                        {
                            "layout_name": job.layout_name,
                            "handle": job.handle,
                            "output_path": job.output_path,
                        }
                    )

            if batch is landscapes and landscapes and portraits:
                sys_logger.info(f"横向打印完成，等待 {defaults.safety_delay} 秒后打印竖向")
                time.sleep(defaults.safety_delay)

    return PrintExecutionSummary(
        total_jobs=plan.total_jobs,
        success_count=success_count,
        failure_count=len(failures),
        generated_files=generated_files,
        failures=failures,
    )


## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/print_runner.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import shutil
import sys
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
from system.CAD_core import close_current_dwg_paradigm, open_dwg_paradigm
from system.CAD_coordination import wait_quiescent

from print_executor import PrintDefaults, execute_print_plan
from print_policy import build_print_plan, plan_to_dict, save_plan_json
from print_verifier import verify_generated_pdfs


DEFAULT_CASE = MODULE_DIR / "cases" / "assets" / "混合空间0109.dwg"


def _make_run_dirs(dwg_path: Path, output_root: Path) -> tuple[Path, Path, Path]:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_root = output_root / dwg_path.stem / stamp
    work_dir = run_root / "work"
    pdf_dir = run_root / "pdf"
    work_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    return run_root, work_dir, pdf_dir


def run_print_case(
    dwg_path: Path,
    output_root: Path,
    *,
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

    run_root, work_dir, pdf_dir = _make_run_dirs(dwg_path, output_root)
    work_dwg = work_dir / dwg_path.name
    shutil.copy2(dwg_path, work_dwg)

    if not open_dwg_paradigm(str(work_dwg)):
        raise RuntimeError(f"打开 DWG 失败: {work_dwg}")
    wait_quiescent(min_quiet=0.5, timeout=20.0)

    plan = build_print_plan(
        str(work_dwg),
        pdf_dir,
        include_model=include_model,
        include_layouts=include_layouts,
        only_layouts=only_layouts,
    )
    plan_json = save_plan_json(plan, run_root / "print_plan.json")

    summary = {
        "run_root": str(run_root),
        "work_dwg": str(work_dwg),
        "plan_json": str(plan_json),
        "plan": plan_to_dict(plan),
    }

    if not dry_run and plan.total_jobs > 0:
        execution = execute_print_plan(
            plan,
            defaults=PrintDefaults(
                safety_delay=safety_delay,
                wps_close_threshold=wps_threshold,
            ),
        )
        verification = verify_generated_pdfs(execution.generated_files)
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
            close_current_dwg_paradigm(save_option="no_save")
        except Exception as exc:
            sys_logger.warning(f"关闭工作 DWG 失败: {exc}")

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


## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/cases/output/混合空间0109/20260315-195434/print_summary.json
{
  "run_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434",
  "work_dwg": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
  "plan_json": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\print_plan.json",
  "plan": {
    "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
    "output_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf",
    "total_jobs": 37,
    "landscape_count": 37,
    "portrait_count": 0,
    "jobs_by_space": {
      "model": [
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "12887",
          "lower_left": [
            380662.0,
            3073909.0
          ],
          "upper_right": [
            380872.0,
            3074057.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 1,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-01.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "12888",
          "lower_left": [
            380892.0,
            3073909.0
          ],
          "upper_right": [
            381102.0,
            3074057.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 2,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-02.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "12889",
          "lower_left": [
            381122.0,
            3073909.0
          ],
          "upper_right": [
            381332.0,
            3074057.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 3,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-03.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "1288A",
          "lower_left": [
            381351.0,
            3073909.0
          ],
          "upper_right": [
            381561.0,
            3074057.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 4,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-04.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "1288B",
          "lower_left": [
            381587.0,
            3073909.0
          ],
          "upper_right": [
            381797.0,
            3074057.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 5,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-05.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "1288C",
          "lower_left": [
            381825.0,
            3073909.0
          ],
          "upper_right": [
            382035.0,
            3074057.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 6,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-06.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "1288D",
          "lower_left": [
            382054.0,
            3073908.0
          ],
          "upper_right": [
            382264.0,
            3074056.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 7,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-07.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "1288E",
          "lower_left": [
            382287.0,
            3073908.0
          ],
          "upper_right": [
            382497.0,
            3074056.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 8,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-08.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "1288F",
          "lower_left": [
            382515.0,
            3073908.0
          ],
          "upper_right": [
            382725.0,
            3074056.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 9,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-09.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "12890",
          "lower_left": [
            382746.0,
            3073908.0
          ],
          "upper_right": [
            382956.0,
            3074056.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 10,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-10.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "12891",
          "lower_left": [
            382968.0,
            3073908.0
          ],
          "upper_right": [
            383178.0,
            3074056.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 11,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-11.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "12892",
          "lower_left": [
            383205.0,
            3073908.0
          ],
          "upper_right": [
            383415.0,
            3074056.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
          "paper_code": "A3",
          "rotation": 0,
          "plot_scale": 1.0,
          "sequence_no": 12,
          "output_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\pdf\\model\\混合空间0109-model-12.pdf"
        },
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260315-195434\\work\\混合空间0109.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "12893",
          "lower_left": [
            383434.0,
            3073908.0
          ],
          "upper_right": [
            383644.0,
            3074056.5
          ],
          "short_side": 148.5,
          "long_side": 210.0,
          "media": "ISO_A3_(420.00_x_297.00_MM)",
          "ratio": "1:50",
...[truncated]...
