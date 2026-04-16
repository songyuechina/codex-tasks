# SelectionSet Object

## 基本信息
- 来源：acadauto
- 类别：object
- 所属对象：SelectionSets
- pywin32 写法：`ss = C.doc.SelectionSets.Add(name)`

## 作用
单个选择集对象，用于承载筛出的实体集合。

## 常见用法
- Select()
- 遍历已选对象

## 参数关注
- 无显式参数

## 返回
- SelectionSet object

## 前置条件
- 先清理旧同名集合

## 常见风险
- 选区模式不对
- 返回对象需做属性兼容处理

## 项目内建议路径
- `cad/system/CAD_selection.py`

## 相关任务
- `build_selection_set`
- `traverse_objects_and_read_identity`

## 原始 CHM 命中页
- `SelectionSets Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_selectionsets.htm`
- `ActiveSelectionSet Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_activeselectionset.htm`
- `PickfirstSelectionSet Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_pickfirstselectionset.htm`
- `ActiveSelectionSet property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_activeselectionset.htm`
- `PickfirstSelectionSet property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_pickfirstselectionset.htm`
