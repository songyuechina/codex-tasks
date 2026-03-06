# META_RULES_V1.2 --- Script → Quote/Procedure Meta 生成规则（简化版）

> 目标：让智能体 **快速使用脚本
> public_api**，并在必要时能基于"流程骨架"独立重构关键函数。\
> 原则：**少而准**，避免为分析而分析；meta
> 追求"可用性与可维护性"，不追求覆盖全部细节。

系统根目录：`D:/codex-tasks`

------------------------------------------------------------------------

# 0. 任务目标

对重要脚本 `A.py` 生成：

-   `A_quote.meta.json`
-   `A_procedure.meta.json`

核心思想：

-   Quote（引用层）= **能立刻调用**（目标、入口、返回结构、关键约束）
-   Procedure（流程层）= **能复刻骨架**（入口函数工作流 + 资源边界）
-   禁止编造语义；不确定就写 todo（允许 low confidence）
-   Evidence 必须存在，但 **允许粗粒度证据**（指向函数整体范围）

------------------------------------------------------------------------

# 0.1 覆盖策略（保持）

## L3（必须生成 Quote + Procedure）

-   对外入口脚本 / 服务脚本（被多个模块调用）
-   CAD/COM 强耦合或高风险
-   DB/文件写入或可能改变状态

## L2（建议生成 Quote；Procedure 可选）

-   中等复杂工具脚本
-   有副作用但风险较低

## L1（可不生成或仅简版 Quote）

-   私有 helper、短脚本、一次性迁移脚本

⚠ 不追求 100% 覆盖率，优先覆盖 L3。

------------------------------------------------------------------------

# 1. 输出位置与命名（更新：与脚本同目录）

对脚本 `A.py`，meta 与其放在同目录：

-   `A_quote.meta.json`
-   `A_procedure.meta.json`

示例：

    cad/system/common_logger.py
    cad/system/common_logger_quote.meta.json
    cad/system/common_logger_procedure.meta.json

------------------------------------------------------------------------

# 2. 生成流程（简化）

## Phase 0（L2/L3 建议执行；L3 尽量执行）

抽取：

-   imports（依赖）
-   globals（关键全局）
-   public_api（入口函数）
-   signatures（入口函数签名）
-   returns（入口函数是否有 early return / 异常 return）
-   sections（段落粗分）
-   行号（可粗定位到函数整体范围即可）

若无法可靠获取行号：

    line_start = -1
    line_end   = -1

并写入 quality.todo。

## Phase 1（生成 meta）

补齐：

-   quote.goal（1\~2 句）
-   quote.public_api（必须准确）
-   函数 description（只写"能用"的信息）
-   return 分支（只对 public_api 必须）
-   procedure.workflow（script-level）
-   procedure.functions.steps（只对 public_api 必须）

------------------------------------------------------------------------

# 3. 共同字段（保持）

``` json
{
  "meta_version": "1.0",
  "script": {
    "name": "A.py",
    "path": "cad/xxx/A.py",
    "encoding": "utf-8",
    "version": ""
  }
}
```

-   script.path 必须为相对 `D:/codex-tasks` 路径
-   encoding 优先读取 `# -*- coding: utf-8 -*-`，否则 `"utf-8"`
-   version 可为空字符串

------------------------------------------------------------------------

# 4. Quote Meta 结构（保持 V1 兼容）

``` json
{
  "meta_version": "1.0",
  "script": { ... },
  "quote": {
    "goal": "...",
    "sections": [],
    "public_api": [],
    "notes": [],
    "confidence": { "goal": "high|medium|low" }
  },
  "functions": [],
  "dependencies": { "imports": [], "globals": [], "files_guess": [] },
  "quality": { "todo": [], "function_count": 0 }
}
```

## 4.1 Quote 的最小有效信息（硬要求）

-   goal（1\~2句）
-   public_api（入口函数名列表）
-   每个 public_api 在 functions\[\] 有一条记录（见下）
-   notes 至少包含：
    -   副作用/约束（是否打开/关闭文件、写DB、依赖当前文档、是否切布局/口径）

