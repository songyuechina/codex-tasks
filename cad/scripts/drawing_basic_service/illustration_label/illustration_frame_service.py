from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from math import pi
import os
from pathlib import Path
import shutil
import time
from typing import Any, Iterable, Sequence

import pythoncom
import win32com.client
from illustration_block_service import (
    DEFAULT_BLOCK_NAMES,
    prepare_cad_runtime,
    replace_single_block_definition,
)
from print.print_area_analysis import (
    get_print_area_polylines,
    get_rect_polylines_by_space,
    is_rectangular_polyline,
    match_standard_print_by_mode,
    select_all_polylines,
)
from print.print_policy import collect_print_jobs
from system.CAD_com_utils import retry_if_busy
from system.CAD_coordination import wait_quiescent
from system.CAD_core import open_file
from system.common_logger import sys_logger
from system.licad import C
from system.runtime_guard_bridge import (
    RuntimeGuardTriggered,
    assert_runtime_guard_ok,
    render_guard_error,
)


DEFAULT_MATCH_MODE = "purified_adaptive"
SUPPORTED_MATCH_MODES = {"basic", "adaptive", "purified_adaptive"}
PORTRAIT_ROTATION = -pi / 2.0
INNER_FRAME_RATIO_THRESHOLD = 0.85
MODEL_SPACE_OWNER = "*MODEL_SPACE"
MODEL_LAYOUT_NAME = "model"
_BLOCK_REF_CAST_MAP = {
    "AcDbBlockReference": "IAcadBlockReference",
    "AcDbMInsertBlock": "IAcadMInsertBlock",
}

FRAME_FILE_BY_PLOT_NAME = {
    "A0": "A0.dwg",
    "A0+1/8": "A0_1_8.dwg",
    "A0+1/4": "A0_1_4.dwg",
    "A1": "A1.dwg",
    "A1+1/4": "A1_1_4.dwg",
    "A1+1/2": "A1_1_2.dwg",
    "A1+3/4": "A1_3_4.dwg",
    "A2": "A2.dwg",
    "A2+1/4": "A2_1_4.dwg",
    "A2+1/2": "A2_1_2.dwg",
    "A2+3/4": "A2_3_4.dwg",
    "A3": "A3.dwg",
}

FRAME_TEMPLATE_BOUNDS = {
    "A0": {
        "outer": (0.0, 0.0, 118900.0, 84100.0),
        "inner": (2500.0, 1000.0, 117900.0, 83100.0),
    },
    "A0+1/8": {
        "outer": (0.0, 0.0, 133800.0, 84100.0),
        "inner": (2500.0, 1000.0, 132800.0, 83100.0),
    },
    "A0+1/4": {
        "outer": (0.0, 0.0, 148600.0, 84100.0),
        "inner": (2500.0, 1000.0, 147600.0, 83100.0),
    },
    "A1": {
        "outer": (0.0, 0.0, 84100.0, 59400.0),
        "inner": (2500.0, 1000.0, 83100.0, 58400.0),
    },
    "A1+1/4": {
        "outer": (0.0, 0.0, 105100.0, 59400.0),
        "inner": (2500.0, 1000.0, 104100.0, 58400.0),
    },
    "A1+1/2": {
        "outer": (0.0, 0.0, 126100.0, 59400.0),
        "inner": (2500.0, 1000.0, 125100.0, 58400.0),
    },
    "A1+3/4": {
        "outer": (0.0, 0.0, 147100.0, 59400.0),
        "inner": (2500.0, 1000.0, 146100.0, 58400.0),
    },
    "A2": {
        "outer": (0.0, 0.0, 59400.0, 42000.0),
        "inner": (2500.0, 1000.0, 58400.0, 41000.0),
    },
    "A2+1/4": {
        "outer": (0.0, 0.0, 74300.0, 42000.0),
        "inner": (2500.0, 1000.0, 73300.0, 41000.0),
    },
    "A2+1/2": {
        "outer": (0.0, 0.0, 89100.0, 42000.0),
        "inner": (2500.0, 1000.0, 88100.0, 41000.0),
    },
    "A2+3/4": {
        "outer": (0.0, 0.0, 104100.0, 42000.0),
        "inner": (2500.0, 1000.0, 103100.0, 41000.0),
    },
    "A3": {
        "outer": (0.0, 0.0, 42000.0, 29700.0),
        "inner": (2500.0, 500.0, 41500.0, 29200.0),
    },
}

TITLE_TEMPLATE_BOUNDS = {
    "A0": {"file": "A0_H.dwg", "block": "A0", "bbox": (-7000.0, 0.0, 0.0, 82100.0)},
    "A1": {"file": "A1_H.dwg", "block": "A1", "bbox": (-7000.0, 0.0, 20.832, 57400.0)},
    "A2": {"file": "A2_H.dwg", "block": "A2", "bbox": (-7000.0, 0.0, 0.0, 40000.0)},
    "A3": {"file": "A3_H.dwg", "block": "A3", "bbox": (-7000.0, 0.0, 0.0, 28700.0)},
}
TITLE_TEMPLATE_FILES = ("A0_H.dwg", "A1_H.dwg", "A2_H.dwg", "A3_H.dwg")


@dataclass
class PrintAreaLabelResult:
    handle: str
    owner: str
    space_kind: str
    layout_name: str
    plot_name: str | None
    paper_code: str | None
    ratio: str | None
    orientation: str | None
    standard_match: bool
    frame_inserted: bool
    frame_already_present: bool
    title_inserted: bool
    title_already_present: bool
    inner_frame_bbox: tuple[float, float, float, float] | None
    status: str
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _service_root() -> Path:
    return Path(__file__).resolve().parent


def _frame_asset_dir() -> Path:
    return _service_root() / "standard_drawing_frame"


def _user_frame_dir() -> Path:
    return _service_root() / "user_frame"


def _ensure_user_title_frame_assets() -> dict[str, Any]:
    user_dir = _user_frame_dir()
    user_dir.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    available: list[str] = []
    for filename in TITLE_TEMPLATE_FILES:
        target = user_dir / filename
        if not target.exists():
            source = _frame_asset_dir() / filename
            if not source.exists():
                raise FileNotFoundError(f"缺少标准图签模板文件: {source}")
            shutil.copy2(source, target)
            copied.append(filename)
        available.append(str(target))

    return {"directory": str(user_dir), "available": available, "copied_defaults": copied}


def _clear_user_title_frame_assets() -> list[str]:
    user_dir = _user_frame_dir()
    if not user_dir.exists():
        return []

    _close_title_asset_documents()

    removed: list[str] = []
    for entry in user_dir.iterdir():
        if entry.is_dir():
            shutil.rmtree(entry, ignore_errors=True)
            removed.append(entry.name)
            continue
        last_error = None
        for _ in range(5):
            try:
                entry.unlink()
                removed.append(entry.name)
                last_error = None
                break
            except FileNotFoundError:
                last_error = None
                break
            except PermissionError as exc:
                last_error = exc
                time.sleep(0.4)
        if last_error is not None:
            raise last_error
    return removed


def _normalize_mode(mode: str | None) -> str:
    normalized = str(mode or DEFAULT_MATCH_MODE).strip().lower().replace("-", "_")
    if normalized not in SUPPORTED_MATCH_MODES:
        raise ValueError(f"不支持的打印区域匹配模式: {mode}")
    return normalized


def _family_from_plot_name(plot_name: str) -> str:
    family = str(plot_name).split("+", 1)[0].strip()
    if family not in TITLE_TEMPLATE_BOUNDS:
        raise ValueError(f"不支持的图签家族: {plot_name}")
    return family


