# Project Supervisor Architecture

本文件不是讲某一个脚本，而是讲：

当项目主管进入 `D:/codex-tasks` 后，应该如何迅速理解整个系统的设计架构、调度关系和关键规则。

目标是让项目主管在最短路径内明白三件事：

1. 谁是项目总管，谁不是。
2. 打印任务是怎么被调度和执行的。
3. 监督链是怎样并行接入执行链的。

进入系统后的标准做法不是全文阅读，而是：

1. 先读根目录 `folder.meta.json`
2. 再读本文件建立总图
3. 再读 `CURRENT_STATE.md` 获取当前工作态
4. 再进入治理文档、系统基础文档和目标领域目录

## 1. 一句话总图

当前系统采用：

**项目总管 + 四角色智能体能力层 + 领域执行工作区 + 运行监督链**

其中：

- 项目总管负责统一接任务、判断领域、调用角色、裁决结果。
- 角色能力层负责规划、编码、审查、测试等通用能力。
- 领域执行层负责真实业务执行，当前第一优先级是打印执行工作区。
- 运行监督链负责在 CAD 环境层面观察、报警、暂停与恢复建议。

## 2. 四层对象关系

### 2.1 项目总管

工作区：

- `D:/codex-tasks`

角色：

- 系统入口
- 任务路由器
- 规则读取者
- 结果裁决者
- 多层知识沉淀者

项目总管不是某个固定脚本名，而是“进入本项目工作区后负责整体调度的智能体”。

它需要掌握：

- 顶层治理结构
- 当前第一优先级领域
- 角色能力层可做什么
- 运行监督链何时要求停下

### 2.2 角色能力层

目录：

- `D:/codex-tasks/dwg_agents_ops`

当前角色：

- `Planner_Agent`
- `Coder_Agent`
- `Reviewer_Agent`
- `Tester_Agent`

定位：

- 它们是项目总管可调用的通用能力角色
- 它们不是项目总管本身
- 它们默认不直接接管项目主权

也就是说：

- 总管做路由和裁决
- 四角色做局部能力输出

### 2.3 领域执行层

当前第一优先级领域：

- `D:/codex-tasks/cad/scripts/drawing_basic_service/print`

定位：

- 这是当前最重要的业务执行工作区
- 它既可由项目总管调度，也可由人直接交办
- 它首先是“完成高质量打印”的执行对象，不是纯研究对象

### 2.4 运行监督链

核心对象：

- `D:/codex-tasks/cad/system/cad_runtime_guard.py`
- `D:/codex-tasks/dwg_agents_ops/Runtime_Guard_Agent`
- `D:/codex-tasks/dwg_agents_ops/agent_control/runtime_events.jsonl`
- `D:/codex-tasks/dwg_agents_ops/agent_control/runtime/runtime_guard_agent.json`

定位：

- 监督链不是打印脚本的一部分
- 它并行观察 CAD 运行环境
- 当环境可疑时，它要求执行链停下、核验或进入恢复链

## 3. 当前最重要的真实任务架构

当前你最关心的是：

**项目总管调度打印执行链推进任务，并让运行监督链并行监督。**

这件事在系统中的对应关系是：

### 3.1 任务入口

用户或人工向项目总管提出打印任务。

项目总管先判断：

- 这是打印任务，不是普通代码整理任务
- 应进入 `print/` 目录的知识与脚本体系

### 3.2 总管切换到打印领域

项目总管进入：

- `cad/scripts/drawing_basic_service/print`

并读取：

- `README.md`
- `AGENTS.md`
- `PRINT_DISPATCH_PROTOCOL.md`
- `PRINT_AGENT_SPEC.md`
- `PRINT_WORKFLOW.md`

### 3.3 总管按需调用角色能力层

如果任务只是执行现有主链，项目总管可直接走打印主链。

如果任务需要拆解、修补、审查、验证，则项目总管可再调：

- `Planner_Agent`
- `Coder_Agent`
- `Reviewer_Agent`
- `Tester_Agent`

调用关系仍然是：

- 总管发包
- 角色回包
- 总管裁决

### 3.4 打印主执行链

当前打印主链核心脚本是：

- `print_batch_dispatch.py`
- `print_runner.py`
- `print_policy.py`
- `print_executor.py`
- `print_verifier.py`

其职责分工大致是：

- `print_batch_dispatch.py`
  目录级调度、blank-fix、print info 汇总、最终复制与批次 summary。
