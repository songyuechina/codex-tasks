# 任务卡：对对象应用三维变换

## Exact Entry
- task_id: `CAD2021-TASK-023`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Move`
- `Rotate3D`
- `Mirror3D`
- `ScaleEntity`
- `TransformBy`
- `transform_matrix`
- `ucs_matrix`
- owners:
- `3dPolyline`
- `Region`
- `3DSolid`
- `Document`
- implementation_entries:
- `move_entities_in_region` -> `cad/scripts/CAD_basic.py`
- `transform_point_by_block` -> `cad/scripts/CAD_basic.py`
- `get_obj_loc` -> `cad/system/CAD_core.py`

## Natural Language Expansion
- aliases_en:
- `apply 3d transform to objects`
- `rotate mirror scale transform objects`
- `3d object alignment`
- aliases_zh_support:
- `对对象应用三维变换`
- `三维变换对象`
- `空间对位`
- keywords_zh_support:
- `Rotate3D`
- `Mirror3D`
- `ScaleEntity`
- `TransformBy`
- `空间对位`

## Goal
通过平移、旋转、镜像、缩放和矩阵变换完成对象空间对位和方向修正。

## Priority Path
1. 优先看 `Move`、`Rotate3D`、`Mirror3D`、`ScaleEntity`
2. 需要统一做复杂变换时，再进入 `TransformBy` 和 `transform_matrix`
3. 若变换与 UCS 基准相关，先回到 `GetUCSMatrix`

## Related Core Symbols
- `Move`
- `Rotate3D`
- `Mirror3D`
- `ScaleEntity`
- `TransformBy`
- `transform_matrix`
- `ucs_matrix`

## Workflow
1. 先判断任务是位移、轴旋转、平面镜像、缩放还是矩阵统一变换
2. 准备轴线、平面、基点或 4x4 矩阵输入
3. 执行对应的变换方法
4. 回读对象位置或边界，确认空间关系没有跑偏

## Project Notes
- 这张卡强调空间对位正确性，而不是造型动作本身。

## Common Failures
- 弧度和角度混淆
- 轴线或平面定义退化
- 矩阵格式非法
- 在集合迭代中直接做写操作变换

## Verification
- 对象包围盒或关键点位按预期变化
- 变换后对象仍能进入后续剖切或打印表达链

## Project Paths
- `cad/scripts/CAD_basic.py`
- `cad/system/CAD_core.py`
- `cad/system/licad.py`

## Pywin32 Rules
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Source Trace
- source_topic_ids:
- `acadauto:idh_move`
- `acad_aag:GUID_19A5491D_7675_4ECF_A66A_5D309A14429F`
- `acadauto:idh_remove`
- `acadauto:idh_rotate3d`
- `acad_aag:GUID_3FEB0A3C_E4B1_40DF_A4DF_CAB22F1E2A92`
- `acadauto:idh_mirror3d`
- `acadauto:idh_3dpoly_object`
- `acadauto:idh_region_object`
- `acadauto:ex_mirror3d`
- `acadauto:mirror3d_see_also`
- `acadauto:idh_scaleentity`
- `acadauto:idh_transformby`
- `acadauto:idh_getucsmatrix`
- `acadauto:ex_getucsmatrix`
- `acadauto:getucsmatrix_see_also`
- `acadauto:ex_transformby`
- source_html_paths:
- `01_extracted_html/acad_aag/GUID-19A5491D-7675-4ECF-A66A-5D309A14429F.htm`
- `01_extracted_html/acadauto/idh_move.htm`
- `01_extracted_html/acadauto/idh_remove.htm`
- `01_extracted_html/acad_aag/GUID-3FEB0A3C-E4B1-40DF-A4DF-CAB22F1E2A92.htm`
- `01_extracted_html/acadauto/idh_rotate3d.htm`
- `01_extracted_html/acadauto/idh_mirror3d.htm`
- `01_extracted_html/acadauto/ex_mirror3d.htm`
- `01_extracted_html/acadauto/mirror3d_see_also.htm`
- `01_extracted_html/acadauto/idh_3dpoly_object.htm`
- `01_extracted_html/acadauto/idh_region_object.htm`
- `01_extracted_html/acadauto/idh_scaleentity.htm`
- `01_extracted_html/acadauto/ex_getucsmatrix.htm`
- `01_extracted_html/acadauto/idh_getucsmatrix.htm`
- `01_extracted_html/acadauto/idh_transformby.htm`
- `01_extracted_html/acadauto/getucsmatrix_see_also.htm`
- `01_extracted_html/acadauto/ex_transformby.htm`

## Stability
- stability_level: `high`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- `cad/scripts/drawing_basic_service/print/cases/assets/远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- reference_objects:
- `3dPolyline`
- `Region`
- `3DSolid`