def _guard_checkpoint(checkpoint: str) -> None:
    try:
        decision = assert_runtime_guard_ok(checkpoint)
    except RuntimeGuardTriggered as exc:
        payload = render_guard_error(exc)
        sys_logger.error("[runtime_guard] %s", payload)
        raise RuntimeError(f"runtime guard blocked at {checkpoint}: {payload}") from exc

    sys_logger.info(
        "[runtime_guard] checkpoint=%s status=%s action=%s",
        checkpoint,
        decision.status,
        decision.recommended_action,
    )


def _point_variant(point: Iterable[float]) -> Any:
    return win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8,
        tuple(float(v) for v in point),
    )


def _dispatch_variant(objects: Sequence[Any]) -> Any:
    return win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH,
        tuple(objects),
    )


def _double_array_variant(values: Sequence[float]) -> Any:
    return win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8,
        tuple(float(v) for v in values),
    )


@retry_if_busy(max_retries=8, delay=0.6)
def _open_document(path: Path) -> Any:
    if not open_file(str(path)):
        raise RuntimeError(f"打开 DWG 失败: {path}")
    wait_quiescent(min_quiet=0.8, timeout=30.0)
    return C.raw_doc


@retry_if_busy(max_retries=8, delay=0.6)
def _collection_count(collection: Any) -> int:
    return int(getattr(collection, "Count", 0) or 0)


@retry_if_busy(max_retries=8, delay=0.6)
def _collection_item(collection: Any, index: int) -> Any:
    return collection.Item(index)


@retry_if_busy(max_retries=8, delay=0.6)
def _insert_block_reference(
    owner_space: Any,
    block_name_or_path: str,
    insertion_point: Sequence[float],
    scale: Sequence[float],
    rotation: float,
) -> Any:
    return owner_space.InsertBlock(
        _point_variant(insertion_point),
        str(block_name_or_path),
        float(scale[0]),
        float(scale[1]),
        float(scale[2]),
        float(rotation),
    )


@retry_if_busy(max_retries=8, delay=0.6)
def _move_entity(entity: Any, from_point: Sequence[float], to_point: Sequence[float]) -> bool:
    entity.Move(_point_variant(from_point), _point_variant(to_point))
    return True


@retry_if_busy(max_retries=8, delay=0.6)
def _scale_entity_uniform(entity: Any, base_point: Sequence[float], factor: float) -> bool:
    entity.ScaleEntity(_point_variant(base_point), float(factor))
    return True


@retry_if_busy(max_retries=8, delay=0.6)
def _delete_entity(entity: Any) -> bool:
    entity.Delete()
    return True


@retry_if_busy(max_retries=8, delay=0.6)
def _save_document(doc: Any) -> bool:
    doc.Save()
    return True


@retry_if_busy(max_retries=8, delay=0.6)
def _set_entity_layer(entity: Any, layer_name: str) -> bool:
    entity.Layer = str(layer_name)
    return True


@retry_if_busy(max_retries=8, delay=0.6)
def _set_polyline_constant_width(entity: Any, width: float) -> bool:
    target = float(width)
    try:
        entity.ConstantWidth = target
    except Exception:
        pass

    for index in range(4):
        try:
            entity.SetWidth(index, target, target)
        except Exception:
            continue
    return True


@retry_if_busy(max_retries=8, delay=0.6)
def _create_block_definition(doc: Any, base_point: Sequence[float], block_name: str) -> Any:
    return doc.Blocks.Add(_point_variant(base_point), block_name)


@retry_if_busy(max_retries=8, delay=0.6)
def _copy_entities_to_owner(source_doc: Any, entities: Sequence[Any], owner: Any) -> Any:
    return source_doc.CopyObjects(_dispatch_variant(entities), owner)


@retry_if_busy(max_retries=8, delay=0.6)
def _get_block_definition(doc: Any, block_name: str) -> Any:
    return doc.Blocks.Item(block_name)


def _block_exists(doc: Any, block_name: str) -> bool:
    try:
        _get_block_definition(doc, block_name)
        return True
    except Exception:
        return False


def _entity_color_index(entity: Any) -> int | None:
    try:
        return int(entity.TrueColor.ColorIndex)
    except Exception:
        pass
    for attr_name in ("Color", "ColorIndex"):
        try:
            return int(getattr(entity, attr_name))
        except Exception:
            continue
    return None


def _float_list(values: Any) -> list[float]:
    try:
        return [round(float(item), 6) for item in values]
    except Exception:
        return []


def _entity_fingerprint_payload(entity: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "object_name": str(getattr(entity, "ObjectName", "") or ""),
        "layer": str(getattr(entity, "Layer", "") or ""),
        "color_index": _entity_color_index(entity),
    }

    bbox = _bbox_xy(entity)
    if bbox is not None:
        payload["bbox"] = [round(value, 6) for value in bbox]

    simple_props = {
        "name": "Name",
        "effective_name": "EffectiveName",
        "text": "TextString",
        "tag": "TagString",
        "prompt": "PromptString",
        "closed": "Closed",
        "rotation": "Rotation",
        "radius": "Radius",
        "height": "Height",
        "constant_width": "ConstantWidth",
        "thickness": "Thickness",
    }
    for key, attr_name in simple_props.items():
        try:
            value = getattr(entity, attr_name)
        except Exception:
            continue
        if value in (None, ""):
            continue
        if isinstance(value, (int, float, bool)):
            payload[key] = round(float(value), 6) if isinstance(value, float) else value
        else:
            payload[key] = str(value)

    point_props = {
        "insertion_point": "InsertionPoint",
        "origin": "Origin",
        "center": "Center",
        "start_point": "StartPoint",
        "end_point": "EndPoint",
        "alignment_point": "AlignmentPoint",
    }
    for key, attr_name in point_props.items():
        try:
            value = getattr(entity, attr_name)
        except Exception:
            continue
        point = _float_list(value)
        if point:
            payload[key] = point

    for key, attr_name in {
        "coordinates": "Coordinates",
        "normal": "Normal",
        "scale_factors": "ScaleFactors",
    }.items():
        try:
            value = getattr(entity, attr_name)
        except Exception:
            continue
        items = _float_list(value)
        if items:
            payload[key] = items

    return payload


def _title_block_profile(block_def: Any) -> dict[str, Any]:
    entity_payloads: list[dict[str, Any]] = []
    color_indexes: set[int] = set()
    defpoints_polyline_count = 0
    total = _collection_count(block_def)
    for idx in range(total):
        entity = _collection_item(block_def, idx)
        payload = _entity_fingerprint_payload(entity)
        entity_payloads.append(payload)

        if payload.get("object_name") not in {
            "AcDbPolyline",
            "AcDb2dPolyline",
            "AcDb3dPolyline",
            "Polyline",
            "LWPOLYLINE",
        }:
            continue
        if str(payload.get("layer") or "").lower() != "defpoints":
            continue
        defpoints_polyline_count += 1
        color_index = payload.get("color_index")
        if isinstance(color_index, int):
            color_indexes.add(color_index)

    entity_payloads.sort(key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True))
    digest = hashlib.sha1(
        json.dumps(entity_payloads, ensure_ascii=False, sort_keys=True).encode("utf-8", errors="ignore")
    ).hexdigest()
    return {
        "digest": digest,
        "entity_count": len(entity_payloads),
        "defpoints_polyline_count": defpoints_polyline_count,
        "color_indexes": sorted(color_indexes),
        "has_signature": defpoints_polyline_count >= 2 and 1 in color_indexes and 3 in color_indexes,
    }


