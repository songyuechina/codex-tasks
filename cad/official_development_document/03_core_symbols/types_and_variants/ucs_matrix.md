# ucs_matrix

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `Variant (4x4 array of doubles)`

## 作用
统一说明 UCS 返回的 4x4 矩阵结构，以及它如何进入 TransformBy。

## 高频场景
- 读取 UCS 变换矩阵
- 把矩阵直接传给 TransformBy
- 分析 UCS 到 WCS 的映射关系

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_core.py`

## 相关任务
- `understand_and_convert_coordinate_systems`
- `apply_3d_transform_to_objects`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:idh_getucsmatrix`
- `acadauto:idh_transformby`
- `acadauto:ex_getucsmatrix`
- `acadauto:ex_transformby`
- `acadauto:getucsmatrix_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_getucsmatrix.htm`
- `01_extracted_html/acadauto/idh_getucsmatrix.htm`
- `01_extracted_html/acadauto/ex_transformby.htm`
- `01_extracted_html/acadauto/idh_transformby.htm`
- `01_extracted_html/acadauto/getucsmatrix_see_also.htm`
