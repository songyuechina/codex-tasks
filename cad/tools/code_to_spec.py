"""代码实体 -> 结构化 spec (YAML)

用法：
  python code_to_spec.py --file D:/codex-tasks/cad/scripts/CAD_basic.py --func select_maxrect_polylines_1
"""

import argparse
import ast
import json
from pathlib import Path
from typing import Any

import yaml


def _literal(node: ast.AST) -> Any:
    try:
        return ast.literal_eval(node)
    except Exception:
        return "<expr>"


def _get_call_name(node: ast.Call) -> str:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        base = _get_attr_base(node.func)
        return f"{base}.{node.func.attr}" if base else node.func.attr
    return "<call>"


def _get_attr_base(attr: ast.Attribute) -> str:
    if isinstance(attr.value, ast.Name):
        return attr.value.id
    if isinstance(attr.value, ast.Attribute):
        base = _get_attr_base(attr.value)
        return f"{base}.{attr.value.attr}" if base else attr.value.attr
    return ""


def _extract_steps_from_source(src: str) -> list[dict[str, str]]:
    steps = []
    for line in src.splitlines():
        line = line.strip()
        if "步骤" in line:
            steps.append({"id": f"step{len(steps)+1}", "title": line.strip('# ').strip(), "details": ""})
    return steps


def build_spec(file_path: Path, func_name: str) -> dict:
    source = file_path.read_text(encoding="utf-8", errors="ignore")
    mod = ast.parse(source)

    target = None
    for node in mod.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            target = node
            break

    if target is None:
        raise RuntimeError(f"未找到函数: {func_name}")

    # 输入参数
    args = target.args
    defaults = [None] * (len(args.args) - len(args.defaults)) + args.defaults
    inputs = []
    for arg, default in zip(args.args, defaults):
        if arg.arg == "self":
            continue
        inputs.append({
            "name": arg.arg,
            "type": "<unknown>",
            "default": _literal(default) if default is not None else None,
            "meaning": "<todo>",
        })
    if args.vararg:
        inputs.append({"name": f"*{args.vararg.arg}", "type": "<varargs>", "default": None, "meaning": "<todo>"})
    if args.kwarg:
        inputs.append({"name": f"**{args.kwarg.arg}", "type": "<kwargs>", "default": {}, "meaning": "<todo>"})

    # 输出
    returns = [n for n in ast.walk(target) if isinstance(n, ast.Return)]
    outputs = []
    if returns:
        outputs.append({"name": "<return>", "type": "<unknown>", "meaning": "<todo>"})
    else:
        outputs.append({"name": "<return>", "type": "None", "meaning": "no return"})

    # 依赖
    calls = set()
    for node in ast.walk(target):
        if isinstance(node, ast.Call):
            calls.add(_get_call_name(node))
    calls = sorted(calls)

    # 控制流
    loops = [n for n in ast.walk(target) if isinstance(n, (ast.For, ast.While))]
    branches = [n for n in ast.walk(target) if isinstance(n, ast.If)]

    src_lines = source.splitlines()
    func_src = "\n".join(src_lines[target.lineno-1: target.end_lineno])

    spec = {
        "id": f"{file_path.stem}.{func_name}",
        "version": 0.1,
        "context": {
            "system_name": "工程图纸基础服务系统",
            "module_name": "插图签编目录打印",
            "control_layer": "D:/codex-tasks/cad/analysis/flows/control_layer.yaml",
        },
        "source": {
            "file": str(file_path).replace("\\", "/"),
            "lines": [target.lineno, target.end_lineno],
        },
        "summary": "<todo>",
        "inputs": inputs,
        "outputs": outputs,
        "preconditions": ["<todo>"],
        "postconditions": ["<todo>"],
        "invariants": ["<todo>"],
        "side_effects": ["<todo>"] if calls else [],
        "dependencies": {
            "globals": [],
            "functions": calls,
        },
        "control_flow": {
            "initialization": [],
            "loop": {
                "type": "while" if any(isinstance(l, ast.While) for l in loops) else ("for" if loops else "none"),
                "max_iterations": "<todo>",
                "exit_conditions": [],
            },
            "branches": [{"condition": "<todo>", "action": "<todo>"} for _ in branches],
        },
        "steps": _extract_steps_from_source(func_src),
        "failure_modes": ["<todo>"],
        "virtual_assets": {
            "flowchart": f"D:/codex-tasks/cad/analysis/flows/{func_name}.mmd",
            "flowchart_png": f"D:/codex-tasks/cad/analysis/flows/{func_name}.png",
        },
    }
    return spec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="源文件路径")
    ap.add_argument("--func", required=True, help="函数名")
    ap.add_argument("--out", default=None, help="输出 spec 路径")
    args = ap.parse_args()

    file_path = Path(args.file)
    spec = build_spec(file_path, args.func)

    out_path = Path(args.out) if args.out else Path(f"D:/codex-tasks/cad/analysis/flows/{args.func}.spec.yaml")
    out_path.write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"已生成: {out_path}")


if __name__ == "__main__":
    main()
