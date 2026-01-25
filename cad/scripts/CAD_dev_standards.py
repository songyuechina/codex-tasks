# -*- coding: utf-8 -*-
# 文件名: CAD_dev_standards.py
# 功能: 复杂函数编写规范、AI指令模板及标准代码范例
# 核心依赖: system/licad.py, system/CAD_coordination.py

import sys
import pythoncom
from win32com.client import VARIANT
from pathlib import Path

# 路径自举：确保能引用到 system 目录
try:
    current_dir = Path(__file__).parent
    system_dir = current_dir.parent / "system"
    if str(system_dir) not in sys.path:
        sys.path.insert(0, str(system_dir))
    
    # 导入核心架构组件
    from licad import C, retry_on_busy
    from CAD_coordination import send_cmd_with_sync
except ImportError:
    pass # 仅做范例展示时忽略错误

# =============================================================================
# 模块一：AI 编程指令模板 (The Golden Prompt)
# [使用说明]: 请直接复制本字符串的内容发送给 AI
# =============================================================================
AI_PROMPT_TEMPLATE = """

【编程规范要求】(必须严格遵守)
1. 架构依赖：
   - 引用核心连接模块：`from system.licad import C, retry_on_busy`
   - (如需发送命令) 引用协同调度模块：`from system.CAD_coordination import send_cmd_with_sync`

2. 稳定性要求：
   - 所有涉及 AutoCAD COM 读写操作（如 Add, Delete, get/set 属性）的函数，**必须**加上 `@retry_on_busy` 装饰器。
   - 这能防止 'Call Rejected' 错误，确保 CAD 忙碌时自动重试。

3. 命令发送规范：
   - **严禁**直接使用 `doc.SendCommand()`。
   - **必须**使用 `send_cmd_with_sync(cmd_string)`，确保同步等待。

4. 对象调用：
   - 一律通过 `C.doc`, `C.mp` (模型空间), `C.sp` (图纸空间) 进行操作。
   - 不要手写 `win32com` 连接逻辑。
   - **严禁缓存**：严禁在函数外部或全局作用域将 `C.doc` 赋值给变量。

5. 调试风格：
   - 采用 `verbose_level` (0=静音, 1=摘要, 2=追踪, 3=调试) 控制日志。
   - 默认值使用全局配置 `GLOBAL_DEFAULT_VERBOSE = 1`。

6. 注释规范 (强制)：
   - 必须遵循【模块二】中的 Docstring 格式，包含函数编号、功能描述、核心特性、参数详解等。
"""

# =============================================================================
# 模块二：文档注释规范 (Docstring Standard)
# =============================================================================

def docstring_standard_example(ctq, layout_target=None):
    """
    【函数编号】: DEMO-001 (V1.0 - 标准范例)
    【所属模块】: 规范演示模块 (Standards)
    【功能描述】: 
        演示标准的函数文档注释写法。
        此部分内容应清晰描述函数的宏观作用。
        
        核心特性：
        1. 规范性：严格遵循规定的字段头。
        2. 清晰度：分点描述复杂逻辑。
        3. 完整性：涵盖参数、返回值及特殊行为。
      
    【参数详解】:
        - ctq (tuple): 数据容器 (polys_list, blocks_list, 字典)。
        - layout_target (str): 
            * None: 模型空间模式。
            * "布局名称": 图纸空间模式，将切换至该布局。

    【返回值】:
        - bool: 执行成功返回 True，失败返回 False。
    """
    pass

# =============================================================================
# 模块三：调试风格规范 (Verbose Level Pattern)
# =============================================================================

# 全局默认等级 (0=静音, 1=关键摘要, 2=详细追踪, 3=底层调试)
GLOBAL_DEFAULT_VERBOSE = 1 

