# 模块自动摘要（AST + 关键依赖）

说明：此文件为自动生成，用于快速浏览。详细分析见 notes.md。

## library/cad_annotation.py
- 描述: CAD注释与文字函数库
- 外部依赖: pythoncom, win32com
- COM: 可能使用 win32com/pythoncom
- 入口: 可能包含 __main__
- 函数: vtpnt, write_cad_text, write_mtext, add_dim_aligned, add_dim_rotated, add_dim_angular, add_dim_radial, add_dim_diametric, add_leader, get_text_content, set_text_content, get_text_height...

## library/cad_blocks.py
- 描述: 第六部分 图块操作
- 外部依赖: pythoncom
- COM: 可能使用 win32com/pythoncom
- 函数: get_block_name, huoqukuai_shuxing_zhi, update_block_def_attributes_safe, update_block_def_attributes_v7, attsync_block_instance, attsync_block_instance_base, set_attribute_mtext, get_block_attributes_dict, separate_entities_by_block_names, huoqu_kuai_pl, create_block_with_basepoint, create_block_with_triangle_and_text...

## library/cad_control.py
- 描述: 第七部分 综合控制
- 外部依赖: ctypes, imageio, subprocess, win32com
- COM: 可能使用 win32com/pythoncom
- 函数: fix_com_cache, delete_all_nul_under_folder, kill_dialog_killer, kill_python_script_by_name, kill_wps, close_all_excel_processes, safe_delete, move_entities_in_region, 圆点, 图纸背景, shitu_region, shitu_entity...

## library/cad_geometry.py
- 描述: 第三部分 线面分析
- 外部依赖: shapely
- 函数: compute_line_angle, draw_point, draw_line, draw_circle, draw_regular_polygon, prioritize_horizontal, get_spline_length_by_conversion, estimate_ellipse_length, get_entity_geometry_info, points_on_line_at_distance_3d, find_fake_intersection_regions, lines_daduan...

## library/cad_objects.py
- 描述: 第四部分 一般对象
- 外部依赖: pythoncom, win32com
- COM: 可能使用 win32com/pythoncom
- 函数: ensure_list, sort_tuples, multi_dim_tolerance_sort, get_ll_pt, get_center, sort_entities_by_position, get_line_start, sort_coms_by_llcorner, sort_coms_by_rbcorner, sort_coms_by_llcorner_custom, sort_coms_by_center, number_entities_by_order...

## library/execution_result.py
- 描述: 函数执行状态规范
- 类: ExecutionStatus, ExecutionResult
- 函数: success, failed, partial, error, with_execution_check

## library/tarch_building.py
- 描述: 天正建筑组件操作模块
- 外部依赖: subprocess, win32com
- COM: 可能使用 win32com/pythoncom
- 函数: dim_by_points, draw_tarch_wall, insert_tarch_door, insert_tarch_window, run_tupdspace_for_tz_room_in_rect, run_auto_TUPDSPACE_with_coord, TDb_single_line_variable_wall, convert_lines_to_walls, set_walls_thickness, activate_cad_middle_click, insert_tarch_window_lisp_mode, _get_dynamic_cache_path...

## library/test_monitor.py
- 描述: 测试监测模块
- 类: TestMonitor

## scripts/_temp_step1_select.py
- 描述: （无模块说明）

## scripts/_temp_step2_insert.py
- 描述: （无模块说明）

## scripts/_temp_task_runner.py
- 描述: （无模块说明）

## scripts/apply_modifications.py
- 描述: 脚本导航14版修改应用工具
- 入口: 可能包含 __main__
- 函数: create_backup, read_file, write_file, find_function_range, apply_modifications

## scripts/auto_TUPDSPACE.py
- 描述: （无模块说明）
- 入口: 可能包含 __main__
- 函数: activate_autocad_window, run_tupdspace_flow, auto_tupdspace_with_repair

## scripts/CAD_basic.py
- 描述: （无模块说明）
- 外部依赖: PIL, comtypes, ctypes, cv2, fitz, imageio, numpy, openpyxl, psutil, pythoncom, pywinauto, pywintypes, shapely, subprocess, tkinter, win32com
- COM: 可能使用 win32com/pythoncom
- UI: tkinter
- 类: _ComLiveProxy, CatalogConfigBuilder
- 函数: _cad_safe_print, _log, _kill_acad, connect_database_task, safe_save_cad, timeout_and_log2, test_draw_circle_and_wait, wait_quiescent_ceshi, complex_operation_demo, draw_infinite_spiral, speak_msg, com_to_handle...

