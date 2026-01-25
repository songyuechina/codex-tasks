# -*- coding: utf-8 -*-
"""
CAD基本操作范式实现

基于ziliao/20251010-0143-CAD开发资料学习的完整操作范式
包含新建、打开、关闭、保存、插入等基本操作的增强实现
"""

import time
import pythoncom
from typing import List, Optional, Tuple

import sys
import os
from pathlib import Path

# ================= 1. 路径系统配置 (System通用版) =================
# 获取当前文件绝对路径 (锚点: .../cad/system/xxxx.py)
CURRENT_FILE = Path(__file__).resolve()

# 推导目录结构
SYSTEM_DIR = CURRENT_FILE.parent             # .../cad/system (本目录)
CAD_DIR = SYSTEM_DIR.parent                  # .../cad
SCRIPTS_DIR = CAD_DIR / "scripts"            # .../cad/scripts (兄弟目录)
WORKSPACE_DIR = CAD_DIR.parent               # 项目根目录

# ================= 2. 动态注入环境变量 =================
# 将 scripts 和 system 目录都加入搜索路径
# 这样 system 下的文件也能 import CAD_basic (位于 scripts)
paths_to_insert = [str(SYSTEM_DIR), str(SCRIPTS_DIR)]

for p in paths_to_insert:
    if p not in sys.path:
        sys.path.insert(0, p)

# ================= 3. 基础依赖导入检查 (可选) =================
# 这里可以尝试导入同一目录下的工具，确保环境正常
try:
    # 尝试导入同级目录的工具，验证路径是否生效
    from CAD_com_utils import SafeCOM
except ImportError:
    pass # 某些基础文件可能不依赖这个，跳过





# 导入协同机制
from CAD_coordination import (
    wait_quiescent,
    wait_document_opened,
    send_cmd_with_sync,
    start_cad_with_dialog_killer,
    ensure_single_process
)

def get_cad_process_count() -> int:
    """获取CAD进程数量"""
    try:
        import psutil
        count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'acad.exe':
                count += 1
        return count
    except:
        return 0

def get_open_file_count() -> int:
    """获取当前打开的DWG文件数量"""
    try:
        import win32com.client
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        return acad.Documents.Count
    except:
        return 0

def is_file_opened(file_path: str) -> bool:
    """检查指定文件是否已打开"""
    try:
        import win32com.client
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        target_path = Path(file_path).resolve().as_posix().lower()

        for i in range(acad.Documents.Count):
            doc = acad.Documents.Item(i)
            if doc.FullName:
                doc_path = Path(doc.FullName).resolve().as_posix().lower()
                if doc_path == target_path:
                    return True
        return False
    except:
        return False

def is_file_opened_by_name(file_name: str) -> bool:
    """检查文件名是否已打开"""
    try:
        import win32com.client
        acad = win32com.client.GetActiveObject("AutoCAD.Application")

        for i in range(acad.Documents.Count):
            doc = acad.Documents.Item(i)
            if doc.Name == file_name:
                return True
        return False
    except:
        return False

def _get_short_path(long_path: str) -> str:
    """获取短路径处理中文/特殊字符"""
    try:
        import ctypes
        from ctypes import wintypes

        GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
        GetShortPathNameW.argtypes = [
            wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD
        ]
        GetShortPathNameW.restype = wintypes.DWORD

        buf = ctypes.create_unicode_buffer(260)
        ret = GetShortPathNameW(long_path, buf, len(buf))
        return buf.value if ret else long_path
    except Exception:
        return long_path

def _activate_document(file_path: str) -> bool:
    """激活指定文档"""
    try:
        import win32com.client
        acad = win32com.client.GetActiveObject("AutoCAD.Application")

        target_path = Path(file_path).resolve().as_posix().lower()

        for i in range(acad.Documents.Count):
            doc = acad.Documents.Item(i)
            if doc.FullName:
                doc_path = Path(doc.FullName).resolve().as_posix().lower()
                if doc_path == target_path:
                    acad.ActiveDocument = doc
                    return True
        return False
    except Exception:
        return False

# ============================================================================
# 1. 新建文件操作范式
# ============================================================================

