# Project Governance

适用范围：

- `D:/codex-tasks/`

本文件用于明确当前项目的总管、四角色智能体、领域执行工作区之间的关系。

## 1. 总体结构

当前项目建议采用三层主结构，并显式接入并行运行监督链：

1. 总管层
2. 角色能力层
3. 领域执行层
4. 运行监督链

## 2. 总管层

总管分为两种：

### 2.1 通用总管

- 运行位置：
  `C:\Users\User`

作用：

- 处理多个项目
- 作为更高层的通用调度入口

### 2.2 项目总管

- 推荐运行位置：
  `D:\codex-tasks`

作用：

- 负责本项目内部的规划、协调、调度、裁决与沉淀
- 读取并维护本项目的系统知识、案例经验、局部智能体规范

结论：

- 以后如果是专门处理 `codex-tasks` 项目，进入 `D:\codex-tasks` 再运行 `codex / gpt-5.4` 更合理
- 因为项目知识、规则、经验、上下文应尽量留在项目目录中

## 3. 四角色能力层

当前角色能力层位于：

- `D:/codex-tasks/dwg_agents_ops/`

当前四角色为：

- `Planner_Agent`
- `Coder_Agent`
- `Reviewer_Agent`
- `Tester_Agent`

它们不是项目总管，而是总管可调用的通用能力角色：

- `Planner`
  负责针对具体任务做阶段规划、依赖拆分、风险识别
- `Coder`
  负责实现
- `Reviewer`
  负责审查
- `Tester`
  负责验证

总管负责调度它们，而不是把项目主权交给它们。

## 4. 领域执行层

领域执行层是按业务模块建设的专门执行工作区。

当前最重要的例子是：

- `D:/codex-tasks/cad/scripts/drawing_basic_service/print/`

它应被视为“打印执行工作区”的工作根目录。

未来还可以继续建设：

- 图签执行工作区
- 块处理执行工作区
- 内容分析执行工作区
- 目录编制执行工作区

这些都属于领域执行层。

## 5. 推荐运转模式

推荐的实际工作方式是：

1. 用户向总管下达任务
2. 总管判断该任务属于哪个领域
3. 总管进入对应领域执行工作区
4. 总管按需要调用四角色能力层
5. 若任务涉及真实 CAD / 打印执行，同时接入运行监督链
6. 总管统一裁决结果并推进落地

例如打印任务：

1. 用户给出打印任务
2. 总管切换到 `print/` 目录的知识与脚本体系
3. 如有需要，先调 `Planner_Agent`
4. 再调 `Coder / Reviewer / Tester`
5. 若进入真实打印链，同时启动或接入 runtime guard 监督
6. 最终仍由总管完成协调、执行、汇报

## 6. 运行监督链

当前监督链核心对象是：

- `D:/codex-tasks/cad/system/cad_runtime_guard.py`
- `D:/codex-tasks/cad/system/runtime_guard_bridge.py`
- `D:/codex-tasks/dwg_agents_ops/Runtime_Guard_Agent/`
- `D:/codex-tasks/dwg_agents_ops/agent_control/RUNTIME_EVENT_PROTOCOL.md`

定位：

- 监督链不是项目总管本体
- 监督链也不是打印主链的一部分
- 它负责并行观察 CAD 环境，并把可疑状态转换为结构化事件和监督结论
- 当监督链给出 `warning / critical` 时，总管必须把“继续执行”视为待裁决事项，而不是默认继续推进

## 7. 并发原则

本项目不刻意追求并发。

默认原则：

- 先保证结构清晰、角色清楚、记录完整
- 再按需要考虑并发

可并发的通常是：

- 文档整理
- 规划输出
- 审查
- 离线分析

不宜随便并发的通常是：

- 天正 CAD GUI 操作
- 同一 DWG 的实际打印
- 会争用 `COM / licad / WPS / CAD` 的任务

结论：

- 模型推理层可以按需并发
- CAD 真机执行层原则上串行独占更稳

## 8. 项目知识沉淀位置

本项目的系统知识、规划、协调、实践、经验，应优先沉淀在：

- `D:/codex-tasks/thoughtway/`

而不是继续散落在 `C:\Users\User` 的通用环境里。

推荐分工：

- `thoughtway/`
  项目级思想、规则、经验、治理
- `dwg_agents_ops/`
  角色协作、调度、监督
- 各业务目录
  领域执行工作区自己的知识与案例

## 9. 当前一句话共识

`C:\Users\User` 下的 Codex 仍是通用总管，
但 `D:\codex-tasks` 内应形成自己的项目总管工作区，并在角色能力层、领域执行层和运行监督链的支持下推进任务。
