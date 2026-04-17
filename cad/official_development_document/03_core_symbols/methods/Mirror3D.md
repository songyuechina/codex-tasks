# Mirror3D

## 基本信息
- kind: `method`
- owners: `All Drawing Objects`
- pywin32: `ret = object.Mirror3D(point1, point2, point3)`

## 作用
围绕由三点定义的平面镜像对象，用于表达对称关系和平面对位。

## 高频场景
- 围绕平面生成对称对象
- 用平面关系修正构件放置
- 快速建立镜像空间表达

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
- `acadauto:idh_mirror3d`
- `acadauto:idh_3dpoly_object`
- `acadauto:idh_region_object`
- `acadauto:ex_mirror3d`
- `acadauto:mirror3d_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/idh_mirror3d.htm`
- `01_extracted_html/acadauto/ex_mirror3d.htm`
- `01_extracted_html/acadauto/mirror3d_see_also.htm`
- `01_extracted_html/acadauto/idh_3dpoly_object.htm`
- `01_extracted_html/acadauto/idh_region_object.htm`
