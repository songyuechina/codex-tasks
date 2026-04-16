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
    keywords = ["layout", "plot", "block", "attribute", "selection", "text", "layer", "variable", "variant", "collection", "point", "bounding", "catalog"]
    for record in manifest_rows + value_rows:
        title = str(record.get("title", ""))
        score = int(record.get("project_score", 0)) * 10
        why: list[str] = []
        if any(token in title.lower() for token in keywords):
            score += 25
            why.append("project keyword")
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
    print(f"Updated existing core metas and ensured {len(NEW_SYMBOL_SPECS)} second-round symbol cards.")
    print(f"Wrote {CANDIDATE_PATH}")


if __name__ == "__main__":
    main()
