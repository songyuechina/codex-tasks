# Section And Region Rules

本文件收口 `Region`、`SectionSolid` 及其与二维施工图表达的衔接规则，供 Codex 组织稳定的剖切与边界提取方法。

## 1. 适用范围

适用于：

- `AddRegion`
- `Region`
- `SectionSolid`
- `GetBoundingBox`
- `Coordinates / Elevation / Normal` 参与的边界还原

## 2. 主要对象 / 方法

- `ModelSpace.AddRegion(ObjectList)`
- `3DSolid.SectionSolid(Point1, Point2, Point3)`
- `entity.GetBoundingBox()`
- `entity.Explode()`

## 3. 典型参数形式

```python
region_list = model_space.AddRegion(curve_objects)
region = region_list[0]

section_region = solid.SectionSolid(
    plane_p1,
    plane_p2,
    plane_p3,
)
```

## 4. 推荐顺序

从三维关系进入二维表达，默认按下面的顺序组织：

1. 先确认三维对象真实位置与坐标基准
2. 若只有轮廓，先 `AddRegion`
3. 若已有实体，定义剖切平面三点
4. 调用 `SectionSolid`
5. 对返回的 `Region` 读取边界、面积、质心或爆炸后的环路
6. 再把这些结果回写到二维表达或打印逻辑

## 5. 常见坐标系问题

- `SectionSolid` 的三点必须是 3D WCS 点
- 剖切平面三点若共线，剖切平面无效
- 从 `Region` 提取二维边界前，必须先确认当前法向量和高程
- 包围盒读取默认给的是轴对齐范围，不等于真实剖面轮廓

## 6. 常见失败模式

- 轮廓不闭合，无法先转 `Region`
- 轮廓虽闭合但不共面，`AddRegion` 结果不稳定
- 剖切平面定义错误，`SectionSolid` 返回空或异常
- 只拿 `GetBoundingBox` 当剖切结果，导致二维表达过粗
- 忽略 `Region` 原始对象会被 AutoCAD 删除或替换的副作用

## 7. 与二维施工图表达的关联

- `SectionSolid` 直接把 3D 实体与剖切平面的交线结果转成 `Region`
- `Region` 可以作为剖面、边界、构件截面、空间分区的中间表达
- 这条链路是“由三维关系支撑二维施工图表达”的关键桥，不是单纯的 3D 建模动作

## 8. 项目内推荐使用场景

- 为剖面、立面、轮廓、构件关系表达提供稳定几何参考
- 为打印区域、布局视口、构件空间身份识别提供二维化的中间结果
- 当三维实体过复杂时，优先先做剖切或边界读取，再决定是否继续深入实体编辑

## 9. 相关任务

- `create_region_and_extrude_solid`
- `section_3d_geometry_for_2d_expression`
- `read_3d_object_spatial_identity`
