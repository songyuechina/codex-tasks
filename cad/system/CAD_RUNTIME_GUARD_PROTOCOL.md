# CAD Runtime Guard Protocol

适用范围：`D:/codex-tasks/cad/system/cad_runtime_guard.py`

## 1. 目标

`cad_runtime_guard.py` 不是打印脚本，也不是恢复脚本。

它的职责是：

1. 长期运行
2. 单实例运行
3. 被动观察当前活动 CAD 运行态
4. 产出结构化状态与告警
5. 为后续运行监督链入口、打印执行链与事件通道提供事实基础

当前阶段，它**不直接接管恢复**，也**不直接强杀 CAD**。

---

## 2. 为什么不依赖窗口文字

不采用“窗口标题里有没有‘天正’”作为主判据，原因有三：

1. 标题文字会随版本、插件、文档名、偶发 UI 状态改变
2. 同一运行环境在不同阶段可能显示不同文字
3. 这种判据对自动化体系来说过于脆弱，容易误判

因此当前协议明确：

- 窗口标题最多作为人工参考
- 不作为运行监管脚本的正式主判据

---

## 3. 当前采用的稳定判据

当前采用“三段式被动判据”：

### 3.1 COM 可达性

监管脚本只尝试：

- `GetActiveObject("AutoCAD.Application")`

它只连接现有活动实例，不主动 `Dispatch` 新建 CAD。

作用：

- 保证监管脚本是观察者，不是干预者

### 3.2 文档可用性

在取得活动实例后，继续检查：

- `ActiveDocument`
- `ModelSpace`
- `PaperSpace`

若这些都可访问，说明当前至少存在一个可工作的 CAD 文档上下文。

### 3.3 进程来源线索

监管脚本会先枚举系统里全部 `acad.exe` 进程，再结合当前活动 CAD 窗口所属进程的：

- `name`
- `exe`
- `cmdline`
- 父进程 `name`
- 父进程 `exe`

若这些来源元数据中包含以下线索之一：

- `tarch`
- `tangent`
- `tgstart`

则判为：

- `healthy_tarch`

若系统里任意 `acad.exe` 仅表现为普通 `acad.exe`，且未发现上述线索，则判为：

- `suspected_plain_cad`

这条规则同样覆盖“混合态”：

- 当前活动实例已经是天正
- 但系统里仍残留一个或多个纯 CAD `acad.exe`

此时也不会放行成 `healthy_tarch`，而是继续上报：

- `suspected_plain_cad`

若 COM 可达、文档可用，但来源线索仍不够明确，则判为：

- `runtime_uncertain`

这是一种保守判定：

- 宁可判为“可疑”
- 也不轻率断言“就是纯 CAD”

---

## 4. 与 `litz()` 的关系

`cad_runtime_guard.py` 与 `litz()` 的关系是：

- `cad_runtime_guard.py` 负责观察与报警
- `litz()` 负责环境恢复与重建

当前阶段，监管脚本不会直接调用 `litz()`。

原因：

1. 若监管脚本自己恢复环境，它就从“观察者”变成“执行者”
2. 后续治理体系中，应由项目总管、监督链或受控执行入口决定何时升级到恢复

因此当前设计是：

- 先记录结构化状态
- 再由后续运行监督链或打印执行链消费这些状态
- 必要时再统一调用 `litz()`

---

## 5. 与现有两个守护脚本的关系

### `cad_dialog_killer.py`

职责：

- 关闭阻塞 CAD 的标准对话框

### `cad_command_monitor.py`

职责：

- 检测 CAD 命令长时间卡死
- 抢焦点后发送 ESC 打断

### `cad_runtime_guard.py`

职责：

- 检测当前是否仍处于可信的天正运行环境
- 当环境来源可疑时，输出结构化告警

三者分工不同，不互相替代：

- `dialog_killer` 处理弹窗
- `command_monitor` 处理命令卡死
- `runtime_guard` 处理运行环境偏航

---

## 6. 单实例与启动方式

`cad_runtime_guard.py` 采用锁文件：

- `D:/codex-tasks/cad/system/cad_runtime_guard.lock`

特性：

