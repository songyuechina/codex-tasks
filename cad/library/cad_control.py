#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第七部分 综合控制
综合控制相关函数

从 CAD_basic.py 拆分而来
"""

# 路径引导
import sys
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

# 导入系统模块
from system.project_setup import PathConfig
from system.licad import C
from system.CAD_com_utils import sys_logger, retry_on_busy, SafeCOM
from system.common_logger import checkpoint
import os
import shutil

# 获取常用对象
acad = C.acad
doc = C.doc
mp = C.mp
sp = C.sp

#&&&&%% 第七部分 综合控制

#&&&% 系统操作

#&&% 清理缓存
"""
在你的 li() 初始化函数或错误处理逻辑中，建议加入一个**“万能重试机制”**：

如果捕获到任何 AttributeError 且涉及 win32com，自动执行一次缓存清理，然后提示用户重启程序。

这样可以极大地降低维护成本，不用每次报错都去手动删文件夹。

"""
def fix_com_cache():
    """
    【急救】清理 win32com 的 gen_py 缓存
    解决 'CLSIDToPackageMap' 或 'AttributeError' 等 COM 接口损坏问题。
    """
    import os
    import shutil
    import sys
    
    print("🧹 正在寻找损坏的 COM 缓存...")
    
    # 1. 尝试动态获取缓存路径
    try:
        import win32com
        #通常在 %TEMP%\gen_py 或 Python安装目录\Lib\site-packages\win32com\gen_py
        if hasattr(win32com, '__gen_path__'):
            gen_path = win32com.__gen_path__
        else:
            import win32com.client
            gen_path = win32com.client.gencache.GetGeneratePath()
    except Exception as e:
        sys_logger.info(f"无法自动定位路径，尝试标准位置... ({e})")
        gen_path = os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py')

    sys_logger.info(f"📍 定位到缓存路径: {gen_path}")

    # 2. 执行删除
    if os.path.exists(gen_path):
        try:
            # 必须删除整个文件夹，不仅仅是里面的文件
            shutil.rmtree(gen_path)
            print("✅ 成功删除损坏的缓存文件夹！")
            print("🚀 下次连接 CAD 时，Python 会自动重新生成它（可能会慢 1-2 秒，正常现象）。")
        except Exception as e:
            sys_logger.info(f"❌ 删除失败 (可能文件被占用): {e}")
            print("请手动删除该文件夹！")
    else:
        print("❓ 未找到缓存文件夹，可能已经被清理过了。")

    # 3. 还有一种情况：在 site-packages 里的只读缓存
    try:
        import site
        for site_package in site.getsitepackages():
            win32_path = os.path.join(site_package, "win32com", "gen_py")
            if os.path.exists(win32_path):
                sys_logger.info(f"🔎 发现系统级缓存: {win32_path}")
                try:
                    shutil.rmtree(win32_path)
                    print("✅ 系统级缓存已清理。")
                except:
                    print("⚠️ 系统级缓存清理失败 (可能需要管理员权限)，通常忽略即可。")
    except: pass




#&&% 清除nul

def delete_all_nul_under_folder(folder_path):
    """
    输入文件夹路径（如 D:\claude-tasks），
    自动扫描该文件夹及所有子文件夹，强制删除所有名为 'nul' 的文件。
    """
    # 1. 获取绝对路径，确保格式正确
    target_dir = os.path.abspath(folder_path)
    
    if not os.path.exists(target_dir):
        sys_logger.info(f"❌ 错误：找不到文件夹 {target_dir}")
        return

    sys_logger.info(f"🔎 正在扫描文件夹: {target_dir} ...")
    
    count = 0
    
    # 2. 递归遍历目录树 (root: 当前路径, dirs: 子文件夹, files: 文件列表)
    for root, dirs, files in os.walk(target_dir):
        # 检查文件列表中是否有 'nul' (Windows下通常不区分大小写，但也做个.lower()保险)
        for filename in files:
            if filename.lower() == "nul":
                # 构造普通完整路径
                full_path = os.path.join(root, filename)
                
                # 3. 构造强制删除路径 (UNC Path)
                # 核心技巧：加上 \\.\ 前缀绕过 Windows 设备检查
                unc_path = r"\\.\%s" % full_path
                
                try:
                    os.remove(unc_path)
                    sys_logger.info(f"✅ [删除成功] {full_path}")
                    count += 1
                except Exception as e:
                    sys_logger.info(f"❌ [删除失败] {full_path} -> 原因: {e}")

    if count == 0:
        print("✨ 扫描完成，未发现 'nul' 文件。")
    else:
        sys_logger.info(f"🎉 扫描完成，共删除了 {count} 个 'nul' 文件。")

#&&% 终止弹窗程序

def kill_dialog_killer():
    """
    查找并终止名为 'cad_dialog_killer.py' 的 Python 进程
    """
    print("正在检查并清理干扰进程...")
    # 使用 wmic 获取所有 python 进程的命令行参数
    try:
        # 获取进程列表 (PID 和 命令行)
        cmd = 'wmic process where "name=\'python.exe\'" get commandline,processid'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = proc.communicate()
        
        # 解码输出 (Windows通常是mbcs或gbk)
        output_str = stdout.decode('mbcs', errors='ignore')
        
        lines = output_str.strip().split('\n')
        killed = False
        
        for line in lines:
            if "cad_dialog_killer.py" in line:
                # 提取 PID (一般在行末)
                parts = line.strip().split()
                if parts:
                    pid = parts[-1]
                    if pid.isdigit():
                        sys_logger.info(f"发现干扰进程 (PID={pid})，正在终止...")
                        os.system(f"taskkill /F /PID {pid}")
                        killed = True
        
        if not killed:
            print("未发现 cad_dialog_killer.py 在运行。")
            
    except Exception as e:
        sys_logger.info(f"尝试清理进程时出错: {e}")





#&&% 终止指定py脚本 (psutil版)
def kill_python_script_by_name(target_script_name):
    """
    【推荐】使用 psutil 精准终止指定名称的 Python 脚本。
    能够准确处理命令行参数中包含空格路径的情况。
    """
    sys_logger.info(f"--- 正在检查进程: {target_script_name} ---")
    current_pid = os.getpid()
    target_lower = target_script_name.lower()
    killed_count = 0

    # 遍历所有进程
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # 1. 过滤掉非 Python 进程 (可选，为了提高效率)
            proc_name = proc.info['name'].lower() if proc.info['name'] else ""
            if "python" not in proc_name and "py.exe" not in proc_name:
                continue

            # 2. 获取命令行参数列表
            cmdline = proc.info['cmdline']
            if not cmdline:
                continue
            
            # 将命令行列表转换为字符串以便查找
            # cmdline 通常是 ['python.exe', 'D:/path/to/script.py', ...]
            cmd_str = " ".join(cmdline).lower()

            # 3. 核心判断：脚本名是否在命令行中
            if target_lower in cmd_str:
                pid = proc.info['pid']
                
                # 保护机制：不杀自己
                if pid == current_pid:
                    sys_logger.info(f"跳过自身进程 (PID={pid})")
                    continue

                sys_logger.info(f"发现目标进程 '{target_script_name}' (PID={pid})，正在终止...")
                
                # 4. 执行终止
                proc.kill() # 或者 proc.terminate()
                killed_count += 1
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 进程可能在遍历过程中已经消失或无法访问
            pass

    if killed_count == 0:
        sys_logger.info(f"未发现 {target_script_name} 在运行。")
    else:
        sys_logger.info(f"成功清理 {killed_count} 个目标进程。")
    
    return killed_count





#&&&% 重要基础知识（python、算法、数据结构）

#&&% ***🧠  抛出异常的处理逻辑

"""
1 try+except+finaly

成功后执行finaly后语句，失败后也会执行finaly后语句，必定预期整个代码段要做的就是finaly提供的功能


2 try+except+else

成功后执行else后语句，失败后不会会执行else后语句，必定预期成功情况下 要做的就是else提供的功能

3
try:
    risky_operation()
except SomeError as e:
    handle_error(e)
    # 这段只在 try 失败时运行
    try:
        do_special_on_failure()
    except Exception as e2:
        log("failure-only block failed:", e2)
else:
    # 成功时走这里
    do_if_success()
finally:
    cleanup()

do_special_on_failure() 就是专门为代码段失败时预期必定要执行的语句。它不同于直接放在except中，因为except可能的失败操作不能保证它被预期必然执行。

我们需要在某个操作失败时，必须执行某个操作，就使用这个逻辑



"""




#&&&% 脚本注释标准模块
# — — — — -- -- -- -- --  — — — — -- -- -- -- -- — — — — -- -- -- -- --  — — — — -- --

#📌 节点 1：形成正式“打印框线”并重排图形
#─────────────────────────────────────

"""🔍 输入:"""

"""🔧 关键函数："""
"""   > F1: `find_standard_printframes()` – 返回标准图框列表"""

"""🧠 处理逻辑:"""

"""📤 输出:"""


 

"""
🄐  🄑  🄒  🄓  🄔  🄕  🄖  🄗  🄘  🄙  🄚  🄛  🄜  🄝  🄞  🄟  🄠  🄡  🄢  🄣  🄤  🅅  🅆  🅇   🅈   🅉







⓿ ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ️⃣  

# ❖❖❖—— 重要函数：foo() ——❖❖❖

# ✺✺✺—— 关键逻辑：process_data()——✺✺✺

# ⚡⚡⚡—— 高优先：init_config() ——⚡⚡⚡

# ★★★—— 核心入口：main() ——★★★
常用符号推荐：

❖ （四角菱形）

✺ （放射状花瓣）

⚡ ★ （闪电）

★ （实心星）

✦ （中实菱形）

❗ （粗感叹号）

 
+--------------------------+
| 方法1：从打印图签块或打印线获取DX |
+--------------------------+
      ↓ 成功          ↓ 失败
+------------------+   +--------------------------+
| 从图签块重建框线 |   | 方法2：从"公司图签"图块提取DX |
+------------------+   +--------------------------+
           ↓                     ↓ 成功    ↓ 失败


+--------------------------------+
| 初始状态：未开始打印           |
+--------------------------------+
               ↓


        +---------+
        | F3函数  | ← 识别拟合框线对应图形
        +---------+
             ↓
 
📌 节点 1：确定“准打印框线”
─────────────────────────────────────
🔁 初始化阶段：
    > 清空 "准打印框线" 图层
    > 若已存在旧对象，则全部删除

🔍 提取打印框候选集合 DX 的三种方法：

① 方法一（推荐方式）
    > 查找 “图签块” + “打印框线” 块
    > 若存在图签块：
        > 提取包围盒 → 重绘为矩形 → 存入“准打印框线”
        > 清除原“打印框线”对象
        > [OK] 完成本节点目标


📦 输出：DX 对象集合 + “准打印框线”图层绘制

------------------------------------------------------

📌 节点 2：形成正式“打印框线”并重排图形
─────────────────────────────────────
🔍 输入：DX 集合（来自上节点）

🧠 图形分析与处理：
    > 识别标准打印框（F1）
    > 识别拟合打印框（F2）

🧱 图框替换与排版：
    > 拟合框 → 替换为最近 A1 标准比例图框
    > 重新排列打印图框，避免重叠

📦 输出：
    > 正式“打印框线”写入目标图层
    > 准打印框图层清空
    > Handle → 信息存储用于后续匹配

🔧 函数：
    > F1: 标准框识别
    > F2: 拟合框识别
    > F3: 图形识别归属（局部）
    > F4: 图形重排整体逻辑

┌────────────┐> F1: 标准框识别 
│ 节点 1：   │
│ 准打印框线 │
└────┬───────┘
     │ 清空图层
     ▼
┌────────────┐
│ 方法一：图签块或框线 │◄─────┐
└────┬──────────────┘      │
     │ 找不到             │
     ▼                    │

┌────────────┐
│ 排序 + 移动图形 F3/F4 │
└────┬────────┘
     ▼
┌────────────────────┐
│ 写入“打印框线”图层 │
└────────────────────┘

📌 节点 X：<简要标题>
─────────────────────────────────────
🔍 输入：
    > 输入数据或图元说明（如 DX 集合）
    > 来源说明（如来自上游节点）
    
🧠 处理逻辑：
    > 步骤说明 1（如：识别标准打印框）
    > 步骤说明 2（如：判断拟合框）

🔧 关键函数：
    > F1: 函数名 – 功能说明
    > F2: 函数名 – 功能说明

📤 输出：
    > 输出数据目标（如写入正式图层）
    > 副作用（如清除中间层、更新 handle 记录）

[警告]️ 异常处理：
    > 未匹配图框 → 输出警告
    > 多图重叠 → 排序并修正重排

🗂 示例调用：
    process_printframes(DX)


📌	节点起始	📌 节点 2：形成正式“打印框线”并重排图形
────────────	分割线	──────── 节点分隔 ────────
🧭	逻辑导向	🧭 下一步识别拟合图框
🔀	路径分支	🔀 分流处理：标准框 vs 拟合框
⤵ / ⤴	子流程跳转	⤵ 进入子流程 F3
🔂	循环处理	🔂 针对所有 F2 框执行替换逻辑

🔧 功能或模块说明
符号	用途	示例
🔧	函数定义	🔧 F1: 标准框识别函数
🧠	处理逻辑	🧠 图形分析与处理
🧪	测试/调试块	🧪 临时打印 bbox 信息
📦	输出结果	📦 输出图层对象
📥 / 📤	输入/输出	📤 输出写入 LAYER_PRINT 正式图框
🧱	数据结构/实体对象	🧱 实体对象替换操作

