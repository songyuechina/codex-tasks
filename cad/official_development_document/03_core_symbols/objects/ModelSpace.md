# ModelSpace Object

## 基本信息
- 来源：acadauto
- 类别：object
- 所属对象：Document
- pywin32 写法：`C.doc.ModelSpace`

## 作用
模型空间对象容器，适合施工图实体创建和全局扫描。

## 常见用法
- AddLine
- InsertBlock
- 对象遍历

## 参数关注
- 无显式参数

## 返回
- Block-like collection

## 前置条件
- 文档已就绪

## 常见风险
- 把布局空间对象误当作模型空间对象

## 项目内建议路径
- `cad/system/licad.py`
- `cad/system/CAD_selection.py`

## 相关任务
- `determine_space_and_layout`
- `create_basic_geometry_smoke`

## 原始 CHM 命中页
- `ElevationModelSpace Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_elevationmodelspace.htm`
- `ModelSpace Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_modelspace.htm`
- `ElevationModelSpace property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_elevationmodelspace.htm`
- `ModelSpace Entities Collection object [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_modelspace_collection.htm`
- `ModelSpace property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_modelspace.htm`
