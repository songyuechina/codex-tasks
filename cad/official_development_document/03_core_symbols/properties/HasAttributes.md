# HasAttributes Property

## 基本信息
- 来源：acadauto
- 类别：property
- 所属对象：BlockReference
- pywin32 写法：`bool(block_ref.HasAttributes)`

## 作用
判定块参照是否具有可读取属性。

## 常见用法
- GetAttributes 前置判断

## 参数关注
- 无显式参数

## 返回
- bool

## 前置条件
- 对象确认为 BlockReference

## 常见风险
- 对象类型不对时读取异常

## 项目内建议路径
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `read_block_attributes`
- `update_titleblock_fields`

## 原始 CHM 命中页
- `HasAttributes Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_hasattributes.htm`
- `HasAttributes property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_hasattributes.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/hasattributes_see_also.htm`
