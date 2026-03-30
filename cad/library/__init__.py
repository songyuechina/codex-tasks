#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Library 模块统一入口

本模块为CAD library的智能体服务函数库，提供：
- cad_annotation: 注释与文字函数
- cad_blocks: 图块操作
- cad_control: 综合控制
- cad_geometry: 几何分析基础
- cad_geometry_draw: 几何绘图
- cad_geometry_polyline: 多段线操作
- cad_geometry_segment: 线段操作
- cad_objects: 对象操作
- Databaseoperation: 数据库操作
- tarch_building: 天正建筑

使用方法:
    from library import cad_annotation
    from library import cad_geometry
"""

import sys
from pathlib import Path

# 确保本目录在sys.path中
_current = Path(__file__).resolve().parent
if str(_current) not in sys.path:
    sys.path.insert(0, str(_current))

# 统一导入各子模块
from . import cad_annotation
from . import cad_blocks
from . import cad_control
from . import cad_geometry
from . import cad_geometry_draw
from . import cad_geometry_polyline
from . import cad_geometry_segment
from . import cad_objects
from . import Databaseoperation
from . import tarch_building

__all__ = [
    'cad_annotation',
    'cad_blocks',
    'cad_control',
    'cad_geometry',
    'cad_geometry_draw',
    'cad_geometry_polyline',
    'cad_geometry_segment',
    'cad_objects',
    'Databaseoperation',
    'tarch_building',
]
