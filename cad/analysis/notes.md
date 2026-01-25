# CAD Python 脚本分析记录

本文件用于持续记录对 `cad/` 下 Python 脚本的理解与分析，便于跨会话持续推进。

## 范围
- 目录：`cad/`
- 文件数：56（见 `cad/analysis/index.csv`）

## 索引文件
- `cad/analysis/index.csv`：每个 .py 的行数与大小
- `cad/analysis/imports.csv`：导入关系（AST 扫描）
- `cad/analysis/symbols.csv`：顶层函数/类清单（AST 扫描）

## 优先级（按行数排序 Top 20）

```
行数   文件
 29454  scripts/CAD_basic.py
  4830  library/cad_geometry.py
  4371  library/cad_blocks.py
  4361  scripts/选择测试错误.py
  3700  scripts/CAD_file_operations.py
  3358  library/cad_control.py
  2633  library/cad_objects.py
  2335  system/CAD_core.py
  1911  scripts/Insert_chart/insert_labels.py
  1629  scripts/函数编写规范.py
  1532  library/tarch_building.py
  1273  scripts/CAD_System_Queue.py
  1272  scripts/脚本导航14版.py
  1264  scripts/Insert_chart/函数测试.py
  1087  scripts/CAD_System_Queue - V31.py
  1081  system/CAD_basic_operations.py
  1078  scripts/CAD_System_Queue - V33.py
  1036  scripts/CAD_System_Queue - V30.py
  1006  system/CAD_selection - V10.py
  1003  system/CAD_selection.py
```

## 导入统计（原样输出）

```
Top imports (overall):
-  64 time
-  46 os
-  44 win32com.client
-  41 sys
-  38 pathlib
-  36 pythoncom
-  34 CAD_file_operations
-  21 CAD_basic
-  19 traceback
-  19 system.CAD_coordination
-  18 system.licad
-  18 subprocess
-  17 datetime
-  16 system.project_setup
-  14 tkinter
-  13 system.CAD_com_utils
-  13 shutil
-  13 math
-  11 system.common_logger
-  11 ctypes
-  11 win32gui
-  11 logging
-  11 re
-  10 win32con
-  10 functools
-   9 openpyxl
-   9 threading
-   8 json
-   8 pywintypes
-   7 system.CAD_selection

Local-ish imports (heuristic):
-  19 system.CAD_coordination
-  18 system.licad
-  16 system.project_setup
-  13 system.CAD_com_utils
-  11 system.common_logger
-   7 system.CAD_selection
-   4 scripts.CAD_basic
-   2 system.CAD_core
-   2 scripts.CAD_file_operations
-   1 system
```

## 关键观察
- `cad/system/licad.py` 内 `get_acad_doc` 被定义了 3 次，最后一个版本覆盖前两个。
- `cad/system/CAD_coordination.py` 内 `wait_quiescent` 被定义了 2 次，后者覆盖前者。

## 已整理模块摘要

### cad/system/CAD_com_utils.py
- 作用：COM 调用重试与日志静默控制。
- 关键点：LoggerHotSwapper 用函数指针替换实现“零开销”静音；warning/error 永远保留。
- API：retry_on_busy 装饰器；SafeCOM.call / SafeCOM.list_selection；silent_mode 上下文。

### cad/system/common_logger.py
- 作用：统一日志 + Excel 记录测试结果（tests/testfunc.xlsx）。
- setup_logger 使用 RotatingFileHandler 与 stdout handler。
- checkpoint / CriticalSection 用于测试记录与可选人工等待。

### cad/system/licad.py
- 作用：核心 COM 连接层（AutoCAD/Tianzheng）。集成 self-healing。
- AutoCadProxy 管理连接、doc/mp/sp 获取，SendCommand 被 SafeDocumentWrapper 接管为同步调用。
- 导出单例 C，提供 li/save/open/close 等薄封装；retry_on_busy 透传自 CAD_com_utils。

