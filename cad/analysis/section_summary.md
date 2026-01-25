# 分区功能概览（按 #&& 标记）

## library/cad_annotation.py
- : 函数 1 个 | 标签 COM:1
  示例: vtpnt
- &&&% 单行文字操作: 函数 1 个 | 标签 无
  示例: write_cad_text
- &&&% 多行文字操作: 函数 1 个 | 标签 无
  示例: write_mtext
- &&% 对齐标注: 函数 1 个 | 标签 无
  示例: add_dim_aligned
- &&% 旋转标注: 函数 1 个 | 标签 几何:1
  示例: add_dim_rotated
- &&% 角度标注: 函数 1 个 | 标签 无
  示例: add_dim_angular
- &&% 半径标注: 函数 1 个 | 标签 无
  示例: add_dim_radial
- &&% 直径标注: 函数 1 个 | 标签 无
  示例: add_dim_diametric
- &&% 添加引线: 函数 5 个 | 标签 COM:1
  示例: add_leader, get_text_content, set_text_content, get_text_height, set_text_height
- &&% 获取文字旋转角度: 函数 1 个 | 标签 无
  示例: get_text_rotation
- &&% 设置文字旋转角度: 函数 1 个 | 标签 无
  示例: set_text_rotation
- &&% 批量修改文字: 函数 1 个 | 标签 无
  示例: batch_modify_text
- &&% 创建表格: 函数 1 个 | 标签 无
  示例: create_table
- &&% 设置表格单元格文字: 函数 1 个 | 标签 无
  示例: set_table_cell_text
- &&% 获取表格单元格文字: 函数 1 个 | 标签 无
  示例: get_table_cell_text

## library/cad_blocks.py
- &&% 获取块实例块名: 函数 1 个 | 标签 无
  示例: get_block_name
- &&% 获取块属性值: 函数 1 个 | 标签 无
  示例: huoqukuai_shuxing_zhi
- &&% 属性块标签编辑: 函数 2 个 | 标签 COM:1
  示例: update_block_def_attributes_safe, update_block_def_attributes_v7
- &&% 属性块标签编辑生效: 函数 2 个 | 标签 COM:1
  示例: attsync_block_instance, attsync_block_instance_base
- &&% 设置属性块的标签值: 函数 1 个 | 标签 无
  示例: set_attribute_mtext
- &&% 获取属性块标签及标签值: 函数 1 个 | 标签 无
  示例: get_block_attributes_dict
- &&% 筛选出指定块名外的对象: 函数 1 个 | 标签 无
  示例: separate_entities_by_block_names
- &&% 获取块内多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: huoqu_kuai_pl
- &&% 创建带基点块: 函数 1 个 | 标签 COM:1
  示例: create_block_with_basepoint
- &&% 创建三角形文字块: 函数 2 个 | 标签 COM:2, 几何:2
  示例: create_block_with_triangle_and_text, huoqu_kuai_pl
- &&% 获取块包围盒: 函数 1 个 | 标签 COM:1
  示例: get_bounding_box_of_block
- &&% 创建含插入和直线的块: 函数 1 个 | 标签 COM:1
  示例: create_new_block_with_insert_and_line
- &&% 复制并移动图层块: 函数 1 个 | 标签 COM:1
  示例: copy_and_move_blocks_from_layer
- &&% 旧版: 函数 1 个 | 标签 无
  示例: delete_block_instances_and_definition_retry
- &&% 极速清理: 函数 1 个 | 标签 COM:1, 选择集:1
  示例: delete_block_instances_and_definition_optimized
- &&% 再次优化: 函数 1 个 | 标签 COM:1, 选择集:1
  示例: delete_block_instances_and_definition_optimized
- &&% 重命名块实体: 函数 1 个 | 标签 无
  示例: rename_block_entity
- &&% 由块名选择实例: 函数 1 个 | 标签 无
  示例: get_block_instances
- &&% 获取块引用实体: 函数 1 个 | 标签 无
  示例: get_entities_from_block_reference
- &&% 插入块到CAD: 函数 1 个 | 标签 无
  示例: insert_block_into_autocad
- &&% 插入标准块: 函数 1 个 | 标签 COM:1, 文件:1
  示例: insert_standard_block
- &&% 插入并炸开DWG: 函数 1 个 | 标签 COM:1, 几何:1, 文件:1
  示例: insert_and_explode_dwg
- &&% 新版本性能测试0109: 函数 1 个 | 标签 COM:1, 文件:1
  示例: insert_and_explode_dwg
- &&% 获取大块实例: 函数 1 个 | 标签 无
  示例: get_large_block_instances
- &&% 确定合乎标准打印要求的自建多段线区域: 函数 1 个 | 标签 无
  示例: get_large_block_instances_with_tolerance
- &&% 块内坐标转换成世界坐标（适合平面上的一般块）: 函数 1 个 | 标签 无
  示例: transform_point_by_block
- &&% 按名称选择块: 函数 1 个 | 标签 选择集:1
  示例: select_block_by_name
- &&% 获取所有块定义: 函数 1 个 | 标签 COM:1
  示例: get_all_block_definitions
- &&% 获取所有块名: 函数 1 个 | 标签 COM:1
  示例: get_all_block_names
- &&% 块清理: 函数 1 个 | 标签 COM:1
  示例: purge_block
- &&% 清理未使用块: 函数 1 个 | 标签 COM:1, 选择集:1
  示例: purge_unused_blocks
- &&% 清理块1: 函数 1 个 | 标签 COM:1
  示例: purge_block_1
- &&% 清理未使用块1: 函数 1 个 | 标签 COM:1
  示例: purge_unused_blocks_1
- &&% 预留新插入块名: 函数 1 个 | 标签 COM:1
  示例: reserve_block_names_for_new_insert
- &&% 获取选定块引用名: 函数 1 个 | 标签 无
  示例: get_selected_blockreference_names
- &&% 从区域创建CAD块: 函数 1 个 | 标签 COM:1, 几何:1
  示例: create_block_from_region_cad
- &&% 从区域创建CMD块: 函数 1 个 | 标签 COM:1, 选择集:1, 几何:1
  示例: create_block_from_region_cmd
- &&% 从列表对象创建块: 函数 1 个 | 标签 COM:1, 几何:1
  示例: create_block_from_list_cmd
- &&% 获取块内实体: 函数 1 个 | 标签 COM:1
  示例: get_block_contents_at_same_location
- &&% 添加实体到块: 函数 2 个 | 标签 COM:2, 几何:1
  示例: add_entities_to_block_direct, add_entities_to_block_definition_explode
- &&% 重定义块内容: 函数 1 个 | 标签 COM:1, 文件:1
  示例: redefine_block_with_entities
- &&% 提取非块实体: 函数 1 个 | 标签 几何:1
  示例: extract_specific_entities_from_block
- &&% 确保简单炸开块: 函数 3 个 | 标签 COM:1
  示例: safe_explode, _atomic_explode_and_delete, safe_explode_retry
- &&% 炸开对象并回溯: 函数 1 个 | 标签 COM:1
  示例: explode_single_object_marker
- &&% 安全炸开并删除: 函数 1 个 | 标签 无
  示例: safe_explode_and_delete
- &&% count_blocks_by_name: 函数 1 个 | 标签 选择集:1
  示例: count_blocks_by_name
- &&% count_blocks_by_type: 函数 1 个 | 标签 选择集:1
  示例: count_blocks_by_type
- &&% generate_block_report: 函数 1 个 | 标签 文件:1
  示例: generate_block_report
- &&% batch_replace_blocks: 函数 1 个 | 标签 选择集:1
  示例: batch_replace_blocks
- &&% smart_replace_blocks: 函数 1 个 | 标签 选择集:1
  示例: smart_replace_blocks

## library/cad_control.py
- &&% 清理缓存: 函数 1 个 | 标签 COM:1, 文件:1
  示例: fix_com_cache
- &&% 清除nul: 函数 1 个 | 标签 文件:1
  示例: delete_all_nul_under_folder
- &&% 终止弹窗程序: 函数 1 个 | 标签 文件:1
  示例: kill_dialog_killer
- &&% 终止指定py脚本 (psutil版): 函数 1 个 | 标签 无
  示例: kill_python_script_by_name
- &&% 结束WPS进程: 函数 1 个 | 标签 无
  示例: kill_wps
- &&%关闭excel进程: 函数 1 个 | 标签 无
  示例: close_all_excel_processes
- &&&% 确保安全删除: 函数 1 个 | 标签 无
  示例: safe_delete
- &&% 区域实体移动: 函数 1 个 | 标签 选择集:1
  示例: move_entities_in_region
- &&% 设置点样式: 函数 1 个 | 标签 无
  示例: 圆点
- &&% 设置图纸背景色: 函数 1 个 | 标签 无
  示例: 图纸背景
- &&% 视图区域缩放: 函数 1 个 | 标签 COM:1
  示例: shitu_region
- &&% 视图实体缩放: 函数 1 个 | 标签 COM:1
  示例: shitu_entity
- &&% 录制屏幕GIF: 函数 1 个 | 标签 无
  示例: record_screen_gif
- &&% 最小化所有窗口: 函数 1 个 | 标签 窗口:1
  示例: minimize_all_windows
- &&% CAD窗口置左上: 函数 1 个 | 标签 无
  示例: set_autocad_window_to_top_left
- &&% CAD窗口置左上别名: 函数 1 个 | 标签 无
  示例: l
- &&% 最小化窗口Win+D: 函数 1 个 | 标签 窗口:1
  示例: minimize_all_windows_d
- &&% 最小化窗口Win+M: 函数 1 个 | 标签 窗口:1
  示例: minimize_all_windows_m
- &&% 恢复并定位窗口: 函数 1 个 | 标签 无
  示例: restore_and_position
- &&% 列出打开窗口标题: 函数 1 个 | 标签 无
  示例: list_open_window_titles
- &&% 测鼠标位置: 函数 1 个 | 标签 无
  示例: ceshubiao_weizhi
- &&% 后台运行IDLE: 函数 1 个 | 标签 文件:1
  示例: run_idle_background
- &&% 点击并拖动: 函数 1 个 | 标签 无
  示例: click_and_drag
- &&% 点击并找图: 函数 1 个 | 标签 文件:1
  示例: click_and_find_image_shape
- &&% 右键点击并移动: 函数 1 个 | 标签 无
  示例: right_click_and_move
