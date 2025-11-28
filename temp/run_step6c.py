import sys
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import cad_zt_zero, cad_zt_oneb, new_file, save_file, close_file
from CAD_basic import li
from CAD_file_operations import draw_tarch_wall, insert_tarch_door

TARGET = r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/File_basic_operation/D.dwg"
print('[STEP] Step6c: cad_zt_zero -> oneb')
cad_zt_zero()
cad_zt_oneb()
print('[STEP] Step6c: new_file D.dwg (overwrite)')
new_file(TARGET)
li()
print('[STEP] Step6c: draw vertical wall through (0,0)')
draw_tarch_wall((0,-2000,0), (0,2000,0), thickness=240)
print('[STEP] Step6c: insert_tarch_door at (0,0,0) width200 height3000')
insert_tarch_door((0,0,0), width=200, height=3000)
print('[STEP] Step6c: save & close + cad_zt_zero')
save_file()
close_file(save_option="prompt")
cad_zt_zero()
print('[DONE] Step6c complete')
