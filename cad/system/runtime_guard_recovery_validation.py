#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

import psutil


current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent

project_root = current.parent
if str(current) not in sys.path:
    sys.path.insert(0, str(current))

from system.CAD_core import collect_cad_process_inventory, inspect_cad_runtime


SYSTEM_DIR = current / "system"
CONTROL_ROOT = project_root / "dwg_agents_ops" / "agent_control"
RUNTIME_DIR = CONTROL_ROOT / "runtime"
GUARD_STATE_PATH = RUNTIME_DIR / "cad_runtime_guard.json"
AGENT_STATE_PATH = RUNTIME_DIR / "runtime_guard_agent.json"
VALIDATION_ROOT = SYSTEM_DIR / "logs" / "runtime-guard-validation"

RUNTIME_GUARD_SCRIPT = SYSTEM_DIR / "cad_runtime_guard.py"
AGENT_SCRIPT = project_root / "dwg_agents_ops" / "Runtime_Guard_Agent" / "agent_cli.py"

PLAIN_CAD_EXE = Path(r"C:\Program Files\Autodesk\AutoCAD 2021\acad.exe")
TARCH_BOOTSTRAP_EXE = Path(r"C:\Tangent\TArchT20V9\TGStart.exe")


def now_compact() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


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


def _kill_process_tree(proc: psutil.Process) -> None:
    try:
        children = proc.children(recursive=True)
    except Exception:
        children = []

    for child in children:
        try:
            child.terminate()
        except Exception:
            pass
    try:
        proc.terminate()
    except Exception:
        pass

    try:
        gone, alive = psutil.wait_procs(children + [proc], timeout=5)
    except Exception:
        alive = []

    for item in alive:
        try:
            item.kill()
        except Exception:
            pass


def stop_python_script(script_fragment: str) -> list[int]:
    killed = []
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            name = str(proc.info.get("name") or "").lower()
            if "python" not in name:
                continue
            cmdline = " ".join(proc.info.get("cmdline") or [])
            if script_fragment.lower() not in cmdline.lower():
                continue
            _kill_process_tree(proc)
            killed.append(int(proc.pid))
        except Exception:
            continue
    return killed


def clean_cad_processes(timeout: float = 20.0) -> dict:
    summary = {
        "taskkill_returncode": None,
        "before": collect_cad_process_inventory(),
        "after": [],
        "extra_killed_pids": [],
    }

    try:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", "acad.exe"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        summary["taskkill_returncode"] = int(result.returncode)
    except Exception:
        summary["taskkill_returncode"] = -1

    deadline = time.time() + max(timeout, 1.0)
    while time.time() < deadline:
        rows = collect_cad_process_inventory()
        if not rows:
            summary["after"] = []
            return summary
        time.sleep(0.5)

    leftovers = collect_cad_process_inventory()
    summary["after"] = leftovers
    if leftovers:
        for row in leftovers:
            pid = int(row.get("pid", 0) or 0)
            if pid <= 0:
                continue
            try:
                _kill_process_tree(psutil.Process(pid))
                summary["extra_killed_pids"].append(pid)
            except Exception:
                continue
        time.sleep(2.0)
    summary["after"] = collect_cad_process_inventory()
    return summary


