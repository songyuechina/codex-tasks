#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CAD核心功能模块

提供CAD系统控制、文件操作、状态管理等核心功能
从 CAD_file_operations.py 拆分而来
"""

"""
本文件已按系统日志规则进行第二轮收束：
- 业务模块统一使用 system.common_logger.sys_logger
- 流程节点优先 info
- 降级/可恢复问题优先 warning
- 失败路径优先 error
- 本轮重点是日志规范化与切断旧依赖，不主动扩大功能改动面
"""
#D:/claude-tasks/cad/system/CAD_core.py

#&&&&%% （一）  可移植性导入
import sys
import os
import time
import shutil
import psutil
import subprocess
import math
from pathlib import Path

import win32api
import win32con
import win32gui
import win32process


# --- COM 相关库 ---
import pythoncom
import win32com.client
from win32com.client import VARIANT, constants

current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

from system.project_setup import PathConfig

from system.common_logger import sys_logger
from system import licad as licad_module
from system.licad import C, get_acad_doc

# 定义资源目录
XITONG_DIR = PathConfig.CAD_DIR / "xitongwenjian"
LOGS_DIR = PathConfig.CAD_DIR / "logs"
TESTS_DIR = PathConfig.WORKSPACE_DIR / "tests"
STATUS_MESSAGES_FILE = PathConfig.SCRIPTS_DIR / "CAD_status_messages.txt"

userpath=os.environ.get('USERPATH')


# ================= 3. 导入模块 =================

# 3.1 导入 System 工具
try:
    from system.CAD_com_utils import retry_on_busy, retry_if_busy,SafeCOM
except ImportError as e:
    sys_logger.critical(f"无法导入 CAD_com_utils: {e}")
    # 这里不raise，后续可能会定义假的 retry_on_busy 兜底

# 3.2 组合导入：替代对遗留 CAD_basic / CAD_file_operations 的依赖
from system.CAD_selection import com_retry, get_object_property, last_obj
from library.cad_blocks import safe_explode
from library.cad_control import group_bbox_corners, safe_delete
from library.cad_objects import ensure_list


def jingchengshu_wenjian() -> int:
    """返回当前 acad.exe 进程数量。"""
    total = 0
    for process in psutil.process_iter(["name"]):
        try:
            if str(process.info.get("name") or "").lower() == "acad.exe":
                total += 1
        except Exception:
            continue
    return total


def close_all_cad_processes(*, max_retries: int = 3, retry_delay: float = 2.0) -> bool:
    """强制关闭所有 acad.exe，并校验是否真正退出。"""
    for attempt in range(1, max_retries + 1):
        process_count = jingchengshu_wenjian()
        if process_count == 0:
            sys_logger.info("[close_all_cad_processes] 当前没有 CAD 进程")
            return True

        sys_logger.info(f"[close_all_cad_processes] 检测到 {process_count} 个 CAD 进程，执行关闭")
        try:
            result = subprocess.run(
                ["taskkill", "/F", "/IM", "acad.exe"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except subprocess.TimeoutExpired:
            result = None
            sys_logger.warning(f"[close_all_cad_processes] 第 {attempt} 次 taskkill 超时")

        if result is not None and result.returncode not in {0, 128}:
            sys_logger.warning(
                f"[close_all_cad_processes] taskkill 返回码={result.returncode} stdout={result.stdout!r}"
            )

        time.sleep(max(retry_delay, 0.5))
        if jingchengshu_wenjian() == 0:
            sys_logger.info("[close_all_cad_processes] 所有 CAD 进程已退出")
            return True

    sys_logger.error("[close_all_cad_processes] 多次尝试后仍有 CAD 进程残留")
    return False


def _find_main_window_by_pid(pid: int) -> int:
    """按 PID 查找可见的顶层主窗口句柄。"""
    matched_hwnds: list[int] = []

    def _enum_windows(hwnd: int, _: object) -> bool:
        try:
            if not win32gui.IsWindow(hwnd):
                return True
            if not win32gui.IsWindowVisible(hwnd):
                return True
            if win32gui.GetParent(hwnd):
                return True
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid != pid:
                return True
            title = str(win32gui.GetWindowText(hwnd) or "").strip()
            if not title:
                return True
            matched_hwnds.append(hwnd)
        except Exception:
            return True
        return True

    win32gui.EnumWindows(_enum_windows, None)
    if not matched_hwnds:
        return 0

    def _score(hwnd: int) -> tuple[int, int]:
        try:
            rect = win32gui.GetWindowRect(hwnd)
            width = max(0, rect[2] - rect[0])
            height = max(0, rect[3] - rect[1])
            return (width * height, hwnd)
        except Exception:
            return (0, hwnd)

    matched_hwnds.sort(key=_score, reverse=True)
    return int(matched_hwnds[0])


def _enumerate_visible_top_windows(
    *,
    process_names: tuple[str, ...] | list[str] | None = None,
    title_keywords: tuple[str, ...] | list[str] | None = None,
) -> list[dict[str, int | str]]:
    """枚举可见顶层窗口，并按进程名/标题关键词过滤。"""
    names = {str(name or "").strip().lower() for name in (process_names or []) if str(name or "").strip()}
    keywords = [str(keyword or "").strip().lower() for keyword in (title_keywords or []) if str(keyword or "").strip()]
    windows: list[dict[str, int | str]] = []

    def _enum_windows(hwnd: int, _: object) -> bool:
        try:
            if not win32gui.IsWindow(hwnd):
                return True
            if not win32gui.IsWindowVisible(hwnd):
                return True
            if win32gui.GetParent(hwnd):
                return True
            title = str(win32gui.GetWindowText(hwnd) or "").strip()
            if not title:
                return True
            _thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
            process_name = ""
            if pid:
                try:
                    process_name = str(psutil.Process(pid).name() or "")
                except Exception:
                    process_name = ""
            process_name_lower = process_name.lower()
            title_lower = title.lower()
            if names and process_name_lower not in names:
                if not (keywords and any(keyword in title_lower for keyword in keywords)):
                    return True
            elif keywords and not any(keyword in title_lower for keyword in keywords) and process_name_lower not in names:
                return True
            windows.append(
                {
                    "hwnd": int(hwnd),
                    "pid": int(pid or 0),
                    "process_name": process_name,
                    "title": title,
                }
            )
        except Exception:
            return True
        return True

    win32gui.EnumWindows(_enum_windows, None)
    return windows


def _get_secondary_work_area() -> tuple[int, int, int, int] | None:
    """优先返回次屏工作区；若不存在次屏则返回 None。"""
    try:
        monitors = []
        for handle, _hdc, _rect in win32api.EnumDisplayMonitors():
            monitor_info = win32api.GetMonitorInfo(handle)
            work_left, work_top, work_right, work_bottom = monitor_info.get("Work")
            monitors.append(
                {
                    "primary": bool(monitor_info.get("Flags", 0) & win32con.MONITORINFOF_PRIMARY),
                    "work": (
                        int(work_left),
                        int(work_top),
                        int(work_right),
                        int(work_bottom),
                    ),
                }
            )
        secondary = [item for item in monitors if not item["primary"]]
        if not secondary:
            return None
        secondary.sort(key=lambda item: (item["work"][0], item["work"][1]), reverse=True)
        return secondary[0]["work"]
    except Exception:
        return None


def _get_target_work_area_for_window(hwnd: int) -> tuple[int, int, int, int]:
    """优先取次屏工作区；若无次屏则退回窗口所在显示器，再退回主屏。"""
    secondary_work = _get_secondary_work_area()
    if secondary_work:
        return secondary_work

    try:
        monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
        monitor_info = win32api.GetMonitorInfo(monitor)
        work_left, work_top, work_right, work_bottom = monitor_info.get("Work")
        return int(work_left), int(work_top), int(work_right), int(work_bottom)
    except Exception:
        width = int(win32api.GetSystemMetrics(0))
        height = int(win32api.GetSystemMetrics(1))
        return 0, 0, width, height


def _place_window_quarter(
    hwnd: int,
    *,
    corner: str = "top-right",
    restore: bool = True,
) -> bool:
    """将窗口缩放到目标工作区 1/4，并放到指定角落。"""
    if not hwnd or not win32gui.IsWindow(hwnd):
        return False

    left, top, right, bottom = _get_target_work_area_for_window(hwnd)
    work_width = max(400, right - left)
    work_height = max(300, bottom - top)
    target_width = max(640, work_width // 2)
    target_height = max(480, work_height // 2)

    if corner == "top-left":
        target_x = left
        target_y = top
    elif corner == "bottom-left":
        target_x = left
        target_y = bottom - target_height
    elif corner == "bottom-right":
        target_x = right - target_width
        target_y = bottom - target_height
    else:
        target_x = right - target_width
        target_y = top

    if restore:
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        except Exception:
            pass

    try:
        flags = win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE | win32con.SWP_ASYNCWINDOWPOS
        win32gui.SetWindowPos(hwnd, 0, target_x, target_y, target_width, target_height, flags)
        return True
    except Exception as exc:
        sys_logger.warning(f"[_place_window_quarter] 调整窗口失败: hwnd={hwnd} corner={corner} exc={exc}")
        return False


def _place_window_top_right_quarter(hwnd: int) -> bool:
    """将窗口缩放到目标工作区 1/4，并优先放到次屏右上角。"""
    return _place_window_quarter(hwnd, corner="top-right")


def _place_window_bottom_right_quarter(hwnd: int) -> bool:
    """将窗口缩放到目标工作区 1/4，并优先放到次屏右下角。"""
    return _place_window_quarter(hwnd, corner="bottom-right")


def _resize_cad_window_for_background_use(pid: int, *, timeout: float = 25.0, poll_interval: float = 0.5) -> bool:
    """等待 CAD 主窗口出现，并缩放到次屏右上角 1/4 工作区。"""
    deadline = time.time() + max(timeout, 1.0)
    last_hwnd = 0
    while time.time() < deadline:
        hwnd = _find_main_window_by_pid(pid)
        if hwnd:
            last_hwnd = hwnd
            if _place_window_top_right_quarter(hwnd):
                return True
        time.sleep(max(poll_interval, 0.2))

    if last_hwnd:
        return _place_window_top_right_quarter(last_hwnd)
    return False


def _resize_windows_for_background_use(
    *,
    process_names: tuple[str, ...] | list[str] | None = None,
    title_keywords: tuple[str, ...] | list[str] | None = None,
    corner: str = "top-right",
) -> dict[str, int]:
    """将匹配到的窗口统一收拢到目标工作区的指定 1/4 区域。"""
    windows = _enumerate_visible_top_windows(process_names=process_names, title_keywords=title_keywords)
    moved = 0
    for window in windows:
        hwnd = int(window.get("hwnd") or 0)
        if hwnd and _place_window_quarter(hwnd, corner=corner):
            moved += 1
    return {"observed": len(windows), "moved": moved}


def start_applicationV9(
    PTH: str = r"C:\Tangent\TArchT20V9",
    max_retries: int = 3,
    retry_delay: float = 2.0,
) -> subprocess.Popen | None:
    """通过 TGStart.exe 启动天正，并挂载守护链。"""
    exe = Path(PTH) / "TGStart.exe"
    if not exe.exists():
        sys_logger.error(f"[start_applicationV9] 天正启动程序不存在: {exe}")
        return None

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            proc = subprocess.Popen([str(exe)], cwd=str(exe.parent))
            time.sleep(3.0)
            resized = _resize_cad_window_for_background_use(proc.pid)
            if resized:
                sys_logger.info(f"[start_applicationV9] 已将天正窗口缩放到次屏右上角 1/4 区域，PID={proc.pid}")
            else:
                sys_logger.warning(f"[start_applicationV9] 未能在启动阶段完成窗口缩放，PID={proc.pid}")
            try:
                launch_cad_guardians()
            except Exception as guard_exc:
                sys_logger.warning(f"[start_applicationV9] 挂载守护链失败: {guard_exc}")
            sys_logger.info(f"[start_applicationV9] 已启动天正，PID={proc.pid}")
            return proc
        except Exception as exc:
            last_error = exc
            sys_logger.warning(f"[start_applicationV9] 第 {attempt}/{max_retries} 次启动失败: {exc}")
            if attempt < max_retries:
                time.sleep(max(retry_delay, 0.5))

    sys_logger.error(f"[start_applicationV9] 启动天正失败: {last_error}")
    return None


class _LegacyCompat:
    """仅保留历史属性名，避免再直接依赖 scripts.CAD_basic。"""

    @staticmethod
    def li():
        return licad_module.li()

    @property
    def acad(self):
        try:
            return C.acad
        except Exception:
            return None

    @property
    def doc(self):
        try:
            return C.raw_doc
        except Exception:
            return None

    @property
    def mp(self):
        try:
            return C.mp
        except Exception:
            return None

    @property
    def sp(self):
        try:
            return C.sp
        except Exception:
            return None

    @staticmethod
    def st():
        return start_applicationV9()

    @staticmethod
    def close_all_cad_processes():
        return close_all_cad_processes()

    @staticmethod
    def safe_explode(block_ref):
        return safe_explode(block_ref)


cb = _LegacyCompat()

# 3.3 CAD 基础文档操作（内生化，替代 CAD_basic_operations 依赖）
def _core_get_short_path(path_str: str) -> str:
    try:
        return win32api.GetShortPathName(str(path_str))
    except Exception:
        return str(path_str)

def _core_get_acad():
    try:
        if 'C' in globals() and getattr(C, 'acad', None):
            return C.acad
    except Exception:
        pass
    try:
        return win32com.client.GetActiveObject("AutoCAD.Application")
    except Exception:
        return win32com.client.Dispatch("AutoCAD.Application")

def _core_get_active_doc():
    try:
        if 'C' in globals() and getattr(C, 'doc', None):
            return C.doc
    except Exception:
        pass
    acad = _core_get_acad()
    return acad.ActiveDocument

def _core_wait_document_opened(path: str, timeout: float = 120.0) -> bool:
    target_path = str(Path(path).resolve()).lower()
    target_name = Path(path).name.lower()
    name_only = Path(path).name.lower() == str(path).lower()
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            app = _core_get_acad()
            for i in range(app.Documents.Count):
                d = app.Documents.Item(i)
                try:
                    d_full = str(Path(d.FullName).resolve()).lower()
                except Exception:
                    d_full = ''
                if d_full == target_path or (name_only and (Path(d_full).name.lower() == target_name or d.Name.lower() == target_name)):
                    try:
                        d.Activate()
                    except Exception:
                        pass
                    return True
        except Exception:
            pass
        time.sleep(0.5)
    return False

def _core_is_file_opened(file_path: str) -> bool:
    target_path = str(Path(file_path).resolve()).lower()
    try:
        acad = _core_get_acad()
        for doc in acad.Documents:
            try:
                if str(Path(doc.FullName).resolve()).lower() == target_path:
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False

def _core_is_file_opened_by_name(name: str) -> bool:
    low = str(name).lower()
    try:
        acad = _core_get_acad()
        for doc in acad.Documents:
            try:
                if doc.Name.lower() == low:
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False

def _core_activate_document(file_path_or_name: str) -> bool:
    target = str(file_path_or_name)
    target_name = Path(target).name.lower()
    name_only = Path(target).name.lower() == target.lower()
    try:
        acad = _core_get_acad()
        for doc in acad.Documents:
            try:
                full_name = str(Path(doc.FullName).resolve()).lower()
            except Exception:
                full_name = ''
            try:
                if full_name == str(Path(target).resolve()).lower() or (name_only and doc.Name.lower() == target_name):
                    doc.Activate()
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False

def _core_get_open_file_count() -> int:
    try:
        return _core_get_acad().Documents.Count
    except Exception:
        return 0

def _core_ensure_single_process() -> bool:
    try:
        if jingchengshu_wenjian() > 1:
            sys_logger.warning('检测到多个 CAD 进程，执行清理后重连')
            close_all_cad_processes()
            time.sleep(1.0)
            return bool(litz())
        return True
    except Exception as e:
        sys_logger.warning(f'单进程检查失败: {e}')
        return False

def new_dwg_enhanced(output_path=None):
    """内生化新建 DWG：确保环境、创建文档、按需保存。"""
    try:
        _core_ensure_single_process()
        try:
            wait_quiescent(min_quiet=0.5, timeout=15.0)
        except Exception:
            pass

        if output_path and Path(output_path).exists():
            sys_logger.info(f'目标文件已存在，直接打开: {output_path}')
            return open_dwg_paradigm(output_path)

        acad = _core_get_acad()
        doc = acad.Documents.Add()
        time.sleep(1.0)

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            doc.SaveAs(str(out))
            try:
                wait_quiescent(min_quiet=0.8, timeout=15.0)
            except Exception:
                pass
            sys_logger.info(f'新建并保存成功: {out}')
        else:
            sys_logger.info('已创建未保存新图纸')
        return True
    except Exception as e:
        sys_logger.error(f'新建文件失败: {e}')
        return False

def open_dwg_paradigm(file_path):
    """内生化打开 DWG：路径幂等 + 单进程 + 等待文档加入集合。"""
    try:
        target = Path(file_path)
        if not target.exists():
            sys_logger.error(f'文件不存在: {file_path}')
            return False

        process_count = jingchengshu_wenjian()
        if process_count == 0:
            sys_logger.info('CAD 未运行，尝试启动')
            if not start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0):
                return False
        elif process_count > 1:
            _core_ensure_single_process()

        try:
            wait_quiescent(min_quiet=0.3, timeout=15.0)
        except Exception:
            pass

        if _core_is_file_opened(str(target)):
            _core_activate_document(str(target))
            sys_logger.info(f'文件已打开，直接激活: {target.name}')
            return True

        if _core_is_file_opened_by_name(target.name):
            sys_logger.warning(f'检测到同名文件已打开但路径不同，继续按目标路径打开: {target}')

        acad = _core_get_acad()
        short_path = _core_get_short_path(str(target))
        acad.Documents.Open(short_path)

        if _core_wait_document_opened(str(target), timeout=120.0):
            try:
                wait_quiescent(min_quiet=0.5, timeout=30.0)
            except Exception:
                pass
            sys_logger.info(f'文件打开成功: {target.name}')
            return True

        sys_logger.error(f'文件打开超时: {target.name}')
        return False
    except Exception as e:
        sys_logger.error(f'打开文件异常: {e}')
        return False

def save_as_dwg_paradigm(output_path):
    """内生化另存为：优先 SaveAs，失败时尝试短路径。"""
    try:
        doc = _core_get_active_doc()
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            doc.SaveAs(str(out))
        except Exception:
            doc.SaveAs(_core_get_short_path(str(out)))
        try:
            wait_quiescent(min_quiet=0.5, timeout=15.0)
        except Exception:
            pass
        sys_logger.info(f'另存为成功: {out}')
        return True
    except Exception as e:
        sys_logger.error(f'另存为失败: {e}')
        return False

def save_current_dwg_paradigm():
    """内生化保存：COM Save -> _qsave -> SaveAs Overwrite。"""
    try:
        doc = _core_get_active_doc()
        name = getattr(doc, 'Name', 'Unknown')
        full_name = getattr(doc, 'FullName', '')

        try:
            if getattr(doc, 'ReadOnly', False):
                sys_logger.warning(f'当前文件只读，无法保存: {name}')
                return False
        except Exception:
            pass

        if not full_name:
            sys_logger.warning(f'未命名文件无法直接保存: {name}')
            return False

        try:
            doc.Saved = False
        except Exception:
            pass

        try:
            doc.Save()
            if getattr(doc, 'Saved', False):
                sys_logger.info(f'COM Save 成功: {name}')
                return True
        except Exception as e:
            sys_logger.warning(f'COM Save 失败，准备降级: {e}')

        try:
            doc.SendCommand('_qsave\n')
            try:
                wait_quiescent(min_quiet=0.5, timeout=10.0)
            except Exception:
                time.sleep(2.0)
            if getattr(doc, 'Saved', False):
                sys_logger.info(f'_qsave 成功: {name}')
                return True
        except Exception as e:
            sys_logger.warning(f'_qsave 失败，继续降级: {e}')

        return save_as_dwg_paradigm(full_name)
    except Exception as e:
        sys_logger.error(f'保存当前文件失败: {e}')
        return False

def close_current_dwg_paradigm(save_option="prompt"):
    """内生化关闭当前文档。"""
    try:
        acad = _core_get_acad()
        if acad.Documents.Count == 0:
            return True
        doc = acad.ActiveDocument
        name = getattr(doc, 'Name', 'Unknown')

        if save_option == 'auto_save':
            doc.Close(True)
        elif save_option == 'no_save':
            doc.Close(False)
        else:
            try:
                need_save = not bool(doc.Saved)
            except Exception:
                need_save = False
            doc.Close(bool(need_save))
        sys_logger.info(f'关闭当前文件成功: {name}')
        return True
    except Exception as e:
        sys_logger.error(f'关闭当前文件失败: {e}')
        return False

def close_all_dwg_paradigm():
    """内生化关闭全部文档。"""
    try:
        total = _core_get_open_file_count()
        success = 0
        for _ in range(total):
            if close_current_dwg_paradigm(save_option='no_save'):
                success += 1
            time.sleep(0.3)
        sys_logger.info(f'关闭全部文档完成: {success}/{total}')
        return success == total
    except Exception as e:
        sys_logger.error(f'关闭全部文档失败: {e}')
        return False

# 3.4 导入 选择模块 (CAD_selection)
try:
    from system.CAD_selection import *


except ImportError as e:
    sys_logger.error(f"[警告] CAD_selection 导入失败: {e}")


# ==============================================================================
# 4. [核心增强] 智能连接与全局变量同步 (Licad / CAD_basic 双核)
# ==============================================================================

# 初始化模块级全局变量 (占位符)
acad = None
doc = None
mp = None
sp = None

sys_logger.info("[初始化] 成功加载 system.licad 核心模块")


def li():
    """
    调用 system.licad.li() 并同步模块级全局变量。
    """
    global acad, doc, mp, sp

    is_connected = licad_module.li()
    if is_connected:
        acad = C.acad
        doc = C.doc
        mp = C.mp
        sp = C.sp
        return True
    return False

# ================= 5. 初始化完成 =================

def launch_tarch_CAD_system():
    return start_applicationV9()


#&&% 关闭天正CAD系统

def close_tarch_CAD_system():
    return close_all_cad_processes()


#&&% 守护天正CAD系统
def launch_cad_guardians():
    """
    【功能】: 独立启动 CAD 的守护脚本（弹窗杀手 + 命令监控 + 运行监管）。
    【特性】: 支持系统任意移动，路径自动识别。
    """
    # ========================================================
    # 1. 动态获取路径 (核心修改)
    # ========================================================
    # 当前文件: .../cad/scripts/CAD_file_operations.py
    current_script = Path(__file__).resolve()
    
    # 项目根目录: .../cad
    project_root = current_script.parent.parent
    
    # 目标目录: .../cad/system
    system_dir = project_root / "system"
    # ========================================================

    scripts_to_launch = [
        "cad_dialog_killer.py",
        "cad_command_monitor.py",
        "cad_runtime_guard.py",
        "cad_window_keeper.py",
    ]

    sys_logger.info(f"🛡️ [守护] 正在从 [{system_dir.name}] 启动守护进程...")
    
    success_count = 0

    for script_name in scripts_to_launch:
        # 拼接完整路径
        script_path = system_dir / script_name
        
        if not script_path.exists():
            sys_logger.error(f"❌ [错误] 找不到脚本: {script_path}")
            continue

        try:
            creation_flags = subprocess.CREATE_NO_WINDOW
            
            # 启动进程 (注意：cwd 参数也使用动态路径)
            proc = subprocess.Popen(
                [sys.executable, str(script_path)], # 路径转为字符串
                creationflags=creation_flags,
                cwd=str(system_dir)                 # 工作目录设为 system
            )
            
            time.sleep(0.5)
            
            if proc.poll() is None:
                sys_logger.info(f"✅ [启动] {script_name} 成功 (PID: {proc.pid})")
                success_count += 1
            else:
                sys_logger.info(f"ℹ️ [跳过] {script_name} 已在运行中。")
                success_count += 1
                
        except Exception as e:
            sys_logger.error(f"❌ [异常] 无法启动 {script_name}: {e}")

    return success_count == len(scripts_to_launch)


def _join_process_cmdline(parts) -> str:
    if not parts:
        return ""
    if isinstance(parts, (list, tuple)):
        return " ".join(str(p) for p in parts)
    return str(parts)


def _has_tarch_markers(values: list[str]) -> bool:
    joined = " | ".join(str(v or "").lower() for v in values)
    return any(mark in joined for mark in ("tarch", "tangent", "tgstart"))


def collect_cad_process_inventory() -> list[dict]:
    """
    收集所有 acad.exe 进程的来源信息。

    说明：
    - 不依赖窗口标题。
    - 主要依据 exe/cmdline/父进程中的 TArch/Tangent/TGStart 线索。
    """
    rows = []
    for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
        try:
            name = str(proc.info.get("name") or "")
            if name.lower() != "acad.exe":
                continue

            exe = str(proc.info.get("exe") or "")
            cmdline = _join_process_cmdline(proc.info.get("cmdline"))
            parent_name = ""
            parent_exe = ""
            try:
                parent = proc.parent()
            except Exception:
                parent = None
            if parent is not None:
                try:
                    parent_name = str(parent.name() or "")
                except Exception:
                    parent_name = ""
                try:
                    parent_exe = str(parent.exe() or "")
                except Exception:
                    parent_exe = ""

            is_tarch = _has_tarch_markers([name, exe, cmdline, parent_name, parent_exe])
            rows.append(
                {
                    "pid": int(proc.info.get("pid") or 0),
                    "process_name": name,
                    "process_exe": exe,
                    "process_cmdline": cmdline,
                    "parent_name": parent_name,
                    "parent_exe": parent_exe,
                    "is_tarch_source": int(is_tarch),
                    "source_hint": "tarch_source" if is_tarch else "plain_acad_source",
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception as exc:
            sys_logger.warning(f"[collect_cad_process_inventory] 进程采集异常: {exc}")

    rows.sort(key=lambda row: (row.get("pid", 0), row.get("process_cmdline", "")))
    return rows


def _split_cad_process_inventory(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    tarch_rows = [row for row in rows if int(row.get("is_tarch_source", 0)) == 1]
    plain_rows = [row for row in rows if int(row.get("is_tarch_source", 0)) != 1]
    return tarch_rows, plain_rows


def _force_terminate_cad_processes(pids: list[int], *, timeout: float = 15.0) -> bool:
    target_pids = sorted({int(pid) for pid in pids if int(pid or 0) > 0})
    if not target_pids:
        return True

    processes: list[psutil.Process] = []
    for pid in target_pids:
        try:
            proc = psutil.Process(pid)
            child_list = []
            try:
                child_list = proc.children(recursive=True)
            except Exception:
                child_list = []
            processes.extend(child_list)
            processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    unique_processes = []
    seen = set()
    for proc in processes:
        try:
            pid = int(proc.pid)
        except Exception:
            continue
        if pid in seen:
            continue
        seen.add(pid)
        unique_processes.append(proc)

    for proc in unique_processes:
        try:
            proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception as exc:
            sys_logger.warning(f"[force_terminate_cad_processes] terminate 失败 PID={proc.pid}: {exc}")

    gone, alive = psutil.wait_procs(unique_processes, timeout=max(timeout / 2.0, 1.0))
    if alive:
        for proc in alive:
            try:
                proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            except Exception as exc:
                sys_logger.warning(f"[force_terminate_cad_processes] kill 失败 PID={proc.pid}: {exc}")
        psutil.wait_procs(alive, timeout=max(timeout / 2.0, 1.0))

    remaining = []
    for pid in target_pids:
        if psutil.pid_exists(pid):
            remaining.append(pid)
    return not remaining


def _wait_for_no_cad_processes(timeout: float = 15.0, poll_interval: float = 0.5) -> bool:
    deadline = time.time() + max(timeout, 1.0)
    while time.time() < deadline:
        if not collect_cad_process_inventory():
            return True
        time.sleep(max(poll_interval, 0.1))
    return not collect_cad_process_inventory()


def _wait_for_healthy_tarch_runtime(timeout: float = 45.0, poll_interval: float = 1.5) -> tuple[bool, dict]:
    deadline = time.time() + max(timeout, 1.0)
    snapshot = {}
    while time.time() < deadline:
        snapshot = inspect_cad_runtime()
        if (
            snapshot.get("status") == "healthy_tarch"
            and not snapshot.get("plain_process_pids", [])
        ):
            return True, snapshot
        time.sleep(max(poll_interval, 0.3))
    snapshot = inspect_cad_runtime()
    return (
        snapshot.get("status") == "healthy_tarch"
        and not snapshot.get("plain_process_pids", []),
        snapshot,
    )


def _reset_cad_proxy_cache() -> None:
    try:
        if 'C' in globals() and C is not None:
            for attr in ("_acad", "_doc", "_mp", "_sp"):
                try:
                    setattr(C, attr, None)
                except Exception:
                    pass
    except Exception:
        pass


def inspect_cad_runtime(*, allow_process_probe: bool = True) -> dict:
    """
    被动检查当前 CAD 运行态，不主动启动新 CAD。

    说明：
    - 不调用 C.li()，避免把观察者变成干预者。
    - 不依赖窗口标题。
    - 主要依据 COM 可达性 + 当前活动进程来源元数据判断：
      是否带有 TArch/Tangent/TGStart 等天正来源线索。
    """

    payload = {
        "status": "unknown",
        "severity": "info",
        "reason": "",
        "process_hint": "unknown",
        "process_name": "",
        "process_exe": "",
        "process_cmdline": "",
        "parent_name": "",
        "parent_exe": "",
        "pid": 0,
        "hwnd": 0,
        "doc_name": "",
        "doc_full_name": "",
        "modelspace_ready": 0,
        "paperspace_ready": 0,
        "com_ready": 0,
        "acad_process_count": 0,
        "tarch_process_count": 0,
        "plain_process_count": 0,
        "tarch_process_pids": [],
        "plain_process_pids": [],
        "acad_processes": [],
    }

    inventory = collect_cad_process_inventory() if allow_process_probe else []
    tarch_rows, plain_rows = _split_cad_process_inventory(inventory)
    payload["acad_process_count"] = len(inventory)
    payload["tarch_process_count"] = len(tarch_rows)
    payload["plain_process_count"] = len(plain_rows)
    payload["tarch_process_pids"] = [int(row.get("pid", 0) or 0) for row in tarch_rows if int(row.get("pid", 0) or 0) > 0]
    payload["plain_process_pids"] = [int(row.get("pid", 0) or 0) for row in plain_rows if int(row.get("pid", 0) or 0) > 0]
    payload["acad_processes"] = inventory

    try:
        pythoncom.CoInitialize()
    except Exception:
        pass

    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
    except Exception as exc:
        payload["status"] = "no_active_cad"
        payload["severity"] = "info"
        payload["reason"] = f"GetActiveObject 未取得活动 CAD: {exc}"
        return payload

    try:
        hwnd = int(getattr(acad, "HWND", 0) or 0)
    except Exception:
        hwnd = 0
    payload["hwnd"] = hwnd

    pid = 0
    proc_name = ""
    proc_exe = ""
    proc_cmdline = ""
    parent_name = ""
    parent_exe = ""
    if allow_process_probe and hwnd:
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid:
                proc = psutil.Process(pid)
                proc_name = str(proc.name() or "")
                proc_exe = str(proc.exe() or "")
                proc_cmdline = _join_process_cmdline(proc.cmdline())
                try:
                    parent = proc.parent()
                except Exception:
                    parent = None
                if parent is not None:
                    parent_name = str(parent.name() or "")
                    try:
                        parent_exe = str(parent.exe() or "")
                    except Exception:
                        parent_exe = ""
        except Exception as exc:
            payload["reason"] = f"进程探测失败: {exc}"

    payload["pid"] = pid
    payload["process_name"] = proc_name
    payload["process_exe"] = proc_exe
    payload["process_cmdline"] = proc_cmdline
    payload["parent_name"] = parent_name
    payload["parent_exe"] = parent_exe

    try:
        doc = acad.ActiveDocument
        payload["doc_name"] = str(getattr(doc, "Name", "") or "")
        payload["doc_full_name"] = str(getattr(doc, "FullName", "") or "")
        _ = doc.ModelSpace
        payload["modelspace_ready"] = 1
        _ = doc.PaperSpace
        payload["paperspace_ready"] = 1
        payload["com_ready"] = 1
    except pythoncom.com_error as exc:
        payload["status"] = "cad_busy"
        payload["severity"] = "warning"
        payload["reason"] = f"COM busy/rejected: {exc}"
        return payload
    except Exception as exc:
        payload["status"] = "cad_doc_unavailable"
        payload["severity"] = "warning"
        payload["reason"] = f"活动文档不可用: {exc}"
        return payload

    values = [proc_name, proc_exe, proc_cmdline, parent_name, parent_exe]
    has_tarch = _has_tarch_markers(values)
    proc_name_low = proc_name.lower()
    active_row = next((row for row in inventory if int(row.get("pid", 0) or 0) == pid), None)

    if plain_rows:
        if active_row and int(active_row.get("is_tarch_source", 0)) == 1:
            payload["process_hint"] = "mixed_sources"
            payload["status"] = "suspected_plain_cad"
            payload["severity"] = "warning"
            payload["reason"] = (
                "当前活动 CAD 为天正来源，但系统仍残留纯 CAD 进程，"
                f"plain_pids={payload['plain_process_pids']}。"
            )
        else:
            payload["process_hint"] = "plain_acad_source"
            payload["status"] = "suspected_plain_cad"
            payload["severity"] = "warning"
            payload["reason"] = (
                "系统里存在未带天正线索的 acad.exe 进程，"
                f"plain_pids={payload['plain_process_pids']}。"
            )
    elif active_row and int(active_row.get("is_tarch_source", 0)) == 1:
        payload["process_hint"] = "tarch_source"
        payload["status"] = "healthy_tarch"
        payload["severity"] = "info"
        payload["reason"] = "活动 CAD 进程来源包含 TArch/Tangent/TGStart 线索，且 COM/文档可用。"
    elif has_tarch or tarch_rows:
        payload["process_hint"] = "tarch_source"
        payload["status"] = "healthy_tarch"
        payload["severity"] = "info"
        payload["reason"] = "活动 CAD 进程来源包含 TArch/Tangent/TGStart 线索，且 COM/文档可用。"
    elif proc_name_low == "acad.exe":
        payload["process_hint"] = "plain_acad_source"
        payload["status"] = "suspected_plain_cad"
        payload["severity"] = "warning"
        payload["reason"] = "活动 CAD 进程仅表现为 acad.exe，未发现天正来源线索。"
    else:
        payload["process_hint"] = "unknown_source"
        payload["status"] = "runtime_uncertain"
        payload["severity"] = "info"
        payload["reason"] = "活动 CAD 可访问，文档上下文正常，但进程来源暂时无法确认。"

    return payload


#&&% 连接天正CAD系统
def litz(max_connect_rounds: int = 3, wait_between_rounds: float = 2.0):
    """
    
    
    【功能】: 
        天正环境灾难恢复与智能重连 (C类单例版)。
    
    【逻辑闭环】:
        1. 尝试连接: 调用 C.li() 尝试获取现有连接。
        2. 探针验证: 如果连接成功，画墙测试是否为有效天正环境。
        3. 灾难重建: 如果验证失败，杀进程 -> 启动天正 -> 等待。
        4. 状态刷新: 再次调用 C.li()，由 C 类统一接管新实例。
        5. 无需反向注入: 所有模块通过访问 C.doc, C.acad 自动获取最新状态。
    """
    import time
    
    # 引用全局单例 (假设文件头部已 import licad.C as C 或类似)
    # from system.licad import C 
    
    # ========= 第一阶段：常规检查 (利用 C.li) =========
    sys_logger.info("[litz] 开始环境健康检查...")
    is_connected = False
    try:
        if C.li():
            is_connected = True
    except:
        pass

    current_snapshot = inspect_cad_runtime()

    if is_connected:
        # 【探针】画天正墙检测
        try:
            # draw_tarch_wall 需确保已导入
            test_res = draw_tarch_wall((0, 0, 0), (1000, 0, 0))
        except Exception:
            test_res = False

        if test_res:
            # 验证通过，清理垃圾
            try:
                obj = last_obj()
                if obj: safe_delete(obj)
            except: pass

            if not current_snapshot.get("plain_process_pids", []):
                sys_logger.info(f"[litz] 环境检测正常，复用现有进程: {C.doc.Name}")
                return True

            sys_logger.warning(
                "[litz] 天正探针通过，但检测到纯 CAD 残留，"
                f"准备定点清理: {current_snapshot.get('plain_process_pids', [])}"
            )
        else:
            sys_logger.error("[litz] 连接正常但探针检测失败（疑似非天正环境），准备重建...")
    else:
        sys_logger.error("[litz] 基础连接 C.li() 失败，准备重建...")

    plain_pids = list(current_snapshot.get("plain_process_pids", []) or [])
    if plain_pids:
        if _force_terminate_cad_processes(plain_pids, timeout=15.0):
            time.sleep(2.0)
            ok_after_kill, snapshot_after_kill = _wait_for_healthy_tarch_runtime(timeout=20.0, poll_interval=1.0)
            if ok_after_kill:
                try:
                    _reset_cad_proxy_cache()
                    C.li()
                except Exception:
                    pass
                sys_logger.info(
                    "[litz] 纯 CAD 残留已定点清理，当前环境恢复为 healthy_tarch: "
                    f"pid={snapshot_after_kill.get('pid', 0)}"
                )
                return True
            current_snapshot = snapshot_after_kill
        else:
            sys_logger.warning(f"[litz] 纯 CAD 定点清理后仍有残留: {plain_pids}")

    # ========= 第二阶段：环境重置 (Kill & Restart) =========
    sys_logger.info("[litz] 执行环境重置...")
    try:
        # 调用 CAD_basic 中的关闭进程函数
        close_all_cad_processes()
    except Exception as e:
        sys_logger.warning(f"[litz] 关闭进程警告: {e}")

    remaining_rows = collect_cad_process_inventory()
    if remaining_rows:
        remaining_pids = [int(row.get("pid", 0) or 0) for row in remaining_rows if int(row.get("pid", 0) or 0) > 0]
        sys_logger.warning(f"[litz] taskkill 后仍有 CAD 残留，执行二次强杀: {remaining_pids}")
        _force_terminate_cad_processes(remaining_pids, timeout=15.0)

    if not _wait_for_no_cad_processes(timeout=20.0, poll_interval=0.5):
        leftovers = collect_cad_process_inventory()
        sys_logger.error(f"[litz] 环境重置失败，仍检测到 CAD 残留: {leftovers}")
        return False

    _reset_cad_proxy_cache()

    try:
        # 启动天正 (调用本模块或 CAD_basic 的启动函数)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
    except Exception as e:
        sys_logger.error(f"[litz] 启动天正失败: {e}")
        return False

    # ========= 第三阶段：等待并刷新 C 类 =========
    sys_logger.info("[litz] 正在等待 CAD 初始化并刷新 C 类连接...")
    
    success = False
    
    # 循环尝试连接，给 CAD 启动留出时间
    # 这里的关键是：我们不再自己去 GetActiveObject，而是不断呼叫 C.li()
    # C.li() 内部封装了 GetActiveObject 和异常处理
    
    for round_idx in range(1, max_connect_rounds + 1):
        if round_idx > 1:
            sys_logger.info(f"[litz] 第 {round_idx} 轮重试...")
            time.sleep(wait_between_rounds)

        snapshot = inspect_cad_runtime()
        if (
            snapshot.get("status") == "healthy_tarch"
            and not snapshot.get("plain_process_pids", [])
        ):
            try:
                _reset_cad_proxy_cache()
                if C.li() and C.doc and C.mp:
                    success = True
                    current_snapshot = snapshot
                    break
            except Exception:
                pass

        # 尝试刷新连接
        if C.li():
            # 再次用探针确认（防止连接到了一个还没加载完插件的空壳 CAD）
            try:
                # 稍微等一下 ModelSpace
                if C.mp is None:
                    time.sleep(1.0)
                    C.li() # 再刷一次
                
                # 只有 C.doc 和 C.mp 都就绪才算成功
                if C.doc and C.mp:
                    snapshot = inspect_cad_runtime()
                    if (
                        snapshot.get("status") == "healthy_tarch"
                        and not snapshot.get("plain_process_pids", [])
                    ):
                        success = True
                        current_snapshot = snapshot
                        break
            except:
                pass
                
        time.sleep(1.0) # 短暂冷却

    if success:
        sys_logger.info(
            "[litz] 连接重建完成，C 类已同步。"
            f" 当前激活文档: {C.doc.Name}; pid={current_snapshot.get('pid', 0)}"
        )
        return True
    else:
        stable_ok, stable_snapshot = _wait_for_healthy_tarch_runtime(timeout=20.0, poll_interval=1.0)
        if stable_ok:
            try:
                _reset_cad_proxy_cache()
                C.li()
            except Exception:
                pass
            sys_logger.info(
                "[litz] 延迟校验通过，环境已恢复到 healthy_tarch。"
                f" pid={stable_snapshot.get('pid', 0)}"
            )
            return True
        sys_logger.error(f"[litz] 严重错误：重启后未建立有效天正环境。snapshot={stable_snapshot}")
        return False


#&&&% CAD状态控制


#&&% 激活桌面指定文件
@retry_if_busy(max_retries=5, delay=1.0)
def activate_document_by_name(filename):
    """
    激活指定文件名的文档为当前操作对象

    Args:
        filename: 支持绝对/相对路径或单纯文件名

    Returns:
        bool: 成功返回True，失败返回False
    """

    target = Path(filename).name.lower()
    open_docs = get_open_document_names()
    normalized = {Path(name).name.lower(): name for name in open_docs}

    if target not in normalized:
        sys_logger.error(f"[错误] 文件 {filename} 未在当前 CAD 会话中打开")
        return False

    actual_name = normalized[target]
    doc = get_doc_by_name(actual_name)
    if doc is None:
        sys_logger.error(f"[错误] 无法获取文件 {actual_name} 的文档对象")
        return False

    try:
        set_active_doc(doc)
    except Exception as exc:
        sys_logger.error(f"[错误] 激活文件 {actual_name} 失败: {exc}")
        return False

    if not C.li():
        sys_logger.error("[警告] li() 连接失败，当前控制对象未确定")
        return False

    sys_logger.info(f"[成功] 已激活文件: {actual_name}")
    return True

#&&% 状态归零

def cad_zt_zero():
    """
    确保CAD进程数为0（关闭所有CAD）
    """
    shu = jingchengshu_wenjian()
    if shu > 0:
        close_all_cad_processes()
    return True

#&&% 标准归一状态

def cad_zt_oneb():
    """
    确保CAD状态为：1个进程+1个空白文件（单文件不确定状态）
    """
    import time
    from system.CAD_coordination import wait_quiescent

    shu = jingchengshu_wenjian()
    if shu == 0:
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
    elif shu == 1:
        def _is_default_session(paths):
            if not paths:
                return True
            if len(paths) != 1:
                return False
            entry = str(paths[0]).strip()
            entry_lower = entry.lower()
            if not entry or ":" in entry or "\\" in entry or "/" in entry:
                return False
            return entry_lower.startswith("drawing") and entry_lower.endswith(".dwg")

        try:
            C.li()
        except Exception:
            pass

        try:
            open_paths = get_all_open_dwg_paths()
        except Exception as exc:
            sys_logger.error(f"[cad_zt_oneb] 获取打开文件失败：{exc}")
            open_paths = []

        sys_logger.info(f"[cad_zt_oneb] 当前打开文件列表: {open_paths}")

        if _is_default_session(open_paths):
            sys_logger.info("[cad_zt_oneb] 检测到天正默认空白 DWG，保持现状。")
            return True

        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
    elif shu > 1:
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
    return True


#&&% 归一状态
def cad_zt_oned(file_path=str(XITONG_DIR / "0.dwg")):
    """
    确保CAD状态为：1个进程+1个指定文件（单文件确定状态）

    Args:
        file_path: 要打开的文件路径，默认为 cad/xitongwenjian/0.dwg
    """
    import time
    from system.CAD_coordination import wait_quiescent

    shu = jingchengshu_wenjian()
    if shu == 0:
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file_path)
    elif shu > 1:
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file_path)
    elif shu == 1:
        
        C.li()
        close_all_except_active_safe()
    return True

#&&% 归二状态

def cad_zt_two(file1=str(XITONG_DIR / "0.dwg"), file2=str(XITONG_DIR / "1.dwg")):
    """
    确保CAD状态为：1个进程+2个文件（双文件确定状态）

    Args:
        file1: 第一个文件路径
        file2: 第二个文件路径
    """
    import time
    from system.CAD_coordination import wait_quiescent

    shu = jingchengshu_wenjian()
    if shu == 0:
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
    elif shu > 1:
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
    elif shu == 1:
        
        C.li()
        open_docs = get_open_document_names()
        # 如果文件数多于2，关闭多余的
        while len(open_docs) > 2:
            close_dwg_by_name(open_docs[0])
            open_docs = get_open_document_names()
        # 如果文件数少于2，打开文件凑到2个
        files_to_open = [file1, file2]
        idx = 0
        while len(open_docs) < 2 and idx < len(files_to_open):
            open_file(files_to_open[idx])
            idx += 1
            open_docs = get_open_document_names()
    return True

#&&% 归三状态

def cad_zt_much(
    file1=str(XITONG_DIR / "0.dwg"),
    file2=str(XITONG_DIR / "1.dwg"),
    file3=str(XITONG_DIR / "2.dwg")
):
    """
    确保CAD状态为：1个进程+多个文件（>2个文件）

    Args:
        file1: 第一个文件路径
        file2: 第二个文件路径
        file3: 第三个文件路径
    """
    shu = jingchengshu_wenjian()
    if shu == 0:
        import time
        from system.CAD_coordination import wait_quiescent
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
        open_file(file3)
    elif shu > 1:
        import time
        from system.CAD_coordination import wait_quiescent
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
        open_file(file3)
    elif shu == 1:
        
        C.li()
        open_docs = get_open_document_names()
        files_to_open = [file1, file2, file3]
        for f in files_to_open:
            if len(open_docs) >= 3:
                break
            open_file(f)
            open_docs = get_open_document_names()
    return True

#&&% 记录当前状态
@retry_if_busy(max_retries=3, delay=1.0)
def cad_zt_xin_1(status_file=None):
    """
    【V2.1 修复版】记录当前 CAD 桌面信息，写入 JSON 状态文件。
    1. 修复 datetime 未定义错误
    2. 修复 NoneType 属性访问错误
    3. 增加文件夹路径反向推导功能
    """
    # ================= 1. 必要的局部导入 =================
    import json
    import os
    import sys
    from datetime import datetime
    from pathlib import Path
    
    # 导入系统配置
    try:
        from system.project_setup import PathConfig
        from system.licad import C
    except ImportError as e:
        sys_logger.error(f"[错误] 模块导入失败: {e}")
        return None

    # ================= 2. 路径处理 =================
    # 如果未指定文件，使用默认日志路径
    if status_file is None:
        status_file = PathConfig.LOGS / "cad_status.json"
    
    status_path = Path(status_file)
    try:
        status_path.parent.mkdir(parents=True, exist_ok=True)
    except: pass

    # ================= 3. 尝试连接 =================
    try:
        # 刷新连接，如果彻底连不上则放弃
        if not C.li():
            sys_logger.error("[cad_zt_xin_1] li() 连接失败，无法记录当前会话。")
            return None
    except Exception:
        return None

    # ================= 4. 安全获取数据 =================
    
    # A. 获取打开的文件列表
    open_paths = []
    try:
        open_paths = get_all_open_dwg_paths() or []
    except Exception:
        pass

    # B. 获取当前文件夹 (允许失败，下面有补救措施)
    active_folder = None
    try:
        active_folder = current_dwg_folder()
    except Exception:
        # 这里不要打印错误，以免刷屏， silently fail
        active_folder = None

    # C. 获取当前文档属性
    active_name = None
    active_full = None
    
    try:
        # 使用 getattr 防止 C.doc 不存在
        active_doc = getattr(C, "doc", None)
        
        if active_doc is not None:
            # 尝试获取 Name 和 FullName
            # 注意：新建未保存的文件 FullName 可能为空字符串
            active_name = getattr(active_doc, "Name", None)
            active_full = getattr(active_doc, "FullName", None)
    except Exception:
        # 如果 COM 忙碌或出错，保持为 None
        pass

    # ================= 5. 逻辑补救 (关键修复) =================
    
    # 情况1: 有全路径，但没获取到文件夹 -> 从全路径推导文件夹
    if active_full and (not active_folder):
        try:
            active_folder = str(Path(active_full).parent)
        except: pass

    # 情况2: 有文件夹和文件名，但没全路径 -> 拼接全路径
    if (not active_full) and active_folder and active_name:
        try:
            active_full = str(Path(active_folder) / active_name)
        except: pass

    # ================= 6. 构造并写入 =================
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "open_files": open_paths,
        "active_folder": active_folder,
        "active_file": active_full,
        "active_name": active_name,
        "pid": os.getpid()
    }

    try:
        status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        sys_logger.info(f"[cad_zt_xin_1] 已写入 CAD 状态信息到 {status_path}")
        return payload
    except Exception as e:
        sys_logger.error(f"[错误] 写入状态文件失败: {e}")
        return None


#&&% 恢复记录状态

def cad_zt_xin_2(status_file=None):
    """
    【V2.1 恢复版】根据 cad_zt_xin_1 记录的状态恢复 CAD 环境。
    逻辑：重启 -> 打开背景文件 -> 打开目标文件(自动激活) -> 强制确认激活
    """
    import json
    import time
    import os
    from pathlib import Path

    # 1. 导入架构组件
    from system.project_setup import PathConfig
    from system.licad import C
    from system.CAD_coordination import wait_quiescent

    # 2. 处理默认路径
    if status_file is None:
        status_file = PathConfig.LOGS / "cad_status.json"
    
    status_path = Path(status_file)
    if not status_path.exists():
        sys_logger.error(f"[cad_zt_xin_2] ❌ 状态文件不存在: {status_path}")
        return False

    # 3. 读取并解析配置
    try:
        payload = json.loads(status_path.read_text(encoding="utf-8"))
        sys_logger.info(f"[cad_zt_xin_2] 成功读取状态记录 (时间: {payload.get('timestamp')})")
    except Exception as e:
        sys_logger.error(f"[cad_zt_xin_2] ❌ 解析 JSON 失败: {e}")
        return False

    raw_open_files = payload.get("open_files") or []
    target_active_file = payload.get("active_file") # 全路径

    # 4. 路径清洗与分类 (关键步骤)
    # 我们需要把“目标激活文件”从列表里剔除，留到最后单独打开
    background_files = []
    target_active_norm = None

    if target_active_file:
        try:
            target_active_norm = str(Path(target_active_file).resolve()).lower()
        except: pass

    seen = set()
    
    for f in raw_open_files:
        if not f: continue
        try:
            p_obj = Path(f)
            if not p_obj.exists():
                sys_logger.info(f"[跳过] 文件不存在: {f}")
                continue
            
            # 归一化：转为绝对路径字符串并小写，用于去重和比对
            norm_str = str(p_obj.resolve()).lower()
            
            # 如果是目标激活文件，先跳过，不放入背景列表
            if target_active_norm and norm_str == target_active_norm:
                continue
                
            if norm_str not in seen:
                seen.add(norm_str)
                # 存储原始路径或解析后的路径均可，这里存解析后的
                background_files.append(str(p_obj.resolve()))
                
        except Exception:
            continue

    # 5. 重置环境 (Kill & Start)
    sys_logger.info("[cad_zt_xin_2] 正在重置 CAD 环境...")
    close_all_cad_processes() # 使用标准清理函数
    
    # 双重保险清理
    time.sleep(1)
    
    start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
    
    # 等待启动稳定 (这里可以复用 cad_zt_oneb 的检测逻辑，或者简单等待)
    sys_logger.info("[cad_zt_xin_2] 等待 CAD 启动就绪...")
    wait_quiescent(min_quiet=2.0, timeout=30.0)
    
    # 6. 执行打开 (The Rhythm Strategy)
    reopened_count = 0
    
    # 6.1 先打开所有背景文件
    for f_path in background_files:
        try:
            sys_logger.info(f"[恢复] 打开背景文件: {Path(f_path).name}")
            open_file(f_path)
            reopened_count += 1
            # 💤 节奏控制：防止 COM 忙碌
            time.sleep(1.5) 
        except Exception as e:
            sys_logger.error(f"[警告] 打开失败 {f_path}: {e}")

    # 6.2 最后打开目标激活文件 (这样它自然就是激活状态)
    if target_active_file and Path(target_active_file).exists():
        try:
            sys_logger.info(f"[恢复] 打开并激活目标文件: {Path(target_active_file).name}")
            open_file(target_active_file)
            reopened_count += 1
            time.sleep(1.5)
        except Exception as e:
            sys_logger.info(f"[严重] 无法打开目标文件: {e}")
    
    # 7. 最终状态确认
    # 虽然最后打开的通常是激活的，但为了稳健，我们再次检查
    if target_active_file:
        target_name = Path(target_active_file).name
        try:
            # 刷新连接
            C.li()
            current_doc = getattr(C.doc, "Name", "")
            
            if current_doc.lower() != target_name.lower():
                sys_logger.info(f"[校准] 当前激活的是 {current_doc}，正在强制切换回 {target_name}...")
                doc_obj = get_doc_by_name(target_name)
                if doc_obj:
                    set_active_doc(doc_obj)
            else:
                sys_logger.info(f"[确认] 当前已正确激活: {target_name}")
                
        except Exception as e:
            sys_logger.error(f"[警告] 激活状态校验失败: {e}")

    sys_logger.info(f"[cad_zt_xin_2] 恢复完成。共打开 {reopened_count} 个文件。")
    return True


#&&&% 单文档操作

@retry_if_busy(max_retries=5, delay=1.0)
#&&% 新建dwg文件

def new_file(output_path=None, close_after=False):
    """Create a DWG file after verifying the current CAD/TArch context.

    Args:
        output_path (str | None): Target path; None keeps an unsaved blank file.
        close_after (bool): Close the newly created/opened file automatically when True.

    Returns:
        bool: True if the DWG was created or opened successfully.

    新建同名文件将会覆盖之前的文件
    output_path=None，则没有创建文件
    新建文件不关闭的话，最多同时打开的文件不会超过4个，最后一个是激活文件

    """

    C.li()

    def _close_new_file(result: bool) -> bool:
        """Close the active file when requested and ignore close errors."""
        if result and close_after:
            try:
                sys_logger.info("[信息] close_after=True，正在关闭新建的文件...")
                # 调用只关闭当前文档的函数，而不是重启整个CAD
                close_current_dwg_paradigm("no_save")
                sys_logger.info("[成功] 新建的文件已关闭。")
            except Exception as exc:
                sys_logger.error(f"[警告] 关闭新建文件失败: {exc}")
        return result

    if output_path:
        target = Path(output_path)
        
        # --- 新增逻辑：检查文件是否已在CAD中打开 ---
        try:
            open_paths = get_all_open_dwg_paths()
            normalized_open_paths = {str(Path(p).resolve()).lower() for p in open_paths}
            target_path_str = str(target.resolve()).lower()

            if target_path_str in normalized_open_paths:
                sys_logger.info(f"[信息] 目标文件 '{target.name}' 已在CAD中打开，将直接激活它。")
                activate_document_by_name(target.name)
                # 因为文件已存在并激活，所以不执行关闭逻辑，直接返回成功
                return True
        except Exception as e:
            sys_logger.warning(f"[警告] 检查已打开文件时出错: {e}")
        # --- 新增逻辑结束 ---

        if target.exists():
            try:
                target.unlink()
                sys_logger.info(f"[信息] 已删除同名文件: {target}")
            except Exception as exc:
                sys_logger.error(f"[错误] 无法删除已存在文件 {target}: {exc}")
                return False

    def _limit_open_documents():
        """When open DWG count > 2, close extras leaving one."""
        try:
            names = get_open_document_names()
        except Exception as exc:
            sys_logger.error(f"[警告] 获取已打开文件失败: {exc}")
            return False, None

        if len(names) <= 3:
            return True, len(names)

        try:
            _, active_doc = get_acad_doc()
            active_name = active_doc.Name if active_doc else None
        except Exception:
            active_name = None

        keep = active_name if active_name in names else names[-1]
        remaining = names.copy()
        sys_logger.info(f"[信息] 当前打开 {len(names)} 个文件，保留 {keep}，关闭部分文件以压缩到 3 个以内")
        ok = True
        for name in names:
            if len(remaining) <= 3:
                break
            if name == keep:
                continue
            try:
                close_dwg_by_name(name)
                remaining.remove(name)
            except Exception as exc:
                ok = False
                sys_logger.error(f"[警告] 关闭文件 {name} 失败: {exc}")

        time.sleep(0.5)
        try:
            remaining = get_open_document_names()
        except Exception:
            remaining = []

        if len(remaining) <= 3:
            sys_logger.info(f"[信息] 已将打开文件数压缩到 {len(remaining)} 个")
            return ok, len(remaining)

        sys_logger.warning(f"[警告] 仍有 {len(remaining)} 个文件未关闭")
        return False, len(remaining)

    shu_1 = jingchengshu_wenjian()
    tarch_ready = False

    if shu_1 == 1:
        sys_logger.info("[信息] 检测到 1 个 CAD 进程，进行天正墙自检...")
        wall_obj = None
        try:
            connected = C.li()
            if connected:
                try:
                    prev_obj = last_obj()
                    prev_handle = getattr(prev_obj, "Handle", None)
                except Exception:
                    prev_obj = None
                    prev_handle = None

                wall_created = draw_tarch_wall((0, 0, 0), (100, 0, 0), thickness=240)
                if wall_created:
                    try:
                        wall_obj = last_obj()
                        handle = getattr(wall_obj, "Handle", None)
                    except Exception:
                        wall_obj = None
                        handle = None

                    if handle and handle != prev_handle:
                        sys_logger.info(f"[成功] 天正墙自检通过 (Handle={handle})")
                        tarch_ready = True
                    elif handle == prev_handle and handle is not None:
                        sys_logger.warning("[警告] last_obj 结果与自检前一致，可能未生成天正墙")
                    else:
                        sys_logger.warning("[警告] 天正墙未返回 Handle，准备重新初始化 CAD")
                else:
                    sys_logger.error("[警告] 绘制天正墙失败，准备重新初始化 CAD")
            else:
                sys_logger.error("[警告] li() 连接失败，准备重新初始化 CAD")
        except Exception as exc:
            sys_logger.error(f"[警告] 天正墙自检异常: {exc}")
        finally:
            if wall_obj is not None:
                try:
                    safe_delete(wall_obj)
                except Exception:
                    try:
                        wall_obj.Delete()
                    except Exception:
                        pass

    if not tarch_ready:
        sys_logger.info("[信息] 执行 cad_zt_zero() + cad_zt_oneb() 重新准备天正环境...")
        cad_zt_zero()
        cad_zt_oneb()

    doc_ok, doc_count = _limit_open_documents()
    if doc_count and doc_count > 2 and not doc_ok:
        sys_logger.error("[信息] 关闭多余文件失败，重启 CAD 环境...")
        cad_zt_zero()
        cad_zt_oneb()

    result = new_dwg_enhanced(output_path)
    return _close_new_file(result)


#&&% 打开dwg文件

@retry_if_busy(max_retries=5, delay=1.0)
def open_file(file_path):
    """
    【函数编号】: SYS-IO-001
    【所属模块】: 系统与文件控制 (System & File Control)
    【功能描述】:
        建立 CAD 运行环境并安全打开指定的 DWG 文件。
        采用“单例进程+负载控制”策略：
        1. 进程守护：确保 Windows 环境中仅存在一个 CAD 进程，防止多开冲突。
        2. 环境自启：若未检测到 CAD/天正进程，自动调用 TArch 启动接口。
        3. 负载均衡：智能监控当前打开的文档数量。若超过安全阈值（通常为 3 个），
           会自动识别并关闭非活跃文档（保留当前活动文档），防止内存溢出。
        4. 幂等打开：若目标文件已处于打开状态，直接激活窗口而不重复加载。

    【参数详解】:
        - file_path (str):
            目标 DWG 文件的路径。
            支持绝对路径或相对路径，函数内部会基于 pathlib 进行标准化解析。

    【返回值】:
        - bool:
            - True: 操作成功（文件被成功打开，或已存在并被激活）。
            - False: 操作失败（环境重置失败、文件无法读取或进程异常）。

    【前置依赖】:
        - 依赖全局变量 global acad 进行 COM 对象传递。
        - 依赖全局工具函数: li(), litz(), start_applicationV9() 等。

    【示例】:
        >>> status = open_file(r"D:\Project\FloorPlan_V1.dwg")
        >>> print(status)
        True
    """


    # --------------------------------------------------------
    # 2. 初始连接检查
    # --------------------------------------------------------
    li_ok = False
    try:
        li_ok = C.li()
    except Exception:
        li_ok = False

    if not li_ok:
        litz()
    else:
        sys_logger.info("[open_file] 复用现有 CAD 连接。")

    # --------------------------------------------------------
    # 3. 定义内部辅助函数 (使用全局导入的工具函数)
    # --------------------------------------------------------
    def _get_acad():
        return win32com.client.GetActiveObject("AutoCAD.Application")

    def _ensure_single_process():
        # 使用全局导入的 jingchengshu_wenjian
        if jingchengshu_wenjian() > 1:
            sys_logger.warning("[警告] 检测到多个 CAD 进程，执行重置...")
            # 替换原有的 cad_zt_zero/oneb 为标准函数，防止报错
            close_all_cad_processes() 
            litz()

    def _ensure_active_only():
        try:
            # 使用全局导入的 get_open_document_names
            names = get_open_document_names()
        except Exception as exc:
            sys_logger.error(f"[警告] 获取已打开文件失败: {exc}")
            return True

        if len(names) <= 3:
            return True

        try:
            # 使用全局导入的 get_acad_doc
            _, active_doc = get_acad_doc()
            active_name = active_doc.Name if active_doc else None
        except Exception:
            active_name = None

        keep = active_name if active_name in names else names[-1]
        remaining = names.copy()
        sys_logger.info(f"[信息] 当前打开 {len(names)} 个文件，保留 {keep}，关闭部分文件以压缩到 3 个以内")
        
        for name in names:
            if len(remaining) <= 3:
                break
            if name == keep:
                continue
            # 使用全局导入的 close_dwg_by_name
            close_dwg_by_name(name)
            remaining.remove(name)

        time.sleep(0.5)
        try:
            remaining = get_open_document_names()
        except Exception:
            remaining = []
            
        if len(remaining) > 3:
            sys_logger.warning("[警告] 仍有多余文件未关闭，重置 CAD 环境")
            return False

        return True

    # --------------------------------------------------------
    # 4. 执行逻辑
    # --------------------------------------------------------
    _ensure_single_process()

    # 确保CAD已启动
    try:
        acad = _get_acad()
    except:
        sys_logger.info("[信息] CAD未启动，正在启动天正...")
        # 使用全局导入的 start_applicationV9
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        acad = _get_acad()

    # ==================== 👇 修改位置在这里 👇 ====================
    # 目的：在打开/激活新文件前，先腾出内存位置
    try:
        target_name = Path(file_path).name
        ensure_max_open_documents(keep_filename=target_name, max_count=3)
    except Exception as e:
        sys_logger.error(f"[警告] 启动前清理环境失败: {e}")
    # ==================== 👆 修改位置结束 👆 ====================

    # 规范化路径 (Path 已在头部导入)
    target_path = str(Path(file_path).resolve()).lower()

    # 检查是否已经打开
    try:
        # 这里的 acad 是通过 _get_acad 获取的 COM 对象
        for doc in acad.Documents:
            try:
                if str(Path(doc.FullName).resolve()).lower() == target_path:
                    sys_logger.info(f"[信息] 文件已打开: {file_path}")
                    try:
                        doc.Activate()
                    except:
                        pass
                    return True
            except:
                continue
    except Exception as e:
        sys_logger.warning(f"[警告] 检查已打开文档时出错: {e}")

    # 使用全局导入的 open_dwg_paradigm
    return open_dwg_paradigm(file_path)

#&&% 复制并递增命名
@retry_if_busy(max_retries=5, delay=1.0)
def copy_file_with_increment(filepath):
    """
    复制文件并自动递增命名
    
    Args:
        filepath: 源文件路径
        
    Returns:
        str: 新文件路径，失败返回None
        
    示例:
        copy_file_with_increment('D:/test.dwg')
        # 如果test-1.dwg不存在，创建test-1.dwg
        # 如果test-1.dwg存在，创建test-2.dwg
        # 以此类推
    """
    from pathlib import Path
    import shutil
    
    try:
        source = Path(filepath)
        if not source.exists():
            sys_logger.error(f"[错误] 源文件不存在: {filepath}")
            return None
            
        # 分离文件名和扩展名
        stem = source.stem  # 不带扩展名的文件名
        suffix = source.suffix  # 扩展名（包含.）
        parent = source.parent  # 父目录
        
        # 查找可用的递增编号
        counter = 1
        while True:
            new_name = f"{stem}-{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                break
            counter += 1
            
        # 复制文件
        shutil.copy2(str(source), str(new_path))
        sys_logger.info(f"[成功] 已复制文件: {new_path}")
        return str(new_path)
        
    except Exception as e:
        sys_logger.error(f"[错误] 复制文件失败: {e}")
        return None

# ============================================================================
# 文件保存
# ============================================================================

#&&% 保存文件
@retry_if_busy(max_retries=5, delay=1.0)
def save_file():
    """
    保存当前文件

    Returns:
        bool: 成功返回True
    """
    return save_current_dwg_paradigm()

#&&% 另存为
@retry_if_busy(max_retries=5, delay=1.0)
def save_file_as(output_path):
    """
    另存为

    Args:
        output_path: 保存路径

    Returns:
        bool: 成功返回True
    """
    return save_as_dwg_paradigm(output_path)

# ============================================================================
# 文件关闭
# ============================================================================

#&&% 关闭文件
@retry_if_busy(max_retries=5, delay=1.0)
def close_file(save_option="auto_save"):
    """
    关闭当前文件

    Args:
        save_option: "auto_save"(默认，先保存再关闭), "no_save"(不保存), 其他值走原始策略

    Returns:
        bool: 成功返回True
    """


    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        
        doc=acad.ActiveDocument
        mp = doc.ModelSpace
        sp = doc.PaperSpace
        

    except NameError:
        # 如果没有 活动 对象，尝试直接连接
        acad = win32com.client.Dispatch("AutoCAD.Application")

        doc=acad.ActiveDocument
        mp = doc.ModelSpace
        sp = doc.PaperSpace


    try:
        if save_option == "auto_save":
            save_current_dwg_paradigm()
            return close_current_dwg_paradigm("no_save")
        elif save_option == "no_save":
            try:
                open_paths = get_all_open_dwg_paths()
            except Exception:
                open_paths = []
            cad_zt_oneb()
            for file_path in open_paths:
                try:
                    if file_path and Path(file_path).exists():
                        open_file(file_path)
                except Exception as exc:
                    sys_logger.error(f"[警告] 重新打开 {file_path} 失败: {exc}")
            return True
        else:
            return close_current_dwg_paradigm(save_option)
    except Exception as exc:
        sys_logger.error(f"[错误] 关闭文件失败: {exc}")
        return False


#&&% 清理文件垃圾
@retry_if_busy(max_retries=3, delay=1.0)
def purge_file(deep_purge=True):
    """
    清理当前文档中的未引用对象（块、图层、线型等）。
    
    Args:
        deep_purge (bool): True则执行多次清理以确保彻底（对应PU命令的递归清理）
    """
    try:
        doc = C.doc
        # 方法1: 使用COM对象的 PurgeAll (较温和)
        doc.PurgeAll()
        
        # 方法2: 如果需要深度清理（尤其是注册应用程序），建议发送命令
        # 注意：-PURGE 命令在不同CAD版本参数略有不同，'A'代表All
        if deep_purge:
            # 这是一个强力清理序列：清理所有、不确认
            cmd = "-PURGE\nA\n\nN\n" 
            doc.SendCommand(cmd)
            # 某些顽固垃圾可能需要两遍
            doc.PurgeAll()
            
        sys_logger.info("[成功] 文件清理完成")
        return True
    except Exception as e:
        sys_logger.error(f"[警告] 清理文件失败: {e}")
        return False

#&&% 检查文件是否被锁定
def check_file_locked(filepath):
    """
    通过检查 .dwl 和 .dwl2 隐藏文件来判断 DWG 是否被占用。
    这是最轻量级的检查，不需要启动 CAD。
    
    Returns:
        bool: True 表示文件被锁定（正在使用），False 表示空闲
        str: 如果被锁定，返回占用者的信息（如果有），否则返回空串
    """
    path_obj = Path(filepath)
    if not path_obj.exists():
        return False, "文件不存在"

    # 构建锁文件路径
    dwl_path = path_obj.with_suffix('.dwl')
    dwl2_path = path_obj.with_suffix('.dwl2')

    is_locked = False
    who_locked = ""

    if dwl_path.exists() or dwl2_path.exists():
        is_locked = True
        # 尝试读取 .dwl 文件获取用户名 (如果是文本格式)
        try:
            if dwl_path.exists():
                with open(dwl_path, 'r', encoding='gbk', errors='ignore') as f:
                    who_locked = f.read().strip()
        except:
            who_locked = "未知用户"
            
    return is_locked, who_locked


#&&% 检查当前文档是否只读
def is_read_only():
    """
    检查当前激活文档是否为只读状态
    """
    try:
        doc = C.doc
        # ReadOnly 是 Document 对象的一个属性
        return doc.ReadOnly
    except Exception:
        return False


#&&&% 跨文件操作

#&&% 插入并炸开
@retry_if_busy(max_retries=5, delay=1.0)
def insert_file_exploded(source_file, target_doc=None, x=0, y=0, z=0, scale=1.0, target_layout=None):
    """
    【功能】: 自适应偏移修复版插入函数20260108。
    【逻辑】: 
       1. 不修改源文件，不打开源文件。
       2. 直接读取当前文档的 INSBASE 作为偏移量。
       3. 插入并炸开后，利用 Explode 的返回值直接获取新对象。
       4. 将这些对象反向移动进行纠偏。
    """
    # 1. 智能获取文档
    if target_doc is None:
        target_doc = C.doc

    # 2. 路径标准化
    try:
        real_path = str(Path(source_file).resolve())
        block_name = Path(real_path).stem
    except:
        sys_logger.error(f"❌ 路径错误: {source_file}")
        return False

    if not os.path.exists(real_path):
        return False

    # 3. 获取纠偏向量 (直接读取当前环境的 INSBASE)
    move_vec = (0.0, 0.0, 0.0)
    try:
        # GetVariable 返回的是 tuple (x, y, z)
        base_pt = target_doc.GetVariable("INSBASE")
        
        # 如果 INSBASE 不为 0，说明插入的对象会被 CAD 自动偏移，我们需要把它移回来
        # 逻辑：如果基点是 (X,Y)，插入后图形会偏到 (-X,-Y)，所以我们要移 (+X,+Y)
        if abs(base_pt[0]) > 1e-6 or abs(base_pt[1]) > 1e-6:
            move_vec = base_pt
            sys_logger.info(f"🔍 [纠偏] 检测到环境 INSBASE={base_pt}，将对插入对象执行自动归位。")
    except:
        pass

    # 4. 临时关闭单位缩放 (防止尺寸乱变)
    old_units = 0
    try:
        old_units = target_doc.GetVariable("INSUNITS")
        target_doc.SetVariable("INSUNITS", 0) 
    except: pass

    try:
        # 5. 确定插入空间
        if target_layout:
            try: dest_space = target_doc.Layouts.Item(target_layout).Block
            except: dest_space = target_doc.ModelSpace
        else:
            dest_space = target_doc.ModelSpace

        # 6. 清理旧定义 (防止定义冲突)
        try: target_doc.Blocks.Item(block_name).Delete()
        except: pass

        # 7. 插入块
        pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (float(x), float(y), float(z)))
        sys_logger.info(f"  -> [底层] 正在插入: {block_name}")
        block_ref = dest_space.InsertBlock(pt, real_path, scale, scale, scale, 0.0)

        # 8. 炸开并捕获新对象 (核心优化)
        sys_logger.info(f"  -> [底层] 正在炸开...")
        # Explode() 返回一个 Variant 数组，里面直接包含了炸开后的所有新对象！
        # 这比“记录句柄往前推”更直接、更稳定。
        ##exploded_objects = block_ref.Explode()
        exploded_objects = safe_explode(block_ref)


        # 9. 删除块引用
        block_ref.Delete()

        # 10. 执行纠偏移动 (如果需要)
        if move_vec != (0.0, 0.0, 0.0):
            sys_logger.info(f"  -> [纠偏] 正在移动 {len(exploded_objects)} 个实体归位...")
            
            # 构造起点(0,0,0) 和 终点(move_vec)
            p1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (0.0, 0.0, 0.0))
            p2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, move_vec)
            
            for obj in exploded_objects:
                try:
                    obj.Move(p1, p2)
                except Exception as ex:
                    # 某些特殊对象可能不支持 Move，跳过
                    pass

        # 11. 再次清理块定义
        try: target_doc.Blocks.Item(block_name).Delete()
        except: pass 

        return True

    except Exception as e:
        sys_logger.error(f"❌ [insert_file_exploded] 失败: {e}")
        return False
        
    finally:
        # 恢复单位
        try: target_doc.SetVariable("INSUNITS", old_units)
        except: pass


#&&% 拷贝文件内容_20260118
@retry_if_busy(max_retries=5, delay=1.0)
def copy_file_content_pywin32(
    source_file, 
    target_file, 
    target_x=0, target_y=0, 
    scale=1.0, 
    rotation=0.0,
    target_layout=None,
    explode=True
):
    """
    【函数编号】: IO-Full-Transfer-V2.0 (全图插入版)
    【功能】: 将 source_file 的全部模型空间内容，作为一个整体插入到 target_file 的指定坐标。
    【原理】: 
        1. 副本机制: 创建源文件的临时副本 (避开文件占用/锁死问题)。
        2. InsertBlock: 利用 CAD 原生插入能力，将副本作为块插入。
        3. 坐标逻辑: 源文件的原点(0,0) 将被放置在 (target_x, target_y)。
        4. 深度清理: 炸开后彻底删除块定义，不留垃圾。

    【参数】:
        source_file: 源文件路径
        target_file: 目标文件路径 (如果已打开则激活，未打开则打开)
        target_x, target_y: 插入点 (对应源文件的 0,0 点)
        scale: 缩放比例
        rotation: 旋转角度 (度)
        target_layout: 插入到哪个布局 (None=模型空间)
        explode: 插入后是否炸开 (True=炸开成实体, False=保留为块)
    
    【返回值】: bool 成功/失败
    """
    import win32com.client
    import pythoncom
    import os
    import time
    import tempfile
    import shutil
    from pathlib import Path

    sys_logger.info(f"🚀 [Full-Transfer-V2] 启动全图合并...")
    
    # 1. 路径检查
    src_path = Path(source_file)
    if not src_path.exists():
        sys_logger.error(f"❌ 源文件不存在: {source_file}")
        return False

    # 2. 创建临时副本 (关键步骤：防止源文件被占用导致 Insert 失败)
    # 我们不直接 Insert 源文件，而是 Insert 它的副本
    temp_dir = Path(tempfile.gettempdir())
    temp_copy_path = temp_dir / f"full_insert_{int(time.time())}.dwg"
    
    try:
        shutil.copy2(src_path, temp_copy_path)
        sys_logger.info(f"  📄 创建临时副本: {temp_copy_path.name}")
    except Exception as e:
        sys_logger.error(f"❌ 创建副本失败: {e}")
        return False

    # ==========================================
    # 阶段: 插入操作
    # ==========================================
    try:
        # 1. 打开/激活目标文件
        sys_logger.info(f"  📂 准备目标: {Path(target_file).name}")
        if not open_file(target_file): 
            return False
        
        doc_tgt = C.doc  # 获取当前激活文档
        
        # 2. 切换空间 (模型 vs 布局)
        if target_layout:
            try: 
                doc_tgt.ActiveLayout = doc_tgt.Layouts.Item(target_layout)
                dest_space = doc_tgt.ActiveLayout.Block
            except: 
                sys_logger.warning(f"  ⚠️ 布局 {target_layout} 不存在，转为模型。")
                dest_space = doc_tgt.ModelSpace
        else:
            doc_tgt.SetVariable("TILEMODE", 1) # 切换到模型
            dest_space = doc_tgt.ModelSpace

        # 3. 准备插入参数
        # 注意：源文件的 (0,0) 会对齐到这里的 (target_x, target_y)
        pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (float(target_x), float(target_y), 0.0))
        
        # 4. 清理潜在的同名块定义 (防止旧定义导致插入内容不更新)
        block_name = temp_copy_path.stem
        try: 
            doc_tgt.Blocks.Item(block_name).Delete()
            sys_logger.info("  🧹 清理了旧的同名块定义")
        except: pass
        
        # 5. 执行插入 (InsertBlock)
        sys_logger.info(f"  🔄 正在插入全图... (Pos: {target_x}, {target_y})")
        # 参数: 插入点, 文件路径, X比例, Y比例, Z比例, 旋转
        block_ref = dest_space.InsertBlock(pt, str(temp_copy_path), scale, scale, scale, rotation)
        
        # 6. 强制冷却 (防 RPC 忙碌)
        time.sleep(1.0)
        
        if not explode:
            sys_logger.info("  ✨ 插入完成 (保留为块引用)")
            doc_tgt.Save()
            return True

        # 7. 炸开逻辑 (Retry Loop)
        sys_logger.info("  💥 正在炸开合并...")
        exploded = False
        for i in range(5):
            try:
                block_ref.Explode()
                exploded = True
                sys_logger.info(f"     ✅ 成功 (Attempt {i+1})")
                break
            except Exception as e:
                if "rejected" in str(e) or "busy" in str(e):
                    sys_logger.info(f"     ⏳ CAD忙碌，重试炸开 ({i+1}/5)...")
                    time.sleep(0.5 + i * 0.5)
                else:
                    # 某些特殊块无法炸开 (如非统一比例)，虽然这里我们设的都是 scale
                    sys_logger.error(f"     ⚠️ 炸开遇到非忙碌错误: {e}")
                    time.sleep(1.0)
        
        # 8. 收尾清理
        if exploded:
            # 删除块引用本身 (Explode 会生成新对象，原块引用还在)
            try: block_ref.Delete()
            except: pass
            
            # 删除块定义 (彻底清除数据依赖，减小文件体积)
            try: doc_tgt.Blocks.Item(block_name).Delete()
            except: pass
            
            # 删除磁盘上的临时文件
            try: temp_copy_path.unlink()
            except: pass
            
            doc_tgt.Save()
            sys_logger.info("  ✨ 全图合并完成")
            return True
        else:
            sys_logger.error("  ⚠️ 炸开失败，保留原块。")
            doc_tgt.Save()
            try: temp_copy_path.unlink()
            except: pass
            return True

    except Exception as e:
        sys_logger.error(f"❌ 全图插入失败: {e}")
        # 失败也要尝试清理临时文件
        try: temp_copy_path.unlink()
        except: pass
        return False


#&&% 跨文件插入区域_20260116

@retry_if_busy(max_retries=5, delay=1.0)
def insert_region_v2(
    src_dwg, 
    target_dwg, 
    x1, y1, x2, y2, 
    target_x, target_y,
    target_layout=None
):
    """
    【函数编号】: IO-Region-Transfer-V2.0 (WBlock 极速版)
    【功能】: 将 src_dwg 指定区域的内容，精确插入到 target_dwg 的指定位置。
    【原理】: 
        1. WBlock提取: 仅提取选区内容到临时文件 (极快)。
        2. 数学偏移: 计算 (Target - Source) 向量，直接插入到偏移点。
        3. 抗扰炸开: 内置 COM 忙碌重试机制。


    如果target_dwg是当前激活文件，src_dwg没有打开，则src_dwg会被插入，插入后保存，target_dwg不会关闭，src_dwg关闭。

    如果target_dwg是打开文件，src_dwg也打开甚至激活，则src_dwg会被插入，插入后保存，target_dwg不会关闭，src_dwg关闭。

    如果target_dwg，src_dwg都未打开，则src_dwg会被插入，插入后保存，target_dwg不会关闭，src_dwg关闭。

    如果src_dwg打开，则src_dwg会被插入，插入后保存，target_dwg不会关闭，src_dwg关闭。

    总之，操作后target_dwg不会关闭，src_dwg关闭，不论之前是什么状态，包括多文件状态可能包含源和目标文件。

    """
    import win32com.client
    import pythoncom
    import os
    import time
    import tempfile
    from pathlib import Path

    sys_logger.info(f"🚀 [Region-V2] 启动跨文件传输...")
    
    # 坐标规范化
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    
    # 临时文件路径
    temp_wblock_path = Path(tempfile.gettempdir()) / f"wb_{int(time.time())}.dwg"
    if temp_wblock_path.exists():
        try: temp_wblock_path.unlink()
        except: pass

    # ==========================================
    # 阶段 1: WBlock 提取源数据 (只读操作)
    # ==========================================
    try:
        # 1. 打开源文件 (不做任何修改，安全)
        sys_logger.info(f"  📖 读取源: {Path(src_dwg).name}")
        if not open_file(src_dwg): return False
        
        doc_src = C.doc
        
        # 2. 创建选择集 (窗选区域)
        try: doc_src.SelectionSets.Item("TempExportSS").Delete()
        except: pass
        ss = doc_src.SelectionSets.Add("TempExportSS")
        
        p1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x_min, y_min, 0))
        p2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x_max, y_max, 0))
        
        # 模式 5 = acSelectionSetWindow (完全包含在框内的对象)
        # 模式 1 = acSelectionSetCrossing (碰到框的对象) -> 建议用 Crossing 防止漏选
        ss.Select(1, p1, p2) 
        
        if ss.Count == 0:
            sys_logger.warning("  ⚠️ 选区为空，取消操作。")
            return False
            
        # 3. 执行 WBlock (写块到磁盘)
        # 注意: WBlock 导出的文件，保持原坐标系！这正是我们想要的。
        # 对象在 (100,100)，导出的文件里它还在 (100,100)。
        sys_logger.info(f"  💾 WBlock 导出 {ss.Count} 个对象...")
        doc_src.Wblock(str(temp_wblock_path), ss)
        
        # 4. 关闭源文件 (释放锁)
        # False = 不保存源文件，因为我们只是选了一下
        doc_src.Close(False) 
        time.sleep(0.5) # 冷却
        
    except Exception as e:
        sys_logger.error(f"❌ 导出阶段失败: {e}")
        return False

    # ==========================================
    # 阶段 2: 偏移插入 (写入操作)
    # ==========================================
    try:
        # 1. 打开目标文件
        sys_logger.info(f"  📂 打开目标: {Path(target_dwg).name}")
        if not open_file(target_dwg): return False
        
        doc_tgt = C.doc
        
        # 2. 切换空间
        if target_layout:
            try: 
                doc_tgt.ActiveLayout = doc_tgt.Layouts.Item(target_layout)
                dest_space = doc_tgt.ActiveLayout.Block
            except: 
                sys_logger.warning(f"  ⚠️ 布局 {target_layout} 不存在，转为模型。")
                dest_space = doc_tgt.ModelSpace
        else:
            doc_tgt.SetVariable("TILEMODE", 1)
            dest_space = doc_tgt.ModelSpace

        # 3. 计算数学偏移量 (核心算法)
        # 源内容的基准点是 (x_min, y_min)。
        # 我们想让这个基准点，落在目标的 (target_x, target_y)。
        # 插入点 InsertPt = Target - Source
        ins_x = target_x - x_min
        ins_y = target_y - y_min
        
        sys_logger.debug(f"  🧮 坐标映射: Src({x_min:.1f}) -> Tgt({target_x:.1f}) | Offset=({ins_x:.1f}, {ins_y:.1f})")
        
        # 4. 插入块
        pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (ins_x, ins_y, 0))
        
        # 清理同名块定义 (防止无法更新)
        block_name = temp_wblock_path.stem
        try: doc_tgt.Blocks.Item(block_name).Delete()
        except: pass
        
        sys_logger.info("  🔄 正在插入...")
        block_ref = dest_space.InsertBlock(pt, str(temp_wblock_path), 1.0, 1.0, 1.0, 0.0)
        
        # 5. 强制冷却 (防 Call Rejected)
        time.sleep(1.0)
        
        # 6. 抗干扰炸开 (Retry Loop)
        sys_logger.info("  💥 正在炸开...")
        exploded = False
        for i in range(5):
            try:
                block_ref.Explode()
                exploded = True
                sys_logger.info(f"     ✅ 成功 (Attempt {i+1})")
                break
            except Exception as e:
                if "rejected" in str(e) or "busy" in str(e):
                    time.sleep(0.5 + i * 0.5)
                else:
                    time.sleep(1.0)
        
        # 7. 收尾
        if exploded:
            try: block_ref.Delete()
            except: pass
            
            # 清理块定义
            try: doc_tgt.Blocks.Item(block_name).Delete()
            except: pass
            
            # 清理临时文件
            try: temp_wblock_path.unlink()
            except: pass
            
            doc_tgt.Save()
            sys_logger.info("  ✨ 传输完成")
            return True
        else:
            sys_logger.error("  ⚠️ 炸开失败，保留原块。")
            doc_tgt.Save()
            return True

    except Exception as e:
        sys_logger.error(f"❌ 插入阶段失败: {e}")
        import traceback; traceback.print_exc()
        return False

#&&&% 多文档控制

#&&% 设置激活文档
@retry_if_busy(max_retries=10, delay=0.5)
def set_active_doc(doc):
    """
    将指定文档 doc 设置为当前激活窗口。
    原理：激活后通常需要重新建立连接 (li) 才能操作新文档。
    """
    try:
        doc.Activate()
        time.sleep(0.3)  # [物理避让] 稍作延时，确保激活生效
        sys_logger.info("[OK] 当前激活文档：", doc.Name)
        return True
    except Exception as e:
        sys_logger.error("[错误] 激活文档失败：", e)
        return False

#&&% 按名称获取文档
@retry_if_busy(max_retries=10, delay=0.5)
def get_doc_by_name(name): 
    """
    通过文件名获取 AutoCAD 文档对象，例如 '空白.dwg'
    如果未找到，返回 None
    """
    # 每次调用都重新获取 app，防止对象失效
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    for doc in acad.Documents:
        if doc.Name.lower() == name.lower():
            return doc
    return None

#&&% 获取打开文档名
@retry_if_busy(max_retries=10, delay=0.5)
def get_open_document_names():
    """返回所有打开的文件名列表"""
    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        return [doc.Name for doc in acad.Documents]
    except Exception:
        # 如果获取失败，尝试通过 C 对象获取
        if C.app:
            return [doc.Name for doc in C.app.Documents]
        raise # 抛出异常让 retry 捕获

#&&% 安全关闭当前文件
def close_current_drawing_safely():
    """
    安全关闭当前 DWG 文件，确保确实关闭并重新连接。
    最多尝试 3 次。
    """
    
    try:
        Name1 = doc.Name
    except:
        sys_logger.warning("[警告]️ 当前 doc 无法获取名称，可能未连接。")

        doc=C.doc

        Name1 = doc.Name
    
    for attempt in range(1, 4):  # 最多尝试3次
        sys_logger.info(f"🔄 第 {attempt} 次尝试关闭 '{Name1}'")
        close_dwg_by_name(Name1)

        doc=C.doc  # 重新连接 acad、doc、mp、sp 等
        try:
            Name2 = doc.Name
        except:
            Name2 = None

        if Name2 != Name1:
            sys_logger.info(f"🟢 已确认文件 '{Name1}' 关闭，当前打开文件为 '{Name2}'")
            doc=C.doc  # 再执行一次，确保变量正确
            return
        else:
            sys_logger.warning("[警告]️ 文件仍未关闭，继续尝试...")

    sys_logger.info(f"[错误] 多次尝试仍未成功关闭 '{Name1}'，请手动检查。")


#&&% 关闭除当前激活文档外的所有 DWG 文件

def close_all_except_active_safe():
    """
    更稳定地关闭除当前激活文档外的所有 DWG 文件，避免 COM 对象断链。
    """
    try:
        active_name = acad.ActiveDocument.Name
        all_names = [acad.Documents.Item(i).Name for i in range(acad.Documents.Count)]
        closed = 0

        for name in all_names:
            if name != active_name:
                try:
                    doc = acad.Documents.Item(name)
                    doc.Close(False)  # 不保存直接关闭
                    sys_logger.info(f"[已关闭] {name}")
                    closed += 1
                except Exception as e:
                    sys_logger.info(f"[警告] 无法关闭 {name}: {e}")

        sys_logger.info(f"[OK] 成功关闭 {closed} 个文档，仅保留 {active_name}")

    except Exception as e:
        sys_logger.info(f"[错误] 安全关闭失败：{e}")


#&&% 按名称关闭DWG
@retry_if_busy(max_retries=5, delay=1.0)
def close_dwg_by_name(Name):
    """
    关闭当前桌面中名为 Name 的 DWG 文件。
    如果文件已打开，则关闭该文件。
    
    参数：
        Name: 要关闭的 DWG 文件的名称（如 "example.dwg"）不含路径的名
    """
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application")  # 获取 AutoCAD 应用
        doc = acad.Documents.Item(Name)  # 获取指定名称的文档
        
        if doc:
            doc.Close(False)  # 关闭文件，不提示保存
            sys_logger.info(f"[OK] 文件 '{Name}' 已关闭")
        else:
            sys_logger.error(f"[错误] 未找到名为 '{Name}' 的文件")
    except Exception as e:
        sys_logger.error(f"[错误] 关闭文件 '{Name}' 失败: {e}")


#&&% 关闭所有文件
@retry_if_busy(max_retries=5, delay=1.0)
def close_all_files(save_option="auto_save"):
    """
    关闭所有文件
   
    默认保存后再关闭就不会跳出要保存吗的弹窗

    Returns:
        bool: 成功返回True
    """
    if save_option == "no_save":
        try:
            open_paths = get_all_open_dwg_paths()
        except Exception:
            open_paths = []
        cad_zt_oneb()
        for file_path in open_paths:
            try:
                if file_path and Path(file_path).exists():
                    open_file(file_path)
            except Exception as exc:
                sys_logger.error(f"[警告] 重新打开 {file_path} 失败: {exc}")
        return True

    try:
        
        names = get_open_document_names()
    except Exception:
        return close_all_dwg_paradigm()

    if not names:
        return True

    for name in names:
        try:
            activate_document_by_name(name)
        except Exception:
            pass

        if save_option == "auto_save":
            try:
                save_current_dwg_paradigm()
            except Exception:
                pass
            close_current_dwg_paradigm("no_save")
        else:
            close_current_dwg_paradigm(save_option)
    return True

#&&% 安全限制打开文件数量
def ensure_max_open_documents(keep_filename, max_count=3):
    """
    【核心修复】安全地限制打开文件数量
    解决：遍历 Documents 集合时关闭文件导致的索引错误 & RPC 拒绝错误

    """
    
    try:
        
        acad = C.acad
        docs = acad.Documents
        current_count = docs.Count
        
        if current_count <= max_count:
            return

        sys_logger.info(f"[清理] 当前打开 {current_count} 个文件，尝试压缩至 {max_count} 个...")

        # 1. 先建立“黑名单” (只记录名字，不直接操作对象)
        #    我们要保留 keep_filename，其他的列入关闭计划
        #    同时尽量避开 ActiveDocument (如果是源文件)
        docs_to_close = []
        active_name = ""
        try: active_name = acad.ActiveDocument.Name
        except: pass

        for i in range(current_count):
            try:
                # 注意：COM 索引从 0 开始
                doc = docs.Item(i)
                d_name = doc.Name
                
                # 跳过要保留的文件
                if d_name.lower() == keep_filename.lower():
                    continue
                    
                # 暂时把 ActiveDocument 放到最后处理，或者跳过
                if d_name == active_name:
                    continue
                    
                docs_to_close.append(d_name)
            except: pass

        # 2. 按照名单逐个关闭
        closed_count = 0
        for name in docs_to_close:
            # 如果已经达标，就停手
            if docs.Count <= max_count: break
            
            try:
                # 通过名字重新获取对象并关闭
                target = docs.Item(name)
                # Close(False) 表示不保存直接关闭
                target.Close(False)
                sys_logger.info(f"  [OK] 已关闭冗余文件: {name}")
                closed_count += 1
            except Exception as e:
                sys_logger.error(f"  [跳过] 关闭 {name} 失败: {e}")

        # 3. 如果还是太多，最后尝试动一下 ActiveDocument (除了 keep_file)
        if docs.Count > max_count and active_name.lower() != keep_filename.lower():
             try:
                 acad.ActiveDocument.Close(False)
             except: pass

    except Exception as e:
        sys_logger.error(f"[警告] 文件清理过程异常: {e}")


#&&&% 空间操作

#&&%判定在什么空间
@retry_on_busy(max_retries=5, base_delay=0.2)
def get_obj_loc(obj):
    """
    判断对象所在的数据库空间。
    注意：这里去掉了宽泛的 try...except，让 COM 错误能传导给装饰器，
    从而触发 retry_on_busy 的重试机制。
    """
    doc = C.doc

    # 1. 这一步是高频报错点 (CAD忙时 ObjectIdToObject 会失败)
    # 让装饰器来处理这里的异常
    owner_btr = doc.ObjectIdToObject(obj.OwnerID)
    btr_name = owner_btr.Name
    
    if btr_name.upper() == "*MODEL_SPACE":
        return 1  # 模型空间
    elif btr_name.upper().startswith("*PAPER_SPACE"):
        return 0  # 图纸空间
    else:
        return -1 # 块定义内部或其他


#&&% 空间切换
@retry_on_busy(max_retries=5, base_delay=0.2)
def set_space_mode(mode_val):
    """
    【功能】: 强制切换当前空间
    【参数】: 1=模型, 0=布局
    """
    doc = C.doc 
    
    # SetVariable 是原子操作，非常适合重试
    # 如果 CAD 正忙（例如正在自动保存），这一步会报错，装饰器会捕获并重试
    doc.SetVariable("TILEMODE", mode_val)

    # 确保退出视口 (PSPACE)
    if mode_val == 0:
        # 这个属性设置偶尔也会因为 RPC 冲突失败，也需要重试
        doc.MSpace = False 
        
    return True


#&&% 布局切换


def switch_to_layout(layout_name, retry=10, delay=0.5):
    """
    【核心修复】切换布局 (增强版)
    功能：
      1. 检查是否已经在该布局，是则直接返回。
      2. 包含 RPC 忙碌自动重试机制 (解决 -2147418111 错误)。
      3. 包含 Command 强行切换兜底。

    @retry_on_busy不要加

    """
    doc = C.doc
    
    # 1. 快速检查：如果已经在目标布局，秒回
    try:
        if doc.ActiveLayout.Name == layout_name:
            return True
    except: pass

    # 2. 循环尝试切换
    sys_logger.info(f"🔄 正在切换至布局: {layout_name} ...")
    
    for i in range(retry):
        try:
            # 尝试 A: 标准 COM 切换
            lay = doc.Layouts.Item(layout_name)
            doc.ActiveLayout = lay
            
            # 刷新一下状态
            C.acad.ActiveDocument = doc 
            return True
            
        except Exception as e:
            # 捕获 "被呼叫方拒绝" (-2147418111) 或其他 COM 错误
            err_msg = str(e)
            
            # 如果是布局不存在，直接放弃，别重试了
            if "Item" in err_msg and "此时无法" in err_msg: # 具体的错误特征可能不同，但通常 COM 会报找不到
                sys_logger.info(f"❌ 布局不存在: {layout_name}")
                return False

            if i < retry - 1:
                # 只有在最后几次尝试时才打印 Log，避免刷屏
                if i > 2: 
                    sys_logger.info(f"   ⏳ CAD忙碌，等待重试 ({i+1}/{retry})...")
                time.sleep(delay)
                
                # 【强力手段】尝试 B: 发送命令 (异步绕过 COM 锁)
                # 在第 3 次和第 7 次失败时尝试
                if i in [3, 7]:
                    try: 
                        doc.SendCommand(f"LAYOUT S \"{layout_name}\"\n")
                        # 发送命令后稍微多睡会儿
                        time.sleep(1.0)
                        # 检查是否切换成功
                        if doc.ActiveLayout.Name == layout_name:
                            return True
                    except: pass
            else:
                sys_logger.info(f"❌ 切换布局失败 (已尝试{retry}次): {e}")
                return False
                
    return False


#&&% 获取所有布局名称
def get_layout_names(exclude_model=False):
    """
    获取当前文档所有布局的名称列表。
    """
    try:
        doc = C.doc
        layouts = []
        for layout in doc.Layouts:
            name = layout.Name
            if exclude_model and name == "Model":
                continue
            layouts.append(name)
        # 很多时候我们需要按Tab顺序排序，但在COM里Layouts集合默认不一定是排序的
        # 这里简单返回列表
        return layouts
    except Exception as e:
        sys_logger.error(f"[错误] 获取布局列表失败: {e}")
        return []


#&&&% 获取文件路径

#&&% 获取当前激活DWG路径 (修复版)
def get_current_dwg_path():
    """
    【函数编号】: SYS-001
    【功能描述】: 获取当前激活 DWG 文件的完整长路径。
    """
    try:
        doc = C.doc
        # 1. 尝试获取 FullName
        full_path = doc.FullName
        
        # 2. 校验是否为空
        if not full_path:
            name = doc.Name
            sys_logger.info(f"⚠️ 当前图纸 [{name}] 尚未保存到硬盘，无物理路径。")
            return None
            
        # 3. 关键修复：转换为长路径
        return get_long_path(full_path)

    except Exception as e:
        sys_logger.info(f"❌ 获取文件路径失败: {e}")
        return None


#&&% 获取所有打开DWG路径 (修复版)
@retry_if_busy(max_retries=10, delay=0.5)
def get_all_open_dwg_paths():
    """返回当前会话中所有已打开 DWG 的完整路径列表（强制转换为长路径）。"""
    paths = []
    
    # 确保 C.acad 连接正常
    try:
        acad = C.acad
        docs = acad.Documents
    except:
        return []

    for doc in docs:
        try:
            full_name = doc.FullName
            if full_name:
                # 关键修复：转换为长路径
                long_name = get_long_path(full_name)
                paths.append(long_name)
        except Exception:
            continue
            
    return paths


def current_dwg_folder():
    """返回当前激活 DWG 所在文件夹；未保存文件返回 None。"""
    try:
        doc = C.raw_doc
    except Exception:
        doc = None
    if doc is None:
        return None

    try:
        full_name = str(getattr(doc, "FullName", "") or "").strip()
        if not full_name:
            return None
        return str(Path(get_long_path(full_name)).parent)
    except Exception:
        return None


def get_long_path(path_str):
    """
    【核心修复】将 Windows 8.3 短路径 (如 D:\CLAUDE~1\...) 转换为完整长路径。
    同时处理大小写规范化。
    """
    if not path_str:
        return None
    
    # 去除可能存在的首尾引号 (修复你日志里的那个错误)
    clean_path = path_str.strip().strip("'").strip('"')
    
    try:
        # 1. 获取长路径 (核心)
        long_path = win32api.GetLongPathName(clean_path)
        # 2. 规范化分隔符 (把 / 变成 \)
        return os.path.normpath(long_path)
    except Exception:
        # 如果转换失败（比如文件还是内存临时态），返回原清洗后的路径
        return os.path.normpath(clean_path)
