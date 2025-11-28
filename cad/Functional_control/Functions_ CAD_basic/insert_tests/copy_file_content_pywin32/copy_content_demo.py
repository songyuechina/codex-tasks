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

from CAD_file_operations import copy_file_content_pywin32
from CAD_basic import li

FUNCTION_DIR = Path(__file__).resolve().parent
INSERT_ROOT = FUNCTION_DIR.parent
SHARED_SOURCE = INSERT_ROOT / "shared" / "source_template.dwg"
SHARED_TARGET = INSERT_ROOT / "shared" / "target_template.dwg"
DEFAULT_SOURCE = FUNCTION_DIR / "source.dwg"
DEFAULT_TARGET = FUNCTION_DIR / "copy_target.dwg"


def ensure_default_samples(path: Path):
    if path == DEFAULT_SOURCE and not DEFAULT_SOURCE.exists():
        DEFAULT_SOURCE.write_bytes(SHARED_SOURCE.read_bytes())
    if path == DEFAULT_TARGET and not DEFAULT_TARGET.exists():
        # 使用目標模板初始化，便於觀察複製效果
        DEFAULT_TARGET.write_bytes(SHARED_TARGET.read_bytes())


def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print("用法: python copy_content_demo.py <source_dwg> <target_dwg>")
        print("示例: python copy_content_demo.py source.dwg copy_target.dwg")
        sys.exit(1)

    src_path = Path(args[0]).expanduser()
    dst_path = Path(args[1]).expanduser()
    if not src_path.is_absolute():
        src_path = (FUNCTION_DIR / src_path).resolve()
    else:
        src_path = src_path.resolve()
    if not dst_path.is_absolute():
        dst_path = (FUNCTION_DIR / dst_path).resolve()
    else:
        dst_path = dst_path.resolve()

    ensure_default_samples(src_path)
    ensure_default_samples(dst_path)

    if not src_path.exists():
        print(f"[错误] 源文件不存在: {src_path}")
        sys.exit(1)
    if not dst_path.exists():
        print(f"[错误] 目标文件不存在: {dst_path}，请先创建或指定已有 DWG。")
        sys.exit(1)

    li()
    print(f"[信息] 准备复制: {src_path} → {dst_path}")

    if copy_file_content_pywin32(str(src_path), str(dst_path)):
        print("[完成] copy_file_content_pywin32 复制成功")
    else:
        print("[警告] copy_file_content_pywin32 返回 False")


if __name__ == "__main__":
    main()
