python activate_document_demo.py activate_A_circle.dwg activate_C_rect.dwg activate_B_line.dwg

脚本流程：cad_zt_oneb() → litz() → (若无示例文件则新建) → 重新打开示例 DWG → 按命令行顺序调用 activate_document_by_name → 关闭这些 DWG → cad_zt_oneb() 复位。
命令行参数决定激活顺序，缺省为 A→B→C。运行记录写入 test_log.txt。
