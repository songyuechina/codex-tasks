# -*- coding: utf-8 -*-
# 文件位置: D:/codex-tasks/cad/system/licad.py V2.6
import time
import os
import sys
import pythoncom
import win32com.client
from pathlib import Path
from win32com.client import VARIANT


current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))
from system.project_setup import PathConfig


# =================================================================
# 1. 核心依赖导入
# =================================================================
try:
    from system.common_logger import sys_logger
    # 🔥【关键修复】导入时直接改名，避免与下方函数名冲突
    from system.CAD_com_utils import retry_on_busy as _tool_retry_on_busy, SafeCOM 
except ImportError as e:
    print(f"❌ [licad] 关键模块缺失: {e}")
    raise

def _coinit_once():
    try: pythoncom.CoInitialize()
    except: pass

# =================================================================
# 2. 核心连接函数
# =================================================================

#清除缓存崩溃
def get_acad_doc(max_wait=15.0): # 增加默认等待时间，天正启动很慢
    """
    [底层原语] 获取/启动 AutoCAD 应用和文档
    【V3.0 自愈版】
    1. 修复双进程问题：检测到进程但未就绪时强制等待。
    2. 新增自愈机制：当连接严重超时，自动清理损坏的 gen_py 缓存。
    """
    import win32com.client
    import time
    from win32com.client import gencache

    # 简单的内部函数：检查是否有名为 acad.exe 的进程
    def _is_acad_process_running():
        try:
            import win32com.client
            wmi = win32com.client.GetObject('winmgmts:')
            # 查找 acad.exe (不区分大小写)
            procs = wmi.ExecQuery("SELECT ProcessId FROM Win32_Process WHERE Name = 'acad.exe'")
            return len(procs) > 0
        except:
            return False

    # 内部自愈函数：清理缓存
    def _auto_fix_com_cache():
        try:
            print("\n[licad] ⚠️ 检测到 COM 接口异常，正在执行自动修复 (清理缓存)...")
            import os, shutil, sys
            paths_to_clean = []
            try:
                import win32com.client
                paths_to_clean.append(win32com.client.gencache.GetGeneratePath())
            except: pass
            
            try:
                import win32com
                paths_to_clean.append(os.path.join(os.path.dirname(win32com.__file__), "gen_py"))
            except: pass
            
            cleaned = False
            for p in paths_to_clean:
                if p and os.path.exists(p):
                    try:
                        shutil.rmtree(p)
                        print(f"[licad] ✅ 已清理缓存: {p}")
                        cleaned = True
                    except: pass
            
            if cleaned:
                print("[licad] 缓存清理完成，请稍后再次运行脚本以生效。")
            else:
                print("[licad] 未发现缓存文件或清理失败。")
        except Exception as e:
            print(f"[licad] ❌ 自动修复失败: {e}")

    _coinit_once()
    t0 = time.time()
    app = None
    
    print("[licad] 正在尝试连接 CAD COM 接口...")

    while True:
        # 1. 尝试连接现有实例
        try:
            if app is None:
                # 尝试获取活跃对象
                app = win32com.client.GetActiveObject("AutoCAD.Application")
                # 封装为 COM 对象
                app = gencache.EnsureDispatch(app)
        except Exception:
            # =======================================================
            # 🛑 关键修改点：捕获失败后，不要立即新建！
            # =======================================================
            
            # A. 检查：系统里到底有没有 acad 进程？
            if _is_acad_process_running():
                # B. 如果有进程，说明它可能正在启动中 (Splash Screen)
                #    我们要做的就是：等！死等！
                if time.time() - t0 > max_wait:
                    # ==========================================
                    # 🔥 自愈触发点：超时了，可能是缓存坏了
                    # ==========================================
                    _auto_fix_com_cache()
                    
                    # 抛出异常，结束脚本
                    raise RuntimeError(f"连接严重超时 ({max_wait}s)，已尝试清理 COM 缓存。请重启 Python 和 CAD 后重试。")
                
                print(f"\r[licad] CAD 进程存在但未就绪，正在重试... ({time.time()-t0:.1f}s)", end="")
                time.sleep(1.0)
                continue # 跳过本次循环，重新尝试 GetActiveObject
            
            else:
                # C. 如果确实没有进程，这才允许新建
                print("\n[licad] 未检测到 CAD 进程，正在通过 COM 启动新实例...")
                try:
                    app = gencache.EnsureDispatch("AutoCAD.Application")
                except Exception as e:
                    # 如果新建也失败，也尝试修一下缓存
                    _auto_fix_com_cache()
                    raise RuntimeError(f"启动新 CAD 实例失败: {e}")

        # 2. 获取 Document (这一部分保持原样，但也加了防错)
        try:
            if app:
                # 只要 app 拿到了，通常 ActiveDocument 就有了
                # 但刚启动瞬间可能还没 Document
                doc = app.ActiveDocument
                _ = doc.Name 
                print(f"\n[licad] 连接成功: {doc.Name}")
                return app, doc
        except Exception:
            # 如果连上了 App 但拿不到 Doc (例如刚启动是 0 文档状态)
            try:
                if app.Documents.Count == 0:
                    print("[licad] App已连接但无文档，正在新建...")
                    doc = app.Documents.Add()
                    time.sleep(1) # 给它一点时间初始化
                    return app, doc
            except:
                pass
            
            # 如果超时
            if time.time() - t0 > max_wait:
                raise RuntimeError("已连接 App，但无法获取 ActiveDocument (超时)")
            
            time.sleep(0.5)
            continue


