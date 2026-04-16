# SendCommand Rules

## 定位

`SendCommand` 是保底回退，不是默认首选。

## 当前项目优先路径

1. 优先走 `system.licad.C.doc`
2. 优先走 `CAD_core.py`、`CAD_selection.py`、`print/` 内已有稳定函数
3. 只有 COM 直接切换/设置不稳定时，再考虑 `SendCommand`

## 已有工程经验

- `SafeDocumentWrapper.SendCommand` 会尽量转到同步安全调用
- `CAD_coordination.send_cmd_with_sync()` 是推荐的同步命令路径
- 布局切换、窗口缩放、选择集回退都已有 `SendCommand` 实战经验

## 风险

- 命令发到错误上下文
- 当前仍处于命令态
- 命令串执行后未等待完成
- 新命令覆盖旧命令
