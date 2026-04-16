# CAD 官方开发文档体系第二轮修正任务书（供 Codex 直接执行）

## 一、任务定位

本任务仅针对：

```text
D:\codex-tasks\cad\official_development_document
```

当前这套体系已经形成 **CAD 官方开发文档本地检索底座 v1**，方向基本成立。第二轮工作的目标，不是继续大规模扩写说明文档，也不是追求“覆盖全部 CHM 页面”，而是要让这套体系更稳定、更精确、更适合 **CAD 施工图自动化、打印、编目录、插图签** 相关任务。

**本轮目标：**

1. 补齐对当前业务真正关键的空缺。
2. 强化“任务 -> 项目稳定实现路径”的落地能力。
3. 减少关键构建脚本中的纯手工硬编码。
4. 强化验证层，避免索引存在但路径失真、映射失真。
5. 明确收缩范围：不重要、不常用、与当前业务弱相关的内容不深入。

---

## 二、范围边界

### 2.1 本轮必须服务的业务范围

本轮只围绕以下四类业务增强文档体系：

- CAD 施工图自动化
- 打印 / 布局输出
- 编目录
- 插图签 / 图签属性处理

### 2.2 本轮不深入的内容

以下内容默认不作为本轮重点，不要投入大量精力：

- 高级 3D 实体建模
- 曲面、放样、材质、渲染、视觉样式
- 冷门事件系统
- 与当前施工图主业务明显无关的高级表格格式化
- 大量低价值示例页全文摘录
- 追求“所有 CHM 页面都变成核心卡片”

### 2.3 本轮工作重心

本轮不是“多写文档”，而是：

- **补关键结构化入口**
- **增强索引到项目实现的映射**
- **加强自动检查**
- **减少后续维护成本**

---

## 三、对当前成果的判断（作为第二轮起点）

当前第一轮成果已经成立的部分：

1. 主骨架已从中文检索转向结构化精确入口：
   - `task_id`
   - `symbol`
   - `owner`
   - `project_function`
   - `module_path`
2. `04_task_cards/` 已成为主入口。
3. `03_core_symbols/` 已有一批高价值对象/方法/属性卡。
4. `05_pywin32_bridge/` 已单独抽出 pywin32 规则层。
5. 中文检索已降级为 alias 辅助层。
6. 已开始将官方符号映射到项目路径。

当前最关键的问题：

1. `system_variables/` 为空。
2. `types_and_variants/` 为空。
3. `build_core_symbols.py` 仍然主要依赖静态手工列表。
4. `build_task_cards.py` 仍然主要依赖静态任务表。
5. `validate_doc_system.py` 仍偏重数量检查，缺少路径真实性与映射真实性校验。
6. 部分 keep/defer/skip 仍偏保守，且主题页较多、精确符号页偏少。

---

## 四、本轮总原则

### 原则 1：只补关键，不追求铺满

本轮要优先补足对施工图自动化最有价值的层，而不是扩充大量一般性内容。

### 原则 2：任务主入口优先于文档完整性

判断成果是否成功，不看是否“整理了很多内容”，而看：

> Codex 是否能更快从任务落到项目内稳定实现路径。

### 原则 3：结构化优先于长篇说明

能用 `json/jsonl/meta` 表达清楚的，不必写成长篇文字。长篇 Markdown 只保留在必要位置。

### 原则 4：减少硬编码，但不盲目追求全自动

本轮应采用：

> **静态种子 + manifest 辅助扩展 + 项目扫描补强**

而不是：

- 继续完全手工硬编码全部对象/任务
- 或一次性激进改成全自动，导致失控

### 原则 5：验证必须从“数量正确”升级到“路径和映射真实”

---

## 五、本轮四大核心任务

# 任务 A：补齐 `system_variables` 层

## A.1 目标

在：

```text
03_core_symbols/system_variables/
```

建立一批对施工图自动化最关键的系统变量卡和结构化元数据。

## A.2 第一批必须纳入的系统变量

优先处理以下变量：

- `TILEMODE`
- `CTAB`
- `CMDACTIVE`
- `FILEDIA`
- `CMDECHO`
- `LTSCALE`（如与打印/比例存在关联）
- `TEXTSTYLE`（如与图签/文字有关联）
- `CLAYER`（如与插图签/绘制对象有关联）

如发现当前项目高频还依赖其他系统变量，可补充，但必须与当前业务直接相关。

## A.3 每个系统变量卡应包含

### Markdown 卡

建议文件命名：

```text
03_core_symbols/system_variables/TILEMODE.md
```

