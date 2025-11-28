from pathlib import Path
import sys
import pythoncom
import win32com.client

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = SCRIPT_PATH.parents[3]
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
HELPER_DIR = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "new_file_draw_shapes"
for extra in (SYSTEM_DIR, SCRIPTS_DIR, HELPER_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import new_file, save_file, close_file
from CAD_basic import get_acad_doc, li
import draw_shapes_helper as helper

BASE_DIR = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "insert_tests"
TEMPLATE_DIR = BASE_DIR / "shared"
SOURCE_TEMPLATE = TEMPLATE_DIR / "source_template.dwg"
TARGET_TEMPLATE = TEMPLATE_DIR / "target_template.dwg"


def draw_source_template():
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    new_file(str(SOURCE_TEMPLATE), close_after=False)
    li()
    helper.draw_polyline([(0, 0), (2000, 0), (2000, 2000), (0, 2000), (0, 0)])
    helper.draw_circle_basic((1000, 1000, 0), 600)
    helper.draw_line_segment((0, 0, 0), (2000, 2000, 0))
    helper.draw_line_segment((0, 2000, 0), (2000, 0, 0))
    save_file()
    close_file("auto_save")


def draw_target_template():
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    new_file(str(TARGET_TEMPLATE), close_after=False)
    li()
    helper.draw_line_segment((0, 0, 0), (1500, 0, 0))
    helper.draw_line_segment((0, 500, 0), (1500, 500, 0))
    save_file()
    close_file("auto_save")


if __name__ == "__main__":
    draw_source_template()
    draw_target_template()