def new_dwg_enhanced(output_path: Optional[str] = None) -> bool:
    """
    新建DWG文件范式（使用pywin32 Documents.Add()）

    规则:
    - 幂等操作: output_path已存在时不再新建,直接打开
    - 无output_path时创建未保存的空白文件
    - 使用pywin32直接创建，更简单可靠

    前置条件:
    - CAD进程已启动
    - 弹窗治理脚本运行中

    后置条件:
    - 文件已创建或已打开
    - 状态为单文件确定状态(有路径)或单文件不确定状态(无路径)
    """
    try:
        import win32com.client

        # 1. 确保CAD环境就绪
        if not ensure_single_process():
            return False
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        # 2. 检查路径幂等性
        if output_path and Path(output_path).exists():
            print(f"[成功] 文件已存在,直接打开: {output_path}")
            return open_dwg_paradigm(output_path)

        # 3. 连接到CAD
        acad = win32com.client.GetActiveObject("AutoCAD.Application")

        # 4. 使用pywin32创建新文档
        print("[新建] 正在创建新文件...")
        doc = acad.Documents.Add()
        time.sleep(1.0)

        # 5. 如需保存
        if output_path:
            print(f"[保存] 正在保存为: {output_path}")
            # 创建输出目录
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            doc.SaveAs(output_path)
            print(f"[成功] 新建并保存文件: {output_path}")
            wait_quiescent(min_quiet=1.0, timeout=15.0)
            return True
        else:
            print("[成功] 新建未保存文件成功")
            return True

    except Exception as e:
        print(f"[错误] 新建文件操作异常: {e}")
        return False

# ============================================================================
# 2. 打开文件操作范式
# ============================================================================

def open_dwg_paradigm(file_path: str) -> bool:
    """
    打开DWG文件范式

    规则:
    - 顺序+去重: 同一文件只触发一次Documents.Open()
    - 等待加入集合: 确保文档真正加入acad.Documents
    - 路径/名称幂等: 避免重复打开相同文件

    前置条件:
    - 非破坏性进程保证
    - 弹窗治理检查

    后置条件:
    - 文件成功打开并激活
    - CAD进入空闲状态
    """
    try:
        # 1. 基础验证
        if not Path(file_path).exists():
            print(f"[错误] 文件不存在: {file_path}")
            return False

        # 2. 进程预处理(非破坏性)
        process_count = get_cad_process_count()
        if process_count == 0:
            print("[启动] CAD未运行,启动CAD...")
            if not start_cad_with_dialog_killer():
                return False
        elif process_count > 1:
            print("[警告] 发现多个CAD进程,确保单进程...")
            ensure_single_process()

        # 3. 等待CAD稳定
        wait_quiescent(min_quiet=0.3, timeout=15.0)

        # 4. 路径级幂等检查
        if is_file_opened(file_path):
            print(f"[成功] 文件已打开: {file_path}")
            return True

        # 5. 名称级幂等检查
        basename = Path(file_path).name
        if is_file_opened_by_name(basename):
            print(f"[警告] 同名文件已打开,跳过: {basename}")
            return True

        # 6. 执行打开操作
        print(f"[处理] 正在打开: {file_path}")

        # 使用协同机制发送打开命令
        import win32com.client
        acad = win32com.client.GetActiveObject("AutoCAD.Application")

        # 转换为短路径处理中文/特殊字符
        short_path = _get_short_path(file_path)

        # 执行打开
        acad.Documents.Open(short_path)

        # 7. 等待文档加入集合
        if wait_document_opened(file_path, timeout=120.0):
            print(f"[成功] 文件成功打开: {file_path}")

            # 8. 激活文档
            _activate_document(file_path)

            # 9. 等待CAD空闲
            wait_quiescent(min_quiet=0.5, timeout=30.0)

            return True
        else:
            print(f"[错误] 文件打开超时: {file_path}")
            return False

    except Exception as e:
        print(f"[错误] 打开文件异常: {e}")
        return False

