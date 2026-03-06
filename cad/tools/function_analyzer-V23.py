#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# D:/codex-tasks/cad/tools/function_analyzer.py
# 版本 V2.3 (SCHEMA COMPAT FIX)

"""
D:/codex-tasks/cad/tools/function_analyzer.py

核心能力（可 import 调用）：
- 扫描单个 .py 文件的顶层函数 def/async def
- 提取函数源码（def 到结束）
- AST 提取 calls
- 调用 fox responses API 做函数流程语义分析（最多重试 5 次）
- 构建函数调用合同（inputs/outputs/side_effects/safe_usage_notes）
- MySQL 落库（CAD_FUNCINFO.function_analysis）并默认优先复用数据库结果（qualified_name + source_hash）

V2.3 修复（你当前遇到的致命问题）：
- DB 表中存在 NOT NULL 字段 qualified_hash（无默认值）时，写库自动补齐
- ensure_function_db_and_table 创建新表时也包含 qualified_hash（新环境不会踩坑）
- 写库失败不假成功：db_save_failed => ok=False
- 写库失败自动落地本地 JSONL：cad/tools/_dump/function_analysis_db_failed.jsonl
- ENGINEERED BATCH 下传 session/timeout/max_stream_seconds，减少连接开销、更稳定
"""

from __future__ import annotations

import os
import re
import ast
import json
import time
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional
import sys

# -------------------------
# 一 找到 cad 根目录并加入 sys.path（保持你的项目风格）
# -------------------------
_current = Path(__file__).resolve()
while _current.name != "cad":
    if _current.parent == _current:
        raise RuntimeError("找不到 cad 根目录")
    _current = _current.parent
CAD_ROOT = _current
if str(CAD_ROOT) not in sys.path:
    sys.path.insert(0, str(CAD_ROOT))

CODEX_API_KEY = os.environ.get("CODEX_API_KEY")

from library import Databaseoperation as dbop

# =============================================================================
# 二  DB 常量
# =============================================================================
FUNC_DB_NAME = "CAD_FUNCINFO"
FUNC_TABLE_NAME = "function_analysis"

def _sha256_text(s: str) -> str:
    return hashlib.sha256((s or "").encode("utf-8", errors="ignore")).hexdigest()

def _qualified_hash(qualified_name: str) -> str:
    return _sha256_text(qualified_name)

# =============================================================================
# 三 DB Runtime (工程化版：一次 init + 连接复用 + 静默)
# =============================================================================
_DB_READY = False
_DB_READY_ERR: str | None = None
_DB_CONN = None  # dbop 连接复用（同进程内）
_DB_LAST_PING_TS = 0.0

# schema cache
_DB_HAS_QUALIFIED_HASH: bool | None = None

def _db_get_conn(database: str):
    """
    复用 dbop 连接；自动 keepalive。
    """
    global _DB_CONN, _DB_LAST_PING_TS
    if _DB_CONN is None:
        _DB_CONN = dbop.connect_to_db(database)

    # 10秒 ping 一次，避免长任务中断
    now = time.time()
    if now - _DB_LAST_PING_TS > 10:
        _DB_CONN = dbop.ensure_connection_alive(_DB_CONN, database=database)
        _DB_LAST_PING_TS = now
    return _DB_CONN

def _db_close_conn():
    global _DB_CONN
    try:
        if _DB_CONN is not None:
            _DB_CONN.close()
    except Exception:
        pass
    _DB_CONN = None

