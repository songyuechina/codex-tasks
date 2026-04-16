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
CAD_ROOT = ROOT / "cad"
DRAWING_BASIC_ROOT = CAD_ROOT / "scripts" / "drawing_basic_service"
for candidate in (ROOT, CAD_ROOT, DRAWING_BASIC_ROOT):
    text = str(candidate)
    if text not in sys.path:
        sys.path.insert(0, text)

from illustration_frame_service import DEFAULT_MATCH_MODE, apply_illustration_labels
from illustration_block_service import DEFAULT_BLOCK_NAMES
from system.common_logger import set_debug_mode, sys_logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="按打印区域插入标准图框和图签块。默认使用 purified_adaptive 模式。"
    )
    parser.add_argument("--target", required=True, help="目标 DWG")
    parser.add_argument(
        "--title-source",
        help="可选。插入前先用该 DWG 中的 A0/A1/A2/A3 替换目标文件同名块定义。",
    )
    parser.add_argument(
        "--names",
        nargs="+",
        default=list(DEFAULT_BLOCK_NAMES),
        help="需要准备的图签块名，默认 A0 A1 A2 A3",
    )
    parser.add_argument(
        "--match-mode",
        default=DEFAULT_MATCH_MODE,
        help="打印区域匹配模式：basic / adaptive / purified_adaptive，默认 purified_adaptive",
    )
    parser.add_argument(
        "--run-attsync",
        action="store_true",
        help="若同时执行块定义替换，则替换后执行 ATTSYNC。",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="日志级别，例如 INFO / DEBUG",
    )
    parser.add_argument(
        "--no-guard-launch",
        action="store_true",
        help="不主动拉起 cad_runtime_guard / dialog killer / command monitor",
    )
    parser.add_argument(
        "--frames-only",
        action="store_true",
        help="只处理标准图框，不插入图签块。",
    )
    parser.add_argument("--layout", action="append", default=None, help="只处理指定布局，可重复传入")
    parser.add_argument("--no-model", action="store_true", help="跳过模型空间")
    parser.add_argument("--no-layouts", action="store_true", help="跳过图纸空间布局")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    set_debug_mode(mode=1, log_level=args.log_level.upper())
    if args.layout and args.no_layouts:
        raise SystemExit("--layout 与 --no-layouts 不能同时使用")

    try:
        result = apply_illustration_labels(
            target_file=args.target,
            title_block_source_file=args.title_source,
            block_names=args.names,
            match_mode=args.match_mode,
            ensure_guard=not args.no_guard_launch,
            run_attsync=args.run_attsync,
            insert_titles=not args.frames_only,
            include_model=not args.no_model,
            include_layouts=not args.no_layouts,
            only_layouts=args.layout,
        )
    except Exception as exc:
        sys_logger.error("[insert_illustration_labels] 执行失败: %s", exc, exc_info=True)
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(exc),
                    "target_file": str(Path(args.target).resolve()),
                    "title_block_source_file": None
                    if not args.title_source
                    else str(Path(args.title_source).resolve()),
                    "match_mode": args.match_mode,
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