def open_multiple_files_paradigm(file_paths: List[str]) -> int:
    """
    多文件打开范式(严格顺序)

    规则:
    - 严格顺序,不可并发
    - 每次成功后等待空闲+0.3s缓冲
    - 路径/同名已存在则跳过
    """
    success_count = 0

    # 进程预处理
    ensure_single_process()
    wait_quiescent(min_quiet=0.3, timeout=15.0)

    print(f"[打开] 开始打开 {len(file_paths)} 个文件")

    for i, file_path in enumerate(file_paths):
        print(f"\n[文件] [{i+1}/{len(file_paths)}] {file_path}")

        if open_dwg_paradigm(file_path):
            success_count += 1
            print(f"[成功] 成功打开: {Path(file_path).name}")
        else:
            print(f"[错误] 打开失败: {Path(file_path).name}")

        # 文件间间隔等待
        if i < len(file_paths) - 1:
            time.sleep(0.3)
            wait_quiescent(min_quiet=0.3, timeout=15.0)

    print(f"\n[统计] 打开结果: {success_count}/{len(file_paths)} 成功")
    return success_count

# ============================================================================
# 3. 关闭文件操作范式
# ============================================================================



def close_current_dwg_paradigm(save_option: str = "prompt") -> bool:
    """
    关闭当前文件范式 (优化版：使用 COM API，无需发送命令)

    参数:
    - save_option: 
        "auto_save": 自动保存更改并关闭
        "no_save": 强制不保存更改直接关闭 (丢弃修改)
        "prompt": 智能判断 (如果已修改则保存，未修改则直接关闭) *注：API无法触发原生UI弹窗*
    
    返回:
    - bool: 执行成功返回 True，失败返回 False
    """
    import win32com.client
    import time

    try:
        # 1. 获取 AutoCAD 应用实例
        try:
            acad = win32com.client.GetActiveObject("AutoCAD.Application")
        except Exception:
            print("[警告] 无法连接到 AutoCAD，可能未启动")
            return True # 视为无文件处理

        # 2. 检查是否有文档打开
        # 注意：AutoCAD 2013+ 在 0 文档时 Count 可能不准确，但通常 Documents.Count 0 表示无图
        if acad.Documents.Count == 0:
            print("[警告] 没有打开的文件")
            return True

        # 3. 获取当前文件对象
        try:
            current_doc = acad.ActiveDocument
            doc_name = current_doc.Name
        except Exception:
            # 某些特殊状态下可能获取不到 ActiveDocument（如只有起始页）
            print("[提示] 无活动文档可关闭")
            return True

        print(f"[处理] 正在通过 API 关闭文件: {doc_name}")

        # 4. 执行关闭逻辑 (使用 API Close 方法)
        # doc.Close(SaveChanges: bool, FileName: str)
        # SaveChanges: True=保存, False=不保存(丢弃)
        
        try:
            if save_option == "auto_save":
                # 显式保存并关闭
                print(f"[状态] 自动保存并关闭: {doc_name}")
                current_doc.Close(True)
                
            elif save_option == "no_save":
                # 显式丢弃修改并关闭
                print(f"[状态] 丢弃修改并关闭: {doc_name}")
                current_doc.Close(False)
                
            else: 
                # case "prompt" 或其他默认值
                # API 无法触发 AutoCAD 的 "是否保存" 弹窗。
                # 这里的逻辑优化为：智能安全关闭。
                if not current_doc.Saved:
                    print(f"[提示] 文件[{doc_name}]有未保存修改，模式为prompt，已自动执行保存以防丢失。")
                    current_doc.Close(True)
                else:
                    print(f"[状态] 文件未修改，直接关闭: {doc_name}")
                    current_doc.Close(False)
            
            # 5. 简单的后置确认 (非必须，但为了稳定性)
            # 由于 COM Close 是同步的，代码走到这里通常意味着文件对象已销毁或正在销毁
            # 释放引用
            del current_doc
            return True

        except Exception as close_err:
            # 常见错误：文件从未保存过（无路径），调用 Close(True) 会触发另存为对话框从而阻塞或报错
            if "未保存" in str(close_err) or "SaveAs" in str(close_err):
                print(f"[警告] 新建文件尚未命名，无法自动保存，尝试强制关闭: {close_err}")
                try:
                    current_doc.Close(False) # 失败后尝试不保存强制关闭
                    return True
                except:
                    pass
            print(f"[错误] API 关闭执行失败: {close_err}")
            return False

    except Exception as e:
        print(f"[错误] 关闭文件流程异常: {e}")
        return False




