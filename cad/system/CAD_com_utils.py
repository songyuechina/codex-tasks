# -*- coding: utf-8 -*-
# 文件位置: D:/claude-tasks/cad/system/CAD_com_utils.py
# 版本: V1.1 (集成日志热替换与静音模式)
"""
引入 silent_mode 上下文管理器。

实现 LoggerHotSwapper 类：通过函数指针替换（Method Swapping）实现零开销静音。

Monkey Patch：强制替换 system.common_logger.sys_logger，确保全局生效。


"""

import time
import functools
import pythoncom
import logging
from contextlib import contextmanager
from pywintypes import com_error

# ================= 0. 路径引导 =================
import os
import sys
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))
from system.project_setup import PathConfig

# ================= 1. 日志控制系统 (核心升级) =================
# 引入原始 logger 模块
import system.common_logger

# 定义空函数 (No-op)，用于静音时的极致性能
def _dummy_func(*args, **kwargs):
    pass

class LoggerHotSwapper:
    """
    【日志热替换控制器】
    不通过 if 判断，而是直接修改函数指针，实现 0 开销静音。
    """
    def __init__(self, original_logger):
        self._wrapped = original_logger
        # 初始化函数指针
        self.info = original_logger.info
        self.debug = original_logger.debug
        # 警告和错误永远保留，确保安全
        self.warning = original_logger.warning
        self.error = original_logger.error
        self.critical = original_logger.critical

    def mute(self):
        """开启静音：将 info/debug 指向空函数"""
        self.info = _dummy_func
        self.debug = _dummy_func
    
    def unmute(self):
        """解除静音：恢复原始函数"""
        self.info = self._wrapped.info
        self.debug = self._wrapped.debug

    # —————————— 新增：状态属性控制 ——————————
    @property
    def mute_mode(self):
        """获取当前静音状态 (True/False)"""
        return self._is_muted

    @mute_mode.setter
    def mute_mode(self, value):
        """
        设置静音状态
        接受: 1, 0, True, False
        用法: sys_logger.mute_mode = 1
        """
        if value:
            self.mute()
        else:
            self.unmute()

    def __getattr__(self, name):
        return getattr(self._wrapped, name)



# --- 执行替换 ---
# 1. 包装原始 logger
sys_logger = LoggerHotSwapper(system.common_logger.sys_logger)
# 2. 【关键】反向注入回源模块，确保所有 import system.common_logger 的地方都生效
system.common_logger.sys_logger = sys_logger

@contextmanager
def silent_mode():
    """
    【静音模式上下文】
    用法:
        with silent_mode():
            func_that_prints_too_much()
    """
    sys_logger.mute()
    try:
        yield
    finally:
        sys_logger.unmute()

# ================= 2. 错误码常量 =================
_RPC_BUSY_CODES = (-2147417846, -2147418111)
_RPC_DOWN_CODES = (-2147023174, -2147467260, -2147417848)
_BUSY_STRINGS = ("Call was rejected", "正在使用", "IsBusy", "2147417846")

# ================= 3. 核心重试逻辑实现 =================
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
                
                # 记录日志 (Warning 永远不会被静音)
                err_code_display = f"0x{hr & 0xFFFFFFFF:08X}" if hr else "NoCode"
                sys_logger.warning(
                    f"CAD忙碌 [{func.__name__}] - {err_code_display} - "
                    f"{wait_time:.2f}s后重试 ({i+1}/{max_retries})"
                )
                
                try: pythoncom.PumpWaitingMessages()
                except: pass
                
                time.sleep(wait_time)
                continue

            # 判据 B: 掉线 (Down)
            if hr in _RPC_DOWN_CODES:
                sys_logger.error(f"CAD连接断开/崩溃 [{func.__name__}]")
                raise e

            # 判据 C: 其他逻辑错误
            # sys_logger.error(f"脚本运行时错误 [{func.__name__}]: {err_msg}")
            raise e
    
    sys_logger.critical(f"❌ 重试彻底失败 [{func.__name__}] - 已耗尽 {max_retries} 次机会")
    if last_err: raise last_err

# ================= 4. 智能装饰器 =================
def retry_on_busy(func_or_retries=None, max_retries=10, base_delay=0.5):
    """
    【智能通用装饰器】
    用法 1: @retry_on_busy
    用法 2: @retry_on_busy(5)
    用法 3: @retry_on_busy(max_retries=20)
    """
    def decorator_factory(final_retries, final_delay):
        def actual_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return _retry_logic(final_retries, final_delay, func, *args, **kwargs)
            return wrapper
        return actual_decorator

    if callable(func_or_retries):
        func = func_or_retries
        return decorator_factory(max_retries, base_delay)(func)

    if isinstance(func_or_retries, int):
        return decorator_factory(func_or_retries, base_delay)

    if func_or_retries is None:
        return decorator_factory(max_retries, base_delay)

    return decorator_factory(10, base_delay)

class SafeCOM:
    """工具类：用于无法使用装饰器的代码块"""
    @staticmethod
    def call(func, *args, **kwargs):
        return retry_on_busy(func)(*args, **kwargs)
    
    @staticmethod
    def list_selection(ss):
        @retry_on_busy(max_retries=20)
        def _to_list():
            if ss.Count == 0: return []
            return list(ss)
        try:
            return _to_list()
        except:
            sys_logger.error("SafeCOM: 转换选择集失败")
            return []

# ================= 5. 向下兼容接口 =================
def retry_if_busy(max_retries=10, delay=0.5):
    return retry_on_busy(max_retries=max_retries, base_delay=delay)





#&&% 函数别名
def alias(*names):
    """
    @alias("别名1","别名2",…)
    def foo(...): …
    """
    def decorator(func):
        mod = sys.modules[func.__module__]
        for nm in names:
            setattr(mod, nm, func)
        return func
    return decorator

#&&% 调试机制

"""
正常运行：DEBUG = False，print 正常输出，node() 什么都不打。

调试模式：enable_debug() → print 全被静音，只有带 @debuggable 的函数里调用的 node() 会输出。

"""



# ---------------- 局部调试控制 ----------------
DEBUG             = False              # 总开关
_DEBUG_CODE_STACK = []                 # ← 新增：调试函数调用栈

def node(msg: str, *args, **kwargs):
    """
    只有 DEBUG = True 且当前帧属于【栈底】函数时才打印。
    """
    if not DEBUG or not _DEBUG_CODE_STACK:
        return
    frame = inspect.currentframe().f_back
    try:
        # 只允许“最外层”调试函数输出
        if frame.f_code is _DEBUG_CODE_STACK[0]:
            _orig_print(msg.format(*args), **kwargs)
    finally:
        del frame




def timeit(func):
    """
    【耗时统计】
    已适配静音模式：使用 warning 确保耗时信息在 silent_mode 下依然可见。
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. 开始信息：静音模式下不显示 (info)
        if 'sys_logger' in globals():
            sys_logger.info(f"⏱ 开始 `{func.__name__}` ...")
            
        start_time = time.time()
        try:
            res = func(*args, **kwargs)
            cost = time.time() - start_time
            
            # 2. 结束信息：强制显示 (warning)
            if 'sys_logger' in globals():
                sys_logger.warning(f"✅ 完成 `{func.__name__}` (耗时 {cost:.2f}s)")
            return res
        except Exception as e:
            if 'sys_logger' in globals():
                sys_logger.error(f"❌ `{func.__name__}` 崩溃: {e}")
            raise e
    return wrapper

def debuggable(func):
    """
    【调试标记】
    最简占位版本：仅作为一个标记，不改变函数行为。
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


































