# TASK_TEMPLATE — 生成 Script Quote/Procedure Meta 任务模板

## 0) 必读规则

在开始前必须阅读：

D:/codex-tasks/dwg_system_tools/meta_gen/META_RULES_V1.md

必须严格按照规则生成 JSON 文件。

---

## 1) 任务输入（只修改此部分）

- SCRIPT_PATH: <D:/codex-tasks/cad/system/common_logger.py>
- STEM: <common_logger>

示例：

SCRIPT_PATH = D:/codex-tasks/cad/system/common_logger.py  
STEM = common_logger

---

## 2) 任务目标

生成以下两个文件：

- D:/codex-tasks/dwg_system_tools/_generated_meta/<STEM>_quote.meta.json  
- D:/codex-tasks/dwg_system_tools/_generated_meta/<STEM>_procedure.meta.json

---

## 3) 必做检查项

1. 每个 return 分支必须包含：
   - id
   - condition
   - value_repr
   - branch_logic
   - evidence
   - confidence

2. 所有推断内容必须附带 evidence 行号。

3. 简单函数 steps 允许为空。

4. 复杂函数若 steps 为空，必须写入 quality.todo。

---

## 3.5 关键函数（本任务优先核对）

- KEY_FUNC_1: <setup_logger>
- KEY_FUNC_2: <record_test_result>
- KEY_FUNC_3: <set_debug_mode>

示例：

- KEY_FUNC_1: setup_logger  
- KEY_FUNC_2: record_test_result  
- KEY_FUNC_3: set_debug_mode  

---

## 4) 交付说明（必须写在回复中）

- 生成的两个文件路径
- quality.todo 中最重要的三条
- 最需要人工确认的 return 分支
