
# ==============================================================================
#  CAD Python 自动化开发核心规范 (System Standards)
#  Level: L1 (Infrastructure) & L4 (Drawing/Operation)
#  Version: 1.0 (Refactored Docstrings Only)
# ==============================================================================
"""

适用范围: AutoCAD Python Automation System (win32com based)

1. 体系架构原则 (Architecture Philosophy)
本系统采用 分层架构 (Layered Architecture)，遵循“高内聚、低耦合”原则。

L3 - 调度层 (Manager / Controller)
职责: “大脑”。负责业务逻辑决策、文件命名计算、列表遍历、错误统计、任务分发。

特征: 唯一的外部调用入口。不直接操作底层绘图指令，而是调度 L2/L1 函数。

命名示例: PRINT-003 (print_polylines_list)

L2 - 执行层 (Executor)
职责: “手脚”。负责具体任务的执行。

特征: 只接受“绝对指令”（如绝对路径、明确的坐标元组）。不包含任何模糊的业务判断（如“该怎么命名文件”）。

命名示例: PRINT-001 (export_model_window_pure), DRAW-005 (draw_lwpolyline)

L1 - 基建层 (Infrastructure / Common)
职责: “工具箱”。提供全局通用的底层能力。

特征: 与具体业务解耦，甚至跨项目通用。

核心模块: 连接管理、对象属性访问、几何计算、通用选择。

命名示例: COMMON-CONN-001 (li), COMMON-OBJ-002 (get_object_property)

2. 命名与编号体系 (Naming & ID System)
2.1 函数编号
所有函数必须分配唯一 ID，格式：[模块]-[功能序号]-[辅助标记]。

模块代码 (Module Codes):

COMMON: 公共基础 (连接/排序/工具)

SELECT: 选择集操作

DRAW: 绘图操作

PRINT: 打印/输出

BLOCK: 图块与属性

GEOM: 几何算法

辅助标记: -AUX 表示仅供内部调用的辅助函数。

2.2 变量命名
严禁拼音: 如 fangxiang, tuceng ❌。

强制英文: 如 rotation, layer_name ✅。

语义化: full_filepath 优于 path；entity_list 优于 l。

3. 函数文档注释标准 (Docstring Protocol)
所有函数必须包含以下标准 Docstring：

Python

def function_name(arg1, arg2):
    
    【函数编号】: MODULE-00X
    【所属模块】: 模块名称 (层级)
    【功能描述】: 
        简明扼要地描述函数做什么。
        如果有特殊副作用（如切换了布局、清空了选择集），必须说明。
    
    【依赖函数】: 
        - li() (COMMON-CONN-001)
        - other_func (ID)
    
    【输入参数】:
        - arg1 (type): 含义说明。
        - arg2 (type): 含义说明。
    
    【输出参数】:
        - return (type): 返回值说明。失败时的返回值（如 None）。
    
    【逻辑流程】:
        1. 步骤一...
        2. 步骤二...
    
4. 强制使用的标准工具 (Mandatory Tooling)
为了系统稳定性，严禁手写以下逻辑，必须调用标准函数：

4.1 连接与环境
初始化: 所有 L2/L3 函数入口必须调用 li()。

布局切换: 必须使用 switch_to_layout(name)，严禁直接设置 doc.ActiveLayout。

4.2 对象操作
获取包围盒: 必须使用 safe_get_bbox(ent)。

理由: 解决新建对象无包围盒及 RPC 忙碌报错。

属性读写: 必须使用 get_attr(obj, name) 和 set_attr(obj, name, val)。

理由: 自动处理天正自定义实体 (TArch) 的 DISPID 映射与标准 CAD 对象的差异。

类型转换: 使用 cast_object(ent) 或内部的 _maybe_cast。

4.3 字符串与路径
文件名清洗: 必须使用 sanitize_filename(name)。

理由: 防止文件名包含 / \ : * ? " < > | 导致保存失败。

4.4 COM 交互
绑定方式: 必须使用 Early Binding (win32com.client.gencache.EnsureDispatch)。

常量使用: 必须使用 win32com.client.constants.acWindow 等常量，严禁使用魔术数字（如 4）。

5. 模块特定规约 (Domain Specific Rules)
5.1 打印系统 (PRINT Module)
职责分离:

文件名拼接、序号生成、缺省命名逻辑 -> 仅在 L3 (Manager) 处理。

L2 (Executor) 函数只接受 full_filepath (绝对路径)。

布局打印次序:

在 Layout 空间打印时，必须严格遵守：先 SetWindowToPlot -> 后 PlotType = acWindow。违背顺序会导致 "Invalid Input"。

5.2 选择系统 (SELECT Module)
图层选择: 使用 select_tuceng，不要自己写遍历逻辑。

区域选择: 使用 select_entities_in_window，利用 Zoom 和 Select 命令组合，确保选择准确性。

5.3 绘图系统 (DRAW Module)
点/向量: 使用 vtpnt 或 pt3 辅助函数将 Python 元组转换为 COM VARIANT 数组。

多段线: 优先使用轻量多段线 (draw_lwpolyline)，除非涉及 3D 标高变化。

6. 异常处理规范 (Error Handling)
COM 错误捕获: 必须捕获 pywintypes.com_error。

重试机制: 对于涉及 RPC 交互的操作（如选择、获取属性），应使用 com_retry 装饰器或内部循环重试，以应对 CAD 忙碌状态。

静默原则: 底层函数出错应打印日志并返回 None/False，尽量避免直接 crash 导致脚本中断（除非是关键的连接失败）。

附录：AI 提示词摘要 (System Prompt)
(将以下内容复制给 AI，作为快速指令)

系统指令： 你是 AutoCAD Python 自动化开发助手。请严格遵守《CAD自动化开发核心规范》：

架构: 区分 Manager (逻辑) 与 Executor (执行)。

基建: 必须使用 li(), safe_get_bbox(), get_attr(), switch_to_layout() 等标准函数，严禁重复造轮子。

COM: 使用 EnsureDispatch (早期绑定) 和 constants 常量。

注释: 使用包含【编号】【功能】【依赖】【输入/输出】【逻辑】的标准 Docstring。

命名: 仅使用英文变量名，MODULE-XXX 编号格式。
"""

import time
import math
import win32com.client as win32
import win32com.client
import pythoncom
import pywintypes
from win32com.client import VARIANT, CastTo

