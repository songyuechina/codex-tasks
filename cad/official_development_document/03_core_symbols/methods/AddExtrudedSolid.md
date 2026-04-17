# AddExtrudedSolid

## 基本信息
- kind: `method`
- owners: `ModelSpace, PaperSpace, Block`
- pywin32: `model_space.AddExtrudedSolid(profile_region, height, taper_angle)`

## 作用
根据 Region、高度和锥角创建 3DSolid，是从平面轮廓进入构件体量表达的主入口。

## 高频场景
- 由剖面轮廓生成构件体量
- 把区域转成可剖切实体
- 建立空间构造关系

## 项目路径
- `cad/system/licad.py`
- `cad/scripts/CAD_basic.py`
- `cad/system/content_analysis_dwg_file.py`

## 相关任务
- `create_region_and_extrude_solid`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/section_region_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_addextrudedsolid`
- `acadauto:idh_3dsolid_object`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dsolid_object.htm`
- `01_extracted_html/acadauto/idh_addextrudedsolid.htm`
