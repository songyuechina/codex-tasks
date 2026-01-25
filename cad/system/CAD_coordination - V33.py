# -*- coding: utf-8 -*-
# 文件位置: D:/claude-tasks/cad/system/CAD_coordination.py
# 版本: V3.3 (修复循环引用导致的 NoneType 错误)
"""
CAD运行协同机制模块 (Licad + Logger 集成终极版)

1. 【连接】深度集成 licad.py，统一使用 C.acad/C.raw_doc。
2. 【日志】全面接入 common_logger.py。
3. 【稳健】提供 wait_quiescent 级的高级空闲检测。
4. 【修复】移除了对 licad 导入错误的掩盖，防止 C 变为 None。
"""



from system.CAD_com_utils import SafeCOM





from pywintypes import com_error  # 必须引入这个来识别具体的错误代码
import time
import subprocess
import sys
import os
import psutil
import inspect
from pathlib import Path

#  引导代码 (确保能找到 system)
import os
import sys
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))
from system.project_setup import PathConfig

# ================= 2. 核心模块集成 =================

# 接入统一日志
try:
    from system.common_logger import sys_logger
except ImportError:
    import logging
    sys_logger = logging.getLogger("Fallback")
    sys_logger.addHandler(logging.StreamHandler())

# 接入 Licad 连接池
# 🔥【关键修复】直接导入，不要用 try...except 吞噬错误！
# 配合 licad.py V2.5 的延迟导入修改，这里的循环引用已被打破。
from system.licad import C, retry_on_busy
sys_logger.info("✅ 协同模块已加载 (集成 Licad V2.5+)")

# ================= 3. 核心协同函数 =================



def wait_quiescent(min_quiet: float = 0.5, timeout: float = 60.0) -> bool:
    """
    【等待空闲】基于 Licad.C 的智能检测 (增强版)
    
    新增功能:
    1. 忙碌拦截计数 (busy_hits): 用于分析该等待是否多余。
    2. 精确错误处理: 识别 CAD 崩溃、断开连接、用户中止，避免无意义的死等。

    原有的“去抖动”逻辑和“绕过 Wrapper 直接访问 raw_doc”的核心思想，并植入了两个关键升级：

    效能监测：增加 busy_hits 计数器，并在日志中告诉你这次等待是否真的拦截到了忙碌状态（判断是否多余）。

    安全熔断：引入了我们之前讨论的 com_error 精确识别，防止在 CAD 崩溃时死等 60 秒

    涉及视口切换 / 重生成 (Regen)触发了 LISP 的操作
    Plot / Publish: 某些打印操作,doc.PostCommand(...)
    doc.SendCommand

    """
    try: caller = inspect.stack()[1].function
    except: caller = "Unknown"

    start_time = time.time()
    last_busy_time = time.time()
    
    # === 新增：忙碌计数器 ===
    # 记录在等待期间检测到 CAD 忙碌的次数
    busy_hits = 0 

    # 1. 初始连接检查
    if not hasattr(C, 'raw_doc') or not C.raw_doc:
        sys_logger.warning(f"[{caller}] 等待失败: 无法获取 CAD 文档 (C.raw_doc is None)")
        return False

    # === 错误代码常量 (为了代码可读性) ===
    ERR_CRASH = -2147023174       # RPC服务器不可用 (CAD崩溃)
    ERR_DISCONNECT = -2147417848  # 对象已断开 (图纸关闭)
    ERR_ABORT = -2147467260       # 操作中止 (用户按Esc)

    while True:
        current_time = time.time()
        is_busy = False
        status_desc = "Idle"

        try:
            # 使用原始对象进行检测
            doc = C.raw_doc
            
            if doc:
                # GetVariable 可能会因为 RPC 忙碌抛错
                cmd_active = int(doc.GetVariable("CMDACTIVE"))
                cmd_names = doc.GetVariable("CMDNAMES")
                
                # CMDACTIVE > 0 表示有命令在运行
                if cmd_active > 0 or (cmd_names and str(cmd_names).strip() != ""):
                    is_busy = True
                    status_desc = f"Active({cmd_active})"
            else:
                is_busy = True
                status_desc = "NoDoc"

        except com_error as e:
            hresult = e.args[0]
            
            # === 增强：致命错误熔断机制 ===
            if hresult == ERR_CRASH:
                sys_logger.critical(f"[{caller}] 检测到 CAD 进程已崩溃/消失！停止等待。")
                return False # 或者 raise SystemExit
            
            elif hresult == ERR_DISCONNECT:
                sys_logger.error(f"[{caller}] 图纸对象已失效，无法检测状态。")
                return False
                
            elif hresult == ERR_ABORT:
                sys_logger.warning(f"[{caller}] 检测到中断信号 (ESC)。")
                return False # 或者 raise KeyboardInterrupt

            # 其他常规 COM 错误 (如 -2147418111 忙拒绝) 视为忙碌，继续等待
            is_busy = True
            status_desc = f"COM_Block({hresult})"

        except Exception as e:
            # 其他未知 Python 错误
            is_busy = True
            status_desc = "Unknown_Err"

        # --- 判定逻辑 ---
        if is_busy:
            # === 计数器 +1 ===
            busy_hits += 1
            
            last_busy_time = current_time
            if current_time - start_time > timeout:
                sys_logger.error(f"[{caller}] 等待超时({timeout}s)! {status_desc}")
                return False
        else:
            # 只有持续空闲超过 min_quiet 才算通过
            if (current_time - last_busy_time) >= min_quiet:
                
                # === 结束时的统计汇报 ===
                total_cost = current_time - start_time
                
                if busy_hits == 0:
                    # 场景 A: 全程没忙过 -> 这个 wait 可能没必要，或者 min_quiet 设置太长
                    sys_logger.debug(f"[{caller}] 等待通过(无痛): {total_cost:.2f}s | 拦截: 0 (全程空闲)")
                else:
                    # 场景 B: 确实等到了忙碌结束 -> 这个 wait 发挥了关键作用
                    sys_logger.info(f"[{caller}] 等待通过(有效): {total_cost:.2f}s | 拦截: {busy_hits} 次 | 状态: {status_desc}")
                
                return True

        time.sleep(0.1)


