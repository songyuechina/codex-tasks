# 任务卡：生成目录或更新目录图签

## Exact Entry
- task_id: `CAD2021-TASK-019`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `AddText`
- `AddMText`
- `BlockReference`
- `GetAttributes`
- `InsertBlock`
- owners:
- `BlockReference`
- `AttributeReference`
- `ModelSpace`
- implementation_entries:
- `write_catalog_from_excel_to_cad` -> `cad/scripts/CAD_basic.py`
- `update_catalog_titleblocks_from_excel` -> `cad/scripts/CAD_basic.py`

## Natural Language Expansion
- aliases_en:
- `generate or update catalog`
- `write drawing list from excel`
- `update catalog title blocks`
- aliases_zh_support:
- `生成目录或更新目录图签`
- `从Excel写目录`
- `更新目录图签`
- keywords_zh_support:
- `目录`
- `Excel`
- `目录图签`
- `目录页`

## Goal
围绕 Excel 与图签模板，完成目录写入、目录图签更新和目录页自动化。

## Priority Path
1. 目录写入优先参考 `write_catalog_from_excel_to_cad()`
2. 目录图签更新优先参考 `update_catalog_titleblocks_from_excel()`
3. 旧版分步逻辑可参考 `bianmulu_func1_h` 到 `bianmulu_func4_h`

## Related Core Symbols
- `AddText`
- `AddMText`
- `BlockReference`
- `GetAttributes`
- `InsertBlock`

## Workflow
1. 读取 Excel 数据
2. 解析目录模板或目录图签块
3. 写入目录文本或更新目录图签属性
4. 校验行数、比例和页码映射

## Project Notes
- 目录主题与当前业务目标直接相关，应保留高优先级入口。

## Common Failures
- 模板字段不一致
- 目录行数超界
- 比例字段计算错误

## Verification
- 目录页内容与 Excel 数据一致
- 目录图签字段回读正确

## Project Paths
- `cad/scripts/CAD_basic.py`
- `cad/scripts/Scheme_drawing/draw_building_outline.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/system/CAD_core.py`

## Pywin32 Rules
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/pywin32_type_rules.md`

## Source Trace
- source_topic_ids:
- `acadauto:ex_addtext`
- `acadauto:idh_addtext`
- `acadauto:addtext_see_also`
- `acadauto:ex_addmtext`
- `acadauto:idh_addmtext`
- `acadauto:addmtext_see_also`
- `acadauto:idh_dynamicblockreferenceproperty_object`
- `acadauto:ex_getattributes`
- `acadauto:idh_getattributes`
- `acadauto:getattributes_see_also`
- `acadauto:ex_insertblock`
- `acadauto:ex_addminsertblock`
- `acadauto:idh_insertblock`
- `acadauto:idh_addminsertblock`
- `acadauto:idh_minsertblock_object`
- source_html_paths:
- `01_extracted_html/acadauto/ex_addtext.htm`
- `01_extracted_html/acadauto/idh_addtext.htm`
- `01_extracted_html/acadauto/addtext_see_also.htm`
- `01_extracted_html/acadauto/ex_addmtext.htm`
- `01_extracted_html/acadauto/idh_addmtext.htm`
- `01_extracted_html/acadauto/addmtext_see_also.htm`
- `01_extracted_html/acadauto/idh_dynamicblockreferenceproperty_object.htm`
- `01_extracted_html/acadauto/ex_getattributes.htm`
- `01_extracted_html/acadauto/idh_getattributes.htm`
- `01_extracted_html/acadauto/getattributes_see_also.htm`
- `01_extracted_html/acadauto/ex_insertblock.htm`
- `01_extracted_html/acadauto/ex_addminsertblock.htm`
- `01_extracted_html/acadauto/idh_insertblock.htm`
- `01_extracted_html/acadauto/idh_addminsertblock.htm`
- `01_extracted_html/acadauto/idh_minsertblock_object.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `AcDbText`
- `AcDbMText`
- `AcDbBlockReference`
