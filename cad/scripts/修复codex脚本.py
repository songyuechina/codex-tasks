def fix_and_copy_newlines(source_filename, target_txt_filename):
    # 读取源文件内容
    with open(source_filename, 'r', encoding='utf-8', newline='') as file:
        content = file.read()
    
    # 替换文件中的换行符为 Windows 格式（\r\n）
    content = content.replace('\r\n', '\n').replace('\n', '\r\n')
    
    # 将修复后的内容写入新的 txt 文件（A）
    with open(target_txt_filename, 'w', encoding='utf-8', newline='') as file:
        file.write(content)

def create_py_file_from_txt(txt_filename, py_filename):
    # 读取 txt 文件内容
    with open(txt_filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # 在内容前添加 UTF-8 编码声明
    content = '# -*- coding: utf-8 -*-\n' + content

    # 将内容写入新的 .py 文件（B）
    with open(py_filename, 'w', encoding='utf-8') as file:
        file.write(content)

# 主函数，处理文件转换
def fix_and_convert(source_filename):
    # 文件 A 路径：先将源文件修复为 txt 格式
    target_txt_filename = source_filename + '_fixed.txt'
    fix_and_copy_newlines(source_filename, target_txt_filename)
    
    # 获取原文件的路径和文件名（去掉后缀 .py）
    base_name = source_filename.rsplit('.', 1)[0]  # 获取不含后缀的文件名
    
    # 为文件名添加 _fixed 后缀
    py_filename = base_name + '_fixed.py'  # 生成最终的 .py 文件名
    
    # 将修复后的 txt 文件转换为 .py 文件
    create_py_file_from_txt(target_txt_filename, py_filename)

    print(f"已修复并生成新的 Python 文件：{py_filename}")

# 输入文件路径
source_filename = 'D:/codex-tasks/cad/scripts/CAD_basic.py'
fix_and_convert(source_filename)