内容应简洁，包含：

- 变量名
- 含义
- 对施工图自动化的直接影响
- 常见使用场景
- 典型读写方式（通过 `GetVariable/SetVariable`）
- 常见风险
- 项目内相关函数/模块

### meta.json

建议文件命名：

```text
03_core_symbols/system_variables/TILEMODE.meta.json
```

建议字段：

```json
{
  "symbol": "TILEMODE",
  "kind": "system_variable",
  "source_doc": "acadauto",
  "value_level": "high",
  "related_tasks": [
    "determine_space_and_layout",
    "switch_to_target_layout",
    "execute_layout_plot"
  ],
  "access_via": ["GetVariable", "SetVariable"],
  "project_refs": [
    "cad/system/CAD_coordination.py",
    "cad/system/CAD_file_operations.py"
  ],
  "risk_tags": ["space_context", "state_switch"]
}
```

## A.4 目标结果

`system_variables/` 不再为空，并且真正服务布局、打印、图签、目录相关任务。

---

# 任务 B：补齐 `types_and_variants` 层

## B.1 目标

在：

```text
03_core_symbols/types_and_variants/
```

建立对 pywin32 控制 CAD 最容易出错、但又最关键的参数/返回值规则卡。

## B.2 第一批必须纳入的主题

优先建立以下主题卡：

- `3d_point`
- `2d_point`
- `variant_array`
- `safearray`
- `collection_iteration`
- `bounding_box_tuple`
- `object_return_type`
- `text_string_encoding`（如实际项目中有中文文字写入问题，可酌情加入）

## B.3 每个主题卡应包含

- 主题名
- 在 AutoCAD ActiveX / pywin32 中的典型表现
- Python 侧推荐写法
- 常见错误写法
- 对哪些高频方法/属性直接相关
- 项目中推荐的统一处理入口

## B.4 与 `05_pywin32_bridge` 的关系

`05_pywin32_bridge/` 继续保留为规则说明层；
`03_core_symbols/types_and_variants/` 则作为**结构化可索引入口层**。

也就是说：

- `05_pywin32_bridge` = 横向规则解释
- `types_and_variants` = 可被搜索脚本直接命中的结构化主题卡

## B.5 目标结果

Codex 在遇到点坐标、数组、Variant、集合返回、外包盒等问题时，不必先读长文档，而能直接命中结构化入口。

---

# 任务 C：减少 `build_core_symbols.py` 与 `build_task_cards.py` 的纯手工硬编码

## C.1 目标

保留当前可控性，但把构建方式从：

> 纯静态列表

升级为：

> 静态种子 + manifest 辅助扩展 + 项目扫描补强

## C.2 对 `build_core_symbols.py` 的要求

当前存在的问题：核心符号主要由静态列表手工定义。

本轮要求：

### 第一步：保留现有静态种子列表
不要推倒重来。

### 第二步：新增“候选符号发现”机制
从以下来源提取候选项：

1. `02_manifest/page_manifest.jsonl`
2. `02_manifest/value_ranking.jsonl`
3. `04_task_cards/task_index.json`
4. 项目映射文件（如 `07_validation/task_to_existing_code_map.json`）

### 第三步：建立候选规则
例如：

- 标题中包含 `Method` / `Property` / `Object`
- 名称与高频任务相关：layout / plot / block / attribute / selection / text / layer / variable
- 已在任务卡中被引用但尚未进入核心符号层

### 第四步：新增候选输出
生成类似：

```text
02_manifest/core_symbol_candidates.jsonl
```

字段建议包括：

- `symbol`
- `kind_guess`
- `owner_guess`
- `source_topic_id`
- `source_html_path`
- `why_selected`
- `score`
- `already_in_core`

### 第五步：核心策略
本轮不要求自动把所有候选都生成为正式卡；
但要求脚本具备：

- 自动给出候选清单
- 自动发现明显遗漏
- 降低后续全靠手工维护的压力

## C.3 对 `build_task_cards.py` 的要求

当前存在的问题：任务主要由静态表定义。

本轮要求：

### 第一步：保留现有静态任务骨架
因为当前任务范围是业务驱动的，仍需人工控制。

### 第二步：加入“任务补强信息自动聚合”
从以下来源自动补入：

- `07_validation/task_to_existing_code_map.json`
- `03_core_symbols/**/*.meta.json`
- `05_pywin32_bridge/*.md`
- `06_on_demand_index/topic_path_map.json`

### 第三步：自动校验任务引用
每张任务卡最终都应能映射到：

