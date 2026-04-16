# CMDECHO

## 基本信息
- kind: `system_variable`
- owners: `Document`
- pywin32: `C.doc.SetVariable("CMDECHO", 0 or 1)`

## 作用
控制命令回显，用于调试和批处理环境归一，但不替代真正的同步判断。

## 高频场景
- 调试阶段临时打开回显
- 批处理阶段关闭噪声输出

## 项目路径
- `cad/system/CAD_coordination.py`
- `cad/system/licad.py`

## 相关任务
- `sendcommand_fallback`
- `execute_layout_plot`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:ex_getvariable`
- `acadauto:ex_setvariable`
- `acadauto:ex_sendcommand`
- `acad_aag:GUID_0A56CD7D_C18E_4A94_B0A7_6F70956A21A9`
- `acad_aag:GUID_ABEEEBC2_3EBE_4AB5_B082_6C736D677965`
- `acad_aag:GUID_17924929_1A87_4B6B_A8A0_AD6762581335`
- source_html_paths:
- `01_extracted_html/acadauto/ex_setvariable.htm`
- `01_extracted_html/acad_aag/GUID-0A56CD7D-C18E-4A94-B0A7-6F70956A21A9.htm`
- `01_extracted_html/acadauto/ex_sendcommand.htm`
- `01_extracted_html/acad_aag/GUID-ABEEEBC2-3EBE-4AB5-B082-6C736D677965.htm`
- `01_extracted_html/acad_aag/GUID-17924929-1A87-4B6B-A8A0-AD6762581335.htm`
- `01_extracted_html/acadauto/ex_getvariable.htm`
