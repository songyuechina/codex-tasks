# Supervised Task Packet
role: coder
title: pseudo-print-area-heuristic

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦实现推进，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。

## Objective
针对建筑施工图打印区域，提出一套可编码的“伪打印区域内容复杂度”度量标准。要求可落地、少而稳，不要空谈。

## Context
已知复杂案例中第一张只是矩形图形，第二张是打印线型说明框，都不应视为有效打印区域。用户建议：若区域空白，或仅有简单几何图形和少量文字，而其它打印区域明显复杂，则可判为伪打印区域候选。需要可编码的指标。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.
