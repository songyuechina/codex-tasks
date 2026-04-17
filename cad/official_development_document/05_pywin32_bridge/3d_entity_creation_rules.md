# 3D Entity Creation Rules

本文件收口三维路径、轮廓、面、区域、实体的 `pywin32` 创建顺序，供 Codex 把空间表达方法组织成稳定主链。

## 1. 适用范围

适用于：

- `Add3DPoly`
- `Add3DFace`
- `AddRegion`
- `AddExtrudedSolid`
- `AddExtrudedSolidAlongPath`
- `AddRevolvedSolid`

## 2. 主要对象 / 方法

- `ModelSpace.Add3DPoly(PointsArray)`
- `ModelSpace.Add3DFace(Point1, Point2, Point3[, Point4])`
- `ModelSpace.AddRegion(ObjectList)`
- `ModelSpace.AddExtrudedSolid(Profile, Height, TaperAngle)`
- `ModelSpace.AddExtrudedSolidAlongPath(Profile, Path)`
- `ModelSpace.AddRevolvedSolid(Profile, AxisPoint, AxisDir, Angle)`

## 3. 典型参数形式

```python
points_array = (
    x1, y1, z1,
    x2, y2, z2,
    x3, y3, z3,
)

region_inputs = [polyline_or_arc_or_circle]
solid = model_space.AddExtrudedSolid(region, height, taper_angle_rad)
solid2 = model_space.AddExtrudedSolidAlongPath(region, path_object)
```

## 4. 推荐顺序

推荐按下面的主干理解：

1. 先确定坐标基准和点位
2. 路径类对象优先用 `Add3DPoly`
3. 面类对象可用 `Add3DFace`
4. 平面闭合轮廓转 `Region`
5. 再从 `Region` 进入 `AddExtrudedSolid` / `AddExtrudedSolidAlongPath` / `AddRevolvedSolid`

不要一开始就直接从零散点位跳到复杂实体。

## 5. 常见坐标系问题

- `Add3DPoly` 的点数组必须是 3D WCS 坐标，元素数必须是 3 的倍数
- `AddRegion` 需要 closed coplanar region
- `AddExtrudedSolid` 只能挤出 2D planar region
- `AddExtrudedSolidAlongPath` 的路径不应与轮廓处于同一平面
- `AddRevolvedSolid` 要先确认旋转轴基点和方向是否在预期基准下

## 6. 常见失败模式

- 轮廓不闭合，`AddRegion` 直接失败
- 输入对象不共面，`AddRegion` 返回结果不稳定
- 轮廓自交或挤出高度/锥角过大，实体自相交失败
- 路径曲率过高，`AddExtrudedSolidAlongPath` 结果异常
- 把临时构造线直接留在主图层，污染后续二维表达

## 7. 与二维施工图表达的关联

- `3dPolyline` 适合表达空间路径、轴线或轮廓骨架
- `Region` 是从二维或共面轮廓进入剖面/面积/实体构造的重要桥
- `3DSolid` 不是为了炫技建模，而是为了得到稳定的空间体量关系、边界和剖切结果

## 8. 项目内推荐使用场景

- 先用 `create_3d_path_or_profile` 建立路径或轮廓
- 再用 `create_region_and_extrude_solid` 完成区域与实体建构
- 实体生成后，再交给变换或剖切任务，不要把所有动作混成一步

## 9. 相关任务

- `create_3d_path_or_profile`
- `create_region_and_extrude_solid`
- `section_3d_geometry_for_2d_expression`