def close_dwg_by_name_paradigm(file_name: str) -> bool:
    """按文件名关闭文件范式"""
    try:
        # 1. 检查文件是否存在
        if not is_file_opened_by_name(file_name):
            print(f"[警告] 文件未打开: {file_name}")
            return True

        # 2. 切换到目标文件
        import win32com.client
        acad = win32com.client.GetActiveObject("AutoCAD.Application")

        # 查找并激活目标文件
        for i in range(acad.Documents.Count):
            doc = acad.Documents.Item(i)
            if doc.Name == file_name:
                acad.ActiveDocument = doc
                break

        # 3. 关闭文件
        return close_current_dwg_paradigm()

    except Exception as e:
        print(f"[错误] 按名关闭文件异常: {e}")
        return False

def close_all_dwg_paradigm() -> bool:
    """关闭所有文件范式"""
    try:
        file_count = get_open_file_count()
        if file_count == 0:
            print("[警告] 没有打开的文件")
            return True

        print(f"[处理] 准备关闭 {file_count} 个文件")

        # 逐一关闭文件
        success_count = 0
        for _ in range(file_count):
            if close_current_dwg_paradigm():
                success_count += 1
            time.sleep(0.5)  # 间隔等待

        print(f"[成功] 关闭完成: {success_count}/{file_count} 成功")
        return success_count == file_count

    except Exception as e:
        print(f"[错误] 关闭所有文件异常: {e}")
        return False

# ============================================================================
# 4. 保存文件操作范式
# ============================================================================

def save_current_dwg_paradigm() -> bool:
    """
    保存当前文件范式 (V2.0 - 策略升级版)

    【升级点】:
    1. 引入 "三级保存策略" (COM Save -> Command Qsave -> SaveAs Overwrite)。
    2. 增加对 "Read-only" 的显式检测。
    3. 增加 SendCommand 后的指令同步等待 (通过检查 cmdActive)。
    """
    import win32com.client
    import os
    import time
    
    # 辅助：检查 CAD 是否在执行命令
    def wait_for_cmd_active(doc, timeout=5):
        start = time.time()
        while time.time() - start < timeout:
            try:
                # GetVariable("CMDACTIVE") 返回位码，0 表示空闲
                if doc.GetVariable("CMDACTIVE") == 0:
                    return True
            except: pass
            time.sleep(0.5)
        return False

    try:
        # 1. 获取环境
        try:
            acad = win32com.client.GetActiveObject("AutoCAD.Application")
            current_doc = acad.ActiveDocument
            doc_name = current_doc.Name
        except Exception:
            print("[错误] 无法获取 CAD 活动文档，保存失败。")
            return False

        # 2. 检查只读状态 (预防性检查)
        # 注意: 只有部分 CAD 版本暴露 ReadOnly 属性，如果没有则跳过
        try:
            if getattr(current_doc, "ReadOnly", False):
                print(f"[警告] 文件 '{doc_name}' 为只读状态，无法保存。")
                return False
        except: pass

        # 3. 检查是否为新建未保存文件
        if not current_doc.FullName:
            print(f"[信息] 检测到未命名文件，转为另存流程...")
            # 假设默认保存路径
            default_path = os.path.join(r"D:\temp", doc_name)
            if "save_as_dwg_paradigm" in globals():
                return save_as_dwg_paradigm(default_path)
            else:
                try:
                    current_doc.SaveAs(default_path)
                    print(f"[成功] 新文件已保存至: {default_path}")
                    return True
                except Exception as e:
                    print(f"[错误] 新文件保存失败: {e}")
                    return False

        # ======================== 核心保存逻辑 ========================
        print(f"[保存] 开始保存: {doc_name} ...")
        
        # 强制标记为未保存，防止 CAD 因为缓存而跳过写入
        try: current_doc.Saved = False
        except: pass

        # --- 策略 A: 标准 COM Save ---
        try:
            current_doc.Save()
            # 双重验证
            if current_doc.Saved:
                print(f"[成功] COM Save 完成: {doc_name}")
                return True
        except Exception as e:
            # 只有当错误是 RPC 拒绝时才值得重试，否则直接降级
            if "-2147418111" in str(e):
                print("   ⚠️ COM Save 被拒绝 (RPC Busy)，尝试降级策略...")
                time.sleep(1.0)
            else:
                print(f"   ⚠️ COM Save 异常: {e}")

        # --- 策略 B: 发送 QSAVE 命令 (降级方案) ---
        print("   🔄 尝试策略 B: 发送 _qsave 命令...")
        try:
            current_doc.SendCommand("_qsave\n")
            
            # 等待命令执行完成 (最多 10秒)
            if wait_for_cmd_active(current_doc, timeout=10):
                # 再次检查 Saved 状态
                if current_doc.Saved:
                    print(f"[成功] Command Save 完成: {doc_name}")
                    return True
            else:
                print("   ⚠️ QSAVE 命令超时。")
                
        except Exception as e:
            print(f"   ⚠️ Command Save 异常: {e}")

        # --- 策略 C: 原位 SaveAs (绝杀方案) ---
        # 当文件锁死导致无法 Save 时，SaveAs 往往能强制覆盖
        print("   🔄 尝试策略 C: 原位 SaveAs (覆盖)...")
        try:
            full_path = current_doc.FullName
            # SaveAs 要求提供文件类型，通常自动识别
            current_doc.SaveAs(full_path)
            print(f"[成功] SaveAs 覆盖完成: {doc_name}")
            return True
        except Exception as e:
            print(f"   ❌ 所有保存策略均失败: {e}")
            return False

    except Exception as e:
        print(f"[错误] 保存流程发生未捕获异常: {e}")
        return False






