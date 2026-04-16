# ObjectName Property

## 基本信息
- 来源：acadauto
- 类别：property
- 所属对象：Entity
- pywin32 写法：`getattr(ent, 'ObjectName', '')`

## 作用
读取对象类型名，是遍历实体时最稳定的首层类型判断依据。

## 常见用法
- 识别块参照、多段线、视口、天正对象

## 参数关注
- 无显式参数

## 返回
- str

## 前置条件
- 对象已获得

## 常见风险
- 天正对象还需配合兼容访问

## 项目内建议路径
- `cad/system/CAD_selection.py`
- `cad/scripts/drawing_basic_service/print/print_area_content_analysis.py`

## 相关任务
- `traverse_objects_and_read_identity`
- `read_block_attributes`

## 原始 CHM 命中页
- `ObjectName Example [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/ex_objectname.htm`
- `ObjectName property [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/idh_objectname.htm`
- `See also [ActiveX and VBA Reference: AAR]` -> `01_extracted_html/acadauto/objectname_see_also.htm`
