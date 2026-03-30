# Project Map

- Generated: `2026-03-21T22:22:56+08:00`
- Root: `D:\codex-tasks`
- Curated sections: `11`
- Indexed files: `199`
- Python files: `56`
- Markdown files: `42`

## Scope

This map focuses on source/docs memory assets and excludes DWG/PDF inputs, outputs, sessions, runtime logs and caches.

## Sections

### README.md

- Kind: `file`
- Summary: codex-tasks
- Files: `1`
- `README.md` [md] codex-tasks

### AGENTS.md

- Kind: `file`
- Summary: 适用范围：`D:/codex-tasks/`
- Files: `1`
- `AGENTS.md` [md] 适用范围：`D:/codex-tasks/`

### folder.meta.json

- Kind: `file`
- Summary: project-governor-workspace: DWG/CAD 自动化项目总管工作区。项目采用项目总管 + 四角色智能体能力层 + 领域执行工作区 + 运行监督链的架构，当前第一优先级领域是打印子系统。
- Files: `1`
- `folder.meta.json` [json] project-governor-workspace: DWG/CAD 自动化项目总管工作区。项目采用项目总管 + 四角色智能体能力层 + 领域执行工作区 + 运行监督链的架构，当前第一优先级领域是打印子系统。

### cad/folder.meta.json

- Kind: `file`
- Summary: cad-execution-kernel: CAD/DWG 执行内核目录。system 提供统一连接与守护能力，library 提供高层业务函数，tools 提供代码压缩/索引工具，scripts 负责具体业务链。
- Files: `1`
- `cad/folder.meta.json` [json] cad-execution-kernel: CAD/DWG 执行内核目录。system 提供统一连接与守护能力，library 提供高层业务函数，tools 提供代码压缩/索引工具，scripts 负责具体业务链。

### thoughtway

- Kind: `directory`
- Summary: governance-method-and-long-term-memory: 项目级治理、系统基础、规则与长期方法目录。这里应沉淀稳定共识，而不是只保存临时对话痕迹。
- Files: `20`
- `thoughtway/0227网页对话摘要.txt` [txt] 整体系统架构
- `thoughtway/CAD_RUNTIME_GUARD_RULES.md` [md] CAD Runtime Guard Rules
- `thoughtway/conversation_log.md` [md] Conversation Log
- `thoughtway/CURRENT_STATE.md` [md] Current State
- `thoughtway/folder.meta.json` [json] governance-method-and-long-term-memory: 项目级治理、系统基础、规则与长期方法目录。这里应沉淀稳定共识，而不是只保存临时对话痕迹。
- `thoughtway/functions_scripting_rules/01_bootstrap_import_rules_v2.md` [md] 01_bootstrap_import_rules.md
- `thoughtway/functions_scripting_rules/02_logging_rules_v2.md` [md] 02_logging_rules.md
- `thoughtway/functions_scripting_rules/03_entry_script_rules_v2.md` [md] 03_entry_script_rules.md
- `thoughtway/functions_scripting_rules/04_business_module_rules_v2.md` [md] 04_business_module_rules.md
- `thoughtway/functions_scripting_rules/05_exception_handling_rules_v2.md` [md] 05_exception_handling_rules.md
- `thoughtway/functions_scripting_rules/06_cad_connection_rules_licad_C_v2.md` [md] 06_cad_connection_rules_licad_C.md
- `thoughtway/meta_json_principles.md` [md] （meta.json 编写总原则）
- `thoughtway/PROJECT_GOVERNANCE.md` [md] Project Governance
- `thoughtway/PROJECT_MEMORY_SYSTEM.md` [md] Project Memory System
- `thoughtway/PROJECT_SUPERVISOR_ARCHITECTURE.md` [md] Project Supervisor Architecture
- `thoughtway/SYSTEM_FOUNDATIONS.md` [md] System Foundations
- `thoughtway/TERMINOLOGY.md` [md] 本文件用于统一 `D:/codex-tasks` 当前有效术语，避免把“智能体角色”和“任务执行链”混为一谈。
- `thoughtway/整体分析.txt` [txt] 20260301
- `thoughtway/新建文本文档.txt` [txt] 1) 最终顶层结构（确认版）
- `thoughtway/通用引导模板.txt` [txt] 通用引导模板（建议作为标准头部）：

