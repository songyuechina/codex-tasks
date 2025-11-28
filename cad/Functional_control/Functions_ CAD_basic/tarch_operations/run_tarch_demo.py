from __future__ import annotations
from pathlib import Path
from datetime import datetime
import argparse
import sys

TARCH_ROOT = Path(__file__).resolve().parent
CAD_DIR = next(parent for parent in TARCH_ROOT.parents if parent.name.lower() == "cad")
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
    draw_tarch_wall,
    insert_tarch_door,
    insert_tarch_window,
    run_tupdspace_for_tz_room_in_rect,
    TDb_single_line_variable_wall,
    dim_by_points,
)
from CAD_basic import li
import draw_shapes_helper as helper

FUNCTION_DIRS = {name: TARCH_ROOT / name for name in (
    "draw_tarch_wall",
    "insert_tarch_door",
    "insert_tarch_window",
    "run_tupdspace_for_tz_room_in_rect",
    "TDb_single_line_variable_wall",
    "dim_by_points",
)}


def ensure_log(func_name: str) -> Path:
    folder = FUNCTION_DIRS[func_name]
    folder.mkdir(parents=True, exist_ok=True)
    log_file = folder / "test_log.txt"
    if not log_file.exists():
        log_file.write_text("", encoding="utf-8")
    return log_file


