# Layer Property

## 基本信息
- 来源：acad_aag, acadauto
- 类别：property
- 所属对象：Entity
- pywin32 写法：`str(getattr(ent, 'Layer', ''))`

## 作用
对象图层属性，是施工图过滤、统计和图签处理的重要筛选维度。

## 常见用法
- 按图层过滤打印框/文字/图签
- 图层切换

## 参数关注
- 无显式参数

## 返回
- str

## 前置条件
- 对象有效

## 常见风险
- 图层名存在大小写/历史命名差异

## 项目内建议路径
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`

## 相关任务
- `traverse_objects_and_read_identity`
- `manage_layers`

## 原始 CHM 命中页
- `About Assigning Layers, Colors, and Linetypes to Objects (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-D86DF08B-BBD3-4E0F-AB75-13B2C4AD972C.htm`
- `About Sorting Layers and Linetypes (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-72E0EC31-B232-4688-BFFF-CA10F42E1034.htm`
- `DefaultPlotStyleForLayer Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_defaultplotstyleforlayer.htm`
- `About Creating and Naming Layers (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-5B2CCA06-1A61-46F6-BABE-6B8BEA1DF20D.htm`
- `About Deleting Layers (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-463948A3-EE1E-4448-B3A6-B0B67B8902F1.htm`
