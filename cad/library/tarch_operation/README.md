# tarch_operation

本目录是 `cad/library` 下的天正专项操作工作区。

当前第一批公共能力：

- `tarch_api.py`
  - 本目录面向外部调用的统一公共脚本
  - 已完成的天正操作函数统一继续往这个脚本收口
  - 当前已收口：
    - `write_tarch_single_line_text()`
    - `write_tarch_drawing_name()`
- `write_tarch_single_line_text()`
  - 使用 `system_files/天.dwg` 作为天正单行文字系统模板
  - 默认文字样式 `TARCH_CN_STANDARD`
  - `TARCH_CN_STANDARD` 默认使用 `宋体`
  - 默认高度 `3.5`
  - 默认宽度因子 `1`
  - 默认旋转角 `0`
  - 默认出图比例 `1:100`
  - 默认对齐方式 `左下`
  - 默认把文字外包盒锚点对齐到 `(0, 0, 0)`
- `write_tarch_drawing_name()`
  - 使用 `system_files/图名标注.dwg` 作为天正图名标注系统模板
  - 模板对象类型为 `TDbDrawingName`
  - 默认把图名标注外包盒左下角对齐到 `(0, 0, 0)` 后再移动到目标点
  - 默认比例文字按 `plot_scale` 自动生成，例如 `150 -> 1:150`
  - 默认显示比例为 `是`
  - 默认旋转角为 `0`
  - 默认图层为 `DIM_SYMB`

当前模板约定：

- 模板文件：`system_files/天.dwg`
- 模板对象：`TDbText`
- 模板图层：`PUB_TEXT`
- 模板样式：`TARCH_CN_STANDARD`
- 模板对象的外包盒左下角已校正到 `(0, 0, 0)`
- 模板文件：`system_files/图名标注.dwg`
- 模板对象：`TDbDrawingName`
- 模板图层：`DIM_SYMB`
- 模板对象的外包盒左下角已校正到 `(0, 0, 0)`

推荐入口：

```python
from library.tarch_operation.tarch_api import write_tarch_single_line_text

result = write_tarch_single_line_text(
    "建",
    target_point=(1000, 2000, 0),
    target_dwg_path=r"D:\path\to\target.dwg",
    plot_scale="1:100",
    save=True,
)
```

```python
from library.tarch_operation.tarch_api import write_tarch_drawing_name

result = write_tarch_drawing_name(
    "远程国际项目",
    target_point=(9000, 12300, 0),
    target_dwg_path=r"D:\codex-tasks\cad\tests\测试图名标注.dwg",
    plot_scale="1:150",
    save=True,
)
```

或：

```python
from library.tarch_operation import write_tarch_drawing_name, write_tarch_single_line_text
```

返回值：

- `dict`
- 关键字段包括：
  - `ok`
  - `entity`
  - `object_name`
  - `handle`
  - `doc_name`
  - `doc_fullname`
  - `bbox_min`
  - `bbox_max`
  - `saved`
  - `warnings`

实现策略：

- 连接统一走 `system.licad.C`
- 不直接依赖裸 `Dispatch/GetActiveObject`
- 这些函数默认假定天正 CAD 已由独立受控入口预先启动
- 这些函数默认要求当前机器上只有 1 个 CAD 进程，且该进程必须是健康的天正进程
- 若当前没有健康的天正运行时，这些函数应直接报错，而不是自行启动或重建天正
- 不走 GUI 点击
- 通过插入并炸开系统模板 `system_files/天.dwg` 得到新的 `TDbText`
- 通过插入并炸开系统模板 `system_files/图名标注.dwg` 得到新的 `TDbDrawingName`
- 再设置文字属性，并按外包盒锚点移动到目标点
- 若目标 DWG 不存在，则仅在当前已运行的天正会话中创建空白文件后再写入

注意：

- `tarch_operation` 不是天正启动入口，也不是环境恢复入口。
- `tarch_operation` 不是 CAD 多进程协调层。若检测到 0 个或超过 1 个 CAD 进程，应由外部受控入口先归一，再调用这里的函数。
- 测试运行必须同时启动 `D:/codex-tasks/cad/system/cad_test_supervisor.py`，并确认 `cad_dialog_killer.py` 已在运行。
- 一个测试任务完成后，应通过 `D:/codex-tasks/cad/system/CAD_core.py` 的受控关闭入口关闭天正 CAD，而不是把测试会话留在后台。
- `TDbDrawingName` 的 `图名样式`、`比例样式` 在当前天正环境下可能由对象内部或模板主导，代码里只做 best-effort 设置。
- 如果读回结果仍然是 `Standard`，应优先检查 `system_files/图名标注.dwg` 模板本身，而不是假设运行时字符串写入一定生效。
