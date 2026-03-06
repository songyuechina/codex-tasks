#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# D:/codex-tasks/cad/tools/function_name_cleaner.py

"""
功能：
1) 扫描单个 .py 文件内的“同名重复函数定义”
2) 默认策略：删除前面的，保留后面的（keep last），符合 Python 实际覆盖语义
3) 同步 DB：对被删除的那段源码，按 (qualified_name, source_hash) 精确软删除（ok=0 + error_text）
   - 可切换 hard delete：直接 DELETE
4) 支持 dry_run：先打印会删什么、会更新 DB 什么

依赖：
- tools.function_analyzer.py（复用：extract_function_source/build_qualified_name/_sha256_text/ensure_function_db_and_table）
- library.Databaseoperation.py（复用：execute_sql / connect_to_db）
"""

from __future__ import annotations

import ast
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ---------------------------------------------------------------------
# 0) 定位 cad 根目录，并加入 sys.path（与你项目保持一致）
# ---------------------------------------------------------------------
_current = Path(__file__).resolve()
while _current.name != "cad":
    if _current.parent == _current:
        raise RuntimeError("找不到 cad 根目录")
    _current = _current.parent
CAD_ROOT = _current
if str(CAD_ROOT) not in sys.path:
    sys.path.insert(0, str(CAD_ROOT))

# 复用你已有的工具函数
from tools import function_analyzer as fa
from library import Databaseoperation as dbop


# ---------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------
@dataclass
class FuncDefRef:
    name: str
    lineno: int  # def 行（1-based, ast 给的）
    kind: str    # "def" / "async def"


@dataclass
class RemovePlanItem:
    func_name: str
    def_line: int
    start_line: int
    end_line: int
    source: str
    qualified_name: str
    source_hash: str


# ---------------------------------------------------------------------
# 1) 扫描：文件内所有函数定义（包含 async def）
# ---------------------------------------------------------------------
def list_function_defs_in_file(file_path: str | Path) -> List[FuncDefRef]:
    p = Path(file_path)
    if not p.exists():
        return []

    try:
        src = p.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(src, filename=str(p))
    except Exception:
        return []

    out: List[FuncDefRef] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            out.append(FuncDefRef(name=node.name, lineno=int(node.lineno), kind="def"))
        elif isinstance(node, ast.AsyncFunctionDef):
            out.append(FuncDefRef(name=node.name, lineno=int(node.lineno), kind="async def"))

    out.sort(key=lambda x: (x.lineno, x.name))
    return out


def find_duplicate_defs(defs: List[FuncDefRef]) -> Dict[str, List[FuncDefRef]]:
    by_name: Dict[str, List[FuncDefRef]] = {}
    for d in defs:
        by_name.setdefault(d.name, []).append(d)

    dups = {k: v for k, v in by_name.items() if len(v) >= 2}
    # 每个名字按行号排序（前 -> 后）
    for k in dups:
        dups[k].sort(key=lambda x: x.lineno)
    return dups


# ---------------------------------------------------------------------
# 2) 生成删除计划：保留最后一个，删除前面的
# ---------------------------------------------------------------------
def build_remove_plan(
    file_path: str | Path,
    *,
    database: str = fa.FUNC_DB_NAME,
    table: str = fa.FUNC_TABLE_NAME,
) -> Dict[str, List[RemovePlanItem]]:
    p = Path(file_path)
    defs = list_function_defs_in_file(p)
    dups = find_duplicate_defs(defs)

    # 确保 DB/表存在（保证后续可 update）
    fa.ensure_function_db_and_table(database=database, table=table)

    plan: Dict[str, List[RemovePlanItem]] = {}

    for func_name, items in dups.items():
        # keep last：保留最后一个 def，删掉前面的
        to_remove = items[:-1]  # 前面那些
        if not to_remove:
            continue

        for d in to_remove:
            src_info = fa.extract_function_source(p, d.lineno)
            if not src_info.get("ok"):
                # 提取失败就跳过（不做危险删除）
                continue

            source = src_info["source"]
            start_line = int(src_info["start_line"])
            end_line = int(src_info["end_line"])

            qn = fa.build_qualified_name(str(p), func_name)
            sh = fa._sha256_text(source)

            plan.setdefault(func_name, []).append(
                RemovePlanItem(
                    func_name=func_name,
                    def_line=d.lineno,
                    start_line=start_line,
                    end_line=end_line,
                    source=source,
                    qualified_name=qn,
                    source_hash=sh,
                )
            )

        # 对同名函数的多个删除块：按 start_line 倒序，避免删一块后行号漂移影响后续
        plan[func_name].sort(key=lambda x: x.start_line, reverse=True)

    return plan


