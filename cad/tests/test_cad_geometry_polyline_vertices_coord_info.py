#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single-function tests:
- cad_geometry_polyline.get_unique_vertices_from_polyline_com
- cad_geometry_polyline.polylines_to_coord_info
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


def _no_adjacent_duplicate(vertices, tol=1e-6):
    if not vertices:
        return True
    prev = vertices[0]
    for cur in vertices[1:]:
        if abs(cur[0] - prev[0]) <= tol and abs(cur[1] - prev[1]) <= tol:
            return False
        prev = cur
    return True


def test_polyline_vertices_and_coord_info():
    tmp_path = str(Path(current) / 'tests' / '_tmp' / 'test_polyline_vertices_coord_info.dwg')
    _launch_cad()

    try:
        _prepare_temp_dwg(tmp_path)
        doc = resolve_doc(None)
        assert doc is not None, 'resolve_doc returned None'

        closed_obj = draw.draw_lwpolyline_wcs(
            vertices=[(0.0, 0.0, 0.0), (80.0, 0.0, 0.0), (80.0, 0.0, 0.0), (80.0, 40.0, 0.0), (0.0, 40.0, 0.0)],
            closed=True,
            docname=None,
        )
        open_obj = draw.draw_lwpolyline_wcs(
            vertices=[(0.0, 100.0, 0.0), (100.0, 100.0, 0.0), (200.0, 110.0, 0.0)],
            closed=False,
            docname=None,
        )
        wait_quiescent(min_quiet=0.3, timeout=10.0)

        assert closed_obj is not None, 'closed polyline draw failed'
        assert open_obj is not None, 'open polyline draw failed'

        verts = polyline.get_unique_vertices_from_polyline_com(closed_obj)
        assert isinstance(verts, list), 'get_unique_vertices_from_polyline_com did not return list'
        assert len(verts) >= 4, f'unexpected vertex count={len(verts)}'
        assert _no_adjacent_duplicate(verts), 'adjacent duplicate vertices still exist'

        infos = polyline.polylines_to_coord_info([closed_obj, open_obj])
        assert isinstance(infos, list), 'polylines_to_coord_info did not return list'
        assert len(infos) == 2, f'unexpected info count={len(infos)}'
        assert bool(infos[0].get('closed', False)) is True, 'first polyline should be closed'
        assert bool(infos[1].get('closed', True)) is False, 'second polyline should be open'
        assert len(infos[0].get('vertices', [])) >= 4, 'closed polyline vertices missing'
        assert len(infos[1].get('vertices', [])) >= 2, 'open polyline vertices missing'

        print('[PASS] get_unique_vertices_from_polyline_com + polylines_to_coord_info')
        return True
    finally:
        for action in (CAD_core.save_file, lambda: CAD_core.close_file('auto_save'), CAD_core.close_tarch_CAD_system):
            try:
                action()
            except Exception:
                pass


if __name__ == '__main__':
    ok = test_polyline_vertices_and_coord_info()
    if not ok:
        raise SystemExit(1)