# =================================================================
# 🌟 CADGuard 上下文管理器V5.0
# =================================================================
# 引入静默等待
try:
    from system.CAD_coordination import wait_quiescent
except ImportError:
    # 防止循环导入，如果 wait_quiescent 就在本文件下方定义，这里不需要
    pass

class CADGuard:
    """
    【CAD 事务守卫 V5.0 - 局部回滚增强版】
    
    新增参数:
    independent_undo (bool): 
        - False (默认): "融合模式"。不创建新的 Undo 标记，与外层共生。
        - True: "独立模式"。创建独立的 Undo 子组。如果出错，只回滚自己，不影响外层。
    """
    
    _nesting_depth = 0
    
    def __init__(self, 
                 task_name="CAD操作", 
                 wait_before=True, 
                 wait_after=True, 
                 timeout=30.0, 
                 disable_ui=True,
                 independent_undo=False): # <--- 新增参数
        
        self.task_name = task_name
        self.wait_before = wait_before
        self.wait_after = wait_after
        self.timeout = timeout
        self.disable_ui = disable_ui
        self.independent_undo = independent_undo # <--- 记录参数
        
        self.doc = None
        self.start_time = 0
        self.is_root = False
        self.should_create_mark = False # 内部决策标志

    def __enter__(self):
        self.start_time = time.time()
        
        # 1. 深度管理
        if CADGuard._nesting_depth == 0:
            self.is_root = True
            sys_logger.info(f"🔰 [主事务开始] {self.task_name}")
        else:
            self.is_root = False
            # 根据模式显示不同的日志
            tag = "🔹 [独立子事务]" if self.independent_undo else "  🔻 [融合子事务]"
            sys_logger.info(f"{tag} {self.task_name}")
            
        CADGuard._nesting_depth += 1

        # 2. 连接检查
        if not C.li():
            raise RuntimeError("CAD 未连接")
        self.doc = C.doc

        # 3. 前置等待 (建议每一层都做，为了安全)
        if self.wait_before:
            try:
                from system.CAD_coordination import wait_quiescent
                wait_quiescent(min_quiet=0.5, timeout=self.timeout)
            except: pass

        # 4. 决策：是否开启 Undo 标记？
        # 规则：如果是根事务，或者用户显式要求独立，则开启
        if self.is_root or self.independent_undo:
            self.should_create_mark = True
            try: self.doc.StartUndoMark()
            except: pass
        else:
            self.should_create_mark = False

        # 5. UI 控制：依然只有根事务才有权关屏幕 (避免内层乱开)
        if self.is_root and self.disable_ui:
            try: C.app.Visible = True 
            except: pass

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        CADGuard._nesting_depth -= 1
        
        # ============================================
        # 异常处理 (局部回滚的核心逻辑)
        # ============================================
        if exc_type:
            sys_logger.error(f"❌ 事务异常: {self.task_name} ({exc_val})")
            
            # 只有当这是个“有标记”的事务时，我们才执行回滚
            if self.should_create_mark:
                # 先结束标记，形成闭环
                try: 
                    if self.doc: self.doc.EndUndoMark()
                except: pass
                
                # 🔥 执行局部回滚！
                # 发送 "U" 命令，只会撤销最近的一组 Start/End，也就是当前这一层
                try:
                    sys_logger.warning(f"🔄 正在回滚局部事务: {self.task_name}")
                    if self.doc: self.doc.SendCommand("_U\n")
                except: pass
            
            # 如果是根节点，需要重置深度并刷新屏幕
            if self.is_root:
                CADGuard._nesting_depth = 0
                try: self.doc.Regen(1)
                except: pass
            
            # 这里有个策略选择：
            # 如果是独立事务，我们回滚了自己，是否还需要抛出异常打断外层？
            # 通常：抛出异常让外层知道子任务失败了
            return False 

        else:
            # ============================================
            # 正常结束
            # ============================================
            sys_logger.info(f"✅ 完成: {self.task_name}")
            
            # 只有创建了标记的，才需要结束标记
            if self.should_create_mark:
                try: 
                    if self.doc: self.doc.EndUndoMark()
                except: pass

            # 只有根节点负责恢复 UI
            if self.is_root:
                try:
                    if self.disable_ui and self.doc: C.app.Update()
                except: pass
                
                # 后置等待
                if self.wait_after:
                    try:
                        from system.CAD_coordination import wait_quiescent
                        wait_quiescent(min_quiet=0.5, timeout=self.timeout)
                    except: pass
            
            return True


