# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


INVALID_FILENAME_CHARS_RE = re.compile(r'[\\/:*?"<>|]+')
SPACE_RE = re.compile(r"\s+")
PAGE_SUFFIX_RE = re.compile(r"-(?P<layout>.+)-(?P<seq>\d+)\.pdf$", re.IGNORECASE)


def _clean_name_part(value: Any) -> str:
    text = str(value or "").strip()
    text = INVALID_FILENAME_CHARS_RE.sub("_", text)
    text = SPACE_RE.sub(" ", text).strip()
    return text


def _build_default_pdf_name(
    *,
    sequence_label: str,
    original_stem: str,
    drawing_title: str,
    drawing_no: str,
    project_name: str = "",
    subproject_name: str = "",
    drawing_no_prefix: str = "",
) -> str:
    number_text = _clean_name_part(drawing_no)
    number_prefix = _clean_name_part(drawing_no_prefix)
    if number_text and number_prefix:
        number_text = f"{number_prefix}{number_text}"

    parts = [
        _clean_name_part(project_name),
        _clean_name_part(subproject_name),
        _clean_name_part(drawing_title),
        number_text,
    ]
    joined = "-".join(part for part in parts if part)
    label = joined or _clean_name_part(original_stem) or "unnamed"
    prefix = _clean_name_part(sequence_label) or "00"
    return f"{prefix}-{label}"


def _unique_target_path(output_dir: Path, base_name: str, suffix: str) -> Path:
    base_name = _clean_name_part(base_name) or "unnamed"
    candidate = output_dir / f"{base_name}{suffix}"
    if not candidate.exists():
        return candidate
    index = 2
    while True:
        candidate = output_dir / f"{base_name}_{index:02d}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def _parse_page_from_pdf_name(pdf_path: Path) -> tuple[str, str] | None:
    match = PAGE_SUFFIX_RE.search(pdf_path.name)
    if not match:
        return None
    return str(match.group("layout")), f"{int(match.group('seq')):02d}"


def _build_row_index(print_info: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], dict[str, Any]]]:
    by_handle: dict[str, dict[str, Any]] = {}
    by_page: dict[tuple[str, str], dict[str, Any]] = {}
    for row in (print_info.get("print_info_dict", {}) or {}).values():
        handle = str(row.get("print_handle", "")).strip()
        if handle:
            by_handle[handle] = row
        layout_name = str(row.get("layout_name", "")).strip()
        sequence_key = str(row.get("sequence_key", "")).strip()
        if layout_name and sequence_key:
            by_page[(layout_name, sequence_key)] = row
    return by_handle, by_page