# 假设全局变量在此处定义，或由 li() 初始化
acad = None
doc = None
mp = None
sp = None

# ==============================================================================
#  MODULE: COMMON-CONN (连接与初始化)
#  Level: L1 (Infrastructure)
# ==============================================================================

# 1 连接cad必须使用li()
def li():
    """
    【函数编号】: COMMON-CONN-001
    【所属模块】: 基础设施 / 连接管理
    【功能描述】: 
        智能连接 AutoCAD 应用程序并复用当前激活文档。
        包含防断线测试机制，确保返回的全局变量 (doc, mp, sp) 真实可用。
        具备“优先复用”和“失败重连”的双重保障策略。
        连接成功后会自动尝试显示并激活 CAD 窗口。
    
    【依赖函数】:
        - get_acad_doc (COMMON-CONN-002)
        - draw_line (DRAW-002) [用于测试连接]
        - get_object_property (COMMON-OBJ-002) [用于测试对象句柄]
        - safe_delete (COMMON-UTIL-XXX) [需外部定义]
    
    【输入参数】: 无
    
    【输出参数】:
        - return (bool): 连接成功返回 True，彻底失败返回 False。
    
    【逻辑流程】:
        1. [复用阶段]: 尝试使用全局 `acad` 变量。若存在，尝试获取 `ActiveDocument`。
        2. [健康检查]: 在模型空间画一条测试直线，获取其 Handle，然后删除。若全程无错，视为连接健康。
        3. [重连阶段]: 若复用失败（或 `acad` 未定义），调用 `get_acad_doc()` 重新建立 COM 连接。
        4. [二次检查]: 重连后再次执行画线测试。
        5. [窗口激活]: 设置 `acad.Visible = True`。
    """
    
    global acad, doc, mp, sp

    # ========= 第一段：尝试“复用已有 acad” =========
    try:
        app = acad  # 如果 acad 尚未定义，这里会 NameError
    except NameError:
        app = None

    if app is not None:
        for attempt in range(1, 4):
            try:
                # 1) 获取当前激活文档
                active_doc = app.ActiveDocument
                if active_doc is None:
                    raise RuntimeError("acad.ActiveDocument 返回 None。")

                doc = active_doc
                mp = doc.ModelSpace
                sp = doc.PaperSpace

                # 2) 在当前激活 DWG 里画一条测试直线
                test_line = draw_line((0, 0, 0), (1000, 0, 0))
                if test_line is None:
                    raise RuntimeError("测试直线创建失败，draw_line 返回 None。")

                handle = get_object_property(test_line, "Handle")
                if not handle:
                    raise RuntimeError("测试直线未获得有效 Handle。")

                # 3) 删除测试线，说明一切正常
                try:
                    safe_delete(test_line)
                except Exception as e_del:
                    print(f"[li] 删除测试直线时出错（忽略）：{e_del}")

                print("当前桌面文件：", doc.Name)
                print(f"win32 已连接（复用现有 acad，第 {attempt} 次成功，Handle={handle}）")
                
                # =======================================================
                # 【新增 1】复用成功后，强制显示窗口
                # =======================================================
                try:
                    acad.Visible = True
                    # 可选：最大化窗口 (3 = acMax)
                    # acad.WindowState = 3 
                except:
                    pass
                
                return True

            except Exception as e:
                print(f"[li] 复用现有 acad 第 {attempt} 次失败：{repr(e)}")
                if attempt < 3:
                    time.sleep(0.5)

        # 走到这里说明“有 acad 但复用失败”，将进入重连逻辑
        print("[li] 提示：存在 acad，但多次复用失败，准备执行重连逻辑 get_acad_doc()。")

    else:
        print("[li] 全局 acad 不存在，将直接执行重连逻辑 get_acad_doc()。")

    # ========= 第二段：调用原来的 get_acad_doc() 做“重连” =========
    for attempt in range(1, 4):
        try:
            acad, doc = get_acad_doc()  # 原来的连接逻辑（内部可能会启动 CAD）
            mp = doc.ModelSpace
            sp = doc.PaperSpace

            # 重连后再做一次测试线，验证连接可用
            try:
                test_line = draw_line((0, 0, 0), (1000, 0, 0))
            except Exception as e_line:
                raise RuntimeError(f"重连后画测试直线时异常：{e_line}")

            if test_line is None:
                raise RuntimeError("重连后测试直线创建失败，draw_line 返回 None。")

            try:
                handle = get_object_property(test_line, "Handle")
            except Exception as e_handle:
                raise RuntimeError(f"重连后读取 Handle 异常：{e_handle}")

            try:
                safe_delete(test_line)
            except Exception as e_del:
                print(f"[li] 重连后删除测试线时出错（忽略）：{e_del}")

            print(f"[li] 重连后测试线 Handle={handle}")
            print("当前桌面文件：", doc.Name)
            print("win32 已重新连接 — CAD基本操作")
            
            # =======================================================
            # 【新增 2】重连成功后，强制显示窗口
            # =======================================================
            try:
                acad.Visible = True
                # 可选：最大化窗口
                # acad.WindowState = 3
            except:
                pass

            return True

        except Exception as e:
            print(f"[li] 第 {attempt} 次重连失败：{repr(e)}")
            if attempt < 3:
                time.sleep(0.5)
    
    print("[li] 警告：多次尝试后仍无法连接 AutoCAD / 当前 DWG。")
    return False


