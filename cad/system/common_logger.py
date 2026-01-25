# -*- coding: utf-8 -*-
# 文件位置: D:/claude-tasks/cad/system/common_logger.py
# 版本: V2.1 (修复 CriticalSection 属性缺失 Bug)

import os
import sys
import logging
import time
import datetime
import inspect
from pathlib import Path
from logging.handlers import RotatingFileHandler

try:
    import openpyxl
    from openpyxl import Workbook, load_workbook
except ImportError:
    openpyxl = None

# ==========================================
# 1. 全局配置
# ==========================================
CURRENT_FILE = Path(__file__).resolve()
TESTS_DIR = CURRENT_FILE.parent.parent / "tests"
TEST_EXCEL_PATH = TESTS_DIR / "testfunc.xlsx"

if not TESTS_DIR.exists():
    try: TESTS_DIR.mkdir(parents=True, exist_ok=True)
    except: pass

DEBUG_CONFIG = {
    "MODE": 0, "WHO": "AI", "WAIT": 0
}

def set_debug_mode(mode=1, who="AI", wait_time=30):
    global DEBUG_CONFIG
    DEBUG_CONFIG["MODE"] = int(mode)
    DEBUG_CONFIG["WHO"] = str(who).upper()
    DEBUG_CONFIG["WAIT"] = int(wait_time)
    if 'sys_logger' in globals():
        sys_logger.info(f"🔧 调试配置更新: Mode={mode}, Who={who}, Wait={wait_time}s")

# ==========================================
# 2. 日志系统
# ==========================================
def setup_logger(log_file="system_run.log"):
    logger = logging.getLogger("CAD_System")
    logger.setLevel(logging.INFO)
    if logger.handlers: return logger
    
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    # File Handler
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file)
    try:
        fh = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except: pass

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

sys_logger = setup_logger()

# ==========================================
# 3. Excel 记录
# ==========================================
def record_test_result(script_name=None, func_name=None, is_pass=False, **variables):
    if not openpyxl: return

    if script_name is None or func_name is None:
        try:
            frame = inspect.currentframe().f_back
            if script_name is None:
                script_name = os.path.basename(frame.f_code.co_filename)
            if func_name is None:
                func_name = frame.f_code.co_name
                if func_name == "<module>": func_name = "[Main]"
        except:
            script_name = script_name or "Unknown"
            func_name = func_name or "Unknown"

    try:
        row_data = [
            f"Time:{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Script:{script_name}",
            f"Func:{func_name}"
        ]
        for k, v in variables.items():
            val = str(v)
            if len(val) > 500: val = val[:500] + "..."
            row_data.append(f"{k}:{val}")
        
        row_data.append(f"Result:{'PASS' if is_pass else 'FAIL'}")

        if os.path.exists(TEST_EXCEL_PATH):
            wb = load_workbook(TEST_EXCEL_PATH)
            ws = wb.active
        else:
            wb = Workbook()
            ws = wb.active
        
        ws.append(row_data)
        wb.save(TEST_EXCEL_PATH)
    except Exception as e:
        sys_logger.error(f"❌ Excel Error: {e}")

# ==========================================
# 4. 核心工具 (修复版)
# ==========================================
def checkpoint(desc, is_pass=True, **variables):
    try:
        frame = inspect.currentframe().f_back
        s_name = os.path.basename(frame.f_code.co_filename)
        f_name = frame.f_code.co_name
    except:
        s_name, f_name = "Unknown", "Unknown"

    record_test_result(s_name, f_name, is_pass, Checkpoint=desc, **variables)

    if DEBUG_CONFIG["MODE"] == 1 and DEBUG_CONFIG["WHO"] == "HUMAN":
        wait = DEBUG_CONFIG["WAIT"]
        if wait > 0:
            print(f"\n✋ [检查点] {desc} | Data: {variables}")
            print(f"⏳ 暂停 {wait}s (Ctrl+C 跳过)...")
            try:
                time.sleep(wait) 
            except KeyboardInterrupt:
                print("⏩ 跳过")

class CriticalSection:
    def __init__(self, description="关键操作", script_name=None, func_name=None):
        self.desc = description
        
        # 1. 自动推断调用者
        if script_name is None or func_name is None:
            try:
                frame = inspect.currentframe().f_back
                if script_name is None:
                    script_name = os.path.basename(frame.f_code.co_filename)
                if func_name is None:
                    func_name = frame.f_code.co_name
            except:
                script_name = script_name or "Unknown"
                func_name = func_name or "Unknown"
        
        self.s_name = script_name
        self.f_name = func_name

        # 2. ✅ [关键修复] 显式初始化模式属性
        self.mode = DEBUG_CONFIG["MODE"]
        self.who = DEBUG_CONFIG["WHO"]
        self.wait_time = DEBUG_CONFIG["WAIT"]
        
        self.is_active = (self.mode == 1)
        self.is_ai = (self.is_active and self.who == "AI")
        self.is_human = (self.is_active and self.who == "HUMAN")
        
        self.metrics = {}
        self.is_pass = False

    def record(self, **kwargs):
        self.metrics.update(kwargs)

    def __enter__(self):
        sys_logger.info(f"🚩 进入区域: {self.desc} [Mode:{self.mode}|{self.who}]")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.is_pass = False
            self.metrics['error'] = str(exc_val)
            sys_logger.error(f"❌ 区域崩溃: {exc_val}")
        else:
            self.is_pass = ('error' not in self.metrics)

        try:
            record_test_result(
                self.s_name, self.f_name, self.is_pass,
                Section=self.desc, **self.metrics
            )
        except: pass

        if self.is_human and self.wait_time > 0:
            print(f"\n✋ [人工干预] {self.desc} | Vars: {self.metrics}")
            print(f"⏳ 暂停 {self.wait_time}s...")
            try:
                time.sleep(self.wait_time)
            except KeyboardInterrupt:
                print("⏩ 跳过")
        
        return False # 不吞异常

def node(msg, *args, **kwargs):
    if args or kwargs:
        try: msg = msg.format(*args, **kwargs)
        except: pass
    sys_logger.info(msg)
