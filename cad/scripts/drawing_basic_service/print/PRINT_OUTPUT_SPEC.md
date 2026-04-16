# PRINT_OUTPUT_SPEC.md

## 1. 打印主链输出规范

每次真实打印运行至少应输出：

- `print_plan.json`
- `print_summary.json`
- `pdf/`
- `pdf/named/`（当需要按打印信息生成命名副本时）

若是单文件调度任务，还应在源 DWG 同目录组织最终交付：

- `<公共名>pdf/`
- `<公共名>pdf/named/`（命名副本，可选但推荐）
- `<公共名>analysis/`
- `<公共名>prosess/`
- `<原文件名>_打印区域.dwg`

若是目录级批量任务，还应额外输出：

- `batch_summary.json`

`print_summary.json` 至少应能回答：

- 使用了什么模式
- 计划打印多少张
- 实际成功多少张
- 失败多少张
- 校验结果如何

## 2. 净化适配输出规范

若模式为 `purified_adaptive`，还必须输出：

- `content_analysis.json`
- `scope_analysis.json`（当触发伪极大范围收束时）

该文件至少应说明：

- 总候选区域数
- 被识别为伪区域的句柄
- 伪区域判定依据
- 若触发范围收束：
  - 选中了哪个伪极大范围
  - 为什么应用范围收束
  - 收束后剩余多少作业

## 3. 打印信息分析输出规范

每次打印信息分析至少应输出：

- `print_info_analysis.json`
- `print_info_analysis.xlsx`

若需要按打印信息复制并重命名最终 PDF，还应额外输出：

- `pdf/named/`

默认命名规则：

- `顺序号-项目名称-子项目名称-图纸名称-图纸编号`
- 其中图纸编号前允许再加用户给出的代号前缀，例如 `JS-`

若本次任务是一次真实打印任务，还应额外输出：

- `*_打印区域.dwg`

该副本用于人工快速检查最终保留的打印区域是否明显异常：

- 最终保留区域应改为红色
- 并按比例规则加粗

按需要可附加：

- `print_info_dict.json`

## 4. 打印信息分析 JSON 关键字段

`print_info_analysis.json` 至少应包含：

- `dwg_path`
- `analysis_dwg_path`
- `print_mode`
- `total_jobs`
- `with_title_count`
- `with_drawing_no_count`
- `with_project_count`
- `print_info_dict`

单页条目至少应包含：

- `sequence_no`
- `sequence_key`
- `page_key`
- `print_handle`
- `drawing_title`
- `drawing_no`
- `project_name`
- `subproject_name`
- `drawing_title_record_count`
- `drawing_no_record_count`
- `drawing_title_handles`
- `drawing_no_handles`
- `inner_frame_exists`
- `inner_frame_bbox`
- `graphic_info_area_bbox`
- `graphic_info_area_source`
- `graphic_orientation`
- `right_bottom_title_block_exists`
- `title_block_kind`
- `title_block_handle`
- `title_block_name`
- `title_block_bbox`
- `title_no_resolve_method`
- `title_block_texts`
- `graphic_info_text_records`
- `classified_text_records`
- `drawing_title_records`
- `drawing_no_records`
- `title_block_attr_fields`
- `analysis_stop_reason`

其中：

- `graphic_info_area_bbox`
  表示当前页用于分析图签信息的窗口区域
- `graphic_info_area_source`
  当前统一记录为角点对齐图签块外包盒来源
- `graphic_orientation`
  表示当前页按横向还是竖向口径判定图签块角点
- `title_no_resolve_method`
  表示当前页编号 / 标题命中的判定路径：
  - `layer_named`
  - `guide_rectangles`
  - `fallback_regex`
- `graphic_info_text_records`
  表示 `graphic_info_area` 内实际采样到的文字对象明细
- `classified_text_records`
  表示在整块采样文字基础上，进一步明确标注 `drawing_title / drawing_no / other` 的分类结果
- `drawing_title_records` / `drawing_no_records`
  表示最终被判定为图纸名称 / 图纸编号的文字记录

## 5. Excel 输出规范

Excel 至少包含三张表：

- `summary`
- `print_info`
- `text_records`
- `drawing_title_records`
- `drawing_no_records`

其中：

- `print_info`
  用于人工总览每张图纸
- `text_records`
  用于人工排查图签块文字采样，并看到每条文字的分类角色
- `drawing_title_records`
  用于人工直接核对每页哪些对象被判定为图纸名称
- `drawing_no_records`
  用于人工直接核对每页哪些对象被判定为图纸编号
- `summary`
  中应能看到 `with_title_count`、`with_drawing_no_count`、`title_block_found_count` 等汇总值

若后续人工排查“为什么这一页误判”，应优先对照：

1. `graphic_info_area_bbox`
2. `graphic_info_text_records`
3. `drawing_title_records`
4. `drawing_no_records`
5. `title_no_resolve_method`

## 6. 权威结果约束

同一案例若多轮运行并存，应明确：

- 哪个目录是当前权威结果
- 为什么它是权威结果

若结果只是中间态，不得宣称为权威基线。
