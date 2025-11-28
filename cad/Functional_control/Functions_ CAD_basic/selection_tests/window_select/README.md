python window_select_demo.py window_select_demo.dwg --region 31910.5135 12035.4536 59141.3859 32002.4430

流程：cad_zt_oneb() → litz() → new_file(close_after=False) → 绘制圆+两条直线 → select_entities_in_window(...,'_W') 与 '_C' → save_file()+close_file('auto_save') → cad_zt_oneb() 复位。
运行记录写入 test_log.txt。
