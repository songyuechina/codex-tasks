# 任务卡：构造选择集 / 选择对象

## Exact Entry
- task_id: `CAD2021-TASK-006`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `SelectionSets`
- `SelectionSet`
- `Select`
- `SendCommand`
- owners:
- `SelectionSets`
- `SelectionSet`
- implementation_entries:
- `ss_select` -> `cad/system/CAD_selection.py`
- `select_entities_in_window` -> `cad/system/CAD_selection.py`
- `send_cmd_with_sync` -> `cad/system/CAD_coordination.py`

## Natural Language Expansion
- aliases_en:
- `build selection set`
- `select objects by window`
- `cad selection workflow`
- aliases_zh_support:
- `构造选择集`
- `窗口选择对象`
- `选择对象`
- keywords_zh_support:
- `选择集`
- `窗口选`
- `对象选择`

## Goal
在模型空间或布局空间里稳定构造选择集，用于后续对象扫描和统计。

## Priority Path
1. 优先复用 `CAD_selection.ss_select()`
2. 需要窗口选时优先复用 `select_entities_in_window()` 一类稳定函数

## Related Core Symbols
- `SelectionSets`
- `SelectionSet`
- `Select`
- `SendCommand`

## Workflow
1. 清理旧同名选择集
2. 新建 `SelectionSet`
3. 用窗口/交叉/过滤方式填充选择集
4. 把结果转换成后续逻辑可直接遍历的对象列表

## Project Notes
- 选择逻辑应优先走 `CAD_selection.py`，不要到处手写。

## Common Failures
- 同名选择集残留
- 窗口点坐标错误
- 命令态阻塞

## Verification
- 返回对象数量符合预期

## Project Paths
- `cad/system/CAD_selection.py`
- `cad/system/CAD_core.py`
- `cad/system/CAD_coordination.py`
- `cad/system/licad.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`

## Pywin32 Rules
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/sendcommand_rules.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Source Trace
- source_topic_ids:
- `acadauto:ex_selectionsets`
- `acadauto:idh_selectionsets_collection`
- `acadauto:idh_selectionsets`
- `acadauto:selectionsets_see_also`
- `acadauto:ex_activeselectionset`
- `acadauto:ex_pickfirstselectionset`
- `acadauto:idh_selectionset_object`
- `acadauto:idh_activeselectionset`
- `acadauto:ex_select`
- `acadauto:idh_select`
- `acadauto:ex_sendcommand`
- `acadauto:idh_sendcommand`
- `acadauto:sendcommand_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_selectionsets.htm`
- `01_extracted_html/acadauto/idh_selectionsets_collection.htm`
- `01_extracted_html/acadauto/idh_selectionsets.htm`
- `01_extracted_html/acadauto/selectionsets_see_also.htm`
- `01_extracted_html/acadauto/ex_activeselectionset.htm`
- `01_extracted_html/acadauto/ex_pickfirstselectionset.htm`
- `01_extracted_html/acadauto/idh_selectionset_object.htm`
- `01_extracted_html/acadauto/idh_activeselectionset.htm`
- `01_extracted_html/acadauto/ex_select.htm`
- `01_extracted_html/acadauto/idh_select.htm`
- `01_extracted_html/acadauto/ex_sendcommand.htm`
- `01_extracted_html/acadauto/idh_sendcommand.htm`
- `01_extracted_html/acadauto/sendcommand_see_also.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `SelectionSet`
- `AcDbPolyline`
- `AcDbBlockReference`
