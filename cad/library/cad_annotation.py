#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CAD注释与文字函数库
从CAD_basic.py中提取的注释、文字、标注相关函数
"""

# ================= 路径引导 =================
import sys
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

# ================= 导入系统模块 =================
from system.project_setup import PathConfig
from system.licad import C
from system.CAD_com_utils import sys_logger, retry_on_busy, SafeCOM
import win32com.client
import pythoncom
from win32com.client import VARIANT

# ================= 辅助函数 =================
def vtpnt(x, y, z):
    """将三维坐标转换为VARIANT类型"""
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [x, y, z])

#&&&&%% 注释文字模块

#&&&% 单行文字操作

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

#&&&% 多行文字操作

def write_mtext(
    text_content,
    insertion_point,
    width=1000,
    height=250,
    attachment_point=1,
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

        if layer_name:
            mtext_obj.Layer = layer_name

        return mtext_obj
    except Exception as e:
        sys_logger.info(f"[错误] 无法写入多行文字: {e}")
        return None

#&&&% 标注操作

#&&% 对齐标注
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

#&&% 旋转标注
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

#&&% 角度标注
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

#&&% 半径标注
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

#&&% 直径标注
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

#&&&% 引线操作

#&&% 添加引线
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

def get_text_content(text_obj):
    """
    获取文字对象的内容

    参数：
        text_obj: 文字对象

    返回：
        文字内容字符串；失败时返回 None
    """
    try:
        obj_type = text_obj.ObjectName

        if obj_type == "AcDbText":
            return text_obj.TextString
        elif obj_type == "AcDbMText":
            return text_obj.TextString
        else:
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

#&&&% 文字查询与修改

#&&% 获取文字旋转角度
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

#&&% 设置文字旋转角度
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

#&&% 批量修改文字
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

#&&&% 表格操作

#&&% 创建表格
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

#&&% 设置表格单元格文字
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

#&&% 获取表格单元格文字
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
    print("CAD注释与文字函数库")
    print("包含函数:")
    print("  - write_cad_text: 写入单行文字")
    print("  - write_mtext: 写入多行文字")
    print("  - add_dim_aligned: 添加对齐标注")
    print("  - add_dim_rotated: 添加旋转标注")
    print("  - add_leader: 添加引线")
    print("  - get_text_content: 获取文字内容")
    print("  - set_text_content: 设置文字内容")
    print("  - get_text_height: 获取文字高度")
    print("  - set_text_height: 设置文字高度")
