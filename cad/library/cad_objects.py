#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第四部分 一般对象
一般对象操作函数

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
from system.CAD_com_utils import sys_logger, alias, retry_on_busy, SafeCOM
from system.common_logger import checkpoint

# 获取常用对象
acad = C.acad
doc = C.doc
mp = C.mp
sp = C.sp

#&&&&%% 第四部分 一般对象


def ensure_list(input_data):
    """
    【通用工具】将输入参数统一转换为列表。
    
    增强功能：
    - 自动解包：如果输入是元组且第一个元素是列表（例如 (polylist, dict, ...)），
      则自动提取第一个元素返回，消除数据结构混乱。
    - 兼容 COM：支持 SelectionSet 等 COM 集合。
    """
    # 1. 处理 None
    if input_data is None:
        return []

    # 定义检测是否为“列表类”的内部函数 (List, Tuple, COM Collection)
    def is_list_like(obj):
        if isinstance(obj, (list, tuple)):
            return True
        # 针对 COM 集合 (有 Count 但没有 ObjectName)
        if hasattr(obj, "Count") and not hasattr(obj, "ObjectName"):
            return True
        return False

    # 2. 判断输入本身是否为列表/集合
    if is_list_like(input_data):
        # 先统一转为 Python 列表，方便操作
        try:
            current_list = list(input_data)
        except:
            # 极少数转换失败的情况（如损坏的 COM 对象），作为单对象处理
            return [input_data]

        # 3. 【核心优化】探测嵌套结构并解包
        if len(current_list) > 0:
            first_item = current_list[0]
            
            # 探测条件：第一个元素也是列表类
            if is_list_like(first_item):
                
                # 场景 A: 输入是元组 (Tuple) -> 强烈的“返回值容器”信号
                # 例子: dy = ([line1, line2], {mapping}) -> 解包返回 [line1, line2]
                if isinstance(input_data, tuple):
                    return ensure_list(first_item) # 递归调用以确保内部也被清理
                
                # 场景 B: 包含且仅包含一个列表的列表 -> 可能是多余的包装
                # 例子: [[line1, line2]] -> 解包返回 [line1, line2]
                if len(current_list) == 1:
                    return ensure_list(first_item)
                
                # 场景 C: 混合结构 (List + Dict) -> 可能是 [list, dict]
                # 例子: [[line1], {"info":1}] -> 判定为数据+元数据，解包
                if len(current_list) > 1 and isinstance(current_list[1], dict):
                    return ensure_list(first_item)

        # 4. 如果不符合解包条件（例如是坐标点列表 [[0,0], [10,10]]），则原样返回
        return current_list

    # 5. 默认：单个对象，包裹返回
    return [input_data]






# 按com实体对象中提取的坐标排序

#&&&%  排序
#&&% 元组排序
def sort_tuples(lst,cha_Y =2000):#对列表按插入点xy坐标排序
    
    """
    这是很有用的一个双值排序函数，对于COM对象，可以先将其转换为元组，即可使用这个函数

    它的价值在于，很容易拓展到n值排序
    """
    
    # 先按照m[1]降序排序
    lst.sort(key=lambda x: -x[2][1])

    i = 0
    while i < len(lst) - 1:
        j = i + 1
        # 查找所有m[1]差距在chaY以内的元素
        while j < len(lst) and abs(lst[i][2][1] - lst[j][2][1]) < cha_Y:
            j += 1
        
        # 如果找到了m[1]值相近的元素，根据m[0]值进行排序
        if j - i > 1:
            lst[i:j] = sorted(lst[i:j], key=lambda x: x[2][0])
        
        i = j

    return lst

#&&% 多维容差排序
def multi_dim_tolerance_sort(lst, key_index=2, tolerances=[10000, 1000, 0]):#高维排序
    """
    对 lst 列表中的元组按多维坐标字段排序，考虑每个维度的容差进行逐层排序。

    参数：
        lst: [(id, name, (x, y, z)), ...]
        key_index: 坐标在元组中的索引（默认是第3项，即元组[2]）
        tolerances: 每个维度允许的容差，例如 [Z差, Y差, X差]

    返回：
        排好序的新列表
    """
    # 最外层排序：按最高维降序排（Z从上往下）
    dim = len(tolerances)
    lst.sort(key=lambda x: -x[key_index][0])  # Z 倒序

    def recursive_sort(sublist, level):
        if level >= dim - 1:
            # 最后一级直接按该维升序
            return sorted(sublist, key=lambda x: x[key_index][level + 1])
        
        i = 0
        while i < len(sublist) - 1:
            j = i + 1
            while j < len(sublist) and abs(sublist[i][key_index][level] - sublist[j][key_index][level]) < tolerances[level]:
                j += 1
            if j - i > 1:
                sublist[i:j] = recursive_sort(sublist[i:j], level + 1)
            i = j
        return sublist

    return recursive_sort(lst, 0)


def get_ll_pt(ent):#提取函数，对象左下角点
    minpt, _ = ent.GetBoundingBox()
    return minpt[0], minpt[1],0

def get_center(ent):#提取函数，中心点
    minpt, maxpt = ent.GetBoundingBox()
    return ((minpt[0]+maxpt[0])/2, (minpt[1]+maxpt[1])/2)

#&&% 实体位置排序
def sort_entities_by_position( entity_list, extract_func, cha_Y=2000):#对com对象按提取坐标分别沿y,x方向排序
        """
        对实体列表根据其坐标（通过 extract_func 获取）进行排序：
        - 先按 Y 值降序（从上到下）
        - Y 值接近（差值 < cha_Y）者再按 X 值升序（从左到右）

        参数：
            entity_list: COM 实体对象列表
            extract_func: 提取坐标函数，返回 (x, y) 元组的函数即可
            cha_Y: 同一行判定的 Y 方向容差

        返回：按坐标顺序排列的新实体对象列表

        调用示例

        sorted_objs = sort_entities_by_position(LB, extract_func=get_ll_pt)
        
        """
        triples = [(ent, *extract_func(ent)) for ent in entity_list]

        # 按 Y 值降序排列
        triples.sort(key=lambda t: -t[2])

        i = 0
        while i < len(triples) - 1:
            j = i + 1
            while j < len(triples) and abs(triples[i][2] - triples[j][2]) < cha_Y:
                j += 1
            triples[i:j] = sorted(triples[i:j], key=lambda t: t[1])  # 按 X 升序
            i = j

        return [t[0] for t in triples]

def get_line_start(ent):
    """
    提取一条直线的起点 (x, y)
    ent: AcDbLine 或类似对象，具有 .StartPoint 属性
    """
    pt = ent.StartPoint   # 假设是一个 (x, y, z) 或 [x, y, z]
    return pt[0], pt[1]

#&&% * 对列表实体进行从上到下、从左到右的排序

#&&% 左下角排序
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
    while i < len(wrapped) - 1:
        j = i + 1
        while j < len(wrapped) and abs(wrapped[i][2] - wrapped[j][2]) < cha_Y:
            j += 1
        # 行内再按 x 升序
        if j - i > 1:
            wrapped[i:j] = sorted(wrapped[i:j], key=lambda t: t[1])
        i = j

    return [ent for ent, _, _ in wrapped]




#&&% 右上角排序
def sort_coms_by_rbcorner(com_list, *, cha_X=100):
    """
    竖向图框（或已整体旋转 -90° 的图纸）使用 ——  
    · 先按列：x₁ 降序（右 → 左）  
    · 列内：  y₂ 降序（上 → 下）

    参数
    ----
    com_list : list[COM object]
        文字实体列表
    cha_X    : float
        判定“同一列”的容差，单位与图纸坐标一致
    """
    wrapped = []
    for ent in com_list:
        try:
            (x1, _, _), (_, y2, _) = ent.GetBoundingBox()  # x1 = 左, y2 = 上
        except Exception:
            x1 = y2 = float("-inf")                        # 失败的排最后
        wrapped.append((ent, x1, y2))

    # — ① 按 x₁ 降序：最右列在前 —
    wrapped.sort(key=lambda t: -t[1])

    # — ② 同列内再按 y₂ 降序：上 → 下 —
    i = 0
    while i < len(wrapped) - 1:
        j = i + 1
        while j < len(wrapped) and abs(wrapped[i][1] - wrapped[j][1]) < cha_X:
            j += 1
        wrapped[i:j] = sorted(wrapped[i:j], key=lambda t: -t[2])
        i = j

    return [t[0] for t in wrapped]


#&&% 自定义左下角排序
def sort_coms_by_llcorner_custom(objs, tol_x=100):
    """
    按左下角 x, y 坐标对 COM 对象列表 objs 排序：
      1. 先按 x 升序分组：相邻 x 差 ≤ tol_x 视为同一组
      2. 每组内按 y 降序排列（y 大的排前）
      3. 最终把各组按它们的 x 升序依次拼接

    参数
    ----
    objs : List[COMObject]
        要排序的 COM 对象列表，每个对象必须支持 GetBoundingBox()
    tol_x : float
        x 方向上的容差，小于等于此值的 x 差视为同组

    返回
    ----
    List[COMObject]
        排序后的对象列表
    """
    # 提取 (obj, llx, lly)
    items = []
    for e in objs:
        ll, ur = e.GetBoundingBox()
        llx, lly, _ = ll
        items.append((e, llx, lly))

    # 按 x 升序初排
    items.sort(key=lambda t: t[1])

    # 分组：相邻 x 差 ≤ tol_x 的归一组
    clusters = []
    rep_x, current = items[0][1], [items[0]]
    for item in items[1:]:
        _, x, _ = item
        if abs(x - rep_x) <= tol_x:
            current.append(item)
        else:
            clusters.append((rep_x, current))
            rep_x, current = x, [item]
    clusters.append((rep_x, current))

    # 按组的 x 升序排好后，组内按 y 降序，再平铺
    result = []
    for _, group in sorted(clusters, key=lambda c: c[0]):
        group_sorted = sorted(group, key=lambda t: t[2], reverse=True)
        result.extend([t[0] for t in group_sorted])

    return result


