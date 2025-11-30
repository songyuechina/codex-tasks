#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CAD文件操作统一接口

提供DWG文件的打开、新建、关闭、保存、另存、插入等基础操作
所有函数都集成了协同机制，可直接调用


"""

import sys
from pathlib import Path

# 路径常量（根据当前脚本位置自动推导，避免 workspace 迁移失败）
SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = SCRIPT_PATH.parent.parent          # D:/codex-tasks/cad
WORKSPACE_DIR = CAD_DIR.parent               # D:/codex-tasks
SYSTEM_DIR = CAD_DIR / "system"
LOGS_DIR = CAD_DIR / "logs"
XITONG_DIR = CAD_DIR / "xitongwenjian"
TESTS_DIR = WORKSPACE_DIR / "tests"

# 添加system路径以及当前脚本目录，确保可以导入 CAD_basic 与相关模块
sys.path.insert(0, str(SYSTEM_DIR))
sys.path.insert(0, str(SCRIPT_PATH.parent))

from CAD_basic_operations import (
    new_dwg_enhanced,
    open_dwg_paradigm,
    close_current_dwg_paradigm,
    close_all_dwg_paradigm,
    save_current_dwg_paradigm,
    save_as_dwg_paradigm,
    insert_dwg_as_block_paradigm,
    insert_and_explode_paradigm
)


#&&&&%% 第一部分  文件基础操作

# ============================================================================
# 文件新建与打开
# ============================================================================

#&&% 天正连接与检测

import CAD_basic as cb   # 建议放在文件头

def litz(max_connect_rounds: int = 3, wait_between_rounds: float = 2.0):
    """
    天正智能连接（基于 CAD_basic.li + close_all_cad_processes + start_applicationV9）

    增强点：
        - 在“杀光 + 启动天正CAD”之后，建立 COM 连接时，
          不再只尝试一轮 10 次，而是：
              · 外层最多 max_connect_rounds 轮（默认 3 轮）；
              · 每轮之间等待 wait_between_rounds 秒（默认 2 秒）；
              · 每一轮内部仍然是 10 次 0.5s 的 GetActiveObject 重试。
    """
    import time
    import win32com.client
    import pythoncom
    from CAD_basic import safe_delete  # 如果你之前是别的来源，这里保持一致即可

    global acad, doc, mp, sp
    import CAD_basic as cb
    from CAD_basic import close_all_cad_processes, start_applicationV9
    

    # ========= 第一步：用 CAD_basic.li() 连接当前 CAD，再画天正墙检测 =========
    try:
        ok = cb.li()  # 设置 cb.acad / cb.doc / cb.mp / cb.sp
        if not ok:
            raise RuntimeError("CAD_basic.li() 返回 False，当前 CAD 连接失败。")

        # —— 探针：在当前激活 DWG 中画一段天正墙 ——
        try:
            test_wall_result = draw_tarch_wall((0, 0, 0), (1000, 0, 0))
        except Exception as e_wall:
            # 画墙过程本身报错，直接视为"非天正"
            raise RuntimeError(f"draw_tarch_wall 抛异常，疑似非天正 CAD 环境：{e_wall}")

        if not test_wall_result:
            # False 或 None → 认为画墙失败
            raise RuntimeError("draw_tarch_wall 返回空/False，疑似非天正 CAD 环境。")

        # 删除测试用的天正墙
        try:
            from CAD_basic import last_obj
            test_wall_obj = last_obj()
            if test_wall_obj is not None:
                safe_delete(test_wall_obj)
                print("[litz] 已删除测试用天正墙")
        except Exception as e_del:
            print(f"[litz] 删除探针天正墙时出错（忽略）：{e_del}")

        # ====== 把 CAD_basic 里的全局同步到当前模块 ======
        acad, doc, mp, sp = cb.acad, cb.doc, cb.mp, cb.sp

        print("当前桌面文件：", doc.Name)
        print("[litz] 通过 CAD_basic.li() + 画天正墙探针，确认当前就是天正 CAD 环境，无需切换。")
        return True

    except Exception as e:
        # 探针失败：当前不是天正 CAD，进入“杀光重启”流程
        print(f"[litz] 当前 CAD 环境检测为非天正或异常，原因：{e}")
        print("[litz] 将调用 close_all_cad_processes() 杀掉所有 CAD，再用 start_applicationV9() 启动天正……")

    # ========= 第二步：关闭所有 CAD 进程，再启动天正 CAD =========
    try:
        try:
            close_all_cad_processes()
        except Exception as e0:
            print(f"[litz] 调用 close_all_cad_processes() 出现异常（忽略继续）：{e0}")

        start_applicationV9(
            PTH=r"C:\Tangent\TArchT20V9",
            max_retries=3,
            retry_delay=2.0
        )

    except Exception as e2:
        print(f"[litz] 调用 start_applicationV9() 失败：{e2}")
        return False

    # ========= 第三步：多轮重试，建立到“新启动”的天正 CAD 的 COM 连接 =========
    print("[litz] 正在建立连接到刚启动的天正CAD...")

    # 确保 COM 初始化
    try:
        pythoncom.CoInitialize()
    except:
        pass

    max_inner_retry = 10      # 每一轮内部的最多尝试次数
    success = False
    last_exc = None

    for round_idx in range(1, max_connect_rounds + 1):
        if round_idx > 1:
            print(f"[litz] 等待 {wait_between_rounds:.1f}s 后开始第 {round_idx} 轮连接重试...")
            time.sleep(wait_between_rounds)

        app = None
        doc_obj = None

        for attempt in range(1, max_inner_retry + 1):
            try:
                app = win32com.client.GetActiveObject("AutoCAD.Application")
                doc_obj = app.ActiveDocument
                # 验证文档可用
                _ = doc_obj.Name
                print(f"[litz] 第 {round_idx} 轮连接尝试：第 {attempt} 次成功连接到CAD。")
                success = True
                break
            except Exception as e_conn:
                last_exc = e_conn
                if attempt < max_inner_retry:
                    print(f"[litz] 第 {round_idx} 轮连接尝试：第 {attempt} 次失败，继续重试... ({e_conn})")
                    time.sleep(0.5)
                else:
                    print(f"[litz] 第 {round_idx} 轮连接尝试：连续 {max_inner_retry} 次失败。")

        if success and app is not None and doc_obj is not None:
            # 本轮已成功，跳出外层循环
            break

    if not success:
        print(f"[litz] 在重启后的天正 CAD 上多轮({max_connect_rounds}轮)重试后仍无法建立连接。最后错误：{last_exc}")
        return False

    # —— 连接成功：同步到 CAD_basic 与当前模块的全局变量 ——
    cb.acad = app
    cb.doc = doc_obj
    cb.mp = doc_obj.ModelSpace
    cb.sp = doc_obj.PaperSpace

    acad = app
    doc = doc_obj
    mp = doc_obj.ModelSpace
    sp = doc_obj.PaperSpace

    print("当前桌面文件：", doc.Name)
    print("[litz] 已通过 start_applicationV9 在天正 CAD 上成功建立连接。")
    return True

#&&% 新建dwg文件

def new_file(output_path=None, close_after=True):
    """Create a DWG file after verifying the current CAD/TArch context.

    Args:
        output_path (str | None): Target path; None keeps an unsaved blank file.
        close_after (bool): Close the newly created/opened file automatically when True.

    Returns:
        bool: True if the DWG was created or opened successfully.
    """
    import sys
    import time
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import (
        jingchengshu_wenjian,
        li,
        safe_delete,
        last_obj,
        get_open_document_names,
        close_dwg_by_name,
        get_acad_doc,
        get_all_open_dwg_paths
    )
    litz()

    def _close_new_file(result: bool) -> bool:
        """Close the active file when requested and ignore close errors."""
        if result and close_after:
            try:
                close_file("no_save")
            except Exception as exc:
                print(f"[警告] 关闭新建文件失败: {exc}")
        return result

    if output_path:
        target = Path(output_path)
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
            connected = li()
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




















def open_file(file_path):
    """
    打开DWG文件

    Args:
        file_path: 文件路径

    Returns:
        bool: 成功返回True
    """
    import sys
    import time
    import win32com.client
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import (
        start_applicationV9,
        jingchengshu_wenjian,
        get_open_document_names,
        close_dwg_by_name,
        get_acad_doc
    )
    litz()
    def _ensure_single_process():
        if jingchengshu_wenjian() > 1:
            print("[警告] 检测到多个 CAD 进程，执行重置...")
            cad_zt_zero()
            cad_zt_oneb()

    def _ensure_active_only():
        try:
            names = get_open_document_names()
        except Exception as exc:
            print(f"[警告] 获取已打开文件失败: {exc}")
            return True

        if len(names) <= 3:
            return True

        try:
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

    _ensure_single_process()

    def _get_acad():
        return win32com.client.GetActiveObject("AutoCAD.Application")

    # 确保CAD已启动
    try:
        acad = _get_acad()
    except:
        print("[信息] CAD未启动，正在启动天正...")
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        acad = _get_acad()

    if not _ensure_active_only():
        cad_zt_zero()
        cad_zt_oneb()
        acad = _get_acad()

    # 规范化路径
    target_path = str(Path(file_path).resolve()).lower()

    # 检查是否已经打开
    for doc in acad.Documents:
        if str(Path(doc.FullName).resolve()).lower() == target_path:
            print(f"[信息] 文件已打开: {file_path}")
            return True

    return open_dwg_paradigm(file_path)



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

def save_file():
    """
    保存当前文件

    Returns:
        bool: 成功返回True
    """
    return save_current_dwg_paradigm()

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

def close_file(save_option="auto_save"):
    """
    关闭当前文件

    Args:
        save_option: "auto_save"(默认，先保存再关闭), "no_save"(不保存), 其他值走原始策略

    Returns:
        bool: 成功返回True
    """
    li()
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

def close_all_files(save_option="auto_save"):
    """
    关闭所有文件

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
        from CAD_basic import get_open_document_names
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

# ============================================================================
# 文件插入
# ============================================================================

def insert_file_as_block(source_file, x=0, y=0, z=0, scale=1.0, rotation=0.0):
    """
    将文件作为块插入到当前文件

    Args:
        source_file: 源文件路径
        x, y, z: 插入位置坐标
        scale: 缩放比例
        rotation: 旋转角度

    Returns:
        bool: 成功返回True
    """
    litz()
    return insert_dwg_as_block_paradigm(
        source_file,
        insert_point=(x, y, z),
        scale=scale,
        rotation=rotation,
        explode=False
    )

def insert_file_exploded(source_file, x=0, y=0, z=0, scale=1.0):
    """
    将文件炸开插入到当前文件

    Args:
        source_file: 源文件路径
        x, y, z: 插入位置坐标
        scale: 缩放比例

    Returns:
        bool: 成功返回True

    """
    litz()
    return insert_and_explode_paradigm(
        source_file,
        insert_point=(x, y, z),
        scale=scale
    )

