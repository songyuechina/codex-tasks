# SetWindowToPlot Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：Layout
- pywin32 写法：`layout.SetWindowToPlot(lower_left, upper_right)`

## 作用
设置布局打印窗口，适合按框选边界输出 PDF。

## 常见用法
- 按打印框输出
- 布局窗口打印

## 参数关注
- LowerLeft
- UpperRight

## 返回
- None

## 前置条件
- 窗口点已按当前布局坐标准备好

## 常见风险
- 布局空间下顺序/刷新不对时容易失效

## 项目内建议路径
- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`

## 相关任务
- `execute_layout_plot`

## 原始 CHM 命中页
- `SetWindowToPlot Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_setwindowtoplot.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/setwindowtoplot_see_also.htm`
- `SetWindowToPlot method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_setwindowtoplot.htm`
