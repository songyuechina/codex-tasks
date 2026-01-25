#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第六部分 图块操作
图块操作相关函数

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
from system.CAD_com_utils import sys_logger, retry_on_busy, SafeCOM, debuggable, timeit
from system.common_logger import checkpoint

# 获取常用对象
acad = C.acad
doc = C.doc
mp = C.mp
sp = C.sp

#&&&&%%  第六部分 图块操作 


#&&&% 原块处理

#&&&% 块属性

#&&% 获取块实例块名

def get_block_name(obj):
    """获取块名，兼容动态块(EffectiveName)"""
    try:
        # 优先尝试获取动态块的真实名称
        return getattr(obj, "EffectiveName", obj.Name)
    except:
        return getattr(obj, "Name", "")


#&&% 获取块属性值
def huoqukuai_shuxing_zhi(XX):#XX为属性块实体


    attributes = XX.GetAttributes()

    tags=[]
    values=[]

    for attr in attributes:
               
        tag = attr.TagString

            
        value = attr.TextString

        tags.append(tag)

        values.append(value)

    return tags,values



#&&% 属性块标签编辑

def update_block_def_attributes_safe(
    block_ref_or_name, 
    target_tag, 
    *, 
    style=None,            
    height=None,           
    width_factor=None,     
    rotation_deg=None,     
    justify=None,         
    align_point=None,     
    boundary_width=None,  
    verbose=True
):
    """
    【函数编号】: BLK-007-Safe
    【功能描述】: 
        修改块定义属性（完全使用 get_attr/set_attr 封装，禁止直接属性访问）。
        保留了 V7 的“对正优先”逻辑。
    """
    doc=C.doc


    # ================= 1. 获取块定义名称 =================
    block_name = None
    if isinstance(block_ref_or_name, str):
        block_name = block_ref_or_name
    else:
        # 替换 .EffectiveName 和 .Name
        block_name = get_attr(block_ref_or_name, 'EffectiveName')
        if not block_name:
            block_name = get_attr(block_ref_or_name, 'Name')

    if not block_name:
        sys_logger.info(f"[错误] 无法解析块名")
        return False

    if verbose:
        sys_logger.info(f"\n=== [修改块定义] 目标: '{block_name}' / 标签: '{target_tag}' ===")

    try:
        # 获取 Blocks 集合 -> Item
        blocks_coll = get_attr(doc, 'Blocks')
        block_def = blocks_coll.Item(block_name)
    except Exception as e:
        sys_logger.info(f"[错误] 找不到块定义: {e}")
        return False

    target_def = None
    
    # ================= 2. 扫描并锁定属性定义对象 =================
    # 遍历块定义中的实体
    for entity in block_def:
        # 替换 entity.ObjectName
        obj_name = get_attr(entity, 'ObjectName')
        
        if obj_name == "AcDbAttributeDefinition":
            # 尝试转换接口
            attr_obj = cast_object(entity)
            
            # 替换 attr_obj.TagString
            current_tag = get_attr(attr_obj, 'TagString')
            
            if current_tag == target_tag:
                target_def = attr_obj
                break
    
    if target_def is None:
        if verbose: sys_logger.info(f"[失败] 未找到标签 '{target_tag}'。")
        return False

    # ================= 3. 执行修改 (使用 set_attr) =================
    any_change = False
    
    try:
        # —————————— [步骤 1] 优先设置对正 (Alignment) ——————————
        if justify is not None:
            # 替换 target_def.Alignment = int(justify)
            if set_attr(target_def, 'Alignment', int(justify)):
                any_change = True
                if verbose: sys_logger.info(f"  - [设置] 对正模式: {justify}")
            else:
                sys_logger.info(f"[警告] 设置对正失败")

        # —————————— [步骤 2] 基础外观属性 ——————————
        if style is not None:
            if set_attr(target_def, 'StyleName', str(style)):
                any_change = True

        if height is not None:
            if set_attr(target_def, 'Height', float(height)):
                any_change = True

        if width_factor is not None:
            if set_attr(target_def, 'ScaleFactor', float(width_factor)):
                any_change = True

        if rotation_deg is not None:
            rad = float(rotation_deg) * math.pi / 180.0
            if set_attr(target_def, 'Rotation', rad):
                any_change = True

        # —————————— [步骤 3] 多行属性与边界 (MText) ——————————
        if boundary_width is not None:
            # 1. 检测当前状态: get_attr(target_def, 'MTextAttribute')
            is_multiline = False
            current_mtext_attr = get_attr(target_def, 'MTextAttribute')
            if current_mtext_attr: 
                is_multiline = True
            
            # 2. 强制开启多行
            if not is_multiline:
                if set_attr(target_def, 'MTextAttribute', True):
                    is_multiline = True

            # 3. 设置宽度
            if is_multiline:
                if set_attr(target_def, 'MTextBoundaryWidth', float(boundary_width)):
                    any_change = True
                    if verbose: sys_logger.info(f"  - [设置] MText边界宽: {boundary_width}")
            else:
                if verbose: sys_logger.info(f"  - [忽略] 无法开启多行模式")

        # —————————— [步骤 4] 坐标移动 (.Move) ——————————
        # Move 是方法，不是属性，但我们需要先获取基点属性
        if align_point is not None:
            if len(align_point) == 2:
                tgt_x, tgt_y, tgt_z = float(align_point[0]), float(align_point[1]), 0.0
            else:
                tgt_x, tgt_y, tgt_z = float(align_point[0]), float(align_point[1]), float(align_point[2])
            
            # 获取当前对正
            current_align = get_attr(target_def, 'Alignment')
            
            start_raw = None
            pt_type = "插入点"
            
            if current_align == 0: # Left
                start_raw = get_attr(target_def, 'InsertionPoint')
            else:
                start_raw = get_attr(target_def, 'TextAlignmentPoint')
                pt_type = "对齐点"
            
            if start_raw:
                start_x, start_y, start_z = start_raw[0], start_raw[1], start_raw[2]

                if verbose:
                    sys_logger.info(f"  - [移动] 以{pt_type}为基准: {start_raw} -> ({tgt_x}, {tgt_y}, {tgt_z})")

                if "vtpnt" in globals():
                    p1_variant = vtpnt(start_x, start_y, start_z)
                    p2_variant = vtpnt(tgt_x, tgt_y, tgt_z)
                    # Move 是方法，直接调用 COM 对象的方法
                    target_def.Move(p1_variant, p2_variant)
                    any_change = True
                else:
                    print("[警告] 缺少 vtpnt 函数")


    except Exception as e:
        sys_logger.info(f"[错误] 修改属性时发生异常: {e}")
        return False

    if any_change:
        if verbose: print("[成功] 属性定义已更新。")
        return True
    return False


def update_block_def_attributes_v7(
    block_ref_or_name, 
    target_tag, 
    *, 
    style=None,           
    height=None,          
    width_factor=None,    
    rotation_deg=None,    
    justify=None,         # 对正 (0-14)
    align_point=None,     # 目标坐标
    boundary_width=None,  # 边界宽度
    verbose=True
):
    """
    【函数编号】: BLK-007
    【所属模块】: 块定义管理模块 (Block Definition)
    【功能描述】: 
        修改图块的“底层定义”(Block Definition) 中的属性特性。
        用于统一修正图签的文字高度、对正方式、MText 边界宽等格式。
        
        V7 版本核心修复：
        1. 顺序免疫：强制将 'Alignment (对正)' 的设置提前到 'MText (边界宽)' 之前。
           (原因：一旦先开启 MText 属性，AutoCAD 往往会锁定 Alignment 属性导致报错)
        2. 坐标修正：保留 .Move() + vtpnt 逻辑，确保基点正确移动。

    【参数详解】:
        - block_ref_or_name (str/Obj): 块名字符串或块引用对象。
        - target_tag (str): 目标属性标签 (如 "图纸名称")。
        - style (str): 文字样式名。
        - height (float): 文字高度。
        - width_factor (float): 宽度因子 (0.7, 0.8 等)。
        - rotation_deg (float): 旋转角度 (度)。
        - justify (int): 对正方式 (0=Left, 1=Center, ...)。
        - align_point (list/tuple): 对齐点/插入点坐标 [x, y]。
        - boundary_width (float): MText 换行边界宽度。若设置此值，会自动开启多行模式。
        - verbose (bool): 是否打印详细日志。

    【返回值】:
        - bool: 修改成功返回 True，无变化或失败返回 False。


    """
    C.li()
    
    # --- 1. 获取块名 ---
    if isinstance(block_ref_or_name, str):
        block_name = block_ref_or_name
    else:
        try: block_name = block_ref_or_name.EffectiveName
        except: block_name = block_ref_or_name.Name

    if verbose:
        sys_logger.info(f"\n=== [修改块定义] 目标: '{block_name}' / 标签: '{target_tag}' ===")

    try:
        block_def = doc.Blocks.Item(block_name)
    except Exception as e:
        sys_logger.info(f"[错误] 找不到块定义: {e}")
        return False

    target_def = None
    
    # --- 2. 扫描并锁定对象 ---
    for entity in block_def:
        if entity.ObjectName == "AcDbAttributeDefinition":
            try:
                attr_obj = win32com.client.CastTo(entity, "IAcadAttribute")
                if not hasattr(attr_obj, "TagString"):
                     attr_obj = win32com.client.dynamic.Dispatch(entity)
            except:
                continue

            if attr_obj.TagString == target_tag:
                target_def = attr_obj
                break
    
    if target_def is None:
        if verbose: sys_logger.info(f"[失败] 未找到标签 '{target_tag}'。")
        return False

    # --- 3. 执行修改 (注意顺序！) ---
    any_change = False
    
    try:
        # =======================================================
        # [步骤 1] 优先设置对正 (Alignment)
        # =======================================================
        # 在开启 MText 之前设置对正，兼容性最好
        if justify is not None:
            try:
                target_def.Alignment = int(justify)
                any_change = True
                if verbose: sys_logger.info(f"  - [设置] 对正: {justify}")
            except Exception as e:
                sys_logger.info(f"[警告] 设置对正失败: {e}")

        # =======================================================
        # [步骤 2] 基础属性
        # =======================================================
        if style is not None:
            target_def.StyleName = str(style)
            any_change = True

        if height is not None:
            target_def.Height = float(height)
            any_change = True

        if width_factor is not None:
            target_def.ScaleFactor = float(width_factor)
            any_change = True

        if rotation_deg is not None:
            target_def.Rotation = float(rotation_deg) * math.pi / 180.0
            any_change = True

        # =======================================================
        # [步骤 3] 多行属性与边界 (MText)
        # =======================================================
        if boundary_width is not None:
            # 1. 检测当前状态
            is_multiline = False
            try:
                if target_def.MTextAttribute: is_multiline = True
            except: pass
            
            # 2. 如果之前不是多行，现在强制开启
            if not is_multiline:
                try:
                    target_def.MTextAttribute = True
                    is_multiline = True
                except:
                    pass

            # 3. 设置宽度
            if is_multiline:
                target_def.MTextBoundaryWidth = float(boundary_width)
                any_change = True
                if verbose: sys_logger.info(f"  - [设置] 边界宽: {boundary_width}")
            else:
                if verbose: sys_logger.info(f"  - [忽略] 无法开启多行模式，忽略边界宽度")

        # =======================================================
        # [步骤 4] 坐标移动 (.Move)
        # =======================================================
        if align_point is not None:
            # 准备数据
            if len(align_point) == 2:
                tgt_x, tgt_y, tgt_z = float(align_point[0]), float(align_point[1]), 0.0
            else:
                tgt_x, tgt_y, tgt_z = float(align_point[0]), float(align_point[1]), float(align_point[2])
            
            # 智能判断基点 (基于最新的对正方式)
            current_align = target_def.Alignment
            if current_align == 0: # Left
                start_raw = target_def.InsertionPoint 
                pt_type = "插入点"
            else:
                start_raw = target_def.TextAlignmentPoint
                pt_type = "对齐点"
            
            start_x, start_y, start_z = start_raw[0], start_raw[1], start_raw[2]

            if verbose:
                sys_logger.info(f"  - [移动] 以{pt_type}为基准: {start_raw} -> ({tgt_x}, {tgt_y}, {tgt_z})")

            # 类型转换 (vtpnt)
            p1_variant = vtpnt(start_x, start_y, start_z)
            p2_variant = vtpnt(tgt_x, tgt_y, tgt_z)

            # 执行移动
            target_def.Move(p1_variant, p2_variant)
            any_change = True

    except Exception as e:
        sys_logger.info(f"[错误] 修改属性时发生异常: {e}")
        return False

    if any_change:
        if verbose: print("[成功] 属性定义已更新。请执行 ATTSYNC 刷新实例。")
        return True
    else:
        if verbose: print("[提示] 无变化。")
        return False

#&&% 属性块标签编辑生效

def attsync_block_instance(block_ref_obj):
    """
    【函数编号】: CMD-001
    【功能描述】: 
        强力同步属性块。
        连续执行 3 次 Base 操作，确保 AutoCAD 彻底刷新属性位置。
    """
    success_at_least_once = False
    
    # 获取块名用于日志（仅用于显示，失败不影响流程）
    try:
        b_name = get_attr(block_ref_obj,"Name")
    except:
        b_name = "未知块"

    sys_logger.info(f"🔄 [强力同步] 正在对 {b_name} 执行 3 轮 ATTSYNC...")

    for i in range(2):
        # 执行底层同步
        result = attsync_block_instance_base(block_ref_obj)
        
        if result:
            success_at_least_once = True
            # sys_logger.info(f"  -> 第 {i+1}/3 次指令已发送")
        
        # 【关键】稍微暂停，防止命令在 CAD 命令行中堆叠过快导致 "未知命令" 错误
        # 0.2秒通常足够 CAD 处理完上一条指令的提示符
        time.sleep(2)

    return success_at_least_once

def attsync_block_instance_base(block_ref_obj):
    """
    【函数编号】: CMD-001
    【功能描述】: 
        对指定的属性块执行 ATTSYNC (属性同步) 操作。
        用于在修改了块定义的属性位置/格式后，强制刷新实例显示。
    
    【参数】:
        - block_ref_obj: 块引用对象 (BlockReference)。
    
    【返回值】:
        - bool: 发送成功返回 True，失败返回 False。
    """
    # 0. 尝试刷新环境 (如果 li 是全局函数)
    try: C.li() 
    except: pass

    try:
        # 1. 获取块名 (用于 ATTSYNC 参数)
        # 优先取 EffectiveName (动态块)，失败则取 Name
        block_name = None
        if hasattr(block_ref_obj, 'EffectiveName'):
            block_name = block_ref_obj.EffectiveName
        if not block_name:
            block_name = getattr(block_ref_obj, 'Name', None)

        if not block_name:
            print("[错误] 无法获取块名，跳过同步。")
            return False

        sys_logger.info(f"🔄 [同步] 正在刷新图块实例: {block_name} ...")

        # 2. 构造命令字符串 (ATTSYNC -> Name -> 块名)
        cmd_str = f"_ATTSYNC\nN\n{block_name}\n"
        
        # 3. 发送命令
        # 【优化】优先使用对象自身的 Document 属性，比全局 doc 更安全
        target_doc = getattr(block_ref_obj, 'Document', None)

        if target_doc:
            target_doc.SendCommand(cmd_str)
            return True
        else:
            # 这里的 else 对应 "not target_doc"
            # 保底方案：使用全局单例 C.doc (它会自动重连)
            C.doc.SendCommand(cmd_str)
            return True

    except Exception as e:
        sys_logger.info(f"[警告] ATTSYNC 执行失败: {e}")
        return False