- &&% 结束所有IDLE进程: 函数 1 个 | 标签 无
  示例: kill_all_idle
- &&% IDLE窗口置右上: 函数 2 个 | 标签 无
  示例: set_idle_window_to_top_right, r
- &&% OBS窗口置右下: 函数 2 个 | 标签 无
  示例: place_obs_bottom_right, r2
- &&% 最小化指定窗口: 函数 1 个 | 标签 无
  示例: minimize_window
- &&% 最大化CAD窗口: 函数 1 个 | 标签 窗口:1
  示例: maximize_autocad_window
- &&% 点击开始OBS录制: 函数 1 个 | 标签 无
  示例: start_obs_recording_by_click
- &&% 发送微信: 函数 1 个 | 标签 无
  示例: fs
- &&% 选微信群: 函数 1 个 | 标签 无
  示例: xuanqun
- &&% 复制到剪贴板: 函数 1 个 | 标签 无
  示例: copy_to_clipboard
- &&% 写微信: 函数 1 个 | 标签 无
  示例: xieweixin
- &&% 主操作函数: 函数 1 个 | 标签 无
  示例: 主操作函数
- &&% 主函数入口: 函数 1 个 | 标签 无
  示例: main_func
- &&% 录屏: 函数 1 个 | 标签 无
  示例: luping
- &&% 魔方: 函数 1 个 | 标签 无
  示例: 魔方
- &&% 运行Python脚本: 函数 1 个 | 标签 无
  示例: run_py
- &&% 聚焦命令行: 函数 1 个 | 标签 无
  示例: focus_cmdline
- &&% 激活窗口和子窗口: 函数 1 个 | 标签 窗口:1
  示例: activate_window_by_title
- &&% 窗口内点击: 函数 1 个 | 标签 窗口:1
  示例: click_in_window
- &&% 激活并点击艾可云: 函数 1 个 | 标签 无
  示例: activate_and_click_aikeyun
- &&% 窗口内简单拖拽: 函数 1 个 | 标签 无
  示例: drag_in_window_simple
- &&% 纯窗口操作炸开区域内对象: 函数 1 个 | 标签 文件:1
  示例: run_auto_explode_area
- &&% 列出所有窗口: 函数 3 个 | 标签 窗口:1
  示例: list_all_windows, minimize_window, maximize_autocad_window
- &&% 设置单位精度: 函数 2 个 | 标签 无
  示例: set_dwg_units_precision, jd
- &&% 列出标注样式: 函数 1 个 | 标签 无
  示例: list_dim_styles
- &&% 设置当前标注样式: 函数 1 个 | 标签 COM:1
  示例: set_current_dimstyle_via_command
- &&% 设置当前文字样式: 函数 1 个 | 标签 无
  示例: set_current_text_style
- &&% 获取字体样式: 函数 1 个 | 标签 无
  示例: huoqu_ziti_style
- &&% 创建文字样式: 函数 1 个 | 标签 无
  示例: create_text_style
- &&% 设置SHX文字样式: 函数 1 个 | 标签 COM:1
  示例: set_text_style_onlyshx
- &&% 设置文字样式: 函数 1 个 | 标签 无
  示例: set_text_style
- &&% 重命名冲突文字样式: 函数 1 个 | 标签 COM:1, 文件:1
  示例: rename_conflicting_text_styles
- &&% 格式刷属性传递: 函数 1 个 | 标签 COM:1, 几何:1
  示例: transfer_props_by_matchprop
- &&% 双线程运行1: 函数 1 个 | 标签 COM:1
  示例: run_dual_threads_1
- &&% 取消CAD选择: 函数 1 个 | 标签 无
  示例: cancel_cad_selection
- &&&% 打印辅助: 函数 1 个 | 标签 窗口:1
  示例: close_wps_window_by_click
- &&% 最小化窗口: 函数 1 个 | 标签 窗口:1
  示例: min_w
- &&% 清除测试图层: 函数 1 个 | 标签 无
  示例: ql
- &&% 模型空间画点: 函数 1 个 | 标签 无
  示例: srhd
- &&% 图纸空间画点: 函数 1 个 | 标签 无
  示例: srhd_p
- &&% COM点转数学点: 函数 2 个 | 标签 无
  示例: comtomath, p
- &&% 复制查看: 函数 1 个 | 标签 无
  示例: fuzhi_chakan
- &&% 测量文字长度: 函数 1 个 | 标签 无
  示例: celiang_wenzichangdu
- &&% 写入并测量文字长度: 函数 1 个 | 标签 无
  示例: celiang_wenzichangdu_write
- &&% 清空文件夹: 函数 1 个 | 标签 文件:1
  示例: qingkong_wenjianjia
- &&% 获取包围盒信息: 函数 1 个 | 标签 几何:1
  示例: get_bbox_info
- &&% 包围盒方向标志: 函数 1 个 | 标签 几何:1
  示例: bbox_orientation_flag
- &&% 获取多个对象的外包盒数据: 函数 1 个 | 标签 COM:1, 几何:1
  示例: group_bbox_corners
- &&% 包围盒中心2D: 函数 1 个 | 标签 几何:1
  示例: bbox_center_2
- &&% 包围盒中心3D: 函数 1 个 | 标签 几何:1
  示例: bbox_center_3
- &&% 安全获取包围盒: 函数 1 个 | 标签 COM:1, 几何:1
  示例: safe_get_bbox
- &&% dwg状态分析函数: 函数 1 个 | 标签 选择集:1, 几何:1
  示例: analyze_dwg_objects_status

## library/cad_geometry.py
- &&% 计算直线角度: 函数 1 个 | 标签 几何:1
  示例: compute_line_angle
- &&% 绘制点: 函数 1 个 | 标签 无
  示例: draw_point
- &&% 绘制直线: 函数 1 个 | 标签 无
  示例: draw_line
- &&% 绘制圆: 函数 1 个 | 标签 无
  示例: draw_circle
- &&% 绘制正多边形: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_regular_polygon
- &&% 优先水平线: 函数 1 个 | 标签 无
  示例: prioritize_horizontal
- &&% 获取样条曲线长度: 函数 1 个 | 标签 COM:1, 几何:1
  示例: get_spline_length_by_conversion
- &&% 估算椭圆周长: 函数 1 个 | 标签 无
  示例: estimate_ellipse_length
- &&% 获取几何信息: 函数 1 个 | 标签 几何:1
  示例: get_entity_geometry_info
- &&% 直线定距点: 函数 1 个 | 标签 几何:1
  示例: points_on_line_at_distance_3d
- &&% 查找伪交点区域: 函数 1 个 | 标签 几何:1
  示例: find_fake_intersection_regions
- &&% 直线打断: 函数 1 个 | 标签 COM:1
  示例: lines_daduan
- &&% 删除重复直线: 函数 1 个 | 标签 无
  示例: delete_duplicate_lines
- &&% 删除冗余直线: 函数 1 个 | 标签 无
  示例: delete_redundant_lines
- &&% 查找孤立交点: 函数 1 个 | 标签 无
  示例: find_isolated_intersections
- &&% 获取多边形内点: 函数 1 个 | 标签 几何:1
  示例: get_inner_point_of_polygon
- &&% 获取房间轮廓: 函数 1 个 | 标签 COM:1
  示例: get_room_outline_from_point
- &&% 连接闭合多段线: 函数 1 个 | 标签 几何:1
  示例: connect_lines_to_polyline_if_closed
- &&% 判断闭合多边形: 函数 1 个 | 标签 几何:1
  示例: is_closed_polygon_from_lines
- &&% 判断同点: 函数 1 个 | 标签 无
  示例: same_point
- &&% 判断同线: 函数 1 个 | 标签 无
  示例: same_line
- &&% 计算绝对角度: 函数 1 个 | 标签 几何:1
  示例: calculate_absolute_angle
- &&% 计算相对角度: 函数 1 个 | 标签 几何:1
  示例: calculate_relative_angle
- &&% 按角度查找线段: 函数 1 个 | 标签 几何:1
  示例: find_lines_angle
- &&% 查找共点线段: 函数 1 个 | 标签 几何:1
  示例: find_lines_sharing_point
- &&% 查找最大转角后继线: 函数 1 个 | 标签 几何:1
  示例: find_successor_line_max
- &&% 查找右下角点: 函数 1 个 | 标签 无
  示例: find_rightbottom_point
- &&% 查找右下角闭合多边形: 函数 1 个 | 标签 几何:1
  示例: find_rightbottom_closed_polygon
- &&% 绘制多边形: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_polygon_as_polyline
- &&% 近似相等: 函数 1 个 | 标签 无
  示例: is_nearly_equal
- &&% 查找最小转角后继线: 函数 1 个 | 标签 几何:1
  示例: find_successor_line_min
- &&% 获取外轮廓: 函数 1 个 | 标签 几何:1
  示例: get_outer_contour
- &&% 顶点去重: 函数 1 个 | 标签 无
  示例: deduplicate_vertices
- &&% 分析多边形分支: 函数 1 个 | 标签 几何:1
  示例: analyze_polygon_branches
- &&% 移除指定顶点线段: 函数 1 个 | 标签 无
  示例: remove_lines_in_LBv
- &&% 处理多边形: 函数 1 个 | 标签 几何:1
  示例: process_polygons
- &&% 提取多边形: 函数 1 个 | 标签 几何:1
  示例: extract_polygon_from_lines
- &&% 炸开多段线: 函数 1 个 | 标签 几何:1
  示例: explode_polylines
- &&% 线段集相减: 函数 1 个 | 标签 无
  示例: subtract_line_sets
- &&% 最终处理: 函数 1 个 | 标签 几何:1
  示例: process_final
- &&% 绘制轻量多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_lwpolyline
- &&% 绘制轻量多段线20260113: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_lwpolyline
- &&% 获取唯一顶点: 函数 1 个 | 标签 几何:1
  示例: get_unique_vertices_from_pl_com
- &&% 线段转点集: 函数 1 个 | 标签 无
  示例: convert_lines_to_points
- &&% 合并线段: 函数 1 个 | 标签 无
  示例: merge_segments_new
- &&% 绘制多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_polyline
- &&% 线段转多段线: 函数 1 个 | 标签 几何:1
  示例: lines_to_polylines
- &&% 查找最小点: 函数 1 个 | 标签 无
  示例: find_min_point
- &&% 查找最大点: 函数 1 个 | 标签 无
  示例: find_max_point
