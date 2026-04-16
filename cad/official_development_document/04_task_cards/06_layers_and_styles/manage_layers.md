# 任务卡：读取 / 创建 / 切换图层

## Exact Entry
- task_id: `CAD2021-TASK-013`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Layers`
- `Layer`
- `Document`
- owners:
- `Layers`
- `Layer`
- `Document`
- implementation_entries:
- `ensure_layer` -> `cad/scripts/CAD_basic.py`
- `draw_outline` -> `cad/scripts/Scheme_drawing/draw_building_outline.py`

## Natural Language Expansion
- aliases_en:
- `manage layers`
- `create switch layer`
- `ensure drawing layer`
- aliases_zh_support:
- `读取创建切换图层`
- `图层管理`
- `确保图层存在`
- keywords_zh_support:
- `图层`
- `创建图层`
- `切换图层`

## Goal
为施工图对象创建、目录生成和图签整理提供图层控制能力。

## Priority Path
1. 先读 `Document.Layers`
2. 已有施工图创建逻辑可参考 `draw_building_outline.py`

## Related Core Symbols
- `Layers`
- `Layer`
- `Document`

## Workflow
1. 尝试 `Layers.Item(name)` 读取目标图层
2. 不存在时调用 `Layers.Add(name)`
3. 按需要设置当前活动图层或实体图层

## Project Notes
- 不要在未知图层锁定/冻结状态下直接批量改写。

## Common Failures
- 目标图层不存在
- 当前图层被冻结或锁定

## Verification
- 图层创建或切换后可再次读取

## Project Paths
- `cad/scripts/Scheme_drawing/draw_building_outline.py`
- `cad/scripts/CAD_basic.py`
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `cad/system/licad.py`
- `cad/system/CAD_core.py`

## Pywin32 Rules
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Source Trace
- source_topic_ids:
- `acad_aag:GUID_D86DF08B_BBD3_4E0F_AB75_13B2C4AD972C`
- `acad_aag:GUID_72E0EC31_B232_4688_BFFF_CA10F42E1034`
- `acad_aag:GUID_5B2CCA06_1A61_46F6_BABE_6B8BEA1DF20D`
- `acad_aag:GUID_463948A3_EE1E_4448_B3A6_B0B67B8902F1`
- `acad_aag:GUID_A1815C41_7753_45F5_B8BC_31F67F79F138`
- `acad_aag:GUID_52B191C9_B183_4B20_96FD_AE3F44FA9AFA`
- `acad_aag:GUID_435FABFF_D469_4004_AB1E_A47295959AB1`
- `acad_aag:GUID_49A4B783_D344_497B_BF37_3B4925813B31`
- `acad_aag:GUID_83045B84_E056_4AE6_AEF5_D48AFB4F9F78`
- `acad_aag:GUID_45654BC7_F6B5_48E9_82FD_CED83FB956C4`
- `acad_aag:GUID_4F4377B1_07C8_4DDA_94D9_23DBF493C871`
- `acad_aag:GUID_675CFE8A_2256_4808_A1C8_186E68A69496`
- `acad_aag:GUID_679FBC1A_DE7B_44BA_9F8B_CD6FF1660D67`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-D86DF08B-BBD3-4E0F-AB75-13B2C4AD972C.htm`
- `01_extracted_html/acad_aag/GUID-72E0EC31-B232-4688-BFFF-CA10F42E1034.htm`
- `01_extracted_html/acad_aag/GUID-5B2CCA06-1A61-46F6-BABE-6B8BEA1DF20D.htm`
- `01_extracted_html/acad_aag/GUID-463948A3-EE1E-4448-B3A6-B0B67B8902F1.htm`
- `01_extracted_html/acad_aag/GUID-A1815C41-7753-45F5-B8BC-31F67F79F138.htm`
- `01_extracted_html/acad_aag/GUID-52B191C9-B183-4B20-96FD-AE3F44FA9AFA.htm`
- `01_extracted_html/acad_aag/GUID-435FABFF-D469-4004-AB1E-A47295959AB1.htm`
- `01_extracted_html/acad_aag/GUID-49A4B783-D344-497B-BF37-3B4925813B31.htm`
- `01_extracted_html/acad_aag/GUID-83045B84-E056-4AE6-AEF5-D48AFB4F9F78.htm`
- `01_extracted_html/acad_aag/GUID-45654BC7-F6B5-48E9-82FD-CED83FB956C4.htm`
- `01_extracted_html/acad_aag/GUID-4F4377B1-07C8-4DDA-94D9-23DBF493C871.htm`
- `01_extracted_html/acad_aag/GUID-675CFE8A-2256-4808-A1C8-186E68A69496.htm`
- `01_extracted_html/acad_aag/GUID-679FBC1A-DE7B-44BA-9F8B-CD6FF1660D67.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- reference_objects:
- `Layers`
- `Layer`
