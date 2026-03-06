"""实 -> 虚 一键生成（spec + mmd + md + png 可选）

用法：
  python code_to_virtual.py --file D:/codex-tasks/cad/scripts/CAD_basic.py --func select_maxrect_polylines_1 --outdir D:/codex-tasks/cad/analysis/flows --png
"""

import argparse
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="源文件路径")
    ap.add_argument("--func", required=True, help="函数名")
    ap.add_argument("--outdir", required=True, help="输出目录")
    ap.add_argument("--png", action="store_true", help="尝试生成 PNG")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    spec_path = outdir / f"{args.func}.spec.yaml"
    mmd_path = outdir / f"{args.func}.mmd"
    md_path = outdir / f"{args.func}.spec.md"
    png_path = outdir / f"{args.func}.png"

    run(["python", "D:/codex-tasks/cad/tools/code_to_spec.py", "--file", args.file, "--func", args.func, "--out", str(spec_path)])
    run(["python", "D:/codex-tasks/cad/tools/spec_to_mermaid.py", "--spec", str(spec_path), "--out", str(mmd_path)])
    run(["python", "D:/codex-tasks/cad/tools/spec_to_text.py", "--spec", str(spec_path), "--out", str(md_path)])

    if args.png:
        # 需要本机已可用 mermaid-cli + Edge
        puppeteer_cfg = outdir / "puppeteer.json"
        if puppeteer_cfg.exists():
            cmd = ["npx", "-y", "@mermaid-js/mermaid-cli", "-p", str(puppeteer_cfg), "-i", str(mmd_path), "-o", str(png_path)]
        else:
            cmd = ["npx", "-y", "@mermaid-js/mermaid-cli", "-i", str(mmd_path), "-o", str(png_path)]
        env = dict(**os.environ)
        env.setdefault("PUPPETEER_SKIP_DOWNLOAD", "1")
        subprocess.run(cmd, check=True, env=env)


if __name__ == "__main__":
    import os
    main()
