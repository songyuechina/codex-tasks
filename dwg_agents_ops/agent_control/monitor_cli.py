#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def parse_ts(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def age_text(value: str) -> str:
    dt = parse_ts(value)
    if dt is None:
        return "-"
    now = datetime.now(timezone.utc).astimezone()
    age = max(0, int((now - dt).total_seconds()))
    if age < 60:
        return f"{age}s"
    if age < 3600:
        return f"{age // 60}m"
    return f"{age // 3600}h"


def board_counts(board: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for task in board.get("tasks", []):
        status = task.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts


def render_once(control_root: Path) -> None:
    board = read_json(control_root / "task_board.json", {"tasks": []})
    runtime_dir = control_root / "runtime"

    print(f"control_root={control_root}")
    print(f"active_plan={board.get('active_plan_version')}")
    print(f"task_counts={board_counts(board)}")
    print("")
    print("roles:")

    if not runtime_dir.exists():
        print("- runtime directory missing")
        return

    files = sorted(runtime_dir.glob("*.json"))
    if not files:
        print("- no role runtime files yet")
        return

    for path in files:
        data = read_json(path, {})
        print(
            f"- {data.get('role', path.stem)} "
            f"status={data.get('current_status', '-')}"
            f" completion={data.get('completion', 0)}%"
            f" task={data.get('current_task', 'none')}"
            f" pending={data.get('pending_count', 0)}"
            f" age={age_text(data.get('last_seen', ''))}"
        )
        print(f"  next={data.get('next_action', '')}")
        print(f"  output={data.get('last_output_file', '')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--control-root",
        default=str(Path(__file__).resolve().parent),
        help="agent_control directory",
    )
    args = parser.parse_args()
    render_once(Path(args.control_root).resolve())


if __name__ == "__main__":
    main()
