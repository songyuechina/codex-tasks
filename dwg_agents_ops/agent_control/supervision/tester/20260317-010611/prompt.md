# Supervised Task Packet
role: tester
title: Minimal test order for title-block analysis

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦测试结论与阻塞，不要自行搜索不存在的路径，严格基于主控提供的上下文回答。

## Objective
给出不超过5步的最小验证顺序，帮助确认当前图签分析拿不到图纸名称/图号，究竟是因为：1) 文字采样缺失；2) 嵌套块未展开；3) 选到的是块框不是文字区。只输出测试观点和验证顺序。

## Context
已知事实：当前复杂案例 47/47 都能找到主图签候选块，多数 block_name=TQ1；但 drawing_title/drawing_no/project_name 全为空。
