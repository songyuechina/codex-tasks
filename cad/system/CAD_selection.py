#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# D:/codex-tasks/cad/system/CAD_selection.py 
# 依赖: CAD_com_utils.py, licad.py
#版本V2.0 (Refactored)
import sys
import math
import time
import uuid
import array
import random
import pythoncom
import win32com.client as win32
from win32com.client import VARIANT, CastTo
import win32com.client.dynamic
from functools import wraps

#  引导代码 (确保能找到 system)
import os

from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))
from system.project_setup import PathConfig

from system.CAD_com_utils import (
    sys_logger, 
     
    timeit,       # <--- 确保这里有
    # debuggable, # <--- 如果没用到就不用引
)




# ==============================================================================
#                            API MANIFEST / 完整函数签名清单
# ==============================================================================
"""
1. 核心工具 (Core & Utils)
--------------------------------------------------------------------------------
[CORE-000]   com_retry(fn, retries=30, delay=0.05)
             : COM调用重试装饰器，自动处理 RPC_BUSY (-2147417846) 等错误。
             
[CORE-002-1] cast_object(obj)
             : [入口] 智能类型转换，将 IAcadEntity 转为具体接口 (如 IAcadLine)。
             
[CORE-002]   _maybe_cast(ent)
             : [核心] 转换核心，混合了查表(CastTo)、动态封装(Dynamic)和兜底策略。
             
[UTILS-001]  to_vt_int(seq)
             : 列表 -> COM 整数变体数组 (VT_I2)。
             
[UTILS-002]  to_vt_variant(seq)
             : 列表 -> COM 变体数组 (VT_VARIANT)。
             
[UTILS-003]  _to_vt_point(pt_tuple)
             : (x,y,z) -> COM 浮点变体数组 (VT_R8)。
             
[UTILS-004]  normalize_rect(x1, y1, x2, y2)
             : 坐标标准化，返回 ((min_x, min_y), (max_x, max_y))。
             
[UTILS-005]  expand_rectangle(p1, p2, offset)
             : 矩形向外扩充 offset 距离。

2. 基础选择引擎 (Selection Engine)
--------------------------------------------------------------------------------
[SEL-001]    ss_select(mode="all", p1=None, p2=None, filter_types=None, filter_data=None, autocast=True, prompt=None)
             : 通用选择集构造器。
             : mode: "all"|"window"|"crossing"|"onscreen"
             : filter_types/data: DXF 组码过滤 (如 [0], ["INSERT"])

3. 几何与空间选择 (Geometric Selection)
--------------------------------------------------------------------------------
[SEL-GEO-001] select_entities_through_point(p, tol=0.1)
              : 点选。通过构造 tol 大小的窗交区域模拟鼠标点击。
              
[SEL-GEO-002] select_objects_in_window_area(x1, y1, x2, y2, max_retry=5)
              : 隐性窗口选择。自动 Zoom 到区域防止选不中，支持重试。
              
[SEL-GEO-003] select_paperspace_objects_in_window(x1, y1, x2, y2)
              : 布局空间区域选择。结合 Window 选择和 BoundingBox 遍历。
              
[SEL-GEO-004] pmxz(prompt="\n请在屏幕拾取图元，以Enter键结束：", autocast=True)
              : 屏幕交互框选 (GetSelection)。
              
[SEL-GEO-005] get_last_n_objects(n=1, autocast=True)
              : 获取模型空间最后生成的 N 个对象。
              
[SEL-GEO-006] last_obj()
              : 获取最后一个对象 (快捷方式)。

4. 类型与图层选择 (Type & Layer Selection)
--------------------------------------------------------------------------------
[SEL-TYPE-001] select_tuceng(layer_names, max_retries=5, delay=0.5, autocast=True)
               : 按图层名选择 (支持 str 或 list[str])。
               
[SEL-ALIAS]    stc(layer_names, **kwargs)
               : select_tuceng 的简写别名。
               
[SEL-TYPE-002] select_kuai(max_retries=5, autocast=True)
               : 全选普通块引用 (INSERT)。
               
[SEL-TYPE-003] select_text(autocast=True) / select_mtext(autocast=True)
               : 全选单行文字 (TEXT) / 多行文字 (MTEXT)。
               
[SEL-TYPE-004] select_line(autocast=True) / select_circle(autocast=True) / select_ellipse(autocast=True)
               : 全选直线 / 圆 / 椭圆。
               
[SEL-TYPE-005] select_polyline(autocast=True)
               : 全选轻量多段线 (LWPOLYLINE)。
               
[SEL-TYPE-006] select_polyline_chuantong(autocast=True)
               : 全选二维多段线 (POLYLINE)。
               
[SEL-TYPE-007] select_spline(autocast=True)
               : 全选样条曲线 (SPLINE)。
               
[SEL-TYPE-011] select_all_texts_mixed(target_space="Model")
               : 混合全选。包含 CAD 文字(*TEXT) 和 天正文字(TDb*)。
               
[SEL-TYPE-012] select_pub_text_entities()
               : 专选 "PUB_TEXT" 图层上的 TDbText 和 TDbMText。
               
[SEL-TYPE-013] select_group_entities(group_obj)
               : 选择组 (Group) 内的所有对象。

5. 可视化与交互 (Visualization & Interaction)
--------------------------------------------------------------------------------
[VIS-001]    yin_to_xian_xuanze(LB, wait_s=0.6)
             : 隐转显 (Delete/Undo法)。强制将 LB 列表放入当前选择集 (兼容性好但慢)。
             
[VIS-002]    yin_to_xian_safe(LB, wait_s=0.1)
             : [推荐] 隐转显 (LISP sssetfirst法)。无副作用高亮选中对象。
             
[VIS-003]    xian_to_yin_pickfirst(clear_grips=True, autocast=True)
             : 获取当前编辑器选中的对象 (Pickfirst)。
             
[VIS-004]    select_entities_in_window(x1, y1, x2, y2, ty=1.0, select_mode="_W")
             : 区域高亮并返回对象。Zoom -> Select -> Pickfirst -> Return。
             
[VIS-005]    highlight_entities_in_window(x1, y1, x2, y2)
             : 仅高亮区域 (视觉提示)。
             
[VIS-006]    highlight_entity_by_bbox(entity)
             : 高亮单个对象 (基于包围盒，对 TDbWall 有额外偏移优化)。
             
[VIS-007]    set_entity_grip_state_precise(ent)
             : 独占式高亮。清除其他选中，仅显示该对象的夹点。
             
[VIS-008]    isolate_modelspace_area(x1, y1, x2, y2)
             : 隔离显示。仅显示区域内对象，隐藏其他 (IsolateObjects)。
             
[VIS-009]    unhide_all(space=None, filter_names=None, highlight=False)
             : 显示隐藏对象 (Visible = True)。

6. 属性与天正支持 (Properties & TArch)
--------------------------------------------------------------------------------
[PROP-000]   _resolve_attr_case_insensitive(obj, attr_name)
             : 属性名大小写智能解析 (PascalCase 优先，缓存加速)。
             
[PROP-001]   get_attr(obj, name)
             : [万能] 获取属性。自动判断天正(Invoke DISPID) 或 普通CAD对象。
             
[PROP-002]   set_attr(obj, name, value)
             : [万能] 设置属性。自动判断天正(Invoke DISPID) 或 普通CAD对象。
             
[PROP-OLD]   get_object_property(obj, property_name) / set_object_property(obj, property_name, value)
             : 兼容旧代码的属性读写接口。
             
[PROP-003]   brute_dump_tarch_props(ent, max_dispid=64)
             : [调试] 暴力扫描天正对象属性 ID (1~max_dispid)。
"""

