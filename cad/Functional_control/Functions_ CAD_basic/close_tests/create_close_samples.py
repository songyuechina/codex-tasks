from pathlib import Path
import sys

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
from CAD_basic import li
import draw_shapes_helper as helper

BASE_DIR = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "close_tests" / "shared"
FILE_A = BASE_DIR / "close_demo_a.dwg"
FILE_B = BASE_DIR / "close_demo_b.dwg"

def draw_file(path, shapes):
    new_file(str(path), close_after=False)
    li()
    for fn, args in shapes:
        fn(*args)
    save_file()
    close_file("auto_save")

def main():
    BASE_DIR.mkdir(exist_ok=True, parents=True)
    cad_zt_oneb()
    litz()
    try:
        draw_file(FILE_A, [
            (helper.draw_line_segment, ((0, 0, 0), (2000, 0, 0))),
            (helper.draw_circle_basic, ((1000, 1000, 0), 500)),
        ])
        draw_file(FILE_B, [
            (helper.draw_polyline, ([(0, 0), (1000, 0), (1000, 1000), (0, 1000), (0, 0)],)),
        ])
    finally:
        cad_zt_oneb()

if __name__ == "__main__":
    main()
