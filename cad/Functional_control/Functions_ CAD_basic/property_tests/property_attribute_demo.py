from __future__ import annotations
from pathlib import Path
import sys
import argparse
import pythoncom
import win32com.client
from datetime import datetime

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = SCRIPT_PATH.parents[3]
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
HELPER_DIR = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "new_file_draw_shapes"
for extra in (SYSTEM_DIR, SCRIPTS_DIR, HELPER_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import open_file, save_file, close_file, cad_zt_oneb, litz
from CAD_basic import get_acad_doc, li, get_object_property, set_object_property
import draw_shapes_helper as helper

DEFAULT_FOLDER = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "property_tests"
LOG_PATH = DEFAULT_FOLDER / "test_log.txt"


def _ensure_samples(folder: Path) -> None:
    from property_draw_demo import draw_entities
    draw_entities()


def _get_first(ms, names):
    for ent in ms:
        if getattr(ent, "ObjectName", "") in names:
            return ent
    raise RuntimeError(f"未找到对象类型 {names}")


def _edit_polyline(folder: Path) -> None:
    target = folder / "prop_polyline.dwg"
    open_file(str(target))
    li()
    _, doc = get_acad_doc()
    pline = _get_first(doc.ModelSpace, ("AcDbPolyline", "AcDb2dPolyline"))
    coords = list(get_object_property(pline, "Coordinates"))
    if len(coords) >= 2:
        coords[0] += 500.0
        coords[1] += 500.0
    set_object_property(pline, "Coordinates", tuple(coords))
    print("[polyline] 更新后首点:", get_object_property(pline, "Coordinates")[:2])
    save_file()
    close_file("auto_save")


def _edit_text(folder: Path) -> None:
    target = folder / "prop_text.dwg"
    open_file(str(target))
    li()
    _, doc = get_acad_doc()
    text = _get_first(doc.ModelSpace, ("AcDbText", "AcDbMText"))
    current = get_object_property(text, "TextString")
    set_object_property(text, "TextString", f"{current}_MOD")
    print("[text] 更新后内容:", get_object_property(text, "TextString"))
    save_file()
    close_file("auto_save")


def _edit_wall(folder: Path) -> None:
    target = folder / "prop_wall.dwg"
    open_file(str(target))
    li()
    _, doc = get_acad_doc()
    wall = _get_first(doc.ModelSpace, ("TDbWall",))
    t1 = get_object_property(wall, "Thickness") or 0
    t2 = get_object_property(wall, "Thickness2") or 0
    set_object_property(wall, "Thickness", t1 + 50)
    set_object_property(wall, "Thickness2", t2 + 50)
    print("[wall] 更新后厚度:", get_object_property(wall, "Thickness"), get_object_property(wall, "Thickness2"))
    save_file()
    close_file("auto_save")


def write_log(folder: Path) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  property_attribute_demo → {folder}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="测试 CAD/TArch 属性读写")
    parser.add_argument("--folder", default=str(DEFAULT_FOLDER), help="prop_* DWG 存放目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    folder = Path(args.folder).resolve()
    cad_zt_oneb()
    litz()
    try:
        _ensure_samples(folder)
        _edit_polyline(folder)
        _edit_text(folder)
        _edit_wall(folder)
        write_log(folder)
    finally:
        cad_zt_oneb()
        print("[property_attribute_demo] 已回到 cad_zt_oneb 状态")


if __name__ == "__main__":
    main()