- &&% 计算距离: 函数 1 个 | 标签 几何:1
  示例: distance
- &&% 定义矩形: 函数 1 个 | 标签 几何:1
  示例: define_rectangle_by_diagonal
- &&% 定义矩形X: 函数 3 个 | 标签 几何:3
  示例: define_rectangle_by_diagonal_x, expand_rectangle, parse_rectangle_points
- &&&% 模型空间选出矩形多段线: 函数 1 个 | 标签 几何:1
  示例: get_rectangular_polylines
- &&%图纸空间矩形多段线: 函数 1 个 | 标签 几何:1
  示例: get_layout_rectangular_polylines_coords
- &&&%  分析打印线20260110: 函数 1 个 | 标签 几何:1
  示例: generate_name_and_ratio_from_com
- &&% 打印数据分析: 函数 5 个 | 标签 COM:1, 选择集:1
  示例: get_cad_app, get_dimensions, sort_coms_by_llcorner, main, generate_relation_list
- &&&% 选择标准打印区域: 函数 1 个 | 标签 几何:1
  示例: check_strict_standard_size
- &&%新版20260111: 函数 1 个 | 标签 无
  示例: check_strict_standard_size
- &&% 多段线排序: 函数 1 个 | 标签 几何:1
  示例: polyline_sort
- &&% 多段线转坐标: 函数 1 个 | 标签 几何:1
  示例: plcom_to_coor
- &&% 坐标转多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: plcoor_to_com
- &&% 判断竖向框: 函数 1 个 | 标签 几何:1
  示例: panduan_shuxiangkuang
- &&% 统一图幅: 函数 1 个 | 标签 无
  示例: tongyi_tufu
- &&% 简化多边形: 函数 1 个 | 标签 几何:1
  示例: simplify_polygon
- &&% 标准化多边形: 函数 1 个 | 标签 几何:1
  示例: normalize_polygon
- &&% 获取相邻点: 函数 1 个 | 标签 几何:1
  示例: get_adjacent_points
- &&% 点在多边形内: 函数 1 个 | 标签 几何:1
  示例: point_in_polygon
- &&% 线段相交: 函数 1 个 | 标签 无
  示例: line_segment_intersection_2d
- &&% 获取辅助点: 函数 1 个 | 标签 几何:1
  示例: get_auxiliary_point
- &&% 凹凸度量: 函数 1 个 | 标签 几何:1
  示例: concavity_measure
- &&% 凹凸角: 函数 1 个 | 标签 几何:1
  示例: concavity_angle
- &&% 水平分割六边形: 函数 1 个 | 标签 几何:1
  示例: split_orthogonal_hexagon
- &&% 竖向分割六边形: 函数 1 个 | 标签 几何:1
  示例: split_orthogonal_hexagon_vertical
- &&% 计算面积: 函数 1 个 | 标签 无
  示例: area_of
- &&% 综合分割六边形: 函数 1 个 | 标签 几何:1
  示例: split_hexagon_combined
- &&% 获取包围盒边: 函数 1 个 | 标签 COM:1, 几何:1
  示例: get_bbox_edge_segments
- &&% 获取多段线内文字: 函数 1 个 | 标签 几何:1
  示例: get_texts_in_polyline
- &&% 获取天正多行文字: 函数 1 个 | 标签 无
  示例: TDbMText_content
- &&% 实体均分点: 函数 1 个 | 标签 几何:1
  示例: distribute_points_on_entity
- &&% 判断线段包含: 函数 1 个 | 标签 无
  示例: is_segment_contained
- &&% 公共线段: 函数 1 个 | 标签 几何:1
  示例: common_segments_between_polylines
- &&% 矩形包含判断: 函数 1 个 | 标签 无
  示例: is_rect_inside_rect
- &&% 两多段线组矩形: 函数 1 个 | 标签 几何:1
  示例: two_plines_making_rectangle
- &&% 顶点全在内部: 函数 1 个 | 标签 几何:1
  示例: are_all_vertices_inside

## library/cad_objects.py
- &&&&%% 第四部分 一般对象: 函数 1 个 | 标签 选择集:1
  示例: ensure_list
- &&% 元组排序: 函数 1 个 | 标签 无
  示例: sort_tuples
- &&% 多维容差排序: 函数 3 个 | 标签 无
  示例: multi_dim_tolerance_sort, get_ll_pt, get_center
- &&% 实体位置排序: 函数 2 个 | 标签 无
  示例: sort_entities_by_position, get_line_start
- &&% 左下角排序: 函数 1 个 | 标签 无
  示例: sort_coms_by_llcorner
- &&% 右上角排序: 函数 1 个 | 标签 无
  示例: sort_coms_by_rbcorner
- &&% 自定义左下角排序: 函数 1 个 | 标签 无
  示例: sort_coms_by_llcorner_custom
- &&% 中心点排序: 函数 1 个 | 标签 几何:1
  示例: sort_coms_by_center
- &&% 实体编号: 函数 1 个 | 标签 无
  示例: number_entities_by_order
- &&% 列表遍历操作: 函数 1 个 | 标签 无
  示例: pr_list
- &&% 列表提取操作: 函数 1 个 | 标签 无
  示例: apply_to_each2
- &&% 获取对象群包围盒: 函数 1 个 | 标签 无
  示例: get_boundingbox_from_objects
- &&% 创建组: 函数 1 个 | 标签 无
  示例: chuangjian_zu
- &&% 获取组对象: 函数 1 个 | 标签 无
  示例: nametogroup
- &&% 获取所有组名: 函数 1 个 | 标签 COM:1
  示例: get_all_group_names
- &&% 获取所有组: 函数 1 个 | 标签 COM:1
  示例: get_all_groups
- &&% 添加对象到组: 函数 1 个 | 标签 无
  示例: add_objects_to_group
- &&% 添加单对象到组: 函数 1 个 | 标签 无
  示例: add_object_to_group
- &&% 移除组内对象: 函数 1 个 | 标签 COM:1
  示例: remove_object_from_group
- &&% 批量移除组内对象: 函数 1 个 | 标签 COM:1
  示例: remove_objects_from_group
- &&% 获取组内实体: 函数 1 个 | 标签 无
  示例: get_com_from_groupname
- &&% 获取组内实体分类: 函数 1 个 | 标签 无
  示例: get_com_from_groupname_by_type
- &&% 获取组内实体排序: 函数 1 个 | 标签 无
  示例: get_group_entities_sorted
- &&% 组内实体按中心排序: 函数 1 个 | 标签 几何:1
  示例: get_group_entities_sorted_by_type_and_bbox
- &&% 共有组实体排序: 函数 1 个 | 标签 几何:1
  示例: common_group_entities_sorted
- &&% 获取组包围盒: 函数 1 个 | 标签 无
  示例: get_boundingbox_from_group
- &&% 复制组S1: 函数 1 个 | 标签 COM:1
  示例: copy_group_S1_from_doc1_to_doc2
- &&% 句柄转对象: 函数 2 个 | 标签 无
  示例: HandleToObject, print_coms_handle
- &&% 批量句柄转对象: 函数 1 个 | 标签 无
  示例: handles_to_coms
- &&% 获取所有句柄: 函数 1 个 | 标签 无
  示例: get_all_handles
- &&% 查找实体: 函数 1 个 | 标签 无
  示例: find_entity_by_handle
- &&% 按类型句柄分组: 函数 1 个 | 标签 无
  示例: group_objects_by_type_and_handle
- &&% 记录类型句柄: 函数 1 个 | 标签 无
  示例: record_handle_with_type
- &&% 转换命名字典: 函数 1 个 | 标签 COM:1
  示例: convert_named_dict
- &&% 获取命名对象: 函数 1 个 | 标签 无
  示例: get_named_object
- &&% 绘制固定标签: 函数 1 个 | 标签 COM:1
  示例: draw_tags_on_objects_fixed
- &&% 标记天正门: 函数 1 个 | 标签 无
  示例: label_tarch_doors
- &&% 获取句柄映射: 函数 1 个 | 标签 无
  示例: get_handle_object_map
- &&% 设置扩展数据: 函数 1 个 | 标签 COM:1
  示例: set_xdata
- &&% 获取扩展数据: 函数 1 个 | 标签 COM:1
  示例: get_xdata
- &&% 设置打印标记: 函数 1 个 | 标签 无
  示例: set_xdata_tab
- &&% 检查打印标记: 函数 1 个 | 标签 无
  示例: is_printApp_xdata_com
- &&% 写CAD单行文字: 函数 1 个 | 标签 COM:1, 几何:1
  示例: write_cad_text
- &&% 写天正单行文字: 函数 1 个 | 标签 COM:1, 几何:1, 文件:1
  示例: write_tianzheng_text
- &&% 文字垂直对齐: 函数 1 个 | 标签 COM:1
  示例: align_text_to_vertical_line
- &&% 文字水平对齐: 函数 1 个 | 标签 COM:1
  示例: align_text_to_horizontal_line
- &&% 缩放天正文字: 函数 1 个 | 标签 COM:1
  示例: scale_tianzheng_text_to_cad
- &&% *** 将屏幕所选对象赋予到指定图层: 函数 1 个 | 标签 选择集:1
  示例: sc_objs_to_layer
- &&% 删除图层: 函数 1 个 | 标签 COM:1
  示例: delete_layer
- &&% 从列表创建图层: 函数 1 个 | 标签 无
  示例: create_layers_from_list
- &&% 从列表删除图层: 函数 1 个 | 标签 无
  示例: delete_layers_from_list
- &&% 逐点标注: 函数 1 个 | 标签 COM:1
  示例: dim_by_points
- &&% 确保图层存在并清空: 函数 1 个 | 标签 COM:1
  示例: ensure_layer
- &&% 只在模型空间上清理: 函数 1 个 | 标签 COM:1
  示例: ensure_layer_model_only
- &&% 确保图层当前: 函数 1 个 | 标签 无
  示例: ensure_layer_current
- &&% 设置图层属性: 函数 1 个 | 标签 COM:1
  示例: set_layer_properties
- &&% 将列表中的对象图层设为目标图层: 函数 1 个 | 标签 无
  示例: set_layer_with_retry
- &&% 强制改图层对象颜色: 函数 1 个 | 标签 无
  示例: force_layer_objects_color

## library/tarch_building.py
- : 函数 1 个 | 标签 无
  示例: dim_by_points
- &&% 绘制天正墙: 函数 1 个 | 标签 文件:1
  示例: draw_tarch_wall
