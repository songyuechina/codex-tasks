# Supervised Task Packet
role: reviewer
title: title-block-heuristic-review

## Supervisor Rules
1. 不要自行猜测或搜索其他工作区路径。
2. 只允许基于本任务包中给出的事实、摘要、文件内容回答。
3. 如果信息不足，应明确指出缺口，但不要编造。
4. 聚焦 findings-first 审查，不要自行猜测工作区路径，严格基于主控提供的上下文回答。

## Objective
以审查视角给出一套高置信的图签识别优先级规则，只要原则，不要长文。重点是属性块优先、普通块退化、右侧/下侧区域判定。

## Context
用户规则：图签通常在打印区域右侧或下侧；右侧时对1:100系列常见宽6000-11000，高与内框线同高；图签可能是属性块、普通块，或块外混有图纸名称和序号文字；原则是能分出图签块就分，能取信息就取，不能就放过。

## Output Requirement
必须以如下格式收尾：
[PROGRESS] task=<id|none>; status=<state>; completion=<0-100>; next=<one sentence>.
