Python 3.11.5 (tags/v3.11.5:cce6ba9, Aug 24 2023, 14:38:34) [MSC v.1936 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.

============================================================Script Navigator 监听服务已就绪 (127.0.0.1:65432)

          CAD Automation Scripts - IDLE Shell
============================================================
  状态: 就绪
  功能: 支持 BOM 格式文件，支持相对路径资源加载
============================================================

>>> 

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> Redefine_standard_blocks(source_file=None, target_file=None)
⏱ 开始 `Redefine_standard_blocks` …
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
[初始化] 脚本环境加载完成: CAD_file_operations.py
当前工作基准路径: D:\Mypro\基础服务\用户1
正在处理文件: D:\Mypro\基础服务\用户1\dwg文件\标准图签.dwg
版本v1.0
[li] 连接已刷新: Drawing2.dwg
[复制] 正在搬运 265 个对象 (保留块结构)...
[成功] 搬运完成
[保存] 目标文件已保存
[状态] 文件未修改，无需保存: 标准图签.dwg
2025-12-23 21:17:28,777 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。
[OK] 第 1 次尝试：选到图层 ['tuqian_neibu_pl'] 上 8 个对象
[OK] 第 1 次尝试：选到图层 ['TWT_TITLE'] 上 2 个对象
2025-12-23 21:17:29,545 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。
[li] 连接已刷新: 标准图签.dwg
[OK] 已高亮选择区域 (0,0) ~ (0,0) 的对象
[OK] 第1次尝试：cancel_cad_selection 成功
2025-12-23 21:17:36,545 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。

--- [DEBUG模式 V2] 正在执行严格版重定义 (ty=0.5) ---
[现状] 块定义 'A3-H' (Handle:4DDE) 当前对象数: 14
[审计] 准备注入 76 个对象。
[握手] Python发送: 76 | LISP接收: 76
[执行] 发送 -BLOCK 覆盖指令...
[结果] 块定义 'A3-H' 旧数:14 -> 新数:76 (变化:62)
✅ [成功确认] 块定义已更新。
2025-12-23 21:17:37,777 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。
[错误] 无法获取块名，跳过同步。
成功重定义: A3-H
2025-12-23 21:17:38,316 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。
[OK] 已高亮选择区域 (0,0) ~ (0,0) 的对象
[OK] 第1次尝试：cancel_cad_selection 成功
2025-12-23 21:17:45,272 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。

--- [DEBUG模式 V2] 正在执行严格版重定义 (ty=0.5) ---
[现状] 块定义 'A2-H' (Handle:4DF2) 当前对象数: 14
[审计] 准备注入 68 个对象。
[握手] Python发送: 68 | LISP接收: 68
[执行] 发送 -BLOCK 覆盖指令...
[结果] 块定义 'A2-H' 旧数:14 -> 新数:68 (变化:54)
✅ [成功确认] 块定义已更新。
2025-12-23 21:17:46,454 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.50s。CAD 全程空闲。
[错误] 无法获取块名，跳过同步。
成功重定义: A2-H
2025-12-23 21:17:46,984 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。
[OK] 已高亮选择区域 (0,0) ~ (0,0) 的对象
[OK] 第1次尝试：cancel_cad_selection 成功
2025-12-23 21:17:53,858 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。

--- [DEBUG模式 V2] 正在执行严格版重定义 (ty=0.5) ---
[现状] 块定义 'A1-H' (Handle:4E07) 当前对象数: 15
[审计] 准备注入 59 个对象。
[握手] Python发送: 59 | LISP接收: 59
[执行] 发送 -BLOCK 覆盖指令...
[结果] 块定义 'A1-H' 旧数:15 -> 新数:59 (变化:44)
✅ [成功确认] 块定义已更新。
2025-12-23 21:17:54,992 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。
[错误] 无法获取块名，跳过同步。
成功重定义: A1-H
2025-12-23 21:17:55,521 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。
[OK] 已高亮选择区域 (0,0) ~ (0,0) 的对象
[OK] 第1次尝试：cancel_cad_selection 成功
2025-12-23 21:18:02,368 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。

--- [DEBUG模式 V2] 正在执行严格版重定义 (ty=0.5) ---
[现状] 块定义 'A0-H' (Handle:4E1C) 当前对象数: 15
[审计] 准备注入 54 个对象。
[握手] Python发送: 54 | LISP接收: 54
[执行] 发送 -BLOCK 覆盖指令...
[结果] 块定义 'A0-H' 旧数:15 -> 新数:54 (变化:39)
✅ [成功确认] 块定义已更新。
2025-12-23 21:18:03,497 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。
[错误] 无法获取块名，跳过同步。
成功重定义: A0-H
2025-12-23 21:18:04,027 - [wait_command_done] - WARNING - [Redefine_standard_blocks] 冗余等待！耗时 0.51s。CAD 全程空闲。
[保存] 正在保存: 标准图签.dwg ...
[成功] 保存完成: 标准图签.dwg
[处理] 正在通过 API 关闭文件: 标准图签.dwg
[状态] 丢弃修改并关闭: 标准图签.dwg
文件已保存并关闭。
⏱ 完成 `Redefine_standard_blocks`，耗时：44.250 秒
attsync_block_instance(target_blocks[0])
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    attsync_block_instance(target_blocks[0])
NameError: name 'target_blocks' is not defined
pm=pmxz()
[li] 连接已刷新: 标准图签.dwg
确认版本v1.0
attsync_block_instance(pm[0])
🔄 [同步] 正在刷新图块实例: A2-H ...
True
pm=pmxz()
确认版本v1.0
attsync_block_instance(pm[0])
🔄 [同步] 正在刷新图块实例: A1-H ...
True
pm=pmxz()
确认版本v1.0
attsync_block_instance(pm[0])
🔄 [同步] 正在刷新图块实例: A0-H ...
True
pm=pmxz()
[li] 连接已刷新: 霞飞云果园【供水平面图-125.dwg
确认版本v1.0
pm=pmxz()
确认版本v1.0
get_attr(pm[0], "图名文字")
'图名1'
set_attr(pm[0], "图名文字","未命名1")
True
lb=stc("")
[OK] 第 1 次尝试：选到图层 [''] 上 0 个对象
pm=pmxz()
确认版本v1.0
pm.Layer
Traceback (most recent call last):
  File "<pyshell#14>", line 1, in <module>
    pm.Layer
AttributeError: 'list' object has no attribute 'Layer'
pm[0].Layer
'DIM_SYMB'
lb=stc("DIM_SYMB")
[OK] 第 1 次尝试：选到图层 ['DIM_SYMB'] 上 60 个对象
[set_attr(obj, "图名文字", f"未命名{i}") for i, obj in enumerate(lb)]
[True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
sdy=elect_print_areas_maxrect_from_polylines()
Traceback (most recent call last):
  File "<pyshell#18>", line 1, in <module>
    sdy=elect_print_areas_maxrect_from_polylines()
NameError: name 'elect_print_areas_maxrect_from_polylines' is not defined
sdy=select_print_areas_maxrect_from_polylines()
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
🟢 已新建图层：dy_zhuanyong
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 0 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.766s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.018s，共 0 条
📌 最终锁定打印区域: 0 个
🎨 重绘完成，数量: 0。正在执行空间排序...
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：1.524 秒
select_print_areas_maxrect_from_polylines(
    lm = 70,
    tol_single = 0.01,
    layer_name: = "dy_zhuanyong",
    width = 0.0,
    color = 1,
    z = 0.0,
    duanbian = 70,
    debug = False,
    print_rejection_reason = False,
    cha_Y = 5, 
)
SyntaxError: positional argument follows keyword argument
dy=select_print_areas_maxrect_from_polylines(
    lm = 70,
    tol_single = 0.01,
    layer_name = "dy_zhuanyong",
    width = 0.0,
    color = 1,
    z = 0.0,
    duanbian = 70,
    debug = False,
    print_rejection_reason = False,
    cha_Y = 5, 
)
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 0 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.764s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.021s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：2.182 秒

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> 
============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> get_sorted_titles_by_areas(layer_name="DIM_SYMB")
Traceback (most recent call last):
  File "<pyshell#22>", line 1, in <module>
    get_sorted_titles_by_areas(layer_name="DIM_SYMB")
  File "D:/claude-tasks/cad/scripts/CAD_basic.py", line 16598, in get_sorted_titles_by_areas
    print(f"开始处理 {len(print_areas_polylines)} 个打印区域...")
NameError: name 'print_areas_polylines' is not defined

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.755s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.016s，共 0 条
📌 最终锁定打印区域: 0 个
🎨 重绘完成，数量: 0。正在执行空间排序...
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：3.631 秒
开始处理 0 个打印区域...
未找到任何图名对象。
[]
get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 0 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.761s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.014s，共 0 条
📌 最终锁定打印区域: 0 个
🎨 重绘完成，数量: 0。正在执行空间排序...
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：1.413 秒
开始处理 0 个打印区域...
未找到任何图名对象。
[]
sdy = select_print_areas_maxrect_from_polylines()
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 0 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.751s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.018s，共 0 条
📌 最终锁定打印区域: 0 个
🎨 重绘完成，数量: 0。正在执行空间排序...
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：1.415 秒

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> fh=get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 0 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.760s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.015s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：2.121 秒
开始处理 37 个打印区域...
已处理并重命名 15 个图名。

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.752s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.015s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.416 秒
开始处理 37 个打印区域...
已处理并重命名 434 个图名。

len(stc("DIM_SYMB"))
[OK] 第 1 次尝试：选到图层 ['DIM_SYMB'] 上 60 个对象
60

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> 
============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.756s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.017s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.422 秒
开始处理 37 个打印区域...
Traceback (most recent call last):
  File "<pyshell#29>", line 1, in <module>
    get_sorted_titles_by_areas(layer_name="DIM_SYMB")
  File "D:/claude-tasks/cad/scripts/CAD_basic.py", line 16620, in get_sorted_titles_by_areas
    sorted_sublist = sort_coms_by_llcorner(found_titles, cha_Y=cha_Y)
NameError: name 'cha_Y' is not defined

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> 
============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.750s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.017s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.049 秒
开始处理 37 个打印区域...
处理完成：共发现 51 个唯一图名 (已去重)。

sdy = select_print_areas_maxrect_from_polylines(
        lm=70, tol_single=0.01, layer_name="dy_zhuanyong",
        width=0.0, color=1, z=0.0, duanbian=70,
        debug=False, print_rejection_reason=False, cha_Y=5, 
    )
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 39 个对象
  第 1 次删除：共删除 39 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.746s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.015s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.498 秒
sdy[3].Delete()
Traceback (most recent call last):
  File "<pyshell#32>", line 1, in <module>
    sdy[3].Delete()
IndexError: tuple index out of range
sdy[0][3].Delete()
sdy[0][4].Delete()

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> 
============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 35 个对象
  第 1 次删除：共删除 35 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.758s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.015s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.320 秒
开始严格处理 37 个打印区域 (按顺序分组)...
区域 0 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 1 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 2 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 3 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 4 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 5 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 6 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 7 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 8 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 9 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 10 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 11 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 12 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 13 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 14 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 15 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 16 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 17 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 18 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 19 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 20 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 21 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 22 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 23 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 24 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 25 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 26 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 27 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 28 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 29 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 30 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 31 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 32 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 33 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 34 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 35 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 36 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
未找到任何图名对象。
[]

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.744s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.015s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.380 秒
开始严格处理 37 个打印区域 (按顺序分组)...
区域 0 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 1 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 2 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 3 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 4 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 5 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 6 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 7 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 8 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 9 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 10 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 11 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 12 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 13 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 14 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 15 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 16 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 17 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 18 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 19 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 20 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 21 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 22 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 23 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 24 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 25 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 26 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 27 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 28 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 29 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 30 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 31 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 32 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 33 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 34 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 35 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
区域 36 坐标处理失败: (-2147352567, '发生意外。', (0, '天正软件', '参数 LowerLeft (位于 ZoomWindow 中) 无效', 'C:\\Program Files\\Autodesk\\AutoCAD 2021\\HELP\\OLE_ERR.CHM', -2145320939, -2147024809), None)
未找到任何图名对象。
[]

============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.761s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.014s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.469 秒
开始按顺序处理 37 个打印区域...
处理完成：共排序并命名 51 个图名。


============================================================
>>> 正在运行脚本: CAD_basic.py
============================================================
[成功] CAD协同机制模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
✔ 脚本执行完成。
============================================================

>>> get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.746s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.014s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.208 秒

====== 开始处理 37 个打印区域 ======

--- 正在分析第 0 张图 (Index: 0) ---
  [选择] 窗口框选命中: 12 个对象
    [新增] 未命名1 (原内容: 'None') -> 归属图框 0
    [新增] 未命名2 (原内容: 'None') -> 归属图框 0
    [新增] 未命名3 (原内容: 'None') -> 归属图框 0
    [新增] 未命名4 (原内容: 'None') -> 归属图框 0
    [新增] 未命名5 (原内容: 'None') -> 归属图框 0
    [新增] 未命名6 (原内容: 'None') -> 归属图框 0
    [新增] 未命名7 (原内容: 'None') -> 归属图框 0
    [新增] 未命名8 (原内容: 'None') -> 归属图框 0
    [新增] 未命名9 (原内容: 'None') -> 归属图框 0
    [新增] 未命名10 (原内容: 'None') -> 归属图框 0
    [新增] 未命名11 (原内容: 'None') -> 归属图框 0
    [新增] 未命名12 (原内容: 'None') -> 归属图框 0
  [结果] 第 0 张图实际新增编号: 12 个

--- 正在分析第 1 张图 (Index: 1) ---
  [选择] 窗口框选命中: 16 个对象
    [警告!] 对象 'None' (Handle: 4F43) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名13 (原内容: 'None') -> 归属图框 1
    [警告!] 对象 'None' (Handle: 4F45) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F50) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F51) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F52) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F53) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名14 (原内容: 'None') -> 归属图框 1
    [警告!] 对象 'None' (Handle: 4F47) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F48) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F54) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F55) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F56) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F57) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名15 (原内容: 'None') -> 归属图框 1
    [新增] 未命名16 (原内容: 'None') -> 归属图框 1
  [结果] 第 1 张图实际新增编号: 4 个