def _block_has_title_signature(block_def: Any) -> bool:
    return bool(_title_block_profile(block_def)["has_signature"])


def _activate_document(doc: Any) -> None:
    try:
        doc.Activate()
    except Exception:
        pass


def _safe_regen(doc: Any) -> None:
    try:
        doc.Regen(1)
    except Exception:
        pass


def _normalize_doc_identity(path_or_name: str | Path | None) -> str:
    if path_or_name is None:
        return ""
    text = str(path_or_name).strip()
    if not text:
        return ""
    normalized = os.path.normcase(os.path.abspath(text))
    try:
        normalized = os.path.normcase(os.path.abspath(os.path.realpath(normalized)))
    except Exception:
        pass
    return normalized


def _iter_open_documents() -> Iterable[Any]:
    docs = None
    for attr_name in ("acad", "app"):
        try:
            app = getattr(C, attr_name)
        except Exception:
            app = None
        if app is None:
            continue
        try:
            docs = app.Documents
            break
        except Exception:
            continue

    if docs is None:
        return

    total = _collection_count(docs)
    for idx in range(total):
        try:
            yield _collection_item(docs, idx)
        except Exception:
            continue


@retry_if_busy(max_retries=8, delay=0.6)
def _close_document(doc: Any, *, save_changes: bool = False) -> bool:
    doc.Close(bool(save_changes))
    return True


def _close_document_by_identity(path_or_name: str | Path, *, save_changes: bool = False) -> bool:
    wanted = _normalize_doc_identity(path_or_name)
    wanted_name = Path(str(path_or_name)).name.lower()
    closed = False

    for doc in list(_iter_open_documents() or []):
        doc_name = str(getattr(doc, "Name", "") or "")
        doc_full_name = str(getattr(doc, "FullName", "") or "")
        if not doc_name and not doc_full_name:
            continue
        same_doc = False
        if doc_full_name and wanted and _normalize_doc_identity(doc_full_name) == wanted:
            same_doc = True
        elif doc_name and doc_name.lower() == wanted_name:
            same_doc = True
        if not same_doc:
            continue
        try:
            _close_document(doc, save_changes=save_changes)
            closed = True
        except Exception:
            continue
    return closed


def _close_title_asset_documents() -> list[str]:
    closed: list[str] = []
    for filename in TITLE_TEMPLATE_FILES:
        asset_path = _user_frame_dir() / filename
        if _close_document_by_identity(asset_path, save_changes=False):
            closed.append(filename)
    return closed


def _owner_space(entity: Any) -> Any:
    return C.doc.ObjectIdToObject(entity.OwnerID)


def _owner_space_name(entity: Any) -> str:
    try:
        return str(_owner_space(entity).Name)
    except Exception:
        return "<unknown>"


def _bbox_xy(entity: Any) -> tuple[float, float, float, float] | None:
    try:
        ll, ur = entity.GetBoundingBox()
        minx, miny = float(ll[0]), float(ll[1])
        maxx, maxy = float(ur[0]), float(ur[1])
        if minx > maxx:
            minx, maxx = maxx, minx
        if miny > maxy:
            miny, maxy = maxy, miny
        return (minx, miny, maxx, maxy)
    except Exception:
        return None


def _bbox_dimensions(bbox: tuple[float, float, float, float]) -> tuple[float, float]:
    minx, miny, maxx, maxy = bbox
    return (abs(maxx - minx), abs(maxy - miny))


def _bbox_area(bbox: tuple[float, float, float, float]) -> float:
    width, height = _bbox_dimensions(bbox)
    return width * height


def _bbox_close(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
    *,
    tol: float,
) -> bool:
    return all(abs(a - b) <= tol for a, b in zip(first, second))


def _orientation_from_bbox(bbox: tuple[float, float, float, float]) -> int:
    width, height = _bbox_dimensions(bbox)
    return 0 if width >= height else 1


def _adaptive_spec_from_bbox(bbox: tuple[float, float, float, float]) -> str:
    width, height = _bbox_dimensions(bbox)
    short_side = min(width, height)
    long_side = max(width, height)
    best_name = None
    best_score = None
    for spec_name, dims in FRAME_TEMPLATE_BOUNDS.items():
        base_width, base_height = _bbox_dimensions(dims["outer"])
        base_short = min(base_width, base_height)
        base_long = max(base_width, base_height)
        score = abs(short_side - base_short) / max(base_short, 1.0) + abs(long_side - base_long) / max(base_long, 1.0)
        if best_name is None or score < best_score:
            best_name = spec_name
            best_score = score
    return str(best_name)


def _layout_name_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    try:
        for layout in C.doc.Layouts:
            try:
                mapping[str(layout.Block.Name)] = str(layout.Name)
            except Exception:
                continue
    except Exception as exc:
        sys_logger.warning("[illustration_label] 解析布局/BTR 映射失败: %s", exc)
    return mapping


def _owner_space_kind(owner_name: str) -> str:
    return "model" if str(owner_name).upper() == MODEL_SPACE_OWNER else "layout"


def _owner_layout_name(owner_name: str, layout_map: dict[str, str] | None = None) -> str:
    layout_map = layout_map or {}
    if str(owner_name).upper() == MODEL_SPACE_OWNER:
        return MODEL_LAYOUT_NAME
    return layout_map.get(str(owner_name), str(owner_name))


def _requested_layouts(only_layouts: Sequence[str] | None) -> set[str]:
    return {str(name).strip().lower() for name in (only_layouts or []) if str(name).strip()}


def _owner_selected(
    owner_name: str,
    *,
    include_model: bool,
    include_layouts: bool,
    only_layouts: set[str],
    layout_map: dict[str, str],
) -> bool:
    if _owner_space_kind(owner_name) == "model":
        return include_model
    if not include_layouts:
        return False
    if not only_layouts:
        return True
    return _owner_layout_name(owner_name, layout_map).lower() in only_layouts


def _contains_bbox(
    outer: tuple[float, float, float, float],
    inner: tuple[float, float, float, float],
    *,
    tol: float,
) -> bool:
    ox1, oy1, ox2, oy2 = outer
    ix1, iy1, ix2, iy2 = inner
    return ox1 <= ix1 + tol and oy1 <= iy1 + tol and ox2 >= ix2 - tol and oy2 >= iy2 - tol


def _bbox_point(bbox: tuple[float, float, float, float], anchor: str) -> tuple[float, float]:
    minx, miny, maxx, maxy = bbox
    if anchor == "lb":
        return (minx, miny)
    if anchor == "rb":
        return (maxx, miny)
    if anchor == "lt":
        return (minx, maxy)
    if anchor == "rt":
        return (maxx, maxy)
    raise ValueError(f"不支持的锚点: {anchor}")


def _move_bbox(
    bbox: tuple[float, float, float, float],
    dx: float,
    dy: float,
) -> tuple[float, float, float, float]:
    minx, miny, maxx, maxy = bbox
    return (minx + dx, miny + dy, maxx + dx, maxy + dy)


def _rect_polyline_coords(bbox: tuple[float, float, float, float]) -> list[float]:
    minx, miny, maxx, maxy = bbox
    return [minx, miny, maxx, miny, maxx, maxy, minx, maxy]


@retry_if_busy(max_retries=8, delay=0.6)
def _add_rectangle_polyline(owner_space: Any, bbox: tuple[float, float, float, float]) -> Any:
    poly = owner_space.AddLightWeightPolyline(_double_array_variant(_rect_polyline_coords(bbox)))
    poly.Closed = True
    return poly


