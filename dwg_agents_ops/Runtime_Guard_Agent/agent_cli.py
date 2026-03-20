#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
CAD_ROOT = PROJECT_ROOT / "cad"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(CAD_ROOT) not in sys.path:
    sys.path.insert(0, str(CAD_ROOT))

from system.runtime_guard_bridge import ACTION_PAUSE_RECOVER, ACTION_PAUSE_VERIFY, decide_runtime_guard


CONTROL_ROOT = ROOT / "agent_control"
RUNTIME_DIR = CONTROL_ROOT / "runtime"
STATE_PATH = RUNTIME_DIR / "runtime_guard_agent.json"
DECISION_LOG = CONTROL_ROOT / "runtime_guard_decisions.jsonl"
LOCK_FILE = Path(__file__).resolve().with_name("runtime_guard_agent.lock")

CHECK_INTERVAL = 5
HEARTBEAT_INTERVAL = 60


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


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
                if "runtime_guard_agent" in cmdline and "python" in proc.name().lower():
                    return True
    except Exception:
        pass
    LOCK_FILE.unlink(missing_ok=True)
    return False


def create_lock() -> None:
    LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")


def remove_lock() -> None:
    LOCK_FILE.unlink(missing_ok=True)


def build_payload(checkpoint: str = "runtime_guard_agent:watch") -> dict:
    decision = decide_runtime_guard(checkpoint)
    manager_notice = int(decision.decision in {ACTION_PAUSE_VERIFY, ACTION_PAUSE_RECOVER})
    execution_notice = manager_notice
    current_status = "alerting" if manager_notice else "monitoring"
    next_action = "notify_and_wait"
    if decision.decision == ACTION_PAUSE_RECOVER:
        next_action = "notify_project_manager_and_execution_agent"
    elif decision.decision == ACTION_PAUSE_VERIFY:
        next_action = "notify_execution_agent"

    payload = {
        "role": "runtime_guard_agent",
        "current_status": current_status,
        "completion": 100 if not manager_notice else 0,
        "current_task": "event_driven_runtime_supervision",
        "pending_count": 0,
        "next_action": next_action,
        "last_output_file": str(DECISION_LOG),
        "last_seen": now_iso(),
        "severity": decision.severity,
        "recommended_action": decision.recommended_action,
        "guard_decision": decision.decision,
        "guard_status": decision.status,
        "manager_notice_required": manager_notice,
        "execution_notice_required": execution_notice,
        "message": decision.message,
        "decision": decision.to_dict(),
    }
    return payload


def should_emit(current: dict, previous: dict) -> bool:
    if not previous:
        return True
    keys = (
        "current_status",
        "severity",
        "recommended_action",
        "guard_decision",
        "guard_status",
        "manager_notice_required",
        "execution_notice_required",
    )
    return any(current.get(key) != previous.get(key) for key in keys)


def run_once() -> int:
    payload = build_payload("runtime_guard_agent:once")
    write_json(STATE_PATH, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def monitor_loop() -> int:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    previous = {}
    last_heartbeat = 0.0
    while True:
        payload = build_payload()
        write_json(STATE_PATH, payload)
        if should_emit(payload, previous):
            append_jsonl(
                DECISION_LOG,
                {
                    "timestamp": payload["last_seen"],
                    "source": "runtime_guard_agent",
                    "severity": payload["severity"],
                    "guard_decision": payload["guard_decision"],
                    "recommended_action": payload["recommended_action"],
                    "guard_status": payload["guard_status"],
                    "manager_notice_required": payload["manager_notice_required"],
                    "execution_notice_required": payload["execution_notice_required"],
                    "message": payload["message"],
                },
            )
            print(
                f"[runtime_guard_agent] status={payload['guard_status']} "
                f"decision={payload['guard_decision']} severity={payload['severity']}"
            )
        previous = payload
        now = time.time()
        if now - last_heartbeat >= HEARTBEAT_INTERVAL:
            print(
                f"[runtime_guard_agent] heartbeat status={payload['guard_status']} "
                f"decision={payload['guard_decision']}"
            )
            last_heartbeat = now
        time.sleep(CHECK_INTERVAL)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="只读取当前运行守护状态并输出 JSON")
    args = parser.parse_args()

    if args.once:
        return run_once()

    if is_already_running():
        print("[警告] runtime_guard_agent 已在运行，无需重复启动")
        return 0

    create_lock()
    try:
        return monitor_loop()
    except KeyboardInterrupt:
        print("[runtime_guard_agent] exit")
        return 0
    finally:
        remove_lock()


if __name__ == "__main__":
    raise SystemExit(main())
