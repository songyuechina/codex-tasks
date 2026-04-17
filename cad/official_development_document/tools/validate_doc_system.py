from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = ROOT.parent.parent
TASK_INDEX_PATH = ROOT / "04_task_cards" / "task_index.json"
TASK_MAP_PATH = ROOT / "07_validation" / "task_to_existing_code_map.json"
TOPIC_PATH_MAP_PATH = ROOT / "06_on_demand_index" / "topic_path_map.json"
MANIFEST_PATH = ROOT / "02_manifest" / "page_manifest.jsonl"
PROMOTION_POLICY_PATH = ROOT / "00_readme" / "PROMOTION_POLICY.md"
USAGE_FEEDBACK_PATH = ROOT / "07_validation" / "usage_feedback.jsonl"
HOTSPOT_CANDIDATES_PATH = ROOT / "07_validation" / "hotspot_candidates.json"
PROMOTION_LOG_PATH = ROOT / "07_validation" / "promotion_log.md"
AGENTS_PATH = ROOT / "AGENTS.md"
FOURTH_ROUND_TASK_DIR = ROOT / "04_task_cards" / "10_3d_spatial_expression"
REQUIRED_3D_RULES = [
    "05_pywin32_bridge/coordinate_system_rules.md",
    "05_pywin32_bridge/3d_transform_rules.md",
    "05_pywin32_bridge/3d_entity_creation_rules.md",
    "05_pywin32_bridge/section_region_rules.md",
]
REQUIRED_3D_TASK_SLUGS = {
    "understand_and_convert_coordinate_systems",
    "create_3d_path_or_profile",
    "create_region_and_extrude_solid",
    "apply_3d_transform_to_objects",
    "section_3d_geometry_for_2d_expression",
    "read_3d_object_spatial_identity",
}
REQUIRED_3D_CORE_SYMBOLS = {
    "UCS",
    "3dPolyline",
    "3DFace",
    "3DSolid",
    "Region",
    "TranslateCoordinates",
    "GetUCSMatrix",
    "Add3DPoly",
    "Add3DFace",
    "AddRegion",
    "AddExtrudedSolid",
    "AddExtrudedSolidAlongPath",
    "AddRevolvedSolid",
    "SectionSolid",
    "Rotate3D",
    "Mirror3D",
    "ScaleEntity",
    "TransformBy",
    "ActiveUCS",
    "Normal",
    "Elevation",
    "ElevationModelSpace",
    "ElevationPaperSpace",
    "ucs_matrix",
    "ocs_point",
    "normal_vector",
    "transform_matrix",
    "section_plane_definition",
}


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name} line {line_number} is not valid JSON: {exc}") from exc
    return rows


def resolve_rel(rel_path: str) -> Path | None:
    if not rel_path:
        return None
    doc_path = ROOT / rel_path
    if doc_path.exists():
        return doc_path
    workspace_path = WORKSPACE_ROOT / rel_path
    if workspace_path.exists():
        return workspace_path
    return None


def rel_exists(rel_path: str) -> bool:
    return resolve_rel(rel_path) is not None


def core_meta_index() -> dict[str, dict[str, Any]]:
    result = {}
    for meta_path in (ROOT / "03_core_symbols").rglob("*.meta.json"):
        payload = load_json(meta_path)
        if isinstance(payload, dict) and payload.get("symbol"):
            result[str(payload["symbol"])] = payload
    return result


def function_exists(module_rel: str, function_name: str) -> bool:
    module_path = resolve_rel(module_rel)
    if module_path is None:
        return False
    text = module_path.read_text(encoding="utf-8", errors="ignore")
    patterns = [
        rf"^\s*def\s+{re.escape(function_name)}\s*\(",
        rf"^\s*class\s+{re.escape(function_name)}\b",
        rf"\b{re.escape(function_name)}\b",
    ]
    return any(re.search(pattern, text, flags=re.MULTILINE) for pattern in patterns)


