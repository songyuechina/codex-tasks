import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
import tomllib

from openai import OpenAI

AGENT_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = AGENT_ROOT.parent
ROLE_PATH = AGENT_ROOT / "role.toml"
SESSIONS_DIR = AGENT_ROOT / "sessions"
OUTPUTS_DIR = AGENT_ROOT / "outputs"
MEMORY_DIR = AGENT_ROOT / "memory"

CONTROL_ROOT = PROJECT_ROOT / "agent_control"
TASK_BOARD_PATH = CONTROL_ROOT / "task_board.json"
RUNTIME_DIR = CONTROL_ROOT / "runtime"

STATE_PATH = MEMORY_DIR / "state.json"
SUMMARY_PATH = MEMORY_DIR / "rolling_summary.md"
TIMELINE_PATH = MEMORY_DIR / "timeline.jsonl"

MAX_FILE_CHARS_DEFAULT = 12000

ROLE_STATUS_FILTER = {
    "planner": {
        "backlog",
        "ready_for_impl",
        "implementing",
        "implemented",
        "reviewing",
        "review_passed",
        "testing",
        "test_passed",
        "review_failed",
        "test_failed",
        "blocked",
        "stale",
    },
    "implementer": {"ready_for_impl", "implementing", "review_failed", "test_failed"},
    "reviewer": {"implemented", "reviewing"},
    "tester": {"review_passed", "testing"},
}

WAITING_DEFAULT = {
    "planner": "active",
    "implementer": "waiting_on_planner",
    "reviewer": "waiting_on_implementation",
    "tester": "waiting_on_review",
}

PROGRESS_RE = re.compile(
    r"^\[PROGRESS\]\s*task=(.*?);\s*status=(.*?);\s*completion=(\d{1,3});\s*next=(.*)$",
    re.IGNORECASE | re.MULTILINE,
)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_role() -> dict:
    data = tomllib.loads(ROLE_PATH.read_text(encoding="utf-8"))
    return data["role"]


def load_codex_config() -> tuple[str | None, str | None]:
    cfg_path = Path.home() / ".codex" / "config.toml"
    if not cfg_path.exists():
        return None, None
    data = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
    model = data.get("model")
    provider = data.get("model_provider")
    base_url = None
    if provider:
        providers = data.get("model_providers", {})
        provider_cfg = providers.get(provider, {})
        base_url = provider_cfg.get("base_url")
    return model, base_url


def load_codex_auth() -> str | None:
    auth_path = Path.home() / ".codex" / "auth.json"
    if not auth_path.exists():
        return None
    try:
        data = json.loads(auth_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data.get("OPENAI_API_KEY") or data.get("CC_IOASIS_API_KEY")


def load_api_config(model_override: str | None) -> tuple[str, str, str]:
    api_key = (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("CC_IOASIS_API_KEY")
        or os.getenv("OPENAI_TOKEN")
    )
    base_url = (
        os.getenv("OPENAI_BASE_URL")
        or os.getenv("OPENAI_API_BASE")
        or os.getenv("CC_IOASIS_BASE_URL")
    )
    model = os.getenv("CAD_AGENT_MODEL")

    if not model or not base_url:
        cfg_model, cfg_base = load_codex_config()
        if not model:
            model = cfg_model
        if not base_url:
            base_url = cfg_base

    if not api_key:
        api_key = load_codex_auth()

    if not model:
        model = "gpt-5.3-codex"
    if not base_url:
        base_url = "https://cc.ioasis.xyz/v1"

    if model_override:
        model = model_override

    if not api_key:
        raise RuntimeError("API key not found. Set OPENAI_API_KEY or CC_IOASIS_API_KEY.")

    return api_key, base_url, model


def load_history(session_path: Path, limit_turns: int) -> list[dict]:
    if not session_path.exists():
        return []
    lines = session_path.read_text(encoding="utf-8").splitlines()
    items = []
    for line in lines:
        try:
            items.append(json.loads(line))
        except Exception:
            continue
    if limit_turns > 0:
        items = items[-(limit_turns * 2):]
    return [{"role": i["role"], "content": i["content"]} for i in items]


def append_session(session_path: Path, role: str, content: str) -> None:
    session_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "role": role,
        "content": content,
        "timestamp": now_iso(),
    }
    with session_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def append_timeline(payload: dict) -> None:
    TIMELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TIMELINE_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def expand_file_macros(text: str, project_root: Path) -> str:
    max_chars = int(os.getenv("CAD_AGENT_MAX_FILE_CHARS", str(MAX_FILE_CHARS_DEFAULT)))
    lines = text.splitlines()
    kept = []
    appended = []
    for line in lines:
        s = line.strip()
        if s.lower().startswith("@file "):
            raw = s[6:].strip().strip("\"")
            path = Path(raw)
            if not path.is_absolute():
                path = project_root / raw
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                content = content[:max_chars]
                appended.append(f"\n[file: {path}]\n{content}\n")
            except Exception as e:
                appended.append(f"\n[file read failed: {path}] {e}\n")
        else:
            kept.append(line)
    base = "\n".join(kept)
    if appended:
        return base + "\n" + "\n".join(appended)
    return base


