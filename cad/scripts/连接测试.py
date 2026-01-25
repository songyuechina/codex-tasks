Python 3.11.5 (tags/v3.11.5:cce6ba9, Aug 24 2023, 14:38:34) [MSC v.1936 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.

= RESTART: D:/claude-tasks/cad/scripts/测试.py

================== RESTART: D:/claude-tasks/cad/scripts/测试.py ==================
==================================================
   实验 A：强制晚期绑定 (Late Binding)
   模拟场景：没有生成 makepy 缓存，或使用 dynamic.Dispatch
==================================================
测试出错: (-2147352567, '发生意外。', (0, None, None, None, 0, -2147024809), None)

================== RESTART: D:/claude-tasks/cad/scripts/测试.py ==================
==================================================
   实验 A：强制晚期绑定 (Late Binding)
==================================================
[结果] App对象类型: <COMObject AutoCAD.Application>
      (看到 COMObject 说明目前是“盲人模式”)
[结果] 画线成功，对象为: <win32com.gen_py.AutoCAD 2021 Type Library.IAcadLine instance at 0x2125134816784>
[验证] dir() 里有 StartPoint 吗? -> True

==================================================
   实验 B：早期绑定 (Early Binding) + 接口退化
==================================================
[结果] Item() 返回的对象: <win32com.gen_py.AutoCAD 2021 Type Library.IAcadEntity instance at 0x2125126206352>
      (注意看是不是 IAcadEntity，而不是 IAcadLine)
[验证] 直接访问 StartPoint? -> 不能 (退化了)
[修复] CastTo 之后: <win32com.gen_py.AutoCAD 2021 Type Library.IAcadLine instance at 0x2125134816592>
[修复] 属性回来了吗? -> True
doc.Name
Traceback (most recent call last):
  File "<pyshell#0>", line 1, in <module>
    doc.Name
NameError: name 'doc' is not defined
import win32com.client.dynamic
import win32com.client
def force_blind_mode(obj):
    """
    【强制致盲函数】
    剥离对象的类型包装，将其还原为原始的 COMObject 盲盒状态。
    原理：取出底层的 _oleobj_ 指针，强制用动态 CDispatch 包装，不带任何类型库信息。
    """
    if obj is None: return None
    try:
        # CDispatch 是 win32com 内部表示 "COMObject" 的类
        # 传入 None 作为 typeinfo，强制它变成“瞎子”
        return win32com.client.dynamic.CDispatch(obj._oleobj_, None)
    except Exception as e:
        print(f"转换失败: {e}")
        return obj

    
def show_me_the_com():
    print("=" * 60)
    print("   终极实验：强行剥离类型信息")
    print("=" * 60)

    # 1. 正常连接 (此时可能是强类型，也可能是弱类型，取决于你之前的操作)
    # 我们故意用 Dispatch，但也无所谓，下面我们会强制转换
    raw_app = win32com.client.Dispatch("AutoCAD.Application")
    
    # 2. 随便画条线 (或者获取一条线)
    doc = raw_app.ActiveDocument
    msp = doc.ModelSpace
    
    # 获取最后一条实体（假设你图纸里有东西）
    if msp.Count == 0:
        print("请在 CAD 里随便画一条线再运行此脚本！")
        return

    item = msp.Item(msp.Count - 1)
    
    print(f"[原始状态] Python 自动识别为:\n -> {item}")
    
    # 3. 【见证奇迹的时刻】强制致盲
    blind_item = force_blind_mode(item)
    
    print("\n[致盲状态] 强制剥离缓存后 (这就是晚期绑定的真面目):\n ->", end=" ")
    print(blind_item)
    
    print("\n" + "-" * 30)
    print("对比验证 (StartPoint 属性):")
    
    # 验证原始对象 (如果有缓存，dir 里应该有 StartPoint)
    has_attr_orig = "StartPoint" in dir(item)
    print(f"1. 原始对象有 StartPoint 吗?  : {has_attr_orig}")
    
    # 验证致盲对象 (变成 COMObject 后，dir() 应该啥都看不见)
    # 注意：COMObject 依然可以调用属性，但 dir() 这种“查户口”的命令会失效
    has_attr_blind = "StartPoint" in dir(blind_item)
    print(f"2. 致盲对象有 StartPoint 吗?  : {has_attr_blind} (预期为 False)")
    
    print("-" * 30)
    print("虽然 dir() 看不到，但盲猜属性依然可用 (如果有的话):")
    try:
        print(f"盲猜 Handle: {blind_item.Handle}")
    except:
...         print("读取失败")
... 
...         
>>> show_me_the_com()
============================================================
   终极实验：强行剥离类型信息
============================================================
[原始状态] Python 自动识别为:
 -> <win32com.gen_py.AutoCAD 2021 Type Library.IAcadEntity instance at 0x2125134816592>

[致盲状态] 强制剥离缓存后 (这就是晚期绑定的真面目):
 -> Traceback (most recent call last):
  File "<pyshell#7>", line 1, in <module>
    show_me_the_com()
  File "<pyshell#6>", line 27, in show_me_the_com
    print(blind_item)
  File "C:\Users\User\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32com\client\dynamic.py", line 230, in __str__
    return str(self.__call__())
  File "C:\Users\User\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32com\client\dynamic.py", line 202, in __call__
    if self._olerepr_.defaultDispatchName:
AttributeError: 'NoneType' object has no attribute 'defaultDispatchName'
>>> raw_app = win32com.client.Dispatch("AutoCAD.Application")
doc=aw_app.ActiveDocument
Traceback (most recent call last):
  File "<pyshell#9>", line 1, in <module>
    doc=aw_app.ActiveDocument
NameError: name 'aw_app' is not defined. Did you mean: 'raw_app'?
raw_app = win32com.client.Dispatch("AutoCAD.Application")
doc=aw_app.ActiveDocument
Traceback (most recent call last):
  File "<pyshell#11>", line 1, in <module>
    doc=aw_app.ActiveDocument
NameError: name 'aw_app' is not defined. Did you mean: 'raw_app'?
doc=raw_app.ActiveDocument
doc.Name
'Drawing2.dwg'
msp = doc.ModelSpace
last_ent = msp.Item(msp.Count - 1)
last_ent.ObjectName
'AcDbLine'
dir(last_ent)
['Application', 'ArrayPolar', 'ArrayRectangular', 'CLSID', 'Copy', 'Database', 'Delete', 'Document', 'EntityName', 'EntityTransparency', 'EntityType', 'Erase', 'GetBoundingBox', 'GetExtensionDictionary', 'GetXData', 'Handle', 'HasExtensionDictionary', 'Highlight', 'Hyperlinks', 'IntersectWith', 'Layer', 'Linetype', 'LinetypeScale', 'Lineweight', 'Material', 'Mirror', 'Mirror3D', 'Move', 'ObjectID', 'ObjectName', 'OwnerID', 'PlotStyleName', 'Rotate', 'Rotate3D', 'ScaleEntity', 'SetXData', 'TransformBy', 'TrueColor', 'Update', 'Visible', '_ApplyTypes_', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_get_good_object_', '_get_good_single_object_', '_oleobj_', '_prop_map_get_', '_prop_map_put_', 'coclass_clsid', 'color']
last_ent
<win32com.gen_py.AutoCAD 2021 Type Library.IAcadEntity instance at 0x2125096112208>
last_ent.StartPoint
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    last_ent.StartPoint
  File "C:\Users\User\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32com\client\__init__.py", line 588, in __getattr__
    raise AttributeError(f"'{self!r}' object has no attribute '{attr}'")
AttributeError: '<win32com.gen_py.AutoCAD 2021 Type Library.IAcadEntity instance at 0x2125096112208>' object has no attribute 'StartPoint'
