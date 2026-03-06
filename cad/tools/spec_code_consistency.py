"""spec 与代码一致性检查

用法：
  python spec_code_consistency.py --spec D:/codex-tasks/cad/analysis/flows/select_maxrect_polylines_1.spec.yaml
"""

import argparse
import ast
from pathlib import Path
from typing import Any

import yaml

IGNORE_CALLS = {
    "len", "min", "max", "abs", "range", "enumerate", "sorted", "set", "list", "dict",
    "float", "int", "str", "print", "sum", "any", "all", "isinstance", "getattr",
    "setattr", "globals", "locals", "type", "zip", "map", "filter"
}
IGNORE_PREFIXES = (
    "sys_logger.",
    "logger.",
)

CAD_MODULE_HINTS = {
    "connect_dwg": ["licad", "get_acad_doc", "C.doc", "C.raw_doc", "C.acad"],
    "logging": ["sys_logger", "common_logger"],
    "coordination": ["CAD_coordination", "wait_quiescent", "CADGuard"],
    "busy_handling": ["CAD_com_utils", "retry_on_busy", "SafeCOM"],
    "selection": ["CAD_selection", "select_", "ss_select", "get_rectangular_polylines"],
    "core_ops": ["CAD_core", "open_dwg", "save_", "close_"],
}


def _literal(node: ast.AST) -> Any:
    try:
        return ast.literal_eval(node)
    except Exception:
        return "<expr>"


def _get_attr_base(attr: ast.Attribute) -> str:
    if isinstance(attr.value, ast.Name):
        return attr.value.id
    if isinstance(attr.value, ast.Attribute):
        base = _get_attr_base(attr.value)
        return f"{base}.{attr.value.attr}" if base else attr.value.attr
    return ""


def _get_call_name(node: ast.Call) -> str:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        base = _get_attr_base(node.func)
        return f"{base}.{node.func.attr}" if base else node.func.attr
    return "<call>"


def _filter_call(name: str) -> bool:
    if name in IGNORE_CALLS:
        return False
    for p in IGNORE_PREFIXES:
        if name.startswith(p):
            return False
    return True


def _normalize_dep(name: str) -> tuple[str, str]:
    short = name.split(".")[-1]
    return name, short


def _extract_signature(func: ast.FunctionDef) -> dict:
    args = func.args
    defaults = [None] * (len(args.args) - len(args.defaults)) + args.defaults

    params = []
    defaults_map = {}
    for arg, default in zip(args.args, defaults):
        if arg.arg == "self":
            continue
        params.append(arg.arg)
        if default is not None:
            defaults_map[arg.arg] = _literal(default)

    vararg = args.vararg.arg if args.vararg else None
    kwarg = args.kwarg.arg if args.kwarg else None

    return {
        "params": params,
        "defaults": defaults_map,
        "vararg": vararg,
        "kwarg": kwarg,
    }