def ensure_runtime_guard_running() -> dict:
    stopped_guard_pids = stop_python_script("cad_runtime_guard.py")
    stopped_agent_pids = stop_python_script("Runtime_Guard_Agent\\agent_cli.py")

    for path in [
        SYSTEM_DIR / "cad_runtime_guard.lock",
        AGENT_SCRIPT.with_name("runtime_guard_agent.lock"),
    ]:
        try:
            path.unlink(missing_ok=True)
        except Exception:
            pass

    proc = subprocess.Popen(
        [sys.executable, str(RUNTIME_GUARD_SCRIPT)],
        cwd=str(SYSTEM_DIR),
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    time.sleep(2.0)
    return {
        "stopped_guard_pids": stopped_guard_pids,
        "stopped_agent_pids": stopped_agent_pids,
        "started_guard_pid": int(proc.pid),
    }


def launch_mode(mode: str) -> dict:
    if mode == "plain":
        if not PLAIN_CAD_EXE.exists():
            raise FileNotFoundError(f"纯 CAD 启动程序不存在: {PLAIN_CAD_EXE}")
        proc = subprocess.Popen([str(PLAIN_CAD_EXE), "/nologo"], cwd=str(PLAIN_CAD_EXE.parent))
        return {
            "mode": mode,
            "pid": int(proc.pid),
            "command": f"{PLAIN_CAD_EXE} /nologo",
        }

    if mode == "tarch":
        if not TARCH_BOOTSTRAP_EXE.exists():
            raise FileNotFoundError(f"天正启动程序不存在: {TARCH_BOOTSTRAP_EXE}")
        proc = subprocess.Popen([str(TARCH_BOOTSTRAP_EXE)], cwd=str(TARCH_BOOTSTRAP_EXE.parent))
        return {
            "mode": mode,
            "pid": int(proc.pid),
            "command": str(TARCH_BOOTSTRAP_EXE),
        }

    raise ValueError(f"不支持的 mode: {mode}")


def run_agent_once() -> dict:
    started_at = now_iso()
    result = subprocess.run(
        [sys.executable, str(AGENT_SCRIPT), "--once"],
        capture_output=True,
        text=True,
        timeout=240,
    )
    return {
        "started_at": started_at,
        "returncode": int(result.returncode),
        "stdout_tail": (result.stdout or "")[-4000:],
        "stderr_tail": (result.stderr or "")[-2000:],
        "state_after": read_json(AGENT_STATE_PATH, {}),
    }


def wait_for_stable_tarch_snapshot(timeout: float = 25.0, poll_interval: float = 1.5) -> dict:
    deadline = time.time() + max(timeout, 1.0)
    snapshot = inspect_cad_runtime()
    while time.time() < deadline:
        snapshot = inspect_cad_runtime()
        if (
            snapshot.get("status") == "healthy_tarch"
            and not snapshot.get("plain_process_pids", [])
        ):
            return snapshot
        time.sleep(max(poll_interval, 0.5))
    return inspect_cad_runtime()


def execute_round(index: int, mode: str, *, timeout: float, poll_interval: float) -> dict:
    round_payload = {
        "index": index,
        "mode": mode,
        "started_at": now_iso(),
        "cleanup": clean_cad_processes(),
        "launch": {},
        "observed_plain": False,
        "observed_pause_and_recover": False,
        "agent_invocations": [],
        "timeline": [],
        "success": False,
        "final_reason": "",
        "final_snapshot": {},
        "final_guard_state": {},
    }

    time.sleep(3.0)
    round_payload["launch"] = launch_mode(mode)

    deadline = time.time() + max(timeout, 10.0)
    agent_triggered = False
    last_recorded = 0.0
    while time.time() < deadline:
        guard_state = read_json(GUARD_STATE_PATH, {})
        snapshot = inspect_cad_runtime()

        guard_status = str(guard_state.get("current_status") or "")
        recommended_action = str(guard_state.get("recommended_action") or "")
        snapshot_status = str(snapshot.get("status") or "")

        if snapshot_status == "suspected_plain_cad" or guard_status == "suspected_plain_cad":
            round_payload["observed_plain"] = True
        if recommended_action == "pause_and_recover":
            round_payload["observed_pause_and_recover"] = True

        now_epoch = time.time()
        if now_epoch - last_recorded >= max(poll_interval, 1.0):
            round_payload["timeline"].append(
                {
                    "timestamp": now_iso(),
                    "guard_status": guard_status,
                    "recommended_action": recommended_action,
                    "snapshot_status": snapshot_status,
                    "pid": int(snapshot.get("pid", 0) or 0),
                    "plain_process_pids": snapshot.get("plain_process_pids", []),
                    "tarch_process_pids": snapshot.get("tarch_process_pids", []),
                    "process_cmdline": snapshot.get("process_cmdline", ""),
                }
            )
            last_recorded = now_epoch

        if mode == "plain" and recommended_action == "pause_and_recover" and not agent_triggered:
            round_payload["agent_invocations"].append(run_agent_once())
            agent_triggered = True

        if (
            snapshot_status == "healthy_tarch"
            and not snapshot.get("plain_process_pids", [])
        ):
            if mode == "tarch":
                round_payload["success"] = True
                round_payload["final_reason"] = "tarch_round_stable"
                break
            if round_payload["observed_plain"]:
                round_payload["success"] = True
                round_payload["final_reason"] = "plain_round_recovered_to_tarch"
                break

        time.sleep(max(poll_interval, 1.0))

    round_payload["finished_at"] = now_iso()
    round_payload["final_snapshot"] = inspect_cad_runtime()
    round_payload["final_guard_state"] = read_json(GUARD_STATE_PATH, {})

    if not round_payload["success"] and not round_payload["final_reason"]:
        round_payload["final_reason"] = "timeout_without_expected_recovery"
    return round_payload


def build_round_modes(mode: str, rounds: int, seed: int) -> list[str]:
    if mode in {"plain", "tarch"}:
        return [mode] * rounds

    rng = random.Random(seed)
    return [rng.choice(["plain", "tarch"]) for _ in range(rounds)]


def main() -> int:
    parser = argparse.ArgumentParser(description="实测 cad_runtime_guard 对 plain CAD 的发现与恢复能力")
    parser.add_argument("--mode", choices=["plain", "tarch", "random"], default="random")
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=150.0)
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=20260321)
    args = parser.parse_args()

    output_dir = VALIDATION_ROOT / f"case-{now_compact()}"
    output_dir.mkdir(parents=True, exist_ok=True)

    runtime_guard_boot = ensure_runtime_guard_running()
    round_modes = build_round_modes(args.mode, max(args.rounds, 1), args.seed)

    summary = {
        "started_at": now_iso(),
        "seed": int(args.seed),
        "mode": args.mode,
        "round_modes": round_modes,
        "runtime_guard_boot": runtime_guard_boot,
        "rounds": [],
        "success": False,
    }

    for idx, round_mode in enumerate(round_modes, start=1):
        payload = execute_round(
            idx,
            round_mode,
            timeout=float(args.timeout),
            poll_interval=float(args.poll_interval),
        )
        summary["rounds"].append(payload)
        write_json(output_dir / f"round-{idx:02d}.json", payload)

    summary["finished_at"] = now_iso()
    summary["success"] = all(item.get("success") for item in summary["rounds"])
    summary["final_runtime_snapshot"] = wait_for_stable_tarch_snapshot(timeout=30.0, poll_interval=1.5)
    summary["final_guard_state"] = read_json(GUARD_STATE_PATH, {})
    summary["final_agent_state"] = read_json(AGENT_STATE_PATH, {})

    write_json(output_dir / "summary.json", summary)
    print(json.dumps({"output_dir": str(output_dir), "success": summary["success"]}, ensure_ascii=False, indent=2))
    return 0 if summary["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
