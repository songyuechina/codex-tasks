# Supervised Task Packet
role: planner
title: healthcheck

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦任务分解、阶段计划和依赖识别，不要越权进入实现细节，严格基于主控提供的上下文回答。

## Objective
返回一句简短确认，证明你当前可以正常收发消息。

## Context
只返回一句确认，不要展开。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.
