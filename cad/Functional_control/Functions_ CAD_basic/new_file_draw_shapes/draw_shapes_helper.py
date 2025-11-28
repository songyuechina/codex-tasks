from __future__ import annotations
from pathlib import Path
import sys

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = SCRIPT_PATH.parents[4]
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
for extra in (SYSTEM_DIR, SCRIPTS_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

import win32com.client
from win32com.client import VARIANT
import pythoncom
from CAD_coordination import send_cmd_with_sync, wait_quiescent
from CAD_basic import get_acad_doc


def _get_model_space():
    """Return (ModelSpace, Document)."""
    _, doc = get_acad_doc()
    return doc.ModelSpace, doc


def _to_point(pt):
    """Normalize a tuple/list to a VARIANT point."""
    if len(pt) == 3:
        x, y, z = pt
    elif len(pt) == 2:
        x, y = pt
        z = 0.0
    else:
        raise ValueError("point must be length 2 or 3")
    return VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (float(x), float(y), float(z)))


def draw_point(pt):
    ms, _ = _get_model_space()
    return ms.AddPoint(_to_point(pt))


def draw_line_segment(p1, p2):
    ms, _ = _get_model_space()
    return ms.AddLine(_to_point(p1), _to_point(p2))


def draw_circle_basic(center, radius):
    ms, _ = _get_model_space()
    return ms.AddCircle(_to_point(center), radius)


def draw_arc_three_points(p1, p2, p3):
    cmd = f"_ARC\n{p1[0]},{p1[1]}\n{p2[0]},{p2[1]}\n{p3[0]},{p3[1]}\n"
    return send_cmd_with_sync(cmd, wait_after=0.6, timeout=20.0)


def draw_ellipse_axes(center, major_length, minor_length):
    half_major = major_length / 2.0
    half_minor = minor_length / 2.0
    start = (center[0] - half_major, center[1])
    end = (center[0] + half_major, center[1])
    minor_pt = (center[0], center[1] + half_minor)
    cmd = f"_ELLIPSE\n{start[0]},{start[1]}\n{end[0]},{end[1]}\n{minor_pt[0]},{minor_pt[1]}\n"
    return send_cmd_with_sync(cmd, wait_after=0.6, timeout=20.0)


def draw_rectangle(lower_left, upper_right):
    cmd = f"_RECTANG\n{lower_left[0]},{lower_left[1]}\n{upper_right[0]},{upper_right[1]}\n"
    return send_cmd_with_sync(cmd, wait_after=0.5, timeout=15.0)


def draw_polyline(points):
    if len(points) < 2:
        return False
    coords = "".join(f"{x},{y}\n" for x, y in points)
    cmd = f"_PLINE\n{coords}\n"
    ok = send_cmd_with_sync(cmd, wait_after=0.6, timeout=20.0)
    wait_quiescent(min_quiet=0.4, timeout=10.0)
    return ok


def draw_spline(points):
    if len(points) < 3:
        return False
    coords = "".join(f"{x},{y}\n" for x, y in points)
    cmd = f"_SPLINE\n{coords}\n"
    ok = send_cmd_with_sync(cmd, wait_after=0.8, timeout=25.0)
    wait_quiescent(min_quiet=0.5, timeout=15.0)
    return ok
