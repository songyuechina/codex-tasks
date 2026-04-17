from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TASK_DIR = ROOT / "04_task_cards"
VALIDATION_DIR = ROOT / "07_validation"
CORE_DIR = ROOT / "03_core_symbols"
TOPIC_PATH_MAP_PATH = ROOT / "06_on_demand_index" / "topic_path_map.json"
TASK_MAP_PATH = VALIDATION_DIR / "task_to_existing_code_map.json"
TASK_INDEX_SCHEMA_VERSION = "2026-04-17-task-entry-v5"

REF_DWG_MIXED = "cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg"
REF_DWG_PRINT = "cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg"
REF_DWG_ANOMALY = "cad/scripts/drawing_basic_service/print/cases/assets/农建房施工图【电气】-0930_t6_t3.dwg"

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

TASK_EXACT_ENTRIES = {
    "connect_active_document": {
        "owners": ["Application", "Documents", "Document"],
        "implementation_entries": [{"project_function": "get_acad_doc", "module_path": "cad/system/licad.py"}],
        "aliases_en": ["connect active document", "get active document", "attach cad document", "connect autocad session"],
        "aliases_zh": ["连接CAD", "获取活动文档", "连接AutoCAD"],
        "keywords_zh": ["活动文档", "连接", "受控入口"],
        "pywin32_rules": [RULE_COMMON_PATTERNS, RULE_COMMON_FAILURES, RULE_PYWIN32_TYPES],
        "reference_dwgs": [REF_DWG_MIXED],
        "reference_objects": ["Application", "Document"],
    },
    "open_save_close_document": {
        "owners": ["Documents", "Document"],
        "implementation_entries": [
            {"project_function": "open_file", "module_path": "cad/system/licad.py"},
            {"project_function": "save_file", "module_path": "cad/system/licad.py"},
            {"project_function": "close_file", "module_path": "cad/system/licad.py"},
            {"project_function": "close_dwg_by_name", "module_path": "cad/system/licad.py"},
        ],
        "aliases_en": ["open save close document", "document lifecycle", "open drawing file", "close active drawing"],
        "aliases_zh": ["打开保存关闭文档", "DWG 生命周期", "打开图纸", "关闭图纸"],
        "keywords_zh": ["打开", "保存", "关闭", "文档"],
        "pywin32_rules": [RULE_COMMON_PATTERNS, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_MIXED],
        "reference_objects": ["Documents", "Document"],
    },
    "determine_space_and_layout": {
        "owners": ["Document", "Layout"],
        "implementation_entries": [
            {"project_function": "get_layout_names", "module_path": "cad/system/CAD_core.py"},
            {"project_function": "switch_to_layout", "module_path": "cad/system/CAD_core.py"},
            {"project_function": "current_space_only", "module_path": "cad/system/CAD_selection.py"},
        ],
        "aliases_en": ["determine space and layout", "detect modelspace paperspace", "check current layout context"],
        "aliases_zh": ["判断模型空间图纸空间当前布局", "检查当前布局上下文"],
        "keywords_zh": ["模型空间", "图纸空间", "布局", "上下文"],
        "pywin32_rules": [RULE_COMMON_PATTERNS, RULE_COLLECTION],
        "reference_dwgs": [REF_DWG_MIXED],
        "reference_objects": ["Document", "Layout", "ModelSpace", "PaperSpace"],
    },
    "enumerate_layouts": {
        "owners": ["Layouts", "Layout", "Document"],
        "implementation_entries": [
            {"project_function": "get_layout_names", "module_path": "cad/system/CAD_core.py"},
            {"project_function": "get_layout_names", "module_path": "cad/scripts/drawing_basic_service/print/print_area_analysis.py"},
        ],
        "aliases_en": ["enumerate layouts", "list layouts", "get layout names"],
        "aliases_zh": ["枚举所有布局", "获取布局列表"],
        "keywords_zh": ["布局", "枚举", "列表"],
        "pywin32_rules": [RULE_COLLECTION, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_MIXED],
        "reference_objects": ["Layouts", "Layout"],
    },
    "switch_to_target_layout": {
        "owners": ["Document", "Layouts", "Layout"],
        "implementation_entries": [
            {"project_function": "switch_to_layout", "module_path": "cad/system/CAD_core.py"},
            {"project_function": "switch_to_layout", "module_path": "cad/scripts/drawing_basic_service/print/print_area_analysis.py"},
            {"project_function": "send_cmd_with_sync", "module_path": "cad/system/CAD_coordination.py"},
        ],
        "aliases_en": ["switch to target layout", "activate layout", "change active layout"],
        "aliases_zh": ["切换到指定布局", "切换布局", "激活布局"],
        "keywords_zh": ["布局切换", "目标布局", "激活"],
        "pywin32_rules": [RULE_SENDCOMMAND, RULE_COLLECTION, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_MIXED, REF_DWG_PRINT],
        "reference_objects": ["Document", "Layout"],
    },
    "build_selection_set": {
        "owners": ["SelectionSets", "SelectionSet"],
        "implementation_entries": [
            {"project_function": "ss_select", "module_path": "cad/system/CAD_selection.py"},
            {"project_function": "select_entities_in_window", "module_path": "cad/system/CAD_selection.py"},
            {"project_function": "send_cmd_with_sync", "module_path": "cad/system/CAD_coordination.py"},
        ],
        "aliases_en": ["build selection set", "select objects by window", "cad selection workflow"],
        "aliases_zh": ["构造选择集", "窗口选择对象", "选择对象"],
        "keywords_zh": ["选择集", "窗口选", "对象选择"],
        "pywin32_rules": [RULE_COLLECTION, RULE_VARIANT, RULE_POINT_ARRAY, RULE_SENDCOMMAND],
        "reference_dwgs": [REF_DWG_MIXED, REF_DWG_PRINT],
        "reference_objects": ["SelectionSet", "AcDbPolyline", "AcDbBlockReference"],
    },
    "traverse_objects_and_read_identity": {
        "owners": ["Entity", "SelectionSet"],
        "implementation_entries": [
            {"project_function": "collect_space_entity_snapshots", "module_path": "cad/scripts/drawing_basic_service/print/print_area_content_analysis.py"},
            {"project_function": "get_dwg_graphics_summary", "module_path": "cad/system/content_analysis_dwg_file.py"},
        ],
        "aliases_en": ["traverse objects and read identity", "read objectname handle layer", "entity identity scan"],
        "aliases_zh": ["遍历对象并读取标识", "读取ObjectName Handle Layer"],
        "keywords_zh": ["对象遍历", "句柄", "图层", "类型识别"],
        "pywin32_rules": [RULE_COLLECTION, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT, REF_DWG_ANOMALY],
        "reference_objects": ["AcDbEntity", "AcDbBlockReference", "SelectionSet"],
    },
    "get_bounding_box_and_object_counts": {
        "owners": ["Entity", "SelectionSet", "BlockReference"],
        "implementation_entries": [
            {"project_function": "collect_area_content_metrics", "module_path": "cad/scripts/drawing_basic_service/print/print_area_content_analysis.py"},
            {"project_function": "get_dwg_graphics_summary", "module_path": "cad/system/content_analysis_dwg_file.py"},
        ],
        "aliases_en": ["get bounding box and object counts", "collect bbox metrics", "count objects by type"],
        "aliases_zh": ["获取边界框和对象统计", "边界框统计", "对象计数"],
        "keywords_zh": ["边界框", "统计", "计数", "打印框"],
        "pywin32_rules": [RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT, REF_DWG_ANOMALY],
        "reference_objects": ["AcDbPolyline", "AcDbBlockReference", "AcDbText", "AcDbMText"],
    },
    "create_basic_geometry_smoke": {
        "owners": ["ModelSpace", "PaperSpace", "Block"],
        "implementation_entries": [
            {"project_function": "draw_outline", "module_path": "cad/scripts/Scheme_drawing/draw_building_outline.py"},
            {"project_function": "ensure_layer", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "get_acad_doc", "module_path": "cad/system/licad.py"},
        ],
        "aliases_en": ["create basic geometry smoke", "geometry smoke test", "add line polyline text"],
        "aliases_zh": ["创建基础几何对象", "几何烟雾测试", "添加直线文字多段线"],
        "keywords_zh": ["基础几何", "直线", "多段线", "文字"],
        "pywin32_rules": [RULE_POINT_ARRAY, RULE_VARIANT, RULE_PYWIN32_TYPES],
        "reference_dwgs": [REF_DWG_MIXED],
        "reference_objects": ["ModelSpace", "AcDbLine", "AcDbPolyline", "AcDbText"],
    },
    "read_block_attributes": {
        "owners": ["BlockReference", "AttributeReference"],
        "implementation_entries": [
            {"project_function": "get_block_attributes_dict", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "_extract_attribute_fields", "module_path": "cad/scripts/drawing_basic_service/print/print_info_analysis.py"},
        ],
        "aliases_en": ["read block attributes", "extract title block fields", "get attribute values from block reference"],
        "aliases_zh": ["读取块属性", "提取图签字段", "获取属性值"],
        "keywords_zh": ["块属性", "图签", "属性字段"],
        "pywin32_rules": [RULE_COLLECTION, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT, REF_DWG_ANOMALY],
        "reference_objects": ["AcDbBlockReference", "AcDbAttribute", "AcDbMText"],
    },
    "insert_block_or_dwg": {
        "owners": ["Block", "BlockReference", "ModelSpace", "PaperSpace"],
        "implementation_entries": [
            {"project_function": "insert_block_into_autocad", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "insert_file_exploded", "module_path": "cad/system/CAD_core.py"},
        ],
        "aliases_en": ["insert block or dwg", "insert title block template", "insert external drawing"],
        "aliases_zh": ["插入块或插入DWG", "插入图签模板", "插入外部图纸"],
        "keywords_zh": ["插块", "插入DWG", "炸开"],
        "pywin32_rules": [RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT],
        "reference_objects": ["Block", "AcDbBlockReference"],
    },
    "update_titleblock_fields": {
        "owners": ["BlockReference", "AttributeReference"],
        "implementation_entries": [
            {"project_function": "process_drawing_names_and_fill_titleblocks", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "update_catalog_titleblocks_from_excel", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "fill_block_attributes_with_tag_name", "module_path": "cad/scripts/CAD_basic.py"},
        ],
        "aliases_en": ["update titleblock fields", "fill title block attributes", "write drawing info to title block"],
        "aliases_zh": ["更新图签属性字段", "回写图签字段", "填写图签属性"],
        "keywords_zh": ["图签", "回写", "属性字段", "图名图号"],
        "pywin32_rules": [RULE_COLLECTION, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT],
        "reference_objects": ["AcDbBlockReference", "AcDbAttribute"],
    },
    "manage_layers": {
        "owners": ["Layers", "Layer", "Document"],
        "implementation_entries": [
            {"project_function": "ensure_layer", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "draw_outline", "module_path": "cad/scripts/Scheme_drawing/draw_building_outline.py"},
        ],
        "aliases_en": ["manage layers", "create switch layer", "ensure drawing layer"],
        "aliases_zh": ["读取创建切换图层", "图层管理", "确保图层存在"],
        "keywords_zh": ["图层", "创建图层", "切换图层"],
        "pywin32_rules": [RULE_COLLECTION, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_MIXED],
        "reference_objects": ["Layers", "Layer"],
    },
    "read_layout_plot_info": {
        "owners": ["Layout", "Plot"],
        "implementation_entries": [
            {"project_function": "analyze_print_info_jobs", "module_path": "cad/scripts/drawing_basic_service/print/print_info_analysis.py"},
            {"project_function": "collect_print_jobs", "module_path": "cad/scripts/drawing_basic_service/print/print_policy.py"},
        ],
        "aliases_en": ["read layout plot info", "inspect plot configuration", "read layout paper and window"],
        "aliases_zh": ["读取布局打印信息", "读取打印配置", "读取纸张窗口范围"],
        "keywords_zh": ["打印信息", "布局打印", "纸张", "打印窗口"],
        "pywin32_rules": [RULE_COLLECTION, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT, REF_DWG_ANOMALY],
        "reference_objects": ["Layout", "Plot", "AcDbBlockReference"],
    },
    "execute_layout_plot": {
        "owners": ["Layout", "Plot", "Document"],
        "implementation_entries": [
            {"project_function": "execute_print_plan", "module_path": "cad/scripts/drawing_basic_service/print/print_executor.py"},
            {"project_function": "export_layout_window_lisp_fit", "module_path": "cad/scripts/drawing_basic_service/print/print_executor.py"},
            {"project_function": "send_cmd_with_sync", "module_path": "cad/system/CAD_coordination.py"},
        ],
        "aliases_en": ["execute layout plot", "plot layout to pdf", "export layout window"],
        "aliases_zh": ["执行布局窗口打印", "输出布局PDF", "导出打印窗口"],
        "keywords_zh": ["打印PDF", "布局输出", "打印执行"],
        "pywin32_rules": [RULE_SENDCOMMAND, RULE_POINT_ARRAY, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT, REF_DWG_ANOMALY],
        "reference_objects": ["Layout", "Plot", "AcDbPolyline"],
    },
    "build_print_plan_and_info": {
        "owners": ["Layout", "BlockReference", "Plot"],
        "implementation_entries": [
            {"project_function": "collect_print_jobs", "module_path": "cad/scripts/drawing_basic_service/print/print_policy.py"},
            {"project_function": "build_print_plan", "module_path": "cad/scripts/drawing_basic_service/print/print_policy.py"},
            {"project_function": "analyze_print_info_jobs", "module_path": "cad/scripts/drawing_basic_service/print/print_info_analysis.py"},
        ],
        "aliases_en": ["build print plan and info", "collect print jobs", "assemble plot execution plan"],
        "aliases_zh": ["构建打印计划和打印信息", "收集打印作业", "组装打印计划"],
        "keywords_zh": ["打印计划", "打印信息", "作业收集"],
        "pywin32_rules": [RULE_COLLECTION, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT, REF_DWG_ANOMALY],
        "reference_objects": ["Layout", "AcDbPolyline", "AcDbBlockReference"],
    },
    "sendcommand_fallback": {
        "owners": ["Document"],
        "implementation_entries": [
            {"project_function": "send_cmd_with_sync", "module_path": "cad/system/CAD_coordination.py"},
            {"project_function": "SendCommand", "module_path": "cad/system/licad.py"},
        ],
        "aliases_en": ["sendcommand fallback", "command line fallback", "synchronize sendcommand"],
        "aliases_zh": ["SendCommand命令回退", "命令行回退", "同步命令发送"],
        "keywords_zh": ["命令回退", "SendCommand", "同步等待"],
        "pywin32_rules": [RULE_SENDCOMMAND, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_MIXED, REF_DWG_PRINT],
        "reference_objects": ["Document", "Layout"],
    },
    "insert_company_title_block": {
        "owners": ["BlockReference", "Block"],
        "implementation_entries": [
            {"project_function": "insert_company_label_common_block", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "insert_block_into_autocad", "module_path": "cad/scripts/CAD_basic.py"},
        ],
        "aliases_en": ["insert company title block", "insert company label block", "place standard title block"],
        "aliases_zh": ["插入公司通用图签", "插入公司图签块", "放置标准图签"],
        "keywords_zh": ["公司图签", "插入图签", "标准图签"],
        "pywin32_rules": [RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT],
        "reference_objects": ["AcDbBlockReference", "AcDbAttribute"],
    },
    "generate_or_update_catalog": {
        "owners": ["BlockReference", "AttributeReference", "ModelSpace"],
        "implementation_entries": [
            {"project_function": "write_catalog_from_excel_to_cad", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "update_catalog_titleblocks_from_excel", "module_path": "cad/scripts/CAD_basic.py"},
        ],
        "aliases_en": ["generate or update catalog", "write drawing list from excel", "update catalog title blocks"],
        "aliases_zh": ["生成目录或更新目录图签", "从Excel写目录", "更新目录图签"],
        "keywords_zh": ["目录", "Excel", "目录图签", "目录页"],
        "pywin32_rules": [RULE_COLLECTION, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT],
        "reference_objects": ["AcDbText", "AcDbMText", "AcDbBlockReference"],
    },
    "understand_and_convert_coordinate_systems": {
        "owners": ["Document", "UCS", "Utility"],
        "implementation_entries": [
            {"project_function": "get_entity_full_info", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "get_entity_geometry_info", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "get_dwg_graphics_summary", "module_path": "cad/system/content_analysis_dwg_file.py"},
        ],
        "aliases_en": ["understand and convert coordinate systems", "convert coordinates between wcs ucs ocs", "translate coordinates and ucs"],
        "aliases_zh": ["理解并转换坐标系", "坐标系转换", "WCS UCS OCS 转换"],
        "keywords_zh": ["坐标系", "坐标转换", "UCS", "OCS", "WCS"],
        "pywin32_rules": [RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_MIXED, REF_DWG_PRINT],
        "reference_objects": ["UCS", "3d_point", "AcDbPolyline"],
    },
    "create_3d_path_or_profile": {
        "owners": ["ModelSpace", "Block", "3dPolyline", "3DFace"],
        "implementation_entries": [
            {"project_function": "draw_outline", "module_path": "cad/scripts/Scheme_drawing/draw_building_outline.py"},
            {"project_function": "draw_polyline", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "draw_lwpolyline", "module_path": "cad/scripts/CAD_basic.py"},
        ],
        "aliases_en": ["create 3d path or profile", "build 3d polyline path", "create profile for region or solid"],
        "aliases_zh": ["创建三维路径或轮廓", "建立三维路径", "建立轮廓 profile"],
        "keywords_zh": ["三维路径", "轮廓", "3dPolyline", "3DFace"],
        "pywin32_rules": [RULE_3D_ENTITY_CREATION, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT],
        "reference_dwgs": [REF_DWG_MIXED],
        "reference_objects": ["3dPolyline", "3DFace"],
    },
    "create_region_and_extrude_solid": {
        "owners": ["ModelSpace", "Region", "3DSolid"],
        "implementation_entries": [
            {"project_function": "insert_region_v2", "module_path": "cad/system/CAD_core.py"},
            {"project_function": "create_block_from_region_cad", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "get_entity_geometry_info", "module_path": "cad/scripts/CAD_basic.py"},
        ],
        "aliases_en": ["create region and extrude solid", "convert profile to region and solid", "extrude region to solid"],
        "aliases_zh": ["创建 Region 并挤出 Solid", "轮廓转区域再转实体", "挤出实体"],
        "keywords_zh": ["Region", "3DSolid", "挤出", "轮廓转实体"],
        "pywin32_rules": [RULE_3D_ENTITY_CREATION, RULE_SECTION_REGION, RULE_COORDINATE_SYSTEMS, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_MIXED, REF_DWG_PRINT],
        "reference_objects": ["Region", "3DSolid"],
    },
    "apply_3d_transform_to_objects": {
        "owners": ["3dPolyline", "Region", "3DSolid", "Document"],
        "implementation_entries": [
            {"project_function": "move_entities_in_region", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "transform_point_by_block", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "get_obj_loc", "module_path": "cad/system/CAD_core.py"},
        ],
        "aliases_en": ["apply 3d transform to objects", "rotate mirror scale transform objects", "3d object alignment"],
        "aliases_zh": ["对对象应用三维变换", "三维变换对象", "空间对位"],
        "keywords_zh": ["Rotate3D", "Mirror3D", "ScaleEntity", "TransformBy", "空间对位"],
        "pywin32_rules": [RULE_3D_TRANSFORM, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_MIXED, REF_DWG_PRINT],
        "reference_objects": ["3dPolyline", "Region", "3DSolid"],
    },
    "section_3d_geometry_for_2d_expression": {
        "owners": ["3DSolid", "Region", "Document"],
        "implementation_entries": [
            {"project_function": "get_dwg_graphics_summary", "module_path": "cad/system/content_analysis_dwg_file.py"},
            {"project_function": "collect_space_entity_snapshots", "module_path": "cad/scripts/drawing_basic_service/print/print_area_content_analysis.py"},
            {"project_function": "get_boundingbox_from_objects", "module_path": "cad/scripts/CAD_basic.py"},
        ],
        "aliases_en": ["section 3d geometry for 2d expression", "section solid for 2d drawing logic", "derive 2d expression from 3d section"],
        "aliases_zh": ["对三维几何做剖切并服务二维表达", "三维剖切转二维表达", "SectionSolid"],
        "keywords_zh": ["剖切", "SectionSolid", "二维表达", "剖面"],
        "pywin32_rules": [RULE_SECTION_REGION, RULE_COORDINATE_SYSTEMS, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT, REF_DWG_ANOMALY],
        "reference_objects": ["3DSolid", "Region"],
    },
    "read_3d_object_spatial_identity": {
        "owners": ["Entity", "3dPolyline", "Region", "3DSolid"],
        "implementation_entries": [
            {"project_function": "get_entity_full_info", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "get_entity_geometry_info", "module_path": "cad/scripts/CAD_basic.py"},
            {"project_function": "get_dwg_graphics_summary", "module_path": "cad/system/content_analysis_dwg_file.py"},
        ],
        "aliases_en": ["read 3d object spatial identity", "inspect 3d object coordinates normal elevation", "read spatial identity"],
        "aliases_zh": ["读取三维对象空间身份", "读取对象空间身份", "坐标法向高程读取"],
        "keywords_zh": ["空间身份", "Coordinates", "Normal", "Elevation", "包围盒"],
        "pywin32_rules": [RULE_COORDINATE_SYSTEMS, RULE_SECTION_REGION, RULE_POINT_ARRAY, RULE_VARIANT, RULE_COMMON_FAILURES],
        "reference_dwgs": [REF_DWG_PRINT, REF_DWG_ANOMALY],
        "reference_objects": ["3dPolyline", "Region", "3DSolid", "AcDbEntity"],
    },
}


