# Supervised Task Packet
role: tester
title: print-validation-gap-check-mini

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦测试结论与阻塞，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。

## Objective
只从测试视角判断：在已知真实打印49/49成功且PDF页尺寸49/49匹配的前提下，当前证据能支持到什么范围，还缺什么最小测试。请简短回答。

## Context
文件只看print_verifier.py。当前结论目标是：这批复杂工程案例的输出PDF图纸规格正确。不要扩展到没证据的范围。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.

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
     
...[truncated]...
