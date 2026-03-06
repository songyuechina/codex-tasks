#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
几何绘制模块（cad_geometry_draw.py）
"""

# ================= 路径引导 =================
import sys
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current:
        raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

# ================= 标准库 =================
import math
import time
from typing import List, Tuple, Optional

# ================= 第三方 =================
import pythoncom
import win32com.client
from win32com.client import VARIANT

# ================= 系统模块 =================
from system.project_setup import PathConfig
from system.licad import resolve_doc
from system.CAD_com_utils import sys_logger, retry_if_busy, retry_on_busy, SafeCOM
from system.common_logger import checkpoint


# ================= 内部工具 =================

# 获取当前时间戳（毫秒）
#&&% _now_ms
def _now_ms():
    return int(time.time() * 1000)


# 点坐标转三维
#&&% _as_3d
def _as_3d(pt):
    if pt is None:
        return None
    try:
        if len(pt) == 2:
            return (float(pt[0]), float(pt[1]), 0.0)
        return (float(pt[0]), float(pt[1]), float(pt[2]))
    except Exception:
        return None


# 顶点序列转二维扁平数组
#&&% _flatten_vertices
def _flatten_vertices(vertices):
    flat = []
    for v in vertices:
        vv = _as_3d(v)
        if vv is None:
            continue
        flat.extend([vv[0], vv[1]])
    return flat


# COM 调用重试封装
#&&% _call_retry
def _call_retry(func, *args, **kwargs):
    @retry_if_busy(max_retries=3, delay=0.4)
    def _inner():
        return func(*args, **kwargs)
    return _inner()


# 确保图层存在（不清理）
#&&% _ensure_layer
def _ensure_layer(doc, layer_name):
    if not layer_name:
        return None
    try:
        layers = doc.Layers
        try:
            layer = layers.Item(layer_name)
        except Exception:
            layer = layers.Add(layer_name)
        doc.ActiveLayer = layer
        return layer_name
    except Exception as e:
        sys_logger.warning(f"[draw] 图层处理失败: {e}")
        return None


# 解析目标空间
#&&% _get_space
def _get_space(doc, target_space):
    if not target_space:
        return doc.ModelSpace
    name = str(target_space)
    if name.lower() in ("model", "modelspace"):
        return doc.ModelSpace
    try:
        layout = doc.Layouts.Item(name)
        return layout.Block
    except Exception:
        return doc.ModelSpace


# 记录开始日志
#&&% _log_start
def _log_start(func_name, detail):
    sys_logger.info(f"[START] {func_name} {detail}")
    return _now_ms()


# 记录结束日志
#&&% _log_end
def _log_end(func_name, start_ms, ok=True, detail=""):
    duration = _now_ms() - start_ms
    sys_logger.info(f"[END] {func_name} ok={ok} duration_ms={duration} {detail}")


# ================= 绘制函数 =================

# 绘制点实体
#&&% draw_point_wcs

def draw_point_wcs(pt, layer=None, color=None, docname=None):
    """
    在 WCS 坐标绘制点实体。
    """
    t0 = _log_start("draw_point_wcs", f"pt={pt} layer={layer} docname={docname}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_point_wcs", t0, ok=False, detail="doc=None")
        return None
    if docname is None:
        sys_logger.warning("[draw_point_wcs] using_active_doc=True")
    p = _as_3d(pt)
    if p is None:
        _log_end("draw_point_wcs", t0, ok=False, detail="invalid pt")
        return None
    try:
        if layer:
            _ensure_layer(doc, layer)
        mp = doc.ModelSpace
        obj = _call_retry(mp.AddPoint, VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [p[0], p[1], p[2]]))
        if layer:
            _call_retry(setattr, obj, "Layer", layer)
        if color is not None:
            _call_retry(setattr, obj, "Color", int(color))
        checkpoint("draw_point_wcs")
        _log_end("draw_point_wcs", t0, ok=True)
        return obj
    except Exception as e:
        sys_logger.info(f"[draw_point_wcs] 异常: {e}")
        _log_end("draw_point_wcs", t0, ok=False)
        return None


# 绘制直线段
#&&% draw_line_wcs

def draw_line_wcs(p1, p2, layer=None, color=None, docname=None):
    """
    在 WCS 坐标绘制直线段。
    """
    t0 = _log_start("draw_line_wcs", f"p1={p1} p2={p2} layer={layer} docname={docname}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_line_wcs", t0, ok=False, detail="doc=None")
        return None
    if docname is None:
        sys_logger.warning("[draw_line_wcs] using_active_doc=True")
    a = _as_3d(p1)
    b = _as_3d(p2)
    if a is None or b is None or (a[0] == b[0] and a[1] == b[1] and a[2] == b[2]):
        _log_end("draw_line_wcs", t0, ok=False, detail="invalid points")
        return None
    try:
        if layer:
            _ensure_layer(doc, layer)
        mp = doc.ModelSpace
        va = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [a[0], a[1], a[2]])
        vb = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [b[0], b[1], b[2]])
        obj = _call_retry(mp.AddLine, va, vb)
        if layer:
            _call_retry(setattr, obj, "Layer", layer)
        if color is not None:
            _call_retry(setattr, obj, "Color", int(color))
        checkpoint("draw_line_wcs")
        _log_end("draw_line_wcs", t0, ok=True)
        return obj
    except Exception as e:
        sys_logger.info(f"[draw_line_wcs] 异常: {e}")
        _log_end("draw_line_wcs", t0, ok=False)
        return None


# 绘制圆
#&&% draw_circle_wcs

def draw_circle_wcs(center, radius, layer=None, color=None, docname=None):
    """
    在 WCS 坐标绘制圆。
    """
    t0 = _log_start("draw_circle_wcs", f"center={center} radius={radius} layer={layer} docname={docname}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_circle_wcs", t0, ok=False, detail="doc=None")
        return None
    if docname is None:
        sys_logger.warning("[draw_circle_wcs] using_active_doc=True")
    c = _as_3d(center)
    if c is None or radius is None or radius <= 0:
        _log_end("draw_circle_wcs", t0, ok=False, detail="invalid params")
        return None
    try:
        if layer:
            _ensure_layer(doc, layer)
        mp = doc.ModelSpace
        vc = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [c[0], c[1], c[2]])
        obj = _call_retry(mp.AddCircle, vc, float(radius))
        if layer:
            _call_retry(setattr, obj, "Layer", layer)
        if color is not None:
            _call_retry(setattr, obj, "Color", int(color))
        checkpoint("draw_circle_wcs")
        _log_end("draw_circle_wcs", t0, ok=True)
        return obj
    except Exception as e:
        sys_logger.info(f"[draw_circle_wcs] 异常: {e}")
        _log_end("draw_circle_wcs", t0, ok=False)
        return None


# 绘制正多边形
#&&% draw_regular_polygon_lwpolyline

def draw_regular_polygon_lwpolyline(center, radius, sides, layer=None, color=None, docname=None):
    """
    绘制正多边形（LWPolyline，闭合）。
    """
    t0 = _log_start("draw_regular_polygon_lwpolyline", f"center={center} r={radius} sides={sides}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_regular_polygon_lwpolyline", t0, ok=False, detail="doc=None")
        return None
    if docname is None:
        sys_logger.warning("[draw_regular_polygon_lwpolyline] using_active_doc=True")
    c = _as_3d(center)
    if c is None or radius is None or radius <= 0 or sides is None or int(sides) < 3:
        _log_end("draw_regular_polygon_lwpolyline", t0, ok=False, detail="invalid params")
        return None
    try:
        if layer:
            _ensure_layer(doc, layer)
        pts_flat = []
        for k in range(int(sides)):
            ang = 2 * math.pi * k / int(sides)
            pts_flat.extend([c[0] + radius * math.cos(ang), c[1] + radius * math.sin(ang)])
        v_pts = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, pts_flat)
        mp = doc.ModelSpace
        poly = _call_retry(mp.AddLightWeightPolyline, v_pts)
        _call_retry(setattr, poly, "Closed", True)
        if layer:
            _call_retry(setattr, poly, "Layer", layer)
        if color is not None:
            try:
                _call_retry(setattr, poly, "Color", int(color))
            except Exception as e:
                sys_logger.warning(f"[draw_regular_polygon_lwpolyline] set color failed, continue: {e}")
        checkpoint("draw_regular_polygon_lwpolyline")
        _log_end("draw_regular_polygon_lwpolyline", t0, ok=True)
        return poly
    except Exception as e:
        sys_logger.info(f"[draw_regular_polygon_lwpolyline] 异常: {e}")
        _log_end("draw_regular_polygon_lwpolyline", t0, ok=False)
        return None


# 绘制轻量多段线
#&&% draw_lwpolyline_wcs

def draw_lwpolyline_wcs(vertices, simplify_tol=None, width=None, color=None, closed=False, layer=None, target_space="ModelSpace", docname=None):
    """
    根据顶点序列绘制 LWPolyline。
    """
    t0 = _log_start("draw_lwpolyline_wcs", f"n={len(vertices) if vertices else 0} closed={closed} space={target_space}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_lwpolyline_wcs", t0, ok=False, detail="doc=None")
        return None
    if docname is None:
        sys_logger.warning("[draw_lwpolyline_wcs] using_active_doc=True")
    if not vertices or len(vertices) < 2:
        _log_end("draw_lwpolyline_wcs", t0, ok=False, detail="vertices<2")
        return None

    try:
        if layer:
            _ensure_layer(doc, layer)
        space = _get_space(doc, target_space)
        pts = []
        last = None
        for v in vertices:
            vv = _as_3d(v)
            if vv is None:
                continue
            if simplify_tol is not None and last is not None:
                if abs(vv[0] - last[0]) <= simplify_tol and abs(vv[1] - last[1]) <= simplify_tol:
                    continue
            pts.append(vv)
            last = vv
        if len(pts) < 2:
            _log_end("draw_lwpolyline_wcs", t0, ok=False, detail="filtered<2")
            return None
        v_pts = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, _flatten_vertices(pts))
        poly = _call_retry(space.AddLightWeightPolyline, v_pts)
        _call_retry(setattr, poly, "Closed", bool(closed))
        if width is not None:
            _call_retry(setattr, poly, "ConstantWidth", float(width))
        if layer:
            _call_retry(setattr, poly, "Layer", layer)
        if color is not None:
            try:
                _call_retry(setattr, poly, "Color", int(color))
            except Exception as e:
                sys_logger.warning(f"[draw_lwpolyline_wcs] set color failed, continue: {e}")
        checkpoint("draw_lwpolyline_wcs")
        _log_end("draw_lwpolyline_wcs", t0, ok=True)
        return poly
    except Exception as e:
        sys_logger.info(f"[draw_lwpolyline_wcs] 异常: {e}")
        _log_end("draw_lwpolyline_wcs", t0, ok=False)
        return None


# 由多边形绘制多段线
#&&% draw_polyline_from_polygon

def draw_polyline_from_polygon(polygon, layer=None, color=None, width=None, simplify_tol=None, include_holes=True, target_space="ModelSpace", docname=None):
    """
    将 polygon（外环+洞）绘制为多条闭合 LWPOLYLINE。
    """
    t0 = _log_start("draw_polyline_from_polygon", f"include_holes={include_holes} space={target_space}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_polyline_from_polygon", t0, ok=False, detail="doc=None")
        return []
    if docname is None:
        sys_logger.warning("[draw_polyline_from_polygon] using_active_doc=True")

    rings = []
    try:
        if hasattr(polygon, "exterior"):
            rings.append(list(polygon.exterior.coords))
            if include_holes:
                for h in polygon.interiors:
                    rings.append(list(h.coords))
        elif isinstance(polygon, dict):
            outer = polygon.get("outer") or polygon.get("exterior")
            holes = polygon.get("holes") or []
            if outer:
                rings.append(list(outer))
            if include_holes:
                for h in holes:
                    rings.append(list(h))
        else:
            rings.append(list(polygon))
    except Exception as e:
        sys_logger.info(f"[draw_polyline_from_polygon] 解析 polygon 失败: {e}")
        _log_end("draw_polyline_from_polygon", t0, ok=False)
        return []

    results = []
    for ring in rings:
        if not ring or len(ring) < 3:
            continue
        obj = draw_lwpolyline_wcs(
            ring,
            simplify_tol=simplify_tol,
            width=width,
            color=color,
            closed=True,
            layer=layer,
            target_space=target_space,
            docname=docname,
        )
        if obj:
            results.append(obj)
    if results:
        checkpoint("draw_polyline_from_polygon")
    _log_end("draw_polyline_from_polygon", t0, ok=True, detail=f"count={len(results)}")
    return results


# 批量绘制多段线
#&&% draw_lwpolylines_batch

def draw_lwpolylines_batch(items, layer=None, target_space="ModelSpace", docname=None):
    """
    批量绘制多条 LWPOLYLINE。
    """
    t0 = _log_start("draw_lwpolylines_batch", f"n={len(items) if items else 0} space={target_space}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_lwpolylines_batch", t0, ok=False, detail="doc=None")
        return []
    if docname is None:
        sys_logger.warning("[draw_lwpolylines_batch] using_active_doc=True")
    if not items:
        _log_end("draw_lwpolylines_batch", t0, ok=False, detail="empty")
        return []

    results = []
    for it in items:
        try:
            verts = it.get("vertices")
            if not verts or len(verts) < 2:
                continue
            obj = draw_lwpolyline_wcs(
                verts,
                simplify_tol=it.get("simplify_tol"),
                width=it.get("width"),
                color=it.get("color"),
                closed=bool(it.get("closed", False)),
                layer=it.get("layer", layer),
                target_space=it.get("target_space", target_space),
                docname=docname,
            )
            if obj:
                results.append(obj)
        except Exception as e:
            sys_logger.info(f"[draw_lwpolylines_batch] item 异常: {e}")
            continue
    if results:
        checkpoint("draw_lwpolylines_batch")
    _log_end("draw_lwpolylines_batch", t0, ok=True, detail=f"count={len(results)}")
    return results


# 点集标记
#&&% draw_markers_for_points

def draw_markers_for_points(points, radius=1000.0, layer_name=None, docname=None):
    """
    对点集绘制圆形标记。
    """
    t0 = _log_start("draw_markers_for_points", f"n={len(points) if points else 0} radius={radius}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_markers_for_points", t0, ok=False, detail="doc=None")
        return []
    if docname is None:
        sys_logger.warning("[draw_markers_for_points] using_active_doc=True")
    if not points:
        _log_end("draw_markers_for_points", t0, ok=False, detail="empty")
        return []

    if layer_name:
        _ensure_layer(doc, layer_name)

    results = []
    mp = doc.ModelSpace
    for pt in points:
        p = _as_3d(pt)
        if p is None:
            continue
        try:
            obj = _call_retry(mp.AddCircle, VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [p[0], p[1], p[2]]), float(radius))
            if layer_name:
                _call_retry(setattr, obj, "Layer", layer_name)
            results.append(obj)
        except Exception as e:
            sys_logger.info(f"[draw_markers_for_points] 单点失败: {e}")
            continue
    if results:
        checkpoint("draw_markers_for_points")
    _log_end("draw_markers_for_points", t0, ok=True, detail=f"count={len(results)}")
    return results


# 沿实体均分插入块（绘制版）
#&&% draw_distributed_blocks_on_entity

def draw_distributed_blocks_on_entity(entity, n, block, scale_factor, color=None, docname=None):
    """
    沿实体均匀插入块（线/弧/多段线）。
    """
    t0 = _log_start("draw_distributed_blocks_on_entity", f"n={n} docname={docname}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_distributed_blocks_on_entity", t0, ok=False, detail="doc=None")
        return []
    if docname is None:
        sys_logger.warning("[draw_distributed_blocks_on_entity] using_active_doc=True")

    try:
        from library import cad_geometry_segment as segment
    except Exception:
        try:
            import cad_geometry_segment as segment
        except Exception as e:
            sys_logger.info(f"[draw_distributed_blocks_on_entity] 无法导入 segment: {e}")
            _log_end("draw_distributed_blocks_on_entity", t0, ok=False)
            return []

    points = segment.compute_distribution_points_on_entity(entity, n)
    if not points:
        _log_end("draw_distributed_blocks_on_entity", t0, ok=False, detail="no points")
        return []

    results = []
    mp = doc.ModelSpace
    block_name = None
    try:
        block_name = block.Name if hasattr(block, "Name") else str(block)
    except Exception:
        block_name = str(block)

    for pt in points:
        p = _as_3d(pt)
        if p is None:
            continue
        try:
            obj = _call_retry(mp.InsertBlock, VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [p[0], p[1], p[2]]), block_name, float(scale_factor), float(scale_factor), float(scale_factor), 0)
            if color is not None:
                _call_retry(setattr, obj, "Color", int(color))
            results.append(obj)
        except Exception as e:
            sys_logger.info(f"[draw_distributed_blocks_on_entity] 插入失败: {e}")
            continue

    if results:
        checkpoint("draw_distributed_blocks_on_entity")
    _log_end("draw_distributed_blocks_on_entity", t0, ok=True, detail=f"count={len(results)}")
    return results


# 绘制样条（可选）
#&&% draw_spline_through_points

def draw_spline_through_points(points, fit=True, layer=None, color=None, target_space="ModelSpace", docname=None):
    """
    通过控制点绘制样条曲线。
    """
    t0 = _log_start("draw_spline_through_points", f"n={len(points) if points else 0} fit={fit}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_spline_through_points", t0, ok=False, detail="doc=None")
        return None
    if docname is None:
        sys_logger.warning("[draw_spline_through_points] using_active_doc=True")
    if not points or len(points) < 2:
        _log_end("draw_spline_through_points", t0, ok=False, detail="points<2")
        return None

    if layer:
        _ensure_layer(doc, layer)

    try:
        space = _get_space(doc, target_space)
        pts = []
        for p in points:
            pp = _as_3d(p)
            if pp is None:
                continue
            pts.extend([pp[0], pp[1], pp[2]])
        if len(pts) < 6:
            _log_end("draw_spline_through_points", t0, ok=False, detail="invalid pts")
            return None
        v_pts = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, pts)
        obj = None
        try:
            p0 = (pts[0], pts[1], pts[2])
            p1 = (pts[3], pts[4], pts[5])
            pn_1 = (pts[-6], pts[-5], pts[-4])
            pn = (pts[-3], pts[-2], pts[-1])
            sdx, sdy, sdz = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
            edx, edy, edz = (pn[0] - pn_1[0], pn[1] - pn_1[1], pn[2] - pn_1[2])
            sl = (sdx ** 2 + sdy ** 2 + sdz ** 2) ** 0.5 or 1.0
            el = (edx ** 2 + edy ** 2 + edz ** 2) ** 0.5 or 1.0
            start_tan = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [sdx / sl, sdy / sl, sdz / sl])
            end_tan = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [edx / el, edy / el, edz / el])
            obj = _call_retry(space.AddSpline, v_pts, start_tan, end_tan)
        except Exception as e:
            sys_logger.warning(f"[draw_spline_through_points] AddSpline with tangents failed, fallback: {e}")

        if obj is None:
            obj = _call_retry(space.AddSpline, v_pts)
        if layer:
            _call_retry(setattr, obj, "Layer", layer)
        if color is not None:
            _call_retry(setattr, obj, "Color", int(color))
        checkpoint("draw_spline_through_points")
        _log_end("draw_spline_through_points", t0, ok=True)
        return obj
    except Exception as e:
        sys_logger.info(f"[draw_spline_through_points] 异常: {e}")
        _log_end("draw_spline_through_points", t0, ok=False)
        return None


# 绘制椭圆
#&&% draw_ellipse_wcs

def draw_ellipse_wcs(center, major_axis_vec, ratio, start_angle=0.0, end_angle=2 * math.pi, layer=None, color=None, target_space="ModelSpace", docname=None):
    """
    按中心、主轴向量与扁率绘制椭圆（或椭圆弧）。
    """
    t0 = _log_start("draw_ellipse_wcs", f"center={center} ratio={ratio}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("draw_ellipse_wcs", t0, ok=False, detail="doc=None")
        return None
    if docname is None:
        sys_logger.warning("[draw_ellipse_wcs] using_active_doc=True")

    c = _as_3d(center)
    v = _as_3d(major_axis_vec)
    if c is None or v is None or ratio is None or ratio <= 0 or ratio > 1:
        _log_end("draw_ellipse_wcs", t0, ok=False, detail="invalid params")
        return None

    try:
        if layer:
            _ensure_layer(doc, layer)
        space = _get_space(doc, target_space)
        vc = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [c[0], c[1], c[2]])
        vv = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [v[0], v[1], v[2]])
        obj = None
        try:
            obj = _call_retry(space.AddEllipse, vc, vv, float(ratio))
        except Exception as e:
            sys_logger.warning(f"[draw_ellipse_wcs] AddEllipse(3 args) failed, try legacy signature: {e}")
            obj = _call_retry(space.AddEllipse, vc, vv, float(ratio), float(start_angle), float(end_angle))

        # Some CAD COM variants only support full ellipse creation, then set angles by properties.
        if not (abs(float(start_angle)) < 1e-9 and abs(float(end_angle) - 2 * math.pi) < 1e-6):
            try:
                _call_retry(setattr, obj, "StartAngle", float(start_angle))
                _call_retry(setattr, obj, "EndAngle", float(end_angle))
            except Exception as e:
                sys_logger.warning(f"[draw_ellipse_wcs] set start/end angle failed, keep full ellipse: {e}")

        if layer:
            _call_retry(setattr, obj, "Layer", layer)
        if color is not None:
            try:
                _call_retry(setattr, obj, "Color", int(color))
            except Exception as e:
                sys_logger.warning(f"[draw_ellipse_wcs] set color failed, continue: {e}")
        checkpoint("draw_ellipse_wcs")
        _log_end("draw_ellipse_wcs", t0, ok=True)
        return obj
    except Exception as e:
        sys_logger.info(f"[draw_ellipse_wcs] 异常: {e}")
        _log_end("draw_ellipse_wcs", t0, ok=False)
        return None

