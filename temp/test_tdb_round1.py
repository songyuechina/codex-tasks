import sys, shutil, importlib.util
from pathlib import Path
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import cad_zt_zero, cad_zt_oneb, open_file, save_file, close_file
from CAD_basic import li

MODULE_FILE = Path(r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/TDb_single_line_variable_wall/TDb_single_line_variable_wall.py")
spec = importlib.util.spec_from_file_location("tdb_module", MODULE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

X1, Y1, X2, Y2 = 7233.482854925562, 21388.129735320166, 59410.111466570175, 52436.37163339066
WIDTH = 200
src = MODULE_FILE.with_suffix('.dwg')
dst = src.with_name('TDb_single_line_variable_wall_round1.dwg')
if dst.exists():
    dst.unlink()
shutil.copy2(src, dst)

print('[Round1] cad_zt_zero -> oneb -> open copy')
cad_zt_zero()
cad_zt_oneb()
open_file(str(dst))
li()
print('[Round1] 调用 TDb_single_line_variable_wall...')
mod.TDb_single_line_variable_wall(X1, Y1, X2, Y2, width=WIDTH)
print('[Round1] 保存并关闭 copy')
save_file()
close_file(save_option="prompt")
cad_zt_zero()
print('[Round1] 完成')
