#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lightweight runtime supervisor for guarded CAD function tests.

Scope:
- watch CAD process count during a test window
- verify cad_dialog_killer is already running
- fail fast when the runtime drifts outside the allowed envelope

This script is intentionally passive. It does not start CAD and does not repair
the runtime. It only observes and reports.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import psutil


current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent

if str(current) not in sys.path:
    sys.path.insert(0, str(current))

from system.CAD_core import collect_cad_process_inventory


SYSTEM_DIR = current / "system"
LOG_DIR = SYSTEM_DIR / "logs" / "test-supervisor"
LOG_FILE = LOG_DIR / "cad_test_supervisor.jsonl"
PID_FILE = LOG_DIR / "cad_test_supervisor.pid"
KILLER_LOCK = SYSTEM_DIR / "cad_dialog_killer.lock"


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def append_log(payload: dict[str, Any]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def read_dialog_killer_state() -> dict[str, Any]:
    payload: dict[str, Any] = {
        "lock_exists": KILLER_LOCK.exists(),
        "pid": 0,
        "running": False,
        "cmdline": "",
        "error": "",
    }
    if not KILLER_LOCK.exists():
        return payload

    try:
        raw = KILLER_LOCK.read_text(encoding="utf-8", errors="ignore").strip("\x00\r\n\t ")
        if not raw:
            payload["error"] = "empty_or_null_lock"
            return payload
        pid = int(raw)
        payload["pid"] = pid
        if psutil.pid_exists(pid):
            proc = psutil.Process(pid)
            payload["running"] = True
            payload["cmdline"] = " ".join(proc.cmdline())
    except Exception as exc:
        payload["error"] = str(exc)
    return payload


def build_snapshot(*, max_cad_processes: int) -> dict[str, Any]:
    cad_rows = collect_cad_process_inventory()
    killer = read_dialog_killer_state()
    ok = len(cad_rows) <= max_cad_processes and killer.get("running", False)
    violations: list[str] = []
    if len(cad_rows) > max_cad_processes:
        violations.append(f"cad_process_count_exceeded:{len(cad_rows)}>{max_cad_processes}")
    if not killer.get("running", False):
        violations.append("cad_dialog_killer_not_running")
    return {
        "timestamp": now_iso(),
        "ok": ok,
        "max_cad_processes": max_cad_processes,
        "cad_process_count": len(cad_rows),
        "cad_processes": cad_rows,
        "cad_dialog_killer": killer,
        "violations": violations,
    }


def run_once(*, max_cad_processes: int) -> int:
    snapshot = build_snapshot(max_cad_processes=max_cad_processes)
    append_log(snapshot)
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0 if snapshot["ok"] else 2


def monitor_loop(*, max_cad_processes: int, interval_sec: float, duration_sec: float | None) -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    deadline = time.time() + duration_sec if duration_sec and duration_sec > 0 else None

    try:
        while True:
            snapshot = build_snapshot(max_cad_processes=max_cad_processes)
            append_log(snapshot)
            if not snapshot["ok"]:
                print(json.dumps(snapshot, ensure_ascii=False, indent=2))
                return 2
            if deadline is not None and time.time() >= deadline:
                return 0
            time.sleep(max(interval_sec, 0.2))
    finally:
        PID_FILE.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="只采样一次并打印 JSON")
    parser.add_argument("--max-cad-processes", type=int, default=2, help="允许的最大 CAD 进程数")
    parser.add_argument("--interval", type=float, default=1.0, help="连续监控时的采样间隔秒数")
    parser.add_argument("--duration", type=float, default=0.0, help="连续监控时长；0 表示一直监控")
    args = parser.parse_args()

    if args.once:
        return run_once(max_cad_processes=args.max_cad_processes)
    duration = args.duration if args.duration > 0 else None
    return monitor_loop(
        max_cad_processes=args.max_cad_processes,
        interval_sec=args.interval,
        duration_sec=duration,
    )


if __name__ == "__main__":
    raise SystemExit(main())