def log_result(func_name: str, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = ensure_log(func_name)
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


def demo_draw_wall(args: argparse.Namespace) -> None:
    output_path = resolve_output("draw_tarch_wall", args.output, "tarch_wall")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        draw_tarch_wall((args.x1, args.y1, 0.0), (args.x2, args.y2, 0.0), thickness=args.thickness)
        save_file()
        close_file("auto_save")
        log_result("draw_tarch_wall", f"draw_tarch_wall -> {output_path}")
    finally:
        cad_zt_oneb()


def _prepare_wall_for_opening(length=6000.0) -> None:
    draw_tarch_wall((0.0, 0.0, 0.0), (length, 0.0, 0.0), thickness=240.0)


def demo_insert_door(args: argparse.Namespace) -> None:
    output_path = resolve_output("insert_tarch_door", args.output, "tarch_door")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        _prepare_wall_for_opening()
        insert_tarch_door((args.x, args.y, 0.0), width=args.width, height=args.height)
        save_file()
        close_file("auto_save")
        log_result("insert_tarch_door", f"insert_tarch_door -> {output_path} @ ({args.x},{args.y})")
    finally:
        cad_zt_oneb()


def demo_insert_window(args: argparse.Namespace) -> None:
    output_path = resolve_output("insert_tarch_window", args.output, "tarch_window")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        _prepare_wall_for_opening()
        insert_tarch_window((args.x, args.y, 0.0), width=args.width, height=args.height,
                             window_type=args.window_type, delete_mc_yuan=args.delete_mc_yuan)
        save_file()
        close_file("auto_save")
        log_result("insert_tarch_window", f"insert_tarch_window -> {output_path} type={args.window_type}")
    finally:
        cad_zt_oneb()


def _draw_room_outline(x1, y1, x2, y2):
    corners = [(x1, y1, 0.0), (x2, y1, 0.0), (x2, y2, 0.0), (x1, y2, 0.0), (x1, y1, 0.0)]
    for i in range(4):
        draw_tarch_wall(corners[i], corners[i+1])


def demo_tupdspace(args: argparse.Namespace) -> None:
    output_path = resolve_output("run_tupdspace_for_tz_room_in_rect", args.output, "tupd_room")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        _draw_room_outline(*args.region)
        result = run_tupdspace_for_tz_room_in_rect(*args.region, ty=args.ty,
                                                   center_z=args.center_z,
                                                   insert_coord=tuple(args.insert_coord) if args.insert_coord else None,
                                                   require_tz_wall=not args.ignore_wall_check)
        save_file()
        close_file("auto_save")
        log_result("run_tupdspace_for_tz_room_in_rect", f"run_tupdspace -> {output_path}, result={result}")
    finally:
        cad_zt_oneb()


def demo_variable_wall(args: argparse.Namespace) -> None:
    output_path = resolve_output("TDb_single_line_variable_wall", args.output, "variable_wall")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        helper.draw_line_segment((args.x1, args.y1, 0.0), (args.x2, args.y2, 0.0))
        helper.draw_line_segment((args.x1, args.y1 + 500, 0.0), (args.x2, args.y2 + 500, 0.0))
        TDb_single_line_variable_wall(args.x1 - 200, args.y1 - 200, args.x2 + 200, args.y2 + 200, width=args.width)
        save_file()
        close_file("auto_save")
        log_result("TDb_single_line_variable_wall", f"variable_wall -> {output_path}")
    finally:
        cad_zt_oneb()


def demo_dim_by_points(args: argparse.Namespace) -> None:
    output_path = resolve_output("dim_by_points", args.output, "dim_points")
    cad_zt_oneb()
    litz()
    try:
        new_file(str(output_path), close_after=False)
        li()
        helper.draw_line_segment((0, 0, 0), (args.p2x, args.p2y, 0.0))
        dim_by_points((args.p1x, args.p1y, 0.0), (args.p2x, args.p2y, 0.0), (args.p3x, args.p3y, 0.0))
        save_file()
        close_file("auto_save")
        log_result("dim_by_points", f"dim_by_points -> {output_path}")
    finally:
        cad_zt_oneb()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="天正墙/门窗/房间函数测试脚本")
    sub = parser.add_subparsers(dest="function", required=True)

    p1 = sub.add_parser("draw_tarch_wall")
    p1.add_argument("--output")
    p1.add_argument("--x1", type=float, default=0.0)
    p1.add_argument("--y1", type=float, default=0.0)
    p1.add_argument("--x2", type=float, default=4000.0)
    p1.add_argument("--y2", type=float, default=0.0)
    p1.add_argument("--thickness", type=float, default=240.0)

    p2 = sub.add_parser("insert_tarch_door")
    p2.add_argument("--output")
    p2.add_argument("--x", type=float, default=2000.0)
    p2.add_argument("--y", type=float, default=0.0)
    p2.add_argument("--width", type=float)
    p2.add_argument("--height", type=float)

    p3 = sub.add_parser("insert_tarch_window")
    p3.add_argument("--output")
    p3.add_argument("--x", type=float, default=2500.0)
    p3.add_argument("--y", type=float, default=0.0)
    p3.add_argument("--width", type=float, default=800.0)
    p3.add_argument("--height", type=float, default=1200.0)
    p3.add_argument("--window-type", dest="window_type", default="jz-pingchuang")
    p3.add_argument("--delete-mc-yuan", dest="delete_mc_yuan", action="store_true")

    p4 = sub.add_parser("run_tupdspace_for_tz_room_in_rect")
    p4.add_argument("--output")
    p4.add_argument("--region", nargs=4, type=float, default=(0.0, 0.0, 5000.0, 4000.0))
    p4.add_argument("--ty", type=float, default=1.0)
    p4.add_argument("--center-z", dest="center_z", type=float, default=0.0)
    p4.add_argument("--insert-coord", dest="insert_coord", nargs=3, type=float)
    p4.add_argument("--ignore-wall-check", action="store_true")

    p5 = sub.add_parser("TDb_single_line_variable_wall")
    p5.add_argument("--output")
    p5.add_argument("--x1", type=float, default=0.0)
    p5.add_argument("--y1", type=float, default=0.0)
    p5.add_argument("--x2", type=float, default=4000.0)
    p5.add_argument("--y2", type=float, default=0.0)
    p5.add_argument("--width", type=float, default=360.0)

    p6 = sub.add_parser("dim_by_points")
    p6.add_argument("--output")
    p6.add_argument("--p1x", type=float, default=0.0)
    p6.add_argument("--p1y", type=float, default=0.0)
    p6.add_argument("--p2x", type=float, default=3000.0)
    p6.add_argument("--p2y", type=float, default=0.0)
    p6.add_argument("--p3x", type=float, default=1500.0)
    p6.add_argument("--p3y", type=float, default=800.0)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = args.function
    if func == "draw_tarch_wall":
        demo_draw_wall(args)
    elif func == "insert_tarch_door":
        demo_insert_door(args)
    elif func == "insert_tarch_window":
        demo_insert_window(args)
    elif func == "run_tupdspace_for_tz_room_in_rect":
        demo_tupdspace(args)
    elif func == "TDb_single_line_variable_wall":
        demo_variable_wall(args)
    elif func == "dim_by_points":
        demo_dim_by_points(args)
    else:
        parser.error(f"未知函数: {func}")


if __name__ == "__main__":
    main()