### dwg_agents_ops

- Kind: `directory`
- Summary: role-agent-collaboration-layer: 项目总管可调度的角色能力层，不直接替代 CAD 内核，而是围绕 task_board、运行时状态与监督协议推进规划、编码、审查、测试。
- Files: `26`
- `dwg_agents_ops/agent_control/monitor_cli.py` [py] py funcs=6 classes=0 main=yes | top=read_json, parse_ts, age_text, board_counts, render_once, main
- `dwg_agents_ops/agent_control/RUNTIME_EVENT_PROTOCOL.md` [md] Runtime Event Protocol
- `dwg_agents_ops/agent_control/SUPERVISION.md` [md] Supervision Guide
- `dwg_agents_ops/agent_control/supervisor_cli.py` [py] py funcs=12 classes=1 main=yes | top=now_tag, ensure_dir, load_text, shrink_text, build_packet, make_command, DispatchResult
- `dwg_agents_ops/agent_control/task_board.json` [json] json file: task_board.json
- `dwg_agents_ops/agent_control/UNIFIED_CONTROL.md` [md] Unified Control
- `dwg_agents_ops/agents.example.toml` [toml] [planner]
- `dwg_agents_ops/Coder_Agent/agent_cli.py` [py] py funcs=0 classes=0 main=yes
- `dwg_agents_ops/Coder_Agent/README.md` [md] Coder Agent
- `dwg_agents_ops/Coder_Agent/role.toml` [toml] [role]
- `dwg_agents_ops/folder.meta.json` [json] role-agent-collaboration-layer: 项目总管可调度的角色能力层，不直接替代 CAD 内核，而是围绕 task_board、运行时状态与监督协议推进规划、编码、审查、测试。
- `dwg_agents_ops/Planner_Agent/agent_cli.py` [py] py funcs=0 classes=0 main=yes
- `dwg_agents_ops/Planner_Agent/README.md` [md] Planner Agent
- `dwg_agents_ops/Planner_Agent/role.toml` [toml] [role]
- `dwg_agents_ops/PROJECT_RESEARCH.md` [md] 项目研究纪要
- `dwg_agents_ops/README.md` [md] DWG Agents Ops
- `dwg_agents_ops/Reviewer_Agent/agent_cli.py` [py] py funcs=0 classes=0 main=yes
- `dwg_agents_ops/Reviewer_Agent/README.md` [md] Reviewer Agent
- `dwg_agents_ops/Reviewer_Agent/role.toml` [toml] [role]
- `dwg_agents_ops/Runtime_Guard_Agent/agent_cli.py` [py] py funcs=11 classes=0 main=yes | top=now_iso, write_json, append_jsonl, is_already_running, create_lock, remove_lock
- `dwg_agents_ops/Runtime_Guard_Agent/README.md` [md] Runtime Guard Agent
- `dwg_agents_ops/shared/__init__.py` [py] py funcs=0 classes=0 main=no
- `dwg_agents_ops/shared/runtime.py` [py] py funcs=31 classes=2 main=no | top=now_iso, read_json, write_json, load_role_config, build_paths, ensure_layout, RoleConfig, AgentPaths
- `dwg_agents_ops/Tester_Agent/agent_cli.py` [py] py funcs=0 classes=0 main=yes
- `dwg_agents_ops/Tester_Agent/README.md` [md] Tester Agent
- `dwg_agents_ops/Tester_Agent/role.toml` [toml] [role]

### dwg_system_tools

