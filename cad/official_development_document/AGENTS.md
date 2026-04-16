# AGENTS.md

适用范围：`D:/codex-tasks/cad/official_development_document/`

本目录不是普通参考资料堆，而是供 Codex 快速检索、拼装并验证 `pywin32` 操作 CAD 方法的本地知识系统。

## 1. 进入本目录后的首读顺序

必须先读：

1. `folder.meta.json`
2. `README.md`
3. `00_readme/README_Codex_Workflow.md`
4. `00_readme/PROMOTION_POLICY.md`
5. `07_validation/hotspot_candidates.json`

目的：

- 先知道这里的主入口不是 CHM 原目录
- 先知道检索顺序和方法构建顺序
- 先知道哪些低频对象已经开始变热
- 避免直接回到原始 HTML 手翻

## 2. 本目录的真实目标

本目录用于让 Codex 在接到以下任务时，能快速建立一个可执行的 `pywin32` CAD 方法：

- 连接 CAD / 获取活动文档
- 布局与空间切换
- 选择与对象遍历
- 块与属性读取/写入
- 布局打印与打印窗口控制
- SendCommand 回退

“建立方法”不只是找到某个 API 名称，而是同时产出：

- 受控入口
- 关键符号与对象归属
- 需要遵守的 pywin32 顺序规则
- 项目内优先实现路径
- 验证步骤
- 必要时的回退路径

## 3. 固定检索顺序

任何任务都按以下顺序查，不要颠倒：

1. `04_task_cards/task_index.json`
2. `03_core_symbols/`
3. `05_pywin32_bridge/`
4. `07_validation/hotspot_candidates.json`
5. `06_on_demand_index/`
6. `01_extracted_html/` 原始 HTML

硬规则：

- 原始 HTML 不是第一入口
- 中文只作辅助 alias，不作为主骨架
- 命中项目实现路径时，优先复用项目稳定函数，不要先发明新写法

## 4. 如何从这里快速建立一个 pywin32 CAD 方法

### 第一步：先定任务类型

先判断任务属于哪类：

- 连接 / 文档
- 布局 / 空间
- 选择 / 遍历
- 块 / 属性
- 打印 / 输出
- 命令回退

### 第二步：先查任务卡

优先使用：

```powershell
py -3 .\tools\search_cad_help.py task "<task description>"
py -3 .\tools\search_cad_help.py task_id CAD2021-TASK-015
py -3 .\tools\search_cad_help.py function execute_print_plan
py -3 .\tools\search_cad_help.py module cad/scripts/drawing_basic_service/print/print_executor.py
```

从任务卡中先拿到：

- `task_id`
- `symbols`
- `owners`
- `project_functions`
- `module_paths`
- `rule_refs`

### 第三步：再查核心符号和规则

如果需要把方法写稳，继续查：

- `03_core_symbols/` 中的对象 / 方法 / 属性 / 系统变量
- `05_pywin32_bridge/` 中的规则文档

典型做法：

```powershell
py -3 .\tools\search_cad_help.py symbol SetWindowToPlot
py -3 .\tools\search_cad_help.py symbol ConfigName
py -3 .\tools\search_cad_help.py keyword "plot device media order"
```

### 第四步：按项目标准组织方法

一个合格的方法说明，至少要包含：

1. 受控连接入口
   默认先用 `from system.licad import C`
2. 核心对象与符号
3. 操作顺序
4. 返回结构 / 输出结果
5. 失败点
6. 验证方法
7. 回退路径

### 第五步：必要时回到项目实现路径

若任务卡或核心卡给出 `project_refs` / `module_paths`，优先打开那些实现，而不是直接照抄 CHM 示例。

## 5. 打印主链的特殊硬规则

凡是涉及布局打印、打印窗口、设备切换、纸张切换，默认按下面的顺序理解：

1. `Layout.RefreshPlotDeviceInfo()`
2. `Layout.ConfigName = ...`
3. 再次 `Layout.RefreshPlotDeviceInfo()`
4. `Layout.CanonicalMediaName = ...`
5. `Layout.PlotRotation = ...`
6. `Layout.CenterPlot = True/False`
7. `Layout.SetWindowToPlot(lower_left, upper_right)`
8. `Layout.PlotType = 4`
9. 进入 `PlotToFile` 或 `SendCommand` 回退

如果这条顺序被破坏，打印方法通常不稳定。

直接参考：

- `05_pywin32_bridge/plot_layout_rules.md`
- `03_core_symbols/properties/ConfigName.md`
- `03_core_symbols/properties/CanonicalMediaName.md`
- `03_core_symbols/methods/RefreshPlotDeviceInfo.md`
- `03_core_symbols/methods/SetWindowToPlot.md`

## 6. 何时要触发晋升机制

若你在真实任务里发现：

- 任务卡里已经反复出现某个低频对象
- 搜索多次退回 `06_on_demand_index` 或原始 HTML
- 该对象直接卡住打印/布局/图签/目录主链
- 该对象需要单独的 pywin32 顺序说明

则不能继续把它长期留在低频层。

必须执行：

1. 记录 `07_validation/usage_feedback.jsonl`
2. 更新 `07_validation/hotspot_candidates.json`
3. 判断是否直接补到 `03_core_symbols/`
4. 更新 `04_task_cards/task_index.json`
5. 记录 `07_validation/promotion_log.md`

## 7. 禁止事项

- 不要把中文命中当成检索成功的主要标准
- 不要一上来从 `01_extracted_html/` 全文搜索
- 不要脱离项目实现路径去写孤立版命令方法
- 不要发现主链阻塞对象后只记反馈、不做晋升处理
