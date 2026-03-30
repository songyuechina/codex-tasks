# 05_exception_handling_rules.md

版本：V2.0

## 目标

规范异常处理与失败路径，使 CAD 自动化系统在高不稳定接口下仍然具备：

- 可追踪性
- 可恢复性
- 可回滚性
- 可重试性

## 基本原则

1. 不要静默吞掉关键异常
2. 可恢复异常用 `warning`
3. 失败路径用 `error`
4. 致命系统错误用 `critical`
5. 对高风险区段尽量形成“记录 + 回滚/重试”闭环

## CAD / COM 特殊原则

对 CAD / COM 这类高不稳定接口，允许采用以下策略：

- 视短时异常为 `busy / blocked`
- 重试而不是立即判死
- 等待就绪而不是立刻重建
- 必要时使用回滚、重启、环境重连

这尤其适用于：

- `licad.py`
- `CAD_com_utils.py`
- `CAD_coordination.py`

## 当前系统中的典型经验

### COM busy / rejected
在 `CAD_com_utils.py` 中：
- `Call was rejected`
- busy 错误码
- `PumpWaitingMessages + 退避等待`

### 等待空闲
在 `CAD_coordination.py` 中：
- 读取失败先视为 `COM_Block`
- 不轻易判死
- 连续静默一段时间后才算通过

### 文件级回滚
在 `FileGuard` / `run_safety_loop` 中：
- 先备份
- 再执行
- 再校验
- 失败时关闭 CAD 并物理恢复文件

### 连接自愈
在 `licad.py` 中：
- 进程已存在但 COM 未就绪时等待
- 严重异常时可清理 `gen_py` 缓存

## 禁止行为

- 宽泛 `except: pass` 掩盖关键失败路径
- 失败后不记录日志
- 对高风险写操作没有回滚思路
- 把 CAD/COM 短时阻塞直接当永久失败处理
- 反过来把真正致命错误无限重试