## scripts/CAD_check_standards.py
- 描述: （无模块说明）
- 函数: bianmulu_func4_h

## scripts/CAD_dev_standards.py
- 描述: （无模块说明）
- 外部依赖: pythoncom, win32com
- COM: 可能使用 win32com/pythoncom
- 函数: docstring_standard_example, count_layers_demo, _check_name_match, draw_circle_standard_example, architecture_full_demo

## scripts/CAD_file_operations.py
- 描述: （无模块说明）

## scripts/CAD_Legacy_Runner.py
- 描述: （无模块说明）
- 外部依赖: tkinter
- UI: tkinter
- 入口: 可能包含 __main__
- 类: LegacyCADRunner

## scripts/CAD_System_Queue - V30.py
- 描述: （无模块说明）
- 外部依赖: ctypes, socket, subprocess, tkinter
- UI: tkinter
- 入口: 可能包含 __main__
- 类: LockManager, MasterRunner

## scripts/CAD_System_Queue - V31.py
- 描述: （无模块说明）
- 外部依赖: ctypes, socket, subprocess, tkinter
- UI: tkinter
- 入口: 可能包含 __main__
- 类: LockManager, MasterRunner

## scripts/CAD_System_Queue - V33.py
- 描述: （无模块说明）
- 外部依赖: ctypes, socket, subprocess, tkinter
- UI: tkinter
- 入口: 可能包含 __main__
- 类: LockManager, MasterRunner

## scripts/CAD_System_Queue.py
- 描述: （无模块说明）
- 外部依赖: ctypes, socket, subprocess, tkinter
- UI: tkinter
- 入口: 可能包含 __main__
- 类: LockManager, MasterRunner

## scripts/IDLE_bootstrap.py
- 描述: （无模块说明）
- 外部依赖: socket
- 函数: run_script_in_main, start_listener

## scripts/Insert_chart/insert_labels.py
- 描述: （无模块说明）

## scripts/Insert_chart/函数测试.py
- 描述: （无模块说明）

## scripts/Insert_chart/剥开.py
- 描述: （无模块说明）

## scripts/Insert_chart/插入20260115.py
- 描述: （无模块说明）

## scripts/Insert_chart/插入20260115f2.py
- 描述: （无模块说明）

## scripts/Insert_chart/选择函数的调试.py
- 描述: （无模块说明）

## scripts/Master_Orchestrator.py
- 描述: 【工程图纸自动化系统 - 总指挥中心】
- 入口: 可能包含 __main__
- 类: AssistantVoice
- 函数: campaign_insert_labels, campaign_build_catalog, campaign_batch_print, run_project_master_control

## scripts/修复codex脚本.py
- 描述: （无模块说明）
- 函数: fix_and_copy_newlines, create_py_file_from_txt, fix_and_convert

## scripts/函数编写规范.py
- 描述: 适用范围: AutoCAD Python Automation System (win32com based)
- 外部依赖: pythoncom, pywintypes, win32com
- COM: 可能使用 win32com/pythoncom
- 函数: li, get_acad_doc, _coinit_once, com_retry, select_tuceng, stc, select_kuai, select_text, select_mtext, select_pub_text_entities, collect_all_texts, select_line...

## scripts/测试.py
- 描述: （无模块说明）
- 函数: generate_relation_list

## scripts/脚本导航14版.py
- 描述: Script Navigator (Tree Edition) - BOM Fixed
- 外部依赖: PIL, ctypes, psutil, socket, subprocess, tkinter
- UI: tkinter
- 入口: 可能包含 __main__
- 类: ScriptNavigator
- 函数: clean_old_logs, _normalize_registry_path, _pid_exists, _read_registry_data, _write_registry_data, _cleanup_registry_data, _load_clean_registry, parse_mark_line, is_file_in_use, _tree_walk

## scripts/连接测试.py
- 描述: （无模块说明）

## scripts/选择测试错误.py
- 描述: （无模块说明）

## system/CAD_basic_operations.py
- 描述: （无模块说明）
- 入口: 可能包含 __main__

## system/CAD_com_utils - V10.py
- 描述: （无模块说明）
- 外部依赖: pythoncom, pywintypes
- COM: 可能使用 win32com/pythoncom
- 类: SafeCOM
- 函数: _retry_logic, retry_on_busy, retry_if_busy

## system/CAD_com_utils.py
- 描述: 引入 silent_mode 上下文管理器。
- 外部依赖: pythoncom, pywintypes
- COM: 可能使用 win32com/pythoncom
- 类: LoggerHotSwapper, SafeCOM
- 函数: _dummy_func, silent_mode, _retry_logic, retry_on_busy, retry_if_busy, alias, node, timeit, debuggable

