# -*- coding: utf-8 -*-
# 文件位置: D:/claude-tasks/cad/scripts/CAD_coordination.py V10
"""
CAD运行协同机制模块

实现CAD命令的同步等待、文档打开等待、空闲状态检测等协同机制
核心升级：
1. 全面接入 common_logger 日志系统
2. wait_quiescent 融合了 COM 阻塞探测与 CMDACTIVE 检查
"""

import time
import subprocess
import sys
import os
import psutil
import pythoncom
import win32com.client
import inspect
from pathlib import Path

# ================= 1. 路径与日志配置 =================
# 获取当前文件绝对路径
CURRENT_FILE = Path(__file__).resolve()
SYSTEM_DIR = CURRENT_FILE.parent.parent / "system"  # .../cad/system
SCRIPTS_DIR = CURRENT_FILE.parent                   # .../cad/scripts

# 注入路径
for p in [str(SYSTEM_DIR), str(SCRIPTS_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# 引入统一日志模块
try:
    from common_logger import sys_logger
except ImportError:
    import logging
    sys_logger = logging.getLogger("Fallback")
    sys_logger.addHandler(logging.NullHandler())
    print("⚠️ 警告: 未找到 common_logger，日志功能已降级。")

# ================= 2. 核心协同函数 =================

def wait_quiescent(min_quiet: float = 0.5, timeout: float = 30.0) -> bool:
    """
    【终极版】等待 CAD 进入完全空闲状态
    
    融合特性：
    1. 智能 COM 探测: 将 'Call rejected' 视为 CAD 忙碌而非错误
    2. 双重变量检查: 结合 CMDACTIVE (状态位) 和 CMDNAMES (命令栈)
    3. 消息泵防死锁: 保持 Windows 消息循环畅通
    
    Returns:
        bool: True=成功空闲, False=超时
    """
    # 获取调用者名称，方便调试
    try: caller_name = inspect.stack()[1].function
    except: caller_name = "Unknown"

    # 1. 连接 CAD (仅附着)
    try:
        pythoncom.CoInitialize()
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        doc = acad.ActiveDocument
    except Exception as e:
        sys_logger.error(f"[{caller_name}] 无法连接 CAD (wait_quiescent): {e}")
        return False

    start_time = time.time()
    last_busy_time = time.time()
    has_really_waited = False
    
    # 【防坑】刚进函数先睡一小会儿
    time.sleep(0.1)

    while True:
        # 2. 防死锁：刷新消息泵
        try: pythoncom.PumpWaitingMessages()
        except: pass

        current_time = time.time()
        
        # --- 核心探测区 ---
        is_busy = False
        status_desc = "Idle"

        try:
            # 尝试读取 CAD 状态
            # 如果 CAD 极度繁忙 (如渲染/保存)，这里会直接抛出 COM Exception
            cmd_active = int(doc.GetVariable("CMDACTIVE"))
            cmd_names = doc.GetVariable("CMDNAMES")
            
            if cmd_active > 0 or cmd_names != "":
                is_busy = True
                status_desc = f"Active({cmd_active})Cmd({cmd_names})"
                
        except Exception:
            # 捕获到 COM 异常，说明 CAD 忙得连话都说不出来 (例如模态对话框阻塞)
            # 此时视为“忙碌”，而不是“出错”
            is_busy = True
            status_desc = "COM_BLOCKING"
            
        # --- 逻辑判断区 ---
        if is_busy:
            last_busy_time = current_time
            has_really_waited = True
            
            # 超时判断
            if current_time - start_time > timeout:
                sys_logger.error(f"[{caller_name}] 等待超时({timeout}s)! 最后状态: {status_desc}")
                return False
        else:
            # 当前看起来空闲，检查持续时间 (去抖动)
            quiet_duration = current_time - last_busy_time
            if quiet_duration >= min_quiet:
                total_time = current_time - start_time
                # 只有等待时间较长时才记录日志，避免刷屏
                if has_really_waited and total_time > 1.0:
                    sys_logger.info(f"[{caller_name}] CAD恢复空闲. 耗时: {total_time:.2f}s")
                return True

        # 轮询间隔
        time.sleep(0.1)

#新版20260109
def wait_quiescent(min_quiet: float = 0.5, timeout: float = 60.0) -> bool:
    """
    【终极加强版】等待 CAD 进入完全空闲状态
    
    修复：增加了"启动等待期"。
    当 CAD 刚启动时，GetActiveObject 会报错，本函数现在会轮询直到连上为止，
    而不是直接报错退出。
    """
    # 获取调用者名称，方便调试
    try: caller_name = inspect.stack()[1].function
    except: caller_name = "Unknown"

    start_time = time.time()
    
    # ================= 阶段 1: 顽强连接 (新增) =================
    # 刚启动时 CAD 会拒绝连接，必须死皮赖脸地重试
    acad = None
    doc = None
    
    # 连接超时通常给 20-30 秒足够了
    connect_timeout = max(20.0, timeout) 
    
    while time.time() - start_time < connect_timeout:
        try:
            pythoncom.PumpWaitingMessages() # 防死锁
            acad = win32com.client.GetActiveObject("AutoCAD.Application")
            doc = acad.ActiveDocument
            # 尝试读一个属性，确保是真的连上了
            _ = doc.Name 
            break # 成功连上，跳出连接循环
        except Exception:
            # 还没准备好，歇一会继续试
            time.sleep(1.0)
            
    if acad is None or doc is None:
        sys_logger.error(f"[{caller_name}] 致命错误: 无法连接 CAD (启动超时?)")
        return False

    # ================= 阶段 2: 空闲检测 (原有逻辑) =================
    
    # 重置计时器，开始算空闲时间
    # 注意：timeout 要减去刚才连接消耗的时间，或者重新给一个 timeout
    # 这里我们重新计时，保证足够的空闲检测时间
    phase2_start = time.time()
    last_busy_time = time.time()
    has_really_waited = False
    
    # 【防坑】连接成功后，先睡一小会儿，让 CAD 喘口气
    time.sleep(0.5)

    while True:
        try: pythoncom.PumpWaitingMessages()
        except: pass

        current_time = time.time()
        
        # --- 核心探测区 ---
        is_busy = False
        status_desc = "Idle"

        try:
            cmd_active = int(doc.GetVariable("CMDACTIVE"))
            cmd_names = doc.GetVariable("CMDNAMES")
            
            if cmd_active > 0 or cmd_names != "":
                is_busy = True
                status_desc = f"Active({cmd_active})Cmd({cmd_names})"
                
        except Exception:
            is_busy = True
            status_desc = "COM_BLOCKING"
            
        # --- 逻辑判断区 ---
        if is_busy:
            last_busy_time = current_time
            has_really_waited = True
            
            if current_time - phase2_start > timeout:
                sys_logger.error(f"[{caller_name}] 等待空闲超时({timeout}s)! 最后状态: {status_desc}")
                return False
        else:
            quiet_duration = current_time - last_busy_time
            if quiet_duration >= min_quiet:
                # 成功
                return True

        time.sleep(0.1)


def wait_document_opened(path: str, timeout: float = 120.0) -> bool:
    """等待文档被CAD完全打开并加入Documents集合"""
    try:
        start_time = time.time()
        target_path = os.path.abspath(path).lower()
        target_name = os.path.basename(target_path).lower()

        while time.time() - start_time < timeout:
            try:
                acad = win32com.client.GetActiveObject("AutoCAD.Application")
                documents = acad.Documents
                count = documents.Count

                for i in range(count):
                    try:
                        doc = documents.Item(i)
                        doc_path = doc.FullName.lower() if doc.FullName else ""
                        doc_name = os.path.basename(doc_path).lower()

                        # 检查路径匹配 或 文件名匹配
                        if doc_path == target_path or doc_name == target_name:
                            time.sleep(0.5) # 额外等待确保加载完毕
                            sys_logger.info(f"文档已就绪: {doc_name}")
                            return True
                    except: continue

            except Exception: pass
            time.sleep(0.5)

        sys_logger.warning(f"等待文档打开超时: {path}")
        return False

    except Exception as e:
        sys_logger.error(f"等待文档打开时出错: {e}")
        return False


def send_cmd_with_sync(cmd: str, wait_after: float = 0.3, timeout: float = 30.0) -> bool:
    """
    发送CAD命令并同步等待执行完成
    约定：仅附着已有 AutoCAD 实例，不主动新建CAD进程
    """
    try:
        pythoncom.CoInitialize()
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        
        # 激活窗口，防止命令因失去焦点失效
        try:
            if not acad.Visible: acad.Visible = True
        except: pass
        
        doc = acad.ActiveDocument
        if not doc:
            sys_logger.error("发送命令失败: 当前无活动文档")
            return False

        # 格式化命令
        formatted_cmd = cmd if cmd.endswith("\n") else (cmd + "\n")
        
        # 发送
        doc.SendCommand(formatted_cmd)
        
        # 记录简略日志 (去掉换行符)
        sys_logger.info(f"发送指令: {cmd.strip()}")

        # 基础等待，让命令进入队列
        time.sleep(wait_after)

        # 调用终极版等待函数
        return wait_quiescent(timeout=timeout)

    except Exception as e:
        sys_logger.error(f"发送指令失败 [{cmd.strip()}]: {e}")
        return False

# ================= 3. 进程与启动管理 =================

DETACHED_PROCESS = 0x00000008

def start_cad_with_dialog_killer() -> bool:
    """启动CAD并运行弹窗治理脚本"""
    try:
        # 导入CAD_basic模块中的start_applicationV9函数
        # 注意：这里假设 CAD_basic 在同级目录
        try:
            from CAD_basic import start_applicationV9
        except ImportError:
            sys_logger.error("找不到 CAD_basic.start_applicationV9，无法启动CAD")
            return False

        sys_logger.info("正在启动天正CAD...")
        proc = start_applicationV9()
        if not proc:
            sys_logger.error("CAD启动失败")
            return False

        # 等待CAD启动初始化
        time.sleep(3.0)

        # 启动弹窗治理脚本
        dialog_killer_path = Path(__file__).parent / "cad_dialog_killer.py"
        if dialog_killer_path.exists():
            already_running = False
            for proc in psutil.process_iter(['pid', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline') or []
                    if any("cad_dialog_killer" in str(arg) for arg in cmdline):
                        already_running = True
                        break
                except: pass

            if not already_running:
                sys_logger.info("启动弹窗治理守护进程...")
                subprocess.Popen(
                    ["python", str(dialog_killer_path)],
                    creationflags=DETACHED_PROCESS
                )
                time.sleep(1.0)
            else:
                sys_logger.info("弹窗治理脚本已在运行")
        else:
            sys_logger.warning("弹窗治理脚本不存在，跳过启动")

        return True

    except Exception as e:
        sys_logger.error(f"启动CAD流程出错: {e}")
        return False


def ensure_single_process() -> bool:
    """确保只有一个CAD进程运行"""
    try:
        CAD_PROCESS_NAME = "acad.exe"
        processes = []

        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] and proc.info['name'].lower() == CAD_PROCESS_NAME:
                processes.append(proc)

        if len(processes) == 0:
            sys_logger.info("未发现运行中的CAD进程")
            return True
        elif len(processes) == 1:
            sys_logger.info("CAD进程状态正常 (单进程)")
            return True
        else:
            sys_logger.warning(f"发现 {len(processes)} 个CAD进程，正在清理多余进程...")
            
            # 保留第一个，关闭其余
            for proc in processes[1:]:
                pid = proc.info['pid']
                try:
                    proc.terminate()
                    sys_logger.info(f"已终止进程 PID: {pid}")
                except:
                    try:
                        proc.kill()
                        sys_logger.warning(f"已强制杀掉进程 PID: {pid}")
                    except Exception as e:
                        sys_logger.error(f"无法终止进程 PID: {pid} - {e}")

            time.sleep(1.0)
            return True

    except Exception as e:
        sys_logger.error(f"确保单进程失败: {e}")
        return False

# ================= 4. 测试入口 =================
if __name__ == "__main__":
    sys_logger.info("=== 开始测试 CAD 协同机制 ===")

    # 1. 确保环境
    ensure_single_process()

    # 2. 尝试连接或等待
    if wait_quiescent(timeout=5.0):
        sys_logger.info("CAD 当前处于空闲状态")
        
        # 3. 发送测试命令 (画一个圆)
        send_cmd_with_sync("_CIRCLE 0,0,0 100 ")
        sys_logger.info("测试命令执行完毕")
    else:
        sys_logger.warning("CAD 忙碌或未启动，跳过命令测试")

    sys_logger.info("=== 测试结束 ===")

# ================= 5. 兼容旧接口 (Compatibility) =================

def wait_command_done(timeout=300.0, poll_interval=0.1, quiet_time=0.5):
    """
    【兼容补丁】
    旧脚本调用 wait_command_done 时，自动转发给新架构的 wait_quiescent。
    
    参数映射:
        timeout       -> 传给 timeout
        quiet_time    -> 传给 min_quiet
        poll_interval -> (忽略) 新架构内部自动处理轮询间隔(0.1s)和消息泵
    """
    # 直接调用终极版等待函数
    return wait_quiescent(min_quiet=quiet_time, timeout=timeout)
    
