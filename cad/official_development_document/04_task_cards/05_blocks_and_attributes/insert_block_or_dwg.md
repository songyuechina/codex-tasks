# 任务卡：插入块或插入 DWG

## Exact Entry
- task_id: `CAD2021-TASK-011`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `InsertBlock`
- `Block`
- `BlockReference`
- `ModelSpace`
- `PaperSpace`
- owners:
- `Block`
- `BlockReference`
- `ModelSpace`
- `PaperSpace`
- implementation_entries:
- `insert_block_into_autocad` -> `cad/scripts/CAD_basic.py`
- `insert_file_exploded` -> `cad/system/CAD_core.py`

## Natural Language Expansion
- aliases_en:
- `insert block or dwg`
- `insert title block template`
- `insert external drawing`
- aliases_zh_support:
- `插入块或插入DWG`
- `插入图签模板`
- `插入外部图纸`
- keywords_zh_support:
- `插块`
- `插入DWG`
- `炸开`

## Goal
在模型空间或布局空间中插入图签、目录模板或外部 DWG。

## Priority Path
1. 普通插块可参考 `CAD_basic.insert_block_into_autocad()`
2. 需要跨文件插入并炸开时优先参考 `CAD_core.insert_file_exploded()`

## Related Core Symbols
- `InsertBlock`
- `Block`
- `BlockReference`
- `ModelSpace`
- `PaperSpace`

## Workflow
1. 确认目标空间和插入点
2. 校验路径存在
3. 调用 `InsertBlock`
4. 若后续需编辑实体，可再 Explode

## Project Notes
- 图签和目录模板通常更接近块插入而非纯几何重建。

## Common Failures
- INSBASE 偏移
- 路径不存在
- 插到错误布局

## Verification
- 插入后能读取到新的 `BlockReference`

## Project Paths
- `cad/system/CAD_core.py`
- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/system/licad.py`
- `cad/system/CAD_selection.py`

## Pywin32 Rules
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/collection_rules.md`

## Source Trace
- source_topic_ids:
- `acadauto:ex_insertblock`
- `acadauto:ex_addminsertblock`
- `acadauto:idh_insertblock`
- `acadauto:idh_addminsertblock`
- `acadauto:idh_minsertblock_object`
- `acad_aag:GUID_10F797AA_5032_4298_A2A5_C69449275F0E`
- `acadauto:ex_blockattribute`
- `acad_aag:GUID_F9C39B22_6AF1_4501_9EE8_928C1B4AAA21`
- `acadauto:idh_dynamicblockreferenceproperty_object`
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
- source_html_paths:
- `01_extracted_html/acadauto/ex_insertblock.htm`
- `01_extracted_html/acadauto/ex_addminsertblock.htm`
- `01_extracted_html/acadauto/idh_insertblock.htm`
- `01_extracted_html/acadauto/idh_addminsertblock.htm`
- `01_extracted_html/acadauto/idh_minsertblock_object.htm`
- `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `01_extracted_html/acadauto/ex_blockattribute.htm`
- `01_extracted_html/acad_aag/GUID-F9C39B22-6AF1-4501-9EE8-928C1B4AAA21.htm`
- `01_extracted_html/acadauto/idh_dynamicblockreferenceproperty_object.htm`
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

## Stability
- stability_level: `high`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `Block`
- `AcDbBlockReference`
