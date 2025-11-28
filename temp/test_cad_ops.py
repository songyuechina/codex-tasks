import sys, time, os, traceback
from pathlib import Path
sys.path.insert(0, r'D:/codex-tasks/cad/scripts')
from CAD_file_operations import (
    new_file, open_file, close_current_dwg_paradigm, close_all_dwg_paradigm,
    save_current_dwg_paradigm, copy_file_with_increment,
    insert_dwg_as_block_paradigm, insert_and_explode_paradigm
)
from CAD_basic import li

START = time.time()
TIMEOUT = 60

def check_timeout():
    if time.time() - START > TIMEOUT:
        os.system('taskkill /F /IM acad.exe >nul 2>nul')
        raise TimeoutError(f'Exceeded {TIMEOUT}s, killed acad.exe')

def log(msg):
    print(f"[TEST] {msg}")

results = []
try:
    check_timeout(); log('Closing all DWGs (clean start)'); close_all_dwg_paradigm()
    out_path = Path(r'D:/codex-tasks/temp/test_spec_ops.dwg')
    log(f'Creating new file: {out_path}'); check_timeout(); new_file(str(out_path))
    log('Saving current DWG'); check_timeout(); save_current_dwg_paradigm()
    log('Closing current DWG'); check_timeout(); close_current_dwg_paradigm()
    log(f'Reopening file: {out_path}'); check_timeout(); open_file(str(out_path))
    log('li() connect to latest doc'); check_timeout(); li()
    log('Copying file with increment'); check_timeout(); copy_file_with_increment(str(out_path))
    copy_path = out_path.with_name(out_path.stem + '-1.dwg')
    if copy_path.exists():
        log(f'Inserting copy as block: {copy_path}'); check_timeout(); insert_dwg_as_block_paradigm(str(copy_path))
        log('Insert+explode copy'); check_timeout(); insert_and_explode_paradigm(str(copy_path))
    else:
        log('Copy not found, skipping insert tests')
    log('Closing all DWGs'); check_timeout(); close_all_dwg_paradigm()
    results.append('OK')
except Exception as e:
    traceback.print_exc()
    results.append(f'FAIL: {e}')

print('RESULT_SUMMARY:', results)
