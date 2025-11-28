import sys
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import cad_zt_zero, cad_zt_oneb, open_file, save_file, close_all_files, insert_region_from_file
from CAD_basic import li

print('[STEP] 4 redo) insert_region_from_file')
cad_zt_zero()
cad_zt_oneb()
open_file(r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/File_basic_operation/B.dwg")
li()
insert_region_from_file(r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/File_basic_operation/A.dwg",
                        16471.017909764152, -3155.7216948113564,
                        31532.684002152455, 7070.542193290901,
                        10000, 10000, explode=True)
save_file()
close_all_files()
cad_zt_zero()
print('[STEP] 4 completed')
