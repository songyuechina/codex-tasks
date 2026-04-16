# File Formats

## `02_manifest/page_manifest.jsonl`

全量页面清单。每行一条记录，字段包含：

- `topic_id`
- `source_doc`
- `basename`
- `title`
- `kind_guess`
- `owner_guess`
- `class_guess`
- `value_level`
- `status`
- `keywords`
- `path`
- `notes`

## `03_core_symbols/**/*.md`

高价值对象/方法/属性卡。要求：

- 短
- 可扫读
- 带 pywin32 写法
- 带项目推荐路径

## `03_core_symbols/**/*.meta.json`

核心卡元数据，供脚本和检索工具读取。

第二轮后至少应包含：

- `symbol`
- `kind`
- `project_refs`
- `rule_refs`
- `source_topic_ids`
- `source_html_paths`
- `path_md`

## `04_task_cards/**/*.md`

任务主入口。应覆盖：

- `task_id`
- `symbol / owner / project_function / module_path`
- `aliases_en`
- `aliases_zh / keywords_zh`（仅辅助）
- 目标
- 优先路径
- 相关核心符号
- 处理步骤
- 项目注意事项
- 常见失败
- 验证方式

## `04_task_cards/task_index.json`

任务结构化主索引。每条任务必须能回落到：

- `task_id`
- `symbols`
- `owners`
- `project_functions`
- `module_paths`
- `aliases_en`
- `aliases_zh`
- `keywords_zh`
- `pywin32_rules`
- `rule_refs`
- `project_refs`
- `source_topic_ids`
- `source_html_paths`
- `reference_dwgs`
- `reference_objects`
- `stability_level`

## `06_on_demand_index/uncommon_topics.jsonl`

低频主题轻量索引，仅保留可搜索信息，不做深加工。