- Kind: `directory`
- Summary: knowledge-compression-tooling: 面向项目记忆压缩、meta 生成与校验的控制工具目录。它不直接执行业务，而是为智能体提供更快的项目理解入口。
- Files: `8`
- `dwg_system_tools/build_project_memory.py` [py] py funcs=15 classes=1 main=yes | top=infer_root, rel_posix, is_excluded, read_text, first_nonempty_line, extract_doc_summary, Section
- `dwg_system_tools/folder.meta.json` [json] knowledge-compression-tooling: 面向项目记忆压缩、meta 生成与校验的控制工具目录。它不直接执行业务，而是为智能体提供更快的项目理解入口。
- `dwg_system_tools/generate_print_meta.py` [py] py funcs=26 classes=2 main=yes | top=infer_root, function_signature, parse_args, collect_functions, build_func_info, infer_purpose, FuncInfo, CallCollector
- `dwg_system_tools/meta_gen/meta_pipeline.py` [py] py funcs=8 classes=0 main=yes | top=find_root, _should_skip_dir, find_script_by_stem, meta_paths_for_script, select_meta_targets, scan_all_meta
- `dwg_system_tools/meta_gen/META_RULES.md` [md] 版本：V2.0
- `dwg_system_tools/meta_gen/META_SCHEMA.json` [json] json file: META_SCHEMA.json
- `dwg_system_tools/meta_gen/meta_validator.py` [py] py funcs=7 classes=1 main=yes | top=_load_json, _detect_meta_kind, _try_jsonschema_validate, _min_validate_script_meta, _min_validate_functions_meta, validate_file, Issue
- `dwg_system_tools/meta_gen/TASK_TEMPLATE_PLAIN.md` [md] TASK_TEMPLATE — 生成 Script / Functions Meta 任务模板

### cad/system

