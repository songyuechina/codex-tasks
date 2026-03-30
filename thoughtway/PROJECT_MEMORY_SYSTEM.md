# Project Memory System

本文件回答一个项目级问题：

随着 `D:/codex-tasks` 持续扩大，怎样让智能体持续延续对整个项目的理解，而不是每次都重新通读全仓库文档和源码？

答案不是再堆更多长文档，而是建立“分层记忆 + 固定刷新协议”。

## 1. 问题本质

项目扩大后，智能体会同时遇到四个问题：

1. 文档越来越多，但很多信息的稳定性不同。
2. 代码越来越多，不能每次都从源码全文开始。
3. 输出文件、案例资产、运行日志会快速淹没真正重要的系统知识。
4. 某次任务中得出的结论，如果不回写到固定位置，下次仍会丢失。

所以需要把项目知识拆成不同层级，而不是只靠一次性上下文窗口。

## 2. 五层记忆结构

### L0 目录语义层

载体：

- `folder.meta.json`
- 各子目录下的 `folder.meta.json`

作用：

- 用最小成本告诉智能体“这个目录是什么、先看什么、哪些是稳定骨架、哪些是波动输出”。
- 负责目录级路由，不负责脚本实现细节。

这是整个项目的第一入口。

### L1 项目治理层

载体：

- `README.md`
- `AGENTS.md`
- `thoughtway/CURRENT_STATE.md`
- `thoughtway/PROJECT_GOVERNANCE.md`
- `thoughtway/SYSTEM_FOUNDATIONS.md`
- 领域目录内的 `README.md` / `AGENTS.md` / protocol / spec 文档

作用：

- 固化项目结构、总目标、默认工作方式、禁止事项与阅读顺序。
- 当目录级语义已确定后，提供第二层规则。
- 其中 `CURRENT_STATE.md` 负责承接“当前正在做什么、下一步该做什么”，避免新窗口只能去翻 `conversation_log.md`。

### L2 代码压缩层

载体：

- `*_quote.meta.json`
- `*_procedure.meta.json`
- `*_functions.quote.meta.json`
- `*_functions.procedure.meta.json`
- `cad/tools/basic_graph_analyzer.py`
- `cad/tools/function_analyzer.py`

作用：

- 把源码压缩成脚本骨架、函数骨架、静态调用图和语义分析结果。
- 让智能体不必每次都从全量源码重新理解。

这层的目标是“先压缩、后下钻”。

### L3 领域与任务记忆层

载体：

- `cad/scripts/drawing_basic_service/print/cases/CASE_MANIFEST.md`
- `dwg_agents_ops/**/memory/rolling_summary.md`
- `dwg_agents_ops/agent_control/task_board.json`

作用：

- 记录当前任务、案例权威输出、领域经验和最近状态。
- 这一层不是长期架构说明，而是“近期工作态”和“领域案例锚点”。

### L4 可刷新快照层

载体：

- `dwg_system_tools/build_project_memory.py`
- `thoughtway/project_memory/PROJECT_MAP.md`
- `thoughtway/project_memory/PROJECT_MAP.json`

作用：

- 周期性或按需对“当前源代码与文档集合”做一次项目快照。
- 重点覆盖 `py`、`md`、`toml`、关键 `json`，并主动排除 DWG/PDF、输出目录、运行日志、会话记录。

这一层解决“项目现实状态不断变化”的问题。

## 3. 以后智能体的标准阅读协议

以后进入 `D:/codex-tasks` 时，不应该再默认全文阅读。

推荐协议：

1. 先读根目录 `folder.meta.json`。
2. 再读 `thoughtway/PROJECT_SUPERVISOR_ARCHITECTURE.md`。
3. 再读 `thoughtway/CURRENT_STATE.md`。
4. 再读 `thoughtway/PROJECT_GOVERNANCE.md` 与 `thoughtway/SYSTEM_FOUNDATIONS.md`。
5. 根据任务进入对应子目录的 `folder.meta.json`。
6. 再读该目录的 `README.md` / `AGENTS.md` / 协议文档。
7. 需要脚本控制层时，读四层 `meta.json`。
8. 只有在需要实现细节、验证细节或修复问题时，才深入源码。

