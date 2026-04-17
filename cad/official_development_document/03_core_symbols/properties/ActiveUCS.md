# ActiveUCS

## 基本信息
- kind: `property`
- owners: `Document`
- pywin32: `C.doc.ActiveUCS`

## 作用
表示当前活动 UCS，是从文档当前三维基准切入空间表达的正式属性入口。

## 高频场景
- 读取当前活动 UCS
- 切换后确认 UCS 是否到位
- 为对象变换取基准矩阵

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_core.py`

## 相关任务
- `understand_and_convert_coordinate_systems`
- `apply_3d_transform_to_objects`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_activeucs`
- `acadauto:idh_ucs_object`
- source_html_paths:
- `01_extracted_html/acadauto/idh_activeucs.htm`
- `01_extracted_html/acadauto/idh_ucs_object.htm`