#&&% 设置属性块的标签值
def set_attribute_mtext(block, tags, new_texts, keep_prefix=True, verbose=True):
    """
    set_attribute_mtext(p[0],"图纸规格","A0")
    
    set_attribute_mtext(p[0],"项目名称",["某某未来城","工业园1#"])

    notes = ["1. 尺寸单位为毫米", "2. 未注公差为IT12"]
    dotes = ["县", "城乡住房和建设局"]
    set_attribute_mtext(p[0],["建设单位名称","图纸名称"],[notes,dotes]) 

    set_attribute_mtext(p[0],["专业名称","出图比例","设计编号"], ["结构","1：20","sjy-01"], keep_prefix=True, verbose=True)

    X混搭不仅仅无效还会破坏set_attribute_mtext(p[0],"图纸规格","项目名称",["A3",["远程国际","主楼"]])

    """
    C.li()
    # --- 1. Normalize Inputs ---
    # Ensure tags is a list
    if isinstance(tags, str):
        tag_list = [tags]
        single_tag_mode = True
    else:
        tag_list = list(tags)
        single_tag_mode = False

    # Ensure new_texts matches the structure of tag_list
    text_list = []
    if single_tag_mode:
        # If single tag, new_texts is the content for that tag
        text_list = [new_texts]
    else:
        # If multiple tags, new_texts must be a list corresponding to tags
        if not isinstance(new_texts, (list, tuple)):
            # Broadcast same text to all tags
            text_list = [new_texts] * len(tag_list)
        else:
            text_list = list(new_texts)
            # Pad or truncate to match tag_list length
            if len(text_list) < len(tag_list):
                text_list.extend([text_list[-1]] * (len(tag_list) - len(text_list)))
            elif len(text_list) > len(tag_list):
                text_list = text_list[:len(tag_list)]

    # --- 2. Get Attribute Objects ---
    block = cast_object(block)
    try:
        raw_attrs = block.GetAttributes()
    except Exception as e:
        if verbose:
            sys_logger.info(f"[Error] Failed to get attributes for block ({get_attr(block, 'Handle')}): {e}")
        return {tag: False for tag in tag_list}

    # Map TagString to Attribute Object (case-insensitive for robustness)
    attr_map = {}
    for ra in raw_attrs:
        attr = cast_object(ra)
        tag_str = get_attr(attr, "TagString")
        if tag_str:
            attr_map[tag_str] = attr
            attr_map[tag_str.upper()] = attr

    result = {}

    # --- 3. Process Each Attribute ---
    for tag, content in zip(tag_list, text_list):
        attr = attr_map.get(tag) or attr_map.get(tag.upper())
        
        if attr is None:
            if verbose: sys_logger.info(f"[Warning] Attribute tag '{tag}' not found.")
            result[tag] = False
            continue

        try:
            # --- A. Prepare Text Content ---
            is_multiline_content = isinstance(content, (list, tuple))
            
            if is_multiline_content:
                # Join list elements with AutoCAD's paragraph break code "\P"
                # Ensure all elements are strings
                clean_lines = [str(line) for line in content]
                body_text = "\\P".join(clean_lines)
            else:
                body_text = str(content)

            # --- B. Handle Prefix (Formatting Codes) ---
            old_text = get_attr(attr, "TextString") or ""
            prefix = ""
            if keep_prefix and old_text:
                # Look for MText formatting end marker ';' (e.g., \W0.8; or \C1;)
                # Simple heuristic: take everything up to the first semicolon if it looks like a format code
                # A more robust check might look for specific start characters like backslash
                if old_text.startswith("\\") and ";" in old_text:
                     pos = old_text.find(";")
                     prefix = old_text[:pos + 1]
            
            final_text = prefix + body_text

            # --- C. Configure Attribute Mode (Single vs Multi-line) ---
            # If the content implies multi-line (list input or contains \P), ensure MText mode
            # Note: Checking for "\\P" in string input allows users to manually pass multi-line strings
            requires_mtext = is_multiline_content or "\\P" in body_text
            
            # Check current mode
            try:
                is_currently_mtext = get_attr(attr, "MTextAttribute")
            except:
                is_currently_mtext = False

            if requires_mtext and not is_currently_mtext:
                # Try to enable MText mode if content requires it
                if not set_attr(attr, "MTextAttribute", True):
                    if verbose: sys_logger.info(f"[Info] Could not enable MText mode for '{tag}'. Text may display on one line.")
            
            # --- D. Set Text String ---
            if set_attr(attr, "TextString", final_text):
                if verbose: 
                    display_text = final_text if len(final_text) < 20 else final_text[:17] + "..."
                    sys_logger.info(f"[Success] Set '{tag}': {display_text}")
                result[tag] = True
            else:
                if verbose: sys_logger.info(f"[Error] Failed to set TextString for '{tag}'")
                result[tag] = False

            # Update the attribute entity
            attr.Update()

        except Exception as e:
            if verbose: sys_logger.info(f"[Error] Exception setting '{tag}': {e}")
            result[tag] = False

    # Update the block reference to reflect changes
    try:
        block.Update()
    except:
        pass

    return result





#&&% 获取属性块标签及标签值
def get_block_attributes_dict(
    block_ref,
    ignore_empty: bool = False,
    upper_tag: bool = True,
):
    """
    获取块参照 block_ref 的所有属性，返回 {标签: 纯文本值} 的字典。

    特别规则：
        若属性值形如 '\\W0.8000;1#楼'，则取 ';' 后面的部分 '1#楼' 作为真实值。
        即：总是优先使用第一个分号 ';' 后面的内容作为纯文本值，
        这用于剥离 MTEXT 格式控制前缀（如宽度控制 \\W0.8000; 等）。

    参数:
        block_ref   : IAcadBlockReference 实例
        ignore_empty: True 时忽略空字符串 / 全空白值
        upper_tag   : True 时将属性标签名统一转大写作为字典 key

    返回:
        dict，如:
        {
            "项目名称": "未来城",
            "图纸名称": "1#楼",
            ...
        }
    """

    attrs_dict: dict[str, str] = {}

    if block_ref is None:
        return attrs_dict

    # 不是块参照，直接返回空
    try:
        obj_name = getattr(block_ref, "ObjectName", "")
    except Exception:
        obj_name = ""
    if "BlockReference" not in str(obj_name):
        return attrs_dict

    # 没有属性，返回空
    try:
        has_attrs = getattr(block_ref, "HasAttributes", False)
    except Exception:
        has_attrs = False
    if not has_attrs:
        return attrs_dict

    try:
        att_refs = block_ref.GetAttributes()
    except Exception:
        return attrs_dict

    # 小工具：剥离 MTEXT 前缀，取分号后面的“真实值”
    def _clean_value(val):
        """把 '\\W0.8000;1#楼' → '1#楼'；其他情况尽量保持原值。"""
        if not isinstance(val, str):
            # 非字符串就直接转成 str
            return "" if val is None else str(val)

        # 统一去掉首尾空白，避免 '\W0.8; 1#楼' 之类
        s = val.strip()

        # 只处理以 '\' 开头且包含 ';' 的情况，避免误伤正常文本里本来就有分号的
        if s.startswith("\\") and ";" in s:
            # 只切第一个分号
            _, right = s.split(";", 1)
            s = right

        # 再 strip 一遍，保证结果干净
        return s.strip()

    # 主循环：收集所有属性
    for att in att_refs:
        try:
            tag = att.TagString
            raw_val = att.TextString
        except Exception:
            continue

        if not isinstance(tag, str):
            continue

        # 标签名大小写控制
        tag_key = tag.upper() if upper_tag else tag

        # 清洗值：去掉 MTEXT 控制前缀，得到纯文本
        val = _clean_value(raw_val)

        if ignore_empty and (val is None or str(val).strip() == ""):
            continue

        attrs_dict[tag_key] = val

    return attrs_dict
#&&% 筛选出指定块名外的对象

def separate_entities_by_block_names(entities, target_names):
    """
    将实体列表分为两组：
    1. 命中组：名字在 target_names 中的块实例。
    2. 保留组：名字不在 target_names 中的块，以及所有非块对象（线、圆等）。
    
    参数:
    entities: 待处理的对象列表
    target_names: 目标块名，可以是单个字符串 "A3-H"，也可以是列表 ["A3-H", "MyBlock"]
    
    依赖:
    外部函数 get_attr(obj, name)
    
    返回:
    (kept_entities, target_blocks) 元组
    """
    
    # 1. 参数标准化：将输入转为集合(set)，提高查找速度，并兼容单字符串输入
    if isinstance(target_names, str):
        target_set = {target_names}
    else:
        # 过滤掉 None 或空值，防止报错
        target_set = set(n for n in target_names if n)

    kept_entities = []   # 存放：非目标对象（保留下来的）
    target_blocks = []   # 存放：目标块实例（被选出来的）

    for obj in entities:
        is_hit = False
        
        # 1. 安全获取对象类型
        obj_type = get_attr(obj, 'ObjectName')
        
        # 2. 只有是块引用时，才去比对名字
        if obj_type == "AcDbBlockReference":
            e_name = get_attr(obj, 'EffectiveName')
            name = get_attr(obj, 'Name')
            
            # 3. 只要 EffectiveName 或 Name 任意一个命中目标集合，就算命中
            # (处理动态块兼容性)
            if (e_name in target_set) or (name in target_set):
                is_hit = True
        
        # 4. 根据命中结果分流
        if is_hit:
            target_blocks.append(obj)
        else:
            kept_entities.append(obj)
            
    return kept_entities, target_blocks




#&&% 获取块内多段线
def huoqu_kuai_pl(blocka):#输入实体块，得到实体块中多段线矩形的坐标，其坐标以插入点的定义点为原点
    # 连接到AutoCAD
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc = acad.ActiveDocument

    kuaiming=blocka.Name

    # 获取块定义
    block_def = doc.Blocks.Item(str(kuaiming))

    # 获取块定义中的所有对象
    block_objects = list(block_def)

    # 查找三角形并删除
    for obj in block_objects:

##        print(obj.ObjectName)
        
        if obj.ObjectName == "AcDbPolyline":

            print(obj.Coordinates)





#&&&% 块定义
#定义基点的块

#&&% 创建带基点块
def create_block_with_basepoint():
    # 连接到AutoCAD
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc = acad.ActiveDocument

    # 定义块的基点位置
    base_point = vtpnt(10, 10, 0)

    # 创建一个新的块
    block = doc.Blocks.Add(base_point, "MyBlock")

    # 在块中添加一个圆形实体
    block.AddCircle(base_point, 5)

#块的添加


#&&% 创建三角形文字块
def create_block_with_triangle_and_text():
    # 连接到AutoCAD
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc = acad.ActiveDocument

    # 创建新块
    grip = vtpnt(0, 0)
    blockObj = doc.Blocks.Add(grip, "MyBlock")

    # 在块中添加三角形
    pt1 = vtpnt(0, 0, 0)
    pt2 = vtpnt(10, 0, 0)
    pt3 = vtpnt(5, 10, 0)
    blockObj.AddLine(pt1, pt2)
    blockObj.AddLine(pt2, pt3)
    blockObj.AddLine(pt3, pt1)

    # 在块中添加文字对象
    text_point = vtpnt(2, 2, 0)
    blockObj.AddText("太美了", text_point, 2)

    print("块 'MyBlock' 创建成功")



def huoqu_kuai_pl(blocka):
    # 连接到AutoCAD
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc = acad.ActiveDocument

    kuaiming=blocka.Name

    # 获取块定义
    block_def = doc.Blocks.Item(str(kuaiming))

    # 获取块定义中的所有对象
    block_objects = list(block_def)

    # 查找三角形并删除
    for obj in block_objects:

        print(obj.ObjectName)
        if obj.ObjectName == "AcDbPolyline":

            print(obj.Coordinates)

    

# 块的边界

#&&% 获取块包围盒
def get_bounding_box_of_block(block_name):
    # 连接到AutoCAD
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc = acad.ActiveDocument

    # 获取块定义
    block_def = doc.Blocks.Item(block_name)

    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

    # 遍历块定义中的所有对象
    for obj in block_def:
        try:
            # 尝试获取对象的边界框
            lower_left, upper_right = obj.GetBoundingBox()
            
            min_x = min(min_x, lower_left[0])
            min_y = min(min_y, lower_left[1])
            min_z = min(min_z, lower_left[2])
            
            max_x = max(max_x, upper_right[0])
            max_y = max(max_y, upper_right[1])
            max_z = max(max_z, upper_right[2])
        except:
            pass

    return ((min_x, min_y, min_z), (max_x, max_y, max_z))


#&&% 创建含插入和直线的块
def create_new_block_with_insert_and_line():
    # 连接到AutoCAD
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc = acad.ActiveDocument

    # 检查块名称"块1"是否已经存在
    if "块3" in [blk.Name for blk in doc.Blocks]:
        print("块名称'块3'已经存在。请选择一个新的名称或删除现有的块。")
        return

    # 创建新块的插入点
    grip = vtpnt(0, 0, 0)
    blockObj1 = doc.Blocks.Add(grip, "块3")

    # 在块1中插入MyBlock块
    insertion_point_for_myblock = vtpnt(10, 10, 0)
    blockObj1.InsertBlock(insertion_point_for_myblock, "MyBlock", 1, 1, 1, 0)

    # 在块1中添加一根直线段
    start_point = vtpnt(0, 0, 0)
    end_point = vtpnt(50, 50, 0)
    blockObj1.AddLine(start_point, end_point)

    print("块1已创建并添加了MyBlock和直线段")


    
#&&% 复制并移动图层块
def copy_and_move_blocks_from_layer(layer_name, block_prefix):
    
        
    # 使用select_tuceng函数选择指定图层上的所有对象
    all_objects = select_tuceng(layer_name)
    
    # 过滤出块对象，且块名的前两个字母与指定的前缀匹配
    blocks = [obj for obj in all_objects if obj.ObjectName == "AcDbBlockReference" and obj.Name[:2] == block_prefix]
    
    # 定义移动的起始点和结束点
    vtpnt_from = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0, 0, 0])
    vtpnt_to = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0, 2000000, 0])
    
    # 对每个块进行复制和移动操作
    for block in blocks:
        # 复制块
        copied_block = block.Copy()
        
        # 移动复制的块
        copied_block.Move(vtpnt_from, vtpnt_to)

    sys_logger.info(f"Copied and moved {len(blocks)} blocks from layer {layer_name} with prefix {block_prefix}.")

#块名的清除

#&&&% 删除指定块名的实例及块

#&&% 旧版
def delete_block_instances_and_definition_retry(target_block_name, max_rounds=3):
    """
    删除指定名称的块实例和块定义，带重试机制。
    """
    _, doc = get_acad_doc()
    if not doc:
        print("❌ 无法获取 AutoCAD 文档对象")
        return

    sys_logger.info(f"\n🚀 开始清理块: [{target_block_name}] (最大尝试 {max_rounds} 轮)")

    for round_idx in range(1, max_rounds + 1):
        sys_logger.info(f"--- 第 {round_idx} 轮清理 ---")
        
        # 1. 获取所有块实例
        # 注意：select_kuai 返回的是所有 INSERT，我们需要自己筛选
        all_blocks = select_kuai(max_retries=3)
        
        # 2. 筛选出目标块
        target_instances = []
        for b in all_blocks:
            # 比较名称（忽略大小写）
            if get_block_name(b).upper() == target_block_name.upper():
                target_instances.append(b)
        
        count = len(target_instances)
        
        # 3. 验证与删除实例
        if count == 0:
            sys_logger.info(f"✅ 第 {round_idx} 轮检测：未发现块实例 [{target_block_name}]")
        else:
            sys_logger.info(f"🔨 发现 {count} 个实例，正在删除...")
            for obj in target_instances:
                safe_delete(obj)
            
            # 删除后简单验证一下，虽然下一轮循环会再次全面检查
            sys_logger.info(f"   已执行删除命令。")

        # 4. 尝试删除块定义 (Purge)
        # 只有当实例数为0（或刚删完）时，才尝试删定义
        definition_deleted = False
        try:
            # 从块表中获取块定义
            blk_def = doc.Blocks.Item(target_block_name)
            blk_def.Delete()
            sys_logger.info(f"🗑️ 块定义 [{target_block_name}] 已从块表中移除。")
            definition_deleted = True
        except Exception as e:
            # 常见错误：eKeyNotFound(块不存在), eBoInUse(还有实例或被嵌套)
            msg = str(e)
            if "eKeyNotFound" in msg:
                sys_logger.info(f"ℹ️ 块定义 [{target_block_name}] 已不存在。")
                definition_deleted = True # 视为成功
            elif "eBoInUse" in msg:
                sys_logger.info(f"⚠️ 无法删除定义：块仍被使用（可能被嵌套在其他块中）。")
            else:
                pass # 其他错误忽略

        # 5. 最终判定：如果没实例了，且定义也没了(或本就不存在)，则成功退出
        if count == 0 and definition_deleted:
            sys_logger.info(f"✨ 彻底清理完成：[{target_block_name}]")
            return True
        
        # 如果还有问题，等待一小会儿进入下一轮
        if round_idx < max_rounds:
            time.sleep(1)

    sys_logger.info(f"❌ 经过 {max_rounds} 轮尝试，未能彻底清除（可能是嵌套块导致）。")
    return False

#&&% 极速清理

def delete_block_instances_and_definition_optimized(target_name, max_retries=5):
    """
    【函数编号】: CLEAN-ROBUST-V34 (核验版)
    【功能】: 
        删除指定图块的实例和定义。
        核心改进：增加【块表反查】。不仅要实例删光，还要确认 Block Table 里彻底查无此人。
    """
    doc = C.doc
    
    # 0. 先预检：如果块表里压根没有，直接返回成功，省得费劲
    try:
        doc.Blocks.Item(target_name)
    except:
        # sys_logger.info(f"ℹ️ [预检] {target_name} 根本不存在，无需清理。")
        return True

    for attempt in range(1, max_retries + 1):
        try:
            # ====================================================
            # 阶段 A: 清理实例 (Model Space) - 过滤器极速版
            # ====================================================
            ss_name = "RobustDelete_SS"
            try: doc.SelectionSets.Item(ss_name).Delete()
            except: pass
            ss = doc.SelectionSets.Add(ss_name)
            
            p_filter_type = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I2, [0, 2])
            p_filter_data = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, ["INSERT", target_name])
            
            ss.Select(5, None, None, p_filter_type, p_filter_data) # 5=All
            
            if ss.Count > 0:
                ss.Erase() # 删除
                # 【关键】等待操作完成
                wait_command_done()
            
            ss.Delete()

            # ====================================================
            # 阶段 B: 清理定义 (Blocks Table)
            # ====================================================
            try:
                blk_def = doc.Blocks.Item(target_name)
                blk_def.Delete()
            except:
                # 这里报错很正常（比如被嵌套引用），先不管，下面统一验尸
                pass

            # ====================================================
            # 阶段 C: 【核心】块表反查验尸
            # ====================================================
            # 无论刚才有没有报错，我现在去查户口。
            # 如果还能查到，说明没死透；如果报错，说明彻底没了。
            try:
                # 尝试再次获取
                _ = doc.Blocks.Item(target_name)
                
                # 🔴 还能获取到？说明清理失败！
                # sys_logger.info(f"   ⚠️ 第 {attempt} 轮：[{target_name}] 定义仍存活 (可能被嵌套)。重试中...")
                
                # 强制刷新，试图断开引用锁
                if attempt % 2 == 0: # 偶数轮次尝试 Regen
                    doc.Regen(1)
                
                time.sleep(0.5)
                continue # 进入下一轮循环
                
            except Exception:
                # 🟢 报错了？说明 Block Table 里没有这个 key 了！
                sys_logger.info(f"🗑️ [清理成功] {target_name} 已彻底根除。")
                return True

        except Exception as e:
            sys_logger.info(f"   ⚠️ 异常: {e}")
            time.sleep(0.5)
            
    # 如果跑完循环还在
    sys_logger.info(f"❌ [清理失败] {target_name} 顽固残留 (检查是否被其他块嵌套引用)。")
    return False