def copy_file_content_pywin32(source_file, target_file):
    """
    使用pywin32将源文件的所有对象复制到目标文件（推荐方法）

    自动处理两种情况：
    1. 如果复制的对象包含块引用，会自动炸开
    2. 如果是普通对象，直接复制

    Args:
        source_file: 源文件路径
        target_file: 目标文件路径（必须已存在）

    Returns:
        bool: 成功返回True
    """
    import win32com.client
    import pythoncom
    import time
    from pathlib import Path
    litz()
    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")

        # 解析路径
        source_path = str(Path(source_file).resolve())
        target_path = str(Path(target_file).resolve())

        print(f"[信息] 源文件: {source_path}")
        print(f"[信息] 目标文件: {target_path}")

        # 打开源文件
        print(f"[打开] 源文件...")
        source_doc = acad.Documents.Open(source_path)
        time.sleep(3)

        # 获取源文件的所有对象
        source_ms = source_doc.ModelSpace
        objects_count = source_ms.Count
        print(f"[信息] 源文件共有 {objects_count} 个对象")

        # 创建对象列表
        objects_to_copy = []
        for i in range(objects_count):
            try:
                obj = source_ms.Item(i)
                objects_to_copy.append(obj)
            except Exception:
                pass

        print(f"[信息] 准备复制 {len(objects_to_copy)} 个对象")

        # 检查目标文件是否已打开
        target_doc = None
        target_path_lower = target_path.lower()
        for doc in acad.Documents:
            try:
                if str(Path(doc.FullName).resolve()).lower() == target_path_lower:
                    target_doc = doc
                    print(f"[信息] 目标文件已打开，使用已打开的文档")
                    break
            except Exception:
                continue

        # 如果未打开，则打开目标文件
        if target_doc is None:
            print(f"[打开] 目标文件...")
            time.sleep(2)
            target_doc = acad.Documents.Open(target_path)
            time.sleep(3)

        # 获取目标ModelSpace
        target_ms = target_doc.ModelSpace

        # 准备对象数组
        obj_array = win32com.client.VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, objects_to_copy
        )

        # 复制对象从源文档到目标文档
        print(f"[复制] 正在复制对象...")
        id_pairs = source_doc.CopyObjects(obj_array, target_ms)
        print(f"[成功] 对象已复制")

        # 关闭源文件（不保存）
        source_doc.Close(False)
        print(f"[关闭] 源文件")

        # —— 查找块引用并炸开 —— #
        print(f"[检查] 查找块引用...")
        blocks_to_explode = []
        try:
            count_target = target_ms.Count
        except pythoncom.com_error as e:
            hresult = getattr(e, "hresult", None)
            if hresult == -2147417846:
                # 应用程序忙：不再强制遍历/炸块，也不强制保存
                print("[警告] AutoCAD 正在忙（应用程序正在使用中），"
                      "暂时跳过块引用检查和炸开步骤，不强制保存。")
                return True
            else:
                raise

        # 如果能正常拿到 Count，再去遍历炸块
        for i in range(count_target):
            try:
                obj = target_ms.Item(i)
                if obj.ObjectName == "AcDbBlockReference":
                    blocks_to_explode.append(obj)
            except pythoncom.com_error as e:
                hresult = getattr(e, "hresult", None)
                if hresult == -2147417846:
                    print("[警告] AutoCAD 在遍历对象时忙（应用程序正在使用中），"
                          "提前结束炸块检查。")
                    blocks_to_explode = []
                    break
                else:
                    continue
            except Exception:
                pass

        if blocks_to_explode:
            print(f"[炸开] 发现 {len(blocks_to_explode)} 个块，正在炸开...")
            for block in blocks_to_explode:
                try:
                    block.Explode()
                    block.Delete()
                except pythoncom.com_error as e:
                    hresult = getattr(e, "hresult", None)
                    if hresult == -2147417846:
                        print("[警告] AutoCAD 在炸开块时忙（应用程序正在使用中），"
                              "停止继续炸块。")
                        break
                    else:
                        continue
                except Exception:
                    pass
            print(f"[成功] 块已炸开")

        # 尝试保存目标文件（即使失败也不当成致命错误）
        try:
            target_doc.Save()
            print(f"[保存] 目标文件")
        except pythoncom.com_error as e:
            hresult = getattr(e, "hresult", None)
            if hresult == -2147417846:
                print("[警告] AutoCAD 在保存目标文件时忙（应用程序正在使用中），"
                      "此次不强制保存，请稍后手动保存。")
            else:
                print(f"[警告] 保存目标文件失败：{e}")

        return True

    except Exception as e:
        # 如果只是 AutoCAD 忙，也不要打红色大堆栈
        try:
            import pythoncom as _pc
            if isinstance(e, _pc.com_error):
                hresult = getattr(e, "hresult", None)
                if hresult == -2147417846:
                    print("[警告] copy_file_content_pywin32 遇到 AutoCAD 忙（应用程序正在使用中），"
                          "但对象很可能已经复制成功，返回 True。")
                    return True
        except Exception:
            pass

        print(f"[错误] {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# 区域选择与插入
# ============================================================================

def insert_region_from_file(source_file, x1, y1, x2, y2, x3, y3, explode=True):
    """
    将源文件中指定区域的对象插入到当前文件

    新方案：通过临时副本文件实现，避免剪贴板问题

    步骤：
    1. 打开源文件，复制副本，删除区域外的对象
    2. 将保留的对象移动到目标位置，保存副本
    3. 使用copy_file_content_pywin32将副本插入到当前文件

    Args:
        source_file: 源文件路径
        x1, y1: 区域左下角坐标
        x2, y2: 区域右上角坐标
        x3, y3: 目标位置(对应区域左下角)
        explode: 是否炸开(默认True)

    Returns:
        bool: 成功返回True
    """
    import sys
    import win32com.client
    import pythoncom
    import time
    import tempfile
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import li, select_entities_in_window
    from CAD_coordination import wait_quiescent, send_cmd_with_sync
    import win32com.client

    print(f"\n[开始] insert_region_from_file (新方案)")
    print(f"  源文件: {source_file}")
    print(f"  区域: ({x1},{y1}) -> ({x2},{y2})")
    print(f"  目标位置: ({x3},{y3})")

    temp_file = None
    litz()

    try:
        # 规范化矩形坐标
        x_lo, x_hi = (x1, x2) if x1 < x2 else (x2, x1)
        y_lo, y_hi = (y1, y2) if y1 < y2 else (y2, y1)
        print(f"[准备] 规范化区域坐标: ({x_lo},{y_lo}) -> ({x_hi},{y_hi})")

        # 步骤1: 打开源文件，复制副本，保留区域内对象
        print(f"\n[步骤1] 打开源文件并创建副本...")
        if not open_file(source_file):
            print(f"[错误] 打开源文件失败: {source_file}")
            return False
        print(f"[成功] 源文件已打开")
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        # 创建临时副本文件
        temp_dir = Path(tempfile.gettempdir())
        temp_file = temp_dir / f"region_temp_{int(time.time())}.dwg"
        print(f"[副本] 创建临时文件: {temp_file}")

        if not save_file_as(str(temp_file)):
            print(f"[错误] 创建副本失败")
            close_file("no_save")
            return False
        print(f"[成功] 副本已创建: {temp_file}")

        # 选择区域内对象，记录Handle
        print(f"\n[步骤1.1] 选择区域内对象...")
        entities = select_entities_in_window(x_lo, y_lo, x_hi, y_hi, ty=1.0, select_mode="_W")

        if not entities or len(entities) == 0:
            print(f"[警告] 区域内没有对象")
            close_file("no_save")
            if temp_file.exists():
                temp_file.unlink()
            return False

        print(f"[成功] 选中 {len(entities)} 个对象")

        # 记录要保留的对象的Handle
        keep_handles = set()
        for ent in entities:
            try:
                keep_handles.add(ent.Handle)
            except:
                pass
        print(f"[记录] 保留 {len(keep_handles)} 个对象的Handle")

        # 删除区域外的对象
        print(f"\n[步骤1.2] 删除区域外的对象...")
        li()
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        doc = acad.ActiveDocument
        model_space = doc.ModelSpace

        delete_count = 0
        for obj in model_space:
            try:
                if obj.Handle not in keep_handles:
                    obj.Delete()
                    delete_count += 1
            except:
                pass

        print(f"[成功] 删除了 {delete_count} 个区域外对象")
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        # 步骤2: 移动保留的对象到目标位置
        print(f"\n[步骤2] 移动对象到目标位置...")

        # 计算移动向量：从区域左下角到目标位置
        offset_x = x3 - x_lo
        offset_y = y3 - y_lo
        print(f"[计算] 移动向量: ({offset_x}, {offset_y})")

        # 使用MOVE命令移动对象
        # 先全选（因为只剩下需要的对象）
        select_all_cmd = "_SELECT\n_ALL\n\n"
        if not send_cmd_with_sync(select_all_cmd, wait_after=0.5, timeout=15.0):
            print(f"[错误] 全选命令失败")
            close_file("no_save")
            if temp_file.exists():
                temp_file.unlink()
            return False

        # 移动命令：基点是区域左下角，目标点是插入位置
        move_cmd = f"_MOVE\n{x_lo},{y_lo}\n{x3},{y3}\n"
        if not send_cmd_with_sync(move_cmd, wait_after=1.0, timeout=30.0):
            print(f"[错误] 移动命令失败")
            close_file("no_save")
            if temp_file.exists():
                temp_file.unlink()
            return False

        print(f"[成功] 对象已移动到目标位置")
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        # 保存副本文件
        print(f"\n[步骤2.1] 保存副本文件...")
        if not save_file():
            print(f"[错误] 保存副本失败")
            close_file("no_save")
            if temp_file.exists():
                temp_file.unlink()
            return False
        print(f"[成功] 副本已保存: {temp_file}")

        # 关闭副本文件
        close_cmd = "_CLOSE\nN\n"
        send_cmd_with_sync(close_cmd, wait_after=0.5, timeout=15.0)
        wait_quiescent(min_quiet=0.5, timeout=15.0)
        print(f"[成功] 副本文件已关闭")

        # 步骤3: 使用copy_file_content_pywin32插入副本到当前文件
        print(f"\n[步骤3] 将副本插入到当前激活文件...")

        # 获取当前激活文件路径
        li()
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        current_doc = acad.ActiveDocument
        current_file = current_doc.FullName
        print(f"[当前] 激活文件: {current_file}")

        # 使用成熟的copy_file_content_pywin32函数
        if not copy_file_content_pywin32(str(temp_file), current_file):
            print(f"[错误] 插入副本失败")
            if temp_file.exists():
                temp_file.unlink()
            return False

        print(f"[成功] 副本已插入到当前文件")

        # 清理临时文件
        print(f"\n[清理] 删除临时文件...")
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
                print(f"[成功] 临时文件已删除")
            except Exception as e:
                print(f"[警告] 删除临时文件失败: {e}")

        print(f"\n[完成] insert_region_from_file 执行成功")
        return True

    except Exception as e:
        print(f"\n[错误] 区域插入失败: {e}")
        import traceback
        traceback.print_exc()

        # 清理临时文件
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except:
                pass

        # 尝试清理
        try:
            close_cmd = "_CLOSE\nN\n"
            send_cmd_with_sync(close_cmd, wait_after=0.5, timeout=10.0)
        except:
            pass

        return False

def insert_region_between_files(source_file, target_file, x1, y1, x2, y2, x3, y3, explode=True):
    """
    直接将文件B的x1,y1,x2,y2区域的图形对象插入到文件A的指定点x3,y3

    这是insert_region_from_file的扩展版本，不需要先打开目标文件

    步骤：
    1. 打开源文件，复制副本，删除区域外的对象
    2. 将保留的对象移动到目标位置，保存副本
    3. 将副本内容插入到目标文件

    Args:
        source_file: 源文件路径（文件B）
        target_file: 目标文件路径（文件A）
        x1, y1: 区域左下角坐标
        x2, y2: 区域右上角坐标
        x3, y3: 目标位置(对应区域左下角)
        explode: 是否炸开(默认True)

    Returns:
        bool: 成功返回True
    """
    import sys
    import win32com.client
    import time
    import tempfile
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import li, select_entities_in_window
    from CAD_coordination import wait_quiescent, send_cmd_with_sync

    print(f"\n[开始] insert_region_between_files")
    print(f"  源文件: {source_file}")
    print(f"  目标文件: {target_file}")
    print(f"  区域: ({x1},{y1}) -> ({x2},{y2})")
    print(f"  目标位置: ({x3},{y3})")

    temp_file = None
    litz()

    try:
        # 规范化矩形坐标
        x_lo, x_hi = (x1, x2) if x1 < x2 else (x2, x1)
        y_lo, y_hi = (y1, y2) if y1 < y2 else (y2, y1)
        print(f"[准备] 规范化区域坐标: ({x_lo},{y_lo}) -> ({x_hi},{y_hi})")

        # 步骤1: 打开源文件，复制副本，保留区域内对象
        print(f"\n[步骤1] 打开源文件并创建副本...")
        if not open_file(source_file):
            print(f"[错误] 打开源文件失败: {source_file}")
            return False
        print(f"[成功] 源文件已打开")
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        # 创建临时副本文件
        temp_dir = Path(tempfile.gettempdir())
        temp_file = temp_dir / f"region_temp_{int(time.time())}.dwg"
        print(f"[副本] 创建临时文件: {temp_file}")

        if not save_file_as(str(temp_file)):
            print(f"[错误] 创建副本失败")
            close_file("no_save")
            return False
        print(f"[成功] 副本已创建: {temp_file}")

        # 选择区域内对象，记录Handle
        print(f"\n[步骤1.1] 选择区域内对象...")
        entities = select_entities_in_window(x_lo, y_lo, x_hi, y_hi, ty=1.0, select_mode="_W")

        if not entities or len(entities) == 0:
            print(f"[警告] 区域内没有对象")
            close_file("no_save")
            if temp_file.exists():
                temp_file.unlink()
            return False

        print(f"[成功] 选中 {len(entities)} 个对象")

        # 记录要保留的对象的Handle
        keep_handles = set()
        for ent in entities:
            try:
                keep_handles.add(ent.Handle)
            except:
                pass
        print(f"[记录] 保留 {len(keep_handles)} 个对象的Handle")

        # 删除区域外的对象
        print(f"\n[步骤1.2] 删除区域外的对象...")
        li()
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        doc = acad.ActiveDocument
        model_space = doc.ModelSpace

        delete_count = 0
        for obj in model_space:
            try:
                if obj.Handle not in keep_handles:
                    obj.Delete()
                    delete_count += 1
            except:
                pass

        print(f"[成功] 删除了 {delete_count} 个区域外对象")
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        # 步骤2: 移动保留的对象到目标位置
        print(f"\n[步骤2] 移动对象到目标位置...")

        # 计算移动向量：从区域左下角到目标位置
        offset_x = x3 - x_lo
        offset_y = y3 - y_lo
        print(f"[计算] 移动向量: ({offset_x}, {offset_y})")

        # 使用MOVE命令移动对象
        # 先全选（因为只剩下需要的对象）
        select_all_cmd = "_SELECT\n_ALL\n\n"
        if not send_cmd_with_sync(select_all_cmd, wait_after=0.5, timeout=15.0):
            print(f"[错误] 全选命令失败")
            close_file("no_save")
            if temp_file.exists():
                temp_file.unlink()
            return False

        # 移动命令：基点是区域左下角，目标点是插入位置
        move_cmd = f"_MOVE\n{x_lo},{y_lo}\n{x3},{y3}\n"
        if not send_cmd_with_sync(move_cmd, wait_after=1.0, timeout=30.0):
            print(f"[错误] 移动命令失败")
            close_file("no_save")
            if temp_file.exists():
                temp_file.unlink()
            return False

        print(f"[成功] 对象已移动到目标位置")
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        # 保存副本文件
        print(f"\n[步骤2.1] 保存副本文件...")
        if not save_file():
            print(f"[错误] 保存副本失败")
            close_file("no_save")
            if temp_file.exists():
                temp_file.unlink()
            return False
        print(f"[成功] 副本已保存: {temp_file}")

        # 关闭副本文件
        close_cmd = "_CLOSE\nN\n"
        send_cmd_with_sync(close_cmd, wait_after=0.5, timeout=15.0)
        wait_quiescent(min_quiet=0.5, timeout=15.0)
        print(f"[成功] 副本文件已关闭")

        # 步骤3: 使用copy_file_content_pywin32插入副本到目标文件
        print(f"\n[步骤3] 将副本插入到目标文件...")

        # 确保目标文件路径规范化
        target_path = str(Path(target_file).resolve())
        print(f"[目标] 文件: {target_path}")

        # 使用成熟的copy_file_content_pywin32函数
        if not copy_file_content_pywin32(str(temp_file), target_path):
            print(f"[错误] 插入副本失败")
            if temp_file.exists():
                temp_file.unlink()
            return False

        print(f"[成功] 副本已插入到目标文件")

        # 清理临时文件
        print(f"\n[清理] 删除临时文件...")
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
                print(f"[成功] 临时文件已删除")
            except Exception as e:
                print(f"[警告] 删除临时文件失败: {e}")

        print(f"\n[完成] insert_region_between_files 执行成功")

        close_file(save_option="auto_save")#关闭文件

        return True

    except Exception as e:
        print(f"\n[错误] 跨文件区域插入失败: {e}")
        import traceback
        traceback.print_exc()

        # 清理临时文件
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except:
                pass

        # 尝试清理
        try:
            close_cmd = "_CLOSE\nN\n"
            send_cmd_with_sync(close_cmd, wait_after=0.5, timeout=10.0)
        except:
            pass

        return False

# ============================================================================
# 标注
# ============================================================================

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
    li()
    import sys
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import dim_by_points as _dim_by_points
    return _dim_by_points(p1, p2, p3)

# ============================================================================
# 墙体和门窗
# ============================================================================

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
    li()
    import sys, time
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import last_obj, set_object_property
    from CAD_coordination import send_cmd_with_sync, wait_quiescent

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
                    set_object_property(wall, 'Thickness', thickness)
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
    from CAD_basic import get_acad_doc, get_object_property, set_object_property
    from CAD_coordination import send_cmd_with_sync, wait_quiescent

    li()
    try:
        _, doc = get_acad_doc()
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

if __name__ == "__main__":
    print("CAD文件操作统一接口")
    print("="*60)
    print("\n可用函数:")
    print("  new_file(path)           - 新建文件")
    print("  open_file(path)          - 打开文件")
    print("  save_file()              - 保存文件")
    print("  save_file_as(path)       - 另存为")
    print("  close_file(option)       - 关闭文件")
    print("  close_all_files()        - 关闭所有文件")
    print("  insert_file_as_block()   - 插入为块")
    print("  insert_file_exploded()   - 插入并炸开")
    print("  copy_file_content_pywin32() - 拷贝文件内容（推荐）")

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
        li, stc, get_object_property, set_object_property,
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
    li()
    try:
        # 1. 检查窗类型
        if window_type not in allowed_types:
            logger.error(f"窗类型错误: {window_type}, 允许的类型: {allowed_types}")
            print(f"[错误] 窗类型错误: {window_type}")
            return {'success': False, 'window': None, 'width': None, 'height': None}
        logger.info(f"窗类型检查通过: {window_type}")
        print(f"[信息] 窗类型检查通过: {window_type}")

        # 2. 连接当前激活文件
        li()
        logger.info("已连接当前激活文件")
        print("[信息] 已连接当前激活文件")

        # 3. 检查是否需要插入MC_yuan.dwg
        lb = stc('Mc_yuan_bj')
        if len(lb) == 0:
            logger.info("未找到Mc_yuan_bj图层，需要插入MC_yuan.dwg")
            print("[信息] 未找到Mc_yuan_bj图层，正在插入MC_yuan.dwg...")
            # 获取当前文件路径
            import win32com.client
            acad = win32com.client.GetActiveObject("AutoCAD.Application")
            current_file = acad.ActiveDocument.FullName
            logger.info(f"当前文件: {current_file}")
            copy_file_content_pywin32(str(XITONG_DIR / "MC_yuan.dwg"), current_file)
            logger.info("已插入MC_yuan.dwg")
            print("[成功] 已插入MC_yuan.dwg")
            # 重新连接
            li()
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

    except Exception as e:
        logger.error(f"插入窗失败: {e}", exc_info=True)
        print(f"[错误] 插入窗失败: {e}")
        return {'success': False, 'window': None, 'width': None, 'height': None}




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

    if not li():
        print("[警告] li() 连接失败，当前控制对象未确定")
        return False

    print(f"[成功] 已激活文件: {actual_name}")
    return True


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


def cad_zt_oneb():
    """
    确保CAD状态为：1个进程+1个空白文件（单文件不确定状态）
    """
    import sys
    import time
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import jingchengshu_wenjian, close_all_cad_processes, start_applicationV9
    from CAD_coordination import wait_quiescent

    shu = jingchengshu_wenjian()
    if shu == 0:
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
    elif shu > 0:
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
    return True


def cad_zt_oned(file_path=str(XITONG_DIR / "0.dwg")):
    """
    确保CAD状态为：1个进程+1个指定文件（单文件确定状态）

    Args:
        file_path: 要打开的文件路径，默认为 cad/xitongwenjian/0.dwg
    """
    import sys
    import time
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import jingchengshu_wenjian, close_all_cad_processes, start_applicationV9, close_all_except_active_safe
    from CAD_file_operations import open_file
    from CAD_coordination import wait_quiescent

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
        from CAD_basic import li
        li()
        close_all_except_active_safe()
    return True


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
    from CAD_basic import jingchengshu_wenjian, close_all_cad_processes, start_applicationV9, get_open_document_names, close_dwg_by_name
    from CAD_file_operations import open_file
    from CAD_coordination import wait_quiescent

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
        from CAD_basic import li
        li()
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
    from CAD_basic import jingchengshu_wenjian, close_all_cad_processes, start_applicationV9, get_open_document_names
    from CAD_file_operations import open_file

    shu = jingchengshu_wenjian()
    if shu == 0:
        import time
        from CAD_coordination import wait_quiescent
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
        open_file(file3)
    elif shu > 1:
        import time
        from CAD_coordination import wait_quiescent
        close_all_cad_processes()
        time.sleep(1)
        start_applicationV9(PTH=r"C:\Tangent\TArchT20V9", max_retries=3, retry_delay=2.0)
        wait_quiescent(min_quiet=2.0, timeout=30.0)
        open_file(file1)
        open_file(file2)
        open_file(file3)
    elif shu == 1:
        from CAD_basic import li
        li()
        open_docs = get_open_document_names()
        files_to_open = [file1, file2, file3]
        for f in files_to_open:
            if len(open_docs) >= 3:
                break
            open_file(f)
            open_docs = get_open_document_names()
    return True



#&&&&%% 第二部分  天正房间

#&&% 获取天正房间

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
    li()

    # 1. 规范化矩形坐标
    (x_lo, y_lo), (x_hi, y_hi) = normalize_rect(x1, y1, x2, y2)
    print(f"[TUPDSPACE_ROOM] 规范化矩形: 左下=({x_lo},{y_lo}), 右上=({x_hi},{y_hi})")

    # 2. 窗口选择 + 夹点编辑状态
    print("[TUPDSPACE_ROOM] 调用 select_entities_in_window 进行窗口选择 ...")
    try:
        com_list = select_entities_in_window(x_lo, y_lo, x_hi, y_hi, ty=ty, select_mode="_W")
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


#&&% 单线变墙


def ensure_cad_ready():
    acad, doc = get_acad_doc()
    try:
        CAD_basic_module.acad = acad
    except Exception:
        pass
    return acad, doc




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
    li()
    ensure_cad_ready()
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
    ensure_cad_ready()
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





def TDb_single_line_variable_wall(x1: float, y1: float, x2: float, y2: float, width: float = 240.0) -> bool:
    li()
    ensure_cad_ready()
    print(f"[stage] tlinebk break window ({x1},{y1}) -> ({x2},{y2})")
    lines_daduan((x1, y1, 0), (x2, y2, 0))
    time.sleep(0.8)

    print("[stage] convert lines to temp walls (thickness 40)")
    total, ok, fail = convert_lines_to_walls(x1, y1, x2, y2, temp_width=40.0)

    print(f"[stage] set walls to final thickness {width}")
    adjusted = set_walls_thickness(x1, y1, x2, y2, width)

    print(f"[done] lines detected {total}, walls success {ok}, failed {fail}, adjusted {adjusted}")
    return fail == 0







#文字处理
# 实现策略: 先创建基本文字,再逐步修改属性

# ==================== 函数1: 写入CAD单行文字 ====================

def write_cad_text(
    p=(0, 0, 0),
    text="单行文字danhangwenzi",
    alignment="左下",      # 推荐用 "左下"/"左上"/"右下"/"右上"/"中心"，兼容"左对齐"/"居中"/"右对齐"
    height=350,
    width_factor=1.0,
    rotation=0.0,
    oblique=0.0,
    style="Standard"
):
    """
    在指定位置写入 CAD 单行文字（AcDbText），并通过外包盒对齐到目标点 p。

    对齐规则（基于外包盒）：
        - "左下" / "左对齐" / "LB"       : 外包盒左下角对齐到 p
        - "左上" / "LT"                 : 外包盒左上角对齐到 p
        - "右下" / "右对齐" / "RB"      : 外包盒右下角对齐到 p
        - "右上" / "RT"                 : 外包盒右上角对齐到 p
        - "中心" / "居中" / "center"/"C": 外包盒中心对齐到 p

    参数:
        p: 插入点坐标 (x, y, z)，默认(0, 0, 0)；对齐后“视觉位置”以 p 为锚点。
        text: 文字内容，默认"单行文字danhangwenzi"
        alignment: 对齐方式（见上），默认"左下"
        height: 文字高度，默认350（你的绘图单位）
        width_factor: 宽度因子，默认1.0
        rotation: 旋转角度(度)，默认0（绕 Z 轴）
        oblique: 倾斜角度(度)，默认0
        style: 文字样式名称，默认"Standard"

    返回:
        text_obj: 创建并对齐后的文字对象 (IAcadText)
    """
    import sys
    from pathlib import Path
    import math
    import pythoncom
    import win32com.client
    from win32com.client import VARIANT

    # 如果你希望复用 li() 保证 doc/mp 一致，也可以这样：
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import li  # noqa

    # —— 小工具：基于外包盒对齐 —— #
    def _align_entity_by_bbox(ent, target_point, align="左下"):
        """
        使用无参数 GetBoundingBox()：
          1. min_pt, max_pt = ent.GetBoundingBox()
          2. 根据 align 选锚点
          3. Move(锚点 → 目标点)
        """
        try:
            min_pt, max_pt = ent.GetBoundingBox()
        except Exception as e:
            print(f"[错误] 获取外包盒失败: {e}")
            return

        xmin, ymin, zmin = min_pt
        xmax, ymax, zmax = max_pt
        print(f"[对齐-前]  BBox min={min_pt}, max={max_pt}")

        alg = str(align).strip().lower()
        if alg in ("左下", "左对齐", "lb"):
            anchor_pt = (xmin, ymin, zmin)
        elif alg in ("左上", "lt"):
            anchor_pt = (xmin, ymax, zmin)
        elif alg in ("右下", "右对齐", "rb"):
            anchor_pt = (xmax, ymin, zmin)
        elif alg in ("右上", "rt"):
            anchor_pt = (xmax, ymax, zmin)
        elif alg in ("中心", "居中", "center", "c"):
            anchor_pt = ((xmin + xmax) / 2.0,
                         (ymin + ymax) / 2.0,
                         (zmin + zmax) / 2.0)
        else:
            # 未识别就按左下处理
            anchor_pt = (xmin, ymin, zmin)

        # 目标点：如果传的是 (x, y)，z 用当前 zmin；否则使用传入 z
        if len(target_point) == 2:
            tx, ty = float(target_point[0]), float(target_point[1])
            tz = float(zmin)
        else:
            tx, ty, tz = float(target_point[0]), float(target_point[1]), float(target_point[2])

        target_pt = (tx, ty, tz)

        print(f"[对齐-计算] alignment='{align}', anchor_pt={anchor_pt} → target_pt={target_pt}")

        from_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, anchor_pt)
        to_pt   = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, target_pt)
        ent.Move(from_pt, to_pt)

        # 再读一次外包盒看结果
        try:
            min_pt2, max_pt2 = ent.GetBoundingBox()
            print(f"[对齐-后]  BBox min={min_pt2}, max={max_pt2}")
        except Exception as e:
            print(f"[警告] 对齐后再次获取外包盒失败: {e}")

    try:
        # 0. 可选：先 li() 一下，保证 CAD_basic 的 doc/mp 状态一致
        li()

        # 1. 获取 CAD 应用/文档/模型空间
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        doc = acad.ActiveDocument
        ms  = doc.ModelSpace

        # 2. 创建基本文字（只设内容、插入点、高度）
        #    注意 AddText 的第三个参数是高度，不带单位转换
        insert_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(p))
        text_obj  = ms.AddText(text, insert_pt, height)
        print(f"[步骤1] 已创建基本文字: \"{text}\"，插入点约为 {p}，高度={height}")

        # 3. 修改文字样式
        try:
            text_obj.StyleName = style
            print(f"[步骤2] 设置样式: {style}")
        except Exception as e:
            print(f"[警告] 设置样式失败: {e}")

        # 4. 修改宽度因子
        try:
            text_obj.ScaleFactor = width_factor
            print(f"[步骤3] 设置宽度因子: {width_factor}")
        except Exception as e:
            print(f"[警告] 设置宽度因子失败: {e}")

        # 5. 修改旋转角度（度 → 弧度）
        try:
            text_obj.Rotation = math.radians(rotation)
            print(f"[步骤4] 设置旋转角度: {rotation}°")
        except Exception as e:
            print(f"[警告] 设置旋转角度失败: {e}")

        # 6. 修改倾斜角度（度 → 弧度）
        try:
            text_obj.ObliqueAngle = math.radians(oblique)
            print(f"[步骤5] 设置倾斜角度: {oblique}°")
        except Exception as e:
            print(f"[警告] 设置倾斜角度失败: {e}")

        # 7. 使用外包盒对齐到 p（而不是依赖 AutoCAD 内部的 Alignment/Justify）
        try:
            _align_entity_by_bbox(text_obj, p, align=alignment or "左下")
        except Exception as e:
            print(f"[警告] 外包盒对齐失败: {e}")

        print(f"[完成] CAD 单行文字创建并对齐成功，目标锚点 ≈ {p}\n")
        return text_obj

    except Exception as e:
        print(f"[错误] 创建 CAD 单行文字失败: {e}")
        import traceback
        traceback.print_exc()
        return None

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
    import sys
    import time
    from pathlib import Path
    import pythoncom
    import win32com.client
    from win32com.client import VARIANT

    # 引入 CAD_basic 工具
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import li, stc, set_object_property, last_obj  # noqa

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
            print(f"[错误] 获取外包盒失败: {e}")
            return

        xmin, ymin, zmin = min_pt
        xmax, ymax, zmax = max_pt
        print(f"[对齐-前]  BBox min={min_pt}, max={max_pt}")

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

        print(f"[对齐-计算] alignment='{align}', anchor_pt={anchor_pt} → target_pt={target_pt}")

        from_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, anchor_pt)
        to_pt   = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, target_pt)
        ent.Move(from_pt, to_pt)

        # 再读一次外包盒看结果
        try:
            min_pt2, max_pt2 = ent.GetBoundingBox()
            print(f"[对齐-后]  BBox min={min_pt2}, max={max_pt2}")
        except Exception as e:
            print(f"[警告] 对齐后再次获取外包盒失败: {e}")

    try:
        # ===== 1. 确保连接到当前 DWG =====
        li()
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        doc  = acad.ActiveDocument

        # ===== 2. 查找/插入系统模板文字 =====
        lb = stc(system_layer)
        if len(lb) == 0:
            # 需要从系统文件插入一次模板
            system_file = Path(XITONG_DIR) / system_file_name
            if not system_file.exists():
                print(f"[错误] 系统天正文字文件不存在: {system_file}")
                return None

            current_file = doc.FullName
            print(f"[信息] 未找到系统文字图层 {system_layer}，从 {system_file} 插入...")

            try:
                # 本模块中已有 copy_file_content_pywin32，直接调用
                ok = copy_file_content_pywin32(str(system_file), current_file)
                if not ok:
                    print("[警告] copy_file_content_pywin32 返回 False，可能部分失败，但继续尝试。")
            except Exception as e:
                print(f"[警告] 插入系统文字文件时抛出异常：{e}，继续尝试查找图层。")

            # 再 li 一次，重新查模板
            li()
            acad = win32com.client.GetActiveObject("AutoCAD.Application")
            doc  = acad.ActiveDocument
            lb   = stc(system_layer)

        if len(lb) == 0:
            print(f"[错误] 即使插入系统文件后，仍未在图层 {system_layer} 找到模板文字。")
            return None
        elif len(lb) > 1:
            print(f"[警告] 图层 {system_layer} 上找到 {len(lb)} 个对象，默认使用第一个作为模板。")

        template = lb[0]
        print(f"[信息] 使用模板文字: ObjectName={template.ObjectName}, Handle={template.Handle}")

        # ===== 3. 从模板 Copy 出新文字对象（不对齐） =====
        try:
            new_text = template.Copy()
        except Exception as e:
            print(f"[错误] 无法从模板文字 Copy 新对象：{e}")
            return None

        print(f"[DEBUG] 复制得到的新文字: ObjectName={new_text.ObjectName}, Handle={new_text.Handle}")

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
            print(f"[警告] 设置天正文字属性时出错：{e}")

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

        li()
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        doc  = acad.ActiveDocument

        try:
            ent = last_obj()
        except Exception as e:
            print(f"[错误] 调用 last_obj() 失败: {e}")
            return None

        # last_obj 可能返回单个对象或列表
        try:
            _ = ent.ObjectName
        except Exception:
            try:
                ent = ent[-1]
            except Exception as e:
                print(f"[错误] last_obj() 返回值类型无法识别: {e}")
                return None

        objname = getattr(ent, "ObjectName", "<无>")
        handle  = getattr(ent, "Handle", "<无>")
        print(f"[DEBUG] last_obj() 得到实体: ObjectName={objname}, Handle={handle}")

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
                print(f"[成功] 已删除 {cnt} 个系统文字模板对象")
            except Exception as e:
                print(f"[警告] 删除系统模板文字失败：{e}")

        print(f"[完成] 天正单行文字创建成功，位置约为 {p}\n")
        return ent  # 返回对齐后的实体

    except Exception as e:
        print(f"[错误] write_tianzheng_text 执行失败：{e}")
        import traceback
        traceback.print_exc()
        return None


