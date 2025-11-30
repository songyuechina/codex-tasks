cmd /c "cd /d D:\codex-tasks\cad\scripts && python -m fire cad_excel_fire read_xlsx_to_dict \"..\Functional_control\Functions_ CAD_basic\excel_dict_conversion\samples\sample_project.xlsx\""
python tests\read_dict_demo.py "..\samples\sample_project.xlsx" tests\outputs\sample_project.json
python tests\read_dict_demo.py "..\samples\project_template.xlsx" tests\outputs\template_check.json

# read_xlsx_to_dict 专属资料夹

- **功能**：从带有标准表头的 Excel 中解析项目总体信息与图纸列表，输出统一字典结构（project + drawings）。
- **脚本位置**：`cad/scripts/CAD_basic.py`
- **测试资产**：
  - 模板：`..\samples\project_template.xlsx`
  - 带数据样例：`..\samples\sample_project.xlsx`
  - 生成脚本：`..\create_sample_workbooks.py`
- **命令流程**：
  1. （如需重置样例）`python ..\create_sample_workbooks.py`
  2. 运行上方命令获取 JSON，脚本会在内部执行 `cad_zt_oneb()` → `litz()` → `read_xlsx_to_dict()` → `cad_zt_oneb()`。
  3. 输出 JSON 位于 `tests\outputs\*.json`，可直接供写回函数或人工查验字段。
- **最新测试**（2025-11-29 12:20）：
  - `sample_project.xlsx` → 2 条 drawings，project["项目名称"]="未来城住宅一期"
  - `project_template.xlsx` → drawings 为空；project 字段为空值
- **日志**：详见 `tests/test_log.txt`
