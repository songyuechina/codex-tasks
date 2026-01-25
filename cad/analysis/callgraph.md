# 模块内调用关系（简版）

## library/cad_annotation.py
- add_dim_aligned -> vtpnt
- add_dim_angular -> vtpnt
- add_dim_diametric -> vtpnt
- add_dim_radial -> vtpnt
- add_dim_rotated -> vtpnt
- batch_modify_text -> set_text_content, set_text_height, set_text_rotation
- create_table -> vtpnt
- write_cad_text -> vtpnt
- write_mtext -> vtpnt

## library/cad_blocks.py
- attsync_block_instance -> attsync_block_instance_base
- count_blocks_by_type -> get_block_name
- delete_block_instances_and_definition_retry -> get_block_name
- generate_block_report -> count_blocks_by_type
- get_all_block_names -> get_all_block_definitions
- safe_explode_retry -> _atomic_explode_and_delete

## library/cad_control.py
- activate_and_click_aikeyun -> activate_window_by_title
- celiang_wenzichangdu_write -> celiang_wenzichangdu
- drag_in_window_simple -> activate_window_by_title
- jd -> set_dwg_units_precision
- l -> set_autocad_window_to_top_left
- luping -> activate_window_by_title, main_func, minimize_all_windows_d, restore_and_position
- p -> comtomath
- r -> set_idle_window_to_top_right
- r2 -> place_obs_bottom_right
- xieweixin -> activate_window_by_title, copy_to_clipboard
- xuanqun -> activate_window_by_title, copy_to_clipboard
- 主操作函数 -> activate_window_by_title, click_and_find_image_shape, fs, restore_and_position, xieweixin, xuanqun

## library/cad_geometry.py
- analyze_polygon_branches -> deduplicate_vertices, same_point
- are_all_vertices_inside -> get_unique_vertices_from_pl_com, point_in_polygon
- calculate_absolute_angle -> same_point
- calculate_relative_angle -> same_point
- check_strict_standard_size -> define_rectangle_by_diagonal, find_max_point, find_min_point
- concavity_angle -> concavity_measure, get_adjacent_points, get_auxiliary_point
- deduplicate_vertices -> same_point
- distribute_points_on_entity -> distance
- draw_polygon_as_polyline -> same_point
- draw_polyline -> same_point
- extract_polygon_from_lines -> deduplicate_vertices, same_point
- find_isolated_intersections -> same_point
- find_lines_angle -> calculate_absolute_angle
- find_lines_sharing_point -> calculate_relative_angle
- find_rightbottom_closed_polygon -> calculate_absolute_angle, find_lines_angle, find_rightbottom_point, find_successor_line_max, same_point
- find_successor_line_max -> calculate_relative_angle, find_lines_sharing_point, same_point
- find_successor_line_min -> calculate_relative_angle, is_nearly_equal
- get_adjacent_points -> normalize_polygon
- get_auxiliary_point -> line_segment_intersection_2d, normalize_polygon, point_in_polygon
- get_entity_geometry_info -> get_spline_length_by_conversion
- get_outer_contour -> find_lines_angle, find_rightbottom_point, find_successor_line_min, is_nearly_equal
- get_texts_in_polyline -> TDbMText_content, get_unique_vertices_from_pl_com, point_in_polygon
- lines_to_polylines -> convert_lines_to_points, draw_polyline, merge_segments_new
- main -> get_cad_app, get_dimensions, sort_coms_by_llcorner
- panduan_shuxiangkuang -> find_max_point, find_min_point
- point_in_polygon -> normalize_polygon
- polyline_sort -> find_min_point
- process_final -> draw_polygon_as_polyline, explode_polylines, extract_polygon_from_lines, process_polygons, subtract_line_sets
- process_polygons -> analyze_polygon_branches, draw_polygon_as_polyline, find_rightbottom_closed_polygon, find_rightbottom_point, remove_lines_in_LBv
- remove_lines_in_LBv -> same_point
- same_line -> same_point
- split_hexagon_combined -> area_of, get_unique_vertices_from_pl_com, simplify_polygon, split_orthogonal_hexagon, split_orthogonal_hexagon_vertical
- split_orthogonal_hexagon -> concavity_angle, normalize_polygon
- split_orthogonal_hexagon_vertical -> concavity_angle, normalize_polygon
- subtract_line_sets -> same_line
- two_plines_making_rectangle -> same_point

