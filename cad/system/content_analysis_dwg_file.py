#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# D:/codex-tasks/cad/system/content_analysis_dwg_file.py

#&&&% 导入

from __future__ import annotations

import time
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import ast
from typing import Iterable,Any
import os
import re
import requests


# 引导：找到 cad 根目录
current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent
sys.path.insert(0, str(current))

CAD_AUDIT_DB = "CAD_AUDIT"

# 早绑定系统入口
from system.licad import C
from system.CAD_selection import get_attr
from system import CAD_core
from system.common_logger import sys_logger  # ✅ 统一消息控制
# 你的数据库通用库
from library.Databaseoperation import (
    create_database_if_not_exists,
    create_table,
    connect_to_db,
    ensure_connection_alive,
)
from system.CAD_com_utils  import  timeit


# =========================
# 小工具
# =========================

def _now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _sha1_text(s: str) -> str:
    return hashlib.sha1((s or "").encode("utf-8", errors="ignore")).hexdigest()

def _norm_path(s: str) -> str:
    if not s:
        return ""
    return str(s).strip().replace("\\", "/").lower()

def _safe_json(obj):
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return json.dumps(str(obj), ensure_ascii=False)

def _try(fn, default=None):
    try:
        return fn()
    except Exception:
        return default

def _parse_identifier(identifier: str) -> dict:
    raw = (identifier or "").strip()
    raw_norm = _norm_path(raw)
    is_path = ("/" in raw_norm)

    base = raw_norm.split("/")[-1] if raw_norm else ""
    stem = base[:-4] if base.endswith(".dwg") else (Path(base).stem if base else "")
    ext = (Path(base).suffix.lower() if base else "")

    return {
        "raw": raw,
        "raw_norm": raw_norm,
        "is_path": is_path,
        "base": base,
        "stem": stem,
        "ext": ext,
    }

#&&&% 数据库

# =========================
# 数据库：建库建表（保持不变）
# =========================

def ensure_cad_audit_schema():
    create_database_if_not_exists(CAD_AUDIT_DB)

    create_table(
        CAD_AUDIT_DB,
        "dwg_files",
        {
            "id": ("INT AUTO_INCREMENT PRIMARY KEY", "主键"),
            "file_key": ("CHAR(40)", "稳定键：sha1(规范化路径或文件名)"),
            "fullname": ("TEXT", "完整路径（可能为空）"),
            "fullname_norm": ("TEXT", "完整路径规范化（小写/斜杠）"),
            "basename": ("VARCHAR(260)", "文件名（含后缀，如 a.dwg）"),
            "basename_norm": ("VARCHAR(260)", "文件名规范化"),
            "stem": ("VARCHAR(260)", "文件名不含后缀（如 a）"),
            "ext": ("VARCHAR(20)", "后缀（如 .dwg）"),
            "created_at": ("DATETIME DEFAULT CURRENT_TIMESTAMP", "创建时间"),
            "updated_at": ("DATETIME DEFAULT CURRENT_TIMESTAMP", "更新时间"),
        }
    )

    create_table(
        CAD_AUDIT_DB,
        "cad_snapshots",
        {
            "id": ("BIGINT AUTO_INCREMENT PRIMARY KEY", "主键"),
            "file_id": ("INT", "外键：dwg_files.id"),
            "ts": ("DATETIME", "采集时间"),
            "ok": ("TINYINT(1)", "状态是否健康"),
            "acad_version": ("VARCHAR(64)", "CAD版本"),
            "dwg_path_used": ("TEXT", "本次实际采集使用的路径/名称"),
            "readonly": ("TINYINT(1)", "只读"),
            "saved": ("TINYINT(1)", "是否已保存"),
            "recovery_guess": ("TINYINT(1)", "恢复/损坏猜测标志"),
            "total_seen": ("INT", "扫描到的对象数"),
            "obj_digest": ("CHAR(40)", "对象摘要sha1"),
            "counts_json": ("JSON", "对象计数JSON"),
            "health_json": ("JSON", "健康检查JSON"),
            "state_json": ("JSON", "完整返回字典JSON（便于直接复用）"),
            "source": ("VARCHAR(20)", "computed 或 db"),
        }
    )

    db = connect_to_db(CAD_AUDIT_DB)
    db = ensure_connection_alive(db, CAD_AUDIT_DB)
    cur = db.cursor()
    try:
        cur.execute("CREATE INDEX idx_dwg_files_file_key ON dwg_files(file_key)")
    except Exception:
        pass
    try:
        cur.execute("CREATE INDEX idx_dwg_files_basename_norm ON dwg_files(basename_norm)")
    except Exception:
        pass
    try:
        cur.execute("CREATE INDEX idx_dwg_files_stem ON dwg_files(stem)")
    except Exception:
        pass
    try:
        cur.execute("CREATE INDEX idx_snap_file_ts ON cad_snapshots(file_id, ts)")
    except Exception:
        pass
    db.commit()
    cur.close()
    db.close()

