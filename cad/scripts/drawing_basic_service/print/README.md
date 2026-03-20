# Print Service

本目录是打印智能体的领域工作区。

目标不是只保存几个脚本，而是建立一套让后续智能体能够：

- 快速理解打印系统骨架
- 快速掌握关键知识和方法
- 按统一规则执行打印任务
- 在新案例出现时稳定迭代

## 文档体系

建议阅读顺序：

1. `README.md`
   先看目录定位、文档地图、脚本地图。
2. `AGENTS.md`
   再看硬规则、默认判断、禁止事项。
3. `PRINT_DISPATCH_PROTOCOL.md`
   再看谁可以调度打印智能体、输入输出契约、默认接单判断。
4. `PRINT_AGENT_SPEC.md`
   再看打印智能体角色定位、职责边界、能力要求。
5. `PRINT_WORKFLOW.md`
   再看接到任务后应如何判断、分析、执行、验证、交付。
6. `PRINT_OUTPUT_SPEC.md`
   再看每类任务必须留下哪些结果文件、满足哪些质量门槛。
7. `PRINT_KNOWLEDGE.md`
   最后看领域知识、经验规则、典型误区。
8. `cases/CASE_MANIFEST.md`
   需要落到真实案例时再看案例与当前权威输出。

## 文档角色分工

- `README.md`
  入口图和总览。
- `AGENTS.md`
  本目录最高优先级的局部硬规则。
- `PRINT_DISPATCH_PROTOCOL.md`
  调度协议、接单输入输出契约、自修复闭环。
- `PRINT_AGENT_SPEC.md`
  打印智能体的角色说明书。
- `PRINT_WORKFLOW.md`
  执行工作流与操作方法。
- `PRINT_OUTPUT_SPEC.md`
  输出结果与质量门槛规范。
- `PRINT_KNOWLEDGE.md`
  专业知识、经验、判断依据。
- `cases/CASE_MANIFEST.md`
  案例资产与权威结果索引。

若文档冲突，优先级为：

1. `AGENTS.md`
2. `PRINT_DISPATCH_PROTOCOL.md`
3. `PRINT_WORKFLOW.md`
4. `PRINT_OUTPUT_SPEC.md`
5. `PRINT_AGENT_SPEC.md`
6. `PRINT_KNOWLEDGE.md`
7. `README.md`

## 当前系统骨架

当前打印主链脚本：

- `print_batch_dispatch.py`
  统一调度入口，支持目录级批量任务与单文件任务，负责打印、打印信息分析、空白页补救与汇总。
- `print_area_analysis.py`
  打印区域识别与标准图幅匹配。
- `print_area_scope_analysis.py`
  `purified_adaptive` 的二次范围分析脚本，用于识别伪极大打印区域并收束最终打印范围。
- `print_policy.py`
  打印计划、排序、过滤、输出路径分配。
- `print_runner.py`
  真实打印入口。
- `print_executor.py`
  打印执行器。
- `print_verifier.py`
  PDF 校验器。

当前辅助分析脚本：

- `print_area_content_analysis.py`
  伪打印区域分析，服务 `purified_adaptive`。
- `print_info_analysis.py`
  打印信息分析，分析打印区域中的内框线、图签块和文字信息。

## 当前输出组织规则

- 单文件任务：
  - 最终 PDF 放在原 DWG 同目录下的 `<公共名>pdf/`
  - 最终分析放在原 DWG 同目录下的 `<公共名>analysis/`
  - 过程文件放在原 DWG 同目录下的 `<公共名>prosess/`
- 目录任务：
  - 仍逐 DWG 按上述规则交付最终结果
  - 另外在调度根目录下保留 `batch_summary.json`

这里的“公共名”用于去掉日期、版次、批次尾缀，便于用户查找最终交付目录。

## 当前异常案例沉淀规则

- 若某个 DWG 暴露了新的打印问题，除了完成用户任务外，还应把该文件复制到 `cases/assets/`
- `cases/` 不是临时附件区，而是打印体系的典型案例库
- 新案例进入后，应同步更新 `cases/CASE_MANIFEST.md`

## 当前有效模式

打印主链只允许三种模式：

- `basic`
- `adaptive`
- `purified_adaptive`

已废除：

- `analysis` 作为打印模式

打印信息分析现在是独立辅助能力，不属于打印模式。

`purified_adaptive` 当前的完整收束链已经变为：

1. `print_area_analysis.py` 生成适配候选区域
2. `print_area_content_analysis.py` 识别明显伪区域
3. `print_area_scope_analysis.py` 判断是否存在伪极大外包范围
4. 若同时命中伪极大范围与伪区域风险，则仅保留最大伪极大范围内的打印区域
5. 再过滤 `pseudo_handles`，得到最终打印计划

## 当前第一职责

打印智能体的第一职责始终是：

- 稳定、高质量、高效率地完成 DWG 打印任务

打印信息分析、目录、命名、插图签等能力都属于扩展，但必须为主任务服务，不能反过来干扰打印主链。

## 当前调度定位

本目录中的打印智能体应被视为一个可被调度的对象。

它可以被以下两类主体直接调度：

- 项目总管智能体
- 人类操作者

无论由谁发起调度，都应统一遵守本目录文档体系，不允许靠临时聊天口径替代规则。

## 当前默认判断

- 用户未明确指定打印模式，默认 `basic`
- 用户未明确指定打印信息分析模式，默认 `basic`
- 只有在用户明确要求或案例表明 `basic` 不足时，才进入 `adaptive` 或 `purified_adaptive`
- 只有在用户明确需要结构化页面信息时，才调用 `print_info_analysis.py`

## 当前对未来迭代的要求

本目录允许随着新案例持续迭代，但必须遵守：

- 新案例优先沉淀到案例与文档，而不是只留在聊天里
- 新经验优先进入 `PRINT_KNOWLEDGE.md`
- 新规则优先进入 `AGENTS.md` 或 `PRINT_WORKFLOW.md`
- 新输出要求优先进入 `PRINT_OUTPUT_SPEC.md`
- 不要轻易增加平行脚本和重复职责脚本
- 调度协议与自修复经验优先进入 `PRINT_DISPATCH_PROTOCOL.md`
