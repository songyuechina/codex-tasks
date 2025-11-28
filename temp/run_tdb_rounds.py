import sys, shutil, importlib.util, time
from pathlib import Path
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import cad_zt_zero, cad_zt_oneb, open_file, save_file, close_file
from CAD_basic import li

MODULE_FILE = Path(r"D:/codex-tasks/cad/Functional_control/Functions_ CAD_basic/TDb_single_line_variable_wall/TDb_single_line_variable_wall.py")
DWG_SRC = MODULE_FILE.with_suffix('.dwg')
spec = importlib.util.spec_from_file_location("tdb_module", MODULE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

COORDS = (7233.482854925562, 21388.129735320166, 59410.111466570175, 52436.37163339066)
WIDTH = 200

for idx in range(1, 4):
    copy_path = DWG_SRC.with_name(f"TDb_single_line_variable_wall_round{idx}.dwg")
    try:
        cad_zt_zero()
        if copy_path.exists():
            copy_path.unlink()
        shutil.copy2(DWG_SRC, copy_path)
        cad_zt_oneb()
        open_file(str(copy_path))
        li()
        print(f"[Round {idx}] running...")
        mod.TDb_single_line_variable_wall(*COORDS, width=WIDTH)
        save_file()
        close_file(save_option="prompt")
        print(f"[Round {idx}] success")
    except Exception as exc:
        print(f"[Round {idx}] ERROR: {exc}")
    finally:
        cad_zt_zero()
