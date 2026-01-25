# CAD 脚本函数级审查（初稿）

说明：本文件基于 AST + 关键字启发式生成，用于全量覆盖与风险初筛。
需要人工复核高风险函数后再进入改动阶段。

## 覆盖统计
- 文件数：56
- 函数/方法数：1301

## 风险标签统计（启发式）
- com: 48
- fileio: 46

## 函数清单（含标签）

| 文件 | 函数 | 行号 | 行数 | Doc | 标签 | 高风险命中 |
|---|---|---:|---:|:---:|---|---|
| library/cad_annotation.py | vtpnt | 27 | 3 | yes | com |  |
| library/cad_annotation.py | write_cad_text | 35 | 45 | yes | com,fileio |  |
| library/cad_annotation.py | write_mtext | 83 | 38 | yes | com,fileio |  |
| library/cad_annotation.py | add_dim_aligned | 125 | 22 | yes |  |  |
| library/cad_annotation.py | add_dim_rotated | 149 | 24 | yes |  |  |
| library/cad_annotation.py | add_dim_angular | 175 | 24 | yes |  |  |
| library/cad_annotation.py | add_dim_radial | 201 | 22 | yes |  |  |
| library/cad_annotation.py | add_dim_diametric | 225 | 22 | yes |  |  |
| library/cad_annotation.py | add_leader | 251 | 27 | yes |  |  |
| library/cad_annotation.py | get_text_content | 279 | 23 | yes |  |  |
| library/cad_annotation.py | set_text_content | 303 | 23 | yes |  |  |
| library/cad_annotation.py | get_text_height | 327 | 15 | yes |  |  |
| library/cad_annotation.py | set_text_height | 343 | 17 | yes |  |  |
| library/cad_annotation.py | get_text_rotation | 364 | 15 | yes |  |  |
| library/cad_annotation.py | set_text_rotation | 381 | 17 | yes |  |  |
| library/cad_annotation.py | batch_modify_text | 400 | 24 | yes |  |  |
| library/cad_annotation.py | create_table | 428 | 26 | yes |  |  |
| library/cad_annotation.py | set_table_cell_text | 456 | 19 | yes |  |  |
| library/cad_annotation.py | get_table_cell_text | 477 | 17 | yes |  |  |
| library/cad_blocks.py | get_block_name | 40 | 7 | yes | fileio |  |
| library/cad_blocks.py | huoqukuai_shuxing_zhi | 50 | 20 | no | com |  |
| library/cad_blocks.py | update_block_def_attributes_safe | 75 | 166 | yes | com,fileio |  |
| library/cad_blocks.py | update_block_def_attributes_v7 | 243 | 183 | yes |  |  |
| library/cad_blocks.py | attsync_block_instance | 429 | 30 | yes |  |  |
| library/cad_blocks.py | attsync_block_instance_base | 460 | 51 | yes |  |  |
| library/cad_blocks.py | set_attribute_mtext | 515 | 137 | yes |  |  |
| library/cad_blocks.py | get_block_attributes_dict | 658 | 95 | yes |  |  |
| library/cad_blocks.py | separate_entities_by_block_names | 755 | 50 | yes |  |  |
| library/cad_blocks.py | huoqu_kuai_pl | 810 | 21 | no |  |  |
| library/cad_blocks.py | create_block_with_basepoint | 840 | 13 | no |  |  |
| library/cad_blocks.py | create_block_with_triangle_and_text | 858 | 22 | no |  |  |
| library/cad_blocks.py | huoqu_kuai_pl | 883 | 20 | no |  |  |
| library/cad_blocks.py | get_bounding_box_of_block | 909 | 28 | no |  |  |
| library/cad_blocks.py | create_new_block_with_insert_and_line | 940 | 24 | no |  |  |
| library/cad_blocks.py | copy_and_move_blocks_from_layer | 968 | 22 | no |  |  |
| library/cad_blocks.py | delete_block_instances_and_definition_retry | 996 | 69 | yes |  |  |
| library/cad_blocks.py | delete_block_instances_and_definition_optimized | 1068 | 79 | yes |  |  |
| library/cad_blocks.py | delete_block_instances_and_definition_optimized | 1150 | 82 | yes |  |  |
| library/cad_blocks.py | rename_block_entity | 1236 | 24 | yes |  |  |
| library/cad_blocks.py | get_block_instances | 1264 | 34 | yes |  |  |
| library/cad_blocks.py | get_entities_from_block_reference | 1304 | 20 | yes |  |  |
| library/cad_blocks.py | insert_block_into_autocad | 1334 | 21 | yes |  |  |
| library/cad_blocks.py | insert_standard_block | 1361 | 71 | yes |  |  |
| library/cad_blocks.py | insert_and_explode_dwg | 1438 | 90 | yes |  |  |
| library/cad_blocks.py | insert_and_explode_dwg | 1533 | 99 | yes |  |  |
| library/cad_blocks.py | get_large_block_instances | 1638 | 54 | yes |  |  |
| library/cad_blocks.py | get_large_block_instances_with_tolerance | 1697 | 32 | yes |  |  |
| library/cad_blocks.py | transform_point_by_block | 1735 | 33 | yes |  |  |
| library/cad_blocks.py | select_block_by_name | 1771 | 34 | yes |  |  |
| library/cad_blocks.py | get_all_block_definitions | 1808 | 58 | yes |  |  |
| library/cad_blocks.py | get_all_block_names | 1869 | 16 | yes |  |  |
| library/cad_blocks.py | purge_block | 1888 | 56 | yes |  |  |
| library/cad_blocks.py | purge_unused_blocks | 1946 | 38 | yes |  |  |
| library/cad_blocks.py | purge_block_1 | 1989 | 138 | yes |  |  |
| library/cad_blocks.py | purge_unused_blocks_1 | 2130 | 158 | yes |  |  |
| library/cad_blocks.py | reserve_block_names_for_new_insert | 2291 | 84 | yes |  |  |
| library/cad_blocks.py | get_selected_blockreference_names | 2381 | 27 | yes |  |  |
| library/cad_blocks.py | create_block_from_region_cad | 2451 | 343 | yes |  |  |
| library/cad_blocks.py | create_block_from_region_cmd | 2798 | 191 | yes |  |  |
| library/cad_blocks.py | create_block_from_list_cmd | 2992 | 158 | yes |  |  |
| library/cad_blocks.py | get_block_contents_at_same_location | 3156 | 52 | yes |  |  |
| library/cad_blocks.py | add_entities_to_block_direct | 3214 | 181 | yes |  |  |
| library/cad_blocks.py | add_entities_to_block_definition_explode | 3398 | 135 | yes |  |  |
| library/cad_blocks.py | redefine_block_with_entities | 3539 | 161 | yes |  |  |
| library/cad_blocks.py | extract_specific_entities_from_block | 3720 | 188 | yes |  |  |
| library/cad_blocks.py | safe_explode | 3914 | 10 | yes |  |  |
| library/cad_blocks.py | _atomic_explode_and_delete | 3928 | 21 | yes |  |  |
| library/cad_blocks.py | safe_explode_retry | 3951 | 129 | yes |  |  |
| library/cad_blocks.py | explode_single_object_marker | 4088 | 86 | yes |  |  |
| library/cad_blocks.py | safe_explode_and_delete | 4176 | 51 | yes |  |  |
| library/cad_blocks.py | count_blocks_by_name | 4231 | 19 | yes |  |  |
| library/cad_blocks.py | count_blocks_by_type | 4252 | 21 | yes |  |  |
| library/cad_blocks.py | generate_block_report | 4275 | 29 | yes |  |  |
| library/cad_blocks.py | batch_replace_blocks | 4307 | 32 | yes |  |  |
| library/cad_blocks.py | smart_replace_blocks | 4341 | 29 | yes |  |  |
| library/cad_control.py | fix_com_cache | 46 | 52 | yes | com,fileio |  |
| library/cad_control.py | delete_all_nul_under_folder | 104 | 39 | yes |  |  |
| library/cad_control.py | kill_dialog_killer | 146 | 34 | yes |  |  |
| library/cad_control.py | kill_python_script_by_name | 186 | 52 | yes |  |  |
| library/cad_control.py | kill_wps | 491 | 34 | yes |  |  |
| library/cad_control.py | close_all_excel_processes | 529 | 89 | yes |  |  |
| library/cad_control.py | safe_delete | 633 | 53 | yes |  |  |
| library/cad_control.py | move_entities_in_region | 698 | 52 | yes |  |  |
| library/cad_control.py | 圆点 | 755 | 15 | yes |  |  |
| library/cad_control.py | 图纸背景 | 774 | 3 | no |  |  |
| library/cad_control.py | shitu_region | 785 | 18 | yes |  |  |
| library/cad_control.py | shitu_entity | 807 | 22 | yes |  |  |
| library/cad_control.py | record_screen_gif | 850 | 30 | yes |  |  |
| library/cad_control.py | minimize_all_windows | 885 | 42 | yes |  |  |
| library/cad_control.py | set_autocad_window_to_top_left | 934 | 37 | yes |  |  |
| library/cad_control.py | l | 975 | 3 | no |  |  |
| library/cad_control.py | minimize_all_windows_d | 985 | 10 | yes |  |  |
| library/cad_control.py | minimize_all_windows_m | 998 | 20 | yes |  |  |
| library/cad_control.py | restore_and_position | 1021 | 68 | yes |  |  |
| library/cad_control.py | list_open_window_titles | 1093 | 12 | yes |  |  |
| library/cad_control.py | ceshubiao_weizhi | 1107 | 10 | yes |  |  |
| library/cad_control.py | run_idle_background | 1119 | 14 | yes |  |  |
| library/cad_control.py | click_and_drag | 1145 | 21 | yes |  |  |
| library/cad_control.py | click_and_find_image_shape | 1169 | 35 | yes |  |  |
| library/cad_control.py | right_click_and_move | 1207 | 19 | yes |  |  |
| library/cad_control.py | kill_all_idle | 1228 | 11 | yes |  |  |
| library/cad_control.py | set_idle_window_to_top_right | 1242 | 26 | no |  |  |
| library/cad_control.py | r | 1270 | 3 | no |  |  |
| library/cad_control.py | place_obs_bottom_right | 1276 | 27 | yes |  |  |
| library/cad_control.py | r2 | 1305 | 3 | no |  |  |
| library/cad_control.py | minimize_window | 1311 | 18 | yes |  |  |
| library/cad_control.py | maximize_autocad_window | 1331 | 32 | yes |  |  |
| library/cad_control.py | start_obs_recording_by_click | 1366 | 22 | yes |  |  |
| library/cad_control.py | fs | 1392 | 9 | yes |  |  |
| library/cad_control.py | xuanqun | 1403 | 28 | no |  |  |
| library/cad_control.py | copy_to_clipboard | 1434 | 18 | yes |  |  |
| library/cad_control.py | xieweixin | 1454 | 22 | no |  |  |
| library/cad_control.py | 主操作函数 | 1478 | 40 | no |  |  |
| library/cad_control.py | main_func | 1521 | 3 | no |  |  |
| library/cad_control.py | luping | 1528 | 45 | yes |  |  |
| library/cad_control.py | 魔方 | 1576 | 5 | no |  |  |
| library/cad_control.py | run_py | 1585 | 16 | no |  |  |
| library/cad_control.py | focus_cmdline | 1604 | 8 | yes |  |  |
| library/cad_control.py | activate_window_by_title | 1618 | 51 | yes |  |  |
| library/cad_control.py | click_in_window | 1672 | 51 | yes |  |  |
| library/cad_control.py | activate_and_click_aikeyun | 1730 | 31 | no |  |  |
| library/cad_control.py | drag_in_window_simple | 1766 | 37 | yes |  |  |
| library/cad_control.py | run_auto_explode_area | 1817 | 25 | yes |  |  |
| library/cad_control.py | list_all_windows | 1845 | 10 | no |  |  |
| library/cad_control.py | minimize_window | 1857 | 18 | yes |  |  |
| library/cad_control.py | maximize_autocad_window | 1876 | 32 | yes |  |  |
| library/cad_control.py | set_dwg_units_precision | 1932 | 20 | yes |  |  |
| library/cad_control.py | jd | 1954 | 2 | no |  |  |
| library/cad_control.py | list_dim_styles | 1960 | 14 | yes |  |  |
| library/cad_control.py | set_current_dimstyle_via_command | 1978 | 12 | yes |  |  |
| library/cad_control.py | set_current_text_style | 1994 | 14 | yes |  |  |
| library/cad_control.py | huoqu_ziti_style | 2011 | 5 | no |  |  |
| library/cad_control.py | create_text_style | 2037 | 46 | yes |  |  |
| library/cad_control.py | set_text_style_onlyshx | 2088 | 36 | yes |  |  |
| library/cad_control.py | set_text_style | 2128 | 24 | yes |  |  |
| library/cad_control.py | rename_conflicting_text_styles | 2170 | 95 | yes |  |  |
| library/cad_control.py | transfer_props_by_matchprop | 2429 | 68 | no |  |  |
| library/cad_control.py | run_dual_threads_1 | 2539 | 96 | yes |  |  |
| library/cad_control.py | cancel_cad_selection | 2639 | 13 | no |  |  |
| library/cad_control.py | close_wps_window_by_click | 2657 | 33 | yes |  |  |
| library/cad_control.py | min_w | 2699 | 20 | no |  |  |
| library/cad_control.py | ql | 2724 | 3 | no |  |  |
| library/cad_control.py | srhd | 2735 | 44 | yes |  |  |
| library/cad_control.py | srhd_p | 2783 | 45 | yes |  |  |
| library/cad_control.py | comtomath | 2831 | 11 | no |  |  |
| library/cad_control.py | p | 2843 | 7 | no |  |  |
| library/cad_control.py | fuzhi_chakan | 2859 | 24 | no |  |  |
| library/cad_control.py | celiang_wenzichangdu | 2887 | 13 | no |  |  |
| library/cad_control.py | celiang_wenzichangdu_write | 2904 | 15 | no |  |  |
| library/cad_control.py | qingkong_wenjianjia | 2925 | 16 | no |  |  |
| library/cad_control.py | get_bbox_info | 2947 | 53 | yes |  |  |
| library/cad_control.py | bbox_orientation_flag | 3003 | 20 | yes |  |  |
| library/cad_control.py | group_bbox_corners | 3026 | 94 | yes |  |  |
| library/cad_control.py | bbox_center_2 | 3154 | 6 | no |  |  |
| library/cad_control.py | bbox_center_3 | 3162 | 6 | yes |  |  |
| library/cad_control.py | safe_get_bbox | 3170 | 64 | yes |  |  |
| library/cad_control.py | analyze_dwg_objects_status | 3238 | 116 | yes |  |  |
| library/cad_geometry.py | compute_line_angle | 52 | 20 | yes | com |  |
| library/cad_geometry.py | draw_point | 76 | 17 | yes | com,fileio |  |
| library/cad_geometry.py | draw_line | 95 | 16 | yes |  |  |
| library/cad_geometry.py | draw_circle | 114 | 17 | yes |  |  |
| library/cad_geometry.py | draw_regular_polygon | 134 | 28 | yes |  |  |
| library/cad_geometry.py | prioritize_horizontal | 166 | 20 | yes |  |  |
| library/cad_geometry.py | get_spline_length_by_conversion | 190 | 36 | yes |  |  |
| library/cad_geometry.py | estimate_ellipse_length | 228 | 15 | yes |  |  |
| library/cad_geometry.py | get_entity_geometry_info | 247 | 83 | yes |  |  |
| library/cad_geometry.py | points_on_line_at_distance_3d | 336 | 36 | yes |  |  |
| library/cad_geometry.py | find_fake_intersection_regions | 379 | 60 | yes |  |  |
| library/cad_geometry.py | lines_daduan | 446 | 17 | yes |  |  |
| library/cad_geometry.py | delete_duplicate_lines | 472 | 46 | yes |  |  |
| library/cad_geometry.py | delete_redundant_lines | 524 | 73 | yes |  |  |
| library/cad_geometry.py | find_isolated_intersections | 602 | 73 | yes |  |  |
| library/cad_geometry.py | get_inner_point_of_polygon | 683 | 15 | yes |  |  |
| library/cad_geometry.py | get_room_outline_from_point | 722 | 23 | yes |  |  |
| library/cad_geometry.py | connect_lines_to_polyline_if_closed | 748 | 73 | yes |  |  |
| library/cad_geometry.py | is_closed_polygon_from_lines | 824 | 60 | yes |  |  |
| library/cad_geometry.py | same_point | 886 | 3 | yes |  |  |
| library/cad_geometry.py | same_line | 892 | 14 | yes |  |  |
| library/cad_geometry.py | calculate_absolute_angle | 909 | 14 | yes |  |  |
| library/cad_geometry.py | calculate_relative_angle | 925 | 32 | yes |  |  |
| library/cad_geometry.py | find_lines_angle | 962 | 36 | yes |  |  |
| library/cad_geometry.py | find_lines_sharing_point | 1003 | 28 | yes |  |  |
| library/cad_geometry.py | find_successor_line_max | 1036 | 43 | yes |  |  |
| library/cad_geometry.py | find_rightbottom_point | 1083 | 16 | yes |  |  |
| library/cad_geometry.py | find_rightbottom_closed_polygon | 1140 | 65 | yes |  |  |
| library/cad_geometry.py | draw_polygon_as_polyline | 1211 | 108 | yes |  |  |
| library/cad_geometry.py | is_nearly_equal | 1327 | 2 | no |  |  |
| library/cad_geometry.py | find_successor_line_min | 1335 | 43 | no |  |  |
| library/cad_geometry.py | get_outer_contour | 1386 | 69 | yes |  |  |
| library/cad_geometry.py | deduplicate_vertices | 1483 | 35 | yes |  |  |
| library/cad_geometry.py | analyze_polygon_branches | 1525 | 143 | yes |  |  |
| library/cad_geometry.py | remove_lines_in_LBv | 1673 | 35 | yes |  |  |
| library/cad_geometry.py | process_polygons | 1714 | 78 | yes |  |  |
| library/cad_geometry.py | extract_polygon_from_lines | 1796 | 65 | yes |  |  |
| library/cad_geometry.py | explode_polylines | 1869 | 25 | yes |  |  |
| library/cad_geometry.py | subtract_line_sets | 1899 | 22 | yes |  |  |
| library/cad_geometry.py | process_final | 1928 | 32 | no |  |  |
| library/cad_geometry.py | draw_lwpolyline | 2011 | 78 | yes |  |  |
| library/cad_geometry.py | draw_lwpolyline | 2092 | 53 | yes |  |  |
| library/cad_geometry.py | get_unique_vertices_from_pl_com | 2151 | 33 | yes |  |  |
| library/cad_geometry.py | convert_lines_to_points | 2188 | 21 | yes |  |  |
| library/cad_geometry.py | merge_segments_new | 2213 | 60 | yes |  |  |
| library/cad_geometry.py | draw_polyline | 2279 | 80 | yes |  |  |
| library/cad_geometry.py | lines_to_polylines | 2374 | 93 | yes |  |  |
| library/cad_geometry.py | find_min_point | 2471 | 14 | yes |  |  |
| library/cad_geometry.py | find_max_point | 2489 | 14 | yes |  |  |
| library/cad_geometry.py | distance | 2506 | 3 | yes |  |  |
| library/cad_geometry.py | define_rectangle_by_diagonal | 2515 | 21 | yes |  |  |
| library/cad_geometry.py | define_rectangle_by_diagonal_x | 2538 | 21 | yes |  |  |
| library/cad_geometry.py | expand_rectangle | 2565 | 19 | yes |  |  |
| library/cad_geometry.py | parse_rectangle_points | 2589 | 48 | yes |  |  |
| library/cad_geometry.py | get_rectangular_polylines | 2640 | 76 | yes |  |  |
| library/cad_geometry.py | get_layout_rectangular_polylines_coords | 2831 | 101 | yes |  |  |
| library/cad_geometry.py | generate_name_and_ratio_from_com | 2938 | 189 | yes |  |  |
| library/cad_geometry.py | get_cad_app | 3133 | 8 | yes |  |  |
| library/cad_geometry.py | get_dimensions | 3142 | 15 | yes |  |  |
| library/cad_geometry.py | sort_coms_by_llcorner | 3158 | 30 | yes |  |  |
| library/cad_geometry.py | main | 3189 | 69 | no |  |  |
| library/cad_geometry.py | generate_relation_list | 3259 | 27 | no |  |  |
| library/cad_geometry.py | check_strict_standard_size | 3291 | 117 | yes |  |  |
| library/cad_geometry.py | check_strict_standard_size | 3412 | 99 | yes |  |  |
| library/cad_geometry.py | polyline_sort | 3514 | 25 | yes |  |  |
| library/cad_geometry.py | plcom_to_coor | 3547 | 49 | yes |  |  |
| library/cad_geometry.py | plcoor_to_com | 3602 | 48 | yes |  |  |
| library/cad_geometry.py | panduan_shuxiangkuang | 3659 | 17 | no |  |  |
| library/cad_geometry.py | tongyi_tufu | 3681 | 15 | yes |  |  |
| library/cad_geometry.py | simplify_polygon | 3714 | 37 | yes |  |  |
| library/cad_geometry.py | normalize_polygon | 3756 | 21 | yes |  |  |
| library/cad_geometry.py | get_adjacent_points | 3781 | 15 | yes |  |  |
| library/cad_geometry.py | point_in_polygon | 3800 | 17 | yes |  |  |
| library/cad_geometry.py | line_segment_intersection_2d | 3821 | 25 | yes |  |  |
| library/cad_geometry.py | get_auxiliary_point | 3850 | 46 | yes |  |  |
| library/cad_geometry.py | concavity_measure | 3900 | 26 | yes |  |  |
| library/cad_geometry.py | concavity_angle | 3930 | 7 | yes |  |  |
| library/cad_geometry.py | split_orthogonal_hexagon | 3945 | 70 | yes |  |  |
| library/cad_geometry.py | split_orthogonal_hexagon_vertical | 4018 | 72 | yes |  |  |
| library/cad_geometry.py | area_of | 4095 | 9 | yes |  |  |
| library/cad_geometry.py | split_hexagon_combined | 4108 | 47 | yes |  |  |
| library/cad_geometry.py | get_bbox_edge_segments | 4165 | 42 | yes |  |  |
| library/cad_geometry.py | get_texts_in_polyline | 4219 | 45 | yes |  |  |
| library/cad_geometry.py | TDbMText_content | 4272 | 99 | yes |  |  |
| library/cad_geometry.py | distribute_points_on_entity | 4383 | 52 | no |  |  |
| library/cad_geometry.py | is_segment_contained | 4449 | 62 | yes |  |  |
| library/cad_geometry.py | common_segments_between_polylines | 4515 | 111 | yes |  |  |
| library/cad_geometry.py | is_rect_inside_rect | 4643 | 25 | yes |  |  |
| library/cad_geometry.py | two_plines_making_rectangle | 4676 | 112 | yes |  |  |
| library/cad_geometry.py | are_all_vertices_inside | 4798 | 29 | yes |  |  |
| library/cad_objects.py | ensure_list | 34 | 58 | yes | com,fileio |  |
| library/cad_objects.py | sort_tuples | 102 | 25 | yes |  |  |
| library/cad_objects.py | multi_dim_tolerance_sort | 129 | 32 | yes |  |  |
| library/cad_objects.py | get_ll_pt | 163 | 3 | no |  |  |
| library/cad_objects.py | get_center | 167 | 3 | no |  |  |
| library/cad_objects.py | sort_entities_by_position | 172 | 32 | yes |  |  |
| library/cad_objects.py | get_line_start | 205 | 7 | yes |  |  |
| library/cad_objects.py | sort_coms_by_llcorner | 216 | 29 | yes |  |  |
| library/cad_objects.py | sort_coms_by_rbcorner | 250 | 34 | yes |  |  |
| library/cad_objects.py | sort_coms_by_llcorner_custom | 287 | 48 | yes |  |  |
| library/cad_objects.py | sort_coms_by_center | 338 | 54 | yes |  |  |
| library/cad_objects.py | number_entities_by_order | 397 | 24 | yes |  |  |
| library/cad_objects.py | pr_list | 428 | 19 | yes |  |  |
| library/cad_objects.py | apply_to_each2 | 453 | 13 | yes |  |  |
| library/cad_objects.py | get_boundingbox_from_objects | 521 | 20 | yes |  |  |
| library/cad_objects.py | chuangjian_zu | 546 | 5 | no |  |  |
| library/cad_objects.py | nametogroup | 553 | 4 | no |  |  |
| library/cad_objects.py | get_all_group_names | 561 | 11 | yes |  |  |
| library/cad_objects.py | get_all_groups | 574 | 15 | yes |  |  |
| library/cad_objects.py | add_objects_to_group | 594 | 15 | yes |  |  |
| library/cad_objects.py | add_object_to_group | 614 | 23 | yes |  |  |
| library/cad_objects.py | remove_object_from_group | 640 | 27 | yes |  |  |
| library/cad_objects.py | remove_objects_from_group | 670 | 24 | yes |  |  |
| library/cad_objects.py | get_com_from_groupname | 701 | 19 | yes |  |  |
| library/cad_objects.py | get_com_from_groupname_by_type | 723 | 26 | yes |  |  |
| library/cad_objects.py | get_group_entities_sorted | 752 | 35 | yes |  |  |
| library/cad_objects.py | get_group_entities_sorted_by_type_and_bbox | 793 | 42 | yes |  |  |
| library/cad_objects.py | common_group_entities_sorted | 839 | 55 | yes |  |  |
| library/cad_objects.py | get_boundingbox_from_group | 896 | 12 | yes |  |  |
| library/cad_objects.py | copy_group_S1_from_doc1_to_doc2 | 910 | 61 | yes |  |  |
| library/cad_objects.py | HandleToObject | 1016 | 10 | yes |  |  |
| library/cad_objects.py | print_coms_handle | 1028 | 9 | no |  |  |
| library/cad_objects.py | handles_to_coms | 1043 | 14 | yes |  |  |
| library/cad_objects.py | get_all_handles | 1060 | 17 | yes |  |  |
| library/cad_objects.py | find_entity_by_handle | 1079 | 18 | yes |  |  |
| library/cad_objects.py | group_objects_by_type_and_handle | 1101 | 32 | yes |  |  |
| library/cad_objects.py | record_handle_with_type | 1137 | 14 | yes |  |  |
| library/cad_objects.py | convert_named_dict | 1153 | 18 | yes |  |  |
| library/cad_objects.py | get_named_object | 1173 | 3 | no |  |  |
| library/cad_objects.py | draw_tags_on_objects_fixed | 1180 | 42 | yes |  |  |
| library/cad_objects.py | label_tarch_doors | 1226 | 29 | yes |  |  |
| library/cad_objects.py | get_handle_object_map | 1271 | 3 | yes |  |  |
| library/cad_objects.py | set_xdata | 1300 | 46 | yes |  |  |
| library/cad_objects.py | get_xdata | 1348 | 41 | yes |  |  |
| library/cad_objects.py | set_xdata_tab | 1394 | 8 | no |  |  |
| library/cad_objects.py | is_printApp_xdata_com | 1404 | 11 | no |  |  |
| library/cad_objects.py | write_cad_text | 1420 | 119 | yes |  |  |
| library/cad_objects.py | write_tianzheng_text | 1543 | 229 | yes |  |  |
| library/cad_objects.py | align_text_to_vertical_line | 1777 | 102 | yes |  |  |
| library/cad_objects.py | align_text_to_horizontal_line | 1882 | 100 | yes |  |  |
| library/cad_objects.py | scale_tianzheng_text_to_cad | 1986 | 103 | yes |  |  |
| library/cad_objects.py | sc_objs_to_layer | 2097 | 46 | no |  |  |
| library/cad_objects.py | delete_layer | 2145 | 34 | yes |  |  |
| library/cad_objects.py | create_layers_from_list | 2183 | 27 | yes |  |  |
| library/cad_objects.py | delete_layers_from_list | 2213 | 39 | yes |  |  |
| library/cad_objects.py | dim_by_points | 2255 | 41 | yes |  |  |
| library/cad_objects.py | ensure_layer | 2299 | 50 | yes |  |  |
| library/cad_objects.py | ensure_layer_model_only | 2351 | 61 | yes |  |  |
| library/cad_objects.py | ensure_layer_current | 2420 | 21 | yes |  |  |
| library/cad_objects.py | set_layer_properties | 2448 | 45 | yes |  |  |
| library/cad_objects.py | set_layer_with_retry | 2500 | 49 | yes |  |  |
| library/cad_objects.py | force_layer_objects_color | 2557 | 74 | yes |  |  |
| library/execution_result.py | ExecutionResult.__init__ | 39 | 23 | yes | com,fileio |  |
| library/execution_result.py | ExecutionResult.is_success | 63 | 3 | yes |  |  |
| library/execution_result.py | ExecutionResult.is_failed | 67 | 8 | yes | fileio |  |
| library/execution_result.py | ExecutionResult.is_partial | 76 | 3 | yes | fileio |  |
| library/execution_result.py | ExecutionResult.to_dict | 80 | 9 | yes | com |  |
| library/execution_result.py | ExecutionResult.__repr__ | 90 | 2 | no | fileio |  |
| library/execution_result.py | ExecutionResult.__bool__ | 93 | 3 | yes |  |  |
| library/execution_result.py | success | 100 | 21 | yes |  |  |
| library/execution_result.py | failed | 123 | 21 | yes |  |  |
| library/execution_result.py | partial | 146 | 27 | yes |  |  |
| library/execution_result.py | error | 175 | 21 | yes |  |  |
| library/execution_result.py | with_execution_check | 200 | 75 | yes |  |  |
| library/tarch_building.py | dim_by_points | 29 | 17 | yes | com,fileio |  |
| library/tarch_building.py | draw_tarch_wall | 49 | 61 | yes | com,fileio |  |
| library/tarch_building.py | insert_tarch_door | 112 | 97 | yes |  |  |
| library/tarch_building.py | insert_tarch_window | 213 | 164 | yes |  |  |
| library/tarch_building.py | run_tupdspace_for_tz_room_in_rect | 383 | 133 | yes |  |  |
| library/tarch_building.py | run_auto_TUPDSPACE_with_coord | 516 | 112 | yes |  |  |
| library/tarch_building.py | TDb_single_line_variable_wall | 633 | 80 | yes |  |  |
| library/tarch_building.py | convert_lines_to_walls | 717 | 55 | yes |  |  |
| library/tarch_building.py | set_walls_thickness | 775 | 15 | yes |  |  |
| library/tarch_building.py | activate_cad_middle_click | 808 | 18 | yes |  |  |
| library/tarch_building.py | insert_tarch_window_lisp_mode | 827 | 78 | yes |  |  |
| library/tarch_building.py | _get_dynamic_cache_path | 917 | 14 | yes |  |  |
| library/tarch_building.py | _load_cache_from_disk | 932 | 11 | yes |  |  |
| library/tarch_building.py | _save_cache_to_disk | 944 | 12 | yes |  |  |
| library/tarch_building.py | _activate_cad_safe | 964 | 17 | yes |  |  |
| library/tarch_building.py | _wait_for_user_hover | 982 | 26 | yes |  |  |
| library/tarch_building.py | get_wall_thickness | 1015 | 19 | yes |  |  |
| library/tarch_building.py | get_wall_length | 1036 | 18 | yes |  |  |
| library/tarch_building.py | get_wall_height | 1056 | 18 | yes |  |  |
| library/tarch_building.py | modify_wall_thickness | 1077 | 21 | yes |  |  |
| library/tarch_building.py | modify_wall_height | 1100 | 19 | yes |  |  |
| library/tarch_building.py | modify_door_size | 1122 | 21 | yes |  |  |
| library/tarch_building.py | modify_window_size | 1145 | 21 | yes |  |  |
| library/tarch_building.py | delete_door | 1168 | 17 | yes |  |  |
| library/tarch_building.py | delete_window | 1187 | 17 | yes |  |  |
| library/tarch_building.py | insert_tarch_column | 1207 | 27 | yes |  |  |
| library/tarch_building.py | modify_column_size | 1236 | 21 | yes |  |  |
| library/tarch_building.py | insert_tarch_stair | 1260 | 26 | yes |  |  |
| library/tarch_building.py | modify_stair_params | 1288 | 20 | yes |  |  |
| library/tarch_building.py | label_room_name | 1311 | 23 | yes |  |  |
| library/tarch_building.py | insert_tarch_door_universal | 1336 | 143 | yes |  |  |
| library/test_monitor.py | TestMonitor.__init__ | 27 | 11 | yes | com |  |
| library/test_monitor.py | TestMonitor.capture_dwg_state | 39 | 57 | yes | com,fileio |  |
| library/test_monitor.py | TestMonitor.capture_folder_state | 97 | 59 | yes |  |  |
| library/test_monitor.py | TestMonitor.before_test | 157 | 31 | yes |  |  |
| library/test_monitor.py | TestMonitor.after_test | 189 | 31 | yes |  |  |
| library/test_monitor.py | TestMonitor.compare_and_judge | 221 | 124 | yes |  |  |
| library/test_monitor.py | TestMonitor.save_report | 346 | 25 | yes |  |  |
| scripts/apply_modifications.py | create_backup | 27 | 9 | yes | com |  |
| scripts/apply_modifications.py | read_file | 37 | 4 | yes |  |  |
| scripts/apply_modifications.py | write_file | 42 | 4 | yes | fileio |  |
| scripts/apply_modifications.py | find_function_range | 47 | 34 | yes | com,fileio |  |
| scripts/apply_modifications.py | apply_modifications | 82 | 89 | yes | com,fileio |  |
| scripts/auto_TUPDSPACE.py | activate_autocad_window | 7 | 8 | no | com,fileio |  |
| scripts/auto_TUPDSPACE.py | run_tupdspace_flow | 17 | 19 | no | com |  |
| scripts/auto_TUPDSPACE.py | auto_tupdspace_with_repair | 38 | 17 | no | com,fileio |  |
| scripts/CAD_basic.py | _ComLiveProxy.__init__ | 1364 | 1 | no |  |  |
| scripts/CAD_basic.py | _ComLiveProxy.__getattr__ | 1365 | 3 | no |  |  |
| scripts/CAD_basic.py | _ComLiveProxy.__dir__ | 1369 | 1 | no |  |  |
| scripts/CAD_basic.py | CatalogConfigBuilder.__init__ | 26447 | 4 | no |  |  |
| scripts/CAD_basic.py | CatalogConfigBuilder.add_column_layout | 26452 | 6 | yes |  |  |
| scripts/CAD_basic.py | CatalogConfigBuilder.set_field_x_ranges | 26459 | 3 | yes |  |  |
| scripts/CAD_basic.py | CatalogConfigBuilder.generate | 26463 | 18 | no |  |  |
| scripts/CAD_basic.py | _cad_safe_print | 35 | 23 | yes | com,fileio |  |
| scripts/CAD_basic.py | _log | 536 | 17 | yes |  |  |
| scripts/CAD_basic.py | _kill_acad | 555 | 11 | yes |  |  |
| scripts/CAD_basic.py | connect_database_task | 572 | 4 | no |  |  |
| scripts/CAD_basic.py | safe_save_cad | 579 | 13 | no |  |  |
| scripts/CAD_basic.py | timeout_and_log2 | 598 | 37 | yes |  |  |
| scripts/CAD_basic.py | test_draw_circle_and_wait | 638 | 52 | yes |  |  |
| scripts/CAD_basic.py | wait_quiescent_ceshi | 719 | 19 | yes |  |  |
| scripts/CAD_basic.py | complex_operation_demo | 740 | 69 | yes |  |  |
| scripts/CAD_basic.py | draw_infinite_spiral | 814 | 59 | no |  |  |
| scripts/CAD_basic.py | speak_msg | 893 | 20 | yes |  |  |
| scripts/CAD_basic.py | com_to_handle | 929 | 11 | yes |  |  |
| scripts/CAD_basic.py | serialize | 941 | 12 | yes |  |  |
| scripts/CAD_basic.py | save_print_dict_generic | 955 | 11 | yes |  |  |
| scripts/CAD_basic.py | load | 970 | 18 | yes |  |  |
| scripts/CAD_basic.py | current_dwg_basename | 990 | 8 | yes |  |  |
| scripts/CAD_basic.py | current_dwg_folder | 999 | 37 | yes |  |  |
| scripts/CAD_basic.py | vtpnt | 1044 | 3 | yes |  |  |
| scripts/CAD_basic.py | vtobj | 1048 | 3 | yes |  |  |
| scripts/CAD_basic.py | vtFloat | 1052 | 3 | yes |  |  |
| scripts/CAD_basic.py | vtInt | 1056 | 3 | yes |  |  |
| scripts/CAD_basic.py | vtVariant | 1060 | 3 | yes |  |  |
| scripts/CAD_basic.py | ConvertArrays2Variant | 1064 | 13 | no |  |  |
| scripts/CAD_basic.py | vtlist | 1078 | 9 | yes |  |  |
| scripts/CAD_basic.py | start_applicationV9 | 1095 | 90 | yes |  |  |
| scripts/CAD_basic.py | force_show_cad_interface | 1186 | 31 | yes |  |  |
| scripts/CAD_basic.py | st | 1219 | 23 | no |  |  |
| scripts/CAD_basic.py | get_acad_process_id | 1243 | 5 | no |  |  |
| scripts/CAD_basic.py | jingchengshu_wenjian | 1252 | 10 | no |  |  |
| scripts/CAD_basic.py | close_all_cad_processes | 1271 | 59 | yes |  |  |
| scripts/CAD_basic.py | close_oldest_cad_process | 1332 | 18 | no |  |  |
| scripts/CAD_basic.py | ensure_typelib_from_running | 1355 | 6 | yes |  |  |
| scripts/CAD_basic.py | zoom_window | 1377 | 4 | no |  |  |
| scripts/CAD_basic.py | aci_to_rgb | 1388 | 7 | no |  |  |
| scripts/CAD_basic.py | get_entity_rgb | 1396 | 33 | yes |  |  |
| scripts/CAD_basic.py | chongfu_caozuo | 1448 | 53 | yes |  |  |
| scripts/CAD_basic.py | simple_timer | 1515 | 8 | no |  |  |
| scripts/CAD_basic.py | _coinit_once | 1535 | 6 | yes |  |  |
| scripts/CAD_basic.py | get_acad_doc | 1542 | 79 | yes |  |  |
| scripts/CAD_basic.py | normalize_rect | 1622 | 4 | no |  |  |
| scripts/CAD_basic.py | get_pmxz_group_bbox | 1770 | 57 | yes |  |  |
| scripts/CAD_basic.py | g | 1831 | 3 | no |  |  |
| scripts/CAD_basic.py | align_last_ms_obj_lb_to_origin | 1837 | 67 | yes |  |  |
| scripts/CAD_basic.py | get_entity_full_info | 1905 | 95 | yes |  |  |
| scripts/CAD_basic.py | compute_line_angle | 2021 | 20 | yes |  |  |
| scripts/CAD_basic.py | draw_point | 2044 | 17 | yes |  |  |
| scripts/CAD_basic.py | draw_line | 2063 | 16 | yes |  |  |
| scripts/CAD_basic.py | draw_circle | 2082 | 17 | yes |  |  |
| scripts/CAD_basic.py | draw_regular_polygon | 2102 | 28 | yes |  |  |
| scripts/CAD_basic.py | prioritize_horizontal | 2134 | 20 | yes |  |  |
| scripts/CAD_basic.py | get_spline_length_by_conversion | 2157 | 36 | yes |  |  |
| scripts/CAD_basic.py | estimate_ellipse_length | 2195 | 15 | yes |  |  |
| scripts/CAD_basic.py | get_entity_geometry_info | 2214 | 83 | yes |  |  |
| scripts/CAD_basic.py | points_on_line_at_distance_3d | 2303 | 36 | yes |  |  |
| scripts/CAD_basic.py | find_fake_intersection_regions | 2344 | 60 | yes |  |  |
| scripts/CAD_basic.py | lines_daduan | 2410 | 17 | yes |  |  |
| scripts/CAD_basic.py | delete_duplicate_lines | 2436 | 46 | yes |  |  |
| scripts/CAD_basic.py | delete_redundant_lines | 2488 | 73 | yes |  |  |
| scripts/CAD_basic.py | find_isolated_intersections | 2566 | 73 | yes |  |  |
| scripts/CAD_basic.py | get_inner_point_of_polygon | 2647 | 15 | yes |  |  |
| scripts/CAD_basic.py | get_room_outline_from_point | 2685 | 23 | yes |  |  |
| scripts/CAD_basic.py | connect_lines_to_polyline_if_closed | 2711 | 73 | yes |  |  |
| scripts/CAD_basic.py | is_closed_polygon_from_lines | 2787 | 60 | yes |  |  |
| scripts/CAD_basic.py | same_point | 2849 | 3 | yes |  |  |
| scripts/CAD_basic.py | same_line | 2855 | 14 | yes |  |  |
| scripts/CAD_basic.py | calculate_absolute_angle | 2872 | 14 | yes |  |  |
| scripts/CAD_basic.py | calculate_relative_angle | 2888 | 32 | yes |  |  |
| scripts/CAD_basic.py | find_lines_angle | 2925 | 36 | yes |  |  |
| scripts/CAD_basic.py | find_lines_sharing_point | 2966 | 28 | yes |  |  |
| scripts/CAD_basic.py | find_successor_line_max | 2999 | 43 | yes |  |  |
| scripts/CAD_basic.py | find_rightbottom_point | 3046 | 16 | yes |  |  |
| scripts/CAD_basic.py | find_rightbottom_closed_polygon | 3103 | 65 | yes |  |  |
| scripts/CAD_basic.py | draw_polygon_as_polyline | 3174 | 108 | yes |  |  |
| scripts/CAD_basic.py | is_nearly_equal | 3290 | 2 | no |  |  |
| scripts/CAD_basic.py | find_successor_line_min | 3298 | 43 | no |  |  |
| scripts/CAD_basic.py | get_outer_contour | 3349 | 69 | yes |  |  |
| scripts/CAD_basic.py | deduplicate_vertices | 3446 | 35 | yes |  |  |
| scripts/CAD_basic.py | analyze_polygon_branches | 3488 | 143 | yes |  |  |
| scripts/CAD_basic.py | remove_lines_in_LBv | 3636 | 35 | yes |  |  |
| scripts/CAD_basic.py | process_polygons | 3677 | 78 | yes |  |  |
| scripts/CAD_basic.py | extract_polygon_from_lines | 3759 | 65 | yes |  |  |
| scripts/CAD_basic.py | explode_polylines | 3832 | 25 | yes |  |  |
| scripts/CAD_basic.py | subtract_line_sets | 3862 | 22 | yes |  |  |
| scripts/CAD_basic.py | process_final | 3891 | 32 | no |  |  |
| scripts/CAD_basic.py | draw_lwpolyline | 3973 | 78 | yes |  |  |
| scripts/CAD_basic.py | draw_lwpolyline | 4054 | 53 | yes |  |  |
| scripts/CAD_basic.py | get_unique_vertices_from_pl_com | 4113 | 33 | yes |  |  |
| scripts/CAD_basic.py | convert_lines_to_points | 4150 | 21 | yes |  |  |
| scripts/CAD_basic.py | merge_segments_new | 4175 | 60 | yes |  |  |
| scripts/CAD_basic.py | draw_polyline | 4241 | 80 | yes |  |  |
| scripts/CAD_basic.py | lines_to_polylines | 4336 | 93 | yes |  |  |
| scripts/CAD_basic.py | find_min_point | 4433 | 14 | yes |  |  |
| scripts/CAD_basic.py | find_max_point | 4451 | 14 | yes |  |  |
| scripts/CAD_basic.py | distance | 4468 | 3 | yes |  |  |
| scripts/CAD_basic.py | define_rectangle_by_diagonal | 4477 | 21 | yes |  |  |
| scripts/CAD_basic.py | define_rectangle_by_diagonal_x | 4500 | 21 | yes |  |  |
| scripts/CAD_basic.py | expand_rectangle | 4527 | 19 | yes |  |  |
| scripts/CAD_basic.py | parse_rectangle_points | 4551 | 47 | yes |  |  |
| scripts/CAD_basic.py | get_rectangular_polylines | 4601 | 76 | yes |  |  |
| scripts/CAD_basic.py | get_layout_rectangular_polylines_coords | 4792 | 101 | yes |  |  |
| scripts/CAD_basic.py | generate_name_and_ratio_from_com | 4898 | 189 | yes |  |  |
| scripts/CAD_basic.py | get_cad_app | 5093 | 8 | yes |  |  |
| scripts/CAD_basic.py | get_dimensions | 5102 | 15 | yes |  |  |
| scripts/CAD_basic.py | sort_coms_by_llcorner | 5118 | 30 | yes |  |  |
| scripts/CAD_basic.py | main | 5149 | 69 | no |  |  |
| scripts/CAD_basic.py | generate_relation_list | 5219 | 27 | no |  |  |
| scripts/CAD_basic.py | check_strict_standard_size | 5251 | 117 | yes |  |  |
| scripts/CAD_basic.py | check_strict_standard_size | 5372 | 99 | yes |  |  |
| scripts/CAD_basic.py | polyline_sort | 5474 | 25 | yes |  |  |
| scripts/CAD_basic.py | plcom_to_coor | 5507 | 49 | yes |  |  |
| scripts/CAD_basic.py | plcoor_to_com | 5562 | 48 | yes |  |  |
| scripts/CAD_basic.py | panduan_shuxiangkuang | 5619 | 17 | no |  |  |
| scripts/CAD_basic.py | tongyi_tufu | 5641 | 15 | yes |  |  |
| scripts/CAD_basic.py | simplify_polygon | 5674 | 37 | yes |  |  |
| scripts/CAD_basic.py | normalize_polygon | 5716 | 21 | yes |  |  |
| scripts/CAD_basic.py | get_adjacent_points | 5741 | 15 | yes |  |  |
| scripts/CAD_basic.py | point_in_polygon | 5760 | 17 | yes |  |  |
| scripts/CAD_basic.py | line_segment_intersection_2d | 5781 | 25 | yes |  |  |
| scripts/CAD_basic.py | get_auxiliary_point | 5810 | 46 | yes |  |  |
| scripts/CAD_basic.py | concavity_measure | 5860 | 26 | yes |  |  |
| scripts/CAD_basic.py | concavity_angle | 5890 | 7 | yes |  |  |
| scripts/CAD_basic.py | split_orthogonal_hexagon | 5905 | 70 | yes |  |  |
| scripts/CAD_basic.py | split_orthogonal_hexagon_vertical | 5978 | 72 | yes |  |  |
| scripts/CAD_basic.py | area_of | 6055 | 9 | yes |  |  |
| scripts/CAD_basic.py | split_hexagon_combined | 6068 | 47 | yes |  |  |
| scripts/CAD_basic.py | get_bbox_edge_segments | 6125 | 42 | yes |  |  |
| scripts/CAD_basic.py | get_texts_in_polyline | 6179 | 45 | yes |  |  |
| scripts/CAD_basic.py | TDbMText_content | 6232 | 99 | yes |  |  |
| scripts/CAD_basic.py | distribute_points_on_entity | 6343 | 52 | no |  |  |
| scripts/CAD_basic.py | is_segment_contained | 6409 | 62 | yes |  |  |
| scripts/CAD_basic.py | common_segments_between_polylines | 6475 | 111 | yes |  |  |
| scripts/CAD_basic.py | is_rect_inside_rect | 6603 | 25 | yes |  |  |
| scripts/CAD_basic.py | two_plines_making_rectangle | 6636 | 112 | yes |  |  |
| scripts/CAD_basic.py | are_all_vertices_inside | 6758 | 29 | yes |  |  |
| scripts/CAD_basic.py | ensure_list | 6793 | 58 | yes |  |  |
| scripts/CAD_basic.py | sort_tuples | 6861 | 25 | yes |  |  |
| scripts/CAD_basic.py | multi_dim_tolerance_sort | 6888 | 32 | yes |  |  |
| scripts/CAD_basic.py | get_ll_pt | 6922 | 3 | no |  |  |
| scripts/CAD_basic.py | get_center | 6926 | 3 | no |  |  |
| scripts/CAD_basic.py | sort_entities_by_position | 6931 | 32 | yes |  |  |
| scripts/CAD_basic.py | get_line_start | 6964 | 7 | yes |  |  |
| scripts/CAD_basic.py | sort_coms_by_llcorner | 6975 | 29 | yes |  |  |
| scripts/CAD_basic.py | sort_coms_by_rbcorner | 7009 | 34 | yes |  |  |
| scripts/CAD_basic.py | sort_coms_by_llcorner_custom | 7046 | 48 | yes |  |  |
| scripts/CAD_basic.py | sort_coms_by_center | 7097 | 54 | yes |  |  |
| scripts/CAD_basic.py | number_entities_by_order | 7156 | 24 | yes |  |  |
| scripts/CAD_basic.py | pr_list | 7186 | 19 | yes |  |  |
| scripts/CAD_basic.py | apply_to_each2 | 7211 | 13 | yes |  |  |
| scripts/CAD_basic.py | get_boundingbox_from_objects | 7278 | 20 | yes |  |  |
| scripts/CAD_basic.py | chuangjian_zu | 7303 | 5 | no |  |  |
| scripts/CAD_basic.py | nametogroup | 7310 | 4 | no |  |  |
| scripts/CAD_basic.py | get_all_group_names | 7318 | 11 | yes |  |  |
| scripts/CAD_basic.py | get_all_groups | 7331 | 15 | yes |  |  |
| scripts/CAD_basic.py | add_objects_to_group | 7351 | 15 | yes |  |  |
| scripts/CAD_basic.py | add_object_to_group | 7371 | 23 | yes |  |  |
| scripts/CAD_basic.py | remove_object_from_group | 7397 | 27 | yes |  |  |
| scripts/CAD_basic.py | remove_objects_from_group | 7427 | 24 | yes |  |  |
| scripts/CAD_basic.py | get_com_from_groupname | 7458 | 19 | yes |  |  |
| scripts/CAD_basic.py | get_com_from_groupname_by_type | 7480 | 26 | yes |  |  |
| scripts/CAD_basic.py | get_group_entities_sorted | 7509 | 35 | yes |  |  |
| scripts/CAD_basic.py | get_group_entities_sorted_by_type_and_bbox | 7550 | 42 | yes |  |  |
| scripts/CAD_basic.py | common_group_entities_sorted | 7596 | 55 | yes |  |  |
| scripts/CAD_basic.py | get_boundingbox_from_group | 7653 | 12 | yes |  |  |
| scripts/CAD_basic.py | copy_group_S1_from_doc1_to_doc2 | 7667 | 61 | yes |  |  |
| scripts/CAD_basic.py | HandleToObject | 7773 | 10 | yes |  |  |
| scripts/CAD_basic.py | print_coms_handle | 7785 | 9 | no |  |  |
| scripts/CAD_basic.py | handles_to_coms | 7800 | 14 | yes |  |  |
| scripts/CAD_basic.py | get_all_handles | 7817 | 17 | yes |  |  |
| scripts/CAD_basic.py | find_entity_by_handle | 7836 | 18 | yes |  |  |
| scripts/CAD_basic.py | group_objects_by_type_and_handle | 7858 | 32 | yes |  |  |
| scripts/CAD_basic.py | record_handle_with_type | 7894 | 14 | yes |  |  |
| scripts/CAD_basic.py | convert_named_dict | 7910 | 18 | yes |  |  |
| scripts/CAD_basic.py | get_named_object | 7930 | 3 | no |  |  |
| scripts/CAD_basic.py | draw_tags_on_objects_fixed | 7937 | 42 | yes |  |  |
| scripts/CAD_basic.py | label_tarch_doors | 7983 | 29 | yes |  |  |
| scripts/CAD_basic.py | get_handle_object_map | 8028 | 3 | yes |  |  |
| scripts/CAD_basic.py | set_xdata | 8057 | 46 | yes |  |  |
| scripts/CAD_basic.py | get_xdata | 8105 | 41 | yes |  |  |
| scripts/CAD_basic.py | set_xdata_tab | 8151 | 8 | no |  |  |
| scripts/CAD_basic.py | is_printApp_xdata_com | 8161 | 11 | no |  |  |
| scripts/CAD_basic.py | write_cad_text | 8177 | 119 | yes |  |  |
| scripts/CAD_basic.py | write_tianzheng_text | 8300 | 229 | yes |  |  |
| scripts/CAD_basic.py | align_text_to_vertical_line | 8534 | 102 | yes |  |  |
| scripts/CAD_basic.py | align_text_to_horizontal_line | 8639 | 100 | yes |  |  |
| scripts/CAD_basic.py | scale_tianzheng_text_to_cad | 8743 | 103 | yes |  |  |
| scripts/CAD_basic.py | sc_objs_to_layer | 8854 | 46 | no |  |  |
| scripts/CAD_basic.py | delete_layer | 8902 | 34 | yes |  |  |
| scripts/CAD_basic.py | create_layers_from_list | 8940 | 27 | yes |  |  |
| scripts/CAD_basic.py | delete_layers_from_list | 8970 | 39 | yes |  |  |
| scripts/CAD_basic.py | dim_by_points | 9012 | 41 | yes |  |  |
| scripts/CAD_basic.py | ensure_layer | 9056 | 50 | yes |  |  |
| scripts/CAD_basic.py | ensure_layer_model_only | 9108 | 61 | yes |  |  |
| scripts/CAD_basic.py | ensure_layer_current | 9177 | 21 | yes |  |  |
| scripts/CAD_basic.py | set_layer_properties | 9205 | 45 | yes |  |  |
| scripts/CAD_basic.py | set_layer_with_retry | 9257 | 49 | yes |  |  |
| scripts/CAD_basic.py | force_layer_objects_color | 9314 | 74 | yes |  |  |
| scripts/CAD_basic.py | build_J_points_from_selected_texts | 9409 | 32 | no |  |  |
| scripts/CAD_basic.py | convert_pts_dict_to_latlon | 9445 | 43 | yes |  |  |
| scripts/CAD_basic.py | xianshi_yincangtuxing | 9519 | 5 | no |  |  |
| scripts/CAD_basic.py | run_cad_program | 9534 | 20 | no |  |  |
| scripts/CAD_basic.py | automate_window_with_pywinauto_t7 | 9557 | 56 | no |  |  |
| scripts/CAD_basic.py | zhuancheng_t7 | 9616 | 40 | yes |  |  |
| scripts/CAD_basic.py | automate_window_with_pywinauto_t3 | 9666 | 55 | no |  |  |
| scripts/CAD_basic.py | zhuancheng_t3 | 9724 | 41 | yes |  |  |
| scripts/CAD_basic.py | ensure_file_absent | 9783 | 17 | yes |  |  |
| scripts/CAD_basic.py | traverse_with_os_walk | 9803 | 11 | yes |  |  |
| scripts/CAD_basic.py | find_files_with_extensions | 9818 | 8 | no |  |  |
| scripts/CAD_basic.py | get_filename_without_extension | 9828 | 8 | no |  |  |
| scripts/CAD_basic.py | delete_files_with_patterns | 9839 | 24 | yes |  |  |
| scripts/CAD_basic.py | clear_files_with_prefix | 9868 | 35 | yes |  |  |
| scripts/CAD_basic.py | find_files_with_string | 9907 | 7 | no |  |  |
| scripts/CAD_basic.py | join_paths | 9917 | 5 | no |  |  |
| scripts/CAD_basic.py | get_block_name | 9934 | 7 | yes |  |  |
| scripts/CAD_basic.py | huoqukuai_shuxing_zhi | 9944 | 20 | no |  |  |
| scripts/CAD_basic.py | update_block_def_attributes_safe | 9969 | 166 | yes |  |  |
| scripts/CAD_basic.py | update_block_def_attributes_v7 | 10137 | 183 | yes |  |  |
| scripts/CAD_basic.py | attsync_block_instance | 10323 | 30 | yes |  |  |
| scripts/CAD_basic.py | attsync_block_instance_base | 10354 | 51 | yes |  |  |
| scripts/CAD_basic.py | set_attribute_mtext | 10409 | 137 | yes |  |  |
| scripts/CAD_basic.py | get_block_attributes_dict | 10552 | 95 | yes |  |  |
| scripts/CAD_basic.py | separate_entities_by_block_names | 10649 | 50 | yes |  |  |
| scripts/CAD_basic.py | huoqu_kuai_pl | 10704 | 21 | no |  |  |
| scripts/CAD_basic.py | create_block_with_basepoint | 10733 | 13 | no |  |  |
| scripts/CAD_basic.py | create_block_with_triangle_and_text | 10751 | 22 | no |  |  |
| scripts/CAD_basic.py | huoqu_kuai_pl | 10776 | 20 | no |  |  |
| scripts/CAD_basic.py | get_bounding_box_of_block | 10802 | 28 | no |  |  |
| scripts/CAD_basic.py | create_new_block_with_insert_and_line | 10833 | 24 | no |  |  |
| scripts/CAD_basic.py | copy_and_move_blocks_from_layer | 10861 | 22 | no |  |  |
| scripts/CAD_basic.py | delete_block_instances_and_definition_retry | 10889 | 69 | yes |  |  |
| scripts/CAD_basic.py | delete_block_instances_and_definition_optimized | 10961 | 79 | yes |  |  |
| scripts/CAD_basic.py | delete_block_instances_and_definition_optimized | 11043 | 82 | yes |  |  |
| scripts/CAD_basic.py | rename_block_entity | 11129 | 24 | yes |  |  |
| scripts/CAD_basic.py | get_block_instances | 11156 | 34 | yes |  |  |
| scripts/CAD_basic.py | get_entities_from_block_reference | 11196 | 20 | yes |  |  |
| scripts/CAD_basic.py | insert_block_into_autocad | 11225 | 21 | yes |  |  |
| scripts/CAD_basic.py | insert_standard_block | 11252 | 71 | yes |  |  |
| scripts/CAD_basic.py | insert_and_explode_dwg | 11329 | 90 | yes |  |  |
| scripts/CAD_basic.py | insert_and_explode_dwg | 11424 | 99 | yes |  |  |
| scripts/CAD_basic.py | get_large_block_instances | 11529 | 54 | yes |  |  |
| scripts/CAD_basic.py | get_large_block_instances_with_tolerance | 11588 | 32 | yes |  |  |
| scripts/CAD_basic.py | transform_point_by_block | 11626 | 33 | yes |  |  |
| scripts/CAD_basic.py | select_block_by_name | 11662 | 34 | yes |  |  |
| scripts/CAD_basic.py | get_all_block_definitions | 11698 | 58 | yes |  |  |
| scripts/CAD_basic.py | get_all_block_names | 11759 | 16 | yes |  |  |
| scripts/CAD_basic.py | purge_block | 11778 | 56 | yes |  |  |
| scripts/CAD_basic.py | purge_unused_blocks | 11836 | 38 | yes |  |  |
| scripts/CAD_basic.py | purge_block_1 | 11879 | 138 | yes |  |  |
| scripts/CAD_basic.py | purge_unused_blocks_1 | 12020 | 158 | yes |  |  |
| scripts/CAD_basic.py | reserve_block_names_for_new_insert | 12181 | 84 | yes |  |  |
| scripts/CAD_basic.py | get_selected_blockreference_names | 12271 | 27 | yes |  |  |
| scripts/CAD_basic.py | create_block_from_region_cad | 12341 | 343 | yes |  |  |
| scripts/CAD_basic.py | create_block_from_region_cmd | 12688 | 191 | yes |  |  |
| scripts/CAD_basic.py | create_block_from_list_cmd | 12882 | 158 | yes |  |  |
| scripts/CAD_basic.py | get_block_contents_at_same_location | 13045 | 52 | yes |  |  |
| scripts/CAD_basic.py | add_entities_to_block_direct | 13103 | 181 | yes |  |  |
| scripts/CAD_basic.py | add_entities_to_block_definition_explode | 13287 | 135 | yes |  |  |
| scripts/CAD_basic.py | redefine_block_with_entities | 13428 | 161 | yes |  |  |
| scripts/CAD_basic.py | extract_specific_entities_from_block | 13609 | 188 | yes |  |  |
| scripts/CAD_basic.py | safe_explode | 13803 | 10 | yes |  |  |
| scripts/CAD_basic.py | _atomic_explode_and_delete | 13817 | 21 | yes |  |  |
| scripts/CAD_basic.py | safe_explode_retry | 13840 | 129 | yes |  |  |
| scripts/CAD_basic.py | explode_single_object_marker | 13977 | 86 | yes |  |  |
| scripts/CAD_basic.py | safe_explode_and_delete | 14065 | 51 | yes |  |  |
| scripts/CAD_basic.py | fix_com_cache | 14130 | 52 | yes |  |  |
| scripts/CAD_basic.py | delete_all_nul_under_folder | 14188 | 39 | yes |  |  |
| scripts/CAD_basic.py | kill_dialog_killer | 14230 | 34 | yes |  |  |
| scripts/CAD_basic.py | kill_python_script_by_name | 14270 | 52 | yes |  |  |
| scripts/CAD_basic.py | kill_wps | 14575 | 34 | yes |  |  |
| scripts/CAD_basic.py | close_all_excel_processes | 14613 | 89 | yes |  |  |
| scripts/CAD_basic.py | safe_delete | 14717 | 53 | yes |  |  |
| scripts/CAD_basic.py | move_entities_in_region | 14782 | 52 | yes |  |  |
| scripts/CAD_basic.py | 圆点 | 14838 | 15 | yes |  |  |
| scripts/CAD_basic.py | 图纸背景 | 14857 | 3 | no |  |  |
| scripts/CAD_basic.py | shitu_region | 14868 | 18 | yes |  |  |
| scripts/CAD_basic.py | shitu_entity | 14890 | 22 | yes |  |  |
| scripts/CAD_basic.py | record_screen_gif | 14933 | 30 | yes |  |  |
| scripts/CAD_basic.py | minimize_all_windows | 14967 | 42 | yes |  |  |
| scripts/CAD_basic.py | set_autocad_window_to_top_left | 15016 | 37 | yes |  |  |
| scripts/CAD_basic.py | l | 15057 | 3 | no |  |  |
| scripts/CAD_basic.py | minimize_all_windows_d | 15067 | 10 | yes |  |  |
| scripts/CAD_basic.py | minimize_all_windows_m | 15080 | 20 | yes |  |  |
| scripts/CAD_basic.py | restore_and_position | 15103 | 68 | yes |  |  |
| scripts/CAD_basic.py | list_open_window_titles | 15175 | 12 | yes |  |  |
| scripts/CAD_basic.py | ceshubiao_weizhi | 15189 | 10 | yes |  |  |
| scripts/CAD_basic.py | run_idle_background | 15201 | 14 | yes |  |  |
| scripts/CAD_basic.py | click_and_drag | 15227 | 21 | yes |  |  |
| scripts/CAD_basic.py | click_and_find_image_shape | 15251 | 35 | yes |  |  |
| scripts/CAD_basic.py | right_click_and_move | 15289 | 19 | yes |  |  |
| scripts/CAD_basic.py | kill_all_idle | 15310 | 11 | yes |  |  |
| scripts/CAD_basic.py | set_idle_window_to_top_right | 15324 | 26 | no |  |  |
| scripts/CAD_basic.py | r | 15352 | 3 | no |  |  |
| scripts/CAD_basic.py | place_obs_bottom_right | 15358 | 27 | yes |  |  |
| scripts/CAD_basic.py | r2 | 15387 | 3 | no |  |  |
| scripts/CAD_basic.py | minimize_window | 15393 | 18 | yes |  |  |
| scripts/CAD_basic.py | maximize_autocad_window | 15413 | 32 | yes |  |  |
| scripts/CAD_basic.py | start_obs_recording_by_click | 15448 | 22 | yes |  |  |
| scripts/CAD_basic.py | fs | 15474 | 9 | yes |  |  |
| scripts/CAD_basic.py | xuanqun | 15485 | 28 | no |  |  |
| scripts/CAD_basic.py | copy_to_clipboard | 15516 | 18 | yes |  |  |
| scripts/CAD_basic.py | xieweixin | 15536 | 22 | no |  |  |
| scripts/CAD_basic.py | 主操作函数 | 15560 | 40 | no |  |  |
| scripts/CAD_basic.py | main_func | 15603 | 3 | no |  |  |
| scripts/CAD_basic.py | luping | 15610 | 45 | yes |  |  |
| scripts/CAD_basic.py | 魔方 | 15658 | 5 | no |  |  |
| scripts/CAD_basic.py | run_py | 15667 | 16 | no |  |  |
| scripts/CAD_basic.py | focus_cmdline | 15686 | 8 | yes |  |  |
| scripts/CAD_basic.py | activate_window_by_title | 15700 | 51 | yes |  |  |
| scripts/CAD_basic.py | click_in_window | 15754 | 51 | yes |  |  |
| scripts/CAD_basic.py | activate_and_click_aikeyun | 15812 | 31 | no |  |  |
| scripts/CAD_basic.py | drag_in_window_simple | 15848 | 37 | yes |  |  |
| scripts/CAD_basic.py | run_auto_explode_area | 15899 | 25 | yes |  |  |
| scripts/CAD_basic.py | list_all_windows | 15927 | 10 | no |  |  |
| scripts/CAD_basic.py | minimize_window | 15939 | 18 | yes |  |  |
| scripts/CAD_basic.py | maximize_autocad_window | 15958 | 32 | yes |  |  |
| scripts/CAD_basic.py | set_dwg_units_precision | 16013 | 20 | yes |  |  |
| scripts/CAD_basic.py | jd | 16035 | 2 | no |  |  |
| scripts/CAD_basic.py | list_dim_styles | 16041 | 14 | yes |  |  |
| scripts/CAD_basic.py | set_current_dimstyle_via_command | 16059 | 12 | yes |  |  |
| scripts/CAD_basic.py | set_current_text_style | 16075 | 14 | yes |  |  |
| scripts/CAD_basic.py | huoqu_ziti_style | 16092 | 5 | no |  |  |
| scripts/CAD_basic.py | create_text_style | 16118 | 46 | yes |  |  |
| scripts/CAD_basic.py | set_text_style_onlyshx | 16169 | 36 | yes |  |  |
| scripts/CAD_basic.py | set_text_style | 16209 | 24 | yes |  |  |
| scripts/CAD_basic.py | rename_conflicting_text_styles | 16251 | 95 | yes |  |  |
| scripts/CAD_basic.py | transfer_props_by_matchprop | 16510 | 68 | no |  |  |
| scripts/CAD_basic.py | run_dual_threads_1 | 16620 | 96 | yes |  |  |
| scripts/CAD_basic.py | cancel_cad_selection | 16720 | 13 | no |  |  |
| scripts/CAD_basic.py | close_wps_window_by_click | 16738 | 33 | yes |  |  |
| scripts/CAD_basic.py | min_w | 16780 | 20 | no |  |  |
| scripts/CAD_basic.py | ql | 16805 | 3 | no |  |  |
| scripts/CAD_basic.py | srhd | 16816 | 44 | yes |  |  |
| scripts/CAD_basic.py | srhd_p | 16864 | 45 | yes |  |  |
| scripts/CAD_basic.py | comtomath | 16912 | 11 | no |  |  |
| scripts/CAD_basic.py | p | 16924 | 7 | no |  |  |
| scripts/CAD_basic.py | fuzhi_chakan | 16940 | 24 | no |  |  |
| scripts/CAD_basic.py | celiang_wenzichangdu | 16968 | 13 | no |  |  |
| scripts/CAD_basic.py | celiang_wenzichangdu_write | 16985 | 15 | no |  |  |
| scripts/CAD_basic.py | qingkong_wenjianjia | 17006 | 16 | no |  |  |
| scripts/CAD_basic.py | get_bbox_info | 17027 | 53 | yes |  |  |
| scripts/CAD_basic.py | bbox_orientation_flag | 17083 | 20 | yes |  |  |
| scripts/CAD_basic.py | group_bbox_corners | 17106 | 94 | yes |  |  |
| scripts/CAD_basic.py | bbox_center_2 | 17234 | 6 | no |  |  |
| scripts/CAD_basic.py | bbox_center_3 | 17242 | 6 | yes |  |  |
| scripts/CAD_basic.py | safe_get_bbox | 17250 | 64 | yes |  |  |
| scripts/CAD_basic.py | resolve_log_level | 17394 | 5 | yes |  |  |
| scripts/CAD_basic.py | get_data_root | 17406 | 6 | yes |  |  |
| scripts/CAD_basic.py | _resolve_json_path | 17413 | 28 | yes |  |  |
| scripts/CAD_basic.py | extract_poly_data | 17446 | 26 | yes |  |  |
| scripts/CAD_basic.py | restore_poly_adaptive | 17474 | 66 | yes |  |  |
| scripts/CAD_basic.py | save_poly_list | 17548 | 23 | yes |  |  |
| scripts/CAD_basic.py | load_poly_list | 17572 | 21 | yes |  |  |
| scripts/CAD_basic.py | save_ctq | 17601 | 36 | yes |  |  |
| scripts/CAD_basic.py | load_ctq | 17639 | 75 | yes |  |  |
| scripts/CAD_basic.py | Redefine_standard_blocks | 17726 | 180 | yes |  |  |
| scripts/CAD_basic.py | get_sorted_titles_by_areas_final | 17915 | 81 | yes |  |  |
| scripts/CAD_basic.py | get_sorted_titles_ce | 18000 | 81 | yes |  |  |
| scripts/CAD_basic.py | batch_attsync_loop | 18087 | 81 | yes |  |  |
| scripts/CAD_basic.py | smart_select_polylines | 18176 | 79 | yes |  |  |
| scripts/CAD_basic.py | universal_select_polylines | 18257 | 68 | yes |  |  |
| scripts/CAD_basic.py | select_print_areas_maxrect_from_polylines | 18333 | 5 | yes |  |  |
| scripts/CAD_basic.py | select_maxrect_polylines_1 | 18341 | 267 | yes |  |  |
| scripts/CAD_basic.py | select_print_areas_paperspace | 18615 | 145 | yes |  |  |
| scripts/CAD_basic.py | select_standard_print_areas | 18766 | 277 | yes |  |  |
| scripts/CAD_basic.py | select_print_areas_from_blocks | 19048 | 217 | yes |  |  |
| scripts/CAD_basic.py | select_print_areas_from_layer | 19271 | 182 | yes |  |  |
| scripts/CAD_basic.py | select_print_areas_from_screen | 19458 | 179 | yes |  |  |
| scripts/CAD_basic.py | check_valid_rect_pro | 19644 | 62 | yes |  |  |
| scripts/CAD_basic.py | remove_duplicate_polylines | 19714 | 128 | yes |  |  |
| scripts/CAD_basic.py | universal_insert_labels_dispatch | 19848 | 182 | no |  |  |
| scripts/CAD_basic.py | insert_and_scale_labels_area_power | 20039 | 92 | yes |  |  |
| scripts/CAD_basic.py | insert_and_scale_labels_paper_space | 20145 | 100 | yes |  |  |
| scripts/CAD_basic.py | clean_blocks_until_vanished | 20248 | 83 | yes |  |  |
| scripts/CAD_basic.py | plcoor_to_com | 20334 | 35 | yes |  |  |
| scripts/CAD_basic.py | draw_pl_and_extract_info | 20372 | 76 | yes |  |  |
| scripts/CAD_basic.py | draw_pl_and_extract_from_entities | 20451 | 88 | yes |  |  |
| scripts/CAD_basic.py | insert_block_into_poly_area | 20542 | 53 | yes |  |  |
| scripts/CAD_basic.py | insert_block_into_poly_area | 20597 | 61 | yes |  |  |
| scripts/CAD_basic.py | compute_insert_factors | 20662 | 36 | yes |  |  |
| scripts/CAD_basic.py | get_factor_for_entity | 20701 | 6 | yes |  |  |
| scripts/CAD_basic.py | insert_company_label_common_block | 20714 | 52 | yes |  |  |
| scripts/CAD_basic.py | f1_insert_company_getwindow | 20773 | 48 | yes |  |  |
| scripts/CAD_basic.py | _find_shx_dialog | 20824 | 13 | yes |  |  |
| scripts/CAD_basic.py | _ignore_shx_dialog | 20840 | 7 | yes |  |  |
| scripts/CAD_basic.py | f2_delwindow | 20850 | 36 | yes |  |  |
| scripts/CAD_basic.py | run_dual_threads | 20889 | 61 | yes |  |  |
| scripts/CAD_basic.py | Insert_Company_Label_Common_Block | 20953 | 32 | yes |  |  |
| scripts/CAD_basic.py | clean_internal_polylines | 20992 | 37 | yes |  |  |
| scripts/CAD_basic.py | fill_block_attributes_with_tag_name | 21034 | 20 | yes |  |  |
| scripts/CAD_basic.py | _make_bind_dict_serializable | 21057 | 95 | yes |  |  |
| scripts/CAD_basic.py | normalize_core_title_blocks_by_layer | 21154 | 24 | yes |  |  |
| scripts/CAD_basic.py | explode_title_wrappers_to_core_layer | 21181 | 106 | yes |  |  |
| scripts/CAD_basic.py | repair_mp_insert | 21298 | 71 | yes |  |  |
| scripts/CAD_basic.py | repair_sp_insert | 21375 | 75 | yes |  |  |
| scripts/CAD_basic.py | smart_repair_frame_polyline_widths_m | 21457 | 193 | yes |  |  |
| scripts/CAD_basic.py | smart_repair_frame_polyline_widths_p | 21651 | 193 | yes |  |  |
| scripts/CAD_basic.py | cut_model_to_paper_and_switch | 21849 | 108 | yes |  |  |
| scripts/CAD_basic.py | _fallback_copy_method | 21961 | 30 | no |  |  |
| scripts/CAD_basic.py | cut_screen_selection_to_paper | 21998 | 87 | yes |  |  |
| scripts/CAD_basic.py | copy_layout_polylines_to_model | 22092 | 95 | yes |  |  |
| scripts/CAD_basic.py | clear_layout_objects | 22192 | 90 | yes |  |  |
| scripts/CAD_basic.py | clean_unused_blocks_global_scan | 22286 | 82 | yes |  |  |
| scripts/CAD_basic.py | smart_rebuild_print_info | 22374 | 119 | yes |  |  |
| scripts/CAD_basic.py | rebuild_print_area_title_mapping | 22501 | 157 | yes |  |  |
| scripts/CAD_basic.py | rebuild_print_area_title_mapping_paper | 22667 | 158 | yes |  |  |
| scripts/CAD_basic.py | build_header_map | 22860 | 14 | yes |  |  |
| scripts/CAD_basic.py | read_xlsx_to_dict | 22880 | 95 | yes |  |  |
| scripts/CAD_basic.py | write_dict_to_xlsx | 22977 | 120 | yes |  |  |
| scripts/CAD_basic.py | auto_export_excel_with_fallback | 23104 | 69 | yes |  |  |
| scripts/CAD_basic.py | build_full_print_dict_and_export_excel | 23181 | 344 | yes |  |  |
| scripts/CAD_basic.py | auto_process_drawing_names_by_style | 23532 | 101 | yes |  |  |
| scripts/CAD_basic.py | process_drawing_names_and_fill_titleblocks | 23640 | 237 | yes |  |  |
| scripts/CAD_basic.py | auto_import_excel_to_cad | 23882 | 103 | yes |  |  |
| scripts/CAD_basic.py | read_excel_and_update_cad_titleblocks | 23994 | 181 | yes |  |  |
| scripts/CAD_basic.py | auto_update_titleblock_format_by_style | 24182 | 70 | yes |  |  |
| scripts/CAD_basic.py | batch_update_block_attributes_config | 24257 | 141 | yes |  |  |
| scripts/CAD_basic.py | bianmulu_func1_h | 24406 | 196 | yes |  |  |
| scripts/CAD_basic.py | bianmulu_func2_h | 24608 | 257 | yes |  |  |
| scripts/CAD_basic.py | bianmulu_func3_h | 24870 | 166 | yes |  |  |
| scripts/CAD_basic.py | bianmulu_func4_h | 25041 | 259 | yes |  |  |
| scripts/CAD_basic.py | update_catalog_titleblocks_from_excel | 25310 | 171 | yes |  |  |
| scripts/CAD_basic.py | update_catalog_titleblocks_from_excel_y | 25502 | 147 | yes |  |  |
| scripts/CAD_basic.py | write_catalog_from_excel_to_cad | 25654 | 675 | yes |  |  |
| scripts/CAD_basic.py | read_catalog_template_config | 26333 | 93 | yes |  |  |
| scripts/CAD_basic.py | get_my_template_config_from_excel | 26483 | 78 | yes |  |  |
| scripts/CAD_basic.py | rename_drawings | 26568 | 104 | yes |  |  |
| scripts/CAD_basic.py | get_mouse_target_v3 | 26687 | 72 | yes |  |  |
| scripts/CAD_basic.py | safe_input_text | 26763 | 10 | no |  |  |
| scripts/CAD_basic.py | auto_setup_custom_paper_sizes | 26777 | 121 | yes |  |  |
| scripts/CAD_basic.py | list_current_printer_papers | 26929 | 57 | yes |  |  |
| scripts/CAD_basic.py | replace_cad_fonts_incremental | 26991 | 63 | no |  |  |
| scripts/CAD_basic.py | is_admin | 27054 | 6 | yes |  |  |
| scripts/CAD_basic.py | sanitize_filename | 27065 | 4 | yes |  |  |
| scripts/CAD_basic.py | export_model_window_pure | 27074 | 128 | yes |  |  |
| scripts/CAD_basic.py | export_model_window_lisp_fit | 27205 | 106 | yes |  |  |
| scripts/CAD_basic.py | export_layout_window_pure | 27318 | 128 | yes |  |  |
| scripts/CAD_basic.py | export_layout_window_pure_bianju | 27450 | 125 | yes |  |  |
| scripts/CAD_basic.py | export_layout_window_lisp_fit_v1 | 27578 | 161 | yes |  |  |
| scripts/CAD_basic.py | export_layout_window_lisp_fit | 27742 | 128 | yes |  |  |
| scripts/CAD_basic.py | print_batch_custom_list | 27873 | 232 | yes |  |  |
| scripts/CAD_basic.py | mark_print_areas_final | 28115 | 126 | yes |  |  |
| scripts/CAD_basic.py | generate_tarch_drawing_names_v5 | 28244 | 123 | yes |  |  |
| scripts/CAD_basic.py | print_dwg_file_model | 28378 | 124 | yes |  |  |
| scripts/CAD_basic.py | print_polylines_list | 28507 | 250 | yes |  |  |
| scripts/CAD_basic.py | print_dwg_file_layout | 28763 | 93 | yes |  |  |
| scripts/CAD_basic.py | print_layout_polylines_list | 28860 | 264 | yes |  |  |
| scripts/CAD_basic.py | print_layout_polylines_list_y | 29127 | 118 | yes |  |  |
| scripts/CAD_basic.py | smart_print_dispatch | 29250 | 105 | yes |  |  |
| scripts/CAD_check_standards.py | bianmulu_func4_h | 14 | 154 | yes | com,fileio |  |
| scripts/CAD_dev_standards.py | docstring_standard_example | 60 | 23 | yes | fileio |  |
| scripts/CAD_dev_standards.py | count_layers_demo | 91 | 42 | yes |  |  |
| scripts/CAD_dev_standards.py | _check_name_match | 134 | 9 | yes |  |  |
| scripts/CAD_dev_standards.py | draw_circle_standard_example | 159 | 25 | yes |  |  |
| scripts/CAD_dev_standards.py | architecture_full_demo | 192 | 35 | yes |  |  |
| scripts/CAD_Legacy_Runner.py | LegacyCADRunner.__init__ | 28 | 35 | no | com,fileio |  |
| scripts/CAD_Legacy_Runner.py | LegacyCADRunner.write | 65 | 6 | no |  |  |
| scripts/CAD_Legacy_Runner.py | LegacyCADRunner.flush | 72 | 1 | no | fileio |  |
| scripts/CAD_Legacy_Runner.py | LegacyCADRunner.run_in_thread | 75 | 10 | no | com,fileio |  |
| scripts/CAD_Legacy_Runner.py | LegacyCADRunner.gui_test_connection | 90 | 11 | yes | fileio |  |
| scripts/CAD_Legacy_Runner.py | LegacyCADRunner.gui_new_file | 102 | 16 | yes |  |  |
| scripts/CAD_Legacy_Runner.py | LegacyCADRunner.gui_save_as | 119 | 26 | yes |  |  |
| scripts/CAD_System_Queue - V30.py | LockManager.__init__ | 160 | 5 | no |  |  |
| scripts/CAD_System_Queue - V30.py | LockManager.try_acquire | 165 | 4 | no |  |  |
| scripts/CAD_System_Queue - V30.py | LockManager._write_lock | 169 | 5 | no |  |  |
| scripts/CAD_System_Queue - V30.py | LockManager.release | 174 | 5 | no |  |  |
| scripts/CAD_System_Queue - V30.py | LockManager.check_waiters | 179 | 1 | no |  |  |
| scripts/CAD_System_Queue - V30.py | LockManager.add_to_wait_list | 180 | 1 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.__init__ | 185 | 53 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner._ensure_bootstrap | 239 | 4 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.launch_idle | 244 | 10 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner._init_ui | 255 | 18 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.create_tab | 274 | 4 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.setup_dashboard | 280 | 27 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.setup_title_block_tab | 309 | 36 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.setup_catalog | 347 | 15 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.setup_print | 364 | 39 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.add_step_btn | 405 | 3 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.add_dragon_btn | 409 | 3 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.send_script_to_idle | 413 | 11 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.ask_attribute_config | 425 | 47 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.ask_detection_params | 476 | 26 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.run_macro | 505 | 464 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.refresh_workspace_paths | 970 | 36 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.log | 1007 | 5 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.monitor_waiters | 1013 | 4 | no |  |  |
| scripts/CAD_System_Queue - V30.py | MasterRunner.on_close | 1018 | 6 | no |  |  |
| scripts/CAD_System_Queue - V31.py | LockManager.__init__ | 162 | 5 | no |  |  |
| scripts/CAD_System_Queue - V31.py | LockManager.try_acquire | 167 | 4 | no |  |  |
| scripts/CAD_System_Queue - V31.py | LockManager._write_lock | 171 | 5 | no |  |  |
| scripts/CAD_System_Queue - V31.py | LockManager.release | 176 | 5 | no |  |  |
| scripts/CAD_System_Queue - V31.py | LockManager.check_waiters | 181 | 1 | no |  |  |
| scripts/CAD_System_Queue - V31.py | LockManager.add_to_wait_list | 182 | 1 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.__init__ | 187 | 53 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner._ensure_bootstrap | 241 | 4 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.launch_idle | 246 | 10 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner._init_ui | 257 | 18 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.create_tab | 276 | 4 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.setup_dashboard | 282 | 27 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.setup_title_block_tab | 311 | 36 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.setup_catalog | 349 | 15 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.setup_print | 366 | 39 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.add_step_btn | 407 | 3 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.add_dragon_btn | 411 | 3 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.send_script_to_idle | 415 | 11 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.ask_attribute_config | 427 | 47 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.ask_detection_params | 478 | 26 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.run_macro | 507 | 513 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.refresh_workspace_paths | 1021 | 36 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.log | 1058 | 5 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.monitor_waiters | 1064 | 4 | no |  |  |
| scripts/CAD_System_Queue - V31.py | MasterRunner.on_close | 1069 | 6 | no |  |  |
| scripts/CAD_System_Queue - V33.py | LockManager.__init__ | 161 | 5 | no |  |  |
| scripts/CAD_System_Queue - V33.py | LockManager.try_acquire | 166 | 4 | no |  |  |
| scripts/CAD_System_Queue - V33.py | LockManager._write_lock | 170 | 5 | no |  |  |
| scripts/CAD_System_Queue - V33.py | LockManager.release | 175 | 5 | no |  |  |
| scripts/CAD_System_Queue - V33.py | LockManager.check_waiters | 180 | 1 | no |  |  |
| scripts/CAD_System_Queue - V33.py | LockManager.add_to_wait_list | 181 | 1 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.__init__ | 186 | 67 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner._ensure_bootstrap | 254 | 4 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.launch_idle | 259 | 10 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner._init_ui | 270 | 25 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.create_tab | 296 | 4 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.setup_dashboard | 302 | 15 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.setup_datacenter | 319 | 51 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.setup_title_block_tab | 372 | 40 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.setup_catalog | 414 | 15 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.setup_print | 431 | 39 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.add_step_btn | 472 | 3 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.add_dragon_btn | 476 | 3 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.send_script_to_idle | 480 | 11 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.ask_attribute_config | 492 | 47 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.run_datacenter_macro | 541 | 143 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.run_macro | 686 | 325 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.refresh_workspace_paths | 1012 | 36 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.log | 1049 | 5 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.monitor_waiters | 1055 | 4 | no |  |  |
| scripts/CAD_System_Queue - V33.py | MasterRunner.on_close | 1060 | 6 | no |  |  |
| scripts/CAD_System_Queue.py | LockManager.__init__ | 161 | 5 | no |  |  |
| scripts/CAD_System_Queue.py | LockManager.try_acquire | 166 | 4 | no |  |  |
| scripts/CAD_System_Queue.py | LockManager._write_lock | 170 | 5 | no |  |  |
| scripts/CAD_System_Queue.py | LockManager.release | 175 | 5 | no |  |  |
| scripts/CAD_System_Queue.py | LockManager.check_waiters | 180 | 1 | no |  |  |
| scripts/CAD_System_Queue.py | LockManager.add_to_wait_list | 181 | 1 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.__init__ | 186 | 67 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner._ensure_bootstrap | 254 | 4 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.launch_idle | 259 | 10 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner._init_ui | 270 | 25 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.create_tab | 296 | 4 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.setup_dashboard | 303 | 54 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.setup_datacenter | 360 | 51 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.setup_title_block_tab | 413 | 40 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.setup_catalog | 455 | 15 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.setup_print | 472 | 39 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.add_step_btn | 513 | 3 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.add_dragon_btn | 517 | 3 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.send_script_to_idle | 521 | 11 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.ask_attribute_config | 533 | 47 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.run_datacenter_macro | 582 | 143 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.run_macro | 727 | 475 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.refresh_workspace_paths | 1207 | 36 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.log | 1244 | 5 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.monitor_waiters | 1250 | 4 | no |  |  |
| scripts/CAD_System_Queue.py | MasterRunner.on_close | 1255 | 6 | no |  |  |
| scripts/IDLE_bootstrap.py | run_script_in_main | 11 | 61 | yes | com,fileio |  |
| scripts/IDLE_bootstrap.py | start_listener | 73 | 24 | yes | com,fileio |  |
| scripts/Master_Orchestrator.py | AssistantVoice.__init__ | 57 | 16 | no | fileio |  |
| scripts/Master_Orchestrator.py | AssistantVoice.speak | 74 | 8 | yes | fileio |  |
| scripts/Master_Orchestrator.py | campaign_insert_labels | 87 | 21 | yes | fileio |  |
| scripts/Master_Orchestrator.py | campaign_build_catalog | 109 | 9 | yes |  |  |
| scripts/Master_Orchestrator.py | campaign_batch_print | 119 | 6 | yes |  |  |
| scripts/Master_Orchestrator.py | run_project_master_control | 128 | 60 | yes |  |  |
| scripts/修复codex脚本.py | fix_and_copy_newlines | 1 | 11 | no | com |  |
| scripts/修复codex脚本.py | create_py_file_from_txt | 13 | 11 | no | com |  |
| scripts/修复codex脚本.py | fix_and_convert | 26 | 15 | no | com |  |
| scripts/函数编写规范.py | li | 186 | 139 | yes |  |  |
| scripts/函数编写规范.py | get_acad_doc | 327 | 90 | yes |  |  |
| scripts/函数编写规范.py | _coinit_once | 422 | 11 | yes |  |  |
| scripts/函数编写规范.py | com_retry | 434 | 22 | yes |  |  |
| scripts/函数编写规范.py | select_tuceng | 468 | 47 | yes |  |  |
| scripts/函数编写规范.py | stc | 517 | 6 | yes |  |  |
| scripts/函数编写规范.py | select_kuai | 526 | 34 | yes |  |  |
| scripts/函数编写规范.py | select_text | 564 | 10 | yes |  |  |
| scripts/函数编写规范.py | select_mtext | 577 | 10 | yes |  |  |
| scripts/函数编写规范.py | select_pub_text_entities | 590 | 24 | yes |  |  |
| scripts/函数编写规范.py | collect_all_texts | 616 | 22 | yes |  |  |
| scripts/函数编写规范.py | select_line | 642 | 6 | yes |  |  |
| scripts/函数编写规范.py | select_circle | 650 | 6 | yes |  |  |
| scripts/函数编写规范.py | select_ellipse | 658 | 6 | yes |  |  |
| scripts/函数编写规范.py | select_spline | 666 | 6 | yes |  |  |
| scripts/函数编写规范.py | select_polyline_chuantong | 676 | 20 | yes |  |  |
| scripts/函数编写规范.py | select_polyline | 698 | 20 | yes |  |  |
| scripts/函数编写规范.py | normalize_rect | 725 | 8 | yes |  |  |
| scripts/函数编写规范.py | pt3 | 735 | 8 | yes |  |  |
| scripts/函数编写规范.py | select_entities_in_window | 748 | 74 | yes |  |  |
| scripts/函数编写规范.py | set_entity_grip_state_precise | 825 | 58 | yes |  |  |
| scripts/函数编写规范.py | safe_get_bbox | 886 | 64 | yes |  |  |
| scripts/函数编写规范.py | _maybe_cast | 1119 | 16 | yes |  |  |
| scripts/函数编写规范.py | cast_object | 1137 | 6 | yes |  |  |
| scripts/函数编写规范.py | get_object_property | 1145 | 20 | yes |  |  |
| scripts/函数编写规范.py | set_object_property | 1167 | 22 | yes |  |  |
| scripts/函数编写规范.py | get_attr | 1191 | 13 | yes |  |  |
| scripts/函数编写规范.py | set_attr | 1207 | 12 | yes |  |  |
| scripts/函数编写规范.py | brute_dump_tarch_props | 1224 | 27 | yes |  |  |
| scripts/函数编写规范.py | sort_coms_by_llcorner | 1257 | 36 | yes |  |  |
| scripts/函数编写规范.py | sort_coms_by_rbcorner | 1298 | 34 | yes |  |  |
| scripts/函数编写规范.py | sort_coms_by_center | 1334 | 46 | yes |  |  |
| scripts/函数编写规范.py | draw_point | 1390 | 19 | yes |  |  |
| scripts/函数编写规范.py | draw_line | 1411 | 18 | yes |  |  |
| scripts/函数编写规范.py | draw_circle | 1432 | 19 | yes |  |  |
| scripts/函数编写规范.py | draw_regular_polygon | 1454 | 36 | yes |  |  |
| scripts/函数编写规范.py | draw_lwpolyline | 1493 | 63 | yes |  |  |
| scripts/函数编写规范.py | draw_polyline | 1558 | 71 | yes |  |  |
| scripts/测试.py | generate_relation_list | 18 | 20 | no | com |  |
| scripts/脚本导航14版.py | ScriptNavigator.__init__ | 313 | 58 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._ensure_idle_bootstrap | 372 | 10 | yes |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._build_ui | 384 | 63 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._bind_shortcuts | 449 | 20 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._apply_fonts | 471 | 22 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._zoom_in | 494 | 4 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._zoom_out | 499 | 4 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_mousewheel_zoom | 504 | 6 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_mousewheel_sync | 512 | 2 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_scrollbar | 515 | 4 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_code_yscroll | 520 | 4 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._schedule_line_numbers | 526 | 2 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator.update_line_numbers | 529 | 18 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_key_release_update | 549 | 2 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_text_modified | 552 | 9 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._schedule_nav_refresh | 562 | 4 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._content_signature | 567 | 5 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._maybe_refresh_nav | 573 | 5 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._open_script | 580 | 7 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._open_new_file | 589 | 10 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator.load_script | 601 | 25 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._register_file_session | 627 | 11 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._unregister_current_file | 639 | 15 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator.save_script | 655 | 27 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._format_nav_label | 684 | 2 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._refresh_nav | 687 | 59 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._collapse_all | 747 | 5 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._expand_all | 753 | 7 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_tree_select | 761 | 8 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._nav_select_and_highlight | 770 | 5 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._highlight_line | 776 | 10 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._auto_resize_nav | 787 | 27 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._indent | 816 | 11 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._unindent | 828 | 16 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._comment_selection | 846 | 17 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._uncomment_selection | 864 | 16 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._get_selection_line_range | 881 | 10 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._leading_ws_len | 893 | 8 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._find_dialog | 903 | 6 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._do_find | 910 | 17 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._go_to_match | 928 | 4 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._find_next | 933 | 6 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._find_prev | 940 | 6 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._copy_all | 947 | 4 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._copy_sel | 952 | 11 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator.goto_line_prompt | 964 | 8 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator.run_in_idle | 974 | 55 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._send_script_to_idle | 1030 | 27 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_close | 1060 | 9 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._add_nav_tag | 1071 | 5 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._remove_nav_tag | 1077 | 3 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._clear_nav_highlight_only | 1081 | 4 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._clear_nav_and_code_highlight | 1086 | 3 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._scan_for_markers | 1090 | 39 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_click_image_marker | 1130 | 9 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._show_image_popup | 1140 | 50 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._hide_image_popup | 1191 | 10 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._toggle_maximize | 1202 | 12 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_popup_mousewheel | 1215 | 33 | no |  |  |
| scripts/脚本导航14版.py | ScriptNavigator._on_click_link | 1249 | 17 | no |  |  |
| scripts/脚本导航14版.py | clean_old_logs | 144 | 11 | no |  |  |
| scripts/脚本导航14版.py | _normalize_registry_path | 168 | 10 | no |  |  |
| scripts/脚本导航14版.py | _pid_exists | 180 | 17 | no |  |  |
| scripts/脚本导航14版.py | _read_registry_data | 199 | 10 | no |  |  |
| scripts/脚本导航14版.py | _write_registry_data | 211 | 5 | no |  |  |
| scripts/脚本导航14版.py | _cleanup_registry_data | 218 | 23 | no |  |  |
| scripts/脚本导航14版.py | _load_clean_registry | 243 | 5 | no |  |  |
| scripts/脚本导航14版.py | parse_mark_line | 253 | 9 | no |  |  |
| scripts/脚本导航14版.py | is_file_in_use | 272 | 28 | no |  |  |
| scripts/脚本导航14版.py | _tree_walk | 301 | 4 | no |  |  |
| system/cad_command_monitor.py | force_bring_to_front | 40 | 26 | yes | com,fileio |  |
| system/cad_command_monitor.py | send_nuclear_esc | 67 | 35 | yes | com,fileio |  |
| system/cad_command_monitor.py | get_active_cad_app | 103 | 7 | no |  |  |
| system/cad_command_monitor.py | analyze_state | 111 | 42 | yes |  |  |
| system/cad_command_monitor.py | is_already_running | 154 | 11 | no |  |  |
| system/cad_command_monitor.py | create_lock | 166 | 1 | no |  |  |
| system/cad_command_monitor.py | remove_lock | 167 | 1 | no |  |  |
| system/cad_command_monitor.py | main | 170 | 92 | no |  |  |
| system/CAD_com_utils - V10.py | SafeCOM.call | 126 | 3 | no |  |  |
| system/CAD_com_utils - V10.py | SafeCOM.list_selection | 131 | 11 | no |  |  |
| system/CAD_com_utils - V10.py | _retry_logic | 36 | 45 | yes | com,fileio |  |
| system/CAD_com_utils - V10.py | retry_on_busy | 83 | 38 | yes | com,fileio |  |
| system/CAD_com_utils - V10.py | retry_if_busy | 147 | 10 | yes |  |  |
| system/CAD_com_utils.py | LoggerHotSwapper.__init__ | 45 | 9 | no | com |  |
| system/CAD_com_utils.py | LoggerHotSwapper.mute | 55 | 4 | yes |  |  |
| system/CAD_com_utils.py | LoggerHotSwapper.unmute | 60 | 4 | yes |  |  |
| system/CAD_com_utils.py | LoggerHotSwapper.mute_mode | 67 | 3 | yes |  |  |
| system/CAD_com_utils.py | LoggerHotSwapper.mute_mode | 72 | 10 | yes | fileio |  |
| system/CAD_com_utils.py | LoggerHotSwapper.__getattr__ | 83 | 2 | no | com |  |
| system/CAD_com_utils.py | SafeCOM.call | 190 | 2 | no |  |  |
| system/CAD_com_utils.py | SafeCOM.list_selection | 194 | 10 | no |  |  |
| system/CAD_com_utils.py | _dummy_func | 37 | 2 | no |  |  |
| system/CAD_com_utils.py | silent_mode | 95 | 12 | yes |  |  |
| system/CAD_com_utils.py | _retry_logic | 114 | 44 | yes |  |  |
| system/CAD_com_utils.py | retry_on_busy | 160 | 26 | yes |  |  |
| system/CAD_com_utils.py | retry_if_busy | 206 | 2 | no |  |  |
| system/CAD_com_utils.py | alias | 214 | 11 | yes |  |  |
| system/CAD_com_utils.py | node | 241 | 13 | yes |  |  |
| system/CAD_com_utils.py | timeit | 258 | 25 | yes |  |  |
| system/CAD_com_utils.py | debuggable | 284 | 9 | yes |  |  |
| system/CAD_coordination - V33.py | CADGuard.__init__ | 197 | 19 | no |  |  |
| system/CAD_coordination - V33.py | CADGuard.__enter__ | 217 | 42 | no |  |  |
| system/CAD_coordination - V33.py | CADGuard.__exit__ | 260 | 61 | no |  |  |
| system/CAD_coordination - V33.py | FileGuard.__init__ | 331 | 5 | no |  |  |
| system/CAD_coordination - V33.py | FileGuard.__enter__ | 337 | 13 | no |  |  |
| system/CAD_coordination - V33.py | FileGuard.set_success | 351 | 3 | yes |  |  |
| system/CAD_coordination - V33.py | FileGuard.__exit__ | 355 | 38 | no |  |  |
| system/CAD_coordination - V33.py | wait_quiescent | 61 | 112 | yes | com,fileio |  |
| system/CAD_coordination - V33.py | run_safety_loop | 397 | 67 | yes |  |  |
| system/CAD_coordination - V33.py | send_cmd_with_sync | 469 | 28 | yes |  |  |
| system/CAD_coordination - V33.py | wait_document_opened | 499 | 22 | yes |  |  |
| system/CAD_coordination - V33.py | ensure_single_process | 524 | 16 | yes |  |  |
| system/CAD_coordination - V33.py | start_cad_with_dialog_killer | 541 | 9 | yes |  |  |
| system/CAD_coordination - V33.py | wait_command_done | 552 | 2 | no |  |  |
| system/CAD_coordination.py | CADGuard.__init__ | 211 | 19 | no |  |  |
| system/CAD_coordination.py | CADGuard.__enter__ | 231 | 42 | no |  |  |
| system/CAD_coordination.py | CADGuard.__exit__ | 274 | 61 | no |  |  |
| system/CAD_coordination.py | FileGuard.__init__ | 345 | 5 | no |  |  |
| system/CAD_coordination.py | FileGuard.__enter__ | 351 | 13 | no |  |  |
| system/CAD_coordination.py | FileGuard.set_success | 365 | 3 | yes |  |  |
| system/CAD_coordination.py | FileGuard.__exit__ | 369 | 38 | no |  |  |
| system/CAD_coordination.py | wait_quiescent | 55 | 56 | yes | com,fileio |  |
| system/CAD_coordination.py | wait_quiescent | 114 | 73 | yes |  |  |
| system/CAD_coordination.py | run_safety_loop | 411 | 67 | yes |  |  |
| system/CAD_coordination.py | send_cmd_with_sync | 483 | 28 | yes |  |  |
| system/CAD_coordination.py | wait_document_opened | 513 | 22 | yes |  |  |
| system/CAD_coordination.py | ensure_single_process | 538 | 16 | yes |  |  |
| system/CAD_coordination.py | start_cad_with_dialog_killer | 555 | 9 | yes |  |  |
| system/CAD_coordination.py | wait_command_done | 566 | 2 | no |  |  |
| system/CAD_selection - V10.py | com_retry | 202 | 10 | no |  |  |
| system/CAD_selection - V10.py | cast_object | 287 | 6 | yes |  |  |
| system/CAD_selection - V10.py | _maybe_cast | 295 | 45 | yes |  |  |
| system/CAD_selection - V10.py | to_vt_int | 344 | 2 | no |  |  |
| system/CAD_selection - V10.py | to_vt_variant | 347 | 2 | no |  |  |
| system/CAD_selection - V10.py | _to_vt_point | 350 | 3 | no |  |  |
| system/CAD_selection - V10.py | pt3 | 354 | 2 | no |  |  |
| system/CAD_selection - V10.py | normalize_rect | 357 | 4 | no |  |  |
| system/CAD_selection - V10.py | expand_rectangle | 362 | 4 | no |  |  |
| system/CAD_selection - V10.py | ss_select | 371 | 52 | yes |  |  |
| system/CAD_selection - V10.py | select_entities_through_point | 428 | 19 | yes |  |  |
| system/CAD_selection - V10.py | select_objects_in_window_area | 448 | 27 | yes |  |  |
| system/CAD_selection - V10.py | select_paperspace_objects_in_window | 476 | 27 | yes |  |  |
| system/CAD_selection - V10.py | pmxz | 504 | 3 | yes |  |  |
| system/CAD_selection - V10.py | get_last_n_objects | 508 | 17 | yes |  |  |
| system/CAD_selection - V10.py | last_obj | 526 | 6 | yes |  |  |
| system/CAD_selection - V10.py | select_tuceng | 537 | 9 | yes |  |  |
| system/CAD_selection - V10.py | stc | 547 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_kuai | 550 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_text | 553 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_mtext | 556 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_line | 559 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_circle | 562 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_ellipse | 565 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_spline | 568 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_polyline | 571 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_polyline_chuantong | 574 | 2 | no |  |  |
| system/CAD_selection - V10.py | select_all_texts_mixed | 577 | 12 | yes |  |  |
| system/CAD_selection - V10.py | select_pub_text_entities | 590 | 9 | yes |  |  |
| system/CAD_selection - V10.py | select_group_entities | 600 | 15 | yes |  |  |
| system/CAD_selection - V10.py | yin_to_xian_xuanze | 620 | 14 | yes |  |  |
| system/CAD_selection - V10.py | yin_to_xian_safe | 635 | 23 | yes |  |  |
| system/CAD_selection - V10.py | xian_to_yin_pickfirst | 659 | 11 | yes |  |  |
| system/CAD_selection - V10.py | select_entities_in_window | 671 | 15 | yes |  |  |
| system/CAD_selection - V10.py | highlight_entities_in_window | 687 | 3 | yes |  |  |
| system/CAD_selection - V10.py | highlight_entity_by_bbox | 691 | 10 | yes |  |  |
| system/CAD_selection - V10.py | set_entity_grip_state_precise | 702 | 10 | yes |  |  |
| system/CAD_selection - V10.py | isolate_modelspace_area | 713 | 8 | yes |  |  |
| system/CAD_selection - V10.py | unhide_all | 722 | 19 | yes |  |  |
| system/CAD_selection - V10.py | _resolve_attr_case_insensitive | 883 | 36 | yes |  |  |
| system/CAD_selection - V10.py | get_attr | 920 | 19 | yes |  |  |
| system/CAD_selection - V10.py | set_attr | 940 | 19 | yes |  |  |
| system/CAD_selection - V10.py | get_object_property | 961 | 14 | yes |  |  |
| system/CAD_selection - V10.py | set_object_property | 977 | 16 | yes |  |  |
| system/CAD_selection - V10.py | brute_dump_tarch_props | 996 | 10 | yes |  |  |
| system/CAD_selection.py | cast_object | 279 | 2 | no |  |  |
| system/CAD_selection.py | _maybe_cast | 282 | 27 | yes |  |  |
| system/CAD_selection.py | to_vt_int | 311 | 2 | no |  |  |
| system/CAD_selection.py | to_vt_variant | 314 | 2 | no |  |  |
| system/CAD_selection.py | _to_vt_point | 317 | 3 | no |  |  |
| system/CAD_selection.py | pt3 | 321 | 2 | no |  |  |
| system/CAD_selection.py | normalize_rect | 324 | 4 | no |  |  |
| system/CAD_selection.py | expand_rectangle | 329 | 4 | no |  |  |
| system/CAD_selection.py | com_retry | 335 | 11 | yes |  |  |
| system/CAD_selection.py | current_space_only | 348 | 38 | yes |  |  |
| system/CAD_selection.py | ss_select | 395 | 48 | yes |  |  |
| system/CAD_selection.py | select_entities_through_point | 449 | 15 | yes |  |  |
| system/CAD_selection.py | select_objects_in_window_area | 467 | 22 | yes |  |  |
| system/CAD_selection.py | select_paperspace_objects_in_window | 491 | 28 | yes |  |  |
| system/CAD_selection.py | pmxz | 520 | 2 | no |  |  |
| system/CAD_selection.py | get_last_n_objects | 524 | 17 | yes |  |  |
| system/CAD_selection.py | last_obj | 542 | 5 | no |  |  |
| system/CAD_selection.py | select_tuceng | 554 | 5 | yes |  |  |
| system/CAD_selection.py | stc | 560 | 2 | no |  |  |
| system/CAD_selection.py | select_kuai | 564 | 2 | no |  |  |
| system/CAD_selection.py | select_text | 566 | 2 | no |  |  |
| system/CAD_selection.py | select_mtext | 568 | 2 | no |  |  |
| system/CAD_selection.py | select_line | 570 | 2 | no |  |  |
| system/CAD_selection.py | select_circle | 572 | 2 | no |  |  |
| system/CAD_selection.py | select_ellipse | 574 | 2 | no |  |  |
| system/CAD_selection.py | select_spline | 576 | 2 | no |  |  |
| system/CAD_selection.py | select_polyline | 578 | 2 | no |  |  |
| system/CAD_selection.py | select_polyline_chuantong | 580 | 2 | no |  |  |
| system/CAD_selection.py | select_all_texts_mixed | 583 | 7 | no |  |  |
| system/CAD_selection.py | select_pub_text_entities | 591 | 8 | no |  |  |
| system/CAD_selection.py | select_group_entities | 602 | 14 | no |  |  |
| system/CAD_selection.py | yin_to_xian_xuanze | 622 | 14 | yes |  |  |
| system/CAD_selection.py | yin_to_xian_safe | 638 | 20 | yes |  |  |
| system/CAD_selection.py | xian_to_yin_pickfirst | 659 | 10 | no |  |  |
| system/CAD_selection.py | select_entities_in_window | 670 | 15 | no |  |  |
| system/CAD_selection.py | highlight_entities_in_window | 686 | 2 | no |  |  |
| system/CAD_selection.py | highlight_entity_by_bbox | 689 | 9 | no |  |  |
| system/CAD_selection.py | set_entity_grip_state_precise | 699 | 9 | no |  |  |
| system/CAD_selection.py | isolate_modelspace_area | 709 | 7 | no |  |  |
| system/CAD_selection.py | unhide_all | 718 | 22 | no |  |  |
| system/CAD_selection.py | _resolve_attr_case_insensitive | 882 | 22 | no |  |  |
| system/CAD_selection.py | get_attr | 905 | 20 | no |  |  |
| system/CAD_selection.py | get_attr | 928 | 35 | yes |  |  |
| system/CAD_selection.py | set_attr | 967 | 19 | no |  |  |
| system/CAD_selection.py | get_object_property | 988 | 1 | no |  |  |
| system/CAD_selection.py | set_object_property | 989 | 1 | no |  |  |
| system/CAD_selection.py | brute_dump_tarch_props | 991 | 9 | no |  |  |
| system/common_logger - V1.1.py | setup_logger | 10 | 50 | yes | com,fileio |  |
| system/common_logger - V1.4.py | DebugContext.__init__ | 208 | 5 | no |  |  |
| system/common_logger - V1.4.py | DebugContext.is_ai | 215 | 3 | yes |  |  |
| system/common_logger - V1.4.py | DebugContext.is_human | 220 | 3 | yes |  |  |
| system/common_logger - V1.4.py | DebugContext.__enter__ | 224 | 5 | no |  |  |
| system/common_logger - V1.4.py | DebugContext.__exit__ | 230 | 24 | no |  |  |
| system/common_logger - V1.4.py | set_debug_mode | 33 | 5 | yes |  |  |
| system/common_logger - V1.4.py | set_debug_mode | 48 | 14 | yes | com |  |
| system/common_logger - V1.4.py | record_test_result | 84 | 60 | yes | fileio |  |
| system/common_logger - V1.4.py | setup_logger | 150 | 50 | yes |  |  |
| system/common_logger - V1.4.py | node | 258 | 19 | yes |  |  |
| system/common_logger.py | CriticalSection.__init__ | 136 | 29 | no |  |  |
| system/common_logger.py | CriticalSection.record | 166 | 2 | no |  |  |
| system/common_logger.py | CriticalSection.__enter__ | 169 | 3 | no |  |  |
| system/common_logger.py | CriticalSection.__exit__ | 173 | 24 | no |  |  |
| system/common_logger.py | set_debug_mode | 35 | 7 | no |  |  |
| system/common_logger.py | setup_logger | 46 | 20 | no | com |  |
| system/common_logger.py | record_test_result | 72 | 39 | no | com,fileio |  |
| system/common_logger.py | checkpoint | 115 | 19 | no |  |  |
| system/common_logger.py | node | 198 | 5 | no |  |  |
| system/licad - V10.py | AutoCadProxy.__init__ | 211 | 5 | no |  |  |
| system/licad - V10.py | AutoCadProxy.li | 220 | 58 | yes |  |  |
| system/licad - V10.py | AutoCadProxy.acad | 281 | 1 | no |  |  |
| system/licad - V10.py | AutoCadProxy.doc | 283 | 1 | no |  |  |
| system/licad - V10.py | AutoCadProxy.mp | 285 | 1 | no |  |  |
| system/licad - V10.py | AutoCadProxy.sp | 287 | 1 | no |  |  |
| system/licad - V10.py | AutoCadProxy.save_file | 294 | 10 | no |  |  |
| system/licad - V10.py | AutoCadProxy.save_file_as | 306 | 17 | no |  |  |
| system/licad - V10.py | AutoCadProxy.open_file | 325 | 28 | no |  |  |
| system/licad - V10.py | AutoCadProxy.close_file | 355 | 22 | no |  |  |
| system/licad - V10.py | AutoCadProxy.close_dwg_by_name | 378 | 10 | no |  |  |
| system/licad - V10.py | _coinit_once | 19 | 6 | yes | com |  |
| system/licad - V10.py | _retry_on_busy | 30 | 89 | yes | com,fileio |  |
| system/licad - V10.py | get_acad_doc | 126 | 79 | yes |  |  |
| system/licad - V10.py | li | 399 | 2 | no |  |  |
| system/licad - V10.py | save_file | 402 | 2 | no |  |  |
| system/licad - V10.py | save_file_as | 405 | 2 | no |  |  |
| system/licad - V10.py | open_file | 408 | 2 | no |  |  |
| system/licad - V10.py | close_file | 411 | 2 | no |  |  |
| system/licad - V10.py | close_dwg_by_name | 414 | 2 | no |  |  |
| system/licad - V10.py | retry_on_busy | 418 | 2 | no |  |  |
| system/licad - V20.py | SafeDocumentWrapper.__init__ | 87 | 2 | no |  |  |
| system/licad - V20.py | SafeDocumentWrapper.SendCommand | 90 | 15 | yes | fileio |  |
| system/licad - V20.py | SafeDocumentWrapper.__getattr__ | 106 | 6 | yes |  |  |
| system/licad - V20.py | SafeDocumentWrapper.__dir__ | 113 | 3 | yes |  |  |
| system/licad - V20.py | AutoCadProxy.__init__ | 122 | 3 | no |  |  |
| system/licad - V20.py | AutoCadProxy.li | 126 | 19 | yes |  |  |
| system/licad - V20.py | AutoCadProxy.doc | 147 | 9 | yes |  |  |
| system/licad - V20.py | AutoCadProxy.acad | 157 | 1 | no |  |  |
| system/licad - V20.py | AutoCadProxy.mp | 159 | 1 | no |  |  |
| system/licad - V20.py | AutoCadProxy.sp | 161 | 1 | no |  |  |
| system/licad - V20.py | AutoCadProxy.save_file | 166 | 5 | no |  |  |
| system/licad - V20.py | AutoCadProxy.save_file_as | 173 | 10 | no |  |  |
| system/licad - V20.py | AutoCadProxy.open_file | 185 | 19 | no |  |  |
| system/licad - V20.py | AutoCadProxy.close_file | 206 | 8 | no |  |  |
| system/licad - V20.py | AutoCadProxy.close_dwg_by_name | 215 | 7 | no |  |  |
| system/licad - V20.py | AutoCadProxy.SendCommand | 226 | 21 | yes |  |  |
| system/licad - V20.py | AutoCadProxy.force_update | 252 | 12 | yes |  |  |
| system/licad - V20.py | _coinit_once | 30 | 3 | no | com |  |
| system/licad - V20.py | get_acad_doc | 34 | 43 | yes | com,fileio |  |
| system/licad - V20.py | li | 274 | 1 | no |  |  |
| system/licad - V20.py | save_file | 275 | 1 | no |  |  |
| system/licad - V20.py | save_file_as | 276 | 1 | no |  |  |
| system/licad - V20.py | open_file | 277 | 1 | no |  |  |
| system/licad - V20.py | close_file | 278 | 1 | no |  |  |
| system/licad - V20.py | close_dwg_by_name | 279 | 1 | no |  |  |
| system/licad.py | SafeDocumentWrapper.__init__ | 310 | 2 | no |  |  |
| system/licad.py | SafeDocumentWrapper.SendCommand | 313 | 10 | no |  |  |
| system/licad.py | SafeDocumentWrapper.__getattr__ | 324 | 2 | no |  |  |
| system/licad.py | SafeDocumentWrapper.__dir__ | 327 | 2 | no |  |  |
| system/licad.py | AutoCadProxy.__init__ | 335 | 5 | no |  |  |
| system/licad.py | AutoCadProxy.li | 341 | 31 | yes |  |  |
| system/licad.py | AutoCadProxy.acad | 375 | 1 | no |  |  |
| system/licad.py | AutoCadProxy.doc | 378 | 4 | yes |  |  |
| system/licad.py | AutoCadProxy.raw_doc | 384 | 4 | yes |  |  |
| system/licad.py | AutoCadProxy.mp | 390 | 1 | no |  |  |
| system/licad.py | AutoCadProxy.sp | 393 | 1 | no |  |  |
| system/licad.py | AutoCadProxy.msp | 396 | 1 | no |  |  |
| system/licad.py | AutoCadProxy.save_file | 401 | 8 | no |  |  |
| system/licad.py | AutoCadProxy.save_file_as | 411 | 11 | no |  |  |
| system/licad.py | AutoCadProxy.open_file | 424 | 15 | no |  |  |
| system/licad.py | AutoCadProxy.close_file | 441 | 11 | no |  |  |
| system/licad.py | AutoCadProxy.close_dwg_by_name | 453 | 5 | no |  |  |
| system/licad.py | _coinit_once | 31 | 3 | no |  |  |
| system/licad.py | get_acad_doc | 39 | 47 | yes | com,fileio |  |
| system/licad.py | get_acad_doc | 89 | 86 | yes | fileio |  |
| system/licad.py | get_acad_doc | 177 | 126 | yes |  |  |
| system/licad.py | li | 465 | 1 | no |  |  |
| system/licad.py | save_file | 466 | 1 | no |  |  |
| system/licad.py | save_file_as | 467 | 1 | no |  |  |
| system/licad.py | open_file | 468 | 1 | no |  |  |
| system/licad.py | close_file | 469 | 1 | no |  |  |
| system/licad.py | close_dwg_by_name | 470 | 1 | no |  |  |
| system/licad.py | retry_on_busy | 473 | 3 | yes |  |  |