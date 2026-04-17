# 任务卡：理解并转换坐标系

## Exact Entry
- task_id: `CAD2021-TASK-020`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `TranslateCoordinates`
- `ActiveUCS`
- `GetUCSMatrix`
- `Normal`
- `Elevation`
- `ElevationModelSpace`
- `ElevationPaperSpace`
- `UCS`
- `3d_point`
- `ocs_point`
- `normal_vector`
- `ucs_matrix`
- owners:
- `Document`
- `UCS`
- `Utility`
- implementation_entries:
- `get_entity_full_info` -> `cad/scripts/CAD_basic.py`
- `get_entity_geometry_info` -> `cad/scripts/CAD_basic.py`
- `get_dwg_graphics_summary` -> `cad/system/content_analysis_dwg_file.py`

## Natural Language Expansion
- aliases_en:
- `understand and convert coordinate systems`
- `convert coordinates between wcs ucs ocs`
- `translate coordinates and ucs`
- aliases_zh_support:
- `理解并转换坐标系`
- `坐标系转换`
- `WCS UCS OCS 转换`
- keywords_zh_support:
- `坐标系`
- `坐标转换`
- `UCS`
- `OCS`
- `WCS`

## Goal
在 `WCS / UCS / OCS / DCS` 之间稳定转换 3D 点和对象基准，为空间关系表达提供统一入口。

## Priority Path
1. 优先看 `TranslateCoordinates`、`ActiveUCS`、`GetUCSMatrix`、`Normal`、`Elevation*`
2. 项目内优先参考 `get_entity_full_info()` 与 `get_entity_geometry_info()` 的坐标读取逻辑
3. 涉及对象基准整体迁移时，再进入 `TransformBy`

## Related Core Symbols
- `TranslateCoordinates`
- `ActiveUCS`
- `GetUCSMatrix`
- `Normal`
- `Elevation`
- `ElevationModelSpace`
- `ElevationPaperSpace`
- `UCS`
- `3d_point`
- `ocs_point`
- `normal_vector`
- `ucs_matrix`

## Workflow
1. 先判断当前点或对象属于 `WCS / UCS / OCS / DCS` 中哪一种基准
2. 若是对象局部坐标，先读取 `Coordinates/Coordinate`，再补 `Elevation` 和 `Normal`
3. 用 `TranslateCoordinates` 把点转换到目标基准
4. 若任务需要整体变换对象，再取 `ActiveUCS/GetUCSMatrix` 进入矩阵链

## Project Notes
- 这张卡服务施工图中的空间关系表达，不是泛化的坐标系教程。

## Common Failures
- 把 OCS 点直接当 WCS 点使用
- 漏传 `OCSNormal`
- 模型空间和图纸空间高程混淆
- 当前 UCS 未保存导致 `ActiveUCS` 读取失败

## Verification
- 同一个点在目标坐标系下得到稳定结果
- 对象 `Coordinates + Elevation + Normal` 能还原出可解释的 3D 点

## Project Paths
- `cad/scripts/CAD_basic.py`
- `cad/system/content_analysis_dwg_file.py`
- `cad/system/licad.py`
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`

## Pywin32 Rules
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/pywin32_type_rules.md`

## Source Trace
- source_topic_ids:
- `acadauto:idh_translatecoordinates`
- `acad_aag:GUID_06B18EED_D4E3_4B81_ACB8_037E884CB93D`
- `acad_aag:GUID_6954AAF3_7107_4D93_A2CE_FE859F3F9902`
- `acadauto:idh_activeucs`
- `acadauto:idh_ucs_object`
- `acadauto:idh_getucsmatrix`
- `acadauto:idh_transformby`
- `acadauto:ex_transformby`
- `acadauto:transformby_see_also`
- `acadauto:idh_normal`
- `acadauto:ex_translatecoordinates`
- `acadauto:translatecoordinates_see_also`
- `acadauto:idh_elevation`
- `acadauto:idh_elevationmodelspace`
- `acadauto:ex_elevationmodelspace`
- `acadauto:idh_elevationpaperspace`
- `acadauto:ex_elevationpaperspace`
- `acadauto:ex_activeucs`
- `acadauto:ex_getucsmatrix`
- `acadauto:ex_addline`
- `acadauto:ex_insertblock`
- `acadauto:ex_setwindowtoplot`
- `acadauto:ex_addminsertblock`
- `acadauto:idh_addline`
- `acadauto:ex_elevation`
- `acadauto:getucsmatrix_see_also`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-06B18EED-D4E3-4B81-ACB8-037E884CB93D.htm`
- `01_extracted_html/acad_aag/GUID-6954AAF3-7107-4D93-A2CE-FE859F3F9902.htm`
- `01_extracted_html/acadauto/idh_translatecoordinates.htm`
- `01_extracted_html/acadauto/idh_activeucs.htm`
- `01_extracted_html/acadauto/idh_ucs_object.htm`
- `01_extracted_html/acadauto/idh_getucsmatrix.htm`
- `01_extracted_html/acadauto/ex_transformby.htm`
- `01_extracted_html/acadauto/idh_transformby.htm`
- `01_extracted_html/acadauto/transformby_see_also.htm`
- `01_extracted_html/acadauto/ex_translatecoordinates.htm`
- `01_extracted_html/acadauto/idh_normal.htm`
- `01_extracted_html/acadauto/translatecoordinates_see_also.htm`
- `01_extracted_html/acadauto/idh_elevation.htm`
- `01_extracted_html/acadauto/idh_elevationmodelspace.htm`
- `01_extracted_html/acadauto/ex_elevationmodelspace.htm`
- `01_extracted_html/acadauto/idh_elevationpaperspace.htm`
- `01_extracted_html/acadauto/ex_elevationpaperspace.htm`
- `01_extracted_html/acadauto/ex_activeucs.htm`
- `01_extracted_html/acadauto/ex_getucsmatrix.htm`
- `01_extracted_html/acadauto/ex_insertblock.htm`
- `01_extracted_html/acadauto/ex_setwindowtoplot.htm`
- `01_extracted_html/acadauto/ex_addminsertblock.htm`
- `01_extracted_html/acadauto/ex_addline.htm`
- `01_extracted_html/acadauto/idh_addline.htm`
- `01_extracted_html/acadauto/ex_elevation.htm`
- `01_extracted_html/acadauto/getucsmatrix_see_also.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `UCS`
- `3d_point`
- `AcDbPolyline`
