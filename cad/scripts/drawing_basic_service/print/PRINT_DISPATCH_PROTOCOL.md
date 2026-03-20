# PRINT_DISPATCH_PROTOCOL.md

## 1. 角色调度对象定义

打印智能体是 `print/` 目录下的领域执行对象。

它必须同时支持两种调度来源：

- 项目总管智能体调度
- 人类直接调度

两种来源在本目录内的执行口径必须一致：

- 同一默认模式
- 同一输出规范
- 同一失败处理规则
- 同一文档沉淀规则

## 2. 可接收的任务类型

打印智能体当前只应接收四类任务：

1. 基本模式打印任务
2. 适配模式打印任务
3. 净化适配打印任务
4. 打印信息分析任务

其中默认任务类型是：

- 用户未特别说明时，按 `basic` 打印任务处理

打印信息分析属于辅助任务，不得反向覆盖打印主链的默认判断。

## 3. 最小输入契约

一次有效调度，最少应明确：

- `dwg_path`

若调用方未补充，打印智能体按默认规则自行补全：

- `mode`
  - 默认 `basic`
- `include_model`
  - 默认 `True`
- `include_layouts`
  - 默认 `True`
- `only_layouts`
  - 默认 `None`
- `need_print_info_analysis`
  - 默认 `False`

若任务本身是打印信息分析，则默认：

- `mode = basic`
- `need_print_info_analysis = True`
- 不附带真实打印

## 4. 输出契约

### 4.1 打印任务

至少输出：

- `print_plan.json`
- `print_summary.json`
- `pdf/`

若是单文件任务，对用户可见的最终交付必须组织为：

- 源 DWG 同目录下的 `<公共名>pdf/`
- 源 DWG 同目录下的 `<公共名>analysis/`
- 源 DWG 同目录下的 `<公共名>prosess/`

若为 `purified_adaptive`，还必须输出：

- `content_analysis.json`
- `scope_analysis.json`（当触发伪极大范围收束时）

### 4.2 打印信息分析任务

至少输出：

- `print_info_analysis.json`
- `print_info_analysis.xlsx`

按需要可附加：

- `print_info_dict.json`

## 5. 调度入口映射

推荐的统一入口如下：

- 目录级批量任务
  - 入口脚本：`print_batch_dispatch.py`
  - 必填输入：`--input-dir` 或 `--dwg`
  - 常用可选：`--output-root`、`--mode`
  - 当前支持：
    - 逐 DWG 调用打印主链
    - 逐 DWG 调用打印信息分析
    - 单文件同目录交付
    - 最终空白页检测
    - 必要时调用空白副本补救链
    - `purified_adaptive` 下的伪极大范围二次收束
- 打印任务
  - 入口脚本：`print_runner.py`
  - 必填输入：`--dwg`
  - 常用可选：`--mode`、`--layout`、`--no-model`、`--no-layouts`、`--output-root`
- 打印信息分析任务
  - 入口脚本：`print_info_analysis.py`
  - 必填输入：`--dwg`
  - 常用可选：`--mode`、`--plan-json`、`--content-json`、`--layout`、`--handle`、`--output`
- 伪区域净化分析
  - 入口脚本：`print_area_content_analysis.py`
  - 角色：服务 `purified_adaptive`
  - 默认不作为独立打印交付入口
- 伪极大范围分析
  - 入口脚本：`print_area_scope_analysis.py`
  - 角色：服务 `purified_adaptive`
  - 默认不作为独立打印交付入口

最小命令示例：

```powershell
python print_batch_dispatch.py --input-dir "D:\path\dwg_dir" --mode purified_adaptive
python print_runner.py --dwg "D:\path\case.dwg"
python print_runner.py --dwg "D:\path\case.dwg" --mode purified_adaptive
python print_info_analysis.py --dwg "D:\path\case.dwg" --mode basic --output "D:\path\print_info_analysis.json"
```

## 6. 接单判断协议

接到任务后，打印智能体必须先判断：

1. 这是打印任务还是辅助分析任务
2. 用户是否明确指定模式
3. 当前是否已有权威结果可直接复用
4. 是否必须先做脚本修正，再继续执行

在以上判断之前，还必须先完成运行时入口确认：

1. 已阅读：
   - `D:\codex-tasks\thoughtway\CAD_RUNTIME_GUARD_RULES.md`
   - `D:\codex-tasks\cad\scripts\drawing_basic_service\print\AGENTS.md`
   - `D:\codex-tasks\cad\system\CAD_RUNTIME_GUARD_PROTOCOL.md`
