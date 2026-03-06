#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single-function test: cad_geometry_polyline.explode_polylines
Requirement: use CAD_core lifecycle for DWG setup/teardown.
"""

import os
import sys
import time
from pathlib import Path

current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current:
        raise Exception('Cannot find project root')
    current = current.parent
sys.path.insert(0, str(current))

os.environ.setdefault('PYTHONUTF8', '1')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

from system import CAD_core
from system.licad import resolve_doc
from system.CAD_coordination import wait_quiescent
from library import cad_geometry_draw as draw
from library import cad_geometry_polyline as polyline


def _launch_cad():
    for attempt in range(1, 4):
        try:
            CAD_core.launch_tarch_CAD_system()
            time.sleep(2.0)
            return
        except Exception as exc:
            print(f'[WARN] launch CAD failed attempt {attempt}/3: {exc}')
            try:
                CAD_core.close_tarch_CAD_system()
            except Exception:
                pass
            time.sleep(3.0)
    raise RuntimeError('CAD launch failed')


def _prepare_temp_dwg(path):
    os.makedirs(Path(path).parent, exist_ok=True)
    CAD_core.new_file(output_path=path, close_after=False)
    wait_quiescent(min_quiet=0.5, timeout=30.0)


def test_explode_polylines():
    tmp_path = str(Path(current) / 'tests' / '_tmp' / 'test_explode_polylines.dwg')
    _launch_cad()

    try:
        _prepare_temp_dwg(tmp_path)
        doc = resolve_doc(None)
        assert doc is not None, 'resolve_doc returned None'

        ms = doc.ModelSpace
        before = ms.Count

        pl = draw.draw_lwpolyline_wcs(
            vertices=[(0.0, 0.0, 0.0), (100.0, 0.0, 0.0), (100.0, 60.0, 0.0), (0.0, 60.0, 0.0)],
            closed=True,
            docname=None,
        )
        wait_quiescent(min_quiet=0.3, timeout=10.0)
        mid = ms.Count

        assert pl is not None, 'draw_lwpolyline_wcs returned None'
        assert mid == before + 1, f'polyline count mismatch before={before}, after={mid}'

        parts = polyline.explode_polylines([pl], docname=None)
        wait_quiescent(min_quiet=0.3, timeout=10.0)
        after = ms.Count

        assert isinstance(parts, list), 'explode_polylines did not return list'
        assert len(parts) >= 1, f'expected exploded parts, got {len(parts)}'
        assert after >= mid, f'entity count did not grow after explode mid={mid}, after={after}'

        print('[PASS] explode_polylines')
        return True
    finally:
        for action in (CAD_core.save_file, lambda: CAD_core.close_file('auto_save'), CAD_core.close_tarch_CAD_system):
            try:
                action()
            except Exception:
                pass


if __name__ == '__main__':
    ok = test_explode_polylines()
    if not ok:
        raise SystemExit(1)
