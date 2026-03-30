#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# D:/codex-tasks/cad/system/cad_command_monitor.py
# 版本 V6.0 (生产终极版 - 强制置顶抢焦)

import time
import win32gui, win32con, win32api
import win32com.client
import psutil
from pathlib import Path
import logging
import sys
import os
import pythoncom
import ctypes

# ================= 配置区 =================
TIMEOUT_THRESHOLD = 60   # 生产环境建议 60s
CHECK_INTERVAL    = 2    
HEARTBEAT_INTERVAL= 60   

# ================= 日志配置 =================
LOG_FILE = Path(__file__).parent / "cad_command_monitor.log"
logger = logging.getLogger("cad_monitor")
logger.setLevel(logging.INFO)
logger.handlers = [] 
formatter = logging.Formatter("%(asctime)s %(levelname)-5s %(message)s")

file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

LOCK_FILE = Path(__file__).parent / "cad_command_monitor.lock"

# ================= 窗口控制增强 =================
def force_bring_to_front(hwnd):
    """
    【霸道操作】强制将窗口置顶并获取焦点
    解决后台运行无法发送物理按键的问题
    """
    try:
        if not win32gui.IsWindow(hwnd):
            return False
            
        # 1. 如果最小化了，先还原
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.2)
            
        # 2. 欺骗 Windows 获取置顶权限 (模拟 Alt 键)
        # Windows 限制后台程序抢焦点，按一下 Alt 可以绕过
        ctypes.windll.user32.keybd_event(0x12, 0, 0, 0) # Alt Down
        ctypes.windll.user32.keybd_event(0x12, 0, 2, 0) # Alt Up
        
        # 3. 强制置前
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.2)
        return True
    except Exception as e:
        logger.error(f"抢占焦点失败: {e}")
        return False

def has_valid_cad_window(hwnd):
    """
    仅当拿到真实 CAD 窗口句柄时，才允许做前台窗口操作。
    hwnd=0 / None 或句柄失效时，一律视为无效。
    """
    return bool(hwnd) and win32gui.IsWindow(hwnd)

def send_nuclear_esc(hwnd, acad_doc):
    """
    先抢焦点，再按 ESC
    """
    logger.warning("☢️ [动作] 准备执行强制取消...")

    valid_hwnd = has_valid_cad_window(hwnd)
    if not valid_hwnd and acad_doc is None:
        logger.warning("   [安全保护] 未拿到有效 CAD 窗口/文档，跳过强制取消，避免误伤前台窗口。")
        return False

    try:
        # 步骤 1: 抢焦点 + 物理 ESC，仅在确认 CAD 主窗口有效时执行
        if valid_hwnd:
            logger.info("   [1/4] 正在将 CAD 窗口置顶...")
            brought = force_bring_to_front(hwnd)
            if brought:
                logger.info("   [2/4] 发送物理 ESC 连击...")
                for _ in range(3):
                    ctypes.windll.user32.keybd_event(0x1B, 0, 0, 0) # ESC Down
                    time.sleep(0.05)
                    ctypes.windll.user32.keybd_event(0x1B, 0, 2, 0) # ESC Up
                    time.sleep(0.1)
            else:
                logger.warning("   [安全保护] CAD 窗口置顶失败，跳过物理 ESC。")

        else:
            logger.warning("   [安全保护] CAD 窗口句柄无效，跳过物理 ESC / PostMessage。")

        # 步骤 3: 消息层 (兜底)
        if valid_hwnd:
            win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)
            win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0)

        # 步骤 4: 逻辑层 (如果 COM 还活着)
        if acad_doc:
            try:
                acad_doc.SendCommand(chr(27))
            except Exception as exc:
                logger.warning(f"   [逻辑层] SendCommand 发送 ESC 失败: {exc}")

        return valid_hwnd or acad_doc is not None
    except Exception as e:
        logger.error(f"发送失败: {e}")
        return False

def get_active_cad_app():
    try:
        pythoncom.CoInitialize()
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        return acad
    except Exception:
        return None

def analyze_state(acad):
    """
    V5.0+ 逻辑：吞掉 Call Rejected，判定为 BUSY
    """
    try:
        try:
            doc = acad.ActiveDocument
            hwnd = acad.HWND
        except:
            return 1, "CAD_BUSY_NO_DOC", 0, None

        try:
            cmd_active = doc.GetVariable("CMDACTIVE")
            cmd_names = doc.GetVariable("CMDNAMES")
            last_prompt = doc.GetVariable("LASTPROMPT")
        except pythoncom.com_error as e:
            if e.hresult == -2147418111:
                return 1, "CAD_BUSY_REJECTED", hwnd, doc
            else:
                return 2, str(e), hwnd, doc
        except Exception as e:
            return 2, str(e), hwnd, doc

        is_waiting = False
        if cmd_active > 0 and not (cmd_active & 8): is_waiting = True
        if cmd_names != "": is_waiting = True
        
        critical_keywords = ["指定", "选择", "输入", "确认", "接点", "搜索", "Select", "Specify", "Enter"]
        if last_prompt not in ["命令:", "Command:", ""]:
            for kw in critical_keywords:
                if kw in last_prompt:
                    is_waiting = True
                    break

        if is_waiting:
            display_name = cmd_names if cmd_names else f"CMD_({last_prompt[-10:].strip()})"
            return 1, display_name, hwnd, doc
            
        return 0, "", hwnd, doc
        
    except Exception as e:
        return 2, str(e), 0, None

