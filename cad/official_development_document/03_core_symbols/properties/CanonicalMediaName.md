# CanonicalMediaName Property

## 基本信息
- 来源：acadauto
- 类别：property
- 所属对象：Layout
- pywin32 写法：`layout.CanonicalMediaName = media_name`

## 作用
指定布局当前使用的标准纸张介质名，是打印纸张、窗口输出和页面尺寸稳定性的关键属性。

## 常见用法
- 在确定设备后指定纸张
- 读取打印配置时回读当前介质名
- 布局打印前固定页面尺寸

## 参数关注
- 赋值为设备支持的 canonical media name

## 返回
- 无显式返回

## 前置条件
- 已固定 `ConfigName`
- 已在设备切换后再次执行 `RefreshPlotDeviceInfo()`

## 常见风险
- 设备和纸张介质强绑定，切设备后旧介质名会失效
- 没先刷新设备列表就设置介质名，容易 silently fail

## 项目内建议路径
- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

## 相关任务
- `read_layout_plot_info`
- `execute_layout_plot`
- `build_print_plan_and_info`

## 原始 CHM 命中页
- `CanonicalMediaName Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_canonicalmedianame.htm`
- `CanonicalMediaName property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_canonicalmedianame.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/canonicalmedianame_see_also.htm`