#&&% 中心点排序
def sort_coms_by_center(objs, tol_x=100):
    """
    按外包盒中心坐标对 COM 对象列表 objs 排序：
      1. 先计算每个对象的 bbox 中心 (cx, cy)
      2. 按 cx 升序初排序
      3. 将相邻 cx 差 ≤ tol_x 的对象归同一组
      4. 各组按 cy 降序排列（cy 大的排前）
      5. 最后按组的 cx 升序依次拼接各组内对象

    参数
    ----
    objs : List[COMObject]
        要排序的 COM 对象列表，每个对象必须支持 GetBoundingBox()
    tol_x : float
        x 方向上的容差，小于等于此值的 cx 差视为同组

    返回
    ----
    List[COMObject]
        排序后的对象列表
    """
    # 1. 提取 (obj, cx, cy)
    items = []
    for e in objs:
        ll, ur = e.GetBoundingBox()
        cx = (ll[0] + ur[0]) / 2.0
        cy = (ll[1] + ur[1]) / 2.0
        items.append((e, cx, cy))

    if not items:
        return []

    # 2. 按 cx 升序初排
    items.sort(key=lambda t: t[1])

    # 3. 分组：相邻 cx 差 ≤ tol_x 的归一组
    clusters = []
    rep_x, current = items[0][1], [items[0]]
    for item in items[1:]:
        _, x, _ = item
        if abs(x - rep_x) <= tol_x:
            current.append(item)
        else:
            clusters.append((rep_x, current))
            rep_x, current = x, [item]
    clusters.append((rep_x, current))

    # 4. 各组内部按 cy 降序排列，再平铺
    result = []
    for rep_x, group in sorted(clusters, key=lambda c: c[0]):
        group_sorted = sorted(group, key=lambda t: t[2], reverse=True)
        result.extend([t[0] for t in group_sorted])

    return result


##对列表实体进行正序或逆序编号

#&&% 实体编号
def number_entities_by_order(entity_list, prefix="", start=1, k=0):
    """
    对排序好的 COM 实体对象列表进行编号。

    参数：
        entity_list: 实体对象列表
        prefix: 编号前缀，默认为空字符串
        start: 编号起始数值，默认为 1
        k: 排序方向控制变量：
            - k = 0 正序编号
            - k = 1 逆序编号

    返回：
        编号字符串列表（如 ["1", "2", "3"] 或 ["图1", "图2", "图3"]）
    """
    n = len(entity_list)
    index_list = range(n) if k == 0 else reversed(range(n))
    
    result = []
    for i, idx in enumerate(index_list):
        label = f"{prefix}{start + i}"
        result.append(label)
    
    return result


# 重复操作列表对象
#&&&% 列表处理

#&&% 列表遍历操作

def pr_list(P: list, f, *args, **kwargs):
    """
    args:  位置参数元组 (例如: 10, 20)
    kwargs: 关键字参数字典 (例如: layer="Wall", color=1)
    """
    results = []
    sys_logger.info(f"开始处理 {len(P)} 个对象...")
    
    for i, item in enumerate(P):
        try:
            # 关键点：将接收到的 item 和额外参数一起传给 f
            # item 是列表里的元素，args/kwargs 是你传入的固定参数
            res = f(item, *args, **kwargs)
            results.append(res)
        except Exception as e:
            sys_logger.info(f"❌ 第 {i} 个出错: {e}")
            results.append(None)
            
    return results





#&&% 列表提取操作
def apply_to_each2(obj_list, extract_func, action_func):#双层嵌套重复操作列表对象
    """
    对 obj_list 中的每个对象，先通过 extract_func 提取值，
    再将该值传入 action_func 中处理。

    参数：
        obj_list: 对象列表
        extract_func: 用于提取 (x, y) 或其他值的函数
        action_func: 用于处理提取结果的函数（如 srhd）
    """
    for obj in obj_list:
        value = extract_func(obj)
        action_func(value)

#&&&% 组
"""

创建组
group = doc.Groups.Add("mygroup")
LB=pmxz()
请在屏幕拾取图元，以Enter键结束

group.AppendItems(vtobj([LB[0], LB[1], LB[2]]))


从组名获取组合组中对象

group = doc.Groups.Item("G001")

entities = [group.Item(i) for i in range(group.Count)]  # 遍历组内对象

entities[0].Handle
'2C3'

entities[0].Move(vtpnt(0,0,0),vtpnt(0,10000,0))


解除组
group.Delete()


group1 = doc.Groups.Add("mygroup")
group1.AppendItems(vtobj([LB[0], LB[1], LB[2]]))
group2 = doc.Groups.Add("mygroupA")
group2.AppendItems(vtobj([LB[3], LB[4], LB[5],LB[6]]))
group3 = doc.Groups.Add("mygroupB")
group3.AppendItems(vtobj([group1,group2]))非法操作
group3.AppendItems(vtobj([LB[0],LB[1],LB[2],LB[3], LB[4], LB[5],LB[6]]))


# 提取 group1 和 group2 的所有成员
group1_entities = [group1.Item(i) for i in range(group1.Count)]
group2_entities = [group2.Item(i) for i in range(group2.Count)]

# 合并成新的列表
all_entities = group1_entities + group2_entities

# 创建 group3
group3 = doc.Groups.Add("mygroupB")
group3.AppendItems(vtobj(all_entities))

 get_boundingbox_from_objects(objs)
"""

# 建立全部列表com对象的最小边界框
#&&&% 边界框

#&&% 获取对象群包围盒
def get_boundingbox_from_objects(objs):#从列表com对象建立最小边界框
    """
    从一组图形对象（如 LB）中获取整体包围盒
    返回值：(min_x, min_y, min_z), (max_x, max_y, max_z)
    """
    min_point, max_point = None, None

    for obj in objs:
        try:
            min_pt, max_pt = obj.GetBoundingBox()
            if min_point is None:
                min_point, max_point = list(min_pt), list(max_pt)
            else:
                min_point = [min(min_point[i], min_pt[i]) for i in range(3)]
                max_point = [max(max_point[i], max_pt[i]) for i in range(3)]
        except Exception as e:
            sys_logger.info(f"跳过无法获取边界的对象: {obj.ObjectName}")
            continue

    return tuple(min_point), tuple(max_point)
        

# 建立组的最小边界框

#&&% 创建组
def chuangjian_zu(group_name):

    group = doc.Groups.Add(group_name)

    return group

#&&% 获取组对象
def nametogroup(group_name):#从组名获取实体com组对象
    group_obj = doc.Groups.Item(group_name)

    return group_obj

##获取所有组

#&&% 获取所有组名
def get_all_group_names():
    """
    获取当前 DWG 文档中所有组的名称列表。
    
    返回:
      List[str] — 包含所有组名称的列表
    """
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc  = acad.ActiveDocument
    groups = doc.Groups
    return [groups.Item(i).Name for i in range(groups.Count)]

#&&% 获取所有组
def get_all_groups():
    """
    获取当前 DWG 文档中所有组的 COM 对象列表及其名称。
    
    返回:
      List[Tuple[str, COMObject]] — 每项为 (组名称, 组对象)
    """
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc  = acad.ActiveDocument
    groups = doc.Groups
    result = []
    for i in range(groups.Count):
        grp = groups.Item(i)
        result.append((grp.Name, grp))
    return result



#将多个com对象对象加入名为group_name的组
#&&% 添加对象到组
def add_objects_to_group(group_name, obj_list):

    """
    将 obj_list 中的所有图形对象加入名为 group_name 的组中
    如果组已存在，使用原组；否则新建
    返回：Group 对象
    """
    groups = doc.Groups
    try:
        group = groups.Item(group_name)
    except:
        group = groups.Add(group_name)

    group.AppendItems(vtlist(obj_list))
    return group


#将单独com对象对象加入名为group_name的组中

#&&% 添加单对象到组
def add_object_to_group(group_name, obj):
    """
    将单个图形对象 obj 加入名为 group_name 的组中。
    如果组已存在，则使用该组；否则新建一个新组。
    
    参数：
      group_name (str)：组名称
      obj：要加入组的 COM 对象（如多段线、线段、块参照等）
    
    返回：
      COM Group 对象
    """
    groups = doc.Groups
    try:
        # 尝试获取已存在的组
        group = groups.Item(group_name)
    except Exception:
        # 不存在则新建
        group = groups.Add(group_name)
    
    # vtlist 工具将 Python list 转成 VBA 可接受的 SAFEARRAY
    group.AppendItems(vtlist([obj]))
    return group

#将单独com对象对象移出名为group_name的组
#&&% 移除组内对象
def remove_object_from_group(group_name, obj):
    """
    将单个 COM 对象 obj 从名为 group_name 的组中移出。
    如果组不存在或对象不在组中，则会打印错误信息但不抛异常。
    
    参数:
      group_name: 组名（字符串）
      obj:         要移出的 COM 对象
    
    返回:
      如果组存在，返回该 Group 对象；否则返回 None。
    """
    try:
        group = doc.Groups.Item(group_name)
    except Exception:
        sys_logger.info(f"[错误] 组 '{group_name}' 不存在")
        return None

    # 把单个对象包装成长度为1的 COM SafeArray
    variant = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [obj])
    try:
        group.RemoveItems(variant)
        sys_logger.info(f"[OK] 已从组 '{group_name}' 中移除对象 {obj.Handle}")
    except Exception as e:
        sys_logger.info(f"[错误] 从组 '{group_name}' 移除对象失败：{e}")

    return group

#将多个com对象对象移出名为group_name的组
#&&% 批量移除组内对象
def remove_objects_from_group(group_name, obj_list):
    """
    将 obj_list 中的所有图形对象从名为 group_name 的组中移出。
    如果组不存在，会打印提示并返回 None；否则返回该组对象。
    
    :param group_name: 组名称
    :param obj_list: 要移除的 COM 对象列表
    :return: Group 对象 或 None
    """
    groups = doc.Groups
    try:
        group = groups.Item(group_name)
    except Exception:
        sys_logger.info(f"组 '{group_name}' 不存在，无法移除对象。")
        return None

    # 把 Python 列表包装成 VARIANT SafeArray，VT_DISPATCH 表示对象类型
    arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, obj_list)
    try:
        group.RemoveItems(arr)
        sys_logger.info(f"已从组 '{group_name}' 中移除 {len(obj_list)} 个对象。")
    except Exception as e:
        sys_logger.info(f"移除对象时发生错误：{e}")
    return group



#&&% 从名为group_name的组获取内部包含的实体对象


#&&% 获取组内实体
def get_com_from_groupname(group_name):
    """
    根据组名获取对应实体列表。
    - 若组不存在、或组中无实体，均返回空列表，不抛异常。
    """

    try:
        group = nametogroup(group_name)
    except Exception:
        # nametogroup 本身失败（组不存在等）
        return []

    if not group:
        # group 为 None 或空，也直接返回空列表
        return []

    entities = [group.Item(i) for i in range(group.Count)] #从com组中获取全部对象
    
    return entities

