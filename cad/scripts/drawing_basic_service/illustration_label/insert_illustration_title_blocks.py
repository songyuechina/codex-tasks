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

from illustration_label.illustration_frame_service import DEFAULT_MATCH_MODE, apply_illustration_labels
from system.common_logger import set_debug_mode, sys_logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="为已具备标准图框的 DWG 插入图签块；若缺少用户模板则自动回填到 user_frame 后使用。"
    )
    parser.add_argument("--target", required=True, help="目标 DWG")
    parser.add_argument(
        "--match-mode",
        default=DEFAULT_MATCH_MODE,
        help="打印区域匹配模式：basic / adaptive / purified_adaptive，默认 purified_adaptive",
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
            match_mode=args.match_mode,
            ensure_guard=not args.no_guard_launch,
            insert_titles=True,
            include_model=not args.no_model,
            include_layouts=not args.no_layouts,
            only_layouts=args.layout,
        )
    except Exception as exc:
        sys_logger.error("[insert_illustration_title_blocks] 执行失败: %s", exc, exc_info=True)
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(exc),
                    "target_file": str(Path(args.target).resolve()),
                    "match_mode": args.match_mode,
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
