# META_RULES.md

版本：V2.0  
适用目录：`D:/codex-tasks/dwg_system_tools/meta_gen`

---

# 1. 核心目标

把脚本信息分成 **四层**，而不是只做两层：

1. 脚本级引用层  
   - `A_quote.meta.json`

2. 脚本级流程层  
   - `A_procedure.meta.json`

3. 函数级引用层  
   - `A_functions.quote.meta.json`

4. 函数级流程层  
   - `A_functions.procedure.meta.json`

目的：

- 让智能体先快速理解脚本骨架
- 再进入每个函数的完整控制信息
- 避免“脚本级 meta 太大”与“函数级信息缺失”这两个极端

---

# 2. 根本原则

## 2.1 脚本级 meta 的任务
脚本级 meta 不负责展开每个函数的全部细节。  
它负责：

- 脚本角色
- 公共入口
- 整体流程
- 关键依赖
- 不可丢失经验

## 2.2 函数级 meta 的任务
函数级 meta 负责覆盖 **脚本中的全部函数**，并为每个函数提供结构化信息。

## 2.3 不允许再把“所有函数信息”强塞进脚本级 quote/procedure
否则会导致：

- 脚本级骨架失去压缩作用
- 文件过大
- 智能体失去快速抓总览的能力

---

# 3. 输出位置与命名

对脚本 `A.py`，四份 meta 与其放在同目录：

- `A_quote.meta.json`
- `A_procedure.meta.json`
- `A_functions.quote.meta.json`
- `A_functions.procedure.meta.json`

示例：

```text
cad/system/common_logger.py
cad/system/common_logger_quote.meta.json
cad/system/common_logger_procedure.meta.json
cad/system/common_logger_functions.quote.meta.json
cad/system/common_logger_functions.procedure.meta.json
```

---

# 4. 覆盖策略

## 4.1 脚本级 meta
只要求覆盖：

- 脚本目标
- script-level workflow
- public_api
- 关键边界与副作用

## 4.2 函数级 meta
必须覆盖 **脚本中的全部函数**，包括：

- public_api
- 关键内部函数
- 一般内部函数
- 小工具函数

但允许 **分级详略**。

---

# 5. 函数分级规则（非常重要）

函数级 meta 必须给每个函数分级：

- `core`
- `normal`
- `utility`

## 5.1 core
适用于：
- public_api
- 高风险函数
- 写文件 / 写库 / 控制 CAD / 切空间 / 发命令 / 建连接
- 被多个模块依赖的核心函数

必须写完整信息：

### 在 functions.quote 中
- name
- signature
- purpose
- inputs
- outputs
- returns
- side_effects
- dependencies
- risk_level
- evidence

### 在 functions.procedure 中
- name
- role
- preconditions
- steps
- failure_paths
- success_conditions
- must_keep_experience
- evidence

## 5.2 normal
适用于：
- 一般内部函数
- 逻辑明显、风险中等的辅助函数

精简要求：

### functions.quote
- name
- signature
- purpose
- inputs
- outputs
- returns（可简化）
- evidence

### functions.procedure
- name
- steps（3~6 步）
- failure_paths（可简）
- evidence

## 5.3 utility
适用于：
- 小工具函数
- 纯转换函数
- 纯格式化函数
- 无明显副作用的简短 helper

最小要求：

### functions.quote
- name
- signature
- purpose
- inputs
- outputs
- evidence

### functions.procedure
- name
- brief_flow
- evidence

---

# 6. 脚本级 quote 规则

脚本级 `A_quote.meta.json` 只应回答：

- 这个脚本在系统中是什么角色
- 主要 public_api 是什么
- 与谁协作
- 有哪些高风险边界
- 哪些经验不能丢

## 硬要求
- `quote.goal`
- `quote.public_api`
- `functions[]` 至少覆盖全部 public_api
- `quality.function_count` 记录脚本总函数数
- `quality.public_api_count` 记录 public_api 数量
- notes 中明确副作用与约束