## library/cad_objects.py
- common_group_entities_sorted -> nametogroup
- copy_group_S1_from_doc1_to_doc2 -> add_objects_to_group, get_handle_object_map
- ensure_list -> ensure_list
- get_boundingbox_from_group -> get_boundingbox_from_objects
- get_com_from_groupname -> nametogroup
- get_com_from_groupname_by_type -> nametogroup
- get_group_entities_sorted -> get_com_from_groupname_by_type, sort_entities_by_position
- get_group_entities_sorted_by_type_and_bbox -> nametogroup
- get_named_object -> convert_named_dict
- is_printApp_xdata_com -> get_xdata
- set_xdata_tab -> set_xdata

## library/tarch_building.py
- TDb_single_line_variable_wall -> draw_tarch_wall
- _load_cache_from_disk -> _get_dynamic_cache_path
- _save_cache_to_disk -> _get_dynamic_cache_path
- convert_lines_to_walls -> draw_tarch_wall, set_walls_thickness
- insert_tarch_door_universal -> _activate_cad_safe, _get_dynamic_cache_path, _load_cache_from_disk, _save_cache_to_disk, _wait_for_user_hover
- insert_tarch_window -> insert_tarch_door
- insert_tarch_window_lisp_mode -> activate_cad_middle_click
- run_tupdspace_for_tz_room_in_rect -> run_auto_TUPDSPACE_with_coord

## scripts/apply_modifications.py
- apply_modifications -> create_backup, find_function_range, read_file, write_file

## scripts/auto_TUPDSPACE.py
- auto_tupdspace_with_repair -> activate_autocad_window, run_tupdspace_flow

