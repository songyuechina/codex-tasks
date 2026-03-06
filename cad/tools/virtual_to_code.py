"""虚 -> 实 一键生成（代码骨架）

用法：
  python virtual_to_code.py --spec D:/codex-tasks/cad/analysis/flows/select_maxrect_polylines_1.spec.yaml --out D:/codex-tasks/cad/analysis/flows/select_maxrect_polylines_1.stub.py
"""

import argparse
import subprocess


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="spec yaml 路径")
    ap.add_argument("--out", required=True, help="输出 py 路径")
    args = ap.parse_args()

    subprocess.run([
        "python",
        "D:/codex-tasks/cad/tools/spec_to_stub.py",
        "--spec",
        args.spec,
        "--out",
        args.out,
    ], check=True)


if __name__ == "__main__":
    main()
