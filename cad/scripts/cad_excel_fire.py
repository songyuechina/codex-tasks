"""Fire entry points for Excel dictionary conversion helpers."""
from __future__ import annotations

import json
from pathlib import Path

import CAD_basic


def read_xlsx_to_dict(xlsx_path: str):
    """Wrapper for CAD_basic.read_xlsx_to_dict."""
    return CAD_basic.read_xlsx_to_dict(xlsx_path)


def write_dict_to_xlsx(json_path: str, template_xlsx: str, output_xlsx: str):
    """Load JSON file and forward to CAD_basic.write_dict_to_xlsx."""
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    CAD_basic.write_dict_to_xlsx(data, template_xlsx, output_xlsx)
    return {
        "output": output_xlsx,
        "drawings": len(data.get("drawings", []) or []),
        "project": data.get("project", {}).get("项目名称"),
    }


if __name__ == "__main__":
    import fire

    fire.Fire()
