# AddPolyline Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：ModelSpace / PaperSpace / Block
- pywin32 写法：`space.AddPolyline(points)`

## 作用
创建多段线，是打印框、边框、目录格线等常见结构的基础。

## 常见用法
- 施工图框线
- 打印区域构造

## 参数关注
- Coordinates array

## 返回
- Polyline object

## 前置条件
- 点数组顺序正确

## 常见风险
- 坐标数组格式错误

## 项目内建议路径
- `cad/scripts/CAD_basic.py`

## 相关任务
- `create_basic_geometry_smoke`

## 原始 CHM 命中页
- `AddPolyline Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_addpolyline.htm`
- `AddLightWeightPolyline Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_addlightweightpolyline.htm`
- `AddLightWeightPolyline method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_addlightweightpolyline.htm`
- `AddPolyline method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_addpolyline.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/addlightweightpolyline_see_also.htm`