--- 正在分析第 2 张图 (Index: 2) ---
  [选择] 窗口框选命中: 20 个对象
    [警告!] 对象 'None' (Handle: 4F43) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4D) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名17 (原内容: 'None') -> 归属图框 2
    [警告!] 对象 'None' (Handle: 4F45) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F50) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F51) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F52) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F53) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4E) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名18 (原内容: 'None') -> 归属图框 2
    [警告!] 对象 'None' (Handle: 4F47) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F48) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F54) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F55) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F56) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F57) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F58) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F59) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名19 (原内容: 'None') -> 归属图框 2
    [新增] 未命名20 (原内容: 'None') -> 归属图框 2
  [结果] 第 2 张图实际新增编号: 4 个

--- 正在分析第 3 张图 (Index: 3) ---
  [选择] 窗口框选命中: 20 个对象
    [警告!] 对象 'None' (Handle: 4F4D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F50) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F51) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F52) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F53) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7E) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名21 (原内容: 'None') -> 归属图框 3
    [新增] 未命名22 (原内容: 'None') -> 归属图框 3
    [警告!] 对象 'None' (Handle: 4F54) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F55) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F56) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F57) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F58) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F59) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5B) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名23 (原内容: 'None') -> 归属图框 3
    [新增] 未命名24 (原内容: 'None') -> 归属图框 3
  [结果] 第 3 张图实际新增编号: 4 个

--- 正在分析第 4 张图 (Index: 4) ---
  [选择] 窗口框选命中: 20 个对象
    [警告!] 对象 'None' (Handle: 4F4D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F52) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F53) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5D) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名25 (原内容: 'None') -> 归属图框 4
    [新增] 未命名26 (原内容: 'None') -> 归属图框 4
    [警告!] 对象 'None' (Handle: 4F56) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F57) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F58) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F59) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7C) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名27 (原内容: 'None') -> 归属图框 4
    [新增] 未命名28 (原内容: 'None') -> 归属图框 4
  [结果] 第 4 张图实际新增编号: 4 个

--- 正在分析第 5 张图 (Index: 5) ---
  [选择] 窗口框选命中: 18 个对象
    [警告!] 对象 'None' (Handle: 4F7D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5F) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名29 (原内容: 'None') -> 归属图框 5
    [新增] 未命名30 (原内容: 'None') -> 归属图框 5
    [警告!] 对象 'None' (Handle: 4F58) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F59) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F62) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F63) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名31 (原内容: 'None') -> 归属图框 5
    [新增] 未命名32 (原内容: 'None') -> 归属图框 5
  [结果] 第 5 张图实际新增编号: 4 个

--- 正在分析第 6 张图 (Index: 6) ---
  [选择] 窗口框选命中: 17 个对象
    [警告!] 对象 'None' (Handle: 4F7D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5F) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F60) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F61) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F62) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F63) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F64) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F65) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名33 (原内容: 'None') -> 归属图框 6
    [新增] 未命名34 (原内容: 'None') -> 归属图框 6
  [结果] 第 6 张图实际新增编号: 2 个

--- 正在分析第 7 张图 (Index: 7) ---
  [选择] 窗口框选命中: 18 个对象
    [警告!] 对象 'None' (Handle: 4F5C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5F) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F60) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F61) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名35 (原内容: 'None') -> 归属图框 7
    [新增] 未命名36 (原内容: 'None') -> 归属图框 7
    [警告!] 对象 'None' (Handle: 4F7B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F62) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F63) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F64) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F65) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F66) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F67) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名37 (原内容: 'None') -> 归属图框 7
    [新增] 未命名38 (原内容: 'None') -> 归属图框 7
  [结果] 第 7 张图实际新增编号: 4 个

--- 正在分析第 8 张图 (Index: 8) ---
  [选择] 窗口框选命中: 17 个对象
    [警告!] 对象 'None' (Handle: 4F5E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5F) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F60) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F61) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6D) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名39 (原内容: 'None') -> 归属图框 8
    [警告!] 对象 'None' (Handle: 4F62) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F63) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F64) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F65) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F66) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F67) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F78) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F79) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名40 (原内容: 'None') -> 归属图框 8
    [新增] 未命名41 (原内容: 'None') -> 归属图框 8
  [结果] 第 8 张图实际新增编号: 3 个

--- 正在分析第 9 张图 (Index: 9) ---
  [选择] 窗口框选命中: 16 个对象
    [警告!] 对象 'None' (Handle: 4F60) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F61) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6E) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名42 (原内容: 'None') -> 归属图框 9
    [警告!] 对象 'None' (Handle: 4F64) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F65) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F66) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F67) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F78) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F79) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F68) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F69) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名43 (原内容: 'None') -> 归属图框 9
    [新增] 未命名44 (原内容: 'None') -> 归属图框 9
  [结果] 第 9 张图实际新增编号: 3 个

--- 正在分析第 10 张图 (Index: 10) ---
  [选择] 窗口框选命中: 13 个对象
    [警告!] 对象 'None' (Handle: 4F6C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F76) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名45 (原内容: 'None') -> 归属图框 10
    [警告!] 对象 'None' (Handle: 4F66) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F67) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F78) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F79) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F68) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F69) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6B) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 10 张图实际新增编号: 1 个

--- 正在分析第 11 张图 (Index: 11) ---
  [选择] 窗口框选命中: 13 个对象
    [警告!] 对象 'None' (Handle: 4F6C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F76) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F77) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名46 (原内容: 'None') -> 归属图框 11
    [新增] 未命名47 (原内容: 'None') -> 归属图框 11
    [警告!] 对象 'None' (Handle: 4F78) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F79) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F68) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F69) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6B) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 11 张图实际新增编号: 2 个

--- 正在分析第 12 张图 (Index: 12) ---
  [选择] 窗口框选命中: 11 个对象
    [警告!] 对象 'None' (Handle: 4F6E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F76) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F77) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F70) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F71) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名48 (原内容: 'None') -> 归属图框 12
    [新增] 未命名49 (原内容: 'None') -> 归属图框 12
    [警告!] 对象 'None' (Handle: 4F68) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F69) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6B) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 12 张图实际新增编号: 2 个

--- 正在分析第 13 张图 (Index: 13) ---
  [选择] 窗口框选命中: 10 个对象
    [警告!] 对象 'None' (Handle: 4F76) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F77) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F70) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F71) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F72) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F73) 在此处被选中，但已被之前的图框抢先处理！
    [新增] 未命名50 (原内容: 'None') -> 归属图框 13
    [新增] 未命名51 (原内容: 'None') -> 归属图框 13
    [警告!] 对象 'None' (Handle: 4F6A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6B) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 13 张图实际新增编号: 2 个

--- 正在分析第 14 张图 (Index: 14) ---
  [选择] 窗口框选命中: 7 个对象
    [警告!] 对象 'None' (Handle: 4F77) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F70) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F71) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F72) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F73) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F74) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F75) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 14 张图实际新增编号: 0 个

--- 正在分析第 15 张图 (Index: 15) ---
  [选择] 窗口框选命中: 6 个对象
    [警告!] 对象 'None' (Handle: 4F70) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F71) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F72) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F73) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F74) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F75) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 15 张图实际新增编号: 0 个

--- 正在分析第 16 张图 (Index: 16) ---
  [选择] 窗口框选命中: 12 个对象
    [警告!] 对象 'None' (Handle: 4F43) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F45) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F50) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F51) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F52) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F53) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F47) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F48) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F54) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F55) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F56) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F57) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 16 张图实际新增编号: 0 个

--- 正在分析第 17 张图 (Index: 17) ---
  [选择] 窗口框选命中: 16 个对象
    [警告!] 对象 'None' (Handle: 4F43) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F45) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F50) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F51) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F52) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F53) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F47) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F48) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F54) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F55) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F56) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F57) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F58) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F59) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 17 张图实际新增编号: 0 个

--- 正在分析第 18 张图 (Index: 18) ---
  [选择] 窗口框选命中: 20 个对象
    [警告!] 对象 'None' (Handle: 4F43) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F45) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F50) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F51) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F52) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F53) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F47) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F48) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F54) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F55) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F56) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F57) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F58) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F59) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5B) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 18 张图实际新增编号: 0 个

--- 正在分析第 19 张图 (Index: 19) ---
  [选择] 窗口框选命中: 20 个对象
    [警告!] 对象 'None' (Handle: 4F4D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F50) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F51) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F52) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F53) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F54) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F55) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F56) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F57) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F58) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F59) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7C) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 19 张图实际新增编号: 0 个

--- 正在分析第 20 张图 (Index: 20) ---
  [选择] 窗口框选命中: 20 个对象
    [警告!] 对象 'None' (Handle: 4F4D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F52) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F53) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F4E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5F) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F56) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F57) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F58) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F59) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F62) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F63) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 20 张图实际新增编号: 0 个

--- 正在分析第 21 张图 (Index: 21) ---
  [选择] 窗口框选命中: 18 个对象
    [警告!] 对象 'None' (Handle: 4F7D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5F) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F60) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F61) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F58) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F59) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F62) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F63) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F64) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F65) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 21 张图实际新增编号: 0 个

--- 正在分析第 22 张图 (Index: 22) ---
  [选择] 窗口框选命中: 17 个对象
    [警告!] 对象 'None' (Handle: 4F7D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5F) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F60) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F61) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F62) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F63) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F64) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F65) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F66) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F67) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 22 张图实际新增编号: 0 个

--- 正在分析第 23 张图 (Index: 23) ---
  [选择] 窗口框选命中: 18 个对象
    [警告!] 对象 'None' (Handle: 4F5C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5F) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F60) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F61) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7B) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F7C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F62) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F63) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F64) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F65) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F66) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F67) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F78) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F79) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 23 张图实际新增编号: 0 个

