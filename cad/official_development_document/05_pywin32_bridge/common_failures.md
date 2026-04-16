# Common Failures

## Busy / Rejected

典型表现：

- RPC 被拒绝
- 调用偶发失败
- 刚切换布局马上读取失败

处理：

- 优先使用项目已有 `retry_on_busy`
- 切换后适度等待
- 必要时走命令回退

## 空间上下文错误

典型表现：

- 以为在布局，实际仍在模型空间
- `ActiveLayout` 切了，但对象容器没按预期理解

处理：

- 先确认当前布局名
- 再确认目标容器是 `ModelSpace`、`PaperSpace` 还是 `ActiveLayout.Block`

## 属性读取为空

典型表现：

- `GetAttributes()` 没值
- `TextString` 带格式前缀

处理：

- 先判 `HasAttributes`
- 对返回文本做清洗
- 可参考 `print_info_analysis.py` 和 `CAD_basic.py` 的属性清洗经验
