# Layout Plot Rules

本文件收口布局打印相关的 `pywin32` 顺序规则，供 Codex 快速组织稳定的打印方法。

## 1. 适用范围

适用于：

- 设置布局打印设备
- 切换纸张介质
- 按窗口打印 PDF
- 需要在 `Layout` 上写打印属性的方法

## 2. 推荐顺序

打印主链默认按下面的顺序写：

```python
layout.RefreshPlotDeviceInfo()
layout.ConfigName = printer_name
layout.RefreshPlotDeviceInfo()
layout.CanonicalMediaName = media_name
layout.PlotRotation = rotation
layout.CenterPlot = True
layout.SetWindowToPlot(lower_left, upper_right)
layout.PlotType = 4  # acWindow
```

若最终走 COM 直接输出，再进入：

```python
plot = C.doc.Plot
plot.QuietErrorMode = True
plot.PlotToFile(output_pdf)
```

若 COM 直接输出不稳定，再评估是否退回 `SendCommand`。

## 3. 为什么要遵守这个顺序

- `RefreshPlotDeviceInfo()` 决定布局当前可见的设备与纸张信息
- `ConfigName` 变更后，常常要再次刷新，才能拿到正确的介质列表
- `CanonicalMediaName` 与设备绑定，设备没定好时赋值很容易失效
- `SetWindowToPlot` 和 `PlotType` 的先后顺序会影响窗口打印是否真正生效

## 4. 常见失败点

- 没刷新设备就直接设置 `ConfigName`
- 切了 `ConfigName` 却没再次刷新就设置 `CanonicalMediaName`
- 在布局窗口未稳定时过早设置 `SetWindowToPlot`
- `PlotType` 没切到窗口模式
- 窗口点坐标顺序或类型不符合 `pywin32` 期待

## 5. 验证建议

- 回读 `layout.ConfigName`
- 回读 `layout.CanonicalMediaName`
- 回读 `layout.GetWindowToPlot()` 或项目内打印信息结构
- 最终校验输出 PDF 是否生成、页尺寸是否正确

## 6. 项目优先实现路径

- `cad/scripts/CAD_basic.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/drawing_basic_service/print/print_policy.py`