- 若已有实例在运行，再次启动不会产生第二个实例
- 会直接退出并提示“已在运行”

推荐启动方式：

```powershell
python D:\codex-tasks\cad\system\cad_runtime_guard.py
```

只做一次检测：

```powershell
python D:\codex-tasks\cad\system\cad_runtime_guard.py --once
```

此外，`CAD_core.launch_cad_guardians()` 现已把它纳入统一守护启动列表。

---

## 7. 输出接口

当前脚本输出两类结构化结果：

### 7.1 当前状态

写入：

- `D:/codex-tasks/dwg_agents_ops/agent_control/runtime/cad_runtime_guard.json`

作用：

- 给监控脚本和后续主控读取最新运行态

### 7.2 事件流

追加写入：

- `D:/codex-tasks/dwg_agents_ops/agent_control/runtime_events.jsonl`

当前事件包含：

- `timestamp`
- `source`
- `target`
- `severity`
- `code`
- `message`
- `recommended_action`
- `status`
- `suspicious_streak`
- `doc_name`
- `pid`
- `process_hint`

当前 `probe` 里还会补充：

- `acad_process_count`
- `tarch_process_count`
- `plain_process_count`
- `tarch_process_pids`
- `plain_process_pids`
- `acad_processes`

---

## 8. 当前升级规则

当前只做保守升级：

- 第一次异常：记录观察
- 连续 2 次可疑：`pause_and_verify`
- 连续 4 次 `suspected_plain_cad`：`pause_and_recover`

注意：

- 当前只是发出结构化建议
- 还没有直接接管恢复

但监督入口 `Runtime_Guard_Agent` 已可以在本地消费 `pause_and_recover`，并调用 `litz()` 做恢复闭环。

---

## 9. 当前最脆弱的点

当前方案最脆弱的点，不是单实例，不是事件写入，而是：

- “天正来源线索”目前仍主要依赖进程来源元数据

这比窗口标题稳定得多，但仍不等于真正的“天正能力探针”。

因此下一阶段最重要的工作是：

1. 为运行监管补一个更可靠的、低侵入的天正能力探针
2. 让 `Runtime_Guard_Agent/` 这一本地监督入口消费 `runtime_events.jsonl`
3. 让打印执行链在关键节点主动轮询并响应 `pause_and_verify / pause_and_recover`

当前这三步中的第 2、3 步已经有首版最小闭环实现：

- `Runtime_Guard_Agent` 已落地为本地事件驱动监督对象
- 打印执行链已接入关键节点响应
- 详细事件字段与响应语义见：
  - `D:/codex-tasks/dwg_agents_ops/agent_control/RUNTIME_EVENT_PROTOCOL.md`

## 11. 实测验证

当前已有专门的实测脚本：

```powershell
python D:\codex-tasks\cad\system\runtime_guard_recovery_validation.py --mode random --rounds 2 --seed 20260321
```

作用：

1. 重启 `cad_runtime_guard.py`
2. 随机用纯 CAD 或天正入口启动一轮
3. 观察 `cad_runtime_guard.json`
4. 在需要时调用 `Runtime_Guard_Agent\agent_cli.py --once`
5. 验证最终是否回到“单一天正进程，无 plain CAD 残留”

实测结果样例：

- `D:/codex-tasks/cad/system/logs/runtime-guard-validation/case-20260321-235550/summary.json`
- `D:/codex-tasks/cad/system/logs/runtime-guard-validation/case-20260321-235816/summary.json`

## 10. 与执行纪律督导的关系

`cad_runtime_guard.py` 负责“看见环境事实”，但它不直接负责执行纪律本身。

例如下面这些事项：

1. 每完成一个 DWG 后关闭相关工作文档
2. 每完成一个 DWG 后调用 `CAD_core.cad_zt_oneb()` 回到简化状态
3. 执行前明确受控入口与恢复入口

这些不应强塞回 `cad_runtime_guard.py` 自己做。

更合理的分工是：

- `cad_runtime_guard.py` 产出环境事实
- `Runtime_Guard_Agent` 基于事实与规则做监督结论
- 项目总管和执行链落实具体收尾、归一和恢复动作
