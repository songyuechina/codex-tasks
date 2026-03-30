#&&% 模拟键盘调整打印图幅

from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import pyautogui


current = Path(__file__).resolve()
project_root = current.parent.parent.parent
cad_root = project_root / "cad"
if str(cad_root) not in sys.path:
    sys.path.insert(0, str(cad_root))

from system.common_logger import sys_logger


def _status(text: str) -> None:
    print(text, end="\r", flush=True)


def _line(text: str = "") -> None:
    print(text, flush=True)


# =============================================================================
# 1. 核心算法：带“防粘连”的双阶段捕获
# =============================================================================
def get_mouse_target_v3(step_idx, total_steps, prompt_text, prev_pos=None, dwell_time=2.0):
    """
    参数:
    - step_idx: 当前步骤序号
    - total_steps: 总步骤数
    - prev_pos: 上一步录入的坐标 (用于判断是否位置重叠)
    """
    step_str = f"[第 {step_idx}/{total_steps} 步]"
    _line()
    _line(f"🔹 {step_str} 目标: {prompt_text}")
    
    # --- 阶段 0: 防粘连检测 (Anti-Stick) ---
    # 如果上一步就在这儿，用户可能根本不动鼠标。
    # 强制要求用户移开，确保程序能检测到"为了当前步骤而做的新动作"。
    if prev_pos is not None:
        curr_x, curr_y = pyautogui.position()
        dist_from_prev = math.sqrt((curr_x - prev_pos[0])**2 + (curr_y - prev_pos[1])**2)
        
        # 如果距离上一步的位置小于 50 像素，提示移开
        if dist_from_prev < 50:
            _status("   ⚠️  检测到鼠标仍在原位！请【移开鼠标再移回来】以激活此步骤...   ")
            while True:
                curr_x, curr_y = pyautogui.position()
                dist_now = math.sqrt((curr_x - prev_pos[0])**2 + (curr_y - prev_pos[1])**2)
                if dist_now > 50: # 用户移开了
                    break
                time.sleep(0.1)

    # --- 阶段 1: 唤醒检测 (等待移动) ---
    _status("   👁️  请移动鼠标去操作/寻找目标...                        ")
    start_x, start_y = pyautogui.position()
    
    while True:
        curr_x, curr_y = pyautogui.position()
        dist = math.sqrt((curr_x - start_x)**2 + (curr_y - start_y)**2)
        
        if dist > 10: # 检测到移动
            break
        time.sleep(0.1)

    # --- 阶段 2: 驻留锁定 ---
    _status(f"   🚀 已激活！请在目标位置【松手静止 {dwell_time} 秒】...         ")
    
    last_x, last_y = pyautogui.position()
    stable_start_time = None
    
    while True:
        curr_x, curr_y = pyautogui.position()
        dist = math.sqrt((curr_x - last_x)**2 + (curr_y - last_y)**2)
        
        # 5像素容差
        if dist < 5:
            if stable_start_time is None:
                stable_start_time = time.time()
            
            elapsed = time.time() - stable_start_time
            
            # 进度条
            progress = int((elapsed / dwell_time) * 10)
            bar = "█" * progress + "░" * (10 - progress)
            _status(f"   ⏳ 正在锁定 {step_str}: {bar} {elapsed:.1f}s | 坐标:({curr_x}, {curr_y})")
            
            if elapsed >= dwell_time:
                # --- 核心改进：即时反馈 ---
                _line(f"   ✅ {step_str} 【{prompt_text.split(':')[0]}】 录入成功！坐标:({curr_x}, {curr_y})      ")
                print('\a') # 提示音
                return (curr_x, curr_y)
        else:
            stable_start_time = None
            last_x, last_y = curr_x, curr_y
            _status(f"   🖱️  寻找中... 当前坐标:({curr_x}, {curr_y})，请在 {prompt_text[:10]}... 处停住      ")
            
        time.sleep(0.1)

# =============================================================================
# 2. 安全输入逻辑
# =============================================================================
def safe_input_text(coords, text, desc="输入"):
    pyautogui.click(coords)
    time.sleep(0.5) 
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.press('delete')
    time.sleep(0.3)
    pyautogui.write(str(text), interval=0.1)
    # sys_logger.info(f"      ...{desc}: {text}") # 减少刷屏，保持清爽
    time.sleep(1.0) 

