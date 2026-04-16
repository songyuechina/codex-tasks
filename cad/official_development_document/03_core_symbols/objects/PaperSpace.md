# PaperSpace Object

## 基本信息
- 来源：acadauto
- 类别：object
- 所属对象：Document
- pywin32 写法：`C.doc.PaperSpace`

## 作用
图纸空间对象容器，适合布局对象处理和布局打印相关操作。

## 常见用法
- 布局块枚举
- 布局图签/边框扫描

## 参数关注
- 无显式参数

## 返回
- Block-like collection

## 前置条件
- 布局上下文明确

## 常见风险
- ActiveLayout 切换成功但空间理解仍错误

## 项目内建议路径
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

## 相关任务
- `determine_space_and_layout`
- `read_layout_plot_info`

## 原始 CHM 命中页
- `ElevationPaperSpace Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_elevationpaperspace.htm`
- `PaperSpace Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_paperspace.htm`
- `ElevationPaperSpace property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_elevationpaperspace.htm`
- `PaperSpace Entities Collection object [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_paperspace_collection.htm`
- `PaperSpace property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_paperspace.htm`
