# Document Object

## 基本信息
- 来源：acad_aag, acadauto
- 类别：object
- 所属对象：Application
- pywin32 写法：`C.doc`

## 作用
当前 DWG 的核心文档对象，是布局、块、打印、选择、变量等操作的主入口。

## 常见用法
- ActiveLayout
- ModelSpace
- PaperSpace
- Plot
- SendCommand

## 参数关注
- 无显式参数

## 返回
- Document object

## 前置条件
- 统一通过 licad 获取

## 常见风险
- Busy 状态
- 切换布局后立即读取不稳定

## 项目内建议路径
- `cad/system/licad.py`
- `cad/system/CAD_core.py`

## 相关任务
- `connect_active_document`
- `switch_to_target_layout`
- `execute_layout_plot`

## 原始 CHM 命中页
- `About Working with No Documents Open (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-83045B84-E056-4AE6-AEF5-D48AFB4F9F78.htm`
- `Documents Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_documents.htm`
- `LoadAcadLspInAllDocuments Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_loadacadlspinalldocuments.htm`
- `About Coding Document Level Events in Environments Other Than VBA (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-45654BC7-F6B5-48E9-82FD-CED83FB956C4.htm`
- `About Coding Document Level Events in VBA (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-4F4377B1-07C8-4DDA-94D9-23DBF493C871.htm`
