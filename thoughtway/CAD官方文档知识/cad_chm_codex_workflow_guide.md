# 围绕 `acad_aag.chm` 与 `acadauto.chm` 建立 CAD2021 本地智能检索文档体系的执行指南

## 一、任务目标

当前原始开发文档位于：

```text
D:\codex-tasks\cad\official_development_document
```

其中包含两份核心文档：

```text
acad_aag.chm
acadauto.chm
```

本任务的目标不是顺序阅读整本 CHM，而是建立一套 **面向 CAD2021 + pywin32 + 本项目自动化任务** 的本地文档检索体系，使 Codex 在需要时能够：

1. 迅速找到当前任务所需的 API、对象、方法、属性、事件。
2. 尽量直接映射到 Python + pywin32 的调用方式。
3. 优先指向项目中已有的稳定包装器和执行路径。
4. 对高频任务形成可复用的任务卡，对低频主题保留临时查询入口。

最终效果应当是：

> Codex 不必反复全文翻阅 CHM，而是通过本地索引、核心符号卡、任务卡、pywin32 规则层，快速定位并支撑代码实现。

---

## 二、总原则

### 1. 不顺序研读整本 CHM

CHM 是原始依据，不是工作主界面。

禁止一开始就：

- 顺序摘要整本 CHM
- 为每个页面都生成 Markdown
- 机械复制书本目录结构
- 把 VBA/ActiveX 语法直接当成 pywin32 代码写法

正确做法是：

- 先解包
- 再建页面总清单
- 再分类 `keep / defer / skip`
- 先做高频内容
- 后做低频临时索引

---

### 2. 以任务为主，不以目录为主

主入口应该是任务，而不是文档章节。

优先围绕以下问题组织：

- 如何连接 AutoCAD / 获取活动文档
- 如何切换布局
- 如何判断模型空间 / 图纸空间
- 如何枚举布局
- 如何构造选择集
- 如何遍历对象并读取 ObjectName / Handle / Layer
- 如何读取块属性
- 如何插入图块
- 如何创建基础几何对象
- 如何读取打印相关信息
- 什么时候应回退到 `SendCommand`

---

### 3. 高频内容做深，低频内容做薄

#### 高频内容
必须建立完整卡片体系：

- 核心符号卡
- 任务卡
- pywin32 映射说明
- 常见失败点
- 项目内推荐路径

#### 低频内容
只保留轻量索引：

- 标题
- 所属对象
- 方法/属性/事件分类
- 路径
- 一行摘要
- 关键词

低频内容不做大面积深加工，只在需要时临时查询。

---

## 三、必须避免的错误方向

### 1. 不要为所有页面都生成完整 Markdown

这会制造大量垃圾文件，尤其以下页面默认不应进入核心层：

- `*_see_also.htm`
- `idx_*`
- `all_*`
- `idh_*`
- `IDH_*`

这些页面通常只是辅助跳转、索引、参见页，信息密度低。

---

### 2. 不要直接复制原始文档结构

原始 CHM 结构适合人工点阅，不适合智能体任务检索。

智能体最需要的是：

- 快速检索入口
- 对应任务路径
- pywin32 参数格式说明
- 前置条件
- 常见风险
- 项目内优先调用方式

---

### 3. 不要把 VBA 语法直接当成 Python 写法

文档大量采用 ActiveX/VBA 叙述方式。必须建立单独的 **pywin32 映射层**，说明：

- 点坐标如何传
- Variant / SAFEARRAY 如何理解
- 集合如何遍历
- 枚举值怎样处理
- 常见 COM 报错的上下文原因是什么

---

### 4. 不要试图第一次就做完整精修

正确策略是：

1. 全量扫描，建立清单
2. 先筛高价值页
3. 建高频任务卡
4. 建 pywin32 规则层
5. 建低频临时查询层
6. 逐步扩展

---

## 四、推荐目录结构

请在原始文档目录下建立如下工作体系：

