"""结构化 spec (YAML) -> 文本描述 (Markdown)

用法：
  python spec_to_text.py --spec D:/codex-tasks/cad/analysis/flows/select_maxrect_polylines_1.spec.yaml --out D:/codex-tasks/cad/analysis/flows/select_maxrect_polylines_1.spec.md
"""

import argparse
from pathlib import Path

import yaml


def build_text(spec: dict) -> str:
    lines = []
    lines.append(f"# {spec.get('id', 'function')}")

    summary = (spec.get("summary") or "").strip()
    if summary:
        lines.append("\n## 实现目标\n" + summary)

    ctx = spec.get("context", {})
    if ctx:
        lines.append("\n## 上下文")
        for k in ("system_name", "module_name", "control_layer"):
            if k in ctx:
                lines.append(f"- {k}: {ctx[k]}")

    inputs = spec.get("inputs", [])
    if inputs:
        lines.append("\n## 输入参数")
        for item in inputs:
            name = item.get("name")
            typ = item.get("type", "")
            default = item.get("default", "")
            meaning = item.get("meaning", "")
            lines.append(f"- {name} ({typ}), default={default}: {meaning}")

    outputs = spec.get("outputs", [])
    if outputs:
        lines.append("\n## 输出")
        for item in outputs:
            lines.append(f"- {item.get('name')}: {item.get('meaning','')}")

    preconditions = spec.get("preconditions", [])
    if preconditions:
        lines.append("\n## 前置条件")
        for item in preconditions:
            lines.append(f"- {item}")

    postconditions = spec.get("postconditions", [])
    if postconditions:
        lines.append("\n## 后置条件")
        for item in postconditions:
            lines.append(f"- {item}")

    invariants = spec.get("invariants", [])
    if invariants:
        lines.append("\n## 不变量")
        for item in invariants:
            lines.append(f"- {item}")

    branches = spec.get("control_flow", {}).get("branches", [])
    if branches:
        lines.append("\n## 分支")
        for b in branches:
            lines.append(f"- 条件: {b.get('condition','')} -> 动作: {b.get('action','')}")

    steps = spec.get("steps", [])
    if steps:
        lines.append("\n## 功能流程")
        for i, s in enumerate(steps, 1):
            title = s.get("title") or s.get("id")
            details = s.get("details", "")
            lines.append(f"{i}. {title}\n   {details}")

    side_effects = spec.get("side_effects", [])
    if side_effects:
        lines.append("\n## 副作用")
        for item in side_effects:
            lines.append(f"- {item}")

    cad_usage = spec.get("cad_module_usage", {})
    if cad_usage:
        lines.append("\n## CAD 模块引用")
        for k, v in cad_usage.items():
            if not v:
                continue
            lines.append(f"- {k}: " + ", ".join(v))

    deps = spec.get("dependencies", {})
    funcs = deps.get("functions", []) if isinstance(deps, dict) else []
    if funcs:
        lines.append("\n## 依赖函数")
        for f in funcs:
            lines.append(f"- {f}")

    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="spec yaml 路径")
    ap.add_argument("--out", required=True, help="输出 md 路径")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    text = build_text(spec)

    out_path = Path(args.out)
    out_path.write_text(text, encoding="utf-8")
    print(f"已生成: {out_path}")


if __name__ == "__main__":
    main()
