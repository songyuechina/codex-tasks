# LTSCALE

## 基本信息
- kind: `system_variable`
- owners: `Document`
- pywin32: `C.doc.GetVariable("LTSCALE") / C.doc.SetVariable("LTSCALE", value)`

## 作用
控制全局线型比例，会直接影响布局输出和打印观感。

## 高频场景
- 打印前核查线型缩放
- 模板插入后统一线型表现

## 项目路径
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `read_layout_plot_info`
- `execute_layout_plot`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:ex_setvariable`
- `acad_aag:GUID_4D1D635B_663F_4BB3_A6BE_46C7D13A39D8`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-4D1D635B-663F-4BB3-A6BE-46C7D13A39D8.htm`
- `01_extracted_html/acadauto/ex_setvariable.htm`
