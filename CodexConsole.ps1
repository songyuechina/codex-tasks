$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.UTF8Encoding]::new()

# 记录当前 Codex 启动进程 PID
$pid | Set-Content -Encoding utf8 -Path 'D:\codex-tasks\codex_pid.txt'

Start-Transcript -Path 'D:\codex-tasks\ai_console.log' -Append -Force

Set-Location 'D:\codex-tasks'

# 关键：恢复上次 codex 会话
& codex resume --cd "D:\codex-tasks" --last

Stop-Transcript