#&&% 再次优化

def delete_block_instances_and_definition_optimized(target_name, max_retries=5):
    """
    【最终推荐版】
    利用选择集极速清理实例，利用验尸逻辑清理定义。
    """
    doc = C.doc
    
    # 0. 预检：如果块表里压根没有，直接返回成功
    try:
        doc.Blocks.Item(target_name)
    except Exception:
        # 查无此人，直接通过
        return True

    sys_logger.info(f"🚀 [极速清理] 开始移除: {target_name}")

    for attempt in range(1, max_retries + 1):
        try:
            # ====================================================
            # 阶段 A: 清理实例 (Model Space) - 过滤器极速版
            # ====================================================
            ss_name = "Clean_Temp_SS"
            
            # 【安全逻辑】先删再建，防止上次崩了残留
            try: doc.SelectionSets.Item(ss_name).Delete()
            except: pass
            
            ss = doc.SelectionSets.Add(ss_name)
            
            # 构建过滤器：只选 块参照(INSERT) 且 块名(2)=target_name
            # 注意：win32com 需要用 VARIANT 包装数组
            p_filter_type = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I2, [0, 2])
            p_filter_data = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, ["INSERT", target_name])
            
            # acSelectionSetAll = 5 (全图搜索，包含屏幕外的)
            ss.Select(5, None, None, p_filter_type, p_filter_data) 
            
            count = ss.Count
            if count > 0:
                ss.Erase() # 极速删除
                sys_logger.info(f"  🔨 第 {attempt} 轮：已销毁 {count} 个实例引用。")
            
            # 用完即删，保持卫生
            ss.Delete() 

            # ====================================================
            # 阶段 B: 清理定义 (Blocks Table)
            # ====================================================
            try:
                blk_def = doc.Blocks.Item(target_name)
                blk_def.Delete()
            except Exception:
                # 这里如果报错，通常是因为有嵌套引用，或者已经删掉了
                # 不要在这里做判断，去阶段 C 统一验证
                pass

            # ====================================================
            # 阶段 C: 【核心】块表反查验尸
            # ====================================================
            try:
                # 再次尝试获取，如果还能拿到，说明没死透
                _ = doc.Blocks.Item(target_name)
                
                # 🔴 还能活着走到这一步，说明清理失败
                # sys_logger.warning(f"  ⚠️ 定义仍存活，尝试强制刷新...")
                
                # 只有在删除失败时才重生成，节省时间
                doc.Regen(1) 
                time.sleep(0.5) # 给 CAD 喘息时间
                
            except Exception:
                # 🟢 触发异常 = 真的没了 = 成功
                sys_logger.info(f"✨ [清理成功] {target_name} 已根除。")
                return True

        except Exception as e:
            sys_logger.error(f"  ❌ 清理过程异常: {e}")
            time.sleep(1)
            
    # 如果跑完所有重试次数还在
    sys_logger.error(f"💀 [清理失败] {target_name} 可能是嵌套块或被锁定。")
    return False



#&&% 重命名块实体
def rename_block_entity(ent, new_name):
    """
    将给定块参照实体 ent 的块名改为 new_name。
    如果 new_name 在 Block 表中已存在，则该实体将指向已有定义；
    否则将重命名它当前所引用的块定义。
    
    参数：
      ent       -- 一个 COM 块参照对象（如 BlockReference）
      new_name  -- 目标块名（字符串）
    """
    # 获取当前文档和块表

    blocks = doc.Blocks
    old_name = ent.Name

    try:
        # 尝试查找 new_name 是否已存在
        blocks.Item(new_name)
        # 存在：直接让该实体引用此定义
        ent.Name = new_name
    except Exception:
        # 不存在：重命名它当前所引用的定义
        blk_def = blocks.Item(old_name)
        blk_def.Name = new_name
#&&&% 块查询

#&&% 由块名选择实例

def get_block_instances(block_name: str, max_retries: int = 5):
    """
    根据给定的块定义名，检索当前图形中所有对应的块参照实例（BlockReference），
    返回这些 COM 对象的列表。

    参数：
      block_name     – 块定义的名称（字符串），如 "MyBlock"
      max_retries    – 调用 select_kuai 时的最大重试次数

    返回：
      instances     – 包含所有匹配块参照的列表（如果未找到或者出错，返回空列表）
    """
    # ① 先调用 select_kuai() 拿到所有块实例 COM 对象（扁平列表）
    try:
        all_blocks = select_kuai(max_retries)
    except Exception as e:
        sys_logger.info(f"[错误] 调用 select_kuai 失败：{e}")
        return []

    instances = []
    # ② select_kuai 已经是所有块实例的列表，直接遍历
    for ent in all_blocks:
        try:
            # 对于块参照，EntityName 通常是 "AcDbBlockReference"
            # 且我们要筛选 Name 恰好等于 block_name 的那些
            if getattr(ent, "EntityName", "") == "AcDbBlockReference" and getattr(ent, "Name", "") == block_name:
                instances.append(ent)
        except Exception:
            # 如果某个 COM 对象没有 EntityName/Name 属性，就跳过
            continue

    sys_logger.info(f"选择到名为{block_name}的实例块{len(instances)}个")

    return instances



#&&% 从块实体对象获取其内部com对象

#&&% 获取块引用实体
def get_entities_from_block_reference(block_ref):
    """
    获取块引用对象中的所有子实体（COM对象形式）。

    参数：
        block_ref: 块引用对象（AcDbBlockReference）
        doc: 当前 AutoCAD 文档对象（Document）

    返回：
        entities: 子实体列表
    """
    try:
        block_name = block_ref.EffectiveName
        block_def = doc.Blocks.Item(block_name)
        entities = [ent for ent in block_def]
        sys_logger.info(f"[OK] 获取到 {len(entities)} 个子对象")
        return entities
    except Exception as e:
        sys_logger.info(f"[错误] 获取失败：{e}")
        return []

    




#以块的方式插入文件
#&&&% 块插入

#&&% 插入块到CAD
def insert_block_into_autocad(block_file_path, insertion_point=(0, 0, 0), scale=(1, 1, 1), rotation=0):
    """
    以块的方式插入 DWG 文件到 AutoCAD 中

    :param block_file_path: 块文件的路径，通常为 DWG 文件路径
    :param insertion_point: 插入位置的三元组 (x, y, z)
    :param scale: 块的缩放比例三元组 (sx, sy, sz)
    :param rotation: 块的旋转角度（弧度）
    """
    try:

        # 定义块插入点
        insertion_point = (insertion_point[0], insertion_point[1], insertion_point[2])

        # 插入块，使用 InsertBlock 方法
        block = ms.InsertBlock(insertion_point, block_file_path, scale[0], scale[1], scale[2], rotation)

        sys_logger.info(f"[OK] 块已插入，文件：{block_file_path}，插入点：{insertion_point}，缩放：{scale}，旋转角度：{rotation}")

    except Exception as e:
        sys_logger.info(f"[错误] 插入块时出错：{e}")



#不炸开

#&&% 插入标准块
def insert_standard_block(block_dwg,
                          insertion_point=(0, 0, 0),
                          scale=(1, 1, 1),
                          rotation=0,
                          wait=0.3):
    """
    不炸开，
    全程无交互对话框。

    block_dwg: 标准块 DWG 路径
    insertion_point: (x,y,z)
    scale: (sx,sy,sz)
    rotation: 旋转角度（度）
    """
    before = select_kuai()
    before_handles = {b.Handle for b in before}


    if not os.path.isfile(block_dwg):
        raise FileNotFoundError(block_dwg)

    # 准备参数
    x, y, z    = insertion_point
    sx, sy, sz = scale
    path       = os.path.abspath(block_dwg).replace("\\", "/")

    # 1) 插入块
    insert_cmd = (
        "-INSERT\n"
        f"\"{path}\"\n"    # 文件路径要加双引号
        f"{x},{y},{z}\n"
        f"{sx}\n"
        f"{sy}\n"
        f"{sz}\n"
        f"{rotation}\n"
    )
    doc.SendCommand(insert_cmd)
    time.sleep(wait)

    doc.SendCommand("RE\n")
    doc.SendCommand("Z\nE\n")
    time.sleep(wait)

    after = select_kuai()
    new_refs = [b for b in after if b.Handle not in before_handles]
    if not new_refs:
        print("[警告] 未检测到任何新插入的块引用")
        return []

    results = []
    for blk in new_refs:
        # 5. 先将它旋转归零
        try:
            blk.Rotation = 0
        except Exception:
            pass

        # 7. 取它的包围盒四角
        p1, p2 = blk.GetBoundingBox()
        minx, miny, minz = p1
        maxx, maxy, maxz = p2
        corners = [
            (minx, miny, minz),  # 左下
            (minx, maxy, minz),  # 左上
            (maxx, maxy, minz),  # 右上
            (maxx, miny, minz),  # 右下
        ]

        results.append((blk, corners))

    return results


#炸开


#&&% 插入并炸开DWG
def insert_and_explode_dwg(block_dwg,
                           insertion_point=(0, 0, 0),
                           scale=(1, 1, 1),
                           rotation=0,
                           wait=0.3):
    """
    将一个 WBLOCK 导出的标准块 DWG 插入到当前图，
    并立即 EXPLODE 成普通图元（不保留块引用）。

    参数:
        block_dwg: 标准块 DWG 路径
        insertion_point: 插入点 (x,y,z)
        scale: (sx,sy,sz)
        rotation: 旋转角度（度）
        wait: 每步命令后等待秒数
    """

    before = select_kuai()
    before_handles = {b.Handle for b in before}

    if not os.path.isfile(block_dwg):
        raise FileNotFoundError(block_dwg)

    # 准备参数
    x, y, z    = insertion_point
    sx, sy, sz = scale
    path       = os.path.abspath(block_dwg).replace("\\", "/")

    # 1) 插入块
    insert_cmd = (
        "-INSERT\n"
        f"\"{path}\"\n"    # 文件路径要加双引号
        f"{x},{y},{z}\n"
        f"{sx}\n"
        f"{sy}\n"
        f"{sz}\n"
        f"{rotation}\n"
    )
    doc.SendCommand(insert_cmd)
    time.sleep(wait)

    doc.SendCommand("RE\n")
    doc.SendCommand("Z\nE\n")
    time.sleep(wait)

    # 2) EXPLODE “Last”   （炸开最新插入的块引用）
    explode_cmd = (
        "EXPLODE\n"
        "L\n"    # Last
        "\n"     # 完成选择
    )
    doc.SendCommand(explode_cmd)
    time.sleep(wait)

    sys_logger.info(f"[OK] 已插入并炸开：{os.path.basename(path)} @ ({x},{y},{z})")

    after = select_kuai()
    new_refs = [b for b in after if b.Handle not in before_handles]
    if not new_refs:
        print("[警告] 未检测到任何新插入的块引用")
        return []

    results = []
    for blk in new_refs:
        # 5. 先将它旋转归零（容错，不成功就算了）
        try:
            blk.Rotation = 0
        except Exception:
            pass

        # 7. 取它的包围盒四角（加上 safe_get_bbox 防 CAD 忙）
        try:
            p1, p2 = safe_get_bbox(blk)
        except Exception as e:
            sys_logger.info(f"[警告] 获取块 {getattr(blk, 'Name', '?')} 外包盒失败：{e}")
            continue

        minx, miny, minz = p1
        maxx, maxy, maxz = p2
        corners = [
            (minx, miny, minz),  # 左下
            (minx, maxy, minz),  # 左上
            (maxx, maxy, minz),  # 右上
            (maxx, miny, minz),  # 右下
        ]

        results.append((blk, corners))

    # 兼容你当前调用方式：返回 (列表, 最后一个块)
    return results, blk if results else ([], None)


#&&% 新版本性能测试0109

@retry_on_busy
def insert_and_explode_dwg(
        block_dwg,
        insertion_point=(0, 0, 0),
        scale=(1, 1, 1),
        rotation=0,
        wait=0.3
    ):
    """
    【V3.0 重构版】插入并炸开 DWG
    
    改进点：
    1. 使用 CADGuard 保护 Insert 和 Explode 操作，防止死锁。
    2. 使用 SafeCOM 获取包围盒，增强稳定性。
    3. 保持原有返回格式，无缝兼容。
    """
    sys_logger.info(f"=====================确认insert_and_explode_dwg版本20260115=====================")    
    
    # 1. 参数与环境检查
    if not os.path.isfile(block_dwg):
        sys_logger.info(f"❌ 文件未找到: {block_dwg}")
        return [], None

    # 刷新一下，确保选择集最新
    # C.doc.SendCommand("RE\n") 
    
    # 2. 记录插入前的状态 (Snapshot)
    before = select_kuai() or []
    before_handles = {b.Handle for b in before}

    # 3. 准备参数
    x, y, z = insertion_point
    sx, sy, sz = scale
    path = os.path.abspath(block_dwg).replace("\\", "/")
    fname = os.path.basename(path)

    # 4. 执行插入 (关键操作，加卫士保护)
    # wait_after=True 确保插入动作完成后，CAD 恢复空闲才继续
    with CADGuard(f"插入-{fname}", wait_after=True):
        insert_cmd = (
            f"-INSERT\n"
            f"\"{path}\"\n"
            f"{x},{y},{z}\n"
            f"{sx}\n{sy}\n{sz}\n"
            f"{rotation}\n"
        )
        C.doc.SendCommand(insert_cmd)

    # 5. 视图调整 (防止炸开时对象在屏幕外报错)
    # with CADGuard("缩放范围"):
    #     C.doc.SendCommand("Z\nE\n") 

    # 6. 执行炸开 (Explode Last)
    with CADGuard(f"炸开-{fname}", wait_after=True):
        # 选中刚插入的块 (Last) 并炸开
        C.doc.SendCommand("EXPLODE\nL\n\n")

    sys_logger.info(f"✅ [OK] 已插入并炸开：{fname} @ ({x},{y},{z})")

    # 7. 捕获新对象 (Diff)
    # C.doc.SendCommand("RE\n") # 刷新数据库
    after = select_kuai() or []
    
    # 筛选出新增加的块引用 (即炸开后释放出来的那些)
    new_refs = [b for b in after if b.Handle not in before_handles]

    if not new_refs:
        print("⚠️ [警告] 炸开后未检测到新的块引用")
        return [], None

    # 8. 提取几何信息 (包围盒计算)
    results = []
    for blk in new_refs:
        # 8.1 归零旋转 (容错处理)
        try:
            if getattr(blk, "Rotation", 0) != 0:
                blk.Rotation = 0
        except: pass

        # 8.2 获取包围盒 (使用 SafeCOM 防止偶尔的 RPC 拒绝)
        try:
            # SafeCOM.call 会自动重试 GetBoundingBox
            p1, p2 = SafeCOM.call(blk.GetBoundingBox)
            minx, miny, minz = p1
            maxx, maxy, maxz = p2
            corners = [
                (minx, miny, minz), # 左下
                (minx, maxy, minz), # 左上
                (maxx, maxy, minz), # 右上
                (maxx, miny, minz), # 右下
            ]
            results.append((blk, corners))
        except Exception as e:
            sys_logger.info(f"⚠️ 无法获取块 {getattr(blk, 'Name', '?')} 包围盒: {e}")
            continue

    # 9. 返回结果
    # 兼容旧接口：返回 (列表, 最后一个块对象)
    last_blk = results[-1][0] if results else None
    return results, last_blk



#&&% 获取面积足够大的全部非同名块实例

#&&% 获取大块实例
def get_large_block_instances(
    area_threshold: float,
    tol: float = 100.0,
    max_retries: int = 5
) -> list:
    """
    获取模型空间中所有块实例，筛选出“包围盒面积大于 area_threshold” 的块，
    并按面积去重：如果两个块的面积差值小于 tol，则只保留其中一个。
    返回一个按出现顺序去重后的 COM 对象列表。

    :param area_threshold: 面积阈值（单位与 CAD 坐标相同，例如以平方图纸单位计）。
    :param tol:            面积去重的容差值（默认 100），若两个块面积差小于 tol，视为同一块。
    :param max_retries:    调用 select_kuai 时的最大重试次数，默认 5 次。
    :return:               包含所有“面积 > area_threshold”且去重后的块引用 COM 对象列表，
                          如果 select_kuai 调用失败，会返回空列表。
    """
    # ① 调用 select_kuai，每隔 max_retries 次重连一次
    try:
        all_blocks = select_kuai(max_retries)
    except Exception as e:
        sys_logger.info(f"[错误] 调用 select_kuai 失败：{e}")
        return []

    # 临时列表，用于收集已加入结果的块面积（用于去重）
    seen_areas = []
    large_blocks = []

    for blk in all_blocks:
        try:
            # GetBoundingBox 返回 (ll_point, ur_point)
            ll_point, ur_point = blk.GetBoundingBox()
            x1, y1, _ = ll_point
            x2, y2, _ = ur_point
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            area = width * height
        except Exception:
            # 如果某些块无法获取包围盒，则跳过
            continue

        # 面积判断
        if area > area_threshold:
            # 检查当前 area 是否已近似出现在 seen_areas 中
            duplicate = False
            for existing_area in seen_areas:
                if abs(area - existing_area) < tol:
                    duplicate = True
                    break

            if not duplicate:
                seen_areas.append(area)
                large_blocks.append(blk)

    return large_blocks

