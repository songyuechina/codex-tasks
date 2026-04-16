# System Foundations

本文件用于沉淀 `D:/codex-tasks` 中最基础、最不应被遗忘的系统知识。

这些知识不是某一轮任务的偶然结论，而是整个 DWG / CAD 自动化系统的底层共识。

项目治理、术语与总管关系，另见：

- `D:/codex-tasks/thoughtway/PROJECT_GOVERNANCE.md`
- `D:/codex-tasks/thoughtway/TERMINOLOGY.md`

## 1. 统一连接入口

- 文件：`D:/codex-tasks/cad/system/licad.py`
- 核心对象：`C`、`C.doc`、`C.raw_doc`

作用：

- 建立和刷新 CAD / 天正连接
- 区分安全包装文档和原始文档
- 作为整个系统默认的 CAD 连接入口

基本原则：

- 默认通过 `from system.licad import C` 连接 CAD
- 不要在业务层分散使用 `GetActiveObject`、`Dispatch`、裸 `SendCommand`

## 2. 文件级控制与基础操作

- 文件：`D:/codex-tasks/cad/system/CAD_core.py`

作用：

- 启动和控制 CAD 环境
- 新建、打开、保存、关闭 DWG
- 处理复制、插入、跨文件操作等文件级动作

## 3. 选择与对象访问

- 文件：`D:/codex-tasks/cad/system/CAD_selection.py`

作用：

- 高效选择对象
- 获取和设置适合早期绑定的对象属性
- 支持模型空间 / 图纸空间对象筛选
- 支持标准 CAD 与天正对象访问

## 4. COM busy / rejected 处理

- 文件：`D:/codex-tasks/cad/system/CAD_com_utils.py`

作用：

- 解决 CAD COM 调用中的 busy / rejected / temporary block 问题
- 提供重试、静默期、包装调用等能力

## 5. 命令同步与协调保护

- 文件：`D:/codex-tasks/cad/system/CAD_coordination.py`

作用：

- 解决命令发送后的延迟、不同步、未稳定就进入下一步的问题
- 提供等待空闲、命令同步、事务保护、文件回滚等能力

## 6. 弹窗干扰处理

- 文件：`D:/codex-tasks/cad/system/cad_dialog_killer.py`

作用：

- 处理运行中出现的 CAD 标准对话框干扰
- 降低弹窗阻塞自动化流程的概率

## 7. 命令卡死监控

- 文件：`D:/codex-tasks/cad/system/cad_command_monitor.py`

作用：

- 解决测试和实际运行中 CAD 命令被卡死的问题
- 在命令长时间无响应时进行监控和打断

## 8. 运行监督链

- 文件：`D:/codex-tasks/cad/system/cad_runtime_guard.py`
- 桥接：`D:/codex-tasks/cad/system/runtime_guard_bridge.py`
- 协作对象：`D:/codex-tasks/dwg_agents_ops/Runtime_Guard_Agent/`

作用：

- 对活动 CAD 环境持续做被动观察
- 输出结构化状态、事件与监督结论
- 让打印等真实执行链在风险出现时可以暂停、核验、恢复或回滚

基础原则：

- 真实 CAD / 打印任务不应把监督链视为可有可无
- 业务链发现 `warning / critical` 时，应先读取监督状态再决定是否继续
- 监督链是执行保护层，不替代业务编排层

说明：

- `Runtime_Guard_Agent/` 是历史目录名保留
- 当前概念上应理解为本地监督对象/监督入口，不属于四角色智能体

## 9. DWG 内容分析与行为核验

- 文件：`D:/codex-tasks/cad/system/content_analysis_dwg_file.py`

作用：

- 分析任意 DWG 文件内容
- 对函数执行前后进行内容对比
- 帮助判断函数实际作用，而不是只靠代码猜测

## 10. 高层业务函数库

- 目录：`D:/codex-tasks/cad/library/`

作用：

- 提供图块、文字、几何、对象、数据库、天正建筑等更高层业务函数

约束：

- 基于 `pywin32` 的 CAD 业务函数应默认只操作单一、已启动的 CAD 进程
- 业务函数层不得自行启动 CAD、重建 CAD，或放任多 CAD 进程并发存在
- 若运行时未预先就绪，应该报错并交还给独立受控入口处理

## 11. 总哲学

这套系统的默认哲学是：

- 优先继承已有框架与历史经验
- 通过函数、脚本、文件夹持续沉淀未来经验
- 不因局部问题就轻率抛弃已有体系
- 只有遇到特别困难时，才允许临时跳出框架独立求解

## 12. 对智能体的要求

任何进入本项目的上层智能体或脚本调度者，都应尽量先掌握本文件所列知识，再进入局部任务实现。
