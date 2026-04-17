# normal_vector

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `(nx, ny, nz) as WCS unit vector`

## 作用
统一说明法向量是方向向量而不是点，并作为 OCS/WCS 换算的输入。

## 高频场景
- 作为 OCSNormal 传给 TranslateCoordinates
- 确定对象平面法向
- 描述剖切和平面方向

## 项目路径
- `cad/system/licad.py`
- `cad/system/content_analysis_dwg_file.py`

## 相关任务
- `understand_and_convert_coordinate_systems`
- `read_3d_object_spatial_identity`
- `section_3d_geometry_for_2d_expression`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:idh_normal`
- `acadauto:idh_translatecoordinates`
- `acadauto:ex_translatecoordinates`
- `acadauto:translatecoordinates_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_translatecoordinates.htm`
- `01_extracted_html/acadauto/idh_normal.htm`
- `01_extracted_html/acadauto/idh_translatecoordinates.htm`
- `01_extracted_html/acadauto/translatecoordinates_see_also.htm`
