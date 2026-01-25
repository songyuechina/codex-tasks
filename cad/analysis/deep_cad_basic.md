# CAD_basic.py 深度结构映射

说明：按脚本内 #&& 标记分区，映射函数到最近的分区标题。

## &&&&%%  第一部分 导入连接
- L35: _cad_safe_print

## &&% 控制函数运行时间
- L536: _log
- L555: _kill_acad

## &&% 超时控制
- L572: connect_database_task
- L579: safe_save_cad

## &&% 双重超时保护装饰器
- L598: timeout_and_log2
- L638: test_draw_circle_and_wait

## &&% 测试轮询等待
- L719: wait_quiescent_ceshi

## &&% 测试PostCommand
- L740: complex_operation_demo

## &&% 测试卡住状态
- L814: draw_infinite_spiral

## &&% 语音播报
- L893: speak_msg

## &&% JSON数据读取存放设置
- L929: com_to_handle
- L941: serialize

## &&% 保存打印字典
- L955: save_print_dict_generic

## &&% 加载打印字典
- L970: load
- L990: current_dwg_basename
- L999: current_dwg_folder

## &&% 数据类型转换函数
- L1044: vtpnt
- L1048: vtobj
- L1052: vtFloat
- L1056: vtInt
- L1060: vtVariant
- L1064: ConvertArrays2Variant
- L1078: vtlist

## &&% 启动天正CAD及守护进程
- L1095: start_applicationV9
- L1186: force_show_cad_interface

## &&% 常规启动
- L1219: st
- L1243: get_acad_process_id

## &&% 获取CAD进程数
- L1252: jingchengshu_wenjian

## &&% 关闭所有CAD进程
- L1271: close_all_cad_processes

## &&% 关闭最早CAD进程
- L1332: close_oldest_cad_process
- L1355: ensure_typelib_from_running

## &&% 窗口缩放
- L1377: zoom_window

## &&&% RGB色彩
- L1388: aci_to_rgb

## &&% 获取实体RGB
- L1396: get_entity_rgb

## &&% 重复操作
- L1448: chongfu_caozuo
- L1508: heavy_func

## &&% 简单计时器
- L1515: simple_timer

## &&&% 选择
- L1535: _coinit_once
- L1542: get_acad_doc
- L1622: normalize_rect

## &&% 获取选择集包围盒
- L1770: get_pmxz_group_bbox

## &&% 获取选择集包围盒别名
- L1831: g

## &&% 最后对象对齐原点
- L1837: align_last_ms_obj_lb_to_origin
- L1905: get_entity_full_info

## &&% 计算直线角度
- L2021: compute_line_angle

## &&% 绘制点
- L2044: draw_point

## &&% 绘制直线
- L2063: draw_line

## &&% 绘制圆
- L2082: draw_circle

## &&% 绘制正多边形
- L2102: draw_regular_polygon

## &&% 优先水平线
- L2134: prioritize_horizontal

## &&% 获取样条曲线长度
- L2157: get_spline_length_by_conversion

## &&% 估算椭圆周长
- L2195: estimate_ellipse_length

## &&% 获取几何信息
- L2214: get_entity_geometry_info

## &&% 直线定距点
- L2303: points_on_line_at_distance_3d

## &&% 查找伪交点区域
- L2344: find_fake_intersection_regions

## &&% 直线打断
- L2410: lines_daduan

## &&% 删除重复直线
- L2436: delete_duplicate_lines

## &&% 删除冗余直线
- L2488: delete_redundant_lines

## &&% 查找孤立交点
- L2566: find_isolated_intersections

## &&% 获取多边形内点
- L2647: get_inner_point_of_polygon

## &&% 获取房间轮廓
- L2685: get_room_outline_from_point

## &&% 连接闭合多段线
- L2711: connect_lines_to_polyline_if_closed

## &&% 判断闭合多边形
- L2787: is_closed_polygon_from_lines

## &&% 判断同点
- L2849: same_point

## &&% 判断同线
- L2855: same_line

## &&% 计算绝对角度
- L2872: calculate_absolute_angle

## &&% 计算相对角度
- L2888: calculate_relative_angle

## &&% 按角度查找线段
- L2925: find_lines_angle

## &&% 查找共点线段
- L2966: find_lines_sharing_point

## &&% 查找最大转角后继线
- L2999: find_successor_line_max

