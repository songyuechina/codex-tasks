# AddMText Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：ModelSpace / PaperSpace / Block
- pywin32 写法：`space.AddMText(insert_point, width, text)`

## 作用
创建多行文字，适合目录表头和图签长文本场景。

## 常见用法
- 目录内容
- 图签长字段

## 参数关注
- InsertionPoint
- Width
- Text

## 返回
- MText object

## 前置条件
- 宽度和换行策略明确

## 常见风险
- 格式控制码影响读取

## 项目内建议路径
- `cad/scripts/CAD_basic.py`

## 相关任务
- `generate_or_update_catalog`
- `update_titleblock_fields`

## 原始 CHM 命中页
- `AddMtext Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_addmtext.htm`
- `AddMtext method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_addmtext.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/addmtext_see_also.htm`
