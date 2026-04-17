# ElevationModelSpace

## 基本信息
- kind: `property`
- owners: `Document`
- pywin32: `C.doc.ElevationModelSpace`

## 作用
表示模型空间当前高程，决定仅给 XY 时如何补出 Z 值。

## 高频场景
- 在模型空间补全 3D 点
- 校验当前模型空间高程基准
- 防止误把二维输入当零高程

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
- `acadauto:idh_elevationmodelspace`
- `acadauto:ex_elevationmodelspace`
- source_html_paths:
- `01_extracted_html/acadauto/idh_elevationmodelspace.htm`
- `01_extracted_html/acadauto/ex_elevationmodelspace.htm`
