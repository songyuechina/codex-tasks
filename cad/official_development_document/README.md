# CAD2021 CHM Local Retrieval System

本目录用于把 `acad_aag.chm` 与 `acadauto.chm` 转成一套面向智能体的本地检索体系。

第三轮后，这里不再只是“可查文档底座”，而是可直接支撑 Codex 组织 `pywin32` CAD 方法的工作区。

第四轮后，当前目标聚焦与本项目强相关的主题：

- 施工图自动化
- 打印
- 编目录
- 插图签
- 与施工图空间关系表达直接相关的三维能力
- pywin32 操作 CAD2021

第四轮的边界是：

- 应进入重点的 3D：
  - 三维坐标与坐标系
  - 三维路径 / 轮廓 / 区域 / 实体 / 剖切
  - 三维变换与空间对位
  - 由三维关系支撑二维施工图表达的方法
- 仍保持低频的 3D：
  - 渲染
  - 材质
  - 光照
  - 视觉样式
  - 纯展示型高级曲面与造型系统
  - 与当前施工图主链弱相关的 3D 浏览/展示主题

## 主入口

优先从以下层开始查：

1. `04_task_cards/`
   `04_task_cards/task_index.json` 是结构化主索引
2. `03_core_symbols/`
3. `05_pywin32_bridge/`
4. `06_on_demand_index/`
5. `02_manifest/page_manifest.jsonl`

第三轮新增的工作区入口：

- `AGENTS.md`
- `00_readme/PROMOTION_POLICY.md`
- `07_validation/hotspot_candidates.json`
- `07_validation/usage_feedback.jsonl`

第二轮补充后，`03_core_symbols/` 现在还应优先命中：

- `system_variables/`
- `types_and_variants/`

第三轮补充后，打印主链还要优先命中：

- `03_core_symbols/properties/ConfigName.md`
- `03_core_symbols/properties/CanonicalMediaName.md`
- `05_pywin32_bridge/plot_layout_rules.md`

第四轮补充后，三维空间表达任务还要优先命中：

- `00_readme/FOURTH_ROUND_GAP_ASSESSMENT.md`
- `00_readme/FOURTH_ROUND_SCOPE.md`
- `04_task_cards/10_3d_spatial_expression/`
- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/section_region_rules.md`

## 快速使用

```powershell
cd D:\codex-tasks\cad\official_development_document

powershell -ExecutionPolicy Bypass -File .\tools\extract_chm.ps1
py -3 .\tools\build_manifest.py
py -3 .\tools\build_core_symbols.py
py -3 .\tools\build_task_cards.py
py -3 .\tools\build_on_demand_index.py
py -3 .\tools\validate_doc_system.py

py -3 .\tools\build_task_cards.py

py -3 .\tools\search_cad_help.py task_id CAD2021-TASK-005
py -3 .\tools\search_cad_help.py function switch_to_layout
py -3 .\tools\search_cad_help.py module cad/system/CAD_core.py
py -3 .\tools\search_cad_help.py task "switch target layout"
py -3 .\tools\search_cad_help.py symbol SendCommand
py -3 .\tools\search_cad_help.py symbol TILEMODE
py -3 .\tools\search_cad_help.py symbol 3d_point
py -3 .\tools\search_cad_help.py symbol ConfigName
py -3 .\tools\search_cad_help.py symbol TranslateCoordinates
py -3 .\tools\search_cad_help.py symbol SectionSolid
py -3 .\tools\search_cad_help.py keyword "title block attribute"
py -3 .\tools\search_cad_help.py keyword "plot device media order"
py -3 .\tools\search_cad_help.py keyword "convert coordinates ucs ocs"
py -3 .\tools\search_cad_help.py keyword "region extrude section solid"
py -3 .\tools\search_cad_help.py task 切换布局
```

## 如何快速建立一个 pywin32 CAD 方法

建议固定按下面的顺序走：

1. 先查任务卡，确认任务入口、模块路径和现有项目函数
2. 再查核心符号，确认对象归属、属性/方法签名和风险
3. 再查 `05_pywin32_bridge/`，补顺序约束、类型规则和常见故障
4. 如果任务涉及空间关系表达，再补查三维规则和 `10_3d_spatial_expression/` 任务卡
5. 若仍缺关键内容，再查 `07_validation/hotspot_candidates.json` 与 `06_on_demand_index/`
6. 只有前面都不够时，才回到原始 HTML

输出的结果不应只是“某个 API 名字”，而应包括：

- 受控连接入口
- 操作顺序
- 项目内优先复用路径
- 验证方式
- 回退方式

打印主链的关键顺序，优先参考：

- `RefreshPlotDeviceInfo -> ConfigName -> RefreshPlotDeviceInfo -> CanonicalMediaName -> PlotRotation/CenterPlot -> SetWindowToPlot -> PlotType`

不要把这些打印属性继续当作长期低频对象处理。

三维空间表达主链的关键入口，优先参考：

- `TranslateCoordinates + Normal + Elevation*`
- `ActiveUCS + GetUCSMatrix + TransformBy`
- `Add3DPoly / AddRegion / AddExtrudedSolid / AddExtrudedSolidAlongPath / AddRevolvedSolid`
- `SectionSolid`

不要再把这些与空间关系表达直接相关的 3D 对象和方法一概视为低频主题。

## 项目内推荐路径

- 统一连接优先看 `D:/codex-tasks/cad/system/licad.py`
- 布局切换/布局枚举优先看 `D:/codex-tasks/cad/system/CAD_core.py`
- 选择与对象访问优先看 `D:/codex-tasks/cad/system/CAD_selection.py`
- 打印执行链优先看 `D:/codex-tasks/cad/scripts/drawing_basic_service/print/`
- 图签/目录/插块经验优先看 `D:/codex-tasks/cad/scripts/CAD_basic.py`

## 约束

- 先建索引，再扩摘要
- 任务卡是主入口，不按 CHM 原目录组织
- 主索引以 `task_id / symbol / owner / project_function / module_path` 为精确入口
- `aliases_en` 是主要自然语言扩展
- `aliases_zh / keywords_zh` 仅作辅助 alias，不作为主骨架
- 当低频对象阻塞打印/布局/图签/目录主链时，必须优先晋升，而不是继续留在 `06_on_demand_index`
- 当低频 3D 对象直接阻塞空间关系表达、剖切、轮廓、构件对位主链时，也必须触发晋升
- 每张任务卡都应补到 `source_topic_ids / source_html_paths / project_refs / rule_refs / reference_dwgs`
- 所有核心卡都要补 pywin32 视角和项目推荐路径
- 与当前目标弱相关的 CHM 页面默认只做轻量索引