--- 正在分析第 24 张图 (Index: 24) ---
  [选择] 窗口框选命中: 17 个对象
    [警告!] 对象 'None' (Handle: 4F5E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F5F) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F60) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F61) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F62) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F63) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F64) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F65) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F66) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F67) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F78) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F79) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F68) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F69) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 24 张图实际新增编号: 0 个

--- 正在分析第 25 张图 (Index: 25) ---
  [选择] 窗口框选命中: 16 个对象
    [警告!] 对象 'None' (Handle: 4F60) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F61) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F76) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F64) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F65) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F66) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F67) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F78) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F79) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F68) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F69) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6B) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 25 张图实际新增编号: 0 个

--- 正在分析第 26 张图 (Index: 26) ---
  [选择] 窗口框选命中: 13 个对象
    [警告!] 对象 'None' (Handle: 4F6C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F76) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F77) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F66) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F67) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F78) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F79) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F68) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F69) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6B) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 26 张图实际新增编号: 0 个

--- 正在分析第 27 张图 (Index: 27) ---
  [选择] 窗口框选命中: 13 个对象
    [警告!] 对象 'None' (Handle: 4F6C) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6D) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6E) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F76) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F77) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F70) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F71) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F78) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F79) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F68) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F69) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6A) 在此处被选中，但已被之前的图框抢先处理！
    [警告!] 对象 'None' (Handle: 4F6B) 在此处被选中，但已被之前的图框抢先处理！
  [结果] 第 27 张图实际新增编号: 0 个

--- 正在分析第 28 张图 (Index: 28) ---
  [选择] 窗口框选命中: 0 个对象
  [结果] 第 28 张图为空

--- 正在分析第 29 张图 (Index: 29) ---
  [选择] 窗口框选命中: 0 个对象
  [结果] 第 29 张图为空

--- 正在分析第 30 张图 (Index: 30) ---
  [选择] 窗口框选命中: 0 个对象
  [结果] 第 30 张图为空

--- 正在分析第 31 张图 (Index: 31) ---
  [选择] 窗口框选命中: 0 个对象
  [结果] 第 31 张图为空

--- 正在分析第 32 张图 (Index: 32) ---
  [选择] 窗口框选命中: 0 个对象
  [结果] 第 32 张图为空

--- 正在分析第 33 张图 (Index: 33) ---
  [选择] 窗口框选命中: 0 个对象
  [结果] 第 33 张图为空

--- 正在分析第 34 张图 (Index: 34) ---
  [选择] 窗口框选命中: 0 个对象
  [结果] 第 34 张图为空

--- 正在分析第 35 张图 (Index: 35) ---
  [选择] 窗口框选命中: 0 个对象
  [结果] 第 35 张图为空

--- 正在分析第 36 张图 (Index: 36) ---
  [选择] 窗口框选命中: 0 个对象
  [结果] 第 36 张图为空

====== 处理结束，总计编号: 51 ======

sdy=select_print_areas_maxrect_from_polylines(
        lm=70, tol_single=0.01, layer_name="dy_zhuanyong",
        width=0.0, color=1, z=0.0, duanbian=70,
        debug=False, print_rejection_reason=False, cha_Y=5, 
    )
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.747s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.016s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.595 秒
sdy[0][0].color=6
g()
========== [PMXZ_BBOX] get_pmxz_group_bbox BEGIN ==========
确认版本v1.0
[PMXZ_BBOX] pmxz() 返回对象数量 = 1
[PMXZ_BBOX] 外包盒四角点: ((380662.0, 3073909.0, 0.0), (380872.0, 3074057.5, 0.0), (380662.0, 3074057.5, 0.0), (380872.0, 3073909.0, 0.0))
[PMXZ_BBOX] 矩形坐标 (x1,y1,x2,y2) = (380662.0, 3073909.0, 380872.0, 3074057.5)
========== [PMXZ_BBOX] get_pmxz_group_bbox END ==========
cc=found_titles = ss_select(
    mode="window", 
    p1=(380662.0, 3073909.0, 0),      # (x,y,z) 元组
    p2=(380872.0, 3074057.5,0),      # (x,y,z) 元组
    filter_types=[8],          # 组码 8 代表图层
    filter_data=["DIM_SYMB"]   # 图层名
)
len(cc)
2
get_attr(cc[0],"图名文字")
'未命名2'
get_attr(cc[1],"图名文字")
'未命名1'
def check_areas_selection_detail():
    li() # 初始化
    
    # 1. 获取打印区域
    print("正在获取区域列表...")
    sdy = select_print_areas_maxrect_from_polylines(
        lm=70, tol_single=0.01, layer_name="dy_zhuanyong",
        width=0.0, color=1, z=0.0, duanbian=70,
        debug=False, print_rejection_reason=False, cha_Y=5, 
    )
    polylines = sdy[0]
    
    print(f"\n共检测到 {len(polylines)} 个打印区域，开始逐个核对...")

    # 2. 逐个遍历，打印坐标和选中内容
    for i, pl in enumerate(polylines):
        print(f"\n========================================")
        print(f"正在检查第 {i} 张图 (Index: {i})")
        
        # A. 获取程序计算的包围盒
        try:
            min_pt, max_pt = pl.GetBoundingBox()
            # 格式化打印坐标，方便您对比
            print(f"【坐标诊断】:")
            print(f"  Min: ({min_pt[0]:.1f}, {min_pt[1]:.1f}, {min_pt[2]:.1f})")
            print(f"  Max: ({max_pt[0]:.1f}, {max_pt[1]:.1f}, {max_pt[2]:.1f})")
        except Exception as e:
            print(f"  获取包围盒失败: {e}")
            continue

        # B. 使用完全相同的参数进行选择
        cc = ss_select(
            mode="window", 
            p1=min_pt, 
            p2=max_pt, 
            filter_types=[8], 
            filter_data=["DIM_SYMB"]
        )
        
        # C. 打印结果
        print(f"【选择结果】: 选中了 {len(cc)} 个对象")
        
        if len(cc) > 0:
            # 先按您的习惯排序一下，方便看
            sorted_cc = sort_coms_by_llcorner(cc, cha_Y=50)
            
            for j, obj in enumerate(sorted_cc):
                # 获取文字内容
                txt = get_attr(obj, "图名文字")
                if txt is None:
                     txt = get_attr(obj, "TextString")
                
                print(f"  {j+1}. 内容: '{txt}'  (Handle: {obj.Handle})")
                
                # 如果数量异常（比如第0张图超过2个），额外打印一下它的位置，看是不是跑偏了
                if len(cc) > 2:
                    try:
                        ins = obj.InsertionPoint
                        print(f"     -> 坐标: ({ins[0]:.1f}, {ins[1]:.1f})")
                    except:
                        pass

    print("\n检查结束。")

    
check_areas_selection_detail()
正在获取区域列表...
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.747s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.017s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.308 秒

共检测到 37 个打印区域，开始逐个核对...

========================================
正在检查第 0 张图 (Index: 0)
【坐标诊断】:
  Min: (380662.0, 3073909.0, 0.0)
  Max: (380872.0, 3074057.5, 0.0)
【选择结果】: 选中了 12 个对象
  1. 内容: '未命名1'  (Handle: 4F43)
  2. 内容: '未命名2'  (Handle: 4F45)
  3. 内容: '未命名3'  (Handle: 4F50)
  4. 内容: '未命名4'  (Handle: 4F51)
  5. 内容: '未命名5'  (Handle: 4F52)
  6. 内容: '未命名6'  (Handle: 4F53)
  7. 内容: '未命名7'  (Handle: 4F47)
  8. 内容: '未命名8'  (Handle: 4F48)
  9. 内容: '未命名9'  (Handle: 4F54)
  10. 内容: '未命名10'  (Handle: 4F55)
  11. 内容: '未命名11'  (Handle: 4F56)
  12. 内容: '未命名12'  (Handle: 4F57)

========================================
正在检查第 1 张图 (Index: 1)
【坐标诊断】:
  Min: (380892.0, 3073909.0, 0.0)
  Max: (381102.0, 3074057.5, 0.0)
【选择结果】: 选中了 16 个对象
  1. 内容: '未命名1'  (Handle: 4F43)
  2. 内容: '未命名13'  (Handle: 4F4D)
  3. 内容: '未命名2'  (Handle: 4F45)
  4. 内容: '未命名3'  (Handle: 4F50)
  5. 内容: '未命名4'  (Handle: 4F51)
  6. 内容: '未命名5'  (Handle: 4F52)
  7. 内容: '未命名6'  (Handle: 4F53)
  8. 内容: '未命名14'  (Handle: 4F4E)
  9. 内容: '未命名7'  (Handle: 4F47)
  10. 内容: '未命名8'  (Handle: 4F48)
  11. 内容: '未命名9'  (Handle: 4F54)
  12. 内容: '未命名10'  (Handle: 4F55)
  13. 内容: '未命名11'  (Handle: 4F56)
  14. 内容: '未命名12'  (Handle: 4F57)
  15. 内容: '未命名15'  (Handle: 4F58)
  16. 内容: '未命名16'  (Handle: 4F59)

========================================
正在检查第 2 张图 (Index: 2)
【坐标诊断】:
  Min: (381122.0, 3073909.0, 0.0)
  Max: (381332.0, 3074057.5, 0.0)
【选择结果】: 选中了 20 个对象
  1. 内容: '未命名1'  (Handle: 4F43)
  2. 内容: '未命名13'  (Handle: 4F4D)
  3. 内容: '未命名17'  (Handle: 4F7D)
  4. 内容: '未命名2'  (Handle: 4F45)
  5. 内容: '未命名3'  (Handle: 4F50)
  6. 内容: '未命名4'  (Handle: 4F51)
  7. 内容: '未命名5'  (Handle: 4F52)
  8. 内容: '未命名6'  (Handle: 4F53)
  9. 内容: '未命名14'  (Handle: 4F4E)
  10. 内容: '未命名18'  (Handle: 4F7E)
  11. 内容: '未命名7'  (Handle: 4F47)
  12. 内容: '未命名8'  (Handle: 4F48)
  13. 内容: '未命名9'  (Handle: 4F54)
  14. 内容: '未命名10'  (Handle: 4F55)
  15. 内容: '未命名11'  (Handle: 4F56)
  16. 内容: '未命名12'  (Handle: 4F57)
  17. 内容: '未命名15'  (Handle: 4F58)
  18. 内容: '未命名16'  (Handle: 4F59)
  19. 内容: '未命名19'  (Handle: 4F5A)
  20. 内容: '未命名20'  (Handle: 4F5B)

========================================
正在检查第 3 张图 (Index: 3)
【坐标诊断】:
  Min: (381351.0, 3073909.0, 0.0)
  Max: (381561.0, 3074057.5, 0.0)
【选择结果】: 选中了 20 个对象
  1. 内容: '未命名13'  (Handle: 4F4D)
  2. 内容: '未命名17'  (Handle: 4F7D)
  3. 内容: '未命名3'  (Handle: 4F50)
  4. 内容: '未命名4'  (Handle: 4F51)
  5. 内容: '未命名5'  (Handle: 4F52)
  6. 内容: '未命名6'  (Handle: 4F53)
  7. 内容: '未命名14'  (Handle: 4F4E)
  8. 内容: '未命名18'  (Handle: 4F7E)
  9. 内容: '未命名21'  (Handle: 4F5C)
  10. 内容: '未命名22'  (Handle: 4F5D)
  11. 内容: '未命名9'  (Handle: 4F54)
  12. 内容: '未命名10'  (Handle: 4F55)
  13. 内容: '未命名11'  (Handle: 4F56)
  14. 内容: '未命名12'  (Handle: 4F57)
  15. 内容: '未命名15'  (Handle: 4F58)
  16. 内容: '未命名16'  (Handle: 4F59)
  17. 内容: '未命名19'  (Handle: 4F5A)
  18. 内容: '未命名20'  (Handle: 4F5B)
  19. 内容: '未命名23'  (Handle: 4F7B)
  20. 内容: '未命名24'  (Handle: 4F7C)

