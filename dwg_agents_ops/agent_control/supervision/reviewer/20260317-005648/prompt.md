# Supervised Task Packet
role: reviewer
title: Review title-block analysis next step

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦 findings-first 审查，不要自行猜测工作区路径，严格基于主控提供的上下文回答。

## Objective
审查当前 title_block_analysis.py 的实现质量，重点看：1) 当前结果为何只落到 TQ1 候选而拿不到图纸名称/图号；2) 下一轮最值得先攻的技术点是什么；3) 是否有明显错误风险。请 findings-first。

## Context
真实案例最新结果：47/47 都能识别主图签候选块，多数为 TQ1；但 drawing_title/drawing_no/project_name 全为空。说明当前实现已完成候选块定位，但未拿到图签内容。请严格基于附件文件。

## File: D:/codex-tasks/cad/scripts/drawing_basic_service/print/title_block_analysis.py
# -*- coding: utf-8 -*-
"""title_block_analysis.py

研究从打印区域中提取图签区域与图纸名称信息，不直接影响当前打印主流程。

当前目标：
1. 尽量分出打印区域右下侧的图签区域
2. 优先识别属性块图签
3. 若不是属性块，则退化为普通块或局部文字分析
4. 为后续目录编制、PDF 重命名、排版服务提供结构化信息
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Optional
import argparse
import json
import re
import sys
import time


current = Path(__file__).resolve()
MODULE_DIR = current.parent
while current.name != "cad":
    if current.parent == current:
        raise Exception("找不到根目录 cad")
    current = current.parent
if str(current) not in sys.path:
    sys.path.insert(0, str(current))
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from system.licad import C
from system.CAD_core import open_dwg_paradigm
from system.CAD_coordination import wait_quiescent
from system.CAD_selection import ss_select
from system.common_logger import sys_logger

from print_policy import build_print_plan, plan_to_dict


TEXT_OBJECTS = {"AcDbText", "AcDbMText", "AcDbAttribute", "AcDbAttributeDefinition"}

TITLE_TAG_HINTS = (
    "图名",
    "图纸名称",
    "TITLE",
    "DWG_NAME",
    "SHEET_NAME",
)
NUMBER_TAG_HINTS = (
    "图纸编号",
    "图号",
    "DWG_NO",
    "DRAWING_NO",
    "SHEET_NO",
    "NO.",
)
PROJECT_TAG_HINTS = (
    "项目名称",
    "工程名称",
    "PROJECT",
    "工程名",
)
BLOCK_NAME_HINTS = ("图签", "TITLE", "SHEET", "TBLOCK", "BORDER")
LABEL_ONLY_TEXT_HINTS = (
    "图纸名称",
    "图名",
    "图号",
    "图纸编号",
    "工程名称",
    "项目名称",
    "审核",
    "校对",
    "设计",
    "制图",
    "日期",
    "比例",
    "专业",
    "阶段",
    "签字",
    "负责人",
)


@dataclass
class BlockSnapshot:
    handle: str
    block_name: str
    bbox: tuple[float, float, float, float]
    layer: str
    is_attribute_block: int
    attr_count: int
    attr_fields: dict[str, str]


@dataclass
class TextSnapshot:
    handle: str
    bbox: tuple[float, float, float, float]
    obj_name: str
    layer: str
    text: str


@dataclass
class TitleBlockCandidate:
    handle: str
    block_name: str
    bbox: tuple[float, float, float, float]
    side: str
    distance_to_corner: float
    is_attribute_block: int
    attr_count: int
    nearby_text_count: int
    extracted_fields: dict[str, str]
    hint_score: int
    band_score: float
    confidence: float


def _safe_handle(obj: Any) -> str:
    try:
        return str(obj.Handle)
    except Exception:
        return str(id(obj))


def _bbox_xy(ent: Any) -> tuple[float, float, float, float] | None:
    try:
        p1, p2 = ent.GetBoundingBox()
        min_x = min(float(p1[0]), float(p2[0]))
        min_y = min(float(p1[1]), float(p2[1]))
        max_x = max(float(p1[0]), float(p2[0]))
        max_y = max(float(p1[1]), float(p2[1]))
        return min_x, min_y, max_x, max_y
    except Exception:
        return None


def _dynamic_tol_from_bbox(print_bbox: tuple[float, float, float, float]) -> float:
    short_side = min(print_bbox[2] - print_bbox[0], print_bbox[3] - print_bbox[1])
    return max(short_side * 0.0005, 1.0)


def _distance_to_right_bottom_corner(
    print_bbox: tuple[float, float, float, float],
    ent_bbox: tuple[float, float, float, float],
) -> tuple[str, float]:
    px1, py1, px2, py2 = print_bbox
    ex1, ey1, ex2, ey2 = ent_bbox
    distance = ((ex2 - px2) ** 2 + (ey1 - py1) ** 2) ** 0.5
    side = "right" if abs(ex2 - px2) <= abs(ey1 - py1) else "bottom"
    return side, distance


def _iter_space_entities(owner_btr_name: str) -> Iterable[Any]:
    doc = C.doc
    if owner_btr_name == "*MODEL_SPACE":
        for ent in doc.ModelSpace:
            yield ent
        return

    for layout in doc.Layouts:
        try:
            if str(layout.Block.Name) == owner_btr_name:
                for ent in layout.Block:
                    yield ent
                return
        except Exception:
            continue


def _find_layout_by_owner_btr(owner_btr_name: str):
    if owner_btr_name == "*MODEL_SPACE":
        try:
            return C.doc.Layouts.Item("Model")
        except Exception:
            return None
    for layout in C.doc.Layouts:
        try:
            if str(layout.Block.Name) == owner_btr_name:
                return layout
        except Exception:
            continue
    return None


def _activate_space_for_owner(owner_btr_name: str) -> bool:
    layout = _find_layout_by_owner_btr(owner_btr_name)
    if layout is None:
        return False
    try:
        C.doc.ActiveLayout = layout
    except Exception:
        return False
    try:
        C.doc.MSpace = owner_btr_name == "*MODEL_SPACE"
    except Exception:
        pass
    time.sleep(0.2)
    return True


def _clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.replace("\\P", " ").replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _clean_attr_value(value: str) -> str:
    text = _clean_text(value)
    if text.startswith("\\") and ";" in text:
        _, right = text.split(";", 1)
        text = right.strip()
    return text


def _extract_attribute_fields(block_ref: Any) -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        if not block_ref.HasAttributes:
            return out
        for attr in block_ref.GetAttributes():
            tag = str(getattr(attr, "TagString", "")).strip()
            value = _clean_attr_value(str(getattr(attr, "TextString", "")).strip())
            if tag and value:
                out[tag] = value
    except Exception:
        return out
    return out


def _extract_text_string(ent: Any) -> str:
    try:
        return _clean_text(str(ent.TextString))
    except Exception:
        return ""


def _build_text_snapshots_from_entities(entities: list[Any]) -> list[TextSnapshot]:
    text_snapshots: list[TextSnapshot] = []
    for ent in entities:
        bbox = _bbox_xy(ent)
        if bbox is None:
            continue
        obj_name = str(getattr(ent, "ObjectName", ""))
        if obj_name not in TEXT_OBJECTS:
            continue
        try:
            layer = str(ent.Layer)
        except Exception:
            layer = ""
        text = _extract_text_string(ent)
        if text:
            text_snapshots.append(
                TextSnapshot(
                    handle=_safe_handle(ent),
                    bbox=bbox,
                    obj_name=obj_name,
                    layer=layer,
                    text=text,
                )
            )
    text_snapshots.sort(key=lambda item: item.bbox[0])
    return text_snapshots


def collect_space_title_snapshots(owner_btr_name: str) -> tuple[list[BlockSnapshot], list[TextSnapshot]]:
    block_snapshots: list[BlockSnapshot] = []

    if not _activate_space_for_owner(owner_btr_name):
        sys_logger.warning(f"无法激活图签分析空间: owner={owner_btr_name}")
        return block_snapshots, []

    try:
        block_entities = ss_select("all", filter_types=[0], filter_data=["INSERT"], autocast=True) or []
    except Exception as exc:
        sys_logger.warning(f"块选择集采样失败: owner={owner_btr_name} err={exc}")
        block_entities = []

    for ent in block_entities:
        bbox = _bbox_xy(ent)
        if bbox is None:
            continue

        obj_name = str(getattr(ent, "ObjectName", ""))
        try:
            layer = str(ent.Layer)
        except Exception:
            layer = ""

        if obj_name == "AcDbBlockReference":
            try:
                block_name = str(getattr(ent, "EffectiveName", getattr(ent, "Name", "")))
            except Exception:
                block_name = str(getattr(ent, "Name", ""))
            attrs = _extract_attribute_fields(ent)
            block_snapshots.append(
                BlockSnapshot(
                    handle=_safe_handle(ent),
                    block_name=block_name,
                    bbox=bbox,
                    layer=layer,
                    is_attribute_block=int(bool(attrs)),
                    attr_count=len(attrs),
                    attr_fields=attrs,
                )
            )
    block_snapshots.sort(key=lambda item: item.bbox[0])
    return block_snapshots, []


def select_text_snapshots_in_region(
    owner_btr_name: str,
    region_bbox: tuple[float, float, float, float],
) -> list[TextSnapshot]:
    if not _activate_space_for_owner(owner_btr_name):
        return []
    p1 = (region_bbox[0], region_bbox[1], 0.0)
    p2
...[middle truncated]...
963.63035286992,
            -570764.6899297202,
            76549.11310248554
          ],
          "side": "right",
          "distance_to_corner": 1000.215,
          "is_attribute_block": 0,
          "attr_count": 0,
          "nearby_text_count": 0,
          "extracted_fields": {},
          "hint_score": 0,
          "band_score": 2.633,
          "confidence": 5.383,
          "corner_tol": 21.0,
          "preferred": 0
        },
        "field_source": "none",
        "drawing_title": "",
        "drawing_no": "",
        "project_name": "",
        "confidence": 5.383,
        "candidate_count": 1,
        "candidate_blocks": [
          {
            "handle": "B739",
            "block_name": "TQ1",
            "bbox": [
              -576846.2939021017,
              35963.63035286992,
              -570764.6899297202,
              76549.11310248554
            ],
            "side": "right",
            "distance_to_corner": 1000.215,
            "is_attribute_block": 0,
            "attr_count": 0,
            "nearby_text_count": 0,
            "extracted_fields": {},
            "hint_score": 0,
            "band_score": 2.633,
            "confidence": 5.383,
            "corner_tol": 21.0,
            "preferred": 0
          }
        ],
        "nearby_texts": []
      },
      {
        "sequence_no": 5,
        "layout_name": "model",
        "space_kind": "model",
        "owner_btr": "*MODEL_SPACE",
        "handle": "A58F",
        "print_bbox": [
          -688857.619265442,
          -43902.50536741951,
          -604757.619265442,
          15497.494632580492
        ],
        "title_block_found": 1,
        "selected_candidate": {
          "handle": "B6B2",
          "block_name": "TQ1",
          "bbox": [
            -614358.6641514631,
            -42901.97382759012,
            -605757.619265442,
            14496.955868514371
          ],
          "side": "right",
          "distance_to_corner": 1414.589,
          "is_attribute_block": 0,
          "attr_count": 0,
          "nearby_text_count": 0,
          "extracted_fields": {},
          "hint_score": 0,
          "band_score": 2.633,
          "confidence": 5.279,
          "corner_tol": 29.7,
          "preferred": 0
        },
        "field_source": "none",
        "drawing_title": "",
        "drawing_no": "",
        "project_name": "",
        "confidence": 5.279,
        "candidate_count": 3,
        "candidate_blocks": [
          {
            "handle": "B6B2",
            "block_name": "TQ1",
            "bbox": [
              -614358.6641514631,
              -42901.97382759012,
              -605757.619265442,
              14496.955868514371
            ],
            "side": "right",
            "distance_to_corner": 1414.589,
            "is_attribute_block": 0,
            "attr_count": 0,
            "nearby_text_count": 0,
            "extracted_fields": {},
            "hint_score": 0,
            "band_score": 2.633,
            "confidence": 5.279,
            "corner_tol": 29.7,
            "preferred": 0
          },
          {
            "handle": "BC16",
            "block_name": "_INDEX",
            "bbox": [
              -628351.3705095359,
              -27705.211009123595,
              -627601.3705095359,
              -26955.211009123595
            ],
            "side": "right",
            "distance_to_corner": 28003.38,
            "is_attribute_block": 1,
            "attr_count": 2,
            "nearby_text_count": 0,
            "extracted_fields": {
              "1": "-",
              "-": "6-9"
            },
            "hint_score": 0,
            "band_score": 0.0,
            "confidence": 0.0,
            "corner_tol": 29.7,
            "preferred": 0
          },
          {
            "handle": "BC0C",
            "block_name": "_INDEX",
            "bbox": [
              -624385.5896234226,
              -15675.642504488707,
              -623635.5896234226,
              -14925.642504488707
            ],
            "side": "right",
            "distance_to_corner": 33957.82,
            "is_attribute_block": 1,
            "attr_count": 2,
            "nearby_text_count": 0,
            "extracted_fields": {
              "1": "-",
              "-": "15"
            },
            "hint_score": 0,
            "band_score": 0.0,
            "confidence": 0.0,
            "corner_tol": 29.7,
            "preferred": 0
          }
        ],
        "nearby_texts": []
      },
      {
        "sequence_no": 6,
        "layout_name": "model",
        "space_kind": "model",
        "owner_btr": "*MODEL_SPACE",
        "handle": "A590",
        "print_bbox": [
          -604757.619265442,
          -43902.50536741951,
          -520657.6192654421,
          15497.494632580492
        ],
        "title_block_found": 1,
        "selected_candidate": {
          "handle": "B6C3",
          "block_name": "TQ1",
          "bbox": [
            -530258.6641514631,
            -42901.97382759,
            -521657.619265442,
            14496.955868514488
          ],
          "side": "right",
          "distance_to_corner": 1414.589,
          "is_attribute_block": 0,
          "attr_count": 0,
          "nearby_text_count": 0,
          "extracted_fields": {},
          "hint_score": 0,
          "band_score": 2.633,
          "confidence": 5.279,
          "corner_tol": 29.7,
          "preferred": 0
        },
        "field_source": "none",
        "drawing_title": "",
        "drawing_no": "",
        "project_name": "",
        "confidence": 5.279,
        "candidate_count": 3,
        "candidate_blocks": [
          {
            "handle": "B6C3",
            "block_name": "TQ1",
            "bbox": [
              -530258.6641514631,
              -42901.97382759,
              -521657.619265442,
              14496.955868514488
            ],
            "side": "right",
            "distance_to_corner": 1414.589,
            "is_attribute_block": 0,
            "attr_count": 0,
            "nearby_text_count": 0,
            "extracted_fields": {},
            "hint_score": 0,
            "band_score": 2.633,
            "confidence": 5.279,
            "corner_tol": 29.7,
            "preferred": 0
          },
          {
            "handle": "B531",
            "block_name": "_INDEX",
            "bbox": [
              -567133.1668713634,
              1888.873216015898,
              -566383.1668713634,
              2638.873216015898
            ],
            "side": "right",
            "distance_to_corner": 64712.256,
            "is_attribute_block": 1,
            "attr_count": 2,
            "nearby_text_count": 0,
            "extracted_fields": {
              "1": "-",
              "-": "59"
            },
            "hint_score": 0,
            "band_score": 0.0,
            "confidence": 0.0,
            "corner_tol": 29.7,
            "preferred": 0
          },
          {
            "handle": "B52D",
            "block_name": "_INDEX",
            "bbox": [
              -567883.1668713634,
              1888.873216015898,
              -567133.1668713634,
              2638.873216015898
            ],
            "side": "right",
            "distance_to_corner": 65244.363,
            "is_attribute_block": 1,
            "attr_count": 2,
            "nearby_text_count": 0,
            "extracted_fields": {
              "1": "-",
              "-": "56"
            },
            "hint_score": 0,
            "band_score": 0.0,
            "confidence": 0.0,
            "corner_tol": 29.7,
            "preferred": 0
          }
        ],
        "nearby_texts": []
      },
      {
        "sequence_no": 7,
        "layout_name": "model",
        "space_kind": "model",
        "owner_btr": "*MODEL_SPACE",
        "handle": "BC27",
        "print_bbox": [
          -520657.6192654421,
          -43902.50536741951,
          -436557.6192654421,
          15497.494632580492
        ],
        "title_block_found": 1,
        "selected_candidate": {
          "handle": "BC79",
          "block_name": "TQ1",
          "bbox": [
            -446158.6641514631,
            -42901.97382759012,
            -437557.619265442,
            14496.955868514371
          ],
          "side": "right",
          "distance_to_corner": 1414.589,
          "is_attribute_block": 0,
          "attr_count": 0,
          "nearby_text_count": 0,
          "extracted_fields": {},
          "hint_score": 0,
          "band_score": 2.633,
          "confidence": 5.279,
          "corner_tol": 29.7,
          "preferred": 0
        },
        "field_source": "none",
        "drawing_title": "",
        "drawing_no": "",
        "project_name": "",
        "confidence": 5.279,
        "candidate_count": 1,
        "candidate_blocks": [
          {
            "handle": "BC79",
            "block_name": "TQ1",
            "bbox": [
              -446158.6641514
...[truncated]...