## system/cad_command_monitor.py
- 描述: （无模块说明）
- 外部依赖: ctypes, psutil, pythoncom, win32com
- COM: 可能使用 win32com/pythoncom
- 入口: 可能包含 __main__
- 函数: force_bring_to_front, send_nuclear_esc, get_active_cad_app, analyze_state, is_already_running, create_lock, remove_lock, main

## system/CAD_coordination - V10.py
- 描述: （无模块说明）
- 入口: 可能包含 __main__

## system/CAD_coordination - V20.py
- 描述: （无模块说明）
- 入口: 可能包含 __main__

## system/CAD_coordination - V33.py
- 描述: CAD运行协同机制模块 (Licad + Logger 集成终极版)
- 外部依赖: psutil, pywintypes, subprocess
- COM: 可能使用 win32com/pythoncom
- 入口: 可能包含 __main__
- 类: CADGuard, FileGuard
- 函数: wait_quiescent, run_safety_loop, send_cmd_with_sync, wait_document_opened, ensure_single_process, start_cad_with_dialog_killer, wait_command_done

## system/CAD_coordination.py
- 描述: CAD运行协同机制模块 (Licad + Logger 集成终极版)
- 外部依赖: psutil, subprocess
- 入口: 可能包含 __main__
- 类: CADGuard, FileGuard
- 函数: wait_quiescent, wait_quiescent, run_safety_loop, send_cmd_with_sync, wait_document_opened, ensure_single_process, start_cad_with_dialog_killer, wait_command_done

## system/CAD_core.py
- 描述: （无模块说明）

## system/cad_dialog_killer.py
- 描述: （无模块说明）
- 入口: 可能包含 __main__

## system/CAD_enhanced_functions.py
- 描述: （无模块说明）
- 入口: 可能包含 __main__

## system/CAD_selection - V10.py
- 描述: （无模块说明）
- 外部依赖: pythoncom, pywintypes, win32com
- COM: 可能使用 win32com/pythoncom
- 函数: com_retry, cast_object, _maybe_cast, to_vt_int, to_vt_variant, _to_vt_point, pt3, normalize_rect, expand_rectangle, ss_select, select_entities_through_point, select_objects_in_window_area...

## system/CAD_selection.py
- 描述: （无模块说明）
- 外部依赖: pythoncom, win32com
- COM: 可能使用 win32com/pythoncom
- 入口: 可能包含 __main__
- 函数: cast_object, _maybe_cast, to_vt_int, to_vt_variant, _to_vt_point, pt3, normalize_rect, expand_rectangle, com_retry, current_space_only, ss_select, select_entities_through_point...

## system/common_logger - V1.1.py
- 描述: （无模块说明）
- 入口: 可能包含 __main__
- 函数: setup_logger

## system/common_logger - V1.4.py
- 描述: （无模块说明）
- 外部依赖: openpyxl
- 入口: 可能包含 __main__
- 类: DebugContext
- 函数: set_debug_mode, set_debug_mode, record_test_result, setup_logger, node

## system/common_logger.py
- 描述: （无模块说明）
- 外部依赖: openpyxl
- 类: CriticalSection
- 函数: set_debug_mode, setup_logger, record_test_result, checkpoint, node

## system/licad - V10.py
- 描述: （无模块说明）
- 外部依赖: pythoncom, win32com
- COM: 可能使用 win32com/pythoncom
- 类: AutoCadProxy
- 函数: _coinit_once, _retry_on_busy, get_acad_doc, li, save_file, save_file_as, open_file, close_file, close_dwg_by_name, retry_on_busy

## system/licad - V20.py
- 描述: （无模块说明）
- 外部依赖: pythoncom, win32com
- COM: 可能使用 win32com/pythoncom
- 类: SafeDocumentWrapper, AutoCadProxy
- 函数: _coinit_once, get_acad_doc, li, save_file, save_file_as, open_file, close_file, close_dwg_by_name

## system/licad.py
- 描述: （无模块说明）
- 外部依赖: pythoncom, win32com
- COM: 可能使用 win32com/pythoncom
- 类: SafeDocumentWrapper, AutoCadProxy
- 函数: _coinit_once, get_acad_doc, get_acad_doc, get_acad_doc, li, save_file, save_file_as, open_file, close_file, close_dwg_by_name, retry_on_busy

## system/project_setup.py
- 描述: （无模块说明）
- 类: PathConfig
