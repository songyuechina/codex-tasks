#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CAD文件操作统一接口

提供DWG文件的打开、新建、关闭、保存、另存、插入等基础操作
所有函数都集成了协同机制，可直接调用
"""
#D:/claude-tasks/cad/scripts/CAD_file_operations.py
# V1.0版

#&&&&%% （一）  可移植性导入
import sys
import os
import time
import shutil
import psutil
import math
from pathlib import Path

import win32api



# --- COM 相关库 ---
import pythoncom
import win32com.client
from win32com.client import VARIANT, constants

current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

from system.project_setup import PathConfig



# 定义资源目录
XITONG_DIR = PathConfig.CAD_DIR / "xitongwenjian"
LOGS_DIR = PathConfig.CAD_DIR / "logs"
TESTS_DIR = PathConfig.WORKSPACE_DIR / "tests"
STATUS_MESSAGES_FILE = PathConfig.SCRIPTS_DIR / "CAD_status_messages.txt"

userpath=os.environ.get('USERPATH')


# ================= 3. 导入模块 =================

# 3.1 导入 System 工具
try:
    from system.CAD_com_utils import retry_on_busy, retry_if_busy,SafeCOM,sys_logger
except ImportError as e:
    print(f"[严重错误] 无法导入 CAD_com_utils: {e}")
    # 这里不raise，后续可能会定义假的 retry_on_busy 兜底

# 3.2 导入 CAD 基础功能 (CAD_basic)
try:
    import scripts.CAD_basic as cb
    from scripts.CAD_basic import (
        close_all_cad_processes,
        start_applicationV9,
        get_acad_doc,
        jingchengshu_wenjian,


        safe_delete,
        last_obj,
        group_bbox_corners,
        com_retry,
        get_object_property,
        ensure_list,
        
    )
except ImportError as e:
    print(f"[严重错误] 无法导入 CAD_basic: {e}")
    raise e

# 3.3 导入 CAD 操作范式 (CAD_basic_operations)
try:
    from system.CAD_basic_operations import (
        open_dwg_paradigm,
        new_dwg_enhanced,
        save_current_dwg_paradigm,
        save_as_dwg_paradigm,
        close_current_dwg_paradigm,
        close_all_dwg_paradigm
    )


except ImportError as e:
    print(f"[警告] CAD_basic_operations 导入失败: {e}")
    # 定义临时替代函数
    def open_dwg_paradigm(*args, **kwargs):
        print("[错误] open_dwg_paradigm 功能不可用")
        return False

# 3.4 导入 选择模块 (CAD_selection)
try:
    from system.CAD_selection import *


except ImportError as e:
    print(f"[警告] CAD_selection 导入失败: {e}")






# ==============================================================================
# 4. [核心增强] 智能连接与全局变量同步 (Licad / CAD_basic 双核)
# ==============================================================================

# 初始化模块级全局变量 (占位符)
acad = None
doc = None
mp = None
sp = None

try:
    # --- 方案 A: 尝试使用新核心 licad ---
    import licad
    from licad import C
    # 尝试从 licad 导入 retry_on_busy，如果前面没导入成功的话
    if 'retry_on_busy' not in globals():
        from licad import retry_on_busy
    
    print("[初始化] 成功加载 licad 核心模块")

    def li():
        """
        【模式 A: 新核心】调用 licad.li() 并同步全局变量
        """
        global acad, doc, mp, sp
        
        # 1. 调用 licad 的强力连接
        is_connected = licad.li()
        
        if is_connected:
            # 2. 桥接数据：把 C 的属性注入给本脚本的全局变量
            acad = C.acad
            doc = C.doc
            mp = C.mp
            sp = C.sp
            return True
        return False

except ImportError:
    # --- 方案 B: 回退使用老核心 CAD_basic ---
    print("[注意] 未找到 licad，回退使用 CAD_basic (cb) 模式")
    
    # 兜底装饰器 (如果 CAD_com_utils 也没导入成功)
    if 'retry_on_busy' not in globals():
        def retry_on_busy(func): return func

    def li():
        """
        【模式 B: 老核心】调用 cb.li() 并同步全局变量
        """
        global acad, doc, mp, sp
        
        try:
            # 调用 CAD_basic 的连接
            result = cb.li()
        except Exception:
            result = False
        
        if result:
            # 从 CAD_basic 模块同步变量
            acad = cb.acad
            doc = cb.doc
            mp = cb.mp
            sp = cb.sp
            return True
        else:
            return False

# ================= 5. 初始化完成 =================
CURRENT_FILE = Path(__file__).resolve()
print(f"[初始化] 脚本环境加载完成: {CURRENT_FILE.name}")


# ==============================================================================
#                            API MANIFEST / 完整函数签名清单
# ==============================================================================
"""
1. 系统初始化与连接 (System Initialization & Connection)
--------------------------------------------------------------------------------
[SYS-INIT-001] li()
               : [核心] 智能连接接口。尝试连接现有 CAD 实例并同步全局变量 (acad, doc, mp, sp)。
                 支持 licad 新核心与 CAD_basic 老核心自动切换。

[SYS-INIT-002] litz(max_connect_rounds=3, wait_between_rounds=2.0)
               : [核心] 天正环境灾难恢复与智能重连。
                 含探针检测、进程自杀重启、等待就绪循环。

2. 进程与基础控制 (Process & Basic Control)
--------------------------------------------------------------------------------
[SYS-CTRL-001] launch_tarch_CAD_system()
               : 启动天正 CAD 系统。
[SYS-CTRL-002] close_tarch_CAD_system()
               : 关闭所有 CAD 进程。
[SYS-CTRL-003] launch_cad_guardians()
               : 启动守护进程 (弹窗杀手 + 命令监控)。

3. 状态控制与恢复 (State Control & Recovery)
--------------------------------------------------------------------------------
[STATE-001]    activate_document_by_name(filename)
               : 激活已打开的指定名称文档。
[STATE-002]    cad_zt_zero()
               : 状态归零 (0进程)。
[STATE-003]    cad_zt_oneb()
               : 状态归一·白 (1进程 + 1空白/默认文件)。
[STATE-004]    cad_zt_oned(file_path)
               : 状态归一·定 (1进程 + 1指定文件)。
[STATE-005]    cad_zt_two(file1, file2)
               : 状态归二 (1进程 + 2指定文件)。
[STATE-006]    cad_zt_much(file1, file2, file3)
               : 状态归三 (1进程 + 3指定文件)。
[STATE-007]    cad_zt_xin_1(status_file=None)
               : [记录] 将当前打开文件列表、激活文件、PID 等写入 JSON。
[STATE-008]    cad_zt_xin_2(status_file=None)
               : [恢复] 读取 JSON，重启 CAD 并恢复之前的文件现场。

4. 单文档 I/O 操作 (Single Document I/O)
--------------------------------------------------------------------------------
[IO-DOC-001]   new_file(output_path=None, close_after=False)
               : 新建 DWG 文件 (支持覆盖、创建后自动关闭)。
[IO-DOC-002]   open_file(file_path)
               : [核心] 打开 DWG 文件。集成进程守护、负载控制(自动关闭多余文件)、幂等激活。
[IO-DOC-003]   copy_file_with_increment(filepath)
               : 复制文件并自动递增文件名 (file-1.dwg, file-2.dwg...)。
[IO-DOC-004]   save_file()
               : 保存当前文件。
[IO-DOC-005]   save_file_as(output_path)
               : 另存为。
[IO-DOC-006]   close_file(save_option="auto_save")
               : 关闭当前文件 (支持 auto_save, no_save)。
[IO-DOC-007]   purge_file(deep_purge=True)
               : 清理文件垃圾 (PurgeAll)。
[IO-DOC-008]   check_file_locked(filepath)
               : 检查文件是否被锁定 (.dwl 检测)。
[IO-DOC-009]   is_read_only()
               : 检查当前文档是否只读。

5. 跨文件与内容操作 (Cross-File & Content Ops)
--------------------------------------------------------------------------------
[IO-X-001]     insert_file_exploded(source_file, ..., explode=True)
               : 插入外部文件并炸开 (支持 INSBASE 自动纠偏)。
[IO-X-002]     copy_file_content_pywin32(source_file, target_file, ...)
               : [全图] 全图内容复制。通过临时副本+InsertBlock+Explode 实现。
[IO-X-003]     insert_region_v2(src_dwg, target_dwg, x1, y1, x2, y2, ...)
               : [区域] 跨文件区域复制。通过 WBlock 提取选区+数学偏移插入。

6. 多文档与空间控制 (Multi-Doc & Space Control)
--------------------------------------------------------------------------------
[MDOC-001]     set_active_doc(doc)
               : 设置激活文档对象。
[MDOC-002]     get_doc_by_name(name)
               : 按文件名获取文档对象。
[MDOC-003]     get_open_document_names()
               : 获取所有打开文档的名称列表。
[MDOC-004]     close_current_drawing_safely()
               : 安全关闭当前文档并重连。
[MDOC-005]     close_all_except_active_safe()
               : 关闭除当前激活文档外的所有文件。
[MDOC-006]     close_dwg_by_name(Name)
               : 按名称关闭特定文档。
[MDOC-007]     close_all_files(save_option="auto_save")
               : 关闭所有文件。
[MDOC-008]     ensure_max_open_documents(keep_filename, max_count=3)
               : 强制限制打开文件数量 (防止内存溢出)。

[SPACE-001]    get_obj_loc(obj)
               : 获取对象所在空间 (1=Model, 0=Paper)。
[SPACE-002]    set_space_mode(mode_val)
               : 切换空间 (TILEMODE)。
[SPACE-003]    switch_to_layout(layout_name, ...)
               : 切换到指定布局 (含命令兜底重试)。
[SPACE-004]    get_layout_names(exclude_model=False)
               : 获取布局名称列表。

7. 路径工具 (Path Utilities)
--------------------------------------------------------------------------------
[PATH-001]     get_current_dwg_path()
               : 获取当前激活文档的长路径。
[PATH-002]     get_all_open_dwg_paths()
               : 获取所有打开文档的长路径列表。
[PATH-003]     get_long_path(path_str)
               : 路径标准化 (短路径转长路径)。

8. 天正专业操作 (TArch Operations)
--------------------------------------------------------------------------------
[TARCH-001]    dim_by_points(p1, p2, p3)
               : 天正逐点标注。
[TARCH-002]    draw_tarch_wall(p1, p2, thickness=240)
               : 绘制天正墙体。
[TARCH-003]    insert_tarch_door(p, width, height)
               : 插入天正门。
[TARCH-004]    insert_tarch_window(p, width, height, window_type, ...)
               : 插入天正窗 (含自动图层匹配和属性刷)。
[TARCH-005]    run_tupdspace_for_tz_room_in_rect(...)
               : [核心] 区域生成天正房间 (调用 TUPDSPACE)。
[TARCH-006]    run_auto_TUPDSPACE_with_coord(coord, ...)
               : 调用子进程执行生成房间命令。
[TARCH-007]    TDb_single_line_variable_wall(...)
               : 单线变墙 (直接转换)。
[TARCH-008]    convert_lines_to_walls(...)
               : 批量线转墙 (临时墙过渡法)。
[TARCH-009]    set_walls_thickness(...)
               : 批量设置墙厚。
