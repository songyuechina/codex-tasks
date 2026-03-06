#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# D:/codex-tasks/cad/tools/basic_graph_analyzer.py

"""
basic_graph_analyzer.py  (实 -> 虚：基础“调用图/索引”层)

设计目标（你描述的“信息压缩影子”）：
- 默认面向 /cad 全局：快速回答“谁调用谁”“在哪里定义”“脚本入口/极大函数”
- 也支持单脚本内：列函数、看本脚本内调用关系、找极大函数
- 纯静态 AST：快、可缓存、token 省（输出是小 JSON，而不是大段源码）
- 不依赖 LLM / DB；可作为 function_analyzer.py（语义层）的地基

核心能力：
1) 目标函数（在某脚本内）引用了哪些函数（callees），并可解析到项目内定义点（可选）
2) 哪些函数引用了目标函数（callers，project-wide）
3) 一个脚本中包含哪些顶层函数
4) 一个脚本内的“极大函数”（in_degree==0 且 out_degree>0）
5) 全项目 def 索引缓存（func_name -> defs[]），加速解析/反查

用法示例：
  # 0) 全项目建立 def 索引（建议先跑一次）
  python basic_graph_analyzer.py build-index --root D:/codex-tasks/cad

  # 1) 列出脚本顶层函数
  python basic_graph_analyzer.py list-funcs --file D:/codex-tasks/cad/scripts/CAD_basic.py

  # 2) 看某函数调用了哪些函数（同脚本抽 calls；并尝试解析到项目内定义点）
  python basic_graph_analyzer.py callees --root D:/codex-tasks/cad --file D:/codex-tasks/cad/scripts/CAD_basic.py --func Founcx --resolve

  # 3) 反向查：全项目里哪些地方调用了某函数名（简单名匹配）
  python basic_graph_analyzer.py callers --root D:/codex-tasks/cad --target Founcx

  # 4) 分析一个脚本的极大函数
  python basic_graph_analyzer.py maximals --file D:/codex-tasks/cad/scripts/CAD_basic.py

输出默认打印 JSON（你也可以 --out 写文件）。
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

# -----------------------------------------------------------------------------
# 0) 路径：自动定位 cad 根目录（保持你项目风格）
# -----------------------------------------------------------------------------
import sys

_current = Path(__file__).resolve()
while _current.name.lower() != "cad":
    if _current.parent == _current:
        raise RuntimeError("找不到 cad 根目录（basic_graph_analyzer.py 需要放在 cad/tools 下）")
    _current = _current.parent

CAD_ROOT = _current
if str(CAD_ROOT) not in sys.path:
    sys.path.insert(0, str(CAD_ROOT))


# -----------------------------------------------------------------------------
# 1) 配置
# -----------------------------------------------------------------------------
DEFAULT_EXCLUDE_DIRS = ("__pycache__", ".git", ".venv", "venv", ".mypy_cache", ".pytest_cache")

# 本地缓存目录：cad/tools/_cache/basic_graph
CACHE_DIR = CAD_ROOT / "tools" / "_cache" / "basic_graph"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

DEF_INDEX_CACHE_NAME = "def_index.json"


# -----------------------------------------------------------------------------
# 2) 小工具
# -----------------------------------------------------------------------------
def _now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def _safe_read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")


def _json_dump(obj: Any, *, pretty: bool = True) -> str:
    if pretty:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    return json.dumps(obj, ensure_ascii=False)


def _norm_path(p: str | Path) -> str:
    return str(Path(p).resolve()).replace("\\", "/")


def _rel_to_root(p: str | Path, root: str | Path) -> str:
    try:
        return str(Path(p).resolve().relative_to(Path(root).resolve())).replace("\\", "/")
    except Exception:
        return _norm_path(p)


def _module_qual_from_file(p: str | Path, root: str | Path) -> str:
    rel = _rel_to_root(p, root)
    if rel.lower().endswith(".py"):
        rel = rel[:-3]
    rel = rel.replace("/", ".")
    # 你的项目里可能出现 cad.xxx：这里做轻微规整（可按你习惯再改）
    if rel.startswith("cad."):
        rel = rel[4:]
    return rel


def build_qualified_name(file: str | Path, func_name: str, root: str | Path) -> str:
    return f"{_module_qual_from_file(file, root)}:{func_name}"


def _iter_py_files(root: str | Path, *, exclude_dirs: Iterable[str] = DEFAULT_EXCLUDE_DIRS) -> Iterable[Path]:
    rootp = Path(root)
    for p in rootp.rglob("*.py"):
        if any(part in exclude_dirs for part in p.parts):
            continue
        yield p


def _short_name(call_name: str) -> str:
    """a.b.c -> c"""
    return (call_name or "").split(".")[-1]


# -----------------------------------------------------------------------------
# 3) AST：列顶层函数
# -----------------------------------------------------------------------------
def list_top_level_functions_in_file(file: str | Path) -> dict:
    """
    输出：
    {
      ok: bool,
      file: "...",
      functions: [
        {name, type, lineno, end_lineno, args: {params, vararg, kwarg, defaults}}
      ],
      error: str|None
    }
    """
    p = Path(file)
    if not p.exists():
        return {"ok": False, "file": _norm_path(p), "functions": [], "error": "file not found"}

    try:
        src = _safe_read_text(p)
        tree = ast.parse(src, filename=str(p))
    except Exception as e:
        return {"ok": False, "file": _norm_path(p), "functions": [], "error": f"parse failed: {e}"}

    def _sig(fn: ast.AST) -> dict:
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return {"params": [], "defaults": {}, "vararg": None, "kwarg": None}
        args = fn.args
        params = [a.arg for a in args.args if a.arg != "self"]
        defaults = [None] * (len(args.args) - len(args.defaults)) + list(args.defaults)
        defaults_map: dict[str, Any] = {}
        for a, d in zip(args.args, defaults):
            if a.arg == "self":
                continue
            if d is None:
                continue
            try:
                defaults_map[a.arg] = ast.literal_eval(d)
            except Exception:
                defaults_map[a.arg] = "<expr>"
        return {
            "params": params,
            "defaults": defaults_map,
            "vararg": args.vararg.arg if args.vararg else None,
            "kwarg": args.kwarg.arg if args.kwarg else None,
        }

    out = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            out.append({
                "name": node.name,
                "type": "def",
                "lineno": getattr(node, "lineno", None),
                "end_lineno": getattr(node, "end_lineno", None),
                "args": _sig(node),
            })
        elif isinstance(node, ast.AsyncFunctionDef):
            out.append({
                "name": node.name,
                "type": "async def",
                "lineno": getattr(node, "lineno", None),
                "end_lineno": getattr(node, "end_lineno", None),
                "args": _sig(node),
            })

    out.sort(key=lambda x: (x.get("lineno") or 0, x.get("name") or ""))
    return {"ok": True, "file": _norm_path(p), "functions": out, "error": None}


# -----------------------------------------------------------------------------
# 4) AST：抽 calls（带上下文：所在函数/类）
# -----------------------------------------------------------------------------
@dataclass
class CallSite:
    call_name: str
    call_short: str
    lineno: Optional[int]
    col: Optional[int]
    caller_func: Optional[str]      # 外层函数名
    caller_class: Optional[str]     # 外层类名（若在类里）
    file: str


class _CallsiteCollector(ast.NodeVisitor):
    """
    扫描整个模块，记录每个 Call 节点在哪个 “外层函数/类” 中出现。
    - 只记录在函数/方法体里的 calls（顶层直接 call 也可以记录为 caller_func=None）
    - 进入子作用域（嵌套 def/class）会更新上下文
    """
    def __init__(self, file: str):
        self.file = _norm_path(file)
        self._func_stack: list[str] = []
        self._class_stack: list[str] = []
        self.calls: list[CallSite] = []

    def _name_of(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            left = self._name_of(node.value)
            return f"{left}.{node.attr}" if left else node.attr
        return ""

    def visit_ClassDef(self, node: ast.ClassDef):
        self._class_stack.append(node.name)
        self.generic_visit(node)
        self._class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._func_stack.append(node.name)
        self.generic_visit(node)
        self._func_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._func_stack.append(node.name)
        self.generic_visit(node)
        self._func_stack.pop()

    def visit_Call(self, node: ast.Call):
        name = self._name_of(node.func)
        if name:
            self.calls.append(
                CallSite(
                    call_name=name,
                    call_short=_short_name(name),
                    lineno=getattr(node, "lineno", None),
                    col=getattr(node, "col_offset", None),
                    caller_func=(self._func_stack[-1] if self._func_stack else None),
                    caller_class=(self._class_stack[-1] if self._class_stack else None),
                    file=self.file,
                )
            )
        self.generic_visit(node)


# -----------------------------------------------------------------------------
# 5) 单函数：callees（同脚本内：从目标函数体抽 calls）
# -----------------------------------------------------------------------------
class _InnerCallCollector(ast.NodeVisitor):
    """
    仅遍历目标函数体，并避免进入内部嵌套 def/class（避免把子作用域混进来）
    """
    def __init__(self):
        self.items: list[dict] = []

    def _name_of(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            left = self._name_of(node.value)
            return f"{left}.{node.attr}" if left else node.attr
        return ""

    def visit_Call(self, node: ast.Call):
        name = self._name_of(node.func)
        if name:
            self.items.append({"name": name, "short": _short_name(name), "line": getattr(node, "lineno", None), "col": getattr(node, "col_offset", None)})
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return

    def visit_ClassDef(self, node: ast.ClassDef):
        return


def get_callees_in_script(
    *,
    root: str | Path,
    file: str | Path,
    func_name: str,
    unique: bool = True,
    with_locations: bool = True,
) -> dict:
    """
    输出：
    {
      ok, file, func,
      target: {lineno,end_lineno, qualified_name},
      callees: [ {name, short, line, col}, ... ]  或去掉 line/col
    }
    """
    p = Path(file)
    if not p.exists():
        return {"ok": False, "error": "file not found", "file": _norm_path(p), "func": func_name, "target": None, "callees": []}

    try:
        src = _safe_read_text(p)
        tree = ast.parse(src, filename=str(p))
    except Exception as e:
        return {"ok": False, "error": f"parse failed: {e}", "file": _norm_path(p), "func": func_name, "target": None, "callees": []}

    target = None
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
            target = node
            break

    if target is None:
        return {"ok": False, "error": "function not found (top-level)", "file": _norm_path(p), "func": func_name, "target": None, "callees": []}

    collector = _InnerCallCollector()
    for stmt in getattr(target, "body", []) or []:
        collector.visit(stmt)

    items = collector.items
    if unique:
        seen = set()
        out = []
        for it in items:
            k = it["name"]
            if k in seen:
                continue
            seen.add(k)
            out.append(it)
        items = out

    if not with_locations:
        items = [{"name": it["name"], "short": it["short"]} for it in items]

    return {
        "ok": True,
        "error": None,
        "file": _norm_path(p),
        "func": func_name,
        "target": {
            "lineno": getattr(target, "lineno", None),
            "end_lineno": getattr(target, "end_lineno", None),
            "qualified_name": build_qualified_name(str(p), func_name, root),
        },
        "callees": items,
    }


# -----------------------------------------------------------------------------
# 6) 全项目：callers（反向引用）
# -----------------------------------------------------------------------------
def find_callers_in_project(
    *,
    root: str | Path,
    target_name: str,
    exclude_dirs: Iterable[str] = DEFAULT_EXCLUDE_DIRS,
    match_mode: str = "short",   # short: 匹配调用名末尾；full: 匹配完整调用名
    limit: Optional[int] = None,
) -> dict:
    """
    在 root 下扫描所有 .py，找 Call 节点调用到 target_name 的位置。
    - match_mode="short": 调用名 foo.bar.baz() 的 baz == target_name 即算命中（更实用）
    - match_mode="full": 必须 call_name == target_name

    输出：
    {
      ok, root, target, match_mode,
      callers: [
        {file, line, col, call_name, caller_func, caller_class}
      ],
      error
    }
    """
    rootp = Path(root)
    if not rootp.exists():
        return {"ok": False, "root": _norm_path(rootp), "target": target_name, "match_mode": match_mode, "callers": [], "error": "root not found"}

    callers: list[dict] = []
    want = (target_name or "").strip()
    if not want:
        return {"ok": False, "root": _norm_path(rootp), "target": target_name, "match_mode": match_mode, "callers": [], "error": "empty target_name"}

    for p in sorted(_iter_py_files(rootp, exclude_dirs=exclude_dirs), key=lambda x: _norm_path(x)):
        try:
            src = _safe_read_text(p)
            tree = ast.parse(src, filename=str(p))
        except Exception:
            continue

        col = _CallsiteCollector(str(p))
        col.visit(tree)

        for cs in col.calls:
            hit = False
            if match_mode == "full":
                hit = (cs.call_name == want)
            else:
                hit = (cs.call_short == want)

            if hit:
                callers.append({
                    "file": cs.file,
                    "line": cs.lineno,
                    "col": cs.col,
                    "call_name": cs.call_name,
                    "caller_func": cs.caller_func,
                    "caller_class": cs.caller_class,
                })

    callers.sort(key=lambda x: (x.get("file") or "", x.get("line") or 0, x.get("col") or 0))
    if limit is not None:
        callers = callers[: max(0, int(limit))]
    return {"ok": True, "root": _norm_path(rootp), "target": want, "match_mode": match_mode, "callers": callers, "error": None}


# -----------------------------------------------------------------------------
# 7) Def 索引：build/load/resolve
# -----------------------------------------------------------------------------
def def_index_cache_path(*, root: str | Path) -> Path:
    # 不同 root 可共存：按 root 绝对路径做哈希
    root_norm = _norm_path(root)
    key = hashlib.md5(root_norm.encode("utf-8")).hexdigest()[:10]
    return CACHE_DIR / f"def_index_{key}.json"


def build_def_index(
    *,
    root: str | Path,
    exclude_dirs: Iterable[str] = DEFAULT_EXCLUDE_DIRS,
    include_async: bool = True,
) -> dict:
    """
    构建全项目 def 索引：
      index[name] = [ {file, lineno, end_lineno, type, qualified_name}, ... ]

    返回：
    { ok, root, built_at, total_defs, index }
    """
    rootp = Path(root)
    if not rootp.exists():
        return {"ok": False, "root": _norm_path(rootp), "built_at": _now_str(), "total_defs": 0, "index": {}, "error": "root not found"}

    index: dict[str, list[dict]] = {}
    total = 0

    for p in _iter_py_files(rootp, exclude_dirs=exclude_dirs):
        try:
            src = _safe_read_text(p)
            tree = ast.parse(src, filename=str(p))
        except Exception:
            continue

        for node in tree.body:
            if isinstance(node, ast.FunctionDef) or (include_async and isinstance(node, ast.AsyncFunctionDef)):
                fn = node.name
                rec = {
                    "file": _norm_path(p),
                    "lineno": getattr(node, "lineno", None),
                    "end_lineno": getattr(node, "end_lineno", None),
                    "type": ("async def" if isinstance(node, ast.AsyncFunctionDef) else "def"),
                    "qualified_name": build_qualified_name(str(p), fn, rootp),
                }
                index.setdefault(fn, []).append(rec)
                total += 1

    # 稳定排序
    for k, lst in index.items():
        lst.sort(key=lambda x: (x.get("file") or "", x.get("lineno") or 0))

    return {"ok": True, "root": _norm_path(rootp), "built_at": _now_str(), "total_defs": total, "index": index, "error": None}


def save_def_index_to_cache(*, root: str | Path, payload: dict) -> dict:
    try:
        fp = def_index_cache_path(root=root)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(_json_dump(payload, pretty=True), encoding="utf-8")
        return {"ok": True, "path": _norm_path(fp), "error": None}
    except Exception as e:
        return {"ok": False, "path": None, "error": str(e)}


def load_def_index_from_cache(*, root: str | Path) -> dict:
    fp = def_index_cache_path(root=root)
    # 兼容旧缓存命名（def_index.json）
    if not fp.exists():
        legacy_fp = CACHE_DIR / DEF_INDEX_CACHE_NAME
        fp = legacy_fp if legacy_fp.exists() else fp
    if not fp.exists():
        return {"ok": True, "hit": False, "path": _norm_path(def_index_cache_path(root=root)), "payload": None, "error": None}
    try:
        obj = json.loads(_safe_read_text(fp))
        return {"ok": True, "hit": True, "path": _norm_path(fp), "payload": obj, "error": None}
    except Exception as e:
        return {"ok": False, "hit": False, "path": _norm_path(fp), "payload": None, "error": str(e)}


def resolve_names_to_defs(
    *,
    names: list[str],
    def_index: dict,
    mode: str = "short",  # short: 用末尾名解析；full: 用完整名（一般 def_index 只有函数名键）
    limit_each: int = 10,
) -> dict:
    """
    输入 calls 名称列表，尝试映射到项目内定义点（可能一对多）。
    返回：
    {
      ok,
      resolved: { call_name: [defrec...] },
      unresolved: [call_name...]
    }
    """
    idx = (def_index or {}).get("index") if isinstance(def_index, dict) and "index" in def_index else def_index
    if not isinstance(idx, dict):
        return {"ok": False, "resolved": {}, "unresolved": names, "error": "bad def_index"}

    resolved: dict[str, list[dict]] = {}
    unresolved: list[str] = []

    for n in names:
        key = _short_name(n) if mode == "short" else n
        hits = idx.get(key)
        if not hits:
            unresolved.append(n)
        else:
            resolved[n] = list(hits)[: int(limit_each)]

    return {"ok": True, "resolved": resolved, "unresolved": unresolved, "error": None}


# -----------------------------------------------------------------------------
# 8) 脚本内调用图 + 极大函数
# -----------------------------------------------------------------------------
def build_local_call_graph_for_script(*, file: str | Path) -> dict:
    """
    构建“脚本顶层函数之间”的调用图：
      edges[f] = set(g)  (g 也必须是本脚本顶层函数)

    输出：
    {
      ok, file,
      functions: [...],
      edges: {f: [g1,g2,...], ...},
      degrees: {f: {in,out}, ...}
    }
    """
    inv = list_top_level_functions_in_file(file)
    if not inv.get("ok"):
        return {"ok": False, "file": inv.get("file"), "functions": [], "edges": {}, "degrees": {}, "error": inv.get("error")}

    funcs_all = [x["name"] for x in inv.get("functions", []) if x.get("name")]
    if not funcs_all:
        p = Path(file)
        return {"ok": True, "file": _norm_path(p), "functions": [], "edges": {}, "degrees": {}, "shadowed_defs": {}, "error": None}

    p = Path(file)
    src = _safe_read_text(p)
    try:
        tree = ast.parse(src, filename=str(p))
    except Exception as e:
        return {"ok": False, "file": _norm_path(p), "functions": funcs_all, "edges": {}, "degrees": {}, "shadowed_defs": {}, "error": f"parse failed: {e}"}

    # 找每个顶层函数节点（同名函数按 Python 语义：后定义覆盖前定义）
    fn_nodes_all: dict[str, list[ast.AST]] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fn_nodes_all.setdefault(node.name, []).append(node)

    fn_nodes_effective: dict[str, ast.AST] = {}
    shadowed_defs: dict[str, list[int]] = {}
    for name, nodes in fn_nodes_all.items():
        fn_nodes_effective[name] = nodes[-1]
        if len(nodes) > 1:
            # 记录被覆盖定义的位置（不含最后一个有效定义）
            shadowed_defs[name] = [int(getattr(n, "lineno", 0) or 0) for n in nodes[:-1]]

    funcs = sorted(fn_nodes_effective.keys(), key=lambda n: (getattr(fn_nodes_effective[n], "lineno", 0) or 0, n))
    func_set = set(funcs)
    edges: dict[str, set[str]] = {f: set() for f in funcs}

    for f, node in fn_nodes_effective.items():
        collector = _InnerCallCollector()
        for stmt in getattr(node, "body", []) or []:
            collector.visit(stmt)
        called_shorts = [_short_name(it["name"]) for it in collector.items if it.get("name")]
        for s in called_shorts:
            if s in func_set and s != f:
                edges[f].add(s)

    # degrees
    indeg = {f: 0 for f in funcs}
    outdeg = {f: len(edges[f]) for f in funcs}
    for f in funcs:
        for g in edges[f]:
            indeg[g] += 1

    edges_out = {k: sorted(list(v)) for k, v in edges.items()}
    degrees = {f: {"in": indeg[f], "out": outdeg[f]} for f in funcs}

    return {
        "ok": True,
        "file": _norm_path(p),
        "functions": funcs,
        "edges": edges_out,
        "degrees": degrees,
        "shadowed_defs": shadowed_defs,
        "error": None,
    }


def find_maximal_functions_in_script(*, file: str | Path) -> dict:
    """
    极大函数（你定义的脚本内入口元）：
      in_degree == 0 且 out_degree > 0

    同时给出 orphans：
      in_degree == 0 且 out_degree == 0
    """
    g = build_local_call_graph_for_script(file=file)
    if not g.get("ok"):
        return {"ok": False, "file": g.get("file"), "maximals": [], "orphans": [], "graph": None, "error": g.get("error")}

    degrees = g.get("degrees") or {}
    edges = g.get("edges") or {}

    maximals = []
    orphans = []
    for f, d in degrees.items():
        din = int((d or {}).get("in") or 0)
        dout = int((d or {}).get("out") or 0)
        if din == 0 and dout > 0:
            maximals.append({"name": f, "in_degree": din, "out_degree": dout, "out_calls_local": edges.get(f) or []})
        elif din == 0 and dout == 0:
            orphans.append({"name": f, "in_degree": din, "out_degree": dout, "out_calls_local": []})

    maximals.sort(key=lambda x: (-x.get("out_degree", 0), x.get("name") or ""))
    orphans.sort(key=lambda x: (x.get("name") or ""))

    return {"ok": True, "file": g.get("file"), "maximals": maximals, "orphans": orphans, "graph": g, "error": None}


# -----------------------------------------------------------------------------
# 9) 邻域摘要（可选但很省 token）
# -----------------------------------------------------------------------------
def get_neighbors_summary(
    *,
    root: str | Path,
    file: str | Path,
    func_name: str,
    target_name_for_callers: Optional[str] = None,
    resolve: bool = False,
    match_mode: str = "short",
    callers_limit: Optional[int] = 200,
) -> dict:
    """
    一次性给“邻域摘要”：
    - callees（目标函数调用谁）
    - callers（谁调用目标函数名；默认用 func_name）
    - 可选 resolve：把 callees 解析到项目内 def
    """
    cal = get_callees_in_script(root=root, file=file, func_name=func_name, unique=True, with_locations=True)
    if not cal.get("ok"):
        return {"ok": False, "error": f"callees failed: {cal.get('error')}", "callees": None, "callers": None, "resolved": None}

    tname = (target_name_for_callers or func_name).strip()
    callers = find_callers_in_project(root=root, target_name=tname, match_mode=match_mode, limit=callers_limit)

    resolved = None
    if resolve:
        # def index：优先读缓存，未命中则现场建（你也可以改成强制先 build-index）
        idx = load_def_index_from_cache(root=root)
        if not (idx.get("ok") and idx.get("hit")):
            built = build_def_index(root=root)
            save_def_index_to_cache(root=root, payload=built)
            idx_payload = built
        else:
            idx_payload = idx.get("payload")

        callees_names = [x.get("name") for x in (cal.get("callees") or []) if isinstance(x, dict) and x.get("name")]
        resolved = resolve_names_to_defs(names=callees_names, def_index=idx_payload, mode="short")

    return {
        "ok": True,
        "error": None,
        "root": _norm_path(root),
        "file": cal.get("file"),
        "func": func_name,
        "callees": cal,
        "callers": callers,
        "resolved": resolved,
    }


# -----------------------------------------------------------------------------
# 10) CLI
# -----------------------------------------------------------------------------
def _write_or_print(*, out: Optional[str], obj: Any, pretty: bool = True) -> None:
    s = _json_dump(obj, pretty=pretty)
    if out:
        Path(out).write_text(s + "\n", encoding="utf-8")
    else:
        print(s)


def main() -> None:
    ap = argparse.ArgumentParser(description="CAD basic graph analyzer (实->虚 基础层)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build-index", help="全项目建立 def 索引并写入本地缓存")
    p_build.add_argument("--root", default=str(CAD_ROOT), help="cad 根目录（默认自动 cad root）")
    p_build.add_argument("--out", default=None, help="可选：把 index JSON 输出到文件（同时也会写缓存）")

    p_list = sub.add_parser("list-funcs", help="列出脚本顶层函数")
    p_list.add_argument("--file", required=True, help="脚本路径")
    p_list.add_argument("--out", default=None)

    p_callees = sub.add_parser("callees", help="目标函数调用了哪些函数（同脚本内抽 calls）")
    p_callees.add_argument("--root", default=str(CAD_ROOT), help="cad 根目录（用于 qualified_name）")
    p_callees.add_argument("--file", required=True)
    p_callees.add_argument("--func", required=True)
    p_callees.add_argument("--no-loc", action="store_true", help="不输出调用点行号")
    p_callees.add_argument("--resolve", action="store_true", help="尝试把 callees 解析到项目内定义点（需要 def index）")
    p_callees.add_argument("--out", default=None)

    p_callers = sub.add_parser("callers", help="全项目反向查：哪些地方调用了 target 函数名")
    p_callers.add_argument("--root", default=str(CAD_ROOT))
    p_callers.add_argument("--target", required=True)
    p_callers.add_argument("--match", choices=["short", "full"], default="short")
    p_callers.add_argument("--limit", type=int, default=None)
    p_callers.add_argument("--out", default=None)

    p_max = sub.add_parser("maximals", help="分析脚本内极大函数（入口元）")
    p_max.add_argument("--file", required=True)
    p_max.add_argument("--out", default=None)

    p_nb = sub.add_parser("neighbors", help="邻域摘要：callees + callers (+可选 resolve)")
    p_nb.add_argument("--root", default=str(CAD_ROOT))
    p_nb.add_argument("--file", required=True)
    p_nb.add_argument("--func", required=True)
    p_nb.add_argument("--target", default=None, help="用于 callers 搜索的函数名（默认=--func）")
    p_nb.add_argument("--resolve", action="store_true")
    p_nb.add_argument("--match", choices=["short", "full"], default="short")
    p_nb.add_argument("--limit", type=int, default=200)
    p_nb.add_argument("--out", default=None)

    args = ap.parse_args()

    if args.cmd == "build-index":
        payload = build_def_index(root=args.root)
        # 同时写缓存（主用途）
        save_def_index_to_cache(root=args.root, payload=payload)
        _write_or_print(out=args.out, obj=payload)

    elif args.cmd == "list-funcs":
        payload = list_top_level_functions_in_file(args.file)
        _write_or_print(out=args.out, obj=payload)

    elif args.cmd == "callees":
        cal = get_callees_in_script(root=args.root, file=args.file, func_name=args.func, unique=True, with_locations=(not args.no_loc))
        if not args.resolve:
            _write_or_print(out=args.out, obj=cal)
            return

        idx = load_def_index_from_cache(root=args.root)
        if not (idx.get("ok") and idx.get("hit")):
            built = build_def_index(root=args.root)
            save_def_index_to_cache(root=args.root, payload=built)
            idx_payload = built
        else:
            idx_payload = idx.get("payload")

        callees_names = [x.get("name") for x in (cal.get("callees") or []) if isinstance(x, dict) and x.get("name")]
        resolved = resolve_names_to_defs(names=callees_names, def_index=idx_payload, mode="short")

        payload = {"callees": cal, "resolved": resolved, "def_index_cache_hit": bool(idx.get("hit"))}
        _write_or_print(out=args.out, obj=payload)

    elif args.cmd == "callers":
        payload = find_callers_in_project(root=args.root, target_name=args.target, match_mode=args.match, limit=args.limit)
        _write_or_print(out=args.out, obj=payload)

    elif args.cmd == "maximals":
        payload = find_maximal_functions_in_script(file=args.file)
        _write_or_print(out=args.out, obj=payload)

    elif args.cmd == "neighbors":
        payload = get_neighbors_summary(
            root=args.root,
            file=args.file,
            func_name=args.func,
            target_name_for_callers=args.target,
            resolve=bool(args.resolve),
            match_mode=args.match,
            callers_limit=args.limit,
        )
        _write_or_print(out=args.out, obj=payload)


if __name__ == "__main__":
    main()