```text
D:\codex-tasks\cad\official_development_document\
│
├─ acad_aag.chm
├─ acadauto.chm
│
├─ 00_readme\
│   ├─ README_Codex_Workflow.md
│   ├─ README_Filter_Rules.md
│   ├─ README_Task_Priority.md
│   └─ README_File_Formats.md
│
├─ 01_extracted_html\
│   ├─ acad_aag\
│   └─ acadauto\
│
├─ 02_manifest\
│   ├─ page_manifest.jsonl
│   ├─ page_manifest.csv
│   ├─ value_ranking.jsonl
│   ├─ skip_list.jsonl
│   ├─ defer_list.jsonl
│   └─ alias_map.json
│
├─ 03_core_symbols\
│   ├─ objects\
│   ├─ methods\
│   ├─ properties\
│   ├─ events\
│   ├─ types_and_variants\
│   └─ system_variables\
│
├─ 04_task_cards\
│   ├─ 01_connect_and_document\
│   ├─ 02_space_and_layout\
│   ├─ 03_selection\
│   ├─ 04_entities_create\
│   ├─ 05_blocks_and_attributes\
│   ├─ 06_layers_and_styles\
│   ├─ 07_plot_and_output\
│   ├─ 08_command_fallback\
│   └─ 09_misc_common_tasks\
│
├─ 05_pywin32_bridge\
│   ├─ pywin32_type_rules.md
│   ├─ point_array_rules.md
│   ├─ variant_rules.md
│   ├─ collection_rules.md
│   ├─ sendcommand_rules.md
│   ├─ common_patterns.md
│   └─ common_failures.md
│
├─ 06_on_demand_index\
│   ├─ uncommon_topics.jsonl
│   ├─ uncommon_keywords.json
│   └─ topic_path_map.json
│
├─ 07_validation\
│   ├─ validation_tasks.md
│   ├─ validation_cases.json
│   ├─ task_to_existing_code_map.json
│   └─ reviewed_examples\
│
└─ tools\
    ├─ extract_chm.ps1
    ├─ build_manifest.py
    ├─ classify_pages.py
    ├─ build_core_symbols.py
    ├─ build_task_cards.py
    ├─ build_on_demand_index.py
    ├─ search_cad_help.py
    └─ validate_doc_system.py
```

---

## 五、分层设计思想

### 第一层：原始层

原始 CHM 只保留，不改写，不作为日常主入口。

---

### 第二层：页面索引层

对所有页面建立统一清单，解决“有什么”的问题。

主要文件：

- `page_manifest.jsonl`
- `page_manifest.csv`
- `skip_list.jsonl`
- `defer_list.jsonl`

---

### 第三层：核心符号层

只提炼高价值对象、方法、属性、事件。

这是精简后的 API 符号层，不是全文复制层。

---

### 第四层：任务卡层

这是主入口层。

必须围绕任务组织，不围绕书本章节组织。

---

### 第五层：pywin32 映射层

把 ActiveX/VBA 术语翻译成 Python + pywin32 视角下的可操作模式。

---

### 第六层：临时查询层

低频内容只做轻量索引，留作按需查询。

---

## 六、页面筛选原则

这是整个工程最关键的判断规则。

### 1. 首批必须优先深读的内容

#### A. 文档/应用/集合类

- Application
- Documents
- Document
- Preferences
- Utility
- SelectionSets
- Layers
- Layouts
- Blocks

#### B. 空间与布局类

- ModelSpace
- PaperSpace
- Layout
- Layouts
- ActiveLayout
- Block

#### C. 几何对象创建类

- AddLine
- AddPolyline
- AddLightWeightPolyline（如有）
- AddText
- AddMText
- AddCircle
- AddArc
- AddBlock / InsertBlock
- 常用 Dim 系方法（若当前项目确实会用）

#### D. 块与属性类

- BlockReference
- Attributes
- GetAttributes
- HasAttributes
- AttributeReference
- 属性读写相关方法或属性

#### E. 选择与枚举类

- SelectionSet
- Select
- SelectOnScreen
- SelectByPolygon（按需要）
- Item
- Count
- Handle
- ObjectName
- Layer
- Coordinates
- BoundingBox
- GetXData（按需要）

#### F. 系统控制类

- SendCommand
- GetVariable
- SetVariable
- Regen
- Open / Save / Close / Activate

#### G. 打印与输出类

- Plot
- ActiveLayout
- PlotConfiguration
- Layout 上与打印有关的重要属性
- PlotDevice / PaperSize / StyleSheet 相关页面

#### H. 类型与参数规则

