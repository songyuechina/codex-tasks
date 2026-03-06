#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
几何分析模块（cad_geometry_segment.py）
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
from typing import List, Tuple

# ================= 系统模块 =================
from system.project_setup import PathConfig
from system.licad import resolve_doc
from system.CAD_com_utils import sys_logger, retry_if_busy, retry_on_busy, SafeCOM
from system.common_logger import checkpoint
from system.CAD_coordination import wait_quiescent
from system import CAD_selection

# ================= 可选第三方 =================
try:
    from shapely.geometry import Polygon, Point, LineString
    from shapely.ops import polygonize
except Exception:
    Polygon = None
    Point = None
    LineString = None
    polygonize = None


# ================= 内部工具 =================

# 获取当前时间戳（毫秒）
#&&% _now_ms
def _now_ms():
    return int(time.time() * 1000)


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


# COM 调用重试封装
#&&% _call_retry
def _call_retry(func, *args, **kwargs):
    @retry_if_busy(max_retries=3, delay=0.4)
    def _inner():
        return func(*args, **kwargs)
    return _inner()


# COM 删除重试封装
#&&% _call_delete
def _call_delete(func, *args, **kwargs):
    @retry_on_busy(max_retries=3, base_delay=0.4)
    def _inner():
        return func(*args, **kwargs)
    return _inner()


# 坐标量化（用于去重）
#&&% _quantize
def _quantize(pt, tol):
    if tol is None or tol <= 0:
        return (round(pt[0], 6), round(pt[1], 6), round(pt[2], 6))
    return (round(pt[0] / tol), round(pt[1] / tol), round(pt[2] / tol))


# 读取线段端点
#&&% _line_endpoints
def _line_endpoints(line):
    if hasattr(line, "StartPoint") and hasattr(line, "EndPoint"):
        return _as_3d(line.StartPoint), _as_3d(line.EndPoint)
    if isinstance(line, (list, tuple)) and len(line) == 2:
        return _as_3d(line[0]), _as_3d(line[1])
    return None, None


# 获取外包盒
#&&% _get_bbox
def _get_bbox(ent):
    try:
        return ent.GetBoundingBox()
    except Exception:
        return None, None


# ================= 角度与基础 =================

# 计算直线方向角
#&&% compute_line_angle_deg

def compute_line_angle_deg(line):
    """按绘制方向计算线段方向角（0-360）。"""
    t0 = _log_start("compute_line_angle_deg", f"line={getattr(line, 'ObjectName', None)}")
    try:
        p1 = _as_3d(line.StartPoint)
        p2 = _as_3d(line.EndPoint)
        if p1 is None or p2 is None:
            _log_end("compute_line_angle_deg", t0, ok=False, detail="no endpoints")
            return None
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        ang = math.degrees(math.atan2(dy, dx))
        if ang < 0:
            ang += 360
        _log_end("compute_line_angle_deg", t0, ok=True)
        return ang
    except Exception as e:
        sys_logger.info(f"[compute_line_angle_deg] 异常: {e}")
        _log_end("compute_line_angle_deg", t0, ok=False)
        return None


# 优先水平线
#&&% prioritize_horizontal_lines

def prioritize_horizontal_lines(lines, tol=0.5):
    """将水平线分组返回。"""
    t0 = _log_start("prioritize_horizontal_lines", f"n={len(lines) if lines else 0} tol={tol}")
    horizontals = []
    others = []
    if not lines:
        _log_end("prioritize_horizontal_lines", t0, ok=False, detail="empty")
        return horizontals, others
    for ln in lines:
        try:
            y1 = ln.StartPoint[1]
            y2 = ln.EndPoint[1]
            if abs(y1 - y2) < tol:
                horizontals.append(ln)
            else:
                others.append(ln)
        except Exception:
            continue
    _log_end("prioritize_horizontal_lines", t0, ok=True, detail=f"h={len(horizontals)} o={len(others)}")
    return horizontals, others


# 距离
#&&% distance_xy_or_xyz

def distance_xy_or_xyz(p1, p2):
    """两点距离（优先三维）。"""
    t0 = _log_start("distance_xy_or_xyz", f"p1={p1} p2={p2}")
    a = _as_3d(p1)
    b = _as_3d(p2)
    if a is None or b is None:
        _log_end("distance_xy_or_xyz", t0, ok=False, detail="invalid")
        return float("nan")
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    d = math.sqrt(dx * dx + dy * dy + dz * dz)
    _log_end("distance_xy_or_xyz", t0, ok=True)
    return d


# 直线定距点
#&&% points_on_line_at_distance_3d

def points_on_line_at_distance_3d(p1, p2, px, distance):
    """已知 px 在线上，返回距 px 为 distance 的两个点。"""
    t0 = _log_start("points_on_line_at_distance_3d", f"distance={distance}")
    a = _as_3d(p1)
    b = _as_3d(p2)
    x = _as_3d(px)
    if a is None or b is None or x is None:
        _log_end("points_on_line_at_distance_3d", t0, ok=False, detail="invalid")
        return []
    dx, dy, dz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length == 0:
        _log_end("points_on_line_at_distance_3d", t0, ok=False, detail="zero length")
        return []
    ux, uy, uz = dx / length, dy / length, dz / length
    p_plus = (x[0] + ux * distance, x[1] + uy * distance, x[2] + uz * distance)
    p_minus = (x[0] - ux * distance, x[1] - uy * distance, x[2] - uz * distance)
    _log_end("points_on_line_at_distance_3d", t0, ok=True)
    return [p_plus, p_minus]


# 点比较
#&&% points_equal_2d

def points_equal_2d(p1, p2, tol=0.01):
    """判断两点 XY 是否相等。"""
    a = _as_3d(p1)
    b = _as_3d(p2)
    if a is None or b is None:
        return False
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


# 数值近似
#&&% nearly_equal

def nearly_equal(a, b, tol=1e-9):
    try:
        return abs(a - b) <= tol
    except Exception:
        return False


# 线段无向相等
#&&% lines_equal_undirected

def lines_equal_undirected(ln1, ln2, tol=0.01):
    a1, a2 = _line_endpoints(ln1)
    b1, b2 = _line_endpoints(ln2)
    if a1 is None or a2 is None or b1 is None or b2 is None:
        return False
    return (points_equal_2d(a1, b1, tol) and points_equal_2d(a2, b2, tol)) or \
           (points_equal_2d(a1, b2, tol) and points_equal_2d(a2, b1, tol))


# 伪交点计算
#&&% find_fake_intersection_points

def find_fake_intersection_points(lines, tol=10.0, real_tol=0.01, dedup_tol=None):
    """计算伪交点坐标（不绘制）。"""
    t0 = _log_start("find_fake_intersection_points", f"n={len(lines) if lines else 0} tol={tol}")
    if not lines or tol <= real_tol:
        _log_end("find_fake_intersection_points", t0, ok=False, detail="invalid")
        return []

    if dedup_tol is None:
        dedup_tol = tol

    def point_to_line_distance(p, a1, a2):
        x0, y0 = p[:2]
        x1, y1 = a1[:2]
        x2, y2 = a2[:2]
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            return math.hypot(x0 - x1, y0 - y1)
        t = max(0.0, min(1.0, ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)))
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return math.hypot(x0 - proj_x, y0 - proj_y)

    added = set()
    results = []
    for A in lines:
        p1, p2 = _line_endpoints(A)
        if p1 is None or p2 is None:
            continue
        for pt in [p1, p2]:
            key = _quantize(pt, dedup_tol)
            if key in added:
                continue
            has_near = False
            has_real_near = False
            for B in lines:
                if B == A:
                    continue
                b1, b2 = _line_endpoints(B)
                if b1 is None or b2 is None:
                    continue
                dist = point_to_line_distance(pt, b1, b2)
                if dist < tol:
                    has_near = True
                if dist < real_tol:
                    has_real_near = True
                    break
            if has_near and not has_real_near:
                added.add(key)
                results.append(pt)
    _log_end("find_fake_intersection_points", t0, ok=True, detail=f"count={len(results)}")
    return results


# 打断线段
#&&% break_lines_between_points

