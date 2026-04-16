# ActiveLayout Property

## 基本信息
- 来源：acadauto
- 类别：property
- 所属对象：Document
- pywin32 写法：`C.doc.ActiveLayout = C.doc.Layouts.Item(layout_name)`

## 作用
当前活动布局，是布局切换和布局打印的核心属性。

## 常见用法
- 读当前布局名
- 写入目标布局对象

## 参数关注
- Layout object on write

## 返回
- Layout object

## 前置条件
- 目标布局对象有效

## 常见风险
- 切换成功但上下文未完全同步

## 项目内建议路径
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`

## 相关任务
- `switch_to_target_layout`
- `determine_space_and_layout`

## 原始 CHM 命中页
- `ActiveLayout Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_activelayout.htm`
- `ActiveLayout property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_activelayout.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/activelayout_see_also.htm`