def is_already_running():
    if not LOCK_FILE.exists(): return False
    try:
        pid = int(LOCK_FILE.read_text().strip())
        if psutil.pid_exists(pid):
            proc = psutil.Process(pid)
            if "python" in proc.name().lower() and "cad_command_monitor" in " ".join(proc.cmdline()):
                return True
    except: pass
    LOCK_FILE.unlink(missing_ok=True)
    return False

def create_lock(): LOCK_FILE.write_text(str(os.getpid()))
def remove_lock(): LOCK_FILE.unlink(missing_ok=True)

# ================= 主循环 =================
def main():

    if is_already_running():
        print(f"[{time.strftime('%H:%M:%S')}] ⛔ 检测到已有实例运行，为防止冲突，当前程序将退出。")
        return



    create_lock()
    
    print(f"\n{'='*50}")
    print(f"   CAD 命令超时监控器 V6.0 (霸道抢焦版)")
    print(f"   功能: 超时将强制置顶 CAD 窗口并发送 ESC")
    print(f"{'='*50}\n")
    
    logger.info("监控启动...")
    _stuck_record = {} 
    last_heartbeat_time = 0
    connected_once = False

    try:
        while True:
            start_loop_time = time.time()
            acad = get_active_cad_app()
            
            if not acad:
                if connected_once:
                    logger.warning("连接断开...")
                    connected_once = False
                    _stuck_record.clear()
                time.sleep(CHECK_INTERVAL)
                continue

            if not connected_once:
                try:
                    logger.info(f"✅ 已连接: [{win32gui.GetWindowText(acad.HWND)}]")
                    connected_once = True
                except: pass

            status, cmd_name, hwnd, doc = analyze_state(acad)
            current_time = time.time()
            key = hwnd if hwnd else 'default'

            if status == 1: # WAITING
                if key not in _stuck_record:
                    _stuck_record[key] = {"start": current_time, "cmd": cmd_name}
                    logger.info(f"🚨 [占用] '{cmd_name}'")
                else:
                    record = _stuck_record[key]
                    elapsed = current_time - record["start"]
                    
                    if (cmd_name != "CAD_BUSY_REJECTED" and record["cmd"] != "CAD_BUSY_REJECTED" and record["cmd"] != cmd_name):
                         logger.info(f"ℹ️ [切换] '{record['cmd']}' -> '{cmd_name}'")
                         _stuck_record[key] = {"start": current_time, "cmd": cmd_name}
                    
                    if elapsed < TIMEOUT_THRESHOLD:
                        sys.stdout.write(f"\r   ⏳ '{record['cmd']}' 已持续 {int(elapsed)}s / {TIMEOUT_THRESHOLD}s   ")
                        sys.stdout.flush()
                    else:
                        print("") 
                        logger.warning(f"⏰ [超时] '{record['cmd']}' 卡顿 {int(elapsed)}s")

                        if not has_valid_cad_window(hwnd) and doc is None:
                            logger.warning("🛑 [安全保护] 当前仅检测到 CAD_BUSY_NO_DOC，未拿到可操作目标，跳过取消动作。")
                        else:
                            # 执行 V6.0 核心：抢焦点 -> 按 ESC
                            send_nuclear_esc(hwnd, doc)
                        
                        logger.info("✨ 暂停监控 3 秒...")
                        _stuck_record.pop(key, None)
                        time.sleep(3.0) 
                        continue 

            else:
                if key in _stuck_record:
                    print("")
                    duration = current_time - _stuck_record[key]["start"]
                    logger.info(f"✅ [释放] '{_stuck_record[key]['cmd']}' (耗时 {int(duration)}s)")
                    _stuck_record.pop(key, None)

            if current_time - last_heartbeat_time >= HEARTBEAT_INTERVAL:
                state_str = "等待中" if status == 1 else "空闲"
                sys.stdout.write(f"\r[{time.strftime('%H:%M:%S')}] ❤️ 服务运行中 | 当前状态: {state_str}           \n")
                last_heartbeat_time = current_time

            execution_time = time.time() - start_loop_time
            sleep_time = max(0, CHECK_INTERVAL - execution_time)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        logger.info("用户停止")
    except Exception as e:
        logger.error(f"异常: {e}")
    finally:
        remove_lock()

if __name__ == "__main__":
    main()

