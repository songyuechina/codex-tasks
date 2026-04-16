# AddText Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：ModelSpace / PaperSpace / Block
- pywin32 写法：`space.AddText(text, insert_point, height)`

## 作用
创建单行文字，适合简单目录或辅助标注。

## 常见用法
- 基础文字写入
- 验证文字样式链路

## 参数关注
- TextString
- InsertionPoint
- Height

## 返回
- Text object

## 前置条件
- 文字高度已确定

## 常见风险
- 文本样式/对齐后续还需设置

## 项目内建议路径
- `cad/scripts/Scheme_drawing/draw_building_outline.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `create_basic_geometry_smoke`
- `generate_or_update_catalog`

## 原始 CHM 命中页
- `AddText Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_addtext.htm`
- `AddText method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_addtext.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/addtext_see_also.htm`
