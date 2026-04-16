# pywin32 Type Rules

## 核心原则

- ActiveX 文档里的 `Variant`、`Array`、`Collection` 不能直接照搬成 VBA 写法
- 在本项目里，优先先看已有包装器，再决定是否直打 COM
- 连接入口统一优先走 `from system.licad import C`

## 常见映射

- COM 对象：直接通过属性/方法访问，如 `C.doc.ActiveLayout`
- 集合：通常支持 `for item in collection` 和 `collection.Item(name_or_index)`
- 布尔值：直接用 Python `True/False`
- 枚举值：CHM 常给常量名，pywin32 实操中经常直接传整数

## 当前最重要的类型坑

- 三维点参数
- SAFEARRAY
- 返回集合的延迟枚举
- Busy 状态下的假失败
- 布局切换后上下文未同步
