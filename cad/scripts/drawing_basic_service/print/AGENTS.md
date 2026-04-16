# AGENTS.md

适用范围：`D:/codex-tasks/cad/scripts/drawing_basic_service/print/`

## 1. 任务总原则

本目录有两条链：

- 打印主链
- 打印信息分析辅助链

优先级永远是：

1. 先保证打印主链稳定
2. 再做打印信息分析与扩展

## 2. 打印模式硬规则

当前有效打印模式只有：

- `basic`
- `adaptive`
- `purified_adaptive`

禁止：

- 重新引入 `analysis` 打印模式
- 把辅助分析伪装成打印模式

## 3. 默认判断

- 用户未明确指定打印模式，默认 `basic`
- 用户未明确指定打印信息分析模式，默认 `basic`
- 用户只说“获取打印信息”时，默认走当前 `print_info_analysis.py` 主链，不另造新入口
- `adaptive` 只在确有必要时使用
- `purified_adaptive` 必须先产出 `content_analysis.json` 再过滤伪区域
- 若 `purified_adaptive` 同时命中伪区域风险和伪极大外包范围，还必须产出 `scope_analysis.json` 并先做范围收束
- 打印信息分析默认只分析最终参与分析的打印区域，不附带真实打印
- 无论由项目总管还是人直接调度，默认判断都不得变化

## 4. 打印信息分析硬规则

当前“获取打印信息”必须按统一主链处理，不得在别处再维护平行图签分析逻辑。

### 4.1 图签信息区域 `graphic_info_area`

- 先找打印区域内框线
- 再找与内框线角点对齐的图签块
- 横向图纸：按内框线右下角和块右下角对齐
- 竖向图纸：按“整体考察时相当于旋转 `-90` 度”的口径处理，使用内框线左下角和块左下角对齐
- 对齐后的块外包盒，就是当前页的 `graphic_info_area`

### 4.2 文字采样硬规则

- `graphic_info_area` 内对象统一通过 `CAD_selection.select_entities_in_window(...)` 取样
- 文字对象只认：`AcDbText`、`AcDbMText`、`TDbText`、`TDbMText`
- 文字内容统一通过 `library.cad_annotation.get_text_content()` 获取纯文字内容
- 不再在业务层重复维护 CAD / 天正文字的分支读取逻辑

### 4.3 图纸编号 / 图纸名称判定顺序

必须按以下优先级依次尝试，命中即停止，不得跳序：

1. `layer_named`
   若 `graphic_info_area` 中存在图层名包含 `图纸编号` 和 `图纸名称` 的文字对象：
   - `图纸编号` 图层中的文字统一视作编号
   - 按外包盒左下角 `x` 从左到右合并为一个编号记录
   - `图纸名称` 图层中的文字统一视作名称
2. `guide_rectangles`
   若角点对齐图签块内部可识别出两根 `Defpoints` 图层的矩形多段线：
   - 红色矩形对应图纸名称区域
   - 绿色矩形对应图纸编号区域
   - 这两个矩形对应的是整个空间中的窗口区域，不是只在块定义内部取文
3. `fallback_regex`
   若前两种都不成立：
   - 按文字内容是否符合编号格式
   - 再结合 `graphic_info_area` 内最低 / 次低文字对象的位置关系
   - 统一收束为 1 个编号记录，其余文字视作图纸名称候选

### 4.4 稳定性口径

- 打印信息单页分析必须接受 COM busy / rejected 的有限重试
- 单页最终失败时允许降级为错误行，但不得拖垮整批任务
- 若真实案例证明三种判定顺序或细节有误，应优先修正文档和当前主链，而不是临时旁路
## 5. 调度与自修复硬规则

1. 打印执行工作区必须可被项目总管或人直接调度
2. 调度输入不完整时，应按 `PRINT_DISPATCH_PROTOCOL.md` 的默认规则补全
3. 若执行过程中暴露脚本缺陷，不得只绕过问题，必须判断是否进入自修复闭环
4. 自修复必须遵守：先复现，再修补，再回归，再沉淀
5. 自修复后，必须同步更新本目录文档和 `D:\codex-tasks\thoughtway\conversation_log.md`

## 6. 执行时的强制要求

1. 不要绕过 `print_policy.py` 私自拼打印计划
2. 不要在打印主链中无故夹带打印信息分析副作用
3. 不要再维护与 `print_info_analysis.py` 重复职责的旧图签分析主链
4. 涉及 COM 枚举、包围盒、选择集、文字读取时，必须考虑 busy/retry
5. 文档口径与代码冲突时，应先修正文档，不要让冲突长期存在
6. 新案例产生后，应同步更新案例与知识文档
7. 单文件任务的最终交付必须落在源 DWG 同目录的 `<公共名>pdf / <公共名>analysis / <公共名>prosess`
8. 暴露新问题的异常 DWG 应同时复制进 `cases/assets/` 作为典型案例
9. 批量打印时默认每成功 `6` 张后清理一次 WPS 窗口，并在横竖向批次切换后强制再清理一次
10. 开始任何真实打印前，必须先遵守 `D:\codex-tasks\thoughtway\CAD_RUNTIME_GUARD_RULES.md`
11. 必须明确本次使用的天正受控入口，以及发现纯 CAD / 非天正环境后的恢复入口
12. 若运行中怀疑已经偏到纯 CAD，必须立即停止当前打印链，先恢复环境，再继续打印
13. 批量打印时，每完成一个 DWG 的完整处理后，必须把 CAD 归一回 `1 个进程 + 1 个空白天正会话`，当前默认入口是 `CAD_core.cad_zt_oneb()`
14. 不得让多个历史 DWG 长时间堆积在同一 CAD 会话里继续跑后续批次
15. 若用户要求“打印并获取打印信息”，默认先完成最终打印，再对最终保留的打印区域集合做 `print_info_analysis`
16. 若用户要求按打印信息命名 PDF，默认基于最终 `print_info_analysis.json` 与最终 PDF 目录生成 `pdf/named/` 副本，不覆盖原 PDF

## 7. 修改策略

优先：

- 收束主链
- 减少平行入口
- 保留实测有效经验

避免：

- 为单次案例临时堆一个新脚本
- 在多个脚本里保存同一职责
- 让 README、规则、脚本实现三套口径并存

## 8. 输出约束

打印主链至少要留下：

- `print_plan.json`
- `print_summary.json`

净化适配模式还要留下：

- `content_analysis.json`
- `scope_analysis.json`（若触发伪极大范围分析）

打印信息分析至少要留下：

- `print_info_analysis.json`
- `print_info_analysis.xlsx`

按打印信息命名 PDF 时，还要留下：

- `pdf/named/`

## 9. 文档约束

本目录文档分工必须清晰：

- 规则写进 `AGENTS.md`
- 调度协议写进 `PRINT_DISPATCH_PROTOCOL.md`
- 流程写进 `PRINT_WORKFLOW.md`
- 输出标准写进 `PRINT_OUTPUT_SPEC.md`
- 经验知识写进 `PRINT_KNOWLEDGE.md`
- 案例索引写进 `cases/CASE_MANIFEST.md`

不要把所有内容继续堆回一个大 README。