__all__ = [
    'com_retry', 'cast_object', '_maybe_cast', 
    'ss_select', 
    'select_entities_through_point', 'select_objects_in_window_area', 'select_paperspace_objects_in_window',
    'pmxz', 'get_last_n_objects', 'last_obj',
    'select_tuceng', 'stc', 'select_kuai', 'select_text', 'select_mtext', 
    'select_line', 'select_circle', 'select_ellipse', 'select_polyline', 'select_spline','select_polyline_chuantong',
    'select_all_texts_mixed', 'select_pub_text_entities', 'select_group_entities',
    'yin_to_xian_xuanze', 'yin_to_xian_safe', 'xian_to_yin_pickfirst', 
    'select_entities_in_window', 'highlight_entities_in_window', 'highlight_entity_by_bbox', 
    'set_entity_grip_state_precise', 'isolate_modelspace_area', 'unhide_all',
    'get_attr', 'set_attr', 'get_object_property', 'set_object_property', 'brute_dump_tarch_props'
]
# =================================================================
# 1. 核心引用 (集成新架构)
# =================================================================
try:
    from system.licad import C
    # 【关键】引入通用防崩工具
    from system.CAD_com_utils import retry_on_busy, SafeCOM
except ImportError:
    print("❌ [严重错误] 无法导入 licad 或 CAD_com_utils，请检查文件位置！")
    raise

# =================================================================
# 2. 核心工具与类型转换
# =================================================================

