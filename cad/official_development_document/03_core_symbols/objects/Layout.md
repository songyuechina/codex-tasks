# Layout Object

## 基本信息
- 来源：acad_aag, acadauto
- 类别：object
- 所属对象：Layouts / Document
- pywin32 写法：`layout = C.doc.Layouts.Item(layout_name)`

## 作用
单个布局对象，承载打印设备、纸张、窗口范围等核心信息。

## 常见用法
- RefreshPlotDeviceInfo
- SetWindowToPlot
- Name

## 参数关注
- 无显式参数

## 返回
- Layout object

## 前置条件
- 布局名有效

## 常见风险
- 布局名大小写/空白不一致
- 切换时 Busy

## 项目内建议路径
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`

## 相关任务
- `switch_to_target_layout`
- `read_layout_plot_info`
- `execute_layout_plot`

## 原始 CHM 命中页
- `About Layouts and Blocks (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `Define and Plot Layouts` -> `01_extracted_html/acad_aag/topichead_9.htm`
- `LayoutShowPlotSetup Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_layoutshowplotsetup.htm`
- `SetLayoutsToPlot Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_setlayoutstoplot.htm`
- `About Layouts (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-10344852-4888-4237-8EB6-5EBE24D5C87C.htm`
