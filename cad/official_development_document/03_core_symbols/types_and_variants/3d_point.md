# 3d_point

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `(x, y, z) or VARIANT(VT_ARRAY | VT_R8, (x, y, z))`

## 作用
统一说明项目中的三维点入参形式，避免二维点或裸 Variant 写错。

## 高频场景
- AddLine 起点终点
- InsertBlock 插入点
- 窗口输出坐标准备

## 项目路径
- `cad/system/licad.py`
- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`

## 相关任务
- `create_basic_geometry_smoke`
- `insert_block_or_dwg`
- `execute_layout_plot`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- `05_pywin32_bridge/pywin32_type_rules.md`
- source_topic_ids:
- `acadauto:ex_addline`
- `acadauto:ex_insertblock`
- `acadauto:ex_setwindowtoplot`
- `acadauto:ex_addminsertblock`
- `acadauto:idh_addline`
- source_html_paths:
- `01_extracted_html/acadauto/ex_insertblock.htm`
- `01_extracted_html/acadauto/ex_setwindowtoplot.htm`
- `01_extracted_html/acadauto/ex_addminsertblock.htm`
- `01_extracted_html/acadauto/ex_addline.htm`
- `01_extracted_html/acadauto/idh_addline.htm`
