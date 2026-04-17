# Add3DPoly

## 基本信息
- kind: `method`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `model_space.Add3DPoly(points_array)`

## 作用
根据三维点数组创建 3dPolyline，是空间路径和轮廓骨架的正式创建入口。

## 高频场景
- 建立空间路径
- 建立三维轮廓
- 为后续剖切或实体生成准备路径对象

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
- `acadauto:idh_add3dpoly`
- `acadauto:idh_3dpoly_object`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dpoly_object.htm`
- `01_extracted_html/acadauto/idh_add3dpoly.htm`
