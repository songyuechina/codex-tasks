from __future__ import annotations
from pathlib import Path
from datetime import datetime
import argparse
import sys

BLOCK_ROOT = Path(__file__).resolve().parent
CAD_DIR = next(parent for parent in BLOCK_ROOT.parents if parent.name.lower() == "cad")
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
    create_block_from_region_cad,
    create_block_from_region_cmd,
    copy_block_contents_at_same_location,
    add_entities_to_block_keep_world,
    extract_nonblock_entities_from_block,
)
from CAD_basic import li, last_obj
import draw_shapes_helper as helper

FUNCTION_DIRS = {name: BLOCK_ROOT / name for name in (
    "create_block_from_region_cad",
    "create_block_from_region_cmd",
    "copy_block_contents_at_same_location",
    "add_entities_to_block_keep_world",
    "extract_nonblock_entities_from_block",
)}


def ensure_log(func_name: str) -> Path:
    folder = FUNCTION_DIRS[func_name]
    folder.mkdir(parents=True, exist_ok=True)
    log_file = folder / "test_log.txt"
    if not log_file.exists():
        log_file.write_text("", encoding="utf-8")
    return log_file


def log_result(func_name: str, message: str) -> None:
    log_file = ensure_log(func_name)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}  {message}\n")


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


def draw_region_geometry() -> None:
    helper.draw_rectangle((0, 0), (2000, 1200))
    helper.draw_circle_basic((800, 600, 0), 250)
    helper.draw_line_segment((0, 0, 0), (2000, 1200, 0))


def demo_create_block_cad(args: argparse.Namespace) -> None:
    output_path = resolve_output("create_block_from_region_cad", args.output, "block_cad")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        draw_region_geometry()
        block_ref = create_block_from_region_cad(*args.region, insert_point_option=args.insert_point_option,
                                                 block_name_prefix=args.block_prefix,
                                                 base_point=tuple(args.base_point) if args.base_point else None,
                                                 ty=args.ty)
        save_file()
        close_file("auto_save")
        log_result("create_block_from_region_cad", f"create_block_from_region_cad -> {output_path}, block={getattr(block_ref, 'Name', 'N/A')}")
    finally:
        cad_zt_oneb()


def demo_create_block_cmd(args: argparse.Namespace) -> None:
    output_path = resolve_output("create_block_from_region_cmd", args.output, "block_cmd")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        draw_region_geometry()
        block_ref = create_block_from_region_cmd(*args.region, insert_point_option=args.insert_point_option,
                                                 block_name_prefix=args.block_prefix,
                                                 base_point=tuple(args.base_point) if args.base_point else None,
                                                 ty=args.ty)
        save_file()
        close_file("auto_save")
        log_result("create_block_from_region_cmd", f"create_block_from_region_cmd -> {output_path}, block={getattr(block_ref, 'Name', 'N/A')}")
    finally:
        cad_zt_oneb()


def _build_sample_block(region, method="cad"):
    draw_region_geometry()
    if method == "cad":
        return create_block_from_region_cad(*region)
    return create_block_from_region_cmd(*region)


def demo_copy_block(args: argparse.Namespace) -> None:
    output_path = resolve_output("copy_block_contents_at_same_location", args.output, "copy_block")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        block_ref = _build_sample_block(args.region)
        copied = copy_block_contents_at_same_location(block_ref)
        save_file()
        close_file("auto_save")
        log_result("copy_block_contents_at_same_location", f"copy_block_contents_at_same_location -> {output_path}, copied={len(copied)}")
    finally:
        cad_zt_oneb()


def demo_add_entities(args: argparse.Namespace) -> None:
    output_path = resolve_output("add_entities_to_block_keep_world", args.output, "add_block_entities")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        block_ref = _build_sample_block(args.region)
        helper.draw_circle_basic((args.extra_x, args.extra_y, 0), 150)
        extra_entity = last_obj()
        add_entities_to_block_keep_world(block_ref, [extra_entity], keep_source=args.keep_source)
        save_file()
        close_file("auto_save")
        log_result("add_entities_to_block_keep_world", f"add_entities_to_block_keep_world -> {output_path}, keep_source={args.keep_source}")
    finally:
        cad_zt_oneb()


def demo_extract_nonblock(args: argparse.Namespace) -> None:
    output_path = resolve_output("extract_nonblock_entities_from_block", args.output, "extract_block")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        block_ref = _build_sample_block(args.region)
        world_entities = extract_nonblock_entities_from_block(block_ref, keep_in_block=args.keep_in_block)
        save_file()
        close_file("auto_save")
        log_result("extract_nonblock_entities_from_block", f"extract_nonblock_entities_from_block -> {output_path}, new_entities={len(world_entities)}")
    finally:
        cad_zt_oneb()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="块处理函数测试脚本")
    sub = parser.add_subparsers(dest="function", required=True)
    def region_option(p):
        p.add_argument("--region", nargs=4, type=float, default=(0.0, 0.0, 2000.0, 1200.0), metavar=("x1","y1","x2","y2"))
        p.add_argument("--output")
        return p

    p1 = region_option(sub.add_parser("create_block_from_region_cad"))
    p1.add_argument("--insert-point-option", default="左下")
    p1.add_argument("--block-prefix", default="块")
    p1.add_argument("--base-point", nargs=2, type=float)
    p1.add_argument("--ty", type=float, default=1.0)

    p2 = region_option(sub.add_parser("create_block_from_region_cmd"))
    p2.add_argument("--insert-point-option", default="左下")
    p2.add_argument("--block-prefix", default="块")
    p2.add_argument("--base-point", nargs=2, type=float)
    p2.add_argument("--ty", type=float, default=1.0)

    p3 = region_option(sub.add_parser("copy_block_contents_at_same_location"))

    p4 = region_option(sub.add_parser("add_entities_to_block_keep_world"))
    p4.add_argument("--extra-x", dest="extra_x", type=float, default=500.0)
    p4.add_argument("--extra-y", dest="extra_y", type=float, default=1500.0)
    p4.add_argument("--keep-source", action="store_true")

    p5 = region_option(sub.add_parser("extract_nonblock_entities_from_block"))
    p5.add_argument("--keep-in-block", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = args.function
    if func == "create_block_from_region_cad":
        demo_create_block_cad(args)
    elif func == "create_block_from_region_cmd":
        demo_create_block_cmd(args)
    elif func == "copy_block_contents_at_same_location":
        demo_copy_block(args)
    elif func == "add_entities_to_block_keep_world":
        demo_add_entities(args)
    elif func == "extract_nonblock_entities_from_block":
        demo_extract_nonblock(args)
    else:
        parser.error(f"未知函数: {func}")


if __name__ == "__main__":
    main()
