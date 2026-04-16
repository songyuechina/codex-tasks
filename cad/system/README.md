# README.md

`D:/codex-tasks/cad/system`

---

# 1. 文件夹定位

`cad/system` 是整个 `codex-tasks` 中面向 **CAD / DWG 自动化控制** 的核心系统脚本目录。

它不是面向人工 GUI 操作的零散工具箱，而是面向 **命令行、本地运行的 agent 智能体** 的基础系统层。  
它为智能体提供：

- CAD 统一连接
- 对象选择与属性访问
- 基础文件控制
- 同步协调与事务保护
- 日志与测试记录
- DWG 内容分析与快照验证
- 守护脚本（弹窗关闭 / 命令超时打断）

---

# 2. 当前主骨架分层

## A. 统一连接入口层
### `licad.py`
定位：整个系统的统一 CAD / DWG 连接入口。  
核心：`C` 代理对象、`li()` 智能连接刷新、`SafeDocumentWrapper`、`doc/raw_doc` 分层语义。

这是高价值稳定核心。  
原则上，业务层不应绕过它直接长期使用 `GetActiveObject / Dispatch`。

## B. 选择与对象研究层
### `CAD_selection.py`
定位：选择、类型转换、当前空间过滤、可视化选中、标准 CAD / 天正对象属性访问核心。  
核心：`ss_select`、`current_space_only`、`_maybe_cast`、天正 `DISPID` 属性映射。

这是高价值稳定核心。  
它承载了大量经过实践磨炼的对象访问经验，不宜轻率整体重写。

## C. 基础控制与文件操作层
### `CAD_core.py`
定位：CAD 基础控制、文件操作、状态归一、跨文件操作核心。  
核心：新建/打开/保存/关闭、`litz()` 环境重建、状态归一、跨文件插入、路径修复。

这是当前系统中的基础控制核心，但仍带有历史兼容桥接痕迹。  
可继续收束和拆分，但必须保留已被实践验证有效的经验。

## D. 协同与保护层
### `CAD_coordination.py`
定位：基于 `licad.C` 的高层协同层。  
负责等待空闲、事务守卫、文件回滚、安全执行循环、命令同步。  
它不负责 CAD 主连接，而是建立在 `licad.py` 之上。

## E. COM busy / retry 辅助层
### `CAD_com_utils.py`
定位：专注处理 CAD COM 调用中的 `busy / rejected / temporary block` 问题。  
核心：`retry_on_busy`、`retry_if_busy`、`SafeCOM`、`silent_mode`、`timeit`。  
它不是主连接入口，不应再扩张成历史式大杂烩辅助模块。

## F. 统一日志与记录层
### `common_logger.py`
定位：整个 `cad/system` 的统一日志系统与关键区段记录模块。  
核心：`sys_logger`、`set_debug_mode`、`record_test_result`、`checkpoint`、`CriticalSection`。

## G. 内容分析与验证层
### `content_analysis_dwg_file.py`
定位：DWG 内容分析、快照持久化、数据库复用、摘要查询脚本。  
核心：`CAD_AUDIT` 数据库、`get_cad_state`、`get_dwg_graphics_summary`、`counts_by_type`、`counts_by_space`、`digest`、按需 handle 采集。

## H. 纯路径配置层
### `project_setup.py`
定位：纯路径常量配置模块。  
只保留 `PathConfig` 与路径常量，不再承担 `sys.path` 引导或导入环境构建职责。

## I. 独立守护层
### `cad_command_monitor.py`
命令超时监控守护脚本。处理命令行卡死、等待输入停滞、抢焦点后 ESC 打断。

### `cad_dialog_killer.py`
弹窗关闭守护脚本。处理 CAD 标准对话框阻塞，支持延迟关闭与单实例守护。

### `cad_runtime_guard.py`
运行环境守护脚本。被动检测当前活动 CAD 是否仍处于可信天正运行环境，并输出结构化状态/告警。

### `cad_test_supervisor.py`
测试期被动监督脚本。用于在真实函数测试期间持续观察：

- `acad.exe` 数量是否超过允许阈值（默认 2）
- `cad_dialog_killer.py` 是否已经在运行

它不负责启动 CAD，也不负责恢复 CAD，只做测试护栏与违规上报。

---

# 3. 当前确认的 11 个正式脚本

1. `CAD_com_utils.py`
2. `cad_command_monitor.py`
3. `CAD_coordination.py`
4. `CAD_core.py`
5. `cad_dialog_killer.py`
6. `cad_runtime_guard.py`
7. `CAD_selection.py`
8. `common_logger.py`
9. `content_analysis_dwg_file.py`
10. `licad.py`
11. `project_setup.py`

---

