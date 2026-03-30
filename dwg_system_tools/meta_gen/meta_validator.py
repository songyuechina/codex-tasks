#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D:/codex-tasks/dwg_system_tools/meta_gen/meta_validator.py

用途
- 校验脚本级 meta 与函数级 meta 是否符合 META_SCHEMA.json 的基本结构
- 输出人类可读报告（stdout）与可选 JSON 报告
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Issue:
    level: str
    path: str
    message: str


def _load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _detect_meta_kind(file_path: Path, data: Dict[str, Any]) -> str:
    name = file_path.name
    if name.endswith("_functions.quote.meta.json"):
        return "functions.quote"
    if name.endswith("_functions.procedure.meta.json"):
        return "functions.procedure"
    if name.endswith("_quote.meta.json"):
        return "quote"
    if name.endswith("_procedure.meta.json"):
        return "procedure"

    if isinstance(data, dict):
        if "quote" in data and data.get("meta_scope") == "functions":
            return "functions.quote"
        if "procedure" in data and data.get("meta_scope") == "functions":
            return "functions.procedure"
        if "quote" in data:
            return "quote"
        if "procedure" in data:
            return "procedure"
    return "unknown"


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


def _min_validate_script_meta(data: Dict[str, Any], kind: str) -> List[Issue]:
    issues: List[Issue] = []

    def req(obj: Any, key: str, jpath: str):
        if not isinstance(obj, dict):
            issues.append(Issue("ERROR", jpath, f"expected object, got {type(obj).__name__}"))
            return None
        if key not in obj:
            issues.append(Issue("ERROR", f"{jpath}.{key}", "missing required field"))
            return None
        return obj[key]

    mv = req(data, "meta_version", "$")
    if mv is not None and not isinstance(mv, str):
        issues.append(Issue("ERROR", "$.meta_version", "must be string"))

    scope = req(data, "meta_scope", "$")
    if scope is not None and scope != "script":
        issues.append(Issue("ERROR", "$.meta_scope", "must be 'script' for script-level meta"))

    script = req(data, "script", "$")
    if isinstance(script, dict):
        for k in ("name", "path", "encoding", "version"):
            v = req(script, k, "$.script")
            if v is not None and not isinstance(v, str):
                issues.append(Issue("ERROR", f"$.script.{k}", "must be string"))

    if kind == "quote":
        q = req(data, "quote", "$")
        if isinstance(q, dict):
            if not isinstance(q.get("goal", ""), str):
                issues.append(Issue("ERROR", "$.quote.goal", "must be string"))
            if not isinstance(q.get("public_api", []), list):
                issues.append(Issue("ERROR", "$.quote.public_api", "must be array"))
        if "functions" in data and not isinstance(data["functions"], list):
            issues.append(Issue("ERROR", "$.functions", "must be array"))

    if kind == "procedure":
        p = req(data, "procedure", "$")
        if isinstance(p, dict):
            if "workflow" in p and not isinstance(p["workflow"], list):
                issues.append(Issue("ERROR", "$.procedure.workflow", "must be array"))
        if "functions" in data and not isinstance(data["functions"], list):
            issues.append(Issue("ERROR", "$.functions", "must be array"))

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


def _min_validate_functions_meta(data: Dict[str, Any], kind: str) -> List[Issue]:
    issues: List[Issue] = []

    def req(obj: Any, key: str, jpath: str):
        if not isinstance(obj, dict):
            issues.append(Issue("ERROR", jpath, f"expected object, got {type(obj).__name__}"))
            return None
        if key not in obj:
            issues.append(Issue("ERROR", f"{jpath}.{key}", "missing required field"))
            return None
        return obj[key]

    mv = req(data, "meta_version", "$")
    if mv is not None and not isinstance(mv, str):
        issues.append(Issue("ERROR", "$.meta_version", "must be string"))

    scope = req(data, "meta_scope", "$")
    if scope is not None and scope != "functions":
        issues.append(Issue("ERROR", "$.meta_scope", "must be 'functions' for function-level meta"))

    script = req(data, "script", "$")
    if isinstance(script, dict):
        for k in ("name", "path", "encoding", "version"):
            v = req(script, k, "$.script")
            if v is not None and not isinstance(v, str):
                issues.append(Issue("ERROR", f"$.script.{k}", "must be string"))

    fx = req(data, "functions", "$")
    if fx is not None and not isinstance(fx, list):
        issues.append(Issue("ERROR", "$.functions", "must be array"))
        fx = []

    if kind == "functions.quote" and "functions_quote" not in data:
        issues.append(Issue("ERROR", "$.functions_quote", "missing required field"))
    if kind == "functions.procedure" and "functions_procedure" not in data:
        issues.append(Issue("ERROR", "$.functions_procedure", "missing required field"))

    if isinstance(fx, list):
        for i, f in enumerate(fx):
            if not isinstance(f, dict):
                issues.append(Issue("ERROR", f"$.functions[{i}]", "must be object"))
                continue
            if not isinstance(f.get("name"), str):
                issues.append(Issue("ERROR", f"$.functions[{i}].name", "must be string"))
            if not isinstance(f.get("signature", ""), str):
                issues.append(Issue("ERROR", f"$.functions[{i}].signature", "must be string"))

            if kind == "functions.quote":
                for k in ("purpose", "inputs", "outputs"):
                    if k not in f:
                        issues.append(Issue("ERROR", f"$.functions[{i}].{k}", "missing required field"))
                if "inputs" in f and not isinstance(f["inputs"], list):
                    issues.append(Issue("ERROR", f"$.functions[{i}].inputs", "must be array"))
                if "outputs" in f and not isinstance(f["outputs"], list):
                    issues.append(Issue("ERROR", f"$.functions[{i}].outputs", "must be array"))
                if "returns" in f and not isinstance(f["returns"], list):
                    issues.append(Issue("ERROR", f"$.functions[{i}].returns", "must be array"))

            if kind == "functions.procedure":
                if "level" not in f:
                    issues.append(Issue("ERROR", f"$.functions[{i}].level", "missing required field"))
                if "steps" in f and not isinstance(f["steps"], list):
                    issues.append(Issue("ERROR", f"$.functions[{i}].steps", "must be array"))
                if "brief_flow" in f and not isinstance(f["brief_flow"], list):
                    issues.append(Issue("ERROR", f"$.functions[{i}].brief_flow", "must be array"))

    return issues