🔍 分析与识别相关
符号	用途	示例
🔍	搜索/识别	🔍 查找符合 A1 比例的图框
🧬	特征提取	🧬 提取图形外包盒坐标与宽高比
🔎	精细识别	🔎 判断是否为完整封闭矩形

[OK] 状态反馈
符号	用途	示例
[OK]	成功	[OK] 图框替换完成
[警告]️	警告	[警告]️ 找不到合适图框匹配项
[错误]	错误	[错误] 无法识别多段线边界
⏳	等待	⏳ 等待 CAD 对象响应

🔁 控制结构（可嵌入注释中）
符号	用途	示例
⬅️ ➡️ ⬆️ ⬇️	方位、移动方向	⬆️ 上移图框 1000 单位避免重叠
🔄	重复执行	🔄 对所有图框执行一次旋转检测
↪️	返回	↪️ 返回原图层处理状态

📊 数据操作与计算
符号	用途	示例
📐	几何计算	📐 计算图框宽高比
📏	测量	📏 测量距离与偏移
🧮	数值处理	🧮 总计图框数量 = len(F1) + len(F2)



"""

#&&% 结束WPS进程
def kill_wps(verbose: bool = False):
    """
    结束所有 WPS/金山办公相关进程，特别是 wpspdf.exe。
    verbose=True 时打印被终止的映像名。
    """
    # 需要关掉的映像清单（全部小写）
    targets = {
        "wps.exe",          # WPS 主进程
        "wpspdf.exe",       # ★ PDF 预览器
        "wpp.exe",          # 演示
        "et.exe",           # 表格
        "ksolaunch.exe",    # 启动器
        "wpscloudsvr.exe",  # 云同步
        "wpsupdate.exe",    # 更新器
        "wpscenter.exe",    # 消息中心
    }

    killed = set()
    for name in targets:
        # /T 连子进程一起；/F 强制；/IM 按映像名
        rc = subprocess.call(
            f'taskkill /T /F /IM {name}',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if rc == 0:      # 返回 0 表示确有此进程并已结束
            killed.add(name)

    if verbose:
        if killed:
            print("[OK] 已结束进程:", ", ".join(sorted(killed)))
        else:
            print("ℹ️ 未检测到 WPS 相关进程")


#&&%关闭excel进程

def close_all_excel_processes():
    """
    【函数编号】: SYS-KILL-XLS
    【功能描述】: 
        强制关闭所有 EXCEL.EXE 进程。
        使用 taskkill /F 强制终止，包含重试机制。
        
    【返回】: 
        bool: True (成功/无进程), False (失败)
    """
    import subprocess
    import time

    # --- 内部辅助：检测Excel进程数 ---
    def _get_excel_count():
        try:
            # 使用 tasklist 查找映像名称为 EXCEL.EXE 的进程
            # /NH 不显示列标题, /FO CSV 输出格式便于解析
            cmd = 'tasklist /FI "IMAGENAME eq EXCEL.EXE" /NH /FO CSV'
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                shell=True
            )
            # 统计输出中 "EXCEL.EXE" 出现的次数 (忽略大小写)
            if result.stdout:
                return result.stdout.lower().count("excel.exe")
            return 0
        except Exception:
            return 0

    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # 1. 检查当前 Excel 进程数
            process_count = _get_excel_count()
            
            if process_count == 0:
                # 如果是第一次循环就没发现，说明本来就没开
                if attempt == 0:
                    print("[信息] 没有 Excel 进程需要关闭")
                return True

            sys_logger.info(f"[清理] 检测到 {process_count} 个 Excel 进程，正在强制关闭 (第 {attempt + 1} 次)...")

            # 2. 使用 taskkill 强制终止
            # /F: 强制终止
            # /IM: 指定映像名称
            # /T: 终止指定的进程及其启动的任何子进程 (Excel常有子挂起进程)
            result = subprocess.run(
                ["taskkill", "/F", "/IM", "EXCEL.EXE", "/T"],
                capture_output=True,
                text=True,
                timeout=10,
                shell=True # Windows下建议开启shell以兼容路径问题
            )

            # 3. 检查结果
            # returncode 0: 成功终止
            # returncode 128: 进程未找到 (可能在检查和执行之间已自行关闭)
            if result.returncode == 0 or result.returncode == 128:
                print("[执行] 终止指令已发送，等待进程释放...")
                time.sleep(1.5) # 给系统一点反应时间

                # 4. 再次验证
                process_count_after = _get_excel_count()
                if process_count_after == 0:
                    print("[验证] 所有 Excel 进程已成功关闭")
                    return True
                else:
                    sys_logger.info(f"[警告] 仍有 {process_count_after} 个 Excel 进程顽固残留")
            else:
                sys_logger.info(f"[警告] taskkill 返回码: {result.returncode}")
                # sys_logger.info(f"[调试] {result.stderr}") 

        except subprocess.TimeoutExpired:
            sys_logger.info(f"[错误] 第 {attempt + 1} 次关闭操作超时")
        except Exception as e:
            sys_logger.info(f"[错误] 关闭 Excel 时发生异常: {e}")

        # 如果还没成功，等待后重试
        if attempt < max_retries - 1:
            sys_logger.info(f"[重试] 等待 1 秒后重试...")
            time.sleep(1)

    print("[失败] 达到最大重试次数，无法彻底关闭所有 Excel 进程")
    return False














#&&&% 确保安全删除
def safe_delete(ob, retries: int = 3, delay: float = 1) -> bool:
    """
    安全删除 CAD 对象。
    
    改进点：
    1. 删除前先检查对象有效性，避免对已删除对象报错重试。
    2. 缩短默认等待时间 (1.0s -> 0.1s)。
    3. 成功删除或对象本就不存在，都返回 True。
    """
    
    # --- 1. 空对象检查 ---
    if ob is None:
        return True

    # --- 2. 有效性预检查 ---
    # 尝试访问 Handle 属性。如果访问失败，说明对象已经失效/被删除。
    try:
        _ = ob.Handle
    except Exception:
        # 访问属性失败，说明对象极可能已经不存在了，视为“删除成功”
        return True

    # --- 3. 尝试删除循环 ---
    for attempt in range(1, retries + 1):
        try:
            ob.Delete()
            return True
        
        except pywintypes.com_error as e:
            # 获取错误码 (HRESULT)
            # -2147418111 (0x80010001)通常是 Call rejected by callee (CAD正忙)
            # 还有可能是对象被锁定
            
            error_code = e.hresult
            
            # 如果错误提示对象已失效 (例如 e.excepinfo 可能包含 'eWasErased')
            # 不同的 CAD 版本/接口错误信息可能不同，但通常如果 Delete 失败，
            # 我们再检查一次 Handle，如果 Handle 也没了，就说明其实删掉了。
            try:
                _ = ob.Handle
            except Exception:
                # 再次确认 Handle 无法访问，说明刚才的 Delete 可能其实生效了，或者并发被删了
                return True

            # 如果对象还在，且报错，说明是“繁忙/锁定”，需要等待重试
            if attempt < retries:
                time.sleep(delay)
            else:
                # 此时 debug 模式下可以打印错误信息
                # sys_logger.info(f"删除失败 Handle={ob.Handle}: {e}")
                pass

    return False



#&&&%  * 高亮选择转隐性移动区域内全部对象


"""
高亮选择窗口操作更可靠从而更快，但要考虑窗口不能挡

"""

#&&% 区域实体移动
def move_entities_in_region(coms, target=(0,0,0), ty=1, max_iter=3):
    """
    将 `coms` 对象的包围盒内所有实体，沿向量 (target - 左下角) 移动，
    每轮等待 `ty` 秒，最多循环 `max_iter` 次。

    参数：
      coms      -- 支持 GetBoundingBox() 的 COM 对象（如多段线、块参照等）
      target    -- 目标基点坐标，默认为 (0,0,0)
      ty        -- 每轮移动后等待秒数
      max_iter  -- 最多尝试的轮数
    """
    # 1. 读取包围盒，计算左下角 (x1,y1) 和右上角 (x2,y2)
    p1, p2 = coms.GetBoundingBox()
    x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
    x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])

    # 2. 计算位移向量 Δ = target - (x1,y1)
    dx = target[0] - x1
    dy = target[1] - y1
    dz = target[2] - 0.0

    for i in range(1, max_iter + 1):
        # 清空显性选择集
        try:
            doc.PickfirstSelectionSet.Clear()
        except Exception:
            pass

        # 3. 在 CAD 里用窗口选择高亮区域内对象
        highlight_entities_in_window(x1, y1, x2, y2)

        # 4. 拿到显性选择集里的实体
        pick = doc.PickfirstSelectionSet
        count = pick.Count if hasattr(pick, 'Count') else len(list(pick))
        if count == 0:
            sys_logger.info(f"[OK] 第 {i} 轮：区域已清空，停止。")
            break

        sys_logger.info(f"♻️ 第 {i} 轮：检测到 {count} 个对象，正在移动…")
        # 5. 对每个实体按计算好的向量执行 Move
        for ent in pick:
            try:
                # 从 (x1,y1,0) 移动到 (x1+dx, y1+dy, dz)
                ent.Move(vtpnt(x1, y1, 0.0),
                         vtpnt(x1 + dx, y1 + dy, dz))
            except Exception as e:
                sys_logger.info(f"  [警告] 对象 {ent.Handle} 移动失败：{e}")

        # 6. 等待 CAD 完成命令再进入下一轮
        time.sleep(ty)
    else:
        print("[警告] 达到最大迭代次数，可能仍有残留对象。")


#&&&% 显示控制

#&&% 设置点样式
def 圆点(tz=1):


    """
    控制点的显示

    """

    zhi=0

    if tz ==1:

        zhi=35

    acad.ActiveDocument.SetVariable("PDMODE", zhi)#就是点最好的圆加十字形显示



#&&% 设置图纸背景色
def 图纸背景(zhi = 16777215 ):

    acad.ActiveDocument.Application.preferences.Display.GraphicsWinModelBackgrndColor = zhi#0即变成黑色





#&&&%  *** 按区域调整视图

#&&% 视图区域缩放
def  shitu_region(x1,y1,x2,y2):

    """
    按按对象外包盒调整视图
    使用时可shitu_region(*p),p=(x1,y1,x2,y2)

    """

    h=0.3*(abs(x1-x2)+abs(y1-y2))/2

    # 1️⃣ 缩放视图到合适窗口
    zoom_cmd = (
        f"_.ZOOM\n"      # 调用 Zoom
        f"_W\n"          # 窗口选项
        f"{x1-h},{y1-h}\n"   # 第一个角点
        f"{x2+h},{y2+h}\n"   # 第二个角点
    )
    doc.SendCommand(zoom_cmd)

#按对象外包盒调整视图

#&&% 视图实体缩放
def  shitu_entity(obj):

    """
    按按对象外包盒调整视图

    """
    p1,p2=obj.GetBoundingBox()

    x1,y1=p1[0],p1[1]

    x2,y2=p2[0],p2[1]

    h=0.3*(abs(x1-x2)+abs(y1-y2))/2

    # 1️⃣ 缩放视图到合适窗口
    zoom_cmd = (
        f"_.ZOOM\n"      # 调用 Zoom
        f"_W\n"          # 窗口选项
        f"{x1-h},{y1-h}\n"   # 第一个角点
        f"{x2+h},{y2+h}\n"   # 第二个角点
    )
    doc.SendCommand(zoom_cmd)




#&&% 截屏
"""
# 1. 截取全屏，返回一个 PIL.Image 对象
img = pyautogui.screenshot()

# 2. 如果想直接保存到文件：
pyautogui.screenshot('full_screen.png')

# 3. 只截取屏幕的一部分（x, y, width, height）
#    例如：从左上角 (100,100) 开始，截取 300×200 的区域
region_img = pyautogui.screenshot(region=(100, 100, 300, 200))
region_img.save('partial.png')