def break_lines_between_points(start_point, end_point, docname=None):
    """调用天正 tlinebk 打断线段。"""
    t0 = _log_start("break_lines_between_points", f"start={start_point} end={end_point} docname={docname}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("break_lines_between_points", t0, ok=False, detail="doc=None")
        return False
    if docname is None:
        sys_logger.warning("[break_lines_between_points] using_active_doc=True")

    sp = _as_3d(start_point)
    ep = _as_3d(end_point)
    if sp is None or ep is None:
        _log_end("break_lines_between_points", t0, ok=False, detail="invalid points")
        return False

    cmd = f"tlinebk\n{sp[0]},{sp[1]},{sp[2]}\n{ep[0]},{ep[1]},{ep[2]}\n\n\n"
    try:
        _call_retry(doc.SendCommand, cmd)
        wait_quiescent(min_quiet=0.3, timeout=10.0)
        checkpoint("break_lines_between_points")
        _log_end("break_lines_between_points", t0, ok=True)
        return True
    except Exception as e:
        sys_logger.info(f"[break_lines_between_points] 命令失败: {e}")
        _log_end("break_lines_between_points", t0, ok=False)
        return False


# 删除重复线段
#&&% delete_duplicate_lines

def delete_duplicate_lines(lines, tol=0.01, docname=None):
    """删除重复线段，仅保留一条。"""
    t0 = _log_start("delete_duplicate_lines", f"n={len(lines) if lines else 0} tol={tol}")
    if docname is None:
        sys_logger.warning("[delete_duplicate_lines] using_active_doc=True")
    if not lines:
        _log_end("delete_duplicate_lines", t0, ok=False, detail="empty")
        return [], 0

    seen = {}
    kept = []
    deleted = 0
    for ln in lines:
        p1, p2 = _line_endpoints(ln)
        if p1 is None or p2 is None:
            continue
        k1 = _quantize(p1, tol)
        k2 = _quantize(p2, tol)
        key = tuple(sorted([k1, k2]))
        if key in seen:
            try:
                _call_delete(ln.Delete)
                deleted += 1
            except Exception:
                pass
        else:
            seen[key] = ln
            kept.append(ln)
    if deleted:
        checkpoint("delete_duplicate_lines")
    _log_end("delete_duplicate_lines", t0, ok=True, detail=f"deleted={deleted}")
    return kept, deleted


# 删除冗余线段
#&&% delete_redundant_lines

def delete_redundant_lines(lines, tol=0.01, docname=None):
    """删除重复及完全包含的冗余线段。"""
    t0 = _log_start("delete_redundant_lines", f"n={len(lines) if lines else 0} tol={tol}")
    if docname is None:
        sys_logger.warning("[delete_redundant_lines] using_active_doc=True")
    if not lines:
        _log_end("delete_redundant_lines", t0, ok=False, detail="empty")
        return [], 0, 0

    def is_same_point(p1, p2):
        return abs(p1[0] - p2[0]) < tol and abs(p1[1] - p2[1]) < tol

    def point_on_segment(p, a, b):
        ax, ay = a[:2]
        bx, by = b[:2]
        px, py = p[:2]
        cross = abs((bx - ax) * (py - ay) - (by - ay) * (px - ax))
        if cross > tol:
            return False
        dot = (px - ax) * (bx - ax) + (py - ay) * (by - ay)
        if dot < 0:
            return False
        sq_len = (bx - ax) ** 2 + (by - ay) ** 2
        if dot > sq_len:
            return False
        return True

    to_delete = set()
    total = len(lines)
    for i in range(total):
        l1 = lines[i]
        p1, p2 = _line_endpoints(l1)
        if p1 is None or p2 is None:
            continue
        for j in range(i + 1, total):
            l2 = lines[j]
            q1, q2 = _line_endpoints(l2)
            if q1 is None or q2 is None:
                continue
            if (is_same_point(p1, q1) and is_same_point(p2, q2)) or (is_same_point(p1, q2) and is_same_point(p2, q1)):
                to_delete.add(l2)
            elif point_on_segment(q1, p1, p2) and point_on_segment(q2, p1, p2):
                to_delete.add(l2)
            elif point_on_segment(p1, q1, q2) and point_on_segment(p2, q1, q2):
                to_delete.add(l1)
                break

    deleted = 0
    for ent in lines:
        if ent in to_delete:
            try:
                _call_delete(ent.Delete)
                deleted += 1
            except Exception:
                continue

    kept = [x for x in lines if x not in to_delete]
    if deleted:
        checkpoint("delete_redundant_lines")
    _log_end("delete_redundant_lines", t0, ok=True, detail=f"deleted={deleted}")
    return kept, deleted, 0


# 椭圆周长估算
#&&% estimate_ellipse_length_ramanujan

def estimate_ellipse_length_ramanujan(ellipse):
    """Ramanujan 公式估算椭圆周长。"""
    t0 = _log_start("estimate_ellipse_length_ramanujan", "")
    try:
        a = ellipse.MajorRadius
        b = ellipse.MinorRadius
        if a <= 0 or b <= 0:
            _log_end("estimate_ellipse_length_ramanujan", t0, ok=False)
            return None
        h = 3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b))
        length = math.pi * h
        _log_end("estimate_ellipse_length_ramanujan", t0, ok=True)
        return length
    except Exception as e:
        sys_logger.info(f"[estimate_ellipse_length_ramanujan] 异常: {e}")
        _log_end("estimate_ellipse_length_ramanujan", t0, ok=False)
        return None


# 获取几何信息
#&&% get_entity_geometry_info

def get_entity_geometry_info(entity, docname=None):
    """统一读取图元几何信息。"""
    t0 = _log_start("get_entity_geometry_info", f"entity={getattr(entity, 'ObjectName', None)}")
    if entity is None:
        _log_end("get_entity_geometry_info", t0, ok=False, detail="entity=None")
        return {"type": "Error", "message": "entity=None"}

    try:
        name = str(entity.ObjectName).lower()
        if "point" in name:
            res = {"type": "Point", "position": getattr(entity, "Coordinates", None)}
        elif "line" in name and "xline" not in name:
            p1 = entity.StartPoint
            p2 = entity.EndPoint
            length = math.dist(p1, p2)
            res = {"type": "Line", "start": p1, "end": p2, "length": length}
        elif "circle" in name:
            center = entity.Center
            radius = entity.Radius
            length = 2 * math.pi * radius
            area = math.pi * radius ** 2
            res = {"type": "Circle", "center": center, "radius": radius, "length": length, "area": area}
        elif "ellipse" in name:
            center = entity.Center
            a = entity.MajorRadius
            b = entity.MinorRadius
            area = math.pi * a * b
            length = estimate_ellipse_length_ramanujan(entity)
            res = {"type": "Ellipse", "center": center, "major_radius": a, "minor_radius": b, "length": length, "area": area}
        elif "polyline" in name:
            coords = entity.Coordinates
            start = (coords[0], coords[1], 0)
            end = (coords[-2], coords[-1], 0)
            length = getattr(entity, "Length", 0)
            area = entity.Area if getattr(entity, "Closed", False) else 0
            res = {"type": "Polyline", "start": start, "end": end, "length": length, "area": area}
        elif "spline" in name:
            if docname is None:
                sys_logger.warning("[get_entity_geometry_info] spline 需要 docname")
                length = None
            else:
                try:
                    from library import cad_geometry_polyline as polyline
                except Exception:
                    import cad_geometry_polyline as polyline
                length = polyline.spline_length_via_conversion(entity, docname=docname)
            try:
                p1 = entity.GetFitPoint(0)
                p2 = entity.GetFitPoint(entity.NumberOfFitPoints - 1)
            except Exception:
                p1 = None
                p2 = None
            area = entity.Area if getattr(entity, "Closed", False) else 0
            res = {"type": "Spline", "start": p1, "end": p2, "length": length, "area": area}
        else:
            res = {"type": "Unknown", "ObjectName": getattr(entity, "ObjectName", "")}
        _log_end("get_entity_geometry_info", t0, ok=True)
        return res
    except Exception as e:
        _log_end("get_entity_geometry_info", t0, ok=False)
        return {"type": "Error", "message": str(e)}


# 选择线段（用于交互）
#&&% select_lines_for_segment_ops