_CAST_MAP = {
    # --- 基础线形 ---
    "AcDbLine": "IAcadLine",
    "AcDbCircle": "IAcadCircle",
    "AcDbArc": "IAcadArc",
    "AcDbEllipse": "IAcadEllipse",
    "AcDbSpline": "IAcadSpline",
    "AcDbPoint": "IAcadPoint",
    "AcDbXline": "IAcadXline",       # 构造线
    "AcDbRay": "IAcadRay",           # 射线

    # --- 多段线与多线 ---
    "AcDbPolyline": "IAcadLWPolyline",    # 轻量多段线 (最常见)
    "AcDb2dPolyline": "IAcadPolyline",    # 老式二维多段线 (重多段线)
    "AcDb3dPolyline": "IAcad3DPolyline",  # 三维多段线
    "AcDbMline": "IAcadMline",            # 多线 (MLINE)

    # --- 文字与属性 ---
    "AcDbText": "IAcadText",
    "AcDbMText": "IAcadMText",
    "AcDbAttribute": "IAcadAttributeReference",
    "AcDbAttributeDefinition": "IAcadAttribute",
    "AcDbFcf": "IAcadTolerance",          # 形位公差 (Feature Control Frame)

    # --- 块、引用与表格 ---
    "AcDbBlockReference": "IAcadBlockReference",
    "AcDbMInsertBlock": "IAcadMInsertBlock",
    "AcDbTable": "IAcadTable",
    "AcDbHatch": "IAcadHatch",            # 填充
    "AcDbRegion": "IAcadRegion",          # 面域
    "AcDbRasterImage": "IAcadRasterImage",# 图片
    "AcDbWipeout": "IAcadWipeout",        # 区域覆盖
    "AcDbOle2Frame": "IAcadOle",          # OLE 对象 (Excel表格等)

    # --- 标注 (Dimensions) ---
    "AcDbDimension": "IAcadDimension",
    "AcDbAlignedDimension": "IAcadDimAligned",
    "AcDbRotatedDimension": "IAcadDimRotated",
    "AcDb3PointAngularDimension": "IAcadDim3PointAngular",
    "AcDb2LineAngularDimension": "IAcadDim2LineAngular",
    "AcDbDiametricDimension": "IAcadDimDiametric",
    "AcDbRadialDimension": "IAcadDimRadial",
    "AcDbOrdinateDimension": "IAcadDimOrdinate",
    "AcDbArcDimension": "IAcadDimArc",
    "AcDbRadialDimensionLarge": "IAcadDimRadialLarge", # 折弯半径标注

    # --- 引线 ---
    "AcDbLeader": "IAcadLeader",      # 旧式引线
    "AcDbMLeader": "IAcadMLeader",    # 多重引线

    # --- 3D 实体与网格 (Solid & Mesh) ---
    "AcDb3dSolid": "IAcad3DSolid",    # 3D 实体 (立方体、球体等)
    "AcDbSurface": "IAcadSurface",    # 3D 曲面
    "AcDbFace": "IAcad3DFace",        # 3D 面
    "AcDbPolyFaceMesh": "IAcadPolyfaceMesh", # 多面网格
    "AcDbPolygonMesh": "IAcadPolygonMesh",   # 多边形网格
    "AcDbSubDMesh": "IAcadSubDMesh",         # 细分网格
    "AcDbHelix": "IAcadHelix",               # 螺旋线

    # --- 2D 填充与痕迹 ---
    "AcDbSolid": "IAcadSolid",        # 2D 实心填充 (非3D实体)
    "AcDbTrace": "IAcadTrace",        # 宽线/痕迹
    "AcDbShape": "IAcadShape",        # 形 (load shape file)

    # --- 布局、视口与其它 ---
    "AcDbViewport": "IAcadViewport",  # 视口
    "AcDbLayout": "IAcadLayout",      # 布局
    "AcDbGroup": "IAcadGroup",        # 组
    "AcDbDictionary": "IAcadDictionary", # 字典
}



def cast_object(obj):
    return _maybe_cast(obj)

def _maybe_cast(ent):
    """
    【CORE-002】智能类型转换
    注意：此函数内部不加 @retry_on_busy，因为它通常在循环中被密集调用。
    如果 ent 本身已经失效，外层的 SafeCOM.list_selection 会处理。
    """
    if ent is None: return None
    
    # 性能优化
    if hasattr(ent, 'CLSID'): pass 

    try:
        # 这里可能触发 COM 通讯，如果在这里崩了，外层的 retry_on_busy 会捕获
        temp_ent = win32.gencache.EnsureDispatch(ent)
        obj_name = getattr(temp_ent, "ObjectName", "")

        if obj_name in _CAST_MAP:
            return CastTo(temp_ent, _CAST_MAP[obj_name])
        
        if not obj_name.startswith("TDb"):
            try:
                return win32com.client.dynamic.Dispatch(temp_ent)
            except: pass
            
        return temp_ent
    except Exception:
        return ent

# --- 内部辅助 (保持不变) ---
def to_vt_int(seq):
    return VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I2, list(seq))

def to_vt_variant(seq):
    return VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, list(seq))

def _to_vt_point(pt_tuple):
    if not pt_tuple: return None
    return VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [float(x) for x in pt_tuple])

def pt3(x, y, z=0):
    return VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [x, y, z])

def normalize_rect(x1, y1, x2, y2):
    x_lo, x_hi = sorted((x1, x2))
    y_lo, y_hi = sorted((y1, y2))
    return (x_lo, y_lo), (x_hi, y_hi)

def expand_rectangle(p1, p2, offset):
    x1, y1 = float(p1[0]), float(p1[1])
    x2, y2 = float(p2[0]), float(p2[1])
    return normalize_rect(x1 - offset, y1 - offset, x2 + offset, y2 + offset)

# --- 兼容旧代码接口 (关键修复) ---
def com_retry(fn, retries=30, delay=0.05):
    """
    【兼容补丁】
    旧脚本调用 com_retry(func) 时，
    自动转发给新架构的 retry_on_busy 进行保护
    """
    # 动态构建装饰器并立即执行
    # 注意：旧代码 delay=0.05 (50ms)，新架构默认 0.5s
    # 这里我们折中一下用 0.1s，或者保留您的习惯
    wrapper = retry_on_busy(max_retries=retries, base_delay=delay)(fn)
    return wrapper()

