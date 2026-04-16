# Coordinates Property

## 基本信息
- 来源：acad_aag, acadauto
- 类别：property
- 所属对象：Polyline / Line / Curve-like entities
- pywin32 写法：`entity.Coordinates`

## 作用
读取对象坐标数组，用于边界框、打印区域、多段线判断。

## 常见用法
- 打印框识别
- 几何统计

## 参数关注
- 无显式参数

## 返回
- array/tuple-like

## 前置条件
- 对象类型支持 Coordinates

## 常见风险
- 返回值需要按偶数对解释

## 项目内建议路径
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`

## 相关任务
- `get_bounding_box_and_object_counts`

## 原始 CHM 命中页
- `About Converting Coordinates (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-06B18EED-D4E3-4B81-ACB8-037E884CB93D.htm`
- `About Specifying 3D Coordinates (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-6954AAF3-7107-4D93-A2CE-FE859F3F9902.htm`
- `Coordinates Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_coordinates.htm`
- `TranslateCoordinates Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_translatecoordinates.htm`
- `Coordinates property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_coordinates.htm`
