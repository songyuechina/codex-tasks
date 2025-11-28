from __future__ import annotations
from pathlib import Path
import sys
import argparse

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = next(parent for parent in SCRIPT_PATH.parents if parent.name.lower() == "cad")
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
HELPER_DIR = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "new_file_draw_shapes"
for extra in (SYSTEM_DIR, SCRIPTS_DIR, HELPER_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import new_file, save_file, close_file, cad_zt_oneb, litz
from CAD_basic import li, select_entities_in_window
import draw_shapes_helper as helper

FUNCTION_DIR = SCRIPT_PATH.parent
LOG_PATH = FUNCTION_DIR / "test_log.txt"
DEFAULT_REGION = (31910.513529656222, 12035.45359950012, 59141.38590817002, 32002.443028740017)


def write_log(msg: str) -> None:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {msg}\n")


def run_demo(output_path: Path, region: tuple[float, float, float, float]) -> None:
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        helper.draw_circle_basic((38586.0, 23987.0, 0.0), 2064.0)
        helper.draw_line_segment((44685.0, 19763.0, 0.0), (50449.0, 19763.0, 0.0))
        helper.draw_line_segment((52898.0, 25859.0, 0.0), (52898.0, 34725.0, 0.0))

        x1, y1, x2, y2 = region
        sel_w = select_entities_in_window(x1, y1, x2, y2, ty=1.0, select_mode="_W")
        sel_c = select_entities_in_window(x1, y1, x2, y2, ty=1.0, select_mode="_C")
        count_w = len(sel_w) if sel_w else 0
        count_c = len(sel_c) if sel_c else 0
        print(f"[_W] 完全窗口选择数量: {count_w}")
        print(f"[_C] 交叉窗口选择数量: {count_c}")

        save_file()
        close_file("auto_save")
        write_log(f"window_select_demo → {output_path}, region={region}, W={count_w}, C={count_c}")
    finally:
        cad_zt_oneb()
        print("[window_select_demo] 已回到 cad_zt_oneb 状态")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="window/交叉窗口选择示例")
    parser.add_argument("output", nargs="?", default="window_select_demo.dwg",
                        help="输出 DWG 路径")
    parser.add_argument("--region", nargs=4, type=float, default=DEFAULT_REGION,
                        metavar=("x1", "y1", "x2", "y2"),
                        help="窗口对角坐标")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = (FUNCTION_DIR / args.output).resolve()
    region = tuple(args.region)  # type: ignore[arg-type]
    run_demo(output_path, region)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