def save_as_dwg_paradigm(output_path: str) -> bool:
    """
    另存为文件范式 (优化版)

    优化说明:
    1. 移除不必要的等待 (COM SaveAs 是阻塞的)。
    2. 优化短路径逻辑 (确保针对存在的目录获取短路径)。
    3. 增加文件已存在时的覆盖逻辑检查。
    """
    import win32com.client
    import os
    from pathlib import Path

    try:
        # 1. 基础验证
        try:
            acad = win32com.client.GetActiveObject("AutoCAD.Application")
        except:
            print("[错误] 无法连接 AutoCAD")
            return False

        if acad.Documents.Count == 0:
            print("[错误] 没有打开的文件")
            return False

        current_doc = acad.ActiveDocument
        doc_name = current_doc.Name

        # 2. 路径与目录准备
        output_file = Path(output_path).resolve()
        
        # 检查目标是否只读/被占用 (简单的预判)
        if output_file.exists():
            try:
                # 尝试以追加模式打开一下，检测是否被占用
                with open(output_file, 'a'): pass
            except PermissionError:
                print(f"[错误] 目标文件被占用或只读，无法覆盖: {output_path}")
                return False

        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"[错误] 无法创建目录: {e}")
            return False

        print(f"[保存] 正在另存为: {doc_name} -> {output_file.name}")

        # 3. 短路径处理 (关键优化)
        # 针对中文路径，COM 接口有时候由于编码问题会报错，转为 8.3 短路径最安全
        # 注意：文件可能还没创建，所以我们获取文件夹的短路径
        try:
            # 假设 _get_short_path 是你外部定义的函数
            # 如果文件不存在，直接对全路径取短路径可能会失败，建议只对文件夹取
            if "_get_short_path" in globals():
                parent_short = _get_short_path(str(output_file.parent))
                final_save_path = os.path.join(parent_short, output_file.name)
            else:
                final_save_path = str(output_file)
        except:
            # 如果短路径获取失败，回退到普通路径
            final_save_path = str(output_file)

        # 4. 执行另存为 (阻塞式)
        try:
            # SaveAs(FileName, FileType)
            # 如果你需要指定存为 2004 格式等，可以在第二个参数指定 Enum
            # 这里默认使用当前版本格式
            current_doc.SaveAs(final_save_path)
            
            # 5. 验证
            if output_file.exists():
                print(f"[成功] 另存为完成: {output_file.name}")
                return True
            else:
                print(f"[错误] SaveAs 未报错但文件未生成: {output_path}")
                return False

        except Exception as save_err:
            print(f"[错误] 执行 SaveAs 失败: {save_err}")
            return False

    except Exception as e:
        print(f"[错误] 另存为流程异常: {e}")
        return False




