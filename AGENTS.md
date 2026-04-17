# AGENTS.md

适用范围：`D:/codex-tasks/`

本文件用于指导 Codex 等命令行智能体理解并操作整个 `codex-tasks` 项目。  
目标不是让智能体机械继承旧代码形式，而是让它迅速理解系统骨架、核心经验、稳定核心、重构边界，并在规则约束下完成高质量修改与重构。

本项目当前已经进入“项目总管 + 四角色智能体能力层 + 领域执行工作区 + 运行监督链”的结构。

## 0. 新智能体首读协议

任何刚进入 `D:/codex-tasks/` 的新智能体，不应直接从源码或局部脚本开始。

必须先读：

1. `folder.meta.json`
2. `thoughtway/PROJECT_SUPERVISOR_ARCHITECTURE.md`
3. `thoughtway/CURRENT_STATE.md`
4. `thoughtway/TERMINOLOGY.md`
5. 再继续阅读本文件 `AGENTS.md`

目的：

- 先建立项目总图
- 先知道当前工作进行到哪里、下一步建议做什么
- 先明确项目总管、四角色能力层、领域执行工作区、运行监督链的关系
- 避免把 `dwg_agents_ops/` 误判为项目总管本体
- 避免把 `print/` 误判为孤立脚本集合
- 避免忽略 `cad_runtime_guard.py + Runtime_Guard_Agent` 的监督链设计

若未完成上述首读，不应直接判定系统架构，也不应直接开始真实 CAD / 打印任务。

含义如下：

- 运行在 `C:\Users\User` 下的通用 Codex，仍可作为跨项目总管
- 但进入 `D:/codex-tasks/` 工作时，应把这里视为“项目总管工作区”
- 项目级知识、规划、协调、经验、规则，应优先沉淀在 `D:/codex-tasks/` 内，而不是继续散落在用户主目录

特别是：

- `thoughtway/` 负责沉淀项目级思想、系统知识、治理规则、经验记录
- `dwg_agents_ops/` 负责角色化协作层
- `cad/system/` 负责统一连接、执行内核与运行监督底座
- 各业务目录可继续建设自己的领域执行工作区，例如：
  - `cad/scripts/drawing_basic_service/print/` 作为打印执行工作区

---

# 1. 项目总目标

本项目的核心目标，不是为人手工点击 CAD，而是为 **本地运行的智能体** 建立一个稳定、可修改、可验证的 DWG / CAD 操作系统。

智能体在本项目中工作的最高原则是：

1. 迅速理解系统骨架  
2. 迅速定位关键函数与关键脚本  
3. 在规则约束下复用或重构脚本  
4. 保留已被实践验证有效的经验  
5. 通过案例、快照、结果验证来确认修改是否成立  

---

# 2. 目录结构理解

当前顶层结构：

- `cad/`  
  驱动天正 CAD 系统的核心脚本目录，是当前最重要的运行环境层。

- `dwg_cases/`  
  DWG 案例资产系统，用于典型案例、真实案例、验证与对照。

- `dwg_agents_ops/`  
  面向 DWG 作业的智能体运行 / 修正 / 反馈层。

- `dwg_system_tools/`  
  面向 DWG 系统控制的工具层，如分析、索引、状态差异、meta 生成等。

- `thoughtway/`  
  项目的思想方法、规则文件、元规则、参考资料。

---

# 3. 首先阅读什么

进入项目后，优先阅读：

1. `folder.meta.json`
2. `thoughtway/PROJECT_SUPERVISOR_ARCHITECTURE.md`
3. `thoughtway/CURRENT_STATE.md`
4. `thoughtway/TERMINOLOGY.md`

若只是为了快速接手当前项目，不要先读完整清单，先完成上面 4 个文件即可。

完成最短接手后，再继续扩展阅读：

