# Supervised Task Packet
role: reviewer
title: print-standard-review

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦 findings-first 审查，不要自行猜测工作区路径，严格基于主控提供的上下文回答。

## Objective
做 findings-first 审查。只基于提供的文件和上下文，找当前标准图幅匹配与PDF页尺寸校验最可能的bug、回归或遗漏。若没有高置信发现，要明确说 no findings。

## Context
复杂工程DWG真实打印49/49成功；新验证显示49份PDF页面尺寸全部匹配计划图幅；其中standard_flag=1有45张，standard_flag=0有4张。不要建议大重构，只看高置信问题。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.

## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/print_area_analysis.py
# -*- coding: utf-8 -*-
"""print_area_analysis.py

本脚本用于“打印区域(打印框)”分析。

约束与假设：
- 打印范围使用“矩形多段线”表示。
- 打印多段线之间不应放置仅用于分隔的矩形多段线（否则会干扰包含关系）。
- 允许存在“外包大矩形”包裹若干打印多段线：脚本采用“极大矩形”算法识别真实打印区域。
- 使用“外包盒短边的万分之五(0.0005*w_short)”作为动态容差：
  - 用于矩形识别（顶点聚类/坐标分类）
  - 用于多段线去重（空间重叠）
  - 用于包含关系判断
- 允许 1:100 系列与 1:1 系列（通过 *0.01 得到）在同一文件中同时出现。

输出：
- 提供：
  1) 严格标准匹配（只匹配288标准值）
  2) 近似匹配（总能返回最接近的标准）
  3) 打印区域提取（模型空间 + 各布局空间）

注意：
- 脚本为“纯函数式模块”（无类），但根据需求包含必要的 CAD 数据库写操作：
  - 删除伪打印区域外框（并在删除前用 4 条直线保留其边界信息）。

路径可随 /cad 项目一起迁移，使用 system.licad 的 C 连接 CAD。
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# -----------------------------------------------------------------------------
# bootstrap: allow free migration under /cad
# -----------------------------------------------------------------------------
current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent
sys.path.insert(0, str(current))

from system.project_setup import PathConfig  # noqa: F401
from system.licad import C

# CAD_selection 提供的选择与早绑定 get/set
from system.CAD_selection import (
    select_polyline,
    select_polyline_chuantong,
    get_attr,
    set_attr,
)

# CAD_file_operations 提供的空间/布局辅助（若导入失败则启用本地实现）
try:
    from scripts.CAD_file_operations import get_obj_loc, set_space_mode, switch_to_layout, get_layout_names
except Exception:  # pragma: no cover

    def get_obj_loc(obj: Any) -> int:
        """1=模型空间,0=图纸空间,-1=其他"""
        doc = C.doc
        owner_btr = doc.ObjectIdToObject(obj.OwnerID)
        btr_name = owner_btr.Name
        if str(btr_name).upper() == "*MODEL_SPACE":
            return 1
        if str(btr_name).upper().startswith("*PAPER_SPACE"):
            return 0
        return -1

    def set_space_mode(mode_val: int) -> bool:
        doc = C.doc
        doc.SetVariable("TILEMODE", mode_val)
        if mode_val == 0:
            doc.MSpace = False
        return True

    def switch_to_layout(layout_name: str, retry: int = 10, delay: float = 0.5) -> bool:
        doc = C.doc
        for i in range(retry):
            try:
                lay = doc.Layouts.Item(layout_name)
                doc.ActiveLayout = lay
                C.acad.ActiveDocument = doc
                return True
            except Exception:
                time.sleep(delay)
        return False

    def get_layout_names(exclude_model: bool = False) -> List[str]:
        doc = C.doc
        out = []
        for layout in doc.Layouts:
            name = layout.Name
            if exclude_model and name == "Model":
                continue
            out.append(name)
        return out


# -----------------------------------------------------------------------------
# 标准打印框：48 + (100%,110%,120%) + (*1, *0.01) => 288
# -----------------------------------------------------------------------------
LB_dayingkuang: List[Tuple[int, int, int]] = [
    (118900, 84100, 100),  (178350, 126150, 150),   (59450, 42050, 50),    (29725, 21025, 25),
    (133800, 84100, 100),  (200700, 126150, 150),   (66900, 42050, 50),    (33450, 21025
...[truncated]...


## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/print_verifier.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from collections import Counter
import logging
from pathlib import Path
import re
from typing import Any
import warnings

from pypdf import PdfReader


MM_PER_POINT = 25.4 / 72.0
logging.getLogger("pypdf").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", module="pypdf")


def _job_value(job: Any, key: str, default: Any = None) -> Any:
    if isinstance(job, dict):
        return job.get(key, default)
    return getattr(job, key, default)


def _parse_media_size_mm(media: str) -> tuple[float, float] | None:
    if not media:
        return None
    iso_match = re.search(r"\(([0-9.]+)_x_([0-9.]+)_MM\)", media)
    if iso_match:
        return float(iso_match.group(1)), float(iso_match.group(2))
    user_defined_match = re.search(r"UserDefinedMetric \(([0-9.]+) x ([0-9.]+)", media)
    if user_defined_match:
        return float(user_defined_match.group(1)), float(user_defined_match.group(2))
    return None


def _read_pdf_page_size_mm(pdf_path: Path) -> tuple[float, float] | None:
    try:
        reader = PdfReader(str(pdf_path), strict=False)
        if not reader.pages:
            return None
        page = reader.pages[0]
        width_mm = float(page.mediabox.width) * MM_PER_POINT
        height_mm = float(page.mediabox.height) * MM_PER_POINT
        return min(width_mm, height_mm), max(width_mm, height_mm)
    except Exception:
        return None


def _verify_page_sizes(existing_paths: list[str], jobs: list[Any], size_tol_mm: float) -> dict:
    job_by_output = {}
    for job in jobs:
        output_path = _job_value(job, "output_path", "")
        if output_path:
            job_by_output[str(Path(output_path))] = job

    checked = 0
    matched = 0
    mismatches: list[dict[str, Any]] = []
    unparsed: list[dict[str, Any]] = []
    standard_flags = Counter()

    for item in existing_paths:
        job = job_by_output.get(str(Path(item)))
        if job is None:
            continue
        standard_flags[int(_job_value(job, "standard_flag", 0))] += 1
        expected = _parse_media_size_mm(str(_job_value(job, "media", "")))
        actual = _read_pdf_page_size_mm(Path(item))
        if expected is None or actual is None:
            unparsed.append(
                {
                    "output_path": item,
                    "media": _job_value(job, "media", ""),
                    "expected_mm": expected,
                    "actual_mm": actual,
                    "standard_flag": int(_job_value(job, "standard_flag", 0)),
                }
            )
            continue

        checked += 1
        expected_short, expected_long = min(expected), max(expected)
        actual_short, actual_long = actual
        delta_short = abs(actual_short - expected_short)
        delta_long = abs(actual_long - expected_long)
        if delta_short <= size_tol_mm and delta_long <= size_tol_mm:
            matched += 1
            continue

        mismatches.append(
            {
                "output_path": item,
                "media": _job_value(job, "media", ""),
                "expected_mm": [round(expected_short, 2), round(expected_lon
...[truncated]...
