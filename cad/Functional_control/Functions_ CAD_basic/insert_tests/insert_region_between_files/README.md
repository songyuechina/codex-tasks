python insert_between_demo.py source.dwg between_explode.dwg between_noexplode.dwg 0 0 1500 1500 4000 0

說明：
1. source.dwg 由 shared/source_template.dwg 複製，腳本會新建兩個目標 DWG 並分別以 explode True/False 插入同一窗口。
2. 參數含義：<x1 y1 x2 y2> 為窗口角點，<x3 y3> 為插入位置；示例值覆蓋 README 中的測試範例。
3. 腳本會在每次插入後自動 save_file() + close_file("auto_save")。
4. 若需重置，刪除 between_explode.dwg / between_noexplode.dwg 再重新執行命令。
5. 測試紀錄請寫入 ../test_log.txt。
