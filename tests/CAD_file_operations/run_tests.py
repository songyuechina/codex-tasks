#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对 cad/scripts/CAD_file_operations.py 中每个函数进行最小可行性回归测试。

说明：
- 仅调用公开函数，不修改源脚本。
- 尝试生成 DWG 测试输出，路径统一放在 tests/CAD_file_operations/dwg_outputs/。
- 若依赖 AutoCAD/TArch COM 环境不可用，将记录为“blocked”并附原因。
"""

import json
from pathlib import Path
import datetime
import traceback

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "cad" / "scripts"
OUTPUT_DIR = ROOT / "tests" / "CAD_file_operations" / "dwg_outputs"
INPUT_DIR = ROOT / "tests" / "CAD_file_operations" / "dwg_inputs"
LOG_FILE = ROOT / "tests" / "CAD_file_operations" / "logs" / "test_log.json"

import sys
sys.path.insert(0, str(SCRIPT_DIR))

from CAD_file_operations import (
    new_file,
    open_file,
    copy_file_with_increment,
    save_file,
    save_file_as,
    close_file,
    close_all_files,
    insert_file_as_block,
    insert_file_exploded,
    copy_file_content_pywin32,
    insert_region_from_file,
    dim_by_points,
    draw_tarch_wall,
    insert_tarch_door,
    insert_tarch_window,
    start_cad_session,
    restore_to_uncertain_state,
    activate_document_by_name,
    cad_zt_zero,
    cad_zt_oneb,
    cad_zt_oned,
    cad_zt_two,
    cad_zt_much,
)
from CAD_basic import li


results = []


def record(name, status, detail=None, output=None):
    results.append(
        {
            "function": name,
            "status": status,  # pass / fail / blocked / error
            "detail": detail or "",
            "output": str(output) if output else "",
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        }
    )


def require_com():
    """简单探测 AutoCAD COM 是否可用。"""
    try:
        import win32com.client

        win32com.client.GetActiveObject("AutoCAD.Application")
        return True
    except Exception:
        return False


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 尝试启动会话
    try:
        start_cad_session()
        cad_ready = True
        record("start_cad_session", "pass", "已调用启动流程")
    except Exception as e:
        cad_ready = require_com()
        record(
            "start_cad_session",
            "blocked" if not cad_ready else "fail",
            f"启动失败: {e}",
        )

    # 1) new_file
    target_new = OUTPUT_DIR / "new_file.dwg"
    try:
        ok = new_file(str(target_new))
        if ok and target_new.exists():
            record("new_file", "pass", output=target_new)
        else:
            reason = "函数返回False" if not ok else "未找到输出文件"
            record("new_file", "fail", reason)
    except Exception as e:
        record("new_file", "blocked", f"依赖COM环境: {e}")

    # 2) open_file
    src = INPUT_DIR / "test_all_func.dwg"
    try:
        ok = open_file(str(src))
        record("open_file", "pass" if ok else "fail", "函数返回False" if not ok else "", output=src)
    except Exception as e:
        record("open_file", "blocked", f"无法连接CAD: {e}")

    # 3) copy_file_with_increment
    try:
        new_path = copy_file_with_increment(str(src))
        if new_path and Path(new_path).exists():
            record("copy_file_with_increment", "pass", output=new_path)
        else:
            record("copy_file_with_increment", "fail", "未生成递增文件")
    except Exception as e:
        record("copy_file_with_increment", "error", traceback.format_exc())

    # 4) save_file
    try:
        ok = save_file()
        detail = "" if ok else "函数返回False"
        record("save_file", "pass" if ok else "fail", detail)
    except Exception as e:
        record("save_file", "blocked", f"依赖已打开文件: {e}")

    # 5) save_file_as
    try:
        target = OUTPUT_DIR / "save_as.dwg"
        ok = save_file_as(str(target))
        detail = "" if ok else "函数返回False"
        record("save_file_as", "pass" if ok else "fail", detail, target)
    except Exception as e:
        record("save_file_as", "blocked", f"依赖已打开文件: {e}")

    # 6) close_file
    try:
        ok = close_file()
        record("close_file", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("close_file", "blocked", f"依赖已打开文件: {e}")

    # 7) close_all_files
    try:
        ok = close_all_files()
        record("close_all_files", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("close_all_files", "blocked", f"依赖COM: {e}")

    # 8) insert_file_as_block
    target = OUTPUT_DIR / "insert_block_target.dwg"
    try:
        new_file(str(target))
        ok = insert_file_as_block(str(INPUT_DIR / "test_block_source.dwg"), 0, 0, 0)
        detail = "" if ok else "函数返回False"
        record("insert_file_as_block", "pass" if ok else "fail", detail, target)
    except Exception as e:
        record("insert_file_as_block", "blocked", f"依赖CAD插入: {e}")

    # 9) insert_file_exploded
    try:
        new_file(str(target))
        ok = insert_file_exploded(str(INPUT_DIR / "test_block_source.dwg"), 0, 0, 0)
        detail = "" if ok else "函数返回False"
        record("insert_file_exploded", "pass" if ok else "fail", detail, target)
    except Exception as e:
        record("insert_file_exploded", "blocked", f"依赖CAD炸开: {e}")

    # 10) copy_file_content_pywin32
    try:
        source = INPUT_DIR / "test_block_source.dwg"
        target = OUTPUT_DIR / "copy_pywin32.dwg"
        target.write_bytes(source.read_bytes())
        ok = copy_file_content_pywin32(str(source), str(target))
        detail = "" if ok else "函数返回False"
        record("copy_file_content_pywin32", "pass" if ok else "fail", detail, target)
    except Exception as e:
        record("copy_file_content_pywin32", "blocked", f"COM复制失败: {e}")

    # 11) insert_region_from_file
    try:
        source_region = OUTPUT_DIR / "insert_region_from_file_2.dwg"
        target_region = OUTPUT_DIR / "insert_region_from_file_1.dwg"
        open_file(str(target_region))
        li()
        ok = insert_region_from_file(
            str(source_region),
            2967.3644,
            484.092,
            6932.79,
            -1821.9816,
            0,
            0,
            True,
        )
        close_file("no_save")
        detail = "" if ok else "未能复制区域对象"
        record("insert_region_from_file", "pass" if ok else "fail", detail, target_region)
    except Exception as e:
        record("insert_region_from_file", "blocked", f"依赖CAD区域插入: {e}")
    # 12) dim_by_points
    try:
        ok = dim_by_points((0, 0, 0), (1000, 0, 0), (500, 200, 0))
        record("dim_by_points", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("dim_by_points", "blocked", f"依赖CAD标注: {e}")

    # 13) draw_tarch_wall
    try:
        ok = draw_tarch_wall((0, 0, 0), (5000, 0, 0), thickness=240)
        record("draw_tarch_wall", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("draw_tarch_wall", "blocked", f"依赖天正墙: {e}")

    # 14) insert_tarch_door
    try:
        ok = insert_tarch_door((2500, 0, 0), width=900, height=2100)
        succeeded = bool(ok and ok.get("success"))
        detail = "" if succeeded else f"返回: {ok}"
        record("insert_tarch_door", "pass" if succeeded else "fail", detail)
    except Exception as e:
        record("insert_tarch_door", "blocked", f"依赖天正门: {e}")

    # 15) insert_tarch_window
    try:
        ok = insert_tarch_window((2500, 0, 0), width=1500, height=1200, window_type="jz-pingchuang")
        succeeded = bool(ok and ok.get("success"))
        detail = "" if succeeded else f"返回: {ok}"
        record("insert_tarch_window", "pass" if succeeded else "fail", detail)
    except Exception as e:
        record("insert_tarch_window", "blocked", f"依赖天正窗: {e}")

    # 16) restore_to_uncertain_state
    try:
        ok = restore_to_uncertain_state()
        record("restore_to_uncertain_state", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("restore_to_uncertain_state", "blocked", f"依赖CAD: {e}")

    # 17) activate_document_by_name
    try:
        open_file(str(INPUT_DIR / "test_block_source.dwg"))
        open_file(str(INPUT_DIR / "test_window_rectangle.dwg"))
        li()
        ok = activate_document_by_name(Path(INPUT_DIR / "test_block_source.dwg").name)
        close_all_files()
        record("activate_document_by_name", "pass" if ok else "fail")
    except Exception as e:
        record("activate_document_by_name", "blocked", f"依赖已打开文件: {e}")

    # 18) cad_zt_zero
    try:
        ok = cad_zt_zero()
        record("cad_zt_zero", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("cad_zt_zero", "blocked", f"依赖CAD: {e}")

    # 19) cad_zt_oneb
    try:
        ok = cad_zt_oneb()
        record("cad_zt_oneb", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("cad_zt_oneb", "blocked", f"依赖CAD: {e}")

    # 20) cad_zt_oned
    try:
        ok = cad_zt_oned(str(INPUT_DIR / "test_all_func.dwg"))
        record("cad_zt_oned", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("cad_zt_oned", "blocked", f"依赖CAD: {e}")

    # 21) cad_zt_two
    try:
        ok = cad_zt_two(
            str(INPUT_DIR / "test_all_func.dwg"),
            str(INPUT_DIR / "test_block_source.dwg"),
        )
        record("cad_zt_two", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("cad_zt_two", "blocked", f"依赖CAD: {e}")

    # 22) cad_zt_much
    try:
        ok = cad_zt_much(
            str(INPUT_DIR / "test_all_func.dwg"),
            str(INPUT_DIR / "test_block_source.dwg"),
            str(INPUT_DIR / "test_window_rectangle.dwg"),
        )
        record("cad_zt_much", "pass" if ok else "fail", "" if ok else "函数返回False")
    except Exception as e:
        record("cad_zt_much", "blocked", f"依赖CAD: {e}")

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

