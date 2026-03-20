#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
CONTROL_ROOT = Path(__file__).resolve().parent
SUPERVISION_ROOT = CONTROL_ROOT / "supervision"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.runtime import (
    build_client,
    build_paths,
    ensure_layout,
    load_role_config,
    resolve_provider_config,
)


ROLE_CONFIG = {
    "planner": {
        "agent_dir": ROOT / "Planner_Agent",
        "default_instruction": "聚焦任务分解、阶段计划和依赖识别，不要越权进入实现细节，严格基于主控提供的上下文回答。",
    },
    "coder": {
        "agent_dir": ROOT / "Coder_Agent",
        "default_instruction": "聚焦实现推进，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。",
    },
    "reviewer": {
        "agent_dir": ROOT / "Reviewer_Agent",
        "default_instruction": "聚焦 findings-first 审查，不要自行猜测工作区路径，严格基于主控提供的上下文回答。",
    },
    "tester": {
        "agent_dir": ROOT / "Tester_Agent",
        "default_instruction": "聚焦测试结论与阻塞，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。",
    },
}


@dataclass
class DispatchResult:
    role: str
    ok: bool
    command: list[str]
    output_path: str
    prompt_path: str
    response_path: str
    exit_code: int
    stdout_tail: str
    stderr_tail: str


def now_tag() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_text(path: Path, max_chars: int) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return f"[FILE READ FAILED] {path}\n{exc}\n"
    if max_chars > 0 and len(text) > max_chars:
        text = text[:max_chars] + "\n...[truncated]...\n"
    return text


def shrink_text(text: str, max_chars: int) -> str:
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    head = max_chars // 2
    tail = max_chars - head
    return text[:head] + "\n...[middle truncated]...\n" + text[-tail:]


def build_packet(
    *,
    role: str,
    title: str,
    objective: str,
    context: str,
    files: list[Path],
    max_file_chars: int,
    require_progress: bool,
) -> str:
    role_cfg = ROLE_CONFIG[role]
    lines = [
        f"# Supervised Task Packet",
        f"role: {role}",
        f"title: {title}",
        "",
        "## Supervisor Rules",
        "1. 不要自行猜测或搜索其他工作区路径。",
        "2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。",
        "3. 如果信息不足，应明确指出缺口，但不要编造。",
        f"4. {role_cfg['default_instruction']}",
        "",
        "## Objective",
        objective.strip(),
        "",
        "## Context",
        context.strip() or "(none)",
    ]
    if require_progress:
        lines.extend(
            [
                "",
                "## Output Requirement",
                "必须以如下格式收尾：",
                "[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.",
            ]
        )

    for file_path in files:
        lines.extend(
            [
                "",
                f"## File: {file_path.as_posix()}",
                load_text(file_path, max_file_chars),
            ]
        )
    return shrink_text("\n".join(lines).strip() + "\n", 18000)


def make_command(role: str, project_root: Path, output_path: Path) -> list[str]:
    role_cfg = ROLE_CONFIG[role]
    return [
        "python",
        str(role_cfg["agent_dir"] / "agent_cli.py"),
        "--once",
        "<prompt>",
        "--max-tokens",
        "16000",
        "--temperature",
        "0.1",
    ]


def run_via_runtime(role: str, prompt_text: str) -> tuple[int, str, str]:
    role_cfg = ROLE_CONFIG[role]
    role_path = role_cfg["agent_dir"] / "role.toml"
    role_meta = load_role_config(role_path)
    paths = build_paths(role_path)
    ensure_layout(paths)
    resolved, _source = resolve_provider_config(role_meta, paths, None)
    client = build_client(resolved["base_url"], resolved["api_key"])
    control_hint = (
        "You are running under supervisor control. "
        "Do not invent filesystem access or tool calls. "
        "Answer strictly from the provided packet. "
        "If information is insufficient, say so plainly."
    )
    supports_system_role = getattr(role_meta, "supports_system_role", True)
    if supports_system_role:
        messages = [
            {"role": "system", "content": role_meta.system_prompt},
            {"role": "system", "content": control_hint},
            {"role": "user", "content": prompt_text},
        ]
    else:
        merged_user = (
            "Supervisor context for this role:\n"
            + role_meta.system_prompt
            + "\n\n"
            + control_hint
            + "\n\nTask packet:\n"
            + prompt_text
        )
        messages = [{"role": "user", "content": merged_user}]
    last_error = ""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=resolved["model"],
                messages=messages,
                max_tokens=16000,
                temperature=0.1,
            )
            content = response.choices[0].message.content or ""
            return 0, content, ""
        except Exception as exc:
            last_error = str(exc)
    return 1, "", last_error


