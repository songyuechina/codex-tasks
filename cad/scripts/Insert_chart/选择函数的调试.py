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
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
2026-01-12 00:43:34 - [INFO] - CAD_coordination.py:51 - ✅ 协同模块已加载 (集成 Licad V2.5+)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
2026-01-12 00:43:35 - [INFO] - CAD_coordination.py:51 - ✅ 协同模块已加载 (集成 Licad V2.5+)
[初始化] 成功加载 licad 核心模块
[初始化] 脚本环境加载完成: CAD_file_operations.py
[成功] licad 核心连接模块已加载 (已建立全局变量桥接)
[成功] CAD协同机制模块已加载
[成功] CAD_selection选择与属性模块已加载
[初始化] CAD_basic 环境加载完成，运行路径: D:\claude-tasks\cad\scripts
__________________  CAD基本操作开始运行 _________________________
2026-01-12 00:43:35 - [INFO] - common_logger.py:41 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=30s
✔ 脚本执行完成。
============================================================

>>> run_full_project_workflow()
⏱ 开始 `run_full_project_workflow` …
2026-01-12 00:43:44 - [INFO] - common_logger.py:170 - 🚩 进入区域: 工程图纸全自动化流水线 [Mode:1|AI]
2026-01-12 00:43:44 - [INFO] - insert_labels.py:1572 - 🚀 启动全流程...
2026-01-12 00:43:44 - [INFO] - common_logger.py:170 - 🚩 进入区域: [总装] 图签全流程 [Mode:1|AI]
2026-01-12 00:43:44 - [INFO] - insert_labels.py:1508 - 
💠 [Phase 1] 启动图签插入与缩放...
⏱ 开始 `insert_and_scale_labels_area_any` …
[licad] 正在尝试连接 CAD COM 接口...

[licad] 连接成功: 图签插入0109.dwg
2026-01-12 00:43:45 - [INFO] - licad.py:365 - [li] 连接已刷新: 图签插入0109.dwg
⏱ 开始 `select_maxrect_polylines_1` …
[OK] 当前图层已设置为：dy_zhuanyong
  第 1 次删除：共删除 2 个对象
