# Layers Object

## 基本信息
- 来源：acad_aag
- 类别：object
- 所属对象：Document
- pywin32 写法：`C.doc.Layers`

## 作用
图层集合，用于读取、创建、切换、锁定或解冻图层。

## 常见用法
- Item(name)
- Add(name)

## 参数关注
- 无显式参数

## 返回
- Layers collection

## 前置条件
- 文档已就绪

## 常见风险
- 当前活动图层被冻结或锁定

## 项目内建议路径
- `cad/scripts/CAD_basic.py`
- `cad/scripts/Scheme_drawing/draw_building_outline.py`

## 相关任务
- `manage_layers`

## 原始 CHM 命中页
- `About Assigning Layers, Colors, and Linetypes to Objects (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-D86DF08B-BBD3-4E0F-AB75-13B2C4AD972C.htm`
- `About Sorting Layers and Linetypes (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-72E0EC31-B232-4688-BFFF-CA10F42E1034.htm`
- `About Creating and Naming Layers (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-5B2CCA06-1A61-46F6-BABE-6B8BEA1DF20D.htm`
- `About Deleting Layers (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-463948A3-EE1E-4448-B3A6-B0B67B8902F1.htm`
- `About Freezing and Thawing Layers (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-A1815C41-7753-45F5-B8BC-31F67F79F138.htm`
