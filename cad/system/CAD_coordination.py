# -*- coding: utf-8 -*-
# 文件位置: D:/codex-tasks/cad/system/CAD_coordination.py
# 版本: V4.0
"""
CAD_coordination.py（收束版）

定位：
- 基于 licad.C 的高层协同层
- 负责：等待空闲、事务守卫、文件回滚、安全循环、命令同步
- 不负责：项目引导、全局日志初始化、CAD 连接主入口

原则：
1. CAD 连接入口统一由 system.licad 的 C 提供
2. 本模块只做“协同与保护”
3. 高风险操作用 sys_logger 记录，失败路径清晰
4. 尽量避免历史自引用、旧式 sys.path 引导、杂散 import

说明：
- 本文件不是最终完美版，而是按当前系统规则收束后的稳定骨架版
- 目标是便于后续 Codex 基于真实案例继续定位与迭代
"""

from __future__ import annotations

import inspect
import os
import shutil
import subprocess
import time
from functools import partial
from pathlib import Path
from typing import Any, Callable, Optional

import psutil

from system.common_logger import sys_logger
from system.licad import C, retry_on_busy


sys_logger.info("✅ 协同模块已加载 (集成 licad)")  # 模块级单条信息，便于排查加载链


# =========================================================================
# 1. 等待 CAD 空闲
# =========================================================================
def wait_quiescent(min_quiet: float = 0.5, timeout: float = 60.0) -> bool:
    """
    等待 CAD 真正进入空闲状态。

    判定逻辑：
    - 使用 C.raw_doc 读取 CMDACTIVE / CMDNAMES
    - 读取失败视为“忙碌/被 COM 阻塞”，而不是立即判死
    - 连续静默 min_quiet 秒后视为通过
    """
    try:
        caller = inspect.stack()[1].function
    except Exception:
        caller = "Unknown"

    start_time = time.time()
    last_busy_time = start_time
    busy_hits = 0

    if not getattr(C, "raw_doc", None):
        sys_logger.warning(f"[{caller}] 等待失败: 无法获取 CAD 文档")
        return False

    while True:
        now = time.time()
        is_busy = False
        status_desc = "Idle"

        try:
            doc = C.raw_doc
            if not doc:
                is_busy = True
                status_desc = "NoDoc"
            else:
                cmd_active = int(doc.GetVariable("CMDACTIVE"))
                cmd_names = doc.GetVariable("CMDNAMES")
                if cmd_active > 0 or (cmd_names and str(cmd_names).strip() != ""):
                    is_busy = True
                    status_desc = f"Active({cmd_active})"
        except Exception:
            is_busy = True
            status_desc = "COM_Block"

        if is_busy:
            busy_hits += 1
            last_busy_time = now

            if now - start_time > timeout:
                sys_logger.error(f"[{caller}] 等待超时({timeout}s)! {status_desc}")
                return False
        else:
            if (now - last_busy_time) >= min_quiet:
                total_cost = now - start_time
                if busy_hits == 0:
                    sys_logger.info(f"[{caller}] 🟢 等待通过(无痛): {total_cost:.2f}s | 拦截: 0")
                else:
                    sys_logger.info(
                        f"[{caller}] 🟡 等待通过(有效): {total_cost:.2f}s | 拦截: {busy_hits} 次 | 状态: {status_desc}"
                    )
                return True

        time.sleep(0.1)


