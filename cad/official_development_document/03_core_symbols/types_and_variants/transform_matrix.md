# transform_matrix

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `((R00,R01,R02,T0),(R10,R11,R12,T1),(R20,R21,R22,T2),(0,0,0,1))`

## 作用
统一说明 4x4 变换矩阵的旋转项与平移项布局，避免 TransformBy 传参错误。

## 高频场景
- 构造 TransformBy 入参
- 组合旋转和平移
- 复用 GetUCSMatrix 返回矩阵

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_core.py`

## 相关任务
- `apply_3d_transform_to_objects`
- `understand_and_convert_coordinate_systems`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:idh_transformby`
- `acadauto:idh_getucsmatrix`
- `acadauto:ex_getucsmatrix`
- `acadauto:ex_transformby`
- `acadauto:getucsmatrix_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_getucsmatrix.htm`
- `01_extracted_html/acadauto/idh_getucsmatrix.htm`
- `01_extracted_html/acadauto/ex_transformby.htm`
- `01_extracted_html/acadauto/idh_transformby.htm`
- `01_extracted_html/acadauto/getucsmatrix_see_also.htm`