# ====================  文字垂直对齐 ====================

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
    import numbers
    import pythoncom
    from win32com.client import VARIANT
    li()
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
            print(f"[错误] 无法从 x_position={x_position!r} 解析出 X 坐标。")
            return False

    print(f"[信息] 垂直对齐目标 X = {x_target}，处理对象数量 = {len(objs)}")

    # —— 3. 遍历对齐每一个对象 —— #
    success_count = 0

    for idx, obj in enumerate(objs, start=1):
        try:
            # 3.1 获取 BoundingBox（无参数版本）
            ll_pt, ur_pt = obj.GetBoundingBox()
            print(f"[对象#{idx}] 原外包盒: min={ll_pt}, max={ur_pt}")

            # 3.2 计算移动距离
            if align_side == "左边界":
                dx = x_target - float(ll_pt[0])
            elif align_side == "右边界":
                dx = x_target - float(ur_pt[0])
            else:
                print(f"[对象#{idx}] [错误] 不支持的对齐方式: {align_side}")
                continue

            # 3.3 执行移动（只沿 X 方向）
            base_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
            move_vec = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [dx, 0.0, 0.0])
            obj.Move(base_pt, move_vec)

            # 3.4 再读一遍外包盒验证
            ll_pt2, ur_pt2 = obj.GetBoundingBox()
            print(f"[对象#{idx}] 新外包盒: min={ll_pt2}, max={ur_pt2}")
            print(f"[对象#{idx}] [成功] 文字{align_side}已对齐到 X={x_target}")
            success_count += 1

        except Exception as e:
            print(f"[对象#{idx}] [错误] 垂直对齐失败: {e}")

    if success_count == 0:
        print("[结果] 所有对象对齐都失败。")
        return False
    elif success_count < len(objs):
        print(f"[结果] 部分对齐成功: 成功 {success_count} / {len(objs)}")
        return False
    else:
        print(f"[结果] 全部 {success_count} 个对象已成功对齐到 X={x_target}")
        return True