## scripts/CAD_basic.py
- Insert_Company_Label_Common_Block -> run_dual_threads
- Redefine_standard_blocks -> batch_attsync_loop, cancel_cad_selection, redefine_block_with_entities, safe_delete, separate_entities_by_block_names
- TDbMText_content -> explode_single_object_marker
- _resolve_json_path -> get_data_root
- activate_and_click_aikeyun -> activate_window_by_title
- add_entities_to_block_definition_explode -> ensure_list
- add_entities_to_block_direct -> ensure_list
- add_object_to_group -> vtlist
- add_objects_to_group -> vtlist
- analyze_polygon_branches -> deduplicate_vertices, same_point
- are_all_vertices_inside -> get_unique_vertices_from_pl_com, point_in_polygon
- attsync_block_instance -> attsync_block_instance_base
- auto_export_excel_with_fallback -> build_full_print_dict_and_export_excel, smart_rebuild_print_info
- auto_import_excel_to_cad -> read_excel_and_update_cad_titleblocks, smart_rebuild_print_info
- auto_process_drawing_names_by_style -> process_drawing_names_and_fill_titleblocks, smart_rebuild_print_info
- auto_setup_custom_paper_sizes -> get_mouse_target_v3, safe_input_text
- auto_update_titleblock_format_by_style -> batch_update_block_attributes_config, smart_rebuild_print_info
- automate_window_with_pywinauto_t3 -> get_acad_process_id
- automate_window_with_pywinauto_t7 -> get_acad_process_id
- batch_attsync_loop -> attsync_block_instance
- batch_update_block_attributes_config -> attsync_block_instance, update_block_def_attributes_safe
- bianmulu_func1_h -> select_maxrect_polylines_1, smart_rebuild_print_info
- bianmulu_func2_h -> ensure_layer, insert_and_scale_labels_area_power, lines_to_polylines, rebuild_print_area_title_mapping, select_maxrect_polylines_1, smart_repair_frame_polyline_widths_m, update_catalog_titleblocks_from_excel
- bianmulu_func3_h -> rebuild_print_area_title_mapping, write_catalog_from_excel_to_cad
- bianmulu_func4_h -> select_maxrect_polylines_1, select_print_areas_paperspace
- build_full_print_dict_and_export_excel -> generate_name_and_ratio_from_com, get_block_attributes_dict
- calculate_absolute_angle -> same_point
- calculate_relative_angle -> same_point
- celiang_wenzichangdu -> vtpnt
- celiang_wenzichangdu_write -> celiang_wenzichangdu, vtpnt
- check_strict_standard_size -> define_rectangle_by_diagonal, find_max_point, find_min_point
- clean_blocks_until_vanished -> delete_block_instances_and_definition_retry
- clean_internal_polylines -> safe_delete
- close_all_cad_processes -> jingchengshu_wenjian
- common_group_entities_sorted -> nametogroup
- concavity_angle -> concavity_measure, get_adjacent_points, get_auxiliary_point
- connect_lines_to_polyline_if_closed -> vtFloat
- copy_group_S1_from_doc1_to_doc2 -> add_objects_to_group, get_handle_object_map
- copy_layout_polylines_to_model -> ensure_layer
- create_block_from_list_cmd -> ensure_list, group_bbox_corners
- create_block_from_region_cad -> group_bbox_corners
- create_block_from_region_cmd -> group_bbox_corners
- create_block_with_basepoint -> vtpnt
- create_block_with_triangle_and_text -> vtpnt
- create_layers_from_list -> get_acad_doc
- create_new_block_with_insert_and_line -> vtpnt
- cut_model_to_paper_and_switch -> _fallback_copy_method
- cut_screen_selection_to_paper -> vtobj
- deduplicate_vertices -> same_point
- delete_block_instances_and_definition_retry -> get_acad_doc, get_block_name, safe_delete
- delete_layers_from_list -> get_acad_doc
- dim_by_points -> activate_window_by_title, get_acad_doc
- distribute_points_on_entity -> distance, vtpnt
- drag_in_window_simple -> activate_window_by_title
- draw_circle -> vtpnt
- draw_line -> vtpnt
- draw_pl_and_extract_from_entities -> generate_name_and_ratio_from_com, plcoor_to_com
- draw_point -> vtpnt
- draw_polygon_as_polyline -> same_point
- draw_polyline -> same_point
- ensure_list -> ensure_list
- ensure_typelib_from_running -> _coinit_once
- explode_title_wrappers_to_core_layer -> safe_explode_and_delete
- export_model_window_lisp_fit -> draw_lwpolyline
- export_model_window_pure -> draw_lwpolyline
- extract_polygon_from_lines -> deduplicate_vertices, same_point
- f1_insert_company_getwindow -> insert_company_label_common_block
- f2_delwindow -> _find_shx_dialog, _ignore_shx_dialog
- find_fake_intersection_regions -> ensure_layer, vtpnt
- find_isolated_intersections -> same_point
- find_lines_angle -> calculate_absolute_angle
- find_lines_sharing_point -> calculate_relative_angle
- find_rightbottom_closed_polygon -> calculate_absolute_angle, find_lines_angle, find_rightbottom_point, find_successor_line_max, same_point
- find_successor_line_max -> calculate_relative_angle, find_lines_sharing_point, same_point
- find_successor_line_min -> calculate_relative_angle, is_nearly_equal
- fuzhi_chakan -> vtpnt
- g -> get_pmxz_group_bbox
- generate_tarch_drawing_names_v5 -> safe_get_bbox, vtpnt
- get_acad_doc -> _coinit_once
- get_adjacent_points -> normalize_polygon
- get_all_block_names -> get_all_block_definitions
- get_auxiliary_point -> line_segment_intersection_2d, normalize_polygon, point_in_polygon
- get_boundingbox_from_group -> get_boundingbox_from_objects
- get_com_from_groupname -> nametogroup
- get_com_from_groupname_by_type -> nametogroup
- get_entity_geometry_info -> get_spline_length_by_conversion
- get_entity_rgb -> aci_to_rgb
- get_group_entities_sorted -> get_com_from_groupname_by_type, sort_entities_by_position
- get_group_entities_sorted_by_type_and_bbox -> bbox_center_2, nametogroup
- get_named_object -> convert_named_dict
- get_outer_contour -> find_lines_angle, find_rightbottom_point, find_successor_line_min, is_nearly_equal
- get_pmxz_group_bbox -> group_bbox_corners
- get_sorted_titles_by_areas_final -> generate_name_and_ratio_from_com, select_print_areas_maxrect_from_polylines, sort_coms_by_llcorner
- get_sorted_titles_ce -> generate_name_and_ratio_from_com, select_print_areas_maxrect_from_polylines, sort_coms_by_llcorner
- get_texts_in_polyline -> TDbMText_content, get_unique_vertices_from_pl_com, point_in_polygon
- insert_and_explode_dwg -> safe_get_bbox
- insert_and_scale_labels_area_power -> select_maxrect_polylines_1
- insert_and_scale_labels_paper_space -> insert_and_scale_labels_area_power, select_print_areas_paperspace
- insert_company_label_common_block -> draw_pl_and_extract_info, insert_and_explode_dwg
- is_printApp_xdata_com -> get_xdata
- jd -> set_dwg_units_precision
- l -> set_autocad_window_to_top_left
- lines_to_polylines -> convert_lines_to_points, draw_polyline, merge_segments_new, safe_delete
- load_ctq -> _resolve_json_path, restore_poly_adaptive, sort_coms_by_llcorner
- load_poly_list -> _resolve_json_path, restore_poly_adaptive
- luping -> activate_window_by_title, main_func, minimize_all_windows_d, restore_and_position
- main -> get_cad_app, get_dimensions, sort_coms_by_llcorner
- mark_print_areas_final -> draw_circle, draw_lwpolyline, safe_get_bbox, write_cad_text
- move_entities_in_region -> vtpnt
- p -> comtomath
- panduan_shuxiangkuang -> find_max_point, find_min_point
- plcom_to_coor -> ensure_list
- point_in_polygon -> normalize_polygon
- polyline_sort -> find_min_point
- print_batch_custom_list -> print_dwg_file_layout, print_dwg_file_model
- print_dwg_file_layout -> print_layout_polylines_list, smart_rebuild_print_info
- print_dwg_file_model -> print_polylines_list, smart_rebuild_print_info
- print_layout_polylines_list -> activate_window_by_title, export_layout_window_lisp_fit_v1, generate_name_and_ratio_from_com, get_block_attributes_dict, minimize_all_windows, safe_get_bbox
- print_layout_polylines_list_y -> export_layout_window_lisp_fit, safe_get_bbox
- print_polylines_list -> activate_window_by_title, export_layout_window_lisp_fit, export_model_window_lisp_fit, generate_name_and_ratio_from_com, get_block_attributes_dict, minimize_all_windows, safe_get_bbox
- process_drawing_names_and_fill_titleblocks -> generate_name_and_ratio_from_com, set_attribute_mtext, sort_coms_by_llcorner, sort_coms_by_rbcorner
- process_final -> draw_polygon_as_polyline, explode_polylines, extract_polygon_from_lines, process_polygons, subtract_line_sets
- process_polygons -> analyze_polygon_branches, draw_polygon_as_polyline, find_rightbottom_closed_polygon, find_rightbottom_point, remove_lines_in_LBv
- ql -> ensure_layer
- r -> set_idle_window_to_top_right
- r2 -> place_obs_bottom_right
- read_excel_and_update_cad_titleblocks -> set_attribute_mtext
- rebuild_print_area_title_mapping -> select_maxrect_polylines_1
- rebuild_print_area_title_mapping_paper -> select_print_areas_paperspace
- remove_duplicate_polylines -> safe_delete
- remove_lines_in_LBv -> same_point
- repair_mp_insert -> ensure_layer, ensure_layer_model_only, lines_to_polylines, set_layer_with_retry, smart_repair_frame_polyline_widths_m
- repair_sp_insert -> ensure_layer, lines_to_polylines, smart_repair_frame_polyline_widths_p
- replace_cad_fonts_incremental -> close_all_cad_processes, is_admin
- safe_explode_retry -> _atomic_explode_and_delete
- same_line -> same_point
- save_ctq -> _resolve_json_path, extract_poly_data
- save_poly_list -> _resolve_json_path, ensure_list, extract_poly_data
- save_print_dict_generic -> serialize
- select_block_by_name -> vtInt, vtVariant
- select_maxrect_polylines_1 -> check_strict_standard_size, get_rectangular_polylines, remove_duplicate_polylines, safe_delete, sort_coms_by_llcorner
- select_print_areas_from_blocks -> ensure_layer, sort_coms_by_llcorner
- select_print_areas_from_layer -> ensure_layer, remove_duplicate_polylines, sort_coms_by_llcorner
- select_print_areas_from_screen -> ensure_layer, sort_coms_by_llcorner
- select_print_areas_maxrect_from_polylines -> select_maxrect_polylines_1
- select_print_areas_paperspace -> get_layout_rectangular_polylines_coords, remove_duplicate_polylines, sort_coms_by_llcorner
- select_standard_print_areas -> ensure_layer, remove_duplicate_polylines, sort_coms_by_llcorner
- serialize -> com_to_handle, serialize
- set_xdata_tab -> set_xdata
- smart_print_dispatch -> print_dwg_file_layout, print_dwg_file_model
- smart_rebuild_print_info -> load_ctq, rebuild_print_area_title_mapping, rebuild_print_area_title_mapping_paper, save_ctq
- smart_repair_frame_polyline_widths_m -> generate_name_and_ratio_from_com
- smart_repair_frame_polyline_widths_p -> generate_name_and_ratio_from_com
- smart_select_polylines -> load_poly_list, save_poly_list, universal_select_polylines
- split_hexagon_combined -> area_of, get_unique_vertices_from_pl_com, simplify_polygon, split_orthogonal_hexagon, split_orthogonal_hexagon_vertical
- split_orthogonal_hexagon -> concavity_angle, normalize_polygon
- split_orthogonal_hexagon_vertical -> concavity_angle, normalize_polygon
- srhd -> vtpnt
- srhd_p -> vtpnt
- st -> jd
- subtract_line_sets -> same_line
- test_draw_circle_and_wait -> _log, current_dwg_basename, draw_circle, timeout_and_log2
- timeout_and_log2 -> _kill_acad, _log
- transfer_props_by_matchprop -> expand_rectangle
- two_plines_making_rectangle -> same_point
- universal_insert_labels_dispatch -> insert_and_scale_labels_area_power, insert_and_scale_labels_paper_space, repair_mp_insert, repair_sp_insert, smart_select_polylines, speak_msg
- universal_select_polylines -> select_maxrect_polylines_1, select_print_areas_paperspace
- update_block_def_attributes_safe -> vtpnt
- update_block_def_attributes_v7 -> vtpnt
- update_catalog_titleblocks_from_excel -> generate_name_and_ratio_from_com, set_attribute_mtext
- update_catalog_titleblocks_from_excel_y -> set_attribute_mtext
- write_catalog_from_excel_to_cad -> generate_name_and_ratio_from_com, get_block_attributes_dict, read_catalog_template_config, write_cad_text
- write_dict_to_xlsx -> build_header_map
- xieweixin -> activate_window_by_title, copy_to_clipboard
- xuanqun -> activate_window_by_title, copy_to_clipboard
- zoom_window -> normalize_rect
- 主操作函数 -> activate_window_by_title, click_and_find_image_shape, fs, restore_and_position, xieweixin, xuanqun

