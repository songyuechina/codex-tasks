import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import sys
import os
import json
import time
import socket
import threading
import shutil
import ctypes
from pathlib import Path
from datetime import datetime

#CAD_System_Queue.py
#版本 V3.0
# ==============================================================================
# 1. IDLE 引导程序 (后台引擎代码)
# ==============================================================================
IDLE_BOOTSTRAP_CODE = r'''
import sys
import os
import socket
import threading
import time
import traceback
import ctypes
import json
import tkinter.messagebox as mb
import tkinter as tk

# === 窗口控制 ===
def position_idle_window():
    try:
        time.sleep(2)
        user32 = ctypes.windll.user32
        sw = user32.GetSystemMetrics(0)
        sh = user32.GetSystemMetrics(1)
        w, h = sw // 2, sh // 2
        x, y = sw - w, 0
        def worker(hwnd, lParam):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                t = buff.value
                if "IDLE Shell" in t or "Python" in t:
                    if user32.IsWindowVisible(hwnd):
                        user32.MoveWindow(hwnd, x, y, w, h, True)
                        return False
            return True
        user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(worker), 0)
    except: pass

try:
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd: ctypes.windll.user32.ShowWindow(hwnd, 6) 
except: pass

threading.Thread(target=position_idle_window, daemon=True).start()

HOST = '127.0.0.1'
PORT = 65432

# === 数据中心 ===
class DataCenter:
    def __init__(self):
        self.root = os.environ.get('USERPATH', '.')
        
    def set_root(self, path):
        self.root = path

DC = DataCenter()

# === 全局内存容器 ===
if 'GLOBAL_CTX' not in globals():
    GLOBAL_CTX = {
        "dy": None,         
        "ctq": None,        
        "ctq_p": None       
    }

def print_status():
    d = GLOBAL_CTX.get('dy')
    c1 = GLOBAL_CTX.get('ctq')   # 模型字典
    c2 = GLOBAL_CTX.get('ctq_p') # 布局字典
    
    n_dy = len(d) if isinstance(d, list) else (len(d[0]) if d else 0)
    
    def fmt_ctq(c):
        if not c or len(c) < 3: return "空"
        return f"P:{len(c[0])} | B:{len(c[1])} | Map:{len(c[2])}"

    print(f"\n📊 [内存状态监控]")
    print(f"   -------------------------------------------")
    print(f"   🟢 Step 2 (选区) : {n_dy} 个")
    print(f"   🟢 Step 4 (模型) : {fmt_ctq(c1)}")
    print(f"   🟢 Step 4 (布局) : {fmt_ctq(c2)}")
    print(f"   -------------------------------------------\n")

def run_script_in_main(script_path):
    if not os.path.exists(script_path): return
    script_dir = os.path.dirname(script_path)
    if script_dir not in sys.path: sys.path.insert(0, script_dir)
    
    old_cwd = os.getcwd()
    try:
        os.chdir(script_dir)
        with open(script_path, 'r', encoding='utf-8-sig') as f:
            code = compile(f.read(), script_path, 'exec')
        main_mod = sys.modules['__main__']
        
        exec_globals = main_mod.__dict__
        exec_globals['__file__'] = str(script_path)
        exec_globals['DC'] = DC
        exec_globals['GLOBAL_CTX'] = GLOBAL_CTX
        exec_globals['print_status'] = print_status
        
        exec(code, exec_globals)
    except Exception:
        traceback.print_exc()
    finally:
        os.chdir(old_cwd)
    
    print_status()
    sys.stdout.write(">>> ")
    sys.stdout.flush()

def start_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"引擎就绪 {HOST}:{PORT}")
    except: pass

    while True:
        try:
            conn, addr = server.accept()
            with conn:
                data = conn.recv(16384).decode('utf-8', errors='ignore')
                if data.startswith("RUN:"):
                    run_script_in_main(data[4:].strip())
        except: time.sleep(1)

t = threading.Thread(target=start_listener, daemon=True)
t.start()
print("CAD 引擎已启动...")
sys.stdout.write(">>> ")
sys.stdout.flush()
'''

# ================= 2. 基础配置 =================
SCRIPT_DIR = Path(__file__).resolve().parent
BOOTSTRAP_FILE = SCRIPT_DIR / "IDLE_bootstrap.py"
TEMP_SCRIPT_FILE = SCRIPT_DIR / "_temp_task_runner.py"

class LockManager:
    def __init__(self, service_root, current_user):
        self.root = service_root
        self.user = current_user
        self.lock_file = os.path.join(self.root, "SYSTEM.lock")
        self.wait_file = os.path.join(self.root, "WAITING.list")
    def try_acquire(self):
        if os.path.exists(self.lock_file): return False, "未知", "未知"
        self._write_lock()
        return True, None, None
    def _write_lock(self):
        try:
            with open(self.lock_file, 'w', encoding='utf-8') as f:
                json.dump({"user": self.user, "time": str(datetime.now())}, f)
        except: pass
    def release(self):
        for f in [self.lock_file, self.wait_file]:
            if os.path.exists(f): 
                try: os.remove(f) 
                except: pass
    def check_waiters(self): return []
    def add_to_wait_list(self): pass

# ================= 3. 主程序 GUI =================

