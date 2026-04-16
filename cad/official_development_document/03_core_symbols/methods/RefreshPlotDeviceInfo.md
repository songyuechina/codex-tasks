# RefreshPlotDeviceInfo Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：Layout
- pywin32 写法：`layout.RefreshPlotDeviceInfo()`

## 作用
刷新布局的打印设备和介质信息，是布局打印前的重要准备动作。

## 常见用法
- 设置设备后刷新
- 读取纸张前刷新

## 参数关注
- 无显式参数

## 返回
- None

## 前置条件
- 布局对象已取得

## 常见风险
- 刷新顺序不对导致打印设置失效

## 项目内建议路径
- `cad/scripts/CAD_basic.py`

## 相关任务
- `read_layout_plot_info`
- `execute_layout_plot`

## 原始 CHM 命中页
- `RefreshPlotDeviceInfo Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_refreshplotdeviceinfo.htm`
- `RefreshPlotDeviceInfo method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_refreshplotdeviceinfo.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/refreshplotdeviceinfo_see_also.htm`
