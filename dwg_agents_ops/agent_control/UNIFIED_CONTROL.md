# Unified Control

`dwg_agents_ops/agent_control/` 是四角色协作的统一控制目录。

## 目标

- 给 `Planner_Agent`、`Coder_Agent`、`Reviewer_Agent`、`Tester_Agent` 提供统一任务板
- 给监控工具提供运行时状态源
- 保持协作状态不散落到各角色目录之外

## 关键文件

- `task_board.json`
  当前任务板。
- `runtime/<role>.json`
  角色心跳与最近状态。
- `runtime/cad_runtime_guard.json`
  运行守护脚本的当前状态。
- `runtime/runtime_guard_agent.json`
  监督对象对当前运行守护状态的结构化结论。
- `runtime_events.jsonl`
  `cad_runtime_guard.py` 产出的运行事件流。
- `runtime_guard_decisions.jsonl`
  `Runtime_Guard_Agent` 对事件的监督结论流。
- `monitor_cli.py`
  命令行监控脚本。

## 状态建议

推荐任务状态：

- `backlog`
- `ready_for_planning`
- `planning`
- `planned`
- `replan_requested`
- `ready_for_coding`
- `coding`
- `coded`
- `reviewing`
- `review_passed`
- `review_failed`
- `testing`
- `test_passed`
- `test_failed`
- `blocked`
- `stale`

## 默认流转

1. 主控智能体或人工把任务写入 `task_board.json`
2. `Planner_Agent` 处理 `ready_for_planning`
3. 完成后置为 `planned`
4. `Coder_Agent` 处理 `planned` 或 `ready_for_coding`
5. 完成后置为 `coded`
6. `Reviewer_Agent` 审查后置为 `review_passed` 或 `review_failed`
7. `Tester_Agent` 测试后置为 `test_passed` 或 `test_failed`

## 注意

- 这里是协作层，不替代 git 或真实代码审阅流程。
- 角色输出必须写清 `task`、`status`、`completion`、`next`。
- 运行守护链当前实行“本地脚本采集事实 -> 本地监督对象形成结论 -> 执行链关键节点响应 -> 项目总管按需介入”的保守闭环。
