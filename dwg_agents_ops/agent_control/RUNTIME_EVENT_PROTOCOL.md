# Runtime Event Protocol

适用范围：

- `D:/codex-tasks/cad/system/cad_runtime_guard.py`
- `D:/codex-tasks/dwg_agents_ops/Runtime_Guard_Agent/`
- `D:/codex-tasks/cad/scripts/drawing_basic_service/print/`

## 1. 目标

本协议定义“运行守护事件”在项目中的最小闭环：

1. `cad_runtime_guard.py` 发现运行环境异常或恢复
2. 结构化事件写入 `runtime_events.jsonl`
3. `Runtime_Guard_Agent` 读取事件并形成监督结论
4. 执行智能体在关键节点读取并响应控制事件
5. 项目总管在需要时读取监督状态并决定是否升级恢复

本协议当前只处理：

- 天正环境可信性
- 纯 CAD / 非天正环境疑似偏航
- 恢复后允许继续执行

## 2. 事件源

当前正式事件源是：

- `D:/codex-tasks/dwg_agents_ops/agent_control/runtime_events.jsonl`

当前正式状态源是：

- `D:/codex-tasks/dwg_agents_ops/agent_control/runtime/cad_runtime_guard.json`

## 3. 事件字段

每条事件至少包含：

- `timestamp`
- `source`
- `target`
- `severity`
- `code`
- `message`
- `recommended_action`
- `status`
- `suspicious_streak`
- `doc_name`
- `pid`
- `process_hint`

## 4. severity 语义

- `info`
  - 当前没有需要执行侧立即暂停的风险
- `warning`
  - 当前环境存在可疑偏航，执行侧应暂停并核验
- `critical`
  - 当前环境高度可疑或已明显偏航，执行侧不得继续，应暂停并进入恢复链

## 5. recommended_action 语义

- `none`
  - 不要求动作
- `observe`
  - 仅观察
- `pause_and_verify`
  - 执行侧应在关键节点显式停下，并报告 / 抛出受控异常
- `pause_and_recover`
  - 执行侧应立即停止继续推进，并请求进入恢复链
- `resume_allowed`
  - 之前的告警已恢复，可允许继续执行

## 6. target 语义

当前默认目标可使用：

- `execution_agents`
- `print_execution`
- `print_agent`
- `all`

打印主链当前按以下目标集合消费事件：

- `execution_agents`
- `print_execution`
- `print_agent`
- `all`

## 7. 执行智能体响应规则

打印执行链在关键节点读取运行守护状态后，应按以下规则响应：

1. 若命中：
   - `severity=critical`
   - 或 `recommended_action=pause_and_recover`

   则：
   - 不得继续打印
   - 必须抛出受控异常
   - 必须把当前 checkpoint、severity、recommended_action、status 带出

2. 若命中：
   - `severity=warning`
   - 或 `recommended_action=pause_and_verify`

   则：
   - 不得继续闷头执行
   - 必须显式停下
   - 必须抛出受控异常或明确上报

3. 若命中：
   - `recommended_action=resume_allowed`

   则：
   - 可允许恢复执行
   - 但应以最新状态为准，不复用旧告警

## 8. 项目总管何时介入

项目总管应在以下情况介入：

1. `Runtime_Guard_Agent` 标记：
   - `manager_notice_required = 1`
2. 执行链抛出运行守护受控异常
3. 当前事件持续升级但仍未恢复
4. 需要决定是否调用 `litz()` 或恢复链

## 9. 当前最小闭环

当前已落地的最小闭环是：

1. `cad_runtime_guard.py` 长期运行并输出事件
2. `Runtime_Guard_Agent` 长期运行并输出监督结论
3. 打印执行链在关键节点调用运行守护桥接模块
4. 命中 `warning/critical` 时，执行链不再静默忽略

这已经满足“先停下，再上报，再决定是否恢复”的最小闭环。
