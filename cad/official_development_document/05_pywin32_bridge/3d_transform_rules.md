# 3D Transform Rules

本文件收口三维对象的移动、旋转、镜像、缩放和矩阵变换规则，供 Codex 组织稳定的空间对位方法。

## 1. 适用范围

适用于：

- `Move`
- `Rotate3D`
- `Mirror3D`
- `ScaleEntity`
- `TransformBy`

## 2. 主要对象 / 方法

- `object.Move(Point1, Point2)`
- `object.Rotate3D(Point1, Point2, RotationAngle)`
- `object.Mirror3D(Point1, Point2, Point3)`
- `object.ScaleEntity(BasePoint, ScaleFactor)`
- `object.TransformBy(TransformationMatrix)`

## 3. 典型参数形式

```python
axis_start = (x1, y1, z1)
axis_end = (x2, y2, z2)
plane_p1 = (x1, y1, z1)
plane_p2 = (x2, y2, z2)
plane_p3 = (x3, y3, z3)
base_point = (x, y, z)
angle_rad = math.radians(angle_deg)
scale_factor = 1.0
matrix_4x4 = (
    (r00, r01, r02, t0),
    (r10, r11, r12, t1),
    (r20, r21, r22, t2),
    (0.0, 0.0, 0.0, 1.0),
)
```

## 4. 推荐顺序

若只做单一变换，优先按语义选方法：

- 平移：`Move`
- 围绕轴旋转：`Rotate3D`
- 围绕平面镜像：`Mirror3D`
- 等比缩放：`ScaleEntity`

若需要把 UCS、旋转、平移合并成统一动作，优先走：

1. 先确认目标基准
2. 生成或读取 4x4 变换矩阵
3. 再调用 `TransformBy`

## 5. 常见坐标系问题

- `Rotate3D` 的轴线两点必须是 3D WCS 点
- `Mirror3D` 的三点定义的是镜像平面，不是投影方向
- `ScaleEntity` 的基点若取错，会导致对象相对关系失真
- `TransformBy` 的矩阵若不是合法 4x4，会直接报错
- 从 UCS 取来的矩阵未确认方向，就直接给对象使用

## 6. 常见失败模式

- 迭代集合时直接调用 `Mirror3D`，触发读写冲突
- 对 `AttributeReference` 强行做不适用的镜像/矩阵操作
- 角度以度传入 `Rotate3D`，而文档要求弧度
- 旋转轴退化成同一点
- 变换矩阵平移项和旋转项写错顺序

## 7. 与二维施工图表达的关联

- 施工图自动化里真正困难的往往不是能否建一个对象，而是能否把它放在正确位置和方向
- 三维对象转二维表达前，若空间对位不正确，边界、剖切、打印窗口都会错
- 使用 `TransformBy` 可以把 UCS 基准、构件方向和放置位置统一成可复用的步骤

## 8. 项目内推荐使用场景

- 对路径、轮廓、构件做空间对位时优先用 `Rotate3D / Move / ScaleEntity`
- 需要围绕平面生成对称表达时用 `Mirror3D`
- 需要把对象整体迁到某个 UCS 下时用 `GetUCSMatrix + TransformBy`

## 9. 相关任务

- `apply_3d_transform_to_objects`
- `read_3d_object_spatial_identity`
- `section_3d_geometry_for_2d_expression`
