python select_print_areas_demo.py block --sample samples/block_mode_sample.dwg --lm 1000 --block-layers dy_quyu tuqian_neibu_pl
python select_print_areas_demo.py layer --sample samples/layer_mode_sample.dwg --layer-name dy_quyu
python tests/create_test_samples.py block layer
python tests/run_tests.py block layer

# select_print_areas_smart 专属资料夹

本资料夹服务于 `cad/scripts/CAD_basic.py` 中的 `select_print_areas_smart` 函数。函数用于在生成图签目录前，根据块外包盒、指定图层或屏幕选择得到打印区域多段线，按行列顺序返回。

## 快速索引

- 函数源码摘录：`select_print_areas_smart_function.txt`
- 测试脚本：`tests/run_tests.py`
- 测试样例生成：`tests/create_test_samples.py`
- 测试日志：`tests/test_log.txt`
- 样例 DWG 目标目录：`samples/`

## 运行前提

1. 按 `/jst` 规范执行，确保：
   - `cad_zt_oneb()` → `litz()` → 目标流程 → `cad_zt_oneb()`。
   - CAD 桌面仅保留天正 V9 单进程。
2. `tests/create_test_samples.py` 依赖 `CAD_basic` / `CAD_file_operations`、`insert_file_as_block`、`draw_lwpolyline` 等函数；脚本内部会自动放大插入块（最小边≥50 000）并在 `open_file` 失败时重试，确保块模式样例满足 `select_print_areas_rect_from_polylines` 的阈值。
3. 需要可写目录 `samples/`，脚本会在此生成：
   - `block_mode_sample.dwg`
   - `layer_mode_sample.dwg`

## 推荐测试顺序

1. `python tests/create_test_samples.py`：生成两份样例 DWG；若已有旧文件，会先删除再重建。
2. `python select_print_areas_demo.py block …` / `python select_print_areas_demo.py layer …`：直连函数并输出句柄，便于人工复验。
3. `python tests/run_tests.py block layer`：
   - block：验证块模式，默认对 `block_mode_sample.dwg` 调用 `select_print_areas_smart(mode="block")`。
- layer：验证图层模式，默认对 `layer_mode_sample.dwg` 调用 `select_print_areas_smart(mode="layer", layer_name="dy_quyu")`。
- 运行结果与时间写入 `tests/test_log.txt`。

### 最近一次现场测试（2025-11-29 02:06-02:08）

- `python tests/run_tests.py block layer`
  - block：返回 2 个打印框，Handles `['4DE', '4DF']`
  - layer：返回 2 个打印框，Handles `['4B8', '4B9']`
  - 详见 `tests/test_log.txt`

## 注意事项

- tests 脚本不会执行屏幕模式（手动选择），按照即时对话的指示无需测试该模式。
- block 样例会在 `dy_quyu` 与 `tuqian_neibu_pl` 图层插入块，同时保留其他无关块以测试图层过滤。
- layer 样例包含闭合/未闭合/非多段线三类对象，方便验证图层模式的过滤逻辑。
- 如果需要添加新测试，请在 `tests/test_log.txt` 中补充记录，并保留生成的 DWG 于 `samples/`。