- &&% 插入天正门: 函数 1 个 | 标签 文件:1
  示例: insert_tarch_door
- &&% 插入天正窗: 函数 1 个 | 标签 COM:1, 文件:1
  示例: insert_tarch_window
- &&% 获取天正房间: 函数 2 个 | 标签 文件:1
  示例: run_tupdspace_for_tz_room_in_rect, run_auto_TUPDSPACE_with_coord
- &&% 单线变墙: 函数 3 个 | 标签 无
  示例: TDb_single_line_variable_wall, convert_lines_to_walls, set_walls_thickness
- &&&% 基本函数: 函数 2 个 | 标签 窗口:2
  示例: activate_cad_middle_click, insert_tarch_window_lisp_mode
- &&&% 门类函数: 函数 5 个 | 标签 文件:3, 窗口:1
  示例: _get_dynamic_cache_path, _load_cache_from_disk, _save_cache_to_disk, _activate_cad_safe, _wait_for_user_hover
- &&% get_wall_thickness: 函数 1 个 | 标签 无
  示例: get_wall_thickness
- &&% get_wall_length: 函数 1 个 | 标签 无
  示例: get_wall_length
- &&% get_wall_height: 函数 1 个 | 标签 无
  示例: get_wall_height
- &&% modify_wall_thickness: 函数 1 个 | 标签 无
  示例: modify_wall_thickness
- &&% modify_wall_height: 函数 1 个 | 标签 无
  示例: modify_wall_height
- &&% modify_door_size: 函数 1 个 | 标签 无
  示例: modify_door_size
- &&% modify_window_size: 函数 1 个 | 标签 无
  示例: modify_window_size
- &&% delete_door: 函数 1 个 | 标签 无
  示例: delete_door
- &&% delete_window: 函数 1 个 | 标签 无
  示例: delete_window
- &&% insert_tarch_column: 函数 1 个 | 标签 无
  示例: insert_tarch_column
- &&% modify_column_size: 函数 1 个 | 标签 无
  示例: modify_column_size
- &&% insert_tarch_stair: 函数 1 个 | 标签 无
  示例: insert_tarch_stair
- &&% modify_stair_params: 函数 1 个 | 标签 无
  示例: modify_stair_params
- &&% label_room_name: 函数 2 个 | 标签 文件:1, 窗口:1
  示例: label_room_name, insert_tarch_door_universal

## scripts/CAD_basic.py
- &&&&%%  第一部分 导入连接: 函数 1 个 | 标签 无
  示例: _cad_safe_print
- &&% 控制函数运行时间: 函数 2 个 | 标签 无
  示例: _log, _kill_acad
- &&% 超时控制: 函数 2 个 | 标签 无
  示例: connect_database_task, safe_save_cad
- &&% 双重超时保护装饰器: 函数 2 个 | 标签 COM:1
  示例: timeout_and_log2, test_draw_circle_and_wait
- &&% 测试轮询等待: 函数 1 个 | 标签 无
  示例: wait_quiescent_ceshi
- &&% 测试PostCommand: 函数 1 个 | 标签 几何:1
  示例: complex_operation_demo
- &&% 测试卡住状态: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_infinite_spiral
- &&% 语音播报: 函数 1 个 | 标签 无
  示例: speak_msg
- &&% JSON数据读取存放设置: 函数 2 个 | 标签 COM:1
  示例: com_to_handle, serialize
- &&% 保存打印字典: 函数 1 个 | 标签 文件:1
  示例: save_print_dict_generic
- &&% 加载打印字典: 函数 3 个 | 标签 文件:3, COM:1
  示例: load, current_dwg_basename, current_dwg_folder
- &&% 数据类型转换函数: 函数 7 个 | 标签 COM:7
  示例: vtpnt, vtobj, vtFloat, vtInt, vtVariant, ConvertArrays2Variant, vtlist
- &&% 启动天正CAD及守护进程: 函数 2 个 | 标签 文件:1, COM:1, 窗口:1
  示例: start_applicationV9, force_show_cad_interface
- &&% 常规启动: 函数 2 个 | 标签 无
  示例: st, get_acad_process_id
- &&% 获取CAD进程数: 函数 1 个 | 标签 无
  示例: jingchengshu_wenjian
- &&% 关闭所有CAD进程: 函数 1 个 | 标签 无
  示例: close_all_cad_processes
- &&% 关闭最早CAD进程: 函数 2 个 | 标签 无
  示例: close_oldest_cad_process, ensure_typelib_from_running
- &&% 窗口缩放: 函数 1 个 | 标签 无
  示例: zoom_window
- &&&% RGB色彩: 函数 1 个 | 标签 无
  示例: aci_to_rgb
- &&% 获取实体RGB: 函数 1 个 | 标签 无
  示例: get_entity_rgb
- &&% 重复操作: 函数 1 个 | 标签 无
  示例: chongfu_caozuo
- &&% 简单计时器: 函数 1 个 | 标签 无
  示例: simple_timer
- &&&% 选择: 函数 3 个 | 标签 COM:2
  示例: _coinit_once, get_acad_doc, normalize_rect
- &&% 获取选择集包围盒: 函数 1 个 | 标签 几何:1
  示例: get_pmxz_group_bbox
- &&% 获取选择集包围盒别名: 函数 1 个 | 标签 几何:1
  示例: g
- &&% 最后对象对齐原点: 函数 2 个 | 标签 COM:2
  示例: align_last_ms_obj_lb_to_origin, get_entity_full_info
- &&% 计算直线角度: 函数 1 个 | 标签 几何:1
  示例: compute_line_angle
- &&% 绘制点: 函数 1 个 | 标签 无
  示例: draw_point
- &&% 绘制直线: 函数 1 个 | 标签 无
  示例: draw_line
- &&% 绘制圆: 函数 1 个 | 标签 无
  示例: draw_circle
- &&% 绘制正多边形: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_regular_polygon
- &&% 优先水平线: 函数 1 个 | 标签 无
  示例: prioritize_horizontal
- &&% 获取样条曲线长度: 函数 1 个 | 标签 COM:1, 几何:1
  示例: get_spline_length_by_conversion
- &&% 估算椭圆周长: 函数 1 个 | 标签 无
  示例: estimate_ellipse_length
- &&% 获取几何信息: 函数 1 个 | 标签 几何:1
  示例: get_entity_geometry_info
- &&% 直线定距点: 函数 1 个 | 标签 几何:1
  示例: points_on_line_at_distance_3d
- &&% 查找伪交点区域: 函数 1 个 | 标签 几何:1
  示例: find_fake_intersection_regions
- &&% 直线打断: 函数 1 个 | 标签 COM:1
  示例: lines_daduan
- &&% 删除重复直线: 函数 1 个 | 标签 无
  示例: delete_duplicate_lines
- &&% 删除冗余直线: 函数 1 个 | 标签 无
  示例: delete_redundant_lines
- &&% 查找孤立交点: 函数 1 个 | 标签 无
  示例: find_isolated_intersections
- &&% 获取多边形内点: 函数 1 个 | 标签 几何:1
  示例: get_inner_point_of_polygon
- &&% 获取房间轮廓: 函数 1 个 | 标签 COM:1
  示例: get_room_outline_from_point
- &&% 连接闭合多段线: 函数 1 个 | 标签 几何:1
  示例: connect_lines_to_polyline_if_closed
- &&% 判断闭合多边形: 函数 1 个 | 标签 几何:1
  示例: is_closed_polygon_from_lines
- &&% 判断同点: 函数 1 个 | 标签 无
  示例: same_point
- &&% 判断同线: 函数 1 个 | 标签 无
  示例: same_line
- &&% 计算绝对角度: 函数 1 个 | 标签 几何:1
  示例: calculate_absolute_angle
- &&% 计算相对角度: 函数 1 个 | 标签 几何:1
  示例: calculate_relative_angle
- &&% 按角度查找线段: 函数 1 个 | 标签 几何:1
  示例: find_lines_angle
- &&% 查找共点线段: 函数 1 个 | 标签 几何:1
  示例: find_lines_sharing_point
- &&% 查找最大转角后继线: 函数 1 个 | 标签 几何:1
  示例: find_successor_line_max
- &&% 查找右下角点: 函数 1 个 | 标签 无
  示例: find_rightbottom_point
- &&% 查找右下角闭合多边形: 函数 1 个 | 标签 几何:1
  示例: find_rightbottom_closed_polygon
- &&% 绘制多边形: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_polygon_as_polyline
- &&% 近似相等: 函数 1 个 | 标签 无
  示例: is_nearly_equal
- &&% 查找最小转角后继线: 函数 1 个 | 标签 几何:1
  示例: find_successor_line_min
- &&% 获取外轮廓: 函数 1 个 | 标签 几何:1
  示例: get_outer_contour
- &&% 顶点去重: 函数 1 个 | 标签 无
  示例: deduplicate_vertices
- &&% 分析多边形分支: 函数 1 个 | 标签 几何:1
  示例: analyze_polygon_branches
- &&% 移除指定顶点线段: 函数 1 个 | 标签 无
  示例: remove_lines_in_LBv
- &&% 处理多边形: 函数 1 个 | 标签 几何:1
  示例: process_polygons
- &&% 提取多边形: 函数 1 个 | 标签 几何:1
  示例: extract_polygon_from_lines
- &&% 炸开多段线: 函数 1 个 | 标签 几何:1
  示例: explode_polylines
- &&% 线段集相减: 函数 1 个 | 标签 无
  示例: subtract_line_sets
- &&% 最终处理: 函数 1 个 | 标签 几何:1
  示例: process_final
- &&% 绘制轻量多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_lwpolyline
- &&% 绘制轻量多段线20260113: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_lwpolyline
- &&% 获取唯一顶点: 函数 1 个 | 标签 几何:1
  示例: get_unique_vertices_from_pl_com
- &&% 线段转点集: 函数 1 个 | 标签 无
  示例: convert_lines_to_points
- &&% 合并线段: 函数 1 个 | 标签 无
  示例: merge_segments_new
- &&% 绘制多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_polyline
- &&% 线段转多段线: 函数 1 个 | 标签 几何:1
  示例: lines_to_polylines
- &&% 查找最小点: 函数 1 个 | 标签 无
  示例: find_min_point
- &&% 查找最大点: 函数 1 个 | 标签 无
  示例: find_max_point
