# 3dPolyline

## 基本信息
- kind: `object`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `model_space.Add3DPoly(points_array)`

## 作用
表示由直线段组成的三维路径对象，适合表达空间路径、轮廓骨架和剖切参考线。

## 高频场景
- 表达空间路径
- 建立三维轮廓骨架
- 作为后续区域/实体构造前的路径表达

## 项目路径
- `cad/system/licad.py`
- `cad/scripts/CAD_basic.py`
- `cad/scripts/Scheme_drawing/draw_building_outline.py`

## 相关任务
- `create_3d_path_or_profile`
- `read_3d_object_spatial_identity`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:idh_3dpoly_object`
- `acadauto:idh_add3dpoly`
- `acadauto:ex_add3dpoly`
- `acadauto:add3dpoly_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dpoly_object.htm`
- `01_extracted_html/acadauto/ex_add3dpoly.htm`
- `01_extracted_html/acadauto/idh_add3dpoly.htm`
- `01_extracted_html/acadauto/add3dpoly_see_also.htm`
