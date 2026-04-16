# 任务卡：读取块属性

## Exact Entry
- task_id: `CAD2021-TASK-010`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `BlockReference`
- `HasAttributes`
- `GetAttributes`
- `AttributeReference`
- owners:
- `BlockReference`
- `AttributeReference`
- implementation_entries:
- `get_block_attributes_dict` -> `cad/scripts/CAD_basic.py`
- `_extract_attribute_fields` -> `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

## Natural Language Expansion
- aliases_en:
- `read block attributes`
- `extract title block fields`
- `get attribute values from block reference`
- aliases_zh_support:
- `读取块属性`
- `提取图签字段`
- `获取属性值`
- keywords_zh_support:
- `块属性`
- `图签`
- `属性字段`

## Goal
从图签、角标或目录模板块中提取属性字段和值。

## Priority Path
1. 优先先判 `HasAttributes`
2. 属性读取优先参考 `print_info_analysis._extract_attribute_fields()`
3. 通用块属性读取也可参考 `CAD_basic.get_block_attributes_dict()`

## Related Core Symbols
- `BlockReference`
- `HasAttributes`
- `GetAttributes`
- `AttributeReference`

## Workflow
1. 定位块参照对象
2. 判断是否有属性
3. 遍历 `GetAttributes()`
4. 读取 `TagString` / `TextString` 并做文本清洗

## Project Notes
- 图签字段常带格式控制前缀，需要清洗。

## Common Failures
- 块无属性
- 属性值为空
- MText 样式前缀干扰

## Verification
- 返回字段字典包含图号/图名/项目名等关键标签

## Project Paths
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
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
- `acadauto:idh_dynamicblockreferenceproperty_object`
- `acadauto:ex_hasattributes`
- `acadauto:idh_hasattributes`
- `acadauto:hasattributes_see_also`
- `acadauto:ex_getattributes`
- `acadauto:idh_getattributes`
- `acadauto:getattributes_see_also`
- `acadauto:idh_attributeref_object`
- source_html_paths:
- `01_extracted_html/acadauto/idh_dynamicblockreferenceproperty_object.htm`
- `01_extracted_html/acadauto/ex_hasattributes.htm`
- `01_extracted_html/acadauto/idh_hasattributes.htm`
- `01_extracted_html/acadauto/hasattributes_see_also.htm`
- `01_extracted_html/acadauto/ex_getattributes.htm`
- `01_extracted_html/acadauto/idh_getattributes.htm`
- `01_extracted_html/acadauto/getattributes_see_also.htm`
- `01_extracted_html/acadauto/idh_attributeref_object.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/农建房施工图【电气】-0930_t6_t3.dwg`
- reference_objects:
- `AcDbBlockReference`
- `AcDbAttribute`
- `AcDbMText`