# =========================
# 数据库：写入与查询（保持不变，改用 logger）
# =========================

def _upsert_dwg_file_record(fullname: str, basename: str) -> int | None:
    ensure_cad_audit_schema()

    fullname_norm = _norm_path(fullname)
    basename_norm = _norm_path(basename)
    stem = (Path(basename_norm).stem if basename_norm else "")
    ext = (Path(basename_norm).suffix.lower() if basename_norm else "")

    key_src = fullname_norm if fullname_norm else basename_norm
    file_key = _sha1_text(key_src)

    db = connect_to_db(CAD_AUDIT_DB)
    db = ensure_connection_alive(db, CAD_AUDIT_DB)
    cur = db.cursor()

    try:
        cur.execute("SELECT id FROM dwg_files WHERE file_key=%s LIMIT 1", (file_key,))
        row = cur.fetchone()
        if row:
            file_id = int(row[0])
            cur.execute(
                """
                UPDATE dwg_files
                SET fullname=%s, fullname_norm=%s, basename=%s, basename_norm=%s, stem=%s, ext=%s,
                    updated_at=CURRENT_TIMESTAMP
                WHERE id=%s
                """,
                (fullname, fullname_norm, basename, basename_norm, stem, ext, file_id)
            )
            db.commit()
            return file_id

        if fullname_norm:
            cur.execute("SELECT id FROM dwg_files WHERE fullname_norm=%s LIMIT 1", (fullname_norm,))
            row = cur.fetchone()
            if row:
                file_id = int(row[0])
                cur.execute(
                    """
                    UPDATE dwg_files
                    SET file_key=%s, fullname=%s, fullname_norm=%s, basename=%s, basename_norm=%s, stem=%s, ext=%s,
                        updated_at=CURRENT_TIMESTAMP
                    WHERE id=%s
                    """,
                    (file_key, fullname, fullname_norm, basename, basename_norm, stem, ext, file_id)
                )
                db.commit()
                return file_id

        if basename_norm:
            cur.execute("SELECT id FROM dwg_files WHERE basename_norm=%s LIMIT 1", (basename_norm,))
            row = cur.fetchone()
            if row:
                file_id = int(row[0])
                cur.execute(
                    """
                    UPDATE dwg_files
                    SET file_key=%s, fullname=%s, fullname_norm=%s, basename=%s, basename_norm=%s, stem=%s, ext=%s,
                        updated_at=CURRENT_TIMESTAMP
                    WHERE id=%s
                    """,
                    (file_key, fullname, fullname_norm, basename, basename_norm, stem, ext, file_id)
                )
                db.commit()
                return file_id

        cur.execute(
            """
            INSERT INTO dwg_files(file_key, fullname, fullname_norm, basename, basename_norm, stem, ext)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            """,
            (file_key, fullname, fullname_norm, basename, basename_norm, stem, ext)
        )
        db.commit()
        return int(cur.lastrowid)

    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass
        sys_logger.error("❌ _upsert_dwg_file_record 失败: %s", e)
        return None
    finally:
        cur.close()
        db.close()


def persist_cad_state(state: dict) -> int | None:
    ensure_cad_audit_schema()

    dwg = state.get("dwg", {}) if isinstance(state, dict) else {}
    fullname = str(dwg.get("fullname") or "")
    name = str(dwg.get("name") or "")
    basename = _norm_path(fullname).split("/")[-1] if fullname else name

    file_id = _upsert_dwg_file_record(fullname=fullname, basename=basename)
    if not file_id:
        return None

    ts = state.get("ts") or _now_str()
    ok = 1 if bool(state.get("ok", False)) else 0
    acad_version = (state.get("acad", {}) or {}).get("version", "")
    dwg_path_used = (dwg.get("path_used") or "")

    readonly = dwg.get("readonly")
    saved = dwg.get("saved")
    recovery_guess = dwg.get("recovery_guess")

    objs = state.get("objects", {}) or {}
    total_seen = objs.get("total_seen")
    obj_digest = objs.get("obj_digest") or ""
    counts_json = objs.get("counts", {}) or {}
    health_json = state.get("health", {}) or {}
    state_json = state

    db = connect_to_db(CAD_AUDIT_DB)
    db = ensure_connection_alive(db, CAD_AUDIT_DB)
    cur = db.cursor()

    try:
        cur.execute(
            """
            INSERT INTO cad_snapshots
            (file_id, ts, ok, acad_version, dwg_path_used, readonly, saved, recovery_guess,
             total_seen, obj_digest, counts_json, health_json, state_json, source)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s,
             %s, %s, %s, %s, %s, %s)
            """,
            (
                int(file_id),
                ts,
                ok,
                str(acad_version or ""),
                str(dwg_path_used or ""),
                None if readonly is None else int(readonly),
                None if saved is None else int(saved),
                None if recovery_guess is None else int(recovery_guess),
                None if total_seen is None else int(total_seen),
                str(obj_digest or ""),
                _safe_json(counts_json),
                _safe_json(health_json),
                _safe_json(state_json),
                "computed",
            )
        )
        db.commit()
        return int(cur.lastrowid)
    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass
        sys_logger.error("❌ persist_cad_state 失败: %s", e)
        return None
    finally:
        cur.close()
        db.close()


