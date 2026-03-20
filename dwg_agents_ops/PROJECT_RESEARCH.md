# 项目研究纪要

## 1. 项目总目标

`D:/codex-tasks` 的核心目标不是“帮人点 CAD”，而是构建一套面向本地智能体的 DWG / CAD 操作系统，使智能体能够：

- 稳定连接天正 / AutoCAD
- 读取、选择、修改、绘制图元
- 执行文件级打开/保存/关闭/跨文件操作
- 通过快照、数据库和案例校验结果
- 在规则约束下持续重构和扩展

当前更贴近业务的落地方向，是为建筑施工图自动化提供基础服务能力，例如插图签、编目录、打印、内容分析、对象处理等。

## 2. 当前已完成成果

### 2.1 CAD 内核已具备主体能力

`cad/system/` 已形成 10 个正式脚本和较完整的分层：

- `licad.py`：统一连接入口，提供 `C` 代理、`doc/raw_doc` 分层、自愈重连。
- `CAD_selection.py`：选择引擎、对象类型转换、空间过滤、天正属性访问。
- `CAD_core.py`：文档新建/打开/保存/关闭、环境重建、跨文件操作等基础控制。
- `CAD_coordination.py`：等待空闲、事务保护、文件回滚、同步命令发送。
- `CAD_com_utils.py`：COM busy / rejected 重试与静默模式。
- `common_logger.py`：统一日志与测试记录。
- `content_analysis_dwg_file.py`：DWG 内容采集、摘要、digest、数据库持久化。
- `cad_command_monitor.py`：命令卡死监控守护。
- `cad_dialog_killer.py`：弹窗关闭守护。
- `project_setup.py`：纯路径配置。

这些模块的根本分工已另外固化到：

- `D:/codex-tasks/thoughtway/SYSTEM_FOUNDATIONS.md`

从源码规模看，`cad/system` 已经不是原型：

- `CAD_core.py` 约 2597 行，54 个顶层函数。
- `CAD_selection.py` 约 984 行，46 个顶层函数。
- `licad.py` 约 392 行，含 17 个类方法。
- `content_analysis_dwg_file.py` 约 1144 行。

### 2.2 业务函数库体量已很大

`cad/library/` 已沉淀大批业务函数：

- `cad_blocks.py` 4370 行
- `cad_control.py` 3357 行
- `Databaseoperation.py` 3493 行
- `cad_objects.py` 2748 行
- `cad_geometry_segment.py` 1939 行
- `cad_geometry_polyline.py` 1539 行
- `tarch_building.py` 1531 行

### 2.3 meta 工具链已经成型

`dwg_system_tools/meta_gen/` 已具备：

- `META_RULES.md`
- `META_SCHEMA.json`
- `meta_pipeline.py`
- `meta_validator.py`

`cad/system/` 已生成脚本级和函数级 meta，共 40 份以上 `.meta.json`。

### 2.4 案例与真实 DWG 资产已存在

`dwg_cases/content_analysis_dwg_file/` 内已有真实 DWG / DXE / bak 文件，可用于内容分析、对照和验证。

## 3. 当前缺口和风险

### 3.1 多智能体协作层目前是空的

当前工作区中的 `dwg_agents_ops/` 为空目录，但 git 历史显示项目曾经有过：

- `Planner_Agent`
- `Implementer_Agent`
- `Reviewer_Agent`
- `Tester_Agent`

### 3.2 旧版多智能体骨架存在结构问题

- 四个角色几乎复制同一份 `agent_cli.py`
- 角色 README 对控制目录路径描述不一致
- API 配置主要依赖通用环境变量，无法自然支持三角色不同 endpoint / key / model
- 任务板和配套文档大多还是空壳

### 3.3 测试资产在当前工作区缺失严重

`git status` 显示 `cad/tests/` 与旧 `dwg_agents_ops/` 在当前工作区被大面积删除，这意味着当前工作区虽保留了核心内核，但“测试层”和“协作层”明显不完整。

### 3.4 `CAD_AUDIT.sqlite` 目前为空

当前仓库根目录下的 `CAD_AUDIT.sqlite` 文件大小为 0，尚未形成可复用的持久快照数据集。

### 3.5 有些知识必须被视为“系统常识”

以下信息不应只存在于某个子任务或某次对话中：

- `CAD_com_utils.py` 负责处理 CAD 忙和 COM busy
- `CAD_coordination.py` 负责解决命令延迟、不同步和保护性协调
- `cad_dialog_killer.py` 负责处理运行中的窗口干扰
- `cad_command_monitor.py` 负责处理 CAD 命令卡死
- `content_analysis_dwg_file.py` 负责分析 DWG 内容并支持前后对比核验

这些基础认知已经被整理进：

- `D:/codex-tasks/thoughtway/SYSTEM_FOUNDATIONS.md`

## 4. 本轮建议方向

### 4.1 先重建三角色，不再保留四角色

当前最合适的角色集合是：

- `Coder_Agent`
- `Reviewer_Agent`
- `Tester_Agent`

### 4.2 每个角色必须独立 provider 配置

这次要直接满足：

- 不同接口网址
- 不同密钥
- 不同模型 ID

### 4.3 共享运行时抽离

旧版最大的工程问题是重复代码。新版本应把会话存储、任务板读取、运行时状态心跳、单次/交互式调用、输出文件写入统一放到 `dwg_agents_ops/shared/runtime.py` 中。
