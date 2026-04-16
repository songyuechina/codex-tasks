# 任务卡：判断模型空间 / 图纸空间 / 当前布局

## Exact Entry
- task_id: `CAD2021-TASK-003`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Document`
- `ModelSpace`
- `PaperSpace`
- `ActiveLayout`
- `GetVariable`
- owners:
- `Document`
- `Layout`
- implementation_entries:
- `get_layout_names` -> `cad/system/CAD_core.py`
- `switch_to_layout` -> `cad/system/CAD_core.py`
- `current_space_only` -> `cad/system/CAD_selection.py`

## Natural Language Expansion
- aliases_en:
- `determine space and layout`
- `detect modelspace paperspace`
- `check current layout context`
- aliases_zh_support:
- `判断模型空间图纸空间当前布局`
- `检查当前布局上下文`
- keywords_zh_support:
- `模型空间`
- `图纸空间`
- `布局`
- `上下文`

## Goal
在后续打印、选区、图签扫描前确认当前空间上下文。

## Priority Path
1. 先看 `Document.ActiveLayout`、`ModelSpace`、`PaperSpace`
2. 需要空间过滤时优先复用 `CAD_selection.py` 的现有能力

## Related Core Symbols
- `Document`
- `ModelSpace`
- `PaperSpace`
- `ActiveLayout`
- `GetVariable`

## Workflow
1. 读取当前 `ActiveLayout.Name`
2. 判断当前任务是模型空间、布局块还是图纸空间扫描
3. 必要时配合系统变量判断上下文
4. 把空间判断结果写入后续任务的输入

## Project Notes
- 打印、图签、目录任务经常因为空间误判而整体跑偏。

## Common Failures
- ActiveLayout 已切但上下文未同步
- 把布局块对象误当模型空间对象

## Verification
- 当前布局名与预期一致
- 对象容器与任务类型一致

## Project Paths
- `cad/system/CAD_selection.py`
- `cad/system/CAD_core.py`
- `cad/system/licad.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`

## Pywin32 Rules
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/collection_rules.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Source Trace
- source_topic_ids:
- `acad_aag:GUID_83045B84_E056_4AE6_AEF5_D48AFB4F9F78`
- `acad_aag:GUID_45654BC7_F6B5_48E9_82FD_CED83FB956C4`
- `acad_aag:GUID_4F4377B1_07C8_4DDA_94D9_23DBF493C871`
- `acad_aag:GUID_675CFE8A_2256_4808_A1C8_186E68A69496`
- `acad_aag:GUID_679FBC1A_DE7B_44BA_9F8B_CD6FF1660D67`
- `acadauto:ex_modelspace`
- `acadauto:ex_elevationmodelspace`
- `acadauto:idh_modelspace_collection`
- `acadauto:idh_modelspace`
- `acadauto:idh_elevationmodelspace`
- `acadauto:ex_paperspace`
- `acadauto:ex_elevationpaperspace`
- `acadauto:idh_paperspace_collection`
- `acadauto:idh_paperspace`
- `acadauto:idh_elevationpaperspace`
- `acadauto:ex_activelayout`
- `acadauto:idh_activelayout`
- `acadauto:activelayout_see_also`
- `acadauto:ex_getvariable`
- `acadauto:idh_getvariable`
- `acadauto:getvariable_see_also`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-83045B84-E056-4AE6-AEF5-D48AFB4F9F78.htm`
- `01_extracted_html/acad_aag/GUID-45654BC7-F6B5-48E9-82FD-CED83FB956C4.htm`
- `01_extracted_html/acad_aag/GUID-4F4377B1-07C8-4DDA-94D9-23DBF493C871.htm`
- `01_extracted_html/acad_aag/GUID-675CFE8A-2256-4808-A1C8-186E68A69496.htm`
- `01_extracted_html/acad_aag/GUID-679FBC1A-DE7B-44BA-9F8B-CD6FF1660D67.htm`
- `01_extracted_html/acadauto/ex_modelspace.htm`
- `01_extracted_html/acadauto/ex_elevationmodelspace.htm`
- `01_extracted_html/acadauto/idh_modelspace_collection.htm`
- `01_extracted_html/acadauto/idh_modelspace.htm`
- `01_extracted_html/acadauto/idh_elevationmodelspace.htm`
- `01_extracted_html/acadauto/ex_paperspace.htm`
- `01_extracted_html/acadauto/ex_elevationpaperspace.htm`
- `01_extracted_html/acadauto/idh_paperspace_collection.htm`
- `01_extracted_html/acadauto/idh_paperspace.htm`
- `01_extracted_html/acadauto/idh_elevationpaperspace.htm`
- `01_extracted_html/acadauto/ex_activelayout.htm`
- `01_extracted_html/acadauto/idh_activelayout.htm`
- `01_extracted_html/acadauto/activelayout_see_also.htm`
- `01_extracted_html/acadauto/ex_getvariable.htm`
- `01_extracted_html/acadauto/idh_getvariable.htm`
- `01_extracted_html/acadauto/getvariable_see_also.htm`

## Stability
- stability_level: `high`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- reference_objects:
- `Document`
- `Layout`
- `ModelSpace`
- `PaperSpace`
