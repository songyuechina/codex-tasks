#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import subprocess
import threading
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pythoncom

current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise RuntimeError("找不到 cad 根目录")
    current = current.parent

import sys

sys.path.insert(0, str(current))

from system import CAD_core  # noqa: E402


CAD_LOCK = threading.Lock()
AUTH_TOKEN = ""
PROJECT_ROOT = Path(r"D:\codex-tasks").resolve()
MAX_OUTPUT_CHARS_DEFAULT = 120000


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def _linux_to_windows_path(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return raw

    prefixes = (
        "/home/user/mnt/",
        "/mnt/host/",
    )
    for prefix in prefixes:
        if raw.startswith(prefix):
            tail = raw[len(prefix):]
            parts = [segment for segment in tail.split("/") if segment]
            if not parts:
                return raw
            drive = parts[0]
            if len(drive) == 1 and drive.isalpha():
                remainder = "\\".join(parts[1:])
                return f"{drive.upper()}:\\{remainder}" if remainder else f"{drive.upper()}:\\"
    return raw


def _normalize_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _normalize_payload(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_payload(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_normalize_payload(item) for item in value)
    if isinstance(value, str):
        return _linux_to_windows_path(value)
    return value


def _json_safe(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    return str(value)


def _truncate_text(value: str, limit: int) -> str:
    raw = str(value or "")
    if limit <= 0 or len(raw) <= limit:
        return raw
    omitted = len(raw) - limit
    return f"{raw[:limit]}\n... [truncated {omitted} chars]"


def _is_within(path: Path, root: Path) -> bool:
    try:
        common = os.path.commonpath([os.path.normcase(str(path)), os.path.normcase(str(root))])
    except ValueError:
        return False
    return common == os.path.normcase(str(root))


def _resolve_project_path(raw_path: str, *, allow_missing: bool = True) -> Path:
    if not raw_path:
        raise ValueError("missing project path")
    normalized = _linux_to_windows_path(raw_path)
    candidate = Path(normalized)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    resolved = candidate.resolve(strict=False)
    if not _is_within(resolved, PROJECT_ROOT):
        raise ValueError(f"path is outside project root: {resolved}")
    if not allow_missing and not resolved.exists():
        raise FileNotFoundError(str(resolved))
    return resolved


def _normalize_env_overrides(env: dict[str, Any] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in (env or {}).items():
        env_name = str(key or "").strip()
        if not env_name:
            continue
        if not env_name.replace("_", "").isalnum():
            raise ValueError(f"invalid env name: {env_name}")
        result[env_name] = str(value)
    return result


def _run_host_command(
    *,
    command: list[str],
    cwd: Path,
    timeout_seconds: int,
    env_overrides: dict[str, str] | None = None,
    max_output_chars: int = MAX_OUTPUT_CHARS_DEFAULT,
) -> dict[str, Any]:
    merged_env = os.environ.copy()
    merged_env.setdefault("PYTHONIOENCODING", "utf-8")
    merged_env.setdefault("PYTHONUTF8", "1")
    merged_env.update(env_overrides or {})
    started = time.time()
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            env=merged_env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=max(1, int(timeout_seconds)),
            check=False,
        )
        timed_out = False
        stdout = completed.stdout
        stderr = completed.stderr
        exit_code = int(completed.returncode)
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        exit_code = 124
    elapsed_ms = int((time.time() - started) * 1000)
    return {
        "command": command,
        "cwd": str(cwd),
        "exit_code": exit_code,
        "timed_out": timed_out,
        "elapsed_ms": elapsed_ms,
        "stdout": _truncate_text(stdout, max_output_chars),
        "stderr": _truncate_text(stderr, max_output_chars),
    }


def _run_project_python(
    *,
    script_path: str,
    script_args: list[Any] | None = None,
    cwd: str = "",
    timeout_seconds: int = 3600,
    env: dict[str, Any] | None = None,
    max_output_chars: int = MAX_OUTPUT_CHARS_DEFAULT,
) -> dict[str, Any]:
    script = _resolve_project_path(script_path, allow_missing=False)
    if script.suffix.lower() != ".py":
        raise ValueError(f"script is not a python file: {script}")
    run_cwd = _resolve_project_path(cwd, allow_missing=True) if cwd else script.parent
    command = ["py", "-3", str(script), *[str(item) for item in (script_args or [])]]
    result = _run_host_command(
        command=command,
        cwd=run_cwd,
        timeout_seconds=timeout_seconds,
        env_overrides=_normalize_env_overrides(env),
        max_output_chars=max_output_chars,
    )
    result["script_path"] = str(script)
    result["script_type"] = "python"
    return result


def _run_project_powershell(
    *,
    script_path: str,
    script_args: list[Any] | None = None,
    cwd: str = "",
    timeout_seconds: int = 3600,
    env: dict[str, Any] | None = None,
    max_output_chars: int = MAX_OUTPUT_CHARS_DEFAULT,
) -> dict[str, Any]:
    script = _resolve_project_path(script_path, allow_missing=False)
    if script.suffix.lower() != ".ps1":
        raise ValueError(f"script is not a powershell file: {script}")
    run_cwd = _resolve_project_path(cwd, allow_missing=True) if cwd else script.parent
    command = ["pwsh", "-NoProfile", "-File", str(script), *[str(item) for item in (script_args or [])]]
    result = _run_host_command(
        command=command,
        cwd=run_cwd,
        timeout_seconds=timeout_seconds,
        env_overrides=_normalize_env_overrides(env),
        max_output_chars=max_output_chars,
    )
    result["script_path"] = str(script)
    result["script_type"] = "powershell"
    return result


def _dispatch_action(action: str, kwargs: dict[str, Any]) -> Any:
    action_map = {
        "ping": lambda: {"bridge": "ok"},
        "project_root": lambda: {"project_root": str(PROJECT_ROOT)},
        "inspect_runtime": CAD_core.inspect_cad_runtime,
        "launch_tarch_cad_system": CAD_core.launch_tarch_CAD_system,
        "close_tarch_cad_system": CAD_core.close_tarch_CAD_system,
        "launch_cad_guardians": CAD_core.launch_cad_guardians,
        "litz": CAD_core.litz,
        "cad_zt_zero": CAD_core.cad_zt_zero,
        "cad_zt_oneb": CAD_core.cad_zt_oneb,
        "new_file": CAD_core.new_file,
        "open_file": CAD_core.open_file,
        "save_file": CAD_core.save_file,
        "save_file_as": CAD_core.save_file_as,
        "close_file": CAD_core.close_file,
        "close_all_files": CAD_core.close_all_files,
        "close_dwg_by_name": CAD_core.close_dwg_by_name,
        "switch_to_layout": CAD_core.switch_to_layout,
        "get_current_dwg_path": CAD_core.get_current_dwg_path,
        "get_all_open_dwg_paths": CAD_core.get_all_open_dwg_paths,
        "run_project_python": _run_project_python,
        "run_project_powershell": _run_project_powershell,
    }
    if action not in action_map:
        raise KeyError(f"unsupported action: {action}")
    return action_map[action](**kwargs)


class CadBridgeHandler(BaseHTTPRequestHandler):
    server_version = "CuabotCadBridge/1.0"

    def _write_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _check_auth(self) -> bool:
        if not AUTH_TOKEN:
            return True
        token = self.headers.get("X-CAD-Bridge-Token", "").strip()
        auth = self.headers.get("Authorization", "").strip()
        if token == AUTH_TOKEN or auth == f"Bearer {AUTH_TOKEN}":
            return True
        self._write_json(
            HTTPStatus.UNAUTHORIZED,
            {"ok": False, "error": "unauthorized"},
        )
        return False

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._write_json(
                HTTPStatus.OK,
                {"ok": True, "service": "cuabot_cad_host_bridge", "timestamp": _now_iso()},
            )
            return
        self._write_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/rpc":
            self._write_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not_found"})
            return
        if not self._check_auth():
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0") or 0)
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            payload = json.loads(raw_body.decode("utf-8"))
        except Exception as exc:
            self._write_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": f"invalid_json: {exc}"})
            return

        action = str(payload.get("action") or "").strip()
        kwargs = payload.get("kwargs") or {}
        if not action:
            self._write_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "missing action"})
            return
        if not isinstance(kwargs, dict):
            self._write_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "kwargs must be object"})
            return

        normalized_kwargs = _normalize_payload(kwargs)
        started = time.time()

        try:
            with CAD_LOCK:
                try:
                    pythoncom.CoInitialize()
                except Exception:
                    pass
                result = _dispatch_action(action, normalized_kwargs)
        except Exception as exc:
            self._write_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {
                    "ok": False,
                    "action": action,
                    "error": str(exc),
                    "timestamp": _now_iso(),
                },
            )
            return

        elapsed_ms = int((time.time() - started) * 1000)
        self._write_json(
            HTTPStatus.OK,
            {
                "ok": True,
                "action": action,
                "kwargs": _json_safe(normalized_kwargs),
                "result": _json_safe(result),
                "elapsed_ms": elapsed_ms,
                "timestamp": _now_iso(),
            },
        )

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="cuabot host bridge for TArch/CAD_core")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=18791)
    parser.add_argument("--token", default="")
    args = parser.parse_args()

    global AUTH_TOKEN
    AUTH_TOKEN = str(args.token or "").strip()

    server = ThreadingHTTPServer((args.host, args.port), CadBridgeHandler)
    print(f"[cuabot_cad_host_bridge] listening on {args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
