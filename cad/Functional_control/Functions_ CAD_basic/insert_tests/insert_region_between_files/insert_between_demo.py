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

from CAD_file_operations import new_file, save_file, close_file, insert_region_between_files
from CAD_basic import li

FUNCTION_DIR = Path(__file__).resolve().parent
INSERT_ROOT = FUNCTION_DIR.parent
SHARED_SOURCE = INSERT_ROOT / "shared" / "source_template.dwg"
DEFAULT_SOURCE = FUNCTION_DIR / "source.dwg"
DEFAULT_EXPLODE = FUNCTION_DIR / "between_explode.dwg"
DEFAULT_KEEP = FUNCTION_DIR / "between_noexplode.dwg"


def resolve_path(raw: str) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (FUNCTION_DIR / path).resolve()
    return path


def ensure_default_source(path: Path):
    if path == DEFAULT_SOURCE and not DEFAULT_SOURCE.exists():
        DEFAULT_SOURCE.write_bytes(SHARED_SOURCE.read_bytes())


def run_case(source: Path, target: Path, region, target_point, explode_flag: bool):
    new_file(str(target), close_after=False)
    li()
    insert_region_between_files(str(source), str(target), *region, *target_point, explode=explode_flag)
    save_file()
    close_file("auto_save")


def parse_args():
    args = sys.argv[1:]
    if len(args) != 9:
        print("用法: python insert_between_demo.py <source_dwg> <explode_target_dwg> <keep_target_dwg> "
              "<x1> <y1> <x2> <y2> <x3> <y3>")
        print("示例: python insert_between_demo.py source.dwg between_explode.dwg between_noexplode.dwg "
              "0 0 1500 1500 4000 0")
        sys.exit(1)
    src = resolve_path(args[0])
    tgt_exp = resolve_path(args[1])
    tgt_keep = resolve_path(args[2])
    coords = list(map(float, args[3:]))
    region = tuple(coords[0:4])
    target_point = tuple(coords[4:6])
    return src, tgt_exp, tgt_keep, region, target_point


def main():
    source, target_exp, target_keep, region, target_point = parse_args()
    ensure_default_source(source)
    run_case(source, target_exp, region, target_point, True)
    run_case(source, target_keep, region, target_point, False)


if __name__ == "__main__":
    main()
