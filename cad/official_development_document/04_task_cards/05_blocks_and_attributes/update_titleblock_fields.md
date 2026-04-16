# 任务卡：更新图签属性字段

## Exact Entry
- task_id: `CAD2021-TASK-012`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `BlockReference`
- `AttributeReference`
- `GetAttributes`
- `HasAttributes`
- `AddMText`
- owners:
- `BlockReference`
- `AttributeReference`
- implementation_entries:
- `process_drawing_names_and_fill_titleblocks` -> `cad/scripts/CAD_basic.py`
- `update_catalog_titleblocks_from_excel` -> `cad/scripts/CAD_basic.py`
- `fill_block_attributes_with_tag_name` -> `cad/scripts/CAD_basic.py`

## Natural Language Expansion
- aliases_en:
- `update titleblock fields`
- `fill title block attributes`
- `write drawing info to title block`
- aliases_zh_support:
- `更新图签属性字段`
- `回写图签字段`
- `填写图签属性`
- keywords_zh_support:
- `图签`
- `回写`
- `属性字段`
- `图名图号`

## Goal
把图名、图号、项目名或目录信息回写到图签属性中。

## Priority Path
1. 图名回写优先参考 `process_drawing_names_and_fill_titleblocks()`
2. 目录图签更新优先参考 `update_catalog_titleblocks_from_excel()`
3. 调试阶段可参考 `fill_block_attributes_with_tag_name()`

## Related Core Symbols
- `BlockReference`
- `AttributeReference`
- `GetAttributes`
- `HasAttributes`
- `AddMText`

## Workflow
1. 先定位目标图签块
2. 读取并识别目标属性标签
3. 按业务规则写入文本
4. 必要时同步目录或 Excel 数据源

## Project Notes
- 这类任务主逻辑优先参考项目现有业务函数，而不是从 CHM 生写。

## Common Failures
- 图签模板版本不一致
- 标签名不统一
- 属性格式被覆盖

## Verification
- 回写后再次读取属性值一致

## Project Paths
- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

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
- `acadauto:idh_dynamicblockreferenceproperty_object`
- `acadauto:idh_attributeref_object`
- `acadauto:ex_getattributes`
- `acadauto:idh_getattributes`
- `acadauto:getattributes_see_also`
- `acadauto:ex_hasattributes`
- `acadauto:idh_hasattributes`
- `acadauto:hasattributes_see_also`
- `acadauto:ex_addmtext`
- `acadauto:idh_addmtext`
- `acadauto:addmtext_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/idh_dynamicblockreferenceproperty_object.htm`
- `01_extracted_html/acadauto/idh_attributeref_object.htm`
- `01_extracted_html/acadauto/ex_getattributes.htm`
- `01_extracted_html/acadauto/idh_getattributes.htm`
- `01_extracted_html/acadauto/getattributes_see_also.htm`
- `01_extracted_html/acadauto/ex_hasattributes.htm`
- `01_extracted_html/acadauto/idh_hasattributes.htm`
- `01_extracted_html/acadauto/hasattributes_see_also.htm`
- `01_extracted_html/acadauto/ex_addmtext.htm`
- `01_extracted_html/acadauto/idh_addmtext.htm`
- `01_extracted_html/acadauto/addmtext_see_also.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `AcDbBlockReference`
- `AcDbAttribute`