# ---------------------------------------------------------------------
# 3) 文件删除：按 (start_line, end_line) 删除源码块
# ---------------------------------------------------------------------
def apply_remove_plan_to_file(file_path: str | Path, plan: Dict[str, List[RemovePlanItem]], *, backup: bool = True) -> Dict:
    p = Path(file_path)
    if not p.exists():
        return {"ok": False, "error": f"file not found: {p}", "removed": 0}

    text = p.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines(True)

    # 汇总所有要删块（跨函数），按 start_line 倒序删
    blocks: List[Tuple[int, int, str]] = []
    for _, items in plan.items():
        for it in items:
            blocks.append((it.start_line, it.end_line, it.func_name))
    blocks.sort(key=lambda x: x[0], reverse=True)

    if backup:
        bak = p.with_suffix(p.suffix + f".bak_{int(time.time())}")
        bak.write_text(text, encoding="utf-8")
        bak_path = str(bak)
    else:
        bak_path = None

    removed = 0
    for start_line, end_line, func_name in blocks:
        # start_line/end_line 是 1-based，Python list 是 0-based；end_line 是“截止行号”(extract 已经按切片 end 给)
        s = max(0, start_line - 1)
        e = max(0, end_line)
        if s >= len(lines):
            continue
        if e > len(lines):
            e = len(lines)
        if e <= s:
            continue

        del lines[s:e]
        removed += 1

    p.write_text("".join(lines), encoding="utf-8")
    return {"ok": True, "error": None, "removed": removed, "backup": bak_path}


# ---------------------------------------------------------------------
# 4) DB 同步：对被删除源码做软删/硬删
# ---------------------------------------------------------------------
def sync_remove_plan_to_db(
    plan: Dict[str, List[RemovePlanItem]],
    *,
    database: str = fa.FUNC_DB_NAME,
    table: str = fa.FUNC_TABLE_NAME,
    mode: str = "soft",  # "soft" | "hard"
    dry_run: bool = True,
) -> Dict:
    """
    mode="soft": UPDATE ok=0, error_text='duplicate_removed@...'
    mode="hard": DELETE row
    """
    fa.ensure_function_db_and_table(database=database, table=table)

    total_ops = 0
    affected = 0
    errors = []

    for _, items in plan.items():
        for it in items:
            total_ops += 1

            if mode == "hard":
                sql = f"DELETE FROM `{table}` WHERE qualified_name=%s AND source_hash=%s"
                params = (it.qualified_name, it.source_hash)
            else:
                sql = f"""
                    UPDATE `{table}`
                    SET ok=0,
                        error_text=CONCAT('duplicate_removed@', NOW()),
                        updated_at=NOW()
                    WHERE qualified_name=%s AND source_hash=%s
                """
                params = (it.qualified_name, it.source_hash)

            if dry_run:
                continue

            try:
                # 你 dbop.execute_sql 支持 fetch/dictionary；这里不 fetch
                ret = dbop.execute_sql(database, sql, params=params, fetch=False, dictionary=False)
                # execute_sql 的返回形式你项目里可能不统一：
                # - 有的实现返回 cursor.rowcount
                # - 有的返回 True/None
                # 所以这里用“尽量”的策略：若 ret 是 int 就累计，否则不强求
                if isinstance(ret, int):
                    affected += ret
            except Exception as e:
                errors.append({"qualified_name": it.qualified_name, "source_hash": it.source_hash, "error": str(e)})

    return {
        "ok": len(errors) == 0,
        "mode": mode,
        "dry_run": dry_run,
        "total_ops": total_ops,
        "affected_maybe": affected,
        "errors": errors[:10],
    }