## scripts/CAD_dev_standards.py
- count_layers_demo -> _check_name_match

## scripts/IDLE_bootstrap.py
- start_listener -> run_script_in_main

## scripts/Master_Orchestrator.py
- run_project_master_control -> campaign_batch_print, campaign_build_catalog, campaign_insert_labels

## scripts/修复codex脚本.py
- fix_and_convert -> create_py_file_from_txt, fix_and_copy_newlines

## scripts/函数编写规范.py
- _maybe_cast -> com_retry
- cast_object -> _maybe_cast
- collect_all_texts -> select_mtext, select_pub_text_entities, select_text
- get_acad_doc -> _coinit_once
- get_attr -> get_object_property
- get_object_property -> _maybe_cast, com_retry
- li -> draw_line, get_acad_doc, get_object_property
- select_entities_in_window -> li
- select_kuai -> get_acad_doc
- select_polyline -> get_acad_doc
- select_polyline_chuantong -> get_acad_doc
- select_pub_text_entities -> select_tuceng
- select_tuceng -> get_acad_doc
- set_attr -> set_object_property
- set_entity_grip_state_precise -> li, select_entities_in_window
- set_object_property -> _maybe_cast, com_retry
- stc -> select_tuceng

## scripts/脚本导航14版.py
- _cleanup_registry_data -> _pid_exists
- _load_clean_registry -> _cleanup_registry_data, _read_registry_data, _write_registry_data
- _tree_walk -> _tree_walk

