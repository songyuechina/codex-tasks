# Supervised Task Packet
role: tester
title: print-min-requirements-check

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦测试结论与阻塞，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。

## Objective
基于给定证据，归纳当前系统下“任意矩形多段线能作为打印区域”的最低要求，限定4条以内，并注明哪些是代码规则、哪些是实测规则。

## Context
关键证据：rect_min_req_source 识别出闭合和未闭合两个轴对齐矩形；rect_rotated_only dry-run 为0；rect_closed_only 单张实打成功；rect_open_same_size 单张实打成功。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.

## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/print_area_analysis.py
# -*- coding: utf-8 -*-
"""print_area_analysis.py

本脚本用于“打印区域(打印框)”分析。

约束与假设：
- 打印范围使用“矩形多段线”表示。
- 打印多段线之间不应放置仅用于分隔的矩形多段线（否则会干扰包含关系）。
- 允许存在“外包大矩形”包裹若干打印多段线：脚本采用“极大矩形”算法识别真实打印区域。
- 使用“外包盒短边的万分之五(0.0005*w_short)”作为动态容差：
  - 用于矩形识别（顶点聚类/坐标分类）
  - 用于多段线去重（空间重叠）
  - 用于包含关系判断
- 允许 1:100 系列与 1:1 系列（通过 *0.01 得到）在同一文件中同时出现。

输出：
- 提供：
  1) 严格标准匹配（只匹配288标准值）
  2) 近似匹配（总能返回最接近的标准）
  3) 打印区域提取（模型空间 + 各布局空间）

注意：
- 脚本为“纯函数式模块”（无类），但根据需求包含必要的 CAD 数据库写操作：
  - 删除伪打印区域外框（并在删除前用 4 条直线保留其边界信息）。

路径可随 /cad 项目一起迁移，使用 system.licad 的 C 连接 CAD。
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# -----------------------------------------------------------------------------
# bootstrap: allow free migration under /cad
# -----------------------------------------------------------------------------
current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise Exception("找
...[truncated]...


## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/cases/output/rect_min_req_source/20260316-002544/print_summary.json
{
  "run_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_min_req_source\\20260316-002544",
  "work_dwg": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_min_req_source\\20260316-002544\\work\\rect_min_req_source__print_work.dwg",
  "plan_json": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_min_req_source\\20260316-002544\\print_plan.json",
  "plan": {
    "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_min_req_source\\20260316-002544\\work\\rect_min_req_source__print_work.dwg",
    "output_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_min_req_source\\20260316-002544\\pdf",
    "total_jobs": 2,
    "landscape_count": 2,
    "portrait_count": 0,
    "jobs_by_space": {
      "model": [
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\
...[truncated]...


## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/cases/output/rect_closed_only/20260316-002950/print_summary.json
{
  "run_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_closed_only\\20260316-002950",
  "work_dwg": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_closed_only\\20260316-002950\\work\\rect_closed_only__print_work.dwg",
  "plan_json": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_closed_only\\20260316-002950\\print_plan.json",
  "plan": {
    "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_closed_only\\20260316-002950\\work\\rect_closed_only__print_work.dwg",
    "output_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_closed_only\\20260316-002950\\pdf",
    "total_jobs": 1,
    "landscape_count": 1,
    "portrait_count": 0,
    "jobs_by_space": {
      "model": [
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_closed_only\\20
...[truncated]...


## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/cases/output/rect_open_same_size/20260316-003303/print_summary.json
{
  "run_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_open_same_size\\20260316-003303",
  "work_dwg": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_open_same_size\\20260316-003303\\work\\rect_open_same_size__print_work.dwg",
  "plan_json": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_open_same_size\\20260316-003303\\print_plan.json",
  "plan": {
    "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_open_same_size\\20260316-003303\\work\\rect_open_same_size__print_work.dwg",
    "output_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_open_same_size\\20260316-003303\\pdf",
    "total_jobs": 1,
    "landscape_count": 1,
    "portrait_count": 0,
    "jobs_by_space": {
      "model": [
        {
          "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\
...[truncated]...


## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/cases/output/rect_rotated_only/20260316-003354/print_summary.json
{
  "run_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_rotated_only\\20260316-003354",
  "work_dwg": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_rotated_only\\20260316-003354\\work\\rect_rotated_only__print_work.dwg",
  "plan_json": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_rotated_only\\20260316-003354\\print_plan.json",
  "plan": {
    "dwg_path": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_rotated_only\\20260316-003354\\work\\rect_rotated_only__print_work.dwg",
    "output_root": "D:\\codex-tasks\\cad\\scripts\\drawing_basic_service\\print\\cases\\output\\rect_rotated_only\\20260316-003354\\pdf",
    "total_jobs": 0,
    "landscape_count": 0,
    "portrait_count": 0,
    "jobs_by_space": {}
  },
  "execution": null,
  "verification": null
}
