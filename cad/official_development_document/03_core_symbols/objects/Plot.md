# Plot Object

## 基本信息
- 来源：acad_aag, acadauto
- 类别：object
- 所属对象：Document
- pywin32 写法：`C.doc.Plot`

## 作用
打印输出对象，用于文件输出、QuietErrorMode 和打印执行控制。

## 常见用法
- PlotToFile
- QuietErrorMode

## 参数关注
- 无显式参数

## 返回
- Plot object

## 前置条件
- 布局和打印参数已准备好

## 常见风险
- 设备未刷新
- 输出文件被占用

## 项目内建议路径
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `execute_layout_plot`

## 原始 CHM 命中页
- `Define and Plot Layouts` -> `01_extracted_html/acad_aag/topichead_9.htm`
- `LayoutShowPlotSetup Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_layoutshowplotsetup.htm`
- `SetLayoutsToPlot Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_setlayoutstoplot.htm`
- `DefaultPlotStyleForLayer Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_defaultplotstyleforlayer.htm`
- `About the Preferences, Plot, and Utility Objects (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-9091E614-25B8-452E-A67A-301939B52161.htm`