#从com对象中，根据其外包盒的矩形的长边与短边的比值和面积在160000000到1000000000两个条件筛算

#&&% 确定合乎标准打印要求的自建多段线区域

def get_large_block_instances_with_tolerance(max_retries: int = 5, area_threshold: float = 70 ):
    """
    获取当前 DWG 中所有大尺寸块实例
    A3 1:100的正常值> 1240000000.000000
   
    """
    # ① 尝试获取所有块实例
    try:
        all_blocks = select_kuai(max_retries)
    except Exception as e:
        sys_logger.info(f"[错误] 调用 select_kuai 失败：{e}")
        return []

    # ② 先筛选面积 >= area_threshold 的块
    LB = []
    for blk in all_blocks:
        try:
            ll_point, ur_point = blk.GetBoundingBox()
            x1, y1, _ = ll_point
            x2, y2, _ = ur_point
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            area = width * height
        except Exception:
            # 读取包围盒失败，跳过
            continue

        if area >= area_threshold:
            # 附带面积信息，便于后续比较
            LB.append((blk, area))

    return LC




#&&% 块内坐标转换成世界坐标（适合平面上的一般块）

def transform_point_by_block(block_ref, local_pt):
    """
    将块内部坐标 local_pt = (lx, ly, lz) 转换为世界坐标：
      1. 按 block_ref 的比例缩放 (XScaleFactor, YScaleFactor, ZScaleFactor)
      2. 按 block_ref.Rotation 旋转（绕 Z 轴，弧度制）
      3. 平移到 block_ref.InsertionPoint = (ix, iy, iz)

    返回 (wx, wy, wz)：
      wx = ix + (lx * sx * cosθ - ly * sy * sinθ)
      wy = iy + (lx * sx * sinθ + ly * sy * cosθ)
      wz = iz + (lz * sz)
    """
    ix, iy, iz = block_ref.InsertionPoint
    sx = block_ref.XScaleFactor
    sy = block_ref.YScaleFactor
    sz = block_ref.ZScaleFactor
    theta = block_ref.Rotation  # 单位：弧度

    lx, ly, lz = local_pt
    # 缩放后再旋转
    x_scaled = lx * sx
    y_scaled = ly * sy

    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    xr = x_scaled * cos_t - y_scaled * sin_t
    yr = x_scaled * sin_t + y_scaled * cos_t
    zr = lz * sz

    wx = ix + xr
    wy = iy + yr
    wz = iz + zr
    return (wx, wy, wz)


#&&% 按名称选择块
def select_block_by_name(block_name: str, max_retries: int = 5):
    """
    从 *模型空间* 快速选出指定块名的所有实例，返回实体列表。
    不遍历 ModelSpace，速度与 SelectionSet 相同量级。
    """
    t0, last_exc = time.time(), None

    for attempt in range(1, max_retries + 1):
        try:
            # 1) 删旧选择集
            with suppress(Exception):
                doc.SelectionSets.Item("SS_block_by_name").Delete()

            # 2) 新建选择集
            ss = doc.SelectionSets.Add("SS_block_by_name")

            # 3) 过滤器：0=INSERT, 2=块名, 410=布局名"Model"
            filterType  = vtInt([0, 2, 410])
            filterData  = vtVariant(["INSERT", block_name, "Model"])

            # acSelectionSetAll = 5
            ss.Select(5, 0, 0, filterType, filterData)

            lb = list(ss)
            sys_logger.info(f"[OK] 选到 {len(lb)} 个 “{block_name}”（{time.time() - t0:.3f}s，第{attempt}次）")
            return lb

        except Exception as e:
            last_exc = e
            sys_logger.info(f"[警告] 第 {attempt} 次失败：{e!r}")
            time.sleep(0.3)

    sys_logger.info(f"[错误] {max_retries} 次仍失败：{last_exc!r}")
    return []
#&&&% 块管理

#&&% 获取所有块定义
def get_all_block_definitions(max_retry: int = 3, quiet: bool = False):
    """
    返回当前 DWG 中所有块定义（BlockTableRecord）对象列表。

    实现策略：
    - 使用全局 li() / doc，不再重复 Dispatch
    - 使用 doc.Blocks.Item(i) 按索引获取，避免枚举器在 CAD 忙时抛 “应用程序正在使用中”
    - 对整个获取过程做最多 max_retry 次重试，若仍失败则返回当时已经获取到的部分列表

    参数:
        max_retry : 失败时最多重试次数（默认 3）
        quiet     : 是否静默，不打印警告信息

    返回:
        list[COM block object]
    """
    import time
    import pythoncom
    from contextlib import suppress

    global acad, doc, mp, sp

    def log(msg):
        if not quiet:
            print(msg)

    if not li():
        raise RuntimeError("get_all_block_definitions: li() 连接失败，无法获取当前 DWG。")

    blocks = []

    for attempt in range(1, max_retry + 1):
        blocks.clear()
        try:
            count = doc.Blocks.Count
        except pythoncom.com_error as e:
            # 可能是应用程序忙
            log(f"[警告] 获取 Blocks.Count 失败（第 {attempt} 次）：{e}")
            pythoncom.PumpWaitingMessages()
            time.sleep(0.2)
            continue

        try:
            for i in range(count):
                with suppress(Exception):
                    blk = doc.Blocks.Item(i)
                    blocks.append(blk)
            # 成功跑完一轮，直接返回
            return blocks
        except pythoncom.com_error as e:
            log(f"[警告] 遍历 Blocks 时出错（第 {attempt} 次）：{e}")
            pythoncom.PumpWaitingMessages()
            time.sleep(0.2)
            continue

    # 多次重试仍不完全成功，返回当前已经拿到的部分
    log(f"[警告] get_all_block_definitions 多次重试后仍存在问题，返回部分块定义，数量={len(blocks)}")
    return blocks


#&&% 获取所有块名
def get_all_block_names():
    """
    使用全局 li()/doc 获取当前 DWG 中所有块定义的名字列表。
    """
    import pythoncom

    blocks = get_all_block_definitions(quiet=True)
    names = []
    for blk in blocks:
        try:
            names.append(str(blk.Name))
        except pythoncom.com_error:
            continue
        except Exception:
            continue
    return names

#&&% 块清理

def purge_block(block_name: str, quiet: bool = False):
    """
    删除指定块的所有实例，并彻底清除该块定义。
    
    步骤：
      1. 在模型空间删除所有同名 INSERT 实例
      2. 在每个布局的 Block (PaperSpace) 删除所有同名 INSERT 实例
      3. 调用 PurgeAll() 清理未用定义
      4. 再次尝试删除块定义
    
    :param block_name: 要清理的块名称（区分大小写）
    :param quiet: True 则不打印过程信息
    """
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc  = acad.ActiveDocument

    # --- 1) 模型空间 ---
    removed = 0
    for ent in list(doc.ModelSpace):
        if ent.ObjectName in ("AcDbBlockReference", "AcDbMInsertBlock") and getattr(ent, "Name", "") == block_name:
            with suppress(Exception):
                ent.Delete()
                removed += 1

    # --- 2) 各布局块空间（PaperSpace） ---
    for layout in doc.Layouts:
        with suppress(Exception):
            block_space = layout.Block
            for ent in list(block_space):
                if ent.ObjectName in ("AcDbBlockReference", "AcDbMInsertBlock") and getattr(ent, "Name", "") == block_name:
                    with suppress(Exception):
                        ent.Delete()
                        removed += 1

    time.sleep(0.2)
    if not quiet:
        sys_logger.info(f"ℹ 共删除 {removed} 个 “{block_name}” 实例")

    # --- 3) PurgeAll 清理所有未被引用的定义 ---
    with suppress(Exception):
        doc.PurgeAll()
        if not quiet:
            print("[OK] PurgeAll 清理未用定义")

    # --- 4) 删除块定义 ---
    try:
        blk = doc.Blocks.Item(block_name)
        blk.Delete()
        if not quiet:
            sys_logger.info(f"[OK] 已删除块定义：{block_name}")
    except Exception as e:
        if not quiet:
            sys_logger.info(f"[警告] 删除块定义失败（仍有隐性引用？）：{e}")

    if not quiet:
        sys_logger.info(f"ℹ 完成对 '{block_name}' 的清理。")

#&&% 清理未使用块
def purge_unused_blocks(quiet: bool = False):
    """
    一次性清除所有未被任何 INSERT 实例引用的块定义。
    速度快、可靠性高（不用逐个 SelectionSet 检测）。
    """
    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    doc  = acad.ActiveDocument

    # 1) 记录清理前的块名列表
    before = []
    for i in range(doc.Blocks.Count):
        with suppress(Exception):
            name = doc.Blocks.Item(i).Name
            before.append(name)

    # 2) 调用 PurgeAll 一次性清理
    t0 = time.time()
    with suppress(Exception):
        doc.PurgeAll()
    t1 = time.time()

    # 3) 记录清理后的块名列表
    after = []
    for i in range(doc.Blocks.Count):
        with suppress(Exception):
            name = doc.Blocks.Item(i).Name
            after.append(name)

    # 4) 计算差集
    removed = [name for name in before if name not in after]

    if not quiet:
        sys_logger.info(f"[OK] PurgeAll 清理完成，耗时 {t1 - t0:.3f}s")
        sys_logger.info(f"ℹ 共移除 {len(removed)} 个未使用块：")
        for nm in removed:
            print("   ·", nm)

    return removed



@debuggable
#&&% 清理块1
def purge_block_1(block_name: str, quiet: bool = False, max_delete_attempts: int = 2):
    """
    删除指定块的所有实例，并尽可能彻底清除该块定义。
    
    步骤：
      1. 在 *Model_Space / *Paper_Space 和其它块定义中删除所有同名 INSERT 实例
      2. 调用 PurgeAll() 清理未用定义
      3. 多次尝试删除块定义
      4. 如果仍然失败，将块名改为 lajikuai_时间戳_N，避免后续块名污染

    :param block_name: 要清理的块名称（区分大小写）
    :param quiet: True 则不打印过程信息
    :param max_delete_attempts: Delete 块定义的最大尝试次数
    """
    import time
    import pythoncom

    from datetime import datetime

    global acad, doc, mp, sp

    def log(msg):
        if not quiet:
            print(msg)

    # 小工具：判断是否块参照
    def is_block_ref(ent) -> bool:
        try:
            on = getattr(ent, "ObjectName", "")
        except Exception:
            return False
        return on in ("AcDbBlockReference", "AcDbMInsertBlock")

    # 小工具：生成垃圾块名
    def make_trash_name(base_prefix: str = "lajikuai", idx: int = 1) -> str:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{base_prefix}_{ts}_{idx}"

    node("▶ PB0  purge_block：开始清理块 '{}'", block_name)

    # 0) 确保连接的是当前激活 DWG
    if not li():
        log(f"[错误] li() 连接失败，无法清理块 {block_name}")
        return

    # 1) 在所有块空间中删除该块的 INSERT 实例
    removed = 0

    # 1.1 模型空间
    with suppress(Exception):
        for ent in list(doc.ModelSpace):
            if is_block_ref(ent) and getattr(ent, "Name", "") == block_name:
                with suppress(Exception):
                    ent.Delete()
                    removed += 1

    # 1.2 所有布局的 Block（包括 PaperSpace）
    for layout in doc.Layouts:
        with suppress(Exception):
            block_space = layout.Block
            for ent in list(block_space):
                if is_block_ref(ent) and getattr(ent, "Name", "") == block_name:
                    with suppress(Exception):
                        ent.Delete()
                        removed += 1

    # 1.3 其它块定义内部的嵌套引用（避免“块中块”暗搓搓引用）
    for blk_def in doc.Blocks:
        with suppress(Exception):
            for ent in list(blk_def):
                if is_block_ref(ent) and getattr(ent, "Name", "") == block_name:
                    with suppress(Exception):
                        ent.Delete()
                        removed += 1

    if not quiet:
        log(f"ℹ 共删除 {removed} 个 “{block_name}” 实例（含模型/图纸/块内部）")

    time.sleep(0.1)

    # 2) PurgeAll 清理未用定义
    with suppress(Exception):
        doc.PurgeAll()
        if not quiet:
            log("[OK] PurgeAll 清理未用定义")

    # 3) 多次尝试删除块定义
    deleted = False
    for attempt in range(1, max_delete_attempts + 1):
        try:
            blk = doc.Blocks.Item(block_name)
        except pythoncom.com_error:
            # 已经不存在，视为删除成功
            deleted = True
            if not quiet:
                log(f"[OK] 块定义 '{block_name}' 已不存在，视为已清理。")
            break

        try:
            blk.Delete()
            deleted = True
            if not quiet:
                log(f"[OK] 已删除块定义：{block_name}（第 {attempt} 次尝试）")
            break
        except Exception as e:
            if not quiet:
                log(f"[警告] 第 {attempt} 次删除块定义 '{block_name}' 失败：{e}")
            time.sleep(0.1)

    # 4) 多次 Delete 仍失败 → 改名为 lajikuai_时间戳_N
    if not deleted:
        try:
            blk = doc.Blocks.Item(block_name)
        except pythoncom.com_error:
            # 刚刚已经被清掉了
            if not quiet:
                log(f"[OK] 块定义 '{block_name}' 在改名前就已不存在。")
            return

        idx = 1
        while True:
            new_name = make_trash_name("lajikuai", idx)
            try:
                _ = doc.Blocks.Item(new_name)
                idx += 1
            except pythoncom.com_error:
                break  # 找到未被占用的新名

        try:
            blk.Name = new_name
            if not quiet:
                log(f"[警告] 块定义 '{block_name}' 无法彻底删除，已改名为垃圾块 '{new_name}'")
        except Exception as e:
            if not quiet:
                log(f"[错误] 块 '{block_name}' Delete/改名均失败，可能仍有系统引用：{e}")

    if not quiet:
        log(f"ℹ 完成对 '{block_name}' 的清理。")

@debuggable
#&&% 清理未使用块1
def purge_unused_blocks_1(
    quiet: bool = False,
    protect_names=None,
    max_delete_attempts: int = 2,
    rename_prefix: str = "lajikuai",
):
    """
    一次性清除“当前文件中没有任何实例引用”的块定义。
    - 对每个无实例块，多次 Delete 不掉则改名为 lajikuai_时间戳_N。

    :param quiet: True 则不打印详细信息
    :param protect_names: 不参与清理的块名白名单（列表）
    :param max_delete_attempts: 每个块 Delete 最大尝试次数
    :param rename_prefix: 删除失败时垃圾块名前缀
    :return: List[str] - 所有被“处理”的块原名（包含已删除+已改名）
    """
    import time
    import pythoncom

    from datetime import datetime
    from collections import Counter

    global acad, doc, mp, sp

    if protect_names is None:
        protect_names = []

    def log(msg):
        if not quiet:
            print(msg)

    # 小工具：判断是否块参照
    def is_block_ref(ent) -> bool:
        try:
            on = getattr(ent, "ObjectName", "")
        except Exception:
            return False
        return on in ("AcDbBlockReference", "AcDbMInsertBlock")

    # 小工具：判断是否系统/匿名块（不要动）
    def is_system_block_name(name: str) -> bool:
        if name.startswith("*"):
            return True
        if "|" in name:
            return True
        return False

    # 小工具：生成垃圾块名
    def make_trash_name(base_prefix: str = "lajikuai", idx: int = 1) -> str:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{base_prefix}_{ts}_{idx}"

    node("▶ PUB0 purge_unused_blocks：开始清理无实例块")

    if not li():
        log("[错误] li() 连接失败，无法清理无实例块。")
        return []

    # 1) 统计每个块名的引用次数（遍历所有块定义内部）
    usage_counter = Counter()
    block_names = []

    t0 = time.time()
    for blk_def in doc.Blocks:
        with suppress(Exception):
            name = str(blk_def.Name)
            block_names.append(name)

        with suppress(Exception):
            for ent in blk_def:
                if not is_block_ref(ent):
                    continue
                with suppress(Exception):
                    ref_name = str(ent.Name)
                    usage_counter[ref_name] += 1
    t1 = time.time()

    log(f"[INFO] 扫描 Blocks 完成，耗时 {t1 - t0:.3f}s，共 {len(block_names)} 个块定义。")

    # 2) 调用 PurgeAll 一次：先让 CAD 自己清一轮
    with suppress(Exception):
        doc.PurgeAll()
        log("[OK] PurgeAll 初步清理未用定义")

    # 3) 重建 block_names（因为部分已被 Purge）
    block_names = []
    for blk_def in doc.Blocks:
        with suppress(Exception):
            block_names.append(str(blk_def.Name))

    # 4) 过滤“无实例块候选”（usage == 0）
    unused_candidates = []
    for name in block_names:
        if is_system_block_name(name) or name in protect_names:
            continue
        if usage_counter.get(name, 0) == 0:
            unused_candidates.append(name)

    log(f"[INFO] 候选“无实例块”数量：{len(unused_candidates)}")

    if not unused_candidates:
        log("[OK] 未发现无实例块，清理结束。")
        return []

    processed = []  # 记录被删除或改名的“原始块名”

    # 5) 对每个无实例块尝试 Delete；失败则改名为 lajikuai_xxx
    for blk_name in unused_candidates:
        deleted = False

        for attempt in range(1, max_delete_attempts + 1):
            try:
                blk = doc.Blocks.Item(blk_name)
            except pythoncom.com_error:
                # 已不存在，当作成功
                deleted = True
                log(f"[OK] 块 '{blk_name}' 已不存在（可能刚刚被 PurgeAll 删除），视为已清理。")
                break

            try:
                blk.Delete()
                deleted = True
                processed.append(blk_name)
                log(f"[OK] 块 '{blk_name}' Delete 成功（第 {attempt} 次尝试）")
                break
            except Exception as e:
                log(f"[警告] 块 '{blk_name}' 第 {attempt} 次 Delete 失败：{e}")
                time.sleep(0.05)

        if deleted:
            continue

        # —— Delete 仍失败，改名为垃圾块 —— 
        try:
            blk = doc.Blocks.Item(blk_name)
        except pythoncom.com_error:
            # 又消失了
            log(f"[OK] 准备改名时，块 '{blk_name}' 已不存在。")
            continue

        idx = 1
        while True:
            new_name = make_trash_name(rename_prefix, idx)
            try:
                _ = doc.Blocks.Item(new_name)
                idx += 1
            except pythoncom.com_error:
                break

        try:
            blk.Name = new_name
            processed.append(blk_name)
            log(f"[警告] 块 '{blk_name}' 无实例但 Delete 失败，已改名为垃圾块 '{new_name}'")
        except Exception as e:
            log(f"[错误] 块 '{blk_name}' 无法 Delete 也无法改名：{e}")

    log(f"[OK] 无实例块清理完成，共处理 {len(processed)} 个块定义。")
    return processed

