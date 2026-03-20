#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any


current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent

project_root = current.parent
if str(current) not in sys.path:
    sys.path.insert(0, str(current))

from system.CAD_core import inspect_cad_runtime


CHECK_INTERVAL = 8
HEARTBEAT_INTERVAL = 60
WARN_STREAK = 2
CRITICAL_STREAK = 4

SYSTEM_DIR = current / "system"
CONTROL_ROOT = project_root / "dwg_agents_ops" / "agent_control"
RUNTIME_DIR = CONTROL_ROOT / "runtime"
EVENTS_PATH = CONTROL_ROOT / "runtime_events.jsonl"
LOG_FILE = SYSTEM_DIR / "cad_runtime_guard.log"
LOCK_FILE = SYSTEM_DIR / "cad_runtime_guard.lock"
STATE_FILE = RUNTIME_DIR / "cad_runtime_guard.json"


logger = logging.getLogger("cad_runtime_guard")
logger.setLevel(logging.INFO)
logger.handlers = []
formatter = logging.Formatter("%(asctime)s %(levelname)-5s %(message)s")

file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def ensure_dirs() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)


def is_already_running() -> bool:
    if not LOCK_FILE.exists():
        return False
    try:
        pid = int(LOCK_FILE.read_text(encoding="utf-8").strip())
        if pid and pid != os.getpid():
            import psutil

            if psutil.pid_exists(pid):
                proc = psutil.Process(pid)
                cmdline = " ".join(proc.cmdline()).lower()
                if "cad_runtime_guard" in cmdline and "python" in proc.name().lower():
                    return True
    except Exception:
        pass
    LOCK_FILE.unlink(missing_ok=True)
    return False


def create_lock() -> None:
    LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")


def remove_lock() -> None:
    LOCK_FILE.unlink(missing_ok=True)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_event(payload: dict[str, Any]) -> None:
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def classify_action(status: str, streak: int) -> tuple[str, str]:
    if status == "healthy_tarch":
        return "info", "none"
    if status in {"no_active_cad"}:
        return "info", "observe"
    if status in {"cad_busy", "cad_doc_unavailable", "runtime_uncertain"}:
        if streak >= WARN_STREAK:
            return "warning", "pause_and_verify"
        return "info", "observe"
    if status == "suspected_plain_cad":
        if streak >= CRITICAL_STREAK:
            return "critical", "pause_and_recover"
        if streak >= WARN_STREAK:
            return "warning", "pause_and_verify"
        return "warning", "observe"
    return "warning", "observe"


def build_state(snapshot: dict[str, Any], streak: int, previous_status: str) -> dict[str, Any]:
    severity, recommended_action = classify_action(snapshot["status"], streak)
    code = snapshot["status"].upper()
    if snapshot["status"] == "healthy_tarch" and previous_status not in {"", "healthy_tarch"}:
        code = "RUNTIME_RECOVERED"
        recommended_action = "resume_allowed"
        severity = "info"

    state = {
        "role": "cad_runtime_guard",
        "current_status": snapshot["status"],
        "completion": 100 if snapshot["status"] == "healthy_tarch" else 0,
        "current_task": "passive_runtime_monitoring",
        "pending_count": max(streak - 1, 0),
        "next_action": recommended_action,
        "last_output_file": str(EVENTS_PATH),
        "last_seen": now_iso(),
        "severity": severity,
        "code": code,
        "recommended_action": recommended_action,
        "suspicious_streak": streak,
        "probe": snapshot,
    }
    return state


def should_emit_event(current: dict[str, Any], previous: dict[str, Any]) -> bool:
    if not previous:
        return True
    watched = (
        "current_status",
        "severity",
        "recommended_action",
        "code",
    )
    for key in watched:
        if current.get(key) != previous.get(key):
            return True
    return False


def monitor_loop() -> None:
    ensure_dirs()
    previous_state = read_json(STATE_FILE, {})
    previous_status = str(previous_state.get("current_status", ""))
    suspicious_streak = 0
    last_heartbeat = 0.0

    logger.info("cad_runtime_guard 启动，进入被动监测循环。")

    while True:
        snapshot = inspect_cad_runtime()
        status = str(snapshot.get("status", "unknown"))

        if status in {"suspected_plain_cad", "runtime_uncertain", "cad_busy", "cad_doc_unavailable"}:
            suspicious_streak += 1
        else:
            suspicious_streak = 0

        state = build_state(snapshot, suspicious_streak, previous_status)
        write_json(STATE_FILE, state)

        if should_emit_event(state, previous_state):
            event = {
                "timestamp": state["last_seen"],
                "source": "cad_runtime_guard",
                "target": "execution_agents",
                "severity": state["severity"],
                "code": state["code"],
                "message": snapshot.get("reason", ""),
                "recommended_action": state["recommended_action"],
                "status": state["current_status"],
                "suspicious_streak": suspicious_streak,
                "doc_name": snapshot.get("doc_name", ""),
                "pid": snapshot.get("pid", 0),
                "process_hint": snapshot.get("process_hint", "unknown"),
            }
            append_event(event)
            logger.info(
                f"状态变更 status={state['current_status']} severity={state['severity']} "
                f"action={state['recommended_action']} streak={suspicious_streak}"
            )

        previous_state = state
        previous_status = state["current_status"]

        now = time.time()
        if now - last_heartbeat >= HEARTBEAT_INTERVAL:
            logger.info(
                f"heartbeat status={state['current_status']} severity={state['severity']} "
                f"doc={snapshot.get('doc_name', '') or '-'} pid={snapshot.get('pid', 0)}"
            )
            last_heartbeat = now

        time.sleep(CHECK_INTERVAL)


def run_once() -> int:
    ensure_dirs()
    snapshot = inspect_cad_runtime()
    state = build_state(snapshot, 0, "")
    write_json(STATE_FILE, state)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="只执行一次检测并打印 JSON")
    args = parser.parse_args()

    if args.once:
        return run_once()

    if is_already_running():
        print("[警告] cad_runtime_guard 已在运行，无需重复启动")
        return 0

    create_lock()
    try:
        monitor_loop()
    except KeyboardInterrupt:
        logger.info("收到中断信号，正常退出")
        return 0
    finally:
        remove_lock()
        logger.info("cad_runtime_guard 已停止")


if __name__ == "__main__":
    raise SystemExit(main())
