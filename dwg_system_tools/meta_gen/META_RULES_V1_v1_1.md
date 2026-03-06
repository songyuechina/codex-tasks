# META_RULES_V1.1 --- Script → Quote/Procedure Meta 生成规则（修订版）

> 系统根目录：`D:/codex-tasks`\
> 五部分并列：\
> A `cad/`（驱动CAD执行环境脚本）\
> B `dwg_cases/`（DWG案例资产）\
> C `dwg_agents_ops/`（DWG作业智能体）\
> D `dwg_system_tools/`（DWG系统控制工具） E
> `thoughtway/`（思想方法与参考资料）

------------------------------------------------------------------------

# 0. 任务目标

对重要脚本 `A.py` 生成：

-   `A_quote.meta.json`
-   `A_procedure.meta.json`

核心思想：

-   引用层 = 骨架（结构、API、Return分支、依赖）\
-   流程层 = 行为与资源边界\
-   return 分支必须标注条件\
-   禁止编造语义\
-   强调副作用与运行环境假设

------------------------------------------------------------------------

# 0.1 覆盖策略（新增）

## L3（必须生成 Quote + Procedure）

-   对外入口脚本
-   涉及 CAD/COM 操作
-   涉及数据库读写
-   会打开/关闭文件
-   被多个模块调用

## L2（建议生成 Quote，Procedure 可选）

-   中等复杂工具脚本
-   存在副作用但风险较低

## L1（可不生成或生成简版 Quote）

-   纯常量文件
-   一次性迁移脚本
-   私有 helper 且无独立调用意义

⚠ 不追求 100% 覆盖率，优先覆盖 L3。

------------------------------------------------------------------------

# 1. 输出位置与命名

默认目录：

    D:/codex-tasks/dwg_system_tools/_generated_meta/

命名规则：

    A_quote.meta.json
    A_procedure.meta.json

------------------------------------------------------------------------

# 2. 生成流程

## Phase 0（L2/L3 必须）

抽取：

-   imports
-   globals
-   signatures
-   returns
-   行号（必须真实来源）
-   docstring
-   section 分块

若无法可靠获取行号：

    line_start = -1
    line_end   = -1

并写入 quality.todo。

## Phase 1

补齐：

-   goal
-   description
-   branch_logic
-   usage
-   workflow
-   side_effects
-   runtime_assumptions

------------------------------------------------------------------------

# 3. 共同字段

``` json
{
  "meta_version": "1.1",
  "script": {
    "name": "A.py",
    "path": "cad/xxx/A.py",
    "encoding": "utf-8",
    "version": ""
  }
}
```

------------------------------------------------------------------------

# 4. Quote Meta 结构（修订）

新增字段：

-   side_effects
-   runtime_assumptions

``` json
{
  "meta_version": "1.1",
  "script": { ... },
  "quote": {
    "goal": "...",
    "sections": [],
    "public_api": [],
    "notes": [],
    "side_effects": {
      "cad": [],
      "db": [],
      "files": [],
      "network": []
    },
    "runtime_assumptions": [],
    "confidence": {
      "goal": "high|medium|low"
    }
  },
  "functions": [],
  "dependencies": {
    "imports": [],
    "globals": [],
    "files_guess": []
  },
  "quality": {
    "todo": [],
    "function_count": 0
  }
}
```

------------------------------------------------------------------------

# 5. Return 分支规则（强化）

必须包含：

-   guard return
-   多分支 return
-   except return
-   implicit return

Condition 抽取规则：

  结构         condition
  ------------ ----------------------
  if           表达式
  else         NOT(表达式)
  except X     exception:X
  implicit     otherwise
  复杂控制流   complex_control_flow

复杂控制流：

    condition = "complex_control_flow"
    confidence = "low"

------------------------------------------------------------------------

# 6. 副作用与资源边界（新增）

若函数：

-   打开文件
-   关闭文件
-   写数据库
-   修改实体
-   切换布局
-   改系统变量

必须在：

-   quote.side_effects
-   procedure.workflow

明确标出。

------------------------------------------------------------------------

# 7. Procedure Meta 结构（修订）

``` json
{
  "meta_version": "1.1",
  "script": { ... },
  "procedure": {
    "usage": "...",
    "examples": [],
    "workflow": []
  },
  "functions": [],
  "quality": {
    "todo": [],
    "function_count": 0
  }
}
```

新增规则：

-   必须包含 script-level workflow
-   public_api 函数必须有 steps 或写 todo

------------------------------------------------------------------------

# 8. Evidence 强制规则

以下必须有 evidence：

-   return 分支
-   函数对象
-   推断 goal
-   推断 description
-   推断 steps

格式：

``` json
"evidence": {
  "line_start": 10,
  "line_end": 30
}
```

禁止随意填写行号。

------------------------------------------------------------------------

# 9. 禁止事项

-   编造 description
-   编造 return 条件
-   无 evidence 的 return
-   隐瞒副作用
-   忽略 todo

------------------------------------------------------------------------

# 10. 修订目标

本版本（V1.1）目标：

-   降低维护成本
-   强化副作用表达
-   强化资源边界安全
-   防止 meta 过期误导智能体
-   保持与原 V1 结构兼容

------------------------------------------------------------------------

**End of META_RULES_V1.1**