# ---------------------------------------------------------------------
# 5) 统一入口：扫描 +（可选）删除文件 +（可选）同步 DB
# ---------------------------------------------------------------------
def clean_duplicate_defs_and_db(
    *,
    file_path: str | Path,
    apply: bool = False,       # True 才实际改文件/改DB
    db_mode: str = "soft",     # "soft" 推荐，"hard" 可选
    backup: bool = True,
    database: str = fa.FUNC_DB_NAME,
    table: str = fa.FUNC_TABLE_NAME,
) -> Dict:
    """
    apply=False: 只打印计划（dry-run）
    apply=True : 实际删除文件中“前面的重复 def”，并同步 DB（软删/硬删）
    """
    p = Path(file_path)
    plan = build_remove_plan(p, database=database, table=table)

    # 打印计划
    print("\n" + "=" * 96)
    print("🧹 Duplicate Function Def Cleaner (KEEP LAST = delete earlier defs)")
    print("=" * 96)
    print(f"File   : {p}")
    print(f"Apply  : {apply}")
    print(f"DBMode : {db_mode}")
    print(f"Backup : {backup}")
    print("-" * 96)

    total_funcs = 0
    total_blocks = 0
    for func_name, items in plan.items():
        total_funcs += 1
        total_blocks += len(items)
        kept = "last one"
        print(f"\nBase: {func_name}  (keep={kept}, remove={len(items)})")
        for it in items:
            print(f"  - remove def@L{it.def_line}  block[{it.start_line}-{it.end_line}]  qn={it.qualified_name}")

    if total_blocks == 0:
        print("\n✅ No duplicates found.\n")
        return {"ok": True, "duplicates": 0, "removed_blocks": 0, "db": None, "file": None}

    print("\n" + "-" * 96)
    print(f"Summary: duplicated_names={total_funcs}, remove_blocks={total_blocks}")
    print("-" * 96)

    if not apply:
        # dry run：不改文件不改 DB
        db_ret = sync_remove_plan_to_db(plan, database=database, table=table, mode=db_mode, dry_run=True)
        print("\n(DRY RUN) DB ops planned:", db_ret["total_ops"])
        print("\n✅ Dry-run done.\n")
        return {"ok": True, "duplicates": total_funcs, "removed_blocks": 0, "db": db_ret, "file": None}

    # 1) 改文件
    file_ret = apply_remove_plan_to_file(p, plan, backup=backup)
    if not file_ret.get("ok"):
        print("\n❌ File update failed:", file_ret.get("error"))
        return {"ok": False, "duplicates": total_funcs, "removed_blocks": 0, "db": None, "file": file_ret}

    # 2) 同步 DB（真正执行）
    db_ret = sync_remove_plan_to_db(plan, database=database, table=table, mode=db_mode, dry_run=False)
    if not db_ret.get("ok"):
        print("\n⚠️ DB sync has errors (file already cleaned). See result.errors.")
    else:
        print("\n✅ DB sync done.")

    print("\n✅ Clean done.\n")
    return {
        "ok": file_ret.get("ok") and db_ret.get("ok"),
        "duplicates": total_funcs,
        "removed_blocks": file_ret.get("removed", 0),
        "db": db_ret,
        "file": file_ret,
    }