TASKS = [
    {
        "slug": "connect_active_document",
        "folder": "01_connect_and_document",
        "title": "任务卡：连接 AutoCAD 并获取活动文档",
        "goal": "在 CAD2021 + pywin32 环境里，以项目受控入口获取稳定的活动文档对象。",
        "priority_path": [
            "优先使用 `from system.licad import C`",
            "连接异常时先看 `licad.get_acad_doc()` 的启动与自愈逻辑",
            "避免业务层长期直接使用 `GetActiveObject` / `Dispatch`",
        ],
        "symbols": ["Application", "Documents", "Document"],
        "steps": [
            "导入 `C` 并访问 `C.doc`",
            "若首次连接失败，检查天正受控入口是否可启动",
            "确认 `ActiveDocument` 已就绪并能读取 `doc.Name`",
            "必要时做一次轻量 COM 烟雾验证",
        ],
        "notes": ["项目统一连接规则优先于 CHM 原始示例。"],
        "failures": ["CAD 进程存在但 COM 未就绪", "应用已连接但无文档", "gen_py 缓存损坏"],
        "verify": ["读取当前 `doc.Name`", "读取 `C.doc.ModelSpace` 不报错"],
        "project_refs": ["cad/system/licad.py"],
        "keywords": ["connect", "active document", "licad", "cad2021"],
    },
    {
        "slug": "open_save_close_document",
        "folder": "01_connect_and_document",
        "title": "任务卡：打开 / 保存 / 关闭文档",
        "goal": "对 DWG 文档执行基础文件生命周期操作，并保持当前环境稳定。",
        "priority_path": [
            "先走 `Documents` / `Document` 的 COM 路径",
            "若任务已纳入打印主链，优先复用 `print_runner.py` 和执行链现有入口",
        ],
        "symbols": ["Documents", "Document", "Application"],
        "steps": [
            "通过 `C.acad.Documents` 打开或新建文档",
            "对目标文档执行保存",
            "在关闭前确认无待处理命令态",
            "批量任务后恢复到项目预期状态",
        ],
        "notes": ["真实打印任务里不要绕过执行链手写零散打开/关闭逻辑。"],
        "failures": ["文件被占用", "切文档时活动文档未同步", "关闭后引用悬空"],
        "verify": ["文档数量变化符合预期", "关闭后活动文档重新可读"],
        "project_refs": ["cad/system/licad.py", "cad/system/CAD_core.py", "cad/scripts/drawing_basic_service/print/print_runner.py"],
        "keywords": ["open", "save", "close", "document"],
    },
    {
        "slug": "determine_space_and_layout",
        "folder": "02_space_and_layout",
        "title": "任务卡：判断模型空间 / 图纸空间 / 当前布局",
        "goal": "在后续打印、选区、图签扫描前确认当前空间上下文。",
        "priority_path": [
            "先看 `Document.ActiveLayout`、`ModelSpace`、`PaperSpace`",
            "需要空间过滤时优先复用 `CAD_selection.py` 的现有能力",
        ],
        "symbols": ["Document", "ModelSpace", "PaperSpace", "ActiveLayout", "GetVariable"],
        "steps": [
            "读取当前 `ActiveLayout.Name`",
            "判断当前任务是模型空间、布局块还是图纸空间扫描",
            "必要时配合系统变量判断上下文",
            "把空间判断结果写入后续任务的输入",
        ],
        "notes": ["打印、图签、目录任务经常因为空间误判而整体跑偏。"],
        "failures": ["ActiveLayout 已切但上下文未同步", "把布局块对象误当模型空间对象"],
        "verify": ["当前布局名与预期一致", "对象容器与任务类型一致"],
        "project_refs": ["cad/system/CAD_selection.py", "cad/system/CAD_core.py"],
        "keywords": ["space", "modelspace", "paperspace", "layout"],
    },
    {
        "slug": "enumerate_layouts",
        "folder": "02_space_and_layout",
        "title": "任务卡：枚举所有布局",
        "goal": "获取当前文档布局列表，供打印、目录、图签任务做分发。",
        "priority_path": [
            "优先使用 `CAD_core.get_layout_names()`",
            "打印场景也可参考 `print_area_analysis.get_layout_names()`",
        ],
        "symbols": ["Layouts", "Layout", "Document"],
        "steps": [
            "读取 `C.doc.Layouts`",
            "遍历并收集 `layout.Name`",
            "按任务需要决定是否排除 `Model`",
        ],
        "notes": ["COM 遍历顺序未必等于标签页顺序。"],
        "failures": ["布局枚举时 Busy", "布局名存在历史残留空白"],
        "verify": ["返回列表非空", "目标布局名可被命中"],
        "project_refs": ["cad/system/CAD_core.py", "cad/scripts/drawing_basic_service/print/print_area_analysis.py"],
        "keywords": ["list layouts", "enumerate layouts"],
    },
    {
        "slug": "switch_to_target_layout",
        "folder": "02_space_and_layout",
        "title": "任务卡：切换到指定布局",
        "goal": "稳定切换到目标布局，并为后续打印或图签扫描提供正确上下文。",
        "priority_path": [
            "优先使用 `CAD_core.switch_to_layout()`",
            "打印执行链内也可参考 `print_area_analysis.switch_to_layout()`",
            "COM 直切不稳时才走 `SendCommand` 兜底",
        ],
        "symbols": ["ActiveLayout", "Layouts", "Layout", "SendCommand"],
        "steps": [
            "若已在目标布局则直接返回",
            "通过 `Layouts.Item(name)` 取得布局对象",
            "写入 `Document.ActiveLayout`",
            "必要时走命令回退",
            "切换后再次读取布局名确认",
        ],
        "notes": ["这是打印和布局图签任务的高频核心步骤。"],
        "failures": ["RPC Busy", "布局不存在", "切换后状态未同步"],
        "verify": ["`C.doc.ActiveLayout.Name` 等于目标布局名"],
        "project_refs": ["cad/system/CAD_core.py", "cad/scripts/drawing_basic_service/print/print_area_analysis.py", "cad/system/CAD_coordination.py"],
        "keywords": ["switch layout", "activelayout", "sendcommand"],
    },
    {
        "slug": "build_selection_set",
        "folder": "03_selection",
        "title": "任务卡：构造选择集 / 选择对象",
        "goal": "在模型空间或布局空间里稳定构造选择集，用于后续对象扫描和统计。",
        "priority_path": [
            "优先复用 `CAD_selection.ss_select()`",
            "需要窗口选时优先复用 `select_entities_in_window()` 一类稳定函数",
        ],
        "symbols": ["SelectionSets", "SelectionSet", "Select", "SendCommand"],
        "steps": [
            "清理旧同名选择集",
            "新建 `SelectionSet`",
            "用窗口/交叉/过滤方式填充选择集",
            "把结果转换成后续逻辑可直接遍历的对象列表",
        ],
        "notes": ["选择逻辑应优先走 `CAD_selection.py`，不要到处手写。"],
        "failures": ["同名选择集残留", "窗口点坐标错误", "命令态阻塞"],
        "verify": ["返回对象数量符合预期"],
        "project_refs": ["cad/system/CAD_selection.py", "cad/system/CAD_core.py"],
        "keywords": ["selection set", "window select"],
    },
    {
        "slug": "traverse_objects_and_read_identity",
        "folder": "03_selection",
        "title": "任务卡：遍历对象并读取 ObjectName / Handle / Layer",
        "goal": "对选中的实体或空间内实体做基础类型识别与追踪标识读取。",
        "priority_path": [
            "优先先读 `ObjectName`",
            "再按需要读取 `Handle` 与 `Layer`",
            "高频统计逻辑优先参考打印分析链现有实现",
        ],
        "symbols": ["ObjectName", "Handle", "Layer", "SelectionSet"],
        "steps": [
            "遍历实体集合",
            "读取 `ObjectName` 作为首层类型判断",
            "按需要读取 `Handle` 与 `Layer`",
            "将结果标准化后输出",
        ],
        "notes": ["Handle 很有用，但批量读取会慢。"],
        "failures": ["天正对象属性访问兼容问题", "大批量句柄读取慢"],
        "verify": ["输出中包含稳定类型名和可追踪句柄"],
        "project_refs": ["cad/system/CAD_selection.py", "cad/scripts/drawing_basic_service/print/print_area_content_analysis.py", "cad/system/content_analysis_dwg_file.py"],
        "keywords": ["objectname", "handle", "layer", "traverse"],
    },
    {
        "slug": "get_bounding_box_and_object_counts",
        "folder": "03_selection",
        "title": "任务卡：获取边界框和对象统计",
        "goal": "为打印框识别、图签匹配和施工图统计准备基础几何与计数信息。",
        "priority_path": [
            "对象统计优先参考 `content_analysis_dwg_file.py`",
            "打印相关边界框匹配优先参考 `print_info_analysis.py`",
        ],
        "symbols": ["BoundingBox", "Coordinates", "ObjectName", "Handle"],
        "steps": [
            "获取目标对象集合",
            "读取边界框或坐标数组",
            "按对象类型做计数",
            "必要时采集句柄建立映射",
        ],
        "notes": ["打印框、多段线、角标块常依赖这一层。"],
        "failures": ["边界框返回不稳定", "对象类型统计口径不一致"],
        "verify": ["统计结果能回溯到具体对象或句柄"],
        "project_refs": ["cad/system/content_analysis_dwg_file.py", "cad/scripts/drawing_basic_service/print/print_info_analysis.py"],
        "keywords": ["bounding box", "count objects", "statistics"],
    },
    {
        "slug": "create_basic_geometry_smoke",
        "folder": "04_entities_create",
        "title": "任务卡：创建基础几何对象",
        "goal": "用最小几何创建验证 pywin32 调用链，并支撑施工图基础构造。",
        "priority_path": [
            "优先使用 `AddLine` 作为连接烟雾测试",
            "需要文本或多段线时再扩到 `AddText`、`AddMText`、`AddPolyline`",
        ],
        "symbols": ["ModelSpace", "AddLine", "AddPolyline", "AddText", "AddMText"],
        "steps": [
            "确定目标空间",
            "准备三维点或坐标数组",
            "调用创建方法",
            "必要时立即清理测试对象",
        ],
        "notes": ["不要在不了解当前空间时直接落实体创建。"],
        "failures": ["点格式错误", "对象插到错误空间"],
        "verify": ["对象创建成功并可再次读取"],
        "project_refs": ["cad/system/licad.py", "cad/scripts/Scheme_drawing/draw_building_outline.py", "cad/scripts/CAD_basic.py"],
        "keywords": ["addline", "addpolyline", "addtext", "smoke test"],
    },
    {
        "slug": "read_block_attributes",
        "folder": "05_blocks_and_attributes",
        "title": "任务卡：读取块属性",
        "goal": "从图签、角标或目录模板块中提取属性字段和值。",
        "priority_path": [
            "优先先判 `HasAttributes`",
            "属性读取优先参考 `print_info_analysis._extract_attribute_fields()`",
            "通用块属性读取也可参考 `CAD_basic.get_block_attributes_dict()`",
        ],
        "symbols": ["BlockReference", "HasAttributes", "GetAttributes", "AttributeReference"],
        "steps": [
            "定位块参照对象",
            "判断是否有属性",
            "遍历 `GetAttributes()`",
            "读取 `TagString` / `TextString` 并做文本清洗",
        ],
        "notes": ["图签字段常带格式控制前缀，需要清洗。"],
        "failures": ["块无属性", "属性值为空", "MText 样式前缀干扰"],
        "verify": ["返回字段字典包含图号/图名/项目名等关键标签"],
        "project_refs": ["cad/scripts/drawing_basic_service/print/print_info_analysis.py", "cad/scripts/CAD_basic.py"],
        "keywords": ["block attributes", "title block", "tagstring"],
    },
    {
        "slug": "insert_block_or_dwg",
        "folder": "05_blocks_and_attributes",
        "title": "任务卡：插入块或插入 DWG",
        "goal": "在模型空间或布局空间中插入图签、目录模板或外部 DWG。",
        "priority_path": [
            "普通插块可参考 `CAD_basic.insert_block_into_autocad()`",
            "需要跨文件插入并炸开时优先参考 `CAD_core.insert_file_exploded()`",
        ],
        "symbols": ["InsertBlock", "Block", "BlockReference", "ModelSpace", "PaperSpace"],
        "steps": [
            "确认目标空间和插入点",
            "校验路径存在",
            "调用 `InsertBlock`",
            "若后续需编辑实体，可再 Explode",
        ],
        "notes": ["图签和目录模板通常更接近块插入而非纯几何重建。"],
        "failures": ["INSBASE 偏移", "路径不存在", "插到错误布局"],
        "verify": ["插入后能读取到新的 `BlockReference`"],
        "project_refs": ["cad/system/CAD_core.py", "cad/scripts/CAD_basic.py"],
        "keywords": ["insert block", "insert dwg", "explode"],
    },
    {
        "slug": "update_titleblock_fields",
        "folder": "05_blocks_and_attributes",
        "title": "任务卡：更新图签属性字段",
        "goal": "把图名、图号、项目名或目录信息回写到图签属性中。",
        "priority_path": [
            "图名回写优先参考 `process_drawing_names_and_fill_titleblocks()`",
            "目录图签更新优先参考 `update_catalog_titleblocks_from_excel()`",
            "调试阶段可参考 `fill_block_attributes_with_tag_name()`",
        ],
        "symbols": ["BlockReference", "AttributeReference", "GetAttributes", "HasAttributes", "AddMText"],
        "steps": [
            "先定位目标图签块",
            "读取并识别目标属性标签",
            "按业务规则写入文本",
            "必要时同步目录或 Excel 数据源",
        ],
        "notes": ["这类任务主逻辑优先参考项目现有业务函数，而不是从 CHM 生写。"],
        "failures": ["图签模板版本不一致", "标签名不统一", "属性格式被覆盖"],
        "verify": ["回写后再次读取属性值一致"],
        "project_refs": ["cad/scripts/CAD_basic.py"],
        "keywords": ["title block", "fill attributes", "drawing name"],
    },
    {
        "slug": "manage_layers",
        "folder": "06_layers_and_styles",
        "title": "任务卡：读取 / 创建 / 切换图层",
        "goal": "为施工图对象创建、目录生成和图签整理提供图层控制能力。",
        "priority_path": [
            "先读 `Document.Layers`",
            "已有施工图创建逻辑可参考 `draw_building_outline.py`",
        ],
        "symbols": ["Layers", "Layer", "Document"],
        "steps": [
            "尝试 `Layers.Item(name)` 读取目标图层",
            "不存在时调用 `Layers.Add(name)`",
            "按需要设置当前活动图层或实体图层",
        ],
        "notes": ["不要在未知图层锁定/冻结状态下直接批量改写。"],
        "failures": ["目标图层不存在", "当前图层被冻结或锁定"],
        "verify": ["图层创建或切换后可再次读取"],
        "project_refs": ["cad/scripts/Scheme_drawing/draw_building_outline.py", "cad/scripts/CAD_basic.py"],
        "keywords": ["layers", "active layer"],
    },
    {
        "slug": "read_layout_plot_info",
        "folder": "07_plot_and_output",
        "title": "任务卡：读取布局打印信息",
        "goal": "读取布局对象的打印设备、纸张、窗口范围和相关图签信息。",
        "priority_path": [
            "优先看 `Layout` / `Plot` / `RefreshPlotDeviceInfo` / `SetWindowToPlot`",
            "业务层优先参考 `print_info_analysis.py` 和 `print_policy.py`",
        ],
        "symbols": ["Layout", "Plot", "RefreshPlotDeviceInfo", "SetWindowToPlot", "ActiveLayout"],
        "steps": [
            "取得目标布局对象",
            "刷新打印设备信息",
            "读取纸张、旋转、窗口或块快照信息",
            "结合图签信息形成后续打印计划输入",
        ],
        "notes": ["当前主线是打印执行链，不要把布局打印信息读取做成孤立脚本。"],
        "failures": ["设备信息未刷新", "布局对象读取不稳定", "打印框与角标匹配失败"],
        "verify": ["产出可用于打印计划的布局信息结构"],
        "project_refs": ["cad/scripts/drawing_basic_service/print/print_info_analysis.py", "cad/scripts/drawing_basic_service/print/print_policy.py", "cad/scripts/CAD_basic.py"],
        "keywords": ["plot info", "layout plot", "paper size"],
    },
    {
        "slug": "execute_layout_plot",
        "folder": "07_plot_and_output",
        "title": "任务卡：执行布局窗口打印",
        "goal": "按布局和窗口范围输出 PDF，并受运行监督链保护。",
        "priority_path": [
            "优先复用 `print_executor.execute_print_plan()`",
            "单任务布局输出优先参考 `export_layout_window_lisp_fit()`",
            "必要时参考 `CAD_basic` 的布局输出经验",
        ],
        "symbols": ["Plot", "Layout", "SetWindowToPlot", "RefreshPlotDeviceInfo", "SendCommand"],
        "steps": [
            "确认目标 DWG 和布局已就绪",
            "准备打印设备、纸张、CTB、方向和窗口点",
            "调用布局输出函数",
            "校验 PDF 是否生成成功",
        ],
        "notes": ["打印执行应在 runtime guard 保护下推进。"],
        "failures": ["布局准备失败", "输出文件被占用", "命令回退未完成"],
        "verify": ["PDF 文件存在且页尺寸符合预期"],
        "project_refs": ["cad/scripts/drawing_basic_service/print/print_executor.py", "cad/scripts/CAD_basic.py"],
        "keywords": ["plot to file", "pdf", "layout output"],
    },
    {
        "slug": "build_print_plan_and_info",
        "folder": "07_plot_and_output",
        "title": "任务卡：构建打印计划和打印信息",
        "goal": "把布局、打印框、角标块和输出参数组织成可执行的打印计划。",
        "priority_path": [
            "优先使用 `collect_print_jobs()` + `build_print_plan()`",
            "打印信息分析优先用 `analyze_print_info_jobs()`",
        ],
        "symbols": ["Layout", "Handle", "ObjectName", "GetAttributes", "Plot"],
        "steps": [
            "先收集布局与打印区域作业",
            "再分析角标块和属性字段",
            "按布局归并为打印计划",
            "交给打印执行层推进",
        ],
        "notes": ["这一步是打印主链的一部分，不应退化为单个 API 查询。"],
        "failures": ["打印框识别失败", "角标块匹配失败", "句柄映射不稳定"],
        "verify": ["生成的计划中包含布局、句柄、输出路径和方向"],
        "project_refs": ["cad/scripts/drawing_basic_service/print/print_policy.py", "cad/scripts/drawing_basic_service/print/print_info_analysis.py"],
        "keywords": ["print plan", "print info", "jobs"],
    },
    {
        "slug": "sendcommand_fallback",
        "folder": "08_command_fallback",
        "title": "任务卡：SendCommand 命令回退",
        "goal": "在 COM 直接调用不稳定时，安全地使用命令行回退完成布局切换、缩放、选择或打印补救。",
        "priority_path": [
            "优先用 `licad.SafeDocumentWrapper.SendCommand`",
            "需要同步等待时优先用 `CAD_coordination.send_cmd_with_sync()`",
        ],
        "symbols": ["SendCommand", "GetVariable", "SetVariable", "Document"],
        "steps": [
            "确认当前确实需要命令回退",
            "构造完整命令串并补换行",
            "发送命令并等待状态稳定",
            "回读关键状态确认命令生效",
        ],
        "notes": ["SendCommand 是保底，不是默认主路。"],
        "failures": ["命令串发到错误上下文", "命令仍在执行就继续发下一条", "系统变量状态不一致"],
        "verify": ["命令后关键状态读数符合预期"],
        "project_refs": ["cad/system/licad.py", "cad/system/CAD_coordination.py", "cad/system/CAD_selection.py", "cad/scripts/drawing_basic_service/print/print_executor.py"],
        "keywords": ["sendcommand", "fallback", "command line"],
    },
    {
        "slug": "insert_company_title_block",
        "folder": "09_misc_common_tasks",
        "title": "任务卡：插入公司通用图签",
        "goal": "向当前图纸插入公司通用图签，并获取后续属性处理所需的信息。",
        "priority_path": [
            "优先参考 `insert_company_label_common_block()`",
            "底层插入依然回到 `InsertBlock` / `insert_file_exploded()`",
        ],
        "symbols": ["InsertBlock", "BlockReference", "GetAttributes"],
        "steps": [
            "确认图签模板路径",
            "在目标空间插入图签块",
            "按需要炸开或保留块参照",
            "收集后续属性填充需要的对象和信息",
        ],
        "notes": ["图签服务是当前目标范围内的重要业务主题。"],
        "failures": ["模板路径失效", "插入后比例不对", "炸开后对象识别失败"],
        "verify": ["图签块或图签实体已在目标位置生成"],
        "project_refs": ["cad/scripts/CAD_basic.py", "cad/system/CAD_core.py"],
        "keywords": ["company label", "title block", "insert"],
    },
    {
        "slug": "generate_or_update_catalog",
        "folder": "09_misc_common_tasks",
        "title": "任务卡：生成目录或更新目录图签",
        "goal": "围绕 Excel 与图签模板，完成目录写入、目录图签更新和目录页自动化。",
        "priority_path": [
            "目录写入优先参考 `write_catalog_from_excel_to_cad()`",
            "目录图签更新优先参考 `update_catalog_titleblocks_from_excel()`",
            "旧版分步逻辑可参考 `bianmulu_func1_h` 到 `bianmulu_func4_h`",
        ],
        "symbols": ["AddText", "AddMText", "BlockReference", "GetAttributes", "InsertBlock"],
        "steps": [
            "读取 Excel 数据",
            "解析目录模板或目录图签块",
            "写入目录文本或更新目录图签属性",
            "校验行数、比例和页码映射",
        ],
        "notes": ["目录主题与当前业务目标直接相关，应保留高优先级入口。"],
        "failures": ["模板字段不一致", "目录行数超界", "比例字段计算错误"],
        "verify": ["目录页内容与 Excel 数据一致", "目录图签字段回读正确"],
        "project_refs": ["cad/scripts/CAD_basic.py"],
        "keywords": ["catalog", "table of contents", "excel", "title block"],
    },
    {
        "slug": "understand_and_convert_coordinate_systems",
        "folder": "10_3d_spatial_expression",
        "title": "任务卡：理解并转换坐标系",
        "goal": "在 `WCS / UCS / OCS / DCS` 之间稳定转换 3D 点和对象基准，为空间关系表达提供统一入口。",
        "priority_path": [
            "优先看 `TranslateCoordinates`、`ActiveUCS`、`GetUCSMatrix`、`Normal`、`Elevation*`",
            "项目内优先参考 `get_entity_full_info()` 与 `get_entity_geometry_info()` 的坐标读取逻辑",
            "涉及对象基准整体迁移时，再进入 `TransformBy`",
        ],
        "symbols": ["TranslateCoordinates", "ActiveUCS", "GetUCSMatrix", "Normal", "Elevation", "ElevationModelSpace", "ElevationPaperSpace", "UCS", "3d_point", "ocs_point", "normal_vector", "ucs_matrix"],
        "steps": [
            "先判断当前点或对象属于 `WCS / UCS / OCS / DCS` 中哪一种基准",
            "若是对象局部坐标，先读取 `Coordinates/Coordinate`，再补 `Elevation` 和 `Normal`",
            "用 `TranslateCoordinates` 把点转换到目标基准",
            "若任务需要整体变换对象，再取 `ActiveUCS/GetUCSMatrix` 进入矩阵链",
        ],
        "notes": ["这张卡服务施工图中的空间关系表达，不是泛化的坐标系教程。"],
        "failures": ["把 OCS 点直接当 WCS 点使用", "漏传 `OCSNormal`", "模型空间和图纸空间高程混淆", "当前 UCS 未保存导致 `ActiveUCS` 读取失败"],
        "verify": ["同一个点在目标坐标系下得到稳定结果", "对象 `Coordinates + Elevation + Normal` 能还原出可解释的 3D 点"],
        "project_refs": ["cad/scripts/CAD_basic.py", "cad/system/content_analysis_dwg_file.py", "cad/system/licad.py", "cad/system/CAD_core.py"],
        "keywords": ["coordinate systems", "translate coordinates", "wcs", "ucs", "ocs", "normal", "elevation"],
    },
    {
        "slug": "create_3d_path_or_profile",
        "folder": "10_3d_spatial_expression",
        "title": "任务卡：创建三维路径或轮廓",
        "goal": "用空间点、3D 路径和面表达轮廓骨架，为 Region、Solid 和剖切主链准备受控输入。",
        "priority_path": [
            "优先看 `Add3DPoly`、`3dPolyline`、`Add3DFace`、`3DFace`",
            "需要统一点数组时先看 `3d_point` 和 `point_array_rules.md`",
            "轮廓后续若要进区域/实体，先保证点序和共面关系明确",
        ],
        "symbols": ["Add3DPoly", "3dPolyline", "Add3DFace", "3DFace", "3d_point"],
        "steps": [
            "先确定路径或轮廓要表达的是轴线、轮廓骨架还是面",
            "统一点数组为三元素 3D 点",
            "路径类优先用 `Add3DPoly`，面类再用 `Add3DFace`",
            "把结果作为后续 Region/Solid/剖切任务的输入对象",
        ],
        "notes": ["这张卡强调的是服务空间关系表达的路径和轮廓，不是复杂造型。"],
        "failures": ["点数组元素数不是 3 的倍数", "轮廓顺序错误导致后续区域构造失败", "把二维轮廓直接误当空间路径"],
        "verify": ["返回对象可被识别为 `3dPolyline` 或 `3DFace`", "读取坐标序列时点序与预期一致"],
        "project_refs": ["cad/scripts/Scheme_drawing/draw_building_outline.py", "cad/scripts/CAD_basic.py", "cad/system/licad.py"],
        "keywords": ["3d path", "3d profile", "3dpolyline", "3dface", "points array"],
    },
    {
        "slug": "create_region_and_extrude_solid",
        "folder": "10_3d_spatial_expression",
        "title": "任务卡：创建 Region 并挤出 Solid",
        "goal": "把闭合轮廓转为 Region，并进一步生成基础 Solid，服务构件体量与剖切表达。",
        "priority_path": [
            "优先看 `AddRegion`、`Region`、`AddExtrudedSolid`、`AddExtrudedSolidAlongPath`、`AddRevolvedSolid`、`3DSolid`",
            "轮廓不闭合或不共面时，先在输入层修正，不要直接强推实体生成",
            "需要沿路径生成实体时，再引入路径对象",
        ],
        "symbols": ["AddRegion", "Region", "AddExtrudedSolid", "AddExtrudedSolidAlongPath", "AddRevolvedSolid", "3DSolid"],
        "steps": [
            "先确认轮廓对象是闭合且共面的",
            "调用 `AddRegion` 获取区域对象",
            "按任务需要选择普通挤出、沿路径挤出或旋转成体",
            "将生成的 `3DSolid` 交给空间对位或剖切任务继续推进",
        ],
        "notes": ["本卡服务施工图中的空间体量与剖切依据，不是为了扩展复杂 3D 造型。"],
        "failures": ["轮廓不闭合", "轮廓不共面", "挤出高度或锥角导致自相交", "路径与轮廓平面关系不正确"],
        "verify": ["能拿到 `Region` 或 `3DSolid` 返回对象", "生成结果可被包围盒和对象类型识别"],
        "project_refs": ["cad/system/CAD_core.py", "cad/scripts/CAD_basic.py", "cad/system/licad.py", "cad/system/content_analysis_dwg_file.py"],
        "keywords": ["region", "extrude solid", "revolved solid", "profile to solid"],
    },
    {
        "slug": "apply_3d_transform_to_objects",
        "folder": "10_3d_spatial_expression",
        "title": "任务卡：对对象应用三维变换",
        "goal": "通过平移、旋转、镜像、缩放和矩阵变换完成对象空间对位和方向修正。",
        "priority_path": [
            "优先看 `Move`、`Rotate3D`、`Mirror3D`、`ScaleEntity`",
            "需要统一做复杂变换时，再进入 `TransformBy` 和 `transform_matrix`",
            "若变换与 UCS 基准相关，先回到 `GetUCSMatrix`",
        ],
        "symbols": ["Move", "Rotate3D", "Mirror3D", "ScaleEntity", "TransformBy", "transform_matrix", "ucs_matrix"],
        "steps": [
            "先判断任务是位移、轴旋转、平面镜像、缩放还是矩阵统一变换",
            "准备轴线、平面、基点或 4x4 矩阵输入",
            "执行对应的变换方法",
            "回读对象位置或边界，确认空间关系没有跑偏",
        ],
        "notes": ["这张卡强调空间对位正确性，而不是造型动作本身。"],
        "failures": ["弧度和角度混淆", "轴线或平面定义退化", "矩阵格式非法", "在集合迭代中直接做写操作变换"],
        "verify": ["对象包围盒或关键点位按预期变化", "变换后对象仍能进入后续剖切或打印表达链"],
        "project_refs": ["cad/scripts/CAD_basic.py", "cad/system/CAD_core.py", "cad/system/licad.py"],
        "keywords": ["rotate3d", "mirror3d", "scaleentity", "transformby", "move", "alignment"],
    },
    {
        "slug": "section_3d_geometry_for_2d_expression",
        "folder": "10_3d_spatial_expression",
        "title": "任务卡：对三维几何做剖切并服务二维表达",
        "goal": "通过 `SectionSolid` 或区域边界提取，把三维空间关系转成二维施工图可用的剖切与边界依据。",
        "priority_path": [
            "优先看 `SectionSolid`、`Region`、`section_plane_definition`",
            "若只需要粗边界，再评估是否先读 `BoundingBox`，不要把包围盒直接等同于剖面轮廓",
            "二维表达落图前，先确认剖切结果的坐标基准",
        ],
        "symbols": ["SectionSolid", "Region", "3DSolid", "section_plane_definition", "BoundingBox"],
        "steps": [
            "先确认三维实体和剖切平面的三点定义",
            "调用 `SectionSolid` 获取剖切 Region",
            "读取返回区域的边界、面积、质心或爆炸后的环路",
            "把结果组织成可供二维施工图表达使用的几何参考",
        ],
        "notes": ["本卡是第四轮最直接体现“由三维关系支撑二维表达”的入口之一。"],
        "failures": ["剖切平面三点共线", "只读包围盒导致表达过粗", "剖切结果坐标基准未统一", "把实体编辑结果直接当二维表达输出"],
        "verify": ["能得到有效 Region 或稳定边界", "剖切结果可解释为二维剖面或轮廓参考"],
        "project_refs": ["cad/system/content_analysis_dwg_file.py", "cad/scripts/drawing_basic_service/print/print_area_content_analysis.py", "cad/scripts/CAD_basic.py", "cad/system/licad.py"],
        "keywords": ["section solid", "section plane", "2d expression", "region boundary", "section geometry"],
    },
    {
        "slug": "read_3d_object_spatial_identity",
        "folder": "10_3d_spatial_expression",
        "title": "任务卡：读取三维对象空间身份",
        "goal": "读取对象的坐标、高程、法向量、包围盒和类型身份，为空间关系分析和二维表达提供稳定输入。",
        "priority_path": [
            "优先看 `Coordinates`、`Normal`、`Elevation`、`BoundingBox`",
            "若对象来自局部坐标，先回到坐标系转换卡，不要直接解释原值",
            "需要做批量对象快照时，优先参考现有内容分析路径",
        ],
        "symbols": ["Coordinates", "Normal", "Elevation", "BoundingBox", "3dPolyline", "Region", "3DSolid"],
        "steps": [
            "先识别对象类型和所有者空间",
            "读取坐标序列、高程、法向量和包围盒",
            "必要时把局部坐标还原到 WCS",
            "把结果整理成可供后续剖切、打印或施工图表达使用的空间身份结构",
        ],
        "notes": ["本卡服务的是对象空间身份识别，而不是单纯的属性列举。"],
        "failures": ["把 OCS 坐标直接当全局坐标", "只看包围盒不看法向", "对象类型识别正确但空间基准解释错误"],
        "verify": ["能得到稳定的对象类型、坐标、法向和包围盒结果", "不同对象在同一基准下可比较空间关系"],
        "project_refs": ["cad/scripts/CAD_basic.py", "cad/system/content_analysis_dwg_file.py", "cad/scripts/drawing_basic_service/print/print_area_content_analysis.py", "cad/system/licad.py"],
        "keywords": ["spatial identity", "coordinates", "normal", "elevation", "bounding box", "3d object"],
    },
]


