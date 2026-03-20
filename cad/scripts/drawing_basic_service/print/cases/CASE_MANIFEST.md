# CASE_MANIFEST.md

## 1. 案例角色

本目录案例不是附件仓库，而是：

- 打印主链验证资产
- 辅助分析验证资产
- 权威结果基线索引

## 2. 当前主要案例

### 2.1 混合空间0109

- 路径：
  `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\assets\混合空间0109.dwg`
- 用途：
  基础打印冒烟、混合空间验证。

### 2.2 远程国际建施2021.0903(LT4、LT5楼梯修改)_t7

- 路径：
  `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\assets\远程国际建施2021.0903(LT4、LT5楼梯修改)_t7.dwg`
- 用途：
  复杂打印区域、净化适配、打印信息分析主案例。

### 2.3 农建房施工图【电气】-0930_t6_t3

- 路径：
  `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\assets\农建房施工图【电气】-0930_t6_t3.dwg`
- 用途：
  净化适配异常案例，验证伪极大打印范围收束、单文件同目录交付、WPS 清理与打印信息分析联动。

## 3. 当前权威回归结果

### 3.1 打印模式回归

目录：

- `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\output\mode-regression\远程国际建施2021.0903(LT4、LT5楼梯修改)_t7`

已确认：

- `basic`
  - `20260317-231805`
  - `45/45`
- `adaptive`
  - `20260317-233026`
  - `49/49`
- `purified_adaptive`
  - `20260318-000050`
  - `47/47`

### 3.2 打印信息分析回归

目录：

- `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\output\远程国际建施2021.0903(LT4、LT5楼梯修改)_t7\20260318-print-info-basic`

已确认：

- 基于 `basic` 模式打印区域
- 共 `45` 个打印区域
- `45/45` 已取到图纸名称
- `45/45` 已取到图号
- `0/45` 项目名称
- 同时输出：
  - `print_info_analysis.json`
  - `print_info_dict.json`
  - `print_info_analysis.xlsx`

## 4. 当前治理验证结果

### 4.1 2026-03-18 治理文档回归验证

目录：

- `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\output\governance-validation\远程国际建施2021.0903(LT4、LT5楼梯修改)_t7\20260318-135042`
- `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\output\governance-validation\远程国际建施2021.0903(LT4、LT5楼梯修改)_t7\20260318-print-info-basic`

说明：

- 这是治理文档调整后的验证结果
- 用于证明当前文档体系对应的主链与辅助链仍可运行
- 不是对 `stable` 权威基线的替代声明

本轮验证结论：

- `basic` 打印
  - `45/45` 成功
  - `missing = 0`
  - `zero_size = 0`
  - `page_size_mismatch = 0`
- `basic` 打印信息分析
  - `45/45` 命中内框线
  - `45/45` 命中右下图签块
  - `45/45` 取到 `drawing_title`
  - `45/45` 取到 `drawing_no`
  - `0/45` 取到 `project_name`

### 4.2 当前默认回归清单

后续若要验证打印智能体是否仍符合当前治理体系，优先对本案例执行以下检查：

1. 基本打印回归
   - 入口：`print_runner.py --mode basic`
   - 检查：
     - 是否生成 `print_plan.json`
     - 是否生成 `print_summary.json`
     - 是否 `45/45` 成功
     - 是否无零字节 PDF
2. 基本打印信息分析回归
   - 入口：`print_info_analysis.py --mode basic`
   - 检查：
     - 是否生成 `print_info_analysis.json`
     - 是否生成 `print_info_analysis.xlsx`
     - 是否 `with_title_count = 45`
     - 是否 `with_drawing_no_count = 45`
     - 是否 `with_project_count = 0`
3. 若本轮涉及脚本修补
   - 检查：
     - 是否更新了相关文档
     - 是否更新了对话记录
     - 是否明确说明结果属于 `stable` 还是 `validation`

### 4.3 2026-03-18 异常电气案例验证

目录：

- `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\assets\农建房施工图【电气】pdf`
- `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\assets\农建房施工图【电气】analysis`
- `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\assets\农建房施工图【电气】prosess\20260318-235548`
- `D:\codex-tasks\cad\scripts\drawing_basic_service\print\cases\output\single-dispatch-validation\batch-20260318-235548`

说明：

- 这是新增“伪极大打印范围收束 + 单文件同目录输出”后的验证结果
- 属于 `validation`，用于证明新规则已经闭环可运行

本轮验证结论：

- `purified_adaptive` 最终打印 `9/9`
- `scope_filter.applied = true`
- 选中的伪极大范围句柄：`23DC`
- 最终交付 PDF：`9`
- 最终分析条目：`9`
- `drawing_title = 9`
- `drawing_no = 9`
- `project_name = 0`

## 5. 案例维护规则

新案例进入后，至少要补：

1. 案例路径
2. 案例用途
3. 结果目录
4. 当前权威结果
5. 新案例带来的规则变化
