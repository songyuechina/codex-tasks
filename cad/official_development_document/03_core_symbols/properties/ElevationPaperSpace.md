# ElevationPaperSpace

## 基本信息
- kind: `property`
- owners: `Document`
- pywin32: `C.doc.ElevationPaperSpace`

## 作用
表示图纸空间当前高程，决定布局上下文里仅给 XY 时如何补出 Z 值。

## 高频场景
- 在布局空间补全 3D 点
- 校验图纸空间高程基准
- 避免模型/图纸空间高程混淆

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_core.py`

## 相关任务
- `understand_and_convert_coordinate_systems`
- `read_3d_object_spatial_identity`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_elevationpaperspace`
- `acadauto:ex_elevationpaperspace`
- source_html_paths:
- `01_extracted_html/acadauto/idh_elevationpaperspace.htm`
- `01_extracted_html/acadauto/ex_elevationpaperspace.htm`
