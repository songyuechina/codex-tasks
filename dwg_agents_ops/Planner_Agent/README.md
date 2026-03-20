# Planner Agent

负责为 `D:/codex-tasks` 中的复杂 DWG / CAD 自动化任务做任务级规划、阶段拆分、依赖识别与执行顺序建议。

## 启动

```powershell
python D:\codex-tasks\dwg_agents_ops\Planner_Agent\agent_cli.py
python D:\codex-tasks\dwg_agents_ops\Planner_Agent\agent_cli.py --print-config
python D:\codex-tasks\dwg_agents_ops\Planner_Agent\agent_cli.py --once "基于 @file cad/scripts/drawing_basic_service/print/README.md 给出打印任务三阶段执行计划"
```