## &&% 查找右下角点
- L3046: find_rightbottom_point

## &&% 查找右下角闭合多边形
- L3103: find_rightbottom_closed_polygon

## &&% 绘制多边形
- L3174: draw_polygon_as_polyline

## &&% 近似相等
- L3290: is_nearly_equal

## &&% 查找最小转角后继线
- L3298: find_successor_line_min

## &&% 获取外轮廓
- L3349: get_outer_contour

## &&% 顶点去重
- L3446: deduplicate_vertices

## &&% 分析多边形分支
- L3488: analyze_polygon_branches

## &&% 移除指定顶点线段
- L3636: remove_lines_in_LBv

## &&% 处理多边形
- L3677: process_polygons

## &&% 提取多边形
- L3759: extract_polygon_from_lines

## &&% 炸开多段线
- L3832: explode_polylines

## &&% 线段集相减
- L3862: subtract_line_sets

## &&% 最终处理
- L3891: process_final

## &&% 绘制轻量多段线
- L3973: draw_lwpolyline

## &&% 绘制轻量多段线20260113
- L4054: draw_lwpolyline

## &&% 获取唯一顶点
- L4113: get_unique_vertices_from_pl_com

## &&% 线段转点集
- L4150: convert_lines_to_points

## &&% 合并线段
- L4175: merge_segments_new

## &&% 绘制多段线
- L4241: draw_polyline

## &&% 线段转多段线
- L4336: lines_to_polylines

## &&% 查找最小点
- L4433: find_min_point

## &&% 查找最大点
- L4451: find_max_point

## &&% 计算距离
- L4468: distance

## &&% 定义矩形
- L4477: define_rectangle_by_diagonal

## &&% 定义矩形X
- L4500: define_rectangle_by_diagonal_x
- L4527: expand_rectangle
- L4551: parse_rectangle_points

## &&&% 模型空间选出矩形多段线
- L4601: get_rectangular_polylines

## &&%图纸空间矩形多段线
- L4792: get_layout_rectangular_polylines_coords

## &&&%  分析打印线20260110
- L4898: generate_name_and_ratio_from_com

## &&% 打印数据分析
- L5093: get_cad_app
- L5102: get_dimensions
- L5118: sort_coms_by_llcorner
- L5149: main
- L5219: generate_relation_list

## &&&% 选择标准打印区域
- L5251: check_strict_standard_size

## &&%新版20260111
- L5372: check_strict_standard_size

## &&% 多段线排序
- L5474: polyline_sort

## &&% 多段线转坐标
- L5507: plcom_to_coor

## &&% 坐标转多段线
- L5562: plcoor_to_com

## &&% 判断竖向框
- L5619: panduan_shuxiangkuang

## &&% 统一图幅
- L5641: tongyi_tufu

## &&% 简化多边形
- L5674: simplify_polygon

## &&% 标准化多边形
- L5716: normalize_polygon

## &&% 获取相邻点
- L5741: get_adjacent_points

## &&% 点在多边形内
- L5760: point_in_polygon

## &&% 线段相交
- L5781: line_segment_intersection_2d

## &&% 获取辅助点
- L5810: get_auxiliary_point

## &&% 凹凸度量
- L5860: concavity_measure

## &&% 凹凸角
- L5890: concavity_angle

## &&% 水平分割六边形
- L5905: split_orthogonal_hexagon

## &&% 竖向分割六边形
- L5978: split_orthogonal_hexagon_vertical

## &&% 计算面积
- L6055: area_of

## &&% 综合分割六边形
- L6068: split_hexagon_combined

## &&% 获取包围盒边
- L6125: get_bbox_edge_segments

## &&% 获取多段线内文字
- L6179: get_texts_in_polyline

## &&% 获取天正多行文字
- L6232: TDbMText_content

## &&% 实体均分点
- L6343: distribute_points_on_entity

## &&% 判断线段包含
- L6409: is_segment_contained

## &&% 公共线段
- L6475: common_segments_between_polylines

## &&% 矩形包含判断
- L6603: is_rect_inside_rect

## &&% 两多段线组矩形
- L6636: two_plines_making_rectangle

## &&% 顶点全在内部
- L6758: are_all_vertices_inside

## &&&&%% 第四部分 一般对象
- L6793: ensure_list

## &&% 元组排序
- L6861: sort_tuples

