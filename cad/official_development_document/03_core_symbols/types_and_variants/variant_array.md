# variant_array

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `VARIANT(VT_ARRAY | base_type, data)`

## 作用
统一说明数组型返回值和入参为何经常以 Variant 包裹，以及项目里何时需要显式处理。

## 高频场景
- 选择集过滤数组
- 坐标数组和边界框解释
- 低层几何参数包装

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_selection.py`

## 相关任务
- `build_selection_set`
- `get_bounding_box_and_object_counts`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/pywin32_type_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- source_topic_ids:
- `acad_aag:GUID_5004997B_3086_4D07_A0A1_AEB32B7727A2`
- `acad_aag:GUID_192B537E_8F89_4F21_BD5D_28B9E3918C88`
- `acad_aag:GUID_F6B0A90B_B484_4B2E_A0E1_FE6B7441ADBC`
- `acad_aag:GUID_CC394595_C4A3_47D4_A040_C58C16B92918`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-5004997B-3086-4D07-A0A1-AEB32B7727A2.htm`
- `01_extracted_html/acad_aag/GUID-192B537E-8F89-4F21-BD5D-28B9E3918C88.htm`
- `01_extracted_html/acad_aag/GUID-F6B0A90B-B484-4B2E-A0E1-FE6B7441ADBC.htm`
- `01_extracted_html/acad_aag/GUID-CC394595-C4A3-47D4-A040-C58C16B92918.htm`
