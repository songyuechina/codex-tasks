# BoundingBox Property

## 基本信息
- 来源：acadauto
- 类别：property
- 所属对象：Entity
- pywin32 写法：`entity.GetBoundingBox(min_pt, max_pt)`

## 作用
对象边界框信息，是打印框、角标和图签定位的核心基础。

## 常见用法
- 对象统计
- 图签匹配
- 窗口打印范围

## 参数关注
- out min
- out max

## 返回
- bounding points via out args

## 前置条件
- 对象支持边界框

## 常见风险
- 不同对象返回形式有差异

## 项目内建议路径
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `get_bounding_box_and_object_counts`
- `read_layout_plot_info`

## 原始 CHM 命中页
- `GetBoundingBox Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_getboundingbox.htm`
- `GetBoundingBox method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_getboundingbox.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/getboundingbox_see_also.htm`
