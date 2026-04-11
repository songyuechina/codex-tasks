# Scheme Drawing

`D:/codex-tasks/cad/scripts/Scheme_drawing`

## 定位

本目录是“总图定位 / 建筑外轮廓绘制”执行工作区。

目标是把已有图片格式的大地坐标数据，或 JSON / CSV / TXT 等结构化坐标数据，直接转换成可交付的 DWG：

- 绘制建筑物闭合外轮廓
- 给每个轮廓点补齐坐标标注
- 保存为 `总图定位.dwg`
- 结束后关闭整个天正 / AutoCAD

## 当前主脚本

- `draw_building_outline.py`
  统一入口。默认执行：
  1. 读取坐标
  2. 新建 CAD 图纸
  3. 绘制闭合外轮廓
  4. 为每个点绘制简单折线引线
  5. 在引线上方写入 `X / Y` 双行坐标文字
  6. 保存 DWG
  7. 关闭整个天正 / AutoCAD

## 默认绘图规则

- 轮廓图层：`建筑外轮廓`
- 标注图层：`坐标标注`
- 大地坐标输入按 `(X, Y)` 理解，但写入 CAD 模型空间时统一映射为 `(x, y) = (Y, X)`
- 文字：使用当前 CAD 默认字体，不主动改文字样式
- 标注单位：按模型空间 `1:1` 单位写入
- 引线样式：简单折线，不使用复杂多重引线
- 默认输出：`D:/腾讯云工作台1#/私人住宅/张嘉辉/总图定位.dwg`
- 若未显式传 `--output`，默认输出到输入文件所在目录下的 `总图定位.dwg`

## 支持输入

- `json`
  支持 `points / vertices / coordinates / outline`
- `csv`
  支持 `x,y,z,seq` 形式或纯坐标行
- `txt`
  支持 `X ... / Y ...` 文本提取
- `png/jpg/jpeg/bmp/tif/tiff`
  优先读取同名 sidecar 文本/JSON/CSV；缺失时再尝试本地 OCR

## 示例

```powershell
python D:\codex-tasks\cad\scripts\Scheme_drawing\draw_building_outline.py `
  --source D:\codex-tasks\cad\scripts\Scheme_drawing\test_image1_points.json `
  --overwrite
```

若只想验证而暂不关闭 CAD：

```powershell
python D:\codex-tasks\cad\scripts\Scheme_drawing\draw_building_outline.py `
  --source D:\codex-tasks\cad\scripts\Scheme_drawing\test_image1_points.json `
  --output "D:\腾讯云工作台1#\私人住宅\张嘉辉\总图定位.dwg" `
  --overwrite `
  --no-shutdown-cad
```

## 阅读顺序

1. `README.md`
2. `AGENTS.md`
3. `draw_building_outline.quote.meta.json`
4. `draw_building_outline.procedure.meta.json`
5. `draw_building_outline_functions.quote.meta.json`
6. `draw_building_outline_functions.procedure.meta.json`
7. `draw_building_outline.py`
