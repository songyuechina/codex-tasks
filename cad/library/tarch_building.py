#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天正建筑组件操作模块

提供天正墙体、门窗、房间等专业组件的操作函数
从 CAD_file_operations.py 拆分而来
"""
#D:/claude-tasks/cad/library/tarch_building.py

import sys
from pathlib import Path

# 路径引导
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

from system.project_setup import PathConfig
from system.licad import C
from system.CAD_com_utils import retry_on_busy, retry_if_busy, sys_logger, SafeCOM
from system.CAD_coordination import send_cmd_with_sync, wait_quiescent
import time
import subprocess


def dim_by_points(p1, p2, p3):
    """
    使用天正逐点标注命令对任意两点进行标注

    Args:
        p1: 起点坐标 (x, y, z)
        p2: 终点坐标 (x, y, z)
        p3: 标注位置点 (x, y, z)

    Returns:
        bool: 成功返回True
    """
    C.li()


    from CAD_basic import dim_by_points as _dim_by_points
    return _dim_by_points(p1, p2, p3)


#&&% 绘制天正墙
def draw_tarch_wall(p1, p2, thickness=240):
    """
    绘制天正墙体

    Args:
        p1: 起点坐标 (x, y, z)
        p2: 终点坐标 (x, y, z)
        thickness: 墙厚，默认240

    Returns:
        bool: 成功返回True
    """
    C.li()
    import sys, time
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import last_obj, set_object_property
    from system.CAD_coordination import send_cmd_with_sync, wait_quiescent

    try:
        # 发送天正墙命令
        cmd = f"tgwall\n{p1[0]},{p1[1]}\n{p2[0]},{p2[1]}\n\n\n"
        send_cmd_with_sync(cmd, wait_after=1.0)
        wait_quiescent(min_quiet=0.5, timeout=10.0)

        # 获取刚绘制的墙，增加重试机制
        time.sleep(1.5)

        for attempt in range(3):
            try:
                wall = last_obj()
                obj_name = wall.ObjectName

                # 检查是否是墙体对象
                if 'Wall' in obj_name or 'TDb' in obj_name:
                    # 设置墙厚
    
                    set_object_property(wall, "Thickness", thickness/2)
                    set_object_property(wall, "Thickness2", thickness/2)
    
                    print(f"[成功] 已绘制墙体，厚度{thickness}")
                    return True
                else:
                    print(f"[警告] 对象类型不是墙体: {obj_name}")
                    if attempt < 2:
                        time.sleep(0.5)
                        continue
                    return False

            except Exception as e:
                print(f"[警告] 第{attempt+1}次获取墙体对象失败: {e}")
                if attempt < 2:
                    time.sleep(0.5)
                    continue
                raise

        print(f"[警告] 未找到墙体对象")
        return False

    except Exception as e:
        print(f"[错误] 绘制墙体失败: {e}")
        return False

#&&% 插入天正门
def insert_tarch_door(p, width=None, height=None):
    """
    在墙体上插入天正门

    Args:
        p: 插入点坐标 (x, y, z)
        width: 门宽（可选，不指定则使用默认值）
        height: 门高（可选，不指定则使用默认值）

    Returns:
        dict: {'success': bool, 'door': 门对象, 'width': 实际宽度, 'height': 实际高度}
    """
    import sys
    import time
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import  get_acad_doc, get_object_property, set_object_property
    from system.CAD_coordination import send_cmd_with_sync, wait_quiescent

    
    try:
        doc = C.doc
        ms = doc.ModelSpace
        count_before = ms.Count

        # 发送TOpening命令插入门
        cmd = f"TOpening\n{p[0]},{p[1]}\n\n\n"
        send_cmd_with_sync(cmd, wait_after=1.0)
        wait_quiescent(min_quiet=0.5, timeout=15.0)

        door = None
        deadline = time.time() + 8.0
        while time.time() < deadline and door is None:
            time.sleep(0.5)
            count_after = ms.Count
            if count_after <= count_before:
                continue
            for idx in range(count_before, count_after):
                try:
                    obj = ms.Item(idx)
                    if getattr(obj, "ObjectName", "").lower() == "tdbopening":
                        door = obj
                        break
                except Exception:
                    continue
        if door is None:
            # 最后再全局搜索一次
            for idx in range(ms.Count - 1, -1, -1):
                try:
                    obj = ms.Item(idx)
                    if getattr(obj, "ObjectName", "").lower() == "tdbopening":
                        door = obj
                        break
                except Exception:
                    continue
        if door is None:
            from CAD_basic import last_obj
            for _ in range(3):
                try:
                    candidate = last_obj()
                    if getattr(candidate, "ObjectName", "").lower() == "tdbopening":
                        door = candidate
                        break
                except Exception:
                    pass
                time.sleep(0.4)

        if door is None:
            print("[错误] 未在模型空间中找到天正门对象")
            return {'success': False, 'door': None, 'width': None, 'height': None}

        # 读取当前尺寸
        current_width = get_object_property(door, 'Width')
        current_height = get_object_property(door, 'Height')

        # 设置尺寸（如果指定）
        if width is not None:
            set_object_property(door, 'Width', width)
            current_width = width

        if height is not None:
            set_object_property(door, 'Height', height)
            current_height = height

        print(f"[成功] 已插入天正门 - 宽度:{current_width}, 高度:{current_height}")

        return {
            'success': True,
            'door': door,
            'width': current_width,
            'height': current_height
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[错误] 插入门失败: {e}")
        return {'success': False, 'door': None, 'width': None, 'height': None}



#&&% 插入天正窗
def insert_tarch_window(p, width=600, height=1000, window_type="jz-pingchuang", delete_mc_yuan=False):
    """
    在墙体上插入天正窗

    Args:
        p: 插入点坐标 (x, y, z)
        width: 窗宽度，默认600
        height: 窗高度，默认1000
        window_type: 窗类型，默认"jz-pingchuang"，允许的类型:
            "jz-menlianchuang", "jz-dong", "jz-gaochuang", "jz-baiyechuang",
            "jz-tuchuang", "jz-pingchuang", "jz-zimumen", "jz-juanlianmen",
            "jz-tuilamen", "jz-shuangmen"
        delete_mc_yuan: 是否删除MC_yuan.dwg插入的对象，默认False不删除

    Returns:
        dict: {'success': bool, 'window': 窗对象, 'width': 宽度, 'height': 高度}
    """
    import time
    import logging
    from pathlib import Path as PathLib
    import sys
    sys.path.append(str(Path(__file__).parent))
    from CAD_basic import (
        get_object_property, set_object_property,
        transfer_props_by_matchprop
    )
    

    # 配置日志
    log_dir = LOGS_DIR
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"insert_tarch_window_{time.strftime('%Y%m%d_%H%M%S')}.log"

    # 配置日志处理器
    logger = logging.getLogger('insert_tarch_window')
    logger.setLevel(logging.INFO)
    # 清除已有的处理器
    if logger.handlers:
        logger.handlers.clear()
    # 添加文件处理器
    fh = logging.FileHandler(str(log_file), encoding='utf-8')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # 允许的窗类型列表
    allowed_types = [
        "jz-menlianchuang", "jz-dong", "jz-gaochuang", "jz-baiyechuang",
        "jz-tuchuang", "jz-pingchuang", "jz-zimumen", "jz-juanlianmen",
        "jz-tuilamen", "jz-shuangmen"
    ]
    C.li()
    # 1. 检查窗类型
    if window_type not in allowed_types:
        logger.error(f"窗类型错误: {window_type}, 允许的类型: {allowed_types}")
        print(f"[错误] 窗类型错误: {window_type}")
        return {'success': False, 'window': None, 'width': None, 'height': None}
    logger.info(f"窗类型检查通过: {window_type}")
    print(f"[信息] 窗类型检查通过: {window_type}")

    # 2. 连接当前激活文件
    C.li()
    logger.info("已连接当前激活文件")
    print("[信息] 已连接当前激活文件")

    # 3. 检查是否需要插入MC_yuan.dwg
    lb = stc('Mc_yuan_bj')
    if len(lb) == 0:
        logger.info("未找到Mc_yuan_bj图层，需要插入MC_yuan.dwg")
        print("[信息] 未找到Mc_yuan_bj图层，正在插入MC_yuan.dwg...")
        # 获取当前文件路径
        import win32com.client
        acad = cb.acad
        current_file = cb.doc.FullName
        logger.info(f"当前文件: {current_file}")
        copy_file_content_pywin32(str(XITONG_DIR / "MC_yuan.dwg"), current_file)
        logger.info("已插入MC_yuan.dwg")
        print("[成功] 已插入MC_yuan.dwg")
        # 重新连接
        C.li()
    else:
        logger.info(f"已存在Mc_yuan_bj图层，无需插入MC_yuan.dwg (找到{len(lb)}个对象)")
        print(f"[信息] 已存在Mc_yuan_bj图层 (找到{len(lb)}个对象)")

    # 4. 插入门
    print(f"[信息] 正在插入门... 位置:{p}, 宽度:{width}, 高度:{height}")
    result = insert_tarch_door(p, width=width, height=height)
    if not result['success']:
        logger.error("插入门失败")
        print("[错误] 插入门失败")
        return {'success': False, 'window': None, 'width': None, 'height': None}
    m1 = result['door']
    logger.info(f"已插入门，宽度:{width}, 高度:{height}")
    print(f"[成功] 已插入门，宽度:{width}, 高度:{height}")

    # 5. 选择窗类型图层的窗元并修改尺寸
    print(f"[信息] 正在选择窗类型图层: {window_type}")
    lc = stc(window_type)
    if len(lc) == 0:
        logger.error(f"未找到窗类型图层: {window_type}")
        print(f"[错误] 未找到窗类型图层: {window_type}")
        return {'success': False, 'window': None, 'width': None, 'height': None}

    window_src = lc[0]
    set_object_property(window_src, "Width", width)
    set_object_property(window_src, "Height", height)
    logger.info(f"已设置窗元尺寸: 宽{width}, 高{height}")
    print(f"[成功] 已设置窗元尺寸: 宽{width}, 高{height}")

    # 6. 使用transfer_props_by_matchprop匹配属性，最多5次
    print("[信息] 正在进行属性匹配...")
    success = False
    for attempt in range(1, 6):
        try:
            result_match = transfer_props_by_matchprop(window_src, m1, max_try=3, delay=0.4)
            if result_match:
                # 检查图层是否改变
                m1_layer = m1.Layer
                if m1_layer == window_type:
                    logger.info(f"第{attempt}次匹配成功，门已转换为窗，图层:{m1_layer}")
                    print(f"[成功] 第{attempt}次匹配成功，门已转换为窗，图层:{m1_layer}")
                    success = True
                    break
                else:
                    logger.warning(f"第{attempt}次匹配后图层不正确: {m1_layer}, 期望:{window_type}")
                    print(f"[警告] 第{attempt}次匹配后图层不正确: {m1_layer}, 期望:{window_type}")
        except Exception as e:
            logger.warning(f"第{attempt}次匹配失败: {e}")
            print(f"[警告] 第{attempt}次匹配失败: {e}")
        time.sleep(0.5)

    if not success:
        logger.error("transfer_props_by_matchprop匹配5次仍然失败")
        print("[错误] 属性匹配5次仍然失败")
        return {'success': False, 'window': None, 'width': None, 'height': None}

    # 7. 可选：删除MC_yuan对象
    if delete_mc_yuan:
        logger.info("正在删除MC_yuan对象...")
        print("[信息] 正在删除MC_yuan对象...")
        try:
            deleted_count = 0
            for obj in stc("MC_yuan_qiang"):
                try:
                    obj.Delete()
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"删除对象失败: {e}")
            for obj in stc("MC_yuan_bj"):
                try:
                    obj.Delete()
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"删除对象失败: {e}")
            logger.info(f"已删除 {deleted_count} 个MC_yuan对象")
            print(f"[成功] 已删除 {deleted_count} 个MC_yuan对象")
        except Exception as e:
            logger.warning(f"删除MC_yuan对象失败: {e}")
            print(f"[警告] 删除MC_yuan对象失败: {e}")

    logger.info(f"成功插入天正窗 - 位置:{p}, 宽度:{width}, 高度:{height}, 类型:{window_type}")
    print(f"[成功] 已插入天正窗 - 宽度:{width}, 高度:{height}, 类型:{window_type}")
    return {'success': True, 'window': m1, 'width': width, 'height': height}




#&&% 获取天正房间

def run_tupdspace_for_tz_room_in_rect(
    x1, y1, x2, y2,
    ty: float = 1.0,
    center_z: float = 0.0,
    insert_coord=None,
    require_tz_wall: bool = True,
):
    """
    在矩形 (x1,y1)-(x2,y2) 范围内：
      1. 调用 select_entities_in_window 让天正墙进入夹点编辑状态；
      2. 日志统计天正墙数量，并打印句柄等信息；
      3. 计算矩形中心 (仅日志用)；
      4. 计算 TUPDSPACE 插入点:
         - 若 insert_coord 为 None:
             水平方向取矩形中心，
             竖向在“矩形下边”外侧 4000，
             z = center_z
         - 若 insert_coord 为 (x,y,z)，则直接使用；
      5. 调用 run_auto_TUPDSPACE_with_coord(call_coord) 触发 TUPDSPACE。

    参数:
        x1, y1, x2, y2 : 矩形两个对角点世界坐标
        ty             : 传给 select_entities_in_window 的等待秒数
        center_z       : 用于默认插入点与矩形中心的 z 值
        insert_coord   : 可选，自定义插入点 (x,y,z)。
                         若为 None，则自动采用“下方 4000 + 水平居中”的默认点。
        require_tz_wall:
                         True  -> 若未检测到天正墙，则不调用 TUPDSPACE
                         False -> 不管有没有天正墙，都调用 TUPDSPACE

    返回:
        dict 示例：
        {
            "rect": ((x_lo, y_lo), (x_hi, y_hi)),
            "tz_wall_count": 13,
            "rect_center": (cx_center, cy_center, center_z),
            "call_coord": (cx, cy, cz),   # 真实传给 TUPDSPACE 的坐标
            "tupd_ok": True/False,
            "tupd_returncode": 0/其他
        }
        若因 require_tz_wall=True 且无天正墙而未调用 TUPDSPACE，则返回 None。
    """
    print("========== [TUPDSPACE_ROOM] run_tupdspace_for_tz_room_in_rect BEGIN ==========")
    print(f"[TUPDSPACE_ROOM] 输入矩形对角点: ({x1},{y1}) - ({x2},{y2})")
    C.li()

    # 1. 规范化矩形坐标
    (x_lo, y_lo), (x_hi, y_hi) = cb.normalize_rect(x1, y1, x2, y2)
    print(f"[TUPDSPACE_ROOM] 规范化矩形: 左下=({x_lo},{y_lo}), 右上=({x_hi},{y_hi})")

    # 2. 窗口选择 + 夹点编辑状态
    print("[TUPDSPACE_ROOM] 调用 select_entities_in_window 进行窗口选择 ...")
    try:
        com_list = cb.select_entities_in_window(x_lo, y_lo, x_hi, y_hi, ty=ty, select_mode="_W")
    except Exception as e:
        print("[TUPDSPACE_ROOM] ❌ 调用 select_entities_in_window 发生异常：", repr(e))
        print("========== [TUPDSPACE_ROOM] run_tupdspace_for_tz_room_in_rect END(ERROR_SELECT) ==========")
        return None

    print(f"[TUPDSPACE_ROOM] select_entities_in_window 返回实体数 = {len(com_list)}")

    # 3. 统计天正墙数量（ObjectName='TDbWall', Layer='WALL'），仅日志
    tz_walls = []
    for ent in com_list:
        try:
            oname = getattr(ent, "ObjectName", "")
            layer = getattr(ent, "Layer", "")
        except Exception:
            continue

        if oname == "TDbWall" and layer.upper() == "WALL":
            tz_walls.append(ent)

    print(f"[TUPDSPACE_ROOM] 其中天正墙 (ObjectName='TDbWall', Layer='WALL') 数量 = {len(tz_walls)}")

    handles = []
    for ent in tz_walls:
        try:
            h = ent.Handle
        except Exception:
            h = "<no_handle>"
        handles.append(h)
    print(f"[TUPDSPACE_ROOM] 天正墙句柄列表: {handles}")

    if require_tz_wall and not tz_walls:
        print("[TUPDSPACE_ROOM] ⚠ 未检测到天正墙，按 require_tz_wall=True 设定，不调用 TUPDSPACE。")
        print("========== [TUPDSPACE_ROOM] run_tupdspace_for_tz_room_in_rect END(NO_WALL) ==========")
        return None

    # 4. 计算矩形中心（仅用于日志参考）
    cx_center = (x_lo + x_hi) / 2.0
    cy_center = (y_lo + y_hi) / 2.0
    rect_center = (cx_center, cy_center, center_z)
    print(f"[TUPDSPACE_ROOM] 矩形中心(仅日志参考): {rect_center}")

    # 5. 决定真正传给 TUPDSPACE 的插入点 call_coord
    if insert_coord is None:
        # “下方 4000 + 水平居中”
        # 这里“最下边”按数值更小的 y_lo 理解；若你图上坐标系是反的，
        # 这一句可以改成用 y_hi + 4000。
        x_mid = cx_center
        bottom_y = y_lo           # 认为 y_lo 是“下边界”
        y_ins = bottom_y - 4000.0 # 再往下 4000
        z_ins = center_z
        call_coord = (x_mid, y_ins, z_ins)
        dy = y_ins - bottom_y
        print(f"[TUPDSPACE_ROOM] insert_coord 未提供，计算默认插入点: {call_coord}")
        print(f"[TUPDSPACE_ROOM] 默认插入点相对于最下边(y_lo={bottom_y})的偏移量 dy = {dy} (期望为 -4000.0)")
    else:
        if not (isinstance(insert_coord, (list, tuple)) and len(insert_coord) == 3):
            raise ValueError("insert_coord 必须是长度为 3 的 (x,y,z) 元组或列表")
        call_coord = tuple(insert_coord)
        print(f"[TUPDSPACE_ROOM] 使用调用方提供的 insert_coord 作为插入点: {call_coord}")

    # 6. 调用子程序，驱动 TUPDSPACE
    print("[TUPDSPACE_ROOM] 调用 run_auto_TUPDSPACE_with_coord() ...")
    tupd_result = run_auto_TUPDSPACE_with_coord(call_coord)
    print(
        f"[TUPDSPACE_ROOM] run_auto_TUPDSPACE_with_coord() 返回: "
        f"ok={tupd_result.get('ok')}, "
        f"returncode={tupd_result.get('returncode')}"
    )

    print("========== [TUPDSPACE_ROOM] run_tupdspace_for_tz_room_in_rect END ==========")

    return {
        "rect": ((x_lo, y_lo), (x_hi, y_hi)),
        "tz_wall_count": len(tz_walls),
        "rect_center": rect_center,
        "call_coord": call_coord,
        "tupd_ok": tupd_result.get("ok"),
        "tupd_returncode": tupd_result.get("returncode"),
    }
def run_auto_TUPDSPACE_with_coord(coord, script_path=None):
    """
    调用 auto_TUPDSPACE.py 子程序，传入坐标，并等待其执行完成（无黑框弹出）。
    增强版：详细打印子进程的 returncode / stdout / stderr，方便定位问题。

    参数:
        coord      : 三元组坐标 (x, y, z)
        script_path: auto_TUPDSPACE.py 的路径。
                     - 若为 None，则使用 "auto_TUPDSPACE.py"，即保持你原来相对路径行为，
                       让 Python 在当前工作目录下去找。

    返回:
        result: dict，例如
        {
            "ok": True/False,
            "returncode": 0 或其他,
            "stdout": "...",
            "stderr": "...",
            "cmd": [...],
            "cwd": "..."
        }
    """
    import os
    import subprocess
    import traceback

    result_info = {
        "ok": False,
        "returncode": None,
        "stdout": "",
        "stderr": "",
        "cmd": None,
        "cwd": None,
    }


    try:
        # 校验 coord 格式
        if not isinstance(coord, (tuple, list)) or len(coord) != 3:
            raise ValueError(f"坐标必须是一个包含三个数值的元组或列表，当前为: {coord!r}")

        x1, y1, z1 = coord
        coord_str = f"{x1},{y1},{z1}"

        # 保持你原来用相对路径的习惯：默认就是 "auto_TUPDSPACE.py"
        if script_path is None:
            script_path = "auto_TUPDSPACE.py"
        else:
            # 如果你以后想传绝对路径，也会在日志里打印出来
            script_path = os.path.abspath(script_path)

        cmd = [
            sys.executable,   # 当前 Python 解释器 (可能是 pythonw.exe)
            script_path,
            "--coord", coord_str
        ]

        result_info["cmd"] = cmd
        result_info["cwd"] = os.getcwd()

        print("========== [AUTO_TUPDSPACE] BEGIN ==========")
        print(f"[AUTO_TUPDSPACE] Python 可执行文件: {sys.executable}")
        print(f"[AUTO_TUPDSPACE] 当前工作目录 os.getcwd(): {os.getcwd()}")
        print(f"[AUTO_TUPDSPACE] auto_TUPDSPACE.py 路径参数: {script_path}")
        print(f"[AUTO_TUPDSPACE] 传入坐标参数: {coord_str}")
        print(f"[AUTO_TUPDSPACE] 最终命令行: {cmd}")

        creationflags = 0
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            creationflags = subprocess.CREATE_NO_WINDOW

        # 与你原来的行为尽量接近：不指定 cwd，由当前工作目录决定脚本位置
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=creationflags
        )

        result_info["returncode"] = proc.returncode
        result_info["stdout"] = proc.stdout or ""
        result_info["stderr"] = proc.stderr or ""

        print(f"[AUTO_TUPDSPACE] 子进程返回码 returncode = {proc.returncode}")
        if proc.stdout:
            print("----- [AUTO_TUPDSPACE] 子进程 STDOUT -----")
            print(proc.stdout)
            print("----- [AUTO_TUPDSPACE] END STDOUT -----")
        else:
            print("[AUTO_TUPDSPACE] 子进程 STDOUT 为空。")

        if proc.stderr:
            print("----- [AUTO_TUPDSPACE] 子进程 STDERR -----")
            print(proc.stderr)
            print("----- [AUTO_TUPDSPACE] END STDERR -----")
        else:
            print("[AUTO_TUPDSPACE] 子进程 STDERR 为空。")

        if proc.returncode == 0:
            result_info["ok"] = True
            print(f"✅ [AUTO_TUPDSPACE] 子程序成功完成：{coord_str}")
        else:
            print(f"❌ [AUTO_TUPDSPACE] 子程序返回非零状态码: {proc.returncode}")

        print("========== [AUTO_TUPDSPACE] END ==========")

    except Exception as e:
        print("❌ [AUTO_TUPDSPACE] 调用过程中发生异常（Python 主进程异常）:")
        print(repr(e))
        traceback.print_exc()

    return result_info

#&&% 单线变墙



def TDb_single_line_variable_wall(x1: float, y1: float, x2: float, y2: float, width: float = 240.0) -> bool:
    """
    单线变墙函数：将区域内的线段转换为天正墙体

    注意：此函数不使用 tlinebk 命令（会导致COM阻塞），
    而是直接读取线段端点并绘制天正墙体。

    Args:
        x1, y1: 区域左下角坐标
        x2, y2: 区域右上角坐标
        width: 墙体厚度，默认240

    Returns:
        bool: 成功返回True
    """
    from system.CAD_coordination import wait_quiescent

    from CAD_basic import (
        lines_daduan, get_acad_doc,
        set_object_property, normalize_rect, 
    )
    import CAD_basic as CAD_basic_module
    



    C.li()


    # 检查区域内是否有线段
    objs = select_objects_in_window_area(x1, y1, x2, y2)
    lines = [o for o in objs if getattr(o, "ObjectName", "") == "AcDbLine"]

    if not lines:
        print("[warn] 区域内没有线段，无需转换")
        return True  # 没有线段也算成功

    print(f"[info] 检测到 {len(lines)} 条线段")

    # 直接将线段转换为墙体（不使用tlinebk打断命令，避免COM阻塞）
    print(f"[stage] 直接转换线段为墙体 (thickness={width})")

    success = 0
    failed = 0

    for ln in lines:
        try:
            p1 = ln.StartPoint
            p2 = ln.EndPoint
            print(f"[info] 转换线段: {p1} -> {p2}")

            # 绘制天正墙
            result = draw_tarch_wall(p1, p2, thickness=width)
            if result:
                # 删除原线段
                try:
                    ln.Delete()
                except Exception as del_e:
                    print(f"[warn] 删除线段失败: {del_e}")
                success += 1
                print(f"[ok] 线段转换成功")
            else:
                failed += 1
                print(f"[warn] 线段转换失败")

            # 每次绘制后等待
            time.sleep(0.5)

        except Exception as exc:
            print(f"[warn] 转换失败: {exc}")
            failed += 1

    # 等待CAD完成
    try:
        wait_quiescent(min_quiet=0.5, timeout=10.0)
    except Exception:
        pass

    print(f"[done] 线段总数={len(lines)}, 成功={success}, 失败={failed}")
    return failed == 0




def convert_lines_to_walls(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    temp_width: float = 40.0,
    final_width: float = 240.0,  # Add final_width to pass for final thickness
) -> tuple[int, int, int]:
    """Convert lines to thin walls; return (detected_lines, success_walls, failed_walls)."""
    from system.CAD_coordination import wait_quiescent

    # 增加重试机制连接CAD
    max_retries = 5
    for attempt in range(max_retries):
        try:
            C.li()
            
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"[info] CAD连接失败，第{attempt+1}次重试... ({e})")
                time.sleep(1.0)
            else:
                print(f"[error] CAD连接失败: {e}")
                raise

    objs = select_objects_in_window_area(x1, y1, x2, y2)
    lines = [o for o in objs if getattr(o, "ObjectName", "") == "AcDbLine"]
    points = sum(1 for o in objs if getattr(o, "ObjectName", "").lower() == "acdbpoint")
    if points:
        print(f"[info] skipped {points} point objects")
    if not lines:
        print("[warn] no lines found after selection")
        return 0, 0, 0

    print(f"[info] lines to convert: {len(lines)}")
    success = failed = 0
    for ln in lines:
        try:
            p1 = ln.StartPoint
            p2 = ln.EndPoint
            draw_tarch_wall(p1, p2, thickness=temp_width)  # temp_width used for creating the temp walls
            ln.Delete()
            success += 1
            print(f"[ok] line {p1}->{p2} -> temp wall thickness {temp_width}")
        except Exception as exc:
            print(f"[warn] convert failed: {exc}")
            failed += 1
    
    # After temporary walls are drawn, set the final thickness to all walls
    print("[stage] set walls to final thickness after conversion")
    set_walls_thickness(x1, y1, x2, y2, width=final_width)

    return len(lines), success, failed



def set_walls_thickness(x1: float, y1: float, x2: float, y2: float, width: float) -> int:
    """Adjust all TDbWall objects in window to desired thickness. Return count."""
    C.li()
    objs = select_objects_in_window_area(x1, y1, x2, y2)
    count = 0
    for obj in objs:
        if getattr(obj, "ObjectName", "") == "TDbWall":
            try:
                set_object_property(obj, "Thickness", width/2)
                set_object_property(obj, "Thickness2", width/2)
                count += 1
            except Exception as exc:
                print(f"[warn] set thickness failed: {exc}")
    print(f"[info] walls set to thickness {width}: {count}")
    return count




#&&&&%% （四）  天正窗口

import time
import win32gui
import win32con
import pyautogui
from system.licad import C
import math
import json
import os


#&&&% 基本函数

def activate_cad_middle_click(hwnd):
    """【纯物理激活】中键点击"""
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        try: win32gui.SetForegroundWindow(hwnd)
        except: pass
        
        rect = win32gui.GetWindowRect(hwnd)
        cx = (rect[0] + rect[2]) // 2
        cy = (rect[1] + rect[3]) // 2
        
        pyautogui.moveTo(cx, cy)
        pyautogui.click(button='middle')
        time.sleep(0.1)
        return True
    except:
        return False

def insert_tarch_window_lisp_mode(wall_p1, wall_p2, cmd_name="TOpening"):
    """
    【函数编号】: TARCH-LISP-V20 (稳健等待版)
    【逻辑】: 
        1. 启动命令。
        2. 循环检测弹窗，直到它出现。
        3. 弹窗出现后，强制等待 3 秒 (不操作)。
        4. 激活 CAD，输入坐标，回车。
        D:/Mypro/基础服务/用户1/备份/插入天正门基本函数测试文件.dwg

        insert_tarch_window_lisp_mode(
            (178121.97856076437, 311217.5889781468, 0.0),
            (178274.28073210327, 311347.21940900886, 0.0),
            cmd_name="TOpening")        

    """
    mid_x = (wall_p1[0] + wall_p2[0]) / 2
    mid_y = (wall_p1[1] + wall_p2[1]) / 2
    
    # 1. 找句柄
    cad_hwnd = C.acad.HWND
    if not cad_hwnd: cad_hwnd = win32gui.FindWindow("AfxMDIFrame140u", None)
    print(f"🚀 [V20] 锁定 CAD: {cad_hwnd}")

    # 2. 启动命令
    activate_cad_middle_click(cad_hwnd)
    pyautogui.press('esc', presses=2, interval=0.1) 
    
    print(f"  -> 敲入命令: {cmd_name}")
    pyautogui.write(f'(command "{cmd_name}")\n', interval=0.05)
    
    # 3. 【关键步骤】死等弹窗出现
    possible_titles = ["门", "窗", "门窗", "天正图库管理系统", "门窗参数", "门窗设置"]
    hwnd_panel = 0
    
    print("  -> 正在侦测弹窗 (最长等 5 秒)...")
    for i in range(50): # 5秒
        for title in possible_titles:
            h = win32gui.FindWindow(None, title)
            if h and win32gui.IsWindowVisible(h):
                hwnd_panel = h
                print(f"  -> ✅ 弹窗已就位: {title}")
                break
        if hwnd_panel: break
        time.sleep(0.1)
    
    if not hwnd_panel:
        print("⚠️ 警告: 未检测到弹窗 (可能已打开或被遮挡)，继续尝试...")
    
    # 4. 【核心要求】强制冷却 3 秒
    # 此时弹窗刚出来，界面可能还在闪烁，焦点可能在跳动
    # 我们什么都不做，静静地等 3 秒
    print("  -> ❄️ 强制冷却 3 秒 (确保界面稳定)...")
    time.sleep(3.0)

    # 5. 激活窗口准备输坐标
    # 此时弹窗已经稳稳地悬浮在那里了，CAD 命令行也在闪烁等待输入了
    print("  -> 激活窗口 (中键)...")
    activate_cad_middle_click(cad_hwnd) 
    
    # 6. 输入坐标
    coord_str = f"{mid_x:.2f},{mid_y:.2f}"
    print(f"  -> 🎯 敲击坐标: {coord_str}")
    
    # 稳稳地输入
    pyautogui.write(coord_str, interval=0.1)
    
    # 7. 确认
    time.sleep(0.5)
    pyautogui.press('enter')
    
    # 8. 结束命令
    time.sleep(1.0)
    print("  -> 结束命令")
    pyautogui.press('esc') 
    
    print("✅ 完成。")
    return True

#&&&% 门类函数



# =============================================================================
# 模块：天正门窗自动化 (带示教缓存 & 多用户支持)
# =============================================================================

# 全局内存缓存
_TARCH_UI_CACHE = {}

def _get_dynamic_cache_path():
    """
    【核心配置】动态获取当前用户的缓存文件路径
    逻辑: 读取环境变量 USERPATH -> 拼接 Config 目录 -> 拼接文件名
    """
    # 1. 获取环境变量 (例如: D:\Mypro\基础服务\用户1)
    user_root = os.environ.get('USERPATH')

    # 2. 防呆保底: 如果没配置环境变量，默认存到当前脚本所在的目录下
    if not user_root:
        user_root = os.path.dirname(os.path.abspath(__file__))
    
    # 3. 构造完整路径
    return os.path.join(user_root, "Config", "tarch_ui_data.json")

def _load_cache_from_disk():
    """[内部] 从硬盘加载缓存到内存"""
    global _TARCH_UI_CACHE
    json_path = _get_dynamic_cache_path()
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                _TARCH_UI_CACHE = json.load(f)
    except Exception as e:
        print(f"⚠️ [系统] 读取缓存失败: {e}")
        _TARCH_UI_CACHE = {}

def _save_cache_to_disk():
    """[内部] 将内存缓存保存到硬盘"""
    json_path = _get_dynamic_cache_path()
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        # 写入文件
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(_TARCH_UI_CACHE, f, indent=4, ensure_ascii=False)
        print(f"💾 [系统] 配置已保存至: {json_path}")
    except Exception as e:
        print(f"❌ [系统] 保存缓存失败: {e}")

# 模块初始化时尝试加载一次
_load_cache_from_disk()

# -----------------------------------------------------------------------------
# 辅助函数
# -----------------------------------------------------------------------------

def _activate_cad_safe(hwnd):
    """
    【物理激活】鼠标移至窗口中心点击中键
    """
    try:
        if win32gui.IsIconic(hwnd): win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        try: win32gui.SetForegroundWindow(hwnd)
        except: pass
        
        rect = win32gui.GetWindowRect(hwnd)
        cx, cy = (rect[0]+rect[2])//2, (rect[1]+rect[3])//2
        
        pyautogui.moveTo(cx, cy)
        pyautogui.click(button='middle')
        time.sleep(0.1)
        return True
    except: return False

def _wait_for_user_hover(prompt, dwell_time=1.5):
    """
    【示教捕获】等待用户悬停鼠标来获取坐标
    """
    print(f"\n👉 {prompt}")
    print("   请移动鼠标到目标位置，然后【松手保持不动】...")
    
    last_pos = pyautogui.position()
    stable_start = None
    
    while True:
        curr_pos = pyautogui.position()
        dist = math.sqrt((curr_pos[0]-last_pos[0])**2 + (curr_pos[1]-last_pos[1])**2)
        
        # 5像素容差判定为静止
        if dist < 5: 
            if stable_start is None: 
                stable_start = time.time()
            elif time.time() - stable_start > dwell_time:
                print(f"   ✅ 坐标捕获: {curr_pos}")
                print('\a') # 提示音
                return curr_pos
        else:
            stable_start = None
            last_pos = curr_pos
        time.sleep(0.1)

# -----------------------------------------------------------------------------
# 核心业务函数
# -----------------------------------------------------------------------------

#&&&% 墙体查询
#&&% get_wall_thickness
def get_wall_thickness(wall_obj):
    """
    # 【新增】获取墙体厚度

    Args:
        wall_obj: 天正墙体对象

    Returns:
        float: 墙体厚度（Thickness + Thickness2）
    """
    try:
        from CAD_basic import get_object_property
        t1 = get_object_property(wall_obj, "Thickness") or 0
        t2 = get_object_property(wall_obj, "Thickness2") or 0
        sys_logger.info(f"[成功] 获取墙体厚度: {t1 + t2}")
        return t1 + t2
    except Exception as e:
        sys_logger.error(f"[错误] 获取墙体厚度失败: {e}")
        return None

#&&% get_wall_length
def get_wall_length(wall_obj):
    """
    # 【新增】获取墙体长度

    Args:
        wall_obj: 天正墙体对象

    Returns:
        float: 墙体长度
    """
    try:
        from CAD_basic import get_object_property
        length = get_object_property(wall_obj, "Length")
        sys_logger.info(f"[成功] 获取墙体长度: {length}")
        return length
    except Exception as e:
        sys_logger.error(f"[错误] 获取墙体长度失败: {e}")
        return None

#&&% get_wall_height
def get_wall_height(wall_obj):
    """
    # 【新增】获取墙体高度

    Args:
        wall_obj: 天正墙体对象

    Returns:
        float: 墙体高度
    """
    try:
        from CAD_basic import get_object_property
        height = get_object_property(wall_obj, "Height")
        sys_logger.info(f"[成功] 获取墙体高度: {height}")
        return height
    except Exception as e:
        sys_logger.error(f"[错误] 获取墙体高度失败: {e}")
        return None

#&&&% 墙体修改
#&&% modify_wall_thickness
def modify_wall_thickness(wall_obj, thickness):
    """
    # 【新增】修改墙体厚度

    Args:
        wall_obj: 天正墙体对象
        thickness: 新厚度值

    Returns:
        bool: 成功返回True
    """
    try:
        from CAD_basic import set_object_property
        half = thickness / 2
        set_object_property(wall_obj, "Thickness", half)
        set_object_property(wall_obj, "Thickness2", half)
        sys_logger.info(f"[成功] 修改墙体厚度为: {thickness}")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 修改墙体厚度失败: {e}")
        return False

#&&% modify_wall_height
def modify_wall_height(wall_obj, height):
    """
    # 【新增】修改墙体高度

    Args:
        wall_obj: 天正墙体对象
        height: 新高度值

    Returns:
        bool: 成功返回True
    """
    try:
        from CAD_basic import set_object_property
        set_object_property(wall_obj, "Height", height)
        sys_logger.info(f"[成功] 修改墙体高度为: {height}")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 修改墙体高度失败: {e}")
        return False

#&&&% 门窗修改
#&&% modify_door_size
def modify_door_size(door_obj, width, height):
    """
    # 【新增】修改门尺寸

    Args:
        door_obj: 天正门对象
        width: 新宽度
        height: 新高度

    Returns:
        bool: 成功返回True
    """
    try:
        from CAD_basic import set_object_property
        set_object_property(door_obj, "Width", width)
        set_object_property(door_obj, "Height", height)
        sys_logger.info(f"[成功] 修改门尺寸为: 宽{width}, 高{height}")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 修改门尺寸失败: {e}")
        return False

#&&% modify_window_size
def modify_window_size(window_obj, width, height):
    """
    # 【新增】修改窗尺寸

    Args:
        window_obj: 天正窗对象
        width: 新宽度
        height: 新高度

    Returns:
        bool: 成功返回True
    """
    try:
        from CAD_basic import set_object_property
        set_object_property(window_obj, "Width", width)
        set_object_property(window_obj, "Height", height)
        sys_logger.info(f"[成功] 修改窗尺寸为: 宽{width}, 高{height}")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 修改窗尺寸失败: {e}")
        return False

#&&% delete_door
def delete_door(door_obj):
    """
    # 【新增】删除门

    Args:
        door_obj: 天正门对象

    Returns:
        bool: 成功返回True
    """
    try:
        door_obj.Delete()
        sys_logger.info("[成功] 删除门")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 删除门失败: {e}")
        return False

#&&% delete_window
def delete_window(window_obj):
    """
    # 【新增】删除窗

    Args:
        window_obj: 天正窗对象

    Returns:
        bool: 成功返回True
    """
    try:
        window_obj.Delete()
        sys_logger.info("[成功] 删除窗")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 删除窗失败: {e}")
        return False

#&&&% 柱子操作
#&&% insert_tarch_column
def insert_tarch_column(p, width, height, column_type="矩形柱"):
    """
    # 【新增】插入天正柱子

    Args:
        p: 插入点坐标 (x, y, z)
        width: 柱宽
        height: 柱高
        column_type: 柱子类型，默认"矩形柱"

    Returns:
        dict: {'success': bool, 'column': 柱对象}
    """
    try:
        from system.CAD_coordination import send_cmd_with_sync, wait_quiescent
        from CAD_basic import last_obj

        cmd = f"TColumn\\n{p[0]},{p[1]}\\n{width}\\n{height}\\n\\n"
        send_cmd_with_sync(cmd, wait_after=1.0)
        wait_quiescent(min_quiet=0.5, timeout=10.0)

        column = last_obj()
        sys_logger.info(f"[成功] 插入天正柱子 - 宽{width}, 高{height}")
        return {'success': True, 'column': column}
    except Exception as e:
        sys_logger.error(f"[错误] 插入柱子失败: {e}")
        return {'success': False, 'column': None}

#&&% modify_column_size
def modify_column_size(column_obj, width, height):
    """
    # 【新增】修改柱子尺寸

    Args:
        column_obj: 天正柱对象
        width: 新宽度
        height: 新高度

    Returns:
        bool: 成功返回True
    """
    try:
        from CAD_basic import set_object_property
        set_object_property(column_obj, "Width", width)
        set_object_property(column_obj, "Height", height)
        sys_logger.info(f"[成功] 修改柱子尺寸为: 宽{width}, 高{height}")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 修改柱子尺寸失败: {e}")
        return False

#&&&% 楼梯操作
#&&% insert_tarch_stair
def insert_tarch_stair(p1, p2, stair_type="直跑楼梯"):
    """
    # 【新增】插入天正楼梯

    Args:
        p1: 起点坐标 (x, y, z)
        p2: 终点坐标 (x, y, z)
        stair_type: 楼梯类型，默认"直跑楼梯"

    Returns:
        dict: {'success': bool, 'stair': 楼梯对象}
    """
    try:
        from system.CAD_coordination import send_cmd_with_sync, wait_quiescent
        from CAD_basic import last_obj

        cmd = f"TStair\\n{p1[0]},{p1[1]}\\n{p2[0]},{p2[1]}\\n\\n"
        send_cmd_with_sync(cmd, wait_after=1.0)
        wait_quiescent(min_quiet=0.5, timeout=10.0)

        stair = last_obj()
        sys_logger.info(f"[成功] 插入天正楼梯 - 类型: {stair_type}")
        return {'success': True, 'stair': stair}
    except Exception as e:
        sys_logger.error(f"[错误] 插入楼梯失败: {e}")
        return {'success': False, 'stair': None}

#&&% modify_stair_params
def modify_stair_params(stair_obj, **params):
    """
    # 【新增】修改楼梯参数

    Args:
        stair_obj: 天正楼梯对象
        **params: 参数字典（如 Width=1200, StepCount=15）

    Returns:
        bool: 成功返回True
    """
    try:
        from CAD_basic import set_object_property
        for key, value in params.items():
            set_object_property(stair_obj, key, value)
        sys_logger.info(f"[成功] 修改楼梯参数: {params}")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 修改楼梯参数失败: {e}")
        return False

#&&&% 房间标注
#&&% label_room_name
def label_room_name(room_point, name):
    """
    # 【新增】标注房间名称

    Args:
        room_point: 房间标注点 (x, y, z)
        name: 房间名称

    Returns:
        bool: 成功返回True
    """
    try:
        from system.CAD_coordination import send_cmd_with_sync, wait_quiescent

        cmd = f"TRoomTag\\n{room_point[0]},{room_point[1]}\\n{name}\\n\\n"
        send_cmd_with_sync(cmd, wait_after=1.0)
        wait_quiescent(min_quiet=0.5, timeout=10.0)

        sys_logger.info(f"[成功] 标注房间名称: {name}")
        return True
    except Exception as e:
        sys_logger.error(f"[错误] 标注房间名称失败: {e}")
        return False


def insert_tarch_door_universal(wall_p1, wall_p2, door_key="普通门", cmd_name="TOpening", force_reteach=False):
    """
    【函数编号】: TARCH-UI-PRO-V2 (终极通用版)
    【功能】:
        1. 自动识别并复用 'USERPATH' 下的缓存数据。
        2. 若 key 不存在，自动进入示教模式。
        3. 执行时使用 "目标-干扰-目标" 点击法破解天正记忆。
        4. 使用 "3秒冷却 + 纯坐标输入" 确保插入成功。

    【参数】:
        - wall_p1, wall_p2: 墙体两点
        - door_key: 门窗类型的唯一标识 (如 "双开防火门", "凸窗_1500")
        - cmd_name: 启动命令 (TOpening / TWindow)
        - force_reteach: True 强制重新录入坐标
    """
    global _TARCH_UI_CACHE
    
    # 确保缓存是最新的
    if not _TARCH_UI_CACHE:
        _load_cache_from_disk()

    # =========================================================================
    # 阶段一：示教录入 (如果缓存不存在)
    # =========================================================================
    if (door_key not in _TARCH_UI_CACHE) or force_reteach:
        print(f"\n🛠️ [示教模式] 新类型: {door_key}")
        print(f"   数据将保存至: {_get_dynamic_cache_path()}")
        
        # 1. 启动命令，让用户看到界面
        hwnd = C.acad.HWND
        if not hwnd: hwnd = win32gui.FindWindow("AfxMDIFrame140u", None)
        _activate_cad_safe(hwnd)
        pyautogui.press('esc', presses=2)
        pyautogui.write(f'(command "{cmd_name}")\n', interval=0.05)
        
        print("   ⏳ 等待界面弹出 (2秒)...")
        time.sleep(2.0)
        
        # 2. 开始录入
        data = {}
        # 步骤 1: 门类型下拉框
        data['pos_main_type'] = _wait_for_user_hover("【1/5】点击面板上的'门类型/窗类型'下拉框或图标")
        
        # 步骤 2: 打开图库
        data['pos_open_lib']  = _wait_for_user_hover("【2/5】点击带图片的'图库/表'按钮")
        input("⚠️ 请手动点击刚才的位置打开新窗口，看到新窗口后按【回车】继续...")
        
        # 步骤 3 & 4: 防记忆点击点
        print("--- 下面录入'防记忆'三连点 ---")
        data['pos_target_tree'] = _wait_for_user_hover("【3/5】点击左侧树状图的【目标类别】(如:平开门)")
        data['pos_other_tree']  = _wait_for_user_hover("【4/5】点击左侧树状图的【任意其他类别】(如:推拉门)用于刷新")
        
        # 步骤 5: 翻页与选择
        print("--- 下面录入选择动作 ---")
        data['pos_scroll_start'] = _wait_for_user_hover("【5a】鼠标在滚动条滑块上【按下】的位置 (若无需滚动则点空白处)")
        data['pos_scroll_end']   = _wait_for_user_hover("【5b】鼠标【拖拽松开】的位置 (若无需滚动则点同一点)")
        data['pos_select_item']  = _wait_for_user_hover("【6/5】双击具体门/窗样式的图标位置")
        
        # 3. 保存
        _TARCH_UI_CACHE[door_key] = data
        _save_cache_to_disk()
        
        # 4. 退出示教状态
        print("✅ 录入完成，重置环境...")
        pyautogui.press('esc', presses=3)
        time.sleep(0.5)

    # =========================================================================
    # 阶段二：自动化执行 (Playback)
    # =========================================================================
    try:
        cfg = _TARCH_UI_CACHE[door_key]
    except KeyError:
        print(f"❌ 错误: 找不到配置且录入失败: {door_key}")
        return False

    mid_x = (wall_p1[0] + wall_p2[0]) / 2
    mid_y = (wall_p1[1] + wall_p2[1]) / 2
    
    hwnd = C.acad.HWND
    if not hwnd: hwnd = win32gui.FindWindow("AfxMDIFrame140u", None)
    
    print(f"🚀 [自动执行] 插入: {door_key}")
    
    # A. 启动命令
    _activate_cad_safe(hwnd)
    pyautogui.press('esc', presses=2, interval=0.1)
    pyautogui.write(f'(command "{cmd_name}")\n', interval=0.05)
    
    # 盲等小面板
    time.sleep(1.5)
    
    # B. 机械操作流程
    # 1. 选大类
    pyautogui.click(cfg['pos_main_type'])
    time.sleep(0.5)
    
    # 2. 进图库
    pyautogui.click(cfg['pos_open_lib'])
    time.sleep(1.5) # 等大窗口
    
    # 3. 防记忆三连击 (目标 -> 干扰 -> 目标)
    # 这能强制天正刷新列表，确保位置正确
    pyautogui.click(cfg['pos_target_tree'])
    time.sleep(0.3)
    pyautogui.click(cfg['pos_other_tree'])
    time.sleep(0.3)
    pyautogui.click(cfg['pos_target_tree'])
    time.sleep(0.5)
    
    # 4. 翻页 (模拟拖拽)
    pyautogui.moveTo(cfg['pos_scroll_start'])
    pyautogui.dragTo(cfg['pos_scroll_end'], button='left', duration=0.5)
    time.sleep(0.5)
    
    # 5. 选中 (双击)
    pyautogui.doubleClick(cfg['pos_select_item'])
    # 双击后窗口通常会自动关闭，回到绘图区
    
    # C. 坐标输入 (复用之前的稳健逻辑)
    print("  -> ❄️ 强制冷却 3 秒 (等待命令就绪)...")
    time.sleep(3.0)
    
    # 激活并输入
    print("  -> 激活窗口...")
    _activate_cad_safe(hwnd)
    
    coord_str = f"{mid_x:.2f},{mid_y:.2f}"
    print(f"  -> 🎯 敲击坐标: {coord_str}")
    
    # 只能用 write 敲纯文本，不能用 list，不能用粘贴
    pyautogui.write(coord_str, interval=0.05)
    
    # 确认与结束
    time.sleep(0.5)
    pyautogui.press('enter')
    
    time.sleep(1.0)
    print("  -> 结束命令")
    pyautogui.press('esc') # 结束循环
    
    print(f"✅ [{door_key}] 插入完成。")
    return True





















