def load_task_board() -> dict:
    return read_json(TASK_BOARD_PATH, {})


def save_task_board(board: dict) -> None:
    write_json(TASK_BOARD_PATH, board)


def role_pending_tasks(role_id: str, board: dict) -> list[dict]:
    tasks = board.get("tasks", [])
    active_plan = board.get("active_plan_version")
    allowed = ROLE_STATUS_FILTER.get(role_id, set())
    pending = []

    for t in tasks:
        status = t.get("status", "")
        if status not in allowed:
            continue
        if role_id != "planner":
            if not active_plan:
                continue
            if t.get("plan_version") != active_plan:
                continue
        pending.append(t)

    pending.sort(key=lambda x: (x.get("priority", "z"), x.get("task_id", "")))
    return pending


def board_status_counts(board: dict) -> dict:
    counts = {}
    for t in board.get("tasks", []):
        s = t.get("status", "unknown")
        counts[s] = counts.get(s, 0) + 1
    return counts


def set_task_status(board: dict, role_id: str, task_id: str, new_status: str) -> tuple[bool, str]:
    tasks = board.get("tasks", [])
    for t in tasks:
        if str(t.get("task_id", "")).lower() != task_id.lower():
            continue
        if role_id != "planner":
            active = board.get("active_plan_version")
            if active and t.get("plan_version") != active:
                return False, "task not in active plan"
        t["status"] = new_status
        t["owner"] = role_id
        t["updated_at"] = now_iso()
        save_task_board(board)
        return True, f"{task_id} -> {new_status}"
    return False, "task not found"


def activate_plan(board: dict, role_id: str, plan_version: str) -> tuple[bool, str]:
    if role_id != "planner":
        return False, "only planner can activate plan"
    plans = board.get("plans", [])
    for p in plans:
        if str(p.get("plan_version", "")).lower() == plan_version.lower():
            board["active_plan_version"] = p.get("plan_version")
            p["status"] = "active"
            p["updated_at"] = now_iso()
            save_task_board(board)
            return True, f"active_plan_version={p.get('plan_version')}"
    return False, "plan version not found"


def load_state(role_cfg: dict) -> dict:
    default = {
        "role": role_cfg["id"],
        "name": role_cfg["name"],
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
        "active_plan_version": None,
    }
    data = read_json(STATE_PATH, default)
    for k, v in default.items():
        data.setdefault(k, v)
    return data


def save_state(state: dict) -> None:
    write_json(STATE_PATH, state)


def load_summary() -> str:
    if not SUMMARY_PATH.exists():
        return ""
    return SUMMARY_PATH.read_text(encoding="utf-8", errors="ignore").strip()


def save_summary(text: str) -> None:
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(text.strip() + "\n", encoding="utf-8")


def build_summary(role_cfg: dict, state: dict, board: dict, pending_tasks: list[dict]) -> str:
    active_plan = board.get("active_plan_version")
    status_counts = board_status_counts(board)
    top_pending = ", ".join([t.get("task_id", "") for t in pending_tasks[:6]]) or "none"
    return "\n".join(
        [
            f"# {role_cfg['name']} Rolling Summary",
            f"- role: {role_cfg['id']}",
            f"- active_plan_version: {active_plan}",
            f"- current_task: {state.get('current_task', 'none')}",
            f"- current_status: {state.get('current_status', 'idle')}",
            f"- completion: {state.get('completion', 0)}%",
            f"- next_action: {state.get('next_action', '')}",
            f"- pending_tasks_for_role: {top_pending}",
            f"- board_status_counts: {status_counts}",
            f"- last_seen: {state.get('last_seen', '')}",
        ]
    )


def extract_progress(reply: str) -> dict | None:
    m = PROGRESS_RE.search(reply)
    if not m:
        return None
    try:
        completion = int(m.group(3).strip())
    except Exception:
        completion = 0
    completion = max(0, min(100, completion))
    return {
        "task": m.group(1).strip(),
        "status": m.group(2).strip(),
        "completion": completion,
        "next": m.group(4).strip(),
    }