@debuggable
#&&% 预留新插入块名
def reserve_block_names_for_new_insert(
    block_names,
    rename_prefix: str = "oldblk",
    verbose: bool = True,
):
    """
    【核心目标】在插入新块之前，为一组块名“预留新定义空间”。

    逻辑：
    - 对于当前 DWG 中已经存在的同名块定义（包括已有实例）：
      → 不删除、不爆炸，只是把块定义统一改名为 rename_prefix_时间戳_N，
        让原有实例跟着一起使用这个“旧名”。
    - 这样，原来的块名（如 A3-H）在 Blocks 表中就“空出来”了，
      之后从标准模板插入同名块，就一定是全新的定义，不会被老文件干扰。

    参数:
        block_names  : 要预留的新块名列表，例如 ["A3-H", "A2-H", "A1-H", "A0-H"]
        rename_prefix: 旧定义改名使用的前缀（默认 "oldblk"）
        verbose      : 是否打印说明信息（node 日志不受此影响）

    返回:
        dict: { 原名 -> 新名 }，没有被占用的块名不会出现在返回字典中。
    """
    import pythoncom
    from datetime import datetime

    global acad, doc, mp, sp

    if isinstance(block_names, str):
        block_names = [block_names]

    def log(msg):
        if verbose:
            print(msg)

    # 生成唯一旧名
    def make_legacy_name(base_prefix: str, base_name: str, idx: int = 1) -> str:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        # 带上原名，方便将来看出来是哪个演化而来
        return f"{base_prefix}_{base_name}_{ts}_{idx}"

    node("▶ RB0 reserve_block_names_for_new_insert：为块名 {} 预留新定义空间", block_names)

    if not li():
        log("[错误] li() 连接失败，无法预留块名。")
        return {}

    renamed_map = {}

    for name in block_names:
        try:
            blk_def = doc.Blocks.Item(name)
        except pythoncom.com_error:
            # 说明当前 DWG 里没有这个块定义，块名是“干净”的
            node("▶ RB1 块名 '{}' 在当前文件中不存在，可直接用于新定义。", name)
            continue

        # 已存在同名块定义 → 给它改个“旧块”名字，让位给后续新定义
        idx = 1
        while True:
            new_name = make_legacy_name(rename_prefix, name, idx)
            try:
                _ = doc.Blocks.Item(new_name)
                idx += 1
            except pythoncom.com_error:
                break  # 找到未占用的新名

        try:
            blk_def.Name = new_name
            renamed_map[name] = new_name
            node("▶ RB2 块定义 '{}' 已改名为旧块 '{}'", name, new_name)
            log(f"[INFO] 块定义 '{name}' 已让位给新定义，旧定义改名为 '{new_name}'。")
        except Exception as e:
            log(f"[警告] 块 '{name}' 改名为旧块失败：{e}")

    if verbose:
        if renamed_map:
            log("[OK] 已为以下块名预留新定义空间：")
            for old, new in renamed_map.items():
                log(f"   · {old} → {new}")
        else:
            log("[OK] 所有块名在当前 DWG 中本来就是干净的，无需让位。")

    return renamed_map





#&&% 获取选定块引用名
def get_selected_blockreference_names():
    """
    使用 pmxz() 选择实体，并返回所有块引用（AcDbBlockReference）的块名列表。

    :return: list of str，所选块引用的 Name 属性列表
    """
    try:
        # 调用已有函数获取当前选择集（返回 COM 对象列表）
        entities = pmxz()
    except Exception as e:
        sys_logger.info(f"[错误] 调用 pmxz() 失败：{e}")
        return []

    block_names = []
    for ent in entities:
        try:
            # 只处理块引用
            if getattr(ent, "ObjectName", "") == "AcDbBlockReference":
                # Name 属性就是块名
                name = getattr(ent, "Name", None)
                if name:
                    block_names.append(name)
        except Exception as e:
            # 某些 COM 对象可能不支持上述属性，忽略它
            continue

    return block_names


#&&&% 新加块处理

"""
20251205-07

1 对块处理函数进行了深入分析和完善，引入了系统模块D:/claude-tasks/cad/system/CAD_com_utils.py
处理RPC_E_CALL_REJECTED (-2147417846) 错误程序忙产生错误的问题。
有些函数发生了错误，没有完全预设。出问题再处理。

2 增加了ensure_list统一列表单元素和列表都可以作为参数的输入的函数。

3 在 CAD_basic 对属性块的格式操作，获取标签及其值，设置标签及其值，在 CAD_file_operations 对整体插图签需要的重构块内容作了深入到位的处理

4 geimini给出了一套LISP窗口静默传递变量的方法，其典型代码在函数redefine_block_with_entities

  ✅ 强烈推荐使用的场景（只要出现“选择对象:”提示）
  任何需要你指定特定一批对象进行操作的命令，用这个方法都是最稳的：
  移动/复制：_.-MOVE / _.-COPY （不想用 COM 接口的 Move 时，或者处理天正对象时）。
  旋转/缩放：_.-ROTATE / _.-SCALE。
  删除：_.-ERASE （比 COM 的 Delete() 更彻底，不容易残留）。
  写块：_.-WBLOCK （把特定对象存为新文件）。
  阵列/镜像：_.-ARRAY / _.-MIRROR。
  炸开：_.-EXPLODE （特别重要！ COM 接口没有 Explode 方法，只能用 SendCommand，而用 LISP 传参是最准的）。


5 CAD_basic新增3个重要函数

  TDbMText_content(comobj) 获取天正多行文字的内容

  set_entity_grip_state_precise 让处于混乱对象丛中的对象实体成为高亮，使用了LISP深度函数方法

  explode_single_object_marker(ent) 通过绘制辅助线段的handle，利用最后模型空间对象的-1，-2……回溯
  确定预期增加的对象，比图层法等方法大大改进


6 add_entities_to_block_direct提供了新的桌面模式引用，由块的桌面，换成直线也行

"""


#&&% 从区域创建CAD块
def create_block_from_region_cad(
    x1, y1, x2, y2,
    insert_point_option="左下",
    block_name_prefix="块",
    base_point=None,      # 不传 → 就地替换；传了则整体挪到 base_point
    ty: float = 1.0,
):
    """
    【纯 CAD 重绘版】从矩形区域创建块（重画为标准 CAD 实体），
    并用块实例替换原对象。

    特点：
      - 使用 select_entities_in_window 做窗口选取（实体进入夹点高亮状态）；
      - 使用 group_bbox_corners 计算整体外包盒，
        选择某个角点作为“块基点”；
      - 块定义基点固定为 (0,0,0)，所有几何以 base_corner 为原点重画；
      - 块实例插入点：
          base_point=None → = base_corner（就地替换）；
          否则插入到 base_point（整体平移到指定位置）；
      - 支持：
          AcDbLine / Circle / Arc / Polyline / LWPolyline / 2d/3dPolyline /
          Text / MText / BlockReference / Point
        TDbText 会转换为普通 TEXT。

    create_block_from_region_cad(
        68118.6404456771, 245584.27806091635, 351250.3972437666, 431600.55564468517,
        insert_point_option="左下",
        block_name_prefix="块",
        base_point=None,      # 不传 → 就地替换；传了则整体挪到 base_point
        ty= 1.0,
    )
    
    [成功] 已创建块 块06，插入块实例并替换原图形。
    <win32com.gen_py.AutoCAD 2021 Type Library.IAcadBlockReference instance at 0x3029450686608>
    
    D:/claude-tasks/cad/Functional_control/块处理/20251207.dwg

    """

    # ---------- 1. 获取应用与文档 ----------
    doc=C.doc

    # ---------- 2. 窗口选取实体 ----------
    entities = select_entities_in_window(
        x1, y1, x2, y2,
        ty=ty,
        select_mode="_W",
    )
    if not entities:
        print("[警告] 矩形区域内没有对象，无法创建块")
        return None

    sys_logger.info(f"[信息] 选中 {len(entities)} 个对象")

    # ---------- 3. 整体外包盒 + 基点 ----------
    bbox = group_bbox_corners(entities)
    if bbox is None:
        print("[错误] 无法计算整体外包盒")
        return None

    bottom_left, top_right, top_left, bottom_right = bbox
    corner_map = {
        "左下": bottom_left,
        "右上": top_right,
        "左上": top_left,
        "右下": bottom_right,
    }
    base_corner = corner_map.get(insert_point_option, bottom_left)
    bx, by, bz = base_corner
    sys_logger.info(f"[信息] 块基点(外包盒角点): {base_corner}")

    # 决定块实例插入点
    if base_point is None:
        insert_pt = base_corner      # 就地替换
    else:
        insert_pt = base_point       # 整体挪到指定点
    sys_logger.info(f"[信息] 块实例插入位置: {insert_pt}")

    # ---------- 4. 生成唯一块名 ----------
    block_name = block_name_prefix + "01"
    counter = 1
    while True:
        try:
            doc.Blocks.Item(block_name)
            counter += 1
            block_name = f"{block_name_prefix}{counter:02d}"
        except Exception:
            break

    sys_logger.info(f"[信息] 块名: {block_name}")

    # ---------- 5. 创建块定义（基点 = (0,0,0)） ----------
    block_base_pt = (0.0, 0.0, 0.0)
    block_base_variant = VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8, list(block_base_pt)
    )
    block_def = doc.Blocks.Add(block_base_variant, block_name)

    # ---------- 小工具：GetBoundingBox ----------
    def bbox_two_points(e):
        try:
            bb_min, bb_max = e.GetBoundingBox()
            return bb_min, bb_max
        except Exception as ex:
            sys_logger.info(f"[警告] GetBoundingBox 失败: {ex}")
            return None, None

    # ---------- 6. 克隆函数：实体 → 块定义（相对 base_corner） ----------
    def clone_entity_to_block(ent):
        try:
            obj_name = com_retry(lambda: ent.ObjectName)
        except Exception as e:
            sys_logger.info(f"[警告] 无法获取实体类型: {e}")
            return False

        try:
            # ------ Line ------
            if obj_name == "AcDbLine":
                sp = get_object_property(ent, "StartPoint")
                ep = get_object_property(ent, "EndPoint")
                if sp is None or ep is None:
                    sp, ep = bbox_two_points(ent)
                    if sp is None or ep is None:
                        print("[警告] 无法获取线的两端点")
                        return False
                sp_rel = [sp[0] - bx, sp[1] - by, sp[2] - bz]
                ep_rel = [ep[0] - bx, ep[1] - by, ep[2] - bz]
                v_sp = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, sp_rel)
                v_ep = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, ep_rel)
                block_def.AddLine(v_sp, v_ep)
                return True

            # ------ Circle ------
            if obj_name == "AcDbCircle":
                center = get_object_property(ent, "Center")
                radius = get_object_property(ent, "Radius")
                if center is None or radius is None:
                    print("[警告] 无法获取圆的属性")
                    return False
                cen_rel = [center[0] - bx, center[1] - by, center[2] - bz]
                v_cen = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, cen_rel)
                block_def.AddCircle(v_cen, radius)
                return True

            # ------ Arc ------
            if obj_name == "AcDbArc":
                center = get_object_property(ent, "Center")
                radius = get_object_property(ent, "Radius")
                sa = get_object_property(ent, "StartAngle")
                ea = get_object_property(ent, "EndAngle")
                if None in (center, radius, sa, ea):
                    print("[警告] 无法获取圆弧的属性")
                    return False
                cen_rel = [center[0] - bx, center[1] - by, center[2] - bz]
                v_cen = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, cen_rel)
                block_def.AddArc(v_cen, radius, sa, ea)
                return True

            # ------ Polyline / LWPolyline / 2d/3dPolyline ------
            if obj_name in ("AcDbPolyline", "AcDb2dPolyline", "AcDb3dPolyline", "AcDbLWPolyline"):
                coords = get_object_property(ent, "Coordinates")
                if coords is None:
                    print("[警告] 无法获取多段线坐标")
                    return False
                coords = list(coords)
                for i in range(0, len(coords), 3):
                    coords[i]   -= bx
                    coords[i+1] -= by
                    coords[i+2] -= bz
                v_pts = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, coords)
                block_def.AddPolyline(v_pts)
                return True

            # ------ 单行文字 Text ------
            if obj_name == "AcDbText":
                ins = get_object_property(ent, "InsertionPoint")
                txt = get_object_property(ent, "TextString")
                h   = get_object_property(ent, "Height")
                if ins is None or txt is None or h is None:
                    print("[警告] 无法获取 Text 属性，保留原对象")
                    return False
                ins_rel = [ins[0] - bx, ins[1] - by, ins[2] - bz]
                v_ins = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, ins_rel)
                new_txt = block_def.AddText(txt, v_ins, h)
                rot = get_object_property(ent, "Rotation")
                sty = get_object_property(ent, "StyleName")
                try:
                    if rot is not None:
                        new_txt.Rotation = rot
                except Exception:
                    pass
                try:
                    if sty is not None:
                        new_txt.StyleName = sty
                except Exception:
                    pass
                return True

            # ------ MText ------
            if obj_name == "AcDbMText":
                ins = get_object_property(ent, "InsertionPoint")
                width = get_object_property(ent, "Width")
                contents = get_object_property(ent, "Contents")
                if ins is None or width is None or contents is None:
                    print("[警告] 无法获取 MText 属性，保留原对象")
                    return False
                ins_rel = [ins[0] - bx, ins[1] - by, ins[2] - bz]
                v_ins = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, ins_rel)
                new_mt = block_def.AddMText(v_ins, width, contents)
                ht  = get_object_property(ent, "TextHeight")
                rot = get_object_property(ent, "Rotation")
                try:
                    if ht is not None:
                        new_mt.Height = ht
                except Exception:
                    pass
                try:
                    if rot is not None:
                        new_mt.Rotation = rot
                except Exception:
                    pass
                return True

            # ------ BlockReference ------
            if obj_name == "AcDbBlockReference":
                ins = get_object_property(ent, "InsertionPoint")
                if ins is None:
                    bb_min, bb_max = bbox_two_points(ent)
                    if bb_min is None:
                        print("[警告] 无法获取块参照插入点")
                        return False
                    ins = bb_min

                name = get_object_property(ent, "Name")
                sx   = get_object_property(ent, "XScaleFactor") or 1.0
                sy   = get_object_property(ent, "YScaleFactor") or 1.0
                sz   = get_object_property(ent, "ZScaleFactor") or 1.0
                rot  = get_object_property(ent, "Rotation") or 0.0
                if name is None:
                    print("[警告] 无法获取块参照名称")
                    return False

                ins_rel = [ins[0] - bx, ins[1] - by, ins[2] - bz]
                v_ins = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, ins_rel)
                block_def.InsertBlock(v_ins, name, sx, sy, sz, rot)
                return True

            # ------ Point ------
            if obj_name == "AcDbPoint":
                bb_min, bb_max = bbox_two_points(ent)
                if bb_min is None:
                    print("[警告] 无法获取点坐标")
                    return False
                px = (bb_min[0] + bb_max[0]) / 2.0
                py = (bb_min[1] + bb_max[1]) / 2.0
                pz = (bb_min[2] + bb_max[2]) / 2.0
                pt_rel = [px - bx, py - by, pz - bz]
                v_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, pt_rel)
                block_def.AddPoint(v_pt)
                return True

            # ------ TDbText：降级为普通 TEXT ------
            if obj_name == "TDbText":
                # 插入点：InsertionPoint / Position / 外包盒左下兜底
                ins = (get_object_property(ent, "InsertionPoint")
                       or get_object_property(ent, "Position"))
                if ins is None:
                    bb_min, bb_max = bbox_two_points(ent)
                    if bb_min is None:
                        print("[警告] TDbText 无法获取插入点，保留原对象")
                        return False
                    ins = bb_min

                txt = (get_object_property(ent, "TextString")
                       or get_object_property(ent, "Contents")
                       or "")
                h = (get_object_property(ent, "Height")
                     or get_object_property(ent, "TextHeight")
                     or 2500.0)
                rot = (get_object_property(ent, "Rotation")
                       or get_object_property(ent, "Angle")
                       or 0.0)

                ins_rel = [ins[0] - bx, ins[1] - by, ins[2] - bz]
                v_ins = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, ins_rel)
                new_txt = block_def.AddText(txt, v_ins, h)
                try:
                    new_txt.Rotation = rot
                except Exception:
                    pass
                return True

            # 其余对象暂不支持：保留在原位置
            sys_logger.info(f"[提示] 暂不支持的实体类型: {obj_name}，将保留在原位置。")
            return False

        except Exception as e:
            sys_logger.info(f"[警告] 克隆实体 {obj_name} 失败: {e}")
            return False

    # ---------- 7. 克隆 & 删除原对象 ----------
    cloned_count = 0
    skipped_count = 0

    for ent in list(entities):
        ok = False
        try:
            ok = clone_entity_to_block(ent)
        except Exception as e:
            sys_logger.info(f"[警告] 处理实体失败: {e}")
            ok = False

        if ok:
            try:
                ent.Delete()
                cloned_count += 1
            except Exception as e:
                sys_logger.info(f"[警告] 删除原实体失败: {e}")
                skipped_count += 1
        else:
            skipped_count += 1

    sys_logger.info(f"[信息] 成功克隆并删除 {cloned_count} 个实体，"
          f"保留 {skipped_count} 个实体(类型不支持或出错)。")

    if cloned_count == 0:
        print("[错误] 块内没有任何实体，取消插入块。")
        try:
            doc.Blocks.Item(block_name).Delete()
        except Exception:
            pass
        return None

    # ---------- 8. 插入块实例 ----------
    ins_variant = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(insert_pt))
    try:
        block_ref = mp.InsertBlock(ins_variant, block_name, 1.0, 1.0, 1.0, 0.0)
    except Exception as e:
        sys_logger.info(f"[错误] 插入块实例失败: {e}")
        return None

    sys_logger.info(f"[成功] 已创建块 {block_name}，插入块实例并替换原图形。")
    return block_ref