def load_latest_state_from_db(identifier: str) -> dict | None:
    ensure_cad_audit_schema()
    info = _parse_identifier(identifier)

    candidates = []
    if info["raw_norm"]:
        candidates.append(("file_key", _sha1_text(info["raw_norm"])))
    if info["base"]:
        candidates.append(("basename_norm", info["base"]))
    if info["stem"]:
        candidates.append(("stem", info["stem"]))

    db = connect_to_db(CAD_AUDIT_DB)
    db = ensure_connection_alive(db, CAD_AUDIT_DB)
    cur = db.cursor()

    try:
        file_id = None
        for field, val in candidates:
            if not val:
                continue
            cur.execute(f"SELECT id FROM dwg_files WHERE {field}=%s ORDER BY updated_at DESC LIMIT 1", (val,))
            row = cur.fetchone()
            if row:
                file_id = int(row[0])
                break

        if file_id is None and info["is_path"] and info["raw_norm"]:
            cur.execute("SELECT id FROM dwg_files WHERE fullname_norm=%s ORDER BY updated_at DESC LIMIT 1", (info["raw_norm"],))
            row = cur.fetchone()
            if row:
                file_id = int(row[0])

        if file_id is None:
            return None

        cur.execute(
            """
            SELECT state_json
            FROM cad_snapshots
            WHERE file_id=%s
            ORDER BY ts DESC, id DESC
            LIMIT 1
            """,
            (file_id,)
        )
        row = cur.fetchone()
        if not row:
            return None

        state = json.loads(row[0]) if row[0] else None
        if isinstance(state, dict):
            state["source"] = "db"
        return state

    except Exception as e:
        sys_logger.error("❌ load_latest_state_from_db 失败: %s", e)
        return None
    finally:
        cur.close()
        db.close()

# =========================
# CAD采集：健康检查（保持你之前逻辑）
# =========================

def _check_doc_health(doc) -> dict:
    errors = []

    def t(name, fn):
        try:
            return fn()
        except Exception as e:
            errors.append(f"{name}: {e}")
            return None

    name = t("doc.Name", lambda: doc.Name) or ""
    fullname = t("doc.FullName", lambda: doc.FullName) or ""

    readonly = t("doc.ReadOnly", lambda: bool(doc.ReadOnly))
    saved = t("doc.Saved", lambda: bool(doc.Saved))

    ms_count = t("doc.ModelSpace.Count", lambda: int(doc.ModelSpace.Count))
    ps_count = t("doc.PaperSpace.Count", lambda: int(doc.PaperSpace.Count))

    recovery_guess = 0
    if not fullname:
        recovery_guess = 1
    if name.lower().startswith("drawing") and not fullname:
        recovery_guess = 1

    ok = (len(errors) == 0)

    return {
        "ok": ok,
        "errors": errors,
        "recovery_guess": int(recovery_guess),
        "readonly": int(bool(readonly)) if readonly is not None else None,
        "saved": int(bool(saved)) if saved is not None else None,
        "modelspace_count": ms_count,
        "paperspace_count": ps_count,
    }