- Kind: `directory`
- Summary: cad-runtime-kernel: CAD/DWG 执行内核目录。这里定义统一连接、文件控制、对象选择、COM busy 重试、命令协调、运行守护与运行时桥接，是整个项目最不应被绕开的系统骨架。
- Files: `57`
- `cad/system/AGENTS.md` [md] 适用范围：`D:/codex-tasks/cad/system/`
- `cad/system/CAD_com_utils.procedure.meta.json` [json] json file: CAD_com_utils.procedure.meta.json
- `cad/system/CAD_com_utils.py` [py] py funcs=9 classes=1 main=no | top=_dummy_func, silent_mode, _retry_logic, retry_on_busy, retry_if_busy, alias, SafeCOM
- `cad/system/CAD_com_utils.quote.meta.json` [json] json file: CAD_com_utils.quote.meta.json
- `cad/system/CAD_com_utils_functions.procedure.meta.json` [json] json file: CAD_com_utils_functions.procedure.meta.json
- `cad/system/CAD_com_utils_functions.quote.meta.json` [json] json file: CAD_com_utils_functions.quote.meta.json
- `cad/system/cad_command_monitor.procedure.meta.json` [json] json file: cad_command_monitor.procedure.meta.json
- `cad/system/cad_command_monitor.py` [py] py funcs=9 classes=0 main=yes | top=force_bring_to_front, has_valid_cad_window, send_nuclear_esc, get_active_cad_app, analyze_state, is_already_running
- `cad/system/cad_command_monitor.quote.meta.json` [json] json file: cad_command_monitor.quote.meta.json
- `cad/system/cad_command_monitor_functions.procedure.meta.json` [json] json file: cad_command_monitor_functions.procedure.meta.json
- `cad/system/cad_command_monitor_functions.quote.meta.json` [json] json file: cad_command_monitor_functions.quote.meta.json
- `cad/system/CAD_coordination.procedure.meta.json` [json] json file: CAD_coordination.procedure.meta.json
- `cad/system/CAD_coordination.py` [py] py funcs=7 classes=2 main=no | top=wait_quiescent, run_safety_loop, send_cmd_with_sync, wait_document_opened, ensure_single_process, start_cad_with_dialog_killer, CADGuard, FileGuard
- `cad/system/CAD_coordination.quote.meta.json` [json] json file: CAD_coordination.quote.meta.json
- `cad/system/CAD_coordination_functions.procedure.meta.json` [json] json file: CAD_coordination_functions.procedure.meta.json
- `cad/system/CAD_coordination_functions.quote.meta.json` [json] json file: CAD_coordination_functions.quote.meta.json
- `cad/system/CAD_core.procedure.meta.json` [json] json file: CAD_core.procedure.meta.json
- `cad/system/CAD_core.py` [py] py funcs=55 classes=0 main=no | top=_core_get_short_path, _core_get_acad, _core_get_active_doc, _core_wait_document_opened, _core_is_file_opened, _core_is_file_opened_by_name
- `cad/system/CAD_core.quote.meta.json` [json] json file: CAD_core.quote.meta.json
- `cad/system/CAD_core_functions.procedure.meta.json` [json] json file: CAD_core_functions.procedure.meta.json
- `cad/system/CAD_core_functions.quote.meta.json` [json] json file: CAD_core_functions.quote.meta.json
- `cad/system/cad_dialog_killer.procedure.meta.json` [json] json file: cad_dialog_killer.procedure.meta.json
- `cad/system/cad_dialog_killer.py` [py] py funcs=7 classes=0 main=yes | top=read_delay, get_cad_pids, enum_and_maybe_close, is_already_running, create_lock, remove_lock
- `cad/system/cad_dialog_killer.quote.meta.json` [json] json file: cad_dialog_killer.quote.meta.json
- `cad/system/cad_dialog_killer_functions.procedure.meta.json` [json] json file: cad_dialog_killer_functions.procedure.meta.json
- `cad/system/cad_dialog_killer_functions.quote.meta.json` [json] json file: cad_dialog_killer_functions.quote.meta.json
- `cad/system/cad_runtime_guard.py` [py] py funcs=14 classes=0 main=yes | top=now_iso, ensure_dirs, is_already_running, create_lock, remove_lock, read_json
- `cad/system/CAD_RUNTIME_GUARD_PROTOCOL.md` [md] CAD Runtime Guard Protocol
- `cad/system/CAD_selection.procedure.meta.json` [json] json file: CAD_selection.procedure.meta.json
- `cad/system/CAD_selection.py` [py] py funcs=46 classes=0 main=yes | top=cast_object, _maybe_cast, to_vt_int, to_vt_variant, _to_vt_point, pt3
- `cad/system/CAD_selection.quote.meta.json` [json] json file: CAD_selection.quote.meta.json
- `cad/system/CAD_selection_functions.procedure.meta.json` [json] json file: CAD_selection_functions.procedure.meta.json
- `cad/system/CAD_selection_functions.quote.meta.json` [json] json file: CAD_selection_functions.quote.meta.json
- `cad/system/common_logger.procedure.meta.json` [json] json file: common_logger.procedure.meta.json
- `cad/system/common_logger.py` [py] py funcs=7 classes=1 main=no | top=_parse_log_level, setup_logger, set_log_level, set_debug_mode, record_test_result, checkpoint, CriticalSection
- `cad/system/common_logger.quote.meta.json` [json] json file: common_logger.quote.meta.json
- `cad/system/common_logger_functions.procedure.meta.json` [json] json file: common_logger_functions.procedure.meta.json
- `cad/system/common_logger_functions.quote.meta.json` [json] json file: common_logger_functions.quote.meta.json
- `cad/system/content_analysis_dwg_file.procedure.meta.json` [json] json file: content_analysis_dwg_file.procedure.meta.json
- `cad/system/content_analysis_dwg_file.py` [py] py funcs=15 classes=0 main=no | top=_now_str, _sha1_text, _norm_path, _safe_json, _try, _parse_identifier
- `cad/system/content_analysis_dwg_file.quote.meta.json` [json] json file: content_analysis_dwg_file.quote.meta.json
- `cad/system/content_analysis_dwg_file_functions.procedure.meta.json` [json] json file: content_analysis_dwg_file_functions.procedure.meta.json
- `cad/system/content_analysis_dwg_file_functions.quote.meta.json` [json] json file: content_analysis_dwg_file_functions.quote.meta.json
- `cad/system/folder.meta.json` [json] cad-runtime-kernel: CAD/DWG 执行内核目录。这里定义统一连接、文件控制、对象选择、COM busy 重试、命令协调、运行守护与运行时桥接，是整个项目最不应被绕开的系统骨架。
- `cad/system/licad.procedure.meta.json` [json] json file: licad.procedure.meta.json
- `cad/system/licad.py` [py] py funcs=11 classes=2 main=no | top=_coinit_once, _launch_tarch_bootstrap, get_acad_doc, li, save_file, save_file_as, SafeDocumentWrapper, AutoCadProxy
- `cad/system/licad.quote.meta.json` [json] json file: licad.quote.meta.json
- `cad/system/licad_functions.procedure.meta.json` [json] json file: licad_functions.procedure.meta.json
- `cad/system/licad_functions.quote.meta.json` [json] json file: licad_functions.quote.meta.json
- `cad/system/project_setup.procedure.meta.json` [json] json file: project_setup.procedure.meta.json
- `cad/system/project_setup.py` [py] py funcs=0 classes=1 main=no | top=PathConfig
- `cad/system/project_setup.quote.meta.json` [json] json file: project_setup.quote.meta.json
- `cad/system/project_setup_functions.procedure.meta.json` [json] json file: project_setup_functions.procedure.meta.json
- `cad/system/project_setup_functions.quote.meta.json` [json] json file: project_setup_functions.quote.meta.json
- `cad/system/README.md` [md] `D:/codex-tasks/cad/system`
- `cad/system/RUN_FUNCTION_META_TASK.md` [md] 适用对象：Codex / 命令行智能体
- `cad/system/runtime_guard_bridge.py` [py] py funcs=11 classes=2 main=no | top=_read_json, _read_jsonl, _parse_ts, _is_recent, read_runtime_guard_state, read_runtime_guard_events, RuntimeGuardDecision, RuntimeGuardTriggered