#从名为group_name的组返回按类型分类的字典
#&&% 获取组内实体分类
def get_com_from_groupname_by_type(group_name):
    """
    根据组名获取对应实体，并按类型名分类返回。

    :param group_name: 组名称
    :return: dict，键为实体类型名（ObjectName），值为该类型的实体列表
    """
    # nametogroup 是你已有的“组名→Group 对象”函数
    group = nametogroup(group_name)
    if group is None:
        sys_logger.info(f"组 '{group_name}' 不存在")
        return {}

    by_type = {}
    # Group.Count 是实体数量，Item(i) 取出第 i 个实体
    for i in range(group.Count):
        ent = group.Item(i)
        # AutoCAD COM 对象一般有 ObjectName 属性
        typ = getattr(ent, "ObjectName", None) or getattr(ent, "EntityName", "Unknown")
        by_type.setdefault(typ, []).append(ent)

    # 打印一下各类型数量，方便调试
    for typ, lst in by_type.items():
        sys_logger.info(f"  类型 {typ} ：{len(lst)} 个实体")

    return by_type

#从名为group_name的组返回按类型分类的字典，且类型按各自位置提取函数排好序
#&&% 获取组内实体排序
def get_group_entities_sorted(group_name, type_extractors, cha_Y=0.5):
    """
    从组中按类型获取实体，并对指定类型按坐标排序。

    :param group_name: str，组名
    :param type_extractors: dict，{ type_name: extract_func }，
           extract_func(ent) 返回 (x, y) 坐标，用于排序。
    :param cha_Y: float，同一行 Y 方向的容差
    :return: dict，{ type_name: [ent, ...] }，已排序或原序

    对天正单行多行文字可以使用GetBoundingBox获取的左下角点
    
    """
    def get_cadtext_pos(ent):
        # CAD单行、多行文字：Position 属性返回 (x, y, z)
        return float(ent.InsertionPoint[0]), float(ent.InsertionPoint[1])


    # 先按类型获取全部实体
    by_type = get_com_from_groupname_by_type(group_name)
    sorted_by_type = {}

    for typ, ents in by_type.items():
        if typ in type_extractors:
            extract_func = type_extractors[typ]
            # 排序
            sorted_list = sort_entities_by_position(ents, extract_func, cha_Y=cha_Y)
            sorted_by_type[typ] = sorted_list
            sys_logger.info(f"Type '{typ}' sorted with {len(sorted_list)} entities")
        else:
            # 保持原序
            sorted_by_type[typ] = list(ents)
            sys_logger.info(f"Type '{typ}' left unsorted ({len(ents)} entities)")

    return sorted_by_type


#从名为group_name的组返回按类型分类的字典，各类型统一按boundingbox中心排好序


#&&% 组内实体按中心排序
def get_group_entities_sorted_by_type_and_bbox(group_name, cha_Y=0.5):
    """
    将组 group_name 中的实体按类型分类，并对每种类型内部按包围盒中心排序：
      1) 先按 center_y 降序（从上到下）
      2) 同一“行”内（|ΔY|<cha_Y）再按 center_x 升序（从左到右）

    参数：
      group_name: 要操作的组名
      cha_Y: 同一“行”Y 方向容差

    返回：
      一个 dict，key=类型名(ObjectName)，value=排序后的实体列表
    """
    # 1. 取组
    group = nametogroup(group_name)
    ents = [group.Item(i) for i in range(group.Count)]

    # 2. 按类型分组
    by_type = {}
    for ent in ents:
        typ = getattr(ent, "ObjectName", None) or ent.EntityName
        by_type.setdefault(typ, []).append(ent)

    # 3. 辅助：计算包围盒中心点

    # 4. 对每个类型内部排序
    for typ, lst in by_type.items():
        triples = [(e, *bbox_center_2(e)) for e in lst]
        # Y 降序
        triples.sort(key=lambda t: -t[2])
        # 同行内按 X 升序
        i = 0
        while i < len(triples) - 1:
            j = i + 1
            while j < len(triples) and abs(triples[i][2] - triples[j][2]) < cha_Y:
                j += 1
            triples[i:j] = sorted(triples[i:j], key=lambda t: t[1])
            i = j
        # 覆盖原列表
        by_type[typ] = [t[0] for t in triples]

    return by_type


# 获取两个组中共有的实体，按类型分类并按包围盒中心排序
#&&% 共有组实体排序
def common_group_entities_sorted(group_name1, group_name2, cha_Y=0.5):
    """
    获取两个组中共有的实体，按类型分类并按包围盒中心排序。

    参数：
      group_name1, group_name2: 要比较的两个组名
      cha_Y: 同一行判定的 Y 方向容差

    返回：
      dict => key: ObjectName 类型名, value: 排序后的实体列表
    """
    # 1. 取组
    g1 = nametogroup(group_name1)
    g2 = nametogroup(group_name2)

    ents1 = [g1.Item(i) for i in range(g1.Count)]
    ents2 = [g2.Item(i) for i in range(g2.Count)]

    # 2. 建立 handle->entity 映射
    map1 = {e.Handle: e for e in ents1}
    map2 = {e.Handle: e for e in ents2}

    # 3. 找共有的 handles
    common_handles = set(map1.keys()) & set(map2.keys())

    # 4. 收集共有实体（这里取自 map1）
    common_ents = [map1[h] for h in common_handles]

    # 5. 按类型分组
    by_type = {}
    for ent in common_ents:
        typ = getattr(ent, "ObjectName", None) or ent.EntityName
        by_type.setdefault(typ, []).append(ent)

    # 6. 包围盒中心点计算
    def bbox_center(e):
        min_pt, max_pt = e.GetBoundingBox()
        x1, y1, _ = tuple(min_pt)
        x2, y2, _ = tuple(max_pt)
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    # 7. 排序：Y 降序，同一行内(|ΔY|<cha_Y)按 X 升序
    for typ, lst in by_type.items():
        triples = [(e, *bbox_center(e)) for e in lst]
        triples.sort(key=lambda t: -t[2])
        i = 0
        while i < len(triples) - 1:
            j = i + 1
            while j < len(triples) and abs(triples[i][2] - triples[j][2]) < cha_Y:
                j += 1
            triples[i:j] = sorted(triples[i:j], key=lambda t: t[1])
            i = j
        by_type[typ] = [t[0] for t in triples]

    return by_type

#&&% 获取组包围盒
def get_boundingbox_from_group(group):#从com对象group建立最小边界框

    """
    并非组的实际BoundingBOX数据

    """

    entities = [group.Item(i) for i in range(group.Count)] #从组中获取全部对象

    p1,p2 = get_boundingbox_from_objects(entities)

    return p1,p2

#&&% 复制组S1
def copy_group_S1_from_doc1_to_doc2(doc1, doc2, group_name="S1"):#将名为“S1”的组复制到当前桌面上另一个文档
    """
    将 doc1 中名为 group_name 的组复制到 doc2 中，并重新组装组。
    粘贴点为 0,0,0。粘贴后通过 handle 差集识别新对象。

    mp要不断更新

    def refresh_modelspace(doc):
        return doc.ModelSpace
    逻辑更清晰

    直接发送命令复制粘贴或许更好
    """
    from system.CAD_core import set_active_doc

    try:
        # 1. 激活源文档
        set_active_doc(doc1)
        li()

        group = doc.Groups.Item(group_name)
        handles = [ent.Handle for ent in group]
        objs = [ent for ent in mp if ent.Handle in handles]

        yin_to_xian_xuanze(objs)

        doc.SendCommand("_copybase\n0,0,0\n")
        time.sleep(0.5)
        doc.SendCommand("_copyclip\n\n")
        time.sleep(1)

        # 2. 激活目标文档
        set_active_doc(doc2)
        li()
        ms2 = doc.ModelSpace

        # 3. 粘贴前记录已有对象
        pre_map = get_handle_object_map(ms2)

        # 4. 粘贴
        doc.SendCommand("_pasteclip"+chr(13)+"0,0,0"+chr(13)+chr(13))#
        time.sleep(1.5)

        # 5. 粘贴后重新记录对象
        ms2 = doc.ModelSpace
        
        post_map = get_handle_object_map(ms2)

        # 6. 取出新对象（通过 handle 差集）
        new_handles = set(post_map) - set(pre_map)
        new_objs = [post_map[h] for h in new_handles]

        sys_logger.info(f"[OK] 粘贴完成，识别出 {len(new_objs)} 个新图元")

        # 7. 添加这些对象到组中（使用你提供的方法）
        add_objects_to_group(group_name, new_objs)

        sys_logger.info(f"[OK] 成功将粘贴对象加入组 '{group_name}'")

    except Exception as e:
        sys_logger.info(f"[错误] 复制组失败: {e}")

        



#&&&% Handle和Label


"""
Handle身份信息和天正标签Label

与列表和组不同，身份信息的标识使我们可以从字典存储的名称信息精准控制每个对象，而不是总依赖对全部对象的遍历


可以在对象创建时就打上标签，使对象归为某个类

可以在一批对象完成后调整标签

可以临时标记一组标签

可以通过Label给天正对象加标签
q1= doc.ModelSpace.Item(doc.ModelSpace.Count - 1)#自动获取图纸空间之前最后一个绘制的对象


从Handle回溯com对象

doc.HandleToObject('2BD')
q1= doc.ModelSpace.Item(doc.ModelSpace.Count - 1)
q1.Label="A1"
q1= doc.ModelSpace.Item(doc.ModelSpace.Count - 1)
q1.Label="B1"
LB=pmxz()
请在屏幕拾取图元，以Enter键结束
LB[0].Label
'B1'
LB[1].Label
'A1'


"""

# 将列表对象按分类将其handle身份标识存入字典

@alias("h")
#&&% 句柄转对象
def HandleToObject(ZF):#从Handle身份信息值回溯com对象

    """
    对连接在墙上的门窗测试无效

    """

    obj = doc.HandleToObject(ZF)

    return obj


def print_coms_handle(LB):

    LC=[]

    for x in LB:

        LC.append(x.Handle)

    sys_logger.info(f"com对象列表对应的Handle句柄列表：{LC} ")




