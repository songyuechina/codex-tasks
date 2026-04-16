# 任务卡：插入公司通用图签

## Exact Entry
- task_id: `CAD2021-TASK-018`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `InsertBlock`
- `BlockReference`
- `GetAttributes`
- owners:
- `BlockReference`
- `Block`
- implementation_entries:
- `insert_company_label_common_block` -> `cad/scripts/CAD_basic.py`
- `insert_block_into_autocad` -> `cad/scripts/CAD_basic.py`

## Natural Language Expansion
- aliases_en:
- `insert company title block`
- `insert company label block`
- `place standard title block`
- aliases_zh_support:
- `插入公司通用图签`
- `插入公司图签块`
- `放置标准图签`
- keywords_zh_support:
- `公司图签`
- `插入图签`
- `标准图签`

## Goal
向当前图纸插入公司通用图签，并获取后续属性处理所需的信息。

## Priority Path
1. 优先参考 `insert_company_label_common_block()`
2. 底层插入依然回到 `InsertBlock` / `insert_file_exploded()`

## Related Core Symbols
- `InsertBlock`
- `BlockReference`
- `GetAttributes`

## Workflow
1. 确认图签模板路径
2. 在目标空间插入图签块
3. 按需要炸开或保留块参照
4. 收集后续属性填充需要的对象和信息

## Project Notes
- 图签服务是当前目标范围内的重要业务主题。

## Common Failures
- 模板路径失效
- 插入后比例不对
- 炸开后对象识别失败

## Verification
- 图签块或图签实体已在目标位置生成

## Project Paths
- `cad/scripts/CAD_basic.py`
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

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
- `acadauto:idh_dynamicblockreferenceproperty_object`
- `acadauto:ex_getattributes`
- `acadauto:idh_getattributes`
- `acadauto:getattributes_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_insertblock.htm`
- `01_extracted_html/acadauto/ex_addminsertblock.htm`
- `01_extracted_html/acadauto/idh_insertblock.htm`
- `01_extracted_html/acadauto/idh_addminsertblock.htm`
- `01_extracted_html/acadauto/idh_minsertblock_object.htm`
- `01_extracted_html/acadauto/idh_dynamicblockreferenceproperty_object.htm`
- `01_extracted_html/acadauto/ex_getattributes.htm`
- `01_extracted_html/acadauto/idh_getattributes.htm`
- `01_extracted_html/acadauto/getattributes_see_also.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `AcDbBlockReference`
- `AcDbAttribute`