class MasterRunner:
    def __init__(self, root, user_name, service_path):
        self.root = root
        self.user_name = user_name
        self.service_path = service_path
        self.user_path = os.path.join(self.service_path, self.user_name)
        os.environ['USERPATH'] = self.user_path 
        
        self.root.title(f"CAD 基础服务 (IDLE版) - {user_name}")
        
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        w, h = int(sw / 2), int(sh / 2)
        x, y = int((sw - w) / 2), int((sh - h) / 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd: ctypes.windll.user32.ShowWindow(hwnd, 6) 
        except: pass
        
        self.locker = LockManager(self.service_path, self.user_name)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dragon.TButton', font=('微软雅黑', 10, 'bold'), foreground='purple')
        style.configure('Repair.TButton', font=('微软雅黑', 9, 'bold'), foreground='darkblue')
        style.configure('Data.TButton', font=('微软雅黑', 9), foreground='green')
        style.configure('Step.TButton', font=('微软雅黑', 9))
        
        self.cfg = {
            "root": tk.StringVar(value=self.user_path), 
            "space_style": tk.StringVar(value="模型空间样式"),
            "target_dwg":   tk.StringVar(), 
            "dir_template": tk.StringVar(), 
            "dir_ctb_root": tk.StringVar(), 
            "dir_dwg":      tk.StringVar(), 
            "dir_pdf":      tk.StringVar(), 
            "cur_cat_tpl":  tk.StringVar(),
            "cur_ctb":      tk.StringVar(),
            "mulu_xuhao":   tk.StringVar(value="1")
        }
        self.session_data = {"method": "智能极大矩形 (默认)", "layout": "布局1", "extra": "标准图签"}

        self._ensure_bootstrap()
        self.idle_proc = None
        self.root.after(500, self.launch_idle)

        self._init_ui() 
        self.refresh_workspace_paths()
        
        self.stop_thread = False
        threading.Thread(target=self.monitor_waiters, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _ensure_bootstrap(self):
        try:
            with open(BOOTSTRAP_FILE, "w", encoding="utf-8") as f: f.write(IDLE_BOOTSTRAP_CODE)
        except: pass

    def launch_idle(self):
        if self.idle_proc and self.idle_proc.poll() is None: return 
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 6
        cmd = [sys.executable, "-m", "idlelib.idle", "-r", str(BOOTSTRAP_FILE)]
        try: self.idle_proc = subprocess.Popen(cmd, cwd=str(SCRIPT_DIR), startupinfo=startupinfo)
        except: pass

    def _init_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tab_dashboard = self.create_tab("🏠 总看板")
        self.tab_titleblock = self.create_tab("🏷️ 插图签 (全流程)")
        self.tab_catalog = self.create_tab("📚 编目录")
        self.tab_print = self.create_tab("🖨️ 打印")
        
        self.setup_dashboard()
        self.setup_title_block_tab()
        self.setup_catalog()
        self.setup_print()
        
        frame_log = ttk.LabelFrame(self.root, text="运行日志", height=100)
        frame_log.pack(fill='x', side='bottom', padx=5, pady=5)
        self.log_widget = scrolledtext.ScrolledText(frame_log, height=5, state='disabled', bg='#f0f0f0')
        self.log_widget.pack(fill='both')

    def create_tab(self, text):
        f = ttk.Frame(self.notebook)
        self.notebook.add(f, text=text)
        return f

    # ================= Tab 1: 总看板 =================
    def setup_dashboard(self):
        f_top = ttk.Frame(self.tab_dashboard)
        f_top.pack(fill='x', padx=10, pady=5)
        ttk.Button(f_top, text="⚡ 重启引擎", command=self.launch_idle).pack(side='right')
        ttk.Button(f_top, text="🔍 检查数据", command=lambda: self.run_macro("Check_Status")).pack(side='right', padx=10)
        
        frame_env = ttk.LabelFrame(self.tab_dashboard, text="全局配置", padding=5)
        frame_env.pack(fill='x', padx=10, pady=5)
        f1 = ttk.Frame(frame_env); f1.pack(fill='x')
        ttk.Label(f1, text="文件:").pack(side='left')
        self.combo_target = ttk.Combobox(f1, textvariable=self.cfg["target_dwg"], width=30, state="readonly")
        self.combo_target.pack(side='left', padx=5)
        ttk.Button(f1, text="刷新", command=self.refresh_workspace_paths, width=6).pack(side='right')
        f2 = ttk.Frame(frame_env); f2.pack(fill='x', pady=5)
        ttk.Label(f2, text="样式:").pack(side='left')
        self.combo_space = ttk.Combobox(f2, textvariable=self.cfg["space_style"], 
                                        values=["模型空间样式", "图纸空间样式", "混合空间样式"], width=15, state="readonly")
        self.combo_space.pack(side='left', padx=5)
        self.combo_space.current(0)

        frame_data = ttk.LabelFrame(self.tab_dashboard, text="状态恢复", padding=5)
        frame_data.pack(fill='x', padx=10, pady=5)
        ttk.Button(frame_data, text="💾 载入当前文件映射", width=25,
                   command=lambda: self.run_macro("Load_Current_Map")).pack(side='left', padx=5)
        ttk.Label(frame_data, text="* 若重启软件，请先点击此按钮恢复上次工作", foreground='gray').pack(side='left', padx=5)
        
        ttk.Label(self.tab_dashboard, text="\n说明: 所有的插图签操作请切换至【插图签】标签页", font=('微软雅黑', 10, 'italic'), foreground='gray').pack()

    # ================= Tab 2: 插图签 =================
    def setup_title_block_tab(self):
        canvas = tk.Canvas(self.tab_titleblock)
        scrollbar = ttk.Scrollbar(self.tab_titleblock, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        pad_opt = {'padx': 10, 'pady': 5}
        
        grp1 = ttk.LabelFrame(scrollable_frame, text="第一阶段：准备与识别", padding=5)
        grp1.pack(fill='x', **pad_opt)
        self.add_dragon_btn(grp1, "Step 1: 生成标准图签", "TB_Gen_Base")
        self.add_dragon_btn(grp1, "Step 2: 识别打印区域 (生成 DY)", "Area_Detect_MaxRect")
        
        grp2 = ttk.LabelFrame(scrollable_frame, text="第二阶段：插入与映射", padding=5)
        grp2.pack(fill='x', **pad_opt)
        self.add_dragon_btn(grp2, "Step 3: 插入图签 (仅插入)", "TB_Insert_Model")
        ttk.Button(grp2, text="Step 3+: 图形修复 (独立)", style='Repair.TButton',
                   command=lambda: self.run_macro("TB_Repair")).pack(fill='x', pady=2)
        self.add_dragon_btn(grp2, "Step 4: 重建字典 (生成 CTQ)", "TB_Rebuild_Map")

        grp3 = ttk.LabelFrame(scrollable_frame, text="第三阶段：内容与数据", padding=5)
        grp3.pack(fill='x', **pad_opt)
        f_s5 = ttk.Frame(grp3); f_s5.pack(fill='x', pady=2)
        ttk.Label(f_s5, text="Step 5: 写图签 (交互)", font=('bold', 10)).pack(anchor='w')
        self.add_step_btn(f_s5, "5.1 抓取图名 (Auto Fill)", "Step5_AutoFill")
        self.add_step_btn(f_s5, "5.2 导出 Excel (核对)", "Step5_ExportExcel")
        self.add_step_btn(f_s5, "5.3 导入 Excel (更新)", "Step5_ImportExcel")
        
        grp4 = ttk.LabelFrame(scrollable_frame, text="第四阶段：样式调整", padding=5)
        grp4.pack(fill='x', **pad_opt)
        ttk.Button(grp4, text="Step 6: 编辑图签属性 (高度/样式/对正)", style='Dragon.TButton',
                   command=lambda: self.run_macro("TB_Edit_Config_UI")).pack(fill='x', pady=5)

    # ================= Tab 3: 编目录 =================
    def setup_catalog(self):
        f = ttk.Frame(self.tab_catalog, padding=20)
        f.pack(fill='both')
        ttk.Label(f, text="目录模板 (请放入 '标准模板' 文件夹):").pack(anchor='w')
        self.combo_tpl = ttk.Combobox(f, textvariable=self.cfg["cur_cat_tpl"], width=40, state="readonly")
        self.combo_tpl.pack(anchor='w', pady=5)
        f_idx = ttk.Frame(f)
        f_idx.pack(fill='x', pady=5)
        ttk.Label(f_idx, text="模板类型:").pack(side='left')
        ttk.Radiobutton(f_idx, text="模板1 (58行/页)", variable=self.cfg["mulu_xuhao"], value="1").pack(side='left', padx=10)
        ttk.Radiobutton(f_idx, text="模板2 (28行/页)", variable=self.cfg["mulu_xuhao"], value="2").pack(side='left')
        self.add_step_btn(f, "1. 插入目录模板 (生成目录文件)", "Cat_Step1")
        self.add_step_btn(f, "2. 插入目录图签 (建立映射)", "Cat_Step2")
        self.add_step_btn(f, "3. 书写目录 (Excel -> CAD)", "Cat_Step3")
        self.add_step_btn(f, "4. 合并目录到主文件", "Cat_Step4")

    # ================= Tab 4: 打印 (6种模式) =================
    def setup_print(self):
        f = ttk.Frame(self.tab_print, padding=20)
        f.pack(fill='both')
        
        f_cfg = ttk.LabelFrame(f, text="全局打印参数", padding=10)
        f_cfg.pack(fill='x', pady=5)
        ttk.Label(f_cfg, text="打印样式表 (.ctb):").pack(side='left')
        self.combo_ctb = ttk.Combobox(f_cfg, textvariable=self.cfg["cur_ctb"], width=30, state="readonly")
        self.combo_ctb.pack(side='left', padx=10)
        
        f_matrix = ttk.LabelFrame(f, text="执行打印 (3种样式 × 2种方式)", padding=10)
        f_matrix.pack(fill='both', expand=True, pady=10)
        f_matrix.columnconfigure(1, weight=1)
        f_matrix.columnconfigure(2, weight=1)
        
        ttk.Label(f_matrix, text="空间样式", font=('bold', 10)).grid(row=0, column=0, padx=5, pady=10)
        ttk.Label(f_matrix, text="📂 按文件打印 (自动全套)", font=('bold', 10), foreground='blue').grid(row=0, column=1, padx=5, pady=10)
        ttk.Label(f_matrix, text="📝 按列表打印 (Step2选区)", font=('bold', 10), foreground='green').grid(row=0, column=2, padx=5, pady=10)
        
        ttk.Label(f_matrix, text="模型空间样式:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        ttk.Button(f_matrix, text="执行 (Model File)", style='Step.TButton',
                   command=lambda: self.run_macro("Print_Model_File")).grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        ttk.Button(f_matrix, text="执行 (Model List)", style='Step.TButton',
                   command=lambda: self.run_macro("Print_Model_List")).grid(row=1, column=2, padx=5, pady=5, sticky='ew')

        ttk.Label(f_matrix, text="图纸空间样式:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        ttk.Button(f_matrix, text="执行 (Layout File)", style='Step.TButton',
                   command=lambda: self.run_macro("Print_Layout_File")).grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        ttk.Button(f_matrix, text="执行 (Layout List)", style='Step.TButton',
                   command=lambda: self.run_macro("Print_Layout_List")).grid(row=2, column=2, padx=5, pady=5, sticky='ew')

        ttk.Label(f_matrix, text="混合空间样式:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        ttk.Button(f_matrix, text="执行 (Hybrid File)", style='Step.TButton',
                   command=lambda: self.run_macro("Print_Hybrid_File")).grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        ttk.Button(f_matrix, text="执行 (Hybrid List)", style='Step.TButton',
                   command=lambda: self.run_macro("Print_Hybrid_List")).grid(row=3, column=2, padx=5, pady=5, sticky='ew')

        ttk.Label(f_matrix, text="\n说明:\n• [按文件]: 自动分析整个文件，无需选区。\n• [按列表]: 仅打印在 Step 2 中识别/加载的红色选框。", 
                  foreground="gray", justify="left").grid(row=4, column=0, columnspan=3, sticky='w', padx=10)

    # ================= 辅助函数 =================
    def add_step_btn(self, parent, text, func_key):
        ttk.Button(parent, text=text, style='Step.TButton',
                   command=lambda: self.run_macro(func_key)).pack(fill='x', padx=5, pady=5)

    def add_dragon_btn(self, parent, text, macro_key):
        ttk.Button(parent, text=text, style='Dragon.TButton', width=40,
                   command=lambda: self.run_macro(macro_key)).pack(pady=5)

    def send_script_to_idle(self, code_str):
        try:
            with open(TEMP_SCRIPT_FILE, "w", encoding="utf-8-sig") as f: f.write(code_str)
            HOST, PORT = '127.0.0.1', 65432
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2); s.connect((HOST, PORT))
                s.sendall(f"RUN:{TEMP_SCRIPT_FILE}".encode('utf-8'))
            return True
        except Exception as e:
            self.log(f"❌ 连接引擎失败: {e}")
            return False

    def ask_attribute_config(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Step 6: 图签属性批量编辑")
        dialog.geometry("800x600")
        target_tags = ["图纸名称", "图纸编号", "图纸规格", "专业名称", "项目名称", "子项目名称", "建设单位名称", "设计阶段", "版本号", "出图日期", "设计编号"]
        prop_keys = ["style", "height", "width_factor", "rotation_deg", "justify", "boundary_width"]
        prop_labels = ["样式", "高度", "宽度因子", "旋转角度", "对正(0-14)", "边界宽"]
        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        frame_grid = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_grid, anchor="nw")
        def configure_scroll_region(event): canvas.configure(scrollregion=canvas.bbox("all"))
        frame_grid.bind("<Configure>", configure_scroll_region)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        ttk.Label(frame_grid, text="标签名", font=('bold', 10)).grid(row=0, column=0, padx=5, pady=5)
        for i, lbl in enumerate(prop_labels): ttk.Label(frame_grid, text=lbl, font=('bold', 9)).grid(row=0, column=i+1, padx=5, pady=5)
        entry_widgets = {}
        for r, tag in enumerate(target_tags):
            row_idx = r + 1
            ttk.Label(frame_grid, text=tag).grid(row=row_idx, column=0, padx=5, pady=5, sticky='w')
            entry_widgets[tag] = {}
            for c, key in enumerate(prop_keys):
                e = ttk.Entry(frame_grid, width=12)
                e.grid(row=row_idx, column=c+1, padx=2, pady=2)
                entry_widgets[tag][key] = e
        result = {"ok": False, "config": {}}
        def on_apply():
            final_config = {}
            for tag, props in entry_widgets.items():
                tag_conf = {}
                for key, entry in props.items():
                    val = entry.get().strip()
                    if val:
                        try:
                            if key in ["height", "width_factor", "rotation_deg", "boundary_width"]: tag_conf[key] = float(val)
                            elif key == "justify": tag_conf[key] = int(val)
                            else: tag_conf[key] = val
                        except: tag_conf[key] = val
                if tag_conf: final_config[tag] = tag_conf
            result["config"] = final_config; result["ok"] = True; dialog.destroy()
        f_btm = ttk.Frame(dialog)
        f_btm.pack(fill='x', padx=10, pady=10)
        ttk.Button(f_btm, text="应用修改", command=on_apply, width=20).pack(side='right')
        self.root.wait_window(dialog)
        return result["ok"], result["config"]




    def ask_detection_params(self, initial_style):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Step 2 配置 - {initial_style}")
        dialog.geometry("450x300")
        
        default_method = "智能极大矩形 (默认)"
        if initial_style == "图纸空间样式": default_method = "布局空间 (Paperspace)"
        
        ttk.Label(dialog, text="策略:").pack(pady=5)
        method_var = tk.StringVar(value=default_method)
        cb = ttk.Combobox(dialog, textvariable=method_var, values=["智能极大矩形 (默认)", "布局空间 (Paperspace)", "按图层选择", "按图块选择", "屏幕手动选择"])
        cb.pack()
        ttk.Label(dialog, text="布局名称:").pack(pady=5)
        layout_var = tk.StringVar(value=self.session_data.get("layout", "布局1"))
        ttk.Entry(dialog, textvariable=layout_var).pack()
        ttk.Label(dialog, text="专用参数:").pack(pady=5)
        extra_var = tk.StringVar(value=self.session_data.get("extra", "标准图签"))
        ttk.Entry(dialog, textvariable=extra_var).pack()
        
        result = {"ok": False}
        def on_ok():
            self.session_data.update({"method": method_var.get(), "layout": layout_var.get(), "extra": extra_var.get()})
            result.update(self.session_data); result["ok"] = True; dialog.destroy()
        ttk.Button(dialog, text="执行", command=on_ok).pack(pady=20)
        self.root.wait_window(dialog)
        return result["ok"], result


    # ================= 宏逻辑分发 =================
    def run_macro(self, macro_name):
        def _watch():
            for _ in range(20): 
                time.sleep(30)
                try: self.root.attributes('-topmost', True); self.root.attributes('-topmost', False)
                except: break
        threading.Thread(target=_watch, daemon=True).start()
        
        ctx = {
            "root": self.cfg['root'].get().replace('\\', '/'),
            "style": self.cfg['space_style'].get(),
            "dwg_dir": self.cfg['dir_dwg'].get().replace('\\', '/'),
            "target": self.cfg['target_dwg'].get(),
            "tpl_root": self.cfg['dir_template'].get().replace('\\', '/'),
            "ctb": self.cfg['cur_ctb'].get(),
            "cat_tpl": self.cfg['cur_cat_tpl'].get(),
            "mulu_n": int(self.cfg['mulu_xuhao'].get())
        }
        
        # --- 内部辅助函数 ---
        def get_list_print_script(mode, layout_name="布局1"):
            return f'''
import os
import CAD_basic as cb
os.environ['USERPATH'] = r"{ctx['root']}"
DC.set_root(r"{ctx['root']}")
print("🔌 连接 CAD...")
cb.li()
target_ctb = r"{ctx['ctb']}"
output_root = os.path.join(os.environ['USERPATH'], "输出pdf", "List_Print")
print(f"🚀 启动按列表打印 (模式: {mode})")
raw_data = GLOBAL_CTX.get('dy')
if not raw_data:
    print("❌ 内存无选区数据！请先执行 [Step 2: 识别打印区域] 或 [载入映射]。")
else:
    real_polys = []
    print(f"🔄 正在准备 {{len(raw_data)}} 个打印区域...")
    iterable = raw_data.values() if isinstance(raw_data, dict) else raw_data
    for item in iterable:
        try:
            if hasattr(item, 'Handle'): real_polys.append(item)
            elif isinstance(item, dict): 
                p = cb.restore_or_find_poly(item)
                if p: real_polys.append(p)
        except: pass
    if not real_polys:
        print("❌ 无法恢复有效的打印框对象。")
    else:
        print(f"🖨️ 发送 {{len(real_polys)}} 个任务至打印引擎...")
        if "{mode}" == "Model":
            cb.print_polylines_list(real_polys, folderpath=output_root, ctb=target_ctb, mode="Model")
        elif "{mode}" == "Layout":
            cb.print_layout_polylines_list(real_polys, layout_name="{layout_name}", folderpath=output_root, ctb=target_ctb)
print("🏁 列表打印结束")
'''

        def ask_layout():
            dialog = tk.Toplevel(self.root)
            dialog.title("输入布局名称")
            dialog.geometry("300x150")
            res = {"ok": False, "val": ""}
            ttk.Label(dialog, text="布局名称:").pack(pady=10)
            v = tk.StringVar(value=self.session_data.get("layout", "布局1"))
            ttk.Entry(dialog, textvariable=v).pack()
            def on_ok(): res["val"] = v.get(); res["ok"] = True; dialog.destroy()
            ttk.Button(dialog, text="确定", command=on_ok).pack(pady=10)
            self.root.wait_window(dialog)
            if res["ok"]: self.session_data["layout"] = res["val"]
            return res["ok"]
        
        TOP_MSG_FUNC = r'''
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
'''
        # ---------------------------------------------------------------------
        # Status & Load
        # ---------------------------------------------------------------------
        if macro_name == "Check_Status":
            self.send_script_to_idle("print_status()")
            
        elif macro_name == "Load_Current_Map":
            layout_name = self.session_data.get("layout", "布局1")
            target_file = ctx['target'] 
            script = f'''
import os
import CAD_basic as cb
os.environ['USERPATH'] = r"{ctx['root']}"
DC.set_root(r"{ctx['root']}")
print("🔌 正在连接 CAD (li)...")
cb.li()
style = "{ctx['style']}"
layout = "{layout_name}"
gui_input = r"{target_file}" 
file_arg = None 
print("-" * 30)
if gui_input and gui_input.strip():
    file_arg = gui_input.strip()
    print(f"📂 [模式] 指定文件名: {{file_arg}}")
else:
    file_arg = None
    print(f"📂 [模式] 自动获取 CAD 当前激活文档...")
print(f"📂 搜索路径: {{os.environ['USERPATH']}}\\配置\\json_maps")
print(f"   >> 正在加载 Step 2 选区 (后缀: '_PrintArea')...")
try:
    dy_polys, _, _ = cb.load_mapping_by_filename(file_arg, folder_name="json_maps", suffix="_PrintArea")
    if dy_polys:
        GLOBAL_CTX['dy'] = dy_polys
        print(f"   ✅ [Step 2] 成功加载 {{len(dy_polys)}} 个打印区域")
    else:
        print(f"   ⚪ [Step 2] 未找到记录")
except Exception as e:
    print(f"   ❌ [Step 2] 加载异常: {{e}}")
suffix_to_load = ""
if style == "图纸空间样式": suffix_to_load = f"_{{layout}}"
print(f"   >> 正在加载 Step 4 映射 (后缀: '{{suffix_to_load}}')...")
try:
    polys, blocks, mapping = cb.load_mapping_by_filename(file_arg, folder_name="json_maps", suffix=suffix_to_load)
    if mapping:
        data_tuple = (polys, blocks, mapping)
        if style == "图纸空间样式": 
            GLOBAL_CTX['ctq_p'] = data_tuple
            print(f"   ✅ [Step 4] 成功加载布局映射")
        else: 
            GLOBAL_CTX['ctq'] = data_tuple
            print(f"   ✅ [Step 4] 成功加载模型映射")
    else:
        print(f"   ❌ [Step 4] 未找到有效数据文件")
except Exception as e:
    print(f"   ❌ [Step 4] 加载异常: {{e}}")
print("-" * 30)
print_status()
'''
            self.send_script_to_idle(script)

        # ---------------------------------------------------------------------
        # Step 1
        # ---------------------------------------------------------------------
        elif macro_name == "TB_Gen_Base":
            script = f'''
import os, shutil, CAD_basic as cb, CAD_file_operations as cfo
{TOP_MSG_FUNC}
target = "{ctx['target']}"
if target: 
    try: cfo.open_file(os.path.join(r"{ctx['dwg_dir']}", target))
    except: pass
src = r"{ctx['tpl_root']}/核心图签模板.dwg"; tgt = r"{ctx['dwg_dir']}/核心图签.dwg"
try: os.remove(tgt)
except: pass
shutil.copy(src, tgt)
shutil.copy(r"{ctx['tpl_root']}/标准图签模板.dwg", r"{ctx['dwg_dir']}/标准图签.dwg")
if show_top_alert("Step 1", "1. 修改核心图签\\n2. PU 清理\\n3. 保存关闭\\n\\n完成后点确定", confirm=True):
    cb.Redefine_standard_blocks(source_file=tgt, target_file=r"{ctx['dwg_dir']}/标准图签.dwg")
    print("✅ Step 1 完成")
'''
            self.send_script_to_idle(script)

        # ---------------------------------------------------------------------
        # Step 2
        # ---------------------------------------------------------------------
        elif macro_name == "Area_Detect_MaxRect":
            ok, res = self.ask_detection_params(ctx['style'])
            if not ok: return
            p = {"lm": 7000, "cha_Y": 2000, "tol": 1.0} if ctx['style']=="模型空间样式" else {"lm": 70, "cha_Y": 20, "tol": 0.01}
            if ctx['style'] == "混合空间样式": p['cha_Y'] = 5
            script = f'''
import CAD_basic as cb
DC.set_root(r"{ctx['root']}")
{TOP_MSG_FUNC}
print("🚀 [Step 2] 识别...")
cb.li()
res = [] 
style = "{ctx['style']}"
if style == "图纸空间样式":
    res = cb.select_print_areas_paperspace(layout_name="{res['layout']}", min_side_len={p['lm']}, mute_logs=False, explicit_owner_id=None)
else:
    if "智能极大矩形" in "{res['method']}":
        raw_ret = cb.select_print_areas_maxrect_from_polylines(lm={p['lm']}, tol_single={p['tol']}, layer_name="dy_zhuanyong", width=0.0, color=1, z=0.0, duanbian={p['lm']}, debug=True, cha_Y={p['cha_Y']})
        if isinstance(raw_ret, tuple): res = raw_ret[0]
        else: res = raw_ret
    elif "按图层" in "{res['method']}":
        res = cb.select_print_areas_from_layer(source_layer="{res['extra']}", rect_layer="dy_zhuanyong", width=0.0, color=1, z=0.0, cha_Y={p['cha_Y']}, debug=True)
GLOBAL_CTX['dy'] = res
try:
    dy_data = {{}}
    if res:
        for i, pl in enumerate(res):
            try:
                poly_info = cb.extract_poly_data(pl) 
                if poly_info: dy_data[i] = poly_info
            except: pass
    if dy_data:
        cb.save_mapping_dict(None, dy_data, folder_name="json_maps", suffix="_PrintArea")
        print("💾 打印区域[几何数据]已保存 (_PrintArea.json)")
except Exception as e: print(f"❌ 保存失败: {{e}}")
print(f"✅ 识别完成: {{len(res)}} 个")
'''
            self.send_script_to_idle(script)

        # ---------------------------------------------------------------------
        # Step 3
        # ---------------------------------------------------------------------
        elif macro_name == "TB_Insert_Model":
            layout = self.session_data.get("layout", "布局1")
            script = f'''
import CAD_basic as cb
{TOP_MSG_FUNC}
print("🚀 [Step 3] 插入图签...")
if not GLOBAL_CTX.get('dy'): 
    print("❌ 错误: 内存无 dy 数据！请先运行 Step 2")
else:
    style = "{ctx['style']}"
    dy = GLOBAL_CTX['dy']
    if style == "模型空间样式":
        cb.insert_and_scale_labels_area_power(dy, layername="dy_quyu", delpan=0, debug=True)
        show_top_alert("检查", "请检查图签块是否已成功剥离。", confirm=False)
    elif style == "图纸空间样式":
        cb.insert_and_scale_labels_paper_space(dy, layername="dy_quyu", layout_name="{layout}", delpan=0, debug=True)
        cb.repair_sp_insert()
        show_top_alert("交互", "请手动将图签复制到布局 '{layout}'。\\n完成后点确定。", confirm=False)
    else: 
        cb.insert_and_scale_labels_area_power(dy, layername="dy_quyu", delpan=0, debug=True)
        cb.repair_sp_insert()
        show_top_alert("交互", "请将【图纸空间】部分剪切到布局 '{layout}'。\\n【模型空间】部分保留。\\n\\n完成后点确定。", confirm=False)
    print("✅ Step 3 完成")
'''
            self.send_script_to_idle(script)

        elif macro_name == "TB_Repair":
            script = f'''
import CAD_basic as cb
print("🚀 [Step 3+] 修复...")
style = "{ctx['style']}"
if style == "模型空间样式": cb.process_layer_cleanup_and_format()
else: cb.repair_sp_insert()
print("✅ 修复完成")
'''
            self.send_script_to_idle(script)

        # ---------------------------------------------------------------------
        # Step 4
        # ---------------------------------------------------------------------
        elif macro_name == "TB_Rebuild_Map":
            layout = self.session_data.get("layout", "布局1")
            script = f'''
import CAD_basic as cb
DC.set_root(r"{ctx['root']}")
print("🚀 [Step 4] 重建字典...")
style = "{ctx['style']}"
def save_result(data_tuple, suffix_str):
    if data_tuple and len(data_tuple) >= 3:
        mapping_data = data_tuple[2]
        cb.save_mapping_dict(None, mapping_data, folder_name="json_maps", suffix=suffix_str)
        print(f"💾 映射关系已保存 (后缀: '{{suffix_str}}')")
    else:
        print("❌ 数据格式错误，无法保存")
if style == "模型空间样式":
    ctq = cb.rebuild_print_area_title_mapping(core_layer="dy_quyu_H", final_poly_layer="tuqian_neibu_pl", cha_Y=2000, mute_logs=False, protected_layers=["dy_quyu"])
    GLOBAL_CTX['ctq'] = ctq
    save_result(ctq, "") 
elif style == "图纸空间样式":
    if show_top_alert("交互", "请手动将图签复制到布局 '{layout}'。\\n完成后点击确定。", confirm=True):
        ctq_p = cb.rebuild_print_area_title_mapping_paper(layout_target="{layout}", core_layer="dy_quyu_H", final_poly_layer="tuqian_neibu_pl", cha_Y=20, mute_logs=False)
        GLOBAL_CTX['ctq_p'] = ctq_p
        save_result(ctq_p, "_{layout}")
else: 
    if show_top_alert("交互", "请将【图纸空间】部分剪切到布局 '{layout}'。\\n【模型空间】部分保留。\\n\\n完成后点确定。", confirm=True):
        print("处理布局部分...")
        ctq_p = cb.rebuild_print_area_title_mapping_paper(layout_target="{layout}", core_layer="dy_quyu_H", final_poly_layer="tuqian_neibu_pl", cha_Y=20, mute_logs=False)
        GLOBAL_CTX['ctq_p'] = ctq_p
        save_result(ctq_p, "_{layout}")
        print("处理模型部分...")
        ctq = cb.rebuild_print_area_title_mapping_hm(core_layer="dy_quyu_H", final_poly_layer="tuqian_neibu_pl", cha_Y=20, mute_logs=False, protected_layers=["dy_quyu"], layout_name="平面分割图")
        GLOBAL_CTX['ctq'] = ctq
        save_result(ctq, "") 
print("✅ Step 4 完成")
'''
            self.send_script_to_idle(script)

        # ---------------------------------------------------------------------
        # Step 5
        # ---------------------------------------------------------------------
        elif macro_name == "Step5_AutoFill":
            script = f'''
import CAD_basic as cb
print("🚀 [Step 5.1] 抓取图名 -> 图签...")
target_map = GLOBAL_CTX.get('ctq')
if not target_map and GLOBAL_CTX.get('ctq_p'): target_map = GLOBAL_CTX.get('ctq_p')
if not target_map: print("❌ 内存无映射数据 (请先执行 Step 4)")
else:
    cb.process_drawing_names_and_fill_titleblocks(target_map, num1=14, num2=3, layername="DIM_SYMB", start_index=1, prefix=None)
    print("✅ 填写完成")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Step5_ExportExcel":
            script = f'''
import CAD_basic as cb
print("🚀 [Step 5.2] 导出 Excel...")
target_map = GLOBAL_CTX.get('ctq')
if not target_map and GLOBAL_CTX.get('ctq_p'): target_map = GLOBAL_CTX.get('ctq_p')
if not target_map: print("❌ 内存无映射数据")
else:
    cb.build_full_print_dict_and_export_excel(target_map, template_path=None, output_path=None, start_index=1)
    print("✅ 导出完成")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Step5_ImportExcel":
            script = f'''
import CAD_basic as cb
print("🚀 [Step 5.3] 导入 Excel -> CAD...")
target_map = GLOBAL_CTX.get('ctq')
if not target_map and GLOBAL_CTX.get('ctq_p'): target_map = GLOBAL_CTX.get('ctq_p')
if not target_map: print("❌ 内存无映射数据")
else:
    cb.read_excel_and_update_cad_titleblocks(target_map, excel_path=None, start_index=1)
    print("✅ 更新完成")
'''
            self.send_script_to_idle(script)

        # ---------------------------------------------------------------------
        # Step 6
        # ---------------------------------------------------------------------
        elif macro_name == "TB_Edit_Config_UI":
            ok, config = self.ask_attribute_config()
            if ok and config:
                config_str = json.dumps(config, ensure_ascii=False)
                script = f'''
import CAD_basic as cb
import json
print("🚀 [Step 6] 批量编辑图签属性...")
target_map = GLOBAL_CTX.get('ctq')
if not target_map and GLOBAL_CTX.get('ctq_p'): target_map = GLOBAL_CTX.get('ctq_p')
if not target_map: 
    print("❌ 内存无映射数据 (请先执行 Step 4)")
else:
    config = json.loads(r'{config_str}')
    print(f"🔧 配置项数量: {{len(config)}}")
    if hasattr(cb, 'batch_update_block_attributes_config'):
        cb.batch_update_block_attributes_config(target_map, config)
    else:
        print("❌ 错误: CAD_basic.py 中找不到 batch_update_block_attributes_config 函数")
'''
                self.send_script_to_idle(script)

        # ---------------------------------------------------------------------
        # Catalog (Cat)
        # ---------------------------------------------------------------------
        elif macro_name == "Cat_Step1":
            if not ctx['cat_tpl']: 
                messagebox.showerror("Err", "请选择目录模板")
                return
            script = f'''
import CAD_basic as cb
DC.set_root(r"{ctx['root']}")
print("🚀 [目录] Step 1: 插入目录模板...")
res = cb.bianmulu_func1(dwg_path=None, mulu_xuhao={ctx['mulu_n']})
if res: print(f"✅ Step 1 执行成功")
else: print(f"❌ Step 1 执行失败")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Cat_Step2":
            script = f'''
import CAD_basic as cb
print("🚀 [目录] Step 2: 插入目录图签...")
res = cb.bianmulu_func2(dwg_path=None)
if res: print(f"✅ Step 2 执行成功")
else: print(f"❌ Step 2 执行失败")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Cat_Step3":
            script = f'''
import CAD_basic as cb
print("🚀 [目录] Step 3: 书写目录...")
res = cb.bianmulu_func3(dwg_path=None, mubanxuhao={ctx['mulu_n']})
if res: print(f"✅ Step 3 执行成功")
else: print(f"❌ Step 3 执行失败")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Cat_Step4":
            script = f'''
import CAD_basic as cb
print("🚀 [目录] Step 4: 合并到主文件...")
res = cb.bianmulu_func4(dwg_path=None)
if res: print(f"✅ Step 4 执行成功")
else: print(f"❌ Step 4 执行失败")
'''
            self.send_script_to_idle(script)
        
        # ---------------------------------------------------------------------
        # 🖨️ 打印模块 (6种模式)
        # ---------------------------------------------------------------------
        elif macro_name == "Print_Model_File":
            script = f'''
import os
import CAD_basic as cb
os.environ['USERPATH'] = r"{ctx['root']}"
DC.set_root(r"{ctx['root']}")
cb.li()
print("🚀 [Model-File] 全文件打印...")
cb.print_dwg_file_model(file_path=None, ctb=r"{ctx['ctb']}")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Print_Model_List":
            script = get_list_print_script(mode="Model")
            self.send_script_to_idle(script)

        elif macro_name == "Print_Layout_File":
            if not ask_layout(): return
            layout_name_user = self.session_data.get("layout", "布局1")
            script = f'''
import os
import CAD_basic as cb
os.environ['USERPATH'] = r"{ctx['root']}"
DC.set_root(r"{ctx['root']}")
cb.li()
print(f"🚀 [Layout-File] 布局打印 ({{'{layout_name_user}'}})...")
cb.print_dwg_file_layout(file_path=None, layout_name="{layout_name_user}", ctb=r"{ctx['ctb']}")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Print_Layout_List":
            if not ask_layout(): return
            layout_name_user = self.session_data.get("layout", "布局1")
            script = get_list_print_script(mode="Layout", layout_name=layout_name_user)
            self.send_script_to_idle(script)

        elif macro_name == "Print_Hybrid_File":
            if not ask_layout(): return 
            layout_name_user = self.session_data.get("layout", "布局1")
            script = f'''
import os
import CAD_basic as cb
os.environ['USERPATH'] = r"{ctx['root']}"
DC.set_root(r"{ctx['root']}")
cb.li()
print("🚀 [Hybrid-File] 混合模式全打印...")

print("\\n>>> 阶段 1: 模型")
try: cb.print_dwg_file_model_h(file_path=None, ctb=r"{ctx['ctb']}")
except Exception as e: print(f"❌ 模型失败: {{e}}")

print("\\n>>> 阶段 2: 布局")
try: cb.print_dwg_file_layout_h(file_path=None, layout_name="{layout_name_user}", ctb=r"{ctx['ctb']}")
except Exception as e: print(f"❌ 布局失败: {{e}}")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Print_Hybrid_List":
            # 混合模式下按列表打印，默认走模型引擎
            script = get_list_print_script(mode="Model")
            self.send_script_to_idle(script)

    def refresh_workspace_paths(self):
        user_root = self.cfg["root"].get()
        dwg_dir = os.path.join(user_root, "dwg文件")
        if not os.path.exists(dwg_dir): 
            try: os.makedirs(dwg_dir)
            except: pass
        self.cfg["dir_dwg"].set(dwg_dir)
        self.cfg["dir_template"].set(os.path.join(user_root, "标准模板"))
        
        files = []
        if os.path.exists(dwg_dir):
            for r, d, f in os.walk(dwg_dir):
                for file in f:
                    if file.lower().endswith(".dwg"):
                        files.append(os.path.relpath(os.path.join(r, file), dwg_dir))
        self.combo_target['values'] = [""] + sorted(files)
        self.combo_target.current(0)
        
        tpl_dir = self.cfg["dir_template"].get()
        if os.path.exists(tpl_dir):
            self.combo_tpl['values'] = [f for f in os.listdir(tpl_dir) if f.lower().endswith(".dwg")]
            if self.combo_tpl['values']: self.combo_tpl.current(0)

        ctb_dir = os.path.join(user_root, "配置", "打印样式")
        self.cfg["dir_ctb_root"].set(ctb_dir)
        if os.path.exists(ctb_dir):
            ctbs = [f for f in os.listdir(ctb_dir) if f.lower().endswith(".ctb")]
            if ctbs:
                self.combo_ctb['values'] = ctbs
                self.combo_ctb.current(0)
            else:
                self.log("⚠️ 打印样式目录为空")
        else:
            self.log(f"⚠️ 找不到打印样式目录: {ctb_dir}")

        self.log(f"资源刷新: {len(files)} 个文件")

    def log(self, text):
        self.log_widget.configure(state='normal')
        self.log_widget.insert(tk.END, text + "\n")
        self.log_widget.see(tk.END)
        self.log_widget.configure(state='disabled')

    def monitor_waiters(self):
        while not self.stop_thread:
            waiters = self.locker.check_waiters()
            time.sleep(3)

    def on_close(self):
        if self.idle_proc:
            try: self.idle_proc.terminate()
            except: pass
        self.locker.release()
        self.root.destroy()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        u, p = "调试用户", r"D:\Mypro\基础服务"
    else:
        u, p = sys.argv[1], sys.argv[2]
    l = LockManager(p, u)
    ok, owner, t = l.try_acquire()
    if not ok: sys.exit()
    root = tk.Tk()
    app = MasterRunner(root, u, p)
    root.mainloop()
