# Block Object

## 基本信息
- 来源：acad_aag, acadauto
- 类别：object
- 所属对象：Blocks / Layout
- pywin32 写法：`layout.Block`

## 作用
块定义或空间容器对象，是布局块、模型空间块和块定义遍历的基础。

## 常见用法
- 布局块扫描
- 块定义访问
- InsertBlock 上下文

## 参数关注
- 无显式参数

## 返回
- Block object

## 前置条件
- 明确是在块定义还是块引用语义下使用

## 常见风险
- 把块定义和块参照混淆

## 项目内建议路径
- `cad/scripts/drawing_basic_service/print/print_info_analysis.py`
- `cad/scripts/CAD_basic.py`

## 相关任务
- `read_block_attributes`
- `insert_block_or_dwg`

## 原始 CHM 命中页
- `About Layouts and Blocks (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-10F797AA-5032-4298-A2A5-C69449275F0E.htm`
- `About Using Blocks and Attributes (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-F9C39B22-6AF1-4501-9EE8-928C1B4AAA21.htm`
- `AddMInsertBlock Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_addminsertblock.htm`
- `Block Attribute Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_blockattribute.htm`
- `InsertBlock Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_insertblock.htm`
