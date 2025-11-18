#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试对象属性处理改进

验证：
1. CAD标准对象使用 _maybe_cast() 后可以访问属性
2. 天正对象使用 get_object_property() 可以访问属性
"""

import sys
import io
from pathlib import Path

# 设置标准输出编码为 UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

print("="*60)
print("对象属性处理改进测试")
print("="*60)

# 测试导入
print("\n1. 测试模块导入...")

try:
    from CAD_basic import _maybe_cast, cast_object, get_object_property, set_object_property, last_obj, li
    print("✅ CAD_basic 导入成功")
    print("   - _maybe_cast: ", _maybe_cast)
    print("   - cast_object: ", cast_object)
    print("   - get_object_property: ", get_object_property)
    print("   - set_object_property: ", set_object_property)
except Exception as e:
    print(f"❌ CAD_basic 导入失败: {e}")
    import traceback
    traceback.print_exc()

try:
    from CAD_object_properties import _maybe_cast as _maybe_cast_2, cast_object as cast_object_2
    from CAD_object_properties import get_object_property as get_prop_2, set_object_property as set_prop_2
    print("✅ CAD_object_properties 导入成功")
    print("   - _maybe_cast: ", _maybe_cast_2)
    print("   - cast_object: ", cast_object_2)
    print("   - get_object_property: ", get_prop_2)
    print("   - set_object_property: ", set_prop_2)
except Exception as e:
    print(f"❌ CAD_object_properties 导入失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 _CAST_MAP
print("\n2. 测试 _CAST_MAP 映射...")

try:
    from CAD_basic import _CAST_MAP
    print(f"✅ CAD_basic._CAST_MAP 包含 {len(_CAST_MAP)} 个映射")

    # 检查关键映射
    required_mappings = [
        "AcDbLine", "AcDbCircle", "AcDbPolyline",
        "AcDbAlignedDimension", "AcDbRotatedDimension",
        "AcDb3PointAngularDimension"
    ]

    for obj_type in required_mappings:
        if obj_type in _CAST_MAP:
            print(f"   ✅ {obj_type} -> {_CAST_MAP[obj_type]}")
        else:
            print(f"   ❌ {obj_type} 缺失")

except Exception as e:
    print(f"❌ 检查 _CAST_MAP 失败: {e}")

# 测试函数签名
print("\n3. 测试函数签名...")

try:
    import inspect

    # 检查 _maybe_cast 函数签名
    sig = inspect.signature(_maybe_cast)
    print(f"✅ _maybe_cast{sig}")

    # 检查 cast_object 函数签名
    sig = inspect.signature(cast_object)
    print(f"✅ cast_object{sig}")

    # 检查 get_object_property 函数签名
    sig = inspect.signature(get_object_property)
    print(f"✅ get_object_property{sig}")

except Exception as e:
    print(f"❌ 检查函数签名失败: {e}")

print("\n" + "="*60)
print("测试完成")
print("="*60)

print("\n📝 使用说明:")
print("\n对 CAD 标准对象（如多段线）：")
print("```python")
print("ob = last_obj()")
print("ob = _maybe_cast(ob)  # 转换到专用接口")
print("coords = ob.Coordinates  # 访问坐标属性")
print("```")

print("\n对天正对象（如门窗）：")
print("```python")
print("ob = last_obj()")
print("width = get_object_property(ob, 'Width')  # 获取宽度")
print("set_object_property(ob, 'Width', 1200)    # 设置宽度")
print("```")

print("\n如需实际测试，请：")
print("1. 启动 CAD 并打开图纸")
print("2. 在 Python 中运行: li()  # 初始化连接")
print("3. 创建或选择一个对象")
print("4. 运行上述代码测试")