# =============================================================================
# 3. 主流程
# =============================================================================
def auto_setup_custom_paper_sizes(data_list):

    """
    auto_setup_custom_paper_sizes(dy_yonghu)

    """

    pyautogui.FAILSAFE = True 
    coords = {}

    print("\n" + "="*70)
    print("🛠️  CAD 批量助手 (终极防呆版)")
    print("="*70)
    
    # --- 关键前置提醒 ---
    print("❗❗❗ 【操作前必读 - 避免数据错误】 ❗❗❗")
    print("1. 打印机必须选为: DWG TO PDF.pc3")
    print("2. 基础图幅必须选择: ISO A1 (594.00 x 841.00 MM) 或其他【MM单位】图幅！")
    print("   ❌ 切勿选择 Inches (英寸) 单位的图幅，否则输入的数据会全部错误。")
    print("3. 【同位置操作提醒】: 如果连续两步按钮位置相同（如连续点“下一步”）：")
    print("   👉 必须先将鼠标【移开】一段距离，然后再【移回来】悬停，程序才能识别。")
    print("-" * 70)
    
    input("👉 确认已理解上述 3 点？按【回车】开始录入流程...")

    # --- 录入步骤定义 ---
    steps_map = [
        ("btn_props",      "特性按钮: 点击【特性(R)】"),
        ("tab_custom",     "选项卡: 点击【自定义图纸尺寸】"), 
        ("btn_add",        "添加按钮: 点击【添加(A)】"),
        ("btn_next_1",     "向导1: 点击【下一步(N)】 (开始)"),
        ("input_width",    "宽度框: 点击【宽度(W)】输入区域"),
        ("input_height",   "高度框: 点击【高度(E)】输入区域"),
        ("btn_next_2",     "向导2: 点击【下一步(N)】 (宽高页)"),
        ("input_top",      "上边距: 点击【上(T)】输入区域"),
        ("input_bottom",   "下边距: 点击【下(O)】输入区域"),
        ("input_left",     "左边距: 点击【左(L)】输入区域"),
        ("input_right",    "右边距: 点击【右(R)】输入区域"),
        ("btn_next_3",     "向导3: 点击【下一步(N)】 (边距页)"),
        ("btn_next_4",     "向导4: 点击【下一步(N)】 (跳过改名)"),
        ("btn_finish",     "完成按钮: 点击【完成】"),
        ("btn_ok",         "确定按钮: 点击底部的【确定】")
    ]

    # --- 循环录入 ---
    total = len(steps_map)
    prev_coordinate = None # 用于记录上一步的坐标

    for idx, (key, prompt) in enumerate(steps_map, 1):
        # 调用 V3 版捕获函数
        current_coord = get_mouse_target_v3(
            step_idx=idx, 
            total_steps=total, 
            prompt_text=prompt, 
            prev_pos=prev_coordinate, # 传入上一步坐标用于防粘连
            dwell_time=2.0
        )
        
        coords[key] = current_coord
        prev_coordinate = current_coord # 更新上一步坐标
        time.sleep(0.5) 

    print("\n🎉 坐标校准全部完成！请将鼠标移至安全区域，3秒后自动执行...")
    time.sleep(3)

    # --- 批量执行 ---
    CLICK_WAIT = 1.0
    WINDOW_WAIT = 2.0
    
    print("\n🚀 开始批量写入数据...")

    for i, item in enumerate(data_list):
        w, h, t, b, l, r = item
        _line(f"[{i+1}/{len(data_list)}] 正在写入: {w} x {h}")

        try:
            # 1. 特性
            pyautogui.click(coords["btn_props"])
            time.sleep(WINDOW_WAIT) 
            # 2. 选项卡
            pyautogui.click(coords["tab_custom"])
            time.sleep(CLICK_WAIT)
            # 3. 添加
            pyautogui.click(coords["btn_add"])
            time.sleep(CLICK_WAIT)
            # 4. 下一步
            pyautogui.click(coords["btn_next_1"])
            time.sleep(CLICK_WAIT)
            # 5. 宽高
            safe_input_text(coords["input_width"], w, "宽度")
            safe_input_text(coords["input_height"], h, "高度")
            # 下一步
            pyautogui.click(coords["btn_next_2"])
            time.sleep(CLICK_WAIT)
            # 6. 边距
            safe_input_text(coords["input_top"], t, "上边距")
            safe_input_text(coords["input_bottom"], b, "下边距")
            safe_input_text(coords["input_left"], l, "左边距")
            safe_input_text(coords["input_right"], r, "右边距")
            # 下一步
            pyautogui.click(coords["btn_next_3"])
            time.sleep(CLICK_WAIT)
            # 下一步
            pyautogui.click(coords["btn_next_4"])
            time.sleep(CLICK_WAIT)
            # 完成
            pyautogui.click(coords["btn_finish"])
            time.sleep(CLICK_WAIT)
            # 确定
            pyautogui.click(coords["btn_ok"])
            
            # PMP 保存处理
            time.sleep(WINDOW_WAIT) 
            pyautogui.press('enter') 
            time.sleep(WINDOW_WAIT) 

        except Exception as e:
            _line(f"❌ 出错: {e}")
            break

    print("\n✅ 所有图纸尺寸添加完成！")


