#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#脚本导航14版 20250813
"""
Script Navigator (Tree Edition)
只识别 3 种标记（忽略前导空白/BOM）：
    #&&&&%% → Level 1
    #&&&% → Level 2
    #&&% → Level 3
其它任何行不影响层级栈，不会把后续 L2/L3 “掉到根”。
其它功能全保留：
- 左/右分栏、行号栏、语法高亮
- 自动刷新导航（500ms 防抖）
- Ctrl+F5 运行到唯一 IDLE
- Ctrl+F、F3/F2 查找
- Alt+G 跳转
- Tab/Shift+Tab & Ctrl+[ / ] 缩进
显示图表示例
放在注释3引号内部，鼠标点击蓝色下划线路径文字即显示图表
系统架构图：
![Architecture](D:/Myprogramsystem/CentralControlProgram/流程图/文件调度系统整体流程图.png)
链接跳转示例
跳转到另一函数，5秒后返回 可修改self._link_delay = 5000
放在注释3引号内部，鼠标点击蓝色下划线函数名即跳转到该函数，5秒返回
- 后台进程: [文本说明](run_daemon)
"""
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
import tkinter.font as tkfont
import subprocess, sys, os, ctypes, re, hashlib
from PIL import Image, ImageTk
import logging
from datetime import datetime, date
import glob

# 日志按日期分割
today = date.today().strftime("%Y-%m-%d")
log_filename = f"script_navigator_{today}.log"

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

# ================== 配置 ==================
DEFAULT_OPEN_FILE = r"D:/Myprogramsystem/cad/CAD基本操作.py"

# ================== 解析器 ==================
def parse_mark_line(raw: str):
    """
    返回 (level, label) 或 None
    level: 1/2/3
    规则严格且明确：
        '#&&&&%%' 开头 -> 1
        '#&&&%' 开头 -> 2
        '#&&%' 开头 -> 3
    """
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

def _tree_walk(tree, parent=""):
    for child in tree.get_children(parent):
        yield child
        yield from _tree_walk(tree, child)

# 语法高亮（若 idlelib 可用）
try:
    from idlelib.percolator import Percolator
    from idlelib.colorizer import ColorDelegator
except ImportError:
    Percolator = ColorDelegator = None

