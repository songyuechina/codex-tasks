# Planner Agent

Independent role agent for `D:/codex-tasks/cad`.

## Run
```powershell
python D:\codex-tasks\cad\Planner_Agent\agent_cli.py
```

Single prompt mode:
```powershell
python D:\codex-tasks\cad\Planner_Agent\agent_cli.py --once "your request"
```

## Folder layout
- `docs/lv1`: quick role notes
- `docs/lv2`: structured working artifacts
- `docs/lv3`: advanced governance/risk/handover docs
- `sessions/session.jsonl`: conversation memory
- `outputs/*.md`: generated responses

## Unified control
All role actions must follow `D:/codex-tasks/cad/agent_control/UNIFIED_CONTROL.md` and check `D:/codex-tasks/cad/agent_control/task_board.json` before starting work.

## Resume and status
- Auto resume sources: `memory/state.json`, `memory/rolling_summary.md`, `sessions/session.jsonl`
- In interactive mode commands: `/progress`, `/tasks`, `/set <task_id> <status>`, `/refresh`, `/exit`
- Runtime heartbeat: `D:/codex-tasks/cad/agent_control/runtime/<role>.json`
- Planner extra command: `/activate <plan_version>`
