python layer_select_demo.py layer_select_demo.dwg --layer 测试001

脚本流程：cad_zt_oneb() → litz() → new_file(close_after=False) → 绘制多段线/圆/直线并设置图层 → stc(layer) 统计 → save_file()+close_file('auto_save') → cad_zt_oneb()。
运行记录写入本目录 test_log.txt。
