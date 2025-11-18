# -*- coding: utf-8 -*-
"""
CAD增强功能模块

提供集成了协同机制的CAD操作函数,作为CAD-basic.py的补充
"""

import os
import time
from pathlib import Path

# 导入协同机制
from CAD_coordination import (
    wait_quiescent,
    wait_document_opened,
    send_cmd_with_sync,
    start_cad_with_dialog_killer,
    ensure_single_process
)

def open_dwg_enhanced(path: str, visible: bool = True):
    """
    增强版DWG文件打开函数,集成了协同机制

    Args:
        path: DWG文件路径
        visible: 是否显示CAD界面

    Returns:
        tuple: (acad, doc) 成功时返回CAD应用和文档对象,失败时返回(None, None)
    """
    try:
        # 确保单进程状态
        ensure_single_process()

        # 初始化COM
        import pythoncom
        from win32com.client import Dispatch
        pythoncom.CoInitialize()

        # 连接到AutoCAD应用
        acad = Dispatch("AutoCAD.Application")
        acad.Visible = visible

        print(f"🔄 正在打开文件: {path}")

        # 打开DWG文档
        doc = acad.Documents.Open(path)

        # 等待文档完全加载
        if wait_document_opened(path, timeout=120.0):
            print(f"✅ 文件已成功打开: {doc.Name}")

            # 等待CAD进入空闲状态
            wait_quiescent(min_quiet=0.5, timeout=30.0)

            return acad, doc
        else:
            print(f"❌ 文件打开失败或超时: {path}")
            return None, None

    except Exception as e:
        print(f"❌ 打开DWG文件时出错: {e}")
        return None, None

def open_dwg_sync(path: str, visible: bool = True) -> bool:
    """
    同步版本的DWG打开函数,专注于协同控制

    Args:
        path: DWG文件路径
        visible: 是否显示CAD界面

    Returns:
        bool: True表示成功,False表示失败
    """
    try:
        # 启动CAD和弹窗治理(如果尚未启动)
        if not start_cad_with_dialog_killer():
            print("❌ CAD启动失败")
            return False

        # 确保单进程
        ensure_single_process()

        # 基础等待
        time.sleep(1.0)

        # 打开文件
        acad, doc = open_dwg_enhanced(path, visible)

        if acad and doc:
            print(f"🎯 文件操作完成: {path}")
            return True
        else:
            print(f"❌ 文件操作失败: {path}")
            return False

    except Exception as e:
        print(f"❌ 同步打开DWG时出错: {e}")
        return False

def start_cad_session_with_coordination() -> bool:
    """
    启动完整的CAD会话,包含所有协同机制

    Returns:
        bool: True表示启动成功,False表示失败
    """
    try:
        print("🚀 正在启动CAD会话,启用完整协同机制...")

        # 1. 启动CAD和弹窗治理
        if not start_cad_with_dialog_killer():
            return False

        # 2. 确保单进程
        ensure_single_process()

        # 3. 等待CAD完全启动
        time.sleep(2.0)

        # 4. 等待CAD进入空闲状态
        if wait_quiescent(min_quiet=1.0, timeout=60.0):
            print("✅ CAD会话启动完成,协同机制已激活")
            return True
        else:
            print("⚠ CAD启动完成但未进入空闲状态")
            return True  # 仍然认为启动成功

    except Exception as e:
        print(f"❌ 启动CAD会话时出错: {e}")
        return False

def test_cad_coordination() -> bool:
    """
    测试CAD协同机制是否正常工作

    Returns:
        bool: True表示测试通过,False表示测试失败
    """
    try:
        print("🧪 开始测试CAD协同机制...")

        # 测试1: 启动CAD会话
        print("\n1. 测试启动CAD会话:")
        if not start_cad_session_with_coordination():
            print("❌ CAD会话启动失败")
            return False

        # 测试2: 发送同步命令
        print("\n2. 测试同步命令发送:")
        if send_cmd_with_sync("_.LINE\n0,0\n100,100\n", wait_after=1.0):
            print("✅ 同步命令发送成功")
        else:
            print("❌ 同步命令发送失败")
            return False

        # 测试3: 等待空闲
        print("\n3. 测试等待CAD空闲:")
        if wait_quiescent(min_quiet=0.5, timeout=15.0):
            print("✅ CAD空闲检测正常")
        else:
            print("❌ CAD空闲检测异常")
            return False

        print("\n✅ CAD协同机制测试全部通过")
        return True

    except Exception as e:
        print(f"❌ CAD协同机制测试失败: {e}")
        return False

if __name__ == "__main__":
    # 运行测试
    test_cad_coordination()