def _transform_point(x: float, y: float, *, scale_x: float, scale_y: float, rotation: float) -> tuple[float, float]:
    sx = x * scale_x
    sy = y * scale_y
    if abs(rotation) < 1e-9:
        return (sx, sy)
    if abs(rotation - PORTRAIT_ROTATION) < 1e-9:
        return (sy, -sx)
    raise ValueError(f"当前仅支持旋转 0 或 -90°，收到: {rotation}")


def _transform_bbox(
    bbox: tuple[float, float, float, float],
    *,
    scale_x: float,
    scale_y: float,
    rotation: float,
) -> tuple[float, float, float, float]:
    minx, miny, maxx, maxy = bbox
    corners = [
        _transform_point(minx, miny, scale_x=scale_x, scale_y=scale_y, rotation=rotation),
        _transform_point(minx, maxy, scale_x=scale_x, scale_y=scale_y, rotation=rotation),
        _transform_point(maxx, miny, scale_x=scale_x, scale_y=scale_y, rotation=rotation),
        _transform_point(maxx, maxy, scale_x=scale_x, scale_y=scale_y, rotation=rotation),
    ]
    xs = [p[0] for p in corners]
    ys = [p[1] for p in corners]
    return (min(xs), min(ys), max(xs), max(ys))


def _space_rectangles_by_owner_name() -> dict[str, list[Any]]:
    polylines = select_all_polylines(autocast=True)
    grouped = get_rect_polylines_by_space(polylines)
    out = {"*model_space": list(grouped.get("model", []))}
    for key, values in (grouped.get("papers") or {}).items():
        out[str(key).lower()] = list(values or [])
    return out


def _reasonable_adaptive_candidates_by_owner() -> dict[str, list[Any]]:
    out: dict[str, list[Any]] = {}
    for poly in select_all_polylines(autocast=True):
        ok, info = is_rectangular_polyline(poly)
        if not ok:
            if info.get("reason") != "xy_clusters_not2":
                continue
            x_clusters = list(info.get("x_clusters") or [])
            y_clusters = list(info.get("y_clusters") or [])
            if info.get("n_unique_pts") != 4:
                continue
            if not ((len(x_clusters) == 2 and len(y_clusters) == 3) or (len(x_clusters) == 3 and len(y_clusters) == 2)):
                continue
        try:
            owner_name = _owner_space_name(poly).lower()
        except Exception:
            continue
        out.setdefault(owner_name, []).append(poly)
    return out


def _iter_entities(owner_space: Any) -> Iterable[Any]:
    total = _collection_count(owner_space)
    for idx in range(total):
        yield _collection_item(owner_space, idx)


def _safe_handle(entity: Any) -> str:
    try:
        return str(getattr(entity, "Handle", "") or "")
    except Exception:
        return ""


def _collect_block_entities(block_def: Any) -> list[Any]:
    total = _collection_count(block_def)
    return [_collection_item(block_def, idx) for idx in range(total)]


def _as_block_reference(entity: Any) -> Any | None:
    obj_name = str(getattr(entity, "ObjectName", "") or "")
    iface = _BLOCK_REF_CAST_MAP.get(obj_name)
    if not iface:
        return None
    try:
        return win32com.client.CastTo(entity, iface)
    except Exception:
        return entity


def _is_entity_alive(entity: Any) -> bool:
    try:
        _ = entity.Layer
        return True
    except Exception:
        return False


def _explode_and_delete_block_ref(block_ref: Any) -> list[Any] | None:
    try:
        owner_space = block_ref.Document.ObjectIdToObject(block_ref.OwnerID)
    except Exception as exc:
        raise RuntimeError("无法定位图框块引用所属空间") from exc

    count_before = 0
    try:
        count_before = _collection_count(owner_space)
    except Exception:
        count_before = 0

    handle = _safe_handle(block_ref)
    exploded = None
    try:
        exploded = list(block_ref.Explode() or [])
    except Exception as exc:
        raise RuntimeError(f"图框块炸开失败: {exc}") from exc

    wait_quiescent(min_quiet=0.2, timeout=10.0)
    if _is_entity_alive(block_ref):
        _delete_entity(block_ref)
        wait_quiescent(min_quiet=0.2, timeout=10.0)

    if exploded:
        return exploded

    if _is_entity_alive(block_ref):
        return None

    try:
        count_after = _collection_count(owner_space)
    except Exception:
        return []

    recovered: list[Any] = []
    start_index = max(0, count_before - 1)
    for idx in range(start_index, count_after):
        try:
            candidate = _collection_item(owner_space, idx)
        except Exception:
            continue
        if handle and _safe_handle(candidate) == handle:
            continue
        recovered.append(candidate)
    return recovered


def _needs_polyline_rebuild_after_explode(scale_x: float, scale_y: float, *, tol: float = 1e-6) -> bool:
    return abs(scale_x - 1.0) > tol or abs(scale_y - 1.0) > tol


def _restore_frame_polylines_after_scaled_explode(
    owner_space: Any,
    exploded_entities: Sequence[Any] | None,
    *,
    outer_bbox: tuple[float, float, float, float],
    inner_bbox: tuple[float, float, float, float],
    scale_x: float,
    scale_y: float,
) -> None:
    if not _needs_polyline_rebuild_after_explode(scale_x, scale_y):
        return

    geometry_entities: list[Any] = []
    geometry_layer = ""
    for entity in exploded_entities or []:
        if not _is_entity_alive(entity):
            continue
        obj_name = str(getattr(entity, "ObjectName", "") or "")
        if obj_name in _BLOCK_REF_CAST_MAP:
            continue
        geometry_entities.append(entity)
        if not geometry_layer:
            try:
                geometry_layer = str(getattr(entity, "Layer", "") or "")
            except Exception:
                geometry_layer = ""

    if not geometry_entities:
        return

    for entity in geometry_entities:
        _safe_delete(entity)
    wait_quiescent(min_quiet=0.2, timeout=10.0)

    outer_poly = _add_rectangle_polyline(owner_space, outer_bbox)
    inner_poly = _add_rectangle_polyline(owner_space, inner_bbox)
    if geometry_layer:
        _set_entity_layer(outer_poly, geometry_layer)
        _set_entity_layer(inner_poly, geometry_layer)

    _set_polyline_constant_width(outer_poly, 0.0)
    _set_polyline_constant_width(inner_poly, min(scale_x, scale_y) * 100.0)
    wait_quiescent(min_quiet=0.2, timeout=10.0)


def _scale_for_outer_bbox(
    plot_name: str,
    target_bbox: tuple[float, float, float, float],
    orient: int,
) -> tuple[float, float, float]:
    outer_bbox = FRAME_TEMPLATE_BOUNDS[plot_name]["outer"]
    src_width, src_height = _bbox_dimensions(outer_bbox)
    target_width, target_height = _bbox_dimensions(target_bbox)
    if orient == 0:
        return (target_width / src_width, target_height / src_height, 0.0)
    return (target_height / src_width, target_width / src_height, PORTRAIT_ROTATION)


def _scale_from_inner_bbox(
    plot_name: str,
    target_inner_bbox: tuple[float, float, float, float],
    orient: int,
) -> tuple[float, float]:
    src_inner_bbox = FRAME_TEMPLATE_BOUNDS[plot_name]["inner"]
    src_width, src_height = _bbox_dimensions(src_inner_bbox)
    target_width, target_height = _bbox_dimensions(target_inner_bbox)
    if orient == 0:
        return (target_width / src_width, target_height / src_height)
    return (target_height / src_width, target_width / src_height)


