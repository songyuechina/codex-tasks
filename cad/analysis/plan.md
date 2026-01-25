# CAD 自动化脚本优化与测试计划（待审批）

## 目标
- 在不破坏现有生产流程的前提下，提高稳定性、可测试性与可维护性。
- 将高风险函数先行梳理并隔离，逐步引入单元测试与集成测试。
- 统一 CAD 连接与文件操作流程，降低重复定义与不一致行为。

## 约束/假设
- 目前不改动代码，仅提交分析与计划；改动需你审批后执行。
- AutoCAD/Tianzheng 依赖 COM，测试必须区分“纯函数单测”与“CAD集成测”。
- 现有脚本中存在大量 UI 自动化与窗口操作，需在可控环境下执行。

## 当前发现（摘要）
- licad.py / CAD_coordination.py 存在函数重复定义，后者覆盖前者（潜在行为不一致）。
- CAD_basic.py 为历史巨型模块，与 library/* 的拆分存在功能重复。
- 多处使用全局单例（C.acad/doc/mp/sp）与全局副作用（print 替换、日志热替换）。
- 大量函数依赖 COM/窗口/进程，测试需要隔离或打桩。

## 分阶段计划
### Phase 0：基线与可回滚保障
- 确认使用的入口脚本与生产路径（例如 CAD_System_Queue / Master_Orchestrator）。
- 标记“只读/只分析”阶段结束节点，设置回滚基线。

### Phase 1：一致性修复与结构化
- 统一核心入口：明确 CAD_basic vs library 的来源优先级。
- 修复重复定义（get_acad_doc / wait_quiescent 等）并保留清晰版本号。
- 将高风险函数集中到单一模块，建立“稳定API层”。

### Phase 2：可测试性改造
- 为纯算法函数（cad_geometry/cad_objects）抽离 COM 依赖，允许纯输入输出测试。
- 为 COM 相关函数增加“依赖注入”接口（如 doc/mp 作为参数）。
- 引入轻量 Mock 层用于模拟 CAD COM 行为（选择集、对象属性）。

### Phase 3：测试体系构建
- 单元测试：几何算法、数据处理、路径计算、名称解析等纯函数。
- 集成测试：关键 CAD 操作（open/new/save/insert/selection）。
- 运行策略：提供“无CAD环境可运行”的最小测试集 + “CAD环境专用”集。

## 测试矩阵（初稿）
- 纯函数：cad_geometry, cad_objects, execution_result
- COM 接口：licad, CAD_coordination, CAD_basic_operations, CAD_selection
- 业务流程：Insert_chart/insert_labels, Master_Orchestrator, CAD_System_Queue

## 风险控制
- 每次改动前自动备份被修改文件。
- 核心流程先写“旁路验证”（不修改生产路径）。
- 所有对 CAD 的写操作必须在测试文件中执行。

## 交付物
- cad/analysis/notes.md：持续分析记录（中文）
- cad/analysis/review.md：函数级审查清单（自动 + 人工复核）
- cad/analysis/plan.md：本计划（待审批）
