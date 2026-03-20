# CAD Runtime Guard Rules

本文件用于约束任何智能体在 `D:/codex-tasks` 项目中操作 CAD / 天正 CAD 时的最小运行纪律。

它解决的不是“如何写打印逻辑”，而是更前面的根本问题：

- 进入 CAD 时，如何尽量不走错入口
- 一旦走错到纯 CAD，如何尽快止损并回到正轨
- 如何把“文档约束”变成“任务入口约束”

---

## 1. 结论先行

仅仅在任务里提醒智能体“去读文档”，是有价值的，但**不可靠，也不充分**。

原因：

1. 智能体可能忘记
2. 智能体可能误读
3. 即使没忘，运行期也可能因偶然环境因素连到纯 CAD
4. 一旦底层连接已偏离，仅靠后续推理很难自动回正

因此，本项目必须采用三层约束：

1. 文档提醒层
2. 任务入口层
3. 运行时自检与恢复层

少任何一层，都不稳。

---

## 2. 文档提醒层

下达任何 CAD / DWG / 打印任务时，都应明确要求智能体先阅读：

1. `D:/codex-tasks/AGENTS.md`
2. `D:/codex-tasks/thoughtway/SYSTEM_FOUNDATIONS.md`
3. `D:/codex-tasks/thoughtway/CAD_RUNTIME_GUARD_RULES.md`

若任务位于打印子系统，还必须再读：

4. `D:/codex-tasks/cad/scripts/drawing_basic_service/print/AGENTS.md`
5. `D:/codex-tasks/cad/scripts/drawing_basic_service/print/PRINT_DISPATCH_PROTOCOL.md`
6. `D:/codex-tasks/cad/scripts/drawing_basic_service/print/PRINT_KNOWLEDGE.md`

作用：

- 帮它进入正确框架
- 让它在开工前主动回忆系统共识
- 降低“忘规则”的概率

但这层只能算提醒，不能算保证。

---

## 3. 任务入口层

任何真实 CAD 任务，在开始执行前，智能体都应先明确回答两件事：

1. 本次将使用哪个受控入口启动 / 连接天正 CAD
2. 若检测到纯 CAD 或疑似非天正环境，将走哪个恢复入口

若连这两件事都没有明确，就不应直接开始操作 DWG。

推荐的受控入口原则：

- 连接默认通过：
  - `from system.licad import C`
- 启动 / 环境恢复优先通过：
  - `CAD_core.litz()`
  - `CAD_core.launch_tarch_CAD_system()`
  - `CAD_core.open_file()`
  - `CAD_core.open_dwg_paradigm()`
  - 任务启动时优先补充：
    - `CAD_core.launch_cad_guardians()`

禁止把下面这些当作业务层主入口长期散用：

- 裸 `win32com.client.Dispatch("AutoCAD.Application")`
- 裸 `GetActiveObject("AutoCAD.Application")`
- 业务脚本私自拼接新的 CAD 启动流程

注意：

`CAD_core.py` 当前内部仍保留了 `GetActiveObject/Dispatch("AutoCAD.Application")` 的兼容兜底，
所以它并没有从机制上彻底杜绝“连到纯 CAD”的可能。
因此，入口受控后仍然必须有运行时自检。

---

## 4. 运行时自检层

任何真实 CAD 执行前，至少应完成一次“天正环境健康确认”。

推荐顺序：

1. 先走受控入口连接环境
2. 优先使用 `CAD_core.litz()` 做健康检查和必要的重建
3. 若任务需要打开 DWG，再通过 `CAD_core.open_file()` 打开目标文件
4. 打开后再次确认目标文档已被正确激活

核心思想：

- 不假设环境天然正确
- 每次真实任务都把环境当作可能已污染
- 先确认环境，再进入业务动作

---

## 5. 发现偏离时的止损规则

一旦出现以下任一现象，应立即怀疑已经偏到纯 CAD 或错误环境：

1. 天正对象操作失败，而普通 CAD 对象操作正常
2. 天正墙探针失败
3. 依赖天正对象名的选择明显异常
4. 打开的是 CAD 空壳环境，而不是预期的天正工作环境
5. 之前正常的脚本突然在启动后表现为“像纯 CAD 一样”

此时禁止继续在错误环境里盲目探索。

必须立即进入恢复协议。

---

## 6. 恢复协议

标准恢复顺序：

1. 停止当前错误路径上的继续操作
2. 记录当前异常现象
3. 调用 `CAD_core.litz()` 做环境重建 / 重连
4. 必要时重新打开目标 DWG：
   - `CAD_core.open_file(...)`
5. 再次确认目标文档激活成功
6. 只有恢复成功后，才继续打印 / 分析 / 修改任务

若恢复失败：

- 不要无限试错
- 应明确报告“当前为环境级阻塞”
- 并把现象记入日志与沟通记录

---

## 7. 对打印智能体的特别要求

打印任务虽然主要在 `print/` 目录下运行，但其 CAD 启动与 DWG 打开仍必须继承整个系统的受控入口。

打印智能体不得：

- 自己另写一套 CAD 启动逻辑
- 在打印目录里绕过 `CAD_core.py`
- 发现环境异常后继续尝试打印

打印智能体必须：

1. 先确认受控入口
2. 先拉起运行守护脚本组
2. 先确认环境健康
3. 再打开工作副本
4. 再生成打印计划
5. 再进入真实打印

---

## 8. 面向任务下达者的建议

以后给项目总管或打印智能体下任务时，推荐把任务开头固定成这种形式：

```text
先阅读并遵守：
1. D:\codex-tasks\AGENTS.md
2. D:\codex-tasks\thoughtway\SYSTEM_FOUNDATIONS.md
3. D:\codex-tasks\thoughtway\CAD_RUNTIME_GUARD_RULES.md
4. 若涉及打印，再读 print/AGENTS.md、PRINT_DISPATCH_PROTOCOL.md、PRINT_KNOWLEDGE.md

开始执行前，先明确回答：
1. 本次使用哪个受控入口启动/连接天正 CAD；
2. 若检测到纯 CAD 或疑似非天正环境，准备如何恢复。
```

这仍不是绝对保证，但会显著提高稳定性。

---

## 9. 根本原则

本项目对智能体的约束，不应只停留在“请记住规则”。

更稳的原则是：

- 用文档减少遗忘
- 用入口减少偏航
- 用自检发现错误
- 用恢复协议尽快回正

只有这样，智能体即使偶然偏离，也不会长时间在错误道路上越走越远。