def _best_inner_frame_candidate(
    print_area: Any,
    same_space_rectangles: Sequence[Any],
    *,
    min_ratio: float = INNER_FRAME_RATIO_THRESHOLD,
) -> tuple[Any, tuple[float, float, float, float]] | None:
    outer_bbox = _bbox_xy(print_area)
    if outer_bbox is None:
        return None

    outer_area = max(_bbox_area(outer_bbox), 1e-9)
    width, height = _bbox_dimensions(outer_bbox)
    tol = max(min(width, height) * 0.001, 1.0)
    outer_handle = _safe_handle(print_area)

    best: tuple[Any, tuple[float, float, float, float]] | None = None
    best_ratio = 0.0
    for poly in same_space_rectangles:
        if _safe_handle(poly) == outer_handle:
            continue
        bbox = _bbox_xy(poly)
        if bbox is None or not _contains_bbox(outer_bbox, bbox, tol=tol):
            continue
        area_ratio = _bbox_area(bbox) / outer_area
        if area_ratio >= 0.999 or area_ratio < min_ratio:
            continue
        if area_ratio > best_ratio:
            best = (poly, bbox)
            best_ratio = area_ratio
    return best


def _filter_outer_print_area_candidates(polylines: Sequence[Any]) -> list[Any]:
    data: list[dict[str, Any]] = []
    for poly in polylines:
        bbox = _bbox_xy(poly)
        if bbox is None:
            continue
        data.append(
            {
                "obj": poly,
                "bbox": bbox,
                "area": max(_bbox_area(bbox), 1e-9),
                "removed": False,
            }
        )

    for idx, current in enumerate(data):
        if current["removed"]:
            continue
        for jdx, other in enumerate(data):
            if idx == jdx or other["removed"]:
                continue
            if other["area"] <= current["area"]:
                continue
            tol = max(min(_bbox_dimensions(current["bbox"])), 1.0) * 0.001
            if not _contains_bbox(other["bbox"], current["bbox"], tol=tol):
                continue
            if current["area"] / other["area"] > INNER_FRAME_RATIO_THRESHOLD:
                current["removed"] = True
                break

    return [item["obj"] for item in data if not item["removed"]]


def _safe_delete(entity: Any) -> bool:
    try:
        _delete_entity(entity)
        return True
    except Exception:
        return False


def _rect_polylines_in_owner_space(owner_space: Any) -> list[Any]:
    rectangles: list[Any] = []
    for entity in _iter_entities(owner_space):
        ok, _ = is_rectangular_polyline(entity)
        if ok:
            rectangles.append(entity)
    return rectangles


def _remove_duplicate_polylines(
    polylines: Sequence[Any],
    *,
    tol: float = 1.0,
    priority_layer: str = "dy_zhuanyong",
) -> list[Any]:
    cached_data: list[dict[str, Any]] = []
    priority_layer_lower = str(priority_layer).lower()

    for pl in polylines:
        bbox = _bbox_xy(pl)
        if bbox is None:
            continue
        try:
            layer = str(getattr(pl, "Layer", "") or "").lower()
        except Exception:
            layer = ""
        cached_data.append(
            {
                "obj": pl,
                "bbox": bbox,
                "layer": layer,
                "removed": False,
            }
        )

    cached_data.sort(key=lambda item: item["bbox"][0])

    removed_count = 0
    for idx, current in enumerate(cached_data):
        if current["removed"]:
            continue
        for jdx in range(idx + 1, len(cached_data)):
            candidate = cached_data[jdx]
            if candidate["removed"]:
                continue
            if candidate["bbox"][0] - current["bbox"][0] > tol:
                break

            is_duplicate = _bbox_close(current["bbox"], candidate["bbox"], tol=tol)
            if not is_duplicate:
                continue

            curr_weight = 1 if current["layer"] == priority_layer_lower else 0
            cand_weight = 1 if candidate["layer"] == priority_layer_lower else 0
            if curr_weight >= cand_weight:
                candidate["removed"] = True
                if _safe_delete(candidate["obj"]):
                    removed_count += 1
            else:
                current["removed"] = True
                if _safe_delete(current["obj"]):
                    removed_count += 1
                break

    survivors = [item["obj"] for item in cached_data if not item["removed"]]
    sys_logger.info(
        "[frame_dedupe] processed=%s removed=%s kept=%s",
        len(cached_data),
        removed_count,
        len(survivors),
    )
    return survivors


def _ensure_inner_frame_polyline(
    owner_space: Any,
    target_inner_bbox: tuple[float, float, float, float],
) -> None:
    minx, miny, maxx, maxy = target_inner_bbox
    width, height = _bbox_dimensions(target_inner_bbox)
    tol = max(min(width, height) * 0.001, 1.0)

    for entity in _iter_entities(owner_space):
        ok, _ = is_rectangular_polyline(entity)
        if not ok:
            continue
        bbox = _bbox_xy(entity)
        if bbox is None:
            continue
        if _bbox_close(bbox, target_inner_bbox, tol=tol):
            return

    poly = owner_space.AddLightWeightPolyline(
        _double_array_variant([minx, miny, maxx, miny, maxx, maxy, minx, maxy])
    )
    poly.Closed = True


def _dedupe_rectangles_in_owner_space(
    owner_space: Any,
    *,
    tol: float = 1.0,
    priority_layer: str = "dy_zhuanyong",
) -> list[Any]:
    rectangles = _rect_polylines_in_owner_space(owner_space)
    if not rectangles:
        return []
    return _remove_duplicate_polylines(
        rectangles,
        tol=tol,
        priority_layer=priority_layer,
    )


def _align_block_ref_bbox(
    block_ref: Any,
    target_bbox: tuple[float, float, float, float],
    *,
    anchor: str,
) -> tuple[float, float, float, float]:
    current_bbox = _bbox_xy(block_ref)
    if current_bbox is None:
        raise RuntimeError("无法获取插入块的包围盒")
    source_anchor = _bbox_point(current_bbox, anchor)
    target_anchor = _bbox_point(target_bbox, anchor)
    dx = target_anchor[0] - source_anchor[0]
    dy = target_anchor[1] - source_anchor[1]
    if abs(dx) > 1e-9 or abs(dy) > 1e-9:
        _move_entity(block_ref, (0.0, 0.0, 0.0), (dx, dy, 0.0))
        wait_quiescent(min_quiet=0.3, timeout=20.0)
    updated_bbox = _bbox_xy(block_ref)
    if updated_bbox is None:
        raise RuntimeError("块移动后无法读取包围盒")
    return updated_bbox