def update_runtime(role_cfg: dict, state: dict, board: dict, pending_tasks: list[dict]) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    waiting = board.get("waiting_queues", {}).get(role_cfg["id"], WAITING_DEFAULT.get(role_cfg["id"], ""))
    payload = {
        "role": role_cfg["id"],
        "name": role_cfg["name"],
        "pid": os.getpid(),
        "last_seen": now_iso(),
        "turn_count": state.get("turn_count", 0),
        "active_plan_version": board.get("active_plan_version"),
        "current_task": state.get("current_task", "none"),
        "current_status": state.get("current_status", "idle"),
        "completion": state.get("completion", 0),
        "next_action": state.get("next_action", ""),
        "pending_count": len(pending_tasks),
        "pending_task_ids": [t.get("task_id", "") for t in pending_tasks[:10]],
        "waiting": waiting,
        "last_output_file": state.get("last_output_file", ""),
    }
    write_json(RUNTIME_DIR / f"{role_cfg['id']}.json", payload)


def format_pending(pending_tasks: list[dict], limit: int = 5) -> str:
    if not pending_tasks:
        return "none"
    parts = []
    for t in pending_tasks[:limit]:
        parts.append(f"{t.get('task_id', '?')}({t.get('status', '?')})")
    return ", ".join(parts)


def print_progress(role_cfg: dict, state: dict, board: dict, pending_tasks: list[dict]) -> None:
    active_plan = board.get("active_plan_version")
    counts = board_status_counts(board)
    print(f"[{role_cfg['name']}] active_plan={active_plan} turns={state.get('turn_count', 0)}")
    print(
        "current="
        f"{state.get('current_task', 'none')} "
        f"status={state.get('current_status', 'idle')} "
        f"completion={state.get('completion', 0)}%"
    )
    print(f"next={state.get('next_action', '')}")
    print(f"pending({len(pending_tasks)}): {format_pending(pending_tasks)}")
    print(f"board_counts={counts}")