@alias("H")
#&&% 批量句柄转对象
def handles_to_coms(LB_handles):

    """
    对连接在墙上的门窗测试无效

    """
    LC=[]

    for xx in LB_handles:

        obj = doc.HandleToObject(xx)
        LC.append(obj)

    return LC


#&&% 获取所有句柄
def get_all_handles():#获取所有Handle
    """
    获取当前图纸中所有对象（通常在 ModelSpace）的 Handle 值列表。

    返回：
        handle_list: 所有图元的 Handle 字符串列表
    """
    handle_list = []

    for obj in mp:  # 使用你已经定义好的全局 ModelSpace mp
        try:
            handle_list.append(obj.Handle)
        except:
            continue  # 跳过无 Handle 或异常对象

    sys_logger.info(f"[OK] 已获取 {len(handle_list)} 个对象的 Handle")
    return handle_list

#&&% 查找实体
def find_entity_by_handle(handle_str):#从Handle获取实体（适合包括天正的文件）
    """
    遍历当前图纸所有对象，手动比对 Handle 值，找到指定的实体对象。

    参数：
        handle_str: 目标 Handle（字符串）

    返回：
        对象（若找到），否则 None
    """
    for obj in mp:  # 可扩展：遍历 sp 也行
        try:
            if obj.Handle == handle_str:
                return obj
        except:
            continue

    return None



#&&% 按类型句柄分组
def group_objects_by_type_and_handle(LB):#将列表对象的Handle身份信息分类存入字典返回
    """
    将com对象列表 LB 中的对象按 ObjectName 分类，并存储其 Handle。
    每类按 LB 中出现顺序编号。

    参数：
        LB - AutoCAD 实体对象列表（如 select_objects_in_window_area() 返回）

    返回：
        ZD - dict 格式 {ObjectName: [Handle1, Handle2, ...]}
    """
    ZD = {}  # 初始化字典

    for obj in LB:
        try:
            obj_type = obj.ObjectName
            handle = obj.Handle

            if obj_type not in ZD:
                ZD[obj_type] = []

            ZD[obj_type].append(handle)

        except Exception as e:
            sys_logger.info(f"[警告]️ 跳过对象，原因: {e}")
            continue

    # 输出提示信息
    for obj_type, handles in ZD.items():
        sys_logger.info(f"[OK] {obj_type}: 共 {len(handles)} 个对象")

    return ZD

# 通过名称存储对象信息反回溯对象

#&&% 记录类型句柄
def record_handle_with_type(LB, typename, prefix="OBJ"):#将一批对象的 Handle 存储到结构化的字典中，并记录类型名和编号
    """
    替代 XData 方法：记录对象 Handle、类型名、编号，返回结构化字典。
    """
    ZD = {typename: {}}
    for i, obj in enumerate(LB, start=1):
        try:
            h = obj.Handle
            tag = f"{prefix}_{i:03d}"
            ZD[typename][h] = tag
        except:
            continue
    sys_logger.info(f"[OK] 已记录 {len(ZD[typename])} 个“{typename}”对象（Handle+编号）")
    return ZD

#&&% 转换命名字典
def convert_named_dict(ZD, typename):# 构建编号 → COM 对象 的映射字典
    """
    将 ZD["门"] 的结构由 Handle: 编号 转换为 编号: COM对象
    返回：新的字典 {编号: COM实体}
    """
    doc = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    named_dict = {}

    handle_map = ZD.get(typename, {})
    for handle, name in handle_map.items():
        try:
            obj = doc.HandleToObject(handle)
            named_dict[name] = obj
        except:
            sys_logger.info(f"[警告]️ 无法找到对象（handle={handle}）")
            continue

    return named_dict

#&&% 获取命名对象
def get_named_object(tag, ZD, typename="门"):#从标签获取对象
    named = convert_named_dict(ZD, typename)
    return named.get(tag)



#&&% 绘制固定标签
def draw_tags_on_objects_fixed(named_dict, height=250, offset=(1000, 1000, 0)):#直接将编号文字写在每个图元上，通常居中或偏移一点点
    """
    在每个对象的中心点附近绘制标注文字。
    
    参数:
        named_dict - 如 {"Men_001": <COMObject>, ...}
        height     - 文字高度
        offset     - 偏移量（用于防止文字盖住对象）
    """
    import win32com.client
    import pythoncom

    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    ms = doc.ModelSpace

    for name, obj in named_dict.items():
        try:
            # 使用 GetBoundingBox 获取中心点
            min_pt, max_pt = obj.GetBoundingBox()
            center_pt = (
                (min_pt[0] + max_pt[0]) / 2,
                (min_pt[1] + max_pt[1]) / 2,
                (min_pt[2] + max_pt[2]) / 2
            )

            # 加上偏移量
            label_pt = (
                center_pt[0] + offset[0],
                center_pt[1] + offset[1],
                center_pt[2] + offset[2]
            )

            # 确保插入点是三维点
            pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, label_pt)
            
            # 添加文字
            ms.AddText(name, pt, height)
            sys_logger.info(f"[OK] 已标注对象: {name}")

        except Exception as e:
            sys_logger.info(f"[警告]️ 标注失败: {name}, 错误: {e}")

# 给天正对象打上标签存入字典，用于以名称反向回溯操作

#&&% 标记天正门
def label_tarch_doors(LB1, typename="门", prefix="men"):#给选中的天正门打上标签并存入字典返回，非天正图元没有Label属性
    """
    从对象列表 LB1 中筛选出天正门 (ObjectName == 'TDbOpening')，
    并为其按顺序打上 .Label 标签（如 men001, men002 ...）。

    返回：
        ZD = {typename: {编号: 对象}}
    """
    ZD = {typename: {}}
    LB2 = []

    for obj in LB1:
        try:
            if hasattr(obj, "ObjectName") and obj.ObjectName == "TDbOpening":
                LB2.append(obj)
        except:
            continue

    for i, obj in enumerate(LB2, start=1):
        try:
            tag = f"{prefix}{i:03d}"
            obj.Label = tag
            ZD[typename][tag] = obj
            sys_logger.info(f"[OK] 已标记: {tag}")
        except Exception as e:
            sys_logger.info(f"[警告]️ 设置标签失败：{e}")

    sys_logger.info(f"\n📦 共找到并标注 {len(LB2)} 个天正门")
    return ZD




# 获取模型空间上的Handle


"""
target_handles = ['5F', '60', '61']
map = get_handle_object_map(doc.ModelSpace)
objs = [map[h] for h in target_handles if h in map]
这比每次都遍历 ModelSpace 快得多，尤其是大图纸中上千个图元时。

"""

#&&% 获取句柄映射
def get_handle_object_map(ms):
    """返回 {handle: object} 映射"""
    return {ent.Handle: ent for ent in ms}



#&&% XData

"""

在 RegAppTable 中注册,在第一次给图元附加 XData 时，AutoCAD 内部会检查 RegAppTable（注册应用程序表）中是否已经存在 “TestApp” 这个名称。

如果不存在，AutoCAD 会自动往 RegAppTable 里插入一条记录，把 “TestApp” 注册进去。

如果你希望手动控制，也可以先调用 doc.Application.RegistryModes.Add("TestApp")（或使用 AutoLISP：(regapp "TestApp")）

app_name    = "TestApp"            # 自定义的应用程序名
data_types  = [1000, 1040, 1070]
data_values = ["示例文字", 3.14159, 12345]
set_xdata(lineObj, app_name, data_types, data_values)
types_out, data_out = get_xdata(lineObj, app_name)
types_out
[1001, 1000, 1040, 1070]
data_out
['TestApp', '示例文字', 3.14159, 12345]


"""
#&&% 设置扩展数据
def set_xdata(
    com_obj,
    app_name: str,
    data_types: list[int],
    data_values: list,
):
    """
    向任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）附加 XData。

    参数：
      com_obj        -- 任意支持 SetXData() 方法的 COM 对象
      app_name       -- 注册过的应用程序名（字符串）；第一个 DataType 一定是 1001，对应的第一个 Data 存放此 app_name
      data_types     -- 后续的 DataType 列表（不含第一项 1001）；例如 [1000, 1040, 1070] 等
      data_values    -- 与 data_types 对应的数据值列表；长度与 data_types 一一对应。例如 ["文字串", 3.14, 42]

    说明：
      AutoCAD 规定 XData 的第一对元素必须是 (1001, 应用程序名)。后面才是按顺序出现的其他 (DataType, Data)。
      因此实际发送给 SetXData 的 DataType 数组第一个元素要放 1001，Data 数组第一个元素要放 app_name。
    """
    def vtint(val):
        """
        将 Python 列表转换为 VARIANT 类型的整数数组，
        以便传给 COM 对象作为 XData 的 DataType。
        """
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I2, val)

    def vtvariant(var):
        """
        将 Python 列表转换为 VARIANT 类型的 VARIANT 数组，
        以便传给 COM 对象作为 XData 的 Data。
        """
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, var)


    # 1. 拼接完整的 DataType 列表：第一个为 1001
    full_types = [1001] + data_types

    # 2. 拼接完整的 Data 列表：第一个为 app_name
    full_data = [app_name] + data_values

    # 3. 将 Python 列表转换为 VARIANT 数组
    vt_types = vtint(full_types)
    vt_data  = vtvariant(full_data)

    # 4. 调用 COM 的 SetXData 方法
    com_obj.SetXData(vt_types, vt_data)

#&&% 获取扩展数据
def get_xdata(
    com_obj,
    app_name: str,
):
    """
    从任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）读取 XData。

    参数：
      com_obj   -- 任意支持 GetXData() 方法的 COM 对象
      app_name  -- 申请读取的应用程序名（必须与 set_xdata 时使用的相同）

    返回：
      (type_codes, data_values) 二元组，其中
        type_codes: Python 列表，对应每个 XData 项目的 DataType（包括第一项 1001）
        data_values: Python 列表，对应每个 XData 项目的 Data（包括第一项 app_name）
    
    如果该对象没有附加此 app_name 下的 XData，则 GetXData 会抛出错误；建议调用前先用 Error Handling 包裹或
    通过 com_obj.GetXData(app_name) 进行捕获并返回 None。
    """
    def vtint(val):
        """
        将 Python 列表转换为 VARIANT 类型的整数数组，
        以便传给 COM 对象作为 XData 的 DataType。
        """
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I2, val)

    def vtvariant(var):
        """
        将 Python 列表转换为 VARIANT 类型的 VARIANT 数组，
        以便传给 COM 对象作为 XData 的 Data。
        """
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, var)


    try:
        type_codes, data_values = com_obj.GetXData(app_name)
        # 注意：返回的 type_codes 和 data_values 都是 tuple，转换为 list 更易处理
        return list(type_codes), list(data_values)
    except pythoncom.com_error:
        # 对象上不存在该 app_name 的 XData，或读取失败
        return None, None