# =========================
# ✅ 核心：对象类型 + Handle + 数量 + digest（稳健枚举版）
# =========================
def _snapshot_obj_counts_handles_and_digest(
    doc,
    *,
    max_entities: int = 300000,
    handle_types: list[str] | set[str] | None = None,
    max_handles_per_type: int | None = None,
    progress_every: int = 5000,
) -> tuple[dict, dict, dict, str, int, dict]:
    """
    ✅ 扫描 ModelSpace + 每个布局(Layout)的 paperspace(Block)
    ✅ 输出三种统计：
      - counts_legacy: 扁平键（兼容旧逻辑）
          "Model:AcDbLine": 123
          "Layout:布局1:AcDbViewport": 2
      - counts_by_type: 全图汇总（不分空间）
          {"AcDbLine": 123, "AcDbViewport": 3, ...}
      - counts_by_space: 按空间聚合（你现在真正想要的）
          {
            "Model": {"AcDbLine": 2, ...},
            "Layout:布局1": {"AcDbViewport": 2, ...},
            ...
          }

    ✅ handles_by_type：仅对 handle_types 指定类型采 Handle（可截断）
    ✅ digest：基于 token(空间+类型+[handle])，稳定用于对比

    返回（注意：比你旧版本多了 counts_by_space）：
      counts_legacy, counts_by_type, counts_by_space, obj_digest, total_seen, handles_by_type
    """
    counts_legacy: dict[str, int] = {}
    counts_by_type: dict[str, int] = {}
    counts_by_space: dict[str, dict[str, int]] = {}
    handles_by_type = defaultdict(list)

    handle_set: set[str] = set()
    if handle_types:
        handle_set = {str(x).strip() for x in handle_types if str(x).strip()}

    tokens: list[str] = []
    total = 0
    truncated = False

    def inc_flat(d: dict[str, int], k: str):
        d[k] = d.get(k, 0) + 1

    def inc_space(space: str, objtype: str):
        if space not in counts_by_space:
            counts_by_space[space] = {}
        counts_by_space[space][objtype] = counts_by_space[space].get(objtype, 0) + 1

    def inc_type(objtype: str):
        counts_by_type[objtype] = counts_by_type.get(objtype, 0) + 1

    def _get_objname(ent) -> str:
        try:
            v = get_attr(ent, "ObjectName") or getattr(ent, "ObjectName", None)
        except Exception:
            v = None
        return str(v) if v else "Unknown"

    def _get_handle(ent) -> str:
        try:
            v = get_attr(ent, "Handle") or getattr(ent, "Handle", None)
        except Exception:
            v = None
        return str(v) if v else ""

    def enum_container(space_label: str, container_obj):
        """
        space_label: "Model" 或 "Layout:布局1"
        container_obj: doc.ModelSpace 或 layout.Block
        """
        nonlocal total, truncated

        try:
            cnt = int(getattr(container_obj, "Count", 0) or 0)
            sys_logger.info("🔎 %s.Count = %s", space_label, cnt)
        except Exception as e:
            inc_flat(counts_legacy, f"{space_label}:ENUM_ERROR")
            sys_logger.error("❌ 读取 %s.Count 失败: %s", space_label, e)
            return

        for i in range(cnt):
            total += 1
            if total > max_entities:
                inc_flat(counts_legacy, f"{space_label}:TRUNCATED")
                sys_logger.warning("⚠️ 达到 max_entities=%s，%s 截断 (i=%s/%s)", max_entities, space_label, i, cnt)
                truncated = True
                return

            if progress_every and progress_every > 0 and i > 0 and (i % progress_every == 0):
                sys_logger.info("… %s scanning i=%s/%s (total=%s)", space_label, i, cnt, total)

            try:
                ent = container_obj.Item(i)
            except Exception as e:
                inc_flat(counts_legacy, f"{space_label}:ITEM_ERROR")
                sys_logger.error("❌ %s.Item(%s) 失败: %s", space_label, i, e)
                continue

            objname = _get_objname(ent)

            # ✅ 三套计数同时更新
            inc_flat(counts_legacy, f"{space_label}:{objname}")
            inc_type(objname)
            inc_space(space_label, objname)

            # ✅ digest token（空间+类型；如采handle则加入handle）
            if handle_set and (objname in handle_set):
                h = _get_handle(ent)
                if h:
                    if (max_handles_per_type is None) or (len(handles_by_type[objname]) < max_handles_per_type):
                        handles_by_type[objname].append(h)
                    tokens.append(f"{space_label}:{objname}:{h}")
                else:
                    tokens.append(f"{space_label}:{objname}:")
            else:
                tokens.append(f"{space_label}:{objname}")

    # 1) ModelSpace
    enum_container("Model", doc.ModelSpace)

    # 2) 每个布局的 Block（paperspace）
    if not truncated:
        try:
            layouts = doc.Layouts
            layout_cnt = int(getattr(layouts, "Count", 0) or 0)
            sys_logger.info("📐 Layouts.Count = %s", layout_cnt)
        except Exception as e:
            inc_flat(counts_legacy, "Layouts:ENUM_ERROR")
            sys_logger.error("❌ 读取 Layouts.Count 失败: %s", e)
            layouts = None
            layout_cnt = 0

        if layouts and layout_cnt > 0:
            for li in range(layout_cnt):
                if truncated:
                    break
                try:
                    lay = layouts.Item(li)
                except Exception as e:
                    inc_flat(counts_legacy, "Layouts:ITEM_ERROR")
                    sys_logger.error("❌ Layouts.Item(%s) 失败: %s", li, e)
                    continue

                try:
                    lay_name = str(getattr(lay, "Name", "") or "")
                except Exception:
                    lay_name = ""

                # doc.Layouts 会包含 "Model"，跳过
                if lay_name.lower() == "model" or lay_name == "Model":
                    continue

                try:
                    blk = getattr(lay, "Block", None)
                except Exception:
                    blk = None

                if blk is None:
                    inc_flat(counts_legacy, f"Layout:{lay_name}:NO_BLOCK")
                    continue

                enum_container(f"Layout:{lay_name}", blk)

    # 排序以稳定 digest、输出
    tokens.sort()
    digest = _sha1_text("\n".join(tokens))

    handles_sorted = {k: sorted(v) for k, v in handles_by_type.items()}

    # counts_by_space 内部排序（可读）
    counts_by_space_sorted: dict[str, dict[str, int]] = {}
    for space, mp in counts_by_space.items():
        counts_by_space_sorted[space] = dict(sorted(mp.items(), key=lambda x: x[0]))
    counts_by_space = dict(sorted(counts_by_space_sorted.items(), key=lambda x: x[0]))

    sys_logger.info(
        "📌 扫描完成 total=%s types=%s spaces=%s truncated=%s handle_types=%s",
        total, len(counts_by_type), len(counts_by_space), int(truncated), len(handle_set)
    )

    return counts_legacy, counts_by_type, counts_by_space, digest, total, handles_sorted

