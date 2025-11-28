from __future__ import annotations
from pathlib import Path
import argparse
import sys

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = next(parent for parent in SCRIPT_PATH.parents if parent.name.lower() == "cad")
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
for extra in (SYSTEM_DIR, SCRIPTS_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import open_file as cfo_open_file, save_file, close_file, cad_zt_oneb, litz

FUNCTION_DIR = SCRIPT_PATH.parent
LOG_PATH = FUNCTION_DIR / "test_log.txt"


def resolve_path(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = (FUNCTION_DIR / raw).resolve()
    return path


def write_log(msg: str) -> None:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {msg}\n")


def run_demo(target: Path) -> None:
    cad_zt_oneb()
    litz()
    try:
        print(f"[open_file_demo] 打开: {target}")
        ok = cfo_open_file(str(target))
        if not ok:
            raise RuntimeError("open_file 返回 False")
        save_file()
        close_file("auto_save")
        write_log(f"open_file_demo → {target}")
    finally:
        cad_zt_oneb()
        print("[open_file_demo] 已回到 cad_zt_oneb 基准状态")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="测试 open_file 函数")
    parser.add_argument("target", help="需要打开的 DWG 文件")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target = resolve_path(args.target)
    run_demo(target)


if __name__ == "__main__":
    main()
