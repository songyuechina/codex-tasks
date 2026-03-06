#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多段线与样条模块（cad_geometry_polyline.py）
"""

# ================= 路径引导 =================
import sys
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current:
        raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

# ================= 标准库 =================
import time
import pythoncom
import math
from typing import List, Tuple

# ================= 系统模块 =================
from system.project_setup import PathConfig
from system.licad import resolve_doc
from system.CAD_com_utils import sys_logger, retry_if_busy, retry_on_busy, SafeCOM
from system.common_logger import checkpoint
from system.CAD_coordination import wait_quiescent
from system import CAD_selection
from system.CAD_core import get_obj_loc


# ================= 内部工具 =================

# 获取当前时间戳（毫秒）
#&&% _now_ms
def _now_ms():
    return int(time.time() * 1000)


# 记录开始日志
#&&% _log_start
def _log_start(func_name, detail):
    sys_logger.info(f"[START] {func_name} {detail}")
    return _now_ms()


# 记录结束日志
#&&% _log_end
def _log_end(func_name, start_ms, ok=True, detail=""):
    duration = _now_ms() - start_ms
    sys_logger.info(f"[END] {func_name} ok={ok} duration_ms={duration} {detail}")


# 点坐标转三维
#&&% _as_3d
def _as_3d(pt):
    if pt is None:
        return None
    try:
        if len(pt) == 2:
            return (float(pt[0]), float(pt[1]), 0.0)
        return (float(pt[0]), float(pt[1]), float(pt[2]))
    except Exception:
        return None


# COM 调用重试封装
#&&% _call_retry
def _call_retry(func, *args, **kwargs):
    @retry_if_busy(max_retries=3, delay=0.4)
    def _inner():
        return func(*args, **kwargs)
    return _inner()


# COM 删除重试封装
#&&% _call_delete
def _call_delete(func, *args, **kwargs):
    @retry_on_busy(max_retries=3, base_delay=0.4)
    def _inner():
        return func(*args, **kwargs)
    return _inner()


# 确保列表输入
#&&% _ensure_list
def _ensure_list(obj):
    if obj is None:
        return []
    return obj if isinstance(obj, (list, tuple)) else [obj]


# ================= 样条与多段线 =================

# 样条转多段线（SPLINEDIT）
#&&% spline_to_polyline_via_splinedit

def spline_to_polyline_via_splinedit(spline_entity, segments=10, docname=None, cleanup_copy=True, wait_sec=1.2):
    """将样条复制并通过 SPLINEDIT 转为多段线，返回新多段线对象。"""
    t0 = _log_start("spline_to_polyline_via_splinedit", f"docname={docname} segments={segments}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("spline_to_polyline_via_splinedit", t0, ok=False, detail="doc=None")
        return None
    if docname is None:
        sys_logger.warning("[spline_to_polyline_via_splinedit] using_active_doc=True")

    copy_ent = None
    new_pl = None
    doc_real = None
    moved = False
    move_dx = 0.0
    move_dy = 0.0
    try:
        doc_real = getattr(doc, "_real_doc", None)
        # 若 docname 与实体所属文档不一致，尝试激活实体文档
        try:
            ent_doc = spline_entity.Document
            if docname and hasattr(ent_doc, "Name"):
                if str(ent_doc.Name).lower() != str(docname).lower():
                    try:
                        ent_doc.Activate()
                        doc = resolve_doc(ent_doc.Name)
                    except Exception:
                        pass
        except Exception:
            pass

        copy_ent = _call_retry(spline_entity.Copy)
        if not copy_ent:
            _log_end("spline_to_polyline_via_splinedit", t0, ok=False, detail="copy failed")
            return None

        # 保持原位，避免改变用户视觉/选择状态

        # 避免额外 SELECT/Zoom 打断预选高亮状态
        try:
            doc.SetVariable("PICKFIRST", 1)
        except Exception:
            pass
        try:
            doc.SetVariable("PICKADD", 1)
        except Exception:
            pass

        pre_count = doc.ModelSpace.Count
        seg_val = int(segments) if segments is not None else 10
        if seg_val < 2:
            seg_val = 2
        def _find_recent_polyline(doc_obj, pre_count, handle_exclude=None, tail=20):
            try:
                count = doc_obj.ModelSpace.Count
            except Exception:
                return None
            if pre_count is None or pre_count < 0:
                start = max(0, count - tail)
            else:
                # 若对象总数未增加，仍检查最后一段，避免“替换”型转换漏检
                if count <= pre_count:
                    start = max(0, count - tail)
                else:
                    start = max(pre_count, count - tail)
            for i in range(count - 1, start - 1, -1):
                try:
                    ent = doc_obj.ModelSpace.Item(i)
                    name = str(getattr(ent, "ObjectName", ""))
                    if "Polyline" in name:
                        if handle_exclude and str(getattr(ent, "Handle", "")).lower() == str(handle_exclude).lower():
                            continue
                        return ent
                except Exception:
                    continue
            return None

        def _find_polyline_by_bbox(doc_obj, ref_min, ref_max, tol=1.0, tail=60):
            if ref_min is None or ref_max is None:
                return None
            try:
                count = doc_obj.ModelSpace.Count
            except Exception:
                return None
            start = max(0, count - tail)
            try:
                span = max(abs(ref_max[0] - ref_min[0]), abs(ref_max[1] - ref_min[1]))
                tol_use = max(float(tol), 2.0, 0.02 * span)
            except Exception:
                tol_use = max(float(tol), 2.0)
            for i in range(count - 1, start - 1, -1):
                try:
                    ent = doc_obj.ModelSpace.Item(i)
                    name = str(getattr(ent, "ObjectName", ""))
                    if "Polyline" not in name:
                        continue
                    p1, p2 = ent.GetBoundingBox()
                    if (
                        abs(p1[0] - ref_min[0]) <= tol_use and
                        abs(p1[1] - ref_min[1]) <= tol_use and
                        abs(p2[0] - ref_max[0]) <= tol_use and
                        abs(p2[1] - ref_max[1]) <= tol_use
                    ):
                        return ent
                except Exception:
                    continue
            return None

        handle = None
        try:
            handle = getattr(copy_ent, "Handle", None)
        except Exception:
            handle = None

        def _send_line(doc_cmd, line, delay=0.18):
            try:
                payload = "" if line is None else str(line)
                if not payload.endswith("\n"):
                    payload += "\n"
                if hasattr(doc_cmd, "PostCommand"):
                    doc_cmd.PostCommand(payload)
                else:
                    doc_cmd.SendCommand(payload)
                sys_logger.info(f"[spline_to_polyline_via_splinedit] cmd>> {payload.strip()}")
            except Exception:
                pass
            if delay:
                time.sleep(delay)

        def _wait_cmd_active(doc_cmd, timeout=2.0):
            start = time.time()
            while time.time() - start < timeout:
                try:
                    if int(doc_cmd.GetVariable("CMDACTIVE")) > 0:
                        return True
                except Exception:
                    pass
                time.sleep(0.05)
            return False

        def _cmd_active(doc_cmd):
            try:
                return int(doc_cmd.GetVariable("CMDACTIVE")) > 0
            except Exception:
                return False

        def _cmd_names(doc_cmd):
            try:
                return str(doc_cmd.GetVariable("CMDNAMES") or "")
            except Exception:
                return ""

        def _last_prompt(doc_cmd):
            try:
                return str(doc_cmd.GetVariable("LASTPROMPT") or "")
            except Exception:
                return ""

        def _log_cmd_state(doc_cmd, tag):
            try:
                ca = None
                try:
                    ca = int(doc_cmd.GetVariable("CMDACTIVE"))
                except Exception:
                    ca = None
                sys_logger.info(
                    f"[spline_to_polyline_via_splinedit] {tag} "
                    f"CMDACTIVE={ca} CMDNAMES='{_cmd_names(doc_cmd)}' LASTPROMPT='{_last_prompt(doc_cmd)}'"
                )
            except Exception:
                pass

        def _wait_cmd_name(doc_cmd, name, timeout=2.0):
            start = time.time()
            while time.time() - start < timeout:
                try:
                    if name and name.lower() in _cmd_names(doc_cmd).lower():
                        return True
                except Exception:
                    pass
                time.sleep(0.05)
            return False

        def _wait_cmd_done(doc_cmd, timeout=20.0, poll_s=0.05):
            t0 = time.time()
            while time.time() - t0 < timeout:
                try:
                    pythoncom.PumpWaitingMessages()
                except Exception:
                    pass
                try:
                    if int(doc_cmd.GetVariable("CMDACTIVE")) == 0:
                        return True
                except Exception:
                    pass
                time.sleep(poll_s)
            return False

        def _wait_prompt_contains(doc_cmd, keywords, timeout=5.0):
            t0 = time.time()
            while time.time() - t0 < timeout:
                try:
                    lp = _last_prompt(doc_cmd)
                except Exception:
                    lp = ""
                if lp:
                    for kw in keywords:
                        if kw and kw in lp:
                            return True
                time.sleep(0.1)
            return False

        def _can_send_p(doc_cmd):
            try:
                if "SPLINEDIT" in _cmd_names(doc_cmd).upper():
                    return True
            except Exception:
                pass
            lp = _last_prompt(doc_cmd)
            if "输入选项" in lp or "Enter an option" in lp:
                return True
            return False

        def _safe_send_p_precision(doc_cmd, precision, timeout=6.0):
            if not _can_send_p(doc_cmd):
                return False
            _send_line(doc_cmd, "P", delay=0.15)
            if not _wait_prompt_contains(doc_cmd, ["指定精度", "Specify precision"], timeout=timeout):
                return False
            _send_line(doc_cmd, str(int(precision)), delay=0.15)
            _send_line(doc_cmd, "", delay=0.1)
            return True

        def _cancel_active(doc_cmd):
            try:
                _send_line(doc_cmd, "\x1b", delay=0.05)
                _send_line(doc_cmd, "\x1b", delay=0.05)
            except Exception:
                pass
            _wait_cmd_done(doc_cmd, timeout=4.0)

        def _wait_prompt_idle(doc_cmd, timeout=8.0, poll_s=0.1):
            t0 = time.time()
            while time.time() - t0 < timeout:
                try:
                    lp = _last_prompt(doc_cmd)
                except Exception:
                    lp = ""
                try:
                    ca = int(doc_cmd.GetVariable("CMDACTIVE"))
                except Exception:
                    ca = 0
                lp_norm = lp.strip().lower()
                # 等待到“命令:”/空提示且不在重生成
                if ca == 0 and (lp_norm in ("命令:", "command:", "命令:") or "command:" in lp_norm):
                    return True
                if "重生成" in lp or "REGEN" in lp.upper():
                    time.sleep(poll_s)
                    continue
                time.sleep(poll_s)
            return False

        def _ensure_prompt_ready(doc_cmd, attempts=3):
            for _ in range(attempts):
                if _wait_prompt_idle(doc_cmd, timeout=2.0):
                    return True
                try:
                    doc_cmd.SendCommand("\n")
                except Exception:
                    pass
                time.sleep(0.2)
            return _wait_prompt_idle(doc_cmd, timeout=3.0)

        def _splinedit_by_handle_raw(ob, precision, timeout_s=30.0):
            try:
                raw_doc = ob.Document
                handle_local = ob.Handle
            except Exception:
                return False
            try:
                # 注意：不要在 P 前插入空回车，否则会直接退出命令
                lisp = (
                    f'(progn '
                    f'(setq __e (handent "{handle_local}")) '
                    f'(if (and __e (wcmatch (strcase (cdr (assoc 0 (entget __e)))) "*SPLINE*")) '
                    f'(vl-cmdf "_.SPLINEDIT" __e "P" "{int(precision)}" "") '
                    f'(princ "noent")) '
                    f'(princ))'
                )
                _log_cmd_state(raw_doc, "before_lisp")
                if not _ensure_prompt_ready(raw_doc, attempts=3):
                    sys_logger.info("[spline_to_polyline_via_splinedit] prompt not idle, skip lisp")
                    return False
                raw_doc.SendCommand(lisp + "\n")
                time.sleep(0.3)
                _log_cmd_state(raw_doc, "after_lisp")
            except Exception:
                return False
            return _wait_cmd_done(raw_doc, timeout=timeout_s)

        doc_cmd = doc_real if doc_real is not None else doc
        cmd_splinedit = "SPLINEDIT"

        # 发送 SPLINEDIT → P → 选择对象 → 回车 → 精度 → 回车
        try:
            wait_quiescent(min_quiet=0.2, timeout=10.0)
        except Exception:
            pass
        sent = False

        # 优先使用 LISP 单条命令，避免命令行交互不稳定
        try:
            if doc_real is not None:
                doc_real.Activate()
        except Exception:
            pass
        try:
            doc.SetVariable("PICKFIRST", 1)
        except Exception:
            pass
        # 优先：按命令行 _C 方式（你给的真实操作）
        def _run_interactive():
            try:
                # 计算“端点 + 左上偏移点”的窗口，匹配你给的 _C 反选方式
                try:
                    sp = getattr(copy_ent, "StartPoint", None)
                except Exception:
                    sp = None
                if sp is None:
                    try:
                        sp = copy_ent.GetPointAtParam(copy_ent.StartParam)
                    except Exception:
                        sp = None
                if sp is not None:
                    # 按你的经验：端点 + 左上 10~20 偏移
                    dx = 20.0
                    dy = 20.0
                    p1 = (float(sp[0]), float(sp[1]))
                    p2 = (float(sp[0]) - dx, float(sp[1]) + dy)
                else:
                    try:
                        bb1, bb2 = copy_ent.GetBoundingBox()
                    except Exception:
                        bb1, bb2 = None, None
                    if bb1 is None or bb2 is None:
                        return False
                    pad = max(10.0, 0.05 * max(abs(bb2[0] - bb1[0]), abs(bb2[1] - bb1[1])))
                    p1 = (float(bb1[0]) - pad, float(bb1[1]) - pad)
                    p2 = (float(bb2[0]) + pad, float(bb2[1]) + pad)

                # 按你给的命令行操作逐步发送并等待提示词出现
                def _wait_prompt_match(doc_cmd, mapping, timeout=5.0):
                    t0 = time.time()
                    while time.time() - t0 < timeout:
                        try:
                            lp = _last_prompt(doc_cmd)
                        except Exception:
                            lp = ""
                        if lp:
                            for key, kws in mapping:
                                for kw in kws:
                                    if kw and kw in lp:
                                        return key, lp
                        time.sleep(0.1)
                    return None, _last_prompt(doc_cmd)

                try:
                    raw = doc_real if doc_real is not None else doc_cmd
                    try:
                        raw.Activate()
                    except Exception:
                        pass
                    if not _ensure_prompt_ready(raw, attempts=3):
                        sys_logger.info("[spline_to_polyline_via_splinedit] prompt not idle, skip _C path")
                        return False
                    sys_logger.info("[spline_to_polyline_via_splinedit] path=_C")

                    def _send_and_wait(cmd_line, expect, timeout=5.0):
                        raw.SendCommand(cmd_line + "\n")
                        try:
                            pythoncom.PumpWaitingMessages()
                        except Exception:
                            pass
                        ok, lastp = _wait_prompt_match(raw, [("ok", expect)], timeout=timeout)
                        if not ok:
                            sys_logger.info(f"[spline_to_polyline_via_splinedit] wait '{expect}' failed, last='{lastp}'")
                        return bool(ok)

                    # 先发 SPLINEDIT，再判断落到哪个提示（选择样条/输入选项）
                    if not _send_and_wait("SPLINEDIT", ["选择样条曲线", "Select spline", "输入选项", "Enter an option"], timeout=6.0):
                        # 兼容：再试一次带下划线的国际化命令
                        if not _send_and_wait("_SPLINEDIT", ["选择样条曲线", "Select spline", "输入选项", "Enter an option"], timeout=6.0):
                            return False

                    # 查看当前提示，若已进入“输入选项”，直接 P -> 精度
                    key, lastp = _wait_prompt_match(
                        raw,
                        [
                            ("options", ["输入选项", "Enter an option"]),
                            ("select", ["选择样条曲线", "Select spline"]),
                        ],
                        timeout=1.5,
                    )
                    if key == "options":
                        sys_logger.info(f"[spline_to_polyline_via_splinedit] options_prompt='{lastp}'")
                        if not _send_and_wait("P", ["指定精度", "Specify precision"], timeout=5.0):
                            return False
                        raw.SendCommand(f"{seg_val}\n")
                        _wait_cmd_done(raw, timeout=10.0)
                        return True

                    if not _send_and_wait("_C", ["指定第一个角点", "Specify first corner"], timeout=5.0):
                        return False

                    if not _send_and_wait(f"{p1[0]},{p1[1]}", ["指定对角点", "Specify opposite corner"], timeout=5.0):
                        return False

                    if not _send_and_wait(f"{p2[0]},{p2[1]}", ["输入选项", "Enter an option"], timeout=6.0):
                        return False

                    if not _send_and_wait("P", ["指定精度", "Specify precision"], timeout=5.0):
                        return False

                    raw.SendCommand(f"{seg_val}\n")
                    try:
                        pythoncom.PumpWaitingMessages()
                    except Exception:
                        pass
                    _wait_cmd_done(raw, timeout=10.0)
                    return True
                except Exception:
                    pass

                # SCRIPT：SPLINEDIT -> C -> p1 -> p2 -> [Enter] -> P -> seg -> Enter
                # 优先：LISP 一步完成 (command 走 C 窗口)
                try:
                    lisp_cmd = (
                        f'(progn '
                        f'(command "{cmd_splinedit}" "C" (list {p1[0]} {p1[1]}) (list {p2[0]} {p2[1]}) "" "P" "{seg_val}" "") '
                        f'(princ))'
                    )
                    _send_line(doc_cmd, lisp_cmd, delay=0.2)
                    return True
                except Exception:
                    pass

                # SCRIPT 方案已在上方以 _C 精确流程执行

                # 逐行发送（同 C 方式）
                _send_line(doc_cmd, cmd_splinedit)
                _wait_cmd_name(doc_cmd, "SPLINEDIT", timeout=2.0)
                _send_line(doc_cmd, "C")
                _send_line(doc_cmd, f"{p1[0]},{p1[1]}")
                _send_line(doc_cmd, f"{p2[0]},{p2[1]}")
                _send_line(doc_cmd, "")  # 结束选择
                _send_line(doc_cmd, "P")
                _send_line(doc_cmd, str(seg_val))
                _send_line(doc_cmd, "")
                return True
            except Exception:
                return False

        # 优先：LISP 原子命令（绑定选择 + 参数）
        if not sent:
            try:
                if copy_ent is not None:
                    sent = _splinedit_by_handle_raw(copy_ent, seg_val, timeout_s=30.0)
            except Exception:
                sent = False

        def _run_preselect_then_cmd():
            try:
                # 仅使用“预选对象 + SPLINEDIT”路径，避免 _C 卡死
                _send_line(doc_cmd, cmd_splinedit, delay=0.2)
                if not _wait_cmd_name(doc_cmd, "SPLINEDIT", timeout=2.0):
                    return False
                # 回车确认预选对象
                _send_line(doc_cmd, "", delay=0.2)
                # 只在 SPLINEDIT 选项提示出现时再发 P，避免误触 PAN
                if not _safe_send_p_precision(doc_cmd, seg_val, timeout=6.0):
                    return False
                return True
            except Exception:
                return False

        # 若仍不成功，再走“先选对象再命令”的路径
        if not sent:
            try:
                sent = _run_preselect_then_cmd()
            except Exception:
                sent = False

        # 最后再走 _C 命令行路径（不稳定，作为兜底）
        if not sent:
            try:
                sent = _run_interactive()
            except Exception:
                sent = False

        # 再兜底：按“逐步回车”流程（强制模拟人工命令行）
        if not sent:
            try:
                if doc_real is not None:
                    doc_real.SendCommand(f"{cmd_splinedit}\n")
                    sys_logger.info(f"[spline_to_polyline_via_splinedit] send>> {cmd_splinedit}")
                    if _wait_cmd_name(doc_real, "SPLINEDIT", timeout=2.0):
                        # 回车确认预选对象
                        doc_real.SendCommand("\n")
                        time.sleep(0.2)
                        if _safe_send_p_precision(doc_real, seg_val, timeout=6.0):
                            sent = True
            except Exception:
                sent = False

        # 再尝试 LISP 单次命令（参考 export_model_window_lisp_fit 的做法）
        if not sent:
            try:
                if handle:
                    lisp_cmd = (
                        f'(progn '
                        f'(setq __sp (handent "{handle}")) '
                        f'(if __sp '
                        f'(command "{cmd_splinedit}" __sp "P" "{seg_val}" "") '
                        f'(princ "noent")) '
                        f'(princ))'
                    )
                    _send_line(doc_cmd, lisp_cmd, delay=0.2)
                    wait_quiescent(min_quiet=0.3, timeout=10.0)
                    sent = True
            except Exception:
                sent = False

        # 若命令仍悬挂过久，尝试退出，避免卡住
        if sent:
            t_dead = time.time() + 8.0
            while time.time() < t_dead:
                if not _cmd_active(doc_cmd):
                    break
                time.sleep(0.2)
            if _cmd_active(doc_cmd) and ("SPLINEDIT" in _cmd_names(doc_cmd) or "PAN" in _cmd_names(doc_cmd)):
                _cancel_active(doc_cmd)

        wait_quiescent(min_quiet=0.3, timeout=10.0)
        # 生成需要时间：轮询等待
        deadline = time.time() + max(6.0, float(wait_sec) * 3.0)
        while time.time() < deadline:
            time.sleep(0.5)
            wait_quiescent(min_quiet=0.3, timeout=3.0)
            # 优先从当前选择集中找
            try:
                ss = doc.PickfirstSelectionSet
                for i in range(ss.Count):
                    ent = ss.Item(i)
                    if "Polyline" in str(getattr(ent, "ObjectName", "")):
                        new_pl = ent
                        break
            except Exception:
                pass
            if new_pl is not None:
                break
            new_pl = _find_recent_polyline(doc, pre_count, handle_exclude=handle, tail=25)
            if new_pl is None:
                try:
                    ref_min, ref_max = copy_ent.GetBoundingBox()
                except Exception:
                    ref_min, ref_max = None, None
                new_pl = _find_polyline_by_bbox(doc, ref_min, ref_max, tol=1.0, tail=60)
            if new_pl is not None:
                break

        # LISP 兜底：用 handent 强制指定对象进行转换
        if new_pl is None and handle:
            try:
                # 备用 LISP：用 ss 传入，提高兼容性
                lisp_cmd = (
                    f'(progn '
                    f'(setq __ss (ssadd (handent "{handle}"))) '
                    f'(if __ss '
                    f'(command "{cmd_splinedit}" __ss "P" "{seg_val}" "") '
                    f'(princ "noent")) '
                    f'(princ))'
                )
                _send_line(doc_cmd, lisp_cmd, delay=0.2)
                wait_quiescent(min_quiet=0.3, timeout=10.0)
                deadline = time.time() + max(6.0, float(wait_sec) * 3.0)
                while time.time() < deadline:
                    time.sleep(0.5)
                    wait_quiescent(min_quiet=0.3, timeout=3.0)
                    new_pl = _find_recent_polyline(doc, pre_count, handle_exclude=handle, tail=25)
                    if new_pl is None:
                        try:
                            ref_min, ref_max = copy_ent.GetBoundingBox()
                        except Exception:
                            ref_min, ref_max = None, None
                        new_pl = _find_polyline_by_bbox(doc, ref_min, ref_max, tol=1.0, tail=60)
                    if new_pl is not None:
                        break
            except Exception:
                pass

        # 若仍无结果，再走“命令行拟人”路径
        if new_pl is None:
            try:
                if _run_interactive():
                    wait_quiescent(min_quiet=0.3, timeout=10.0)
                    deadline = time.time() + max(6.0, float(wait_sec) * 3.0)
                    while time.time() < deadline:
                        time.sleep(0.5)
                        wait_quiescent(min_quiet=0.3, timeout=3.0)
                        try:
                            ss = doc.PickfirstSelectionSet
                            for i in range(ss.Count):
                                ent = ss.Item(i)
                                if "Polyline" in str(getattr(ent, "ObjectName", "")):
                                    new_pl = ent
                                    break
                        except Exception:
                            pass
                        if new_pl is not None:
                            break
                        new_pl = _find_recent_polyline(doc, pre_count, handle_exclude=handle, tail=25)
                        if new_pl is None:
                            try:
                                ref_min, ref_max = copy_ent.GetBoundingBox()
                            except Exception:
                                ref_min, ref_max = None, None
                            new_pl = _find_polyline_by_bbox(doc, ref_min, ref_max, tol=1.0, tail=60)
                        if new_pl is not None:
                            break
            except Exception:
                pass

        # 诊断：检查原句柄当前对象类型
        if new_pl is None and handle:
            try:
                ent_now = doc.HandleToObject(handle)
                sys_logger.info(
                    f"[spline_to_polyline_via_splinedit] handle={handle} obj={getattr(ent_now, 'ObjectName', '')}"
                )
            except Exception:
                pass

        if new_pl is None:
            try:
                name = getattr(copy_ent, "ObjectName", "")
                if "Polyline" in str(name):
                    new_pl = copy_ent
            except Exception:
                pass
        if new_pl is None:
            try:
                h = getattr(copy_ent, "Handle", None)
                if h:
                    try:
                        ent = doc.HandleToObject(h)
                        if "Polyline" in str(getattr(ent, "ObjectName", "")):
                            new_pl = ent
                    except Exception:
                        pass
                if h and new_pl is None:
                    for i in range(doc.ModelSpace.Count - 1, -1, -1):
                        try:
                            ent = doc.ModelSpace.Item(i)
                            if str(getattr(ent, "Handle", "")).lower() == str(h).lower():
                                if "Polyline" in str(getattr(ent, "ObjectName", "")):
                                    new_pl = ent
                                    break
                        except Exception:
                            continue
            except Exception:
                pass
        if new_pl is None:
            # 兜底：采样样条点并绘制多段线
            try:
                pts = []
                try:
                    sp = float(getattr(spline_entity, "StartParam"))
                    ep = float(getattr(spline_entity, "EndParam"))
                    if ep > sp:
                        for i in range(int(seg_val) + 1):
                            t = sp + (ep - sp) * (i / float(seg_val))
                            try:
                                if hasattr(spline_entity, "GetPointAtParameter"):
                                    p = spline_entity.GetPointAtParameter(t)
                                else:
                                    p = spline_entity.GetPointAtParam(t)
                            except Exception:
                                p = None
                            if p is not None:
                                pts.append((p[0], p[1], p[2] if len(p) > 2 else 0.0))
                except Exception:
                    pts = []
                if not pts:
                    try:
                        length = getattr(spline_entity, "Length", None)
                        if length and length > 0 and hasattr(spline_entity, "GetPointAtDist"):
                            for i in range(int(seg_val) + 1):
                                d = length * (i / float(seg_val))
                                p = spline_entity.GetPointAtDist(d)
                                if p is not None:
                                    pts.append((p[0], p[1], p[2] if len(p) > 2 else 0.0))
                    except Exception:
                        pts = []
                if not pts:
                    try:
                        raw = getattr(spline_entity, "FitPoints", None) or getattr(spline_entity, "ControlPoints", None)
                        if raw:
                            if isinstance(raw, (list, tuple)) and raw and isinstance(raw[0], (list, tuple)):
                                pts = [(_as_3d(p)) for p in raw]
                            else:
                                flat = list(raw)
                                if len(flat) % 3 == 0:
                                    for i in range(0, len(flat), 3):
                                        pts.append((flat[i], flat[i + 1], flat[i + 2]))
                    except Exception:
                        pts = []
                pts = [p for p in pts if p is not None]
                if pts and len(pts) >= 2:
                    try:
                        from library import cad_geometry_draw as draw
                    except Exception:
                        import cad_geometry_draw as draw
                    layer = None
                    color = None
                    try:
                        layer = getattr(spline_entity, "Layer", None)
                    except Exception:
                        layer = None
                    try:
                        color = getattr(spline_entity, "Color", None)
                    except Exception:
                        color = None
                    new_pl = draw.draw_lwpolyline_wcs(pts, closed=False, layer=layer, color=color, docname=docname)
                    if new_pl is not None:
                        sys_logger.info("[spline_to_polyline_via_splinedit] fallback sampled polyline")
            except Exception:
                pass

        if cleanup_copy and (new_pl is None or new_pl is not copy_ent):
            try:
                if copy_ent is not None:
                    _call_delete(copy_ent.Delete)
            except Exception:
                pass

        if new_pl is not None:
            checkpoint("spline_to_polyline_via_splinedit")
        _log_end("spline_to_polyline_via_splinedit", t0, ok=new_pl is not None)
        return new_pl
    except Exception as e:
        sys_logger.info(f"[spline_to_polyline_via_splinedit] 异常: {e}")
        _log_end("spline_to_polyline_via_splinedit", t0, ok=False)
        return None

# 样条长度（转换）
#&&% spline_length_via_conversion

def spline_length_via_conversion(spline_entity, docname=None, cleanup=True, wait_sec=1.2, segments=10):
    """复制样条并转为多段线，读取 Length。"""
    t0 = _log_start("spline_length_via_conversion", f"docname={docname} cleanup={cleanup}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("spline_length_via_conversion", t0, ok=False, detail="doc=None")
        return None
    if docname is None:
        sys_logger.warning("[spline_length_via_conversion] using_active_doc=True")

    try:
        # 若 docname 与实体所属文档不一致，尝试激活实体文档
        try:
            ent_doc = spline_entity.Document
            if docname and hasattr(ent_doc, "Name"):
                if str(ent_doc.Name).lower() != str(docname).lower():
                    try:
                        ent_doc.Activate()
                        doc = resolve_doc(ent_doc.Name)
                    except Exception:
                        pass
        except Exception:
            pass

        new_pl = spline_to_polyline_via_splinedit(
            spline_entity,
            segments=segments,
            docname=docname,
            cleanup_copy=True,
            wait_sec=wait_sec,
        )

        length = new_pl.Length if new_pl is not None else None
        if length is None:
            try:
                direct = getattr(spline_entity, "Length", None)
                if direct is not None and direct > 0:
                    length = float(direct)
                    sys_logger.info("[spline_length_via_conversion] fallback direct Length")
            except Exception:
                pass
        if length is None:
            # 兜底：复制体炸开求长度
            try:
                temp_copy = None
                try:
                    temp_copy = _call_retry(spline_entity.Copy)
                except Exception:
                    temp_copy = None
                parts = None
                try:
                    parts = temp_copy.Explode() if temp_copy is not None else None
                except Exception:
                    parts = None
                if parts:
                    total = 0.0
                    for part in parts:
                        try:
                            pl = getattr(part, "Length", None)
                            if pl is None:
                                sp = getattr(part, "StartPoint", None)
                                ep = getattr(part, "EndPoint", None)
                                if sp is not None and ep is not None:
                                    dx = ep[0] - sp[0]
                                    dy = ep[1] - sp[1]
                                    dz = ep[2] - sp[2] if len(ep) > 2 and len(sp) > 2 else 0.0
                                    pl = math.hypot(math.hypot(dx, dy), dz)
                            if pl is not None:
                                total += float(pl)
                        except Exception:
                            continue
                    if total > 0:
                        length = total
                        sys_logger.info("[spline_length_via_conversion] fallback explode length")
                    if cleanup:
                        for part in parts:
                            try:
                                _call_delete(part.Delete)
                            except Exception:
                                pass
                if cleanup and temp_copy is not None:
                    try:
                        _call_delete(temp_copy.Delete)
                    except Exception:
                        pass
            except Exception:
                pass
        if length is None:
            # 兜底：用 FitPoints / ControlPoints 近似
            try:
                raw = None
                try:
                    raw = getattr(spline_entity, "FitPoints", None)
                except Exception:
                    raw = None
                if not raw:
                    try:
                        raw = getattr(spline_entity, "ControlPoints", None)
                    except Exception:
                        raw = None
                pts = []
                if raw:
                    if isinstance(raw, (list, tuple)):
                        if raw and isinstance(raw[0], (list, tuple)):
                            pts = [(_as_3d(p)) for p in raw]
                        else:
                            flat = list(raw)
                            if len(flat) % 3 == 0:
                                for i in range(0, len(flat), 3):
                                    pts.append((flat[i], flat[i + 1], flat[i + 2]))
                    else:
                        try:
                            flat = list(raw)
                            if len(flat) % 3 == 0:
                                for i in range(0, len(flat), 3):
                                    pts.append((flat[i], flat[i + 1], flat[i + 2]))
                        except Exception:
                            pts = []
                pts = [p for p in pts if p is not None]
                if len(pts) >= 2:
                    total = 0.0
                    for i in range(len(pts) - 1):
                        a = pts[i]
                        b = pts[i + 1]
                        dx = b[0] - a[0]
                        dy = b[1] - a[1]
                        dz = b[2] - a[2]
                        total += math.hypot(math.hypot(dx, dy), dz)
                    if total > 0:
                        length = total
                        sys_logger.info("[spline_length_via_conversion] fallback fit/control points length")
            except Exception:
                pass

        if cleanup:
            try:
                if new_pl is not None:
                    _call_delete(new_pl.Delete)
            except Exception:
                pass

        if length is not None:
            checkpoint("spline_length_via_conversion")
        _log_end("spline_length_via_conversion", t0, ok=length is not None)
        return length
    except Exception as e:
        sys_logger.info(f"[spline_length_via_conversion] 异常: {e}")
        _log_end("spline_length_via_conversion", t0, ok=False)
        return None


# 多段线基础信息
#&&% polyline_basic_info

def polyline_basic_info(pl_entity):
    """读取多段线起点/终点/长度/面积/闭合。"""
    t0 = _log_start("polyline_basic_info", "")
    if pl_entity is None:
        _log_end("polyline_basic_info", t0, ok=False, detail="pl=None")
        return None
    try:
        coords = list(getattr(pl_entity, "Coordinates", []))
        if not coords:
            _log_end("polyline_basic_info", t0, ok=False, detail="no coords")
            return None
        step = 2
        name = getattr(pl_entity, "ObjectName", "")
        if "3d" in str(name).lower() or "2d" in str(name).lower():
            step = 3
        pts = []
        for i in range(0, len(coords), step):
            x = coords[i]
            y = coords[i + 1]
            z = coords[i + 2] if step == 3 else 0.0
            pts.append((x, y, z))
        start = pts[0]
        end = pts[-1]
        length = getattr(pl_entity, "Length", None)
        is_closed = getattr(pl_entity, "Closed", False)
        area = getattr(pl_entity, "Area", 0) if is_closed else 0
        res = {"start": start, "end": end, "length": length, "area": area, "is_closed": bool(is_closed)}
        _log_end("polyline_basic_info", t0, ok=True)
        return res
    except Exception as e:
        sys_logger.info(f"[polyline_basic_info] 异常: {e}")
        _log_end("polyline_basic_info", t0, ok=False)
        return None


# 多段线闭合判断
#&&% polyline_is_closed

def polyline_is_closed(pl_entity, tol=1e-6):
    t0 = _log_start("polyline_is_closed", "")
    try:
        if hasattr(pl_entity, "Closed"):
            res = bool(pl_entity.Closed)
            _log_end("polyline_is_closed", t0, ok=True, detail=f"closed={res}")
            return res
        info = polyline_basic_info(pl_entity)
        if not info:
            _log_end("polyline_is_closed", t0, ok=False)
            return False
        s = info["start"]
        e = info["end"]
        res = abs(s[0] - e[0]) <= tol and abs(s[1] - e[1]) <= tol
        _log_end("polyline_is_closed", t0, ok=True, detail=f"closed={res}")
        return res
    except Exception:
        _log_end("polyline_is_closed", t0, ok=False)
        return False


# 获取唯一顶点
#&&% get_unique_vertices_from_polyline_com

def get_unique_vertices_from_polyline_com(pl_com, tol=1e-6):
    t0 = _log_start("get_unique_vertices_from_polyline_com", "")
    if pl_com is None:
        _log_end("get_unique_vertices_from_polyline_com", t0, ok=False, detail="pl=None")
        return []
    coords = list(getattr(pl_com, "Coordinates", []))
    if not coords:
        _log_end("get_unique_vertices_from_polyline_com", t0, ok=False, detail="no coords")
        return []
    step = 2
    name = getattr(pl_com, "ObjectName", "")
    if "3d" in str(name).lower() or "2d" in str(name).lower():
        step = 3
    pts = []
    last = None
    for i in range(0, len(coords), step):
        x = coords[i]
        y = coords[i + 1]
        z = coords[i + 2] if step == 3 else 0.0
        p = (x, y, z)
        if last and abs(p[0] - last[0]) <= tol and abs(p[1] - last[1]) <= tol:
            continue
        pts.append(p)
        last = p
    _log_end("get_unique_vertices_from_polyline_com", t0, ok=True, detail=f"count={len(pts)}")
    return pts


# 多段线转坐标信息
#&&% polylines_to_coord_info

def polylines_to_coord_info(plines):
    t0 = _log_start("polylines_to_coord_info", f"n={len(plines) if plines else 0}")
    res = []
    for pl in _ensure_list(plines):
        verts = get_unique_vertices_from_polyline_com(pl)
        closed = polyline_is_closed(pl)
        res.append({"vertices": verts, "closed": closed})
    _log_end("polylines_to_coord_info", t0, ok=True, detail=f"count={len(res)}")
    return res


# 炸开多段线
#&&% explode_polylines

def explode_polylines(LB, docname=None):
    t0 = _log_start("explode_polylines", f"n={len(LB) if LB else 0}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("explode_polylines", t0, ok=False, detail="doc=None")
        return []
    if docname is None:
        sys_logger.warning("[explode_polylines] using_active_doc=True")
    res = []
    for pl in _ensure_list(LB):
        try:
            if hasattr(pl, "Explode"):
                parts = pl.Explode()
                res.extend(list(parts))
            else:
                CAD_selection.set_entity_grip_state_precise(pl)
                _call_retry(doc.SendCommand, "_.EXPLODE\n")
                wait_quiescent(min_quiet=0.3, timeout=10.0)
        except Exception:
            continue
    _log_end("explode_polylines", t0, ok=True, detail=f"count={len(res)}")
    return res


# 连接线段形成多段线
#&&% connect_lines_to_polyline_if_closed

def connect_lines_to_polyline_if_closed(lines, tol=0.01, layer=None, width=None, color=None, docname=None):
    t0 = _log_start("connect_lines_to_polyline_if_closed", f"n={len(lines) if lines else 0}")
    if not lines:
        _log_end("connect_lines_to_polyline_if_closed", t0, ok=False, detail="empty")
        return None
    try:
        from library import cad_geometry_segment as segment
    except Exception:
        import cad_geometry_segment as segment
    if not segment.is_closed_polygon_from_lines(lines, tol=tol):
        _log_end("connect_lines_to_polyline_if_closed", t0, ok=False, detail="not closed")
        return None
    verts = segment.extract_polygon_vertices_from_lines(lines, tol=tol)
    if not verts:
        _log_end("connect_lines_to_polyline_if_closed", t0, ok=False, detail="no verts")
        return None
    try:
        from library import cad_geometry_draw as draw
    except Exception:
        import cad_geometry_draw as draw
    obj = draw.draw_lwpolyline_wcs(verts, width=width, color=color, closed=True, layer=layer, docname=docname)
    _log_end("connect_lines_to_polyline_if_closed", t0, ok=bool(obj))
    return obj


# 直线段合并成多段线
#&&% lines_to_polylines

def lines_to_polylines(lines, tol=0.01, layer=None, width=None, color=None, docname=None):
    t0 = _log_start("lines_to_polylines", f"n={len(lines) if lines else 0}")
    try:
        from library import cad_geometry_segment as segment
    except Exception:
        import cad_geometry_segment as segment
    polys = segment.compute_closed_polygons_from_lines(lines, tol=tol)
    if not polys:
        _log_end("lines_to_polylines", t0, ok=False, detail="no polys")
        return []
    try:
        from library import cad_geometry_draw as draw
    except Exception:
        import cad_geometry_draw as draw
    items = []
    for poly in polys:
        items.append({"vertices": poly, "closed": True, "width": width, "color": color, "layer": layer})
    res = draw.draw_lwpolylines_batch(items, docname=docname)
    _log_end("lines_to_polylines", t0, ok=True, detail=f"count={len(res)}")
    return res


# 筛选矩形多段线
#&&% get_rectangular_polylines

def get_rectangular_polylines(min_side=100.0, area_tolerance=0.02, docname=None):
    t0 = _log_start("get_rectangular_polylines", f"min_side={min_side} tol={area_tolerance}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("get_rectangular_polylines", t0, ok=False, detail="doc=None")
        return []
    if docname is None:
        sys_logger.warning("[get_rectangular_polylines] using_active_doc=True")

    candidates = []
    try:
        candidates.extend(CAD_selection.select_polyline() or [])
    except Exception:
        pass
    try:
        candidates.extend(CAD_selection.select_polyline_chuantong() or [])
    except Exception:
        pass

    candidates = [ent for ent in candidates if get_obj_loc(ent) == 1]
    results = []
    for pl in candidates:
        try:
            min_pt, max_pt = pl.GetBoundingBox()
            dx = abs(max_pt[0] - min_pt[0])
            dy = abs(max_pt[1] - min_pt[1])
            if dx < 1e-3 or dy < 1e-3:
                continue
            if max(dx, dy) < min_side or min(dx, dy) < min_side:
                continue
            real_area = abs(getattr(pl, "Area", 0))
            box_area = dx * dy
            if box_area <= 0:
                continue
            diff_ratio = abs(real_area - box_area) / box_area
            if diff_ratio <= area_tolerance:
                coords = list(getattr(pl, "Coordinates", []))
                if coords:
                    step = 2
                    obj_name = getattr(pl, "ObjectName", "")
                    if "AcDb2dPolyline" in obj_name or "AcDb3dPolyline" in obj_name:
                        step = 3
                    xs = coords[0::step]
                    ys = coords[1::step]
                    current_min_side = min(dx, dy)
                    coord_tol = current_min_side * 0.0005
                    coord_tol = max(0.1, min(coord_tol, 10.0))
                    x_bad = 0
                    for x in xs:
                        if not (abs(x - min_pt[0]) <= coord_tol or abs(x - max_pt[0]) <= coord_tol):
                            x_bad += 1
                    y_bad = 0
                    for y in ys:
                        if not (abs(y - min_pt[1]) <= coord_tol or abs(y - max_pt[1]) <= coord_tol):
                            y_bad += 1
                    if x_bad == 0 and y_bad == 0:
                        results.append(pl)
                else:
                    results.append(pl)
        except Exception:
            continue
    _log_end("get_rectangular_polylines", t0, ok=True, detail=f"count={len(results)}")
    return results


# 布局空间矩形多段线
#&&% get_layout_rectangular_polylines_coords

def get_layout_rectangular_polylines_coords(layout_name, min_side=100.0, docname=None):
    t0 = _log_start("get_layout_rectangular_polylines_coords", f"layout={layout_name}")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("get_layout_rectangular_polylines_coords", t0, ok=False, detail="doc=None")
        return []
    if docname is None:
        sys_logger.warning("[get_layout_rectangular_polylines_coords] using_active_doc=True")

    results = []
    try:
        target_layout = doc.Layouts.Item(layout_name)
        layout_block = target_layout.Block
    except Exception as e:
        sys_logger.info(f"[get_layout_rectangular_polylines_coords] 获取布局失败: {e}")
        _log_end("get_layout_rectangular_polylines_coords", t0, ok=False)
        return []

    for obj in layout_block:
        try:
            obj_name = getattr(obj, "ObjectName", "")
            if "Polyline" not in str(obj_name):
                continue
            coords = list(getattr(obj, "Coordinates", []))
            if not coords:
                continue
            step = 2
            if "AcDb2dPolyline" in obj_name or "AcDb3dPolyline" in obj_name:
                step = 3
            num_points = len(coords) // step
            if num_points < 4:
                continue
            xs = coords[0::step]
            ys = coords[1::step]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            w = max_x - min_x
            h = max_y - min_y
            if w < min_side or h < min_side:
                continue
            current_min_side = min(w, h)
            coord_tol = current_min_side * 0.0005
            coord_tol = max(0.1, min(coord_tol, 10.0))
            x_bad = 0
            for x in xs:
                if not (abs(x - min_x) <= coord_tol or abs(x - max_x) <= coord_tol):
                    x_bad += 1
            y_bad = 0
            for y in ys:
                if not (abs(y - min_y) <= coord_tol or abs(y - max_y) <= coord_tol):
                    y_bad += 1
            if x_bad > 0 or y_bad > 0:
                continue
            results.append(obj)
        except Exception:
            continue
    _log_end("get_layout_rectangular_polylines_coords", t0, ok=True, detail=f"count={len(results)}")
    return results


# 多段线排序
#&&% sort_polylines_by_rule

def sort_polylines_by_rule(polyline_list):
    """按照左下角坐标排序，y 优先降序，近似行内按 x 升序。"""
    if not polyline_list:
        return []
    try:
        from library import cad_geometry_segment as segment
    except Exception:
        import cad_geometry_segment as segment
    polylines_with_min = [(pl, segment.get_bbox_min_point(pl)) for pl in polyline_list]
    polylines_with_min.sort(key=lambda item: -item[1][1])
    i = 0
    while i < len(polylines_with_min) - 1:
        j = i + 1
        while j < len(polylines_with_min) and abs(polylines_with_min[i][1][1] - polylines_with_min[j][1][1]) < 1000:
            j += 1
        if j - i > 1:
            polylines_with_min[i:j] = sorted(polylines_with_min[i:j], key=lambda item: item[1][0])
        i = j
    return [item[0] for item in polylines_with_min]


# 获取多段线内文字
#&&% get_texts_inside_polyline

def get_texts_inside_polyline(com_pl, tol=0.5, docname=None):
    t0 = _log_start("get_texts_inside_polyline", "")
    doc = resolve_doc(docname)
    if doc is None:
        _log_end("get_texts_inside_polyline", t0, ok=False, detail="doc=None")
        return [], []
    if docname is None:
        sys_logger.warning("[get_texts_inside_polyline] using_active_doc=True")

    try:
        from library import cad_geometry_segment as segment
    except Exception:
        import cad_geometry_segment as segment

    poly = get_unique_vertices_from_polyline_com(com_pl)
    texts = CAD_selection.select_all_texts_mixed()
    inside = []
    contents = []
    for txt in texts:
        try:
            min_pt, _ = txt.GetBoundingBox()
            if segment.point_in_polygon_xy(min_pt, poly, tol=tol):
                inside.append(txt)
                name = getattr(txt, "ObjectName", "") or getattr(txt, "EntityName", "")
                if name in ("AcDbText", "AcDbMText"):
                    contents.append(txt.TextString)
                elif name == "TDbText":
                    contents.append(txt.Text)
                elif name == "TDbMText":
                    contents.append(segment.explode_copy_and_get_mtext_content(txt, docname=docname))
                else:
                    contents.append("")
        except Exception:
            continue
    _log_end("get_texts_inside_polyline", t0, ok=True, detail=f"count={len(inside)}")
    return inside, contents


# 公共线段
#&&% common_segments_between_polylines

def common_segments_between_polylines(pl1, pl2, tol=0.5):
    """返回 pl1 与 pl2 共线且重叠的区段。"""
    def coords_to_xy_pairs(coords):
        pairs = []
        for i in range(0, len(coords) - 1, 2):
            pairs.append((coords[i], coords[i + 1]))
        return pairs

    def build_segments(verts, closed=False):
        segs = []
        for i in range(len(verts) - 1):
            segs.append([verts[i], verts[i + 1]])
        if closed and len(verts) > 2:
            segs.append([verts[-1], verts[0]])
        return segs

    def dist(p, q):
        return math.hypot(p[0] - q[0], p[1] - q[1])

    def colinear(p, q, r):
        return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) <= tol * max(dist(p, q), dist(p, r), dist(q, r), 1)

    def segment_overlap(seg_a, seg_b):
        (p1, p2), (q1, q2) = seg_a, seg_b
        if not (colinear(p1, p2, q1) and colinear(p1, p2, q2)):
            return None
        axis = 0 if abs(p2[0] - p1[0]) >= abs(p2[1] - p1[1]) else 1
        a1, a2 = p1[axis], p2[axis]
        b1, b2 = q1[axis], q2[axis]
        if a1 > a2:
            p1, p2 = p2, p1
            a1, a2 = a2, a1
        if b1 > b2:
            q1, q2 = q2, q1
            b1, b2 = b2, b1
        left, right = max(a1, b1), min(a2, b2)
        if right - left <= tol:
            return None
        def interp(t):
            return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
        len_p = a2 - a1 if a2 != a1 else 1e-9
        pa = interp((left - a1) / len_p)
        pb = interp((right - a1) / len_p)
        return pa, pb

    v1 = coords_to_xy_pairs(pl1.Coordinates)
    v2 = coords_to_xy_pairs(pl2.Coordinates)
    if getattr(pl1, "Closed", False) and v1 and v1[0] != v1[-1]:
        v1.append(v1[0])
    if getattr(pl2, "Closed", False) and v2 and v2[0] != v2[-1]:
        v2.append(v2[0])
    segs1 = build_segments(v1, closed=False)
    segs2 = build_segments(v2, closed=False)
    overlaps = []
    for s1 in segs1:
        for s2 in segs2:
            ov = segment_overlap(s1, s2)
            if ov:
                pa, pb = ov
                overlaps.append([(pa[0], pa[1], 0.0), (pb[0], pb[1], 0.0)])
                break
    return overlaps


# 两多段线组成矩形
#&&% two_polylines_form_rectangle

def two_polylines_form_rectangle(pl1, pl2, tol=0.5):
    """判断两条正交多段线拼在一起是否形成矩形。"""
    def same_point(a, b, tol):
        return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol

    def pline_vertices(pl):
        c = pl.Coordinates
        verts = []
        for i in range(0, len(c), 2):
            verts.append((c[i], c[i + 1]))
        if not same_point(verts[0], verts[-1], tol):
            verts.append(verts[0])
        return verts

    def poly_area(verts):
        s = 0
        for i in range(len(verts) - 1):
            x1, y1 = verts[i]
            x2, y2 = verts[i + 1]
            s += x1 * y2 - x2 * y1
        return abs(s) * 0.5

    def collect_segments(verts):
        segs = []
        for i in range(len(verts) - 1):
            segs.append((verts[i], verts[i + 1]))
        return segs

    def covers_edge(edge, segs):
        (x0, y0), (x1, y1) = edge
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        if L < tol:
            return False
        ux, uy = dx / L, dy / L
        intervals = []
        for (ax, ay), (bx, by) in segs:
            cross = (ax - x0) * dy - (ay - y0) * dx
            if abs(cross) > tol * L:
                continue
            t1 = (ax - x0) * ux + (ay - y0) * uy
            t2 = (bx - x0) * ux + (by - y0) * uy
            a, b = min(t1, t2), max(t1, t2)
            if b < -tol or a > L + tol:
                continue
            intervals.append((max(0.0, a), min(L, b)))
        if not intervals:
            return False
        intervals.sort(key=lambda iv: iv[0])
        cur_start, cur_end = intervals[0]
        for a, b in intervals[1:]:
            if a > cur_end + tol:
                return False
            cur_end = max(cur_end, b)
        return (cur_start <= tol) and (cur_end >= L - tol)

    v1 = pline_vertices(pl1)
    v2 = pline_vertices(pl2)
    A1 = poly_area(v1)
    A2 = poly_area(v2)
    xs = [p[0] for p in v1[:-1]] + [p[0] for p in v2[:-1]]
    ys = [p[1] for p in v1[:-1]] + [p[1] for p in v2[:-1]]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    A_bbox = (xmax - xmin) * (ymax - ymin)
    if abs((A1 + A2) - A_bbox) > tol:
        return False
    bbox_edges = [
        ((xmin, ymin), (xmax, ymin)),
        ((xmax, ymin), (xmax, ymax)),
        ((xmax, ymax), (xmin, ymax)),
        ((xmin, ymax), (xmin, ymin)),
    ]
    segs = collect_segments(v1) + collect_segments(v2)
    hits = 0
    for edge in bbox_edges:
        if covers_edge(edge, segs):
            hits += 1
    return hits == 4

