Python 3.11.5 (tags/v3.11.5:cce6ba9, Aug 24 2023, 14:38:34) [MSC v.1936 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.

= RESTART: D:\codex-tasks\cad\tests\any_test.py
[TEST] cad root = D:\codex-tasks\cad
2026-02-04 01:30:22 - [INFO] - common_logger.py:85 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=0s, LogLevel=INFO
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
2026-02-04 01:30:24 - [INFO] - CAD_coordination.py:51 - ✅ 协同模块已加载 (集成 Licad V2.5+)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
2026-02-04 01:30:24 - [INFO] - common_logger.py:85 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=0s, LogLevel=INFO
2026-02-04 01:30:24 - [INFO] - CAD_basic.py:511 - [初始化] CAD_basic 环境加载完成，运行路径: D:\codex-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
2026-02-04 01:30:24 - [INFO] - CAD_coordination.py:51 - ✅ 协同模块已加载 (集成 Licad V2.5+)
[初始化] 成功加载 licad 核心模块
2026-02-04 01:30:25 - [INFO] - common_logger.py:85 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=0s, LogLevel=INFO
[TEST] total top-level functions = 447

================================================================================================
START FULL BATCH (NO ARTIFICIAL STOP)
================================================================================================
Database CAD_FUNCINFO already exists.

================================================================================================
🚀 ENGINEERED BATCH (DBOP CACHE + SESSION + SSE HARD TIMEOUT)
================================================================================================
File    : D:\codex-tasks\cad\scripts\CAD_basic.py
Model   : gpt-5.2-codex
Total   : 447 functions
Force   : False
Resume  : None
Stop    : None
Timeout : 60s  |  StreamHardLimit : 120s
Time    : 2026-02-04 01:30:25
================================================================================================

[001/447] ▶️ START _cad_safe_print @L35
[001/447] ✅ END   _cad_safe_print  0.2s  (reuse DB)
[002/447] ▶️ START _log @L536
[002/447] ✅ END   _log  0.3s  (reuse DB)
[003/447] ▶️ START _kill_acad @L555
[003/447] ✅ END   _kill_acad  0.2s  (reuse DB)
[004/447] ▶️ START connect_database_task @L572
[004/447] ✅ END   connect_database_task  0.2s  (reuse DB)
[005/447] ▶️ START safe_save_cad @L579
[005/447] ✅ END   safe_save_cad  0.2s  (reuse DB)
[006/447] ▶️ START timeout_and_log2 @L598
[006/447] ✅ END   timeout_and_log2  16.4s  (API ok)
[007/447] ▶️ START test_draw_circle_and_wait @L638
[007/447] ✅ END   test_draw_circle_and_wait  15.8s  (API ok)
[008/447] ▶️ START wait_quiescent_ceshi @L719
[008/447] ✅ END   wait_quiescent_ceshi  9.9s  (API ok)
[009/447] ▶️ START complex_operation_demo @L740
[009/447] ✅ END   complex_operation_demo  11.1s  (API ok)
[010/447] ▶️ START draw_infinite_spiral @L814

################################################################################################
CHECKPOINT VERIFY: #10
################################################################################################
[FUNC] draw_infinite_spiral
[FILE] D:/codex-tasks/cad/scripts/CAD_basic.py
[DEF ] start=814 end=885
[DB ] HIT ✅  id=10  updated_at=2026-02-04 01:31:32
[DB ] source_hash=dbeaceee13f3971a84ceb293627eaf6344a455e308500dd66819314a0374c368
[DB ] file_path_in_db=D:\codex-tasks\cad\scripts\CAD_basic.py

========================================================================================
🧠 函数流程分析：draw_infinite_spiral
========================================================================================

【总体功能】
  连接 AutoCAD 并持续绘制螺旋线用于压力测试，循环直到中断或异常。

【主要执行流程】
 1. 打印启动与目的说明
 2. 尝试连接 AutoCAD COM 对象并获取 ModelSpace
 3. 定义带重试的安全画线与更新函数
 4. 初始化中心点、角度、半径和计数器
 5. 进入无限循环计算两点坐标
 6. 调用安全画线，按计数设置颜色
 7. 每 50 条输出进度并更新对象
 8. 递增计数并短暂休眠
 9. 捕获中断或异常打印提示

【关键分支】
 - 当 连接 AutoCAD 失败（GetActiveObject 异常） 时：
   → 执行：打印无法连接 CAD
   → 返回：None（提前结束）
 - 当 i % 50 == 0 时：
   → 执行：打印进度并对最后一条线调用 Update
   → 返回：继续循环
 - 当 KeyboardInterrupt 时：
   → 执行：打印测试停止
   → 返回：None（自然结束）
 - 当 其他异常 时：
   → 执行：打印未知错误
   → 返回：None（自然结束）

【异常与失败路径】
 - 情况：无法连接 CAD（COM 连接异常）
   表现：打印“无法连接 CAD: ...”
   处理：直接返回
   返回：None
 - 情况：绘制过程中未知异常
   表现：打印“未知错误: ...”
   处理：结束循环
   返回：None
 - 情况：用户中断（Ctrl+C）
   表现：打印“测试停止。”
   处理：结束循环
   返回：None

【返回值】
  形式： None
   - 函数无显式返回值，默认返回 None (示例：None)

========================================================================================

[010/447] ✅ END   draw_infinite_spiral  12.2s  (API ok)
[011/447] ▶️ START speak_msg @L893
[011/447] ✅ END   speak_msg  9.9s  (API ok)
[012/447] ▶️ START com_to_handle @L929
[012/447] ✅ END   com_to_handle  8.1s  (API ok)
[013/447] ▶️ START serialize @L941
[013/447] ✅ END   serialize  13.0s  (API ok)
[014/447] ▶️ START save_print_dict_generic @L955
[014/447] ✅ END   save_print_dict_generic  12.0s  (API ok)
[015/447] ▶️ START load @L970
[015/447] ✅ END   load  10.5s  (API ok)
[016/447] ▶️ START current_dwg_basename @L990
[016/447] ✅ END   current_dwg_basename  11.7s  (API ok)
[017/447] ▶️ START current_dwg_folder @L999
[017/447] ✅ END   current_dwg_folder  12.4s  (API ok)
[018/447] ▶️ START vtpnt @L1044
[018/447] ✅ END   vtpnt  13.2s  (API ok)
[019/447] ▶️ START vtobj @L1048
[019/447] ✅ END   vtobj  9.3s  (API ok)
[020/447] ▶️ START vtFloat @L1052

################################################################################################
CHECKPOINT VERIFY: #20
################################################################################################
[FUNC] vtFloat
[FILE] D:/codex-tasks/cad/scripts/CAD_basic.py
[DEF ] start=1052 end=1055
[DB ] HIT ✅  id=20  updated_at=2026-02-04 01:33:23
[DB ] source_hash=45c27dc2879e183eb1c099f5e40278dd4ec4936a093b8a087a36810157d2a9b6
[DB ] file_path_in_db=D:\codex-tasks\cad\scripts\CAD_basic.py

========================================================================================
🧠 函数流程分析：vtFloat
========================================================================================

【总体功能】
  将传入列表封装为 COM VARIANT 的双精度浮点数组。

【输入参数】
 - lst: 需要转换为 COM 浮点数组的数值列表 (默认=无)

【主要执行流程】
 1. 接收列表参数
 2. 调用 win32com.client.VARIANT 构造函数
 3. 使用 pythoncom.VT_ARRAY | pythoncom.VT_R8 作为类型标志并返回封装结果

【关键分支】
 - 当 正常输入列表且 COM 组件可用 时：
   → 执行：构造 VARIANT 浮点数组
   → 返回：VARIANT(VT_ARRAY|VT_R8, lst)

【异常与失败路径】
 - 情况：win32com/pythoncom 不可用或未安装
   表现：ImportError/AttributeError/COM 相关异常
   处理：未捕获，向外抛出
   返回：无
 - 情况：lst 含不可转换为浮点的元素或类型不支持
   表现：TypeError/ValueError 或 COM 类型异常
   处理：未捕获，向外抛出
   返回：无

【返回值】
  形式： win32com.client.VARIANT 对象
   - value: 封装的浮点数组内容 (示例：[1.0, 2.5])
   - vt: COM 类型标志 (示例：VT_ARRAY|VT_R8)

========================================================================================

[020/447] ✅ END   vtFloat  10.5s  (API ok)
[021/447] ▶️ START vtInt @L1056
[021/447] ✅ END   vtInt  43.7s  (API ok)
[022/447] ▶️ START vtVariant @L1060
[022/447] ✅ END   vtVariant  11.2s  (API ok)
[023/447] ▶️ START ConvertArrays2Variant @L1064
[023/447] ✅ END   ConvertArrays2Variant  13.1s  (API ok)
[024/447] ▶️ START vtlist @L1078
[024/447] ✅ END   vtlist  33.0s  (API ok)
[025/447] ▶️ START start_applicationV9 @L1095
[025/447] ✅ END   start_applicationV9  69.8s  (API ok)
[026/447] ▶️ START force_show_cad_interface @L1186
[026/447] ✅ END   force_show_cad_interface  87.7s  (API ok)
[027/447] ▶️ START st @L1219
[027/447] ✅ END   st  10.5s  (API ok)
[028/447] ▶️ START get_acad_process_id @L1243
[028/447] ✅ END   get_acad_process_id  10.9s  (API ok)
[029/447] ▶️ START jingchengshu_wenjian @L1252
[029/447] ✅ END   jingchengshu_wenjian  9.5s  (API ok)
[030/447] ▶️ START close_all_cad_processes @L1271
[030/447] ✅ END   close_all_cad_processes  12.4s  (API ok)
[031/447] ▶️ START close_oldest_cad_process @L1332
[031/447] ✅ END   close_oldest_cad_process  12.0s  (API ok)
[032/447] ▶️ START ensure_typelib_from_running @L1355
[032/447] ✅ END   ensure_typelib_from_running  14.1s  (API ok)
[033/447] ▶️ START zoom_window @L1377
[033/447] ✅ END   zoom_window  13.8s  (API ok)
[034/447] ▶️ START aci_to_rgb @L1388
[034/447] ✅ END   aci_to_rgb  8.5s  (API ok)
[035/447] ▶️ START get_entity_rgb @L1396
[035/447] ✅ END   get_entity_rgb  19.9s  (API ok)
[036/447] ▶️ START chongfu_caozuo @L1448
[036/447] ✅ END   chongfu_caozuo  151.1s  (API ok)
[037/447] ▶️ START simple_timer @L1515
[037/447] ✅ END   simple_timer  11.9s  (API ok)
[038/447] ▶️ START _coinit_once @L1535
[038/447] ✅ END   _coinit_once  7.5s  (API ok)
[039/447] ▶️ START get_acad_doc @L1542
[039/447] ✅ END   get_acad_doc  19.1s  (API ok)
[040/447] ▶️ START normalize_rect @L1622
[040/447] ✅ END   normalize_rect  11.6s  (API ok)
[041/447] ▶️ START get_pmxz_group_bbox @L1770
[041/447] ✅ END   get_pmxz_group_bbox  16.4s  (API ok)
[042/447] ▶️ START g @L1831
[042/447] ✅ END   g  7.4s  (API ok)
[043/447] ▶️ START align_last_ms_obj_lb_to_origin @L1837
[043/447] ✅ END   align_last_ms_obj_lb_to_origin  58.1s  (API ok)
[044/447] ▶️ START get_entity_full_info @L1905
[044/447] ✅ END   get_entity_full_info  16.1s  (API ok)
[045/447] ▶️ START compute_line_angle @L2021
[045/447] ✅ END   compute_line_angle  9.8s  (API ok)
[046/447] ▶️ START draw_point @L2044
[046/447] ✅ END   draw_point  9.4s  (API ok)
[047/447] ▶️ START draw_line @L2063
[047/447] ✅ END   draw_line  11.6s  (API ok)
[048/447] ▶️ START draw_circle @L2082
[048/447] ✅ END   draw_circle  11.9s  (API ok)
[049/447] ▶️ START draw_regular_polygon @L2102
[049/447] ✅ END   draw_regular_polygon  11.8s  (API ok)
[050/447] ▶️ START prioritize_horizontal @L2134

################################################################################################
CHECKPOINT VERIFY: #50
################################################################################################
[FUNC] prioritize_horizontal
[FILE] D:/codex-tasks/cad/scripts/CAD_basic.py
[DEF ] start=2134 end=2156
[DB ] HIT ✅  id=50  updated_at=2026-02-04 01:45:42
[DB ] source_hash=fb2eee31681e4fd090618d93d25d7f7c3f6a7061b46f7725360b00b731582fc3
[DB ] file_path_in_db=D:\codex-tasks\cad\scripts\CAD_basic.py

========================================================================================
🧠 函数流程分析：prioritize_horizontal
========================================================================================

【总体功能】
  按 y 差是否小于容差将直线分为水平与非水平两组，保持原有相对顺序并返回两组列表。

【输入参数】
 - lines: 直线对象列表，每个对象需有 StartPoint/EndPoint 可下标三元组 (默认=None)
 - tol: 判定水平的 y 方向容差阈值 (默认=0.5)

【主要执行流程】
 1. 初始化 horizontals 与 non_horizontals 空列表
 2. 遍历 lines，读取每条线的起点/终点 y 值
 3. 计算 |y1 - y2| 与 tol 比较
 4. 满足水平条件加入 horizontals，否则加入 non_horizontals
 5. 返回 (horizontals, non_horizontals)

【关键分支】
 - 当 abs(y1 - y2) < tol 时：
   → 执行：将当前线加入 horizontals
   → 返回：最终返回的第一个列表包含该线
 - 当 abs(y1 - y2) >= tol 时：
   → 执行：将当前线加入 non_horizontals
   → 返回：最终返回的第二个列表包含该线

【异常与失败路径】
 - 情况：lines 为空或为 None
   表现：None 不可迭代导致 TypeError
   处理：未捕获，异常向外抛出
   返回：None
 - 情况：线对象缺少 StartPoint/EndPoint
   表现：AttributeError
   处理：未捕获，异常向外抛出
   返回：None
 - 情况：StartPoint/EndPoint 不可下标或长度不足
   表现：TypeError/IndexError
   处理：未捕获，异常向外抛出
   返回：None
 - 情况：y1/y2 与 tol 不可相减或比较
   表现：TypeError
   处理：未捕获，异常向外抛出
   返回：None

【返回值】
  形式： Tuple[List[LineLike], List[LineLike]]
   - 0: 水平线段列表，保持原相对顺序 (示例：[ln1, ln3])
   - 1: 非水平线段列表，保持原相对顺序 (示例：[ln2])

========================================================================================

[050/447] ✅ END   prioritize_horizontal  14.6s  (API ok)
[051/447] ▶️ START get_spline_length_by_conversion @L2157
[051/447] ✅ END   get_spline_length_by_conversion  13.7s  (API ok)
[052/447] ▶️ START estimate_ellipse_length @L2195
[052/447] ✅ END   estimate_ellipse_length  11.5s  (API ok)
[053/447] ▶️ START get_entity_geometry_info @L2214
[053/447] ✅ END   get_entity_geometry_info  28.3s  (API ok)
[054/447] ▶️ START points_on_line_at_distance_3d @L2303
[054/447] ✅ END   points_on_line_at_distance_3d  41.8s  (API ok)
[055/447] ▶️ START find_fake_intersection_regions @L2344
[055/447] ✅ END   find_fake_intersection_regions  21.6s  (API ok)
[056/447] ▶️ START lines_daduan @L2410
[056/447] ✅ END   lines_daduan  12.2s  (API ok)
[057/447] ▶️ START delete_duplicate_lines @L2436
[057/447] ✅ END   delete_duplicate_lines  19.1s  (API ok)
[058/447] ▶️ START delete_redundant_lines @L2488
[058/447] ✅ END   delete_redundant_lines  15.1s  (API ok)
[059/447] ▶️ START find_isolated_intersections @L2566
[059/447] ✅ END   find_isolated_intersections  18.0s  (API ok)
[060/447] ▶️ START get_inner_point_of_polygon @L2647
[060/447] ✅ END   get_inner_point_of_polygon  10.2s  (API ok)
[061/447] ▶️ START get_room_outline_from_point @L2685
[061/447] ✅ END   get_room_outline_from_point  12.0s  (API ok)
[062/447] ▶️ START connect_lines_to_polyline_if_closed @L2711
[062/447] ✅ END   connect_lines_to_polyline_if_closed  13.7s  (API ok)
[063/447] ▶️ START is_closed_polygon_from_lines @L2787
[063/447] ✅ END   is_closed_polygon_from_lines  14.1s  (API ok)
[064/447] ▶️ START same_point @L2849
[064/447] ✅ END   same_point  12.1s  (API ok)
[065/447] ▶️ START same_line @L2855
[065/447] ✅ END   same_line  14.3s  (API ok)
[066/447] ▶️ START calculate_absolute_angle @L2872
[066/447] ✅ END   calculate_absolute_angle  21.9s  (API ok)
[067/447] ▶️ START calculate_relative_angle @L2888
[067/447] ✅ END   calculate_relative_angle  16.3s  (API ok)
[068/447] ▶️ START find_lines_angle @L2925
[068/447] ✅ END   find_lines_angle  15.2s  (API ok)
[069/447] ▶️ START find_lines_sharing_point @L2966
[069/447] ✅ END   find_lines_sharing_point  16.7s  (API ok)
[070/447] ▶️ START find_successor_line_max @L2999
[070/447] ✅ END   find_successor_line_max  15.5s  (API ok)
[071/447] ▶️ START find_rightbottom_point @L3046
[071/447] ✅ END   find_rightbottom_point  13.7s  (API ok)
[072/447] ▶️ START find_rightbottom_closed_polygon @L3103
[072/447] ✅ END   find_rightbottom_closed_polygon  21.4s  (API ok)
[073/447] ▶️ START draw_polygon_as_polyline @L3174
[073/447] ✅ END   draw_polygon_as_polyline  44.8s  (API ok)
[074/447] ▶️ START is_nearly_equal @L3290
[074/447] ✅ END   is_nearly_equal  12.8s  (API ok)
[075/447] ▶️ START find_successor_line_min @L3298
[075/447] ✅ END   find_successor_line_min  16.8s  (API ok)
[076/447] ▶️ START get_outer_contour @L3349
[076/447] ✅ END   get_outer_contour  61.2s  (API ok)
[077/447] ▶️ START deduplicate_vertices @L3446
[077/447] ✅ END   deduplicate_vertices  14.7s  (API ok)
[078/447] ▶️ START analyze_polygon_branches @L3488
[078/447] ✅ END   analyze_polygon_branches  19.7s  (API ok)
[079/447] ▶️ START remove_lines_in_LBv @L3636
[079/447] ✅ END   remove_lines_in_LBv  15.5s  (API ok)
[080/447] ▶️ START process_polygons @L3677
[080/447] ✅ END   process_polygons  23.7s  (API ok)
[081/447] ▶️ START extract_polygon_from_lines @L3759
[081/447] ✅ END   extract_polygon_from_lines  18.9s  (API ok)
[082/447] ▶️ START explode_polylines @L3832
[082/447] ✅ END   explode_polylines  13.8s  (API ok)
[083/447] ▶️ START subtract_line_sets @L3862
[083/447] ✅ END   subtract_line_sets  14.1s  (API ok)
[084/447] ▶️ START process_final @L3891
[084/447] ✅ END   process_final  20.9s  (API ok)
[085/447] ▶️ START draw_lwpolyline @L3973
[085/447] ❌ END   draw_lwpolyline  590.3s  error=stream timeout: exceeded 120s without completed response
[086/447] ▶️ START draw_lwpolyline @L4054
[086/447] ✅ END   draw_lwpolyline  0.2s  (reuse DB)
[087/447] ▶️ START get_unique_vertices_from_pl_com @L4113
[087/447] ✅ END   get_unique_vertices_from_pl_com  15.0s  (API ok)
[088/447] ▶️ START convert_lines_to_points @L4150
[088/447] ✅ END   convert_lines_to_points  10.8s  (API ok)
[089/447] ▶️ START merge_segments_new @L4175
[089/447] ✅ END   merge_segments_new  17.1s  (API ok)
[090/447] ▶️ START draw_polyline @L4241
[090/447] ❌ END   draw_polyline  161.4s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[091/447] ▶️ START lines_to_polylines @L4336
[091/447] ✅ END   lines_to_polylines  20.7s  (API ok)
[092/447] ▶️ START find_min_point @L4433
[092/447] ✅ END   find_min_point  11.5s  (API ok)
[093/447] ▶️ START find_max_point @L4451
[093/447] ✅ END   find_max_point  13.5s  (API ok)
[094/447] ▶️ START distance @L4468
[094/447] ✅ END   distance  8.5s  (API ok)
[095/447] ▶️ START define_rectangle_by_diagonal @L4477
[095/447] ✅ END   define_rectangle_by_diagonal  14.1s  (API ok)
[096/447] ▶️ START define_rectangle_by_diagonal_x @L4500
[096/447] ✅ END   define_rectangle_by_diagonal_x  12.2s  (API ok)
[097/447] ▶️ START expand_rectangle @L4527
[097/447] ✅ END   expand_rectangle  16.3s  (API ok)
[098/447] ▶️ START parse_rectangle_points @L4551
[098/447] ✅ END   parse_rectangle_points  13.5s  (API ok)
[099/447] ▶️ START get_rectangular_polylines @L4601
[099/447] ✅ END   get_rectangular_polylines  25.2s  (API ok)
[100/447] ▶️ START get_layout_rectangular_polylines_coords @L4792
[100/447] ✅ END   get_layout_rectangular_polylines_coords  15.9s  (API ok)
[101/447] ▶️ START generate_name_and_ratio_from_com @L4898
[101/447] ✅ END   generate_name_and_ratio_from_com  274.4s  (API ok)
[102/447] ▶️ START get_cad_app @L5093
[102/447] ✅ END   get_cad_app  8.0s  (API ok)
[103/447] ▶️ START get_dimensions @L5102
[103/447] ✅ END   get_dimensions  10.8s  (API ok)
[104/447] ▶️ START sort_coms_by_llcorner @L5118
[104/447] ✅ END   sort_coms_by_llcorner  15.9s  (API ok)
[105/447] ▶️ START main @L5149
[105/447] ✅ END   main  13.7s  (API ok)
[106/447] ▶️ START generate_relation_list @L5219
[106/447] ✅ END   generate_relation_list  12.5s  (API ok)
[107/447] ▶️ START check_strict_standard_size @L5251
[107/447] ✅ END   check_strict_standard_size  23.4s  (API ok)
[108/447] ▶️ START check_strict_standard_size @L5372
[108/447] ✅ END   check_strict_standard_size  29.1s  (API ok)
[109/447] ▶️ START polyline_sort @L5474
[109/447] ✅ END   polyline_sort  13.4s  (API ok)
[110/447] ▶️ START plcom_to_coor @L5507
[110/447] ✅ END   plcom_to_coor  16.5s  (API ok)
[111/447] ▶️ START plcoor_to_com @L5562
[111/447] ✅ END   plcoor_to_com  18.8s  (API ok)
[112/447] ▶️ START panduan_shuxiangkuang @L5619
[112/447] ✅ END   panduan_shuxiangkuang  13.8s  (API ok)
[113/447] ▶️ START tongyi_tufu @L5641
[113/447] ✅ END   tongyi_tufu  13.2s  (API ok)
[114/447] ▶️ START simplify_polygon @L5674
[114/447] ✅ END   simplify_polygon  19.4s  (API ok)
[115/447] ▶️ START normalize_polygon @L5716
[115/447] ✅ END   normalize_polygon  14.7s  (API ok)
[116/447] ▶️ START get_adjacent_points @L5741
[116/447] ✅ END   get_adjacent_points  13.5s  (API ok)
[117/447] ▶️ START point_in_polygon @L5760
[117/447] ✅ END   point_in_polygon  14.3s  (API ok)
[118/447] ▶️ START line_segment_intersection_2d @L5781
[118/447] ✅ END   line_segment_intersection_2d  14.5s  (API ok)
[119/447] ▶️ START get_auxiliary_point @L5810
[119/447] ✅ END   get_auxiliary_point  32.8s  (API ok)
[120/447] ▶️ START concavity_measure @L5860
[120/447] ✅ END   concavity_measure  14.8s  (API ok)
[121/447] ▶️ START concavity_angle @L5890
[121/447] ✅ END   concavity_angle  15.6s  (API ok)
[122/447] ▶️ START split_orthogonal_hexagon @L5905
[122/447] ✅ END   split_orthogonal_hexagon  20.9s  (API ok)
[123/447] ▶️ START split_orthogonal_hexagon_vertical @L5978
[123/447] ✅ END   split_orthogonal_hexagon_vertical  21.8s  (API ok)
[124/447] ▶️ START area_of @L6055
[124/447] ✅ END   area_of  10.9s  (API ok)
[125/447] ▶️ START split_hexagon_combined @L6068
[125/447] ✅ END   split_hexagon_combined  57.3s  (API ok)
[126/447] ▶️ START get_bbox_edge_segments @L6125
[126/447] ✅ END   get_bbox_edge_segments  17.5s  (API ok)
[127/447] ▶️ START get_texts_in_polyline @L6179
[127/447] ✅ END   get_texts_in_polyline  20.6s  (API ok)
[128/447] ▶️ START TDbMText_content @L6232
[128/447] ✅ END   TDbMText_content  13.8s  (API ok)
[129/447] ▶️ START distribute_points_on_entity @L6343
[129/447] ✅ END   distribute_points_on_entity  15.4s  (API ok)
[130/447] ▶️ START is_segment_contained @L6409
[130/447] ✅ END   is_segment_contained  19.9s  (API ok)
[131/447] ▶️ START common_segments_between_polylines @L6475
[131/447] ✅ END   common_segments_between_polylines  19.1s  (API ok)
[132/447] ▶️ START is_rect_inside_rect @L6603
[132/447] ✅ END   is_rect_inside_rect  11.5s  (API ok)
[133/447] ▶️ START two_plines_making_rectangle @L6636
[133/447] ✅ END   two_plines_making_rectangle  17.9s  (API ok)
[134/447] ▶️ START are_all_vertices_inside @L6758
[134/447] ✅ END   are_all_vertices_inside  15.9s  (API ok)
[135/447] ▶️ START ensure_list @L6793
[135/447] ✅ END   ensure_list  11.6s  (API ok)
[136/447] ▶️ START sort_tuples @L6861
[136/447] ✅ END   sort_tuples  13.5s  (API ok)
[137/447] ▶️ START multi_dim_tolerance_sort @L6888
[137/447] ✅ END   multi_dim_tolerance_sort  25.3s  (API ok)
[138/447] ▶️ START get_ll_pt @L6922
[138/447] ✅ END   get_ll_pt  11.2s  (API ok)
[139/447] ▶️ START get_center @L6926
[139/447] ✅ END   get_center  11.6s  (API ok)
[140/447] ▶️ START sort_entities_by_position @L6931
[140/447] ✅ END   sort_entities_by_position  16.0s  (API ok)
[141/447] ▶️ START get_line_start @L6964
[141/447] ✅ END   get_line_start  9.1s  (API ok)
[142/447] ▶️ START sort_coms_by_llcorner @L6975
[142/447] ✅ END   sort_coms_by_llcorner  13.0s  (API ok)
[143/447] ▶️ START sort_coms_by_rbcorner @L7009
[143/447] ✅ END   sort_coms_by_rbcorner  14.2s  (API ok)
[144/447] ▶️ START sort_coms_by_llcorner_custom @L7046
[144/447] ✅ END   sort_coms_by_llcorner_custom  16.3s  (API ok)
[145/447] ▶️ START sort_coms_by_center @L7097
[145/447] ✅ END   sort_coms_by_center  14.0s  (API ok)
[146/447] ▶️ START number_entities_by_order @L7156
[146/447] ✅ END   number_entities_by_order  11.1s  (API ok)
[147/447] ▶️ START pr_list @L7186
[147/447] ✅ END   pr_list  12.7s  (API ok)
[148/447] ▶️ START apply_to_each2 @L7211
[148/447] ✅ END   apply_to_each2  16.1s  (API ok)
[149/447] ▶️ START get_boundingbox_from_objects @L7278
[149/447] ✅ END   get_boundingbox_from_objects  16.3s  (API ok)
[150/447] ▶️ START chuangjian_zu @L7303
[150/447] ✅ END   chuangjian_zu  9.1s  (API ok)
[151/447] ▶️ START nametogroup @L7310
[151/447] ✅ END   nametogroup  8.4s  (API ok)
[152/447] ▶️ START get_all_group_names @L7318
[152/447] ✅ END   get_all_group_names  9.8s  (API ok)
[153/447] ▶️ START get_all_groups @L7331
[153/447] ✅ END   get_all_groups  9.8s  (API ok)
[154/447] ▶️ START add_objects_to_group @L7351
[154/447] ✅ END   add_objects_to_group  10.9s  (API ok)
[155/447] ▶️ START add_object_to_group @L7371
[155/447] ✅ END   add_object_to_group  10.9s  (API ok)
[156/447] ▶️ START remove_object_from_group @L7397
[156/447] ✅ END   remove_object_from_group  11.3s  (API ok)
[157/447] ▶️ START remove_objects_from_group @L7427
[157/447] ✅ END   remove_objects_from_group  13.1s  (API ok)
[158/447] ▶️ START get_com_from_groupname @L7458
[158/447] ✅ END   get_com_from_groupname  10.1s  (API ok)
[159/447] ▶️ START get_com_from_groupname_by_type @L7480
[159/447] ✅ END   get_com_from_groupname_by_type  13.4s  (API ok)
[160/447] ▶️ START get_group_entities_sorted @L7509
[160/447] ✅ END   get_group_entities_sorted  14.8s  (API ok)
[161/447] ▶️ START get_group_entities_sorted_by_type_and_bbox @L7550
[161/447] ✅ END   get_group_entities_sorted_by_type_and_bbox  16.9s  (API ok)
[162/447] ▶️ START common_group_entities_sorted @L7596
[162/447] ✅ END   common_group_entities_sorted  15.6s  (API ok)
[163/447] ▶️ START get_boundingbox_from_group @L7653
[163/447] ✅ END   get_boundingbox_from_group  13.1s  (API ok)
[164/447] ▶️ START copy_group_S1_from_doc1_to_doc2 @L7667
[164/447] ✅ END   copy_group_S1_from_doc1_to_doc2  62.2s  (API ok)
[165/447] ▶️ START HandleToObject @L7773
[165/447] ✅ END   HandleToObject  11.6s  (API ok)
[166/447] ▶️ START print_coms_handle @L7785
[166/447] ✅ END   print_coms_handle  10.2s  (API ok)
[167/447] ▶️ START handles_to_coms @L7800
[167/447] ✅ END   handles_to_coms  10.9s  (API ok)
[168/447] ▶️ START get_all_handles @L7817
[168/447] ✅ END   get_all_handles  12.6s  (API ok)
[169/447] ▶️ START find_entity_by_handle @L7836
[169/447] ✅ END   find_entity_by_handle  10.7s  (API ok)
[170/447] ▶️ START group_objects_by_type_and_handle @L7858
[170/447] ✅ END   group_objects_by_type_and_handle  12.6s  (API ok)
[171/447] ▶️ START record_handle_with_type @L7894
[171/447] ✅ END   record_handle_with_type  12.3s  (API ok)
[172/447] ▶️ START convert_named_dict @L7910
[172/447] ✅ END   convert_named_dict  13.2s  (API ok)
[173/447] ▶️ START get_named_object @L7930
[173/447] ✅ END   get_named_object  10.8s  (API ok)
[174/447] ▶️ START draw_tags_on_objects_fixed @L7937
[174/447] ✅ END   draw_tags_on_objects_fixed  14.7s  (API ok)
[175/447] ▶️ START label_tarch_doors @L7983
[175/447] ✅ END   label_tarch_doors  16.9s  (API ok)
[176/447] ▶️ START get_handle_object_map @L8028
[176/447] ✅ END   get_handle_object_map  8.8s  (API ok)
[177/447] ▶️ START set_xdata @L8057
[177/447] ❌ END   set_xdata  293.7s  error=stream timeout: exceeded 120s without completed response
[178/447] ▶️ START get_xdata @L8105
[178/447] ❌ END   get_xdata  151.2s  error=request failed: ("Connection broken: InvalidChunkLength(got length b'', 0 bytes read)", InvalidChunkLength(got length b'', 0 bytes read))
[179/447] ▶️ START set_xdata_tab @L8151
[179/447] ✅ END   set_xdata_tab  8.1s  (API ok)
[180/447] ▶️ START is_printApp_xdata_com @L8161
[180/447] ✅ END   is_printApp_xdata_com  9.6s  (API ok)
[181/447] ▶️ START write_cad_text @L8177
[181/447] ✅ END   write_cad_text  243.0s  (API ok)
[182/447] ▶️ START write_tianzheng_text @L8300
[182/447] ❌ END   write_tianzheng_text  331.8s  error=request failed: ("Connection broken: InvalidChunkLength(got length b'', 0 bytes read)", InvalidChunkLength(got length b'', 0 bytes read))
[183/447] ▶️ START align_text_to_vertical_line @L8534
[183/447] ❌ END   align_text_to_vertical_line  93.2s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[184/447] ▶️ START align_text_to_horizontal_line @L8639
[184/447] ✅ END   align_text_to_horizontal_line  167.7s  (API ok)
[185/447] ▶️ START scale_tianzheng_text_to_cad @L8743
[185/447] ❌ END   scale_tianzheng_text_to_cad  257.0s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[186/447] ▶️ START sc_objs_to_layer @L8854
[186/447] ✅ END   sc_objs_to_layer  22.6s  (API ok)
[187/447] ▶️ START delete_layer @L8902
[187/447] ✅ END   delete_layer  15.1s  (API ok)
[188/447] ▶️ START create_layers_from_list @L8940
[188/447] ✅ END   create_layers_from_list  13.0s  (API ok)
[189/447] ▶️ START delete_layers_from_list @L8970
[189/447] ✅ END   delete_layers_from_list  46.5s  (API ok)
[190/447] ▶️ START dim_by_points @L9012
[190/447] ✅ END   dim_by_points  12.4s  (API ok)
[191/447] ▶️ START ensure_layer @L9056
[191/447] ✅ END   ensure_layer  18.5s  (API ok)
[192/447] ▶️ START ensure_layer_model_only @L9108
[192/447] ✅ END   ensure_layer_model_only  15.4s  (API ok)
[193/447] ▶️ START ensure_layer_current @L9177
[193/447] ✅ END   ensure_layer_current  15.4s  (API ok)
[194/447] ▶️ START set_layer_properties @L9205
[194/447] ✅ END   set_layer_properties  16.3s  (API ok)
[195/447] ▶️ START set_layer_with_retry @L9257
[195/447] ✅ END   set_layer_with_retry  18.1s  (API ok)
[196/447] ▶️ START force_layer_objects_color @L9314
[196/447] ✅ END   force_layer_objects_color  18.5s  (API ok)
[197/447] ▶️ START build_J_points_from_selected_texts @L9409
[197/447] ✅ END   build_J_points_from_selected_texts  20.5s  (API ok)
[198/447] ▶️ START convert_pts_dict_to_latlon @L9445
[198/447] ✅ END   convert_pts_dict_to_latlon  15.3s  (API ok)
[199/447] ▶️ START xianshi_yincangtuxing @L9519
[199/447] ✅ END   xianshi_yincangtuxing  7.1s  (API ok)
[200/447] ▶️ START run_cad_program @L9534
[200/447] ✅ END   run_cad_program  12.0s  (API ok)
[201/447] ▶️ START automate_window_with_pywinauto_t7 @L9557
[201/447] ✅ END   automate_window_with_pywinauto_t7  15.8s  (API ok)
[202/447] ▶️ START zhuancheng_t7 @L9616
[202/447] ✅ END   zhuancheng_t7  10.9s  (API ok)
[203/447] ▶️ START automate_window_with_pywinauto_t3 @L9666
[203/447] ✅ END   automate_window_with_pywinauto_t3  20.3s  (API ok)
[204/447] ▶️ START zhuancheng_t3 @L9724
[204/447] ✅ END   zhuancheng_t3  9.8s  (API ok)
[205/447] ▶️ START ensure_file_absent @L9783
[205/447] ✅ END   ensure_file_absent  10.2s  (API ok)
[206/447] ▶️ START traverse_with_os_walk @L9803
[206/447] ✅ END   traverse_with_os_walk  10.8s  (API ok)
[207/447] ▶️ START find_files_with_extensions @L9818
[207/447] ✅ END   find_files_with_extensions  11.1s  (API ok)
[208/447] ▶️ START get_filename_without_extension @L9828
[208/447] ✅ END   get_filename_without_extension  7.5s  (API ok)
[209/447] ▶️ START delete_files_with_patterns @L9839
[209/447] ✅ END   delete_files_with_patterns  12.2s  (API ok)
[210/447] ▶️ START clear_files_with_prefix @L9868
[210/447] ✅ END   clear_files_with_prefix  14.3s  (API ok)
[211/447] ▶️ START find_files_with_string @L9907
[211/447] ✅ END   find_files_with_string  11.6s  (API ok)
[212/447] ▶️ START join_paths @L9917
[212/447] ✅ END   join_paths  8.6s  (API ok)
[213/447] ▶️ START get_block_name @L9934
[213/447] ✅ END   get_block_name  10.1s  (API ok)
[214/447] ▶️ START huoqukuai_shuxing_zhi @L9944
[214/447] ✅ END   huoqukuai_shuxing_zhi  10.0s  (API ok)
[215/447] ▶️ START update_block_def_attributes_safe @L9969
[215/447] ❌ END   update_block_def_attributes_safe  395.5s  error=request failed: HTTPSConnectionPool(host='code.newcli.com', port=443): Read timed out.
[216/447] ▶️ START update_block_def_attributes_v7 @L10137
[216/447] ❌ END   update_block_def_attributes_v7  595.4s  error=stream timeout: exceeded 120s without completed response
[217/447] ▶️ START attsync_block_instance @L10323
[217/447] ✅ END   attsync_block_instance  17.5s  (API ok)
[218/447] ▶️ START attsync_block_instance_base @L10354
[218/447] ✅ END   attsync_block_instance_base  13.5s  (API ok)
[219/447] ▶️ START set_attribute_mtext @L10409
[219/447] ✅ END   set_attribute_mtext  24.4s  (API ok)
[220/447] ▶️ START get_block_attributes_dict @L10552
[220/447] ✅ END   get_block_attributes_dict  89.7s  (API ok)
[221/447] ▶️ START separate_entities_by_block_names @L10649
[221/447] ✅ END   separate_entities_by_block_names  16.0s  (API ok)
[222/447] ▶️ START huoqu_kuai_pl @L10704
[222/447] ✅ END   huoqu_kuai_pl  14.4s  (API ok)
[223/447] ▶️ START create_block_with_basepoint @L10733
[223/447] ✅ END   create_block_with_basepoint  10.6s  (API ok)
[224/447] ▶️ START create_block_with_triangle_and_text @L10751
[224/447] ✅ END   create_block_with_triangle_and_text  12.4s  (API ok)
[225/447] ▶️ START huoqu_kuai_pl @L10776
[225/447] ✅ END   huoqu_kuai_pl  14.8s  (API ok)
[226/447] ▶️ START get_bounding_box_of_block @L10802
[226/447] ✅ END   get_bounding_box_of_block  15.7s  (API ok)
[227/447] ▶️ START create_new_block_with_insert_and_line @L10833
[227/447] ✅ END   create_new_block_with_insert_and_line  12.0s  (API ok)
[228/447] ▶️ START copy_and_move_blocks_from_layer @L10861
[228/447] ✅ END   copy_and_move_blocks_from_layer  14.1s  (API ok)
[229/447] ▶️ START delete_block_instances_and_definition_retry @L10889
[229/447] ✅ END   delete_block_instances_and_definition_retry  17.5s  (API ok)
[230/447] ▶️ START delete_block_instances_and_definition_optimized @L10961
[230/447] ✅ END   delete_block_instances_and_definition_optimized  28.2s  (API ok)
[231/447] ▶️ START delete_block_instances_and_definition_optimized @L11043
[231/447] ✅ END   delete_block_instances_and_definition_optimized  17.6s  (API ok)
[232/447] ▶️ START rename_block_entity @L11129
[232/447] ✅ END   rename_block_entity  12.4s  (API ok)
[233/447] ▶️ START get_block_instances @L11156
[233/447] ✅ END   get_block_instances  13.9s  (API ok)
[234/447] ▶️ START get_entities_from_block_reference @L11196
[234/447] ✅ END   get_entities_from_block_reference  11.2s  (API ok)
[235/447] ▶️ START insert_block_into_autocad @L11225
[235/447] ✅ END   insert_block_into_autocad  12.8s  (API ok)
[236/447] ▶️ START insert_standard_block @L11252
[236/447] ✅ END   insert_standard_block  16.0s  (API ok)
[237/447] ▶️ START insert_and_explode_dwg @L11329
[237/447] ✅ END   insert_and_explode_dwg  28.3s  (API ok)
[238/447] ▶️ START insert_and_explode_dwg @L11424
[238/447] ✅ END   insert_and_explode_dwg  63.9s  (API ok)
[239/447] ▶️ START get_large_block_instances @L11529
[239/447] ❌ END   get_large_block_instances  317.0s  error=stream timeout: exceeded 120s without completed response
[240/447] ▶️ START get_large_block_instances_with_tolerance @L11588
[240/447] ✅ END   get_large_block_instances_with_tolerance  20.4s  (API ok)
[241/447] ▶️ START transform_point_by_block @L11626
[241/447] ✅ END   transform_point_by_block  16.7s  (API ok)
[242/447] ▶️ START select_block_by_name @L11662
[242/447] ✅ END   select_block_by_name  13.4s  (API ok)
[243/447] ▶️ START get_all_block_definitions @L11698
[243/447] ✅ END   get_all_block_definitions  21.0s  (API ok)
[244/447] ▶️ START get_all_block_names @L11759
[244/447] ✅ END   get_all_block_names  11.2s  (API ok)
[245/447] ▶️ START purge_block @L11778
[245/447] ✅ END   purge_block  17.0s  (API ok)
[246/447] ▶️ START purge_unused_blocks @L11836
[246/447] ✅ END   purge_unused_blocks  13.9s  (API ok)
[247/447] ▶️ START purge_block_1 @L11879
[247/447] ✅ END   purge_block_1  19.6s  (API ok)
[248/447] ▶️ START purge_unused_blocks_1 @L12020
[248/447] ❌ END   purge_unused_blocks_1  178.3s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[249/447] ▶️ START reserve_block_names_for_new_insert @L12181
[249/447] ✅ END   reserve_block_names_for_new_insert  113.7s  (API ok)
[250/447] ▶️ START get_selected_blockreference_names @L12271
[250/447] ✅ END   get_selected_blockreference_names  11.0s  (API ok)
[251/447] ▶️ START create_block_from_region_cad @L12341
[251/447] ❌ END   create_block_from_region_cad  341.0s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[252/447] ▶️ START create_block_from_region_cmd @L12688
[252/447] ❌ END   create_block_from_region_cmd  474.7s  error=stream timeout: exceeded 120s without completed response
[253/447] ▶️ START create_block_from_list_cmd @L12882
[253/447] ✅ END   create_block_from_list_cmd  120.0s  (API ok)
[254/447] ▶️ START get_block_contents_at_same_location @L13045
[254/447] ✅ END   get_block_contents_at_same_location  11.1s  (API ok)
[255/447] ▶️ START add_entities_to_block_direct @L13103
[255/447] ✅ END   add_entities_to_block_direct  21.0s  (API ok)
[256/447] ▶️ START add_entities_to_block_definition_explode @L13287
[256/447] ✅ END   add_entities_to_block_definition_explode  16.0s  (API ok)
[257/447] ▶️ START redefine_block_with_entities @L13428
[257/447] ✅ END   redefine_block_with_entities  71.1s  (API ok)
[258/447] ▶️ START extract_specific_entities_from_block @L13609
[258/447] ✅ END   extract_specific_entities_from_block  31.4s  (API ok)
[259/447] ▶️ START safe_explode @L13803
[259/447] ✅ END   safe_explode  9.9s  (API ok)
[260/447] ▶️ START _atomic_explode_and_delete @L13817
[260/447] ✅ END   _atomic_explode_and_delete  13.9s  (API ok)
[261/447] ▶️ START safe_explode_retry @L13840
[261/447] ✅ END   safe_explode_retry  25.3s  (API ok)
[262/447] ▶️ START explode_single_object_marker @L13977
[262/447] ✅ END   explode_single_object_marker  16.0s  (API ok)
[263/447] ▶️ START safe_explode_and_delete @L14065
[263/447] ✅ END   safe_explode_and_delete  20.9s  (API ok)
[264/447] ▶️ START fix_com_cache @L14130
[264/447] ✅ END   fix_com_cache  16.3s  (API ok)
[265/447] ▶️ START delete_all_nul_under_folder @L14188
[265/447] ✅ END   delete_all_nul_under_folder  13.4s  (API ok)
[266/447] ▶️ START kill_dialog_killer @L14230
[266/447] ✅ END   kill_dialog_killer  13.9s  (API ok)
[267/447] ▶️ START kill_python_script_by_name @L14270
[267/447] ✅ END   kill_python_script_by_name  19.5s  (API ok)
[268/447] ▶️ START kill_wps @L14575
[268/447] ✅ END   kill_wps  11.2s  (API ok)
[269/447] ▶️ START close_all_excel_processes @L14613
[269/447] ✅ END   close_all_excel_processes  15.6s  (API ok)
[270/447] ▶️ START safe_delete @L14717
[270/447] ✅ END   safe_delete  16.1s  (API ok)
[271/447] ▶️ START move_entities_in_region @L14782
[271/447] ✅ END   move_entities_in_region  21.2s  (API ok)
[272/447] ▶️ START 圆点 @L14838
[272/447] ✅ END   圆点  9.6s  (API ok)
[273/447] ▶️ START 图纸背景 @L14857
[273/447] ✅ END   图纸背景  9.8s  (API ok)
[274/447] ▶️ START shitu_region @L14868
[274/447] ✅ END   shitu_region  12.6s  (API ok)
[275/447] ▶️ START shitu_entity @L14890
[275/447] ✅ END   shitu_entity  9.6s  (API ok)
[276/447] ▶️ START record_screen_gif @L14933
[276/447] ✅ END   record_screen_gif  417.5s  (API ok)
[277/447] ▶️ START minimize_all_windows @L14967
[277/447] ✅ END   minimize_all_windows  11.9s  (API ok)
[278/447] ▶️ START set_autocad_window_to_top_left @L15016
[278/447] ✅ END   set_autocad_window_to_top_left  13.7s  (API ok)
[279/447] ▶️ START l @L15057
[279/447] ✅ END   l  6.2s  (API ok)
[280/447] ▶️ START minimize_all_windows_d @L15067
[280/447] ✅ END   minimize_all_windows_d  8.5s  (API ok)
[281/447] ▶️ START minimize_all_windows_m @L15080
[281/447] ✅ END   minimize_all_windows_m  9.9s  (API ok)
[282/447] ▶️ START restore_and_position @L15103
[282/447] ❌ END   restore_and_position  37.9s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[283/447] ▶️ START list_open_window_titles @L15175
[283/447] ✅ END   list_open_window_titles  11.1s  (API ok)
[284/447] ▶️ START ceshubiao_weizhi @L15189
[284/447] ✅ END   ceshubiao_weizhi  9.9s  (API ok)
[285/447] ▶️ START run_idle_background @L15201
[285/447] ✅ END   run_idle_background  10.1s  (API ok)
[286/447] ▶️ START click_and_drag @L15227
[286/447] ✅ END   click_and_drag  14.4s  (API ok)
[287/447] ▶️ START click_and_find_image_shape @L15251
[287/447] ✅ END   click_and_find_image_shape  16.7s  (API ok)
[288/447] ▶️ START right_click_and_move @L15289
[288/447] ✅ END   right_click_and_move  13.5s  (API ok)
[289/447] ▶️ START kill_all_idle @L15310
[289/447] ✅ END   kill_all_idle  9.9s  (API ok)
[290/447] ▶️ START set_idle_window_to_top_right @L15324
[290/447] ✅ END   set_idle_window_to_top_right  10.4s  (API ok)
[291/447] ▶️ START r @L15352
[291/447] ✅ END   r  6.0s  (API ok)
[292/447] ▶️ START place_obs_bottom_right @L15358
[292/447] ✅ END   place_obs_bottom_right  13.3s  (API ok)
[293/447] ▶️ START r2 @L15387
[293/447] ✅ END   r2  6.9s  (API ok)
[294/447] ▶️ START minimize_window @L15393
[294/447] ✅ END   minimize_window  11.1s  (API ok)
[295/447] ▶️ START maximize_autocad_window @L15413
[295/447] ✅ END   maximize_autocad_window  11.5s  (API ok)
[296/447] ▶️ START start_obs_recording_by_click @L15448
[296/447] ✅ END   start_obs_recording_by_click  13.3s  (API ok)
[297/447] ▶️ START fs @L15474
[297/447] ✅ END   fs  9.6s  (API ok)
[298/447] ▶️ START xuanqun @L15485
[298/447] ✅ END   xuanqun  13.9s  (API ok)
[299/447] ▶️ START copy_to_clipboard @L15516
[299/447] ✅ END   copy_to_clipboard  11.1s  (API ok)
[300/447] ▶️ START xieweixin @L15536
[300/447] ✅ END   xieweixin  13.7s  (API ok)
[301/447] ▶️ START 主操作函数 @L15560
[301/447] ✅ END   主操作函数  11.6s  (API ok)
[302/447] ▶️ START main_func @L15603
[302/447] ✅ END   main_func  8.1s  (API ok)
[303/447] ▶️ START luping @L15610
[303/447] ✅ END   luping  12.2s  (API ok)
[304/447] ▶️ START 魔方 @L15658
[304/447] ✅ END   魔方  9.6s  (API ok)
[305/447] ▶️ START run_py @L15667
[305/447] ✅ END   run_py  9.3s  (API ok)
[306/447] ▶️ START focus_cmdline @L15686
[306/447] ✅ END   focus_cmdline  8.6s  (API ok)
[307/447] ▶️ START activate_window_by_title @L15700
[307/447] ✅ END   activate_window_by_title  18.5s  (API ok)
[308/447] ▶️ START click_in_window @L15754
[308/447] ✅ END   click_in_window  16.3s  (API ok)
[309/447] ▶️ START activate_and_click_aikeyun @L15812
[309/447] ✅ END   activate_and_click_aikeyun  11.1s  (API ok)
[310/447] ▶️ START drag_in_window_simple @L15848
[310/447] ✅ END   drag_in_window_simple  184.8s  (API ok)
[311/447] ▶️ START run_auto_explode_area @L15899
[311/447] ✅ END   run_auto_explode_area  14.7s  (API ok)
[312/447] ▶️ START list_all_windows @L15927
[312/447] ✅ END   list_all_windows  8.3s  (API ok)
[313/447] ▶️ START minimize_window @L15939
[313/447] ✅ END   minimize_window  12.6s  (API ok)
[314/447] ▶️ START maximize_autocad_window @L15958
[314/447] ✅ END   maximize_autocad_window  13.1s  (API ok)
[315/447] ▶️ START set_dwg_units_precision @L16013
[315/447] ✅ END   set_dwg_units_precision  9.1s  (API ok)
[316/447] ▶️ START jd @L16035
[316/447] ✅ END   jd  8.3s  (API ok)
[317/447] ▶️ START list_dim_styles @L16041
[317/447] ✅ END   list_dim_styles  9.6s  (API ok)
[318/447] ▶️ START set_current_dimstyle_via_command @L16059
[318/447] ✅ END   set_current_dimstyle_via_command  9.2s  (API ok)
[319/447] ▶️ START set_current_text_style @L16075
[319/447] ✅ END   set_current_text_style  9.9s  (API ok)
[320/447] ▶️ START huoqu_ziti_style @L16092
[320/447] ✅ END   huoqu_ziti_style  7.7s  (API ok)
[321/447] ▶️ START create_text_style @L16118
[321/447] ✅ END   create_text_style  14.4s  (API ok)
[322/447] ▶️ START set_text_style_onlyshx @L16169
[322/447] ✅ END   set_text_style_onlyshx  15.4s  (API ok)
[323/447] ▶️ START set_text_style @L16209
[323/447] ✅ END   set_text_style  12.9s  (API ok)
[324/447] ▶️ START rename_conflicting_text_styles @L16251
[324/447] ✅ END   rename_conflicting_text_styles  23.3s  (API ok)
[325/447] ▶️ START transfer_props_by_matchprop @L16510
[325/447] ✅ END   transfer_props_by_matchprop  18.0s  (API ok)
[326/447] ▶️ START run_dual_threads_1 @L16620
[326/447] ✅ END   run_dual_threads_1  17.7s  (API ok)
[327/447] ▶️ START cancel_cad_selection @L16720
[327/447] ✅ END   cancel_cad_selection  10.6s  (API ok)
[328/447] ▶️ START close_wps_window_by_click @L16738
[328/447] ✅ END   close_wps_window_by_click  113.6s  (API ok)
[329/447] ▶️ START min_w @L16780
[329/447] ✅ END   min_w  8.9s  (API ok)
[330/447] ▶️ START ql @L16805
[330/447] ✅ END   ql  5.8s  (API ok)
[331/447] ▶️ START srhd @L16816
[331/447] ✅ END   srhd  15.2s  (API ok)
[332/447] ▶️ START srhd_p @L16864
[332/447] ✅ END   srhd_p  15.4s  (API ok)
[333/447] ▶️ START comtomath @L16912
[333/447] ✅ END   comtomath  8.6s  (API ok)
[334/447] ▶️ START p @L16924
[334/447] ✅ END   p  9.3s  (API ok)
[335/447] ▶️ START fuzhi_chakan @L16940
[335/447] ✅ END   fuzhi_chakan  12.1s  (API ok)
[336/447] ▶️ START celiang_wenzichangdu @L16968
[336/447] ✅ END   celiang_wenzichangdu  10.8s  (API ok)
[337/447] ▶️ START celiang_wenzichangdu_write @L16985
[337/447] ✅ END   celiang_wenzichangdu_write  11.3s  (API ok)
[338/447] ▶️ START qingkong_wenjianjia @L17006
[338/447] ✅ END   qingkong_wenjianjia  10.7s  (API ok)
[339/447] ▶️ START get_bbox_info @L17027
[339/447] ✅ END   get_bbox_info  15.1s  (API ok)
[340/447] ▶️ START bbox_orientation_flag @L17083
[340/447] ✅ END   bbox_orientation_flag  43.5s  (API ok)
[341/447] ▶️ START group_bbox_corners @L17106
[341/447] ✅ END   group_bbox_corners  17.5s  (API ok)
[342/447] ▶️ START bbox_center_2 @L17234
[342/447] ✅ END   bbox_center_2  11.5s  (API ok)
[343/447] ▶️ START bbox_center_3 @L17242
[343/447] ✅ END   bbox_center_3  10.7s  (API ok)
[344/447] ▶️ START safe_get_bbox @L17250
[344/447] ✅ END   safe_get_bbox  21.9s  (API ok)
[345/447] ▶️ START resolve_log_level @L17394
[345/447] ✅ END   resolve_log_level  7.8s  (API ok)
[346/447] ▶️ START get_data_root @L17406
[346/447] ✅ END   get_data_root  10.4s  (API ok)
[347/447] ▶️ START _resolve_json_path @L17413
[347/447] ✅ END   _resolve_json_path  25.9s  (API ok)
[348/447] ▶️ START extract_poly_data @L17446
[348/447] ✅ END   extract_poly_data  13.9s  (API ok)
[349/447] ▶️ START restore_poly_adaptive @L17474
[349/447] ✅ END   restore_poly_adaptive  14.7s  (API ok)
[350/447] ▶️ START save_poly_list @L17548
[350/447] ✅ END   save_poly_list  12.7s  (API ok)
[351/447] ▶️ START load_poly_list @L17572
[351/447] ✅ END   load_poly_list  11.3s  (API ok)
[352/447] ▶️ START save_ctq @L17601
[352/447] ✅ END   save_ctq  15.5s  (API ok)
[353/447] ▶️ START load_ctq @L17639
[353/447] ✅ END   load_ctq  18.5s  (API ok)
[354/447] ▶️ START Redefine_standard_blocks @L17726
[354/447] ✅ END   Redefine_standard_blocks  25.0s  (API ok)
[355/447] ▶️ START get_sorted_titles_by_areas_final @L17915
[355/447] ✅ END   get_sorted_titles_by_areas_final  17.7s  (API ok)
[356/447] ▶️ START get_sorted_titles_ce @L18000
[356/447] ✅ END   get_sorted_titles_ce  30.6s  (API ok)
[357/447] ▶️ START batch_attsync_loop @L18087
[357/447] ✅ END   batch_attsync_loop  23.3s  (API ok)
[358/447] ▶️ START smart_select_polylines @L18176
[358/447] ✅ END   smart_select_polylines  69.9s  (API ok)
[359/447] ▶️ START universal_select_polylines @L18257
[359/447] ❌ END   universal_select_polylines  70.3s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[360/447] ▶️ START select_print_areas_maxrect_from_polylines @L18333
[360/447] ✅ END   select_print_areas_maxrect_from_polylines  12.6s  (API ok)
[361/447] ▶️ START select_maxrect_polylines_1 @L18341
[361/447] ❌ END   select_maxrect_polylines_1  544.6s  error=stream timeout: exceeded 120s without completed response
[362/447] ▶️ START select_print_areas_paperspace @L18615
[362/447] ❌ END   select_print_areas_paperspace  466.4s  error=request failed: HTTPSConnectionPool(host='code.newcli.com', port=443): Read timed out.
[363/447] ▶️ START select_standard_print_areas @L18766
[363/447] ❌ END   select_standard_print_areas  180.5s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[364/447] ▶️ START select_print_areas_from_blocks @L19048
[364/447] ❌ END   select_print_areas_from_blocks  308.7s  error=stream timeout: exceeded 120s without completed response
[365/447] ▶️ START select_print_areas_from_layer @L19271
[365/447] ❌ END   select_print_areas_from_layer  269.2s  error=stream timeout: exceeded 120s without completed response
[366/447] ▶️ START select_print_areas_from_screen @L19458
[366/447] ❌ END   select_print_areas_from_screen  435.0s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[367/447] ▶️ START check_valid_rect_pro @L19644
[367/447] ✅ END   check_valid_rect_pro  21.2s  (API ok)
[368/447] ▶️ START remove_duplicate_polylines @L19714
[368/447] ❌ END   remove_duplicate_polylines  69.0s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[369/447] ▶️ START universal_insert_labels_dispatch @L19848
[369/447] ✅ END   universal_insert_labels_dispatch  26.4s  (API ok)
[370/447] ▶️ START insert_and_scale_labels_area_power @L20039
[370/447] ✅ END   insert_and_scale_labels_area_power  73.5s  (API ok)
[371/447] ▶️ START insert_and_scale_labels_paper_space @L20145
[371/447] ✅ END   insert_and_scale_labels_paper_space  20.4s  (API ok)
[372/447] ▶️ START clean_blocks_until_vanished @L20248
[372/447] ✅ END   clean_blocks_until_vanished  17.9s  (API ok)
[373/447] ▶️ START plcoor_to_com @L20334
[373/447] ✅ END   plcoor_to_com  20.6s  (API ok)
[374/447] ▶️ START draw_pl_and_extract_info @L20372
[374/447] ✅ END   draw_pl_and_extract_info  21.9s  (API ok)
[375/447] ▶️ START draw_pl_and_extract_from_entities @L20451
[375/447] ✅ END   draw_pl_and_extract_from_entities  329.5s  (API ok)
[376/447] ▶️ START insert_block_into_poly_area @L20542
[376/447] ✅ END   insert_block_into_poly_area  19.3s  (API ok)
[377/447] ▶️ START insert_block_into_poly_area @L20597
[377/447] ✅ END   insert_block_into_poly_area  20.0s  (API ok)
[378/447] ▶️ START compute_insert_factors @L20662
[378/447] ✅ END   compute_insert_factors  19.6s  (API ok)
[379/447] ▶️ START get_factor_for_entity @L20701
[379/447] ✅ END   get_factor_for_entity  10.2s  (API ok)
[380/447] ▶️ START insert_company_label_common_block @L20714
[380/447] ✅ END   insert_company_label_common_block  112.2s  (API ok)
[381/447] ▶️ START f1_insert_company_getwindow @L20773
[381/447] ❌ END   f1_insert_company_getwindow  201.2s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[382/447] ▶️ START _find_shx_dialog @L20824
[382/447] ✅ END   _find_shx_dialog  10.4s  (API ok)
[383/447] ▶️ START _ignore_shx_dialog @L20840
[383/447] ✅ END   _ignore_shx_dialog  11.7s  (API ok)
[384/447] ▶️ START f2_delwindow @L20850
[384/447] ✅ END   f2_delwindow  106.8s  (API ok)
[385/447] ▶️ START run_dual_threads @L20889
[385/447] ❌ END   run_dual_threads  151.6s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[386/447] ▶️ START Insert_Company_Label_Common_Block @L20953
[386/447] ✅ END   Insert_Company_Label_Common_Block  68.4s  (API ok)
[387/447] ▶️ START clean_internal_polylines @L20992
[387/447] ✅ END   clean_internal_polylines  18.1s  (API ok)
[388/447] ▶️ START fill_block_attributes_with_tag_name @L21034
[388/447] ✅ END   fill_block_attributes_with_tag_name  14.3s  (API ok)
[389/447] ▶️ START _make_bind_dict_serializable @L21057
[389/447] ✅ END   _make_bind_dict_serializable  23.1s  (API ok)
[390/447] ▶️ START normalize_core_title_blocks_by_layer @L21154
[390/447] ✅ END   normalize_core_title_blocks_by_layer  99.9s  (API ok)
[391/447] ▶️ START explode_title_wrappers_to_core_layer @L21181
[391/447] ✅ END   explode_title_wrappers_to_core_layer  387.9s  (API ok)
[392/447] ▶️ START repair_mp_insert @L21298
[392/447] ✅ END   repair_mp_insert  16.8s  (API ok)
[393/447] ▶️ START repair_sp_insert @L21375
[393/447] ✅ END   repair_sp_insert  14.5s  (API ok)
[394/447] ▶️ START smart_repair_frame_polyline_widths_m @L21457
[394/447] ✅ END   smart_repair_frame_polyline_widths_m  23.0s  (API ok)
[395/447] ▶️ START smart_repair_frame_polyline_widths_p @L21651
[395/447] ✅ END   smart_repair_frame_polyline_widths_p  17.9s  (API ok)
[396/447] ▶️ START cut_model_to_paper_and_switch @L21849
[396/447] ✅ END   cut_model_to_paper_and_switch  17.4s  (API ok)
[397/447] ▶️ START _fallback_copy_method @L21961
[397/447] ✅ END   _fallback_copy_method  11.9s  (API ok)
[398/447] ▶️ START cut_screen_selection_to_paper @L21998
[398/447] ✅ END   cut_screen_selection_to_paper  14.0s  (API ok)
[399/447] ▶️ START copy_layout_polylines_to_model @L22092
[399/447] ✅ END   copy_layout_polylines_to_model  17.0s  (API ok)
[400/447] ▶️ START clear_layout_objects @L22192
[400/447] ✅ END   clear_layout_objects  20.5s  (API ok)
[401/447] ▶️ START clean_unused_blocks_global_scan @L22286
[401/447] ✅ END   clean_unused_blocks_global_scan  14.4s  (API ok)
[402/447] ▶️ START smart_rebuild_print_info @L22374
[402/447] ❌ END   smart_rebuild_print_info  133.5s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[403/447] ▶️ START rebuild_print_area_title_mapping @L22501
[403/447] ✅ END   rebuild_print_area_title_mapping  263.0s  (API ok)
[404/447] ▶️ START rebuild_print_area_title_mapping_paper @L22667
[404/447] ✅ END   rebuild_print_area_title_mapping_paper  119.3s  (API ok)
[405/447] ▶️ START build_header_map @L22860
[405/447] ✅ END   build_header_map  13.0s  (API ok)
[406/447] ▶️ START read_xlsx_to_dict @L22880
[406/447] ✅ END   read_xlsx_to_dict  13.8s  (API ok)
[407/447] ▶️ START write_dict_to_xlsx @L22977
[407/447] ❌ END   write_dict_to_xlsx  435.3s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[408/447] ▶️ START auto_export_excel_with_fallback @L23104
[408/447] ✅ END   auto_export_excel_with_fallback  274.3s  (API ok)
[409/447] ▶️ START build_full_print_dict_and_export_excel @L23181
[409/447] ✅ END   build_full_print_dict_and_export_excel  221.4s  (API ok)
[410/447] ▶️ START auto_process_drawing_names_by_style @L23532
[410/447] ✅ END   auto_process_drawing_names_by_style  294.6s  (API ok)
[411/447] ▶️ START process_drawing_names_and_fill_titleblocks @L23640
[411/447] ✅ END   process_drawing_names_and_fill_titleblocks  259.1s  (API ok)
[412/447] ▶️ START auto_import_excel_to_cad @L23882
[412/447] ✅ END   auto_import_excel_to_cad  118.2s  (API ok)
[413/447] ▶️ START read_excel_and_update_cad_titleblocks @L23994
[413/447] ✅ END   read_excel_and_update_cad_titleblocks  134.6s  (API ok)
[414/447] ▶️ START auto_update_titleblock_format_by_style @L24182
[414/447] ❌ END   auto_update_titleblock_format_by_style  186.4s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[415/447] ▶️ START batch_update_block_attributes_config @L24257
[415/447] ✅ END   batch_update_block_attributes_config  59.8s  (API ok)
[416/447] ▶️ START bianmulu_func1_h @L24406
[416/447] ✅ END   bianmulu_func1_h  142.1s  (API ok)
[417/447] ▶️ START bianmulu_func2_h @L24608
[417/447] ✅ END   bianmulu_func2_h  217.8s  (API ok)
[418/447] ▶️ START bianmulu_func3_h @L24870
[418/447] ❌ END   bianmulu_func3_h  338.0s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[419/447] ▶️ START bianmulu_func4_h @L25041
[419/447] ✅ END   bianmulu_func4_h  60.1s  (API ok)
[420/447] ▶️ START update_catalog_titleblocks_from_excel @L25310
[420/447] ✅ END   update_catalog_titleblocks_from_excel  376.7s  (API ok)
[421/447] ▶️ START update_catalog_titleblocks_from_excel_y @L25502
[421/447] ❌ END   update_catalog_titleblocks_from_excel_y  392.8s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[422/447] ▶️ START write_catalog_from_excel_to_cad @L25654
[422/447] ❌ END   write_catalog_from_excel_to_cad  228.3s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[423/447] ▶️ START read_catalog_template_config @L26333
[423/447] ✅ END   read_catalog_template_config  25.8s  (API ok)
[424/447] ▶️ START get_my_template_config_from_excel @L26483
[424/447] ✅ END   get_my_template_config_from_excel  20.5s  (API ok)
[425/447] ▶️ START rename_drawings @L26568
[425/447] ❌ END   rename_drawings  583.3s  error=stream timeout: exceeded 120s without completed response
[426/447] ▶️ START get_mouse_target_v3 @L26687
[426/447] ✅ END   get_mouse_target_v3  18.8s  (API ok)
[427/447] ▶️ START safe_input_text @L26763
[427/447] ✅ END   safe_input_text  10.1s  (API ok)
[428/447] ▶️ START auto_setup_custom_paper_sizes @L26777
[428/447] ✅ END   auto_setup_custom_paper_sizes  20.2s  (API ok)
[429/447] ▶️ START list_current_printer_papers @L26929
[429/447] ✅ END   list_current_printer_papers  13.0s  (API ok)
[430/447] ▶️ START replace_cad_fonts_incremental @L26991
[430/447] ✅ END   replace_cad_fonts_incremental  12.7s  (API ok)
[431/447] ▶️ START is_admin @L27054
[431/447] ✅ END   is_admin  7.6s  (API ok)
[432/447] ▶️ START sanitize_filename @L27065
[432/447] ✅ END   sanitize_filename  9.4s  (API ok)
[433/447] ▶️ START export_model_window_pure @L27074
[433/447] ✅ END   export_model_window_pure  100.6s  (API ok)
[434/447] ▶️ START export_model_window_lisp_fit @L27205
[434/447] ❌ END   export_model_window_lisp_fit  523.0s  error=stream timeout: exceeded 120s without completed response
[435/447] ▶️ START export_layout_window_pure @L27318
[435/447] ✅ END   export_layout_window_pure  320.5s  (API ok)
[436/447] ▶️ START export_layout_window_pure_bianju @L27450
[436/447] ❌ END   export_layout_window_pure_bianju  392.2s  error=stream timeout: exceeded 120s without completed response
[437/447] ▶️ START export_layout_window_lisp_fit_v1 @L27578
[437/447] ❌ END   export_layout_window_lisp_fit_v1  483.0s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[438/447] ▶️ START export_layout_window_lisp_fit @L27742
[438/447] ✅ END   export_layout_window_lisp_fit  98.7s  (API ok)
[439/447] ▶️ START print_batch_custom_list @L27873
[439/447] ✅ END   print_batch_custom_list  345.5s  (API ok)
[440/447] ▶️ START mark_print_areas_final @L28115
[440/447] ✅ END   mark_print_areas_final  16.7s  (API ok)
[441/447] ▶️ START generate_tarch_drawing_names_v5 @L28244
[441/447] ✅ END   generate_tarch_drawing_names_v5  18.3s  (API ok)
[442/447] ▶️ START print_dwg_file_model @L28378
[442/447] ❌ END   print_dwg_file_model  450.0s  error=stream timeout: exceeded 120s without completed response
[443/447] ▶️ START print_polylines_list @L28507
[443/447] ❌ END   print_polylines_list  494.8s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[444/447] ▶️ START print_dwg_file_layout @L28763
[444/447] ✅ END   print_dwg_file_layout  389.7s  (API ok)
[445/447] ▶️ START print_layout_polylines_list @L28860
[445/447] ❌ END   print_layout_polylines_list  422.1s  error=JSON解析失败: Expecting value: line 1 column 1 (char 0)
[446/447] ▶️ START print_layout_polylines_list_y @L29127
[446/447] ❌ END   print_layout_polylines_list_y  519.4s  error=request failed: HTTPSConnectionPool(host='code.newcli.com', port=443): Read timed out.
[447/447] ▶️ START smart_print_dispatch @L29250
[447/447] ✅ END   smart_print_dispatch  109.8s  (API ok)

================================================================================================
✅ BATCH DONE (ENGINEERED)
================================================================================================
File     : D:\codex-tasks\cad\scripts\CAD_basic.py
Total    : 447
Processed: 447
Reused   : 6
Analyzed : 403
Failed   : 38
DB_SAVE_FAILED: 0
Time     : 2026-02-04 08:33:46
================================================================================================


================================================================================================
FULL BATCH DONE
================================================================================================
ok        = False
processed = 447
reused    = 6
analyzed  = 403
failed    = 38
================================================================================================
