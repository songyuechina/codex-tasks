# DWG Agents Ops

`dwg_agents_ops/` 是面向 `D:/codex-tasks` 的四角色智能体协作层。

它不是项目总管本身，而是项目总管可调用的“角色能力层”。

如果当前是在 `D:\codex-tasks` 中运行项目总管，那么总管应把这里视为：

- 任务级规划
- 编码实现
- 审查
- 测试

这四类通用能力的统一调度层。

目标不是替代 `cad/system` 这套 CAD 内核，而是给规划、编码、审查、测试四个子智能体提供一套稳定的协作入口，使它们能够围绕同一个任务板和同一个项目上下文推进 DWG/CAD 自动化迭代。

## 当前定位

- `cad/system/`：CAD / DWG 统一连接、选择、文件操作、协调、日志、内容分析内核。
- `cad/library/`：建立在 `cad/system/` 之上的业务函数库。
- `dwg_system_tools/`：meta 生成、校验、扫描工具链。
- `dwg_cases/`：样例 DWG / DXE 资产。
- `dwg_agents_ops/`：四角色智能体协作层。

项目治理关系见：

- `D:/codex-tasks/thoughtway/PROJECT_GOVERNANCE.md`

## 系统基础知识

进入本目录工作的角色智能体，应优先掌握：

- `D:/codex-tasks/thoughtway/SYSTEM_FOUNDATIONS.md`

尤其要明确以下模块分工：

- `licad.py`：统一连接入口
- `CAD_core.py`：文件级控制
- `CAD_selection.py`：选择与属性访问
- `CAD_com_utils.py`：CAD 忙 / COM busy 处理
- `CAD_coordination.py`：命令同步与事务保护
- `cad_dialog_killer.py`：弹窗干扰处理
- `cad_command_monitor.py`：命令卡死监控
- `content_analysis_dwg_file.py`：DWG 内容分析与前后对比

## 本轮重建内容

当前工作区中的旧 `dwg_agents_ops` 已被清空，但 git 历史表明曾经存在一版多智能体骨架。新版本保留“角色化协作”方向，同时修正旧版的几个关键问题：

- 不再为每个角色复制一整份运行时代码。
- `Planner_Agent`、`Coder_Agent`、`Reviewer_Agent`、`Tester_Agent` 都通过共享运行时启动。
- 每个角色都支持独立的 `base_url`、`api_key`、`model`。
- 任务板与运行时状态统一落在 `dwg_agents_ops/agent_control/`。
- 新增 `Runtime_Guard_Agent` 作为本地事件驱动监督对象，优先消费运行守护事件，而不是高频调用远程模型。

## 目录

- `PROJECT_RESEARCH.md`
  当前项目研究纪要，记录项目目标、现状、成果与缺口。
- `shared/runtime.py`
  共享智能体运行时。
- `Planner_Agent/`
  任务级规划子智能体。
- `Coder_Agent/`
  编码子智能体。
- `Reviewer_Agent/`
  审查子智能体。
- `Tester_Agent/`
  测试子智能体。
- `Runtime_Guard_Agent/`
  历史目录名保留；概念上属于本地监督对象/监督入口，不属于四角色智能体，负责消费 `cad_runtime_guard.py` 产出的事件并形成结构化监督结论。
- `agent_control/`
  任务板、运行时状态、监控工具与统一协作约定。
- `agents.example.toml`
  四角色独立接口配置样例。

## 配置方式

推荐在本地创建：

- `D:/codex-tasks/dwg_agents_ops/local/agents.local.toml`

格式可直接参考：

- `D:/codex-tasks/dwg_agents_ops/agents.example.toml`

每个角色使用独立配置段：

```toml
[planner]
base_url = "https://your-planner-endpoint/v1"
api_key = "planner-key"
model = "planner-model"

[coder]
base_url = "https://your-coder-endpoint/v1"
api_key = "coder-key"
model = "coder-model"

[reviewer]
base_url = "https://your-reviewer-endpoint/v1"
api_key = "reviewer-key"
model = "reviewer-model"

[tester]
base_url = "https://your-tester-endpoint/v1"
api_key = "tester-key"
model = "tester-model"
```

如果不想写本地 TOML，也可以改用环境变量：

- `DWG_CODER_BASE_URL`
- `DWG_CODER_API_KEY`
- `DWG_CODER_MODEL`
- `DWG_PLANNER_BASE_URL`
- `DWG_PLANNER_API_KEY`
- `DWG_PLANNER_MODEL`
- `DWG_REVIEWER_BASE_URL`
- `DWG_REVIEWER_API_KEY`
- `DWG_REVIEWER_MODEL`
- `DWG_TESTER_BASE_URL`
- `DWG_TESTER_API_KEY`
- `DWG_TESTER_MODEL`

## 启动

```powershell
python D:\codex-tasks\dwg_agents_ops\Planner_Agent\agent_cli.py
python D:\codex-tasks\dwg_agents_ops\Coder_Agent\agent_cli.py
python D:\codex-tasks\dwg_agents_ops\Reviewer_Agent\agent_cli.py
python D:\codex-tasks\dwg_agents_ops\Tester_Agent\agent_cli.py
python D:\codex-tasks\dwg_agents_ops\Runtime_Guard_Agent\agent_cli.py
python D:\codex-tasks\dwg_agents_ops\agent_control\monitor_cli.py
```

## 注意事项

- 四个角色默认要求显式配置自己的接口，不再共享全局模型配置。
- 本目录只负责“协作层”，不会替代 `cad/system` 的统一连接规则。
- 涉及 CAD 真机操作时，仍应优先复用 `system.licad.C`、`CAD_selection.py`、`CAD_coordination.py`、`content_analysis_dwg_file.py`。
- `Runtime_Guard_Agent` 当前阶段默认采用本地事件驱动，不应被设计为每几秒调用一次远程模型的高耗轮询器。
- 当任务进入真实 CAD / 打印执行时，`Runtime_Guard_Agent` 的合理职责不应只限于环境报警，还应督导：
  - 每 DWG 收尾后的环境归一
  - 执行者是否明确受控入口与恢复入口
  - 执行者是否遵守关键规则与输出契约
