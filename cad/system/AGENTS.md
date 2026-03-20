# AGENTS.md

适用范围：`D:/codex-tasks/cad/system/`

本文件用于指导 Codex 等命令行智能体理解并操作 `cad/system` 目录。  
这里是整个项目中最核心的 CAD / DWG 系统层。

---

# 1. 本目录的根本定位

`cad/system` 不是面向人工点击 CAD 的零散工具目录，而是面向 **本地运行的智能体** 的 CAD / DWG 操作内核。

它提供：

- 统一连接入口
- 对象选择与属性访问
- 基础文件控制
- 同步协调与事务保护
- 日志与记录
- DWG 内容分析与快照验证
- 守护脚本（弹窗 / 命令超时）

---

# 2. 进入本目录后先看什么

请先阅读：

1. `README.md`

然后按以下顺序阅读：

2. `licad.py`
3. `CAD_selection.py`
4. `common_logger.py`
5. `CAD_com_utils.py`
6. `CAD_coordination.py`
7. `CAD_core.py`
8. `content_analysis_dwg_file.py`
9. `cad_command_monitor.py`
10. `cad_dialog_killer.py`
11. `project_setup.py`

如某个脚本已存在：

- `quote.meta.json`
- `procedure.meta.json`
- `functions.quote.meta.json`
- `functions.procedure.meta.json`

则建议顺序为：

1. 先看 `README.md`
2. 再看脚本级 meta
3. 再看函数级 meta
4. 最后再下钻源码

---

# 3. 本目录当前主骨架

## 3.1 统一连接入口层
### `licad.py`
这是整个系统的统一 CAD 连接入口。

关键点：
- 统一使用 `from system.licad import C`
- `C.doc` 是安全包装文档
- `C.raw_doc` 是原始 COM 文档
- 不要轻率重写 `SafeDocumentWrapper`
- 不要轻率破坏 `li()` 的连接刷新与自愈经验

这是高价值稳定核心。

---

## 3.2 选择与对象研究层
### `CAD_selection.py`
这是对象选择、类型转换、当前空间过滤、天正属性访问的核心。

关键点：
- `ss_select`
- `current_space_only`
- `_maybe_cast`
- 天正 `DISPID` 属性映射

这是高价值稳定核心。  
允许局部修补，但不宜轻率整体重写。

---

## 3.3 基础控制与文件操作层
### `CAD_core.py`
这是基础控制、文件操作、状态归一、跨文件操作的核心。  
它当前仍带有历史兼容桥接痕迹，可以继续收束，但不能丢掉已验证有效的经验。

---

## 3.4 协同与保护层
### `CAD_coordination.py`
建立在 `licad.C` 之上，负责：

- 等待空闲
- 事务守卫
- 文件回滚
- 安全循环
- 命令同步

它不是主连接入口。

---

## 3.5 COM busy / retry 辅助层
### `CAD_com_utils.py`
负责：

- `retry_on_busy`
- `retry_if_busy`
- `SafeCOM`
- `silent_mode`
- `timeit`

它只应处理 COM busy / rejected 等问题，不能再膨胀成大杂烩辅助模块。

---

## 3.6 日志与记录层
### `common_logger.py`
全目录统一使用：

```python
from system.common_logger import sys_logger
```

规则：
- 业务模块不要自己建立新的日志体系
- `set_debug_mode()` 只允许入口/测试/agent 启动脚本调用
- `CriticalSection` 不吞异常

---

## 3.7 内容分析与验证层
### `content_analysis_dwg_file.py`
负责：

- DWG 内容快照
- 数据库持久化
- `counts_by_type`
- `counts_by_space`
- digest
- 按需 handle 采集

它是后续案例验证、结果核验、快照比较的重要基础。

---

## 3.8 守护层
### `cad_command_monitor.py`
处理命令超时卡死、等待输入停滞、抢焦点后 ESC 打断。

### `cad_dialog_killer.py`
处理 CAD 标准对话框阻塞，支持延迟关闭与单实例守护。

这两个脚本属于独立守护脚本，不是普通业务模块。

---

## 3.9 纯路径配置层
### `project_setup.py`
只负责稳定路径常量。  
不负责：

- bootstrap
- sys.path 引导
- CAD 连接

---

# 4. 本目录中的稳定核心与过渡核心

## 4.1 高价值稳定核心
- `licad.py`
- `CAD_selection.py`

原则：
- 允许局部修补
- 不宜轻率整体推翻

## 4.2 允许继续收束的核心
- `CAD_core.py`
- `CAD_coordination.py`
- `CAD_com_utils.py`
- `common_logger.py`
- `content_analysis_dwg_file.py`

