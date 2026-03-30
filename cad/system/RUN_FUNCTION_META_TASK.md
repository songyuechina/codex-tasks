# RUN_FUNCTION_META_TASK.md

适用对象：Codex / 命令行智能体  
任务类型：为 `cad/system` 的正式脚本生成**函数级 meta.json**

---

# 0. 任务总目标

你需要在本地项目：

`D:/codex-tasks`

中工作，并完成：

`D:/codex-tasks/cad/system`

目录下 10 个正式脚本的**函数级 meta 生成任务**。

本任务只要求生成函数级两份文件：

- `A_functions.quote.meta.json`
- `A_functions.procedure.meta.json`

目标不是追求每个函数说明都极其完美，而是：

- 不漏掉脚本中的函数
- 为每个函数建立整体概括层
- 简单函数简写
- 复杂函数适度展开
- 允许局部不精确
- 整体完成优先于局部完美

---

# 1. 必读文件

开始前必须阅读以下文件，并严格遵守：

- `D:/codex-tasks/AGENTS.md`
- `D:/codex-tasks/cad/system/AGENTS.md`
- `D:/codex-tasks/cad/system/README.md`
- `D:/codex-tasks/dwg_system_tools/meta_gen/META_RULES.md`
- `D:/codex-tasks/dwg_system_tools/meta_gen/TASK_TEMPLATE_PLAIN.md`

如果 `META_RULES.md` 与旧记忆冲突，以当前文件内容为准。

---

# 2. 需要处理的 10 个脚本

你必须处理以下 10 个正式脚本：

1. `D:/codex-tasks/cad/system/CAD_com_utils.py`
2. `D:/codex-tasks/cad/system/cad_command_monitor.py`
3. `D:/codex-tasks/cad/system/CAD_coordination.py`
4. `D:/codex-tasks/cad/system/CAD_core.py`
5. `D:/codex-tasks/cad/system/cad_dialog_killer.py`
6. `D:/codex-tasks/cad/system/CAD_selection.py`
7. `D:/codex-tasks/cad/system/common_logger.py`
8. `D:/codex-tasks/cad/system/content_analysis_dwg_file.py`
9. `D:/codex-tasks/cad/system/licad.py`
10. `D:/codex-tasks/cad/system/project_setup.py`

---

# 3. 输出文件要求

对每个脚本 `A.py`，在**同目录**生成以下两份文件：

- `A_functions.quote.meta.json`
- `A_functions.procedure.meta.json`

例如：

- `D:/codex-tasks/cad/system/common_logger_functions.quote.meta.json`
- `D:/codex-tasks/cad/system/common_logger_functions.procedure.meta.json`

---

# 4. 覆盖要求（硬要求）

## 4.1 必须尽量覆盖脚本中的全部函数

不要只写 `public_api`。  
必须尽量覆盖该脚本中**可以静态识别到的全部函数**，包括：

- public_api
- 内部函数
- helper
- 小工具函数
- 类方法（如当前结构允许，应一并纳入）

核心要求：

> 不要漏掉脚本中的每个函数。

## 4.2 不要求每个函数都写得一样深

允许按复杂度分级：

- `core`
- `normal`
- `utility`

## 4.3 简单函数不需要太多内容

简单函数只要尽量具备：

- 函数名
- 签名
- 功能目标
- 输入参数
- 输出/返回
- 简要流程

即可。

## 4.4 复杂函数适度展开

复杂函数尽量补充：

- 返回分支
- 主要步骤
- 失败路径
- 副作用
- 必须保留的经验

---

# 5. 最重要的工作原则

## 5.1 不要追求绝对完美

这些 functions meta 文件的本质用途是：

- 给智能体建立函数级概括层
- 便于后续快速引用
- 便于快速理解与重构
- 便于快速定位

因此：

- 允许局部不准确
- 允许局部粗糙
- 允许某些判断不够精密
- 不要因为少量不确定而卡住整个任务

## 5.2 允许你自主综合判断

当某些函数存在：

- 动态行为较强
- 包装层较多
- alias / monkey patch
- 返回条件难完全拆清
- 输入输出边界不绝对清楚

你不需要无限纠结。  
请结合源码上下文自行做一个**整体上最合理、最有用**的概括。

## 5.3 不确定时写 todo，而不是停工

遇到以下情况时：

- 行号难确认
- 语义局部模糊
- 方法归属难整理
- 返回分支过复杂
- 某些 steps 只能推断

允许：

- 先生成一个可用概括
- 再把不确定点记入 `quality.todo`

## 5.4 重点是整体可用，而不是局部绝对正确

完成标准首先看：

