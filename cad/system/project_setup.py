# -*- coding: utf-8 -*-
# 文件位置: D:/codex-tasks/cad/system/project_setup.py
# 版本: V2.0
"""
project_setup.py（精简版）

定位：
- 仅保留“纯路径配置”职责
- 不再负责 sys.path 引导
- 不再承担项目导入环境构建职责

说明：
- import 环境统一由入口脚本的 bootstrap 规则负责
- 库模块禁止在内部修改 sys.path
- 本文件只提供稳定的路径常量给系统脚本引用

推荐用法：
    from system.project_setup import PathConfig
    tests_dir = PathConfig.TESTS
    logs_dir = PathConfig.LOGS
"""

from __future__ import annotations

import os
from pathlib import Path


# ==========================================
# 1. 核心锚点定位
# ==========================================
CURRENT_FILE = Path(__file__).resolve()
SYSTEM_DIR = CURRENT_FILE.parent            # .../cad/system
CAD_ROOT = SYSTEM_DIR.parent                # .../cad
WORKSPACE_DIR = CAD_ROOT.parent             # .../codex-tasks


class PathConfig:
    """
    统一路径常量配置。

    约定：
    - ROOT / CAD_DIR 指向 cad 根目录
    - WORKSPACE_DIR 指向 codex-tasks 根目录
    - 本类只导出路径，不做导入引导
    """

    ROOT = CAD_ROOT
    CAD_DIR = CAD_ROOT
    SYSTEM_DIR = SYSTEM_DIR
    SCRIPTS_DIR = CAD_ROOT / "scripts"
    TESTS = CAD_ROOT / "tests"
    LOGS = SYSTEM_DIR / "logs"
    WORKSPACE_DIR = WORKSPACE_DIR

    _user_env = os.environ.get("USERPATH")
    if _user_env:
        userpath = Path(_user_env)
    else:
        userpath = Path("D:/Mypro/基础服务/用户1")

    TEST_EXCEL = TESTS / "testfunc.xlsx"
    COMMON_LOGGER = SYSTEM_DIR / "common_logger.py"


# ==========================================
# 2. 目录保障（仅限纯目录创建）
# ==========================================
for p in [PathConfig.LOGS, PathConfig.TESTS]:
    try:
        p.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass


__all__ = [
    "PathConfig",
    "CURRENT_FILE",
    "SYSTEM_DIR",
    "CAD_ROOT",
    "WORKSPACE_DIR",
]
