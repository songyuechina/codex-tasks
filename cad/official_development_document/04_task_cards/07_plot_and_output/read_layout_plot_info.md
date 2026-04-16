# 任务卡：读取布局打印信息

## Exact Entry
- task_id: `CAD2021-TASK-014`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Layout`
- `Plot`
- `RefreshPlotDeviceInfo`
- `ConfigName`
- `CanonicalMediaName`
- `SetWindowToPlot`
- `ActiveLayout`
- owners:
- `Layout`
- `Plot`
- implementation_entries:
- `analyze_print_info_jobs` -> `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `collect_print_jobs` -> `cad/scripts/drawing_basic_service/print/print_policy.py`

## Natural Language Expansion
- aliases_en:
- `read layout plot info`
- `inspect plot configuration`
- `read layout paper and window`
- aliases_zh_support:
- `读取布局打印信息`
- `读取打印配置`
- `读取纸张窗口范围`
- keywords_zh_support:
- `打印信息`
- `布局打印`
- `纸张`
- `打印窗口`

## Goal
读取布局对象的打印设备、纸张、窗口范围和相关图签信息。

## Priority Path
1. 优先看 `Layout` / `Plot` / `RefreshPlotDeviceInfo` / `ConfigName` / `CanonicalMediaName` / `SetWindowToPlot`
2. 业务层优先参考 `print_info_analysis.py` 和 `print_policy.py`

## Related Core Symbols
- `Layout`
- `Plot`
- `RefreshPlotDeviceInfo`
- `ConfigName`
- `CanonicalMediaName`
- `SetWindowToPlot`
- `ActiveLayout`

## Workflow
1. 取得目标布局对象
2. 刷新打印设备信息并固定 `ConfigName`
3. 再次刷新后读取 `CanonicalMediaName`、旋转、窗口或块快照信息
4. 结合图签信息形成后续打印计划输入

## Project Notes
- 当前主线是打印执行链，不要把布局打印信息读取做成孤立脚本。

## Common Failures
- 设备信息未刷新
- 布局对象读取不稳定
- 打印框与角标匹配失败

## Verification
- 产出可用于打印计划的布局信息结构

## Project Paths
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/drawing_basic_service/print/print_policy.py`
- `cad/scripts/CAD_basic.py`
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`

## Pywin32 Rules
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/plot_layout_rules.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/plot_layout_rules.md`

## Source Trace
- source_topic_ids:
- `acad_aag:GUID_10F797AA_5032_4298_A2A5_C69449275F0E`
- `acad_aag:topichead_9`
- `acadauto:ex_layoutshowplotsetup`
- `acadauto:ex_setlayoutstoplot`
- `acad_aag:GUID_10344852_4888_4237_8EB6_5EBE24D5C87C`
- `acad_aag:GUID_9091E614_25B8_452E_A67A_301939B52161`
- `acadauto:ex_defaultplotstyleforlayer`
- `acadauto:ex_refreshplotdeviceinfo`
- `acadauto:idh_refreshplotdeviceinfo`
- `acadauto:refreshplotdeviceinfo_see_also`
- `acadauto:ex_setwindowtoplot`
- `acadauto:idh_setwindowtoplot`
- `acadauto:setwindowtoplot_see_also`
- `acadauto:ex_activelayout`
- `acadauto:idh_activelayout`
- `acadauto:activelayout_see_also`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `01_extracted_html/acad_aag/topichead_9.htm`
- `01_extracted_html/acadauto/ex_layoutshowplotsetup.htm`
- `01_extracted_html/acadauto/ex_setlayoutstoplot.htm`
- `01_extracted_html/acad_aag/GUID-10344852-4888-4237-8EB6-5EBE24D5C87C.htm`
- `01_extracted_html/acad_aag/GUID-9091E614-25B8-452E-A67A-301939B52161.htm`
- `01_extracted_html/acadauto/ex_defaultplotstyleforlayer.htm`
- `01_extracted_html/acadauto/ex_refreshplotdeviceinfo.htm`
- `01_extracted_html/acadauto/idh_refreshplotdeviceinfo.htm`
- `01_extracted_html/acadauto/refreshplotdeviceinfo_see_also.htm`
- `01_extracted_html/acadauto/ex_setwindowtoplot.htm`
- `01_extracted_html/acadauto/idh_setwindowtoplot.htm`
- `01_extracted_html/acadauto/setwindowtoplot_see_also.htm`
- `01_extracted_html/acadauto/ex_activelayout.htm`
- `01_extracted_html/acadauto/idh_activelayout.htm`
- `01_extracted_html/acadauto/activelayout_see_also.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/农建房施工图【电气】-0930_t6_t3.dwg`
- reference_objects:
- `Layout`
- `Plot`
- `AcDbBlockReference`
