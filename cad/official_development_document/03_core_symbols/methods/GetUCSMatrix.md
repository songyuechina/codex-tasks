# GetUCSMatrix

## 基本信息
- kind: `method`
- owners: `UCS`
- pywin32: `ucs.GetUCSMatrix()`

## 作用
获取 UCS 的 4x4 变换矩阵，用于把对象或点稳定地映射到指定坐标基准。

## 高频场景
- 读取 UCS 变换矩阵
- 配合 TransformBy 执行整体坐标基准变换
- 建立从 UCS 到 WCS 的稳定映射

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
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_getucsmatrix`
- `acadauto:idh_ucs_object`
- `acadauto:idh_transformby`
- `acadauto:ex_transformby`
- `acadauto:transformby_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/idh_getucsmatrix.htm`
- `01_extracted_html/acadauto/ex_transformby.htm`
- `01_extracted_html/acadauto/idh_transformby.htm`
- `01_extracted_html/acadauto/transformby_see_also.htm`
- `01_extracted_html/acadauto/idh_ucs_object.htm`
