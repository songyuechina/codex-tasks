# Region

## 基本信息
- kind: `object`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `region_list = model_space.AddRegion(object_list)`

## 作用
表示有界平面区域，是从轮廓进入面积、剖切、实体和二维表达中间层的关键对象。

## 高频场景
- 由闭合轮廓生成区域
- 作为挤出或旋转实体的 profile
- 作为剖切结果的二维中间表达

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
- `acadauto:idh_region_object`
- `acadauto:idh_addregion`
- `acad_aag:GUID_4699B54A_2628_49FE_B093_0062FBEC37EA`
- `acad_aag:GUID_9EB18E5E_9C16_4FB9_B334_D61ED00DCB80`
- `acadauto:ex_addregion`
- `acadauto:addregion_see_also`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-9EB18E5E-9C16-4FB9-B334-D61ED00DCB80.htm`
- `01_extracted_html/acadauto/ex_addregion.htm`
- `01_extracted_html/acadauto/idh_addregion.htm`
- `01_extracted_html/acadauto/idh_region_object.htm`
- `01_extracted_html/acadauto/addregion_see_also.htm`
- `01_extracted_html/acad_aag/GUID-4699B54A-2628-49FE-B093-0062FBEC37EA.htm`
