# -*- coding: utf-8 -*-
# 文件位置: D:/codex-tasks/cad/system/CAD_com_utils.py
# 版本: V2.0
"""
CAD_com_utils.py（精简重构版）

定位：
- 专注解决 CAD COM 调用中的 busy / rejected 问题
- 提供局部静音工具，减少高频轮询时的日志噪声
- 提供少量兼容装饰器与辅助函数
- 不再承担项目引导职责
- 不再 monkey patch system.common_logger.sys_logger
- 不再承载复杂局部调试栈机制

保留核心价值：
1. retry_on_busy / retry_if_busy
2. SafeCOM.call / SafeCOM.list_selection
3. silent_mode
4. timeit

兼容保留：
- alias
- debuggable
- node（降级为 debug 日志快捷输出）

规则：
- 业务模块统一使用 system.common_logger.sys_logger
- 本模块只做 COM 辅助，不做 CAD 连接主入口
- 真正的连接入口仍然是 system.licad.py 的 C 类
"""

from __future__ import annotations

import functools
import time
from contextlib import contextmanager
from typing import Any, Callable, Iterable, List, Optional

import pythoncom

from system.common_logger import sys_logger


# ===============================
# 1. 日志静音（局部）
# ===============================

def _dummy_func(*args: Any, **kwargs: Any) -> None:
    """No-op，占位空函数。"""
    return None


@contextmanager
def silent_mode():
    """
    局部静音 sys_logger.info / sys_logger.debug。

    用法：
        with silent_mode():
            do_many_polling_calls()

    说明：
    - warning / error / critical 永远保留，不会被静音
    - 仅在上下文内临时替换，退出后恢复
    """
    orig_info = getattr(sys_logger, "info", None)
    orig_debug = getattr(sys_logger, "debug", None)

    try:
        if orig_info is not None:
            sys_logger.info = _dummy_func  # type: ignore[attr-defined]
        if orig_debug is not None:
            sys_logger.debug = _dummy_func  # type: ignore[attr-defined]
        yield
    finally:
        if orig_info is not None:
            sys_logger.info = orig_info  # type: ignore[attr-defined]
        if orig_debug is not None:
            sys_logger.debug = orig_debug  # type: ignore[attr-defined]


# ===============================
# 2. COM 忙碌 / 掉线判据
# ===============================

_RPC_BUSY_CODES = (-2147417846, -2147418111)
_RPC_DOWN_CODES = (-2147023174, -2147467260, -2147417848)
_BUSY_STRINGS = ("Call was rejected", "正在使用", "IsBusy", "2147417846")


# ===============================
# 3. 核心重试逻辑
# ===============================

def _retry_logic(
    max_retries: int,
    base_delay: float,
    func: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    实际执行重试的内部函数。

    判据：
    - Busy / Rejected：warning + 退避重试
    - Down / 崩溃：error + 直接抛出
    - 其他异常：直接抛出
    """
    last_err: Optional[Exception] = None
    if max_retries <= 0:
        max_retries = 1

    for i in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_msg = str(e)
            hr = getattr(e, "hresult", None)

            is_busy_code = hr in _RPC_BUSY_CODES
            is_busy_text = any(s in err_msg for s in _BUSY_STRINGS)

            if is_busy_code or is_busy_text:
                last_err = e
                wait_time = base_delay * (1.5 ** i)

                err_code_display = f"0x{hr & 0xFFFFFFFF:08X}" if hr else "NoCode"
                sys_logger.warning(
                    f"CAD忙碌 [{func.__name__}] - {err_code_display} - "
                    f"{wait_time:.2f}s后重试 ({i + 1}/{max_retries})"
                )

                try:
                    pythoncom.PumpWaitingMessages()
                except Exception:
                    pass

                time.sleep(wait_time)
                continue

            if hr in _RPC_DOWN_CODES:
                sys_logger.error(f"CAD连接断开/崩溃 [{func.__name__}]")
                raise

            raise

    sys_logger.critical(f"❌ 重试彻底失败 [{func.__name__}] - 已耗尽 {max_retries} 次机会")
    if last_err is not None:
        raise last_err
    raise RuntimeError(f"未知重试失败: {func.__name__}")


# ===============================
# 4. 智能装饰器
# ===============================

def retry_on_busy(
    func_or_retries: Optional[Any] = None,
    max_retries: int = 10,
    base_delay: float = 0.5,
):
    """
    智能通用装饰器。

    用法 1: @retry_on_busy
    用法 2: @retry_on_busy(5)
    用法 3: @retry_on_busy(max_retries=20, base_delay=0.5)
    """

    def decorator_factory(final_retries: int, final_delay: float):
        def actual_decorator(func: Callable[..., Any]):
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any):
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


def retry_if_busy(max_retries: int = 10, delay: float = 0.5):
    """
    向下兼容旧接口。
    """
    return retry_on_busy(max_retries=max_retries, base_delay=delay)


# ===============================
# 5. SafeCOM 工具类
# ===============================

class SafeCOM:
    """
    工具类：用于无法使用装饰器的代码块。
    """

    @staticmethod
    def call(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        return retry_on_busy(func)(*args, **kwargs)

    @staticmethod
    def list_selection(ss: Any) -> List[Any]:
        """
        将选择集转成 list。
        失败时返回 []，并记录 error。
        """

        @retry_on_busy(max_retries=20)
        def _to_list():
            if ss.Count == 0:
                return []
            return list(ss)

        try:
            return _to_list()
        except Exception as e:
            sys_logger.error(f"SafeCOM: 转换选择集失败: {e}")
            return []


# ===============================
# 6. 兼容辅助
# ===============================

def alias(*names: str):
    """
    为函数注册多个模块级别名。

    用法：
        @alias("别名1", "别名2")
        def foo(...):
            ...
    """
    def decorator(func: Callable[..., Any]):
        mod = __import__(func.__module__, fromlist=["*"])
        for nm in names:
            setattr(mod, nm, func)
        return func

    return decorator


def node(msg: str, *args: Any, **kwargs: Any) -> None:
    """
    兼容旧接口。
    现在统一退化为 debug 日志快捷输出。
    """
    if args or kwargs:
        try:
            msg = msg.format(*args, **kwargs)
        except Exception:
            pass
    sys_logger.debug(msg)


def timeit(func: Callable[..., Any]):
    """
    耗时统计装饰器。

    规则：
    - 开始：info
    - 结束：warning（确保在 silent_mode 下仍可见）
    - 异常：error + raise
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        sys_logger.info(f"⏱ 开始 `{func.__name__}` ...")
        start_time = time.time()
        try:
            res = func(*args, **kwargs)
            cost = time.time() - start_time
            sys_logger.warning(f"✅ 完成 `{func.__name__}` (耗时 {cost:.2f}s)")
            return res
        except Exception as e:
            sys_logger.error(f"❌ `{func.__name__}` 崩溃: {e}")
            raise

    return wrapper


def debuggable(func: Callable[..., Any]):
    """
    调试标记兼容装饰器。
    当前只保留占位语义，不改变函数行为。
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        return func(*args, **kwargs)

    return wrapper


__all__ = [
    "silent_mode",
    "retry_on_busy",
    "retry_if_busy",
    "SafeCOM",
    "alias",
    "node",
    "timeit",
    "debuggable",
]