def get_acad_doc(max_wait=8.0):
    """
    【函数编号】: COMMON-CONN-002
    【所属模块】: 基础设施 / 连接管理
    【功能描述】: 
        底层连接函数。智能获取 AutoCAD Application 对象和当前 ActiveDocument。
        处理 RPC 忙碌状态，支持自动启动 CAD 进程，并在无文档时自动新建文档。
        使用 gencache.EnsureDispatch 确保建立强类型连接（早期绑定）。
    
    【依赖函数】:
        - _coinit_once (COMMON-CONN-003-AUX)
    
    【输入参数】:
        - max_wait (float): RPC 忙碌时的最大等待时间（秒）。默认 8.0。
    
    【输出参数】:
        - return (tuple): (app, doc) 对象元组。若失败可能抛出异常。
    
    【逻辑流程】:
        1. 调用 _coinit_once 初始化 COM 环境。
        2. 尝试 GetActiveObject 获取现有进程（强类型转换）。
        3. 若无，尝试 EnsureDispatch 启动新进程。
        4. 获取 ActiveDocument。若 RPC 报错（忙碌），则循环重试。
        5. 若无活动文档（AttributeError），尝试 Add() 新建文档。
        6. 返回 (app, doc)。
    """
    _coinit_once()
    t0 = time.time()
    app = None
    
    while True:
        try:
            # --- 阶段 A: 获取/启动 App ---
            if app is None:
                try:
                    # 1. 优先尝试 GetActiveObject (只连不启，速度快)
                    app = win32.GetActiveObject("AutoCAD.Application")
                    # 拿到了对象，为了保险，转成强类型接口 (加载缓存)
                    app = win32.gencache.EnsureDispatch(app)
                except Exception:
                    # 2. 没找到活动的，则使用 EnsureDispatch (启动或连接)
                    app = win32.gencache.EnsureDispatch("AutoCAD.Application")
            
            # --- 阶段 B: 获取文档 ---
            # 尝试访问 ActiveDocument，如果 CAD 刚启动可能还没有文档
            doc = app.ActiveDocument
            
            # 激活一下属性，确保没报错且对象存活
            _ = doc.Name 
            
            return app, doc

        except pywintypes.com_error as e:
            # --- 阶段 C: 异常处理 ---
            code = e.args[0] if e.args else None
            
            # 情况 1: RPC 忙碌/未就绪 -> 等待并重试
            if (code in _RPC_BUSY + _RPC_DOWN):
                if (time.time() - t0 < max_wait):
                    time.sleep(0.05)
                    continue
                else:
                    raise RuntimeError("连接超时：AutoCAD 响应过慢或处于忙碌状态。")
            
            # 情况 2: 无激活文档 (通常错误码不同，或者直接报错 AttributeError)
            # 尝试自愈：新建文档
            try:
                if app is not None:
                    print("检测到 CAD 已启动但无文档，正在新建...")
                    doc = app.Documents.Add()
                    _ = doc.Name
                    return app, doc
            except Exception as e_add:
                print(f"尝试新建文档失败: {e_add}")
                pass
            
            # 无法处理的错误，抛出
            raise
        
        except AttributeError:
             # 有时 app.ActiveDocument 为 None 会报 AttributeError 而不是 COM error
             try:
                if app is not None:
                    doc = app.Documents.Add()
                    return app, doc
             except:
                pass
             if (time.time() - t0 < max_wait):
                 time.sleep(0.1); continue
             raise

# RPC 错误码：忙碌 或 服务不可用
_RPC_BUSY = (-2147417846, -2147418111)
_RPC_DOWN = (-2147023174,)

def _coinit_once():
    """
    【函数编号】: COMMON-CONN-003-AUX
    【所属模块】: 基础设施 / 连接管理
    【功能描述】: 
        COM 线程初始化防呆封装。确保 CoInitialize 被调用，忽略重复调用错误。
    """
    try: 
        pythoncom.CoInitialize()
    except pythoncom.error: 
        pass

def com_retry(fn, retries=30, delay=0.05):
    """
    【函数编号】: COMMON-CONN-004-AUX
    【所属模块】: 基础设施 / 错误处理
    【功能描述】: 
        通用的 COM 调用重试装饰器/包装器。
        专门处理 RPC_E_CALL_REJECTED (CAD 忙碌) 错误。
    
    【输入参数】:
        - fn (callable): 需要执行的函数或 lambda。
        - retries (int): 重试次数。
        - delay (float): 重试间隔。
    """
    for _ in range(retries):
        try:
            return fn()
        except pywintypes.com_error as e:
            code = e.args[0] if e.args else None
            if code in _RPC_BUSY + _RPC_DOWN:
                time.sleep(delay); continue
            raise
    return fn()


# ==============================================================================
#  MODULE: SELECT (选择集操作)
#  Level: L2 (Selection)
# ==============================================================================

# 2 选择不要使用遍历模型空间，应该使用图层选择，多段线选择，快选择等类型选择区域选择要用

# ===================== 选择函数（重写版） =====================

#&&% 按图层选择
def select_tuceng(layer_names, max_retries=5, delay=0.5, autocast=True):
    """
    【函数编号】: SELECT-001
    【所属模块】: 选择模块 (Selection)
    【功能描述】: 
        按图层名称快速选择实体。
        支持单个图层名或图层名列表。内置重试机制应对 CAD 选择集繁忙。
    
    【依赖函数】:
        - ss_select (SELECT-CORE-XXX) [需外部定义]
        - get_acad_doc (COMMON-CONN-002) [用于失败时的视图刷新]
    
    【输入参数】:
        - layer_names (str/list): 图层名或列表。
        - max_retries (int): 失败重试次数。
        - delay (float): 重试间隔。
        - autocast (bool): 是否自动转换 COM 接口。
    
    【输出参数】:
        - return (list): 选中的实体对象列表。失败返回空列表。
    """
    if isinstance(layer_names, str):
        layers = [layer_names]
    else:
        layers = list(layer_names)
    last = None
    for k in range(1, max_retries+1):
        try:
            ents = ss_select(
                mode="all",
                filter_types=[8],                # 8 = Layer
                filter_data=[layers if len(layers)>1 else layers[0]],
                autocast=autocast
            )
            print(f"[OK] 第 {k} 次尝试：选到图层 {layers} 上 {len(ents)} 个对象")
            return ents
        except Exception as e:
            last = e
            print(f"[警告] 第 {k} 次失败：{e!r}")
            try:
                _, doc = get_acad_doc()
                doc.SendCommand("RE\nZ\nE\n")
            except Exception:
                pass
            time.sleep(delay)
    print(f"[错误] 重试 {max_retries} 次后仍失败：{last!r}")
    return []

#&&% 图层选择别名
def stc(layer_names, **kwargs):
    """
    【函数编号】: SELECT-001-ALIAS
    【功能描述】: select_tuceng 的简写别名。
    """
    return select_tuceng(layer_names, **kwargs)