这样做的关键是：

- 目录层负责路由。
- 架构层负责建立项目主管的总图。
- 文档层负责规则。
- meta 层负责压缩源码。
- 源码层只在需要时读取。

## 4. 刷新协议

要让项目理解长期延续，重点不在“多读”，而在“每次变化后正确回写”。

### 4.1 结构变化

当目录职责、模块边界、主优先级业务发生变化时：

1. 先更新相关 `folder.meta.json`
2. 再更新对应 `README.md` / `AGENTS.md`
3. 最后刷新 `PROJECT_MAP.md/json`

### 4.2 脚本职责变化

当脚本功能、公共入口或关键流程变化时：

1. 更新脚本文档
2. 更新对应四层 `meta.json`
3. 必要时更新 `basic_graph` 缓存或函数分析资产

### 4.2.1 meta 覆盖边界

不是所有 `py` 文件都应该纳入 `meta.json` 覆盖。

应纳入的，通常是：

- 长期维护的系统脚本
- 业务主链脚本
- 协作层与工具层中的正式脚本
- 后续仍会被智能体重复调用、修改、排查的脚本

默认不纳入的，通常是：

- `thoughtway/` 根目录下的思想指导文本
- `thoughtway/参考/` 下的参考脚本，即使它们仍是 `py`
- 纯参考、纯归档、纯实验、纯迁移脚本
- 输入输出资产、运行日志、缓存与一次性会话产物

当前项目中的明确约定是：

- `thoughtway` 的思想指导文件以 `txt/md` 为主，不做 `meta.json`
- `thoughtway/参考/*.py` 保留为参考脚本，但不做 `meta.json`

因此后续统计“脚本是否缺少 meta”时，必须先按覆盖范围过滤，而不是把所有 `py` 文件直接算进去。

### 4.3 新案例出现

当真实任务暴露新案例时：

1. 把案例放入案例资产区
2. 更新 `CASE_MANIFEST.md`
3. 把稳定经验回写到 `PRINT_KNOWLEDGE.md` 或规则文档

### 4.4 新任务结论

如果某轮任务形成了新的长期共识，不要只留在聊天或 `rolling_summary` 中。

必须把稳定结论回写到：

- `thoughtway/*.md`
- 对应目录的 `README.md` / `AGENTS.md`
- 必要时 `folder.meta.json`

## 5. 当前项目的推荐落地方式

对本项目，建议长期坚持下面这套组合：

1. 用 `folder.meta.json` 管目录级语义地图。
2. 用 `README.md` / `AGENTS.md` / `thoughtway/*.md` 管规则和系统共识。
3. 用四层 `meta.json` 管脚本和函数骨架。
4. 用 `CASE_MANIFEST.md`、`rolling_summary.md`、`task_board.json` 管任务态和领域态。
5. 用 `build_project_memory.py` 周期性生成项目快照。

其中：

- `CURRENT_STATE.md` 负责新窗口快速接手
- `conversation_log.md` 只保留过程背景，不应充当当前任务态入口

## 6. 明确不要做的事

不要依赖以下方式维持长期项目理解：

- 只靠聊天历史
- 只靠某一次任务中的临时摘要
- 让输出目录和资产目录混进项目主知识入口
- 把 `conversation_log.md` 当作唯一真相
- 让 `rolling_summary.md` 承担长期架构职责
- 把参考脚本和思想材料强行纳入 `meta.json` 覆盖统计

这些都只能作为补充，不能作为项目主记忆层。

## 7. 一句话结论

让智能体持续理解整个项目，不靠反复通读，而靠：

**目录语义地图 + 稳定规则文档 + 代码压缩资产 + 任务/案例记忆 + 可刷新项目快照。**
