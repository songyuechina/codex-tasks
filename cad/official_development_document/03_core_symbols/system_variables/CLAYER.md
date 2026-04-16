# CLAYER

## 基本信息
- kind: `system_variable`
- owners: `Document`
- pywin32: `C.doc.GetVariable("CLAYER") / C.doc.ActiveLayer`

## 作用
当前活动图层变量，用于对象落层、插图签和图层环境归一。

## 高频场景
- 对象创建前切换目标图层
- 插图签后恢复原图层

## 项目路径
- `cad/scripts/CAD_basic.py`
- `cad/scripts/Scheme_drawing/draw_building_outline.py`

## 相关任务
- `manage_layers`
- `insert_company_title_block`
- `create_basic_geometry_smoke`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:ex_activelayer`
- `acad_aag:GUID_D86DF08B_BBD3_4E0F_AB75_13B2C4AD972C`
- `acad_aag:GUID_52B191C9_B183_4B20_96FD_AE3F44FA9AFA`
- `acad_aag:GUID_435FABFF_D469_4004_AB1E_A47295959AB1`
- `acad_aag:GUID_49A4B783_D344_497B_BF37_3B4925813B31`
- `acad_aag:GUID_72E0EC31_B232_4688_BFFF_CA10F42E1034`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-52B191C9-B183-4B20-96FD-AE3F44FA9AFA.htm`
- `01_extracted_html/acad_aag/GUID-435FABFF-D469-4004-AB1E-A47295959AB1.htm`
- `01_extracted_html/acad_aag/GUID-49A4B783-D344-497B-BF37-3B4925813B31.htm`
- `01_extracted_html/acad_aag/GUID-D86DF08B-BBD3-4E0F-AB75-13B2C4AD972C.htm`
- `01_extracted_html/acad_aag/GUID-72E0EC31-B232-4688-BFFF-CA10F42E1034.htm`
- `01_extracted_html/acadauto/ex_activelayer.htm`