5. `thoughtway/PROJECT_GOVERNANCE.md`
6. `thoughtway/SYSTEM_FOUNDATIONS.md`
7. `thoughtway/PROJECT_MEMORY_SYSTEM.md`
8. `thoughtway/meta_json_principles.md`
9. `thoughtway/functions_scripting_rules/01_bootstrap_import_rules_v2.md`
10. `thoughtway/functions_scripting_rules/02_logging_rules_v2.md`
11. `thoughtway/functions_scripting_rules/03_entry_script_rules_v2.md`
12. `thoughtway/functions_scripting_rules/04_business_module_rules_v2.md`
13. `thoughtway/functions_scripting_rules/05_exception_handling_rules_v2.md`
14. `thoughtway/functions_scripting_rules/06_cad_connection_rules_licad_C_v2.md`
15. `thoughtway/CAD_RUNTIME_GUARD_RULES.md`

然后进入：

16. `dwg_agents_ops/README.md`
17. `dwg_agents_ops/agent_control/UNIFIED_CONTROL.md`
18. `dwg_agents_ops/agent_control/RUNTIME_EVENT_PROTOCOL.md`
19. `cad/system/folder.meta.json`
20. `cad/system/README.md`
21. `cad/scripts/drawing_basic_service/print/folder.meta.json`
22. `cad/scripts/drawing_basic_service/print/README.md`

之后按 `cad/system/README.md` 的推荐顺序继续阅读：

- `licad.py`
- `CAD_selection.py`
- `common_logger.py`
- `CAD_com_utils.py`
- `CAD_coordination.py`
- `CAD_core.py`
- `content_analysis_dwg_file.py`
- `cad_command_monitor.py`
- `cad_dialog_killer.py`
- `project_setup.py`

凡是涉及真实 CAD / DWG / 打印任务，开始执行前还必须先明确两件事：

1. 本次使用哪个受控入口启动 / 连接天正 CAD
2. 若检测到纯 CAD 或疑似非天正环境，将走哪个恢复入口

若这两件事未被明确，不应直接开始操作 DWG。

对于打印任务，还必须再明确第三件事：

3. 当前是否处于“项目总管调度打印主链 + 运行监督链并行监督”的监督版架构下

若当前架构未被明确，不应把打印主链误判为裸执行脚本。

凡是涉及真实 CAD / DWG 的测试、回归、烟测，还必须再明确第四件事：

4. 本次测试文件是否统一放在 `D:/codex-tasks/cad/tests/`

若测试资产散落在临时目录、用户桌面或脚本私有目录，不应视为符合本项目规则。

---

# 4. 关于 meta.json 的根本理解（已升级为四层结构）

本项目现在采用 **四层 meta 结构**，而不是只做两层。

## 4.1 脚本级 meta
- `A_quote.meta.json`
- `A_procedure.meta.json`

作用：
- 快速知道脚本角色
- 快速知道 public_api
- 快速知道脚本整体 workflow
- 快速知道关键依赖、边界与不可丢失经验

## 4.2 函数级 meta
- `A_functions.quote.meta.json`
- `A_functions.procedure.meta.json`

作用：
- 覆盖脚本中的全部函数
- 快速知道每个函数的功能目标
- 快速知道输入输出与返回结构
- 快速知道函数的大流程
- 支撑后续修改、替换、重构与定位

## 4.3 根本原则
- 脚本级 meta 负责“先抓骨架”
- 函数级 meta 负责“进入函数控制层”
- meta 是压缩骨架，不是源码替身
- 修改前应先看脚本级 meta，再按需要进入函数级 meta

## 4.4 关于函数级 meta 的准确度
函数级 meta 的目标是整体可用、整体覆盖，不是逐条绝对完美。  
允许：

- 局部不准确
- 局部粗糙
- 局部低置信度推断

但要求：

- 尽量不要漏函数
- 简单函数简写
- 复杂函数适度展开
- 不确定内容写入 `quality.todo`

---

# 5. cad/system 的骨架共识

`cad/system` 是当前项目最关键的系统骨架。  
其中：

## 高价值稳定核心
- `licad.py`
- `CAD_selection.py`

这两个脚本非必要不整体重写。  
允许局部修补、补充、去重，但不应轻率整体推翻。

## 过渡性核心
- `CAD_core.py`
- `CAD_coordination.py`
- `CAD_com_utils.py`
- `common_logger.py`
- `content_analysis_dwg_file.py`

这些脚本允许继续收束、拆分、减耦合，但必须保留已经被实践验证有效的经验。

## 守护脚本
- `cad_command_monitor.py`
- `cad_dialog_killer.py`

