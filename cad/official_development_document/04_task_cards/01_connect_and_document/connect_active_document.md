# 任务卡：连接 AutoCAD 并获取活动文档

## Exact Entry
- task_id: `CAD2021-TASK-001`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Application`
- `Documents`
- `Document`
- owners:
- `Application`
- `Documents`
- `Document`
- implementation_entries:
- `get_acad_doc` -> `cad/system/licad.py`

## Natural Language Expansion
- aliases_en:
- `connect active document`
- `get active document`
- `attach cad document`
- `connect autocad session`
- aliases_zh_support:
- `连接CAD`
- `获取活动文档`
- `连接AutoCAD`
- keywords_zh_support:
- `活动文档`
- `连接`
- `受控入口`

## Goal
在 CAD2021 + pywin32 环境里，以项目受控入口获取稳定的活动文档对象。

## Priority Path
1. 优先使用 `from system.licad import C`
2. 连接异常时先看 `licad.get_acad_doc()` 的启动与自愈逻辑
3. 避免业务层长期直接使用 `GetActiveObject` / `Dispatch`

## Related Core Symbols
- `Application`
- `Documents`
- `Document`

## Workflow
1. 导入 `C` 并访问 `C.doc`
2. 若首次连接失败，检查天正受控入口是否可启动
3. 确认 `ActiveDocument` 已就绪并能读取 `doc.Name`
4. 必要时做一次轻量 COM 烟雾验证

## Project Notes
- 项目统一连接规则优先于 CHM 原始示例。

## Common Failures
- CAD 进程存在但 COM 未就绪
- 应用已连接但无文档
- gen_py 缓存损坏

## Verification
- 读取当前 `doc.Name`
- 读取 `C.doc.ModelSpace` 不报错

## Project Paths
- `cad/system/licad.py`
- `cad/system/CAD_core.py`

## Pywin32 Rules
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/pywin32_type_rules.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/common_failures.md`
- `05_pywin32_bridge/pywin32_type_rules.md`
- `05_pywin32_bridge/collection_rules.md`

## Source Trace
- source_topic_ids:
- `acad_aag:GUID_9C66C307_9ED1_492B_9CE5_F81F73671C88`
- `acad_aag:GUID_BCE7E749_DCCB_4914_9E52_CC1265A3574F`
- `acad_aag:GUID_FD48FD40_1077_4054_8A15_CA55DADF821F`
- `acad_aag:GUID_A2018D0D_2778_4823_A4A2_1A467A807F42`
- `acad_aag:GUID_C584A219_3E90_4D1B_B382_6000F00CE9B0`
- `acad_aag:GUID_83045B84_E056_4AE6_AEF5_D48AFB4F9F78`
- `acadauto:ex_documents`
- `acadauto:ex_loadacadlspinalldocuments`
- `acadauto:idh_documents_collection`
- `acadauto:idh_documents`
- `acad_aag:GUID_45654BC7_F6B5_48E9_82FD_CED83FB956C4`
- `acad_aag:GUID_4F4377B1_07C8_4DDA_94D9_23DBF493C871`
- `acad_aag:GUID_675CFE8A_2256_4808_A1C8_186E68A69496`
- `acad_aag:GUID_679FBC1A_DE7B_44BA_9F8B_CD6FF1660D67`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-9C66C307-9ED1-492B-9CE5-F81F73671C88.htm`
- `01_extracted_html/acad_aag/GUID-BCE7E749-DCCB-4914-9E52-CC1265A3574F.htm`
- `01_extracted_html/acad_aag/GUID-FD48FD40-1077-4054-8A15-CA55DADF821F.htm`
- `01_extracted_html/acad_aag/GUID-A2018D0D-2778-4823-A4A2-1A467A807F42.htm`
- `01_extracted_html/acad_aag/GUID-C584A219-3E90-4D1B-B382-6000F00CE9B0.htm`
- `01_extracted_html/acad_aag/GUID-83045B84-E056-4AE6-AEF5-D48AFB4F9F78.htm`
- `01_extracted_html/acadauto/ex_documents.htm`
- `01_extracted_html/acadauto/ex_loadacadlspinalldocuments.htm`
- `01_extracted_html/acadauto/idh_documents_collection.htm`
- `01_extracted_html/acadauto/idh_documents.htm`
- `01_extracted_html/acad_aag/GUID-45654BC7-F6B5-48E9-82FD-CED83FB956C4.htm`
- `01_extracted_html/acad_aag/GUID-4F4377B1-07C8-4DDA-94D9-23DBF493C871.htm`
- `01_extracted_html/acad_aag/GUID-675CFE8A-2256-4808-A1C8-186E68A69496.htm`
- `01_extracted_html/acad_aag/GUID-679FBC1A-DE7B-44BA-9F8B-CD6FF1660D67.htm`

## Stability
- stability_level: `high`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- reference_objects:
- `Application`
- `Document`
