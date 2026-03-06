# META_RULES_V1 — Script → Quote/Procedure Meta 生成规则（/codex-tasks）

> 系统根目录：`D:/codex-tasks`  
> 五部分并列：  
> A `cad/`（驱动CAD执行环境脚本）  
> B `dwg_cases/`（DWG案例资产）  
> C `dwg_agents_ops/`（DWG作业智能体）  
> D `dwg_system_tools/`（DWG系统控制工具）
> E `thoughtway/`（整个项目的思想方法和参考资料）
---

# 0. 任务目标

对重要脚本 `A.py` 生成：

- `A_quote.meta.json`
- `A_procedure.meta.json`

核心思想：

- 引用层 = 骨架  
- 流程层 = 深入理解材料  
- return 分支必须标注条件  
- 禁止编造语义  

---

# 1. 输出位置与命名

## 1.1 默认目录

```
D:/codex-tasks/dwg_system_tools/_generated_meta/
```

## 1.2 命名

```
A_quote.meta.json
A_procedure.meta.json
```

示例：

```
common_logger.py
→ common_logger_quote.meta.json
→ common_logger_procedure.meta.json
```

---

# 2. 生成流程

## Phase 0（可选）

抽取：

- imports  
- globals  
- signatures  
- returns  
- 行号  
- docstring  
- sections  

## Phase 1

智能体补齐：

- goal  
- description  
- branch_logic  
- usage  
- steps  

---

# 3. 共同字段

```json
{
  "meta_version": "1.0",
  "script": {
    "name": "A.py",
    "path": "cad/xxx/A.py",
    "encoding": "utf-8",
    "version": "Vx.y"
  }
}
```

---

## 3.1 script.path

必须为相对 `D:/codex-tasks` 路径。

## 3.2 script.encoding

优先读取：

```
# -*- coding: utf-8 -*-
```

否则 `"utf-8"`。

## 3.3 script.version

优先读取：

```
版本: V3.0
```

否则空字符串。

---

# 4. Quote Meta 结构

```json
{
  "meta_version": "1.0",
  "script": { ... },
  "quote": {
    "goal": "...",
    "sections": [
      { "title": "...", "line_start": 1, "line_end": 120 }
    ],
    "public_api": ["..."],
    "notes": [],
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

---

# 5. 函数结构（引用层）

```json
{
  "name": "func",
  "signature": "def func(x=1):",
  "inputs": [],
  "outputs": [
    "return1: ...",
    "return2: ..."
  ],
  "returns": [
    {
      "id": "return1",
      "condition": "...",
      "value_repr": "...",
      "branch_logic": "...",
      "evidence": {
        "line_start": 10,
        "line_end": 10
      },
      "confidence": "high"
    }
  ],
  "description": "...",
  "evidence": {
    "line_start": 1,
    "line_end": 80
  },
  "confidence": {
    "description": "high",
    "returns": "high"
  }
}
```

---

# 6. 多分支 Return 规则

必须生成 returns[] 的情况：

- 多个 return  
- guard return  
- implicit return  

## 6.1 Condition 抽取

| 结构 | condition |
|------|-----------|
| if | 条件表达式 |
| else | NOT(条件) |
| except X | exception:X |
| implicit | otherwise |

## 6.2 复杂控制流

```
condition = "complex_control_flow"
confidence = "low"
```

并写入 todo。

---

# 7. Procedure Meta 结构

```json
{
  "meta_version": "1.0",
  "script": { ... },
  "procedure": {
    "usage": "...",
    "examples": [],
    "workflow": []
  },
  "functions": [
    {
      "name": "...",
      "is_simple": true,
      "steps": [],
      "confidence": {
        "steps": "n/a"
      },
      "evidence": {
        "line_start": 1,
        "line_end": 20
      }
    }
  ],
  "quality": {
    "todo": [],
    "function_count": 0
  }
}
```

---

# 8. Steps 规则

## 简单函数

```
steps = []
confidence.steps = "n/a"
```

## 复杂函数

- docstring 列表 → 直接提取  
- 或总结步骤 + evidence  
- 无法可靠生成 → 留空 + todo  

---

# 9. Evidence 强制

必须包含 evidence 的对象：

- returns 分支  
- function 对象  
- 推断 goal/description/steps  

格式：

```json
"evidence": {
  "line_start": 10,
  "line_end": 30
}
```

---

# 10. quality.todo

必须记录：

- 缺失 docstring  
- 推断 description  
- complex_control_flow  
- 缺少 steps  

示例：

```
function:setup_logger: complex control flow return, verify condition
```

---

# 11. 禁止事项

- 编造 description  
- 编造 condition  
- 无 evidence 的 return  
- 忽略 todo  
