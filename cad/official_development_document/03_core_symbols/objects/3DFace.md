# 3DFace

## 基本信息
- kind: `object`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `model_space.Add3DFace(point1, point2, point3[, point4])`

## 作用
表示由三点或四点定义的三维面对象，可用于构造面、剖切参考和平面关系表达。

## 高频场景
- 表达三维面
- 构造共面轮廓参考
- 为区域/剖切前置建模提供面级对象

## 项目路径
- `cad/system/licad.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `create_3d_path_or_profile`
- `section_3d_geometry_for_2d_expression`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:idh_3dface_object`
- `acadauto:idh_add3dface`
- `acadauto:ex_add3dface`
- `acadauto:add3dface_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dface_object.htm`
- `01_extracted_html/acadauto/ex_add3dface.htm`
- `01_extracted_html/acadauto/idh_add3dface.htm`
- `01_extracted_html/acadauto/add3dface_see_also.htm`