### cad/tools

- Kind: `directory`
- Summary: analysis-index-and-spec-toolbox: 面向源码理解、静态索引、spec 转换与导航注册的工具目录。它不是业务执行主链，但对智能体快速理解项目、定位调用关系和压缩代码骨架有明确价值。
- Files: `15`
- `cad/tools/basic_graph_analyzer.py` [py] py funcs=22 classes=3 main=yes | top=_now_str, _safe_read_text, _json_dump, _norm_path, _rel_to_root, _module_qual_from_file, CallSite, _CallsiteCollector, _InnerCallCollector
- `cad/tools/code_to_spec.py` [py] py funcs=6 classes=0 main=yes | top=_literal, _get_call_name, _get_attr_base, _extract_steps_from_source, build_spec, main
- `cad/tools/code_to_virtual.py` [py] py funcs=2 classes=0 main=yes | top=run, main
- `cad/tools/folder.meta.json` [json] analysis-index-and-spec-toolbox: 面向源码理解、静态索引、spec 转换与导航注册的工具目录。它不是业务执行主链，但对智能体快速理解项目、定位调用关系和压缩代码骨架有明确价值。
- `cad/tools/function_analyzer.py` [py] py funcs=44 classes=1 main=no | top=_sha256_text, _qualified_hash, _db_get_conn, _db_close_conn, _db_has_column, _db_has_index, _CallCollector
- `cad/tools/function_name_cleaner.py` [py] py funcs=15 classes=2 main=no | top=list_function_defs_in_file, find_duplicate_defs, build_remove_plan, apply_remove_plan_to_file, sync_remove_plan_to_db, clean_duplicate_defs_and_db, FuncDefRef, RemovePlanItem
- `cad/tools/IDLE_bootstrap.py` [py] py funcs=2 classes=0 main=no | top=run_script_in_main, start_listener
- `cad/tools/ReadMe.md` [md] function_analyzer.py是核心之一，意图将具体的函数代码转换为虚的结构分解并保存在数据库中。同时将函数表达为文本、结构图等。
- `cad/tools/script_navigator_registry.json` [json] json file: script_navigator_registry.json
- `cad/tools/spec_code_consistency.py` [py] py funcs=10 classes=0 main=yes | top=_literal, _get_attr_base, _get_call_name, _filter_call, _normalize_dep, _extract_signature
- `cad/tools/spec_to_mermaid.py` [py] py funcs=3 classes=0 main=yes | top=_q, build_mermaid, main
- `cad/tools/spec_to_stub.py` [py] py funcs=3 classes=0 main=yes | top=_fmt_default, build_stub, main
- `cad/tools/spec_to_text.py` [py] py funcs=2 classes=0 main=yes | top=build_text, main
- `cad/tools/virtual_to_code.py` [py] py funcs=1 classes=0 main=yes | top=main
- `cad/tools/脚本导航14版.py` [py] py funcs=10 classes=1 main=yes | top=clean_old_logs, _normalize_registry_path, _pid_exists, _read_registry_data, _write_registry_data, _cleanup_registry_data, ScriptNavigator

