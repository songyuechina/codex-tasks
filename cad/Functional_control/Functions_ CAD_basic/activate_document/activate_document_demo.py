from __future__ import annotations
from pathlib import Path
import argparse
import sys
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

from CAD_file_operations import new_file, save_file, close_file, activate_document_by_name, cad_zt_oneb, litz
from CAD_basic import li
import draw_shapes_helper as helper

FUNCTION_DIR = SCRIPT_PATH.parent
DEMO_NAMES = ("activate_A_circle.dwg", "activate_B_line.dwg", "activate_C_rect.dwg")
LOG_PATH = FUNCTION_DIR / "test_log.txt"


def ensure_demo_files(folder: Path) -> tuple[Path, Path, Path]:
    folder.mkdir(exist_ok=True)
    created = []
    shapes = {
        "activate_A_circle.dwg": lambda: helper.draw_circle_basic((1000, 1000, 0), 600),
        "activate_B_line.dwg": lambda: helper.draw_line_segment((0, 0, 0), (2500, 0, 0)),
        "activate_C_rect.dwg": lambda: helper.draw_rectangle((0, 0), (1500, 800)),
    }
    for name, draw_fn in shapes.items():
        path = folder / name
        if path.exists():
            continue
        new_file(str(path), close_after=False)
        if not li():
            print("[activate_demo] li() 连接失败，继续绘制")
        draw_fn()
        save_file()
        close_file("auto_save")
        created.append(path)
    return tuple(folder / n for n in DEMO_NAMES)


def reopen_documents(paths: tuple[Path, ...]) -> None:
    pythoncom.CoInitialize()
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    for path in paths:
        acad.Documents.Open(str(path))


def close_documents(names: tuple[str, ...]) -> None:
    pythoncom.CoInitialize()
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    for name in names:
        try:
            doc = acad.Documents.Item(name)
            doc.Close(False)
        except Exception:
            pass


def write_log(order: list[str]) -> None:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  activate_document_demo → {order}\n")


def run_demo(order: list[str]) -> None:
    cad_zt_oneb()
    litz()
    try:
        folder = FUNCTION_DIR
        paths = ensure_demo_files(folder)
        reopen_documents(paths)
        for target in order:
            print(f"[activate_demo] 激活 {target}")
            activate_document_by_name(target)
        write_log(order)
    finally:
        close_documents(tuple(order))
        cad_zt_oneb()
        print("[activate_demo] 已复位到 cad_zt_oneb 状态")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="测试 activate_document_by_name")
    parser.add_argument("targets", nargs="*", default=list(DEMO_NAMES),
                        help="按顺序激活的 DWG 名称 (默认 A→B→C)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    order = list(args.targets)
    run_demo(order)


if __name__ == "__main__":
    main()
