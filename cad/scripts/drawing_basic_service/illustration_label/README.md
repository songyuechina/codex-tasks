# Illustration Label Service

本目录是 `D:/codex-tasks/cad/scripts/drawing_basic_service/illustration_label` 的插图签执行工作区。

目标不是只提供一个函数，而是提供一组可直接落地的插图签服务，让智能体进入本目录后可以快速判断：

- 当前任务是替换图签块定义，还是插标准图框，还是插图签块，还是三者联动
- 用户应该提供什么 DWG
- 默认会做什么，不会做什么
- 真正执行时该用哪个入口脚本
- 结果应该如何验证

## 先看什么

进入本目录后，优先阅读：

1. `README.md`
2. `folder.meta.json`
3. `illustration_frame_service.quote.meta.json`
4. `illustration_frame_service.procedure.meta.json`

若需要进入代码，再看：

- `illustration_block_service.py`
- `illustration_frame_service.py`
- `replace_defined_blocks.py`
- `insert_illustration_labels.py`
- `insert_illustration_title_blocks.py`

## 本目录包含的能力

当前已经落地 3 类能力。

### 1. 替换目标 DWG 中已定义的标准块

用途：

- 把目标文件 `A.dwg` 中的 `A0 / A1 / A2 / A3` 块定义替换成来源文件 `B.dwg` 中的同名块定义
- 用于用户后续用自定义图签块接管系统默认图签块

入口：

- `replace_defined_blocks.py`

核心服务：

- `illustration_block_service.replace_defined_blocks`

典型场景：

- 用户已经准备好了自己的 `A0 / A1 / A2 / A3` 图签块，希望替换目标 DWG 中已有同名标准块

### 2. 插入标准图框

用途：

- 对任何合理的矩形打印区域，在适配模式下匹配一个标准图纸规格
- 若该打印区域内部没有内框线，则插入对应标准图框
- 图框来源于 `standard_drawing_frame/*.dwg`

入口：

- `insert_illustration_labels.py --frames-only`

核心服务：

- `illustration_frame_service.apply_illustration_labels(..., insert_titles=False)`

典型场景：

- 目标 DWG 中只有打印区域外框，没有内框和附加块
- 目标 DWG 已经做过外框处理，但要重新做回归验证

### 3. 插入图签块

用途：

- 对已经有标准内框的打印区域，插入真正的图签块 `A0 / A1 / A2 / A3`
- 图签块不是随便的同名块，必须来自 `A0_H.dwg / A1_H.dwg / A2_H.dwg / A3_H.dwg` 内部的真实块定义

入口：

- `insert_illustration_title_blocks.py`
- `insert_illustration_labels.py`（完整链，图框 + 图签）

核心服务：

- `illustration_frame_service.apply_illustration_labels(..., insert_titles=True)`

典型场景：

- 目标 DWG 已经完成标准图框处理，现在只差插图签
- 用户没有自定义图签模板，要先用系统默认图签块

## 标准资源与用户资源

### 标准图框资源

目录：

- `standard_drawing_frame/`

内容：

- `A0.dwg`
- `A0_1_8.dwg`
- `A0_1_4.dwg`
- `A1.dwg`
- `A1_1_4.dwg`
- `A1_1_2.dwg`
- `A1_3_4.dwg`
- `A2.dwg`
- `A2_1_4.dwg`
- `A2_1_2.dwg`
- `A2_3_4.dwg`
- `A3.dwg`

这些文件用于插标准外框和内框。

### 标准图签模板资源

目录：

- `standard_drawing_frame/`

内容：

- `A0_H.dwg`
- `A1_H.dwg`
- `A2_H.dwg`
- `A3_H.dwg`

这些文件不是直接作为最终图签放进目标 DWG 的“结果块”。
它们的作用是提供内部真实块定义 `A0 / A1 / A2 / A3`。

### 用户图签模板资源

目录：

- `user_frame/`

规则：

- 若 `user_frame` 中已有 `A0_H.dwg / A1_H.dwg / A2_H.dwg / A3_H.dwg`，优先使用用户文件
- 若缺失，则从 `standard_drawing_frame` 自动复制默认文件到 `user_frame`
- 使用完成后，脚本会清空 `user_frame`

## 什么叫“真正的图签块”

这是本目录最重要的约束之一。

正确的图签块不是“名字碰巧叫 A0 / A1 / A2 / A3 的任意块”。
真正可接受的图签块定义，必须满足以下特征：