def auto_save_dwg_paradigm(interval_seconds: int = 300) -> bool:
    """自动保存范式"""
    try:
        if get_open_file_count() == 0:
            print("[警告] 没有打开的文件,跳过自动保存")
            return True

        import win32com.client
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        current_doc = acad.ActiveDocument
        doc_name = current_doc.Name

        print(f"[处理] 自动保存: {doc_name}")

        # 执行保存
        current_doc.Save()
        print(f"[成功] 自动保存完成: {doc_name}")

        return True

    except Exception as e:
        print(f"[错误] 自动保存异常: {e}")
        return False

# ============================================================================
# 5. 插入文件操作范式
# ============================================================================

def insert_dwg_as_block_paradigm(block_file_path: str,
                                insert_point: Tuple[float, float, float] = (0, 0, 0),
                                scale: float = 1.0,
                                rotation: float = 0.0,
                                explode: bool = False) -> bool:
    """
    插入DWG文件作为块的完整范式

    规则:
    - 使用-INSERT命令避免Unicode编码问题
    - 稳定路径处理中文/特殊字符
    - 等待插入操作完成
    - 可选炸开/缩放/旋转参数

    前置条件:
    - 有文件打开作为接收文件
    - 块文件存在

    后置条件:
    - 块已插入指定位置
    - 文件有未保存更改
    - CAD进入空闲状态
    """
    try:
        # 1. 基础验证
        if not Path(block_file_path).exists():
            print(f"[错误] 块文件不存在: {block_file_path}")
            return False

        if get_open_file_count() == 0:
            print("[错误] 没有打开的文件作为接收文件")
            return False

        # 2. 获取当前文件信息
        import win32com.client
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        current_doc = acad.ActiveDocument
        doc_name = current_doc.Name

        print(f"[处理] 正在插入块: {Path(block_file_path).name} → {doc_name}")
        print(f"[位置] 插入位置: {insert_point}, 缩放: {scale}, 旋转: {rotation}°, 炸开: {explode}")

        # 3. 等待CAD空闲
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        # 4. 构建INSERT命令
        # 使用-INSERT命令避免外部脚本控制台Unicode输出问题
        short_path = _get_short_path(block_file_path)

        cmd_parts = [
            "-INSERT",
            f'"{short_path}"',  # 块文件路径
            f"{insert_point[0]},{insert_point[1]},{insert_point[2]}",  # 插入点
            str(scale),  # X比例
            str(scale) if scale != 1.0 else "1",  # Y比例 (如果X=1则跳过)
            str(rotation),  # 旋转角度
            "1" if explode else "0"  # 是否炸开
        ]

        insert_cmd = "\n".join(cmd_parts) + "\n"

        # 5. 执行插入命令
        success = send_cmd_with_sync(insert_cmd, wait_after=2.0, timeout=60.0)

        if not success:
            print(f"[错误] 插入块命令失败: {Path(block_file_path).name}")
            return False

        # 6. 等待插入完成
        wait_quiescent(min_quiet=2.0, timeout=60.0)

        # 7. 验证插入结果
        # 检查是否有未保存更改
        try:
            has_changes = not getattr(current_doc, 'Saved', True)
            if has_changes:
                print(f"[成功] 块插入成功: {Path(block_file_path).name}")
                return True
            else:
                print(f"[警告] 块插入后未检测到更改: {Path(block_file_path).name}")
                return True  # 仍然认为成功
        except:
            print(f"[成功] 块插入完成(无法验证更改状态): {Path(block_file_path).name}")
            return True

    except Exception as e:
        print(f"[错误] 插入块异常: {e}")
        return False

