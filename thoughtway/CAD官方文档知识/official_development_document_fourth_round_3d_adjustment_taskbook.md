# official_development_document 第四轮任务书

## 任务定位

本轮不是推翻第三轮成果，而是在第三轮已经可投入使用的基础上，做一次**方向性调整**：

- 保留当前围绕 **施工图自动化、打印、编目录、插图签** 的主链组织方式；
- 同时将**与施工图空间关系表达直接相关的三维绘图 / 建模内容**提升为重点；
- 仍然避免把体系扩散到与当前目标弱相关的渲染、材质、视觉样式、低频高级展示功能。

本轮要解决的核心问题是：

> 施工图自动化并不只是二维图元处理。为了表达建筑对象之间的空间关系、剖切关系、投影关系、构造位置关系，三维坐标、三维变换、区域/实体、剖切与由三维导出二维表达的方法，必须进入主干体系。

因此，第四轮结束后，`official_development_document` 应从：

- 以二维施工图主链为核心的官方文档检索底座

调整为：

- 以二维施工图主链为核心，同时把**空间关系表达所需的三维能力**纳入重点范围的官方文档检索底座

---

## 本轮最重要的前置要求

**在做任何调整前，先阅读并理解当前文件夹内已有文档。**

不要直接改代码或补卡片。

### 必读顺序

先按下面顺序阅读：

1. `README.md`
2. `00_readme/README_Codex_Workflow.md`
3. `00_readme/README_Task_Priority.md`
4. `00_readme/README_Filter_Rules.md`
5. `00_readme/PROMOTION_POLICY.md`
6. `04_task_cards/task_index.json`
7. `07_validation/hotspot_candidates.json`
8. `07_validation/usage_feedback.jsonl`
9. `tools/build_core_symbols.py`
10. `tools/build_task_cards.py`
11. `tools/search_cad_help.py`
12. `tools/validate_doc_system.py`

阅读后，先输出一个新的分析文件：

```text
00_readme/FOURTH_ROUND_GAP_ASSESSMENT.md
```

这个文件必须说明：

1. 第三轮体系当前把哪些内容视为主链；
2. 第三轮体系当前如何处理三维内容；
3. 哪些三维主题虽然在 `02_manifest` 中存在，但仍被停留在 `defer/skip`；
4. 哪些三维主题与施工图空间关系表达高度相关，应提升；
5. 哪些三维主题仍应保持低频层，不进入主干。

**在 `FOURTH_ROUND_GAP_ASSESSMENT.md` 完成前，不要开始改任务卡和核心卡。**

---

## 本轮的原则

### 原则 1：三维要进入重点，但不是全盘三维化

本轮提升的是：

- 与空间关系表达相关的三维坐标与坐标系
- 与对象空间定位相关的三维变换
- 与路径、轮廓、区域、剖切、投影有关的三维对象与方法
- 与由三维关系支撑二维施工图表达相关的方法

不是提升下面这些：

- 渲染
- 材质
- 光照
- 视觉样式美化
- 纯展示型高级曲面功能
- 与当前施工图主链弱相关的三维炫技对象

### 原则 2：三维重点必须服务于施工图自动化

所有新提升的三维对象、方法、任务卡，都必须明确说明它们服务于什么任务，例如：

- 空间位置表达
- 模型空间对象关系描述
- 由三维对象提取二维边界或剖切信息
- 路径、轴线、立面、剖面关系辅助表达
- 由三维构件关系推导二维施工图中的表达逻辑

如果某个三维主题不能明确服务于当前项目目标，则不要进入本轮主干。

### 原则 3：三维的提升必须按主干标准补全

一旦某个三维对象 / 方法被提升，不是简单改优先级，而是要按主干标准补齐：

- 核心符号卡
- `meta.json`
- 任务卡关联
- pywin32 规则
- 项目用途说明
- 验证要求
- 来源追踪

---

## 本轮需要重点提升的三维主题范围

下面这些是本轮建议重点扫描并提升的对象范围。

### A. 三维坐标与坐标系

必须重点检查并提升：

- `3d_point`
- `TranslateCoordinates`
- `ActiveUCS`
- `GetUCSMatrix`
- `Normal`
- `Elevation`
- `ElevationModelSpace`
- `ElevationPaperSpace`
- 相关 `WCS / UCS / OCS` 概念

理由：

这些是三维空间关系表达的基础，不理解这些，就无法稳定描述：

- 对象在三维空间中的位置
- 坐标变换
- 三维对象向二维表达的投影与基准
- 模型空间和图纸空间之间的定位关系

### B. 三维对象创建与轮廓表达

重点检查并提升：

- `3dPolyline`
- `Add3DPoly`
- `3DFace`
- `Add3DFace`
- `Region`
- `AddRegion`
- `3DSolid`
- `AddExtrudedSolid`
- `AddExtrudedSolidAlongPath`
- `AddRevolvedSolid`
- `SectionSolid`

理由：

这些对象和方法不是为了做复杂炫技建模，而是为了表达：

