from pathlib import Path
import sys

# ----- 动态挂载 CAD 模块路径，便于在 IDLE 中直接运行 -----
SCRIPT_PATH = Path(__file__).resolve()
CAD_DIR = SCRIPT_PATH.parents[3]
SYSTEM_DIR = CAD_DIR / "system"
SCRIPTS_DIR = CAD_DIR / "scripts"
for extra in (str(SYSTEM_DIR), str(SCRIPTS_DIR)):
    if extra not in sys.path:
        sys.path.insert(0, extra)

from CAD_basic import jingchengshu_wenjian, li, safe_delete_1, last_obj
from CAD_file_operations import (
    draw_tarch_wall,
    new_dwg_enhanced,
    close_file,
    cad_zt_zero,
    cad_zt_oneb,
)


def new_file(output_path=None, close_after=True):
    """Create a DWG file after verifying the current CAD/TArch context.

    Args:
        output_path (str | None): Target path; None keeps an unsaved blank file.
        close_after (bool): Close the newly created/opened file automatically when True.

    Returns:
        bool: True if the DWG was created or opened successfully.
    """

    def _close_new_file(result: bool) -> bool:
        """Close the active file when requested and ignore close errors."""
        if result and close_after:
            try:
                close_file("no_save")
            except Exception as exc:
                print(f"[警告] 关闭新建文件失败: {exc}")
        return result

    if output_path:
        target = Path(output_path)
        if target.exists():
            try:
                target.unlink()
                print(f"[信息] 已删除同名文件: {target}")
            except Exception as exc:
                print(f"[错误] 无法删除已存在文件 {target}: {exc}")
                return False

    shu_1 = jingchengshu_wenjian()
    tarch_ready = False

    if shu_1 == 1:
        print("[信息] 检测到 1 个 CAD 进程，进行天正墙自检...")
        wall_obj = None
        try:
            connected = li()
            if connected:
                try:
                    prev_obj = last_obj()
                    prev_handle = getattr(prev_obj, "Handle", None)
                except Exception:
                    prev_obj = None
                    prev_handle = None

                wall_created = draw_tarch_wall((0, 0, 0), (100, 0, 0), thickness=240)
                if wall_created:
                    try:
                        wall_obj = last_obj()
                        handle = getattr(wall_obj, "Handle", None)
                    except Exception:
                        wall_obj = None
                        handle = None

                    if handle and handle != prev_handle:
                        print(f"[成功] 天正墙自检通过 (Handle={handle})")
                        tarch_ready = True
                    elif handle == prev_handle and handle is not None:
                        print("[警告] last_obj 结果与自检前一致，可能未生成天正墙")
                    else:
                        print("[警告] 天正墙未返回 Handle，准备重新初始化 CAD")
                else:
                    print("[警告] 绘制天正墙失败，准备重新初始化 CAD")
            else:
                print("[警告] li() 连接失败，准备重新初始化 CAD")
        except Exception as exc:
            print(f"[警告] 天正墙自检异常: {exc}")
        finally:
            if wall_obj is not None:
                try:
                    safe_delete_1(wall_obj)
                except Exception:
                    try:
                        wall_obj.Delete()
                    except Exception:
                        pass

    if not tarch_ready:
        print("[信息] 执行 cad_zt_zero() + cad_zt_oneb() 重新准备天正环境...")
        cad_zt_zero()
        cad_zt_oneb()

    result = new_dwg_enhanced(output_path)
    return _close_new_file(result)


if __name__ == "__main__":
    from datetime import datetime

    demo_name = datetime.now().strftime("new_file_%d%M%S.dwg")
    demo_path = CAD_DIR / "Functional_control" / "Functions_ CAD_basic" / "File_basic_operation" / demo_name
    print(f">>> 示例：new_file(output_path='{demo_path}', close_after=False)")
    new_file(str(demo_path), close_after=False)