#&&% Xdata标记

#&&% 设置打印标记
def set_xdata_tab(entitycom):

    app_name    = "PrintApp"
    data_types  = [1000]
    data_values = ["增补目录模板"]
    set_xdata(entitycom, app_name, data_types, data_values)

    return

#&&% 检查打印标记
def is_printApp_xdata_com(entitycom):

    try:

        get_xdata( entitycom, "PrintApp")

        return True

    except:

        return  False

#&&&% 文字

#&&% 写CAD单行文字

def write_cad_text(
    p=(0, 0, 0),
    text="单行文字",
    alignment="左下",
    height=350,
    width_factor=1.0,
    rotation=0.0,
    oblique=0.0,
    style="Standard",
    layer=None
):

    """
    【架构适配版】在指定位置写入 CAD 单行文字。

    """
   

    # =========================================================================
    # 1. 架构接入：获取环境
    # =========================================================================
    # 不再自己去 GetActiveObject，而是请求 CAD_basic 刷新环境
    if not C.li():
        print("[错误] 无法连接 CAD 或无激活文档，write_cad_text 中止。")
        return None


    ms = C.mp 

    # =========================================================================
    # 2. 内部辅助函数 (保持不变，逻辑很棒)
    # =========================================================================
    def local_set_attr(obj, name, value):
        try:
            setattr(obj, name, value)
        except Exception as e:
            # sys_logger.info(f"[警告] 属性 {name} 设置忽略") 
            pass

    def _align_text_dynamic(text_ent, target_pt, align_mode):
        try:
            # 强制刷新，确保 GetBoundingBox 能拿到真实尺寸
            text_ent.Update()
            
            # 获取包围盒 (MinPt, MaxPt)
            bbox = text_ent.GetBoundingBox()
            if not bbox: return
            
            min_pt, max_pt = bbox
            xmin, ymin, zmin = min_pt
            xmax, ymax, zmax = max_pt
            
            # 解析对齐模式，计算文字目前的“锚点”位置
            alg = str(align_mode).strip().lower()
            if alg in ("左下", "lb"):
                anchor = (xmin, ymin, zmin)
            elif alg in ("左上", "lt"):
                anchor = (xmin, ymax, zmin)
            elif alg in ("右下", "rb"):
                anchor = (xmax, ymin, zmin)
            elif alg in ("右上", "rt"):
                anchor = (xmax, ymax, zmin)
            elif alg in ("中心", "居中", "center", "c"):
                anchor = ((xmin + xmax)/2.0, (ymin + ymax)/2.0, (zmin + zmax)/2.0)
            else:
                return # 默认对齐（左下）不需要移动

            # 准备目标点 (Z轴补全)
            if len(target_pt) == 2:
                tp = (float(target_pt[0]), float(target_pt[1]), float(zmin))
            else:
                tp = (float(target_pt[0]), float(target_pt[1]), float(target_pt[2]))

            # 计算移动向量：从 anchor 移到 tp
            # 注意：Move 方法需要 VARIANT 类型的起点和终点
            vt_from = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, anchor)
            vt_to   = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, tp)
            
            text_ent.Move(vt_from, vt_to)
            
        except Exception as e:
            sys_logger.info(f"[警告] 文字对齐运算失败: {e}")

    # =========================================================================
    # 3. 核心执行逻辑
    # =========================================================================
    try:
        # --- 参数准备 ---
        p_list = [float(x) for x in p]
        if len(p_list) == 2: p_list.append(0.0)
        
        # 封装坐标点 (Early Binding 要求)
        insert_pt_variant = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, p_list)
        height_float = float(height)

        # --- 创建对象 ---
        # 使用 cb.mp (ms) 创建
        text_obj = ms.AddText(text, insert_pt_variant, height_float)

        # --- 属性设置 ---
        if style: local_set_attr(text_obj, "StyleName", style)
        if width_factor != 1.0: local_set_attr(text_obj, "ScaleFactor", float(width_factor))
        if rotation != 0.0: local_set_attr(text_obj, "Rotation", math.radians(rotation))
        if oblique != 0.0: local_set_attr(text_obj, "ObliqueAngle", math.radians(oblique))
        if layer: local_set_attr(text_obj, "Layer", layer)

        # --- 执行对齐 ---
        # 只有当需要特殊对齐时才调用移动逻辑
        if alignment and alignment not in ["左下", "lb", None]:
             _align_text_dynamic(text_obj, p_list, alignment)

        return text_obj

    except pythoncom.com_error as e:
        sys_logger.info(f"[COM 错误] WriteCadText 失败 (HR={e.hresult}): {e}")
        return None
    except Exception as e:
        sys_logger.info(f"[通用错误] WriteCadText 失败: {e}")
        return None



#&&% 写天正单行文字
def write_tianzheng_text(
    p=(0, 0, 0),
    text="天正单行文字tianzhengdanhangwenzi",
    alignment="左下",            # "左下"/"左对齐"/"左上"/"右下"/"右上"/"中心"/"center"
    height=3.5,
    width_factor=1.0,
    rotation=0.0,
    oblique=0.0,
    style="Standard",
    system_layer="xitong_tianzhengwenzi",
    system_file_name="tianzhengdanhangwenzi.dwg",
    delete_system_text=False,
):
    """
    在当前激活图中写入一段“天正单行文字”（通过系统模板 Copy 实现），
    然后通过 last_obj() 找到模型空间最后生成的对象，
    按其外包盒锚点对齐到指定点 p。

    alignment 支持：
        - "左下" / "左对齐" / "LB"
        - "左上" / "LT"
        - "右下" / "RB"
        - "右上" / "RT"
        - "中心" / "center" / "C"
      其它值默认按“左下”处理。
    """
    from system.CAD_core import copy_file_content_pywin32

    # —— 小工具：根据外包盒对齐到目标点 —— #
    def _align_entity_by_bbox(ent, target_point, align="左下"):
        """
        使用无参数版 GetBoundingBox()：
          1. min_pt, max_pt = ent.GetBoundingBox()
          2. 根据 alignment 选锚点
          3. Move(锚点 → 目标点)
        """
        try:
            min_pt, max_pt = ent.GetBoundingBox()  # ★ 关键：和你在控制台里一样的调用方式
        except Exception as e:
            sys_logger.info(f"[错误] 获取外包盒失败: {e}")
            return

        xmin, ymin, zmin = min_pt
        xmax, ymax, zmax = max_pt
        sys_logger.info(f"[对齐-前]  BBox min={min_pt}, max={max_pt}")

        alg = str(align).strip().lower()
        if alg in ("左下", "左对齐", "lb"):
            anchor_pt = (xmin, ymin, zmin)
        elif alg in ("左上", "lt"):
            anchor_pt = (xmin, ymax, zmin)
        elif alg in ("右下", "rb"):
            anchor_pt = (xmax, ymin, zmin)
        elif alg in ("右上", "rt"):
            anchor_pt = (xmax, ymax, zmin)
        elif alg in ("中心", "center", "c"):
            anchor_pt = ((xmin + xmax) / 2.0,
                         (ymin + ymax) / 2.0,
                         (zmin + zmax) / 2.0)
        else:
            anchor_pt = (xmin, ymin, zmin)

        # 目标点：如果只传 (x, y)，z 用当前 zmin；否则用传入的 z
        if len(target_point) == 2:
            tx, ty = float(target_point[0]), float(target_point[1])
            tz = float(zmin)
        else:
            tx, ty, tz = float(target_point[0]), float(target_point[1]), float(target_point[2])

        target_pt = (tx, ty, tz)

        sys_logger.info(f"[对齐-计算] alignment='{align}', anchor_pt={anchor_pt} → target_pt={target_pt}")

        from_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, anchor_pt)
        to_pt   = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, target_pt)
        ent.Move(from_pt, to_pt)

        # 再读一次外包盒看结果
        try:
            min_pt2, max_pt2 = ent.GetBoundingBox()
            sys_logger.info(f"[对齐-后]  BBox min={min_pt2}, max={max_pt2}")
        except Exception as e:
            sys_logger.info(f"[警告] 对齐后再次获取外包盒失败: {e}")

    try:
        # ===== 1. 确保连接到当前 DWG =====

        acad = C.acad
        doc  = C.doc

        # ===== 2. 查找/插入系统模板文字 =====
        lb = stc(system_layer)
        if len(lb) == 0:
            # 需要从系统文件插入一次模板
            system_file = Path(XITONG_DIR) / system_file_name
            if not system_file.exists():
                sys_logger.info(f"[错误] 系统天正文字文件不存在: {system_file}")
                return None

            current_file = doc.FullName
            sys_logger.info(f"[信息] 未找到系统文字图层 {system_layer}，从 {system_file} 插入...")

            try:
                
                ok = copy_file_content_pywin32(str(system_file), current_file)
                if not ok:
                    print("[警告] copy_file_content_pywin32 返回 False，可能部分失败，但继续尝试。")
            except Exception as e:
                sys_logger.info(f"[警告] 插入系统文字文件时抛出异常：{e}，继续尝试查找图层。")

            # 再 li 一次，重新查模板

            acad = C.acad
            doc  = C.doc
            lb   = stc(system_layer)

        if len(lb) == 0:
            sys_logger.info(f"[错误] 即使插入系统文件后，仍未在图层 {system_layer} 找到模板文字。")
            return None
        elif len(lb) > 1:
            sys_logger.info(f"[警告] 图层 {system_layer} 上找到 {len(lb)} 个对象，默认使用第一个作为模板。")

        template = lb[0]
        sys_logger.info(f"[信息] 使用模板文字: ObjectName={template.ObjectName}, Handle={template.Handle}")

        # ===== 3. 从模板 Copy 出新文字对象（不对齐） =====
        try:
            new_text = template.Copy()
        except Exception as e:
            sys_logger.info(f"[错误] 无法从模板文字 Copy 新对象：{e}")
            return None

        sys_logger.info(f"[DEBUG] 复制得到的新文字: ObjectName={new_text.ObjectName}, Handle={new_text.Handle}")

        # ===== 4. 设置天正文字属性（对新对象操作） =====
        try:
            set_object_property(new_text, "Text", text)
            set_object_property(new_text, "Height", height)
            set_object_property(new_text, "WidthFactor", width_factor)
            set_object_property(new_text, "Rotation", rotation)
            set_object_property(new_text, "Oblique", oblique)
            if style:
                set_object_property(new_text, "TextStyle", style)

            print(
                f"[步骤] 已设置天正文字属性: "
                f"text='{text}', 高度={height}, 宽度因子={width_factor}, "
                f"旋转={rotation}, 倾斜={oblique}, 样式={style or '[沿用模板]'}"
            )
        except Exception as e:
            sys_logger.info(f"[警告] 设置天正文字属性时出错：{e}")

        # ===== 5. 等待天正生成完对象，再通过 last_obj() 重新选取 =====
        try:
            time.sleep(1.5)     # 给天正一点时间
            try:
                doc.Regen(1)    # acAllViewports
            except Exception:
                pass
            try:
                pythoncom.PumpWaitingMessages()
            except Exception:
                pass
        except Exception:
            pass


        acad = C.acad
        doc  = C.doc

        try:
            ent = last_obj()
        except Exception as e:
            sys_logger.info(f"[错误] 调用 last_obj() 失败: {e}")
            return None

        # last_obj 可能返回单个对象或列表
        try:
            _ = ent.ObjectName
        except Exception:
            try:
                ent = ent[-1]
            except Exception as e:
                sys_logger.info(f"[错误] last_obj() 返回值类型无法识别: {e}")
                return None

        objname = getattr(ent, "ObjectName", "<无>")
        handle  = getattr(ent, "Handle", "<无>")
        sys_logger.info(f"[DEBUG] last_obj() 得到实体: ObjectName={objname}, Handle={handle}")

        # ===== 6. 用外包盒锚点对齐到 p（默认左下） =====
        _align_entity_by_bbox(ent, p, align=alignment or "左下")

        # ===== 7. 按需删除系统模板文字（保留这次新写的文字） =====
        if delete_system_text:
            try:
                print(
                    f"[信息] delete_system_text=True，正在删除图层 "
                    f"{system_layer} 上的系统模板文字（保留当前新文字）..."
                )
                cnt = 0
                ent_handle = str(getattr(ent, "Handle", "")).upper()
                objs = stc(system_layer)
                print(
                    f"[OK] 第 1 次尝试：选到图层 ['{system_layer}'] 上 "
                    f"{len(objs)} 个对象"
                )
                for obj in objs:
                    try:
                        h = str(getattr(obj, "Handle", "")).upper()
                        # 保护当前新文字：Handle 相同则跳过
                        if h == ent_handle:
                            continue
                        obj.Delete()
                        cnt += 1
                    except Exception:
                        pass
                sys_logger.info(f"[成功] 已删除 {cnt} 个系统文字模板对象")
            except Exception as e:
                sys_logger.info(f"[警告] 删除系统模板文字失败：{e}")

        sys_logger.info(f"[完成] 天正单行文字创建成功，位置约为 {p}\n")
        return ent  # 返回对齐后的实体

    except Exception as e:
        sys_logger.info(f"[错误] write_tianzheng_text 执行失败：{e}")
        import traceback
        traceback.print_exc()
        return None


