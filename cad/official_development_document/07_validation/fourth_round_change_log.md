# Fourth Round Change Log

## 1. 本轮目标

第四轮没有推翻第三轮二维施工图、打印、图签、目录主链，而是在此基础上增加了正式的三维空间表达主干：

- 保留二维施工图自动化主链
- 保留打印 / 图签 / 目录主链
- 新增服务施工图空间关系表达的三维主干

## 2. 新增说明文件

- `00_readme/FOURTH_ROUND_GAP_ASSESSMENT.md`
- `00_readme/FOURTH_ROUND_SCOPE.md`

这两份文件分别负责：

- 说明第三轮的结构性缺口
- 明确第四轮提升范围与不提升范围

## 3. 说明层调整

已更新：

- `README.md`
- `00_readme/README_Codex_Workflow.md`
- `00_readme/README_Task_Priority.md`
- `00_readme/README_Filter_Rules.md`

调整结果：

- 删除了“默认不把 3D 作为主入口”的旧口径
- 改为“将与施工图空间关系表达直接相关的三维主题纳入重点”
- 保留对渲染、材质、视觉样式、纯展示型曲面系统的低频定位

## 4. 新增 pywin32 规则层

新增：

- `05_pywin32_bridge/coordinate_system_rules.md`
- `05_pywin32_bridge/3d_transform_rules.md`
- `05_pywin32_bridge/3d_entity_creation_rules.md`
- `05_pywin32_bridge/section_region_rules.md`

这四份规则文档分别收口：

- 坐标系和三维点
- 三维变换
- 三维路径 / 轮廓 / Region / Solid 创建
- 剖切与由三维导向二维表达

## 5. 核心符号层新增

已补到 `03_core_symbols/`：

- objects
  - `UCS`
  - `3dPolyline`
  - `3DFace`
  - `Region`
  - `3DSolid`
- methods
  - `TranslateCoordinates`
  - `GetUCSMatrix`
  - `Add3DPoly`
  - `Add3DFace`
  - `AddRegion`
  - `AddExtrudedSolid`
  - `AddExtrudedSolidAlongPath`
  - `AddRevolvedSolid`
  - `SectionSolid`
  - `Move`
  - `Rotate3D`
  - `Mirror3D`
  - `ScaleEntity`
  - `TransformBy`
- properties
  - `ActiveUCS`
  - `Normal`
  - `Elevation`
  - `ElevationModelSpace`
  - `ElevationPaperSpace`
- types_and_variants
  - `ucs_matrix`
  - `ocs_point`
  - `normal_vector`
  - `transform_matrix`
  - `section_plane_definition`

## 6. 任务卡层新增

新增任务组：

- `04_task_cards/10_3d_spatial_expression/`

新增任务卡：

- `CAD2021-TASK-020` `understand_and_convert_coordinate_systems`
- `CAD2021-TASK-021` `create_3d_path_or_profile`
- `CAD2021-TASK-022` `create_region_and_extrude_solid`
- `CAD2021-TASK-023` `apply_3d_transform_to_objects`
- `CAD2021-TASK-024` `section_3d_geometry_for_2d_expression`
- `CAD2021-TASK-025` `read_3d_object_spatial_identity`

`task_index.json` 和 `task_to_existing_code_map.json` 已同步重建。

## 7. 构建与验证层调整

已更新：

- `tools/build_core_symbols.py`
- `tools/build_task_cards.py`
- `tools/validate_doc_system.py`
- `07_validation/validation_tasks.md`
- `07_validation/validation_cases.json`
- `07_validation/hotspot_candidates.json`
- `07_validation/usage_feedback.jsonl`

关键变化：

- `build_core_symbols.py` 新增第四轮三维对象 / 方法 / 属性 / 类型种子
- 新增第四轮白名单，允许关键 `idh_*` 三维页面进入核心候选层
- `build_task_cards.py` 新增 `10_3d_spatial_expression` 组六张任务卡
- `validate_doc_system.py` 新增对三维任务组、三维规则文档、三维核心卡的显式检查

## 8. 验证结果

执行命令：

```powershell
py -3 .\tools\validate_doc_system.py
```

结果：

- `Validation passed.`
- `task_cards = 25`
- `core_symbol_cards = 81`
- `bridge_docs = 12`
- `fourth_round_3d_task_cards_present = true`
- `fourth_round_3d_core_symbols_present = true`
- `fourth_round_3d_rule_docs_present = true`

## 9. 当前结论

第四轮完成后，本目录已经从：

- 以二维施工图主链为核心的官方文档检索底座

调整为：

- 以二维施工图主链为核心，同时把服务施工图空间关系表达的三维能力纳入正式重点的官方文档检索底座
