# Fourth Round Gap Assessment

## 1. 第三轮当前实际主链

第三轮已经把本目录从“CHM 解包结果”收束成了围绕施工图自动化主链的检索工作区，当前主链很明确：

- 连接 AutoCAD / 获取活动文档
- 打开 / 保存 / 关闭文档
- 判断模型空间 / 图纸空间 / 当前布局
- 布局枚举与切换
- 选择集构造、对象遍历、对象身份读取
- 块属性读取 / 写回
- 图签插入
- 目录生成 / 目录图签更新
- 布局打印信息读取
- 布局输出与 `SendCommand` 回退

这条主链已经落实到三个层次：

- `04_task_cards/` 以二维施工图、图签、目录、打印为主入口
- `03_core_symbols/` 以 `Application / Document / Layout / SelectionSet / BlockReference / Plot` 等对象为核心骨架
- `05_pywin32_bridge/` 重点覆盖集合遍历、点数组、Variant、打印布局、`SendCommand`

结论：第三轮主链是“二维施工图自动化 + 打印链 + 图签目录链”，不是通用 AutoCAD 开发百科。

## 2. 第三轮当前如何处理三维内容

第三轮没有完全排斥 3D，但处理方式明显是“局部保留、整体压低”：

- `03_core_symbols/types_and_variants/3d_point.md` 已进入主干，但定位仍是二维主链的参数类型辅助件
- `determine_space_and_layout` 已把 `ElevationModelSpace / ElevationPaperSpace` 作为来源页纳入追踪，但没有提升为单独核心卡
- `get_bounding_box_and_object_counts`、`Coordinates` 等卡片与属性能间接服务空间表达，但没有形成“三维空间表达”任务组
- `tools/search_cad_help.py` 能搜到 `TranslateCoordinates`、`Rotate3D`、`SectionSolid`、`TransformBy` 等原始页面，但多数结果仍来自 `06_on_demand_index/` 或原始 HTML
- `README.md`、`README_Codex_Workflow.md`、`README_Task_Priority.md`、`README_Filter_Rules.md` 仍把 3D 默认视为非主入口或次级主题

结论：第三轮对 3D 的态度是“只保留最基础的 3D 点和零散坐标线索，不让 3D 进入主干组织层”。

## 3. 已存在于 `02_manifest` 但仍停留在 `defer/skip` 的三维主题

### 3.1 与空间表达高度相关、但仍被压低的主题

这些主题已经在 `02_manifest/page_manifest.jsonl`、`02_manifest/value_ranking.jsonl` 或 `06_on_demand_index/uncommon_topics.jsonl` 中存在，但当前状态仍是 `defer` 或 `skip`：

- 坐标与坐标系
  - `acad_aag:GUID_06B18EED_D4E3_4B81_ACB8_037E884CB93D` `About Converting Coordinates`
  - `acad_aag:GUID_6954AAF3_7107_4D93_A2CE_FE859F3F9902` `About Specifying 3D Coordinates`
  - `acadauto:idh_translatecoordinates` `TranslateCoordinates method`
  - `acadauto:idh_activeucs` `ActiveUCS property`
  - `acadauto:idh_getucsmatrix` `GetUCSMatrix method`
  - `acadauto:idh_ucs_object` `UCS object`
  - `acadauto:idh_normal` `Normal property`
  - `acadauto:idh_elevation` `Elevation property`
  - `acadauto:idh_elevationmodelspace` `ElevationModelSpace property`
  - `acadauto:idh_elevationpaperspace` `ElevationPaperSpace property`

- 三维对象与轮廓/区域/实体
  - `acadauto:idh_3dpoly_object` `3dPolyline object`
  - `acadauto:idh_3dface_object` `3DFace object`
  - `acadauto:idh_3dsolid_object` `3DSolid object`
  - `acadauto:idh_region_object` `Region object`
  - `acadauto:idh_add3dpoly` `Add3DPoly method`
  - `acadauto:idh_add3dface` `Add3DFace method`
  - `acadauto:idh_addregion` `AddRegion method`
  - `acadauto:idh_addextrudedsolid` `AddExtrudedSolid method`
  - `acadauto:idh_addextrudedsolidalongpath` `AddExtrudedSolidAlongPath method`
  - `acadauto:idh_addrevolvedsolid` `AddRevolvedSolid method`
  - `acadauto:idh_sectionsolid` `SectionSolid method`

- 三维变换
  - `acadauto:idh_rotate3d` `Rotate3D method`
  - `acadauto:idh_mirror3d` `Mirror3D method`
  - `acadauto:idh_scaleentity` `ScaleEntity method`
  - `acadauto:idh_transformby` `TransformBy method`
  - `acad_aag:GUID_19A5491D_7675_4ECF_A66A_5D309A14429F` `About Transforming Objects`
  - `acad_aag:GUID_3FEB0A3C_E4B1_40DF_A4DF_CAB22F1E2A92` `About Rotating in 3D`

### 3.2 当前问题

