# Reviewer Agent

负责对 `D:/codex-tasks` 的实现结果进行 findings-first 审查，强调风险、回归、遗漏与边界。

## 启动

```powershell
python D:\codex-tasks\dwg_agents_ops\Reviewer_Agent\agent_cli.py
python D:\codex-tasks\dwg_agents_ops\Reviewer_Agent\agent_cli.py --print-config
python D:\codex-tasks\dwg_agents_ops\Reviewer_Agent\agent_cli.py --once "审查 @file cad/system/licad.py 的最近修改思路"
```