## &&% 多维容差排序
- L6888: multi_dim_tolerance_sort
- L6922: get_ll_pt
- L6926: get_center

## &&% 实体位置排序
- L6931: sort_entities_by_position
- L6964: get_line_start

## &&% 左下角排序
- L6975: sort_coms_by_llcorner

## &&% 右上角排序
- L7009: sort_coms_by_rbcorner

## &&% 自定义左下角排序
- L7046: sort_coms_by_llcorner_custom

## &&% 中心点排序
- L7097: sort_coms_by_center

## &&% 实体编号
- L7156: number_entities_by_order

## &&% 列表遍历操作
- L7186: pr_list

## &&% 列表提取操作
- L7211: apply_to_each2

## &&% 获取对象群包围盒
- L7278: get_boundingbox_from_objects

## &&% 创建组
- L7303: chuangjian_zu

## &&% 获取组对象
- L7310: nametogroup

## &&% 获取所有组名
- L7318: get_all_group_names

## &&% 获取所有组
- L7331: get_all_groups

## &&% 添加对象到组
- L7351: add_objects_to_group

## &&% 添加单对象到组
- L7371: add_object_to_group

## &&% 移除组内对象
- L7397: remove_object_from_group

## &&% 批量移除组内对象
- L7427: remove_objects_from_group

## &&% 获取组内实体
- L7458: get_com_from_groupname

## &&% 获取组内实体分类
- L7480: get_com_from_groupname_by_type

## &&% 获取组内实体排序
- L7509: get_group_entities_sorted

## &&% 组内实体按中心排序
- L7550: get_group_entities_sorted_by_type_and_bbox

## &&% 共有组实体排序
- L7596: common_group_entities_sorted

## &&% 获取组包围盒
- L7653: get_boundingbox_from_group

## &&% 复制组S1
- L7667: copy_group_S1_from_doc1_to_doc2

## &&% 句柄转对象
- L7773: HandleToObject
- L7785: print_coms_handle

## &&% 批量句柄转对象
- L7800: handles_to_coms

## &&% 获取所有句柄
- L7817: get_all_handles

## &&% 查找实体
- L7836: find_entity_by_handle

## &&% 按类型句柄分组
- L7858: group_objects_by_type_and_handle

## &&% 记录类型句柄
- L7894: record_handle_with_type

## &&% 转换命名字典
- L7910: convert_named_dict

## &&% 获取命名对象
- L7930: get_named_object

## &&% 绘制固定标签
- L7937: draw_tags_on_objects_fixed

## &&% 标记天正门
- L7983: label_tarch_doors

## &&% 获取句柄映射
- L8028: get_handle_object_map

## &&% 设置扩展数据
- L8057: set_xdata

## &&% 获取扩展数据
- L8105: get_xdata

## &&% 设置打印标记
- L8151: set_xdata_tab

## &&% 检查打印标记
- L8161: is_printApp_xdata_com

## &&% 写CAD单行文字
- L8177: write_cad_text

## &&% 写天正单行文字
- L8300: write_tianzheng_text

## &&% 文字垂直对齐
- L8534: align_text_to_vertical_line

## &&% 文字水平对齐
- L8639: align_text_to_horizontal_line

## &&% 缩放天正文字
- L8743: scale_tianzheng_text_to_cad

## &&% *** 将屏幕所选对象赋予到指定图层
- L8854: sc_objs_to_layer

## &&% 删除图层
- L8902: delete_layer

## &&% 从列表创建图层
- L8940: create_layers_from_list

## &&% 从列表删除图层
- L8970: delete_layers_from_list

## &&% 逐点标注
- L9012: dim_by_points

## &&% 确保图层存在并清空
- L9056: ensure_layer

## &&% 只在模型空间上清理
- L9108: ensure_layer_model_only

## &&% 确保图层当前
- L9177: ensure_layer_current

## &&% 设置图层属性
- L9205: set_layer_properties

## &&% 将列表中的对象图层设为目标图层
- L9257: set_layer_with_retry

## &&% 强制改图层对象颜色
- L9314: force_layer_objects_color

## &&% 从文本构建J点
- L9409: build_J_points_from_selected_texts

## &&% 坐标转经纬度
- L9445: convert_pts_dict_to_latlon

## &&% 显示隐藏图形
- L9519: xianshi_yincangtuxing

