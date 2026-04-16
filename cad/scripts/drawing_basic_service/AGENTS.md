# AGENTS.md

适用范围：`D:/codex-tasks/cad/scripts/drawing_basic_service/`

本目录是 `drawing_basic_service` 领域工作区的根目录，当前主要包含两个子域：

- `illustration_label/`
- `print/`

## 1. 进入本目录先看什么

优先阅读：

1. 本文件 `AGENTS.md`
2. `illustration_label/AGENTS.md`
3. `print/AGENTS.md`
4. `illustration_label/README.md`
5. `print/README.md`

若需要结构分析，再使用本目录已经准备好的 GitNexus 索引。

## 2. GitNexus 已就绪

本目录已经完成 GitNexus 索引，索引目录在：

- `.gitnexus/`

当前索引摘要：

- repo: `drawing_basic_service`
- files: `112`
- nodes: `914`
- edges: `2036`
- clusters: `46`
- processes: `73`

说明：

- 该索引是按 `D:/codex-tasks/cad/scripts/drawing_basic_service` 目录建立的
- 建索引时使用了 `--skip-git`，因为这里是项目子目录，不是独立 git 仓库
- 它适合帮助新智能体快速理解文件依赖、执行流、影响范围
- 它不能替代 CAD 业务规则、真实 DWG 测试、runtime guard 监督链

## 3. GitNexus 适合用来解决什么

适合：

- 快速看 `illustration_label` 和 `print` 的文件级依赖关系
- 查某个脚本/函数的上下游
- 查改动影响面
- 辅助生成结构说明和接手地图

不适合：

- 判断 CAD 图形语义是否正确
- 判断某个块是否是真正图签块
- 替代真实 DWG 回归测试

## 4. 常用 GitNexus 命令

在本目录执行：

```powershell
& 'C:\Users\User\AppData\Roaming\npm\gitnexus.cmd' status
& 'C:\Users\User\AppData\Roaming\npm\gitnexus.cmd' list
& 'C:\Users\User\AppData\Roaming\npm\gitnexus.cmd' query "illustration label"
& 'C:\Users\User\AppData\Roaming\npm\gitnexus.cmd' context illustration_frame_service
& 'C:\Users\User\AppData\Roaming\npm\gitnexus.cmd' impact illustration_frame_service
```

若目录结构有明显变化，需要刷新索引：

```powershell
& 'C:\Users\User\AppData\Roaming\npm\gitnexus.cmd' analyze D:\codex-tasks\cad\scripts\drawing_basic_service --skip-git --skip-agents-md
```

## 5. 接手策略

新智能体进入本目录时，建议顺序如下：

1. 先读子目录 `AGENTS.md/README.md`
2. 再用 GitNexus 看骨架与依赖
3. 再进入具体脚本和函数
4. 真正执行 CAD 任务时，回到各子目录规则，并使用 runtime guard

## 6. 当前共识

GitNexus 在这里的角色是“结构导航器”，不是“业务裁判”。

它负责帮助智能体更快看清：

- 哪些脚本是入口
- 哪些脚本是核心
- 哪些依赖需要小心

真正的业务判断仍以：

- 子目录 `AGENTS.md`
- 子目录 `README.md`
- meta 文件
- 真实 DWG 测试

为准。