- &&% 计算距离: 函数 1 个 | 标签 几何:1
  示例: distance
- &&% 定义矩形: 函数 1 个 | 标签 几何:1
  示例: define_rectangle_by_diagonal
- &&% 定义矩形X: 函数 3 个 | 标签 几何:3
  示例: define_rectangle_by_diagonal_x, expand_rectangle, parse_rectangle_points
- &&&% 模型空间选出矩形多段线: 函数 1 个 | 标签 几何:1
  示例: get_rectangular_polylines
- &&%图纸空间矩形多段线: 函数 1 个 | 标签 几何:1
  示例: get_layout_rectangular_polylines_coords
- &&&%  分析打印线20260110: 函数 1 个 | 标签 几何:1
  示例: generate_name_and_ratio_from_com
- &&% 打印数据分析: 函数 5 个 | 标签 COM:1, 选择集:1
  示例: get_cad_app, get_dimensions, sort_coms_by_llcorner, main, generate_relation_list
- &&&% 选择标准打印区域: 函数 1 个 | 标签 几何:1
  示例: check_strict_standard_size
- &&%新版20260111: 函数 1 个 | 标签 无
  示例: check_strict_standard_size
- &&% 多段线排序: 函数 1 个 | 标签 几何:1
  示例: polyline_sort
- &&% 多段线转坐标: 函数 1 个 | 标签 几何:1
  示例: plcom_to_coor
- &&% 坐标转多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: plcoor_to_com
- &&% 判断竖向框: 函数 1 个 | 标签 几何:1
  示例: panduan_shuxiangkuang
- &&% 统一图幅: 函数 1 个 | 标签 无
  示例: tongyi_tufu
- &&% 简化多边形: 函数 1 个 | 标签 几何:1
  示例: simplify_polygon
- &&% 标准化多边形: 函数 1 个 | 标签 几何:1
  示例: normalize_polygon
- &&% 获取相邻点: 函数 1 个 | 标签 几何:1
  示例: get_adjacent_points
- &&% 点在多边形内: 函数 1 个 | 标签 几何:1
  示例: point_in_polygon
- &&% 线段相交: 函数 1 个 | 标签 无
  示例: line_segment_intersection_2d
- &&% 获取辅助点: 函数 1 个 | 标签 几何:1
  示例: get_auxiliary_point
- &&% 凹凸度量: 函数 1 个 | 标签 几何:1
  示例: concavity_measure
- &&% 凹凸角: 函数 1 个 | 标签 几何:1
  示例: concavity_angle
- &&% 水平分割六边形: 函数 1 个 | 标签 几何:1
  示例: split_orthogonal_hexagon
- &&% 竖向分割六边形: 函数 1 个 | 标签 几何:1
  示例: split_orthogonal_hexagon_vertical
- &&% 计算面积: 函数 1 个 | 标签 无
  示例: area_of
- &&% 综合分割六边形: 函数 1 个 | 标签 几何:1
  示例: split_hexagon_combined
- &&% 获取包围盒边: 函数 1 个 | 标签 COM:1, 几何:1
  示例: get_bbox_edge_segments
- &&% 获取多段线内文字: 函数 1 个 | 标签 几何:1
  示例: get_texts_in_polyline
- &&% 获取天正多行文字: 函数 1 个 | 标签 无
  示例: TDbMText_content
- &&% 实体均分点: 函数 1 个 | 标签 几何:1
  示例: distribute_points_on_entity
- &&% 判断线段包含: 函数 1 个 | 标签 无
  示例: is_segment_contained
- &&% 公共线段: 函数 1 个 | 标签 几何:1
  示例: common_segments_between_polylines
- &&% 矩形包含判断: 函数 1 个 | 标签 无
  示例: is_rect_inside_rect
- &&% 两多段线组矩形: 函数 1 个 | 标签 几何:1
  示例: two_plines_making_rectangle
- &&% 顶点全在内部: 函数 1 个 | 标签 几何:1
  示例: are_all_vertices_inside
- &&&&%% 第四部分 一般对象: 函数 1 个 | 标签 选择集:1
  示例: ensure_list
- &&% 元组排序: 函数 1 个 | 标签 无
  示例: sort_tuples
- &&% 多维容差排序: 函数 3 个 | 标签 无
  示例: multi_dim_tolerance_sort, get_ll_pt, get_center
- &&% 实体位置排序: 函数 2 个 | 标签 无
  示例: sort_entities_by_position, get_line_start
- &&% 左下角排序: 函数 1 个 | 标签 无
  示例: sort_coms_by_llcorner
- &&% 右上角排序: 函数 1 个 | 标签 无
  示例: sort_coms_by_rbcorner
- &&% 自定义左下角排序: 函数 1 个 | 标签 无
  示例: sort_coms_by_llcorner_custom
- &&% 中心点排序: 函数 1 个 | 标签 几何:1
  示例: sort_coms_by_center
- &&% 实体编号: 函数 1 个 | 标签 无
  示例: number_entities_by_order
- &&% 列表遍历操作: 函数 1 个 | 标签 无
  示例: pr_list
- &&% 列表提取操作: 函数 1 个 | 标签 无
  示例: apply_to_each2
- &&% 获取对象群包围盒: 函数 1 个 | 标签 无
  示例: get_boundingbox_from_objects
- &&% 创建组: 函数 1 个 | 标签 无
  示例: chuangjian_zu
- &&% 获取组对象: 函数 1 个 | 标签 无
  示例: nametogroup
- &&% 获取所有组名: 函数 1 个 | 标签 COM:1
  示例: get_all_group_names
- &&% 获取所有组: 函数 1 个 | 标签 COM:1
  示例: get_all_groups
- &&% 添加对象到组: 函数 1 个 | 标签 无
  示例: add_objects_to_group
- &&% 添加单对象到组: 函数 1 个 | 标签 无
  示例: add_object_to_group
- &&% 移除组内对象: 函数 1 个 | 标签 COM:1
  示例: remove_object_from_group
- &&% 批量移除组内对象: 函数 1 个 | 标签 COM:1
  示例: remove_objects_from_group
- &&% 获取组内实体: 函数 1 个 | 标签 无
  示例: get_com_from_groupname
- &&% 获取组内实体分类: 函数 1 个 | 标签 无
  示例: get_com_from_groupname_by_type
- &&% 获取组内实体排序: 函数 1 个 | 标签 无
  示例: get_group_entities_sorted
- &&% 组内实体按中心排序: 函数 1 个 | 标签 几何:1
  示例: get_group_entities_sorted_by_type_and_bbox
- &&% 共有组实体排序: 函数 1 个 | 标签 几何:1
  示例: common_group_entities_sorted
- &&% 获取组包围盒: 函数 1 个 | 标签 无
  示例: get_boundingbox_from_group
- &&% 复制组S1: 函数 1 个 | 标签 COM:1
  示例: copy_group_S1_from_doc1_to_doc2
- &&% 句柄转对象: 函数 2 个 | 标签 无
  示例: HandleToObject, print_coms_handle
- &&% 批量句柄转对象: 函数 1 个 | 标签 无
  示例: handles_to_coms
- &&% 获取所有句柄: 函数 1 个 | 标签 无
  示例: get_all_handles
- &&% 查找实体: 函数 1 个 | 标签 无
  示例: find_entity_by_handle
- &&% 按类型句柄分组: 函数 1 个 | 标签 无
  示例: group_objects_by_type_and_handle
- &&% 记录类型句柄: 函数 1 个 | 标签 无
  示例: record_handle_with_type
- &&% 转换命名字典: 函数 1 个 | 标签 COM:1
  示例: convert_named_dict
- &&% 获取命名对象: 函数 1 个 | 标签 无
  示例: get_named_object
- &&% 绘制固定标签: 函数 1 个 | 标签 COM:1
  示例: draw_tags_on_objects_fixed
- &&% 标记天正门: 函数 1 个 | 标签 无
  示例: label_tarch_doors
- &&% 获取句柄映射: 函数 1 个 | 标签 无
  示例: get_handle_object_map
- &&% 设置扩展数据: 函数 1 个 | 标签 COM:1
  示例: set_xdata
- &&% 获取扩展数据: 函数 1 个 | 标签 COM:1
  示例: get_xdata
- &&% 设置打印标记: 函数 1 个 | 标签 无
  示例: set_xdata_tab
- &&% 检查打印标记: 函数 1 个 | 标签 无
  示例: is_printApp_xdata_com
- &&% 写CAD单行文字: 函数 1 个 | 标签 COM:1, 几何:1
  示例: write_cad_text
- &&% 写天正单行文字: 函数 1 个 | 标签 COM:1, 几何:1, 文件:1
  示例: write_tianzheng_text
- &&% 文字垂直对齐: 函数 1 个 | 标签 COM:1
  示例: align_text_to_vertical_line
- &&% 文字水平对齐: 函数 1 个 | 标签 COM:1
  示例: align_text_to_horizontal_line
- &&% 缩放天正文字: 函数 1 个 | 标签 COM:1
  示例: scale_tianzheng_text_to_cad
- &&% *** 将屏幕所选对象赋予到指定图层: 函数 1 个 | 标签 选择集:1
  示例: sc_objs_to_layer
- &&% 删除图层: 函数 1 个 | 标签 COM:1
  示例: delete_layer
- &&% 从列表创建图层: 函数 1 个 | 标签 无
  示例: create_layers_from_list
- &&% 从列表删除图层: 函数 1 个 | 标签 无
  示例: delete_layers_from_list
- &&% 逐点标注: 函数 1 个 | 标签 COM:1
  示例: dim_by_points
- &&% 确保图层存在并清空: 函数 1 个 | 标签 COM:1
  示例: ensure_layer
- &&% 只在模型空间上清理: 函数 1 个 | 标签 COM:1
  示例: ensure_layer_model_only
- &&% 确保图层当前: 函数 1 个 | 标签 无
  示例: ensure_layer_current
- &&% 设置图层属性: 函数 1 个 | 标签 COM:1
  示例: set_layer_properties
- &&% 将列表中的对象图层设为目标图层: 函数 1 个 | 标签 无
  示例: set_layer_with_retry
- &&% 强制改图层对象颜色: 函数 1 个 | 标签 无
  示例: force_layer_objects_color
- &&% 从文本构建J点: 函数 1 个 | 标签 无
  示例: build_J_points_from_selected_texts
- &&% 坐标转经纬度: 函数 1 个 | 标签 无
  示例: convert_pts_dict_to_latlon
