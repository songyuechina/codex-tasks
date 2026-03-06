#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单函数测试：cad_geometry_draw.draw_point_wcs
要求：使用 CAD_core 启动/关闭系统与 DWG 操作
"""

# ================= 路径引导 =================
import sys
import os

# 统一 UTF-8 输出，避免日志表情触发 GBK 编码异常
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current:
        raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

# ================= 标准库 =================
import time

# ================= 系统模块 =================
from system import CAD_core
from system.licad import resolve_doc
from system.CAD_coordination import wait_quiescent

# 被测模块
from library import cad_geometry_draw as draw


def _prepare_temp_dwg(path):
    """创建/打开测试 DWG。"""
    os.makedirs(Path(path).parent, exist_ok=True)
    CAD_core.new_file(output_path=path, close_after=False)
    wait_quiescent(min_quiet=0.5, timeout=30.0)


def test_draw_point_wcs():
    """测试 draw_point_wcs：创建点并验证数量与类型。"""
    tmp_path = str(Path(current) / "tests" / "_tmp" / "test_draw_point.dwg")

    # 1) 启动 CAD
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

    try:
        # 2) 新建/打开 DWG
        _prepare_temp_dwg(tmp_path)

        # 3) 获取文档
        doc = resolve_doc(None)
        assert doc is not None, "doc 解析失败"
        ms = doc.ModelSpace

        # 4) 记录初始数量
        before = ms.Count

        # 5) 绘制点
        obj = draw.draw_point_wcs((100.0, 200.0, 0.0), docname=None)
        wait_quiescent(min_quiet=0.3, timeout=10.0)

        # 6) 验证
        after = ms.Count
        assert obj is not None, "draw_point_wcs 返回 None"
        assert after == before + 1, f"对象数量未增加: before={before}, after={after}"
        assert "Point" in getattr(obj, "ObjectName", ""), f"对象类型异常: {getattr(obj, 'ObjectName', '')}"

        print("[PASS] draw_point_wcs")
        return True
    finally:
        # 7) 保存并关闭
        try:
            CAD_core.save_file()
        except Exception:
            pass
        try:
            CAD_core.close_file("auto_save")
        except Exception:
            pass
        # 8) 关闭 CAD
        try:
            CAD_core.close_tarch_CAD_system()
        except Exception:
            pass


if __name__ == "__main__":
    ok = test_draw_point_wcs()
    if not ok:
        raise SystemExit(1)