"""

#&&% 录制屏幕GIF
def record_screen_gif(
    output_path: str,
    duration: float = 5.0,
    fps: int = 10,
    region: tuple[int,int,int,int] | None = None
):
    """
    录制屏幕并保存为 GIF。

    :param output_path: 输出 GIF 文件路径，比如 "demo.gif"
    :param duration:    录制时长（秒）
    :param fps:         帧率（每秒截多少帧）
    :param region:      可选，(left, top, width, height) 只录制这一区域
    """
    import imageio 

    frames = []
    interval = 1.0 / fps
    end_time = time.time() + duration

    sys_logger.info(f"▶ 开始录制：时长={duration}s，帧率={fps}fps，区域={region or '全屏'}")
    while time.time() < end_time:
        img = pyautogui.screenshot(region=region)  # PIL.Image 对象
        frames.append(img)
        time.sleep(interval)

    sys_logger.info(f"🛑 录制结束，共捕获 {len(frames)} 帧，正在合成 GIF……")
    # imageio 能直接接受 PIL.Image
    imageio.mimsave(output_path, frames, fps=fps)
    sys_logger.info(f"[OK] 已保存为 {output_path}")


#&&&% 窗口控制

#&&% 最小化所有窗口
def minimize_all_windows():
    """
    模拟按下 Win+M，将所有窗口最小化。

    特性	Win + D (显示桌面)	Win + M (最小化所有)
    核心逻辑	切换开关 (Toggle)	单向命令 (Command)
    动作行为	
    第1次：隐藏所有窗口
    
    
    第2次：恢复原窗口布局
    
    第1次：最小化所有窗口
    
    
    第2次：无变化 (继续保持最小化)
    
    覆盖范围	极强。能隐藏几乎所有类型的窗口（包括无法最小化的对话框）。	普通。只能最小化支持“最小化”属性的窗口（某些固定对话框可能关不掉）。
    自动化风险	高。如果脚本判断失误连续运行了两次，窗口会弹回来，导致后续截图或操作失败。	低。它是幂等的（Idempotent），无论运行多少次，窗口都是最小化状态，适合“强制清场”。
    恢复方式	再按一次 Win+D	需要按 Win+Shift+M
    

    """

    import ctypes

    user32 = ctypes.windll.user32
    VK_LWIN = 0x5B   # 左 Win 键
    VK_M    = 0x4D   # M 键
    KEYEVENTF_KEYUP = 0x2

    # 按下 Win
    user32.keybd_event(VK_LWIN, 0, 0, 0)
    # 按下 M
    user32.keybd_event(VK_M,    0, 0, 0)
    # 松开 M
    user32.keybd_event(VK_M,    0, KEYEVENTF_KEYUP, 0)
    # 松开 Win
    user32.keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0)

    # 给系统一点反应时间
    time.sleep(0.1)



#&&%#控制CAD屏幕窗口在左上角


#&&% CAD窗口置左上
def set_autocad_window_to_top_left(resize_half: bool = True):
    """
    将 AutoCAD 窗口还原并移动到屏幕左上角，可选将其调整为半屏大小。
    """
    # 1️⃣ 找到可见或最小化的 AutoCAD 窗口
    windows = [w for w in gw.getWindowsWithTitle('AutoCAD')]
    if not windows:
        print("[错误] 未找到 AutoCAD 窗口！")
        return
    win = windows[0]

    # 2️⃣ 如果窗口最小化，先还原
    if win.isMinimized:
        win.restore()
        time.sleep(0.3)

    # 3️⃣ 激活窗口，确保我们操作的是真正的前台窗口
    try:
        win.activate()
    except Exception:
        # 有时 activate 也会失败，短暂等待再试
        time.sleep(0.2)
        win.activate()
    time.sleep(0.2)

    # 4️⃣ 移动到左上角 (0,0)
    win.moveTo(0, 0)
    time.sleep(0.2)

    # 5️⃣ 可选：将窗口调整为屏幕一半大小
    if resize_half:
        screen_w, screen_h = pyautogui.size()
        win.resizeTo(screen_w // 2, screen_h // 2)
        time.sleep(0.2)
        sys_logger.info(f"[OK] AutoCAD 窗口已恢复并移动到左上角，尺寸设为 {screen_w//2} x {screen_h//2}")
    else:
        print("[OK] AutoCAD 窗口已恢复并移动到左上角")



#&&% CAD窗口置左上别名
def l():

    set_autocad_window_to_top_left()



#&&% 更合理控制窗口函数
# — — — — -- -- -- -- --  — — — — -- -- -- -- -- — — — — -- -- -- -- --  — — — — -- --

#&&% 最小化窗口Win+D
def minimize_all_windows_d():
    """
    模拟 Win + D，将所有窗口最小化（切换）。
    """
    # VK_LWIN = 0x5B, VK_D = 0x44, KEYEVENTF_KEYUP = 0x2
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)       # 按下 Win
    ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)       # 按下 D
    ctypes.windll.user32.keybd_event(0x44, 0, 0x2, 0)     # 松开 D
    ctypes.windll.user32.keybd_event(0x5B, 0, 0x2, 0)     # 松开 Win
    time.sleep(0.3)


#&&% 最小化窗口Win+M
def minimize_all_windows_m():
    """
    模拟按下 Win+M，将所有窗口最小化。
    """
    user32 = ctypes.windll.user32
    VK_LWIN = 0x5B   # 左 Win 键
    VK_M    = 0x4D   # M 键
    KEYEVENTF_KEYUP = 0x2

    # 按下 Win
    user32.keybd_event(VK_LWIN, 0, 0, 0)
    # 按下 M
    user32.keybd_event(VK_M,    0, 0, 0)
    # 松开 M
    user32.keybd_event(VK_M,    0, KEYEVENTF_KEYUP, 0)
    # 松开 Win
    user32.keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0)

    # 给系统一点反应时间
    time.sleep(0.1)


#&&% 恢复并定位窗口
def restore_and_position(
    name: str = "AutoCAD",
    width_ratio: float = 0.5,
    height_ratio: float = 0.5,
    x: int = 0,
    y: int = 0
) -> bool:
    """
    将第一个标题中包含 name 的窗口恢复、激活，并调整到指定位置和大小。

    :param name:          窗口标题关键字，默认 "AutoCAD"
    :param width_ratio:   窗口宽度占屏幕宽度的比例 (0 < ratio ≤ 1)
    :param height_ratio:  窗口高度占屏幕高度的比例 (0 < ratio ≤ 1)
    :param x:             窗口左上角 X 坐标，默认 0
    :param y:             窗口左上角 Y 坐标，默认 0
    :return:              找到并操作成功返回 True，否则 False
    """
    # ① 查找窗口
    candidates = [w for w in gw.getWindowsWithTitle(name) if w.title]
    if not candidates:
        sys_logger.info(f"[错误] 未找到标题包含 “{name}” 的窗口。")
        return False
    win = candidates[0]

    # ② 如果最小化，则还原
    if win.isMinimized:
        try:
            win.restore()
            time.sleep(0.2)
        except Exception as e:
            sys_logger.info(f"[警告] 无法还原窗口：{e}")

    # ③ 激活窗口（置于最前）
    try:
        win.activate()
    except Exception:
        time.sleep(0.1)
        try:
            win.activate()
        except Exception as e:
            sys_logger.info(f"[警告] 激活窗口失败：{e}")

    time.sleep(0.2)

    # ④ 移动到指定位置
    try:
        win.moveTo(x, y)
    except Exception as e:
        sys_logger.info(f"[警告] 移动窗口失败：{e}")

    time.sleep(0.2)

    # ⑤ 调整窗口大小
    sw, sh = pyautogui.size()
    # 限制比例范围
    wr = max(0.01, min(1.0, width_ratio))
    hr = max(0.01, min(1.0, height_ratio))
    new_w = int(sw * wr)
    new_h = int(sh * hr)
    try:
        win.resizeTo(new_w, new_h)
        time.sleep(0.2)
    except Exception as e:
        sys_logger.info(f"[警告] 调整窗口大小失败：{e}")

    sys_logger.info(f"[OK] 已将窗口“{win.title}”移动到 ({x},{y})，并调整为 {new_w}×{new_h}（占屏幕 {wr*100:.0f}% × {hr*100:.0f}%）")

    return True



#&&% 列出打开窗口标题
def list_open_window_titles() -> list[str]:
    """
    获取当前所有可见窗口的标题列表包括子窗口。

    :return: 一个字符串列表，每一项都是一个非空窗口标题。
    """
    titles = []
    for w in gw.getAllWindows():
        title = w.title.strip()
        if title:
            titles.append(title)
    return titles

#&&% 测鼠标位置
def ceshubiao_weizhi():
    """
    提示用户 5 秒内将鼠标移动到 AutoCAD 命令栏输入位置，
    然后采集当前鼠标坐标并返回 (x, y)。
    """
    print("请在 5 秒钟内，将鼠标精确地放在 AutoCAD 命令栏的输入位置…")
    time.sleep(5)
    x, y = pyautogui.position()
    sys_logger.info(f"已获取坐标：({x}, {y})")
    return x, y

#&&% 后台运行IDLE
def run_idle_background(script_path: str):
    """
    用后台模式启动 IDLE 去运行某个脚本，返回 Popen 实例。
    """
    # Windows 上隐藏窗口的 flag
    CREATE_NO_WINDOW = 0x08000000
    proc = subprocess.Popen([
            sys.executable, "-m", "idlelib", "-r", script_path
        ],
        creationflags=CREATE_NO_WINDOW,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return proc



"""
idle_proc = run_idle_background(r"D:/Myprogramsystem/cad/CAD基本操作.py")
# 结束刚才启动的 IDLE
idle_proc.terminate()
idle_proc.wait(timeout=5)
"""


#&&% 点击并拖动
def click_and_drag(x: int, y: int, juli: int):
    """
    在屏幕坐标 (x, y) 按下左键，然后向纵向拖动距离 juli。
    若 juli 为正值，则向上拖动；若为负值，则向下拖动。
    """
    # 1. 移动到 (x, y)
    pyautogui.moveTo(x, y)

    time.sleep(2) 

    # 2. 按住左键
    pyautogui.mouseDown(button='left')

    # 3. 拖动：拖动到 (x, y + juli)
    #    如果仅需相对拖动，也可用 dragRel(0, juli)。
    dest_x = x
    dest_y = y - juli  # 注意：屏幕坐标里，向上是 y 减小，向下是 y 增大
    pyautogui.moveTo(dest_x, dest_y, duration=0.2)

    # 4. 松开左键
    pyautogui.mouseUp(button='left')


#&&% 点击并找图
def click_and_find_image_shape(x: int, y: int, tupian_path: str, timeout: float = 10.0):
    """
    在 (x, y) 单击一次，然后不断在整个屏幕上查找与 tupian_path 对应的图片形状，
    一旦找到，就把鼠标移到它的中心并返回中心坐标 (Python int)；超时仍未找到则返回 None。

    :param x, y:        单击的初始坐标（可触发界面更新）
    :param tupian_path: 要识别的目标图片路径（如微信笑脸）
    :param timeout:     最长等待时间（秒）
    :return:            找到时返回 (x, y)；否则返回 None
    """
    if not os.path.isfile(tupian_path):
        raise FileNotFoundError(f"找不到图片文件：{tupian_path}")

    # 1. 右键点击 (x, y)
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(0.3)  # 等待界面刷新

    start = time.time()
    while True:
        # 2. 搜索图片并获取中心坐标
        loc = pyautogui.locateCenterOnScreen(tupian_path, confidence=0.9)
        if loc:
            cx, cy = loc
            # 转为 Python int 再移动
            cx, cy = int(cx), int(cy)
            pyautogui.moveTo(cx, cy)
            return cx, cy

        # 3. 检查超时
        if time.time() - start > timeout:
            print("[错误] 超时，未能识别到指定图片形状。")
            return None

        time.sleep(0.2)


#&&% 右键点击并移动
def right_click_and_move(x: int, y: int, x_xiangdui: int, y_xiangdui: int):
    """
    在屏幕坐标 (x, y) 处执行右键点击，然后将鼠标相对于 (x, y) 
    移动到 (x + x_xiangdui, y + y_xiangdui) 并停留。

    :param x:            初始水平坐标
    :param y:            初始垂直坐标
    :param x_xiangdui:   相对水平偏移（正值向右，负值向左）
    :param y_xiangdui:   相对垂直偏移（正值向下，负值向上）
    """
    # 移动到目标位置并右键点击
    pyautogui.moveTo(x, y)
    pyautogui.click(button='right')
    time.sleep(2)
    # 计算相对目标位置
    dest_x = x + x_xiangdui
    dest_y = y + y_xiangdui
    # 平滑移动到新位置
    pyautogui.moveTo(dest_x, dest_y, duration=0.2)

#&&% 结束所有IDLE进程
def kill_all_idle():
    """
    终止所有名为 'idle' 或 'idle.exe' 的进程（不再需要任务管理器）。
    """
    for p in psutil.process_iter(("pid", "name")):
        name = (p.info["name"] or "").lower()
        if name.startswith("idle"):
            try:
                p.terminate()
            except Exception:
                pass


#&&% IDLE窗口置右上
def set_idle_window_to_top_right():

    # 获取IDLE窗口句柄
    windows = [w for w in gw.getWindowsWithTitle('IDLE') if w.visible]
    
    if not windows:
        print("[错误] 未找到IDLE窗口！")
        return
    
    # 获取IDLE主窗口
    win = windows[0]
    
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()

    # 计算窗口大小：横竖各占1/2
    half_width = screen_width // 2
    half_height = screen_height // 2

    # 将窗口移动到屏幕的右上角 (屏幕宽度的一半，顶部为0)
    win.moveTo(half_width, 0)

    # 调整窗口大小，设置为屏幕的1/2宽度和1/2高度
    win.resizeTo(half_width, half_height)
    
    sys_logger.info(f"[OK] IDLE窗口已调整到屏幕右上角，尺寸为 {half_width} x {half_height}")


def r():

    set_idle_window_to_top_right()

##控制OBS窗口在右下角
#&&% OBS窗口置右下
def place_obs_bottom_right():
    """
    将 OBS Studio 主窗口移动到屏幕右下角，并缩放为屏幕宽高的一半。
    - 若找不到 OBS 窗口，会打印错误信息。
    - 若有多个 OBS 窗口，仅操作第一个可见窗口。
    """
    # 1️⃣ 获取 OBS 主窗口
    obs_windows = [w for w in gw.getWindowsWithTitle('OBS') if w.visible]
    if not obs_windows:
        print('[错误] 未找到可见的 OBS Studio 窗口')
        return

    obs = obs_windows[0]            # 取第一个
    print(f'🔍 找到窗口: {obs.title}')

    # 2️⃣ 计算目标尺寸与位置 —— 右下角 1/4 区域
    screen_w, screen_h = pyautogui.size()
    half_w, half_h = screen_w // 2, screen_h // 2
    target_left = screen_w - half_w      # 右半屏起点
    target_top  = screen_h - half_h      # 下半屏起点

    # 3️⃣ 移动并缩放
    obs.moveTo(target_left, target_top)
    time.sleep(0.1)                      # 给系统一点缓冲
    obs.resizeTo(half_w, half_h)

    print(f'[OK] 已将 OBS 窗口调整到右下角 {half_w}×{half_h}')


def r2():

    place_obs_bottom_right()


#&&% 最小化指定窗口
def minimize_window(window_keyword: str = 'OBS') -> bool:
    """
    通用：最小化第一个标题包含 window_keyword 的可见窗口。

    :param window_keyword: 要匹配的窗口标题关键字（子串匹配），默认 'OBS'
    :return: 如果成功最小化返回 True，否则返回 False
    """
    # 1) 找到所有匹配的可见窗口
    windows = [w for w in gw.getWindowsWithTitle(window_keyword) if w.visible]
    if not windows:
        print(f'[错误] 未找到标题包含 "{window_keyword}" 的可见窗口')
        return False

    # 2) 取第一个并最小化
    win = windows[0]
    print(f'🔍 找到窗口: "{win.title}"，执行最小化')
    win.minimize()
    return True

#&&% 最大化CAD窗口
def maximize_autocad_window(window_keyword: str = 'AutoCAD') -> bool:
    """
    强制最大化第一个标题包含 window_keyword 的可见窗口。
    优先尝试使用 win32gui，如不可用则退回 ctypes 调用 user32。
    """
    # 1) 找到目标窗口
    wins = [w for w in gw.getWindowsWithTitle(window_keyword) if w.visible]
    if not wins:
        sys_logger.info(f"[错误] 未找到标题包含 “{window_keyword}” 的可见窗口")
        return False

    win = wins[0]
    hWnd = win._hWnd

    # 2) 先恢复（避免最小化状态），再最大化
    #    尝试使用 win32gui
    try:
        import win32gui, win32con
        win32gui.ShowWindow(hWnd, win32con.SW_RESTORE)
        time.sleep(0.1)
        win32gui.ShowWindow(hWnd, win32con.SW_MAXIMIZE)
    except ImportError:
        # 如果没有 pywin32，就退回 ctypes
        SW_RESTORE  = 9
        SW_MAXIMIZE = 3
        ctypes.windll.user32.ShowWindow(hWnd, SW_RESTORE)
        time.sleep(0.1)
        ctypes.windll.user32.ShowWindow(hWnd, SW_MAXIMIZE)

    time.sleep(0.2)  # 确保窗口完成最大化
    sys_logger.info(f"[OK] 已将窗口 “{win.title}” 最大化")
    return True


#&&% 点击开始OBS录制
def start_obs_recording_by_click(x: int = 1768, y: int = 872,
                                 button: str = 'left',
                                 clicks: int = 1,
                                 move_duration: float = 0.2):
    """
    通过鼠标点击屏幕上 (x,y) 坐标来控制 OBS 开始/停止录制。
    
    :param x: 目标点击点 X 坐标
    :param y: 目标点击点 Y 坐标
    :param button: 鼠标按钮，'left'、'right' 或 'middle'
    :param clicks: 点击次数，默认为单击
    :param move_duration: 从当前位置移动到目标的耗时（秒）
    """
    # 安全设置（可选）
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE    = 0.1

    # 1) 平滑移动到目标
    pyautogui.moveTo(x, y, duration=move_duration)
    # 2) 点击
    pyautogui.click(x=x, y=y, clicks=clicks, button=button)
    sys_logger.info(f"[OK] 已点击 ({x}, {y})，请检查 OBS 是否已开始/停止录制。")


#&&&% *** 录屏
#&&% 发送微信
def fs(x1,y1):
    """
    微信调到0.5窗口

    """
    
    pyautogui.moveTo(x1+595,y1+190)
    pyautogui.click(x1+595,y1+190)
    pyautogui.press("enter")

#&&% 选微信群
def xuanqun(x1,y1,neirong):
    
    copy_to_clipboard(neirong)

    pyautogui.moveTo(x1+128,y1+33) 
    pyautogui.click(x1+128,y1+33)   
    time.sleep(2)
    activate_window_by_title("微信")

    time.sleep(2)

    pyautogui.moveTo(x1+128,y1+33)

    activate_window_by_title("微信")

    time.sleep(2)

    pyautogui.click(x1+128,y1+33)
  

    pyautogui.hotkey('ctrl', 'v') 


    pyautogui.moveTo(x1+158,y1+49) 
    pyautogui.click(x1+158,y1+49)   
 

    pyautogui.press("enter")


#&&% 复制到剪贴板
def copy_to_clipboard(text: str):
    """
    将传入的 text 文本写入系统剪贴板，供后续右键→粘贴使用。
    
    """
    
    # 创建一个隐藏的 tk 根窗口
    r = tkinter.Tk()
    r.withdraw()  # 隐藏主窗口

    # 清空剪贴板并写入新的文本
    r.clipboard_clear()
    r.clipboard_append(text)
    # 必须 update() 一下，确保数据真正存到剪贴板
    r.update()

    # 销毁隐藏窗口
    r.destroy()

#&&% 写微信
def xieweixin(x1,y1,neirong):
        
        copy_to_clipboard(neirong)

        time.sleep(2)
   
        pyautogui.moveTo(x1+532,y1+151)

        time.sleep(2)
        activate_window_by_title("微信")

        
        pyautogui.moveTo(x1+532,y1+151)

        time.sleep(2)

        pyautogui.click(x1+532,y1+151)
      

        pyautogui.hotkey('ctrl', 'v')        

        pyautogui.click(x1+532,y1+151)
    
#&&% 主操作函数
def 主操作函数():
    restore_and_position(
        name = "微信",
        width_ratio = 0.5,
        height_ratio = 0.5,
        x = 0,
        y = 0
    )  
 
    time.sleep(1)


    x1,y1,_,_ = activate_window_by_title("微信")

    xuanqun(x1,y1,"华新工作群")

    time.sleep(3)

    x2,y2=click_and_find_image_shape(358, 594, r"D:/Myprogramsystem/XT/weixin_xiaolian.png", timeout = 10.0)

    time.sleep(5)

    pyautogui.click(x2,y2) 

    time.sleep(5)

    x3,y3=click_and_find_image_shape(358, 594, r"D:/Myprogramsystem/XT/weixin_daixao_biaoqingbao.png", timeout = 10.0)

    time.sleep(2)
    pyautogui.click(x3,y3) 
    time.sleep(2)


 
    xieweixin(x1,y1,"Hello!我是公司管理员小化身，从今天起将参与公司管理，与各位一起奋进！")

    fs(x1,y1)

    
    time.sleep(1)


#&&% 主函数入口
def  main_func(folder_path=r"D:/Myprogramsystem/BaiduSyncdisk/宋岳/工业园整理/三期/测试"):

    打印输出PDF() 



#&&% 录屏
def luping(main_func, *args, **kwargs):
    """
    1) 开始 OBS 录制  
    2) 最小化所有窗口；恢复并定位 OBS  
    3) 切换到 CAD 窗口，调用 main_func(*args, **kwargs）  
    4) 切换回 OBS，停止录制  

    main_func : 任意可调用对象  
    *args, **kwargs : 会原样传给 main_func  
    """
    # —— 最小化所有窗口 ——  
    minimize_all_windows_d()

    # —— 定位并激活 OBS ——  
    restore_and_position(name="OBS", width_ratio=0.5, height_ratio=0.5, x=0, y=0)
    time.sleep(1)

    # 点击 OBS “开始录制”  
    x0, y0, _, _ = activate_window_by_title("OBS")
    pyautogui.moveTo(x0 + 824, y0 + 328)
    time.sleep(0.2)
    pyautogui.click(x0 + 824, y0 + 328)

    # —— 切换到 CAD ——  
    minimize_all_windows_d()
    time.sleep(0.5)
    restore_and_position(name="AutoCAD", width_ratio=1.0, height_ratio=1.0, x=0, y=0)
    time.sleep(1)

    # —— 3️⃣ 执行主操作 ——  
    main_func(*args, **kwargs)
    print("主操作函数执行完毕")

    # —— 停止录制 ——  
    time.sleep(0.5)
    minimize_all_windows_d()
    restore_and_position(name="OBS", width_ratio=0.5, height_ratio=0.5, x=0, y=0)
    time.sleep(0.2)

    x4, y4, _, _ = activate_window_by_title("OBS")
    pyautogui.moveTo(x4 + 824, y4 + 328)
    time.sleep(0.2)
    pyautogui.click(x4 + 824, y4 + 328)

    print("录制已停止")


#&&% 魔方
def 魔方():

    import 魔方分析

    魔方分析.魔方控制台(r"D:/Myprogramsystem/BaiduSyncdisk/宋岳/自动化(动态)/魔方/分析")



#&&% 运行Python脚本
def run_py(pyname):
    try:
        # 运行指定的 Python 程序，隐藏命令行窗口
        result = subprocess.run(
            [sys.executable, pyname],
            check=True,
            text=True,
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        sys_logger.info(f"[OK] 程序 {pyname} 执行成功。输出:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        sys_logger.info(f"[错误] 运行 {pyname} 时发生错误: {e}")
        sys_logger.info(f"错误信息: {e.stderr}")
    except FileNotFoundError:
        sys_logger.info(f"[错误] 未找到程序 {pyname}。请检查文件名和路径。")


#&&% 聚焦命令行
def focus_cmdline(cmd_x, cmd_y, delay=0.2):
    """
    把鼠标移到命令行并单击，确保焦点回到 AutoCAD 命令栏。

    
    """
    pyautogui.moveTo(cmd_x, cmd_y, duration=delay)
    pyautogui.click()



#&&% 激活窗口和子窗口


def activate_window_by_title(title: str, click_titlebar: bool = True) -> bool:
    """
    激活一个指定标题的窗口。
    
    1. 用 pygetwindow 找到窗口对象；
    2. 如果窗口被最小化，先还原；
    3. 将窗口置为前台（优先使用 win.activate()，失败时用 ctypes 强制）；
    4. （可选）在标题栏中点击一次，确保焦点。
    
    :param title: 要激活的窗口标题（部分匹配）。
    :param click_titlebar: 是否模拟一次点击标题栏，以确保窗口获得焦点。
    :return: True=激活成功，False=未找到窗口。
    """
    USER32 = ctypes.windll.user32
    SW_RESTORE = 9


    # ① 查找标题包含关键字的窗口
    wins = [w for w in gw.getWindowsWithTitle(title) if title in w.title]
    if not wins:
        sys_logger.info(f"[错误] 未找到标题包含 “{title}” 的窗口")
        return False
    win = wins[0]

    # ② 如果最小化，先还原
    if win.isMinimized:
        win.restore()
        time.sleep(0.2)

    
    # ③ 置为前台：先尝试 pygetwindow.activate()
    try:
        win.activate()
        time.sleep(0.2)
    except Exception:
        # ctypes 强制还原并置前
        hwnd = win._hWnd
        USER32.ShowWindow(hwnd, SW_RESTORE)          # 还原
        USER32.SetForegroundWindow(hwnd)             # 置前
        time.sleep(0.2)

    # ④ 可选：在标题栏中点一下
    if click_titlebar:
        x = win.left + win.width // 2
        y = win.top + max(1, min(30, win.height // 10))
        pyautogui.click(x, y)
        time.sleep(0.1)

    sys_logger.info(f"[成功] 已激活窗口: {win.title} 位置({win.left},{win.top}) 大小{win.width}x{win.height}")

    return  win.left,win.top,win.width,win.height


#&&% 窗口内点击
def click_in_window(title: str, offset_x: float, offset_y: float, click_titlebar: bool = False) -> bool:
    """
    在指定窗口的某个相对像素位置点击一次（相对于窗口左上角的偏移量）。

    :param title:         窗口标题关键字（部分匹配）
    :param offset_x:      从窗口左上角算起的水平像素偏移量（0 表示左边缘，width 表示右边缘）
    :param offset_y:      从窗口左上角算起的垂直像素偏移量（0 表示顶边缘，height 表示底边缘）
    :param click_titlebar: 是否先在标题栏点击一次以确保窗口获取焦点
    :return:              True=点击成功，False=未找到窗口
    """
    # 1) 查找窗口
    wins = [w for w in gw.getWindowsWithTitle(title) if title in w.title]
    if not wins:
        sys_logger.info(f"[错误] 未找到标题包含 “{title}” 的窗口")
        return False
    win = wins[0]

    # 2) 如果最小化，就先还原
    if win.isMinimized:
        win.restore()
        time.sleep(0.2)

    # 3) 尝试激活
    try:
        win.activate()
        time.sleep(0.2)
    except Exception:
        # ctypes 强制还原并置前
        hwnd = win._hWnd
        SW_RESTORE = 9
        ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.2)

    # 4) 可选：点击标题栏让焦点真正到窗口
    if click_titlebar:
        tx = win.left + win.width // 2
        ty = win.top + 10  # 标题栏一般在窗口顶部 10px 左右
        pyautogui.click(tx, ty)
        time.sleep(0.1)

    # 5) 计算目标点的绝对屏幕坐标
    abs_x = int(win.left + offset_x)
    abs_y = int(win.top  + offset_y)

    # 6) 点击
    pyautogui.moveTo(abs_x, abs_y, duration=0.2)
    pyautogui.click(abs_x, abs_y)
    time.sleep(0.1)
    sys_logger.info(f"🔘 已在窗口 “{win.title}” 内部点击 ({offset_x}, {offset_y}) → 绝对 ({abs_x}, {abs_y})")
    return True

"""
click_in_window("图形导出", offset_x=600-10, offset_y=600-10, click_titlebar=True)