#&&% 选择所有块
def select_kuai(max_retries: int = 5, autocast=True):
    """
    【函数编号】: SELECT-002
    【所属模块】: 选择模块
    【功能描述】: 
        选择当前空间内的所有块参照 (INSERT)。
    
    【输入参数】:
        - max_retries (int): 重试次数。
        - autocast (bool): 是否自动转换接口。
    
    【输出参数】:
        - return (list): 块参照对象列表。
    """
    last = None; t0 = time.time()
    for k in range(1, max_retries+1):
        try:
            ents = ss_select(
                mode="all",
                filter_types=[0],               # 0 = 实体类型
                filter_data=["INSERT"],
                autocast=autocast
            )
            print(f"[OK] select_kuai 成功（第 {k} 次），耗时 {time.time()-t0:.3f}s，共 {len(ents)} 个块")
            return ents
        except Exception as e:
            last = e
            print(f"[警告] select_kuai 第 {k} 次失败：{e!r}")
            try:
                _, doc = get_acad_doc(); doc.SendCommand("RE\nZ\nE\n")
            except Exception: pass
            time.sleep(0.5)
    print(f"[错误] select_kuai 在 {max_retries} 次尝试后仍失败：{last!r}")
    return []


# 4) 选择所有 TEXT
#&&% 选择所有文本
def select_text(autocast=True):
    """
    【函数编号】: SELECT-003
    【所属模块】: 选择模块
    【功能描述】: 选择所有单行文本 (TEXT)。
    """
    t0 = time.time()
    ents = ss_select(mode="all", filter_types=[0], filter_data=["TEXT"], autocast=autocast)
    print("耗时：", time.time()-t0)
    return ents

# 5) 选择所有 MTEXT
#&&% 选择所有多行文本
def select_mtext(autocast=True):
    """
    【函数编号】: SELECT-004
    【所属模块】: 选择模块
    【功能描述】: 选择所有多行文本 (MTEXT)。
    """
    t0 = time.time()
    ents = ss_select(mode="all", filter_types=[0], filter_data=["MTEXT"], autocast=autocast)
    print("耗时：", time.time()-t0)
    return ents

# 6) PUB_TEXT 图层上的“天正文字”分类（按 ObjectName）
#&&% 选择天正文本
def select_pub_text_entities():
    """
    【函数编号】: SELECT-005
    【所属模块】: 选择模块 / 天正支持
    【功能描述】: 
        选择 'PUB_TEXT' 图层上的天正自定义文字对象。
        自动区分单行 (TDbText) 和多行 (TDbMText)。
    
    【依赖函数】:
        - select_tuceng (SELECT-001)
    
    【输出参数】:
        - return (tuple): (tdb_texts, tdb_mtexts) 两个列表。
    """
    LAYER_NAME = "PUB_TEXT"
    ents = select_tuceng(LAYER_NAME, autocast=False)  # 天正对象通常是代理/专有类，先别 Cast
    tdb_texts, tdb_mtexts = [], []
    for ent in ents:
        name = getattr(ent, "ObjectName", None) or getattr(ent, "EntityName", "")
        if name == "TDbText":
            tdb_texts.append(ent)
        elif name == "TDbMText":
            tdb_mtexts.append(ent)
    return tdb_texts, tdb_mtexts

#&&% 收集所有文本
def collect_all_texts():
    """
    【函数编号】: SELECT-006
    【所属模块】: 选择模块
    【功能描述】: 
        综合收集器。同时收集天正文字、原生 TEXT 和 MTEXT。
        副作用：会将所有收集到的文字强制归层到 'PUB_TEXT'。
    
    【输出参数】:
        - return (tuple): (tz_texts, tz_mtexts, cad_texts, cad_mtexts)
    """
    LAYER_NAME = "PUB_TEXT"
    tz_texts, tz_mtexts = select_pub_text_entities()
    cad_texts  = select_text(autocast=True)
    cad_mtexts = select_mtext(autocast=True)

    for ent in (tz_texts + tz_mtexts + cad_texts + cad_mtexts):
        try:
            ent.Layer = LAYER_NAME
        except Exception:
            pass
    return tz_texts, tz_mtexts, cad_texts, cad_mtexts


# 7) 选择 LINE / CIRCLE / ELLIPSE / SPLINE
#&&% 选择直线
def select_line(autocast=True):
    """【函数编号】: SELECT-007 | 选择所有直线 (LINE)"""
    t0 = time.time()
    ents = ss_select(mode="all", filter_types=[0], filter_data=["LINE"], autocast=autocast)
    print("耗时：", time.time()-t0)
    return ents

#&&% 选择圆
def select_circle(autocast=True):
    """【函数编号】: SELECT-008 | 选择所有圆 (CIRCLE)"""
    t0 = time.time()
    ents = ss_select(mode="all", filter_types=[0], filter_data=["CIRCLE"], autocast=autocast)
    print("耗时：", time.time()-t0)
    return ents

#&&% 选择椭圆
def select_ellipse(autocast=True):
    """【函数编号】: SELECT-009 | 选择所有椭圆 (ELLIPSE)"""
    t0 = time.time()
    ents = ss_select(mode="all", filter_types=[0], filter_data=["ELLIPSE"], autocast=autocast)
    print("耗时：", time.time()-t0)
    return ents

#&&% 选择样条曲线
def select_spline(autocast=True):
    """【函数编号】: SELECT-010 | 选择所有样条曲线 (SPLINE)"""
    t0 = time.time()
    ents = ss_select(mode="all", filter_types=[0], filter_data=["SPLINE"], autocast=autocast)
    print("耗时：", time.time()-t0)
    return ents


# 8) 传统多段线（POLYLINE）与轻量多段线（LWPOLYLINE）
#&&% 选择传统多段线
def select_polyline_chuantong(max_retries: int = 5, autocast=True):
    """
    【函数编号】: SELECT-011
    【功能描述】: 选择传统重型多段线 (POLYLINE - 2D/3D)。
    """
    last = None; t0 = time.time()
    for k in range(1, max_retries+1):
        try:
            ents = ss_select(mode="all", filter_types=[0], filter_data=["POLYLINE"], autocast=autocast)
            print(f"[OK] select_polyline_chuantong 成功（第 {k} 次），耗时 {time.time()-t0:.3f}s，共 {len(ents)} 条")
            return ents
        except Exception as e:
            last = e
            print(f"[警告] select_polyline_chuantong 第 {k} 次失败：{e!r}")
            try:
                _, doc = get_acad_doc(); doc.SendCommand("RE\nZ\nE\n")
            except Exception: pass
            time.sleep(0.5)
    print(f"[错误] select_polyline_chuantong 在 {max_retries} 次后仍失败：{last!r}")
    return []

