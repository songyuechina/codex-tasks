# TASK_TEMPLATE — 生成 Script / Functions Meta 任务模板

## 0) 必读规则

在开始前必须阅读：

- `D:/codex-tasks/dwg_system_tools/meta_gen/META_RULES.md`

必须严格按照规则生成 JSON 文件。

---

## 1) 任务输入（只修改此部分）

- SCRIPT_PATH: <填写完整脚本路径>
- STEM: <脚本名去掉 .py>

示例：

```text
SCRIPT_PATH = D:/codex-tasks/cad/system/common_logger.py
STEM = common_logger
```

---

## 2) 任务目标

为脚本 `A.py` 生成四份文件（与脚本同目录）：

- `<same_dir>/<STEM>_quote.meta.json`
- `<same_dir>/<STEM>_procedure.meta.json`
- `<same_dir>/<STEM>_functions.quote.meta.json`
- `<same_dir>/<STEM>_functions.procedure.meta.json`

说明：

- 前两份是脚本级骨架
- 后两份是函数级全展开
- 函数级必须覆盖脚本中的全部函数
- 但允许分级详略：`core` / `normal` / `utility`

---

## 3) 必做检查项

### 3.1 脚本级
1. `quote.goal` 是否清楚
2. `quote.public_api` 是否准确
3. `procedure.workflow` 是否反映 script-level 工作流
4. 脚本级 `functions[]` 是否至少覆盖所有 public_api

### 3.2 函数级
1. 是否覆盖脚本全部函数
2. 每个函数是否有：
   - `name`
   - `signature`
   - `level`
   - `evidence`
3. `core` 函数是否完整提供输入/输出/返回/步骤/失败路径
4. `utility` 函数是否至少提供简要作用与流程
5. `quality.function_count` 是否与函数总数一致

### 3.3 不确定性处理
1. 所有推断内容必须附带 evidence
2. 行号无法确认时必须写 `-1/-1`
3. 复杂返回分支未拆清时必须写入 `quality.todo`
4. 不允许用编造语义填补空白

---

## 4) 关键函数（本任务优先核对）

- KEY_FUNC_1: <函数名>
- KEY_FUNC_2: <函数名>
- KEY_FUNC_3: <函数名>

示例：

- KEY_FUNC_1: setup_logger
- KEY_FUNC_2: record_test_result
- KEY_FUNC_3: set_debug_mode

---

## 5) 交付说明（必须写在回复中）

必须说明：

1. 生成的四个文件路径
2. `quality.todo` 中最重要的三条
3. 最需要人工确认的函数或返回分支
4. 函数总数 / public_api 数量 / core 函数数量
