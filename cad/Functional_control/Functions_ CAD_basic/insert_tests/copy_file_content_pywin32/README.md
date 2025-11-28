python copy_content_demo.py source.dwg copy_target.dwg

說明：
1. 在本目錄內準備 source.dwg（內容模板）與 copy_target.dwg（目標模板），兩者可由 shared 模板複製。
2. 執行命令會先透過 li() 連接 CAD，再調用 copy_file_content_pywin32 將 source 內容複製到 target。
3. 測試完成後，如需恢復初始狀態，請刪除 copy_target.dwg 並從 insert_tests/shared/target_template.dwg 重新複製。
4. 所有 CLI 測試結果請追加到 ../test_log.txt。
