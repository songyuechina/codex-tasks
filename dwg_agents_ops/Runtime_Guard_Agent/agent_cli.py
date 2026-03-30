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
from system.CAD_core import inspect_cad_runtime, litz


CONTROL_ROOT = ROOT / "agent_control"
RUNTIME_DIR = CONTROL_ROOT / "runtime"
STATE_PATH = RUNTIME_DIR / "runtime_guard_agent.json"
DECISION_LOG = CONTROL_ROOT / "runtime_guard_decisions.jsonl"
LOCK_FILE = Path(__file__).resolve().with_name("runtime_guard_agent.lock")

CHECK_INTERVAL = 5
HEARTBEAT_INTERVAL = 60
RECOVERY_COOLDOWN_SECONDS = 90
RECOVERY_WAIT_TIMEOUT = 90
RECOVERY_POLL_INTERVAL = 3


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


def _default_auto_recovery(previous: dict | None = None) -> dict:
    previous = previous or {}
    return {
        "enabled": int(previous.get("enabled", 1)),
        "attempt_count": int(previous.get("attempt_count", 0)),
        "last_attempt_at": str(previous.get("last_attempt_at", "")),
        "last_attempt_epoch": float(previous.get("last_attempt_epoch", 0.0) or 0.0),
        "last_result": str(previous.get("last_result", "idle")),
        "last_reason": str(previous.get("last_reason", "")),
        "last_before_status": str(previous.get("last_before_status", "")),
        "last_after_status": str(previous.get("last_after_status", "")),
        "last_recovered_pid": int(previous.get("last_recovered_pid", 0) or 0),
    }


def _wait_for_guard_recovered(timeout: int = RECOVERY_WAIT_TIMEOUT) -> tuple[bool, object]:
    deadline = time.time() + max(timeout, 1)
    last_decision = decide_runtime_guard("runtime_guard_agent:post_recovery_probe")
    while time.time() < deadline:
        last_decision = decide_runtime_guard("runtime_guard_agent:post_recovery_probe")
        if last_decision.status == "healthy_tarch" and last_decision.decision not in {
            ACTION_PAUSE_VERIFY,
            ACTION_PAUSE_RECOVER,
        }:
            return True, last_decision
        time.sleep(RECOVERY_POLL_INTERVAL)
    return False, last_decision


def _maybe_auto_recover(payload: dict, *, auto_recover: bool, previous: dict | None = None) -> dict:
    recovery = _default_auto_recovery((previous or {}).get("auto_recovery"))
    recovery["enabled"] = int(auto_recover)
    payload["auto_recovery"] = recovery
    if not auto_recover:
        return payload

    if payload.get("guard_decision") != ACTION_PAUSE_RECOVER:
        return payload
    if payload.get("guard_status") != "suspected_plain_cad":
        return payload

    now_epoch = time.time()
    last_attempt_epoch = float(recovery.get("last_attempt_epoch", 0.0) or 0.0)
    if last_attempt_epoch and now_epoch - last_attempt_epoch < RECOVERY_COOLDOWN_SECONDS:
        recovery["last_result"] = "cooldown_active"
        recovery["last_reason"] = f"cooldown<{RECOVERY_COOLDOWN_SECONDS}s"
        payload["auto_recovery"] = recovery
        return payload

    before_snapshot = inspect_cad_runtime()
    recovery["attempt_count"] = int(recovery.get("attempt_count", 0)) + 1
    recovery["last_attempt_at"] = now_iso()
    recovery["last_attempt_epoch"] = now_epoch
    recovery["last_before_status"] = str(before_snapshot.get("status", "unknown"))
    recovery["last_recovered_pid"] = int(before_snapshot.get("pid", 0) or 0)
    recovery["last_result"] = "running"
    recovery["last_reason"] = "pause_and_recover_for_plain_cad"
    payload["auto_recovery"] = recovery

    print(
        "[runtime_guard_agent] auto_recovery start "
        f"status={payload['guard_status']} pid={recovery['last_recovered_pid']}"
    )
    litz_ok = bool(litz())
    recovered_ok = False
    final_decision = decide_runtime_guard("runtime_guard_agent:post_recovery_probe")
    if litz_ok:
        recovered_ok, final_decision = _wait_for_guard_recovered()

    after_snapshot = inspect_cad_runtime()
    recovery["last_after_status"] = str(after_snapshot.get("status", "unknown"))
    recovery["last_recovered_pid"] = int(after_snapshot.get("pid", 0) or 0)
    recovery["last_result"] = "recovered" if recovered_ok else "failed"
    recovery["last_reason"] = (
        "healthy_tarch_restored"
        if recovered_ok
        else f"litz_ok={int(litz_ok)} after_status={after_snapshot.get('status', 'unknown')}"
    )
    payload["auto_recovery"] = recovery

    if recovered_ok:
        payload["current_status"] = "monitoring"
        payload["completion"] = 100
        payload["next_action"] = "continue_monitoring"
        payload["severity"] = final_decision.severity
        payload["recommended_action"] = final_decision.recommended_action
        payload["guard_decision"] = final_decision.decision
        payload["guard_status"] = final_decision.status
        payload["manager_notice_required"] = 0
        payload["execution_notice_required"] = 0
        payload["message"] = (
            "检测到 suspected_plain_cad 后已执行本地恢复，当前环境已回到 healthy_tarch。"
        )
        payload["decision"] = final_decision.to_dict()
    else:
        payload["message"] = (
            "检测到 suspected_plain_cad 并已尝试本地恢复，但尚未确认回到 healthy_tarch。"
        )
    return payload


def build_payload(checkpoint: str = "runtime_guard_agent:watch", *, auto_recover: bool = True, previous: dict | None = None) -> dict:
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
    return _maybe_auto_recover(payload, auto_recover=auto_recover, previous=previous)


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


def monitor_loop(*, auto_recover: bool) -> int:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    previous = {}
    last_heartbeat = 0.0
    while True:
        payload = build_payload(auto_recover=auto_recover, previous=previous)
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
                    "auto_recovery": payload.get("auto_recovery", {}),
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
    parser.add_argument("--no-auto-recover", action="store_true", help="只做监督，不对 suspected_plain_cad 执行本地恢复")
    args = parser.parse_args()

    if args.once:
        return run_once()

    if is_already_running():
        print("[警告] runtime_guard_agent 已在运行，无需重复启动")
        return 0

    create_lock()
    try:
        return monitor_loop(auto_recover=not args.no_auto_recover)
    except KeyboardInterrupt:
        print("[runtime_guard_agent] exit")
        return 0
    finally:
        remove_lock()


if __name__ == "__main__":
    raise SystemExit(main())