def _db_has_column(database: str, table: str, column: str) -> bool:
    """
    检测表字段是否存在（带缓存）。
    """
    global _DB_HAS_QUALIFIED_HASH
    if column == "qualified_hash" and _DB_HAS_QUALIFIED_HASH is not None:
        return _DB_HAS_QUALIFIED_HASH

    conn = _db_get_conn(database)
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s
            """,
            (database, table, column),
        )
        n = cur.fetchone()[0]
        ok = bool(n and int(n) > 0)
        if column == "qualified_hash":
            _DB_HAS_QUALIFIED_HASH = ok
        return ok
    finally:
        try:
            cur.close()
        except Exception:
            pass

def ensure_function_db_and_table(*, database: str = FUNC_DB_NAME, table: str = FUNC_TABLE_NAME) -> dict:
    """
    确保函数信息数据库 + 表存在（工程化版）：
    - 进程内只初始化一次
    - 复用连接
    - 避免重复输出 / 重复建库建表

    V2.3：创建新表时增加 qualified_hash（兼容旧表：旧表可能已有该字段，也可能没有）
    """
    global _DB_READY, _DB_READY_ERR, _DB_HAS_QUALIFIED_HASH
    if _DB_READY:
        return {"ok": True, "database": database, "table": table, "error": None}
    if _DB_READY_ERR:
        return {"ok": False, "database": database, "table": table, "error": _DB_READY_ERR}

    try:
        dbop.create_database_if_not_exists(database)

        conn = _db_get_conn(database)
        cur = conn.cursor()

        # 新建表：直接包含 qualified_hash（不影响已存在表）
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS `{table}` (
            `id` BIGINT AUTO_INCREMENT PRIMARY KEY,

            `qualified_name` VARCHAR(512) NOT NULL COMMENT '模块限定名: module:func',
            `qualified_hash` CHAR(64) NOT NULL COMMENT 'sha256(qualified_name) 用于兼容旧schema',

            `func_name` VARCHAR(255) NOT NULL COMMENT '函数名(冗余字段便于检索)',
            `file_path` TEXT NOT NULL COMMENT '函数所在文件完整路径',
            `start_line` INT DEFAULT NULL COMMENT '起始行(1-based)',
            `end_line` INT DEFAULT NULL COMMENT '结束行(1-based)',
            `source_hash` CHAR(64) NOT NULL COMMENT '源码sha256',
            `analysis_json` LONGTEXT NOT NULL COMMENT '分析结果JSON(文本)',
            `contract_json` LONGTEXT DEFAULT NULL COMMENT '合同JSON(可选)',
            `model` VARCHAR(255) DEFAULT NULL COMMENT '使用的模型',
            `base_url` TEXT DEFAULT NULL COMMENT '使用的API base_url',
            `ok` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '分析是否成功',
            `error_text` TEXT DEFAULT NULL COMMENT '失败原因',
            `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',

            UNIQUE KEY `uq_qname_hash` (`qualified_name`(191), `source_hash`),
            KEY `idx_qhash` (`qualified_hash`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        conn.commit()
        try:
            cur.close()
        except Exception:
            pass

        # 运行时检测真实表 schema（关键）
        _DB_HAS_QUALIFIED_HASH = _db_has_column(database, table, "qualified_hash")

        _DB_READY = True
        return {"ok": True, "database": database, "table": table, "error": None, "has_qualified_hash": _DB_HAS_QUALIFIED_HASH}
    except Exception as e:
        _DB_READY_ERR = str(e)
        return {"ok": False, "database": database, "table": table, "error": _DB_READY_ERR}


# =============================================================================
# 四 DB 读写
# =============================================================================
def load_function_analysis_from_db(
    *,
    qualified_name: str,
    func_source: str | None = None,
    database: str = FUNC_DB_NAME,
    table: str = FUNC_TABLE_NAME,
) -> dict:
    try:
        ready = ensure_function_db_and_table(database=database, table=table)
        if not ready.get("ok"):
            return {"ok": False, "hit": False, "record": None, "error": ready.get("error")}

        source_hash = _sha256_text(func_source) if func_source is not None else None

        conn = _db_get_conn(database)
        cur = conn.cursor(dictionary=True)

        if source_hash:
            cur.execute(
                f"""SELECT * FROM `{table}`
                    WHERE qualified_name=%s AND source_hash=%s
                    ORDER BY updated_at DESC LIMIT 1""",
                (qualified_name, source_hash),
            )
        else:
            cur.execute(
                f"""SELECT * FROM `{table}`
                    WHERE qualified_name=%s
                    ORDER BY updated_at DESC LIMIT 1""",
                (qualified_name,),
            )

        row = cur.fetchone()
        cur.close()

        if not row:
            return {"ok": True, "hit": False, "record": None, "error": None}

        try:
            row["analysis"] = json.loads(row.get("analysis_json") or "{}")
        except Exception:
            row["analysis"] = None

        try:
            cj = row.get("contract_json")
            row["contract"] = json.loads(cj) if cj else None
        except Exception:
            row["contract"] = None

        return {"ok": True, "hit": True, "record": row, "error": None}
    except Exception as e:
        return {"ok": False, "hit": False, "record": None, "error": str(e)}

def save_function_analysis_to_db(
    *,
    qualified_name: str,
    func_name: str,
    file_path: str,
    start_line: int | None,
    end_line: int | None,
    func_source: str,
    analysis: dict,
    contract: dict | None = None,
    ok: bool = True,
    error_text: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
    database: str = FUNC_DB_NAME,
    table: str = FUNC_TABLE_NAME,
) -> dict:
    """
    V2.3：如果表里有 qualified_hash，则 INSERT/UPDATE 自动写入
    """
    try:
        ready = ensure_function_db_and_table(database=database, table=table)
        if not ready.get("ok"):
            return {"ok": False, "error": ready.get("error")}

        has_qh = _db_has_column(database, table, "qualified_hash")

        source_hash = _sha256_text(func_source)
        analysis_json = json.dumps(analysis or {}, ensure_ascii=False)
        contract_json = json.dumps(contract or {}, ensure_ascii=False) if contract is not None else None

        qh = _qualified_hash(qualified_name)

        conn = _db_get_conn(database)
        cur = conn.cursor()

        if has_qh:
            cur.execute(
                f"""
                INSERT INTO `{table}`
                    (qualified_name, qualified_hash, func_name, file_path, start_line, end_line, source_hash,
                     analysis_json, contract_json, model, base_url, ok, error_text, updated_at)
                VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
                ON DUPLICATE KEY UPDATE
                    qualified_hash=VALUES(qualified_hash),
                    func_name=VALUES(func_name),
                    file_path=VALUES(file_path),
                    start_line=VALUES(start_line),
                    end_line=VALUES(end_line),
                    analysis_json=VALUES(analysis_json),
                    contract_json=VALUES(contract_json),
                    model=VALUES(model),
                    base_url=VALUES(base_url),
                    ok=VALUES(ok),
                    error_text=VALUES(error_text),
                    updated_at=NOW()
                """,
                (
                    qualified_name, qh, func_name, file_path, start_line, end_line, source_hash,
                    analysis_json, contract_json, model, base_url,
                    1 if ok else 0, error_text
                ),
            )
        else:
            cur.execute(
                f"""
                INSERT INTO `{table}`
                    (qualified_name, func_name, file_path, start_line, end_line, source_hash,
                     analysis_json, contract_json, model, base_url, ok, error_text, updated_at)
                VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
                ON DUPLICATE KEY UPDATE
                    func_name=VALUES(func_name),
                    file_path=VALUES(file_path),
                    start_line=VALUES(start_line),
                    end_line=VALUES(end_line),
                    analysis_json=VALUES(analysis_json),
                    contract_json=VALUES(contract_json),
                    model=VALUES(model),
                    base_url=VALUES(base_url),
                    ok=VALUES(ok),
                    error_text=VALUES(error_text),
                    updated_at=NOW()
                """,
                (
                    qualified_name, func_name, file_path, start_line, end_line, source_hash,
                    analysis_json, contract_json, model, base_url,
                    1 if ok else 0, error_text
                ),
            )

        conn.commit()
        cur.close()
        return {"ok": True, "error": None, "has_qualified_hash": has_qh}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# =============================================================================
# 五  基础工具
# =============================================================================
def _now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def _safe_read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def _norm_path(p: str | Path) -> str:
    return str(Path(p).resolve())

def _rel_to_cad_root(p: str | Path) -> str:
    try:
        return str(Path(p).resolve().relative_to(CAD_ROOT))
    except Exception:
        return str(Path(p).resolve())

def _module_qual_from_file(p: str | Path) -> str:
    rel = _rel_to_cad_root(p).replace("\\", "/")
    if rel.lower().endswith(".py"):
        rel = rel[:-3]
    rel = rel.replace("/", ".")
    if rel.startswith("cad."):
        rel = rel[4:]
    return rel

def build_qualified_name(file: str | Path, func_name: str) -> str:
    return f"{_module_qual_from_file(file)}:{func_name}"

def _append_jsonl(path: str | Path, obj: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


#获取失败函数的本地信息

def load_local_failed_function_records(
    *,
    dump_dir: str | Path | None = None,
    include_api_failed: bool = True,
    include_db_failed: bool = True,
    latest_only: bool = True,
) -> list[dict]:
    """
    读取本地 dump 的失败记录，按列表返回。

    来源文件（你的 V2.2 已在写）：
    - tools/_dump/function_analysis_api_failed.jsonl
    - tools/_dump/function_analysis_db_failed.jsonl

    返回字段尽量统一：
    {
      "ts": "...",
      "qualified_name": "...",
      "func_name": "...",
      "file_path": "...",
      "start_line": ...,
      "end_line": ...,
      "kind": "api_failed" | "db_failed",
      "api_error": "...",          # kind=api_failed
      "db_error": "...",           # kind=db_failed
      "analysis": {...} | None,     # kind=db_failed 一般有
      "contract": {...} | None,     # kind=db_failed 一般有
      "raw": {...} | None,          # kind=api_failed 一般有 raw/db_saved 等
    }
    """
    dump_dir = Path(dump_dir) if dump_dir else (CAD_ROOT / "tools" / "_dump")
    dump_dir = Path(dump_dir)

    files = []
    if include_api_failed:
        files.append(("api_failed", dump_dir / "function_analysis_api_failed.jsonl"))
    if include_db_failed:
        files.append(("db_failed", dump_dir / "function_analysis_db_failed.jsonl"))

    items: list[dict] = []
    for kind, fp in files:
        if not fp.exists():
            continue
        try:
            with fp.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = (line or "").strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue

                    qn = obj.get("qualified_name")
                    fn = obj.get("func_name") or obj.get("function") or ""
                    rec = {
                        "ts": obj.get("ts"),
                        "qualified_name": qn,
                        "func_name": fn,
                        "file_path": obj.get("file_path"),
                        "start_line": obj.get("start_line"),
                        "end_line": obj.get("end_line"),
                        "kind": kind,
                        "api_error": obj.get("api_error"),
                        "db_error": obj.get("db_error"),
                        "analysis": obj.get("analysis"),
                        "contract": obj.get("contract"),
                        "raw": obj,  # 原始整条，便于你追溯
                    }
                    items.append(rec)
        except Exception:
            continue

    # 去重策略：qualified_name 优先；没有则退化为 (file_path, func_name, start_line)
    def _key(x: dict):
        if x.get("qualified_name"):
            return ("qn", x["qualified_name"])
        return ("fp", x.get("file_path"), x.get("func_name"), x.get("start_line"))

    # latest_only=True：同一个 key 只保留最后一条（按文件顺序就是追加顺序）
    if latest_only:
        d: dict[tuple, dict] = {}
        for it in items:
            d[_key(it)] = it
        items = list(d.values())

    # 按时间/函数名做一个稳定排序（ts 为空就排前）
    items.sort(key=lambda x: (x.get("ts") or "", x.get("qualified_name") or "", x.get("func_name") or ""))
    return items


def find_local_failed_record_for_function(
    *,
    qualified_name: str,
    dump_dir: str | Path | None = None,
) -> dict | None:
    """
    给定 qualified_name，查本地 dump 是否已有失败记录。
    有则返回那条 dict；没有返回 None。
    """
    qualified_name = (qualified_name or "").strip()
    if not qualified_name:
        return None

    recs = load_local_failed_function_records(dump_dir=dump_dir, latest_only=True)
    for r in recs:
        if r.get("qualified_name") == qualified_name:
            return r
    return None

# =============================================================================
# 六 扫描：文件顶层函数 def/async def
# =============================================================================
def list_top_level_function_defs_in_file(file: str | Path) -> list[dict]:
    p = Path(file)
    if not p.exists():
        return []
    try:
        src = _safe_read_text(p)
        tree = ast.parse(src, filename=str(p))
    except Exception:
        return []

    out: list[dict] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            out.append({"name": node.name, "lineno": getattr(node, "lineno", None), "col": getattr(node, "col_offset", None), "type": "def"})
        elif isinstance(node, ast.AsyncFunctionDef):
            out.append({"name": node.name, "lineno": getattr(node, "lineno", None), "col": getattr(node, "col_offset", None), "type": "async def"})
    out.sort(key=lambda x: (x.get("lineno") or 0, x.get("name") or ""))
    return out

# =============================================================================
# 七  源码提取：从 def 行（含装饰器）到函数结束
# =============================================================================
def extract_function_source(file: str | Path, def_line_1based: int) -> dict:
    p = Path(file)
    if not p.exists():
        return {"ok": False, "file": str(p), "errors": ["file not found"]}

    lines = _safe_read_text(p).splitlines(True)
    i = max(0, int(def_line_1based) - 1)
    if i >= len(lines):
        return {"ok": False, "file": str(p), "errors": ["line out of range"]}

    start = i
    while start > 0 and lines[start - 1].lstrip().startswith("@"):
        start -= 1

    j = start
    while j < len(lines) and not re.match(r"^\s*(async\s+def|def)\s+\w+\s*\(", lines[j]):
        j += 1
    if j >= len(lines):
        return {"ok": False, "file": str(p), "errors": ["def not found near line"]}

    def_line = j
    def_indent = len(lines[def_line]) - len(lines[def_line].lstrip(" \t"))

    end = def_line + 1
    while end < len(lines):
        line = lines[end]
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            end += 1
            continue
        indent = len(line) - len(line.lstrip(" \t"))
        if indent <= def_indent and re.match(r"^\s*(def|async\s+def|class)\s+\w+", line):
            break
        if indent <= def_indent and not line.startswith((" ", "\t")):
            break
        end += 1

    src = "".join(lines[start:end]).rstrip() + "\n"
    return {"ok": True, "file": str(p), "start_line": start + 1, "end_line": end, "source": src, "errors": []}

# =============================================================================
# 八  AST：提取 calls（函数内部调用）
# =============================================================================
class _CallCollector(ast.NodeVisitor):
    def __init__(self):
        self.items: list[dict] = []

    def _name_of(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            left = self._name_of(node.value)
            return f"{left}.{node.attr}" if left else node.attr
        return ""

    def visit_Call(self, node: ast.Call):
        name = self._name_of(node.func)
        if name:
            self.items.append({"name": name, "line": getattr(node, "lineno", None), "col": getattr(node, "col_offset", None)})
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return

def list_called_functions(
    file: str | Path,
    *,
    func_name: str,
    unique: bool = True,
    with_locations: bool = False,
) -> list:
    p = Path(file)
    if not p.exists():
        return []
    try:
        src = _safe_read_text(p)
        tree = ast.parse(src, filename=str(p))
    except Exception:
        return []

    target = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
            target = node
            break
    if target is None:
        return []

    collector = _CallCollector()
    for n in getattr(target, "body", []) or []:
        collector.visit(n)

    if with_locations:
        return collector.items

    names = [it["name"] for it in collector.items if it.get("name")]
    if not unique:
        return names

    seen = set()
    out = []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out

# =============================================================================
# 九 Fox Responses API (SSE) + 解析
# =============================================================================
def parse_sse_response_text(sse_text: str) -> dict:
    events = []
    last_response = None
    event = None
    data_buf: list[str] = []

    def flush():
        nonlocal event, data_buf, last_response
        if event is None and not data_buf:
            return
        raw = "\n".join(data_buf).strip()
        item = {"event": event, "data_raw": raw}
        try:
            if raw.startswith("{") and raw.endswith("}"):
                item["data_json"] = json.loads(raw)
        except Exception:
            pass
        events.append(item)

        dj = item.get("data_json")
        if isinstance(dj, dict) and dj.get("type") == "response.completed":
            last_response = dj.get("response")

        event = None
        data_buf = []

    for line in (sse_text or "").splitlines():
        line = line.rstrip("\n")
        if line.startswith("event:"):
            flush()
            event = line.split(":", 1)[1].strip()
        elif line.startswith("data:"):
            data_buf.append(line.split(":", 1)[1].strip())
        elif line.strip() == "":
            flush()

    flush()
    return {"events": events, "last_response_obj": last_response}

def extract_output_text_from_response(resp_obj: dict | None) -> str:
    if not isinstance(resp_obj, dict):
        return ""
    out = []
    output = resp_obj.get("output") or []
    if not isinstance(output, list):
        return ""
    for item in output:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "message":
            content = item.get("content") or []
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "output_text":
                        out.append(c.get("text") or "")
    return "\n".join([x for x in out if x])

def fox_responses_smoke_test(
    base_url: str,
    api_key: str,
    *,
    model: str,
    text: str,
    timeout: int = 60,
    max_stream_seconds: int = 120,
    session=None,
) -> dict:
    import requests

    endpoint = base_url.rstrip("/") + "/responses"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "stream": True,
        "input": [{"type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}],
    }

    sess = session or requests.Session()

    try:
        with sess.post(endpoint, headers=headers, json=payload, stream=True, timeout=timeout) as r:
            status = r.status_code
            if status >= 400:
                raw = ""
                try:
                    raw = r.text or ""
                except Exception:
                    pass
                return {"ok": False, "status_code": status, "endpoint": endpoint, "error": f"HTTP {status}", "text": raw}

            t0 = time.time()
            chunks: list[str] = []
            for line_bytes in r.iter_lines(decode_unicode=True):
                if line_bytes is None:
                    continue
                line = str(line_bytes)

                if max_stream_seconds and (time.time() - t0) > max_stream_seconds:
                    break

                chunks.append(line)

            raw_sse = "\n".join(chunks)

        parsed = parse_sse_response_text(raw_sse)
        resp_obj = parsed.get("last_response_obj")
        output_text = extract_output_text_from_response(resp_obj)

        if not output_text and max_stream_seconds:
            return {
                "ok": False,
                "status_code": status,
                "endpoint": endpoint,
                "error": f"stream timeout: exceeded {max_stream_seconds}s without completed response",
                "response_id": (resp_obj or {}).get("id") if isinstance(resp_obj, dict) else None,
                "output_text": output_text,
                "raw_sse_text": raw_sse,
            }

        return {
            "ok": True,
            "status_code": status,
            "endpoint": endpoint,
            "error": None,
            "response_id": (resp_obj or {}).get("id") if isinstance(resp_obj, dict) else None,
            "output_text": output_text,
            "raw_sse_text": raw_sse,
        }
    except Exception as e:
        return {"ok": False, "status_code": None, "endpoint": endpoint, "error": f"request failed: {e}", "text": None}

# =============================================================================
# 十  API 分析：prompt + JSON 解析
# =============================================================================
def _build_function_flow_prompt(
    *,
    func_name: str,
    func_source: str,
    local_calls: list | None,
    max_source_chars: int = 22000,
) -> str:
    lines: list[str] = []
    lines.append("你是一个“函数流程分析器”。请分析下面 Python 函数的功能流程，输出 **JSON**（仅 JSON，不要解释文字）。")
    lines.append("")
    lines.append("要求：")
    lines.append("- 简洁但完整，覆盖所有分支与返回")
    lines.append("- 列出：输入参数语义、主要步骤、关键分支条件、异常/失败分支、资源开关、返回结构")
    lines.append("- 给出：典型调用案例 2~3 个（输入->输出字段要点）")
    lines.append("- 如果函数依赖外部系统（CAD/DB/API/文件系统），在 side_effects / errors 中明确体现")
    lines.append("- **只输出一个 JSON 对象**；不要输出 Markdown，不要解释文字")
    lines.append("")

    lines.append("输出 JSON 结构必须满足：")
    lines.append("{")
    lines.append(f'  "function": "{func_name}",')
    lines.append('  "summary": "...",')
    lines.append('  "inputs": [{"name":"...","type":"...","meaning":"...","default":"..."}],')
    lines.append('  "steps": ["..."],')
    lines.append('  "branches": [{"when":"...","does":"...","returns":"..."}],')
    lines.append('  "errors": [{"case":"...","symptom":"...","handling":"...","returns":"..."}],')
    lines.append('  "side_effects": ["..."],')
    lines.append('  "returns": {')
    lines.append('    "shape": "...",')
    lines.append('    "fields": [{"path":"a.b.c","meaning":"...","example":"..."}]')
    lines.append("  },")
    lines.append('  "examples": [{"call":"...","expect":"..."}]')
    lines.append("}")
    lines.append("")

    lines.append("（可选参考）本地 AST 提取到的调用点：")
    try:
        calls_text = json.dumps(local_calls or [], ensure_ascii=False, indent=2)
    except Exception:
        calls_text = "[]"
    lines.append(calls_text)
    lines.append("")

    src = func_source or ""
    if max_source_chars and len(src) > max_source_chars:
        head = src[: int(max_source_chars * 0.75)]
        tail = src[-int(max_source_chars * 0.25):]
        src = head + "\n\n# ... [TRUNCATED: function source too long] ...\n\n" + tail
        lines.append(f"# 注意：函数源码过长，已截断显示（max_source_chars={max_source_chars}）")

    lines.append("")
    lines.append("函数源码如下：")
    lines.append("```python")
    lines.append(src)
    lines.append("```")
    return "\n".join(lines)

def analyze_function_flow_via_api(
    *,
    base_url: str,
    api_key: str,
    model: str,
    func_name: str,
    func_source: str,
    local_calls: list | None = None,
    timeout: int = 180,
    max_stream_seconds: int = 180,
    session=None,
) -> dict:
    prompt = _build_function_flow_prompt(func_name=func_name, func_source=func_source, local_calls=local_calls)

    res = fox_responses_smoke_test(
        base_url=base_url,
        api_key=api_key,
        model=model,
        text=prompt,
        timeout=timeout,
        max_stream_seconds=max_stream_seconds,
        session=session,
    )

    ret = {
        "ok": False,
        "status_code": res.get("status_code"),
        "endpoint": res.get("endpoint"),
        "response_id": res.get("response_id"),
        "error": res.get("error"),
        "output_text": res.get("output_text", "") or "",
        "analysis": None,
        "raw_sse_text": res.get("raw_sse_text"),
    }

    if not res.get("ok"):
        return ret

    text = (ret["output_text"] or "").strip()
    if not text:
        ret["error"] = "API返回为空 output_text"
        return ret

    try:
        cleaned = text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.I)
        cleaned = re.sub(r"^```\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()
        ret["analysis"] = json.loads(cleaned)
        ret["ok"] = True
        ret["error"] = None
        return ret
    except Exception as e:
        ret["error"] = f"JSON解析失败: {e}"
        return ret

def print_human_flow_summary(*, func_name: str, analysis: dict, stream=print) -> None:
    def out(s: str = ""):
        stream(s)

    out("\n" + "=" * 88)
    out(f"🧠 函数流程分析：{func_name}")
    out("=" * 88)

    summary = analysis.get("summary")
    if summary:
        out("\n【总体功能】")
        out("  " + str(summary).replace("\n", "\n  "))

    inputs = analysis.get("inputs") or []
    if isinstance(inputs, list) and inputs:
        out("\n【输入参数】")
        for p in inputs:
            name = p.get("name")
            meaning = p.get("meaning")
            default = p.get("default")
            out(f" - {name}: {meaning} (默认={default})")

    steps = analysis.get("steps") or []
    if isinstance(steps, list) and steps:
        out("\n【主要执行流程】")
        for i, step in enumerate(steps, 1):
            out(f" {i}. {step}")

    branches = analysis.get("branches") or []
    if isinstance(branches, list) and branches:
        out("\n【关键分支】")
        for b in branches:
            when = b.get("when")
            does = b.get("does")
            returns = b.get("returns")
            out(f" - 当 {when} 时：")
            out(f"   → 执行：{does}")
            out(f"   → 返回：{returns}")

    errors = analysis.get("errors") or []
    if isinstance(errors, list) and errors:
        out("\n【异常与失败路径】")
        for e in errors:
            case = e.get("case")
            symptom = e.get("symptom")
            handling = e.get("handling")
            returns = e.get("returns")
            out(f" - 情况：{case}")
            out(f"   表现：{symptom}")
            out(f"   处理：{handling}")
            out(f"   返回：{returns}")

    returns = analysis.get("returns") or {}
    if isinstance(returns, dict) and returns:
        out("\n【返回值】")
        out(f"  形式： {returns.get('shape')}")
        fields = returns.get("fields") or []
        if isinstance(fields, list):
            for f in fields:
                meaning = f.get("meaning")
                example = f.get("example")
                path = f.get("path")
                if path:
                    out(f"   - {path}: {meaning} (示例：{example})")
                else:
                    out(f"   - {meaning} (示例：{example})")

    out("\n" + "=" * 88 + "\n")

def analyze_function_flow_with_retry(
    *,
    func_name: str,
    func_source: str,
    local_calls: list | None,
    base_url: str,
    api_key: str,
    model: str = "gpt-5.3-codex",
    timeout: int = 180,
    max_stream_seconds: int = 180,
    max_retries: int = 5,
    retry_sleep: float = 2.0,
    verbose: bool = True,
    session=None,
) -> dict:
    last_error = None
    last_raw = None

    for attempt in range(1, max_retries + 1):
        api_ret = analyze_function_flow_via_api(
            base_url=base_url,
            api_key=api_key,
            model=model,
            func_name=func_name,
            func_source=func_source,
            local_calls=local_calls,
            timeout=timeout,
            max_stream_seconds=max_stream_seconds,
            session=session,
        )
        last_raw = api_ret

        if api_ret.get("ok") and isinstance(api_ret.get("analysis"), dict):
            analysis = api_ret["analysis"]
            printed = False
            if verbose:
                print_human_flow_summary(func_name=func_name, analysis=analysis)
                printed = True
            return {"ok": True, "retries": attempt, "error": None, "analysis": analysis, "printed": printed, "raw": api_ret}

        last_error = api_ret.get("error") or "unknown error"

        if attempt < max_retries:
            sleep_s = retry_sleep * attempt
            sc = api_ret.get("status_code")
            if sc in (429, 500, 502, 503, 504):
                sleep_s = max(sleep_s, 5.0 * attempt)
            time.sleep(sleep_s)

    return {"ok": False, "retries": max_retries, "error": last_error, "analysis": None, "printed": False, "raw": last_raw}

# =============================================================================
# 十一  Build Function Call Contract（v1）
# =============================================================================
def build_function_contract_v1(analysis: dict) -> dict:
    if not isinstance(analysis, dict):
        raise ValueError("analysis must be a dict")

    func_name = analysis.get("function", "")
    required_inputs: list[str] = []
    optional_inputs: Dict[str, dict] = {}

    for inp in analysis.get("inputs", []) or []:
        name = inp.get("name")
        if not name:
            continue
        optional_inputs[name] = {"type": inp.get("type"), "meaning": inp.get("meaning"), "default": inp.get("default")}

    returns = analysis.get("returns", {}) or {}
    success_output = {"type": returns.get("shape"), "fields": returns.get("fields", []), "meaning": "函数正常执行时的返回结果"}

    failure_outputs = []
    for e in analysis.get("errors", []) or []:
        failure_outputs.append({"when": e.get("case"), "returns": e.get("returns"), "meaning": e.get("symptom")})

    side_effects = analysis.get("side_effects") or []
    safe_usage_notes: list[str] = []

    if returns.get("shape") == "string":
        safe_usage_notes.append("返回值为字符串，调用方需通过内容判断成功/失败（例如是否以 ❌ 开头）")

    return {
        "function": func_name,
        "inputs": {"required": required_inputs, "optional": optional_inputs},
        "outputs": {"success": success_output, "failure": failure_outputs},
        "side_effects": side_effects,
        "safe_usage_notes": safe_usage_notes,
    }

# =============================================================================
# 十二 DB 优先：cache->api->save（写库失败 => ok=False + dump）
# =============================================================================
def analyze_function_flow_cached(
    *,
    qualified_name: str,
    func_name: str,
    func_source: str,
    local_calls: list | None,
    file_path: str,
    start_line: int | None = None,
    end_line: int | None = None,
    base_url: str,
    api_key: str,
    model: str = "gpt-5.2-codex",
    force: bool = False,
    max_retries: int = 5,
    retry_sleep: float = 2.0,
    verbose: bool = True,
    write_contract: bool = True,
    session=None,
    timeout: int = 180,
    max_stream_seconds: int = 180,
) -> dict:
    if not force:
        hit = load_function_analysis_from_db(qualified_name=qualified_name, func_source=func_source)
        if hit.get("ok") and hit.get("hit"):
            record = hit["record"]
            analysis = record.get("analysis") or {}
            if verbose:
                print_human_flow_summary(func_name=func_name, analysis=analysis)
            return {
                "ok": True,
                "cached": True,
                "analysis": analysis,
                "contract": record.get("contract"),
                "db_record": {"id": record.get("id"), "updated_at": str(record.get("updated_at")), "source_hash": record.get("source_hash")},
            }



    # 2nd cache: 本地 dump（失败记录）
    local_fail = find_local_failed_record_for_function(qualified_name=qualified_name)
    if local_fail:
        # 本地已经有记录：按你的要求，不再重新跑 API
        return {
            "ok": False,
            "cached": False,
            "cached_local": True,
            "error": local_fail.get("api_error") or local_fail.get("db_error") or "local_failed_record",
            "local_record": local_fail,
        }





    api_ret = analyze_function_flow_with_retry(
        func_name=func_name,
        func_source=func_source,
        local_calls=local_calls,
        base_url=base_url,
        api_key=api_key,
        model=model,
        max_retries=max_retries,
        retry_sleep=retry_sleep,
        verbose=verbose,
        timeout=timeout,
        max_stream_seconds=max_stream_seconds,
        session=session,
    )

    if not api_ret.get("ok"):
        save_ret = save_function_analysis_to_db(
            qualified_name=qualified_name,
            func_name=func_name,
            file_path=file_path,
            start_line=start_line,
            end_line=end_line,
            func_source=func_source,
            analysis={"function": func_name, "summary": "", "_note": "api_failed", "error": api_ret.get("error")},
            contract=None,
            ok=False,
            error_text=api_ret.get("error"),
            model=model,
            base_url=base_url,
        )
        _append_jsonl(
            CAD_ROOT / "tools" / "_dump" / "function_analysis_api_failed.jsonl",
            {
                "ts": _now_str(),
                "qualified_name": qualified_name,
                "func_name": func_name,
                "file_path": file_path,
                "start_line": start_line,
                "end_line": end_line,
                "api_error": api_ret.get("error"),
                "db_saved": save_ret,
            },
        )
        return {"ok": False, "cached": False, "error": api_ret.get("error"), "raw": api_ret.get("raw"), "db_saved": save_ret}

    analysis = api_ret.get("analysis") or {}
    contract = build_function_contract_v1(analysis) if (write_contract and isinstance(analysis, dict)) else None

    save_ret = save_function_analysis_to_db(
        qualified_name=qualified_name,
        func_name=func_name,
        file_path=file_path,
        start_line=start_line,
        end_line=end_line,
        func_source=func_source,
        analysis=analysis,
        contract=contract,
        ok=True,
        error_text=None,
        model=model,
        base_url=base_url,
    )

    if not (save_ret or {}).get("ok"):
        _append_jsonl(
            CAD_ROOT / "tools" / "_dump" / "function_analysis_db_failed.jsonl",
            {
                "ts": _now_str(),
                "qualified_name": qualified_name,
                "func_name": func_name,
                "file_path": file_path,
                "start_line": start_line,
                "end_line": end_line,
                "db_error": save_ret.get("error"),
                "analysis": analysis,
                "contract": contract,
            },
        )
        return {"ok": False, "cached": False, "error": f"db_save_failed: {save_ret.get('error')}", "analysis": analysis, "contract": contract, "db_saved": save_ret}

    return {"ok": True, "cached": False, "analysis": analysis, "contract": contract, "db_saved": save_ret}

# =============================================================================
# 十三 ENGINEERED BATCH：扫描单脚本所有顶层函数
# =============================================================================
def analyze_all_top_level_functions_in_file_with_dbop_cache(
    *,
    file_path: str | Path,
    base_url: str = "https://code.newcli.com/codex/v1",
    api_key: str | None = None,
    model: str = "gpt-5.2-codex",
    max_retries: int = 5,
    retry_sleep: float = 2.0,
    include_calls: bool = True,
    force: bool = False,
    print_each_summary: bool = False,
    timeout: int = 180,
    max_stream_seconds: int = 180,
    resume_from: str | None = None,
    stop_after: int | None = None,
) -> dict:
    import requests

    api_key = api_key or CODEX_API_KEY
    if not api_key:
        raise RuntimeError("CODEX_API_KEY not found; pass api_key or set env CODEX_API_KEY")

    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(str(p))

    ready = ensure_function_db_and_table(database=FUNC_DB_NAME, table=FUNC_TABLE_NAME)
    if not ready.get("ok"):
        raise RuntimeError(f"DB init failed: {ready.get('error')}")

    sess = requests.Session()

    defs = list_top_level_function_defs_in_file(p)
    total = len(defs)

    reused = 0
    analyzed = 0
    failed = 0
    db_save_failed = 0
    items: list[dict] = []

    print("\n" + "=" * 96)
    print("🚀 ENGINEERED BATCH (DBOP CACHE + SESSION + SSE HARD TIMEOUT)")
    print("=" * 96)
    print(f"File    : {p}")
    print(f"Model   : {model}")
    print(f"Total   : {total} functions")
    print(f"Force   : {force}")
    print(f"Resume  : {resume_from}")
    print(f"Stop    : {stop_after}")
    print(f"Timeout : {timeout}s  |  StreamHardLimit : {max_stream_seconds}s")
    print(f"Time    : {_now_str()}")
    print("=" * 96 + "\n")

    started = resume_from is None
    processed = 0

    for idx, d in enumerate(defs, 1):
        fn = d["name"]
        line = int(d.get("lineno") or 0)

        if not started:
            if fn == resume_from:
                started = True
            else:
                continue

        if stop_after is not None and processed >= stop_after:
            break

        processed += 1

        print(f"[{idx:03d}/{total:03d}] ▶️ START {fn} @L{line}", flush=True)
        t0 = time.time()

        src_info = extract_function_source(p, line)
        if not src_info.get("ok"):
            failed += 1
            err = f"extract source failed: {src_info.get('errors')}"
            dt = time.time() - t0
            print(f"[{idx:03d}/{total:03d}] ❌ END   {fn}  {dt:.1f}s  {err}", flush=True)
            items.append({"func": fn, "line": line, "ok": False, "cached": False, "error": err})
            continue

        func_src = src_info["source"]
        qn = build_qualified_name(str(p), fn)

        calls = None
        if include_calls:
            try:
                calls = list_called_functions(p, func_name=fn, unique=True, with_locations=False)
            except Exception:
                calls = None

        ret = analyze_function_flow_cached(
            qualified_name=qn,
            func_name=fn,
            func_source=func_src,
            local_calls=calls,
            file_path=_norm_path(p),
            start_line=src_info.get("start_line"),
            end_line=src_info.get("end_line"),
            base_url=base_url,
            api_key=api_key,
            model=model,
            force=force,
            max_retries=max_retries,
            retry_sleep=retry_sleep,
            verbose=print_each_summary,
            write_contract=True,
            session=sess,
            timeout=timeout,
            max_stream_seconds=max_stream_seconds,
        )

        dt = time.time() - t0

        if not ret.get("ok"):
            failed += 1
            err = ret.get("error") or "unknown error"
            if "db_save_failed:" in err:
                db_save_failed += 1
            print(f"[{idx:03d}/{total:03d}] ❌ END   {fn}  {dt:.1f}s  error={err}", flush=True)
            items.append({"func": fn, "qualified_name": qn, "line": line, "ok": False, "cached": False, "error": err, "db_saved": ret.get("db_saved")})
            continue

        if ret.get("cached"):
            reused += 1
            print(f"[{idx:03d}/{total:03d}] ✅ END   {fn}  {dt:.1f}s  (reuse DB)", flush=True)
        else:
            analyzed += 1
            print(f"[{idx:03d}/{total:03d}] ✅ END   {fn}  {dt:.1f}s  (API ok)", flush=True)

        items.append({"func": fn, "qualified_name": qn, "line": line, "ok": True, "cached": bool(ret.get("cached")), "error": None, "db_saved": ret.get("db_saved")})

    try:
        sess.close()
    except Exception:
        pass
    _db_close_conn()

    print("\n" + "=" * 96)
    print("✅ BATCH DONE (ENGINEERED)")
    print("=" * 96)
    print(f"File     : {p}")
    print(f"Total    : {total}")
    print(f"Processed: {processed}")
    print(f"Reused   : {reused}")
    print(f"Analyzed : {analyzed}")
    print(f"Failed   : {failed}")
    print(f"DB_SAVE_FAILED: {db_save_failed}")
    print(f"Time     : {_now_str()}")
    print("=" * 96 + "\n")

    return {
        "ok": failed == 0,
        "file": str(p),
        "total_functions": total,
        "processed": processed,
        "reused": reused,
        "analyzed": analyzed,
        "failed": failed,
        "db_save_failed": db_save_failed,
        "items": items,
    }