========================================
正在检查第 4 张图 (Index: 4)
【坐标诊断】:
  Min: (381587.0, 3073909.0, 0.0)
  Max: (381797.0, 3074057.5, 0.0)
【选择结果】: 选中了 20 个对象
  1. 内容: '未命名13'  (Handle: 4F4D)
  2. 内容: '未命名17'  (Handle: 4F7D)
  3. 内容: '未命名5'  (Handle: 4F52)
  4. 内容: '未命名6'  (Handle: 4F53)
  5. 内容: '未命名14'  (Handle: 4F4E)
  6. 内容: '未命名18'  (Handle: 4F7E)
  7. 内容: '未命名21'  (Handle: 4F5C)
  8. 内容: '未命名22'  (Handle: 4F5D)
  9. 内容: '未命名25'  (Handle: 4F5E)
  10. 内容: '未命名26'  (Handle: 4F5F)
  11. 内容: '未命名11'  (Handle: 4F56)
  12. 内容: '未命名12'  (Handle: 4F57)
  13. 内容: '未命名15'  (Handle: 4F58)
  14. 内容: '未命名16'  (Handle: 4F59)
  15. 内容: '未命名19'  (Handle: 4F5A)
  16. 内容: '未命名20'  (Handle: 4F5B)
  17. 内容: '未命名23'  (Handle: 4F7B)
  18. 内容: '未命名24'  (Handle: 4F7C)
  19. 内容: '未命名27'  (Handle: 4F62)
  20. 内容: '未命名28'  (Handle: 4F63)

========================================
正在检查第 5 张图 (Index: 5)
【坐标诊断】:
  Min: (381825.0, 3073909.0, 0.0)
  Max: (382035.0, 3074057.5, 0.0)
【选择结果】: 选中了 18 个对象
  1. 内容: '未命名17'  (Handle: 4F7D)
  2. 内容: '未命名18'  (Handle: 4F7E)
  3. 内容: '未命名21'  (Handle: 4F5C)
  4. 内容: '未命名22'  (Handle: 4F5D)
  5. 内容: '未命名25'  (Handle: 4F5E)
  6. 内容: '未命名26'  (Handle: 4F5F)
  7. 内容: '未命名29'  (Handle: 4F60)
  8. 内容: '未命名30'  (Handle: 4F61)
  9. 内容: '未命名15'  (Handle: 4F58)
  10. 内容: '未命名16'  (Handle: 4F59)
  11. 内容: '未命名19'  (Handle: 4F5A)
  12. 内容: '未命名20'  (Handle: 4F5B)
  13. 内容: '未命名23'  (Handle: 4F7B)
  14. 内容: '未命名24'  (Handle: 4F7C)
  15. 内容: '未命名27'  (Handle: 4F62)
  16. 内容: '未命名28'  (Handle: 4F63)
  17. 内容: '未命名31'  (Handle: 4F64)
  18. 内容: '未命名32'  (Handle: 4F65)

========================================
正在检查第 6 张图 (Index: 6)
【坐标诊断】:
  Min: (382054.0, 3073908.0, 0.0)
  Max: (382264.0, 3074056.5, 0.0)
【选择结果】: 选中了 17 个对象
  1. 内容: '未命名17'  (Handle: 4F7D)
  2. 内容: '未命名21'  (Handle: 4F5C)
  3. 内容: '未命名22'  (Handle: 4F5D)
  4. 内容: '未命名25'  (Handle: 4F5E)
  5. 内容: '未命名26'  (Handle: 4F5F)
  6. 内容: '未命名29'  (Handle: 4F60)
  7. 内容: '未命名30'  (Handle: 4F61)
  8. 内容: '未命名19'  (Handle: 4F5A)
  9. 内容: '未命名20'  (Handle: 4F5B)
  10. 内容: '未命名23'  (Handle: 4F7B)
  11. 内容: '未命名24'  (Handle: 4F7C)
  12. 内容: '未命名27'  (Handle: 4F62)
  13. 内容: '未命名28'  (Handle: 4F63)
  14. 内容: '未命名31'  (Handle: 4F64)
  15. 内容: '未命名32'  (Handle: 4F65)
  16. 内容: '未命名33'  (Handle: 4F66)
  17. 内容: '未命名34'  (Handle: 4F67)

========================================
正在检查第 7 张图 (Index: 7)
【坐标诊断】:
  Min: (382287.0, 3073908.0, 0.0)
  Max: (382497.0, 3074056.5, 0.0)
【选择结果】: 选中了 18 个对象
  1. 内容: '未命名21'  (Handle: 4F5C)
  2. 内容: '未命名22'  (Handle: 4F5D)
  3. 内容: '未命名25'  (Handle: 4F5E)
  4. 内容: '未命名26'  (Handle: 4F5F)
  5. 内容: '未命名29'  (Handle: 4F60)
  6. 内容: '未命名30'  (Handle: 4F61)
  7. 内容: '未命名35'  (Handle: 4F6C)
  8. 内容: '未命名36'  (Handle: 4F6D)
  9. 内容: '未命名23'  (Handle: 4F7B)
  10. 内容: '未命名24'  (Handle: 4F7C)
  11. 内容: '未命名27'  (Handle: 4F62)
  12. 内容: '未命名28'  (Handle: 4F63)
  13. 内容: '未命名31'  (Handle: 4F64)
  14. 内容: '未命名32'  (Handle: 4F65)
  15. 内容: '未命名33'  (Handle: 4F66)
  16. 内容: '未命名34'  (Handle: 4F67)
  17. 内容: '未命名37'  (Handle: 4F78)
  18. 内容: '未命名38'  (Handle: 4F79)

========================================
正在检查第 8 张图 (Index: 8)
【坐标诊断】:
  Min: (382515.0, 3073908.0, 0.0)
  Max: (382725.0, 3074056.5, 0.0)
【选择结果】: 选中了 17 个对象
  1. 内容: '未命名25'  (Handle: 4F5E)
  2. 内容: '未命名26'  (Handle: 4F5F)
  3. 内容: '未命名29'  (Handle: 4F60)
  4. 内容: '未命名30'  (Handle: 4F61)
  5. 内容: '未命名35'  (Handle: 4F6C)
  6. 内容: '未命名36'  (Handle: 4F6D)
  7. 内容: '未命名39'  (Handle: 4F6E)
  8. 内容: '未命名27'  (Handle: 4F62)
  9. 内容: '未命名28'  (Handle: 4F63)
  10. 内容: '未命名31'  (Handle: 4F64)
  11. 内容: '未命名32'  (Handle: 4F65)
  12. 内容: '未命名33'  (Handle: 4F66)
  13. 内容: '未命名34'  (Handle: 4F67)
  14. 内容: '未命名37'  (Handle: 4F78)
  15. 内容: '未命名38'  (Handle: 4F79)
  16. 内容: '未命名40'  (Handle: 4F68)
  17. 内容: '未命名41'  (Handle: 4F69)

========================================
正在检查第 9 张图 (Index: 9)
【坐标诊断】:
  Min: (382746.0, 3073908.0, 0.0)
  Max: (382956.0, 3074056.5, 0.0)
【选择结果】: 选中了 16 个对象
  1. 内容: '未命名29'  (Handle: 4F60)
  2. 内容: '未命名30'  (Handle: 4F61)
  3. 内容: '未命名35'  (Handle: 4F6C)
  4. 内容: '未命名36'  (Handle: 4F6D)
  5. 内容: '未命名39'  (Handle: 4F6E)
  6. 内容: '未命名42'  (Handle: 4F76)
  7. 内容: '未命名31'  (Handle: 4F64)
  8. 内容: '未命名32'  (Handle: 4F65)
  9. 内容: '未命名33'  (Handle: 4F66)
  10. 内容: '未命名34'  (Handle: 4F67)
  11. 内容: '未命名37'  (Handle: 4F78)
  12. 内容: '未命名38'  (Handle: 4F79)
  13. 内容: '未命名40'  (Handle: 4F68)
  14. 内容: '未命名41'  (Handle: 4F69)
  15. 内容: '未命名43'  (Handle: 4F6A)
  16. 内容: '未命名44'  (Handle: 4F6B)

========================================
正在检查第 10 张图 (Index: 10)
【坐标诊断】:
  Min: (382968.0, 3073908.0, 0.0)
  Max: (383178.0, 3074056.5, 0.0)
【选择结果】: 选中了 13 个对象
  1. 内容: '未命名35'  (Handle: 4F6C)
  2. 内容: '未命名36'  (Handle: 4F6D)
  3. 内容: '未命名39'  (Handle: 4F6E)
  4. 内容: '未命名42'  (Handle: 4F76)
  5. 内容: '未命名45'  (Handle: 4F77)
  6. 内容: '未命名33'  (Handle: 4F66)
  7. 内容: '未命名34'  (Handle: 4F67)
  8. 内容: '未命名37'  (Handle: 4F78)
  9. 内容: '未命名38'  (Handle: 4F79)
  10. 内容: '未命名40'  (Handle: 4F68)
  11. 内容: '未命名41'  (Handle: 4F69)
  12. 内容: '未命名43'  (Handle: 4F6A)
  13. 内容: '未命名44'  (Handle: 4F6B)

========================================
正在检查第 11 张图 (Index: 11)
【坐标诊断】:
  Min: (383205.0, 3073908.0, 0.0)
  Max: (383415.0, 3074056.5, 0.0)
【选择结果】: 选中了 13 个对象
  1. 内容: '未命名35'  (Handle: 4F6C)
  2. 内容: '未命名36'  (Handle: 4F6D)
  3. 内容: '未命名39'  (Handle: 4F6E)
  4. 内容: '未命名42'  (Handle: 4F76)
  5. 内容: '未命名45'  (Handle: 4F77)
  6. 内容: '未命名46'  (Handle: 4F70)
  7. 内容: '未命名47'  (Handle: 4F71)
  8. 内容: '未命名37'  (Handle: 4F78)
  9. 内容: '未命名38'  (Handle: 4F79)
  10. 内容: '未命名40'  (Handle: 4F68)
  11. 内容: '未命名41'  (Handle: 4F69)
  12. 内容: '未命名43'  (Handle: 4F6A)
  13. 内容: '未命名44'  (Handle: 4F6B)

========================================
正在检查第 12 张图 (Index: 12)
【坐标诊断】:
  Min: (383434.0, 3073908.0, 0.0)
  Max: (383644.0, 3074056.5, 0.0)
【选择结果】: 选中了 11 个对象
  1. 内容: '未命名39'  (Handle: 4F6E)
  2. 内容: '未命名42'  (Handle: 4F76)
  3. 内容: '未命名45'  (Handle: 4F77)
  4. 内容: '未命名46'  (Handle: 4F70)
  5. 内容: '未命名47'  (Handle: 4F71)
  6. 内容: '未命名48'  (Handle: 4F72)
  7. 内容: '未命名49'  (Handle: 4F73)
  8. 内容: '未命名40'  (Handle: 4F68)
  9. 内容: '未命名41'  (Handle: 4F69)
  10. 内容: '未命名43'  (Handle: 4F6A)
  11. 内容: '未命名44'  (Handle: 4F6B)

========================================
正在检查第 13 张图 (Index: 13)
【坐标诊断】:
  Min: (383667.0, 3073908.0, 0.0)
  Max: (383877.0, 3074056.5, 0.0)
【选择结果】: 选中了 10 个对象
  1. 内容: '未命名42'  (Handle: 4F76)
  2. 内容: '未命名45'  (Handle: 4F77)
  3. 内容: '未命名46'  (Handle: 4F70)
  4. 内容: '未命名47'  (Handle: 4F71)
  5. 内容: '未命名48'  (Handle: 4F72)
  6. 内容: '未命名49'  (Handle: 4F73)
  7. 内容: '未命名50'  (Handle: 4F74)
  8. 内容: '未命名51'  (Handle: 4F75)
  9. 内容: '未命名43'  (Handle: 4F6A)
  10. 内容: '未命名44'  (Handle: 4F6B)

