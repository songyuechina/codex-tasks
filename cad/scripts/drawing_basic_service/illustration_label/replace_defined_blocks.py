from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def find_codex_tasks_root(p: Path) -> Path:
    cur = p.resolve()
    if cur.is_file():
        cur = cur.parent
    while True:
        if cur.name.lower() == "codex-tasks":
            return cur
        if cur.parent == cur:
            raise RuntimeError("找不到根目录 codex-tasks")
        cur = cur.parent


ROOT = find_codex_tasks_root(Path(__file__))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "cad") not in sys.path:
    sys.path.insert(0, str(ROOT / "cad"))

from illustration_block_service import DEFAULT_BLOCK_NAMES, replace_defined_blocks
from system.common_logger import set_debug_mode, sys_logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="用源 DWG 的同名块定义替换目标 DWG 中已存在的块定义。"
    )
    parser.add_argument("--target", required=True, help="目标 DWG，例如 A.dwg")
    parser.add_argument("--source", required=True, help="源 DWG，例如 B.dwg")
    parser.add_argument(
        "--names",
        nargs="+",
        default=list(DEFAULT_BLOCK_NAMES),
        help="要替换的块名列表，默认 A0 A1 A2 A3",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="日志级别，例如 INFO / DEBUG",
    )
    parser.add_argument(
        "--run-attsync",
        action="store_true",
        help="替换后执行 ATTSYNC。默认关闭，避免历史同步链在无属性块时引入额外不稳定性。",
    )
    parser.add_argument(
        "--no-guard-launch",
        action="store_true",
        help="不主动拉起 cad_runtime_guard / dialog killer / command monitor",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    set_debug_mode(mode=1, log_level=args.log_level.upper())

    try:
        result = replace_defined_blocks(
            target_file=args.target,
            source_file=args.source,
            block_names=args.names,
            ensure_guard=not args.no_guard_launch,
            run_attsync=args.run_attsync,
        )
    except Exception as exc:
        sys_logger.error("[replace_defined_blocks] 执行失败: %s", exc, exc_info=True)
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(exc),
                    "target_file": str(Path(args.target).resolve()),
                    "source_file": str(Path(args.source).resolve()),
                    "block_names": args.names,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
