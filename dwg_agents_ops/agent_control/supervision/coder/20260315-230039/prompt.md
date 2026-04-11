# Supervised Task Packet
role: coder
title: layout-print-stability

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦实现推进，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。

## Objective
基于给定文件，指出导致布局批量打印不稳定的最可能根因，并给出最小修复建议。只允许给出2-4条具体建议。

## Context
已知：模型空间37张成功，布局识别9张；曾出现切换布局失败、被呼叫方拒绝接收呼叫、同名文档误激活。请优先判断执行器和打开文档流程。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.

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

    run_root, work_dir, pdf_dir = _make_run_dirs(dwg_path, output_r
...[truncated]...


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
        time.sleep(0.
...[truncated]...


## File: D:/codex-tasks/cad/system/CAD_core.py
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
from system.licad import C

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

# 3.2 导入 CAD 基础功能 (CAD_basic)
try:
    import scripts.CAD_basic as cb
    from scripts.CAD_basic import (
        close_all_cad_processes,
        start_applicationV9,
        get_acad_doc,
        jingchengshu_wenjian,


        safe_delete,
        last_obj,
        group_bbox_corners,
        com_retry,
        get_object_property,
        ensure_list,
        
    )
except ImportError as e:
...[truncated]...