========================================
正在检查第 14 张图 (Index: 14)
【坐标诊断】:
  Min: (383895.0, 3073908.0, 0.0)
  Max: (384105.0, 3074056.5, 0.0)
【选择结果】: 选中了 7 个对象
  1. 内容: '未命名45'  (Handle: 4F77)
  2. 内容: '未命名46'  (Handle: 4F70)
  3. 内容: '未命名47'  (Handle: 4F71)
  4. 内容: '未命名48'  (Handle: 4F72)
  5. 内容: '未命名49'  (Handle: 4F73)
  6. 内容: '未命名50'  (Handle: 4F74)
  7. 内容: '未命名51'  (Handle: 4F75)

========================================
正在检查第 15 张图 (Index: 15)
【坐标诊断】:
  Min: (384126.0, 3073908.0, 0.0)
  Max: (384336.0, 3074056.5, 0.0)
【选择结果】: 选中了 6 个对象
  1. 内容: '未命名46'  (Handle: 4F70)
  2. 内容: '未命名47'  (Handle: 4F71)
  3. 内容: '未命名48'  (Handle: 4F72)
  4. 内容: '未命名49'  (Handle: 4F73)
  5. 内容: '未命名50'  (Handle: 4F74)
  6. 内容: '未命名51'  (Handle: 4F75)

========================================
正在检查第 16 张图 (Index: 16)
【坐标诊断】:
  Min: (380662.0, 3073712.5, 0.0)
  Max: (380872.0, 3073861.0, 0.0)
【选择结果】: 选中了 12 个对象
  1. 内容: '未命名1'  (Handle: 4F43)
  2. 内容: '未命名2'  (Handle: 4F45)
  3. 内容: '未命名3'  (Handle: 4F50)
  4. 内容: '未命名4'  (Handle: 4F51)
  5. 内容: '未命名5'  (Handle: 4F52)
  6. 内容: '未命名6'  (Handle: 4F53)
  7. 内容: '未命名7'  (Handle: 4F47)
  8. 内容: '未命名8'  (Handle: 4F48)
  9. 内容: '未命名9'  (Handle: 4F54)
  10. 内容: '未命名10'  (Handle: 4F55)
  11. 内容: '未命名11'  (Handle: 4F56)
  12. 内容: '未命名12'  (Handle: 4F57)

========================================
正在检查第 17 张图 (Index: 17)
【坐标诊断】:
  Min: (380892.0, 3073712.5, 0.0)
  Max: (381102.0, 3073861.0, 0.0)
【选择结果】: 选中了 16 个对象
  1. 内容: '未命名1'  (Handle: 4F43)
  2. 内容: '未命名13'  (Handle: 4F4D)
  3. 内容: '未命名2'  (Handle: 4F45)
  4. 内容: '未命名3'  (Handle: 4F50)
  5. 内容: '未命名4'  (Handle: 4F51)
  6. 内容: '未命名5'  (Handle: 4F52)
  7. 内容: '未命名6'  (Handle: 4F53)
  8. 内容: '未命名14'  (Handle: 4F4E)
  9. 内容: '未命名7'  (Handle: 4F47)
  10. 内容: '未命名8'  (Handle: 4F48)
  11. 内容: '未命名9'  (Handle: 4F54)
  12. 内容: '未命名10'  (Handle: 4F55)
  13. 内容: '未命名11'  (Handle: 4F56)
  14. 内容: '未命名12'  (Handle: 4F57)
  15. 内容: '未命名15'  (Handle: 4F58)
  16. 内容: '未命名16'  (Handle: 4F59)

========================================
正在检查第 18 张图 (Index: 18)
【坐标诊断】:
  Min: (381122.0, 3073712.5, 0.0)
  Max: (381332.0, 3073861.0, 0.0)
【选择结果】: 选中了 20 个对象
  1. 内容: '未命名1'  (Handle: 4F43)
  2. 内容: '未命名13'  (Handle: 4F4D)
  3. 内容: '未命名17'  (Handle: 4F7D)
  4. 内容: '未命名2'  (Handle: 4F45)
  5. 内容: '未命名3'  (Handle: 4F50)
  6. 内容: '未命名4'  (Handle: 4F51)
  7. 内容: '未命名5'  (Handle: 4F52)
  8. 内容: '未命名6'  (Handle: 4F53)
  9. 内容: '未命名14'  (Handle: 4F4E)
  10. 内容: '未命名18'  (Handle: 4F7E)
  11. 内容: '未命名7'  (Handle: 4F47)
  12. 内容: '未命名8'  (Handle: 4F48)
  13. 内容: '未命名9'  (Handle: 4F54)
  14. 内容: '未命名10'  (Handle: 4F55)
  15. 内容: '未命名11'  (Handle: 4F56)
  16. 内容: '未命名12'  (Handle: 4F57)
  17. 内容: '未命名15'  (Handle: 4F58)
  18. 内容: '未命名16'  (Handle: 4F59)
  19. 内容: '未命名19'  (Handle: 4F5A)
  20. 内容: '未命名20'  (Handle: 4F5B)

========================================
正在检查第 19 张图 (Index: 19)
【坐标诊断】:
  Min: (381351.0, 3073712.5, 0.0)
  Max: (381561.0, 3073861.0, 0.0)
【选择结果】: 选中了 20 个对象
  1. 内容: '未命名13'  (Handle: 4F4D)
  2. 内容: '未命名17'  (Handle: 4F7D)
  3. 内容: '未命名3'  (Handle: 4F50)
  4. 内容: '未命名4'  (Handle: 4F51)
  5. 内容: '未命名5'  (Handle: 4F52)
  6. 内容: '未命名6'  (Handle: 4F53)
  7. 内容: '未命名14'  (Handle: 4F4E)
  8. 内容: '未命名18'  (Handle: 4F7E)
  9. 内容: '未命名21'  (Handle: 4F5C)
  10. 内容: '未命名22'  (Handle: 4F5D)
  11. 内容: '未命名9'  (Handle: 4F54)
  12. 内容: '未命名10'  (Handle: 4F55)
  13. 内容: '未命名11'  (Handle: 4F56)
  14. 内容: '未命名12'  (Handle: 4F57)
  15. 内容: '未命名15'  (Handle: 4F58)
  16. 内容: '未命名16'  (Handle: 4F59)
  17. 内容: '未命名19'  (Handle: 4F5A)
  18. 内容: '未命名20'  (Handle: 4F5B)
  19. 内容: '未命名23'  (Handle: 4F7B)
  20. 内容: '未命名24'  (Handle: 4F7C)

========================================
正在检查第 20 张图 (Index: 20)
【坐标诊断】:
  Min: (381587.0, 3073712.5, 0.0)
  Max: (381797.0, 3073861.0, 0.0)
【选择结果】: 选中了 20 个对象
  1. 内容: '未命名13'  (Handle: 4F4D)
  2. 内容: '未命名17'  (Handle: 4F7D)
  3. 内容: '未命名5'  (Handle: 4F52)
  4. 内容: '未命名6'  (Handle: 4F53)
  5. 内容: '未命名14'  (Handle: 4F4E)
  6. 内容: '未命名18'  (Handle: 4F7E)
  7. 内容: '未命名21'  (Handle: 4F5C)
  8. 内容: '未命名22'  (Handle: 4F5D)
  9. 内容: '未命名25'  (Handle: 4F5E)
  10. 内容: '未命名26'  (Handle: 4F5F)
  11. 内容: '未命名11'  (Handle: 4F56)
  12. 内容: '未命名12'  (Handle: 4F57)
  13. 内容: '未命名15'  (Handle: 4F58)
  14. 内容: '未命名16'  (Handle: 4F59)
  15. 内容: '未命名19'  (Handle: 4F5A)
  16. 内容: '未命名20'  (Handle: 4F5B)
  17. 内容: '未命名23'  (Handle: 4F7B)
  18. 内容: '未命名24'  (Handle: 4F7C)
  19. 内容: '未命名27'  (Handle: 4F62)
  20. 内容: '未命名28'  (Handle: 4F63)

========================================
正在检查第 21 张图 (Index: 21)
【坐标诊断】:
  Min: (381825.0, 3073712.5, 0.0)
  Max: (382035.0, 3073861.0, 0.0)
【选择结果】: 选中了 18 个对象
  1. 内容: '未命名17'  (Handle: 4F7D)
  2. 内容: '未命名18'  (Handle: 4F7E)
  3. 内容: '未命名21'  (Handle: 4F5C)
  4. 内容: '未命名22'  (Handle: 4F5D)
  5. 内容: '未命名25'  (Handle: 4F5E)
  6. 内容: '未命名26'  (Handle: 4F5F)
  7. 内容: '未命名29'  (Handle: 4F60)
  8. 内容: '未命名30'  (Handle: 4F61)
  9. 内容: '未命名15'  (Handle: 4F58)
  10. 内容: '未命名16'  (Handle: 4F59)
  11. 内容: '未命名19'  (Handle: 4F5A)
  12. 内容: '未命名20'  (Handle: 4F5B)
  13. 内容: '未命名23'  (Handle: 4F7B)
  14. 内容: '未命名24'  (Handle: 4F7C)
  15. 内容: '未命名27'  (Handle: 4F62)
  16. 内容: '未命名28'  (Handle: 4F63)
  17. 内容: '未命名31'  (Handle: 4F64)
  18. 内容: '未命名32'  (Handle: 4F65)

========================================
正在检查第 22 张图 (Index: 22)
【坐标诊断】:
  Min: (382054.0, 3073711.5, 0.0)
  Max: (382264.0, 3073860.0, 0.0)
【选择结果】: 选中了 17 个对象
  1. 内容: '未命名17'  (Handle: 4F7D)
  2. 内容: '未命名21'  (Handle: 4F5C)
  3. 内容: '未命名22'  (Handle: 4F5D)
  4. 内容: '未命名25'  (Handle: 4F5E)
  5. 内容: '未命名26'  (Handle: 4F5F)
  6. 内容: '未命名29'  (Handle: 4F60)
  7. 内容: '未命名30'  (Handle: 4F61)
  8. 内容: '未命名19'  (Handle: 4F5A)
  9. 内容: '未命名20'  (Handle: 4F5B)
  10. 内容: '未命名23'  (Handle: 4F7B)
  11. 内容: '未命名24'  (Handle: 4F7C)
  12. 内容: '未命名27'  (Handle: 4F62)
  13. 内容: '未命名28'  (Handle: 4F63)
  14. 内容: '未命名31'  (Handle: 4F64)
  15. 内容: '未命名32'  (Handle: 4F65)
  16. 内容: '未命名33'  (Handle: 4F66)
  17. 内容: '未命名34'  (Handle: 4F67)

========================================
正在检查第 23 张图 (Index: 23)
【坐标诊断】:
  Min: (382287.0, 3073711.5, 0.0)
  Max: (382497.0, 3073860.0, 0.0)
【选择结果】: 选中了 18 个对象
  1. 内容: '未命名21'  (Handle: 4F5C)
  2. 内容: '未命名22'  (Handle: 4F5D)
  3. 内容: '未命名25'  (Handle: 4F5E)
  4. 内容: '未命名26'  (Handle: 4F5F)
  5. 内容: '未命名29'  (Handle: 4F60)
  6. 内容: '未命名30'  (Handle: 4F61)
  7. 内容: '未命名35'  (Handle: 4F6C)
  8. 内容: '未命名36'  (Handle: 4F6D)
  9. 内容: '未命名23'  (Handle: 4F7B)
  10. 内容: '未命名24'  (Handle: 4F7C)
  11. 内容: '未命名27'  (Handle: 4F62)
  12. 内容: '未命名28'  (Handle: 4F63)
  13. 内容: '未命名31'  (Handle: 4F64)
  14. 内容: '未命名32'  (Handle: 4F65)
  15. 内容: '未命名33'  (Handle: 4F66)
  16. 内容: '未命名34'  (Handle: 4F67)
  17. 内容: '未命名37'  (Handle: 4F78)
  18. 内容: '未命名38'  (Handle: 4F79)

