#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第三部分 线面分析
几何分析相关函数

从 CAD_basic.py 拆分而来
"""

# 路径引导
import sys
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

# 导入系统模块
from system.project_setup import PathConfig
from system.licad import C
from system.CAD_com_utils import sys_logger, alias, retry_on_busy, retry_if_busy, SafeCOM, debuggable, timeit
from system.common_logger import checkpoint

# 第三方库
from shapely.geometry import Polygon, Point, LineString
from typing import Tuple, List
import math

# 获取常用对象
acad = C.acad
doc = C.doc
mp = C.mp
sp = C.sp

#&&&&%%  第三部分 线面分析
from typing import Tuple, List



#_____________________________________________________________________________________________________________________________________________

#  模块使用说明

"""
该模块研究dwg图纸中的线段、圆曲线、平面等基本几何问题

"""

#&&&% 角度计算
#&&% 计算直线角度
def compute_line_angle(line):#按绘制顺序度量线段角度
    """
    计算直线的方向角（单位：度），基于 StartPoint / EndPoint。
    非直线对象将抛出异常。
    0-360，从起点处画横线，旋转到终点的角度
    """

    try:
        x1, y1, _ = line.StartPoint
        x2, y2, _ = line.EndPoint
        dx = x2 - x1
        dy = y2 - y1
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        if angle_deg < 0:
            angle_deg += 360
        return angle_deg
    except AttributeError:
        print("[错误] 该对象不具备 StartPoint / EndPoint")
        return None


#&&&% 基础绘图
#&&% 绘制点
def draw_point(pt):
    """
    在模型空间绘制一个 AutoCAD 点实体。

    参数：
        pt: (x, y, z) 三维坐标元组

    返回：
        新创建的 Point 对象；失败时返回 None
    """
    try:
        # AutoCAD 的“点”由 AddPoint 创建，需传 VARIANT
        obj = mp.AddPoint(vtpnt(*pt))
        return obj
    except Exception as e:
        sys_logger.info(f"[错误] 无法绘制点: {e}")
        return None

#&&% 绘制直线
def draw_line(p1, p2):#从两点坐标返回直线段
    """
    在模型空间中绘制从 p1 到 p2 的直线段。

    参数：
        p1, p2: 三维坐标元组 (x, y, z)

    返回：
        新创建的直线对象（COM 对象）
    """
    try:
        line_obj = mp.AddLine(vtpnt(*p1), vtpnt(*p2))
        return line_obj
    except Exception as e:
        sys_logger.info(f"[错误] 无法绘制直线: {e}")
        return None


#&&% 绘制圆
def draw_circle(center, radius):
    """
    以 center 为圆心、radius 为半径绘制圆。

    参数：
        center: (x, y, z)
        radius: 浮点半径

    返回：
        新创建的 Circle 对象；失败时返回 None
    """
    try:
        obj = mp.AddCircle(vtpnt(*center), radius)
        return obj
    except Exception as e:
        sys_logger.info(f"[错误] 无法绘制圆: {e}")
        return None


#&&% 绘制正多边形
def draw_regular_polygon(center, radius, sides):
    """
    绘制正多边形（LWPolyline，已闭合）
    :param center: 圆心 (x,y,z)
    :param radius: 外接圆半径
    :param sides : 边数 ≥3
    """
    if sides < 3:
        print("[错误] 边数必须 ≥ 3"); return None
    cx, cy, cz = (center + (0.0,))[:3]

    pts_flat = []
    for k in range(sides):
        ang = 2 * math.pi * k / sides
        pts_flat.extend([cx + radius*math.cos(ang),
                         cy + radius*math.sin(ang)])

    try:
        v_pts = win32com.client.VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_R8,
            pts_flat
        )
        poly = mp.AddLightWeightPolyline(v_pts)
        poly.Closed = True
        return poly
    except Exception as e:
        sys_logger.info(f"[错误] 无法绘制正多边形: {e}")
        return None



#&&% 优先水平线
def prioritize_horizontal(lines, tol=0.5):
    """
    将列表中所有“水平”直线段（起点和终点的 y 差小于 tol）放在最前面，
    其它直线保留原有相对顺序。

    :param lines: 直线对象列表，每个对象具有 .StartPoint 和 .EndPoint 属性，
                  这两个属性应返回 (x, y, z) 或类似可下标的三元组。
    :param tol:   判定为水平的 y 方向容差（默认 0.5）
    :return:      新列表，水平直线段在前，非水平在后
    """
    horizontals = []
    non_horizontals = []
    for ln in lines:
        y1 = ln.StartPoint[1]
        y2 = ln.EndPoint[1]
        if abs(y1 - y2) < tol:
            horizontals.append(ln)
        else:
            non_horizontals.append(ln)
    return horizontals,non_horizontals
#&&&% 曲线处理

    
#&&% 获取样条曲线长度
def get_spline_length_by_conversion(spline_entity):#返回样条曲线的长度（按默认10分断拟合）
    
    """
    将样条曲线对象复制、高亮并通过 _SPLINEDIT 转为多段线，
    然后读取长度，并删除该多段线。

    返回：
        样条曲线转换后的长度值（float）
    """
    try:
        # Step 1：复制 spline 对象
        new_spline = spline_entity.Copy()

        # Step 2：显性高亮
        highlight_entity_by_bbox(new_spline)

        # Step 3：模拟命令 SPLINEDIT → P → Enter → Enter
        doc.SendCommand("_SPLINEDIT\nP\n\n\n")
        time.sleep(1.2)  # 等待 CAD 完成处理（可根据机器速度调整）

        # Step 4：获取新生成的对象（最后一个）
        last_index = doc.ModelSpace.Count - 1
        poly = doc.ModelSpace.Item(last_index)

        # Step 5：检查 Length 属性
        if hasattr(poly, "Length"):
            length = poly.Length
            poly.Delete()  # 删除临时 polyline
            return length
        else:
            print("[错误] 转换后对象没有 Length 属性")
            return None

    except Exception as e:
        sys_logger.info(f"[错误] 获取样条曲线长度失败：{e}")
        return None

#&&% 估算椭圆周长
def estimate_ellipse_length(ellipse):#返回椭圆长度
    """
    估算椭圆对象的长度（周长），使用 Ramanujan 公式。
    """
    try:
        a = ellipse.MajorRadius
        b = ellipse.MinorRadius

        pi = math.pi
        h = 3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b))
        length = pi * h
        return length
    except Exception as e:
        sys_logger.info(f"[错误] 无法估算椭圆长度: {e}")
        return None



#&&% 获取几何信息
def get_entity_geometry_info(obj):#返回图形关键几何信息
    """
    根据图元类型返回其关键几何信息：
    - 点：坐标
    - 直线：起点、终点、长度
    - 圆：圆心、半径、长度、面积
    - 椭圆：中心、主轴、次轴、长度、面积
    - 多段线：起点、终点、长度、面积（若闭合）
    - 样条曲线：起点、终点、长度（需转换），面积（若闭合）
    """
    try:
        name = obj.ObjectName.lower()

        # 点
        if "point" in name:
            return {"type": "Point", "position": obj.Coordinates}

        # 直线
        elif "line" in name and "xline" not in name:
            p1 = obj.StartPoint
            p2 = obj.EndPoint
            length = math.dist(p1, p2)
            return {"type": "Line", "start": p1, "end": p2, "length": length}

        # 圆
        elif "circle" in name:
            center = obj.Center
            radius = obj.Radius
            length = 2 * math.pi * radius
            area = math.pi * radius ** 2
            return {"type": "Circle", "center": center, "radius": radius, "length": length, "area": area}

        # 椭圆
        elif "ellipse" in name:
            center = obj.Center
            a = obj.MajorRadius
            b = obj.MinorRadius
            area = math.pi * a * b
            h = 3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b))
            length = math.pi * h  # Ramanujan 公式
            return {
                "type": "Ellipse",
                "center": center,
                "major_radius": a,
                "minor_radius": b,
                "length": length,
                "area": area
            }

        # 多段线
        elif "polyline" in name:
            coords = obj.Coordinates
            start = (coords[0], coords[1], 0)
            end = (coords[-2], coords[-1], 0)
            length = getattr(obj, "Length", 0)
            area = obj.Area if obj.Closed else 0
            return {
                "type": "Polyline",
                "start": start,
                "end": end,
                "length": length,
                "area": area
            }

        # 样条曲线（需转换测量）
        elif "spline" in name:
            p1 = obj.GetFitPoint(0)
            p2 = obj.GetFitPoint(obj.NumberOfFitPoints - 1)
            length = get_spline_length_by_conversion(obj)
            area = obj.Area if obj.Closed else 0
            return {
                "type": "Spline",
                "start": p1,
                "end": p2,
                "length": length,
                "area": area
            }

        else:
            return {"type": "Unknown", "ObjectName": obj.ObjectName}

    except Exception as e:
        return {"type": "Error", "message": str(e)}



##在两点确定的方向上，返回与对象点指定距离的点

#&&% 直线定距点
def points_on_line_at_distance_3d(
    p1: Tuple[float, float, float],
    p2: Tuple[float, float, float],
    px: Tuple[float, float, float],
    distance: float
) -> List[Tuple[float, float, float]]:
    """
    已知 px 在由 p1->p2 确定的直线上，返回在该直线上与 px 距离为 distance 的两个点。

    :param p1: 起点 (x1, y1, z1)
    :param p2: 终点 (x2, y2, z2)
    :param px: 参考点 (x, y, z)，位于直线上
    :param distance: 与 px 的目标距离
    :return: [(ax, ay, az), (bx, by, bz)]，分别为正向和反向移动 distance 后的点
    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    xx, yy, zz = px

    # 1) 计算方向向量并归一化
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    if length == 0:
        raise ValueError("p1 和 p2 重合，无法确定方向向量")
    ux, uy, uz = dx / length, dy / length, dz / length

    # 2) 沿正向和反向各移动 distance
    ax = xx + ux * distance
    ay = yy + uy * distance
    az = zz + uz * distance

    bx = xx - ux * distance
    by = yy - uy * distance
    bz = zz - uz * distance

    return [(ax, ay, az), (bx, by, bz)]


#&&&% 交点计算

# 找出一组直线段内的伪相交区域

#&&% 查找伪交点区域
def find_fake_intersection_regions(lines, tol=10, real_tol=0.01):
    """
    查找伪相交区域：对于任意线段 A 的端点 P，若：
    - 存在其他线段 B 满足 P 到 B 距离 < tol，且
    - 对所有 B，P 到 B 的距离 >= real_tol
    则判定为伪相交点。
    在模型空间中绘制圆（半径 1000）表示这些点。
    """
    ensure_layer("测试辅助")
    ms = doc.ModelSpace
    added = []

    def point_to_line_distance(p, a1, a2):
        x0, y0 = p[:2]
        x1, y1 = a1[:2]
        x2, y2 = a2[:2]
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0:
            return math.hypot(x0 - x1, y0 - y1)
        t = max(0, min(1, ((x0 - x1) * dx + (y0 - y1) * dy) / (dx*dx + dy*dy)))
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return math.hypot(x0 - proj_x, y0 - proj_y)

    for A in lines:
        try:
            p1 = A.StartPoint
            p2 = A.EndPoint
        except Exception:
            continue

        for pt in [p1, p2]:
            pt_key = tuple(round(c, 3) for c in pt)
            if pt_key in added:
                continue

            min_dist = 1e10
            has_near = False
            has_real_near = False

            for B in lines:
                if B == A:
                    continue
                try:
                    b1, b2 = B.StartPoint, B.EndPoint
                    dist = point_to_line_distance(pt, b1, b2)
                    if dist < tol:
                        has_near = True
                    if dist < real_tol:
                        has_real_near = True
                        break
                except:
                    continue

            if has_near and not has_real_near:
                ms.AddCircle(vtpnt(*pt), 1000).Layer = "测试辅助"
                added.append(pt_key)
                sys_logger.info(f"[OK] 伪相交区域点: {pt}")

    print("[OK] 伪相交区域绘制完成")



#&&&% 打断与删除
# 把区域内的直线段交点打断

#&&% 直线打断
def lines_daduan(start_point,end_point):#全部脚本统一采用三维坐标点模式

    """
    这个命令对于避免天正墙体没有出现不相交的覆盖是非常重要的，直接应用天正的tlinebk

    还要先处理假相交点区域待优化20250409

    """

    # 使用 f-string 语法将三维坐标变量插入命令字符串中
    start_point_str = f"{start_point[0]},{start_point[1]},{start_point[2]}"

    end_point_str = f"{end_point[0]},{end_point[1]},{end_point[2]}"

    command = f"tlinebk{chr(13)}{start_point_str}{chr(13)}{end_point_str}{chr(13)}{chr(13)}{chr(13)}"

    acad.ActiveDocument.SendCommand(command)






#找出一组直线段中的所有直线段中所有重复的线段并删除

#&&% 删除重复直线
def delete_duplicate_lines(lines, tol=0.01):
    """
    删除重复的直线段，仅保留每组中一条。

    参数：
        lines: 模型空间中所有线段对象列表（ObjectName 为 'AcDbLine'）
        tol: 距离容差，小于此值认为两点重合
    """
    def is_same_point(p1, p2):
        return all(abs(a - b) < tol for a, b in zip(p1, p2))

    def is_duplicate(line1, line2):
        try:
            a1, a2 = line1.StartPoint, line1.EndPoint
            b1, b2 = line2.StartPoint, line2.EndPoint
            return (
                (is_same_point(a1, b1) and is_same_point(a2, b2)) or
                (is_same_point(a1, b2) and is_same_point(a2, b1))
            )
        except:
            return False

    keep = []
    to_delete = []

    for i, line in enumerate(lines):
        is_dup = False
        for j in range(i):
            if is_duplicate(line, lines[j]):
                is_dup = True
                break
        if is_dup:
            to_delete.append(line)
        else:
            keep.append(line)

    count = 0
    for dup in to_delete:
        try:
            dup.Delete()
            count += 1
        except:
            continue

    sys_logger.info(f"[OK] 删除了 {count} 条重复直线段，保留 {len(keep)} 条。")
    return keep



#删除完全或局部重复线段

#&&% 删除冗余直线
def delete_redundant_lines(lines, tol=0.01):
    """
    删除重复线段和局部重复线段，只保留每组中的一条。
    """
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
        sq_len = (bx - ax)**2 + (by - ay)**2
        if dot > sq_len:
            return False
        return True

    def is_completely_duplicate(l1, l2):
        try:
            p1, p2 = l1.StartPoint, l1.EndPoint
            q1, q2 = l2.StartPoint, l2.EndPoint
            return (
                (is_same_point(p1, q1) and is_same_point(p2, q2)) or
                (is_same_point(p1, q2) and is_same_point(p2, q1))
            )
        except:
            return False

    def is_locally_duplicate(short_line, long_line):
        try:
            p1, p2 = short_line.StartPoint, short_line.EndPoint
            q1, q2 = long_line.StartPoint, long_line.EndPoint
            return point_on_segment(p1, q1, q2) and point_on_segment(p2, q1, q2)
        except:
            return False

    to_delete_handles = set()
    total = len(lines)

    for i in range(total):
        l1 = lines[i]
        h1 = l1.Handle
        if h1 in to_delete_handles:
            continue
        for j in range(i + 1, total):
            l2 = lines[j]
            h2 = l2.Handle
            if h2 in to_delete_handles:
                continue

            if is_completely_duplicate(l1, l2):
                to_delete_handles.add(h2)
            elif is_locally_duplicate(l2, l1):
                to_delete_handles.add(h2)
            elif is_locally_duplicate(l1, l2):
                to_delete_handles.add(h1)
                break

    deleted = 0
    for ent in lines:
        if ent.Handle in to_delete_handles:
            try:
                ent.Delete()
                deleted += 1
            except:
                continue

    sys_logger.info(f"[OK] 删除重复/局部重复线段 {deleted} 条，保留 {total - deleted} 条。")

#找出一组直线段中的孤立线段产生的交点


#&&% 查找孤立交点
def find_isolated_intersections(LB, tol=0.5):
    """
    找出线段列表 LB 中的孤立线段，并计算它们与其它线段的所有交点。

    用于人工标记的门窗位置

    参数：
      LB:   线段列表，每个元素是 [(x1,y1,z1), (x2,y2,z2)]
      tol:  端点重合判断容差

    返回：
      intersections: 交点列表，每个元素是 (x, y, z)
    """
    def segment_intersection(seg1, seg2, tol):
        """
        计算线段 seg1=(A,B) 与 seg2=(C,D) 的交点（二维），
        若相交且唯一，返回 (x, y, z)，否则返回 None。
        z 取 seg1 第一端点的 z。
        """
        (x1, y1, z1), (x2, y2, _) = seg1
        (x3, y3, _),  (x4, y4, _) = seg2

        # 方向向量
        r = (x2-x1, y2-y1)
        s = (x4-x3, y4-y3)
        # 叉积 r × s
        rxs = r[0]*s[1] - r[1]*s[0]
        if abs(rxs) < tol:
            return None  # 平行或共线，不处理
        # 解 t, u
        qp = (x3-x1, y3-y1)
        t = (qp[0]*s[1] - qp[1]*s[0]) / rxs
        u = (qp[0]*r[1] - qp[1]*r[0]) / rxs
        # 只考虑严格交于段内
        if -tol <= t <= 1+tol and -tol <= u <= 1+tol:
            xi = x1 + t*r[0]
            yi = y1 + t*r[1]
            zi = z1
            return (xi, yi, zi)
        return None

    # 1. 找出孤立线段
    isolated = []
    for i, seg in enumerate(LB):
        p1, p2 = seg
        shared = False
        for j, other in enumerate(LB):
            if i == j:
                continue
            q1, q2 = other
            if same_point(p1, q1, tol) or same_point(p1, q2, tol) \
            or same_point(p2, q1, tol) or same_point(p2, q2, tol):
                shared = True
                break
        if not shared:
            isolated.append(seg)

    # 2. 对每根孤立线段，与其余线段求交点
    intersections = []
    for seg in isolated:
        for other in LB:
            if other is seg:
                continue
            ip = segment_intersection(seg, other, tol)
            if ip is not None:
                intersections.append(ip)

    #删除孤立线段20250420
    for seg in isolated:

        seg.Delete()

    return intersections    


##doc.sendcommand("TSpOutline"+chr(13)+"41849.69465957, 12250.50102376, 0"+chr(13)+chr(13)+chr(13))

##doc.sendcommand("TRoflna"+chr(13)+"0"+chr(13))


#&&% 获取多边形内点
def get_inner_point_of_polygon(polygon: Polygon):
    """
    获取给定 polygon 的一个保证在其内部的点。

    参数：
        polygon (shapely.geometry.Polygon): 目标多边形

    返回：
        (x, y): 内部点坐标元组
    """
    if not isinstance(polygon, Polygon):
        raise ValueError("[错误] 输入必须是 shapely.geometry.Polygon")

    inner_point = polygon.representative_point()
    return inner_point.x, inner_point.y
#&&&% 轮廓提取


#&&%____________________________________________________       获取一组直线段所有的封闭多边形和外轮廓线       ________________
#…………………………………………………………………………………………………………………………………………………………………
# 线面分析 - 获取一组直线段所有的封闭多边形和外轮廓线

#__________________________________________________________________________________________________________________________
#…………………………………………………………………………………………………………………………………………………………………
#  使用说明