# ====================  文字垂直对齐 ====================

#&&% 文字垂直对齐
def align_text_to_vertical_line(
    text_obj,
    x_position,
    align_side="左边界"
):
    """
    将文字按 BoundingBox 边界对齐到指定垂直线的 X 坐标。

    参数:
        text_obj:
            - 单个文字对象 (AcDbText / TDbText / 其它有 GetBoundingBox 的实体)
            - 或者多个文字对象组成的列表 / 元组 / 其它可迭代

        x_position:
            - 一个数字 x
            - 或一个点 (x, y)
            - 或一个点 (x, y, z)
            最终只使用 x 作为垂直线的 X 坐标。

        align_side:
            - "左边界": 使用外包盒左边界对齐到 x
            - "右边界": 使用外包盒右边界对齐到 x
    """

    C.li()
    # —— 1. 归一化 text_obj 为列表 —— #
    if text_obj is None:
        print("[错误] text_obj 为空，无法对齐。")
        return False

    # 单个对象：不是可迭代（或者是 COM 对象），就包装成列表
    objs = None
    if isinstance(text_obj, (list, tuple, set)):
        objs = list(text_obj)
    else:
        # 有些 COM 对象也会被当成可迭代，这里简单认为“有 GetBoundingBox 属性”的就是单个对象
        # 保守起见：直接包装成列表
        objs = [text_obj]

    if not objs:
        print("[错误] text_obj 列表为空，无法对齐。")
        return False

    # —— 2. 解析 x_position —— #
    if isinstance(x_position, numbers.Real):
        x_target = float(x_position)
    elif isinstance(x_position, (list, tuple)):
        if len(x_position) == 0:
            print("[错误] x_position 为空序列。")
            return False
        x_target = float(x_position[0])
    else:
        # 其它类型（例如 VARIANT），尝试转成 float
        try:
            x_target = float(x_position)
        except Exception:
            sys_logger.info(f"[错误] 无法从 x_position={x_position!r} 解析出 X 坐标。")
            return False

    sys_logger.info(f"[信息] 垂直对齐目标 X = {x_target}，处理对象数量 = {len(objs)}")

    # —— 3. 遍历对齐每一个对象 —— #
    success_count = 0

    for idx, obj in enumerate(objs, start=1):
        try:
            # 3.1 获取 BoundingBox（无参数版本）
            ll_pt, ur_pt = obj.GetBoundingBox()
            sys_logger.info(f"[对象#{idx}] 原外包盒: min={ll_pt}, max={ur_pt}")

            # 3.2 计算移动距离
            if align_side == "左边界":
                dx = x_target - float(ll_pt[0])
            elif align_side == "右边界":
                dx = x_target - float(ur_pt[0])
            else:
                sys_logger.info(f"[对象#{idx}] [错误] 不支持的对齐方式: {align_side}")
                continue

            # 3.3 执行移动（只沿 X 方向）
            base_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
            move_vec = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [dx, 0.0, 0.0])
            obj.Move(base_pt, move_vec)

            # 3.4 再读一遍外包盒验证
            ll_pt2, ur_pt2 = obj.GetBoundingBox()
            sys_logger.info(f"[对象#{idx}] 新外包盒: min={ll_pt2}, max={ur_pt2}")
            sys_logger.info(f"[对象#{idx}] [成功] 文字{align_side}已对齐到 X={x_target}")
            success_count += 1

        except Exception as e:
            sys_logger.info(f"[对象#{idx}] [错误] 垂直对齐失败: {e}")

    if success_count == 0:
        print("[结果] 所有对象对齐都失败。")
        return False
    elif success_count < len(objs):
        sys_logger.info(f"[结果] 部分对齐成功: 成功 {success_count} / {len(objs)}")
        return False
    else:
        sys_logger.info(f"[结果] 全部 {success_count} 个对象已成功对齐到 X={x_target}")
        return True

# ====================  文字水平对齐 ====================
#&&% 文字水平对齐
def align_text_to_horizontal_line(
    text_obj,
    y_position,
    align_side="下边界"
):
    """
    将文字按 BoundingBox 边界对齐到指定水平线的 Y 坐标。

    参数:
        text_obj:
            - 单个文字对象 (AcDbText / TDbText / 其它有 GetBoundingBox 的实体)
            - 或者多个文字对象组成的列表 / 元组 / 其它可迭代

        y_position:
            - 一个数字 y
            - 或一个点 (x, y)
            - 或一个点 (x, y, z)
            最终只使用 y 作为水平线的 Y 坐标。

        align_side:
            - "下边界": 使用外包盒下边界对齐到 y
            - "上边界": 使用外包盒上边界对齐到 y
    """


    C.li()
    # —— 1. 归一化 text_obj 为列表 —— #
    if text_obj is None:
        print("[错误] text_obj 为空，无法对齐。")
        return False

    if isinstance(text_obj, (list, tuple, set)):
        objs = list(text_obj)
    else:
        # 直接包装成列表（和垂直对齐那边保持一致）
        objs = [text_obj]

    if not objs:
        print("[错误] text_obj 列表为空，无法对齐。")
        return False

    # —— 2. 解析 y_position —— #
    if isinstance(y_position, numbers.Real):
        y_target = float(y_position)
    elif isinstance(y_position, (list, tuple)):
        if len(y_position) < 2:
            print("[错误] y_position 序列长度不足 2，无法获取 Y 坐标。")
            return False
        y_target = float(y_position[1])
    else:
        # 尝试从其它类型（例如 VARIANT）解析为 float
        try:
            y_target = float(y_position)
        except Exception:
            sys_logger.info(f"[错误] 无法从 y_position={y_position!r} 解析出 Y 坐标。")
            return False

    sys_logger.info(f"[信息] 水平对齐目标 Y = {y_target}，处理对象数量 = {len(objs)}")

    # —— 3. 遍历对齐每一个对象 —— #
    success_count = 0

    for idx, obj in enumerate(objs, start=1):
        try:
            # 3.1 获取 BoundingBox（无参数版本）
            ll_pt, ur_pt = obj.GetBoundingBox()
            sys_logger.info(f"[对象#{idx}] 原外包盒: min={ll_pt}, max={ur_pt}")

            # 3.2 计算移动距离
            if align_side == "下边界":
                dy = y_target - float(ll_pt[1])
            elif align_side == "上边界":
                dy = y_target - float(ur_pt[1])
            else:
                sys_logger.info(f"[对象#{idx}] [错误] 不支持的对齐方式: {align_side}")
                continue

            # 3.3 执行移动（只沿 Y 方向）
            base_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
            move_vec = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, dy, 0.0])
            obj.Move(base_pt, move_vec)

            # 3.4 再读一遍外包盒验证
            ll_pt2, ur_pt2 = obj.GetBoundingBox()
            sys_logger.info(f"[对象#{idx}] 新外包盒: min={ll_pt2}, max={ur_pt2}")
            sys_logger.info(f"[对象#{idx}] [成功] 文字{align_side}已对齐到 Y={y_target}")
            success_count += 1

        except Exception as e:
            sys_logger.info(f"[对象#{idx}] [错误] 水平对齐失败: {e}")

    if success_count == 0:
        print("[结果] 所有对象水平对齐都失败。")
        return False
    elif success_count < len(objs):
        sys_logger.info(f"[结果] 部分水平对齐成功: 成功 {success_count} / {len(objs)}")
        return False
    else:
        sys_logger.info(f"[结果] 全部 {success_count} 个对象已成功对齐到 Y={y_target}")
        return True

