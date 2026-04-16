# Application Object

## 基本信息
- 来源：acad_aag
- 类别：object
- 所属对象：AutoCAD
- pywin32 写法：`C.acad`

## 作用
AutoCAD COM 顶层应用对象，负责文档集合、可见性和全局环境入口。

## 常见用法
- 获取 ActiveDocument
- 访问 Documents 集合
- 判断应用是否可见

## 参数关注
- 无显式参数

## 返回
- Application object

## 前置条件
- 优先通过 from system.licad import C 进入

## 常见风险
- 直接绕过 licad 建立裸连接
- 应用存在但文档尚未就绪

## 项目内建议路径
- `cad/system/licad.py`

## 相关任务
- `connect_active_document`
- `open_save_close_document`

## 原始 CHM 命中页
- `About Accessing the Application Object (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-9C66C307-9ED1-492B-9CE5-F81F73671C88.htm`
- `About Controlling the Application Window (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-BCE7E749-DCCB-4914-9E52-CC1265A3574F.htm`
- `About Creating an Instance of the Other Application (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-FD48FD40-1077-4054-8A15-CA55DADF821F.htm`
- `About Distributing Your Application (VBA)` -> `01_extracted_html/acad_aag/GUID-A2018D0D-2778-4823-A4A2-1A467A807F42.htm`
- `About Enabling Application Level Events (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-C584A219-3E90-4D1B-B382-6000F00CE9B0.htm`