def count_layers_demo(filter_name="Wall", verbose=None):
    """
    [范例] 统计包含指定名称的图层数量
    展示 verbose_level 的标准用法：主函数控制流程，子函数按需输出。
    """
    # 1. 解析日志等级 (优先使用参数，否则使用全局)
    lvl = int(verbose) if verbose is not None else GLOBAL_DEFAULT_VERBOSE

    # 2. 定义内部日志函数 (闭包)
    def log(msg, min_lvl=1):
        if lvl >= min_lvl:
            # 缩进技巧：等级越高，缩进越深，日志越清晰
            indent = "  " * (min_lvl - 1)
            print(f"{indent}[LayerCount] {msg}")

    # --- 主流程 ---
    log(f"开始统计图层，过滤词: '{filter_name}'", min_lvl=1) # L1: 关键步骤

    try:
        count = 0
        # 假设 layers 是一个列表，模拟 C.doc.Layers
        # 在实际代码中，应使用: layers = C.doc.Layers
        layers = ["Wall_01", "Wall_02", "Door_01", "Window_01", "Wall_Backup"] 
        
        for layer_name in layers:
            # 只有 verbose >= 2 时才打印正在检查哪个图层
            log(f"检查图层: {layer_name}", min_lvl=2) 

            # 调用子函数，透传 verbose 等级
            if _check_name_match(layer_name, filter_name, verbose=lvl):
                count += 1
                log(f"-> 匹配成功 (+1)", min_lvl=2)
            else:
                # 只有 verbose >= 3 (Deep Debug) 时才打印“忽略”这种琐碎信息
                log(f"-> 忽略", min_lvl=3) 

        log(f"统计完成，共找到 {count} 个图层。", min_lvl=1)
        return count

    except Exception as e:
        log(f"发生错误: {e}", min_lvl=0) # L0: 错误必须打印
        return 0

def _check_name_match(name, keyword, verbose=1):
    """
    [子函数] 配合主函数的 verbose 等级
    只有当 verbose >= 3 (Deep Debug) 时，子函数才允许打印自己的内部日志
    """
    if verbose >= 3:
        print(f"    [DeepCheck] Comparing '{name}' with '{keyword}'...")
    
    return keyword in name


# =============================================================================
# 模块四：标准范例函数 (展示装饰器和 C 对象的使用)
# =============================================================================
import pythoncom
from win32com.client import VARIANT

# 1. 导入核心和装饰器
try: 
    from system.licad import C, retry_on_busy
except ImportError:
    pass 

# 2. 加上装饰器 (AI 看到这个示例就懂了)
@retry_on_busy
def draw_circle_standard_example():
    """
    [范例] 标准绘图函数
    展示核心规范：
    1. 使用 @retry_on_busy 防崩溃
    2. 使用 C.mp 自动管理连接
    3. 使用 VARIANT 进行坐标转换
    """
    try:
        # 数据准备
        center = (0.0, 0.0, 0.0)
        radius = 100.0

        # 类型转换
        center_variant = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, center)

        # 核心操作 (无需 try-except 连接，但建议 try-except 业务逻辑)
        circle = C.mp.AddCircle(center_variant, radius)

        print(f"[成功] 在 {C.doc.Name} 绘制圆形 (Handle: {circle.Handle})")
        return True

    except Exception as e:
        print(f"[错误] {e}")
        return False



# =============================================================================
# 模块五：架构标准范例 (连接 + 装饰器 + 命令同步 + 类型转换)
# =============================================================================

@retry_on_busy
def architecture_full_demo():
    """
    [范例] 集成所有架构要求的标准函数
    展示：@retry_on_busy, C.mp, VARIANT, send_cmd_with_sync
    """
    try:
        print("[Step 1] 开始 COM 操作 (由装饰器保护)...")
        
        # 1. 数据准备 (类型转换)
        # VT_ARRAY | VT_R8 代表 "双精度浮点数数组"
        center = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (0, 0, 0))
        radius = 50.0

        # 2. 核心操作 (直接调用 C.mp，无需 try-connect)
        circle = C.mp.AddCircle(center, radius)
        
        # 使用 C.doc 获取信息
        print(f"[成功] 在文件 '{C.doc.Name}' 绘制圆形 (ID: {circle.Handle})")

        # -------------------------------------------------------
        
        print("[Step 2] 开始发送命令 (由 sync 函数保护)...")
        
        # 3. 命令操作 (严禁使用 doc.SendCommand)
        # 发送全图缩放命令，并等待 CAD 空闲
        if send_cmd_with_sync("_ZOOM _E"):
            print("[CMD] 视图缩放完成")
        else:
            print("[CMD] 视图缩放超时或失败")
            
        return True

    except Exception as e:
        print(f"[错误] 执行失败: {e}")
        return False