#&&% 选择轻量多段线
def select_polyline(max_retries: int = 5, autocast=True):
    """
    【函数编号】: SELECT-012
    【功能描述】: 选择轻量多段线 (LWPOLYLINE)。
    """
    last = None; t0 = time.time()
    for k in range(1, max_retries+1):
        try:
            ents = ss_select(mode="all", filter_types=[0], filter_data=["LWPOLYLINE"], autocast=autocast)
            print(f"[OK] select_polyline 成功（第 {k} 次），耗时 {time.time()-t0:.3f}s，共 {len(ents)} 条")
            return ents
        except Exception as e:
            last = e
            print(f"[警告] select_polyline 第 {k} 次失败：{e!r}")
            try:
                _, doc = get_acad_doc(); doc.SendCommand("RE\nZ\nE\n")
            except Exception: pass
            time.sleep(0.5)
    print(f"[错误] select_polyline 在 {max_retries} 次后仍失败：{last!r}")
    return []


# ==============================================================================
#  MODULE: GEOM-UTIL (几何计算工具)
#  Level: L2 (Geometry)
# ==============================================================================

def normalize_rect(x1, y1, x2, y2):
    """
    【函数编号】: GEOM-UTIL-001
    【功能描述】: 规范化矩形坐标。确保输出为 (min_x, min_y) 和 (max_x, max_y)。
    """
    x_lo, x_hi = (x1, x2) if x1 < x2 else (x2, x1)
    y_lo, y_hi = (y1, y2) if y1 < y2 else (y2, y1)
    return (x_lo, y_lo), (x_hi, y_hi)


def pt3(x, y, z=0):
    """
    【函数编号】: GEOM-UTIL-002
    【功能描述】: 创建 win32com 兼容的 3D 点 VARIANT 对象 (VT_ARRAY | VT_R8)。
    """
    import win32com.client
    import pythoncom
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [x, y, z])

 
#&&% 隐显结合的区域选择（高亮选择并返回 PickfirstSelectionSet）


def select_entities_in_window(x1, y1, x2, y2, ty: float = 1.0, select_mode: str = "_W"):
    """
    【函数编号】: SELECT-013
    【所属模块】: 选择模块 / 交互式选择
    【功能描述】: 
        结合视口缩放 (Zoom) 和指令选择 (Select) 的高级区域选择函数。
        高亮显示选中区域，并返回 PickfirstSelectionSet (当前选中集) 的内容。
        这是一种“视觉反馈”强烈的选择方式，常用于调试或需要用户确认的场景。
    
    【依赖函数】:
        - li() (COMMON-CONN-001)
    
    【输入参数】:
        - x1, y1, x2, y2 (float): 区域对角坐标（自动规范化）。
        - ty (float): 动作间隔等待时间 (秒)。
        - select_mode (str): "_W" (窗口) 或 "_C" (交叉)。
    
    【输出参数】:
        - return (list): 选中区域内的 COM 实体列表。
    
    【逻辑流程】:
        1. 规范化坐标。
        2. 清空当前捡拾集 (PickfirstSelectionSet)。
        3. 发送 ZOOM 命令，将视口缩放至目标区域（带 20% 缓冲）。
        4. 发送 SELECT 命令，执行窗口或交叉选择。
        5. 读取 doc.PickfirstSelectionSet 获取选中对象。
        6. 清空捡拾集并返回列表。
    """
    li()
    
    # —— 归一化输入坐标 —— 
    x_lo, x_hi = sorted((x1, x2))
    y_lo, y_hi = sorted((y1, y2))

    # 先清空已有的捡拾集
    try:
        doc.Pickenabled = False
    except Exception:
        pass
    try:
        doc.PickfirstSelectionSet.Clear()
    except Exception:
        pass

    # 进行 Zoom 操作，加 20% 缓冲
    buf = 0.20 * ((x_hi - x_lo) + (y_hi - y_lo)) / 2
    zoom_cmd = (
        "_.ZOOM\n_W\n"
        f"{x_lo - buf},{y_lo - buf}\n"
        f"{x_hi + buf},{y_hi + buf}\n"
    )
    doc.SendCommand(zoom_cmd)
    time.sleep(ty)

    # 进行 Select 操作，使用归一化后的坐标和传入的 select_mode
    sel_cmd = (
        f"_.SELECT\n{select_mode}\n"
        f"{x_lo},{y_lo}\n"
        f"{x_hi},{y_hi}\n\n"
    )
    doc.SendCommand(sel_cmd)
    time.sleep(ty / 2)

    # 从 PickfirstSelectionSet 中读取实体
    selset = doc.PickfirstSelectionSet
    com_list = [ent for ent in selset]

    # 清空捡拾集，以免影响后续操作
    try:
        selset.Clear()
    except Exception:
        pass

    return com_list

#&&% 让对象处于夹点编辑状态

def set_entity_grip_state_precise(ent):
    """
    【函数编号】: SELECT-014
    【所属模块】: 交互模块 / 状态控制
    【功能描述】: 
        让指定的实体进入“夹点编辑”状态 (Grips On)。
        使用 LISP 接口 (sssetfirst) 实现，比 SendCommand(ESC) 更稳定，防止死锁。
    
    【输入参数】:
        - ent (COMObject): 目标实体。
    
    【输出参数】:
        - return (COMObject): 成功返回原对象，失败返回 None。
    
    【逻辑流程】:
        1. 获取对象 Handle 和 BoundingBox。
        2. 缩放至对象区域 (select_entities_in_window) 以确保可见。
        3. 发送 LISP (sssetfirst nil nil) 清空当前选择。
        4. 发送 LISP (sssetfirst nil (ssadd (handent Handle))) 精确选中目标。
    """
    li()

    if not ent: return None
    
    try:
        target_handle = ent.Handle
        
        # 1. 获取外包盒
        min_pt, max_pt = ent.GetBoundingBox()
        x1, y1, _ = min_pt
        x2, y2, _ = max_pt
        
        # 2. 区域选择 (利用它来 ZOOM 和获取上下文)
        # 这会让一堆对象变成夹点状态
        select_entities_in_window(x1, y1, x2, y2, ty=0.2, select_mode="_C")
        
        # =======================================================
        # 【核心修复】 LISP 强力清空
        # =======================================================
        # (sssetfirst nil nil) = 取消所有夹点，取消所有选择
        # 这是一个 LISP 指令，不是模拟按键，所以绝对不会卡死
        doc.SendCommand("(sssetfirst nil nil)\n")
        
        # 稍作停顿，确保状态更新
        time.sleep(0.1)
        
        # 3. 精准选中目标
        # 发送 LISP 使得只有目标对象进入夹点状态
        # (sssetfirst nil (ssadd (handent "Handle") (ssadd)))
        # 这句 LISP 的意思是：创建一个只包含该 Handle 的选择集，并将其设为当前夹点集
        cmd = f'(sssetfirst nil (ssadd (handent "{target_handle}") (ssadd)))\n'
        doc.SendCommand(cmd)
        
        return ent

    except Exception as e:
        print(f"[错误] 设置夹点状态失败: {e}")
        return None

