# codex-tasks

本目录是 `DWG / CAD` 自动化项目的项目总管工作区。

如果当前任务是专门处理本项目，推荐直接进入：

- `D:\codex-tasks`

再运行 `codex / gpt-5.4`。

这样做的原因是：

- 项目级知识已经开始沉淀在本目录内
- 多智能体协作层也在本目录内
- 各领域智能体工作区也在本目录内
- 有利于后续持续积累，而不是把经验散落到用户主目录

## 当前治理结构

当前项目采用：

- 项目总管
- 角色能力层
- 领域执行层

其中：

- 项目总管工作区：
  `D:\codex-tasks`
- 角色能力层：
  `D:\codex-tasks\dwg_agents_ops`
- 当前最重要的领域执行层：
  `D:\codex-tasks\cad\scripts\drawing_basic_service\print`

## 当前四角色

当前四角色能力层为：

- `Planner_Agent`
- `Coder_Agent`
- `Reviewer_Agent`
- `Tester_Agent`

它们由项目总管调度，而不是独立接管项目。

## 当前最重要的领域智能体

当前第一优先级的领域智能体是：

- 打印智能体

工作根目录：

- `D:\codex-tasks\cad\scripts\drawing_basic_service\print`

其当前目标不是抽象研究，而是：

- 掌握项目级基础知识
- 掌握打印专业知识
- 根据任务要求完成高质量打印
- 持续守护、沉淀、扩展打印子系统

## 进入项目后先看什么

1. `AGENTS.md`
2. `thoughtway/PROJECT_GOVERNANCE.md`
3. `thoughtway/SYSTEM_FOUNDATIONS.md`
4. `dwg_agents_ops/README.md`
5. `cad/scripts/drawing_basic_service/print/README.md`
6. `cad/scripts/drawing_basic_service/print/PRINT_AGENT_SPEC.md`

## 当前一句话共识

`C:\Users\User` 下的 Codex 仍是跨项目通用总管，  
但 `D:\codex-tasks` 已经被正式建设为本项目的项目总管工作区。

## GitHub 版本说明

- GitHub 上提交 `baee4bb`（`Add print orchestration and runtime guard framework`）是一个明确的监督版基线。
- 这里的“监督版”是指：打印编排链已接入 `cad_runtime_guard.py` 与对应的 runtime guard orchestration，用于复杂批量打印任务的运行时监督与稳定性增强。
- 若后续本地实验回退到“无监督、朴素守护”状态，不应反向覆盖这条说明；应通过新的提交单独标注“朴素版”或“对比实验版”。
