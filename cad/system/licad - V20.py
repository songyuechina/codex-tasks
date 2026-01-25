# -*- coding: utf-8 -*-
# 文件位置: D:/claude-tasks/cad/system/licad.py V2.0
import time
import os
import sys
import pythoncom
import win32com.client
from pathlib import Path

try:
    from CAD_coordination import send_cmd_with_sync
except ImportError:
    send_cmd_with_sync = None

# =======================================================
# 1. 导入依赖 (日志 + 重试工具)
# =======================================================
try:
    from common_logger import sys_logger
    from CAD_com_utils import retry_on_busy, SafeCOM
except ImportError as e:
    print(f"❌ 关键模块缺失: {e}")
    print("请确保 common_logger.py 和 CAD_com_utils.py 在同一目录下。")
    raise

# =======================================================
# 2. 核心功能函数 (连接逻辑)
# =======================================================

def _coinit_once():
    try: pythoncom.CoInitialize()
    except: pass

def get_acad_doc(max_wait=7.0):
    """获取/启动 AutoCAD 应用和文档"""
    _coinit_once()
    t0 = time.time()
    app = None
    
    while True:
        try:
            # 1. 获取 APP
            if app is None:
                try:
                    app = win32com.client.GetActiveObject("AutoCAD.Application")
                    app = win32com.client.gencache.EnsureDispatch(app)
                except:
                    app = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
            
            # 2. 获取 DOC
            try:
                doc = app.ActiveDocument
                _ = doc.Name 
                return app, doc
            except:
                # 智能等待逻辑：判断是没文档还是忙碌
                try: cnt = app.Documents.Count
                except: cnt = -1
                
                if cnt == 0:
                    try: 
                        sys_logger.info("检测到无文档，正在新建...")
                        doc = app.Documents.Add(); time.sleep(1)
                        return app, doc
                    except: pass
                
                if time.time() - t0 > max_wait:
                    raise RuntimeError("AutoCAD 忙碌或无响应(超时)")
                time.sleep(0.5)
                continue

        except Exception as e:
            if time.time() - t0 > max_wait:
                sys_logger.error(f"get_acad_doc 彻底失败: {e}")
                raise RuntimeError("无法连接 AutoCAD")
            time.sleep(0.5)


# =================================================================
# 【核心黑科技】文档影子替身 (Safe Document Wrapper)
# =================================================================
class SafeDocumentWrapper:
    """
    这是一个"影子对象"，它包装了真实的 CAD Document COM 对象。
    目的：拦截 SendCommand 调用，强制转换为安全的同步调用。
    """
    def __init__(self, real_com_doc):
        self._real_doc = real_com_doc

    def SendCommand(self, cmd: str):
        """
        【拦截】劫持 SendCommand，转为同步安全模式
        """
        # 1. 自动补全回车
        if not (cmd.endswith("\n") or cmd.endswith("\r")):
            cmd += "\n"
        
        # 2. 调用 CAD_coordination 的安全函数
        if send_cmd_with_sync:
            # 使用同步等待 (30秒超时)
            return send_cmd_with_sync(cmd, wait_after=0.3, timeout=30.0)
        else:
            # 降级：如果模块导入失败，调用原生方法
            return self._real_doc.SendCommand(cmd)

    def __getattr__(self, name):
        """
        【转发】除了 SendCommand 以外的所有属性/方法（如 Name, SaveAs, Layers），
        全部自动转发给真实的 COM 对象。
        """
        return getattr(self._real_doc, name)
        
    def __dir__(self):
        """让 IDE 能自动提示真实对象的属性"""
        return dir(self._real_doc) + ['SendCommand']

# =======================================================
# 3. 核心代理类 (使用了来自 CAD_com_utils 的装饰器)
# =======================================================