- `task_id`
- 至少一个核心符号
- 至少一个项目内实现路径或函数
- 至少一个 pywin32 规则文档（如适用）

### 第四步：增强 task_index.json
在不破坏现有结构的前提下，可考虑新增：

- `source_topic_ids`
- `source_html_paths`
- `project_refs`
- `rule_refs`
- `reference_dwgs`
- `stability_level`

---

# 任务 D：升级 `validate_doc_system.py`

## D.1 目标

把验证从“数量检查”升级到“真实性检查 + 一致性检查 + 可落地性检查”。

## D.2 必须新增的验证项

### 1. 路径真实性验证
检查以下路径是否真实存在：

- `task_index.json` 中的 `module_path`
- `project_refs`
- `rule_refs`
- `reference_dwgs`
- `core_symbol.meta.json` 中的 `path_md`
- `source_html_paths`

### 2. 映射一致性验证
例如：

- `task_index.json` 中引用的任务卡文件是否存在
- 每张任务卡的 `task_id` 是否能在 `task_index.json` 找到
- `task_index.json` 里引用的 symbol 是否真的存在对应 `meta.json`
- `core_symbol.meta.json` 的 `related_tasks` 是否真的存在

### 3. 项目函数存在性验证
当 `project_function` 与 `module_path` 同时存在时，至少做轻量校验：

- 目标文件存在
- 文件文本中能找到对应函数名或显著符号名

无需本轮做复杂 AST 分析，但不能只做字符串存在性空转。

### 4. 来源追踪验证
如果 `source_topic_ids` 或 `source_html_paths` 被加入，则要校验：

- topic_id 是否能在 manifest 中找到
- html_path 是否真实存在

### 5. 结构覆盖率提示
验证结果除报错外，还应给出提示：

- `system_variables` 当前条数
- `types_and_variants` 当前条数
- 被任务卡引用但尚未进入核心符号层的候选数

## D.3 验证输出要求

验证输出不要只给“通过/失败”，应当可区分：

- 致命错误（必须修）
- 非致命不一致（建议修）
- 结构缺口提示（后续补）

---

## 六、第二轮必须关注的高频任务主题

本轮新增或增强内容时，只优先围绕以下任务主题：

### 6.1 布局与空间

- 判断当前模型/图纸空间
- 枚举布局
- 切换布局
- 布局状态与系统变量联动

### 6.2 打印与输出

- 读取布局打印信息
- 构建打印计划
- 执行布局输出
- 打印前的关键上下文检查

### 6.3 图签与属性

- 插入图签
- 获取图签属性
- 更新图签字段
- 块引用 / 属性引用关系

### 6.4 编目录

- 目录生成与更新
- 遍历对象与读取标识信息
- 与图签/块属性/布局之间的联动

### 6.5 基础对象识别与检索

- `ObjectName`
- `Handle`
- `Layer`
- `BoundingBox`
- 选择集

---

## 七、本轮不应扩展的方向

以下方向如非必要，不要投入：

1. 不新增大量 3D、曲面、材质、渲染相关卡片。
2. 不把所有 `defer` 页面强行升级为核心卡片。
3. 不为了“页数好看”生成大量低价值 Markdown。
4. 不把中文 alias 再抬回主骨架。
5. 不把任务系统做成人类说明书式的长篇叙述。
6. 不在本轮引入复杂、不可控的全自动语义分类器。

---

## 八、需要修改或新增的重点文件

### 8.1 重点修改

- `tools/build_core_symbols.py`
- `tools/build_task_cards.py`
- `tools/validate_doc_system.py`
- `README.md`
- `00_readme/README_Codex_Workflow.md`
- `00_readme/README_File_Formats.md`

### 8.2 重点新增

- `03_core_symbols/system_variables/*.md`
- `03_core_symbols/system_variables/*.meta.json`
- `03_core_symbols/types_and_variants/*.md`
- `03_core_symbols/types_and_variants/*.meta.json`
- `02_manifest/core_symbol_candidates.jsonl`
- 如需要，可新增：
  - `02_manifest/system_variable_candidates.jsonl`
  - `02_manifest/type_variant_candidates.jsonl`

### 8.3 可选新增

- `07_validation/validation_report_schema.json`
- `07_validation/source_trace_index.json`

---

## 九、推荐执行顺序

请严格按以下顺序推进，不要乱序扩展。

### 第 1 步：补结构空缺
先补：

- `system_variables/`
- `types_and_variants/`

至少形成第一批可用卡片。

### 第 2 步：增强 meta 字段
给新增及已有核心卡补充必要来源追踪字段：