### cad/system/CAD_coordination.py
- 作用：运行协同与稳态等待（wait_quiescent）、命令同步、进程守护。
- 依赖 licad.C.raw_doc 进行状态检测，异常视为忙碌；记录 busy_hits。
- 提供 CADGuard/FileGuard、send_cmd_with_sync、wait_document_opened、ensure_single_process 等。

### cad/system/CAD_core.py
- 作用：高层 CAD API 聚合层，汇总 CAD_basic / CAD_basic_operations / CAD_selection。
- 连接策略：优先 licad，失败回退 CAD_basic；同步全局 acad/doc/mp/sp。
- 提供系统启动/关闭、文件操作、插入、文档管理等大量接口。

## 后续计划
- 继续整理 `cad/library/*.py`（领域模型与几何/对象封装）。
- 之后整理 `cad/scripts/*.py`（入口与编排脚本）。
- 最后梳理测试策略与优化路径。

## 模块总览（人工摘要）
- 详细自动摘要见 `cad/analysis/modules_summary.md`。
- 函数级审查清单见 `cad/analysis/review.md`（含 1301 个函数/方法）。

## 体系结构理解（当前版）
- **连接层**：`system/licad.py` 提供 C 代理（AutoCadProxy）连接 CAD COM；带自愈与重试。
- **重试/静音层**：`system/CAD_com_utils.py` 提供 retry_on_busy 与日志静默（LoggerHotSwapper）。
- **协同层**：`system/CAD_coordination.py` 负责等待空闲、命令同步、进程/文件守护。
- **操作范式层**：`system/CAD_basic_operations.py` 封装 open/new/save/close 标准流程。
- **聚合层**：`system/CAD_core.py` 与 `scripts/CAD_file_operations.py` 统一接口并回退 CAD_basic。
- **功能库层**：`library/*` 拆分自 CAD_basic，覆盖几何、对象、图块、注释、控制。
- **业务脚本层**：`scripts/Insert_chart/*`、`scripts/Master_Orchestrator.py` 等。
- **守护/监控层**：`system/cad_dialog_killer.py`、`system/cad_command_monitor.py`。

## 关键风险与现状
- `licad.py` 内 `get_acad_doc` 三次定义，行为由最后版本决定；历史逻辑被覆盖。
- `CAD_coordination.py` 内 `wait_quiescent` 两次定义，后者覆盖前者。
- `CAD_basic.py` 与 `library/*` 功能重叠，存在两套来源与不一致风险。
- 大量全局单例与副作用（C.acad/doc/mp/sp、日志替换、print 替换）。
- UI 自动化（窗口控制/鼠标点击/OBS录屏）依赖环境，测试需隔离。

## 核心模块详解（人工摘要）

### system/project_setup.py
- 作用：路径配置（PathConfig），提供 cad/scripts/system/workspace 的根路径。
- 依赖：无 COM；纯路径配置。

### system/CAD_selection.py
- 作用：选择集与实体转换（CastTo、动态封装）；提供丰富选择接口清单。
- 特点：包含 API MANIFEST；多处自动重试与窗口选择。
- 风险：依赖 CAD COM，选择与 Zoom 可能影响当前图面状态。

### system/CAD_basic_operations.py
- 作用：open/new/save/close 的标准化流程与进程检查。
- 依赖：CAD_coordination（wait_quiescent、send_cmd_with_sync 等）。
- 风险：对 CAD 状态高度敏感，需稳定的单进程环境。

### system/cad_dialog_killer.py
- 作用：后台关闭 CAD 弹窗（扫描 HWND，发送 ESC）。
- 风险：可能误关非目标弹窗；依赖窗口类名与进程名。

### system/cad_command_monitor.py
- 作用：监测 CAD 命令卡死并强制取消（ESC + COM）。
- 风险：抢焦点/发送物理按键可能影响用户环境。