# =========================================================================
# 门神二号：FileGuard (物理/文件级保护)
# =========================================================================
class FileGuard:
    """
    【文件级卫士】
    负责：物理备份、强杀进程、文件覆盖回滚
    """
    def __init__(self, file_path):
        self.file_path = Path(file_path).resolve()
        # 备份文件名为: 原名.bak_safety
        self.backup_path = self.file_path.with_suffix(self.file_path.suffix + ".bak_safety")
        self.success = False 

    def __enter__(self):
        sys_logger.info(f"💾 [文件备份] 创建副本: {self.file_path.name}")
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"原文件不存在: {self.file_path}")

        try:
            # 复制原文件到备份路径
            shutil.copy2(self.file_path, self.backup_path)
        except Exception as e:
            sys_logger.error(f"❌ 备份失败: {e}")
            raise
        return self

    def set_success(self):
        """显式标记为成功"""
        self.success = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.success and exc_type is None:
            # --- 成功：清理备份 ---
            sys_logger.info("✅ [文件安全] 操作成功，清理临时备份。")
            try:
                if self.backup_path.exists():
                    os.remove(self.backup_path)
            except: pass
        else:
            # --- 失败：执行回滚 ---
            sys_logger.error(f"❌ [文件回滚] 任务失败/校验未通过 (原因: {exc_val})")
            sys_logger.warning("🔄 正在执行物理级回滚 (强杀 CAD -> 覆盖文件)...")

            # -------------------------------------------------------
            # ⚠️ 关键点：延迟导入，防止循环引用
            # -------------------------------------------------------
            try:
                # 假设 close_all_cad_processes 在 scripts.CAD_basic 中
                from scripts.CAD_basic import close_all_cad_processes
                close_all_cad_processes()
            except ImportError:
                sys_logger.critical("💀 无法导入 close_all_cad_processes，回滚可能因文件占用而失败！")
            except Exception as e:
                sys_logger.error(f"关闭 CAD 进程失败: {e}")

            # 等待进程释放锁
            time.sleep(1.5) 

            # 覆盖恢复
            try:
                if self.backup_path.exists():
                    # 使用 move 将备份文件移回原位 (覆盖)
                    shutil.move(str(self.backup_path), str(self.file_path))
                    sys_logger.info(f"✅ 已恢复原文件: {self.file_path.name}")
                else:
                    sys_logger.critical("💀 灾难！备份文件丢失，无法恢复！")
            except Exception as e:
                sys_logger.critical(f"💀 回滚失败 (文件可能仍被占用): {e}")

