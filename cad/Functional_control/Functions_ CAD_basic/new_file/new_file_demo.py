from __future__ import annotations
from pathlib import Path
from datetime import datetime
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

from CAD_file_operations import new_file as cfo_new_file, save_file, close_file, cad_zt_oneb, litz

FUNCTION_DIR = SCRIPT_PATH.parent
LOG_PATH = FUNCTION_DIR / "test_log.txt"


def resolve_path(raw: str | None) -> Path:
    if not raw:
        raw = datetime.now().strftime("new_file_demo_%d%M%S.dwg")
    path = Path(raw)
    if not path.is_absolute():
        path = (FUNCTION_DIR / path).resolve()
    return path


def write_log(message: str) -> None:
    LOG_PATH.parent.mkdir(exist_ok=True, parents=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {message}\n")


def run_demo(output_path: Path, close_after: bool) -> None:
    cad_zt_oneb()
    litz()
    try:
        print(f"[new_file_demo] 目标: {output_path}")
        ok = cfo_new_file(str(output_path), close_after=close_after)
        if not ok:
            raise RuntimeError("new_file 返回 False")
        if not close_after:
            print("[new_file_demo] 准备保存并关闭以清理环境")
            save_file()
            close_file("auto_save")
        write_log(f"new_file_demo → {output_path} (close_after={close_after})")
    finally:
        cad_zt_oneb()
        print("[new_file_demo] 已回到 cad_zt_oneb 基准状态")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="测试 new_file 函数，自动应用 cad_zt_oneb/litz 流程。")
    parser.add_argument("output", nargs="?", help="新建 DWG 文件名或绝对路径，缺省按日分秒生成")
    parser.add_argument("--close-after", dest="close_after", action="store_true",
                        help="调用 new_file 后立即关闭新文件 (默认 False 以测试保持打开)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = resolve_path(args.output)
    run_demo(output_path, close_after=args.close_after)


if __name__ == "__main__":
    main()
