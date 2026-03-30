整体系统架构
版本V1.0  2026-02-27
---------------------

1) 顶层结构
D:/codex-tasks/
  cad/                  # A. 驱动天正CAD系统脚本（执行环境层，历史保留）
  dwg_cases/            # B. DWG案例资产系统（典型 + 真实）
  dwg_agents_ops/       # C. 面向DWG作业的智能体系统（运行/修正/反馈）
  dwg_system_tools/     # D. 面向DWG系统控制的工具系统（分析/索引/状态差异）
  thoughtway/           # E. 整个项目的思想方法和参考资料（我新加的部分）
  folder.meta.json      # 根系统宪法（机器读）
  SYSTEM_RULES.md       # 根系统宪法（人读，可选）

2) 系统语义定位（写进 root folder.meta）
目录	           系统角色	        核心对象	     职责关键词
cad	           执行层	      CAD软件接口	驱动、绘图、文件操作
dwg_cases	   资产层	        DWG文件	       典型案例、真实案例、回归
dwg_agents_ops	   作业层	        DWG任务	        运行、验证、修正、积累
dwg_system_tools   控制层	        DWG系统	         分析、生成、索引、对比
thoughtway         方法层               全部体系         实现目标的思想指导

依赖关系：

dwg_agents_ops → cad + dwg_cases + dwg_system_tools #智能体通过cad、dwg_system_tools操作dwg_cases
cad → dwg_cases                                     #cad脚本从dwg_cases建立
dwg_cases → (无)                                    #dwg_cases是最底层的对象 
dwg_system_tools → (thoughtway)                     #为智能体控制cad脚本服务
thoughtway → (实践反馈和哲学思想)                   #控制整个系统的指导思想


4) 各子系统内部最小结构
4.1 cad/
cad/
  scripts/              # 业务脚本
  system/               # 系统基础脚本
  library/              # 一般操作 
  system_dwg_file       # 系统所用的dwg文件 
  folder.meta.json


4.2 dwg_cases/
dwg_cases/
  typical/              # 典型基准案例（可回归）
  real/                 # 真实生产案例（持续累积）
  folder.meta.json

每个案例配 meta：
print_area_01.dwg
print_area_01.case.meta.json

4.3 dwg_agents_ops/
dwg_agents_ops/

  Planner_Agent/        # 规划
  Implementer_Agent/    # 编码
  Reviewer_Agent/       # 审查
  Tester_Agent/         # 测试

  folder.meta.json

这里放：

案例运行器

meta 生成驱动

回归校验器

自动修正调度器

4.4 dwg_system_tools/
dwg_system_tools/
  meta_gen/            # 从脚本生成 quote/procedure meta
  function_graph/      # 函数引用/调用图
  state_diff/          # CAD运行前后状态差异
  registry/            # 全局索引数据库
  folder.meta.json


5) folder.meta.json 在这个结构里的角色

现在它的语义非常清晰：

/codex-tasks/folder.meta.json → 系统地图 + 依赖规则

/cad/folder.meta.json → CAD执行脚本结构

/dwg_cases/folder.meta.json → 案例资产结构

/dwg_agents_ops/folder.meta.json → 智能体作业结构

/dwg_system_tools/folder.meta.json → 控制工具结构

/thoughtway → 控制整个系统

形成完整“系统语义目录树”。

6) 系统哲学（写进 SYSTEM_RULES）

在哲学思想和实践反馈"/thoughtway"的指导下，建立系统控制工具"/dwg_system_tools"和dwg文件操作脚本"/cad"；智能体"/dwg_agents_ops"

借助累积建立的"/cad"脚本和系统控制工具"/dwg_system_tools"操作"/dwg_cases"。


系统架构为AI的高效稳定运转服务同时兼顾人理解的方便，人的需求和AI的运转融合为一；
真实案例和典型测试案例融合为一,案例和脚本融合为一；
脚本和脚本信息是系统控制的核心依赖，通过信息分层和合理存储实现控制的快速和稳定，脚本和信息融合为一；
深度展开各个重要问题的专题研究驱动全部体系的发展，人和AI融合为一。




你接下来要跑的第一个任务（common_logger.py）可以这样填：

<SCRIPT_PATH>：D:/codex-tasks/cad/system/common_logger.py

<STEM>：common_logger

<KEY_FUNC_1>：setup_logger

<KEY_FUNC_2>：record_test_result

<KEY_FUNC_3>：set_debug_mode
