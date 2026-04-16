# SetVariable Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：Document / Application / Utility
- pywin32 写法：`C.doc.SetVariable(name, value)`

## 作用
写系统变量，用于环境复位和命令前置准备。

## 常见用法
- 控制系统状态
- 命令前后归一

## 参数关注
- Name
- Value

## 返回
- None

## 前置条件
- 变量值合法

## 常见风险
- 影响全局状态

## 项目内建议路径
- `cad/system/CAD_core.py`

## 相关任务
- `sendcommand_fallback`

## 原始 CHM 命中页
- `SetVariable Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_setvariable.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/setvariable_see_also.htm`
- `SetVariable method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_setvariable.htm`