# ====================  文字水平对齐 ====================
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
    import numbers
    import pythoncom
    from win32com.client import VARIANT
    li()
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
            print(f"[错误] 无法从 y_position={y_position!r} 解析出 Y 坐标。")
            return False

    print(f"[信息] 水平对齐目标 Y = {y_target}，处理对象数量 = {len(objs)}")

    # —— 3. 遍历对齐每一个对象 —— #
    success_count = 0

    for idx, obj in enumerate(objs, start=1):
        try:
            # 3.1 获取 BoundingBox（无参数版本）
            ll_pt, ur_pt = obj.GetBoundingBox()
            print(f"[对象#{idx}] 原外包盒: min={ll_pt}, max={ur_pt}")

            # 3.2 计算移动距离
            if align_side == "下边界":
                dy = y_target - float(ll_pt[1])
            elif align_side == "上边界":
                dy = y_target - float(ur_pt[1])
            else:
                print(f"[对象#{idx}] [错误] 不支持的对齐方式: {align_side}")
                continue

            # 3.3 执行移动（只沿 Y 方向）
            base_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
            move_vec = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, dy, 0.0])
            obj.Move(base_pt, move_vec)

            # 3.4 再读一遍外包盒验证
            ll_pt2, ur_pt2 = obj.GetBoundingBox()
            print(f"[对象#{idx}] 新外包盒: min={ll_pt2}, max={ur_pt2}")
            print(f"[对象#{idx}] [成功] 文字{align_side}已对齐到 Y={y_target}")
            success_count += 1

        except Exception as e:
            print(f"[对象#{idx}] [错误] 水平对齐失败: {e}")

    if success_count == 0:
        print("[结果] 所有对象水平对齐都失败。")
        return False
    elif success_count < len(objs):
        print(f"[结果] 部分水平对齐成功: 成功 {success_count} / {len(objs)}")
        return False
    else:
        print(f"[结果] 全部 {success_count} 个对象已成功对齐到 Y={y_target}")
        return True