def copy_named_pdfs_from_print_info(
    *,
    print_info: dict[str, Any],
    output_dir: Path,
    pdf_paths: list[str] | None = None,
    selected_handles: list[str] | None = None,
    pdf_dir: Path | None = None,
    project_name: str = "",
    subproject_name: str = "",
    drawing_no_prefix: str = "",
    reset_output_dir: bool = True,
) -> dict[str, Any]:
    if reset_output_dir and output_dir.exists():
        shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    by_handle, by_page = _build_row_index(print_info)

    source_paths: list[Path] = []
    if pdf_paths:
        source_paths = [Path(item) for item in pdf_paths if str(item).strip()]
    elif pdf_dir:
        source_paths = sorted(path for path in pdf_dir.glob("*.pdf") if path.is_file())

    copied: list[str] = []
    named_items: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    handles = [str(item or "").strip() for item in (selected_handles or [])]

    total_rows = max(len(source_paths), len(print_info.get("print_info_dict", {}) or {}), 1)
    seq_width = max(2, len(str(total_rows)))

    for index, source_path in enumerate(source_paths):
        if not source_path.exists():
            unresolved.append(
                {
                    "source_pdf": str(source_path),
                    "reason": "missing_source_pdf",
                }
            )
            continue

        row = None
        source_handle = handles[index] if index < len(handles) else ""
        if source_handle:
            row = by_handle.get(source_handle)
        if row is None:
            page_key = _parse_page_from_pdf_name(source_path)
            if page_key is not None:
                row = by_page.get(page_key)

        if row is None:
            unresolved.append(
                {
                    "source_pdf": str(source_path),
                    "source_handle": source_handle,
                    "reason": "missing_print_info_row",
                }
            )
            continue

        effective_project_name = _clean_name_part(project_name or row.get("project_name", ""))
        effective_subproject_name = _clean_name_part(subproject_name or row.get("subproject_name", ""))
        drawing_title = _clean_name_part(row.get("drawing_title", ""))
        drawing_no = _clean_name_part(row.get("drawing_no", ""))
        sequence_label = f"{int(row.get('sequence_no', index + 1)):0{seq_width}d}"
        target_base_name = _build_default_pdf_name(
            sequence_label=sequence_label,
            original_stem=source_path.stem,
            drawing_title=drawing_title,
            drawing_no=drawing_no,
            project_name=effective_project_name,
            subproject_name=effective_subproject_name,
            drawing_no_prefix=drawing_no_prefix,
        )
        target_path = _unique_target_path(output_dir, target_base_name, source_path.suffix)
        shutil.copy2(source_path, target_path)

        copied.append(str(target_path))
        named_items.append(
            {
                "source_pdf": str(source_path),
                "target_pdf": str(target_path),
                "print_handle": str(row.get("print_handle", "")),
                "page_key": str(row.get("page_key", "")),
                "sequence_no": int(row.get("sequence_no", 0) or 0),
                "project_name": effective_project_name,
                "subproject_name": effective_subproject_name,
                "drawing_title": drawing_title,
                "drawing_no": drawing_no,
                "drawing_no_prefix": _clean_name_part(drawing_no_prefix),
                "naming_rule": "default_sequence_project_subproject_title_prefixed_no",
            }
        )

    return {
        "named_pdf_dir": str(output_dir),
        "named_pdf_count": len(copied),
        "named_pdf_paths": copied,
        "named_pdf_items": named_items,
        "named_pdf_unresolved": unresolved,
    }


def copy_named_pdfs_from_print_info_json(
    *,
    print_info_json: Path,
    pdf_dir: Path,
    output_dir: Path | None = None,
    project_name: str = "",
    subproject_name: str = "",
    drawing_no_prefix: str = "",
    reset_output_dir: bool = True,
) -> dict[str, Any]:
    print_info = json.loads(print_info_json.read_text(encoding="utf-8"))
    target_dir = output_dir or (pdf_dir / "named")
    return copy_named_pdfs_from_print_info(
        print_info=print_info,
        output_dir=target_dir,
        pdf_dir=pdf_dir,
        project_name=project_name,
        subproject_name=subproject_name,
        drawing_no_prefix=drawing_no_prefix,
        reset_output_dir=reset_output_dir,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-info-json", required=True, help="print_info_analysis.json path")
    parser.add_argument("--pdf-dir", required=True, help="directory containing copied pdf outputs")
    parser.add_argument("--output-dir", default="", help="directory for named copies; default: <pdf-dir>/named")
    parser.add_argument("--project-name", default="", help="override project name")
    parser.add_argument("--subproject-name", default="", help="override subproject name")
    parser.add_argument("--drawing-no-prefix", default="", help="prefix added before drawing_no, e.g. JS-")
    parser.add_argument("--keep-existing", action="store_true", help="do not reset output dir before copying")
    args = parser.parse_args()

    result = copy_named_pdfs_from_print_info_json(
        print_info_json=Path(args.print_info_json),
        pdf_dir=Path(args.pdf_dir),
        output_dir=Path(args.output_dir) if args.output_dir else None,
        project_name=args.project_name,
        subproject_name=args.subproject_name,
        drawing_no_prefix=args.drawing_no_prefix,
        reset_output_dir=not args.keep_existing,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
