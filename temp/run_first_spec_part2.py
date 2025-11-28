import sys, time
from pathlib import Path
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import (
    cad_zt_zero,
    cad_zt_oneb,
    open_file,
    save_file,
    close_file,
    close_all_files,
    copy_file_content_pywin32,
    insert_region_from_file
)
from CAD_basic import li
from CAD_basic import draw_circle
from CAD_file_operations import draw_tarch_wall, insert_tarch_door, insert_tarch_window

base_dir = Path(r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/File_basic_operation")
file_new = base_dir / 'new_file.dwg'
file_a = base_dir / 'A.dwg'
file_b = base_dir / 'B.dwg'
file_c = base_dir / 'C.dwg'
file_d = base_dir / 'D.dwg'
file_e = base_dir / 'E.dwg'

print('[STEP] 2) open_file + draw_circle')
cad_zt_zero()
cad_zt_oneb()
open_file(str(file_new))
li()
draw_circle((0,1000,0), 40000)
save_file()
close_file(save_option="prompt")
cad_zt_zero()

print('[STEP] 3) copy_file_content_pywin32 B->A')
cad_zt_oneb()
copy_file_content_pywin32(str(file_b), str(file_a))
save_file()
close_file(save_option="prompt")
cad_zt_zero()

print('[STEP] 4) insert_region_from_file B區域 -> A')
cad_zt_oneb()
open_file(str(file_b))
li()
insert_region_from_file(str(file_a), 16471.017909764152, -3155.7216948113564,
                        31532.684002152455, 7070.542193290901,
                        10000, 10000, explode=True)
save_file()
close_all_files()
cad_zt_zero()

print('[STEP] 5) draw_tarch_wall in C')
cad_zt_oneb()
open_file(str(file_c))
li()
draw_tarch_wall((1000,0,0), (1000,1000,0), thickness=240)
save_file()
close_file(save_option="prompt")
cad_zt_zero()

print('[STEP] 6) insert_tarch_door in D')
cad_zt_oneb()
open_file(str(file_d))
li()
insert_tarch_door((0,0,0), width=200, height=3000)
save_file()
close_file(save_option="prompt")
cad_zt_zero()

print('[STEP] 7) insert_tarch_window in E')
cad_zt_oneb()
open_file(str(file_e))
li()
insert_tarch_window((0,0,0), width=600, height=1000, window_type="jz-pingchuang", delete_mc_yuan=False)
save_file()
close_file(save_option="prompt")
cad_zt_zero()

print('[DONE] Steps 2-7 completed')