- 路径
- 轮廓
- 面
- 区域
- 体
- 剖切

而这些恰恰和施工图中轴线、轮廓、剖面、空间分区、构件关系等表达密切相关。

### C. 三维变换与空间调整

重点检查并提升：

- `Rotate3D`
- `Mirror3D`
- `ScaleEntity`
- `Move`
- `TransformBy`（若文档中存在）
- 与三维基点、法向量、旋转轴有关的方法和属性

理由：

施工图自动化中的很多空间关系表达，关键不在“是否能建模”，而在：

- 是否能正确放置
- 是否能以正确方向表达
- 是否能围绕正确轴线或平面变换
- 是否能在不同坐标基准下保持稳定

### D. 与二维图纸表达直接衔接的三维主题

重点检查并提升：

- 三维对象的边界 / 包围盒 / 坐标序列读取
- 三维对象剖切后产生二维参考信息的方法
- 模型空间中三维对象与布局 / 视口 / 打印表达关系相关的页面

理由：

本项目最终仍要落在施工图表达与打印，因此三维主题的重点不只是“造实体”，而是：

> 如何让三维关系进入二维图纸逻辑。

---

## 本轮仍然不作为重点的三维内容

下列内容原则上继续保持低频层，除非真实任务强行触发晋升：

- 材质
- 光照
- 渲染
- 视觉样式
- 纯展示型表面/曲面系统
- 与施工图自动化主链无关的高级造型内容
- 仅为视觉效果服务的三维浏览与展示主题

如果相关主题只出现在 `06_on_demand_index/` 即可，不进入主干层。

---

## 本轮要修改的关键文件

### 1. 更新总说明

修改：

- `README.md`
- `00_readme/README_Codex_Workflow.md`
- `00_readme/README_Task_Priority.md`
- `00_readme/README_Filter_Rules.md`

要求：

1. 删除或修正“默认不把 3D 作为主入口”的表述；
2. 改为“将与施工图空间关系表达相关的三维主题纳入重点”；
3. 明确区分：
   - 应提升的三维主题
   - 仍保持低频的三维主题
4. 在 `README_Task_Priority.md` 中把“复杂 3D 几何”这一条细分，不要再整块放在 `P2`。

### 2. 补新的 pywin32 规则文件

在 `05_pywin32_bridge/` 中新增至少下面这些文档：

- `coordinate_system_rules.md`
- `3d_transform_rules.md`
- `3d_entity_creation_rules.md`
- `section_region_rules.md`

每份文档至少说明：

- 主要对象 / 方法
- 典型参数形式
- 常见坐标系问题
- 常见失败模式
- 与二维施工图表达的关联
- 项目内的推荐使用场景

### 3. 补三维核心符号卡

在 `03_core_symbols/` 下新增或补齐：

#### objects
- `3dPolyline`
- `3DFace`
- `3DSolid`
- `Region`
- 如有必要可加 `UCS`

#### methods
- `TranslateCoordinates`
- `GetUCSMatrix`
- `Add3DPoly`
- `Add3DFace`
- `AddRegion`
- `AddExtrudedSolid`
- `AddExtrudedSolidAlongPath`
- `AddRevolvedSolid`
- `SectionSolid`
- `Rotate3D`
- `Mirror3D`
- `ScaleEntity`
- `TransformBy`（若存在）

#### properties
- `ActiveUCS`
- `Normal`
- `Elevation`
- `ElevationModelSpace`
- `ElevationPaperSpace`

#### types_and_variants
在现有基础上继续补与三维相关的：
- `ucs_matrix`
- `ocs_point`
- `normal_vector`
- `transform_matrix`
- `section_plane_definition`

### 4. 补三维任务卡

在 `04_task_cards/` 中新增专门分组：

```text
10_3d_spatial_expression
```

至少新增以下任务卡：

1. `understand_and_convert_coordinate_systems.md`
2. `create_3d_path_or_profile.md`
3. `create_region_and_extrude_solid.md`
4. `apply_3d_transform_to_objects.md`
5. `section_3d_geometry_for_2d_expression.md`
6. `read_3d_object_spatial_identity.md`

每张任务卡都必须说明：

- 该任务与施工图自动化的关系
- 哪些对象 / 方法是主入口
- 先查哪些规则文件
- 可能关联的项目路径
- 哪些仍需真实案例验证

### 5. 更新 `task_index.json`

要求：

- 为新增三维任务生成稳定的 `task_id`
- 将这些任务纳入主索引
- 保留 `task_id / symbol / owner / project_function / module_path` 为主骨架
- 中文别名继续只作为辅助层

### 6. 调整构建脚本

重点改：

- `tools/build_core_symbols.py`
- `tools/build_task_cards.py`

要求：

1. 不要只停留在原先二维主链的静态种子；
2. 把本轮新增的三维对象 / 方法 / 属性 / 类型也纳入种子；
3. 允许从 `02_manifest/page_manifest.jsonl` 中挑选与三维空间表达相关的高价值主题；
4. 不要机械地因为 `idh_` 命名就把相关页面永久排除掉；
5. 对本轮白名单内的三维 `idh_` 页允许进入核心候选集合。