# =================================================================
# 【Wrapper】文档影子替身
# =================================================================
class SafeDocumentWrapper:
    """劫持 SendCommand，转为同步安全调用"""
    def __init__(self, real_com_doc):
        self._real_doc = real_com_doc

    def SendCommand(self, cmd: str):
        if not (cmd.endswith("\n") or cmd.endswith("\r")):
            cmd += "\n"
        
        # 延迟导入防止循环引用
        try:
            from CAD_coordination import send_cmd_with_sync
            return send_cmd_with_sync(cmd, wait_after=0.3, timeout=30.0)
        except ImportError:
            return self._real_doc.SendCommand(cmd)

    def __getattr__(self, name):
        return getattr(self._real_doc, name)
        
    def __dir__(self):
        return dir(self._real_doc) + ['SendCommand']

# =================================================================
# 3. 核心代理类
# =================================================================

class AutoCadProxy:
    def __init__(self):
        self._acad = None
        self._doc = None
        self._mp = None
        self._sp = None

    def li(self):
        """[智能连接] 三层验证"""
        try:
            if self._acad is None or self._doc is None: raise RuntimeError
            real = self._acad.ActiveDocument
            if self._doc.Name != real.Name: raise RuntimeError
            return True
        except:
            pass

        try:
            self._acad, self._doc = get_acad_doc()
        except Exception as e:
            sys_logger.error(f"[li] 连接失败: {e}")
            return False

        try:
            tmp = self._doc.ModelSpace
            pt = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (0,0,0))
            l = tmp.AddLine(pt, pt); l.Delete()
        except:
            return False

        self._mp = self._doc.ModelSpace
        self._sp = self._doc.PaperSpace
        try: 
            if not self._acad.Visible: self._acad.Visible = True
        except: pass
        
        sys_logger.info(f"[li] 连接已刷新: {self._doc.Name}")
        return True

    # --- 属性 ---
    @property
    def acad(self): self.li(); return self._acad
    
    @property
    def doc(self): 
        """【Wrapper】返回安全替身"""
        self.li()
        return SafeDocumentWrapper(self._doc)
    
    @property
    def raw_doc(self):
        """【Raw】返回原始对象"""
        self.li()
        return self._doc
    
    @property
    def mp(self): self.li(); return self._mp
    
    @property
    def sp(self): self.li(); return self._sp
    
    @property
    def msp(self): return self.mp

    # --- 文件操作 (直接使用导入的工具) ---

    @_tool_retry_on_busy
    def save_file(self):
        try:
            self.raw_doc.Save() 
            sys_logger.info(f"[licad] 已保存")
            return True
        except Exception as e:
            sys_logger.error(f"[licad] 保存失败: {e}")
            return False

    @_tool_retry_on_busy(max_retries=5)
    def save_file_as(self, path):
        try:
            p = Path(path).resolve()
            if not p.parent.exists(): return False
            sys_logger.info(f"[licad] 另存为: {p.name}")
            self.raw_doc.SaveAs(str(p))
            self.li()
            return True
        except Exception as e:
            sys_logger.error(f"[licad] 另存为失败: {e}")
            return False

    @_tool_retry_on_busy(max_retries=10, base_delay=1.0)
    def open_file(self, path):
        target = str(Path(path).resolve()).lower()
        try:
            for d in self.acad.Documents:
                if str(Path(d.FullName).resolve()).lower() == target:
                    d.Activate(); self.li(); return True
        except: pass
        
        if not os.path.exists(path): return False
        try:
            sys_logger.info(f"[licad] 打开: {Path(path).name}")
            self.acad.Documents.Open(str(path))
            self.li()
            return True
        except: return False

    @_tool_retry_on_busy
    def close_file(self, opt="auto_save"):
        try:
            d = self.raw_doc
            n = d.Name
            if opt == "auto_save": d.Save()
            d.Close(False)
            sys_logger.info(f"[licad] 已关闭: {n}")
            try: self.li()
            except: pass
            return True
        except: return False

    def close_dwg_by_name(self, name):
        try:
            win32com.client.GetActiveObject("AutoCAD.Application").Documents.Item(name).Close(False)
            return True
        except: return False

