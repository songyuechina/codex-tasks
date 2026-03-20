# Runtime Guard Agent

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

## 当前输出口径

- `guard_status`
  - 当前来自 `cad_runtime_guard.py` 的运行态判断
- `guard_decision`
  - `continue / pause_and_verify / pause_and_recover / resume_allowed`
- `manager_notice_required`
  - 是否需要项目总管介入
- `execution_notice_required`
  - 是否需要执行智能体暂停或上报

## 与项目总管的关系

项目总管调度执行任务时，应同时保证两件事成立：

1. `cad_runtime_guard.py` 已运行
2. `Runtime_Guard_Agent` 已运行

然后在需要时读取：

- `runtime/runtime_guard_agent.json`
- `runtime_guard_decisions.jsonl`

来判断当前是否需要暂停执行、触发恢复或上报裁决。