# ====================  缩放天正文字高度 ====================

#&&% 缩放天正文字
def scale_tianzheng_text_to_cad(
    tianzheng_text_obj,
    cad_text_obj
):
    """
    使用 ScaleEntity 将天正文字的 BoundingBox 高度缩放到 CAD 文字的高度。

    参数:
        tianzheng_text_obj:
            - 单个天正文字对象（TDbText/TDbMText等，有 GetBoundingBox/ScaleEntity）
            - 或多个天正文字对象组成的列表/元组/集合

        cad_text_obj:
            - CAD 文字对象（AcDbText/AcDbMText 等），
              用它的 BoundingBox 高度作为“目标高度”
    """
    C.li()
    # —— 1. 归一化 tianzheng_text_obj 为列表 —— #
    if tianzheng_text_obj is None:
        print("[错误] tianzheng_text_obj 为空，无法缩放。")
        return False

    if isinstance(tianzheng_text_obj, (list, tuple, set)):
        tz_objs = list(tianzheng_text_obj)
    else:
        tz_objs = [tianzheng_text_obj]

    if not tz_objs:
        print("[错误] tianzheng_text_obj 列表为空，无法缩放。")
        return False

    # —— 2. 获取 CAD 文字的目标高度 —— #
    try:
        cad_ll_pt, cad_ur_pt = cad_text_obj.GetBoundingBox()
        cad_height = float(cad_ur_pt[1]) - float(cad_ll_pt[1])
    except Exception as e:
        sys_logger.info(f"[错误] 获取 CAD 文字 BoundingBox 失败: {e}")
        return False

    if not isinstance(cad_height, numbers.Real) or cad_height == 0:
        sys_logger.info(f"[错误] CAD 文字高度无效: {cad_height}")
        return False

    sys_logger.info(f"[信息] 目标 CAD 文字高度 = {cad_height:.4f}，待缩放对象数 = {len(tz_objs)}")

    # —— 3. 遍历缩放每一个天正文字 —— #
    success_count = 0

    for idx, tz_obj in enumerate(tz_objs, start=1):
        try:
            # 3.1 获取天正文字的 BoundingBox（无参数版）
            tz_ll_pt, tz_ur_pt = tz_obj.GetBoundingBox()
            tz_height = float(tz_ur_pt[1]) - float(tz_ll_pt[1])

            sys_logger.info(f"[对象#{idx}] 原外包盒: min={tz_ll_pt}, max={tz_ur_pt}")
            sys_logger.info(f"[对象#{idx}] 原高度: {tz_height:.4f}")

            if tz_height == 0:
                sys_logger.info(f"[对象#{idx}] [错误] 天正文字高度为 0，跳过。")
                continue

            # 3.2 计算缩放比例
            scale_factor = cad_height / tz_height

            # 3.3 以外包盒中心作为缩放基点
            center_x = (float(tz_ll_pt[0]) + float(tz_ur_pt[0])) / 2.0
            center_y = (float(tz_ll_pt[1]) + float(tz_ur_pt[1])) / 2.0
            if len(tz_ll_pt) > 2:
                center_z = (float(tz_ll_pt[2]) + float(tz_ur_pt[2])) / 2.0
            else:
                center_z = 0.0

            scale_pt = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_R8,
                [center_x, center_y, center_z]
            )

            # 3.4 执行缩放
            tz_obj.ScaleEntity(scale_pt, scale_factor)

            # 3.5 再获取一次外包盒，验证新的高度
            new_ll_pt, new_ur_pt = tz_obj.GetBoundingBox()
            new_height = float(new_ur_pt[1]) - float(new_ll_pt[1])

            sys_logger.info(f"[对象#{idx}] [成功] 已缩放天正文字")
            sys_logger.info(f"  原高度: {tz_height:.4f}")
            sys_logger.info(f"  目标高度: {cad_height:.4f}")
            sys_logger.info(f"  实际新高度: {new_height:.4f}")
            sys_logger.info(f"  缩放比例: {scale_factor:.6f}")
            success_count += 1

        except Exception as e:
            sys_logger.info(f"[对象#{idx}] [错误] 缩放失败: {e}")

    if success_count == 0:
        print("[结果] 所有天正文字缩放都失败。")
        return False
    elif success_count < len(tz_objs):
        sys_logger.info(f"[结果] 部分缩放成功: 成功 {success_count} / {len(tz_objs)}")
        return False
    else:
        sys_logger.info(f"[结果] 全部 {success_count} 个天正文字已成功缩放到 CAD 文字高度。")
        return True

#&&&% 非图形对象


#&&% *** 将屏幕所选对象赋予到指定图层


@alias("s1")
def sc_objs_to_layer(layer_name,cl=256):

    doc=C.doc

    def pmxz_new():
        """
        人工选择对象，返回所选实体对象列表。
        自动清理已有的 "SS1" 选择集。
        """
        try:
            # 如果 "SS1" 已存在，先删除
            try:
                ss = doc.SelectionSets.Item("SS1")
                ss.Delete()
            except:
                pass  # 如果不存在就忽略

            selection = doc.SelectionSets.Add("SS1")
            selection.SelectOnScreen()
            objs = [selection.Item(i) for i in range(selection.Count)]
            selection.Delete()
            return objs
        except Exception as e:
            print("[错误] 选择失败:", e)
            return []



    layers = doc.Layers

    try:
        layer = layers.Item(layer_name)
    except:
        layer = layers.Add(layer_name)
        sys_logger.info(f"🟢 已新建图层：{layer_name}")

    LB=pmxz_new()

    for x in LB:

        x.Layer = layer_name

        x.color = cl


    return LB

#&&% 删除图层
def delete_layer(layername: str):
    """
    删除当前 DWG 文件中名为 layername 的图层。
    - 如果图层不存在，直接返回。
    - 如果图层是当前层，则切换到 0 层后再删除。
    - 删除前会尝试解锁、去掉冻结/打印锁。
    """
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    layers = doc.Layers

    try:
        layer = layers.Item(layername)
    except Exception:
        sys_logger.info(f"[警告] 图层 {layername} 不存在。")
        return

    # 如果该图层是当前层，切换到 "0"
    if doc.ActiveLayer.Name == layername:
        doc.ActiveLayer = layers.Item("0")

    # 解锁、解冻、去掉打印锁定，避免删除失败
    try:
        layer.Lock = False
        layer.Freeze = False
        layer.Plottable = True
    except Exception:
        pass

    try:
        layer.Delete()
        sys_logger.info(f"[OK] 图层 {layername} 已删除。")
    except Exception as e:
        sys_logger.info(f"[错误] 删除失败：{e}")



#&&% 从列表创建图层
def create_layers_from_list(layer_names):
    """
    创建列表中指定的图层，如果图层已存在则跳过。

    参数：
        layer_names: 包含图层名称的字符串列表
    """
    try:
        _, doc = get_acad_doc()
        layers = doc.Layers
        created = 0
        skipped = 0

        for name in layer_names:
            try:
                _ = layers.Item(name)  # 检查是否已存在
                sys_logger.info(f"⏩ 图层已存在：{name}")
                skipped += 1
            except:
                layers.Add(name)
                sys_logger.info(f"[OK] 新建图层：{name}")
                created += 1

        sys_logger.info(f"\n📊 总计：新建 {created} 个图层，跳过 {skipped} 个已有图层")

    except Exception as e:
        print("[错误] 创建图层时出错：", e)


#&&% 从列表删除图层
def delete_layers_from_list(layer_names):
    """
    删除列表中指定的图层

    参数：
        layer_names: 包含图层名称的字符串列表

    返回：
        dict: {'deleted': 删除成功的图层列表, 'failed': 删除失败的图层列表}
    """
    try:
        _, doc = get_acad_doc()
        layers = doc.Layers
        deleted = []
        failed = []

        for name in layer_names:
            try:
                layer = layers.Item(name)
                # 检查是否为当前图层
                if doc.ActiveLayer.Name == name:
                    sys_logger.info(f"[警告] 图层 '{name}' 是当前图层，无法删除")
                    failed.append(name)
                    continue

                # 尝试删除图层
                layer.Delete()
                sys_logger.info(f"[成功] 已删除图层：{name}")
                deleted.append(name)
            except Exception as e:
                sys_logger.info(f"[失败] 无法删除图层 '{name}'：{e}")
                failed.append(name)

        sys_logger.info(f"\n[统计] 成功删除 {len(deleted)} 个图层，失败 {len(failed)} 个")
        return {'deleted': deleted, 'failed': failed}

    except Exception as e:
        sys_logger.info(f"[错误] 删除图层时出错：{e}")
        return {'deleted': [], 'failed': layer_names}


#&&% 逐点标注
def dim_by_points(*args):
    """
    使用天正逐点标注命令对倾斜对象进行标注

    参数：
        *args: 三个点坐标 (x1,y1,z1), (x2,y2,z2), (x3,y3,z3)
               或 p1, p2, p3 其中p1,p2是被标注对象的起始点和终点，p3是标注位置点

    返回：
        bool: 成功返回True
    """
    import pyautogui
    import time

    try:
        # 解析参数
        if len(args) == 3:
            p1, p2, p3 = args
        else:
            print("[错误] 需要3个点坐标")
            return False

        # 最小化所有窗口
        pyautogui.hotkey('win', 'd')
        time.sleep(0.5)

        # 激活AutoCAD窗口
        activate_window_by_title("AutoCAD", click_titlebar=True)
        time.sleep(0.5)

        # 发送天正逐点标注命令
        _, doc = get_acad_doc()
        cmd = f"zdbz\n{p1[0]},{p1[1]}\n{p2[0]},{p2[1]}\n{p3[0]},{p3[1]}\n\n"
        doc.SendCommand(cmd)

        print("[成功] 已执行逐点标注")
        return True

    except Exception as e:
        sys_logger.info(f"[错误] 标注失败：{e}")
        return False


