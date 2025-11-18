#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 GetBoundingBox 的返回值结构
"""

import sys
import io
from pathlib import Path

# 设置 UTF-8 编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加 scripts 目录
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from CAD_basic import li, stc, com_retry
from CAD_file_operations import open_file
from CAD_enhanced_functions import start_cad_session_with_coordination

print("="*60)
print("测试 GetBoundingBox 返回值结构")
print("="*60)

# 1. 启动 CAD
print("\n🚀 步骤 1: 启动 CAD...")
start_cad_session_with_coordination()
print("✅ CAD 已启动并就绪")

# 2. 打开测试文件
print("\n📂 步骤 2: 打开测试文件...")
file_path = "D:/claude-tasks/tests/test_files/天正测试文件2-1.dwg"
open_file(file_path)

# 3. 选择对象
print("\n🔍 步骤 3: 选择 WINDOW 对象...")
lb = stc("WINDOW")
print(f"✅ 选中 {len(lb)} 个对象")

if len(lb) > 0:
    obj = lb[0]
    print(f"\n📊 测试对象: {obj.ObjectName}")

    # 方法1: 直接调用 GetBoundingBox
    print("\n方法1: 直接调用 GetBoundingBox()")
    try:
        result = obj.GetBoundingBox()
        print(f"  返回值类型: {type(result)}")
        print(f"  返回值: {result}")
        if isinstance(result, (tuple, list)):
            print(f"  返回值长度: {len(result)}")
            for i, item in enumerate(result):
                print(f"  [{i}] 类型={type(item)}, 值={item}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()

    # 方法2: 使用 com_retry
    print("\n方法2: 使用 com_retry")
    try:
        result = com_retry(lambda: obj.GetBoundingBox())
        print(f"  返回值类型: {type(result)}")
        print(f"  返回值: {result}")
        if isinstance(result, (tuple, list)):
            print(f"  返回值长度: {len(result)}")
            for i, item in enumerate(result):
                print(f"  [{i}] 类型={type(item)}, 值={item}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()

    # 方法3: 使用 output 参数方式
    print("\n方法3: 尝试 output 参数方式")
    try:
        import win32com.client
        import pythoncom

        minpt = win32com.client.VARIANT(pythoncom.VT_VARIANT | pythoncom.VT_BYREF, [0,0,0])
        maxpt = win32com.client.VARIANT(pythoncom.VT_VARIANT | pythoncom.VT_BYREF, [0,0,0])
        obj.GetBoundingBox(minpt, maxpt)

        p1 = minpt.value
        p2 = maxpt.value

        print(f"  MinPoint: {p1}")
        print(f"  MaxPoint: {p2}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*60)
print("测试完成")
print("="*60)