class ScriptNavigator(tk.Tk):
    def __init__(self, script_path=None):
        super().__init__()
        logging.debug("初始化 ScriptNavigator 开始")
        clean_old_logs()  # 清理旧日志
        self.title("Script Navigator (Tree Edition)")
        self.geometry("1200x780")
        # 状态
        self.font_size = 11
        self.script_path = script_path
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
        self._is_maximized = False  # 跟踪窗口是否最大化
        # 字体
        self._font_level1 = None
        self._font_level2 = None
        self._font_level3 = None
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_ui()
        self._bind_shortcuts()
        # 初始加载
        if self.script_path and os.path.isfile(self.script_path):
            logging.debug(f"加载初始脚本: {self.script_path}")
            self.load_script(self.script_path)
        else:
            if not self.script_path:
                self.script_path = DEFAULT_OPEN_FILE
            if os.path.exists(self.script_path):
                logging.debug(f"加载默认脚本: {self.script_path}")
                self.load_script(self.script_path)
            else:
                logging.debug("打开脚本选择对话框")
                self._open_script()
        logging.debug("初始化 ScriptNavigator 完成")

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
            logging.debug("配置 Treeview 标签失败")
        # 编辑区
        self.edit_frm = tk.Frame(self.pw)
        self.pw.add(self.edit_frm)
        # 行号栏
        self.gutter = tk.Text(
            self.edit_frm, width=6, padx=4, takefocus=0,
            state="disabled", background="#f0f0f0", foreground="#888",
            wrap="none", relief=tk.FLAT
        )
        self.gutter.pack(side=tk.LEFT, fill=tk.Y)
        # 代码框
        self.code = tk.Text(self.edit_frm, wrap="none", undo=True, tabs=("4c",))
        self.code.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.hbar = tk.Scrollbar(self.edit_frm, orient=tk.HORIZONTAL, command=self.code.xview)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.code.configure(xscrollcommand=self.hbar.set)
        self.vbar = tk.Scrollbar(self.edit_frm, orient=tk.VERTICAL, command=self._on_scrollbar)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.code.configure(yscrollcommand=self._on_code_yscroll)
        if Percolator and ColorDelegator:
            logging.debug("应用语法高亮")
            Percolator(self.code).insertfilter(ColorDelegator())
        # 按钮
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
        # 事件
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
        logging.debug("绑定快捷键开始")
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
        self.code.bind("<Tab>", self._indent)
        self.code.bind("<Shift-Tab>", self._unindent)
        logging.debug("绑定快捷键完成")

    # ---------- 字体/缩放 ----------
    def _apply_fonts(self):
        logging.debug("应用字体开始")
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
            logging.debug("配置 Treeview 字体标签失败")
        self.code.tag_config("find_highlight", background="#a6e3ff")
        self.code.tag_config("nav_pick", background="#ffff66")
        self.after(10, self._auto_resize_nav)
        self.after(20, self.update_line_numbers)
        logging.debug("应用字体完成")

    def _zoom_in(self):
        logging.debug("放大字体开始")
        self.font_size = min(self.font_size + 1, 42)
        self._apply_fonts()
        self._refresh_nav()
        logging.debug("放大字体完成")

    def _zoom_out(self):
        logging.debug("缩小字体开始")
        self.font_size = max(self.font_size - 1, 6)
        self._apply_fonts()
        self._refresh_nav()
        logging.debug("缩小字体完成")

    def _on_mousewheel_zoom(self, e):
        logging.debug(f"鼠标滚轮缩放事件: delta={e.delta}")
        if e.delta > 0:
            self._zoom_in()
        else:
            self._zoom_out()
        logging.debug("鼠标滚轮缩放事件处理完成")
        return "break"

    # ---------- 滚动同步 ----------
    def _on_mousewheel_sync(self, _):
        logging.debug("鼠标滚轮同步事件")
        self.after_idle(self.update_line_numbers)

    def _on_scrollbar(self, *args):
        logging.debug(f"滚动条事件: args={args}")
        self.code.yview(*args)
        self.gutter.yview(*args)
        self.update_line_numbers()

    def _on_code_yscroll(self, *args):
        logging.debug(f"代码滚动事件: args={args}")
        self.vbar.set(*args)
        self.gutter.yview_moveto(args[0])
        self.after_idle(self.update_line_numbers)

    # ---------- 行号 ----------
    def _schedule_line_numbers(self):
        logging.debug("调度更新行号")
        self.after_idle(self.update_line_numbers)

    def update_line_numbers(self):
        logging.debug("更新行号开始")
        try:
            first_visible = int(self.code.index("@0,0").split('.')[0])
            last_visible = int(self.code.index(f"@0,{self.code.winfo_height()}").split('.')[0])
            logging.debug(f"可见行范围: {first_visible} - {last_visible}")
        except Exception as e:
            logging.debug(f"获取可见行失败: {str(e)}")
            return
        total_lines = int(self.code.index("end-1c").split('.')[0])
        last_visible = min(last_visible + 1, total_lines)
        digits = max(3, len(str(total_lines)))
        if digits != self._gutter_digits:
            logging.debug(f"更新行号宽度: {digits}")
            self._gutter_digits = digits
            self.gutter.config(width=digits + 2)
        lines = [f"{ln:>{digits}} " for ln in range(first_visible, last_visible + 1)]
        new_text = "\n".join(lines)
        self.gutter.config(state="normal")
        self.gutter.delete("1.0", tk.END)
        self.gutter.insert("1.0", new_text)
        self.gutter.config(state="disabled")
        logging.debug("更新行号完成")

    # ---------- 内容修改 / 导航刷新 ----------
    def _on_key_release_update(self, _):
        logging.debug("键释放事件更新")
        self._schedule_line_numbers()

    def _on_text_modified(self, _):
        logging.debug("文本修改事件开始")
        if self.code.edit_modified():
            self.code.edit_modified(False)
            self._schedule_line_numbers()
            if not self._suppress_clear:
                logging.debug("清除导航和高亮")
                self._clear_nav_and_code_highlight()
                self.nav_tree.selection_remove(self.nav_tree.selection())
            self._schedule_nav_refresh()
            self._scan_for_markers()
        logging.debug("文本修改事件完成")

    def _schedule_nav_refresh(self, delay=500):
        logging.debug(f"调度导航刷新，延迟: {delay}ms")
        if self._nav_refresh_job:
            self.after_cancel(self._nav_refresh_job)
        self._nav_refresh_job = self.after(delay, self._maybe_refresh_nav)

    def _content_signature(self):
        logging.debug("计算内容签名开始")
        txt = self.code.get("1.0", "end-1c")
        md5 = hashlib.md5(txt.encode("utf-8")).hexdigest()
        sig = f"{len(txt)}:{md5}"
        logging.debug(f"内容签名: {sig}")
        return sig

    def _maybe_refresh_nav(self):
        logging.debug("可能刷新导航开始")
        sig = self._content_signature()
        if sig != self._last_nav_content_sig:
            logging.debug(f"签名变化，刷新导航: old={self._last_nav_content_sig}, new={sig}")
            self._last_nav_content_sig = sig
            self._refresh_nav()
        else:
            logging.debug("签名未变，无需刷新")

    # ---------- 文件 ----------
    def _open_script(self):
        logging.debug("打开脚本对话框开始")
        p = filedialog.askopenfilename(
            title="选择脚本",
            filetypes=[("Python", "*.py"), ("全部", "*.*")]
        )
        if p:
            logging.debug(f"选择文件: {p}")
            self.script_path = p
            self.load_script(p)
        else:
            logging.debug("未选择文件")

    def _open_new_file(self):
        logging.debug("打开新文件开始")
        if self.script_path:
            try:
                self.save_script()
            except Exception as e:
                logging.debug(f"保存失败: {str(e)}")
        self._open_script()

    def load_script(self, path):
        logging.debug(f"加载脚本开始: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                txt = f.read()
            self.code.delete("1.0", tk.END)
            self.code.insert("1.0", txt)
            self.code.edit_reset()
            self.title(f"Script Navigator – {os.path.basename(path)}")
            self._last_nav_content_sig = self._content_signature()
            self._refresh_nav()
            self.update_line_numbers()
            self._scan_for_markers()
            logging.debug("加载脚本完成")
        except Exception as e:
            logging.debug(f"加载失败: {str(e)}")
            messagebox.showerror("打开失败", str(e))

    def save_script(self):
        logging.debug("保存脚本开始")
        if not self.script_path:
            logging.debug("无路径，打开选择对话框")
            self._open_script()
            return
        try:
            with open(self.script_path, "w", encoding="utf-8") as f:
                f.write(self.code.get("1.0", tk.END))
            self._last_nav_content_sig = self._content_signature()
            self._refresh_nav()
            self._scan_for_markers()
            messagebox.showinfo("保存", "保存成功")
            logging.debug("保存成功")
        except Exception as e:
            logging.debug(f"保存失败: {str(e)}")
            messagebox.showerror("保存失败", str(e))

    # ---------- 导航 ----------
    def _format_nav_label(self, lineno: int, label: str) -> str:
        return f"{lineno:>{self._nav_line_digits}} {label}"

    def _refresh_nav(self):
        logging.debug("刷新导航开始")
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
        logging.debug(f"保存展开行: {open_lines}, 选中行: {selected_line}")
        for item in self.nav_tree.get_children():
            self.nav_tree.delete(item)
        self._node_line_map.clear()
        lines = self.code.get("1.0", tk.END).splitlines()
        total = len(lines)
        self._nav_line_digits = max(3, len(str(total)))
        logging.debug(f"总行数: {total}, 行号位数: {self._nav_line_digits}")
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
        except Exception as e:
            logging.debug(f"配置标签失败: {str(e)}")
        self._auto_resize_nav()
        if self._nav_hl_iid and self._nav_hl_iid not in self._node_line_map:
            self._nav_hl_iid = None
        logging.debug("刷新导航完成")

    def _collapse_all(self):
        logging.debug("折叠全部开始")
        for n in self.nav_tree.get_children():
            self.nav_tree.item(n, open=False)
            for c in self.nav_tree.get_children(n):
                self.nav_tree.item(c, open=False)
        logging.debug("折叠全部完成")

    def _expand_all(self):
        logging.debug("展开全部开始")
        def open_rec(iid):
            self.nav_tree.item(iid, open=True)
            for c in self.nav_tree.get_children(iid):
                open_rec(c)
        for n in self.nav_tree.get_children():
            open_rec(n)
        logging.debug("展开全部完成")

    def _on_tree_select(self, _):
        logging.debug("树选择事件开始")
        sel = self.nav_tree.selection()
        if not sel:
            logging.debug("无选择")
            return
        iid = sel[0]
        ln = self._node_line_map.get(iid)
        if ln:
            logging.debug(f"选择 iid={iid}, 行={ln}")
            self._nav_select_and_highlight(iid, ln)
        logging.debug("树选择事件完成")

    def _nav_select_and_highlight(self, iid, line_no: int):
        logging.debug(f"导航选择和高亮: iid={iid}, 行={line_no}")
        self._clear_nav_highlight_only()
        self._add_nav_tag(iid, "NAV_HL")
        self._nav_hl_iid = iid
        self._highlight_line(line_no)

    def _highlight_line(self, ln: int, source="unknown"):
        logging.debug(f"高亮行开始: {ln}, 来源={source}")
        try:
            self.code.tag_remove("nav_pick", "1.0", tk.END)
            self.code.see(f"{ln}.0")
            self.code.tag_add("nav_pick", f"{ln}.0", f"{ln}.0 lineend")
            self.update_line_numbers()
            self.update_idletasks()
            self.after(2000, lambda: self.code.tag_remove("nav_pick", "1.0", tk.END))
            logging.debug(f"跳转到行 {ln} (来源: {source})")
        except Exception as e:
            logging.debug(f"跳转失败: {str(e)} (来源: {source})")

    # ---------- 自适应列宽 ----------
    def _auto_resize_nav(self):
        logging.debug("自适应导航宽度开始")
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
        except Exception as e:
            logging.debug(f"设置列宽失败: {str(e)}")
        self.nav_frm.update_idletasks()
        logging.debug("自适应导航宽度完成")

    # ---------- 缩进 ----------
    def _indent(self, event):
        logging.debug("增加缩进开始")
        try:
            start = self.code.index("sel.first")
            end = self.code.index("sel.last")
            l1 = int(start.split('.')[0])
            l2 = int(end.split('.')[0])
            for ln in range(l1, l2 + 1):
                self.code.insert(f"{ln}.0", " " * 4)
        except tk.TclError:
            self.code.insert("insert", " " * 4)
        logging.debug("增加缩进完成")
        return "break"

    def _unindent(self, event):
        logging.debug("减少缩进开始")
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
        logging.debug("减少缩进完成")
        return "break"

    # ---------- 查找 ----------
    def _find_dialog(self, _=None):
        logging.debug("查找对话框开始")
        key = simpledialog.askstring("查找", "输入要查找的字符串：", parent=self)
        if not key:
            logging.debug("取消查找")
            return "break"
        self._do_find(key)
        logging.debug("查找对话框完成")
        return "break"

    def _do_find(self, key):
        logging.debug(f"执行查找: {key}")
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
            logging.debug("未找到匹配")
            return
        self.find_index = 0
        self._go_to_match()
        logging.debug(f"找到匹配: {len(self.find_matches)}")

    def _go_to_match(self):
        logging.debug(f"跳转到匹配: index={self.find_index}")
        pos = self.find_matches[self.find_index]
        ln = int(pos.split('.')[0])
        self._highlight_line(ln)

    def _find_next(self, _=None):
        logging.debug("查找下一个")
        if not self.find_matches:
            return "break"
        self.find_index = (self.find_index + 1) % len(self.find_matches)
        self._go_to_match()
        return "break"

    def _find_prev(self, _=None):
        logging.debug("查找上一个")
        if not self.find_matches:
            return "break"
        self.find_index = (self.find_index - 1) % len(self.find_matches)
        self._go_to_match()
        return "break"

    # ---------- 复制 ----------
    def _copy_all(self):
        logging.debug("复制全部开始")
        self.clipboard_clear()
        self.clipboard_append(self.code.get("1.0", tk.END))
        messagebox.showinfo("复制", "已复制全部代码")
        logging.debug("复制全部完成")

    def _copy_sel(self):
        logging.debug("复制选中开始")
        try:
            txt = self.code.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            txt = ""
        if not txt:
            messagebox.showwarning("未选中", "请先选中文本")
            logging.debug("无选中文本")
        else:
            self.clipboard_clear()
            self.clipboard_append(txt)
            messagebox.showinfo("复制", "已复制选中文本")
            logging.debug("复制选中完成")

    # ---------- 跳转行 ----------
    def goto_line_prompt(self):
        logging.debug("跳转行提示开始")
        total = int(float(self.code.index("end-1c").split('.')[0]))
        line = simpledialog.askinteger(
            "转到行", f"输入行号 (1 - {total}):",
            parent=self, minvalue=1, maxvalue=total
        )
        if line:
            self._highlight_line(line)
            logging.debug(f"跳转到行: {line}")
        else:
            logging.debug("取消跳转")

    # ---------- 运行 ----------
    def run_in_idle(self):
        logging.debug("运行在 IDLE 开始")
        if not self.script_path:
            messagebox.showwarning("未保存", "请先保存脚本")
            logging.debug("未保存脚本")
            return
        self.save_script()
        try:
            if self._idle_proc and self._idle_proc.poll() is None:
                logging.debug("终止现有进程")
                self._idle_proc.terminate()
                self._idle_proc.wait(timeout=2)
            logging.debug(f"启动 IDLE: {self.script_path}")
            self._idle_proc = subprocess.Popen(
                [sys.executable, "-m", "idlelib", "-r", self.script_path],
                close_fds=True
            )
        except Exception as e:
            logging.debug(f"运行失败: {str(e)}")
            messagebox.showerror("运行失败", str(e))

    # ---------- 关闭 ----------
    def _on_close(self):
        logging.debug("关闭窗口开始")
        try:
            if self._idle_proc and self._idle_proc.poll() is None:
                logging.debug("终止 IDLE 进程")
                self._idle_proc.terminate()
        except Exception as e:
            logging.debug(f"终止进程失败: {str(e)}")
        self.destroy()
        sys.exit(0)

    # ================== 新增辅助函数 ==================
    def _add_nav_tag(self, iid, tag):
        logging.debug(f"添加导航标签: iid={iid}, tag={tag}")
        tags = list(self.nav_tree.item(iid, "tags"))
        if tag not in tags:
            tags.append(tag)
            self.nav_tree.item(iid, tags=tuple(tags))

    def _remove_nav_tag(self, iid, tag):
        logging.debug(f"移除导航标签: iid={iid}, tag={tag}")
        tags = [t for t in self.nav_tree.item(iid, "tags") if t != tag]
        self.nav_tree.item(iid, tags=tuple(tags))

    def _clear_nav_highlight_only(self):
        logging.debug("清除导航高亮开始")
        if self._nav_hl_iid and self.nav_tree.exists(self._nav_hl_iid):
            self._remove_nav_tag(self._nav_hl_iid, "NAV_HL")
        self._nav_hl_iid = None
        logging.debug("清除导航高亮完成")

    def _clear_nav_and_code_highlight(self):
        logging.debug("清除导航和代码高亮开始")
        self._clear_nav_highlight_only()
        self.code.tag_remove("nav_pick", "1.0", tk.END)
        logging.debug("清除导航和代码高亮完成")

    def _scan_for_markers(self):
        logging.debug("扫描标记开始")
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
                    logging.debug(f"扫描图片: {text_content} -> {target}, 标签: {unique_tag}")
                else:
                    unique_tag = f"link_{len(self._link_tags)}"
                    self.code.tag_add("link_marker", md_start, md_end)
                    self.code.tag_add(unique_tag, md_start, md_end)
                    logging.debug(f"扫描链接: {text_content} -> {target}, 标签: {unique_tag}")
                    try:
                        target_line = int(target)
                        self._link_tags[unique_tag] = target_line
                        logging.debug(f"链接 {unique_tag} 映射到行号: {target_line}")
                    except ValueError:
                        pattern = r'^\s*def\s+' + re.escape(target) + r'\b\s*\('
                        found = False
                        for i, line in enumerate(lines, 1):
                            if re.match(pattern, line):
                                self._link_tags[unique_tag] = i
                                logging.debug(f"找到函数 {target} 在行 {i}, 标签: {unique_tag}")
                                found = True
                                break
                        if not found:
                            logging.debug(f"未找到函数定义: {target}")
        logging.debug(f"最终链接映射: {self._link_tags}")
        logging.debug("扫描标记完成")

    def _on_click_image_marker(self, event):
        logging.debug(f"点击图片标记: x={event.x}, y={event.y}")
        pos = self.code.index(f"@{event.x},{event.y}")
        tags = self.code.tag_names(pos)
        logging.debug(f"点击位置: {pos}, 标签: {tags}")
        for tag in tags:
            if tag.startswith("img_"):
                path = self._image_tags.get(tag)
                if path and os.path.isfile(path):
                    logging.debug(f"显示图片弹出: {path}")
                    self._show_image_popup(path, event)
                break

    def _show_image_popup(self, path, event):
        logging.debug(f"显示图片弹出开始: {path}, 鼠标位置: x={event.x}, y={event.y}")
        self._hide_image_popup()
        try:
            if not os.path.isfile(path):
                logging.debug(f"文件不存在: {path}")
                messagebox.showerror("图片加载失败", f"图片文件不存在: {path}")
                return
            self._original_img = Image.open(path)
            orig_width, orig_height = self._original_img.size
            logging.debug(f"原始图片尺寸: {orig_width}x{orig_height}")
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            max_win_w = int(screen_w * 0.8)
            max_win_h = int(screen_h * 0.8)
            logging.debug(f"屏幕尺寸: {screen_w}x{screen_h}, 最大窗口: {max_win_w}x{max_win_h}")
            if self._image_scale == 1.0:
                fit_scale = min(float(max_win_w) / orig_width, float(max_win_h) / orig_height, 1.0)
                self._image_scale = fit_scale
                logging.debug(f"初始缩放比例: {self._image_scale}")
            new_width = int(orig_width * self._image_scale)
            new_height = int(orig_height * self._image_scale)
            logging.debug(f"调整后图片尺寸: {new_width}x{new_height}")
            if new_width < 1 or new_height < 1:
                logging.debug("图片尺寸过小，取消显示")
                return
            resized_img = self._original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self._popup_image = ImageTk.PhotoImage(resized_img)
            self._popup_window = tk.Toplevel(self)
            self._popup_window.title("Image Viewer")
            self._popup_window.attributes("-topmost", True)
            # 创建按钮框架
            button_frame = tk.Frame(self._popup_window)
            button_frame.pack(side=tk.TOP, fill=tk.X)
            close_button = tk.Button(button_frame, text="X", command=self._hide_image_popup)
            close_button.pack(side=tk.RIGHT, padx=5, pady=5)
            maximize_button = tk.Button(button_frame, text="□", command=self._toggle_maximize)
            maximize_button.pack(side=tk.RIGHT, padx=5, pady=5)
            # 创建画布
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
            # 保存初始窗口大小和位置
            self._normal_geometry = f"{min(max_win_w, new_width + vbar.winfo_reqwidth())}x{min(max_win_h, new_height + hbar.winfo_reqheight())}"
            x = self.winfo_pointerx() + 20
            y = self.winfo_pointery() + 20
            self._popup_window.geometry(f"{self._normal_geometry}+{x}+{y}")
            logging.debug("图片弹出显示完成")
        except Exception as e:
            logging.debug(f"图片加载失败: {str(e)}")
            messagebox.showerror("图片加载失败", f"无法加载图片 {path}: {str(e)}")

    def _hide_image_popup(self):
        logging.debug("隐藏图片弹出开始")
        if self._popup_window:
            self._popup_window.destroy()
            self._popup_window = None
            self._popup_image = None
            self._original_img = None
            self.popup_canvas = None
            self.popup_image_item = None
            self._image_scale = 1.0
            self._is_maximized = False
            logging.debug("隐藏图片弹出完成")

    def _toggle_maximize(self, event=None):
        logging.debug(f"切换最大化状态: 当前状态={'最大化' if self._is_maximized else '正常'}")
        if self._popup_window is None:
            return
        if self._is_maximized:
            self._popup_window.geometry(self._normal_geometry)
            self._is_maximized = False
            logging.debug("还原窗口")
        else:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            self._popup_window.geometry(f"{screen_w}x{screen_h}+0+0")
            self._is_maximized = True
            logging.debug("最大化窗口")
        self.update_idletasks()

    def _on_popup_mousewheel(self, event):
        logging.debug(f"弹出窗口滚轮事件: delta={event.delta}, 鼠标位置: x={event.x}, y={event.y}")
        if self._original_img is None:
            logging.debug("无原始图片，忽略滚轮事件")
            return
        if event.delta > 0:
            zoom_factor = 1.1
            logging.debug("放大: factor=1.1")
        else:
            zoom_factor = 0.9
            logging.debug("缩小: factor=0.9")
        new_scale = self._image_scale * zoom_factor
        if new_scale < 0.1 or new_scale > 10.0:
            logging.debug(f"缩放比例超出范围: {new_scale}")
            return
        mouse_x = self.popup_canvas.canvasx(event.x)
        mouse_y = self.popup_canvas.canvasy(event.y)
        logging.debug(f"鼠标在画布坐标: x={mouse_x}, y={mouse_y}")
        self._image_scale = new_scale
        orig_width, orig_height = self._original_img.size
        new_width = int(orig_width * self._image_scale)
        new_height = int(orig_height * self._image_scale)
        logging.debug(f"缩放后尺寸: {new_width}x{new_height}, 缩放比例: {self._image_scale}")
        if new_width < 1 or new_height < 1:
            logging.debug("图片尺寸过小，取消缩放")
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
            logging.debug(f"调整滚动位置: x={scroll_x}, y={scroll_y}")
            self.popup_canvas.xview_moveto(scroll_x)
            self.popup_canvas.yview_moveto(scroll_y)
            logging.debug("滚轮缩放完成")
        except Exception as e:
            logging.debug(f"缩放失败: {str(e)}")
            messagebox.showerror("缩放失败", f"图片缩放失败: {str(e)}")

    def _on_click_image_marker(self, event):
        logging.debug(f"点击图片标记: x={event.x}, y={event.y}")
        pos = self.code.index(f"@{event.x},{event.y}")
        tags = self.code.tag_names(pos)
        logging.debug(f"点击位置: {pos}, 标签: {tags}")
        for tag in tags:
            if tag.startswith("img_"):
                path = self._image_tags.get(tag)
                if path and os.path.isfile(path):
                    self._show_image_popup(path, event)
                break

    def _on_click_link(self, event):
        logging.debug(f"点击链接事件: x={event.x}, y={event.y}")
        pos = self.code.index(f"@{event.x},{event.y}")
        tags = self.code.tag_names(pos)
        logging.debug(f"点击位置: {pos}, 标签: {tags}")
        unique_tag = None
        for tag in tags:
            if tag.startswith("link_") and tag != "link_marker" and tag[len("link_"):].isdigit():
                unique_tag = tag
                break
        if unique_tag:
            target_line = self._link_tags.get(unique_tag)
            logging.debug(f"点击链接唯一标签: {unique_tag}, 目标行: {target_line}")
            if target_line:
                try:
                    current_view = self.code.yview()
                    self._highlight_line(target_line, source="link")
                    self.after(self._link_delay, lambda: self.code.yview_moveto(current_view[0]))
                except Exception as e:
                    logging.debug(f"链接跳转失败: {str(e)}")
            else:
                logging.debug(f"无效的目标行号 for 唯一标签: {unique_tag}")
        else:
            logging.debug("未找到有效的唯一 link_ 标签")

# ================== 主入口 ==================
if __name__ == "__main__":
    start_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OPEN_FILE
    app = ScriptNavigator(start_file)
    app.mainloop()