#天正数据

dy_yonghu = [
    ("1338.00", "841.00", "0", "0", "0", "0"), 
    ("1486.00", "841.00", "0", "0", "0", "0"), 
    ("1051.00", "594.00", "0", "0", "0", "0"), 
    ("1261.00", "594.00", "0", "0", "0", "0"), 
    ("1471.00", "594.00", "0", "0", "0", "0"), 
    ("743.00", "420.00", "0", "0", "0", "0"),  
    ("891.00", "420.00", "0", "0", "0", "0"),  
    ("1041.00", "420.00", "0", "0", "0", "0")  
]


def _configure_console() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

def list_current_printer_papers(printer_name="DWG To PDF.pc3"):
    """
    列出指定打印机的所有纸张名称 (内部名 vs 显示名)
    """
    sys_logger.info(f"🔌 正在连接 AutoCAD...")
    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        doc = acad.ActiveDocument
        layout = doc.ActiveLayout
    except Exception as e:
        sys_logger.info(f"❌ 无法连接 AutoCAD: {e}")
        return

    sys_logger.info(f"⚙️ 正在切换打印机配置为: {printer_name} ...")
    try:
        # 必须先设置 ConfigName，否则获取的是默认打印机的纸张
        layout.RefreshPlotDeviceInfo()
        layout.ConfigName = printer_name
        # 再次刷新以加载该打印机的图幅列表
        layout.RefreshPlotDeviceInfo() 
    except Exception as e:
        sys_logger.info(f"❌ 设置打印机失败 (可能拼写错误或驱动不存在): {e}")
        return

    # 获取所有纸张的内部名
    canonical_names = layout.GetCanonicalMediaNames()
    
    print("\n" + "="*90)
    sys_logger.info(f"🖨️  打印机 [{printer_name}] 纸张列表侦探")
    sys_logger.info(f"📋 共发现 {len(canonical_names)} 种纸张")
    print("="*90)
    sys_logger.info(f"| {'内部名 (写代码用这个!)':<50} | {'显示名 (你在CAD里看到的)':<35} |")
    print("-" * 90)

    count = 0
    user_defined_count = 0

    for c_name in canonical_names:
        # 获取对应的本地显示名
        l_name = layout.GetLocaleMediaName(c_name)
        
        # 过滤逻辑：我们重点关注 "User" (自定义) 或 "Full bleed" (扩展)
        # 如果你想看所有纸张，把下面的 if 注释掉即可
        is_custom = "User" in c_name or "Custom" in c_name
        is_full_bleed = "full_bleed" in c_name
        
        # 这里我设置只显示 自定义纸张 和 A0/A1/A2 的扩展纸张，防止列表太长刷屏
        if is_custom or (is_full_bleed and "A0" in c_name): 
            sys_logger.info(f"| {c_name:<50} | {l_name:<35} |")
            count += 1
            if is_custom:
                user_defined_count += 1
    
    print("-" * 90)
    sys_logger.info(f"✅ 扫描结束。显示了 {count} 个相关结果。")
    sys_logger.info(f"🔍 其中包含 {user_defined_count} 个用户自定义图幅 (UserDefined)。")
    print("💡 请将左侧的【内部名】复制到你的 Python 代码中，替换掉报错的纸张名称。")



def main() -> None:
    _configure_console()
    auto_setup_custom_paper_sizes(dy_yonghu)


if __name__ == "__main__":
    main()



