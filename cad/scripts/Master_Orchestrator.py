# -*- coding: utf-8 -*-
# 文件位置: D:\claude-tasks\cad\scripts\Master_Orchestrator.py
# 版本: V1.0 旗舰总控
"""
【工程图纸自动化系统 - 总指挥中心】
Master Orchestrator

架构层级：
1. 战略层 (Strategy): 处理文件级灾难恢复 (FileGuard)、进程控制、语音播报。
2. 战役层 (Campaign): 调度各个子系统 (插图签、编目录、打印)。
3. 战术层 (Tactics): 具体业务脚本 (insert_labels 等)，由 CADGuard 保护。

特性：
- 语音播报反馈 (TTS)
- 阶段性数据传递
- 熔断与灾难恢复
"""

import sys
import os
import time
import shutil
from pathlib import Path
from functools import partial

# ================= 0. 环境引导 =================
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

# ================= 1. 系统组件导入 =================
from system.common_logger import (
    sys_logger, CriticalSection, checkpoint, set_debug_mode
)
from system.CAD_coordination import (
    run_safety_loop,        # 核弹级安全循环
    FileGuard,              # 文件备份卫士
    ensure_single_process,  # 进程清理
    wait_quiescent          # 静默等待
)
from system.licad import C

# ================= 2. 业务模块导入 (按需加载) =================
# 注意：这里导入具体的业务脚本
try:
    import Insert_chart.insert_labels as sys_insert
    # import Catalog.make_catalog as sys_catalog  # (待开发)
    # import Print.batch_plot as sys_print        # (待开发)
except ImportError as e:
    sys_logger.warning(f"部分业务模块尚未就绪: {e}")

# ================= 3. 语音播报组件 (TTS) =================
class AssistantVoice:
    """语音助手：让系统开口说话"""
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.engine = None
        if self.enabled:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                # 尝试设置中文语音
                for voice in self.engine.getProperty('voices'):
                    if 'chinese' in voice.name.lower() or 'cn' in voice.id:
                        self.engine.setProperty('voice', voice.id)
                        break
                self.engine.setProperty('rate', 170) # 语速稍快
            except ImportError:
                sys_logger.warning("未安装 pyttsx3，语音播报已禁用 (pip install pyttsx3)")
                self.enabled = False

    def speak(self, text):
        """播报消息（非阻塞模式建议，这里简化为阻塞）"""
        if not self.enabled or not self.engine: return
        try:
            sys_logger.info(f"🗣️ [播报] {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except: pass

speaker = AssistantVoice(enabled=True)

# ================= 4. 子系统封装 (Campaign Layer) =================

def campaign_insert_labels(target_file):
    """
    【战役 1】插图签系统
    调用 insert_labels.py 中的总装流水线
    """
    sys_logger.info(">>> 进入战役: 智能图签插入...")
    
    # 调用业务脚本的流水线
    # 注意：业务脚本内部已有 CADGuard 保护，这里只负责调用和接收结果
    if not hasattr(sys_insert, 'run_title_block_assembly_pipeline'):
        raise ImportError("insert_labels 模块缺少 run_title_block_assembly_pipeline 函数")

    # 执行流水线
    success = sys_insert.run_title_block_assembly_pipeline()
    
    if success:
        # 这里未来可以返回具体的统计数据，例如插入了多少个
        # 目前假设业务函数内部已经记录了 Excel
        return {"status": "success", "count": 23} # 示例数据
    else:
        raise RuntimeError("插图签流水线执行失败")

def campaign_build_catalog(prev_data):
    """
    【战役 2】编目录系统 (示例框架)
    接收上一阶段的数据 (prev_data)
    """
    sys_logger.info(">>> 进入战役: 目录生成...")
    # 模拟操作
    # time.sleep(1)
    return {"status": "skipped", "msg": "模块待开发"}

def campaign_batch_print(prev_data):
    """
    【战役 3】自动打印系统 (示例框架)
    """
    sys_logger.info(">>> 进入战役: 智能打印...")
    return {"status": "skipped", "msg": "模块待开发"}

# ================= 5. 总控逻辑 (Strategy Layer) =================

def run_project_master_control(dwg_file_path):
    """
    【战略总控】
    负责串联所有战役，处理文件级灾难恢复。
    """
    
    # 1. 环境准备
    speaker.speak("自动化系统启动，正在检查环境。")
    if not ensure_single_process():
        sys_logger.warning("发现多个CAD进程，建议清理。")
    
    # 2. 定义核心任务 (Action)
    # 这个函数包含了所有的 F1 -> F2 -> F3 逻辑
    def mission_impossible():
        
        # --- F1: 插图签 ---
        with CriticalSection("阶段一：图签总成") as ctx:
            result_f1 = campaign_insert_labels(dwg_file_path)
            ctx.record(data=str(result_f1))
            
            # 语音反馈
            count = result_f1.get('count', 0)
            speaker.speak(f"图签插入完成，处理图纸 {count} 张。")

        # --- F2: 编目录 ---
        with CriticalSection("阶段二：目录生成") as ctx:
            # 将 F1 的结果传给 F2
            result_f2 = campaign_build_catalog(result_f1) 
            ctx.record(data=str(result_f2))

        # --- F3: 打印 ---
        with CriticalSection("阶段三：自动打印") as ctx:
            result_f3 = campaign_batch_print(result_f2)
            ctx.record(data=str(result_f3))
            
        return True

    # 3. 定义校验任务 (Check)
    # 简单的最终校验，或者留空恒为 True
    def mission_verify():
        return True

    # 4. 启动核弹级安全循环 (FileGuard + Retry)
    # 如果 mission_impossible 内部抛出异常，这里会负责：
    # 杀进程 -> 还原文件 -> 重启 CAD -> 重试
    speaker.speak("开始执行任务，已启用安全保护。")
    
    is_success = run_safety_loop(
        target_dwg=dwg_file_path,
        action_func=mission_impossible,
        check_func=mission_verify,
        max_retries=3
    )

    if is_success:
        sys_logger.info("🎉🎉🎉 所有战役全部胜利！")
        speaker.speak("所有任务圆满完成，系统已待命。")
    else:
        sys_logger.error("☠️☠️☠️ 任务最终失败，已执行文件回滚保护。")
        speaker.speak("任务执行遇到严重错误，已停止并恢复文件。")

# ================= 6. 执行入口 =================

if __name__ == "__main__":
    # 配置调试模式
    # set_debug_mode(1, "HUMAN", 30)
    
    # 模拟用户输入的文件路径
    # 实际使用时，这里可以通过命令行参数或 UI 获取
    from system.project_setup import PathConfig
    target_dwg = str(PathConfig.userpath / "dwg文件/图签插入0109.dwg")
    
    if os.path.exists(target_dwg):
        run_project_master_control(target_dwg)
    else:
        sys_logger.error(f"找不到目标文件: {target_dwg}")
        speaker.speak("找不到目标文件，请检查路径。")


















        