## &&% 运行CAD程序
- L9534: run_cad_program

## &&% 自动化T7窗口
- L9557: automate_window_with_pywinauto_t7

## &&% 转成T7
- L9616: zhuancheng_t7

## &&% 自动化T3窗口
- L9666: automate_window_with_pywinauto_t3

## &&% 转成T3
- L9724: zhuancheng_t3

## &&% 确保文件被删除
- L9783: ensure_file_absent

## &&% 遍历目录
- L9803: traverse_with_os_walk

## &&% 按后缀查找文件
- L9818: find_files_with_extensions

## &&% 获取无后缀文件名
- L9828: get_filename_without_extension

## &&% 按模式删除文件
- L9839: delete_files_with_patterns

## &&% 清除指定前缀文件
- L9868: clear_files_with_prefix

## &&% 按字符串查找文件
- L9907: find_files_with_string

## &&% 路径拼接
- L9917: join_paths

## &&% 获取块实例块名
- L9934: get_block_name

## &&% 获取块属性值
- L9944: huoqukuai_shuxing_zhi

## &&% 属性块标签编辑
- L9969: update_block_def_attributes_safe
- L10137: update_block_def_attributes_v7

## &&% 属性块标签编辑生效
- L10323: attsync_block_instance
- L10354: attsync_block_instance_base

## &&% 设置属性块的标签值
- L10409: set_attribute_mtext

## &&% 获取属性块标签及标签值
- L10552: get_block_attributes_dict

## &&% 筛选出指定块名外的对象
- L10649: separate_entities_by_block_names

## &&% 获取块内多段线
- L10704: huoqu_kuai_pl

## &&% 创建带基点块
- L10733: create_block_with_basepoint

## &&% 创建三角形文字块
- L10751: create_block_with_triangle_and_text
- L10776: huoqu_kuai_pl

## &&% 获取块包围盒
- L10802: get_bounding_box_of_block

## &&% 创建含插入和直线的块
- L10833: create_new_block_with_insert_and_line

## &&% 复制并移动图层块
- L10861: copy_and_move_blocks_from_layer

## &&% 旧版
- L10889: delete_block_instances_and_definition_retry

## &&% 极速清理
- L10961: delete_block_instances_and_definition_optimized

## &&% 再次优化
- L11043: delete_block_instances_and_definition_optimized

## &&% 重命名块实体
- L11129: rename_block_entity

## &&% 由块名选择实例
- L11156: get_block_instances

## &&% 获取块引用实体
- L11196: get_entities_from_block_reference

## &&% 插入块到CAD
- L11225: insert_block_into_autocad

## &&% 插入标准块
- L11252: insert_standard_block

## &&% 插入并炸开DWG
- L11329: insert_and_explode_dwg

## &&% 新版本性能测试0109
- L11424: insert_and_explode_dwg

## &&% 获取大块实例
- L11529: get_large_block_instances

## &&% 确定合乎标准打印要求的自建多段线区域
- L11588: get_large_block_instances_with_tolerance

## &&% 块内坐标转换成世界坐标（适合平面上的一般块）
- L11626: transform_point_by_block

## &&% 按名称选择块
- L11662: select_block_by_name

## &&% 获取所有块定义
- L11698: get_all_block_definitions

## &&% 获取所有块名
- L11759: get_all_block_names

## &&% 块清理
- L11778: purge_block

## &&% 清理未使用块
- L11836: purge_unused_blocks

## &&% 清理块1
- L11879: purge_block_1

## &&% 清理未使用块1
- L12020: purge_unused_blocks_1

## &&% 预留新插入块名
- L12181: reserve_block_names_for_new_insert

## &&% 获取选定块引用名
- L12271: get_selected_blockreference_names

## &&% 从区域创建CAD块
- L12341: create_block_from_region_cad

## &&% 从区域创建CMD块
- L12688: create_block_from_region_cmd

## &&% 从列表对象创建块
- L12882: create_block_from_list_cmd

## &&% 获取块内实体
- L13045: get_block_contents_at_same_location

## &&% 添加实体到块
- L13103: add_entities_to_block_direct
- L13287: add_entities_to_block_definition_explode

## &&% 重定义块内容
- L13428: redefine_block_with_entities

## &&% 提取非块实体
- L13609: extract_specific_entities_from_block