"""
获取一组直线段所有的封闭多边形和外轮廓线

主要函数有：
(1)寻找直线段组中最右下角封闭多边性
(2)从com边或顶点坐标列表用PL复线绘制多边形
(3)获取一组直线段的外轮廓线
(4)获取最右下角的封闭多边形不影响其他封闭多边形的连续边的顶点列表
(5)获取全部封闭多边形，但不完全
(6)获取全部封闭多边形

"""
#&&% 获取房间轮廓
def get_room_outline_from_point(x, y, z=0):## 获取输入点所在房间的轮廓
    """
    自动发送 TSpOutline 命令，从指定点获取房间轮廓。

    参数:
        x, y, z: 点的坐标，z 默认为 0。

    也许会有用处，能从多边形内点迅速得到多边形
        
    """
    try:
        point_str = f"{x},{y},{z}"
        cmd = (
            "TSpOutline" + chr(13) +  # 启动命令
            point_str + chr(13) +     # 输入点
            chr(13) +                 # 确认默认设置
            chr(13)                   # 确认生成
        )
        doc.SendCommand(cmd)
        sys_logger.info(f"[OK] 已请求获取点 ({x},{y},{z}) 的房间轮廓。")

    except Exception as e:
        sys_logger.info(f"[错误] 获取房间轮廓失败：{e}")


#&&% 连接闭合多段线
def connect_lines_to_polyline_if_closed(lines, tol=0.5):##判断一组闭合直线段是否构成封闭多段线，是就返回PL复线
    """
    判断线段是否首尾连接成闭合多边形，如果是，则绘制PL多段线。
    
    参数:
        lines: AutoCAD中选中的 AcDbLine 对象列表。
        tol: 容许的端点闭合误差。
    
    返回:
        多段线对象，或 None。
    """

    try:
        # 提取二维端点集合（忽略z）
        segments = []
        for ln in lines:
            try:
                p1 = (ln.StartPoint[0], ln.StartPoint[1])
                p2 = (ln.EndPoint[0], ln.EndPoint[1])
                segments.append((p1, p2))
            except Exception:
                continue

        if not segments:
            print("[警告]️ 无有效线段")
            return None

        # 构建连接链条
        used = set()
        sequence = [segments[0][0]]
        current = segments[0][1]
        used.add(0)

        while True:
            found = False
            for idx, (a, b) in enumerate(segments):
                if idx in used:
                    continue
                if Point(current).distance(Point(a)) < tol:
                    sequence.append(current)
                    current = b
                    used.add(idx)
                    found = True
                    break
                elif Point(current).distance(Point(b)) < tol:
                    sequence.append(current)
                    current = a
                    used.add(idx)
                    found = True
                    break
            if not found:
                break

        # 检查是否闭合
        if Point(current).distance(Point(sequence[0])) > tol:
            print("[错误] 线段未构成闭合区域")
            return None
        sequence.append(sequence[0])  # 闭合环

        # 构造二维点数组
        pts = []
        for pt in sequence:
            pts.extend([pt[0], pt[1]])

        # 绘制PL
        poly = doc.ModelSpace.AddLightWeightPolyline(vtFloat(pts))
        poly.Closed = True
        print("[OK] 成功绘制封闭PL线")
        return poly

    except Exception as e:
        sys_logger.info(f"[错误] Polyline 创建失败: {e}")
        return None


#&&% 判断闭合多边形
def is_closed_polygon_from_lines(lines, tol=0.5):##判断一组闭合直线段是否构成封闭多段线，不返回PL复线
    """
    判断一组 AutoCAD 直线段是否首尾连接形成闭合多边形。
    
    参数:
        lines: AcDbLine 类型的 COM 对象列表
        tol: 闭合判断容差，单位与CAD一致（如mm）

    返回:
        True 表示首尾闭合形成多边形，False 否则
    """
    try:
        # 提取二维端点 (x, y)
        segments = []
        for ln in lines:
            try:
                p1 = (ln.StartPoint[0], ln.StartPoint[1])
                p2 = (ln.EndPoint[0], ln.EndPoint[1])
                segments.append((p1, p2))
            except Exception:
                continue

        if not segments:
            return False

        # 构造首尾连接链
        used = set()
        sequence = [segments[0][0]]
        current = segments[0][1]
        used.add(0)

        while True:
            found = False
            for idx, (a, b) in enumerate(segments):
                if idx in used:
                    continue
                if Point(current).distance(Point(a)) < tol:
                    sequence.append(current)
                    current = b
                    used.add(idx)
                    found = True
                    break
                elif Point(current).distance(Point(b)) < tol:
                    sequence.append(current)
                    current = a
                    used.add(idx)
                    found = True
                    break
            if not found:
                break

        # 判断是否回到起点（闭合）
        if Point(current).distance(Point(sequence[0])) < tol and len(used) == len(segments):
            return True
        else:
            return False

    except Exception as e:
        sys_logger.info(f"[错误] 判断失败: {e}")
        return False

#&&% 判断同点
def same_point(p1, p2, tol=0.5):
    """判断两个点是否在容差范围内相同（只比较 X、Y 坐标）"""
    return abs(p1[0] - p2[0]) <= tol and abs(p1[1] - p2[1]) <= tol


#&&% 判断同线
def same_line(ln1, ln2, tol=0.5):
    """
    判断两条线段 ln1 和 ln2 是否“相同”
    线段被认为相同的条件是：
      ln1 的 StartPoint 与 ln2 的 StartPoint 近似相同且 ln1 的 EndPoint 与 ln2 的 EndPoint 近似相同，
      或者 ln1 的 StartPoint 与 ln2 的 EndPoint 近似相同且 ln1 的 EndPoint 与 ln2 的 StartPoint 近似相同。
    """
    p1 = tuple(ln1.StartPoint)
    p2 = tuple(ln1.EndPoint)
    q1 = tuple(ln2.StartPoint)
    q2 = tuple(ln2.EndPoint)

    return (same_point(p1, q1, tol) and same_point(p2, q2, tol)) or \
           (same_point(p1, q2, tol) and same_point(p2, q1, tol))


#&&% 计算绝对角度
def calculate_absolute_angle(line, P, tol=0.5):
    """
    计算线段（line）从点 P 出发的绝对角度（0-360°）
    如果 line 的起点等于 P，则返回从 P 到终点的角度，否则返回从 P 到起点的角度。
    """
    sp = tuple(line.StartPoint)
    ep = tuple(line.EndPoint)
    if same_point(sp, P, tol):
        dx = ep[0] - P[0]
        dy = ep[1] - P[1]
    else:
        dx = sp[0] - P[0]
        dy = sp[1] - P[1]
    return math.degrees(math.atan2(dy, dx)) % 360

#&&% 计算相对角度
def calculate_relative_angle(line, P, current_line, tol=0.5):
    """
    计算当前参考线（current_line）与候选线段（line）之间的相对角度，
    角度是以共点 P 为中心，当前线从 P 到其非 P 的端点的绝对角度为基准，
    计算 candidate line 与该基准角度之间顺时针或逆时针的角度差（逆时针方向）。
    结果为 0 到 360 之间的数值。
    """
    sp_current = tuple(current_line.StartPoint)
    ep_current = tuple(current_line.EndPoint)
    sp = tuple(line.StartPoint)
    ep = tuple(line.EndPoint)

    # 选择当前线段中不等于 P 的端点作为参考
    if same_point(sp_current, P, tol):
        current_point = ep_current
    else:
        current_point = sp_current

    def angle(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.degrees(math.atan2(dy, dx)) % 360

    angle_current = angle(P, current_point)
    # 对候选线段，选择不等于 P 的端点
    if same_point(sp, P, tol):
        target_point = ep
    else:
        target_point = sp
    angle_target = angle(P, target_point)
    angle_diff = (angle_target - angle_current) % 360
    return angle_diff

#####################
# 函数：查找给定点P经过的线段，按照绝对角度排序

#&&% 按角度查找线段
def find_lines_angle(lines, P, tol=0.5):
    """
    查找与指定点 P 共端点的所有线段，并按从 P 出发离开的绝对几何角度排序。

    参数:
        lines: 直线段对象列表，每个对象要求具备 StartPoint, EndPoint, Handle 属性。
        P: 三元组 (x, y, z)，目标共点。
        tol: 判断共点的容差（仅比较 x 和 y 坐标）。

    返回:
        按绝对角度从小到大排序的共点线段列表。
    """
    shared_lines = []
    P = tuple(P)
    sys_logger.info(f"调试：目标共点 P = {P}")
    
    for ln in lines:
        try:
            sp = tuple(ln.StartPoint)
            ep = tuple(ln.EndPoint)
            dx_sp = abs(sp[0] - P[0])
            dy_sp = abs(sp[1] - P[1])
            dx_ep = abs(ep[0] - P[0])
            dy_ep = abs(ep[1] - P[1])
            sys_logger.info(f"线段 {ln.Handle}: sp={sp} 差值=({dx_sp:.4f},{dy_sp:.4f}), ep={ep} 差值=({dx_ep:.4f},{dy_ep:.4f})")
            if (dx_sp <= tol and dy_sp <= tol) or (dx_ep <= tol and dy_ep <= tol):
                shared_lines.append(ln)
        except Exception as e:
            sys_logger.info(f"[警告]️ 跳过无效线段 {getattr(ln, 'Handle', '未知')} : {e}")
            continue

    shared_lines.sort(key=lambda ln: calculate_absolute_angle(ln, P, tol))
    print("调试：按绝对角度排序后的共点线段：")
    for ln in shared_lines:
        sys_logger.info(f"  线段 {ln.Handle}：角度 = {calculate_absolute_angle(ln, P, tol):.2f}°")
    return shared_lines

#####################
# 函数：查找与P共点的线段，按照与当前线段的相对角度排序

#&&% 查找共点线段
def find_lines_sharing_point(lines, P, current_line, tol=0.5):
    """
    查找与指定点 P 共端点的所有线段，并按从 current_line 逆时针旋转到其他线段的相对角度排序。
    其中 current_line 的角度定义为 0°。
    
    参数:
        lines: 直线段对象列表，每个对象要求具备 StartPoint, EndPoint, Handle 属性。
        P: 共点，三元组 (x, y, z)。
        current_line: 当前参考线段，对应角度定义为 0°。
        tol: 判断共点的容差（只比较 x 和 y 坐标）。
        
    返回:
        按相对角度从小到大排序的经过 P 的线段列表（current_line 亦包括其中）。
    """
    shared_lines = []
    P = tuple(P)
    for ln in lines:
        try:
            sp = tuple(ln.StartPoint)
            ep = tuple(ln.EndPoint)
            if (abs(sp[0]-P[0])<=tol and abs(sp[1]-P[1])<=tol) or (abs(ep[0]-P[0])<=tol and abs(ep[1]-P[1])<=tol):
                shared_lines.append(ln)
        except Exception as e:
            sys_logger.info(f"[警告]️ 跳过无效线段 {getattr(ln, 'Handle', '未知')} : {e}")
            continue
    # 根据从当前线段旋转（逆时针）的相对角度排序
    shared_lines.sort(key=lambda ln: calculate_relative_angle(ln, P, current_line, tol))
    return shared_lines

#####################
# 函数：根据当前线段和共点 P，选择下一条后继线段（选择相对角度最大的那条），返回 (后继线段, 新共点)

#&&% 查找最大转角后继线
def find_successor_line_max(current_line, lines, P, tol=0.5):
    """
    在给定共点 P 处，排除当前线段（current_line）后，
    选择在该点处与当前线段相对旋转角度最大的那条线段作为后继线段，
    返回 (后继线段, 新共点)。

    参数：
      current_line: 当前线段对象。
      lines: 所有直线段对象列表，每个对象必须具备 StartPoint, EndPoint, Handle 属性。
      P: 共点（三元组）。
      tol: 共点判断的容差（默认 0.5）。

    返回：
      (后继线段, 新共点)，若找不到合适的后继线段，则返回 (None, P)。
    """
    # 调用 find_lines_sharing_point 获取所有经过 P 的线段，并使用 current_line 的相对角度排序
    candidates = find_lines_sharing_point(lines, P, current_line, tol)
    # 排除当前线段
    candidates = [ln for ln in candidates if ln.Handle != current_line.Handle]

    if not candidates:
        sys_logger.info(f"[错误] 在点 {P} 处找不到除当前线外的候选后继线段")
        return None, P

    best_line = None
    max_angle = -1
    new_point = P
    for ln in candidates:
        relative_angle = calculate_relative_angle(ln, P, current_line, tol)
        if relative_angle > max_angle:
            max_angle = relative_angle
            if same_point(tuple(ln.StartPoint), P, tol):
                new_point = tuple(ln.EndPoint)
            else:
                new_point = tuple(ln.StartPoint)
            best_line = ln

    if best_line is None:
        sys_logger.info(f"[错误] 没有找到有效的后继线段")
        return None, P

    sys_logger.info(f"选中后继线段 {best_line.Handle}，新共点 {new_point}")
    return best_line, new_point

#&&%#####################
# 辅助函数：从所有线段中找出最右下角的点
#&&% 查找右下角点
def find_rightbottom_point(lines, tol=0.5):
    """
    从所有线段端点中，找出 y 值最小的点；若有多个，则选 x 最大的点作为最右下角点。
    """
    all_points = []
    for line in lines:
        if hasattr(line, "StartPoint") and hasattr(line, "EndPoint"):
            all_points.append(tuple(line.StartPoint))
            all_points.append(tuple(line.EndPoint))
    if not all_points:
        return None
    min_y = min(p[1] for p in all_points)
    candidates = [p for p in all_points if abs(p[1]-min_y) <= tol]
    rb = max(candidates, key=lambda p: p[0])
    sys_logger.info(f"[OK] 最右下角点为：{rb}")
    return rb



#  主函数
#  (1)
# 寻找直线段组中最右下角封闭多边性

#  该函数系列包括如下一些函数


"""
辅助函数

same_point(p1, p2, tol) 判断两点是否在容差范围内相同

calculate_absolute_angle(line, P, tol) 计算从点 P 出发到某条线段（取与 P 不相同的端点）的绝对角度

calculate_relative_angle(line, P, current_line, tol) 计算当前线（以 P 为起点，选取与 P 不相同的端点）

和候选线（以 P 为起点）的角度差（逆时针方向，结果在 0～360 之间）

函数 find_lines_angle
用于初始阶段：给定一个共点 P，找到所有经过该点的线段，并按它们的绝对角度排序（从小到大）。

函数 find_lines_sharing_point
给定共点 P 与一个“当前线段”（作为参考），返回所有经过 P 的线段，并按照从当前线段出发旋转（逆时针）的相对角度排序。

函数 find_successor_line_max
根据当前线段和共点 P，从通过 P 的候选线中选取“转角”最大的作为后继线段，并返回后继线段及该线段另一端的新共点。

函数 find_rightbottom_closed_polygon
利用上述函数构造封闭多边形。初始时先根据所有线段端点确定“最右下角”点（函数 find_rightbottom_point），然后在该点处调用

find_lines_angle 得到所有经过该点的线段，选取绝对角度最小的那一根作为第一条边（初始 current_line），再依次调用

find_successor_line_max 推进多边形直到闭合或达到最大步数。


"""

#&&% 查找右下角闭合多边形
def find_rightbottom_closed_polygon(lines, tol=0.5, max_steps=50):
    """
    利用所有线段构造封闭多边形：
      1. 先查找所有线段端点中的最右下角点（RB）。
      2. 在 RB 处获取所有经过该点的线段（按照绝对角度排序），选择绝对角度最小的那根作为初始边。
      3. 以该初始边为第一条边，之后依次利用 find_successor_line_max 选择后继边，
         直到新共点回到初始点（闭合）或超过最大步数。
         
    返回：
      构成封闭多边形的点列表（依次为每条边的终点），若无法构成则返回 None。
    """
    # 定位最右下角点 RB
    rb = find_rightbottom_point(lines, tol)
    if rb is None:
        print("[错误] 无右下角点")
        return None

    # 初始共点
    current_point = rb
    # 从 RB 处按绝对角度排序取候选线段
    candidates = find_lines_angle(lines, rb, tol)
    if not candidates:
        sys_logger.info(f"[错误] 在右下角点 {rb} 处没有找到经过的线段")
        return None
    # 选择绝对角度最小的线段作为初始边
    current_line = candidates[0]
    sys_logger.info(f"调试：选中初始线段 {current_line.Handle}，绝对角度 = {calculate_absolute_angle(current_line, rb, tol):.2f}°")

    # 得到初始边的另一端
    sp = tuple(current_line.StartPoint)
    ep = tuple(current_line.EndPoint)
    if same_point(sp, rb, tol):
        next_point = ep
    else:
        next_point = sp

    polygon_points = [rb, next_point]
    visited_handles = {current_line.Handle}
    current_point = next_point
    steps = 1

    while steps < max_steps:
        # 调用 find_successor_line_max 得到下一条线段及其另一端的点
        successor, new_point = find_successor_line_max(current_line, lines, current_point, tol)
        if successor is None:
            print("[错误] 无后继线段，构造失败")
            return None
        # 检查是否闭合（新共点与起始点接近）
        if same_point(new_point, rb, tol):
            polygon_points.append(rb)
            sys_logger.info(f"[OK] 成功构建封闭多边形，步数 = {steps}")
            return polygon_points

        if successor.Handle in visited_handles:
            print("🔁 检测到重复线段，构造失败")
            return None

        polygon_points.append(new_point)
        visited_handles.add(successor.Handle)
        current_line = successor
        current_point = new_point
        steps += 1

    print("[警告]️ 达到最大步数，未能构造出闭合多边形")
    return None


# 从com边或顶点坐标列表用PL复线绘制多边形


#&&% 绘制多边形
def draw_polygon_as_polyline(polygon, layer_name="测试辅助", tol=0.5):
    """
    将构造的多边形（polygon）转换为顶点序列，并在当前 AutoCAD 文档 doc 的 ModelSpace 中添加
    一个多段线（PLINE）。如果顶点序列的首尾两点重合，则绘制闭合多段线，否则绘制开放多段线。
    
    参数:
      polygon:
        1. 如果是由线段组成的列表，每个元素要求具备 StartPoint 和 EndPoint 属性，
           则按照这些线段的端点顺序构造顶点序列。
        2. 如果是顶点列表，例如 [(x, y, z), (x, y, z), ...]，则直接使用。
      layer_name: 绘制多段线所在的图层名称（默认为 "测试辅助"）。
      tol: 判断点是否重合的容差值（仅比较 x 和 y 坐标）。
      
    返回:
      成功时返回创建的多段线对象（PLINE），否则返回 None。
    """

    # 内部函数：判断两个点是否近似相等（仅比较 x 和 y 坐标）
##    def same_point(p1, p2, tol=tol):
##        return abs(p1[0] - p2[0]) <= tol and abs(p1[1] - p2[1]) <= tol

    if not polygon:
        print("[错误] 未提供有效的 polygon 数据")
        return None

    vertices = []
    is_closed = False  # 是否绘制闭合多段线

    # 判断 polygon 是顶点列表还是线段列表
    if isinstance(polygon[0], (tuple, list)):
        # 判断传入是否为顶点列表：检查第一个元素为 tuple/list 且长度>=3
        if len(polygon[0]) < 3:
            print("[错误] 顶点数据格式错误")
            return None
        # 直接使用顶点列表（转换为 tuple 形式）
        vertices = [tuple(pt) for pt in polygon]
        # 如果首尾已经重合，则视为闭合；否则保持开放（不自动补充首点）
        if same_point(vertices[0], vertices[-1], tol):
            is_closed = True
        else:
            is_closed = False
    else:
        # 假定 polygon 是线段列表，每个元素具有 StartPoint 和 EndPoint 属性
        first_line = polygon[0]
        start_pt = tuple(first_line.StartPoint)
        last_line = polygon[-1]
        # 判断哪一端与起始点相连，作为初始点
        if same_point(start_pt, tuple(last_line.StartPoint), tol) or same_point(start_pt, tuple(last_line.EndPoint), tol):
            # start_pt 可以作为起点
            pass
        else:
            # 否则选用第一条线段的 EndPoint作为起始点
            start_pt = tuple(first_line.EndPoint)
        vertices.append(start_pt)
        current_pt = start_pt
        # 遍历每条线段构造顶点序列
        for line in polygon:
            sp = tuple(line.StartPoint)
            ep = tuple(line.EndPoint)
            if same_point(current_pt, sp, tol):
                next_pt = ep
            elif same_point(current_pt, ep, tol):
                next_pt = sp
            else:
                sys_logger.info(f"[错误] 线段 {line.Handle} 与当前点 {current_pt} 未连接，构造多边形失败")
                return None
            vertices.append(next_pt)
            current_pt = next_pt
        # 检查是否闭合（首尾重合）
        if same_point(vertices[0], vertices[-1], tol):
            is_closed = True
        else:
            is_closed = False

    # 输出调试信息：打印顶点序列
    print("调试：多段线顶点序列：")
    for i, pt in enumerate(vertices):
        sys_logger.info(f"  顶点 {i}: {pt}")

    # 将顶点序列转换为一维坐标数组：[x1, y1, z1, x2, y2, z2, …]
    coords = []
    for pt in vertices:
        coords.extend([pt[0], pt[1], pt[2]])
    coords_tuple = tuple(coords)
    coords_variant = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, coords_tuple)

    # 确保图层存在，否则创建新图层
    try:
        _ = doc.Layers.Item(layer_name)
    except Exception:
        doc.Layers.Add(layer_name)

    # 在 ModelSpace 中添加多段线并设置相应属性
    try:
        ms = doc.ModelSpace
        polyline = ms.AddPolyline(coords_variant)
        polyline.Closed = is_closed
        polyline.Layer = layer_name
        # 可选设置颜色和宽度，按需要调整
        polyline.color = 1
        polyline.ConstantWidth = 20
        polyline.Update()
        doc.Regen(0)
        sys_logger.info(f"[OK] 成功在图层 '{layer_name}' 绘制多段线, Closed={is_closed}")
        return polyline
    except Exception as e:
        print("[错误] 绘制多段线失败：", e)
        return None



