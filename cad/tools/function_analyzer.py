#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# D:/codex-tasks/cad/tools/function_analyzer.py
# 版本 V2.4 (SCHEMA COMPAT FIX)

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


def _db_has_index(database: str, table: str, index_name: str) -> bool:
    conn = _db_get_conn(database)
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND INDEX_NAME=%s
            """,
            (database, table, index_name),
        )
        n = cur.fetchone()[0]
        return bool(n and int(n) > 0)
    finally:
        try:
            cur.close()
        except Exception:
            pass


def _db_ensure_index_qname_source(database: str, table: str) -> dict:
    """
    方案2核心：确保 uq_qname_source(qualified_name(191), source_hash) 存在（幂等）。
    - 已存在：ok=True, created=False
    - 并发/重复执行导致的 Duplicate key name：视为已存在，ok=True
    - 其它错误：ok=False
    """
    try:
        # 先查是否已有索引（最快路径）
        if _db_has_index(database, table, "uq_qname_source"):
            return {"ok": True, "created": False, "error": None}

        conn = _db_get_conn(database)
        cur = conn.cursor()
        try:
            try:
                cur.execute(
                    f"ALTER TABLE `{table}` "
                    f"ADD UNIQUE KEY `uq_qname_source` (`qualified_name`(191), `source_hash`);"
                )
                conn.commit()
                return {"ok": True, "created": True, "error": None}
            except Exception as e:
                msg = str(e)

                # ✅ 幂等容忍：索引名已存在（常见 MySQL errno 1061）
                if ("Duplicate key name" in msg) or ("1061" in msg):
                    try:
                        # 再查一次确认（避免吞掉其它错误）
                        if _db_has_index(database, table, "uq_qname_source"):
                            return {"ok": True, "created": False, "error": None}
                    except Exception:
                        # 查失败就按“已存在”处理也行，但这里更保守：返回可读错误
                        return {"ok": False, "created": False, "error": f"duplicate key name but recheck failed: {msg}"}

                    return {"ok": True, "created": False, "error": None}

                # 🚫 其它错误：直接失败上抛给调用方（由 ensure_function_db_and_table 严格处理）
                return {"ok": False, "created": False, "error": msg}
        finally:
            try:
                cur.close()
            except Exception:
                pass
    except Exception as e:
        return {"ok": False, "created": False, "error": str(e)}


def ensure_function_db_and_table(*, database: str = FUNC_DB_NAME, table: str = FUNC_TABLE_NAME) -> dict:
    """
    确保函数分析 DB 与表存在；并刷新运行时 schema 标记；
    并确保方案2索引 uq_qname_source(qualified_name(191), source_hash) 存在（幂等、严格：失败则 ok=False）。

    关键点：
    - 新建表时直接包含 uq_qhash_source + uq_qname_source 两个唯一键（新环境一步到位）
    - 老表通过 _db_ensure_index_qname_source 补齐 uq_qname_source
    - uq_qname_source 补齐失败 => 返回 ok=False（不再“假成功”）
    """
    global _DB_HAS_QUALIFIED_HASH

    try:
        # 1) 确保 DB 存在（用 dbop 的标准实现）
        try:
            dbop.create_database_if_not_exists(database)
        except Exception:
            # dbop 内部可能只是 print，不抛异常；这里兜底
            pass

        # 2) 确保表存在（兼容字段集合；新建表时包含两个唯一键）
        conn = _db_get_conn(database)
        cur = conn.cursor()
        try:
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS `{table}` (
                  `id` bigint NOT NULL AUTO_INCREMENT,
                  `qualified_name` varchar(512) NOT NULL COMMENT '模块限定名: module:func',
                  `qualified_hash` char(64) NOT NULL COMMENT 'sha256(qualified_name)',
                  `func_name` varchar(255) NOT NULL COMMENT '函数名(冗余字段便于检索)',
                  `file_path` text NOT NULL COMMENT '函数所在文件完整路径',
                  `start_line` int DEFAULT NULL COMMENT '起始行(1-based)',
                  `end_line` int DEFAULT NULL COMMENT '结束行(1-based)',
                  `source_hash` char(64) NOT NULL COMMENT '源码sha256',
                  `analysis_json` longtext NOT NULL COMMENT '分析结果JSON(文本)',
                  `contract_json` longtext COMMENT '合同JSON(可选)',
                  `model` varchar(255) DEFAULT NULL COMMENT '使用的模型',
                  `base_url` text COMMENT '使用的API base_url',
                  `ok` tinyint(1) NOT NULL DEFAULT '1' COMMENT '分析是否成功',
                  `error_text` text COMMENT '失败原因',
                  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                  PRIMARY KEY (`id`),

                  -- 兼容旧逻辑：以 qualified_hash + source_hash 为唯一
                  UNIQUE KEY `uq_qhash_source` (`qualified_hash`,`source_hash`),

                  -- 方案2主键：以 qualified_name(191) + source_hash 为唯一
                  UNIQUE KEY `uq_qname_source` (`qualified_name`(191), `source_hash`),

                  KEY `idx_qname` (`qualified_name`(191)),
                  KEY `idx_func_name` (`func_name`(191))
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
            )
            conn.commit()
        finally:
            try:
                cur.close()
            except Exception:
                pass

        # 3) 刷新 schema 标记（读真实表）
        _DB_HAS_QUALIFIED_HASH = _db_has_column(database, table, "qualified_hash")

        # 4) 方案2：确保 uq_qname_source 存在（幂等）；失败则严格返回 ok=False
        idx_ret = _db_ensure_index_qname_source(database, table)
        if not idx_ret.get("ok"):
            return {"ok": False, "error": f"ensure uq_qname_source failed: {idx_ret.get('error')}"}

        return {"ok": True, "error": None}
    except Exception as e:
        return {"ok": False, "error": str(e)}

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
    """
    方案2读库：
    - func_source 给出：优先按 (qualified_name, source_hash) 精确命中
    - 否则：按 qualified_name 取最新一条
    """
    try:
        ready = ensure_function_db_and_table(database=database, table=table)
        if not ready.get("ok"):
            return {"ok": False, "hit": False, "record": None, "error": ready.get("error")}

        source_hash = _sha256_text(func_source) if func_source is not None else None

        conn = _db_get_conn(database)
        cur = conn.cursor(dictionary=True)
        try:
            if source_hash:
                cur.execute(
                    f"""
                    SELECT *
                    FROM `{table}`
                    WHERE qualified_name=%s AND source_hash=%s
                    ORDER BY updated_at DESC, id DESC
                    LIMIT 1
                    """,
                    (qualified_name, source_hash),
                )
            else:
                cur.execute(
                    f"""
                    SELECT *
                    FROM `{table}`
                    WHERE qualified_name=%s
                    ORDER BY updated_at DESC, id DESC
                    LIMIT 1
                    """,
                    (qualified_name,),
                )

            row = cur.fetchone()
        finally:
            try:
                cur.close()
            except Exception:
                pass

        if not row:
            return {"ok": True, "hit": False, "record": None, "error": None}

        # JSON decode
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
    方案2写库：
    - 以 (qualified_name, source_hash) 唯一为主（uq_qname_source）
    - 同时写 qualified_hash，兼容旧唯一键 uq_qhash_source
    - ON DUPLICATE KEY UPDATE：两个唯一键任一触发都能更新
    """
    try:
        ready = ensure_function_db_and_table(database=database, table=table)
        if not ready.get("ok"):
            return {"ok": False, "error": ready.get("error")}

        source_hash = _sha256_text(func_source)
        qh = _qualified_hash(qualified_name)

        analysis_json = json.dumps(analysis or {}, ensure_ascii=False)
        contract_json = json.dumps(contract or {}, ensure_ascii=False) if contract is not None else None

        conn = _db_get_conn(database)
        cur = conn.cursor()
        try:
            cur.execute(
                f"""
                INSERT INTO `{table}`
                    (qualified_name, qualified_hash, func_name, file_path, start_line, end_line, source_hash,
                     analysis_json, contract_json, model, base_url, ok, error_text, updated_at)
                VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
                ON DUPLICATE KEY UPDATE
                    qualified_name=VALUES(qualified_name),
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
            conn.commit()
        finally:
            try:
                cur.close()
            except Exception:
                pass

        return {"ok": True, "error": None}
    except Exception as e:
        return {"ok": False, "error": str(e)}




def debug_db_hit_for_local_db_failed(
    *, dump_dir: str | Path | None = None, limit: int = 5
) -> list[dict]:
    recs = load_local_failed_function_records(dump_dir=dump_dir, include_api_failed=False, include_db_failed=True, latest_only=True)
    out = []
    for r in recs[:limit]:
        qn = r.get("qualified_name")
        fp = r.get("file_path")
        sl = r.get("start_line")
        if not (qn and fp and sl):
            out.append({"qualified_name": qn, "db_hit": False, "reason": "missing fields"})
            continue
        src_info = extract_function_source(fp, int(sl))
        if not src_info.get("ok"):
            out.append({"qualified_name": qn, "db_hit": False, "reason": f"extract failed {src_info.get('errors')}"})
            continue
        hit = load_function_analysis_from_db(qualified_name=qn, func_source=src_info["source"])
        out.append({
            "qualified_name": qn,
            "db_hit": bool(hit.get("ok") and hit.get("hit")),
            "db_error": hit.get("error"),
            "file": fp,
            "start_line": sl,
        })
    return out
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


def _db_get_conn_no_db():
    """
    使用 library.Databaseoperation.py 中的 connect_to_db_no_db()
    获取不指定数据库的连接，用于 CREATE DATABASE 等。
    """
    return dbop.connect_to_db_no_db()

def _local_cache_dir() -> Path:
    # ✅ 成功缓存单独放 _cache，避免跟 _dump 混用
    return CAD_ROOT / "tools" / "_cache" / "function_analysis"


def _local_cache_path(qualified_name: str, source_hash: str) -> Path:
    # 分层目录，避免单目录文件过多
    qh = _qualified_hash(qualified_name)
    return _local_cache_dir() / qh[:2] / qh[2:4] / f"{qh}__{source_hash}.json"


def load_function_analysis_from_local_cache(
    *,
    qualified_name: str,
    func_source: str,
) -> dict:
    """
    本地成功缓存：
    - 只缓存成功(ok=1)的 analysis/contract
    """
    try:
        source_hash = _sha256_text(func_source)
        fp = _local_cache_path(qualified_name, source_hash)
        if not fp.exists():
            return {"ok": True, "hit": False, "record": None, "error": None}

        obj = json.loads(_safe_read_text(fp))
        return {"ok": True, "hit": True, "record": obj, "error": None}
    except Exception as e:
        return {"ok": False, "hit": False, "record": None, "error": str(e)}


def save_function_analysis_to_local_cache(
    *,
    qualified_name: str,
    func_source: str,
    payload: dict,
) -> dict:
    """
    payload 推荐结构：
    {
      "qualified_name": "...",
      "source_hash": "...",
      "analysis": {...},
      "contract": {...} | None,
      "ok": True,
      "updated_at": "...",
    }
    """
    try:
        source_hash = _sha256_text(func_source)
        fp = _local_cache_path(qualified_name, source_hash)
        fp.parent.mkdir(parents=True, exist_ok=True)

        payload2 = dict(payload or {})
        payload2.setdefault("qualified_name", qualified_name)
        payload2.setdefault("source_hash", source_hash)
        payload2.setdefault("updated_at", _now_str())

        fp.write_text(json.dumps(payload2, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"ok": True, "path": str(fp), "error": None}
    except Exception as e:
        return {"ok": False, "path": None, "error": str(e)}


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


def find_local_analysis_record_for_function(
    *,
    qualified_name: str,
    dump_dir: str | Path | None = None,
) -> dict | None:
    """
    返回“本地可用分析记录”（优先 db_failed 且带 analysis）。
    只要 record 里有 analysis(dict)，就认为可用，可用于回填 DB 并复用。
    """
    qualified_name = (qualified_name or "").strip()
    if not qualified_name:
        return None

    recs = load_local_failed_function_records(dump_dir=dump_dir, latest_only=True)

    best = None
    for r in recs:
        if r.get("qualified_name") != qualified_name:
            continue
        analysis = r.get("analysis")
        if isinstance(analysis, dict) and analysis:
            # db_failed 一般会带 analysis/contract；优先选择它
            best = r
            if r.get("kind") == "db_failed":
                return r
    return best




def load_local_cached_function_record(
    *,
    qualified_name: str,
    dump_dir: str | Path | None = None,
) -> dict | None:
    """
    本地缓存层：只要本地 jsonl 里有 analysis/contract，就视为“可复用结果”。
    当前实现优先利用 db_failed.jsonl（因为它往往包含完整 analysis/contract）。

    返回：
      {
        "ts": "...",
        "qualified_name": "...",
        "func_name": "...",
        "file_path": "...",
        "start_line": ...,
        "end_line": ...,
        "analysis": {...},
        "contract": {...} | None,
        "source": "db_failed_jsonl" | "...",
        "raw": {...}
      }
    """
    qualified_name = (qualified_name or "").strip()
    if not qualified_name:
        return None

    dump_dir = Path(dump_dir) if dump_dir else (CAD_ROOT / "tools" / "_dump")
    fp = dump_dir / "function_analysis_db_failed.jsonl"
    if not fp.exists():
        return None

    last_hit = None
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
                if obj.get("qualified_name") != qualified_name:
                    continue

                analysis = obj.get("analysis")
                # db_failed.jsonl 通常有 analysis/contract；只要 analysis 是 dict 就可复用
                if isinstance(analysis, dict) and analysis:
                    last_hit = {
                        "ts": obj.get("ts"),
                        "qualified_name": obj.get("qualified_name"),
                        "func_name": obj.get("func_name"),
                        "file_path": obj.get("file_path"),
                        "start_line": obj.get("start_line"),
                        "end_line": obj.get("end_line"),
                        "analysis": analysis,
                        "contract": obj.get("contract"),
                        "source": "db_failed_jsonl",
                        "raw": obj,
                    }
    except Exception:
        return None

    return last_hit


def backfill_db_from_local_record(
    *,
    local_rec: dict,
    func_source: str,
    model: str | None,
    base_url: str | None,
    database: str = FUNC_DB_NAME,
    table: str = FUNC_TABLE_NAME,
) -> dict:
    """
    将本地缓存(analysis/contract)回填到数据库。
    - 只要 local_rec 里有 analysis(dict)，就尝试 save_function_analysis_to_db
    - 写库失败也不算致命（因为本地已经可用），只返回状态
    """
    if not isinstance(local_rec, dict):
        return {"ok": False, "error": "local_rec not dict"}

    analysis = local_rec.get("analysis")
    if not isinstance(analysis, dict) or not analysis:
        return {"ok": False, "error": "local_rec has no analysis"}

    qualified_name = local_rec.get("qualified_name") or ""
    func_name = local_rec.get("func_name") or analysis.get("function") or ""
    file_path = local_rec.get("file_path") or ""
    start_line = local_rec.get("start_line")
    end_line = local_rec.get("end_line")
    contract = local_rec.get("contract")

    return save_function_analysis_to_db(
        qualified_name=qualified_name,
        func_name=func_name,
        file_path=file_path,
        start_line=start_line,
        end_line=end_line,
        func_source=func_source,
        analysis=analysis,
        contract=contract if isinstance(contract, dict) else None,
        ok=True,
        error_text=None,
        model=model,
        base_url=base_url,
        database=database,
        table=table,
    )


def replay_db_failed_jsonl_to_db(
    *,
    dump_dir: str | Path | None = None,
    database: str = FUNC_DB_NAME,
    table: str = FUNC_TABLE_NAME,
    dry_run: bool = False,
    verbose: bool = True,
    limit: int | None = None,
) -> dict:
    dump_dir = Path(dump_dir) if dump_dir else (CAD_ROOT / "tools" / "_dump")
    fp = Path(dump_dir) / "function_analysis_db_failed.jsonl"

    if not fp.exists():
        return {
            "ok": False,
            "error": f"db_failed jsonl not found: {fp}",
            "total": 0,
            "would_write": 0,
            "written": 0,
            "skipped": 0,
            "failed": 0,
            "file_missing": 0,
            "extract_failed": 0,
            "dry_run": dry_run,
            "errors": [],
        }

    ready = ensure_function_db_and_table(database=database, table=table)
    if not ready.get("ok"):
        return {
            "ok": False,
            "error": f"DB init failed: {ready.get('error')}",
            "total": 0,
            "would_write": 0,
            "written": 0,
            "skipped": 0,
            "failed": 0,
            "file_missing": 0,
            "extract_failed": 0,
            "dry_run": dry_run,
            "errors": [],
        }

    total = 0
    would_write = 0
    written = 0
    skipped = 0
    failed = 0
    file_missing = 0
    extract_failed = 0
    errors: list[dict] = []

    def _vprint(*a):
        if verbose:
            print(*a)

    _vprint("\n" + "=" * 96)
    _vprint("🔁 REPLAY DB_FAILED JSONL -> DB")
    _vprint("=" * 96)
    _vprint(f"DumpFile : {fp}")
    _vprint(f"DB       : {database}.{table}")
    _vprint(f"DryRun   : {dry_run}")
    _vprint(f"Limit    : {limit}")
    _vprint("=" * 96 + "\n")

    with fp.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if limit is not None and total >= int(limit):
                break

            line = (line or "").strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue

            total += 1

            qn = (obj.get("qualified_name") or "").strip()
            func_name = (obj.get("func_name") or "").strip()
            file_path = obj.get("file_path")
            start_line = obj.get("start_line")
            analysis = obj.get("analysis")
            contract = obj.get("contract")

            if not qn or not file_path:
                failed += 1
                if len(errors) < 10:
                    errors.append({"qualified_name": qn, "reason": "missing qualified_name or file_path"})
                continue

            p = Path(file_path)
            if not p.exists():
                file_missing += 1
                if len(errors) < 10:
                    errors.append({"qualified_name": qn, "reason": f"file missing: {p}"})
                continue

            if not start_line:
                extract_failed += 1
                if len(errors) < 10:
                    errors.append({"qualified_name": qn, "reason": "missing start_line; cannot extract source"})
                continue

            src_info = extract_function_source(p, int(start_line))
            if not src_info.get("ok"):
                extract_failed += 1
                if len(errors) < 10:
                    errors.append({"qualified_name": qn, "reason": f"extract source failed: {src_info.get('errors')}"})
                continue

            func_source = src_info.get("source") or ""

            hit = load_function_analysis_from_db(
                qualified_name=qn,
                func_source=func_source,
                database=database,
                table=table,
            )
            if hit.get("ok") and hit.get("hit"):
                skipped += 1
                continue

            if not isinstance(analysis, dict) or not analysis:
                failed += 1
                if len(errors) < 10:
                    errors.append({"qualified_name": qn, "reason": "no analysis dict in jsonl record"})
                continue

            would_write += 1
            if dry_run:
                continue

            save_ret = save_function_analysis_to_db(
                qualified_name=qn,
                func_name=func_name or (analysis.get("function") or ""),
                file_path=str(p),
                start_line=int(src_info.get("start_line")) if src_info.get("start_line") else None,
                end_line=int(src_info.get("end_line")) if src_info.get("end_line") else None,
                func_source=func_source,
                analysis=analysis,
                contract=contract if isinstance(contract, dict) else None,
                ok=True,
                error_text=None,
                model=None,
                base_url=None,
                database=database,
                table=table,
            )

            if save_ret.get("ok"):
                written += 1
            else:
                failed += 1
                if len(errors) < 10:
                    errors.append({"qualified_name": qn, "reason": f"db save failed: {save_ret.get('error')}"})

    _vprint("\n" + "=" * 96)
    _vprint("✅ REPLAY DONE")
    _vprint("=" * 96)
    _vprint(f"Total       : {total}")
    _vprint(f"WouldWrite  : {would_write}{' (dry_run)' if dry_run else ''}")
    _vprint(f"Written     : {written}")
    _vprint(f"Skipped     : {skipped}  (already in DB)")
    _vprint(f"Failed      : {failed}")
    _vprint(f"FileMissing : {file_missing}")
    _vprint(f"ExtractFail : {extract_failed}")
    _vprint("=" * 96 + "\n")

    return {
        "ok": (failed == 0 and extract_failed == 0 and file_missing == 0),
        "total": total,
        "would_write": would_write,
        "written": written,
        "skipped": skipped,
        "failed": failed,
        "file_missing": file_missing,
        "extract_failed": extract_failed,
        "dry_run": dry_run,
        "errors": errors,
        "dump_file": str(fp),
        "db": f"{database}.{table}",
    }


#把失败统一落地到json
def dump_failed_function_analysis(
    *,
    qualified_name: str,
    func_name: str,
    file_path: str,
    start_line: int | None,
    end_line: int | None,
    func_source: str | None = None,
    analysis: dict | None = None,
    contract: dict | None = None,
    api_error: str | None = None,
    db_error: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
    dump_dir: str | Path | None = None,
) -> dict:
    """
    统一将失败记录写入 tools/_dump/*.jsonl
    分类规则（更严格）：
    - db_failed：只要 db_error 存在（通常带 analysis/contract，便于回放回填）
    - api_failed：api_error 存在 且 analysis 为空（即 API 没产出可用 analysis）
    - 其它情况：拒绝落盘（避免写垃圾行）
    """
    dump_dir = Path(dump_dir) if dump_dir else (CAD_ROOT / "tools" / "_dump")
    dump_dir.mkdir(parents=True, exist_ok=True)

    # ---- 分类 ----
    kind = None
    if db_error:
        kind = "db_failed"
    elif api_error and not (isinstance(analysis, dict) and analysis):
        kind = "api_failed"
    else:
        return {"ok": False, "path": None, "error": "no meaningful failure info to dump"}

    rec = {
        "ts": _now_str(),
        "kind": kind,
        "qualified_name": qualified_name,
        "func_name": func_name,
        "file_path": str(file_path) if file_path is not None else None,
        "start_line": start_line,
        "end_line": end_line,
        "model": model,
        "base_url": base_url,
        "api_error": api_error,
        "db_error": db_error,
    }

    if func_source is not None:
        rec["source_hash"] = _sha256_text(func_source)

    if isinstance(analysis, dict) and analysis:
        rec["analysis"] = analysis
    if isinstance(contract, dict) and contract:
        rec["contract"] = contract

    try:
        fp = dump_dir / ("function_analysis_db_failed.jsonl" if kind == "db_failed" else "function_analysis_api_failed.jsonl")
        _append_jsonl(fp, rec)
        return {"ok": True, "path": str(fp), "error": None}
    except Exception as e:
        return {"ok": False, "path": None, "error": str(e)}


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
    model: str = "gpt-5.2-codex",
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
    file_path: str,
    start_line: int | None,
    end_line: int | None,
    func_source: str,

    # --- 你 batch 里会传的参数 ---
    local_calls: list | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    force: bool = False,
    verbose: bool = False,
    write_contract: bool = True,
    session=None,
    timeout: int = 180,
    max_stream_seconds: int = 180,
    max_retries: int = 5,
    retry_sleep: float = 2.0,

    database: str = FUNC_DB_NAME,
    table: str = FUNC_TABLE_NAME,
) -> dict:
    """
    方案2缓存优先级（严格工程版）：
      1) 本地成功缓存（命中则直接返回；同时尝试写回DB，写库失败 => ok=False）
      2) DB（命中则返回；并落本地成功缓存）
      3) 本地失败 dump（命中则直接返回失败，不跑API）
      4) API（成功后写DB+写本地成功缓存；写库失败 => ok=False + dump db_failed）
         API失败 => dump api_failed
    """

    # -------------------------
    # 0) 参数归一
    # -------------------------
    base_url = base_url or "https://code.newcli.com/codex/v1"
    model = model or "gpt-5.2-codex"

    # -------------------------
    # 1) 本地成功缓存（可跳过）
    # -------------------------
    if not force:
        local_ok = load_function_analysis_from_local_cache(
            qualified_name=qualified_name,
            func_source=func_source,
        )
        if local_ok.get("ok") and local_ok.get("hit"):
            rec = local_ok["record"] or {}
            analysis = rec.get("analysis") or {}
            contract = rec.get("contract")

            # 尝试写回 DB（幂等 upsert）
            db_ret = save_function_analysis_to_db(
                qualified_name=qualified_name,
                func_name=func_name,
                file_path=file_path,
                start_line=start_line,
                end_line=end_line,
                func_source=func_source,
                analysis=analysis,
                contract=contract if isinstance(contract, dict) else None,
                ok=True,
                error_text=None,
                model=rec.get("model") or model,
                base_url=rec.get("base_url") or base_url,
                database=database,
                table=table,
            )

            if verbose:
                try:
                    print_human_flow_summary(func_name=func_name, analysis=analysis)
                except Exception:
                    pass

            if not db_ret.get("ok"):
                # 写库失败不算成功（按你的硬要求）
                dump_failed_function_analysis(
                    qualified_name=qualified_name,
                    func_name=func_name,
                    file_path=file_path,
                    start_line=start_line,
                    end_line=end_line,
                    func_source=func_source,
                    analysis=analysis if isinstance(analysis, dict) else None,
                    contract=contract if isinstance(contract, dict) else None,
                    api_error=None,
                    db_error=db_ret.get("error"),
                    model=model,
                    base_url=base_url,
                )
                return {
                    "ok": False,
                    "cached": True,
                    "cache_layer": "local_ok",
                    "error": f"db_save_failed: {db_ret.get('error')}",
                    "analysis": analysis,
                    "contract": contract,
                    "db_saved": db_ret,
                }

            return {
                "ok": True,
                "cached": True,
                "cache_layer": "local_ok",
                "error": None,
                "analysis": analysis,
                "contract": contract,
                "db_saved": db_ret,
            }

        # -------------------------
        # 2) DB 命中
        # -------------------------
        hit = load_function_analysis_from_db(
            qualified_name=qualified_name,
            func_source=func_source,
            database=database,
            table=table,
        )
        if hit.get("ok") and hit.get("hit"):
            record = hit["record"] or {}
            analysis = record.get("analysis") or {}
            contract = record.get("contract")

            # 落本地成功缓存（只要 DB 命中就缓存，提升离线能力）
            save_function_analysis_to_local_cache(
                qualified_name=qualified_name,
                func_source=func_source,
                payload={
                    "analysis": analysis,
                    "contract": contract,
                    "ok": True,
                    "model": record.get("model") or model,
                    "base_url": record.get("base_url") or base_url,
                },
            )

            if verbose:
                try:
                    print_human_flow_summary(func_name=func_name, analysis=analysis)
                except Exception:
                    pass

            return {
                "ok": True,
                "cached": True,
                "cache_layer": "db",
                "error": None,
                "analysis": analysis,
                "contract": contract,
                "db_record": {
                    "id": record.get("id"),
                    "updated_at": str(record.get("updated_at")),
                    "source_hash": record.get("source_hash"),
                },
            }

    # -------------------------
    # 3) 本地失败 dump（命中则直接返回失败）
    # -------------------------
    local_fail = find_local_failed_record_for_function(qualified_name=qualified_name)
    if local_fail:
        return {
            "ok": False,
            "cached": True,
            "cache_layer": "local_failed",
            "error": local_fail.get("api_error") or local_fail.get("db_error") or "local_failed_record",
            "analysis": None,
            "contract": None,
            "local_record": local_fail,
        }

    # -------------------------
    # 4) 调 API：用你文件里已有的 analyze_function_flow_with_retry
    # -------------------------
    api_ret = analyze_function_flow_with_retry(
        func_name=func_name,
        func_source=func_source,
        local_calls=local_calls,
        base_url=base_url,
        api_key=api_key,
        model=model,
        timeout=timeout,
        max_stream_seconds=max_stream_seconds,
        max_retries=max_retries,
        retry_sleep=retry_sleep,
        verbose=verbose,
        session=session,
    )

    if not api_ret.get("ok") or not isinstance(api_ret.get("analysis"), dict):
        err = api_ret.get("error") or "api_failed"
        dump_failed_function_analysis(
            qualified_name=qualified_name,
            func_name=func_name,
            file_path=file_path,
            start_line=start_line,
            end_line=end_line,
            func_source=func_source,
            analysis=None,
            contract=None,
            api_error=err,
            db_error=None,
            model=model,
            base_url=base_url,
        )
        return {
            "ok": False,
            "cached": False,
            "cache_layer": None,
            "error": err,
            "analysis": None,
            "contract": None,
            "raw": api_ret.get("raw"),
        }

    analysis = api_ret["analysis"]

    # 可选：生成合同
    contract = None
    if write_contract:
        try:
            contract = build_function_contract_v1(analysis)
        except Exception:
            contract = None

    # -------------------------
    # 5) 写 DB（写库失败 => ok=False + dump db_failed）
    # -------------------------
    db_ret = save_function_analysis_to_db(
        qualified_name=qualified_name,
        func_name=func_name,
        file_path=file_path,
        start_line=start_line,
        end_line=end_line,
        func_source=func_source,
        analysis=analysis,
        contract=contract if isinstance(contract, dict) else None,
        ok=True,
        error_text=None,
        model=model,
        base_url=base_url,
        database=database,
        table=table,
    )

    if not db_ret.get("ok"):
        dump_failed_function_analysis(
            qualified_name=qualified_name,
            func_name=func_name,
            file_path=file_path,
            start_line=start_line,
            end_line=end_line,
            func_source=func_source,
            analysis=analysis,
            contract=contract if isinstance(contract, dict) else None,
            api_error=None,
            db_error=db_ret.get("error"),
            model=model,
            base_url=base_url,
        )
        return {
            "ok": False,
            "cached": False,
            "cache_layer": None,
            "error": f"db_save_failed: {db_ret.get('error')}",
            "analysis": analysis,
            "contract": contract,
            "db_saved": db_ret,
        }

    # -------------------------
    # 6) 写本地成功缓存（只有 DB 成功才算“成功缓存”）
    # -------------------------
    save_function_analysis_to_local_cache(
        qualified_name=qualified_name,
        func_source=func_source,
        payload={
            "analysis": analysis,
            "contract": contract,
            "ok": True,
            "model": model,
            "base_url": base_url,
        },
    )

    if verbose:
        try:
            print_human_flow_summary(func_name=func_name, analysis=analysis)
        except Exception:
            pass

    return {
        "ok": True,
        "cached": False,
        "cache_layer": None,
        "error": None,
        "analysis": analysis,
        "contract": contract,
        "db_saved": db_ret,
        "raw": api_ret.get("raw"),
    }


# =============================================================================
# 十三 ENGINEERED BATCH：扫描单脚本所有顶层函数
# =============================================================================
def analyze_all_top_level_functions_in_file_with_dbop_cache(
    *,
    file_path: str | Path,
    base_url: str = "https://code.newcli.com/codex/v1",
    api_key: str | None = None,
    model: str = "gpt-5.3-codex",
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
    """
    ENGINEERED BATCH：扫描单脚本所有顶层函数
    - 缓存层级打印：local_ok / db / local_failed / api
    - 统计拆分：reused_local_ok / reused_db / cached_failed / analyzed_api_ok / failed / db_save_failed
    """
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

    reused_local_ok = 0
    reused_db = 0
    cached_failed = 0
    analyzed_api_ok = 0
    failed = 0
    db_save_failed = 0

    items: list[dict] = []

    print("\n" + "=" * 96)
    print("🚀 ENGINEERED BATCH (CACHE LAYERS + SESSION + SSE HARD TIMEOUT)")
    print("=" * 96)
    print(f"File    : {p}")
    print(f"Model   : {model}")
    print(f"Total   : {total} functions")
    print(f"Force   : {force}   (True=skip success caches, still respects local_failed short-circuit)")
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

        if stop_after is not None and processed >= int(stop_after):
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
            items.append({
                "func": fn,
                "qualified_name": None,
                "line": line,
                "ok": False,
                "cached": False,
                "cache_layer": None,
                "error": err,
            })
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

        # ---- 失败 ----
        if not ret.get("ok"):
            failed += 1
            err = ret.get("error") or "unknown error"
            layer = ret.get("cache_layer")
            if isinstance(err, str) and "db_save_failed:" in err:
                db_save_failed += 1

            # local_failed 命中：单独计数，便于你评估“失败缓存是否在阻挡推进”
            if ret.get("cached") and layer == "local_failed":
                cached_failed += 1
                print(f"[{idx:03d}/{total:03d}] ⛔ END   {fn}  {dt:.1f}s  (CACHE=local_failed)  error={err}", flush=True)
            else:
                print(f"[{idx:03d}/{total:03d}] ❌ END   {fn}  {dt:.1f}s  error={err}", flush=True)

            items.append({
                "func": fn,
                "qualified_name": qn,
                "line": line,
                "ok": False,
                "cached": bool(ret.get("cached")),
                "cache_layer": layer,
                "error": err,
                "db_saved": ret.get("db_saved"),
            })
            continue

        # ---- 成功 ----
        layer = ret.get("cache_layer")
        if ret.get("cached"):
            # cached 成功只可能是 local_ok 或 db（按我们的实现）
            if layer == "local_ok":
                reused_local_ok += 1
                print(f"[{idx:03d}/{total:03d}] ✅ END   {fn}  {dt:.1f}s  (CACHE=local_ok)", flush=True)
            elif layer == "db":
                reused_db += 1
                print(f"[{idx:03d}/{total:03d}] ✅ END   {fn}  {dt:.1f}s  (CACHE=db)", flush=True)
            else:
                # 理论上不会出现，但保底
                print(f"[{idx:03d}/{total:03d}] ✅ END   {fn}  {dt:.1f}s  (CACHE={layer})", flush=True)
        else:
            analyzed_api_ok += 1
            print(f"[{idx:03d}/{total:03d}] ✅ END   {fn}  {dt:.1f}s  (API ok)", flush=True)

        items.append({
            "func": fn,
            "qualified_name": qn,
            "line": line,
            "ok": True,
            "cached": bool(ret.get("cached")),
            "cache_layer": layer,
            "error": None,
            "db_saved": ret.get("db_saved"),
        })

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
    print(f"Reused   : local_ok={reused_local_ok} | db={reused_db}")
    print(f"API_OK   : {analyzed_api_ok}")
    print(f"CachedFailed(local_failed): {cached_failed}")
    print(f"Failed   : {failed}")
    print(f"DB_SAVE_FAILED: {db_save_failed}")
    print(f"Time     : {_now_str()}")
    print("=" * 96 + "\n")

    return {
        "ok": failed == 0,
        "file": str(p),
        "total_functions": total,
        "processed": processed,
        "reused_local_ok": reused_local_ok,
        "reused_db": reused_db,
        "analyzed_api_ok": analyzed_api_ok,
        "cached_failed": cached_failed,
        "failed": failed,
        "db_save_failed": db_save_failed,
        "items": items,
    }


#数据库迁移

def migrate_function_analysis_table_to_v2(*, dry_run: bool = False, drop_old: bool = False) -> dict:
    """
    迁移策略（安全默认）：
    1) 检查 (qualified_name, source_hash) 是否有重复（有则拒绝迁移）
    2) 添加 uq_qname_source（若已存在则跳过）
    3) updated_at 加 ON UPDATE（若已具备则可能报错/或无影响；这里尽量容忍“已是目标状态”）
    4) 是否删除旧 uq_qhash_source：默认 False（避免破坏旧逻辑/兼容）

    返回：
    {
      "ok": bool,
      "dry_run": bool,
      "drop_old": bool,
      "sql": [...],        # dry_run=True 时返回
      "errors": [...],     # 执行错误（少量样本）
    }
    """
    from library import Databaseoperation as dbop

    db = FUNC_DB_NAME
    table = FUNC_TABLE_NAME

    # 1) 查重复：如果有重复，加 uq_qname_source 会直接失败（Duplicate entry），必须先清理
    dup = dbop.execute_sql(
        db,
        f"""
        SELECT qualified_name, source_hash, COUNT(*) AS c
        FROM `{table}`
        GROUP BY qualified_name, source_hash
        HAVING c > 1
        """,
        fetch=True,
        dictionary=True,
    )

    if dup:
        return {"ok": False, "stage": "check_duplicates", "duplicates": dup, "dry_run": dry_run, "drop_old": drop_old}

    stmts = [
        # 2) 新增方案2唯一键（若已存在应容忍）
        f"ALTER TABLE `{table}` ADD UNIQUE KEY `uq_qname_source` (`qualified_name`(191), `source_hash`);",

        # 3) updated_at 自动更新（如果已设置，可能不同 MySQL/驱动会报“无变化/重复定义”等，后面做容忍）
        f"""ALTER TABLE `{table}`
            MODIFY COLUMN `updated_at` DATETIME NOT NULL
              DEFAULT CURRENT_TIMESTAMP
              ON UPDATE CURRENT_TIMESTAMP
              COMMENT '更新时间';""",
    ]

    if drop_old:
        stmts.append(f"ALTER TABLE `{table}` DROP INDEX `uq_qhash_source`;")

    if dry_run:
        return {"ok": True, "dry_run": True, "drop_old": drop_old, "sql": stmts}

    errors: list[dict] = []

    def _is_duplicate_key_name(msg: str) -> bool:
        m = (msg or "")
        # 常见：1061 Duplicate key name / "Duplicate key name"
        return ("1061" in m) or ("Duplicate key name" in m)

    def _is_duplicate_entry(msg: str) -> bool:
        m = (msg or "")
        # 常见：1062 Duplicate entry
        return ("1062" in m) or ("Duplicate entry" in m)

    def _is_already_target_state(msg: str) -> bool:
        """
        容忍一些“已经是目标状态/无变化”的报错文本（不同驱动可能差异很大）
        """
        m = (msg or "").lower()
        return any(x in m for x in [
            "duplicate key name",      # 已存在索引
            "already exists",          # 已存在
            "can't drop",              # drop_old 时索引不存在（可选容忍）
            "doesn't exist",           # drop_old 时索引不存在（可选容忍）
            "unchanged",               # 有的驱动会提示无变化
            "same",                    # 同上（保守）
        ])

    for s in stmts:
        try:
            dbop.execute_sql(db, s)
        except Exception as e:
            msg = str(e)

            # uq_qname_source 已存在：允许跳过
            if ("uq_qname_source" in msg) and _is_duplicate_key_name(msg):
                continue

            # uq_qname_source 添加时出现 Duplicate entry：这是数据问题，不能吞，直接失败返回
            if ("uq_qname_source" in msg) and _is_duplicate_entry(msg):
                errors.append({"sql": s, "error": msg})
                return {"ok": False, "dry_run": False, "drop_old": drop_old, "errors": errors, "stage": "add_uq_qname_source_duplicate_entry"}

            # updated_at 修改：若因为“已是目标状态/差异提示”而失败，尽量容忍
            if "modify column" in (s or "").lower() and _is_already_target_state(msg):
                continue

            # drop_old：索引不存在时可容忍（因为 drop_old 是可选行为）
            if drop_old and ("drop index" in (s or "").lower()) and _is_already_target_state(msg):
                continue

            errors.append({"sql": s, "error": msg})

    return {"ok": len(errors) == 0, "dry_run": False, "drop_old": drop_old, "errors": errors}













