# safearray

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `通常经 VARIANT(VT_ARRAY | base_type, data) 间接接触 SAFEARRAY`

## 作用
说明 SAFEARRAY 是许多 ActiveX 数组参数/返回值的底层载体，帮助正确理解 pywin32 包装形态。

## 高频场景
- Variant 数组底层结构识别
- 数组参数类型排错

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_selection.py`

## 相关任务
- `build_selection_set`
- `create_basic_geometry_smoke`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/pywin32_type_rules.md`
- source_topic_ids:
- `acad_aag:GUID_5004997B_3086_4D07_A0A1_AEB32B7727A2`
- `acad_aag:GUID_192B537E_8F89_4F21_BD5D_28B9E3918C88`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-192B537E-8F89-4F21-BD5D-28B9E3918C88.htm`
- `01_extracted_html/acad_aag/GUID-5004997B-3086-4D07-A0A1-AEB32B7727A2.htm`
