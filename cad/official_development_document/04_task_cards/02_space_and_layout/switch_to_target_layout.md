# 任务卡：切换到指定布局

## Exact Entry
- task_id: `CAD2021-TASK-005`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `ActiveLayout`
- `Layouts`
- `Layout`
- `SendCommand`
- owners:
- `Document`
- `Layouts`
- `Layout`
- implementation_entries:
- `switch_to_layout` -> `cad/system/CAD_core.py`
- `switch_to_layout` -> `cad/scripts/drawing_basic_service/print/print_area_analysis.py`
- `send_cmd_with_sync` -> `cad/system/CAD_coordination.py`

## Natural Language Expansion
- aliases_en:
- `switch to target layout`
- `activate layout`
- `change active layout`
- aliases_zh_support:
- `切换到指定布局`
- `切换布局`
- `激活布局`
- keywords_zh_support:
- `布局切换`
- `目标布局`
- `激活`

## Goal
稳定切换到目标布局，并为后续打印或图签扫描提供正确上下文。

## Priority Path
1. 优先使用 `CAD_core.switch_to_layout()`
2. 打印执行链内也可参考 `print_area_analysis.switch_to_layout()`
3. COM 直切不稳时才走 `SendCommand` 兜底

## Related Core Symbols
- `ActiveLayout`
- `Layouts`
- `Layout`
- `SendCommand`

## Workflow
1. 若已在目标布局则直接返回
2. 通过 `Layouts.Item(name)` 取得布局对象
3. 写入 `Document.ActiveLayout`
4. 必要时走命令回退
5. 切换后再次读取布局名确认

## Project Notes
- 这是打印和布局图签任务的高频核心步骤。

## Common Failures
- RPC Busy
- 布局不存在
- 切换后状态未同步

## Verification
- `C.doc.ActiveLayout.Name` 等于目标布局名

## Project Paths
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`
- `cad/system/CAD_coordination.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/system/licad.py`

## Pywin32 Rules
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Source Trace
- source_topic_ids:
- `acadauto:ex_activelayout`
- `acadauto:idh_activelayout`
- `acadauto:activelayout_see_also`
- `acad_aag:GUID_10F797AA_5032_4298_A2A5_C69449275F0E`
- `acad_aag:topichead_9`
- `acad_aag:GUID_10344852_4888_4237_8EB6_5EBE24D5C87C`
- `acadauto:ex_layoutshowplotsetup`
- `acadauto:ex_setlayoutstoplot`
- `acadauto:ex_sendcommand`
- `acadauto:idh_sendcommand`
- `acadauto:sendcommand_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_activelayout.htm`
- `01_extracted_html/acadauto/idh_activelayout.htm`
- `01_extracted_html/acadauto/activelayout_see_also.htm`
- `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `01_extracted_html/acad_aag/topichead_9.htm`
- `01_extracted_html/acad_aag/GUID-10344852-4888-4237-8EB6-5EBE24D5C87C.htm`
- `01_extracted_html/acadauto/ex_layoutshowplotsetup.htm`
- `01_extracted_html/acadauto/ex_setlayoutstoplot.htm`
- `01_extracted_html/acadauto/ex_sendcommand.htm`
- `01_extracted_html/acadauto/idh_sendcommand.htm`
- `01_extracted_html/acadauto/sendcommand_see_also.htm`

## Stability
- stability_level: `high`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `Document`
- `Layout`
