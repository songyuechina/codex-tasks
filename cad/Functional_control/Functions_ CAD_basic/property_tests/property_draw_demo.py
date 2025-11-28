from __future__ import annotations
from pathlib import Path
import sys
import argparse
import win32com.client
import pythoncom

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = SCRIPT_PATH.parents[3]
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
HELPER_DIR = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "new_file_draw_shapes"
for extra in (SYSTEM_DIR, SCRIPTS_DIR, HELPER_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import new_file, save_file, close_file, draw_tarch_wall, cad_zt_oneb, litz
from CAD_basic import get_acad_doc, li
import draw_shapes_helper as helper

DEFAULT_FOLDER = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "property_tests"


def draw_entities(folder: Path) -> None:
    folder.mkdir(exist_ok=True, parents=True)
    circle_file = folder / "prop_polyline.dwg"
    text_file = folder / "prop_text.dwg"
    wall_file = folder / "prop_wall.dwg"

    new_file(str(circle_file), close_after=False)
    li()
    helper.draw_polyline([(0, 0), (1000, 0), (1500, 500), (200, 1000)])
    save_file()
    close_file("auto_save")

    new_file(str(text_file), close_after=False)
    li()
    acad, doc = get_acad_doc()
    text_pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (500.0, 200.0, 0.0))
    doc.ModelSpace.AddText("Hello CAD", text_pt, 250)
    save_file()
    close_file("auto_save")

    new_file(str(wall_file), close_after=False)
    li()
    draw_tarch_wall((0, 0, 0), (3000, 0, 0), thickness=240)
    save_file()
    close_file("auto_save")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 property_tests 所需 DWG")
    parser.add_argument("--folder", default=str(DEFAULT_FOLDER), help="输出 DWG 的目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    folder = Path(args.folder).resolve()
    cad_zt_oneb()
    litz()
    try:
        draw_entities(folder)
    finally:
        cad_zt_oneb()
        print("[property_draw_demo] 已回到 cad_zt_oneb 状态")


if __name__ == "__main__":
    main()
