# Handle Property

## 基本信息
- 来源：acad_aag, acadauto
- 类别：property
- 所属对象：Entity
- pywin32 写法：`str(getattr(ent, 'Handle', ''))`

## 作用
对象句柄，是跨步骤追踪实体和建立映射的关键标识。

## 常见用法
- 打印框追踪
- 对象二次定位
- 映射表存储

## 参数关注
- 无显式参数

## 返回
- str

## 前置条件
- 对象有效

## 常见风险
- 高频批量读取会慢

## 项目内建议路径
- `cad/system/content_analysis_dwg_file.py`
- `cad/scripts/drawing_basic_service/print/print_policy.py`

## 相关任务
- `traverse_objects_and_read_identity`
- `build_print_plan_and_info`

## 原始 CHM 命中页
- `About Event Handlers (VBA/ActiveX)` -> `01_extracted_html/acad_aag/GUID-2FF2F1B5-FFAC-420A-A741-15D1FC1A571E.htm`
- `Handle Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_handle.htm`
- `HandleToObject Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_handletoobject.htm`
- `Handle property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_handle.htm`
- `HandleToObject method [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_handletoobject.htm`