def select_lines_for_segment_ops(filter_by_layer=None, docname=None):
    """通过 CAD_selection 选择 Line 对象。"""
    t0 = _log_start("select_lines_for_segment_ops", f"layer={filter_by_layer} docname={docname}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("select_lines_for_segment_ops", t0, ok=False, detail="doc=None")
        return []
    if docname is None:
        sys_logger.warning("[select_lines_for_segment_ops] using_active_doc=True")
    try:
        lines = CAD_selection.select_line(autocast=True)
        if filter_by_layer:
            lines = [x for x in lines if getattr(x, "Layer", None) == filter_by_layer]
        _log_end("select_lines_for_segment_ops", t0, ok=True, detail=f"count={len(lines)}")
        return lines
    except Exception as e:
        sys_logger.info(f"[select_lines_for_segment_ops] 异常: {e}")
        _log_end("select_lines_for_segment_ops", t0, ok=False)
        return []


# ================= BBox 与矩形 =================

# 获取外包盒左下
#&&% get_bbox_min_point

def get_bbox_min_point(entity):
    t0 = _log_start("get_bbox_min_point", f"entity={getattr(entity, 'ObjectName', None)}")
    min_pt, max_pt = _get_bbox(entity)
    if min_pt is None:
        _log_end("get_bbox_min_point", t0, ok=False, detail="no bbox")
        return None
    _log_end("get_bbox_min_point", t0, ok=True)
    return min_pt


# 获取外包盒右上
#&&% get_bbox_max_point

def get_bbox_max_point(entity):
    t0 = _log_start("get_bbox_max_point", f"entity={getattr(entity, 'ObjectName', None)}")
    min_pt, max_pt = _get_bbox(entity)
    if max_pt is None:
        _log_end("get_bbox_max_point", t0, ok=False, detail="no bbox")
        return None
    _log_end("get_bbox_max_point", t0, ok=True)
    return max_pt


# 轴对齐矩形定义
#&&% define_axis_aligned_rectangle_by_diagonal

def define_axis_aligned_rectangle_by_diagonal(p1, p2):
    t0 = _log_start("define_axis_aligned_rectangle_by_diagonal", f"p1={p1} p2={p2}")
    a = _as_3d(p1)
    b = _as_3d(p2)
    if a is None or b is None or (a[0] == b[0] and a[1] == b[1]):
        _log_end("define_axis_aligned_rectangle_by_diagonal", t0, ok=False, detail="invalid")
        return []
    xmin, xmax = min(a[0], b[0]), max(a[0], b[0])
    ymin, ymax = min(a[1], b[1]), max(a[1], b[1])
    z = a[2]
    pts = [(xmin, ymin, z), (xmax, ymin, z), (xmax, ymax, z), (xmin, ymax, z)]
    _log_end("define_axis_aligned_rectangle_by_diagonal", t0, ok=True)
    return pts


# 矩形外扩
#&&% expand_axis_aligned_rectangle

def expand_axis_aligned_rectangle(p1, p2, offset):
    t0 = _log_start("expand_axis_aligned_rectangle", f"offset={offset}")
    a = _as_3d(p1)
    b = _as_3d(p2)
    if a is None or b is None:
        _log_end("expand_axis_aligned_rectangle", t0, ok=False, detail="invalid")
        return []
    xmin, xmax = min(a[0], b[0]) - offset, max(a[0], b[0]) + offset
    ymin, ymax = min(a[1], b[1]) - offset, max(a[1], b[1]) + offset
    z = a[2]
    pts = [(xmin, ymin, z), (xmax, ymin, z), (xmax, ymax, z), (xmin, ymax, z)]
    _log_end("expand_axis_aligned_rectangle", t0, ok=True)
    return pts


# 解析矩形输入
#&&% parse_rectangle_inputs

def parse_rectangle_inputs(*args):
    t0 = _log_start("parse_rectangle_inputs", f"args={len(args)}")
    if len(args) == 2:
        pts = define_axis_aligned_rectangle_by_diagonal(args[0], args[1])
        _log_end("parse_rectangle_inputs", t0, ok=True)
        return pts
    if len(args) == 3:
        origin = _as_3d(args[0])
        w = float(args[1])
        h = float(args[2])
        if origin is None:
            _log_end("parse_rectangle_inputs", t0, ok=False, detail="invalid origin")
            return []
        p1 = origin
        p2 = (origin[0] + w, origin[1] + h, origin[2])
        pts = define_axis_aligned_rectangle_by_diagonal(p1, p2)
        _log_end("parse_rectangle_inputs", t0, ok=True)
        return pts
    _log_end("parse_rectangle_inputs", t0, ok=False, detail="unsupported")
    return []


# 获取实体尺寸
#&&% get_entity_bbox_dimensions

def get_entity_bbox_dimensions(ent):
    t0 = _log_start("get_entity_bbox_dimensions", f"entity={getattr(ent, 'ObjectName', None)}")
    min_pt, max_pt = _get_bbox(ent)
    if min_pt is None or max_pt is None:
        _log_end("get_entity_bbox_dimensions", t0, ok=False, detail="no bbox")
        return None
    dx = abs(max_pt[0] - min_pt[0])
    dy = abs(max_pt[1] - min_pt[1])
    length, width = (dx, dy) if dx >= dy else (dy, dx)
    _log_end("get_entity_bbox_dimensions", t0, ok=True)
    return length, width


# 按左下角排序
#&&% sort_entities_by_lower_left_corner

def sort_entities_by_lower_left_corner(com_list, cha_Y=1000):
    t0 = _log_start("sort_entities_by_lower_left_corner", f"n={len(com_list) if com_list else 0}")
    if not com_list:
        _log_end("sort_entities_by_lower_left_corner", t0, ok=False, detail="empty")
        return []

    items = []
    for ent in com_list:
        min_pt, _ = _get_bbox(ent)
        if min_pt is None:
            continue
        items.append((ent, min_pt[0], min_pt[1]))
    items.sort(key=lambda x: (int(x[2] // cha_Y), x[1]))
    res = [x[0] for x in items]
    _log_end("sort_entities_by_lower_left_corner", t0, ok=True, detail=f"count={len(res)}")
    return res


# 关系构建
#&&% build_relation_list_by_proximity

def build_relation_list_by_proximity(data_list, tol=1.0):
    t0 = _log_start("build_relation_list_by_proximity", f"n={len(data_list) if data_list else 0}")
    res = []
    if not data_list:
        _log_end("build_relation_list_by_proximity", t0, ok=False, detail="empty")
        return res
    for i in range(len(data_list)):
        for j in range(i + 1, len(data_list)):
            try:
                a = data_list[i]
                b = data_list[j]
                min_a, _ = _get_bbox(a)
                min_b, _ = _get_bbox(b)
                if min_a is None or min_b is None:
                    continue
                if distance_xy_or_xyz(min_a, min_b) <= tol:
                    res.append((i, j, "near"))
            except Exception:
                continue
    _log_end("build_relation_list_by_proximity", t0, ok=True, detail=f"relations={len(res)}")
    return res


# 打印框标准表
_PRINT_FRAME_LB = [
    (118900, 84100, 100),  (178350, 126150, 150),   (59450, 42050, 50),     (29725, 21025, 25),
    (133800, 84100, 100),  (200700, 126150, 150),   (66900, 42050, 50),     (33450, 21025, 25),
    (148600, 84100, 100),  (222900, 126150, 150),   (74300, 42050, 50),     (37150, 21025, 25),
    (84100,  59400, 100),  (126150, 89100,  150),   (42050, 29700, 50),     (21025, 14850, 25),
    (105100, 59400, 100),  (157650, 89100,  150),   (52550, 29700, 50),     (26275, 14850, 25),
    (126100, 59400, 100),  (189150, 89100,  150),   (63050, 29700, 50),     (31525, 14850, 25),
    (147100, 59400, 100),  (220650, 89100,  150),   (73550, 29700, 50),     (36775, 14850, 25),
    (59400,  42000, 100),  (89100,  63000,  150),   (29700, 21000, 50),     (14850, 10500, 25),
    (74300,  42000, 100),  (111450, 63000,  150),   (37150, 21000, 50),     (18575, 10500, 25),
    (89100,  42000, 100),  (133650, 63000,  150),   (44550, 21000, 50),     (22275, 10500, 25),
    (104100, 42000, 100),  (156150, 63000,  150),   (52050, 21000, 50),     (26025, 10500, 25),
    (42000,  29700, 100),  (63000,  44550,  150),   (21000, 14850, 50),     (10500, 7425,  25),
]

_PRINT_FRAME_MAP_ML = [
    ("A0", "1:100"), ("A0", "1:150"), ("A0", "1:50"),  ("A0", "1:25"),
    ("A0+1/8", "1:100"), ("A0+1/8", "1:150"), ("A0+1/8", "1:50"),  ("A0+1/8", "1:25"),
    ("A0+1/4", "1:100"), ("A0+1/4", "1:150"), ("A0+1/4", "1:50"),  ("A0+1/4", "1:25"),
    ("A1", "1:100"), ("A1", "1:150"), ("A1", "1:50"), ("A1", "1:25"),
    ("A1+1/4", "1:100"), ("A1+1/4", "1:150"), ("A1+1/4", "1:50"),  ("A1+1/4", "1:25"),
    ("A1+1/2", "1:100"), ("A1+1/2", "1:150"), ("A1+1/2", "1:50"),  ("A1+1/2", "1:25"),
    ("A1+3/4", "1:100"), ("A1+3/4", "1:150"), ("A1+3/4", "1:50"),  ("A1+3/4", "1:25"),
    ("A2", "1:100"), ("A2", "1:150"), ("A2", "1:50"),  ("A2", "1:25"),
    ("A2+1/4", "1:100"), ("A2+1/4", "1:150"), ("A2+1/4", "1:50"),  ("A2+1/4", "1:25"),
    ("A2+1/2", "1:100"), ("A2+1/2", "1:150"), ("A2+1/2", "1:50"),  ("A2+1/2", "1:25"),
    ("A2+3/4", "1:100"), ("A2+3/4", "1:150"), ("A2+3/4", "1:50"),  ("A2+3/4", "1:25"),
    ("A3", "1:100"), ("A3", "1:150"), ("A3", "1:50"),  ("A3", "1:25"),
]

_PRINT_FRAME_MAP = [
    "ISO_A0_(841.00_x_1189.00_MM)", "ISO_A0_(841.00_x_1189.00_MM)", "ISO_A0_(841.00_x_1189.00_MM)", "ISO_A0_(841.00_x_1189.00_MM)",
    "UserDefinedMetric (1338.00 x 841.00毫米)", "UserDefinedMetric (1338.00 x 841.00毫米)",
    "UserDefinedMetric (1338.00 x 841.00毫米)", "UserDefinedMetric (1338.00 x 841.00毫米)",
    "UserDefinedMetric (1486.00 x 841.00毫米)", "UserDefinedMetric (1486.00 x 841.00毫米)",
    "UserDefinedMetric (1486.00 x 841.00毫米)", "UserDefinedMetric (1486.00 x 841.00毫米)",
    "ISO_A1_(841.00_x_594.00_MM)", "ISO_A1_(841.00_x_594.00_MM)", "ISO_A1_(841.00_x_594.00_MM)", "ISO_A1_(841.00_x_594.00_MM)",
    "UserDefinedMetric (1051.00 x 594.00毫米)", "UserDefinedMetric (1051.00 x 594.00毫米)",
    "UserDefinedMetric (1051.00 x 594.00毫米)", "UserDefinedMetric (1051.00 x 594.00毫米)",
    "UserDefinedMetric (1261.00 x 594.00毫米)", "UserDefinedMetric (1261.00 x 594.00毫米)",
    "UserDefinedMetric (1261.00 x 594.00毫米)", "UserDefinedMetric (1261.00 x 594.00毫米)",
    "UserDefinedMetric (1471.00 x 594.00毫米)", "UserDefinedMetric (1471.00 x 594.00毫米)",
    "UserDefinedMetric (1471.00 x 594.00毫米)", "UserDefinedMetric (1471.00 x 594.00毫米)",
    "ISO_A2_(594.00_x_420.00_MM)", "ISO_A2_(594.00_x_420.00_MM)", "ISO_A2_(594.00_x_420.00_MM)", "ISO_A2_(594.00_x_420.00_MM)",
    "UserDefinedMetric (743.00 x 420.00毫米)", "UserDefinedMetric (743.00 x 420.00毫米)",
    "UserDefinedMetric (743.00 x 420.00毫米)", "UserDefinedMetric (743.00 x 420.00毫米)",
    "UserDefinedMetric (891.00 x 420.00毫米)", "UserDefinedMetric (891.00 x 420.00毫米)",
    "UserDefinedMetric (891.00 x 420.00毫米)", "UserDefinedMetric (891.00 x 420.00毫米)",
    "UserDefinedMetric (1041.00 x 420.00毫米)", "UserDefinedMetric (1041.00 x 420.00毫米)",
    "UserDefinedMetric (1041.00 x 420.00毫米)", "UserDefinedMetric (1041.00 x 420.00毫米)",
    "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)",
]


def _get_print_frame_tables():
    return _PRINT_FRAME_LB, _PRINT_FRAME_MAP_ML, _PRINT_FRAME_MAP


# 图框名称与比例推断（完整表）
#&&% generate_name_and_ratio_from_com

def generate_name_and_ratio_from_com(
    comobj,
    A3dy=0,
    Fandy=("ISO_A3_(420.00_x_297.00_MM)", "0:0", "A3", 0),
    tol=10,
):
    t0 = _log_start("generate_name_and_ratio_from_com", f"tol={tol}")

    try:
        obj_name = getattr(comobj, "ObjectName", "")
        if "Polyline" not in obj_name:
            _log_end("generate_name_and_ratio_from_com", t0, ok=False, detail="not polyline")
            return 0
    except Exception:
        _log_end("generate_name_and_ratio_from_com", t0, ok=False, detail="type check fail")
        return 0

    try:
        min_pt, max_pt = comobj.GetBoundingBox()
        dx = abs(max_pt[0] - min_pt[0])
        dy = abs(max_pt[1] - min_pt[1])
        if dx < 100 or dy < 100:
            _log_end("generate_name_and_ratio_from_com", t0, ok=False, detail="too small")
            return 0
        try:
            real_area = abs(getattr(comobj, "Area", 0))
            box_area = dx * dy
            if box_area > 0 and abs(real_area - box_area) / box_area > 0.02:
                _log_end("generate_name_and_ratio_from_com", t0, ok=False, detail="non-rect")
                return 0
        except Exception:
            pass
        length = max(dx, dy)
        width = min(dx, dy)
        orientation_flag = 1 if dy > dx else 0
    except Exception:
        _log_end("generate_name_and_ratio_from_com", t0, ok=False, detail="bbox fail")
        return 0

    if A3dy == 1:
        _log_end("generate_name_and_ratio_from_com", t0, ok=True, detail="force A3")
        return (Fandy[0], Fandy[1], Fandy[2], orientation_flag)

    dynamic_tol = 10.0 if length > 1783.5 else 1.0

    LB_dayingkuang, drawing_map_ml, drawing_map = _get_print_frame_tables()
    draw_factors = [1.0, 0.5, 0.25, 1.5]
    multipliers = [1.0, 1.1, 1.2]

    strict_best_index = None
    strict_min_diff = float("inf")
    approx_best_index = None
    approx_min_diff = float("inf")

    for i, (std_len, std_wid, scale_val) in enumerate(LB_dayingkuang):
        label = drawing_map_ml[i][0]
        mult_list = multipliers if label != "A3" else [1.0]
        for df in draw_factors:
            for mult in mult_list:
                tgt_len_m = std_len * df * mult
                tgt_wid_m = std_wid * df * mult
                diff_m = abs(length - tgt_len_m) + abs(width - tgt_wid_m)

                tgt_len_l = (std_len / scale_val) * df * mult
                tgt_wid_l = (std_wid / scale_val) * df * mult
                diff_l = abs(length - tgt_len_l) + abs(width - tgt_wid_l)

                current_diff = min(diff_m, diff_l)
                if current_diff < approx_min_diff:
                    approx_min_diff = current_diff
                    approx_best_index = i

                if diff_m <= diff_l:
                    d_len = abs(length - tgt_len_m)
                    d_wid = abs(width - tgt_wid_m)
                else:
                    d_len = abs(length - tgt_len_l)
                    d_wid = abs(width - tgt_wid_l)

                if d_len <= dynamic_tol and d_wid <= dynamic_tol:
                    if current_diff < strict_min_diff:
                        strict_min_diff = current_diff
                        strict_best_index = i

    if strict_best_index is not None:
        final_index = strict_best_index
    elif approx_best_index is not None:
        final_index = approx_best_index
    else:
        _log_end("generate_name_and_ratio_from_com", t0, ok=False, detail="no match")
        return 0

    res_name = drawing_map[final_index]
    res_ratio = drawing_map_ml[final_index][1]
    res_code = drawing_map_ml[final_index][0]
    _log_end("generate_name_and_ratio_from_com", t0, ok=True, detail=f"name={res_code}")
    return (res_name, res_ratio, res_code, orientation_flag)


# 图框名称与比例推断（简版）
#&&% infer_frame_name_and_scale_from_entity

def infer_frame_name_and_scale_from_entity(comobj, A3dy=0, Fandy=("ISO_A3_(420.00_x_297.00_MM)", "0:0", "A3", 0), tol=10):
    t0 = _log_start("infer_frame_name_and_scale_from_entity", "")
    res = generate_name_and_ratio_from_com(comobj, A3dy=A3dy, Fandy=Fandy, tol=tol)
    if res == 0:
        _log_end("infer_frame_name_and_scale_from_entity", t0, ok=False)
        return "UNKNOWN", 1.0
    ratio_val = 1.0
    try:
        ratio_str = res[1]
        if ":" in ratio_str:
            ratio_val = float(ratio_str.split(":")[1]) / 100.0
    except Exception:
        ratio_val = 1.0
    _log_end("infer_frame_name_and_scale_from_entity", t0, ok=True, detail=f"name={res[2]}")
    return res[2], ratio_val


# 严格尺寸匹配（完整表）
#&&% check_strict_standard_size

def check_strict_standard_size(comobj, tol=10):
    t0 = _log_start("check_strict_standard_size", f"tol={tol}")
    try:
        min_p, max_p = comobj.GetBoundingBox()
        dx = abs(max_p[0] - min_p[0])
        dy = abs(max_p[1] - min_p[1])
        obj_L = max(dx, dy)
        obj_W = min(dx, dy)
        orientation = 1 if dy > dx else 0
    except Exception:
        _log_end("check_strict_standard_size", t0, ok=False, detail="bbox fail")
        return 0

    is_mini_scale = True if obj_L < 2140.8 else False
    active_tol = 0.1 if is_mini_scale else float(tol)
    env_scale = 0.01 if is_mini_scale else 1.0
    growth_factors = [1.0, 1.1, 1.2]

    LB_dayingkuang, drawing_map_ml, drawing_map = _get_print_frame_tables()
    for i, (std_L, std_W, _) in enumerate(LB_dayingkuang):
        label_size = drawing_map_ml[i][0]
        factor_list = growth_factors if label_size != "A3" else [1.0]
        for factor in factor_list:
            target_L = std_L * env_scale * factor
            target_W = std_W * env_scale * factor
            current_tol = active_tol * factor
            if abs(obj_L - target_L) <= current_tol and abs(obj_W - target_W) <= current_tol:
                scale_label = drawing_map_ml[i][1]
                if is_mini_scale:
                    try:
                        scale_val = float(scale_label.split(":")[1]) / 100.0
                        final_scale_label = f"1:{scale_val:g}"
                    except Exception:
                        final_scale_label = scale_label
                else:
                    final_scale_label = scale_label
                if abs(factor - 1.2) < 0.01:
                    try:
                        comobj.Color = 5
                    except Exception:
                        pass
                _log_end("check_strict_standard_size", t0, ok=True, detail=label_size)
                return (
                    drawing_map[i],
                    final_scale_label,
                    label_size,
                    orientation,
                )
    _log_end("check_strict_standard_size", t0, ok=True, detail="UNKNOWN")
    return 0


# 判断竖向图框
#&&% detect_portrait_frame_from_polyline

def detect_portrait_frame_from_polyline(polyline, tol=0.01):
    t0 = _log_start("detect_portrait_frame_from_polyline", "")
    try:
        from library import cad_geometry_polyline as polyline_mod
    except Exception:
        import cad_geometry_polyline as polyline_mod
    info = polyline_mod.polyline_basic_info(polyline)
    if not info:
        _log_end("detect_portrait_frame_from_polyline", t0, ok=False)
        return None
    min_pt, max_pt = _get_bbox(polyline)
    if min_pt is None or max_pt is None:
        _log_end("detect_portrait_frame_from_polyline", t0, ok=False)
        return None
    dx = abs(max_pt[0] - min_pt[0])
    dy = abs(max_pt[1] - min_pt[1])
    res = dy > dx + tol
    _log_end("detect_portrait_frame_from_polyline", t0, ok=True, detail=f"portrait={res}")
    return res


# 统一图幅标记（计算版）
#&&% unify_print_frame_size_labels

def unify_print_frame_size_labels(LB, TFname):
    t0 = _log_start("unify_print_frame_size_labels", f"n={len(LB) if LB else 0}")
    res = []
    if not LB:
        _log_end("unify_print_frame_size_labels", t0, ok=False, detail="empty")
        return res
    for ent in LB:
        res.append((ent, TFname))
    _log_end("unify_print_frame_size_labels", t0, ok=True, detail=f"count={len(res)}")
    return res


# 简化多边形
#&&% simplify_polygon_collinear

def simplify_polygon_collinear(poly, tol=1e-6):
    t0 = _log_start("simplify_polygon_collinear", f"n={len(poly) if poly else 0}")
    if not poly or len(poly) < 3:
        _log_end("simplify_polygon_collinear", t0, ok=True, detail="short")
        return list(poly) if poly else []

    def colinear(p, q, r):
        return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) <= tol

    res = []
    n = len(poly)
    for i in range(n):
        p_prev = poly[i - 1]
        p = poly[i]
        p_next = poly[(i + 1) % n]
        if colinear(p_prev, p, p_next):
            continue
        res.append(p)
    _log_end("simplify_polygon_collinear", t0, ok=True, detail=f"out={len(res)}")
    return res


# 标准化多边形
#&&% normalize_polygon_vertices

def normalize_polygon_vertices(polygon, close=True, tol=1e-6):
    t0 = _log_start("normalize_polygon_vertices", f"n={len(polygon) if polygon else 0}")
    if not polygon:
        _log_end("normalize_polygon_vertices", t0, ok=False, detail="empty")
        return []
    res = []
    last = None
    for p in polygon:
        pp = _as_3d(p)
        if pp is None:
            continue
        if last and abs(pp[0] - last[0]) <= tol and abs(pp[1] - last[1]) <= tol:
            continue
        res.append(pp)
        last = pp
    if close and res:
        if abs(res[0][0] - res[-1][0]) > tol or abs(res[0][1] - res[-1][1]) > tol:
            res.append(res[0])
    _log_end("normalize_polygon_vertices", t0, ok=True, detail=f"out={len(res)}")
    return res


# 相邻顶点
#&&% get_adjacent_vertices_in_polygon

def get_adjacent_vertices_in_polygon(polygon, p, tol=1e-6):
    if not polygon:
        return None, None
    for i, v in enumerate(polygon):
        if abs(v[0] - p[0]) <= tol and abs(v[1] - p[1]) <= tol:
            return polygon[i - 1], polygon[(i + 1) % len(polygon)]
    return None, None


# 点在多边形内
#&&% point_in_polygon_xy

def point_in_polygon_xy(pt, polygon, tol=1e-6):
    t0 = _log_start("point_in_polygon_xy", "")
    if not polygon or len(polygon) < 3:
        _log_end("point_in_polygon_xy", t0, ok=False, detail="short")
        return False
    x, y, _ = _as_3d(pt)
    inside = False
    n = len(polygon)
    for i in range(n):
        x1, y1, _ = _as_3d(polygon[i])
        x2, y2, _ = _as_3d(polygon[(i + 1) % n])
        if ((y1 > y) != (y2 > y)):
            x_int = (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1
            if x < x_int + tol:
                inside = not inside
    _log_end("point_in_polygon_xy", t0, ok=True, detail=f"inside={inside}")
    return inside


# 射线-线段交点
#&&% ray_segment_intersection_2d

def ray_segment_intersection_2d(p, d, a, b, tol=1e-9):
    p = _as_3d(p)
    d = _as_3d(d)
    a = _as_3d(a)
    b = _as_3d(b)
    if None in (p, d, a, b):
        return None
    px, py = p[0], p[1]
    dx, dy = d[0], d[1]
    ax, ay = a[0], a[1]
    bx, by = b[0], b[1]
    rx, ry = bx - ax, by - ay
    denom = dx * ry - dy * rx
    if abs(denom) <= tol:
        return None
    t = ((ax - px) * ry - (ay - py) * rx) / denom
    u = ((ax - px) * dy - (ay - py) * dx) / denom
    if t >= -tol and u >= -tol and u <= 1 + tol:
        hit = (px + t * dx, py + t * dy, 0.0)
        return hit, t, u
    return None


# 辅助点
#&&% compute_auxiliary_point_for_vertex

def compute_auxiliary_point_for_vertex(p, p_prev, p_next, polygon, tol=1e-6):
    p = _as_3d(p)
    p_prev = _as_3d(p_prev)
    p_next = _as_3d(p_next)
    if None in (p, p_prev, p_next):
        return None
    v1 = (p_prev[0] - p[0], p_prev[1] - p[1])
    v2 = (p_next[0] - p[0], p_next[1] - p[1])
    n1 = math.hypot(v1[0], v1[1]) or 1.0
    n2 = math.hypot(v2[0], v2[1]) or 1.0
    u1 = (v1[0] / n1, v1[1] / n1)
    u2 = (v2[0] / n2, v2[1] / n2)
    bis = (u1[0] + u2[0], u1[1] + u2[1])
    bn = math.hypot(bis[0], bis[1]) or 1.0
    q = (p[0] + bis[0] / bn * tol, p[1] + bis[1] / bn * tol, p[2])
    return q


# 凹凸度量值
#&&% concavity_measure_value

def concavity_measure_value(p, p_prev, p_next, q):
    try:
        a = (p_prev[0] - p[0], p_prev[1] - p[1])
        b = (p_next[0] - p[0], p_next[1] - p[1])
        cross = a[0] * b[1] - a[1] * b[0]
        return cross
    except Exception:
        return 0.0


# 凹凸角
#&&% concavity_measure_angle

def concavity_measure_angle(p, polygon):
    p_prev, p_next = get_adjacent_vertices_in_polygon(polygon, p)
    if p_prev is None or p_next is None:
        return None
    q = compute_auxiliary_point_for_vertex(p, p_prev, p_next, polygon)
    if q is None:
        return None
    v1 = (p_prev[0] - p[0], p_prev[1] - p[1])
    v2 = (p_next[0] - p[0], p_next[1] - p[1])
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    n1 = math.hypot(v1[0], v1[1])
    n2 = math.hypot(v2[0], v2[1])
    if n1 == 0 or n2 == 0:
        return None
    ang = math.degrees(math.acos(max(-1.0, min(1.0, dot / (n1 * n2)))))
    return ang


# 水平分割六边形
#&&% split_orthogonal_hexagon_by_horizontal

def split_orthogonal_hexagon_by_horizontal(polygon, tol=0.1):
    t0 = _log_start("split_orthogonal_hexagon_by_horizontal", "")
    try:
        poly = normalize_polygon_vertices(polygon, close=False)
        if len(poly) != 6:
            _log_end("split_orthogonal_hexagon_by_horizontal", t0, ok=False, detail="not 6")
            return []
        concaves = [pt for pt in poly if abs((concavity_measure_angle(pt, poly) or 0) - 270) < tol]
        if len(concaves) != 1:
            _log_end("split_orthogonal_hexagon_by_horizontal", t0, ok=False, detail="concave!=1")
            return []
        p = concaves[0]
        y0 = p[1]
        intersections = []
        n = len(poly)
        for i in range(n):
            a = poly[i]
            b = poly[(i + 1) % n]
            y1, y2 = a[1], b[1]
            if (y1 - y0) * (y2 - y0) < -tol ** 2:
                t = (y0 - y1) / (y2 - y1)
                xi = a[0] + t * (b[0] - a[0])
                intersections.append((xi, y0, a[2], i))
        if len(intersections) != 1:
            _log_end("split_orthogonal_hexagon_by_horizontal", t0, ok=False, detail="no q")
            return []
        xi, yi, zi, edge_idx = intersections[0]
        q = (xi, yi, zi)
        newpoly = []
        for i in range(n):
            newpoly.append(poly[i])
            if i == edge_idx:
                newpoly.append(q)
        i_p = newpoly.index(p)
        i_q = newpoly.index(q)
        if i_q < i_p:
            rect1 = newpoly[i_q:i_p + 1]
            rect2 = newpoly[i_p:] + newpoly[:i_q + 1]
        else:
            rect1 = newpoly[i_p:i_q + 1]
            rect2 = newpoly[i_q:] + newpoly[:i_p + 1]
        _log_end("split_orthogonal_hexagon_by_horizontal", t0, ok=True)
        return [rect1, rect2]
    except Exception as e:
        sys_logger.info(f"[split_orthogonal_hexagon_by_horizontal] 异常: {e}")
        _log_end("split_orthogonal_hexagon_by_horizontal", t0, ok=False)
        return []


# 竖向分割六边形
#&&% split_orthogonal_hexagon_by_vertical

def split_orthogonal_hexagon_by_vertical(polygon, tol=0.1):
    t0 = _log_start("split_orthogonal_hexagon_by_vertical", "")
    try:
        poly = normalize_polygon_vertices(polygon, close=False)
        if len(poly) != 6:
            _log_end("split_orthogonal_hexagon_by_vertical", t0, ok=False, detail="not 6")
            return []
        concaves = [pt for pt in poly if abs((concavity_measure_angle(pt, poly) or 0) - 270) < tol]
        if len(concaves) != 1:
            _log_end("split_orthogonal_hexagon_by_vertical", t0, ok=False, detail="concave!=1")
            return []
        p = concaves[0]
        x0 = p[0]
        intersections = []
        n = len(poly)
        for i in range(n):
            a = poly[i]
            b = poly[(i + 1) % n]
            x1, x2 = a[0], b[0]
            if (x1 - x0) * (x2 - x0) < -tol ** 2:
                t = (x0 - x1) / (x2 - x1)
                yi = a[1] + t * (b[1] - a[1])
                intersections.append((x0, yi, a[2], i))
        if len(intersections) != 1:
            _log_end("split_orthogonal_hexagon_by_vertical", t0, ok=False, detail="no q")
            return []
        xi, yi, zi, edge_idx = intersections[0]
        q = (xi, yi, zi)
        newpoly = []
        for i in range(n):
            newpoly.append(poly[i])
            if i == edge_idx:
                newpoly.append(q)
        i_p = newpoly.index(p)
        i_q = newpoly.index(q)
        if i_q < i_p:
            rect1 = newpoly[i_q:i_p + 1]
            rect2 = newpoly[i_p:] + newpoly[:i_q + 1]
        else:
            rect1 = newpoly[i_p:i_q + 1]
            rect2 = newpoly[i_q:] + newpoly[:i_p + 1]
        _log_end("split_orthogonal_hexagon_by_vertical", t0, ok=True)
        return [rect1, rect2]
    except Exception as e:
        sys_logger.info(f"[split_orthogonal_hexagon_by_vertical] 异常: {e}")
        _log_end("split_orthogonal_hexagon_by_vertical", t0, ok=False)
        return []


# 多边形有向面积
#&&% polygon_area_signed

def polygon_area_signed(verts):
    if not verts or len(verts) < 3:
        return 0.0
    s = 0.0
    n = len(verts)
    for i in range(n):
        x1, y1, _ = _as_3d(verts[i])
        x2, y2, _ = _as_3d(verts[(i + 1) % n])
        s += x1 * y2 - x2 * y1
    return s / 2.0


# 自动分割六边形
#&&% split_orthogonal_hexagon_auto

def split_orthogonal_hexagon_auto(polygon, tol=0.1, simplify_tol=None):
    t0 = _log_start("split_orthogonal_hexagon_auto", "")
    if simplify_tol is not None:
        polygon = simplify_polygon_collinear(polygon, tol=simplify_tol)
    res = split_orthogonal_hexagon_by_horizontal(polygon, tol=tol)
    if res:
        _log_end("split_orthogonal_hexagon_auto", t0, ok=True, detail="horizontal")
        return res
    res = split_orthogonal_hexagon_by_vertical(polygon, tol=tol)
    _log_end("split_orthogonal_hexagon_auto", t0, ok=bool(res), detail="vertical")
    return res


# BBox 边线段
#&&% get_bbox_as_edge_segments

def get_bbox_as_edge_segments(pl, tol=0.0):
    t0 = _log_start("get_bbox_as_edge_segments", "")
    min_pt, max_pt = _get_bbox(pl)
    if min_pt is None or max_pt is None:
        _log_end("get_bbox_as_edge_segments", t0, ok=False, detail="no bbox")
        return []
    xmin, ymin, zmin = min_pt
    xmax, ymax, _ = max_pt
    p1 = (xmin, ymin, zmin)
    p2 = (xmax, ymin, zmin)
    p3 = (xmax, ymax, zmin)
    p4 = (xmin, ymax, zmin)
    _log_end("get_bbox_as_edge_segments", t0, ok=True)
    return [(p4, p3), (p1, p2), (p1, p4), (p2, p3)]


# 天正多行文字内容
#&&% explode_copy_and_get_mtext_content

def explode_copy_and_get_mtext_content(comobj, separator="|", docname=None):
    """复制并炸开多行文字，拼接内容。"""
    t0 = _log_start("explode_copy_and_get_mtext_content", f"docname={docname}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("explode_copy_and_get_mtext_content", t0, ok=False, detail="doc=None")
        return ""
    if docname is None:
        sys_logger.warning("[explode_copy_and_get_mtext_content] using_active_doc=True")

    fragments = []
    try:
        copy_ent = _call_retry(comobj.Copy)
        if not copy_ent:
            _log_end("explode_copy_and_get_mtext_content", t0, ok=False, detail="copy failed")
            return ""

        try:
            CAD_selection.set_entity_grip_state_precise(copy_ent)
        except Exception:
            pass

        pre_count = doc.ModelSpace.Count
        _call_retry(doc.SendCommand, "_.EXPLODE\n")
        wait_quiescent(min_quiet=0.3, timeout=10.0)
        time.sleep(0.2)
        post_count = doc.ModelSpace.Count
        if post_count > pre_count:
            for i in range(pre_count, post_count):
                try:
                    fragments.append(doc.ModelSpace.Item(i))
                except Exception:
                    continue

        if not fragments:
            _log_end("explode_copy_and_get_mtext_content", t0, ok=False, detail="no fragments")
            return ""

        def _get_sort_info(ent):
            try:
                ins = getattr(ent, "InsertionPoint", None)
                if not ins:
                    min_p, _ = ent.GetBoundingBox()
                    return (round(min_p[1] / 0.3), min_p[0])
                return (round(ins[1] / 0.3), ins[0])
            except Exception:
                return (0, 0)

        fragments.sort(key=lambda e: (-_get_sort_info(e)[0], _get_sort_info(e)[1]))
        final_string = ""
        last_y_bin = None
        for frag in fragments:
            try:
                txt = getattr(frag, "TextString", None) or getattr(frag, "Text", None)
                if not txt:
                    continue
                y_bin, _ = _get_sort_info(frag)
                if last_y_bin is not None and y_bin != last_y_bin:
                    final_string += separator
                final_string += txt
                last_y_bin = y_bin
            except Exception:
                continue

        for frag in fragments:
            try:
                _call_delete(frag.Delete)
            except Exception:
                pass
        try:
            _call_delete(copy_ent.Delete)
        except Exception:
            pass

        checkpoint("explode_copy_and_get_mtext_content")
        _log_end("explode_copy_and_get_mtext_content", t0, ok=True)
        return final_string
    except Exception as e:
        sys_logger.info(f"[explode_copy_and_get_mtext_content] 异常: {e}")
        _log_end("explode_copy_and_get_mtext_content", t0, ok=False)
        return ""


# 均分点计算
#&&% compute_distribution_points_on_entity

def compute_distribution_points_on_entity(entity, n, use_parametric=True):
    """沿实体均匀分布 n 个点（仅计算）。"""
    t0 = _log_start("compute_distribution_points_on_entity", f"n={n}")
    if n is None or n < 2:
        _log_end("compute_distribution_points_on_entity", t0, ok=False, detail="n<2")
        return []
    try:
        name = getattr(entity, "ObjectName", "")
        points = []
        if name == "AcDbLine":
            p1 = _as_3d(entity.StartPoint)
            p2 = _as_3d(entity.EndPoint)
            for i in range(n):
                t = i / (n - 1)
                points.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]), p1[2]))
        elif name == "AcDbArc":
            start_angle = entity.StartAngle
            end_angle = entity.EndAngle
            center = _as_3d(entity.Center)
            radius = entity.Radius
            for i in range(n):
                ang = start_angle + i * (end_angle - start_angle) / (n - 1)
                x = center[0] + radius * math.cos(ang)
                y = center[1] + radius * math.sin(ang)
                points.append((x, y, center[2]))
        elif name == "AcDbPolyline":
            coords = entity.Coordinates
            pts = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
            def dist(a, b):
                return math.hypot(a[0] - b[0], a[1] - b[1])
            total = sum(dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
            seg = total / (n - 1)
            cur = 0.0
            for _ in range(n):
                acc = 0.0
                for j in range(len(pts) - 1):
                    d = dist(pts[j], pts[j + 1])
                    if acc + d >= cur:
                        ratio = (cur - acc) / d if d != 0 else 0
                        x = pts[j][0] + ratio * (pts[j + 1][0] - pts[j][0])
                        y = pts[j][1] + ratio * (pts[j + 1][1] - pts[j][1])
                        points.append((x, y, 0.0))
                        break
                    acc += d
                cur += seg
        else:
            _log_end("compute_distribution_points_on_entity", t0, ok=False, detail="unsupported")
            return []
        _log_end("compute_distribution_points_on_entity", t0, ok=True, detail=f"count={len(points)}")
        return points
    except Exception as e:
        sys_logger.info(f"[compute_distribution_points_on_entity] 异常: {e}")
        _log_end("compute_distribution_points_on_entity", t0, ok=False)
        return []


# 线段包含
#&&% segment_contained_in_segment

def segment_contained_in_segment(seg_a, seg_b, tol=1e-4):
    a1, a2 = _line_endpoints(seg_a)
    b1, b2 = _line_endpoints(seg_b)
    if None in (a1, a2, b1, b2):
        return False

    def colinear(p, q, r):
        return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) <= tol

    if not (colinear(b1, b2, a1) and colinear(b1, b2, a2)):
        return False

    b_dir = (b2[0] - b1[0], b2[1] - b1[1])
    b_len2 = b_dir[0] ** 2 + b_dir[1] ** 2
    if b_len2 == 0:
        return False

    def proj_param(p):
        return ((p[0] - b1[0]) * b_dir[0] + (p[1] - b1[1]) * b_dir[1]) / b_len2

    t1 = proj_param(a1)
    t2 = proj_param(a2)
    return -tol <= t1 <= 1 + tol and -tol <= t2 <= 1 + tol


# 矩形包含
#&&% rect_contains_rect_axis_aligned

def rect_contains_rect_axis_aligned(rect_outer, rect_inner, tol=1e-6):
    (ox0, oy0), (ox1, oy1) = rect_outer
    (ix0, iy0), (ix1, iy1) = rect_inner
    return ix0 >= ox0 - tol and iy0 >= oy0 - tol and ix1 <= ox1 + tol and iy1 <= oy1 + tol


# 多段线顶点包含
#&&% all_polyline_vertices_inside_polygon

def all_polyline_vertices_inside_polygon(pl1, pl2, tol=0.01):
    try:
        from library import cad_geometry_polyline as polyline_mod
    except Exception:
        import cad_geometry_polyline as polyline_mod
    verts1 = polyline_mod.get_unique_vertices_from_polyline_com(pl1)
    verts2 = polyline_mod.get_unique_vertices_from_polyline_com(pl2)
    if not verts1 or not verts2:
        return False
    for pt in verts2:
        if not point_in_polygon_xy(pt, verts1, tol=tol):
            return False
    return True


# 孤立交点
#&&% find_isolated_intersections

def find_isolated_intersections(LB, tol=0.5):
    t0 = _log_start("find_isolated_intersections", f"n={len(LB) if LB else 0}")
    intersections = []
    if not LB:
        _log_end("find_isolated_intersections", t0, ok=False, detail="empty")
        return intersections

    def segment_intersection(seg1, seg2, tol):
        (x1, y1, z1), (x2, y2, _) = seg1
        (x3, y3, _), (x4, y4, _) = seg2
        r = (x2 - x1, y2 - y1)
        s = (x4 - x3, y4 - y3)
        rxs = r[0] * s[1] - r[1] * s[0]
        if abs(rxs) < tol:
            return None
        qp = (x3 - x1, y3 - y1)
        t = (qp[0] * s[1] - qp[1] * s[0]) / rxs
        u = (qp[0] * r[1] - qp[1] * r[0]) / rxs
        if -tol <= t <= 1 + tol and -tol <= u <= 1 + tol:
            xi = x1 + t * r[0]
            yi = y1 + t * r[1]
            zi = z1
            return (xi, yi, zi)
        return None

    isolated = []
    for i, seg in enumerate(LB):
        p1, p2 = seg
        shared = False
        for j, other in enumerate(LB):
            if i == j:
                continue
            q1, q2 = other
            if points_equal_2d(p1, q1, tol) or points_equal_2d(p1, q2, tol) or points_equal_2d(p2, q1, tol) or points_equal_2d(p2, q2, tol):
                shared = True
                break
        if not shared:
            isolated.append(seg)

    for seg in isolated:
        for other in LB:
            if other is seg:
                continue
            ip = segment_intersection(seg, other, tol)
            if ip is not None:
                intersections.append(ip)

    _log_end("find_isolated_intersections", t0, ok=True, detail=f"count={len(intersections)}")
    return intersections


# 多边形内部点
#&&% get_inner_point_of_polygon

def get_inner_point_of_polygon(polygon):
    t0 = _log_start("get_inner_point_of_polygon", "")
    if Polygon is None:
        _log_end("get_inner_point_of_polygon", t0, ok=False, detail="no shapely")
        return None
    try:
        poly = Polygon([(p[0], p[1]) for p in polygon])
        p = poly.representative_point()
        res = (p.x, p.y, 0.0)
        _log_end("get_inner_point_of_polygon", t0, ok=True)
        return res
    except Exception as e:
        sys_logger.info(f"[get_inner_point_of_polygon] 异常: {e}")
        _log_end("get_inner_point_of_polygon", t0, ok=False)
        return None


# 房间轮廓提取
#&&% extract_room_outline_by_point

def extract_room_outline_by_point(x, y, z=0.0, docname=None):
    t0 = _log_start("extract_room_outline_by_point", f"x={x} y={y} z={z}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("extract_room_outline_by_point", t0, ok=False, detail="doc=None")
        return []
    if docname is None:
        sys_logger.warning("[extract_room_outline_by_point] using_active_doc=True")

    cmd = f"TSpOutline\n{x},{y},{z}\n\n"
    try:
        before = doc.ModelSpace.Count
        _call_retry(doc.SendCommand, cmd)
        wait_quiescent(min_quiet=0.3, timeout=10.0)
        time.sleep(0.2)
        after = doc.ModelSpace.Count
        res = []
        for i in range(before, after):
            try:
                ent = doc.ModelSpace.Item(i)
                if "Polyline" in getattr(ent, "ObjectName", ""):
                    res.append(ent)
            except Exception:
                continue
        if res:
            checkpoint("extract_room_outline_by_point")
        _log_end("extract_room_outline_by_point", t0, ok=True, detail=f"count={len(res)}")
        return res
    except Exception as e:
        sys_logger.info(f"[extract_room_outline_by_point] 异常: {e}")
        _log_end("extract_room_outline_by_point", t0, ok=False)
        return []


# 判断闭合多边形
#&&% is_closed_polygon_from_lines

def is_closed_polygon_from_lines(lines, tol=0.01):
    if not lines:
        return False
    points = []
    for ln in lines:
        p1, p2 = _line_endpoints(ln)
        if p1 is None or p2 is None:
            continue
        points.append(p1)
        points.append(p2)
    if not points:
        return False
    counts = {}
    for p in points:
        key = _quantize(p, tol)
        counts[key] = counts.get(key, 0) + 1
    return all(v % 2 == 0 for v in counts.values())


# 线段绝对角
#&&% compute_line_absolute_angle_from_point_deg

def compute_line_absolute_angle_from_point_deg(line, P, tol=0.01):
    p1, p2 = _line_endpoints(line)
    if p1 is None or p2 is None:
        return None
    P = _as_3d(P)
    if P is None:
        return None
    d1 = distance_xy_or_xyz(P, p1)
    d2 = distance_xy_or_xyz(P, p2)
    start = p1 if d1 <= d2 + tol else p2
    end = p2 if start == p1 else p1
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    ang = math.degrees(math.atan2(dy, dx))
    if ang < 0:
        ang += 360
    return ang


# 相对角
#&&% compute_relative_angle_between_lines_at_point_deg

def compute_relative_angle_between_lines_at_point_deg(line, current_line, P, tol=0.01):
    a = compute_line_absolute_angle_from_point_deg(current_line, P, tol)
    b = compute_line_absolute_angle_from_point_deg(line, P, tol)
    if a is None or b is None:
        return None
    d = (b - a) % 360
    return d


# 共点线段绝对角排序
#&&% sort_incident_lines_by_absolute_angle

def sort_incident_lines_by_absolute_angle(lines, P, tol=0.01):
    incident = []
    for ln in lines:
        p1, p2 = _line_endpoints(ln)
        if p1 is None or p2 is None:
            continue
        if points_equal_2d(p1, P, tol) or points_equal_2d(p2, P, tol):
            ang = compute_line_absolute_angle_from_point_deg(ln, P, tol)
            if ang is not None:
                incident.append((ang, ln))
    incident.sort(key=lambda x: x[0])
    return [x[1] for x in incident]


# 共点线段相对角排序
#&&% sort_incident_lines_by_relative_angle

def sort_incident_lines_by_relative_angle(lines, P, current_line, tol=0.01):
    incident = []
    for ln in lines:
        if ln == current_line:
            continue
        ang = compute_relative_angle_between_lines_at_point_deg(ln, current_line, P, tol)
        if ang is not None:
            incident.append((ang, ln))
    incident.sort(key=lambda x: x[0])
    return [x[1] for x in incident]


# 最大后继线段
#&&% find_successor_line_max_angle

def find_successor_line_max_angle(current_line, lines, P, tol=0.01):
    candidates = sort_incident_lines_by_relative_angle(lines, P, current_line, tol)
    return candidates[-1] if candidates else None


# 最小后继线段
#&&% find_successor_line_min_angle

def find_successor_line_min_angle(current_line, lines, P, tol=0.01):
    candidates = sort_incident_lines_by_relative_angle(lines, P, current_line, tol)
    return candidates[0] if candidates else None


# 右下点
#&&% find_bottom_right_point

def find_bottom_right_point(lines, tol=0.0):
    points = []
    for ln in lines:
        p1, p2 = _line_endpoints(ln)
        if p1 is None or p2 is None:
            continue
        points.append(p1)
        points.append(p2)
    if not points:
        return None
    points.sort(key=lambda p: (p[1], -p[0]))
    return points[0]


# 右下起始闭合多边形
#&&% find_bottom_right_closed_polygon

def find_bottom_right_closed_polygon(lines, tol=0.01, max_steps=10000):
    if not lines:
        return []
    start = find_bottom_right_point(lines, tol)
    if start is None:
        return []
    polygon = [start]
    current = None
    P = start
    for _ in range(max_steps):
        if current is None:
            candidates = sort_incident_lines_by_absolute_angle(lines, P, tol)
            if not candidates:
                return []
            current = candidates[0]
        nxt = find_successor_line_min_angle(current, lines, P, tol)
        if nxt is None:
            break
        p1, p2 = _line_endpoints(nxt)
        P = p2 if points_equal_2d(p1, P, tol) else p1
        if points_equal_2d(P, start, tol):
            polygon.append(start)
            return polygon
        polygon.append(P)
        current = nxt
    return []


# 外轮廓
#&&% extract_outer_contour_from_lines

def extract_outer_contour_from_lines(lines, tol=0.01, max_steps=20000):
    polys = compute_closed_polygons_from_lines(lines, tol=tol, max_steps=max_steps)
    if not polys:
        return []
    polys.sort(key=lambda p: abs(polygon_area_signed(p)), reverse=True)
    return polys[0]


# 去重顶点序列
#&&% deduplicate_vertices_sequence

def deduplicate_vertices_sequence(vertices, tol=0.01, keep_ends=True):
    if not vertices:
        return []
    res = []
    last = None
    for v in vertices:
        vv = _as_3d(v)
        if vv is None:
            continue
        if last and points_equal_2d(vv, last, tol):
            continue
        res.append(vv)
        last = vv
    if keep_ends and len(res) > 1 and points_equal_2d(res[0], res[-1], tol):
        return res
    return res


# 分枝分析
#&&% analyze_polygon_branches

def analyze_polygon_branches(PL, lines, p1=None, tol=0.01):
    t0 = _log_start("analyze_polygon_branches", f"n_lines={len(lines) if lines else 0}")
    res = {"junctions": [], "branches": [], "stats": {"count": 0}}
    if not PL or not lines:
        _log_end("analyze_polygon_branches", t0, ok=False, detail="empty")
        return res
    for ln in lines:
        p1, p2 = _line_endpoints(ln)
        if p1 is None or p2 is None:
            continue
        on1 = any(points_equal_2d(p1, v, tol) for v in PL)
        on2 = any(points_equal_2d(p2, v, tol) for v in PL)
        if on1 != on2:
            res["junctions"].append(p1 if on1 else p2)
            res["branches"].append(ln)
    res["stats"]["count"] = len(res["branches"])
    _log_end("analyze_polygon_branches", t0, ok=True, detail=f"count={res['stats']['count']}")
    return res


# 过滤两端点在集合内的线段
#&&% remove_lines_with_both_vertices_in_set

def remove_lines_with_both_vertices_in_set(lines, vertices_set, tol=0.01):
    res = []
    for ln in lines:
        p1, p2 = _line_endpoints(ln)
        if p1 is None or p2 is None:
            res.append(ln)
            continue
        in1 = any(points_equal_2d(p1, v, tol) for v in vertices_set)
        in2 = any(points_equal_2d(p2, v, tol) for v in vertices_set)
        if in1 and in2:
            continue
        res.append(ln)
    return res


# 提取闭合多边形（计算）
#&&% compute_closed_polygons_from_lines

def compute_closed_polygons_from_lines(lines, tol=0.01, max_steps=20000):
    t0 = _log_start("compute_closed_polygons_from_lines", f"n={len(lines) if lines else 0}")
    if not lines:
        _log_end("compute_closed_polygons_from_lines", t0, ok=False, detail="empty")
        return []
    if polygonize is None:
        _log_end("compute_closed_polygons_from_lines", t0, ok=False, detail="no shapely")
        return []
    try:
        segs = []
        for ln in lines:
            p1, p2 = _line_endpoints(ln)
            if p1 is None or p2 is None:
                continue
            segs.append(LineString([(p1[0], p1[1]), (p2[0], p2[1])]))
        polys = list(polygonize(segs))
        res = []
        for poly in polys:
            coords = list(poly.exterior.coords)
            res.append([(x, y, 0.0) for (x, y) in coords])
        _log_end("compute_closed_polygons_from_lines", t0, ok=True, detail=f"count={len(res)}")
        return res
    except Exception as e:
        sys_logger.info(f"[compute_closed_polygons_from_lines] 异常: {e}")
        _log_end("compute_closed_polygons_from_lines", t0, ok=False)
        return []


# 线段集转顶点序列
#&&% extract_polygon_vertices_from_lines

def extract_polygon_vertices_from_lines(lines, tol=0.01):
    polys = compute_closed_polygons_from_lines(lines, tol=tol)
    return polys[0] if polys else []


# 线段集合差集
#&&% subtract_line_sets_undirected

def subtract_line_sets_undirected(lines1, lines2, tol=0.01):
    res = []
    for ln in lines1:
        if not any(lines_equal_undirected(ln, x, tol) for x in lines2):
            res.append(ln)
    return res


# 最终多边形整理
#&&% compute_final_polygons_from_lines

def compute_final_polygons_from_lines(lines, tol=0.01, max_steps=20000):
    polys = compute_closed_polygons_from_lines(lines, tol=tol, max_steps=max_steps)
    unique = []
    for p in polys:
        if not any(len(p) == len(q) and all(points_equal_2d(a, b, tol) for a, b in zip(p, q)) for q in unique):
            unique.append(p)
    unique.sort(key=lambda p: abs(polygon_area_signed(p)), reverse=True)
    return unique


# 线段转端点对
#&&% convert_lines_to_endpoint_pairs

def convert_lines_to_endpoint_pairs(segments):
    res = []
    for ln in segments:
        p1, p2 = _line_endpoints(ln)
        if p1 is None or p2 is None:
            continue
        res.append([p1, p2])
    return res


# 合并线段建议
#&&% merge_segments_from_lines

def merge_segments_from_lines(LB, tol=0.01):
    t0 = _log_start("merge_segments_from_lines", f"n={len(LB) if LB else 0}")
    pairs = convert_lines_to_endpoint_pairs(LB)
    groups = []
    suggestions = []
    used = set()
    for i, seg in enumerate(pairs):
        if i in used:
            continue
        used.add(i)
        group = [seg]
        for j in range(i + 1, len(pairs)):
            if j in used:
                continue
            a1, a2 = seg
            b1, b2 = pairs[j]
            if points_equal_2d(a2, b1, tol) or points_equal_2d(a1, b2, tol):
                group.append(pairs[j])
                used.add(j)
        groups.append(group)
    for g in groups:
        if len(g) > 1:
            suggestions.append((g[0][0], g[-1][1]))
    _log_end("merge_segments_from_lines", t0, ok=True, detail=f"suggestions={len(suggestions)}")
    return {"merged_groups": groups, "suggestions": suggestions, "residual": []}

