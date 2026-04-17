# UCS

## 基本信息
- kind: `object`
- owners: `Document, UCSs`
- pywin32: `C.doc.ActiveUCS / C.doc.UserCoordinateSystems.Item(name)`

## 作用
表示用户坐标系对象，是从绘图基准切入三维空间表达和矩阵变换的正式入口。

## 高频场景
- 读取当前活动 UCS
- 获取 UCS 变换矩阵
- 把对象对齐到特定 UCS 基准

## 项目路径
- `cad/system/licad.py`
- `cad/system/CAD_core.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `understand_and_convert_coordinate_systems`
- `apply_3d_transform_to_objects`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/common_failures.md`
- source_topic_ids:
- `acadauto:idh_ucs_object`
- `acadauto:idh_activeucs`
- `acadauto:idh_getucsmatrix`
- `acadauto:ex_activeucs`
- `acadauto:ex_getucsmatrix`
- source_html_paths:
- `01_extracted_html/acadauto/ex_activeucs.htm`
- `01_extracted_html/acadauto/idh_activeucs.htm`
- `01_extracted_html/acadauto/ex_getucsmatrix.htm`
- `01_extracted_html/acadauto/idh_getucsmatrix.htm`
- `01_extracted_html/acadauto/idh_ucs_object.htm`
