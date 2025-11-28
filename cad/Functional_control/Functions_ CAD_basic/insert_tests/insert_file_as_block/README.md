python insert_block_as_block_demo.py source.dwg block_insert.dwg 0 0 0 1 0

說明：
1. source.dwg 從 shared/source_template.dwg 複製，命令會建立 block_insert.dwg 並按給定參數插入整個 DWG 作為塊。
2. 參數順序為 X、Y、Z、scale、rotation；若省略則使用預設 0,0,0,1,0。
3. 腳本自動執行 save_file() 與 close_file("auto_save")，避免打斷 CAD 工作流。
4. 測試後刪除 block_insert.dwg 或以模板覆蓋即可重置。
5. 測試資訊請追加到 ../test_log.txt。
