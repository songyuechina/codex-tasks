from __future__ import annotations
from pathlib import Path
import sys
import argparse
from datetime import datetime

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = next(parent for parent in SCRIPT_PATH.parents if parent.name.lower() == "cad")
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
for extra in (SYSTEM_DIR, SCRIPTS_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import open_file as cfo_open_file, close_file as cfo_close_file, cad_zt_oneb, litz, save_file
from CAD_basic import li

FUNCTION_DIR = SCRIPT_PATH.parent
ROOT_DIR = FUNCTION_DIR.parent
SHARED_DIR = ROOT_DIR / "shared"
TEMPLATE = SHARED_DIR / "close_demo_a.dwg"
LOG_PATH = FUNCTION_DIR / "test_log.txt"


def ensure_template() -> None:
    if TEMPLATE.exists():
        return
    from create_close_samples import main as create_samples
    create_samples()


def prepare_work_file(target: Path) -> Path:
    ensure_template()
    target.parent.mkdir(parents=True, exist_ok=True)
    data = TEMPLATE.read_bytes()
    target.write_bytes(data)
    return target


def write_log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {message}\n")


def run_demo(target: Path) -> None:
    cad_zt_oneb()
    litz()
    try:
        work_file = prepare_work_file(target)
        print(f"[close_file_demo] 打开: {work_file}")
        ok = cfo_open_file(str(work_file))
        if not ok:
            raise RuntimeError("open_file 返回 False")
        li()
        save_file()
        cfo_close_file("auto_save")
        write_log(f"close_file_demo → {work_file}")
    finally:
        cad_zt_oneb()
        print("[close_file_demo] 已回到 cad_zt_oneb 状态")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="测试 close_file(auto_save)")
    parser.add_argument("output", nargs="?", default="close_file_demo.dwg",
                        help="复制模板后用于测试的 DWG 名称")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target = Path(args.output)
    if not target.is_absolute():
        target = (FUNCTION_DIR / target).resolve()
    run_demo(target)


if __name__ == "__main__":
    main()
