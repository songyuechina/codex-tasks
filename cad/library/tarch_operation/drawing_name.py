#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TArch drawing-name helpers built around the local system template DWG."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from system.CAD_selection import get_object_property, set_object_property
from system.CAD_com_utils import sys_logger
from system.licad import C

from .single_line_text import (
    DEFAULT_TEXT_STYLE,
    DEFAULT_TEXT_TYPEFACE,
    SYSTEM_FILES_DIR,
    _ensure_text_style,
    _ensure_target_document,
    _insert_template_entity,
    _move_entity_bbox_anchor,
    _normalize_plot_scale,
    _refresh_active_doc,
)

DEFAULT_TEMPLATE_FILE = SYSTEM_FILES_DIR / "图名标注.dwg"
DEFAULT_TEMPLATE_LAYER = "DIM_SYMB"
DEFAULT_TEMPLATE_OBJECT = "TDbDrawingName"


def _format_scale_text(plot_scale: float) -> str:
    rounded = round(float(plot_scale))
    if abs(float(plot_scale) - rounded) < 1e-9:
        return f"1:{int(rounded)}"
    return f"1:{float(plot_scale):g}"


def _normalize_yes_no(value) -> str:
    if isinstance(value, str):
        text = value.strip()
        if text in {"是", "否"}:
            return text
        lowered = text.lower()
        if lowered in {"true", "yes", "y", "1"}:
            return "是"
        if lowered in {"false", "no", "n", "0"}:
            return "否"
    return "是" if bool(value) else "否"


def _best_effort_set(ent, property_name: str, value, *, warnings: list[str]) -> None:
    try:
        ok = set_object_property(ent, property_name, value)
        if ok is False:
            raise RuntimeError("set_object_property returned False")
    except Exception as exc:
        warnings.append(f"{property_name} set failed: {exc}")
        sys_logger.warning(f"[tarch_operation] TDbDrawingName property set failed: {property_name}={value!r}, exc={exc}")


def _build_result(
    ent,
    *,
    template_path: Path,
    target_dwg_path: str | None,
    bbox_min,
    bbox_max,
    saved: bool,
    warnings: list[str],
) -> dict:
    return {
        "ok": True,
        "entity": ent,
        "object_name": getattr(ent, "ObjectName", None),
        "handle": getattr(ent, "Handle", None),
        "doc_name": getattr(C.raw_doc, "Name", None),
        "doc_fullname": getattr(C.raw_doc, "FullName", None),
        "template_path": str(template_path),
        "target_dwg_path": target_dwg_path,
        "layer": get_object_property(ent, "Layer"),
        "drawing_name_text": get_object_property(ent, "图名文字"),
        "drawing_name_style": get_object_property(ent, "图名样式"),
        "drawing_name_height": get_object_property(ent, "图名高度"),
        "scale_text": get_object_property(ent, "比例文字"),
        "scale_style": get_object_property(ent, "比例样式"),
        "scale_height": get_object_property(ent, "比例高度"),
        "spacing_factor": get_object_property(ent, "间距系数"),
        "annotation_style": get_object_property(ent, "标注样式"),
        "show_scale": get_object_property(ent, "显示比例"),
        "rotation": get_object_property(ent, "布局转角"),
        "prefix_text": get_object_property(ent, "前缀文字"),
        "scale_value": get_object_property(ent, "比例数值"),
        "bbox_min": bbox_min,
        "bbox_max": bbox_max,
        "saved": saved,
        "warnings": warnings,
    }


def write_tarch_drawing_name(
    drawing_name_text: str,
    target_point: Sequence[float] = (0.0, 0.0, 0.0),
    *,
    target_dwg_path: str | Path | None = None,
    plot_scale: float | int | str = 100,
    scale_text: str | None = None,
    drawing_name_height: float | None = None,
    scale_height: float | None = None,
    spacing_factor: float | None = None,
    annotation_style: str | None = None,
    text_style: str = DEFAULT_TEXT_STYLE,
    show_scale: bool | str = True,
    rotation_degrees: float = 0.0,
    prefix_text: str | None = None,
    layer: str | None = None,
    alignment: str = "左下",
    template_path: str | Path | None = None,
    save: bool = False,
) -> dict:
    """
    Write one TArch drawing-name entity into the active or target DWG.

    The function inserts and explodes the local `图名标注.dwg` template, updates
    the new `TDbDrawingName`, then aligns its bbox anchor to `target_point`.
    """

    resolved_target_path = _ensure_target_document(target_dwg_path)

    template_file = Path(template_path).resolve() if template_path else DEFAULT_TEMPLATE_FILE.resolve()
    if not template_file.exists():
        raise FileNotFoundError(f"template dwg not found: {template_file}")

    normalized_plot_scale = _normalize_plot_scale(plot_scale)
    resolved_scale_text = scale_text or _format_scale_text(normalized_plot_scale)
    resolved_layer = layer or DEFAULT_TEMPLATE_LAYER
    _ensure_text_style(style_name=text_style, typeface=DEFAULT_TEXT_TYPEFACE)

    ent = _insert_template_entity(
        template_file,
        layer_name=DEFAULT_TEMPLATE_LAYER,
        object_name=DEFAULT_TEMPLATE_OBJECT,
    )

    set_object_property(ent, "图名文字", drawing_name_text)
    set_object_property(ent, "比例文字", resolved_scale_text)
    set_object_property(ent, "比例数值", normalized_plot_scale)
    set_object_property(ent, "显示比例", _normalize_yes_no(show_scale))
    set_object_property(ent, "布局转角", float(rotation_degrees))
    set_object_property(ent, "Layer", resolved_layer)

    if drawing_name_height is not None:
        set_object_property(ent, "图名高度", float(drawing_name_height))
    if scale_height is not None:
        set_object_property(ent, "比例高度", float(scale_height))
    if spacing_factor is not None:
        set_object_property(ent, "间距系数", float(spacing_factor))
    if annotation_style:
        set_object_property(ent, "标注样式", annotation_style)
    if prefix_text is not None:
        set_object_property(ent, "前缀文字", prefix_text)

    warnings: list[str] = []
    _best_effort_set(ent, "图名样式", text_style, warnings=warnings)
    _best_effort_set(ent, "比例样式", text_style, warnings=warnings)

    _refresh_active_doc()
    bbox_min, bbox_max = _move_entity_bbox_anchor(ent, target_point, alignment)

    saved = False
    if save:
        from system.CAD_core import save_file

        saved = bool(save_file())

    sys_logger.info(
        "[tarch_operation] write_tarch_drawing_name ok: "
        f"text={drawing_name_text!r}, doc={getattr(C.raw_doc, 'Name', None)}, handle={getattr(ent, 'Handle', None)}"
    )

    return _build_result(
        ent,
        template_path=template_file,
        target_dwg_path=resolved_target_path,
        bbox_min=bbox_min,
        bbox_max=bbox_max,
        saved=saved,
        warnings=warnings,
    )
