from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "02_manifest" / "page_manifest.jsonl"
OUT_DIR = ROOT / "06_on_demand_index"


def load_manifest() -> list[dict[str, object]]:
    rows = []
    with MANIFEST_PATH.open("r", encoding="utf-8") as fh:
        for line in fh:
            rows.append(json.loads(line))
    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = load_manifest()
    uncommon = []
    keyword_map: dict[str, list[str]] = defaultdict(list)
    path_map = {}

    for record in records:
        if record["status"] != "defer":
            continue
        item = {
            "topic_id": record["topic_id"],
            "source": record["source_doc"],
            "kind": record["kind_guess"],
            "owner": record["owner_guess"],
            "title": record["title"],
            "keywords": record["keywords"],
            "value_level": record["value_level"],
            "path": record["path"],
            "summary": record["notes"],
        }
        uncommon.append(item)
        path_map[record["topic_id"]] = record["path"]
        for keyword in record["keywords"][:8]:
            keyword_map[keyword].append(record["topic_id"])

    uncommon.sort(key=lambda item: (item["value_level"] != "medium", item["title"]))
    with (OUT_DIR / "uncommon_topics.jsonl").open("w", encoding="utf-8", newline="\n") as fh:
        for item in uncommon:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")

    compact_keywords = {
        key: sorted(values)[:20]
        for key, values in sorted(keyword_map.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        if len(values) >= 2
    }
    (OUT_DIR / "uncommon_keywords.json").write_text(
        json.dumps(compact_keywords, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    (OUT_DIR / "topic_path_map.json").write_text(
        json.dumps(path_map, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )

    summary = Counter(item["kind"] for item in uncommon)
    print(f"Generated on-demand index for {len(uncommon)} topics.")
    print(json.dumps(dict(summary), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
