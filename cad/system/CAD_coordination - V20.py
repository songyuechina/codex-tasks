# -*- coding: utf-8 -*-
# 文件位置: D:/claude-tasks/cad/system/CAD_coordination.py
"""
CAD运行协同机制模块 (Licad + Logger 集成终极版)

1. 【连接】深度集成 licad.py，统一使用 C.acad/C.doc，确保连接唯一性。
2. 【日志】全面接入 common_logger.py，所有动作留痕。
3. 【稳健】提供 wait_quiescent 级的高级空闲检测。
"""
#V20
import time
import subprocess
import sys
import os
import psutil
import inspect
from pathlib import Path

# ================= 1. 路径环境配置 =================
# 锚定当前文件: .../cad/system/CAD_coordination.py
CURRENT_FILE = Path(__file__).resolve()
SYSTEM_DIR = CURRENT_FILE.parent           # .../cad/system
CAD_DIR = SYSTEM_DIR.parent                # .../cad
SCRIPTS_DIR = CAD_DIR / "scripts"          # .../cad/scripts

# 注入路径，确保能引用到 licad, common_logger 和 scripts 下的模块
for p in [str(SYSTEM_DIR), str(SCRIPTS_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ================= 2. 核心模块集成 =================

# 接入统一日志
try:
    from common_logger import sys_logger
except ImportError:
    print("❌ [严重错误] 找不到 common_logger.py")
    # 紧急降级，防止脚本直接崩溃
    import logging
    sys_logger = logging.getLogger("Fallback")

# 接入 Licad 连接池
try:
    # C: 全局代理对象, retry_on_busy: 装饰器
    from licad import C, retry_on_busy
    sys_logger.info("✅ 协同模块已加载 (集成 Licad + CommonLogger)")
except ImportError:
    sys_logger.critical("❌ [严重错误] 找不到 licad.py")
    C = None
    def retry_on_busy(func): return func

# ================= 3. 核心协同函数 =================

def wait_quiescent(min_quiet: float = 0.5, timeout: float = 60.0) -> bool:
    """
    【等待空闲】基于 Licad.C 的智能检测
    
    检测逻辑:
    1. 检查 C.doc 是否可用 (自动重连)。
    2. 检查 CMDACTIVE 系统变量 (是否在命令中)。
    3. 检查 CMDNAMES (是否有命令栈)。
    """
    # 获取调用者名字，方便在日志里排查是谁在等
    try: caller = inspect.stack()[1].function
    except: caller = "Unknown"

    start_time = time.time()
    last_busy_time = time.time()

    # 1. 初始连接检查
    if not C.doc:
        sys_logger.warning(f"[{caller}] 等待空闲失败: 无法获取 CAD 文档")
        return False

    while True:
        current_time = time.time()
        is_busy = False
        status_desc = "Idle"

        try:
            # 获取文档对象 (C.doc 属性会自动处理连接有效性)
            doc = C.doc
            
            if doc:
                # GetVariable 可能会因为 RPC 忙碌抛错，这正是我们需要的 busy 信号
                cmd_active = int(doc.GetVariable("CMDACTIVE"))
                cmd_names = doc.GetVariable("CMDNAMES")
                
                # CMDACTIVE > 0 表示有命令在运行 (如 PLOT, OPEN 等)
                if cmd_active > 0 or (cmd_names and str(cmd_names).strip() != ""):
                    is_busy = True
                    status_desc = f"Active({cmd_active})"
            else:
                # 连上了 App 但没文档，视为忙碌或不可用
                is_busy = True
                status_desc = "NoDoc"

        except Exception:
            # 任何 COM 报错 (RPC Rejected) 都视为忙碌
            is_busy = True
            status_desc = "COM_Block"

        # --- 判定逻辑 ---
        if is_busy:
            last_busy_time = current_time
            # 超时检查
            if current_time - start_time > timeout:
                sys_logger.error(f"[{caller}] 等待空闲超时({timeout}s)! 状态: {status_desc}")
                return False
        else:
            # 持续空闲时间达标
            if (current_time - last_busy_time) >= min_quiet:
                return True

        time.sleep(0.1)


@retry_on_busy # <--- 复用 licad 的装饰器，处理 RPC 拒绝
def send_cmd_with_sync(cmd: str, wait_after: float = 0.3, timeout: float = 30.0) -> bool:
    """
    【发送命令】带同步等待的命令发送
    
    1. 激活窗口
    2. 发送命令 (C.doc.SendCommand)
    3. 等待空闲 (wait_quiescent)
    """
    # 1. 窗口保活 (防止后台运行导致命令失效)
    try:
        if C.acad and not C.acad.Visible:
            C.acad.Visible = True
    except: pass

    # 2. 检查文档
    doc = C.doc
    if not doc:
        sys_logger.error(f"发送命令失败 [{cmd.strip()}]: 无活动文档")
        return False

    # 3. 格式化并发送
    try:
        real_cmd = cmd if cmd.endswith("\n") else (cmd + "\n")
        doc.SendCommand(real_cmd)
        sys_logger.info(f"CMD -> {cmd.strip()}")
    except Exception as e:
        sys_logger.error(f"发送异常: {e}")
        raise e # 抛出给 @retry_on_busy 处理

    # 4. 等待
    if wait_after > 0:
        time.sleep(wait_after)

    return wait_quiescent(timeout=timeout)


def wait_document_opened(path: str, timeout: float = 120.0) -> bool:
    """等待特定文档加载完成"""
    start_time = time.time()
    # 统一路径格式
    target_path = str(Path(path).resolve()).lower()
    target_name = Path(path).name.lower()

    sys_logger.info(f"等待文档: {target_name}")

    while time.time() - start_time < timeout:
        try:
            # 利用 C.acad 遍历文档
            app = C.acad
            if app:
                for i in range(app.Documents.Count):
                    d = app.Documents.Item(i)
                    d_full = str(Path(d.FullName).resolve()).lower()
                    
                    if d_full == target_path or Path(d_full).name.lower() == target_name:
                        sys_logger.info(f"✅ 文档已就绪: {target_name}")
                        return True
        except:
            pass # 忽略遍历过程中的 COM 错误
            
        time.sleep(0.5)

    sys_logger.warning(f"等待文档超时: {target_name}")
    return False

# ================= 4. 进程与启动 (保持独立) =================

def ensure_single_process() -> bool:
    """确保单进程 (保留最早启动的)"""
    try:
        targets = ["acad.exe", "zwcad.exe", "gcad.exe"]
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'create_time']):
            if p.info['name'] and p.info['name'].lower() in targets:
                procs.append(p)
        
        if not procs: return True
        
        # 按时间排序，保留老大
        procs.sort(key=lambda x: x.info['create_time'])
        
        if len(procs) > 1:
            sys_logger.warning(f"清理多余进程，保留 PID={procs[0].info['pid']}")
            for p in procs[1:]:
                try: p.terminate()
                except: pass
        
        return True
    except Exception as e:
        sys_logger.error(f"进程管理错误: {e}")
        return False

def start_cad_with_dialog_killer() -> bool:
    """启动 CAD (调用 scripts/CAD_basic.py)"""
    try:
        # 因为前面 sys.path 已经加了 SCRIPTS_DIR，这里可以直接导
        from CAD_basic import start_applicationV9
        
        sys_logger.info("正在启动 CAD...")
        if start_applicationV9():
            # 使用 wait_quiescent 智能等待初始化
            sys_logger.info("等待 CAD 初始化...")
            return wait_quiescent(timeout=45.0)
        return False
    except ImportError:
        sys_logger.error("找不到 CAD_basic，无法启动")
        return False
    except Exception as e:
        sys_logger.error(f"启动异常: {e}")
        return False

# ================= 5. 兼容接口 =================

def wait_command_done(timeout=300.0, poll_interval=None, quiet_time=0.5):
    """兼容旧代码的别名"""
    return wait_quiescent(min_quiet=quiet_time, timeout=timeout)

if __name__ == "__main__":
    sys_logger.info("--- 测试协同模块 ---")
    ensure_single_process()
    if wait_quiescent(timeout=5):
        send_cmd_with_sync("(princ \"System Ready\") ")
    else:
        sys_logger.warning("CAD 未就绪")
