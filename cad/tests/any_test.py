#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# D:/codex-tasks/cad/tests/any_test.py
#
# 一次跑完全部函数 + 10/20/50 运行中即时 DB 验证（不截断）

import os
import sys
from pathlib import Path
import time

# -------------------------
# 1) 确保 cad 根目录在 sys.path
# -------------------------
current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise RuntimeError("找不到 cad 根目录")
    current = current.parent

if str(current) not in sys.path:
    sys.path.insert(0, str(current))

print(f"[TEST] cad root = {current}")

# -------------------------
# 2) 固定日志节奏（必须最早）
# -------------------------
from system.common_logger import set_debug_mode
set_debug_mode(mode=1, who="AI", wait_time=0)

# -------------------------
# 3) 工程环境
# -------------------------
from system.core_tools import *  # noqa
set_debug_mode(mode=1, who="AI", wait_time=0)

# -------------------------
# 4) 函数分析器
# -------------------------
import tools.function_analyzer as fa
import importlib
importlib.reload(fa)

# -------------------------
# 5) 配置
# -------------------------
api_key = os.environ.get("CODEX_API_KEY")
if not api_key:
    raise RuntimeError("CODEX_API_KEY not found")

target_file = r"D:/codex-tasks/cad/scripts/CAD_basic.py"

TIMEOUT = 60
MAX_STREAM_SECONDS = 120
FORCE = False
PRINT_EACH_SUMMARY = False

# -------------------------
# 6) 获取函数列表（用于第 N 个定位）
# -------------------------
defs = fa.list_top_level_function_defs_in_file(target_file)
total = len(defs)
print(f"[TEST] total top-level functions = {total}")

CHECKPOINTS = {10, 20, 50}
checked = set()

# =============================================================================
# 工具：打印第 N 个函数的 DB 结果
# =============================================================================
def print_db_analysis_for_nth(n: int):
    d = defs[n - 1]
    fn = d["name"]
    line = int(d.get("lineno") or 0)

    src_info = fa.extract_function_source(target_file, line)
    if not src_info.get("ok"):
        print(f"[CHECK {n}] ❌ extract source failed")
        return

    qn = fa.build_qualified_name(target_file, fn)

    hit = fa.load_function_analysis_from_db(
        qualified_name=qn,
        func_source=src_info["source"],
        database=fa.FUNC_DB_NAME,
        table=fa.FUNC_TABLE_NAME,
    )

    print("\n" + "#" * 96)
    print(f"CHECKPOINT VERIFY: #{n}")
    print("#" * 96)
    print(f"[FUNC] {fn}")
    print(f"[FILE] {target_file}")
    print(f"[DEF ] start={src_info.get('start_line')} end={src_info.get('end_line')}")

    if not hit.get("ok"):
        print(f"[DB ] READ FAILED: {hit.get('error')}")
        return

    if not hit.get("hit"):
        print("[DB ] MISS ❌（未命中数据库，可能写库失败或未完成）")
        return

    rec = hit["record"]
    print(f"[DB ] HIT ✅  id={rec.get('id')}  updated_at={rec.get('updated_at')}")
    print(f"[DB ] source_hash={rec.get('source_hash')}")
    print(f"[DB ] file_path_in_db={rec.get('file_path')}")

    analysis = rec.get("analysis") or {}
    if isinstance(analysis, dict):
        fa.print_human_flow_summary(func_name=fn, analysis=analysis)

# =============================================================================
# 7) Hook：包装 analyze_function_flow_cached 以统计完成数
# =============================================================================
_original_cached = fa.analyze_function_flow_cached
completed_count = 0

def _hooked_analyze_function_flow_cached(*args, **kwargs):
    global completed_count
    ret = _original_cached(*args, **kwargs)

    # 只在成功或失败“结束一次函数分析”后计数
    completed_count += 1

    if completed_count in CHECKPOINTS and completed_count not in checked:
        checked.add(completed_count)
        print_db_analysis_for_nth(completed_count)

    return ret

fa.analyze_function_flow_cached = _hooked_analyze_function_flow_cached

# =============================================================================
# 8) 一次性跑完整个脚本（不设 stop_after）
# =============================================================================
print("\n" + "=" * 96)
print("START FULL BATCH (NO ARTIFICIAL STOP)")
print("=" * 96)

ret = fa.analyze_all_top_level_functions_in_file_with_dbop_cache(
    file_path=target_file,
    base_url="https://code.newcli.com/codex/v1",
    api_key=api_key,
    model="gpt-5.2-codex",
    timeout=TIMEOUT,
    max_stream_seconds=MAX_STREAM_SECONDS,
    force=FORCE,
    print_each_summary=PRINT_EACH_SUMMARY,
    include_calls=True,
    max_retries=5,
    retry_sleep=2.0,
)

print("\n" + "=" * 96)
print("FULL BATCH DONE")
print("=" * 96)
print("ok        =", ret.get("ok"))
print("processed =", ret.get("processed"))
print("reused    =", ret.get("reused"))
print("analyzed  =", ret.get("analyzed"))
print("failed    =", ret.get("failed"))
print("=" * 96)
