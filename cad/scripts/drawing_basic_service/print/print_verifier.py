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


def _read_pdf_page_sizes_mm(pdf_path: Path) -> list[tuple[float, float]] | None:
    try:
        reader = PdfReader(str(pdf_path), strict=False)
        if not reader.pages:
            return None
        sizes = []
        for page in reader.pages:
            width_mm = float(page.mediabox.width) * MM_PER_POINT
            height_mm = float(page.mediabox.height) * MM_PER_POINT
            sizes.append((min(width_mm, height_mm), max(width_mm, height_mm)))
        return sizes
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
    multi_page_files: list[dict[str, Any]] = []
    standard_flags = Counter()

    for item in existing_paths:
        job = job_by_output.get(str(Path(item)))
        if job is None:
            continue
        standard_flags[int(_job_value(job, "standard_flag", 0))] += 1
        expected = _parse_media_size_mm(str(_job_value(job, "media", "")))
        actual_pages = _read_pdf_page_sizes_mm(Path(item))
        if expected is None or actual_pages is None:
            unparsed.append(
                {
                    "output_path": item,
                    "media": _job_value(job, "media", ""),
                    "expected_mm": expected,
                    "actual_pages_mm": actual_pages,
                    "standard_flag": int(_job_value(job, "standard_flag", 0)),
                }
            )
            continue

        if len(actual_pages) > 1:
            multi_page_files.append(
                {
                    "output_path": item,
                    "page_count": len(actual_pages),
                    "standard_flag": int(_job_value(job, "standard_flag", 0)),
                }
            )

        expected_short, expected_long = min(expected), max(expected)
        page_ok = True
        for page_no, (actual_short, actual_long) in enumerate(actual_pages, start=1):
            checked += 1
            delta_short = abs(actual_short - expected_short)
            delta_long = abs(actual_long - expected_long)
            if delta_short <= size_tol_mm and delta_long <= size_tol_mm:
                matched += 1
                continue
            page_ok = False
            mismatches.append(
                {
                    "output_path": item,
                    "page_no": page_no,
                    "page_count": len(actual_pages),
                    "media": _job_value(job, "media", ""),
                    "expected_mm": [round(expected_short, 2), round(expected_long, 2)],
                    "actual_mm": [round(actual_short, 2), round(actual_long, 2)],
                    "delta_mm": [round(delta_short, 2), round(delta_long, 2)],
                    "paper_code": _job_value(job, "paper_code", ""),
                    "ratio": _job_value(job, "ratio", ""),
                    "standard_flag": int(_job_value(job, "standard_flag", 0)),
                }
            )

        if page_ok:
            continue

    return {
        "page_size_checked_count": checked,
        "page_size_match_count": matched,
        "page_size_mismatch_count": len(mismatches),
        "page_size_unparsed_count": len(unparsed),
        "size_tolerance_mm": float(size_tol_mm),
        "standard_flag_counts": {str(k): v for k, v in sorted(standard_flags.items())},
        "multi_page_file_count": len(multi_page_files),
        "multi_page_files": multi_page_files,
        "mismatches": mismatches,
        "unparsed": unparsed,
    }


def verify_generated_pdfs(output_paths: list[str], jobs: list[Any] | None = None, size_tol_mm: float = 1.0) -> dict:
    existing = []
    missing = []
    zero_size = []
    for item in output_paths:
        path = Path(item)
        if not path.exists():
            missing.append(str(path))
            continue
        if path.stat().st_size <= 0:
            zero_size.append(str(path))
            continue
        existing.append(str(path))

    result = {
        "expected_count": len(output_paths),
        "existing_count": len(existing),
        "missing_count": len(missing),
        "zero_size_count": len(zero_size),
        "existing": existing,
        "missing": missing,
        "zero_size": zero_size,
    }

    if jobs:
        result["page_verification"] = _verify_page_sizes(existing, jobs, size_tol_mm=size_tol_mm)

    return result
