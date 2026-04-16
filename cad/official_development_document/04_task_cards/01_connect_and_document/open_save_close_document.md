# 任务卡：打开 / 保存 / 关闭文档

## Exact Entry
- task_id: `CAD2021-TASK-002`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Documents`
- `Document`
- `Application`
- owners:
- `Documents`
- `Document`
- implementation_entries:
- `open_file` -> `cad/system/licad.py`
- `save_file` -> `cad/system/licad.py`
- `close_file` -> `cad/system/licad.py`
- `close_dwg_by_name` -> `cad/system/licad.py`

## Natural Language Expansion
- aliases_en:
- `open save close document`
- `document lifecycle`
- `open drawing file`
- `close active drawing`
- aliases_zh_support:
- `打开保存关闭文档`
- `DWG 生命周期`
- `打开图纸`
- `关闭图纸`
- keywords_zh_support:
- `打开`
- `保存`
- `关闭`
- `文档`

## Goal
对 DWG 文档执行基础文件生命周期操作，并保持当前环境稳定。

## Priority Path
1. 先走 `Documents` / `Document` 的 COM 路径
2. 若任务已纳入打印主链，优先复用 `print_runner.py` 和执行链现有入口

## Related Core Symbols
- `Documents`
- `Document`
- `Application`

## Workflow
1. 通过 `C.acad.Documents` 打开或新建文档
2. 对目标文档执行保存
3. 在关闭前确认无待处理命令态
4. 批量任务后恢复到项目预期状态

## Project Notes
- 真实打印任务里不要绕过执行链手写零散打开/关闭逻辑。

## Common Failures
- 文件被占用
- 切文档时活动文档未同步
- 关闭后引用悬空

## Verification
- 文档数量变化符合预期
- 关闭后活动文档重新可读

## Project Paths
- `cad/system/licad.py`
- `cad/system/CAD_core.py`
- `cad/scripts/drawing_basic_service/print/print_runner.py`

## Pywin32 Rules
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/collection_rules.md`

## Source Trace
- source_topic_ids:
- `acad_aag:GUID_83045B84_E056_4AE6_AEF5_D48AFB4F9F78`
- `acadauto:ex_documents`
- `acadauto:ex_loadacadlspinalldocuments`
- `acadauto:idh_documents_collection`
- `acadauto:idh_documents`
- `acad_aag:GUID_45654BC7_F6B5_48E9_82FD_CED83FB956C4`
- `acad_aag:GUID_4F4377B1_07C8_4DDA_94D9_23DBF493C871`
- `acad_aag:GUID_675CFE8A_2256_4808_A1C8_186E68A69496`
- `acad_aag:GUID_679FBC1A_DE7B_44BA_9F8B_CD6FF1660D67`
- `acad_aag:GUID_9C66C307_9ED1_492B_9CE5_F81F73671C88`
- `acad_aag:GUID_BCE7E749_DCCB_4914_9E52_CC1265A3574F`
- `acad_aag:GUID_FD48FD40_1077_4054_8A15_CA55DADF821F`
- `acad_aag:GUID_A2018D0D_2778_4823_A4A2_1A467A807F42`
- `acad_aag:GUID_C584A219_3E90_4D1B_B382_6000F00CE9B0`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-83045B84-E056-4AE6-AEF5-D48AFB4F9F78.htm`
- `01_extracted_html/acadauto/ex_documents.htm`
- `01_extracted_html/acadauto/ex_loadacadlspinalldocuments.htm`
- `01_extracted_html/acadauto/idh_documents_collection.htm`
- `01_extracted_html/acadauto/idh_documents.htm`
- `01_extracted_html/acad_aag/GUID-45654BC7-F6B5-48E9-82FD-CED83FB956C4.htm`
- `01_extracted_html/acad_aag/GUID-4F4377B1-07C8-4DDA-94D9-23DBF493C871.htm`
- `01_extracted_html/acad_aag/GUID-675CFE8A-2256-4808-A1C8-186E68A69496.htm`
- `01_extracted_html/acad_aag/GUID-679FBC1A-DE7B-44BA-9F8B-CD6FF1660D67.htm`
- `01_extracted_html/acad_aag/GUID-9C66C307-9ED1-492B-9CE5-F81F73671C88.htm`
- `01_extracted_html/acad_aag/GUID-BCE7E749-DCCB-4914-9E52-CC1265A3574F.htm`
- `01_extracted_html/acad_aag/GUID-FD48FD40-1077-4054-8A15-CA55DADF821F.htm`
- `01_extracted_html/acad_aag/GUID-A2018D0D-2778-4823-A4A2-1A467A807F42.htm`
- `01_extracted_html/acad_aag/GUID-C584A219-3E90-4D1B-B382-6000F00CE9B0.htm`

## Stability
- stability_level: `high`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- reference_objects:
- `Documents`
- `Document`