def load_json(path: Path) -> object:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def uniq(values: list[str]) -> list[str]:
    result = []
    seen = set()
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def task_id_for(index: int) -> str:
    return f"CAD2021-TASK-{index:03d}"


def list_lines(items: list[str], *, code: bool = False) -> list[str]:
    return [f"- `{item}`" if code else f"- {item}" for item in items]


def implementation_lines(items: list[dict[str, str]]) -> list[str]:
    return [f"- `{item['project_function']}` -> `{item['module_path']}`" for item in items]


def load_core_meta_index() -> dict[str, dict[str, object]]:
    result = {}
    for meta_path in CORE_DIR.rglob("*.meta.json"):
        payload = load_json(meta_path)
        if isinstance(payload, dict) and payload.get("symbol"):
            result[str(payload["symbol"])] = payload
    return result


def load_previous_task_map() -> dict[str, dict[str, object]]:
    payload = load_json(TASK_MAP_PATH)
    if not isinstance(payload, dict):
        return {}
    return {key: value for key, value in payload.items() if isinstance(value, dict)}


def previous_task_by_slug(previous_map: dict[str, dict[str, object]], slug: str) -> dict[str, object]:
    for payload in previous_map.values():
        if payload.get("slug") == slug:
            return payload
    return {}


def infer_stability_level(module_paths: list[str]) -> str:
    joined = " ".join(module_paths)
    if "cad/system/licad.py" in joined or "cad/system/CAD_core.py" in joined:
        return "high"
    if "drawing_basic_service/print" in joined:
        return "medium"
    return "medium"


