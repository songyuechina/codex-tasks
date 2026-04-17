from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "02_manifest" / "page_manifest.jsonl"
VALUE_RANKING_PATH = ROOT / "02_manifest" / "value_ranking.jsonl"
TASK_INDEX_PATH = ROOT / "04_task_cards" / "task_index.json"
TASK_MAP_PATH = ROOT / "07_validation" / "task_to_existing_code_map.json"
TOPIC_PATH_MAP_PATH = ROOT / "06_on_demand_index" / "topic_path_map.json"
CORE_DIR = ROOT / "03_core_symbols"
CANDIDATE_PATH = ROOT / "02_manifest" / "core_symbol_candidates.jsonl"

RULE_COMMON_PATTERNS = "05_pywin32_bridge/common_patterns.md"
RULE_COMMON_FAILURES = "05_pywin32_bridge/common_failures.md"
RULE_PYWIN32_TYPES = "05_pywin32_bridge/pywin32_type_rules.md"
RULE_POINT_ARRAY = "05_pywin32_bridge/point_array_rules.md"
RULE_VARIANT = "05_pywin32_bridge/variant_rules.md"
RULE_COLLECTION = "05_pywin32_bridge/collection_rules.md"
RULE_SENDCOMMAND = "05_pywin32_bridge/sendcommand_rules.md"
RULE_COORDINATE_SYSTEMS = "05_pywin32_bridge/coordinate_system_rules.md"
RULE_3D_TRANSFORM = "05_pywin32_bridge/3d_transform_rules.md"
RULE_3D_ENTITY_CREATION = "05_pywin32_bridge/3d_entity_creation_rules.md"
RULE_SECTION_REGION = "05_pywin32_bridge/section_region_rules.md"

SPATIAL_3D_BASENAME_WHITELIST = {
    "idh_translatecoordinates.htm",
    "idh_activeucs.htm",
    "idh_getucsmatrix.htm",
    "idh_ucs_object.htm",
    "idh_normal.htm",
    "idh_elevation.htm",
    "idh_elevationmodelspace.htm",
    "idh_elevationpaperspace.htm",
    "idh_3dpoly_object.htm",
    "idh_3dface_object.htm",
    "idh_3dsolid_object.htm",
    "idh_region_object.htm",
    "idh_add3dpoly.htm",
    "idh_add3dface.htm",
    "idh_addregion.htm",
    "idh_addextrudedsolid.htm",
    "idh_addextrudedsolidalongpath.htm",
    "idh_addrevolvedsolid.htm",
    "idh_sectionsolid.htm",
    "idh_rotate3d.htm",
    "idh_mirror3d.htm",
    "idh_scaleentity.htm",
    "idh_transformby.htm",
    "idh_move.htm",
}


