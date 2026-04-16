from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

from lxml import html


ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "01_extracted_html"
MANIFEST_DIR = ROOT / "02_manifest"

SKIP_PREFIXES = ("idx_", "all_", "idh_", "idh", "idh-", "idh")
DEFER_PREFIXES = ("ex_",)
DEFER_KEYWORDS = {
    "3d",
    "surface",
    "render",
    "material",
    "camera",
    "mesh",
    "loft",
    "helix",
    "visual style",
    "sun",
    "light",
    "section",
}
HIGH_PRIORITY_KEYWORDS = {
    "application",
    "documents",
    "document",
    "modelspace",
    "paperspace",
    "layout",
    "layouts",
    "activelayout",
    "selectionset",
    "selectionsets",
    "block",
    "blockreference",
    "attribute",
    "attributereference",
    "getattributes",
    "hasattributes",
    "insertblock",
    "addline",
    "addpolyline",
    "addtext",
    "addmtext",
    "layer",
    "layers",
    "objectname",
    "handle",
    "boundingbox",
    "coordinates",
    "plot",
    "plotconfiguration",
    "refreshplotdeviceinfo",
    "setwindowtoplot",
    "getvariable",
    "setvariable",
    "sendcommand",
    "regen",
    "utility",
}
PROJECT_TASK_KEYWORDS = {
    "plot": "print",
    "print": "print",
    "layout": "layout",
    "paperspace": "layout",
    "modelspace": "layout",
    "selection": "selection",
    "selectionset": "selection",
    "block": "titleblock",
    "attribute": "titleblock",
    "text": "titleblock",
    "mtext": "titleblock",
    "insertblock": "titleblock",
    "getattributes": "titleblock",
    "layer": "construction",
    "polyline": "construction",
    "line": "construction",
    "document": "document",
    "application": "document",
    "sendcommand": "fallback",
    "variable": "fallback",
}
ALIASES = {
    "titleblock": {
        "aliases_en": ["title block", "block attribute", "attribute block"],
        "aliases_zh": ["图签"],
        "keywords_zh": ["图签属性", "属性块"],
    },
    "catalog": {
        "aliases_en": ["drawing list", "catalog", "table of contents"],
        "aliases_zh": ["目录"],
        "keywords_zh": ["目录图签", "目录页"],
    },
    "print": {
        "aliases_en": ["print", "plot", "pdf"],
        "aliases_zh": ["布局输出"],
        "keywords_zh": ["打印", "出图"],
    },
    "layout": {
        "aliases_en": ["layout", "paperspace", "modelspace", "space"],
        "aliases_zh": ["布局"],
        "keywords_zh": ["模型空间", "图纸空间"],
    },
    "selection": {
        "aliases_en": ["selection", "selectionset", "window select"],
        "aliases_zh": ["选择集"],
        "keywords_zh": ["选择", "窗口选"],
    },
}


def iter_html_files() -> Iterable[Path]:
    for doc_name in ("acad_aag", "acadauto"):
        doc_root = EXTRACTED / doc_name
        if not doc_root.exists():
            raise SystemExit(f"Missing extracted directory: {doc_root}")
        yield from sorted(doc_root.rglob("*.htm"))
        yield from sorted(doc_root.rglob("*.html"))


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def extract_title(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    try:
        doc = html.fromstring(raw)
        title = normalize_space(doc.findtext(".//title", default=""))
        if title:
            return title
        h1 = doc.xpath("string(//h1)")
        if h1:
            return normalize_space(h1)
    except Exception:
        pass

    match = re.search(r"<title>(.*?)</title>", raw, flags=re.I | re.S)
    if match:
        return normalize_space(match.group(1))
    return path.stem


def guess_kind(title: str, basename: str) -> str:
    text = f"{title} {basename}".lower()
    if " method" in text:
        return "method"
    if " property" in text:
        return "property"
    if " event" in text:
        return "event"
    if " object" in text or " collection" in text:
        return "object"
    if " system variable" in text:
        return "system_variable"
    if " enum" in text or " enumeration" in text:
        return "enum"
    if " type" in text or " variant" in text:
        return "type"
    return "topic"


def guess_owner(title: str) -> str:
    match = re.search(r"\(([^)]+)\)", title)
    if match:
        owner = normalize_space(match.group(1))
        if len(owner) <= 48:
            return owner
    return ""


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9_]+", text)