2. 已明确：
   - 本次使用哪个受控入口启动 / 连接天正 CAD
   - 若检测到纯 CAD 或疑似非天正环境，准备走哪个恢复入口

若这一步未完成，不应直接打开 DWG 或开始打印。

推荐动作：

- 在任务启动时通过 `CAD_core.launch_cad_guardians()` 拉起守护脚本
- 其中已包含：
  - `cad_dialog_killer.py`
  - `cad_command_monitor.py`
  - `cad_runtime_guard.py`
- 同时由项目总管或人拉起：
  - `D:\codex-tasks\dwg_agents_ops\Runtime_Guard_Agent\agent_cli.py`

默认判断如下：

- 只说“打印”，按 `basic` 打印
- 只说“分析打印信息”，按 `basic` 打印区域做分析
- 只有在 `basic` 无法满足目标或用户明确要求时，才进入 `adaptive`
- 只有在 `adaptive` 已出现伪区域风险时，才进入 `purified_adaptive`

若用户给的是异常单文件且该文件暴露了新问题，打印智能体除完成本次交付外，还应：

1. 复制该文件进入 `cases/assets/`
2. 用该副本做最小回归验证
3. 将新经验写入案例和文档

## 7. 稳定轨与验证轨

当前体系实行两条轨道：

- `stable`
  - 指当前权威模式、权威案例、权威结果口径
- `validation`
  - 指新一轮验证、治理回归、脚本修补后的确认运行

规则如下：

- `stable` 结果才能作为默认复用基线
- `validation` 结果可用于证明本轮修改成立
- 未经权威案例回归确认的 `validation` 结果，不得直接覆盖 `stable`

## 8. 自修复触发条件

打印智能体不是只会执行既有脚本，也必须具备自修复能力。

出现以下情况时，应进入自修复闭环：

1. 当前脚本无法完成既有打印主链
2. 输出结果与文档约定冲突
3. 新案例暴露出稳定性问题或明显误判
4. 旧经验已失效，继续沿用会误导后续任务

但自修复必须满足以下约束：

- 先复现问题，再修脚本
- 优先最小修补，不优先平行重写
- 不得破坏打印主链稳定性
- 修脚本后必须回归验证
- 验证后必须回写文档和案例记录

## 9. 自修复闭环

自修复的最小闭环为：

1. 用真实案例复现问题
2. 明确问题所在脚本与职责边界
3. 实施最小必要修补
4. 用同一案例重新验证
5. 更新本目录文档
6. 更新案例结果索引
7. 更新 `D:\codex-tasks\thoughtway\conversation_log.md`

若问题已涉及默认判断变化，还必须同步更新：

- `AGENTS.md`
- `PRINT_WORKFLOW.md`
- `PRINT_KNOWLEDGE.md`

若问题涉及 WPS 窗口堆积或空白 PDF，还应同步复核：

- `print_executor.py`
- `print_batch_dispatch.py`

## 10. 稳定沉淀与开放发展

打印智能体必须同时满足两点：

- 保持主链稳定沉淀
- 允许在新案例驱动下持续演进

具体要求：

- 已经实测稳定的主链经验优先保留
- 允许修正误判规则、去噪规则、输出结构
- 不允许为单次案例长期保留重复职责脚本
- 新规则要写入文档，不能只停留在对话

## 11. 统一调度时的协作口径

当项目总管统一调度打印智能体时，打印智能体应返回：

- 采用了什么模式
- 用了哪个入口脚本
- 输出目录在哪里
- 成功数 / 失败数
- 是否触发脚本修正
- 是否产生新的规则或知识沉淀

## 12. 运行守护事件响应

打印执行链在关键节点必须读取运行守护状态，并按以下规则响应：

1. 若命中：
   - `severity = critical`
   - 或 `recommended_action = pause_and_recover`

   则：
   - 不得继续执行打印
   - 必须抛出受控异常
   - 必须把 checkpoint / severity / recommended_action / status 带出

2. 若命中：
   - `severity = warning`
   - 或 `recommended_action = pause_and_verify`

   则：
   - 不得继续闷头推进
   - 必须显式停下并报告

3. 当前最小闭环是：
   - `cad_runtime_guard.py` 提供事件
   - `Runtime_Guard_Agent` 形成监督结论
   - 打印执行链在关键节点做保守响应
   - 项目总管按需决定是否升级到恢复链

当人类直接调度打印智能体时，也应返回同样口径，避免形成两套汇报体系。