- 块名是 `A0` 或 `A1` 或 `A2` 或 `A3`
- 块定义来自 `A0_H.dwg / A1_H.dwg / A2_H.dwg / A3_H.dwg` 内部
- 块定义内部包含两根 `Defpoints` 图层的多段线
- 这两根多段线的颜色特征分别是红色与绿色

当前实现会在导入和插入后做校验，避免把外层文件块或错误的同名块当成图签块。

## 默认工作方式

### 打印区域识别

默认使用：

- `purified_adaptive`

含义：

- 任何合理的矩形多段线都尽量匹配到 288 种标准打印区域中的一个标准规格
- 用户没有显式要求时，不走严格 `basic`

### 内框存在判定

对某个打印区域：

- 若其内部存在一个矩形多段线
- 且该矩形多段线面积 / 打印区域面积 > 85%

则判定该打印区域已经有内框线，不再插标准图框。

### 横向与竖向

横向：

- 图框按外包盒右下角对齐
- 图签按内框右下角对齐

竖向：

- 图框插入后旋转 `-90°`
- 图框按外包盒左下角对齐
- 图签插入后旋转 `-90°`
- 图签按内框左下角对齐

### 图框炸开规则

当某打印区域缺少内框时：

1. 先把标准图框 DWG 作为块插入
2. 按目标打印区域外包盒做缩放、旋转、对齐
3. 删除原始打印区域外框
4. 炸开块

若缩放比例不是 `x=1,y=1`，AutoCAD 会把原本的多段线炸坏。
因此当前实现会在炸开后重建：

- 宽度为 `0` 的外框矩形多段线
- 宽度为 `min(scale_x, scale_y) * 100` 的内框矩形多段线

并删除炸开后产生的错误线段。

### 图签插入规则

图签处理不是把 `A0_H.dwg` 这个文件块直接留在目标图里。
真实流程是：

1. 从 `A0_H.dwg / A1_H.dwg / A2_H.dwg / A3_H.dwg` 中导入或替换内部块定义 `A0 / A1 / A2 / A3`
2. 按打印区域规格家族选择 `A0 / A1 / A2 / A3`
3. 把这个内部块定义插入目标打印区域
4. 插入后按内框锚点对齐
5. 若尺寸不一致，做等比例缩放
6. 再次校验插入的块引用确实指向真实图签块定义

注意：

- 当前图签块默认保留为块引用，不做炸开
- 若用户任务明确要求“插入后再炸开图签块”，应在新任务中单独说明

## 用户如何正确提需求

智能体接到任务时，优先把用户需求归入以下 4 类之一。

### 类型 A：只替换块定义

用户要表达清楚：

- 目标文件路径
- 源文件路径
- 要替换的块名，通常是 `A0 A1 A2 A3`

典型表达：

- “把 B.dwg 中的 A0 A1 A2 A3 替换到 A.dwg”

### 类型 B：只补标准图框

用户要表达清楚：

- 目标 DWG 路径
- 是否只做净化适配模式
- 是否只处理缺内框的打印区域

典型表达：

- “按适配模式给这个 DWG 中所有合理打印区域补标准图框，不插图签”

### 类型 C：只插图签

用户要表达清楚：

- 目标 DWG 路径
- 该文件是否已经处理好标准图框
- 是否使用 `user_frame` 中的用户自定义模板

典型表达：

- “对这个已处理好外框的 DWG 插图签”

### 类型 D：完整链

用户要表达清楚：

- 目标 DWG 路径
- 是否使用用户自定义图签源
- 是否要同时补外框与插图签

典型表达：

- “按适配模式处理这个 DWG，缺内框就补标准图框，再插图签”

## 命令行使用方法

### 1. 替换 A0/A1/A2/A3 同名块定义

```powershell
cd D:\codex-tasks\cad\scripts\drawing_basic_service\illustration_label

py -3 .\replace_defined_blocks.py `
  --target D:\path\A.dwg `
  --source D:\path\B.dwg `
  --names A0 A1 A2 A3
```

需要属性同步时：

```powershell
py -3 .\replace_defined_blocks.py `
  --target D:\path\A.dwg `
  --source D:\path\B.dwg `
  --names A0 A1 A2 A3 `
  --run-attsync
```

### 2. 只补标准图框

```powershell
py -3 .\insert_illustration_labels.py `
  --target D:\path\target.dwg `
  --match-mode purified_adaptive `
  --frames-only
```