原则：
- 可继续拆分、收束、减耦合
- 但必须保留已被实践验证有效的经验

---

# 5. 本目录的 meta 体系（重点更新）

本目录当前采用四层 meta 结构：

## 5.1 脚本级
- `A_quote.meta.json`
- `A_procedure.meta.json`

作用：
- 先抓脚本骨架
- 确定脚本角色、public_api、workflow、边界

## 5.2 函数级
- `A_functions.quote.meta.json`
- `A_functions.procedure.meta.json`

作用：
- 覆盖脚本中的全部函数
- 提供函数功能目标
- 提供输入输出和返回结构
- 提供函数流程概括
- 支撑快速修改和重构

## 5.3 使用顺序
修改某脚本前，推荐顺序：

1. `README.md`
2. 脚本级 quote / procedure
3. 函数级 functions.quote / functions.procedure
4. 源码
5. 调用链 / 引用链搜索

## 5.4 函数级 meta 的工作目标
函数级 meta 的目标是：

- 尽量覆盖脚本中的全部函数
- 不要求每个函数都一样详细
- 简单函数简写
- 复杂函数适度展开
- 允许局部不精确
- 允许不确定内容写入 `quality.todo`
- 不要因局部不确定而停工

---

# 6. 本目录当前重点任务（若用户正在推进 meta 建设）

如果用户正在推进 `cad/system` 的函数级 meta 建设，则你的优先目标是：

1. 为 10 个正式脚本建立函数级 meta
2. 对每个脚本尽量覆盖全部函数
3. 对函数做分级：
   - `core`
   - `normal`
   - `utility`
4. 简单函数简写，复杂函数适度展开
5. 保持整体完成优先于局部完美

若当前任务与函数级 meta 直接相关，不要反复要求绝对精准；应先完成整体覆盖。

---

# 7. 本目录的强制规则

## 7.1 连接规则
所有 CAD 主连接原则上统一通过：

```python
from system.licad import C
```

进行。

禁止业务层长期分散使用：
- `GetActiveObject`
- `Dispatch`
- 裸 `SendCommand`
- 各自维护的 app/doc 缓存

## 7.2 日志规则
业务模块统一使用：

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

## 7.3 引导规则
`cad/system` 内的库模块原则上不应自行承担 bootstrap 责任。  
当前残留的旧式引导属于历史兼容痕迹，不是未来标准。

## 7.4 异常规则
对 CAD / COM 这类高不稳定接口：

- 可将短时异常视为 busy / blocked
- 允许等待与重试
- 必要时执行环境重建、自愈、回滚
- 但不能无限吞掉真正致命错误

---

# 8. 如何在本目录工作

## 8.1 修改前
1. 先看 `README.md`
2. 再看对应脚本的脚本级 meta
3. 再看函数级 meta
4. 再搜索真实定义点与调用点
5. 再进入源码修改

## 8.2 修改时
1. 尽量最小化破坏面
2. 保持层级边界
3. 不新增杂项职责
4. 不破坏统一连接规则
5. 不破坏统一日志规则

## 8.3 修改后
1. 用案例或快照验证
2. 检查是否误动高价值稳定核心
3. 检查脚本级 / 函数级 meta / README 是否需要同步更新

---

# 9. 对智能体的特别提醒

## 9.1 不要把旧代码形式当最高权威
真正该继承的是：
- 项目思想
- 系统规则
- 已验证经验
- 案例与校验标准

## 9.2 不要误判“脚本多 = 全部推翻”
应先判断：
- 哪些是稳定核心
- 哪些是过渡核心
- 哪些只是守护补充

## 9.3 不要轻率整体重写
尤其不要轻率整体重写：
- `licad.py`
- `CAD_selection.py`

## 9.4 meta 不是装饰品
meta 的作用是帮助你摆脱源码过多内容的束缚，迅速定位角色、函数、流程与不可丢失经验。

## 9.5 若脚本级 meta 与函数级 meta 冲突
优先顺序为：

1. 当前规则文件
2. `README.md`
3. 源码真实实现
4. 脚本级 meta
5. 函数级 meta

若发现冲突，应优先修正 meta，而不是机械服从旧 meta。

---

# 10. 本目录最重要的一句话

> `cad/system` 是整个项目中面向智能体的 CAD / DWG 操作系统骨架；脚本级 meta 帮助你先抓骨架，函数级 meta 帮助你进入全部函数的控制层。你可以重构函数形式，但不能丢失已被实践验证有效的核心经验。
