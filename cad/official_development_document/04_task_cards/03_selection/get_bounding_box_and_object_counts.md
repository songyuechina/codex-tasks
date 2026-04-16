# 任务卡：获取边界框和对象统计

## Exact Entry
- task_id: `CAD2021-TASK-008`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `BoundingBox`
- `Coordinates`
- `ObjectName`
- `Handle`
- owners:
- `Entity`
- `SelectionSet`
- `BlockReference`
- implementation_entries:
- `collect_area_content_metrics` -> `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `get_dwg_graphics_summary` -> `cad/system/content_analysis_dwg_file.py`

## Natural Language Expansion
- aliases_en:
- `get bounding box and object counts`
- `collect bbox metrics`
- `count objects by type`
- aliases_zh_support:
- `获取边界框和对象统计`
- `边界框统计`
- `对象计数`
- keywords_zh_support:
- `边界框`
- `统计`
- `计数`
- `打印框`

## Goal
为打印框识别、图签匹配和施工图统计准备基础几何与计数信息。

## Priority Path
1. 对象统计优先参考 `content_analysis_dwg_file.py`
2. 打印相关边界框匹配优先参考 `print_info_analysis.py`

## Related Core Symbols
- `BoundingBox`
- `Coordinates`
- `ObjectName`
- `Handle`

## Workflow
1. 获取目标对象集合
2. 读取边界框或坐标数组
3. 按对象类型做计数
4. 必要时采集句柄建立映射

## Project Notes
- 打印框、多段线、角标块常依赖这一层。

## Common Failures
- 边界框返回不稳定
- 对象类型统计口径不一致

## Verification
- 统计结果能回溯到具体对象或句柄

## Project Paths
- `cad/system/content_analysis_dwg_file.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_policy.py`

## Pywin32 Rules
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/pywin32_type_rules.md`

## Source Trace
- source_topic_ids:
- `acadauto:ex_getboundingbox`
- `acadauto:idh_getboundingbox`
- `acadauto:getboundingbox_see_also`
- `acad_aag:GUID_06B18EED_D4E3_4B81_ACB8_037E884CB93D`
- `acad_aag:GUID_6954AAF3_7107_4D93_A2CE_FE859F3F9902`
- `acadauto:ex_coordinates`
- `acadauto:idh_coordinates`
- `acadauto:ex_translatecoordinates`
- `acadauto:ex_objectname`
- `acadauto:idh_objectname`
- `acadauto:objectname_see_also`
- `acadauto:ex_handle`
- `acadauto:idh_handle`
- `acad_aag:GUID_2FF2F1B5_FFAC_420A_A741_15D1FC1A571E`
- `acadauto:ex_handletoobject`
- `acadauto:idh_handletoobject`
- source_html_paths:
- `01_extracted_html/acadauto/ex_getboundingbox.htm`
- `01_extracted_html/acadauto/idh_getboundingbox.htm`
- `01_extracted_html/acadauto/getboundingbox_see_also.htm`
- `01_extracted_html/acad_aag/GUID-06B18EED-D4E3-4B81-ACB8-037E884CB93D.htm`
- `01_extracted_html/acad_aag/GUID-6954AAF3-7107-4D93-A2CE-FE859F3F9902.htm`
- `01_extracted_html/acadauto/ex_coordinates.htm`
- `01_extracted_html/acadauto/idh_coordinates.htm`
- `01_extracted_html/acadauto/ex_translatecoordinates.htm`
- `01_extracted_html/acadauto/ex_objectname.htm`
- `01_extracted_html/acadauto/idh_objectname.htm`
- `01_extracted_html/acadauto/objectname_see_also.htm`
- `01_extracted_html/acadauto/ex_handle.htm`
- `01_extracted_html/acadauto/idh_handle.htm`
- `01_extracted_html/acad_aag/GUID-2FF2F1B5-FFAC-420A-A741-15D1FC1A571E.htm`
- `01_extracted_html/acadauto/ex_handletoobject.htm`
- `01_extracted_html/acadauto/idh_handletoobject.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/农建房施工图【电气】-0930_t6_t3.dwg`
- reference_objects:
- `AcDbPolyline`
- `AcDbBlockReference`
- `AcDbText`
- `AcDbMText`
