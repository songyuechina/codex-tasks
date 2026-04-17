# Normal

## 基本信息
- kind: `property`
- owners: `Entity`
- pywin32: `entity.Normal`

## 作用
表示对象的三维法向量，是确定 OCS 和执行 OCS/WCS 换算的关键属性。

## 高频场景
- 作为 TranslateCoordinates 的 OCSNormal
- 判断对象平面方向
- 还原对象真实空间姿态

## 项目路径
- `cad/system/licad.py`
- `cad/system/content_analysis_dwg_file.py`
- `cad/scripts/CAD_basic.py`

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
- `acadauto:idh_normal`
- `acadauto:idh_translatecoordinates`
- `acadauto:ex_translatecoordinates`
- `acadauto:translatecoordinates_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_translatecoordinates.htm`
- `01_extracted_html/acadauto/idh_normal.htm`
- `01_extracted_html/acadauto/idh_translatecoordinates.htm`
- `01_extracted_html/acadauto/translatecoordinates_see_also.htm`
