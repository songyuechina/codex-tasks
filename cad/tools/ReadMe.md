function_analyzer.py是核心之一，意图将具体的函数代码转换为虚的结构分解并保存在数据库中。同时将函数表达为文本、结构图等。
spec_to_text.py：虚 → 文本影子（压缩展示）

spec_to_mermaid.py：虚 → 图（展示）

spec_to_stub.py：虚 → 代码壳（占位）

virtual_to_code.py：只是把上面的 stub 生成串起来

unction_analyzer.py（你那份 V2.x 版）

从真实代码里提取：源码片段、AST calls、分支/循环痕迹

再用 API（LLM）做“语义流程分析”，产出结构化 analysis JSON

生成“函数调用合同 contract”（inputs/outputs/side_effects/safe_usage_notes）

把这些“虚”的结果落库（CAD_FUNCINFO.function_analysis），并做缓存层（local_ok / db / local_failed / api）

这就是：实代码 → 虚分析 → 可复用知识资产（DB/缓存）

code_to_spec.py

直接从代码 AST 抽一个“spec YAML”的雏形：输入参数/默认值、calls 依赖、控制流占位、步骤占位

相当于：实代码 → spec（虚结构）

code_to_virtual.py

把上面链路串起来：code -> spec -> mermaid(mmd) -> markdown(md) -> png(可选)

本质是把“虚资产”一次性生成成多种可视化/可阅读形式（spec/mmd/md/png）

spec_code_consistency.py

把 spec 反过来和代码对齐检查（参数、默认值、依赖 calls、行号、return、CAD 模块引用弱校验）

这相当于给“实→虚”这条路加了一道一致性约束，防止 spec 漂移