#&&%###外轮廓线

# -----------------------------------------------------
# 辅助函数：判断两个点是否近似相等（仅比较 x 和 y 坐标）
#&&% 近似相等
def is_nearly_equal(p1, p2, tol):
    return abs(p1[0] - p2[0]) <= tol and abs(p1[1] - p2[1]) <= tol



# -----------------------------------------------------
# 寻找后继线段：在共点 P 处，从当前边之外的候选边中选择相对角度最小的边
#&&% 查找最小转角后继线
def find_successor_line_min(current_line, lines, P, tol=0.5):
    # 先获取共点 P 的所有线段，使用 find_lines_sharing_point 逻辑，但这里直接采用 find_lines_angle 排序后筛选
    candidates = []
    P = tuple(P)
    for ln in lines:
        try:
            sp = tuple(ln.StartPoint)
            ep = tuple(ln.EndPoint)
            if (abs(sp[0]-P[0]) <= tol and abs(sp[1]-P[1]) <= tol) or (abs(ep[0]-P[0]) <= tol and abs(ep[1]-P[1]) <= tol):
                # 排除当前线段自身
                if ln.Handle == current_line.Handle:
                    continue
                candidates.append(ln)
        except Exception as e:
            continue

    if not candidates:
        sys_logger.info(f"[错误] 在点 {P} 处找不到候选后继线段")
        return None, P

    best_line = None
    min_angle = 360
    new_point = P
    for candidate in candidates:
        angle_diff = calculate_relative_angle(candidate, P, current_line, tol)
        # 选择相对角度最小的候选
        if angle_diff < min_angle:
            min_angle = angle_diff
            best_line = candidate
            # 更新新共点：选择 candidate 中不等于 P 的端点
            sp_cand = tuple(candidate.StartPoint)
            ep_cand = tuple(candidate.EndPoint)
            if is_nearly_equal(sp_cand, P, tol):
                new_point = ep_cand
            else:
                new_point = sp_cand

    if best_line is None:
        sys_logger.info(f"[错误] 没有找到合适的后继线段")
        return None, P

    sys_logger.info(f"选中后继线段 {best_line.Handle}，新共点 {new_point}，相对转角 = {min_angle:.2f}°")
    return best_line, new_point



#  主函数
#  (3)
# 获取一组直线段的外轮廓线

#&&% 获取外轮廓
def get_outer_contour(lines, tol=0.5, max_steps=50):
    """
    获取一组直线段的外轮廓线
    规则：
      1. 计算所有线段端点的最右下角点 P（绝对方法）。
      2. 在 P 处，按绝对角度排序，选择绝对角度最小的边作为第一条边；
      3. 以当前边的另一端点作为新的共点，从当前边出发，选择相对于当前边逆时针转角最小的候选边，
         直到新共点回到初始 P 点（闭合）或达到最大步数为止。
    返回：
      外轮廓线构成的线段列表，如果无法构成封闭轮廓则返回空列表。
    """
    # 内部函数：获取所有线段的最右下角点
    rb = find_rightbottom_point(lines, tol)
    if rb is None:
        print("[错误] 无最右下角点")
        return []

    # 设置初始共点为 rb
    P = rb
    sys_logger.info(f"调试：最右下角点为 {P}")

    # 在 P 处，按照绝对角度排序获取所有共点的线段
    candidate_lines = find_lines_angle(lines, P, tol)
    if not candidate_lines:
        sys_logger.info(f"[错误] 在点 {P} 处未找到共点线段")
        return []

    # 根据题目要求，第一条边选择绝对角度最小的线段（即排序后第 1 根线段）
    initial_line = candidate_lines[0]
    # 确定初始线段的另一端点
    sp_init = tuple(initial_line.StartPoint)
    ep_init = tuple(initial_line.EndPoint)
    if is_nearly_equal(sp_init, P, tol):
        next_point = ep_init
    else:
        next_point = sp_init
    sys_logger.info(f"调试：选中初始线段 {initial_line.Handle}，起点 {P} -> 终点 {next_point}")
    
    contour_lines = [initial_line]
    visited_handles = {initial_line.Handle}
    current_line = initial_line
    current_point = next_point
    steps = 0

    # 迭代构造外轮廓
    while steps < max_steps:
        sys_logger.info(f"调试：目标共点 P = {current_point}")
        # 在当前共点处查找候选的后继线段，使用最小相对角度策略
        successor, new_point = find_successor_line_min(current_line, lines, current_point, tol)
        if successor is None:
            print("[错误] 无后继线段，构造失败")
            return []
        if successor.Handle in visited_handles:
            sys_logger.info(f"🔁 检测到重复线段 {successor.Handle}，构造失败")
            return []
        contour_lines.append(successor)
        visited_handles.add(successor.Handle)
        sys_logger.info(f"步 {steps+1}: 选中线段 {successor.Handle}，新共点 {new_point}")
        # 检查是否闭合：如果新共点与最右下角点近似相等，则认为闭合
        if is_nearly_equal(new_point, rb, tol):
            print("[OK] 成功构造封闭轮廓线")
            return contour_lines
        # 更新当前线段及共点
        current_line = successor
        current_point = new_point
        steps += 1

    print("[警告]️ 达到最大步数，未能构造封闭轮廓线")
    return []


#&&%##获取所有封闭多边形

#删除多边形的一些边

"""
有lines中多于两条直线段经过，就称该点为多分枝点

编制函数，PL是lines中的封闭多边形，用顶点列表表示，p1是lines的最右下角点，

且p1是PL的一个顶点，用坐标点表示。将PL的顶点排序，从p1按逆时针方向推进，

将遇到的非多分枝顶点放入列表LN，直到遇到一个多分枝点D1结束；再从p1按顺时

针方向推进，将遇到的顶点放入列表LN，直到遇到一个多分枝点D2结束。顺时针方

向推进时，把p1考虑在内，即p1如果为多分枝点则立即结束，结束时遇到的多分枝

点D2就是p1。逆时针方向推进时，不把p1考虑在内，即p1为多分枝点仍然推进，遇

到一个多分枝点D1结束。函数返回多分枝点D1，D2，以及它们之间的非多分枝顶点

列表LN。


"""
#&&% 顶点去重
def deduplicate_vertices(vertices, tol=0.5):
    """
    去掉顶点列表中相邻重复的顶点：
    如果两个相邻顶点（顺序出现）之间的二维距离小于 tol，则认为它们重复，只保留前一个，
    但如果这个重复点是列表中的最后一个且与第一个顶点相同（表示闭合多边形），则保留此重复点。
    
    参数:
      vertices: 顶点列表，每个顶点格式为 (x, y, z) 的元组。
      tol: 距离阈值。
      
    返回:
      处理后的顶点列表，只有中间连续重复的点被去除，保留闭合多边形的首尾重复。
    """
    if not vertices:
        return []
    
    deduped = [vertices[0]]
    n = len(vertices)
    
    for i in range(1, n):
        pt = vertices[i]
        prev = deduped[-1]
        dx = pt[0] - prev[0]
        dy = pt[1] - prev[1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        # 如果距离大于等于 tol，则认为是不同的顶点，保留它
        if dist >= tol:
            deduped.append(pt)
        else:
            # 如果当前顶点是最后一个，并且与第一个顶点相同，则保留它（表示闭合）
            if i == n - 1 and same_point(pt, vertices[0], tol):
                deduped.append(pt)
            # 否则跳过该点
    return deduped


#  主函数
#  (4)
# 获取最右下角的封闭多边形不影响其他封闭多边形的连续边的顶点列表 

#&&% 分析多边形分支
def analyze_polygon_branches(PL, lines, p1, tol=0.5):
    """
    分析封闭多边形 PL 的分枝情况。PL 为封闭多边形的顶点列表（按逆时针顺序排列），
    p1 为最右下角点，必在 PL 中。
    
    规则：
      1. 从 p1 出发：
         - 沿逆时针方向（不将 p1 视为候选）推进，累计遇到的非多分枝顶点，直至遇到第一个多分枝点 D1；
         - 沿顺时针方向（将 p1 也考虑在内）推进，累计遇到的非多分枝顶点，直至遇到第一个多分枝点 D2。
      2. 将这两个方向累计得到的非多分枝顶点 LN（其中顺时针方向得到的顶点需要反转后与逆时针方向的顶点相接）打印出来。
      3. 由于 PL 是闭合多边形，从 D1 到 D2有两条连续顶点序列，从中选择包含 LN 的那条作为最终返回结果。

    返回：
      返回从 D1 到 D2（包含 D1 和 D2）的连续顶点序列，此序列包含了 LN 的顶点。
      如果任一方向未能找到多分枝点，则打印提示，并返回 None。
    """


    # 内部辅助：判断两个点是否近似相等（仅比较 x,y 坐标）
##    def same_point(a, b, tol=tol):
##        return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol
##


    # 内部辅助：判断某顶点是否为多分枝点
    def is_multi_branch(vertex):
        cnt = 0
        for ln in lines:
            try:
                sp = tuple(ln.StartPoint)
                ep = tuple(ln.EndPoint)
            except Exception:
                continue
            if same_point(vertex, sp, tol) or same_point(vertex, ep, tol):
                cnt += 1
        return cnt > 2

    # 找出 p1 在 PL 中的索引
    try:
        idx = PL.index(p1)
    except Exception as e:
        print("错误：p1 不在 PL 中")
        return None

    n = len(PL)

    # 沿逆时针方向推进（不包括 p1），累计非多分枝顶点 LN_ccw，直到遇到第一个多分枝点 D1
    LN_ccw = []
    D1 = None
    i = (idx + 1) % n
    while i != idx:
        v = PL[i]
        if is_multi_branch(v):
            D1 = v
            break
        else:
            LN_ccw.append(v)
        i = (i + 1) % n
    if D1 is None:
        print("调试：逆时针方向未遇到多分枝点")
        return None

    # 沿顺时针方向推进（包含 p1），累计非多分枝顶点 LN_cw，直到遇到第一个多分枝点 D2
    LN_cw = []
    if is_multi_branch(PL[idx]):
        D2 = PL[idx]
    else:
        D2 = None
        i = (idx - 1) % n
        while i != idx:
            v = PL[i]
            if is_multi_branch(v):
                D2 = v
                break
            else:
                LN_cw.append(v)
            i = (i - 1) % n
        if D2 is None:
            print("调试：顺时针方向未遇到多分枝点")
            return None

    # 合并顺时针方向的顶点（需要反转）和逆时针方向的顶点
    LN = list(reversed(LN_cw)) + LN_ccw

    # 调试打印
    print("调试信息：")
    print("目标共点 p1 =", p1)
    print("逆时针方向收集的非多分枝顶点 (LN_ccw):")
    for pt in LN_ccw:
        print("  ", pt)
    print("顺时针方向收集的非多分枝顶点 (LN_cw, 原顺序):")
    for pt in LN_cw:
        print("  ", pt)
    print("合并后的非多分枝顶点 LN (从 D2 到 D1):")
    for pt in LN:
        print("  ", pt)
    print("逆时针方向遇到的多分枝点 D1:", D1)
    print("顺时针方向遇到的多分枝点 D2:", D2)

    # 计算在 PL 中 D1 和 D2 的索引
    try:
        idx_D1 = PL.index(D1)
        idx_D2 = PL.index(D2)
    except Exception as e:
        print("错误：无法在 PL 中查找 D1 或 D2:", e)
        return None

    # 由于 PL 是闭合的，我们有两条连接 D1 和 D2：
    if idx_D1 <= idx_D2:
        branch_A = PL[idx_D1: idx_D2 + 1]
        branch_B = PL[idx_D2:] + PL[:idx_D1 + 1]
    else:
        branch_A = PL[idx_D1:] + PL[:idx_D2 + 1]
        branch_B = PL[idx_D2: idx_D1 + 1]

    # 选择包含 LN 中顶点的那个分枝
    selected_branch = None
    if LN:
        found_in_A = any(same_point(v, LN[0], tol) for v in branch_A)
        found_in_B = any(same_point(v, LN[0], tol) for v in branch_B)
        if found_in_A and not found_in_B:
            selected_branch = branch_A
        elif found_in_B and not found_in_A:
            selected_branch = branch_B
        elif found_in_A and found_in_B:
            # 如果两条分枝都包含，则选择较短的那条，通常这才是“局部”的分枝
            selected_branch = branch_A if len(branch_A) <= len(branch_B) else branch_B
        else:
            print("调试：LN 中的顶点不在任一分枝上，默认选择 branch_A")
            selected_branch = branch_A
    else:
        print("调试：LN 为空，无法确定包含 LN 的分枝，默认选择 branch_A")
        selected_branch = branch_A

    print("最终返回的从 D1 到 D2（包含 LN 的分枝）顶点序列：")
    for pt in selected_branch:
        print("  ", pt)


    #去重
    selected_branch=deduplicate_vertices(selected_branch, tol=tol)

    return selected_branch

##根据输入的顶点列表判断，将lines的其顶点在该顶点列表的线段移出列表


#&&% 移除指定顶点线段
def remove_lines_in_LBv(lines, LB_v, tol=0.1):
    """
    从 COM 线段列表 lines 中移除那些其两个顶点都在 LB_v 中的线段。
    
    参数：
      lines: COM 线段对象列表，每个对象要求具有 StartPoint 与 EndPoint 属性，
             其值为形如 (x, y, z) 的可迭代对象。
      LB_v: 顶点列表，每个顶点为 (x, y, z) 的元组。
      tol: 判断两顶点近似相等的容差值（默认 0.1）。
    
    返回：
      返回移除满足条件（即两端点都在 LB_v 中）的线段后剩余的线段列表。
    """

    def same_point(pt1, pt2, tol=tol):
        # 只比较 x, y, z 坐标的差值，判断两点是否近似相等
        return abs(pt1[0] - pt2[0]) <= tol and abs(pt1[1] - pt2[1]) <= tol and abs(pt1[2] - pt2[2]) <= tol

    remaining_lines = []
    for ln in lines:
        try:
            sp = tuple(ln.StartPoint)
            ep = tuple(ln.EndPoint)
        except Exception as e:
            sys_logger.info(f"[警告]️ 跳过无效线段，原因: {e}")
            continue

        # 判断该线段的起点和终点是否均存在于 LB_v 中
        sp_in = any(same_point(sp, lb, tol) for lb in LB_v)
        ep_in = any(same_point(ep, lb, tol) for lb in LB_v)
        if not (sp_in and ep_in):
            remaining_lines.append(ln)
        else:
            sys_logger.info(f"删除线段 {ln.Handle}，其两个端点均在 LB_v 中：sp={sp}, ep={ep}")
    return remaining_lines

#  主函数
#  (5)
#&&% 获取全部封闭多边形，但不完全

#&&% 处理多边形
def process_polygons(lines, tol=0.5, max_steps=50, layer_name="测试辅助"):
    """
    递归提取并绘制直线段集 lines 中所有封闭多边形。
    
    流程：
      1. 从 lines 中提取最右下角封闭多边形（调用 find_rightbottom_closed_polygon）。
      2. 对该多边形：
            - 获取最右下角点 p1（调用 find_rightbottom_point）；
            - 将多边形（polygon）加入列表 LB；
            - 调用 analyze_polygon_branches 分析多边形分枝，得到用来判断移除线段的顶点列表 Lv；
            - 调用 remove_lines_in_LBv，将所有两端点均在 Lv 中的直线段从 lines 中移除；
            - 调用 draw_polygon_as_polyline 绘制该多边形，将生成的多段线 COM 对象加入 LBcom；
            - 然后调用 draw_polygon_as_polyline 绘制顶点列表 Lv（蓝色绘制），将生成的多段线 COM 对象加入 LB_yc；
      3. 重复上述过程直至无法提取出封闭多边形；
    
    返回：
      (LB, LBcom, LB_yc)，其中：
         LB: 封闭多边形顶点列表集合（每个为顶点序列）。
         LBcom: 绘制出的多段线 COM 对象列表。
         LB_yc: 绘制蓝色辅助多段线（用于检查移除的线段顶点）的 COM 对象列表。
    """
    LB = []
    LBcom = []
    LB_yc = []  # 存储蓝色辅助多段线 COM 对象，用于检查移除的顶点
    Ly = []  # 用来记录每次移除的直线段
    iteration = 0

    while True:
        iteration += 1
        sys_logger.info(f"\n【迭代 {iteration}】剩余直线段数量 = {len(lines)}")
        p1 = find_rightbottom_point(lines, tol)
        if p1 is None:
            print("未找到最右下角点，结束迭代")
            break
        sys_logger.info(f"当前最右下角点 p1 = {p1}")
        
        polygon = find_rightbottom_closed_polygon(lines, tol=tol, max_steps=max_steps)
        if polygon is None:
            print("无法提取封闭多边形，结束迭代")
            break
        LB.append(polygon)
        print("提取的封闭多边形顶点：")
        for pt in polygon:
            print("  ", pt)
        
        Lv = analyze_polygon_branches(polygon, lines, p1, tol=tol)
        if Lv is None:
            print("分析多分枝失败，结束本次迭代")
        else:
            print("用于移除线段的顶点列表 Lv：")
            for pt in Lv:
                print("  ", pt)
            # 移除 lines 中两端点均在 Lv 中的直线段（调用 remove_lines_in_LBv）
            new_lines = remove_lines_in_LBv(lines, Lv, tol=0.1)
            removed_count = len(lines) - len(new_lines)
            sys_logger.info(f"本次移除直线段数: {removed_count}")
            # 记录被移除的直线段
            for ln in lines:
                if ln not in new_lines:
                    Ly.append(ln)
            lines = new_lines
        
        # 绘制提取出的封闭多边形
        polyline = draw_polygon_as_polyline(polygon, layer_name=layer_name, tol=tol)
        if polyline:
            LBcom.append(polyline)
        
        # 调用 draw_polygon_as_polyline 绘制 Lv（辅助多段线，注意Lv是顶点列表）
        if Lv is not None and len(Lv) > 0:
            poly_blue = draw_polygon_as_polyline(Lv, layer_name=layer_name, tol=tol)
            if poly_blue:
                LB_yc.append(poly_blue)
        
        if len(lines) < 3:
            print("剩余直线段不足以构成封闭多边形，退出")
            break

    return LB, LBcom, LB_yc



#&&% 提取多边形
def extract_polygon_from_lines(lines, tol=0.5):
    """
    将表示封闭多边形边缘的线段（COM对象列表）转换为顶点列表（按顺序排列），
    消除中间相邻的重复顶点。若能成功构成闭合多边形，则返回顶点列表（闭环不重复），否则返回 None。
    
    参数：
      lines: 直线段对象列表，每个对象要求具有 StartPoint 和 EndPoint 属性
      tol: 判断顶点相等的容差（仅比较 x 和 y 坐标）。
    
    返回：
      顶点列表，如 [p1, p2, ..., pn]，其中 p1 表示多边形的起点（不重复列出闭合顶点）。
    """
    if not lines:
        return None
    
    # 定义同点判断函数
##    def same_point(a, b, tol=tol):
##        return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol
    
    # 拷贝线段列表，方便修改（注意：此处不会复制COM对象，仅复制引用）
    remaining_lines = list(lines)
    
    try:
        start_pt = tuple(remaining_lines[0].StartPoint)
    except Exception as e:
        print("提取第一条线段起点失败：", e)
        return None
    vertices = [start_pt]
    current_pt = start_pt

    # 由于多边形是闭合的，最多尝试 2*len(remaining_lines) 次
    for _ in range(len(remaining_lines) * 2):
        found_edge = False
        for ln in remaining_lines:
            try:
                sp = tuple(ln.StartPoint)
                ep = tuple(ln.EndPoint)
            except Exception:
                continue

            nxt = None
            if same_point(current_pt, sp) and (not same_point(current_pt, ep)):
                nxt = ep
            elif same_point(current_pt, ep) and (not same_point(current_pt, sp)):
                nxt = sp

            if nxt is None:
                continue

            # 一旦找到与当前点相连的边，移除此边
            remaining_lines.remove(ln)
            # 如果得到的 nxt 与起点相同，则说明闭合结束
            if same_point(nxt, start_pt):
                vertices.append(start_pt)
                return deduplicate_vertices(vertices, tol)
            else:
                vertices.append(nxt)
                current_pt = nxt
                found_edge = True
                break
        if not found_edge:
            # 未能找到与当前点相连的边，构成闭合失败
            break
    # 如果循环结束后闭合未完成，则返回 None
    return None



#将多段线列表炸开为线段，返回线段列表



#&&% 炸开多段线
def explode_polylines(LB):
    """
    对多段线列表 LB 中的每一个多段线，调用 .Explode() 方法，
    并将炸开得到的所有线段合并为一个新的线段列表返回。

    参数:
      LB: 多段线 COM 对象列表，每个对象应支持 .Explode() 方法，
          如 pl = polyline_explode_object.Explode() 返回该多段线炸开后的线段集合。
          
    返回:
      一个包含所有炸开后直线段 COM 对象的列表。
    """
    exploded_lines = []
    for pl in LB:
        try:
            # 调用 Explode() 方法，返回一个集合（例如 COM Collection）
            exploded = pl.Explode()
            # 遍历返回的集合，将每根线段添加到列表中
            # 注意：遍历 COM Collection 的方法可能因环境不同而不同，此处假设可以直接迭代
            for ln in exploded:
                exploded_lines.append(ln)
        except Exception as e:
            handle = getattr(pl, 'Handle', '未知')
            sys_logger.info(f"[警告]️ 处理多段线 {handle} 时出错: {e}")
    return exploded_lines


#lines1 中那些不在 lines2 中的线段

#&&% 线段集相减
def subtract_line_sets(lines1, lines2, tol=0.5):
    """
    比较两个线段集合 lines1 和 lines2，返回 lines1 中那些不在 lines2 中的线段。

    参数：
      lines1: 第一组线段（候选集合），每个对象须具有 StartPoint 和 EndPoint 属性。
      lines2: 第二组线段，参照集合。
      tol: 判断点是否相同的容差，默认值为 0.5。
      
    返回：
      lines1 中所有不与 lines2 中任意线段相同的线段构成的列表。
    """
    result = []
    for ln in lines1:
        found = False
        for ln2 in lines2:
            if same_line(ln, ln2, tol):
                found = True
                break
        if not found:
            result.append(ln)
    return result

#  主函数
#  (6)
#&&% 获取全部封闭多边形


#&&% 最终处理
def process_final(lines, tol=0.5, max_steps=50, layer_name="测试辅助"):

    print("len(lines):",len(lines))

    L1, L2, L3 = process_polygons(lines, tol=tol, max_steps=max_steps, layer_name=layer_name)

    sys_logger.info(f"process_polygons 完成：\n  L1 数量 = {len(L1)}\n  L2 数量 = {len(L2)}\n  L3 数量 = {len(L3)}")
    
    print(">>> 对 L3 中的多段线执行 Explode() 操作...")

    exploded_lines=explode_polylines(L3)



    shengyu = subtract_line_sets(lines, exploded_lines, tol=tol)

    for x in shengyu:

        print(x.StartPoint,x.EndPoint)

    L_shengyu=extract_polygon_from_lines(shengyu, tol=tol)
   

    ld = draw_polygon_as_polyline(L_shengyu, layer_name=layer_name, tol=tol)

    L2.append(ld)

    L1.append(L_shengyu)
    for x in exploded_lines:
        x.Delete()

    return L1, L2, L3



#&&&% PL复线处理


"""
研究PL复线处理的问题

(1)多段线的基本操作 get_unique_vertices_from_pl_com

(2)PL打印线 generate_name_and_ratio_from_polyline(polyline,A3dy=0)

(3)将正交六边形多段线分成两个矩形区域 split_hexagon_combined(polygon, tol=0.1, simplify_tol=0.5)

(4)获取多段线的上下左右边界的直线段，返回线段端点列表 get_bbox_edge_segments(pl, tol=0.5)

(5)获取多段线的内部的文字 get_texts_in_polyline(com_pl, tol=0.5)

(6)多段线上的均分插入 distribute_points_on_entity(entity, n, block, scale_factor, ys)

(7)返回 pl1 中与 pl2 “共线且有重叠”的区段列表 common_segments_between_polylines(pl1, pl2, tol=0.5)

(8)找到全部“两根多段线耦合成一个矩形”的多段线 two_plines_making_rectangle(pl1, pl2, tol=0.5)






"""
#  主函数
#  (1)
# 多段线的基本操作

#  该函数系列包括如下一些函数
"""

标准顶点坐标列表,是像[(0, 0, 0), (0, 100, 0), (0, 900, 0)]这样的列表

它表示3个连续顶点2根连续线段，公共点坐标不重复

"""
## 0 轻量多段线和一般传统多段线各有用处，后者才能在三维中使用，更广泛


#&&&% 多段线操作


#&&% 绘制轻量多段线
@alias("画轻量多段线")
def draw_lwpolyline(
    coords3d: list[tuple[float, float, float]],
    layer_name: str = "0",
    width: float = 0.0,
    color: int = 256,
    closed: bool = False
):
    """
    根据一组 (x, y, z) 坐标点绘制轻量级多段线（LWPOLYLINE）。

    :param coords3d: 形如 [(x1, y1, z1), (x2, y2, z2), …] 的点列表，
                     仅使用 x,y 坐标，忽略 z。
    :param layer_name: 目标图层名称，不存在则自动创建。
    :param width:      多段线恒宽 (ConstantWidth)。
    :param color:      颜色索引 (AutoCAD Color Index)，256=BYLAYER。
    :param closed:     是否闭合多段线（首尾相连）。

    :return:           新建的轻量级多段线对象 (COM AddLightWeightPolyline)。

    pts = [
        (0.0, 0.0, 0.0),
        (100.0, 0.0, 0.0),
        (100.0, 50.0, 0.0),
        (0.0, 50.0, 0.0),
    ]
    poly = draw_lwpolyline(
        coords3d=pts,
        layer_name="dy_quyu",
        width=0.0,
        color=1,      # 红色
        closed=True
    )
    poly.Coordinates
    (0.0, 0.0, 100.0, 0.0, 100.0, 50.0, 0.0, 50.0)

    len((0.0, 0.0, 100.0, 0.0, 100.0, 50.0, 0.0, 50.0))
    8

    """
    # 1️⃣ 连接 AutoCAD

    # 2️⃣ 确保图层存在
    layers = doc.Layers
    try:
        lyr = layers.Item(layer_name)
    except Exception:
        lyr = layers.Add(layer_name)
    # Optional: 开启图层
    lyr.LayerOn = True

    # 3️⃣ 准备坐标数组：扁平化 x,y
    raw = []
    for x, y, _ in coords3d:
        raw.extend((x, y))
    # 转 COM VARIANT 数组
    arr = win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8,
        raw
    )

    # 4️⃣ 绘制轻量级多段线

    try:

        pline = mp.AddLightWeightPolyline(arr)
        pline.Layer         = layer_name
        pline.ConstantWidth = width
        pline.color         = color
        pline.Closed        = bool(closed)

        sys_logger.info(f"[OK] 已在图层『{layer_name}』绘制多段线，Closed = {closed}")
        return pline
    except Exception as e:
        print("[错误] 绘制多段线失败:", e) 

   # 5️⃣ 返回新对象

    return pline