- 点坐标
- Variant
- SAFEARRAY / 数组
- 集合遍历
- 枚举值
- 返回对象类型

---

### 2. 首批不应深度整理的内容

#### A. 直接 `skip`

以下页面类型默认直接跳过：

- `*_see_also.htm`
- `idx_*`
- `all_*`
- `idh_*`
- `IDH_*`

#### B. 先 `defer`

以下页面先降级处理，只留轻量索引：

- `ex_*` 示例页
- 高级 3D 实体、曲面、放样、材质、渲染、颜色书相关页
- 当前项目主线明显不需要的冷门对象

#### C. 当前业务暂缓

如果当前核心是施工图自动化、打印、插图签、目录、布局、块属性、对象统计，则以下内容暂缓：

- 高级 3D 实体建模
- loft / helix / surface / materials
- 复杂视觉样式控制
- 冷门事件系统细节
- 很少用到的发布功能
- 高级表格细枝末节

---

## 七、常用与不常用内容的处理策略

### 1. 常用内容：做成完整卡片体系

对高频高价值内容，建立：

- 核心符号卡
- 核心符号元数据
- 任务卡
- pywin32 映射说明
- 易错点说明
- 项目内优先调用路径

---

### 2. 不常用内容：做成轻量临时索引

低频内容只保留如下信息：

- 标题
- 所属对象
- 分类
- 路径
- 一行摘要
- 关键词
- 延后原因

这样以后需要时可迅速查到，但不会污染核心层。

---

## 八、文件格式要求

## 1. 页面总清单：`page_manifest.jsonl`

所有页面必须先进入清单，再决定是否深入。

建议字段如下：

```json
{
  "topic_id": "acadauto:AddLine",
  "source_doc": "acadauto",
  "basename": "AddLine.htm",
  "title": "AddLine Method",
  "kind_guess": "method",
  "owner_guess": "ModelSpace|PaperSpace|Block",
  "class_guess": "core_symbol",
  "value_level": "high",
  "status": "keep",
  "keywords": ["AddLine", "geometry", "line", "create"],
  "path": "01_extracted_html/acadauto/AddLine.htm",
  "notes": "高频几何创建方法，应进入核心符号层和任务层。"
}
```

说明：

- `status` 只能是 `keep / defer / skip`
- `value_level` 建议使用 `high / medium / low`
- `owner_guess` 允许不完全准确，但后续要修正

---

## 2. 核心符号卡：`03_core_symbols/.../*.md`

每个高价值符号建立一个简洁 Markdown 文件。

推荐模板：

```md
# AddLine Method

## 基本信息
- 来源：acadauto
- 类别：method
- 所属对象：ModelSpace / PaperSpace / Block
- 价值等级：high

## 作用
创建一条由起点和终点定义的直线对象。

## 常见用法
- 在模型空间创建线
- 在布局块中创建线
- 作为几何测试对象快速验证 COM 调用链

## 典型 pywin32 写法
`doc.ModelSpace.AddLine(start_point, end_point)`

## 参数关注
- StartPoint：三维点
- EndPoint：三维点
- 点参数需符合 pywin32 可接受的数组/VARIANT 规则

## 返回
- Line 对象

## 前置条件
- 已取得活动 Document
- 已明确目标空间
- 点参数格式正确

## 常见风险
- 点坐标格式错误
- 当前对象空间理解错误
- CAD Busy 导致 COM 调用失败

## 项目内建议
- 优先走已存在的稳定包装器或统一入口
- 高风险批量创建时配合日志和重试策略
```

要求：

- 必须短、小、硬
- 不得只是原文复制
- 必须增加 pywin32 与项目内调用视角

---

## 3. 核心符号元数据：`*.meta.json`

每张核心符号卡都应配套一个元数据文件。

推荐模板：

```json
{
  "symbol": "AddLine",
  "kind": "method",
  "source_doc": "acadauto",
  "owners": ["ModelSpace", "PaperSpace", "Block"],
  "value_level": "high",
  "related_tasks": ["create_line", "geometry_smoke_test"],
  "pywin32_signature": "doc.ModelSpace.AddLine(start_point, end_point)",
  "risk_tags": ["variant_point", "space_context", "com_busy"],
  "path_md": "03_core_symbols/methods/AddLine.md"
}
```

