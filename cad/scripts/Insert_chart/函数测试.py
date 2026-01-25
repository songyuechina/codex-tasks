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
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 02:35:38 - [INFO] - CAD_coordination.py:51 - ✅ 协同模块已加载 (集成 Licad V2.5+)
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
2026-01-11 02:35:38 - [INFO] - CAD_coordination.py:51 - ✅ 协同模块已加载 (集成 Licad V2.5+)
[初始化] 成功加载 licad 核心模块
[初始化] 脚本环境加载完成: CAD_file_operations.py
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
2026-01-11 02:35:38 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[licad] 正在尝试连接 CAD COM 接口...

[licad] 连接成功: 图签插入0109.dwg
2026-01-11 02:39:36 - [INFO] - licad.py:365 - [li] 连接已刷新: 图签插入0109.dwg
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 02:39:36 - [INFO] - insert_labels.py:657 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 02:39:36 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 02:39:37 - [INFO] - insert_labels.py:670 - ⏳ 正在导入模板...
[初始化] 成功加载 licad 核心模块
[初始化] 脚本环境加载完成: CAD_file_operations.py
2026-01-11 02:39:37 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 02:39:38 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 02:39:39 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 02:39:39 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 02:39:40 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 02:39:40 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 02:39:41 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 02:39:43 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 02:39:45 - [INFO] - insert_labels.py:684 - ⏳ [同步] 第 1/3 次等待数据库刷新 (3.0s)...
2026-01-11 02:39:48 - [INFO] - insert_labels.py:713 - 🧐 [审计报告] 预期: 12 | 实测: 0 | 匹配名单: []
2026-01-11 02:39:48 - [WARNING] - insert_labels.py:721 - ⚠️ [同步未完] 仍缺失 12 个: ['A0', 'A0_1_4', 'A0_1_8', 'A1', 'A1_1_2', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 02:39:48 - [WARNING] - insert_labels.py:722 -    -> 可能是 CAD 反应慢，准备延长等待至 6.0s...
2026-01-11 02:39:48 - [INFO] - insert_labels.py:684 - ⏳ [同步] 第 2/3 次等待数据库刷新 (6.0s)...
[licad] 正在尝试连接 CAD COM 接口...

[licad] 连接成功: 图签插入0109.dwg
2026-01-11 02:39:55 - [INFO] - licad.py:365 - [li] 连接已刷新: 图签插入0109.dwg
2026-01-11 02:39:55 - [INFO] - insert_labels.py:713 - 🧐 [审计报告] 预期: 12 | 实测: 0 | 匹配名单: []
2026-01-11 02:39:55 - [WARNING] - insert_labels.py:721 - ⚠️ [同步未完] 仍缺失 12 个: ['A0', 'A0_1_4', 'A0_1_8', 'A1', 'A1_1_2', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 02:39:55 - [WARNING] - insert_labels.py:722 -    -> 可能是 CAD 反应慢，准备延长等待至 9.0s...
2026-01-11 02:39:55 - [INFO] - insert_labels.py:684 - ⏳ [同步] 第 3/3 次等待数据库刷新 (9.0s)...
2026-01-11 02:40:04 - [INFO] - insert_labels.py:713 - 🧐 [审计报告] 预期: 12 | 实测: 0 | 匹配名单: []
2026-01-11 02:40:04 - [WARNING] - insert_labels.py:721 - ⚠️ [同步未完] 仍缺失 12 个: ['A0', 'A0_1_4', 'A0_1_8', 'A1', 'A1_1_2', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 02:40:04 - [WARNING] - insert_labels.py:722 -    -> 可能是 CAD 反应慢，准备延长等待至 12.0s...
2026-01-11 02:40:04 - [ERROR] - insert_labels.py:730 - ❌ [严重超时] 尝试 3 次后，仍未能捕捉到完整的 12 个标准块。操作已终止并回滚。
2026-01-11 02:40:04 - [ERROR] - CAD_coordination.py:205 - ❌ 事务异常: 一键插图签总成 (❌ [严重超时] 尝试 3 次后，仍未能捕捉到完整的 12 个标准块。操作已终止并回滚。)
2026-01-11 02:40:04 - [WARNING] - CAD_coordination.py:217 - 🔄 正在回滚局部事务: 一键插图签总成
2026-01-11 02:40:04 - [INFO] - CAD_coordination.py:427 - CMD -> _U
Traceback (most recent call last):
  File "<pyshell#0>", line 1, in <module>
    insert_and_scale_labels_area_any(
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 801, in wrapper
    result = func(*args, **kwargs)
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 609, in wrapper
    return func(*args, **kw)
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 731, in insert_and_scale_labels_area_any
RuntimeError: ❌ [严重超时] 尝试 3 次后，仍未能捕捉到完整的 12 个标准块。操作已终止并回滚。

============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
✗ 执行出错: insert_labels.py
Traceback (most recent call last):
  File "D:\claude-tasks\cad\scripts\IDLE_bootstrap.py", line 45, in run_script_in_main
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 567
    EXPECTED_BLOCK_NAMES = [
    ^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax
============================================================

>>> 
============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
✗ 执行出错: insert_labels.py
Traceback (most recent call last):
  File "D:\claude-tasks\cad\scripts\IDLE_bootstrap.py", line 45, in run_script_in_main
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 567
    EXPECTED_BLOCK_NAMES = [
    ^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax
============================================================

>>> 
============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 02:51:40 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
    
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 02:52:15 - [INFO] - insert_labels.py:625 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 02:52:15 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 02:52:16 - [INFO] - insert_labels.py:638 - ⏳ 正在导入模板...
2026-01-11 02:52:16 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 02:52:16 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 02:52:17 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 02:52:17 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 02:52:18 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 02:52:19 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 02:52:19 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 02:52:21 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 02:52:24 - [INFO] - insert_labels.py:648 - ⏳ [同步] 等待数据落盘 (1.0s)...
2026-01-11 02:52:25 - [INFO] - insert_labels.py:660 - 🔍 [直连审计] 正在倒序扫描 ModelSpace 最后 38 个对象...
2026-01-11 02:52:25 - [INFO] - insert_labels.py:679 - 🧐 [审计报告] 匹配: 0/12 | 名单: []
2026-01-11 02:52:25 - [ERROR] - insert_labels.py:686 - ❌ [严重缺失] 依然缺失: {'A2', 'A3', 'A1_1_4', 'A2_3_4', 'A2_1_2', 'A1_1_2', 'A1_3_4', 'A0_1_4', 'A2_1_4', 'A1', 'A0_1_8', 'A0'}
2026-01-11 02:52:25 - [INFO] - insert_labels.py:688 - ❓ [现场发现] 找到的其他块: set()
2026-01-11 02:52:25 - [ERROR] - CAD_coordination.py:205 - ❌ 事务异常: 一键插图签总成 (无法在模型空间末尾找到预期的 12 个标准块，操作中止。)
2026-01-11 02:52:25 - [WARNING] - CAD_coordination.py:217 - 🔄 正在回滚局部事务: 一键插图签总成
2026-01-11 02:52:25 - [INFO] - CAD_coordination.py:427 - CMD -> _U
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    insert_and_scale_labels_area_any(
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 801, in wrapper
    result = func(*args, **kwargs)
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 609, in wrapper
    return func(*args, **kw)
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 695, in insert_and_scale_labels_area_any
    raise RuntimeError("无法在模型空间末尾找到预期的 12 个标准块，操作中止。")
RuntimeError: 无法在模型空间末尾找到预期的 12 个标准块，操作中止。

============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 02:56:58 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 02:57:10 - [INFO] - insert_labels.py:627 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 02:57:10 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 02:57:11 - [INFO] - insert_labels.py:640 - ⏳ 正在导入模板...
2026-01-11 02:57:11 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 02:57:12 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 02:57:13 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 02:57:13 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 02:57:14 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 02:57:14 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 02:57:15 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 02:57:16 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 02:57:19 - [INFO] - insert_labels.py:648 - ⏳ [指令执行] 强制等待 6 秒，确保数据落地...
2026-01-11 02:57:25 - [INFO] - insert_labels.py:653 - ⏳ [系统探路] 正在检测 CAD 是否静默 (wait_quiescent)...
2026-01-11 02:57:26 - [INFO] - insert_labels.py:655 - ✅ CAD 已就绪。
2026-01-11 02:57:26 - [INFO] - insert_labels.py:665 - 🔍 [全局扫描] 正在执行 select_kuai()...
2026-01-11 02:57:26 - [INFO] - insert_labels.py:685 - 🧐 [审计报告] 匹配: 0/12 | 名单: []
2026-01-11 02:57:26 - [ERROR] - insert_labels.py:689 - ❌ [资源缺失] 仍缺失 12 个: ['A0', 'A0_1_4', 'A0_1_8', 'A1', 'A1_1_2', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 02:57:26 - [INFO] - insert_labels.py:693 - 🔎 [现场实况] 当前图纸里的名字示例: ['A2_100550', 'A1_3_4_100550', 'A0_1_8_100550', 'A0_100550', 'A1_1_2_100550', 'A1_1_4_100550', 'A2_1_4_100550', 'A2_1_2_100550', 'A3_100550', 'A1_100550', 'A0_1_4_100550', 'A2_3_4_100550']
2026-01-11 02:57:26 - [ERROR] - insert_labels.py:702 - 扫描过程出错: 炸开后无法捕捉到标准的 12 个图块，可能是名字变异或匿名化。
2026-01-11 02:57:26 - [ERROR] - CAD_coordination.py:205 - ❌ 事务异常: 一键插图签总成 (炸开后无法捕捉到标准的 12 个图块，可能是名字变异或匿名化。)
2026-01-11 02:57:26 - [WARNING] - CAD_coordination.py:217 - 🔄 正在回滚局部事务: 一键插图签总成
2026-01-11 02:57:27 - [INFO] - CAD_coordination.py:427 - CMD -> _U
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    insert_and_scale_labels_area_any(
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 801, in wrapper
    result = func(*args, **kwargs)
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 609, in wrapper
    return func(*args, **kw)
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 703, in insert_and_scale_labels_area_any
    raise e # 必须抛出，触发 CADGuard 回滚
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 695, in insert_and_scale_labels_area_any
    raise RuntimeError("炸开后无法捕捉到标准的 12 个图块，可能是名字变异或匿名化。")
RuntimeError: 炸开后无法捕捉到标准的 12 个图块，可能是名字变异或匿名化。

============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 03:01:23 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 12
正在分析 12 个对象进行去重...
✅ 去重完成：处理 12 个，删除 0 个，保留 12 个。
2026-01-11 03:02:06 - [INFO] - insert_labels.py:628 - 📋 [任务锁定] 目标区域: 12 个
2026-01-11 03:02:06 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 03:02:06 - [INFO] - insert_labels.py:641 - ⏳ 正在导入模板...
2026-01-11 03:02:06 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 03:02:07 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 03:02:08 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 03:02:08 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 03:02:09 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 03:02:10 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 03:02:10 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 03:02:12 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:02:14 - [INFO] - insert_labels.py:645 - ⏳ [指令执行] 强制等待 6 秒，让数据库飞一会儿...
2026-01-11 03:02:20 - [INFO] - insert_labels.py:657 - 🔍 [全局扫描] 正在构建图块名称映射表...
2026-01-11 03:02:21 - [ERROR] - insert_labels.py:697 - 扫描映射过程出错: name 'EXPECTED_PREFIXES' is not defined
2026-01-11 03:02:21 - [ERROR] - CAD_coordination.py:205 - ❌ 事务异常: 一键插图签总成 (name 'EXPECTED_PREFIXES' is not defined)
2026-01-11 03:02:21 - [WARNING] - CAD_coordination.py:217 - 🔄 正在回滚局部事务: 一键插图签总成
2026-01-11 03:02:21 - [INFO] - CAD_coordination.py:427 - CMD -> _U
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    insert_and_scale_labels_area_any(
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 801, in wrapper
    result = func(*args, **kwargs)
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 609, in wrapper
    return func(*args, **kw)
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 698, in insert_and_scale_labels_area_any
    raise e
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 669, in insert_and_scale_labels_area_any
    for std_name in EXPECTED_PREFIXES:
NameError: name 'EXPECTED_PREFIXES' is not defined

============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 03:05:00 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
2026-01-11 03:05:16 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [_to_list] - 0x80010001 - 0.50s后重试 (1/20)
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 03:05:17 - [INFO] - insert_labels.py:627 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 03:05:17 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 03:05:17 - [INFO] - insert_labels.py:640 - ⏳ 正在导入模板...
2026-01-11 03:05:17 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 03:05:18 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 03:05:19 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 03:05:19 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 03:05:20 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 03:05:20 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 03:05:21 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 03:05:23 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:05:25 - [INFO] - insert_labels.py:644 - ⏳ [指令执行] 强制等待 6 秒，让数据库飞一会儿...
2026-01-11 03:05:31 - [INFO] - insert_labels.py:656 - 🔍 [全局扫描] 正在构建图块名称映射表...
2026-01-11 03:05:31 - [INFO] - insert_labels.py:685 - 🧐 [映射报告] 成功映射: 12/12
2026-01-11 03:05:31 - [INFO] - insert_labels.py:693 - ✅ [映射就绪] 示例: A3 -> A3_100550
2026-01-11 03:05:31 - [INFO] - insert_labels.py:702 - ▶ 开始分发图签...
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.5714, YScaleFactor 1.0000→1.0000
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:05:32 - [WARNING] - insert_labels.py:712 - ⚠️ 跳过: 规格 A0+1/8 没有对应的块定义
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:05:32 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:05:32 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:05:33 - [INFO] - insert_labels.py:738 - ✅ 所有图签处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：16.759 秒


============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 03:28:22 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
2026-01-11 03:29:02 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 03:29:02 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 03:29:03 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 03:29:04 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 03:29:04 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 03:29:05 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 03:29:06 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 03:29:06 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 03:29:08 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:29:10 - [INFO] - insert_labels.py:601 - ⏳ [核心等待] 强制等待 6s 同步数据库...
2026-01-11 03:29:16 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [ss_select] - 0x80010001 - 0.50s后重试 (1/10)
2026-01-11 03:29:17 - [INFO] - insert_labels.py:622 - 🧐 [审计报告] 预期 12 个，实测匹配到 12 个。
2026-01-11 03:29:17 - [INFO] - insert_labels.py:630 - ▶ 开始按信号分发...
2026-01-11 03:29:17 - [ERROR] - CAD_coordination.py:205 - ❌ 事务异常: 一键插图签总成 (name 'valid_ents' is not defined)
2026-01-11 03:29:17 - [WARNING] - CAD_coordination.py:217 - 🔄 正在回滚局部事务: 一键插图签总成
2026-01-11 03:29:17 - [INFO] - CAD_coordination.py:427 - CMD -> _U
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    insert_and_scale_labels_area_any(
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 801, in wrapper
    result = func(*args, **kwargs)
  File "D:\claude-tasks\cad\scripts\CAD_basic.py", line 609, in wrapper
    return func(*args, **kw)
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 632, in insert_and_scale_labels_area_any
    for seq, ob in enumerate(valid_ents, 1):
NameError: name 'valid_ents' is not defined

============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 03:30:35 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
2026-01-11 03:30:57 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [_to_list] - 0x80010001 - 0.50s后重试 (1/20)
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 03:30:57 - [INFO] - insert_labels.py:625 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 03:30:57 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 03:30:58 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 03:30:59 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 03:31:00 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 03:31:00 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 03:31:00 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 03:31:01 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 03:31:02 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 03:31:03 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:31:06 - [INFO] - insert_labels.py:639 - ⏳ [核心等待] 强制等待 6s 同步数据库...
2026-01-11 03:31:12 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [ss_select] - 0x80010001 - 0.50s后重试 (1/10)
2026-01-11 03:31:13 - [INFO] - insert_labels.py:656 - 🧐 [审计报告] 预期 12 个，实测匹配到 12 个。
2026-01-11 03:31:13 - [INFO] - insert_labels.py:663 - ▶ 开始按信号分发...
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.5714, YScaleFactor 1.0000→1.0000
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:31:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:31:13 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:31:14 - [INFO] - insert_labels.py:696 - ✅ 所有图签处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：17.133 秒


============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 03:34:59 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 03:35:31 - [INFO] - insert_labels.py:625 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 03:35:31 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 03:35:31 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 03:35:32 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 03:35:33 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 03:35:33 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 03:35:34 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 03:35:35 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 03:35:35 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [_to_list] - 0x80010001 - 0.50s后重试 (1/20)
2026-01-11 03:35:36 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 03:35:38 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:35:40 - [INFO] - insert_labels.py:639 - ⏳ [核心等待] 强制等待 6s 同步数据库...
2026-01-11 03:35:46 - [INFO] - insert_labels.py:661 - 📋 [实物清单] 现场锁定块名: ['A0_1_4_100550', 'A0_1_4_100550', 'A0_1_8_100550', 'A1_1_2_100550', 'A1_1_4_100550', 'A1_3_4_100550', 'A1_3_4_100550', 'A2_1_2_100550', 'A2_1_4_100550', 'A2_3_4_100550', 'A2_3_4_100550', 'A3_100550']
2026-01-11 03:35:46 - [INFO] - insert_labels.py:663 - 🧐 [审计报告] 预期 12 个，实测匹配到 12 个。
2026-01-11 03:35:46 - [INFO] - insert_labels.py:672 - ▶ 开始按信号分发...
2026-01-11 03:35:46 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.5714, YScaleFactor 1.0000→1.0000
2026-01-11 03:35:46 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 03:35:46 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:35:46 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:35:46 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 03:35:47 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:35:47 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 03:35:47 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:35:47 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:35:47 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:35:47 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:35:47 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:35:47 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:35:47 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:35:48 - [INFO] - insert_labels.py:705 - ✅ 所有图签处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：16.786 秒

#上面是按固定等待6秒进行的测试。下面是使用wait_quiescent(min_quiet=1.0, timeout=12)

============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 03:57:57 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 03:58:24 - [INFO] - insert_labels.py:625 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 03:58:24 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 03:58:24 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 03:58:25 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 03:58:26 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 03:58:26 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 03:58:27 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 03:58:28 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 03:58:28 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 03:58:30 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:58:32 - [INFO] - insert_labels.py:642 - ⏳ [系统同步] 模板已炸开，正在探测 CAD 数据库自然静默时间...
2026-01-11 03:58:33 - [INFO] - insert_labels.py:650 - ✅ [同步达成] CAD 已就绪。本次自然同步耗时: 1.04s
2026-01-11 03:58:34 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [_to_list] - 0x80010001 - 0.50s后重试 (1/20)
2026-01-11 03:58:34 - [INFO] - insert_labels.py:675 - 📋 [实物清单] 现场锁定块名: ['A0_1_4_100550', 'A0_1_4_100550', 'A0_1_8_100550', 'A1_1_2_100550', 'A1_1_4_100550', 'A1_3_4_100550', 'A1_3_4_100550', 'A2_1_2_100550', 'A2_1_4_100550', 'A2_3_4_100550', 'A2_3_4_100550', 'A3_100550']
2026-01-11 03:58:34 - [INFO] - insert_labels.py:677 - 🧐 [审计报告] 预期 12 个，实测匹配到 12 个。
2026-01-11 03:58:34 - [INFO] - insert_labels.py:686 - ▶ 开始按信号分发...
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.5714, YScaleFactor 1.0000→1.0000
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:58:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 03:58:34 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 03:58:35 - [INFO] - insert_labels.py:719 - ✅ 所有图签处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：11.837 秒


============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
✗ 执行出错: insert_labels.py
Traceback (most recent call last):
  File "D:\claude-tasks\cad\scripts\IDLE_bootstrap.py", line 45, in run_script_in_main
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 635
    real_live_map = {}
IndentationError: unexpected indent
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 04:17:52 - [INFO] - insert_labels.py:625 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 04:17:52 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 04:17:53 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 04:17:54 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 04:17:55 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 04:17:55 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 04:17:56 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 04:17:56 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 04:17:57 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 04:17:59 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 04:18:01 - [INFO] - insert_labels.py:642 - ⏳ [系统同步] 模板已炸开，正在探测 CAD 数据库自然静默时间...
2026-01-11 04:18:02 - [INFO] - insert_labels.py:650 - ✅ [同步达成] CAD 已就绪。本次自然同步耗时: 1.05s
2026-01-11 04:18:02 - [INFO] - insert_labels.py:675 - 📋 [实物清单] 现场锁定块名: ['A0_1_4_100550', 'A0_1_4_100550', 'A0_1_8_100550', 'A1_1_2_100550', 'A1_1_4_100550', 'A1_3_4_100550', 'A1_3_4_100550', 'A2_1_2_100550', 'A2_1_4_100550', 'A2_3_4_100550', 'A2_3_4_100550', 'A3_100550']
2026-01-11 04:18:03 - [INFO] - insert_labels.py:677 - 🧐 [审计报告] 预期 12 个，实测匹配到 12 个。
2026-01-11 04:18:03 - [INFO] - insert_labels.py:686 - ▶ 开始按信号分发...
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.5714, YScaleFactor 1.0000→1.0000
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:18:03 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:18:03 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 04:18:04 - [INFO] - insert_labels.py:719 - ✅ 所有图签处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：11.485 秒

jc()
1

============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 04:42:24 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
确认版本
[licad] 正在尝试连接 CAD COM 接口...

[licad] 连接成功: 图签插入0109.dwg
2026-01-11 04:42:38 - [INFO] - licad.py:365 - [li] 连接已刷新: 图签插入0109.dwg
2026-01-11 04:42:38 - [ERROR] - CAD_com_utils.py:76 - 脚本运行时错误 [_to_list]: This object does not support enumeration
2026-01-11 04:42:38 - [ERROR] - CAD_com_utils.py:140 - SafeCOM: 转换选择集失败
[筛选] 待检查多段线总数: 0
[筛选] 最终获得矩形数量: 0
2026-01-11 04:42:38 - [WARNING] - insert_labels.py:576 - ⚠️ 未找到任何矩形多段线。
2026-01-11 04:42:38 - [WARNING] - insert_labels.py:701 - ⚠️ 登记失败: [Errno 13] Permission denied: 'D:/claude-tasks/cad/tests/testfunc.xlsx'
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：0.138 秒
{}

============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
✗ 执行出错: insert_labels.py
Traceback (most recent call last):
  File "D:\claude-tasks\cad\scripts\IDLE_bootstrap.py", line 45, in run_script_in_main
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 636
    real_live_map = {}
IndentationError: unexpected indent
============================================================

>>> 
============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
✗ 执行出错: insert_labels.py
Traceback (most recent call last):
  File "D:\claude-tasks\cad\scripts\IDLE_bootstrap.py", line 45, in run_script_in_main
  File "D:/claude-tasks/cad/scripts/Insert_chart/insert_labels.py", line 636
    real_live_map = {}
IndentationError: unexpected indent
============================================================

>>> 
============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 04:47:47 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 04:48:08 - [INFO] - insert_labels.py:591 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 04:48:08 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 04:48:08 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 04:48:09 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 04:48:10 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 04:48:10 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 04:48:11 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 04:48:12 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 04:48:12 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 04:48:14 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 04:48:17 - [INFO] - insert_labels.py:613 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-11 04:48:18 - [INFO] - insert_labels.py:619 - ✅ [状态确认] CAD 已就绪。探测耗时: 1.04s
2026-01-11 04:48:18 - [INFO] - insert_labels.py:635 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-11 04:48:18 - [INFO] - insert_labels.py:649 - ▶ 开始按信号分发...
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:48:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:48:18 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 04:48:19 - [INFO] - insert_labels.py:672 - ✅ 处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：11.578 秒


============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 04:50:40 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
2026-01-11 04:52:18 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [_to_list] - 0x80010001 - 0.50s后重试 (1/20)
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 04:52:19 - [INFO] - insert_labels.py:737 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 04:52:19 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 04:52:19 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 04:52:20 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 04:52:21 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 04:52:21 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 04:52:22 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 04:52:23 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 04:52:23 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 04:52:25 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 04:52:28 - [INFO] - insert_labels.py:758 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-11 04:52:29 - [INFO] - insert_labels.py:764 - ✅ [状态确认] CAD 已就绪。探测耗时: 1.04s
2026-01-11 04:52:29 - [INFO] - insert_labels.py:780 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-11 04:52:29 - [INFO] - insert_labels.py:784 - 📋 [实物清单] 现场锁定块名: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 04:52:29 - [INFO] - insert_labels.py:798 - ▶ 开始按信号分发...
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:52:29 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:52:29 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
2026-01-11 04:52:30 - [WARNING] - insert_labels.py:859 - ⚠️ 登记失败: [Errno 13] Permission denied: 'D:/claude-tasks/cad/tests/testfunc.xlsx'
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 04:52:30 - [INFO] - insert_labels.py:862 - ✅ 处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：11.801 秒

insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 04:56:02 - [INFO] - insert_labels.py:737 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 04:56:02 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 04:56:03 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 04:56:04 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 04:56:05 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 04:56:05 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 04:56:06 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 04:56:06 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 04:56:07 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 04:56:09 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 04:56:11 - [INFO] - insert_labels.py:758 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-11 04:56:12 - [INFO] - insert_labels.py:764 - ✅ [状态确认] CAD 已就绪。探测耗时: 1.03s
2026-01-11 04:56:12 - [INFO] - insert_labels.py:780 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-11 04:56:12 - [INFO] - insert_labels.py:784 - 📋 [实物清单] 现场锁定块名: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 04:56:12 - [INFO] - insert_labels.py:798 - ▶ 开始按信号分发...
2026-01-11 04:56:12 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 04:56:12 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 04:56:12 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:56:12 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:56:12 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 04:56:12 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:56:12 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 04:56:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:56:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:56:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:56:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:56:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:56:13 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 04:56:13 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
2026-01-11 04:56:13 - [INFO] - insert_labels.py:857 - 📊 记录仪: 结果已自动登记至 Excel (状态: PASS)
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 04:56:14 - [INFO] - insert_labels.py:862 - ✅ 处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：11.329 秒

insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 24
[筛选] 最终获得矩形数量: 24
正在分析 24 个对象进行去重...
✅ 去重完成：处理 24 个，删除 0 个，保留 24 个。
2026-01-11 05:01:15 - [INFO] - insert_labels.py:737 - 📋 [任务锁定] 目标区域: 24 个
2026-01-11 05:01:15 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 05:01:16 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 05:01:17 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 05:01:18 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 05:01:18 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 05:01:19 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 05:01:19 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 05:01:20 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 05:01:22 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 05:01:24 - [INFO] - insert_labels.py:758 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-11 05:01:25 - [INFO] - insert_labels.py:764 - ✅ [状态确认] CAD 已就绪。探测耗时: 1.04s
2026-01-11 05:01:25 - [INFO] - insert_labels.py:780 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-11 05:01:25 - [INFO] - insert_labels.py:784 - 📋 [实物清单] 现场锁定块名: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 05:01:25 - [INFO] - insert_labels.py:798 - ▶ 开始按信号分发...
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8001, YScaleFactor 1.0000→1.0000
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:01:25 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0001→1.0000, YScaleFactor 1.0001→1.0000
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0002→1.0000, YScaleFactor 1.0002→1.0000
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-11 05:01:26 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0003→1.0000, YScaleFactor 1.0003→1.0000
2026-01-11 05:01:26 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
2026-01-11 05:01:26 - [WARNING] - insert_labels.py:859 - ⚠️ 登记失败: [Errno 13] Permission denied: 'D:/claude-tasks/cad/tests/testfunc.xlsx'
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 05:01:27 - [INFO] - insert_labels.py:862 - ✅ 处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：11.516 秒


============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 05:02:56 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 05:03:23 - [INFO] - insert_labels.py:737 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 05:03:23 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 05:03:24 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 05:03:25 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 05:03:26 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 05:03:26 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 05:03:26 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 05:03:27 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 05:03:28 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 05:03:29 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 05:03:32 - [INFO] - insert_labels.py:758 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-11 05:03:33 - [INFO] - insert_labels.py:764 - ✅ [状态确认] CAD 已就绪。探测耗时: 1.04s
2026-01-11 05:03:33 - [INFO] - insert_labels.py:780 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-11 05:03:33 - [INFO] - insert_labels.py:784 - 📋 [实物清单] 现场锁定块名: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 05:03:33 - [INFO] - insert_labels.py:798 - ▶ 开始按信号分发...
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:03:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:03:33 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
2026-01-11 05:03:34 - [WARNING] - insert_labels.py:889 - ⚠️ 登记异常: module 'datetime' has no attribute 'now'
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：10.856 秒


============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 05:06:10 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 05:06:56 - [INFO] - insert_labels.py:737 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 05:06:56 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 05:06:57 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 05:06:58 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 05:06:59 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 05:06:59 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 05:07:00 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 05:07:00 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 05:07:01 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 05:07:03 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 05:07:05 - [INFO] - insert_labels.py:758 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-11 05:07:06 - [INFO] - insert_labels.py:764 - ✅ [状态确认] CAD 已就绪。探测耗时: 1.04s
2026-01-11 05:07:06 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [ss_select] - 0x80010001 - 0.50s后重试 (1/10)
2026-01-11 05:07:07 - [INFO] - insert_labels.py:780 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-11 05:07:07 - [INFO] - insert_labels.py:784 - 📋 [实物清单] 现场锁定块名: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 05:07:07 - [INFO] - insert_labels.py:798 - ▶ 开始按信号分发...
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:07:07 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:07:07 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
2026-01-11 05:07:08 - [INFO] - insert_labels.py:863 - 📊 记录仪: 结果已成功登记至 Excel。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：11.412 秒


============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 05:09:59 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 05:10:33 - [INFO] - insert_labels.py:737 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 05:10:33 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 05:10:34 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 05:10:35 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 05:10:36 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 05:10:36 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 05:10:36 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 05:10:37 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 05:10:38 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 05:10:39 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 05:10:42 - [INFO] - insert_labels.py:758 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-11 05:10:43 - [INFO] - insert_labels.py:764 - ✅ [状态确认] CAD 已就绪。探测耗时: 1.04s
2026-01-11 05:10:43 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [_to_list] - 0x80010001 - 0.50s后重试 (1/20)
2026-01-11 05:10:44 - [INFO] - insert_labels.py:780 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-11 05:10:44 - [INFO] - insert_labels.py:784 - 📋 [实物清单] 现场锁定块名: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 05:10:44 - [INFO] - insert_labels.py:798 - ▶ 开始按信号分发...
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:10:44 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:10:44 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
2026-01-11 05:10:44 - [WARNING] - insert_labels.py:873 - ⚠️ 登记异常: [Errno 13] Permission denied: 'D:/claude-tasks/cad/tests/testfunc.xlsx'
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：11.409 秒

insert_and_scale_labels_area_any(
        coms_dayin=None,        
        filepath=str(userpath/"dwg文件/标准图签.dwg"),
    )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 05:11:23 - [INFO] - insert_labels.py:737 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 05:11:23 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 05:11:24 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 05:11:25 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 05:11:26 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 05:11:26 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 05:11:27 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 05:11:27 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 05:11:28 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 05:11:30 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 05:11:32 - [INFO] - insert_labels.py:758 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-11 05:11:33 - [INFO] - insert_labels.py:764 - ✅ [状态确认] CAD 已就绪。探测耗时: 1.03s
2026-01-11 05:11:33 - [INFO] - insert_labels.py:780 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-11 05:11:33 - [INFO] - insert_labels.py:784 - 📋 [实物清单] 现场锁定块名: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 05:11:33 - [INFO] - insert_labels.py:798 - ▶ 开始按信号分发...
2026-01-11 05:11:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 05:11:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 05:11:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:11:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:11:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 05:11:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:11:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 05:11:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:11:33 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:11:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:11:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:11:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:11:34 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:11:34 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
2026-01-11 05:11:34 - [INFO] - insert_labels.py:870 - 📊 记录仪: 结果已成功登记 (标题检查完成)。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：10.926 秒


============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-11 05:13:33 - [INFO] - common_logger.py:55 - 🔧 调试配置更新: 模式=1, 对象=AI, 等待=30s
✔ 脚本执行完成。
============================================================

>>> insert_and_scale_labels_area_any(
...         coms_dayin=None,        
...         filepath=str(userpath/"dwg文件/标准图签.dwg"),
...     )
⏱ 开始 `insert_and_scale_labels_area_any` …
[筛选] 待检查多段线总数: 13
[筛选] 最终获得矩形数量: 13
正在分析 13 个对象进行去重...
✅ 去重完成：处理 13 个，删除 0 个，保留 13 个。
2026-01-11 05:14:08 - [INFO] - insert_labels.py:737 - 📋 [任务锁定] 目标区域: 13 个
2026-01-11 05:14:08 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-11 05:14:08 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-11 05:14:09 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-11 05:14:10 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-11 05:14:10 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-11 05:14:11 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-11 05:14:12 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-11 05:14:12 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-11 05:14:14 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-11 05:14:16 - [INFO] - insert_labels.py:758 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-11 05:14:17 - [INFO] - insert_labels.py:764 - ✅ [状态确认] CAD 已就绪。探测耗时: 1.03s
2026-01-11 05:14:18 - [INFO] - insert_labels.py:780 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-11 05:14:18 - [INFO] - insert_labels.py:784 - 📋 [实物清单] 现场锁定块名: ['A0_1_4', 'A0_1_4', 'A0_1_8', 'A1_1_2', 'A1_1_4', 'A1_1_4', 'A1_3_4', 'A2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-11 05:14:18 - [INFO] - insert_labels.py:798 - ▶ 开始按信号分发...
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.8000, YScaleFactor 1.0000→1.0000
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:14:18 - [INFO] - common_logger.py:243 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-11 05:14:18 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
2026-01-11 05:14:18 - [INFO] - insert_labels.py:875 - 📊 记录仪: 结果已成功登记 (标题强制校验完成)。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：11.016 秒

