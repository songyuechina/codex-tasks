# Add3DFace

## 基本信息
- kind: `method`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `model_space.Add3DFace(point1, point2, point3[, point4])`

## 作用
根据三点或四点创建 3DFace，用于表达面、共面关系和剖切辅助面。

## 高频场景
- 建立三维面
- 表达构件平面关系
- 为区域/剖切构造面级参考

## 项目路径
- `cad/system/licad.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `create_3d_path_or_profile`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:idh_add3dface`
- `acadauto:idh_3dface_object`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dface_object.htm`
- `01_extracted_html/acadauto/idh_add3dface.htm`
