#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os
import subprocess
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
from system.CAD_core import _place_window_bottom_right_quarter, _resize_windows_for_background_use, set_space_mode, switch_to_layout
from system.CAD_coordination import wait_quiescent
from system.runtime_guard_bridge import assert_runtime_guard_ok
from cad_control import activate_window_by_title

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


WPS_WINDOW_KEYWORDS = ("WPS OFFICE", "WPS PDF")
WPS_PROCESS_IMAGES = ("wps.exe", "wpspdf.exe")


def _keep_wps_windows_bottom_right() -> None:
    try:
        _resize_windows_for_background_use(
            process_names=WPS_PROCESS_IMAGES,
            title_keywords=WPS_WINDOW_KEYWORDS,
            corner="bottom-right",
        )
    except Exception:
        pass


def _wait_for_pdf_ready(pdf_path: str | Path, timeout: float = 90.0) -> bool:
    target = Path(pdf_path)
    deadline = time.time() + timeout
    while time.time() < deadline:
        _keep_wps_windows_bottom_right()
        if target.exists():
            try:
                if target.stat().st_size > 0:
                    _keep_wps_windows_bottom_right()
                    with target.open("rb"):
                        pass
                    return True
            except OSError:
                pass
        time.sleep(0.5)
    return False


def _normalize_path(path: str | Path) -> str:
    return str(Path(path).resolve()).lower()


def _is_name_only_target(target_path: str | Path) -> bool:
    raw = str(target_path)
    return Path(raw).name.lower() == raw.lower()


def _active_doc_matches(target_path: str | Path) -> bool:
    wanted = _normalize_path(target_path)
    target_name = Path(target_path).name.lower()
    allow_name_fallback = _is_name_only_target(target_path)
    try:
        active = C.raw_doc
        active_name = str(getattr(active, "Name", "") or "").lower()
        return bool(
            active
            and (
                _normalize_path(active.FullName) == wanted
                or (allow_name_fallback and active_name == target_name)
            )
        )
    except Exception:
        return False


def _activate_document_by_path(target_path: str | Path, retries: int = 6, delay: float = 0.6) -> bool:
    wanted = _normalize_path(target_path)
    target_name = Path(target_path).name.lower()
    allow_name_fallback = _is_name_only_target(target_path)
    for _ in range(retries):
        try:
            docs = C.acad.Documents
        except Exception:
            time.sleep(delay)
            continue
        found = False
        for doc in docs:
            try:
                doc_name = str(getattr(doc, "Name", "") or "").lower()
                if _normalize_path(doc.FullName) != wanted and not (allow_name_fallback and doc_name == target_name):
                    continue
                found = True
                doc.Activate()
                time.sleep(delay)
                if _active_doc_matches(target_path):
                    return True
            except Exception:
                continue
        if not found:
            time.sleep(delay)
            continue
        time.sleep(delay)
    return False


def _ensure_model_doc_ready(target_path: str | Path, retries: int = 3) -> bool:
    for attempt in range(retries):
        try:
            wait_quiescent(min_quiet=0.5, timeout=15.0)
        except Exception:
            pass
        if not _activate_document_by_path(target_path):
            time.sleep(0.8 * (attempt + 1))
            continue
        try:
            set_space_mode(1)
            wait_quiescent(min_quiet=0.5, timeout=15.0)
        except Exception:
            time.sleep(0.8 * (attempt + 1))
            continue
        if _active_doc_matches(target_path):
            return True
    return False


def _ensure_layout_doc_ready(target_path: str | Path, layout_name: str, retries: int = 4) -> bool:
    for attempt in range(retries):
        try:
            wait_quiescent(min_quiet=0.5, timeout=15.0)
        except Exception:
            pass
        if not _activate_document_by_path(target_path):
            time.sleep(0.8 * (attempt + 1))
            continue
        try:
            set_space_mode(0)
            wait_quiescent(min_quiet=0.5, timeout=15.0)
            if not switch_to_layout(layout_name):
                raise RuntimeError(f"切换布局失败: {layout_name}")
            wait_quiescent(min_quiet=0.5, timeout=15.0)
            active = C.raw_doc
            active_layout = str(active.ActiveLayout.Name)
            if _active_doc_matches(target_path) and active_layout == layout_name:
                return True
        except Exception as exc:
            sys_logger.warning(
                f"布局预备失败，准备重试: layout={layout_name} attempt={attempt + 1}/{retries} err={exc}"
            )
        time.sleep(0.8 * (attempt + 1))
    return False


def export_model_window_lisp_fit(
    point_a,
    point_b,
    pdf_fullpath: str,
    dwg_path: str,
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

    if not _ensure_model_doc_ready(dwg_path):
        sys_logger.error(f"模型空间预备失败: {dwg_path}")
        return False

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
    dwg_path: str,
    layout_name: str,
    *,
    device: str,
    media: str,
    ctb: str,
    rotation: int,
) -> bool:
    if not _ensure_layout_doc_ready(dwg_path, layout_name):
        sys_logger.error(f"布局预备失败: layout={layout_name} dwg={dwg_path}")
        return False
    doc = C.doc
    time.sleep(1.0)

    if os.path.exists(pdf_fullpath):
        try:
            os.remove(pdf_fullpath)
        except OSError:
            pass

    orientation = "Portrait" if int(rotation) == 1 else "Landscape"
    output_path = str(pdf_fullpath).replace("\\", "/")
    p1 = f"{point_a[0]},{point_a[1]}"
    p2 = f"{point_b[0]},{point_b[1]}"
    command = (
        '(command "._-plot" '
        f'"Yes" "{layout_name}" "{device}" "{media}" "Millimeters" '
        f'"{orientation}" "No" "Window" "{p1}" "{p2}" '
        f'"Fit" "Center" "Yes" "{ctb}" "Yes" "No" "No" "No" '
        f'"{output_path}" "No" "Yes")'
    )
    doc.SendCommand(command + "\n")

    ok = _wait_for_pdf_ready(pdf_fullpath)
    if not ok:
        sys_logger.error(f"布局打印失败: layout={layout_name} file={pdf_fullpath}")
    return ok