#&&% 从区域创建CMD块
@retry_on_busy 
def create_block_from_region_cmd(
    x1, y1, x2, y2,
    insert_point_option="左下",
    block_name_prefix="块",
    base_point=None,      # 不传则就地替换，传了则整体挪到 base_point
    ty: float = 1.0,
):
    """
    【命令行版】通过 -BLOCK 从矩形区域创建块（保留天正对象），
    已集成 SafeCOM 防崩溃机制。

    create_block_from_region_cmd(
        68118.6404456771, 245584.27806091635, 351250.3972437666, 431600.55564468517,
        insert_point_option="左下",
        block_name_prefix="块",
        base_point=None,      # 不传则就地替换，传了则整体挪到 base_point
        ty= 1.0,
    )
    
    [成功] 已创建块 块07，插入块实例。
    <win32com.gen_py.AutoCAD 2021 Type Library.IAcadBlockReference instance at 0x3029450694608>
    
    D:/claude-tasks/cad/Functional_control/块处理/20251207.dwg

    使用这个命令将属性文字和其它对象可以做成属性块
    create_block_from_region_cmd(
        432574.7599864453, 847782.1082262965, 464037.73142620176, 869475.5330589646,
        insert_point_option="左下",
        block_name_prefix="块",
        base_point=None,      # 不传则就地替换，传了则整体挪到 base_point
        ty = 1.0,
    )
    当前桌面文件： 20251207.dwg
    [成功] 已创建块 块09，插入块实例。
    <win32com.gen_py.AutoCAD 2021 Type Library.IAcadBlockReference instance at 0x2308131932240>
    
    """
    # 确保连接到 CAD
    doc = C.doc
     

    # --- 0. 状态检查：防止在命令交互中强行执行 ---
    try:
        cmd_active = doc.GetVariable("CMDACTIVE")
        if cmd_active != 0:
            sys_logger.info(f"[警告] AutoCAD 处于交互状态 (CMDACTIVE={cmd_active})，尝试取消...")
            doc.SendCommand("\x1b\x1b") # 发送 ESC
            time.sleep(0.5)
    except:
        pass

    # ---------- 小工具：归一化矩形 ----------
    def _normalize_rect(a1, b1, a2, b2):
        x_lo = min(a1, a2)
        x_hi = max(a1, a2)
        y_lo = min(b1, b2)
        y_hi = max(b1, b2)
        return (x_lo, y_lo), (x_hi, y_hi)

    (x_lo, y_lo), (x_hi, y_hi) = _normalize_rect(x1, y1, x2, y2)

    # ---------- 1. 用 SelectionSet.Window 做“后台选取” ----------
    ss_name = "ZB_TMP_BLOCK_SEL_SAFE"
    try:
        doc.SelectionSets.Item(ss_name).Delete()
    except Exception:
        pass

    ss = doc.SelectionSets.Add(ss_name)

    p1 = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [x_lo, y_lo, 0.0])
    p2 = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [x_hi, y_hi, 0.0])

    try:
        ss.Select(constants.acSelectionSetWindow, p1, p2)
    except Exception as e:
        sys_logger.info(f"[错误] SelectionSet.Window 选择失败: {e}")
        return None

    # === 【关键修改点 1】使用 SafeCOM 安全获取列表 ===
    # 替换掉了原来的 entities = list(ss)
    print("[信息] 正在获取选中对象列表...")
    entities = SafeCOM.list_selection(ss) 

    # 用完立即删除选择集，释放资源
    try:
        ss.Delete()
    except Exception:
        pass

    if not entities:
        print("[警告] 矩形区域内没有对象，无法创建块")
        return None

    sys_logger.info(f"[信息] 后台选中 {len(entities)} 个对象（含天正对象）。")

    # ---------- 2. 用 group_bbox_corners 计算整体外包盒 + 基点 ----------
    bbox = group_bbox_corners(entities)
    if bbox is None:
        print("[错误] 无法计算整体外包盒")
        return None

    bottom_left, top_right, top_left, bottom_right = bbox
    corner_map = {
        "左下": bottom_left,
        "右上": top_right,
        "左上": top_left,
        "右下": bottom_right,
    }
    base_corner = corner_map.get(insert_point_option, bottom_left)
    bx, by, bz = base_corner
    sys_logger.info(f"[信息] 块基点(外包盒角点): {base_corner}")

    # 决定块实例插入点
    if base_point is None:
        insert_pt = base_corner
    else:
        insert_pt = base_point
    sys_logger.info(f"[信息] 块实例插入位置: {insert_pt}")

    # ---------- 3. 生成唯一块名 ----------
    block_name = block_name_prefix + "01"
    counter = 1
    while True:
        try:
            doc.Blocks.Item(block_name)
            counter += 1
            block_name = f"{block_name_prefix}{counter:02d}"
        except Exception:
            break

    sys_logger.info(f"[信息] 计划创建块名: {block_name}")

    # ---------- 4. 用 -BLOCK + W 窗口，只建块定义 ----------
    base_pt_str = f"{bx},{by}"
    win_p1_str = f"{x_lo},{y_lo}"
    win_p2_str = f"{x_hi},{y_hi}"

    cmd_lines = [
        "_.-BLOCK",
        block_name,
        base_pt_str,
        "W",
        win_p1_str,
        win_p2_str,
        "",
    ]
    cmd = "\n".join(cmd_lines) + "\n"

    print("[信息] 发送命令流 -BLOCK（窗口选择，只建块定义）...")
    doc.SendCommand(cmd)
    
    # 必须等待命令消化
    time.sleep(ty)
    
    # 额外的忙碌等待
    wait_count = 0
    while doc.GetVariable("CMDACTIVE") != 0 and wait_count < 10:
        time.sleep(0.5)
        wait_count += 1

    # ---------- 5. 用 COM 插入块实例到 insert_pt ----------
    ins_variant = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(insert_pt))
    
    block_ref = None
    # 简单的本地重试，或者也可以用 SafeCOM.call(mp.InsertBlock, ...)
    for i in range(5):
        try:
            block_ref = mp.InsertBlock(ins_variant, block_name, 1.0, 1.0, 1.0, 0.0)
            break
        except Exception:
            time.sleep(0.5)
            
    if block_ref is None:
        sys_logger.info(f"[错误] 插入块实例失败")
        return None

    # ---------- 6. 删除原对象 ----------
    # === 【关键修改点 2】使用 SafeCOM 安全删除对象 ===
    # 很多对象可能已经被 -BLOCK 吸纳，所以这里是为了清理残留
    deleted = 0
    for ent in entities:
        try:
            # 安全调用 Delete，如果对象已失效会自动忽略
            SafeCOM.call(ent.Delete)
            deleted += 1
        except Exception:
            pass

    sys_logger.info(f"[成功] 已创建块 {block_name}，插入块实例。")
    return block_ref

#&&% 从列表对象创建块
@retry_on_busy
def create_block_from_list_cmd(
    entities,
    insert_point_option="左下",
    block_name_prefix="块",
    base_point=None, 
    ty: float = 0.5,
):
    """
    【命令行版】将指定的 Python 对象列表封装成块。
    
    原理：
      虽然 SendCommand 不接受 vtlist (VARIANT)，但我们可以提取对象的 Handle，
      通过 LISP 将其转换为命令行可识别的选择集。
      
    优势：
      1. 完美保留天正/自定义实体特性（非 COM 复制）。
      2. 即使对象不连续、不在矩形内也能精准建块。

    p=cb.pmxz()
                                         
    create_block_from_list_cmd(
        p,
        insert_point_option="左下",
        block_name_prefix="块",
        base_point=None, 
        ty = 0.5,
    )
                                         
    当前桌面文件： 20251207.dwg
    win32 已连接（复用现有 acad，第 1 次成功，Handle=5481）
    [成功] 块 块08 创建完成。
    <win32com.gen_py.AutoCAD 2021 Type Library.IAcadBlockReference instance at 0x3029422644624>
    
    使用这个命令可以创建处属性块，如果使用向普通块追加属性文字不能成属性块
    cb.get_block_attributes_dict(
        kuai,
        ignore_empty= False,
        upper_tag = True,
    )
    {'MINGCHENG': '', 'RIQI': ''}
    
    D:/claude-tasks/cad/Functional_control/块处理/20251207.dwg







    """

    # 1. 列表预处理
    if not entities:
        print("[警告] 列表为空")
        return None
    entities = ensure_list(entities)

    doc = C.doc


    # 2. 计算包围盒 & 基点 (自动处理)
    # 调用现有的 group_bbox_corners 计算几何中心
    bbox = group_bbox_corners(entities)
    if not bbox:
        print("[错误] 无法计算包围盒")
        return None

    bottom_left, top_right, top_left, bottom_right = bbox
    corner_map = {
        "左下": bottom_left, "右上": top_right,
        "左上": top_left,    "右下": bottom_right,
    }
    
    # 确定最终基点
    final_base = base_point if base_point else corner_map.get(insert_point_option, bottom_left)
    bx, by, bz = final_base
    sys_logger.info(f"[信息] 块基点: {bx:.2f}, {by:.2f}, {bz:.2f}")

    # 3. 生成块名
    block_name = block_name_prefix + "01"
    i = 1
    while True:
        try:
            doc.Blocks.Item(block_name)
            i += 1
            block_name = f"{block_name_prefix}{i:02d}"
        except:
            break # 报错说明名字不存在，可用

    # =========================================================
    # 【关键步骤】 将 Python 列表转换为命令行选择集
    # =========================================================
    # 原理：我们不能传 VARIANT 给 SendCommand，但可以传 Handle 字符串
    sys_logger.info(f"[处理] 正在将 {len(entities)} 个对象加入选择集...")
    
    # 定义一个临时的 LISP 变量名
    ss_var = "myss" 
    
    # 1. 清空/新建选择集: (setq myss (ssadd))
    doc.SendCommand(f"(setq {ss_var} (ssadd))\n")
    
    # 2. 遍历列表，将每个对象的 Handle 加入选择集
    # 构造 LISP 语句: (ssadd (handent "句柄值") myss)
    # 为了速度，我们分批拼接字符串发送
    
    cmd_buffer = []
    for ent in entities:
        try:
            h = ent.Handle
            # 将句柄加入 LISP 变量
            cmd_buffer.append(f'(ssadd (handent "{h}") {ss_var})')
        except:
            pass

    # 将巨大的命令拆分成小块发送（避免命令行缓冲区溢出）
    chunk_size = 20 
    for i in range(0, len(cmd_buffer), chunk_size):
        chunk = cmd_buffer[i:i+chunk_size]
        # 用 progn 包裹可以一次执行多条
        full_lisp = "(progn " + " ".join(chunk) + ")\n"
        doc.SendCommand(full_lisp)

    # =========================================================
    # 4. 执行 -BLOCK 命令
    # =========================================================
    sys_logger.info(f"[执行] -BLOCK 创建块: {block_name}")
    
    # 格式: -BLOCK <名> <基点> !<LISP变量名> <回车结束>
    # 注意 !myss 是告诉 CAD "去读 LISP 变量 myss 的内容"
    cmd_str = f"_.-BLOCK\n{block_name}\n{bx},{by},{bz}\n!{ss_var}\n\n"
    
    doc.SendCommand(cmd_str)

    # 等待命令完成
    time.sleep(ty) 
    
    # 清理 LISP 变量
    doc.SendCommand(f"(setq {ss_var} nil)\n")

    # =========================================================
    # 5. 原地插入块参照
    # =========================================================
    # -BLOCK 会把原对象吸走，我们需要原地插回来
    print("[收尾] 原地插入块参照...")
    try:
        ins_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [bx, by, bz])
        # 简单的重试机制
        for _ in range(3):
            try:
                blk_ref = mp.InsertBlock(ins_pt, block_name, 1.0, 1.0, 1.0, 0.0)
                sys_logger.info(f"[成功] 块 {block_name} 创建完成。")
                return blk_ref
            except:
                time.sleep(0.2)
    except Exception as e:
        sys_logger.info(f"[错误] 插入块失败: {e}")

    return None



#&&&% 块编辑

#&&% 获取块内实体
def get_block_contents_at_same_location(block_ref):
    """
    【函数2】获取块内图形并在原位置复制,它的作用是获取到实体内部对象

    思路：
        1. 复制一份块参照（与 block_ref 完全重合）；
        2. 对复制出来的块参照执行 Explode()；
        3. 删除临时块参照；
        4. 返回 Explode 产生的新实体列表。

    优点：
        - 位置、比例、旋转全部由 AutoCAD 自己处理；
        - 包括嵌套块在内的所有内容都会展开到当前空间；
        - 原 block_ref 保留不动。

    20251207测试完毕



    """
    C.li() 

    copied_entities = []

    try:
        # 防止传进来的不是 IAcadBlockReference，可以适当 CastTo（可选）
        # from win32com.client import CastTo
        # block_ref = CastTo(block_ref, "IAcadBlockReference")

        # 1. 复制一份块参照（复制品和原块重合）
        temp_ref = block_ref.Copy()
        print("[信息] 已创建临时块参照作为爆炸对象。")

        # 2. Explode：返回一组新实体，这些实体已经应用了块的变换
        exploded = temp_ref.Explode()  # 一般返回 tuple/列表
        if exploded is None:
            exploded = []
        copied_entities = list(exploded)
        sys_logger.info(f"[信息] Explode 产生 {len(copied_entities)} 个实体。")

        # 3. 删除临时块参照，保留原块参照不动
        try:
            temp_ref.Delete()
        except Exception:
            pass

        sys_logger.info(f"[成功] 已在原位置复制块内容（保留原块参照），复制实体数: {len(copied_entities)}")
        return copied_entities

    except Exception as e:
        sys_logger.info(f"[错误] 操作失败: {e}")
        return []



#&&% 添加实体到块

