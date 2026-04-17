# Coordinate System Rules

本文件收口与三维坐标、坐标系换算、UCS/OCS 基准相关的 `pywin32` 规则，供 Codex 快速组织稳定的空间表达方法。

## 1. 适用范围

适用于：

- 表达 3D 点
- 在 `WCS / UCS / OCS / DisplayDCS / PaperSpaceDCS` 之间转换坐标
- 读取或切换 `ActiveUCS`
- 通过 `GetUCSMatrix` 获取 UCS 变换矩阵
- 处理 `Normal / Elevation / ElevationModelSpace / ElevationPaperSpace`

## 2. 主要对象 / 方法 / 属性

- `Utility.TranslateCoordinates(OriginalPoint, From, To, Disp[, OCSNormal])`
- `Document.ActiveUCS`
- `UCS.GetUCSMatrix()`
- `Entity.Normal`
- `Polyline.Elevation`
- `Document.ElevationModelSpace`
- `Document.ElevationPaperSpace`

## 3. 典型参数形式

```python
point_wcs = (x, y, z)
normal = (nx, ny, nz)

translated = utility.TranslateCoordinates(
    point_wcs,
    from_cs,
    to_cs,
    False,        # False=point, True=displacement
    normal,       # 仅在 OCS 相关转换时传
)
```

```python
ucs = C.doc.ActiveUCS
ucs_matrix = ucs.GetUCSMatrix()
```

## 4. 推荐顺序

坐标换算默认按下面的顺序理解：

1. 先明确当前点属于哪一个坐标系
2. 若是对象的 OCS 点，先取 `Coordinates` / `Coordinate`
3. 再补 `Elevation`
4. 再取对象 `Normal`
5. 调用 `TranslateCoordinates`
6. 若要把对象整体变换到目标 UCS，再取 `ActiveUCS` 或显式 UCS
7. 用 `GetUCSMatrix()` 得到 4x4 矩阵
8. 再交给 `TransformBy`

## 5. 常见坐标系问题

- 把 OCS 点直接当 WCS 点使用
- 漏传 `OCSNormal`，导致 `TranslateCoordinates` 结果失真
- 把点和位移向量混淆，`Disp` 传错
- 忽略 `ElevationModelSpace / ElevationPaperSpace` 对 `Z` 的隐式补值
- 读取 `ActiveUCS` 时当前 UCS 未保存，直接报错

## 6. 常见失败模式

- `ActiveUCS` 读取失败：当前 UCS 未保存，`UCSNAME` 为空
- OCS 到 OCS 直接换算失败：需要先经 WCS 中转
- 以为只处理二维点，实际方法要求三元素 3D 点
- 模型空间与图纸空间的高程补值混淆

## 7. 与二维施工图表达的关联

- 打印窗口、视口、布局定位背后都依赖统一的基准坐标
- 三维对象转二维轮廓或剖切参考时，必须先确定点和法向量的真实坐标系
- 轴线、轮廓、构件定位若在错误坐标系下计算，最终二维表达会整体偏移

## 8. 项目内推荐使用场景

- 读取对象空间身份时，用 `Coordinates + Elevation + Normal` 统一还原点位
- 需要把对象对齐到特定 UCS 时，走 `ActiveUCS/GetUCSMatrix/TransformBy`
- 需要把三维关系回落到打印、布局、图签逻辑时，先统一转回稳定 WCS 表达

## 9. 相关任务

- `understand_and_convert_coordinate_systems`
- `read_3d_object_spatial_identity`
- `apply_3d_transform_to_objects`
- `section_3d_geometry_for_2d_expression`