# =========================================================================
# 门神三号：安全循环 (把上面两个串起来)
# =========================================================================
def run_safety_loop(target_dwg, action_func, check_func, max_retries=3):
    """
    【核弹级安全执行循环】
    自动调度 FileGuard 进行重试

    from functools import partial # 需导入

    # 1. 准备参数
    my_polylines = [...] 
    tpl_path = str(userpath / "dwg文件/标准图签.dwg")

    # 2. 制作“偏函数”
    # 语法: partial(函数名, 参数1, 参数2...)
    # 它会返回一个新的函数，这个新函数已经不需要传参了
    action_wrapper = partial(
        insert_and_scale_labels_area_any, 
        coms_dayin=my_polylines, 
        filepath=tpl_path
    )

    check_wrapper = partial(verify_blocks_exist, "A3-H")

    # 3. 传入
    run_safety_loop(
        target_dwg=work_dwg,
        action_func=action_wrapper,
        check_func=check_wrapper,
        max_retries=3
    )

    """
    target_dwg = Path(target_dwg)
    
    # 在这里导入打开文件的函数
    from scripts.CAD_basic import open_file
    
    for i in range(1, max_retries + 1):
        sys_logger.info(f"\n🔁 [第 {i}/{max_retries} 次尝试] {target_dwg.name}")
        
        try:
            # 1. 物理备份
            with FileGuard(target_dwg) as file_guard:
                
                # 2. 确保文件打开 (如果是回滚后的重试，CAD是关着的)
                open_file(str(target_dwg))
                
                # 3. 执行业务 (内部通常有 CADGuard)
                sys_logger.info("▶ 开始执行...")
                action_func()
                
                # 4. 校验
                sys_logger.info("▶ 结果校验...")
                if check_func():
                    file_guard.set_success()
                    sys_logger.info("✨ 任务完成！")
                    return True
                else:
                    raise RuntimeError("结果校验不通过")

        except Exception as e:
            sys_logger.warning(f"⚠️ 尝试 {i} 失败: {e}")
            if i < max_retries:
                time.sleep(2)
            else:
                sys_logger.error("🚫 达到最大重试次数，放弃。")
    
    return False


# ================= 3.1 常用功能 =================

@retry_on_busy
def send_cmd_with_sync(cmd: str, wait_after: float = 0.3, timeout: float = 30.0) -> bool:
    """
    【发送命令】带同步等待
    ⚠️ 必须使用 C.raw_doc 防止死锁
    """
    try:
        if C.acad and not C.acad.Visible: C.acad.Visible = True
    except: pass

    # 获取原始对象
    doc = C.raw_doc 
    if not doc:
        sys_logger.error(f"发送失败 [{cmd.strip()}]: 无文档")
        return False

    try:
        real_cmd = cmd if cmd.endswith("\n") else (cmd + "\n")
        
        # 原生发送，不经过 Wrapper
        doc.SendCommand(real_cmd)
        
        sys_logger.info(f"CMD -> {cmd.strip()}")
    except Exception as e:
        sys_logger.error(f"发送异常: {e}")
        raise e

    if wait_after > 0: time.sleep(wait_after)
    return wait_quiescent(timeout=timeout)


def wait_document_opened(path: str, timeout: float = 120.0) -> bool:
    """等待文档加载"""
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
                        sys_logger.info(f"✅ 文档已就绪")
                        return True
        except: pass
        time.sleep(0.5)
    
    sys_logger.warning(f"等待超时: {target_name}")
    return False

# ================= 4. 进程与启动 =================

def ensure_single_process() -> bool:
    """进程清理"""
    try:
        targets = ["acad.exe", "zwcad.exe", "gcad.exe"]
        procs = sorted(
            [p for p in psutil.process_iter(['pid', 'name', 'create_time']) 
             if p.info['name'].lower() in targets],
            key=lambda x: x.info['create_time']
        )
        if len(procs) > 1:
            sys_logger.warning(f"清理多余进程，保留 PID={procs[0].info['pid']}")
            for p in procs[1:]:
                try: p.terminate()
                except: pass
        return True
    except: return False

def start_cad_with_dialog_killer() -> bool:
    """启动 CAD"""
    try:
        from CAD_basic import start_applicationV9
        sys_logger.info("启动 CAD...")
        if start_applicationV9():
            return wait_quiescent(timeout=45.0)
        return False
    except: return False

# ================= 5. 兼容接口 =================
def wait_command_done(timeout=300.0, poll_interval=None, quiet_time=0.5):
    return wait_quiescent(min_quiet=quiet_time, timeout=timeout)

if __name__ == "__main__":
    sys_logger.info("--- 测试协同模块 V3.2 ---")
    if ensure_single_process() and wait_quiescent(timeout=5):
        with CADGuard("测试操作"):
            send_cmd_with_sync("(princ \"System Ready\") ")
    else:
        sys_logger.warning("CAD 未就绪")
