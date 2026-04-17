# Filter Rules

## 直接跳过

以下页面默认记为 `skip`：

- `*_see_also.htm`
- `idx_*`
- `all_*`
- `idh_*`，但第四轮三维空间表达白名单除外
- `IDH_*`
- 纯导航页

第四轮三维空间表达白名单包括：

- `idh_translatecoordinates`
- `idh_activeucs`
- `idh_getucsmatrix`
- `idh_ucs_object`
- `idh_normal`
- `idh_elevation`
- `idh_elevationmodelspace`
- `idh_elevationpaperspace`
- `idh_3dpoly_object`
- `idh_3dface_object`
- `idh_3dsolid_object`
- `idh_region_object`
- `idh_add3dpoly`
- `idh_add3dface`
- `idh_addregion`
- `idh_addextrudedsolid`
- `idh_addextrudedsolidalongpath`
- `idh_addrevolvedsolid`
- `idh_sectionsolid`
- `idh_rotate3d`
- `idh_mirror3d`
- `idh_scaleentity`
- `idh_transformby`

## 默认延后

以下页面默认记为 `defer`：

- `ex_*` 示例页
- 高级 3D 造型与曲面系统
- 曲面、材质、渲染、视觉样式
- 当前施工图自动化主链弱相关内容

注意：

- 与空间关系表达直接相关的三维对象页、方法页、属性页，不应继续默认压到 `defer/skip`
- 白名单内的 `idh_*` 页允许进入核心候选层
- 与坐标系、Region/Solid、剖切、三维变换直接相关的主题，应优先进入第四轮主干评估

## 默认保留

以下页面优先记为 `keep`：

- Application / Documents / Document
- ModelSpace / PaperSpace / Layout / Layouts / ActiveLayout
- SelectionSet / SelectionSets
- Block / BlockReference / AttributeReference
- GetAttributes / HasAttributes
- ObjectName / Handle / Layer / BoundingBox / Coordinates
- InsertBlock / AddLine / AddPolyline / AddText / AddMText
- GetVariable / SetVariable / Regen / SendCommand
- Plot / PlotConfiguration / RefreshPlotDeviceInfo / SetWindowToPlot
- TranslateCoordinates / ActiveUCS / GetUCSMatrix / Normal / Elevation*
- 3dPolyline / 3DFace / Region / 3DSolid
- Add3DPoly / Add3DFace / AddRegion / AddExtrudedSolid / AddExtrudedSolidAlongPath / AddRevolvedSolid / SectionSolid
- Rotate3D / Mirror3D / ScaleEntity / TransformBy

## 价值判断偏置

当前清单构建时优先偏向：

- 打印
- 布局
- 图签
- 块属性
- 目录
- 选择
- 施工图常见几何
- 与施工图空间关系表达直接相关的三维坐标、变换、轮廓、区域、实体、剖切

对这些主题的命中，会提高 `value_level` 和 `status=keep` 的概率。