- `print_runner.py`
  单文件打印主编排，组织 plan、scope/content 分析、execute、verify、summary。
- `print_policy.py`
  构建 PrintPlan，收集 job、排序、分配输出路径。
- `print_executor.py`
  执行真实打印导出。
- `print_verifier.py`
  校验 PDF 页面尺寸与结果完整性。

### 3.5 并行监督链

打印主执行链不是裸跑。

当前已经接入并行监督链：

1. `cad_runtime_guard.py`
   持续被动观察活动 CAD 运行环境，输出状态和事件。
2. `Runtime_Guard_Agent`
   读取事件并形成结构化监督结论。
3. 打印执行链关键节点
   调用 guard bridge / runtime 状态读取逻辑，在危险时显式停下。
4. 项目总管
   需要时介入，决定是否升级到恢复链。

所以当前真实架构不是：

- “打印脚本自己一路跑完”

而是：

- “打印执行链在监督链保护下推进，遇到环境可疑时必须暂停并交还控制权”

## 4. 控制流总图

可以把当前系统理解为下面这条主流：

1. 用户发起任务
2. 项目总管判断任务属于打印领域
3. 项目总管切到 `print/` 知识与脚本体系
4. 项目总管按需调用 `Planner/Coder/Reviewer/Tester`
5. 项目总管启动或接入打印主链
6. 打印主链执行过程中，运行监督链并行工作
7. 若监督链发出 `warning/critical`
8. 执行链停止继续推进
9. 项目总管决定是否核验、恢复或回滚
10. 最终由项目总管统一汇报结果

## 5. 为什么项目总管必须先看这个架构

如果项目总管一进入项目就直接看源码，很容易犯三个错误：

1. 把 `dwg_agents_ops` 误看成项目总管本体。
2. 把 `print` 误看成孤立脚本集合，而不是领域执行层。
3. 忽略 `cad_runtime_guard + Runtime_Guard_Agent` 的监督链设计。

所以项目总管的第一理解顺序应该是：

1. 先看本文件，建立总图。
2. 再看 `CURRENT_STATE.md`，确认当前工作进行到哪里。
3. 再看 `PROJECT_GOVERNANCE.md`，明确项目总管与角色层/领域层关系。
4. 再看 `SYSTEM_FOUNDATIONS.md`，明确 CAD 内核共识。
5. 再进入 `print/` 的领域规则文档。
6. 最后才进入具体脚本和四层 meta。

## 6. 项目总管进入后推荐阅读顺序

1. `folder.meta.json`
2. `thoughtway/PROJECT_SUPERVISOR_ARCHITECTURE.md`
3. `thoughtway/CURRENT_STATE.md`
4. `thoughtway/PROJECT_GOVERNANCE.md`
5. `thoughtway/SYSTEM_FOUNDATIONS.md`
6. `thoughtway/PROJECT_MEMORY_SYSTEM.md`
7. `dwg_agents_ops/README.md`
8. `dwg_agents_ops/agent_control/UNIFIED_CONTROL.md`
9. `dwg_agents_ops/agent_control/RUNTIME_EVENT_PROTOCOL.md`
10. `cad/system/folder.meta.json`
11. `cad/scripts/drawing_basic_service/print/folder.meta.json`
12. `cad/scripts/drawing_basic_service/print/README.md`
13. `cad/scripts/drawing_basic_service/print/PRINT_DISPATCH_PROTOCOL.md`
14. `cad/scripts/drawing_basic_service/print/PRINT_AGENT_SPEC.md`
15. 对应脚本的四层 `meta.json`

## 7. 新窗口主管的最小验收

一个刚进入 `D:/codex-tasks` 的项目主管，在完成上面的最短阅读后，至少应能直接回答：

1. `D:/codex-tasks` 是项目总管工作区，不是普通源码目录。
2. `dwg_agents_ops/` 是角色能力层，不是项目总管本体。
3. 当前第一优先级领域执行层是 `cad/scripts/drawing_basic_service/print/`。
4. 当前打印真实架构是“项目总管调度打印执行链，并行接入 runtime guard 监督链”。
5. `cad/system/` 是统一连接、协调和守护底座，业务层不应长期绕过。
6. 真正进入源码前，应先依赖 `folder.meta.json + 治理文档 + 四层 meta` 建立压缩理解。

## 8. 一句话结论

当前项目不是“几个打印脚本 + 几个 agent 脚本”的松散集合，而是：

**项目总管统一调度打印领域执行链，并在运行监督链保护下推进任务闭环的系统。**
