#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
import tomllib


MAX_FILE_CHARS_DEFAULT = 16000

ROLE_STATUS_FILTER = {
    "planner": {
        "backlog",
        "ready_for_planning",
        "planning",
        "planned",
        "replan_requested",
        "blocked",
        "stale",
    },
    "coder": {
        "planned",
        "backlog",
        "ready_for_coding",
        "coding",
        "coded",
        "review_failed",
        "test_failed",
        "blocked",
        "stale",
    },
    "reviewer": {
        "coded",
        "reviewing",
        "review_failed",
        "review_passed",
        "blocked",
    },
    "tester": {
        "review_passed",
        "testing",
        "test_failed",
        "test_passed",
        "blocked",
    },
}

WAITING_DEFAULT = {
    "planner": "waiting_on_task",
    "coder": "waiting_on_task",
    "reviewer": "waiting_on_review_target",
    "tester": "waiting_on_review",
}

PROGRESS_RE = re.compile(
    r"^\[PROGRESS\]\s*task=(.*?);\s*status=(.*?);\s*completion=(\d{1,3});\s*next=(.*)$",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass
class RoleConfig:
    id: str
    name: str
    description: str
    system_prompt: str
    api_key_env: str
    base_url_env: str
    model_env: str
    allow_global_fallback: bool
    require_explicit_provider: bool
    supports_system_role: bool


@dataclass
class AgentPaths:
    role_dir: Path
    ops_root: Path
    project_root: Path
    role_path: Path
    sessions_dir: Path
    outputs_dir: Path
    memory_dir: Path
    state_path: Path
    summary_path: Path
    session_path: Path
    timeline_path: Path
    task_board_path: Path
    runtime_dir: Path
    local_config_path: Path


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


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


def load_role_config(role_path: Path) -> RoleConfig:
    raw = tomllib.loads(role_path.read_text(encoding="utf-8"))
    role = raw["role"]
    return RoleConfig(
        id=role["id"],
        name=role["name"],
        description=role["description"],
        system_prompt=role["system_prompt"].strip(),
        api_key_env=role["api_key_env"],
        base_url_env=role["base_url_env"],
        model_env=role["model_env"],
        allow_global_fallback=bool(role.get("allow_global_fallback", False)),
        require_explicit_provider=bool(role.get("require_explicit_provider", True)),
        supports_system_role=bool(role.get("supports_system_role", True)),
    )


def build_paths(role_path: Path) -> AgentPaths:
    role_dir = role_path.resolve().parent
    ops_root = role_dir.parent
    project_root = ops_root.parent
    memory_dir = role_dir / "memory"
    sessions_dir = role_dir / "sessions"
    outputs_dir = role_dir / "outputs"
    control_root = ops_root / "agent_control"
    return AgentPaths(
        role_dir=role_dir,
        ops_root=ops_root,
        project_root=project_root,
        role_path=role_path.resolve(),
        sessions_dir=sessions_dir,
        outputs_dir=outputs_dir,
        memory_dir=memory_dir,
        state_path=memory_dir / "state.json",
        summary_path=memory_dir / "rolling_summary.md",
        session_path=sessions_dir / "session.jsonl",
        timeline_path=memory_dir / "timeline.jsonl",
        task_board_path=control_root / "task_board.json",
        runtime_dir=control_root / "runtime",
        local_config_path=ops_root / "local" / "agents.local.toml",
    )


def ensure_layout(paths: AgentPaths) -> None:
    paths.memory_dir.mkdir(parents=True, exist_ok=True)
    paths.sessions_dir.mkdir(parents=True, exist_ok=True)
    paths.outputs_dir.mkdir(parents=True, exist_ok=True)
    paths.runtime_dir.mkdir(parents=True, exist_ok=True)
    if not paths.task_board_path.exists():
        write_json(
            paths.task_board_path,
            {
                "active_plan_version": None,
                "plans": [],
                "tasks": [],
                "waiting_queues": WAITING_DEFAULT,
            },
        )


def load_local_provider_config(paths: AgentPaths) -> dict[str, Any]:
    if not paths.local_config_path.exists():
        return {}
    try:
        return tomllib.loads(paths.local_config_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def env_first(*names: str) -> Optional[str]:
    for name in names:
        if not name:
            continue
        value = os.getenv(name)
        if value:
            return value
    return None


def mask_secret(value: str) -> str:
    if len(value) <= 8:
        return "*" * len(value)
    return value[:4] + "*" * (len(value) - 8) + value[-4:]


def resolve_provider_config(
    role_cfg: RoleConfig,
    paths: AgentPaths,
    model_override: Optional[str],
) -> tuple[dict[str, str], dict[str, str]]:
    local_cfg = load_local_provider_config(paths)
    role_local = local_cfg.get(role_cfg.id, {}) if isinstance(local_cfg, dict) else {}
    resolved: dict[str, str] = {}
    source: dict[str, str] = {}

    def pick(field: str, env_name: str, global_envs: tuple[str, ...] = ()) -> None:
        if field in role_local and role_local[field]:
            resolved[field] = str(role_local[field])
            source[field] = f"local:{paths.local_config_path}"
            return
        env_value = env_first(env_name)
        if env_value:
            resolved[field] = env_value
            source[field] = f"env:{env_name}"
            return
        if role_cfg.allow_global_fallback:
            fallback = env_first(*global_envs)
            if fallback:
                resolved[field] = fallback
                source[field] = "env:global"

    pick("base_url", role_cfg.base_url_env, ("OPENAI_BASE_URL", "OPENAI_API_BASE"))
    pick("api_key", role_cfg.api_key_env, ("OPENAI_API_KEY",))
    pick("model", role_cfg.model_env, ("OPENAI_MODEL",))

    if model_override:
        resolved["model"] = model_override
        source["model"] = "cli:--model"

    missing = [name for name in ("base_url", "api_key", "model") if not resolved.get(name)]
    if missing:
        lines = [
            f"Missing provider config for role '{role_cfg.id}': {', '.join(missing)}",
            f"Expected local config: {paths.local_config_path}",
            "Expected env vars:",
            f"- {role_cfg.base_url_env}",
            f"- {role_cfg.api_key_env}",
            f"- {role_cfg.model_env}",
        ]
        if role_cfg.allow_global_fallback:
            lines.append("Global fallback is enabled for this role.")
        else:
            lines.append("Global fallback is disabled for this role.")
        raise RuntimeError("\n".join(lines))

    if role_cfg.require_explicit_provider:
        for field in ("base_url", "api_key", "model"):
            if source.get(field) == "env:global":
                raise RuntimeError(
                    f"Role '{role_cfg.id}' must use dedicated provider config, but {field} fell back to a global env."
                )

    return resolved, source


def load_history(session_path: Path, limit_turns: int) -> list[dict[str, str]]:
    if not session_path.exists():
        return []
    items = []
    for line in session_path.read_text(encoding="utf-8").splitlines():
        try:
            items.append(json.loads(line))
        except Exception:
            continue
    if limit_turns > 0:
        items = items[-(limit_turns * 2) :]
    return [{"role": item["role"], "content": item["content"]} for item in items]


def append_session(session_path: Path, role: str, content: str) -> None:
    session_path.parent.mkdir(parents=True, exist_ok=True)
    record = {"role": role, "content": content, "timestamp": now_iso()}
    with session_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def append_timeline(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def expand_file_macros(text: str, project_root: Path) -> str:
    max_chars = int(os.getenv("DWG_AGENT_MAX_FILE_CHARS", str(MAX_FILE_CHARS_DEFAULT)))
    lines = text.splitlines()
    kept: list[str] = []
    appended: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("@file "):
            raw = stripped[6:].strip().strip("\"")
            path = Path(raw)
            if not path.is_absolute():
                path = project_root / raw
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                appended.append(f"\n[file: {path}]\n{content[:max_chars]}\n")
            except Exception as exc:
                appended.append(f"\n[file read failed: {path}] {exc}\n")
        else:
            kept.append(line)
    base = "\n".join(kept)
    if appended:
        return base + "\n" + "\n".join(appended)
    return base


def load_task_board(path: Path) -> dict[str, Any]:
    return read_json(path, {"active_plan_version": None, "plans": [], "tasks": [], "waiting_queues": WAITING_DEFAULT})


def save_task_board(path: Path, board: dict[str, Any]) -> None:
    write_json(path, board)


def board_status_counts(board: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for task in board.get("tasks", []):
        status = task.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts


def role_pending_tasks(role_id: str, board: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = board.get("tasks", [])
    allowed = ROLE_STATUS_FILTER.get(role_id, set())
    pending = [task for task in tasks if task.get("status") in allowed]
    pending.sort(key=lambda item: (item.get("priority", "z"), item.get("task_id", "")))
    return pending


def set_task_status(board: dict[str, Any], role_id: str, task_id: str, new_status: str) -> tuple[bool, str]:
    for task in board.get("tasks", []):
        if str(task.get("task_id", "")).lower() != task_id.lower():
            continue
        task["status"] = new_status
        task["owner"] = role_id
        task["updated_at"] = now_iso()
        return True, f"{task_id} -> {new_status}"
    return False, "task not found"


def load_state(paths: AgentPaths, role_cfg: RoleConfig) -> dict[str, Any]:
    default = {
        "role": role_cfg.id,
        "name": role_cfg.name,
        "started_at": now_iso(),
        "last_seen": "",
        "turn_count": 0,
        "current_task": "none",
        "current_status": "idle",
        "completion": 0,
        "next_action": "",
        "last_user": "",
        "last_output": "",
        "last_output_file": "",
        "pending_task_ids": [],
    }
    data = read_json(paths.state_path, default)
    for key, value in default.items():
        data.setdefault(key, value)
    return data


def save_state(paths: AgentPaths, state: dict[str, Any]) -> None:
    write_json(paths.state_path, state)


def load_summary(paths: AgentPaths) -> str:
    if not paths.summary_path.exists():
        return ""
    return paths.summary_path.read_text(encoding="utf-8", errors="ignore").strip()


def save_summary(paths: AgentPaths, text: str) -> None:
    paths.summary_path.parent.mkdir(parents=True, exist_ok=True)
    paths.summary_path.write_text(text.strip() + "\n", encoding="utf-8")


def build_summary(
    role_cfg: RoleConfig,
    state: dict[str, Any],
    board: dict[str, Any],
    pending_tasks: list[dict[str, Any]],
) -> str:
    top_pending = ", ".join([task.get("task_id", "") for task in pending_tasks[:6]]) or "none"
    return "\n".join(
        [
            f"# {role_cfg.name} Rolling Summary",
            f"- role: {role_cfg.id}",
            f"- current_task: {state.get('current_task', 'none')}",
            f"- current_status: {state.get('current_status', 'idle')}",
            f"- completion: {state.get('completion', 0)}%",
            f"- next_action: {state.get('next_action', '')}",
            f"- pending_tasks: {top_pending}",
            f"- board_status_counts: {board_status_counts(board)}",
            f"- last_seen: {state.get('last_seen', '')}",
        ]
    )


def update_runtime(
    paths: AgentPaths,
    role_cfg: RoleConfig,
    state: dict[str, Any],
    board: dict[str, Any],
    pending_tasks: list[dict[str, Any]],
) -> None:
    payload = {
        "role": role_cfg.id,
        "name": role_cfg.name,
        "pid": os.getpid(),
        "last_seen": now_iso(),
        "turn_count": state.get("turn_count", 0),
        "current_task": state.get("current_task", "none"),
        "current_status": state.get("current_status", "idle"),
        "completion": state.get("completion", 0),
        "next_action": state.get("next_action", ""),
        "pending_count": len(pending_tasks),
        "pending_task_ids": [task.get("task_id", "") for task in pending_tasks[:10]],
        "waiting": board.get("waiting_queues", {}).get(role_cfg.id, WAITING_DEFAULT.get(role_cfg.id, "")),
        "last_output_file": state.get("last_output_file", ""),
    }
    write_json(paths.runtime_dir / f"{role_cfg.id}.json", payload)


def extract_progress(reply: str) -> Optional[dict[str, Any]]:
    match = PROGRESS_RE.search(reply)
    if not match:
        return None
    completion = max(0, min(100, int(match.group(3).strip())))
    return {
        "task": match.group(1).strip(),
        "status": match.group(2).strip(),
        "completion": completion,
        "next": match.group(4).strip(),
    }


def print_progress(role_cfg: RoleConfig, state: dict[str, Any], board: dict[str, Any], pending: list[dict[str, Any]]) -> None:
    print(f"[{role_cfg.name}] turns={state.get('turn_count', 0)}")
    print(
        f"current={state.get('current_task', 'none')} "
        f"status={state.get('current_status', 'idle')} "
        f"completion={state.get('completion', 0)}%"
    )
    print(f"next={state.get('next_action', '')}")
    print(f"pending({len(pending)}): " + ", ".join(task.get("task_id", "?") for task in pending[:8]))
    print(f"board_counts={board_status_counts(board)}")


def build_client(base_url: str, api_key: str):
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Package 'openai' is required. Install it before running role agents.") from exc
    return OpenAI(api_key=api_key, base_url=base_url, max_retries=2, timeout=60)


def chat_once(
    client: Any,
    model: str,
    supports_system_role: bool,
    system_prompt: str,
    summary_text: str,
    control_hint: str,
    history: list[dict[str, str]],
    user_text: str,
    max_tokens: int,
    temperature: float,
) -> str:
    if supports_system_role:
        messages = [{"role": "system", "content": system_prompt}]
        if summary_text:
            messages.append({"role": "system", "content": "Rolling memory:\n" + summary_text})
        if control_hint:
            messages.append({"role": "system", "content": control_hint})
        messages.extend(history)
        messages.append({"role": "user", "content": user_text})
    else:
        preface_parts = [system_prompt]
        if summary_text:
            preface_parts.append("Rolling memory:\n" + summary_text)
        if control_hint:
            preface_parts.append(control_hint)
        merged_user = (
            "Supervisor context for this role:\n"
            + "\n\n".join(part for part in preface_parts if part)
            + "\n\nUser task:\n"
            + user_text
        )
        messages = []
        messages.extend(history)
        messages.append({"role": "user", "content": merged_user})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def print_provider_config(role_cfg: RoleConfig, resolved: dict[str, str], source: dict[str, str]) -> None:
    print(f"role={role_cfg.id}")
    print(f"base_url={resolved['base_url']} ({source['base_url']})")
    print(f"model={resolved['model']} ({source['model']})")
    print(f"api_key={mask_secret(resolved['api_key'])} ({source['api_key']})")


def main_for_role(role_path: Path) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=None, help="override model name")
    parser.add_argument("--max-tokens", type=int, default=16000, help="max tokens per answer")
    parser.add_argument("--temperature", type=float, default=0.2, help="sampling temperature")
    parser.add_argument("--history", type=int, default=4, help="history turns to keep")
    parser.add_argument("--once", default=None, help="single-run prompt")
    parser.add_argument("--print-config", action="store_true", help="print resolved provider config and exit")
    args = parser.parse_args()

    paths = build_paths(role_path)
    ensure_layout(paths)
    role_cfg = load_role_config(role_path)
    resolved, source = resolve_provider_config(role_cfg, paths, args.model)

    if args.print_config:
        print_provider_config(role_cfg, resolved, source)
        return

    client = build_client(resolved["base_url"], resolved["api_key"])
    model = resolved["model"]
    history = load_history(paths.session_path, args.history)
    state = load_state(paths, role_cfg)
    board = load_task_board(paths.task_board_path)
    pending_tasks = role_pending_tasks(role_cfg.id, board)

    state["pending_task_ids"] = [task.get("task_id", "") for task in pending_tasks[:20]]
    state["last_seen"] = now_iso()
    save_state(paths, state)
    save_summary(paths, build_summary(role_cfg, state, board, pending_tasks))
    update_runtime(paths, role_cfg, state, board, pending_tasks)

    print(
        f"[{role_cfg.name}] resume: "
        f"task={state.get('current_task', 'none')} "
        f"status={state.get('current_status', 'idle')} "
        f"completion={state.get('completion', 0)}% "
        f"pending={len(pending_tasks)}"
    )
    print("commands: /progress /tasks /set <task_id> <status> /refresh /exit")

    def handle_user_input(user_text: str) -> None:
        nonlocal board, pending_tasks, history, state
        board = load_task_board(paths.task_board_path)
        pending_tasks = role_pending_tasks(role_cfg.id, board)
        control_hint = (
            f"Project root: {paths.project_root}; "
            f"pending_for_{role_cfg.id}={', '.join(task.get('task_id', '?') for task in pending_tasks[:8]) or 'none'}. "
            "Always end reply with: [PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>."
        )
        expanded = expand_file_macros(user_text, paths.project_root)
        summary_text = load_summary(paths)
        reply = chat_once(
            client=client,
            model=model,
            supports_system_role=role_cfg.supports_system_role,
            system_prompt=role_cfg.system_prompt,
            summary_text=summary_text,
            control_hint=control_hint,
            history=history,
            user_text=expanded,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
        print("\n" + reply + "\n")

        append_session(paths.session_path, "user", user_text)
        append_session(paths.session_path, "assistant", reply)
        history.extend(
            [
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": reply},
            ]
        )
        if args.history > 0 and len(history) > args.history * 2:
            history = history[-(args.history * 2) :]

        out_path = paths.outputs_dir / f"{role_cfg.id}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        out_path.write_text(reply, encoding="utf-8")

        progress = extract_progress(reply)
        if progress:
            state["current_task"] = progress["task"]
            state["current_status"] = progress["status"]
            state["completion"] = progress["completion"]
            state["next_action"] = progress["next"]

        state["turn_count"] = int(state.get("turn_count", 0)) + 1
        state["last_seen"] = now_iso()
        state["last_user"] = user_text[:1600]
        state["last_output"] = reply[:2400]
        state["last_output_file"] = str(out_path)
        state["pending_task_ids"] = [task.get("task_id", "") for task in pending_tasks[:20]]
        save_state(paths, state)

        append_timeline(
            paths.timeline_path,
            {
                "ts": now_iso(),
                "role": role_cfg.id,
                "user": user_text[:400],
                "progress": progress or {},
                "output_file": str(out_path),
            },
        )
        save_summary(paths, build_summary(role_cfg, state, board, pending_tasks))
        update_runtime(paths, role_cfg, state, board, pending_tasks)

    if args.once:
        handle_user_input(args.once)
        return

    while True:
        try:
            user_text = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nexit")
            break
        if not user_text:
            continue

        cmd = user_text.lower()
        if cmd in {"/exit", "/quit", "exit", "quit"}:
            print("exit")
            break
        if cmd in {"/progress", "/status"}:
            board = load_task_board(paths.task_board_path)
            pending_tasks = role_pending_tasks(role_cfg.id, board)
            print_progress(role_cfg, state, board, pending_tasks)
            update_runtime(paths, role_cfg, state, board, pending_tasks)
            continue
        if cmd == "/tasks":
            board = load_task_board(paths.task_board_path)
            pending_tasks = role_pending_tasks(role_cfg.id, board)
            if not pending_tasks:
                print("no pending tasks for this role")
            else:
                for task in pending_tasks[:20]:
                    print(f"- {task.get('task_id', '?')} [{task.get('status', '?')}] {task.get('title', '')}")
            update_runtime(paths, role_cfg, state, board, pending_tasks)
            continue
        if cmd.startswith("/set "):
            parts = user_text.split(maxsplit=2)
            if len(parts) < 3:
                print("usage: /set <task_id> <status>")
                continue
            board = load_task_board(paths.task_board_path)
            ok, message = set_task_status(board, role_cfg.id, parts[1], parts[2])
            if ok:
                save_task_board(paths.task_board_path, board)
            print(message)
            pending_tasks = role_pending_tasks(role_cfg.id, board)
            state["pending_task_ids"] = [task.get("task_id", "") for task in pending_tasks[:20]]
            state["last_seen"] = now_iso()
            save_state(paths, state)
            save_summary(paths, build_summary(role_cfg, state, board, pending_tasks))
            update_runtime(paths, role_cfg, state, board, pending_tasks)
            continue
        if cmd == "/refresh":
            board = load_task_board(paths.task_board_path)
            pending_tasks = role_pending_tasks(role_cfg.id, board)
            state["pending_task_ids"] = [task.get("task_id", "") for task in pending_tasks[:20]]
            state["last_seen"] = now_iso()
            save_state(paths, state)
            save_summary(paths, build_summary(role_cfg, state, board, pending_tasks))
            update_runtime(paths, role_cfg, state, board, pending_tasks)
            print_progress(role_cfg, state, board, pending_tasks)
            continue

        handle_user_input(user_text)
