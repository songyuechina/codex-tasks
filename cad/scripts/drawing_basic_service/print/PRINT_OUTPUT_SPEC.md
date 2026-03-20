# PRINT_OUTPUT_SPEC.md

## 1. 打印主链输出规范

每次真实打印运行至少应输出：

- `print_plan.json`
- `print_summary.json`
- `pdf/`

若是单文件调度任务，还应在源 DWG 同目录组织最终交付：

- `<公共名>pdf/`
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
- `inner_frame_exists`
- `right_bottom_title_block_exists`
- `title_block_kind`
- `title_block_texts`
- `title_block_attr_fields`
- `analysis_stop_reason`

## 5. Excel 输出规范

Excel 至少包含三张表：

- `summary`
- `print_info`
- `text_records`

其中：

- `print_info`
  用于人工总览每张图纸
- `text_records`
  用于人工排查图签块文字采样

## 6. 权威结果约束

同一案例若多轮运行并存，应明确：

- 哪个目录是当前权威结果
- 为什么它是权威结果

若结果只是中间态，不得宣称为权威基线。