"""

#&&% 激活并点击艾可云
def activate_and_click_aikeyun():


    try:
    
        left, top, width, height = activate_window_by_title("艾可云", click_titlebar=True)
        
        # Calculate relative offsets from provided data
        rel_x1 = 887 - 682  # 205
        rel_y1 = 542 - 93   # 449
        
        # Move to first click position and left click
        pyautogui.moveTo(left + rel_x1, top + rel_y1)
        pyautogui.click(button='left')
        
        # Wait for 2 seconds
        time.sleep(2)
        
        # Calculate close position: using width - 22 for x, as it aligns with top-right close button
        rel_x2 = width - 22  # Equivalent to 400 - 22 = 378 in data
        rel_y2 = 18          # 111 - 93
        
        # Move to close position and left click
        pyautogui.moveTo(left + rel_x2, top + rel_y2)
        pyautogui.click(button='left')
    
    
    
    except:
    
        pass
    



#&&% 窗口内简单拖拽
def drag_in_window_simple(
    title: str,
    start: tuple[float,float],
    offset: tuple[float,float],
    duration: float = 0.3,
    button: str = 'left',
    absolute_start: bool = False
):
    """
    拖拽函数，支持相对或绝对起点：

    :param title: 窗口标题关键字
    :param start: 起点坐标，(x, y)；
                  如果 absolute_start==False，则当成“窗口内部”坐标
                  如果 absolute_start==True，则当成“屏幕”坐标
    :param offset: 拖拽向量 (dx, dy)
    :param duration: 拖动时长
    :param button: 'left' 或 'right'
    :param absolute_start: True 则 start 视为屏幕绝对坐标
    """
    left, top, w, h = activate_window_by_title(title)

    if absolute_start:
        x1, y1 = start
    else:
        x1 = left + start[0]
        y1 = top  + start[1]

    x2 = x1 + offset[0]
    y2 = y1 + offset[1]

    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown(button=button)
    pyautogui.moveTo(x2, y2, duration=duration)
    pyautogui.mouseUp(button=button)
    time.sleep(0.1)
    sys_logger.info(f"已在“{title}”窗口拖拽：起点{(x1,y1)} → 终点{(x2,y2)}")


"""
drag_in_window_simple(
    "图形导出",
    start=(10,10),
    offset=(100,50),
    absolute_start=False
)

