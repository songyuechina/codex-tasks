#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single-function tests:
- cad_geometry_polyline.polyline_basic_info
- cad_geometry_polyline.polyline_is_closed
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


def test_polyline_basic_info_and_closed():
    tmp_path = str(Path(current) / 'tests' / '_tmp' / 'test_polyline_basic_info.dwg')
    _launch_cad()

    try:
        _prepare_temp_dwg(tmp_path)
        doc = resolve_doc(None)
        assert doc is not None, 'resolve_doc returned None'

        closed_obj = draw.draw_lwpolyline_wcs(
            vertices=[(0.0, 0.0, 0.0), (100.0, 0.0, 0.0), (100.0, 50.0, 0.0), (0.0, 50.0, 0.0)],
            closed=True,
            docname=None,
        )
        open_obj = draw.draw_lwpolyline_wcs(
            vertices=[(0.0, 100.0, 0.0), (100.0, 100.0, 0.0), (200.0, 100.0, 0.0)],
            closed=False,
            docname=None,
        )
        wait_quiescent(min_quiet=0.3, timeout=10.0)

        assert closed_obj is not None, 'closed polyline draw failed'
        assert open_obj is not None, 'open polyline draw failed'

        info = polyline.polyline_basic_info(closed_obj)
        assert info is not None, 'polyline_basic_info returned None'
        assert bool(info.get('is_closed', False)) is True, f'unexpected is_closed={info.get("is_closed")}'
        assert float(info.get('length', 0.0)) > 0.0, f'unexpected length={info.get("length")}'
        assert float(info.get('area', 0.0)) > 0.0, f'unexpected area={info.get("area")}'

        is_closed_closed = polyline.polyline_is_closed(closed_obj)
        is_closed_open = polyline.polyline_is_closed(open_obj)
        assert is_closed_closed is True, 'closed polyline detected as open'
        assert is_closed_open is False, 'open polyline detected as closed'

        print('[PASS] polyline_basic_info + polyline_is_closed')
        return True
    finally:
        for action in (CAD_core.save_file, lambda: CAD_core.close_file('auto_save'), CAD_core.close_tarch_CAD_system):
            try:
                action()
            except Exception:
                pass


if __name__ == '__main__':
    ok = test_polyline_basic_info_and_closed()
    if not ok:
        raise SystemExit(1)
