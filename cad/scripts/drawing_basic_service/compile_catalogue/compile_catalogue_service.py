#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile catalogue service for DWG drawing sets."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence
import json
import math
import re
import shutil
import sys
import time

import pythoncom
import win32com.client


current = Path(__file__).resolve()
MODULE_DIR = current.parent
while current.name != "cad":
    if current.parent == current:
        raise RuntimeError("找不到根目录 cad")
    current = current.parent
CAD_DIR = current
if str(CAD_DIR) not in sys.path:
    sys.path.insert(0, str(CAD_DIR))
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))
DRAWING_BASIC_SERVICE_DIR = MODULE_DIR.parent
ILLUSTRATION_LABEL_DIR = DRAWING_BASIC_SERVICE_DIR / "illustration_label"
PRINT_DIR = DRAWING_BASIC_SERVICE_DIR / "print"
for extra_path in (DRAWING_BASIC_SERVICE_DIR, ILLUSTRATION_LABEL_DIR, PRINT_DIR):
    if str(extra_path) not in sys.path:
        sys.path.insert(0, str(extra_path))

from system.licad import C
from system.CAD_core import cad_zt_oneb, open_file, save_file
from system.CAD_coordination import wait_quiescent
from system.CAD_selection import get_attr, select_entities_in_window
from system.common_logger import sys_logger
from system.runtime_guard_bridge import RuntimeGuardTriggered, assert_runtime_guard_ok, render_guard_error
from library.cad_annotation import write_cad_text
from scripts.drawing_basic_service.illustration_label.illustration_block_service import prepare_cad_runtime
from scripts.drawing_basic_service.illustration_label.illustration_frame_service import apply_illustration_labels
from scripts.drawing_basic_service.print.print_policy import (
    PRINT_MODE_ADAPTIVE,
    PRINT_MODE_BASIC,
    build_print_plan,
    normalize_print_mode,
)
from scripts.drawing_basic_service.print.print_info_analysis import (
    TEXT_OBJECTS,
    TextRecord,
    _activate_document_by_path,
    _choose_corner_block,
    _choose_inner_frame,
    _classify_text_record_dicts,
    _collect_rectangles_by_owner,
    _extract_guide_rectangles,
    _filter_jobs_by_requested_handles,
    _make_text_record,
    _resolve_by_fallback_rules,
    _resolve_by_guide_rectangles,
    _resolve_by_named_layers,
    _resolve_owner_btr_name,
    _select_entities_in_bbox,
    _text_record_to_dict,
    analyze_print_info_jobs,
    collect_space_block_snapshots,
    select_texts_in_bbox,
)


DIRECTORY_TEMPLATE = MODULE_DIR / "directory_template" / "目录模板1.dwg"
USER_DIRECTORY = MODULE_DIR / "user_directory"
DEFAULT_PREFIX = "JS-"
DEFAULT_MATCH_MODE = PRINT_MODE_BASIC
DEFAULT_CATALOG_NAME = "图纸目录"
DEFAULT_TITLE = "无图纸名称"
DEFAULT_REMARK = ""
DEFAULT_TEXT_STYLE = "HT"
DEFAULT_TEXT_HEIGHT = 196.0
DEFAULT_LINE_SPACING_RATIO = 0.25
PORTRAIT_ROTATION = -math.pi / 2.0
INVALID_FILENAME_CHARS_RE = re.compile(r'[\\/:*?"<>|]+')

ROW_HEIGHT = 800.0
ROW_SEGMENT_WIDTHS = (1000.0, 11000.0, 2400.0, 1500.0, 2100.0)
ROW_SEGMENT_KEYS = ("sequence_no", "drawing_title", "drawing_no", "paper_code", "remark")
ROW_STARTS = (
    ("row_1", (208050.58918416, -256788.99090111, 226050.58918416, -255988.99090111), 27),
    ("row_2", (229050.58918416, -251188.99090111, 247050.58918416, -250388.99090111), 34),
    ("row_3", (277786.45312686, -251188.99090111, 295786.45312686, -250388.99090111), 34),
    ("row_4", (300786.45312686, -251188.99090111, 318786.45312686, -250388.99090111), 34),
)


@dataclass
class TitleStyle:
    style: str
    height: float


@dataclass
class PrintAreaResolved:
    sequence_no: int
    layout_name: str
    owner_btr: str
    print_handle: str
    paper_code: str
    graphic_orientation: str
    print_bbox: tuple[float, float, float, float]
    inner_frame_bbox: tuple[float, float, float, float] | None
    graphic_info_area_bbox: tuple[float, float, float, float] | None
    red_border_area: tuple[float, float, float, float] | None
    green_border_area: tuple[float, float, float, float] | None
    drawing_title: str
    drawing_no: str
    drawing_title_source: str
    drawing_no_source: str
    drawing_title_records: list[dict[str, Any]]
    drawing_no_records: list[dict[str, Any]]
    graphic_info_text_records: list[dict[str, Any]]
    classified_text_records: list[dict[str, Any]]
    title_block_handle: str
    title_block_name: str
    title_block_bbox: tuple[float, float, float, float] | None
    title_block_kind: str
    title_style: dict[str, Any]
    number_style: dict[str, Any]


@dataclass
class CatalogueEntry:
    sequence_no: str
    drawing_title: str
    drawing_no: str
    paper_code: str
    remark: str
    source_print_handle: str
    kind: str


def _guard_checkpoint(checkpoint: str) -> None:
    decision = assert_runtime_guard_ok(checkpoint)
    sys_logger.info(
        "[compile_catalogue][runtime_guard] checkpoint=%s status=%s action=%s",
        checkpoint,
        decision.status,
        decision.recommended_action,
    )


def _sanitize_filename_part(value: str) -> str:
    text = INVALID_FILENAME_CHARS_RE.sub("_", str(value or "").strip())
    text = re.sub(r"\s+", "_", text)
    return text.strip("_")


def _now_timestamp_text() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def _scope_suffix(
    *,
    include_model: bool,
    include_layouts: bool,
    only_layouts: Sequence[str] | None,
    requested_handles: Sequence[str] | None,
) -> str:
    handles = [str(item).strip() for item in (requested_handles or []) if str(item).strip()]
    layouts = [str(item).strip() for item in (only_layouts or []) if str(item).strip()]
    if handles:
        return "selected"
    if include_model and not include_layouts:
        return "model"
    if include_layouts and not include_model:
        if len(layouts) == 1:
            return f"layout_{_sanitize_filename_part(layouts[0])}"
        return "layouts"
    if layouts:
        if len(layouts) == 1:
            return f"mixed_{_sanitize_filename_part(layouts[0])}"
        return "mixed_layouts"
    return ""


def _point_variant(point: Sequence[float]) -> Any:
    values = [float(v) for v in point]
    if len(values) == 2:
        values.append(0.0)
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, values[:3])


def _dispatch_variant(objects: Sequence[Any]) -> Any:
    return win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH,
        tuple(objects),
    )


def _bbox_xy(entity: Any) -> tuple[float, float, float, float] | None:
    try:
        ll, ur = entity.GetBoundingBox()
        min_x = min(float(ll[0]), float(ur[0]))
        min_y = min(float(ll[1]), float(ur[1]))
        max_x = max(float(ll[0]), float(ur[0]))
        max_y = max(float(ll[1]), float(ur[1]))
        return (min_x, min_y, max_x, max_y)
    except Exception:
        return None


def _bbox_union(bboxes: Iterable[tuple[float, float, float, float] | None]) -> tuple[float, float, float, float] | None:
    items = [bbox for bbox in bboxes if bbox is not None]
    if not items:
        return None
    return (
        min(item[0] for item in items),
        min(item[1] for item in items),
        max(item[2] for item in items),
        max(item[3] for item in items),
    )


