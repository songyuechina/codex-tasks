# SendCommand Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：Document
- pywin32 写法：`C.doc.SendCommand(command + '\n')`

## 作用
向 CAD 命令行发送命令串，是 COM 直调不稳时的保底路径。

## 常见用法
- 布局切换兜底
- 选择/缩放兜底
- 打印命令回退

## 参数关注
- Command string

## 返回
- 通常无直接结果

## 前置条件
- 命令串完整且上下文正确

## 常见风险
- 异步、时序、命令态冲突

## 项目内建议路径
- `cad/system/licad.py`
- `cad/system/CAD_coordination.py`
- `cad/scripts/drawing_basic_service/print/print_executor.py`

## 相关任务
- `sendcommand_fallback`
- `switch_to_target_layout`
- `execute_layout_plot`

## 原始 CHM 命中页
- `SendCommand Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_sendcommand.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/sendcommand_see_also.htm`
- `SendCommand method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_sendcommand.htm`
