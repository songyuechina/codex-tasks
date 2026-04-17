# ScaleEntity

## 基本信息
- kind: `method`
- owners: `All Drawing Objects`
- pywin32: `object.ScaleEntity(base_point, scale_factor)`

## 作用
围绕基点在 X/Y/Z 方向等比缩放对象，用于统一空间尺寸关系。

## 高频场景
- 统一构件比例
- 调整实体或路径尺寸
- 对位前做尺寸归一

## 项目路径
- `cad/system/licad.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `apply_3d_transform_to_objects`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_scaleentity`
- source_html_paths:
- `01_extracted_html/acadauto/idh_scaleentity.htm`
