# Supervised Task Packet
role: tester
title: pseudo-print-area-test-plan

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦测试结论与阻塞，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。

## Objective
从测试视角提出最小验证集，专门验证伪打印区域内容判定和图签识别两类新能力。要小而有效。

## Context
已有复杂案例：第一张是简单矩形，第二张是打印说明框，其余大量图纸较复杂。后续还要做图签识别，优先属性块，再普通块，再局部文字。请给最小测试样本集合与预期。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.