#3 获取外包盒
#&&% 安全获取包围盒
def safe_get_bbox(ent, max_retry=5, delay=0.05):
    """
    【函数编号】: COMMON-UTIL-003
    【所属模块】: 基础设施 / 几何计算
    【功能描述】: 
        【核心组件】安全获取图元外包盒 (GetBoundingBox)。
        具备强制 Update 刷新机制，解决新创建对象无包围盒问题。
        具备重试机制，解决 CAD 忙碌 (Call Rejected) 问题。
        具备数据清洗功能，统一返回 Python 列表格式坐标。
    
    【输入参数】:
        - ent (COMObject): 实体对象。
        - max_retry (int): 重试次数。
        - delay (float): 重试间隔。
    
    【输出参数】:
        - return (tuple): ([min_x, min_y, min_z], [max_x, max_y, max_z])。失败返回 None。
    """


    # 如果对象本身就是空的，直接返回
    if ent is None:
        return None

    for i in range(max_retry):
        try:
            # [关键步骤] 强制刷新对象数据库
            # 这是解决 "刚创建的文字取不到包围盒" 的核心
            ent.Update()

            # 获取包围盒
            min_var, max_var = ent.GetBoundingBox()

            # [数据清洗] 确保拿到的是 Python 可用的数据
            # 有时 win32com 返回的是 tuple，有时是 SafeArray，这里做个转换保平安
            p1 = list(min_var) if hasattr(min_var, '__iter__') else min_var
            p2 = list(max_var) if hasattr(max_var, '__iter__') else max_var

            return p1, p2

        except pywintypes.com_error as e:
            hresult = e.args[0] if e.args else 0
            
            # 常见错误代码分析：
            # -2147417846: RPC_E_CALL_REJECTED (CAD 忙，例如正在自动保存或执行命令)
            # -2145386308: eInvalidExtents (对象无几何范围，常见于空文字或新对象)
            # -2147352567: 通用错误
            
            # 如果是最后一次尝试，或者错误严重，则记录日志（可选）
            if i == max_retry - 1:
                # print(f"[BBox最终失败] Handle={getattr(ent, 'Handle', 'Unknown')}, Err={hresult}")
                pass
            else:
                # 还有机会，休眠后重试
                time.sleep(delay)
                continue
                
        except Exception as e:
            # 捕获其他非 COM 错误（如 Python 逻辑错误）
            if i < max_retry - 1:
                time.sleep(delay)
                continue

    return None
    
# 4 属性获取和设置

# ==============================================================================
#  MODULE: COMMON-OBJ (对象属性访问 - L1 基础设施)
#  (此处仅保留映射表定义，具体的 get/set 函数在下方)
# ==============================================================================

# CAD标准对象类型映射（与第四部分保持一致）
_CAST_MAP = {
    # 基础几何
    "AcDbLine":"IAcadLine", "AcDbCircle":"IAcadCircle", "AcDbArc":"IAcadArc","AcDbPoint":"IAcadPoint",
    "AcDbEllipse":"IAcadEllipse", "AcDbSpline":"IAcadSpline",
    # 多段线
    "AcDbPolyline":"IAcadLWPolyline", "AcDb2dPolyline":"IAcadPolyline", "AcDb3dPolyline":"IAcad3DPolyline",
    # 文字
    "AcDbText":"IAcadText", "AcDbMText":"IAcadMText",
    # 块/属性
    "AcDbBlockReference":"IAcadBlockReference",
    "AcDbAttribute":"IAcadAttributeReference", "AcDbAttributeDefinition":"IAcadAttribute",
    # 引线/标注（常用）
    "AcDbLeader":"IAcadLeader", "AcDbMLeader":"IAcadMLeader",
    "AcDbDimension":"IAcadDimension", "AcDbAlignedDimension":"IAcadDimAligned",
    "AcDbRotatedDimension":"IAcadDimRotated", "AcDbRadialDimension":"IAcadDimRadial",
    "AcDbDiametricDimension":"IAcadDimDiametric", "AcDbArcDimension":"IAcadDimArc",
    "AcDb3PointAngularDimension":"IAcadDim3PointAngular", "AcDb2LineAngularDimension":"IAcadDim2LineAngular",
    "AcDbOrdinateDimension":"IAcadDimOrdinate",
    # 其它
    "AcDbHatch":"IAcadHatch", "AcDbTable":"IAcadTable",
}

### 天正对象属性DISPID映射

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
        'Height':       1,   # '3.5' → 高度
        'Justify':      2,   # '左下(BL)'
        'Rotation':     3,   # 0.0 度
        'TextStyle':    4,   # 'Standard'
        'Text':         5,   # '天正单行文字...'
        'Oblique':      6,   # 0.0 度（斜体角）
        # 'BigFont':    29,  # '无'，暂时不用
        'SomeSize':     30,  # 100.0，暂时占位
        'Flag40':       40,  # '是'/'否' 之类的开关
        'WidthFactor': 41,  # '1' → 宽度因子
        'Flag42':       42,  # 另一开关
    },

    # 多行天正文字（TDbMText）
    'TDbMText': {
        'Height':           1,   # '3.5'
        'Justify':          2,   # '左对齐'
        'Rotation':         3,   # 0.0 度
        'TextStyle':        4,   # 'Standard'
        'Width':            5,   # '200.0' — MText 框宽
        'LineSpacing':      6,   # '0.40' — 行距系数（猜测）
        'Oblique':          7,   # 0.0 度（可能是倾斜/其他角度）
        # 'BigFont':        29,  # '无'
        'SomeSize':         30,  # 100.0
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
        "偏移量": 11,           # 几何偏移/基线距离，当前看到是 0.0
        "文字颜色索引": 12,     # 颜色索引/枚举值
        "前缀文字": 29,         # "无" 等附加字段
        "比例数值": 30,         # 100.0 等数值形式
    },
    
}