def validate_usage_feedback(
    rows: list[dict[str, Any]],
    fatal: list[str],
    warning: list[str],
    core_index: dict[str, dict[str, Any]],
    hotspot_symbols: set[str],
) -> set[str]:
    required_fields = {
        "date",
        "task_id",
        "queried_symbols",
        "fallback_to_raw_html",
        "missing_info",
        "blocker_level",
        "promotion_candidates",
    }
    refs: set[str] = set()
    for row in rows:
        missing = sorted(field for field in required_fields if field not in row)
        if missing:
            fatal.append(f"usage_feedback row missing fields: {', '.join(missing)}")
            continue
        if not isinstance(row.get("queried_symbols"), list):
            fatal.append(f"usage_feedback {row.get('task_id')} queried_symbols must be a list")
        if not isinstance(row.get("missing_info"), list):
            fatal.append(f"usage_feedback {row.get('task_id')} missing_info must be a list")
        if not isinstance(row.get("promotion_candidates"), list):
            fatal.append(f"usage_feedback {row.get('task_id')} promotion_candidates must be a list")
        refs.add(f"07_validation/usage_feedback.jsonl#{row.get('date')}-{row.get('task_id')}")
        for symbol in row.get("promotion_candidates", []):
            if symbol not in core_index and symbol not in hotspot_symbols:
                warning.append(
                    f"usage_feedback {row.get('task_id')} promotion_candidate not in core/hotspot: {symbol}"
                )
    return refs


def validate_hotspot_candidates(
    payload: dict[str, Any],
    fatal: list[str],
    warning: list[str],
    core_index: dict[str, dict[str, Any]],
) -> set[str]:
    items = payload.get("items", []) if isinstance(payload, dict) else []
    if not isinstance(items, list):
        fatal.append("hotspot_candidates.json items is not a list")
        return set()
    symbols = set()
    for item in items:
        if not isinstance(item, dict):
            fatal.append("hotspot_candidates.json contains non-dict item")
            continue
        missing = [field for field in ("symbol", "current_level", "suggested_action") if not item.get(field)]
        if missing:
            fatal.append(
                "hotspot_candidates item missing fields: "
                + ", ".join(missing)
            )
            continue
        symbol = str(item.get("symbol", ""))
        symbols.add(symbol)
        state = str(item.get("state", "candidate"))
        if state == "promoted" and symbol not in core_index:
            fatal.append(f"hotspot promoted item missing core symbol: {symbol}")
        if state == "candidate" and item.get("current_level") == "core":
            warning.append(f"hotspot candidate {symbol} has current_level=core")
    return symbols


def validate_uncommon_topics(
    rows: list[dict[str, Any]],
    fatal: list[str],
    warning: list[str],
    core_index: dict[str, dict[str, Any]],
    hotspot_symbols: set[str],
) -> tuple[int, int]:
    promoted_count = 0
    candidate_count = 0
    allowed_status = {"archive", "hotspot_candidate", "promoted_to_core", ""}
    for row in rows:
        status = str(row.get("status", ""))
        if status not in allowed_status:
            warning.append(f"uncommon topic has unexpected status {status}: {row.get('topic_id')}")
        if status == "promoted_to_core":
            promoted_count += 1
            promoted_symbol = str(row.get("promoted_symbol", ""))
            if not promoted_symbol:
                fatal.append(f"promoted_to_core topic missing promoted_symbol: {row.get('topic_id')}")
            elif promoted_symbol not in core_index:
                fatal.append(f"promoted_to_core topic references missing core symbol: {promoted_symbol}")
        if status == "hotspot_candidate":
            candidate_count += 1
            candidate_symbol = str(row.get("candidate_symbol", ""))
            if candidate_symbol and candidate_symbol not in hotspot_symbols:
                warning.append(
                    f"hotspot_candidate uncommon topic not present in hotspot_candidates.json: {candidate_symbol}"
                )
    return promoted_count, candidate_count


