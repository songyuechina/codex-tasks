from pathlib import Path
import sys

SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = next(parent for parent in SCRIPT_PATH.parents if parent.name.lower() == "cad")
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
for extra in (SYSTEM_DIR, SCRIPTS_DIR):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from CAD_file_operations import new_file, save_file, close_file, insert_file_as_block
from CAD_basic import li

FUNCTION_DIR = Path(__file__).resolve().parent
INSERT_ROOT = FUNCTION_DIR.parent
SHARED_SOURCE = INSERT_ROOT / "shared" / "source_template.dwg"
DEFAULT_SOURCE = FUNCTION_DIR / "source.dwg"
DEFAULT_TARGET = FUNCTION_DIR / "block_insert.dwg"


def resolve_path(raw: str) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (FUNCTION_DIR / path).resolve()
    return path


def ensure_default_source(path: Path):
    if path == DEFAULT_SOURCE and not DEFAULT_SOURCE.exists():
        DEFAULT_SOURCE.write_bytes(SHARED_SOURCE.read_bytes())


def parse_args():
    args = sys.argv[1:]
    if len(args) not in (2, 7):
        print("用法: python insert_block_as_block_demo.py <source_dwg> <target_dwg> "
              "[x y z scale rotation]")
        print("示例: python insert_block_as_block_demo.py source.dwg block_insert.dwg "
              "0 0 0 1.0 0")
        sys.exit(1)
    src = resolve_path(args[0])
    tgt = resolve_path(args[1])
    if len(args) == 2:
        params = (0.0, 0.0, 0.0, 1.0, 0.0)
    else:
        params = tuple(map(float, args[2:7]))
    return src, tgt, params


def main():
    source, target, (x, y, z, scale, rotation) = parse_args()
    ensure_default_source(source)
    new_file(str(target), close_after=False)
    li()
    insert_file_as_block(str(source), x=x, y=y, z=z, scale=scale, rotation=rotation)
    save_file()
    close_file("auto_save")


if __name__ == "__main__":
    main()