# ---------------------------------------------------------------------
# 6) 你之前的调用方式兼容：run_similar_function_scan()
# ---------------------------------------------------------------------
def run_similar_function_scan(
    file_path: str | Path = None,
    *,
    apply: bool = False,
    db_mode: str = "soft",
    backup: bool = True,
):
    """
    兼容你的入口：
      from tools.function_name_cleaner import run_similar_function_scan
      run_similar_function_scan()

    默认：只扫描+打印（dry-run）
    传 apply=True 才会实际删除 + 同步 DB
    """
    if file_path is None:
        raise ValueError("Please pass file_path explicitly for now (avoid deleting wrong file).")

    return clean_duplicate_defs_and_db(
        file_path=file_path,
        apply=apply,
        db_mode=db_mode,
        backup=backup,
    )



#使用
"""

) 先 dry-run 看清单（不改任何东西）
from tools.function_name_cleaner import run_similar_function_scan
run_similar_function_scan(r"D:/codex-tasks/cad/scripts/CAD_basic.py")

2) 确认后执行（删除前面的定义，保留后面）
from tools.function_name_cleaner import run_similar_function_scan
run_similar_function_scan(r"D:/codex-tasks/cad/scripts/CAD_basic.py", apply=True, db_mode="hard")hard真删除soft只标记

"""


###只改相近名函数

import re
from pathlib import Path

from tools.function_analyzer import (
    list_top_level_function_defs_in_file,
)



_SIMILAR_TAIL_TOKEN_RE = re.compile(
    r"""^(?:
        \d+                 |   # 1 2 3
        v\d+                |   # v1 v2
        ver\d+              |   # ver2
        rev\d+              |   # rev3
        t\d+                |   # t7 t3
        tmp|temp|test       |
        old|new             |
        bak|backup|copy     |
        bifen|y             |
        [a-zA-Z]                # a b c (单字母)
    )$""",
    re.IGNORECASE | re.VERBOSE,
)





def _strip_known_tail_tokens(tokens: List[str]) -> List[str]:
    """剥离末尾明确的版本/测试 token（可重复剥离）"""
    t = list(tokens)
    while t and _SIMILAR_TAIL_TOKEN_RE.match(t[-1] or ""):
        t.pop()
    return t

def _choose_family_base(tokens: List[str], max_tokens: int = 4) -> str:
    """
    老版本“族名 base”选择策略（核心）：
    - 优先识别结构型前缀：*_by / *_from / *_with / *_to
    - 否则：按“动词 + 1~2 个名词”形成族名
    - 并限制最多 max_tokens，避免 base 太长
    """
    if not tokens:
        return ""

    # 结构型：select_print_areas_from_* / sort_coms_by_* / find_files_with_*
    # 规则：如果 tokens 里出现 by/from/with/to，优先把 base 截到该词为止（含该词）
    for kw in ("by", "from", "with", "to", "of"):
        if kw in tokens[:max_tokens+1]:
            idx = tokens.index(kw)
            # 至少保留到 kw（含），并且 base 最多 max_tokens
            cut = min(idx + 1, max_tokens)
            return "_".join(tokens[:cut])

    # 动词族：保留 1~2 token（老版本就是会出现 get/ensure/purge/draw 这种大族）
    verb_first = tokens[0].lower()

    # 这些动词常见：用更“粗”的族（只取 1 token）——对应你贴的 get / draw / purge / safe / same / normalize / process...
    coarse_verbs = {
        "get", "set", "draw", "purge", "safe", "same",
        "normalize", "process", "ensure", "load", "save",
        "find", "select", "delete", "insert", "create",
        "export", "import", "run", "open", "close",
        "maximize", "minimize", "update", "print", "main",
    }
    if verb_first in coarse_verbs:
        # 但如果第二个 token 明显是结构名（all/block/layout/window/...），允许扩展到 2~3 token
        if len(tokens) >= 3 and tokens[1].lower() in {"all", "layout", "block", "blocks", "dwg", "files", "window"}:
            return "_".join(tokens[:min(3, max_tokens)])
        if len(tokens) >= 2 and tokens[1].lower() in {"all", "block", "blocks"}:
            return "_".join(tokens[:min(2, max_tokens)])
        return tokens[0]

    # 默认：取前 2 token（避免 base 太散）
    if len(tokens) >= 2:
        return "_".join(tokens[:min(2, max_tokens)])
    return tokens[0]

