# bounding_box_tuple

## 基本信息
- kind: `type_topic`
- owners: `pywin32, ActiveX`
- pywin32: `entity.GetBoundingBox(min_pt, max_pt) -> bbox tuple`

## 作用
统一说明如何把 GetBoundingBox 的双输出点归一成稳定的 `(xmin, ymin, xmax, ymax)` 结构。

## 高频场景
- 打印框识别
- 图签定位
- 对象统计裁剪

## 项目路径
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`
- `cad/system/content_analysis_dwg_file.py`

## 相关任务
- `get_bounding_box_and_object_counts`
- `read_layout_plot_info`

## 规则与来源
- rule_refs:
- `05_pywin32_bridge/point_array_rules.md`
- `05_pywin32_bridge/variant_rules.md`
- source_topic_ids:
- `acadauto:ex_getboundingbox`
- `acadauto:idh_getboundingbox`
- `acadauto:getboundingbox_see_also`
- source_html_paths:
- `01_extracted_html/acadauto/ex_getboundingbox.htm`
- `01_extracted_html/acadauto/idh_getboundingbox.htm`
- `01_extracted_html/acadauto/getboundingbox_see_also.htm`
