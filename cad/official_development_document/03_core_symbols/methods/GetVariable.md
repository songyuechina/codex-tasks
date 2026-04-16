# GetVariable Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：Document / Application / Utility
- pywin32 写法：`C.doc.GetVariable(name)`

## 作用
读取系统变量，用于命令回退和环境判断。

## 常见用法
- 读 CTAB
- 读 TILEMODE
- 读打印相关状态

## 参数关注
- Name

## 返回
- Variant value

## 前置条件
- 变量名正确

## 常见风险
- 返回值类型不固定

## 项目内建议路径
- `cad/system/CAD_core.py`

## 相关任务
- `sendcommand_fallback`
- `determine_space_and_layout`

## 原始 CHM 命中页
- `GetVariable Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_getvariable.htm`
- `GetVariable method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_getvariable.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/getvariable_see_also.htm`
