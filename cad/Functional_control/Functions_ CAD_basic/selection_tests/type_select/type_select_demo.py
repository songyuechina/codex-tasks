from __future__ import annotations
from pathlib import Path
import sys
import argparse
import pythoncom
import win32com.client

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
from CAD_basic import (
    li,
    get_acad_doc,
    select_text,
    select_mtext,
    select_pub_text_entities,
    select_line,
    select_circle,
    select_ellipse,
    select_spline,
    select_polyline_chuantong,
    select_polyline,
)
import draw_shapes_helper as helper

FUNCTION_DIR = SCRIPT_PATH.parent
LOG_PATH = FUNCTION_DIR / "test_log.txt"


def write_log(msg: str) -> None:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {msg}\n")


def run_demo(output_path: Path) -> None:
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        acad, doc = get_acad_doc()
        ms = doc.ModelSpace

        text_pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (1000.0, 1000.0, 0.0))
        ms.AddText("TXT", text_pt, 300)
        mtext_pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (2000.0, 1500.0, 0.0))
        ms.AddMText(mtext_pt, 500, "MTEXT CONTENT")

        helper.draw_line_segment((0, 0, 0), (1000, 0, 0))
        helper.draw_circle_basic((2000, 0, 0), 400)
        helper.draw_ellipse_axes((3000, 0, 0), 1200, 600)
        helper.draw_spline([(0, 1000), (500, 1500), (1200, 1200), (1800, 1600)])
        helper.draw_polyline([(0, -500), (500, -800), (900, -100), (1200, -600)])
        helper.draw_polyline([(1500, -500), (2000, -200), (2500, -500)])

        li()
        counts = {
            "select_text": len(select_text()) if select_text() else 0,
            "select_mtext": len(select_mtext()) if select_mtext() else 0,
            "select_pub_text_entities": len(select_pub_text_entities() or []),
            "select_line": len(select_line() or []),
            "select_circle": len(select_circle() or []),
            "select_ellipse": len(select_ellipse() or []),
            "select_spline": len(select_spline() or []),
            "select_polyline_chuantong": len(select_polyline_chuantong() or []),
            "select_polyline": len(select_polyline() or []),
        }
        for k, v in counts.items():
            print(f"[{k}] -> {v}")

        save_file()
        close_file("auto_save")
        write_log(f"type_select_demo → {output_path}, counts={counts}")
    finally:
        cad_zt_oneb()
        print("[type_select_demo] 已回到 cad_zt_oneb 状态")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="对象类型选择示例")
    parser.add_argument("output", nargs="?", default="type_select_demo.dwg",
                        help="输出 DWG 文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = (FUNCTION_DIR / args.output).resolve()
    run_demo(output_path)


if __name__ == "__main__":
    main()
