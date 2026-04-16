# BlockReference Object

## 基本信息
- 来源：acadauto
- 类别：object
- 所属对象：ModelSpace / PaperSpace / Block
- pywin32 写法：`if ent.ObjectName == 'AcDbBlockReference': ...`

## 作用
块参照对象，是图签、角标、目录模板等核心载体。

## 常见用法
- GetAttributes()
- Name/ObjectName 判断
- 定位图签实例

## 参数关注
- 无显式参数

## 返回
- BlockReference object

## 前置条件
- 对象类型识别正确

## 常见风险
- 动态块名/匿名块
- 属性块与无属性块混在一起

## 项目内建议路径
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `read_block_attributes`
- `update_titleblock_fields`

## 原始 CHM 命中页
- `DynamicBlockReferenceProperty object [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_dynamicblockreferenceproperty_object.htm`
