# Codex Workflow

本体系的工作流固定为：

1. 解包 CHM 到 `01_extracted_html/`
2. 扫描全部页面，生成 `02_manifest/page_manifest.jsonl`
3. 明确 `keep / defer / skip`
4. 只对高频高价值主题生成：
   - `03_core_symbols/`
   - `04_task_cards/`
   - `05_pywin32_bridge/`
5. 对低频主题只保留 `06_on_demand_index/`
6. 用 `tools/search_cad_help.py` 查询，而不是重新手翻 CHM

第三轮新增硬规则：

> 当真实任务暴露某个低频对象已经影响打印、布局、图签、目录等主链实现时，必须优先补全该对象，而不是继续维持其低频状态。

第四轮新增硬规则：

> 当真实任务需要表达空间关系、剖切关系、投影关系、构件位置关系时，必须优先命中三维空间表达任务卡、核心卡和规则层，不再把相关 3D 主题整体压回低频层。

## 主索引字段

当前任务检索顺序固定为：

1. `task_id`
2. `symbol`
3. `owner`
4. `project_function`
5. `module_path`
6. `aliases_en`
7. `aliases_zh / keywords_zh` 仅作辅助

任务卡不是“支持中文查询”即成功。
成功标准是 Codex 能从任务快速落到稳定的模块路径、函数名、pywin32 规则和参考 DWG。

## 本项目检索顺序

1. 任务卡
   精确入口先查 `04_task_cards/task_index.json`
2. 核心符号
3. pywin32 规则
4. 低频索引
5. 原始 HTML

第二轮新增的稳定入口：

- `03_core_symbols/system_variables/`
- `03_core_symbols/types_and_variants/`
- `04_task_cards/task_index.json` 内的 `source_topic_ids / source_html_paths / rule_refs / project_refs`

第三轮新增的稳定入口：

- `AGENTS.md`
- `00_readme/PROMOTION_POLICY.md`
- `07_validation/hotspot_candidates.json`
- `07_validation/usage_feedback.jsonl`
- `05_pywin32_bridge/plot_layout_rules.md`

第四轮新增的稳定入口：

- `00_readme/FOURTH_ROUND_GAP_ASSESSMENT.md`
- `00_readme/FOURTH_ROUND_SCOPE.md`
- `04_task_cards/10_3d_spatial_expression/`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/section_region_rules.md`

## 第三轮工作流

1. 先查现有体系
2. 完成当前任务
3. 记录缺失信息
4. 判断是否触发晋升评估
5. 若触发，则补核心卡 / 任务关联 / 规则 / 验证
6. 更新热点清单与晋升日志

## 第四轮工作流补充

当任务属于下面任一情况时，必须走第四轮三维主干：

- 需要描述构件在三维空间中的位置关系
- 需要在 `WCS / UCS / OCS` 之间转换点或对象
- 需要把轮廓转成 `Region` 或 `3DSolid`
- 需要用剖切结果支撑二维施工图表达
- 需要通过三维变换完成空间对位

固定顺序：

1. 先查 `04_task_cards/task_index.json`
2. 若命中空间关系任务，优先查 `04_task_cards/10_3d_spatial_expression/`
3. 再查对应核心符号
4. 再查三维 pywin32 规则
5. 若仍不足，再查 `06_on_demand_index/`
6. 最后才回原始 HTML

## 如何用本体系组装一个 pywin32 CAD 方法

固定输出模板应覆盖：

1. 受控入口
2. 相关任务卡
3. 相关核心符号
4. 关键 pywin32 规则
5. 项目实现路径
6. 验证步骤
7. 回退路径

打印类方法还必须额外检查：

- 打印设备刷新顺序
- 设备与纸张介质的绑定关系
- 打印窗口坐标格式
- 失败时是否应退回 `SendCommand`

空间表达类方法还必须额外检查：

- 当前点是 `WCS / UCS / OCS / DCS` 中的哪一种
- 当前 `Elevation*` 是否会隐式补 `Z`
- 当前对象是否需要 `Normal`
- 当前变换是围绕轴、平面还是 4x4 矩阵
- 最终输出如何回到二维施工图表达

## 当前优先主题

- 获取活动文档
- 布局枚举与切换
- 模型/图纸空间判断
- 选择集与对象遍历
- 块属性读取
- 插入块/插入 DWG
- 打印信息读取
- 布局输出与命令回退
- 图签属性回写
- 目录生成/目录图签更新
- 坐标系转换与三维点表达
- 三维对象空间身份读取
- 三维路径 / 轮廓 / Region / Solid
- 三维变换与剖切
