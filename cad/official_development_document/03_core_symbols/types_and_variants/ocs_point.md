# ocs_point

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `(x, y[, z]) + Elevation + Normal -> 3D WCS point`

## 作用
统一说明对象局部坐标点如何结合 Elevation 与 Normal 还原为空间点。

## 高频场景
- 从 Polyline/LightweightPolyline 读取 OCS 点
- 结合 Elevation 与 Normal 转到 WCS
- 避免直接把 OCS 点当 WCS 点

## 项目路径
- `cad/system/content_analysis_dwg_file.py`
- `cad/system/licad.py`

## 相关任务
- `understand_and_convert_coordinate_systems`
- `read_3d_object_spatial_identity`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:idh_translatecoordinates`
- `acadauto:idh_normal`
- `acadauto:idh_elevation`
- `acadauto:ex_translatecoordinates`
- `acadauto:ex_elevationmodelspace`
- `acadauto:ex_elevationpaperspace`
- `acadauto:ex_elevation`
- source_html_paths:
- `01_extracted_html/acadauto/ex_translatecoordinates.htm`
- `01_extracted_html/acadauto/ex_elevationmodelspace.htm`
- `01_extracted_html/acadauto/ex_elevationpaperspace.htm`
- `01_extracted_html/acadauto/ex_elevation.htm`
- `01_extracted_html/acadauto/idh_elevation.htm`
- `01_extracted_html/acadauto/idh_translatecoordinates.htm`
- `01_extracted_html/acadauto/idh_normal.htm`
