# Filter Rules

## 直接跳过

以下页面默认记为 `skip`：

- `*_see_also.htm`
- `idx_*`
- `all_*`
- `idh_*`
- `IDH_*`
- 纯导航页

## 默认延后

以下页面默认记为 `defer`：

- `ex_*` 示例页
- 高级 3D 实体
- 曲面、材质、渲染、视觉样式
- 当前施工图自动化主链弱相关内容

## 默认保留

以下页面优先记为 `keep`：

- Application / Documents / Document
- ModelSpace / PaperSpace / Layout / Layouts / ActiveLayout
- SelectionSet / SelectionSets
- Block / BlockReference / AttributeReference
- GetAttributes / HasAttributes
- ObjectName / Handle / Layer / BoundingBox / Coordinates
- InsertBlock / AddLine / AddPolyline / AddText / AddMText
- GetVariable / SetVariable / Regen / SendCommand
- Plot / PlotConfiguration / RefreshPlotDeviceInfo / SetWindowToPlot

## 价值判断偏置

当前清单构建时优先偏向：

- 打印
- 布局
- 图签
- 块属性
- 目录
- 选择
- 施工图常见几何

对这些主题的命中，会提高 `value_level` 和 `status=keep` 的概率。