def _load_spec(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _find_func(mod: ast.Module, name: str) -> ast.FunctionDef | None:
    for node in mod.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


def check(spec_path: Path) -> tuple[bool, str]:
    spec = _load_spec(spec_path)
    src = spec.get("source", {})
    file_path = Path(src.get("file", ""))
    if not file_path.exists():
        return False, f"未找到源文件: {file_path}"

    func_name = spec.get("id", "").split(".")[-1]
    if not func_name:
        return False, "spec.id 缺失"

    source = file_path.read_text(encoding="utf-8", errors="ignore")
    mod = ast.parse(source)
    func = _find_func(mod, func_name)
    if not func:
        return False, f"未找到函数: {func_name}"

    actual_sig = _extract_signature(func)
    spec_inputs = spec.get("inputs", [])

    spec_params = []
    spec_vararg = None
    spec_kwarg = None
    spec_defaults = {}
    for item in spec_inputs:
        name = item.get("name", "")
        if name.startswith("**"):
            spec_kwarg = name[2:]
            continue
        if name.startswith("*"):
            spec_vararg = name[1:]
            continue
        spec_params.append(name)
        if "default" in item:
            spec_defaults[name] = item.get("default")

    # 参数一致性
    missing_in_spec = [p for p in actual_sig["params"] if p not in spec_params]
    extra_in_spec = [p for p in spec_params if p not in actual_sig["params"]]

    # 默认值一致性
    default_mismatch = []
    for name, val in actual_sig["defaults"].items():
        if name in spec_defaults and spec_defaults[name] != val:
            default_mismatch.append((name, spec_defaults[name], val))

    # var/kw
    var_mismatch = (spec_vararg != actual_sig["vararg"]) if (spec_vararg or actual_sig["vararg"]) else False
    kw_mismatch = (spec_kwarg != actual_sig["kwarg"]) if (spec_kwarg or actual_sig["kwarg"]) else False

    # 依赖一致性
    calls = set()
    for node in ast.walk(func):
        if isinstance(node, ast.Call):
            name = _get_call_name(node)
            if _filter_call(name):
                calls.add(name)
    calls = sorted(calls)

    spec_deps = spec.get("dependencies", {}).get("functions", [])
    spec_deps_norm = [_normalize_dep(d) for d in spec_deps]
    spec_full = {d[0] for d in spec_deps_norm}
    spec_short = {d[1] for d in spec_deps_norm}

    missing_in_code = [d for d in spec_deps if _normalize_dep(d)[1] not in calls and d not in calls]
    extra_in_code = [c for c in calls if c not in spec_full and c not in spec_short]

    # 行号一致性
    spec_lines = src.get("lines", [])
    line_mismatch = False
    if isinstance(spec_lines, list) and len(spec_lines) == 2:
        if spec_lines[0] != func.lineno or spec_lines[1] != func.end_lineno:
            line_mismatch = True

    # 返回一致性
    has_return = any(isinstance(n, ast.Return) for n in ast.walk(func))
    outputs = spec.get("outputs", [])
    return_mismatch = bool(outputs) and not has_return

    # CAD 模块引用一致性（弱校验）
    cad_usage = spec.get("cad_module_usage", {}) or {}
    cad_issues = []
    code_text = func and ast.get_source_segment(source, func) or ""
    for group, hints in CAD_MODULE_HINTS.items():
        declared = cad_usage.get(group)
        if not declared:
            continue
        has_hint = any(h in code_text for h in hints)
        if not has_hint:
            cad_issues.append(f"{group} 未在代码中发现对应调用迹象")

    ok = not (missing_in_spec or extra_in_spec or default_mismatch or var_mismatch or kw_mismatch or missing_in_code or extra_in_code or line_mismatch or return_mismatch)
    if cad_issues:
        ok = False

    # 构建报告
    report = []
    report.append(f"函数: {func_name}")
    report.append(f"源文件: {file_path}")

    if missing_in_spec:
        report.append(f"参数未写入 spec: {missing_in_spec}")
    if extra_in_spec:
        report.append(f"spec 多余参数: {extra_in_spec}")
    if default_mismatch:
        report.append(f"默认值不一致: {default_mismatch}")
    if var_mismatch:
        report.append("*args 不一致")
    if kw_mismatch:
        report.append("**kwargs 不一致")
    if missing_in_code:
        report.append(f"spec 依赖未在代码中出现: {missing_in_code}")
    if extra_in_code:
        report.append(f"代码依赖未在 spec 中声明: {extra_in_code}")
    if line_mismatch:
        report.append(f"行号不一致: spec {spec_lines} vs code [{func.lineno}, {func.end_lineno}]")
    if return_mismatch:
        report.append("spec 有输出但代码未显式 return")
    if cad_issues:
        report.append("CAD 模块引用检查: " + "; ".join(cad_issues))

    if ok:
        report.append("一致性检查通过")

    return ok, "\n".join(report)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="spec yaml 路径")
    ap.add_argument("--out", default=None, help="输出报告路径")
    args = ap.parse_args()

    ok, report = check(Path(args.spec))
    if args.out:
        Path(args.out).write_text(report + "\n", encoding="utf-8")
    print(report)
    if not ok:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
