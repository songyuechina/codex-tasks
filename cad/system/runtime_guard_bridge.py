#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent

PROJECT_ROOT = current.parent
CONTROL_ROOT = PROJECT_ROOT / "dwg_agents_ops" / "agent_control"
RUNTIME_DIR = CONTROL_ROOT / "runtime"
STATE_PATH = RUNTIME_DIR / "cad_runtime_guard.json"
EVENTS_PATH = CONTROL_ROOT / "runtime_events.jsonl"

ACTION_CONTINUE = "continue"
ACTION_PAUSE_VERIFY = "pause_and_verify"
ACTION_PAUSE_RECOVER = "pause_and_recover"
ACTION_RESUME = "resume_allowed"

DEFAULT_EVENT_TARGETS = {"execution_agents", "print_execution", "print_agent", "all"}


@dataclass
class RuntimeGuardDecision:
    checkpoint: str
    decision: str
    severity: str
    recommended_action: str
    status: str
    message: str
    state: dict[str, Any]
    event: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "checkpoint": self.checkpoint,
            "decision": self.decision,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "status": self.status,
            "message": self.message,
            "state": self.state,
            "event": self.event,
        }


class RuntimeGuardTriggered(RuntimeError):
    def __init__(self, decision: RuntimeGuardDecision):
        self.decision = decision
        payload = decision.to_dict()
        super().__init__(json.dumps(payload, ensure_ascii=False))


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _read_jsonl(path: Path, limit: int = 80) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    if limit > 0:
        return rows[-limit:]
    return rows


def _parse_ts(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        try:
            if value.endswith("Z"):
                return datetime.fromisoformat(value[:-1] + "+00:00")
        except Exception:
            return None
    return None


def _is_recent(value: str, max_age_seconds: int) -> bool:
    if max_age_seconds <= 0:
        return True
    ts = _parse_ts(value)
    if ts is None:
        return False
    now = datetime.now(timezone.utc).astimezone()
    return (now - ts).total_seconds() <= max_age_seconds


def read_runtime_guard_state(path: Path | None = None) -> dict[str, Any]:
    return _read_json(path or STATE_PATH, {})


def read_runtime_guard_events(path: Path | None = None, limit: int = 80) -> list[dict[str, Any]]:
    return _read_jsonl(path or EVENTS_PATH, limit=limit)


def _target_matches(event: dict[str, Any], targets: set[str]) -> bool:
    raw = str(event.get("target", "")).strip().lower()
    if not raw:
        return False
    return raw in {item.lower() for item in targets}


def latest_runtime_guard_event(
    *,
    path: Path | None = None,
    limit: int = 80,
    max_age_seconds: int = 600,
    targets: set[str] | None = None,
) -> dict[str, Any]:
    wanted = targets or DEFAULT_EVENT_TARGETS
    for event in reversed(read_runtime_guard_events(path, limit=limit)):
        if not _target_matches(event, wanted):
            continue
        if max_age_seconds > 0 and not _is_recent(str(event.get("timestamp", "")), max_age_seconds):
            continue
        return event
    return {}


def decide_runtime_guard(
    checkpoint: str,
    *,
    state_path: Path | None = None,
    events_path: Path | None = None,
    max_event_age_seconds: int = 600,
) -> RuntimeGuardDecision:
    state = read_runtime_guard_state(state_path)
    event = latest_runtime_guard_event(
        path=events_path,
        max_age_seconds=max_event_age_seconds,
    )

    status = str(state.get("current_status") or state.get("probe", {}).get("status") or "unknown")
    severity = str(event.get("severity") or state.get("severity") or "info")
    recommended_action = str(event.get("recommended_action") or state.get("recommended_action") or "none")
    message = str(event.get("message") or state.get("probe", {}).get("reason") or "")

    decision = ACTION_CONTINUE
    if recommended_action == ACTION_PAUSE_RECOVER or severity == "critical":
        decision = ACTION_PAUSE_RECOVER
    elif recommended_action == ACTION_PAUSE_VERIFY or severity == "warning":
        decision = ACTION_PAUSE_VERIFY
    elif recommended_action == ACTION_RESUME:
        decision = ACTION_RESUME

    if status in {"suspected_plain_cad"} and decision == ACTION_CONTINUE:
        decision = ACTION_PAUSE_VERIFY
        recommended_action = ACTION_PAUSE_VERIFY
        severity = "warning"
    if status in {"cad_doc_unavailable"} and decision == ACTION_CONTINUE:
        decision = ACTION_PAUSE_VERIFY
        recommended_action = ACTION_PAUSE_VERIFY
        severity = "warning"

    return RuntimeGuardDecision(
        checkpoint=checkpoint,
        decision=decision,
        severity=severity,
        recommended_action=recommended_action,
        status=status,
        message=message,
        state=state,
        event=event,
    )


def assert_runtime_guard_ok(
    checkpoint: str,
    *,
    state_path: Path | None = None,
    events_path: Path | None = None,
    max_event_age_seconds: int = 600,
    transient_retry_count: int = 10,
    transient_retry_delay: float = 3.0,
) -> RuntimeGuardDecision:
    attempt = 0
    while True:
        decision = decide_runtime_guard(
            checkpoint,
            state_path=state_path,
            events_path=events_path,
            max_event_age_seconds=max_event_age_seconds,
        )
        if decision.decision not in {ACTION_PAUSE_VERIFY, ACTION_PAUSE_RECOVER}:
            return decision

        if (
            decision.status in {"cad_busy", "cad_doc_unavailable"}
            and decision.decision == ACTION_PAUSE_VERIFY
            and attempt < transient_retry_count
        ):
            attempt += 1
            time.sleep(max(transient_retry_delay, 0.1))
            continue

        raise RuntimeGuardTriggered(decision)


def render_guard_error(exc: RuntimeGuardTriggered) -> dict[str, Any]:
    return {
        "error": "runtime_guard_triggered",
        **exc.decision.to_dict(),
    }
