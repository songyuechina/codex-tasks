#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TArch single-line text helpers built around the local system template DWG."""

from __future__ import annotations

import math
import time
from pathlib import Path
from typing import Iterable, Sequence

import pythoncom
from win32com.client import VARIANT

from system.CAD_selection import get_object_property, set_object_property, stc
from system.CAD_com_utils import sys_logger
from system.licad import C

SYSTEM_FILES_DIR = Path(__file__).with_name("system_files")
DEFAULT_TEMPLATE_FILE = SYSTEM_FILES_DIR / "天.dwg"
DEFAULT_TEMPLATE_LAYER = "PUB_TEXT"
DEFAULT_TEMPLATE_OBJECT = "TDbText"
DEFAULT_TEXT_STYLE = "TARCH_CN_STANDARD"
DEFAULT_TEXT_TYPEFACE = "宋体"


def _point3(point: Sequence[float]) -> tuple[float, float, float]:
    values = [float(v) for v in point]
    if len(values) == 2:
        values.append(0.0)
    if len(values) != 3:
        raise ValueError(f"point must have 2 or 3 numbers, got {point!r}")
    return values[0], values[1], values[2]


def _vt_point(point: Sequence[float]) -> VARIANT:
    return VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, _point3(point))


def _refresh_active_doc() -> None:
    try:
        C.raw_doc.Regen(1)
    except Exception:
        pass


def _require_prestarted_tarch_runtime() -> dict:
    """
    Require an already running healthy TArch runtime.

    This workspace must not bootstrap or rebuild CAD on behalf of business
    functions. The caller is expected to start TArch in advance via a separate
    controlled entry.
    """
    from system.CAD_core import inspect_cad_runtime

    snapshot = inspect_cad_runtime()
    status = snapshot.get("status")
    acad_process_count = int(snapshot.get("acad_process_count", 0) or 0)
    tarch_process_count = int(snapshot.get("tarch_process_count", 0) or 0)
    plain_pids = list(snapshot.get("plain_process_pids") or [])

    if (
        status != "healthy_tarch"
        or acad_process_count != 1
        or tarch_process_count != 1
        or plain_pids
    ):
        raise RuntimeError(
            "tarch_operation requires exactly one prestarted healthy TArch CAD process. "
            "Start or recover CAD through a separate controlled entry before "
            f"calling this function. snapshot={snapshot}"
        )

    if not C.li():
        raise RuntimeError(
            "TArch runtime appears active but the COM connection could not be refreshed. "
            "Recover the runtime through a separate controlled entry before calling this function."
        )

    try:
        pythoncom.PumpWaitingMessages()
    except Exception:
        pass

    return snapshot


def _alignment_anchor(min_pt: Sequence[float], max_pt: Sequence[float], alignment: str) -> tuple[float, float, float]:
    xmin, ymin, zmin = _point3(min_pt)
    xmax, ymax, zmax = _point3(max_pt)
    mode = (alignment or "左下").strip().lower()
    if mode in {"左下", "左对齐", "lb"}:
        return xmin, ymin, zmin
    if mode in {"左上", "lt"}:
        return xmin, ymax, zmin
    if mode in {"右下", "rb"}:
        return xmax, ymin, zmin
    if mode in {"右上", "rt"}:
        return xmax, ymax, zmin
    if mode in {"中心", "center", "c"}:
        return (xmin + xmax) / 2.0, (ymin + ymax) / 2.0, (zmin + zmax) / 2.0
    return xmin, ymin, zmin


def _move_entity_bbox_anchor(ent, target_point: Sequence[float], alignment: str) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    min_pt, max_pt = ent.GetBoundingBox()
    anchor = _alignment_anchor(min_pt, max_pt, alignment)
    ent.Move(_vt_point(anchor), _vt_point(target_point))
    _refresh_active_doc()
    min_after, max_after = ent.GetBoundingBox()
    return _point3(min_after), _point3(max_after)


def _iter_entities_by_object_name(entities: Iterable, object_name: str) -> list:
    matched = []
    for ent in list(entities):
        try:
            if getattr(ent, "ObjectName", "") == object_name:
                matched.append(ent)
        except Exception:
            continue
    return matched


def _layer_object_candidates(layer_name: str, object_name: str) -> list:
    last_error = None
    for _ in range(10):
        try:
            return _iter_entities_by_object_name(stc(layer_name), object_name)
        except Exception as exc:
            last_error = exc
            time.sleep(0.3)
    if last_error:
        raise last_error
    return []


def _handle_value(ent) -> str:
    return str(getattr(ent, "Handle", "")).upper()


def _ensure_target_document(target_dwg_path: str | Path | None) -> str | None:
    _require_prestarted_tarch_runtime()

    acad = C.acad

    if target_dwg_path is None:
        return None

    resolved = Path(target_dwg_path).resolve()
    resolved.parent.mkdir(parents=True, exist_ok=True)

    if resolved.exists():
        normalized = str(resolved).lower()
        try:
            for doc in acad.Documents:
                try:
                    if str(Path(doc.FullName).resolve()).lower() == normalized:
                        doc.Activate()
                        if not C.li():
                            raise RuntimeError(
                                f"failed to refresh active document after activating target dwg: {resolved}"
                            )
                        return str(resolved)
                except Exception:
                    continue
        except Exception as exc:
            raise RuntimeError(f"failed to inspect open documents for {resolved}: {exc}") from exc

        try:
            acad.Documents.Open(str(resolved))
        except Exception as exc:
            raise RuntimeError(f"failed to open target dwg in prestarted TArch runtime: {resolved}") from exc

        time.sleep(0.6)
        if not C.li():
            raise RuntimeError(f"failed to refresh active document after opening target dwg: {resolved}")
        return str(resolved)

    try:
        doc = acad.Documents.Add()
        time.sleep(0.6)
        doc.SaveAs(str(resolved))
    except Exception as exc:
        raise RuntimeError(f"failed to create target dwg in prestarted TArch runtime: {resolved}") from exc

    time.sleep(0.6)
    if not C.li():
        raise RuntimeError(f"failed to refresh active document after creating target dwg: {resolved}")
    return str(resolved)


