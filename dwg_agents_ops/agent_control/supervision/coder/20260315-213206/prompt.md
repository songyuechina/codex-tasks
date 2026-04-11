# Supervised Task Packet
role: coder
title: print-supervision-smoke

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦实现推进，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。

## Objective
用不超过6行说明当前打印实现已覆盖什么，以及下一步最值得补强的一项。

## Context
不要搜索其他路径；只基于主控提供的上下文回答。

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
