from __future__ import annotations
from pathlib import Path
import sys
import argparse
import win32com.client
import pythoncom

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
from CAD_basic import get_acad_doc, li, set_object_property, last_obj, stc
import draw_shapes_helper as helper

FUNCTION_DIR = SCRIPT_PATH.parent
LOG_PATH = FUNCTION_DIR / "test_log.txt"


def ensure_layer(doc, name: str) -> None:
    try:
        doc.Layers.Item(name)
    except Exception:
        doc.Layers.Add(name)


def write_log(msg: str) -> None:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {msg}\n")


def run_demo(output_path: Path, layer: str) -> None:
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        _, doc = get_acad_doc()
        ensure_layer(doc, layer)

        helper.draw_polyline([(0, 0), (1000, 0), (1500, 500), (200, 1000)])
        pline = last_obj()
        helper.draw_circle_basic((1500, 1500, 0), 400)
        circle = last_obj()
        helper.draw_line_segment((0, 0, 0), (2000, -500, 0))
        line = last_obj()

        for obj in (pline, circle, line):
            set_object_property(obj, "Layer", layer)

        selected = stc(layer)
        count = len(selected) if selected else 0
        print(f"[layer_select] stc('{layer}') 选中数量: {count}")
        save_file()
        close_file("auto_save")
        write_log(f"layer_select_demo → {output_path}, layer={layer}, count={count}")
    finally:
        cad_zt_oneb()
        print("[layer_select_demo] 已回到 cad_zt_oneb 状态")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="stc 图层选择示例")
    parser.add_argument("output", nargs="?", default="layer_select_demo.dwg",
                        help="输出 DWG 文件名或路径")
    parser.add_argument("--layer", default="测试001", help="目标图层名称")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = (FUNCTION_DIR / args.output).resolve()
    run_demo(output_path, args.layer)


if __name__ == "__main__":
    main()
