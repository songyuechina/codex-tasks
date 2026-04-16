# 任务卡：SendCommand 命令回退

## Exact Entry
- task_id: `CAD2021-TASK-017`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `SendCommand`
- `GetVariable`
- `SetVariable`
- `Document`
- owners:
- `Document`
- implementation_entries:
- `send_cmd_with_sync` -> `cad/system/CAD_coordination.py`
- `SendCommand` -> `cad/system/licad.py`

## Natural Language Expansion
- aliases_en:
- `sendcommand fallback`
- `command line fallback`
- `synchronize sendcommand`
- aliases_zh_support:
- `SendCommand命令回退`
- `命令行回退`
- `同步命令发送`
- keywords_zh_support:
- `命令回退`
- `SendCommand`
- `同步等待`

## Goal
在 COM 直接调用不稳定时，安全地使用命令行回退完成布局切换、缩放、选择或打印补救。

## Priority Path
1. 优先用 `licad.SafeDocumentWrapper.SendCommand`
2. 需要同步等待时优先用 `CAD_coordination.send_cmd_with_sync()`

## Related Core Symbols
- `SendCommand`
- `GetVariable`
- `SetVariable`
- `Document`

## Workflow
1. 确认当前确实需要命令回退
2. 构造完整命令串并补换行
3. 发送命令并等待状态稳定
4. 回读关键状态确认命令生效

## Project Notes
- SendCommand 是保底，不是默认主路。

## Common Failures
- 命令串发到错误上下文
- 命令仍在执行就继续发下一条
- 系统变量状态不一致

## Verification
- 命令后关键状态读数符合预期

## Project Paths
- `cad/system/licad.py`
- `cad/system/CAD_coordination.py`
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/system/CAD_core.py`

## Pywin32 Rules
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/collection_rules.md`

## Source Trace
- source_topic_ids:
- `acadauto:ex_sendcommand`
- `acadauto:idh_sendcommand`
- `acadauto:sendcommand_see_also`
- `acadauto:ex_getvariable`
- `acadauto:idh_getvariable`
- `acadauto:getvariable_see_also`
- `acadauto:ex_setvariable`
- `acadauto:idh_setvariable`
- `acadauto:setvariable_see_also`
- `acad_aag:GUID_83045B84_E056_4AE6_AEF5_D48AFB4F9F78`
- `acad_aag:GUID_45654BC7_F6B5_48E9_82FD_CED83FB956C4`
- `acad_aag:GUID_4F4377B1_07C8_4DDA_94D9_23DBF493C871`
- `acad_aag:GUID_675CFE8A_2256_4808_A1C8_186E68A69496`
- `acad_aag:GUID_679FBC1A_DE7B_44BA_9F8B_CD6FF1660D67`
- source_html_paths:
- `01_extracted_html/acadauto/ex_sendcommand.htm`
- `01_extracted_html/acadauto/idh_sendcommand.htm`
- `01_extracted_html/acadauto/sendcommand_see_also.htm`
- `01_extracted_html/acadauto/ex_getvariable.htm`
- `01_extracted_html/acadauto/idh_getvariable.htm`
- `01_extracted_html/acadauto/getvariable_see_also.htm`
- `01_extracted_html/acadauto/ex_setvariable.htm`
- `01_extracted_html/acadauto/idh_setvariable.htm`
- `01_extracted_html/acadauto/setvariable_see_also.htm`
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
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `Document`
- `Layout`