def build_task_payload(
    task: dict[str, object],
    index: int,
    rel_path: str,
    *,
    core_meta_index: dict[str, dict[str, object]],
    topic_path_map: dict[str, str],
    previous_map: dict[str, dict[str, object]],
) -> dict[str, object]:
    exact = TASK_EXACT_ENTRIES[task["slug"]]
    previous_payload = previous_task_by_slug(previous_map, str(task["slug"]))
    implementations = list(exact["implementation_entries"])
    previous_implementations = previous_payload.get("implementation_entries", []) if isinstance(previous_payload, dict) else []
    if isinstance(previous_implementations, list):
        implementations.extend(item for item in previous_implementations if isinstance(item, dict))
    deduped_implementations = []
    seen_impl = set()
    for item in implementations:
        key = (item["project_function"], item["module_path"])
        if key not in seen_impl:
            deduped_implementations.append(item)
            seen_impl.add(key)

    symbols = uniq(list(task["symbols"]))
    symbol_metas = [core_meta_index[symbol] for symbol in symbols if symbol in core_meta_index]
    symbol_rule_refs = []
    symbol_project_refs = []
    source_topic_ids = []
    source_html_paths = []
    for meta in symbol_metas:
        symbol_rule_refs.extend(meta.get("rule_refs", []))
        symbol_project_refs.extend(meta.get("project_refs", []))
        source_topic_ids.extend(meta.get("source_topic_ids", []))
        source_html_paths.extend(meta.get("source_html_paths", []))

    for topic_id in source_topic_ids:
        if topic_id in topic_path_map:
            source_html_paths.append(topic_path_map[topic_id])

    previous_project_refs = previous_payload.get("project_refs", []) if isinstance(previous_payload, dict) else []
    previous_rule_refs = previous_payload.get("rule_refs", []) if isinstance(previous_payload, dict) else []
    previous_source_ids = previous_payload.get("source_topic_ids", []) if isinstance(previous_payload, dict) else []
    previous_source_paths = previous_payload.get("source_html_paths", []) if isinstance(previous_payload, dict) else []

    project_refs = uniq(
        list(task["project_refs"])
        + [item["module_path"] for item in deduped_implementations]
        + symbol_project_refs
        + (previous_project_refs if isinstance(previous_project_refs, list) else [])
    )
    rule_refs = uniq(
        list(exact["pywin32_rules"])
        + symbol_rule_refs
        + (previous_rule_refs if isinstance(previous_rule_refs, list) else [])
    )
    source_topic_ids = uniq(source_topic_ids + (previous_source_ids if isinstance(previous_source_ids, list) else []))
    source_html_paths = uniq(source_html_paths + (previous_source_paths if isinstance(previous_source_paths, list) else []))
    reference_dwgs = uniq(
        list(exact["reference_dwgs"])
        + (previous_payload.get("reference_dwgs", []) if isinstance(previous_payload.get("reference_dwgs", []), list) else [])
    )
    return {
        "task_id": task_id_for(index),
        "slug": task["slug"],
        "title": task["title"],
        "path": rel_path,
        "goal": task["goal"],
        "priority_path": task["priority_path"],
        "symbols": symbols,
        "owners": uniq(list(exact["owners"])),
        "project_functions": uniq([item["project_function"] for item in deduped_implementations]),
        "module_paths": uniq([item["module_path"] for item in deduped_implementations]),
        "implementation_entries": deduped_implementations,
        "aliases_en": uniq(list(exact["aliases_en"])),
        "aliases_zh": uniq(list(exact["aliases_zh"])),
        "keywords_zh": uniq(list(exact["keywords_zh"])),
        "steps": task["steps"],
        "notes": task["notes"],
        "failures": task["failures"],
        "verify": task["verify"],
        "project_refs": project_refs,
        "keywords": task["keywords"],
        "pywin32_rules": uniq(list(exact["pywin32_rules"])),
        "rule_refs": rule_refs,
        "source_topic_ids": source_topic_ids,
        "source_html_paths": source_html_paths,
        "reference_dwgs": reference_dwgs,
        "reference_objects": uniq(list(exact["reference_objects"])),
        "stability_level": infer_stability_level(uniq([item["module_path"] for item in deduped_implementations])),
    }


