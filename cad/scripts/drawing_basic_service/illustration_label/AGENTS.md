# AGENTS.md

适用范围：`D:/codex-tasks/cad/scripts/drawing_basic_service/illustration_label/`

本文件用于让进入本目录的新智能体快速接手“插图签”工作。

这里的“插图签”不是单一动作，而是一条受控服务链，通常包含：

- 替换目标 DWG 中 `A0 / A1 / A2 / A3` 同名块定义
- 为缺少内框的打印区域补标准图框
- 为已经有标准内框的打印区域插入真正的图签块

## 1. 进入本目录先看什么

优先阅读：

1. `README.md`
2. `folder.meta.json`
3. `illustration_frame_service.quote.meta.json`
4. `illustration_frame_service.procedure.meta.json`

再进入代码：

5. `illustration_block_service.py`
6. `illustration_frame_service.py`
7. `replace_defined_blocks.py`
8. `insert_illustration_labels.py`
9. `insert_illustration_title_blocks.py`

若没先完成上述阅读，不应直接改代码或直接操作真实 DWG。

## 2. 本目录当前已落地的服务

### 服务 A：替换同名图签块定义

目标：

- 用源 DWG 中的 `A0 / A1 / A2 / A3` 块定义替换目标 DWG 中的同名块定义

入口：

- `replace_defined_blocks.py`

核心模块：

- `illustration_block_service.py`

### 服务 B：补标准图框

目标：

- 按打印区域分析结果，为缺少内框的打印区域插入标准图框

入口：

- `insert_illustration_labels.py --frames-only`

核心模块：

- `illustration_frame_service.py`

### 服务 C：插入图签块

目标：

- 对已经有标准内框的打印区域插入真正的 `A0 / A1 / A2 / A3` 图签块

入口：

- `insert_illustration_title_blocks.py`
- `insert_illustration_labels.py`

核心模块：

- `illustration_frame_service.py`

## 3. 最关键的业务共识

### 3.1 默认打印区域模式

默认使用：

- `purified_adaptive`

含义：

- 任何合理的矩形多段线都尽量匹配一个标准打印区域规格

除非用户明确要求 `basic`，否则不要主动切换到严格模式。

### 3.2 内框判定

若某打印区域内部存在一个矩形多段线，并且：

- 面积比 > 85%

则视为该打印区域已经有内框，不再插标准图框。

### 3.3 标准图框处理

当打印区域缺少内框时，必须按以下流程处理：

1. 将对应 `standard_drawing_frame/*.dwg` 先作为块插入
2. 按目标打印区域外包盒进行缩放、旋转、对齐
3. 删除原始打印区域矩形多段线
4. 炸开块
5. 若缩放比例不是 `x=1,y=1`，则重建外框与内框多段线，修正 AutoCAD 炸开后的错误几何

### 3.4 图签块处理

这里最容易做错。

真正插入的图签块，不是把 `A0_H.dwg / A1_H.dwg / A2_H.dwg / A3_H.dwg` 作为外层文件块直接放进目标图。

正确流程是：

1. 从 `A0_H.dwg / A1_H.dwg / A2_H.dwg / A3_H.dwg` 内部提取真实块定义 `A0 / A1 / A2 / A3`
2. 将这些真实块定义导入或替换到目标 DWG
3. 再把 `A0 / A1 / A2 / A3` 这个内部块定义插入目标打印区域

### 3.5 什么叫“真正的图签块”

必须满足：

- 块名是 `A0` 或 `A1` 或 `A2` 或 `A3`
- 块定义来自 `A0_H / A1_H / A2_H / A3_H` 文件内部
- 块定义内部有两根 `Defpoints` 图层的多段线
- 这两根多段线颜色索引应为 `1` 和 `3`

如果只看到同名块、但没有这个签名特征，就不能认定为正确图签块。

## 4. 资源目录规则

### 标准资源

- `standard_drawing_frame/`

包含：

- 标准图框文件：`A0.dwg`、`A1.dwg`、`A2.dwg`、`A3.dwg` 及其加长规格
- 标准图签来源文件：`A0_H.dwg`、`A1_H.dwg`、`A2_H.dwg`、`A3_H.dwg`

### 用户资源

- `user_frame/`

规则：

1. 若 `user_frame` 已有 `A0_H.dwg / A1_H.dwg / A2_H.dwg / A3_H.dwg`，优先使用用户文件
2. 若缺失，则从 `standard_drawing_frame/` 自动复制默认文件
3. 使用完成后，清空 `user_frame`

## 5. 坐标与对齐规则

### 图框

横向：

- 外包盒右下角对齐目标打印区域右下角

竖向：

- 旋转 `-90°`
- 外包盒左下角对齐目标打印区域左下角

### 图签

横向：

- 按内框右下角对齐

竖向：

- 旋转 `-90°`
- 按内框左下角对齐

若仅对齐锚点后尺寸仍不一致，则按内框尺寸做等比例缩放。

## 6. 入口脚本与使用边界

### `replace_defined_blocks.py`

用于：

- 只做 `A0 / A1 / A2 / A3` 同名块定义替换

不要把“补图框”或“插图签”逻辑继续堆到这个入口。

### `insert_illustration_labels.py`

用于：

- 完整链处理
- 只补标准图框
- 图框 + 图签一起做
- 先替换同名块再插图签

### `insert_illustration_title_blocks.py`

用于：

- 目标 DWG 已经完成标准图框处理，只需要插图签

## 7. 强制规则

1. CAD 连接统一通过 `CAD_core.litz()`、`open_file()` 和 `from system.licad import C`
2. 真实执行时必须明确 `cad_runtime_guard.py` 监督链是否已运行
3. 入口脚本负责 bootstrap，业务模块禁止自行修改 `sys.path`
4. 日志统一使用 `system.common_logger.sys_logger`
5. 测试文件统一放在 `D:/codex-tasks/cad/tests`
6. 真实测试或回归前先保留备份
7. 遇到 busy / rejected / RPC 错误，优先等待与重试，不要直接判死
8. 不要把 `A0_H / A1_H / A2_H / A3_H` 外层文件块错误保留为最终图签结果

## 8. 修改策略

优先：

- 复用 `cad/system` 与 `cad/library` 的稳定能力
- 复用 `print/print_area_analysis.py` 的打印区域分析能力
- 让入口脚本保持薄，业务逻辑收束到服务模块
- 修改后用真实 DWG 或测试 DWG 验证结果

避免：

- 在多个脚本里复制同一套图签处理逻辑
- 绕开 runtime guard 去做真实 CAD 操作
- 只按块名判断图签块真伪
- 直接把外层模板文件块插进去就认为完成任务

## 9. 接手任务时先判断什么

进入具体任务后，优先判断：

1. 用户是要替换块定义、补图框、插图签，还是完整链
2. 目标 DWG 是否已经有标准内框
3. 用户是否提供自定义 `A0_H / A1_H / A2_H / A3_H`
4. 是否只处理 `purified_adaptive`
5. 是否需要先从备份恢复测试文件
6. 是否需要在执行后用 COM 再校验块定义签名

## 10. 最后一条共识

本目录的成功标准，不是“脚本跑完了”，而是：

- 打印区域识别正确
- 标准图框插入正确
- 最终插入的是内部真实图签块 `A0 / A1 / A2 / A3`
- 这些块定义带有 `Defpoints` 的红绿两根多段线特征
- 结果可通过 JSON 返回值和 COM 二次检查共同验证
