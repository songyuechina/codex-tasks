@echo off
chcp 65001 >nul
title CodexGuardLauncher

REM 直接启动带 Transcript 的 Codex 控制台
REM 这里调用的是 D:\codex-tasks\CodexConsole.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "D:\codex-tasks\CodexConsole.ps1"