2026-01-12 00:43:45 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-12 00:43:47 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
2026-01-12 00:43:48 - [INFO] - CAD_basic.py:18785 - 🧹 [初始化] 已清空图层 dy_zhuanyong
2026-01-12 00:43:48 - [INFO] - CAD_basic.py:18799 - ⚙️ [模式] 自适应模式 (MinSide=100)
2026-01-12 00:43:48 - [INFO] - CAD_basic.py:18807 - 
🔄 --- 开始第 1 次分析循环 ---
[筛选] 待检查多段线总数: 25
[筛选] 最终获得矩形数量: 25
2026-01-12 00:43:48 - [INFO] - CAD_basic.py:18813 - 📍 [步骤1] 原始选择矩形数量: 25 个
2026-01-12 00:43:48 - [INFO] - CAD_basic.py:18831 - 📍 [步骤4] 经模型空间过滤后数量: 25 个 (剔除 0 个非模型对象)
2026-01-12 00:43:48 - [INFO] - CAD_basic.py:18897 - 📍 [步骤2] 发现伪极大矩形数量: 1 个
2026-01-12 00:43:48 - [WARNING] - CAD_basic.py:18902 -    💥 正在炸开伪极大矩形: 18E95
2026-01-12 00:43:48 - [INFO] - CAD_basic.py:18908 - ⏳ 等待炸开生效，准备重新分析...
2026-01-12 00:43:48 - [INFO] - CAD_basic.py:18807 - 
🔄 --- 开始第 2 次分析循环 ---
[筛选] 待检查多段线总数: 24
[筛选] 最终获得矩形数量: 24
2026-01-12 00:43:49 - [INFO] - CAD_basic.py:18813 - 📍 [步骤1] 原始选择矩形数量: 24 个
2026-01-12 00:43:49 - [INFO] - CAD_basic.py:18831 - 📍 [步骤4] 经模型空间过滤后数量: 24 个 (剔除 0 个非模型对象)
2026-01-12 00:43:49 - [INFO] - CAD_basic.py:18897 - 📍 [步骤2] 发现伪极大矩形数量: 0 个
2026-01-12 00:43:49 - [INFO] - CAD_basic.py:18917 - 📍 [步骤3] 真实的极大多段线打印区域数量: 24 个
正在分析 24 个对象进行去重...
✅ 去重完成：处理 24 个，删除 0 个，保留 24 个。
2026-01-12 00:43:49 - [INFO] - CAD_basic.py:18924 - 📍 [步骤5] 去重后的最终多段线数量: 24 个
2026-01-12 00:43:49 - [INFO] - CAD_basic.py:18933 - 🎨 开始重绘 24 个区域...
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
⏱ 完成 `select_maxrect_polylines_1`，耗时：4.570 秒
正在分析 24 个对象进行去重...
✅ 去重完成：处理 23 个，删除 0 个，保留 23 个。
2026-01-12 00:43:49 - [INFO] - insert_labels.py:885 - 📋 [任务锁定] 目标区域: 23 个
2026-01-12 00:43:49 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
[初始化] 成功加载 licad 核心模块
[初始化] 脚本环境加载完成: CAD_file_operations.py
2026-01-12 00:43:50 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-12 00:43:51 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-12 00:43:52 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-12 00:43:52 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-12 00:43:53 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-12 00:43:53 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-12 00:43:54 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-12 00:43:55 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-12 00:43:57 - [INFO] - insert_labels.py:912 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-12 00:43:58 - [INFO] - insert_labels.py:918 - ✅ [状态确认] CAD 已就绪。耗时: 1.04s
2026-01-12 00:43:59 - [INFO] - insert_labels.py:934 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-12 00:43:59 - [INFO] - insert_labels.py:937 - 📋 [实物清单]: ['A0', 'A0_1_4', 'A0_1_8', 'A1', 'A1_1_2', 'A1_1_4', 'A1_3_4', 'A2_1_2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-12 00:43:59 - [INFO] - insert_labels.py:969 - ▶ 开始按信号分发...
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.6667, YScaleFactor 1.0000→1.0000
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0001→1.0000, YScaleFactor 1.0001→1.0000
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0002→1.0000, YScaleFactor 1.0002→1.0000
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 00:43:59 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0003→1.0000, YScaleFactor 1.0003→1.0000
2026-01-12 00:43:59 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-12 00:44:00 - [INFO] - insert_labels.py:999 - ✅ 所有图签处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：15.534 秒
2026-01-12 00:44:00 - [INFO] - insert_labels.py:1524 - 
💤 [Bridge] 等待几何数据落地...
2026-01-12 00:44:02 - [INFO] - insert_labels.py:1530 - 
💠 [Phase 2] 启动核心规范化...
⏱ 开始 `normalize_core_title_blocks_by_layer` …
2026-01-12 00:44:02 - [INFO] - insert_labels.py:1374 - [CoreBlock] 🔄 [Attempt 1/3] 启动事务流程...
2026-01-12 00:44:02 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 核心规范化-第1次
2026-01-12 00:44:03 - [INFO] - insert_labels.py:1374 - [CoreBlock]   锁定目标: 23 个
2026-01-12 00:44:03 - [INFO] - insert_labels.py:1374 - [CoreBlock]   执行批量炸开...
2026-01-12 00:44:03 - [INFO] - insert_labels.py:1374 - [CoreBlock]   等待同步 (1.0s)...
开始筛选，待处理对象总数: 23
筛选完成。在列表中找到的块实例数: 23
开始筛选，待处理对象总数: 23
筛选完成。在列表中找到的块实例数: 0
2026-01-12 00:44:04 - [INFO] - insert_labels.py:1374 - [CoreBlock]   ✅ 本次尝试成功，事务提交。
2026-01-12 00:44:04 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 核心规范化-第1次
⏱ 完成 `normalize_core_title_blocks_by_layer`，耗时：3.093 秒
2026-01-12 00:44:05 - [INFO] - insert_labels.py:1552 - 
✨ 流水线执行完毕。
2026-01-12 00:44:05 - [INFO] - insert_labels.py:1585 - 🎉 全流程圆满结束！
⏱ 完成 `run_full_project_workflow`，耗时：20.642 秒

============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-12 01:39:20 - [INFO] - common_logger.py:41 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=30s
✔ 脚本执行完成。
============================================================

>>> 
============================================================
>>> 正在运行脚本: insert_labels.py
============================================================
2026-01-12 01:40:36 - [INFO] - common_logger.py:41 - 🔧 调试配置更新: Mode=1, Who=AI, Wait=30s
✔ 脚本执行完成。
============================================================

>>> run_full_project_workflow()
⏱ 开始 `run_full_project_workflow` …
2026-01-12 01:40:55 - [INFO] - common_logger.py:170 - 🚩 进入区域: 工程图纸全自动化流水线 [Mode:1|AI]
2026-01-12 01:40:55 - [INFO] - insert_labels.py:1572 - 🚀 启动全流程...
2026-01-12 01:40:55 - [INFO] - common_logger.py:170 - 🚩 进入区域: [总装] 图签全流程 [Mode:1|AI]
2026-01-12 01:40:55 - [INFO] - insert_labels.py:1508 - 
💠 [Phase 1] 启动图签插入与缩放...
⏱ 开始 `insert_and_scale_labels_area_any` …
⏱ 开始 `select_maxrect_polylines_1` …
[OK] 当前图层已设置为：dy_zhuanyong
  第 1 次删除：共删除 2 个对象
2026-01-12 01:40:55 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-12 01:40:57 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[CLEAN] 图层 'dy_zhuanyong' 已清空（共尝试 1 次）
2026-01-12 01:40:58 - [INFO] - CAD_basic.py:18785 - 🧹 [初始化] 已清空图层 dy_zhuanyong
2026-01-12 01:40:58 - [INFO] - CAD_basic.py:18799 - ⚙️ [模式] 自适应模式 (MinSide=100)
2026-01-12 01:40:58 - [INFO] - CAD_basic.py:18807 - 
🔄 --- 开始第 1 次分析循环 ---
[筛选] 待检查多段线总数: 25
[筛选] 最终获得矩形数量: 25
2026-01-12 01:40:58 - [INFO] - CAD_basic.py:18813 - 📍 [步骤1] 原始选择矩形数量: 25 个
2026-01-12 01:40:58 - [INFO] - CAD_basic.py:18831 - 📍 [步骤4] 经模型空间过滤后数量: 25 个 (剔除 0 个非模型对象)
2026-01-12 01:40:58 - [INFO] - CAD_basic.py:18897 - 📍 [步骤2] 发现伪极大矩形数量: 1 个
2026-01-12 01:40:58 - [WARNING] - CAD_basic.py:18902 -    💥 正在炸开伪极大矩形: 18E95
2026-01-12 01:40:58 - [INFO] - CAD_basic.py:18908 - ⏳ 等待炸开生效，准备重新分析...
2026-01-12 01:40:58 - [INFO] - CAD_basic.py:18807 - 
🔄 --- 开始第 2 次分析循环 ---
[筛选] 待检查多段线总数: 24
[筛选] 最终获得矩形数量: 24
2026-01-12 01:40:59 - [INFO] - CAD_basic.py:18813 - 📍 [步骤1] 原始选择矩形数量: 24 个
2026-01-12 01:40:59 - [INFO] - CAD_basic.py:18831 - 📍 [步骤4] 经模型空间过滤后数量: 24 个 (剔除 0 个非模型对象)
2026-01-12 01:40:59 - [INFO] - CAD_basic.py:18897 - 📍 [步骤2] 发现伪极大矩形数量: 0 个
2026-01-12 01:40:59 - [INFO] - CAD_basic.py:18917 - 📍 [步骤3] 真实的极大多段线打印区域数量: 24 个
正在分析 24 个对象进行去重...
✅ 去重完成：处理 24 个，删除 0 个，保留 24 个。
2026-01-12 01:40:59 - [INFO] - CAD_basic.py:18924 - 📍 [步骤5] 去重后的最终多段线数量: 24 个
2026-01-12 01:40:59 - [INFO] - CAD_basic.py:18933 - 🎨 开始重绘 24 个区域...
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
[OK] 已在图层『dy_zhuanyong』绘制多段线，Closed = True
⏱ 完成 `select_maxrect_polylines_1`，耗时：4.055 秒
正在分析 24 个对象进行去重...
✅ 去重完成：处理 24 个，删除 0 个，保留 24 个。
2026-01-12 01:40:59 - [INFO] - insert_labels.py:885 - 📋 [任务锁定] 目标区域: 24 个
2026-01-12 01:40:59 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 一键插图签总成
2026-01-12 01:41:00 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 插入-标准图签.dwg
2026-01-12 01:41:01 - [INFO] - CAD_coordination.py:427 - CMD -> -INSERT
"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg"
0,0,0
1
1
1
0
2026-01-12 01:41:02 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 插入-标准图签.dwg
2026-01-12 01:41:02 - [INFO] - CAD_coordination.py:165 -   🔻 [融合子事务] 炸开-标准图签.dwg
2026-01-12 01:41:03 - [INFO] - CAD_coordination.py:427 - CMD -> EXPLODE
L
2026-01-12 01:41:03 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 炸开-标准图签.dwg
✅ [OK] 已插入并炸开：标准图签.dwg @ (0,0,0)
2026-01-12 01:41:04 - [INFO] - CAD_coordination.py:427 - CMD -> RE
2026-01-12 01:41:05 - [INFO] - CAD_coordination.py:427 - CMD -> Z
E
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-12 01:41:07 - [INFO] - insert_labels.py:912 - ⏳ [探测中] 第 1/3 次锁定 CAD 状态...
2026-01-12 01:41:08 - [INFO] - insert_labels.py:918 - ✅ [状态确认] CAD 已就绪。耗时: 1.05s
2026-01-12 01:41:08 - [WARNING] - CAD_com_utils.py:58 - CAD忙碌 [_to_list] - 0x80010001 - 0.50s后重试 (1/20)
2026-01-12 01:41:09 - [INFO] - insert_labels.py:934 - 🎊 [审计通过] 成功锁定 12 个块名。
2026-01-12 01:41:09 - [INFO] - insert_labels.py:937 - 📋 [实物清单]: ['A0', 'A0_1_4', 'A0_1_8', 'A1', 'A1_1_2', 'A1_1_4', 'A1_3_4', 'A2_1_2', 'A2_1_2', 'A2_1_4', 'A2_3_4', 'A3']
2026-01-12 01:41:09 - [INFO] - insert_labels.py:969 - ▶ 开始按信号分发...
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.6667, YScaleFactor 1.0000→1.0000
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0050, YScaleFactor 1.0000→0.0050
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0054, YScaleFactor 1.0000→0.0075
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_vertical，rot≈90.0°: XScaleFactor 0.0030→0.0027, YScaleFactor 0.0030→0.0027
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0000→0.0093, YScaleFactor 1.0000→0.0097
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0001→1.0000, YScaleFactor 1.0001→1.0000
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 01:41:09 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 01:41:10 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0002→1.0000, YScaleFactor 1.0002→1.0000
2026-01-12 01:41:10 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 01:41:10 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame: 框与图签块尺寸已在容差内，无需校正
2026-01-12 01:41:10 - [INFO] - common_logger.py:202 -   ▶ adjust_block_to_frame 模式=anisotropic_horizontal，rot≈0.0°: XScaleFactor 1.0003→1.0000, YScaleFactor 1.0003→1.0000
2026-01-12 01:41:10 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 一键插图签总成
[保存] 开始保存: 图签插入0109.dwg ...
[成功] COM Save 完成: 图签插入0109.dwg
2026-01-12 01:41:10 - [INFO] - insert_labels.py:999 - ✅ 所有图签处理完成。
⏱ 完成 `insert_and_scale_labels_area_any`，耗时：15.423 秒
2026-01-12 01:41:11 - [INFO] - insert_labels.py:1524 - 
💤 [Bridge] 等待几何数据落地...
2026-01-12 01:41:12 - [INFO] - insert_labels.py:1530 - 
💠 [Phase 2] 启动核心规范化...
⏱ 开始 `normalize_core_title_blocks_by_layer` …
2026-01-12 01:41:12 - [INFO] - insert_labels.py:1374 - [CoreBlock] 🔄 [Attempt 1/3] 启动事务流程...
2026-01-12 01:41:12 - [INFO] - CAD_coordination.py:160 - 🔰 [主事务开始] 核心规范化-第1次
2026-01-12 01:41:13 - [INFO] - insert_labels.py:1374 - [CoreBlock]   锁定目标: 24 个
2026-01-12 01:41:13 - [INFO] - insert_labels.py:1374 - [CoreBlock]   执行批量炸开...
2026-01-12 01:41:13 - [INFO] - insert_labels.py:1374 - [CoreBlock]   等待同步 (1.0s)...
开始筛选，待处理对象总数: 24
筛选完成。在列表中找到的块实例数: 24
开始筛选，待处理对象总数: 24
筛选完成。在列表中找到的块实例数: 0
2026-01-12 01:41:15 - [INFO] - insert_labels.py:1374 - [CoreBlock]   ✅ 本次尝试成功，事务提交。
2026-01-12 01:41:15 - [INFO] - CAD_coordination.py:236 - ✅ 完成: 核心规范化-第1次
⏱ 完成 `normalize_core_title_blocks_by_layer`，耗时：3.115 秒
2026-01-12 01:41:15 - [INFO] - insert_labels.py:1552 - 
✨ 流水线执行完毕。
2026-01-12 01:41:16 - [INFO] - insert_labels.py:1585 - 🎉 全流程圆满结束！
⏱ 完成 `run_full_project_workflow`，耗时：20.516 秒