#&&% 限定空间装饰器
def current_space_only(func):
    """
    【装饰器】过滤结果，只保留属于当前激活空间（模型或当前布局）的对象。
    
    使用条件：
    1. 被装饰的函数必须返回一个列表或可迭代对象 (list/tuple)。
    2. 列表中的元素必须是 CAD 的实体对象 (拥有 OwnerID 属性)。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1. 获取原始函数的全部结果
        all_objects = func(*args, **kwargs)
        
        if not all_objects:
            return []

        # 2. 获取当前激活空间的 ID
        # doc.ActiveLayout.Block 就是当前也就是所谓 "ModelSpace" 或 "PaperSpaceX" 的容器
        try:
            doc = C.doc
            current_space_id = doc.ActiveLayout.Block.ObjectID
        except Exception as e:
            sys_logger.error(f"无法获取当前空间 ID: {e}")
            return all_objects # 降级处理：获取失败则不过滤，避免造成空数据风险

        # 3. 执行过滤 (比对 OwnerID)
        filtered_objects = []
        for obj in all_objects:
            try:
                if obj.OwnerID == current_space_id:
                    filtered_objects.append(obj)
            except:
                # 某些特殊对象可能访问 OwnerID 报错，跳过
                pass
                
        return filtered_objects

    return wrapper



# =================================================================
# 3. 基础选择核心 (Selection Engine) - 【核心重构区域】
# =================================================================

@retry_on_busy
@current_space_only
def ss_select(mode="all", p1=None, p2=None, filter_types=None, filter_data=None, autocast=True, prompt=None):
    """
    【SEL-001】通用选择集构造器 (重构版)
    利用 SafeCOM 和 retry_on_busy 自动处理所有 COM 交互细节
    """
    doc = C.doc
    # 使用 UUID 确保唯一性，不再需要 Delete 旧集合的 try-catch
    ss_name = f"SS_{uuid.uuid4().hex[:8]}"
    ss = doc.SelectionSets.Add(ss_name)

    try:
        if mode == "onscreen":
            if prompt:
                try: doc.Utility.Prompt(prompt)
                except: pass
            ss.SelectOnScreen()
            
        elif mode in ("all", "window", "crossing"):
            if filter_types is None:
                f_types, f_data = [8], ["*"]
            else:
                f_types, f_data = filter_types, filter_data

            selmode = 5 if mode == "all" else (0 if mode == "window" else 1)
            vt_p1 = _to_vt_point(p1) if mode != "all" else None
            vt_p2 = _to_vt_point(p2) if mode != "all" else None

            # 执行选择 (这里受 @retry_on_busy 保护)
            ss.Select(
                selmode, vt_p1, vt_p2,
                to_vt_int(f_types) if f_types else None,
                to_vt_variant(f_data) if f_data else None
            )
        else:
            raise ValueError(f"未知模式: {mode}")

        # 【优化】使用 SafeCOM 批量转换，极大提高稳定性
        # 它会自动处理 ss.Count 和 ss.Item(i) 的循环重试
        raw_items = SafeCOM.list_selection(ss)
        
        if autocast:
            return [_maybe_cast(e) for e in raw_items]
        return raw_items

    finally:
        # 清理工作
        try: ss.Delete()
        except: pass

# =================================================================
# 4. 几何与空间选择 (Geometric Selection)
# =================================================================

@retry_on_busy
def select_entities_through_point(p, tol=0.1):
    """【SEL-GEO-001】点选"""
    px, py = p[0], p[1]
    p1 = (px - tol, py - tol, 0.0)
    p2 = (px + tol, py + tol, 0.0)

    selected = ss_select("crossing", p1=p1, p2=p2, autocast=True)
    
    valid_kws = ["Line", "Circle", "Arc", "Polyline", "Spline", "BlockReference", "Insert", "TDb"]
    valid_objs = []
    for obj in selected:
        name = getattr(obj, "ObjectName", "") or getattr(obj, "EntityName", "")
        if any(k in name for k in valid_kws):
            valid_objs.append(obj)
    return valid_objs

@retry_on_busy(max_retries=5) # 包含 Zoom 操作，值得重试

def select_objects_in_window_area(x1, y1, x2, y2):
    """【SEL-GEO-002】隐性窗口选择（带自动 Zoom）"""
    acad = C.acad
    doc = C.doc

    cx, cy = (x1 + x2)/2, (y1 + y2)/2
    w, h = abs(x2 - x1), abs(y2 - y1)
    
    margin = 1.2
    z_x1, z_y1 = cx - (w*margin)/2, cy - (h*margin)/2
    z_x2, z_y2 = cx + (w*margin)/2, cy + (h*margin)/2

    zoom_p1 = array.array('d', [z_x1, z_y1, 0.0])
    zoom_p2 = array.array('d', [z_x2, z_y2, 0.0])

    try: acad.ZoomWindow(zoom_p1, zoom_p2)
    except: doc.SendCommand(f"_Zoom _W {z_x1},{z_y1} {z_x2},{z_y2} ")
    
    # 稍作等待让视图刷新，但不需要 sleep 很久，因为 Select 会自动等
    time.sleep(0.05) 
    
    return ss_select("window", [x1, y1, 0], [x2, y2, 0], autocast=True)

@retry_on_busy
def select_paperspace_objects_in_window(x1, y1, x2, y2):
    """【SEL-GEO-003】图纸空间区域选择"""
    doc = C.doc
    try: doc.SetVariable("TILEMODE", 0)
    except: pass

    (x_lo, y_lo), (x_hi, y_hi) = normalize_rect(x1, y1, x2, y2)
    
    # 尝试1: 窗口选择
    items = ss_select("window", pt3(x_lo, y_lo), pt3(x_hi, y_hi), autocast=True)
    if items: return items

    # 尝试2: 遍历包围盒 (使用 SafeCOM 保护遍历)
    sp = C.sp 
    selected = []
    def intersects(a1, a2, b1, b2): return (a1 <= b2) and (a2 >= b1)
    
    # 获取布局空间所有对象
    all_ents = SafeCOM.list_selection(sp) # <--- 优化点
    
    for ent in all_ents:
        try:
            min_p, max_p = ent.GetBoundingBox()
            if intersects(min_p[0], max_p[0], x_lo, x_hi) and \
               intersects(min_p[1], max_p[1], y_lo, y_hi):
                selected.append(_maybe_cast(ent))
        except: continue
    return selected

def pmxz(prompt="\n请在屏幕拾取图元，以Enter键结束：", autocast=True):
    return ss_select("onscreen", prompt=prompt, autocast=autocast)

@retry_on_busy
def get_last_n_objects(n=1, autocast=True):
    """【SEL-GEO-005】获取最后生成的 N 个图元"""
    mp = C.mp
    count = mp.Count
    if count == 0: return []
    
    start = max(0, count - n)
    objs = []
    for i in range(start, count):
        try:
            # 单个获取也要保护，这里用 retry 保护整个函数其实已经够了
            # 如果想极致安全，可以用 SafeCOM.call(lambda: mp.Item(i))
            item = mp.Item(i)
            if autocast: item = _maybe_cast(item)
            objs.append(item)
        except: pass
    return objs

def last_obj():
    mp = C.mp
    if mp.Count > 0:
        return mp.Item(mp.Count - 1)
    return None

# =================================================================
# 5. 类型与图层选择 (Type & Layer Selection)
# =================================================================

@retry_on_busy(max_retries=5)

def select_tuceng(layer_names, delay=0.5, autocast=True): # delay 参数保留兼容性但不再使用
    """【SEL-TYPE-001】按图层名选择"""
    layers = [layer_names] if isinstance(layer_names, str) else list(layer_names)
    f_data = [layers[0] if len(layers)==1 else layers]
    return ss_select("all", filter_types=[8], filter_data=f_data, autocast=autocast)

def stc(layer_names, **kwargs):
    return select_tuceng(layer_names, **kwargs)

# 以下均为快捷方式，自动继承 ss_select 的重试能力
def select_kuai(autocast=True):
    return ss_select("all", filter_types=[0], filter_data=["INSERT"], autocast=autocast)
def select_text(autocast=True):
    return ss_select("all", filter_types=[0], filter_data=["TEXT"], autocast=autocast)
def select_mtext(autocast=True):
    return ss_select("all", filter_types=[0], filter_data=["MTEXT"], autocast=autocast)
def select_line(autocast=True):
    return ss_select("all", filter_types=[0], filter_data=["LINE"], autocast=autocast)
def select_circle(autocast=True):
    return ss_select("all", filter_types=[0], filter_data=["CIRCLE"], autocast=autocast)
def select_ellipse(autocast=True):
    return ss_select("all", filter_types=[0], filter_data=["ELLIPSE"], autocast=autocast)
def select_spline(autocast=True):
    return ss_select("all", filter_types=[0], filter_data=["SPLINE"], autocast=autocast)
def select_polyline(autocast=True):
    return ss_select("all", filter_types=[0], filter_data=["LWPOLYLINE"], autocast=autocast)
def select_polyline_chuantong(autocast=True):
    return ss_select("all", filter_types=[0], filter_data=["POLYLINE"], autocast=autocast)

def select_all_texts_mixed(target_space="Model"):
    try:
        raw = ss_select("all", filter_types=[0], filter_data=["*TEXT,TDB*"], autocast=True)
    except:
        raw = ss_select("all", autocast=True)
    target_names = {"AcDbText", "AcDbMText", "TDbText", "TDbMText"}
    return [obj for obj in raw if getattr(obj, "ObjectName", "") in target_names]

def select_pub_text_entities():
    ents = select_tuceng("PUB_TEXT", autocast=False)
    tdb_t, tdb_m = [], []
    for e in ents:
        name = getattr(e, "ObjectName", "")
        if name == "TDbText": tdb_t.append(e)
        elif name == "TDbMText": tdb_m.append(e)
    return tdb_t, tdb_m

@retry_on_busy
@current_space_only
def select_group_entities(group_obj):
    doc = C.doc
    try:
        handles = [e.Handle for e in group_obj]
        objs = []
        for h in handles:
            try: objs.append(doc.HandleToObject(h))
            except: pass
        if objs:
            yin_to_xian_xuanze(objs)
            return True
    except Exception as e:
        print(f"[错误] 组选择失败: {e}")
    return False

# =================================================================
# 6. 可视化与交互 (Visualization)
# =================================================================

@retry_on_busy
def yin_to_xian_xuanze(LB, wait_s=0.6):
    """【VIS-001】隐转显 (Delete/Undo法)"""
    doc = C.doc
    doc.StartUndoMark()
    try:
        for x in LB:
            # SafeCOM.call(x.Delete) # 这里也可以用 SafeCOM 保护
            try: x.Delete()
            except: pass
        doc.SendCommand("_U\n\n")
        time.sleep(wait_s)
        doc.SendCommand("_.SELECT\nP\n\n")
    finally:
        doc.EndUndoMark()

@retry_on_busy
def yin_to_xian_safe(LB, wait_s=0.1):
    """【VIS-002】隐转显 (LISP sssetfirst法)"""
    if not LB: return
    # 使用 raw_doc 避免 SendCommand 同步等待导致命令链阻塞
    try:
        doc = C.raw_doc if hasattr(C, 'raw_doc') and C.raw_doc else C.doc
    except Exception:
        doc = C.doc
    handles = [obj.Handle for obj in LB if getattr(obj, 'Handle', None)]
    if not handles: return

    lisp_var = f"ss_temp_{random.randint(1000, 9999)}"
    doc.SendCommand(f"(setq {lisp_var} (ssadd))\n")
    
    batch, buf = 20, ""
    for i, h in enumerate(handles):
        buf += f'(ssadd (handent "{h}") {lisp_var}) '
        if (i+1) % batch == 0:
            doc.SendCommand(buf + "\n"); buf = ""
    if buf: doc.SendCommand(buf + "\n")

    doc.SendCommand(f"(sssetfirst nil {lisp_var})\n")
    doc.SendCommand(f"(setq {lisp_var} nil)\n")
    if wait_s: time.sleep(wait_s)

def xian_to_yin_pickfirst(clear_grips=True, autocast=True):
    try:
        doc = C.doc
        ss = doc.PickfirstSelectionSet
        # 使用 SafeCOM 提取，防止 Pickfirst 刚好被用户操作打断
        items = SafeCOM.list_selection(ss)
        if autocast: items = [_maybe_cast(e) for e in items]
        if clear_grips: doc.SendCommand("(sssetfirst nil nil)\n")
        return items
    except: return []

def select_entities_in_window(x1, y1, x2, y2, ty=1.0, select_mode="_W"):
    doc = C.doc
    (x_lo, y_lo), (x_hi, y_hi) = normalize_rect(x1, y1, x2, y2)
    
    try: doc.PickfirstSelectionSet.Clear()
    except: pass

    buf = 0.2 * ((x_hi-x_lo) + (y_hi-y_lo))/2
    doc.SendCommand(f"_.ZOOM\n_W\n{x_lo-buf},{y_lo-buf}\n{x_hi+buf},{y_hi+buf}\n")
    time.sleep(ty)
    doc.SendCommand(f"_.SELECT\n{select_mode}\n{x_lo},{y_lo}\n{x_hi},{y_hi}\n\n")
    time.sleep(ty/2)
    
    # 同样使用 SafeCOM 提取结果
    return SafeCOM.list_selection(doc.PickfirstSelectionSet)

def highlight_entities_in_window(x1, y1, x2, y2):
    select_entities_in_window(x1, y1, x2, y2)

def highlight_entity_by_bbox(entity):
    try:
        p1, p2 = entity.GetBoundingBox()
        (x1, y1), (x2, y2) = expand_rectangle(p1, p2, 0)
        offset = 130 if getattr(entity, "ObjectName", "") == "TDbWall" else 0
        (x1, y1), (x2, y2) = expand_rectangle((x1, y1), (x2, y2), offset)
        highlight_entities_in_window(x1, y1, x2, y2)
    except Exception as e:
        print(f"Highlight Error: {e}")

def set_entity_grip_state_precise(ent):
    if not ent: return
    doc = C.doc
    try:
        doc.SendCommand("(sssetfirst nil nil)\n")
        time.sleep(0.1)
        doc.SendCommand(f'(sssetfirst nil (ssadd (handent "{ent.Handle}") (ssadd)))\n')
        return ent
    except: pass

def isolate_modelspace_area(x1, y1, x2, y2):
    doc = C.doc
    LB = select_objects_in_window_area(x1, y1, x2, y2)
    if LB:
        yin_to_xian_xuanze(LB)
        time.sleep(0.4)
        doc.SendCommand("_.IsolateObjects\n")

@retry_on_busy
def unhide_all(space=None, filter_names=None, highlight=False):
    target = space if space else C.msp
    revealed = []
    
    # 优化：一次性取出所有对象，避免反复 RPC
    # 注意：如果空间对象非常多(>5万)，这里可能会卡一下，但比反复Item(i)快得多
    all_objs = SafeCOM.list_selection(target)

    for obj in all_objs:
        try:
            if not getattr(obj, "Visible", True):
                name = getattr(obj, "ObjectName", "")
                if filter_names is None or name in filter_names:
                    # 赋值操作，使用 SafeCOM.call 保护更佳
                    SafeCOM.call(setattr, obj, 'Visible', True)
                    
                    if highlight: 
                        try: obj.Highlight(True)
                        except: pass
                    revealed.append(_maybe_cast(obj))
        except: pass
    return revealed

# =================================================================
# 7. 属性与天正支持 (Properties & TArch)
# =================================================================
# (这部分大字典保持不变，节省篇幅，请保留你原来的 _TARCH_PROPERTY_MAP)
_TARCH_PROPERTY_MAP = {
    # ……原来的……
    'TDbOpening': {
        'Offset': 1, 'Width': 2, 'Type': 3, 'Direction': 7,
        'Angle': 8, 'Height': 10, 'Name': 11
    },
    'TDbWall': {
        'Offset1': 1, 'Thickness': 2, 'Thickness2': 3, 'Length': 4,
        'WallType': 11, 'Material': 13, 'Hatch': 21, 'Surface': 22
    },

    # 单行天正文字
    'TDbText': {
        'Height':      1,   # '3.5' → 高度
        'Justify':     2,   # '左下(BL)'
        'Rotation':    3,   # 0.0 度
        'TextStyle':   4,   # 'Standard'
        'Text':        5,   # '天正单行文字...'
        'Oblique':     6,   # 0.0 度（斜体角）
        # 'BigFont':   29,  # '无'，暂时不用
        'SomeSize':    30,  # 100.0，暂时占位
        'Flag40':      40,  # '是'/'否' 之类的开关
        'WidthFactor': 41,  # '1' → 宽度因子
        'Flag42':      42,  # 另一开关
    },

    # 多行天正文字（TDbMText）
    'TDbMText': {
        'Height':          1,   # '3.5'
        'Justify':         2,   # '左对齐'
        'Rotation':        3,   # 0.0 度
        'TextStyle':       4,   # 'Standard'
        'Width':           5,   # '200.0' — MText 框宽
        'LineSpacing':     6,   # '0.40' — 行距系数（猜测）
        'Oblique':         7,   # 0.0 度（可能是倾斜/其他角度）
        # 'BigFont':       29,  # '无'
        'SomeSize':        30,  # 100.0
        # 内容 Text / TextString 暂时没看到对应 DISPID，先不写
    },


    'TDbSpace': {
            # --- 基本信息 ---
            'Name':          1,   # 房间名称，如 '房间'
            'Number':        2,   # 房间编号，如 '1002'
            'Area':          3,   # 房间面积，字符串形式的数值 '53.212'

            # 4–9 这几个是面积/周长/投影等各类几何参数，语义不够确定，先挂上通用名字
            'Param4':        4,
            'Param5':        5,
            'Param6':        6,
            'Param7':        7,
            'Param8':        8,
            'Param9':        9,

            # --- 高度/几何 ---
            'RoomHeight':   10,   # 3000.0  房间高度/楼层高度（需你实测确认）
            'Perimeter1':   11,   # 与 12 数值相同，很可能是周长类参数
            'Perimeter2':   12,

            # --- 标注/显示控制 ---
            'ShowName':     13,   # '是'/'否'  是否显示名称
            'NameTextMode': 14,   # '单行名称' 等
            'RoomCode':     15,   # 'ROOM'（房间类型代码）
            'Flag16':       16,   # '否'
            'UserText':     17,   # 预留的说明文字（目前为空）
            'BoundaryRef':  18,   # IDispatch：房间外轮廓对象引用
            'ScaleText':    19,   # '100'  标注比例/比例因子
            'AngleBase':    20,   # '0' 基准角度

            'HasSomething': 21,   # '有'  某类附加信息存在与否
            'StyleName':    22,   # '_TCH_SPACE' 空间样式名
            'TextOffset':   23,   # 5.0  文字相对房间几何的偏移
            'Angle24':      24,
            'TextRotation': 25,   # 120.0  文字方向
            'Angle26':      26,
            'Angle27':      27,
            'Flag28':       28,   # '否'
            'BigFont':      29,   # '无'
            'SizeParam':    30,   # 100.0

            'AreaLabelText':31,   # '房间面积'  标注文字内容
            'RoomHeight2':  32,   # 3000.0  与 10 一致，多半是同义字段
            'ShowAreaText': 33,   # '是'

            'StyleName2':   42,   # '_TCH_SPACE'
            'TextHeight':   43,   # 3.5  房间文字高度

            # --- 其它设置（100+） ---
            'Default100':   100,  # ' (缺省)'
            'Default101':   101,  # ' (缺省)'
            'FloorType':    102,  # '接地楼板'
            'Param103':     103,
            'Note':         104,
            'Param105':     105,
            'Param106':     106,
            'Scope':        107,  # '全部'  作用范围
            'HatchName':    108,  # 'SPACE_HATCH' 填充样式名
            'HatchOn':      109,  # '是' 是否填充
            'ControlMode':  110,  # '全局控制'
            'OverrideLocal':111,  # '否' 是否局部覆盖
            'HasHatch':     112,  # '有'
            'Param113':     113,
        
   

    },

   "TDbDrawingName": {
        # 基本图名
        "图名文字": 1,          # 例如 "一层平面图"^C42^C~^C1^C轴立面图文字加圆圈
        "图名样式": 2,          # 文字样式名，如 "Standard"
        "图名高度": 3,          # 文字高度

        # 比例相关
        "比例文字": 4,          # 例如 "1:100"
        "比例样式": 5,          # 比例文字样式
        "比例高度": 6,          # 比例文字高度

        # 版式 / 标注样式
        "间距系数": 8,          # 0.60
        "标注样式": 9,          # "传统" / "国标" 等

        # 显示控制
        "显示比例": 10,         # "是"/"否"（有的版本会是真布尔）

        # 其它参数（按需使用）
        "布局转角": 11,           # 几何偏移/基线距离，当前看到是 0.0
        "颜色索引": 12,     # 颜色索引/枚举值
        "前缀文字": 29,         # "无" 等附加字段
        "比例数值": 30,         # 100.0 等数值形式
    },
    
}

_ATTR_CASE_CACHE = {}

def _resolve_attr_case_insensitive(obj, attr_name):
    if hasattr(obj, attr_name): return attr_name
    pascal_name = attr_name[0].upper() + attr_name[1:]
    if hasattr(obj, pascal_name): return pascal_name

    try:
        type_name = obj.ObjectName
    except:
        type_name = str(type(obj))
        
    cache_key = f"{type_name}.{attr_name.lower()}"
    if cache_key in _ATTR_CASE_CACHE: return _ATTR_CASE_CACHE[cache_key]

    try:
        all_attrs = dir(obj) 
        target_lower = attr_name.lower()
        for real_name in all_attrs:
            if real_name.lower() == target_lower:
                _ATTR_CASE_CACHE[cache_key] = real_name
                return real_name
    except Exception: pass
    return None

#&&% 20261014
def get_attr(obj, name, default=None):
    """
    【修正版】安全获取对象属性 (支持默认值)
    解决: get_attr() takes 2 positional arguments but 3 were given
    """
    if obj is None: 
        return default
        
    try:
        # 1. 尝试获取 ObjectName 用于判断是否为天正对象
        # 注意：这里调用原生 getattr 防止死循环
        obj_name = getattr(obj, "ObjectName", "")
        
        # --- A. 天正对象 (TArch) 处理 ---
        if obj_name in _TARCH_PROPERTY_MAP:
            mapping = _TARCH_PROPERTY_MAP[obj_name]
            # 尝试直接匹配或忽略大小写匹配
            dispid = mapping.get(name) or mapping.get(name.lower())
            
            if dispid:
                # 通过 IDispatch 接口直接调用
                return obj._oleobj_.Invoke(dispid, 0, pythoncom.DISPATCH_PROPERTYGET, True)
        
        # --- B. 标准 COM 对象处理 ---
        real_obj = _maybe_cast(obj)
        real_name = _resolve_attr_case_insensitive(real_obj, name)
        
        if real_name:
            return getattr(real_obj, real_name)
            
    except Exception:
        pass
        
    # 如果都获取不到，返回默认值
    return default




def set_attr(obj, name, value):
    if obj is None: return False
    try:
        obj_name = getattr(obj, "ObjectName", "")
        if obj_name in _TARCH_PROPERTY_MAP:
            mapping = _TARCH_PROPERTY_MAP[obj_name]
            dispid = mapping.get(name) or mapping.get(name.lower())
            if dispid:
                obj._oleobj_.Invoke(dispid, 0, pythoncom.DISPATCH_PROPERTYPUT, True, value)
                return True
        
        real_obj = _maybe_cast(obj)
        real_name = _resolve_attr_case_insensitive(real_obj, name)
        if real_name:
            # 属性赋值，建议使用 SafeCOM 保护，因为设置属性最容易触发“正在执行命令”的错误
            SafeCOM.call(setattr, real_obj, real_name, value)
            return True
    except: pass
    return False

# 兼容旧代码接口
def get_object_property(obj, property_name): return get_attr(obj, property_name)
def set_object_property(obj, property_name, value): return set_attr(obj, property_name, value)

def brute_dump_tarch_props(ent, max_dispid=64, *, echo=True):
    """
    Brutally scan a TArch entity's DISPIDs and return readable hits.

    Use this as a diagnostic fallback when normal property mapping is missing or
    a TArch object refuses regular get/set access.
    """
    rows = []
    ole = getattr(ent, "_oleobj_", None)
    if ole is None:
        return rows

    object_name = getattr(ent, "ObjectName", "?")
    if echo:
        print(f"Scanning {object_name}...")

    for i in range(1, max_dispid + 1):
        try:
            val = ole.Invoke(i, 0, pythoncom.DISPATCH_PROPERTYGET, True)
        except Exception:
            continue
        if val is None:
            continue
        row = {
            "object_name": object_name,
            "dispid": i,
            "value": val,
            "value_type": type(val).__name__,
        }
        rows.append(row)
        if echo:
            print(f"ID {i:2d}: {val} ({type(val).__name__})")
    return rows

if __name__ == '__main__':
    print("CAD Selection Library Loaded.")


