# AttributeReference Object

## 基本信息
- 来源：acadauto
- 类别：object
- 所属对象：BlockReference
- pywin32 写法：`for attr in block_ref.GetAttributes(): ...`

## 作用
块属性参照对象，承载 TagString 与 TextString。

## 常见用法
- 读取图号/图名/项目名
- 回写图签属性

## 参数关注
- 无显式参数

## 返回
- AttributeReference object

## 前置条件
- 块具有属性

## 常见风险
- TextString 含格式前缀
- 属性值为空

## 项目内建议路径
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `read_block_attributes`
- `update_titleblock_fields`

## 原始 CHM 命中页
- `AttributeReference object [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_attributeref_object.htm`
