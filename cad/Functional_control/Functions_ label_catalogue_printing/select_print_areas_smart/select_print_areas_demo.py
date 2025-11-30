"""CLI demo runner for select_print_areas_smart."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, r"D:/codex-tasks/cad/scripts")

from CAD_file_operations import cad_zt_oneb, litz, open_file, close_file
from CAD_basic import li, select_print_areas_smart, get_attr

ROOT = Path(__file__).parent
SAMPLES_DIR = ROOT / "samples"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run select_print_areas_smart with explicit parameters."
    )
    parser.add_argument(
        "mode",
        choices=["block", "layer"],
        help="测试模式：block 或 layer（screen 需人工选择，此处不提供）。",
    )
    parser.add_argument(
        "--sample",
        type=Path,
        help="待打开的 DWG 文件；若未指定，将使用 samples/ 下的对应样例。",
    )
    parser.add_argument("--lm", type=float, default=1000.0, help="最小边长阈值 lm。")
    parser.add_argument(
        "--tol-single",
        type=float,
        default=0.01,
        dest="tol_single",
        help="单向多段线判断 tol_single。",
    )
    parser.add_argument(
        "--cha-y", type=float, default=2000.0, dest="cha_y", help="行判定纵向容差。"
    )
    parser.add_argument(
        "--layer-name",
        default="dy_quyu",
        dest="layer_name",
        help="layer 模式下的打印图层名。",
    )
    parser.add_argument(
        "--block-layers",
        nargs="+",
        default=["dy_quyu", "tuqian_neibu_pl"],
        dest="block_layers",
        help="block 模式下识别为打印块的图层集合。",
    )
    parser.add_argument(
        "--aux-layer",
        default="kuai_pl",
        dest="aux_layer",
        help="block 模式绘制辅助矩形的图层。",
    )
    parser.add_argument(
        "--rect-layer",
        default="dy_zhuanyong",
        dest="rect_layer",
        help="最终打印框所在图层。",
    )
    return parser.parse_args()


def resolve_sample_path(mode: str, sample: Path | None) -> Path:
    if sample is not None:
        return sample
    default = {
        "block": SAMPLES_DIR / "block_mode_sample.dwg",
        "layer": SAMPLES_DIR / "layer_mode_sample.dwg",
    }.get(mode)
    if default is None:
        raise ValueError(f"模式 {mode} 暂未提供默认样例。")
    return default


def main():
    args = parse_args()
    sample_path = resolve_sample_path(args.mode, args.sample).resolve()
    if not sample_path.exists():
        raise FileNotFoundError(
            f"缺少样例文件：{sample_path}\n"
            "请先运行 python tests/create_test_samples.py block layer"
        )

    kwargs = dict(
        mode=args.mode,
        lm=args.lm,
        tol_single=args.tol_single,
        cha_Y=args.cha_y,
    )
    if args.mode == "layer":
        kwargs["layer_name"] = args.layer_name
    if args.mode == "block":
        kwargs["block_layers"] = tuple(args.block_layers)
        kwargs["aux_layer"] = args.aux_layer
        kwargs["rect_layer"] = args.rect_layer

    cad_zt_oneb()
    try:
        litz()
        open_file(str(sample_path))
        li()
        result = select_print_areas_smart(**kwargs)
        handles = [get_attr(ent, "Handle") for ent in result]
        payload = {
            "mode": args.mode,
            "sample": str(sample_path),
            "count": len(handles),
            "handles": handles,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    finally:
        try:
            close_file("no_save")
        except Exception:
            pass
        cad_zt_oneb()


if __name__ == "__main__":
    main()