---

## 4. 任务卡：`04_task_cards/.../*.md`

任务卡是主入口，必须说明：

- 做什么
- 优先路径
- 相关核心符号
- 处理步骤
- 常见失败
- 项目注意事项
- 验证方式

推荐模板：

```md
# 任务卡：切换到指定布局

## 目标
将当前文档切换到指定布局，并确保后续对象读取/打印操作在正确上下文中进行。

## 优先路径
1. 优先使用项目中已验证的布局切换包装函数
2. 如底层需补查，再查 ActiveLayout / Layouts / SendCommand 相关页面
3. 当 COM 切换不稳定时，记录命令回退路径

## 相关核心符号
- Document.ActiveLayout
- Layouts
- Layout
- SendCommand
- PaperSpace / ModelSpace

## 处理步骤
1. 获取当前活动文档
2. 枚举布局名并校验目标布局是否存在
3. 切换到目标布局
4. 必要时退出编辑态/命令态
5. 校验当前空间状态
6. 返回布局对象或成功标志

## 常见失败
- 布局不存在
- 当前处于命令执行状态
- COM busy
- 切换成功但空间状态未同步

## 项目注意
- 不要单凭文档写法直接落地，应优先参考项目中现有稳定函数

## 验证
- 读取当前布局名
- 校验布局枚举结果中包含目标布局
- 切换后再次读取当前布局对象或空间状态
```

---

## 5. 低频索引：`06_on_demand_index/uncommon_topics.jsonl`

用于记录暂不深加工的主题。

推荐结构：

```json
{
  "topic_id": "acadauto:LoftedSurface_StartDraftMagnitude",
  "source": "acadauto",
  "kind": "property",
  "owner": "LoftedSurface",
  "title": "StartDraftMagnitude Property",
  "keywords": ["LoftedSurface", "surface", "3d", "draft"],
  "value_level": "defer",
  "path": "01_extracted_html/acadauto/LoftedSurface_StartDraftMagnitude.htm",
  "summary": "低频高级曲面属性，当前施工图自动化主流程暂不进入核心层。"
}
```

---

## 6. pywin32 规则文档

必须建立以下跨主题规则文件：

- `pywin32_type_rules.md`
- `point_array_rules.md`
- `variant_rules.md`
- `collection_rules.md`
- `sendcommand_rules.md`
- `common_patterns.md`
- `common_failures.md`

这些文件不按单个 API 名称组织，而按跨 API 的共同难点组织。

---

## 九、首批高频任务清单

以下任务优先级最高，应先做完整任务卡：

| 优先级 | 任务名 | 是否做完整任务卡 |
|---|---|---|
| P0 | 连接 AutoCAD / 获取活动文档 | 是 |
| P0 | 打开/关闭/保存文档 | 是 |
| P0 | 获取模型空间/图纸空间/当前布局 | 是 |
| P0 | 切换到指定布局 | 是 |
| P0 | 枚举所有布局 | 是 |
| P0 | 遍历对象、读取 ObjectName/Handle/Layer | 是 |
| P0 | 构造选择集 / 选择对象 | 是 |
| P0 | 读取块属性 | 是 |
| P0 | 插入块 | 是 |
| P0 | 获取边界框/对象统计 | 是 |
| P0 | 读写系统变量 | 是 |
| P0 | SendCommand 命令回退 | 是 |
| P0 | 打印相关布局信息读取 | 是 |
| P1 | 添加直线/文字/圆/多段线 | 是 |
| P1 | 图层读取/创建/切换 | 是 |
| P1 | Regen / Zoom / Update | 是 |
| P1 | 删除/复制/移动常见对象 | 视项目需要 |
| P2 | 事件系统 | 暂缓 |
| P2 | 高级表格 | 暂缓 |
| P2 | 复杂 3D 实体/曲面 | 暂缓 |

---

## 十、Codex 的执行阶段

## 阶段 1：解包 CHM

### 目标
把 CHM 解包成 HTML 文件集合，供程序扫描。

### 输出
```text
01_extracted_html/acad_aag/
01_extracted_html/acadauto/
```

### 要求
- 只解包，不做总结
- 保留原始文件名和目录信息
- 尽量保持可追溯性

---

## 阶段 2：建立页面总清单

