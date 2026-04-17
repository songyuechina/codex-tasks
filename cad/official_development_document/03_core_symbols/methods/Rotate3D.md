# Rotate3D

## 基本信息
- kind: `method`
- owners: `All Drawing Objects`
- pywin32: `object.Rotate3D(point1, point2, rotation_angle_radians)`

## 作用
围绕由两点定义的 3D 轴旋转对象，是空间方向调整的主入口。

## 高频场景
- 围绕空间轴线旋转构件
- 纠正三维对象方向
- 统一对象空间姿态

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
- `acadauto:idh_rotate3d`
- `acad_aag:GUID_3FEB0A3C_E4B1_40DF_A4DF_CAB22F1E2A92`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-3FEB0A3C-E4B1-40DF-A4DF-CAB22F1E2A92.htm`
- `01_extracted_html/acadauto/idh_rotate3d.htm`
