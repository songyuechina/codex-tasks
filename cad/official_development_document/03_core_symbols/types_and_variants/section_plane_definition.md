# section_plane_definition

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `(point1, point2, point3) in 3D WCS`

## 作用
统一说明剖切平面由三个 3D 点定义，避免把视向或法向误当平面定义。

## 高频场景
- 给 SectionSolid 定义剖切平面
- 组织剖面表达的输入
- 统一构件截面提取规则

## 项目路径
- `cad/system/licad.py`
- `cad/system/content_analysis_dwg_file.py`

## 相关任务
- `section_3d_geometry_for_2d_expression`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:idh_sectionsolid`
- `acadauto:idh_3dsolid_object`
- `acadauto:ex_sectionsolid`
- `acadauto:sectionsolid_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_sectionsolid.htm`
- `01_extracted_html/acadauto/idh_sectionsolid.htm`
- `01_extracted_html/acadauto/sectionsolid_see_also.htm`
- `01_extracted_html/acadauto/idh_3dsolid_object.htm`
