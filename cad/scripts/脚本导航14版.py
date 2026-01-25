#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#脚本导航14版_BOM修复版 20250813
"""
Script Navigator (Tree Edition) - BOM Fixed
修复内容：
1. [关键修复] IDLE_bootstrap.py 读取文件时使用 'utf-8-sig' 编码。
   -> 彻底解决 SyntaxError: invalid non-printable character U+FEFF 问题。
2. 优化运行逻辑：在执行脚本前自动切换 cwd 到脚本所在目录，执行后还原。
"""
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
import tkinter.font as tkfont
import subprocess, sys, os, ctypes, re, hashlib, json
from PIL import Image, ImageTk
import logging
from datetime import datetime, date
import glob
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None

# 日志按日期分割
today = date.today().strftime("%Y-%m-%d")
log_filename = f"script_navigator_{today}.log"

# ================== 核心修复：内置 IDLE 引导程序代码 ==================
IDLE_BOOTSTRAP_CODE = r'''import sys
import os
import socket
import threading
import time
import traceback

HOST = '127.0.0.1'
PORT = 65432

def run_script_in_main(script_path):
    """
    模拟 IDLE 的 'Run Module' (F5)。
    直接在 __main__ 命名空间中执行脚本代码。
    """
    if not os.path.exists(script_path):
        print(f"错误: 找不到文件 {script_path}")
        return

    script_dir = os.path.dirname(script_path)
    script_name = os.path.basename(script_path)

    print(f"\n{'='*60}")
    print(f">>> 正在运行脚本: {script_name}")
    print(f"{'='*60}")

    # 1. 将脚本目录加入 sys.path
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    # 保存当前工作目录，以便执行后还原
    old_cwd = os.getcwd()

    try:
        # 2. 切换工作目录到脚本所在位置 (这对 CAD 脚本读取相对资源很重要)
        os.chdir(script_dir)

        # 3. 读取脚本内容
        # 【关键修复】使用 'utf-8-sig' 自动处理 BOM (\ufeff)
        with open(script_path, 'r', encoding='utf-8-sig') as f:
            code_content = f.read()
        
        # 4. 编译代码
        code = compile(code_content, script_path, 'exec')

        # 5. 获取 __main__ 的字典
        main_mod = sys.modules['__main__']
        
        # 6. 设置 __file__
        main_mod.__file__ = script_path

        # 7. 执行
        exec(code, main_mod.__dict__)

        print(f"✔ 脚本执行完成。")

    except SystemExit:
        print("\n[脚本执行了 sys.exit()]")
    except Exception:
        print(f"✗ 执行出错: {script_name}")
        traceback.print_exc()
    finally:
        # 还原工作目录
        os.chdir(old_cwd)
        
    print(f"{'='*60}\n")
    
    # 【优化】模拟回车效果：手动输出提示符并刷新缓冲区
    # 这样运行结束后，控制台会直接显示 >>>，无需人工按回车
    sys.stdout.write(">>> ")
    sys.stdout.flush()

def start_listener():
    """启动 Socket 监听线程"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
    except OSError:
        print(f"警告: 端口 {PORT} 被占用。如果是之前的 IDLE 进程未关闭，请忽略。")

    print(f"Script Navigator 监听服务已就绪 ({HOST}:{PORT})")

    while True:
        try:
            conn, addr = server_socket.accept()
            with conn:
                data = conn.recv(4096).decode('utf-8', errors='ignore')
                if data.startswith("RUN:"):
                    script_path = data[4:].strip()
                    run_script_in_main(script_path)
        except Exception as e:
            print(f"监听错误: {e}")
            time.sleep(1)

# 启动后台线程监听
t = threading.Thread(target=start_listener, daemon=True)
t.start()

print("\n" + "="*60)
print("          CAD Automation Scripts - IDLE Shell")
print("="*60)
print("  状态: 就绪")
print("  功能: 支持 BOM 格式文件，支持相对路径资源加载")
print("="*60 + "\n")
sys.stdout.write(">>> ") # 启动时也显示一个提示符
sys.stdout.flush()
'''
# ==========================================================================
# 清理非当天的日志文件
def clean_old_logs():
    log_dir = os.path.dirname(log_filename) or "."
    for old_log in glob.glob(os.path.join(log_dir, "script_navigator_*.log")):
        log_date_str = old_log.split("script_navigator_")[-1].split(".log")[0]
        try:
            log_date = datetime.strptime(log_date_str, "%Y-%m-%d").date()
            if log_date != date.today():
                os.remove(old_log)
                logging.debug(f"删除旧日志文件: {old_log}")
        except (ValueError, OSError) as e:
            logging.debug(f"清理旧日志失败: {str(e)}")

logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)

SCRIPT_DIR = Path(__file__).resolve().parent
REGISTRY_FILE = SCRIPT_DIR / "script_navigator_registry.json"
LAUNCH_IDLE_BAT = SCRIPT_DIR / "launch_idle.bat"


def _normalize_registry_path(path: str | None) -> str | None:
    if not path:
        return None
    try:
        return str(Path(path).resolve())
    except Exception:
        try:
            return os.path.abspath(path)
        except Exception:
            return path


def _pid_exists(pid: int) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    if pid == os.getpid():
        return True
    if sys.platform.startswith("win"):
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if handle:
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _read_registry_data() -> dict:
    if not REGISTRY_FILE.exists():
        return {}
    try:
        data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception as exc:
        logging.debug(f"读取脚本注册表失败: {exc}")
    return {}


