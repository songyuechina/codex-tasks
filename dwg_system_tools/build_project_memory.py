#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


TEXT_EXTS = {".py", ".md", ".txt", ".json", ".toml", ".yml", ".yaml", ".ps1", ".bat", ".ini"}

CURATED_TARGETS = [
    "README.md",
    "AGENTS.md",
    "folder.meta.json",
    "cad/folder.meta.json",
    "thoughtway",
    "dwg_agents_ops",
    "dwg_system_tools",
    "cad/system",
    "cad/tools",
    "cad/library",
    "cad/scripts/drawing_basic_service/print",
]

EXCLUDED_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "_cache",
    "logs",
    "runtime",
    "outputs",
    "output",
    "sessions",
    "supervision",
    "assets",
    "_generated_meta",
}

EXCLUDED_PREFIXES = [
    ".accelerate",
    ".codex",
    ".spec-workflow",
    "dwg_cases",
    "thoughtway/参考",
    "thoughtway/project_memory",
    "cad/scripts/drawing_basic_service/print/cases/assets",
    "cad/scripts/drawing_basic_service/print/cases/output",
    "dwg_agents_ops/local",
    "dwg_agents_ops/Planner_Agent/memory",
    "dwg_agents_ops/Coder_Agent/memory",
    "dwg_agents_ops/Reviewer_Agent/memory",
    "dwg_agents_ops/Tester_Agent/memory",
    "dwg_agents_ops/agent_control/runtime",
    "dwg_agents_ops/agent_control/supervision",
]


@dataclass
class Section:
    path: str
    kind: str
    summary: str
    files: list[dict[str, Any]]


def infer_root(start: Path) -> Path:
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent
    while True:
        if cur.name.lower() == "codex-tasks":
            return cur
        if cur.parent == cur:
            raise RuntimeError("Cannot find codex-tasks root")
        cur = cur.parent


def rel_posix(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def is_excluded(rel_path: str, parts: tuple[str, ...]) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in parts[:-1]):
        return True
    return any(rel_path == prefix or rel_path.startswith(prefix + "/") for prefix in EXCLUDED_PREFIXES)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def first_nonempty_line(text: str) -> str:
    for raw in text.splitlines():
        line = raw.strip()
        if line:
            return line
    return ""


def extract_doc_summary(path: Path) -> str:
    text = read_text(path)
    generic_tokens = {
        path.name.strip().lower(),
        path.stem.strip().lower(),
    }
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if heading and heading.lower() not in generic_tokens:
                return heading
            continue
        if line:
            return line[:120]
    return first_nonempty_line(text)[:120]


def extract_json_summary(path: Path) -> str:
    if path.name == "folder.meta.json":
        try:
            data = json.loads(read_text(path))
        except Exception:
            return "folder meta (parse failed)"
        role = str(data.get("role", "")).strip()
        summary = str(data.get("summary", "")).strip()
        if role and summary:
            return f"{role}: {summary}"
        if summary:
            return summary
    return f"json file: {path.name}"


def extract_py_summary(path: Path) -> dict[str, Any]:
    src = read_text(path)
    try:
        tree = ast.parse(src, filename=str(path))
    except Exception as exc:
        return {
            "summary": f"python parse failed: {exc}",
            "functions": 0,
            "classes": 0,
            "has_main": False,
            "top_symbols": [],
        }

    funcs = []
    classes = []
    has_main = False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.If):
            try:
                test_text = ast.unparse(node.test)
            except Exception:
                test_text = ""
            if "__name__" in test_text and "__main__" in test_text:
                has_main = True

    top_symbols = funcs[:6] + classes[:4]
    summary = f"py funcs={len(funcs)} classes={len(classes)} main={'yes' if has_main else 'no'}"
    return {
        "summary": summary,
        "functions": len(funcs),
        "classes": len(classes),
        "has_main": has_main,
        "top_symbols": top_symbols,
    }


