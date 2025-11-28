import sys
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import cad_zt_zero, cad_zt_oneb, new_file, open_file, save_file, close_file
from CAD_basic import li
from CAD_file_operations import draw_tarch_wall, insert_tarch_window

TARGET = r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/File_basic_operation/E.dwg"
INS_PT = (0, 0, 0)
HALF_LEN = 2500

print('[STEP] Step7b: cad_zt_zero -> oneb')
cad_zt_zero()
cad_zt_oneb()
print('[STEP] Step7b: new_file overwrite E.dwg')
new_file(TARGET)
li()
print(f"[STEP] Step7b: draw wall from ({-HALF_LEN},0,0) to ({HALF_LEN},0,0)")
draw_tarch_wall((-HALF_LEN, 0, 0), (HALF_LEN, 0, 0), thickness=240)
print(f"[STEP] Step7b: insert window at {INS_PT}")
insert_tarch_window(INS_PT, width=600, height=1000, window_type="jz-pingchuang", delete_mc_yuan=False)
print('[STEP] Step7b: save & close -> cad_zt_zero')
save_file()
close_file(save_option="prompt")
cad_zt_zero()
print('[DONE] Step7b complete')
