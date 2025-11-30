"""Create layer-mode sample DWG for select_print_areas_smart."""
from __future__ import annotations
from pathlib import Path

import sys
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")

import shutil

from CAD_file_operations import cad_zt_zero, cad_zt_oneb, open_file, save_file, close_file, litz
from CAD_basic import li, ensure_layer, draw_lwpolyline, draw_line

BASE_TEMPLATE = Path(r"D:/codex-tasks/cad/xitongwenjian/0.dwg")
TARGET = Path(r"D:/codex-tasks/cad/Functional_control/Functions_ label_catalogue_printing/select_print_areas_smart/samples/layer_mode_sample.dwg")


def build_layer_sample():
    if TARGET.exists():
        TARGET.unlink()
    shutil.copy(BASE_TEMPLATE, TARGET)
    cad_zt_zero()
    cad_zt_oneb()
    litz()
    open_file(str(TARGET))
    li()
    ensure_layer("dy_quyu")
    draw_lwpolyline(
        [
            (0, 0, 0),
            (0, 50000, 0),
            (80000, 50000, 0),
            (80000, 0, 0),
            (0, 0, 0),
        ],
        layer_name="dy_quyu",
        closed=True,
    )
    draw_lwpolyline(
        [
            (100000, 0, 0),
            (100000, 40000, 0),
            (160000, 40000, 0),
            (160000, 0, 0),
            (100000, 0, 0),
        ],
        layer_name="dy_quyu",
        closed=True,
    )
    draw_lwpolyline(
        [
            (0, 70000, 0),
            (0, 100000, 0),
            (40000, 100000, 0),
            (40000, 70000, 0),
        ],
        layer_name="dy_quyu",
        closed=False,
    )
    draw_line((0, -20000, 0), (100000, -20000, 0))
    save_file()
    close_file("no_save")
    cad_zt_oneb()


if __name__ == "__main__":
    build_layer_sample()
