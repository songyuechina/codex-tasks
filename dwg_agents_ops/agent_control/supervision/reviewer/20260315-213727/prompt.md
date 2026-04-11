# Supervised Task Packet
role: reviewer
title: print-review-supervised

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦 findings-first 审查，不要自行猜测工作区路径，严格基于主控提供的上下文回答。

## Objective
只基于给定文件内容，列出当前打印实现最重要的1-2个残余风险；如果没有高严重度问题，就明确说没有高严重度发现。

## Context
不要假设你能访问其他本地路径；不要输出伪工具调用。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.

## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/print_policy.py
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
from scripts.drawing_basic_service.print.print_area_analysis import get_print_area_polylines, match_nearest_standard_print


ROW_FACTOR = 2000.0 / 42000.0
MODEL_LAYOUT_NAME = "model"


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
    sequence_no: int = 0
    output_path: str = ""


@dataclass
class PrintPlan:
    dwg_path: str
    output_root: str
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


def _make_job(poly: Any, dwg_path: str, space_kind: str, layout_name: str, owner_btr: str) -> Optional[PrintJob]:
    bbox = _get_bbox(poly)
    if bbox is None:
        return None
    matched = match_nearest_standard_print(poly)
    if not matched:
        sys_logger.warning(f"无法匹配标准图幅，跳过: handle={_safe_handle(poly)}")
        return None

    min_x, min_y, max_x, max_y = bbox
    dx = max_x - min_x
    dy = max_y - min_y
    media, ratio, paper_code, rotation, plot_scale = matched
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
    )


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
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Optional[list[str]] = None,
) -> dict[str, list[PrintJob]]:
    """
    当前默认策略遵循用户最新约定：
    - 若文件同时包含模型空间和布局空间打印区域，默认两者都输出
    - 但排序与执行计划按空间独立
    """
    areas = get_print_area_polylines()
    layout_map = _layout_name_map()
    selected_layouts = {name.lower() for name in only_layouts or []}
    jobs_by_space: dict[str, list[PrintJob]] = {}

    if include_model:
        model_jobs = [
            _make_job(poly, dwg_path, "model", MODEL_LAYOUT_NAME, "*MODEL_SPACE")
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
                job = _make_job(poly, dwg_path, "layout", layout_name, owner_btr)
                if job is not None:
                    job_list.append(job)

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


def build_print_plan(
    dwg_path: str,
    output_root: str | Path,
    *,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Optional[list[str]] = None,
) -> PrintPlan:
    dwg = Path(dwg_path)
    output_root_path = Path(output_root)
    jobs_by_space = collect_print_jobs(
        str(dwg),
        include_model=include_model,
        include_layouts=include_layouts,
        only_layouts=only_layouts,
    )

    for layout_name, jobs in jobs_by_space.items():
        layout_dir = output_root_path / _sanitize_name(layout_name)
        for job in jobs:
            filename = f"{dwg.stem}-{_sanitize_name(layout_name)}-{job.sequence_no:02d}.pdf"
            job.output_path = str(layout_dir / filename)

    return PrintPlan(
        dwg_path=str(dwg),
        output_root=str(output_root_path),
        jobs_by_space=jobs_by_space,
    )


def plan_to_dict(plan: PrintPlan) -> dict[str, Any]:
    return {
        "dwg_path": plan.dwg_path,
        "output_root": plan.output_root,
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


## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/print_verifier.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path


def verify_generated_pdfs(output_paths: list[str]) -> dict:
    existing = []
    missing = []
    zero_size = []
    for item in output_paths:
        path = Path(item)
        if not path.exists():
            missing.append(str(path))
            continue
        if path.stat().st_size <= 0:
            zero_size.append(str(path))
            continue
        existing.append(str(path))

    return {
        "expected_count": len(output_paths),
        "existing_count": len(existing),
        "missing_count": len(missing),
        "zero_size_count": len(zero_size),
        "existing": existing,
        "missing": missing,
        "zero_size": zero_size,
    }
