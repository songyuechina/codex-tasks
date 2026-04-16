# collection_iteration

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `for item in collection / collection.Item(name_or_index)`

## 作用
统一说明对 Layouts、SelectionSets、Attributes 等集合对象的推荐遍历方式。

## 高频场景
- 枚举布局
- 遍历块属性
- 遍历选择集

## 项目路径
- `cad/system/CAD_core.py`
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

## 相关任务
- `enumerate_layouts`
- `build_selection_set`
- `read_block_attributes`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acad_aag:GUID_589F246A_41BE_4D38_AA91_9FDA3ABABEA6`
- `acad_aag:GUID_05AC034B_3E51_4EC3_85BE_B3153B8CC40B`
- `acad_aag:GUID_A73AB626_5DAF_4F03_936A_655F772263E0`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-589F246A-41BE-4D38-AA91-9FDA3ABABEA6.htm`
- `01_extracted_html/acad_aag/GUID-05AC034B-3E51-4EC3-85BE-B3153B8CC40B.htm`
- `01_extracted_html/acad_aag/GUID-A73AB626-5DAF-4F03-936A-655F772263E0.htm`