1. 全部脚本都处理了
2. 函数尽量全覆盖了
3. 每个函数都有基本概括
4. 复杂函数有适度展开
5. todo 承接了不确定部分

---

# 6. functions.quote 的生成要求

对每个函数，尽量提供这些字段：

- `name`
- `level`
- `signature`
- `purpose`
- `inputs`
- `outputs`
- `returns`
- `side_effects`
- `dependencies`
- `risk_level`
- `evidence`

但是允许按复杂度简化。

## 6.1 utility 函数最小要求

至少尽量给出：

- `name`
- `level`
- `signature`
- `purpose`
- `inputs`
- `outputs`
- `evidence`

## 6.2 normal 函数建议

尽量给出：

- `name`
- `level`
- `signature`
- `purpose`
- `inputs`
- `outputs`
- `returns`
- `evidence`

## 6.3 core 函数应尽量完整

尽量给出：

- `name`
- `level`
- `signature`
- `purpose`
- `inputs`
- `outputs`
- `returns`
- `side_effects`
- `dependencies`
- `risk_level`
- `evidence`

---

# 7. functions.procedure 的生成要求

对每个函数，尽量提供这些字段：

- `name`
- `level`
- `role`
- `preconditions`
- `steps`
- `failure_paths`
- `success_conditions`
- `must_keep_experience`
- `brief_flow`
- `evidence`

允许按复杂度简化。

## 7.1 utility 函数

可以只写：

- `name`
- `level`
- `brief_flow`
- `evidence`

## 7.2 normal 函数

建议写：

- `name`
- `level`
- `steps`
- `failure_paths`
- `evidence`

## 7.3 core 函数

尽量写：

- `name`
- `level`
- `role`
- `preconditions`
- `steps`
- `failure_paths`
- `success_conditions`
- `must_keep_experience`
- `evidence`

---

# 8. 输入、输出、返回值的处理要求

## 8.1 输入参数

必须尽量从以下来源提取：

- 函数签名
- 默认值
- 注释
- docstring
- 实现逻辑

## 8.2 输出

输出不只是 `return`。  
还包括：

- 写文件
- 写数据库
- 改变 CAD 当前状态
- 修改对象
- 其它重要外部效果

## 8.3 返回值

不必对每个函数都做极细致的控制流拆解。  
但至少要尽量概括：

- 成功返回
- 失败返回
- guard return
- implicit return

如果太复杂，可以简化，并把问题写入 todo。

---

# 9. 类与方法的处理

若脚本中存在 `class`：

- 优先把方法也纳入 `functions` 覆盖范围
- 方法名可写成：
  - `ClassName.method_name`
  或
  - `method_name`（但要在说明中体现归属）
- 如果当前结构不方便完整表达类层级，也不要漏掉方法
- 若确实难处理，至少写入 `quality.todo`

---

# 10. evidence 与行号策略

- 尽量给函数整体范围的 `line_start / line_end`
- 不要求极致精准
- 如果无法可靠确认：
  - `line_start = -1`
  - `line_end = -1`
  - 并写入 `quality.todo`

不要为了形式完整而编造行号。

---

# 11. 具体执行步骤

请按以下顺序工作：

## Step 1
阅读规则文件与 README / AGENTS。

## Step 2
逐个读取这 10 个脚本源码。

## Step 3
列出每个脚本的全部函数清单。

## Step 4
为每个脚本生成：

- `*_functions.quote.meta.json`
- `*_functions.procedure.meta.json`

## Step 5
将结果直接写回脚本同目录。

## Step 6
如有必要，使用以下工具做校验：

- `D:/codex-tasks/dwg_system_tools/meta_gen/meta_validator.py`
- `D:/codex-tasks/dwg_system_tools/meta_gen/meta_pipeline.py`

但不要因为校验细节问题阻塞整体任务推进。

---

# 12. 完成标准

任务完成的标准不是“每个字段都完美”，而是：

1. 10 个脚本都处理完
2. 每个脚本都生成两份函数级 meta
3. 每个脚本的函数尽量全覆盖
4. 简单函数已简要概括
5. 复杂函数已适度展开
6. 不确定处通过 todo 处理，而不是停工

---

# 13. 交付要求

全部完成后，请汇报：

1. 生成的全部文件路径
2. 每个脚本的函数总数
3. 每个脚本中 `core / normal / utility` 数量
4. 最重要的 todo 项
5. 哪些脚本最需要后续人工复核

---

# 14. 最关键的一句话

> 你的任务不是完美分析每个函数，而是把每个函数都纳入可用的函数级概括层：不要漏函数，简单函数简写，复杂函数适度展开，整体完成优先于局部完美。
