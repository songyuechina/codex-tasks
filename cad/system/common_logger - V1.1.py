# -*- coding: utf-8 -*-
# 文件位置: D:/claude-tasks/cad/system/common_logger.py
# 版本: V1.1 (增强 Windows 控制台兼容性)

import os
import sys
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file="system_run.log"):
    """
    配置全局唯一的日志记录器
    """
    logger = logging.getLogger("CAD_System")
    logger.setLevel(logging.INFO)

    # 防止重复添加 Handler (避免日志重复打印)
    if logger.handlers:
        return logger

    # 1. 定义格式: 时间 - 级别 - 文件名:行号 - 消息
    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 2. 文件输出 (自动保存在本脚本同级目录下)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # [优化] 确保目录存在（虽然获取的是当前目录，但为了健壮性）
    if not os.path.exists(current_dir):
        os.makedirs(current_dir, exist_ok=True)
        
    log_path = os.path.join(current_dir, log_file)
    
    try:
        # 5MB 一个文件，最多保留 3 个备份
        file_handler = RotatingFileHandler(
            log_path, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"❌ 无法创建日志文件 handler: {e}")

    # 3. 控制台输出
    # [优化] 解决 Windows 控制台中文输出可能崩溃的问题
    try:
        # 尝试强制设置 stdout 为 utf-8 (Python 3.7+)
        if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

    console_handler = logging.StreamHandler(sys.stdout) 
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# 全局单例
sys_logger = setup_logger()

# 简单的自测代码
if __name__ == "__main__":
    sys_logger.info("✅ 日志系统初始化完成")
    sys_logger.warning("⚠️ 这是一条警告测试")
    sys_logger.error("❌ 这是一条错误测试")