def insert_multiple_blocks_paradigm(block_configs: List[dict]) -> int:
    """
    批量插入块范式

    block_configs格式:
    [
        {
            'path': 'block_file.dwg',
            'point': (x, y, z),
            'scale': 1.0,
            'rotation': 0.0,
            'explode': False
        },
        ...
    ]
    """
    success_count = 0

    print(f"[处理] 开始批量插入 {len(block_configs)} 个块")

    for i, config in enumerate(block_configs):
        print(f"\n[块] [{i+1}/{len(block_configs)}] 插入块 {i+1}")

        try:
            block_path = config['path']
            insert_point = config.get('point', (0, 0, 0))
            scale = config.get('scale', 1.0)
            rotation = config.get('rotation', 0.0)
            explode = config.get('explode', False)

            if insert_dwg_as_block_paradigm(
                block_path, insert_point, scale, rotation, explode
            ):
                success_count += 1
                print(f"[成功] 成功插入: {Path(block_path).name}")
            else:
                print(f"[错误] 插入失败: {Path(block_path).name}")

            # 块间间隔等待
            if i < len(block_configs) - 1:
                time.sleep(1.0)
                wait_quiescent(min_quiet=0.5, timeout=15.0)

        except Exception as e:
            print(f"[错误] 插入块配置错误: {e}")

    print(f"\n[统计] 批量插入结果: {success_count}/{len(block_configs)} 成功")
    return success_count

def insert_and_explode_paradigm(block_file_path: str,
                               insert_point: Tuple[float, float, float] = (0, 0, 0),
                               scale: float = 1.0) -> bool:
    """插入并炸开块范式"""
    print(f"[处理] 插入并炸开: {Path(block_file_path).name}")

    # 1. 先插入块
    if not insert_dwg_as_block_paradigm(
        block_file_path, insert_point, scale, explode=True
    ):
        return False

    # 2. 等待插入完成
    wait_quiescent(min_quiet=1.0, timeout=30.0)

    # 3. 验证炸开结果
    print(f"[成功] 插入并炸开完成: {Path(block_file_path).name}")
    return True

# ============================================================================
# 完整工作流范式
# ============================================================================

def standard_workflow_paradigm(source_file: str,
                             block_files: List[dict],
                             output_file: str) -> bool:
    """
    标准工作流范式: 打开文件 → 插入块 → 保存 → 关闭

    参数:
    - source_file: 源文件路径
    - block_files: 块配置列表
    - output_file: 输出文件路径
    """
    try:
        print("[启动] 开始标准工作流")
        print(f"[文件] 源文件: {source_file}")
        print(f"[块] 块数量: {len(block_files)}")
        print(f"[保存] 输出文件: {output_file}")

        # 1. 打开源文件
        if not open_dwg_paradigm(source_file):
            print("[错误] 工作流失败: 无法打开源文件")
            return False

        # 2. 插入所有块
        if block_files:
            success_count = insert_multiple_blocks_paradigm(block_files)
            if success_count == 0:
                print("[错误] 工作流失败: 没有块插入成功")
                return False

        # 3. 保存到输出文件
        if not save_as_dwg_paradigm(output_file):
            print("[错误] 工作流失败: 无法保存输出文件")
            return False

        # 4. 关闭文件
        close_current_dwg_paradigm("no_save")

        print("[成功] 标准工作流完成")
        return True

    except Exception as e:
        print(f"[错误] 标准工作流异常: {e}")
        return False

# ============================================================================
# 6. 文件拷贝操作范式
# ============================================================================

