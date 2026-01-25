# -*- coding: utf-8 -*-
# 文件位置: D:/claude-tasks/cad/system/project_setup.py
import sys
import os
from pathlib import Path

"""
#  引导代码 (确保能找到 system)
import os
import sys
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))
from system.project_setup import PathConfig

userpath=os.environ.get('USERPATH')

# ================= 2.5 [新增] 核心连接模块导入 =================
try:
    from system import licad

    from system.licad import C
    from   system.CAD_com_utils  import SafeCOM,retry_on_busy ,retry_if_busy 

    from system.common_logger import sys_logger

    from system.CAD_coordination import CADGuard



"""
# ==========================================
# 1. 核心锚点定位 (不管这个文件被谁引用，__file__ 永远指向它自己)
# ==========================================
# 假设结构是:
# D:/claude-tasks/cad/  <-- 项目根目录 (Project Root)
#       ├── system/     <-- 当前文件所在
#       ├── scripts/
#       └── tests/

CURRENT_FILE = Path(__file__).resolve()
SYSTEM_DIR = CURRENT_FILE.parent        # .../cad/system
PROJECT_ROOT = SYSTEM_DIR.parent        # .../cad  (这就是项目的根节点)

# ==========================================
# 2. 实现“自由导入”的关键魔法
# ==========================================
# 将项目根目录添加到 Python 的搜索路径 (sys.path)
# 这样，你在任何脚本里都可以直接写: from system import common_logger
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    # print(f"🚀 已将项目根目录加入搜索路径: {PROJECT_ROOT}")

# ==========================================
# 3. 导出常用的绝对路径 (供其他脚本直接使用)
# ==========================================
class PathConfig:
    ROOT = PROJECT_ROOT
    SYSTEM_DIR = SYSTEM_DIR
    SCRIPTS_DIR = PROJECT_ROOT / "scripts"
    TESTS = PROJECT_ROOT / "tests"
    LOGS = SYSTEM_DIR / "logs"
    CAD_DIR = SCRIPTS_DIR.parent 
   

    _user_env = os.environ.get('USERPATH')
        
    if _user_env:
        # 必须用 Path() 包裹，否则后面不能用 / 拼接
        userpath = Path(_user_env) 
    else:
        # Fallback 默认值 (也要 Path 对象)
        userpath = Path("D:/Mypro/基础服务/用户1")



    # 甚至可以定义具体的通用文件路径
    TEST_EXCEL = TESTS / "testfunc.xlsx"
    COMMON_LOGGER = SYSTEM_DIR / "common_logger.py"
    WORKSPACE_DIR = CAD_DIR.parent               # .../claude-tasks



# 自动创建必要的文件夹
for p in [PathConfig.LOGS, PathConfig.TESTS]:
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
