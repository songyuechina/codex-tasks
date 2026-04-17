# AddRegion

## 基本信息
- kind: `method`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `model_space.AddRegion(object_list)`

## 作用
把闭合共面轮廓转换成 Region，是从轮廓进入区域、实体和剖切逻辑的关键桥。

## 高频场景
- 闭合轮廓转区域
- 为挤出或旋转实体准备 profile
- 为二维剖切表达准备中间区域对象

## 项目路径
- `cad/system/licad.py`
- `cad/system/content_analysis_dwg_file.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `create_region_and_extrude_solid`
- `section_3d_geometry_for_2d_expression`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_addregion`
- `acadauto:idh_region_object`
- `acad_aag:GUID_4699B54A_2628_49FE_B093_0062FBEC37EA`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-4699B54A-2628-49FE-B093-0062FBEC37EA.htm`
- `01_extracted_html/acadauto/idh_addregion.htm`
- `01_extracted_html/acadauto/idh_region_object.htm`
