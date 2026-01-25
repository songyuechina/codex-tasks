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
2026-01-15 14:29:49 - [INFO] - CAD_coordination.py:51 - ✅ 协同模块已加载 (集成 Licad V2.5+)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
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
[licad] 正在尝试连接 CAD COM 接口...

[licad] 连接成功: 图签插入0115.dwg
2026-01-15 14:29:56 - [INFO] - licad.py:370 - [li] 连接已刷新: 图签插入0115.dwg
2026-01-15 14:29:57 - [WARNING] - CAD_basic.py:19440 - 🧹 发现 6 个伪外框，正在移除并重新扫描...
2026-01-15 14:29:58 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `select_print_areas_paperspace` (耗时 2.12s)
2026-01-15 14:29:58 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `smart_select_polylines` (耗时 2.15s)
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
__________________  CAD基本操作开始运行 _________________________
[初始化] 成功加载 licad 核心模块
[初始化] 脚本环境加载完成: CAD_file_operations.py
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
__________________  CAD基本操作开始运行 _________________________
[初始化] 成功加载 licad 核心模块
[初始化] 脚本环境加载完成: CAD_file_operations.py
[保存] 开始保存: 图签插入0115.dwg ...
[成功] COM Save 完成: 图签插入0115.dwg
[保存] 开始保存: 图签插入0115.dwg ...
[成功] COM Save 完成: 图签插入0115.dwg
2026-01-15 14:30:12 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `insert_and_scale_labels_area_any` (耗时 13.99s)
2026-01-15 14:30:15 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:16 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:17 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:17 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:18 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:19 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:19 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:20 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:21 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:21 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
2026-01-15 14:30:22 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `safe_explode_retry` (耗时 0.67s)
开始筛选，待处理对象总数: 11
筛选完成。在列表中找到的块实例数: 11
开始筛选，待处理对象总数: 11
筛选完成。在列表中找到的块实例数: 0
2026-01-15 14:30:24 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `normalize_core_title_blocks_by_layer_new1` (耗时 10.54s)
2026-01-15 14:30:25 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `insert_and_scale_labels_area_power` (耗时 26.12s)
[保存] 开始保存: 图签插入0115.dwg ...
[成功] COM Save 完成: 图签插入0115.dwg
2026-01-15 14:30:26 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `insert_and_scale_labels_paper_space` (耗时 27.35s)
2026-01-15 14:30:26 - [WARNING] - CAD_com_utils.py:276 - ✅ 完成 `universal_insert_labels_dispatch` (耗时 29.64s)
True