## &&% 确保简单炸开块
- L13803: safe_explode
- L13817: _atomic_explode_and_delete
- L13840: safe_explode_retry

## &&% 炸开对象并回溯
- L13977: explode_single_object_marker

## &&% 安全炸开并删除
- L14065: safe_explode_and_delete

## &&% 清理缓存
- L14130: fix_com_cache

## &&% 清除nul
- L14188: delete_all_nul_under_folder

## &&% 终止弹窗程序
- L14230: kill_dialog_killer

## &&% 终止指定py脚本 (psutil版)
- L14270: kill_python_script_by_name

## &&% 结束WPS进程
- L14575: kill_wps

## &&%关闭excel进程
- L14613: close_all_excel_processes

## &&&% 确保安全删除
- L14717: safe_delete

## &&% 区域实体移动
- L14782: move_entities_in_region

## &&% 设置点样式
- L14838: 圆点

## &&% 设置图纸背景色
- L14857: 图纸背景

## &&% 视图区域缩放
- L14868: shitu_region

## &&% 视图实体缩放
- L14890: shitu_entity

## &&% 录制屏幕GIF
- L14933: record_screen_gif

## &&% 最小化所有窗口
- L14967: minimize_all_windows

## &&% CAD窗口置左上
- L15016: set_autocad_window_to_top_left

## &&% CAD窗口置左上别名
- L15057: l

## &&% 最小化窗口Win+D
- L15067: minimize_all_windows_d

## &&% 最小化窗口Win+M
- L15080: minimize_all_windows_m

## &&% 恢复并定位窗口
- L15103: restore_and_position

## &&% 列出打开窗口标题
- L15175: list_open_window_titles

## &&% 测鼠标位置
- L15189: ceshubiao_weizhi

## &&% 后台运行IDLE
- L15201: run_idle_background

## &&% 点击并拖动
- L15227: click_and_drag

## &&% 点击并找图
- L15251: click_and_find_image_shape

## &&% 右键点击并移动
- L15289: right_click_and_move

## &&% 结束所有IDLE进程
- L15310: kill_all_idle

## &&% IDLE窗口置右上
- L15324: set_idle_window_to_top_right
- L15352: r

## &&% OBS窗口置右下
- L15358: place_obs_bottom_right
- L15387: r2

## &&% 最小化指定窗口
- L15393: minimize_window

## &&% 最大化CAD窗口
- L15413: maximize_autocad_window

## &&% 点击开始OBS录制
- L15448: start_obs_recording_by_click

## &&% 发送微信
- L15474: fs

## &&% 选微信群
- L15485: xuanqun

## &&% 复制到剪贴板
- L15516: copy_to_clipboard

## &&% 写微信
- L15536: xieweixin

## &&% 主操作函数
- L15560: 主操作函数

## &&% 主函数入口
- L15603: main_func

## &&% 录屏
- L15610: luping

## &&% 魔方
- L15658: 魔方

## &&% 运行Python脚本
- L15667: run_py

## &&% 聚焦命令行
- L15686: focus_cmdline

## &&% 激活窗口和子窗口
- L15700: activate_window_by_title

## &&% 窗口内点击
- L15754: click_in_window

## &&% 激活并点击艾可云
- L15812: activate_and_click_aikeyun

## &&% 窗口内简单拖拽
- L15848: drag_in_window_simple

## &&% 纯窗口操作炸开区域内对象
- L15899: run_auto_explode_area

## &&% 列出所有窗口
- L15927: list_all_windows
- L15939: minimize_window
- L15958: maximize_autocad_window

## &&% 设置单位精度
- L16013: set_dwg_units_precision
- L16035: jd

## &&% 列出标注样式
- L16041: list_dim_styles

## &&% 设置当前标注样式
- L16059: set_current_dimstyle_via_command

## &&% 设置当前文字样式
- L16075: set_current_text_style

## &&% 获取字体样式
- L16092: huoqu_ziti_style

## &&% 创建文字样式
- L16118: create_text_style

## &&% 设置SHX文字样式
- L16169: set_text_style_onlyshx

## &&% 设置文字样式
- L16209: set_text_style

## &&% 重命名冲突文字样式
- L16251: rename_conflicting_text_styles

## &&&%CAD连接问题
- L16464: connect_to_acad

## &&% 格式刷属性传递
- L16510: transfer_props_by_matchprop

