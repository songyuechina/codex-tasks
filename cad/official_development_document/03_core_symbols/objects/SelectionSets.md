# SelectionSets Object

## 基本信息
- 来源：acadauto
- 类别：object
- 所属对象：Document
- pywin32 写法：`C.doc.SelectionSets`

## 作用
选择集集合，用于创建、删除和复用命名选择集。

## 常见用法
- 先删旧集合再 Add
- 窗口选、交叉选

## 参数关注
- 无显式参数

## 返回
- SelectionSets collection

## 前置条件
- 文档已就绪

## 常见风险
- 同名集合残留
- 命令态下选择异常

## 项目内建议路径
- `cad/system/CAD_selection.py`
- `cad/system/CAD_core.py`

## 相关任务
- `build_selection_set`

## 原始 CHM 命中页
- `SelectionSets Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_selectionsets.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/selectionsets_see_also.htm`
- `SelectionSets Collection object [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_selectionsets_collection.htm`
- `SelectionSets property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_selectionsets.htm`
