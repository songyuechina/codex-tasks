# Supervision Guide

`agent_control/supervisor_cli.py` 是主控层对四角色的稳定监督入口。

## 目标

- 不再让子智能体自己猜本地路径
- 由主控先读取文件，再把必要上下文打包给角色
- 统一保存 prompt、response、工具输出
- 先做健康检查，再做任务派发

## 为什么更稳定

旧问题主要有两类：

1. 子智能体尝试自己访问 `D:\codex-tasks`，但其内部工具环境并不总能看到该路径
2. prompt 过松，角色会把精力浪费在“找文件”“猜环境”上，而不是回答任务本身

主控打包后，角色只处理：

- 目标
- 约束
- 已知事实
- 必要文件内容

## 用法

### 1. 健康检查

```powershell
python D:\codex-tasks\dwg_agents_ops\agent_control\supervisor_cli.py healthcheck --all
```

### 2. 派发单个任务

```powershell
python D:\codex-tasks\dwg_agents_ops\agent_control\supervisor_cli.py dispatch `
  --role coder `
  --title "print-followup" `
  --objective "说明当前打印实现最值得补强的一项" `
  --context "不要搜索其他路径，只基于给定文件回答" `
  --file D:\codex-tasks\cad\scripts\drawing_basic_service\print\print_policy.py `
  --file D:\codex-tasks\cad\scripts\drawing_basic_service\print\print_executor.py
```

## 输出归档

所有监督运行都会写入：

- `dwg_agents_ops/agent_control/supervision/<role>/<timestamp>/prompt.md`
- `dwg_agents_ops/agent_control/supervision/<role>/<timestamp>/response.txt`
- `dwg_agents_ops/agent_control/supervision/<role>/<timestamp>/tool_output.txt`

## 管理规则

1. 每次真实任务前，先做 `healthcheck`
2. 复杂任务拆成：
   - planner 先做任务分解和阶段计划
   - coder 再做实现建议或实现复核
   - reviewer 再做 findings-first 审查
   - tester 最后做覆盖结论
3. 不要把“读整个项目”的责任丢给子智能体
4. 主控应先筛选关键文件，再投喂
5. 如果角色返回空内容、超时或无 `PROGRESS` 尾注，应直接视为失败并重派
6. 若任务涉及真实 CAD / 打印执行，项目总管还应确认：
   - `cad_runtime_guard.py` 已运行
   - `Runtime_Guard_Agent` 已运行
   - 执行入口已接入运行守护响应逻辑

## 当前实测经验

截至当前阶段的控制经验：

- `planner` 适合先吃任务目标、约束、关键文件摘要，再输出阶段计划
- `coder`、`tester` 在“精简证据包”下较稳定
- `reviewer` 的健康检查可稳定通过，但在大文件包下更容易超时

因此当前建议：

1. `planner`
   - 单次投喂任务目标、约束和少量关键文件
   - 先让它产出阶段拆分、风险和依赖
1. `coder` / `tester`
   - 单次投喂 `1-3` 个关键文件
   - 每个文件建议 `1200-2000` 字以内
2. `reviewer`
   - 先 `healthcheck`
   - 再投喂单文件或摘要化风险包
   - 不要一次喂多份长文件
3. 复杂任务采用三阶段
   - 第一阶段：planner 出任务拆分
   - 第二阶段：主控整理代码摘要/事实提炼并派给 coder
   - 第三阶段：再把摘要包派给 reviewer/tester

## 运行守护链建议

当任务会真正操作 CAD 时，推荐项目总管同时维护两条链：

1. 任务执行链
   - planner / coder / reviewer / tester
2. 运行监督链
   - `cad_runtime_guard.py`
   - `Runtime_Guard_Agent`

其中：

- `cad_runtime_guard.py` 负责持续采集事实
- `Runtime_Guard_Agent` 负责消费事件并形成监督结论
- 项目总管只在事件升级、需要裁决或需要恢复时介入

## 运行监督的扩展口径

若任务是“真实 CAD / 打印执行”，监督不应只理解为“看到纯 CAD 再报警”。

当前更合理的监督对象应覆盖三层：

1. 环境层
   - 是否出现纯 CAD / 非天正偏航
   - 是否出现 `cad_busy / cad_doc_unavailable`
2. 流程纪律层
   - 每完成一个 DWG 后，是否已关掉相关工作文档
   - 是否已调用 `CAD_core.cad_zt_oneb()` 把环境压回简化状态
3. 知识前置层
   - 执行者是否已经明确受控入口与恢复入口
   - 执行者是否已经掌握本轮任务必须依赖的系统知识和打印规则

也就是说，本地监督对象不应只是“告警转发器”，而应逐步成为：

- 环境事实协调者
- 执行纪律督导者
- 关键规则与知识的前置把关者
