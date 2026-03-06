import sys
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
