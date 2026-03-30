# 06_cad_connection_rules_licad_C.md

版本：V2.0

## 目标

统一整个 `codex-tasks` 对 CAD / DWG 的连接方式，明确：

- 连接入口是谁
- 上层协同层是谁
- 基础控制层是谁
- 哪些脚本属于高价值稳定核心

## 根本规则（强制）

所有 CAD 连接原则上统一通过：

```python
from system.licad import C
```

进行。

禁止业务层长期分散使用：

- `win32com.client.GetActiveObject`
- `win32com.client.Dispatch`
- 裸 `SendCommand`
- 各自维护的 app/doc 缓存

## 当前系统骨架

### 统一连接入口层
`licad.py`
负责：
- 获取/启动 CAD 实例
- 统一连接刷新
- `C` 代理对象
- `doc / raw_doc` 分层语义
- `SafeDocumentWrapper`
- `SendCommand` 安全包装入口

这是高价值稳定核心，非必要不整体重写。

### 选择与对象研究层
`CAD_selection.py`
负责：
- 选择引擎
- 类型转换
- 当前空间过滤
- 天正属性访问

这也是高价值稳定核心，非必要不整体重写。

### 协同与保护层
`CAD_coordination.py`
建立在 `licad.py` 之上，负责：
- 等待空闲
- 事务保护
- 文件回滚
- 命令同步
- 安全循环

### 基础控制层
`CAD_core.py`
建立在 `licad.py` 之上，负责：
- 基础文件控制
- 环境重连
- 状态归一
- 跨文件操作

## doc / raw_doc 规则

- `C.doc`：默认给业务层使用的安全包装文档
- `C.raw_doc`：给高层协调或特殊底层逻辑使用的原始 COM 文档

原则：
- 普通业务层优先使用 `C.doc`
- 只有在明确需要原始行为时才使用 `C.raw_doc`
- 不得混淆二者语义

## SendCommand 规则

普通业务层不应随意裸调用原始 `SendCommand`。

原则：
- 默认通过 `C.doc` 的包装能力使用
- 高层同步命令场景由 `CAD_coordination.send_cmd_with_sync` 处理
- 不要轻率绕开 `SafeDocumentWrapper`

## 连接失败时的策略

优先顺序：

1. 刷新 `C.li()`
2. 等待当前进程与 COM 就绪
3. 必要时执行环境重建
4. 必要时触发缓存自愈
5. 仍失败则明确报错

## 禁止行为

- 业务层自行建立新的 CAD 主连接入口
- 长期分散使用 `GetActiveObject / Dispatch`
- 轻率整体推翻 `licad.py`
- 轻率整体推翻 `CAD_selection.py`
- 混淆 `doc` 和 `raw_doc`
- 随意裸发 `SendCommand`
