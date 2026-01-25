# -*- coding: utf-8 -*-
# 文件位置: D:/claude-tasks/cad/system/CAD_com_utils.py V1.0
import time
import functools
import pythoncom
from pywintypes import com_error

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

# 引入日志模块
try:
    from system.common_logger import sys_logger
except ImportError:
    import logging
    sys_logger = logging.getLogger("Fallback")
    sys_logger.addHandler(logging.NullHandler())




# ================= 1. 错误码常量 =================
_RPC_BUSY_CODES = (-2147417846, -2147418111)
_RPC_DOWN_CODES = (-2147023174, -2147467260, -2147417848)
_BUSY_STRINGS = ("Call was rejected", "正在使用", "IsBusy", "2147417846")

# ================= 2. 核心重试逻辑实现 =================
def _retry_logic(max_retries, base_delay, func, *args, **kwargs):
    """实际执行重试的内部函数"""
    last_err = None
    if max_retries <= 0: max_retries = 1

    for i in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_msg = str(e)
            hr = getattr(e, 'hresult', None)

            # 判据 A: 忙碌 (Busy)
            is_busy_code = (hr in _RPC_BUSY_CODES)
            is_busy_text = any(s in err_msg for s in _BUSY_STRINGS)

            if is_busy_code or is_busy_text:
                last_err = e
                wait_time = base_delay * (1.5 ** i)
                
                # 记录日志 (Warning)
                err_code_display = f"0x{hr & 0xFFFFFFFF:08X}" if hr else "NoCode"
                sys_logger.warning(
                    f"CAD忙碌 [{func.__name__}] - {err_code_display} - "
                    f"{wait_time:.2f}s后重试 ({i+1}/{max_retries})"
                )
                
                # 消息泵 (防死锁)
                try: pythoncom.PumpWaitingMessages()
                except: pass
                
                time.sleep(wait_time)
                continue

            # 判据 B: 掉线 (Down)
            if hr in _RPC_DOWN_CODES:
                sys_logger.error(f"CAD连接断开/崩溃 [{func.__name__}]")
                raise e

            # 判据 C: 其他逻辑错误
            sys_logger.error(f"脚本运行时错误 [{func.__name__}]: {err_msg}")
            raise e
    
    sys_logger.critical(f"❌ 重试彻底失败 [{func.__name__}] - 已耗尽 {max_retries} 次机会")
    if last_err: raise last_err

# ================= 3. 智能装饰器 (修正版) =================
def retry_on_busy(func_or_retries=None, max_retries=10, base_delay=0.5):
    """
    【智能通用装饰器】
    既可以当作普通装饰器用，也可以传参数。
    用法 1: @retry_on_busy                  -> 使用默认 max_retries=10
    用法 2: @retry_on_busy(5)               -> 设置 max_retries=5
    用法 3: @retry_on_busy(max_retries=20)  -> 显式指定参数 (修复了之前的报错)
    """
    
    # 内部工厂：负责生成最终的装饰器
    def decorator_factory(final_retries, final_delay):
        def actual_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return _retry_logic(final_retries, final_delay, func, *args, **kwargs)
            return wrapper
        return actual_decorator

    # --- 智能参数解析 ---
    
    # 情况 A: @retry_on_busy (无括号调用)
    # 此时 func_or_retries 是被装饰的函数，其他参数使用默认值
    if callable(func_or_retries):
        func = func_or_retries
        return decorator_factory(max_retries, base_delay)(func)

    # 情况 B: @retry_on_busy(5) (位置参数调用)
    # 此时 func_or_retries 是数字 5
    if isinstance(func_or_retries, int):
        return decorator_factory(func_or_retries, base_delay)

    # 情况 C: @retry_on_busy(max_retries=5) (关键字参数调用)
    # 此时 func_or_retries 是 None，但 max_retries 被赋值了
    if func_or_retries is None:
        return decorator_factory(max_retries, base_delay)

    # 兜底：如果用户传了奇奇怪怪的东西，默认按10次处理
    return decorator_factory(10, base_delay)


class SafeCOM:
    """工具类：用于无法使用装饰器的代码块"""
    @staticmethod
    def call(func, *args, **kwargs):
        # 动态包装并执行任意函数
        return retry_on_busy(func)(*args, **kwargs)
    
    @staticmethod
    def list_selection(ss):
        # 安全地将 SelectionSet 转为 list
        @retry_on_busy(max_retries=20)
        def _to_list():
            if ss.Count == 0: return []
            return list(ss)
        try:
            return _to_list()
        except:
            sys_logger.error("SafeCOM: 转换选择集失败")
            return []



# ================= 4. 向下兼容接口 =================

def retry_if_busy(max_retries=10, delay=0.5):
    """
    【兼容补丁】旧接口：retry_if_busy
    
    完全转发给新架构的 retry_on_busy。
    这样旧代码中写 @retry_if_busy(max_retries=5) 依然有效，
    但底层享受新架构的日志系统和消息泵防死锁机制。
    """
    # 直接调用智能装饰器，参数一一对应
    return retry_on_busy(max_retries=max_retries, base_delay=delay)





        
