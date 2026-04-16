# -*- coding: utf-8 -*-
"""print_area_analysis.py

本脚本用于“打印区域(打印框)”分析。

约束与假设：
- 打印范围使用“矩形多段线”表示。
- 打印多段线之间不应放置仅用于分隔的矩形多段线（否则会干扰包含关系）。
- 允许存在“外包大矩形”包裹若干打印多段线：脚本采用“极大矩形”算法识别真实打印区域。
- 使用“外包盒短边的万分之五(0.0005*w_short)”作为动态容差：
  - 用于矩形识别（顶点聚类/坐标分类）
  - 用于多段线去重（空间重叠）
  - 用于包含关系判断
- 允许 1:100 系列与 1:1 系列（通过 *0.01 得到）在同一文件中同时出现。

输出：
- 提供：
  1) 严格标准匹配（只匹配容差内命中的 288 标准值）
  2) 适配匹配（仅对短边/长边落在 288 标准支持范围内的矩形，返回最近标准）
  3) 打印区域提取（模型空间 + 各布局空间）

注意：
- 脚本为“纯函数式模块”（无类），但根据需求包含必要的 CAD 数据库写操作：
  - 删除伪打印区域外框（并在删除前用 4 条直线保留其边界信息）。

路径可随 /cad 项目一起迁移，使用 system.licad 的 C 连接 CAD。
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# -----------------------------------------------------------------------------
# bootstrap: allow free migration under /cad
# -----------------------------------------------------------------------------
current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent
sys.path.insert(0, str(current))

from system.project_setup import PathConfig  # noqa: F401
from system.licad import C
from system.CAD_com_utils import retry_on_busy

# CAD_selection 提供的选择与早绑定 get/set
from system.CAD_selection import (
    select_polyline,
    select_polyline_chuantong,
    get_attr,
    set_attr,
)

# 空间/布局辅助内生化，避免再依赖遗留 CAD_file_operations.py
def get_obj_loc(obj: Any) -> int:
    """1=模型空间,0=图纸空间,-1=其他"""
    doc = C.doc
    owner_btr = doc.ObjectIdToObject(obj.OwnerID)
    btr_name = owner_btr.Name
    layout_block_names = set()
    try:
        for layout in doc.Layouts:
            try:
                layout_name = str(layout.Name or "")
                if layout_name.lower() == "model":
                    continue
                layout_block_names.add(str(layout.Block.Name or ""))
            except Exception:
                continue
    except Exception:
        pass
    if str(btr_name).upper() == "*MODEL_SPACE":
        return 1
    if str(btr_name).upper().startswith("*PAPER_SPACE") or str(btr_name) in layout_block_names:
        return 0
    return -1


def set_space_mode(mode_val: int) -> bool:
    doc = C.doc
    doc.SetVariable("TILEMODE", mode_val)
    if mode_val == 0:
        doc.MSpace = False
    return True


def switch_to_layout(layout_name: str, retry: int = 10, delay: float = 0.5) -> bool:
    doc = C.doc
    for _ in range(retry):
        try:
            lay = doc.Layouts.Item(layout_name)
            doc.ActiveLayout = lay
            C.acad.ActiveDocument = doc
            return True
        except Exception:
            time.sleep(delay)
    return False


def get_layout_names(exclude_model: bool = False) -> List[str]:
    doc = C.doc
    out = []
    for layout in doc.Layouts:
        name = layout.Name
        if exclude_model and name == "Model":
            continue
        out.append(name)
    return out


# -----------------------------------------------------------------------------
# 标准打印框：48 + (100%,110%,120%) + (*1, *0.01) => 288
# -----------------------------------------------------------------------------
LB_dayingkuang: List[Tuple[int, int, int]] = [
    (118900, 84100, 100),  (178350, 126150, 150),   (59450, 42050, 50),    (29725, 21025, 25),
    (133800, 84100, 100),  (200700, 126150, 150),   (66900, 42050, 50),    (33450, 21025, 25),
    (148600, 84100, 100),  (222900, 126150, 150),   (74300, 42050, 50),    (37150, 21025, 25),
    (84100,  59400, 100),  (126150, 89100,  150),   (42050, 29700, 50),    (21025, 14850, 25),
    (105100, 59400, 100),  (157650, 89100,  150),   (52550, 29700, 50),    (26275, 14850, 25),
    (126100, 59400, 100),  (189150, 89100,  150),   (63050, 29700, 50),    (31525, 14850, 25),
    (147100, 59400, 100),  (220650, 89100,  150),   (73550, 29700, 50),    (36775, 14850, 25),
    (59400,  42000, 100),  (89100,  63000,  150),   (29700, 21000, 50),    (14850, 10500, 25),
    (74300,  42000, 100),  (111450, 63000,  150),   (37150, 21000, 50),    (18575, 10500, 25),
    (89100,  42000, 100),  (133650, 63000,  150),   (44550, 21000, 50),    (22275, 10500, 25),
    (104100, 42000, 100),  (156150, 63000,  150),   (52050, 21000, 50),    (26025, 10500, 25),
    (42000,  29700, 100),  (63000,  44550,  150),   (21000, 14850, 50),    (10500, 7425,  25),
]

drawing_map_ml: List[Tuple[str, str]] = [
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

drawing_map: List[str] = [
    "ISO_A0_(841.00_x_1189.00_MM)", "ISO_A0_(841.00_x_1189.00_MM)", "ISO_A0_(841.00_x_1189.00_MM)", "ISO_A0_(841.00_x_1189.00_MM)",
    "UserDefinedMetric (1338.00 x 841.00毫米)", "UserDefinedMetric (1338.00 x 841.00毫米)", "UserDefinedMetric (1338.00 x 841.00毫米)", "UserDefinedMetric (1338.00 x 841.00毫米)",
    "UserDefinedMetric (1486.00 x 841.00毫米)", "UserDefinedMetric (1486.00 x 841.00毫米)", "UserDefinedMetric (1486.00 x 841.00毫米)", "UserDefinedMetric (1486.00 x 841.00毫米)",
    "ISO_A1_(841.00_x_594.00_MM)", "ISO_A1_(841.00_x_594.00_MM)", "ISO_A1_(841.00_x_594.00_MM)", "ISO_A1_(841.00_x_594.00_MM)",
    "UserDefinedMetric (1051.00 x 594.00毫米)", "UserDefinedMetric (1051.00 x 594.00毫米)", "UserDefinedMetric (1051.00 x 594.00毫米)", "UserDefinedMetric (1051.00 x 594.00毫米)",
    "UserDefinedMetric (1261.00 x 594.00毫米)", "UserDefinedMetric (1261.00 x 594.00毫米)", "UserDefinedMetric (1261.00 x 594.00毫米)", "UserDefinedMetric (1261.00 x 594.00毫米)",
    "UserDefinedMetric (1471.00 x 594.00毫米)", "UserDefinedMetric (1471.00 x 594.00毫米)", "UserDefinedMetric (1471.00 x 594.00毫米)", "UserDefinedMetric (1471.00 x 594.00毫米)",
    "ISO_A2_(594.00_x_420.00_MM)", "ISO_A2_(594.00_x_420.00_MM)", "ISO_A2_(594.00_x_420.00_MM)", "ISO_A2_(594.00_x_420.00_MM)",
    "UserDefinedMetric (743.00 x 420.00毫米)", "UserDefinedMetric (743.00 x 420.00毫米)", "UserDefinedMetric (743.00 x 420.00毫米)", "UserDefinedMetric (743.00 x 420.00毫米)",
    "UserDefinedMetric (891.00 x 420.00毫米)", "UserDefinedMetric (891.00 x 420.00毫米)", "UserDefinedMetric (891.00 x 420.00毫米)", "UserDefinedMetric (891.00 x 420.00毫米)",
    "UserDefinedMetric (1041.00 x 420.00毫米)", "UserDefinedMetric (1041.00 x 420.00毫米)", "UserDefinedMetric (1041.00 x 420.00毫米)", "UserDefinedMetric (1041.00 x 420.00毫米)",
    "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)",
]

assert len(LB_dayingkuang) == 48
assert len(drawing_map_ml) == 48
assert len(drawing_map) == 48


# -----------------------------------------------------------------------------
# geometry helpers
# -----------------------------------------------------------------------------

def _safe_delete(ent: Any) -> bool:
    try:
        ent.Delete()
        return True
    except Exception:
        return False


def _bbox_xy(ent: Any) -> Optional[Tuple[float, float, float, float]]:
    """(minx,miny,maxx,maxy) or None"""
    try:
        ll, ur = ent.GetBoundingBox()
        minx, miny = float(ll[0]), float(ll[1])
        maxx, maxy = float(ur[0]), float(ur[1])
        if minx > maxx:
            minx, maxx = maxx, minx
        if miny > maxy:
            miny, maxy = maxy, miny
        return (minx, miny, maxx, maxy)
    except Exception:
        return None


def _bbox_wh_from_bbox(b: Tuple[float, float, float, float]) -> Tuple[float, float]:
    minx, miny, maxx, maxy = b
    dx = abs(maxx - minx)
    dy = abs(maxy - miny)
    w = min(dx, dy)
    h = max(dx, dy)
    return (w, h)


def _eps_from_short_side(short_side: float) -> float:
    return max(0.0, float(short_side) * 0.0005)


def _cluster_1d(values: List[float], tol: float) -> List[float]:
    """聚类后返回代表值（按排序扫描）"""
    if not values:
        return []
    vals = sorted(values)
    clusters: List[List[float]] = [[vals[0]]]
    for v in vals[1:]:
        if abs(v - clusters[-1][-1]) <= tol:
            clusters[-1].append(v)
        else:
            clusters.append([v])
    # 用均值作为代表
    return [sum(c) / len(c) for c in clusters]


def _cluster_points_2d(points: List[Tuple[float, float]], tol: float) -> List[Tuple[float, float]]:
    """在 tol 内视为同一点，返回唯一点集合（代表点用均值）"""
    reps: List[Tuple[float, float]] = []
    buckets: List[List[Tuple[float, float]]] = []
    for (x, y) in points:
        placed = False
        for i, (rx, ry) in enumerate(reps):
            if abs(x - rx) <= tol and abs(y - ry) <= tol:
                buckets[i].append((x, y))
                # 更新代表
                cx = sum(p[0] for p in buckets[i]) / len(buckets[i])
                cy = sum(p[1] for p in buckets[i]) / len(buckets[i])
                reps[i] = (cx, cy)
                placed = True
                break
        if not placed:
            reps.append((x, y))
            buckets.append([(x, y)])
    return reps


# -----------------------------------------------------------------------------
# polyline vertex extraction (two coordinate structures)
# -----------------------------------------------------------------------------

def _get_polyline_points(poly: Any) -> List[Tuple[float, float]]:
    """尽力提取2D顶点列表。"""
    # 1) Coordinates (LWPOLYLINE)
    try:
        coords = list(get_attr(poly, "Coordinates"))
        if coords:
            # 有的传统多段线可能是 (x,y,z) 或 (x,y)；这里尝试识别
            if len(coords) % 2 == 0:
                pts = [(float(coords[i]), float(coords[i + 1])) for i in range(0, len(coords), 2)]
                return pts
            if len(coords) % 3 == 0:
                pts = [(float(coords[i]), float(coords[i + 1])) for i in range(0, len(coords), 3)]
                return pts
    except Exception:
        pass

    # 2) NumberOfVertices + GetPointAt
    try:
        n = int(get_attr(poly, "NumberOfVertices"))
        pts: List[Tuple[float, float]] = []
        for i in range(n):
            p = poly.GetPointAt(i)
            pts.append((float(p[0]), float(p[1])))
        return pts
    except Exception:
        pass

    # 3) Vertices collection
    try:
        pts = []
        for v in poly:
            p = v.Coordinates
            pts.append((float(p[0]), float(p[1])))
        if pts:
            return pts
    except Exception:
        pass

    return []


# -----------------------------------------------------------------------------
# rectangle polyline detection (deep algorithm)
# -----------------------------------------------------------------------------

def is_rectangular_polyline(poly: Any) -> Tuple[bool, Dict[str, Any]]:
    """严格矩形判定。

    规则：
    - 顶点数 < 4 => False
    - 对 n>=4 顶点：
      * 动态 tol = bbox短边 * 0.0005
      * 在 tol 内合并顶点 => 只能有4个不同位置点
      * 这4点的 x 值只能分成2类；y 值只能分成2类（均在 tol 内）

    返回：(ok, info)
    info 包含：bbox,w,h,short,eps,n_pts,n_unique_pts,x_clusters,y_clusters
    """
    b = _bbox_xy(poly)
    if b is None:
        return False, {"reason": "no_bbox"}
    w, h = _bbox_wh_from_bbox(b)
    short = min(w, h)
    eps = _eps_from_short_side(short)

    pts = _get_polyline_points(poly)
    if len(pts) < 4:
        return False, {"reason": "lt4", "bbox": b, "w": w, "h": h, "eps": eps, "n_pts": len(pts)}

    uniq = _cluster_points_2d(pts, tol=eps)
    if len(uniq) != 4:
        return False, {
            "reason": "unique_pts_not4",
            "bbox": b,
            "w": w,
            "h": h,
            "short": short,
            "eps": eps,
            "n_pts": len(pts),
            "n_unique_pts": len(uniq),
        }

    xs = [p[0] for p in uniq]
    ys = [p[1] for p in uniq]
    xcls = _cluster_1d(xs, tol=eps)
    ycls = _cluster_1d(ys, tol=eps)

    if len(xcls) != 2 or len(ycls) != 2:
        return False, {
            "reason": "xy_clusters_not2",
            "bbox": b,
            "w": w,
            "h": h,
            "short": short,
            "eps": eps,
            "n_pts": len(pts),
            "n_unique_pts": len(uniq),
            "x_clusters": xcls,
            "y_clusters": ycls,
        }

    return True, {
        "bbox": b,
        "w": w,
        "h": h,
        "short": short,
        "eps": eps,
        "n_pts": len(pts),
        "n_unique_pts": len(uniq),
        "x_clusters": xcls,
        "y_clusters": ycls,
    }


# -----------------------------------------------------------------------------
# selection: get polylines in current doc (two kinds)
# -----------------------------------------------------------------------------

POLYLINE_OBJECT_NAMES = {
    "AcDbPolyline",
    "AcDbLwPolyline",
    "AcDb2dPolyline",
    "AcDb3dPolyline",
    "Polyline",
    "LWPOLYLINE",
}


@retry_on_busy(max_retries=10, base_delay=0.2)
def _get_collection_count(collection: Any) -> int:
    return int(collection.Count)


@retry_on_busy(max_retries=10, base_delay=0.2)
def _get_collection_item(collection: Any, index: int) -> Any:
    return collection.Item(index)


def _iter_collection_entities(collection: Any):
    try:
        count = _get_collection_count(collection)
    except Exception:
        return
    for index in range(count):
        try:
            yield _get_collection_item(collection, index)
        except Exception:
            continue


def _collect_all_doc_polylines() -> List[Any]:
    """直接枚举 ModelSpace + 每个 Layout.Block，避免只取当前活动空间。"""
    doc = C.doc
    out: List[Any] = []

    for ent in _iter_collection_entities(doc.ModelSpace):
        try:
            if str(getattr(ent, "ObjectName", "")) in POLYLINE_OBJECT_NAMES:
                out.append(ent)
        except Exception:
            continue

    try:
        layouts = doc.Layouts
    except Exception:
        layouts = None

    if layouts is not None:
        for layout in layouts:
            try:
                layout_name = str(layout.Name or "")
                if layout_name.lower() == "model":
                    continue
                block = layout.Block
            except Exception:
                continue
            for ent in _iter_collection_entities(block):
                try:
                    if str(getattr(ent, "ObjectName", "")) in POLYLINE_OBJECT_NAMES:
                        out.append(ent)
                except Exception:
                    continue

    return out

def select_all_polylines(autocast: bool = True) -> List[Any]:
    """获取全图多段线，覆盖模型空间与全部布局空间。"""
    collected = _collect_all_doc_polylines()
    if collected:
        return collected
    lb1 = select_polyline(autocast=autocast) or []
    lb2 = select_polyline_chuantong(autocast=autocast) or []
    return list(lb1) + list(lb2)


# -----------------------------------------------------------------------------
# classify by space: model and paper-space block table records
# -----------------------------------------------------------------------------

def get_rect_polylines_by_space(polylines: List[Any]) -> Dict[str, Any]:
    """返回当前DWG中矩形多段线：

    {
      "model": [poly,...],
      "papers": { "*Paper_Space": [poly,...], "*Paper_Space0": [...], ... },
      "other": [poly,...],
      "info": { handle: {rect_info...}, ... }
    }

    备注：paper space 这里按 owner BTR 名称分组（能覆盖多个布局/视口场景）。
    """
    doc = C.doc
    layout_block_names: set[str] = set()
    try:
        for layout in doc.Layouts:
            try:
                layout_name = str(layout.Name or "")
                if layout_name.lower() == "model":
                    continue
                layout_block_names.add(str(layout.Block.Name or ""))
            except Exception:
                continue
    except Exception:
        pass
    out_model: List[Any] = []
    out_other: List[Any] = []
    out_papers: Dict[str, List[Any]] = {}
    info: Dict[str, Dict[str, Any]] = {}

    for pl in polylines:
        ok, ri = is_rectangular_polyline(pl)
        if not ok:
            continue
        try:
            handle = str(get_attr(pl, "Handle"))
        except Exception:
            handle = str(id(pl))
        info[handle] = ri

        try:
            owner_btr = doc.ObjectIdToObject(pl.OwnerID)
            btr_name = str(owner_btr.Name)
        except Exception:
            out_other.append(pl)
            continue

        if btr_name.upper() == "*MODEL_SPACE":
            out_model.append(pl)
        elif btr_name.upper().startswith("*PAPER_SPACE") or btr_name in layout_block_names:
            out_papers.setdefault(btr_name, []).append(pl)
        else:
            out_other.append(pl)

    return {"model": out_model, "papers": out_papers, "other": out_other, "info": info}


# -----------------------------------------------------------------------------
# build standard 288 table (cached)
# -----------------------------------------------------------------------------

def build_std288(
    scales: Tuple[float, ...] = (1.0, 1.1, 1.2),
    real_scales: Tuple[float, ...] = (1.0, 0.01),
) -> List[Dict[str, Any]]:
    """构造 288 标准表（只用 bbox 尺寸匹配）。"""
    std: List[Dict[str, Any]] = []
    for i, (a, b, denom) in enumerate(LB_dayingkuang):
        base_w = float(min(a, b))
        base_h = float(max(a, b))
        paper_code, ratio_str = drawing_map_ml[i]
        plot_name = drawing_map[i]
        for s in scales:
            for k in real_scales:
                w = base_w * s * k
                h = base_h * s * k
                if w > h:
                    w, h = h, w
                std.append(
                    {
                        "base_i": i,
                        "plot_name": plot_name,
                        "ratio": ratio_str,
                        "paper": paper_code,
                        "base_w": base_w,
                        "base_h": base_h,
                        "base_denom": int(denom),
                        "w": float(w),
                        "h": float(h),
                        "s": float(s),
                        "k": float(k),
                        "scale": float(s),  # alias
                    }
                )
    # 便于 debug
    std.sort(key=lambda d: (d["w"], d["h"], d["paper"], d["ratio"], d["s"], d["k"]))
    return std


_STD288_CACHE: Optional[List[Dict[str, Any]]] = None
_STD288_BOUNDS_CACHE: Optional[tuple[float, float]] = None


def get_std288_cached() -> List[Dict[str, Any]]:
    global _STD288_CACHE
    if _STD288_CACHE is None:
        _STD288_CACHE = build_std288()
    return _STD288_CACHE


def get_std288_bounds() -> tuple[float, float]:
    global _STD288_BOUNDS_CACHE
    if _STD288_BOUNDS_CACHE is None:
        std = get_std288_cached()
        min_short = min(float(item["w"]) for item in std)
        max_long = max(float(item["h"]) for item in std)
        _STD288_BOUNDS_CACHE = (min_short, max_long)
    return _STD288_BOUNDS_CACHE


# -----------------------------------------------------------------------------
# match helpers
# -----------------------------------------------------------------------------

def _orientation_from_bbox(dx: float, dy: float) -> int:
    """横竖信息：0=横向(dx>=dy), 1=竖向(dx<dy)"""
    return 0 if dx >= dy else 1


def _match_score(w: float, h: float, ws: float, hs: float) -> float:
    """归一化评分（越小越好）。对称：同时考虑对象与标准的 eps。"""
    dw = abs(w - ws)
    dh = abs(h - hs)
    eo = max(_eps_from_short_side(w), 1e-12)
    es = max(_eps_from_short_side(ws), 1e-12)
    return max(dw / eo, dh / eo, dw / es, dh / es)


def _within_supported_bounds(w: float, h: float) -> bool:
    min_short, max_long = get_std288_bounds()
    eps = _eps_from_short_side(w)
    return w >= (min_short - eps) and h <= (max_long + eps)


# -----------------------------------------------------------------------------
# #4: 判断“标准打印多段线”（严格匹配288）
# -----------------------------------------------------------------------------

def check_strict_standard_print_polyline(poly: Any) -> Any:
    """如果 poly 的 bbox 属于 288 标准之一（按动态容差/对称判据），返回：

    (plot_name, ratio, paper_code, orient, scale, standard_flag)

    - orient: 0横 1竖
    - scale: 1.0/1.1/1.2

    不属于则返回 0
    """
    b = _bbox_xy(poly)
    if b is None:
        return 0
    minx, miny, maxx, maxy = b
    dx = abs(maxx - minx)
    dy = abs(maxy - miny)
    w = min(dx, dy)
    h = max(dx, dy)

    orient = _orientation_from_bbox(dx, dy)
    eo = _eps_from_short_side(w)

    best = None
    best_score = None

    for s in get_std288_cached():
        ws, hs = float(s["w"]), float(s["h"])
        dw = abs(w - ws)
        dh = abs(h - hs)
        es = _eps_from_short_side(ws)

        # 对称判据：dw/dh 同时 <= eo 与 <= es
        if not (dw <= eo and dh <= eo and dw <= es and dh <= es):
            continue

        sc = _match_score(w, h, ws, hs)
        if best is None or sc < best_score:
            best = s
            best_score = sc

    if best is None:
        return 0

    return (best["plot_name"], best["ratio"], best["paper"], orient, float(best["scale"]), 1)


# -----------------------------------------------------------------------------
# #5: 适配匹配“最接近的标准打印多段线”
# -----------------------------------------------------------------------------

def match_nearest_standard_print(poly: Any) -> Any:
    """对支持范围内的矩形多段线，找最接近的 288 标准，返回：

    (plot_name, ratio, paper_code, orient, scale, standard_flag)

    支持范围：
    - 短边 >= 288 标准中的最小短边（允许动态容差）
    - 长边 <= 288 标准中的最长长边（允许动态容差）

    不在支持范围内，或对象无 bbox，则返回 0。
    """
    b = _bbox_xy(poly)
    if b is None:
        return 0
    minx, miny, maxx, maxy = b
    dx = abs(maxx - minx)
    dy = abs(maxy - miny)
    w = min(dx, dy)
    h = max(dx, dy)

    strict = check_strict_standard_print_polyline(poly)
    if strict != 0:
        return strict

    if not _within_supported_bounds(w, h):
        return 0

    orient = _orientation_from_bbox(dx, dy)

    best = None
    best_score = None

    for s in get_std288_cached():
        ws, hs = float(s["w"]), float(s["h"])
        sc = _match_score(w, h, ws, hs)
        if best is None or sc < best_score:
            best = s
            best_score = sc

    if best is None:
        return 0

    return (best["plot_name"], best["ratio"], best["paper"], orient, float(best["scale"]), 0)


def match_standard_print_by_mode(poly: Any, mode: str = "basic") -> Any:
    """按模式返回标准打印匹配结果。

    - basic: 只接受严格命中的 288 标准区域
    - adaptive / purified_adaptive: 使用适配匹配
    """
    normalized = str(mode or "basic").strip().lower().replace("-", "_")
    if normalized == "basic":
        return check_strict_standard_print_polyline(poly)
    if normalized in {"adaptive", "purified_adaptive"}:
        return match_nearest_standard_print(poly)
    raise ValueError(f"不支持的打印区域匹配模式: {mode}")


# -----------------------------------------------------------------------------
# 去重（动态容差版本：pair_tol=max(eps_i, eps_j)）
# -----------------------------------------------------------------------------

def remove_duplicate_polylines_dynamic(
    polylines: List[Any],
    priority_layer: str = "dy_zhuanyong",
) -> List[Any]:
    """对矩形多段线去重（动态容差）。

    判定重复：两者 bbox 四个边界差值都 <= pair_tol
      pair_tol = max(eps(short_i), eps(short_j))

    决策：发生冲突时，优先保留 priority_layer 上的对象。

    返回：幸存对象列表

    注：本函数会物理删除冗余对象。
    """
    cached = []
    pr = str(priority_layer).lower()
    for pl in polylines:
        b = _bbox_xy(pl)
        if b is None:
            continue
        w, h = _bbox_wh_from_bbox(b)
        eps = _eps_from_short_side(min(w, h))
        try:
            layer = str(get_attr(pl, "Layer")).lower()
        except Exception:
            layer = ""
        cached.append({"obj": pl, "bbox": b, "eps": eps, "layer": layer, "removed": False})

    cached.sort(key=lambda it: it["bbox"][0])  # minx

    for i in range(len(cached)):
        a = cached[i]
        if a["removed"]:
            continue
        ax1, ay1, ax2, ay2 = a["bbox"]
        for j in range(i + 1, len(cached)):
            b = cached[j]
            if b["removed"]:
                continue
            bx1, by1, bx2, by2 = b["bbox"]

            pair_tol = max(a["eps"], b["eps"])
            if bx1 - ax1 > pair_tol:
                break

            is_dup = (
                abs(ax1 - bx1) <= pair_tol
                and abs(ay1 - by1) <= pair_tol
                and abs(ax2 - bx2) <= pair_tol
                and abs(ay2 - by2) <= pair_tol
            )
            if not is_dup:
                continue

            wa = 1 if a["layer"] == pr else 0
            wb = 1 if b["layer"] == pr else 0

            if wa >= wb:
                b["removed"] = True
                _safe_delete(b["obj"])
            else:
                a["removed"] = True
                _safe_delete(a["obj"])
                break

    return [it["obj"] for it in cached if not it["removed"]]


# -----------------------------------------------------------------------------
# 极大矩形分析（不被其他矩形包含）
# -----------------------------------------------------------------------------

def _contains_bbox(outer: Tuple[float, float, float, float], inner: Tuple[float, float, float, float], tol: float) -> bool:
    ox1, oy1, ox2, oy2 = outer
    ix1, iy1, ix2, iy2 = inner
    return (ox1 <= ix1 + tol) and (oy1 <= iy1 + tol) and (ox2 >= ix2 - tol) and (oy2 >= iy2 - tol)


def find_maximal_rect_polylines(rect_polylines: List[Any]) -> List[Any]:
    """返回极大矩形（不被其他矩形包含）。"""
    data = []
    for pl in rect_polylines:
        b = _bbox_xy(pl)
        if b is None:
            continue
        w, h = _bbox_wh_from_bbox(b)
        eps = _eps_from_short_side(min(w, h))
        diag = (w * w + h * h) ** 0.5
        data.append({"obj": pl, "bbox": b, "eps": eps, "diag": diag})

    maxima = []
    for i, a in enumerate(data):
        contained = False
        for j, b in enumerate(data):
            if i == j:
                continue
            tol = max(a["eps"], b["eps"])
            if _contains_bbox(b["bbox"], a["bbox"], tol=tol) and (b["diag"] > a["diag"] + tol):
                contained = True
                break
        if not contained:
            maxima.append(a["obj"])
    return maxima


def collect_pseudo_maximal_rect_polylines(rect_polylines: List[Any]) -> List[Any]:
    """非破坏性分析伪极大矩形。

    逻辑与 remove_pseudo_maxima_in_space 保持同源，但不会删除对象。
    若一个极大矩形内部包含至少一个 scale==1.0 的标准打印框，则认为它是伪极大矩形。
    为了覆盖“伪极大矩形包裹伪极大矩形”的情况，采用逻辑迭代剥离，直到稳定。
    """
    data = []
    for pl in rect_polylines:
        b = _bbox_xy(pl)
        if b is None:
            continue
        w, h = _bbox_wh_from_bbox(b)
        eps = _eps_from_short_side(min(w, h))
        diag = (w * w + h * h) ** 0.5
        data.append({"obj": pl, "bbox": b, "eps": eps, "diag": diag})

    pseudo_out: List[Any] = []
    active = list(data)
    for _ in range(10):
        if not active:
            break

        maxima = []
        for i, a in enumerate(active):
            contained = False
            for j, b in enumerate(active):
                if i == j:
                    continue
                tol = max(a["eps"], b["eps"])
                if _contains_bbox(b["bbox"], a["bbox"], tol=tol) and (b["diag"] > a["diag"] + tol):
                    contained = True
                    break
            if not contained:
                maxima.append(a)

        pseudo_round = []
        for mx in maxima:
            mb = mx["bbox"]
            meps = mx["eps"]
            is_pseudo = False
            for item in active:
                if item["obj"] is mx["obj"]:
                    continue
                tol = max(meps, item["eps"])
                if _contains_bbox(mb, item["bbox"], tol=tol) and _is_standard_scale_1(item["obj"]):
                    is_pseudo = True
                    break
            if is_pseudo:
                pseudo_round.append(mx)

        if not pseudo_round:
            break

        pseudo_out.extend(item["obj"] for item in pseudo_round)
        active = [item for item in active if item not in pseudo_round]

    return pseudo_out


# -----------------------------------------------------------------------------
# 伪打印区域极大矩形处理：
# - 若极大矩形包含至少一个“非1.1/1.2缩放”的标准打印框（scale==1.0，且k可为1.0或0.01）
#   则删除该极大矩形（删除前沿其四边绘制4条直线段保留信息）
# -----------------------------------------------------------------------------

def _add_edge_lines_and_delete(ent: Any) -> bool:
    """沿 bbox 四边添加 4 条 Line，然后删除 ent。"""
    doc = C.doc
    b = _bbox_xy(ent)
    if b is None:
        return False
    x1, y1, x2, y2 = b

    try:
        owner_btr = doc.ObjectIdToObject(ent.OwnerID)
    except Exception:
        owner_btr = doc.ModelSpace

    def add_line(p1: Tuple[float, float], p2: Tuple[float, float]):
        try:
            owner_btr.AddLine((p1[0], p1[1], 0.0), (p2[0], p2[1], 0.0))
        except Exception:
            # 忽略绘制失败
            pass

    add_line((x1, y1), (x2, y1))
    add_line((x2, y1), (x2, y2))
    add_line((x2, y2), (x1, y2))
    add_line((x1, y2), (x1, y1))

    return _safe_delete(ent)


def _is_standard_scale_1(poly: Any) -> bool:
    """判断 poly 是否属于标准值且 scale==1.0（允许k=1 或 0.01）。"""
    res = check_strict_standard_print_polyline(poly)
    if res == 0:
        return False
    # res=(plot,ratio,paper,orient,scale)
    try:
        return abs(float(res[4]) - 1.0) < 1e-9
    except Exception:
        return False


def remove_pseudo_maxima_in_space(rects: List[Any]) -> List[Any]:
    """在一个空间集合内：迭代删除伪极大矩形，直到稳定。

    返回：最终极大矩形（打印区域）列表
    """
    doc = C.doc

    # 先去重
    rects = remove_duplicate_polylines_dynamic(rects)

    for _ in range(10):
        maxima = find_maximal_rect_polylines(rects)
        if not maxima:
            return []

        # 计算 rects 的缓存 bbox
        rect_data = []
        for pl in rects:
            b = _bbox_xy(pl)
            if b is None:
                continue
            w, h = _bbox_wh_from_bbox(b)
            eps = _eps_from_short_side(min(w, h))
            rect_data.append({"obj": pl, "bbox": b, "eps": eps})

        pseudo: List[Any] = []
        for mx in maxima:
            mb = _bbox_xy(mx)
            if mb is None:
                continue
            mw, mh = _bbox_wh_from_bbox(mb)
            meps = _eps_from_short_side(min(mw, mh))

            is_pseudo = False
            for item in rect_data:
                if item["obj"] is mx:
                    continue
                tol = max(meps, item["eps"])
                if _contains_bbox(mb, item["bbox"], tol=tol):
                    # 关键：内部包含 scale==1.0 的标准框（48*2）
                    if _is_standard_scale_1(item["obj"]):
                        is_pseudo = True
                        break
            if is_pseudo:
                pseudo.append(mx)

        if not pseudo:
            # 稳定：返回当前 maxima（并再去重一次）
            return remove_duplicate_polylines_dynamic(maxima)

        # 删除伪外框（先画边线）
        for p in pseudo:
            _add_edge_lines_and_delete(p)

        try:
            doc.Regen(1)
        except Exception:
            pass

        # 删除后重新扫描 rects：剔除已经删除的对象
        alive: List[Any] = []
        for pl in rects:
            try:
                _ = get_attr(pl, "Handle")
                alive.append(pl)
            except Exception:
                continue
        rects = alive

    # 超过迭代次数，返回当前最大集（保守）
    return find_maximal_rect_polylines(rects)


# -----------------------------------------------------------------------------
# #6: 获取当前激活文件的打印多段线区域（模型空间 + 各布局空间）
# -----------------------------------------------------------------------------

def get_print_area_polylines() -> Dict[str, Any]:
    """获取当前激活文件的打印多段线区域。

    流程：
    1) 获取全部多段线（两类）
    2) 选择矩形多段线（深度矩形算法）
    3) 按空间分组
    4) 去重
    5) 极大矩形分析
    6) 删除伪打印区域外框（含画边线）并反复分析直到稳定

    返回：
    {
      "model": [rect_poly,...],
      "papers": { btr_name: [rect_poly,...], ... },
    }

    说明：
    - 本函数不返回打印信息字典（按你的要求）。
    - 各空间内“打印区域”以最终极大矩形列表表示。
    """
    all_pls = select_all_polylines(autocast=True)
    grouped = get_rect_polylines_by_space(all_pls)

    model_rects = grouped["model"]
    papers: Dict[str, List[Any]] = grouped["papers"]

    # 模型空间
    model_areas = remove_pseudo_maxima_in_space(model_rects)

    # 图纸空间：按 BTR 名称分别处理
    paper_areas: Dict[str, List[Any]] = {}
    for btr_name, lst in papers.items():
        paper_areas[btr_name] = remove_pseudo_maxima_in_space(lst)

    return {"model": model_areas, "papers": paper_areas}


def get_pseudo_maximal_polylines() -> Dict[str, Any]:
    """返回当前激活文件中的伪极大矩形区域，不修改图形数据库。"""
    all_pls = select_all_polylines(autocast=True)
    grouped = get_rect_polylines_by_space(all_pls)

    model_rects = grouped["model"]
    papers: Dict[str, List[Any]] = grouped["papers"]

    model_pseudo = collect_pseudo_maximal_rect_polylines(model_rects)
    paper_pseudo: Dict[str, List[Any]] = {}
    for btr_name, lst in papers.items():
        pseudo = collect_pseudo_maximal_rect_polylines(lst)
        if pseudo:
            paper_pseudo[btr_name] = pseudo

    return {"model": model_pseudo, "papers": paper_pseudo}


# -----------------------------------------------------------------------------
# 调试入口（可选）
# -----------------------------------------------------------------------------

def _debug_dump_standard_matches(rects: List[Any]) -> None:
    """打印每个矩形的严格/近似匹配结果（用于调试）"""
    for pl in rects:
        strict = check_strict_standard_print_polyline(pl)
        near = match_nearest_standard_print(pl)
        try:
            h = str(get_attr(pl, "Handle"))
        except Exception:
            h = "?"
        print("Handle", h, "strict=", strict, "near=", near)


if __name__ == "__main__":
    # 仅用于手工测试：
    # 1) 扫描矩形
    # 2) 打印模型空间打印区域数量
    # 3) 输出严格匹配信息
    all_pls = select_all_polylines(autocast=True)
    grouped = get_rect_polylines_by_space(all_pls)

    print("[INFO] rects model:", len(grouped["model"]))
    print("[INFO] rects paper groups:", {k: len(v) for k, v in grouped["papers"].items()})

    areas = get_print_area_polylines()
    print("[RESULT] model print areas:", len(areas["model"]))
    print("[RESULT] paper print areas:", {k: len(v) for k, v in areas["papers"].items()})

    # 仅打印模型区域的匹配
    _debug_dump_standard_matches(areas["model"])
