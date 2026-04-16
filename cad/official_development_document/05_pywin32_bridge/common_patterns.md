# Common Patterns

## 连接并拿活动文档

```python
from system.licad import C

doc = C.doc
```

## 枚举布局

```python
for layout in C.doc.Layouts:
    print(layout.Name)
```

## 按块属性取图签字段

```python
if block_ref.HasAttributes:
    for attr in block_ref.GetAttributes():
        print(attr.TagString, attr.TextString)
```

## 布局打印执行链

推荐先看：

- `print_policy.py`
- `print_info_analysis.py`
- `print_executor.py`

而不是直接手写零散 Plot 调用。