def _is_wps_window_title(title: str) -> bool:
    title_upper = str(title or "").upper()
    return any(keyword in title_upper for keyword in WPS_WINDOW_KEYWORDS)


def _enumerate_wps_windows() -> list[dict[str, int | str]]:
    try:
        import win32gui
        import win32process
    except ImportError:
        return []

    windows: list[dict[str, int | str]] = []

    def callback(hwnd, _extra):
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return
            title = str(win32gui.GetWindowText(hwnd) or "").strip()
            if not title or not _is_wps_window_title(title):
                return
            _thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
            windows.append({"hwnd": int(hwnd), "pid": int(pid or 0), "title": title})
        except Exception:
            return

    win32gui.EnumWindows(callback, None)
    return windows


def _kill_process_tree(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/PID", str(pid), "/T"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return False
    return result.returncode == 0


def _kill_process_by_image(image_name: str) -> bool:
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", image_name, "/T"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return False
    return result.returncode == 0


def cleanup_wps_windows() -> None:
    try:
        import win32con
        import win32gui
    except ImportError:
        return

    observed_windows: list[dict[str, int | str]] = []
    for attempt in range(3):
        current_windows = _enumerate_wps_windows()
        if not current_windows:
            break
        observed_windows = current_windows
        _keep_wps_windows_bottom_right()
        for window in current_windows:
            try:
                hwnd = int(window["hwnd"])
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.2)
                try:
                    _place_window_bottom_right_quarter(hwnd)
                    time.sleep(0.2)
                except Exception:
                    pass
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            except Exception:
                pass
        sys_logger.info(
            f"WPS 清理轮次 {attempt + 1}/3: windows={len(current_windows)}"
        )
        time.sleep(0.8)

    residual_windows = _enumerate_wps_windows()
    candidate_pids = {
        int(window["pid"])
        for window in [*observed_windows, *residual_windows]
        if int(window.get("pid", 0) or 0) > 0
    }
    killed_pids: list[int] = []
    if candidate_pids:
        for pid in sorted(candidate_pids):
            if _kill_process_tree(pid):
                killed_pids.append(pid)
        time.sleep(0.8)
    if observed_windows or residual_windows:
        for image_name in WPS_PROCESS_IMAGES:
            _kill_process_by_image(image_name)
        time.sleep(0.8)
        residual_windows = _enumerate_wps_windows()

    if observed_windows or residual_windows or killed_pids:
        sys_logger.info(
            "WPS 清理结果: "
            f"observed={len(observed_windows)} "
            f"killed_pids={len(killed_pids)} "
            f"remaining={len(residual_windows)}"
        )

    for title in ("AutoCAD", "天正"):
        try:
            if activate_window_by_title(title, click_titlebar=False):
                time.sleep(1.0)
                break
        except Exception:
            continue


def _cleanup_wps_if_needed(success_count: int, defaults: PrintDefaults, *, force: bool = False) -> None:
    if defaults.wps_close_threshold <= 0:
        return
    if not force:
        if success_count <= 0:
            return
        if success_count % defaults.wps_close_threshold != 0:
            return
    time.sleep(0.5)
    cleanup_wps_windows()


def _run_job(job: PrintJob, defaults: PrintDefaults) -> bool:
    output_path = Path(job.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if job.space_kind == "model":
        return export_model_window_lisp_fit(
            job.lower_left,
            job.upper_right,
            str(output_path),
            job.dwg_path,
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
        job.dwg_path,
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
            batch_name = "landscape" if batch is landscapes else "portrait"
            assert_runtime_guard_ok(f"print_executor:before_batch:{layout_name}:{batch_name}")
            for job in batch:
                assert_runtime_guard_ok(f"print_executor:before_job:{layout_name}:{job.handle}")
                try:
                    ok = _run_job(job, defaults)
                except Exception as exc:
                    ok = False
                    sys_logger.error(f"打印异常: layout={layout_name} handle={job.handle} err={exc}")
                if ok:
                    success_count += 1
                    generated_files.append(job.output_path)
                    time.sleep(1.5)
                    _cleanup_wps_if_needed(success_count, defaults)
                else:
                    failures.append(
                        {
                            "layout_name": job.layout_name,
                            "handle": job.handle,
                            "output_path": job.output_path,
                        }
                    )

            if batch is landscapes and landscapes and portraits:
                _cleanup_wps_if_needed(success_count, defaults, force=True)
                sys_logger.info(f"横向打印完成，等待 {defaults.safety_delay} 秒后打印竖向")
                time.sleep(defaults.safety_delay)

        _cleanup_wps_if_needed(success_count, defaults, force=True)

    return PrintExecutionSummary(
        total_jobs=plan.total_jobs,
        success_count=success_count,
        failure_count=len(failures),
        generated_files=generated_files,
        failures=failures,
    )
