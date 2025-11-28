python type_select_demo.py type_select_demo.dwg

流程：cad_zt_oneb() → litz() → new_file(close_after=False) 绘制文字/多段线/样条/椭圆/圆/直线 → 调用 select_text/mtext/... → save_file()+close_file('auto_save') → cad_zt_oneb()。
结果计数写入 test_log.txt。
