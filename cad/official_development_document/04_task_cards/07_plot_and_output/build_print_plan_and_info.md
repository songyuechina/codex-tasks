# 任务卡：构建打印计划和打印信息

## Exact Entry
- task_id: `CAD2021-TASK-016`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Layout`
- `Handle`
- `ObjectName`
- `GetAttributes`
- `Plot`
- owners:
- `Layout`
- `BlockReference`
- `Plot`
- implementation_entries:
- `collect_print_jobs` -> `cad/scripts/drawing_basic_service/print/print_policy.py`
- `build_print_plan` -> `cad/scripts/drawing_basic_service/print/print_policy.py`
- `analyze_print_info_jobs` -> `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

## Natural Language Expansion
- aliases_en:
- `build print plan and info`
- `collect print jobs`
- `assemble plot execution plan`
- aliases_zh_support:
- `构建打印计划和打印信息`
- `收集打印作业`
- `组装打印计划`
- keywords_zh_support:
- `打印计划`
- `打印信息`
- `作业收集`

## Goal
把布局、打印框、角标块和输出参数组织成可执行的打印计划。

## Priority Path
1. 优先使用 `collect_print_jobs()` + `build_print_plan()`
2. 打印信息分析优先用 `analyze_print_info_jobs()`

## Related Core Symbols
- `Layout`
- `Handle`
- `ObjectName`
- `GetAttributes`
- `Plot`

## Workflow
1. 先收集布局与打印区域作业
2. 再分析角标块和属性字段
3. 按布局归并为打印计划
4. 交给打印执行层推进

## Project Notes
- 这一步是打印主链的一部分，不应退化为单个 API 查询。

## Common Failures
- 打印框识别失败
- 角标块匹配失败
- 句柄映射不稳定

## Verification
- 生成的计划中包含布局、句柄、输出路径和方向

## Project Paths
- `cad/scripts/drawing_basic_service/print/print_policy.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/system/content_analysis_dwg_file.py`
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `cad/scripts/CAD_basic.py`

## Pywin32 Rules
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Source Trace
- source_topic_ids:
- `acad_aag:GUID_10F797AA_5032_4298_A2A5_C69449275F0E`
- `acad_aag:topichead_9`
- `acadauto:ex_layoutshowplotsetup`
- `acadauto:ex_setlayoutstoplot`
- `acad_aag:GUID_10344852_4888_4237_8EB6_5EBE24D5C87C`
- `acadauto:ex_handle`
- `acadauto:idh_handle`
- `acad_aag:GUID_2FF2F1B5_FFAC_420A_A741_15D1FC1A571E`
- `acadauto:ex_handletoobject`
- `acadauto:idh_handletoobject`
- `acadauto:ex_objectname`
- `acadauto:idh_objectname`
- `acadauto:objectname_see_also`
- `acadauto:ex_getattributes`
- `acadauto:idh_getattributes`
- `acadauto:getattributes_see_also`
- `acad_aag:GUID_9091E614_25B8_452E_A67A_301939B52161`
- `acadauto:ex_defaultplotstyleforlayer`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `01_extracted_html/acad_aag/topichead_9.htm`
- `01_extracted_html/acadauto/ex_layoutshowplotsetup.htm`
- `01_extracted_html/acadauto/ex_setlayoutstoplot.htm`
- `01_extracted_html/acad_aag/GUID-10344852-4888-4237-8EB6-5EBE24D5C87C.htm`
- `01_extracted_html/acadauto/ex_handle.htm`
- `01_extracted_html/acadauto/idh_handle.htm`
- `01_extracted_html/acad_aag/GUID-2FF2F1B5-FFAC-420A-A741-15D1FC1A571E.htm`
- `01_extracted_html/acadauto/ex_handletoobject.htm`
- `01_extracted_html/acadauto/idh_handletoobject.htm`
- `01_extracted_html/acadauto/ex_objectname.htm`
- `01_extracted_html/acadauto/idh_objectname.htm`
- `01_extracted_html/acadauto/objectname_see_also.htm`
- `01_extracted_html/acadauto/ex_getattributes.htm`
- `01_extracted_html/acadauto/idh_getattributes.htm`
- `01_extracted_html/acadauto/getattributes_see_also.htm`
- `01_extracted_html/acad_aag/GUID-9091E614-25B8-452E-A67A-301939B52161.htm`
- `01_extracted_html/acadauto/ex_defaultplotstyleforlayer.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/农建房施工图【电气】-0930_t6_t3.dwg`
- reference_objects:
- `Layout`
- `AcDbPolyline`
- `AcDbBlockReference`