### cad/library

- Kind: `directory`
- Summary: high-level-business-function-library: 建立在 cad/system 之上的高层业务函数库，负责块、文字、几何、对象、控制和数据库等复用能力。它承接业务实现，但不替代 system 层的统一连接与协调原则。
- Files: `15`
- `cad/library/__init__.py` [py] py funcs=0 classes=0 main=no
- `cad/library/cad_annotation.py` [py] py funcs=19 classes=0 main=yes | top=vtpnt, write_cad_text, write_mtext, add_dim_aligned, add_dim_rotated, add_dim_angular
- `cad/library/cad_blocks.py` [py] py funcs=56 classes=0 main=no | top=get_block_name, huoqukuai_shuxing_zhi, update_block_def_attributes_safe, update_block_def_attributes_v7, attsync_block_instance, attsync_block_instance_base
- `cad/library/cad_control.py` [py] py funcs=82 classes=0 main=no | top=fix_com_cache, delete_all_nul_under_folder, kill_dialog_killer, kill_python_script_by_name, kill_wps, close_all_excel_processes
- `cad/library/cad_geometry_draw.py` [py] py funcs=19 classes=0 main=no | top=_now_ms, _as_3d, _flatten_vertices, _call_retry, _ensure_layer, _get_space
- `cad/library/cad_geometry_polyline.py` [py] py funcs=22 classes=0 main=no | top=_now_ms, _log_start, _log_end, _as_3d, _call_retry, _call_delete
- `cad/library/cad_geometry_segment.py` [py] py funcs=77 classes=0 main=no | top=_now_ms, _log_start, _log_end, _as_3d, _call_retry, _call_delete
- `cad/library/cad_objects.py` [py] py funcs=62 classes=0 main=no | top=ensure_list, sort_tuples, multi_dim_tolerance_sort, get_ll_pt, get_center, sort_entities_by_position
- `cad/library/Databaseoperation.py` [py] py funcs=83 classes=0 main=no | top=connect_to_db_no_db, create_database_if_not_exists, connect_to_db, ensure_connection_alive, execute_sql, create_table
- `cad/library/folder.meta.json` [json] high-level-business-function-library: 建立在 cad/system 之上的高层业务函数库，负责块、文字、几何、对象、控制和数据库等复用能力。它承接业务实现，但不替代 system 层的统一连接与协调原则。
- `cad/library/meta/cad_annotation.meta.json` [json] json file: cad_annotation.meta.json
- `cad/library/meta/cad_geometry.meta.json` [json] json file: cad_geometry.meta.json
- `cad/library/meta/functions.cad_annotation.meta.json` [json] json file: functions.cad_annotation.meta.json
- `cad/library/meta/functions.cad_geometry.meta.json` [json] json file: functions.cad_geometry.meta.json
- `cad/library/tarch_building.py` [py] py funcs=31 classes=0 main=no | top=dim_by_points, draw_tarch_wall, insert_tarch_door, insert_tarch_window, run_tupdspace_for_tz_room_in_rect, run_auto_TUPDSPACE_with_coord

