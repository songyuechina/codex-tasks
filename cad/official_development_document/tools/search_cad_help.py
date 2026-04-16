from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
TASK_INDEX_PATH = ROOT / "04_task_cards" / "task_index.json"
ALIAS_MAP_PATH = ROOT / "02_manifest" / "alias_map.json"
HOTSPOT_CANDIDATES_PATH = ROOT / "07_validation" / "hotspot_candidates.json"
MANIFEST_PATH = ROOT / "02_manifest" / "page_manifest.jsonl"


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip()).lower()


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_./-]+", normalize(text))


def load_task_index() -> list[dict[str, Any]]:
    payload = load_json(TASK_INDEX_PATH)
    tasks = payload.get("tasks", []) if isinstance(payload, dict) else []
    return [task for task in tasks if isinstance(task, dict)]


def load_alias_map() -> dict[str, dict[str, list[str]]]:
    payload = load_json(ALIAS_MAP_PATH)
    return payload if isinstance(payload, dict) else {}


def load_hotspot_candidates() -> list[dict[str, Any]]:
    payload = load_json(HOTSPOT_CANDIDATES_PATH)
    items = payload.get("items", []) if isinstance(payload, dict) else []
    return [item for item in items if isinstance(item, dict)]


def hotspot_lookup() -> dict[str, dict[str, Any]]:
    return {
        normalize(str(item.get("symbol", ""))): item
        for item in load_hotspot_candidates()
        if item.get("symbol")
    }


def expand_query(query: str) -> list[str]:
    alias_map = load_alias_map()
    base = normalize(query)
    variants = {base}
    variants.update(tokens(base))
    for key, groups in alias_map.items():
        aliases = []
        for field in ("aliases_en", "aliases_zh", "keywords_zh"):
            aliases.extend(normalize(item) for item in groups.get(field, []))
        if base == normalize(key) or any(alias and alias in base for alias in aliases):
            variants.add(normalize(key))
            variants.update(normalize(item) for item in groups.get("aliases_en", []))
    return sorted(item for item in variants if item)


def score_list(query: str, values: list[str], *, exact: int, prefix: int, contains: int) -> int:
    q = normalize(query)
    best = 0
    for value in values:
        current = normalize(value)
        if not current:
            continue
        if current == q:
            best = max(best, exact)
        elif current.startswith(q) or q.startswith(current):
            best = max(best, prefix)
        elif q in current or current in q:
            best = max(best, contains)
    return best


def score_text(variants: list[str], *fields: str) -> int:
    corpus = " ".join(normalize(field) for field in fields if field)
    score = 0
    for variant in variants:
        if variant in corpus:
            score += 10
        for token in tokens(variant):
            if token in corpus:
                score += 3
    return score