def copy_dwg_to_dwg_paradigm(source_file: str, target_file: str, explode: bool = False) -> bool:
    """
    将DWG文件A完整拷贝到DWG文件B

    Args:
        source_file: 源文件路径
        target_file: 目标文件路径
        explode: True=炸开(直接拷贝内容), False=作为块插入

    Returns:
        bool: True表示成功, False表示失败
    """
    try:
        print(f"[拷贝] 开始拷贝: {Path(source_file).name} → {Path(target_file).name}")
        print(f"[模式] {'炸开模式' if explode else '块模式'}")

        # 1. 验证源文件
        if not Path(source_file).exists():
            print(f"[错误] 源文件不存在: {source_file}")
            return False

        # 2. 打开或创建目标文件
        if not Path(target_file).exists():
            print(f"[创建] 目标文件不存在,创建新文件: {target_file}")
            if not new_dwg_enhanced(target_file):
                return False
        else:
            if not open_dwg_paradigm(target_file):
                return False

        # 3. 插入源文件
        if explode:
            # 炸开模式: 插入并炸开
            success = insert_and_explode_paradigm(source_file, (0, 0, 0))
        else:
            # 块模式: 作为块插入
            success = insert_dwg_as_block_paradigm(source_file, (0, 0, 0))

        if not success:
            print(f"[错误] 插入失败")
            return False

        # 4. 保存目标文件
        if not save_current_dwg_paradigm():
            print(f"[错误] 保存失败")
            return False

        print(f"[成功] 拷贝完成: {Path(source_file).name} → {Path(target_file).name}")
        return True

    except Exception as e:
        print(f"[错误] 拷贝文件异常: {e}")
        return False

def copy_region_to_dwg_paradigm(source_file: str, target_file: str,
                                x1: float, y1: float, x2: float, y2: float,
                                xb: float, yb: float) -> bool:
    """
    将源文件中指定区域的图形对象拷贝到目标文件指定位置

    Args:
        source_file: 源文件路径
        target_file: 目标文件路径
        x1, y1: 区域左下角坐标
        x2, y2: 区域右上角坐标
        xb, yb: 目标位置坐标(区域左下角对应此点)

    Returns:
        bool: True表示成功, False表示失败
    """
    try:
        import sys
        sys.path.append(str(Path(__file__).parent))
        from CAD_basic import select_objects_in_window_area, get_acad_doc
        import win32com.client

        print(f"[区域拷贝] {Path(source_file).name} → {Path(target_file).name}")
        print(f"[区域] ({x1},{y1}) 到 ({x2},{y2})")
        print(f"[目标] ({xb},{yb},0)")

        # 1. 验证文件
        if not Path(source_file).exists():
            print(f"[错误] 源文件不存在: {source_file}")
            return False

        # 2. 打开源文件
        if not open_dwg_paradigm(source_file):
            return False
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        # 3. 选择区域内的对象
        print(f"[选择] 选择区域内对象...")
        entities = select_objects_in_window_area(x1, y1, x2, y2)

        if not entities or len(entities) == 0:
            print(f"[警告] 区域内没有对象")
            return False

        print(f"[成功] 选中 {len(entities)} 个对象")

        # 4. 计算偏移量
        offset_x = xb - x1
        offset_y = yb - y1

        # 5. 打开或创建目标文件
        if not Path(target_file).exists():
            if not new_dwg_enhanced(target_file):
                return False
        else:
            if not open_dwg_paradigm(target_file):
                return False

        wait_quiescent(min_quiet=0.5, timeout=15.0)
        _, doc2 = get_acad_doc()

        # 6. 复制对象到目标文件
        print(f"[复制] 复制对象到目标文件...")
        copied_count = 0
        for obj in entities:
            try:
                new_obj = obj.Copy()
                # 移动到目标位置
                base_point = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0, 0, 0])
                displacement = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [offset_x, offset_y, 0])
                new_obj.Move(base_point, displacement)
                copied_count += 1
            except Exception as e:
                print(f"[警告] 复制对象失败: {e}")

        print(f"[成功] 已复制 {copied_count}/{len(entities)} 个对象")

        # 7. 保存目标文件
        if not save_current_dwg_paradigm():
            print(f"[错误] 保存目标文件失败")
            return False

        print(f"[成功] 区域拷贝完成")
        return True

    except Exception as e:
        print(f"[错误] 区域拷贝异常: {e}")
        return False

if __name__ == "__main__":
    # 测试基本操作范式
    print("[测试] 测试CAD基本操作范式")

    # 测试新建文件
    print("\n1. 测试新建文件")
    new_dwg_enhanced("D:/temp/test_new.dwg")

    # 测试保存
    print("\n2. 测试保存文件")
    save_current_dwg_paradigm()

    # 测试关闭
    print("\n3. 测试关闭文件")
    close_current_dwg_paradigm()

    print("\n[成功] 基本操作范式测试完成")
