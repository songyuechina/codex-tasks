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

# CAD_System_Queue.py
# 版本 V3.3 (UI优化与流程重构版)

# ==============================================================================
# 1. IDLE 引导程序 (保持不变)
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
    c1 = GLOBAL_CTX.get('ctq')   # 模型字典 / 通用字典
    c2 = GLOBAL_CTX.get('ctq_p') # 布局字典 (旧兼容)
    
    n_dy = len(d) if isinstance(d, list) else (len(d.values()) if isinstance(d, dict) else 0)
    
    def fmt_ctq(c):
        if not c or len(c) < 3: return "空"
        return f"P:{len(c[0])} | B:{len(c[1])} | Map:{len(c[2])}"

    print(f"\n📊 [内存状态监控]")
    print(f"   -------------------------------------------")
    print(f"   🟢 Step 2 (选区) : {n_dy} 个")
    print(f"   🟢 Step 4 (CTQ)  : {fmt_ctq(c1)}")
    if c2: print(f"   🟢 Step 4 (Lay)  : {fmt_ctq(c2)}")
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
        
        self.root.title(f"CAD 基础服务 (IDLE版) V3.3 - {user_name}")
        
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
        
        # === 样式统一 ===
        style = ttk.Style()
        style.theme_use('clam')
        # 主要步骤按钮 (紫色加粗)
        style.configure('Dragon.TButton', font=('微软雅黑', 10, 'bold'), foreground='purple')
        # 修复类按钮 (蓝色加粗)
        style.configure('Repair.TButton', font=('微软雅黑', 9, 'bold'), foreground='darkblue')
        # 数据类按钮 (绿色加粗)
        style.configure('Data.TButton', font=('微软雅黑', 9, 'bold'), foreground='darkgreen')
        # 普通步骤按钮 (标准)
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
        
        # 数据中心专用变量
        self.dc_vars = {
            "layout_name": tk.StringVar(value=""),
            "operate_target": tk.StringVar(value="Model"),
            "select_config": tk.StringVar(value="None"),
            "use_cache": tk.BooleanVar(value=True)
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
        
        # 1. 更名：系统控制台
        self.tab_dashboard = self.create_tab("🏠 系统控制台")
        # 2. 数据中心
        self.tab_datacenter = self.create_tab("💾 数据中心")
        # 3. 插图签
        self.tab_titleblock = self.create_tab("🏷️ 插图签")
        # 4. 编目录
        self.tab_catalog = self.create_tab("📚 编目录")
        # 5. 打印
        self.tab_print = self.create_tab("🖨️ 打印")
        
        self.setup_dashboard()
        self.setup_datacenter()
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

    # ================= Tab 1: 系统控制台 (原总看板) =================
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
        
        ttk.Label(self.tab_dashboard, text="\n说明: 样式配置、打印区域识别等操作请前往【数据中心】", font=('微软雅黑', 9, 'italic'), foreground='gray').pack()

    # ================= Tab 2: 数据中心 =================
    def setup_datacenter(self):
        pad_opt = {'padx': 10, 'pady': 5}
        
        # 1. 上下文配置
        grp_ctx = ttk.LabelFrame(self.tab_datacenter, text="上下文配置 (Context)", padding=5)
        grp_ctx.pack(fill='x', **pad_opt)
        
        f_row1 = ttk.Frame(grp_ctx)
        f_row1.pack(fill='x', pady=2)
        ttk.Label(f_row1, text="操作目标:").pack(side='left')
        ttk.Combobox(f_row1, textvariable=self.dc_vars["operate_target"], values=["Model", "Layout"], width=10, state="readonly").pack(side='left', padx=5)
        
        ttk.Label(f_row1, text="布局名称:").pack(side='left', padx=(10, 0))
        ttk.Entry(f_row1, textvariable=self.dc_vars["layout_name"], width=15).pack(side='left', padx=5)
        ttk.Label(f_row1, text="(空则为None)", font=('Arial', 8), foreground='gray').pack(side='left')

        f_row2 = ttk.Frame(grp_ctx)
        f_row2.pack(fill='x', pady=2)
        ttk.Label(f_row2, text="识别参数:").pack(side='left')
        ttk.Entry(f_row2, textvariable=self.dc_vars["select_config"], width=10).pack(side='left', padx=5)
        ttk.Checkbutton(f_row2, text="使用缓存", variable=self.dc_vars["use_cache"]).pack(side='left', padx=15)
        
        # 2. 核心操作区 (调整顺序)
        grp_act = ttk.LabelFrame(self.tab_datacenter, text="数据获取与生成 (Core Actions)", padding=5)
        grp_act.pack(fill='x', **pad_opt)
        
        f_act = ttk.Frame(grp_act)
        f_act.pack(fill='x')
        f_act.columnconfigure(0, weight=1)
        f_act.columnconfigure(1, weight=1)
        
        # 按钮 1 & 2
        ttk.Button(f_act, text="1. 获取打印区域 (DY)", style='Data.TButton', 
                   command=lambda: self.run_datacenter_macro("Get_Polylines")).grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Button(f_act, text="2. 获取映射信息 (CTQ)", style='Data.TButton', 
                   command=lambda: self.run_datacenter_macro("Get_CTQ")).grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # 按钮 3 & 4 (调整位置)
        ttk.Button(f_act, text="3. 强制生成 Excel", style='Dragon.TButton', 
                   command=lambda: self.run_datacenter_macro("Force_Excel")).grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        ttk.Button(f_act, text="4. 查询环境资源 (Info)", style='Step.TButton', 
                   command=lambda: self.run_datacenter_macro("Query_Info")).grid(row=1, column=1, sticky='ew', padx=5, pady=5)

        # 3. 信息显示区
        grp_info = ttk.LabelFrame(self.tab_datacenter, text="环境信息反馈", padding=5)
        grp_info.pack(fill='both', expand=True, **pad_opt)
        
        self.txt_env_info = tk.Text(grp_info, height=8, bg="#F5F5F5", font=('Consolas', 9))
        self.txt_env_info.pack(fill='both', expand=True)

    # ================= Tab 3: 插图签 (重构与重号) =================
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
        
        # 组1：准备
        grp1 = ttk.LabelFrame(scrollable_frame, text="第一阶段：准备", padding=5)
        grp1.pack(fill='x', **pad_opt)
        self.add_dragon_btn(grp1, "Step 1: 生成标准图签", "TB_Gen_Base")
        
        # 组2：插入与修复 (Step 2 & 3)
        grp2 = ttk.LabelFrame(scrollable_frame, text="第二阶段：插入 (需先在数据中心获取DY)", padding=5)
        grp2.pack(fill='x', **pad_opt)
        self.add_dragon_btn(grp2, "Step 2: 插入图签 (仅插入)", "TB_Insert_Model")
        
        # 修复按钮独立一行，蓝色
        ttk.Button(grp2, text="Step 3: 图形修复 (必要时执行)", style='Repair.TButton',
                   command=lambda: self.run_macro("TB_Repair")).pack(fill='x', pady=5)

        # 组3：内容与数据 (Step 4)
        grp3 = ttk.LabelFrame(scrollable_frame, text="第三阶段：内容 (需先在数据中心获取CTQ)", padding=5)
        grp3.pack(fill='x', **pad_opt)
        f_content = ttk.Frame(grp3); f_content.pack(fill='x', pady=2)
        ttk.Label(f_content, text="Step 4: 内容处理", font=('bold', 10)).pack(anchor='w')
        
        # 子步骤使用 Step.TButton
        self.add_step_btn(f_content, "4.1 抓取图名 -> 填写图签", "Step5_AutoFill")
        self.add_step_btn(f_content, "4.2 导入 Excel -> 更新图签", "Step5_ImportExcel")
        
        # 组4：样式 (Step 5)
        grp4 = ttk.LabelFrame(scrollable_frame, text="第四阶段：样式", padding=5)
        grp4.pack(fill='x', **pad_opt)
        self.add_dragon_btn(grp4, "Step 5: 编辑属性样式 (高度/对正)", "TB_Edit_Config_UI")

    # ================= Tab 4: 编目录 (保持原样) =================
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

    # ================= Tab 5: 打印 (保持原样) =================
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

        ttk.Label(f_matrix, text="\n说明:\n• [按文件]: 自动分析整个文件，无需选区。\n• [按列表]: 仅打印在 Data Center 中识别/加载的红色选框。", 
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
        dialog.title("Step 5: 图签属性批量编辑")
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

    # ================= 数据中心逻辑 (已修复反斜杠问题) =================
    def run_datacenter_macro(self, action):
        layout_in = self.dc_vars["layout_name"].get().strip()
        layout_arg = f'"{layout_in}"' if layout_in else "None"
        
        op_target = self.dc_vars["operate_target"].get()
        
        sel_conf_in = self.dc_vars["select_config"].get().strip()
        sel_conf_arg = sel_conf_in if sel_conf_in.lower() != "none" else "None"
        if sel_conf_arg != "None" and sel_conf_arg.isdigit():
            sel_conf_arg = int(sel_conf_arg)
            
        use_cache_arg = str(self.dc_vars["use_cache"].get())
        
        # --- 修复: 预先处理路径，避免在 f-string 中使用反斜杠 ---
        dwg_dir_safe = self.cfg['dir_dwg'].get().replace('\\', '/')
        user_path_safe = self.user_path.replace('\\', '/')
        
        target_file = self.cfg['target_dwg'].get().strip()
        file_open_code = ""
        if target_file:
             file_open_code = f'''
# 自动打开总看板指定的文件
try:
    cfo.open_file(os.path.join(r"{dwg_dir_safe}", "{target_file}"))
except: pass
'''

        base_ctx = f'''
import os
import CAD_basic as cb
import CAD_file_operations as cfo
os.environ['USERPATH'] = r"{user_path_safe}"
DC.set_root(r"{user_path_safe}")
print("🔌 连接 CAD...")
cb.li()
{file_open_code}
'''

        if action == "Get_Polylines":
            script = base_ctx + f'''
print(f"🚀 [数据中心] 1. 获取打印区域 (DY)...")
dy = cb.smart_select_polylines(
    layout_name={layout_arg},
    operate_target="{op_target}",
    select_config={sel_conf_arg},
    use_cache={use_cache_arg},
    verbose=True
)
GLOBAL_CTX['dy'] = dy
if dy:
    print(f"✅ 内存已更新: {{len(dy)}} 个打印区域")
else:
    print("❌ 未获取到多段线")
print_status()
'''
            self.send_script_to_idle(script)

        elif action == "Get_CTQ":
            script = base_ctx + f'''
print(f"🚀 [数据中心] 2. 获取映射信息 (CTQ)...")
ctq = cb.smart_rebuild_print_info(
    layout_name={layout_arg},
    operate_target="{op_target}",
    select_config={sel_conf_arg},
    use_cache={use_cache_arg},
    verbose=True
)
GLOBAL_CTX['ctq'] = ctq
if ctq and len(ctq) >= 3:
    print(f"✅ 内存已更新 CTQ: P={{len(ctq[0])}}, B={{len(ctq[1])}}, Map={{len(ctq[2])}}")
else:
    print("❌ 未获取到有效 CTQ 数据")
print_status()
'''
            self.send_script_to_idle(script)

        elif action == "Force_Excel":
            # 路径处理
            tpl_path = os.path.join(self.cfg['dir_template'].get(), "项目图纸信息模板.xlsx").replace('\\', '/')
            script = base_ctx + f'''
print(f"🚀 [数据中心] 3. 强制生成 Excel...")
res = cb.auto_export_excel_with_fallback(
    layout_name={layout_arg},
    operate_target="{op_target}",
    select_config={sel_conf_arg},
    template_path=r"{tpl_path}",
    output_path=None,
    start_index=1,
    use_cache={use_cache_arg},
    verbose=1
)
if res: print("✅ Excel 生成成功")
else: print("❌ Excel 生成失败")
'''
            self.send_script_to_idle(script)

        elif action == "Query_Info":
            cat_tpl = self.cfg['cur_cat_tpl'].get()
            ctb = self.cfg['cur_ctb'].get()
            script = base_ctx + f'''
from pathlib import Path
print(f"🚀 [数据中心] 4. 环境查询...")
doc_name = "未知"
try: 
    doc_name = Path(cb.C.doc.Name).stem
    full_path = Path(cb.C.doc.FullName)
except: 
    full_path = None

layout = {layout_arg}
op = "{op_target}"
suffix = ""
if op == "Layout" and layout: suffix = f"_{{layout}}"
elif op == "Model" and layout: suffix = f"_{{layout}}" 

info = []
info.append(f"📄 当前文件: {{doc_name}}")
info.append(f"🎯 操作目标: {{op}} (Layout={{layout}})")

if full_path:
    base = full_path.parent / full_path.stem
    excel_path = f"{{base}}{{suffix}}.xlsx"
    cat_dwg = f"{{base}}{{suffix}}_目录.dwg"
    info.append(f"📊 关联Excel: {{excel_path}}")
    info.append(f"📑 关联目录: {{cat_dwg}}")
else:
    info.append("❌ 无法获取当前文件路径")

info.append(f"🧩 目录模板: {cat_tpl}")
info.append(f"🖨️ 打印样式: {ctb}")

font_dir = os.path.join(os.environ['USERPATH'], "配置", "Fonts")
if os.path.exists(font_dir):
    fonts = os.listdir(font_dir)
    if fonts: info.append(f"🔤 字体配置: {{len(fonts)}} 个字体文件")
    else: info.append(f"🔤 字体配置: [空] (请补充字体)")
else:
    info.append(f"🔤 字体配置: 目录不存在")

print("\\n".join(info))
print("-" * 30)
'''
            self.send_script_to_idle(script)

    # ================= 宏逻辑分发 (旧版兼容/更新) =================
    def run_macro(self, macro_name):
        def _watch():
            for _ in range(20): 
                time.sleep(30)
                try: self.root.attributes('-topmost', True); self.root.attributes('-topmost', False)
                except: break
        threading.Thread(target=_watch, daemon=True).start()
        
        ctx = {
            "root": self.cfg['root'].get().replace('\\', '/'),
            "style": self.cfg['space_style'].get(), # 仍保留给某些遗留判断
            "dwg_dir": self.cfg['dir_dwg'].get().replace('\\', '/'),
            "target": self.cfg['target_dwg'].get(),
            "tpl_root": self.cfg['dir_template'].get().replace('\\', '/'),
            "ctb": self.cfg['cur_ctb'].get(),
            "cat_tpl": self.cfg['cur_cat_tpl'].get(),
            "mulu_n": int(self.cfg['mulu_xuhao'].get())
        }
        
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
        # Status
        if macro_name == "Check_Status":
            self.send_script_to_idle("print_status()")

        # Step 1
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

        # Step 2: 插入图签
        elif macro_name == "TB_Insert_Model":
            layout = self.dc_vars["layout_name"].get()
            op_target = self.dc_vars["operate_target"].get()
            
            script = f'''
import CAD_basic as cb
{TOP_MSG_FUNC}
print("🚀 [Step 2] 插入图签...")
if not GLOBAL_CTX.get('dy'): 
    print("❌ 错误: 内存无 dy 数据！请先在数据中心获取 DY")
else:
    dy = GLOBAL_CTX['dy']
    op = "{op_target}"
    lay = "{layout}"
    
    if op == "Model" and not lay:
        cb.insert_and_scale_labels_area_power(dy, layername="dy_quyu", delpan=0, debug=True)
        show_top_alert("完成", "图签插入完成。", confirm=False)
    elif op == "Layout":
        cb.insert_and_scale_labels_paper_space(dy, layername="dy_quyu", layout_name=lay, delpan=0, debug=True)
        show_top_alert("交互", f"图签已插入到布局 '{{lay}}'。", confirm=False)
    else: 
        cb.insert_and_scale_labels_area_power(dy, layername="dy_quyu", delpan=0, debug=True)
        cb.repair_sp_insert(target_layout_name=lay)
        show_top_alert("交互", f"请将【图纸空间】部分剪切到布局 '{{lay}}'。", confirm=False)
    print("✅ Step 2 完成")
'''
            self.send_script_to_idle(script)

        # Step 3: 修复
        elif macro_name == "TB_Repair":
            layout = self.dc_vars["layout_name"].get()
            op_target = self.dc_vars["operate_target"].get()
            script = f'''
import CAD_basic as cb
print("🚀 [Step 3] 图形修复...")
op = "{op_target}"
lay = "{layout}"
if op == "Model" and not lay: 
    cb.process_layer_cleanup_and_format()
else: 
    cb.repair_sp_insert(target_layout_name=lay)
print("✅ 修复完成")
'''
            self.send_script_to_idle(script)

        # Step 4.1
        elif macro_name == "Step5_AutoFill":
            layout = self.dc_vars["layout_name"].get()
            op_target = self.dc_vars["operate_target"].get()
            script = f'''
import CAD_basic as cb
print("🚀 [Step 4.1] 抓取图名 -> 图签...")
target_map = GLOBAL_CTX.get('ctq')
if not target_map: 
    print("❌ 内存无映射数据 (请先在数据中心获取 CTQ)")
else:
    op = "{op_target}"
    lay = "{layout}"
    if op == "Layout":
        cb.process_drawing_names_and_fill_titleblocks(target_map, layout_target=lay, num1=14, num2=3, layername="DIM_SYMB", start_index=1, prefix=None)
    else:
        cb.process_drawing_names_and_fill_titleblocks(target_map, num1=14, num2=3, layername="DIM_SYMB", start_index=1, prefix=None)
    print("✅ 填写完成")
'''
            self.send_script_to_idle(script)

        # Step 4.2
        elif macro_name == "Step5_ImportExcel":
            layout = self.dc_vars["layout_name"].get()
            op_target = self.dc_vars["operate_target"].get()
            script = f'''
import CAD_basic as cb
print("🚀 [Step 4.2] 导入 Excel -> CAD...")
target_map = GLOBAL_CTX.get('ctq')
if not target_map: print("❌ 内存无映射数据")
else:
    op = "{op_target}"
    lay = "{layout}"
    if op == "Layout":
        cb.read_excel_and_update_cad_titleblocks(target_map, layout_target=lay, excel_path=None, start_index=1)
    else:
        cb.read_excel_and_update_cad_titleblocks(target_map, excel_path=None, start_index=1)
    print("✅ 更新完成")
'''
            self.send_script_to_idle(script)

        # Step 5
        elif macro_name == "TB_Edit_Config_UI":
            ok, config = self.ask_attribute_config()
            if ok and config:
                config_str = json.dumps(config, ensure_ascii=False)
                script = f'''
import CAD_basic as cb
import json
print("🚀 [Step 5] 批量编辑图签属性...")
target_map = GLOBAL_CTX.get('ctq')
if not target_map: 
    print("❌ 内存无映射数据")
else:
    config = json.loads(r'{config_str}')
    if hasattr(cb, 'batch_update_block_attributes_config'):
        cb.batch_update_block_attributes_config(target_map, config)
    else:
        print("❌ 错误: 找不到 batch_update_block_attributes_config 函数")
'''
                self.send_script_to_idle(script)

        # Catalog
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
'''
            self.send_script_to_idle(script)

        elif macro_name == "Cat_Step2":
            script = f'''
import CAD_basic as cb
print("🚀 [目录] Step 2: 插入目录图签...")
res = cb.bianmulu_func2(dwg_path=None)
if res: print(f"✅ Step 2 执行成功")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Cat_Step3":
            script = f'''
import CAD_basic as cb
print("🚀 [目录] Step 3: 书写目录...")
res = cb.bianmulu_func3(dwg_path=None, mubanxuhao={ctx['mulu_n']})
if res: print(f"✅ Step 3 执行成功")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Cat_Step4":
            script = f'''
import CAD_basic as cb
print("🚀 [目录] Step 4: 合并到主文件...")
res = cb.bianmulu_func4(dwg_path=None)
if res: print(f"✅ Step 4 执行成功")
'''
            self.send_script_to_idle(script)
        
        # Print
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
            script = f'''
import os
import CAD_basic as cb
os.environ['USERPATH'] = r"{ctx['root']}"
DC.set_root(r"{ctx['root']}")
cb.li()
print("🚀 [Model-List] 列表打印...")
dy = GLOBAL_CTX.get('dy')
if not dy: print("❌ 无内存选区 (请在数据中心获取DY)")
else:
    real_polys = []
    iterable = dy.values() if isinstance(dy, dict) else dy
    for item in iterable:
        try:
            if hasattr(item, 'Handle'): real_polys.append(item)
            elif isinstance(item, dict): 
                p = cb.restore_or_find_poly(item)
                if p: real_polys.append(p)
        except: pass
    output_root = os.path.join(os.environ['USERPATH'], "输出pdf", "List_Print")
    cb.print_polylines_list(real_polys, folderpath=output_root, ctb=r"{ctx['ctb']}", mode="Model")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Print_Layout_File":
            layout_name_user = self.dc_vars["layout_name"].get()
            if not layout_name_user: layout_name_user = "布局1"
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
            layout_name_user = self.dc_vars["layout_name"].get()
            if not layout_name_user: layout_name_user = "布局1"
            script = f'''
import os
import CAD_basic as cb
os.environ['USERPATH'] = r"{ctx['root']}"
DC.set_root(r"{ctx['root']}")
cb.li()
print("🚀 [Layout-List] 列表打印...")
dy = GLOBAL_CTX.get('dy')
if not dy: print("❌ 无内存选区")
else:
    real_polys = []
    iterable = dy.values() if isinstance(dy, dict) else dy
    for item in iterable:
        try:
            if hasattr(item, 'Handle'): real_polys.append(item)
            elif isinstance(item, dict): 
                p = cb.restore_or_find_poly(item)
                if p: real_polys.append(p)
        except: pass
    output_root = os.path.join(os.environ['USERPATH'], "输出pdf", "List_Print")
    cb.print_layout_polylines_list(real_polys, layout_name="{layout_name_user}", folderpath=output_root, ctb=r"{ctx['ctb']}")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Print_Hybrid_File":
            layout_name_user = self.dc_vars["layout_name"].get()
            if not layout_name_user: layout_name_user = "布局1"
            script = f'''
import os
import CAD_basic as cb
os.environ['USERPATH'] = r"{ctx['root']}"
DC.set_root(r"{ctx['root']}")
cb.li()
print("🚀 [Hybrid-File] 混合模式全打印...")
try: cb.print_dwg_file_model_h(file_path=None, ctb=r"{ctx['ctb']}")
except Exception as e: print(f"❌ 模型失败: {{e}}")
try: cb.print_dwg_file_layout_h(file_path=None, layout_name="{layout_name_user}", ctb=r"{ctx['ctb']}")
except Exception as e: print(f"❌ 布局失败: {{e}}")
'''
            self.send_script_to_idle(script)

        elif macro_name == "Print_Hybrid_List":
            script = f'''
import os
import CAD_basic as cb
os.environ['USERPATH'] = r"{ctx['root']}"
DC.set_root(r"{ctx['root']}")
cb.li()
print("🚀 [Hybrid-List] 列表打印 (调用Model)...")
dy = GLOBAL_CTX.get('dy')
if not dy: print("❌ 无内存选区")
else:
    real_polys = []
    iterable = dy.values() if isinstance(dy, dict) else dy
    for item in iterable:
        try:
            if hasattr(item, 'Handle'): real_polys.append(item)
            elif isinstance(item, dict): 
                p = cb.restore_or_find_poly(item)
                if p: real_polys.append(p)
        except: pass
    output_root = os.path.join(os.environ['USERPATH'], "输出pdf", "List_Print")
    cb.print_polylines_list(real_polys, folderpath=output_root, ctb=r"{ctx['ctb']}", mode="Model")
'''
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