def dispatch_once(
    *,
    role: str,
    title: str,
    objective: str,
    context: str,
    files: list[Path],
    max_file_chars: int,
    timeout: int,
    require_progress: bool,
) -> DispatchResult:
    role_cfg = ROLE_CONFIG[role]
    run_root = SUPERVISION_ROOT / role / now_tag()
    ensure_dir(run_root)
    prompt_path = run_root / "prompt.md"
    response_path = run_root / "response.txt"
    output_path = run_root / "tool_output.txt"

    prompt_text = build_packet(
        role=role,
        title=title,
        objective=objective,
        context=context,
        files=files,
        max_file_chars=max_file_chars,
        require_progress=require_progress,
    )
    prompt_path.write_text(prompt_text, encoding="utf-8")

    command = make_command(role, PROJECT_ROOT, output_path)
    return_code, stdout, stderr = run_via_runtime(role, prompt_text)

    combined = stdout.strip()
    if not combined and output_path.exists():
        combined = output_path.read_text(encoding="utf-8", errors="ignore").strip()
    response_path.write_text(combined + ("\n" if combined else ""), encoding="utf-8")

    ok = return_code == 0 and bool(combined.strip())
    return DispatchResult(
        role=role,
        ok=ok,
        command=command,
        output_path=str(output_path),
        prompt_path=str(prompt_path),
        response_path=str(response_path),
        exit_code=return_code,
        stdout_tail=stdout[-2000:],
        stderr_tail=stderr[-2000:],
    )


def cmd_healthcheck(args: argparse.Namespace) -> int:
    roles = list(ROLE_CONFIG.keys()) if args.all else [args.role]
    results = []
    for role in roles:
        result = dispatch_once(
            role=role,
            title="healthcheck",
            objective="返回一句简短确认，证明你当前可以正常收发消息。",
            context="只返回一句确认，不要展开。",
            files=[],
            max_file_chars=0,
            timeout=args.timeout,
            require_progress=True,
        )
        results.append(result)

    print(json.dumps([result.__dict__ for result in results], ensure_ascii=False, indent=2))
    return 0 if all(item.ok for item in results) else 1


def cmd_dispatch(args: argparse.Namespace) -> int:
    files = [Path(item).resolve() for item in args.file]
    result = dispatch_once(
        role=args.role,
        title=args.title,
        objective=args.objective,
        context=args.context or "",
        files=files,
        max_file_chars=args.max_file_chars,
        timeout=args.timeout,
        require_progress=not args.no_progress_footer,
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    return 0 if result.ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    health = sub.add_parser("healthcheck")
    health.add_argument("--role", choices=sorted(ROLE_CONFIG.keys()))
    health.add_argument("--all", action="store_true")
    health.add_argument("--timeout", type=int, default=180)
    health.set_defaults(func=cmd_healthcheck)

    dispatch = sub.add_parser("dispatch")
    dispatch.add_argument("--role", required=True, choices=sorted(ROLE_CONFIG.keys()))
    dispatch.add_argument("--title", required=True)
    dispatch.add_argument("--objective", required=True)
    dispatch.add_argument("--context", default="")
    dispatch.add_argument("--file", action="append", default=[])
    dispatch.add_argument("--max-file-chars", type=int, default=4000)
    dispatch.add_argument("--timeout", type=int, default=300)
    dispatch.add_argument("--no-progress-footer", action="store_true")
    dispatch.set_defaults(func=cmd_dispatch)

    return parser


def main() -> int:
    ensure_dir(SUPERVISION_ROOT)
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd == "healthcheck" and not args.all and not args.role:
        parser.error("healthcheck requires --role or --all")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
