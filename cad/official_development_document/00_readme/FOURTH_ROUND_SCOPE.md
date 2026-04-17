# Fourth Round Scope

## 1. 本轮为什么提升三维

第三轮已经把二维施工图、图签、目录、打印主链组织起来了，但这还不够支撑完整的施工图自动化。

原因很直接：

- 施工图里的轴线、轮廓、构件位置、立剖关系，本质上都依赖空间关系
- `TranslateCoordinates / ActiveUCS / GetUCSMatrix / Normal / Elevation*` 决定了对象在不同坐标基准下如何被稳定描述
- `Region / 3DSolid / SectionSolid` 决定了三维构件如何转回二维剖切或边界表达
- `Rotate3D / Mirror3D / ScaleEntity / TransformBy` 决定了对象是否能在正确基准下完成空间对位

所以第四轮不是“给 3D 加一点补丁”，而是把“服务施工图空间关系表达的三维能力”正式纳入主干。

## 2. 本轮提升的三维范围

### 2.1 坐标与坐标系

纳入重点：

- `3d_point`
- `TranslateCoordinates`
- `ActiveUCS`
- `GetUCSMatrix`
- `UCS`
- `Normal`
- `Elevation`
- `ElevationModelSpace`
- `ElevationPaperSpace`
- `WCS / UCS / OCS / DisplayDCS / PaperSpaceDCS`

### 2.2 三维轮廓、区域、实体、剖切

纳入重点：

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

### 2.3 三维变换与空间对位

纳入重点：

- `Move`
- `Rotate3D`
- `Mirror3D`
- `ScaleEntity`
- `TransformBy`
- `ucs_matrix`
- `ocs_point`
- `normal_vector`
- `transform_matrix`
- `section_plane_definition`

## 3. 本轮不提升的三维范围

以下内容继续保持低频层，不进入第四轮主干：

- 渲染
- 材质
- 光照
- 视觉样式
- 纯展示型高级曲面
- 与施工图自动化主链弱相关的高级造型系统
- 仅为视觉浏览服务的 3D 展示能力

它们可以继续存在于 `06_on_demand_index/`，但不应占用主干卡片、任务卡和规则层容量。

## 4. 三维提升如何服务施工图自动化

第四轮提升的三维主题，必须明确落到下面这些任务目标之一：

- 表达对象在三维空间中的位置关系
- 在 `WCS / UCS / OCS` 之间稳定换算点和对象
- 建立路径、轮廓、面、区域、体的受控表达
- 从闭合轮廓进入 `Region`，再进入 `Solid`
- 通过三维变换完成构件对位、方向修正和基准统一
- 通过 `SectionSolid` 或几何边界读取，为二维剖面、立面、轮廓输出提供依据
- 把三维关系转成可落到布局、视口、打印逻辑的二维表达支持

如果某个三维主题不能落到这些目标，就不属于本轮主干。

## 5. 本轮执行边界

第四轮要做的是：

- 改写 README 和工作流说明，停止沿用“默认压低 3D”的旧表述
- 建立专门的三维 pywin32 规则层
- 建立三维核心卡
- 建立 `10_3d_spatial_expression/` 任务组
- 调整构建脚本与验证脚本，让这些主题能被系统性维护

第四轮不做的是：

- 把所有 3D 页面一股脑升入核心层
- 脱离施工图主链去整理无关 3D 百科
- 让渲染、材质、视觉样式抢占主干优先级

## 6. 后续如何继续扩展

如果后续真实任务继续触发新的三维主题，按现有晋升机制扩展：

1. 在 `07_validation/usage_feedback.jsonl` 记录真实任务反馈
2. 在 `07_validation/hotspot_candidates.json` 标记候选热点
3. 判断它是否直接阻塞空间表达主链
4. 若阻塞，则补：
   - 核心符号卡
   - `meta.json`
   - 任务卡关联
   - pywin32 规则
   - 项目用途说明
   - 验证要求
5. 在 `07_validation/promotion_log.md` 记录晋升动作

扩展原则保持不变：

- 先服务施工图自动化
- 先补方法组织层
- 不做无边界 3D 扩散
