# 任务卡：读取三维对象空间身份

## Exact Entry
- task_id: `CAD2021-TASK-025`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Coordinates`
- `Normal`
- `Elevation`
- `BoundingBox`
- `3dPolyline`
- `Region`
- `3DSolid`
- owners:
- `Entity`
- `3dPolyline`
- `Region`
- `3DSolid`
- implementation_entries:
- `get_entity_full_info` -> `cad/scripts/CAD_basic.py`
- `get_entity_geometry_info` -> `cad/scripts/CAD_basic.py`
- `get_dwg_graphics_summary` -> `cad/system/content_analysis_dwg_file.py`

## Natural Language Expansion
- aliases_en:
- `read 3d object spatial identity`
- `inspect 3d object coordinates normal elevation`
- `read spatial identity`
- aliases_zh_support:
- `读取三维对象空间身份`
- `读取对象空间身份`
- `坐标法向高程读取`
- keywords_zh_support:
- `空间身份`
- `Coordinates`
- `Normal`
- `Elevation`
- `包围盒`

## Goal
读取对象的坐标、高程、法向量、包围盒和类型身份，为空间关系分析和二维表达提供稳定输入。

## Priority Path
1. 优先看 `Coordinates`、`Normal`、`Elevation`、`BoundingBox`
2. 若对象来自局部坐标，先回到坐标系转换卡，不要直接解释原值
3. 需要做批量对象快照时，优先参考现有内容分析路径

## Related Core Symbols
- `Coordinates`
- `Normal`
- `Elevation`
- `BoundingBox`
- `3dPolyline`
- `Region`
- `3DSolid`

## Workflow
1. 先识别对象类型和所有者空间
2. 读取坐标序列、高程、法向量和包围盒
3. 必要时把局部坐标还原到 WCS
4. 把结果整理成可供后续剖切、打印或施工图表达使用的空间身份结构

## Project Notes
- 本卡服务的是对象空间身份识别，而不是单纯的属性列举。

## Common Failures
- 把 OCS 坐标直接当全局坐标
- 只看包围盒不看法向
- 对象类型识别正确但空间基准解释错误

## Verification
- 能得到稳定的对象类型、坐标、法向和包围盒结果
- 不同对象在同一基准下可比较空间关系

## Project Paths
- `cad/scripts/CAD_basic.py`
- `cad/system/content_analysis_dwg_file.py`
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `cad/system/licad.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/Scheme_drawing/draw_building_outline.py`

## Pywin32 Rules
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/pywin32_type_rules.md`
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/3d_transform_rules.md`

## Source Trace
- source_topic_ids:
- `acad_aag:GUID_06B18EED_D4E3_4B81_ACB8_037E884CB93D`
- `acad_aag:GUID_6954AAF3_7107_4D93_A2CE_FE859F3F9902`
- `acadauto:ex_coordinates`
- `acadauto:idh_coordinates`
- `acadauto:ex_translatecoordinates`
- `acadauto:idh_normal`
- `acadauto:idh_translatecoordinates`
- `acadauto:translatecoordinates_see_also`
- `acadauto:idh_elevation`
- `acadauto:ex_getboundingbox`
- `acadauto:idh_getboundingbox`
- `acadauto:getboundingbox_see_also`
- `acadauto:idh_3dpoly_object`
- `acadauto:idh_add3dpoly`
- `acadauto:ex_add3dpoly`
- `acadauto:add3dpoly_see_also`
- `acadauto:idh_region_object`
- `acadauto:idh_addregion`
- `acad_aag:GUID_4699B54A_2628_49FE_B093_0062FBEC37EA`
- `acad_aag:GUID_9EB18E5E_9C16_4FB9_B334_D61ED00DCB80`
- `acadauto:ex_addregion`
- `acadauto:addregion_see_also`
- `acadauto:idh_3dsolid_object`
- `acadauto:idh_addextrudedsolid`
- `acadauto:idh_addextrudedsolidalongpath`
- `acadauto:idh_addrevolvedsolid`
- `acadauto:idh_sectionsolid`
- `acadauto:ex_addextrudedsolidalongpath`
- `acadauto:ex_addextrudedsolid`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-06B18EED-D4E3-4B81-ACB8-037E884CB93D.htm`
- `01_extracted_html/acad_aag/GUID-6954AAF3-7107-4D93-A2CE-FE859F3F9902.htm`
- `01_extracted_html/acadauto/ex_coordinates.htm`
- `01_extracted_html/acadauto/idh_coordinates.htm`
- `01_extracted_html/acadauto/ex_translatecoordinates.htm`
- `01_extracted_html/acadauto/idh_normal.htm`
- `01_extracted_html/acadauto/idh_translatecoordinates.htm`
- `01_extracted_html/acadauto/translatecoordinates_see_also.htm`
- `01_extracted_html/acadauto/idh_elevation.htm`
- `01_extracted_html/acadauto/ex_getboundingbox.htm`
- `01_extracted_html/acadauto/idh_getboundingbox.htm`
- `01_extracted_html/acadauto/getboundingbox_see_also.htm`
- `01_extracted_html/acadauto/idh_3dpoly_object.htm`
- `01_extracted_html/acadauto/ex_add3dpoly.htm`
- `01_extracted_html/acadauto/idh_add3dpoly.htm`
- `01_extracted_html/acadauto/add3dpoly_see_also.htm`
- `01_extracted_html/acad_aag/GUID-9EB18E5E-9C16-4FB9-B334-D61ED00DCB80.htm`
- `01_extracted_html/acadauto/ex_addregion.htm`
- `01_extracted_html/acadauto/idh_addregion.htm`
- `01_extracted_html/acadauto/idh_region_object.htm`
- `01_extracted_html/acadauto/addregion_see_also.htm`
- `01_extracted_html/acad_aag/GUID-4699B54A-2628-49FE-B093-0062FBEC37EA.htm`
- `01_extracted_html/acadauto/ex_addextrudedsolidalongpath.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolidalongpath.htm`
- `01_extracted_html/acadauto/idh_3dsolid_object.htm`
- `01_extracted_html/acadauto/ex_addextrudedsolid.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolid.htm`
- `01_extracted_html/acadauto/idh_addrevolvedsolid.htm`
- `01_extracted_html/acadauto/idh_sectionsolid.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/农建房施工图【电气】-0930_t6_t3.dwg`
- reference_objects:
- `3dPolyline`
- `Region`
- `3DSolid`
- `AcDbEntity`