这些主题不是“不存在”，而是被第三轮筛选规则整体压在了低频层：

- `idh_*` 页面被机械当成辅助页
- 大多数对象/方法只留在 `06_on_demand_index/uncommon_topics.jsonl`
- 没有专门任务卡把它们组织成可执行方法
- 没有专门 pywin32 规则把坐标系、矩阵、剖切、Region/Solid 顺序写清楚

## 4. 哪些三维主题应在第四轮提升为重点

第四轮应提升的不是“全部 3D”，而是与施工图空间关系表达直接相关的三类能力。

### 4.1 坐标与坐标系主干

应提升：

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

理由：

- `TranslateCoordinates` 已明确要求 `OriginalPoint` 是三元素 3D 点，并要求在 OCS 转换时传入 `OCSNormal`
- `Normal` 页明确说明它定义对象 OCS 的 Z 轴，并直接作为 `TranslateCoordinates` 的 `OCSNormal`
- `ElevationModelSpace / ElevationPaperSpace` 明确说明当只给 `X/Y` 时，当前高程会补成 3D 点的 `Z`
- `ActiveUCS + GetUCSMatrix + TransformBy` 已形成从 UCS 获取矩阵、再把对象变换到对应坐标基准的完整链路

这组主题必须进入主干，因为它们是“空间关系表达”而不是“炫技建模”。

### 4.2 三维路径、轮廓、区域、实体、剖切主干

应提升：

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

- `Add3DPoly` 是空间路径和三维轮廓的直接入口
- `AddRegion` 要求输入对象必须构成 closed coplanar region，是从轮廓进入区域/剖面表达的关键桥
- `AddExtrudedSolid`、`AddExtrudedSolidAlongPath`、`AddRevolvedSolid` 提供从二维轮廓或路径进入三维构件表达的受控入口
- `SectionSolid` 直接返回 `Region`，可以把三维实体的剖切结果导回二维表达逻辑

这组主题服务的是轮廓、剖切、构件空间关系，不是泛化的 3D 展示。

### 4.3 三维变换与空间对位主干

应提升：

- `Move`
- `Rotate3D`
- `Mirror3D`
- `ScaleEntity`
- `TransformBy`
- `transform_matrix`
- `section_plane_definition`

理由：

- `Rotate3D` 要求用两点定义 3D 旋转轴
- `Mirror3D` 要求用三点定义镜像平面
- `ScaleEntity` 和 `Move` 共同服务对象空间定位
- `TransformBy` 能以 4x4 矩阵统一表达移动、旋转、缩放和坐标基准变换

第四轮如果不把这层补齐，三维对象即使进主干，也仍然无法稳定服务施工图空间表达。

## 5. 哪些三维主题仍应保持低频层

以下内容不应在第四轮进入主干：

- 材质
- 光照
- 渲染
- 视觉样式
- `Surface / LoftedSurface / SweptSurface` 一类以展示或高级造型为主的体系
- 纯展示型高级曲面
- 与施工图自动化主链弱相关的 3D 浏览、相机、阴影、视觉效果
- 仅为造型复杂度服务、但不能直接落到施工图表达的高级实体编辑

这些内容继续留在 `06_on_demand_index/` 是合理的。

## 6. 第四轮最关键的结构性缺口

当前最大的缺口不是“缺页面”，而是缺主干组织：

1. 缺范围说明
   - 当前 README 仍在延续“默认压低 3D”的第三轮表述。

2. 缺任务入口
   - 还没有 `10_3d_spatial_expression/` 分组。

3. 缺规则层
   - 没有坐标系、三维变换、Region/Solid、剖切的独立 pywin32 规则文件。

4. 缺核心卡
   - 只有 `3d_point` 进入了类型层，真正的对象 / 方法 / 属性几乎都没有进入 `03_core_symbols/`。

5. 缺构建白名单
   - 当前 `build_core_symbols.py` 仍只有第三轮二维静态种子。
   - 当前 `build_task_cards.py` 也完全没有三维任务分组。
   - 当前筛选逻辑仍把本轮关键 `idh_*` 页机械压为 `skip`。

6. 缺验证问题
   - `validation_tasks.md` 和 `validation_cases.json` 还没有把坐标系转换、Region/Solid、SectionSolid、3D 变换纳入验收。

## 7. 第四轮调整方向

第四轮应保持原有二维施工图、打印、图签、目录主链不动，同时增加一条新的正式重点分支：

- `二维施工图主链`
- `打印 / 图签 / 目录主链`
- `服务施工图空间关系表达的三维能力主链`

不应改成：

- “全面 3D 化”
- “AutoCAD 3D 百科”
- “把所有 `idh_*` 页都升格”

第四轮的成功标准是：

- Codex 接到空间关系、剖切、轮廓、三维对位相关任务时，先命中任务卡和规则层
- 不必先回退到大量原始 HTML
- 仍然清楚知道 3D 只是在服务施工图自动化，而不是扩散成无边界的主题库