#&&% 确保图层存在并清空
def ensure_layer(layer_name="jizhunwall"):
    """
    确保图层存在并设为当前图层，同时删除该图层上所有对象（最多重试 3 次）。
    """
    try:
        li()

        layers = doc.Layers
        # 1) 获取或新建图层
        try:
            layer = layers.Item(layer_name)
        except Exception:
            layer = layers.Add(layer_name)
            sys_logger.info(f"🟢 已新建图层：{layer_name}")
        # 2) 切换到图层
        doc.ActiveLayer = layer
        sys_logger.info(f"[OK] 当前图层已设置为：{layer_name}")

        # 3) 删除图层中全部对象，重试 up to 5
        for attempt in range(1, 6):
            ents = select_tuceng(layer_name)
            if not ents:
                # 已经没有对象，提前退出
                sys_logger.info(f"[CLEAN] 图层 '{layer_name}' 已清空（共尝试 {attempt - 1} 次）")
                break

            deleted = 0
            for ent in ents:
                try:
                    ent.Delete()
                    deleted += 1
                except:
                    continue
            sys_logger.info(f"  第 {attempt} 次删除：共删除 {deleted} 个对象")

            time.sleep(0.1)  # 短暂等待，确保对象被移除


            #刷新

            doc.SendCommand("RE\n")
            doc.SendCommand("Z\nE\n")

        else:
            # 五次都还有残留
            remaining = len(select_tuceng(layer_name))
            sys_logger.info(f"[警告] 重试 3 次后，图层 '{layer_name}' 仍有 {remaining} 个对象未能删除")

    except Exception as e:
        print("[错误] 创建/切换图层或清理失败：", e)
#&&% 只在模型空间上清理

def ensure_layer_model_only(layer_name="jizhunwall"):
    """
    确保图层存在并设为当前图层，同时【仅删除】该图层在模型空间（Model Space）中的对象。
    """
    from  CAD_file_operations   import get_obj_loc
    try:
        doc=C.doc  # 确保连接

        layers = doc.Layers
        # 1) 获取或新建图层
        try:
            layer = layers.Item(layer_name)
        except Exception:
            layer = layers.Add(layer_name)
            sys_logger.info(f"🟢 已新建图层：{layer_name}")
            
        # 2) 切换到图层
        doc.ActiveLayer = layer
        sys_logger.info(f"[OK] 当前图层已设置为：{layer_name}")

        # 3) 循环清理模型空间的对象
        for attempt in range(1, 6):
            # 获取该图层的所有对象（可能跨空间）
            ents = select_tuceng(layer_name)
            if not ents:
                sys_logger.info(f"[CLEAN] 图层 '{layer_name}' 已无对象（共尝试 {attempt - 1} 次）")
                break

            deleted_count = 0
            model_ents_found = False

            for ent in ents:
                # --- 空间判定核心逻辑 ---
                # 调用 get_obj_loc 判定，如果是 1 则代表模型空间
                if get_obj_loc(ent) == 1:
                    model_ents_found = True
                    try:
                        ent.Delete()
                        deleted_count += 1
                    except Exception as e:
                        continue
            
            if not model_ents_found:
                sys_logger.info(f"[CLEAN] 图层 '{layer_name}' 在模型空间中已清空")
                break

            sys_logger.info(f"  第 {attempt} 次尝试删除：模型空间已移除 {deleted_count} 个对象")
            
            # 短暂等待并刷新视图
            time.sleep(0.1)
            doc.SendCommand("RE\n")

        else:
            # 如果 5 次后仍有模型空间对象
            remaining_ents = select_tuceng(layer_name)
            still_in_model = sum(1 for e in remaining_ents if get_obj_loc(e) == 1)
            if still_in_model > 0:
                sys_logger.info(f"[警告] 经过 5 次尝试后，模型空间仍有 {still_in_model} 个对象无法删除")

    except Exception as e:
        print("[错误] 空间清理操作失败：", e)





#&&% 确保图层当前
@alias("s2")

def ensure_layer_current(layer_name="jizhunwall", max_retries=3):
    """
    确保图层存在并设为当前图层，失败时最多重试 max_retries 次。
    """
    layers = doc.Layers
    for attempt in range(1, max_retries + 1):
        try:
            # 获取或新建图层
            try:
                layer = layers.Item(layer_name)
            except Exception:
                layer = layers.Add(layer_name)
                sys_logger.info(f"🟢 已新建图层：{layer_name}")
            # 切换到图层
            doc.ActiveLayer = layer
            sys_logger.info(f"[OK] 当前图层已设置为：{layer_name} (尝试 {attempt})")
            return True
        except Exception as e:
            sys_logger.info(f"[错误] 尝试 {attempt} 创建/设置图层失败：{e}")
    sys_logger.info(f"[错误] 达到最大重试次数 ({max_retries})，无法创建或切换到图层：{layer_name}")
    return False


# 设置指定图层的颜色、线型、开关状态和冻结状态

#&&% 设置图层属性
@alias("s3")

def set_layer_properties(layer_name, color_index=9, linetype="Continuous", on=True, frozen=False):
    """
    设置指定图层的颜色、线型、开关状态和冻结状态。

    参数：
        layer_name (str): 图层名称
        color_index (int): 图层颜色索引（默认 9）
        linetype (str): 图层线型名称（默认 'Continuous'）
        on (bool): 图层是否打开（默认 True）
        frozen (bool): 图层是否冻结（默认 False）
    """
    li()
    try:
        layers = doc.Layers
        try:
            layer = layers.Item(layer_name)
        except:
            layer = layers.Add(layer_name)
            sys_logger.info(f"[OK] 已新建图层：{layer_name}")

        # 设置颜色
        layer.color = color_index

        # 设置线型
        try:
            ltype = doc.Linetypes.Item(linetype)
        except:
            doc.Linetypes.Load(linetype, linetype)
            ltype = doc.Linetypes.Item(linetype)
        layer.Linetype = linetype

        # 设置开关状态
        layer.LayerOn = on

        # 设置冻结状态
        layer.Freeze = frozen


        doc.SendCommand("re\n")


        sys_logger.info(f"🔧 图层属性已更新：{layer_name} | 颜色={color_index} | 线型={linetype} | 开关={'开' if on else '关'} | 冻结={'是' if frozen else '否'}")

    except Exception as e:
        sys_logger.info(f"[错误] 设置图层属性失败：{e}")




#&&% 将列表中的对象图层设为目标图层


def set_layer_with_retry(LB, layername, ci=3):
    """
    将给定 COM 对象列表 LB 中的每个对象的 Layer 属性设为 layername。
    【核心逻辑】:
    1. 自动创建不存在的图层。
    2. 使用 setattr 动态设置属性，避开部分第三方实体的早期绑定限制。
    3. 针对 CAD 繁忙状态提供重试机制。
    """

    li() 
    current_doc = globals().get('doc')
    if current_doc is None:
        print("❌ 无法获取 CAD 文档对象")
        return [], list(LB)
    
    success = []
    failed = []

    # --- 1. 检查并创建图层 ---
    try:
        layers = current_doc.Layers
        try:
            layers.Item(layername)
        except Exception:
            sys_logger.info(f"[信息] 图层“{layername}”不存在，正在创建...")
            layers.Add(layername)
    except Exception as e:
        sys_logger.info(f"[错误] 无法访问或创建图层“{layername}”: {e}")
        return [], list(LB)

    # --- 2. 遍历设置对象图层 ---
    for obj in LB:
        set_done = False
        for attempt in range(1, ci + 1):
            try:
                # 使用 setattr 动态设置属性，增强对第三方实体的兼容性
                setattr(obj, 'Layer', layername)
                success.append(obj)
                set_done = True
                break
            except Exception as e:
                if attempt == ci:
                    failed.append(obj)
                    handle = getattr(obj, 'Handle', '<未知Handle>')
                    sys_logger.info(f"[警告] 对象 {handle} 设置图层“{layername}”失败：{e}")
                else:
                    time.sleep(1) # 失败重试间隔
                    
    return success, failed






#&&% 强制改图层对象颜色

def force_layer_objects_color(layer_name, target_color=256, max_retries=3):
    """
    [最终修正版] 强制改色
    修复逻辑: 当 set_attr 成功但无法读取属性(None)时，视为成功。
    """
    sys_logger.info(f"\n🎨 [改色执行] 图层: {layer_name} -> 目标颜色: {target_color}")
    
    try:
        all_objs = stc(layer_name)
    except:
        sys_logger.info(f"   ❌ 无法选择图层 {layer_name}")
        return False

    if not all_objs:
        print("   ℹ️ 图层为空，跳过")
        return True

    pending_objs = list(all_objs)
    
    for attempt in range(1, max_retries + 1):
        if not pending_objs:
            print("   ✅ 所有对象已达标")
            break
            
        sys_logger.info(f"   🔄 第 {attempt} 轮 (剩 {len(pending_objs)} 个)...")
        next_round_objs = []
        
        for i, obj in enumerate(pending_objs):
            try:
                # 1. 执行修改
                # 使用小写 "color"，这是你实测有效的
                is_set_ok = set_attr(obj, "color", target_color)
                
                # 尝试刷新显示
                try: obj.Update()
                except: pass
                
                # 2. 读取验证
                new_color = get_attr(obj, "Color")
                
                # --- [关键逻辑修正] ---
                # 判定成功的两种情况:
                # A: 读回来的值等于目标值 (完美)
                # B: set_attr 说成功了(True)，但读回来是 None (无法读取，但信任写入)
                
                if new_color == target_color:
                    # sys_logger.info(f"      [Obj {i}] ✅ 验证成功")
                    pass 
                elif is_set_ok and new_color is None:
                    # sys_logger.info(f"      [Obj {i}] ⚠️ 验证受限 (读回None)，但写入返回True -> 视为成功")
                    pass 
                else:
                    # 只有当 写入失败 或者 读回来是明确的错误数值 时，才重试
                    # 获取 Handle 方便调试
                    h_val = "???"
                    try: h_val = get_attr(obj, "Handle")
                    except: pass
                    
                    sys_logger.info(f"      [Obj {i} | H={h_val}] ❌ 失败: Set={is_set_ok}, Get={new_color}")
                    next_round_objs.append(obj)
                    
            except Exception as e:
                sys_logger.info(f"      ❌ 异常: {e}")
                next_round_objs.append(obj)
        
        pending_objs = next_round_objs
        if pending_objs: time.sleep(0.1)

    if not pending_objs:
        sys_logger.info(f"   ✅ 改色完成: 图层 {layer_name} 全员 {target_color}")
        return True
    else:
        sys_logger.info(f"   ⚠️ 改色结束: 仍有 {len(pending_objs)} 个对象状态存疑")
        return False


