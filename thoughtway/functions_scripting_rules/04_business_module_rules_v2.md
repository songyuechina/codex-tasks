# 04_business_module_rules.md

版本：V2.0

## 目标

规范业务模块与系统模块的写法，使智能体能够：

- 快速定位职责
- 快速引用函数
- 快速重构而不迷失边界

## 业务模块基本要求

1. 职责单纯
2. 边界清楚
3. 通过系统层复用基础能力
4. 不自行建立新的连接入口、日志入口、引导入口

## 当前系统骨架中的参考边界

- `licad.py`：统一连接入口层
- `CAD_selection.py`：选择与对象研究层
- `CAD_core.py`：基础控制与文件操作层
- `CAD_coordination.py`：协同与保护层
- `CAD_com_utils.py`：COM busy/retry 辅助层
- `common_logger.py`：日志与记录层
- `content_analysis_dwg_file.py`：内容分析与验证层
- `project_setup.py`：纯路径配置层

业务模块应建立在这些基础层之上。

## 可重构原则

业务模块不必机械继承历史函数形式。  
但必须继承：

- 项目思想
- 系统规则
- 已被实践验证有效的经验
- 案例与校验标准

## 当前特别注意事项

### 不轻率整体重写的核心
- `licad.py`
- `CAD_selection.py`

### 允许继续收束的核心
- `CAD_core.py`
- `CAD_coordination.py`
- `CAD_com_utils.py`
- `common_logger.py`
- `content_analysis_dwg_file.py`

## meta 与业务模块的关系

每个重要脚本都应有：

- `quote.meta.json`
- `procedure.meta.json`

目的不是重复源码，而是压缩：
- 脚本角色
- 关键函数
- 核心流程
- 不可丢失经验

## 禁止行为

- 业务模块自行建立新的 CAD 主连接入口
- 业务模块自行建立新的日志总入口
- 把新的杂项职责无限堆进单个核心模块
- 认为旧代码形式不可改变
- 反过来又轻率推翻已验证有效的经验