@retry_on_busy
def add_entities_to_block_direct(block_ref, entities, delete_original=True):
    """
    【函数】进入块定义内部添加对象（强类型修正版）
    1. 修复 CopyObjects 的 Variant 数组传参。
    2. 修复 CopyObjects 返回值嵌套元组解包。
    3. 【本次修复】修复 Move/Rotate/Scale 的点坐标参数无效问题 (强制转为 COM Variant)。

    保留原块的所有属性机制

    p=cb.pmxz()
    当前桌面文件： 20251207.dwg
    win32 已连接（复用现有 acad，第 1 次成功，Handle=566B）
    q=cb.pmxz()
    当前桌面文件： 20251207.dwg
    win32 已连接（复用现有 acad，第 1 次成功，Handle=566D）
    add_entities_to_block_direct(p[0], q, delete_original=True)
    [进入] 正在操作块定义: 块07
    [处理] 正在校正 9 个对象的位置...
    [成功] 已将 9 个对象加入块 块07 并校正位置。
    True
    测试完毕
    D:/claude-tasks/cad/Functional_control/块处理/20251207.dwg

    使用这个命令向普通块追加属性文字就是属性块，但还需要cb.attsync_block_instance(p[0])后才能生效
    add_entities_to_block_definition_1(p[0], q, ty = 0.5)
    
    [完成] 块 cfff 已包含新对象并原位重定义。
    True
    
    cb.get_block_attributes_dict(
    p[0],
    ignore_empty= False,
    upper_tag = True,
    )
    {}


    """
    
    # --- 内部辅助函数：将点转换为 COM 变体 ---
    def com_point(pt_tuple):
        """将 Python 元组 (x,y,z) 转换为 ActiveX 需要的 Variant (Array of Doubles)"""
        # 确保转为 float，防止 int 导致类型错误
        pt_list = [float(x) for x in pt_tuple]
        # 如果是二维点，补全为三维
        if len(pt_list) == 2:
            pt_list.append(0.0)
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, pt_list)

    # 1. 检查输入
    if not entities:
        return False
    entities = ensure_list(entities)

    doc = block_ref.Document ##这是一种特殊语法，换成直线等对象也可以，没有出错，也许多文档有用
    


    # 2. 获取块定义 (修改后)
    try:
        # A. 获取块名：优先取 EffectiveName (处理动态块)，失败则取 Name
        #    利用 get_attr 安全读取，避免报错
        block_name = cb.get_attr(block_ref, 'EffectiveName')
        if not block_name:
            block_name = cb.get_attr(block_ref, 'Name')

        # B. 判空检查：这是最关键的一步！
        #    如果 block_name 是 None，传给 doc.Blocks.Item() 会直接崩溃
        if not block_name:
            sys_logger.info(f"[错误] 无法读取块对象的名称 (Handle={getattr(block_ref, 'Handle', '未知')})")
            return False

        # C. 获取块定义
        #    此时 block_name 肯定是字符串，安全通过
        block_def = doc.Blocks.Item(block_name)

    except Exception as e:
        # 使用 locals() 检查变量是否存在，防止打印错误日志时自身又报错
        safe_name = block_name if 'block_name' in locals() and block_name else "未知"
        sys_logger.info(f"[错误] 获取块定义失败: '{safe_name}'. 错误信息: {e}")
        return False







    sys_logger.info(f"[进入] 正在操作块定义: {block_name}")

    # =========================================================
    # 3. 复制对象 (构建 Dispatch 数组)
    # =========================================================
    try:
        dispatch_array = win32com.client.VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, 
            entities
        )
        ret_obj = doc.CopyObjects(dispatch_array, block_def)
        
        # 解包逻辑
        new_inner_objects = []
        if not isinstance(ret_obj, (list, tuple)):
            new_inner_objects = [ret_obj]
        else:
            if len(ret_obj) > 0 and isinstance(ret_obj[0], tuple):
                new_inner_objects = list(ret_obj[0])
            else:
                new_inner_objects = list(ret_obj)
        
        # 二次防御
        if new_inner_objects and isinstance(new_inner_objects[0], tuple):
             new_inner_objects = list(new_inner_objects[0])

    except Exception as e:
        sys_logger.info(f"[错误] CopyObjects 失败: {e}")
        return False

    # =========================================================
    # 4. 计算并执行位置逆变换 (使用 com_point 包装参数)
    # =========================================================
    # 获取参数


    ins_pt_raw = get_attr(block_ref, 'InsertionPoint')


    rot_angle = block_ref.Rotation    
    scale_factor = block_ref.XScaleFactor 
    origin_raw = (0.0, 0.0, 0.0)

    # 【关键步骤】预先将点转换为 COM Variant
    # Move/Rotate/ScaleEntity 方法对参数类型极其敏感
    try:
        com_ins_pt = com_point(ins_pt_raw)
        com_origin = com_point(origin_raw)
    except Exception as e:
        sys_logger.info(f"[致命错误] 坐标点转换失败: {e}")
        return False

    success_count = 0
    sys_logger.info(f"[处理] 正在校正 {len(new_inner_objects)} 个对象的位置...")

    for obj in new_inner_objects:
        try:
            # A: 逆向移动
            # Move(Point1, Point2) - 必须传入 Variant
            obj.Move(com_ins_pt, com_origin)
            
            # B: 逆向旋转
            # Rotate(BasePoint, RotationAngle)
            if abs(rot_angle) > 1e-6:
                obj.Rotate(com_origin, -rot_angle)
            
            # C: 逆向缩放
            # ScaleEntity(BasePoint, ScaleFactor)
            if abs(scale_factor - 1.0) > 1e-6:
                 obj.ScaleEntity(com_origin, 1.0 / scale_factor)
            
            success_count += 1
                 
        except Exception as e:
            # 打印更详细的 Handle 以便追踪
            h = "Unknown"
            try: h = obj.Handle
            except: pass
            sys_logger.info(f"[警告] 对象(H:{h}) 变换失败: {e}")

    # =========================================================
    # 5. 删除外部原对象
    # =========================================================
    if delete_original and success_count > 0:
        for ent in entities:
            try:
                ent.Delete()
            except:
                pass

    block_ref.Update()
    sys_logger.info(f"[成功] 已将 {success_count} 个对象加入块 {block_name} 并校正位置。")
    return True


@retry_on_busy
def add_entities_to_block_definition_explode(block_ref, new_entities, ty: float = 0.5):
    """
    【函数】向块定义中追加对象（独立版）
    不清除原块对象，而是将新对象与原块内容合并，原地重定义块。
    
    逻辑：
    1. 利用 ActiveX Explode 方法获取块的原有几何体（生成新图元，原块引用保持不变）。
    2. 将“新图元”与“原有几何体”合并。
    3. 使用 -BLOCK 命令覆盖原定义（由于选中的是炸开后的图元，命令执行后它们会消失进入块定义）。
    4. 原有的 block_ref 会自动更新显示新内容。

    :param block_ref: 目标块引用对象 (IAcadBlockReference)
    :param new_entities: 待加入的新图元列表
    :param ty: 等待时间
    """

    # 1. 检查新对象
    if not new_entities:
        return False
    new_entities = ensure_list(new_entities)

    # 调试信息（假设 li() 是你的日志函数）
    try:
        doc = C.doc
    except:
        pass


        
    # 2. 获取锁定目标信息
    # 优先取 EffectiveName (处理动态块)，如果你有 get_attr 函数，这是最稳健的写法
    block_name = cb.get_attr(block_ref, 'EffectiveName')
    
    # 如果 EffectiveName 获取失败（返回 None），降级尝试获取 Name
    if not block_name:
        block_name = cb.get_attr(block_ref, 'Name')

    # 【关键】必须进行判空检查
    # 因为如果 block_ref 既没有 EffectiveName 也没有 Name，block_name 会是 None
    if not block_name:
        sys_logger.info(f"[错误] 无法获取块名称 (Handle={cb.get_attr(block_ref, 'Handle')})")
        return False  # 或者 continue，视上下文而定






    # 获取基点 (必须是原插入点，保证视觉不动)


    ins_pt = get_attr(block_ref, 'InsertionPoint')


    bx, by, bz = ins_pt

    sys_logger.info(f"[追加对象] 锁定目标块: {block_name}")

    # =========================================================
    # 3. 关键步骤：获取原块内的几何体
    # =========================================================
    try:
        # Explode() 方法会在原地生成块内的图元对象，并返回一个元组/列表
        # 注意：这不会删除 block_ref 本身，仅仅是生成了它的组成部分
        # 这些部分位于当前模型空间，且坐标已经是变换后的世界坐标
        exploded_objects = block_ref.Explode()
        
        # 将 tuple 转为 list 以便合并
        exploded_list = list(exploded_objects)
        sys_logger.info(f"[处理] 原块分解出 {len(exploded_list)} 个图元用于重组")
    except Exception as e:
        sys_logger.info(f"[错误] 无法炸开块引用获取原几何体: {e}")
        return False

    # 合并：新对象 + 原块炸开的对象
    total_entities = new_entities + exploded_list

    # =========================================================
    # 4. 构建 LISP 选择集
    # =========================================================
    ss_var = "zb_append_ss"
    
    # 4.1 初始化
    doc.SendCommand(f"(setq {ss_var} (ssadd))\n")
    
    # 4.2 注入 Handle (包含新对象和原块分解出的对象)
    cmd_buffer = []
    for ent in total_entities:
        try:
            h = ent.Handle
            cmd_buffer.append(f'(ssadd (handent "{h}") {ss_var})')
        except:
            pass

    # 4.3 发送 LISP 填充命令 (分块发送防止命令行溢出)
    chunk_size = 20
    for i in range(0, len(cmd_buffer), chunk_size):
        chunk = cmd_buffer[i:i+chunk_size]
        doc.SendCommand("(progn " + " ".join(chunk) + ")\n")

    # =========================================================
    # 5. 发送覆盖命令
    # =========================================================
    print("[执行] 发送重定义指令(追加模式)...")
    
    # _.-BLOCK -> 名字 -> Y(覆盖) -> 基点 -> !变量 -> 结束
    # 原理：BLOCK 命令会将选择集中的对象（exploded_list 和 new_entities）
    # 从模型空间移除，并存入块定义中。
    cmd_str = f"_.-BLOCK\n{block_name}\nY\n{bx},{by},{bz}\n!{ss_var}\n\n"
    
    doc.SendCommand(cmd_str)
    
    # 等待命令执行完成
    time.sleep(ty)
    wait_count = 0
    while doc.GetVariable("CMDACTIVE") != 0 and wait_count < 20:
        time.sleep(0.2)
        wait_count += 1

    # 清理 LISP 变量
    doc.SendCommand(f"(setq {ss_var} nil)\n")

    # =========================================================
    # 6. 刷新与善后
    # =========================================================
    try:
        # 强制刷新显示
        doc.Regen(1)
        # 尝试更新块引用（虽然重定义后通常会自动更新）
        block_ref.Update()
    except:
        pass

    sys_logger.info(f"[完成] 块 {block_name} 已包含新对象并原位重定义。")
    return True



#&&% 重定义块内容

@retry_on_busy
def redefine_block_with_entities(block_ref, entities, ty: float = 0.5, debug_log_path="C:\\cad_debug_log.txt"):
    """
    【调试专用版 V2】redefine_block_with_entities
    修复了 'IAcadEntity object has no attribute Name' 的接口类型问题。
    """
    sys_logger.info(f"\n--- [DEBUG模式 V2] 正在执行严格版重定义 (ty={ty}) ---")
    
    # ================= 0. 环境准备 & 接口修复 =================
    if not entities:
        print("[错误] 输入实体列表为空。")
        return False
        
    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        doc = acad.ActiveDocument
    except:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument

    # 【关键修复】尝试强制类型转换，确保它是块引用
    try:
        if block_ref.ObjectName == "AcDbBlockReference":
            block_ref = win32com.client.CastTo(block_ref, "IAcadBlockReference")
    except Exception as cast_e:
        # 如果转换失败，不阻断，后续用 getattr 尝试
        sys_logger.info(f"[类型警告] 接口转换失败，将尝试直接读取: {cast_e}")

    # 获取块名和 Handle
    try:
        # 1. 尝试获取属性（兼容 generic entity）
        # getattr(obj, name, default) 可以避免报错
        block_name = getattr(block_ref, 'EffectiveName', None)
        if not block_name:
            block_name = getattr(block_ref, 'Name', None)
            
        if not block_name:
            # 如果还是拿不到，可能是对象失效了
            sys_logger.info(f"[致命错误] 无法获取块名 (ObjectName={getattr(block_ref, 'ObjectName', 'Unknown')})")
            return False

        target_handle = getattr(block_ref, 'Handle', None)
        ins_pt = getattr(block_ref, 'InsertionPoint', None)
        
        if not target_handle or not ins_pt:
            print("[致命错误] 无法获取 Handle 或 插入点")
            return False
            
        bx, by, bz = ins_pt
    except Exception as e:
        sys_logger.info(f"[致命错误] 读取目标块信息时发生异常: {e}")
        return False

    # ================= 1. 现状快照 (基准线) =================
    try:
        block_def = doc.Blocks.Item(block_name)
        old_count = block_def.Count
        sys_logger.info(f"[现状] 块定义 '{block_name}' (Handle:{target_handle}) 当前对象数: {old_count}")
    except:
        sys_logger.info(f"[警告] 无法获取块定义 '{block_name}'，可能是匿名块。")
        old_count = -1

    # ================= 2. 输入审计 (Input Audit) =================
    valid_handles = []
    
    try:
        with open(debug_log_path, "a", encoding="utf-8") as f:
            f.write(f"\n====== {time.strftime('%H:%M:%S')} 处理块: {block_name} ======\n")
            f.write(f"目标 Handle: {target_handle}\n")
            
            for i, ent in enumerate(entities):
                try:
                    h = ent.Handle
                    if h == target_handle:
                        f.write(f"索引 {i}: Handle={h} -> [剔除] 目标块自身\n")
                        sys_logger.info(f"[警报] 发现目标块自身混入列表 (Handle={h})，已剔除。")
                        continue
                    
                    valid_handles.append(h)
                    f.write(f"索引 {i}: Handle={h} -> [有效] 类型={getattr(ent, 'ObjectName', 'Unknown')}\n")
                except:
                    pass
    except Exception as log_e:
        sys_logger.info(f"[日志警告] 写日志失败: {log_e}")
        valid_handles = []
        for ent in entities:
            if hasattr(ent, 'Handle') and ent.Handle != target_handle:
                valid_handles.append(ent.Handle)

    input_count = len(valid_handles)
    sys_logger.info(f"[审计] 准备注入 {input_count} 个对象。")

    if input_count == 0:
        print("[终止] 有效对象为 0，取消操作。")
        return False

    # ================= 3. 构建 LISP 选择集 & 握手 =================
    ss_var = "zb_debug_ss"
    doc.SetVariable("USERI1", 0) 
    doc.SendCommand(f"(setq {ss_var} (ssadd))\n")

    cmd_buffer = []
    for h in valid_handles:
        cmd_buffer.append(f'(ssadd (handent "{h}") {ss_var})')
    
    chunk_size = 10
    for i in range(0, len(cmd_buffer), chunk_size):
        chunk = cmd_buffer[i:i+chunk_size]
        doc.SendCommand("(progn " + " ".join(chunk) + ")\n")

    # === 握手验证 ===
    doc.SendCommand(f'(setvar "USERI1" (sslength {ss_var}))\n')
    
    # 等待 LISP 回写
    lisp_count = 0
    retries = 0
    while retries < 20: 
        time.sleep(0.1)
        lisp_count = doc.GetVariable("USERI1")
        if lisp_count > 0:
            break
        retries += 1

    sys_logger.info(f"[握手] Python发送: {input_count} | LISP接收: {lisp_count}")

    if lisp_count == 0:
        print("[失败] LISP 选择集为空，操作终止。")
        return False

    # ================= 4. 执行核心指令 =================
    print("[执行] 发送 -BLOCK 覆盖指令...")
    
    cmd = f"_.-BLOCK\n{block_name}\nY\n{bx},{by},{bz}\n!{ss_var}\n\n"
    doc.SendCommand(cmd)
    
    wait_cycles = 0
    while doc.GetVariable("CMDACTIVE") != 0 and wait_cycles < 50:
        time.sleep(0.1)
        wait_cycles += 1
    
    doc.SendCommand(f"(setq {ss_var} nil)\n")
    
    # ================= 5. 结果验尸 =================
    try:
        doc.Regen(1)
        block_ref.Update()
    except:
        pass
    
    try:
        new_count = doc.Blocks.Item(block_name).Count
        delta = new_count - old_count
        sys_logger.info(f"[结果] 块定义 '{block_name}' 旧数:{old_count} -> 新数:{new_count} (变化:{delta})")

        if new_count == old_count:
            print("❌ [失败确认] 块内部实体数量未变化！")
            return False
        else:
            print("✅ [成功确认] 块定义已更新。")
            return True
    except:
        return True


















