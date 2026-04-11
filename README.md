# codex-tasks

本目录是 `DWG / CAD` 自动化项目的项目总管工作区。

如果当前任务是专门处理本项目，推荐直接进入：

- `D:\codex-tasks`

再运行 `codex / gpt-5.4`。

这样做的原因是：

- 项目级知识已经开始沉淀在本目录内
- 多智能体协作层也在本目录内
- 各领域执行工作区也在本目录内
- 有利于后续持续积累，而不是把经验散落到用户主目录

## 当前治理结构

当前项目采用：

- 项目总管
- 角色能力层
- 领域执行层
- 运行监督链

其中：

- 项目总管工作区：
  `D:\codex-tasks`
- 角色能力层：
  `D:\codex-tasks\dwg_agents_ops`
- 当前最重要的领域执行工作区：
  `D:\codex-tasks\cad\scripts\drawing_basic_service\print`
- 当前监督链核心：
  `D:\codex-tasks\cad\system\cad_runtime_guard.py`
  与
  `D:\codex-tasks\dwg_agents_ops\Runtime_Guard_Agent`

## 当前四角色

当前四角色能力层为：

- `Planner_Agent`
- `Coder_Agent`
- `Reviewer_Agent`
- `Tester_Agent`

它们由项目总管调度，而不是独立接管项目。

## 当前最重要的执行工作区

当前第一优先级的领域执行工作区是：

- 打印执行工作区

工作根目录：

- `D:\codex-tasks\cad\scripts\drawing_basic_service\print`

其当前目标不是抽象研究，而是：

- 掌握项目级基础知识
- 掌握打印专业知识
- 根据任务要求完成高质量打印
- 持续沉淀并扩展打印执行体系

## 进入项目后先看什么

1. `folder.meta.json`
2. `thoughtway/PROJECT_SUPERVISOR_ARCHITECTURE.md`
3. `thoughtway/CURRENT_STATE.md`
4. `thoughtway/TERMINOLOGY.md`
5. `AGENTS.md`
6. `thoughtway/PROJECT_GOVERNANCE.md`
7. `thoughtway/SYSTEM_FOUNDATIONS.md`
8. `thoughtway/PROJECT_MEMORY_SYSTEM.md`
9. `dwg_agents_ops/README.md`
10. `dwg_agents_ops/agent_control/UNIFIED_CONTROL.md`
11. `dwg_agents_ops/agent_control/RUNTIME_EVENT_PROTOCOL.md`
12. `cad/scripts/drawing_basic_service/print/README.md`
13. `cad/scripts/drawing_basic_service/print/PRINT_AGENT_SPEC.md`

## 当前一句话共识

`C:\Users\User` 下的 Codex 仍是跨项目通用总管，  
但 `D:\codex-tasks` 已经被正式建设为本项目的项目总管工作区。

## GitHub 版本说明

- GitHub 上提交 `baee4bb`（`Add print orchestration and runtime guard framework`）是一个明确的监督版基线。
- 这里的“监督版”是指：打印执行链已接入 `cad_runtime_guard.py` 与对应的 runtime guard orchestration，用于复杂批量打印任务的运行时监督与稳定性增强。
- GitHub 标签：
  - `print-supervised-runtime-guard-20260321`
    对应带运行监督链 / runtime guard 的监督版基线。
  - `print-unsupervised-plain-guard-20260321`
    对应移除 runtime guard 监督链、回到朴素守护后的无监督对比版快照。
  - `project-governor-doc-outline-20260411`
    对应本轮小步增量版本：补入 `cad/official_development_document/` 官方开发文档，并新增总图轮廓绘制工作区 `cad/scripts/Scheme_drawing/`。
- 若后续本地实验回退到“无监督、朴素守护”状态，不应反向覆盖监督版说明；应通过新的提交或标签单独标注“朴素版”或“对比实验版”。