========================================
正在检查第 24 张图 (Index: 24)
【坐标诊断】:
  Min: (382515.0, 3073711.5, 0.0)
  Max: (382725.0, 3073860.0, 0.0)
【选择结果】: 选中了 17 个对象
  1. 内容: '未命名25'  (Handle: 4F5E)
  2. 内容: '未命名26'  (Handle: 4F5F)
  3. 内容: '未命名29'  (Handle: 4F60)
  4. 内容: '未命名30'  (Handle: 4F61)
  5. 内容: '未命名35'  (Handle: 4F6C)
  6. 内容: '未命名36'  (Handle: 4F6D)
  7. 内容: '未命名39'  (Handle: 4F6E)
  8. 内容: '未命名27'  (Handle: 4F62)
  9. 内容: '未命名28'  (Handle: 4F63)
  10. 内容: '未命名31'  (Handle: 4F64)
  11. 内容: '未命名32'  (Handle: 4F65)
  12. 内容: '未命名33'  (Handle: 4F66)
  13. 内容: '未命名34'  (Handle: 4F67)
  14. 内容: '未命名37'  (Handle: 4F78)
  15. 内容: '未命名38'  (Handle: 4F79)
  16. 内容: '未命名40'  (Handle: 4F68)
  17. 内容: '未命名41'  (Handle: 4F69)

========================================
正在检查第 25 张图 (Index: 25)
【坐标诊断】:
  Min: (382746.0, 3073711.5, 0.0)
  Max: (382956.0, 3073860.0, 0.0)
【选择结果】: 选中了 16 个对象
  1. 内容: '未命名29'  (Handle: 4F60)
  2. 内容: '未命名30'  (Handle: 4F61)
  3. 内容: '未命名35'  (Handle: 4F6C)
  4. 内容: '未命名36'  (Handle: 4F6D)
  5. 内容: '未命名39'  (Handle: 4F6E)
  6. 内容: '未命名42'  (Handle: 4F76)
  7. 内容: '未命名31'  (Handle: 4F64)
  8. 内容: '未命名32'  (Handle: 4F65)
  9. 内容: '未命名33'  (Handle: 4F66)
  10. 内容: '未命名34'  (Handle: 4F67)
  11. 内容: '未命名37'  (Handle: 4F78)
  12. 内容: '未命名38'  (Handle: 4F79)
  13. 内容: '未命名40'  (Handle: 4F68)
  14. 内容: '未命名41'  (Handle: 4F69)
  15. 内容: '未命名43'  (Handle: 4F6A)
  16. 内容: '未命名44'  (Handle: 4F6B)

========================================
正在检查第 26 张图 (Index: 26)
【坐标诊断】:
  Min: (382968.0, 3073711.5, 0.0)
  Max: (383178.0, 3073860.0, 0.0)
【选择结果】: 选中了 13 个对象
  1. 内容: '未命名35'  (Handle: 4F6C)
  2. 内容: '未命名36'  (Handle: 4F6D)
  3. 内容: '未命名39'  (Handle: 4F6E)
  4. 内容: '未命名42'  (Handle: 4F76)
  5. 内容: '未命名45'  (Handle: 4F77)
  6. 内容: '未命名33'  (Handle: 4F66)
  7. 内容: '未命名34'  (Handle: 4F67)
  8. 内容: '未命名37'  (Handle: 4F78)
  9. 内容: '未命名38'  (Handle: 4F79)
  10. 内容: '未命名40'  (Handle: 4F68)
  11. 内容: '未命名41'  (Handle: 4F69)
  12. 内容: '未命名43'  (Handle: 4F6A)
  13. 内容: '未命名44'  (Handle: 4F6B)

========================================
正在检查第 27 张图 (Index: 27)
【坐标诊断】:
  Min: (383196.0, 3073711.5, 0.0)
  Max: (383406.0, 3073860.0, 0.0)
【选择结果】: 选中了 13 个对象
  1. 内容: '未命名35'  (Handle: 4F6C)
  2. 内容: '未命名36'  (Handle: 4F6D)
  3. 内容: '未命名39'  (Handle: 4F6E)
  4. 内容: '未命名42'  (Handle: 4F76)
  5. 内容: '未命名45'  (Handle: 4F77)
  6. 内容: '未命名46'  (Handle: 4F70)
  7. 内容: '未命名47'  (Handle: 4F71)
  8. 内容: '未命名37'  (Handle: 4F78)
  9. 内容: '未命名38'  (Handle: 4F79)
  10. 内容: '未命名40'  (Handle: 4F68)
  11. 内容: '未命名41'  (Handle: 4F69)
  12. 内容: '未命名43'  (Handle: 4F6A)
  13. 内容: '未命名44'  (Handle: 4F6B)

========================================
正在检查第 28 张图 (Index: 28)
【坐标诊断】:
  Min: (-336.0, 701.2, 0.0)
  Max: (84.0, 998.2, 0.0)
【选择结果】: 选中了 0 个对象

========================================
正在检查第 29 张图 (Index: 29)
【坐标诊断】:
  Min: (137.9, 701.2, 0.0)
  Max: (557.9, 998.2, 0.0)
【选择结果】: 选中了 0 个对象

========================================
正在检查第 30 张图 (Index: 30)
  获取包围盒失败: (-2147418111, '被呼叫方拒绝接收呼叫。', None, None)

========================================
正在检查第 31 张图 (Index: 31)
【坐标诊断】:
  Min: (1119.3, 701.2, 0.0)
  Max: (1539.3, 998.2, 0.0)
【选择结果】: 选中了 0 个对象

========================================
正在检查第 32 张图 (Index: 32)
【坐标诊断】:
  Min: (1617.8, 701.2, 0.0)
  Max: (2037.8, 998.2, 0.0)
【选择结果】: 选中了 0 个对象

========================================
正在检查第 33 张图 (Index: 33)
【坐标诊断】:
  Min: (2116.2, 701.2, 0.0)
  Max: (2536.2, 998.2, 0.0)
【选择结果】: 选中了 0 个对象

========================================
正在检查第 34 张图 (Index: 34)
【坐标诊断】:
  Min: (2614.7, 701.2, 0.0)
  Max: (3034.7, 998.2, 0.0)
【选择结果】: 选中了 0 个对象

========================================
正在检查第 35 张图 (Index: 35)
【坐标诊断】:
  Min: (3113.2, 701.2, 0.0)
  Max: (3533.2, 998.2, 0.0)
【选择结果】: 选中了 0 个对象

========================================
正在检查第 36 张图 (Index: 36)
【坐标诊断】:
  Min: (3611.7, 701.2, 0.0)
  Max: (4031.7, 998.2, 0.0)
【选择结果】: 选中了 0 个对象

检查结束。
sdy = select_print_areas_maxrect_from_polylines(
        lm=70, tol_single=0.01, layer_name="dy_zhuanyong",
        width=0.0, color=1, z=0.0, duanbian=70,
        debug=False, print_rejection_reason=False, cha_Y=5, 
    )

⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.763s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.016s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.299 秒
for i in range(0,len(sdy)) :

    pl=sdy[i]

    lk=ss_select(
        mode="window", 
        p1=pl.GetBoundingBox()[0],      # (x,y,z) 元组
        p2=pl.GetBoundingBox()[1],      # (x,y,z) 元组
        filter_types=[8],          # 组码 8 代表图层
        filter_data=["DIM_SYMB"]   # 图层名
    )
    print("第",i,"打印区：")
    for xx in lk:

        name = get_attr(xx,"图名文字")

        print(name)

        
Traceback (most recent call last):
  File "<pyshell#51>", line 7, in <module>
    p1=pl.GetBoundingBox()[0],      # (x,y,z) 元组
AttributeError: 'list' object has no attribute 'GetBoundingBox'
sdy = select_print_areas_maxrect_from_polylines(
    lm=70, tol_single=0.01, layer_name="dy_zhuanyong",
    width=0.0, color=1, z=0.0, duanbian=70,
    debug=False, print_rejection_reason=False, cha_Y=5, 
)
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.759s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.016s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：3.407 秒
polylines = sdy[0]
for i, pl in enumerate(polylines):
    
    # 【修正3】一次性获取包围盒，避免重复调用
    try:
        min_pt, max_pt = pl.GetBoundingBox()
    except:
        print(f"第 {i} 打印区：无法获取包围盒")
        continue

    # 【关键修正4】必须缩放视图！否则后面的图会选错！
    try:
        p1_var = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, min_pt)
        p2_var = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, max_pt)
        acad_app.ZoomWindow(p1_var, p2_var)
    except:
        pass

    # 执行选择
    lk = ss_select(
        mode="window", 
        p1=min_pt,      # 直接使用解包后的变量
        p2=max_pt, 
        filter_types=[8], 
        filter_data=["DIM_SYMB"]
    )

    print(f"第 {i} 打印区（命中 {len(lk)} 个）：")
    
    if lk:
        # 如果需要排序，可以在这里加: lk = sort_coms_by_llcorner(lk, cha_Y=50)
        for xx in lk:
            # 尝试获取图名，如果"图名文字"属性不存在则获取"TextString"
            name = get_attr(xx, "图名文字")
            if name is None:
                name = get_attr(xx, "TextString")
            print(f"  - {name}")
    else:
        print("  (空)")

        
第 0 打印区（命中 12 个）：
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
第 1 打印区（命中 16 个）：
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
第 2 打印区（命中 20 个）：
  - 未命名18
  - 未命名17
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
第 3 打印区（命中 20 个）：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
第 4 打印区（命中 20 个）：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名28
  - 未命名27
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名6
  - 未命名5
  - 未命名14
  - 未命名13
第 5 打印区（命中 18 个）：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
第 6 打印区（命中 17 个）：
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
第 7 打印区（命中 18 个）：
  - 未命名24
  - 未命名23
  - 未命名38
  - 未命名37
  - 未命名36
  - 未命名35
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
第 8 打印区（命中 17 个）：
  - 未命名38
  - 未命名37
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
第 9 打印区（命中 16 个）：
  - 未命名38
  - 未命名37
  - 未命名42
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名30
  - 未命名29
第 10 打印区（命中 13 个）：
  - 未命名38
  - 未命名37
  - 未命名45
  - 未命名42
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
第 11 打印区（命中 13 个）：
  - 未命名38
  - 未命名37
  - 未命名45
  - 未命名42
  - 未命名47
  - 未命名46
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
第 12 打印区（命中 11 个）：
  - 未命名45
  - 未命名42
  - 未命名49
  - 未命名48
  - 未命名47
  - 未命名46
  - 未命名39
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
第 13 打印区（命中 10 个）：
  - 未命名45
  - 未命名42
  - 未命名51
  - 未命名50
  - 未命名49
  - 未命名48
  - 未命名47
  - 未命名46
  - 未命名44
  - 未命名43
第 14 打印区（命中 7 个）：
  - 未命名45
  - 未命名51
  - 未命名50
  - 未命名49
  - 未命名48
  - 未命名47
  - 未命名46
第 15 打印区（命中 6 个）：
  - 未命名51
  - 未命名50
  - 未命名49
  - 未命名48
  - 未命名47
  - 未命名46
第 16 打印区（命中 12 个）：
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
第 17 打印区（命中 16 个）：
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
第 18 打印区（命中 20 个）：
  - 未命名18
  - 未命名17
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
第 19 打印区（命中 20 个）：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
第 20 打印区（命中 20 个）：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名28
  - 未命名27
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名6
  - 未命名5
  - 未命名14
  - 未命名13