"""


#&&% 纯窗口操作炸开区域内对象
def run_auto_explode_area(x1, y1, x2, y2, cmd_x, cmd_y, delay=2):

    """
    这是一个未使用pywin32API控制天正CAD的典型函数
    它炸开区域x1, y1, x2, y2的所有对象，不适合反复操作

    合理的处理方式还是配合视窗调整（发送z\na或e\n）先slect显性选择对象，再发送命令

    """
    
    script = Path(__file__).with_name('auto_EXPLODE.py')
    cmd = [
        sys.executable, str(script),
        f'--x1={x1}', f'--y1={y1}',
        f'--x2={x2}', f'--y2={y2}',
        f'--cmd_x={cmd_x}', f'--cmd_y={cmd_y}',
        f'--delay={delay}'
    ]
    # 隐藏子进程窗口
    flags = subprocess.CREATE_NO_WINDOW
    try:
        subprocess.run(cmd, check=True, creationflags=flags)
        print('▶ 子程序完成')
    except subprocess.CalledProcessError as e:
        print(f'[错误] 子程序退出码 {e.returncode}')


#&&% 列出所有窗口
def list_all_windows():
    # 获取所有可见的窗口
    windows = gw.getWindowsWithTitle('')
    
    if not windows:
        print("[错误] 没有找到任何可见窗口。")
    else:
        print("当前桌面上的所有窗口：")
        for win in windows:
            sys_logger.info(f"窗口标题: {win.title}, 窗口大小: {win.width}x{win.height}, 位置: ({win.left}, {win.top})")

##最小、最大化窗口
def minimize_window(window_keyword: str = 'OBS') -> bool:
    """
    通用：最小化第一个标题包含 window_keyword 的可见窗口。

    :param window_keyword: 要匹配的窗口标题关键字（子串匹配），默认 'OBS'
    :return: 如果成功最小化返回 True，否则返回 False
    """
    # 1) 找到所有匹配的可见窗口
    windows = [w for w in gw.getWindowsWithTitle(window_keyword) if w.visible]
    if not windows:
        print(f'❌ 未找到标题包含 "{window_keyword}" 的可见窗口')
        return False

    # 2) 取第一个并最小化
    win = windows[0]
    print(f'🔍 找到窗口: "{win.title}"，执行最小化')
    win.minimize()
    return True

def maximize_autocad_window(window_keyword: str = 'AutoCAD') -> bool:
    """
    强制最大化第一个标题包含 window_keyword 的可见窗口。
    优先尝试使用 win32gui，如不可用则退回 ctypes 调用 user32。
    """
    # 1) 找到目标窗口
    wins = [w for w in gw.getWindowsWithTitle(window_keyword) if w.visible]
    if not wins:
        sys_logger.info(f"❌ 未找到标题包含 “{window_keyword}” 的可见窗口")
        return False

    win = wins[0]
    hWnd = win._hWnd

    # 2) 先恢复（避免最小化状态），再最大化
    #    尝试使用 win32gui
    try:
        import win32gui, win32con
        win32gui.ShowWindow(hWnd, win32con.SW_RESTORE)
        time.sleep(0.1)
        win32gui.ShowWindow(hWnd, win32con.SW_MAXIMIZE)
    except ImportError:
        # 如果没有 pywin32，就退回 ctypes
        SW_RESTORE  = 9
        SW_MAXIMIZE = 3
        ctypes.windll.user32.ShowWindow(hWnd, SW_RESTORE)
        time.sleep(0.1)
        ctypes.windll.user32.ShowWindow(hWnd, SW_MAXIMIZE)

    time.sleep(0.2)  # 确保窗口完成最大化
    sys_logger.info(f"✅ 已将窗口 “{win.title}” 最大化")
    return True




# 天正墙中轴线显示与隐藏

#  该函数系列包括如下一些函数

"""
墙是否加粗边线，墙中线显示，墙中线隐藏是文件属性，因此我们用D:/Myprogramsystem/cad/xitongjicuwenjian/墙基线打开.dwg，

D:/Myprogramsystem/cad/xitongjicuwenjian/墙基线关闭.dwg，D:/Myprogramsystem/cad/xitongjicuwenjian/墙线加粗.dwg三个空文件来

控制文件和程序的运行。因为获取天正墙信息的函数依赖墙中线的显示，所以对不熟悉的文件进行处理时，就可以通过这几个基本文件实现确定

的控制，即我们预期要文件的墙中线显示出来，或者墙边线要加粗，不加粗，依赖实际的需要。




"""
#&&&% 文字样式

#&&% 设置单位精度
def set_dwg_units_precision():
    """
    设置当前 DWG 文件的单位及精度：
    - 长度单位：单位类型不变，仅设置精度为 0.00000000
    - 角度单位：单位类型不变，精度为 0.00000000
    """
    doc=C.doc

    try:
        vars = doc.GetVariable

        # 设置长度精度（LUPREC = 8 表示 8 位小数）
        doc.SetVariable("LUPREC", 8)

        # 设置角度精度（AUPREC = 8 表示 8 位小数）
        doc.SetVariable("AUPREC", 8)

        print("[OK] 已将长度和角度单位精度设置为 8 位小数 (0.00000000)")
    except Exception as e:
        sys_logger.info(f"[错误] 设置失败: {e}")


def jd():
    set_dwg_units_precision()



#&&% 列出标注样式
def list_dim_styles():
    """
    列出当前 DWG 文件中所有标注样式名称。
    """
    try:
        styles = doc.DimStyles
        names = [styles.Item(i).Name for i in range(styles.Count)]
        print("📐 当前标注样式列表：")
        for name in names:
            print(" -", name)
        return names
    except Exception as e:
        sys_logger.info(f"[错误] 获取标注样式失败：{e}")
        return []



#&&% 设置当前标注样式
def set_current_dimstyle_via_command(style_name="_TCH_ARCH"):
    """
    使用命令行方式设置当前标注样式，兼容天正。

    参数:
        style_name (str): 要设为当前标注样式的名称（如 "_TCH_ARCH"）
    """
    try:
        doc.SendCommand(f"-DIMSTYLE\nR\n{style_name}\n")
        sys_logger.info(f"[OK] 已尝试通过命令行设置标注样式为：{style_name}")
    except Exception as e:
        sys_logger.info(f"[错误] 命令行设置标注样式失败：{e}")


        
#&&% 设置当前文字样式
def set_current_text_style(style_name="Standard"):
    """
    设置当前文字样式（通过 COM 接口方式）。

    参数:
        style_name (str): 要设置为当前的文字样式名称
    """
    try:
        text_styles = doc.TextStyles
        style = text_styles.Item(style_name)  # 获取指定样式
        doc.ActiveTextStyle = style           # 设置为当前样式
        sys_logger.info(f"[OK] 当前文字样式已设置为：{style_name}")
    except Exception as e:
        sys_logger.info(f"[错误] 设置文字样式失败：{e}")


#&&% 获取字体样式
def huoqu_ziti_style():

    styles = {ts.Name for ts in doc.TextStyles}
    
    return styles




#&&% 设置字体样式

"""
1，可多次对某种样式设置再更新

2，对汉字字体设置，不存在要设大字体。可用字体在C:/Windows/Fonts查找，直接用汉字名，使用create_text_style命令

3， 可以单独设置shx字体，使用set_text_style_onlyshx(style_name="style01", font_file="gbenor.shx", big_font_file=None)

所造字体缺失大字体，对汉字会产生问号

4，如不是单独设置汉字字体，完整的字体设置应包括英文部分的设置和大字体设置，用于中文显示而且是shx字体

 

"""
#&&% 创建文字样式
def create_text_style(sty_name="style01", ziti="宋体"):
    """
    在当前 DWG 中创建（或更新）一个中文文字样式。
    

    :param sty_name: 样式名称，默认 "style01"
    :param ziti:     字体名称，AutoCAD 会在系统字体中查找，例如 "宋体"
    # acad.ActiveDocument.ActiveTextStyle.SetFont(Typeface, Bold, Italic, charSet, PitchandFamily)
    # Typeface 字体名称；
    # Bold 加粗，布尔值，False为不加粗字体；
    # Italic 倾斜，布尔值，False为倾斜字体；
    # CharSet 字体字符集，1为默认字符集；
    # PitchAndFamily 字节及笔画形式。

    ts = doc.TextStyles.Item("HIT_TxtStyle")对shx

    ts.fontFile = "bigfont.shx"



    """

    # 1️⃣ 确保样式存在
    styles = doc.TextStyles
    try:
        ts = styles.Item(sty_name)
        sys_logger.info(f"[警告] 样式 '{sty_name}' 已存在，正在更新其属性。")
    except Exception:
        ts = styles.Add(sty_name)
        sys_logger.info(f"[OK] 已创建文字样式 '{sty_name}'。")

    # 2️⃣ 设置字体
    try:
        acad.ActiveDocument.TextStyles.Item(sty_name).SetFont(ziti, False, False, 1, 0 or 0)
    except Exception:
        try:
            acad.ActiveDocument.TextStyles.Item(sty_name).SetFont(ziti, False, False, 1, 0 or 0)
        except Exception as e:
            sys_logger.info(f"[警告] 无法设置字体为 '{ziti}'：{e}")

    # 3️⃣ 置为当前

    acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item(sty_name)
    
    # 5️⃣ 通知用户
    sys_logger.info(f"[OK] 样式 '{sty_name}' 属性已更新")




#&&% 设置SHX文字样式
def set_text_style_onlyshx(style_name="style01", font_file="gbenor.shx", big_font_file=None):
    """
    C:/Program Files/Autodesk/AutoCAD 2021/Fonts查找可用shx字体    
    设置 AutoCAD 的文字样式：
    - font_file：英文字体（.shx 或 .ttf）
    - big_font_file：可选的大字体（如 gbcbig.txt），默认为 None 表示不设置，仅设置英文字体
    set_text_style_onlyshx(style_name="TEST_STYLE", font_file="gbxxx.shx", big_font_file=None)
    不成功消息可用于判定shx字体在不在左侧英文字体


    """
    try:
        import win32com.client

        acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
        doc = acad.ActiveDocument
        styles = doc.TextStyles

        # 查找或创建字体样式
        if style_name in [s.Name for s in styles]:
            text_style = styles.Item(style_name)
        else:
            text_style = styles.Add(style_name)

        text_style.FontFile = font_file

        # 只有传入合法的大字体路径才设置 BigFontFile，否则跳过设置
        if big_font_file and isinstance(big_font_file, str):
            text_style.BigFontFile = big_font_file

        sys_logger.info(f"字体样式 '{style_name}' 设置成功：英文字体 = {font_file}，大字体 = {big_font_file or '未设置'}")
        return True

    except Exception as e:
        sys_logger.info(f"设置字体样式失败：{e}")
        return False



#&&% 设置文字样式
def set_text_style(style_name="style01", font_file="gbenor.shx", big_font_file="gbcbig.shx"):
    """
    设置CAD中文字样式：英文shx文件 + 中文大字体文件
    """
    try:

        styles = doc.TextStyles

        # 判断是否已有该样式
        if style_name in [s.Name for s in styles]:
            text_style = styles.Item(style_name)
        else:
            text_style = styles.Add(style_name)

        # 设置字体和大字体
        text_style.FontFile = font_file
        text_style.BigFontFile = big_font_file

        sys_logger.info(f"字体样式 '{style_name}' 设置成功，英文字体: {font_file}, 中文大字体: {big_font_file}")
        return True

    except Exception as e:
        sys_logger.info(f"设置字体样式失败：{e}")
        return False

#&&% 列出可用shx非大字表 shx大字表 

"""