def build_file_entry(path: Path, root: Path) -> dict[str, Any]:
    rel = rel_posix(path, root)
    suffix = path.suffix.lower()
    if suffix == ".py":
        py_info = extract_py_summary(path)
        return {
            "path": rel,
            "type": "py",
            **py_info,
        }
    if suffix in {".md", ".txt"}:
        return {
            "path": rel,
            "type": suffix.lstrip("."),
            "summary": extract_doc_summary(path),
        }
    if suffix in {".toml", ".yml", ".yaml", ".ps1", ".bat", ".ini"}:
        return {
            "path": rel,
            "type": suffix.lstrip("."),
            "summary": first_nonempty_line(read_text(path))[:120],
        }
    if suffix == ".json":
        return {
            "path": rel,
            "type": "json",
            "summary": extract_json_summary(path),
        }
    return {
        "path": rel,
        "type": suffix.lstrip("."),
        "summary": path.name,
    }


def walk_curated_dir(dir_path: Path, root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(dir_path.rglob("*")):
        if not path.is_file():
            continue
        rel = rel_posix(path, root)
        if path.suffix.lower() not in TEXT_EXTS:
            continue
        if is_excluded(rel, tuple(Path(rel).parts)):
            continue
        entries.append(build_file_entry(path, root))
    return entries


def section_summary(dir_path: Path, root: Path) -> str:
    meta_path = dir_path / "folder.meta.json"
    if meta_path.exists():
        return extract_json_summary(meta_path)
    rel = rel_posix(dir_path, root)
    return f"source section: {rel}"


def build_sections(root: Path) -> list[Section]:
    sections: list[Section] = []
    for target in CURATED_TARGETS:
        path = root / target
        if not path.exists():
            continue
        rel = rel_posix(path, root)
        if path.is_file():
            sections.append(
                Section(
                    path=rel,
                    kind="file",
                    summary=build_file_entry(path, root)["summary"],
                    files=[build_file_entry(path, root)],
                )
            )
            continue
        files = walk_curated_dir(path, root)
        sections.append(Section(path=rel, kind="directory", summary=section_summary(path, root), files=files))
    return sections


def build_payload(root: Path) -> dict[str, Any]:
    sections = build_sections(root)
    total_files = sum(len(section.files) for section in sections)
    py_files = sum(1 for section in sections for item in section.files if item["type"] == "py")
    md_files = sum(1 for section in sections for item in section.files if item["type"] == "md")
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "root": str(root),
        "scope": {
            "curated_targets": CURATED_TARGETS,
            "excluded_prefixes": EXCLUDED_PREFIXES,
            "excluded_dir_names": sorted(EXCLUDED_DIR_NAMES),
            "included_extensions": sorted(TEXT_EXTS),
            "notes": [
                "thoughtway 根目录用于治理与思想指导。",
                "thoughtway/参考 下的参考脚本不纳入项目主记忆地图。",
            ],
        },
        "stats": {
            "section_count": len(sections),
            "file_count": total_files,
            "py_file_count": py_files,
            "md_file_count": md_files,
        },
        "sections": [
            {
                "path": section.path,
                "kind": section.kind,
                "summary": section.summary,
                "files": section.files,
            }
            for section in sections
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Project Map",
        "",
        f"- Generated: `{payload['generated_at']}`",
        f"- Root: `{payload['root']}`",
        f"- Curated sections: `{payload['stats']['section_count']}`",
        f"- Indexed files: `{payload['stats']['file_count']}`",
        f"- Python files: `{payload['stats']['py_file_count']}`",
        f"- Markdown files: `{payload['stats']['md_file_count']}`",
        "",
        "## Scope",
        "",
        "This map focuses on source/docs memory assets and excludes DWG/PDF inputs, outputs, sessions, runtime logs and caches.",
        "",
        "## Sections",
    ]

    for section in payload["sections"]:
        lines.extend(
            [
                "",
                f"### {section['path']}",
                "",
                f"- Kind: `{section['kind']}`",
                f"- Summary: {section['summary']}",
                f"- Files: `{len(section['files'])}`",
            ]
        )
        for item in section["files"]:
            line = f"- `{item['path']}` [{item['type']}] {item['summary']}"
            symbols = item.get("top_symbols") or []
            if symbols:
                line += f" | top={', '.join(symbols)}"
            lines.append(line)
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    root = infer_root(Path.cwd())
    payload = build_payload(root)
    out_dir = root / "thoughtway" / "project_memory"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "PROJECT_MAP.json"
    md_path = out_dir / "PROJECT_MAP.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"[OK] wrote {json_path}")
    print(f"[OK] wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
