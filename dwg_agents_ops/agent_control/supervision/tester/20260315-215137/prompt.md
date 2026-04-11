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
    on
...[truncated]...


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
          "sequence_no": 1
...[truncated]...