- &&% 显示隐藏图形: 函数 1 个 | 标签 COM:1
  示例: xianshi_yincangtuxing
- &&% 运行CAD程序: 函数 1 个 | 标签 COM:1
  示例: run_cad_program
- &&% 自动化T7窗口: 函数 1 个 | 标签 COM:1
  示例: automate_window_with_pywinauto_t7
- &&% 转成T7: 函数 1 个 | 标签 无
  示例: zhuancheng_t7
- &&% 自动化T3窗口: 函数 1 个 | 标签 COM:1
  示例: automate_window_with_pywinauto_t3
- &&% 转成T3: 函数 1 个 | 标签 无
  示例: zhuancheng_t3
- &&% 确保文件被删除: 函数 1 个 | 标签 文件:1
  示例: ensure_file_absent
- &&% 遍历目录: 函数 1 个 | 标签 文件:1
  示例: traverse_with_os_walk
- &&% 按后缀查找文件: 函数 1 个 | 标签 文件:1
  示例: find_files_with_extensions
- &&% 获取无后缀文件名: 函数 1 个 | 标签 文件:1
  示例: get_filename_without_extension
- &&% 按模式删除文件: 函数 1 个 | 标签 文件:1
  示例: delete_files_with_patterns
- &&% 清除指定前缀文件: 函数 1 个 | 标签 文件:1
  示例: clear_files_with_prefix
- &&% 按字符串查找文件: 函数 1 个 | 标签 无
  示例: find_files_with_string
- &&% 路径拼接: 函数 1 个 | 标签 文件:1
  示例: join_paths
- &&% 获取块实例块名: 函数 1 个 | 标签 无
  示例: get_block_name
- &&% 获取块属性值: 函数 1 个 | 标签 无
  示例: huoqukuai_shuxing_zhi
- &&% 属性块标签编辑: 函数 2 个 | 标签 COM:1
  示例: update_block_def_attributes_safe, update_block_def_attributes_v7
- &&% 属性块标签编辑生效: 函数 2 个 | 标签 COM:1
  示例: attsync_block_instance, attsync_block_instance_base
- &&% 设置属性块的标签值: 函数 1 个 | 标签 无
  示例: set_attribute_mtext
- &&% 获取属性块标签及标签值: 函数 1 个 | 标签 无
  示例: get_block_attributes_dict
- &&% 筛选出指定块名外的对象: 函数 1 个 | 标签 无
  示例: separate_entities_by_block_names
- &&% 获取块内多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: huoqu_kuai_pl
- &&% 创建带基点块: 函数 1 个 | 标签 COM:1
  示例: create_block_with_basepoint
- &&% 创建三角形文字块: 函数 2 个 | 标签 COM:2, 几何:2
  示例: create_block_with_triangle_and_text, huoqu_kuai_pl
- &&% 获取块包围盒: 函数 1 个 | 标签 COM:1
  示例: get_bounding_box_of_block
- &&% 创建含插入和直线的块: 函数 1 个 | 标签 COM:1
  示例: create_new_block_with_insert_and_line
- &&% 复制并移动图层块: 函数 1 个 | 标签 COM:1
  示例: copy_and_move_blocks_from_layer
- &&% 旧版: 函数 1 个 | 标签 无
  示例: delete_block_instances_and_definition_retry
- &&% 极速清理: 函数 1 个 | 标签 COM:1, 选择集:1
  示例: delete_block_instances_and_definition_optimized
- &&% 再次优化: 函数 1 个 | 标签 COM:1, 选择集:1
  示例: delete_block_instances_and_definition_optimized
- &&% 重命名块实体: 函数 1 个 | 标签 无
  示例: rename_block_entity
- &&% 由块名选择实例: 函数 1 个 | 标签 无
  示例: get_block_instances
- &&% 获取块引用实体: 函数 1 个 | 标签 无
  示例: get_entities_from_block_reference
- &&% 插入块到CAD: 函数 1 个 | 标签 无
  示例: insert_block_into_autocad
- &&% 插入标准块: 函数 1 个 | 标签 COM:1, 文件:1
  示例: insert_standard_block
- &&% 插入并炸开DWG: 函数 1 个 | 标签 COM:1, 几何:1, 文件:1
  示例: insert_and_explode_dwg
- &&% 新版本性能测试0109: 函数 1 个 | 标签 COM:1, 文件:1
  示例: insert_and_explode_dwg
- &&% 获取大块实例: 函数 1 个 | 标签 无
  示例: get_large_block_instances
- &&% 确定合乎标准打印要求的自建多段线区域: 函数 1 个 | 标签 无
  示例: get_large_block_instances_with_tolerance
- &&% 块内坐标转换成世界坐标（适合平面上的一般块）: 函数 1 个 | 标签 无
  示例: transform_point_by_block
- &&% 按名称选择块: 函数 1 个 | 标签 选择集:1
  示例: select_block_by_name
- &&% 获取所有块定义: 函数 1 个 | 标签 COM:1
  示例: get_all_block_definitions
- &&% 获取所有块名: 函数 1 个 | 标签 COM:1
  示例: get_all_block_names
- &&% 块清理: 函数 1 个 | 标签 COM:1
  示例: purge_block
- &&% 清理未使用块: 函数 1 个 | 标签 COM:1, 选择集:1
  示例: purge_unused_blocks
- &&% 清理块1: 函数 1 个 | 标签 COM:1
  示例: purge_block_1
- &&% 清理未使用块1: 函数 1 个 | 标签 COM:1
  示例: purge_unused_blocks_1
- &&% 预留新插入块名: 函数 1 个 | 标签 COM:1
  示例: reserve_block_names_for_new_insert
- &&% 获取选定块引用名: 函数 1 个 | 标签 无
  示例: get_selected_blockreference_names
- &&% 从区域创建CAD块: 函数 1 个 | 标签 COM:1, 几何:1
  示例: create_block_from_region_cad
- &&% 从区域创建CMD块: 函数 1 个 | 标签 COM:1, 选择集:1, 几何:1
  示例: create_block_from_region_cmd
- &&% 从列表对象创建块: 函数 1 个 | 标签 COM:1, 几何:1
  示例: create_block_from_list_cmd
- &&% 获取块内实体: 函数 1 个 | 标签 COM:1
  示例: get_block_contents_at_same_location
- &&% 添加实体到块: 函数 2 个 | 标签 COM:2, 几何:1
  示例: add_entities_to_block_direct, add_entities_to_block_definition_explode
- &&% 重定义块内容: 函数 1 个 | 标签 COM:1, 文件:1
  示例: redefine_block_with_entities
- &&% 提取非块实体: 函数 1 个 | 标签 几何:1
  示例: extract_specific_entities_from_block
- &&% 确保简单炸开块: 函数 3 个 | 标签 COM:1
  示例: safe_explode, _atomic_explode_and_delete, safe_explode_retry
- &&% 炸开对象并回溯: 函数 1 个 | 标签 COM:1
  示例: explode_single_object_marker
- &&% 安全炸开并删除: 函数 1 个 | 标签 无
  示例: safe_explode_and_delete
- &&% 清理缓存: 函数 1 个 | 标签 COM:1, 文件:1
  示例: fix_com_cache
- &&% 清除nul: 函数 1 个 | 标签 文件:1
  示例: delete_all_nul_under_folder
- &&% 终止弹窗程序: 函数 1 个 | 标签 文件:1
  示例: kill_dialog_killer
- &&% 终止指定py脚本 (psutil版): 函数 1 个 | 标签 无
  示例: kill_python_script_by_name
- &&% 结束WPS进程: 函数 1 个 | 标签 无
  示例: kill_wps
- &&%关闭excel进程: 函数 1 个 | 标签 无
  示例: close_all_excel_processes
- &&&% 确保安全删除: 函数 1 个 | 标签 无
  示例: safe_delete
- &&% 区域实体移动: 函数 1 个 | 标签 选择集:1
  示例: move_entities_in_region
- &&% 设置点样式: 函数 1 个 | 标签 无
  示例: 圆点
- &&% 设置图纸背景色: 函数 1 个 | 标签 无
  示例: 图纸背景
- &&% 视图区域缩放: 函数 1 个 | 标签 COM:1
  示例: shitu_region
- &&% 视图实体缩放: 函数 1 个 | 标签 COM:1
  示例: shitu_entity
- &&% 录制屏幕GIF: 函数 1 个 | 标签 无
  示例: record_screen_gif
- &&% 最小化所有窗口: 函数 1 个 | 标签 窗口:1
  示例: minimize_all_windows
- &&% CAD窗口置左上: 函数 1 个 | 标签 无
  示例: set_autocad_window_to_top_left
- &&% CAD窗口置左上别名: 函数 1 个 | 标签 无
  示例: l
- &&% 最小化窗口Win+D: 函数 1 个 | 标签 窗口:1
  示例: minimize_all_windows_d
- &&% 最小化窗口Win+M: 函数 1 个 | 标签 窗口:1
  示例: minimize_all_windows_m
- &&% 恢复并定位窗口: 函数 1 个 | 标签 无
  示例: restore_and_position
- &&% 列出打开窗口标题: 函数 1 个 | 标签 无
  示例: list_open_window_titles
- &&% 测鼠标位置: 函数 1 个 | 标签 无
  示例: ceshubiao_weizhi
- &&% 后台运行IDLE: 函数 1 个 | 标签 文件:1
  示例: run_idle_background
- &&% 点击并拖动: 函数 1 个 | 标签 无
  示例: click_and_drag
- &&% 点击并找图: 函数 1 个 | 标签 文件:1
  示例: click_and_find_image_shape
- &&% 右键点击并移动: 函数 1 个 | 标签 无
  示例: right_click_and_move
- &&% 结束所有IDLE进程: 函数 1 个 | 标签 无
  示例: kill_all_idle
- &&% IDLE窗口置右上: 函数 2 个 | 标签 无
  示例: set_idle_window_to_top_right, r
- &&% OBS窗口置右下: 函数 2 个 | 标签 无
  示例: place_obs_bottom_right, r2
- &&% 最小化指定窗口: 函数 1 个 | 标签 无
  示例: minimize_window
- &&% 最大化CAD窗口: 函数 1 个 | 标签 窗口:1
  示例: maximize_autocad_window
- &&% 点击开始OBS录制: 函数 1 个 | 标签 无
  示例: start_obs_recording_by_click