def classify(title: str, basename: str) -> tuple[str, str, int, list[str], str]:
    lower_name = basename.lower()
    combined = f"{title.lower()} {lower_name}"

    if lower_name.endswith("_see_also.htm") or lower_name.endswith("_see_also.html"):
        return "skip", "low", 0, [], "see_also helper page"
    if lower_name.startswith(SKIP_PREFIXES):
        return "skip", "low", 0, [], "index/helper page"

    matched_tags: list[str] = []
    score = 0

    for keyword in HIGH_PRIORITY_KEYWORDS:
        if keyword in combined:
            score += 4

    for keyword, tag in PROJECT_TASK_KEYWORDS.items():
        if keyword in combined:
            score += 2
            matched_tags.append(tag)

    if lower_name.startswith(DEFER_PREFIXES):
        return "defer", "low", score, sorted(set(matched_tags)), "example page"

    if any(keyword in combined for keyword in DEFER_KEYWORDS):
        return "defer", "low", score, sorted(set(matched_tags)), "low relevance to current project focus"

    if score >= 8:
        return "keep", "high", score, sorted(set(matched_tags)), "project-relevant core topic"
    if score >= 3:
        return "defer", "medium", score, sorted(set(matched_tags)), "useful but not first-batch core"
    return "defer", "low", score, sorted(set(matched_tags)), "kept only for on-demand search"


def build_record(path: Path) -> dict[str, object]:
    title = extract_title(path)
    source_doc = path.parts[path.parts.index("01_extracted_html") + 1]
    basename = path.name
    status, value_level, score, matched_tags, notes = classify(title, basename)
    tokens = tokenize(f"{title} {basename}")
    topic_seed = re.sub(r"[^A-Za-z0-9_]+", "_", Path(basename).stem).strip("_") or "topic"
    return {
        "topic_id": f"{source_doc}:{topic_seed}",
        "source_doc": source_doc,
        "basename": basename,
        "title": title,
        "kind_guess": guess_kind(title, basename),
        "owner_guess": guess_owner(title),
        "class_guess": "core_symbol" if status == "keep" else ("auxiliary" if status == "skip" else "on_demand"),
        "value_level": value_level,
        "status": status,
        "project_score": score,
        "project_tags": matched_tags,
        "keywords": sorted(set(token.lower() for token in tokens if len(token) > 2))[:20],
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "notes": notes,
    }


def write_jsonl(path: Path, records: Iterable[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    records = [build_record(path) for path in iter_html_files()]
    records.sort(key=lambda item: (item["status"] != "keep", -int(item["project_score"]), item["title"]))

    page_manifest = MANIFEST_DIR / "page_manifest.jsonl"
    write_jsonl(page_manifest, records)

    with (MANIFEST_DIR / "page_manifest.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "topic_id",
                "source_doc",
                "basename",
                "title",
                "kind_guess",
                "owner_guess",
                "class_guess",
                "value_level",
                "status",
                "project_score",
                "project_tags",
                "keywords",
                "path",
                "notes",
            ],
        )
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["project_tags"] = ",".join(record["project_tags"])
            row["keywords"] = ",".join(record["keywords"])
            writer.writerow(row)

    defer_records = [record for record in records if record["status"] == "defer"]
    skip_records = [record for record in records if record["status"] == "skip"]
    ranked_records = sorted(records, key=lambda item: (-int(item["project_score"]), item["title"]))

    write_jsonl(MANIFEST_DIR / "defer_list.jsonl", defer_records)
    write_jsonl(MANIFEST_DIR / "skip_list.jsonl", skip_records)
    write_jsonl(MANIFEST_DIR / "value_ranking.jsonl", ranked_records)
    (MANIFEST_DIR / "alias_map.json").write_text(json.dumps(ALIASES, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    counts = Counter(record["status"] for record in records)
    tag_counts = Counter(tag for record in records for tag in record["project_tags"])
    summary = {
        "total_pages": len(records),
        "status_counts": dict(counts),
        "project_tag_counts": dict(tag_counts),
        "top_keep_titles": [record["title"] for record in records if record["status"] == "keep"][:30],
    }
    (MANIFEST_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print(f"Manifest written: {page_manifest}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
