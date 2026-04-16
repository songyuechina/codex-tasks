# Regen Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：Document
- pywin32 写法：`C.doc.Regen(mode)`

## 作用
刷新图形显示与数据库状态，适合打印前和批量修改后归一。

## 常见用法
- 修改后刷新
- 打印前归一

## 参数关注
- Regen mode

## 返回
- None

## 前置条件
- 上下文稳定

## 常见风险
- 频繁调用拖慢批处理

## 项目内建议路径
- `cad/system/CAD_core.py`

## 相关任务
- `execute_layout_plot`

## 原始 CHM 命中页
- `ObjectSortByRegens Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_objectsortbyregens.htm`
- `Regen Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_regen.htm`
- `RegenerateTableSuppressed Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_regeneratetablesuppressed.htm`
- `ObjectSortByRegens property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_objectsortbyregens.htm`
- `Regen method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_regen.htm`