# ====================  缩放天正文字高度 ====================

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
    import numbers
    import pythoncom
    from win32com.client import VARIANT
    li()
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
        print(f"[错误] 获取 CAD 文字 BoundingBox 失败: {e}")
        return False

    if not isinstance(cad_height, numbers.Real) or cad_height == 0:
        print(f"[错误] CAD 文字高度无效: {cad_height}")
        return False

    print(f"[信息] 目标 CAD 文字高度 = {cad_height:.4f}，待缩放对象数 = {len(tz_objs)}")

    # —— 3. 遍历缩放每一个天正文字 —— #
    success_count = 0

    for idx, tz_obj in enumerate(tz_objs, start=1):
        try:
            # 3.1 获取天正文字的 BoundingBox（无参数版）
            tz_ll_pt, tz_ur_pt = tz_obj.GetBoundingBox()
            tz_height = float(tz_ur_pt[1]) - float(tz_ll_pt[1])

            print(f"[对象#{idx}] 原外包盒: min={tz_ll_pt}, max={tz_ur_pt}")
            print(f"[对象#{idx}] 原高度: {tz_height:.4f}")

            if tz_height == 0:
                print(f"[对象#{idx}] [错误] 天正文字高度为 0，跳过。")
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

            print(f"[对象#{idx}] [成功] 已缩放天正文字")
            print(f"  原高度: {tz_height:.4f}")
            print(f"  目标高度: {cad_height:.4f}")
            print(f"  实际新高度: {new_height:.4f}")
            print(f"  缩放比例: {scale_factor:.6f}")
            success_count += 1

        except Exception as e:
            print(f"[对象#{idx}] [错误] 缩放失败: {e}")

    if success_count == 0:
        print("[结果] 所有天正文字缩放都失败。")
        return False
    elif success_count < len(tz_objs):
        print(f"[结果] 部分缩放成功: 成功 {success_count} / {len(tz_objs)}")
        return False
    else:
        print(f"[结果] 全部 {success_count} 个天正文字已成功缩放到 CAD 文字高度。")
        return True

