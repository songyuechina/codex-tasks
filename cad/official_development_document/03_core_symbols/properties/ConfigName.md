# ConfigName Property

## 基本信息
- 来源：acadauto
- 类别：property
- 所属对象：Layout
- pywin32 写法：`layout.ConfigName = printer_name`

## 作用
指定布局当前使用的打印设备，是打印设备与纸张介质链路中的第一关键属性。

## 常见用法
- 切换 PDF 打印设备
- 在读取可用纸张前先固定设备
- 布局打印前显式指定输出设备

## 参数关注
- 赋值为设备名字符串

## 返回
- 无显式返回

## 前置条件
- 已取得目标 `Layout`
- 已至少执行一次 `RefreshPlotDeviceInfo()`

## 常见风险
- 未刷新设备信息就赋值，后续纸张列表可能仍是旧设备
- 切换 `ConfigName` 后不再次刷新，`CanonicalMediaName` 可能失效

## 项目内建议路径
- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

## 相关任务
- `read_layout_plot_info`
- `execute_layout_plot`
- `build_print_plan_and_info`

## 原始 CHM 命中页
- `ConfigName Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_configname.htm`
- `ConfigName property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_configname.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/configname_see_also.htm`