NEW_SYMBOL_SPECS = [
    {
        "symbol": "TILEMODE",
        "kind": "system_variable",
        "folder": "system_variables",
        "owners": ["Document"],
        "source_terms": ["tilemode", "active space"],
        "purpose": "控制模型空间主态和布局/图纸空间主态，是布局判断与打印前上下文校验的底层变量。",
        "common_uses": ["判断当前是否仍处于模型空间", "布局切换前校验上下文", "打印前确认纸空间相关状态"],
        "pywin32_signature": 'C.doc.GetVariable("TILEMODE") / C.doc.SetVariable("TILEMODE", 0)',
        "parameters": ["读取: Name='TILEMODE'", "写入: 0=布局/图纸空间, 1=模型空间"],
        "returns": "int",
        "prerequisites": ["理解 ActiveSpace/MSpace 与布局语义关系"],
        "risks": ["把 TILEMODE 与浮动视口内编辑态混淆", "切换后立刻读取布局状态可能未同步"],
        "project_paths": ["cad/system/CAD_core.py", "cad/system/CAD_selection.py", "cad/scripts/drawing_basic_service/print/print_area_analysis.py"],
        "related_tasks": ["determine_space_and_layout", "switch_to_target_layout", "read_layout_plot_info"],
        "source_topic_ids": ["acadauto:ex_activespace", "acad_aag:GUID_4EAB8372_859A_4C6E_BEE5_B2C8EBA31AD7", "acad_aag:GUID_9DCF17E7_717B_4766_AFFE_D3C9ED506BB8"],
        "rule_refs": [RULE_COMMON_PATTERNS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "CTAB",
        "kind": "system_variable",
        "folder": "system_variables",
        "owners": ["Document"],
        "source_terms": ["ctab", "active layout", "layout"],
        "purpose": "当前标签页布局名，是从当前任务定位真实布局的直接变量入口。",
        "common_uses": ["回读当前布局名", "布局切换后验证是否到位", "打印任务开始前确认目标布局已经激活"],
        "pywin32_signature": 'C.doc.GetVariable("CTAB")',
        "parameters": ["读取: Name='CTAB'"],
        "returns": "str",
        "prerequisites": ["理解 CTAB 与 ActiveLayout 的协同关系"],
        "risks": ["布局切换命令刚结束时 CTAB 读数可能尚未稳定"],
        "project_paths": ["cad/system/CAD_core.py", "cad/system/CAD_coordination.py", "cad/scripts/drawing_basic_service/print/print_area_analysis.py"],
        "related_tasks": ["determine_space_and_layout", "switch_to_target_layout", "execute_layout_plot"],
        "source_topic_ids": ["acadauto:ex_getvariable", "acadauto:ex_activelayout", "acad_aag:GUID_A55918B2_0D79_476A_9A20_A1BA80AB2EDD"],
        "rule_refs": [RULE_COMMON_PATTERNS, RULE_SENDCOMMAND, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "CMDACTIVE",
        "kind": "system_variable",
        "folder": "system_variables",
        "owners": ["Document"],
        "source_terms": ["cmdactive", "sendcommand", "command"],
        "purpose": "命令执行态位标志，是 SendCommand 回退链等待和同步判断的重要读数。",
        "common_uses": ["命令发送后等待空闲", "打印回退链防止命令串扰", "布局切换命令同步判断"],
        "pywin32_signature": 'C.doc.GetVariable("CMDACTIVE")',
        "parameters": ["读取: Name='CMDACTIVE'"],
        "returns": "int bitmask",
        "prerequisites": ["把它当状态探针，不当业务语义变量"],
        "risks": ["误解位掩码", "把命令态噪声误判为真正失败"],
        "project_paths": ["cad/system/CAD_coordination.py", "cad/system/licad.py", "cad/scripts/drawing_basic_service/print/print_executor.py"],
        "related_tasks": ["sendcommand_fallback", "switch_to_target_layout", "execute_layout_plot"],
        "source_topic_ids": ["acadauto:ex_getvariable", "acadauto:ex_sendcommand"],
        "rule_refs": [RULE_SENDCOMMAND, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "FILEDIA",
        "kind": "system_variable",
        "folder": "system_variables",
        "owners": ["Document"],
        "source_terms": ["filedia", "setvariable", "dialog"],
        "purpose": "控制文件类对话框显隐，是批处理和无交互命令链必须明确的环境变量。",
        "common_uses": ["关闭对话框避免阻塞", "批处理结束后恢复交互环境"],
        "pywin32_signature": 'C.doc.SetVariable("FILEDIA", 0 or 1)',
        "parameters": ["写入: 0=禁用对话框, 1=启用对话框"],
        "returns": "int on read / None on write",
        "prerequisites": ["明确当前任务是自动化批处理还是人工交互"],
        "risks": ["忘记恢复导致后续人工操作异常", "对话框阻塞被误判为 CAD 卡死"],
        "project_paths": ["cad/system/CAD_coordination.py", "cad/system/CAD_core.py", "cad/system/licad.py"],
        "related_tasks": ["sendcommand_fallback", "open_save_close_document", "execute_layout_plot"],
        "source_topic_ids": ["acadauto:ex_getvariable", "acadauto:ex_setvariable"],
        "rule_refs": [RULE_COMMON_PATTERNS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "CMDECHO",
        "kind": "system_variable",
        "folder": "system_variables",
        "owners": ["Document"],
        "source_terms": ["cmdecho", "setvariable", "command"],
        "purpose": "控制命令回显，用于调试和批处理环境归一，但不替代真正的同步判断。",
        "common_uses": ["调试阶段临时打开回显", "批处理阶段关闭噪声输出"],
        "pywin32_signature": 'C.doc.SetVariable("CMDECHO", 0 or 1)',
        "parameters": ["写入: 0=关闭回显, 1=打开回显"],
        "returns": "int on read / None on write",
        "prerequisites": ["理解它只影响回显，不影响命令是否执行完"],
        "risks": ["把回显变化误当作命令完成信号"],
        "project_paths": ["cad/system/CAD_coordination.py", "cad/system/licad.py"],
        "related_tasks": ["sendcommand_fallback", "execute_layout_plot"],
        "source_topic_ids": ["acadauto:ex_getvariable", "acadauto:ex_setvariable", "acadauto:ex_sendcommand"],
        "rule_refs": [RULE_SENDCOMMAND, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "LTSCALE",
        "kind": "system_variable",
        "folder": "system_variables",
        "owners": ["Document"],
        "source_terms": ["ltscale", "linetype scale"],
        "purpose": "控制全局线型比例，会直接影响布局输出和打印观感。",
        "common_uses": ["打印前核查线型缩放", "模板插入后统一线型表现"],
        "pywin32_signature": 'C.doc.GetVariable("LTSCALE") / C.doc.SetVariable("LTSCALE", value)',
        "parameters": ["读取/写入: Name='LTSCALE'"],
        "returns": "float",
        "prerequisites": ["结合 PSLTSCALE、布局视口比例一起理解"],
        "risks": ["全局修改影响整个图纸视觉结果"],
        "project_paths": ["cad/scripts/drawing_basic_service/print/print_executor.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["read_layout_plot_info", "execute_layout_plot"],
        "source_topic_ids": ["acadauto:ex_setvariable", "acad_aag:GUID_4D1D635B_663F_4BB3_A6BE_46C7D13A39D8"],
        "rule_refs": [RULE_COMMON_PATTERNS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "TEXTSTYLE",
        "kind": "system_variable",
        "folder": "system_variables",
        "owners": ["Document"],
        "source_terms": ["textstyle", "activetextstyle", "unicode"],
        "purpose": "控制当前文字样式，对图签字段写入、目录生成和中文显示稳定性都有直接影响。",
        "common_uses": ["文本写入前核查当前样式", "中文字体/大字体排查"],
        "pywin32_signature": 'C.doc.GetVariable("TEXTSTYLE") / C.doc.ActiveTextStyle',
        "parameters": ["读取: Name='TEXTSTYLE'"],
        "returns": "str",
        "prerequisites": ["理解 TEXTSTYLE 与 ActiveTextStyle/TextStyles 的关系"],
        "risks": ["中文字体缺失导致显示异常", "模板样式不一致导致回写效果不稳定"],
        "project_paths": ["cad/scripts/CAD_basic.py", "cad/scripts/drawing_basic_service/print/print_info_analysis.py"],
        "related_tasks": ["update_titleblock_fields", "generate_or_update_catalog", "create_basic_geometry_smoke"],
        "source_topic_ids": ["acadauto:ex_activetextstyle", "acad_aag:GUID_29E096AD_6237_4B26_8964_A55DDF7197F8"],
        "rule_refs": [RULE_COMMON_PATTERNS, RULE_PYWIN32_TYPES],
    },
    {
        "symbol": "CLAYER",
        "kind": "system_variable",
        "folder": "system_variables",
        "owners": ["Document"],
        "source_terms": ["clayer", "activelayer", "layer"],
        "purpose": "当前活动图层变量，用于对象落层、插图签和图层环境归一。",
        "common_uses": ["对象创建前切换目标图层", "插图签后恢复原图层"],
        "pywin32_signature": 'C.doc.GetVariable("CLAYER") / C.doc.ActiveLayer',
        "parameters": ["读取: Name='CLAYER'"],
        "returns": "str",
        "prerequisites": ["明确当前图层和目标对象图层的职责差异"],
        "risks": ["忘记恢复当前图层污染后续任务", "锁定/冻结图层导致写入失败"],
        "project_paths": ["cad/scripts/CAD_basic.py", "cad/scripts/Scheme_drawing/draw_building_outline.py"],
        "related_tasks": ["manage_layers", "insert_company_title_block", "create_basic_geometry_smoke"],
        "source_topic_ids": ["acadauto:ex_activelayer", "acad_aag:GUID_D86DF08B_BBD3_4E0F_AB75_13B2C4AD972C"],
        "rule_refs": [RULE_COMMON_PATTERNS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "3d_point",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["addline", "insertblock", "setwindowtoplot"],
        "purpose": "统一说明项目中的三维点入参形式，避免二维点或裸 Variant 写错。",
        "common_uses": ["AddLine 起点终点", "InsertBlock 插入点", "窗口输出坐标准备"],
        "pywin32_signature": "(x, y, z) or VARIANT(VT_ARRAY | VT_R8, (x, y, z))",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py", "cad/scripts/drawing_basic_service/print/print_executor.py"],
        "related_tasks": ["create_basic_geometry_smoke", "insert_block_or_dwg", "execute_layout_plot"],
        "source_topic_ids": ["acadauto:ex_addline", "acadauto:ex_insertblock", "acadauto:ex_setwindowtoplot"],
        "rule_refs": [RULE_POINT_ARRAY, RULE_VARIANT, RULE_PYWIN32_TYPES],
    },
    {
        "symbol": "2d_point",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["setwindowtoplot", "getwindowtoplot"],
        "purpose": "说明窗口点这类二维语义坐标如何统一落到稳定的 COM 传参格式。",
        "common_uses": ["SetWindowToPlot 窗口点", "bbox 转窗口点"],
        "pywin32_signature": "(x, y) -> 项目内先归一，再决定是否补 z",
        "project_paths": ["cad/scripts/drawing_basic_service/print/print_executor.py", "cad/scripts/drawing_basic_service/print/print_area_analysis.py"],
        "related_tasks": ["execute_layout_plot", "get_bounding_box_and_object_counts"],
        "source_topic_ids": ["acadauto:ex_setwindowtoplot", "acadauto:ex_getwindowtoplot"],
        "rule_refs": [RULE_POINT_ARRAY, RULE_VARIANT],
    },
    {
        "symbol": "variant_array",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["variant arrays", "converting arrays to variants", "using variants for array data"],
        "purpose": "统一说明数组型返回值和入参为何经常以 Variant 包裹，以及项目里何时需要显式处理。",
        "common_uses": ["选择集过滤数组", "坐标数组和边界框解释", "低层几何参数包装"],
        "pywin32_signature": "VARIANT(VT_ARRAY | base_type, data)",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_selection.py"],
        "related_tasks": ["build_selection_set", "get_bounding_box_and_object_counts"],
        "source_topic_ids": ["acad_aag:GUID_5004997B_3086_4D07_A0A1_AEB32B7727A2", "acad_aag:GUID_192B537E_8F89_4F21_BD5D_28B9E3918C88", "acad_aag:GUID_F6B0A90B_B484_4B2E_A0E1_FE6B7441ADBC", "acad_aag:GUID_CC394595_C4A3_47D4_A040_C58C16B92918"],
        "rule_refs": [RULE_VARIANT, RULE_PYWIN32_TYPES, RULE_POINT_ARRAY],
    },
    {
        "symbol": "safearray",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["safearray", "variant arrays"],
        "purpose": "说明 SAFEARRAY 是许多 ActiveX 数组参数/返回值的底层载体，帮助正确理解 pywin32 包装形态。",
        "common_uses": ["Variant 数组底层结构识别", "数组参数类型排错"],
        "pywin32_signature": "通常经 VARIANT(VT_ARRAY | base_type, data) 间接接触 SAFEARRAY",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_selection.py"],
        "related_tasks": ["build_selection_set", "create_basic_geometry_smoke"],
        "source_topic_ids": ["acad_aag:GUID_5004997B_3086_4D07_A0A1_AEB32B7727A2", "acad_aag:GUID_192B537E_8F89_4F21_BD5D_28B9E3918C88"],
        "rule_refs": [RULE_VARIANT, RULE_PYWIN32_TYPES],
    },
    {
        "symbol": "collection_iteration",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["iterating through a collection object", "collection objects"],
        "purpose": "统一说明对 Layouts、SelectionSets、Attributes 等集合对象的推荐遍历方式。",
        "common_uses": ["枚举布局", "遍历块属性", "遍历选择集"],
        "pywin32_signature": "for item in collection / collection.Item(name_or_index)",
        "project_paths": ["cad/system/CAD_core.py", "cad/system/CAD_selection.py", "cad/scripts/drawing_basic_service/print/print_info_analysis.py"],
        "related_tasks": ["enumerate_layouts", "build_selection_set", "read_block_attributes"],
        "source_topic_ids": ["acad_aag:GUID_589F246A_41BE_4D38_AA91_9FDA3ABABEA6", "acad_aag:GUID_05AC034B_3E51_4EC3_85BE_B3153B8CC40B"],
        "rule_refs": [RULE_COLLECTION, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "bounding_box_tuple",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["getboundingbox", "bounding box"],
        "purpose": "统一说明如何把 GetBoundingBox 的双输出点归一成稳定的 `(xmin, ymin, xmax, ymax)` 结构。",
        "common_uses": ["打印框识别", "图签定位", "对象统计裁剪"],
        "pywin32_signature": "entity.GetBoundingBox(min_pt, max_pt) -> bbox tuple",
        "project_paths": ["cad/scripts/drawing_basic_service/print/print_area_content_analysis.py", "cad/system/content_analysis_dwg_file.py"],
        "related_tasks": ["get_bounding_box_and_object_counts", "read_layout_plot_info"],
        "source_topic_ids": ["acadauto:ex_getboundingbox"],
        "rule_refs": [RULE_POINT_ARRAY, RULE_VARIANT],
    },
    {
        "symbol": "object_return_type",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["insertblock", "getattributes", "selectionsets"],
        "purpose": "统一说明哪些方法返回 COM 对象、集合或对象引用，避免把返回值当成纯数据结构处理。",
        "common_uses": ["InsertBlock 返回 BlockReference", "GetAttributes 返回属性集合", "SelectionSets.Add 返回 SelectionSet"],
        "pywin32_signature": "result = com_method(...); 用对象属性/方法继续处理",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_selection.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["insert_block_or_dwg", "read_block_attributes", "build_selection_set"],
        "source_topic_ids": ["acadauto:ex_insertblock", "acadauto:ex_getattributes", "acadauto:ex_selectionsets"],
        "rule_refs": [RULE_COLLECTION, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "text_string_encoding",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["unicode", "big fonts", "textstyle"],
        "purpose": "说明中文图签和目录文字涉及的编码/字体兼容问题，避免写入成功但显示异常。",
        "common_uses": ["图签字段中文回写", "目录文本中文生成"],
        "pywin32_signature": "str -> COM string; 字体效果由 TextStyle/Big Font 共同决定",
        "project_paths": ["cad/scripts/CAD_basic.py", "cad/scripts/drawing_basic_service/print/print_info_analysis.py"],
        "related_tasks": ["update_titleblock_fields", "generate_or_update_catalog"],
        "source_topic_ids": ["acadauto:ex_activetextstyle", "acad_aag:GUID_29E096AD_6237_4B26_8964_A55DDF7197F8"],
        "rule_refs": [RULE_PYWIN32_TYPES, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "UCS",
        "kind": "object",
        "folder": "objects",
        "owners": ["Document", "UCSs"],
        "source_terms": ["ucs object", "user coordinate system object", "activeucs", "getucsmatrix"],
        "purpose": "表示用户坐标系对象，是从绘图基准切入三维空间表达和矩阵变换的正式入口。",
        "common_uses": ["读取当前活动 UCS", "获取 UCS 变换矩阵", "把对象对齐到特定 UCS 基准"],
        "pywin32_signature": "C.doc.ActiveUCS / C.doc.UserCoordinateSystems.Item(name)",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_core.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "apply_3d_transform_to_objects"],
        "source_topic_ids": ["acadauto:idh_ucs_object", "acadauto:idh_activeucs", "acadauto:idh_getucsmatrix"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_3D_TRANSFORM, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "3dPolyline",
        "kind": "object",
        "folder": "objects",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["3dpolyline object", "add3dpoly", "3d polyline"],
        "purpose": "表示由直线段组成的三维路径对象，适合表达空间路径、轮廓骨架和剖切参考线。",
        "common_uses": ["表达空间路径", "建立三维轮廓骨架", "作为后续区域/实体构造前的路径表达"],
        "pywin32_signature": "model_space.Add3DPoly(points_array)",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py", "cad/scripts/Scheme_drawing/draw_building_outline.py"],
        "related_tasks": ["create_3d_path_or_profile", "read_3d_object_spatial_identity"],
        "source_topic_ids": ["acadauto:idh_3dpoly_object", "acadauto:idh_add3dpoly"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT],
    },
    {
        "symbol": "3DFace",
        "kind": "object",
        "folder": "objects",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["3dface object", "add3dface"],
        "purpose": "表示由三点或四点定义的三维面对象，可用于构造面、剖切参考和平面关系表达。",
        "common_uses": ["表达三维面", "构造共面轮廓参考", "为区域/剖切前置建模提供面级对象"],
        "pywin32_signature": "model_space.Add3DFace(point1, point2, point3[, point4])",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["create_3d_path_or_profile", "section_3d_geometry_for_2d_expression"],
        "source_topic_ids": ["acadauto:idh_3dface_object", "acadauto:idh_add3dface"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT],
    },
    {
        "symbol": "Region",
        "kind": "object",
        "folder": "objects",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["region object", "addregion", "working with regions"],
        "purpose": "表示有界平面区域，是从轮廓进入面积、剖切、实体和二维表达中间层的关键对象。",
        "common_uses": ["由闭合轮廓生成区域", "作为挤出或旋转实体的 profile", "作为剖切结果的二维中间表达"],
        "pywin32_signature": "region_list = model_space.AddRegion(object_list)",
        "project_paths": ["cad/system/licad.py", "cad/system/content_analysis_dwg_file.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["create_region_and_extrude_solid", "section_3d_geometry_for_2d_expression"],
        "source_topic_ids": ["acadauto:idh_region_object", "acadauto:idh_addregion", "acad_aag:GUID_4699B54A_2628_49FE_B093_0062FBEC37EA", "acad_aag:GUID_9EB18E5E_9C16_4FB9_B334_D61ED00DCB80"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_SECTION_REGION, RULE_COORDINATE_SYSTEMS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "3DSolid",
        "kind": "object",
        "folder": "objects",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["3dsolid object", "addextrudedsolid", "addextrudedsolidalongpath", "addrevolvedsolid", "sectionsolid"],
        "purpose": "表示三维实体对象，用于稳定表达构件体量、空间关系和剖切结果来源。",
        "common_uses": ["由 Region 生成实体", "沿路径或绕轴形成构件体量", "通过 SectionSolid 导回二维剖切表达"],
        "pywin32_signature": "model_space.AddExtrudedSolid(...) / model_space.AddExtrudedSolidAlongPath(...) / model_space.AddRevolvedSolid(...)",
        "project_paths": ["cad/system/licad.py", "cad/system/content_analysis_dwg_file.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["create_region_and_extrude_solid", "section_3d_geometry_for_2d_expression", "read_3d_object_spatial_identity"],
        "source_topic_ids": ["acadauto:idh_3dsolid_object", "acadauto:idh_addextrudedsolid", "acadauto:idh_addextrudedsolidalongpath", "acadauto:idh_addrevolvedsolid", "acadauto:idh_sectionsolid"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_SECTION_REGION, RULE_3D_TRANSFORM, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "TranslateCoordinates",
        "kind": "method",
        "folder": "methods",
        "owners": ["Utility"],
        "source_terms": ["translatecoordinates method", "converting coordinates", "specifying 3d coordinates"],
        "purpose": "在 WCS/UCS/OCS/DCS 之间转换点或位移向量，是三维空间关系表达的基础方法。",
        "common_uses": ["在 WCS 与 OCS 之间换算点", "读取对象 OCS 点并还原到 WCS", "在布局/显示坐标与模型坐标之间换算"],
        "pywin32_signature": "utility.TranslateCoordinates(original_point, from_cs, to_cs, disp[, ocs_normal])",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_core.py", "cad/system/content_analysis_dwg_file.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "read_3d_object_spatial_identity"],
        "source_topic_ids": ["acadauto:idh_translatecoordinates", "acad_aag:GUID_06B18EED_D4E3_4B81_ACB8_037E884CB93D", "acad_aag:GUID_6954AAF3_7107_4D93_A2CE_FE859F3F9902"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "GetUCSMatrix",
        "kind": "method",
        "folder": "methods",
        "owners": ["UCS"],
        "source_terms": ["getucsmatrix method", "ucs matrix", "transformby"],
        "purpose": "获取 UCS 的 4x4 变换矩阵，用于把对象或点稳定地映射到指定坐标基准。",
        "common_uses": ["读取 UCS 变换矩阵", "配合 TransformBy 执行整体坐标基准变换", "建立从 UCS 到 WCS 的稳定映射"],
        "pywin32_signature": "ucs.GetUCSMatrix()",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_core.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "apply_3d_transform_to_objects"],
        "source_topic_ids": ["acadauto:idh_getucsmatrix", "acadauto:idh_ucs_object", "acadauto:idh_transformby"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_3D_TRANSFORM, RULE_VARIANT, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "Add3DPoly",
        "kind": "method",
        "folder": "methods",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["add3dpoly method", "3dpolyline object"],
        "purpose": "根据三维点数组创建 3dPolyline，是空间路径和轮廓骨架的正式创建入口。",
        "common_uses": ["建立空间路径", "建立三维轮廓", "为后续剖切或实体生成准备路径对象"],
        "pywin32_signature": "model_space.Add3DPoly(points_array)",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["create_3d_path_or_profile"],
        "source_topic_ids": ["acadauto:idh_add3dpoly", "acadauto:idh_3dpoly_object"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT],
    },
    {
        "symbol": "Add3DFace",
        "kind": "method",
        "folder": "methods",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["add3dface method", "3dface object"],
        "purpose": "根据三点或四点创建 3DFace，用于表达面、共面关系和剖切辅助面。",
        "common_uses": ["建立三维面", "表达构件平面关系", "为区域/剖切构造面级参考"],
        "pywin32_signature": "model_space.Add3DFace(point1, point2, point3[, point4])",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["create_3d_path_or_profile"],
        "source_topic_ids": ["acadauto:idh_add3dface", "acadauto:idh_3dface_object"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT],
    },
    {
        "symbol": "AddRegion",
        "kind": "method",
        "folder": "methods",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["addregion method", "region object", "creating regions"],
        "purpose": "把闭合共面轮廓转换成 Region，是从轮廓进入区域、实体和剖切逻辑的关键桥。",
        "common_uses": ["闭合轮廓转区域", "为挤出或旋转实体准备 profile", "为二维剖切表达准备中间区域对象"],
        "pywin32_signature": "model_space.AddRegion(object_list)",
        "project_paths": ["cad/system/licad.py", "cad/system/content_analysis_dwg_file.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["create_region_and_extrude_solid", "section_3d_geometry_for_2d_expression"],
        "source_topic_ids": ["acadauto:idh_addregion", "acadauto:idh_region_object", "acad_aag:GUID_4699B54A_2628_49FE_B093_0062FBEC37EA"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_SECTION_REGION, RULE_COORDINATE_SYSTEMS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "AddExtrudedSolid",
        "kind": "method",
        "folder": "methods",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["addextrudedsolid method", "3dsolid object"],
        "purpose": "根据 Region、高度和锥角创建 3DSolid，是从平面轮廓进入构件体量表达的主入口。",
        "common_uses": ["由剖面轮廓生成构件体量", "把区域转成可剖切实体", "建立空间构造关系"],
        "pywin32_signature": "model_space.AddExtrudedSolid(profile_region, height, taper_angle)",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py", "cad/system/content_analysis_dwg_file.py"],
        "related_tasks": ["create_region_and_extrude_solid"],
        "source_topic_ids": ["acadauto:idh_addextrudedsolid", "acadauto:idh_3dsolid_object"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_SECTION_REGION, RULE_COORDINATE_SYSTEMS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "AddExtrudedSolidAlongPath",
        "kind": "method",
        "folder": "methods",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["addextrudedsolidalongpath method", "3dsolid object"],
        "purpose": "根据 Region 和路径对象创建沿路径挤出的 3DSolid，适合表达沿轴线或轨迹生成的构件。",
        "common_uses": ["沿路径生成实体", "表达沿轴线构件", "把轮廓沿空间轨迹转成体量"],
        "pywin32_signature": "model_space.AddExtrudedSolidAlongPath(profile_region, path_object)",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py", "cad/system/content_analysis_dwg_file.py"],
        "related_tasks": ["create_region_and_extrude_solid", "create_3d_path_or_profile"],
        "source_topic_ids": ["acadauto:idh_addextrudedsolidalongpath", "acadauto:idh_3dsolid_object"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_COORDINATE_SYSTEMS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "AddRevolvedSolid",
        "kind": "method",
        "folder": "methods",
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "source_terms": ["addrevolvedsolid method", "3dsolid object"],
        "purpose": "根据 Region 与旋转轴生成旋转实体，用于表达由剖面绕轴形成的空间构件。",
        "common_uses": ["绕轴生成实体", "表达旋转对称构件", "从二维剖面进入三维体量"],
        "pywin32_signature": "model_space.AddRevolvedSolid(profile_region, axis_point, axis_dir, angle)",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["create_region_and_extrude_solid"],
        "source_topic_ids": ["acadauto:idh_addrevolvedsolid", "acadauto:idh_3dsolid_object"],
        "rule_refs": [RULE_3D_ENTITY_CREATION, RULE_COORDINATE_SYSTEMS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "SectionSolid",
        "kind": "method",
        "folder": "methods",
        "owners": ["3DSolid"],
        "source_terms": ["sectionsolid method", "section solid", "3dsolid object"],
        "purpose": "根据三点定义的平面剖切 3DSolid 并返回 Region，是把三维关系导回二维表达的核心方法。",
        "common_uses": ["获取剖切区域", "为二维剖面表达提供几何依据", "从实体生成截面 Region"],
        "pywin32_signature": "solid.SectionSolid(point1, point2, point3)",
        "project_paths": ["cad/system/licad.py", "cad/system/content_analysis_dwg_file.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["section_3d_geometry_for_2d_expression"],
        "source_topic_ids": ["acadauto:idh_sectionsolid", "acadauto:idh_3dsolid_object", "acadauto:idh_region_object"],
        "rule_refs": [RULE_SECTION_REGION, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "Move",
        "kind": "method",
        "folder": "methods",
        "owners": ["All Drawing Objects"],
        "source_terms": ["move method", "transforming objects"],
        "purpose": "按两个 3D 点定义位移，是最基础的空间对位方法之一。",
        "common_uses": ["对象平移到目标位置", "在变换链前做简单位移", "调整空间放置关系"],
        "pywin32_signature": "object.Move(point1, point2)",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["apply_3d_transform_to_objects"],
        "source_topic_ids": ["acadauto:idh_move", "acad_aag:GUID_19A5491D_7675_4ECF_A66A_5D309A14429F"],
        "rule_refs": [RULE_3D_TRANSFORM, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT],
    },
    {
        "symbol": "Rotate3D",
        "kind": "method",
        "folder": "methods",
        "owners": ["All Drawing Objects"],
        "source_terms": ["rotate3d method", "rotating in 3d"],
        "purpose": "围绕由两点定义的 3D 轴旋转对象，是空间方向调整的主入口。",
        "common_uses": ["围绕空间轴线旋转构件", "纠正三维对象方向", "统一对象空间姿态"],
        "pywin32_signature": "object.Rotate3D(point1, point2, rotation_angle_radians)",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["apply_3d_transform_to_objects"],
        "source_topic_ids": ["acadauto:idh_rotate3d", "acad_aag:GUID_3FEB0A3C_E4B1_40DF_A4DF_CAB22F1E2A92"],
        "rule_refs": [RULE_3D_TRANSFORM, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "Mirror3D",
        "kind": "method",
        "folder": "methods",
        "owners": ["All Drawing Objects"],
        "source_terms": ["mirror3d method", "mirror3d"],
        "purpose": "围绕由三点定义的平面镜像对象，用于表达对称关系和平面对位。",
        "common_uses": ["围绕平面生成对称对象", "用平面关系修正构件放置", "快速建立镜像空间表达"],
        "pywin32_signature": "ret = object.Mirror3D(point1, point2, point3)",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["apply_3d_transform_to_objects"],
        "source_topic_ids": ["acadauto:idh_mirror3d", "acadauto:idh_3dpoly_object", "acadauto:idh_region_object"],
        "rule_refs": [RULE_3D_TRANSFORM, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "ScaleEntity",
        "kind": "method",
        "folder": "methods",
        "owners": ["All Drawing Objects"],
        "source_terms": ["scaleentity method", "scale entity"],
        "purpose": "围绕基点在 X/Y/Z 方向等比缩放对象，用于统一空间尺寸关系。",
        "common_uses": ["统一构件比例", "调整实体或路径尺寸", "对位前做尺寸归一"],
        "pywin32_signature": "object.ScaleEntity(base_point, scale_factor)",
        "project_paths": ["cad/system/licad.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["apply_3d_transform_to_objects"],
        "source_topic_ids": ["acadauto:idh_scaleentity"],
        "rule_refs": [RULE_3D_TRANSFORM, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "TransformBy",
        "kind": "method",
        "folder": "methods",
        "owners": ["All Drawing Objects", "AttributeReference"],
        "source_terms": ["transformby method", "transformation matrix", "getucsmatrix"],
        "purpose": "使用 4x4 变换矩阵移动、缩放或旋转对象，是统一空间变换和基准切换的高级入口。",
        "common_uses": ["根据 UCS 矩阵整体变换对象", "统一执行平移+旋转+缩放", "把对象迁移到指定空间基准"],
        "pywin32_signature": "object.TransformBy(transformation_matrix)",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_core.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["apply_3d_transform_to_objects", "understand_and_convert_coordinate_systems"],
        "source_topic_ids": ["acadauto:idh_transformby", "acadauto:idh_getucsmatrix", "acad_aag:GUID_19A5491D_7675_4ECF_A66A_5D309A14429F"],
        "rule_refs": [RULE_3D_TRANSFORM, RULE_COORDINATE_SYSTEMS, RULE_VARIANT, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "ActiveUCS",
        "kind": "property",
        "folder": "properties",
        "owners": ["Document"],
        "source_terms": ["activeucs property", "ucs object"],
        "purpose": "表示当前活动 UCS，是从文档当前三维基准切入空间表达的正式属性入口。",
        "common_uses": ["读取当前活动 UCS", "切换后确认 UCS 是否到位", "为对象变换取基准矩阵"],
        "pywin32_signature": "C.doc.ActiveUCS",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_core.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "apply_3d_transform_to_objects"],
        "source_topic_ids": ["acadauto:idh_activeucs", "acadauto:idh_ucs_object"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_3D_TRANSFORM, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "Normal",
        "kind": "property",
        "folder": "properties",
        "owners": ["Entity"],
        "source_terms": ["normal property", "translatecoordinates", "ocs"],
        "purpose": "表示对象的三维法向量，是确定 OCS 和执行 OCS/WCS 换算的关键属性。",
        "common_uses": ["作为 TranslateCoordinates 的 OCSNormal", "判断对象平面方向", "还原对象真实空间姿态"],
        "pywin32_signature": "entity.Normal",
        "project_paths": ["cad/system/licad.py", "cad/system/content_analysis_dwg_file.py", "cad/scripts/CAD_basic.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "read_3d_object_spatial_identity"],
        "source_topic_ids": ["acadauto:idh_normal", "acadauto:idh_translatecoordinates"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "Elevation",
        "kind": "property",
        "folder": "properties",
        "owners": ["Hatch", "Polyline", "Section"],
        "source_terms": ["elevation property", "translatecoordinates", "polyline elevation"],
        "purpose": "表示对象当前高程，用于把仅含 XY 的对象点恢复为完整的 3D 空间点。",
        "common_uses": ["补全 OCS/WCS 转换中的 Z 值", "读取多段线或剖切对象高程", "还原对象空间位置"],
        "pywin32_signature": "entity.Elevation",
        "project_paths": ["cad/system/licad.py", "cad/system/content_analysis_dwg_file.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "read_3d_object_spatial_identity"],
        "source_topic_ids": ["acadauto:idh_elevation", "acadauto:idh_translatecoordinates"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "ElevationModelSpace",
        "kind": "property",
        "folder": "properties",
        "owners": ["Document"],
        "source_terms": ["elevationmodelspace property", "model space elevation"],
        "purpose": "表示模型空间当前高程，决定仅给 XY 时如何补出 Z 值。",
        "common_uses": ["在模型空间补全 3D 点", "校验当前模型空间高程基准", "防止误把二维输入当零高程"],
        "pywin32_signature": "C.doc.ElevationModelSpace",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_core.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "read_3d_object_spatial_identity"],
        "source_topic_ids": ["acadauto:idh_elevationmodelspace", "acadauto:ex_elevationmodelspace"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "ElevationPaperSpace",
        "kind": "property",
        "folder": "properties",
        "owners": ["Document"],
        "source_terms": ["elevationpaperspace property", "paper space elevation"],
        "purpose": "表示图纸空间当前高程，决定布局上下文里仅给 XY 时如何补出 Z 值。",
        "common_uses": ["在布局空间补全 3D 点", "校验图纸空间高程基准", "避免模型/图纸空间高程混淆"],
        "pywin32_signature": "C.doc.ElevationPaperSpace",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_core.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "read_3d_object_spatial_identity"],
        "source_topic_ids": ["acadauto:idh_elevationpaperspace", "acadauto:ex_elevationpaperspace"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_COMMON_FAILURES],
    },
    {
        "symbol": "ucs_matrix",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["getucsmatrix", "transformby", "ucs matrix"],
        "purpose": "统一说明 UCS 返回的 4x4 矩阵结构，以及它如何进入 TransformBy。",
        "common_uses": ["读取 UCS 变换矩阵", "把矩阵直接传给 TransformBy", "分析 UCS 到 WCS 的映射关系"],
        "pywin32_signature": "Variant (4x4 array of doubles)",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_core.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "apply_3d_transform_to_objects"],
        "source_topic_ids": ["acadauto:idh_getucsmatrix", "acadauto:idh_transformby"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_3D_TRANSFORM, RULE_VARIANT],
    },
    {
        "symbol": "ocs_point",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["translatecoordinates", "ocs", "normal", "elevation"],
        "purpose": "统一说明对象局部坐标点如何结合 Elevation 与 Normal 还原为空间点。",
        "common_uses": ["从 Polyline/LightweightPolyline 读取 OCS 点", "结合 Elevation 与 Normal 转到 WCS", "避免直接把 OCS 点当 WCS 点"],
        "pywin32_signature": "(x, y[, z]) + Elevation + Normal -> 3D WCS point",
        "project_paths": ["cad/system/content_analysis_dwg_file.py", "cad/system/licad.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "read_3d_object_spatial_identity"],
        "source_topic_ids": ["acadauto:idh_translatecoordinates", "acadauto:idh_normal", "acadauto:idh_elevation"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT],
    },
    {
        "symbol": "normal_vector",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["normal property", "ocs normal", "translatecoordinates"],
        "purpose": "统一说明法向量是方向向量而不是点，并作为 OCS/WCS 换算的输入。",
        "common_uses": ["作为 OCSNormal 传给 TranslateCoordinates", "确定对象平面法向", "描述剖切和平面方向"],
        "pywin32_signature": "(nx, ny, nz) as WCS unit vector",
        "project_paths": ["cad/system/licad.py", "cad/system/content_analysis_dwg_file.py"],
        "related_tasks": ["understand_and_convert_coordinate_systems", "read_3d_object_spatial_identity", "section_3d_geometry_for_2d_expression"],
        "source_topic_ids": ["acadauto:idh_normal", "acadauto:idh_translatecoordinates"],
        "rule_refs": [RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT],
    },
    {
        "symbol": "transform_matrix",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["transformby", "transformation matrix", "getucsmatrix"],
        "purpose": "统一说明 4x4 变换矩阵的旋转项与平移项布局，避免 TransformBy 传参错误。",
        "common_uses": ["构造 TransformBy 入参", "组合旋转和平移", "复用 GetUCSMatrix 返回矩阵"],
        "pywin32_signature": "((R00,R01,R02,T0),(R10,R11,R12,T1),(R20,R21,R22,T2),(0,0,0,1))",
        "project_paths": ["cad/system/licad.py", "cad/system/CAD_core.py"],
        "related_tasks": ["apply_3d_transform_to_objects", "understand_and_convert_coordinate_systems"],
        "source_topic_ids": ["acadauto:idh_transformby", "acadauto:idh_getucsmatrix"],
        "rule_refs": [RULE_3D_TRANSFORM, RULE_COORDINATE_SYSTEMS, RULE_VARIANT],
    },
    {
        "symbol": "section_plane_definition",
        "kind": "type_topic",
        "folder": "types_and_variants",
        "owners": ["pywin32", "ActiveX"],
        "source_terms": ["sectionsolid", "plane defined by three points", "section solid"],
        "purpose": "统一说明剖切平面由三个 3D 点定义，避免把视向或法向误当平面定义。",
        "common_uses": ["给 SectionSolid 定义剖切平面", "组织剖面表达的输入", "统一构件截面提取规则"],
        "pywin32_signature": "(point1, point2, point3) in 3D WCS",
        "project_paths": ["cad/system/licad.py", "cad/system/content_analysis_dwg_file.py"],
        "related_tasks": ["section_3d_geometry_for_2d_expression"],
        "source_topic_ids": ["acadauto:idh_sectionsolid", "acadauto:idh_3dsolid_object"],
        "rule_refs": [RULE_SECTION_REGION, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT],
    },
]


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def uniq(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip()).lower()


def build_manifest_lookup(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("topic_id", "")): row for row in records if row.get("topic_id")}


def find_matches(records: list[dict[str, Any]], terms: list[str], limit: int = 5) -> list[dict[str, Any]]:
    lowered = [normalize(term) for term in terms if normalize(term)]
    matches: list[tuple[int, dict[str, Any]]] = []
    for row in records:
        corpus = " ".join([str(row.get("title", "")), str(row.get("basename", "")), " ".join(row.get("keywords", [])), str(row.get("path", ""))]).lower()
        score = 0
        for term in lowered:
            if re.search(rf"(?<![a-z0-9_]){re.escape(term)}(?![a-z0-9_])", corpus):
                score += 80
            elif term in corpus:
                score += 35
        if not score:
            continue
        score += int(row.get("project_score", 0)) * 10
        if row.get("status") == "keep":
            score += 20
        matches.append((score, row))
    matches.sort(key=lambda item: (-item[0], item[1].get("title", "")))
    return [row for _, row in matches[:limit]]


def resolve_trace(spec: dict[str, Any], records: list[dict[str, Any]], manifest_lookup: dict[str, dict[str, Any]], topic_map: dict[str, str]) -> tuple[list[str], list[str]]:
    topic_ids = list(spec.get("source_topic_ids", []))
    html_paths = list(spec.get("source_html_paths", []))
    for match in find_matches(records, list(spec.get("source_terms", []))):
        if match.get("topic_id"):
            topic_ids.append(str(match["topic_id"]))
        if match.get("path"):
            html_paths.append(str(match["path"]))
    for topic_id in uniq(topic_ids):
        if topic_id in manifest_lookup and manifest_lookup[topic_id].get("path"):
            html_paths.append(str(manifest_lookup[topic_id]["path"]))
        elif topic_id in topic_map:
            html_paths.append(str(topic_map[topic_id]))
    return uniq(topic_ids), uniq(html_paths)


def render_card(spec: dict[str, Any], source_topic_ids: list[str], source_html_paths: list[str]) -> str:
    lines = [
        f"# {spec['symbol']}",
        "",
        "## 基本信息",
        f"- kind: `{spec['kind']}`",
        f"- owners: `{', '.join(spec.get('owners', []))}`",
        f"- pywin32: `{spec.get('pywin32_signature', '')}`",
        "",
        "## 作用",
        spec["purpose"],
        "",
        "## 高频场景",
    ]
    lines.extend(f"- {item}" for item in spec.get("common_uses", []))
    lines.extend(["", "## 项目路径"])
    lines.extend(f"- `{item}`" for item in spec.get("project_paths", []))
    lines.extend(["", "## 相关任务"])
    lines.extend(f"- `{item}`" for item in spec.get("related_tasks", []))
    lines.extend(["", "## 规则与来源", "- rule_refs:"])
    lines.extend(f"- `{item}`" for item in spec.get("rule_refs", []))
    lines.extend(["- source_topic_ids:"])
    lines.extend(f"- `{item}`" for item in source_topic_ids)
    lines.extend(["- source_html_paths:"])
    lines.extend(f"- `{item}`" for item in source_html_paths)
    return "\n".join(lines) + "\n"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def update_existing_core_meta(records: list[dict[str, Any]], manifest_lookup: dict[str, dict[str, Any]], topic_map: dict[str, str]) -> set[str]:
    symbols: set[str] = set()
    for meta_path in CORE_DIR.rglob("*.meta.json"):
        meta = load_json(meta_path)
        if not isinstance(meta, dict) or not meta.get("symbol"):
            continue
        symbols.add(str(meta["symbol"]))
        spec_like = {"source_terms": meta.get("source_terms", [meta["symbol"]]), "source_topic_ids": meta.get("source_topic_ids", []), "source_html_paths": meta.get("source_html_paths", [])}
        topic_ids, html_paths = resolve_trace(spec_like, records, manifest_lookup, topic_map)
        haystack = " ".join([str(meta.get("symbol", "")), str(meta.get("pywin32_signature", "")), " ".join(meta.get("owners", []))]).lower()
        rule_refs = list(meta.get("rule_refs", []))
        if not rule_refs:
            if any(token in haystack for token in ["variant", "array", "coordinate", "bounding", "point"]):
                rule_refs.extend([RULE_VARIANT, RULE_POINT_ARRAY, RULE_PYWIN32_TYPES])
            if any(token in haystack for token in ["selection", "layout", "document", "block", "attribute", "layer"]):
                rule_refs.append(RULE_COLLECTION)
            if "sendcommand" in haystack:
                rule_refs.append(RULE_SENDCOMMAND)
            rule_refs.append(RULE_COMMON_FAILURES)
        meta["project_refs"] = uniq(list(meta.get("project_refs", [])) + list(meta.get("project_paths", [])))
        meta["rule_refs"] = uniq(rule_refs)
        meta["source_topic_ids"] = topic_ids
        meta["source_html_paths"] = html_paths
        write_json(meta_path, meta)
    return symbols


def write_new_symbols(records: list[dict[str, Any]], manifest_lookup: dict[str, dict[str, Any]], topic_map: dict[str, str]) -> set[str]:
    symbols: set[str] = set()
    for spec in NEW_SYMBOL_SPECS:
        topic_ids, html_paths = resolve_trace(spec, records, manifest_lookup, topic_map)
        folder = CORE_DIR / str(spec["folder"])
        md_path = folder / f"{spec['symbol']}.md"
        meta_path = folder / f"{spec['symbol']}.meta.json"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_card(spec, topic_ids, html_paths), encoding="utf-8", newline="\n")
        write_json(
            meta_path,
            {
                "symbol": spec["symbol"],
                "kind": spec["kind"],
                "owners": spec.get("owners", []),
                "source_terms": spec.get("source_terms", []),
                "value_level": "high",
                "related_tasks": spec.get("related_tasks", []),
                "pywin32_signature": spec.get("pywin32_signature", ""),
                "risk_tags": spec.get("risks", []),
                "project_paths": spec.get("project_paths", []),
                "project_refs": spec.get("project_paths", []),
                "rule_refs": spec.get("rule_refs", []),
                "path_md": str(md_path.relative_to(ROOT)).replace("\\", "/"),
                "source_topic_ids": topic_ids,
                "source_html_paths": html_paths,
            },
        )
        symbols.add(str(spec["symbol"]))
    return symbols


def build_candidates(core_symbols: set[str]) -> list[dict[str, Any]]:
    manifest_rows = load_jsonl(MANIFEST_PATH)
    value_rows = load_jsonl(VALUE_RANKING_PATH)
    task_index = load_json(TASK_INDEX_PATH)
    task_map = load_json(TASK_MAP_PATH)
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    keywords = [
        "layout", "plot", "block", "attribute", "selection", "text", "layer", "variable",
        "variant", "collection", "point", "bounding", "catalog", "ucs", "ocs", "wcs",
        "3d", "polyline", "region", "solid", "section", "transform", "rotate3d",
        "mirror3d", "scaleentity", "translatecoordinates", "normal", "elevation",
    ]
    for record in manifest_rows + value_rows:
        title = str(record.get("title", ""))
        basename = str(record.get("basename", "")).lower()
        score = int(record.get("project_score", 0)) * 10
        why: list[str] = []
        if any(token in title.lower() for token in keywords):
            score += 25
            why.append("project keyword")
        if basename in SPATIAL_3D_BASENAME_WHITELIST:
            score += 80
            why.append("fourth-round spatial 3d whitelist")
        if any(token in title.lower() for token in ["method", "property", "object", "collection", "system variable"]):
            score += 15
            why.append("symbol-like title")
        if score < 20:
            continue
        symbol = re.sub(r"\s+(Example|object|method|property).*", "", title, flags=re.IGNORECASE).replace("About ", "").strip()
        key = (symbol, str(record.get("topic_id", "")))
        if key in seen:
            continue
        seen.add(key)
        rows.append({"symbol": symbol, "kind_guess": str(record.get("kind_guess", "topic")), "owner_guess": str(record.get("owner_guess", "")), "source_topic_id": str(record.get("topic_id", "")), "source_html_path": str(record.get("path", "")), "why_selected": ", ".join(why), "score": score, "already_in_core": symbol in core_symbols})
    tasks = task_index.get("tasks", []) if isinstance(task_index, dict) else []
    for task in tasks:
        for symbol in task.get("symbols", []):
            if symbol in core_symbols:
                continue
            rows.append({"symbol": symbol, "kind_guess": "task_referenced_symbol", "owner_guess": "", "source_topic_id": "", "source_html_path": "", "why_selected": f"referenced by {task.get('task_id', '')}", "score": 999, "already_in_core": False})
    if isinstance(task_map, dict):
        for task_id, payload in task_map.items():
            if not isinstance(payload, dict):
                continue
            for symbol in payload.get("symbols", []):
                if symbol in core_symbols:
                    continue
                rows.append({"symbol": symbol, "kind_guess": "task_referenced_symbol", "owner_guess": "", "source_topic_id": "", "source_html_path": "", "why_selected": f"referenced by {task_id}", "score": 999, "already_in_core": False})
    rows.sort(key=lambda item: (-int(item["score"]), item["symbol"], item["source_topic_id"]))
    return rows


def main() -> None:
    manifest_rows = load_jsonl(MANIFEST_PATH)
    manifest_lookup = build_manifest_lookup(manifest_rows)
    topic_map = load_json(TOPIC_PATH_MAP_PATH)
    core_symbols = update_existing_core_meta(manifest_rows, manifest_lookup, topic_map)
    core_symbols.update(write_new_symbols(manifest_rows, manifest_lookup, topic_map))
    write_jsonl(CANDIDATE_PATH, build_candidates(core_symbols))
    print(f"Updated existing core metas and ensured {len(NEW_SYMBOL_SPECS)} generated symbol cards.")
    print(f"Wrote {CANDIDATE_PATH}")


if __name__ == "__main__":
    main()
