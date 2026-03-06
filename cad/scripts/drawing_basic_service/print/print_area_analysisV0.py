# -*- coding: utf-8 -*-
"""
printframe_distinguishability.py

功能：
1) 从当前激活DWG（C.doc）扫描打印框矩形（BoundingBox）
2) 得到48组(w,h)（w<=h）
3) 扩展为288组（×1.0/1.1/1.2，再×1 或 ×0.01）
4) 按“每个矩形自身的 w * 0.0005 作为容差”，做对称判据碰撞检测
5) 打印报告

说明：
- 你已确认打印框在图层 PUB_TITLE（从你的输出看是这样），默认只取该图层。
- 若你的打印框不在该层，把 DEFAULT_LAYER_FILTER 改掉或传 None。
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ------------------------------------------------------------
# project bootstrap (与您现有脚本一致的 cad 根目录定位)
# ------------------------------------------------------------
current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent
sys.path.insert(0, str(current))

from system.project_setup import PathConfig  # noqa: F401
from system.licad import C


# ------------------------------------------------------------
# config
# ------------------------------------------------------------
DEFAULT_LAYER_FILTER = ["PUB_TITLE"]  # 你输出里全部是 PUB_TITLE；若不确定可改为 None
SCALES = (1.0, 1.1, 1.2)
REAL_SCALES = (1.0, 0.01)
TOL_RATIO = 0.0005  # 每个矩形 eps = TOL_RATIO * w


# ------------------------------------------------------------
# bbox and extraction
# ------------------------------------------------------------
def _bbox_wh(ent: Any) -> Optional[Tuple[float, float]]:
    """
    返回 (w, h) 其中 w<=h，失败返回 None
    """
    try:
        mn, mx = ent.GetBoundingBox()  # (minPoint, maxPoint)
        dx = float(mx[0]) - float(mn[0])
        dy = float(mx[1]) - float(mn[1])
        if dx <= 0 or dy <= 0:
            return None
        w = min(dx, dy)
        h = max(dx, dy)
        return (w, h)
    except Exception:
        return None


def get_printframe_rects_wh_bbox(
    expect_count: int = 48,
    layer_filter: Optional[List[str]] = DEFAULT_LAYER_FILTER,
    scan_paperspace: bool = True,
    object_name_filter: Optional[Tuple[str, ...]] = ("AcDbPolyline",),
) -> List[Dict[str, Any]]:
    """
    获取打印框矩形的长宽（BoundingBox）
    """
    doc = C.doc
    spaces = [doc.ModelSpace]
    if scan_paperspace:
        try:
            spaces.append(doc.PaperSpace)
        except Exception:
            pass

    rects: List[Dict[str, Any]] = []

    for sp in spaces:
        for ent in sp:
            try:
                objname = str(ent.ObjectName)
            except Exception:
                continue

            if object_name_filter is not None and objname not in object_name_filter:
                continue

            try:
                layer = str(ent.Layer)
            except Exception:
                layer = ""

            if layer_filter is not None and layer not in layer_filter:
                continue

            wh = _bbox_wh(ent)
            if wh is None:
                continue
            w, h = wh

            try:
                handle = str(ent.Handle)
            except Exception:
                handle = ""

            rects.append(
                dict(
                    handle=handle,
                    layer=layer,
                    object_name=objname,
                    w=float(w),
                    h=float(h),
                    area=float(w * h),
                )
            )

    rects.sort(key=lambda d: (d["w"], d["h"]))

    if expect_count is not None and len(rects) != expect_count:
        print(f"[WARN] 识别到矩形 {len(rects)} 个（期望 {expect_count}）。"
              f"建议检查 layer_filter/object_name_filter 或是否在块中。")

    return rects


# ------------------------------------------------------------
# expand to 288
# ------------------------------------------------------------
def expand_288(rects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for idx, r in enumerate(rects):
        w0, h0 = float(r["w"]), float(r["h"])
        for s in SCALES:
            for k in REAL_SCALES:
                w = w0 * s * k
                h = h0 * s * k
                if w > h:
                    w, h = h, w
                out.append(
                    dict(
                        src_index=idx,
                        src_handle=r.get("handle", ""),
                        layer=r.get("layer", ""),
                        s=float(s),
                        k=float(k),
                        w=float(w),
                        h=float(h),
                    )
                )
    return out


# ------------------------------------------------------------
# collision test (per-rect eps, symmetric)
# ------------------------------------------------------------
def eps(item: Dict[str, Any]) -> float:
    # 每个矩形自身容差：eps = TOL_RATIO * w（w是短边）
    return TOL_RATIO * float(item["w"])


def collide_symmetric(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    dw = abs(float(a["w"]) - float(b["w"]))
    dh = abs(float(a["h"]) - float(b["h"]))
    ea = eps(a)
    eb = eps(b)
    # 对称判据：同时落入双方容差盒
    return (dw <= ea and dh <= ea) and (dw <= eb and dh <= eb)


def find_collisions(data: List[Dict[str, Any]]) -> List[Tuple[int, int, float, float, float, float]]:
    """
    返回碰撞列表：
    (i, j, dw, dh, eps_i, eps_j)
    """
    cols: List[Tuple[int, int, float, float, float, float]] = []
    n = len(data)
    for i in range(n):
        ai = data[i]
        ei = eps(ai)
        wi = float(ai["w"])
        hi = float(ai["h"])
        for j in range(i + 1, n):
            bj = data[j]
            # 快速剪枝：若短边差已经大于两者最大容差，不可能碰撞（对称判据）
            dw = abs(wi - float(bj["w"]))
            # 只要 dw > max(ei, ej) 就一定无法同时满足双方（对称）
            ej = eps(bj)
            if dw > max(ei, ej):
                continue
            dh = abs(hi - float(bj["h"]))
            if dh > max(ei, ej):
                continue
            if (dw <= ei and dh <= ei) and (dw <= ej and dh <= ej):
                cols.append((i, j, dw, dh, ei, ej))
    return cols


# ------------------------------------------------------------
# report
# ------------------------------------------------------------
def main() -> None:
    doc = C.doc
    print(f"[INFO] Active DWG: {getattr(doc, 'Name', '(unknown)')}")

    rects48 = get_printframe_rects_wh_bbox(
        expect_count=48,
        layer_filter=DEFAULT_LAYER_FILTER,
        scan_paperspace=True,
        object_name_filter=("AcDbPolyline",),  # 你输出就是这个；若以后需要可加 "AcDbBlockReference"
    )

    print(f"[INFO] rect48 count = {len(rects48)}")
    for r in rects48:
        print(r["object_name"], r["layer"], r["w"], r["h"])

    data288 = expand_288(rects48)
    print(f"[INFO] data288 count = {len(data288)} (expect 288)")

    cols = find_collisions(data288)
    print(f"[RESULT] collisions = {len(cols)} under rule eps = {TOL_RATIO} * w(each-rect) with symmetric test")

    if cols:
        print("\n[DETAIL] first 200 collision pairs:")
        for n, (i, j, dw, dh, ei, ej) in enumerate(cols[:200], 1):
            a = data288[i]
            b = data288[j]
            print(f"#{n}")
            print(f"  A: src={a['src_index']:02d} handle={a['src_handle']} s={a['s']} k={a['k']} w={a['w']} h={a['h']} eps={ei}")
            print(f"  B: src={b['src_index']:02d} handle={b['src_handle']} s={b['s']} k={b['k']} w={b['w']} h={b['h']} eps={ej}")
            print(f"  dw={dw} dh={dh}")
    else:
        print("[OK] No collisions detected. 288组在该判据下可精确区分。")


if __name__ == "__main__":
    main()
