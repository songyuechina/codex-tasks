from pathlib import Path
import sys

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = SCRIPT_PATH.parents[3]
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
for extra in (SYSTEM_DIR, SCRIPTS_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import (
    new_file,
    insert_file_as_block,
    insert_file_exploded,
)
from CAD_basic import li

BASE_DIR = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "insert_tests"
SOURCE = BASE_DIR / "insert_source.dwg"
TARGET_BLOCK = BASE_DIR / "block_insert.dwg"
TARGET_EXPLODED = BASE_DIR / "block_insert_exploded.dwg"


def ensure_source():
    if not SOURCE.exists():
        import create_base_dwgs  # type: ignore
        create_base_dwgs.draw_source()


def main():
    ensure_source()

    new_file(str(TARGET_BLOCK), close_after=False)
    li()
    insert_file_as_block(str(SOURCE), x=0, y=0, z=0, scale=1.0, rotation=0.0)

    new_file(str(TARGET_EXPLODED), close_after=False)
    li()
    insert_file_exploded(str(SOURCE), x=8000, y=0, z=0, scale=1.0)


if __name__ == "__main__":
    main()