# =========================================================================
# 2. CAD 事务守卫
# =========================================================================
class CADGuard:
    """
    CAD 事务守卫。

    功能：
    - 进入前等待
    - 事务嵌套深度管理
    - Undo 标记控制
    - 异常时局部回滚
    - 根事务结束时刷新/后置等待
    """

    _nesting_depth = 0

    def __init__(
        self,
        task_name: str = "CAD操作",
        wait_before: bool = True,
        wait_after: bool = True,
        timeout: float = 30.0,
        disable_ui: bool = True,
        independent_undo: bool = False,
    ):
        self.task_name = task_name
        self.wait_before = wait_before
        self.wait_after = wait_after
        self.timeout = timeout
        self.disable_ui = disable_ui
        self.independent_undo = independent_undo

        self.doc = None
        self.start_time = 0.0
        self.is_root = False
        self.should_create_mark = False

    def __enter__(self):
        self.start_time = time.time()

        if CADGuard._nesting_depth == 0:
            self.is_root = True
            sys_logger.info(f"🔰 [主事务开始] {self.task_name}")
        else:
            self.is_root = False
            tag = "🔹 [独立子事务]" if self.independent_undo else "🔻 [融合子事务]"
            sys_logger.info(f"{tag} {self.task_name}")

        CADGuard._nesting_depth += 1

        if not C.li():
            raise RuntimeError("CAD 未连接")

        self.doc = C.doc

        if self.wait_before:
            wait_quiescent(min_quiet=0.5, timeout=self.timeout)

        if self.is_root or self.independent_undo:
            self.should_create_mark = True
            try:
                if self.doc:
                    self.doc.StartUndoMark()
            except Exception:
                pass
        else:
            self.should_create_mark = False

        if self.is_root and self.disable_ui:
            try:
                if C.app:
                    C.app.Visible = True
            except Exception:
                pass

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        CADGuard._nesting_depth -= 1

        if exc_type:
            sys_logger.error(f"❌ 事务异常: {self.task_name} ({exc_val})")

            if self.should_create_mark:
                try:
                    if self.doc:
                        self.doc.EndUndoMark()
                except Exception:
                    pass

                try:
                    sys_logger.warning(f"🔄 正在回滚局部事务: {self.task_name}")
                    if self.doc:
                        self.doc.SendCommand("_U\n")
                except Exception:
                    pass

            if self.is_root:
                CADGuard._nesting_depth = 0
                try:
                    if self.doc:
                        self.doc.Regen(1)
                except Exception:
                    pass

            return False

        sys_logger.info(f"✅ 完成: {self.task_name} | 耗时 {duration:.2f}s")

        if self.should_create_mark:
            try:
                if self.doc:
                    self.doc.EndUndoMark()
            except Exception:
                pass

        if self.is_root:
            try:
                if self.disable_ui and self.doc and C.app:
                    C.app.Update()
            except Exception:
                pass

            if self.wait_after:
                wait_quiescent(min_quiet=0.5, timeout=self.timeout)

        return True


# =========================================================================
# 3. 文件级保护
# =========================================================================
class FileGuard:
    """
    文件级卫士：
    - 进入时做物理备份
    - 失败时尝试关闭 CAD 并回滚原文件
    """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path).resolve()
        self.backup_path = self.file_path.with_suffix(self.file_path.suffix + ".bak_safety")
        self.success = False

    def __enter__(self):
        sys_logger.info(f"💾 [文件备份] 创建副本: {self.file_path.name}")

        if not self.file_path.exists():
            raise FileNotFoundError(f"原文件不存在: {self.file_path}")

        try:
            shutil.copy2(self.file_path, self.backup_path)
        except Exception as e:
            sys_logger.error(f"❌ 备份失败: {e}")
            raise
        return self

    def set_success(self):
        self.success = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.success and exc_type is None:
            sys_logger.info("✅ [文件安全] 操作成功，清理临时备份。")
            try:
                if self.backup_path.exists():
                    os.remove(self.backup_path)
            except Exception:
                pass
            return False

        sys_logger.error(f"❌ [文件回滚] 任务失败/校验未通过 (原因: {exc_val})")
        sys_logger.warning("🔄 正在执行物理级回滚 (强杀 CAD -> 覆盖文件)...")

        try:
            from scripts.CAD_basic import close_all_cad_processes

            close_all_cad_processes()
        except ImportError:
            sys_logger.critical("💀 无法导入 close_all_cad_processes，回滚可能失败！")
        except Exception as e:
            sys_logger.error(f"关闭 CAD 进程失败: {e}")

        time.sleep(1.5)

        try:
            if self.backup_path.exists():
                shutil.move(str(self.backup_path), str(self.file_path))
                sys_logger.info(f"✅ 已恢复原文件: {self.file_path.name}")
            else:
                sys_logger.critical("💀 灾难！备份文件丢失，无法恢复！")
        except Exception as e:
            sys_logger.critical(f"💀 回滚失败 (文件可能仍被占用): {e}")

        return False


# =========================================================================
# 4. 安全执行循环
# =========================================================================
def run_safety_loop(
    target_dwg: str | Path,
    action_func: Callable[[], Any],
    check_func: Callable[[], bool],
    max_retries: int = 3,
) -> bool:
    """
    备份 -> 打开 -> 执行动作 -> 校验 -> 失败回滚 -> 重试

    说明：
    - action_func / check_func 建议由 partial 预先固化参数
    - 真正打开文件仍委托给脚本层 open_file（历史兼容）
    """
    target_dwg = Path(target_dwg)

    from scripts.CAD_basic import open_file

    for i in range(1, max_retries + 1):
        sys_logger.info(f"🔁 [第 {i}/{max_retries} 次尝试] {target_dwg.name}")

        try:
            with FileGuard(target_dwg) as file_guard:
                open_file(str(target_dwg))

                sys_logger.info("▶ 开始执行...")
                action_func()

                sys_logger.info("▶ 结果校验...")
                if check_func():
                    file_guard.set_success()
                    sys_logger.info("✨ 任务完成！")
                    return True

                raise RuntimeError("结果校验不通过")

        except Exception as e:
            sys_logger.warning(f"⚠️ 尝试 {i} 失败: {e}")
            if i < max_retries:
                time.sleep(2)
            else:
                sys_logger.error("🚫 达到最大重试次数，放弃。")

    return False


