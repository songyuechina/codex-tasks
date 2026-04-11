# Supervised Task Packet
role: reviewer
title: print-stability-review

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦 findings-first 审查，不要自行猜测工作区路径，严格基于主控提供的上下文回答。

## Objective
基于给定文件与结果，指出这次打印修复后最主要的剩余风险，限定1-2条，必须 findings-first。

## Context
已实测：典型文件布局9/9成功，混合46/46成功。请只看剩余风险，不要重复成功结论。

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
from system.CAD_core import open_dwg_paradigm
from system.CAD_coordination import wait_quiescent
from system.licad import C

from print_executor import PrintDefaults, execute_print_plan
from print_policy import build_print_plan, plan_to_dict, save_plan_json
from print_verifier import verify_generated_pdfs


DEFAULT_CASE = MODULE_DIR / "cases" / "assets" / "混合空间0109.dwg"


def _make_run_dirs(dwg_path: Path, output_root: Path) -> tuple[Path, Path, Path]:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_root = output_root / dwg_path.stem / stamp
    work_dir = run_root / "work
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
class 
...[truncated]...


## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/cases/output/混合空间0109/20260316-001916/print_summary.json
{
  "run_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260316-001916",
  "work_dwg": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260316-001916\\work\\混合空间0109__print_work.dwg",
  "plan_json": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260316-001916\\print_plan.json",
  "plan": {
    "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260316-001916\\work\\混合空间0109__print_work.dwg",
    "output_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260316-001916\\pdf",
    "total_jobs": 46,
    "landscape_count": 46,
    "portrait_count": 0,
    "jobs_by_space": {
      "model": [
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\混合空间0109\\20260316-001916\\work\\混合空间0109__print_work.dwg",
          "space_kind": "model",
          "layout_name": "model",
          "owner_btr": "*MODEL_SPACE",
          "handle": "12887",
          "lower_left": [
            380662.0,
            3073909.0
         
...[truncated]...
