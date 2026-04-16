# 任务卡：枚举所有布局

## Exact Entry
- task_id: `CAD2021-TASK-004`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Layouts`
- `Layout`
- `Document`
- owners:
- `Layouts`
- `Layout`
- `Document`
- implementation_entries:
- `get_layout_names` -> `cad/system/CAD_core.py`
- `get_layout_names` -> `cad/scripts/drawing_basic_service/print/print_area_analysis.py`

## Natural Language Expansion
- aliases_en:
- `enumerate layouts`
- `list layouts`
- `get layout names`
- aliases_zh_support:
- `枚举所有布局`
- `获取布局列表`
- keywords_zh_support:
- `布局`
- `枚举`
- `列表`

## Goal
获取当前文档布局列表，供打印、目录、图签任务做分发。

## Priority Path
1. 优先使用 `CAD_core.get_layout_names()`
2. 打印场景也可参考 `print_area_analysis.get_layout_names()`

## Related Core Symbols
- `Layouts`
- `Layout`
- `Document`

## Workflow
1. 读取 `C.doc.Layouts`
2. 遍历并收集 `layout.Name`
3. 按任务需要决定是否排除 `Model`

## Project Notes
- COM 遍历顺序未必等于标签页顺序。

## Common Failures
- 布局枚举时 Busy
- 布局名存在历史残留空白

## Verification
- 返回列表非空
- 目标布局名可被命中

## Project Paths
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/system/licad.py`

## Pywin32 Rules
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Source Trace
- source_topic_ids:
- `acad_aag:GUID_10F797AA_5032_4298_A2A5_C69449275F0E`
- `acad_aag:topichead_9`
- `acad_aag:GUID_10344852_4888_4237_8EB6_5EBE24D5C87C`
- `acadauto:ex_layoutshowplotsetup`
- `acadauto:ex_setlayoutstoplot`
- `acad_aag:GUID_83045B84_E056_4AE6_AEF5_D48AFB4F9F78`
- `acad_aag:GUID_45654BC7_F6B5_48E9_82FD_CED83FB956C4`
- `acad_aag:GUID_4F4377B1_07C8_4DDA_94D9_23DBF493C871`
- `acad_aag:GUID_675CFE8A_2256_4808_A1C8_186E68A69496`
- `acad_aag:GUID_679FBC1A_DE7B_44BA_9F8B_CD6FF1660D67`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `01_extracted_html/acad_aag/topichead_9.htm`
- `01_extracted_html/acad_aag/GUID-10344852-4888-4237-8EB6-5EBE24D5C87C.htm`
- `01_extracted_html/acadauto/ex_layoutshowplotsetup.htm`
- `01_extracted_html/acadauto/ex_setlayoutstoplot.htm`
- `01_extracted_html/acad_aag/GUID-83045B84-E056-4AE6-AEF5-D48AFB4F9F78.htm`
- `01_extracted_html/acad_aag/GUID-45654BC7-F6B5-48E9-82FD-CED83FB956C4.htm`
- `01_extracted_html/acad_aag/GUID-4F4377B1-07C8-4DDA-94D9-23DBF493C871.htm`
- `01_extracted_html/acad_aag/GUID-675CFE8A-2256-4808-A1C8-186E68A69496.htm`
- `01_extracted_html/acad_aag/GUID-679FBC1A-DE7B-44BA-9F8B-CD6FF1660D67.htm`

## Stability
- stability_level: `high`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- reference_objects:
- `Layouts`
- `Layout`