# =========================
# ✅ 对外唯一入口（保持你的接口）
# =========================

def get_cad_state(
    filepath: str | None = None,
    *,
    reuse_db: bool = False,
    max_entities: int = 300000,
    handle_types: list[str] | set[str] | None = None,
    max_handles_per_type: int | None = None,
    progress_every: int = 5000,
) -> dict:
    """
    ✅ 默认：重算 + 写入数据库（避免混乱）
    ✅ reuse_db=True：优先从数据库取（找不到则重算并写入）

    filepath:
    - None：当前激活DWG
    - 指定路径：按要求 open_file -> C.li -> 采集 -> close_file(auto_save)

    采集策略：
    - 永远扫描所有对象，得到 counts_by_type（全量类型计数）
    - ✅ Model + 每个 Layout 的 Block（paperspace），得到 counts_by_space（按空间聚合）
    - 仅对 handle_types 指定的类型采集 Handle（Handle 很慢，所以可选）

    timing：
    - state["timing"] = {total_sec, enum_sec, db_sec, obj_per_sec}
    """
    # -------------------------
    # 0) 复用模式：先查库
    # -------------------------
    if reuse_db:
        ident = None
        if filepath:
            ident = filepath
        else:
            # 当前激活：尽力取 doc.FullName / doc.Name
            if C.li():
                d = C.raw_doc
                ident = _try(lambda: d.FullName, "") or _try(lambda: d.Name, "")
        if ident:
            st = load_latest_state_from_db(ident)
            if isinstance(st, dict):
                return st
        # 查不到就继续重算

    errors = []
    opened_by_me = False

    # 总计时
    t0 = time.perf_counter()

    try:
        # -------------------------
        # 1) 如指定 filepath，则由我打开
        # -------------------------
        if filepath:
            sys_logger.info("📂 打开DWG: %s", filepath)
            res = _try(lambda: CAD_core.open_file(filepath), default=False)
            if not res:
                return {
                    "ok": False,
                    "ts": _now_str(),
                    "filepath_param": filepath,
                    "source": "computed",
                    "errors": [f"CAD_core.open_file('{filepath}') 失败"],
                }
            opened_by_me = True

        # -------------------------
        # 2) 连接/刷新 CAD 文档
        # -------------------------
        if not C.li():
            return {
                "ok": False,
                "ts": _now_str(),
                "filepath_param": filepath,
                "source": "computed",
                "errors": ["C.li() 失败：无法连接/刷新CAD文档"],
            }

        doc = C.raw_doc
        acad = C.acad

        dwg_name = _try(lambda: doc.Name, "")
        dwg_fullname = _try(lambda: doc.FullName, "")
        dwg_path = dwg_fullname or dwg_name or ""

        sys_logger.info("📄 当前DWG: name=%s fullname=%s", dwg_name, dwg_fullname)

        # -------------------------
        # 3) 健康检查
        # -------------------------
        health = _check_doc_health(doc)

        acad_version = _try(lambda: str(getattr(acad, "Version", "") or ""), "")
        acad_visible = _try(lambda: int(bool(getattr(acad, "Visible", False))), None)

        # -------------------------
        # 4) 扫描对象（计时）
        # -------------------------
        t_enum0 = time.perf_counter()

        # ✅ 注意：此函数现在返回 6 个值（新增 counts_by_space）
        counts_legacy, counts_by_type, counts_by_space, obj_digest, total_seen, handles_by_type = \
            _snapshot_obj_counts_handles_and_digest(
                doc,
                max_entities=max_entities,
                handle_types=handle_types,                 # ✅ 关键：按需采 handle
                max_handles_per_type=max_handles_per_type,
                progress_every=progress_every,
            )

        t_enum1 = time.perf_counter()

        # -------------------------
        # 5) 组装 state
        # -------------------------
        state = {
            "ok": True if health.get("ok", True) else False,
            "ts": _now_str(),
            "filepath_param": filepath,
            "source": "computed",
            "dwg": {
                "name": dwg_name,
                "fullname": dwg_fullname,
                "path_used": dwg_path,
                "readonly": health.get("readonly"),
                "saved": health.get("saved"),
                "recovery_guess": health.get("recovery_guess"),
            },
            "acad": {
                "version": acad_version,
                "visible": acad_visible,
            },
            "health": health,
            "objects": {
                "total_seen": total_seen,

                # ✅ 兼容旧字段：扁平键（空间:类型）
                "counts": counts_legacy,

                "obj_digest": obj_digest,

                # ✅ 全图聚合：类型计数
                "counts_by_type": counts_by_type,

                # ✅ 新增：按空间聚合（Model / Layout:xxx）
                "counts_by_space": counts_by_space,

                # ✅ 按需 handle
                "handles_by_type": handles_by_type,

                "limits": {
                    "max_entities": max_entities,
                    "handle_types": sorted(list(handle_types)) if handle_types else [],
                    "max_handles_per_type": max_handles_per_type,
                    "progress_every": progress_every,
                },
            },
            "errors": errors + health.get("errors", []),
        }

        # -------------------------
        # 6) 写库（计时）
        # -------------------------
        t_db0 = time.perf_counter()
        snapshot_id = persist_cad_state(state)
        t_db1 = time.perf_counter()

        state["snapshot_id"] = snapshot_id

        # -------------------------
        # 7) timing（总计时）
        # -------------------------
        t1 = time.perf_counter()
        enum_sec = (t_enum1 - t_enum0)
        total_sec = (t1 - t0)
        db_sec = (t_db1 - t_db0)

        state["timing"] = {
            "total_sec": round(total_sec, 3),
            "enum_sec": round(enum_sec, 3),
            "db_sec": round(db_sec, 3),
            "obj_per_sec": round((total_seen / max(enum_sec, 1e-9)), 1),
        }

        sys_logger.info(
            "⏱ timing total=%.3fs enum=%.3fs db=%.3fs speed=%.1f obj/s (handle_types=%s) spaces=%s types=%s",
            state["timing"]["total_sec"],
            state["timing"]["enum_sec"],
            state["timing"]["db_sec"],
            state["timing"]["obj_per_sec"],
            len(handle_types) if handle_types else 0,
            len(counts_by_space) if isinstance(counts_by_space, dict) else 0,
            len(counts_by_type) if isinstance(counts_by_type, dict) else 0,
        )

        return state

    except Exception as e:
        sys_logger.error("❌ get_cad_state 异常: %s", e)
        return {
            "ok": False,
            "ts": _now_str(),
            "filepath_param": filepath,
            "source": "computed",
            "errors": [f"get_cad_state 异常: {e}"],
        }

    finally:
        # -------------------------
        # 8) 如果是我打开的文件，则我负责关闭
        # -------------------------
        if opened_by_me:
            sys_logger.info("📁 关闭DWG (auto_save)")
            _try(lambda: CAD_core.close_file(save_option="auto_save"), default=None)


