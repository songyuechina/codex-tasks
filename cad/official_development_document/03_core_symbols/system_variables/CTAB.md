# CTAB

## 基本信息
- kind: `system_variable`
- owners: `Document`
- pywin32: `C.doc.GetVariable("CTAB")`

## 作用
当前标签页布局名，是从当前任务定位真实布局的直接变量入口。

## 高频场景
- 回读当前布局名
- 布局切换后验证是否到位
- 打印任务开始前确认目标布局已经激活

## 项目路径
- `cad/system/CAD_core.py`
- `cad/system/CAD_coordination.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`

## 相关任务
- `determine_space_and_layout`
- `switch_to_target_layout`
- `execute_layout_plot`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:ex_getvariable`
- `acadauto:ex_activelayout`
- `acad_aag:GUID_A55918B2_0D79_476A_9A20_A1BA80AB2EDD`
- `acad_aag:GUID_10F797AA_5032_4298_A2A5_C69449275F0E`
- `acad_aag:topichead_9`
- `acadauto:ex_layoutshowplotsetup`
- `acadauto:ex_setlayoutstoplot`
- `acad_aag:GUID_10344852_4888_4237_8EB6_5EBE24D5C87C`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `01_extracted_html/acad_aag/topichead_9.htm`
- `01_extracted_html/acadauto/ex_layoutshowplotsetup.htm`
- `01_extracted_html/acadauto/ex_setlayoutstoplot.htm`
- `01_extracted_html/acad_aag/GUID-10344852-4888-4237-8EB6-5EBE24D5C87C.htm`
- `01_extracted_html/acadauto/ex_getvariable.htm`
- `01_extracted_html/acadauto/ex_activelayout.htm`
- `01_extracted_html/acad_aag/GUID-A55918B2-0D79-476A-9A20-A1BA80AB2EDD.htm`