def normalize_function_base_name(func_name: str) -> str:
    """
    老版本 base 归一：
    - 先 token 化
    - 去掉末尾明确的版本/测试 token（_1/_v2/_tmp/_test/_bak/_y/_bifen/...）
    - 再用“族名选择器”生成 base（会产生 get / ensure / sort_coms_by / select_*_from 这种）
    """
    fn = (func_name or "").strip()
    if not fn:
        return ""

    tokens = [t for t in fn.split("_") if t]
    tokens = _strip_known_tail_tokens(tokens)

    # 如果剥离后空了，退回原名（保底）
    if not tokens:
        tokens = [t for t in fn.split("_") if t]

    base = _choose_family_base(tokens, max_tokens=4)
    return base or fn


# =============================================================================
# 三 同源函数分组（老版本：族名聚类，不止 suffix）
# =============================================================================
def find_similar_named_functions_from_db(
    *,
    database="CAD_FUNCINFO",
    table="function_analysis",
    min_group_size=2,
) -> Dict[str, List[dict]]:
    rows = load_functions_from_db(database=database, table=table)

    groups: Dict[str, List[dict]] = {}
    for r in rows:
        fn = (r.get("func_name") or "").strip()
        if not fn:
            continue
        base = normalize_function_base_name(fn)
        groups.setdefault(base, []).append(r)

    # 只保留组内至少 2 个，并且确实存在不同 func_name（避免同名重复行导致假组）
    out: Dict[str, List[dict]] = {}
    for base, items in groups.items():
        names = {x.get("func_name") for x in items if x.get("func_name")}
        if len(names) >= int(min_group_size):
            # 稳定排序：按 func_name
            out[base] = sorted(items, key=lambda x: (x.get("func_name") or "", x.get("qualified_name") or ""))

    return out


# =============================================================================
# 五 删除建议生成（老版本风格：更像你贴的那种）
# =============================================================================
def build_delete_suggestions(groups: dict) -> dict:
    """
    老版本建议：
    - 优先建议删：*_test/*_tmp/*_bak/*_copy
    - 其次：*_1/*_2/...（数字后缀）
    - 其次：*_a/*_b（单字母）
    - 其次：*_y/*_bifen
    - 尽量保留“无尾缀的那个”（如果存在）
    """
    delete_map: Dict[str, List[str]] = {}

    def _score(fn: str) -> int:
        # 分越高越该删
        if re.search(r"_(test|tmp|temp|bak|backup|copy)$", fn, flags=re.I):
            return 100
        if re.search(r"_\d+$", fn):
            return 80
        if re.search(r"_[a-zA-Z]$", fn):
            return 60
        if re.search(r"_(y|bifen)$", fn, flags=re.I):
            return 50
        if re.search(r"_(v\d+|ver\d+|rev\d+)$", fn, flags=re.I):
            return 40
        return 0

    for base, items in groups.items():
        names = sorted({x.get("func_name") for x in items if x.get("func_name")})
        if len(names) < 2:
            continue

        # 如果存在“无尾缀原名”，尽量保留它
        # 这里用简单判定：去掉已知尾 token 后是否等于自己
        keep_candidates = []
        for fn in names:
            toks = [t for t in fn.split("_") if t]
            stripped = _strip_known_tail_tokens(toks)
            if "_".join(stripped) == fn:
                keep_candidates.append(fn)

        keep = keep_candidates[0] if keep_candidates else None

        # 建议删除：按 score 排序，score>0 的优先
        candidates = []
        for fn in names:
            if keep and fn == keep:
                continue
            s = _score(fn)
            if s > 0:
                candidates.append((s, fn))

        # 如果没有明显尾巴，但组很大（老版本也会给建议），就不强推删除
        if candidates:
            candidates.sort(key=lambda x: (-x[0], x[1]))
            delete_map[base] = [fn for _, fn in candidates]

    return delete_map



