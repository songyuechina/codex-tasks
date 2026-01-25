import time
import pyautogui
import pygetwindow as gw
import argparse

# 激活 AutoCAD 主窗口
def activate_autocad_window():
    windows = [w for w in gw.getWindowsWithTitle('AutoCAD') if w.visible]
    if windows:
        win = windows[0]
        win.activate()
        time.sleep(1)
        return True
    return False

# 执行 TUPDSPACE 命令流
def run_tupdspace_flow(coord_str="1000,2000,0"):
    print("[TUPDSPACE] 启动 TUPDSPACE 命令序列...")
    pyautogui.write("TUPDSPACE")
    pyautogui.press("enter")
    time.sleep(0.6)

    pyautogui.press("enter")  # 跳过手动选择
    time.sleep(0.4)

    print(f"[TUPDSPACE] 输入坐标: {coord_str}")
    pyautogui.write(coord_str)
    pyautogui.press("enter")
    time.sleep(0.5)

    pyautogui.press("enter")  # 结束命令
    time.sleep(0.5)

    pyautogui.press("esc")
    print("[TUPDSPACE] 一次命令流程执行完毕，并发送 ESC 清理提示。")

# 主逻辑
def auto_tupdspace_with_repair(coord_str):
    print(f"[TUPDSPACE] 收到坐标参数: {coord_str}")
    if not activate_autocad_window():
        print("[TUPDSPACE] 无法激活 AutoCAD 窗口，退出。")
        return

    print("[TUPDSPACE] 第一次尝试执行命令...")
    run_tupdspace_flow(coord_str)
    time.sleep(2)

    print("[TUPDSPACE] 尝试修复命令窗口：按 Ctrl+9 重新显示命令行")
    pyautogui.hotkey("ctrl", "9")
    time.sleep(1.5)

    print("[TUPDSPACE] 第二次尝试执行命令...")
    run_tupdspace_flow(coord_str)
    print("[TUPDSPACE] 自动输入流程完成。")

# 接收主程序传入参数
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AutoCAD TUPDSPACE 自动输入脚本")
    parser.add_argument("--coord", type=str, default="1000,2000,0", help="插入点坐标 (x,y,z)")
    args = parser.parse_args()

    auto_tupdspace_with_repair(args.coord)