## &&% 双线程运行1
- L16620: run_dual_threads_1

## &&% 取消CAD选择
- L16720: cancel_cad_selection

## &&&% 打印辅助
- L16738: close_wps_window_by_click

## &&% 最小化窗口
- L16780: min_w

## &&% 清除测试图层
- L16805: ql

## &&% 模型空间画点
- L16816: srhd

## &&% 图纸空间画点
- L16864: srhd_p

## &&% COM点转数学点
- L16912: comtomath
- L16924: p

## &&% 复制查看
- L16940: fuzhi_chakan

## &&% 测量文字长度
- L16968: celiang_wenzichangdu

## &&% 写入并测量文字长度
- L16985: celiang_wenzichangdu_write

## &&% 清空文件夹
- L17006: qingkong_wenjianjia

## &&% 获取包围盒信息
- L17027: get_bbox_info

## &&% 包围盒方向标志
- L17083: bbox_orientation_flag

## &&% 获取多个对象的外包盒数据
- L17106: group_bbox_corners

## &&% 包围盒中心2D
- L17234: bbox_center_2

## &&% 包围盒中心3D
- L17242: bbox_center_3

## &&% 安全获取包围盒
- L17250: safe_get_bbox

## &&% 调试风格规范
- L17394: resolve_log_level

## &&% 数据处理中心
- L17406: get_data_root
- L17413: _resolve_json_path
- L17446: extract_poly_data
- L17474: restore_poly_adaptive

## &&% 多段线列表信息存取
- L17548: save_poly_list
- L17572: load_poly_list

## &&% ctq信息存取
- L17601: save_ctq
- L17639: load_ctq

## &&% 重定义标准图签文件中的核心块
- L17726: Redefine_standard_blocks

## &&% 图名排序
- L17915: get_sorted_titles_by_areas_final

## &&% 选择测试
- L18000: get_sorted_titles_ce

## &&% 编辑块生效的强化
- L18087: batch_attsync_loop

## &&% 统一选择
- L18176: smart_select_polylines
- L18257: universal_select_polylines

## &&% 模型空间极大矩形选择打印区域
- L18333: select_print_areas_maxrect_from_polylines
- L18341: select_maxrect_polylines_1

## &&% 图纸空间打印区域的选择
- L18615: select_print_areas_paperspace

## &&% 标准框选择打印区域
- L18766: select_standard_print_areas

## &&% 从指定图层列表的图块建立打印区域
- L19048: select_print_areas_from_blocks

## &&% 从指定图层获得打印区域
- L19271: select_print_areas_from_layer

## &&% 从屏幕选择获得打印区域
- L19458: select_print_areas_from_screen
- L19644: check_valid_rect_pro

## &&% 对多段线去重处理
- L19714: remove_duplicate_polylines

## &&% 统一插图签
- L19848: universal_insert_labels_dispatch

## &&% 幂等增强插入加速版
- L20039: insert_and_scale_labels_area_power

## &&% 图纸空间的图签插入
- L20145: insert_and_scale_labels_paper_space
- L20248: clean_blocks_until_vanished

## &&% 坐标转多段线COM
- L20334: plcoor_to_com

## &&% 绘制PL并提取信息
- L20372: draw_pl_and_extract_info

## &&% 从实体绘制PL并提取
- L20451: draw_pl_and_extract_from_entities

## &&% 区域内插入块
- L20542: insert_block_into_poly_area

## &&% 区域内插入块20260109
- L20597: insert_block_into_poly_area

## &&% 计算插入因子
- L20662: compute_insert_factors

## &&% 获取实体因子
- L20701: get_factor_for_entity

## &&% 插入公司通用图签单线程
- L20714: insert_company_label_common_block

## &&% 线程1:插入公司图签
- L20773: f1_insert_company_getwindow
- L20824: _find_shx_dialog
- L20840: _ignore_shx_dialog

## &&% 线程2:删除窗口
- L20850: f2_delwindow
- L20889: run_dual_threads

## &&% 插入公司通用图签(双线程)
- L20953: Insert_Company_Label_Common_Block

## &&% 清理内部多段线
- L20992: clean_internal_polylines
- L21034: fill_block_attributes_with_tag_name
- L21057: _make_bind_dict_serializable
- L21154: normalize_core_title_blocks_by_layer