def main() -> None:
    fatal: list[str] = []
    warning: list[str] = []
    gap: list[str] = []

    for required_file in (
        PROMOTION_POLICY_PATH,
        USAGE_FEEDBACK_PATH,
        HOTSPOT_CANDIDATES_PATH,
        PROMOTION_LOG_PATH,
        AGENTS_PATH,
    ):
        if not required_file.exists():
            fatal.append(f"required file missing: {required_file.relative_to(ROOT)}")
    for rel_path in REQUIRED_3D_RULES:
        if not rel_exists(rel_path):
            fatal.append(f"required fourth-round 3d rule missing: {rel_path}")
    if not FOURTH_ROUND_TASK_DIR.exists():
        fatal.append("required fourth-round task group missing: 04_task_cards/10_3d_spatial_expression")

    task_index = load_json(TASK_INDEX_PATH)
    task_map = load_json(TASK_MAP_PATH)
    topic_map = load_json(TOPIC_PATH_MAP_PATH)
    manifest_rows = load_jsonl(MANIFEST_PATH)
    uncommon_rows = load_jsonl(ROOT / "06_on_demand_index" / "uncommon_topics.jsonl")
    manifest_topic_ids = {str(row.get("topic_id", "")) for row in manifest_rows if row.get("topic_id")}
    core_index = core_meta_index()

    hotspot_payload = load_json(HOTSPOT_CANDIDATES_PATH)
    hotspot_symbols = validate_hotspot_candidates(hotspot_payload, fatal, warning, core_index)
    usage_feedback_rows = load_jsonl(USAGE_FEEDBACK_PATH)
    feedback_refs = validate_usage_feedback(usage_feedback_rows, fatal, warning, core_index, hotspot_symbols)
    promoted_count, candidate_count = validate_uncommon_topics(
        uncommon_rows,
        fatal,
        warning,
        core_index,
        hotspot_symbols,
    )

    tasks = task_index.get("tasks", []) if isinstance(task_index, dict) else []
    if not isinstance(tasks, list):
        fatal.append("task_index.json tasks is not a list")
        tasks = []

    task_ids = {str(task.get("task_id", "")) for task in tasks if isinstance(task, dict)}
    task_slugs = {str(task.get("slug", "")) for task in tasks if isinstance(task, dict)}
    required_fields = {"task_id", "slug", "path", "symbols", "owners", "project_functions", "module_paths", "aliases_en"}

    for task in tasks:
        if not isinstance(task, dict):
            fatal.append("task_index contains non-dict task payload")
            continue
        missing = sorted(field for field in required_fields if not task.get(field))
        if missing:
            fatal.append(f"{task.get('task_id', '<unknown>')} missing fields: {', '.join(missing)}")
            continue

        task_path = resolve_rel(str(task["path"]))
        if task_path is None:
            fatal.append(f"{task['task_id']} task card missing: {task['path']}")
        else:
            text = task_path.read_text(encoding="utf-8", errors="ignore")
            if str(task["task_id"]) not in text:
                warning.append(f"{task['task_id']} markdown missing inline task_id marker")

        for field in ["module_paths", "project_refs", "rule_refs", "reference_dwgs", "source_html_paths"]:
            for rel_path in task.get(field, []):
                if not rel_exists(str(rel_path)):
                    fatal.append(f"{task['task_id']} missing path in {field}: {rel_path}")

        for symbol in task.get("symbols", []):
            if symbol not in core_index:
                if symbol in hotspot_symbols:
                    warning.append(f"{task['task_id']} references hotspot candidate symbol not yet in core: {symbol}")
                else:
                    fatal.append(f"{task['task_id']} references missing core symbol: {symbol}")

        implementation_entries = task.get("implementation_entries", [])
        if isinstance(implementation_entries, list):
            for entry in implementation_entries:
                if not isinstance(entry, dict):
                    continue
                module_path = str(entry.get("module_path", ""))
                function_name = str(entry.get("project_function", ""))
                if not rel_exists(module_path):
                    fatal.append(f"{task['task_id']} implementation module missing: {module_path}")
                elif function_name and not function_exists(module_path, function_name):
                    fatal.append(f"{task['task_id']} function not found: {function_name} in {module_path}")

        for topic_id in task.get("source_topic_ids", []):
            if topic_id not in manifest_topic_ids and topic_id not in topic_map:
                warning.append(f"{task['task_id']} unresolved source_topic_id: {topic_id}")

        if "promotion_watch_symbols" in task and not isinstance(task.get("promotion_watch_symbols"), list):
            fatal.append(f"{task['task_id']} promotion_watch_symbols must be a list")
        if "high_risk_missing_info" in task and not isinstance(task.get("high_risk_missing_info"), list):
            fatal.append(f"{task['task_id']} high_risk_missing_info must be a list")
        if "usage_feedback_refs" in task:
            refs = task.get("usage_feedback_refs")
            if not isinstance(refs, list):
                fatal.append(f"{task['task_id']} usage_feedback_refs must be a list")
            else:
                for ref in refs:
                    if ref not in feedback_refs:
                        warning.append(f"{task['task_id']} usage_feedback_ref not found: {ref}")

    missing_3d_task_slugs = sorted(REQUIRED_3D_TASK_SLUGS - task_slugs)
    if missing_3d_task_slugs:
        fatal.append(
            "missing fourth-round 3d task slugs: " + ", ".join(missing_3d_task_slugs)
        )

    if isinstance(task_map, dict):
        for task_id, payload in task_map.items():
            if task_id not in task_ids:
                fatal.append(f"task_to_existing_code_map has unknown task_id: {task_id}")
            if isinstance(payload, dict) and payload.get("path") and not rel_exists(str(payload["path"])):
                fatal.append(f"task map path missing for {task_id}: {payload['path']}")

    for symbol, meta in core_index.items():
        path_md = str(meta.get("path_md", ""))
        if not rel_exists(path_md):
            fatal.append(f"core symbol markdown missing for {symbol}: {path_md}")
        for rel_path in meta.get("project_refs", []):
            if not rel_exists(str(rel_path)):
                fatal.append(f"{symbol} missing project_ref path: {rel_path}")
        for rel_path in meta.get("rule_refs", []):
            if not rel_exists(str(rel_path)):
                fatal.append(f"{symbol} missing rule_ref path: {rel_path}")
        for rel_path in meta.get("source_html_paths", []):
            if not rel_exists(str(rel_path)):
                fatal.append(f"{symbol} missing source_html_path: {rel_path}")
        for topic_id in meta.get("source_topic_ids", []):
            if topic_id not in manifest_topic_ids and topic_id not in topic_map:
                warning.append(f"{symbol} unresolved source_topic_id: {topic_id}")
        for related_task in meta.get("related_tasks", []):
            if related_task not in task_ids and related_task not in task_slugs:
                warning.append(f"{symbol} related_task not found: {related_task}")

    missing_3d_core_symbols = sorted(REQUIRED_3D_CORE_SYMBOLS - set(core_index.keys()))
    if missing_3d_core_symbols:
        fatal.append(
            "missing fourth-round 3d core symbols: " + ", ".join(missing_3d_core_symbols)
        )

    system_variable_count = sum(1 for meta in core_index.values() if meta.get("kind") == "system_variable")
    type_topic_count = sum(1 for meta in core_index.values() if meta.get("kind") == "type_topic")
    task_referenced_missing = sorted(
        {
            symbol
            for task in tasks
            if isinstance(task, dict)
            for symbol in task.get("symbols", [])
            if symbol not in core_index and symbol not in hotspot_symbols
        }
    )

    checks = {
        "manifest_pages": len(manifest_rows),
        "core_symbol_cards": sum(1 for _ in (ROOT / "03_core_symbols").rglob("*.md")),
        "task_cards": sum(1 for _ in (ROOT / "04_task_cards").rglob("*.md")),
        "bridge_docs": sum(1 for _ in (ROOT / "05_pywin32_bridge").rglob("*.md")),
        "task_index_entries": len(tasks),
        "system_variables": system_variable_count,
        "types_and_variants": type_topic_count,
        "usage_feedback_entries": len(usage_feedback_rows),
        "hotspot_candidate_items": len(load_json(HOTSPOT_CANDIDATES_PATH).get("items", [])),
        "on_demand_promoted_to_core": promoted_count,
        "on_demand_hotspot_candidates": candidate_count,
        "task_referenced_symbols_missing_from_core": task_referenced_missing,
        "fourth_round_3d_task_cards_present": not missing_3d_task_slugs,
        "fourth_round_3d_core_symbols_present": not missing_3d_core_symbols,
        "fourth_round_3d_rule_docs_present": all(rel_exists(path) for path in REQUIRED_3D_RULES),
    }

    if system_variable_count == 0:
        fatal.append("system_variables still empty")
    if type_topic_count == 0:
        fatal.append("types_and_variants still empty")
    if not core_index:
        fatal.append("no core symbol meta found")

    print(json.dumps(checks, ensure_ascii=False, indent=2))
    if fatal:
        print("Fatal:")
        for item in fatal:
            print(f"- {item}")
    if warning:
        print("Warning:")
        for item in warning:
            print(f"- {item}")
    if gap:
        print("Gap:")
        for item in gap:
            print(f"- {item}")

    if fatal:
        raise SystemExit(1)
    print("Validation passed.")


if __name__ == "__main__":
    main()
