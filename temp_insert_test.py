import sys
import traceback
from pathlib import Path
sys.path.insert(0, r"D:/codex-tasks/cad/scripts")
from CAD_file_operations import *  # noqa
from Print_illustration_label_catalogue import insert_and_scale_labels_area

try:
    print("Running cad_zt_oneb()...")
    cad_zt_oneb()
    print("Running litz()...")
    litz()
    file_path = r"D:/codex-tasks/cad/ziliao/图签测试0.dwg"
    print(f"Opening file: {file_path}")
    open_file(file_path)
    print("Reconnecting via li()...")
    li()
    print("Selecting entities on layer 'dy'...")
    lb = stc("dy")
    print(f"Layer 'dy' selection count: {len(lb)}")
    print("Calling insert_and_scale_labels_area...")
    res = insert_and_scale_labels_area(
        lb,
        filepath=r"D:/Myprogramsystem/XT/标准图签模板.dwg",
        layername="dy_quyu",
        timestamp=None,
        delpan=0,
    )
    print("insert_and_scale_labels_area finished.")
    if isinstance(res, dict):
        print(f"Result keys: {list(res.keys())[:5]}")
except Exception as exc:
    print("Test execution failed:")
    traceback.print_exc()
