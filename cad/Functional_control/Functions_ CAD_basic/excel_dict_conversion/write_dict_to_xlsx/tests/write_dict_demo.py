"""Command-line demo for write_dict_to_xlsx."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, r"D:/codex-tasks/cad/scripts")

from CAD_file_operations import cad_zt_oneb, litz
from CAD_basic import write_dict_to_xlsx, read_xlsx_to_dict


def parse_args():
    parser = argparse.ArgumentParser(description="Invoke write_dict_to_xlsx with explicit arguments.")
    parser.add_argument("template_xlsx", help="模板 Excel 文件路径")
    parser.add_argument("data_json", help="包含 project/drawings 字段的 JSON 数据文件")
    parser.add_argument("output_xlsx", help="写入结果的 Excel 文件路径")
    return parser.parse_args()


def main():
    args = parse_args()
    template_path = Path(args.template_xlsx).resolve()
    json_path = Path(args.data_json).resolve()
    output_path = Path(args.output_xlsx).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = json.loads(json_path.read_text(encoding="utf-8"))

    cad_zt_oneb()
    try:
        litz()
    except Exception:
        pass

    write_dict_to_xlsx(data, str(template_path), str(output_path))
    print(f"[OK] 已写入 {output_path}")

    result = read_xlsx_to_dict(str(output_path))
    print(f"[OK] drawings={len(result.get('drawings', []))}, 项目={result.get('project', {}).get('项目名称')}")

    cad_zt_oneb()


if __name__ == "__main__":
    main()

