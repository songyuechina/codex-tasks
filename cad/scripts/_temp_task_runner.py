
import os, shutil, CAD_basic as cb, CAD_file_operations as cfo

def show_top_alert(title, msg, confirm=False):
    import tkinter as tk
    from tkinter import messagebox
    try:
        root = tk.Tk(); root.withdraw(); root.attributes('-topmost', True)
        root.lift(); root.focus_force()
        res = messagebox.askokcancel(title, msg, parent=root) if confirm else messagebox.showinfo(title, msg, parent=root)
        root.destroy()
        return res if confirm else True
    except: return True

target = ""
if target: 
    try: cfo.open_file(os.path.join(r"D:/Mypro/基础服务/用户1/dwg文件", target))
    except: pass
src = r"D:/Mypro/基础服务/用户1/标准模板/核心图签模板.dwg"; tgt = r"D:/Mypro/基础服务/用户1/dwg文件/核心图签.dwg"
try: os.remove(tgt)
except: pass
shutil.copy(src, tgt)
shutil.copy(r"D:/Mypro/基础服务/用户1/标准模板/标准图签模板.dwg", r"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg")
if show_top_alert("Step 1", "1. 修改核心图签\n2. PU 清理\n3. 保存关闭\n\n完成后点确定", confirm=True):
    cb.Redefine_standard_blocks(source_file=tgt, target_file=r"D:/Mypro/基础服务/用户1/dwg文件/标准图签.dwg")
    print("✅ Step 1 完成")