### 7. 更新筛选规则

修改：

- `00_readme/README_Filter_Rules.md`
- `02_manifest/value_ranking.jsonl`（如有必要重建）

要求：

- 保持对 `see_also / idx / all_` 的强过滤；
- 但对与三维空间表达直接相关的对象 / 方法页，不能继续一概视为低优先级；
- 必须允许本轮白名单内的三维对象页和方法页从 `defer/skip` 升到核心候选层。

### 8. 更新验证层

修改：

- `07_validation/validation_tasks.md`
- `07_validation/validation_cases.json`
- `07_validation/hotspot_candidates.json`
- `07_validation/usage_feedback.jsonl`
- `tools/validate_doc_system.py`

要求：

新增三维相关验证问题，例如：

- 如何在不同坐标系间转换 3D 点
- 如何建立 3D 路径或轮廓
- 如何将闭合轮廓转为 Region 并挤出为 Solid
- 如何用三维变换调整对象位置和方向
- 如何剖切 3D 实体并为二维表达服务
- 如何读取三维对象的空间身份信息

同时，`validate_doc_system.py` 要新增检查：

- `10_3d_spatial_expression/` 分组存在
- 三维任务卡已进入 `task_index.json`
- 三维规则文件存在
- 新增核心卡与 `meta.json` 配对存在

---

## 本轮推荐的优先级重排

请修改 `00_readme/README_Task_Priority.md`，调整为如下思想。

### P0
保持不变的二维主链：

- 连接 AutoCAD / 获取活动文档
- 打开 / 保存 / 关闭文档
- 判断模型空间 / 图纸空间 / 当前布局
- 枚举布局
- 切换布局
- 选择集与对象识别
- 块属性读取 / 写入
- 打印信息读取与布局输出
- `SendCommand` 回退

### P1
本轮新增的三维重点：

- 坐标系转换与三维点表达
- 三维对象空间身份读取
- 三维路径 / 轮廓表达
- Region / Solid 的基础建构
- 三维变换与空间对位
- 剖切与由三维支持二维表达

### P2
仍保持次级：

- 复杂高级三维造型
- 曲面系统
- 渲染 / 材质 / 视觉样式
- 与当前业务弱相关的三维展示功能

---

## 本轮必须产出的新说明文件

新增：

```text
00_readme/FOURTH_ROUND_SCOPE.md
```

内容必须明确：

1. 本轮为什么提升三维；
2. 本轮提升的三维范围；
3. 本轮不提升的三维范围；
4. 三维提升如何服务施工图自动化；
5. 后续若真实任务继续触发更多三维主题，如何按晋升机制扩展。

---

## 本轮执行顺序

严格按这个顺序执行：

1. 阅读既有文档与脚本
2. 生成 `FOURTH_ROUND_GAP_ASSESSMENT.md`
3. 生成 `FOURTH_ROUND_SCOPE.md`
4. 修改 `README` 与优先级说明
5. 补三维规则文件
6. 补三维核心符号卡
7. 补 `10_3d_spatial_expression/` 任务卡
8. 更新 `task_index.json`
9. 调整构建脚本
10. 调整验证脚本与验证数据
11. 运行验证
12. 写出本轮变更总结

变更总结文件新增为：

```text
07_validation/fourth_round_change_log.md
```

---

## 本轮验收标准

第四轮完成后，验收标准不是“3D 内容更多了”，而是下面这些问题能快速回答：

1. 如果要表达一个构件在三维空间中的位置关系，先查哪里？
2. 如果要在不同坐标系之间转换点或对象，先查哪里？
3. 如果要通过三维轮廓生成 Region 或 Solid，先查哪里？
4. 如果要通过剖切或空间关系，为二维施工图表达提供依据，先查哪里？
5. Codex 是否能在不回到大量原始 HTML 的情况下，先命中三维相关任务卡、核心卡和规则文档？
6. 三维主题是否仍然保持“服务施工图自动化”的边界，而没有扩散成无关的 AutoCAD 三维百科？

只有满足上面这些，第四轮才算完成。

---

## 特别提醒

本轮最容易犯的错误是：

1. 把“提升三维重点”误解成“补很多三维页面”；
2. 把渲染、材质、视觉样式也拉进主干；
3. 继续沿用第三轮“默认压低 3D”的旧表述；
4. 只加一些 3D 关键词，却没有建立任务卡和规则层；
5. 没有先阅读现有文件，导致改动与第三轮体系脱节。

必须避免这些问题。

---

## 最终目标

第四轮完成后，这套系统应当能够同时支撑：

- 二维施工图主链任务
- 打印 / 编目录 / 插图签主链任务
- 与施工图空间关系表达直接相关的三维检索与实现导航

换句话说，目标不是把它做成“AutoCAD 全百科”，而是把它做成：

> **面向施工图自动化的 CAD 官方开发文档动态检索系统，其中三维空间表达已经成为正式重点之一。**