#&&% 绘制轻量多段线20260113
@alias("画轻量多段线")
def draw_lwpolyline(
    coords3d: list[tuple[float, float, float]],
    layer_name: str = "0",
    width: float = 0.0,
    color: int = 256,
    closed: bool = False
):
    """
    【通用版】支持在 模型空间 或 任意布局空间 绘制。
    它会自动检测当前激活的是哪个空间，就画在哪里。
    """
    # 1️⃣ 获取文档对象 (假设 C.doc 是全局的，如果不是，建议通过参数传入或者在函数内获取)
    doc = C.doc 
    
    # 2️⃣ 关键修改：动态获取绘制目标 (ModelSpace 或 PaperSpace)
    # doc.ActiveLayout.Block 代表当前激活界面的“容器”
    # 如果你在模型界面，它就是模型空间；如果你在布局界面，它就是当前那张纸
    target_space = doc.ActiveLayout.Block 

    # 3️⃣ 确保图层存在
    layers = doc.Layers
    try:
        lyr = layers.Item(layer_name)
    except Exception:
        lyr = layers.Add(layer_name)
    lyr.LayerOn = True

    # 4️⃣ 准备坐标数组
    raw = []
    for x, y, _ in coords3d:
        raw.extend((x, y))
    
    # 转 COM VARIANT 数组
    arr = win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8,
        raw
    )

    # 5️⃣ 绘制
    try:
        # 使用 target_space 替代原来的 mp
        pline = target_space.AddLightWeightPolyline(arr)
        
        pline.Layer         = layer_name
        pline.ConstantWidth = width
        pline.color         = color
        pline.Closed        = bool(closed)

        # sys_logger.info(f"[OK] 已在图层『{layer_name}』绘制多段线")
        return pline
    except Exception as e:
        sys_logger.info(f"[错误] 绘制多段线失败: {e}") 
        return None



# 1 从com复线获取标准顶点坐标列表

#&&% 获取唯一顶点
def get_unique_vertices_from_pl_com(pl_com):
    """
    提取多段线的顶点列表，不重复连续线段的公共顶点，返回顶点列表。
    
    参数:
        pl_com: AutoCAD 中的 Polyline COM 对象（AcDbPolyline）
        
    返回:
        顶点列表，每两个点构成一条线段，格式：[ (x1, y1, z1), (x2, y2, z2), ... ]
        
    """
    # 获取二维坐标数据
    coords = pl_com.Coordinates
    vertices = []

    # 以每两个坐标为一组，构成线段
    for i in range(0, len(coords) - 1, 2):
        x1, y1 = coords[i], coords[i + 1]
        z1 = 0  # 假设z坐标为0，如果需要，可以通过某种方式获取真实z坐标
        if not vertices:
            vertices.append((x1, y1, z1))
        else:
            # 如果当前点与上一个点不重复，添加到顶点列表
            if (x1, y1, z1) != vertices[-1]:
                vertices.append((x1, y1, z1))
    
    # 添加最后一个点，避免遗漏
    last_x, last_y = coords[-2], coords[-1]
    z_last = 0  # 同样，假设最后的z坐标为0
    if (last_x, last_y, z_last) != vertices[-1]:
        vertices.append((last_x, last_y, z_last))
    
    return vertices

# 2 将com线段转成顶点坐标列表，一根线段一个列表

#&&% 线段转点集
def convert_lines_to_points(segments):
    """
    将com线段列表转换为顶点列表，每条线段的两个端点作为一个独立的列表。

    参数:
      segments: 线段对象列表，每个元素具有 StartPoint 和 EndPoint 属性。

    返回:
      包含多个线段顶点的列表，每个线段是一个包含两个端点坐标的列表。
    """
    points_list = []

    for segment in segments:
        # 提取线段的两个端点
        start_point = tuple(segment.StartPoint)
        end_point = tuple(segment.EndPoint)

        # 将线段的两个端点存入一个列表，添加到结果列表
        points_list.append([start_point, end_point])

    return points_list

# 3 合并顶点列表表示的连续线段，允许多根断开的连续线段

#&&% 合并线段
def merge_segments_new(LB, tol=0.5):
    """
    使用convert_lines_to_points 将线段实体转成顶点列表表达式后就可以使用此命令

    不断合并连接，能连接的都会连接   

    """
    def same(p, q):
        return abs(p[0]-q[0]) <= tol and abs(p[1]-q[1]) <= tol

    # 1) 为端点做哈希 — 用 round() 把 tol 纳入 key，避免浮点字典键难比较
    def key(pt):
        return (round(pt[0]/tol), round(pt[1]/tol))   # 只 hash XY

    buckets = defaultdict(list)   # key(pt)  ->  [(seg_index, dir), ...]
    for idx, seg in enumerate(LB):
        a, b = seg[0], seg[-1]
        buckets[key(a)].append((idx, +1))   #  +1 表示 seg[0] 方向
        buckets[key(b)].append((idx, -1))   #  -1 表示 seg[-1] 方向

    used = [False]*len(LB)
    sequences = []

    while True:
        # 找到尚未使用的第一条线段
        try:
            seed_idx = next(i for i,u in enumerate(used) if not u)
        except StopIteration:
            break                           # 全部用完
        used[seed_idx] = True
        seq = deque(LB[seed_idx])           # 双端队列便于首尾增长

        # 函数: 把可接的线段拼到 deque 的一头
        def grow(at_tail: bool):
            while True:
                end_pt = seq[-1] if at_tail else seq[0]
                bucket = buckets[key(end_pt)]
                # 移除已用完的骨牌
                bucket[:] = [pair for pair in bucket if not used[pair[0]]]
                if not bucket:              # 再也接不上
                    break
                idx, direction = bucket.pop()
                used[idx] = True
                seg = LB[idx]
                # 根据 direction 决定正向还是反向加入
                if direction == +1:         # bucket 点是 seg[0]
                    add = seg[1:]           # 去掉公共点再拼
                else:                       # bucket 点是 seg[-1]
                    add = seg[-2::-1]       # 反向、去掉公共点
                if at_tail:
                    seq.extend(add)
                else:
                    seq.extendleft(add[::-1])   # extendleft 要反转

        # 先往尾巴拼，再往头拼（顺序无所谓，都会做到极限）
        grow(True)
        grow(False)
        sequences.append(list(seq))

    return sequences

# 4 绘制连续PL多段线，断开的PL多段线要分开绘制

#&&% 绘制多段线

@retry_if_busy(max_retries=5, delay=0.2)
def draw_polyline(
    vertices,
    layer_name="tuqian_baobu",
    tol=0.5,
    width=50,
    color=256,
    target_space=None # ✨ 关键参数：指定绘制在哪个空间 (Block容器)
):
    """
    【修正版 V3】绘制轻量多段线 (LWPolyline)
    1. 移除了 li()，使用 C.doc。
    2. 支持 target_space 参数，实现 Model/Layout 自适应绘制。
    """
    
    # 1. 获取文档 (规范化使用 C.doc)
    doc = getattr(C, 'doc', None)
    if doc is None:
        sys_logger.error("[Draw] 失败: C.doc 未初始化")
        return None

    # 2. 确定绘制容器
    # 如果没传 target_space，默认为当前激活的布局/空间
    container = target_space
    if container is None:
        try:
            container = doc.ActiveLayout.Block
        except:
            container = doc.ModelSpace

    # ----------------- 内部工具 -----------------
    def same_point(p1, p2, _tol=tol):
        return abs(p1[0] - p2[0]) <= _tol and abs(p1[1] - p2[1]) <= _tol

    # ---------- 数据准备 ----------
    if not vertices or len(vertices) < 2:
        return None

    # 处理闭合
    is_closed = False
    if len(vertices) > 2 and same_point(vertices[0], vertices[-1]):
        is_closed = True

    # 展平坐标 (LWPolyline 需要 [x1, y1, x2, y2...])
    flat = []
    for pt in vertices:
        if len(pt) >= 2:
            flat.extend([pt[0], pt[1]])
        else:
            return None
            
    try:
        # 创建 COM 数组
        coords_var = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, tuple(flat))
    except Exception as e:
        sys_logger.error(f"[Draw] 坐标转换失败: {e}")
        return None

    # ---------- 绘制 ----------
    pl = None
    try:
        # 🟢 核心修正：在指定容器中创建，而不是 ModelSpace
        pl = container.AddLightWeightPolyline(coords_var)
        
        # --- 属性设置 ---
        # 分开设置以防单项失败导致整体崩溃
        try:
            if layer_name: pl.Layer = layer_name
        except: pass

        try:
            pl.Color = color
            pl.Closed = is_closed
            pl.ConstantWidth = width
        except: pass

        return pl

    except Exception as e:
        sys_logger.error(f"[Draw] AddLightWeightPolyline 失败: {e}")
        return None

# 5 获取多段线后的线段列表，原来的多段线仍然存在


"""
pl=  Pl_obj.Explode()

"""



# 6 将多条直线段（允许不连续）连接成PL复线

#&&% 线段转多段线

def lines_to_polylines(Lc=None,
                        tol=0.5,
                        layer_name="tuqian_baobu",
                        width=50,
                        color=256):
    """
    将直线段合并为多段线 (空间自适应版)
    """
    sys_logger.info(f"\n--- 🔍 开始 lines_to_polylines (Layer: {layer_name}) ---")

    # 0. 规范化连接 (替代 li())
    try:
        C.li() # 刷新连接
        doc = C.doc
    except Exception as e:
        sys_logger.error(f"CAD 连接失败: {e}")
        return []

    # 1. 获取源对象
    raw_objects = []
    if Lc is None:
        sys_logger.info(f"[Step 1] 搜索图层: {layer_name}")
        raw_objects = stc(layer_name)
    else:
        raw_objects = Lc

    if not raw_objects:
        sys_logger.info("[Step 1] 未找到对象")
        return []

    # 2. 筛选直线并确定宿主空间
    valid_lines = []
    target_container = None # 用于存放这些线所在的 Block (Model 或 Layout)

    for obj in raw_objects:
        try:
            if get_attr(obj, "ObjectName") == "AcDbLine":
                valid_lines.append(obj)
                
                # 🔥 核心逻辑：捕获第一条有效直线的“宿主”
                if target_container is None:
                    owner_id = obj.OwnerID
                    # 通过 OwnerID 反向获取容器对象 (Layout Block 或 ModelSpace)
                    try:
                        target_container = doc.ObjectIDToObject(owner_id)
                    except:
                        pass
        except: 
            continue

    if not valid_lines:
        return []

    # 兜底：如果没能通过 OwnerID 找到容器，就用当前激活的
    if target_container is None:
        target_container = doc.ActiveLayout.Block

    sys_logger.info(f"[Step 2] 有效直线: {len(valid_lines)} 条 | 目标容器: {get_attr(target_container, 'Name', 'Unknown')}")

    # 3. 转换点
    LB = convert_lines_to_points(valid_lines)
    if not LB: return []

    # 4. 合并段
    LK = merge_segments_new(LB, tol=tol)
    if not LK: return []

    # 5. 生成多段线
    PLs = []
    for verts in LK:
        if len(verts) < 2: continue
        
        # 🟢 传入探测到的 target_container
        pl = draw_polyline(verts,
                           layer_name=layer_name,
                           tol=tol,
                           width=width,
                           color=color,
                           target_space=target_container) # <--- 传入正确的空间
        if pl:
            PLs.append(pl)

    # 6. 删除原直线
    if PLs:
        deleted_count = 0
        for ln in valid_lines:
            try: 
                safe_delete(ln)
                deleted_count += 1
            except: pass
        sys_logger.info(f"✅ 生成 {len(PLs)} 条多段线，删除 {deleted_count} 条原直线")
            
    return PLs