### 目标
扫描全部 HTML 页面，提取：

- 文件名
- 页面标题
- 可能的对象/方法/属性/事件类型
- 可能的价值等级
- 是否跳过/延后/保留

### 要求
- 先建清单，再建摘要
- 不允许在没有清单的情况下盲目大量生成文档

### 状态字段
- `keep`：进入主体系
- `defer`：延后，仅做索引
- `skip`：直接跳过

---

## 阶段 3：按规则过滤页面

### 建议过滤规则

#### 直接 `skip`
- `*_see_also.htm`
- `idx_*`
- `all_*`
- `idh_*`
- `IDH_*`

#### 先 `defer`
- `ex_*` 示例页
- 高级 3D、曲面、材质、渲染等低相关内容
- 当前业务明显不需要的冷门主题

#### 重点 `keep`
- 对象页
- 方法页
- 属性页
- 事件页
- 与布局、块、属性、选择、文档、打印、空间、系统变量、命令发送、参数格式相关的说明页

---

## 阶段 4：生成核心符号层

### 目标
从 `keep` 页面中提炼高价值符号卡。

### 要求
- 每个高价值对象/方法/属性/事件一个卡片
- 卡片必须简洁、可扫读
- 卡片必须补充 pywin32 映射说明
- 不能只是复制原文

---

## 阶段 5：生成任务卡层

### 目标
围绕项目核心工作建立任务卡。

### 要求
每个任务卡必须说明：

- 目标
- 优先路径
- 相关 API
- 处理步骤
- 项目内优先策略
- 常见失败
- 如何验证

---

## 阶段 6：建立临时查询层

### 目标
对未进入核心层的低频页面保留可搜信息。

### 要求
- 不做大面积摘要
- 只做轻量记录
- 保证以后需要时能搜到

---

## 阶段 7：建立搜索入口

### 目标
让 Codex 不必手翻文档，而是先查本地索引。

请建立：

```text
tools/search_cad_help.py
```

建议支持以下查询方式：

```bash
python search_cad_help.py task "切换布局"
python search_cad_help.py symbol "AddLine"
python search_cad_help.py keyword "block attribute"
python search_cad_help.py owner "Document"
python search_cad_help.py uncommon "plot style"
```

### 搜索结果优先级
1. 任务卡
2. 核心符号卡
3. pywin32 规则文件
4. 低频临时索引
5. 原始 HTML 路径

---

## 阶段 8：验证体系是否可用

### 目标
证明这套体系真的能指导代码，不是摆设。

### 回归验证问题
至少验证以下问题能否不翻全文而迅速定位：

- 如何获取当前活动文档
- 如何枚举所有布局
- 如何切换到指定布局
- 如何读取块属性
- 如何插入块
- 如何获得对象 Handle / ObjectName / Layer
- 如何读取当前布局打印关键参数
- 如何通过 `SendCommand` 做命令回退

### 验收标准
若 Codex 能通过：

- 正确任务卡
- 正确核心符号
- 正确 pywin32 参数规则
- 正确项目内优先路径

快速定位并给出实现方向，则体系建立成功。

---

## 十一、价值分级规则

为防止整理失控，请统一打分。

### High
满足以下任一条件：

- 当前项目高频使用
- 与布局、打印、块属性、选择、文档、对象操作强相关
- 是 pywin32 中容易出错的关键调用
- 是多个任务的共用基础对象

### Medium
具备参考价值，但不是首批核心：

- 会用到，但不是当前最常见
- 可在第二阶段补充
- 先保留索引即可

### Low
当前项目明显不常用：

- 冷门高级功能
- 当前业务不涉及
- 只保留轻量索引即可

---

## 十二、Codex 执行纪律

请严格遵守以下规则：

1. 先建索引，再建摘要，不得反过来。
2. 先做高频任务，不做全量文档抄录。
3. 页面分类必须明确 `keep / defer / skip`。
4. 遇到 `_see_also`、`idx_`、`all_`、`idh_`、`IDH_` 一类页面，默认不进入核心层。
5. 示例页 `ex_*` 默认不进入核心层，只在需要时关联到对应核心符号。
6. 所有核心符号卡必须写出 pywin32 视角下的调用关注点。
7. 所有任务卡必须优先指向项目既有稳定包装器，而不是鼓励直接写底层 COM。
8. 对冷门功能，宁可只做轻索引，不要生成大量低价值 Markdown。
9. 文档体系的主入口必须是任务卡，而不是按 CHM 目录顺序。
10. 任何新生成文件都必须服务于“更快找到可执行方法”，否则不生成。

