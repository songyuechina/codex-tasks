import sys
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import cad_zt_zero, cad_zt_oneb, open_file, save_file, close_file
from CAD_basic import li
from CAD_file_operations import draw_tarch_wall, insert_tarch_window

TARGET = r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/File_basic_operation/E.dwg"
print('[STEP] Step7: cad_zt_zero -> oneb -> open E')
cad_zt_zero()
cad_zt_oneb()
open_file(TARGET)
li()
print('[STEP] Step7: ensure wall (-2000,0,0)->(2000,0,0)')
draw_tarch_wall((-2000,0,0), (2000,0,0), thickness=240)
print('[STEP] Step7: insert_tarch_window at (0,0,0)')
insert_tarch_window((0,0,0), width=600, height=1000, window_type="jz-pingchuang", delete_mc_yuan=False)
print('[STEP] Step7: save/close + cad_zt_zero')
save_file()
close_file(save_option="prompt")
cad_zt_zero()
print('[DONE] Step7 complete')
