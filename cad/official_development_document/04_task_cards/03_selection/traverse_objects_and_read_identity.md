# 任务卡：遍历对象并读取 ObjectName / Handle / Layer

## Exact Entry
- task_id: `CAD2021-TASK-007`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `ObjectName`
- `Handle`
- `Layer`
- `SelectionSet`
- owners:
- `Entity`
- `SelectionSet`
- implementation_entries:
- `collect_space_entity_snapshots` -> `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `get_dwg_graphics_summary` -> `cad/system/content_analysis_dwg_file.py`

## Natural Language Expansion
- aliases_en:
- `traverse objects and read identity`
- `read objectname handle layer`
- `entity identity scan`
- aliases_zh_support:
- `遍历对象并读取标识`
- `读取ObjectName Handle Layer`
- keywords_zh_support:
- `对象遍历`
- `句柄`
- `图层`
- `类型识别`

## Goal
对选中的实体或空间内实体做基础类型识别与追踪标识读取。

## Priority Path
1. 优先先读 `ObjectName`
2. 再按需要读取 `Handle` 与 `Layer`
3. 高频统计逻辑优先参考打印分析链现有实现

## Related Core Symbols
- `ObjectName`
- `Handle`
- `Layer`
- `SelectionSet`

## Workflow
1. 遍历实体集合
2. 读取 `ObjectName` 作为首层类型判断
3. 按需要读取 `Handle` 与 `Layer`
4. 将结果标准化后输出

## Project Notes
- Handle 很有用，但批量读取会慢。

## Common Failures
- 天正对象属性访问兼容问题
- 大批量句柄读取慢

## Verification
- 输出中包含稳定类型名和可追踪句柄

## Project Paths
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `cad/system/content_analysis_dwg_file.py`
- `cad/scripts/drawing_basic_service/print/print_policy.py`

## Pywin32 Rules
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Source Trace
- source_topic_ids:
- `acadauto:ex_objectname`
- `acadauto:idh_objectname`
- `acadauto:objectname_see_also`
- `acadauto:ex_handle`
- `acadauto:idh_handle`
- `acad_aag:GUID_2FF2F1B5_FFAC_420A_A741_15D1FC1A571E`
- `acadauto:ex_handletoobject`
- `acadauto:idh_handletoobject`
- `acad_aag:GUID_52B191C9_B183_4B20_96FD_AE3F44FA9AFA`
- `acad_aag:GUID_435FABFF_D469_4004_AB1E_A47295959AB1`
- `acad_aag:GUID_49A4B783_D344_497B_BF37_3B4925813B31`
- `acad_aag:GUID_D86DF08B_BBD3_4E0F_AB75_13B2C4AD972C`
- `acad_aag:GUID_72E0EC31_B232_4688_BFFF_CA10F42E1034`
- `acadauto:ex_selectionsets`
- `acadauto:ex_activeselectionset`
- `acadauto:ex_pickfirstselectionset`
- `acadauto:idh_selectionset_object`
- `acadauto:idh_activeselectionset`
- source_html_paths:
- `01_extracted_html/acadauto/ex_objectname.htm`
- `01_extracted_html/acadauto/idh_objectname.htm`
- `01_extracted_html/acadauto/objectname_see_also.htm`
- `01_extracted_html/acadauto/ex_handle.htm`
- `01_extracted_html/acadauto/idh_handle.htm`
- `01_extracted_html/acad_aag/GUID-2FF2F1B5-FFAC-420A-A741-15D1FC1A571E.htm`
- `01_extracted_html/acadauto/ex_handletoobject.htm`
- `01_extracted_html/acadauto/idh_handletoobject.htm`
- `01_extracted_html/acad_aag/GUID-52B191C9-B183-4B20-96FD-AE3F44FA9AFA.htm`
- `01_extracted_html/acad_aag/GUID-435FABFF-D469-4004-AB1E-A47295959AB1.htm`
- `01_extracted_html/acad_aag/GUID-49A4B783-D344-497B-BF37-3B4925813B31.htm`
- `01_extracted_html/acad_aag/GUID-D86DF08B-BBD3-4E0F-AB75-13B2C4AD972C.htm`
- `01_extracted_html/acad_aag/GUID-72E0EC31-B232-4688-BFFF-CA10F42E1034.htm`
- `01_extracted_html/acadauto/ex_selectionsets.htm`
- `01_extracted_html/acadauto/ex_activeselectionset.htm`
- `01_extracted_html/acadauto/ex_pickfirstselectionset.htm`
- `01_extracted_html/acadauto/idh_selectionset_object.htm`
- `01_extracted_html/acadauto/idh_activeselectionset.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/农建房施工图【电气】-0930_t6_t3.dwg`
- reference_objects:
- `AcDbEntity`
- `AcDbBlockReference`
- `SelectionSet`
