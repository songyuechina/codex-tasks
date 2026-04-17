# AddRevolvedSolid

## 基本信息
- kind: `method`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `model_space.AddRevolvedSolid(profile_region, axis_point, axis_dir, angle)`

## 作用
根据 Region 与旋转轴生成旋转实体，用于表达由剖面绕轴形成的空间构件。

## 高频场景
- 绕轴生成实体
- 表达旋转对称构件
- 从二维剖面进入三维体量

## 项目路径
- `cad/system/licad.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `create_region_and_extrude_solid`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_addrevolvedsolid`
- `acadauto:idh_3dsolid_object`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dsolid_object.htm`
- `01_extracted_html/acadauto/idh_addrevolvedsolid.htm`
