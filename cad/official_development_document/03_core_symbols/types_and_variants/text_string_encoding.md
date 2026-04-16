# text_string_encoding

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `str -> COM string; 字体效果由 TextStyle/Big Font 共同决定`

## 作用
说明中文图签和目录文字涉及的编码/字体兼容问题，避免写入成功但显示异常。

## 高频场景
- 图签字段中文回写
- 目录文本中文生成

## 项目路径
- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

## 相关任务
- `update_titleblock_fields`
- `generate_or_update_catalog`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/pywin32_type_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:ex_activetextstyle`
- `acad_aag:GUID_29E096AD_6237_4B26_8964_A55DDF7197F8`
- `acadauto:ex_textstyle`
- `acad_aag:GUID_004B0417_AB7A_46A2_AAD0_1B2E90C9F3ED`
- `acadauto:idh_textstyle_object`
- `acadauto:idh_textstyle`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-29E096AD-6237-4B26-8964-A55DDF7197F8.htm`
- `01_extracted_html/acadauto/ex_textstyle.htm`
- `01_extracted_html/acad_aag/GUID-004B0417-AB7A-46A2-AAD0-1B2E90C9F3ED.htm`
- `01_extracted_html/acadauto/idh_textstyle_object.htm`
- `01_extracted_html/acadauto/idh_textstyle.htm`
- `01_extracted_html/acadauto/ex_activetextstyle.htm`
