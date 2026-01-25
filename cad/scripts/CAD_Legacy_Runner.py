import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import os

# CAD_Legacy_Runner.py
# =========================================================================
# 1. 挂载区：直接引用你现有的两个核心文件
# =========================================================================
# 确保当前目录在系统路径中，以便能找到模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    import CAD_basic as cb             # 你的底层核心
    import CAD_file_operations as cfo  # 你的文件操作库
    print("✅ 成功加载原始 CAD 脚本模块！")
except ImportError as e:
    print(f"❌ 加载失败，请确保 CAD_basic.py 和 CAD_file_operations.py 在同级目录下。\n错误信息: {e}")

# =========================================================================
# 2. 图形界面逻辑 (Tkinter)
# =========================================================================

class LegacyCADRunner:
    def __init__(self, root):
        self.root = root
        self.root.title("CAD 脚本控制台 (基于原始文件)")
        self.root.geometry("700x550")
        
        # 样式设置
        style = ttk.Style()
        style.theme_use('clam') 

        # --- 顶部按钮区 ---
        self.frame_top = ttk.LabelFrame(root, text="现有功能调用", padding=10)
        self.frame_top.pack(fill="x", padx=10, pady=5)

        # 按钮 1: 测试连接 (调用 CAD_basic.li)
        self.btn_link = ttk.Button(self.frame_top, text="🔌 测试 CAD 连接 (li)", command=self.gui_test_connection)
        self.btn_link.grid(row=0, column=0, padx=5, pady=5)

        # 按钮 2: 新建文件 (调用 CAD_file_operations.new_file)
        self.btn_new = ttk.Button(self.frame_top, text="📄 新建 DWG 文件", command=self.gui_new_file)
        self.btn_new.grid(row=0, column=1, padx=5, pady=5)

        # 按钮 3: 另存为 (调用 CAD_file_operations.save_as)
        self.btn_save = ttk.Button(self.frame_top, text="💾 当前图纸另存为...", command=self.gui_save_as)
        self.btn_save.grid(row=0, column=2, padx=5, pady=5)

        # --- 底部日志区 ---
        self.frame_log = ttk.LabelFrame(root, text="运行日志 (Real-time Log)", padding=10)
        self.frame_log.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_area = scrolledtext.ScrolledText(self.frame_log, height=10, state='disabled', bg="#f0f0f0")
        self.log_area.pack(fill="both", expand=True)

        # 接管系统的 print 输出
        sys.stdout = self
        sys.stderr = self

    # --- 日志重定向 ---
    def write(self, text):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, text)
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')
        self.root.update_idletasks()

    def flush(self): pass

    # --- 异步执行包装器 (防止界面卡死) ---
    def run_in_thread(self, target_func, *args, **kwargs):
        def wrapper():
            print(f"\n--- 开始执行: {target_func.__name__} ---")
            try:
                target_func(*args, **kwargs)
                print(f"--- 执行结束 ---\n")
            except Exception as e:
                print(f"❌ 执行出错: {e}")
        
        threading.Thread(target=wrapper, daemon=True).start()

    # =========================================================================
    # 3. 按钮功能映射 (这里是关键：如何把按钮对应到你的旧代码)
    # =========================================================================

    def gui_test_connection(self):
        """对应 CAD_basic.py 中的 li()"""
        # 我们把它包在一个函数里调用，方便看日志
        def _action():
            cb.li()
            if cb.doc:
                print(f"✅ 连接成功！当前文档: {cb.doc.Name}")
            else:
                print("❌ 连接失败，请检查 CAD 是否打开。")
        
        self.run_in_thread(_action)

    def gui_new_file(self):
        """对应 CAD_file_operations.py 中的 new_file()"""
        # 1. 弹窗让用户选路径
        path = filedialog.asksaveasfilename(
            title="新建文件保存位置",
            defaultextension=".dwg",
            filetypes=[("CAD 图纸", "*.dwg")]
        )
        if not path: return

        # 2. 弹窗询问参数 (对应函数里的 close_after)
        should_close = messagebox.askyesno("选项", "创建后是否立即关闭文件？")

        # 3. 调用你的原始函数
        # 注意：这里直接使用了你 cfo.new_file 的原始定义
        self.run_in_thread(cfo.new_file, path, close_after=should_close)

    def gui_save_as(self):
        """对应 CAD_file_operations.py 中的 save_as (假设你有这个函数)"""
        # 1. 先确保连接
        cb.li()
        if not cb.doc:
            print("❌ 未连接到 CAD，无法操作。")
            return

        path = filedialog.asksaveasfilename(title="另存为...")
        if not path: return

        def _action():
            # 假设你的 file_operations 里有 save_as，如果没有，直接调用 doc 方法
            try:
                # 尝试调用你的库
                if hasattr(cfo, 'save_as'):
                    cfo.save_as(path) 
                else:
                    # 如果库里没有，直接用底层对象操作
                    print("调用 doc.SaveAs...")
                    cb.doc.SaveAs(path)
                print(f"✅ 文件已另存为: {path}")
            except Exception as e:
                print(f"保存失败: {e}")

        self.run_in_thread(_action)

if __name__ == "__main__":
    root = tk.Tk()
    app = LegacyCADRunner(root)
    root.mainloop()
