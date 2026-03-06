#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path

import tools.basic_graph_analyzer as bga


def _cad_root() -> Path:
    cur = Path(__file__).resolve()
    while cur.name.lower() != "cad":
        if cur.parent == cur:
            raise RuntimeError("cad root not found")
        cur = cur.parent
    return cur


def _selection_file() -> Path:
    return _cad_root() / "system" / "CAD_selection.py"


def test_list_funcs_on_cad_selection() -> None:
    inv = bga.list_top_level_functions_in_file(_selection_file())
    assert inv["ok"] is True
    names = [x["name"] for x in inv["functions"]]
    assert "select_objects_in_window_area" in names
    # CAD_selection.py 当前存在 2 个同名 get_attr（后者覆盖前者）
    assert names.count("get_attr") == 2


def test_callees_on_cad_selection() -> None:
    ret = bga.get_callees_in_script(
        root=_cad_root(),
        file=_selection_file(),
        func_name="select_objects_in_window_area",
        unique=True,
        with_locations=False,
    )
    assert ret["ok"] is True
    names = [x["name"] for x in ret["callees"]]
    assert "ss_select" in names
    assert "time.sleep" in names


def test_callers_limit_is_stable_and_post_sorted() -> None:
    root = _cad_root()
    full = bga.find_callers_in_project(root=root, target_name="ss_select", match_mode="short", limit=None)
    cut = bga.find_callers_in_project(root=root, target_name="ss_select", match_mode="short", limit=5)
    assert full["ok"] is True and cut["ok"] is True
    assert len(full["callers"]) >= 5
    assert cut["callers"] == full["callers"][:5]


def test_local_graph_handles_shadowed_defs() -> None:
    g = bga.build_local_call_graph_for_script(file=_selection_file())
    assert g["ok"] is True
    funcs = g["functions"]
    # 局部调用图应按“有效定义”去重，不应有重复函数名
    assert len(funcs) == len(set(funcs))
    assert "get_attr" in (g.get("shadowed_defs") or {})


def test_def_index_cache_path_is_root_scoped() -> None:
    p1 = bga.def_index_cache_path(root=_cad_root())
    p2 = bga.def_index_cache_path(root=_cad_root() / "system")
    assert p1 != p2
    assert p1.name.startswith("def_index_")
    assert p2.name.startswith("def_index_")
