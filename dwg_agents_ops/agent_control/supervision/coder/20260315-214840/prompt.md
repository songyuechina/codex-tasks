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
    d
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