### library/cad_geometry.py
- 作用：线面/多段线几何分析、封闭多边形、框选、轮廓、分割等算法。
- 依赖：shapely + CAD COM；大量函数用于多段线处理与打印区域识别。
- 风险：算法链较长，需独立纯函数化以便单元测试。

### library/cad_blocks.py
- 作用：块属性读写、块定义/实例管理、插入与炸开、清理块、块内实体处理。
- 观察：存在函数重复定义（如 delete_block_instances_and_definition_optimized）。
- 风险：破坏性操作多（删除/炸开/重定义），需事务化与备份。

### library/cad_objects.py
- 作用：对象排序、分组、句柄、XData、文字处理、图层管理。
- 特点：大量工具函数可拆分为纯函数；依赖 CAD COM。

### library/cad_control.py
- 作用：系统级控制（清缓存、杀进程、窗口/鼠标自动化、录屏、OBS）。
- 风险：强副作用/系统级操作；建议隔离为“运维工具层”。

### library/cad_annotation.py
- 作用：文字/标注/表格等注释工具函数。
- 风险：CAD COM 依赖；测试可通过 Mock 对象验证参数拼装。

### library/tarch_building.py
- 作用：天正建筑组件操作（墙/门/窗/房间）与 TUPDSPACE。
- 风险：强依赖 SendCommand 与等待空闲；易受 CAD 状态影响。

### library/execution_result.py
- 作用：统一执行结果模型（ExecutionStatus/ExecutionResult）。
- 可作为后续重构的返回值标准。

### library/test_monitor.py
- 作用：测试前后状态监测（对象统计、文件夹状态）并输出日志。

