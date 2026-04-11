# Supervised Task Packet
role: tester
title: print-validation-gap-check

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦测试结论与阻塞，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。

## Objective
基于提供文件和上下文，判断当前验证是否足以支持“打印出来的pdf图纸规格正确”这个结论；列出仍缺什么测试，如果现有证据已经足够说明某个范围，也要指出范围。

## Context
已有真实打印49/49成功；verify_generated_pdfs新增了页面尺寸校验，结果49/49匹配，0 mismatch。需要测试视角，不要泛泛而谈。

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
    work_dir = run_root / "work"
    pdf_dir = run_root / "pdf"
    work_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    return run_root, work_dir, pdf_dir


def _normalize_path(path: str | Path) -> str:
    return str(Path(path).resolve()).lower()


def _find_document_by_path(target_path: str | Path):
    wanted = _normalize_path(target_path)
    try:
        for doc in C.acad.Documents:
            try:
                if _normalize_path(doc.FullName) == wanted:
                    return doc
            except Exception:
                continue
    except Exception:
        return None
    return None


def _activate_document_by_path(target_path: str | Path, retries: int = 8, delay: float = 0.5) -> bool:
    wanted = _normalize_path(target_path)
    for _ in range(retries):
        doc = _find_document_by_path(target_path)
        if doc is None:
            time.sleep(delay)
            continue
        try:
            doc.Activate()
        except Exception:
            time.sleep(delay)
            continue
        time.sleep(delay)
        try:
            active = C.raw_doc
            if active and _normalize_path(active.FullName) == wanted:
                return True
        except Exception:
            pass
        time.sleep(delay)
    return False


def _close_document_by_path(target_path: str | Path, save_changes: bool = False) -> bool:
    doc = _find_document_by_path(target_path)
    if doc is None:
        return True
    try:
        doc.Close(bool(save_changes))
        return True
    except Exception as exc:
        sys_logger.warning(f"关闭工作 DWG 失败: {exc}")
        return False


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
        raise FileNotFoun
...[truncated]...
