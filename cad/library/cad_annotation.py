#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CAD注释与文字函数库
"""

import time
import re

from system.licad import C
from system.CAD_com_utils import sys_logger, retry_on_busy, SafeCOM
from system.CAD_coordination import wait_command_done
from system.CAD_selection import get_attr, set_entity_grip_state_precise
import win32com.client
import pythoncom
from win32com.client import VARIANT


def vtpnt(x, y, z):
    """将三维坐标转换为VARIANT类型"""
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [x, y, z])


def write_cad_text(
    text_content,
    insertion_point,
    height=250,
    rotation=0,
    style="Standard",
    layer_name=None,
    color_index=256
):
    """
    在CAD中写入单行文字

    参数：
        text_content: 文字内容
        insertion_point: 插入点 (x, y, z)
        height: 文字高度
        rotation: 旋转角度（弧度）
        style: 文字样式名称
        layer_name: 图层名称
        color_index: 颜色索引

    返回：
        新创建的文字对象；失败时返回 None
    """
    try:
        text_obj = C.mp.AddText(
            str(text_content),
            vtpnt(*insertion_point),
            height
        )
        text_obj.Rotation = rotation

        if style:
            text_obj.StyleName = style

        if layer_name:
            text_obj.Layer = layer_name

        if color_index != 256:
            text_obj.Color = color_index

        return text_obj
    except Exception as e:
        sys_logger.info(f"[错误] 无法写入文字: {e}")
        return None


def write_mtext(
    text_content,
    insertion_point,
    width=1000,
    height=250,
    attachment_point=1,
    style="Standard",
    layer_name=None
):
    """
    在CAD中写入多行文字

    参数：
        text_content: 文字内容
        insertion_point: 插入点 (x, y, z)
        width: 文字框宽度
        height: 文字高度
        attachment_point: 附着点（1-9）
        style: 文字样式名称
        layer_name: 图层名称

    返回：
        新创建的多行文字对象；失败时返回 None
    """
    try:
        mtext_obj = C.mp.AddMText(
            vtpnt(*insertion_point),
            width,
            str(text_content)
        )
        mtext_obj.Height = height
        mtext_obj.AttachmentPoint = attachment_point

        if style:
            mtext_obj.StyleName = style

        if layer_name:
            mtext_obj.Layer = layer_name

        return mtext_obj
    except Exception as e:
        sys_logger.info(f"[错误] 无法写入多行文字: {e}")
        return None


def add_dim_aligned(p1, p2, p3):
    """
    添加对齐标注

    参数：
        p1: 第一个标注点 (x, y, z)
        p2: 第二个标注点 (x, y, z)
        p3: 标注线位置点 (x, y, z)

    返回：
        新创建的标注对象；失败时返回 None
    """
    try:
        dim_obj = C.mp.AddDimAligned(
            vtpnt(*p1),
            vtpnt(*p2),
            vtpnt(*p3)
        )
        return dim_obj
    except Exception as e:
        sys_logger.info(f"[错误] 无法添加对齐标注: {e}")
        return None

def add_dim_rotated(p1, p2, p3, angle=0):
    """
    添加旋转标注

    参数：
        p1: 第一个标注点 (x, y, z)
        p2: 第二个标注点 (x, y, z)
        p3: 标注线位置点 (x, y, z)
        angle: 旋转角度（弧度）

    返回：
        新创建的标注对象；失败时返回 None
    """
    try:
        dim_obj = C.mp.AddDimRotated(
            vtpnt(*p1),
            vtpnt(*p2),
            vtpnt(*p3),
            angle
        )
        return dim_obj
    except Exception as e:
        sys_logger.info(f"[错误] 无法添加旋转标注: {e}")
        return None

def add_dim_angular(vertex, p1, p2, p3):
    """
    【新增】添加角度标注

    Args:
        vertex: 角顶点 (x, y, z)
        p1: 第一条边上的点
        p2: 第二条边上的点
        p3: 标注文字位置

    Returns:
        标注对象
    """
    try:
        dim_obj = C.mp.AddDimAngular(
            vtpnt(*vertex),
            vtpnt(*p1),
            vtpnt(*p2),
            vtpnt(*p3)
        )
        return dim_obj
    except Exception as e:
        sys_logger.error(f"[错误] add_dim_angular 失败: {e}")
        return None

def add_dim_radial(center, chord_point, leader_length=None):
    """
    【新增】添加半径标注

    Args:
        center: 圆心 (x, y, z)
        chord_point: 圆上一点
        leader_length: 引线长度(可选)

    Returns:
        标注对象
    """
    try:
        dim_obj = C.mp.AddDimRadial(
            vtpnt(*center),
            vtpnt(*chord_point),
            leader_length or 1.0
        )
        return dim_obj
    except Exception as e:
        sys_logger.error(f"[错误] add_dim_radial 失败: {e}")
        return None

def add_dim_diametric(chord_point, far_chord_point, leader_length=None):
    """
    【新增】添加直径标注

    Args:
        chord_point: 圆上第一点
        far_chord_point: 圆上对侧点
        leader_length: 引线长度(可选)

    Returns:
        标注对象
    """
    try:
        dim_obj = C.mp.AddDimDiametric(
            vtpnt(*chord_point),
            vtpnt(*far_chord_point),
            leader_length or 1.0
        )
        return dim_obj
    except Exception as e:
        sys_logger.error(f"[错误] add_dim_diametric 失败: {e}")
        return None


def add_leader(points, annotation=None):
    """
    添加引线

    参数：
        points: 引线点列表 [(x1,y1,z1), (x2,y2,z2), ...]
        annotation: 注释对象（可选）

    返回：
        新创建的引线对象；失败时返回 None
    """
    try:
        # 将点列表展平
        pts_flat = []
        for pt in points:
            pts_flat.extend([pt[0], pt[1], pt[2]])

        v_pts = win32com.client.VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_R8,
            pts_flat
        )

        leader_obj = C.mp.AddLeader(v_pts, annotation, 0)  # 0 = acLineWithArrow
        return leader_obj
    except Exception as e:
        sys_logger.info(f"[错误] 无法添加引线: {e}")
        return None

def _get_text_fragment_sort_info(ent, tolerance=0.3):
    """返回文字碎片的行桶与 X 坐标，用于天正多行文字排序。"""
    ins = get_attr(ent, "InsertionPoint")
    if not ins:
        try:
            min_p, _ = ent.GetBoundingBox()
            return round(min_p[1] / tolerance), min_p[0]
        except Exception:
            return 0, 0
    return round(ins[1] / tolerance), ins[0]

def _clean_text_content(text):
    """
    提取纯文字内容，剥离常见 MText 格式控制码与排版控制信息。
    """
    if text is None:
        return ""

    s = str(text).strip()
    if not s:
        return ""

    # 剥离开头连续的格式前缀，如 \W0.8;、\C1;、\pxt9;。
    while s.startswith("\\") and ";" in s:
        left, right = s.split(";", 1)
        if "\\" in left[1:]:
            break
        s = right.lstrip()

    # 常见段落/空格控制转为普通空白。
    s = s.replace("\\P", " ")
    s = s.replace("\\~", " ").replace("\r", " ").replace("\n", " ")

    # 剥离正文中残留的分号型控制码。
    s = re.sub(r"\\[A-Za-z][^;\\{}]*;", "", s)

    # 去掉大括号分组等版式痕迹。
    s = s.replace("{", "").replace("}", "")

    # 归一空白，返回纯文本。
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def _get_tdb_mtext_content(text_obj, separator="\n"):
    """
    复制并炸开天正多行文字，按行重建内容。

    这里沿用已验证有效的“副本炸开 + Y/X 排序 + 行切换插入换行符”经验，
    统一兼容 cad_annotation 对 TDbMText 的读取。
    """
    try:
        C.li()
    except Exception:
        pass

    fragments = []
    copy_ent = None

    marker = None

    try:
        try:
            copy_ent = text_obj.Copy()
        except Exception as exc:
            sys_logger.info(f"[错误] 复制天正对象失败: {exc}")
            return ""

        try:
            marker = C.mp.AddLine(
                VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0]),
                VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [1.0, 1.0, 0.0]),
            )
        except Exception as exc:
            sys_logger.info(f"[错误] 无法创建炸开辅助线: {exc}")
            return ""

        marker_handle = marker.Handle
        if not set_entity_grip_state_precise(copy_ent):
            sys_logger.info("[错误] 无法精确选中 TDbMText 副本，取消炸开。")
            return ""

        C.doc.SendCommand("._EXPLODE\n")
        wait_command_done(timeout=20.0, quiet_time=0.5)
        time.sleep(0.5)

        for idx in range(C.mp.Count - 1, -1, -1):
            try:
                obj = C.mp.Item(idx)
            except Exception:
                continue
            if obj.Handle == marker_handle:
                break
            fragments.append(obj)

        if not fragments:
            return ""

        fragments.sort(
            key=lambda ent: (
                -_get_text_fragment_sort_info(ent)[0],
                _get_text_fragment_sort_info(ent)[1],
            )
        )

        final_parts = []
        last_y_bin = None
        for frag in fragments:
            txt = get_attr(frag, "TextString")
            if not txt:
                continue

            current_y_bin, _ = _get_text_fragment_sort_info(frag)
            if last_y_bin is not None and current_y_bin != last_y_bin:
                final_parts.append(separator)

            final_parts.append(_clean_text_content(txt))
            last_y_bin = current_y_bin

        return "".join(final_parts)
    except Exception as exc:
        sys_logger.info(f"[错误] 提取天正多行文字内容失败: {exc}")
        return ""
    finally:
        for frag in fragments:
            try:
                frag.Delete()
            except Exception:
                pass
        if marker is not None:
            try:
                marker.Delete()
            except Exception:
                pass
        if copy_ent is not None:
            try:
                copy_ent.Delete()
            except Exception:
                pass

def get_text_content(text_obj):
    """
    获取文字对象的内容

    参数：
        text_obj: 文字对象

    返回：
        文字内容字符串；失败时返回 None
    """
    try:
        obj_type = str(get_attr(text_obj, "ObjectName", getattr(text_obj, "ObjectName", "")))

        if obj_type in {"AcDbText", "Text"}:
            return _clean_text_content(get_attr(text_obj, "TextString", None))
        if obj_type in {"AcDbMText", "MText"}:
            return _clean_text_content(get_attr(text_obj, "TextString", None))
        if obj_type == "TDbText":
            return _clean_text_content(get_attr(text_obj, "Text", get_attr(text_obj, "TextString", None)))
        if obj_type == "TDbMText":
            return _clean_text_content(_get_tdb_mtext_content(text_obj))

        sys_logger.info(f"[警告] 不支持的对象类型: {obj_type}")
        return None
    except Exception as e:
        sys_logger.info(f"[错误] 无法获取文字内容: {e}")
        return None

def set_text_content(text_obj, new_content):
    """
    设置文字对象的内容

    参数：
        text_obj: 文字对象
        new_content: 新的文字内容

    返回：
        成功返回 True，失败返回 False
    """
    try:
        obj_type = text_obj.ObjectName

        if obj_type in ["AcDbText", "AcDbMText"]:
            text_obj.TextString = str(new_content)
            return True
        else:
            sys_logger.info(f"[警告] 不支持的对象类型: {obj_type}")
            return False
    except Exception as e:
        sys_logger.info(f"[错误] 无法设置文字内容: {e}")
        return False

def get_text_height(text_obj):
    """
    获取文字高度

    参数：
        text_obj: 文字对象

    返回：
        文字高度；失败时返回 None
    """
    try:
        return text_obj.Height
    except Exception as e:
        sys_logger.info(f"[错误] 无法获取文字高度: {e}")
        return None

def set_text_height(text_obj, height):
    """
    设置文字高度

    参数：
        text_obj: 文字对象
        height: 新的高度值

    返回：
        成功返回 True，失败返回 False
    """
    try:
        text_obj.Height = height
        return True
    except Exception as e:
        sys_logger.info(f"[错误] 无法设置文字高度: {e}")
        return False


def get_text_rotation(text_obj):
    """
    【新增】获取文字旋转角度

    Args:
        text_obj: 文字对象

    Returns:
        旋转角度(弧度)
    """
    try:
        return text_obj.Rotation
    except Exception as e:
        sys_logger.error(f"[错误] get_text_rotation 失败: {e}")
        return None

def set_text_rotation(text_obj, rotation):
    """
    【新增】设置文字旋转角度

    Args:
        text_obj: 文字对象
        rotation: 旋转角度(弧度)

    Returns:
        成功返回True
    """
    try:
        text_obj.Rotation = rotation
        return True
    except Exception as e:
        sys_logger.error(f"[错误] set_text_rotation 失败: {e}")
        return False

def batch_modify_text(text_objs, **kwargs):
    """
    【新增】批量修改文字属性

    Args:
        text_objs: 文字对象列表
        **kwargs: 要修改的属性(height, rotation, content等)

    Returns:
        成功修改的数量
    """
    count = 0
    for text_obj in text_objs:
        try:
            if 'height' in kwargs:
                set_text_height(text_obj, kwargs['height'])
            if 'rotation' in kwargs:
                set_text_rotation(text_obj, kwargs['rotation'])
            if 'content' in kwargs:
                set_text_content(text_obj, kwargs['content'])
            count += 1
        except Exception as e:
            sys_logger.error(f"[错误] 修改文字失败: {e}")
    return count


def create_table(insertion_point, rows, cols, row_height=300, col_width=1000):
    """
    【新增】创建表格

    Args:
        insertion_point: 插入点 (x, y, z)
        rows: 行数
        cols: 列数
        row_height: 行高
        col_width: 列宽

    Returns:
        表格对象
    """
    try:
        table_obj = C.mp.AddTable(
            vtpnt(*insertion_point),
            rows,
            cols,
            row_height,
            col_width
        )
        return table_obj
    except Exception as e:
        sys_logger.error(f"[错误] create_table 失败: {e}")
        return None

def set_table_cell_text(table_obj, row, col, text):
    """
    【新增】设置表格单元格文字

    Args:
        table_obj: 表格对象
        row: 行号(从0开始)
        col: 列号(从0开始)
        text: 文字内容

    Returns:
        成功返回True
    """
    try:
        table_obj.SetText(row, col, str(text))
        return True
    except Exception as e:
        sys_logger.error(f"[错误] set_table_cell_text 失败: {e}")
        return False

def get_table_cell_text(table_obj, row, col):
    """
    【新增】获取表格单元格文字

    Args:
        table_obj: 表格对象
        row: 行号
        col: 列号

    Returns:
        单元格文字内容
    """
    try:
        return table_obj.GetText(row, col)
    except Exception as e:
        sys_logger.error(f"[错误] get_table_cell_text 失败: {e}")
        return None

if __name__ == "__main__":
    sys_logger.info("CAD注释与文字函数库")
    sys_logger.info("包含函数:")
    sys_logger.info("  - write_cad_text: 写入单行文字")
    sys_logger.info("  - write_mtext: 写入多行文字")
    sys_logger.info("  - add_dim_aligned: 添加对齐标注")
    sys_logger.info("  - add_dim_rotated: 添加旋转标注")
    sys_logger.info("  - add_leader: 添加引线")
    sys_logger.info("  - get_text_content: 获取文字内容")
    sys_logger.info("  - set_text_content: 设置文字内容")
    sys_logger.info("  - get_text_height: 获取文字高度")
    sys_logger.info("  - set_text_height: 设置文字高度")

