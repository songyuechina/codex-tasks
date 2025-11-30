"""Create sample DWGs for select_print_areas_smart tests."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import sys
import time
import shutil

sys.path.insert(0, r"D:/codex-tasks/cad/scripts")

from CAD_file_operations import (
    cad_zt_zero,
    cad_zt_oneb,
    open_file,
    save_file,
    close_file,
    insert_file_as_block,
    litz,
)
from CAD_basic import (
    li,
    ensure_layer,
    draw_lwpolyline,
    draw_line,
)

import pythoncom
import win32com.client

ROOT = Path(r"D:/codex-tasks/cad/Functional_control/Functions_ label_catalogue_printing/select_print_areas_smart")
SAMPLES_DIR = ROOT / "samples"
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

BLOCK_TEMPLATE = Path(r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/insert_tests/shared/source_template.dwg")
BASE_TEMPLATE = Path(r"D:/codex-tasks/cad/xitongwenjian/0.dwg")


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


def _collect_handles(ms):
    handles = set()
    for i in range(ms.Count):
        try:
            handles.add(ms.Item(i).Handle)
        except Exception:
            continue
    return handles


def _get_block_min_side(ref):
    try:
        ll, ur = ref.GetBoundingBox()
        dx = abs(float(ur[0]) - float(ll[0]))
        dy = abs(float(ur[1]) - float(ll[1]))
        min_side = min(dx, dy)
        center = (
            (float(ur[0]) + float(ll[0])) / 2.0,
            (float(ur[1]) + float(ll[1])) / 2.0,
            float(ll[2]) if len(ll) > 2 else 0.0,
        )
        return min_side, center
    except Exception:
        return None, (0.0, 0.0, 0.0)


def _scale_block_reference(ref, target_min):
    min_side, center = _get_block_min_side(ref)
    if not min_side or min_side <= 0:
        return False
    if min_side >= target_min:
        return True
    factor = target_min / min_side
    scaled = False
    try:
        ref.XScaleFactor = float(ref.XScaleFactor) * factor
        ref.YScaleFactor = float(ref.YScaleFactor) * factor
        ref.ZScaleFactor = float(ref.ZScaleFactor) * factor
        scaled = True
    except Exception:
        try:
            current = float(getattr(ref, "ScaleFactor", 1.0))
            ref.ScaleFactor = current * factor
            scaled = True
        except Exception:
            pass
    if not scaled:
        try:
            base_pt = win32com.client.VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_R8, center
            )
            ref.ScaleEntity(base_pt, factor)
            scaled = True
        except Exception:
            pass
    return scaled


def _insert_block_and_tag(layer, point, target_min=50000.0):
    if not BLOCK_TEMPLATE.exists():
        raise FileNotFoundError(f"缺少块模板: {BLOCK_TEMPLATE}")
    acad = win32com.client.GetActiveObject("AutoCAD.Application")
    doc = acad.ActiveDocument
    ms = doc.ModelSpace
    before = _collect_handles(ms)
    if not insert_file_as_block(str(BLOCK_TEMPLATE), x=point[0], y=point[1], z=point[2]):
        raise RuntimeError("插入块失败")
    li()
    ms = doc.ModelSpace
    new_refs = []
    for i in range(ms.Count):
        obj = ms.Item(i)
        try:
            name = obj.ObjectName
        except Exception:
            continue
        if name != "AcDbBlockReference":
            continue
        handle = getattr(obj, "Handle", None)
        if handle in before:
            continue
        obj.Layer = layer
        new_refs.append(obj)

    for ref in new_refs:
        _scale_block_reference(ref, target_min)
    return new_refs


def _draw_rect(llx, lly, w, h, layer, closed=True):
    coords = [
        (llx, lly, 0),
        (llx, lly + h, 0),
        (llx + w, lly + h, 0),
        (llx + w, lly, 0),
    ]
    if closed:
        coords.append((llx, lly, 0))
    draw_lwpolyline(coords, layer_name=layer, closed=closed)


def build_block_mode_sample():
    target = SAMPLES_DIR / "block_mode_sample.dwg"
    if target.exists():
        target.unlink()
    cad_zt_zero()
    cad_zt_oneb()
    litz()
    shutil.copy(BASE_TEMPLATE, target)
    _open_file_with_retry(str(target))
    li()
    ensure_layer("dy_quyu")
    ensure_layer("tuqian_neibu_pl")
    ensure_layer("non_print")
    pythoncom.CoInitialize()
    try:
        _insert_block_and_tag("dy_quyu", (0, 0, 0))
        _insert_block_and_tag("tuqian_neibu_pl", (160000, 0, 0))
        _insert_block_and_tag("non_print", (0, 90000, 0))
    finally:
        pythoncom.CoUninitialize()
    save_file()
    close_file("no_save")
    cad_zt_oneb()
    print(f"[样例] 已创建块模式样例: {target}")


def build_layer_mode_sample():
    target = SAMPLES_DIR / "layer_mode_sample.dwg"
    if target.exists():
        target.unlink()
    cad_zt_zero()
    cad_zt_oneb()
    litz()
    shutil.copy(BASE_TEMPLATE, target)
    _open_file_with_retry(str(target))
    li()
    ensure_layer("dy_quyu")
    _draw_rect(0, 0, 80000, 50000, "dy_quyu", closed=True)
    _draw_rect(100000, 0, 60000, 40000, "dy_quyu", closed=True)
    _draw_rect(0, 70000, 40000, 30000, "dy_quyu", closed=False)  # 未闭合
    draw_line((0, -20000, 0), (100000, -20000, 0))  # 非多段线
    save_file()
    close_file("no_save")
    cad_zt_oneb()
    print(f"[样例] 已创建图层模式样例: {target}")


def main(args=None):
    modes = {
        "block": build_block_mode_sample,
        "layer": build_layer_mode_sample,
    }
    executed = []
    if not args:
        funcs = [build_block_mode_sample, build_layer_mode_sample]
    else:
        funcs = []
        for arg in args:
            func = modes.get(arg.lower())
            if func:
                funcs.append(func)
    if not funcs:
        funcs = [build_block_mode_sample, build_layer_mode_sample]
    for func in funcs:
        func()
        executed.append(func.__name__)
    (ROOT / "tests" / "test_log.txt").open("a", encoding="utf-8").write(
        f"{datetime.now():%Y-%m-%d %H:%M:%S} - 已生成样例: {executed}\n"
    )


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