- `source_topic_ids`
- `source_html_paths`
- `project_refs`
- `rule_refs`

### 第 3 步：改 `build_core_symbols.py`
先实现候选发现与候选输出，不要急于全自动正式生成。

### 第 4 步：改 `build_task_cards.py`
让任务卡与 `task_index.json` 自动补强更多结构字段。

### 第 5 步：升级 `validate_doc_system.py`
先把路径真实性和映射一致性校验补齐。

### 第 6 步：回跑验证
至少执行：

```bash
py -3 .\tools\build_manifest.py
py -3 .\tools\build_core_symbols.py
py -3 .\tools\build_task_cards.py
py -3 .\tools\validate_doc_system.py
```

并新增若干针对新入口的检索验证。

---

## 十、检索与验证样例要求

第二轮完成后，至少应能稳定支持以下检索和验证：

### 10.1 精确入口

```bash
py -3 .\tools\search_cad_help.py task_id CAD2021-TASK-005
py -3 .\tools\search_cad_help.py symbol ActiveLayout
py -3 .\tools\search_cad_help.py function switch_to_layout
py -3 .\tools\search_cad_help.py module cad/system/CAD_file_operations.py
```

### 10.2 新增结构入口

```bash
py -3 .\tools\search_cad_help.py symbol TILEMODE
py -3 .\tools\search_cad_help.py symbol CMDACTIVE
py -3 .\tools\search_cad_help.py symbol 3d_point
py -3 .\tools\search_cad_help.py symbol variant_array
```

### 10.3 辅助意图入口

```bash
py -3 .\tools\search_cad_help.py task "switch target layout"
py -3 .\tools\search_cad_help.py task "read block attributes"
py -3 .\tools\search_cad_help.py task "execute layout plot"
py -3 .\tools\search_cad_help.py task "更新图签字段"
```

### 10.4 验证脚本至少应能发现以下问题

- `task_index.json` 中有路径不存在
- 任务卡引用的符号不存在
- `project_function` 找不到对应文件或文件中找不到函数名
- `source_html_paths` 指向丢失页面
- `system_variables` 或 `types_and_variants` 仍为空

---

## 十一、完成标准

本轮完成标准不是“多生成多少文件”，而是同时满足下面几条：

### 标准 1：结构空缺补上
- `system_variables/` 不再为空
- `types_and_variants/` 不再为空

### 标准 2：检索更实用
Codex 在处理布局、打印、图签、目录相关问题时，能更快命中：

- 任务入口
- 核心符号入口
- 系统变量入口
- pywin32 参数规则入口
- 项目稳定实现路径

### 标准 3：验证更严格
`validate_doc_system.py` 能检查路径真实性、映射一致性、函数存在性，而不只是文件数量。

### 标准 4：硬编码压力下降
虽然仍保留静态种子，但构建脚本已经具备候选发现与自动补强能力。

### 标准 5：不跑偏
第二轮成果没有把重心带去不重要的 3D/渲染/材质等方向。

---

## 十二、禁止事项

1. 禁止把本轮变成大规模 Markdown 扩写工程。
2. 禁止把低价值 defer 页面大量升级为核心卡。
3. 禁止把中文查询重新抬为主骨架。
4. 禁止为了“自动化”而引入过重、不可控的复杂系统。
5. 禁止脱离当前项目主业务去扩展冷门功能。

---

## 十三、交付物清单

本轮至少应交付：

1. 更新后的：
   - `tools/build_core_symbols.py`
   - `tools/build_task_cards.py`
   - `tools/validate_doc_system.py`
2. 新增的：
   - `03_core_symbols/system_variables/` 首批卡片
   - `03_core_symbols/types_and_variants/` 首批卡片
   - `02_manifest/core_symbol_candidates.jsonl`
3. 更新后的：
   - `04_task_cards/task_index.json`
   - `README.md`
   - `00_readme/README_Codex_Workflow.md`
   - `00_readme/README_File_Formats.md`
4. 一份简短的本轮结果说明：
   - 新增了哪些高价值入口
   - 增强了哪些验证项
   - 仍然保留哪些后续缺口

---

## 十四、Codex 最后执行提醒

请始终记住：

> 这套体系不是为了让人类“看起来更完整”，而是为了让 Codex 在 CAD 施工图自动化、打印、编目录、插图签相关任务中，能更快从任务落到项目内稳定实现路径。

因此，本轮必须坚持：

- 任务导向
- 业务收缩
- 结构化优先
- 来源可追踪
- 验证可落地
- 少而硬，不要泛而多