def _write_registry_data(data: dict) -> None:
    try:
        REGISTRY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as exc:
        logging.debug(f"写入脚本注册表失败: {exc}")


def _cleanup_registry_data(data: dict) -> bool:
    changed = False
    for key in list(data.keys()):
        entries = data.get(key, [])
        if not isinstance(entries, list):
            data.pop(key, None)
            changed = True
            continue
        unique = []
        seen = set()
        for pid in entries:
            if isinstance(pid, int) and pid not in seen:
                seen.add(pid)
                unique.append(pid)
        live = [pid for pid in unique if _pid_exists(pid)]
        if live:
            if live != entries:
                changed = True
            data[key] = live
        else:
            data.pop(key, None)
            changed = True
    return changed


def _load_clean_registry() -> dict:
    data = _read_registry_data()
    if _cleanup_registry_data(data):
        _write_registry_data(data)
    return data

# ================== 配置 ==================
DEFAULT_OPEN_FILE = r"D:/gemini-tasks/cad/scripts/修复codex脚本.py"

# ================== 解析器 ==================
def parse_mark_line(raw: str):
    s = raw.lstrip().lstrip("\ufeff")
    if s.startswith("#&&&&%%"):
        return 1, s[len("#&&&&%%"):].strip()
    if s.startswith("#&&&%"):
        return 2, s[len("#&&&%"):].strip()
    if s.startswith("#&&%"):
        return 3, s[len("#&&%"):].strip()
    return None

# ================== 隐藏控制台（Windows） ==================
if sys.platform.startswith("win"):
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)
    except Exception:
        pass

def is_file_in_use(filepath):
    if not psutil:
        logging.warning("psutil 模块未安装，文件占用检查功能已禁用。")
        if not getattr(is_file_in_use, "warned", False):
            is_file_in_use.warned = True
        return False

    if not filepath or not os.path.exists(filepath):
        return False

    norm_filepath = os.path.normcase(os.path.abspath(filepath))
    current_pid = os.getpid()

    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        if proc.info['pid'] == current_pid:
            continue
        try:
            if proc.info['open_files'] is not None:
                for file in proc.info['open_files']:
                    if os.path.normcase(os.path.abspath(file.path)) == norm_filepath:
                        logging.info(f"文件 '{filepath}' 被进程 '{proc.info['name']}' (pid: {proc.pid}) 打开。")
                        return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception as e:
            logging.debug(f"检查进程 {proc.pid} 时出错: {e}")
            continue
    return False

def _tree_walk(tree, parent=""):
    for child in tree.get_children(parent):
        yield child
        yield from _tree_walk(tree, child)

try:
    from idlelib.percolator import Percolator
    from idlelib.colorizer import ColorDelegator
except ImportError:
    Percolator = ColorDelegator = None

