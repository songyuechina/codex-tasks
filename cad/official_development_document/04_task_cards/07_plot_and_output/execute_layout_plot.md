# 任务卡：执行布局窗口打印

## Exact Entry
- task_id: `CAD2021-TASK-015`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Plot`
- `Layout`
- `SetWindowToPlot`
- `RefreshPlotDeviceInfo`
- `SendCommand`
- owners:
- `Layout`
- `Plot`
- `Document`
- implementation_entries:
- `execute_print_plan` -> `cad/scripts/drawing_basic_service/print/print_executor.py`
- `export_layout_window_lisp_fit` -> `cad/scripts/drawing_basic_service/print/print_executor.py`
- `send_cmd_with_sync` -> `cad/system/CAD_coordination.py`

## Natural Language Expansion
- aliases_en:
- `execute layout plot`
- `plot layout to pdf`
- `export layout window`
- aliases_zh_support:
- `执行布局窗口打印`
- `输出布局PDF`
- `导出打印窗口`
- keywords_zh_support:
- `打印PDF`
- `布局输出`
- `打印执行`

## Goal
按布局和窗口范围输出 PDF，并受运行监督链保护。

## Priority Path
1. 优先复用 `print_executor.execute_print_plan()`
2. 单任务布局输出优先参考 `export_layout_window_lisp_fit()`
3. 必要时参考 `CAD_basic` 的布局输出经验

## Related Core Symbols
- `Plot`
- `Layout`
- `SetWindowToPlot`
- `RefreshPlotDeviceInfo`
- `SendCommand`

## Workflow
1. 确认目标 DWG 和布局已就绪
2. 准备打印设备、纸张、CTB、方向和窗口点
3. 调用布局输出函数
4. 校验 PDF 是否生成成功

## Project Notes
- 打印执行应在 runtime guard 保护下推进。

## Common Failures
- 布局准备失败
- 输出文件被占用
- 命令回退未完成

## Verification
- PDF 文件存在且页尺寸符合预期

## Project Paths
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/scripts/CAD_basic.py`
- `cad/system/CAD_coordination.py`
- `cad/system/CAD_core.py`
- `cad/system/licad.py`

## Pywin32 Rules
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/collection_rules.md`

## Source Trace
- source_topic_ids:
- `acad_aag:topichead_9`
- `acad_aag:GUID_9091E614_25B8_452E_A67A_301939B52161`
- `acadauto:ex_layoutshowplotsetup`
- `acadauto:ex_setlayoutstoplot`
- `acadauto:ex_defaultplotstyleforlayer`
- `acad_aag:GUID_10F797AA_5032_4298_A2A5_C69449275F0E`
- `acad_aag:GUID_10344852_4888_4237_8EB6_5EBE24D5C87C`
- `acadauto:ex_setwindowtoplot`
- `acadauto:idh_setwindowtoplot`
- `acadauto:setwindowtoplot_see_also`
- `acadauto:ex_refreshplotdeviceinfo`
- `acadauto:idh_refreshplotdeviceinfo`
- `acadauto:refreshplotdeviceinfo_see_also`
- `acadauto:ex_sendcommand`
- `acadauto:idh_sendcommand`
- `acadauto:sendcommand_see_also`
- source_html_paths:
- `01_extracted_html/acad_aag/topichead_9.htm`
- `01_extracted_html/acad_aag/GUID-9091E614-25B8-452E-A67A-301939B52161.htm`
- `01_extracted_html/acadauto/ex_layoutshowplotsetup.htm`
- `01_extracted_html/acadauto/ex_setlayoutstoplot.htm`
- `01_extracted_html/acadauto/ex_defaultplotstyleforlayer.htm`
- `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `01_extracted_html/acad_aag/GUID-10344852-4888-4237-8EB6-5EBE24D5C87C.htm`
- `01_extracted_html/acadauto/ex_setwindowtoplot.htm`
- `01_extracted_html/acadauto/idh_setwindowtoplot.htm`
- `01_extracted_html/acadauto/setwindowtoplot_see_also.htm`
- `01_extracted_html/acadauto/ex_refreshplotdeviceinfo.htm`
- `01_extracted_html/acadauto/idh_refreshplotdeviceinfo.htm`
- `01_extracted_html/acadauto/refreshplotdeviceinfo_see_also.htm`
- `01_extracted_html/acadauto/ex_sendcommand.htm`
- `01_extracted_html/acadauto/idh_sendcommand.htm`
- `01_extracted_html/acadauto/sendcommand_see_also.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/农建房施工图【电气】-0930_t6_t3.dwg`
- reference_objects:
- `Layout`
- `Plot`
- `AcDbPolyline`
