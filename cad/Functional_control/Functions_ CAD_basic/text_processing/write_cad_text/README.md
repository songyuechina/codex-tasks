python write_cad_text_demo.py --text 示例CAD文字 --x 0 --y 0 --height 350

脚本自动调用 text_processing/run_text_demo.py，流程：cad_zt_oneb() → litz() → new_file() → write_cad_text() → save/close → cad_zt_oneb()，运行记录写入 test_log.txt。