#&&% 安全转换COM对象
def _maybe_cast(ent):
    """
    【函数编号】: COMMON-OBJ-001-AUX
    【功能描述】: 内部辅助。安全地将 CAD 图元对象转换为特定的 COM 接口类型。
    """
    try:
        name = com_retry(lambda: ent.ObjectName)
        iface = _CAST_MAP.get(name)
        if iface:
            try:
                return CastTo(ent, iface)
            except Exception:
                return ent
        return ent
    except Exception:
        return ent

#&&% 转换对象
def cast_object(obj):
    """
    【函数编号】: COMMON-OBJ-001
    【功能描述】: 公开接口。将对象转换为具体的 CAD 接口对象（如 IAcadLine）。
    """
    return _maybe_cast(obj)

#&&% 获取对象属性
def get_object_property(obj, property_name):
    """
    【函数编号】: COMMON-OBJ-002
    【所属模块】: 通用对象属性
    【功能描述】: 
        统一获取对象属性值。
        自动区分标准 CAD 对象（Cast 后 getattr）和天正对象（Invoke DISPID）。
    """
    try:
        obj_name = com_retry(lambda: obj.ObjectName)
        # 天正对象：使用DISPID方式访问
        if obj_name in _TARCH_PROPERTY_MAP:
            dispid = _TARCH_PROPERTY_MAP[obj_name].get(property_name)
            if dispid:
                return obj._oleobj_.Invoke(dispid, 0, pythoncom.DISPATCH_PROPERTYGET, True)
        # CAD标准对象：先Cast再访问属性
        obj = _maybe_cast(obj)
        return getattr(obj, property_name)
    except Exception as e:
        return None

#&&% 设置对象属性
def set_object_property(obj, property_name, value):
    """
    【函数编号】: COMMON-OBJ-003
    【所属模块】: 通用对象属性
    【功能描述】: 
        统一设置对象属性值。
        自动区分标准 CAD 对象（setattr）和天正对象（Invoke PUT）。
    """
    try:
        obj_name = com_retry(lambda: obj.ObjectName)
        # 天正对象：使用DISPID方式设置
        if obj_name in _TARCH_PROPERTY_MAP:
            dispid = _TARCH_PROPERTY_MAP[obj_name].get(property_name)
            if dispid:
                obj._oleobj_.Invoke(dispid, 0, pythoncom.DISPATCH_PROPERTYPUT, True, value)
                return True
        # CAD标准对象：先Cast再设置属性
        obj = _maybe_cast(obj)
        setattr(obj, property_name, value)
        return True
    except Exception as e:
        return False

#&&% 安全获取属性
def get_attr(obj, name):
    """
    【函数编号】: COMMON-OBJ-004
    【功能描述】: 
        高级获取。先尝试通用机制 (get_object_property)，失败则退回原生 getattr。
    """
    val = get_object_property(obj, name)
    if val is None:
        try:
            val = getattr(obj, name)
        except Exception:
            val = None
    return val


#&&% 安全设置属性
def set_attr(obj, name, value):
    """
    【函数编号】: COMMON-OBJ-005
    【功能描述】: 
        高级设置。先尝试通用机制 (set_object_property)，失败则退回原生 setattr。
    """
    if not set_object_property(obj, name, value):
        try:
            setattr(obj, name, value)
        except Exception:
            return False
    return True


##属性探测器

#&&% 暴力获取天正属性
def brute_dump_tarch_props(ent, max_dispid=64):
    """
    【函数编号】: DEBUG-TARCH-001
    【所属模块】: 调试工具
    【功能描述】: 
        暴力枚举 DISPID，探测未知天正对象的属性。用于开发阶段分析。
    """
    ole = ent._oleobj_
    obj_name = getattr(ent, "ObjectName", "<no ObjectName>")
    print(f"=== brute_dump_tarch_props: ObjectName = {obj_name}, max_dispid = {max_dispid} ===")

    for dispid in range(1, max_dispid + 1):
        try:
            # 直接按 "返回一个 VARIANT" 来读
            val = ole.InvokeTypes(
                dispid,
                0,
                pythoncom.DISPATCH_PROPERTYGET,
                (pythoncom.VT_VARIANT, 0),
                ()
            )
            print(f"DISPID {dispid:2d} -> {repr(val)}")
        except pythoncom.com_error:
            # 这个 dispid 不对应属性（可能是方法、或根本不存在），忽略
            continue
        except Exception as e:
            print(f"DISPID {dispid:2d} 异常: {e}")


#5排序
#&&% * 对列表实体进行从上到下、从左到右的排序

#&&% 左下角排序
def sort_coms_by_llcorner(com_list, cha_Y=2000):
    """
    【函数编号】: COMMON-SORT-001
    【所属模块】: 通用排序
    【功能描述】: 
        按实体外包盒【左下角】排序。
        主序：Y 轴降序 (上 -> 下)。
        次序：X 轴升序 (左 -> 右)。适用于常见的横向排版图纸。
    
    【输入参数】:
        - com_list (list): 实体列表。
        - cha_Y (float): 行高容差。小于此值的 Y 差视为同一行。
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
    【函数编号】: COMMON-SORT-002
    【所属模块】: 通用排序
    【功能描述】: 
        按实体外包盒【右上角】排序。
        主序：X 轴降序 (右 -> 左)。
        次序：Y 轴降序 (上 -> 下)。适用于竖向排版或已旋转 90 度的图纸。
    
    【输入参数】:
        - com_list (list): 实体列表。
        - cha_X (float): 列宽容差。
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

#&&% 中心点排序
def sort_coms_by_center(objs, tol_x=100):
    """
    【函数编号】: COMMON-SORT-003
    【所属模块】: 通用排序
    【功能描述】: 
        按实体【中心点】排序。
        主序：X 轴升序 (左 -> 右) 分组。
        次序：组内 Y 轴降序 (上 -> 下)。
    
    【输入参数】:
        - objs (list): 实体列表。
        - tol_x (float): 分组容差。X 差值小于此值的视为同一列/组。
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