def _insert_frame_geometry(
    owner_space: Any,
    original_print_area: Any,
    plot_name: str,
    target_outer_bbox: tuple[float, float, float, float],
    orient: int,
) -> tuple[tuple[float, float, float, float], tuple[float, float]]:
    frame_file = _frame_asset_dir() / FRAME_FILE_BY_PLOT_NAME[plot_name]
    if not frame_file.exists():
        raise FileNotFoundError(f"找不到标准图框文件: {frame_file}")

    scale_x, scale_y, rotation = _scale_for_outer_bbox(plot_name, target_outer_bbox, orient)
    template_outer_bbox = FRAME_TEMPLATE_BOUNDS[plot_name]["outer"]
    raw_outer_bbox = _transform_bbox(
        template_outer_bbox,
        scale_x=scale_x,
        scale_y=scale_y,
        rotation=rotation,
    )
    block_ref = _insert_block_reference(
        owner_space,
        str(frame_file),
        (0.0, 0.0, 0.0),
        (scale_x, scale_y, 1.0),
        rotation,
    )
    wait_quiescent(min_quiet=0.3, timeout=20.0)

    anchor = "rb" if orient == 0 else "lb"
    _align_block_ref_bbox(block_ref, target_outer_bbox, anchor=anchor)
    raw_anchor = _bbox_point(raw_outer_bbox, anchor)
    target_anchor = _bbox_point(target_outer_bbox, anchor)
    dx = target_anchor[0] - raw_anchor[0]
    dy = target_anchor[1] - raw_anchor[1]

    template_inner_bbox = FRAME_TEMPLATE_BOUNDS[plot_name]["inner"]
    transformed_inner = _transform_bbox(
        template_inner_bbox,
        scale_x=scale_x,
        scale_y=scale_y,
        rotation=rotation,
    )
    target_inner_bbox = _move_bbox(transformed_inner, dx=dx, dy=dy)

    _delete_entity(original_print_area)
    wait_quiescent(min_quiet=0.2, timeout=10.0)

    exploded = _explode_and_delete_block_ref(block_ref)
    if exploded is None:
        raise RuntimeError("标准图框炸开失败")
    _restore_frame_polylines_after_scaled_explode(
        owner_space,
        exploded,
        outer_bbox=target_outer_bbox,
        inner_bbox=target_inner_bbox,
        scale_x=scale_x,
        scale_y=scale_y,
    )
    wait_quiescent(min_quiet=0.3, timeout=20.0)

    return (target_inner_bbox, (scale_x, scale_y))


def _block_reference_name(entity: Any) -> str:
    block_ref = _as_block_reference(entity) or entity
    for attr_name in ("EffectiveName", "Name"):
        try:
            value = str(getattr(block_ref, attr_name, "") or "")
        except Exception:
            value = ""
        if value:
            return value
    return ""


def _is_block_reference(entity: Any) -> bool:
    return str(getattr(entity, "ObjectName", "") or "") in {"AcDbBlockReference", "AcDbMInsertBlock"}


def _find_existing_title_block(
    owner_space: Any,
    family: str,
    target_inner_bbox: tuple[float, float, float, float],
    orient: int,
) -> Any | None:
    inner_width, inner_height = _bbox_dimensions(target_inner_bbox)
    tol = max(min(inner_width, inner_height) * 0.01, 20.0)
    target_anchor = _bbox_point(target_inner_bbox, "rb" if orient == 0 else "lb")

    for entity in _iter_entities(owner_space):
        if not _is_block_reference(entity):
            continue
        if _block_reference_name(entity) != TITLE_TEMPLATE_BOUNDS[family]["block"]:
            continue
        bbox = _bbox_xy(entity)
        if bbox is None:
            continue
        anchor = _bbox_point(bbox, "rb" if orient == 0 else "lb")
        if abs(anchor[0] - target_anchor[0]) > tol or abs(anchor[1] - target_anchor[1]) > tol:
            continue
        return entity
    return None


def _resolve_title_asset_path(family: str) -> Path:
    _ensure_user_title_frame_assets()
    asset = _user_frame_dir() / TITLE_TEMPLATE_BOUNDS[family]["file"]
    if not asset.exists():
        raise FileNotFoundError(f"找不到图签文件: {asset}")
    return asset


def _assert_title_block_matches_asset(
    block_def: Any,
    *,
    family: str,
    stage: str,
    asset_path: Path,
    expected_profile: dict[str, Any],
) -> dict[str, Any]:
    expected_digest = str(expected_profile.get("digest") or expected_profile.get("source_digest") or "").strip()
    if not expected_digest:
        raise RuntimeError(f"{stage} 缺少图签模板指纹: family={family} asset={asset_path}")
    actual_profile = _title_block_profile(block_def)
    if not actual_profile["has_signature"]:
        raise RuntimeError(
            f"{stage} 图签块定义缺少指定模板特征: family={family} block={TITLE_TEMPLATE_BOUNDS[family]['block']} "
            f"asset={asset_path} defpoints={actual_profile['defpoints_polyline_count']} colors={actual_profile['color_indexes']}"
        )
    if actual_profile["digest"] != expected_digest:
        raise RuntimeError(
            f"{stage} 图签块定义与指定模板不一致: family={family} block={TITLE_TEMPLATE_BOUNDS[family]['block']} "
            f"asset={asset_path} expected={expected_digest} actual={actual_profile['digest']}"
        )
    return actual_profile


def _ensure_single_title_block_definition(
    target_doc: Any,
    *,
    family: str,
) -> dict[str, Any]:
    asset_path = _resolve_title_asset_path(family)
    block_name = TITLE_TEMPLATE_BOUNDS[family]["block"]
    source_doc = _open_document(asset_path)
    try:
        source_block = _get_block_definition(source_doc, block_name)
        source_profile = _title_block_profile(source_block)
        if not source_profile["has_signature"]:
            raise RuntimeError(
                f"图签源文件中的块定义不符合要求: {asset_path} -> {block_name} "
                f"defpoints={source_profile['defpoints_polyline_count']} colors={source_profile['color_indexes']}"
            )

        action = "imported"
        if _block_exists(target_doc, block_name):
            replace_single_block_definition(
                source_doc,
                target_doc,
                block_name,
                run_attsync=False,
            )
            action = "replaced"
        else:
            source_entities = _collect_block_entities(source_block)
            if not source_entities:
                raise RuntimeError(f"图签源块定义为空: {asset_path} -> {block_name}")
            source_origin = tuple(float(v) for v in getattr(source_block, "Origin", (0.0, 0.0, 0.0)))
            new_block = _create_block_definition(target_doc, source_origin, block_name)
            _copy_entities_to_owner(source_doc, source_entities, new_block)
            wait_quiescent(min_quiet=0.5, timeout=20.0)

        target_block = _get_block_definition(target_doc, block_name)
        target_profile = _assert_title_block_matches_asset(
            target_block,
            family=family,
            stage="同步后",
            asset_path=asset_path,
            expected_profile=source_profile,
        )

        return {
            "family": family,
            "block_name": block_name,
            "asset_path": str(asset_path),
            "action": action,
            "digest": source_profile["digest"],
            "source_digest": source_profile["digest"],
            "target_digest": target_profile["digest"],
            "entity_count": target_profile["entity_count"],
            "defpoints_polyline_count": target_profile["defpoints_polyline_count"],
            "color_indexes": target_profile["color_indexes"],
        }
    finally:
        _close_document_by_identity(asset_path, save_changes=False)
        _activate_document(target_doc)
        wait_quiescent(min_quiet=0.3, timeout=15.0)


def _ensure_title_block_definitions(target_doc: Any) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for family in TITLE_TEMPLATE_BOUNDS:
        results.append(_ensure_single_title_block_definition(target_doc, family=family))
    return results


def _title_scale_factor_for_inner_bbox(
    inserted_bbox: tuple[float, float, float, float],
    target_inner_bbox: tuple[float, float, float, float],
    orient: int,
) -> float:
    inserted_width, inserted_height = _bbox_dimensions(inserted_bbox)
    target_width, target_height = _bbox_dimensions(target_inner_bbox)

    if orient == 0:
        basis = max(inserted_height, 1e-9)
        return target_height / basis

    basis = max(inserted_width, 1e-9)
    return target_width / basis


