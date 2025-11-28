python new_file_demo.py new_file_demo.dwg

流程：cad_zt_oneb() → litz() → 调用 new_file(close_after=False) 生成新 DWG → save_file()+close_file('auto_save') 做善后 → cad_zt_oneb() 复位。
如未提供文件名，脚本自动以日分秒命名并存于本目录。
运行成功会把记录写入 test_log.txt，并确保桌面恢复到天正未保存 DWG 状态。