"""

__all__ = [
    # --- 1. 系统初始化与连接 ---
    'li', 'litz', 
    'launch_tarch_CAD_system', 'close_tarch_CAD_system', 'launch_cad_guardians',

    # --- 2. 状态控制与恢复 ---
    'activate_document_by_name', 
    'cad_zt_zero', 'cad_zt_oneb', 'cad_zt_oned', 
    'cad_zt_two', 'cad_zt_much', 
    'cad_zt_xin_1', 'cad_zt_xin_2',

    # --- 3. 单文档 I/O 操作 ---
    'new_file', 'open_file', 'copy_file_with_increment',
    'save_file', 'save_file_as', 'close_file', 
    'purge_file', 'check_file_locked', 'is_read_only',

    # --- 4. 跨文件与内容操作 ---
    'insert_file_exploded', 'copy_file_content_pywin32', 'insert_region_v2',

    # --- 5. 多文档与空间控制 ---
    'set_active_doc', 'get_doc_by_name', 'get_open_document_names',
    'close_current_drawing_safely', 'close_all_except_active_safe',
    'close_dwg_by_name', 'close_all_files', 'ensure_max_open_documents',
    'get_obj_loc', 'set_space_mode', 'switch_to_layout', 'get_layout_names',

    # --- 6. 路径工具 ---
    'get_current_dwg_path', 'get_all_open_dwg_paths', 'get_long_path',

    # --- 7. 天正专业操作 ---
    'dim_by_points', 'draw_tarch_wall', 'insert_tarch_door', 'insert_tarch_window',
    'run_tupdspace_for_tz_room_in_rect', 'run_auto_TUPDSPACE_with_coord',
    'TDb_single_line_variable_wall', 'convert_lines_to_walls', 'set_walls_thickness'
]


#&&&&%% （二）  文件基础操作

#&&&% 系统界面控制


#&&% 启动天正CAD系统

def launch_tarch_CAD_system():

    return cb.st()


#&&% 关闭天正CAD系统

def close_tarch_CAD_system():

    return cb.close_all_cad_processes()


#&&% 守护天正CAD系统
def launch_cad_guardians():
    """
    【功能】: 独立启动 CAD 的两个守护脚本（弹窗杀手 + 命令监控）。
    【特性】: 支持系统任意移动，路径自动识别。
    """
    # ========================================================
    # 1. 动态获取路径 (核心修改)
    # ========================================================
    # 当前文件: .../cad/scripts/CAD_file_operations.py
    current_script = Path(__file__).resolve()
    
    # 项目根目录: .../cad
    project_root = current_script.parent.parent
    
    # 目标目录: .../cad/system
    system_dir = project_root / "system"
    # ========================================================

    scripts_to_launch = [
        "cad_dialog_killer.py",
        "cad_command_monitor.py"
    ]

    print(f"🛡️ [守护] 正在从 [{system_dir.name}] 启动守护进程...")
    
    success_count = 0

    for script_name in scripts_to_launch:
        # 拼接完整路径
        script_path = system_dir / script_name
        
        if not script_path.exists():
            print(f"❌ [错误] 找不到脚本: {script_path}")
            continue

        try:
            creation_flags = subprocess.CREATE_NO_WINDOW
            
            # 启动进程 (注意：cwd 参数也使用动态路径)
            proc = subprocess.Popen(
                [sys.executable, str(script_path)], # 路径转为字符串
                creationflags=creation_flags,
                cwd=str(system_dir)                 # 工作目录设为 system
            )
            
            time.sleep(0.5)
            
            if proc.poll() is None:
                print(f"✅ [启动] {script_name} 成功 (PID: {proc.pid})")
                success_count += 1
            else:
                print(f"ℹ️ [跳过] {script_name} 已在运行中。")
                success_count += 1
                
        except Exception as e:
            print(f"❌ [异常] 无法启动 {script_name}: {e}")

    return success_count == len(scripts_to_launch)



#&&% 连接天正CAD系统
def litz(max_connect_rounds: int = 3, wait_between_rounds: float = 2.0):
    """
    
    
    【功能】: 
        天正环境灾难恢复与智能重连 (C类单例版)。
    
    【逻辑闭环】:
        1. 尝试连接: 调用 C.li() 尝试获取现有连接。
        2. 探针验证: 如果连接成功，画墙测试是否为有效天正环境。
        3. 灾难重建: 如果验证失败，杀进程 -> 启动天正 -> 等待。
        4. 状态刷新: 再次调用 C.li()，由 C 类统一接管新实例。
        5. 无需反向注入: 所有模块通过访问 C.doc, C.acad 自动获取最新状态。
    """
    import time
    
    # 引用全局单例 (假设文件头部已 import licad.C as C 或类似)
    # from system.licad import C 
    
    # ========= 第一阶段：常规检查 (利用 C.li) =========
    print("[litz] 开始环境健康检查...")
    is_connected = False
    try:
        if C.li():
            is_connected = True
    except:
        pass

    if is_connected:
        # 【探针】画天正墙检测
        try:
            # draw_tarch_wall 需确保已导入
            test_res = draw_tarch_wall((0, 0, 0), (1000, 0, 0))
        except Exception:
            test_res = False

        if test_res:
            # 验证通过，清理垃圾
            try:
                obj = last_obj()
                if obj: safe_delete(obj)
            except: pass
            
            print(f"[litz] 环境检测正常，复用现有进程: {C.doc.Name}")
            return True
        else:
            print("[litz] 连接正常但探针检测失败（疑似非天正环境），准备重建...")
    else:
        print("[litz] 基础连接 C.li() 失败，准备重建...")

    # ========= 第二阶段：环境重置 (Kill & Restart) =========
    print("[litz] 执行环境重置...")
    try:
        # 调用 CAD_basic 中的关闭进程函数
        close_all_cad_processes()
    except Exception as e:
        print(f"[litz] 关闭进程警告: {e}")

    try:
        # 启动天正 (调用本模块或 CAD_basic 的启动函数)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
    except Exception as e:
        print(f"[litz] 启动天正失败: {e}")
        return False

    # ========= 第三阶段：等待并刷新 C 类 =========
    print("[litz] 正在等待 CAD 初始化并刷新 C 类连接...")
    
    success = False
    
    # 循环尝试连接，给 CAD 启动留出时间
    # 这里的关键是：我们不再自己去 GetActiveObject，而是不断呼叫 C.li()
    # C.li() 内部封装了 GetActiveObject 和异常处理
    
    for round_idx in range(1, max_connect_rounds + 1):
        if round_idx > 1:
            print(f"[litz] 第 {round_idx} 轮重试...")
            time.sleep(wait_between_rounds)
        
        # 尝试刷新连接
        if C.li():
            # 再次用探针确认（防止连接到了一个还没加载完插件的空壳 CAD）
            try:
                # 稍微等一下 ModelSpace
                if C.mp is None:
                    time.sleep(1.0)
                    C.li() # 再刷一次
                
                # 只有 C.doc 和 C.mp 都就绪才算成功
                if C.doc and C.mp:
                    success = True
                    break
            except:
                pass
                
        time.sleep(1.0) # 短暂冷却

    if success:
        print(f"[litz] 连接重建完成，C 类已同步。当前激活文档: {C.doc.Name}")
        return True
    else:
        print("[litz] 严重错误：重启后 C.li() 无法建立有效连接。")
        return False



#&&&% CAD状态控制


#&&% 激活桌面指定文件
@retry_if_busy(max_retries=5, delay=1.0)
def activate_document_by_name(filename):
    """
    激活指定文件名的文档为当前操作对象

    Args:
        filename: 支持绝对/相对路径或单纯文件名

    Returns:
        bool: 成功返回True，失败返回False
    """

    target = Path(filename).name.lower()
    open_docs = get_open_document_names()
    normalized = {Path(name).name.lower(): name for name in open_docs}

    if target not in normalized:
        print(f"[错误] 文件 {filename} 未在当前 CAD 会话中打开")
        return False

    actual_name = normalized[target]
    doc = get_doc_by_name(actual_name)
    if doc is None:
        print(f"[错误] 无法获取文件 {actual_name} 的文档对象")
        return False

    try:
        set_active_doc(doc)
    except Exception as exc:
        print(f"[错误] 激活文件 {actual_name} 失败: {exc}")
        return False

    if not C.li():
        print("[警告] li() 连接失败，当前控制对象未确定")
        return False

    print(f"[成功] 已激活文件: {actual_name}")
    return True

#&&% 状态归零

def cad_zt_zero():
    """
    确保CAD进程数为0（关闭所有CAD）
    """
    import sys
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import jingchengshu_wenjian, close_all_cad_processes

    shu = jingchengshu_wenjian()
    if shu > 0:
        close_all_cad_processes()
    return True

#&&% 标准归一状态

def cad_zt_oneb():
    """
    确保CAD状态为：1个进程+1个空白文件（单文件不确定状态）
    """
    import time
    from CAD_basic import (
        jingchengshu_wenjian,
        close_all_cad_processes,
        start_applicationV9,
        
        
    )
    from system.CAD_coordination import wait_quiescent

    shu = jingchengshu_wenjian()
    if shu == 0:
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
    elif shu == 1:
        def _is_default_session(paths):
            if not paths:
                return True
            if len(paths) != 1:
                return False
            entry = str(paths[0]).strip()
            entry_lower = entry.lower()
            if not entry or ":" in entry or "\\" in entry or "/" in entry:
                return False
            return entry_lower.startswith("drawing") and entry_lower.endswith(".dwg")

        try:
            C.li()
        except Exception:
            pass

        try:
            open_paths = get_all_open_dwg_paths()
        except Exception as exc:
            print(f"[cad_zt_oneb] 获取打开文件失败：{exc}")
            open_paths = []

        print(f"[cad_zt_oneb] 当前打开文件列表: {open_paths}")

        if _is_default_session(open_paths):
            print("[cad_zt_oneb] 检测到天正默认空白 DWG，保持现状。")
            return True

        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
    elif shu > 1:
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
    return True


#&&% 归一状态
def cad_zt_oned(file_path=str(XITONG_DIR / "0.dwg")):
    """
    确保CAD状态为：1个进程+1个指定文件（单文件确定状态）

    Args:
        file_path: 要打开的文件路径，默认为 cad/xitongwenjian/0.dwg
    """
    import sys
    import time
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import jingchengshu_wenjian, close_all_cad_processes, start_applicationV9 
    
    from system.CAD_coordination import wait_quiescent

    shu = jingchengshu_wenjian()
    if shu == 0:
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file_path)
    elif shu > 1:
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file_path)
    elif shu == 1:
        
        C.li()
        close_all_except_active_safe()
    return True

#&&% 归二状态

def cad_zt_two(file1=str(XITONG_DIR / "0.dwg"), file2=str(XITONG_DIR / "1.dwg")):
    """
    确保CAD状态为：1个进程+2个文件（双文件确定状态）

    Args:
        file1: 第一个文件路径
        file2: 第二个文件路径
    """
    import sys
    import time
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import jingchengshu_wenjian, close_all_cad_processes, start_applicationV9
    
    from system.CAD_coordination import wait_quiescent

    shu = jingchengshu_wenjian()
    if shu == 0:
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
    elif shu > 1:
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
    elif shu == 1:
        
        C.li()
        open_docs = get_open_document_names()
        # 如果文件数多于2，关闭多余的
        while len(open_docs) > 2:
            close_dwg_by_name(open_docs[0])
            open_docs = get_open_document_names()
        # 如果文件数少于2，打开文件凑到2个
        files_to_open = [file1, file2]
        idx = 0
        while len(open_docs) < 2 and idx < len(files_to_open):
            open_file(files_to_open[idx])
            idx += 1
            open_docs = get_open_document_names()
    return True

#&&% 归三状态

def cad_zt_much(
    file1=str(XITONG_DIR / "0.dwg"),
    file2=str(XITONG_DIR / "1.dwg"),
    file3=str(XITONG_DIR / "2.dwg")
):
    """
    确保CAD状态为：1个进程+多个文件（>2个文件）

    Args:
        file1: 第一个文件路径
        file2: 第二个文件路径
        file3: 第三个文件路径
    """
    import sys
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import jingchengshu_wenjian, close_all_cad_processes, start_applicationV9
    

    shu = jingchengshu_wenjian()
    if shu == 0:
        import time
        from system.CAD_coordination import wait_quiescent
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
        open_file(file3)
    elif shu > 1:
        import time
        from system.CAD_coordination import wait_quiescent
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
        open_file(file3)
    elif shu == 1:
        
        C.li()
        open_docs = get_open_document_names()
        files_to_open = [file1, file2, file3]
        for f in files_to_open:
            if len(open_docs) >= 3:
                break
            open_file(f)
            open_docs = get_open_document_names()
    return True

#&&% 记录当前状态
@retry_if_busy(max_retries=3, delay=1.0)
def cad_zt_xin_1(status_file=None):
    """
    【V2.1 修复版】记录当前 CAD 桌面信息，写入 JSON 状态文件。
    1. 修复 datetime 未定义错误
    2. 修复 NoneType 属性访问错误
    3. 增加文件夹路径反向推导功能
    """
    # ================= 1. 必要的局部导入 =================
    import json
    import os
    import sys
    from datetime import datetime
    from pathlib import Path
    
    # 导入系统配置
    try:
        from system.project_setup import PathConfig
        from system.licad import C
        from scripts.CAD_basic import get_all_open_dwg_paths, current_dwg_folder
    except ImportError as e:
        print(f"[错误] 模块导入失败: {e}")
        return None

    # ================= 2. 路径处理 =================
    # 如果未指定文件，使用默认日志路径
    if status_file is None:
        status_file = PathConfig.LOGS / "cad_status.json"
    
    status_path = Path(status_file)
    try:
        status_path.parent.mkdir(parents=True, exist_ok=True)
    except: pass

    # ================= 3. 尝试连接 =================
    try:
        # 刷新连接，如果彻底连不上则放弃
        if not C.li():
            print("[cad_zt_xin_1] li() 连接失败，无法记录当前会话。")
            return None
    except Exception:
        return None

    # ================= 4. 安全获取数据 =================
    
    # A. 获取打开的文件列表
    open_paths = []
    try:
        open_paths = get_all_open_dwg_paths() or []
    except Exception:
        pass

    # B. 获取当前文件夹 (允许失败，下面有补救措施)
    active_folder = None
    try:
        active_folder = current_dwg_folder()
    except Exception:
        # 这里不要打印错误，以免刷屏， silently fail
        active_folder = None

    # C. 获取当前文档属性
    active_name = None
    active_full = None
    
    try:
        # 使用 getattr 防止 C.doc 不存在
        active_doc = getattr(C, "doc", None)
        
        if active_doc is not None:
            # 尝试获取 Name 和 FullName
            # 注意：新建未保存的文件 FullName 可能为空字符串
            active_name = getattr(active_doc, "Name", None)
            active_full = getattr(active_doc, "FullName", None)
    except Exception:
        # 如果 COM 忙碌或出错，保持为 None
        pass

    # ================= 5. 逻辑补救 (关键修复) =================
    
    # 情况1: 有全路径，但没获取到文件夹 -> 从全路径推导文件夹
    if active_full and (not active_folder):
        try:
            active_folder = str(Path(active_full).parent)
        except: pass

    # 情况2: 有文件夹和文件名，但没全路径 -> 拼接全路径
    if (not active_full) and active_folder and active_name:
        try:
            active_full = str(Path(active_folder) / active_name)
        except: pass

    # ================= 6. 构造并写入 =================
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "open_files": open_paths,
        "active_folder": active_folder,
        "active_file": active_full,
        "active_name": active_name,
        "pid": os.getpid()
    }

    try:
        status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[cad_zt_xin_1] 已写入 CAD 状态信息到 {status_path}")
        return payload
    except Exception as e:
        print(f"[错误] 写入状态文件失败: {e}")
        return None



#&&% 恢复记录状态

def cad_zt_xin_2(status_file=None):
    """
    【V2.1 恢复版】根据 cad_zt_xin_1 记录的状态恢复 CAD 环境。
    逻辑：重启 -> 打开背景文件 -> 打开目标文件(自动激活) -> 强制确认激活
    """
    import json
    import time
    import os
    from pathlib import Path

    # 1. 导入架构组件
    from system.project_setup import PathConfig
    from system.licad import C
    from scripts.CAD_basic import (
        close_all_cad_processes, 
        start_applicationV9, 
         
        
        
    )
    from system.CAD_coordination import wait_quiescent

    # 2. 处理默认路径
    if status_file is None:
        status_file = PathConfig.LOGS / "cad_status.json"
    
    status_path = Path(status_file)
    if not status_path.exists():
        print(f"[cad_zt_xin_2] ❌ 状态文件不存在: {status_path}")
        return False

    # 3. 读取并解析配置
    try:
        payload = json.loads(status_path.read_text(encoding="utf-8"))
        print(f"[cad_zt_xin_2] 成功读取状态记录 (时间: {payload.get('timestamp')})")
    except Exception as e:
        print(f"[cad_zt_xin_2] ❌ 解析 JSON 失败: {e}")
        return False

    raw_open_files = payload.get("open_files") or []
    target_active_file = payload.get("active_file") # 全路径

    # 4. 路径清洗与分类 (关键步骤)
    # 我们需要把“目标激活文件”从列表里剔除，留到最后单独打开
    background_files = []
    target_active_norm = None

    if target_active_file:
        try:
            target_active_norm = str(Path(target_active_file).resolve()).lower()
        except: pass

    seen = set()
    
    for f in raw_open_files:
        if not f: continue
        try:
            p_obj = Path(f)
            if not p_obj.exists():
                print(f"[跳过] 文件不存在: {f}")
                continue
            
            # 归一化：转为绝对路径字符串并小写，用于去重和比对
            norm_str = str(p_obj.resolve()).lower()
            
            # 如果是目标激活文件，先跳过，不放入背景列表
            if target_active_norm and norm_str == target_active_norm:
                continue
                
            if norm_str not in seen:
                seen.add(norm_str)
                # 存储原始路径或解析后的路径均可，这里存解析后的
                background_files.append(str(p_obj.resolve()))
                
        except Exception:
            continue

    # 5. 重置环境 (Kill & Start)
    print("[cad_zt_xin_2] 正在重置 CAD 环境...")
    close_all_cad_processes() # 使用标准清理函数
    
    # 双重保险清理
    time.sleep(1)
    
    start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
    
    # 等待启动稳定 (这里可以复用 cad_zt_oneb 的检测逻辑，或者简单等待)
    print("[cad_zt_xin_2] 等待 CAD 启动就绪...")
    wait_quiescent(min_quiet=2.0, timeout=30.0)
    
    # 6. 执行打开 (The Rhythm Strategy)
    reopened_count = 0
    
    # 6.1 先打开所有背景文件
    for f_path in background_files:
        try:
            print(f"[恢复] 打开背景文件: {Path(f_path).name}")
            open_file(f_path)
            reopened_count += 1
            # 💤 节奏控制：防止 COM 忙碌
            time.sleep(1.5) 
        except Exception as e:
            print(f"[警告] 打开失败 {f_path}: {e}")

    # 6.2 最后打开目标激活文件 (这样它自然就是激活状态)
    if target_active_file and Path(target_active_file).exists():
        try:
            print(f"[恢复] 打开并激活目标文件: {Path(target_active_file).name}")
            open_file(target_active_file)
            reopened_count += 1
            time.sleep(1.5)
        except Exception as e:
            print(f"[严重] 无法打开目标文件: {e}")
    
    # 7. 最终状态确认
    # 虽然最后打开的通常是激活的，但为了稳健，我们再次检查
    if target_active_file:
        target_name = Path(target_active_file).name
        try:
            # 刷新连接
            C.li()
            current_doc = getattr(C.doc, "Name", "")
            
            if current_doc.lower() != target_name.lower():
                print(f"[校准] 当前激活的是 {current_doc}，正在强制切换回 {target_name}...")
                doc_obj = get_doc_by_name(target_name)
                if doc_obj:
                    set_active_doc(doc_obj)
            else:
                print(f"[确认] 当前已正确激活: {target_name}")
                
        except Exception as e:
            print(f"[警告] 激活状态校验失败: {e}")

    print(f"[cad_zt_xin_2] 恢复完成。共打开 {reopened_count} 个文件。")
    return True



#&&&% 单文档操作

@retry_if_busy(max_retries=5, delay=1.0)
#&&% 新建dwg文件

def new_file(output_path=None, close_after=False):
    """Create a DWG file after verifying the current CAD/TArch context.

    Args:
        output_path (str | None): Target path; None keeps an unsaved blank file.
        close_after (bool): Close the newly created/opened file automatically when True.

    Returns:
        bool: True if the DWG was created or opened successfully.

    新建同名文件将会覆盖之前的文件
    output_path=None，则没有创建文件
    新建文件不关闭的话，最多同时打开的文件不会超过4个，最后一个是激活文件

    """

    C.li()

    def _close_new_file(result: bool) -> bool:
        """Close the active file when requested and ignore close errors."""
        if result and close_after:
            try:
                print("[信息] close_after=True，正在关闭新建的文件...")
                # 调用只关闭当前文档的函数，而不是重启整个CAD
                close_current_dwg_paradigm("no_save")
                print("[成功] 新建的文件已关闭。")
            except Exception as exc:
                print(f"[警告] 关闭新建文件失败: {exc}")
        return result

    if output_path:
        target = Path(output_path)
        
        # --- 新增逻辑：检查文件是否已在CAD中打开 ---
        try:
            open_paths = get_all_open_dwg_paths()
            normalized_open_paths = {str(Path(p).resolve()).lower() for p in open_paths}
            target_path_str = str(target.resolve()).lower()

            if target_path_str in normalized_open_paths:
                print(f"[信息] 目标文件 '{target.name}' 已在CAD中打开，将直接激活它。")
                activate_document_by_name(target.name)
                # 因为文件已存在并激活，所以不执行关闭逻辑，直接返回成功
                return True
        except Exception as e:
            print(f"[警告] 检查已打开文件时出错: {e}")
        # --- 新增逻辑结束 ---

        if target.exists():
            try:
                target.unlink()
                print(f"[信息] 已删除同名文件: {target}")
            except Exception as exc:
                print(f"[错误] 无法删除已存在文件 {target}: {exc}")
                return False

    def _limit_open_documents():
        """When open DWG count > 2, close extras leaving one."""
        try:
            names = get_open_document_names()
        except Exception as exc:
            print(f"[警告] 获取已打开文件失败: {exc}")
            return False, None

        if len(names) <= 3:
            return True, len(names)

        try:
            _, active_doc = get_acad_doc()
            active_name = active_doc.Name if active_doc else None
        except Exception:
            active_name = None

        keep = active_name if active_name in names else names[-1]
        remaining = names.copy()
        print(f"[信息] 当前打开 {len(names)} 个文件，保留 {keep}，关闭部分文件以压缩到 3 个以内")
        ok = True
        for name in names:
            if len(remaining) <= 3:
                break
            if name == keep:
                continue
            try:
                close_dwg_by_name(name)
                remaining.remove(name)
            except Exception as exc:
                ok = False
                print(f"[警告] 关闭文件 {name} 失败: {exc}")

        time.sleep(0.5)
        try:
            remaining = get_open_document_names()
        except Exception:
            remaining = []

        if len(remaining) <= 3:
            print(f"[信息] 已将打开文件数压缩到 {len(remaining)} 个")
            return ok, len(remaining)

        print(f"[警告] 仍有 {len(remaining)} 个文件未关闭")
        return False, len(remaining)

    shu_1 = jingchengshu_wenjian()
    tarch_ready = False

    if shu_1 == 1:
        print("[信息] 检测到 1 个 CAD 进程，进行天正墙自检...")
        wall_obj = None
        try:
            connected = C.li()
            if connected:
                try:
                    prev_obj = last_obj()
                    prev_handle = getattr(prev_obj, "Handle", None)
                except Exception:
                    prev_obj = None
                    prev_handle = None

                wall_created = draw_tarch_wall((0, 0, 0), (100, 0, 0), thickness=240)
                if wall_created:
                    try:
                        wall_obj = last_obj()
                        handle = getattr(wall_obj, "Handle", None)
                    except Exception:
                        wall_obj = None
                        handle = None

                    if handle and handle != prev_handle:
                        print(f"[成功] 天正墙自检通过 (Handle={handle})")
                        tarch_ready = True
                    elif handle == prev_handle and handle is not None:
                        print("[警告] last_obj 结果与自检前一致，可能未生成天正墙")
                    else:
                        print("[警告] 天正墙未返回 Handle，准备重新初始化 CAD")
                else:
                    print("[警告] 绘制天正墙失败，准备重新初始化 CAD")
            else:
                print("[警告] li() 连接失败，准备重新初始化 CAD")
        except Exception as exc:
            print(f"[警告] 天正墙自检异常: {exc}")
        finally:
            if wall_obj is not None:
                try:
                    safe_delete(wall_obj)
                except Exception:
                    try:
                        wall_obj.Delete()
                    except Exception:
                        pass

    if not tarch_ready:
        print("[信息] 执行 cad_zt_zero() + cad_zt_oneb() 重新准备天正环境...")
        cad_zt_zero()
        cad_zt_oneb()

    doc_ok, doc_count = _limit_open_documents()
    if doc_count and doc_count > 2 and not doc_ok:
        print("[信息] 关闭多余文件失败，重启 CAD 环境...")
        cad_zt_zero()
        cad_zt_oneb()

    result = new_dwg_enhanced(output_path)
    return _close_new_file(result)



#&&% 打开dwg文件

@retry_if_busy(max_retries=5, delay=1.0)
def open_file(file_path):
    """
    【函数编号】: SYS-IO-001
    【所属模块】: 系统与文件控制 (System & File Control)
    【功能描述】:
        建立 CAD 运行环境并安全打开指定的 DWG 文件。
        采用“单例进程+负载控制”策略：
        1. 进程守护：确保 Windows 环境中仅存在一个 CAD 进程，防止多开冲突。
        2. 环境自启：若未检测到 CAD/天正进程，自动调用 TArch 启动接口。
        3. 负载均衡：智能监控当前打开的文档数量。若超过安全阈值（通常为 3 个），
           会自动识别并关闭非活跃文档（保留当前活动文档），防止内存溢出。
        4. 幂等打开：若目标文件已处于打开状态，直接激活窗口而不重复加载。

    【参数详解】:
        - file_path (str):
            目标 DWG 文件的路径。
            支持绝对路径或相对路径，函数内部会基于 pathlib 进行标准化解析。

    【返回值】:
        - bool:
            - True: 操作成功（文件被成功打开，或已存在并被激活）。
            - False: 操作失败（环境重置失败、文件无法读取或进程异常）。

    【前置依赖】:
        - 依赖全局变量 global acad 进行 COM 对象传递。
        - 依赖全局工具函数: li(), litz(), start_applicationV9() 等。

    【示例】:
        >>> status = open_file(r"D:\Project\FloorPlan_V1.dwg")
        >>> print(status)
        True
    """


    # --------------------------------------------------------
    # 2. 初始连接检查
    # --------------------------------------------------------
    li_ok = False
    try:
        li_ok = C.li()
    except Exception:
        li_ok = False

    if not li_ok:
        litz()
    else:
        print("[open_file] 复用现有 CAD 连接。")

    # --------------------------------------------------------
    # 3. 定义内部辅助函数 (使用全局导入的工具函数)
    # --------------------------------------------------------
    def _get_acad():
        return win32com.client.GetActiveObject("AutoCAD.Application")

    def _ensure_single_process():
        # 使用全局导入的 jingchengshu_wenjian
        if jingchengshu_wenjian() > 1:
            print("[警告] 检测到多个 CAD 进程，执行重置...")
            # 替换原有的 cad_zt_zero/oneb 为标准函数，防止报错
            close_all_cad_processes() 
            litz()

    def _ensure_active_only():
        try:
            # 使用全局导入的 get_open_document_names
            names = get_open_document_names()
        except Exception as exc:
            print(f"[警告] 获取已打开文件失败: {exc}")
            return True

        if len(names) <= 3:
            return True

        try:
            # 使用全局导入的 get_acad_doc
            _, active_doc = get_acad_doc()
            active_name = active_doc.Name if active_doc else None
        except Exception:
            active_name = None

        keep = active_name if active_name in names else names[-1]
        remaining = names.copy()
        print(f"[信息] 当前打开 {len(names)} 个文件，保留 {keep}，关闭部分文件以压缩到 3 个以内")
        
        for name in names:
            if len(remaining) <= 3:
                break
            if name == keep:
                continue
            # 使用全局导入的 close_dwg_by_name
            close_dwg_by_name(name)
            remaining.remove(name)

        time.sleep(0.5)
        try:
            remaining = get_open_document_names()
        except Exception:
            remaining = []
            
        if len(remaining) > 3:
            print("[警告] 仍有多余文件未关闭，重置 CAD 环境")
            return False

        return True

    # --------------------------------------------------------
    # 4. 执行逻辑
    # --------------------------------------------------------
    _ensure_single_process()

    # 确保CAD已启动
    try:
        acad = _get_acad()
    except:
        print("[信息] CAD未启动，正在启动天正...")
        # 使用全局导入的 start_applicationV9
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        acad = _get_acad()

    # ==================== 👇 修改位置在这里 👇 ====================
    # 目的：在打开/激活新文件前，先腾出内存位置
    try:
        target_name = Path(file_path).name
        ensure_max_open_documents(keep_filename=target_name, max_count=3)
    except Exception as e:
        print(f"[警告] 启动前清理环境失败: {e}")
    # ==================== 👆 修改位置结束 👆 ====================

    # 规范化路径 (Path 已在头部导入)
    target_path = str(Path(file_path).resolve()).lower()

    # 检查是否已经打开
    try:
        # 这里的 acad 是通过 _get_acad 获取的 COM 对象
        for doc in acad.Documents:
            try:
                if str(Path(doc.FullName).resolve()).lower() == target_path:
                    print(f"[信息] 文件已打开: {file_path}")
                    try:
                        doc.Activate()
                    except:
                        pass
                    return True
            except:
                continue
    except Exception as e:
        print(f"[警告] 检查已打开文档时出错: {e}")

    # 使用全局导入的 open_dwg_paradigm
    return open_dwg_paradigm(file_path)

#&&% 复制并递增命名
@retry_if_busy(max_retries=5, delay=1.0)
def copy_file_with_increment(filepath):
    """
    复制文件并自动递增命名
    
    Args:
        filepath: 源文件路径
        
    Returns:
        str: 新文件路径，失败返回None
        
    示例:
        copy_file_with_increment('D:/test.dwg')
        # 如果test-1.dwg不存在，创建test-1.dwg
        # 如果test-1.dwg存在，创建test-2.dwg
        # 以此类推
    """
    from pathlib import Path
    import shutil
    
    try:
        source = Path(filepath)
        if not source.exists():
            print(f"[错误] 源文件不存在: {filepath}")
            return None
            
        # 分离文件名和扩展名
        stem = source.stem  # 不带扩展名的文件名
        suffix = source.suffix  # 扩展名（包含.）
        parent = source.parent  # 父目录
        
        # 查找可用的递增编号
        counter = 1
        while True:
            new_name = f"{stem}-{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                break
            counter += 1
            
        # 复制文件
        shutil.copy2(str(source), str(new_path))
        print(f"[成功] 已复制文件: {new_path}")
        return str(new_path)
        
    except Exception as e:
        print(f"[错误] 复制文件失败: {e}")
        return None

# ============================================================================
# 文件保存
# ============================================================================

#&&% 保存文件
@retry_if_busy(max_retries=5, delay=1.0)
def save_file():
    """
    保存当前文件

    Returns:
        bool: 成功返回True
    """
    return save_current_dwg_paradigm()

#&&% 另存为
@retry_if_busy(max_retries=5, delay=1.0)
def save_file_as(output_path):
    """
    另存为

    Args:
        output_path: 保存路径

    Returns:
        bool: 成功返回True
    """
    return save_as_dwg_paradigm(output_path)

# ============================================================================
# 文件关闭
# ============================================================================

#&&% 关闭文件
@retry_if_busy(max_retries=5, delay=1.0)
def close_file(save_option="auto_save"):
    """
    关闭当前文件

    Args:
        save_option: "auto_save"(默认，先保存再关闭), "no_save"(不保存), 其他值走原始策略

    Returns:
        bool: 成功返回True
    """


    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        
        doc=acad.ActiveDocument
        mp = doc.ModelSpace
        sp = doc.PaperSpace
        

    except NameError:
        # 如果没有 活动 对象，尝试直接连接
        acad = win32com.client.Dispatch("AutoCAD.Application")

        doc=acad.ActiveDocument
        mp = doc.ModelSpace
        sp = doc.PaperSpace


    try:
        if save_option == "auto_save":
            save_current_dwg_paradigm()
            return close_current_dwg_paradigm("no_save")
        elif save_option == "no_save":
            from CAD_basic import get_all_open_dwg_paths
            try:
                open_paths = get_all_open_dwg_paths()
            except Exception:
                open_paths = []
            cad_zt_oneb()
            for file_path in open_paths:
                try:
                    if file_path and Path(file_path).exists():
                        open_file(file_path)
                except Exception as exc:
                    print(f"[警告] 重新打开 {file_path} 失败: {exc}")
            return True
        else:
            return close_current_dwg_paradigm(save_option)
    except Exception as exc:
        print(f"[错误] 关闭文件失败: {exc}")
        return False


#&&% 清理文件垃圾
@retry_if_busy(max_retries=3, delay=1.0)
def purge_file(deep_purge=True):
    """
    清理当前文档中的未引用对象（块、图层、线型等）。
    
    Args:
        deep_purge (bool): True则执行多次清理以确保彻底（对应PU命令的递归清理）
    """
    try:
        doc = C.doc
        # 方法1: 使用COM对象的 PurgeAll (较温和)
        doc.PurgeAll()
        
        # 方法2: 如果需要深度清理（尤其是注册应用程序），建议发送命令
        # 注意：-PURGE 命令在不同CAD版本参数略有不同，'A'代表All
        if deep_purge:
            # 这是一个强力清理序列：清理所有、不确认
            cmd = "-PURGE\nA\n\nN\n" 
            doc.SendCommand(cmd)
            # 某些顽固垃圾可能需要两遍
            doc.PurgeAll()
            
        print("[成功] 文件清理完成")
        return True
    except Exception as e:
        print(f"[警告] 清理文件失败: {e}")
        return False

#&&% 检查文件是否被锁定
def check_file_locked(filepath):
    """
    通过检查 .dwl 和 .dwl2 隐藏文件来判断 DWG 是否被占用。
    这是最轻量级的检查，不需要启动 CAD。
    
    Returns:
        bool: True 表示文件被锁定（正在使用），False 表示空闲
        str: 如果被锁定，返回占用者的信息（如果有），否则返回空串
    """
    path_obj = Path(filepath)
    if not path_obj.exists():
        return False, "文件不存在"

    # 构建锁文件路径
    dwl_path = path_obj.with_suffix('.dwl')
    dwl2_path = path_obj.with_suffix('.dwl2')

    is_locked = False
    who_locked = ""

    if dwl_path.exists() or dwl2_path.exists():
        is_locked = True
        # 尝试读取 .dwl 文件获取用户名 (如果是文本格式)
        try:
            if dwl_path.exists():
                with open(dwl_path, 'r', encoding='gbk', errors='ignore') as f:
                    who_locked = f.read().strip()
        except:
            who_locked = "未知用户"
            
    return is_locked, who_locked


#&&% 检查当前文档是否只读
def is_read_only():
    """
    检查当前激活文档是否为只读状态
    """
    try:
        doc = C.doc
        # ReadOnly 是 Document 对象的一个属性
        return doc.ReadOnly
    except Exception:
        return False



#&&&% 跨文件操作

#&&% 插入并炸开
@retry_if_busy(max_retries=5, delay=1.0)
def insert_file_exploded(source_file, target_doc=None, x=0, y=0, z=0, scale=1.0, target_layout=None):
    """
    【功能】: 自适应偏移修复版插入函数20260108。
    【逻辑】: 
       1. 不修改源文件，不打开源文件。
       2. 直接读取当前文档的 INSBASE 作为偏移量。
       3. 插入并炸开后，利用 Explode 的返回值直接获取新对象。
       4. 将这些对象反向移动进行纠偏。
    """
    # 1. 智能获取文档
    if target_doc is None:
        target_doc = C.doc

    # 2. 路径标准化
    try:
        real_path = str(Path(source_file).resolve())
        block_name = Path(real_path).stem
    except:
        print(f"❌ 路径错误: {source_file}")
        return False

    if not os.path.exists(real_path):
        return False

    # 3. 获取纠偏向量 (直接读取当前环境的 INSBASE)
    move_vec = (0.0, 0.0, 0.0)
    try:
        # GetVariable 返回的是 tuple (x, y, z)
        base_pt = target_doc.GetVariable("INSBASE")
        
        # 如果 INSBASE 不为 0，说明插入的对象会被 CAD 自动偏移，我们需要把它移回来
        # 逻辑：如果基点是 (X,Y)，插入后图形会偏到 (-X,-Y)，所以我们要移 (+X,+Y)
        if abs(base_pt[0]) > 1e-6 or abs(base_pt[1]) > 1e-6:
            move_vec = base_pt
            print(f"🔍 [纠偏] 检测到环境 INSBASE={base_pt}，将对插入对象执行自动归位。")
    except:
        pass

    # 4. 临时关闭单位缩放 (防止尺寸乱变)
    old_units = 0
    try:
        old_units = target_doc.GetVariable("INSUNITS")
        target_doc.SetVariable("INSUNITS", 0) 
    except: pass

    try:
        # 5. 确定插入空间
        if target_layout:
            try: dest_space = target_doc.Layouts.Item(target_layout).Block
            except: dest_space = target_doc.ModelSpace
        else:
            dest_space = target_doc.ModelSpace

        # 6. 清理旧定义 (防止定义冲突)
        try: target_doc.Blocks.Item(block_name).Delete()
        except: pass

        # 7. 插入块
        pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (float(x), float(y), float(z)))
        print(f"  -> [底层] 正在插入: {block_name}")
        block_ref = dest_space.InsertBlock(pt, real_path, scale, scale, scale, 0.0)

        # 8. 炸开并捕获新对象 (核心优化)
        print(f"  -> [底层] 正在炸开...")
        # Explode() 返回一个 Variant 数组，里面直接包含了炸开后的所有新对象！
        # 这比“记录句柄往前推”更直接、更稳定。
        ##exploded_objects = block_ref.Explode()


        exploded_objects = cb.safe_explode(block_ref)






        # 9. 删除块引用
        block_ref.Delete()

        # 10. 执行纠偏移动 (如果需要)
        if move_vec != (0.0, 0.0, 0.0):
            print(f"  -> [纠偏] 正在移动 {len(exploded_objects)} 个实体归位...")
            
            # 构造起点(0,0,0) 和 终点(move_vec)
            p1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (0.0, 0.0, 0.0))
            p2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, move_vec)
            
            for obj in exploded_objects:
                try:
                    obj.Move(p1, p2)
                except Exception as ex:
                    # 某些特殊对象可能不支持 Move，跳过
                    pass

        # 11. 再次清理块定义
        try: target_doc.Blocks.Item(block_name).Delete()
        except: pass 

        return True

    except Exception as e:
        print(f"❌ [insert_file_exploded] 失败: {e}")
        return False
        
    finally:
        # 恢复单位
        try: target_doc.SetVariable("INSUNITS", old_units)
        except: pass




#&&% 拷贝文件内容_20260118
@retry_if_busy(max_retries=5, delay=1.0)
def copy_file_content_pywin32(
    source_file, 
    target_file, 
    target_x=0, target_y=0, 
    scale=1.0, 
    rotation=0.0,
    target_layout=None,
    explode=True
):
    """
    【函数编号】: IO-Full-Transfer-V2.0 (全图插入版)
    【功能】: 将 source_file 的全部模型空间内容，作为一个整体插入到 target_file 的指定坐标。
    【原理】: 
        1. 副本机制: 创建源文件的临时副本 (避开文件占用/锁死问题)。
        2. InsertBlock: 利用 CAD 原生插入能力，将副本作为块插入。
        3. 坐标逻辑: 源文件的原点(0,0) 将被放置在 (target_x, target_y)。
        4. 深度清理: 炸开后彻底删除块定义，不留垃圾。

    【参数】:
        source_file: 源文件路径
        target_file: 目标文件路径 (如果已打开则激活，未打开则打开)
        target_x, target_y: 插入点 (对应源文件的 0,0 点)
        scale: 缩放比例
        rotation: 旋转角度 (度)
        target_layout: 插入到哪个布局 (None=模型空间)
        explode: 插入后是否炸开 (True=炸开成实体, False=保留为块)
    
    【返回值】: bool 成功/失败
    """
    from CAD_file_operations import open_file, save_file
    import win32com.client
    import pythoncom
    import os
    import time
    import tempfile
    import shutil
    from pathlib import Path

    print(f"🚀 [Full-Transfer-V2] 启动全图合并...")
    
    # 1. 路径检查
    src_path = Path(source_file)
    if not src_path.exists():
        print(f"❌ 源文件不存在: {source_file}")
        return False

    # 2. 创建临时副本 (关键步骤：防止源文件被占用导致 Insert 失败)
    # 我们不直接 Insert 源文件，而是 Insert 它的副本
    temp_dir = Path(tempfile.gettempdir())
    temp_copy_path = temp_dir / f"full_insert_{int(time.time())}.dwg"
    
    try:
        shutil.copy2(src_path, temp_copy_path)
        print(f"  📄 创建临时副本: {temp_copy_path.name}")
    except Exception as e:
        print(f"❌ 创建副本失败: {e}")
        return False

    # ==========================================
    # 阶段: 插入操作
    # ==========================================
    try:
        # 1. 打开/激活目标文件
        print(f"  📂 准备目标: {Path(target_file).name}")
        if not open_file(target_file): 
            return False
        
        doc_tgt = C.doc  # 获取当前激活文档
        
        # 2. 切换空间 (模型 vs 布局)
        if target_layout:
            try: 
                doc_tgt.ActiveLayout = doc_tgt.Layouts.Item(target_layout)
                dest_space = doc_tgt.ActiveLayout.Block
            except: 
                print(f"  ⚠️ 布局 {target_layout} 不存在，转为模型。")
                dest_space = doc_tgt.ModelSpace
        else:
            doc_tgt.SetVariable("TILEMODE", 1) # 切换到模型
            dest_space = doc_tgt.ModelSpace

        # 3. 准备插入参数
        # 注意：源文件的 (0,0) 会对齐到这里的 (target_x, target_y)
        pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (float(target_x), float(target_y), 0.0))
        
        # 4. 清理潜在的同名块定义 (防止旧定义导致插入内容不更新)
        block_name = temp_copy_path.stem
        try: 
            doc_tgt.Blocks.Item(block_name).Delete()
            print("  🧹 清理了旧的同名块定义")
        except: pass
        
        # 5. 执行插入 (InsertBlock)
        print(f"  🔄 正在插入全图... (Pos: {target_x}, {target_y})")
        # 参数: 插入点, 文件路径, X比例, Y比例, Z比例, 旋转
        block_ref = dest_space.InsertBlock(pt, str(temp_copy_path), scale, scale, scale, rotation)
        
        # 6. 强制冷却 (防 RPC 忙碌)
        time.sleep(1.0)
        
        if not explode:
            print("  ✨ 插入完成 (保留为块引用)")
            doc_tgt.Save()
            return True

        # 7. 炸开逻辑 (Retry Loop)
        print("  💥 正在炸开合并...")
        exploded = False
        for i in range(5):
            try:
                block_ref.Explode()
                exploded = True
                print(f"     ✅ 成功 (Attempt {i+1})")
                break
            except Exception as e:
                if "rejected" in str(e) or "busy" in str(e):
                    print(f"     ⏳ CAD忙碌，重试炸开 ({i+1}/5)...")
                    time.sleep(0.5 + i * 0.5)
                else:
                    # 某些特殊块无法炸开 (如非统一比例)，虽然这里我们设的都是 scale
                    print(f"     ⚠️ 炸开遇到非忙碌错误: {e}")
                    time.sleep(1.0)
        
        # 8. 收尾清理
        if exploded:
            # 删除块引用本身 (Explode 会生成新对象，原块引用还在)
            try: block_ref.Delete()
            except: pass
            
            # 删除块定义 (彻底清除数据依赖，减小文件体积)
            try: doc_tgt.Blocks.Item(block_name).Delete()
            except: pass
            
            # 删除磁盘上的临时文件
            try: temp_copy_path.unlink()
            except: pass
            
            doc_tgt.Save()
            print("  ✨ 全图合并完成")
            return True
        else:
            print("  ⚠️ 炸开失败，保留原块。")
            doc_tgt.Save()
            try: temp_copy_path.unlink()
            except: pass
            return True

    except Exception as e:
        print(f"❌ 全图插入失败: {e}")
        # 失败也要尝试清理临时文件
        try: temp_copy_path.unlink()
        except: pass
        return False




#&&% 跨文件插入区域_20260116

@retry_if_busy(max_retries=5, delay=1.0)
def insert_region_v2(
    src_dwg, 
    target_dwg, 
    x1, y1, x2, y2, 
    target_x, target_y,
    target_layout=None
):
    """
    【函数编号】: IO-Region-Transfer-V2.0 (WBlock 极速版)
    【功能】: 将 src_dwg 指定区域的内容，精确插入到 target_dwg 的指定位置。
    【原理】: 
        1. WBlock提取: 仅提取选区内容到临时文件 (极快)。
        2. 数学偏移: 计算 (Target - Source) 向量，直接插入到偏移点。
        3. 抗扰炸开: 内置 COM 忙碌重试机制。


    如果target_dwg是当前激活文件，src_dwg没有打开，则src_dwg会被插入，插入后保存，target_dwg不会关闭，src_dwg关闭。

    如果target_dwg是打开文件，src_dwg也打开甚至激活，则src_dwg会被插入，插入后保存，target_dwg不会关闭，src_dwg关闭。

    如果target_dwg，src_dwg都未打开，则src_dwg会被插入，插入后保存，target_dwg不会关闭，src_dwg关闭。

    如果src_dwg打开，则src_dwg会被插入，插入后保存，target_dwg不会关闭，src_dwg关闭。

    总之，操作后target_dwg不会关闭，src_dwg关闭，不论之前是什么状态，包括多文件状态可能包含源和目标文件。

    """
    from CAD_file_operations import open_file, save_file
    import win32com.client
    import pythoncom
    import os
    import time
    import tempfile
    from pathlib import Path

    print(f"🚀 [Region-V2] 启动跨文件传输...")
    
    # 坐标规范化
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    
    # 临时文件路径
    temp_wblock_path = Path(tempfile.gettempdir()) / f"wb_{int(time.time())}.dwg"
    if temp_wblock_path.exists():
        try: temp_wblock_path.unlink()
        except: pass

    # ==========================================
    # 阶段 1: WBlock 提取源数据 (只读操作)
    # ==========================================
    try:
        # 1. 打开源文件 (不做任何修改，安全)
        print(f"  📖 读取源: {Path(src_dwg).name}")
        if not open_file(src_dwg): return False
        
        doc_src = C.doc
        
        # 2. 创建选择集 (窗选区域)
        try: doc_src.SelectionSets.Item("TempExportSS").Delete()
        except: pass
        ss = doc_src.SelectionSets.Add("TempExportSS")
        
        p1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x_min, y_min, 0))
        p2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x_max, y_max, 0))
        
        # 模式 5 = acSelectionSetWindow (完全包含在框内的对象)
        # 模式 1 = acSelectionSetCrossing (碰到框的对象) -> 建议用 Crossing 防止漏选
        ss.Select(1, p1, p2) 
        
        if ss.Count == 0:
            print("  ⚠️ 选区为空，取消操作。")
            return False
            
        # 3. 执行 WBlock (写块到磁盘)
        # 注意: WBlock 导出的文件，保持原坐标系！这正是我们想要的。
        # 对象在 (100,100)，导出的文件里它还在 (100,100)。
        print(f"  💾 WBlock 导出 {ss.Count} 个对象...")
        doc_src.Wblock(str(temp_wblock_path), ss)
        
        # 4. 关闭源文件 (释放锁)
        # False = 不保存源文件，因为我们只是选了一下
        doc_src.Close(False) 
        time.sleep(0.5) # 冷却
        
    except Exception as e:
        print(f"❌ 导出阶段失败: {e}")
        return False

    # ==========================================
    # 阶段 2: 偏移插入 (写入操作)
    # ==========================================
    try:
        # 1. 打开目标文件
        print(f"  📂 打开目标: {Path(target_dwg).name}")
        if not open_file(target_dwg): return False
        
        doc_tgt = C.doc
        
        # 2. 切换空间
        if target_layout:
            try: 
                doc_tgt.ActiveLayout = doc_tgt.Layouts.Item(target_layout)
                dest_space = doc_tgt.ActiveLayout.Block
            except: 
                print(f"  ⚠️ 布局 {target_layout} 不存在，转为模型。")
                dest_space = doc_tgt.ModelSpace
        else:
            doc_tgt.SetVariable("TILEMODE", 1)
            dest_space = doc_tgt.ModelSpace

        # 3. 计算数学偏移量 (核心算法)
        # 源内容的基准点是 (x_min, y_min)。
        # 我们想让这个基准点，落在目标的 (target_x, target_y)。
        # 插入点 InsertPt = Target - Source
        ins_x = target_x - x_min
        ins_y = target_y - y_min
        
        print(f"  🧮 坐标映射: Src({x_min:.1f}) -> Tgt({target_x:.1f}) | Offset=({ins_x:.1f}, {ins_y:.1f})")
        
        # 4. 插入块
        pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (ins_x, ins_y, 0))
        
        # 清理同名块定义 (防止无法更新)
        block_name = temp_wblock_path.stem
        try: doc_tgt.Blocks.Item(block_name).Delete()
        except: pass
        
        print("  🔄 正在插入...")
        block_ref = dest_space.InsertBlock(pt, str(temp_wblock_path), 1.0, 1.0, 1.0, 0.0)
        
        # 5. 强制冷却 (防 Call Rejected)
        time.sleep(1.0)
        
        # 6. 抗干扰炸开 (Retry Loop)
        print("  💥 正在炸开...")
        exploded = False
        for i in range(5):
            try:
                block_ref.Explode()
                exploded = True
                print(f"     ✅ 成功 (Attempt {i+1})")
                break
            except Exception as e:
                if "rejected" in str(e) or "busy" in str(e):
                    time.sleep(0.5 + i * 0.5)
                else:
                    time.sleep(1.0)
        
        # 7. 收尾
        if exploded:
            try: block_ref.Delete()
            except: pass
            
            # 清理块定义
            try: doc_tgt.Blocks.Item(block_name).Delete()
            except: pass
            
            # 清理临时文件
            try: temp_wblock_path.unlink()
            except: pass
            
            doc_tgt.Save()
            print("  ✨ 传输完成")
            return True
        else:
            print("  ⚠️ 炸开失败，保留原块。")
            doc_tgt.Save()
            return True

    except Exception as e:
        print(f"❌ 插入阶段失败: {e}")
        import traceback; traceback.print_exc()
        return False

#&&&% 多文档控制

#&&% 设置激活文档
@retry_if_busy(max_retries=10, delay=0.5)
def set_active_doc(doc):
    """
    将指定文档 doc 设置为当前激活窗口。
    原理：激活后通常需要重新建立连接 (li) 才能操作新文档。
    """
    try:
        doc.Activate()
        time.sleep(0.3)  # [物理避让] 稍作延时，确保激活生效
        print("[OK] 当前激活文档：", doc.Name)
        return True
    except Exception as e:
        print("[错误] 激活文档失败：", e)
        return False

#&&% 按名称获取文档
@retry_if_busy(max_retries=10, delay=0.5)
def get_doc_by_name(name): 
    """
    通过文件名获取 AutoCAD 文档对象，例如 '空白.dwg'
    如果未找到，返回 None
    """
    # 每次调用都重新获取 app，防止对象失效
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    for doc in acad.Documents:
        if doc.Name.lower() == name.lower():
            return doc
    return None

#&&% 获取打开文档名
@retry_if_busy(max_retries=10, delay=0.5)
def get_open_document_names():
    """返回所有打开的文件名列表"""
    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        return [doc.Name for doc in acad.Documents]
    except Exception:
        # 如果获取失败，尝试通过 C 对象获取
        if C.app:
            return [doc.Name for doc in C.app.Documents]
        raise # 抛出异常让 retry 捕获

#&&% 安全关闭当前文件
def close_current_drawing_safely():
    """
    安全关闭当前 DWG 文件，确保确实关闭并重新连接。
    最多尝试 3 次。
    """
    
    try:
        Name1 = doc.Name
    except:
        print("[警告]️ 当前 doc 无法获取名称，可能未连接。")

        doc=C.doc

        Name1 = doc.Name
    
    for attempt in range(1, 4):  # 最多尝试3次
        sys_logger.info(f"🔄 第 {attempt} 次尝试关闭 '{Name1}'")
        close_dwg_by_name(Name1)

        doc=C.doc  # 重新连接 acad、doc、mp、sp 等
        try:
            Name2 = doc.Name
        except:
            Name2 = None

        if Name2 != Name1:
            sys_logger.info(f"🟢 已确认文件 '{Name1}' 关闭，当前打开文件为 '{Name2}'")
            doc=C.doc  # 再执行一次，确保变量正确
            return
        else:
            print("[警告]️ 文件仍未关闭，继续尝试...")

    sys_logger.info(f"[错误] 多次尝试仍未成功关闭 '{Name1}'，请手动检查。")



#&&% 关闭除当前激活文档外的所有 DWG 文件

def close_all_except_active_safe():
    """
    更稳定地关闭除当前激活文档外的所有 DWG 文件，避免 COM 对象断链。
    """
    try:
        active_name = acad.ActiveDocument.Name
        all_names = [acad.Documents.Item(i).Name for i in range(acad.Documents.Count)]
        closed = 0

        for name in all_names:
            if name != active_name:
                try:
                    doc = acad.Documents.Item(name)
                    doc.Close(False)  # 不保存直接关闭
                    sys_logger.info(f"[已关闭] {name}")
                    closed += 1
                except Exception as e:
                    sys_logger.info(f"[警告] 无法关闭 {name}: {e}")

        sys_logger.info(f"[OK] 成功关闭 {closed} 个文档，仅保留 {active_name}")

    except Exception as e:
        sys_logger.info(f"[错误] 安全关闭失败：{e}")



#&&% 按名称关闭DWG
@retry_if_busy(max_retries=5, delay=1.0)
def close_dwg_by_name(Name):
    """
    关闭当前桌面中名为 Name 的 DWG 文件。
    如果文件已打开，则关闭该文件。
    
    参数：
        Name: 要关闭的 DWG 文件的名称（如 "example.dwg"）不含路径的名
    """
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application")  # 获取 AutoCAD 应用
        doc = acad.Documents.Item(Name)  # 获取指定名称的文档
        
        if doc:
            doc.Close(False)  # 关闭文件，不提示保存
            print(f"[OK] 文件 '{Name}' 已关闭")
        else:
            print(f"[错误] 未找到名为 '{Name}' 的文件")
    except Exception as e:
        print(f"[错误] 关闭文件 '{Name}' 失败: {e}")







#&&% 关闭所有文件
@retry_if_busy(max_retries=5, delay=1.0)
def close_all_files(save_option="auto_save"):
    """
    关闭所有文件
   
    默认保存后再关闭就不会跳出要保存吗的弹窗

    Returns:
        bool: 成功返回True
    """
    if save_option == "no_save":
        try:
            from CAD_basic import get_all_open_dwg_paths
            open_paths = get_all_open_dwg_paths()
        except Exception:
            open_paths = []
        cad_zt_oneb()
        for file_path in open_paths:
            try:
                if file_path and Path(file_path).exists():
                    open_file(file_path)
            except Exception as exc:
                print(f"[警告] 重新打开 {file_path} 失败: {exc}")
        return True

    try:
        
        names = get_open_document_names()
    except Exception:
        return close_all_dwg_paradigm()

    if not names:
        return True

    for name in names:
        try:
            activate_document_by_name(name)
        except Exception:
            pass

        if save_option == "auto_save":
            try:
                save_current_dwg_paradigm()
            except Exception:
                pass
            close_current_dwg_paradigm("no_save")
        else:
            close_current_dwg_paradigm(save_option)
    return True

#&&% 安全限制打开文件数量
def ensure_max_open_documents(keep_filename, max_count=3):
    """
    【核心修复】安全地限制打开文件数量
    解决：遍历 Documents 集合时关闭文件导致的索引错误 & RPC 拒绝错误

    """
    
    try:
        
        acad = C.acad
        docs = acad.Documents
        current_count = docs.Count
        
        if current_count <= max_count:
            return

        print(f"[清理] 当前打开 {current_count} 个文件，尝试压缩至 {max_count} 个...")

        # 1. 先建立“黑名单” (只记录名字，不直接操作对象)
        #    我们要保留 keep_filename，其他的列入关闭计划
        #    同时尽量避开 ActiveDocument (如果是源文件)
        docs_to_close = []
        active_name = ""
        try: active_name = acad.ActiveDocument.Name
        except: pass

        for i in range(current_count):
            try:
                # 注意：COM 索引从 0 开始
                doc = docs.Item(i)
                d_name = doc.Name
                
                # 跳过要保留的文件
                if d_name.lower() == keep_filename.lower():
                    continue
                    
                # 暂时把 ActiveDocument 放到最后处理，或者跳过
                if d_name == active_name:
                    continue
                    
                docs_to_close.append(d_name)
            except: pass

        # 2. 按照名单逐个关闭
        closed_count = 0
        for name in docs_to_close:
            # 如果已经达标，就停手
            if docs.Count <= max_count: break
            
            try:
                # 通过名字重新获取对象并关闭
                target = docs.Item(name)
                # Close(False) 表示不保存直接关闭
                target.Close(False)
                print(f"  [OK] 已关闭冗余文件: {name}")
                closed_count += 1
            except Exception as e:
                print(f"  [跳过] 关闭 {name} 失败: {e}")

        # 3. 如果还是太多，最后尝试动一下 ActiveDocument (除了 keep_file)
        if docs.Count > max_count and active_name.lower() != keep_filename.lower():
             try:
                 acad.ActiveDocument.Close(False)
             except: pass

    except Exception as e:
        print(f"[警告] 文件清理过程异常: {e}")


#&&&% 空间操作

#&&%判定在什么空间
@retry_on_busy(max_retries=5, base_delay=0.2)
def get_obj_loc(obj):
    """
    判断对象所在的数据库空间。
    注意：这里去掉了宽泛的 try...except，让 COM 错误能传导给装饰器，
    从而触发 retry_on_busy 的重试机制。
    """
    doc = C.doc

    # 1. 这一步是高频报错点 (CAD忙时 ObjectIdToObject 会失败)
    # 让装饰器来处理这里的异常
    owner_btr = doc.ObjectIdToObject(obj.OwnerID)
    btr_name = owner_btr.Name
    
    if btr_name.upper() == "*MODEL_SPACE":
        return 1  # 模型空间
    elif btr_name.upper().startswith("*PAPER_SPACE"):
        return 0  # 图纸空间
    else:
        return -1 # 块定义内部或其他


#&&% 空间切换
@retry_on_busy(max_retries=5, base_delay=0.2)
def set_space_mode(mode_val):
    """
    【功能】: 强制切换当前空间
    【参数】: 1=模型, 0=布局
    """
    doc = C.doc 
    
    # SetVariable 是原子操作，非常适合重试
    # 如果 CAD 正忙（例如正在自动保存），这一步会报错，装饰器会捕获并重试
    doc.SetVariable("TILEMODE", mode_val)

    # 确保退出视口 (PSPACE)
    if mode_val == 0:
        # 这个属性设置偶尔也会因为 RPC 冲突失败，也需要重试
        doc.MSpace = False 
        
    return True




#&&% 布局切换


def switch_to_layout(layout_name, retry=10, delay=0.5):
    """
    【核心修复】切换布局 (增强版)
    功能：
      1. 检查是否已经在该布局，是则直接返回。
      2. 包含 RPC 忙碌自动重试机制 (解决 -2147418111 错误)。
      3. 包含 Command 强行切换兜底。

    @retry_on_busy不要加

    """
    doc = C.doc
    
    # 1. 快速检查：如果已经在目标布局，秒回
    try:
        if doc.ActiveLayout.Name == layout_name:
            return True
    except: pass

    # 2. 循环尝试切换
    sys_logger.info(f"🔄 正在切换至布局: {layout_name} ...")
    
    for i in range(retry):
        try:
            # 尝试 A: 标准 COM 切换
            lay = doc.Layouts.Item(layout_name)
            doc.ActiveLayout = lay
            
            # 刷新一下状态
            C.acad.ActiveDocument = doc 
            return True
            
        except Exception as e:
            # 捕获 "被呼叫方拒绝" (-2147418111) 或其他 COM 错误
            err_msg = str(e)
            
            # 如果是布局不存在，直接放弃，别重试了
            if "Item" in err_msg and "此时无法" in err_msg: # 具体的错误特征可能不同，但通常 COM 会报找不到
                sys_logger.info(f"❌ 布局不存在: {layout_name}")
                return False

            if i < retry - 1:
                # 只有在最后几次尝试时才打印 Log，避免刷屏
                if i > 2: 
                    sys_logger.info(f"   ⏳ CAD忙碌，等待重试 ({i+1}/{retry})...")
                time.sleep(delay)
                
                # 【强力手段】尝试 B: 发送命令 (异步绕过 COM 锁)
                # 在第 3 次和第 7 次失败时尝试
                if i in [3, 7]:
                    try: 
                        doc.SendCommand(f"LAYOUT S \"{layout_name}\"\n")
                        # 发送命令后稍微多睡会儿
                        time.sleep(1.0)
                        # 检查是否切换成功
                        if doc.ActiveLayout.Name == layout_name:
                            return True
                    except: pass
            else:
                sys_logger.info(f"❌ 切换布局失败 (已尝试{retry}次): {e}")
                return False
                
    return False


#&&% 获取所有布局名称
def get_layout_names(exclude_model=False):
    """
    获取当前文档所有布局的名称列表。
    """
    try:
        doc = C.doc
        layouts = []
        for layout in doc.Layouts:
            name = layout.Name
            if exclude_model and name == "Model":
                continue
            layouts.append(name)
        # 很多时候我们需要按Tab顺序排序，但在COM里Layouts集合默认不一定是排序的
        # 这里简单返回列表
        return layouts
    except Exception as e:
        print(f"[错误] 获取布局列表失败: {e}")
        return []




#&&&% 获取文件路径

#&&% 获取当前激活DWG路径 (修复版)
def get_current_dwg_path():
    """
    【函数编号】: SYS-001
    【功能描述】: 获取当前激活 DWG 文件的完整长路径。
    """
    try:
        doc = C.doc
        # 1. 尝试获取 FullName
        full_path = doc.FullName
        
        # 2. 校验是否为空
        if not full_path:
            name = doc.Name
            sys_logger.info(f"⚠️ 当前图纸 [{name}] 尚未保存到硬盘，无物理路径。")
            return None
            
        # 3. 关键修复：转换为长路径
        return get_long_path(full_path)

    except Exception as e:
        sys_logger.info(f"❌ 获取文件路径失败: {e}")
        return None


#&&% 获取所有打开DWG路径 (修复版)
@retry_if_busy(max_retries=10, delay=0.5)
def get_all_open_dwg_paths():
    """返回当前会话中所有已打开 DWG 的完整路径列表（强制转换为长路径）。"""
    paths = []
    
    # 确保 C.acad 连接正常
    try:
        acad = C.acad
        docs = acad.Documents
    except:
        return []

    for doc in docs:
        try:
            full_name = doc.FullName
            if full_name:
                # 关键修复：转换为长路径
                long_name = get_long_path(full_name)
                paths.append(long_name)
        except Exception:
            continue
            
    return paths


def get_long_path(path_str):
    """
    【核心修复】将 Windows 8.3 短路径 (如 D:\CLAUDE~1\...) 转换为完整长路径。
    同时处理大小写规范化。
    """
    if not path_str:
        return None
    
    # 去除可能存在的首尾引号 (修复你日志里的那个错误)
    clean_path = path_str.strip().strip("'").strip('"')
    
    try:
        # 1. 获取长路径 (核心)
        long_path = win32api.GetLongPathName(clean_path)
        # 2. 规范化分隔符 (把 / 变成 \)
        return os.path.normpath(long_path)
    except Exception:
        # 如果转换失败（比如文件还是内存临时态），返回原清洗后的路径
        return os.path.normpath(clean_path)





#&&&&%% （三）  天正基础操作

"""
20251204对天正基础操作进行了详细测试，恢复了显隐选择函数