# 7 找到多段线的最左下角的点

#&&% 查找最小点
def find_min_point(obj):
    """
    获取任意对象的左下角坐标（通过其外包盒）。

    :param obj: 支持 GetBoundingBox() 方法的 COM 对象（如多段线、块参照等）。
    :return:    (min_x, min_y) 元组，表示对象外包盒的左下角坐标
    """
    try:
        ll_point, _ = obj.GetBoundingBox()
        min_x, min_y, _ = ll_point
        return min_x, min_y
    except Exception as e:
        sys_logger.info(f"[错误] 获取外包盒失败: {e}")
        return None, None

# 8 找到多段线的最右上角的点

#&&% 查找最大点
def find_max_point(obj):
    """
    获取任意对象的右上角坐标（通过其外包盒）。

    :param obj: 支持 GetBoundingBox() 方法的 COM 对象（如多段线、块参照等）。
    :return:    (max_x, max_y) 元组，表示对象外包盒的右上角坐标
    """
    try:
        _, ur_point = obj.GetBoundingBox()
        max_x, max_y, _ = ur_point
        return max_x, max_y
    except Exception as e:
        sys_logger.info(f"[错误] 获取外包盒失败: {e}")
        return None, None


#&&% 计算距离
def distance(point1, point2):
    """计算两点之间的距离"""
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5



# 10 定义矩形

#&&% 定义矩形
def define_rectangle_by_diagonal(p1, p2):
    """
    使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。
    p1, p2: 分别为矩形的一对对角顶点，格式为 (x, y)。
    返回矩形的四个顶点、长和宽。
    """
    x1, y1 = p1
    x2, y2 = p2

    # 计算两个边长
    length_x = abs(x2 - x1)
    length_y = abs(y2 - y1)

    # 确定长和宽
    length = max(length_x, length_y)
    width = min(length_x, length_y)

    # 确定矩形的四个顶点
    rectangle_points = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]

    return rectangle_points, length, width

#&&% 定义矩形X
def define_rectangle_by_diagonal_x(p1, p2):
    """
    使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。
    p1, p2: 分别为矩形的一对对角顶点，格式为 (x, y)。
    返回矩形的四个顶点、长和宽。
    """
    x1, y1 = p1
    x2, y2 = p2

    # 计算两个边长
    length_x = abs(x2 - x1)
    length_y = abs(y2 - y1)

    # 确定长和宽
    length = max(length_x, length_y)
    width = min(length_x, length_y)

    # 确定矩形的四个顶点
    rectangle_points = [x1, y1, x2, y1, x2, y2, x1, y2]

    return rectangle_points






def expand_rectangle(p1, p2, offset=130):
    """
    给定矩形框的两个对角点（p1 和 p2），
    返回在四个方向扩展 offset 后的新对角点 P1 和 P2。
    """

    x1, y1, z1 = p1
    x2, y2, z2 = p2

    # 确保 p1 是左下角，p2 是右上角（即使输入反了）
    x_min, x_max = sorted([x1, x2])
    y_min, y_max = sorted([y1, y2])
    z = z1  # z 坐标保持一致

    # 四向扩展 offset，构造新的矩形框
    P1 = (x_min - offset, y_min - offset, z)
    P2 = (x_max + offset, y_max + offset, z)

    return P1, P2





def parse_rectangle_points(*args):
    """
    接收多种坐标格式输入，统一解析为矩形四角点：
    返回：
        (左下, 右上, 左上, 右下)，每个为三元组 (x, y, z)
    
    合法输入形式：
        - (x1, y1, z1), (x2, y2, z2)
        - [(x1, y1, z1), (x2, y2, z2)]
        - (x1, y1, x2, y2)
        - (x1, y1, 0, x2, y2, 0)
    """
    try:
        # 解包列表输入
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]

        # 标准化为两个三维点
        if len(args) == 2 and all(isinstance(pt, (tuple, list)) and len(pt) == 3 for pt in args):
            p1, p2 = args
        elif len(args) == 4:
            x1, y1, x2, y2 = args
            p1, p2 = (x1, y1, 0), (x2, y2, 0)
        elif len(args) == 6:
            x1, y1, z1, x2, y2, z2 = args
            p1, p2 = (x1, y1, z1), (x2, y2, z2)
        else:
            raise ValueError("输入格式不合法")

        # 解析 min/max 点坐标
        x_min = min(p1[0], p2[0])
        x_max = max(p1[0], p2[0])
        y_min = min(p1[1], p2[1])
        y_max = max(p1[1], p2[1])
        z = p1[2] if len(p1) > 2 else 0

        # 四角坐标
        left_bottom = (x_min, y_min, z)
        right_top = (x_max, y_max, z)
        left_top = (x_min, y_max, z)
        right_bottom = (x_max, y_min, z)

        return left_bottom, right_top, left_top, right_bottom

    except Exception as e:
        sys_logger.info(f"[错误] 解析矩形点失败: {e}")
#&&&% 矩形识别
        return None

#&&&% 模型空间选出矩形多段线

def get_rectangular_polylines(min_side=100.0, area_tolerance=0.02):
    """
    【智能筛选】获取所有“矩形”多段线 (兼容轻量线和老式线)。
    
    逻辑：
    1. 合并两种多段线列表 (物理互斥，直接相加)。
    2. 过滤掉尺寸太小的。
    3. 核心：通过 (自身面积 / 包围盒面积) 判断是否为矩形。
       完美排除 L形、三角形、凹多边形。

    Args:
        min_side: 最小边长 (默认100mm)
        area_tolerance: 面积容差 (默认 2%)

    Returns:
        List[COMObject]: 筛选出的矩形多段线列表
    """
    from  CAD_file_operations   import get_obj_loc    
    
    # 1. 获取并合并列表 (既然类型互斥，直接相加即可)
    candidates_1 = []
    try:
        l1 = select_polyline() or []
        if l1: candidates_1.extend(l1)
    except: pass
    
    try:
        l2 = select_polyline_chuantong() or []
        if l2: candidates_1.extend(l2)
    except: pass
    
    sys_logger.info(f"[筛选] 待检查多段线总数: {len(candidates_1)}")
    
    candidates=[ ent for ent in candidates_1 if  get_obj_loc(ent) == 1]



    results = []
    
    for pl in candidates:
        try:
            # --- A. 尺寸检查 (Bounding Box) ---
            # GetBoundingBox 对 LWPolyline 和 Polyline 都通用
            min_pt, max_pt = pl.GetBoundingBox()
            dx = abs(max_pt[0] - min_pt[0])
            dy = abs(max_pt[1] - min_pt[1])
            
            # 过滤掉“一条线”的情况 (宽度极小)
            if dx < 1e-3 or dy < 1e-3:
                continue
                
            # 过滤掉太小的 (如小于100mm)
            if max(dx, dy) < min_side or min(dx, dy) < min_side:
                continue
                
            # --- B. 形状检查 (核心逻辑: 面积法) ---
            # Area 属性对 LWPolyline 和 Polyline 也都通用
            real_area = abs(getattr(pl, "Area", 0))
            box_area = dx * dy
            
            if box_area <= 0: continue

            # 计算 (真实面积 - 包围盒面积) 的差异比例
            diff_ratio = abs(real_area - box_area) / box_area
            
            # 矩形的面积应该几乎填满包围盒
            # 容差 0.02 允许 2% 的绘图误差或圆角
            if diff_ratio <= area_tolerance:
                results.append(pl)

        except Exception:
            # 个别对象无法获取 Area 或 BoundingBox，直接跳过
            continue

    sys_logger.info(f"[筛选] 最终获得矩形数量: {len(results)}")
    return results

#&&%图纸空间矩形多段线


##def get_layout_rectangular_polylines_coords(layout_name, min_side=100.0):
    ##"""
    ##【早期绑定专用】基于 get_attr 的矩形分析 (已集成 sys_logger)
    ##"""
    ##doc = C.doc
    ##results = []
    ##
    ### [普通信息] -> info (可静音)
    ##sys_logger.info(f"🚀 [COM安全模式] 启动布局扫描: {layout_name}")
##
    ##try:
        ##target_layout = doc.Layouts.Item(layout_name)
        ##layout_block = target_layout.Block
    ##except Exception as e:
        ### [致命错误] -> error (永远显示)
        ##sys_logger.error(f"❌ 获取布局失败: {e}")
        ##return []
##
    ##sys_logger.info(f"📊 容器内对象总数: {layout_block.Count}")
    ##
    ### 遍历
    ##for i, obj in enumerate(layout_block):
        ##try:
            ### --- 1. 安全获取类型 ---
            ##obj_name = get_attr(obj, "ObjectName") 
            ##
            ##if not obj_name or "Polyline" not in str(obj_name):
                ##continue
##
            ##hdl = get_attr(obj, "Handle")
            ### [调试详情] -> info (可静音)
            ##sys_logger.info(f"\n🔍 [分析对象] Handle={hdl} | Type={obj_name}")
##
            ### --- 2. 安全获取坐标 ---
            ##coords = get_attr(obj, "Coordinates")
            ##
            ##if not coords:
                ##sys_logger.info("   ❌ 坐标为空 (None)")
                ##continue
                ##
            ##coords = list(coords)
            ##total_len = len(coords)
##
            ### --- 3. 智能判断维度 ---
            ##step = 2
            ##if "AcDb2dPolyline" in obj_name or "AcDb3dPolyline" in obj_name:
                ##step = 3
            ##
            ##num_points = total_len // step
            ##sys_logger.info(f"   📐 数据结构: 坐标总数={total_len}, 推断步长={step}, 顶点数={num_points}")
##
            ### 打印预览
            ##sys_logger.info(f"   💾 原始数据前预览: {coords[:6]}...")
##
            ##if num_points < 4:
                ##sys_logger.info("   ❌ 忽略: 顶点少于4个")
                ##continue
##
            ### --- 4. 提取 X 和 Y ---
            ##xs = coords[0::step]
            ##ys = coords[1::step]
##
            ### --- 5. 尺寸判定 ---
            ##min_x, max_x = min(xs), max(xs)
            ##min_y, max_y = min(ys), max(ys)
            ##
            ##w = max_x - min_x
            ##h = max_y - min_y
            ##
            ##sys_logger.info(f"   📏 计算尺寸: W={w:.2f}, H={h:.2f} (阈值 {min_side})")
            ##
            ##if w < min_side or h < min_side:
                ##sys_logger.info("   ❌ 忽略: 尺寸过小")
                ##continue
##
            ### --- 6. 正交矩形判定 ---
            ##coord_tol = 1.0 
            ##
            ##is_rect = True
            ##
            ### 检查 X 轴
            ##x_bad_count = 0
            ##for x in xs:
                ##if not (abs(x - min_x) <= coord_tol or abs(x - max_x) <= coord_tol):
                    ##x_bad_count += 1
            ##
            ### 检查 Y 轴
            ##y_bad_count = 0
            ##for y in ys:
                ##if not (abs(y - min_y) <= coord_tol or abs(y - max_y) <= coord_tol):
                    ##y_bad_count += 1
            ##
            ##if x_bad_count > 0 or y_bad_count > 0:
                ##sys_logger.info(f"   ❌ 形状不规则: X轴偏离点={x_bad_count}, Y轴偏离点={y_bad_count}")
                ##continue
##
            ### --- 7. 成功 ---
            ##sys_logger.info("   ✅ >> 匹配成功！")
            ##results.append(obj)
##
        ##except Exception as e:
            ### [非致命警告] -> warning (永远显示)
            ### 捕获单个对象处理时的异常，不中断整个循环
            ##sys_logger.warning(f"   ⚠️ [处理异常] Handle={get_attr(obj, 'Handle', '未知')}: {e}")
            ##continue
##
    ##sys_logger.info(f"\n✅ [扫描结束] 最终找到 {len(results)} 个矩形")
    ##return results
##
##

def get_layout_rectangular_polylines_coords(layout_name, min_side=100.0):
    """
    【早期绑定专用】基于 get_attr 的矩形分析 (已集成 sys_logger)
    【V2.0 动态容差版】修复大图框因微小形变被判定为不规则的问题。
    """
    doc = C.doc
    results = []
    
    # [普通信息] -> info
    sys_logger.info(f"🚀 [COM安全模式] 启动布局扫描: {layout_name}")

    try:
        target_layout = doc.Layouts.Item(layout_name)
        layout_block = target_layout.Block
    except Exception as e:
        sys_logger.error(f"❌ 获取布局失败: {e}")
        return []

    sys_logger.info(f"📊 容器内对象总数: {layout_block.Count}")
    
    # 遍历
    for i, obj in enumerate(layout_block):
        try:
            # --- 1. 安全获取类型 ---
            obj_name = get_attr(obj, "ObjectName") 
            
            if not obj_name or "Polyline" not in str(obj_name):
                continue

            hdl = get_attr(obj, "Handle")
            # [调试详情]
            # sys_logger.info(f"\n🔍 [分析对象] Handle={hdl} | Type={obj_name}")

            # --- 2. 安全获取坐标 ---
            coords = get_attr(obj, "Coordinates")
            
            if not coords:
                continue
                
            coords = list(coords)
            total_len = len(coords)

            # --- 3. 智能判断维度 ---
            step = 2
            if "AcDb2dPolyline" in obj_name or "AcDb3dPolyline" in obj_name:
                step = 3
            
            num_points = total_len // step

            if num_points < 4:
                continue

            # --- 4. 提取 X 和 Y ---
            xs = coords[0::step]
            ys = coords[1::step]

            # --- 5. 尺寸判定 ---
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            
            w = max_x - min_x
            h = max_y - min_y
            
            # sys_logger.info(f"   📏 计算尺寸: W={w:.2f}, H={h:.2f} (阈值 {min_side})")
            
            if w < min_side or h < min_side:
                # sys_logger.info("   ❌ 忽略: 尺寸过小")
                continue

            # --- 6. 正交矩形判定 (核心修复) ---
            # 动态计算容差：短边 * 0.0005，限制在 [0.1, 10.0]
            current_min_side = min(w, h)
            coord_tol = current_min_side * 0.0005
            coord_tol = max(0.1, min(coord_tol, 10.0))
            
            # sys_logger.info(f"   📐 动态容差: {coord_tol:.4f} (基准短边: {current_min_side:.1f})")
            
            x_bad_count = 0
            for x in xs:
                if not (abs(x - min_x) <= coord_tol or abs(x - max_x) <= coord_tol):
                    x_bad_count += 1
            
            y_bad_count = 0
            for y in ys:
                if not (abs(y - min_y) <= coord_tol or abs(y - max_y) <= coord_tol):
                    y_bad_count += 1
            
            if x_bad_count > 0 or y_bad_count > 0:
                # sys_logger.info(f"   ❌ 形状不规则: X轴偏离={x_bad_count}, Y轴偏离={y_bad_count} (容差={coord_tol:.3f})")
                continue

            # --- 7. 成功 ---
            # sys_logger.info("   ✅ >> 匹配成功！")
            results.append(obj)

        except Exception as e:
            sys_logger.warning(f"   ⚠️ [处理异常] Handle={get_attr(obj, 'Handle', '未知')}: {e}")
            continue

    sys_logger.info(f"✅ [扫描结束] 最终找到 {len(results)} 个矩形")
    return results
#&&&% 打印分析


#&&&%  分析打印线20260110


