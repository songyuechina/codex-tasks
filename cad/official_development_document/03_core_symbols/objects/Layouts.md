# Layouts Object

## 基本信息
- 来源：acad_aag, acadauto
- 类别：object
- 所属对象：Document
- pywin32 写法：`C.doc.Layouts`

## 作用
布局集合，负责枚举和按名称获取布局对象。

## 常见用法
- for layout in C.doc.Layouts
- C.doc.Layouts.Item(name)

## 参数关注
- 无显式参数

## 返回
- Layouts collection

## 前置条件
- 文档已打开

## 常见风险
- 遍历顺序不一定等于标签页顺序

## 项目内建议路径
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`

## 相关任务
- `enumerate_layouts`
- `switch_to_target_layout`

## 原始 CHM 命中页
- `About Layouts and Blocks (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `Define and Plot Layouts` -> `01_extracted_html/acad_aag/topichead_9.htm`
- `LayoutShowPlotSetup Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_layoutshowplotsetup.htm`
- `SetLayoutsToPlot Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_setlayoutstoplot.htm`
- `About Layouts (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-10344852-4888-4237-8EB6-5EBE24D5C87C.htm`
