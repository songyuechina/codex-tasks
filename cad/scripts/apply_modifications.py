#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本导航14版修改应用工具

此脚本会：
1. 备份原始文件
2. 读取原始脚本导航文件
3. 替换 run_in_idle 相关函数
4. 备份并替换 IDLE_bootstrap.py
5. 保存修改后的文件

使用方法：
    python apply_modifications.py
"""

import os
import shutil
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_SCRIPT = os.path.join(SCRIPT_DIR, "脚本导航14版.py")
NEW_FUNCTIONS_FILE = os.path.join(SCRIPT_DIR, "run_in_idle_new_version.py")
ORIGINAL_BOOTSTRAP = os.path.join(SCRIPT_DIR, "IDLE_bootstrap.py")
NEW_BOOTSTRAP = os.path.join(SCRIPT_DIR, "IDLE_bootstrap_new.py")

def create_backup(filepath):
    """创建文件备份"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.backup_{timestamp}"
    if os.path.exists(filepath):
        shutil.copy2(filepath, backup_path)
        print(f"✓ 已备份: {os.path.basename(backup_path)}")
        return backup_path
    return None

def read_file(filepath):
    """读取文件内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """写入文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def find_function_range(lines, function_name):
    """
    查找函数的起始和结束行号

    返回: (start_line, end_line) 或 None
    """
    start_line = None
    indent_level = None

    for i, line in enumerate(lines):
        # 查找函数定义
        if f"def {function_name}(" in line:
            start_line = i
            # 计算缩进级别
            indent_level = len(line) - len(line.lstrip())
            continue

        # 如果已找到函数开始，查找结束
        if start_line is not None:
            # 跳过空行和注释
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # 如果遇到同级别或更低级别的代码，说明函数结束
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= indent_level:
                return (start_line, i)

    # 如果到文件末尾还没找到结束，返回到文件末尾
    if start_line is not None:
        return (start_line, len(lines))

    return None

def apply_modifications():
    """应用修改"""
    print("="*60)
    print("脚本导航14版修改应用工具")
    print("="*60 + "\n")

    # 1. 检查文件是否存在
    if not os.path.exists(ORIGINAL_SCRIPT):
        print(f"✗ 错误: 找不到原始脚本: {ORIGINAL_SCRIPT}")
        return False

    if not os.path.exists(NEW_FUNCTIONS_FILE):
        print(f"✗ 错误: 找不到新函数文件: {NEW_FUNCTIONS_FILE}")
        return False

    # 2. 创建备份
    print("\n步骤 1: 备份原始文件")
    print("-" * 60)
    backup_script = create_backup(ORIGINAL_SCRIPT)
    if backup_script:
        print(f"  原始脚本备份于: {backup_script}")

    # 3. 读取文件
    print("\n步骤 2: 读取文件")
    print("-" * 60)
    original_content = read_file(ORIGINAL_SCRIPT)
    new_functions_content = read_file(NEW_FUNCTIONS_FILE)
    print(f"✓ 已读取原始脚本 ({len(original_content)} 字符)")
    print(f"✓ 已读取新函数 ({len(new_functions_content)} 字符)")

    # 4. 替换函数
    print("\n步骤 3: 替换 run_in_idle() 函数")
    print("-" * 60)

    original_lines = original_content.split('\n')

    # 查找 run_in_idle 函数的位置
    run_in_idle_range = find_function_range(original_lines, 'run_in_idle')

    if not run_in_idle_range:
        print("✗ 错误: 找不到 run_in_idle 函数")
        return False

    start, end = run_in_idle_range
    print(f"✓ 找到 run_in_idle 函数: 第 {start+1} 行到第 {end} 行")

    # 删除旧函数，插入新函数
    modified_lines = original_lines[:start] + [new_functions_content] + original_lines[end:]
    modified_content = '\n'.join(modified_lines)

    # 5. 写入修改后的文件
    print("\n步骤 4: 保存修改后的脚本")
    print("-" * 60)
    write_file(ORIGINAL_SCRIPT, modified_content)
    print(f"✓ 已保存修改后的脚本: {ORIGINAL_SCRIPT}")

    # 6. 替换 IDLE_bootstrap.py
    if os.path.exists(ORIGINAL_BOOTSTRAP) and os.path.exists(NEW_BOOTSTRAP):
        print("\n步骤 5: 替换 IDLE_bootstrap.py")
        print("-" * 60)
        backup_bootstrap = create_backup(ORIGINAL_BOOTSTRAP)
        if backup_bootstrap:
            print(f"  IDLE bootstrap 备份于: {backup_bootstrap}")

        shutil.copy2(NEW_BOOTSTRAP, ORIGINAL_BOOTSTRAP)
        print(f"✓ 已替换 IDLE_bootstrap.py")
    else:
        print("\n步骤 5: 跳过（IDLE_bootstrap 文件不存在）")

    print("\n" + "="*60)
    print("✓ 修改应用完成！")
    print("="*60)
    print("\n修改内容:")
    print("  1. ✓ 启动 IDLE 时不再弹出黑色 cmd 窗口")
    print("  2. ✓ 多次运行会复用同一个 IDLE 窗口")
    print("  3. ✓ 脚本中的函数会自动导入到 IDLE 环境")
    print("  4. ✓ 之前定义的变量会保留在内存中")
    print("\n使用说明:")
    print("  - 关闭当前运行的脚本导航程序（如果有）")
    print("  - 重新运行 '脚本导航14版.py'")
    print("  - 打开一个脚本，按 Ctrl+F5 运行")
    print("  - 在 IDLE 中可以直接使用脚本中的函数")
    print("\n备份文件位置:")
    print(f"  - {os.path.basename(backup_script)}")
    if 'backup_bootstrap' in locals():
        print(f"  - {os.path.basename(backup_bootstrap)}")
    print("\n如需恢复，将备份文件改名为原文件名即可。\n")

    return True

if __name__ == "__main__":
    try:
        success = apply_modifications()
        if not success:
            print("\n✗ 应用修改失败")
            input("\n按回车键退出...")
            exit(1)
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        exit(1)

    input("\n按回车键退出...")
