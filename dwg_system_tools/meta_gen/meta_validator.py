#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
meta_validator.py

用途（DWG System Tools / meta_gen）
- 校验 *_quote.meta.json / *_procedure.meta.json 是否符合 META_SCHEMA_V1.json 的基本结构
- 输出人类可读的校验报告（stdout）与可选的 JSON 报告文件

说明
- 优先使用 jsonschema 库（若已安装）进行严格校验
- 若 jsonschema 不可用，则使用内置的“最小校验器”进行关键字段校验（保证不阻塞）
- 语义正确性（例如 branch_logic 是否合理）不在 schema 里强校验，仍依赖 META_RULES_V1 的 evidence/todo 规则

CLI 示例：
  python meta_validator.py --schema D:/codex-tasks/dwg_system_tools/meta_gen/META_SCHEMA_V1.json ^
    --files D:/codex-tasks/dwg_system_tools/_generated_meta/common_logger_quote.meta.json

  python meta_validator.py --schema ... --dir D:/codex-tasks/dwg_system_tools/_generated_meta --glob "*_quote.meta.json"
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Issue:
    level: str  # "ERROR" | "WARN"
    path: str   # json pointer-ish path
    message: str


def _load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _try_jsonschema_validate(schema: Dict[str, Any], data: Any) -> Tuple[bool, List[Issue]]:
    try:
        import jsonschema  # type: ignore
        from jsonschema import Draft7Validator  # type: ignore
    except Exception:
        return False, []

    v = Draft7Validator(schema)
    issues: List[Issue] = []
    for e in sorted(v.iter_errors(data), key=lambda x: str(x.path)):
        jpath = "$"
        for part in list(e.path):
            if isinstance(part, int):
                jpath += f"[{part}]"
            else:
                jpath += f".{part}"
        issues.append(Issue(level="ERROR", path=jpath, message=e.message))
    return True, issues


def _min_validate(schema: Dict[str, Any], data: Any) -> List[Issue]:
    """
    兜底最小校验：只检查 META_SCHEMA_V1.json 中的关键 required 字段与基础类型。
    """
    issues: List[Issue] = []

    def req(obj: Any, key: str, jpath: str):
        if not isinstance(obj, dict):
            issues.append(Issue("ERROR", jpath, f"expected object, got {type(obj).__name__}"))
            return None
        if key not in obj:
            issues.append(Issue("ERROR", f"{jpath}.{key}", "missing required field"))
            return None
        return obj[key]

    if not isinstance(data, dict):
        return [Issue("ERROR", "$", f"root must be object, got {type(data).__name__}")]

    mv = req(data, "meta_version", "$")
    if mv is not None and not isinstance(mv, str):
        issues.append(Issue("ERROR", "$.meta_version", "must be string"))

    script = req(data, "script", "$")
    if isinstance(script, dict):
        for k in ("name", "path", "encoding", "version"):
            v = req(script, k, "$.script")
            if v is not None and not isinstance(v, str):
                issues.append(Issue("ERROR", f"$.script.{k}", "must be string"))

    # functions 若存在必须为 array
    if "functions" in data and not isinstance(data["functions"], list):
        issues.append(Issue("ERROR", "$.functions", "must be array"))

    # quality.todo 若存在必须为 array
    if "quality" in data:
        q = data["quality"]
        if not isinstance(q, dict):
            issues.append(Issue("ERROR", "$.quality", "must be object"))
        else:
            if "todo" in q and not isinstance(q["todo"], list):
                issues.append(Issue("ERROR", "$.quality.todo", "must be array"))
            if "function_count" in q and not isinstance(q["function_count"], int):
                issues.append(Issue("ERROR", "$.quality.function_count", "must be integer"))

    return issues


def validate_file(schema: Dict[str, Any], file_path: Path) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "file": str(file_path),
        "ok": True,
        "used": "min",
        "errors": [],
        "warnings": [],
    }

    try:
        data = _load_json(file_path)
    except Exception as e:
        result["ok"] = False
        result["errors"].append({"path": "$", "message": f"failed to parse json: {e}"})
        return result

    used_jsonschema, js_issues = _try_jsonschema_validate(schema, data)
    if used_jsonschema:
        result["used"] = "jsonschema"
        issues = js_issues
    else:
        issues = _min_validate(schema, data)

    # extra pragmatic warnings (not schema-enforced)
    def warn(path: str, msg: str):
        result["warnings"].append({"path": path, "message": msg})

    # If quote/procedure exists, suggest todo presence when confidence low-ish (can't enforce)
    if isinstance(data, dict):
        if "quote" in data and isinstance(data["quote"], dict):
            conf = data["quote"].get("confidence", {})
            if isinstance(conf, dict) and conf.get("goal") in ("low", "medium"):
                warn("$.quote.confidence.goal", "goal confidence is not high; ensure evidence/todo are present per META_RULES_V1")
        if "functions" in data and isinstance(data["functions"], list):
            # check returns evidence presence lightly
            for i, f in enumerate(data["functions"]):
                if not isinstance(f, dict):
                    continue
                if "returns" in f and isinstance(f["returns"], list):
                    for j, r in enumerate(f["returns"]):
                        if isinstance(r, dict):
                            if "evidence" not in r:
                                warn(f"$.functions[{i}].returns[{j}].evidence", "missing evidence; META_RULES_V1 requires evidence for each return branch")

    for iss in issues:
        if iss.level == "ERROR":
            result["errors"].append({"path": iss.path, "message": iss.message})
        else:
            result["warnings"].append({"path": iss.path, "message": iss.message})

    if result["errors"]:
        result["ok"] = False
    return result


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True, help="Path to META_SCHEMA_V1.json")
    ap.add_argument("--files", nargs="*", default=[], help="One or more meta json files to validate")
    ap.add_argument("--dir", default="", help="Directory to scan for meta json files")
    ap.add_argument("--glob", default="*.meta.json", help="Glob pattern when using --dir (default: *.meta.json)")
    ap.add_argument("--report", default="", help="Optional output report json path")
    args = ap.parse_args(argv)

    schema_path = Path(args.schema).resolve()
    schema = _load_json(schema_path)

    targets: List[Path] = [Path(p).resolve() for p in args.files]
    if args.dir:
        d = Path(args.dir).resolve()
        targets.extend(sorted(d.glob(args.glob)))

    # unique
    seen = set()
    uniq: List[Path] = []
    for p in targets:
        if str(p) not in seen:
            seen.add(str(p))
            uniq.append(p)
    targets = uniq

    if not targets:
        print("[ERROR] No target files. Use --files ... or --dir ...")
        return 2

    results = []
    ok_count = 0
    for fp in targets:
        res = validate_file(schema, fp)
        results.append(res)
        if res["ok"]:
            ok_count += 1
            print(f"[OK]   {fp}  (used={res['used']})")
        else:
            print(f"[FAIL] {fp}  (used={res['used']})")
            for e in res["errors"]:
                print(f"       - ERROR {e['path']}: {e['message']}")
        for w in res["warnings"]:
            print(f"       - WARN  {w['path']}: {w['message']}")

    summary = {
        "schema": str(schema_path),
        "validated": len(results),
        "ok": ok_count,
        "fail": len(results) - ok_count,
        "results": results,
    }

    if args.report:
        outp = Path(args.report).resolve()
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[REPORT] {outp}")

    return 0 if ok_count == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
