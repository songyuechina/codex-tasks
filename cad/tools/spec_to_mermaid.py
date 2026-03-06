"""结构化 spec (YAML) -> Mermaid 流程图 (mmd)

用法：
  python spec_to_mermaid.py --spec D:/codex-tasks/cad/analysis/flows/select_maxrect_polylines_1.spec.yaml --out D:/codex-tasks/cad/analysis/flows/select_maxrect_polylines_1.mmd
"""

import argparse
from pathlib import Path

import yaml


def _q(text: str) -> str:
    text = text.replace("\"", "'").strip()
    return f"\"{text}\""


def build_mermaid(spec: dict) -> str:
    func_id = spec.get("id", "function")
    summary = (spec.get("summary") or "").strip()
    inputs = spec.get("inputs", [])
    steps = spec.get("steps", [])
    branches = spec.get("control_flow", {}).get("branches", [])

    lines = ["flowchart TD"]

    title = summary if summary else func_id
    lines.append(f"    A[{_q('实现目标: ' + title)}]")

    if inputs:
        inp = "输入参数: " + ", ".join([i.get("name", "") for i in inputs])
        lines.append(f"    B[{_q(inp)}]")
        lines.append("    A --> B")
        prev = "B"
    else:
        prev = "A"

    # 主流程
    for idx, step in enumerate(steps, 1):
        title = step.get("title") or step.get("id") or f"step{idx}"
        details = step.get("details", "")
        label = f"{idx}. {title}" + (" | " + details if details else "")
        node = f"S{idx}"
        lines.append(f"    {node}[{_q(label)}]")
        lines.append(f"    {prev} --> {node}")
        prev = node

    # 分支（以虚线提示）
    for i, br in enumerate(branches, 1):
        cond = br.get("condition", "<condition>")
        action = br.get("action", "<action>")
        lines.append(f"    BR{i}{{{_q('分支: ' + cond)}}}")
        lines.append(f"    BR{i} --> ACT{i}[{_q('动作: ' + action)}]")
        lines.append(f"    {prev} -.-> BR{i}")

    lines.append(f"    {prev} --> Z[{_q('输出')}]")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="spec yaml 路径")
    ap.add_argument("--out", required=True, help="输出 mmd 路径")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    mmd = build_mermaid(spec)

    out_path = Path(args.out)
    out_path.write_text(mmd, encoding="utf-8")
    print(f"已生成: {out_path}")


if __name__ == "__main__":
    main()