### cad/scripts/drawing_basic_service/print

- Kind: `directory`
- Summary: primary-domain-print-execution-workspace: 当前第一优先级的领域执行工作区，目标是稳定完成 DWG 打印，并把新案例与新规则沉淀回脚本与文档。
- Files: `54`
- `cad/scripts/drawing_basic_service/print/AGENTS.md` [md] 适用范围：`D:/codex-tasks/cad/scripts/drawing_basic_service/print/`
- `cad/scripts/drawing_basic_service/print/cases/CASE_MANIFEST.md` [md] 1. 案例角色
- `cad/scripts/drawing_basic_service/print/folder.meta.json` [json] primary-domain-print-execution-workspace: 当前第一优先级的领域执行工作区，目标是稳定完成 DWG 打印，并把新案例与新规则沉淀回脚本与文档。
- `cad/scripts/drawing_basic_service/print/PRINT_AGENT_SPEC.md` [md] 说明：
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py` [py] py funcs=29 classes=0 main=yes | top=_safe_delete, _bbox_xy, _bbox_wh_from_bbox, _eps_from_short_side, _cluster_1d, _cluster_points_2d
- `cad/scripts/drawing_basic_service/print/print_area_analysis_functions.procedure.meta.json` [json] json file: print_area_analysis_functions.procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_analysis_functions.quote.meta.json` [json] json file: print_area_analysis_functions.quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_analysis_procedure.meta.json` [json] json file: print_area_analysis_procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_analysis_quote.meta.json` [json] json file: print_area_analysis_quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py` [py] py funcs=28 classes=2 main=yes | top=_safe_handle, _bbox_xy, _contains_bbox, _get_entity_bbox_points, _get_collection_count, _get_collection_item, AreaContentMetrics, EntitySnapshot
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis_functions.procedure.meta.json` [json] json file: print_area_content_analysis_functions.procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis_functions.quote.meta.json` [json] json file: print_area_content_analysis_functions.quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis_procedure.meta.json` [json] json file: print_area_content_analysis_procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis_quote.meta.json` [json] json file: print_area_content_analysis_quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_scope_analysis.py` [py] py funcs=11 classes=0 main=yes | top=_normalize_path, _is_name_only_target, _find_document_by_path, _activate_document_by_path, _close_document_by_path, _area_from_bbox
- `cad/scripts/drawing_basic_service/print/print_area_scope_analysis_functions.procedure.meta.json` [json] json file: print_area_scope_analysis_functions.procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_scope_analysis_functions.quote.meta.json` [json] json file: print_area_scope_analysis_functions.quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_scope_analysis_procedure.meta.json` [json] json file: print_area_scope_analysis_procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_area_scope_analysis_quote.meta.json` [json] json file: print_area_scope_analysis_quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_batch_dispatch.py` [py] py funcs=19 classes=0 main=yes | top=_is_dispatch_source_dwg, _derive_public_base_name, _reset_dir, _prepare_public_output_dirs, _load_json, _write_batch_summary
- `cad/scripts/drawing_basic_service/print/print_batch_dispatch_functions.procedure.meta.json` [json] json file: print_batch_dispatch_functions.procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_batch_dispatch_functions.quote.meta.json` [json] json file: print_batch_dispatch_functions.quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_batch_dispatch_procedure.meta.json` [json] json file: print_batch_dispatch_procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_batch_dispatch_quote.meta.json` [json] json file: print_batch_dispatch_quote.meta.json
- `cad/scripts/drawing_basic_service/print/PRINT_DISPATCH_PROTOCOL.md` [md] 1. 角色调度对象定义
- `cad/scripts/drawing_basic_service/print/print_executor.py` [py] py funcs=13 classes=2 main=no | top=_wait_for_pdf_ready, _normalize_path, _is_name_only_target, _active_doc_matches, _activate_document_by_path, _ensure_model_doc_ready, PrintDefaults, PrintExecutionSummary
- `cad/scripts/drawing_basic_service/print/print_executor_functions.procedure.meta.json` [json] json file: print_executor_functions.procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_executor_functions.quote.meta.json` [json] json file: print_executor_functions.quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_executor_procedure.meta.json` [json] json file: print_executor_procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_executor_quote.meta.json` [json] json file: print_executor_quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py` [py] py funcs=39 classes=2 main=yes | top=_safe_handle, _bbox_xy, _normalize_path, _is_name_only_target, _find_document_by_path, _activate_document_by_path, BlockSnapshot, TextRecord
- `cad/scripts/drawing_basic_service/print/print_info_analysis_functions.procedure.meta.json` [json] json file: print_info_analysis_functions.procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_info_analysis_functions.quote.meta.json` [json] json file: print_info_analysis_functions.quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_info_analysis_procedure.meta.json` [json] json file: print_info_analysis_procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_info_analysis_quote.meta.json` [json] json file: print_info_analysis_quote.meta.json
- `cad/scripts/drawing_basic_service/print/PRINT_KNOWLEDGE.md` [md] 1. 打印区域认知
- `cad/scripts/drawing_basic_service/print/PRINT_OUTPUT_SPEC.md` [md] 1. 打印主链输出规范
- `cad/scripts/drawing_basic_service/print/print_policy.py` [py] py funcs=17 classes=2 main=no | top=_safe_handle, _get_bbox, _layout_name_map, _sanitize_name, _contains_bbox, normalize_print_mode, PrintJob, PrintPlan
- `cad/scripts/drawing_basic_service/print/print_policy_functions.procedure.meta.json` [json] json file: print_policy_functions.procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_policy_functions.quote.meta.json` [json] json file: print_policy_functions.quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_policy_procedure.meta.json` [json] json file: print_policy_procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_policy_quote.meta.json` [json] json file: print_policy_quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_runner.py` [py] py funcs=10 classes=0 main=yes | top=_make_process_token, _make_run_dirs, _normalize_path, _is_name_only_target, _find_document_by_path, _activate_document_by_path
- `cad/scripts/drawing_basic_service/print/print_runner_functions.procedure.meta.json` [json] json file: print_runner_functions.procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_runner_functions.quote.meta.json` [json] json file: print_runner_functions.quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_runner_procedure.meta.json` [json] json file: print_runner_procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_runner_quote.meta.json` [json] json file: print_runner_quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_verifier.py` [py] py funcs=5 classes=0 main=no | top=_job_value, _parse_media_size_mm, _read_pdf_page_sizes_mm, _verify_page_sizes, verify_generated_pdfs
- `cad/scripts/drawing_basic_service/print/print_verifier_functions.procedure.meta.json` [json] json file: print_verifier_functions.procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_verifier_functions.quote.meta.json` [json] json file: print_verifier_functions.quote.meta.json
- `cad/scripts/drawing_basic_service/print/print_verifier_procedure.meta.json` [json] json file: print_verifier_procedure.meta.json
- `cad/scripts/drawing_basic_service/print/print_verifier_quote.meta.json` [json] json file: print_verifier_quote.meta.json
- `cad/scripts/drawing_basic_service/print/PRINT_WORKFLOW.md` [md] 1. 接单入口
- `cad/scripts/drawing_basic_service/print/README.md` [md] Print Service
