# object_return_type

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `result = com_method(...); 用对象属性/方法继续处理`

## 作用
统一说明哪些方法返回 COM 对象、集合或对象引用，避免把返回值当成纯数据结构处理。

## 高频场景
- InsertBlock 返回 BlockReference
- GetAttributes 返回属性集合
- SelectionSets.Add 返回 SelectionSet

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_selection.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `insert_block_or_dwg`
- `read_block_attributes`
- `build_selection_set`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:ex_insertblock`
- `acadauto:ex_getattributes`
- `acadauto:ex_selectionsets`
- `acadauto:ex_addminsertblock`
- `acadauto:idh_getattributes`
- source_html_paths:
- `01_extracted_html/acadauto/ex_getattributes.htm`
- `01_extracted_html/acadauto/ex_insertblock.htm`
- `01_extracted_html/acadauto/ex_selectionsets.htm`
- `01_extracted_html/acadauto/ex_addminsertblock.htm`
- `01_extracted_html/acadauto/idh_getattributes.htm`
