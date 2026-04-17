# Elevation

## 基本信息
- kind: `property`
- owners: `Hatch, Polyline, Section`
- pywin32: `entity.Elevation`

## 作用
表示对象当前高程，用于把仅含 XY 的对象点恢复为完整的 3D 空间点。

## 高频场景
- 补全 OCS/WCS 转换中的 Z 值
- 读取多段线或剖切对象高程
- 还原对象空间位置

## 项目路径
- `cad/system/licad.py`
- `cad/system/content_analysis_dwg_file.py`

## 相关任务
- `understand_and_convert_coordinate_systems`
- `read_3d_object_spatial_identity`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_elevation`
- `acadauto:idh_translatecoordinates`
- `acadauto:ex_translatecoordinates`
- `acadauto:translatecoordinates_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_translatecoordinates.htm`
- `01_extracted_html/acadauto/idh_elevation.htm`
- `01_extracted_html/acadauto/idh_translatecoordinates.htm`
- `01_extracted_html/acadauto/translatecoordinates_see_also.htm`
