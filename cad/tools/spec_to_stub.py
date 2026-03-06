"""结构化 spec (YAML) -> 代码骨架

用法：
  python spec_to_stub.py --spec D:/codex-tasks/cad/analysis/flows/select_maxrect_polylines_1.spec.yaml --out D:/codex-tasks/cad/analysis/flows/select_maxrect_polylines_1.stub.py
"""

import argparse
from pathlib import Path
from typing import Any

import yaml


def _fmt_default(val: Any) -> str:
    if isinstance(val, str):
        return f"\"{val}\""
    if val is None:
        return "None"
    return str(val)


def build_stub(spec: dict) -> str:
    func_id = spec.get("id", "function")
    func_name = func_id.split(".")[-1]
    inputs = spec.get("inputs", [])

    params = []
    for item in inputs:
        name = item.get("name")
        if not name:
            continue
        if name.startswith("*") or name.startswith("**"):
            params.append(name)
            continue
        default = item.get("default", None)
        params.append(f"{name}={_fmt_default(default)}")

    params_str = ", ".join(params) if params else ""

    summary = (spec.get("summary") or "").strip()
    outputs = spec.get("outputs", [])
    side_effects = spec.get("side_effects", [])
    preconditions = spec.get("preconditions", [])
    postconditions = spec.get("postconditions", [])
    invariants = spec.get("invariants", [])
    steps = spec.get("steps", [])

    doc = []
    if summary:
        doc.append(summary)
    if inputs:
        doc.append("\n参数:")
        for item in inputs:
            doc.append(f"- {item.get('name')}: {item.get('meaning','')}")
    if outputs:
        doc.append("\n输出:")
        for item in outputs:
            doc.append(f"- {item.get('name')}: {item.get('meaning','')}")
    if preconditions:
        doc.append("\n前置条件:")
        for item in preconditions:
            doc.append(f"- {item}")
    if postconditions:
        doc.append("\n后置条件:")
        for item in postconditions:
            doc.append(f"- {item}")
    if invariants:
        doc.append("\n不变量:")
        for item in invariants:
            doc.append(f"- {item}")
    if side_effects:
        doc.append("\n副作用:")
        for item in side_effects:
            doc.append(f"- {item}")

    docstring = "\n".join(doc) if doc else "TODO"

    body_lines = ["    # TODO: 根据 spec 实现功能\n"]
    for step in steps:
        title = step.get("title") or step.get("id")
        if title:
            body_lines.append(f"    # {title}\n")
    body_lines.append("    pass\n")

    stub = f"""def {func_name}({params_str}):\n    \"\"\"{docstring}\n    \"\"\"\n""" + "".join(body_lines)
    return stub


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="spec yaml 路径")
    ap.add_argument("--out", default=None, help="输出 py 路径（可选）")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    stub = build_stub(spec)

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(stub, encoding="utf-8")
        print(f"已生成: {out_path}")
    else:
        print(stub)


if __name__ == "__main__":
    main()
