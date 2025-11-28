python open_file_demo.py ..\\new_file_draw_shapes\\shapes_demo_213859.dwg

脚本先 cad_zt_oneb() → litz()，再调用 open_file(target)；验证成功后 save_file()+close_file('auto_save') 清理环境，最后 cad_zt_oneb() 复位。
所有运行记录会追加到 test_log.txt。
