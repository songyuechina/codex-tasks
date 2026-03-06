# -*- coding: utf-8 -*-
import os
import sys

# 让 Python 能找到 D:/codex-tasks/cad
CAD_ROOT = r"D:/codex-tasks/cad"
if CAD_ROOT not in sys.path:
    sys.path.insert(0, CAD_ROOT)

# 关键：环境变量要有数据库密码
# 建议你在系统环境变量里永久配置 DATABASE_PASSWORD
# 临时也可以这样写：os.environ["DATABASE_PASSWORD"] = "你的密码"
# os.environ["DATABASE_PASSWORD"] = "xxxx"

from library import Databaseoperation as dbop

def sql_count_cad_basic():
    conn = dbop.connect_to_db("CAD_FUNCINFO")
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) 
        FROM function_analysis 
        WHERE file_path LIKE %s
    """, ("%CAD_basic.py%",))
    n = cur.fetchone()[0]
    cur.close()
    conn.close()
    print("COUNT =", n)

def sql_count_all():
    conn = dbop.connect_to_db("CAD_FUNCINFO")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM function_analysis")
    print("TOTAL =", cur.fetchone()[0])
    cur.close()
    conn.close()

if __name__ == "__main__":
    sql_count_all()