这两个脚本属于独立守护脚本，不是普通业务模块。

## 纯配置层
- `project_setup.py`

它只负责路径常量配置，不再承担 bootstrap 或连接职责。

---

# 6. 强制规则

## 6.1 连接规则
所有 CAD 主连接原则上统一通过：

```python
from system.licad import C
```

进行。

禁止业务层长期分散使用：
- `GetActiveObject`
- `Dispatch`
- 裸 `SendCommand`
- 各自维护的 app/doc 全局缓存

## 6.2 日志规则
业务脚本统一使用：

```python
from system.common_logger import sys_logger
```

并使用：
- `debug`
- `info`
- `warning`
- `error`
- `critical`

普通业务模块禁止大量 `print()`。

## 6.3 引导规则
bootstrap / `sys.path` 引导只由入口脚本负责。  
库模块禁止内部随意修改 `sys.path`。  
当前项目中残留的旧式引导属于历史兼容痕迹，不是未来标准。

## 6.4 异常规则
对 CAD / COM 这类高不稳定接口：

- 可将短时异常视为 busy / blocked
- 允许等待与重试
- 必要时执行环境重建、自愈、回滚
- 但不能把真正致命错误无限吞掉

## 6.5 测试资产规则
真实 CAD / DWG 测试、回归、烟测所使用的文件，默认统一放在：

- `D:/codex-tasks/cad/tests/`

原则：

- 临时测试 DWG 优先落在 `cad/tests/`
- 测试前若会改写原文件，应优先放入 `cad/tests/备份/`
- 不再把测试文件散落到 `temp`、用户桌面或各业务目录私有角落

## 6.6 运行监督链规则
凡是真实 CAD / DWG 执行，不仅是打印任务，默认都应同时运行：

- `D:/codex-tasks/cad/system/cad_runtime_guard.py`

推荐做法：

- 通过 `CAD_core.launch_cad_guardians()` 统一挂载守护脚本组
- 至少在关键节点读取 runtime guard 状态或事件
- 若 guard 给出 `pause_and_verify / pause_and_recover`，不得无视继续推进

## 6.7 cuabot 容器中的宿主机 CAD 控制规则
当工作环境是 `cuabot codex`（Linux 容器）时：

- 容器内可以直接读取 `/home/user/mnt/c/...`、`/home/user/mnt/d/...` 对应的宿主机文件。
- 但本地天正/CAD 的真实控制必须通过宿主机桥接命令 `cad-host` 完成。
- 禁止在 `cuabot` 容器里把本地 Windows 天正 CAD 误判为容器内 GUI 应用。
- 优先使用：
  - `cad-host inspect-runtime`
  - `cad-host launch`
  - `cad-host recover`
  - `cad-host open-file <path>`
  - `cad-host save`
  - `cad-host close`
- `cad-host` 接受容器路径，例如：
  - `/home/user/mnt/d/codex-tasks/...`
  - 桥接层会自动换算成宿主机 Windows 路径再交给 `CAD_core.py`
- 若任务目标是“后台控制本地天正 CAD 且尽量不抢鼠标键盘”，默认优先走 `cad-host + CAD_core.py`，不要先设计新的 GUI 鼠标自动化方案。

## 6.8 cuabot 容器中的项目脚本执行规则
当任务不只是 `CAD_core.py` 级别动作，而是需要调用 `D:/codex-tasks/` 下的项目脚本时：

- 代码阅读、改代码、搜索、整理输出，仍优先在容器内直接对 `/home/user/mnt/d/codex-tasks/...` 操作。
- 但凡脚本真实依赖宿主机 Windows / 天正 / AutoCAD / COM / WPS / 打印机，就不要直接在容器 Linux Python 里运行。
- 统一改用宿主机桥接命令 `task-host` 发起执行。
- `task-host` 的执行根目录固定受控在 `D:/codex-tasks/`。
- `task-host` 接受容器路径，例如：
  - `/home/user/mnt/d/codex-tasks/cad/scripts/drawing_basic_service/print/print_runner.py`
  - 桥接层会自动换算成宿主机 Windows 路径，再由宿主机 Python / PowerShell 执行。
