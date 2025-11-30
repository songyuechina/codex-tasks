"""Command-line demo for read_xlsx_to_dict."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, r"D:/codex-tasks/cad/scripts")

from CAD_file_operations import cad_zt_oneb, litz
from CAD_basic import read_xlsx_to_dict


def parse_args():
    parser = argparse.ArgumentParser(description="Invoke read_xlsx_to_dict with explicit arguments.")
    parser.add_argument("xlsx_path", help="待读取的 Excel 文件路径")
    parser.add_argument("output_json", help="保存结果字典的 JSON 文件路径")
    return parser.parse_args()


def main():
    args = parse_args()
    xlsx_path = Path(args.xlsx_path).resolve()
    output_path = Path(args.output_json).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cad_zt_oneb()
    try:
        litz()
    except Exception:
        pass

    data = read_xlsx_to_dict(str(xlsx_path))
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] 已读取 {xlsx_path}")
    print(f"[OK] JSON 写入 {output_path}")

    cad_zt_oneb()


if __name__ == "__main__":
    main()

