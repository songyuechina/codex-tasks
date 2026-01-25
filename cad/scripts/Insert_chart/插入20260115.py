Python 3.11.5 (tags/v3.11.5:cce6ba9, Aug 24 2023, 14:38:34) [MSC v.1936 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.

============================================================Script Navigator 监听服务已就绪 (127.0.0.1:65432)

          CAD Automation Scripts - IDLE Shell
============================================================
  状态: 就绪
  功能: 支持 BOM 格式文件，支持相对路径资源加载
============================================================

>>> 

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
2026-01-15 14:20:07 - [INFO] - CAD_coordination.py:51 - ✅ 协同模块已加载 (集成 Licad V2.5+)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
2026-01-15 14:20:07 - [INFO] - common_logger.py:41 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=30s
2026-01-15 14:20:07 - [INFO] - CAD_basic.py:511 - [初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> universal_insert_labels_dispatch(
        layout_name="平面分割图", 
        operate_target="Layout", 
        Select_Config=0,      # ✨ [核心] 0=常规选择, 1=精细选择
        manual_dy_list=None,  
        filepath=None,
        layername="dy_quyu",
        delpan=0,
        debug=False,
        ref_width=None, 
        use_cache=False
    )
2026-01-15 14:21:40 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `universal_insert_labels_dispatch` ...
[licad] 正在尝试连接 CAD COM 接口...

[licad] 连接成功: 图签插入0115.dwg
2026-01-15 14:21:40 - [INFO] - licad.py:370 - [li] 连接已刷新: 图签插入0115.dwg
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:20658 - 🏗️ [Dispatch] 模式: Layout | 布局: 平面分割图 | 策略: 常规模式
2026-01-15 14:21:40 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `smart_select_polylines` ...
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:18916 - 🧠 [SmartCache] ⚡ 模式: 强制重算 (Skip Cache)
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:19003 - 🚀 [统一选择] 目标: Layout | 布局: 平面分割图 | MinSide: 100.0
2026-01-15 14:21:40 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `select_print_areas_paperspace` ...
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:19299 - 🚀 [启动] 图纸空间选择 - 目标布局: 平面分割图
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:9218 - [OK] 当前图层已设置为：dy_zhuanyong
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:9225 - [CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 0 次）
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:19313 - 🧹 [初始化] 已清空图层 dy_zhuanyong
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:19326 - 
🔄 --- 开始第 1 次分析循环 ---
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:5001 - 🚀 [COM安全模式] 启动布局扫描: 平面分割图
2026-01-15 14:21:40 - [INFO] - CAD_basic.py:5011 - 📊 容器内对象总数: 128
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19314 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [-310.9841886581022, 993.1662634268623, -310.9841886581022, 706.1662634268639, 79.01581134189797, 706.1662634268639]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19315 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [162.85949222645453, 993.1662634268623, 162.85949222645453, 706.1662634268639, 552.8594922264547, 706.1662634268639]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19316 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [645.7992503808167, 993.1662634268623, 645.7992503808167, 706.1662634268639, 1035.7992503808168, 706.1662634268639]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19317 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [1144.2819015391676, 993.1662634268623, 1144.2819015391676, 706.1662634268639, 1534.2819015391678, 706.1662634268639]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19318 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [1642.7645526975186, 993.1662634268623, 1642.7645526975186, 706.1662634268639, 2032.7645526975189, 706.1662634268639]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19319 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [2141.24720385587, 993.1662634268623, 2141.24720385587, 706.1662634268639, 2531.24720385587, 706.1662634268639]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931A | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [2639.729855014221, 993.1662634268623, 2639.729855014221, 706.1662634268639, 3029.729855014221, 706.1662634268639]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931B | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [3138.212506172572, 993.1662634268623, 3138.212506172572, 706.1662634268639, 3528.212506172572, 706.1662634268639]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931C | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [3636.695157330923, 993.1662634268623, 3636.695157330923, 706.1662634268639, 4026.695157330923, 706.1662634268639]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19779 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [4736.426538862754, 706.1662634268639, 5023.426538862752, 706.1662634268639, 5023.426538862753, 1096.166263426864]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=287.00, H=390.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1981A | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [14057.032410995656, 5121.049243687463, 98157.03241099566, 5121.049243687463, 98157.03241099566, 64521.04924368746]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=84100.00, H=59400.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19824 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [136722.03241099886, 5121.049243687463, 178722.03241099886, 5121.049243687463, 178722.03241099886, 34821.04924368746]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=42000.00, H=29700.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19825 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [227543.0324109991, 5121.049243687463, 227543.03241099912, 64521.04924368746, 185543.0324109991, 64521.04924368746]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=42000.00, H=59400.00 (阈值 100.0)
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19828 | Type=AcDbPolyline
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [299298.7341388955, 5121.049243687463, 299298.7341388955, 47121.04924368746, 269598.7341388955, 47121.04924368746]...
2026-01-15 14:21:41 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=29700.00, H=42000.00 (阈值 100.0)
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF3D | Type=AcDbPolyline
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [269598.7341388955, 47121.04924368746, 269598.7341388955, 5121.04924368723, 299298.7341388955, 5121.049243687223]...
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=29700.00, H=42000.00 (阈值 100.0)
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF3E | Type=AcDbPolyline
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [270098.7341388955, 44621.04924368746, 270098.7341388955, 5621.04924368723, 298798.7341388955, 5621.049243687223]...
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=28700.00, H=39000.00 (阈值 100.0)
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF51 | Type=AcDbPolyline
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [185543.0324109991, 64521.04924368746, 185543.0324109991, 5121.049243687463, 227543.03241099906, 5121.049243687456]...
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=42000.00, H=59400.00 (阈值 100.0)
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF52 | Type=AcDbPolyline
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [186543.0324109991, 62021.04924368746, 186543.0324109991, 6121.049243687463, 226543.03241099906, 6121.049243687456]...
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=40000.00, H=55900.00 (阈值 100.0)
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF65 | Type=AcDbPolyline
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [136722.03241099886, 5121.049243687463, 178722.0324109991, 5121.049243687463, 178722.0324109991, 34821.04924368746]...
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=42000.00, H=29700.00 (阈值 100.0)
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF66 | Type=AcDbPolyline
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [139222.03241099886, 5621.049243687463, 178222.0324109991, 5621.049243687463, 178222.0324109991, 34321.04924368746]...
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=39000.00, H=28700.00 (阈值 100.0)
2026-01-15 14:21:42 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5099 - 
✅ [扫描结束] 最终找到 20 个矩形
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:19335 - 📍 [步骤1] 几何扫描完成，获得 20 个基础矩形
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:19405 - 📍 [包含过滤] 极大候选数量: 17 个
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:19434 - 📍 [步骤2] 发现伪极大矩形(大套小): 6 个
2026-01-15 14:21:43 - [WARNING] - CAD_basic.py:19440 - 🧹 发现 6 个伪外框，正在移除并重新扫描...
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:19326 - 
🔄 --- 开始第 2 次分析循环 ---
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5001 - 🚀 [COM安全模式] 启动布局扫描: 平面分割图
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5011 - 📊 容器内对象总数: 122
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19314 | Type=AcDbPolyline
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [-310.9841886581022, 993.1662634268623, -310.9841886581022, 706.1662634268639, 79.01581134189797, 706.1662634268639]...
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19315 | Type=AcDbPolyline
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [162.85949222645453, 993.1662634268623, 162.85949222645453, 706.1662634268639, 552.8594922264547, 706.1662634268639]...
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19316 | Type=AcDbPolyline
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [645.7992503808167, 993.1662634268623, 645.7992503808167, 706.1662634268639, 1035.7992503808168, 706.1662634268639]...
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19317 | Type=AcDbPolyline
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [1144.2819015391676, 993.1662634268623, 1144.2819015391676, 706.1662634268639, 1534.2819015391678, 706.1662634268639]...
2026-01-15 14:21:43 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19318 | Type=AcDbPolyline
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [1642.7645526975186, 993.1662634268623, 1642.7645526975186, 706.1662634268639, 2032.7645526975189, 706.1662634268639]...
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19319 | Type=AcDbPolyline
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [2141.24720385587, 993.1662634268623, 2141.24720385587, 706.1662634268639, 2531.24720385587, 706.1662634268639]...
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931A | Type=AcDbPolyline
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [2639.729855014221, 993.1662634268623, 2639.729855014221, 706.1662634268639, 3029.729855014221, 706.1662634268639]...
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931B | Type=AcDbPolyline
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [3138.212506172572, 993.1662634268623, 3138.212506172572, 706.1662634268639, 3528.212506172572, 706.1662634268639]...
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931C | Type=AcDbPolyline
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [3636.695157330923, 993.1662634268623, 3636.695157330923, 706.1662634268639, 4026.695157330923, 706.1662634268639]...
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19779 | Type=AcDbPolyline
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [4736.426538862754, 706.1662634268639, 5023.426538862752, 706.1662634268639, 5023.426538862753, 1096.166263426864]...
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=287.00, H=390.00 (阈值 100.0)
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1981A | Type=AcDbPolyline
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [14057.032410995656, 5121.049243687463, 98157.03241099566, 5121.049243687463, 98157.03241099566, 64521.04924368746]...
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=84100.00, H=59400.00 (阈值 100.0)
2026-01-15 14:21:44 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF3E | Type=AcDbPolyline
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [270098.7341388955, 44621.04924368746, 270098.7341388955, 5621.04924368723, 298798.7341388955, 5621.049243687223]...
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=28700.00, H=39000.00 (阈值 100.0)
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF52 | Type=AcDbPolyline
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [186543.0324109991, 62021.04924368746, 186543.0324109991, 6121.049243687463, 226543.03241099906, 6121.049243687456]...
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=40000.00, H=55900.00 (阈值 100.0)
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF66 | Type=AcDbPolyline
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [139222.03241099886, 5621.049243687463, 178222.0324109991, 5621.049243687463, 178222.0324109991, 34321.04924368746]...
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=39000.00, H=28700.00 (阈值 100.0)
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:5099 - 
✅ [扫描结束] 最终找到 14 个矩形
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:19335 - 📍 [步骤1] 几何扫描完成，获得 14 个基础矩形
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:19405 - 📍 [包含过滤] 极大候选数量: 14 个
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:19434 - 📍 [步骤2] 发现伪极大矩形(大套小): 0 个
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:19452 - ✅ [步骤3] 锁定真实的打印区域: 14 个
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:20488 - 正在分析 14 个对象进行去重...
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:20578 - ✅ 去重完成：处理 14 个，删除 0 个，保留 14 个。
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:19460 - 📍 [步骤5] 去重整理完成: 14 个
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:19469 - 🎨 开始在图层 'dy_zhuanyong' 重绘并提取信息...
2026-01-15 14:21:45 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `select_print_areas_paperspace` (耗时 5.03s)
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:18916 - 🧠 [SmartCache] 💾 计算完成，正在写入缓存: 图签插入0115_Layout_平面分割图_L100.json
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:18116 - ✅ 保存列表成功: 图签插入0115_Layout_平面分割图_L100.json
2026-01-15 14:21:45 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `smart_select_polylines` (耗时 5.15s)
2026-01-15 14:21:45 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `insert_and_scale_labels_paper_space` ...
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
2026-01-15 14:21:45 - [INFO] - common_logger.py:41 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=30s
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:511 - [初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
2026-01-15 14:21:45 - [INFO] - CAD_coordination.py:51 - ✅ 协同模块已加载 (集成 Licad V2.5+)
[初始化] 成功加载 licad 核心模块
[初始化] 脚本环境加载完成: CAD_file_operations.py
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
2026-01-15 14:21:45 - [INFO] - common_logger.py:41 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=30s
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:511 - [初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
2026-01-15 14:21:45 - [INFO] - CAD_basic.py:20873 - 
🚀 [流程启动] 布局 '平面分割图' 全自动处理模式...
2026-01-15 14:21:46 - [INFO] - CAD_basic.py:20908 - ✅ 锁定待处理对象: 14 个
2026-01-15 14:21:46 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `insert_and_scale_labels_area_power` ...
2026-01-15 14:21:46 - [INFO] - CAD_basic.py:20822 - 🔄 [兼容层] Power版 -> 请求流水线...
[初始化] 成功加载 licad 核心模块
[初始化] 脚本环境加载完成: CAD_file_operations.py
2026-01-15 14:21:46 - [INFO] - common_logger.py:41 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=30s
2026-01-15 14:21:46 - [INFO] - common_logger.py:170 - 🚩 进入区域: [总装] 图签全流程 [Mode:1|AI]
2026-01-15 14:21:46 - [INFO] - insert_labels.py:1750 - 🚀 [管道] 接收外部传入对象: 14 个
2026-01-15 14:21:46 - [INFO] - insert_labels.py:1774 - 
💠 [Phase 1] 启动图签插入与缩放...
2026-01-15 14:21:46 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `insert_and_scale_labels_area_any` ...
2026-01-15 14:21:47 - [INFO] - CAD_basic.py:16299 - [成功] 已激活窗口: T20天正建筑软件 V9.0 For Autodesk AutoCAD 2021 - [图签插入0115.dwg] 位置(-8,-8) 大小1936x1056
2026-01-15 14:21:47 - [INFO] - CAD_basic.py:20488 - 正在分析 14 个对象进行去重...
2026-01-15 14:21:47 - [INFO] - CAD_basic.py:20578 - ✅ 去重完成：处理 14 个，删除 0 个，保留 14 个。
2026-01-15 14:21:47 - [INFO] - insert_labels.py:891 - 📋 [任务锁定] 目标区域: 14 个
2026-01-15 14:21:47 - [INFO] - CAD_coordination.py:237 - 🔰 [主事务开始] 一键插图签总成
2026-01-15 14:21:48 - [INFO] - CAD_coordination.py:180 - [__enter__] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:21:48 - [INFO] - common_logger.py:202 - 线程2启动（监控 SHX 对话框）
2026-01-15 14:21:48 - [INFO] - common_logger.py:202 - 线程1启动（Insert_Company_Label_Common_Block）
2026-01-15 14:21:48 - [INFO] - CAD_basic.py:12018 - =====================确认insert_and_explode_dwg版本20260115=====================
2026-01-15 14:21:49 - [INFO] - CAD_coordination.py:242 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-15 14:21:49 - [INFO] - CAD_coordination.py:180 - [__enter__] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:21:50 - [INFO] - CAD_coordination.py:504 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-15 14:21:50 - [INFO] - CAD_coordination.py:180 - [send_cmd_with_sync] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:21:50 - [INFO] - CAD_coordination.py:313 - ✅ 完成: 插入-标准图签.dwg
2026-01-15 14:21:50 - [INFO] - CAD_coordination.py:242 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-15 14:21:51 - [INFO] - CAD_coordination.py:180 - [__enter__] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:21:51 - [INFO] - CAD_coordination.py:504 - CMD -> EXPLODE
L
2026-01-15 14:21:52 - [INFO] - CAD_coordination.py:180 - [send_cmd_with_sync] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:21:52 - [INFO] - CAD_coordination.py:313 - ✅ 完成: 炸开-标准图签.dwg
2026-01-15 14:21:52 - [INFO] - CAD_basic.py:12059 - ✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-15 14:21:53 - [INFO] - CAD_coordination.py:504 - CMD -> RE
2026-01-15 14:21:54 - [INFO] - CAD_coordination.py:180 - [send_cmd_with_sync] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:21:54 - [INFO] - CAD_coordination.py:504 - CMD -> Z
E
2026-01-15 14:21:55 - [INFO] - CAD_coordination.py:180 - [send_cmd_with_sync] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
[保存] 开始保存: 图签插入0115.dwg ...
[成功] COM Save 完成: 图签插入0115.dwg
2026-01-15 14:21:56 - [INFO] - common_logger.py:202 - 线程1完成插入, 写入 result_box
2026-01-15 14:21:56 - [INFO] - common_logger.py:202 - [OK] 双线程任务完成
2026-01-15 14:21:56 - [INFO] - insert_labels.py:918 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-15 14:21:57 - [INFO] - CAD_coordination.py:180 - [insert_and_scale_labels_area_any] 🟢 等待通过(无痛): 1.03s | 拦截: 0 (全程空闲)
2026-01-15 14:21:57 - [INFO] - insert_labels.py:924 - ✅ [状态确认] CAD 已就绪。耗时: 1.04s
2026-01-15 14:21:58 - [INFO] - insert_labels.py:940 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-15 14:21:58 - [INFO] - insert_labels.py:943 - 📋 [实物清单]: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_3_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-15 14:21:58 - [INFO] - insert_labels.py:975 - ▶ 开始按信号分发...
2026-01-15 14:21:58 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.5714, YScaleFactor 1.0000→1.0000
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.2650, YScaleFactor 1.0000→0.4832
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 1.0000→0.3762, YScaleFactor 1.0000→0.4756
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 1.0000→0.2650, YScaleFactor 1.0000→0.4832
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:21:59 - [INFO] - CAD_coordination.py:313 - ✅ 完成: 一键插图签总成
2026-01-15 14:21:59 - [INFO] - CAD_coordination.py:180 - [__exit__] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
[保存] 开始保存: 图签插入0115.dwg ...
[成功] COM Save 完成: 图签插入0115.dwg
2026-01-15 14:22:00 - [INFO] - insert_labels.py:1005 - ✅ 所有图签处理完成。
2026-01-15 14:22:00 - [INFO] - CAD_basic.py:9218 - [OK] 当前图层已设置为：测试辅助
2026-01-15 14:22:00 - [INFO] - CAD_basic.py:9225 - [CLEAN] 图层 '测试辅助' 已清空（共尝试 0 次）
2026-01-15 14:22:00 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `insert_and_scale_labels_area_any` (耗时 14.77s)
2026-01-15 14:22:00 - [INFO] - insert_labels.py:1793 - 
💤 [Bridge] 等待几何数据落地...
2026-01-15 14:22:01 - [INFO] - CAD_coordination.py:180 - [run_title_block_assembly_pipeline] 🟢 等待通过(无痛): 1.03s | 拦截: 0 (全程空闲)
2026-01-15 14:22:02 - [INFO] - insert_labels.py:1799 - 
💠 [Phase 2] 启动核心规范化 (原子重试版)...
2026-01-15 14:22:02 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `normalize_core_title_blocks_by_layer_new1` ...
2026-01-15 14:22:02 - [INFO] - insert_labels.py:1528 - [CoreBlock] 🔄 [Attempt 1/3] 启动事务流程...
2026-01-15 14:22:02 - [INFO] - CAD_coordination.py:237 - 🔰 [主事务开始] 核心规范化-第1次
2026-01-15 14:22:02 - [INFO] - CAD_coordination.py:180 - [__enter__] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:03 - [INFO] - insert_labels.py:1528 - [CoreBlock]   锁定目标: 14 个
2026-01-15 14:22:03 - [INFO] - insert_labels.py:1528 - [CoreBlock]   执行批量炸开与验证...
2026-01-15 14:22:03 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:03 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:03 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:22:03 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:22:03 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:03 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:04 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:04 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:22:04 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:04 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:05 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:05 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:22:05 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:05 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:05 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:05 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:22:05 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:06 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:06 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:06 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:22:06 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:06 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:07 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:07 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:22:07 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:07 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:07 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:07 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:22:07 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:08 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:08 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:08 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:22:08 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:08 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:09 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:09 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:22:09 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:09 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.11s | 拦截: 0 (全程空闲)
2026-01-15 14:22:10 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:10 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.78s)
2026-01-15 14:22:10 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:10 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.11s | 拦截: 0 (全程空闲)
2026-01-15 14:22:10 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:22:10 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.70s)
2026-01-15 14:22:10 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:11 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.11s | 拦截: 0 (全程空闲)
2026-01-15 14:22:11 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:22:11 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:22:11 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:11 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:22:12 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:12 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:22:12 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:22:12 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.11s | 拦截: 0 (全程空闲)
2026-01-15 14:22:12 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:22:12 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:22:12 - [INFO] - insert_labels.py:1528 - [CoreBlock]   等待同步 (1.0s)...
2026-01-15 14:22:14 - [INFO] - CAD_coordination.py:180 - [normalize_core_title_blocks_by_layer_new1] 🟢 等待通过(无痛): 1.03s | 拦截: 0 (全程空闲)
开始筛选，待处理对象总数: 14
筛选完成。在列表中找到的块实例数: 14
开始筛选，待处理对象总数: 14
筛选完成。在列表中找到的块实例数: 0
2026-01-15 14:22:14 - [INFO] - insert_labels.py:1528 - [CoreBlock]   ✅ 本次尝试成功，事务提交。
2026-01-15 14:22:14 - [INFO] - CAD_coordination.py:313 - ✅ 完成: 核心规范化-第1次
2026-01-15 14:22:15 - [INFO] - CAD_coordination.py:180 - [__exit__] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:22:15 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `normalize_core_title_blocks_by_layer_new1` (耗时 12.90s)
2026-01-15 14:22:15 - [INFO] - insert_labels.py:1821 - 
✨ 流水线执行完毕。
2026-01-15 14:22:15 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `insert_and_scale_labels_area_power` (耗时 29.34s)
2026-01-15 14:22:15 - [INFO] - CAD_coordination.py:180 - [wait_command_done] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:22:15 - [INFO] - CAD_basic.py:20940 - ✅ [流程结束] 布局 '平面分割图' 处理完毕。
[保存] 开始保存: 图签插入0115.dwg ...
[成功] COM Save 完成: 图签插入0115.dwg
2026-01-15 14:22:16 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `insert_and_scale_labels_paper_space` (耗时 30.69s)
2026-01-15 14:22:16 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `universal_insert_labels_dispatch` (耗时 35.94s)
True
universal_insert_labels_dispatch(
        layout_name="平面分割图", 
        operate_target="Layout", 
        Select_Config=0,      # ✨ [核心] 0=常规选择, 1=精细选择
        manual_dy_list=None,  
        filepath=None,
        layername="dy_quyu",
        delpan=0,
        debug=False,
        ref_width=None, 
        use_cache=False
    )
2026-01-15 14:27:36 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `universal_insert_labels_dispatch` ...
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:20658 - 🏗️ [Dispatch] 模式: Layout | 布局: 平面分割图 | 策略: 常规模式
2026-01-15 14:27:36 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `smart_select_polylines` ...
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:18916 - 🧠 [SmartCache] ⚡ 模式: 强制重算 (Skip Cache)
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:19003 - 🚀 [统一选择] 目标: Layout | 布局: 平面分割图 | MinSide: 100.0
2026-01-15 14:27:36 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `select_print_areas_paperspace` ...
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:19299 - 🚀 [启动] 图纸空间选择 - 目标布局: 平面分割图
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:9218 - [OK] 当前图层已设置为：dy_zhuanyong
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:9225 - [CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 0 次）
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:19313 - 🧹 [初始化] 已清空图层 dy_zhuanyong
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:19326 - 
🔄 --- 开始第 1 次分析循环 ---
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5001 - 🚀 [COM安全模式] 启动布局扫描: 平面分割图
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5011 - 📊 容器内对象总数: 80
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19314 | Type=AcDbPolyline
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [-310.9841886581022, 993.1662634268623, -310.9841886581022, 706.1662634268639, 79.01581134189797, 706.1662634268639]...
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19315 | Type=AcDbPolyline
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [162.85949222645453, 993.1662634268623, 162.85949222645453, 706.1662634268639, 552.8594922264547, 706.1662634268639]...
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19316 | Type=AcDbPolyline
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [645.7992503808167, 993.1662634268623, 645.7992503808167, 706.1662634268639, 1035.7992503808168, 706.1662634268639]...
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19317 | Type=AcDbPolyline
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [1144.2819015391676, 993.1662634268623, 1144.2819015391676, 706.1662634268639, 1534.2819015391678, 706.1662634268639]...
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19318 | Type=AcDbPolyline
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [1642.7645526975186, 993.1662634268623, 1642.7645526975186, 706.1662634268639, 2032.7645526975189, 706.1662634268639]...
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19319 | Type=AcDbPolyline
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [2141.24720385587, 993.1662634268623, 2141.24720385587, 706.1662634268639, 2531.24720385587, 706.1662634268639]...
2026-01-15 14:27:36 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931A | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [2639.729855014221, 993.1662634268623, 2639.729855014221, 706.1662634268639, 3029.729855014221, 706.1662634268639]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931B | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [3138.212506172572, 993.1662634268623, 3138.212506172572, 706.1662634268639, 3528.212506172572, 706.1662634268639]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931C | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [3636.695157330923, 993.1662634268623, 3636.695157330923, 706.1662634268639, 4026.695157330923, 706.1662634268639]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19779 | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [4736.426538862754, 706.1662634268639, 5023.426538862752, 706.1662634268639, 5023.426538862753, 1096.166263426864]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=287.00, H=390.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1981A | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [14057.032410995656, 5121.049243687463, 98157.03241099566, 5121.049243687463, 98157.03241099566, 64521.04924368746]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=84100.00, H=59400.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19824 | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [136722.03241099886, 5121.049243687463, 178722.03241099886, 5121.049243687463, 178722.03241099886, 34821.04924368746]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=42000.00, H=29700.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19825 | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [227543.0324109991, 5121.049243687463, 227543.03241099912, 64521.04924368746, 185543.0324109991, 64521.04924368746]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=42000.00, H=59400.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19828 | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [299298.7341388955, 5121.049243687463, 299298.7341388955, 47121.04924368746, 269598.7341388955, 47121.04924368746]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=29700.00, H=42000.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF3D | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [269598.7341388955, 47121.04924368746, 269598.7341388955, 5121.04924368723, 299298.7341388955, 5121.049243687223]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=29700.00, H=42000.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF51 | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [185543.0324109991, 64521.04924368746, 185543.0324109991, 5121.049243687463, 227543.03241099906, 5121.049243687456]...
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=42000.00, H=59400.00 (阈值 100.0)
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1AF65 | Type=AcDbPolyline
2026-01-15 14:27:37 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [136722.03241099886, 5121.049243687463, 178722.0324109991, 5121.049243687463, 178722.0324109991, 34821.04924368746]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=42000.00, H=29700.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5099 - 
✅ [扫描结束] 最终找到 17 个矩形
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:19335 - 📍 [步骤1] 几何扫描完成，获得 17 个基础矩形
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:19405 - 📍 [包含过滤] 极大候选数量: 17 个
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:19434 - 📍 [步骤2] 发现伪极大矩形(大套小): 6 个
2026-01-15 14:27:38 - [WARNING] - CAD_basic.py:19440 - 🧹 发现 6 个伪外框，正在移除并重新扫描...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:19326 - 
🔄 --- 开始第 2 次分析循环 ---
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5001 - 🚀 [COM安全模式] 启动布局扫描: 平面分割图
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5011 - 📊 容器内对象总数: 74
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19314 | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [-310.9841886581022, 993.1662634268623, -310.9841886581022, 706.1662634268639, 79.01581134189797, 706.1662634268639]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19315 | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [162.85949222645453, 993.1662634268623, 162.85949222645453, 706.1662634268639, 552.8594922264547, 706.1662634268639]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19316 | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [645.7992503808167, 993.1662634268623, 645.7992503808167, 706.1662634268639, 1035.7992503808168, 706.1662634268639]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19317 | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [1144.2819015391676, 993.1662634268623, 1144.2819015391676, 706.1662634268639, 1534.2819015391678, 706.1662634268639]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19318 | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [1642.7645526975186, 993.1662634268623, 1642.7645526975186, 706.1662634268639, 2032.7645526975189, 706.1662634268639]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19319 | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [2141.24720385587, 993.1662634268623, 2141.24720385587, 706.1662634268639, 2531.24720385587, 706.1662634268639]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931A | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [2639.729855014221, 993.1662634268623, 2639.729855014221, 706.1662634268639, 3029.729855014221, 706.1662634268639]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931B | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [3138.212506172572, 993.1662634268623, 3138.212506172572, 706.1662634268639, 3528.212506172572, 706.1662634268639]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1931C | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [3636.695157330923, 993.1662634268623, 3636.695157330923, 706.1662634268639, 4026.695157330923, 706.1662634268639]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=390.00, H=287.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=19779 | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=10, 推断步长=2, 顶点数=5
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [4736.426538862754, 706.1662634268639, 5023.426538862752, 706.1662634268639, 5023.426538862753, 1096.166263426864]...
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=287.00, H=390.00 (阈值 100.0)
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5024 - 
🔍 [分析对象] Handle=1981A | Type=AcDbPolyline
2026-01-15 14:27:38 - [INFO] - CAD_basic.py:5042 -    📐 数据结构: 坐标总数=8, 推断步长=2, 顶点数=4
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:5045 -    💾 原始数据前预览: [14057.032410995656, 5121.049243687463, 98157.03241099566, 5121.049243687463, 98157.03241099566, 64521.04924368746]...
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:5062 -    📏 计算尺寸: W=84100.00, H=59400.00 (阈值 100.0)
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:5090 -    ✅ >> 匹配成功！
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:5099 - 
✅ [扫描结束] 最终找到 11 个矩形
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:19335 - 📍 [步骤1] 几何扫描完成，获得 11 个基础矩形
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:19405 - 📍 [包含过滤] 极大候选数量: 11 个
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:19434 - 📍 [步骤2] 发现伪极大矩形(大套小): 0 个
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:19452 - ✅ [步骤3] 锁定真实的打印区域: 11 个
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:20488 - 正在分析 11 个对象进行去重...
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:20578 - ✅ 去重完成：处理 11 个，删除 0 个，保留 11 个。
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:19460 - 📍 [步骤5] 去重整理完成: 11 个
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:19469 - 🎨 开始在图层 'dy_zhuanyong' 重绘并提取信息...
2026-01-15 14:27:39 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `select_print_areas_paperspace` (耗时 3.35s)
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:18916 - 🧠 [SmartCache] 💾 计算完成，正在写入缓存: 图签插入0115_Layout_平面分割图_L100.json
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:18116 - ✅ 保存列表成功: 图签插入0115_Layout_平面分割图_L100.json
2026-01-15 14:27:39 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `smart_select_polylines` (耗时 3.47s)
2026-01-15 14:27:39 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `insert_and_scale_labels_paper_space` ...
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:20873 - 
🚀 [流程启动] 布局 '平面分割图' 全自动处理模式...
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:20908 - ✅ 锁定待处理对象: 11 个
2026-01-15 14:27:39 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `insert_and_scale_labels_area_power` ...
2026-01-15 14:27:39 - [INFO] - CAD_basic.py:20822 - 🔄 [兼容层] Power版 -> 请求流水线...
2026-01-15 14:27:39 - [INFO] - common_logger.py:170 - 🚩 进入区域: [总装] 图签全流程 [Mode:1|AI]
2026-01-15 14:27:39 - [INFO] - insert_labels.py:1750 - 🚀 [管道] 接收外部传入对象: 11 个
2026-01-15 14:27:39 - [INFO] - insert_labels.py:1774 - 
💠 [Phase 1] 启动图签插入与缩放...
2026-01-15 14:27:39 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `insert_and_scale_labels_area_any` ...
2026-01-15 14:27:41 - [INFO] - CAD_basic.py:16299 - [成功] 已激活窗口: T20天正建筑软件 V9.0 For Autodesk AutoCAD 2021 - [图签插入0115.dwg] 位置(-8,-8) 大小1936x1056
2026-01-15 14:27:41 - [INFO] - CAD_basic.py:20488 - 正在分析 11 个对象进行去重...
2026-01-15 14:27:41 - [INFO] - CAD_basic.py:20578 - ✅ 去重完成：处理 11 个，删除 0 个，保留 11 个。
2026-01-15 14:27:41 - [INFO] - insert_labels.py:891 - 📋 [任务锁定] 目标区域: 11 个
2026-01-15 14:27:41 - [INFO] - CAD_coordination.py:237 - 🔰 [主事务开始] 一键插图签总成
2026-01-15 14:27:42 - [INFO] - CAD_coordination.py:180 - [__enter__] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:27:42 - [INFO] - common_logger.py:202 - 线程2启动（监控 SHX 对话框）
2026-01-15 14:27:42 - [INFO] - common_logger.py:202 - 线程1启动（Insert_Company_Label_Common_Block）
2026-01-15 14:27:42 - [INFO] - CAD_basic.py:12018 - =====================确认insert_and_explode_dwg版本20260115=====================
2026-01-15 14:27:42 - [INFO] - CAD_coordination.py:242 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-15 14:27:42 - [INFO] - CAD_coordination.py:180 - [__enter__] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:27:43 - [INFO] - CAD_coordination.py:504 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-15 14:27:44 - [INFO] - CAD_coordination.py:180 - [send_cmd_with_sync] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:27:44 - [INFO] - CAD_coordination.py:313 - ✅ 完成: 插入-标准图签.dwg
2026-01-15 14:27:44 - [INFO] - CAD_coordination.py:242 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-15 14:27:44 - [INFO] - CAD_coordination.py:180 - [__enter__] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:27:45 - [INFO] - CAD_coordination.py:504 - CMD -> EXPLODE
L
2026-01-15 14:27:45 - [INFO] - CAD_coordination.py:180 - [send_cmd_with_sync] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:27:45 - [INFO] - CAD_coordination.py:313 - ✅ 完成: 炸开-标准图签.dwg
2026-01-15 14:27:45 - [INFO] - CAD_basic.py:12059 - ✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-15 14:27:46 - [INFO] - CAD_coordination.py:504 - CMD -> RE
2026-01-15 14:27:47 - [INFO] - CAD_coordination.py:180 - [send_cmd_with_sync] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:27:47 - [INFO] - CAD_coordination.py:504 - CMD -> Z
E
2026-01-15 14:27:48 - [INFO] - CAD_coordination.py:180 - [send_cmd_with_sync] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
[保存] 开始保存: 图签插入0115.dwg ...
[成功] COM Save 完成: 图签插入0115.dwg
2026-01-15 14:27:50 - [INFO] - common_logger.py:202 - 线程1完成插入, 写入 result_box
2026-01-15 14:27:50 - [INFO] - common_logger.py:202 - [OK] 双线程任务完成
2026-01-15 14:27:50 - [INFO] - insert_labels.py:918 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-15 14:27:51 - [INFO] - CAD_coordination.py:180 - [insert_and_scale_labels_area_any] 🟢 等待通过(无痛): 1.03s | 拦截: 0 (全程空闲)
2026-01-15 14:27:51 - [INFO] - insert_labels.py:924 - ✅ [状态确认] CAD 已就绪。耗时: 1.05s
2026-01-15 14:27:52 - [INFO] - insert_labels.py:940 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-15 14:27:52 - [INFO] - insert_labels.py:943 - 📋 [实物清单]: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_3_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-15 14:27:52 - [INFO] - insert_labels.py:975 - ▶ 开始按信号分发...
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.5714, YScaleFactor 1.0000→1.0000
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-15 14:27:52 - [INFO] - CAD_coordination.py:313 - ✅ 完成: 一键插图签总成
2026-01-15 14:27:53 - [INFO] - CAD_coordination.py:180 - [__exit__] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
[保存] 开始保存: 图签插入0115.dwg ...
[成功] COM Save 完成: 图签插入0115.dwg
2026-01-15 14:27:53 - [INFO] - insert_labels.py:1005 - ✅ 所有图签处理完成。
2026-01-15 14:27:53 - [INFO] - CAD_basic.py:9218 - [OK] 当前图层已设置为：测试辅助
2026-01-15 14:27:54 - [INFO] - CAD_basic.py:9225 - [CLEAN] 图层 '测试辅助' 已清空（共尝试 0 次）
2026-01-15 14:27:54 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `insert_and_scale_labels_area_any` (耗时 14.34s)
2026-01-15 14:27:54 - [INFO] - insert_labels.py:1793 - 
💤 [Bridge] 等待几何数据落地...
2026-01-15 14:27:55 - [INFO] - CAD_coordination.py:180 - [run_title_block_assembly_pipeline] 🟢 等待通过(无痛): 1.02s | 拦截: 0 (全程空闲)
2026-01-15 14:27:55 - [INFO] - insert_labels.py:1799 - 
💠 [Phase 2] 启动核心规范化 (原子重试版)...
2026-01-15 14:27:55 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `normalize_core_title_blocks_by_layer_new1` ...
2026-01-15 14:27:55 - [INFO] - insert_labels.py:1528 - [CoreBlock] 🔄 [Attempt 1/3] 启动事务流程...
2026-01-15 14:27:55 - [INFO] - CAD_coordination.py:237 - 🔰 [主事务开始] 核心规范化-第1次
2026-01-15 14:27:56 - [INFO] - CAD_coordination.py:180 - [__enter__] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:27:56 - [INFO] - insert_labels.py:1528 - [CoreBlock]   锁定目标: 11 个
2026-01-15 14:27:56 - [INFO] - insert_labels.py:1528 - [CoreBlock]   执行批量炸开与验证...
2026-01-15 14:27:56 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:27:56 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:27:57 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:27:57 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:27:57 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:27:57 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.11s | 拦截: 0 (全程空闲)
2026-01-15 14:27:57 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:27:57 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:27:57 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:27:57 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:27:58 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:27:58 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:27:58 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:27:58 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:27:59 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:27:59 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:27:59 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:27:59 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:27:59 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:27:59 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:27:59 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:28:00 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:28:00 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:28:00 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:28:00 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:28:00 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:28:01 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:28:01 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:28:01 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:28:01 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:28:01 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:28:02 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:28:02 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:28:02 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:28:02 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:28:02 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:28:02 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:28:02 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:28:03 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:28:03 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.68s)
2026-01-15 14:28:03 - [INFO] - CAD_com_utils.py:267 - ⏱ 开始 `safe_explode_retry` ...
2026-01-15 14:28:03 - [INFO] - CAD_coordination.py:180 - [_atomic_explode_and_delete] 🟢 等待通过(无痛): 0.10s | 拦截: 0 (全程空闲)
2026-01-15 14:28:04 - [INFO] - CAD_coordination.py:180 - [safe_explode_retry] 🟢 等待通过(无痛): 0.52s | 拦截: 0 (全程空闲)
2026-01-15 14:28:04 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.69s)
2026-01-15 14:28:04 - [INFO] - insert_labels.py:1528 - [CoreBlock]   等待同步 (1.0s)...
2026-01-15 14:28:05 - [INFO] - CAD_coordination.py:180 - [normalize_core_title_blocks_by_layer_new1] 🟢 等待通过(无痛): 1.03s | 拦截: 0 (全程空闲)
开始筛选，待处理对象总数: 11
筛选完成。在列表中找到的块实例数: 11
开始筛选，待处理对象总数: 11
筛选完成。在列表中找到的块实例数: 0
2026-01-15 14:28:05 - [INFO] - insert_labels.py:1528 - [CoreBlock]   ✅ 本次尝试成功，事务提交。
2026-01-15 14:28:05 - [INFO] - CAD_coordination.py:313 - ✅ 完成: 核心规范化-第1次
2026-01-15 14:28:06 - [INFO] - CAD_coordination.py:180 - [__exit__] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:28:06 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `normalize_core_title_blocks_by_layer_new1` (耗时 10.63s)
2026-01-15 14:28:06 - [INFO] - insert_labels.py:1821 - 
✨ 流水线执行完毕。
2026-01-15 14:28:06 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `insert_and_scale_labels_area_power` (耗时 26.59s)
2026-01-15 14:28:06 - [INFO] - CAD_coordination.py:180 - [wait_command_done] 🟢 等待通过(无痛): 0.51s | 拦截: 0 (全程空闲)
2026-01-15 14:28:06 - [INFO] - CAD_basic.py:20940 - ✅ [流程结束] 布局 '平面分割图' 处理完毕。
[保存] 开始保存: 图签插入0115.dwg ...
[成功] COM Save 完成: 图签插入0115.dwg
2026-01-15 14:28:07 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `insert_and_scale_labels_paper_space` (耗时 27.74s)
2026-01-15 14:28:07 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `universal_insert_labels_dispatch` (耗时 31.26s)
True
