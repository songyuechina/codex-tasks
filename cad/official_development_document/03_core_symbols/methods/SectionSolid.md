# SectionSolid

## 基本信息
- kind: `method`
- owners: `3DSolid`
- pywin32: `solid.SectionSolid(point1, point2, point3)`

## 作用
根据三点定义的平面剖切 3DSolid 并返回 Region，是把三维关系导回二维表达的核心方法。

## 高频场景
- 获取剖切区域
- 为二维剖面表达提供几何依据
- 从实体生成截面 Region

## 项目路径
- `cad/system/licad.py`
- `cad/system/content_analysis_dwg_file.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `section_3d_geometry_for_2d_expression`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_sectionsolid`
- `acadauto:idh_3dsolid_object`
- `acadauto:idh_region_object`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dsolid_object.htm`
- `01_extracted_html/acadauto/idh_sectionsolid.htm`
- `01_extracted_html/acadauto/idh_region_object.htm`