class AutoCadProxy:
    def __init__(self):
        self._acad = None
        self._doc = None

    def li(self):
        """连接刷新"""
        try:
            if self._acad is None or self._doc is None: raise Exception("Init")
            real_doc = self._acad.ActiveDocument
            if self._doc.Name != real_doc.Name: raise Exception("Switch")
            return True
        except:
            # 重连
            try:
                self._acad, self._doc = get_acad_doc()
                try: 
                    if not self._acad.Visible: self._acad.Visible = True
                except: pass
                sys_logger.info(f"[li] 连接已刷新: {self._doc.Name}")
                return True
            except Exception as e:
                sys_logger.error(f"[li] 连接失败: {e}")
                return False

    @property
    def doc(self):
        """
        【关键修改】
        现在返回的不是原始 COM 对象，而是我们的"影子替身"。
        用户感觉不到区别，但 SendCommand 已经被换掉了。
        """
        self.li()
        # 将原始 doc 包装进 SafeDocumentWrapper
        return SafeDocumentWrapper(self._doc)
    @property
    def acad(self): self.li(); return self._acad
    @property
    def mp(self): self.li(); return self._doc.ModelSpace
    @property
    def sp(self): self.li(); return self._doc.PaperSpace

    # --- 使用 retry_on_busy (来自 CAD_com_utils) ---

    @retry_on_busy  # 智能用法 1：默认参数
    def save_file(self):
        name = self.doc.Name
        self.doc.Save()
        sys_logger.info(f"已保存: {name}")
        return True

    @retry_on_busy(max_retries=5)  # 智能用法 2：自定义参数
    def save_file_as(self, output_path):
        p = Path(output_path).resolve()
        if not p.parent.exists(): 
            sys_logger.error(f"另存为失败，目录不存在: {p.parent}")
            return False
        
        sys_logger.info(f"正在另存为: {p.name}")
        self.doc.SaveAs(str(p))
        self.li() # 另存为后文档指针会变，必须刷新
        return True

    @retry_on_busy(max_retries=15, base_delay=1.0) # 打开可能很慢
    def open_file(self, file_path):
        target = str(Path(file_path).resolve()).lower()
        # 检查是否已打开
        try:
            for d in self.acad.Documents:
                if str(Path(d.FullName).resolve()).lower() == target:
                    d.Activate(); self.li()
                    sys_logger.info(f"文件已在运行中，直接激活: {d.Name}")
                    return True
        except: pass
        
        if not os.path.exists(file_path): 
            sys_logger.error(f"文件不存在: {file_path}")
            return False
            
        sys_logger.info(f"正在打开文件: {Path(file_path).name}")
        self.acad.Documents.Open(str(file_path))
        self.li()
        return True

    @retry_on_busy
    def close_file(self, save_option="auto_save"):
        doc = self.doc
        name = doc.Name
        if save_option == "auto_save": 
            self.save_file()
        doc.Close(False)
        sys_logger.info(f"已关闭: {name}")
        return True
    
    def close_dwg_by_name(self, name):
        try:
            app = win32com.client.GetActiveObject("AutoCAD.Application")
            app.Documents.Item(name).Close(False)
            sys_logger.info(f"后台关闭文件: {name}")
            return True
        except: return False

    # ==============================================================
    # 【必须补上】让 C.SendCommand 变为合法调用
    # ==============================================================
    def SendCommand(self, cmd_str: str):
        """
        代理发送命令：
        1. 自动补全回车
        2. 调用 CAD_coordination.send_cmd_with_sync 实现同步等待
        """
        # 1. 动态导入防止循环引用
        try:
            from CAD_coordination import send_cmd_with_sync
        except ImportError:
            # 兜底：如果导不进来，就用原生 doc 发送（不安全但能跑）
            if not (cmd_str.endswith("\n") or cmd_str.endswith("\r")):
                cmd_str += "\n"
            return self.doc.SendCommand(cmd_str)

        # 2. 补全回车符
        if not (cmd_str.endswith("\n") or cmd_str.endswith("\r")):
            cmd_str += "\n"

        # 3. 调用安全发送 (设置超时 30秒)
        return send_cmd_with_sync(cmd_str, wait_after=0.3, timeout=30.0)





    def force_update(self, new_acad, new_doc):
        """
        【灾难恢复专用】
        外部脚本(如 litz)重启CAD后，强制更新内部引用，
        避免二次连接开销。
        """
        self._acad = new_acad
        self._doc = new_doc
        # 清空子对象缓存，强制下次重新获取
        self._mp = None 
        self._sp = None
        print(f"[licad] 代理对象已强制更新为: {new_doc.Name}")




# =======================================================
# 4. 实例化与导出
# =======================================================

C = AutoCadProxy()

def li(): return C.li()
def save_file(): return C.save_file()
def save_file_as(path): return C.save_file_as(path)
def open_file(path): return C.open_file(path)
def close_file(opt="auto_save"): return C.close_file(opt)
def close_dwg_by_name(name): return C.close_dwg_by_name(name)

# 兼容导出 (可选)
acad = None
doc = None