def generate_name_and_ratio_from_com(
    comobj,
    A3dy=0,
    Fandy=("ISO_A3_(420.00_x_297.00_MM)", "0:0", "A3", 0),
    tol=10, 
):
    """
    【V5.0 强制兜底版】
    逻辑：
    1. 严格筛选：排除非多段线、非矩形、尺寸过小(<100)的对象 -> return 0
    2. 优先匹配：在 tol 容差范围内寻找标准图框。
    3. 强制兜底：如果找不到标准图框，直接返回“最接近”的那个（将就模式），绝不返回 0。
    """
    import math

    # =========================================================================
    # 第一阶段：严格的合法性校验 (不合格直接踢出)
    # =========================================================================
    
    # 1. 类型检查
    try:
        obj_name = getattr(comobj, "ObjectName", "")
        if "Polyline" not in obj_name:
            return 0
    except: return 0

    # 2. 几何尺寸获取
    try:
        min_pt, max_pt = comobj.GetBoundingBox()
        dx = abs(max_pt[0] - min_pt[0])
        dy = abs(max_pt[1] - min_pt[1])
        
        # 3. 极小尺寸过滤 (短边小于100直接扔)
        if dx < 100 or dy < 100: 
            return 0

        # 4. 矩形形状校验 (防止三角形、L型)
        # 允许 2% 的面积误差
        try:
            real_area = abs(getattr(comobj, "Area", 0))
            box_area = dx * dy
            if box_area > 0 and abs(real_area - box_area) / box_area > 0.02:
                return 0 
        except: pass

        # 统一长宽方向
        length = max(dx, dy)
        width = min(dx, dy)
        orientation_flag = 1 if dy > dx else 0

    except Exception:
        return 0

    # 到这里，说明它肯定是一个合格的矩形多段线。
    # 接下来必须给它返回一个值，不能再 return 0 了。

    # —————————— 强制指定A3模式 ——————————
    if A3dy == 1:
        return (Fandy[0], Fandy[1], Fandy[2], orientation_flag)

    # —————————— 设定动态容差 ——————————
    if length > 1783.5:
        dynamic_tol = 10.0
    else:
        dynamic_tol = 1.0

    # —————————— 数据定义 ——————————
    LB_dayingkuang = [
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
    
    drawing_map_ml = [
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
        ("A3", "1:100"), ("A3", "1:150"), ("A3", "1:50"),  ("A3", "1:25")
    ]

    drawing_map = [
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
        "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)"
    ]

    # =========================================================================
    # 第二阶段：双轨匹配 (优先命中 -> 否则兜底)
    # =========================================================================
    draw_factors = [1.0, 0.5, 0.25, 1.5]
    multipliers = [1.0, 1.1, 1.2]
    
    # 追踪器 1: 完美匹配 (Difference <= dynamic_tol)
    strict_best_index = None
    strict_min_diff = float('inf')

    # 追踪器 2: 兜底匹配 (Global Minimum Difference)
    approx_best_index = None
    approx_min_diff = float('inf')
    
    for i, (std_len, std_wid, scale_val) in enumerate(LB_dayingkuang):
        for df in draw_factors:
            for mult in multipliers:
                
                # --- 计算两种模式的误差 ---
                # A. 模型空间模式
                tgt_len_m = std_len * df * mult
                tgt_wid_m = std_wid * df * mult
                diff_m = abs(length - tgt_len_m) + abs(width - tgt_wid_m)
                
                # B. 布局空间模式
                tgt_len_l = (std_len / scale_val) * df * mult
                tgt_wid_l = (std_wid / scale_val) * df * mult
                diff_l = abs(length - tgt_len_l) + abs(width - tgt_wid_l)
                
                # 取两者中较优的那个误差
                current_diff = min(diff_m, diff_l)
                
                # --- 逻辑 A: 记录全局最小误差 (用于兜底) ---
                if current_diff < approx_min_diff:
                    approx_min_diff = current_diff
                    approx_best_index = i
                
                # --- 逻辑 B: 记录严格匹配 (优先选择) ---
                # 判断标准：长宽误差都在容差内 (这里用总误差简化判断，或者沿用长宽独立判断均可)
                # 为了简化且有效，这里使用总误差 <= 2 * dynamic_tol 近似判断，
                # 或者严格判断: (dL <= tol and dW <= tol)。这里沿用之前的严格逻辑。
                
                # 重新计算单边误差用于严格判定
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

    # =========================================================================
    # 第三阶段：决策输出
    # =========================================================================
    
    # 1. 优先返回严格匹配的结果
    if strict_best_index is not None:
        final_index = strict_best_index
    
    # 2. 如果没有严格匹配，返回兜底结果 (将就模式)
    elif approx_best_index is not None:
        final_index = approx_best_index
        # sys_logger.info(f"⚠️ [将就匹配] 未找到标准框，已匹配最近似标准 (误差 {approx_min_diff:.1f})")
    
    # 3. 理论上不应该发生 (除非列表为空)，防止 crash
    else:
        return 0

    res_name = drawing_map[final_index]
    res_ratio = drawing_map_ml[final_index][1]
    res_code = drawing_map_ml[final_index][0]
    
    return (res_name, res_ratio, res_code, orientation_flag)




#&&% 打印数据分析

def get_cad_app():
    """连接 CAD"""
    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        return acad
    except Exception:
        print("请先打开 AutoCAD。")
        return None

def get_dimensions(ent):
    """获取实体长宽（长边在前）"""
    try:
        min_pt, max_pt = ent.GetBoundingBox()
        width = abs(max_pt[0] - min_pt[0])
        height = abs(max_pt[1] - min_pt[1])
        
        # 保持长边在前，短边在后
        length = max(width, height)
        wid = min(width, height)
        
        # 处理浮点数精度（可选：如果全是整数图框，可以直接取整）
        return length, wid
    except Exception:
        return 0, 0

def sort_coms_by_llcorner(com_list, cha_Y=2000):
    """
    按 BoundingBox 左下角坐标排序：
      · 先按 y 降序（越大越靠前，即自上而下）
      · 同一行(Δy<cha_Y)内按 x 升序（自左向右）
    """
    wrapped = []
    for ent in com_list:
        try:
            p1, _ = ent.GetBoundingBox()      # p1 已是左下
            x_ll, y_ll = p1[0], p1[1]
        except Exception:
            x_ll = y_ll = float('-inf')       # 取不到的一律放最后
        wrapped.append((ent, x_ll, y_ll))     # (实体, x, y)

    # 先按 y 降序
    wrapped.sort(key=lambda t: -t[2])

    i = 0
    while i < len(wrapped): # 注意：这里稍微改了一点点逻辑以确保处理最后一行
        j = i + 1
        # 寻找当前行的结束位置
        while j < len(wrapped) and abs(wrapped[i][2] - wrapped[j][2]) < cha_Y:
            j += 1
        # 行内再按 x 升序
        if j - i > 1:
            wrapped[i:j] = sorted(wrapped[i:j], key=lambda t: t[1])
        i = j

    return [ent for ent, _, _ in wrapped]

def main():
    acad = get_cad_app()
    if not acad: return
    doc = acad.ActiveDocument
    
    # 1. 手动选择
    print(">>> 请切换到 CAD 窗口，选择那 48 个多段线，然后按回车...")
    ss_name = "PythonFixScaleSelect"
    try:
        doc.SelectionSets.Item(ss_name).Delete()
    except Exception:
        pass
        
    ss = doc.SelectionSets.Add(ss_name)
    try:
        ss.SelectOnScreen()
    except Exception:
        print("选择已取消。")
        return
        
    if ss.Count == 0:
        print("未选择任何对象。")
        return

    # 提取对象到列表
    raw_objs = [ss.Item(i) for i in range(ss.Count)]
    
    # 2. 调用你的排序函数
    # 注意：cha_Y=1000 是你之前的容差，如果行间距较大，可以用默认2000
    sorted_objs = sort_coms_by_llcorner(raw_objs, cha_Y=1000)
    
    # 3. 构造数据并分配固定比例
    # 固定比例序列
    fixed_scales = [100, 150, 50, 25]
    
    output_lines = []
    current_line_str = "    "
    
    sys_logger.info(f"正在处理 {len(sorted_objs)} 个对象...")
    
    for idx, obj in enumerate(sorted_objs):
        # 获取尺寸
        l, w = get_dimensions(obj)
        
        # 格式化尺寸数值（去除无效的小数点）
        l_str = f"{l:.2f}".rstrip('0').rstrip('.')
        w_str = f"{w:.2f}".rstrip('0').rstrip('.')
        
        # 分配比例：使用模运算循环取值 (idx % 4)
        # 0->100, 1->150, 2->50, 3->25, 4->100...
        scale_val = fixed_scales[idx % 4]
        
        # 拼接到当前行字符串
        current_line_str += f"({l_str}, {w_str}, {scale_val}), "
        
        # 每4个换行，或者到了最后一个元素换行
        if (idx + 1) % 4 == 0 or (idx + 1) == len(sorted_objs):
            output_lines.append(current_line_str)
            current_line_str = "    " # 重置并缩进

    # 4. 打印结果
    print("\n" + "="*30 + " 结果 " + "="*30)
    print("LB_dayingkuang = [")
    for line in output_lines:
        print(line)
    print("]")
    print("="*66)
    
    ss.Delete()

def generate_relation_list(data_list):
    result_list = []
    
    for i, current in enumerate(data_list):
        best_match = None
        min_metric = float('inf') # 最小评价值
        
        for j, candidate in enumerate(data_list):
            if i == j: continue # 跳过自己
            
            # 计算 X 差值 和 Y 差值
            dx = abs(current[0] - candidate[0])
            dy = abs(current[1] - candidate[1])
            
            # 核心规则：x或y方向的最后选最小的那个
            current_metric = min(dx, dy)
            
            # 寻找最小差异
            if current_metric < min_metric:
                min_metric = current_metric
                best_match = candidate
        
        # 按照要求的形式生成字符串： "旧元素 : 最近的那个"
        formatted_str = f"{current} : {best_match}"
        result_list.append(formatted_str)
        
    return result_list


#&&&% 选择标准打印区域


def check_strict_standard_size(comobj, tol=10):
    """
    【函数编号】: MAP-CHECK-SIZE-004
    【功能】: 严格检查对象外包盒是否符合标准打印框尺寸。
             支持动态容差：虽然输入参数 tol 固定，但内部判定时会根据倍率缩放容差。
             即：当 scale=0.01 时，实际使用的容差是 tol * 0.01 = 0.1。
    
    【参数】:
        tol: 基准容差 (默认10)，对应 scale=1.0 时的允许误差。
    """
    
    # ————————————— 1. 基础数据定义 —————————————
    LB_dayingkuang = [
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

    drawing_map_ml = [
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
        ("A3", "1:100"), ("A3", "1:150"), ("A3", "1:50"),  ("A3", "1:25")
    ]

    drawing_map = [
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
        "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)"
    ]

    # —————————— 2. 获取对象外包盒信息 ——————————
    try:
        PL_min = find_min_point(comobj)
        PL_max = find_max_point(comobj)
        # 依赖外部函数 define_rectangle_by_diagonal
        _, length, width = define_rectangle_by_diagonal(PL_min, PL_max)
        
        dx = abs(PL_max[0] - PL_min[0])
        dy = abs(PL_max[1] - PL_min[1])
        # 1表示竖向，0表示横向
        orientation_flag = 1 if dy > dx else 0
    except Exception as e:
        sys_logger.info(f"获取对象几何信息失败: {e}")
        return 0

    # —————————— 3. 严格匹配逻辑 ——————————
    allowed_scales = [1.0, 1.1, 1.2, 0.01]

    for i, (std_len, std_wid, _) in enumerate(LB_dayingkuang):
        for scale in allowed_scales:
            # 计算目标尺寸
            target_len = std_len * scale
            target_wid = std_wid * scale
            
            # 🔥 核心修正：使用传入的 tol 乘以 scale 得到当前容差
            # tol 是基准容差(针对1.0倍率)。
            # 当 scale=0.01 时，current_tol 变成 0.1 (假设 tol=10)
            current_tol = tol * scale
            
            # 判断是否命中
            if (abs(length - target_len) <= current_tol) and (abs(width - target_wid) <= current_tol):
                
                # --- 命中后的附加视觉处理 ---
                try:
                    if scale == 1.2:
                        comobj.Color = 5  # 蓝色 (×1.2)
                except Exception:
                    pass

                # --- 构造返回值 ---
                scale_str = drawing_map_ml[i][1]
                
                result = (
                    drawing_map[i],          # 纸张规范名
                    scale_str,               # 比例
                    drawing_map_ml[i][0],    # 图号
                    orientation_flag         # 竖向标志
                )
                return result

    # —————————— 4. 未命中 ——————————
    return 0


#&&%新版20260111
@debuggable
def check_strict_standard_size(comobj, tol=10):
    """
    【修正版 V5.0】
    逻辑：
    1. 根据长边判定环境：长边 < 2140.8 (1784*1.2) 则 tol_base=0.1，否则 tol_base=10。
    2. 支持比例：标准(1:100系)、缩小(1:1系) 及其 1.0, 1.1, 1.2 倍率。
    """
    # ————————————— 1. 基础数据定义 (1:100比例下的基准尺寸) —————————————
    # LB_dayingkuang 存储 (长, 宽)
    LB_dayingkuang = [
        (118900, 84100), (178350, 126150), (59450, 42050), (29725, 21025), # A0, A0+1/8, A0+1/4, A1
        (133800, 84100), (200700, 126150), (66900, 42050), (33450, 21025), 
        (148600, 84100), (222900, 126150), (74300, 42050), (37150, 21025), 
        (84100,  59400), (126150, 89100),  (42050, 29700), (21025, 14850), 
        (105100, 59400), (157650, 89100),  (52550, 29700), (26275, 14850), 
        (126100, 59400), (189150, 89100),  (63050, 29700), (31525, 14850), 
        (147100, 59400), (220650, 89100),  (73550, 29700), (36775, 14850), 
        (59400,  42000), (89100,  63000),  (29700, 21000), (14850, 10500), # A2, A2+1/4...
        (74300,  42000), (111450, 63000),  (37150, 21000), (18575, 10500), 
        (89100,  42000), (133650, 63000),  (44550, 21000), (22275, 10500), 
        (104100, 42000), (156150, 63000),  (52050, 21000), (26025, 10500), 
        (42000,  29700), (63000,  44550),  (21000, 14850), (10500, 7425),  # A3...
    ]

    # 对应的显示标签 (对应 1:100, 1:150, 1:50, 1:25)
    # 当检测到 1:1 环境时，标签会映射为 1:1, 1:1.5, 1:0.5, 1:0.25
    specs = [
        ("A0", "1:100"), ("A0", "1:150"), ("A0", "1:50"), ("A0", "1:25"),
        ("A0+1/8", "1:100"), ("A0+1/8", "1:150"), ("A0+1/8", "1:50"), ("A0+1/8", "1:25"),
        ("A0+1/4", "1:100"), ("A0+1/4", "1:150"), ("A0+1/4", "1:50"), ("A0+1/4", "1:25"),
        ("A1", "1:100"), ("A1", "1:150"), ("A1", "1:50"), ("A1", "1:25"),
        ("A1+1/4", "1:100"), ("A1+1/4", "1:150"), ("A1+1/4", "1:50"), ("A1+1/4", "1:25"),
        ("A1+1/2", "1:100"), ("A1+1/2", "1:150"), ("A1+1/2", "1:50"), ("A1+1/2", "1:25"),
        ("A1+3/4", "1:100"), ("A1+3/4", "1:150"), ("A1+3/4", "1:50"), ("A1+3/4", "1:25"),
        ("A2", "1:100"), ("A2", "1:150"), ("A2", "1:50"), ("A2", "1:25"),
        ("A2+1/4", "1:100"), ("A2+1/4", "1:150"), ("A2+1/4", "1:50"), ("A2+1/4", "1:25"),
        ("A2+1/2", "1:100"), ("A2+1/2", "1:150"), ("A2+1/2", "1:50"), ("A2+1/2", "1:25"),
        ("A2+3/4", "1:100"), ("A2+3/4", "1:150"), ("A2+3/4", "1:50"), ("A2+3/4", "1:25"),
        ("A3", "1:100"), ("A3", "1:150"), ("A3", "1:50"), ("A3", "1:25")
    ]

    # —————————— 2. 获取几何信息 ——————————
    try:
        min_p, max_p = comobj.GetBoundingBox()
        dx = abs(max_p[0] - min_p[0])
        dy = abs(max_p[1] - min_p[1])
        obj_L = max(dx, dy)
        obj_W = min(dx, dy)
        orientation = 1 if dy > dx else 0
    except: return 0

    # —————————— 3. 动态环境判定 (长边阈值) ——————————
    # 判定是否属于 1:1 系列环境 (长边 < 1784 * 1.2)
    is_mini_scale = True if obj_L < 2140.8 else False
    
    # 根据环境设定基准容差
    active_tol = 0.1 if is_mini_scale else 10.0
    
    # 设定检测的倍率 (1.0, 1.1, 1.2)
    growth_factors = [1.0, 1.1, 1.2]
    
    # 设定环境缩放系数 (1:100环境对应1.0, 1:1环境对应0.01)
    env_scale = 0.01 if is_mini_scale else 1.0

    # —————————— 4. 匹配循环 ——————————
    for i, (std_L, std_W) in enumerate(LB_dayingkuang):
        for factor in growth_factors:
            # 最终目标尺寸 = 基准尺寸 * 环境缩放 * 扩展倍率
            target_L = std_L * env_scale * factor
            target_W = std_W * env_scale * factor
            
            # 容差也随 factor 稍微波动 (确保 1.2 倍的框也有足够的容差空间)
            current_tol = active_tol * factor

            if abs(obj_L - target_L) <= current_tol and abs(obj_W - target_W) <= current_tol:
                # 命中！处理标签映射
                label_size = specs[i][0]
                raw_scale_label = specs[i][1]
                
                # 如果是 1:1 环境，修正比例标签 (例如 1:100 -> 1:1)
                if is_mini_scale:
                    scale_val = float(raw_scale_label.split(":")[1]) / 100.0
                    final_scale_label = f"1:{scale_val:g}"
                else:
                    final_scale_label = raw_scale_label
                
                # 如果倍率是 1.2，变蓝标记
                if abs(factor - 1.2) < 0.01:
                    try: comobj.Color = 5
                    except: pass
                
                return (
                    f"Paper_{label_size}", # 模拟 paper 规范名
                    final_scale_label,     # 比例 (1:1 或 1:100等)
                    label_size,            # 图号 (A0等)
                    orientation            # 旋转
                )

    return 0


#&&% 多段线排序
def polyline_sort(polyline_list):
    """对com多段线按照特定规则进行排序"""

    # 存储多段线及其最左下角点
    polylines_with_min_points = [(pl, find_min_point(pl)) for pl in polyline_list]

    # 先按照y值降序排序
    polylines_with_min_points.sort(key=lambda item: -item[1][1])

    # 再对y值差距在1000以内的多段线按照x值升序排序
    i = 0
    while i < len(polylines_with_min_points) - 1:
        j = i + 1
        # 查找所有y值差距在1000以内的多段线
        while j < len(polylines_with_min_points) and abs(polylines_with_min_points[i][1][1] - polylines_with_min_points[j][1][1]) < 1000:
            j += 1
        
        # 如果找到了y值相近的多段线，根据x值进行排序
        if j - i > 1:
            polylines_with_min_points[i:j] = sorted(polylines_with_min_points[i:j], key=lambda item: item[1][0])
        
        i = j

    # 只返回多段线对象
    return [item[0] for item in polylines_with_min_points]




#&&&%  *** 3 将PLcom线列表的坐标信息存储


#&&% 多段线转坐标
def plcom_to_coor(plines):
    """
    接受多根轻量级多段线或常规多段线的 COM 对象列表，返回它们的坐标列表及闭合状态。

    :param plines: 可迭代的一组 LWPOLYLINE 或 POLYLINE COM 对象
    :return: 列表，每个元素为 (pts, closed_flag)：
             - pts: 顶点列表 [(x0, y0), (x1, y1), …]
             - closed_flag: 1 表示闭合，0 表示未闭合

    兼容两种情况：
      1. LWPOLYLINE.Coordinates → 偶数长度，例如 [x0,y0, x1,y1, x2,y2, …]
      2. POLYLINE.Coordinates  → 3 的倍数长度，例如 [x0,y0,z0, x1,y1,z1, …]

    如果既不是偶数也不是 3 的倍数，将跳过该条多段线并打印 WARN 提示。
    """
    plines = ensure_list(plines)
    all_info = []

    for pl in plines:
        raw = list(pl.Coordinates)  # 可能是偶数长度 (LWPOLYLINE) 或 3 的倍数长度 (POLYLINE)

        pts = []
        # —— 情况 A：如果长度能被 3 整除，认为是常规 POLYLINE → 每 3 个数一组 (x,y,z)
        if len(raw) % 3 == 0 and len(raw) > 0:
            for i in range(0, len(raw), 3):
                x = raw[i]
                y = raw[i + 1]
                pts.append((x, y))

        # —— 情况 B：否则如果长度能被 2 整除，认为是轻量级 LWPOLYLINE → 每 2 个数一组 (x,y)
        elif len(raw) % 2 == 0 and len(raw) > 0:
            for i in range(0, len(raw), 2):
                x = raw[i]
                y = raw[i + 1]
                pts.append((x, y))

        else:
            # 既不是 2 的倍数也不是 3 的倍数：坐标数据异常，跳过这一条，打印 WARN
            handle = getattr(pl, "Handle", "<unknown>")
            sys_logger.info(f"[WARN] plcom_to_coor：跳过 Handle={handle} 的多段线，"
                  f"Coordinates 长度={len(raw)} 既非 2 的倍数也非 3 的倍数。")
            continue

        # 读取 Closed 属性，True 表示闭合
        closed_flag = 1 if getattr(pl, "Closed", False) else 0

        all_info.append((pts, closed_flag))

    return all_info


# 4 从坐标信息列表返回PLcom线列表

    
#&&% 坐标转多段线
def plcoor_to_com(coord_info, layer_name="测试辅助", width=0, color=256):
    """
    在当前 DWG 中根据坐标和封闭标志绘制多条轻量级多段线。

    :param coord_info: 列表，每个元素为 (pts, closed_flag)，
                       pts 为 [(x0,y0),…] 顶点列表，
                       closed_flag 为 1（闭合）或 0（不闭合）。
    :param layer_name: 目标图层名称（不存在则创建），默认 "测试辅助"
    :param width:      多段线宽度，默认 0
    :param color:      颜色索引，默认 256（BYLAYER）
    :return:           绘制的多段线对象列表
    """
    # 1) 连接 AutoCAD
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc  = acad.ActiveDocument
    ms   = doc.ModelSpace

    # 2) 确保图层存在
    layers = doc.Layers
    try:
        lyr = layers.Item(layer_name)
    except Exception:
        lyr = layers.Add(layer_name)
    lyr.LayerOn = True

    created = []
    for pts, closed_flag in coord_info:
        # 将 pts 展平为 [x0,y0,x1,y1,…]
        raw = []
        for x, y in pts:
            raw.extend((x, y))
        # 转为 COM 数组
        arr = win32com.client.VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_R8,
            raw
        )
        # 添加轻量级多段线
        lw = ms.AddLightWeightPolyline(arr)
        lw.Layer         = layer_name
        lw.ConstantWidth = width
        lw.color         = color
        lw.Closed        = bool(closed_flag)
        created.append(lw)

    # 可选：缩放到可见范围
    acad.ZoomExtents()
    sys_logger.info(f"[OK] 已绘制 {len(created)} 条轻量级多段线到图层 “{layer_name}”")
    return created






# 5 确定多段线打印框是否竖向

#&&% 判断竖向框
def panduan_shuxiangkuang(polyline):

    PL_min = find_min_point(polyline)
    
    PL_max = find_max_point(polyline)

    cha_x  = abs(PL_max[0] - PL_min[0])   

    cha_y  = abs(PL_max[1] - PL_min[1])

    if  cha_y > cha_x:

        return True

    else :

        return False


# 6 统一为A2的图幅打印

#&&% 统一图幅
def tongyi_tufu(LB,TFname):


    """
    将打印线列表的每根线对应的图纸尺寸统一为一个TFname
        
    """

    LB_xin = []

    for ob in LB:

        LB_xin.append(TFname)#"ISO_A2_(594.00_x_420.00_MM)","ISO_A3_(420.00_x_297.00_MM)"

    return LB_xin



#  主函数
#  (3)
#  将正交六边形多段线分成两个矩形区域

#  该函数系列包括如下一些函数

"""
该函数将正交六边形多段线分成两个矩形区域，只针对标准六点六边的PL多边形
在处理六点六边的正交PL形多边形之前，使用simplify_polygon(polygon, tol=0.5)将伪边点清除
            
"""

# 消除多边形的伪边点

#&&% 简化多边形
def simplify_polygon(poly, tol=0.5):
    """
    简化多边形顶点列表：如果某顶点 P 与其前后两点共线（在容差 tol 范围内），则将其移除。
    首尾相连处理：第一个点的“前点”是最后一个点，最后一个点的“次点”是第一个点。
    
    参数:
        poly: [(x, y, z), …]  原始顶点列表（可能首尾重复或有多余顶点）
        tol:  共线判断的容差（对应叉积绝对值）
    
    返回:
        简化后的顶点列表（同样保留首尾是否闭合的形式，不会自动去重首尾）
    """
    # 先做一次“去掉首尾重复”以免无限循环
    if len(poly) > 1 and poly[0] == poly[-1]:
        poly = poly[:-1]

    def is_colinear(p_prev, p, p_next):
        # 只比较 x,y，计算 (p - p_prev) × (p_next - p) 的“叉积”
        x1, y1 = p[0] - p_prev[0], p[1] - p_prev[1]
        x2, y2 = p_next[0] - p[0],   p_next[1] - p[1]
        cross = x1 * y2 - y1 * x2
        return abs(cross) <= tol

    # 重复扫一遍能删就删，直到一轮下来没有删除
    changed = True
    while changed and len(poly) >= 3:
        changed = False
        n = len(poly)
        for i in range(n):
            prev_idx = (i - 1) % n
            next_idx = (i + 1) % n
            if is_colinear(poly[prev_idx], poly[i], poly[next_idx]):
                # 删除第 i 个点，重置一轮扫描
                del poly[i]
                changed = True
                break
    return poly



# 1. 标准化多边形顶点列表，去掉相邻和首尾重复点
#&&% 标准化多边形
def normalize_polygon(polygon):
    """
    标准化多边形顶点列表：  
      - 去掉任意相邻重复的点  
      - 如果首尾相同，则去掉末尾那个  
      
    参数:
        polygon: 原始顶点列表，每个点为 (x, y, z)
    返回:
        去重后的顶点列表
    """
    if not polygon:
        return []
    normalized = [polygon[0]]
    for pt in polygon[1:]:
        if pt != normalized[-1]:
            normalized.append(pt)
    # 首尾相同则删尾
    if len(normalized) > 1 and normalized[0] == normalized[-1]:
        normalized.pop()
    return normalized


# 2. 找到某顶点的前驱/后继（按循环多边形）
#&&% 获取相邻点
def get_adjacent_points(polygon, p):
    """
    在多边形 polygon 中返回顶点 p 的前后相邻点（支持循环）。
    会先调用 normalize_polygon 清理重复点。
    """
    poly = normalize_polygon(polygon)
    if not poly:
        raise ValueError("多边形为空")
    try:
        idx = poly.index(p)
    except ValueError:
        raise ValueError(f"点 {p} 不在多边形顶点列表中")
    prev_pt = poly[idx - 1] if idx > 0 else poly[-1]
    next_pt = poly[idx + 1] if idx < len(poly) - 1 else poly[0]
    return prev_pt, next_pt


# 3. 点是否在多边形内部（射线法，仅在 XY 平面判断）
#&&% 点在多边形内
def point_in_polygon(pt, polygon):
    """
    判断三维点 pt=(x,y,z) 在多边形 polygon 的 XY 投影内否。
    polygon 中点格式为 (x,y,z)，首尾可重复或不重复均可。
    """
    x, y, _ = pt
    poly2d = [(q[0], q[1]) for q in normalize_polygon(polygon)]
    inside = False
    n = len(poly2d)
    for i in range(n):
        x1, y1 = poly2d[i]
        x2, y2 = poly2d[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xint = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xint > x:
                inside = not inside
    return inside


# 4. 无穷直线 vs 线段在 XY 平面相交
#&&% 线段相交
def line_segment_intersection_2d(p, d, a, b, tol=1e-8):
    """
    计算射线 L(t)=p + t·d 与线段 AB 在 XY 平面上的交点。
    p,d,a,b 皆为 (x,y,z)，但只取 x,y 分量参与计算。
    返回 (xi, yi, t) 或 None。
    """
    px, py, _ = p
    dx, dy, _ = d
    ax, ay, _ = a
    bx, by, _ = b
    ux, uy = bx - ax, by - ay

    det = dx * (-uy) - dy * (-ux)
    if abs(det) < tol:
        return None

    rhsx, rhsy = ax - px, ay - py
    t_param = (rhsx * (-uy) - rhsy * (-ux)) / det
    u_param = (dx * rhsy - dy * rhsx) / det

    if -tol <= u_param <= 1 + tol:
        xi = px + t_param * dx
        yi = py + t_param * dy
        return xi, yi, t_param
    return None


# 5. 计算 p 和其相邻点中点 c，如果 c 内部则返回 c，否则沿 p->c 的射线找到第一个交点
#&&% 获取辅助点
def get_auxiliary_point(p, p_prev, p_next, polygon, tol=1e-8):
    """
    对于多边形顶点 p 及其前后相邻点 p_prev, p_next，
    返回一个位于多边形内部的辅助点 q：
      1. 先取 c = (p_prev + p_next)/2；若 c 在内部，则返回 c
      2. 否则沿射线 p->c 与多边形其它边求最靠近 p 的交点
    返回点格式为 (x,y,z)。
    """
    # 1) 中点 c
    cx = (p_prev[0] + p_next[0]) / 2
    cy = (p_prev[1] + p_next[1]) / 2
    cz = (p_prev[2] + p_next[2]) / 2
    c = (cx, cy, cz)

    if point_in_polygon(c, polygon):
        return c

    # 2) 构造方向 d = c - p 并归一化
    dx, dy = cx - p[0], cy - p[1]
    mag = math.hypot(dx, dy)
    if mag < tol:
        raise RuntimeError("辅助点方向向量过小")
    d = (dx / mag, dy / mag, 0.0)

    # 在每条不含 p 的边上求交
    poly = normalize_polygon(polygon)
    intersects = []
    for i in range(len(poly)):
        a = poly[i]
        b = poly[(i + 1) % len(poly)]
        if a == p or b == p:
            continue
        res = line_segment_intersection_2d(p, d, a, b, tol)
        if res:
            xi, yi, t_param = res
            if abs(t_param) > tol:
                # 插值出对应的 z
                zi = p[2] + t_param * d[2]
                intersects.append((xi, yi, zi, t_param))

    if not intersects:
        raise RuntimeError("未找到有效交点")
    # 取最小 |t| 的那一个
    intersects.sort(key=lambda it: abs(it[3]))
    xi, yi, zi, _ = intersects[0]
    return (xi, yi, zi)


# 6. 计算 p 点的“凹凸度量角”
#&&% 凹凸度量
def concavity_measure(p, p_prev, p_next, q):
    """
    给定 p, p_prev, p_next, q（均为 (x,y,z)），
    计算度量角：
      angle = 360 - larger_angle + smaller_angle  
    其中 smaller/larger 是 pq→p_prev 与 pq→p_next 的逆时针夹角。
    凸点约 ~90°，凹点约 ~270°。
    """
    def angle_of(vx, vy):
        a = math.degrees(math.atan2(vy, vx))
        return a if a >= 0 else a + 360

    # 构造 2D 向量
    vq = (q[0] - p[0], q[1] - p[1])
    v1 = (p_prev[0] - p[0], p_prev[1] - p[1])
    v2 = (p_next[0] - p[0], p_next[1] - p[1])

    a_q = angle_of(*vq)
    a1  = angle_of(*v1)
    a2  = angle_of(*v2)

    d1 = (a1 - a_q) % 360
    d2 = (a2 - a_q) % 360

    small, large = (d1, d2) if d1 < d2 else (d2, d1)
    return 360 - large + small


# 7. 直接给出 p 在多边形上的度量角
#&&% 凹凸角
def concavity_angle(p, polygon):
    """
    直接计算多边形 polygon 上顶点 p 的凹凸度量角。
    """
    p_prev, p_next = get_adjacent_points(polygon, p)
    q = get_auxiliary_point(p, p_prev, p_next, polygon)
    return concavity_measure(p, p_prev, p_next, q)





# 8.合理分割PL正交六边形

#&&% 水平分割六边形
def split_orthogonal_hexagon(polygon, tol=0.1):#水平分割
    """
    将正交六边形 polygon 按凹顶点所在水平线切成两个矩形。
    polygon: 6 个 (x,y,z) 顶点的列表，允许首尾重合或相邻重复，会自动规范化。
    """
    # 1. 规范化，去掉相邻重复和首尾同点
    poly = normalize_polygon(polygon)
    if len(poly) != 6:
        raise ValueError("必须传入6点正交多边形")
    # 2. 找出唯一的凹点 p
    concaves = [pt for pt in poly
                if abs(concavity_angle(pt, poly) - 270) < tol]
    if len(concaves) != 1:
        raise RuntimeError(f"没能唯一定位凹点，找到 {len(concaves)} 个")
    p = concaves[0]
    y0 = p[1]

    # 3. 只对真正“跨越” y=y0 的边求交
    intersections = []
    n = len(poly)
    for i in range(n):
        a = poly[i]
        b = poly[(i+1) % n]
        y1, y2 = a[1], b[1]
        # 仅当严格跨越才算：一端在上 (y>y0)，一端在下 (y<y0)
        if (y1 - y0) * (y2 - y0) < -tol**2:
            t = (y0 - y1) / (y2 - y1)
            xi = a[0] + t * (b[0] - a[0])
            zi = a[2] + t * (b[2] - a[2])
            intersections.append((xi, y0, zi, i))

    # 4. 应该只剩一个真的 crossing 交点
    if len(intersections) != 1:
        raise RuntimeError(f"没能唯一定位 q，找到 {len(intersections)} 个候选点")
    xi, yi, zi, edge_idx = intersections[0]
    q = (xi, yi, zi)

    # 5. 把 q 插回那条边之后
    newpoly = []
    for i in range(n):
        newpoly.append(poly[i])
        if i == edge_idx:
            newpoly.append(q)
    # now len(newpoly)==7

    # 6. 找 p, q 的索引
    i_p = newpoly.index(p)
    i_q = newpoly.index(q)

    # 7. 分割成两段多边形
    if i_q < i_p:
        rect1 = newpoly[i_q:i_p+1]
        rect2 = newpoly[i_p:] + newpoly[:i_q+1]
    else:
        rect1 = newpoly[i_p:i_q+1]
        rect2 = newpoly[i_q:] + newpoly[:i_p+1]

    # 8. 计算2D面积
    def area2d(pts):
        s = 0
        m = len(pts)
        for j in range(m):
            x1,y1,_ = pts[j]
            x2,y2,_ = pts[(j+1)%m]
            s += x1*y2 - x2*y1
        return abs(s)/2

    A1, A2 = area2d(rect1), area2d(rect2)
    # 面积小的放前面
    return (rect1, rect2) if A1 <= A2 else (rect2, rect1)


#&&% 竖向分割六边形
def split_orthogonal_hexagon_vertical(polygon, tol=0.1):#竖向分割
    """
    将正交六边形 polygon 按凹顶点所在竖线切成两个矩形。
    polygon: 6 个 (x,y,z) 顶点的列表，允许首尾重合或相邻重复，会自动规范化。
    tol: 用于识别凹点和跨越判断的容差。
    返回: (rect1, rect2)，面积小的放前面。
    """
    # 规范化：去掉相邻重复和首尾同点
    poly = normalize_polygon(polygon)
    if len(poly) != 6:
        raise ValueError("必须传入6点正交多边形")

    # 找唯一凹点
    concaves = [pt for pt in poly
                if abs(concavity_angle(pt, poly) - 270) < tol]
    if len(concaves) != 1:
        raise RuntimeError(f"没能唯一定位凹点，找到 {len(concaves)} 个")
    p = concaves[0]
    x0 = p[0]

    # 求竖线 x=x0 与真正跨越边的交点
    intersections = []
    n = len(poly)
    for i in range(n):
        a = poly[i]
        b = poly[(i+1)%n]
        x1, x2 = a[0], b[0]
        # 仅对严格跨越的边求交
        if (x1 - x0)*(x2 - x0) < -tol**2:
            # 插值比例
            t = (x0 - x1)/(x2 - x1)
            yi = a[1] + t*(b[1] - a[1])
            zi = a[2] + t*(b[2] - a[2])
            intersections.append((x0, yi, zi, i))

    if len(intersections) != 1:
        raise RuntimeError(f"没能唯一定位 q，找到 {len(intersections)} 个候选点")
    xi, yi, zi, edge_idx = intersections[0]
    q = (xi, yi, zi)

    # 把 q 插回那条边
    newpoly = []
    for i in range(n):
        newpoly.append(poly[i])
        if i == edge_idx:
            newpoly.append(q)
    # newpoly 长度应为7

    # 定位 p、q 索引
    i_p = newpoly.index(p)
    i_q = newpoly.index(q)

    # 分割两段
    if i_q < i_p:
        rect1 = newpoly[i_q:i_p+1]
        rect2 = newpoly[i_p:] + newpoly[:i_q+1]
    else:
        rect1 = newpoly[i_p:i_q+1]
        rect2 = newpoly[i_q:] + newpoly[:i_p+1]

    # 面积计算（2D）
    def area2d(pts):
        s = 0
        m = len(pts)
        for j in range(m):
            x1,y1,_ = pts[j]
            x2,y2,_ = pts[(j+1)%m]
            s += x1*y2 - x2*y1
        return abs(s)*0.5

    A1, A2 = area2d(rect1), area2d(rect2)
    return (rect1, rect2) if A1 <= A2 else (rect2, rect1)


# 合理分割PL正交六边形

#&&% 计算面积
def area_of(verts):
    """多边形面积计算（顶点首尾闭合或不闭合均可）"""
    s = 0
    n = len(verts)
    for i in range(n):
        x1, y1, *_ = verts[i]
        x2, y2, *_ = verts[(i+1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) * 0.5



#&&% 综合分割六边形
def split_hexagon_combined(polygon, tol=0.1, simplify_tol=0.5):# 合理分割PL正交六边形
    """
    合理分割一个正交（近似）六边形 PL：
      1) 如果传入的是 COM PL 对象，则先提取唯一顶点列表；
      2) 对顶点列表做简化（去除伪顶点/伪边）；
      3) 先做横向分割，再做竖向分割，比较两种分割最小矩形面积，
         将最小的那对矩形排在前面，返回四个矩形顶点列表：
         [min1, partner1, min2, partner2]
    参数:
      polygon: 要分割的多段线，既可以是 [(x,y,z),...] 顶点列表，也可以是 COM PL 对象
      tol: 分割时判断凹角的容差
      simplify_tol: 简化多边形时去除“伪顶点/伪边”的容差
    返回:
      四个矩形的顶点列表：最小矩形、其同组矩形、次小矩形、其同组矩形
    """
    # —— 1. 如果是 COM PL 对象，先提取顶点列表 —— 
    # （假定已有 get_unique_vertices_from_pl_com(com_pl) -> [(x,y,z),...]）
    if not isinstance(polygon, list):
        polygon = get_unique_vertices_from_pl_com(polygon)

    # —— 2. 简化顶点列表 —— 
    # （假定已有 simplify_polygon(verts, tol) -> 清理后的顶点列表）
    polygon = simplify_polygon(polygon, simplify_tol)

    # —— 3. 横向与竖向分割 —— 
    rects_h = split_orthogonal_hexagon(polygon, tol)
    rects_v = split_orthogonal_hexagon_vertical(polygon, tol)

    A_h1, A_h2 = rects_h
    A_v1, A_v2 = rects_v

    # 计算每对的“更小”矩形和“配对”矩形
    if area_of(A_h1) <= area_of(A_h2):
        min_h, partner_h = A_h1, A_h2
    else:
        min_h, partner_h = A_h2, A_h1

    if area_of(A_v1) <= area_of(A_v2):
        min_v, partner_v = A_v1, A_v2
    else:
        min_v, partner_v = A_v2, A_v1

    # —— 4. 根据最小面积值决定输出顺序 —— 
    if area_of(min_h) <= area_of(min_v):
        return [min_h, partner_h, min_v, partner_v]
    else:
        return [min_v, partner_v, min_h, partner_h]



#  主函数
#  (4)
#  获取多段线的上下左右边界的直线段，返回线段端点列表

#  该函数系列包括如下一些函数

#&&% 获取包围盒边
def get_bbox_edge_segments(pl, tol=0.5):
    """
    获取对象 pl 的包围盒四条边，分别作为独立的列表返回：
      top    = [(xmin, ymax, z), (xmax, ymax, z)]
      bottom = [(xmin, ymin, z), (xmax, ymin, z)]
      left   = [(xmin, ymin, z), (xmin, ymax, z)]
      right  = [(xmax, ymin, z), (xmax, ymax, z)]
    并打印调试信息。
    """
    # ----- 1. 调用 GetBoundingBox -----
    try:
        min_pt, max_pt = pl.GetBoundingBox()
    except Exception:
        mins = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (0.0, 0.0, 0.0))
        maxs = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (0.0, 0.0, 0.0))
        pl.GetBoundingBox(mins, maxs)
        min_pt = tuple(mins.value)
        max_pt = tuple(maxs.value)

    xmin, ymin, zmin = min_pt
    xmax, ymax, _    = max_pt

    sys_logger.info(f"▶ BoundingBox Min 点: {min_pt}")
    sys_logger.info(f"▶ BoundingBox Max 点: {max_pt}")

    # ----- 2. 构造四个顶点（顺时针） -----
    p1 = (xmin, ymin, zmin)
    p2 = (xmax, ymin, zmin)
    p3 = (xmax, ymax, zmin)
    p4 = (xmin, ymax, zmin)

    print("▶ 矩形四个顶点 (顺时针):")
    for i, pt in enumerate((p1, p2, p3, p4), 1):
        sys_logger.info(f"   {i}: {pt}")

    # ----- 3. 四条边，各自用列表表达 -----
    top    = [p4, p3]    # y = ymax
    bottom = [p1, p2]    # y = ymin
    left   = [p1, p4]    # x = xmin
    right  = [p2, p3]    # x = xmax

    return top, bottom, left, right



#  主函数
#  (5)
#&&%  获取多段线的内部的文字

#  该函数系列包括如下一些函数



#&&% 获取多段线内文字
def get_texts_in_polyline(com_pl, tol=0.5):
    """
    在多段线 com_pl 内部筛选文字，并返回文字对象列表和对应的文字内容列表。

    参数:
      com_pl:  COM 多段线对象
      tol:     点-in-多边形时的容差（目前未用到，可留作将来扩展）

    返回:
      inside:   落在 com_pl 内部的文字 COM 对象列表
      contents: 对应 inside 中每个对象的文字内容列表
    """
    # 1) 多段线转顶点列表（标准化后的三维点）
    poly = get_unique_vertices_from_pl_com(com_pl)

    # 2) 收集所有文字实体（天正＋原生 CAD）
    tzh_text, tzh_mtext, cad_text, cad_mtext = collect_all_texts()
    all_texts = tzh_text + tzh_mtext + cad_text + cad_mtext

    inside = []
    contents = []

    for txt in all_texts:
        # 用左下角点判断是否在多段线内
        min_pt, _ = txt.GetBoundingBox()
        if point_in_polygon(min_pt, poly):
            inside.append(txt)

            # 根据对象类型取出内容
            name = getattr(txt, "ObjectName", "") or getattr(txt, "EntityName", "")
            if name in ("AcDbText", "AcDbMText"):
                # AutoCAD 原生单/多行
                contents.append(txt.TextString)
            elif name == "TDbText":
                # 天正单行
                contents.append(txt.Text)
            elif name == "TDbMText":
                # 天正多行，需要炸开取内容
                contents.append( TDbMText_content(txt))
            else:
                # 其它（万一有），留空或用 repr
                contents.append("")

    sys_logger.info(f"总共找到 {len(inside)} 条落在多段线内部的文字。")
    return inside, contents




# 获取单独一行的天正多行文字内容

#&&% 获取天正多行文字

def TDbMText_content(comobj, separator="\n"):
    """
    【函数】获取天正多行文字内容（副本炸开版，支持换行识别）
    
    参数:
      comobj: 天正文字对象
      separator: 换行符，默认为 "\n"，也可以设为 "\\" 或其他
    
    逻辑:
      1. 复制并炸开对象。
      2. 按 Y(容差0.3)+X 排序。
      3. 遍历碎片，检测 Y 坐标变化插入换行符。
      4. 清理碎片并返回。
    """
    # 确保环境已连接
    li() 
    
    fragments = []
    
    try:
        # 1. 复制副本
        try:
            copy_ent = comobj.Copy()
        except Exception as e:
            sys_logger.info(f"[错误] 复制天正对象失败: {e}")
            return ""

        # 2. 炸开副本
        fragments = explode_single_object_marker(copy_ent)
        
        if not fragments:
            return ""

        # 3. 排序 (Sort)
        # 容差设为 0.3 (可根据图纸精度调整)
        TOLERANCE = 0.3
        
        def get_sort_info(ent):
            """辅助函数：获取排序用的 y_bin 和 x"""
            ins = get_attr(ent, "InsertionPoint")
            if not ins:
                try:
                    min_p, _ = ent.GetBoundingBox()
                    x, y = min_p[0], min_p[1]
                except:
                    return 0, 0
            else:
                x, y, z = ins
            
            # y_bin 用于判定“行”
            y_bin = round(y / TOLERANCE)
            return y_bin, x

        # Python 的 sort key
        def sort_key(ent):
            y_bin, x = get_sort_info(ent)
            # Y 越大(越靠上)排越前 -> 取负
            return (-y_bin, x)

        fragments.sort(key=sort_key)

        # 4. 提取内容并处理换行 (Extract with Line Breaks)
        final_string = ""
        last_y_bin = None
        
        for i, frag in enumerate(fragments):
            # 获取内容
            txt = get_attr(frag, "TextString")
            if not txt:
                continue
                
            # 获取当前行的标识
            current_y_bin, _ = get_sort_info(frag)
            
            # 判断是否换行
            if last_y_bin is not None:
                # 如果当前行 Y (分桶后) 不等于上一行 Y，说明换行了
                if current_y_bin != last_y_bin:
                    final_string += separator
            
            final_string += txt
            
            # 更新 last_y_bin
            last_y_bin = current_y_bin
        
        return final_string

    except Exception as e:
        sys_logger.info(f"[错误] 提取天正文字内容失败: {e}")
        return ""

    finally:
        # 5. 清理碎片
        if fragments:
            for frag in fragments:
                try:
                    frag.Delete()
                except:
                    pass

#  主函数
#  (6)
#  多段线上的均分插入


"""
该函数用于在dwg文件沿着PL线快速均衡放置树木等图块

            
"""
#&&% 实体均分点
def distribute_points_on_entity(entity, n, block, scale_factor, ys):

    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    model_space = doc.ModelSpace
    block_name = block.Name  # 获取块的名称
    
    # 如果实体是直线
    if entity.ObjectName == "AcDbLine":
        start_point = entity.StartPoint
        end_point = entity.EndPoint
        for i in range(n):
            x = start_point[0] + i * (end_point[0] - start_point[0]) / (n - 1)
            y = start_point[1] + i * (end_point[1] - start_point[1]) / (n - 1)
            inserted_block = model_space.InsertBlock(vtpnt(x, y, 0), block_name, scale_factor, scale_factor, scale_factor, 0)
            inserted_block.color = ys  # 设置颜色为红色

    # 如果实体是圆弧
    elif entity.ObjectName == "AcDbArc":
        start_angle = entity.StartAngle
        end_angle = entity.EndAngle
        center = entity.Center
        radius = entity.Radius
        for i in range(n):
            angle = start_angle + i * (end_angle - start_angle) / (n - 1)
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            inserted_block = model_space.InsertBlock(vtpnt(x, y, 0), block_name, scale_factor, scale_factor, scale_factor, 0)
            inserted_block.color = ys  # 设置颜色为红色

    # 如果实体是多段线
    elif entity.ObjectName == "AcDbPolyline":
        coords = entity.Coordinates
        points = [(coords[i], coords[i+1]) for i in range(0, len(coords), 2)]
        total_length = sum(distance(points[i], points[i+1]) for i in range(len(points)-1))
        segment_length = total_length / n
        current_length = 0

        for i in range(n):
            accumulated_length = 0
            for j in range(len(points) - 1):
                segment = distance(points[j], points[j+1])
                if accumulated_length + segment > current_length:
                    ratio = (current_length - accumulated_length) / segment
                    x = points[j][0] + ratio * (points[j+1][0] - points[j][0])
                    y = points[j][1] + ratio * (points[j+1][1] - points[j][1])
                    inserted_block = model_space.InsertBlock(vtpnt(x, y, 0), block_name, scale_factor, scale_factor, scale_factor, 0)
                    inserted_block.color = ys  # 设置颜色为红色
                    break
                accumulated_length += segment
            current_length += segment_length
            




#  主函数
#  (7)
# 返回 pl1 中与 pl2 “共线且有重叠”的区段列表

#  该函数系列包括如下一些函数

# 1 判断一条直线是否完全在另一条直线上

#&&% 判断线段包含
def is_segment_contained(seg_a, seg_b, tol=1e-4):
    """
    判断 seg_a 是否完全位于 seg_b 上（包含端点）。
    
    参数
    ----
    seg_a, seg_b :  ( (x1,y1,z1), (x2,y2,z2) )   或   AcDbLine
        两条待比较的线段。先判断 seg_a 是否被 seg_b 覆盖；
        若想双向判断，调用两次并对调顺序即可。
    tol : float
        距离与投影误差容差，默认 1e‑4 (CAD 单位)。

    返回
    ----
    bool
        True  —— seg_a 整段落在 seg_b 上  
        False —— 否则
    """
    # -------- 把输入统一转成端点元组 ----------
    def get_endpoints(entity):
        if hasattr(entity, "StartPoint"):            # COM 线段
            return (tuple(entity.StartPoint), tuple(entity.EndPoint))
        else:                                        # 纯坐标二元组
            return (tuple(entity[0]), tuple(entity[1]))

    a1, a2 = get_endpoints(seg_a)
    b1, b2 = get_endpoints(seg_b)

    # -------- 基本几何工具 ----------
    def dist(p, q):
        return math.hypot(p[0]-q[0], p[1]-q[1])

    def dot(u, v):
        return u[0]*v[0] + u[1]*v[1]

    def colinear(p, q, r, tol):
        """三点是否近似共线（面积≈0）"""
        return abs( (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0]) ) <= tol

    # -------- 先检测共线性 ----------
    if not (colinear(b1, b2, a1, tol) and colinear(b1, b2, a2, tol)):
        return False          # seg_a 端点不与 seg_b 共线 → 不可能包含

    # -------- 再检测投影是否在 b1‑b2 区间内 ----------
    # 令 b1 为原点，b_dir 为方向向量
    b_dir = (b2[0]-b1[0], b2[1]-b1[1])
    b_len2 = dot(b_dir, b_dir)
    if b_len2 == 0:           # seg_b 长度为 0 → 无法包含他段
        return False

    def proj_param(p):
        # 标准化投影参数 t，若 0<=t<=1 则投影落在 seg_b 上
        return dot( (p[0]-b1[0], p[1]-b1[1]), b_dir ) / b_len2

    t_a1 = proj_param(a1)
    t_a2 = proj_param(a2)

    # 允许介于 0±tol 到 1±tol 之间
    inside_1 = -tol <= t_a1 <= 1+tol
    inside_2 = -tol <= t_a2 <= 1+tol

    return inside_1 and inside_2

