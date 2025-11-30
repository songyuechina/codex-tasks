"""Run select_print_areas_smart tests for block/layer modes."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import sys
import time

sys.path.insert(0, r"D:/codex-tasks/cad/scripts")

from CAD_file_operations import cad_zt_oneb, open_file, close_file, litz
from CAD_basic import li, select_print_areas_smart, get_attr

ROOT = Path(r"D:/codex-tasks/cad/Functional_control/Functions_ label_catalogue_printing/select_print_areas_smart")
SAMPLES_DIR = ROOT / "samples"
LOG_FILE = ROOT / "tests" / "test_log.txt"


def _open_file_with_retry(path: str, retries: int = 5, delay: float = 3.0):
    last = None
    for attempt in range(1, retries + 1):
        try:
            ok = open_file(path)
            if ok:
                return True
            last = RuntimeError("open_file 返回 False")
        except Exception as exc:
            last = exc
        print(f"[重试] open_file 第 {attempt} 次失败：{last!r}，{delay}s 后重试...")
        time.sleep(delay)
    raise RuntimeError(f"open_file 多次失败：{last!r}")


def _run_on_file(sample, mode, **kwargs):
    sample_path = SAMPLES_DIR / sample
    if not sample_path.exists():
        raise FileNotFoundError(f"缺少样例文件: {sample_path}")
    cad_zt_oneb()
    litz()
    _open_file_with_retry(str(sample_path))
    li()
    result = select_print_areas_smart(mode=mode, **kwargs)
    handles = [get_attr(ent, "Handle") for ent in result]
    close_file("no_save")
    cad_zt_oneb()
    return handles


def test_block():
    handles = _run_on_file(
        "block_mode_sample.dwg",
        mode="block",
        block_layers=("dy_quyu", "tuqian_neibu_pl"),
        cha_Y=2000,
        lm=1000,
    )
    return {
        "mode": "block",
        "count": len(handles),
        "handles": handles,
    }


def test_layer():
    handles = _run_on_file(
        "layer_mode_sample.dwg",
        mode="layer",
        layer_name="dy_quyu",
        cha_Y=2000,
    )
    return {
        "mode": "layer",
        "count": len(handles),
        "handles": handles,
    }


def log_result(result):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fp:
        fp.write(
            f"{datetime.now():%Y-%m-%d %H:%M:%S} | {result['mode']} | count={result['count']} | handles={result['handles']}\n"
        )
    print(result)


def main(args):
    tasks = []
    if not args:
        tasks = [test_block, test_layer]
    else:
        for name in args:
            name = name.lower()
            if name.startswith("block"):
                tasks.append(test_block)
            elif name.startswith("layer"):
                tasks.append(test_layer)
    if not tasks:
        print("未指定有效测试；使用 block layer")
        tasks = [test_block, test_layer]
    for task in tasks:
        log_result(task())


if __name__ == "__main__":
    main(sys.argv[1:])
