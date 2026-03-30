# Current State

最后更新：`2026-03-21`

本文件不是长期架构说明，而是给新窗口一个最短接手入口：

- 这个项目当前是什么结构
- 最近已经做了哪些关键变更
- 当前第一优先级是什么
- 下一步最值得做什么

若你是第一次进入 `D:/codex-tasks`，推荐只先读：

1. `folder.meta.json`
2. `thoughtway/PROJECT_SUPERVISOR_ARCHITECTURE.md`
3. `thoughtway/CURRENT_STATE.md`
4. `thoughtway/TERMINOLOGY.md`
5. `AGENTS.md`

## 1. 当前总图

当前项目统一按下面这套结构理解：

- 项目总管工作区：`D:/codex-tasks`
- 四角色智能体能力层：`dwg_agents_ops/`
- 当前第一优先级领域执行工作区：`cad/scripts/drawing_basic_service/print/`
- 运行监督链：`cad/system/cad_runtime_guard.py` 及其相关监督入口

当前推荐口径是：

- `项目总管 + 四角色能力层 + 打印执行链 + 运行监督链`

不要再默认说成：

- `项目总管 + 打印智能体 + 监督智能体`

## 2. 当前关键共识

1. 真正的智能体角色只有四个：
   - `Planner_Agent`
   - `Coder_Agent`
   - `Reviewer_Agent`
   - `Tester_Agent`
2. 打印体系当前不是第五个智能体，而是：
   - 打印执行工作区
   - 打印执行链
3. `Runtime_Guard_Agent/` 是历史目录名保留：
   - 概念上应理解为本地监督入口 / 监督链协调组件
   - 不应与四角色并列理解
4. 对真实 CAD / 打印任务：
   - 应先明确受控入口
   - 应先明确纯 CAD / 非天正环境的恢复入口
   - 应在运行监督链保护下推进

## 3. 最近已经完成的关键工作

### 3.1 术语治理已收口

已经把项目入口层和打印领域文档统一成：

- 四角色智能体
- 打印执行链
- 运行监督链

不再把执行链和监督链写成额外智能体角色。

### 3.2 Planner 配置已更新

本地四角色配置文件位于：

- `dwg_agents_ops/local/agents.local.toml`

其中 `planner` 已改为：

- `base_url = https://cc.ioasis.xyz/v1`
- `model = gpt-5.4`

具体密钥以本地配置文件为准，不在本文重复扩散。

### 3.3 打印体系当前工程共识已稳定

当前打印任务应理解为：

- `print_batch_dispatch.py` 负责脚本级调度
- `print_runner.py` / `print_executor.py` / `print_info_analysis.py` 等组成执行链
- `cad_runtime_guard.py` / `cad_dialog_killer.py` / `cad_command_monitor.py` 组成运行监督链

其工程目标不是抽象研究，而是：

- 稳定完成 DWG 打印
- 让监督链及时发现环境偏航
- 每个 DWG 完成后把 CAD 归一回简化状态

## 4. 当前第一优先级

当前第一优先级仍是：

- 打印执行工作区的稳定运行与持续治理

尤其关注：

1. 新窗口进入后是否能迅速理解项目总图与关键规则
2. 打印执行链与运行监督链在真实案例中的配合是否稳定
3. 每个 DWG 完成后的关图与 `cad_zt_oneb()` 归一是否严格执行
4. 监督侧是否逐步覆盖环境监督、流程纪律监督、规则前置监督、知识前置监督

## 5. 当前建议的下一步

如果你是新开的窗口，最值得优先做的是：

1. 按本文开头的最短路径完成首读
2. 直接回答以下问题，验证自己是否真正接手成功：
   - `D:/codex-tasks` 是什么工作区
   - `dwg_agents_ops/` 是什么，不是什么
   - 当前第一优先级领域目录是哪一个
   - 当前打印任务的真实架构是什么
   - 当前为什么不能再泛称“打印智能体 / 监督智能体”
3. 若上述回答无误，再进入：
   - `cad/scripts/drawing_basic_service/print/`
   - 准备继续真实案例验证或脚本修补

## 6. 当前不要做的事

不要：

- 一上来全文通读整个仓库
- 把 `conversation_log.md` 当作当前任务入口
- 把 `dwg_agents_ops/` 误判为项目总管本体
- 把 `print/` 误判为几个孤立脚本
- 忽略运行监督链对真实打印任务的约束

## 7. 当前任务态锚点

当前任务板位于：

- `dwg_agents_ops/agent_control/task_board.json`

当前最值得继续推进的事项是：

- `OPS-20260321-02`
  - 验证新窗口项目总管能否快速理解体系并续接工作
- `PRINT-20260321-03`
  - 继续观察打印执行链与运行监督链在真实案例中的配合问题

如果本文与其他旧记录冲突：

1. 先以 `folder.meta.json`
2. 再以 `PROJECT_SUPERVISOR_ARCHITECTURE.md`
3. 再以本文 `CURRENT_STATE.md`
4. 再以 `AGENTS.md`

为准。
