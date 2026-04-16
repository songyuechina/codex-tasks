# FILEDIA

## 基本信息
- kind: `system_variable`
- owners: `Document`
- pywin32: `C.doc.SetVariable("FILEDIA", 0 or 1)`

## 作用
控制文件类对话框显隐，是批处理和无交互命令链必须明确的环境变量。

## 高频场景
- 关闭对话框避免阻塞
- 批处理结束后恢复交互环境

## 项目路径
- `cad/system/CAD_coordination.py`
- `cad/system/CAD_core.py`
- `cad/system/licad.py`

## 相关任务
- `sendcommand_fallback`
- `open_save_close_document`
- `execute_layout_plot`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:ex_getvariable`
- `acadauto:ex_setvariable`
- `acad_aag:GUID_DD968EB1_6DED_44D4_9956_9E8B843FBA1B`
- `acad_aag:GUID_EF5CD99F_A6DC_46BC_862E_02C6D5908B3E`
- `acadauto:idh_setvariable`
- `acad_aag:GUID_329CE95B_61A4_4EC4_A9CB_BE342F1BDCFA`
- source_html_paths:
- `01_extracted_html/acadauto/ex_setvariable.htm`
- `01_extracted_html/acad_aag/GUID-DD968EB1-6DED-44D4-9956-9E8B843FBA1B.htm`
- `01_extracted_html/acad_aag/GUID-EF5CD99F-A6DC-46BC-862E-02C6D5908B3E.htm`
- `01_extracted_html/acadauto/idh_setvariable.htm`
- `01_extracted_html/acad_aag/GUID-329CE95B-61A4-4EC4-A9CB-BE342F1BDCFA.htm`
- `01_extracted_html/acadauto/ex_getvariable.htm`