def _insert_title_block(
    owner_space: Any,
    plot_name: str,
    target_inner_bbox: tuple[float, float, float, float],
    orient: int,
    *,
    expected_profile: dict[str, Any],
) -> Any:
    family = _family_from_plot_name(plot_name)
    rotation = 0.0 if orient == 0 else PORTRAIT_ROTATION
    anchor = "rb" if orient == 0 else "lb"
    block_name = TITLE_TEMPLATE_BOUNDS[family]["block"]
    asset_path = Path(str(expected_profile.get("asset_path") or _resolve_title_asset_path(family)))

    block_def = _get_block_definition(owner_space.Document, block_name)
    _assert_title_block_matches_asset(
        block_def,
        family=family,
        stage="插入前",
        asset_path=asset_path,
        expected_profile=expected_profile,
    )

    block_ref = _insert_block_reference(
        owner_space,
        block_name,
        (0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0),
        rotation,
    )
    wait_quiescent(min_quiet=0.3, timeout=20.0)

    aligned_bbox = _align_block_ref_bbox(block_ref, target_inner_bbox, anchor=anchor)
    factor = _title_scale_factor_for_inner_bbox(aligned_bbox, target_inner_bbox, orient)
    if abs(factor - 1.0) > 1e-6:
        scale_base = _bbox_point(aligned_bbox, anchor)
        _scale_entity_uniform(block_ref, (scale_base[0], scale_base[1], 0.0), factor)
        wait_quiescent(min_quiet=0.3, timeout=20.0)
        _align_block_ref_bbox(block_ref, target_inner_bbox, anchor=anchor)
        wait_quiescent(min_quiet=0.3, timeout=20.0)

    inserted_name = _block_reference_name(block_ref)
    if inserted_name != block_name:
        raise RuntimeError(f"插入后的图签块名异常，期望 {block_name}，实际 {inserted_name or '<empty>'}")

    try:
        block_def = _get_block_definition(block_ref.Document, block_name)
    except Exception as exc:
        raise RuntimeError(f"无法读取插入图签块定义: {block_name}") from exc
    _assert_title_block_matches_asset(
        block_def,
        family=family,
        stage="插入后",
        asset_path=asset_path,
        expected_profile=expected_profile,
    )

    wait_quiescent(min_quiet=0.3, timeout=20.0)
    return block_ref


def _ensure_block_definitions_from_source(
    *,
    target_path: Path,
    source_path: Path,
    block_names: Sequence[str],
    ensure_guard: bool,
    run_attsync: bool,
) -> dict[str, Any]:
    prepare_cad_runtime(ensure_guard=ensure_guard)
    source_doc = _open_document(source_path)
    target_doc = _open_document(target_path)
    _activate_document(target_doc)

    results: list[dict[str, Any]] = []
    for block_name in block_names:
        if _block_exists(target_doc, block_name):
            result = replace_single_block_definition(
                source_doc,
                target_doc,
                block_name,
                run_attsync=run_attsync,
            ).to_dict()
            result["action"] = "replaced"
            results.append(result)
            continue

        source_block = _get_block_definition(source_doc, block_name)
        source_entities = _collect_block_entities(source_block)
        if not source_entities:
            raise RuntimeError(f"源块定义为空，无法导入: {block_name}")

        source_origin = tuple(float(v) for v in getattr(source_block, "Origin", (0.0, 0.0, 0.0)))
        new_block = _create_block_definition(target_doc, source_origin, block_name)
        _copy_entities_to_owner(source_doc, source_entities, new_block)
        wait_quiescent(min_quiet=0.5, timeout=20.0)

        results.append(
            {
                "block_name": block_name,
                "source_entity_count": len(source_entities),
                "reassigned_reference_count": 0,
                "backup_block_name": None,
                "backup_deleted": False,
                "attribute_sync_triggered": False,
                "action": "imported",
            }
        )

    _save_document(target_doc)
    wait_quiescent(min_quiet=0.8, timeout=30.0)
    return {
        "ok": True,
        "target_file": str(target_path),
        "source_file": str(source_path),
        "block_names": list(block_names),
        "results": results,
    }


def _collect_print_areas(
    print_areas: dict[str, Any],
    *,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Sequence[str] | None = None,
) -> list[Any]:
    layout_map = _layout_name_map()
    selected_layouts = _requested_layouts(only_layouts)
    areas: list[Any] = []
    if include_model:
        areas.extend(list(print_areas.get("model", []) or []))
    if include_layouts:
        for owner_btr, values in (print_areas.get("papers") or {}).items():
            if not _owner_selected(
                str(owner_btr),
                include_model=include_model,
                include_layouts=include_layouts,
                only_layouts=selected_layouts,
                layout_map=layout_map,
            ):
                continue
            areas.extend(values or [])
    return areas


def _adaptive_print_area_candidates(
    *,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Sequence[str] | None = None,
) -> list[Any]:
    layout_map = _layout_name_map()
    selected_layouts = _requested_layouts(only_layouts)
    candidates: list[Any] = []
    for owner_name, values in _reasonable_adaptive_candidates_by_owner().items():
        if not _owner_selected(
            owner_name,
            include_model=include_model,
            include_layouts=include_layouts,
            only_layouts=selected_layouts,
            layout_map=layout_map,
        ):
            continue
        candidates.extend(_filter_outer_print_area_candidates(values))
    return candidates


def _filter_entities_by_handles(
    entities: Sequence[Any],
    requested_handles: Sequence[str] | None = None,
) -> list[Any]:
    wanted = {str(handle).strip() for handle in (requested_handles or []) if str(handle).strip()}
    if not wanted:
        return list(entities)
    return [entity for entity in entities if _safe_handle(entity) in wanted]


def _collect_target_print_areas(
    *,
    target_path: Path,
    match_mode: str,
    include_model: bool,
    include_layouts: bool,
    only_layouts: Sequence[str] | None,
    requested_handles: Sequence[str] | None,
) -> list[tuple[Any, dict[str, Any]]]:
    wanted_handles = {str(item).strip() for item in (requested_handles or []) if str(item).strip()}
    targets: list[tuple[Any, dict[str, Any]]] = []
    jobs_by_space = collect_print_jobs(
        str(target_path),
        mode=match_mode,
        include_model=include_model,
        include_layouts=include_layouts,
        only_layouts=list(only_layouts or []),
    )
    for jobs in jobs_by_space.values():
        for job in jobs:
            handle = str(job.handle or "")
            if wanted_handles and handle not in wanted_handles:
                continue
            try:
                entity = C.raw_doc.HandleToObject(handle)
            except Exception as exc:
                sys_logger.warning("[illustration_label] 通过句柄回取打印区域失败: handle=%s err=%s", handle, exc)
                continue
            targets.append(
                (
                    entity,
                    {
                        "handle": handle,
                        "space_kind": str(job.space_kind),
                        "layout_name": str(job.layout_name),
                        "owner_btr": str(job.owner_btr),
                        "media": str(job.media),
                        "ratio": str(job.ratio),
                        "paper_code": str(job.paper_code),
                        "rotation": int(job.rotation),
                        "standard_flag": int(job.standard_flag),
                    },
                )
            )
    return targets