- &&% 发送微信: 函数 1 个 | 标签 无
  示例: fs
- &&% 选微信群: 函数 1 个 | 标签 无
  示例: xuanqun
- &&% 复制到剪贴板: 函数 1 个 | 标签 无
  示例: copy_to_clipboard
- &&% 写微信: 函数 1 个 | 标签 无
  示例: xieweixin
- &&% 主操作函数: 函数 1 个 | 标签 无
  示例: 主操作函数
- &&% 主函数入口: 函数 1 个 | 标签 无
  示例: main_func
- &&% 录屏: 函数 1 个 | 标签 无
  示例: luping
- &&% 魔方: 函数 1 个 | 标签 无
  示例: 魔方
- &&% 运行Python脚本: 函数 1 个 | 标签 无
  示例: run_py
- &&% 聚焦命令行: 函数 1 个 | 标签 无
  示例: focus_cmdline
- &&% 激活窗口和子窗口: 函数 1 个 | 标签 窗口:1
  示例: activate_window_by_title
- &&% 窗口内点击: 函数 1 个 | 标签 窗口:1
  示例: click_in_window
- &&% 激活并点击艾可云: 函数 1 个 | 标签 无
  示例: activate_and_click_aikeyun
- &&% 窗口内简单拖拽: 函数 1 个 | 标签 无
  示例: drag_in_window_simple
- &&% 纯窗口操作炸开区域内对象: 函数 1 个 | 标签 文件:1
  示例: run_auto_explode_area
- &&% 列出所有窗口: 函数 3 个 | 标签 窗口:1
  示例: list_all_windows, minimize_window, maximize_autocad_window
- &&% 设置单位精度: 函数 2 个 | 标签 无
  示例: set_dwg_units_precision, jd
- &&% 列出标注样式: 函数 1 个 | 标签 无
  示例: list_dim_styles
- &&% 设置当前标注样式: 函数 1 个 | 标签 COM:1
  示例: set_current_dimstyle_via_command
- &&% 设置当前文字样式: 函数 1 个 | 标签 无
  示例: set_current_text_style
- &&% 获取字体样式: 函数 1 个 | 标签 无
  示例: huoqu_ziti_style
- &&% 创建文字样式: 函数 1 个 | 标签 无
  示例: create_text_style
- &&% 设置SHX文字样式: 函数 1 个 | 标签 COM:1
  示例: set_text_style_onlyshx
- &&% 设置文字样式: 函数 1 个 | 标签 无
  示例: set_text_style
- &&% 重命名冲突文字样式: 函数 1 个 | 标签 COM:1, 文件:1
  示例: rename_conflicting_text_styles
- &&% 格式刷属性传递: 函数 1 个 | 标签 COM:1, 几何:1
  示例: transfer_props_by_matchprop
- &&% 双线程运行1: 函数 1 个 | 标签 COM:1
  示例: run_dual_threads_1
- &&% 取消CAD选择: 函数 1 个 | 标签 无
  示例: cancel_cad_selection
- &&&% 打印辅助: 函数 1 个 | 标签 窗口:1
  示例: close_wps_window_by_click
- &&% 最小化窗口: 函数 1 个 | 标签 窗口:1
  示例: min_w
- &&% 清除测试图层: 函数 1 个 | 标签 无
  示例: ql
- &&% 模型空间画点: 函数 1 个 | 标签 无
  示例: srhd
- &&% 图纸空间画点: 函数 1 个 | 标签 无
  示例: srhd_p
- &&% COM点转数学点: 函数 2 个 | 标签 无
  示例: comtomath, p
- &&% 复制查看: 函数 1 个 | 标签 无
  示例: fuzhi_chakan
- &&% 测量文字长度: 函数 1 个 | 标签 无
  示例: celiang_wenzichangdu
- &&% 写入并测量文字长度: 函数 1 个 | 标签 无
  示例: celiang_wenzichangdu_write
- &&% 清空文件夹: 函数 1 个 | 标签 文件:1
  示例: qingkong_wenjianjia
- &&% 获取包围盒信息: 函数 1 个 | 标签 几何:1
  示例: get_bbox_info
- &&% 包围盒方向标志: 函数 1 个 | 标签 几何:1
  示例: bbox_orientation_flag
- &&% 获取多个对象的外包盒数据: 函数 1 个 | 标签 COM:1, 几何:1
  示例: group_bbox_corners
- &&% 包围盒中心2D: 函数 1 个 | 标签 几何:1
  示例: bbox_center_2
- &&% 包围盒中心3D: 函数 1 个 | 标签 几何:1
  示例: bbox_center_3
- &&% 安全获取包围盒: 函数 1 个 | 标签 COM:1, 几何:1
  示例: safe_get_bbox
- &&% 调试风格规范: 函数 1 个 | 标签 无
  示例: resolve_log_level
- &&% 数据处理中心: 函数 4 个 | 标签 文件:2, COM:2, 几何:2
  示例: get_data_root, _resolve_json_path, extract_poly_data, restore_poly_adaptive
- &&% 多段线列表信息存取: 函数 2 个 | 标签 文件:2
  示例: save_poly_list, load_poly_list
- &&% ctq信息存取: 函数 2 个 | 标签 文件:2, COM:1
  示例: save_ctq, load_ctq
- &&% 重定义标准图签文件中的核心块: 函数 1 个 | 标签 文件:1
  示例: Redefine_standard_blocks
- &&% 图名排序: 函数 1 个 | 标签 COM:1, 几何:1
  示例: get_sorted_titles_by_areas_final
- &&% 选择测试: 函数 1 个 | 标签 COM:1, 几何:1
  示例: get_sorted_titles_ce
- &&% 编辑块生效的强化: 函数 1 个 | 标签 无
  示例: batch_attsync_loop
- &&% 统一选择: 函数 2 个 | 标签 几何:2, 文件:1
  示例: smart_select_polylines, universal_select_polylines
- &&% 模型空间极大矩形选择打印区域: 函数 2 个 | 标签 几何:2
  示例: select_print_areas_maxrect_from_polylines, select_maxrect_polylines_1
- &&% 图纸空间打印区域的选择: 函数 1 个 | 标签 COM:1, 几何:1
  示例: select_print_areas_paperspace
- &&% 标准框选择打印区域: 函数 1 个 | 标签 几何:1
  示例: select_standard_print_areas
- &&% 从指定图层列表的图块建立打印区域: 函数 1 个 | 标签 几何:1
  示例: select_print_areas_from_blocks
- &&% 从指定图层获得打印区域: 函数 1 个 | 标签 几何:1
  示例: select_print_areas_from_layer
- &&% 从屏幕选择获得打印区域: 函数 2 个 | 标签 几何:2
  示例: select_print_areas_from_screen, check_valid_rect_pro
- &&% 对多段线去重处理: 函数 1 个 | 标签 几何:1
  示例: remove_duplicate_polylines
- &&% 统一插图签: 函数 1 个 | 标签 几何:1
  示例: universal_insert_labels_dispatch
- &&% 幂等增强插入加速版: 函数 1 个 | 标签 几何:1, 文件:1
  示例: insert_and_scale_labels_area_power
- &&% 图纸空间的图签插入: 函数 2 个 | 标签 无
  示例: insert_and_scale_labels_paper_space, clean_blocks_until_vanished
- &&% 坐标转多段线COM: 函数 1 个 | 标签 COM:1, 几何:1
  示例: plcoor_to_com
- &&% 绘制PL并提取信息: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_pl_and_extract_info
- &&% 从实体绘制PL并提取: 函数 1 个 | 标签 COM:1
  示例: draw_pl_and_extract_from_entities
- &&% 区域内插入块: 函数 1 个 | 标签 COM:1
  示例: insert_block_into_poly_area
- &&% 区域内插入块20260109: 函数 1 个 | 标签 COM:1
  示例: insert_block_into_poly_area
- &&% 计算插入因子: 函数 1 个 | 标签 无
  示例: compute_insert_factors
- &&% 获取实体因子: 函数 1 个 | 标签 无
  示例: get_factor_for_entity
- &&% 插入公司通用图签单线程: 函数 1 个 | 标签 无
  示例: insert_company_label_common_block
- &&% 线程1:插入公司图签: 函数 3 个 | 标签 COM:1, 窗口:2
  示例: f1_insert_company_getwindow, _find_shx_dialog, _ignore_shx_dialog
- &&% 线程2:删除窗口: 函数 2 个 | 标签 COM:1
  示例: f2_delwindow, run_dual_threads
- &&% 插入公司通用图签(双线程): 函数 1 个 | 标签 无
  示例: Insert_Company_Label_Common_Block
- &&% 清理内部多段线: 函数 4 个 | 标签 COM:1, 几何:2
  示例: clean_internal_polylines, fill_block_attributes_with_tag_name, _make_bind_dict_serializable, normalize_core_title_blocks_by_layer
- &&% 炸开图签壳块: 函数 1 个 | 标签 COM:1
  示例: explode_title_wrappers_to_core_layer
- &&% 模型空间修复插入: 函数 1 个 | 标签 几何:1
  示例: repair_mp_insert
- &&% 图纸空间样式修复插入: 函数 1 个 | 标签 几何:1
  示例: repair_sp_insert
- &&% 线宽修复: 函数 2 个 | 标签 几何:2
  示例: smart_repair_frame_polyline_widths_m, smart_repair_frame_polyline_widths_p
- &&% 从模型空间剪切到图纸空间: 函数 2 个 | 标签 COM:2, 选择集:1, 文件:1
  示例: cut_model_to_paper_and_switch, _fallback_copy_method
- &&% 从模型空间屏幕选择对象复制到图纸空间: 函数 1 个 | 标签 无
  示例: cut_screen_selection_to_paper
- &&% 从图纸空间复制打印区域到模型空间: 函数 1 个 | 标签 COM:1, 几何:1
  示例: copy_layout_polylines_to_model
- &&% 清空图纸空间: 函数 1 个 | 标签 COM:1
  示例: clear_layout_objects
- &&% 清除无实例块: 函数 1 个 | 标签 无
  示例: clean_unused_blocks_global_scan
- &&% 统一重建字典: 函数 1 个 | 标签 文件:1
  示例: smart_rebuild_print_info
- &&% 重建字典_模型空间: 函数 1 个 | 标签 几何:1
  示例: rebuild_print_area_title_mapping
- &&% 重建字典_图纸空间: 函数 1 个 | 标签 无
  示例: rebuild_print_area_title_mapping_paper