## system/CAD_com_utils - V10.py
- retry_if_busy -> retry_on_busy
- retry_on_busy -> _retry_logic

## system/CAD_com_utils.py
- retry_if_busy -> retry_on_busy
- retry_on_busy -> _retry_logic

## system/cad_command_monitor.py
- main -> analyze_state, create_lock, get_active_cad_app, is_already_running, remove_lock, send_nuclear_esc
- send_nuclear_esc -> force_bring_to_front

## system/CAD_coordination - V33.py
- send_cmd_with_sync -> wait_quiescent
- start_cad_with_dialog_killer -> wait_quiescent
- wait_command_done -> wait_quiescent

## system/CAD_coordination.py
- send_cmd_with_sync -> wait_quiescent
- start_cad_with_dialog_killer -> wait_quiescent
- wait_command_done -> wait_quiescent

## system/CAD_selection - V10.py
- cast_object -> _maybe_cast
- expand_rectangle -> normalize_rect
- get_attr -> _maybe_cast, _resolve_attr_case_insensitive
- get_last_n_objects -> _maybe_cast, com_retry
- get_object_property -> _maybe_cast, com_retry
- highlight_entities_in_window -> select_entities_in_window
- highlight_entity_by_bbox -> expand_rectangle, highlight_entities_in_window
- isolate_modelspace_area -> select_objects_in_window_area, yin_to_xian_xuanze
- pmxz -> ss_select
- select_all_texts_mixed -> ss_select
- select_circle -> ss_select
- select_ellipse -> ss_select
- select_entities_in_window -> normalize_rect
- select_entities_through_point -> ss_select
- select_group_entities -> yin_to_xian_xuanze
- select_kuai -> ss_select
- select_line -> ss_select
- select_mtext -> ss_select
- select_objects_in_window_area -> ss_select
- select_paperspace_objects_in_window -> _maybe_cast, com_retry, normalize_rect, pt3, ss_select
- select_polyline -> ss_select
- select_polyline_chuantong -> ss_select
- select_pub_text_entities -> select_tuceng
- select_spline -> ss_select
- select_text -> ss_select
- select_tuceng -> ss_select
- set_attr -> _maybe_cast, _resolve_attr_case_insensitive
- set_object_property -> _maybe_cast, com_retry
- ss_select -> _maybe_cast, _to_vt_point, com_retry, to_vt_int, to_vt_variant
- stc -> select_tuceng
- unhide_all -> _maybe_cast, com_retry
- xian_to_yin_pickfirst -> _maybe_cast
- yin_to_xian_xuanze -> com_retry