到CAD字体设置下拉菜单找

"""

##&&% 问号字体替换
"""
网友的ftst方案已经彻底解决此问题，我们需要的是备份好文件和进一步编制点击窗口的函数
我建议使用Standard样式的gbenor.shx和大字gbcbig.shx替换更安全
"""



#&&% 重命名冲突文字样式
def rename_conflicting_text_styles(file1_path: str,
                                   file2_path: str,
                                   suffix: str = "_1",
                                   retry_delay: float = 0.2,
                                   max_retries: int = 10):
    """
    在两个 DWG 中找出同名（用户）文字样式，
    并在第一个文件中将它们重命名（原名 + suffix）：
      1) 通过 -RENAME 命令重命名样式
      2) 确认样式表里旧名已消失、新名已出现
      3) REGEN 强制刷新
      4) 遍历 ModelSpace，将引用旧样式的实体指向新样式
      5) 保存并关闭
    系统默认样式会被自动跳过。
    """
    SYSTEM_STYLES = {"Standard", "ASHADE", "Annotative", "BigFont"}

    acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
    acad.Visible = True

    doc1 = acad.Documents.Open(os.path.abspath(file1_path))
    doc2 = acad.Documents.Open(os.path.abspath(file2_path))

    try:
        # 1) 收集两文件的样式
        styles1 = {ts.Name for ts in doc1.TextStyles}
        styles2 = {ts.Name for ts in doc2.TextStyles}
        conflicts = (styles1 & styles2) - SYSTEM_STYLES
        if not conflicts:
            print("[OK] 未发现需要重命名的用户样式。")
            return

        sys_logger.info(f"[警告] 发现同名用户样式：{conflicts}，将在 “{os.path.basename(file1_path)}” 中重命名：")
        ms = doc1.ModelSpace

        for old_name in conflicts:
            new_name = old_name + suffix
            # 如果新名也冲突，就多加后缀，直到独一
            while new_name in styles1:
                new_name += suffix

            # 2) 发送 RENAME 命令
            cmd = f"-RENAME\nStyle\n{old_name}\n{new_name}\n\n"
            doc1.SendCommand(cmd)
            # 等待命令被处理、样式表更新
            for attempt in range(max_retries):
                time.sleep(retry_delay)
                # 强制刷新图形状态
                doc1.SendCommand("REGEN\n")
                try:
                    # 如果旧名已不存在并且新名存在，就跳出重试
                    doc1.TextStyles.Item(new_name)
                    try:
                        doc1.TextStyles.Item(old_name)
                        # 旧名仍然存在，继续等
                        continue
                    except Exception:
                        # 旧名被正确移除
                        break
                except Exception:
                    # 新名还没出现，继续等
                    continue
            else:
                sys_logger.info(f"  ❗ 重命名 “{old_name}” → “{new_name}” 可能未生效（超时）。")

            # 3) 再把所有实体中引用旧样式的改成新样式
            for ent in ms:
                try:
                    ename = getattr(ent, "EntityName", "").upper()
                    oname = getattr(ent, "ObjectName", "")
                    # 原生 TEXT/MTEXT
                    if ename in ("TEXT", "MTEXT"):
                        if ent.TextStyle == old_name:
                            ent.TextStyle = new_name
                    # 天正文字
                    elif oname in ("TDbText", "TDbMText"):
                        if ent.TextStyle == old_name:
                            ent.TextStyle = new_name
                except Exception:
                    # 有些实体可能不允许改样式，忽略它们
                    pass

            # 更新本地样式集合
            styles1.discard(old_name)
            styles1.add(new_name)
            sys_logger.info(f"  · 样式 “{old_name}” → “{new_name}”")

        # 4) 最后保存并反馈
        doc1.Save()
        sys_logger.info(f"[OK] 已保存改动到 “{os.path.basename(file1_path)}”。")

    finally:
        # 关闭文档，不保存对第二个文件的任何改动
        doc1.Close(False)
        doc2.Close(False)

#&&&%CAD连接问题

"""

在 pywin32 (win32com) 操作 AutoCAD 的上下文中，Dispatch 和 EnsureDispatch 的核心区别在于 “后期绑定” (Late Binding) 与 “早期绑定” (Early Binding)，这直接影响到代码提示、运行速度以及常量 (Constants) 的使用。

以下是详细对比和 pywin32 中其他常见的 Dispatch 方式。

1. Dispatch vs. EnsureDispatch
win32com.client.Dispatch("AutoCAD.Application")
机制 (后期绑定):

这是最基础的连接方式。Python 在运行时才去询问 AutoCAD：“你有没有这个属性？你有没有这个方法？”

它不会生成 Python 包装文件（wrapper files）。

缺点:

无常量: 你无法使用 AutoCAD 的内置常量（如 acRed, acLine, acSelectionSetWindow）。你必须手动查找这些常量对应的整数值（例如用 1 代表红色）。

无代码提示: 在 IDE（如 PyCharm, VS Code）中，你基本上看不到任何自动补全，因为编辑器不知道返回的对象是什么。

速度稍慢: 每次调用都需要动态查询接口。

优点:

启动快（不需要生成中间文件）。

对版本不敏感（不需要重新生成缓存）。

win32com.client.EnsureDispatch("AutoCAD.Application")
机制 (早期绑定):

它会强制运行 makepy 过程。它会读取 AutoCAD 的类型库 (Type Library)，并在你的 Python site-packages/win32com/gen_py 目录下生成一套对应的 Python 源代码文件。

如果缓存文件已存在，它就直接加载；如果不存在，它会自动生成。

优点:

可以使用常量: 这是最大的优势。你可以直接使用 win32com.client.constants.acRed，而不需要查表找数字。

更好的类型支持: 某些特定的 COM 方法（涉及 ByRef 参数或复杂类型）在 Dispatch 下可能会报错，但在 EnsureDispatch 下能正常工作。

可能略快: 对于大量重复调用，因为它已经知道了方法的内存地址（Dispid），调用速度会略快。

缺点:

第一次运行会慢（因为要生成文件）。

如果 AutoCAD 升级了，可能需要手动删除 gen_py 缓存文件夹来强制重新生成。

直观对比示例
Python

import win32com.client

# --- 使用 Dispatch (后期绑定) ---
acad_late = win32com.client.Dispatch("AutoCAD.Application")
# 你必须知道 1 代表红色，0 代表 ByLayer
line = acad_late.ActiveDocument.ModelSpace.AddLine((0,0,0), (10,10,0))
line.Color = 1  # 必须写数字

# --- 使用 EnsureDispatch (早期绑定) ---
acad_early = win32com.client.EnsureDispatch("AutoCAD.Application")
# 现在可以使用常量了
from win32com.client import constants
line = acad_early.ActiveDocument.ModelSpace.AddLine((0,0,0), (10,10,0))
line.Color = constants.acRed  # 代码可读性大大增强
2. 总共有哪些 Dispatch 及其变体？
在 win32com.client 模块中，主要有以下几种获取 COM 对象的方式：

A. Dispatch
用途: 创建一个新的对象，或者连接到一个现有的对象（取决于该软件的 COM 实现，AutoCAD 通常是如果已打开则连接，未打开则新建）。

语法: win32com.client.Dispatch("ProgID")

B. EnsureDispatch (属于 gencache 模块)
用途: 强制生成类型库缓存（早期绑定），然后返回对象。

语法: win32com.client.EnsureDispatch("ProgID")

注意: win32com.client.gencache.EnsureDispatch 是其完整路径，client.EnsureDispatch 只是一个快捷方式。

C. DispatchEx
用途: 强制创建一个新的实例。

场景: 如果你已经打开了一个 AutoCAD 窗口，但你想在后台启动另一个完全独立的 AutoCAD 进程（不干扰前台操作），使用这个。

语法: win32com.client.DispatchEx("AutoCAD.Application")

区别: 普通的 Dispatch 会查看 Windows 的运行对象表 (ROT)，如果有现成的就拿来用；DispatchEx 忽略 ROT，直接让系统启动新进程。

D. GetActiveObject (及其重要)
用途: 仅连接到正在运行的实例。

场景: 如果 AutoCAD 没有打开，这个命令会直接报错 (com_error)。这通常用于脚本的开头，判断用户是否已经打开了软件。

语法: win32com.client.GetActiveObject("AutoCAD.Application")

E. CastTo (虽不是 Dispatch，但在 CAD 中必用)
用途: 类型转换（QueryInterface）。

场景: 当你通过选择集或遍历获得一个对象，它可能被泛型包装为 IAcadEntity。此时如果你想访问该对象特有的属性（例如动态块的 EffectiveName），直接访问可能报错。

语法: win32com.client.CastTo(obj, "IAcadBlockReference")

注意: 必须配合 EnsureDispatch 生成的库使用，因为它需要知道目标类型的定义。

3. AutoCAD 开发的最佳实践代码
为了兼顾稳定性和常量的使用，通常推荐的连接代码如下：

Python

import win32com.client
from win32com.client import constants
import sys

def connect_to_acad():
    try:
        # 1. 尝试连接已打开的 AutoCAD
        # 使用 gencache.EnsureDispatch 包装 GetActiveObject 以获得常量支持
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        
        # 这一步是为了确保 gen_py 缓存被加载，否则 GetActiveObject 拿到的可能还是后期绑定对象
        # 另一种方法是显式调用 gencache.EnsureModule(...)
        acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application") 
        
        print("已连接到正在运行的 AutoCAD 实例。")
        
    except Exception:
        try:
            # 2. 如果没打开，则启动新的实例
            acad = win32com.client.EnsureDispatch("AutoCAD.Application")
            acad.Visible = True # 默认可能不可见
            print("已启动新的 AutoCAD 实例。")
        except Exception as e:
            sys_logger.info(f"无法连接或启动 AutoCAD: {e}")
            return None

    return acad

acad_app = connect_to_acad()

# 测试常量是否可用
if acad_app:
    try:
        sys_logger.info(f"AutoCAD 红色常量值: {constants.acRed}") 
    except AttributeError:
        print("警告：常量未加载，可能是缓存问题。尝试删除 gen_py 文件夹。")
总结
简单脚本/不想生成缓存文件 → 用 Dispatch。

需要代码提示/需要使用 constants/复杂项目 → 用 EnsureDispatch。

需要强制多开后台进程 → 用 DispatchEx。

你是否遇到过 AttributeError: <unknown>.Name 这种错误？这通常就是因为使用了 Dispatch (后期绑定) 导致 Python 无法正确解析某些特定接口，切换到 EnsureDispatch 配合 CastTo 通常能解决。

"""

##将一个对象属性传给多个对象

#&&% 格式刷属性传递
def transfer_props_by_matchprop(entity, Ob, max_try=3, delay=0.4):

    CR = chr(13)

    def wait_idle(acad, dt=0.2, n=50):
        """轮询 IsQuiescent，最多 n 次，每次 dt 秒"""
        for _ in range(n):
            if acad.GetAcadState().IsQuiescent:
                return
            time.sleep(dt)

    def expand_rectangle(p1, p2, offset):
        return (p1[0]-offset, p1[1]-offset), (p2[0]+offset, p2[1]+offset)


    """
    把 entity 的属性批量复制到 Ob。若 Layer 未变化则重试，最多 3 次。
    """
    li()

    src_layer   = entity.Layer
    orig_layer  = Ob.Layer        # 复制前目标的图层

    # 目标包围盒窗口
    p1, p2 = Ob.GetBoundingBox()
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
    h = 0.1 * (abs(x1 - x2) + abs(y1 - y2)) / 2
    (wx1, wy1), (wx2, wy2) = expand_rectangle(p1, p2, h)

    match_cmd = (
        "_MATCHPROP" + CR +
        "P"          + CR +            # Previous 作为源
        "_W"         + CR +
        f"{wx1},{wy1}" + CR +
        f"{wx2},{wy2}" + CR + CR
    )

    for attempt in range(1, max_try + 1):
        try:
            # ——— 1. 设定源对象为 Previous ———
            try:
                highlight_entity_by_bbox(entity)
            except Exception as e:
                # 退而求其次：使用 LISP 通过 Handle 选择对象
                sys_logger.info(f"[FALLBACK] highlight_entity_by_bbox 失败，使用 Handle 选择: {e}")
                handle = com_retry(lambda: entity.Handle)
                # 使用 LISP 的 ssget 创建选择集并显示
                doc.SendCommand(f"(sssetfirst nil (ssget \"_X\" '((5 . \"{handle}\"))))\n")
                time.sleep(0.5)
            time.sleep(delay)

            # ——— 2. 发送 MATCHPROP ———
            doc.SendCommand(match_cmd)
            wait_idle(acad)

            # ——— 3. 判断是否成功 ———
            if Ob.Layer == src_layer:
                sys_logger.info(f"[OK] 第 {attempt} 次匹配成功，Layer 改为 {src_layer}")
                return True

            sys_logger.info(f"[WARN] 第 {attempt} 次后 Layer 未变，重试…")
            time.sleep(delay)

        except Exception as e:
            sys_logger.info(f"[ERR] 第 {attempt} 次匹配异常：{e}")

    sys_logger.info(f"[FAIL] 连续 {max_try} 次仍未把属性复制给目标")
    return False


#视图合理化控制
"""
acad.ActiveDocument.SendCommand("_-view"+chr(13)+"_swiso"+chr(13))#西南轴测
acad.ActiveDocument.SendCommand("_-view"+chr(13)+"_seiso"+chr(13))#东南轴测
acad.ActiveDocument.SendCommand(
    "_-view" + chr(13) +
    "_nwiso" + chr(13)
)#西北轴测
acad.ActiveDocument.SendCommand(
    "_-view" + chr(13) +
    "_neiso" + chr(13)
)#东北轴测
acad.ActiveDocument.SendCommand("_-view"+chr(13)+"_top"+chr(13))#俯视图
acad.ActiveDocument.SendCommand("_-view"+chr(13)+"_bottom"+chr(13))#仰视图
acad.ActiveDocument.SendCommand("_-view"+chr(13)+"_front"+chr(13))#前视图
acad.ActiveDocument.SendCommand("_-view"+chr(13)+"_Right"+chr(13))#右视图
acad.ActiveDocument.SendCommand("_-view"+chr(13)+"_Back"+chr(13))#后视图
acad.ActiveDocument.SendCommand("_-view"+chr(13)+"_Left"+chr(13))#左视图
acad.ActiveDocument.SendCommand("_vscurrent"+chr(13)+"_R"+chr(13))#真实视觉样式