### 3. 图框 + 图签一起做

```powershell
py -3 .\insert_illustration_labels.py `
  --target D:\path\target.dwg `
  --match-mode purified_adaptive
```

若要先把用户自定义 `A0/A1/A2/A3` 同名块替换进目标图，再插图签：

```powershell
py -3 .\insert_illustration_labels.py `
  --target D:\path\target.dwg `
  --title-source D:\path\custom_title_blocks.dwg `
  --match-mode purified_adaptive
```

### 4. 只对已完成图框处理的 DWG 插图签

```powershell
py -3 .\insert_illustration_title_blocks.py `
  --target D:\path\target.dwg `
  --match-mode purified_adaptive
```

## 类似函数的输入输出说明

虽然这里主要按脚本服务使用，但可以把 `apply_illustration_labels` 理解成目录核心服务。

### 服务输入

核心参数：

- `target_file`
  目标 DWG
- `title_block_source_file`
  可选。若提供，则先用该文件中的 `A0 / A1 / A2 / A3` 替换目标文件同名块定义
- `block_names`
  默认 `A0 A1 A2 A3`
- `match_mode`
  `basic / adaptive / purified_adaptive`，默认 `purified_adaptive`
- `ensure_guard`
  是否确保监督链存在，默认 `True`
- `run_attsync`
  块定义替换后是否执行 `ATTSYNC`
- `insert_titles`
  是否插图签

### 服务输出

返回 JSON 风格结果，核心字段包括：

- `ok`
- `target_file`
- `match_mode`
- `replace_summary`
- `title_asset_summary`
- `print_area_count`
- `results`

其中 `results` 的每一项会给出：

- `handle`
- `owner`
- `plot_name`
- `paper_code`
- `ratio`
- `orientation`
- `standard_match`
- `frame_inserted`
- `frame_already_present`
- `title_inserted`
- `title_already_present`
- `inner_frame_bbox`
- `status`
- `message`

这组结果就是后续自动验证与回归分析的主要依据。

## 执行要求

### 1. 测试文件位置

统一放在：

- `D:/codex-tasks/cad/tests`

### 2. 真实运行时监督链

真实执行时必须遵守：

- 同时运行 `D:/codex-tasks/cad/system/cad_runtime_guard.py`

入口脚本默认会尝试拉起：

- `cad_dialog_killer.py`
- `cad_command_monitor.py`
- `cad_runtime_guard.py`

### 3. 备份要求

对真实测试文件或用户文件，修改前应先保留备份。

### 4. 不要误用的方式

不要把以下对象误当成最终图签块：

- `A0_H.dwg / A1_H.dwg / A2_H.dwg / A3_H.dwg` 作为外层文件块直接留在目标图里
- 任意名字叫 `A0 / A1 / A2 / A3` 但不带 `Defpoints` 红绿多段线特征的错误块

## 如何验证结果

至少验证以下几项。

### 图框验证

- 每个打印区域都被识别
- 缺内框的打印区域已经补上标准内框
- 竖向打印区域的标准图框方向正确

### 图签验证

- 目标 DWG 中存在 `A0 / A1 / A2 / A3` 块定义
- 这些块定义内部包含两根 `Defpoints` 多段线
- 两根多段线颜色索引分别为 `1` 和 `3`
- 目标 DWG 中没有把 `A0_H / A1_H / A2_H / A3_H` 外层文件块错误地保留下来作为图签结果

### 服务结果验证

- 返回结果中 `ok=true`
- `print_area_count` 合理
- 每个区域的 `status=ok`
- `frame_inserted / frame_already_present / title_inserted / title_already_present` 符合现场状态

## 当前建议的接手策略

若将来有新智能体进入本目录，建议按以下顺序判断任务：

1. 用户是要替换图签块定义，还是补图框，还是插图签，还是完整链
2. 目标 DWG 是否已经有标准内框
3. 用户是否提供了自定义 `A0_H / A1_H / A2_H / A3_H`
4. 若没有用户模板，是不是要回退到系统默认模板
5. 是否需要在执行前恢复备份并在执行后做 COM 验证

一句话总结：

本目录的“插图签”不是单一步骤，而是一条受控服务链：

- 先识别打印区域
- 再补标准图框
- 再导入真实图签块定义
- 再按内框锚点插入正确图签块
- 最后用结果 JSON 和块定义签名一起验证
