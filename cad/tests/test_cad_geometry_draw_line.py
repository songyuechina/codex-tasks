#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单函数测试：cad_geometry_draw.draw_line_wcs
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
from library import cad_geometry_draw as draw


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


def test_draw_line_wcs():
    tmp_path = str(Path(current) / "tests" / "_tmp" / "test_draw_line.dwg")

    _launch_cad()

    try:
        _prepare_temp_dwg(tmp_path)
        doc = resolve_doc(None)
        assert doc is not None, "doc 解析失败"
        ms = doc.ModelSpace
        before = ms.Count

        obj = draw.draw_line_wcs((0.0, 0.0, 0.0), (100.0, 0.0, 0.0), docname=None)
        wait_quiescent(min_quiet=0.3, timeout=10.0)

        after = ms.Count
        assert obj is not None, "draw_line_wcs 返回 None"
        assert after == before + 1, f"对象数量未增加: before={before}, after={after}"
        assert "Line" in getattr(obj, "ObjectName", ""), f"对象类型异常: {getattr(obj, 'ObjectName', '')}"

        print("[PASS] draw_line_wcs")
        return True
    finally:
        try:
            CAD_core.save_file()
        except Exception:
            pass
        try:
            CAD_core.close_file("auto_save")
        except Exception:
            pass
        try:
            CAD_core.close_tarch_CAD_system()
        except Exception:
            pass


if __name__ == "__main__":
    ok = test_draw_line_wcs()
    if not ok:
        raise SystemExit(1)