---

# 7. 脚本级 procedure 规则

脚本级 `A_procedure.meta.json` 只应回答：

- 脚本整体 workflow
- 典型使用方式
- 公共入口大流程
- 资源边界

## 硬要求
- `procedure.workflow`
- `functions[]` 至少覆盖全部 public_api
- public_api 的 steps 应提供骨架步骤

---

# 8. 函数级 quote 结构

推荐结构：

```json
{
  "meta_version": "2.0",
  "meta_scope": "functions",
  "script": { ... },
  "functions_quote": {
    "goal": "...",
    "coverage": "graded-all",
    "grading": {
      "core": "...",
      "normal": "...",
      "utility": "..."
    }
  },
  "functions": [
    {
      "name": "func_a",
      "level": "core",
      "signature": "def func_a(x, y=1):",
      "purpose": "...",
      "inputs": [],
      "outputs": [],
      "returns": [],
      "side_effects": [],
      "dependencies": [],
      "risk_level": "high|medium|low",
      "evidence": { "line_start": 10, "line_end": 80 }
    }
  ],
  "quality": {
    "todo": [],
    "function_count": 0
  }
}
```

---

# 9. 函数级 procedure 结构

推荐结构：

```json
{
  "meta_version": "2.0",
  "meta_scope": "functions",
  "script": { ... },
  "functions_procedure": {
    "goal": "...",
    "step_style": "graded"
  },
  "functions": [
    {
      "name": "func_a",
      "level": "core",
      "role": "...",
      "preconditions": [],
      "steps": [],
      "failure_paths": [],
      "success_conditions": [],
      "must_keep_experience": [],
      "brief_flow": [],
      "evidence": { "line_start": 10, "line_end": 80 }
    }
  ],
  "quality": {
    "todo": [],
    "function_count": 0
  }
}
```

说明：
- `core` / `normal` 用 `steps`
- `utility` 可只写 `brief_flow`
- 不要为了凑齐字段而编造复杂步骤

---

# 10. inputs / outputs / returns 规则

## 10.1 inputs
必须尽量从函数签名、默认值、注释、实现中提取：

- 参数名
- 是否可选
- 典型类型
- 含义
- 特殊约束

## 10.2 outputs
不是指所有内部中间值，而是函数对外输出的结构：

- 返回值
- 修改对象
- 写文件
- 写数据库
- 改变 CAD 当前状态

## 10.3 returns
对于 `core` 和重要 `normal` 函数，应写清返回分支：

- success
- error
- guard return
- implicit return

允许简化，但禁止完全忽略。

---

# 11. evidence 规则

所有函数记录必须有 evidence。  
优先给函数整体范围：

- `line_start`
- `line_end`

若行号无法可靠确认：

- `-1`
- `-1`

并写入 `quality.todo`。

禁止随意编造行号。

---

# 12. todo 规则

以下情况必须写入 `quality.todo`：

- 行号无法确认
- 返回分支复杂但未完全拆开
- steps 为推断而非直接可见
- 某些输入输出只能低置信度推断
- 存在动态生成函数 / monkey patch / alias 难以静态确认

---

# 13. 禁止事项

- 把脚本级 meta 写成函数说明大全
- 函数级 meta 只写 public_api 而忽略其余函数
- 编造 inputs / outputs / returns / steps
- 没有 evidence 就给出强结论
- 不写 todo 就把不确定内容伪装成确定事实

---

# 14. 合格标准

一个脚本的 meta 体系合格，至少满足：

## 脚本级
- 不看源码也能知道脚本在系统中干什么
- 能知道主要 public_api
- 能知道脚本的大流程和边界

## 函数级
- 每个函数都能被看到
- core 函数能直接支撑调用与重构
- normal 函数能快速理解其逻辑位置
- utility 函数能快速理解其基本作用

---

# 15. 最重要的一句话

> 脚本级 meta 负责“先抓骨架”，函数级 meta 负责“进入每个函数的控制层”。二者不能互相替代。
