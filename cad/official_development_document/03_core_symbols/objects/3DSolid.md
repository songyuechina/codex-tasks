# 3DSolid

## 基本信息
- kind: `object`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `model_space.AddExtrudedSolid(...) / model_space.AddExtrudedSolidAlongPath(...) / model_space.AddRevolvedSolid(...)`

## 作用
表示三维实体对象，用于稳定表达构件体量、空间关系和剖切结果来源。

## 高频场景
- 由 Region 生成实体
- 沿路径或绕轴形成构件体量
- 通过 SectionSolid 导回二维剖切表达

## 项目路径
- `cad/system/licad.py`
- `cad/system/content_analysis_dwg_file.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `create_region_and_extrude_solid`
- `section_3d_geometry_for_2d_expression`
- `read_3d_object_spatial_identity`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_3dsolid_object`
- `acadauto:idh_addextrudedsolid`
- `acadauto:idh_addextrudedsolidalongpath`
- `acadauto:idh_addrevolvedsolid`
- `acadauto:idh_sectionsolid`
- `acadauto:ex_addextrudedsolidalongpath`
- `acadauto:ex_addextrudedsolid`
- source_html_paths:
- `01_extracted_html/acadauto/ex_addextrudedsolidalongpath.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolidalongpath.htm`
- `01_extracted_html/acadauto/idh_3dsolid_object.htm`
- `01_extracted_html/acadauto/ex_addextrudedsolid.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolid.htm`
- `01_extracted_html/acadauto/idh_addrevolvedsolid.htm`
- `01_extracted_html/acadauto/idh_sectionsolid.htm`
