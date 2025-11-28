python insert_block_exploded_demo.py source.dwg block_insert_exploded.dwg 8000 0 0 1

說明：
1. source.dwg 從 shared/source_template.dwg 複製，命令會新建 block_insert_exploded.dwg 並以 explode 模式插入。
2. 參數依序代表 X、Y、Z、scale；若僅輸入檔案名則採用預設 0,0,0,1。
3. 腳本完成後會 save_file() + close_file("auto_save")，確保沒有未保存對話框。
4. 要回到初始狀態，刪除 block_insert_exploded.dwg 再重新執行命令。
5. 測試紀錄寫入 ../test_log.txt。
