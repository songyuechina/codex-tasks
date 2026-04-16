# Select Method

## 基本信息
- 来源：acad_aag, acadauto
- 类别：method
- 所属对象：SelectionSet
- pywin32 写法：`ss.Select(mode, p1, p2, filter_types, filter_data)`

## 作用
按窗口、交叉、过滤条件填充选择集。

## 常见用法
- 打印框扫描
- 对象窗口选择

## 参数关注
- Mode
- Point1
- Point2
- FilterType
- FilterData

## 返回
- 填充后的 SelectionSet

## 前置条件
- 模式和过滤数组正确

## 常见风险
- 过滤类型不兼容
- 坐标窗口错位

## 项目内建议路径
- `cad/system/CAD_selection.py`
- `cad/system/CAD_core.py`

## 相关任务
- `build_selection_set`

## 原始 CHM 命中页
- `SelectionSets Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_selectionsets.htm`
- `ActiveSelectionSet Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_activeselectionset.htm`
- `PickfirstSelectionSet Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_pickfirstselectionset.htm`
- `About Adding Objects to a Selection Set (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-2709CA2D-509E-4C55-AD48-3F8303AF6E8D.htm`
- `About Creating a Selection Set (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-F23DA291-5F68-4DAA-BA2B-A92A4A8D2942.htm`