"""



#&&% 逐点标注
def dim_by_points(p1, p2, p3):
    """
    使用天正逐点标注命令对任意两点进行标注

    Args:
        p1: 起点坐标 (x, y, z)
        p2: 终点坐标 (x, y, z)
        p3: 标注位置点 (x, y, z)

    Returns:
        bool: 成功返回True
    """
    C.li()


    from CAD_basic import dim_by_points as _dim_by_points
    return _dim_by_points(p1, p2, p3)


#&&% 绘制天正墙
def draw_tarch_wall(p1, p2, thickness=240):
    """
    绘制天正墙体

    Args:
        p1: 起点坐标 (x, y, z)
        p2: 终点坐标 (x, y, z)
        thickness: 墙厚，默认240

    Returns:
        bool: 成功返回True
    """
    C.li()
    import sys, time
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import last_obj, set_object_property
    from system.CAD_coordination import send_cmd_with_sync, wait_quiescent

    try:
        # 发送天正墙命令
        cmd = f"tgwall\n{p1[0]},{p1[1]}\n{p2[0]},{p2[1]}\n\n\n"
        send_cmd_with_sync(cmd, wait_after=1.0)
        wait_quiescent(min_quiet=0.5, timeout=10.0)

        # 获取刚绘制的墙，增加重试机制
        time.sleep(1.5)

        for attempt in range(3):
            try:
                wall = last_obj()
                obj_name = wall.ObjectName

                # 检查是否是墙体对象
                if 'Wall' in obj_name or 'TDb' in obj_name:
                    # 设置墙厚
    
                    set_object_property(wall, "Thickness", thickness/2)
                    set_object_property(wall, "Thickness2", thickness/2)
    
                    print(f"[成功] 已绘制墙体，厚度{thickness}")
                    return True
                else:
                    print(f"[警告] 对象类型不是墙体: {obj_name}")
                    if attempt < 2:
                        time.sleep(0.5)
                        continue
                    return False

            except Exception as e:
                print(f"[警告] 第{attempt+1}次获取墙体对象失败: {e}")
                if attempt < 2:
                    time.sleep(0.5)
                    continue
                raise

        print(f"[警告] 未找到墙体对象")
        return False

    except Exception as e:
        print(f"[错误] 绘制墙体失败: {e}")
        return False

#&&% 插入天正门
def insert_tarch_door(p, width=None, height=None):
    """
    在墙体上插入天正门

    Args:
        p: 插入点坐标 (x, y, z)
        width: 门宽（可选，不指定则使用默认值）
        height: 门高（可选，不指定则使用默认值）

    Returns:
        dict: {'success': bool, 'door': 门对象, 'width': 实际宽度, 'height': 实际高度}
    """
    import sys
    import time
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import  get_acad_doc, get_object_property, set_object_property
    from system.CAD_coordination import send_cmd_with_sync, wait_quiescent

    
    try:
        doc = C.doc
        ms = doc.ModelSpace
        count_before = ms.Count

        # 发送TOpening命令插入门
        cmd = f"TOpening\n{p[0]},{p[1]}\n\n\n"
        send_cmd_with_sync(cmd, wait_after=1.0)
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        door = None
        deadline = time.time() + 8.0
        while time.time() < deadline and door is None:
            time.sleep(0.5)
            count_after = ms.Count
            if count_after <= count_before:
                continue
            for idx in range(count_before, count_after):
                try:
                    obj = ms.Item(idx)
                    if getattr(obj, "ObjectName", "").lower() == "tdbopening":
                        door = obj
                        break
                except Exception:
                    continue
        if door is None:
            # 最后再全局搜索一次
            for idx in range(ms.Count - 1, -1, -1):
                try:
                    obj = ms.Item(idx)
                    if getattr(obj, "ObjectName", "").lower() == "tdbopening":
                        door = obj
                        break
                except Exception:
                    continue
        if door is None:
            from CAD_basic import last_obj
            for _ in range(3):
                try:
                    candidate = last_obj()
                    if getattr(candidate, "ObjectName", "").lower() == "tdbopening":
                        door = candidate
                        break
                except Exception:
                    pass
                time.sleep(0.4)

        if door is None:
            print("[错误] 未在模型空间中找到天正门对象")
            return {'success': False, 'door': None, 'width': None, 'height': None}

        # 读取当前尺寸
        current_width = get_object_property(door, 'Width')
        current_height = get_object_property(door, 'Height')

        # 设置尺寸（如果指定）
        if width is not None:
            set_object_property(door, 'Width', width)
            current_width = width

        if height is not None:
            set_object_property(door, 'Height', height)
            current_height = height

        print(f"[成功] 已插入天正门 - 宽度:{current_width}, 高度:{current_height}")

        return {
            'success': True,
            'door': door,
            'width': current_width,
            'height': current_height
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[错误] 插入门失败: {e}")
        return {'success': False, 'door': None, 'width': None, 'height': None}



#&&% 插入天正窗
def insert_tarch_window(p, width=600, height=1000, window_type="jz-pingchuang", delete_mc_yuan=False):
    """
    在墙体上插入天正窗

    Args:
        p: 插入点坐标 (x, y, z)
        width: 窗宽度，默认600
        height: 窗高度，默认1000
        window_type: 窗类型，默认"jz-pingchuang"，允许的类型:
            "jz-menlianchuang", "jz-dong", "jz-gaochuang", "jz-baiyechuang",
            "jz-tuchuang", "jz-pingchuang", "jz-zimumen", "jz-juanlianmen",
            "jz-tuilamen", "jz-shuangmen"
        delete_mc_yuan: 是否删除MC_yuan.dwg插入的对象，默认False不删除

    Returns:
        dict: {'success': bool, 'window': 窗对象, 'width': 宽度, 'height': 高度}
    """
    import time
    import logging
    from pathlib import Path as PathLib
    import sys
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import (
        get_object_property, set_object_property,
        transfer_props_by_matchprop
    )
    

    # 配置日志
    log_dir = LOGS_DIR
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"insert_tarch_window_{time.strftime('%Y%m%d_%H%M%S')}.log"

    # 配置日志处理器
    logger = logging.getLogger('insert_tarch_window')
    logger.setLevel(logging.INFO)
    # 清除已有的处理器
    if logger.handlers:
        logger.handlers.clear()
    # 添加文件处理器
    fh = logging.FileHandler(str(log_file), encoding='utf-8')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # 允许的窗类型列表
    allowed_types = [
        "jz-menlianchuang", "jz-dong", "jz-gaochuang", "jz-baiyechuang",
        "jz-tuchuang", "jz-pingchuang", "jz-zimumen", "jz-juanlianmen",
        "jz-tuilamen", "jz-shuangmen"
    ]
    C.li()
    # 1. 检查窗类型
    if window_type not in allowed_types:
        logger.error(f"窗类型错误: {window_type}, 允许的类型: {allowed_types}")
        print(f"[错误] 窗类型错误: {window_type}")
        return {'success': False, 'window': None, 'width': None, 'height': None}
    logger.info(f"窗类型检查通过: {window_type}")
    print(f"[信息] 窗类型检查通过: {window_type}")

    # 2. 连接当前激活文件
    C.li()
    logger.info("已连接当前激活文件")
    print("[信息] 已连接当前激活文件")

    # 3. 检查是否需要插入MC_yuan.dwg
    lb = stc('Mc_yuan_bj')
    if len(lb) == 0:
        logger.info("未找到Mc_yuan_bj图层，需要插入MC_yuan.dwg")
        print("[信息] 未找到Mc_yuan_bj图层，正在插入MC_yuan.dwg...")
        # 获取当前文件路径
        import win32com.client
        acad = cb.acad
        current_file = cb.doc.FullName
        logger.info(f"当前文件: {current_file}")
        copy_file_content_pywin32(str(XITONG_DIR / "MC_yuan.dwg"), current_file)
        logger.info("已插入MC_yuan.dwg")
        print("[成功] 已插入MC_yuan.dwg")
        # 重新连接
        C.li()
    else:
        logger.info(f"已存在Mc_yuan_bj图层，无需插入MC_yuan.dwg (找到{len(lb)}个对象)")
        print(f"[信息] 已存在Mc_yuan_bj图层 (找到{len(lb)}个对象)")

    # 4. 插入门
    print(f"[信息] 正在插入门... 位置:{p}, 宽度:{width}, 高度:{height}")
    result = insert_tarch_door(p, width=width, height=height)
    if not result['success']:
        logger.error("插入门失败")
        print("[错误] 插入门失败")
        return {'success': False, 'window': None, 'width': None, 'height': None}
    m1 = result['door']
    logger.info(f"已插入门，宽度:{width}, 高度:{height}")
    print(f"[成功] 已插入门，宽度:{width}, 高度:{height}")

    # 5. 选择窗类型图层的窗元并修改尺寸
    print(f"[信息] 正在选择窗类型图层: {window_type}")
    lc = stc(window_type)
    if len(lc) == 0:
        logger.error(f"未找到窗类型图层: {window_type}")
        print(f"[错误] 未找到窗类型图层: {window_type}")
        return {'success': False, 'window': None, 'width': None, 'height': None}

    window_src = lc[0]
    set_object_property(window_src, "Width", width)
    set_object_property(window_src, "Height", height)
    logger.info(f"已设置窗元尺寸: 宽{width}, 高{height}")
    print(f"[成功] 已设置窗元尺寸: 宽{width}, 高{height}")

    # 6. 使用transfer_props_by_matchprop匹配属性，最多5次
    print("[信息] 正在进行属性匹配...")
    success = False
    for attempt in range(1, 6):
        try:
            result_match = transfer_props_by_matchprop(window_src, m1, max_try=3, delay=0.4)
            if result_match:
                # 检查图层是否改变
                m1_layer = m1.Layer
                if m1_layer == window_type:
                    logger.info(f"第{attempt}次匹配成功，门已转换为窗，图层:{m1_layer}")
                    print(f"[成功] 第{attempt}次匹配成功，门已转换为窗，图层:{m1_layer}")
                    success = True
                    break
                else:
                    logger.warning(f"第{attempt}次匹配后图层不正确: {m1_layer}, 期望:{window_type}")
                    print(f"[警告] 第{attempt}次匹配后图层不正确: {m1_layer}, 期望:{window_type}")
        except Exception as e:
            logger.warning(f"第{attempt}次匹配失败: {e}")
            print(f"[警告] 第{attempt}次匹配失败: {e}")
        time.sleep(0.5)

    if not success:
        logger.error("transfer_props_by_matchprop匹配5次仍然失败")
        print("[错误] 属性匹配5次仍然失败")
        return {'success': False, 'window': None, 'width': None, 'height': None}

    # 7. 可选：删除MC_yuan对象
    if delete_mc_yuan:
        logger.info("正在删除MC_yuan对象...")
        print("[信息] 正在删除MC_yuan对象...")
        try:
            deleted_count = 0
            for obj in stc("MC_yuan_qiang"):
                try:
                    obj.Delete()
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"删除对象失败: {e}")
            for obj in stc("MC_yuan_bj"):
                try:
                    obj.Delete()
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"删除对象失败: {e}")
            logger.info(f"已删除 {deleted_count} 个MC_yuan对象")
            print(f"[成功] 已删除 {deleted_count} 个MC_yuan对象")
        except Exception as e:
            logger.warning(f"删除MC_yuan对象失败: {e}")
            print(f"[警告] 删除MC_yuan对象失败: {e}")

    logger.info(f"成功插入天正窗 - 位置:{p}, 宽度:{width}, 高度:{height}, 类型:{window_type}")
    print(f"[成功] 已插入天正窗 - 宽度:{width}, 高度:{height}, 类型:{window_type}")
    return {'success': True, 'window': m1, 'width': width, 'height': height}




#&&% 获取天正房间

def run_tupdspace_for_tz_room_in_rect(
    x1, y1, x2, y2,
    ty: float = 1.0,
    center_z: float = 0.0,
    insert_coord=None,
    require_tz_wall: bool = True,
):
    """
    在矩形 (x1,y1)-(x2,y2) 范围内：
      1. 调用 select_entities_in_window 让天正墙进入夹点编辑状态；
      2. 日志统计天正墙数量，并打印句柄等信息；
      3. 计算矩形中心 (仅日志用)；
      4. 计算 TUPDSPACE 插入点:
         - 若 insert_coord 为 None:
             水平方向取矩形中心，
             竖向在“矩形下边”外侧 4000，
             z = center_z
         - 若 insert_coord 为 (x,y,z)，则直接使用；
      5. 调用 run_auto_TUPDSPACE_with_coord(call_coord) 触发 TUPDSPACE。

    参数:
        x1, y1, x2, y2 : 矩形两个对角点世界坐标
        ty             : 传给 select_entities_in_window 的等待秒数
        center_z       : 用于默认插入点与矩形中心的 z 值
        insert_coord   : 可选，自定义插入点 (x,y,z)。
                         若为 None，则自动采用“下方 4000 + 水平居中”的默认点。
        require_tz_wall:
                         True  -> 若未检测到天正墙，则不调用 TUPDSPACE
                         False -> 不管有没有天正墙，都调用 TUPDSPACE

    返回:
        dict 示例：
        {
            "rect": ((x_lo, y_lo), (x_hi, y_hi)),
            "tz_wall_count": 13,
            "rect_center": (cx_center, cy_center, center_z),
            "call_coord": (cx, cy, cz),   # 真实传给 TUPDSPACE 的坐标
            "tupd_ok": True/False,
            "tupd_returncode": 0/其他
        }
        若因 require_tz_wall=True 且无天正墙而未调用 TUPDSPACE，则返回 None。
    """
    print("========== [TUPDSPACE_ROOM] run_tupdspace_for_tz_room_in_rect BEGIN ==========")
    print(f"[TUPDSPACE_ROOM] 输入矩形对角点: ({x1},{y1}) - ({x2},{y2})")
    C.li()

    # 1. 规范化矩形坐标
    (x_lo, y_lo), (x_hi, y_hi) = cb.normalize_rect(x1, y1, x2, y2)
    print(f"[TUPDSPACE_ROOM] 规范化矩形: 左下=({x_lo},{y_lo}), 右上=({x_hi},{y_hi})")

    # 2. 窗口选择 + 夹点编辑状态
    print("[TUPDSPACE_ROOM] 调用 select_entities_in_window 进行窗口选择 ...")
    try:
        com_list = cb.select_entities_in_window(x_lo, y_lo, x_hi, y_hi, ty=ty, select_mode="_W")
    except Exception as e:
        print("[TUPDSPACE_ROOM] ❌ 调用 select_entities_in_window 发生异常：", repr(e))
        print("========== [TUPDSPACE_ROOM] run_tupdspace_for_tz_room_in_rect END(ERROR_SELECT) ==========")
        return None

    print(f"[TUPDSPACE_ROOM] select_entities_in_window 返回实体数 = {len(com_list)}")

    # 3. 统计天正墙数量（ObjectName='TDbWall', Layer='WALL'），仅日志
    tz_walls = []
    for ent in com_list:
        try:
            oname = getattr(ent, "ObjectName", "")
            layer = getattr(ent, "Layer", "")
        except Exception:
            continue

        if oname == "TDbWall" and layer.upper() == "WALL":
            tz_walls.append(ent)

    print(f"[TUPDSPACE_ROOM] 其中天正墙 (ObjectName='TDbWall', Layer='WALL') 数量 = {len(tz_walls)}")

    handles = []
    for ent in tz_walls:
        try:
            h = ent.Handle
        except Exception:
            h = "<no_handle>"
        handles.append(h)
    print(f"[TUPDSPACE_ROOM] 天正墙句柄列表: {handles}")

    if require_tz_wall and not tz_walls:
        print("[TUPDSPACE_ROOM] ⚠ 未检测到天正墙，按 require_tz_wall=True 设定，不调用 TUPDSPACE。")
        print("========== [TUPDSPACE_ROOM] run_tupdspace_for_tz_room_in_rect END(NO_WALL) ==========")
        return None

    # 4. 计算矩形中心（仅用于日志参考）
    cx_center = (x_lo + x_hi) / 2.0
    cy_center = (y_lo + y_hi) / 2.0
    rect_center = (cx_center, cy_center, center_z)
    print(f"[TUPDSPACE_ROOM] 矩形中心(仅日志参考): {rect_center}")

    # 5. 决定真正传给 TUPDSPACE 的插入点 call_coord
    if insert_coord is None:
        # “下方 4000 + 水平居中”
        # 这里“最下边”按数值更小的 y_lo 理解；若你图上坐标系是反的，
        # 这一句可以改成用 y_hi + 4000。
        x_mid = cx_center
        bottom_y = y_lo           # 认为 y_lo 是“下边界”
        y_ins = bottom_y - 4000.0 # 再往下 4000
        z_ins = center_z
        call_coord = (x_mid, y_ins, z_ins)
        dy = y_ins - bottom_y
        print(f"[TUPDSPACE_ROOM] insert_coord 未提供，计算默认插入点: {call_coord}")
        print(f"[TUPDSPACE_ROOM] 默认插入点相对于最下边(y_lo={bottom_y})的偏移量 dy = {dy} (期望为 -4000.0)")
    else:
        if not (isinstance(insert_coord, (list, tuple)) and len(insert_coord) == 3):
            raise ValueError("insert_coord 必须是长度为 3 的 (x,y,z) 元组或列表")
        call_coord = tuple(insert_coord)
        print(f"[TUPDSPACE_ROOM] 使用调用方提供的 insert_coord 作为插入点: {call_coord}")

    # 6. 调用子程序，驱动 TUPDSPACE
    print("[TUPDSPACE_ROOM] 调用 run_auto_TUPDSPACE_with_coord() ...")
    tupd_result = run_auto_TUPDSPACE_with_coord(call_coord)
    print(
        f"[TUPDSPACE_ROOM] run_auto_TUPDSPACE_with_coord() 返回: "
        f"ok={tupd_result.get('ok')}, "
        f"returncode={tupd_result.get('returncode')}"
    )

    print("========== [TUPDSPACE_ROOM] run_tupdspace_for_tz_room_in_rect END ==========")

    return {
        "rect": ((x_lo, y_lo), (x_hi, y_hi)),
        "tz_wall_count": len(tz_walls),
        "rect_center": rect_center,
        "call_coord": call_coord,
        "tupd_ok": tupd_result.get("ok"),
        "tupd_returncode": tupd_result.get("returncode"),
    }
def run_auto_TUPDSPACE_with_coord(coord, script_path=None):
    """
    调用 auto_TUPDSPACE.py 子程序，传入坐标，并等待其执行完成（无黑框弹出）。
    增强版：详细打印子进程的 returncode / stdout / stderr，方便定位问题。

    参数:
        coord      : 三元组坐标 (x, y, z)
        script_path: auto_TUPDSPACE.py 的路径。
                     - 若为 None，则使用 "auto_TUPDSPACE.py"，即保持你原来相对路径行为，
                       让 Python 在当前工作目录下去找。

    返回:
        result: dict，例如
        {
            "ok": True/False,
            "returncode": 0 或其他,
            "stdout": "...",
            "stderr": "...",
            "cmd": [...],
            "cwd": "..."
        }
    """
    import os
    import subprocess
    import traceback

    result_info = {
        "ok": False,
        "returncode": None,
        "stdout": "",
        "stderr": "",
        "cmd": None,
        "cwd": None,
    }


    try:
        # 校验 coord 格式
        if not isinstance(coord, (tuple, list)) or len(coord) != 3:
            raise ValueError(f"坐标必须是一个包含三个数值的元组或列表，当前为: {coord!r}")

        x1, y1, z1 = coord
        coord_str = f"{x1},{y1},{z1}"

        # 保持你原来用相对路径的习惯：默认就是 "auto_TUPDSPACE.py"
        if script_path is None:
            script_path = "auto_TUPDSPACE.py"
        else:
            # 如果你以后想传绝对路径，也会在日志里打印出来
            script_path = os.path.abspath(script_path)

        cmd = [
            sys.executable,   # 当前 Python 解释器 (可能是 pythonw.exe)
            script_path,
            "--coord", coord_str
        ]

        result_info["cmd"] = cmd
        result_info["cwd"] = os.getcwd()

        print("========== [AUTO_TUPDSPACE] BEGIN ==========")
        print(f"[AUTO_TUPDSPACE] Python 可执行文件: {sys.executable}")
        print(f"[AUTO_TUPDSPACE] 当前工作目录 os.getcwd(): {os.getcwd()}")
        print(f"[AUTO_TUPDSPACE] auto_TUPDSPACE.py 路径参数: {script_path}")
        print(f"[AUTO_TUPDSPACE] 传入坐标参数: {coord_str}")
        print(f"[AUTO_TUPDSPACE] 最终命令行: {cmd}")

        creationflags = 0
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            creationflags = subprocess.CREATE_NO_WINDOW

        # 与你原来的行为尽量接近：不指定 cwd，由当前工作目录决定脚本位置
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=creationflags
        )

        result_info["returncode"] = proc.returncode
        result_info["stdout"] = proc.stdout or ""
        result_info["stderr"] = proc.stderr or ""

        print(f"[AUTO_TUPDSPACE] 子进程返回码 returncode = {proc.returncode}")
        if proc.stdout:
            print("----- [AUTO_TUPDSPACE] 子进程 STDOUT -----")
            print(proc.stdout)
            print("----- [AUTO_TUPDSPACE] END STDOUT -----")
        else:
            print("[AUTO_TUPDSPACE] 子进程 STDOUT 为空。")

        if proc.stderr:
            print("----- [AUTO_TUPDSPACE] 子进程 STDERR -----")
            print(proc.stderr)
            print("----- [AUTO_TUPDSPACE] END STDERR -----")
        else:
            print("[AUTO_TUPDSPACE] 子进程 STDERR 为空。")

        if proc.returncode == 0:
            result_info["ok"] = True
            print(f"✅ [AUTO_TUPDSPACE] 子程序成功完成：{coord_str}")
        else:
            print(f"❌ [AUTO_TUPDSPACE] 子程序返回非零状态码: {proc.returncode}")

        print("========== [AUTO_TUPDSPACE] END ==========")

    except Exception as e:
        print("❌ [AUTO_TUPDSPACE] 调用过程中发生异常（Python 主进程异常）:")
        print(repr(e))
        traceback.print_exc()

    return result_info

#&&% 单线变墙



def TDb_single_line_variable_wall(x1: float, y1: float, x2: float, y2: float, width: float = 240.0) -> bool:
    """
    单线变墙函数：将区域内的线段转换为天正墙体

    注意：此函数不使用 tlinebk 命令（会导致COM阻塞），
    而是直接读取线段端点并绘制天正墙体。

    Args:
        x1, y1: 区域左下角坐标
        x2, y2: 区域右上角坐标
        width: 墙体厚度，默认240

    Returns:
        bool: 成功返回True
    """
    from system.CAD_coordination import wait_quiescent

    from CAD_basic import (
        lines_daduan, get_acad_doc,
        set_object_property, normalize_rect, 
    )
    import CAD_basic as CAD_basic_module
    



    C.li()


    # 检查区域内是否有线段
    objs = select_objects_in_window_area(x1, y1, x2, y2)
    lines = [o for o in objs if getattr(o, "ObjectName", "") == "AcDbLine"]

    if not lines:
        print("[warn] 区域内没有线段，无需转换")
        return True  # 没有线段也算成功

    print(f"[info] 检测到 {len(lines)} 条线段")

    # 直接将线段转换为墙体（不使用tlinebk打断命令，避免COM阻塞）
    print(f"[stage] 直接转换线段为墙体 (thickness={width})")

    success = 0
    failed = 0

    for ln in lines:
        try:
            p1 = ln.StartPoint
            p2 = ln.EndPoint
            print(f"[info] 转换线段: {p1} -> {p2}")

            # 绘制天正墙
            result = draw_tarch_wall(p1, p2, thickness=width)
            if result:
                # 删除原线段
                try:
                    ln.Delete()
                except Exception as del_e:
                    print(f"[warn] 删除线段失败: {del_e}")
                success += 1
                print(f"[ok] 线段转换成功")
            else:
                failed += 1
                print(f"[warn] 线段转换失败")

            # 每次绘制后等待
            time.sleep(0.5)

        except Exception as exc:
            print(f"[warn] 转换失败: {exc}")
            failed += 1

    # 等待CAD完成
    try:
        wait_quiescent(min_quiet=0.5, timeout=10.0)
    except Exception:
        pass

    print(f"[done] 线段总数={len(lines)}, 成功={success}, 失败={failed}")
    return failed == 0




def convert_lines_to_walls(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    temp_width: float = 40.0,
    final_width: float = 240.0,  # Add final_width to pass for final thickness
) -> tuple[int, int, int]:
    """Convert lines to thin walls; return (detected_lines, success_walls, failed_walls)."""
    from system.CAD_coordination import wait_quiescent

    # 增加重试机制连接CAD
    max_retries = 5
    for attempt in range(max_retries):
        try:
            C.li()
            
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"[info] CAD连接失败，第{attempt+1}次重试... ({e})")
                time.sleep(1.0)
            else:
                print(f"[error] CAD连接失败: {e}")
                raise

    objs = select_objects_in_window_area(x1, y1, x2, y2)
    lines = [o for o in objs if getattr(o, "ObjectName", "") == "AcDbLine"]
    points = sum(1 for o in objs if getattr(o, "ObjectName", "").lower() == "acdbpoint")
    if points:
        print(f"[info] skipped {points} point objects")
    if not lines:
        print("[warn] no lines found after selection")
        return 0, 0, 0

    print(f"[info] lines to convert: {len(lines)}")
    success = failed = 0
    for ln in lines:
        try:
            p1 = ln.StartPoint
            p2 = ln.EndPoint
            draw_tarch_wall(p1, p2, thickness=temp_width)  # temp_width used for creating the temp walls
            ln.Delete()
            success += 1
            print(f"[ok] line {p1}->{p2} -> temp wall thickness {temp_width}")
        except Exception as exc:
            print(f"[warn] convert failed: {exc}")
            failed += 1
    
    # After temporary walls are drawn, set the final thickness to all walls
    print("[stage] set walls to final thickness after conversion")
    set_walls_thickness(x1, y1, x2, y2, width=final_width)

    return len(lines), success, failed



def set_walls_thickness(x1: float, y1: float, x2: float, y2: float, width: float) -> int:
    """Adjust all TDbWall objects in window to desired thickness. Return count."""
    C.li()
    objs = select_objects_in_window_area(x1, y1, x2, y2)
    count = 0
    for obj in objs:
        if getattr(obj, "ObjectName", "") == "TDbWall":
            try:
                set_object_property(obj, "Thickness", width/2)
                set_object_property(obj, "Thickness2", width/2)
                count += 1
            except Exception as exc:
                print(f"[warn] set thickness failed: {exc}")
    print(f"[info] walls set to thickness {width}: {count}")
    return count




#&&&&%% （四）  天正窗口

import time
import win32gui
import win32con
import pyautogui
from licad import C
import math
import json
import os


#&&&% 基本函数

def activate_cad_middle_click(hwnd):
    """【纯物理激活】中键点击"""
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        try: win32gui.SetForegroundWindow(hwnd)
        except: pass
        
        rect = win32gui.GetWindowRect(hwnd)
        cx = (rect[0] + rect[2]) // 2
        cy = (rect[1] + rect[3]) // 2
        
        pyautogui.moveTo(cx, cy)
        pyautogui.click(button='middle')
        time.sleep(0.1)
        return True
    except:
        return False

def insert_tarch_window_lisp_mode(wall_p1, wall_p2, cmd_name="TOpening"):
    """
    【函数编号】: TARCH-LISP-V20 (稳健等待版)
    【逻辑】: 
        1. 启动命令。
        2. 循环检测弹窗，直到它出现。
        3. 弹窗出现后，强制等待 3 秒 (不操作)。
        4. 激活 CAD，输入坐标，回车。
        D:/Mypro/基础服务/用户1/备份/插入天正门基本函数测试文件.dwg

        insert_tarch_window_lisp_mode(
            (178121.97856076437, 311217.5889781468, 0.0),
            (178274.28073210327, 311347.21940900886, 0.0),
            cmd_name="TOpening")        

    """
    mid_x = (wall_p1[0] + wall_p2[0]) / 2
    mid_y = (wall_p1[1] + wall_p2[1]) / 2
    
    # 1. 找句柄
    cad_hwnd = C.acad.HWND
    if not cad_hwnd: cad_hwnd = win32gui.FindWindow("AfxMDIFrame140u", None)
    print(f"🚀 [V20] 锁定 CAD: {cad_hwnd}")

    # 2. 启动命令
    activate_cad_middle_click(cad_hwnd)
    pyautogui.press('esc', presses=2, interval=0.1) 
    
    print(f"  -> 敲入命令: {cmd_name}")
    pyautogui.write(f'(command "{cmd_name}")\n', interval=0.05)
    
    # 3. 【关键步骤】死等弹窗出现
    possible_titles = ["门", "窗", "门窗", "天正图库管理系统", "门窗参数", "门窗设置"]
    hwnd_panel = 0
    
    print("  -> 正在侦测弹窗 (最长等 5 秒)...")
    for i in range(50): # 5秒
        for title in possible_titles:
            h = win32gui.FindWindow(None, title)
            if h and win32gui.IsWindowVisible(h):
                hwnd_panel = h
                print(f"  -> ✅ 弹窗已就位: {title}")
                break
        if hwnd_panel: break
        time.sleep(0.1)
    
    if not hwnd_panel:
        print("⚠️ 警告: 未检测到弹窗 (可能已打开或被遮挡)，继续尝试...")
    
    # 4. 【核心要求】强制冷却 3 秒
    # 此时弹窗刚出来，界面可能还在闪烁，焦点可能在跳动
    # 我们什么都不做，静静地等 3 秒
    print("  -> ❄️ 强制冷却 3 秒 (确保界面稳定)...")
    time.sleep(3.0)

    # 5. 激活窗口准备输坐标
    # 此时弹窗已经稳稳地悬浮在那里了，CAD 命令行也在闪烁等待输入了
    print("  -> 激活窗口 (中键)...")
    activate_cad_middle_click(cad_hwnd) 
    
    # 6. 输入坐标
    coord_str = f"{mid_x:.2f},{mid_y:.2f}"
    print(f"  -> 🎯 敲击坐标: {coord_str}")
    
    # 稳稳地输入
    pyautogui.write(coord_str, interval=0.1)
    
    # 7. 确认
    time.sleep(0.5)
    pyautogui.press('enter')
    
    # 8. 结束命令
    time.sleep(1.0)
    print("  -> 结束命令")
    pyautogui.press('esc') 
    
    print("✅ 完成。")
    return True

#&&&% 门类函数



# =============================================================================
# 模块：天正门窗自动化 (带示教缓存 & 多用户支持)
# =============================================================================

# 全局内存缓存
_TARCH_UI_CACHE = {}

def _get_dynamic_cache_path():
    """
    【核心配置】动态获取当前用户的缓存文件路径
    逻辑: 读取环境变量 USERPATH -> 拼接 Config 目录 -> 拼接文件名
    """
    # 1. 获取环境变量 (例如: D:\Mypro\基础服务\用户1)
    user_root = os.environ.get('USERPATH')

    # 2. 防呆保底: 如果没配置环境变量，默认存到当前脚本所在的目录下
    if not user_root:
        user_root = os.path.dirname(os.path.abspath(__file__))
    
    # 3. 构造完整路径
    return os.path.join(user_root, "Config", "tarch_ui_data.json")

def _load_cache_from_disk():
    """[内部] 从硬盘加载缓存到内存"""
    global _TARCH_UI_CACHE
    json_path = _get_dynamic_cache_path()
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                _TARCH_UI_CACHE = json.load(f)
    except Exception as e:
        print(f"⚠️ [系统] 读取缓存失败: {e}")
        _TARCH_UI_CACHE = {}

def _save_cache_to_disk():
    """[内部] 将内存缓存保存到硬盘"""
    json_path = _get_dynamic_cache_path()
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        # 写入文件
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(_TARCH_UI_CACHE, f, indent=4, ensure_ascii=False)
        print(f"💾 [系统] 配置已保存至: {json_path}")
    except Exception as e:
        print(f"❌ [系统] 保存缓存失败: {e}")

# 模块初始化时尝试加载一次
_load_cache_from_disk()

# -----------------------------------------------------------------------------
# 辅助函数
# -----------------------------------------------------------------------------

def _activate_cad_safe(hwnd):
    """
    【物理激活】鼠标移至窗口中心点击中键
    """
    try:
        if win32gui.IsIconic(hwnd): win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        try: win32gui.SetForegroundWindow(hwnd)
        except: pass
        
        rect = win32gui.GetWindowRect(hwnd)
        cx, cy = (rect[0]+rect[2])//2, (rect[1]+rect[3])//2
        
        pyautogui.moveTo(cx, cy)
        pyautogui.click(button='middle')
        time.sleep(0.1)
        return True
    except: return False

def _wait_for_user_hover(prompt, dwell_time=1.5):
    """
    【示教捕获】等待用户悬停鼠标来获取坐标
    """
    print(f"\n👉 {prompt}")
    print("   请移动鼠标到目标位置，然后【松手保持不动】...")
    
    last_pos = pyautogui.position()
    stable_start = None
    
    while True:
        curr_pos = pyautogui.position()
        dist = math.sqrt((curr_pos[0]-last_pos[0])**2 + (curr_pos[1]-last_pos[1])**2)
        
        # 5像素容差判定为静止
        if dist < 5: 
            if stable_start is None: 
                stable_start = time.time()
            elif time.time() - stable_start > dwell_time:
                print(f"   ✅ 坐标捕获: {curr_pos}")
                print('\a') # 提示音
                return curr_pos
        else:
            stable_start = None
            last_pos = curr_pos
        time.sleep(0.1)

# -----------------------------------------------------------------------------
# 核心业务函数
# -----------------------------------------------------------------------------

def insert_tarch_door_universal(wall_p1, wall_p2, door_key="普通门", cmd_name="TOpening", force_reteach=False):
    """
    【函数编号】: TARCH-UI-PRO-V2 (终极通用版)
    【功能】: 
        1. 自动识别并复用 'USERPATH' 下的缓存数据。
        2. 若 key 不存在，自动进入示教模式。
        3. 执行时使用 "目标-干扰-目标" 点击法破解天正记忆。
        4. 使用 "3秒冷却 + 纯坐标输入" 确保插入成功。
    
    【参数】:
        - wall_p1, wall_p2: 墙体两点
        - door_key: 门窗类型的唯一标识 (如 "双开防火门", "凸窗_1500")
        - cmd_name: 启动命令 (TOpening / TWindow)
        - force_reteach: True 强制重新录入坐标
    """
    global _TARCH_UI_CACHE
    
    # 确保缓存是最新的
    if not _TARCH_UI_CACHE:
        _load_cache_from_disk()

    # =========================================================================
    # 阶段一：示教录入 (如果缓存不存在)
    # =========================================================================
    if (door_key not in _TARCH_UI_CACHE) or force_reteach:
        print(f"\n🛠️ [示教模式] 新类型: {door_key}")
        print(f"   数据将保存至: {_get_dynamic_cache_path()}")
        
        # 1. 启动命令，让用户看到界面
        hwnd = C.acad.HWND
        if not hwnd: hwnd = win32gui.FindWindow("AfxMDIFrame140u", None)
        _activate_cad_safe(hwnd)
        pyautogui.press('esc', presses=2)
        pyautogui.write(f'(command "{cmd_name}")\n', interval=0.05)
        
        print("   ⏳ 等待界面弹出 (2秒)...")
        time.sleep(2.0)
        
        # 2. 开始录入
        data = {}
        # 步骤 1: 门类型下拉框
        data['pos_main_type'] = _wait_for_user_hover("【1/5】点击面板上的'门类型/窗类型'下拉框或图标")
        
        # 步骤 2: 打开图库
        data['pos_open_lib']  = _wait_for_user_hover("【2/5】点击带图片的'图库/表'按钮")
        input("⚠️ 请手动点击刚才的位置打开新窗口，看到新窗口后按【回车】继续...")
        
        # 步骤 3 & 4: 防记忆点击点
        print("--- 下面录入'防记忆'三连点 ---")
        data['pos_target_tree'] = _wait_for_user_hover("【3/5】点击左侧树状图的【目标类别】(如:平开门)")
        data['pos_other_tree']  = _wait_for_user_hover("【4/5】点击左侧树状图的【任意其他类别】(如:推拉门)用于刷新")
        
        # 步骤 5: 翻页与选择
        print("--- 下面录入选择动作 ---")
        data['pos_scroll_start'] = _wait_for_user_hover("【5a】鼠标在滚动条滑块上【按下】的位置 (若无需滚动则点空白处)")
        data['pos_scroll_end']   = _wait_for_user_hover("【5b】鼠标【拖拽松开】的位置 (若无需滚动则点同一点)")
        data['pos_select_item']  = _wait_for_user_hover("【6/5】双击具体门/窗样式的图标位置")
        
        # 3. 保存
        _TARCH_UI_CACHE[door_key] = data
        _save_cache_to_disk()
        
        # 4. 退出示教状态
        print("✅ 录入完成，重置环境...")
        pyautogui.press('esc', presses=3)
        time.sleep(0.5)

    # =========================================================================
    # 阶段二：自动化执行 (Playback)
    # =========================================================================
    try:
        cfg = _TARCH_UI_CACHE[door_key]
    except KeyError:
        print(f"❌ 错误: 找不到配置且录入失败: {door_key}")
        return False

    mid_x = (wall_p1[0] + wall_p2[0]) / 2
    mid_y = (wall_p1[1] + wall_p2[1]) / 2
    
    hwnd = C.acad.HWND
    if not hwnd: hwnd = win32gui.FindWindow("AfxMDIFrame140u", None)
    
    print(f"🚀 [自动执行] 插入: {door_key}")
    
    # A. 启动命令
    _activate_cad_safe(hwnd)
    pyautogui.press('esc', presses=2, interval=0.1)
    pyautogui.write(f'(command "{cmd_name}")\n', interval=0.05)
    
    # 盲等小面板
    time.sleep(1.5)
    
    # B. 机械操作流程
    # 1. 选大类
    pyautogui.click(cfg['pos_main_type'])
    time.sleep(0.5)
    
    # 2. 进图库
    pyautogui.click(cfg['pos_open_lib'])
    time.sleep(1.5) # 等大窗口
    
    # 3. 防记忆三连击 (目标 -> 干扰 -> 目标)
    # 这能强制天正刷新列表，确保位置正确
    pyautogui.click(cfg['pos_target_tree'])
    time.sleep(0.3)
    pyautogui.click(cfg['pos_other_tree'])
    time.sleep(0.3)
    pyautogui.click(cfg['pos_target_tree'])
    time.sleep(0.5)
    
    # 4. 翻页 (模拟拖拽)
    pyautogui.moveTo(cfg['pos_scroll_start'])
    pyautogui.dragTo(cfg['pos_scroll_end'], button='left', duration=0.5)
    time.sleep(0.5)
    
    # 5. 选中 (双击)
    pyautogui.doubleClick(cfg['pos_select_item'])
    # 双击后窗口通常会自动关闭，回到绘图区
    
    # C. 坐标输入 (复用之前的稳健逻辑)
    print("  -> ❄️ 强制冷却 3 秒 (等待命令就绪)...")
    time.sleep(3.0)
    
    # 激活并输入
    print("  -> 激活窗口...")
    _activate_cad_safe(hwnd)
    
    coord_str = f"{mid_x:.2f},{mid_y:.2f}"
    print(f"  -> 🎯 敲击坐标: {coord_str}")
    
    # 只能用 write 敲纯文本，不能用 list，不能用粘贴
    pyautogui.write(coord_str, interval=0.05)
    
    # 确认与结束
    time.sleep(0.5)
    pyautogui.press('enter')
    
    time.sleep(1.0)
    print("  -> 结束命令")
    pyautogui.press('esc') # 结束循环
    
    print(f"✅ [{door_key}] 插入完成。")
    return True





















































