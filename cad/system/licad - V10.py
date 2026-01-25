# D:/claude-tasks/cad/system/licad.py
import functools
import time
import os
import pythoncom
import win32com.client
from pathlib import Path
from win32com.client import VARIANT

#licad.py V1.0版
# =================================================================
# 1. 基础配置与常量
# =================================================================

# RPC 错误码：忙碌 或 服务不可用
_RPC_BUSY = (-2147417846, -2147418111)
_RPC_DOWN = (-2147023174, -2147467260, -2147417848)

def _coinit_once():
    """线程初始化防呆设计"""
    try: 
        pythoncom.CoInitialize()
    except: 
        pass

# =================================================================
# 2. 核心连接函数 (公开工具)
# =================================================================

def _retry_on_busy(max_retries=10, base_delay=0.5):
    """
    [装饰器工厂] 自动处理 CAD 忙碌 (RPC_E_CALL_REJECTED)。
    
    参数:
        max_retries (int): 最大重试次数。如果你发现日志里全是 "重试失败"，请增大此值。
        base_delay (float): 初始等待秒数(指数退避)。
        
    异常处理:
        - 忙碌: 记录 WARNING 日志并重试。
        - 掉线: 记录 ERROR 日志并抛出。
        - 次数耗尽: 记录 CRITICAL 日志（提示参数可能不恰当）并抛出。
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            
            # 1. 参数防呆检查 (如果参数写得太离谱，直接报错记录)
            if max_retries <= 0:
                msg = f"参数配置错误 [_retry_on_busy]: max_retries必须大于0, 当前={max_retries}"
                sys_logger.error(msg)
                raise ValueError(msg)

            for i in range(max_retries):
                try:
                    # 尝试执行原函数
                    return func(*args, **kwargs)
                
                except Exception as e:
                    err_msg = str(e)
                    # 安全获取 hresult，普通异常没有此属性
                    hr = getattr(e, 'hresult', None)

                    # -----------------------------------------------------------
                    # 判据 A: 忙碌 (Busy) - 属于"正常"的异常，需要重试
                    # -----------------------------------------------------------
                    is_busy_code = (hr in _RPC_BUSY_CODES)
                    is_busy_text = any(s in err_msg for s in _BUSY_STRINGS)

                    if is_busy_code or is_busy_text:
                        last_err = e
                        # 指数退避算法: 0.5, 0.75, 1.125, 1.68...
                        wait_time = base_delay * (1.5 ** i)
                        
                        # [日志-WARNING] 记录过程，但不惊慌
                        # 方便你分析：是不是 wait_time 太短了？是不是 i 很快就用完了？
                        err_code_display = f"0x{hr & 0xFFFFFFFF:08X}" if hr else "NoCode"
                        sys_logger.warning(
                            f"CAD忙碌 [{func.__name__}] - {err_code_display} - "
                            f"{wait_time:.2f}s后重试 ({i+1}/{max_retries})"
                        )
                        
                        # 关键：消息泵，防止死锁
                        try:
                            pythoncom.PumpWaitingMessages()
                        except:
                            pass
                        
                        time.sleep(wait_time)
                        continue

                    # -----------------------------------------------------------
                    # 判据 B: 掉线 (Down) - 属于"致命"异常，无法重试
                    # -----------------------------------------------------------
                    if hr in _RPC_DOWN_CODES:
                        sys_logger.error(f"CAD连接断开/崩溃 [{func.__name__}] - Code: 0x{hr & 0xFFFFFFFF:08X}")
                        raise e

                    # -----------------------------------------------------------
                    # 判据 C: 代码逻辑错误或其他未知错误 - 记录并抛出
                    # -----------------------------------------------------------
                    # 比如: AttributeError, TypeError 等
                    sys_logger.error(f"脚本运行时错误 [{func.__name__}]: {err_msg}")
                    raise e
            
            # ===========================================================
            # 循环结束仍未成功 -> 说明参数(max_retries)可能太小，或者CAD彻底卡死
            # ===========================================================
            sys_logger.critical(
                f"❌ 重试彻底失败 [{func.__name__}] - "
                f"已耗尽 {max_retries} 次重试机会。请检查 CAD 是否卡死或增加 max_retries 参数。"
            )
            
            if last_err:
                raise last_err
                
        return wrapper
    return decorator







def get_acad_doc(max_wait=7.0):
    """
    [底层原语] 获取/启动 AutoCAD 应用和文档 (安全修正版)
    修正：仅当确实无文档时才新建；若有文档但无法激活(忙碌/弹窗)，则进入等待而非新建。
    """
    _coinit_once()
    t0 = time.time()
    app = None
    
    while True:
        try:
            # --- 阶段 A: 获取/启动 App ---
            if app is None:
                try:
                    app = win32com.client.GetActiveObject("AutoCAD.Application")
                    app = win32com.client.gencache.EnsureDispatch(app)
                except Exception:
                    app = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
            
            # --- 阶段 B: 获取文档 (带智能判断) ---
            try:
                # 1. 尝试直接获取
                doc = app.ActiveDocument
                _ = doc.Name 
                return app, doc
                
            except Exception as e_doc:
                # 🔥【关键逻辑修正】获取不到 ActiveDocument，必须区分是“没文档”还是“CAD忙/锁死”
                
                # 1. 先尝试探测当前文档数量
                doc_count = -1 # 初始化为 -1 表示探测失败
                try:
                    doc_count = app.Documents.Count
                except Exception:
                    # 如果连 Count 都读不到，说明 CAD 彻底僵死或有模态对话框阻挡 COM 通讯
                    # 此时千万不能新建，视为忙碌
                    print("[licad] 无法读取文档数量 (CAD可能正忙或有弹窗)，暂停操作...")
                    pass 

                # 2. 只有明确知道数量为 0 时，才执行新建
                if doc_count == 0:
                    try:
                        print("[licad] 检测到 CAD 运行中但无文档 (Count=0)，正在新建...")
                        doc = app.Documents.Add()
                        # 等待初始化
                        for _ in range(5):
                            time.sleep(0.2)
                            try:
                                if doc.Name: break
                            except: pass
                        return app, doc
                    except Exception as e_add:
                        print(f"[licad] 新建文档失败: {e_add}")
                        raise e_doc # 新建失败，抛出异常让外层重试

                else:
                    # 3. 如果 doc_count > 0，或者读取失败 (-1)
                    # 说明有文档但拿不到 ActiveDocument，这是 CAD 在忙（如正处于命令中、有弹窗等）
                    # 此时绝对不能新建，而是抛出异常进入外层的“等待重试”循环
                    print(f"[licad] 获取文档失败但存在 {doc_count} 个文档。CAD 可能正忙/有弹窗/在命令中。")
                    raise RuntimeError("AutoCAD 忙碌或被阻塞，暂时无法获取活动文档。")

        except pythoncom.com_error as e:
            # --- 阶段 C: 全局 COM 异常处理 (RPC 忙碌等) ---
            code = e.args[0] if e.args else None
            # RPC 忙碌 / 呼叫被拒绝 / 无法获取对象
            if (time.time() - t0 < max_wait):
                # 打印个简单的点，表示在等
                print(".", end="", flush=True) 
                time.sleep(0.5)
                continue
            else:
                raise RuntimeError("连接超时：AutoCAD 响应过慢或处于长期忙碌状态(请检查是否有未关闭的对话框)。")

        except Exception as e:
            # 其他未知错误
            if (time.time() - t0 < max_wait):
                time.sleep(0.5); continue
            raise e

# =================================================================
# 3. 核心代理类 (真正的逻辑实现者)
# =================================================================

class AutoCadProxy:
    def __init__(self):
        self._acad = None
        self._doc = None
        self._mp = None
        self._sp = None

    # -------------------------------------------------------------
    # 连接逻辑 (保留你的三层验证)
    # -------------------------------------------------------------
    def li(self):
        """
        [智能连接]
        1. 极速检查：当前持有对象是否就是 CAD 当前激活的窗口？
        2. 自动切换：如果用户切换了图纸，自动更新内部引用。
        3. 深度验证：仅在需要重连时执行画线防断测试。
        """
        # --- 第一层：快速路径 (Fast Path) ---
        try:
            if self._acad is None or self._doc is None:
                raise RuntimeError("需要初始化")

            try:
                real_active_doc = self._acad.ActiveDocument
            except:
                raise RuntimeError("RPC忙碌")
            
            # 检查名字一致性 (防切屏)
            if self._doc.Name != real_active_doc.Name:
                # print(f"[li] 窗口切换: {self._doc.Name} -> {real_active_doc.Name}")
                raise RuntimeError("文档焦点已改变")

            return True
        except Exception:
            pass # 进入重连

        # --- 第二层：重连 (Reconnect) ---
        try:
            # 【修改】这里直接调用上面定义的公开函数
            new_acad, new_doc = get_acad_doc()
        except Exception as e:
            print(f"[li] 致命错误：无法连接 AutoCAD 进程。{e}")
            return False

        # --- 第三层：深度验证 (画线测试) ---
        try:
            test_mp = new_doc.ModelSpace
            pt1 = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (0, 0, 0))
            pt2 = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (10, 0, 0))
            line = test_mp.AddLine(pt1, pt2)
            _ = line.Handle
            line.Delete()
        except Exception as e:
            print(f"[li] 重连验证失败 (可能处于命令中或只读): {e}")
            return False

        # --- 收尾：更新状态 ---
        self._acad = new_acad
        self._doc = new_doc
        self._mp = new_doc.ModelSpace
        self._sp = new_doc.PaperSpace

        try:
            if not self._acad.Visible: self._acad.Visible = True
        except: pass

        print(f"[li] 连接已刷新: {self._doc.Name}")
        return True

    # --- 属性代理 ---
    @property
    def acad(self): self.li(); return self._acad
    @property
    def doc(self): self.li(); return self._doc
    @property
    def mp(self): self.li(); return self._mp
    @property
    def sp(self): self.li(); return self._sp

    # -------------------------------------------------------------
    # 文件操作逻辑
    # -------------------------------------------------------------

    @_retry_on_busy
    def save_file(self):
        try:
            doc = self.doc 
            name = doc.Name
            doc.Save()
            print(f"[licad] 成功保存: {name}")
            return True
        except Exception as e:
            print(f"[licad] 保存失败: {e}")
            return False

    @_retry_on_busy
    def save_file_as(self, output_path):
        try:
            doc = self.doc
            path_obj = Path(output_path).resolve()
            
            if not path_obj.parent.exists():
                print(f"[licad] 错误: 目标目录不存在 {path_obj.parent}")
                return False

            print(f"[licad] 正在另存为: {path_obj.name}")
            doc.SaveAs(str(path_obj))
            
            self.li() 
            return True
        except Exception as e:
            print(f"[licad] 另存为失败: {e}")
            return False

    @_retry_on_busy
    def open_file(self, file_path):
        target_path = str(Path(file_path).resolve()).lower()
        
        # 1. 检查内存
        try:
            for d in self.acad.Documents:
                try:
                    if str(Path(d.FullName).resolve()).lower() == target_path:
                        print(f"[licad] 文件已打开，正在激活: {d.Name}")
                        d.Activate()
                        self.li()
                        return True
                except: continue
        except: pass

        # 2. 物理打开
        if not os.path.exists(file_path):
            print(f"[licad] 文件不存在: {file_path}")
            return False

        try:
            print(f"[licad] 正在打开: {Path(file_path).name}")
            self.acad.Documents.Open(str(file_path))
            self.li()
            return True
        except Exception as e:
            print(f"[licad] 打开失败: {e}")
            return False

    @_retry_on_busy
    def close_file(self, save_option="auto_save"):
        try:
            doc = self.doc
            name = doc.Name
            
            if save_option == "auto_save":
                self.save_file()
                doc.Close(False)
            elif save_option == "no_save":
                doc.Close(False)
            else:
                doc.Close(False)

            print(f"[licad] 已关闭: {name}")
            
            try: self.li()
            except: pass
            
            return True
        except Exception as e:
            print(f"[licad] 关闭失败: {e}")
            return False

    def close_dwg_by_name(self, name):
        try:
            app = win32com.client.GetActiveObject("AutoCAD.Application")
            doc = app.Documents.Item(name)
            doc.Close(False)
            print(f"[licad] 文件 '{name}' 已关闭")
            return True
        except Exception as e:
            print(f"[licad] 关闭 '{name}' 失败: {e}")
            return False

# =================================================================
# 4. 单例实例化
# =================================================================

C = AutoCadProxy()

# =================================================================
# 5. 模块级函数导出 (提供给外部脚本调用)
# =================================================================

def li():
    return C.li()

def save_file():
    return C.save_file()

def save_file_as(output_path):
    return C.save_file_as(output_path)

def open_file(file_path):
    return C.open_file(file_path)

def close_file(save_option="auto_save"):
    return C.close_file(save_option)

def close_dwg_by_name(name):
    return C.close_dwg_by_name(name)

# 【新增】导出装饰器
def retry_on_busy(func):
    return _retry_on_busy(func)

# 兼容旧代码的全局变量 (虽然不建议直接用)
acad = None 
doc = None