def get_cad_state_from_db(identifier: str) -> dict:
    st = load_latest_state_from_db(identifier)
    if st is None:
        return {
            "ok": False,
            "ts": _now_str(),
            "source": "db",
            "errors": [f"数据库未找到该文件的快照：{identifier}"],
        }
    return st

#&&&% 获取dwg文件内容信息
@timeit
def get_dwg_graphics_summary(
    filepath: str | None = None,
    *,
    types: list[str] | set[str] | None = None,
    handle_types: list[str] | set[str] | None = None,
    use_db: bool = False,
    max_handles_per_type: int | None = None,
    verbose: bool = True,
) -> dict:
    """
    便捷 API：获取 DWG 图形统计信息（程序可用 dict + 人类可读输出）

    返回新增：
      - counts_legacy   : 扁平键（兼容）
      - counts_by_space : ✅按空间聚合（Model / Layout:xxx）

    其他字段保持不变：
      ok, ts, source, dwg, total, types, counts_by_type, handles_by_type, timing, errors
    """
    # -------------------------
    # 0) 规范 types / handle_types
    # -------------------------
    type_set = None
    if types:
        type_set = {str(t).strip() for t in types if str(t).strip()}

    handle_type_set = None
    if handle_types:
        handle_type_set = {str(t).strip() for t in handle_types if str(t).strip()}

    def _clip_handles(lst):
        if not lst:
            return []
        if max_handles_per_type is None:
            return list(lst)
        try:
            n = int(max_handles_per_type)
            if n <= 0:
                return []
            return list(lst)[:n]
        except Exception:
            return list(lst)

    # -------------------------
    # 1) 取得 state（db 或 computed）
    # -------------------------
    if use_db:
        ident = filepath
        if ident is None:
            if C.li():
                d = C.raw_doc
                ident = _try(lambda: d.FullName, "") or _try(lambda: d.Name, "")

        if not ident:
            return {
                "ok": False,
                "ts": _now_str(),
                "source": "db",
                "errors": ["无法确定 DWG 标识符（filepath / 当前文档均不可用）"],
            }

        state = load_latest_state_from_db(ident)
        if not state:
            return {
                "ok": False,
                "ts": _now_str(),
                "source": "db",
                "errors": [f"数据库未找到该 DWG 的快照: {ident}"],
            }
    else:
        state = get_cad_state(
            filepath=filepath,
            reuse_db=False,
            handle_types=handle_type_set,
            max_handles_per_type=max_handles_per_type,
        )

    if not isinstance(state, dict) or not state.get("ok", False):
        return state if isinstance(state, dict) else {
            "ok": False,
            "ts": _now_str(),
            "source": "unknown",
            "errors": ["state 不是 dict 或 state.ok=False"],
        }

    # -------------------------
    # 2) 抽取对象统计
    # -------------------------
    objs = state.get("objects", {}) or {}

    counts_all = objs.get("counts_by_type", {}) or {}
    handles_all = objs.get("handles_by_type", {}) or {}
    counts_legacy_all = objs.get("counts", {}) or {}

    # ✅ 新增：优先使用源头提供的 counts_by_space；没有则从 counts_legacy 推导（兼容旧快照）
    counts_by_space_all = objs.get("counts_by_space")

    def _group_counts_legacy_by_space(counts_legacy: dict) -> dict:
        out: dict[str, dict[str, int]] = {}
        for k, v in (counts_legacy or {}).items():
            try:
                v_int = int(v)
            except Exception:
                continue

            k_str = str(k)

            if k_str.endswith(":ENUM_ERROR") or k_str.endswith(":ITEM_ERROR") or k_str.endswith(":TRUNCATED"):
                continue

            if k_str.startswith("Model:"):
                parts = k_str.split(":", 1)
                if len(parts) != 2:
                    continue
                space = "Model"
                objtype = parts[1]
            elif k_str.startswith("Layout:"):
                parts = k_str.split(":", 2)
                if len(parts) != 3:
                    continue
                space = f"Layout:{parts[1]}"
                objtype = parts[2]
            else:
                continue

            if not objtype:
                continue

            if space not in out:
                out[space] = {}
            out[space][objtype] = out[space].get(objtype, 0) + v_int

        out_sorted = {}
        for space, mp in out.items():
            out_sorted[space] = dict(sorted(mp.items(), key=lambda x: x[0]))
        return dict(sorted(out_sorted.items(), key=lambda x: x[0]))

    if isinstance(counts_by_space_all, dict):
        counts_by_space_all = counts_by_space_all
    else:
        counts_by_space_all = _group_counts_legacy_by_space(counts_legacy_all)

    # -------------------------
    # 3) types 过滤（只过滤 counts_by_type/handles；counts_by_space 保持全量更利于人工核验）
    # -------------------------
    if type_set is not None:
        counts = {k: v for k, v in counts_all.items() if k in type_set}
        handles = {k: _clip_handles(handles_all.get(k, [])) for k in type_set if k in counts_all}
    else:
        counts = dict(counts_all)
        handles = {k: _clip_handles(v) for k, v in handles_all.items()}

    total = sum(int(v) for v in counts.values()) if counts else 0

    # -------------------------
    # 4) 返回
    # -------------------------
    result = {
        "ok": True,
        "ts": state.get("ts"),
        "source": state.get("source", "computed"),
        "dwg": state.get("dwg", {}),
        "total": total,
        "types": sorted(counts.keys()),
        "counts_by_type": counts,
        "handles_by_type": handles,
        "counts_legacy": counts_legacy_all,          # ✅ 兼容保留
        "counts_by_space": counts_by_space_all,      # ✅ 你需要的聚合结构
        "timing": state.get("timing"),
        "errors": state.get("errors", []),
    }

    # -------------------------
    # 5) 可读输出
    # -------------------------
    if verbose:
        try:
            print("\n" + "=" * 88)
            print("📊 DWG GRAPHICS SUMMARY")
            print("=" * 88)
            print(f"OK        : {result.get('ok')}")
            print(f"SOURCE    : {result.get('source')}")
            print(f"TIMESTAMP : {result.get('ts')}")

            dwg = result.get("dwg", {}) or {}
            print("-" * 88)
            print(f"DWG NAME  : {dwg.get('name')}")
            print(f"FULL PATH : {dwg.get('fullname')}")

            print("-" * 88)
            print(f"TOTAL OBJECTS (filtered by types) : {result.get('total')}")
            print(f"TYPE COUNT (filtered)            : {len(result.get('types', []))}")

            print("\n🔢 TOP OBJECT TYPES (by count, filtered)")
            print("-" * 88)
            top_items = sorted(
                (result.get("counts_by_type", {}) or {}).items(),
                key=lambda x: int(x[1]),
                reverse=True
            )
            show_top = 15
            max_name_len = max((len(str(k)) for k, _ in top_items[:show_top]), default=20)
            for k, v in top_items[:show_top]:
                print(f"{str(k).ljust(max_name_len)} : {v}")

            # ✅ counts_by_space：最关键的人工核验输出
            cbs = result.get("counts_by_space", {}) or {}
            if cbs:
                print("\n🧱 COUNTS BY SPACE (unfiltered, best for manual verification)")
                print("-" * 88)
                for space, mp in cbs.items():
                    subtotal = sum(int(x) for x in mp.values())
                    print(f"[{space}]  total={subtotal}  types={len(mp)}")
                    items = sorted(mp.items(), key=lambda x: int(x[1]), reverse=True)
                    for k, v in items[:20]:
                        print(f"  {k} : {v}")
                    if len(items) > 20:
                        print(f"  ... ({len(items) - 20} more types)")

            print("\n🔎 HANDLE PREVIEW")
            print("-" * 88)
            preview_types = list(type_set) if type_set else [k for k, _ in top_items[:3]]
            handles_map = result.get("handles_by_type", {}) or {}
            for t in preview_types:
                hs = handles_map.get(t, [])
                if not hs:
                    continue
                print(f"{t}  ({len(hs)} handles kept)")
                print("  ", hs[:10])

            timing = result.get("timing")
            if timing:
                print("\n⏱️ TIMING")
                print("-" * 88)
                for k, v in (timing or {}).items():
                    print(f"{str(k).ljust(20)} : {v}")

            if max_handles_per_type is not None:
                print("\n📝 NOTE")
                print("-" * 88)
                print(f"max_handles_per_type = {max_handles_per_type} (only affects handles_by_type output)")

            if handle_type_set:
                print("\n🧩 HANDLE TYPES")
                print("-" * 88)
                print(sorted(handle_type_set))

            print("\n" + "=" * 88 + "\n")

        except Exception as e:
            try:
                sys_logger.warning(f"[WARN] get_dwg_graphics_summary summary print failed: {e}")
            except Exception:
                print(f"[WARN] summary print failed: {e}")

    return result


##调用示例（非常清晰）
##✅ 默认：重新计算（最安全）
##ret = get_dwg_graphics_summary()
##
##🚀 从数据库读取（极快）
##ret = get_dwg_graphics_summary(use_db=True)
##
##🎯 只关心某几种类型（不管 db / computed）
##ret = get_dwg_graphics_summary(
##    use_db=True,
##    types=["AcDbBlockReference", "AcDbLine"],
##    max_handles_per_type=100,
##)
##
##📂 指定文件 + 强制重新算
##ret = get_dwg_graphics_summary(
##    filepath=r"D:\xxx\yyy.dwg",
##    use_db=False
##)
