# ==================== 块处理核心函数 (2025-11-22新增) ====================

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
    """
    import time
    import pythoncom
    import win32com.client
    from win32com.client import VARIANT

    # ---------- 1. 获取应用与文档 ----------
    acad = win32com.client.Dispatch("AutoCAD.Application")
    try:
        # 如果你有 get_acad_doc，就优先用它保证 doc 正确
        _, doc = get_acad_doc()
    except NameError:
        doc = acad.ActiveDocument
    ms = doc.ModelSpace

    # ---------- 2. 窗口选取实体 ----------
    entities = select_entities_in_window(
        x1, y1, x2, y2,
        ty=ty,
        select_mode="_W",
    )
    if not entities:
        print("[警告] 矩形区域内没有对象，无法创建块")
        return None

    print(f"[信息] 选中 {len(entities)} 个对象")

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
    print(f"[信息] 块基点(外包盒角点): {base_corner}")

    # 决定块实例插入点
    if base_point is None:
        insert_pt = base_corner      # 就地替换
    else:
        insert_pt = base_point       # 整体挪到指定点
    print(f"[信息] 块实例插入位置: {insert_pt}")

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

    print(f"[信息] 块名: {block_name}")

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
            print(f"[警告] GetBoundingBox 失败: {ex}")
            return None, None

    # ---------- 6. 克隆函数：实体 → 块定义（相对 base_corner） ----------
    def clone_entity_to_block(ent):
        try:
            obj_name = com_retry(lambda: ent.ObjectName)
        except Exception as e:
            print(f"[警告] 无法获取实体类型: {e}")
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
            print(f"[提示] 暂不支持的实体类型: {obj_name}，将保留在原位置。")
            return False

        except Exception as e:
            print(f"[警告] 克隆实体 {obj_name} 失败: {e}")
            return False

    # ---------- 7. 克隆 & 删除原对象 ----------
    cloned_count = 0
    skipped_count = 0

    for ent in list(entities):
        ok = False
        try:
            ok = clone_entity_to_block(ent)
        except Exception as e:
            print(f"[警告] 处理实体失败: {e}")
            ok = False

        if ok:
            try:
                ent.Delete()
                cloned_count += 1
            except Exception as e:
                print(f"[警告] 删除原实体失败: {e}")
                skipped_count += 1
        else:
            skipped_count += 1

    print(f"[信息] 成功克隆并删除 {cloned_count} 个实体，"
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
        block_ref = ms.InsertBlock(ins_variant, block_name, 1.0, 1.0, 1.0, 0.0)
    except Exception as e:
        print(f"[错误] 插入块实例失败: {e}")
        return None

    print(f"[成功] 已创建块 {block_name}，插入块实例并替换原图形。")
    return block_ref


def create_block_from_region_cmd(
    x1, y1, x2, y2,
    insert_point_option="左下",
    block_name_prefix="块",
    base_point=None,      # 不传则就地替换，传了则整体挪到 base_point
    ty: float = 1.0,
):
    """
    【命令行版】通过 -BLOCK 从矩形区域创建块（保留天正对象），
    然后用块实例替换原对象。

    步骤概述：
      1. 用 SelectionSet.Window 选中区域对象（仅用于 bbox 和删除，不影响命令行）；
      2. 用 group_bbox_corners 计算整体外包盒，按 insert_point_option 选基点；
      3. 生成不重名块名；
      4. 发送命令行：
           _.-BLOCK
           块名
           基点X,Y
           W
           x_lo,y_lo
           x_hi,y_hi
           ""       ← 回车，结束选择
         ——只建 block 定义，不依赖 Retain/Convert/Delete；
      5. 用 COM 在 insert_point（默认 = 基点）插入块参照；
      6. 删除第 1 步选中的原对象。

    返回:
        block_ref 块参照对象（IAcadBlockReference），失败返回 None。
    """
    import time
    import pythoncom
    import win32com.client
    from win32com.client import VARIANT, constants

    acad = win32com.client.Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    ms = doc.ModelSpace

    # ---------- 小工具：归一化矩形 ----------
    def _normalize_rect(a1, b1, a2, b2):
        x_lo = min(a1, a2)
        x_hi = max(a1, a2)
        y_lo = min(b1, b2)
        y_hi = max(b1, b2)
        return (x_lo, y_lo), (x_hi, y_hi)

    (x_lo, y_lo), (x_hi, y_hi) = _normalize_rect(x1, y1, x2, y2)

    # ---------- 1. 用 SelectionSet.Window 做“后台选取” ----------
    ss_name = "ZB_TMP_BLOCK_SEL"
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
        print(f"[错误] SelectionSet.Window 选择失败: {e}")
        try:
            ss.Delete()
        except Exception:
            pass
        return None

    entities = list(ss)
    try:
        ss.Delete()
    except Exception:
        pass

    if not entities:
        print("[警告] 矩形区域内没有对象，无法创建块")
        return None

    print(f"[信息] 后台选中 {len(entities)} 个对象（含天正对象），用于外包盒和删除。")

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
    print(f"[信息] 块基点(外包盒角点): {base_corner}")

    # 决定块实例插入点：不指定就就地替换（基点位置），指定则整体挪到 base_point
    if base_point is None:
        insert_pt = base_corner
    else:
        insert_pt = base_point
    print(f"[信息] 块实例插入位置: {insert_pt}")

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

    print(f"[信息] 计划创建块名: {block_name}")

    # ---------- 4. 用 -BLOCK + W 窗口，只建块定义 ----------
    base_pt_str = f"{bx},{by}"
    win_p1_str = f"{x_lo},{y_lo}"
    win_p2_str = f"{x_hi},{y_hi}"

    cmd_lines = [
        "_.-BLOCK",   # 启动 -BLOCK
        block_name,   # 块名
        base_pt_str,  # 基点坐标
        "W",          # 选择对象方式：窗口
        win_p1_str,   # 窗口第一角点
        win_p2_str,   # 窗口对角点
        "",           # 回车：结束选择
        # 不再发 C/R/D，让 -BLOCK 用默认行为（通常 = 仅建定义，保留原对象）
    ]
    cmd = "\n".join(cmd_lines) + "\n"

    print("[信息] 发送命令流 -BLOCK（窗口选择，只建块定义）...")
    time.sleep(ty)
    doc.SendCommand(cmd)

    # 等命令执行完一点（根据图形复杂度可调大）
    time.sleep(ty)

    # ---------- 5. 用 COM 插入块实例到 insert_pt ----------
    ins_variant = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(insert_pt))
    try:
        block_ref = ms.InsertBlock(ins_variant, block_name, 1.0, 1.0, 1.0, 0.0)
    except Exception as e:
        print(f"[错误] 插入块实例失败: {e}")
        return None

    # ---------- 6. 删除原对象 ----------
    deleted = 0
    for ent in entities:
        try:
            ent.Delete()
            deleted += 1
        except Exception:
            # 如果将来某种情况下 BLOCK 自己变动/删除了对象，这里失败就直接跳过
            pass

    print(f"[成功] 已创建块 {block_name}，插入块实例，并删除 {deleted} 个原对象。")
    return block_ref


def copy_block_contents_at_same_location(block_ref):
    """
    【函数2】获取块内图形并在原位置复制

    思路：
        1. 复制一份块参照（与 block_ref 完全重合）；
        2. 对复制出来的块参照执行 Explode()；
        3. 删除临时块参照；
        4. 返回 Explode 产生的新实体列表。

    优点：
        - 位置、比例、旋转全部由 AutoCAD 自己处理；
        - 包括嵌套块在内的所有内容都会展开到当前空间；
        - 原 block_ref 保留不动。
    """
    import win32com.client

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
        print(f"[信息] Explode 产生 {len(copied_entities)} 个实体。")

        # 3. 删除临时块参照，保留原块参照不动
        try:
            temp_ref.Delete()
        except Exception:
            pass

        print(f"[成功] 已在原位置复制块内容（保留原块参照），复制实体数: {len(copied_entities)}")
        return copied_entities

    except Exception as e:
        print(f"[错误] 操作失败: {e}")
        return []


##yuanweirukuai
def add_entities_to_block_keep_world(block_ref, entities, keep_source: bool = False):
    """
    【函数3】将块外的一组对象“加入块”，并可选择是否保留源对象

    思路：
      - 原对象的几何形状和世界坐标不变；
      - 在块定义中创建一份“局部坐标系下”的几何副本；
      - 利用块参照的 InsertionPoint / Rotation / ScaleFactor / 块定义 Origin
        做世界坐标 → 块局部坐标的逆变换；
      - 通过 block_ref 显示出来时，块里的副本会和原对象重合。

    参数:
        block_ref : 块参照对象（IAcadBlockReference）
        entities  : 需要加入块的实体列表（COM 对象列表）
        keep_source : 是否保留源对象
                      False（默认）→ 克隆成功后删除源对象
                      True         → 仅在块中增加副本，源对象保留

    支持的实体类型：
      - AcDbLine / AcDbCircle / AcDbArc
      - AcDbPolyline / AcDb2dPolyline / AcDb3dPolyline / AcDbLWPolyline
      - AcDbText / AcDbMText
      - AcDbPoint
      其他类型（包括天正对象、外部块参照）暂时跳过。
    """
    import win32com.client
    import pythoncom
    import math
    from win32com.client import VARIANT

    new_ents_in_block = []

    try:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument

        # 块定义：优先用 EffectiveName（兼容动态块）
        try:
            block_name = block_ref.EffectiveName
            block_def = doc.Blocks.Item(block_name)
        except Exception:
            block_name = block_ref.Name
            block_def = doc.Blocks.Item(block_name)

        print(f"[信息] 目标块: {block_name}")
        origin = block_def.Origin  # 块定义原点 (Ox, Oy, Oz)

        # 块参照变换信息（世界 → 局部 需要用逆变换）
        ins_pt   = block_ref.InsertionPoint  # 插入点
        sx       = block_ref.XScaleFactor or 1.0
        sy       = block_ref.YScaleFactor or 1.0
        sz       = block_ref.ZScaleFactor or 1.0
        rotation = block_ref.Rotation or 0.0    # 弧度

        ox, oy, oz = origin
        ix, iy, iz = ins_pt

        cos_r = math.cos(-rotation)
        sin_r = math.sin(-rotation)

        if abs(sx) < 1e-9: sx = 1.0
        if abs(sy) < 1e-9: sy = 1.0
        if abs(sz) < 1e-9: sz = 1.0

        def world_to_block(pt):
            """
            世界坐标 pt = (xw, yw, zw)
            求块局部坐标 Pb = (xb, yb, zb)，满足：
              P_world = InsertPoint + R * S * (Pb - Origin)
            """
            xw, yw, zw = pt

            # Step1: 世界 → 以插入点为原点
            vx = xw - ix
            vy = yw - iy
            vz = zw - iz

            # Step2: 逆旋转
            x1 = cos_r * vx + sin_r * vy
            y1 = -sin_r * vx + cos_r * vy
            z1 = vz

            # Step3: 逆缩放
            xr = x1 / sx
            yr = y1 / sy
            zr = z1 / sz

            # Step4: 加回块定义 Origin
            xb = ox + xr
            yb = oy + yr
            zb = oz + zr
            return (xb, yb, zb)

        def bbox_two_points(e):
            try:
                bb_min, bb_max = e.GetBoundingBox()
                return bb_min, bb_max
            except Exception as ex:
                print(f"[警告] GetBoundingBox 失败: {ex}")
                return None, None

        for ent in entities:
            try:
                obj_name = com_retry(lambda: ent.ObjectName)
            except Exception as e:
                print(f"[警告] 获取实体类型失败: {e}")
                continue

            success = False  # 当前实体是否成功加入块

            try:
                # ---------- Line ----------
                if obj_name == "AcDbLine":
                    sp = get_object_property(ent, "StartPoint")
                    ep = get_object_property(ent, "EndPoint")
                    if sp is None or ep is None:
                        sp, ep = bbox_two_points(ent)
                        if sp is None or ep is None:
                            print("[警告] 无法获取 Line 端点，跳过")
                            pass
                        else:
                            sp_b = world_to_block(sp)
                            ep_b = world_to_block(ep)
                            v_sp = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(sp_b))
                            v_ep = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(ep_b))
                            new_ent = block_def.AddLine(v_sp, v_ep)
                            new_ents_in_block.append(new_ent)
                            success = True
                    else:
                        sp_b = world_to_block(sp)
                        ep_b = world_to_block(ep)
                        v_sp = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(sp_b))
                        v_ep = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(ep_b))
                        new_ent = block_def.AddLine(v_sp, v_ep)
                        new_ents_in_block.append(new_ent)
                        success = True

                # ---------- Circle ----------
                elif obj_name == "AcDbCircle":
                    center = get_object_property(ent, "Center")
                    radius_w = get_object_property(ent, "Radius")
                    if center is None or radius_w is None:
                        print("[警告] 无法获取 Circle 属性，跳过")
                    else:
                        cen_b = world_to_block(center)
                        avg_s = (sx + sy) / 2.0
                        radius_b = radius_w / avg_s if avg_s != 0 else radius_w
                        v_cen = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(cen_b))
                        new_ent = block_def.AddCircle(v_cen, radius_b)
                        new_ents_in_block.append(new_ent)
                        success = True

                # ---------- Arc ----------
                elif obj_name == "AcDbArc":
                    center = get_object_property(ent, "Center")
                    radius_w = get_object_property(ent, "Radius")
                    sa_w = get_object_property(ent, "StartAngle")
                    ea_w = get_object_property(ent, "EndAngle")
                    if None in (center, radius_w, sa_w, ea_w):
                        print("[警告] 无法获取 Arc 属性，跳过")
                    else:
                        cen_b = world_to_block(center)
                        avg_s = (sx + sy) / 2.0
                        radius_b = radius_w / avg_s if avg_s != 0 else radius_w
                        v_cen = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(cen_b))
                        new_ent = block_def.AddArc(v_cen, radius_b, sa_w, ea_w)
                        new_ents_in_block.append(new_ent)
                        success = True

                # ---------- Polyline / 2d/3d / LW ----------
                elif obj_name in ("AcDbPolyline", "AcDb2dPolyline",
                                  "AcDb3dPolyline", "AcDbLWPolyline"):
                    coords = get_object_property(ent, "Coordinates")
                    if coords is None:
                        print("[警告] 无法获取多段线坐标，跳过")
                    else:
                        coords = list(coords)
                        new_coords = []
                        for i in range(0, len(coords), 3):
                            pt_w = (coords[i], coords[i+1], coords[i+2])
                            pb = world_to_block(pt_w)
                            new_coords.extend(pb)
                        v_pts = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, new_coords)
                        new_ent = block_def.AddPolyline(v_pts)
                        new_ents_in_block.append(new_ent)
                        success = True

                # ---------- Text ----------
                elif obj_name == "AcDbText":
                    ins = get_object_property(ent, "InsertionPoint")
                    txt = get_object_property(ent, "TextString")
                    h_w = get_object_property(ent, "Height")
                    if ins is None or txt is None or h_w is None:
                        print("[警告] 无法获取 Text 属性，跳过")
                    else:
                        ins_b = world_to_block(ins)
                        avg_s = (sx + sy) / 2.0
                        h_b = h_w / avg_s if avg_s != 0 else h_w
                        v_ins = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(ins_b))
                        new_txt = block_def.AddText(txt, v_ins, h_b)
                        rot_w = get_object_property(ent, "Rotation") or 0.0
                        try:
                            new_txt.Rotation = rot_w - rotation
                        except Exception:
                            pass
                        new_ents_in_block.append(new_txt)
                        success = True

                # ---------- MText ----------
                elif obj_name == "AcDbMText":
                    ins = get_object_property(ent, "InsertionPoint")
                    width_w = get_object_property(ent, "Width")
                    contents = get_object_property(ent, "Contents")
                    if ins is None or width_w is None or contents is None:
                        print("[警告] 无法获取 MText 属性，跳过")
                    else:
                        ins_b = world_to_block(ins)
                        avg_s = (sx + sy) / 2.0
                        width_b = width_w / avg_s if avg_s != 0 else width_w
                        v_ins = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(ins_b))
                        new_mt = block_def.AddMText(v_ins, width_b, contents)
                        ht_w = get_object_property(ent, "TextHeight")
                        rot_w = get_object_property(ent, "Rotation") or 0.0
                        try:
                            if ht_w:
                                new_mt.Height = ht_w / avg_s if avg_s != 0 else ht_w
                        except Exception:
                            pass
                        try:
                            new_mt.Rotation = rot_w - rotation
                        except Exception:
                            pass
                        new_ents_in_block.append(new_mt)
                        success = True

                # ---------- Point ----------
                elif obj_name == "AcDbPoint":
                    bb_min, bb_max = bbox_two_points(ent)
                    if bb_min is None:
                        print("[警告] 无法获取 Point 坐标，跳过")
                    else:
                        px = (bb_min[0] + bb_max[0]) / 2.0
                        py = (bb_min[1] + bb_max[1]) / 2.0
                        pz = (bb_min[2] + bb_max[2]) / 2.0
                        pt_b = world_to_block((px, py, pz))
                        v_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(pt_b))
                        new_pt = block_def.AddPoint(v_pt)
                        new_ents_in_block.append(new_pt)
                        success = True

                else:
                    print(f"[提示] 暂不支持加入块的实体类型: {obj_name}，已跳过。")

            except Exception as e:
                print(f"[警告] 处理实体 {obj_name} 失败: {e}")
                success = False

            # ---- 成功加入块后，根据 keep_source 决定是否删除原对象 ----
            if success and not keep_source:
                try:
                    ent.Delete()
                except Exception as e:
                    print(f"[警告] 删除源对象失败: {e}")

        print(f"[成功] 已向块 {block_name} 中添加 {len(new_ents_in_block)} 个新实体，"
              f"{'保留' if keep_source else '删除'}了已成功加入块的源对象。")

        
        # 👉 最后强制重生成，让图形立刻可见
        try:
            doc.SendCommand("_.REGEN\n")  # 或者 "RE\n"
        except Exception:
            pass

        return new_ents_in_block

    except Exception as e:
        print(f"[错误] add_entities_to_block_keep_world 整体失败: {e}")
        return []

##quchulai
def extract_nonblock_entities_from_block(block_ref, keep_in_block: bool = False):
    """
    【函数X】将指定块中的“非块对象”按当前显示位置取出到模型空间

    特点：
      - 只处理块定义内部的非 AcDbBlockReference 实体；
      - 块内嵌套块（AcDbBlockReference）完全不动（不删除、不复制出来）；
      - 新建的几何落在模型空间，位置和块显示效果一致；
      - keep_in_block=False（默认）：成功取出的那些实体会从块定义中删除；
        keep_in_block=True：块内保留它们，只是外面多一份展开几何。

    参数:
        block_ref     : IAcadBlockReference 块参照对象
        keep_in_block : 是否保留块内原实体（非块部分）
                        False → 取出后删除块内对应实体
                        True  → 取出后块内也保留

    返回:
        world_entities : 在模型空间中新建的实体列表
    """
    import win32com.client
    import pythoncom
    import math
    from win32com.client import VARIANT

    world_entities = []

    try:
        # 更稳一点：从 block_ref.Document 拿 doc
        try:
            doc = block_ref.Document
        except Exception:
            acad = win32com.client.Dispatch("AutoCAD.Application")
            doc = acad.ActiveDocument

        ms = doc.ModelSpace

        # ---- 1. 获取块定义 ----
        try:
            block_name = block_ref.EffectiveName
            block_def = doc.Blocks.Item(block_name)
        except Exception:
            block_name = block_ref.Name
            block_def = doc.Blocks.Item(block_name)

        print(f"[信息] 源块: {block_name}")
        origin = block_def.Origin  # 块定义原点 (Ox, Oy, Oz)

        # 块定义中的所有对象
        block_entities = [ent for ent in block_def]
        if not block_entities:
            print("[警告] 块定义中没有任何对象。")
            return []

        # ---- 2. 块参照的变换信息（局部 → 世界）----
        ins_pt   = block_ref.InsertionPoint   # 插入点
        sx       = block_ref.XScaleFactor or 1.0
        sy       = block_ref.YScaleFactor or 1.0
        sz       = block_ref.ZScaleFactor or 1.0
        rotation = block_ref.Rotation or 0.0  # 弧度

        ox, oy, oz = origin
        ix, iy, iz = ins_pt

        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)

        if abs(sx) < 1e-9: sx = 1.0
        if abs(sy) < 1e-9: sy = 1.0
        if abs(sz) < 1e-9: sz = 1.0

        # ---- 3. 块局部坐标 → 世界坐标 ----
        def block_to_world(pt):
            """
            给定块局部坐标 Pb = (xb, yb, zb)，求世界坐标 Pw：

              Pw = InsertPoint + R * S * (Pb - Origin)
            """
            xb, yb, zb = pt

            # 相对块原点
            vx = xb - ox
            vy = yb - oy
            vz = zb - oz

            # 缩放
            vx *= sx
            vy *= sy
            vz *= sz

            # 旋转（绕 Z）
            x1 = cos_r * vx - sin_r * vy
            y1 = sin_r * vx + cos_r * vy
            z1 = vz

            # 平移到插入点
            xw = ix + x1
            yw = iy + y1
            zw = iz + z1
            return (xw, yw, zw)

        # ---- 4. 小工具：GetBoundingBox ----
        def bbox_two_points(e):
            try:
                bb_min, bb_max = e.GetBoundingBox()
                return bb_min, bb_max
            except Exception as ex:
                print(f"[警告] GetBoundingBox 失败: {ex}")
                return None, None

        # ---- 5. 遍历块内“非块对象”，生成世界空间几何 ----
        for ent in list(block_entities):
            try:
                obj_name = com_retry(lambda: ent.ObjectName)
            except Exception as e:
                print(f"[警告] 获取块内实体类型失败: {e}")
                continue

            # 块内块：完全不动，也不取出
            if obj_name == "AcDbBlockReference":
                # 块内的嵌套块保持原样
                continue

            created = False  # 当前实体是否成功生成世界实体

            try:
                # ---------- Line ----------
                if obj_name == "AcDbLine":
                    sp = get_object_property(ent, "StartPoint")
                    ep = get_object_property(ent, "EndPoint")
                    if sp is None or ep is None:
                        sp, ep = bbox_two_points(ent)
                        if sp is None or ep is None:
                            print("[警告] 无法获取 Line 局部端点，跳过")
                        else:
                            sp_w = block_to_world(sp)
                            ep_w = block_to_world(ep)
                            v_sp = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(sp_w))
                            v_ep = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(ep_w))
                            new_ent = ms.AddLine(v_sp, v_ep)
                            world_entities.append(new_ent)
                            created = True
                    else:
                        sp_w = block_to_world(sp)
                        ep_w = block_to_world(ep)
                        v_sp = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(sp_w))
                        v_ep = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(ep_w))
                        new_ent = ms.AddLine(v_sp, v_ep)
                        world_entities.append(new_ent)
                        created = True

                # ---------- Circle ----------
                elif obj_name == "AcDbCircle":
                    center_b = get_object_property(ent, "Center")
                    radius_b = get_object_property(ent, "Radius")
                    if center_b is None or radius_b is None:
                        print("[警告] 无法获取 Circle 局部属性，跳过")
                    else:
                        cen_w = block_to_world(center_b)
                        avg_s = (sx + sy) / 2.0
                        radius_w = radius_b * avg_s
                        v_cen = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(cen_w))
                        new_ent = ms.AddCircle(v_cen, radius_w)
                        world_entities.append(new_ent)
                        created = True

                # ---------- Arc ----------
                elif obj_name == "AcDbArc":
                    center_b = get_object_property(ent, "Center")
                    radius_b = get_object_property(ent, "Radius")
                    sa_b = get_object_property(ent, "StartAngle")
                    ea_b = get_object_property(ent, "EndAngle")
                    if None in (center_b, radius_b, sa_b, ea_b):
                        print("[警告] 无法获取 Arc 局部属性，跳过")
                    else:
                        cen_w = block_to_world(center_b)
                        avg_s = (sx + sy) / 2.0
                        radius_w = radius_b * avg_s
                        # 角度加上块的整体旋转（假定等比缩放）
                        v_cen = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(cen_w))
                        new_ent = ms.AddArc(v_cen, radius_w, sa_b + rotation, ea_b + rotation)
                        world_entities.append(new_ent)
                        created = True

                # ---------- Polyline / 2d/3d / LW ----------
                elif obj_name in ("AcDbPolyline", "AcDb2dPolyline",
                                  "AcDb3dPolyline", "AcDbLWPolyline"):
                    coords = get_object_property(ent, "Coordinates")
                    if coords is None:
                        print("[警告] 无法获取多段线局部坐标，跳过")
                    else:
                        coords = list(coords)
                        new_coords = []
                        for i in range(0, len(coords), 3):
                            pt_b = (coords[i], coords[i+1], coords[i+2])
                            pw = block_to_world(pt_b)
                            new_coords.extend(pw)
                        v_pts = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, new_coords)
                        new_ent = ms.AddPolyline(v_pts)
                        world_entities.append(new_ent)
                        created = True

                # ---------- Text ----------
                elif obj_name == "AcDbText":
                    ins_b = get_object_property(ent, "InsertionPoint")
                    txt = get_object_property(ent, "TextString")
                    h_b = get_object_property(ent, "Height")
                    if ins_b is None or txt is None or h_b is None:
                        print("[警告] 无法获取 Text 局部属性，跳过")
                    else:
                        ins_w = block_to_world(ins_b)
                        avg_s = (sx + sy) / 2.0
                        h_w = h_b * avg_s
                        v_ins = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(ins_w))
                        new_txt = ms.AddText(txt, v_ins, h_w)
                        rot_b = get_object_property(ent, "Rotation") or 0.0
                        try:
                            new_txt.Rotation = rot_b + rotation
                        except Exception:
                            pass
                        world_entities.append(new_txt)
                        created = True

                # ---------- MText ----------
                elif obj_name == "AcDbMText":
                    ins_b   = get_object_property(ent, "InsertionPoint")
                    width_b = get_object_property(ent, "Width")
                    contents = get_object_property(ent, "Contents")
                    if ins_b is None or width_b is None or contents is None:
                        print("[警告] 无法获取 MText 局部属性，跳过")
                    else:
                        ins_w = block_to_world(ins_b)
                        avg_s = (sx + sy) / 2.0
                        width_w = width_b * avg_s
                        v_ins = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(ins_w))
                        new_mt = ms.AddMText(v_ins, width_w, contents)
                        ht_b = get_object_property(ent, "TextHeight")
                        rot_b = get_object_property(ent, "Rotation") or 0.0
                        try:
                            if ht_b:
                                new_mt.Height = ht_b * avg_s
                        except Exception:
                            pass
                        try:
                            new_mt.Rotation = rot_b + rotation
                        except Exception:
                            pass
                        world_entities.append(new_mt)
                        created = True

                # ---------- Point ----------
                elif obj_name == "AcDbPoint":
                    bb_min, bb_max = bbox_two_points(ent)
                    if bb_min is None:
                        print("[警告] 无法获取 Point 局部坐标，跳过")
                    else:
                        px = (bb_min[0] + bb_max[0]) / 2.0
                        py = (bb_min[1] + bb_max[1]) / 2.0
                        pz = (bb_min[2] + bb_max[2]) / 2.0
                        pw = block_to_world((px, py, pz))
                        v_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(pw))
                        new_pt = ms.AddPoint(v_pt)
                        world_entities.append(new_pt)
                        created = True

                else:
                    print(f"[提示] 暂不支持从块中取出的实体类型: {obj_name}，已跳过。")

            except Exception as e:
                print(f"[警告] 处理块内实体 {obj_name} 失败: {e}")
                created = False

            # 如果成功生成世界实体，且不保留块内版本，则删除块内原对象
            if created and (not keep_in_block):
                try:
                    ent.Delete()
                except Exception as e:
                    print(f"[警告] 删除块内原实体失败: {e}")

        print(f"[成功] 已从块 {block_name} 中取出 {len(world_entities)} 个“非块对象”到模型空间，"
              f"块内嵌套块保持不动，"
              f"{'保留' if keep_in_block else '删除'}对应的块内实体。")

        # 强制 REGEN，让结果立刻可见
        try:
            doc.SendCommand("_.REGEN\n")
        except Exception:
            pass

        return world_entities

    except Exception as e:
        print(f"[错误] extract_nonblock_entities_from_block 整体失败: {e}")
        return []


#bianhuan
def remap_block_contents_between_rects(
    block_ref,
    rectA,
    rectB,
    anchor_corner: str = "右上",
    target_point: tuple | None = None,
    only_text: bool = False,
):
    """
    【函数X】块内部“重排”：把块内容从外包盒 A 的布局映射到 B 的布局

    要求：
      - 不改 BlockReference 的 Scale/Rotation；
      - 块内对象不缩放，只整体平移；
      - 文本大小、内容等属性保持不变，只位置改变；
      - 其它对象（线/多段线/点/块参照等）形状尺寸不变，只按外包盒中心平移；
      - 块内“最大外包盒”从矩形 A 的布局映射到矩形 B 的布局。

    参数:
        block_ref    : IAcadBlockReference，目标块实例
        rectA        : 模型空间中表示“当前布局范围”的矩形多段线对象
        rectB        : 模型空间中表示“目标布局范围”的矩形多段线对象
        anchor_corner: 锚点角 "左下"/"右下"/"左上"/"右上"
                       - 用于对齐 B 的角点位置
        target_point : 可选 (x,y) 或 (x,y,z)
                       - None: 默认让 B 的该角点对齐 A 的同名角点
                       - 非 None: 让 B 的该角点对齐 target_point
        only_text    : True  只移动文字类对象 (AcDbText/AcDbMText)
                       False 移动块内所有实体（包括线、多段线、点、块参照等）

    返回:
        True / False 是否成功
    """
    import win32com.client
    import pythoncom
    import math
    from win32com.client import VARIANT

    # ---------- 0. 文档 ----------
    try:
        doc = block_ref.Document
    except Exception:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument

    # ---------- 1. A/B 外包盒 ----------
    bboxA = group_bbox_corners([rectA])
    bboxB = group_bbox_corners([rectB])
    if bboxA is None or bboxB is None:
        print("[错误] 无法计算 A/B 外包盒。")
        return False

    A_bottom_left, A_top_right, A_top_left, A_bottom_right = bboxA
    B_bottom_left, B_top_right, B_top_left, B_bottom_right = bboxB

    Ax_min, Ay_min, _ = A_bottom_left
    Ax_max, Ay_max, _ = A_top_right

    Bx_min0, By_min0, _ = B_bottom_left
    Bx_max0, By_max0, _ = B_top_right

    if Ax_max == Ax_min or Ay_max == Ay_min:
        print("[错误] A 外包盒宽或高为 0。")
        return False

    # 选锚点角
    corner_map_A = {
        "左下": A_bottom_left,
        "右上": A_top_right,
        "左上": A_top_left,
        "右下": A_bottom_right,
    }
    corner_map_B = {
        "左下": B_bottom_left,
        "右上": B_top_right,
        "左上": B_top_left,
        "右下": B_bottom_right,
    }
    if anchor_corner not in corner_map_A:
        print(f"[警告] 未知锚点角 '{anchor_corner}'，改用 '右上'")
        anchor_corner = "右上"

    A_anchor = corner_map_A[anchor_corner]
    B_anchor = corner_map_B[anchor_corner]

    # 目标对齐点
    if target_point is None:
        # 默认：B 的该角点对齐到 A 的同名角点
        target_world = A_anchor
    else:
        if len(target_point) == 2:
            target_world = (target_point[0], target_point[1], A_anchor[2])
        else:
            target_world = tuple(target_point[:3])

    # 计算 B 的平移，使得 B_anchor → target_world
    dx_B = target_world[0] - B_anchor[0]
    dy_B = target_world[1] - B_anchor[1]

    # 平移后的 B 外包盒
    Bx_min = Bx_min0 + dx_B
    By_min = By_min0 + dy_B
    Bx_max = Bx_max0 + dx_B
    By_max = By_max0 + dy_B

    print(f"[信息] A 外包盒: x=({Ax_min},{Ax_max}), y=({Ay_min},{Ay_max})")
    print(f"[信息] B 外包盒(平移后): x=({Bx_min},{Bx_max}), y=({By_min},{By_max})")

    # ---------- 2. 块定义 & 变换信息 ----------
    try:
        block_name = block_ref.EffectiveName
        block_def = doc.Blocks.Item(block_name)
    except Exception:
        block_name = block_ref.Name
        block_def = doc.Blocks.Item(block_name)
    origin = block_def.Origin
    Ox, Oy, Oz = origin

    I = block_ref.InsertionPoint
    Ix, Iy, Iz = I

    sx = block_ref.XScaleFactor or 1.0
    sy = block_ref.YScaleFactor or 1.0
    sz = block_ref.ZScaleFactor or 1.0

    if abs(sx) < 1e-9 or abs(sy) < 1e-9:
        print("[错误] 块缩放为 0，无法计算。")
        return False

    rot = block_ref.Rotation or 0.0
    cos_r = math.cos(rot)
    sin_r = math.sin(rot)

    # 局部 -> 世界
    def block_to_world(pt_b):
        xb, yb, zb = pt_b
        # 相对块原点
        vx = xb - Ox
        vy = yb - Oy
        vz = zb - Oz
        # 缩放
        vx *= sx
        vy *= sy
        vz *= sz
        # 旋转
        x1 = cos_r * vx - sin_r * vy
        y1 = sin_r * vx + cos_r * vy
        z1 = vz
        # 平移到插入点
        return (Ix + x1, Iy + y1, Iz + z1)

    # 世界向量 -> 块局部向量
    def world_vec_to_block_vec(dwx, dwy, dwz):
        """
        Δw = R * S * Δb  =>  Δb = S^-1 * R^T * Δw
        """
        # 先逆旋转（乘 R^T）
        # R = [[c,-s],[s,c]]，R^T = [[c,s],[-s,c]]
        vx = cos_r * dwx + sin_r * dwy
        vy = -sin_r * dwx + cos_r * dwy
        vz = dwz
        # 再逆缩放
        bx = vx / sx
        by = vy / sy
        bz = vz / sz if abs(sz) > 1e-9 else vz
        return (bx, by, bz)

    # ---------- 3. 遍历块内实体，按“外包盒中心”重排 ----------
    moved_count = 0
    skipped_count = 0

    for ent in block_def:
        try:
            obj_name = com_retry(lambda: ent.ObjectName)
        except Exception as e:
            print(f"[警告] 获取块内实体类型失败: {e}")
            skipped_count += 1
            continue

        # 只移动文字？
        if only_text and obj_name not in ("AcDbText", "AcDbMText"):
            continue

        # 如果完全不想动块内块，也可以在这里跳过 AcDbBlockReference
        # 现在的逻辑：块内块也按“外包盒中心”移动整体位置，大小不变
        # 如需块内块不动，可以改成：
        # if obj_name == "AcDbBlockReference":
        #     continue

        # 取局部外包盒中心
        try:
            bb_min, bb_max = ent.GetBoundingBox()
        except Exception as e:
            print(f"[警告] GetBoundingBox 失败: {e}")
            skipped_count += 1
            continue

        cx_b = (bb_min[0] + bb_max[0]) / 2.0
        cy_b = (bb_min[1] + bb_max[1]) / 2.0
        cz_b = (bb_min[2] + bb_max[2]) / 2.0
        center_b = (cx_b, cy_b, cz_b)

        # 当前世界中心
        cx_w, cy_w, cz_w = block_to_world(center_b)

        # ---- A → B 的“布局映射”（只改 center，不改大小）----
        tx = (cx_w - Ax_min) / (Ax_max - Ax_min)
        ty = (cy_w - Ay_min) / (Ay_max - Ay_min)

        new_cx_w = Bx_min + tx * (Bx_max - Bx_min)
        new_cy_w = By_min + ty * (By_max - By_min)
        new_cz_w = cz_w  # Z 不变

        dx_w = new_cx_w - cx_w
        dy_w = new_cy_w - cy_w
        dz_w = new_cz_w - cz_w

        # 转成块局部平移向量 Δb
        dx_b, dy_b, dz_b = world_vec_to_block_vec(dx_w, dy_w, dz_w)

        # Move：在块定义坐标系下平移实体
        try:
            from_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
            to_pt   = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [dx_b, dy_b, dz_b])
            ent.Move(from_pt, to_pt)
            moved_count += 1
        except Exception as e:
            print(f"[警告] 移动块内实体 {obj_name} 失败: {e}")
            skipped_count += 1

    print(f"[结果] 已移动 {moved_count} 个块内实体，跳过 {skipped_count} 个实体。")

    # ---------- 4. REGEN 刷新 ----------
    try:
        doc.SendCommand("_.REGEN\n")
    except Exception:
        pass

    return True






def create_attribute_block(
    attributes_dict,
    block_name_prefix="属性块",
    rect_width=6000,
    rect_height=21000
):
    """
    【函数4】创建属性块

    创建包含矩形框和属性文字的块

    参数:
        attributes_dict: 属性字典 {标签名: 默认值, ...}
        block_name_prefix: 块名前缀
        rect_width: 矩形宽度,默认6000
        rect_height: 矩形高度,默认21000

    返回:
        块定义对象
    """
    import win32com.client
    import pythoncom
    from win32com.client import VARIANT

    acad = win32com.client.Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    ms = doc.ModelSpace

    try:
        # 1. 生成唯一块名
        block_name = block_name_prefix + "01"
        counter = 1
        while True:
            try:
                doc.Blocks.Item(block_name)
                counter += 1
                block_name = f"{block_name_prefix}{counter:02d}"
            except:
                break

        print(f"[信息] 创建属性块: {block_name}")

        # 2. 创建块定义
        base_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0, 0, 0])
        block_def = doc.Blocks.Add(base_pt, block_name)

        # 3. 添加矩形多段线（必须使用3D坐标：x, y, z）
        rect_pts = [
            0, 0, 0,
            rect_width, 0, 0,
            rect_width, rect_height, 0,
            0, rect_height, 0,
            0, 0, 0  # 闭合
        ]
        rect_coords = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, rect_pts)
        pline = block_def.AddPolyline(rect_coords)
        pline.Closed = True

        print(f"[信息] 已添加矩形: {rect_width} x {rect_height}")

        # 4. 添加属性定义 - 修复：使用位置参数而不是关键字参数
        attr_count = len(attributes_dict)
        if attr_count > 0:
            y_spacing = rect_height / (attr_count + 1)

            for i, (tag, default_value) in enumerate(attributes_dict.items(), 1):
                y_pos = rect_height - i * y_spacing
                attr_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [rect_width/2, y_pos, 0])

                # 添加属性定义 - 使用位置参数
                # AddAttribute(Height, Mode, Prompt, InsertionPoint, Tag, Value)
                attr_def = block_def.AddAttribute(
                    300,                  # Height - 字高
                    0,                    # Mode - 普通模式
                    tag,                  # Prompt - 提示
                    attr_pt,              # InsertionPoint - 插入点
                    tag,                  # Tag - 标签
                    str(default_value)    # Value - 默认值
                )
                attr_def.Alignment = 10  # 中心对齐

                # 修复：设置对齐方式后，需要重新设置对齐点位置
                # 当Alignment不是左对齐(0)时，必须设置TextAlignmentPoint
                align_pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [rect_width/2, y_pos, 0])
                attr_def.TextAlignmentPoint = align_pt

                print(f"[信息] 已添加属性: {tag} = {default_value} at y={y_pos}")

        print(f"[成功] 属性块 '{block_name}' 创建完成")
        return block_def

    except Exception as e:
        print(f"[错误] 创建属性块失败: {e}")
        import traceback
        traceback.print_exc()
        return None


















































































