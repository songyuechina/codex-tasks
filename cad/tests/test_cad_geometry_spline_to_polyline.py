#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单函数测试：cad_geometry_polyline.spline_to_polyline_via_splinedit
要求：使用 CAD_core 启动/关闭系统与 DWG 操作
"""

# ================= 路径引导 =================
import sys
import os
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current:
        raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

# 统一 UTF-8 输出，避免日志表情触发 GBK 编码异常
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ================= 标准库 =================
import time

# ================= 系统模块 =================
from system import CAD_core
from system.licad import resolve_doc
from system.CAD_coordination import wait_quiescent

# 被测模块
from library import cad_geometry_polyline as polyline


def _prepare_temp_dwg(path):
    os.makedirs(Path(path).parent, exist_ok=True)
    CAD_core.new_file(output_path=path, close_after=False)
    wait_quiescent(min_quiet=0.5, timeout=30.0)


def _launch_cad():
    launched = False
    for attempt in range(1, 4):
        try:
            CAD_core.launch_tarch_CAD_system()
            launched = True
            break
        except Exception as e:
            print(f"[警告] 启动 CAD 失败，尝试 {attempt}/3: {e}")
            try:
                CAD_core.close_tarch_CAD_system()
            except Exception:
                pass
            time.sleep(3.0)
    if not launched:
        raise RuntimeError("CAD 启动失败")
    time.sleep(2.0)


def _should_keep_cad_open():
    return os.environ.get("CAD_TEST_KEEP_OPEN", "").strip().lower() in ("1", "true", "yes")


def _create_spline_by_command(doc, pts):
    """通过命令创建样条并返回对象。"""
    if not pts or len(pts) < 3:
        return None
    try:
        doc.SetVariable("TILEMODE", 1)
    except Exception:
        pass
    try:
        doc.ActiveSpace = 0
    except Exception:
        pass
    cmd = "_.SPLINE\n"
    for p in pts:
        cmd += f"{p[0]},{p[1]},{p[2]}\n"
    cmd += "\n\n\n"
    try:
        before = doc.ModelSpace.Count
        doc.SendCommand(cmd)
        wait_quiescent(min_quiet=0.3, timeout=10.0)
        after = before
        deadline = time.time() + 5.0
        while time.time() < deadline:
            time.sleep(0.2)
            try:
                after = doc.ModelSpace.Count
            except Exception:
                continue
            if after > before:
                break
        if after <= before:
            return None
        for i in range(after - 1, before - 1, -1):
            try:
                ent = doc.ModelSpace.Item(i)
                if "Spline" in getattr(ent, "ObjectName", ""):
                    return ent
            except Exception:
                continue
        return None
    except Exception:
        return None


def _create_spline_by_com(doc, pts):
    """通过 COM 直接创建样条并返回对象。"""
    if not pts or len(pts) < 3:
        return None
    try:
        import pythoncom
        from win32com.client import VARIANT
        try:
            doc.SetVariable("TILEMODE", 1)
        except Exception:
            pass
        try:
            doc.ActiveSpace = 0
        except Exception:
            pass
        ms = doc.ModelSpace
        arr = []
        for p in pts:
            arr.extend([float(p[0]), float(p[1]), float(p[2])])
        if len(arr) < 6:
            return None
        v_pts = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, arr)
        try:
            p0 = pts[0]
            p1 = pts[1]
            pn_1 = pts[-2]
            pn = pts[-1]
            sdx, sdy, sdz = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
            edx, edy, edz = (pn[0] - pn_1[0], pn[1] - pn_1[1], pn[2] - pn_1[2])
            sl = (sdx ** 2 + sdy ** 2 + sdz ** 2) ** 0.5 or 1.0
            el = (edx ** 2 + edy ** 2 + edz ** 2) ** 0.5 or 1.0
            start_tan = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [sdx / sl, sdy / sl, sdz / sl])
            end_tan = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [edx / el, edy / el, edz / el])
            return ms.AddSpline(v_pts, start_tan, end_tan)
        except Exception:
            return ms.AddSpline(v_pts)
    except Exception as e:
        print(f"[警告] AddSpline 失败: {e}")
        return None


def test_spline_to_polyline_via_splinedit():
    tmp_path = str(Path(current) / "tests" / "_tmp" / "test_spline_to_polyline.dwg")

    _launch_cad()

    try:
        _prepare_temp_dwg(tmp_path)
        doc = resolve_doc(None)
        assert doc is not None, "doc 解析失败"
        try:
            doc.SetVariable("TILEMODE", 1)
        except Exception:
            pass
        try:
            doc.ActiveSpace = 0
        except Exception:
            pass

        # 1) 绘制样条（COM 优先，命令兜底）
        pts = [(0.0, 0.0, 0.0), (50.0, 80.0, 0.0), (120.0, 20.0, 0.0), (200.0, 60.0, 0.0)]
        spline = _create_spline_by_com(doc, pts)
        if spline is None:
            spline = _create_spline_by_command(doc, pts)
        assert spline is not None, "样条绘制失败"

        # 2) 转多段线
        pl = polyline.spline_to_polyline_via_splinedit(spline, segments=10, docname=None, cleanup_copy=True, wait_sec=1.2)
        wait_quiescent(min_quiet=0.3, timeout=10.0)

        assert pl is not None, "spline_to_polyline_via_splinedit 返回 None"
        assert "Polyline" in getattr(pl, "ObjectName", ""), f"对象类型异常: {getattr(pl, 'ObjectName', '')}"
        pl_len = getattr(pl, "Length", None)
        assert pl_len is None or pl_len > 0, f"多段线长度异常: {pl_len}"

        try:
            pl.Delete()
        except Exception:
            pass

        print("[PASS] spline_to_polyline_via_splinedit")
        return True
    finally:
        try:
            CAD_core.save_file()
        except Exception:
            pass
        if not _should_keep_cad_open():
            try:
                CAD_core.close_file("auto_save")
            except Exception:
                pass
            try:
                CAD_core.close_tarch_CAD_system()
            except Exception:
                pass


if __name__ == "__main__":
    ok = test_spline_to_polyline_via_splinedit()
    if not ok:
        raise SystemExit(1)