##合理显示对象

acad.ActiveDocument.SendCommand(
    "_z" + chr(13) +
    "_e" + chr(13)
)

acad.ActiveDocument.SendCommand(
    "_zoom" + chr(13) +
    "s"     + chr(13) +
    "0.8xp" + chr(13)
)




"""
#&&% 双线程生成器

#&&% 双线程运行1
def run_dual_threads_1(f1,                     # 线程1 函数

                     f2,                     # 线程2 函数

                     f1_args=(), f1_kwargs=None,

                     f2_args=(), f2_kwargs=None,

                     timeout_sec=180):



    """
    通用“双线程-GUI”调度器

    - f1 必须负责触发一个阻塞性窗口（如 SendCommand、ShowModalDlg 等）。
    - f2 负责侦测并自动化处理该窗口，当处理完毕后通知 f1 继续或退出。
    - f1、f2 的函数签名都应以 (timeout_event, done_event, …) 开头：
    
      def f1(timeout_event, done_event, …):
          pythoncom.CoInitialize()
          try:
              # ……主体代码：例如触发打印对话框
              timeout_event.wait()    # 等待线程2通知或超时
          except Exception:
              # 打印日志或其他处理
          finally:
              pythoncom.CoUninitialize()
              done_event.set()        # 通知“双线程”总控：我结束了

      def f2(timeout_event, done_event, …):
          pythoncom.CoInitialize()
          try:
              # ……主体代码：例如等待“创建打印文件”对话框出现并点击“回车”键
          except Exception:
              # 打印日志或其他处理
          finally:
              pythoncom.CoUninitialize()
              timeout_event.set()    # 通知 f1 线程：窗口已处理完，可以结束等待
              done_event.set()       # 通知“双线程”总控：我结束了

    - 参数说明：
        f1, f2：传入上面那种签名的函数
        f1_args、f1_kwargs：给 f1 传递的位置参数和关键字参数
        f2_args、f2_kwargs：给 f2 传递的位置参数和关键字参数
        timeout_sec：最多等待多少秒，如果超过则报告超时并返回 False

    - 返回值：
        True  ：两个子线程在 time_limit 内都完成了
        False ：超时，至少一个线程没及时调用 done_event.set()
    """
    if f1_kwargs is None:
        f1_kwargs = {}
    if f2_kwargs is None:
        f2_kwargs = {}

    # ① 为线程 1、2 准备同一个事件对
    timeout_event = threading.Event()
    done_event    = threading.Event()

    # ② 启动“线程1”：负责弹出、阻塞窗口
    t1 = threading.Thread(
        target=f1,
        args=(timeout_event, done_event, *f1_args),
        kwargs=f1_kwargs,
        daemon=True
    )
    # ③ 启动“线程2”：负责侦测窗口并点击、关闭
    t2 = threading.Thread(
        target=f2,
        args=(timeout_event, done_event, *f2_args),
        kwargs=f2_kwargs,
        daemon=True
    )

    start_time = time.time()
    t1.start()
    t2.start()

    # ④ 等待线程1 在 timeout_sec 秒内结束
    t1.join(timeout=timeout_sec)
    
    t2.join(timeout=timeout_sec)
    
        
        

    # ⑥ 检查 done_event 是否已被 set()
    if not done_event.is_set():
        # 超时：由调度器负责给线程1 发送退出信号
        timeout_event.set()
        sys_logger.info(f"[警告] 双线程执行超过 {timeout_sec}s —— 已触发 timeout_event")
        return False
    else:
        print("[OK] 双线程任务在时限内完成")
        return True



#&&% 取消CAD选择
def cancel_cad_selection(attempts: int = 3, delay: float = 0.5) -> bool:

    for i in range(1, attempts + 1):
        try:
            highlight_entities_in_window(0, 0, 0, 0)
            sys_logger.info(f"[OK] 第{i}次尝试：cancel_cad_selection 成功")
            return True
        except Exception as e:
            sys_logger.info(f"[警告] 第{i}次尝试失败：{e}")
            if i < attempts:
                time.sleep(delay)
    print("[错误] 已重试多次，仍未能执行 cancel_cad_selection")
    return False



#&&&% 打印辅助

def close_wps_window_by_click(
    title_keyword: str = "WPS Office",
    offset_x: int = 22,    # 距窗口右边缘的像素
    offset_y: int = 19,    # 距窗口上边缘的像素
    pause_before: float = 0.2
) -> bool:
    """
    在标题包含 title_keyword 的窗口右上角点击一次（×），尝试关闭该窗口。
    如果没找到窗口，则返回 False 并跳过。
    """
    # 枚举可见窗口，匹配标题
    handles = []
    def _enum(hwnd, lst):
        if win32gui.IsWindowVisible(hwnd):
            txt = win32gui.GetWindowText(hwnd) or ""
            if title_keyword.lower() in txt.lower():
                lst.append(hwnd)
    win32gui.EnumWindows(_enum, handles)

    if not handles:
        node("ℹ️ 未找到标题含 ‘{}’ 的窗口，跳过关闭", title_keyword)
        return False

    hwnd = handles[0]
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    x = right - offset_x
    y = top   + offset_y

    time.sleep(pause_before)
    pyautogui.click(x, y)
    node("✅ 点击 '{}' 窗口(句柄 {}) 的关闭按钮坐标：({}, {})",
         title_keyword, hwnd, x, y)
    return True






#&&&% 测试辅助

#&&% 最小化窗口
def min_w():
    import ctypes
    
    VK_MENU = 0x12  # Alt键
    VK_TAB = 0x09   # Tab键
    VK_LWIN = 0x5B  # 左Win键
    VK_M = 0x4D     # M键
    KEYEVENTF_KEYUP = 0x2

    # 模拟Alt + Tab
    ctypes.windll.user32.keybd_event(VK_MENU, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_TAB, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_TAB, 0, KEYEVENTF_KEYUP, 0)
    ctypes.windll.user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)

    # 模拟Win + M
    ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_M, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_M, 0, KEYEVENTF_KEYUP, 0)
    ctypes.windll.user32.keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0)




#&&% 清除测试图层
def ql():#清除测试辅助图层上的对象

    ensure_layer("测试辅助")

    




    
#&&% 模型空间画点
def srhd(*args):#根据输入坐标在模型空间画点
    """
    在模型空间绘制点并标注序号，支持以下调用形式：
    - srhd((x1,y1,z1), (x2,y2,z2))   # 多个点元组
    - srhd([(x1,y1,z1), (x2,y2,z2)]) # 列表形式
    - srhd((x1,y1,z1))               # 单点
    """
    doc = acad.ActiveDocument
    ms = doc.ModelSpace
    layer_name = "测试辅助"

    # 创建图层（如果不存在）
    try:
        doc.Layers.Item(layer_name)
    except:
        doc.Layers.Add(layer_name)
        sys_logger.info(f"[OK] 已创建图层：{layer_name}")

    # 统一格式处理：允许单点、多个点、列表传入
    if len(args) == 1:
        if isinstance(args[0], (list, tuple)):
            if len(args[0]) == 3 and all(isinstance(i, (int, float)) for i in args[0]):
                points = [args[0]]
            else:
                points = args[0]
        else:
            print("[错误] 输入格式不正确")
            return
    else:
        points = args

    # 绘制点与编号
    for idx, P in enumerate(points, 1):
        try:
            pt = vtpnt(*P)
            point = ms.AddPoint(pt)
            point.Layer = layer_name

            text = ms.AddText(str(idx), pt, 10)
            text.Layer = layer_name
        except Exception as e:
            sys_logger.info(f"[错误] 添加点失败: {e}")

    return "[OK] 点与编号已绘制"



#&&% 图纸空间画点
def srhd_p(*args):#根据输入坐标在图纸空间画点
    """
    在图纸空间绘制点和编号，支持：
    - 多个坐标元组：srhd_p((x1,y1,z1), (x2,y2,z2))
    - 单个列表：srhd_p([(x1,y1,z1), (x2,y2,z2)])
    - 单个点：srhd_p((x1,y1,z1))
    """
    ps = doc.PaperSpace
    layer_name = "测试辅助"

    # 创建图层（如果不存在）
    try:
        doc.Layers.Item(layer_name)
    except:
        doc.Layers.Add(layer_name)
        sys_logger.info(f"[OK] 已创建图层：{layer_name}")

    # 判断参数结构
    if len(args) == 1:
        if isinstance(args[0], (list, tuple)):
            if len(args[0]) == 3 and all(isinstance(i, (int, float)) for i in args[0]):
                # 单个点元组
                points = [args[0]]
            else:
                # 列表形式
                points = args[0]
        else:
            print("[错误] 输入格式不正确")
            return
    else:
        # 多个点元组
        points = args

    for idx, P in enumerate(points, 1):
        try:
            pt = vtpnt(*P)
            point = ps.AddPoint(pt)
            point.Layer = layer_name

            text = ps.AddText(str(idx), pt, 10)
            text.Layer = layer_name
        except Exception as e:
            sys_logger.info(f"[错误] 添加点失败: {e}")

    return "[OK] 图纸空间中的点与编号已绘制"


#&&% COM点转数学点
def comtomath(LBcom):#将com点列表转为数学点列表

    LB_point=[]

    for i in range(0,len(LBcom)):

        point = LBcom[i].Coordinates

        LB_point.append(point)

    return LB_point        

def p():

    li()

    oblist= pmxz()
    LBpoint=comtomath(oblist)
    return print(LBpoint)




        

#&&% 隔远查看

#&&% 复制查看
def fuzhi_chakan(LBcom,K=1):#K为放大倍数

    LK=[]

    for xx in LBcom:

        try:

            copy_obj = xx.Copy()
    
            point1 = vtpnt(0,0,0)
    
            point2 = vtpnt(0,K*1000000,0)
    
            copy_obj.Move(point1,point2)


            LK.append(copy_obj)

        except Exception as e:

            sys_logger.info(f"[错误] 移动对象{xx.Handle}失败: {e}")               

    return LK



#&&% 测量文字长度
def celiang_wenzichangdu(TEXTCOM):

    text_copy = TEXTCOM.Copy()

    text_copy.Alignment = 2

    text_copy.TextAlignmentPoint =vtpnt(0,0,0)

    chang = abs(text_copy.InsertionPoint[0])

    text_copy.Delete()

    return chang

#测量新写文字长度

#&&% 写入并测量文字长度
def celiang_wenzichangdu_write(ZF,style="图签",height=270,scalefactor=0.8):

    #根据字符串按样式字高宽度因子写入cad后的测量长度

    text_obj = acad.ActiveDocument.ModelSpace.AddText(ZF, vtpnt(0,0,0), height)

    text_obj.StyleName = style

    text_obj.ScaleFactor =scalefactor #宽度因子

    chang = celiang_wenzichangdu(text_obj)

    text_obj.Delete()

    return chang




##清空文件夹
#&&% 清空文件夹
def qingkong_wenjianjia(FolderPath):

     #清空文件夹B
    folder_path_1 = FolderPath 

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path_1):
        
        file_pathx = os.path.join(folder_path_1, filename)
        
        # 确保它是一个文件而不是文件夹
        if os.path.isfile(file_pathx):
            
            os.remove(file_pathx)  # 删除文件

        sys_logger.info(f"{FolderPath}文件夹已清空")

#&&&% 包围盒工具

#&&% 返回对象外包盒的长，宽，横竖向，角点信息

#&&% 获取包围盒信息
def get_bbox_info(com_obj):
    """
    获取传入 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）的外包盒信息，
    并计算其长（length）、宽（width）以及横向或竖向（orientation）状态。

    参数：
      com_obj -- 任意支持 GetBoundingBox() 方法的 AutoCAD COM 对象

    返回：
      (length, width, orientation)
        length      -- 外包盒较长一边的长度（在 X/Y 平面上）
        width       -- 外包盒较短一边的长度（在 X/Y 平面上）
        orientation -- 字符串：
                         "horizontal" 表示 X 方向跨度 ≥ Y 方向跨度，
                         "vertical"   表示 Y 方向跨度 >  X 方向跨度
    如果对象不支持 GetBoundingBox，会抛出异常；也可根据需要自行捕获处理。
    """
 


   # 调用 GetBoundingBox 方法，返回两个点：minPt、maxPt
    # minPt、maxPt 都是 3 元素的 tuple 或 list，形如 (x, y, z)
    




    try:

        minPt, maxPt = com_obj.GetBoundingBox()

    except Exception as e:

        sys_logger.info(f"获取外包盒失败: {e}")               

        return None


    # 计算 X、Y 方向跨度
    dx = maxPt[0] - minPt[0]
    dy = maxPt[1] - minPt[1]

    # 将较大值定义为 length，较小值定义为 width
    length = max(dx, dy)
    width  = min(dx, dy)

    # 判断横向（X 跨度 ≥ Y 跨度）还是竖向（Y 跨度 > X 跨度）
    if dx >= dy:
        orientation = "horizontal"
    else:
        orientation = "vertical"

    return minPt, maxPt,length, width, orientation


#&&% 包围盒方向标志
def bbox_orientation_flag(com_obj):
    """
    判断任意 COM 对象的外包盒是竖向、横向还是正方形：
      - 如果 Y 方向跨度 > X 方向跨度，返回 1（竖向）
      - 否则（包括 X 方向跨度 >= Y 方向跨度），返回 0
        —— 即当外包盒为正方形（X 跨度 == Y 跨度）时，也返回 0

    参数：
      com_obj -- 支持 GetBoundingBox() 的 AutoCAD COM 对象

    返回：
      int -- 竖向返回 1，横向或正方形返回 0
    """
    # 获取外包盒的最小点和最大点
    min_pt, max_pt = com_obj.GetBoundingBox()
    # 计算 X、Y 方向跨度
    dx = abs(max_pt[0] - min_pt[0])
    dy = abs(max_pt[1] - min_pt[1])
    # 如果是竖向（dy > dx），返回 1；否则（横向或正方形）返回 0
    return 1 if dy > dx else 0

#&&% 获取多个对象的外包盒数据

def group_bbox_corners(com_objs, max_retry=3, delay=0.05):
    """
    【通用加强版】计算一组 COM 对象的整体外包盒，并按顺序返回四个角点。
    
    集成特性：
    1. 包含 safe_get_bbox 的重试与刷新逻辑，防止因单个对象 "Call Rejected" 导致失败。
    2. 自动过滤无法获取几何信息的对象（如空文字、未生成的实体）。
    3. 自动解包 COM 数据类型。

    参数：
        com_objs: 可迭代的 COM 对象列表
        max_retry: 单个对象获取失败时的重试次数
        delay: 重试间隔

    返回：
        四元组：(左下, 右上, 左上, 右下)
        每个点为 (x, y, z)。如果不含有效对象，返回 None。
    """
    import math
    import time
    from win32com.client import VARIANT

    # 初始化为极端值
    global_min_x = float('inf')
    global_min_y = float('inf')
    global_max_x = float('-inf')
    global_max_y = float('-inf')
    global_min_z = float('inf')
    
    valid_count = 0

    for obj in com_objs:
        if obj is None: continue

        # --- 单个对象的安全获取逻辑 (内嵌 safe_get_bbox 核心) ---
        p1, p2 = None, None
        
        for k in range(max_retry):
            try:
                # [关键] 强制刷新，防止新对象无几何数据
                obj.Update()
                
                # 获取包围盒
                min_var, max_var = obj.GetBoundingBox()
                
                # [清洗] 确保转为 list/tuple，防止 SafeArray 报错
                p1 = list(min_var) if hasattr(min_var, '__iter__') else min_var
                p2 = list(max_var) if hasattr(max_var, '__iter__') else max_var
                
                # 成功获取，跳出重试循环
                break 
            except Exception:
                # 遇到错误（如 CAD 忙），稍作休眠后重试
                if k < max_retry - 1:
                    time.sleep(delay)
                else:
                    # 彻底失败，p1 p2 保持为 None
                    pass
        
        # 如果该对象获取失败，跳过它，处理下一个
        if p1 is None or p2 is None:
            continue
        
        # --- 数据更新 ---
        valid_count += 1
        x1, y1, z1 = p1[0], p1[1], p1[2]
        x2, y2, z2 = p2[0], p2[1], p2[2]

        # 更新 X/Y/Z 极值
        if x1 < global_min_x: global_min_x = x1
        if y1 < global_min_y: global_min_y = y1
        if x2 > global_max_x: global_max_x = x2
        if y2 > global_max_y: global_max_y = y2
        
        # 统一使用所有对象中最低的 Z 值
        if z1 < global_min_z: global_min_z = z1

    # 结果校验：如果没有一个有效对象，返回 None
    if valid_count == 0:
        return None

    # 构造结果
    z = global_min_z
    
    # 1. 左下 (Min X, Min Y)
    bottom_left  = (global_min_x, global_min_y, z)
    # 2. 右上 (Max X, Max Y)
    top_right    = (global_max_x, global_max_y, z)
    # 3. 左上 (Min X, Max Y)
    top_left     = (global_min_x, global_max_y, z)
    # 4. 右下 (Max X, Min Y)
    bottom_right = (global_max_x, global_min_y, z)

    return bottom_left, top_right, top_left, bottom_right



#&&% zip的用法
"""
seq_x0  = (x0, y0, z0)
P_start = (dx, dy, dz)
要得到新坐标 (x0+dx, y0+dy, z0+dz)，就可以写：
seq_x0 = tuple(a + b for a, b in zip(seq_x0, P_start))
zip(seq_x0, P_start) 会产出 (x0, dx), (y0, dy), (z0, dz)
a + b for a, b in ... 就对每一对做相加
最后用 tuple(...) 把结果收成三元组
对两个列表求和
xs = [10, 20, 30]
ys = [1, 2, 3]
sums = [x + y for x, y in zip(xs, ys)]
# sums == [11, 22, 33]
并行遍历三组数据
names = ["A", "B", "C"]
ages  = [30, 25, 40]
scores= [85, 92, 78]
for n, a, s in zip(names, ages, scores):
    sys_logger.info(f"{n} 年龄{a} 分数{s}")
