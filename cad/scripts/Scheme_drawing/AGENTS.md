# AGENTS.md

适用范围：`D:/codex-tasks/cad/scripts/Scheme_drawing/`

## 目录定位

这里不是通用 CAD 工具箱，而是“总图定位 / 外轮廓绘制”工作区。

当前统一入口是：

- `draw_building_outline.py`

凡是“根据坐标数据出总图定位 DWG”一类任务，优先复用它，不要先重写新脚本。

## 首先阅读什么

1. `README.md`
2. `draw_building_outline.quote.meta.json`
3. `draw_building_outline.procedure.meta.json`
4. `draw_building_outline_functions.quote.meta.json`
5. `draw_building_outline_functions.procedure.meta.json`

只有需要实现细节时再进源码。

## 当前硬规则

1. CAD 连接统一通过 `from system.licad import C`。
2. 不在业务层长期分散使用裸 `GetActiveObject / Dispatch / SendCommand`。
3. 日志统一使用 `system.common_logger.sys_logger`。
4. 默认能力必须包含：
   - 外轮廓绘制
   - 点位坐标标注
   - 保存 DWG
   - 关闭整个天正 / AutoCAD
5. 大地坐标与模型空间坐标轴按交换规则处理：输入 `(X, Y)`，落图 `(x, y) = (Y, X)`。
6. 坐标标注默认使用简单折线引线，文字使用当前默认字体。
7. 文字大小、引线长度等默认按模型空间 `1:1` 单位解释，不走标注比例缩放。

## 默认判断

- 用户只给图片时：
  优先找同名 sidecar 文本/JSON/CSV；没有再尝试 OCR。
- 用户只给结构化坐标时：
  优先直接读取结构化文件，不额外做图片识别。
- 用户没有明确要求时：
  默认输出到输入文件所在目录下的 `总图定位.dwg`。
- 用户没有明确禁止时：
  默认在保存后关闭整个 CAD 进程。

## 修改约束

- 不要绕过 `licad.C` 重新发明连接入口。
- 不要把本目录扩张成杂项脚本堆。
- 新增输入格式时，要先补四层 meta，再补 README 示例。
- 修改默认绘图/标注/关闭策略时，必须同步更新本文件和 `README.md`。

## 当前最重要的一句话

> 这个目录的目标不是“画一条线”，而是把坐标数据稳定地变成可交付的总图定位 DWG，并把标注、保存、收尾关闭做成可复用默认能力。
