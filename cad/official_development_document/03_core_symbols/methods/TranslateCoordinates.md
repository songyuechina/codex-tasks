# TranslateCoordinates

## 基本信息
- kind: `method`
- owners: `Utility`
- pywin32: `utility.TranslateCoordinates(original_point, from_cs, to_cs, disp[, ocs_normal])`

## 作用
在 WCS/UCS/OCS/DCS 之间转换点或位移向量，是三维空间关系表达的基础方法。

## 高频场景
- 在 WCS 与 OCS 之间换算点
- 读取对象 OCS 点并还原到 WCS
- 在布局/显示坐标与模型坐标之间换算

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_core.py`
- `cad/system/content_analysis_dwg_file.py`

## 相关任务
- `understand_and_convert_coordinate_systems`
- `read_3d_object_spatial_identity`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_translatecoordinates`
- `acad_aag:GUID_06B18EED_D4E3_4B81_ACB8_037E884CB93D`
- `acad_aag:GUID_6954AAF3_7107_4D93_A2CE_FE859F3F9902`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-06B18EED-D4E3-4B81-ACB8-037E884CB93D.htm`
- `01_extracted_html/acad_aag/GUID-6954AAF3-7107-4D93-A2CE-FE859F3F9902.htm`
- `01_extracted_html/acadauto/idh_translatecoordinates.htm`
