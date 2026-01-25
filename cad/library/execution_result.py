#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
函数执行状态规范
定义统一的函数返回值标准
"""

from enum import Enum
from typing import Any, Dict, Optional


class ExecutionStatus(Enum):
    """
    函数执行状态枚举

    用于明确区分函数执行结果，避免使用简单的True/False
    """
    # 成功状态
    EXECUTION_SUCCESS = "EXECUTION_SUCCESS"  # 执行成功

    # 失败状态
    EXECUTION_FAILED = "EXECUTION_FAILED"    # 执行失败
    EXECUTION_PARTIAL = "EXECUTION_PARTIAL"  # 部分成功
    EXECUTION_TIMEOUT = "EXECUTION_TIMEOUT"  # 执行超时
    EXECUTION_CANCELLED = "EXECUTION_CANCELLED"  # 执行取消

    # 异常状态
    EXECUTION_ERROR = "EXECUTION_ERROR"      # 执行错误
    EXECUTION_INVALID = "EXECUTION_INVALID"  # 参数无效


class ExecutionResult:
    """
    函数执行结果标准类

    所有复杂函数应该返回此类的实例，而不是简单的True/False
    """

    def __init__(
        self,
        status: ExecutionStatus,
        data: Optional[Any] = None,
        message: str = "",
        details: Optional[Dict] = None,
        error: Optional[Exception] = None
    ):
        """
        初始化执行结果

        Args:
            status: 执行状态（必填）
            data: 返回数据（可选）
            message: 结果消息（可选）
            details: 详细信息字典（可选）
            error: 异常对象（可选）
        """
        self.status = status
        self.data = data
        self.message = message
        self.details = details or {}
        self.error = error

    def is_success(self) -> bool:
        """判断是否成功"""
        return self.status == ExecutionStatus.EXECUTION_SUCCESS

    def is_failed(self) -> bool:
        """判断是否失败"""
        return self.status in [
            ExecutionStatus.EXECUTION_FAILED,
            ExecutionStatus.EXECUTION_ERROR,
            ExecutionStatus.EXECUTION_TIMEOUT,
            ExecutionStatus.EXECUTION_CANCELLED
        ]

    def is_partial(self) -> bool:
        """判断是否部分成功"""
        return self.status == ExecutionStatus.EXECUTION_PARTIAL

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'status': self.status.value,
            'data': self.data,
            'message': self.message,
            'details': self.details,
            'error': str(self.error) if self.error else None
        }

    def __repr__(self):
        return f"ExecutionResult(status={self.status.value}, message='{self.message}')"

    def __bool__(self):
        """支持布尔判断：if result: ..."""
        return self.is_success()


# ========== 便捷构造函数 ==========

def success(data=None, message="执行成功", **details) -> ExecutionResult:
    """
    创建成功结果

    Args:
        data: 返回数据
        message: 成功消息
        **details: 详细信息

    Returns:
        ExecutionResult: 成功结果

    示例:
        >>> return success(data=result_list, message="成功生成15个PDF", count=15)
    """
    return ExecutionResult(
        status=ExecutionStatus.EXECUTION_SUCCESS,
        data=data,
        message=message,
        details=details
    )


def failed(message="执行失败", error=None, **details) -> ExecutionResult:
    """
    创建失败结果

    Args:
        message: 失败消息
        error: 异常对象
        **details: 详细信息

    Returns:
        ExecutionResult: 失败结果

    示例:
        >>> return failed(message="文件不存在", error=e, file_path=path)
    """
    return ExecutionResult(
        status=ExecutionStatus.EXECUTION_FAILED,
        message=message,
        details=details,
        error=error
    )


def partial(data=None, message="部分成功", **details) -> ExecutionResult:
    """
    创建部分成功结果

    Args:
        data: 返回数据
        message: 消息
        **details: 详细信息

    Returns:
        ExecutionResult: 部分成功结果

    示例:
        >>> return partial(
        ...     data=success_list,
        ...     message="15个中成功12个",
        ...     total=15,
        ...     success=12,
        ...     failed=3
        ... )
    """
    return ExecutionResult(
        status=ExecutionStatus.EXECUTION_PARTIAL,
        data=data,
        message=message,
        details=details
    )


def error(message="执行错误", exception=None, **details) -> ExecutionResult:
    """
    创建错误结果

    Args:
        message: 错误消息
        exception: 异常对象
        **details: 详细信息

    Returns:
        ExecutionResult: 错误结果

    示例:
        >>> return error(message="COM接口异常", exception=e, retry_count=3)
    """
    return ExecutionResult(
        status=ExecutionStatus.EXECUTION_ERROR,
        message=message,
        details=details,
        error=exception
    )


# ========== 函数内置判定标准装饰器 ==========

def with_execution_check(expected_conditions):
    """
    函数执行检查装饰器

    自动在函数执行后检查是否满足预期条件

    Args:
        expected_conditions: 预期条件字典
            {
                'min_result_count': 10,  # 最小结果数量
                'max_error_count': 0,    # 最大错误数量
                'required_keys': ['data', 'count'],  # 必需的键
                ...
            }

    示例:
        >>> @with_execution_check({
        ...     'min_result_count': 15,
        ...     'max_error_count': 0
        ... })
        ... def my_function():
        ...     # 函数实现
        ...     return result
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 执行函数
            result = func(*args, **kwargs)

            # 如果返回的不是ExecutionResult，直接返回
            if not isinstance(result, ExecutionResult):
                return result

            # 检查预期条件
            checks_passed = True
            failed_checks = []

            # 检查最小结果数量
            if 'min_result_count' in expected_conditions:
                min_count = expected_conditions['min_result_count']
                actual_count = result.details.get('count', 0)
                if actual_count < min_count:
                    checks_passed = False
                    failed_checks.append(
                        f"结果数量不足: 预期>={min_count}, 实际={actual_count}"
                    )

            # 检查最大错误数量
            if 'max_error_count' in expected_conditions:
                max_errors = expected_conditions['max_error_count']
                actual_errors = result.details.get('error_count', 0)
                if actual_errors > max_errors:
                    checks_passed = False
                    failed_checks.append(
                        f"错误数量过多: 预期<={max_errors}, 实际={actual_errors}"
                    )

            # 检查必需的键
            if 'required_keys' in expected_conditions:
                required_keys = expected_conditions['required_keys']
                for key in required_keys:
                    if key not in result.details:
                        checks_passed = False
                        failed_checks.append(f"缺少必需的键: {key}")

            # 如果检查失败，修改状态
            if not checks_passed:
                result.status = ExecutionStatus.EXECUTION_FAILED
                result.message += f" (检查失败: {'; '.join(failed_checks)})"
                result.details['failed_checks'] = failed_checks

            return result

        return wrapper
    return decorator
