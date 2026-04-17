# AddExtrudedSolidAlongPath

## 基本信息
- kind: `method`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `model_space.AddExtrudedSolidAlongPath(profile_region, path_object)`

## 作用
根据 Region 和路径对象创建沿路径挤出的 3DSolid，适合表达沿轴线或轨迹生成的构件。

## 高频场景
- 沿路径生成实体
- 表达沿轴线构件
- 把轮廓沿空间轨迹转成体量

## 项目路径
- `cad/system/licad.py`
- `cad/scripts/CAD_basic.py`
- `cad/system/content_analysis_dwg_file.py`

## 相关任务
- `create_region_and_extrude_solid`
- `create_3d_path_or_profile`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_addextrudedsolidalongpath`
- `acadauto:idh_3dsolid_object`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dsolid_object.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolidalongpath.htm`
