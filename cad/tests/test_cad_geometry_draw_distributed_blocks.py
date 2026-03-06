#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single-function test: cad_geometry_draw.draw_distributed_blocks_on_entity
Requirement: use CAD_core lifecycle for DWG setup/teardown.
"""

import os
import sys
import time
from pathlib import Path

import pythoncom
from win32com.client import VARIANT

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


def _ensure_test_block(doc, block_name='OC_TEST_BLOCK_DIST'):
    blocks = doc.Blocks
    try:
        return blocks.Item(block_name)
    except Exception:
        base = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
        blk = blocks.Add(base, block_name)
        blk.AddCircle(base, 2.0)
        return blk


def test_draw_distributed_blocks_on_entity():
    tmp_path = str(Path(current) / 'tests' / '_tmp' / 'test_draw_distributed_blocks.dwg')
    _launch_cad()

    try:
        _prepare_temp_dwg(tmp_path)
        doc = resolve_doc(None)
        assert doc is not None, 'resolve_doc returned None'

        ms = doc.ModelSpace
        before = ms.Count

        line = draw.draw_line_wcs((0.0, 0.0, 0.0), (200.0, 0.0, 0.0), docname=None)
        wait_quiescent(min_quiet=0.3, timeout=10.0)
        assert line is not None, 'seed line draw failed'

        block_def = _ensure_test_block(doc)
        objs = draw.draw_distributed_blocks_on_entity(line, n=5, block=block_def, scale_factor=1.0, docname=None)
        wait_quiescent(min_quiet=0.3, timeout=10.0)

        after = ms.Count
        assert isinstance(objs, list), 'draw_distributed_blocks_on_entity did not return list'
        assert len(objs) == 5, f'expected 5 block refs, got {len(objs)}'
        assert after == before + 1 + 5, f'entity count mismatch before={before}, after={after}'
        assert all('BlockReference' in getattr(o, 'ObjectName', '') for o in objs), 'result objects should be block references'

        print('[PASS] draw_distributed_blocks_on_entity')
        return True
    finally:
        for action in (CAD_core.save_file, lambda: CAD_core.close_file('auto_save'), CAD_core.close_tarch_CAD_system):
            try:
                action()
            except Exception:
                pass


if __name__ == '__main__':
    ok = test_draw_distributed_blocks_on_entity()
    if not ok:
        raise SystemExit(1)
