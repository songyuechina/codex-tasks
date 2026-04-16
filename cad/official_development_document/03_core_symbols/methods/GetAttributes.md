# GetAttributes Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：BlockReference
- pywin32 写法：`block_ref.GetAttributes()`

## 作用
读取块参照上的属性对象集合。

## 常见用法
- 图签字段提取
- 目录模板字段扫描

## 参数关注
- 无显式参数

## 返回
- AttributeReference collection

## 前置条件
- 先判 HasAttributes

## 常见风险
- 直接调用报错
- 属性文本需清洗

## 项目内建议路径
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `read_block_attributes`
- `update_titleblock_fields`

## 原始 CHM 命中页
- `GetAttributes Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_getattributes.htm`
- `GetAttributes method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_getattributes.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/getattributes_see_also.htm`