def _bbox_contains(
    outer: tuple[float, float, float, float],
    inner: tuple[float, float, float, float],
    *,
    tol: float = 1.0,
) -> bool:
    return (
        outer[0] <= inner[0] + tol
        and outer[1] <= inner[1] + tol
        and outer[2] >= inner[2] - tol
        and outer[3] >= inner[3] - tol
    )


def _bbox_center(bbox: tuple[float, float, float, float]) -> tuple[float, float, float]:
    return ((bbox[0] + bbox[2]) / 2.0, (bbox[1] + bbox[3]) / 2.0, 0.0)


def _bbox_size(bbox: tuple[float, float, float, float]) -> tuple[float, float]:
    return (max(bbox[2] - bbox[0], 0.0), max(bbox[3] - bbox[1], 0.0))


def _bbox_inset_ratio(bbox: tuple[float, float, float, float], ratio: float) -> tuple[float, float, float, float]:
    width, height = _bbox_size(bbox)
    keep_ratio = max(min(float(ratio), 1.0), 0.05)
    dx = width * (1.0 - keep_ratio) / 2.0
    dy = height * (1.0 - keep_ratio) / 2.0
    return (bbox[0] + dx, bbox[1] + dy, bbox[2] - dx, bbox[3] - dy)


def _fallback_red_green_areas(
    graphic_info_area_bbox: tuple[float, float, float, float],
    orientation: str,
) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float]]:
    x1, y1, x2, y2 = graphic_info_area_bbox
    if orientation == "portrait":
        mid_x = (x1 + x2) / 2.0
        red = (x1, y1, mid_x, y2)
        green = (mid_x, y1, x2, y2)
    else:
        mid_y = (y1 + y2) / 2.0
        red = (x1, mid_y, x2, y2)
        green = (x1, y1, x2, mid_y)
    return (_bbox_inset_ratio(red, 0.8), _bbox_inset_ratio(green, 0.8))


def _transform_xy_for_orientation(x: float, y: float, orientation: str) -> tuple[float, float]:
    if orientation == "portrait":
        return (y, -x)
    return (x, y)


def _reading_sort_key_for_record(record: TextRecord, orientation: str) -> tuple[float, float]:
    tx, ty = _transform_xy_for_orientation(record.bbox[0], record.bbox[1], orientation)
    return (-ty, tx)


def _sort_records_for_orientation(records: Sequence[TextRecord], orientation: str) -> list[TextRecord]:
    return sorted(records, key=lambda item: _reading_sort_key_for_record(item, orientation))


def _sort_entities_for_orientation(entities: Sequence[Any], orientation: str) -> list[Any]:
    def _key(ent: Any) -> tuple[float, float]:
        bbox = _bbox_xy(ent) or (0.0, 0.0, 0.0, 0.0)
        tx, ty = _transform_xy_for_orientation(bbox[0], bbox[1], orientation)
        return (-ty, tx)

    return sorted(entities, key=_key)


def _format_index(number: int, *, width: int = 2) -> str:
    return f"{int(number):0{width}d}"


