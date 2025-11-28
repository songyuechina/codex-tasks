python draw_shapes_demo.py shapes_demo_test.dwg

执行顺序：cad_zt_oneb() → litz() → new_file(close_after=False) → draw_shapes_helper 画点/线/圆/弧/椭圆/矩形/多段线/样条 → save_file()+close_file('auto_save') → cad_zt_oneb()。
输出 DWG 默认保存在当前文件夹，可通过命令行参数自定义文件名。
脚本运行记录写入 test_log.txt。
