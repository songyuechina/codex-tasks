import sys, time
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import cad_zt_zero, cad_zt_oneb, open_file, save_file, close_file
from CAD_basic import li
from CAD_file_operations import draw_tarch_wall

TARGET = r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/File_basic_operation/C.dwg"
STEP_NAME = "Step5_draw_wall"

start = time.time()
TIMEOUT = 60

print(f"[STEP] {STEP_NAME}: cad_zt_zero()")
cad_zt_zero()

print(f"[STEP] {STEP_NAME}: cad_zt_oneb()")
cad_zt_oneb()

print(f"[STEP] {STEP_NAME}: open_file {TARGET}")
open_file(TARGET)
li()

print(f"[STEP] {STEP_NAME}: draw_tarch_wall")
draw_tarch_wall((1000,0,0), (1000,1000,0), thickness=240)

print(f"[STEP] {STEP_NAME}: save + close")
save_file()
close_file(save_option="prompt")

print(f"[STEP] {STEP_NAME}: final cad_zt_zero()")
cad_zt_zero()
print(f"[DONE] {STEP_NAME}")