# ==============================================================================
#  MODULE: DRAW (绘图操作)
#  Level: L4 (Drawing)
# ==============================================================================

# 6 基本绘图

#&&% 绘制点
def draw_point(pt):
    """
    【函数编号】: DRAW-001
    【所属模块】: 绘图模块
    【功能描述】: 在模型空间绘制一个点 (POINT)。
    
    【输入参数】:
        - pt (tuple): (x, y, z) 坐标。
    
    【输出参数】:
        - return (COMObject): 新建的点对象，失败返回 None。
    """
    try:
        # AutoCAD 的“点”由 AddPoint 创建，需传 VARIANT
        obj = mp.AddPoint(vtpnt(*pt))
        return obj
    except Exception as e:
        print(f"[错误] 无法绘制点: {e}")
        return None

#&&% 绘制直线
def draw_line(p1, p2):#从两点坐标返回直线段
    """
    【函数编号】: DRAW-002
    【所属模块】: 绘图模块
    【功能描述】: 在模型空间绘制一条直线 (LINE)。
    
    【输入参数】:
        - p1, p2 (tuple): (x, y, z) 端点坐标。
    
    【输出参数】:
        - return (COMObject): 新建的直线对象，失败返回 None。
    """
    try:
        line_obj = mp.AddLine(vtpnt(*p1), vtpnt(*p2))
        return line_obj
    except Exception as e:
        print(f"[错误] 无法绘制直线: {e}")
        return None


#&&% 绘制圆
def draw_circle(center, radius):
    """
    【函数编号】: DRAW-003
    【所属模块】: 绘图模块
    【功能描述】: 在模型空间绘制一个圆 (CIRCLE)。
    
    【输入参数】:
        - center (tuple): (x, y, z) 圆心坐标。
        - radius (float): 半径。
    
    【输出参数】:
        - return (COMObject): 新建的圆对象，失败返回 None。
    """
    try:
        obj = mp.AddCircle(vtpnt(*center), radius)
        return obj
    except Exception as e:
        print(f"[错误] 无法绘制圆: {e}")
        return None


#&&% 绘制正多边形
def draw_regular_polygon(center, radius, sides):
    """
    【函数编号】: DRAW-004
    【所属模块】: 绘图模块
    【功能描述】: 
        绘制正多边形。实质是绘制一个闭合的轻量多段线 (LWPOLYLINE)。
    
    【输入参数】:
        - center (tuple): 圆心。
        - radius (float): 外接圆半径。
        - sides (int): 边数 (>=3)。
    
    【输出参数】:
        - return (COMObject): 新建的多段线对象，失败返回 None。
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
        print(f"[错误] 无法绘制正多边形: {e}")
        return None

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
    【函数编号】: DRAW-005
    【所属模块】: 绘图模块
    【功能描述】: 
        绘制轻量级多段线 (LWPOLYLINE)。仅使用 X, Y 坐标。
        支持自动创建图层、设置宽度、颜色和闭合属性。
    
    【输入参数】:
        - coords3d (list): [(x1,y1,z1), ...] 坐标列表。
        - layer_name (str): 目标图层。
        - width (float): 线宽 (ConstantWidth)。
        - color (int): 颜色索引。
        - closed (bool): 是否闭合。
    
    【输出参数】:
        - return (COMObject): 新建的多段线对象。
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

        print(f"[OK] 已在图层『{layer_name}』绘制多段线，Closed = {closed}")
        return pline
    except Exception as e:
        print("[错误] 绘制多段线失败:", e) 

   # 5️⃣ 返回新对象

    return pline

#&&% 绘制多段线
def draw_polyline(vertices,
                  layer_name="测试辅助",
                  tol=0.5,
                  width=20,
                  color=1):
    """
    【函数编号】: DRAW-006
    【所属模块】: 绘图模块
    【功能描述】: 
        绘制传统（重型）多段线 (POLYLINE - 2D/3D)。
        包含输入校验、坐标扁平化、自动图层创建和闭合检测。
    
    【输入参数】:
        - vertices (list): [(x,y,z), ...] 顶点列表。
        - layer_name (str): 目标图层。
        - tol (float): 闭合检测容差。
        - width (float): 线宽。
        - color (int): 颜色索引。
    
    【输出参数】:
        - return (COMObject): 新建的多段线对象。
    """

    # ----------------- 内部工具 -----------------
##    def same_point(p1, p2, _tol=tol):
##        """只比较 x、y 坐标的近似相等"""
##        return abs(p1[0] - p2[0]) <= _tol and abs(p1[1] - p2[1]) <= _tol
    # --------------------------------------------

    # ---------- 输入校验 ----------
    if not vertices or not isinstance(vertices, (list, tuple)):
        print("[错误] 请输入有效的顶点列表")
        return None
    if not isinstance(vertices[0], (list, tuple)) or len(vertices[0]) < 3:
        print("[错误] 顶点格式错误，应为 (x, y, z)")
        return None

    # --------- 处理闭合性 ---------
    is_closed = same_point(vertices[0], vertices[-1])

    # --------- 打印调试信息 --------
    print("调试：绘制多段线的顶点序列")
    for idx, pt in enumerate(vertices):
        print(f"  {idx}: {pt}")

    # --------- 生成 SAFEARRAY ------
    flat = []
    for x, y, z in vertices:
        flat.extend([x, y, z])
    coords_var = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, tuple(flat))

    # ---------- 确保图层存在 -------
    try:
        _ = doc.Layers.Item(layer_name)
    except Exception:
        doc.Layers.Add(layer_name)

    # ---------- 绘制多段线 ----------
    try:
        pl = doc.ModelSpace.AddPolyline(coords_var)
        pl.Closed = is_closed
        pl.Layer = layer_name
        pl.color = color
        pl.ConstantWidth = width
        pl.Update()
        doc.Regen(0)
        print(f"[OK] 已在图层『{layer_name}』绘制多段线，Closed = {is_closed}")
        return pl
    except Exception as e:
        print("[错误] 绘制多段线失败:", e)
        return None
