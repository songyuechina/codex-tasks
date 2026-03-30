# 02_logging_rules.md

版本：V2.0

## 目标

统一函数与脚本的日志写法，确保：
- agent 可快速理解输出层级
- 故障路径清晰
- 调试与批量运行可切换
- 高风险区段可记录、可追溯

## 根本规则（强制）

1. 所有业务脚本禁止 `print()`；必须使用：
   `from system.common_logger import sys_logger`

2. 统一使用：
   - `sys_logger.debug(...)`
   - `sys_logger.info(...)`
   - `sys_logger.warning(...)`
   - `sys_logger.error(...)`
   - `sys_logger.critical(...)`

3. `set_debug_mode()` 只能在以下脚本调用一次：
   - 入口脚本
   - 测试脚本
   - agent 启动脚本

4. 普通业务模块禁止自行初始化新的全局日志体系

## 日志等级规范

- `debug`：变量细节、频繁内部状态
- `info`：流程节点、阶段切换、正常关键事件
- `warning`：可恢复异常、降级策略、兼容处理
- `error`：失败路径，应引发上层关注或异常
- `critical`：系统级致命问题

## 调试模式约定

- 批量运行：`set_debug_mode(mode=0)` → 默认 `WARNING`
- 调试运行：`set_debug_mode(mode=1)` → 默认 `INFO`
- 深度调试：`set_debug_mode(mode=1, log_level="DEBUG")`

## 高风险区段规则

建议使用：

```python
with CriticalSection("...") as cs:
    cs.record(...)
```

典型场景：
- pywin32 CAD 调用
- 文件写入
- 数据库写入
- 回滚逻辑
- 跨文件合并
- 高风险命令链

`CriticalSection` 不吞异常。

## 关于 print 的例外

### 人工介入提示
`common_logger.py` 中的 `checkpoint` / `CriticalSection`，在：
- `WHO == "HUMAN"`
- `WAIT > 0`

时允许使用 `print` 做人工暂停提示。

### 守护脚本
如：
- `cad_command_monitor.py`
- `cad_dialog_killer.py`

可阶段性保留独立 logging / 控制台输出机制。  
但这属于守护层例外，不是业务模块标准写法。

## 禁止行为

- 业务模块中随意 `print()`
- 在多个业务模块中分散调用 `set_debug_mode()`
- 各模块各自建立不同的日志规范
- 把人工介入提示 print 扩散为普通输出方式
