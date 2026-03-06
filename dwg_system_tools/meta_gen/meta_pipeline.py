#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
meta_pipeline.py

用途（DWG System Tools / meta_gen）
- 为“脚本 → meta”工作流提供一个可控的本地流水线入口
- 当前版本聚焦于：定位目标脚本 → 定位同目录 meta → 运行校验（meta_validator）→ 汇总报告
- 生成 meta 的“语义部分”由 dwg_agents_ops 智能体按 META_RULES_V1 执行，本脚本不调用任何 API（节省 token）

约定（新策略：meta 与脚本同目录）
- 对脚本 A.py，在相同目录放置：
  - A_quote.meta.json
  - A_procedure.meta.json

典型用法（common_logger.py）：

1) 让智能体生成（与脚本同目录）：
   D:/codex-tasks/cad/system/common_logger.py
   D:/codex-tasks/cad/system/common_logger_quote.meta.json
   D:/codex-tasks/cad/system/common_logger_procedure.meta.json

2) 运行流水线校验并汇总：
   python meta_pipeline.py --root D:/codex-tasks --stem common_logger --validate

也可以扫描全仓 meta：
   python meta_pipeline.py --root D:/codex-tasks --scan-generated --validate

输出：
- stdout 汇总
- 可选写入 report json：
  --report D:/codex-tasks/dwg_system_tools/meta_gen/_reports/report.json
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional, Tuple
import subprocess
import sys


# -------------------------
# Root
# -------------------------
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


# -------------------------
# Search rules
# -------------------------
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "_generated_meta",   # 旧集中输出目录（保留排除）
    "_reports",
    ".pytest_cache",
    ".mypy_cache",
}


def _should_skip_dir(path: Path, exclude_dirs: set[str]) -> bool:
    name = path.name
    if name in exclude_dirs:
        return True
    # 额外：跳过隐藏目录（可选）
    if name.startswith(".") and name not in {".", ".."}:
        return True
    return False


def find_script_by_stem(root: Path, stem: str, exclude_dirs: Optional[set[str]] = None) -> Path:
    """
    在 root 下递归寻找 {stem}.py
    若找到多个，抛错并列出候选。
    """
    if exclude_dirs is None:
        exclude_dirs = set(DEFAULT_EXCLUDE_DIRS)

    target_name = f"{stem}.py"
    hits: List[Path] = []

    # 手写递归，便于排除目录
    stack = [root]
    while stack:
        cur = stack.pop()
        try:
            for p in cur.iterdir():
                if p.is_dir():
                    if _should_skip_dir(p, exclude_dirs):
                        continue
                    stack.append(p)
                elif p.is_file():
                    if p.name == target_name:
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


def meta_paths_for_script(script_path: Path) -> Tuple[Path, Path]:
    """
    A.py -> same_dir/A_quote.meta.json, same_dir/A_procedure.meta.json
    """
    stem = script_path.stem
    d = script_path.parent
    return d / f"{stem}_quote.meta.json", d / f"{stem}_procedure.meta.json"


def scan_all_meta(root: Path, exclude_dirs: Optional[set[str]] = None) -> List[Path]:
    """
    递归扫描 root 下所有 *.meta.json（默认排除旧 _generated_meta、_reports 等目录）
    """
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
                elif p.is_file():
                    if p.name.endswith(".meta.json"):
                        hits.append(p)
        except PermissionError:
            continue

    return sorted(hits)


# -------------------------
# Validator
# -------------------------
def run_validator(root: Path, files: List[Path], report: Optional[Path] = None) -> int:
    schema = root / "dwg_system_tools" / "meta_gen" / "META_SCHEMA_V1.json"
    validator = root / "dwg_system_tools" / "meta_gen" / "meta_validator.py"

    cmd = [sys.executable, str(validator), "--schema", str(schema), "--files"] + [str(f) for f in files]
    if report is not None:
        cmd += ["--report", str(report)]

    print("[RUN] " + " ".join(cmd))
    return subprocess.call(cmd)


# -------------------------
# Main
# -------------------------
def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="", help="Path to D:/codex-tasks (optional; will infer from cwd)")
    ap.add_argument("--stem", default="", help="Script stem name (e.g., common_logger) to validate its quote/procedure meta")
    ap.add_argument(
        "--scan-generated",
        action="store_true",
        help="Scan whole repository for *.meta.json (in-place, excluding _generated_meta/_reports by default)"
    )
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

        q, p = meta_paths_for_script(script_path)
        targets = [q, p]

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
            print("Hint: generate meta next to the script:")
            try:
                script_path = find_script_by_stem(root, args.stem)
                q, p = meta_paths_for_script(script_path)
                print(f" - {q}")
                print(f" - {p}")
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
