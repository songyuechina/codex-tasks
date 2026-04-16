# Promotion Log

## 2026-04-12

### ConfigName

- 原等级：`06_on_demand_index` 低频索引
- 晋升原因：真实打印主链中，设备选择已直接决定后续纸张列表和窗口打印稳定性
- 补齐文件：
  - `03_core_symbols/properties/ConfigName.md`
  - `03_core_symbols/properties/ConfigName.meta.json`
  - `05_pywin32_bridge/plot_layout_rules.md`
  - `07_validation/usage_feedback.jsonl`
- 关联任务：
  - `read_layout_plot_info`
  - `execute_layout_plot`
  - `build_print_plan_and_info`
- 影响项目路径：
  - `cad/scripts/CAD_basic.py`
  - `cad/scripts/drawing_basic_service/print/print_executor.py`
  - `cad/scripts/drawing_basic_service/print/print_info_analysis.py`

### CanonicalMediaName

- 原等级：`06_on_demand_index` 低频索引
- 晋升原因：纸张介质名与设备绑定，直接影响布局输出页面尺寸和打印结果正确性
- 补齐文件：
  - `03_core_symbols/properties/CanonicalMediaName.md`
  - `03_core_symbols/properties/CanonicalMediaName.meta.json`
  - `05_pywin32_bridge/plot_layout_rules.md`
  - `07_validation/usage_feedback.jsonl`
- 关联任务：
  - `read_layout_plot_info`
  - `execute_layout_plot`
  - `build_print_plan_and_info`
- 影响项目路径：
  - `cad/scripts/CAD_basic.py`
  - `cad/scripts/drawing_basic_service/print/print_executor.py`
  - `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
