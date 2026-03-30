# Runtime Guard Agent

说明：

- `Runtime_Guard_Agent` 是历史目录名，当前保留以兼容既有文档与脚本引用
- 它不属于 `Planner / Coder / Reviewer / Tester` 四角色智能体
- 当前概念上应理解为“本地监督对象 / 监督入口”

`Runtime_Guard_Agent/` 是面向 `cad_runtime_guard.py` 的本地事件驱动监督入口。

它当前不是高频远程模型轮询器，而是一个低耗、单实例、本地读取型监督对象。

## 当前职责

1. 读取：
   - `dwg_agents_ops/agent_control/runtime/cad_runtime_guard.json`
   - `dwg_agents_ops/agent_control/runtime_events.jsonl`
2. 形成结构化监督结论
3. 将自己的当前状态写入：
   - `dwg_agents_ops/agent_control/runtime/runtime_guard_agent.json`
4. 将监督决策追加写入：
   - `dwg_agents_ops/agent_control/runtime_guard_decisions.jsonl`

当前当监督对象读到：

- `guard_status = suspected_plain_cad`
- `guard_decision = pause_and_recover`

时，已可在本地直接调用 `CAD_core.litz()` 执行恢复闭环。

## 当前最合理的扩展职责

如果当前本地监督对象的设计被证明合理，那么它的职责不应长期停留在“只消费纯 CAD 告警”。

更合理的扩展口径是：

1. 环境监督
   - 发现 `suspected_plain_cad`
   - 发现 `cad_busy / cad_doc_unavailable`
   - 发现恢复后的 `resume_allowed`
2. 流程纪律督导
   - 督导执行链在每个 DWG 完成后做收尾关图
   - 督导执行链调用 `CAD_core.cad_zt_oneb()`，把环境压回简化状态
3. 规则前置督导
   - 督导执行者明确本次受控入口和恢复入口
   - 督导执行者遵守打印模式、输出契约和停机规则
4. 知识前置核查
   - 督导执行者掌握当前任务必需的系统知识和打印专业知识关键点

也就是说，它应逐步从“事件消费者”升级为“环境监督 + 流程纪律督导 + 关键知识核查”的监督对象。

## 为什么现在先做成本地协调对象

当前阶段的关键不是“让更多模型一直跑”，而是先形成稳定闭环：

- 本地守护脚本采集事实
- 本地监督对象消费事件
- 执行链在关键节点响应控制信号
- 项目总管按需介入

这样可以把 token 消耗压到最低，只在真正升级、裁决、汇报时再调用远程模型。

## 启动

```powershell
python D:\codex-tasks\dwg_agents_ops\Runtime_Guard_Agent\agent_cli.py
python D:\codex-tasks\dwg_agents_ops\Runtime_Guard_Agent\agent_cli.py --once
```

说明：

- 常驻模式：持续监督
- `--once`：适合在实测或调试时手动触发一次监督与恢复

## 当前输出口径

- `guard_status`
  - 当前来自 `cad_runtime_guard.py` 的运行态判断
- `guard_decision`
  - `continue / pause_and_verify / pause_and_recover / resume_allowed`
- `manager_notice_required`
  - 是否需要项目总管介入
- `execution_notice_required`
  - 是否需要执行链暂停或上报

当前 `runtime_guard_agent.json` 里还会附带 `auto_recovery`：

- `attempt_count`
- `last_result`
- `last_before_status`
- `last_after_status`
- `last_recovered_pid`

## 与项目总管的关系

项目总管调度执行任务时，应同时保证两件事成立：

1. `cad_runtime_guard.py` 已运行
2. `Runtime_Guard_Agent` 已运行

然后在需要时读取：

- `runtime/runtime_guard_agent.json`
- `runtime_guard_decisions.jsonl`

来判断当前是否需要暂停执行、触发恢复或上报裁决。

若后续继续扩展监督职责，项目总管还应把下面三类信息纳入监督口径：

1. 当前 DWG 是否已完成收尾归一
2. 当前执行者是否已明确受控入口与恢复入口
3. 当前执行者是否已经读过本轮必须遵守的规则文档

## 实测脚本

当前用于验证 plain CAD 自动恢复的脚本：

```powershell
python D:\codex-tasks\cad\system\runtime_guard_recovery_validation.py --mode random --rounds 2 --seed 20260321
```

输出落盘到：

- `D:/codex-tasks/cad/system/logs/runtime-guard-validation/`
