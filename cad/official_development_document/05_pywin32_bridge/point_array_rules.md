# Point Array Rules

## 三维点

许多 CAD COM 方法要求三维点，即使你只在 2D 平面工作，也应传 `(x, y, z)`。

本项目常见形式：

```python
(0, 0, 0)
(x, y, 0.0)
```

更稳的写法可参考 `licad.py` 里通过 `VARIANT` 构造点数组的方式。

## 当前高频场景

- `AddLine(start_point, end_point)`
- `InsertBlock(insertion_point, path, sx, sy, sz, rotation)`
- `SetWindowToPlot(lower_left, upper_right)`

## 实务建议

- 点统一补成三元组
- 混用整数和浮点通常没问题，但批量任务建议统一为浮点
- 布局打印窗口点要确认坐标系处于预期空间
