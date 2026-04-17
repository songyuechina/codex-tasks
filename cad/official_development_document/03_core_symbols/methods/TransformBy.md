# TransformBy

## 基本信息
- kind: `method`
- owners: `All Drawing Objects, AttributeReference`
- pywin32: `object.TransformBy(transformation_matrix)`

## 作用
使用 4x4 变换矩阵移动、缩放或旋转对象，是统一空间变换和基准切换的高级入口。

## 高频场景
- 根据 UCS 矩阵整体变换对象
- 统一执行平移+旋转+缩放
- 把对象迁移到指定空间基准

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_core.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `apply_3d_transform_to_objects`
- `understand_and_convert_coordinate_systems`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_transformby`
- `acadauto:idh_getucsmatrix`
- `acad_aag:GUID_19A5491D_7675_4ECF_A66A_5D309A14429F`
- `acadauto:ex_getucsmatrix`
- `acadauto:getucsmatrix_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_getucsmatrix.htm`
- `01_extracted_html/acadauto/idh_getucsmatrix.htm`
- `01_extracted_html/acadauto/idh_transformby.htm`
- `01_extracted_html/acadauto/getucsmatrix_see_also.htm`
- `01_extracted_html/acad_aag/GUID-19A5491D-7675-4ECF-A66A-5D309A14429F.htm`
