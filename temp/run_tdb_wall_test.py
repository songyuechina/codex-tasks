import sys, importlib.util, traceback
from pathlib import Path

# Prepare paths
SCRIPTS = Path(r"D:/codex-tasks/cad/scripts")
MODULE_FILE = Path(r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/TDb_single_line_variable_wall/TDb_single_line_variable_wall.py")
DWG_FILE = Path(r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/TDb_single_line_variable_wall/TDb_single_line_variable_wall.dwg")
X1, Y1, X2, Y2 = 7233.482854925562, 21388.129735320166, 59410.111466570175, 52436.37163339066
WIDTH = 200

sys.path.insert(0, str(SCRIPTS))

from CAD_file_operations import close_all_dwg_paradigm, open_file
from CAD_basic import li, get_acad_doc

# dynamic import of the function module (folder name has space)
spec = importlib.util.spec_from_file_location("tdb_wall", MODULE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

try:
    print('[info] closing all DWGs')
    close_all_dwg_paradigm()
    print('[info] opening target DWG:', DWG_FILE)
    open_file(str(DWG_FILE))
    li(); get_acad_doc()
    print('[info] running TDb_single_line_variable_wall...')
    mod.TDb_single_line_variable_wall(X1, Y1, X2, Y2, width=WIDTH)
    print('[info] completed.')
except Exception as e:
    traceback.print_exc()