# 4. 当前系统中的稳定核心

- `licad.py`
- `CAD_selection.py`

这两个脚本允许局部修补，但不宜轻率整体推翻。

---

# 5. 当前系统中的过渡性核心

- `CAD_core.py`
- `CAD_coordination.py`
- `CAD_com_utils.py`
- `common_logger.py`
- `content_analysis_dwg_file.py`

这些模块可以继续拆分和收束，但必须保留核心经验。

---

# 6. meta 体系（已升级为四层结构）

本目录当前采用 **四层 meta 结构**。

## 6.1 脚本级引用层
- `A_quote.meta.json`

作用：
- 让智能体快速知道脚本角色
- 快速知道 public_api
- 快速知道关键约束与边界
- 快速知道与谁协作

## 6.2 脚本级流程层
- `A_procedure.meta.json`

作用：
- 让智能体快速知道脚本整体 workflow
- 快速知道典型使用方式
- 快速知道入口函数的大流程
- 快速知道资源边界

## 6.3 函数级引用层
- `A_functions.quote.meta.json`

作用：
- 覆盖脚本中的全部函数
- 给出每个函数的功能目标
- 给出输入参数、输出与返回结构
- 给出副作用、依赖与风险等级的概括

## 6.4 函数级流程层
- `A_functions.procedure.meta.json`

作用：
- 覆盖脚本中的全部函数
- 给出每个函数的步骤概括
- 给出失败路径、成功条件与必须保留经验
- 让智能体在不立刻啃源码的情况下先抓住函数流程骨架

## 6.5 四层结构的分工

### 脚本级 meta
负责：
- 先抓骨架
- 快速知道脚本是什么
- 快速知道脚本在整个系统中处于什么层级

### 函数级 meta
负责：
- 进入每个函数的控制层
- 快速知道函数做什么
- 快速知道函数输入输出和大流程
- 支撑后续定位、修改和重构

## 6.6 关于函数级 meta 的准确度
函数级 meta 的目标不是逐条绝对精准，而是：

- 尽量覆盖全部函数
- 简单函数简写
- 复杂函数适度展开
- 局部不确定写入 `quality.todo`
- 整体完成优先于局部完美

---

# 7. 智能体工作原则

- 不把旧代码形式当最高权威
- 真正应继承的是项目思想、系统规则、已验证经验、案例与校验标准
- 脚本级 meta 用来快速抓总骨架
- 函数级 meta 用来快速进入具体函数控制层
- 可以重构，但不能乱重构

---

# 8. 与 thoughtway / meta_gen 规则文件的关系

`cad/system` 内所有脚本原则上应服从：

- `01_bootstrap_import_rules.md`
- `02_logging_rules.md`
- `03_entry_script_rules.md`
- `04_business_module_rules.md`
- `05_exception_handling_rules.md`
- `06_cad_connection_rules_licad_C.md`
- `dwg_system_tools/meta_gen/META_RULES.md`

若脚本现状与规则冲突：
- 以规则为未来收束方向
- 对高价值稳定核心，允许保留部分历史实现，逐步推进

---

# 9. 推荐阅读顺序

## 第一层：总览
1. `README.md`

## 第二层：脚本级骨架
2. 对应脚本的：
   - `A_quote.meta.json`
   - `A_procedure.meta.json`

## 第三层：函数级骨架
3. 对应脚本的：
   - `A_functions.quote.meta.json`
   - `A_functions.procedure.meta.json`

## 第四层：真实实现
4. 脚本源码本体

## 第五层：补充验证
5. 调用链 / 引用链搜索
6. 案例 / 快照 / 结果验证
7. 若涉及运行守护，再阅读：
   - `CAD_RUNTIME_GUARD_PROTOCOL.md`

---

# 10. 当前不建议做的事

- 不要轻率整体推翻 `licad.py`
- 不要轻率整体推翻 `CAD_selection.py`
- 不要把新的杂项职责继续堆进 `CAD_core.py`
- 不要把 `CAD_com_utils.py` 再次扩张成大杂烩
- 不要把 `project_setup.py` 再变回引导脚本
- 不要让守护脚本伪装成普通业务模块
- 不要把脚本级 meta 写成函数说明大全
- 不要让函数级 meta 因为追求完美而停工

---

# 11. 当前最重要的系统共识

> `cad/system` 不是为了给人手工点按钮，而是为了给本地运行的智能体建立稳定、可修改、可验证的 DWG/CAD 操作内核。

真正的目标是：

- 让智能体迅速定位脚本
- 让智能体迅速理解脚本骨架
- 让智能体迅速进入函数控制层
- 让智能体在规则约束下快速修正和重构
- 让案例验证与快照分析能支撑持续迭代