def render_task(payload: dict[str, object]) -> str:
    lines = [
        f"# {payload['title']}",
        "",
        "## Exact Entry",
        f"- task_id: `{payload['task_id']}`",
        "- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`",
        "- symbols:",
        *list_lines(payload["symbols"], code=True),
        "- owners:",
        *list_lines(payload["owners"], code=True),
        "- implementation_entries:",
        *implementation_lines(payload["implementation_entries"]),
        "",
        "## Natural Language Expansion",
        "- aliases_en:",
        *list_lines(payload["aliases_en"], code=True),
        "- aliases_zh_support:",
        *list_lines(payload["aliases_zh"], code=True),
        "- keywords_zh_support:",
        *list_lines(payload["keywords_zh"], code=True),
        "",
        "## Goal",
        str(payload["goal"]),
        "",
        "## Priority Path",
    ]
    lines.extend(f"1. {item}" if idx == 0 else f"{idx + 1}. {item}" for idx, item in enumerate(payload["priority_path"]))
    lines.extend(["", "## Related Core Symbols"])
    lines.extend(list_lines(payload["symbols"], code=True))
    lines.extend(["", "## Workflow"])
    lines.extend(f"1. {item}" if idx == 0 else f"{idx + 1}. {item}" for idx, item in enumerate(payload["steps"]))
    lines.extend(["", "## Project Notes"])
    lines.extend(list_lines(payload["notes"]))
    lines.extend(["", "## Common Failures"])
    lines.extend(list_lines(payload["failures"]))
    lines.extend(["", "## Verification"])
    lines.extend(list_lines(payload["verify"]))
    lines.extend(["", "## Project Paths"])
    lines.extend(list_lines(payload["project_refs"], code=True))
    lines.extend(["", "## Pywin32 Rules"])
    lines.extend(list_lines(payload["pywin32_rules"], code=True))
    lines.extend(["", "## Aggregated Rule Refs"])
    lines.extend(list_lines(payload["rule_refs"], code=True))
    lines.extend(["", "## Source Trace", "- source_topic_ids:"])
    lines.extend(list_lines(payload["source_topic_ids"], code=True))
    lines.extend(["- source_html_paths:"])
    lines.extend(list_lines(payload["source_html_paths"], code=True))
    lines.extend(["", "## Stability", f"- stability_level: `{payload['stability_level']}`"])
    lines.extend(["", "## Reference DWG And Objects", "- reference_dwgs:"])
    lines.extend(list_lines(payload["reference_dwgs"], code=True))
    lines.extend(["- reference_objects:"])
    lines.extend(list_lines(payload["reference_objects"], code=True))
    return "\n".join(lines) + "\n"


