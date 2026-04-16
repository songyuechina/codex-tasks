# Documents Object

## 基本信息
- 来源：acad_aag, acadauto
- 类别：object
- 所属对象：Application
- pywin32 写法：`C.acad.Documents`

## 作用
文档集合，用于打开、新建、枚举 DWG 文档。

## 常见用法
- Documents.Add()
- Documents.Open()
- 检查当前文档数量

## 参数关注
- 无显式参数

## 返回
- Documents collection

## 前置条件
- 应用对象已就绪

## 常见风险
- 刚启动 CAD 时 Documents.Count 可能为 0

## 项目内建议路径
- `cad/system/licad.py`

## 相关任务
- `open_save_close_document`

## 原始 CHM 命中页
- `About Working with No Documents Open (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-83045B84-E056-4AE6-AEF5-D48AFB4F9F78.htm`
- `Documents Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_documents.htm`
- `LoadAcadLspInAllDocuments Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_loadacadlspinalldocuments.htm`
- `Documents Collection object [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_documents_collection.htm`
- `Documents property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_documents.htm`