def validate_file(schema: Dict[str, Any], file_path: Path) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "file": str(file_path),
        "ok": True,
        "used": "min",
        "meta_kind": "unknown",
        "errors": [],
        "warnings": [],
    }

    try:
        data = _load_json(file_path)
    except Exception as e:
        result["ok"] = False
        result["errors"].append({"path": "$", "message": f"failed to parse json: {e}"})
        return result

    kind = _detect_meta_kind(file_path, data if isinstance(data, dict) else {})
    result["meta_kind"] = kind

    used_jsonschema, js_issues = _try_jsonschema_validate(schema, data)
    if used_jsonschema:
        result["used"] = "jsonschema"
        issues = js_issues
    else:
        if not isinstance(data, dict):
            issues = [Issue("ERROR", "$", f"root must be object, got {type(data).__name__}")]
        elif kind in ("quote", "procedure"):
            issues = _min_validate_script_meta(data, kind)
        elif kind in ("functions.quote", "functions.procedure"):
            issues = _min_validate_functions_meta(data, kind)
        else:
            issues = [Issue("ERROR", "$", "cannot detect meta kind from filename/content")]

    def warn(path: str, msg: str):
        result["warnings"].append({"path": path, "message": msg})

    if isinstance(data, dict):
        if kind == "quote":
            public_api = ((data.get("quote") or {}).get("public_api") or [])
            functions = data.get("functions") or []
            if isinstance(public_api, list) and isinstance(functions, list):
                fn_names = {f.get("name") for f in functions if isinstance(f, dict)}
                for api in public_api:
                    if api not in fn_names:
                        warn("$.functions", f"public_api '{api}' missing in script-level functions[]")
        if kind == "functions.quote":
            fq = data.get("functions_quote") or {}
            if isinstance(fq, dict) and fq.get("coverage") not in ("all", "graded-all"):
                warn("$.functions_quote.coverage", "recommended value is 'all' or 'graded-all'")
        if kind == "functions.procedure":
            fp = data.get("functions_procedure") or {}
            if isinstance(fp, dict) and "step_style" not in fp:
                warn("$.functions_procedure.step_style", "missing step_style")
        if "quality" in data:
            q = data.get("quality") or {}
            if isinstance(q, dict) and "function_count" in q and isinstance(data.get("functions"), list):
                if q["function_count"] != len(data["functions"]):
                    warn("$.quality.function_count", "function_count does not match len(functions)")

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
    ap.add_argument("--schema", required=True, help="Path to META_SCHEMA.json")
    ap.add_argument("--files", nargs="*", default=[], help="One or more meta json files to validate")
    ap.add_argument("--dir", default="", help="Directory to scan for meta json files")
    ap.add_argument("--glob", default="*.meta.json", help="Glob pattern when using --dir")
    ap.add_argument("--report", default="", help="Optional output report json path")
    args = ap.parse_args(argv)

    schema_path = Path(args.schema).resolve()
    schema = _load_json(schema_path)

    targets: List[Path] = [Path(p).resolve() for p in args.files]
    if args.dir:
        d = Path(args.dir).resolve()
        targets.extend(sorted(d.glob(args.glob)))

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
            print(f"[OK]   {fp}  (used={res['used']}, kind={res['meta_kind']})")
        else:
            print(f"[FAIL] {fp}  (used={res['used']}, kind={res['meta_kind']})")
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
