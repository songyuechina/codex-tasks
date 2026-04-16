# TILEMODE

## 基本信息
- kind: `system_variable`
- owners: `Document`
- pywin32: `C.doc.GetVariable("TILEMODE") / C.doc.SetVariable("TILEMODE", 0)`

## 作用
控制模型空间主态和布局/图纸空间主态，是布局判断与打印前上下文校验的底层变量。

## 高频场景
- 判断当前是否仍处于模型空间
- 布局切换前校验上下文
- 打印前确认纸空间相关状态

## 项目路径
- `cad/system/CAD_core.py`
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`

## 相关任务
- `determine_space_and_layout`
- `switch_to_target_layout`
- `read_layout_plot_info`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:ex_activespace`
- `acad_aag:GUID_4EAB8372_859A_4C6E_BEE5_B2C8EBA31AD7`
- `acad_aag:GUID_9DCF17E7_717B_4766_AFFE_D3C9ED506BB8`
- source_html_paths:
- `01_extracted_html/acadauto/ex_activespace.htm`
- `01_extracted_html/acad_aag/GUID-4EAB8372-859A-4C6E-BEE5-B2C8EBA31AD7.htm`
- `01_extracted_html/acad_aag/GUID-9DCF17E7-717B-4766-AFFE-D3C9ED506BB8.htm`
