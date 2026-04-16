# CMDACTIVE

## 基本信息
- kind: `system_variable`
- owners: `Document`
- pywin32: `C.doc.GetVariable("CMDACTIVE")`

## 作用
命令执行态位标志，是 SendCommand 回退链等待和同步判断的重要读数。

## 高频场景
- 命令发送后等待空闲
- 打印回退链防止命令串扰
- 布局切换命令同步判断

## 项目路径
- `cad/system/CAD_coordination.py`
- `cad/system/licad.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`

## 相关任务
- `sendcommand_fallback`
- `switch_to_target_layout`
- `execute_layout_plot`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/sendcommand_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:ex_getvariable`
- `acadauto:ex_sendcommand`
- `acadauto:idh_sendcommand`
- `acad_aag:GUID_0A56CD7D_C18E_4A94_B0A7_6F70956A21A9`
- `acad_aag:GUID_ABEEEBC2_3EBE_4AB5_B082_6C736D677965`
- `acad_aag:GUID_17924929_1A87_4B6B_A8A0_AD6762581335`
- source_html_paths:
- `01_extracted_html/acadauto/ex_sendcommand.htm`
- `01_extracted_html/acadauto/idh_sendcommand.htm`
- `01_extracted_html/acad_aag/GUID-0A56CD7D-C18E-4A94-B0A7-6F70956A21A9.htm`
- `01_extracted_html/acad_aag/GUID-ABEEEBC2-3EBE-4AB5-B082-6C736D677965.htm`
- `01_extracted_html/acad_aag/GUID-17924929-1A87-4B6B-A8A0-AD6762581335.htm`
- `01_extracted_html/acadauto/ex_getvariable.htm`