- &&% 构建表头映射: 函数 1 个 | 标签 无
  示例: build_header_map
- &&% 读取Excel到字典: 函数 1 个 | 标签 无
  示例: read_xlsx_to_dict
- &&% 写入字典到Excel: 函数 1 个 | 标签 文件:1
  示例: write_dict_to_xlsx
- &&% 自动导出: 函数 1 个 | 标签 无
  示例: auto_export_excel_with_fallback
- &&% 基础导出: 函数 1 个 | 标签 COM:1, 文件:1
  示例: build_full_print_dict_and_export_excel
- &&% 自动_图名标注写入图签: 函数 1 个 | 标签 无
  示例: auto_process_drawing_names_by_style
- &&% 基础_图名标注写入图签: 函数 1 个 | 标签 无
  示例: process_drawing_names_and_fill_titleblocks
- &&% 自动写入: 函数 1 个 | 标签 无
  示例: auto_import_excel_to_cad
- &&% 基础写入: 函数 1 个 | 标签 COM:1, 文件:1
  示例: read_excel_and_update_cad_titleblocks
- &&% 自动_修改图块标签属性: 函数 1 个 | 标签 无
  示例: auto_update_titleblock_format_by_style
- &&% 基础_修改图块标签属性: 函数 1 个 | 标签 无
  示例: batch_update_block_attributes_config
- &&% 统一编目录1: 函数 1 个 | 标签 几何:1, 文件:1
  示例: bianmulu_func1_h
- &&% 编目录2_统一: 函数 1 个 | 标签 几何:1, 文件:1
  示例: bianmulu_func2_h
- &&% 编好目录: 函数 1 个 | 标签 文件:1
  示例: bianmulu_func3_h
- &&% 合并: 函数 1 个 | 标签 COM:1, 几何:1, 文件:1
  示例: bianmulu_func4_h
- &&% 写入目录图签: 函数 2 个 | 标签 COM:2, 文件:2
  示例: update_catalog_titleblocks_from_excel, update_catalog_titleblocks_from_excel_y
- &&% 从excel写入目录dwg文件: 函数 1 个 | 标签 COM:1, 文件:1
  示例: write_catalog_from_excel_to_cad
- &&% 读取目录结构的excel文件: 函数 1 个 | 标签 COM:1, 文件:1
  示例: read_catalog_template_config
- &&% 将目录dwg文件合并到主文件: 函数 1 个 | 标签 COM:1, 文件:1
  示例: get_my_template_config_from_excel
- &&% 文件名修改1: 函数 1 个 | 标签 文件:1
  示例: rename_drawings
- &&% 模拟键盘调整打印图幅: 函数 3 个 | 标签 无
  示例: get_mouse_target_v3, safe_input_text, auto_setup_custom_paper_sizes
- &&% 获取当前图幅尺寸: 函数 1 个 | 标签 COM:1
  示例: list_current_printer_papers
- &&% 配置字体: 函数 3 个 | 标签 文件:1
  示例: replace_cad_fonts_incremental, is_admin, sanitize_filename
- &&% 模型空间窗口打印: 函数 1 个 | 标签 几何:1, 文件:1
  示例: export_model_window_pure
- &&% 模型空间LISP窗口打印export_model_window_lisp_fit: 函数 1 个 | 标签 COM:1, 几何:1, 文件:1
  示例: export_model_window_lisp_fit
- &&% 图纸空间窗口打印: 函数 1 个 | 标签 文件:1
  示例: export_layout_window_pure
- &&% 图纸空间打印边距修正版备用: 函数 1 个 | 标签 文件:1
  示例: export_layout_window_pure_bianju
- &&% 布局空间LISP窗口打印: 函数 2 个 | 标签 COM:2, 文件:2
  示例: export_layout_window_lisp_fit_v1, export_layout_window_lisp_fit
- &&% 文件夹打印: 函数 1 个 | 标签 文件:1
  示例: print_batch_custom_list
- &&% 典型文件的绘制: 函数 1 个 | 标签 几何:1
  示例: mark_print_areas_final
- &&% 生成图名标注: 函数 1 个 | 标签 COM:1, 几何:1
  示例: generate_tarch_drawing_names_v5
- &&% 模型空间文件打印: 函数 1 个 | 标签 几何:1, 文件:1
  示例: print_dwg_file_model
- &&% 模型空间批量打印: 函数 1 个 | 标签 几何:1, 文件:1, 窗口:1
  示例: print_polylines_list
- &&% 图纸空间文件打印: 函数 1 个 | 标签 几何:1, 文件:1
  示例: print_dwg_file_layout
- &&% 图纸空间列表打印: 函数 2 个 | 标签 COM:1, 几何:2, 文件:2, 窗口:1
  示例: print_layout_polylines_list, print_layout_polylines_list_y
- &&% 统一打印: 函数 1 个 | 标签 无
  示例: smart_print_dispatch

## scripts/函数编写规范.py
- : 函数 4 个 | 标签 COM:2
  示例: li, get_acad_doc, _coinit_once, com_retry
- &&% 按图层选择: 函数 1 个 | 标签 COM:1, 选择集:1
  示例: select_tuceng
- &&% 图层选择别名: 函数 1 个 | 标签 无
  示例: stc
- &&% 选择所有块: 函数 1 个 | 标签 COM:1, 选择集:1
  示例: select_kuai
- &&% 选择所有文本: 函数 1 个 | 标签 选择集:1
  示例: select_text
- &&% 选择所有多行文本: 函数 1 个 | 标签 选择集:1
  示例: select_mtext
- &&% 选择天正文本: 函数 1 个 | 标签 无
  示例: select_pub_text_entities
- &&% 收集所有文本: 函数 1 个 | 标签 无
  示例: collect_all_texts
- &&% 选择直线: 函数 1 个 | 标签 选择集:1
  示例: select_line
- &&% 选择圆: 函数 1 个 | 标签 选择集:1
  示例: select_circle
- &&% 选择椭圆: 函数 1 个 | 标签 选择集:1
  示例: select_ellipse
- &&% 选择样条曲线: 函数 1 个 | 标签 选择集:1
  示例: select_spline
- &&% 选择传统多段线: 函数 1 个 | 标签 COM:1, 选择集:1, 几何:1
  示例: select_polyline_chuantong
- &&% 选择轻量多段线: 函数 3 个 | 标签 COM:2, 选择集:1, 几何:1
  示例: select_polyline, normalize_rect, pt3
- &&% 隐显结合的区域选择（高亮选择并返回 PickfirstSelectionSet）: 函数 1 个 | 标签 COM:1, 选择集:1
  示例: select_entities_in_window
- &&% 让对象处于夹点编辑状态: 函数 1 个 | 标签 COM:1
  示例: set_entity_grip_state_precise
- &&% 安全获取包围盒: 函数 1 个 | 标签 COM:1, 几何:1
  示例: safe_get_bbox
- &&% 安全转换COM对象: 函数 1 个 | 标签 无
  示例: _maybe_cast
- &&% 转换对象: 函数 1 个 | 标签 无
  示例: cast_object
- &&% 获取对象属性: 函数 1 个 | 标签 COM:1
  示例: get_object_property
- &&% 设置对象属性: 函数 1 个 | 标签 COM:1
  示例: set_object_property
- &&% 安全获取属性: 函数 1 个 | 标签 无
  示例: get_attr
- &&% 安全设置属性: 函数 1 个 | 标签 无
  示例: set_attr
- &&% 暴力获取天正属性: 函数 1 个 | 标签 COM:1
  示例: brute_dump_tarch_props
- &&% 左下角排序: 函数 1 个 | 标签 无
  示例: sort_coms_by_llcorner
- &&% 右上角排序: 函数 1 个 | 标签 无
  示例: sort_coms_by_rbcorner
- &&% 中心点排序: 函数 1 个 | 标签 无
  示例: sort_coms_by_center
- &&% 绘制点: 函数 1 个 | 标签 无
  示例: draw_point
- &&% 绘制直线: 函数 1 个 | 标签 无
  示例: draw_line
- &&% 绘制圆: 函数 1 个 | 标签 无
  示例: draw_circle
- &&% 绘制正多边形: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_regular_polygon
- &&% 绘制轻量多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_lwpolyline
- &&% 绘制多段线: 函数 1 个 | 标签 COM:1, 几何:1
  示例: draw_polyline

## system/CAD_com_utils.py
- : 函数 5 个 | 标签 COM:1
  示例: _dummy_func, silent_mode, _retry_logic, retry_on_busy, retry_if_busy
- &&% 函数别名: 函数 1 个 | 标签 无
  示例: alias
- &&% 调试机制: 函数 3 个 | 标签 无
  示例: node, timeit, debuggable

## system/CAD_coordination.py
- : 函数 1 个 | 标签 无
  示例: wait_quiescent
- &&% 20260114: 函数 7 个 | 标签 几何:1, 文件:2, COM:1
  示例: wait_quiescent, run_safety_loop, send_cmd_with_sync, wait_document_opened, ensure_single_process, start_cad_with_dialog_killer, wait_command_done

## system/CAD_selection - V10.py
- : 函数 42 个 | 标签 COM:14, 几何:6, 选择集:18
  示例: com_retry, cast_object, _maybe_cast, to_vt_int, to_vt_variant, _to_vt_point, pt3, normalize_rect, expand_rectangle, ss_select, select_entities_through_point, select_objects_in_window_area...
- &&% 兼容旧代码获取对象属性: 函数 1 个 | 标签 COM:1
  示例: get_object_property
- &&% 兼容旧代设置对象属性: 函数 2 个 | 标签 COM:2
  示例: set_object_property, brute_dump_tarch_props

## system/CAD_selection.py
- : 函数 9 个 | 标签 COM:5, 几何:1
  示例: cast_object, _maybe_cast, to_vt_int, to_vt_variant, _to_vt_point, pt3, normalize_rect, expand_rectangle, com_retry
- &&% 限定空间装饰器: 函数 33 个 | 标签 选择集:18, 几何:4, COM:8
  示例: current_space_only, ss_select, select_entities_through_point, select_objects_in_window_area, select_paperspace_objects_in_window, pmxz, get_last_n_objects, last_obj, select_tuceng, stc, select_kuai, select_text...
- &&% 20261014: 函数 5 个 | 标签 COM:3
  示例: get_attr, set_attr, get_object_property, set_object_property, brute_dump_tarch_props
