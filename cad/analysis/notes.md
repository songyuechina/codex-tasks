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
