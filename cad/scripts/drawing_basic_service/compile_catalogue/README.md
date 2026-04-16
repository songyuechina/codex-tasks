# Compile Catalogue

本目录负责“编目录”执行链。

当前入口：

- `compile_catalogue.py`
- `compile_catalogue_service.py`

当前主流程：

1. 通过 `print` 主链取出目标 DWG 的打印区域。
2. 若缺少标准内框，调用 `illustration_label` 补标准图框。
3. 若缺少角点对齐图签块，调用 `illustration_label` 插图签。
4. 逐个打印区域收集图纸名称、图纸编号、图签信息区域。
5. 对缺失图名/图号的打印区域执行补写。
6. 复制 `directory_template/目录模板1.dwg` 到 `user_directory/`，生成 `<目标文件名>_目录.dwg`。
7. 按固定行列坐标写入目录内容。
8. 若第二目录页未使用，则删除第二目录页完整打印区域。
9. 将保留目录页复制回目标 DWG 的首个选中打印区域前方，水平间距为该首打印区域宽度的 `1/8`，并以下边对齐。

当前新增约定：

- 当布局空间在 `basic` 下未识别到有效打印区域时，会自动回退到 `adaptive` 再试一次。
- 返回 JSON 结果中包含 `started_at`、`finished_at`、`elapsed_seconds`、`stage_durations`，用于观察编目录全流程耗时。

当前默认值：

- 取区模式：`basic`
- 图号前缀：`JS-`
- 目录标题：`图纸目录`

示例：

```powershell
py -3 .\compile_catalogue.py `
  --dwg D:\codex-tasks\cad\tests\编目录测试_1.dwg `
  --output-json D:\codex-tasks\cad\scripts\drawing_basic_service\compile_catalogue\user_directory\编目录测试_1_目录.json
```
