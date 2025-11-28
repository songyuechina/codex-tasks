python insert_from_explode.py source.dwg fromfile_explode.dwg fromfile_keep.dwg 0 0 1500 1500 6000 0

說明：
1. source.dwg 由 shared/source_template.dwg 初始化；命令會創建 fromfile_explode.dwg 與 fromfile_keep.dwg 兩個目標檔。
2. 參數 <x1 y1 x2 y2> 控制窗口對角點，<x3 y3> 為在目標文件中的插入位置。
3. 每次插入後腳本會自動 save_file() + close_file("auto_save")，避免未保存對話框。
4. 重置方式：刪除 fromfile_explode.dwg / fromfile_keep.dwg，並視需要用 shared 模板覆蓋 source.dwg。
5. 測試紀錄寫入 ../test_log.txt。
