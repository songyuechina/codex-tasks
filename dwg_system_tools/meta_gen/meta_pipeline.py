#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D:/codex-tasks/dwg_system_tools/meta_gen/meta_pipeline.py

用途（DWG System Tools / meta_gen）
- 为“脚本 → meta”工作流提供一个可控的本地流水线入口
- 支持脚本级 meta 与函数级 meta 的统一选择、缺失检查、校验与汇总
- 生成 meta 的“语义部分”由智能体按 META_RULES.md 执行，本脚本不调用任何 API

新的四层结构（meta 与脚本同目录）
- A.py
- A_quote.meta.json
- A_procedure.meta.json
- A_functions.quote.meta.json
- A_functions.procedure.meta.json
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import sys


DEFAULT_EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "_generated_meta",
    "_reports",
    ".pytest_cache",
    ".mypy_cache",
}


def find_root(p: Path) -> Path:
    cur = p.resolve()
    if cur.is_file():
        cur = cur.parent
    while True:
        if cur.name.lower() == "codex-tasks":
            return cur
        if cur.parent == cur:
            raise RuntimeError("Cannot find codex-tasks root")
        cur = cur.parent


def _should_skip_dir(path: Path, exclude_dirs: set[str]) -> bool:
    name = path.name
    if name in exclude_dirs:
        return True
    if name.startswith(".") and name not in {".", ".."}:
        return True
    return False


def find_script_by_stem(root: Path, stem: str, exclude_dirs: Optional[set[str]] = None) -> Path:
    if exclude_dirs is None:
        exclude_dirs = set(DEFAULT_EXCLUDE_DIRS)

    target_name = f"{stem}.py"
    hits: List[Path] = []
    stack = [root]

    while stack:
        cur = stack.pop()
        try:
            for p in cur.iterdir():
                if p.is_dir():
                    if _should_skip_dir(p, exclude_dirs):
                        continue
                    stack.append(p)
                elif p.is_file() and p.name == target_name:
                    hits.append(p)
        except PermissionError:
            continue

    if not hits:
        raise FileNotFoundError(f"Cannot find script '{target_name}' under root: {root}")

    if len(hits) > 1:
        msg = ["Multiple scripts found for stem:", f"  stem={stem}", "Candidates:"]
        msg += [f" - {h}" for h in sorted(hits)]
        raise RuntimeError("\n".join(msg))

    return hits[0]


def meta_paths_for_script(script_path: Path) -> Dict[str, Path]:
    stem = script_path.stem
    d = script_path.parent
    return {
        "quote": d / f"{stem}_quote.meta.json",
        "procedure": d / f"{stem}_procedure.meta.json",
        "functions.quote": d / f"{stem}_functions.quote.meta.json",
        "functions.procedure": d / f"{stem}_functions.procedure.meta.json",
    }


def select_meta_targets(script_path: Path, kind: str) -> List[Path]:
    mp = meta_paths_for_script(script_path)
    if kind == "script":
        return [mp["quote"], mp["procedure"]]
    if kind == "functions":
        return [mp["functions.quote"], mp["functions.procedure"]]
    if kind == "all":
        return [mp["quote"], mp["procedure"], mp["functions.quote"], mp["functions.procedure"]]
    raise ValueError(f"Unknown kind: {kind}")


def scan_all_meta(root: Path, exclude_dirs: Optional[set[str]] = None) -> List[Path]:
    if exclude_dirs is None:
        exclude_dirs = set(DEFAULT_EXCLUDE_DIRS)

    hits: List[Path] = []
    stack = [root]
    while stack:
        cur = stack.pop()
        try:
            for p in cur.iterdir():
                if p.is_dir():
                    if _should_skip_dir(p, exclude_dirs):
                        continue
                    stack.append(p)
                elif p.is_file() and p.name.endswith(".meta.json"):
                    hits.append(p)
        except PermissionError:
            continue
    return sorted(hits)


def run_validator(root: Path, files: List[Path], report: Optional[Path] = None) -> int:
    schema = root / "dwg_system_tools" / "meta_gen" / "META_SCHEMA.json"
    validator = root / "dwg_system_tools" / "meta_gen" / "meta_validator.py"

    cmd = [sys.executable, str(validator), "--schema", str(schema), "--files"] + [str(f) for f in files]
    if report is not None:
        cmd += ["--report", str(report)]

    print("[RUN] " + " ".join(cmd))
    return subprocess.call(cmd)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="", help="Path to D:/codex-tasks (optional; will infer from cwd)")
    ap.add_argument("--stem", default="", help="Script stem name (e.g., common_logger)")
    ap.add_argument("--kind", default="all", choices=["script", "functions", "all"], help="Which meta layer to select")
    ap.add_argument("--scan-generated", action="store_true", help="Scan whole repository for *.meta.json")
    ap.add_argument("--validate", action="store_true", help="Run meta_validator.py on selected files")
    ap.add_argument("--report", default="", help="Optional report json path")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else find_root(Path.cwd())
    targets: List[Path] = []

    if args.stem:
        try:
            script_path = find_script_by_stem(root, args.stem)
        except Exception as e:
            print("[ERROR] " + str(e))
            return 2

        targets = select_meta_targets(script_path, args.kind)
        print(f"[INFO] script={script_path}")

    elif args.scan_generated:
        targets = scan_all_meta(root)
    else:
        print("[ERROR] Must provide --stem <name> or --scan-generated")
        return 2

    if not targets:
        print("[ERROR] No meta files selected")
        return 2

    missing = [t for t in targets if not t.exists()]
    if missing:
        print("[ERROR] Missing meta files:")
        for m in missing:
            print(" - " + str(m))
        if args.stem:
            try:
                script_path = find_script_by_stem(root, args.stem)
                for p in select_meta_targets(script_path, args.kind):
                    print(" - " + str(p))
            except Exception:
                pass
        return 2

    print(f"[INFO] root={root}")
    print("[INFO] targets:")
    for t in targets:
        print(" - " + str(t))

    if args.validate:
        rp = Path(args.report).resolve() if args.report else None
        rc = run_validator(root, targets, report=rp)
        if rc != 0:
            print("[FAIL] Validation failed")
            return 1
        print("[OK] Validation passed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