## system/CAD_selection.py
- cast_object -> _maybe_cast
- expand_rectangle -> normalize_rect
- get_attr -> _maybe_cast, _resolve_attr_case_insensitive
- get_last_n_objects -> _maybe_cast
- get_object_property -> get_attr
- highlight_entities_in_window -> select_entities_in_window
- highlight_entity_by_bbox -> expand_rectangle, highlight_entities_in_window
- isolate_modelspace_area -> select_objects_in_window_area, yin_to_xian_xuanze
- pmxz -> ss_select
- select_all_texts_mixed -> ss_select
- select_circle -> ss_select
- select_ellipse -> ss_select
- select_entities_in_window -> normalize_rect
- select_entities_through_point -> ss_select
- select_group_entities -> yin_to_xian_xuanze
- select_kuai -> ss_select
- select_line -> ss_select
- select_mtext -> ss_select
- select_objects_in_window_area -> ss_select
- select_paperspace_objects_in_window -> _maybe_cast, normalize_rect, pt3, ss_select
- select_polyline -> ss_select
- select_polyline_chuantong -> ss_select
- select_pub_text_entities -> select_tuceng
- select_spline -> ss_select
- select_text -> ss_select
- select_tuceng -> ss_select
- set_attr -> _maybe_cast, _resolve_attr_case_insensitive
- set_object_property -> set_attr
- ss_select -> _maybe_cast, _to_vt_point, to_vt_int, to_vt_variant
- stc -> select_tuceng
- unhide_all -> _maybe_cast
- xian_to_yin_pickfirst -> _maybe_cast

## system/common_logger.py
- checkpoint -> record_test_result

## system/licad - V10.py
- get_acad_doc -> _coinit_once
- retry_on_busy -> _retry_on_busy

## system/licad - V20.py
- get_acad_doc -> _coinit_once

## system/licad.py
- get_acad_doc -> _coinit_once