def apply_illustration_labels(
    *,
    target_file: str | Path,
    title_block_source_file: str | Path | None = None,
    block_names: Sequence[str] = DEFAULT_BLOCK_NAMES,
    match_mode: str = DEFAULT_MATCH_MODE,
    ensure_guard: bool = True,
    run_attsync: bool = False,
    insert_titles: bool = True,
    include_model: bool = True,
    include_layouts: bool = True,
    only_layouts: Sequence[str] | None = None,
    requested_handles: Sequence[str] | None = None,
) -> dict[str, Any]:
    target_path = Path(target_file).resolve()
    if not target_path.exists():
        raise FileNotFoundError(f"目标文件不存在: {target_path}")

    normalized_mode = _normalize_mode(match_mode)
    replace_summary = None
    runtime_already_prepared = False
    title_asset_summary: dict[str, Any] | None = None
    cleared_user_frame: list[str] = []

    if title_block_source_file:
        source_path = Path(title_block_source_file).resolve()
        if not source_path.exists():
            raise FileNotFoundError(f"图签源文件不存在: {source_path}")
        replace_summary = _ensure_block_definitions_from_source(
            target_path=target_path,
            source_path=source_path,
            block_names=block_names,
            ensure_guard=ensure_guard,
            run_attsync=run_attsync,
        )
        runtime_already_prepared = True

    try:
        if insert_titles:
            title_asset_summary = _ensure_user_title_frame_assets()

        if not runtime_already_prepared:
            prepare_cad_runtime(ensure_guard=ensure_guard)
        target_doc = _open_document(target_path)
        _activate_document(target_doc)
        _guard_checkpoint("after_open_target_for_illustration_labels")

        layout_map = _layout_name_map()
        target_print_areas = _collect_target_print_areas(
            target_path=target_path,
            match_mode=normalized_mode,
            include_model=include_model,
            include_layouts=include_layouts,
            only_layouts=only_layouts,
            requested_handles=requested_handles,
        )
        space_rectangles = _space_rectangles_by_owner_name()

        results: list[PrintAreaLabelResult] = []
        title_targets: list[dict[str, Any]] = []
        for print_area, job_meta in target_print_areas:
            handle = str(job_meta.get("handle") or _safe_handle(print_area) or "<unknown>")
            owner_name = _owner_space_name(print_area)
            space_kind = str(job_meta.get("space_kind") or _owner_space_kind(owner_name))
            layout_name = str(job_meta.get("layout_name") or _owner_layout_name(owner_name, layout_map))
            owner_space = _owner_space(print_area)
            area_bbox = _bbox_xy(print_area)
            if area_bbox is None:
                results.append(
                    PrintAreaLabelResult(
                        handle=handle,
                        owner=owner_name,
                        space_kind=space_kind,
                        layout_name=layout_name,
                        plot_name=None,
                        paper_code=None,
                        ratio=None,
                        orientation=None,
                        standard_match=False,
                        frame_inserted=False,
                        frame_already_present=False,
                        title_inserted=False,
                        title_already_present=False,
                        inner_frame_bbox=None,
                        status="skipped",
                        message="无法读取打印区域包围盒",
                    )
                )
                continue

            media_name = str(job_meta.get("media", "") or "")
            if media_name:
                spec_name = str(job_meta.get("paper_code", "") or _adaptive_spec_from_bbox(area_bbox))
                plot_device_name = media_name
                ratio = str(job_meta.get("ratio", "") or "")
                orient = int(job_meta.get("rotation", _orientation_from_bbox(area_bbox)))
                standard_flag = int(job_meta.get("standard_flag", 1))
            else:
                match = match_standard_print_by_mode(print_area, mode=normalized_mode)
                if match == 0:
                    spec_name = _adaptive_spec_from_bbox(area_bbox)
                    plot_device_name = spec_name
                    ratio = "adaptive_fallback"
                    orient = _orientation_from_bbox(area_bbox)
                    standard_flag = 0
                else:
                    plot_device_name, ratio, paper_code, orient, _scale_flag, standard_flag = match
                    spec_name = str(paper_code)
            same_space_rectangles = space_rectangles.get(owner_name.lower(), [])

            frame_inserted = False
            frame_already_present = False
            title_inserted = False
            title_already_present = False
            inner_frame_bbox: tuple[float, float, float, float] | None = None

            existing_inner = _best_inner_frame_candidate(print_area, same_space_rectangles)
            if existing_inner is not None:
                frame_already_present = True
                inner_frame_bbox = existing_inner[1]
            else:
                inner_frame_bbox, _ = _insert_frame_geometry(
                    owner_space,
                    print_area,
                    spec_name,
                    area_bbox,
                    orient,
                )
                frame_inserted = True
                _safe_regen(target_doc)
                wait_quiescent(min_quiet=0.5, timeout=20.0)

            result_item = PrintAreaLabelResult(
                handle=handle,
                owner=owner_name,
                space_kind=space_kind,
                layout_name=layout_name,
                plot_name=spec_name,
                paper_code=str(plot_device_name),
                ratio=str(ratio),
                orientation="portrait" if orient == 1 else "landscape",
                standard_match=bool(standard_flag),
                frame_inserted=frame_inserted,
                frame_already_present=frame_already_present,
                title_inserted=title_inserted,
                title_already_present=title_already_present,
                inner_frame_bbox=inner_frame_bbox,
                status="ok",
            )
            results.append(result_item)
            if insert_titles and inner_frame_bbox is not None:
                title_targets.append(
                    {
                        "result": result_item,
                        "owner_space": owner_space,
                        "spec_name": spec_name,
                        "inner_frame_bbox": inner_frame_bbox,
                        "orient": orient,
                    }
                )

        if insert_titles and title_targets:
            _activate_document(target_doc)
            title_asset_summary["definition_sync"] = _ensure_title_block_definitions(target_doc)
            title_definition_profiles = {
                str(item["family"]): dict(item)
                for item in title_asset_summary["definition_sync"]
            }

            for target in title_targets:
                result_item = target["result"]
                spec_name = str(target["spec_name"])
                inner_frame_bbox = target["inner_frame_bbox"]
                orient = int(target["orient"])
                owner_space = target["owner_space"]
                family = _family_from_plot_name(spec_name)
                expected_profile = title_definition_profiles.get(family)
                if not expected_profile:
                    raise RuntimeError(f"缺少图签模板同步结果: {family}")

                existing_title = _find_existing_title_block(owner_space, family, inner_frame_bbox, orient)
                if existing_title is not None:
                    existing_block_def = _get_block_definition(target_doc, TITLE_TEMPLATE_BOUNDS[family]["block"])
                    _assert_title_block_matches_asset(
                        existing_block_def,
                        family=family,
                        stage="复用已有图签时",
                        asset_path=Path(str(expected_profile["asset_path"])),
                        expected_profile=expected_profile,
                    )
                    result_item.title_already_present = True
                    continue

                _insert_title_block(
                    owner_space,
                    spec_name,
                    inner_frame_bbox,
                    orient,
                    expected_profile=expected_profile,
                )
                result_item.title_inserted = True
                _safe_regen(target_doc)
                wait_quiescent(min_quiet=0.5, timeout=20.0)

        _activate_document(target_doc)
        _save_document(target_doc)
        wait_quiescent(min_quiet=0.8, timeout=30.0)
        _guard_checkpoint("after_save_illustration_labels")

        return {
            "ok": True,
            "target_file": str(target_path),
            "match_mode": normalized_mode,
            "title_block_source_file": None if title_block_source_file is None else str(Path(title_block_source_file).resolve()),
            "block_names": list(block_names),
            "include_model": bool(include_model),
            "include_layouts": bool(include_layouts),
            "only_layouts": [str(item) for item in (only_layouts or []) if str(item).strip()],
            "requested_handles": [str(item) for item in (requested_handles or []) if str(item).strip()],
            "replace_summary": replace_summary,
            "title_asset_summary": title_asset_summary,
            "print_area_count": len(target_print_areas),
            "results": [item.to_dict() for item in results],
        }
    finally:
        if insert_titles:
            cleared_user_frame = _clear_user_title_frame_assets()
            if cleared_user_frame:
                sys_logger.info("[title_assets] cleared_user_frame=%s", cleared_user_frame)
