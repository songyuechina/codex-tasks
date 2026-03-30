# 01_bootstrap_import_rules.md

版本：V2.0

## 目标

统一 `codex-tasks` 项目中的导入引导方式，确保：

1. `codex-tasks/` 文件夹可整体迁移  
2. 脚本可跨目录稳定导入基础模块  
3. 引导逻辑只由入口脚本负责，库模块保持纯净  

## 通用引导模板

```python
from pathlib import Path
import sys

def find_codex_tasks_root(p: Path) -> Path:
    cur = p.resolve()
    if cur.is_file():
        cur = cur.parent
    while True:
        if cur.name.lower() == "codex-tasks":
            return cur
        if cur.parent == cur:
            raise RuntimeError("找不到根目录 codex-tasks")
        cur = cur.parent

root = find_codex_tasks_root(Path(__file__))
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "cad"))
```

## 适用范围

允许使用通用引导模板的对象：
- 入口脚本
- 测试脚本
- agent 启动脚本
- 独立守护脚本

不应自行写引导的对象：
- `cad/system` 内的库模块
- 通用业务模块
- 纯配置模块
- 纯工具模块

## 强制规则

1. import 环境由入口脚本负责  
2. 库模块内部禁止修改 `sys.path`  
3. 禁止在多个模块中重复写不同形式的引导逻辑  
4. 禁止使用相对路径硬编码替代引导逻辑  

## 当前系统现状说明

`cad/system` 中部分历史脚本仍带有旧式引导代码。  
这些旧式引导属于历史兼容痕迹，不是未来标准。

未来收束方向：
- 新写脚本：遵守本规则
- 旧脚本：在不破坏稳定性的前提下逐步去除内部引导
- `project_setup.py` 不再承担引导职责

## 禁止行为

- 库模块内部修改 `sys.path`
- 在多个模块中写不同版本的“找根目录”逻辑
- 让 `project_setup.py` 重新承担导入引导职责
- 用局部相对路径硬编码替代引导规则
