from __future__ import annotations
from pathlib import Path
from datetime import datetime
import argparse
import sys

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = next(parent for parent in SCRIPT_PATH.parents if parent.name.lower() == "cad")
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
HELPER_DIR = SCRIPT_PATH.parent
for extra in (SYSTEM_DIR, SCRIPTS_DIR, HELPER_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import new_file, save_file, close_file, cad_zt_oneb, litz
from CAD_basic import li
import draw_shapes_helper as helper

FUNCTION_DIR = SCRIPT_PATH.parent
LOG_PATH = FUNCTION_DIR / "test_log.txt"


def resolve_path(raw: str | None) -> Path:
    if not raw:
        raw = datetime.now().strftime("shapes_demo_%d%M%S.dwg")
    path = Path(raw)
    if not path.is_absolute():
        path = (FUNCTION_DIR / path).resolve()
    return path


def write_log(msg: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {msg}\n")


def draw_all() -> None:
    helper.draw_point((0, 0, 0))
    helper.draw_line_segment((0, 0, 0), (2000, 0, 0))
    helper.draw_circle_basic((1000, 1200, 0), 400)
    helper.draw_arc_three_points((0, 0), (1000, 800), (2000, 0))
    helper.draw_ellipse_axes((2500, 0), 1600, 900)
    helper.draw_rectangle((300, -800), (1300, -200))
    helper.draw_polyline([(0, 0), (0, 1500), (800, 1800), (1200, 600)])
    helper.draw_spline([(1500, 0), (1800, 500), (2100, -200), (2500, 300), (2800, 0)])


def run_demo(output_path: Path) -> None:
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        if not li():
            print("[draw_shapes_demo] li() 连接失败，仍尝试绘图")
        draw_all()
        save_file()
        close_file("auto_save")
        write_log(f"draw_shapes_demo → {output_path}")
    finally:
        cad_zt_oneb()
        print("[draw_shapes_demo] 已恢复 cad_zt_oneb 状态")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="新建 DWG 并绘制线面示例")
    parser.add_argument("output", nargs="?", help="输出 DWG 名称，缺省以日分秒命名")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = resolve_path(args.output)
    run_demo(output_path)


if __name__ == "__main__":
    main()