def main() -> None:
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    core_meta_index = load_core_meta_index()
    topic_path_map = load_json(TOPIC_PATH_MAP_PATH)
    previous_map = load_previous_task_map()
    task_index = {
        "schema_version": TASK_INDEX_SCHEMA_VERSION,
        "primary_fields": ["task_id", "symbols", "owners", "project_functions", "module_paths"],
        "natural_language_primary": ["aliases_en"],
        "natural_language_support": ["aliases_zh", "keywords_zh"],
        "success_criteria": "Codex can move from task lookup to stable project implementation paths without treating Chinese retrieval as the main success metric.",
        "tasks": [],
    }
    task_map = {}
    for idx, task in enumerate(TASKS, start=1):
        folder = TASK_DIR / task["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{task['slug']}.md"
        rel_path = str(path.relative_to(ROOT)).replace("\\", "/")
        payload = build_task_payload(
            task,
            idx,
            rel_path,
            core_meta_index=core_meta_index,
            topic_path_map=topic_path_map if isinstance(topic_path_map, dict) else {},
            previous_map=previous_map,
        )
        path.write_text(render_task(payload), encoding="utf-8", newline="\n")
        task_index["tasks"].append(payload)
        task_map[payload["task_id"]] = {
            "slug": payload["slug"],
            "title": payload["title"],
            "path": payload["path"],
            "symbols": payload["symbols"],
            "owners": payload["owners"],
            "project_functions": payload["project_functions"],
            "module_paths": payload["module_paths"],
            "implementation_entries": payload["implementation_entries"],
            "aliases_en": payload["aliases_en"],
            "aliases_zh": payload["aliases_zh"],
            "keywords_zh": payload["keywords_zh"],
            "pywin32_rules": payload["pywin32_rules"],
            "project_refs": payload["project_refs"],
            "rule_refs": payload["rule_refs"],
            "source_topic_ids": payload["source_topic_ids"],
            "source_html_paths": payload["source_html_paths"],
            "reference_dwgs": payload["reference_dwgs"],
            "reference_objects": payload["reference_objects"],
            "stability_level": payload["stability_level"],
        }

    task_index_path = TASK_DIR / "task_index.json"
    task_index_path.write_text(json.dumps(task_index, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    map_path = VALIDATION_DIR / "task_to_existing_code_map.json"
    map_path.write_text(json.dumps(task_map, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(f"Generated {len(TASKS)} task cards.")
    print(f"Wrote {task_index_path}")
    print(f"Wrote {map_path}")


if __name__ == "__main__":
    main()