class ScriptNavigator(tk.Tk):
    def __init__(self, script_path=None):
        super().__init__()
        logging.debug("初始化 ScriptNavigator 开始")
        clean_old_logs()
        
        # 确保 IDLE 引导程序是最新的
        self._ensure_idle_bootstrap()

        self.title("Script Navigator (Tree Edition)")
        self.geometry("1200x780")
        # 状态
        self.font_size = 11
        self.script_path = None
        self._current_reg_key = None
        self._last_mod_time = None
        self._loaded_content_hash = None
        self.find_matches = []
        self.find_index = -1
        self._node_line_map = {}
        self._idle_proc = None
        self._nav_line_digits = 3
        self._nav_refresh_job = None
        self._last_nav_content_sig = ""
        self._gutter_digits = 3
        self._nav_hl_iid = None
        self._suppress_clear = False
        self._popup_window = None
        self._popup_image = None
        self._original_img = None
        self.popup_canvas = None
        self.popup_image_item = None
        self._image_tags = {}
        self._image_scale = 1.0
        self._link_tags = {}
        self._link_delay = 5000
        self._is_maximized = False
        self._font_level1 = None
        self._font_level2 = None
        self._font_level3 = None
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_ui()
        self._bind_shortcuts()
        
        initial_target = script_path
        if initial_target and os.path.isfile(initial_target):
            logging.debug(f"加载初始脚本: {initial_target}")
            self.load_script(initial_target)
        else:
            if not initial_target:
                default_target = DEFAULT_OPEN_FILE
                if os.path.exists(default_target):
                    logging.debug(f"加载默认脚本: {default_target}")
                    self.load_script(default_target)
                else:
                    self._open_script()
            else:
                self._open_script()
        logging.debug("初始化 ScriptNavigator 完成")

    def _ensure_idle_bootstrap(self):
        """检查并更新/创建 IDLE_bootstrap.py 文件"""
        bootstrap_path = SCRIPT_DIR / "IDLE_bootstrap.py"
        try:
            with open(bootstrap_path, "w", encoding="utf-8") as f:
                f.write(IDLE_BOOTSTRAP_CODE)
            logging.info(f"已更新 IDLE_bootstrap.py: {bootstrap_path}")
        except Exception as e:
            logging.error(f"无法写入 IDLE_bootstrap.py: {e}")
            messagebox.showwarning("警告", f"无法更新 IDLE 引导程序，运行可能会出错: {e}")

    # ---------- UI ----------
    def _build_ui(self):
        logging.debug("构建 UI 开始")
        self.pw = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief="raised")
        self.pw.pack(fill=tk.BOTH, expand=True)
        self.nav_frm = tk.Frame(self.pw, width=320)
        self.pw.add(self.nav_frm)
        self.nav_tree = ttk.Treeview(self.nav_frm, show="tree", selectmode="browse")
        self.nav_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        nav_scroll = tk.Scrollbar(self.nav_frm, orient=tk.VERTICAL, command=self.nav_tree.yview)
        nav_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.nav_tree.configure(yscrollcommand=nav_scroll.set)
        self.nav_tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        try:
            self.nav_tree.tag_configure("NAV_HL", background="#fff799")
        except Exception:
            pass
        self.edit_frm = tk.Frame(self.pw)
        self.pw.add(self.edit_frm)
        self.gutter = tk.Text(
            self.edit_frm, width=6, padx=4, takefocus=0,
            state="disabled", background="#f0f0f0", foreground="#888",
            wrap="none", relief=tk.FLAT
        )
        self.gutter.pack(side=tk.LEFT, fill=tk.Y)
        self.code = tk.Text(self.edit_frm, wrap="none", undo=True, tabs=("4c",))
        self.code.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.hbar = tk.Scrollbar(self.edit_frm, orient=tk.HORIZONTAL, command=self.code.xview)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.code.configure(xscrollcommand=self.hbar.set)
        self.vbar = tk.Scrollbar(self.edit_frm, orient=tk.VERTICAL, command=self._on_scrollbar)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.code.configure(yscrollcommand=self._on_code_yscroll)
        if Percolator and ColorDelegator:
            Percolator(self.code).insertfilter(ColorDelegator())
        bar = tk.Frame(self)
        bar.pack(fill=tk.X)
        for t, c in [
            ("打开 (Ctrl+O)", self._open_new_file),
            ("保存 (Ctrl+S)", self.save_script),
            ("运行 (Ctrl+F5)", self.run_in_idle),
            ("刷新导航", self._refresh_nav),
            ("折叠全部", self._collapse_all),
            ("展开全部", self._expand_all),
            ("A+", self._zoom_in), ("A-", self._zoom_out),
            ("复制全部", self._copy_all),
            ("复制选中", self._copy_sel),
            ("查找 (Ctrl+F)", self._find_dialog),
            ("转到行 (Alt+G)", self.goto_line_prompt),
        ]:
            tk.Button(bar, text=t, command=c).pack(side=tk.LEFT, padx=4, pady=2)
        self.code.bind("<MouseWheel>", self._on_mousewheel_sync)
        self.code.bind("<KeyRelease>", self._on_key_release_update)
        self.code.bind("<Configure>", lambda e: self._schedule_line_numbers())
        self.code.bind("<<Modified>>", self._on_text_modified)
        self.code.tag_config("find_highlight", background="#a6e3ff")
        self.code.tag_config("nav_pick", background="#ffff66")
        self.code.tag_config("image_marker", foreground="blue", underline=True)
        self.code.tag_bind("image_marker", "<Button-1>", self._on_click_image_marker)
        self.code.tag_config("link_marker", foreground="blue", underline=True)
        self.code.tag_bind("link_marker", "<Button-1>", self._on_click_link)
        self._apply_fonts()
        self.after(50, self.update_line_numbers)
        logging.debug("构建 UI 完成")

    # ---------- 快捷键 ----------
    def _bind_shortcuts(self):
        self.bind_all("<Control-o>", lambda e: (self._open_new_file(), "break"))
        self.bind_all("<Control-s>", lambda e: (self.save_script(), "break"))
        self.bind_all("<Control-F5>", lambda e: (self.run_in_idle(), "break"))
        self.bind_all("<Control-MouseWheel>", self._on_mousewheel_zoom)
        self.bind_all("<Control-f>", lambda e: (self._find_dialog(), "break"))
        self.bind_all("<F3>", lambda e: (self._find_next(), "break"))
        self.bind_all("<F2>", lambda e: (self._find_prev(), "break"))
        self.bind_all("<Alt-g>", lambda e: (self.goto_line_prompt(), "break"))
        self.bind_all("<Alt-G>", lambda e: (self.goto_line_prompt(), "break"))
        self.bind_all("<Control-bracketleft>", lambda e: (self._unindent(e), "break"))
        self.bind_all("<Control-bracketright>", lambda e: (self._indent(e), "break"))
        comment_cb = lambda e: (self._comment_selection(), "break")
        uncomment_cb = lambda e: (self._uncomment_selection(), "break")
        for key in ("<Alt-KeyPress-3>", "<Alt-3>", "<Alt-KeyPress-KP_3>"):
            self.bind_all(key, comment_cb)
        for key in ("<Alt-KeyPress-4>", "<Alt-4>", "<Alt-KeyPress-KP_4>"):
            self.bind_all(key, uncomment_cb)
        self.code.bind("<Tab>", self._indent)
        self.code.bind("<Shift-Tab>", self._unindent)

    # ---------- 字体/缩放 ----------
    def _apply_fonts(self):
        base = tkfont.nametofont("TkFixedFont")
        base.configure(size=self.font_size)
        self.code.configure(font=base)
        self.gutter.configure(font=base)
        self._font_level1 = base.copy()
        self._font_level1.configure(size=self.font_size + 2, weight="bold")
        self._font_level2 = base.copy()
        self._font_level2.configure(weight="bold")
        self._font_level3 = base.copy()
        style = ttk.Style()
        style.configure("Treeview", font=base)
        try:
            self.nav_tree.tag_configure("L1", font=self._font_level1)
            self.nav_tree.tag_configure("L2", font=self._font_level2)
            self.nav_tree.tag_configure("L3", font=self._font_level3)
        except Exception:
            pass
        self.code.tag_config("find_highlight", background="#a6e3ff")
        self.code.tag_config("nav_pick", background="#ffff66")
        self.after(10, self._auto_resize_nav)
        self.after(20, self.update_line_numbers)

    def _zoom_in(self):
        self.font_size = min(self.font_size + 1, 42)
        self._apply_fonts()
        self._refresh_nav()

    def _zoom_out(self):
        self.font_size = max(self.font_size - 1, 6)
        self._apply_fonts()
        self._refresh_nav()

    def _on_mousewheel_zoom(self, e):
        if e.delta > 0:
            self._zoom_in()
        else:
            self._zoom_out()
        return "break"

    # ---------- 滚动同步 ----------
    def _on_mousewheel_sync(self, _):
        self.after_idle(self.update_line_numbers)

    def _on_scrollbar(self, *args):
        self.code.yview(*args)
        self.gutter.yview(*args)
        self.update_line_numbers()

    def _on_code_yscroll(self, *args):
        self.vbar.set(*args)
        self.gutter.yview_moveto(args[0])
        self.after_idle(self.update_line_numbers)

    # ---------- 行号 ----------
    def _schedule_line_numbers(self):
        self.after_idle(self.update_line_numbers)

    def update_line_numbers(self):
        try:
            first_visible = int(self.code.index("@0,0").split('.')[0])
            last_visible = int(self.code.index(f"@0,{self.code.winfo_height()}").split('.')[0])
        except Exception:
            return
        total_lines = int(self.code.index("end-1c").split('.')[0])
        last_visible = min(last_visible + 1, total_lines)
        digits = max(3, len(str(total_lines)))
        if digits != self._gutter_digits:
            self._gutter_digits = digits
            self.gutter.config(width=digits + 2)
        lines = [f"{ln:>{digits}} " for ln in range(first_visible, last_visible + 1)]
        new_text = "\n".join(lines)
        self.gutter.config(state="normal")
        self.gutter.delete("1.0", tk.END)
        self.gutter.insert("1.0", new_text)
        self.gutter.config(state="disabled")

    # ---------- 内容修改 / 导航刷新 ----------
    def _on_key_release_update(self, _):
        self._schedule_line_numbers()

    def _on_text_modified(self, _):
        if self.code.edit_modified():
            self.code.edit_modified(False)
            self._schedule_line_numbers()
            if not self._suppress_clear:
                self._clear_nav_and_code_highlight()
                self.nav_tree.selection_remove(self.nav_tree.selection())
            self._schedule_nav_refresh()
            self._scan_for_markers()

    def _schedule_nav_refresh(self, delay=500):
        if self._nav_refresh_job:
            self.after_cancel(self._nav_refresh_job)
        self._nav_refresh_job = self.after(delay, self._maybe_refresh_nav)

    def _content_signature(self):
        txt = self.code.get("1.0", "end-1c")
        md5 = hashlib.md5(txt.encode("utf-8")).hexdigest()
        sig = f"{len(txt)}:{md5}"
        return sig

    def _maybe_refresh_nav(self):
        sig = self._content_signature()
        if sig != self._last_nav_content_sig:
            self._last_nav_content_sig = sig
            self._refresh_nav()

    # ---------- 文件 ----------
    def _open_script(self):
        p = filedialog.askopenfilename(
            title="选择脚本",
            filetypes=[("Python", "*.py"), ("全部", "*.*")]
        )
        if p:
            self.load_script(p)


    def _open_new_file(self):
            # 【优化】打开新文件时，不再检查或强制保存当前文件
            # if self.script_path:
            #     try:
            #         if not self.save_script():
            #             return
            #     except Exception as e:
            #         logging.debug(f"保存失败: {str(e)}")
            #         return
            self._open_script()


    def load_script(self, path):
        normalized_target = _normalize_registry_path(path)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                txt = f.read()
            self._last_mod_time = os.path.getmtime(path)
            self._loaded_content_hash = hashlib.md5(txt.encode("utf-8", "replace")).hexdigest()
        except Exception as e:
            logging.debug(f"加载失败: {str(e)}")
            messagebox.showerror("打开失败", str(e))
            return

        if self._current_reg_key and normalized_target != self._current_reg_key:
            self._unregister_current_file()

        self.code.delete("1.0", tk.END)
        self.code.insert("1.0", txt)
        self.code.edit_reset()
        self.title(f"Script Navigator – {os.path.basename(path)}")
        self._last_nav_content_sig = self._content_signature()
        self._refresh_nav()
        self.update_line_numbers()
        self._scan_for_markers()
        self.script_path = path
        self._register_file_session(normalized_target)

    def _register_file_session(self, normalized_path: str | None):
        if not normalized_path:
            self._current_reg_key = None
            return
        data = _load_clean_registry()
        entries = list(data.get(normalized_path, []))
        if os.getpid() not in entries:
            entries.append(os.getpid())
            data[normalized_path] = entries
            _write_registry_data(data)
        self._current_reg_key = normalized_path

    def _unregister_current_file(self):
        key = self._current_reg_key
        if not key:
            return
        data = _load_clean_registry()
        if key not in data:
            self._current_reg_key = None
            return
        entries = [pid for pid in data[key] if pid != os.getpid()]
        if entries:
            data[key] = entries
        else:
            data.pop(key, None)
        _write_registry_data(data)
        self._current_reg_key = None

    def save_script(self):
        if not self.script_path:
            self._open_script()
            if not self.script_path:
                return False

        msg = "请检查该文件是否被别的软件打开，可能造成版本冲突！\n\n您确定要继续保存吗？"
        if not messagebox.askyesno("保存警告", msg):
            return False

        try:
            content_to_save = self.code.get("1.0", tk.END)
            with open(self.script_path, "w", encoding="utf-8") as f:
                f.write(content_to_save)
            
            self._last_mod_time = os.path.getmtime(self.script_path)
            self._loaded_content_hash = hashlib.md5(content_to_save.encode("utf-8", "replace")).hexdigest()
            
            self._last_nav_content_sig = self._content_signature()
            self._refresh_nav()
            self._scan_for_markers()
            messagebox.showinfo("保存", "保存成功")
            return True
        except Exception as e:
            logging.error(f"保存脚本时发生严重错误: {e}")
            messagebox.showerror("保存失败", str(e))
            return False

    # ---------- 导航 ----------
    def _format_nav_label(self, lineno: int, label: str) -> str:
        return f"{lineno:>{self._nav_line_digits}} {label}"

    def _refresh_nav(self):
        open_lines = set()
        selected_line = None
        for iid in _tree_walk(self.nav_tree):
            ln = self._node_line_map.get(iid)
            if ln is None:
                continue
            if self.nav_tree.item(iid, "open"):
                open_lines.add(ln)
            if iid in self.nav_tree.selection():
                selected_line = ln
        
        for item in self.nav_tree.get_children():
            self.nav_tree.delete(item)
        self._node_line_map.clear()
        
        lines = self.code.get("1.0", tk.END).splitlines()
        total = len(lines)
        self._nav_line_digits = max(3, len(str(total)))
        
        stack = [None, None, None]
        for idx, raw in enumerate(lines, start=1):
            parsed = parse_mark_line(raw)
            if not parsed:
                continue
            level, label = parsed
            if level == 1:
                parent = ""
            elif level == 2:
                parent = stack[0] or ""
            else:
                parent = stack[1] or stack[0] or ""
            tag = f"L{level}"
            display = self._format_nav_label(idx, label)
            node_id = self.nav_tree.insert(
                parent, "end", text=display,
                open=(idx in open_lines),
                values=(idx,), tags=(tag,)
            )
            stack[level - 1] = node_id
            for deeper in range(level, 3):
                stack[deeper] = None
            self._node_line_map[node_id] = idx
            
        if selected_line:
            for iid, ln in self._node_line_map.items():
                if ln == selected_line:
                    self.nav_tree.selection_set(iid)
                    break
        try:
            self.nav_tree.tag_configure("L1", font=self._font_level1)
            self.nav_tree.tag_configure("L2", font=self._font_level2)
            self.nav_tree.tag_configure("L3", font=self._font_level3)
            self.nav_tree.tag_configure("NAV_HL", background="#fff799")
        except Exception:
            pass
        self._auto_resize_nav()
        if self._nav_hl_iid and self._nav_hl_iid not in self._node_line_map:
            self._nav_hl_iid = None

    def _collapse_all(self):
        for n in self.nav_tree.get_children():
            self.nav_tree.item(n, open=False)
            for c in self.nav_tree.get_children(n):
                self.nav_tree.item(c, open=False)

    def _expand_all(self):
        def open_rec(iid):
            self.nav_tree.item(iid, open=True)
            for c in self.nav_tree.get_children(iid):
                open_rec(c)
        for n in self.nav_tree.get_children():
            open_rec(n)

    def _on_tree_select(self, _):
        sel = self.nav_tree.selection()
        if not sel:
            return
        iid = sel[0]
        ln = self._node_line_map.get(iid)
        if ln:
            self._nav_select_and_highlight(iid, ln)

    def _nav_select_and_highlight(self, iid, line_no: int):
        self._clear_nav_highlight_only()
        self._add_nav_tag(iid, "NAV_HL")
        self._nav_hl_iid = iid
        self._highlight_line(line_no)

    def _highlight_line(self, ln: int, source="unknown"):
        try:
            self.code.tag_remove("nav_pick", "1.0", tk.END)
            self.code.see(f"{ln}.0")
            self.code.tag_add("nav_pick", f"{ln}.0", f"{ln}.0 lineend")
            self.update_line_numbers()
            self.update_idletasks()
            self.after(2000, lambda: self.code.tag_remove("nav_pick", "1.0", tk.END))
        except Exception:
            pass

    def _auto_resize_nav(self):
        measure_font = self._font_level1 or tkfont.nametofont("TkFixedFont")
        line_space = measure_font.metrics("linespace")
        row_h = line_space + max(4, int(line_space * 0.25))
        style = ttk.Style()
        style.configure("Treeview", rowheight=row_h)
        def iter_nodes(parent=""):
            for iid in self.nav_tree.get_children(parent):
                yield self.nav_tree.item(iid, "text")
                yield from iter_nodes(iid)
        max_px = 0
        for txt in iter_nodes():
            w = measure_font.measure(txt)
            if w > max_px:
                max_px = w
        char_w = measure_font.measure("0")
        indent_comp = char_w * 2 * 3 + 24
        padding_comp = char_w * 2
        total_needed = max_px + indent_comp + padding_comp
        min_w = 240 + (self.font_size - 10) * 6
        max_w = 700
        final_w = max(min_w, min(total_needed, max_w))
        try:
            self.nav_tree.column("#0", width=int(final_w), stretch=False)
        except Exception:
            pass
        self.nav_frm.update_idletasks()

    # ---------- 缩进 ----------
    def _indent(self, event):
        try:
            start = self.code.index("sel.first")
            end = self.code.index("sel.last")
            l1 = int(start.split('.')[0])
            l2 = int(end.split('.')[0])
            for ln in range(l1, l2 + 1):
                self.code.insert(f"{ln}.0", " " * 4)
        except tk.TclError:
            self.code.insert("insert", " " * 4)
        return "break"

    def _unindent(self, event):
        try:
            start = self.code.index("sel.first")
            end = self.code.index("sel.last")
            l1 = int(start.split('.')[0])
            l2 = int(end.split('.')[0])
        except tk.TclError:
            pos = self.code.index("insert")
            l1 = l2 = int(pos.split('.')[0])
        for ln in range(l1, l2 + 1):
            line0 = f"{ln}.0"
            frag = self.code.get(line0, f"{ln}.0+4c")
            rm = min(4, len(frag) - len(frag.lstrip(" ")))
            if rm > 0:
                self.code.delete(line0, f"{ln}.0+{rm}c")
        return "break"

    # ---------- 批量注释 ----------
    def _comment_selection(self, event=None):
        line_range = self._get_selection_line_range()
        if not line_range:
            return "break"
        start_line, end_line = line_range
        self.code.edit_separator()
        for ln in range(start_line, end_line + 1):
            line_start = f"{ln}.0"
            raw = self.code.get(line_start, f"{line_start} lineend")
            indent_len = self._leading_ws_len(raw)
            insert_pos = f"{ln}.{indent_len}"
            prefix = self.code.get(insert_pos, f"{insert_pos}+2c")
            if prefix == "##":
                continue
            self.code.insert(insert_pos, "##")
        self.code.edit_separator()
        return "break"

    def _uncomment_selection(self, event=None):
        line_range = self._get_selection_line_range()
        if not line_range:
            return "break"
        start_line, end_line = line_range
        self.code.edit_separator()
        for ln in range(start_line, end_line + 1):
            line_start = f"{ln}.0"
            raw = self.code.get(line_start, f"{line_start} lineend")
            indent_len = self._leading_ws_len(raw)
            remove_pos = f"{ln}.{indent_len}"
            prefix = self.code.get(remove_pos, f"{remove_pos}+2c")
            if prefix == "##":
                self.code.delete(remove_pos, f"{remove_pos}+2c")
        self.code.edit_separator()
        return "break"

    def _get_selection_line_range(self):
        try:
            start = self.code.index("sel.first")
            end = self.code.index("sel.last")
        except tk.TclError:
            messagebox.showinfo("提示", "请先选择需要处理的代码块。")
            return None
        start_line = int(start.split('.')[0])
        end_line = int(end.split('.')[0])
        return start_line, end_line

    @staticmethod
    def _leading_ws_len(text: str) -> int:
        count = 0
        for ch in text:
            if ch in (" ", "\t"):
                count += 1
            else:
                break
        return count

    # ---------- 查找/复制/跳转 ----------
    def _find_dialog(self, _=None):
        key = simpledialog.askstring("查找", "输入要查找的字符串：", parent=self)
        if not key:
            return "break"
        self._do_find(key)
        return "break"

    def _do_find(self, key):
        self.code.tag_remove("find_highlight", "1.0", tk.END)
        self.find_matches.clear()
        idx = "1.0"
        while True:
            pos = self.code.search(key, idx, stopindex=tk.END)
            if not pos:
                break
            self.find_matches.append(pos)
            end = f"{pos}+{len(key)}c"
            self.code.tag_add("find_highlight", pos, end)
            idx = end
        if not self.find_matches:
            messagebox.showinfo("查找", f"未找到：{key}")
            return
        self.find_index = 0
        self._go_to_match()

    def _go_to_match(self):
        pos = self.find_matches[self.find_index]
        ln = int(pos.split('.')[0])
        self._highlight_line(ln)

    def _find_next(self, _=None):
        if not self.find_matches:
            return "break"
        self.find_index = (self.find_index + 1) % len(self.find_matches)
        self._go_to_match()
        return "break"

    def _find_prev(self, _=None):
        if not self.find_matches:
            return "break"
        self.find_index = (self.find_index - 1) % len(self.find_matches)
        self._go_to_match()
        return "break"

    def _copy_all(self):
        self.clipboard_clear()
        self.clipboard_append(self.code.get("1.0", tk.END))
        messagebox.showinfo("复制", "已复制全部代码")

    def _copy_sel(self):
        try:
            txt = self.code.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            txt = ""
        if not txt:
            messagebox.showwarning("未选中", "请先选中文本")
        else:
            self.clipboard_clear()
            self.clipboard_append(txt)
            messagebox.showinfo("复制", "已复制选中文本")

    def goto_line_prompt(self):
        total = int(float(self.code.index("end-1c").split('.')[0]))
        line = simpledialog.askinteger(
            "转到行", f"输入行号 (1 - {total}):",
            parent=self, minvalue=1, maxvalue=total
        )
        if line:
            self._highlight_line(line)

    # ---------- 运行 ----------
    def run_in_idle(self):
        if not self.script_path:
            messagebox.showwarning("未保存", "请先保存脚本")
            return
        if not self.save_script():
            return

        try:
            idle_running = False
            if self._idle_proc and self._idle_proc.poll() is None:
                idle_running = True
                logging.debug("IDLE 进程已运行，复用现有窗口")

            if not idle_running:
                logging.debug("启动新的 IDLE 进程")
                idle_script = SCRIPT_DIR / "IDLE_bootstrap.py"
                
                if not idle_script.exists():
                    self._ensure_idle_bootstrap()
                    if not idle_script.exists():
                        messagebox.showerror("运行失败", f"未找到 {idle_script}")
                        return

                cmd = [
                    sys.executable,
                    "-m", "idlelib.idle",
                    "-r", str(idle_script)
                ]

                startupinfo = None
                creationflags = 0
                if sys.platform.startswith("win"):
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = 0 
                    creationflags = subprocess.CREATE_NO_WINDOW

                self._idle_proc = subprocess.Popen(
                    cmd,
                    startupinfo=startupinfo,
                    creationflags=creationflags,
                    cwd=str(SCRIPT_DIR)
                )
                
                # 等待IDLE启动
                import time
                time.sleep(2)

            self._send_script_to_idle(self.script_path)

        except Exception as e:
            logging.error(f"运行失败: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            messagebox.showerror("运行失败", str(e))

    def _send_script_to_idle(self, script_path):
        import socket
        import time

        HOST = '127.0.0.1'
        PORT = 65432

        max_retries = 5
        for attempt in range(max_retries):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((HOST, PORT))
                    message = f"RUN:{script_path}"
                    s.sendall(message.encode('utf-8'))
                    logging.debug(f"成功发送脚本路径到 IDLE: {script_path}")
                    return True
            except (ConnectionRefusedError, socket.timeout):
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    messagebox.showerror("连接失败", "无法连接到 IDLE，请检查 IDLE 是否正常运行")
                    return False
            except Exception as e:
                messagebox.showerror("发送失败", str(e))
                return False
        return False


    # ---------- 关闭 ----------
    def _on_close(self):
        try:
            if self._idle_proc and self._idle_proc.poll() is None:
                self._idle_proc.terminate()
        except Exception:
            pass
        self._unregister_current_file()
        self.destroy()
        sys.exit(0)

    # ================== 辅助函数 ==================
    def _add_nav_tag(self, iid, tag):
        tags = list(self.nav_tree.item(iid, "tags"))
        if tag not in tags:
            tags.append(tag)
            self.nav_tree.item(iid, tags=tuple(tags))

    def _remove_nav_tag(self, iid, tag):
        tags = [t for t in self.nav_tree.item(iid, "tags") if t != tag]
        self.nav_tree.item(iid, tags=tuple(tags))

    def _clear_nav_highlight_only(self):
        if self._nav_hl_iid and self.nav_tree.exists(self._nav_hl_iid):
            self._remove_nav_tag(self._nav_hl_iid, "NAV_HL")
        self._nav_hl_iid = None

    def _clear_nav_and_code_highlight(self):
        self._clear_nav_highlight_only()
        self.code.tag_remove("nav_pick", "1.0", tk.END)

    def _scan_for_markers(self):
        self.code.tag_remove("image_marker", "1.0", tk.END)
        self.code.tag_remove("link_marker", "1.0", tk.END)
        self._image_tags.clear()
        self._link_tags.clear()
        text = self.code.get("1.0", tk.END)
        lines = text.splitlines()
        for match in re.finditer(r'""".*?"""', text, re.DOTALL):
            comment = match.group(0)
            start_idx = text[:match.start()].count('\n') + 1
            for md_match in re.finditer(r'(!?)\[(.*?)\]\((.*?)\)', comment):
                is_image = md_match.group(1) == '!'
                text_content = md_match.group(2)
                target = md_match.group(3).strip()
                rel_start = md_match.start()
                line_offset = comment[:rel_start].count('\n')
                col_start = rel_start - comment.rfind('\n', 0, rel_start) - 1
                md_start = f"{start_idx + line_offset}.{col_start}"
                md_end = f"{start_idx + line_offset}.{col_start + md_match.end() - md_match.start()}"
                if is_image:
                    unique_tag = f"img_{len(self._image_tags)}"
                    self.code.tag_add("image_marker", md_start, md_end)
                    self.code.tag_add(unique_tag, md_start, md_end)
                    self._image_tags[unique_tag] = target
                else:
                    unique_tag = f"link_{len(self._link_tags)}"
                    self.code.tag_add("link_marker", md_start, md_end)
                    self.code.tag_add(unique_tag, md_start, md_end)
                    try:
                        target_line = int(target)
                        self._link_tags[unique_tag] = target_line
                    except ValueError:
                        pattern = r'^\s*def\s+' + re.escape(target) + r'\b\s*\('
                        found = False
                        for i, line in enumerate(lines, 1):
                            if re.match(pattern, line):
                                self._link_tags[unique_tag] = i
                                found = True
                                break

    def _on_click_image_marker(self, event):
        pos = self.code.index(f"@{event.x},{event.y}")
        tags = self.code.tag_names(pos)
        for tag in tags:
            if tag.startswith("img_"):
                path = self._image_tags.get(tag)
                if path and os.path.isfile(path):
                    self._show_image_popup(path, event)
                break

    def _show_image_popup(self, path, event):
        self._hide_image_popup()
        try:
            if not os.path.isfile(path):
                messagebox.showerror("图片加载失败", f"图片文件不存在: {path}")
                return
            self._original_img = Image.open(path)
            orig_width, orig_height = self._original_img.size
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            max_win_w = int(screen_w * 0.8)
            max_win_h = int(screen_h * 0.8)
            if self._image_scale == 1.0:
                fit_scale = min(float(max_win_w) / orig_width, float(max_win_h) / orig_height, 1.0)
                self._image_scale = fit_scale
            new_width = int(orig_width * self._image_scale)
            new_height = int(orig_height * self._image_scale)
            if new_width < 1 or new_height < 1:
                return
            resized_img = self._original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self._popup_image = ImageTk.PhotoImage(resized_img)
            self._popup_window = tk.Toplevel(self)
            self._popup_window.title("Image Viewer")
            self._popup_window.attributes("-topmost", True)
            
            button_frame = tk.Frame(self._popup_window)
            button_frame.pack(side=tk.TOP, fill=tk.X)
            close_button = tk.Button(button_frame, text="X", command=self._hide_image_popup)
            close_button.pack(side=tk.RIGHT, padx=5, pady=5)
            maximize_button = tk.Button(button_frame, text="□", command=self._toggle_maximize)
            maximize_button.pack(side=tk.RIGHT, padx=5, pady=5)
            
            self.popup_canvas = tk.Canvas(self._popup_window, bg="white")
            self.popup_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            vbar = tk.Scrollbar(self._popup_window, orient=tk.VERTICAL, command=self.popup_canvas.yview)
            vbar.pack(side=tk.RIGHT, fill=tk.Y)
            hbar = tk.Scrollbar(self._popup_window, orient=tk.HORIZONTAL, command=self.popup_canvas.xview)
            hbar.pack(side=tk.BOTTOM, fill=tk.X)
            self.popup_canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.popup_image_item = self.popup_canvas.create_image(0, 0, anchor=tk.NW, image=self._popup_image)
            self.popup_canvas.configure(scrollregion=(0, 0, new_width, new_height))
            self.popup_canvas.bind("<MouseWheel>", self._on_popup_mousewheel)
            self.popup_canvas.bind("<Double-Button-1>", self._toggle_maximize)
            
            self._normal_geometry = f"{min(max_win_w, new_width + vbar.winfo_reqwidth())}x{min(max_win_h, new_height + hbar.winfo_reqheight())}"
            x = self.winfo_pointerx() + 20
            y = self.winfo_pointery() + 20
            self._popup_window.geometry(f"{self._normal_geometry}+{x}+{y}")
        except Exception as e:
            messagebox.showerror("图片加载失败", f"无法加载图片 {path}: {str(e)}")

    def _hide_image_popup(self):
        if self._popup_window:
            self._popup_window.destroy()
            self._popup_window = None
            self._popup_image = None
            self._original_img = None
            self.popup_canvas = None
            self.popup_image_item = None
            self._image_scale = 1.0
            self._is_maximized = False

    def _toggle_maximize(self, event=None):
        if self._popup_window is None:
            return
        if self._is_maximized:
            self._popup_window.geometry(self._normal_geometry)
            self._is_maximized = False
        else:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            self._popup_window.geometry(f"{screen_w}x{screen_h}+0+0")
            self._is_maximized = True
        self.update_idletasks()

    def _on_popup_mousewheel(self, event):
        if self._original_img is None:
            return
        if event.delta > 0:
            zoom_factor = 1.1
        else:
            zoom_factor = 0.9
        new_scale = self._image_scale * zoom_factor
        if new_scale < 0.1 or new_scale > 10.0:
            return
        mouse_x = self.popup_canvas.canvasx(event.x)
        mouse_y = self.popup_canvas.canvasy(event.y)
        self._image_scale = new_scale
        orig_width, orig_height = self._original_img.size
        new_width = int(orig_width * self._image_scale)
        new_height = int(orig_height * self._image_scale)
        if new_width < 1 or new_height < 1:
            return
        try:
            resized_img = self._original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self._popup_image = ImageTk.PhotoImage(resized_img)
            self.popup_canvas.itemconfig(self.popup_image_item, image=self._popup_image)
            self.popup_canvas.configure(scrollregion=(0, 0, new_width, new_height))
            canvas_w = self.popup_canvas.winfo_width()
            canvas_h = self.popup_canvas.winfo_height()
            scroll_x = (mouse_x * zoom_factor - canvas_w / 2) / new_width
            scroll_y = (mouse_y * zoom_factor - canvas_h / 2) / new_height
            scroll_x = max(0, min(scroll_x, 1 - canvas_w / new_width))
            scroll_y = max(0, min(scroll_y, 1 - canvas_h / new_height))
            self.popup_canvas.xview_moveto(scroll_x)
            self.popup_canvas.yview_moveto(scroll_y)
        except Exception as e:
            messagebox.showerror("缩放失败", f"图片缩放失败: {str(e)}")

    def _on_click_link(self, event):
        pos = self.code.index(f"@{event.x},{event.y}")
        tags = self.code.tag_names(pos)
        unique_tag = None
        for tag in tags:
            if tag.startswith("link_") and tag != "link_marker" and tag[len("link_"):].isdigit():
                unique_tag = tag
                break
        if unique_tag:
            target_line = self._link_tags.get(unique_tag)
            if target_line:
                try:
                    current_view = self.code.yview()
                    self._highlight_line(target_line, source="link")
                    self.after(self._link_delay, lambda: self.code.yview_moveto(current_view[0]))
                except Exception:
                    pass

# ================== 主入口 ==================
if __name__ == "__main__":
    start_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OPEN_FILE
    app = ScriptNavigator(start_file)
    app.mainloop()