#&&% 2 返回 PL线pl1 中与 pl2 “共线且有重叠”的区段列表

#&&% 公共线段
def common_segments_between_polylines(pl1, pl2, tol=0.5):
    """
    返回 pl1 中与 pl2 “共线且有重叠”的区段列表，每个区段用
      [(x1,y1,0.0),(x2,y2,0.0)] 表示。

    参数
    ----
    pl1, pl2 : AutoCAD AcDbPolyline COM 对象 (或伪造对象，只需有 .Coordinates / .Closed)
    tol      : 共线 & 距离容差 (同 CAD 单位)

    返回
    ----
    overlaps : list[ list[(x,y,z),(x,y,z)] ]
    """

    # ────────── 内部小工具 ──────────
    def coords_to_xy_pairs(coords):
        """把 (x1,y1,x2,y2,…) 转成 [(x,y),…]；自动丢弃尾部残值"""
        pairs = []
        for i in range(0, len(coords) - 1, 2):
            pairs.append((coords[i], coords[i + 1]))
        return pairs

    def build_segments(verts, closed=False):
        """由顶点顺序生成线段 [P,Q] 列表"""
        segs = []
        for i in range(len(verts) - 1):
            segs.append([verts[i], verts[i + 1]])
        if closed and len(verts) > 2:
            segs.append([verts[-1], verts[0]])
        return segs

    def dist(p, q):
        return math.hypot(p[0] - q[0], p[1] - q[1])

    def colinear(p, q, r):
        """三点共线判定 |叉积| < tol · max(边长)"""
        return abs((q[0] - p[0]) * (r[1] - p[1]) -
                   (q[1] - p[1]) * (r[0] - p[0])) <= tol * max(dist(p, q), dist(p, r), dist(q, r), 1)

    def project(p, axis):
        """根据 axis==0 用 x，否则 y"""
        return p[axis]

    def segment_overlap(seg_a, seg_b):
        """
        若共线且区间有重叠，返回实际重叠区间端点 (pa, pb)（二维点）。
        否则返回 None
        """
        (p1, p2), (q1, q2) = seg_a, seg_b
        # 共线检测
        if not (colinear(p1, p2, q1) and colinear(p1, p2, q2)):
            return None

        # 选投影轴
        axis = 0 if abs(p2[0] - p1[0]) >= abs(p2[1] - p1[1]) else 1
        a1, a2 = project(p1, axis), project(p2, axis)
        b1, b2 = project(q1, axis), project(q2, axis)
        # 使 a1 <= a2, b1 <= b2
        if a1 > a2:
            p1, p2 = p2, p1
            a1, a2 = a2, a1
        if b1 > b2:
            q1, q2 = q2, q1
            b1, b2 = b2, b1

        # 计算 1‑D 重叠区间
        left, right = max(a1, b1), min(a2, b2)
        if right - left <= tol:          # “长度”≈0 视为无重叠
            return None

        # 把投影点还原到 2D 端点 —— 在线段 p1‑p2 上按比例取值
        def interp(t):
            """t 为 0~1"""
            return (p1[0] + t * (p2[0] - p1[0]),
                    p1[1] + t * (p2[1] - p1[1]))

        len_p = a2 - a1 if a2 != a1 else 1e-9
        pa = interp((left - a1) / len_p)
        pb = interp((right - a1) / len_p)
        return pa, pb

    # ────────── 主流程 ──────────
    v1 = coords_to_xy_pairs(pl1.Coordinates)
    v2 = coords_to_xy_pairs(pl2.Coordinates)

    # 若为闭合 polyline，补一个首尾顶点
    if getattr(pl1, "Closed", False) and v1 and v1[0] != v1[-1]:
        v1.append(v1[0])
    if getattr(pl2, "Closed", False) and v2 and v2[0] != v2[-1]:
        v2.append(v2[0])

    segs1 = build_segments(v1, closed=False)
    segs2 = build_segments(v2, closed=False)

    overlaps = []

    for s1 in segs1:
        for s2 in segs2:
            ov = segment_overlap(s1, s2)
            if ov:
                pa, pb = ov
                overlaps.append([(pa[0], pa[1], 0.0), (pb[0], pb[1], 0.0)])
                break        # 一条 s1 找到重叠就够了，可跳出

    # --- 打印摘要 ---
    print("★ 与 pl2 重叠 (或被包含) 的 pl1 线段数：", len(overlaps))
    for idx, seg in enumerate(overlaps, 1):
        sys_logger.info(f"  {idx}. {seg[0]}  →  {seg[1]}")

    return overlaps




