# TEXTSTYLE

## 基本信息
- kind: `system_variable`
- owners: `Document`
- pywin32: `C.doc.GetVariable("TEXTSTYLE") / C.doc.ActiveTextStyle`

## 作用
控制当前文字样式，对图签字段写入、目录生成和中文显示稳定性都有直接影响。

## 高频场景
- 文本写入前核查当前样式
- 中文字体/大字体排查

## 项目路径
- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

## 相关任务
- `update_titleblock_fields`
- `generate_or_update_catalog`
- `create_basic_geometry_smoke`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/common_patterns.md`
- `05_pywin32_bridge/pywin32_type_rules.md`
- source_topic_ids:
- `acadauto:ex_activetextstyle`
- `acad_aag:GUID_29E096AD_6237_4B26_8964_A55DDF7197F8`
- `acadauto:idh_activetextstyle`
- `acadauto:ex_textstyle`
- `acad_aag:GUID_004B0417_AB7A_46A2_AAD0_1B2E90C9F3ED`
- source_html_paths:
- `01_extracted_html/acadauto/ex_activetextstyle.htm`
- `01_extracted_html/acadauto/idh_activetextstyle.htm`
- `01_extracted_html/acadauto/ex_textstyle.htm`
- `01_extracted_html/acad_aag/GUID-004B0417-AB7A-46A2-AAD0-1B2E90C9F3ED.htm`
- `01_extracted_html/acad_aag/GUID-29E096AD-6237-4B26-8964-A55DDF7197F8.htm`