---

## 十三、首批产物规模控制

为防止体系膨胀，首批目标建议控制为：

- `page_manifest.jsonl`：全量
- 高价值核心符号卡：**80～150 个**
- 高频任务卡：**15～30 个**
- pywin32 规则文档：**5～10 个**
- 低频临时索引：全量轻记录即可

这样可以保证：

- 覆盖主流程
- 避免几千个低价值文件
- 保持后续可扩展性

---

## 十四、当前项目最应优先覆盖的主题

### 1. 文档与空间
- 获取活动文档
- 文档打开/关闭/保存
- 模型空间/图纸空间判断
- 布局切换与布局枚举

### 2. 对象与选择
- SelectionSet
- 对象遍历
- ObjectName / Handle / Layer / BoundingBox
- 类型识别和统计

### 3. 块与属性
- 插入块
- 获取块属性
- 修改属性值
- 块引用与属性引用关系

### 4. 绘图创建
- AddLine
- AddPolyline
- AddText / AddMText
- 必要的基础几何

### 5. 打印与命令回退
- Layout / Plot 信息
- Print / Plot 相关配置
- `SendCommand` 作为不稳定或缺失 API 时的补充路径

---

## 十五、最终目标的正确理解

这套体系不是要把 Autodesk 的 CHM “重新抄写一遍”。

真正目标是：

> 把原始 CHM 转化为一个面向任务、面向 pywin32、面向本项目调用规则的本地智能检索系统。

它必须同时满足：

### 第一条：找得到
Codex 能迅速定位到任务和对应 API。

### 第二条：看得懂
Codex 能从 ActiveX 文档术语迅速映射到 Python/pywin32 写法。

### 第三条：用得对
Codex 能知道在本项目里应优先走哪个包装器、哪个稳定路径、何时命令回退、何时谨慎处理空间与 Busy 问题。

---

## 十六、建议的起步顺序

请不要一开始就生成全部卡片。

第一步只做以下四件事：

1. 解包 CHM
2. 生成 `page_manifest`
3. 建立 `keep / defer / skip` 分类规则并完成初步分类
4. 输出首批高频任务清单

完成这四件事后，再进入：

- 核心符号卡生成
- 任务卡生成
- pywin32 规则层生成
- 临时查询层生成
- 搜索入口建立
- 回归验证

---

## 十七、直接执行说明

请按以下目标开始工作：

```text
任务目标：
围绕 D:\codex-tasks\cad\official_development_document\acad_aag.chm 和 acadauto.chm，
建立一套“面向 CAD2021 + pywin32 + 本项目自动化任务”的本地文档检索体系。

核心原则：
1. 不顺序研读整本 CHM。
2. 先解包，再建 page_manifest，再分类 keep/defer/skip。
3. 只对高频高价值内容建立核心符号卡与任务卡。
4. 低频内容只做轻量索引，留作临时查询。
5. 文档主入口必须是任务卡，不是原始书本目录。
6. 所有核心卡片都要尽量映射到 pywin32 调用与本项目优先包装路径。
7. 默认跳过或降级处理 see_also、idx、all、idh、IDH、ex 等低价值或辅助页面。

首批重点任务：
- 获取活动文档
- 布局枚举与切换
- 模型/图纸空间判断
- 选择集构造与对象遍历
- 块属性读取与块插入
- 基础几何创建
- 系统变量读写
- SendCommand 回退
- 打印相关布局信息

验收标准：
Codex 能通过本地索引和任务卡，迅速定位到相应的对象、方法、属性和项目内推荐路径，
而不需要再次全文翻阅 CHM。
```

---

## 十八、最终要求

你接下来开始工作时，应以“建立检索体系”为目标，而不是以“阅读完文档”为目标。

判断每一步工作的标准只有一个：

> 是否让后续在 CAD 自动化任务中更快找到可执行的方法。

若答案是否定的，则该文件、该摘要、该分类、该加工都不应继续扩展。