def _insert_template_entity(
    template_path: Path,
    *,
    layer_name: str = DEFAULT_TEMPLATE_LAYER,
    object_name: str = DEFAULT_TEMPLATE_OBJECT,
):
    from system.CAD_core import insert_file_exploded

    before = {_handle_value(ent): ent for ent in _layer_object_candidates(layer_name, object_name)}
    ok = insert_file_exploded(str(template_path), target_doc=C.raw_doc, x=0, y=0, z=0, scale=1.0)
    if not ok:
        raise RuntimeError(f"failed to insert template dwg: {template_path}")

    last_error = None
    for _ in range(10):
        try:
            time.sleep(0.4)
            _refresh_active_doc()
            after = _layer_object_candidates(layer_name, object_name)
            new_entities = [ent for ent in after if _handle_value(ent) not in before]
            if new_entities:
                return new_entities[-1]
        except Exception as exc:
            last_error = exc
        time.sleep(0.3)
    if last_error:
        raise RuntimeError(
            f"template {template_path} inserted but new {object_name} scan failed: {last_error}"
        )
    raise RuntimeError(f"template {template_path} inserted no new {object_name}")


def _normalize_plot_scale(plot_scale) -> float:
    if plot_scale is None:
        return 100.0
    if isinstance(plot_scale, str):
        text = plot_scale.strip().replace("：", ":")
        if ":" in text:
            left, right = text.split(":", 1)
            if left.strip() == "1":
                return float(right.strip())
        return float(text)
    return float(plot_scale)


def _ensure_text_style(style_name: str = DEFAULT_TEXT_STYLE, typeface: str = DEFAULT_TEXT_TYPEFACE):
    styles = C.raw_doc.TextStyles
    try:
        text_style = styles.Item(style_name)
    except Exception:
        text_style = styles.Add(style_name)

    text_style.SetFont(typeface, False, False, 1, 0)
    return text_style


def _build_result(ent, *, template_path: Path, target_dwg_path: str | None, bbox_min, bbox_max, saved: bool) -> dict:
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
        "text": get_object_property(ent, "Text"),
        "height": get_object_property(ent, "Height"),
        "width_factor": get_object_property(ent, "WidthFactor"),
        "rotation": get_object_property(ent, "Rotation"),
        "oblique": get_object_property(ent, "Oblique"),
        "plot_scale": get_object_property(ent, "Scale"),
        "text_style": get_object_property(ent, "TextStyle"),
        "bbox_min": bbox_min,
        "bbox_max": bbox_max,
        "saved": saved,
    }


def write_tarch_single_line_text(
    text: str,
    target_point: Sequence[float] = (0.0, 0.0, 0.0),
    *,
    target_dwg_path: str | Path | None = None,
    height: float = 3.5,
    width_factor: float = 1.0,
    rotation_degrees: float = 0.0,
    oblique_degrees: float = 0.0,
    style: str = DEFAULT_TEXT_STYLE,
    alignment: str = "左下",
    layer: str | None = None,
    plot_scale: float | int | str = 100,
    template_path: str | Path | None = None,
    save: bool = False,
) -> dict:
    """
    Write one TArch single-line text into the active or target DWG.

    The function reuses the local `天.dwg` template, keeps the default TArch
    shape, and aligns the requested bbox anchor to `target_point`.
    """

    resolved_target_path = _ensure_target_document(target_dwg_path)

    template_file = Path(template_path).resolve() if template_path else DEFAULT_TEMPLATE_FILE.resolve()
    if not template_file.exists():
        raise FileNotFoundError(f"template dwg not found: {template_file}")

    rotation_radians = math.radians(float(rotation_degrees))
    oblique_radians = math.radians(float(oblique_degrees))
    normalized_plot_scale = _normalize_plot_scale(plot_scale)

    ent = _insert_template_entity(
        template_file,
        layer_name=DEFAULT_TEMPLATE_LAYER,
        object_name=DEFAULT_TEMPLATE_OBJECT,
    )
    layer_name = layer or get_object_property(ent, "Layer") or DEFAULT_TEMPLATE_LAYER

    _ensure_text_style(style_name=style, typeface=DEFAULT_TEXT_TYPEFACE)

    set_object_property(ent, "Text", text)
    set_object_property(ent, "Height", float(height))
    set_object_property(ent, "WidthFactor", float(width_factor))
    set_object_property(ent, "Rotation", rotation_radians)
    set_object_property(ent, "Oblique", oblique_radians)
    set_object_property(ent, "Scale", normalized_plot_scale)
    set_object_property(ent, "TextStyle", style)
    set_object_property(ent, "Layer", layer_name)

    time.sleep(0.4)
    _refresh_active_doc()
    bbox_min, bbox_max = _move_entity_bbox_anchor(ent, target_point, alignment)

    saved = False
    if save:
        from system.CAD_core import save_file
        saved = bool(save_file())

    sys_logger.info(
        "[tarch_operation] write_tarch_single_line_text ok: "
        f"text={text!r}, doc={getattr(C.raw_doc, 'Name', None)}, handle={getattr(ent, 'Handle', None)}"
    )

    return _build_result(
        ent,
        template_path=template_file,
        target_dwg_path=resolved_target_path,
        bbox_min=bbox_min,
        bbox_max=bbox_max,
        saved=saved,
    )