解压
如果有一个列表 pairs = [(1,4),(2,5),(3,6)]，要拆成两个列表：
a, b = zip(*pairs)
# a == (1,2,3), b == (4,5,6)

"""

#&&% 从两点绘制矩形


#&&% 包围盒中心2D
def bbox_center_2(e):
    # GetBoundingBox 返回两个 Point (minPt, maxPt)
    min_pt, max_pt = e.GetBoundingBox()
    x1, y1, _ = tuple(min_pt)
    x2, y2, _ = tuple(max_pt)
    return ((x1 + x2) / 2, (y1 + y2) / 2)

#&&% 包围盒中心3D
def bbox_center_3(ent):
    """返回实体外包盒中心 (cx, cy, cz)"""
    mn, mx = ent.GetBoundingBox()
    return ((mn[0] + mx[0]) / 2.0,
            (mn[1] + mx[1]) / 2.0,
            (mn[2] + mx[2]) / 2.0)

#&&% 安全获取包围盒
def safe_get_bbox(ent, max_retry=5, delay=0.05):
    """
    【通用加强版】安全获取 AutoCAD 图元外包盒 (GetBoundingBox)
    
    解决痛点：
    1. 新创建的对象（如 Text/Block）未计算几何数据导致的 "Empty Extents" (-2145386308)。
    2. AutoCAD 忙碌导致的 "Call Rejected" (-2147417846)。
    3. 偶发的通用 COM 错误。
    
    参数:
        ent: AutoCAD 图元对象 (IAcadEntity)
        max_retry: 最大重试次数 (默认5次)
        delay: 失败后的休眠秒数 (默认0.05秒)
        
    返回:
        (min_point, max_point) 元组，坐标为 (x, y, z)。
        如果彻底失败，返回 None。
    """


    # 如果对象本身就是空的，直接返回
    if ent is None:
        return None

    for i in range(max_retry):
        try:
            # [关键步骤] 强制刷新对象数据库
            # 这是解决 "刚创建的文字取不到包围盒" 的核心
            ent.Update()

            # 获取包围盒
            min_var, max_var = ent.GetBoundingBox()

            # [数据清洗] 确保拿到的是 Python 可用的数据
            # 有时 win32com 返回的是 tuple，有时是 SafeArray，这里做个转换保平安
            p1 = list(min_var) if hasattr(min_var, '__iter__') else min_var
            p2 = list(max_var) if hasattr(max_var, '__iter__') else max_var

            return p1, p2

        except com_error as e:
            hresult = e.args[0] if e.args else 0
            
            # 常见错误代码分析：
            # -2147417846: RPC_E_CALL_REJECTED (CAD 忙，例如正在自动保存或执行命令)
            # -2145386308: eInvalidExtents (对象无几何范围，常见于空文字或新对象)
            # -2147352567: 通用错误
            
            # 如果是最后一次尝试，或者错误严重，则记录日志（可选）
            if i == max_retry - 1:
                # sys_logger.info(f"[BBox最终失败] Handle={getattr(ent, 'Handle', 'Unknown')}, Err={hresult}")
                pass
            else:
                # 还有机会，休眠后重试
                time.sleep(delay)
                continue
                
        except Exception as e:
            # 捕获其他非 COM 错误（如 Python 逻辑错误）
            if i < max_retry - 1:
                time.sleep(delay)
                continue

    return None


#&&% dwg状态分析函数

def analyze_dwg_objects_status():
    """
    分析当前激活DWG文件中的对象状态

    功能：
        - 统计直线、多段线、圆、块实例的数量
        - 获取每个对象的Handle
        - 对于块实例，获取块名称

    Returns:
        dict: {
            'lines': {'count': int, 'handles': [str]},
            'polylines': {'count': int, 'handles': [str]},
            'circles': {'count': int, 'handles': [str]},
            'blocks': {'count': int, 'handles': [str], 'names': {handle: name}}
        }

    示例：
        >>> result = analyze_dwg_objects_status()
        >>> print(f"直线数量: {result['lines']['count']}")
        >>> print(f"第一条直线Handle: {result['lines']['handles'][0]}")
        >>> print(f"块实例: {result['blocks']['names']}")
    """
    from system.CAD_selection import ss_select

    sys_logger.info("=" * 60)
    sys_logger.info("开始分析DWG文件对象状态")
    sys_logger.info("=" * 60)

    result = {
        'lines': {'count': 0, 'handles': []},
        'polylines': {'count': 0, 'handles': []},
        'circles': {'count': 0, 'handles': []},
        'blocks': {'count': 0, 'handles': [], 'names': {}}
    }

    # ========== 1. 分析直线 ==========
    sys_logger.info("[1/4] 分析直线对象...")
    try:
        lines = ss_select(mode="all", filter_types=[0], filter_data=["LINE"])
        if lines:
            result['lines']['count'] = len(lines)
            result['lines']['handles'] = [obj.Handle for obj in lines]
            sys_logger.info(f"  ✓ 找到 {len(lines)} 条直线")
        else:
            sys_logger.info("  - 未找到直线对象")
    except Exception as e:
        sys_logger.error(f"  ✗ 分析直线失败: {e}")

    # ========== 2. 分析多段线 ==========
    sys_logger.info("[2/4] 分析多段线对象...")
    try:
        polylines = ss_select(mode="all", filter_types=[0], filter_data=["LWPOLYLINE"])
        if polylines:
            result['polylines']['count'] = len(polylines)
            result['polylines']['handles'] = [obj.Handle for obj in polylines]
            sys_logger.info(f"  ✓ 找到 {len(polylines)} 条多段线")
        else:
            sys_logger.info("  - 未找到多段线对象")
    except Exception as e:
        sys_logger.error(f"  ✗ 分析多段线失败: {e}")

    # ========== 3. 分析圆 ==========
    sys_logger.info("[3/4] 分析圆对象...")
    try:
        circles = ss_select(mode="all", filter_types=[0], filter_data=["CIRCLE"])
        if circles:
            result['circles']['count'] = len(circles)
            result['circles']['handles'] = [obj.Handle for obj in circles]
            sys_logger.info(f"  ✓ 找到 {len(circles)} 个圆")
        else:
            sys_logger.info("  - 未找到圆对象")
    except Exception as e:
        sys_logger.error(f"  ✗ 分析圆失败: {e}")

    # ========== 4. 分析块实例 ==========
    sys_logger.info("[4/4] 分析块实例...")
    try:
        blocks = ss_select(mode="all", filter_types=[0], filter_data=["INSERT"])
        if blocks:
            result['blocks']['count'] = len(blocks)
            result['blocks']['handles'] = [obj.Handle for obj in blocks]

            # 获取块名称
            for obj in blocks:
                try:
                    block_name = obj.Name
                    result['blocks']['names'][obj.Handle] = block_name
                except:
                    result['blocks']['names'][obj.Handle] = "Unknown"

            sys_logger.info(f"  ✓ 找到 {len(blocks)} 个块实例")

            # 统计块名称分布
            name_counts = {}
            for name in result['blocks']['names'].values():
                name_counts[name] = name_counts.get(name, 0) + 1

            sys_logger.info("  块名称分布:")
            for name, count in sorted(name_counts.items()):
                sys_logger.info(f"    - {name}: {count} 个")
        else:
            sys_logger.info("  - 未找到块实例")
    except Exception as e:
        sys_logger.error(f"  ✗ 分析块实例失败: {e}")

    # ========== 汇总 ==========
    sys_logger.info("=" * 60)
    sys_logger.info("分析完成 - 汇总:")
    sys_logger.info(f"  直线: {result['lines']['count']} 个")
    sys_logger.info(f"  多段线: {result['polylines']['count']} 个")
    sys_logger.info(f"  圆: {result['circles']['count']} 个")
    sys_logger.info(f"  块实例: {result['blocks']['count']} 个")
    sys_logger.info("=" * 60)

    return result




