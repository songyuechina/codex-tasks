# InsertBlock Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：ModelSpace / PaperSpace / Block
- pywin32 写法：`space.InsertBlock(pt, path, sx, sy, sz, rotation)`

## 作用
把 DWG 或块定义按插入点和比例插入当前空间。

## 常见用法
- 插图签
- 插目录模板
- 跨文件插入

## 参数关注
- InsertionPoint
- Name/Path
- Xscale
- Yscale
- Zscale
- Rotation

## 返回
- BlockReference object

## 前置条件
- 点参数正确
- 路径存在
- 目标空间明确

## 常见风险
- INSBASE 偏移
- 插到错误空间
- 需要 Explode 后再处理

## 项目内建议路径
- `cad/system/CAD_core.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `insert_block_or_dwg`
- `insert_company_title_block`

## 原始 CHM 命中页
- `AddMInsertBlock Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_addminsertblock.htm`
- `InsertBlock Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_insertblock.htm`
- `AddMInsertBlock method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_addminsertblock.htm`
- `InsertBlock method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_insertblock.htm`
- `MInsertBlock object [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_minsertblock_object.htm`
