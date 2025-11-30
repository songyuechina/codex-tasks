cd /d D:\codex-tasks\cad\scripts && python -m fire cad_excel_fire write_dict_to_xlsx "..\Functional_control\Functions_ CAD_basic\excel_dict_conversion\samples\sample_project_data.json" "..\Functional_control\Functions_ CAD_basic\excel_dict_conversion\samples\project_template.xlsx" "..\Functional_control\Functions_ CAD_basic\excel_dict_conversion\write_dict_to_xlsx\tests\outputs\fire_sample_out.xlsx"
python tests\write_dict_demo.py "..\samples\project_template.xlsx" "..\samples\sample_project_data.json" tests\outputs\sample_project_out.xlsx

# write_dict_to_xlsx 专属资料夹

- **功能**：将 `read_xlsx_to_dict` 返回的统一字典写回 Excel 模板，保持表头/格式不变。
- **脚本位置**：`cad/scripts/CAD_basic.py`
- **测试资产**：
  - 模板：`..\samples\project_template.xlsx`
  - JSON：`..\samples\sample_project_data.json`
  - 生成脚本：`..\create_sample_workbooks.py`
- **命令流程**：
  1. （如需重置样例）`python ..\create_sample_workbooks.py`
  2. 运行首行命令，脚本内部执行 `cad_zt_oneb()` → `litz()` → `write_dict_to_xlsx()` → `read_xlsx_to_dict()` → `cad_zt_oneb()`，最后打印写入结果及 drawings 数量。
  3. 输出 DWG?（无）——生成的 Excel 位于 `tests\outputs\sample_project_out.xlsx`，可再次用 read 函数验算。
- **最新测试**（2025-11-29 12:22）：
  - 输出文件包含 2 条 drawings，项目名称“未来城住宅一期”。
- **日志**：详见 `tests/test_log.txt`
