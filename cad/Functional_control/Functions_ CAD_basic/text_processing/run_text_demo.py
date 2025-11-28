from __future__ import annotations
from pathlib import Path
from datetime import datetime
import argparse
import sys

TEXT_ROOT = Path(__file__).resolve().parent
CAD_DIR = next(parent for parent in TEXT_ROOT.parents if parent.name.lower() == "cad")
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
HELPER_DIR = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "new_file_draw_shapes"
for extra in (SYSTEM_DIR, SCRIPTS_DIR, HELPER_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import (
    new_file,
    save_file,
    close_file,
    cad_zt_oneb,
    litz,
    write_cad_text,
    write_tianzheng_text,
    align_text_to_vertical_line,
    align_text_to_horizontal_line,
    scale_tianzheng_text_to_cad,
)
from CAD_basic import li

FUNCTION_DIRS = {name: TEXT_ROOT / name for name in (
    "write_cad_text",
    "write_tianzheng_text",
    "align_text_to_vertical_line",
    "align_text_to_horizontal_line",
    "scale_tianzheng_text_to_cad",
)}


def ensure_log(func_name: str) -> Path:
    folder = FUNCTION_DIRS[func_name]
    folder.mkdir(parents=True, exist_ok=True)
    log_file = folder / "test_log.txt"
    if not log_file.exists():
        log_file.write_text("", encoding="utf-8")
    return log_file


def resolve_output(func_name: str, filename: str | None, prefix: str) -> Path:
    folder = FUNCTION_DIRS[func_name]
    if filename:
        path = Path(filename)
        if not path.is_absolute():
            path = folder / filename
    else:
        stamp = datetime.now().strftime("%d%H%M%S")
        path = folder / f"{prefix}_{stamp}.dwg"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def log_result(func_name: str, message: str) -> None:
    log_file = ensure_log(func_name)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {message}\n")


def demo_write_cad_text(args: argparse.Namespace) -> None:
    output_path = resolve_output("write_cad_text", args.output, "write_cad_text")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        write_cad_text(
            p=(args.x, args.y, args.z),
            text=args.text,
            alignment=args.alignment,
            height=args.height,
            width_factor=args.width_factor,
            rotation=args.rotation,
            oblique=args.oblique,
            style=args.style,
        )
        save_file()
        close_file("auto_save")
        log_result("write_cad_text", f"write_cad_text -> {output_path}")
    finally:
        cad_zt_oneb()


def demo_write_tianzheng_text(args: argparse.Namespace) -> None:
    output_path = resolve_output("write_tianzheng_text", args.output, "write_tz_text")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        write_tianzheng_text(
            p=(args.x, args.y, args.z),
            text=args.text,
            alignment=args.alignment,
            height=args.height,
            width_factor=args.width_factor,
            rotation=args.rotation,
            oblique=args.oblique,
            style=args.style,
            system_layer=args.system_layer,
            system_file_name=args.system_file_name,
            delete_system_text=args.delete_system_text,
        )
        save_file()
        close_file("auto_save")
        log_result("write_tianzheng_text", f"write_tianzheng_text -> {output_path}")
    finally:
        cad_zt_oneb()


def _prepare_two_texts() -> tuple[object, object]:
    txt1 = write_cad_text(p=(0, 0, 0), text="TEXT_A", alignment="左下", height=300)
    txt2 = write_cad_text(p=(1200, 800, 0), text="TEXT_B", alignment="左下", height=300)
    return txt1, txt2


def demo_align_vertical(args: argparse.Namespace) -> None:
    output_path = resolve_output("align_text_to_vertical_line", args.output, "align_vertical")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        txt1, txt2 = _prepare_two_texts()
        align_text_to_vertical_line([txt1, txt2], args.x_position, align_side=args.align_side)
        save_file()
        close_file("auto_save")
        log_result("align_text_to_vertical_line", f"align_text_to_vertical_line -> {output_path} @ X={args.x_position}")
    finally:
        cad_zt_oneb()


def demo_align_horizontal(args: argparse.Namespace) -> None:
    output_path = resolve_output("align_text_to_horizontal_line", args.output, "align_horizontal")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        txt1, txt2 = _prepare_two_texts()
        align_text_to_horizontal_line([txt1, txt2], args.y_position, align_side=args.align_side)
        save_file()
        close_file("auto_save")
        log_result("align_text_to_horizontal_line", f"align_text_to_horizontal_line -> {output_path} @ Y={args.y_position}")
    finally:
        cad_zt_oneb()


def demo_scale_tz_to_cad(args: argparse.Namespace) -> None:
    output_path = resolve_output("scale_tianzheng_text_to_cad", args.output, "scale_tz_text")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        cad_text = write_cad_text(p=(0, 0, 0), text="CAD_BASE", height=args.cad_height)
        tz_text = write_tianzheng_text(p=(args.tx, args.ty, args.tz), text="TZ_TEXT")
        scale_tianzheng_text_to_cad(tz_text, cad_text)
        save_file()
        close_file("auto_save")
        log_result("scale_tianzheng_text_to_cad", f"scale_tianzheng_text_to_cad -> {output_path}")
    finally:
        cad_zt_oneb()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="文字处理函数测试脚本")
    sub = parser.add_subparsers(dest="function", required=True)

    p1 = sub.add_parser("write_cad_text", help="测试 write_cad_text")
    p1.add_argument("--output")
    p1.add_argument("--text", default="示例CAD文字")
    p1.add_argument("--x", type=float, default=0.0)
    p1.add_argument("--y", type=float, default=0.0)
    p1.add_argument("--z", type=float, default=0.0)
    p1.add_argument("--alignment", default="左下")
    p1.add_argument("--height", type=float, default=350.0)
    p1.add_argument("--width-factor", dest="width_factor", type=float, default=1.0)
    p1.add_argument("--rotation", type=float, default=0.0)
    p1.add_argument("--oblique", type=float, default=0.0)
    p1.add_argument("--style", default="Standard")

    p2 = sub.add_parser("write_tianzheng_text", help="测试 write_tianzheng_text")
    p2.add_argument("--output")
    p2.add_argument("--text", default="天正单行文字")
    p2.add_argument("--x", type=float, default=0.0)
    p2.add_argument("--y", type=float, default=0.0)
    p2.add_argument("--z", type=float, default=0.0)
    p2.add_argument("--alignment", default="左下")
    p2.add_argument("--height", type=float, default=3.5)
    p2.add_argument("--width-factor", dest="width_factor", type=float, default=1.0)
    p2.add_argument("--rotation", type=float, default=0.0)
    p2.add_argument("--oblique", type=float, default=0.0)
    p2.add_argument("--style", default="Standard")
    p2.add_argument("--system-layer", dest="system_layer", default="xitong_tianzhengwenzi")
    p2.add_argument("--system-file-name", dest="system_file_name", default="tianzhengdanhangwenzi.dwg")
    p2.add_argument("--delete-system-text", action="store_true")

    p3 = sub.add_parser("align_text_to_vertical_line", help="测试垂直对齐")
    p3.add_argument("--output")
    p3.add_argument("--x-position", dest="x_position", type=float, default=500.0)
    p3.add_argument("--align-side", dest="align_side", default="左边界")

    p4 = sub.add_parser("align_text_to_horizontal_line", help="测试水平对齐")
    p4.add_argument("--output")
    p4.add_argument("--y-position", dest="y_position", type=float, default=200.0)
    p4.add_argument("--align-side", dest="align_side", default="下边界")

    p5 = sub.add_parser("scale_tianzheng_text_to_cad", help="缩放天正文字到 CAD 高度")
    p5.add_argument("--output")
    p5.add_argument("--cad-height", dest="cad_height", type=float, default=500.0)
    p5.add_argument("--tx", type=float, default=1200.0)
    p5.add_argument("--ty", type=float, default=0.0)
    p5.add_argument("--tz", type=float, default=0.0)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = args.function
    if func == "write_cad_text":
        demo_write_cad_text(args)
    elif func == "write_tianzheng_text":
        demo_write_tianzheng_text(args)
    elif func == "align_text_to_vertical_line":
        demo_align_vertical(args)
    elif func == "align_text_to_horizontal_line":
        demo_align_horizontal(args)
    elif func == "scale_tianzheng_text_to_cad":
        demo_scale_tz_to_cad(args)
    else:
        parser.error(f"未知函数: {func}")


if __name__ == "__main__":
    main()
