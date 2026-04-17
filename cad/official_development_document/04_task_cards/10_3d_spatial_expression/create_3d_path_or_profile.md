# 任务卡：创建三维路径或轮廓

## Exact Entry
- task_id: `CAD2021-TASK-021`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `Add3DPoly`
- `3dPolyline`
- `Add3DFace`
- `3DFace`
- `3d_point`
- owners:
- `ModelSpace`
- `Block`
- `3dPolyline`
- `3DFace`
- implementation_entries:
- `draw_outline` -> `cad/scripts/Scheme_drawing/draw_building_outline.py`
- `draw_polyline` -> `cad/scripts/CAD_basic.py`
- `draw_lwpolyline` -> `cad/scripts/CAD_basic.py`

## Natural Language Expansion
- aliases_en:
- `create 3d path or profile`
- `build 3d polyline path`
- `create profile for region or solid`
- aliases_zh_support:
- `创建三维路径或轮廓`
- `建立三维路径`
- `建立轮廓 profile`
- keywords_zh_support:
- `三维路径`
- `轮廓`
- `3dPolyline`
- `3DFace`

## Goal
用空间点、3D 路径和面表达轮廓骨架，为 Region、Solid 和剖切主链准备受控输入。

## Priority Path
1. 优先看 `Add3DPoly`、`3dPolyline`、`Add3DFace`、`3DFace`
2. 需要统一点数组时先看 `3d_point` 和 `point_array_rules.md`
3. 轮廓后续若要进区域/实体，先保证点序和共面关系明确

## Related Core Symbols
- `Add3DPoly`
- `3dPolyline`
- `Add3DFace`
- `3DFace`
- `3d_point`

## Workflow
1. 先确定路径或轮廓要表达的是轴线、轮廓骨架还是面
2. 统一点数组为三元素 3D 点
3. 路径类优先用 `Add3DPoly`，面类再用 `Add3DFace`
4. 把结果作为后续 Region/Solid/剖切任务的输入对象

## Project Notes
- 这张卡强调的是服务空间关系表达的路径和轮廓，不是复杂造型。

## Common Failures
- 点数组元素数不是 3 的倍数
- 轮廓顺序错误导致后续区域构造失败
- 把二维轮廓直接误当空间路径

## Verification
- 返回对象可被识别为 `3dPolyline` 或 `3DFace`
- 读取坐标序列时点序与预期一致

## Project Paths
- `cad/scripts/Scheme_drawing/draw_building_outline.py`
- `cad/scripts/CAD_basic.py`
- `cad/system/licad.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`

## Pywin32 Rules
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/pywin32_type_rules.md`

## Source Trace
- source_topic_ids:
- `acadauto:idh_add3dpoly`
- `acadauto:idh_3dpoly_object`
- `acadauto:ex_add3dpoly`
- `acadauto:add3dpoly_see_also`
- `acadauto:idh_add3dface`
- `acadauto:idh_3dface_object`
- `acadauto:ex_add3dface`
- `acadauto:add3dface_see_also`
- `acadauto:ex_addline`
- `acadauto:ex_insertblock`
- `acadauto:ex_setwindowtoplot`
- `acadauto:ex_addminsertblock`
- `acadauto:idh_addline`
- source_html_paths:
- `01_extracted_html/acadauto/idh_3dpoly_object.htm`
- `01_extracted_html/acadauto/idh_add3dpoly.htm`
- `01_extracted_html/acadauto/ex_add3dpoly.htm`
- `01_extracted_html/acadauto/add3dpoly_see_also.htm`
- `01_extracted_html/acadauto/idh_3dface_object.htm`
- `01_extracted_html/acadauto/idh_add3dface.htm`
- `01_extracted_html/acadauto/ex_add3dface.htm`
- `01_extracted_html/acadauto/add3dface_see_also.htm`
- `01_extracted_html/acadauto/ex_insertblock.htm`
- `01_extracted_html/acadauto/ex_setwindowtoplot.htm`
- `01_extracted_html/acadauto/ex_addminsertblock.htm`
- `01_extracted_html/acadauto/ex_addline.htm`
- `01_extracted_html/acadauto/idh_addline.htm`

## Stability
- stability_level: `medium`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- reference_objects:
- `3dPolyline`
- `3DFace`
