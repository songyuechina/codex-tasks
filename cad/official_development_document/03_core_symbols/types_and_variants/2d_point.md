# 2d_point

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `(x, y) -> 项目内先归一，再决定是否补 z`

## 作用
说明窗口点这类二维语义坐标如何统一落到稳定的 COM 传参格式。

## 高频场景
- SetWindowToPlot 窗口点
- bbox 转窗口点

## 项目路径
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/scripts/drawing_basic_service/print/print_area_analysis.py`

## 相关任务
- `execute_layout_plot`
- `get_bounding_box_and_object_counts`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:ex_setwindowtoplot`
- `acadauto:ex_getwindowtoplot`
- `acadauto:idh_getwindowtoplot`
- `acadauto:idh_setwindowtoplot`
- `acadauto:getwindowtoplot_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_setwindowtoplot.htm`
- `01_extracted_html/acadauto/ex_getwindowtoplot.htm`
- `01_extracted_html/acadauto/idh_getwindowtoplot.htm`
- `01_extracted_html/acadauto/idh_setwindowtoplot.htm`
- `01_extracted_html/acadauto/getwindowtoplot_see_also.htm`
