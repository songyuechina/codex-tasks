# AGENTS.md

适用范围：`D:/codex-tasks/cad/scripts/drawing_basic_service/compile_catalogue/`

本目录是“编目录”执行工作区。

## 工作原则

1. 打印区域、内框、图签块判断优先复用 `print/` 与 `illustration_label/` 现有能力。
2. 不再单独维护平行的打印区识别逻辑。
3. 真实 CAD 运行前必须先走 `cad/system` 的受控连接与 runtime guard。
4. 对缺失图名、图号的页面，允许在图签信息区域内补写文字，但不能绕开统一 COM 入口。
5. 目录 DWG 统一从 `directory_template/目录模板1.dwg` 复制生成，输出到 `user_directory/`。

## 当前入口

- `compile_catalogue.py`
- `compile_catalogue_service.py`

## 输出约束

至少应留下：

- 生成的 `<目标文件名>_目录.dwg`
- 可选的执行结果 JSON