def chat_once(
    client: OpenAI,
    model: str,
    system_prompt: str,
    summary_text: str,
    control_hint: str,
    history: list[dict],
    user_text: str,
    max_tokens: int,
    temperature: float,
) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    if summary_text:
        messages.append({"role": "system", "content": "Rolling memory:\n" + summary_text})
    if control_hint:
        messages.append({"role": "system", "content": control_hint})
    messages.extend(history)
    messages.append({"role": "user", "content": user_text})

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=None, help="override model name")
    parser.add_argument("--max-tokens", type=int, default=1200, help="max tokens per answer")
    parser.add_argument("--temperature", type=float, default=0.2, help="sampling temperature")
    parser.add_argument("--history", type=int, default=4, help="history turns to keep")
    parser.add_argument("--once", default=None, help="single-run prompt")
    args = parser.parse_args()

    role_cfg = load_role()

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    api_key, base_url, model = load_api_config(args.model)
    client = OpenAI(api_key=api_key, base_url=base_url, max_retries=2, timeout=60)

    session_path = SESSIONS_DIR / "session.jsonl"
    history = load_history(session_path, args.history)
    state = load_state(role_cfg)
    board = load_task_board()
    pending_tasks = role_pending_tasks(role_cfg["id"], board)
    state["pending_task_ids"] = [t.get("task_id", "") for t in pending_tasks[:20]]
    state["active_plan_version"] = board.get("active_plan_version")
    state["last_seen"] = now_iso()
    save_state(state)
    save_summary(build_summary(role_cfg, state, board, pending_tasks))
    update_runtime(role_cfg, state, board, pending_tasks)

    print(
        f"[{role_cfg['name']}] resume: "
        f"task={state.get('current_task', 'none')} "
        f"status={state.get('current_status', 'idle')} "
        f"completion={state.get('completion', 0)}% "
        f"pending={len(pending_tasks)}"
    )
    print("commands: /progress /tasks /set <task_id> <status> /refresh /exit")

    def handle_user_input(user_text: str) -> None:
        nonlocal board, pending_tasks

        board = load_task_board()
        pending_tasks = role_pending_tasks(role_cfg["id"], board)

        control_hint = (
            f"Control snapshot: active_plan={board.get('active_plan_version')}; "
            f"pending_for_{role_cfg['id']}={format_pending(pending_tasks)}; "
            "If blocked by gate, explicitly return waiting status. "
            "Always end reply with: [PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>."
        )
        expanded = expand_file_macros(user_text, PROJECT_ROOT)
        summary_text = load_summary()

        reply = chat_once(
            client=client,
            model=model,
            system_prompt=role_cfg["system_prompt"].strip(),
            summary_text=summary_text,
            control_hint=control_hint,
            history=history,
            user_text=expanded,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
        print("\n" + reply + "\n")

        append_session(session_path, "user", user_text)
        append_session(session_path, "assistant", reply)

        history.extend(
            [
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": reply},
            ]
        )
        if args.history > 0 and len(history) > args.history * 2:
            del history[:-args.history * 2]

        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = OUTPUTS_DIR / f"{role_cfg['id']}_{ts}.md"
        out_path.write_text(reply, encoding="utf-8")

        progress = extract_progress(reply)
        if progress:
            state["current_task"] = progress["task"]
            state["current_status"] = progress["status"]
            state["completion"] = progress["completion"]
            state["next_action"] = progress["next"]

        state["turn_count"] = int(state.get("turn_count", 0)) + 1
        state["last_seen"] = now_iso()
        state["last_user"] = user_text[:1200]
        state["last_output"] = reply[:2000]
        state["last_output_file"] = str(out_path)
        state["active_plan_version"] = board.get("active_plan_version")
        state["pending_task_ids"] = [t.get("task_id", "") for t in pending_tasks[:20]]
        save_state(state)

        append_timeline(
            {
                "ts": now_iso(),
                "role": role_cfg["id"],
                "user": user_text[:400],
                "progress": progress or {},
                "output_file": str(out_path),
            }
        )

        save_summary(build_summary(role_cfg, state, board, pending_tasks))
        update_runtime(role_cfg, state, board, pending_tasks)

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
        if cmd in ("/exit", "/quit", "quit", "exit"):
            print("exit")
            break
        if cmd in ("/progress", "/status"):
            board = load_task_board()
            pending_tasks = role_pending_tasks(role_cfg["id"], board)
            print_progress(role_cfg, state, board, pending_tasks)
            update_runtime(role_cfg, state, board, pending_tasks)
            continue
        if cmd == "/tasks":
            board = load_task_board()
            pending_tasks = role_pending_tasks(role_cfg["id"], board)
            if not pending_tasks:
                print("no pending tasks for this role under current active plan")
            else:
                for t in pending_tasks[:20]:
                    print(
                        f"- {t.get('task_id', '?')} "
                        f"[{t.get('status', '?')}] "
                        f"{t.get('title', '')}"
                    )
            update_runtime(role_cfg, state, board, pending_tasks)
            continue
        if cmd.startswith("/set "):
            parts = user_text.split(maxsplit=2)
            if len(parts) < 3:
                print("usage: /set <task_id> <status>")
                continue
            board = load_task_board()
            ok, msg = set_task_status(board, role_cfg["id"], parts[1], parts[2])
            print(msg)
            pending_tasks = role_pending_tasks(role_cfg["id"], board)
            state["last_seen"] = now_iso()
            state["pending_task_ids"] = [t.get("task_id", "") for t in pending_tasks[:20]]
            save_state(state)
            save_summary(build_summary(role_cfg, state, board, pending_tasks))
            update_runtime(role_cfg, state, board, pending_tasks)
            continue
        if cmd.startswith("/activate "):
            parts = user_text.split(maxsplit=1)
            if len(parts) < 2:
                print("usage: /activate <plan_version>")
                continue
            board = load_task_board()
            ok, msg = activate_plan(board, role_cfg["id"], parts[1])
            print(msg)
            pending_tasks = role_pending_tasks(role_cfg["id"], board)
            state["active_plan_version"] = board.get("active_plan_version")
            state["pending_task_ids"] = [t.get("task_id", "") for t in pending_tasks[:20]]
            state["last_seen"] = now_iso()
            save_state(state)
            save_summary(build_summary(role_cfg, state, board, pending_tasks))
            update_runtime(role_cfg, state, board, pending_tasks)
            continue
        if cmd == "/refresh":
            board = load_task_board()
            pending_tasks = role_pending_tasks(role_cfg["id"], board)
            state["active_plan_version"] = board.get("active_plan_version")
            state["pending_task_ids"] = [t.get("task_id", "") for t in pending_tasks[:20]]
            state["last_seen"] = now_iso()
            save_state(state)
            save_summary(build_summary(role_cfg, state, board, pending_tasks))
            update_runtime(role_cfg, state, board, pending_tasks)
            print_progress(role_cfg, state, board, pending_tasks)
            continue

        handle_user_input(user_text)


if __name__ == "__main__":
    main()