def unique(seq: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in seq:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def build_hit(
    *,
    score: int,
    title: str,
    path: str,
    task_id: str,
    reasons: list[str],
    sources: list[str],
    project_functions: list[str] | None = None,
    module_paths: list[str] | None = None,
    hotspot_item: dict[str, Any] | None = None,
) -> dict[str, Any]:
    hit = {
        "score": score,
        "title": title,
        "path": path,
        "task_id": task_id,
        "reasons": unique(reasons),
        "sources": unique(sources),
        "project_functions": project_functions or [],
        "module_paths": module_paths or [],
    }
    if hotspot_item:
        hit["hotspot"] = {
            "symbol": str(hotspot_item.get("symbol", "")),
            "state": str(hotspot_item.get("state", "")),
            "suggested_action": str(hotspot_item.get("suggested_action", "")),
            "reason": str(hotspot_item.get("reason", "")),
        }
    return hit


def attach_hotspot(hit: dict[str, Any], names: list[str]) -> dict[str, Any]:
    lookup = hotspot_lookup()
    matched = None
    for name in names:
        key = normalize(name)
        if key and key in lookup:
            matched = lookup[key]
            break
    if not matched:
        return hit
    hit["hotspot"] = {
        "symbol": str(matched.get("symbol", "")),
        "state": str(matched.get("state", "")),
        "suggested_action": str(matched.get("suggested_action", "")),
        "reason": str(matched.get("reason", "")),
    }
    if str(matched.get("state", "")) == "candidate":
        hit["sources"] = unique(hit.get("sources", []) + ["from_hotspot_candidate"])
    return hit


def merge_hits(*groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[tuple[str, str, str], dict[str, Any]] = {}
    for group in groups:
        for item in group:
            key = (item.get("title", ""), item.get("path", ""), item.get("task_id", ""))
            existing = merged.get(key)
            if existing is None:
                merged[key] = item
                continue
            existing["score"] = max(existing["score"], item["score"])
            existing["reasons"] = unique(existing.get("reasons", []) + item.get("reasons", []))
            existing["sources"] = unique(existing.get("sources", []) + item.get("sources", []))
            existing["project_functions"] = unique(existing.get("project_functions", []) + item.get("project_functions", []))
            existing["module_paths"] = unique(existing.get("module_paths", []) + item.get("module_paths", []))
            if item.get("hotspot") and not existing.get("hotspot"):
                existing["hotspot"] = item["hotspot"]
    return list(merged.values())


def sort_hits(hits: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    return sorted(hits, key=lambda item: (-item["score"], item["task_id"], item["path"]))[:limit]


def search_tasks(query: str) -> list[dict[str, Any]]:
    variants = expand_query(query)
    hits = []
    for task in load_task_index():
        reasons = []
        score = 0

        task_id_score = score_list(query, [task.get("task_id", "")], exact=1000, prefix=700, contains=500)
        if task_id_score:
            score += task_id_score
            reasons.append("task_id")

        symbol_score = score_list(query, task.get("symbols", []), exact=700, prefix=450, contains=250)
        if symbol_score:
            score += symbol_score
            reasons.append("symbol")

        owner_score = score_list(query, task.get("owners", []), exact=650, prefix=420, contains=220)
        if owner_score:
            score += owner_score
            reasons.append("owner")

        func_score = score_list(query, task.get("project_functions", []), exact=800, prefix=500, contains=320)
        if func_score:
            score += func_score
            reasons.append("project_function")

        module_score = score_list(query, task.get("module_paths", []), exact=800, prefix=520, contains=320)
        if module_score:
            score += module_score
            reasons.append("module_path")

        aliases_en_score = score_list(query, task.get("aliases_en", []), exact=420, prefix=260, contains=160)
        if aliases_en_score:
            score += aliases_en_score
            reasons.append("aliases_en")

        aliases_zh_score = score_list(query, task.get("aliases_zh", []), exact=150, prefix=90, contains=50)
        if aliases_zh_score:
            score += aliases_zh_score
            reasons.append("aliases_zh_support")

        keywords_zh_score = score_list(query, task.get("keywords_zh", []), exact=120, prefix=80, contains=40)
        if keywords_zh_score:
            score += keywords_zh_score
            reasons.append("keywords_zh_support")

        score += score_text(
            variants,
            task.get("title", ""),
            " ".join(task.get("symbols", [])),
            " ".join(task.get("project_functions", [])),
            " ".join(task.get("module_paths", [])),
            " ".join(task.get("aliases_en", [])),
        )

        if score:
            hit = build_hit(
                score=score,
                title=str(task.get("title", "")),
                path=str(task.get("path", "")),
                task_id=str(task.get("task_id", "-")),
                reasons=reasons,
                sources=["from_task"],
                project_functions=task.get("project_functions", []),
                module_paths=task.get("module_paths", []),
            )
            attach_hotspot(
                hit,
                list(task.get("symbols", [])) + list(task.get("promotion_watch_symbols", [])),
            )
            hits.append(hit)
    return sort_hits(hits, 15)


def search_task_field(query: str, field: str) -> list[dict[str, Any]]:
    hits = []
    for task in load_task_index():
        raw = task.get(field, [])
        values = raw if isinstance(raw, list) else [str(raw)]
        score = score_list(query, values, exact=1000, prefix=550, contains=300)
        if score:
            hit = build_hit(
                score=score,
                title=str(task.get("title", "")),
                path=str(task.get("path", "")),
                task_id=str(task.get("task_id", "-")),
                reasons=[field],
                sources=["from_task"],
                project_functions=task.get("project_functions", []),
                module_paths=task.get("module_paths", []),
            )
            attach_hotspot(
                hit,
                list(task.get("symbols", [])) + list(task.get("promotion_watch_symbols", [])),
            )
            hits.append(hit)
    return sort_hits(hits, 15)


def search_core_symbols(query: str) -> list[dict[str, Any]]:
    hits = []
    variants = expand_query(query)
    for meta_path in sorted((ROOT / "03_core_symbols").rglob("*.meta.json")):
        meta = load_json(meta_path)
        if not isinstance(meta, dict):
            continue
        symbol = str(meta.get("symbol", ""))
        score = score_list(query, [symbol], exact=900, prefix=500, contains=260)
        score += score_text(
            variants,
            symbol,
            " ".join(meta.get("owners", [])),
            str(meta.get("pywin32_signature", "")),
        )
        if score:
            hit = build_hit(
                score=score,
                title=symbol,
                path=str(meta.get("path_md", "")),
                task_id="-",
                reasons=["core_symbol"],
                sources=["from_core"],
                module_paths=meta.get("project_paths", []),
            )
            attach_hotspot(hit, [symbol])
            hits.append(hit)
    return sort_hits(hits, 15)


def scan_markdown(root: Path) -> list[dict[str, str]]:
    rows = []
    if not root.exists():
        return rows
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), path.stem)
        rows.append({"title": title, "path": str(path.relative_to(ROOT)).replace("\\", "/"), "text": text})
    return rows


def search_bridge_docs(query: str) -> list[dict[str, Any]]:
    variants = expand_query(query)
    hits = []
    for row in scan_markdown(ROOT / "05_pywin32_bridge"):
        score = score_text(variants, row["title"], row["path"], row["text"])
        if score:
            hits.append(
                build_hit(
                    score=score,
                    title=row["title"],
                    path=row["path"],
                    task_id="-",
                    reasons=["bridge_doc"],
                    sources=["from_bridge"],
                )
            )
    return sort_hits(hits, 12)


def search_hotspot_candidates(query: str) -> list[dict[str, Any]]:
    variants = expand_query(query)
    hits = []
    for item in load_hotspot_candidates():
        score = score_list(query, [str(item.get("symbol", ""))], exact=860, prefix=500, contains=260)
        score += score_text(
            variants,
            str(item.get("symbol", "")),
            str(item.get("owner", "")),
            str(item.get("reason", "")),
            str(item.get("last_seen_task", "")),
        )
        if score:
            hits.append(
                build_hit(
                    score=score,
                    title=f"Hotspot: {item.get('symbol', '')}",
                    path="07_validation/hotspot_candidates.json",
                    task_id="-",
                    reasons=["hotspot_candidate"],
                    sources=["from_hotspot_candidate"],
                    hotspot_item=item,
                )
            )
    return sort_hits(hits, 10)


def search_on_demand(query: str) -> list[dict[str, Any]]:
    variants = expand_query(query)
    hits = []
    for row in load_jsonl(ROOT / "06_on_demand_index" / "uncommon_topics.jsonl"):
        row_title = str(row.get("title", ""))
        status = str(row.get("status", "archive"))
        score = score_text(
            variants,
            row_title,
            str(row.get("topic_id", "")),
            str(row.get("path", "")),
            str(row.get("summary", "")),
            " ".join(str(keyword) for keyword in row.get("keywords", [])),
        )
        if score:
            source = "from_hotspot_candidate" if status == "hotspot_candidate" else "from_on_demand"
            hit = build_hit(
                score=score,
                title=row_title,
                path=str(row.get("path", "")),
                task_id="-",
                reasons=[status if status else "uncommon"],
                sources=[source],
            )
            symbol_names = [str(row.get("candidate_symbol", "")), str(row.get("promoted_symbol", ""))]
            attach_hotspot(hit, symbol_names)
            hits.append(hit)
    return sort_hits(hits, 15)


def search_raw_html(query: str) -> list[dict[str, Any]]:
    variants = expand_query(query)
    hits = []
    for row in load_jsonl(MANIFEST_PATH):
        score = score_text(
            variants,
            str(row.get("title", "")),
            str(row.get("path", "")),
            " ".join(str(keyword) for keyword in row.get("keywords", [])),
        )
        if score:
            hits.append(
                build_hit(
                    score=score,
                    title=str(row.get("title", "")),
                    path=str(row.get("path", "")),
                    task_id="-",
                    reasons=["raw_html"],
                    sources=["from_raw_html"],
                )
            )
    return sort_hits(hits, 12)


def search_keyword(query: str) -> list[dict[str, Any]]:
    hits = merge_hits(
        search_tasks(query),
        search_core_symbols(query),
        search_bridge_docs(query),
        search_hotspot_candidates(query),
        search_on_demand(query),
        search_raw_html(query),
    )
    return sort_hits(hits, 20)


def print_hits(hits: list[dict[str, Any]]) -> None:
    if not hits:
        print("No hits.")
        return
    for item in hits:
        print(f"[{item['score']:04d}] {item['title']}")
        print(
            "      "
            f"task_id={item['task_id']} reasons={', '.join(item['reasons'])} "
            f"sources={', '.join(item.get('sources', []))}"
        )
        print(f"      {item['path']}")
        if item.get("project_functions"):
            print(f"      project_functions={', '.join(item['project_functions'])}")
        if item.get("module_paths"):
            print(f"      module_paths={', '.join(item['module_paths'])}")
        hotspot = item.get("hotspot")
        if hotspot:
            state = hotspot.get("state", "")
            symbol = hotspot.get("symbol", "")
            action = hotspot.get("suggested_action", "")
            reason = hotspot.get("reason", "")
            print(f"      hotspot={symbol} state={state} action={action}")
            if reason:
                print(f"      hotspot_note={reason}")


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(
            "Usage: py -3 tools/search_cad_help.py "
            "<task|task_id|symbol|owner|function|module|keyword|uncommon> <query>"
        )
        return 1

    mode = argv[1].lower()
    query = " ".join(argv[2:]).strip()
    if not query:
        print("Empty query.")
        return 1

    if mode == "task":
        print_hits(search_tasks(query))
    elif mode == "task_id":
        print_hits(search_task_field(query, "task_id"))
    elif mode == "symbol":
        print_hits(
            sort_hits(
                merge_hits(
                    search_task_field(query, "symbols"),
                    search_task_field(query, "promotion_watch_symbols"),
                    search_core_symbols(query),
                    search_hotspot_candidates(query),
                    search_on_demand(query),
                    search_raw_html(query),
                ),
                20,
            )
        )
    elif mode == "owner":
        print_hits(search_task_field(query, "owners"))
    elif mode == "function":
        print_hits(search_task_field(query, "project_functions"))
    elif mode == "module":
        print_hits(search_task_field(query, "module_paths"))
    elif mode == "keyword":
        print_hits(search_keyword(query))
    elif mode == "uncommon":
        print_hits(sort_hits(merge_hits(search_hotspot_candidates(query), search_on_demand(query)), 15))
    else:
        print(f"Unsupported mode: {mode}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
