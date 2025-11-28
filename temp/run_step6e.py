import sys
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import cad_zt_zero, cad_zt_oneb, new_file, save_file, close_file
from CAD_basic import li
from CAD_file_operations import draw_tarch_wall, insert_tarch_door

TARGET = r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/File_basic_operation/D.dwg"
INS_PT = (0, 0, 0)
HALF_LEN = 2500  # each side >2000

print('[STEP] Step6e: cad_zt_zero -> oneb')
cad_zt_zero()
cad_zt_oneb()
print('[STEP] Step6e: new_file overwrite D.dwg')
new_file(TARGET)
li()
print(f"[STEP] Step6e: draw wall from ({-HALF_LEN},0,0) to ({HALF_LEN},0,0)")
draw_tarch_wall((-HALF_LEN, 0, 0), (HALF_LEN, 0, 0), thickness=240)
print(f"[STEP] Step6e: insert door at {INS_PT}")
insert_tarch_door(INS_PT, width=200, height=3000)
print('[STEP] Step6e: save & close -> cad_zt_zero')
save_file()
close_file(save_option="prompt")
cad_zt_zero()
print('[DONE] Step6e complete')