- 对项目脚本的默认判断如下：
  - 纯文件读写、纯文本处理、纯仓库分析：可直接在容器内执行。
  - 依赖 CAD / COM / 宿主机桌面软件的脚本：必须经 `task-host` 或 `cad-host` 执行。
- 典型命令：
  - `task-host project-root`
  - `task-host python /home/user/mnt/d/codex-tasks/cad/scripts/drawing_basic_service/print/print_runner.py -- --dwg /home/user/mnt/d/.../xxx.dwg`
  - `task-host python /home/user/mnt/d/codex-tasks/cad/scripts/drawing_basic_service/print/print_batch_dispatch.py -- --input-dir /home/user/mnt/d/...`
  - `task-host pwsh /home/user/mnt/d/codex-tasks/.../some_script.ps1 -- ...`
- 这样做的目标是：
  - 智能体仍隔离在容器中工作
  - 代码和 DWG 仍然落在本地 `D:/codex-tasks`
  - 真实 Windows 能力继续在宿主机执行
  - 尽量不抢本地鼠标键盘

---

# 7. 如何判断“该复用、该修补，还是该重构”

## 应优先复用
当已有脚本已经：
- 解决了真实顽疾
- 被多次实测验证
- 只是命名或结构稍乱

## 应局部修补
当已有函数核心经验正确，但存在：
- 日志不规范
- 局部兼容分支混乱
- 参数组织不佳
- 旧桥接未切断

## 应重构
当脚本：
- 角色已经混乱
- 同时承担多个层级职责
- 旧桥接严重阻碍后续扩展
- 但其核心经验仍值得保留

原则：  
**可以重写函数形式，但不能丢掉有效经验。**

---

# 8. 搜索与定位策略

搜索代码、函数定义、引用关系时，优先使用快速文本搜索工具。  
优先级：

1. `rg`
2. `rg --files`
3. 必要时辅以 Python 小脚本做结构分析

原则：

- 先用 `README.md` 和脚本级 meta 确定范围
- 再用文本搜索查真实定义点与调用点
- 需要函数细节时，再进入函数级 meta
- 最后再深入源码

不要盲目从整个仓库全文通读开始。

---

# 9. 修改前后的工作方式

## 修改前
1. 先确认脚本层级与角色
2. 先看 README 与脚本级 meta
3. 再看函数级 meta
4. 再定位真实源码
5. 再搜索调用链与依赖链
6. 明确哪些经验不能丢

## 修改时
1. 尽量最小化破坏面
2. 日志路径清楚
3. 失败路径清楚
4. 保留兼容边界说明
5. 不把新职责继续堆进错误层级

## 修改后
1. 用案例或快照验证
2. 检查是否破坏统一连接规则
3. 检查是否破坏日志规则
4. 检查是否误动高价值稳定核心
5. 记录必要的 meta / README 变化

---

# 10. 对智能体的特别提醒

## 10.1 不要误判“旧代码 = 无价值”
很多核心经验恰恰存在于旧代码中。

## 10.2 不要误判“脚本很多 = 必须全部推翻”
真正需要保留的是系统中经过实践磨炼的经验。

## 10.3 不要把 README / meta 当成装饰品
它们是帮助你快速抓住系统骨架与函数控制层的第一入口。

## 10.4 不要轻率重写以下脚本
- `licad.py`
- `CAD_selection.py`

## 10.5 若有冲突
优先遵守：
1. 项目规则文件
2. `cad/system/README.md`
3. 脚本级 meta
4. 函数级 meta
5. 源码中的真实实现细节

---

# 11. 新主管进入后必须立即能回答的问题

1. 当前项目总管工作区是不是 `D:/codex-tasks`
2. `dwg_agents_ops/` 是不是项目总管本体
3. 当前第一优先级领域是不是 `cad/scripts/drawing_basic_service/print/`
4. 打印主链是不是在 `cad_runtime_guard.py + Runtime_Guard_Agent` 的监督下推进
5. 真正进入脚本细节前，是否已经先读完目录级 `folder.meta.json`、架构文档和基础治理文档

# 12. 当前最重要的一句话

> 这个项目的目标不是保存旧代码原样，而是让智能体能够在规则、骨架、函数级概括、案例和经验的支持下，迅速理解系统、迅速定位函数、迅速完成高质量重构。
