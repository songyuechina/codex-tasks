# Variant Rules

## 何时需要关注 Variant

当 CHM 写出 `Variant`、`Variant (three-element array of doubles)`、`SAFEARRAY` 时，不能只按字符串理解。

## 当前项目里的经验

- 简单点参数很多时候直接传 Python 三元组即可
- 更敏感的低层测试可参考 `licad.py` 中 `VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (...))`
- Busy/Rejected 常常看起来像类型错误，先别误判

## 处理顺序

1. 先查项目现有包装器是否已处理
2. 再查核心符号卡的 pywin32 写法
3. 最后才手写 `VARIANT`