def _strip_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\\P", " ").replace("\r", " ").replace("\n", " ").strip()
    text = re.sub(r"\^C[^\u4e00-\u9fff]*", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _safe_text_height(ent: Any) -> float:
    for attr_name in ("Height", "TextHeight", "图名高度"):
        try:
            value = get_attr(ent, attr_name, None)
            if value is not None:
                height = float(value)
                if height > 0:
                    return height
        except Exception:
            continue
    bbox = _bbox_xy(ent)
    if bbox is None:
        return 350.0
    return max(bbox[3] - bbox[1], 350.0)


def _safe_text_style(ent: Any) -> str:
    for attr_name in ("StyleName", "图名样式"):
        try:
            value = get_attr(ent, attr_name, None)
            if value:
                return str(value)
        except Exception:
            continue
    return "Standard"


def _get_entity_by_handle(handle: str) -> Any | None:
    if not handle:
        return None
    try:
        return C.raw_doc.HandleToObject(str(handle))
    except Exception:
        return None


def _derive_style_from_text_records(records: Sequence[TextRecord]) -> TitleStyle:
    for record in records:
        ent = _get_entity_by_handle(record.handle)
        if ent is None:
            continue
        return TitleStyle(style=_safe_text_style(ent), height=_safe_text_height(ent))
    if records:
        return TitleStyle(style="Standard", height=max(records[0].height, 250.0))
    return TitleStyle(style="Standard", height=350.0)


def _derive_style_from_tdb_drawing_names(entities: Sequence[Any]) -> TitleStyle:
    if not entities:
        return TitleStyle(style="Standard", height=350.0)
    style = "Standard"
    height = 350.0
    for ent in entities:
        style = _safe_text_style(ent) or style
        value = _safe_text_height(ent)
        if value > 0:
            height = value
            break
    return TitleStyle(style=style, height=height)


def _combine_texts_by_orientation(records: Sequence[TextRecord], orientation: str, *, separator: str = "、") -> str:
    ordered = _sort_records_for_orientation(records, orientation)
    return separator.join(_strip_text(item.text) for item in ordered if _strip_text(item.text))


def _select_tdb_drawing_names(
    owner_btr_name: str,
    print_bbox: tuple[float, float, float, float],
) -> list[Any]:
    entities = _select_entities_in_bbox(owner_btr_name, print_bbox)
    rows = [ent for ent in entities if str(get_attr(ent, "ObjectName", getattr(ent, "ObjectName", ""))) == "TDbDrawingName"]
    orientation = "portrait" if (print_bbox[3] - print_bbox[1]) > (print_bbox[2] - print_bbox[0]) else "landscape"
    return _sort_entities_for_orientation(rows, orientation)


def _group_text_records_into_lines(records: Sequence[TextRecord], orientation: str) -> list[list[TextRecord]]:
    ordered = _sort_records_for_orientation(records, orientation)
    lines: list[list[TextRecord]] = []
    current: list[TextRecord] = []
    current_y: float | None = None
    current_h = 0.0

    for record in ordered:
        _x1, y1 = _transform_xy_for_orientation(record.bbox[0], record.bbox[1], orientation)
        _x2, y2 = _transform_xy_for_orientation(record.bbox[2], record.bbox[3], orientation)
        top = max(y1, y2)
        height = max(abs(y2 - y1), 1.0)
        if not current:
            current = [record]
            current_y = top
            current_h = height
            continue
        threshold = max(current_h, height) * 0.5
        if current_y is not None and abs(top - current_y) <= threshold:
            current.append(record)
            current_h = max(current_h, height)
        else:
            lines.append(_sort_records_for_orientation(current, orientation))
            current = [record]
            current_y = top
            current_h = height
    if current:
        lines.append(_sort_records_for_orientation(current, orientation))
    return lines


def _resolve_top_text_line_title(
    owner_btr_name: str,
    print_bbox: tuple[float, float, float, float],
    orientation: str,
) -> tuple[str, list[TextRecord], TitleStyle] | None:
    raw_entities = _select_entities_in_bbox(owner_btr_name, print_bbox)
    text_records = [_make_text_record(ent) for ent in raw_entities]
    text_records = [record for record in text_records if record is not None]
    if len(text_records) < 3:
        return None

    all_entity_count = max(len(raw_entities), 1)
    if len(text_records) / all_entity_count < 0.3:
        return None

    lines = _group_text_records_into_lines(text_records, orientation)
    if len(lines) < 2:
        return None

    top_line = lines[0]
    top_height = max(max(item.height, 1.0) for item in top_line)
    other_heights = [max(item.height, 1.0) for line in lines[1:] for item in line]
    other_heights.sort()
    median_other = other_heights[len(other_heights) // 2]
    if top_height < median_other * 1.15:
        return None

    title = _combine_texts_by_orientation(top_line, orientation, separator="")
    if not title:
        return None
    return title, list(top_line), _derive_style_from_text_records(top_line)


def _move_entity_by_anchor(entity: Any, target_bbox: tuple[float, float, float, float]) -> bool:
    bbox = _bbox_xy(entity)
    if bbox is None:
        return False
    source = _bbox_center(bbox)
    target = _bbox_center(target_bbox)
    try:
        entity.Move(_point_variant(source), _point_variant(target))
        return True
    except Exception:
        return False


def _delete_entity(entity: Any) -> None:
    try:
        entity.Delete()
    except Exception:
        pass


def _entities_fit_in_bbox(
    entities: Sequence[Any],
    target_bbox: tuple[float, float, float, float],
    *,
    tol: float = 1.0,
) -> bool:
    union = _bbox_union(_bbox_xy(item) for item in entities)
    if union is None:
        return False
    return _bbox_contains(target_bbox, union, tol=tol)


def _center_entities_in_bbox(entities: Sequence[Any], target_bbox: tuple[float, float, float, float]) -> None:
    union = _bbox_union(_bbox_xy(item) for item in entities)
    if union is None:
        return
    source = _bbox_center(union)
    target = _bbox_center(target_bbox)
    for ent in entities:
        try:
            ent.Move(_point_variant(source), _point_variant(target))
        except Exception:
            continue


def _estimate_visual_units(text: str) -> float:
    units = 0.0
    for ch in text:
        if ch.isspace():
            units += 0.4
        elif ord(ch) < 128:
            units += 0.65
        else:
            units += 1.0
    return max(units, 1.0)


def _wrap_text_by_width(text: str, bbox: tuple[float, float, float, float], height: float) -> list[str]:
    compact = _strip_text(text)
    if not compact:
        return [""]
    width, _ = _bbox_size(bbox)
    max_units = max(width / max(height * 0.9, 1.0), 3.0)
    if _estimate_visual_units(compact) <= max_units:
        return [compact]

    tokens: list[str] = []
    current = ""
    delimiters = {"、", ",", "，", ";", "；", " "}
    for ch in compact:
        current += ch
        if ch in delimiters:
            tokens.append(current)
            current = ""
    if current:
        tokens.append(current)
    if not tokens:
        tokens = list(compact)

    lines: list[str] = []
    line = ""
    for token in tokens:
        candidate = f"{line}{token}"
        if line and _estimate_visual_units(candidate) > max_units:
            lines.append(line.strip())
            line = token
        else:
            line = candidate
    if line:
        lines.append(line.strip())

    normalized: list[str] = []
    for item in lines:
        if _estimate_visual_units(item) <= max_units:
            normalized.append(item)
            continue
        chunk = ""
        for ch in item:
            if chunk and _estimate_visual_units(chunk + ch) > max_units:
                normalized.append(chunk)
                chunk = ch
            else:
                chunk += ch
        if chunk:
            normalized.append(chunk)
    return [item for item in normalized if item] or [compact]


def _write_centered_text(
    text: str,
    bbox: tuple[float, float, float, float],
    *,
    height: float,
    style: str,
    rotation: float,
) -> Any | None:
    ent = write_cad_text(
        text_content=text,
        insertion_point=_bbox_center(bbox),
        height=height,
        rotation=rotation,
        style=style,
    )
    if ent is None:
        return None
    _move_entity_by_anchor(ent, bbox)
    return ent


def _write_best_fit_text(
    text: str,
    bbox: tuple[float, float, float, float],
    *,
    style: str,
    base_height: float,
    rotation: float = 0.0,
    allow_wrap: bool = False,
    min_height: float = 40.0,
) -> list[str]:
    content = _strip_text(text)
    if not content:
        return []

    scale = 1.0
    while base_height * scale >= min_height:
        current_height = base_height * scale
        lines = _wrap_text_by_width(content, bbox, current_height) if allow_wrap else [content]
        entities: list[Any] = []
        line_spacing = current_height * DEFAULT_LINE_SPACING_RATIO
        total_height = len(lines) * current_height + max(len(lines) - 1, 0) * line_spacing
        _center_x, center_y, _center_z = _bbox_center(bbox)
        top_center_y = center_y + total_height / 2.0 - current_height / 2.0

        for idx, line in enumerate(lines):
            line_center_y = top_center_y - idx * (current_height + line_spacing)
            line_bbox = (
                bbox[0],
                line_center_y - current_height / 2.0,
                bbox[2],
                line_center_y + current_height / 2.0,
            )
            ent = _write_centered_text(
                line,
                line_bbox,
                height=current_height,
                style=style,
                rotation=rotation,
            )
            if ent is None:
                entities = []
                break
            entities.append(ent)

        if entities:
            _center_entities_in_bbox(entities, bbox)
            wait_quiescent(min_quiet=0.1, timeout=3.0)
            if _entities_fit_in_bbox(entities, bbox, tol=1.0):
                return [str(get_attr(item, "Handle", getattr(item, "Handle", "")) or "") for item in entities]

        for ent in entities:
            _delete_entity(ent)
        scale *= 0.8

    return []


def _paper_code_for_job(job: dict[str, Any]) -> str:
    for key in ("paper_code", "media"):
        value = _strip_text(job.get(key, ""))
        if value:
            return value
    return "A2"


def _resolve_catalogue_drawing_no(raw_no: str, sequence_no: int, prefix: str) -> str:
    core = _strip_text(raw_no)
    if not core:
        core = _format_index(sequence_no)
    normalized_prefix = str(prefix or "").strip()
    if not normalized_prefix:
        return core
    if core.upper().startswith(normalized_prefix.upper()):
        return core
    if "-" in core and any(ch.isalpha() for ch in core):
        return core
    return f"{normalized_prefix}{core}"


def _clear_text_entities_in_bbox(bbox: tuple[float, float, float, float]) -> list[str]:
    handles: list[str] = []
    try:
        entities = select_entities_in_window(
            bbox[0],
            bbox[1],
            bbox[2],
            bbox[3],
            ty=1.0,
            select_mode="_W",
        ) or []
    except Exception:
        entities = []
    for ent in entities:
        obj_name = str(get_attr(ent, "ObjectName", getattr(ent, "ObjectName", "")))
        if obj_name not in TEXT_OBJECTS and obj_name not in {"TDbDrawingName", "AcDbBlockReference"}:
            continue
        handle = str(get_attr(ent, "Handle", getattr(ent, "Handle", "")) or "")
        _delete_entity(ent)
        if handle:
            handles.append(handle)
    return handles


def _catalogue_row_bboxes() -> list[tuple[str, tuple[float, float, float, float]]]:
    rows: list[tuple[str, tuple[float, float, float, float]]] = []
    for band_name, first_row_bbox, count in ROW_STARTS:
        x1, y1, x2, y2 = first_row_bbox
        for idx in range(count):
            offset = idx * ROW_HEIGHT
            row_bbox = (x1, y1 - offset, x2, y2 - offset)
            rows.append((f"{band_name}:{idx + 1:02d}", row_bbox))
    return rows


def _row_segment_bboxes(row_bbox: tuple[float, float, float, float]) -> dict[str, tuple[float, float, float, float]]:
    x1, y1, _x2, y2 = row_bbox
    cursor = x1
    out: dict[str, tuple[float, float, float, float]] = {}
    for key, width in zip(ROW_SEGMENT_KEYS, ROW_SEGMENT_WIDTHS):
        out[key] = (cursor, y1, cursor + width, y2)
        cursor += width
    return out


def _second_catalogue_page_bbox() -> tuple[float, float, float, float]:
    rows = [item for name, item in _catalogue_row_bboxes() if name.startswith("row_3:") or name.startswith("row_4:")]
    bbox = _bbox_union(rows)
    if bbox is None:
        raise RuntimeError("无法计算第二目录区域范围")
    return bbox


def _collection_count(collection: Any) -> int:
    try:
        return int(getattr(collection, "Count", 0) or 0)
    except Exception:
        return 0


def _collection_item(collection: Any, index: int) -> Any | None:
    try:
        return collection.Item(index)
    except Exception:
        return None


def _iter_collection_entities(collection: Any) -> Iterable[Any]:
    total = _collection_count(collection)
    for index in range(total):
        entity = _collection_item(collection, index)
        if entity is not None:
            yield entity


def _resolve_owner_container(doc: Any, owner_btr: str) -> Any:
    normalized = str(owner_btr or "").strip()
    if not normalized or normalized == "*MODEL_SPACE":
        return doc.ModelSpace
    if normalized == "*PAPER_SPACE":
        return doc.PaperSpace
    return doc.Blocks.Item(normalized)


def _collect_entities_in_owner_bbox(
    owner: Any,
    bbox: tuple[float, float, float, float],
    *,
    tol: float = 5.0,
) -> list[Any]:
    entities: list[Any] = []
    for entity in _iter_collection_entities(owner):
        entity_bbox = _bbox_xy(entity)
        if entity_bbox is None:
            continue
        if _bbox_contains(bbox, entity_bbox, tol=tol):
            entities.append(entity)
    return entities


def _delete_entities_in_owner_bbox(
    owner: Any,
    bbox: tuple[float, float, float, float],
    *,
    tol: float = 5.0,
) -> list[str]:
    deleted_handles: list[str] = []
    for entity in _collect_entities_in_owner_bbox(owner, bbox, tol=tol):
        handle = str(get_attr(entity, "Handle", getattr(entity, "Handle", "")) or "")
        _delete_entity(entity)
        if handle:
            deleted_handles.append(handle)
    return deleted_handles


def _normalize_com_object_list(raw_value: Any) -> list[Any]:
    if raw_value is None:
        return []
    if isinstance(raw_value, (list, tuple)):
        return [item for item in raw_value if item is not None]
    try:
        return [item for item in raw_value if item is not None]
    except Exception:
        return [raw_value]


def _move_entities_by_delta(entities: Sequence[Any], dx: float, dy: float) -> list[str]:
    moved_handles: list[str] = []
    from_point = _point_variant((0.0, 0.0, 0.0))
    to_point = _point_variant((float(dx), float(dy), 0.0))
    for entity in entities:
        try:
            entity.Move(from_point, to_point)
        except Exception:
            continue
        handle = str(get_attr(entity, "Handle", getattr(entity, "Handle", "")) or "")
        if handle:
            moved_handles.append(handle)
    return moved_handles


def _collect_catalogue_page_jobs(catalogue_path: Path) -> list[dict[str, Any]]:
    if not open_file(str(catalogue_path)):
        raise RuntimeError(f"打开目录 DWG 失败: {catalogue_path}")
    if not _activate_document_by_path(catalogue_path):
        raise RuntimeError(f"未能激活目录 DWG: {catalogue_path}")
    wait_quiescent(min_quiet=0.6, timeout=10.0)
    plan = build_print_plan(
        str(catalogue_path),
        str(USER_DIRECTORY / "_compile_plan_tmp"),
        mode=PRINT_MODE_BASIC,
        include_model=True,
        include_layouts=False,
    )
    jobs = [job.__dict__.copy() for job in plan.jobs_by_space.get("model", [])]
    jobs.sort(key=lambda item: (float(item["lower_left"][0]), float(item["lower_left"][1])))
    return jobs


def _trim_catalogue_pages(
    catalogue_path: Path,
    *,
    use_second_page: bool,
) -> dict[str, Any]:
    jobs = _collect_catalogue_page_jobs(catalogue_path)
    deleted_handles: list[str] = []
    deleted_page: dict[str, Any] | None = None

    if not use_second_page and len(jobs) > 1:
        page_to_remove = jobs[-1]
        owner = _resolve_owner_container(C.raw_doc, str(page_to_remove.get("owner_btr", "*MODEL_SPACE")))
        bbox = tuple(page_to_remove["lower_left"] + page_to_remove["upper_right"])
        deleted_handles = _delete_entities_in_owner_bbox(owner, bbox, tol=10.0)
        deleted_page = {
            "handle": str(page_to_remove.get("handle", "")),
            "owner_btr": str(page_to_remove.get("owner_btr", "*MODEL_SPACE")),
            "bbox": bbox,
            "deleted_handle_count": len(deleted_handles),
        }
        save_file()
        wait_quiescent(min_quiet=0.5, timeout=10.0)
        jobs = _collect_catalogue_page_jobs(catalogue_path)

    page_summaries = [
        {
            "handle": str(job.get("handle", "")),
            "layout_name": str(job.get("layout_name", "model")),
            "owner_btr": str(job.get("owner_btr", "*MODEL_SPACE")),
            "print_bbox": tuple(job["lower_left"] + job["upper_right"]),
            "paper_code": str(job.get("paper_code", "")),
            "media": str(job.get("media", "")),
            "sequence_no": int(job.get("sequence_no", 0) or 0),
        }
        for job in jobs
    ]
    return {
        "pages": page_summaries,
        "page_count": len(page_summaries),
        "trimmed_second_page": bool(deleted_page),
        "deleted_second_page": deleted_page,
        "deleted_handles": deleted_handles,
    }


def _attach_catalogue_pages_to_target(
    target_path: Path,
    areas: Sequence[PrintAreaResolved],
    catalogue_path: Path,
    catalogue_pages: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    if not catalogue_pages:
        return {"ok": True, "skipped": True, "reason": "no_catalogue_pages"}
    if not areas:
        return {"ok": True, "skipped": True, "reason": "no_target_print_areas"}

    distinct_spaces = {(item.layout_name, item.owner_btr) for item in areas}
    if len(distinct_spaces) != 1:
        return {
            "ok": False,
            "skipped": True,
            "reason": "multiple_target_spaces",
            "spaces": sorted(f"{layout}:{owner}" for layout, owner in distinct_spaces),
        }

    first_area = areas[0]
    target_bbox = tuple(float(v) for v in first_area.print_bbox)
    gap = max((target_bbox[2] - target_bbox[0]) / 8.0, 1.0)

    if not open_file(str(catalogue_path)):
        raise RuntimeError(f"打开目录 DWG 失败: {catalogue_path}")
    if not _activate_document_by_path(catalogue_path):
        raise RuntimeError(f"未能激活目录 DWG: {catalogue_path}")
    wait_quiescent(min_quiet=0.6, timeout=10.0)
    source_doc = C.raw_doc
    source_owner = _resolve_owner_container(source_doc, str(catalogue_pages[0].get("owner_btr", "*MODEL_SPACE")))

    if not open_file(str(target_path)):
        raise RuntimeError(f"打开目标 DWG 失败: {target_path}")
    if not _activate_document_by_path(target_path):
        raise RuntimeError(f"未能激活目标 DWG: {target_path}")
    wait_quiescent(min_quiet=0.6, timeout=10.0)
    target_doc = C.raw_doc
    target_owner = _resolve_owner_container(target_doc, first_area.owner_btr)

    ordered_pages = sorted(
        catalogue_pages,
        key=lambda item: (float(item["print_bbox"][0]), float(item["print_bbox"][1])),
    )
    destination_bboxes: list[tuple[float, float, float, float]] = []
    cursor_right = target_bbox[0] - gap
    for page in reversed(ordered_pages):
        page_bbox = tuple(float(v) for v in page["print_bbox"])
        width, height = _bbox_size(page_bbox)
        dest_left = cursor_right - width
        destination_bboxes.insert(
            0,
            (dest_left, target_bbox[1], cursor_right, target_bbox[1] + height),
        )
        cursor_right = dest_left - gap

    inserted_pages: list[dict[str, Any]] = []
    for page, destination_bbox in zip(ordered_pages, destination_bboxes):
        page_bbox = tuple(float(v) for v in page["print_bbox"])
        source_entities = _collect_entities_in_owner_bbox(source_owner, page_bbox, tol=10.0)
        if not source_entities:
            inserted_pages.append(
                {
                    "source_handle": str(page.get("handle", "")),
                    "inserted": False,
                    "reason": "source_entities_not_found",
                    "destination_bbox": destination_bbox,
                }
            )
            continue

        raw_copy_result = source_doc.CopyObjects(_dispatch_variant(source_entities), target_owner)
        wait_quiescent(min_quiet=0.1, timeout=3.0)
        copied_entities = _collect_entities_in_owner_bbox(target_owner, page_bbox, tol=10.0)
        if not copied_entities:
            copied_entities = _normalize_com_object_list(raw_copy_result)
        dx = destination_bbox[0] - page_bbox[0]
        dy = destination_bbox[1] - page_bbox[1]
        moved_handles = _move_entities_by_delta(copied_entities, dx, dy)
        inserted_pages.append(
            {
                "source_handle": str(page.get("handle", "")),
                "inserted": True,
                "source_bbox": page_bbox,
                "destination_bbox": destination_bbox,
                "copied_count": len(copied_entities),
                "moved_handles": moved_handles,
            }
        )

    save_file()
    wait_quiescent(min_quiet=0.5, timeout=10.0)
    return {
        "ok": True,
        "skipped": False,
        "target_layout_name": first_area.layout_name,
        "target_owner_btr": first_area.owner_btr,
        "gap": gap,
        "inserted_pages": inserted_pages,
    }


def _prepare_target_dwg(
    target_path: Path,
    *,
    match_mode: str,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Sequence[str] | None = None,
    requested_handles: set[str] | None = None,
) -> dict[str, Any]:
    prepare_cad_runtime(ensure_guard=True)
    if not open_file(str(target_path)):
        raise RuntimeError(f"打开 DWG 失败: {target_path}")
    if not _activate_document_by_path(target_path):
        raise RuntimeError(f"未能激活 DWG: {target_path}")
    wait_quiescent(min_quiet=0.8, timeout=20.0)
    _guard_checkpoint("compile_catalogue:after_open_target")

    tmp_output_root = USER_DIRECTORY / "_compile_plan_tmp"
    tmp_output_root.mkdir(parents=True, exist_ok=True)
    plan = build_print_plan(
        str(target_path),
        str(tmp_output_root),
        mode=normalize_print_mode(match_mode),
        include_model=include_model,
        include_layouts=include_layouts,
        only_layouts=list(only_layouts or []),
    )
    plan_jobs = {
        layout_name: [job.__dict__.copy() for job in items]
        for layout_name, items in plan.jobs_by_space.items()
    }
    plan_jobs = _filter_jobs_by_requested_handles(plan_jobs, requested_handles=requested_handles)
    return {
        "plan": plan,
        "jobs_by_space": plan_jobs,
    }


def _is_busy_exc(exc: Exception) -> bool:
    code = None
    if getattr(exc, "args", None):
        code = exc.args[0]
    text = str(exc)
    return code in (-2147418111, -2147417846) or "拒绝接收呼叫" in text or "busy" in text.lower()


def _apply_illustration_labels_with_retry(
    target_path: Path,
    *,
    match_mode: str,
    insert_titles: bool,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Sequence[str] | None = None,
    requested_handles: Sequence[str] | None = None,
) -> dict[str, Any]:
    last_exc: Exception | None = None
    for attempt in range(1, 4):
        try:
            return apply_illustration_labels(
                target_file=str(target_path),
                match_mode=match_mode,
                ensure_guard=True,
                insert_titles=insert_titles,
                include_model=include_model,
                include_layouts=include_layouts,
                only_layouts=only_layouts,
                requested_handles=requested_handles,
            )
        except Exception as exc:
            last_exc = exc
            if attempt >= 3 or not _is_busy_exc(exc):
                raise
            sys_logger.warning(
                "[compile_catalogue] illustration_label busy, retry=%s error=%s",
                attempt,
                exc,
            )
            prepare_cad_runtime(ensure_guard=True)
            open_file(str(target_path))
            _activate_document_by_path(target_path)
            wait_quiescent(min_quiet=0.8, timeout=20.0)
    assert last_exc is not None
    raise last_exc


def _resolve_single_print_area(
    job: dict[str, Any],
    *,
    owner_rects: list[Any],
    block_snapshots: list[Any],
    drawing_sequence: int,
    drawing_no_prefix: str,
) -> PrintAreaResolved:
    owner_btr_name = _resolve_owner_btr_name(job)
    _inner_handle, inner_bbox = _choose_inner_frame(job, owner_rects)
    portrait = inner_bbox is not None and (inner_bbox[3] - inner_bbox[1]) > (inner_bbox[2] - inner_bbox[0])
    orientation = "portrait" if portrait else "landscape"

    selected_block = None
    graphic_info_area_bbox = None
    guide_rectangles: dict[str, tuple[float, float, float, float]] = {}
    graphic_info_text_records: list[TextRecord] = []
    drawing_title_records: list[TextRecord] = []
    drawing_no_records: list[TextRecord] = []
    drawing_title = ""
    drawing_no = ""
    title_source = ""
    no_source = ""
    title_style = TitleStyle(style="Standard", height=350.0)
    number_style = TitleStyle(style="Standard", height=350.0)

    if inner_bbox is not None:
        selected_block = _choose_corner_block(inner_bbox, block_snapshots, portrait=portrait)
        if selected_block is not None:
            graphic_info_area_bbox = selected_block.bbox
            graphic_info_text_records = select_texts_in_bbox(owner_btr_name, graphic_info_area_bbox)
            resolved = _resolve_by_named_layers(graphic_info_text_records)
            if resolved is not None:
                drawing_title_records, drawing_no_records, _ = resolved
                title_source = "existing_layer_named"
                no_source = "existing_layer_named"
            else:
                guide_rectangles = _extract_guide_rectangles(selected_block)
                resolved = _resolve_by_guide_rectangles(owner_btr_name, guide_rectangles)
                if resolved is not None:
                    drawing_title_records, drawing_no_records, _ = resolved
                    title_source = "existing_guide_rectangles"
                    no_source = "existing_guide_rectangles"
                else:
                    drawing_title_records, drawing_no_records, _ = _resolve_by_fallback_rules(
                        graphic_info_text_records,
                        graphic_info_area_bbox,
                    )
                    if drawing_title_records:
                        title_source = "existing_fallback_regex"
                    if drawing_no_records:
                        no_source = "existing_fallback_regex"

    if drawing_title_records:
        drawing_title = _combine_texts_by_orientation(drawing_title_records, orientation)
        title_style = _derive_style_from_text_records(drawing_title_records)

    if drawing_no_records:
        drawing_no = _combine_texts_by_orientation(drawing_no_records, orientation, separator="、")
        number_style = _derive_style_from_text_records(drawing_no_records)

    red_border_area = guide_rectangles.get("red")
    green_border_area = guide_rectangles.get("green")
    if graphic_info_area_bbox and (red_border_area is None or green_border_area is None):
        fallback_red, fallback_green = _fallback_red_green_areas(graphic_info_area_bbox, orientation)
        red_border_area = red_border_area or fallback_red
        green_border_area = green_border_area or fallback_green

    if not drawing_title:
        tdb_names = _select_tdb_drawing_names(owner_btr_name, tuple(job["lower_left"] + job["upper_right"]))
        if tdb_names:
            values = []
            for ent in tdb_names:
                value = _strip_text(get_attr(ent, "图名文字", ""))
                if value:
                    values.append(value)
            drawing_title = "、".join(values)
            title_style = _derive_style_from_tdb_drawing_names(tdb_names)
            title_source = "tdb_drawing_name"
            if drawing_title and red_border_area is not None:
                _write_best_fit_text(
                    drawing_title,
                    red_border_area,
                    style=title_style.style,
                    base_height=max(title_style.height, 1.0),
                    rotation=PORTRAIT_ROTATION if orientation == "portrait" else 0.0,
                    allow_wrap=True,
                )
        else:
            top_line = _resolve_top_text_line_title(owner_btr_name, tuple(job["lower_left"] + job["upper_right"]), orientation)
            if top_line is not None:
                drawing_title, records, style = top_line
                title_style = style
                title_source = "top_text_line"
                if drawing_title and red_border_area is not None:
                    _write_best_fit_text(
                        drawing_title,
                        red_border_area,
                        style=style.style,
                        base_height=max(style.height, 1.0),
                        rotation=PORTRAIT_ROTATION if orientation == "portrait" else 0.0,
                        allow_wrap=True,
                    )
                    drawing_title_records = list(records)
            else:
                drawing_title = DEFAULT_TITLE
                title_style = TitleStyle(style="Standard", height=350.0)
                title_source = "no_title_found"

    if not drawing_no:
        drawing_no = _format_index(drawing_sequence)
        no_source = "generated_by_sequence"
        if green_border_area is not None:
            fallback_style = title_style if drawing_title != DEFAULT_TITLE else TitleStyle(style="Standard", height=350.0)
            number_style = fallback_style
            _write_best_fit_text(
                drawing_no,
                green_border_area,
                style=fallback_style.style,
                base_height=max(fallback_style.height, 1.0),
                rotation=PORTRAIT_ROTATION if orientation == "portrait" else 0.0,
                allow_wrap=False,
            )

    title_block_name = ""
    title_block_bbox = None
    title_block_handle = ""
    title_block_kind = ""
    if selected_block is not None:
        title_block_name = selected_block.block_name
        title_block_bbox = selected_block.bbox
        title_block_handle = selected_block.handle
        title_block_kind = "attribute_block" if selected_block.is_attribute_block else "normal_block"

    classified_text_records = _classify_text_record_dicts(
        graphic_info_text_records,
        drawing_title_records,
        drawing_no_records,
    )

    return PrintAreaResolved(
        sequence_no=drawing_sequence,
        layout_name=str(job.get("layout_name", "")),
        owner_btr=owner_btr_name,
        print_handle=str(job.get("handle", "")),
        paper_code=_paper_code_for_job(job),
        graphic_orientation=orientation,
        print_bbox=tuple(job["lower_left"] + job["upper_right"]),
        inner_frame_bbox=inner_bbox,
        graphic_info_area_bbox=graphic_info_area_bbox,
        red_border_area=red_border_area,
        green_border_area=green_border_area,
        drawing_title=drawing_title,
        drawing_no=_resolve_catalogue_drawing_no(drawing_no, drawing_sequence, drawing_no_prefix),
        drawing_title_source=title_source,
        drawing_no_source=no_source,
        drawing_title_records=[_text_record_to_dict(item) for item in drawing_title_records],
        drawing_no_records=[_text_record_to_dict(item) for item in drawing_no_records],
        graphic_info_text_records=[_text_record_to_dict(item) for item in graphic_info_text_records],
        classified_text_records=classified_text_records,
        title_block_handle=title_block_handle,
        title_block_name=title_block_name,
        title_block_bbox=title_block_bbox,
        title_block_kind=title_block_kind,
        title_style=asdict(title_style),
        number_style=asdict(number_style),
    )


def _dict_records_to_styles(records: Sequence[dict[str, Any]]) -> TitleStyle:
    for item in records:
        ent = _get_entity_by_handle(str(item.get("handle", "")))
        if ent is None:
            continue
        return TitleStyle(style=_safe_text_style(ent), height=_safe_text_height(ent))
    if records:
        bbox = item.get("bbox") if (item := records[0]) else None
        if bbox and len(bbox) == 4:
            return TitleStyle(style="Standard", height=max(float(bbox[3]) - float(bbox[1]), 250.0))
    return TitleStyle(style="Standard", height=350.0)


def _resolve_single_print_area_from_analysis(
    job: dict[str, Any],
    row: dict[str, Any],
    *,
    block_snapshots: list[Any],
    drawing_no_prefix: str,
) -> PrintAreaResolved:
    owner_btr_name = _resolve_owner_btr_name(job)
    orientation = str(row.get("graphic_orientation") or ("portrait" if int(job.get("rotation", 0)) == 1 else "landscape"))
    graphic_info_area_bbox = row.get("graphic_info_area_bbox")
    if graphic_info_area_bbox:
        graphic_info_area_bbox = tuple(float(v) for v in graphic_info_area_bbox)
    inner_frame_bbox = row.get("inner_frame_bbox")
    if inner_frame_bbox:
        inner_frame_bbox = tuple(float(v) for v in inner_frame_bbox)

    selected_block = None
    title_block_handle = str(row.get("title_block_handle", "") or "")
    if title_block_handle:
        for item in block_snapshots:
            if str(item.handle) == title_block_handle:
                selected_block = item
                break

    guide_rectangles: dict[str, tuple[float, float, float, float]] = {}
    if selected_block is not None:
        guide_rectangles = _extract_guide_rectangles(selected_block)

    red_border_area = guide_rectangles.get("red")
    green_border_area = guide_rectangles.get("green")
    if graphic_info_area_bbox and (red_border_area is None or green_border_area is None):
        fallback_red, fallback_green = _fallback_red_green_areas(graphic_info_area_bbox, orientation)
        red_border_area = red_border_area or fallback_red
        green_border_area = green_border_area or fallback_green

    drawing_title = _strip_text(row.get("drawing_title", ""))
    drawing_no = _strip_text(row.get("drawing_no", ""))
    title_source = _strip_text(row.get("title_no_resolve_method", "")) or "existing"
    no_source = _strip_text(row.get("title_no_resolve_method", "")) or "existing"

    drawing_title_records = list(row.get("drawing_title_records", []) or [])
    drawing_no_records = list(row.get("drawing_no_records", []) or [])
    graphic_info_text_records = list(row.get("graphic_info_text_records", []) or [])
    classified_text_records = list(row.get("classified_text_records", []) or [])

    title_style = _dict_records_to_styles(drawing_title_records)
    number_style = _dict_records_to_styles(drawing_no_records)

    if not drawing_title:
        tdb_names = _select_tdb_drawing_names(owner_btr_name, tuple(job["lower_left"] + job["upper_right"]))
        if tdb_names:
            values = []
            for ent in tdb_names:
                value = _strip_text(get_attr(ent, "图名文字", ""))
                if value:
                    values.append(value)
            drawing_title = "、".join(values)
            title_style = _derive_style_from_tdb_drawing_names(tdb_names)
            title_source = "tdb_drawing_name"
            if drawing_title and red_border_area is not None:
                _write_best_fit_text(
                    drawing_title,
                    red_border_area,
                    style=title_style.style,
                    base_height=max(title_style.height, 1.0),
                    rotation=PORTRAIT_ROTATION if orientation == "portrait" else 0.0,
                    allow_wrap=True,
                )
        else:
            top_line = _resolve_top_text_line_title(owner_btr_name, tuple(job["lower_left"] + job["upper_right"]), orientation)
            if top_line is not None:
                drawing_title, records, style = top_line
                title_style = style
                title_source = "top_text_line"
                drawing_title_records = [_text_record_to_dict(item) for item in records]
                if drawing_title and red_border_area is not None:
                    _write_best_fit_text(
                        drawing_title,
                        red_border_area,
                        style=style.style,
                        base_height=max(style.height, 1.0),
                        rotation=PORTRAIT_ROTATION if orientation == "portrait" else 0.0,
                        allow_wrap=True,
                    )
            else:
                drawing_title = DEFAULT_TITLE
                title_style = TitleStyle(style="Standard", height=350.0)
                title_source = "no_title_found"

    if not drawing_no:
        drawing_no = _format_index(int(row.get("sequence_no", 0) or 0))
        no_source = "generated_by_sequence"
        fallback_style = title_style if drawing_title != DEFAULT_TITLE else TitleStyle(style="Standard", height=350.0)
        number_style = fallback_style
        if green_border_area is not None:
            _write_best_fit_text(
                drawing_no,
                green_border_area,
                style=fallback_style.style,
                base_height=max(fallback_style.height, 1.0),
                rotation=PORTRAIT_ROTATION if orientation == "portrait" else 0.0,
                allow_wrap=False,
            )

    return PrintAreaResolved(
        sequence_no=int(row.get("sequence_no", 0) or 0),
        layout_name=str(job.get("layout_name", "")),
        owner_btr=owner_btr_name,
        print_handle=str(job.get("handle", "")),
        paper_code=_paper_code_for_job(job),
        graphic_orientation=orientation,
        print_bbox=tuple(job["lower_left"] + job["upper_right"]),
        inner_frame_bbox=inner_frame_bbox,
        graphic_info_area_bbox=graphic_info_area_bbox,
        red_border_area=red_border_area,
        green_border_area=green_border_area,
        drawing_title=drawing_title,
        drawing_no=_resolve_catalogue_drawing_no(drawing_no, int(row.get("sequence_no", 0) or 0), drawing_no_prefix),
        drawing_title_source=title_source,
        drawing_no_source=no_source,
        drawing_title_records=drawing_title_records,
        drawing_no_records=drawing_no_records,
        graphic_info_text_records=graphic_info_text_records,
        classified_text_records=classified_text_records,
        title_block_handle=str(row.get("title_block_handle", "") or ""),
        title_block_name=str(row.get("title_block_name", "") or ""),
        title_block_bbox=tuple(float(v) for v in row.get("title_block_bbox")) if row.get("title_block_bbox") else None,
        title_block_kind=str(row.get("title_block_kind", "") or ""),
        title_style=asdict(title_style),
        number_style=asdict(number_style),
    )


def _resolve_print_areas(
    target_path: Path,
    *,
    match_mode: str,
    drawing_no_prefix: str,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Sequence[str] | None = None,
    requested_handles: Sequence[str] | None = None,
) -> list[PrintAreaResolved]:
    requested_handle_set = {str(item).strip() for item in (requested_handles or []) if str(item).strip()}
    refreshed = _prepare_target_dwg(
        target_path,
        match_mode=match_mode,
        include_model=include_model,
        include_layouts=include_layouts,
        only_layouts=only_layouts,
        requested_handles=requested_handle_set,
    )
    jobs_by_space = refreshed["jobs_by_space"]
    all_jobs = [job for jobs in jobs_by_space.values() for job in jobs]
    if (
        not all_jobs
        and normalize_print_mode(match_mode) == PRINT_MODE_BASIC
        and include_layouts
    ):
        sys_logger.info(
            "[compile_catalogue] basic 模式下未识别到布局打印区域，自动回退到 adaptive 再试一次。"
        )
        refreshed = _prepare_target_dwg(
            target_path,
            match_mode=PRINT_MODE_ADAPTIVE,
            include_model=include_model,
            include_layouts=include_layouts,
            only_layouts=only_layouts,
            requested_handles=requested_handle_set,
        )
        jobs_by_space = refreshed["jobs_by_space"]
        all_jobs = [job for jobs in jobs_by_space.values() for job in jobs]
    if not all_jobs:
        return []

    analysis = analyze_print_info_jobs(jobs_by_space)
    page_info_dict = analysis.get("page_info_dict", {}) or {}
    need_illustration = False
    for row in page_info_dict.values():
        if int(row.get("inner_frame_exists", 0) or 0) == 0:
            need_illustration = True
            break
        if int(row.get("right_bottom_title_block_exists", 0) or 0) == 0:
            need_illustration = True
            break

    if need_illustration:
        sys_logger.info("[compile_catalogue] 检测到缺少内框或角点图签块，执行 illustration_label 补全。")
        original_jobs_by_space = {
            layout_name: [dict(item) for item in jobs]
            for layout_name, jobs in jobs_by_space.items()
        }
        _apply_illustration_labels_with_retry(
            target_path,
            match_mode=match_mode,
            insert_titles=True,
            include_model=include_model,
            include_layouts=include_layouts,
            only_layouts=only_layouts,
            requested_handles=requested_handles,
        )
        jobs_by_space = original_jobs_by_space
        analysis = analyze_print_info_jobs(jobs_by_space)
        page_info_dict = analysis.get("page_info_dict", {}) or {}

    blocks_cache: dict[str, list[Any]] = {}
    rows: list[PrintAreaResolved] = []

    for jobs in jobs_by_space.values():
        for job in jobs:
            owner_btr_name = _resolve_owner_btr_name(job)
            if owner_btr_name not in blocks_cache:
                blocks_cache[owner_btr_name] = collect_space_block_snapshots(owner_btr_name)
            page_key = f"{job['layout_name']}-{int(job['sequence_no']):02d}"
            row = page_info_dict.get(page_key, {})
            rows.append(
                _resolve_single_print_area_from_analysis(
                    job,
                    row,
                    block_snapshots=blocks_cache.get(owner_btr_name, []),
                    drawing_no_prefix=drawing_no_prefix,
                )
            )

    if rows:
        save_file()
        wait_quiescent(min_quiet=0.5, timeout=10.0)
    return rows


def _copy_directory_template(target_name: str) -> Path:
    if not DIRECTORY_TEMPLATE.exists():
        raise FileNotFoundError(f"目录模板不存在: {DIRECTORY_TEMPLATE}")
    USER_DIRECTORY.mkdir(parents=True, exist_ok=True)
    output_path = USER_DIRECTORY / target_name
    if output_path.exists():
        output_path.unlink()
    shutil.copy2(DIRECTORY_TEMPLATE, output_path)
    return output_path


def _catalogue_entries(
    areas: Sequence[PrintAreaResolved],
    *,
    drawing_no_prefix: str,
    catalog_name: str,
    default_remark: str,
) -> tuple[list[CatalogueEntry], bool]:
    use_second_page = len(areas) > 60
    entries: list[CatalogueEntry] = []

    header_no = f"{drawing_no_prefix}00"
    if use_second_page:
        entries.extend(
            (
                CatalogueEntry("01", catalog_name, f"{drawing_no_prefix}00a", "A2", default_remark, "", "catalog_header"),
                CatalogueEntry("02", catalog_name, f"{drawing_no_prefix}00b", "A2", default_remark, "", "catalog_header"),
            )
        )
    else:
        entries.append(CatalogueEntry("01", catalog_name, header_no, "A2", default_remark, "", "catalog_header"))

    start_seq = len(entries) + 1
    for idx, area in enumerate(areas, start=1):
        entries.append(
            CatalogueEntry(
                sequence_no=_format_index(start_seq + idx - 1),
                drawing_title=_strip_text(area.drawing_title) or DEFAULT_TITLE,
                drawing_no=f"{drawing_no_prefix}{_format_index(idx)}",
                paper_code=area.paper_code or "A2",
                remark=default_remark,
                source_print_handle=area.print_handle,
                kind="drawing",
            )
        )
    return entries, use_second_page


def _write_catalogue_entries(
    catalogue_path: Path,
    entries: Sequence[CatalogueEntry],
    *,
    use_second_page: bool,
) -> dict[str, Any]:
    if not open_file(str(catalogue_path)):
        raise RuntimeError(f"打开目录 DWG 失败: {catalogue_path}")
    if not _activate_document_by_path(catalogue_path):
        raise RuntimeError(f"未能激活目录 DWG: {catalogue_path}")
    wait_quiescent(min_quiet=0.6, timeout=10.0)
    _guard_checkpoint("compile_catalogue:after_open_catalogue_template")

    row_bboxes = _catalogue_row_bboxes()
    if len(entries) > len(row_bboxes):
        raise RuntimeError(f"目录容量不足：需要 {len(entries)} 行，模板仅支持 {len(row_bboxes)} 行")

    cleared_handles: list[str] = []
    for _row_name, row_bbox in row_bboxes:
        cleared_handles.extend(_clear_text_entities_in_bbox(row_bbox))

    if not use_second_page:
        cleared_handles.extend(_clear_text_entities_in_bbox(_second_catalogue_page_bbox()))

    written_handles: list[str] = []
    for entry, (_row_name, row_bbox) in zip(entries, row_bboxes):
        segment_bboxes = _row_segment_bboxes(row_bbox)
        for key in ROW_SEGMENT_KEYS:
            handles = _write_best_fit_text(
                getattr(entry, key),
                segment_bboxes[key],
                style=DEFAULT_TEXT_STYLE,
                base_height=DEFAULT_TEXT_HEIGHT,
                allow_wrap=False,
            )
            written_handles.extend(handles)

    save_file()
    wait_quiescent(min_quiet=0.5, timeout=10.0)
    return {
        "catalogue_path": str(catalogue_path),
        "entry_count": len(entries),
        "used_second_page": use_second_page,
        "cleared_handles": cleared_handles,
        "written_handles": written_handles,
    }


def compile_catalogue(
    *,
    target_file: str | Path,
    match_mode: str = DEFAULT_MATCH_MODE,
    drawing_no_prefix: str = DEFAULT_PREFIX,
    catalog_name: str = DEFAULT_CATALOG_NAME,
    default_remark: str = DEFAULT_REMARK,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Sequence[str] | None = None,
    requested_handles: Sequence[str] | None = None,
) -> dict[str, Any]:
    target_path = Path(target_file).resolve()
    if not target_path.exists():
        raise FileNotFoundError(target_path)

    started_at = _now_timestamp_text()
    total_timer = time.perf_counter()
    stage_timers: dict[str, float] = {}

    result: dict[str, Any] = {
        "ok": False,
        "target_file": str(target_path),
        "match_mode": normalize_print_mode(match_mode),
        "drawing_no_prefix": drawing_no_prefix,
        "catalog_name": catalog_name,
        "default_remark": default_remark,
        "include_model": bool(include_model),
        "include_layouts": bool(include_layouts),
        "only_layouts": [str(item) for item in (only_layouts or []) if str(item).strip()],
        "requested_handles": [str(item) for item in (requested_handles or []) if str(item).strip()],
        "started_at": started_at,
    }

    try:
        stage_start = time.perf_counter()
        areas = _resolve_print_areas(
            target_path,
            match_mode=normalize_print_mode(match_mode),
            drawing_no_prefix=drawing_no_prefix,
            include_model=include_model,
            include_layouts=include_layouts,
            only_layouts=only_layouts,
            requested_handles=requested_handles,
        )
        stage_timers["resolve_print_areas_seconds"] = round(time.perf_counter() - stage_start, 3)
        result["print_area_count"] = len(areas)
        result["print_areas"] = [asdict(item) for item in areas]

        if not areas:
            result["ok"] = True
            result["skipped"] = True
            result["message"] = "未识别到打印区域，不执行后续目录生成。"
            return result

        stage_start = time.perf_counter()
        scope_suffix = _scope_suffix(
            include_model=include_model,
            include_layouts=include_layouts,
            only_layouts=only_layouts,
            requested_handles=requested_handles,
        )
        result["scope_suffix"] = scope_suffix
        target_name = f"{target_path.stem}_{scope_suffix}_目录.dwg" if scope_suffix else f"{target_path.stem}_目录.dwg"
        catalogue_path = _copy_directory_template(target_name)
        entries, use_second_page = _catalogue_entries(
            areas,
            drawing_no_prefix=drawing_no_prefix,
            catalog_name=catalog_name,
            default_remark=default_remark,
        )
        stage_timers["prepare_catalogue_seconds"] = round(time.perf_counter() - stage_start, 3)
        result["entries"] = [asdict(item) for item in entries]

        stage_start = time.perf_counter()
        result["catalogue_write"] = _write_catalogue_entries(
            catalogue_path,
            entries,
            use_second_page=use_second_page,
        )
        stage_timers["write_catalogue_seconds"] = round(time.perf_counter() - stage_start, 3)

        stage_start = time.perf_counter()
        result["catalogue_finalize"] = _trim_catalogue_pages(
            catalogue_path,
            use_second_page=use_second_page,
        )
        stage_timers["finalize_catalogue_seconds"] = round(time.perf_counter() - stage_start, 3)

        stage_start = time.perf_counter()
        result["catalogue_attach"] = _attach_catalogue_pages_to_target(
            target_path,
            areas,
            catalogue_path,
            result["catalogue_finalize"].get("pages", []),
        )
        stage_timers["attach_catalogue_seconds"] = round(time.perf_counter() - stage_start, 3)
        result["catalogue_file"] = str(catalogue_path)
        result["ok"] = True
        return result
    finally:
        result["finished_at"] = _now_timestamp_text()
        result["elapsed_seconds"] = round(time.perf_counter() - total_timer, 3)
        result["stage_durations"] = stage_timers
        try:
            cad_zt_oneb()
        except Exception as exc:
            sys_logger.warning("[compile_catalogue] cad_zt_oneb 收尾失败: %s", exc)


def main() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dwg", required=True, help="target dwg path")
    parser.add_argument("--match-mode", default=DEFAULT_MATCH_MODE, help="basic/adaptive/purified_adaptive")
    parser.add_argument("--drawing-no-prefix", default=DEFAULT_PREFIX, help="default prefix for generated drawing no")
    parser.add_argument("--catalog-name", default=DEFAULT_CATALOG_NAME, help="catalog header title")
    parser.add_argument("--remark", default=DEFAULT_REMARK, help="default remark value")
    parser.add_argument("--output-json", default="", help="optional json summary path")
    parser.add_argument("--layout", action="append", default=None, help="only compile specified layout, repeatable")
    parser.add_argument("--handle", action="append", default=None, help="only compile specified print-area handle, repeatable")
    parser.add_argument("--no-model", action="store_true", help="skip model space")
    parser.add_argument("--no-layouts", action="store_true", help="skip layout spaces")
    args = parser.parse_args()
    if args.layout and args.no_layouts:
        raise SystemExit("--layout 与 --no-layouts 不能同时使用")

    try:
        payload = compile_catalogue(
            target_file=args.dwg,
            match_mode=args.match_mode,
            drawing_no_prefix=args.drawing_no_prefix,
            catalog_name=args.catalog_name,
            default_remark=args.remark,
            include_model=not args.no_model,
            include_layouts=not args.no_layouts,
            only_layouts=args.layout,
            requested_handles=args.handle,
        )
        if args.output_json:
            output_path = Path(args.output_json).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except RuntimeGuardTriggered as exc:
        payload = render_guard_error(exc)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