# =================================================================
# 4. 实例化与导出
# =================================================================

C = AutoCadProxy()

def li(): return C.li()
def save_file(): return C.save_file()
def save_file_as(p): return C.save_file_as(p)
def open_file(p): return C.open_file(p)
def close_file(o="auto_save"): return C.close_file(o)
def close_dwg_by_name(n): return C.close_dwg_by_name(n)

#&&% 解析文档
def resolve_doc(docname=None):
    """
    解析文档名称/路径并激活，返回安全文档对象（SafeDocumentWrapper）。
    docname=None 时返回当前激活文档。
    """
    try:
        C.li()
    except Exception as e:
        sys_logger.error(f"[licad.resolve_doc] 连接失败: {e}")
        return None

    if docname is None:
        return C.doc

    try:
        target = str(docname).strip()
        if not target:
            return C.doc
        target_lower = target.lower()
    except Exception as e:
        sys_logger.error(f"[licad.resolve_doc] docname 非法: {e}")
        return None

    try:
        for d in C.acad.Documents:
            try:
                name = str(d.Name or "").lower()
                full = str(d.FullName or "").lower()
                stem = Path(full).stem.lower() if full else ""
                if target_lower in (name, full, stem):
                    try:
                        d.Activate()
                    except Exception:
                        pass
                    try:
                        C.li()
                    except Exception:
                        pass
                    return C.doc
            except Exception:
                continue
    except Exception as e:
        sys_logger.error(f"[licad.resolve_doc] 遍历文档失败: {e}")
        return None

    sys_logger.warning(f"[licad.resolve_doc] 未找到文档: {docname}")
    return None

# 🔥【关键修复】直接使用别名调用，解决递归死锁
def retry_on_busy(func_or_args=None, **kwargs):
    """转发给 CAD_com_utils 的装饰器"""
    return _tool_retry_on_busy(func_or_args, **kwargs)

# 兼容变量
acad = None 
doc = None