## &&% 炸开图签壳块
- L21181: explode_title_wrappers_to_core_layer

## &&% 模型空间修复插入
- L21298: repair_mp_insert

## &&% 图纸空间样式修复插入
- L21375: repair_sp_insert

## &&% 线宽修复
- L21457: smart_repair_frame_polyline_widths_m
- L21651: smart_repair_frame_polyline_widths_p

## &&% 从模型空间剪切到图纸空间
- L21849: cut_model_to_paper_and_switch
- L21961: _fallback_copy_method

## &&% 从模型空间屏幕选择对象复制到图纸空间
- L21998: cut_screen_selection_to_paper

## &&% 从图纸空间复制打印区域到模型空间
- L22092: copy_layout_polylines_to_model

## &&% 清空图纸空间
- L22192: clear_layout_objects

## &&% 清除无实例块
- L22286: clean_unused_blocks_global_scan

## &&% 统一重建字典
- L22374: smart_rebuild_print_info

## &&% 重建字典_模型空间
- L22501: rebuild_print_area_title_mapping

## &&% 重建字典_图纸空间
- L22667: rebuild_print_area_title_mapping_paper

## &&% 构建表头映射
- L22860: build_header_map

## &&% 读取Excel到字典
- L22880: read_xlsx_to_dict

## &&% 写入字典到Excel
- L22977: write_dict_to_xlsx

## &&% 自动导出
- L23104: auto_export_excel_with_fallback

## &&% 基础导出
- L23181: build_full_print_dict_and_export_excel

## &&% 自动_图名标注写入图签
- L23532: auto_process_drawing_names_by_style

## &&% 基础_图名标注写入图签
- L23640: process_drawing_names_and_fill_titleblocks

## &&% 自动写入
- L23882: auto_import_excel_to_cad

## &&% 基础写入
- L23994: read_excel_and_update_cad_titleblocks

## &&% 自动_修改图块标签属性
- L24182: auto_update_titleblock_format_by_style

## &&% 基础_修改图块标签属性
- L24257: batch_update_block_attributes_config

## &&% 统一编目录1
- L24406: bianmulu_func1_h

## &&% 编目录2_统一
- L24608: bianmulu_func2_h

## &&% 编好目录
- L24870: bianmulu_func3_h

## &&% 合并
- L25041: bianmulu_func4_h

## &&% 写入目录图签
- L25310: update_catalog_titleblocks_from_excel
- L25502: update_catalog_titleblocks_from_excel_y

## &&% 从excel写入目录dwg文件
- L25654: write_catalog_from_excel_to_cad

## &&% 读取目录结构的excel文件
- L26333: read_catalog_template_config

## &&% 将目录dwg文件合并到主文件
- L26483: get_my_template_config_from_excel

## &&% 文件名修改1
- L26568: rename_drawings

## &&% 模拟键盘调整打印图幅
- L26687: get_mouse_target_v3
- L26763: safe_input_text
- L26777: auto_setup_custom_paper_sizes

## &&% 获取当前图幅尺寸
- L26929: list_current_printer_papers

## &&% 配置字体
- L26991: replace_cad_fonts_incremental
- L27054: is_admin
- L27065: sanitize_filename

## &&% 模型空间窗口打印
- L27074: export_model_window_pure

## &&% 模型空间LISP窗口打印export_model_window_lisp_fit
- L27205: export_model_window_lisp_fit

## &&% 图纸空间窗口打印
- L27318: export_layout_window_pure

## &&% 图纸空间打印边距修正版备用
- L27450: export_layout_window_pure_bianju

## &&% 布局空间LISP窗口打印
- L27578: export_layout_window_lisp_fit_v1
- L27742: export_layout_window_lisp_fit

## &&% 文件夹打印
- L27873: print_batch_custom_list

## &&% 典型文件的绘制
- L28115: mark_print_areas_final

## &&% 生成图名标注
- L28244: generate_tarch_drawing_names_v5

## &&% 模型空间文件打印
- L28378: print_dwg_file_model

## &&% 模型空间批量打印
- L28507: print_polylines_list

## &&% 图纸空间文件打印
- L28763: print_dwg_file_layout

## &&% 图纸空间列表打印
- L28860: print_layout_polylines_list
- L29127: print_layout_polylines_list_y

## &&% 统一打印
- L29250: smart_print_dispatch