第 21 打印区（命中 18 个）：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
第 22 打印区（命中 17 个）：
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
第 23 打印区（命中 18 个）：
  - 未命名24
  - 未命名23
  - 未命名38
  - 未命名37
  - 未命名36
  - 未命名35
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
第 24 打印区（命中 17 个）：
  - 未命名38
  - 未命名37
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
第 25 打印区（命中 16 个）：
  - 未命名38
  - 未命名37
  - 未命名42
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名30
  - 未命名29
第 26 打印区（命中 13 个）：
  - 未命名38
  - 未命名37
  - 未命名45
  - 未命名42
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
第 27 打印区（命中 13 个）：
  - 未命名38
  - 未命名37
  - 未命名45
  - 未命名42
  - 未命名47
  - 未命名46
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
第 28 打印区（命中 0 个）：
  (空)
第 29 打印区（命中 0 个）：
  (空)
第 30 打印区（命中 0 个）：
  (空)
第 31 打印区（命中 0 个）：
  (空)
第 32 打印区（命中 0 个）：
  (空)
第 33 打印区（命中 0 个）：
  (空)
第 34 打印区（命中 0 个）：
  (空)
第 35 打印区（命中 0 个）：
  (空)
第 36 打印区（命中 0 个）：
  (空)
def get_sorted_titles_by_areas(layer_name="DIM_SYMB"):
    # 1. 初始化
    li()
    
    # 2. 获取数据 (sdy[0] 是已排序的列表)
    sdy = select_print_areas_maxrect_from_polylines(
        lm=70, tol_single=0.01, layer_name="dy_zhuanyong",
        width=0.0, color=1, z=0.0, duanbian=70,
        debug=False, print_rejection_reason=False, cha_Y=5, 
    )
    polylines = sdy[0]

    # 3. 循环处理
    for i, pl in enumerate(polylines):
        try:
            min_pt, max_pt = pl.GetBoundingBox()
            x1, y1 = min_pt[0], min_pt[1]
            x2, y2 = max_pt[0], max_pt[1]
        except:
            print(f"第 {i} 打印区：无效的包围盒")
            continue

        # 使用您的新函数进行选择
        lk = select_objects_in_window_area(
            x1, y1, x2, y2, 
            layer_filter=layer_name
        )

        print(f"第 {i} 打印区（命中 {len(lk)} 个）：")
        
        # 如果需要排序
        if lk:
            # 排序逻辑: 上到下，左到右
            # 这里需要引用之前的 sort_coms_by_llcorner 函数
            lk_sorted = sort_coms_by_llcorner(lk, cha_Y=50)
            
            for xx in lk_sorted:
                try:
                    name = get_attr(xx, "图名文字")
                    if name is None: name = get_attr(xx, "TextString")
                    print(f"  - {name}")
                except:
                    pass
        else:
            print("  (空)")

            
get_sorted_titles_by_areas(layer_name="DIM_SYMB")
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.748s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.015s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：3.397 秒
Traceback (most recent call last):
  File "<pyshell#58>", line 1, in <module>
    get_sorted_titles_by_areas(layer_name="DIM_SYMB")
  File "<pyshell#57>", line 24, in get_sorted_titles_by_areas
    lk = select_objects_in_window_area(
TypeError: select_objects_in_window_area() got an unexpected keyword argument 'layer_filter'
sdy = select_print_areas_maxrect_from_polylines(
        lm=70, tol_single=0.01, layer_name="dy_zhuanyong",
        width=0.0, color=1, z=0.0, duanbian=70,
        debug=False, print_rejection_reason=False, cha_Y=5, 
    )
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.765s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.016s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[错误] 绘制多段线失败: (-2147418111, '被呼叫方拒绝接收呼叫。', None, None)
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.420 秒
for i in range(0,len(sdy)) :

    pl=sdy[i]

    p1=pl.GetBoundingBox()[0],      # (x,y,z) 元组
    p2=pl.GetBoundingBox()[1],
    x1=p1[0]
    y1=p1[1]
    x2=p2[0]
    y2=p2[1]
    
    lk=select_objects_in_window_area(x1, y1, x2, y2, max_retry=5)


    
    print("第",i,"打印区：")
    for xx in lk:

        name = get_attr(xx,"图名文字")

        print(name)

Traceback (most recent call last):
  File "<pyshell#61>", line 5, in <module>
    p1=pl.GetBoundingBox()[0],      # (x,y,z) 元组
AttributeError: 'list' object has no attribute 'GetBoundingBox'
for i in range(0,len(sdy[0])) :

    pl=sdy[i]

    p1=pl.GetBoundingBox()[0],      # (x,y,z) 元组
    p2=pl.GetBoundingBox()[1],
    x1=p1[0]
    y1=p1[1]
    x2=p2[0]
    y2=p2[1]
    
    lk=select_objects_in_window_area(x1, y1, x2, y2, max_retry=5)


    
    print("第",i,"打印区：")
    for xx in lk:

        name = get_attr(xx,"图名文字")

        print(name)

Traceback (most recent call last):
  File "<pyshell#63>", line 5, in <module>
    p1=pl.GetBoundingBox()[0],      # (x,y,z) 元组
AttributeError: 'list' object has no attribute 'GetBoundingBox'
for i in range(0,len(sdy[0])) :

    pl=sdy[0][i]

    p1=pl.GetBoundingBox()[0],      # (x,y,z) 元组
    p2=pl.GetBoundingBox()[1],
    x1=p1[0]
    y1=p1[1]
    x2=p2[0]
    y2=p2[1]
    
    lk=select_objects_in_window_area(x1, y1, x2, y2, max_retry=5)


    
    print("第",i,"打印区：")
    for xx in lk:

        name = get_attr(xx,"图名文字")

        print(name)

Traceback (most recent call last):
  File "<pyshell#65>", line 8, in <module>
    y1=p1[1]
IndexError: tuple index out of range
polylines = sdy[0]
for i, pl in enumerate(polylines):
    
    # --- 修正 1: 正确的包围盒解包 ---
    try:
        # GetBoundingBox 返回两个点：(MinPoint, MaxPoint)
        min_pt, max_pt = pl.GetBoundingBox()
        
        # 提取坐标 (用于 select 函数)
        x1, y1 = min_pt[0], min_pt[1]
        x2, y2 = max_pt[0], max_pt[1]
    except Exception:
        print(f"第 {i} 打印区：无法获取几何范围，跳过")
        continue

    # --- 修正 2: 必须强制缩放视图 (防止选错) ---
    if acad_app:
        try:
            p1_var = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, min_pt)
            p2_var = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, max_pt)
            acad_app.ZoomWindow(p1_var, p2_var)
        except:
            pass

    # --- 执行选择 ---
    # 注意：这个函数会返回框内的“所有”东西
    lk = select_objects_in_window_area(x1, y1, x2, y2, max_retry=5)

    print(f"第 {i} 打印区：")
    
    found_count = 0
    if lk:
        # (可选) 如果你希望图名按位置排序，请取消下面注释
        # lk = sort_coms_by_llcorner(lk, cha_Y=50)

        for xx in lk:
            # --- 修正 3: 增加过滤 (只处理图名图层) ---
            # 如果不加这一步，墙线、标注等没有"图名文字"属性的对象也会报错或打印None
            try:
                # 假设图名都在 "DIM_SYMB" 图层
                if xx.Layer == "DIM_SYMB": 
                    name = get_attr(xx, "图名文字")
                    # 兜底：如果是普通文字对象，取 TextString
                    if name is None:
                        name = get_attr(xx, "TextString")
                    
                    if name:
                        print(f"  - {name}")
                        found_count += 1
            except:
                continue
    
    if found_count == 0:
        print("  (空)")

        
Traceback (most recent call last):
  File "<pyshell#68>", line 16, in <module>
    if acad_app:
NameError: name 'acad_app' is not defined
try:
    acad_app = win32com.client.Dispatch("AutoCAD.Application")
except:
    acad_app = None

    
for i, pl in enumerate(polylines):
    
    # --- 修正 1: 正确的包围盒解包 ---
    try:
        # GetBoundingBox 返回两个点：(MinPoint, MaxPoint)
        min_pt, max_pt = pl.GetBoundingBox()
        
        # 提取坐标 (用于 select 函数)
        x1, y1 = min_pt[0], min_pt[1]
        x2, y2 = max_pt[0], max_pt[1]
    except Exception:
        print(f"第 {i} 打印区：无法获取几何范围，跳过")
        continue

    # --- 修正 2: 必须强制缩放视图 (防止选错) ---
    if acad_app:
        try:
            p1_var = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, min_pt)
            p2_var = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, max_pt)
            acad_app.ZoomWindow(p1_var, p2_var)
        except:
            pass

    # --- 执行选择 ---
    # 注意：这个函数会返回框内的“所有”东西
    lk = select_objects_in_window_area(x1, y1, x2, y2, max_retry=5)

    print(f"第 {i} 打印区：")
    
    found_count = 0
    if lk:
        # (可选) 如果你希望图名按位置排序，请取消下面注释
        # lk = sort_coms_by_llcorner(lk, cha_Y=50)

        for xx in lk:
            # --- 修正 3: 增加过滤 (只处理图名图层) ---
            # 如果不加这一步，墙线、标注等没有"图名文字"属性的对象也会报错或打印None
            try:
                # 假设图名都在 "DIM_SYMB" 图层
                if xx.Layer == "DIM_SYMB": 
                    name = get_attr(xx, "图名文字")
                    # 兜底：如果是普通文字对象，取 TextString
                    if name is None:
                        name = get_attr(xx, "TextString")
                    
                    if name:
                        print(f"  - {name}")
                        found_count += 1
            except:
                continue
    
    if found_count == 0:
        print("  (空)")

        
[OK] 窗口选择成功，共 8 个对象。
第 0 打印区：
  - 未命名2
  - 未命名1
Traceback (most recent call last):
  File "C:\Users\User\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32com\client\gencache.py", line 650, in EnsureDispatch
    ti = disp._oleobj_.GetTypeInfo()
