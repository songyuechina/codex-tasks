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

from CAD_file_operations import open_file as cfo_open_file, close_all_files as cfo_close_all, cad_zt_oneb, litz
from CAD_basic import li

FUNCTION_DIR = SCRIPT_PATH.parent
ROOT_DIR = FUNCTION_DIR.parent
SHARED_DIR = ROOT_DIR / "shared"
TEMPLATE_A = SHARED_DIR / "close_demo_a.dwg"
TEMPLATE_B = SHARED_DIR / "close_demo_b.dwg"
LOG_PATH = FUNCTION_DIR / "test_log.txt"


def ensure_templates() -> None:
    if TEMPLATE_A.exists() and TEMPLATE_B.exists():
        return
    from create_close_samples import main as create_samples
    create_samples()


def prepare_work_files(targets: list[Path]) -> list[Path]:
    ensure_templates()
    sources = [TEMPLATE_A, TEMPLATE_B]
    prepared = []
    for target, source in zip(targets, sources):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        prepared.append(target)
    return prepared


def write_log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {message}\n")


def run_demo(file_a: Path, file_b: Path) -> None:
    cad_zt_oneb()
    litz()
    try:
        prepared = prepare_work_files([file_a, file_b])
        for path in prepared:
            cfo_open_file(str(path))
        li()
        cfo_close_all("auto_save")

        for path in prepared:
            cfo_open_file(str(path))
        li()
        cfo_close_all("no_save")
        write_log(f"close_all_files_demo → {[str(p) for p in prepared]}")
    finally:
        cad_zt_oneb()
        print("[close_all_files_demo] 已回到 cad_zt_oneb 状态")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="测试 close_all_files")
    parser.add_argument("file_a", nargs="?", default="close_all_demo_a.dwg")
    parser.add_argument("file_b", nargs="?", default="close_all_demo_b.dwg")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    targets = []
    for raw in (args.file_a, args.file_b):
        path = Path(raw)
        if not path.is_absolute():
            path = (FUNCTION_DIR / raw).resolve()
        targets.append(path)
    run_demo(targets[0], targets[1])


if __name__ == "__main__":
    main()
