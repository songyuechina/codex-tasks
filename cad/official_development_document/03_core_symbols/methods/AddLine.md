# AddLine Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：ModelSpace / PaperSpace / Block
- pywin32 写法：`space.AddLine(start_point, end_point)`

## 作用
创建直线，是 COM 链路健康和基础几何创建的典型烟雾测试。

## 常见用法
- 连接验证
- 施工图辅助构造

## 参数关注
- StartPoint
- EndPoint

## 返回
- Line object

## 前置条件
- 三维点格式正确

## 常见风险
- 点参数错误
- 空间选错

## 项目内建议路径
- `cad/system/licad.py`

## 相关任务
- `create_basic_geometry_smoke`

## 原始 CHM 命中页
- `AddLine Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_addline.htm`
- `AddLine method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_addline.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/addline_see_also.htm`