#&&% 提取非块实体
@retry_on_busy
def extract_specific_entities_from_block(block_ref, mode: str = 'all', keep_in_block: bool = True):
    """
    【函数】从块中提取指定类型的对象（筛选版）
    
    :param block_ref: 块引用对象
    :param mode: 提取模式 
                 'text'    - 提取文字 (AcDbText, MText, AttributeDef, TDb...)
                 'block'   - 提取嵌套块 (BlockReference)
                 'polyline'- 提取多段线 (LWPolyline, 2d/3dPolyline)
                 'all'     - 提取所有对象
    :param keep_in_block: True=仅复制出来(保留原块内容); False=剪切出来(删除块内对应内容)
    :return: 提取出的新对象列表 (位于模型空间)


    lb=extract_specific_entities_from_block(p[0], mode = 'text', keep_in_block = True)
    
    [开始] 提取模式: text | 保留原块: True
    [提取] 成功筛选出 6 个目标对象。
    lb[0].ObjectName
    'TDbText'
    lb[1].ObjectName
    'TDbMText'
    lb[2].ObjectName
    'AcDbMText'
    lb[3].ObjectName
    'AcDbText'
    lb[4].ObjectName
    'AcDbAttributeDefinition'
    lb[5].ObjectName
    'AcDbAttributeDefinition'

    D:/claude-tasks/cad/Functional_control/块处理/20251207.dwg    

    """
    
    # ================= 配置区域 =================
    # 1. 预定义目标类型集合 (ObjectName)
    target_map = {
        'text': {
            'AcDbText', 
            'AcDbMText', 
            'AcDbAttributeDefinition', 
            'TDbMText',  # 天正多行文字
            'TDbText'    # 天正单行文字
        },
        'block': {
            'AcDbBlockReference', 
            'AcDbMInsertBlock'
        },
        'polyline': {
            'AcDbPolyline', 
            'AcDbLWPolyline', 
            'AcDb2dPolyline', 
            'AcDb3dPolyline'
        }
    }
    
    mode = mode.lower()
    extracted_entities = []
    
    sys_logger.info(f"\n[开始] 提取模式: {mode} | 保留原块: {keep_in_block}")

    try:
        doc = block_ref.Document
        
        # 0. 检查是否为 MInsertBlock
        if hasattr(block_ref, "MInsertCount"):
            if block_ref.MInsertCount > 1 or block_ref.MInsertRow > 1:
                print("[警告] 无法处理多重插入块 (MInsertBlock)。")
                return []

        # =========================================================
        # 第一步：炸开获取副本 (ModelSpace)
        # =========================================================
        try:
            # Explode 生成新对象在原位
            exploded_variants = block_ref.Explode()
        except Exception as e:
            sys_logger.info(f"[错误] 炸开失败: {e}")
            return []
            
        if not exploded_variants:
            return []

        # =========================================================
        # 第二步：筛选与清理副本
        # =========================================================
        # 逻辑：遍历炸开后的碎片，符合要求的保留，不符合的由程序立即删除
        
        for ent in exploded_variants:
            try:
                obj_name = ent.ObjectName
                is_match = False
                
                # --- 匹配逻辑 ---
                if mode == 'all':
                    is_match = True
                elif mode in target_map:
                    if obj_name in target_map[mode]:
                        is_match = True
                else:
                    sys_logger.info(f"[错误] 未知模式: {mode}")
                    return []

                # --- 动作 ---
                if is_match:
                    extracted_entities.append(ent)
                else:
                    # 关键：这不是我想要的东西，这是 Explode 产生的“废料”，立即删除
                    ent.Delete()
                    
            except Exception:
                # 异常对象防御性删除
                try: ent.Delete() 
                except: pass

        sys_logger.info(f"[提取] 成功筛选出 {len(extracted_entities)} 个目标对象。")

        # =========================================================
        # 第三步：处理原块定义 (如果需要“剪切”效果)
        # =========================================================
        if not keep_in_block and len(extracted_entities) > 0:
            try:

                
                # 获取块名 (优先取 EffectiveName 以支持动态块，失败则退回 Name)
                b_name = cb.get_attr(block_ref, 'EffectiveName')
                if not b_name:
                    b_name = cb.get_attr(block_ref, 'Name')
                
                # 2. 安全获取块定义
                # 必须判空！如果 b_name 为 None，直接传给 Item() 会导致 COM 崩溃
                if b_name:
                    try:
                        block_def = doc.Blocks.Item(b_name)
                    except Exception:
                        # 只有在名字存在但块定义表中找不到时才会进这里（极少见）
                        block_def = None
                else:
                    block_def = None



                sys_logger.info(f"[内部] 正在清理块定义 {b_name} 中的对应对象...")
                count_deleted = 0
                
                # 遍历块定义内部的所有实体
                # 注意：不能直接在循环中删除集合元素，建议先收集再删除，或者小心处理
                items_to_delete = []
                
                for item in block_def:
                    obj_name = item.ObjectName
                    should_delete = False
                    
                    if mode == 'all':
                        # 注意：全选模式下，不建议删除里面的 EndBlk 等特殊对象，通常只需删除几何体
                        # 但简单起见，且 Explode 无法还原属性，慎用 all + keep_in_block=False
                        if obj_name != "AcDbBlockEnd" and obj_name != "AcDbBlockBegin":
                             should_delete = True
                    elif mode in target_map:
                        if obj_name in target_map[mode]:
                            should_delete = True
                            
                    if should_delete:
                        items_to_delete.append(item)

                # 执行删除
                for item in items_to_delete:
                    try:
                        item.Delete()
                        count_deleted += 1
                    except:
                        pass
                
                sys_logger.info(f"[完成] 从块定义中移除了 {count_deleted} 个对象。")
                
                # 强制刷新
                block_ref.Update()
                doc.Regen(1)
                
            except Exception as e:
                sys_logger.info(f"[警告] 修改块定义失败: {e}")

        return extracted_entities

    except Exception as e:
        sys_logger.info(f"[异常] extract_specific_entities 发生错误: {e}")
        return []

#&&&% 确定炸开块

#&&% 确保简单炸开块

@retry_on_busy(max_retries=5, base_delay=0.2)
def safe_explode(block_entity):
    """
    【原子操作】
    只负责炸开和删除。如果 CAD 忙，@retry_on_busy 会自动原地重试。
    如果 5 次后依然失败（如对象锁定），抛出异常给上层处理。
    """
    # 1. 炸开 (Explode 保留原对象)
    result=block_entity.Explode()

    return  result



@retry_on_busy(max_retries=5, base_delay=0.2)
def _atomic_explode_and_delete(block_entity):
    """
    【原子操作】
    只负责炸开和删除。如果 CAD 忙，@retry_on_busy 会自动原地重试。
    如果 5 次后依然失败（如对象锁定），抛出异常给上层处理。
    """
    # 1. 炸开 (Explode 保留原对象)
    result=block_entity.Explode()

    try:
        # 这里的 wait 不需要太久，旨在让指令队列“落地”
        wait_quiescent(min_quiet=0.1, timeout=1.0) 
    except:
        time.sleep(0.1) # 兜底



    # 2. 删除 (Delete 移除原对象)
    block_entity.Delete()

    return  result

@timeit
def safe_explode_retry(entity, max_retries=5, rescue_retries=5, interval=1.0, verbose=True):
    """
    【通用原子函数 - 深度搜救修正版 (V5.0)】
    
    功能：
        尝试炸开实体并返回新对象。
        如果 Explode 返回空但原对象已消失，启用“深度搜救”在数据库中查找新生成的对象。
    
    返回契约 (Strict Mode):
        list: [新对象...] 或 [] -> 成功 (原对象已彻底消失)
        None:                  -> 失败 (原对象依然健在)
    
    修复记录:
        - 修正搜救索引算法：从 count_before - 1 开始扫描，解决多抓取一个旧对象的问题。
    """
    
    # 1. 保存身份信息与容器
    try:
        ent_handle = entity.Handle
        ent_name = entity.Name if hasattr(entity, 'Name') else "<Block>"
        # 获取 Document 和 容器 (ModelSpace/PaperSpace) 用于人口普查
        doc = entity.Document
        owner_space = doc.ObjectIdToObject(entity.OwnerID)
    except:
        if verbose: print("⚠️ [前置检查] 对象无效或无法读取容器，视为已处理。")
        return [] # 死对象视为成功处理

    # 闭包：存活检查
    def is_entity_alive(ent):
        try:
            _ = ent.Layer
            return True
        except:
            return False

    # 0. 开局检查
    if not is_entity_alive(entity):
        if verbose: sys_logger.info(f"ℹ️ [前置] 对象 {ent_name} 已不存在，无需炸开。")
        return []

    for i in range(1, max_retries + 1):
        # —————— 📸 拍摄快照 (人口普查) ——————
        count_before = 0
        try: count_before = owner_space.Count
        except: pass
        # ————————————————————————————————————

        try:
            # 1. 执行原子操作 (Explode + Delete)
            # 注意：_atomic_explode_and_delete 自带 @retry_on_busy 抗忙碌
            result = _atomic_explode_and_delete(entity)

            # 2. 【完美路径】直接拿到了返回对象
            if result and len(result) > 0:
                return list(result)

            # 3. 【搜救路径】返回空，但原对象没了 -> 启动深度搜救
            if not is_entity_alive(entity):
                if verbose: sys_logger.info(f"✅ [尝试 {i}] 炸开成功(无返回)，启动深度搜救 (Max {rescue_retries}次)...")
                
                # —————— ⛑️ 深度搜救循环 (索引修正版) ——————
                # 逻辑推导：
                # 旧数量 N -> 删1剩 N-1 (索引 0~N-2) -> 新对象从 N-1 开始
                # 修正：start_index = count_before - 1
                start_index = max(0, count_before - 1) 
                
                for r_attempt in range(1, rescue_retries + 1):
                    try:
                        # a. 等待数据库同步 (时间递增)
                        wait_time = 0.5 * r_attempt
                        wait_quiescent(min_quiet=wait_time, timeout=3.0)
                        
                        # b. 获取当前数量
                        count_after = owner_space.Count
                        
                        # c. 如果数量确实增加了 (排除仅仅是删除了的情况)
                        if count_after > count_before: 
                            recovered_objs = []
                            
                            # 遍历新增区间
                            # range(start, end) 含头不含尾
                            for idx in range(start_index, count_after):
                                try:
                                    item = owner_space.Item(idx)
                                    # 双重保险：排除掉自己(虽然应该已经死了)
                                    if hasattr(item, 'Handle') and item.Handle != ent_handle:
                                        recovered_objs.append(item)
                                except: pass
                            
                            # 如果捞到了东西
                            if recovered_objs:
                                if verbose: sys_logger.info(f"   🎉 [搜救 {r_attempt}] 成功找回 {len(recovered_objs)} 个新对象。")
                                return recovered_objs
                        
                        # d. 如果还没刷新出来，尝试 Regen 刺激一下 CAD
                        if verbose: sys_logger.info(f"   ⏳ [搜救 {r_attempt}] 数据库未刷新 (Cnt: {count_before}->{count_after})，尝试 Regen...")
                        try: doc.Regen(0) 
                        except: pass
                        
                    except Exception as rescue_err:
                        if verbose: sys_logger.info(f"   ⚠️ 搜救出错: {rescue_err}")

                # —————— 搜救结束 ——————
                if verbose: sys_logger.info(f"⚠️ [搜救结束] 尽力了，数据库未返回新对象。返回空列表。")
                return [] # 实在捞不到，只能返回空，但因为对象没了，算成功

            # 4. 逻辑失败: 对象还在
            if verbose: sys_logger.info(f"⚠️ [尝试 {i}/{max_retries}] 对象依然健在，重试...")

        except pythoncom.com_error as e:
            # 5. 捕获 "对象已删除" -> 视为成功
            if e.hresult == -2147352567 or "对象已被删除" in str(e):
                if verbose: sys_logger.info(f"✅ [尝试 {i}] 捕获删除信号。")
                return []
            
            if verbose: sys_logger.info(f"⚠️ [尝试 {i}] COM 报错: {e}")
            time.sleep(interval)
        
        except Exception as e:
            if verbose: sys_logger.info(f"⚠️ [尝试 {i}] 未知错误: {e}")
            time.sleep(interval)

    # 循环结束，最后确认一眼
    if not is_entity_alive(entity):
        return [] # 虽然坎坷，但结果是对象没了，算成功
    
    if verbose:
        sys_logger.info(f"❌ [最终失败] {ent_name} (Handle: {ent_handle}) 依然健在。")
    return None # ❌ 唯一返回 None 的情况：失败






#&&% 炸开对象并回溯

def explode_single_object_marker(ent):
    """
    【主函数】炸开单个对象（辅助线回溯版）
    
    逻辑：
      1. 创建一根辅助线（Marker）。
      2. 选中目标对象 (set_entity_grip_state_precise)。
      3. 发送 EXPLODE。
      4. 倒序遍历模型空间，收集对象，直到遇到辅助线为止。
      5. 删除辅助线，返回收集到的碎片。
    """


    li()

    if not ent: return []

    marker = None
    exploded_objs = []

    try:
        # 1. 创建辅助线 (Marker)
        # 随便画在原点附近即可，位置不重要，重要的是 Handle
        # 使用 VARIANT 创建坐标点
        pt1 = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
        pt2 = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [1.0, 1.0, 0.0])
        
        try:
            marker = mp.AddLine(pt1, pt2)
            marker_handle = marker.Handle
        except Exception as e:
            sys_logger.info(f"[错误] 无法创建辅助标记线: {e}")
            return []

        # 2. 选中目标对象 (进入夹点状态)
        # 调用之前写好的精确选中函数
        if not set_entity_grip_state_precise(ent):
            print("[中断] 无法选中对象，取消炸开。")
            return []

        # 3. 发送炸开命令
        # print("[操作] 发送 EXPLODE...")
        doc.SendCommand("._EXPLODE\n")

        # 4. 等待炸开完成
        try:
            # 调用已有的等待函数
            wait_command_done()
        except:
            # 简单回退策略
            time.sleep(0.5)

        # 5. 回溯模型空间 (Backtracking)
        # 原理：AutoCAD 新生成的对象（碎片）一定在 Database 的最后面
        # 我们从最后往前找，直到撞到我们的 Marker 辅助线
        
        current_count = mp.Count
        
        # 倒序遍历
        for i in range(current_count - 1, -1, -1):
            try:
                obj = mp.Item(i)
                
                # 如果遇到了我们的辅助线，说明后面的都是新炸出来的
                if obj.Handle == marker_handle:
                    break
                
                # 收集碎片
                exploded_objs.append(obj)
                
            except Exception:
                continue

    except Exception as e:
        sys_logger.info(f"[错误] 炸开过程异常: {e}")

    finally:
        # 6. 清理现场 (删除辅助线)
        if marker:
            try:
                marker.Delete()
            except:
                pass

    sys_logger.info(f"[成功] 炸开回收 {len(exploded_objs)} 个碎片。")
    return exploded_objs

#&&% 安全炸开并删除
def safe_explode_and_delete(bk, ci=3, delay=1.0):
    """
    对块对象 bk 执行安全的 Explode 与 Delete 操作：
      1. 最多尝试 ci 次调用 bk.Explode()，
         每次调用后等待 delay 秒，再检查返回的实体列表长度是否 > 1。
      2. 如果 ci 次都没有成功（len(LP) <= 1），抛出 RuntimeError。
      3. 如果 Explode 成功，最多尝试 ci 次调用 bk.Delete()，遇错则继续重试。
      4. 返回第一次成功 Explode 时得到的实体列表 LP。

    :param bk:    要炸开的块引用 COM 对象
    :param ci:    最大尝试次数，默认 3
    :param delay: 每次 Explode 后的等待时间（秒），默认 1.0
    :return:      成功 Explode 后返回的新实体列表 LP
    :raises:      RuntimeError 如果 Explode 在 ci 次内都失败
    """
    LP = []
    # 1️⃣ 重试 Explode
    for attempt in range(1, ci + 1):
        try:
            LP = bk.Explode()
        except Exception as e:
            LP = []  # 如果调用失败，视为没有炸开
        time.sleep(delay)

        # 尝试获取长度
        try:
            count = len(LP)
        except Exception:
            # 如果 LP 不是标准序列，就把它转换一下
            LP = list(LP)
            count = len(LP)

        if count > 1:
            # 炸开成功
            break
        else:
            # 第 attempt 次 Explode 未成功，继续重试
            continue
    else:
        raise RuntimeError(f"Explode 在 {ci} 次尝试后仍未成功 (len(LP)={len(LP)})")

    # 2️⃣ Explode 成功后，重试 Delete
    for attempt in range(1, ci + 1):
        try:
            bk.Delete()
            break
        except Exception:
            # Delete 出错，继续下次重试
            continue
    # 如果 ci 次都失败，也不抛错误，只是放弃删除
    return LP


#&&&% 块统计
#&&% count_blocks_by_name
def count_blocks_by_name(block_name):
    """
    # 【新增】统计指定块数量

    Args:
        block_name: 块名称

    Returns:
        int: 块实例数量
    """
    try:
        from system.CAD_selection import ss_select
        blocks = ss_select(mode="all", filter_types=[2], filter_data=[block_name])
        count = len(blocks) if blocks else 0
        sys_logger.info(f"[成功] 统计块'{block_name}'数量: {count}")
        return count
    except Exception as e:
        sys_logger.error(f"[错误] 统计块数量失败: {e}")
        return 0

#&&% count_blocks_by_type
def count_blocks_by_type():
    """
    # 【新增】按类型统计块

    Returns:
        dict: {块名: 数量}
    """
    try:
        from system.CAD_selection import ss_select
        all_blocks = ss_select(mode="all", filter_types=[2], filter_data=["INSERT"])

        block_counts = {}
        for blk in all_blocks:
            name = get_block_name(blk)
            block_counts[name] = block_counts.get(name, 0) + 1

        sys_logger.info(f"[成功] 统计块类型: {len(block_counts)}种")
        return block_counts
    except Exception as e:
        sys_logger.error(f"[错误] 统计块类型失败: {e}")
        return {}

#&&% generate_block_report
def generate_block_report(output_path):
    """
    # 【新增】生成块统计报告

    Args:
        output_path: 输出文件路径（Excel或文本）

    Returns:
        bool: 成功返回True
    """
    try:
        block_counts = count_blocks_by_type()

        if output_path.endswith('.xlsx'):
            import pandas as pd
            df = pd.DataFrame(list(block_counts.items()), columns=['块名', '数量'])
            df.to_excel(output_path, index=False)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("块统计报告\n")
                f.write("=" * 50 + "\n")
                for name, count in sorted(block_counts.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"{name}: {count}\n")

        sys_logger.info(f"[成功] 生成块统计报告: {output_path}")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 生成块统计报告失败: {e}")
        return False

#&&&% 块替换
#&&% batch_replace_blocks
def batch_replace_blocks(old_name, new_name):
    """
    # 【新增】批量替换块

    Args:
        old_name: 旧块名
        new_name: 新块名

    Returns:
        int: 替换数量
    """
    try:
        from system.CAD_selection import ss_select
        blocks = ss_select(mode="all", filter_types=[2], filter_data=[old_name])

        if not blocks:
            sys_logger.info(f"[信息] 未找到块'{old_name}'")
            return 0

        count = 0
        for blk in blocks:
            try:
                blk.Name = new_name
                count += 1
            except Exception as e:
                sys_logger.warning(f"[警告] 替换块失败: {e}")

        sys_logger.info(f"[成功] 批量替换块: {count}个")
        return count
    except Exception as e:
        sys_logger.error(f"[错误] 批量替换块失败: {e}")
        return 0

#&&% smart_replace_blocks
def smart_replace_blocks(criteria, new_name):
    """
    # 【新增】智能替换块

    Args:
        criteria: 筛选条件函数 lambda blk: bool
        new_name: 新块名

    Returns:
        int: 替换数量
    """
    try:
        from system.CAD_selection import ss_select
        all_blocks = ss_select(mode="all", filter_types=[2], filter_data=["INSERT"])

        count = 0
        for blk in all_blocks:
            try:
                if criteria(blk):
                    blk.Name = new_name
                    count += 1
            except Exception as e:
                sys_logger.warning(f"[警告] 智能替换块失败: {e}")

        sys_logger.info(f"[成功] 智能替换块: {count}个")
        return count
    except Exception as e:
        sys_logger.error(f"[错误] 智能替换块失败: {e}")
        return 0

