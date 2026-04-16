# 任务卡：创建基础几何对象

## Exact Entry
- task_id: `CAD2021-TASK-009`
- primary_retrieval_order: `task_id -> symbol -> owner -> project_function -> module_path -> aliases_en -> aliases_zh/keywords_zh`
- symbols:
- `ModelSpace`
- `AddLine`
- `AddPolyline`
- `AddText`
- `AddMText`
- owners:
- `ModelSpace`
- `PaperSpace`
- `Block`
- implementation_entries:
- `draw_outline` -> `cad/scripts/Scheme_drawing/draw_building_outline.py`
- `ensure_layer` -> `cad/scripts/CAD_basic.py`
- `get_acad_doc` -> `cad/system/licad.py`

## Natural Language Expansion
- aliases_en:
- `create basic geometry smoke`
- `geometry smoke test`
- `add line polyline text`
- aliases_zh_support:
- `创建基础几何对象`
- `几何烟雾测试`
- `添加直线文字多段线`
- keywords_zh_support:
- `基础几何`
- `直线`
- `多段线`
- `文字`

## Goal
用最小几何创建验证 pywin32 调用链，并支撑施工图基础构造。

## Priority Path
1. 优先使用 `AddLine` 作为连接烟雾测试
2. 需要文本或多段线时再扩到 `AddText`、`AddMText`、`AddPolyline`

## Related Core Symbols
- `ModelSpace`
- `AddLine`
- `AddPolyline`
- `AddText`
- `AddMText`

## Workflow
1. 确定目标空间
2. 准备三维点或坐标数组
3. 调用创建方法
4. 必要时立即清理测试对象

## Project Notes
- 不要在不了解当前空间时直接落实体创建。

## Common Failures
- 点格式错误
- 对象插到错误空间

## Verification
- 对象创建成功并可再次读取

## Project Paths
- `cad/system/licad.py`
- `cad/scripts/Scheme_drawing/draw_building_outline.py`
- `cad/scripts/CAD_basic.py`
- `cad/system/CAD_selection.py`

## Pywin32 Rules
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/pywin32_type_rules.md`

## Aggregated Rule Refs
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/pywin32_type_rules.md`
- `05_pywin32_bridge/collection_rules.md`
- `05_pywin32_bridge/common_failures.md`

## Source Trace
- source_topic_ids:
- `acadauto:ex_modelspace`
- `acadauto:ex_elevationmodelspace`
- `acadauto:idh_modelspace_collection`
- `acadauto:idh_modelspace`
- `acadauto:idh_elevationmodelspace`
- `acadauto:ex_addline`
- `acadauto:idh_addline`
- `acadauto:addline_see_also`
- `acadauto:ex_addpolyline`
- `acadauto:ex_addlightweightpolyline`
- `acadauto:idh_addlightweightpolyline`
- `acadauto:idh_addpolyline`
- `acadauto:addlightweightpolyline_see_also`
- `acadauto:ex_addtext`
- `acadauto:idh_addtext`
- `acadauto:addtext_see_also`
- `acadauto:ex_addmtext`
- `acadauto:idh_addmtext`
- `acadauto:addmtext_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_modelspace.htm`
- `01_extracted_html/acadauto/ex_elevationmodelspace.htm`
- `01_extracted_html/acadauto/idh_modelspace_collection.htm`
- `01_extracted_html/acadauto/idh_modelspace.htm`
- `01_extracted_html/acadauto/idh_elevationmodelspace.htm`
- `01_extracted_html/acadauto/ex_addline.htm`
- `01_extracted_html/acadauto/idh_addline.htm`
- `01_extracted_html/acadauto/addline_see_also.htm`
- `01_extracted_html/acadauto/ex_addpolyline.htm`
- `01_extracted_html/acadauto/ex_addlightweightpolyline.htm`
- `01_extracted_html/acadauto/idh_addlightweightpolyline.htm`
- `01_extracted_html/acadauto/idh_addpolyline.htm`
- `01_extracted_html/acadauto/addlightweightpolyline_see_also.htm`
- `01_extracted_html/acadauto/ex_addtext.htm`
- `01_extracted_html/acadauto/idh_addtext.htm`
- `01_extracted_html/acadauto/addtext_see_also.htm`
- `01_extracted_html/acadauto/ex_addmtext.htm`
- `01_extracted_html/acadauto/idh_addmtext.htm`
- `01_extracted_html/acadauto/addmtext_see_also.htm`

## Stability
- stability_level: `high`

## Reference DWG And Objects
- reference_dwgs:
- `cad/scripts/drawing_basic_service/print/cases/assets/混合空间0109.dwg`
- reference_objects:
- `ModelSpace`
- `AcDbLine`
- `AcDbPolyline`
- `AcDbText`
