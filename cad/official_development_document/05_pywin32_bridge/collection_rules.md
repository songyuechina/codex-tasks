# Collection Rules

## 常见集合

- `Documents`
- `Layouts`
- `Layers`
- `SelectionSets`
- `Blocks`

## 访问模式

```python
for layout in C.doc.Layouts:
    print(layout.Name)

layout = C.doc.Layouts.Item("布局1")
```

## 项目注意

- `Layouts` 的遍历顺序不一定等于标签页顺序
- `SelectionSets` 常需要先删同名旧集合，再新建
- 块属性集合前先检查 `HasAttributes`