pywintypes.com_error: (-2147418111, '被呼叫方拒绝接收呼叫。', None, None)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "D:/claude-tasks/cad/scripts/CAD_basic.py", line 2528, in get_acad_doc
    app = win32.gencache.EnsureDispatch(app)
  File "C:\Users\User\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32com\client\gencache.py", line 662, in EnsureDispatch
    raise TypeError(
TypeError: This COM object can not automate the makepy process - please run makepy manually for this object

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\User\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32com\client\gencache.py", line 650, in EnsureDispatch
    ti = disp._oleobj_.GetTypeInfo()
pywintypes.com_error: (-2147418111, '被呼叫方拒绝接收呼叫。', None, None)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<pyshell#72>", line 26, in <module>
    lk = select_objects_in_window_area(x1, y1, x2, y2, max_retry=5)
  File "D:/claude-tasks/cad/scripts/CAD_basic.py", line 3567, in select_objects_in_window_area
    _, doc = get_acad_doc()
  File "D:/claude-tasks/cad/scripts/CAD_basic.py", line 2531, in get_acad_doc
    app = win32.gencache.EnsureDispatch("AutoCAD.Application")
  File "C:\Users\User\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32com\client\gencache.py", line 662, in EnsureDispatch
    raise TypeError(
TypeError: This COM object can not automate the makepy process - please run makepy manually for this object
sdy = select_print_areas_maxrect_from_polylines(
    lm=70, tol_single=0.01, layer_name="dy_zhuanyong",
    width=0.0, color=1, z=0.0, duanbian=70,
    debug=False, print_rejection_reason=False, cha_Y=5, 
)
⏱ 开始 `select_print_areas_maxrect_from_polylines` …
[OK] 当前图层已设置为：dy_zhuanyong
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 37 个对象
  第 1 次删除：共删除 37 个对象
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
[OK] 第 1 次尝试：选到图层 ['dy_zhuanyong'] 上 0 个对象
[OK] select_polyline 成功（第 1 次），耗时 0.762s，共 184 条
[OK] select_polyline_chuantong 成功（第 1 次），耗时 0.017s，共 0 条
📌 最终锁定打印区域: 37 个
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
🎨 重绘完成，数量: 37。正在执行空间排序...
正在分析 37 个对象进行去重...
✅ 去重完成：处理 37 个，删除 0 个，保留 37 个。
🔢 排序与信息生成完毕，返回结果。
⏱ 完成 `select_print_areas_maxrect_from_polylines`，耗时：4.314 秒
polylines = sdy[0]
for i, pl in enumerate(polylines):
    
    # 1. 获取包围盒 (修正了之前的语法错误)
    try:
        min_pt, max_pt = pl.GetBoundingBox()
        x1, y1 = min_pt[0], min_pt[1]
        x2, y2 = max_pt[0], max_pt[1]
    except Exception:
        print(f"第 {i} 打印区：无法获取几何范围，跳过")
        continue

    # [已删除] acad_app.ZoomWindow(...) <-- 视图相关代码已移除

    # 2. 执行选择
    # 注意：select_objects_in_window_area 返回的是区域内的【所有对象】
    lk = select_objects_in_window_area(x1, y1, x2, y2, max_retry=1) # retry 设为1即可，因为没有zoom，重试也没用

    print(f"第 {i} 打印区：")
    
    found_count = 0
    if lk:
        for xx in lk:
            try:
                # 3. 必须过滤图层！只处理图名
                if xx.Layer == "DIM_SYMB": 
                    name = get_attr(xx, "图名文字")
                    if name is None:
                        name = get_attr(xx, "TextString")
                    
                    if name:
                        print(f"  - {name}")
                        found_count += 1
            except:
                continue
    
    if found_count == 0:
        print("  (空)")

        
[OK] 窗口选择成功，共 271 个对象。
第 0 打印区：
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
[OK] 窗口选择成功，共 395 个对象。
第 1 打印区：
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
[OK] 窗口选择成功，共 663 个对象。
第 2 打印区：
  - 未命名18
  - 未命名17
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
[OK] 窗口选择成功，共 763 个对象。
第 3 打印区：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
[OK] 窗口选择成功，共 652 个对象。
第 4 打印区：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名28
  - 未命名27
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名6
  - 未命名5
  - 未命名14
  - 未命名13
[OK] 窗口选择成功，共 546 个对象。
第 5 打印区：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名14
  - 未命名13
[OK] 窗口选择成功，共 428 个对象。
第 6 打印区：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
[OK] 窗口选择成功，共 135 个对象。
第 7 打印区：
  - 未命名24
  - 未命名23
  - 未命名38
  - 未命名37
  - 未命名36
  - 未命名35
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
[OK] 窗口选择成功，共 75 个对象。
第 8 打印区：
  - 未命名38
  - 未命名37
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
[OK] 窗口选择成功，共 71 个对象。
第 9 打印区：
  - 未命名38
  - 未命名37
  - 未命名42
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名30
  - 未命名29
[OK] 窗口选择成功，共 61 个对象。
第 10 打印区：
  - 未命名38
  - 未命名37
  - 未命名45
  - 未命名42
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
[OK] 窗口选择成功，共 57 个对象。
第 11 打印区：
  - 未命名38
  - 未命名37
  - 未命名45
  - 未命名42
  - 未命名47
  - 未命名46
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
[OK] 窗口选择成功，共 49 个对象。
第 12 打印区：
  - 未命名45
  - 未命名42
  - 未命名49
  - 未命名48
  - 未命名47
  - 未命名46
  - 未命名39
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
[OK] 窗口选择成功，共 43 个对象。
第 13 打印区：
  - 未命名45
  - 未命名42
  - 未命名51
  - 未命名50
  - 未命名49
  - 未命名48
  - 未命名47
  - 未命名46
  - 未命名44
  - 未命名43
[OK] 窗口选择成功，共 31 个对象。
第 14 打印区：
  - 未命名45
  - 未命名51
  - 未命名50
  - 未命名49
  - 未命名48
  - 未命名47
  - 未命名46
[OK] 窗口选择成功，共 25 个对象。
第 15 打印区：
  - 未命名51
  - 未命名50
  - 未命名49
  - 未命名48
  - 未命名47
  - 未命名46
[OK] 窗口选择成功，共 45 个对象。
第 16 打印区：
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
[OK] 窗口选择成功，共 61 个对象。
第 17 打印区：
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
[OK] 窗口选择成功，共 229 个对象。
第 18 打印区：
  - 未命名18
  - 未命名17
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
  - 未命名8
  - 未命名7
  - 未命名2
  - 未命名1
[OK] 窗口选择成功，共 359 个对象。
第 19 打印区：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名10
  - 未命名9
  - 未命名6
  - 未命名5
  - 未命名4
  - 未命名3
  - 未命名14
  - 未命名13
[OK] 窗口选择成功，共 360 个对象。
第 20 打印区：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名28
  - 未命名27
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名12
  - 未命名11
  - 未命名6
  - 未命名5
  - 未命名14
  - 未命名13
[OK] 窗口选择成功，共 360 个对象。
第 21 打印区：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
  - 未命名16
  - 未命名15
  - 未命名14
  - 未命名13
[OK] 窗口选择成功，共 354 个对象。
第 22 打印区：
  - 未命名18
  - 未命名17
  - 未命名24
  - 未命名23
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
  - 未命名20
  - 未命名19
[OK] 窗口选择成功，共 135 个对象。
第 23 打印区：
  - 未命名24
  - 未命名23
  - 未命名38
  - 未命名37
  - 未命名36
  - 未命名35
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
  - 未命名22
  - 未命名21
[OK] 窗口选择成功，共 75 个对象。
第 24 打印区：
  - 未命名38
  - 未命名37
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名28
  - 未命名27
  - 未命名30
  - 未命名29
  - 未命名26
  - 未命名25
[OK] 窗口选择成功，共 71 个对象。
第 25 打印区：
  - 未命名38
  - 未命名37
  - 未命名42
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
  - 未命名32
  - 未命名31
  - 未命名30
  - 未命名29
[OK] 窗口选择成功，共 61 个对象。
第 26 打印区：
  - 未命名38
  - 未命名37
  - 未命名45
  - 未命名42
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
  - 未命名34
  - 未命名33
[OK] 窗口选择成功，共 56 个对象。
第 27 打印区：
  - 未命名38
  - 未命名37
  - 未命名45
  - 未命名42
  - 未命名47
  - 未命名46
  - 未命名39
  - 未命名36
  - 未命名35
  - 未命名44
  - 未命名43
  - 未命名41
  - 未命名40
[FALLBACK] 遍历模型空间得到 1 个对象。
第 28 打印区：
  (空)
[错误] 遍历模型空间失败: (-2147418111, '被呼叫方拒绝接收呼叫。', None, None)
第 29 打印区：
  (空)
[OK] 窗口选择成功，共 9 个对象。
第 30 打印区：
  (空)
[OK] 窗口选择成功，共 9 个对象。
第 31 打印区：
  (空)
[OK] 窗口选择成功，共 9 个对象。
第 32 打印区：
  (空)
[OK] 窗口选择成功，共 9 个对象。
第 33 打印区：
  (空)
[OK] 窗口选择成功，共 9 个对象。
第 34 打印区：
  (空)
[OK] 窗口选择成功，共 9 个对象。
第 35 打印区：
  (空)
[OK] 窗口选择成功，共 9 个对象。
第 36 打印区：
  (空)
for i, pl in enumerate(polylines):
    
    # 1. 获取包围盒 (修正了之前的语法错误)
    try:
        min_pt, max_pt = pl.GetBoundingBox()
        x1, y1 = min_pt[0], min_pt[1]
        x2, y2 = max_pt[0], max_pt[1]
    except Exception:
        print(f"第 {i} 打印区：无法获取几何范围，跳过")
        continue

    # [已删除] acad_app.ZoomWindow(...) <-- 视图相关代码已移除

    # 2. 执行选择
    # 注意：select_objects_in_window_area 返回的是区域内的【所有对象】
    lk = select_entities_in_window(x1, y1, x2, y2, max_retry=1) # retry 设为1即可，因为没有zoom，重试也没用

    print(f"第 {i} 打印区：")
    
    found_count = 0
    if lk:
        for xx in lk:
            try:
                # 3. 必须过滤图层！只处理图名
                if xx.Layer == "DIM_SYMB": 
                    name = get_attr(xx, "图名文字")
                    if name is None:
                        name = get_attr(xx, "TextString")
                    
                    if name:
                        print(f"  - {name}")
                        found_count += 1
            except:
                continue
    
    if found_count == 0:
        print("  (空)")

        
Traceback (most recent call last):
  File "<pyshell#78>", line 16, in <module>
    lk = select_entities_in_window(x1, y1, x2, y2, max_retry=1) # retry 设为1即可，因为没有zoom，重试也没用
TypeError: select_entities_in_window() got an unexpected keyword argument 'max_retry'
for i, pl in enumerate(polylines):
    
    # 1. 获取包围盒 (修正了之前的语法错误)
    try:
        min_pt, max_pt = pl.GetBoundingBox()
        x1, y1 = min_pt[0], min_pt[1]
        x2, y2 = max_pt[0], max_pt[1]
    except Exception:
        print(f"第 {i} 打印区：无法获取几何范围，跳过")
        continue

    # [已删除] acad_app.ZoomWindow(...) <-- 视图相关代码已移除

    # 2. 执行选择
    
    lk = select_entities_in_window(x1, y1, x2, y2, ty = 1.0, select_mode = "_W")

    print(f"第 {i} 打印区：")
    
    found_count = 0
    if lk:
        for xx in lk:
            try:
                # 3. 必须过滤图层！只处理图名
                if xx.Layer == "DIM_SYMB": 
                    name = get_attr(xx, "图名文字")
                    if name is None:
                        name = get_attr(xx, "TextString")
                    
                    if name:
...                         print(f"  - {name}")
...                         found_count += 1
...             except:
...                 continue
...     
...     if found_count == 0:
...         print("  (空)")
... 
...         
第 0 打印区：
  - 未命名2
  - 未命名1
第 1 打印区：
  - 未命名4
  - 未命名3
第 2 打印区：
  - 未命名6
  - 未命名5
第 3 打印区：
  - 未命名14
  - 未命名13
第 4 打印区：
  - 未命名18
  - 未命名17
第 5 打印区：
  - 未命名22
  - 未命名21
第 6 打印区：
  - 未命名26
  - 未命名25
第 7 打印区：
  - 未命名30
  - 未命名29
第 8 打印区：
  (空)
第 9 打印区：
  - 未命名36
  - 未命名35
第 10 打印区：
  - 未命名39
第 11 打印区：
  - 未命名42
第 12 打印区：
  - 未命名45
第 13 打印区：
  - 未命名47
  - 未命名46
第 14 打印区：
  - 未命名49
  - 未命名48
第 15 打印区：
  - 未命名51
  - 未命名50
第 16 打印区：
  - 未命名8
  - 未命名7
第 17 打印区：
  - 未命名10
  - 未命名9
第 18 打印区：
  - 未命名12
  - 未命名11
第 19 打印区：
  - 未命名16
  - 未命名15
第 20 打印区：
  - 未命名20
  - 未命名19
第 21 打印区：
  - 未命名24
  - 未命名23
第 22 打印区：
  - 未命名28
  - 未命名27
第 23 打印区：
  - 未命名32
  - 未命名31
第 24 打印区：
  - 未命名34
  - 未命名33
第 25 打印区：
  - 未命名38
  - 未命名37
第 26 打印区：
  - 未命名41
  - 未命名40
第 27 打印区：
  - 未命名44
  - 未命名43
第 28 打印区：
  (空)
第 29 打印区：
  (空)
第 30 打印区：
  (空)
第 31 打印区：
  (空)
第 32 打印区：
  (空)
第 33 打印区：
  (空)
第 34 打印区：
  (空)
第 35 打印区：
  (空)
第 36 打印区：
  (空)