### scripts/CAD_basic.py
- 作用：历史巨型核心脚本，包含连接、选择、几何、对象、文件、块、控制等全套逻辑。
- 现状：与 library/* 高度重叠；仍被多个脚本直接 import。
- 风险：全局副作用多（print 替换、全局变量、复合依赖）。

### scripts/CAD_file_operations.py
- 作用：文件操作统一接口（open/new/save/close/insert）；与 CAD_core 功能重叠。
- 风险：依赖 CAD_basic + CAD_basic_operations + CAD_selection，多层耦合。

### scripts/CAD_System_Queue*.py
- 作用：UI 队列/调度系统（Tkinter + 内置 IDLE 执行器），用于分步执行脚本。
- 风险：大量 exec/动态执行，依赖 GLOBAL_CTX 共享内存。

### scripts/Master_Orchestrator.py
- 作用：工程图纸自动化总控（战役/战术层），串联 Insert_chart 流程。
- 风险：依赖业务脚本稳定性；需 FileGuard 与 CADGuard 保驾。

### scripts/Insert_chart/*
- 作用：图签插入/选择/测试与绘图脚本；属于业务层核心。
- 风险：操作面广、强依赖 CAD 状态，建议优先补充集成测试。

### scripts/函数编写规范.py / CAD_dev_standards.py / CAD_check_standards.py
- 作用：编码与脚本规范/检查辅助。

### scripts/选择测试错误.py / 测试.py / 连接测试.py / 修复codex脚本.py
- 作用：测试/修复类脚本，偏一次性或开发调试用途。

## 下一步工作指引
- 继续对 scripts/Insert_chart 与 CAD_basic.py 分段精读，补充关键流程与参数约束。
- 针对 review.md 中的高风险标记函数进行人工复核与分级。

## 函数级理解记录
- 已生成 `cad/analysis/functions.md`：每个函数包含参数、返回推断、调用概览、理解/风险/测试点。该文件为持续迭代的主入口。

## 进一步观察（脚本层）
- `scripts/Insert_chart/insert_labels.py` 内 `insert_and_scale_labels_area_any` 与 `normalize_core_title_blocks_by_layer_new1` 多次重复定义（后者覆盖前者），`run_title_block_assembly_pipeline` 也重复定义（后者覆盖前者）。

## 重复定义清单
- 已生成 `cad/analysis/duplicates.md`：列出同文件内重复定义函数（后定义覆盖前定义）。

## 调用关系图
- 已生成 `cad/analysis/callgraph.md`：同文件内的函数调用关系（简版）。

## 深度结构映射
- `cad/analysis/deep_cad_basic.md`：CAD_basic.py 分区与函数映射。 
- `cad/analysis/deep_insert_labels.md`：insert_labels.py 分区与函数映射。

## 函数级深度草稿
- 已生成 `cad/analysis/functions_deep.md`：包含调用/属性/异常结构/副作用线索，待逐函数人工修订。

## 重点重复定义（清单）
- `cad/analysis/duplicates.md` 已记录关键重复定义，例如 `licad.get_acad_doc` x3、`CAD_coordination.wait_quiescent` x2、`insert_labels.run_title_block_assembly_pipeline` 等（后者在 notes 中补充）。

## insert_labels 重复定义
- `cad/analysis/deep_insert_labels_duplicates.md`：重复定义的具体行号，用于人工核对覆盖版本。 

## Docstring 覆盖率
- `cad/analysis/doc_coverage.md`：按文件统计函数注释覆盖率。

## 风险热点
- `cad/analysis/risk_hotspots.md`：裸 except / COM / 文件 / 窗口操作函数清单。

## 分区概览
- `cad/analysis/section_summary.md`：按 #&& 分区统计函数与标签。

## 进一步人工理解补充
### scripts/CAD_System_Queue.py
- 结构：内嵌 IDLE 引导代码（字符串），通过本地 socket 监听执行脚本；GUI 负责选择/下发任务。
- 关键点：IDLE 端维护 GLOBAL_CTX（dy/ctq/ctq_p），用于跨步骤共享内存；run_script_in_main 在 __main__ 执行脚本。
- 风险：大量 exec/动态执行 + 全局状态共享；socket 端口固定 65432。

### scripts/脚本导航14版.py
- 作用：脚本导航/执行 GUI（Tree Edition），内置 IDLE 引导程序；修复 BOM 读取并在执行前切换 cwd。
- 机制：通过 socket 将脚本路径发送给 IDLE 引擎执行，日志按日期写入脚本目录。
- 风险：动态执行 + GUI 依赖，路径/编码处理是关键点。

## 选择模块清单
- `cad/analysis/selection_manifest.md`：CAD_selection 的 API MANIFEST 完整摘录。

## 深读优先级
- `cad/analysis/manual_focus.md`：自动评分得到的优先深读函数列表。

## insert_labels 流水线理解补充
- `run_title_block_assembly_pipeline`（后定义版本生效）：
  - Phase 1: 根据外部 coms 或交互选区，调用 `insert_and_scale_labels_area_any` 插入图签。
  - Bridge: `wait_quiescent` + `C.doc.Regen(1)` 稳定几何。
  - Phase 2: `normalize_core_title_blocks_by_layer_new1` 规范化/炸开核心图签壳块。
  - 失败即终止；成功输出流程完成日志。
## insert_labels 深读进度
- 已补充 `insert_labels.py` 的辅助函数（真实块名、规格→块名、几何缩放计算、二次校正等）与主流程 V9.3/V3.2 最终版理解，标注多版本定义覆盖关系。

## CAD_basic 连接层理解补充
- `CAD_basic.py` 通过 try/except 引入 `system.licad`，并覆盖 `li()` 实现连接后同步全局 `acad/doc/mp/sp`；若 licad 不可用则提供哑函数与退化 retry_on_busy。 
- 因此大量旧函数依赖全局变量，不经过 C 代理直接操作 COM 对象。 

## 人工深读记录
- 已新增 `cad/analysis/manual_understanding.md`：人工深读的函数级理解（持续补充）。

## 人工深读进度
- 已补充 CAD_basic 的目录编制与 Excel 导入/导出相关核心函数到 manual_understanding.md。

## 人工深读进度
- 已补充打印相关函数与目录图签写入函数的人工理解。 

## 人工深读进度
- 已补充图层管理函数与 cad_command_monitor 强制取消逻辑的人工理解。

## 人工深读进度
- 已补充 CAD_coordination 的 CADGuard 与 send_cmd_with_sync 理解。 

## 人工深读进度
- 已补充 CAD_selection 关键窗口/选择集函数理解。 

## 人工深读进度
- 已标注 CAD_basic 中与库重复的块重定义函数。 

## 人工深读进度
- 已补充 CAD_file_operations 的新建/打开/保存/布局切换等核心接口理解。 

## 人工深读进度
- 已补充 licad 核心连接与文件操作函数理解。 

## 人工深读进度
- 已补充 cad_blocks 关键块操作函数（ATTSYNC/属性读写/插入炸开/建块/追加/回溯爆炸）。
## 人工深读进度
- 已补充 CAD_basic 的目录模板配置读取与 LISP 布局打印 v1 逻辑理解。
## 人工深读进度
- 已补充 CAD_basic 目录图签专用写入函数 update_catalog_titleblocks_from_excel_y 理解。
## 人工深读进度
- 已补充 CAD_basic 模型/布局打印核心与批量打印引擎函数理解（export_*_pure / print_dwg_file_model / print_polylines_list）。
## 人工深读进度
- 已补充 library/cad_control.py 核心控制函数理解（fix_com_cache / 视图缩放 / 样式重命名 / MATCHPROP / srhd/srhd_p）。
## 人工深读进度
- 已补充 library/cad_geometry.py 关键几何处理函数理解（样条长度估算/伪交点/打断/去重/房间轮廓/绘制/天正多行文字提取）。
## 人工深读进度
- 已补充 library/cad_objects.py 常用对象/图层操作函数理解（分组复制/交互设层/批量建层/逐点标注/模型空间清理/强制改色）。
## 人工深读进度
- 已补充 library/cad_blocks.py 块定义/清理/提取/炸开等核心函数理解（update_block_def_attributes_v7、delete_block_instances_and_definition_optimized、safe_explode_retry 等）。
## 人工深读进度
- 已补充 CAD_coordination 的 wait_quiescent/wait_document_opened 理解（注意文件内重复定义覆盖）。
## 人工深读进度
- 已补充 CAD_selection 扩展选择函数理解（ss_select / select_paperspace_objects_in_window / get_last_n_objects / unhide_all）。
## 人工深读进度
- 已补充 cad_command_monitor.analyze_state 理解（忙碌判定与提示语关键字）。
## 人工深读进度
- 已补充 CAD_System_Queue.py 锁管理与 MasterRunner 初始化逻辑理解。
## 人工深读进度
- 已补充 CAD_basic 中与 library 模块重复实现的函数映射说明（控制/几何/块/对象）。
## 人工深读进度
- 已补充 CAD_Legacy_Runner GUI 初始化与另存为逻辑理解。
## 人工深读进度
- 已补充 tarch_building 的窗口激活函数理解（activate_cad_middle_click / _activate_cad_safe）。
## 人工深读进度
- 已标注 system/licad、CAD_coordination、CAD_selection、CAD_System_Queue 的版本快照与主文件的对应关系。
## 人工深读进度
- 已补充 CAD_check_standards.bianmulu_func4_h 测试规范版逻辑理解。
## 人工深读进度
- 已补充 脚本导航14版.py 的日志/注册表/解析与 GUI 初始化逻辑理解。
## 人工深读进度
- 已补充 common_logger 的关键日志/检查点/Excel 记录机制理解。
## 人工深读进度
- 已补充 CAD_com_utils 的日志热替换与重试机制理解（LoggerHotSwapper / retry_on_busy / SafeCOM）。
## 人工深读进度
- 已补充 project_setup.PathConfig 路径配置理解。
## 人工深读进度
- 已补充 CAD_basic_operations 关键保存/关闭范式理解。
