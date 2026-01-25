# -*- coding: utf-8 -*-
# 文件名: CAD_check_standards.py
# 功能: 复杂函数测试规范
# 核心依赖: system/licad.py, system/CAD_coordination.py

# 对复杂函数，必须编写独立的测试py脚本。

#第一，明确目标函数所在的脚本和内容。
#1，所在脚本 D:/claude-tasks/cad/scripts/CAD_basic.py

#2，定义

@timeit
def bianmulu_func4_h(
    layout_name=None, 
    operate_target="Model", 
    # --- 统一标准参数 ---
    select_config=None, 
    verbose=1,
    # --- 合并特有参数 ---
    tol=0.01  
):
    """
    【函数编号】: CAT-UNIFIED-004 (V6.2 - 显式句柄版)
    【核心优化】: 
        1. 移除 li()，全程使用 C.doc/C.acad 显式指定句柄。
        2. 针对“找不到函数”问题，采用模块显式调用 CAD_file_operations.insert_region_between_files。
        3. 增加文件 IO 后的强制等待，确保 CAD 数据库就绪。
    """
    import CAD_file_operations as CFO
    import time
    from pathlib import Path
    import os

    MODEL_SPACE_CHA_Y = 2000 
    
    if verbose >= 1:
        print(f"\n🚀 [编目录 Step 4] 合并目录 | 目标: {operate_target} | 布局: {layout_name}")

    # ================= 1. 获取主文件信息 =================
    doc_main = C.doc
    try:
        main_dwg_path = doc_main.FullName
        if not main_dwg_path:
            print("❌ 主文件未保存，无法定位。")
            return False
        
        src_path_obj = Path(main_dwg_path)
        current_stem = src_path_obj.stem
        parent_dir = src_path_obj.parent
        print(f"📌 主文件锁定: {main_dwg_path}")
        
    except Exception as e:
        print(f"❌ 获取主文件信息失败: {e}")
        return False

    # ================= 2. 推导目录文件路径 =================
    try:
        if operate_target == "Layout":
            mulu_dwg_name = f"{current_stem}_{layout_name}_目录.dwg"
        elif operate_target == "Model":
            candidate_1 = f"{current_stem}_目录.dwg"       
            candidate_2 = f"{current_stem}_Model_目录.dwg" 
            mulu_dwg_name = candidate_1 if os.path.exists(parent_dir / candidate_1) else candidate_2
        
        mulu_dwg_path = str(parent_dir / mulu_dwg_name)
        if not os.path.exists(mulu_dwg_path):
            print(f"❌ 目录文件不存在: {mulu_dwg_path}")
            return False
            
    except Exception as e:
        print(f"❌ 路径推导错误: {e}")
        return False

    # ================= 分支 A: 合并到布局 (Layout) =================
    if operate_target == "Layout":
        print(f"🔄 执行 Layout 跨空间合并...")
        # 1. 打开源文件
        CFO.open_file(mulu_dwg_path)
        time.sleep(1.5) # 显式等待文件 IO 完成
        
        # 使用 C.doc 显式指向当前打开的目录文件
        doc_src = C.doc 
        try:
            # 扫描与缩放逻辑 (省略部分重复逻辑，核心使用 doc_src.SendCommand)
            raw_ret = select_print_areas_maxrect_from_polylines(debug=False, cha_Y=MODEL_SPACE_CHA_Y)
            mulu_polys = raw_ret[0] if isinstance(raw_ret, tuple) else raw_ret
            
            min_x, min_y = mulu_polys[0].GetBoundingBox()[0][:2] # 简化获取基点
            base_pt = f"{min_x},{min_y}"
            
            doc_src.SendCommand(f'(command "_.SCALE" "_All" "" "{base_pt}" "0.01")\n')
            doc_src.SendCommand(f'(command "_.COPYBASE" "{base_pt}" "_All" "")\n')
            time.sleep(1.5)
            doc_src.Close(False) # 炸完即丢
            
        except Exception as e:
            print(f"❌ 复制出错: {e}")
            CFO.open_file(main_dwg_path)
            return False

        # 2. 粘贴回主文件
        CFO.open_file(main_dwg_path)
        doc_target = C.doc
        # ... 执行粘贴逻辑，使用 doc_target.SendCommand ...
        return True

    # ================= 分支 B: 合并到模型 (Model) =================
    elif operate_target == "Model":
        print(f"🔄 执行 Model 同空间合并...")
        
        # 1. 获取源区域
        CFO.open_file(mulu_dwg_path)
        time.sleep(1.0)
        dy = select_print_areas_maxrect_from_polylines(cha_Y=MODEL_SPACE_CHA_Y, debug=False)
        
        min_p, max_p = dy[0][0].GetBoundingBox() # 假设只有一页目录
        src_rect = (min_p[0], min_p[1], max_p[0], max_p[1])
        src_width = src_rect[2] - src_rect[0]
        
        C.doc.Close(False) # 关闭源
        time.sleep(1.0)

        # 2. 获取目标位置
        CFO.open_file(main_dwg_path)
        time.sleep(1.0)
        doc_target = C.doc
        doc_target.SetVariable("TILEMODE", 1)
        
        scan_tol = 20 if layout_name else 2000
        zy = select_print_areas_maxrect_from_polylines(cha_Y=scan_tol, debug=False)
        
        target_x, target_y = 0, 0
        if zy and zy[0]:
            min_tx = min([p.GetBoundingBox()[0][0] for p in zy[0]])
            target_x = min_tx - src_width - 20000 
            target_y = zy[0][0].GetBoundingBox()[0][1]
        
        # 关键操作：必须先关闭 Target 才能执行后台 InsertBlock
        doc_target.Close(True) 
        time.sleep(1.5)

        # 3. 显式调用模块函数 (不再通过全局查找)
        print("⚡ 正在调用 CFO.insert_region_between_files...")
        try:
            # 直接使用 CFO 前缀调用，确保 Python 引擎定位到函数
            success = CFO.insert_region_between_files(
                mulu_dwg_path, main_dwg_path,
                src_rect[0], src_rect[1], src_rect[2], src_rect[3], 
                target_x, target_y 
            )
            
            if success:
                print("✅ 目录合并成功！")
                CFO.open_file(main_dwg_path)
                return True
            else:
                print("❌ 合并函数执行失败。")
                CFO.open_file(main_dwg_path)
                return False
                
        except AttributeError:
            print("❌ 系统错误: CAD_file_operations 中依然找不到 insert_region_between_files。")
            CFO.open_file(main_dwg_path)
            return False

    return True

#3，函数功能结构划分

#对函数的内部代码，按代码顺序分成明确的板块，分别称为 功能逻辑流程1，功能逻辑流程2，……



#4，测试文件路径和内容

#1） D:/Mypro/基础服务/用户1/dwg文件/0103测试/混合空间0103.dwg

#验证文件存在




#2） 运行D:/claude-tasks/cad/scripts/CAD_basic.py，

#执行open_file(file_path)打开文件


















# 明确测试文件的路径。