# =========================================================================
# 5. 命令同步与文档等待
# =========================================================================
@retry_on_busy
def send_cmd_with_sync(cmd: str, wait_after: float = 0.3, timeout: float = 30.0) -> bool:
    """
    发送命令并等待同步完成。
    必须使用 C.raw_doc，避免 wrapper/同步死锁。
    """
    try:
        if C.acad and not C.acad.Visible:
            C.acad.Visible = True
    except Exception:
        pass

    doc = C.raw_doc
    if not doc:
        sys_logger.error(f"发送失败 [{cmd.strip()}]: 无文档")
        return False

    try:
        real_cmd = cmd if cmd.endswith("\n") else (cmd + "\n")
        doc.SendCommand(real_cmd)
        sys_logger.info(f"CMD -> {cmd.strip()}")
    except Exception as e:
        sys_logger.error(f"发送异常: {e}")
        raise

    if wait_after > 0:
        time.sleep(wait_after)
    return wait_quiescent(timeout=timeout)


def wait_document_opened(path: str, timeout: float = 120.0) -> bool:
    """
    等待目标文档出现在 CAD Documents 集合中。
    """
    start_time = time.time()
    target_path = str(Path(path).resolve()).lower()
    target_name = Path(path).name.lower()

    sys_logger.info(f"等待文档: {target_name}")

    while time.time() - start_time < timeout:
        try:
            app = C.acad
            if app:
                for i in range(app.Documents.Count):
                    d = app.Documents.Item(i)
                    d_full = str(Path(d.FullName).resolve()).lower()
                    if d_full == target_path or Path(d_full).name.lower() == target_name:
                        sys_logger.info("✅ 文档已就绪")
                        return True
        except Exception:
            pass

        time.sleep(0.5)

    sys_logger.warning(f"等待超时: {target_name}")
    return False


# =========================================================================
# 6. 进程与启动辅助
# =========================================================================
def ensure_single_process() -> bool:
    """
    清理多余 CAD 进程，仅保留最早的一个。
    """
    try:
        targets = ["acad.exe", "zwcad.exe", "gcad.exe"]
        procs = sorted(
            [
                p
                for p in psutil.process_iter(["pid", "name", "create_time"])
                if p.info.get("name", "").lower() in targets
            ],
            key=lambda x: x.info["create_time"],
        )

        if len(procs) > 1:
            sys_logger.warning(f"清理多余进程，保留 PID={procs[0].info['pid']}")
            for p in procs[1:]:
                try:
                    p.terminate()
                except Exception:
                    pass

        return True
    except Exception as e:
        sys_logger.warning(f"ensure_single_process 异常: {e}")
        return False


def start_cad_with_dialog_killer() -> bool:
    """
    启动 CAD，并等待进入可用状态。
    说明：
    - 启动逻辑仍委托给历史脚本 start_applicationV9
    - 协同层只负责等待与收束
    """
    try:
        from scripts.CAD_basic import start_applicationV9

        sys_logger.info("启动 CAD...")
        if start_applicationV9():
            return wait_quiescent(timeout=45.0)
        return False
    except Exception as e:
        sys_logger.error(f"启动 CAD 失败: {e}")
        return False


# =========================================================================
# 7. 兼容接口
# =========================================================================
def wait_command_done(timeout: float = 300.0, poll_interval: Any = None, quiet_time: float = 0.5) -> bool:
    """
    兼容旧接口，映射到 wait_quiescent。
    poll_interval 参数保留但不使用。
    """
    _ = poll_interval
    return wait_quiescent(min_quiet=quiet_time, timeout=timeout)


__all__ = [
    "wait_quiescent",
    "CADGuard",
    "FileGuard",
    "run_safety_loop",
    "send_cmd_with_sync",
    "wait_document_opened",
    "ensure_single_process",
    "start_cad_with_dialog_killer",
    "wait_command_done",
]
