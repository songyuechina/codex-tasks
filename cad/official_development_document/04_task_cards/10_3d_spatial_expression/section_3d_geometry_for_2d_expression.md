# 任务卡：对三维几何做剖切并服务二维表达

## Exact Entry
- task_id: `CAD2021-TASK-024`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `SectionSolid`
- `Region`
- `3DSolid`
- `section_plane_definition`
- `BoundingBox`
- owners:
- `3DSolid`
- `Region`
- `Document`
- implementation_entries:
- `get_dwg_graphics_summary` -> `cad/system/content_analysis_dwg_file.py`
- `collect_space_entity_snapshots` -> `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `get_boundingbox_from_objects` -> `cad/scripts/CAD_basic.py`

## Natural Language Expansion
- aliases_en:
- `section 3d geometry for 2d expression`
- `section solid for 2d drawing logic`
- `derive 2d expression from 3d section`
- aliases_zh_support:
- `对三维几何做剖切并服务二维表达`
- `三维剖切转二维表达`
- `SectionSolid`
- keywords_zh_support:
- `剖切`
- `SectionSolid`
- `二维表达`
- `剖面`

## Goal
通过 `SectionSolid` 或区域边界提取，把三维空间关系转成二维施工图可用的剖切与边界依据。

## Priority Path
1. 优先看 `SectionSolid`、`Region`、`section_plane_definition`
2. 若只需要粗边界，再评估是否先读 `BoundingBox`，不要把包围盒直接等同于剖面轮廓
3. 二维表达落图前，先确认剖切结果的坐标基准

## Related Core Symbols
- `SectionSolid`
- `Region`
- `3DSolid`
- `section_plane_definition`
- `BoundingBox`

## Workflow
1. 先确认三维实体和剖切平面的三点定义
2. 调用 `SectionSolid` 获取剖切 Region
3. 读取返回区域的边界、面积、质心或爆炸后的环路
4. 把结果组织成可供二维施工图表达使用的几何参考

## Project Notes
- 本卡是第四轮最直接体现“由三维关系支撑二维表达”的入口之一。

## Common Failures
- 剖切平面三点共线
- 只读包围盒导致表达过粗
- 剖切结果坐标基准未统一
- 把实体编辑结果直接当二维表达输出

## Verification
- 能得到有效 Region 或稳定边界
- 剖切结果可解释为二维剖面或轮廓参考

## Project Paths
- `cad/system/content_analysis_dwg_file.py`
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `cad/scripts/CAD_basic.py`
- `cad/system/licad.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

## Pywin32 Rules
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/pywin32_type_rules.md`

## Source Trace
- source_topic_ids:
- `acadauto:idh_sectionsolid`
- `acadauto:idh_3dsolid_object`
- `acadauto:idh_region_object`
- `acadauto:idh_addregion`
- `acad_aag:GUID_4699B54A_2628_49FE_B093_0062FBEC37EA`
- `acad_aag:GUID_9EB18E5E_9C16_4FB9_B334_D61ED00DCB80`
- `acadauto:ex_addregion`
- `acadauto:addregion_see_also`
- `acadauto:idh_addextrudedsolid`
- `acadauto:idh_addextrudedsolidalongpath`
- `acadauto:idh_addrevolvedsolid`
- `acadauto:ex_addextrudedsolidalongpath`
- `acadauto:ex_addextrudedsolid`
- `acadauto:ex_sectionsolid`
- `acadauto:sectionsolid_see_also`
- `acadauto:ex_getboundingbox`
- `acadauto:idh_getboundingbox`
- `acadauto:getboundingbox_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dsolid_object.htm`
- `01_extracted_html/acadauto/idh_sectionsolid.htm`
- `01_extracted_html/acadauto/idh_region_object.htm`
- `01_extracted_html/acad_aag/GUID-9EB18E5E-9C16-4FB9-B334-D61ED00DCB80.htm`
- `01_extracted_html/acadauto/ex_addregion.htm`
- `01_extracted_html/acadauto/idh_addregion.htm`
- `01_extracted_html/acadauto/addregion_see_also.htm`
- `01_extracted_html/acad_aag/GUID-4699B54A-2628-49FE-B093-0062FBEC37EA.htm`
- `01_extracted_html/acadauto/ex_addextrudedsolidalongpath.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolidalongpath.htm`
- `01_extracted_html/acadauto/ex_addextrudedsolid.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolid.htm`
- `01_extracted_html/acadauto/idh_addrevolvedsolid.htm`
- `01_extracted_html/acadauto/ex_sectionsolid.htm`
- `01_extracted_html/acadauto/sectionsolid_see_also.htm`
- `01_extracted_html/acadauto/ex_getboundingbox.htm`
- `01_extracted_html/acadauto/idh_getboundingbox.htm`
- `01_extracted_html/acadauto/getboundingbox_see_also.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/农建房施工图【电气】-0930_t6_t3.dwg`
- reference_objects:
- `3DSolid`
- `Region`
