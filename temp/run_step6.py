import sys
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import cad_zt_zero, cad_zt_oneb, open_file, save_file, close_file
from CAD_basic import li
from CAD_file_operations import insert_tarch_door

TARGET = r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/File_basic_operation/D.dwg"
print('[STEP] Step6_insert_door: cad_zt_zero()')
cad_zt_zero()
print('[STEP] Step6_insert_door: cad_zt_oneb()')
cad_zt_oneb()
print('[STEP] Step6_insert_door: open_file')
open_file(TARGET)
li()
print('[STEP] Step6_insert_door: insert_tarch_door at (0,0,0)')
insert_tarch_door((0,0,0), width=200, height=3000)
print('[STEP] Step6_insert_door: save & close')
save_file()
close_file(save_option="prompt")
print('[STEP] Step6_insert_door: cad_zt_zero() final')
cad_zt_zero()
print('[DONE] Step6_insert_door complete')