def _format_similar_report(
    groups: Dict[str, List[dict]],
    delete_map: Dict[str, List[str]],
    *,
    title: str = "🔍 Similar Function Name Report",
    suggestion_title: str = "🧹 Delete Suggestions (Manual Review Required)",
    max_bases: Optional[int] = None,
) -> None:
    """
    把相近函数 groups / delete_map 打印成你贴的报告格式
    """
    print("\n" + "=" * 96)
    print(title)
    print("=" * 96)

    # 稳定输出：按 base 排序；你也可以改成按组大小排序
    bases = sorted(groups.keys())
    if max_bases is not None:
        bases = bases[: int(max_bases)]

    for base in bases:
        items = groups.get(base) or []
        if not items:
            continue

        print(f"\n🧩 Base Function: {base}")
        print("-" * 72)

        # 计算对齐宽度：按 func_name 最大长度
        max_name_len = 0
        for r in items:
            fn = (r.get("func_name") or "").strip()
            if len(fn) > max_name_len:
                max_name_len = len(fn)
        max_name_len = max(max_name_len, 8)
        pad = min(max_name_len + 2, 42)  # 不让列太宽

        # items 已在 find_similar_named_functions_from_db 里排序过；这里再保险一次
        items_sorted = sorted(items, key=lambda x: ((x.get("func_name") or ""), (x.get("qualified_name") or "")))

        for r in items_sorted:
            fn = (r.get("func_name") or "").strip()
            qn = (r.get("qualified_name") or "").strip()
            # 输出两列：func_name + qualified_name
            print(f"  {fn:<{pad}} {qn}")

    print("\n" + "=" * 96)
    print("\n" + "=" * 96)
    print(suggestion_title)
    print("=" * 96)

    if not delete_map:
        print("\n✅ No delete suggestions.\n")
        return

    for base in sorted(delete_map.keys()):
        names = delete_map.get(base) or []
        if not names:
            continue
        print(f"\nBase: {base}")
        print("-" * 48)
        for fn in names:
            print(f"  ❌ {fn}")

    print("\n" + "=" * 96)
    print()


def run_similar_name_scan(
    *,
    database: str = "CAD_FUNCINFO",
    table: str = "function_analysis",
    min_group_size: int = 2,
    only_ok: bool = True,
    max_bases: Optional[int] = None,
) -> Dict:
    """
    一键：从 DB 做相近函数族群分析 + 打印报告 + 返回结果
    """
    # 复用你已经写好的分组逻辑
    groups = find_similar_named_functions_from_db(
        database=database,
        table=table,
        min_group_size=min_group_size,
    )
    delete_map = build_delete_suggestions(groups)

    _format_similar_report(groups, delete_map, max_bases=max_bases)

    return {
        "ok": True,
        "groups": groups,
        "delete_map": delete_map,
        "group_count": len(groups),
        "suggestion_group_count": len(delete_map),
    }


# ---------------------------------------------------------------------
# DB 读取：加载函数分析结果
# ---------------------------------------------------------------------
def load_functions_from_db(
    *,
    database: str,
    table: str,
) -> List[dict]:
    """
    从函数分析库加载函数记录
    仅加载 ok=1 的有效函数
    """

    sql = f"""
        SELECT
            id,
            func_name,
            qualified_name,
            file_path,
            start_line,
            end_line,
            source_hash,
            ok
        FROM `{table}`
        WHERE ok=1
    """

    rows = dbop.execute_sql(
        database,
        sql,
        params=None,
        fetch=True,
        dictionary=True,
    )

    return rows or []



##使用
"""

from tools.function_name_cleaner import run_similar_name_scan

run_similar_name_scan(
    database="CAD_FUNCINFO",
    table="function_analysis",
    min_group_size=2,
)


"""