#  主函数
#  (8)
# 找到全部“两根多段线耦合成一个矩形”的多段线

#  该函数系列包括如下一些函数

"""
函数是用来分析主房间带卫生间这种情况的，因此对输入变量是有较严格假定的，并非针对任意情况

"""
# 1 判断矩形是否包含另一个矩形

#&&% 矩形包含判断
def is_rect_inside_rect(rect_outer, rect_inner, tol=1e-6):
    """
    判定 axis‑aligned 的矩形 rect_inner 是否被（含边界）完全包在 rect_outer 内。

    参数
    ----
    rect_outer : ((xmin, ymin), (xmax, ymax))
    rect_inner : ((xmin, ymin), (xmax, ymax))
        两个元组分别给出矩形左下、右上坐标（假定 Z 全 0）。
    tol        : float
        容差（允许轻微数值误差；AutoCAD double 转 python float 时推荐 1e‑6～1e‑4）。

    返回
    ----
    bool   ——  rect_inner ⊆ rect_outer ？
    """
    (ox0, oy0), (ox1, oy1) = rect_outer
    (ix0, iy0), (ix1, iy1) = rect_inner

    return (
        ix0 >= ox0 - tol and
        iy0 >= oy0 - tol and
        ix1 <= ox1 + tol and
        iy1 <= oy1 + tol
    )




# 2 判断两条正交多段线拼在一起后是否正好是一个矩形


#&&% 两多段线组矩形
def two_plines_making_rectangle(pl1, pl2, tol=0.5):#
    """
    判断两条正交多段线拼在一起后是否正好是一个矩形。
    假设：两 PLine 没有面积重叠，只可能共用完整边或边的一部分。
    """

    import math

    def same_point(a, b, tol):
        return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol

    def pline_vertices(pl):
        # 从 pl.Coordinates 提取 (x,y) 顶点列表，自动闭合
        c = pl.Coordinates
        verts = []
        for i in range(0, len(c), 2):
            verts.append((c[i], c[i+1]))
        if not same_point(verts[0], verts[-1], tol):
            verts.append(verts[0])
        return verts

    def poly_area(verts):
        # 计算首尾闭合的多边形面积
        s = 0
        for i in range(len(verts)-1):
            x1,y1 = verts[i]
            x2,y2 = verts[i+1]
            s += x1*y2 - x2*y1
        return abs(s)*0.5

    def collect_segments(verts):
        # 从顶点列表生成线段列表 [((x1,y1),(x2,y2)), ...]
        segs = []
        for i in range(len(verts)-1):
            segs.append((verts[i], verts[i+1]))
        return segs

    def covers_edge(edge, segs):
        """
        判断给定的 bbox 边 edge=((x0,y0),(x1,y1)) 能否被 segs 中若干共线线段
        连续覆盖（无缝隙）。
        """
        (x0,y0),(x1,y1) = edge
        # 算出方向向量和长度
        dx, dy = x1-x0, y1-y0
        L = math.hypot(dx, dy)
        if L < tol:
            return False
        ux, uy = dx/L, dy/L  # 单位方向向量

        # 投影每条 seg 到 [0,L] 参数区间
        intervals = []
        for (ax,ay),(bx,by) in segs:
            # 判断端点是否在同一直线上
            # cross == 0
            cross = (ax-x0)*dy - (ay-y0)*dx
            if abs(cross) > tol*L:  
                continue
            # 计算两端投影参数
            t1 = (  (ax-x0)*ux + (ay-y0)*uy )
            t2 = (  (bx-x0)*ux + (by-y0)*uy )
            a, b = min(t1,t2), max(t1,t2)
            # 只保留与 [0,L] 有交集的部分
            if b < -tol or a > L+tol:
                continue
            intervals.append((max(0.0, a), min(L, b)))

        if not intervals:
            return False

        # 合并所有区间
        intervals.sort(key=lambda iv: iv[0])
        cur_start, cur_end = intervals[0]
        for a,b in intervals[1:]:
            if a > cur_end + tol:
                # 出现间隙
                return False
            cur_end = max(cur_end, b)
        # 最后检测是否覆盖了整个 [0, L]
        return (cur_start <= tol) and (cur_end >= L - tol)

    # 1) 提取顶点及面积
    v1 = pline_vertices(pl1)
    v2 = pline_vertices(pl2)
    A1 = poly_area(v1)
    A2 = poly_area(v2)

    # 2) 计算公共外包矩形
    xs = [p[0] for p in v1[:-1]] + [p[0] for p in v2[:-1]]
    ys = [p[1] for p in v1[:-1]] + [p[1] for p in v2[:-1]]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    A_bbox = (xmax-xmin)*(ymax-ymin)

    # 3) 面积校验
    if abs((A1 + A2) - A_bbox) > tol:
        return False

    # 4) 检查四条边被覆盖
    bbox_edges = [
        ((xmin,ymin),(xmax,ymin)),
        ((xmax,ymin),(xmax,ymax)),
        ((xmax,ymax),(xmin,ymax)),
        ((xmin,ymax),(xmin,ymin))
    ]
    segs = collect_segments(v1) + collect_segments(v2)

    hits = 0
    for edge in bbox_edges:
        if covers_edge(edge, segs):
            hits += 1
    return hits == 4



#  主函数
#  (9)
#  判断多段线PL2是否在多段线PL1多边形中

#  该函数系列包括如下一些函数

#&&% 顶点全在内部
def are_all_vertices_inside(pl1, pl2):
    """
    判断多段线 pl2 的所有顶点是否都在多段线 pl1 构成的多边形内部。

    参数：
      pl1, pl2: COM 多段线对象（LWPOLYLINE 或 POLYLINE），视为封闭正多边形。
    返回：
      (all_inside, outside_pts)
      - all_inside: 如果 pl2 的每个顶点都在 pl1 内部，返回 True，否则 False。
      - outside_pts: 列表，包含所有落在 pl1 外部的 pl2 顶点 (x, y, z)。
    """
    # 先把 COM 多段线转成顶点列表 [(x,y,z), ...]
    verts1 = get_unique_vertices_from_pl_com(pl1)
    verts2 = get_unique_vertices_from_pl_com(pl2)

    outside_pts = []
    for pt in verts2:
        if not point_in_polygon(pt, verts1):
            outside_pts.append(pt)

    all_inside = len(outside_pts) == 0
    if all_inside:
        print("[OK] pl2 的所有顶点都在 pl1 的内部。")
    else:
        sys_logger.info(f"[错误] pl2 有 {len(outside_pts)} 个顶点不在 pl1 内部：")
        for p in outside_pts:
            print("   ", p)

    return all_inside, outside_pts



