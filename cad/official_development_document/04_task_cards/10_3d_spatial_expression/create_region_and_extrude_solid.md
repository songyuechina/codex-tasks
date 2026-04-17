# 任务卡：创建 Region 并挤出 Solid

## Exact Entry
- task_id: `CAD2021-TASK-022`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `AddRegion`
- `Region`
- `AddExtrudedSolid`
- `AddExtrudedSolidAlongPath`
- `AddRevolvedSolid`
- `3DSolid`
- owners:
- `ModelSpace`
- `Region`
- `3DSolid`
- implementation_entries:
- `insert_region_v2` -> `cad/system/CAD_core.py`
- `create_block_from_region_cad` -> `cad/scripts/CAD_basic.py`
- `get_entity_geometry_info` -> `cad/scripts/CAD_basic.py`

## Natural Language Expansion
- aliases_en:
- `create region and extrude solid`
- `convert profile to region and solid`
- `extrude region to solid`
- aliases_zh_support:
- `创建 Region 并挤出 Solid`
- `轮廓转区域再转实体`
- `挤出实体`
- keywords_zh_support:
- `Region`
- `3DSolid`
- `挤出`
- `轮廓转实体`

## Goal
把闭合轮廓转为 Region，并进一步生成基础 Solid，服务构件体量与剖切表达。

## Priority Path
1. 优先看 `AddRegion`、`Region`、`AddExtrudedSolid`、`AddExtrudedSolidAlongPath`、`AddRevolvedSolid`、`3DSolid`
2. 轮廓不闭合或不共面时，先在输入层修正，不要直接强推实体生成
3. 需要沿路径生成实体时，再引入路径对象

## Related Core Symbols
- `AddRegion`
- `Region`
- `AddExtrudedSolid`
- `AddExtrudedSolidAlongPath`
- `AddRevolvedSolid`
- `3DSolid`

## Workflow
1. 先确认轮廓对象是闭合且共面的
2. 调用 `AddRegion` 获取区域对象
3. 按任务需要选择普通挤出、沿路径挤出或旋转成体
4. 将生成的 `3DSolid` 交给空间对位或剖切任务继续推进

## Project Notes
- 本卡服务施工图中的空间体量与剖切依据，不是为了扩展复杂 3D 造型。

## Common Failures
- 轮廓不闭合
- 轮廓不共面
- 挤出高度或锥角导致自相交
- 路径与轮廓平面关系不正确

## Verification
- 能拿到 `Region` 或 `3DSolid` 返回对象
- 生成结果可被包围盒和对象类型识别

## Project Paths
- `cad/system/CAD_core.py`
- `cad/scripts/CAD_basic.py`
- `cad/system/licad.py`
- `cad/system/content_analysis_dwg_file.py`

## Pywin32 Rules
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/3d_transform_rules.md`

## Source Trace
- source_topic_ids:
- `acadauto:idh_addregion`
- `acadauto:idh_region_object`
- `acad_aag:GUID_4699B54A_2628_49FE_B093_0062FBEC37EA`
- `acad_aag:GUID_9EB18E5E_9C16_4FB9_B334_D61ED00DCB80`
- `acadauto:ex_addregion`
- `acadauto:addregion_see_also`
- `acadauto:idh_addextrudedsolid`
- `acadauto:idh_3dsolid_object`
- `acadauto:idh_addextrudedsolidalongpath`
- `acadauto:idh_addrevolvedsolid`
- `acadauto:idh_sectionsolid`
- `acadauto:ex_addextrudedsolidalongpath`
- `acadauto:ex_addextrudedsolid`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-4699B54A-2628-49FE-B093-0062FBEC37EA.htm`
- `01_extracted_html/acadauto/idh_addregion.htm`
- `01_extracted_html/acadauto/idh_region_object.htm`
- `01_extracted_html/acad_aag/GUID-9EB18E5E-9C16-4FB9-B334-D61ED00DCB80.htm`
- `01_extracted_html/acadauto/ex_addregion.htm`
- `01_extracted_html/acadauto/addregion_see_also.htm`
- `01_extracted_html/acadauto/idh_3dsolid_object.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolid.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolidalongpath.htm`
- `01_extracted_html/acadauto/idh_addrevolvedsolid.htm`
- `01_extracted_html/acadauto/ex_addextrudedsolidalongpath.htm`
- `01_extracted_html/acadauto/ex_addextrudedsolid.htm`
- `01_extracted_html/acadauto/idh_sectionsolid.htm`

## Stability
- stability_level: `high`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `Region`
- `3DSolid`
