from pathlib import Path
import sys

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = next(parent for parent in SCRIPT_PATH.parents if parent.name.lower() == "cad")
SCRIPTS_DIR = CAD_DIR / "scripts"
SYSTEM_DIR = CAD_DIR / "system"

for extra in (SCRIPTS_DIR, SYSTEM_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import litz, cad_zt_oneb  # noqa: E402


def main():
    cad_zt_oneb()
    try:
        result = litz()
        print(f"litz result: {result}")
    finally:
        cad_zt_oneb()
        print("[litz_demo] 已回到 cad_zt_oneb 状态")


if __name__ == "__main__":
    main()
