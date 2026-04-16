# TArch Operation Work State

最后更新：`2026-04-12`

本文件用于让下一个 Codex 窗口直接续接 `D:/codex-tasks/cad/library/tarch_operation/` 的当前工作，不必重新摸索。

## 已完成

1. 已建立统一外部入口：
   - `D:/codex-tasks/cad/library/tarch_operation/tarch_api.py`
2. 已完成并实测通过的函数：
   - `write_tarch_single_line_text()`
   - `write_tarch_drawing_name()`
3. 两个函数都支持：
   - 指定 `target_dwg_path`
   - 在指定的任意 DWG 文件中操作
   - 若目标 DWG 不存在，则在当前已运行的天正会话里创建后再操作
4. 图名标注函数已确认：
   - `图名样式 = TARCH_CN_STANDARD`
   - `比例样式 = TARCH_CN_STANDARD`
5. 已新增测试期监督脚本：
   - `D:/codex-tasks/cad/system/cad_test_supervisor.py`

## 当前硬规则

1. `tarch_operation` 只是业务函数层，不是 CAD 启动入口。
2. 这些函数默认假定天正 CAD 已预先启动。
3. 这些函数不允许自行启动、重建、恢复 CAD。
4. 这些函数只允许在“恰好 1 个健康天正 CAD 进程”下运行。
5. 若检测到 `0` 个 CAD 进程、`>1` 个 CAD 进程、或混入纯 CAD 进程，应直接报错并交还给外部受控入口。
6. 测试运行必须同时启动 `cad_test_supervisor.py`，并确认 `cad_dialog_killer.py` 已运行。
7. 一个测试任务完成后，应通过 `CAD_core.py` 的受控关闭入口关闭 CAD 会话。

## 本轮测试结果

1. 单行文字测试输出：
   - `D:/codex-tasks/cad/library/tarch_operation/outputs/single_line_text_guarded_test.dwg`
2. 图名标注测试输出：
   - `D:/codex-tasks/cad/library/tarch_operation/outputs/drawing_name_guarded_test.dwg`
   - `D:/codex-tasks/cad/library/tarch_operation/outputs/drawing_name_guarded_test_v2.dwg`
3. 测试期间监督结果：
   - `acad.exe` 始终为 `1`
   - `cad_dialog_killer.py` 已运行
   - `cad_test_supervisor.py` 未报告违规
4. 本轮结束时已调用 `CAD_core.close_tarch_CAD_system()` 关闭会话，当前运行态已回到 `no_active_cad`

## 调试结论

1. `D:/codex-tasks/cad/system/CAD_selection.py` 中的 `brute_dump_tarch_props(ent, max_dispid=64)` 是有效的。
2. 它已被收束为：
   - 可打印暴力扫描结果
   - 同时返回结构化结果列表
3. 当某个天正对象无法通过现有属性映射正确 `get/set` 时，应优先用它探测真实 DISPID 与值，再决定是否补充 `_TARCH_PROPERTY_MAP`。

## 下一步建议

1. 继续新增其它天正业务函数，并统一收口到 `tarch_api.py`。
2. 每新增一个函数，都保持同样的前置约束：
   - 预启动天正
   - 单进程
   - 监督陪跑测试
   - 测试后关闭 CAD
3. 若后续某类天正对象属性异常，先用 `brute_dump_tarch_props()` 取证，再补 `CAD_selection.py` 映射。