------------------------------------------------------------------------

# 5. functions\[\]（引用层）简化规则（核心改动）

## 5.1 只覆盖 public_api（硬规则）

functions\[\] 必须包含：**quote.public_api 中的每个函数**。

除 public_api 外： - 默认不写入 functions\[\] -
只有"关键内部函数（critical helper）"才允许加入，且 **最多 3 个** - 其余
helper 只在 quote.notes 提一句即可

## 5.2 函数结构（保持）

``` json
{
  "name": "func",
  "signature": "def func(x=1):",
  "inputs": [],
  "outputs": [],
  "returns": [],
  "description": "...",
  "evidence": { "line_start": 1, "line_end": 80 },
  "confidence": { "description": "high", "returns": "high" }
}
```

------------------------------------------------------------------------

# 6. Return 分支规则（降级但保底）

## 6.1 public_api 必须写 returns\[\]（硬规则）

必须生成 returns\[\] 的情况： - 多个 return - guard return（早退） -
except return（异常分支） - implicit return（无显式 return 的
otherwise）

## 6.2 允许"二分法"返回（推荐）

对多数脚本，仅需： - return_success - return_error

复杂控制流：

    condition = "complex_control_flow"
    confidence = "low"

并写入 todo；不要求当场拆尽所有条件。

------------------------------------------------------------------------

# 7. Procedure Meta 结构（保持 V1 兼容）

``` json
{
  "meta_version": "1.0",
  "script": { ... },
  "procedure": {
    "usage": "...",
    "examples": [],
    "workflow": []
  },
  "functions": [],
  "quality": { "todo": [], "function_count": 0 }
}
```

## 7.1 Procedure 的最小有效信息（硬要求）

-   procedure.workflow：必须包含 **script-level workflow**（3\~8
    行即可）
-   procedure.functions：只要求覆盖 public_api
-   public_api 的 steps：必须提供"骨架步骤"（4\~10 步），强调资源边界

------------------------------------------------------------------------

# 8. Steps 规则（简化）

## 简单函数

-   steps = \[\]
-   confidence.steps = "n/a"

## 复杂函数（只强制 public_api）

-   steps 只写"骨架"：连接/读取/扫描/写入/关闭/返回
-   无法可靠生成 → 留空 steps + 写 todo（不要硬编）

------------------------------------------------------------------------

# 9. Evidence 规则（放宽）

必须包含 evidence 的对象： - public_api 函数对象（function.evidence） -
public_api returns 分支（return.evidence） - 推断 goal / usage /
workflow（可指向"入口函数整体范围"）

允许证据粗粒度： - 对函数：evidence 覆盖整个 def 块即可 - 对
returns：evidence 覆盖 return 附近 5\~15 行即可

禁止随意填写行号；无法确定则 -1/-1 并写 todo。

------------------------------------------------------------------------

# 10. quality.todo（保留，作为"不确定性出口"）

必须记录： - 行号缺失 - complex_control_flow 未拆解 - 缺失 docstring
导致 description/steps 需要推断 - public_api steps 缺失

示例： -
`function:get_cad_state: complex_control_flow return; verify conditions` -
`script:content_analysis_dwg_file: line numbers not verified; run Phase 0 extractor`

------------------------------------------------------------------------

# 11. 禁止事项（保持）

-   编造 description
-   编造 condition
-   无 evidence 的 return（public_api）
-   忽略 todo

------------------------------------------------------------------------

# 12. 评判标准（新）

一个 meta 是否合格，只看三条： 1) 不看源码也能正确调用
public_api（参数/返回结构/副作用清楚） 2)
不会踩关键坑（CAD连接、布局口径、DB复用、文件打开关闭） 3) 必要时能按
procedure.steps 复刻入口函数骨架（不要求复刻所有 helper）

------------------------------------------------------------------------

**End of META_RULES_V1.2**
