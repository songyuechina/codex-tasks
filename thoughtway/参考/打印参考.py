#&&% LISP窗口打印

def export_model_window_lisp_fit(
        point_a,
        point_b,
        pdf_fullpath,  # <--- 参数名是这个
        *,
        device="DWG To PDF.pc3",
        media="ISO_A3_(420.00_x_297.00_MM)",
        ctb="monochrome.ctb",
        rotation=0,
        xiubukuan=25
):
    """
    【函数编号】: PRINT-002 (LISP 强力修正版 - V2修复Bug)
    """
    import os
    import time

    # 0. 连接环境
    doc = C.doc

    # ———————————————— 1. 坐标标准化 ————————————————
    try:
        x1, y1 = float(point_a[0]), float(point_a[1])
        x2, y2 = float(point_b[0]), float(point_b[1])
        
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
    except Exception as e:
        sys_logger.info(f"❌ [PRINT-LISP] 坐标解析失败: {e}")
        return False

    # ———————————————— 2. 内部辅助：视觉反馈 ————————————————
    def _draw_boundary_markers():
        try:
            if 'draw_lwpolyline' in globals():
                draw_lwpolyline(
                    coords3d=[(min_x, min_y, 0), (min_x, max_y, 0)],
                    layer_name="dy_zhuanyong",
                    width=xiubukuan, color=256, closed=False
                )
                draw_lwpolyline(
                    coords3d=[(min_x, min_y, 0), (max_x, min_y, 0)],
                    layer_name="dy_zhuanyong",
                    width=xiubukuan, color=256, closed=False
                )
        except Exception:
            pass 

    # ———————————————— 3. 执行打印逻辑 ————————————————
    try:
        # A. 绘制边界标记
        #_draw_boundary_markers()

        # B. A0 旋转修正逻辑
        final_rotation = rotation
        if media == "ISO_A0_(841.00_x_1189.00_MM)":
            if rotation == 0:
                final_rotation = 1
                sys_logger.info(f"ℹ️ [A0修正] 检测到 A0 图纸，强制旋转: 0 -> 1")
            elif rotation == 1:
                final_rotation = 0
                sys_logger.info(f"ℹ️ [A0修正] 检测到 A0 图纸，强制旋转: 1 -> 0")

        # C. 构造 LISP 参数
        p1_str = f"{min_x},{min_y}"
        p2_str = f"{max_x},{max_y}"

        # 🔥🔥🔥 修正点：使用正确的变量名 pdf_fullpath 🔥🔥🔥
        pdf_path_lisp = pdf_fullpath.replace("\\", "/") 

        orientation_str = "Portrait" if final_rotation == 1 else "Landscape"

        # 预清理文件
        if os.path.exists(pdf_fullpath):
            try: os.remove(pdf_fullpath)
            except: pass

        # D. 构造 LISP 命令流
        lisp_cmd = f"""(command "-plot" 
            "Yes" "Model" "{device}" "{media}" "Millimeters" 
            "{orientation_str}" "No" "Window" "{p1_str}" "{p2_str}" 
            "Fit" "Center" "Yes" "{ctb}" "Yes" "As displayed" 
            "{pdf_path_lisp}" "No" "Yes"
        ) """

        # E. 发送命令
        clean_cmd = " ".join([line.strip() for line in lisp_cmd.split('\n') if line.strip()])
        doc.SendCommand(clean_cmd + "\n")

        # F. 等待文件生成
        max_wait = 60 # 稍微延长等待时间
        start_time = time.time()
        while time.time() - start_time < max_wait:
            if os.path.exists(pdf_fullpath):
                time.sleep(0.5) 
                if os.path.getsize(pdf_fullpath) > 0:
                    sys_logger.info(f"✅ [LISP-Model] 输出成功: {os.path.basename(pdf_fullpath)}")
                    return True
            time.sleep(0.5)
        
        sys_logger.info(f"❌ [LISP-Model] 超时未生成文件: {os.path.basename(pdf_fullpath)}")
        return False

    except Exception as e:
        sys_logger.info(f"❌ [LISP-Model] 打印流程异常: {e}")
        return False



def export_layout_window_lisp_fit(
        point_a,
        point_b,
        pdf_fullpath,
        layout_name,
        *,
        device="DWG To PDF.pc3",
        media="ISO_A3_(420.00_x_297.00_MM)",
        ctb="monochrome.ctb",
        rotation=0
):
    """
    【函数编号】: PRINT-LAYOUT-ANTI-TARCH (天正穿透版)
    【修复原理】: 使用 ._-plot 强制绕过天正软件的命令劫持。
    """
    import time
    from system.CAD_coordination import wait_quiescent

    doc = C.doc

    # 路径与坐标处理
    pdf_path_final = pdf_fullpath.replace("\\", "/")
    p1_str = f"{point_a[0]},{point_a[1]}"
    p2_str = f"{point_b[0]},{point_b[1]}"
    orientation_str = "Portrait" if rotation == 1 else "Landscape"

    # ———————————————— 1. 构造指令队列 ————————————————
    # 🔥 核心修改：使用 ._-plot 绕过天正劫持
    commands_sequence = [
        "._-plot",         # <--- 关键修改！加点(.)强制使用原生命令，加下划线(_)适配中文版
        "Yes",             # 详细配置
        layout_name,       # 布局名称
        device,            # 打印机
        media,             # 纸张
        "Millimeters",     # 单位
        orientation_str,   # 方向
        "No",              # 反向?
        "Window",          # 窗口模式
        p1_str,            # 角点1
        p2_str,            # 角点2
        "Fit",             # 比例:布满
        "Center",          # 居中
        "Yes",             # 打印样式?
        ctb,               # 样式表
        "Yes",             # 线宽?
        "No",              # 缩放线宽? (Fit模式下)
        "No",              # 先打图纸空间?
        "No",              # 隐藏对象?
        pdf_path_final,    # 文件名
        "No",              # 保存设置?
        "Yes"              # 继续?
    ]

    sys_logger.info(f"🛡️ [天正穿透] 正在向 {layout_name} 发送打印指令...")

    # ———————————————— 2. 激活窗口 ————————————————
    try:
        if doc.WindowState == 2: # 如果最小化了
            doc.WindowState = 1  # 恢复正常
        doc.Activate()
    except: pass

    # ———————————————— 2.5. 等待CAD就绪 ————————————————
    if not wait_quiescent(min_quiet=0.5, timeout=10.0):
        sys_logger.warning("⚠️ CAD未完全就绪，尝试继续...")

    # ———————————————— 2.6. 切换到目标布局 ————————————————
    from scripts.CAD_file_operations import switch_to_layout
    if not switch_to_layout(layout_name):
        sys_logger.error(f"❌ 无法切换到布局: {layout_name}")
        return False

    # 布局切换后等待稳定
    time.sleep(1.0)

    # ———————————————— 3. 步进发送循环 ————————————————
    try:
        # 清理命令行（如果失败则跳过）
        try:
            doc.SendCommand("\x1b\x1b")
            time.sleep(0.2)
        except Exception as esc_err:
            sys_logger.debug(f"⚠️ ESC命令失败（已忽略）: {esc_err}")
            time.sleep(0.2)
        
        for i, cmd in enumerate(commands_sequence):
            # 简单的防错处理：给包含空格的名称加引号
            send_str = cmd
            if " " in str(cmd) and "," not in str(cmd) and not str(cmd).startswith("."):
                 send_str = f'"{cmd}"'
            
            try:
                doc.SendCommand(send_str + "\n")
            except Exception as e:
                # 🔥 天正特异性处理：
                # 天正有时会抛出 "输入无效" 但实际上命令已经进入缓冲区。
                # 如果是第一条命令报错，可能是真报错；如果是中间报错，可能是假警报。
                err_msg = str(e)
                if "天正" in err_msg or "输入无效" in err_msg:
                    sys_logger.info(f"   ⚠️ 无视天正干扰报错 (Step {i}): {cmd}")
                    time.sleep(0.2)
                    continue # 尝试继续发下一条
                else:
                    raise e # 其他错误正常抛出
            
            # 保持 0.15s 步进延迟
            time.sleep(0.15) 
            
    except Exception as e:
        sys_logger.info(f"❌ 发送指令致命中断: {e}")
        return False

    # ———————————————— 4. 等待结果 ————————————————
    max_wait = 20
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if os.path.exists(pdf_fullpath):
            try:
                os.rename(pdf_fullpath, pdf_fullpath)
                sys_logger.info(f"✅ [输出成功] {os.path.basename(pdf_fullpath)}")
                return True
            except OSError:
                time.sleep(0.5) 
                continue
        time.sleep(0.5)
    
    sys_logger.info(f"❌ 超时未生成: {os.path.basename(pdf_fullpath)}")
    return False

#&&% 打印
#&&% 模型空间文件打印

def print_dwg_file_model(
        file_path=None,               # 目标文件路径 (None表示当前文件)
        *,
        # --- 命名与序号控制 ---
        start_index=0,                # 起始序号
        digit_width=2,                # 序号位数
        
        # --- 智能与安全控制 ---
        force_fixed_media=False,      # 是否强制使用固定图幅
        safety_delay=10,              # 横竖切换安全等待时间(秒)
        wps_close_threshold=6,        # 触发WPS关闭的打印张数阈值
        
        # --- 路径与设备配置 ---
        output_folder_root=None,      # 根输出目录
        device="DWG To PDF.pc3",
        media="ISO_A3_(420.00_x_297.00_MM)", # 根输出目录force_fixed_media为真的打印图幅
        ctb="monochrome.ctb",

        # --- 空间定向 ---

        layout_name = None,
        operate_target = "Model",
        select_config = 0,                   #0为常规模式1为精细模式
        use_cache = False,

        #边线补偿宽度
        xiubukuan = 25,

):
    """
    【函数编号】: PRINT-MODEL-MANAGER (V1 - 模型空间专用)
    【功能】: 
        1. 专用于处理模型空间 (Model Space) 的批量打印任务。
        2. 自动打开文件、提取多段线和图签。
        3. 调用 print_polylines_list 引擎执行。
    """
    # 0. 路径初始化
    if output_folder_root is None:
        if userpath: output_folder_root = os.path.join(userpath, "输出pdf")
        else: output_folder_root = r"D:/Myprogramsystem/XT/dayinSHUCHU"

    if select_config == 1:
        xiubukuan = 0.25 

    # 1. 打开文件 & 连接
    doc=C.doc
    if file_path:
        try:
            from CAD_file_operations import open_file
            sys_logger.info(f"📂 打开: {file_path}")
            open_file(file_path)
            
        except Exception as e:
            return f"❌ 打开失败: {e}"

    # 2. 准备输出目录
    try:
        doc_name = doc.Name
        file_name_pure = os.path.splitext(doc_name)[0]
        target_folder = os.path.join(output_folder_root, file_name_pure)
        
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        os.makedirs(target_folder)
    except: pass

    # 3. 强制进入模型空间 & 提取数据
    print("🔍 [Model] 正在提取图框与图签...")
    try:
        doc.SetVariable("TILEMODE", 1) # 🔥 强制模型空间
        
        # 调用你的核心提取函数
        # 该函数返回 [多段线列表, 图签块列表, ...]

        ctq = smart_rebuild_print_info(
        layout_name=layout_name,
        operate_target=operate_target,
        select_config=select_config, 
        use_cache=use_cache,
        )
   
    except Exception as e:
        return f"❌ 数据提取失败: {e}"

    if not ctq or not ctq[0]:
        return "❌ 未找到打印框"
        
    polys_list = ctq[0]
    # 如果有图签列表则获取，没有则为 None
    titles_list = ctq[1] if len(ctq) > 1 else None

    # 4. 委托给打印引擎

    print_polylines_list(
        polylines_list=polys_list,
        title_blocks_list=titles_list, # 传入图签，让引擎自动命名
        
        start_index=start_index,
        digit_width=digit_width,
        folderpath=target_folder,
        
        device=device,
        media=media,
        ctb=ctb,
        
        mode="Model", # 🔥 显式指定模型模式
        force_fixed_media=force_fixed_media,
        safety_delay=safety_delay,
        wps_close_threshold=wps_close_threshold,
        xiubukuan = xiubukuan

    )
    
    # 5. 简单校验
    try:
        if os.path.exists(target_folder):
            generated_files = [f for f in os.listdir(target_folder) if f.lower().endswith(".pdf")]
            actual_count = len(generated_files)
        else:
            actual_count = 0
        
        return f"✅ [Model] 打印完成: {actual_count}/{len(polys_list)} (目录: {file_name_pure})"
    except Exception as e:
        return f"❌ 校验异常: {e}"



#&&% 模型空间批量打印

def print_polylines_list(
        polylines_list,
        title_blocks_list=None,       # [可选] 对应的图签块列表，用于生成文件名
        subproject=None,      
        dwg_num=None,         
        dwg_name=None,        
        *,
        # --- 基础配置 ---
        folderpath=os.path.join(userpath,"输出pdf"),
        start_index=0,
        digit_width=2,
        
        # --- 打印控制 ---
        force_fixed_media=False,
        safety_delay=10,              # 横竖切换的休息时间
        wps_close_threshold=6,
        
        # --- 设备参数 ---
        device="DWG To PDF.pc3",
        media="ISO_A3_(420.00_x_297.00_MM)",
        ctb="monochrome.ctb",
        mode="Model",
        layout_name="布局1",
        xiubukuan = 25,   
):
    """
    【函数编号】: PRINT-FINAL (V14 - 旋转逻辑修复版)
    【修复内容】: 
        1. 废弃正则表达式判定旋转的旧逻辑。
        2. 直接使用 generate_name_and_ratio_from_com 返回的 orientation_flag (0或1) 控制旋转。
        3. 完美支持 UserDefinedMetric 等非标自定义图纸的自动旋转。
    """

    import re
    
    # 0. 环境准备
    doc=C.doc
    
    # 兼容 rebuild_print_area_title_mapping 返回的元组结构
    if isinstance(polylines_list, tuple): polylines_list = polylines_list[0]
    
    if not polylines_list: return False
    if not os.path.exists(folderpath): os.makedirs(folderpath, exist_ok=True)

    try:
        current_doc_name = os.path.splitext(doc.Name)[0]
    except:
        current_doc_name = "Unnamed"
    
    # 1. 切换空间
    try:
        if mode.lower() == "model":
            doc.SetVariable("TILEMODE", 1)
        else:
            doc.SetVariable("TILEMODE", 0)
            doc.ActiveLayout = doc.Layouts.Item(layout_name)
    except: pass

    # ==================== A. 预处理：生成任务单 (含文件名和分组) ====================
    sys_logger.info(f"🚀 [引擎启动] 处理 {len(polylines_list)} 个对象 (图签: {'有' if title_blocks_list else '无'})...")
    
    tasks_landscape = [] # 横向组
    tasks_portrait = []  # 竖向组
    
    for i, pl in enumerate(polylines_list):
        # --- 1. 几何与纸张分析 ---
        bbox = safe_get_bbox(pl) 
        if not bbox: continue
        
        # 获取几何原始宽高，仅用于最后的任务分组 (减少打印机切换卡顿)
        width_raw = float(abs(bbox[1][0] - bbox[0][0]))
        height_raw = float(abs(bbox[1][1] - bbox[0][1]))
        dwg_is_landscape = width_raw > height_raw 
        
        # 调用分析函数
        target_fandy = (media, "Fit", "Fixed", 0)
        print_info = generate_name_and_ratio_from_com(
            pl, A3dy=1 if force_fixed_media else 0, Fandy=target_fandy
        )
        
        if print_info == 0:
            sys_logger.info(f"   ⚠️ 跳过: 第 {i} 个对象无法识别图幅。")
            continue
            
        # 🔥【核心修改】正确解包所有4个参数
        # print_info 结构: (图纸名, 比例, 图号名, 旋转标志0或1)
        calc_media, calc_scale_str, _, calc_orientation = print_info
        
        # --- 2. 旋转计算 ---
        # 🔥【核心修改】直接使用计算好的方向标志，不再猜测
        target_rotation = calc_orientation

        # --- 3. 文件名生成 ---
        idx_str = f"{i + start_index:0{digit_width}d}"
        fname = f"{current_doc_name}-{idx_str}.pdf" 
        
        if title_blocks_list and i < len(title_blocks_list):
            blk = title_blocks_list[i]
            try:
                attrs = get_block_attributes_dict(blk, ignore_empty=True, upper_tag=True)
                
                s_p = attrs.get("子项目名称") or attrs.get("子项名称") or subproject or ""
                d_n = attrs.get("图纸名称") or attrs.get("图名") or dwg_name or ""
                d_u = attrs.get("图纸编号") or attrs.get("图号") or dwg_num or ""
                
                parts = [p for p in [s_p, d_u, d_n] if p]
                if parts: fname = f"{'-'.join(parts)}.pdf"
            except: pass
        elif any([subproject, dwg_num, dwg_name]):
             parts = [p for p in [subproject, dwg_num, dwg_name] if p]
             fname = f"{'-'.join(parts)}-{idx_str}.pdf"



        # 文件名清洗
        fname = "".join([c if c not in '<>:"/\\|?*\n\r\t' else '_' for c in fname])
        full_path = os.path.join(folderpath, fname)

        # --- 4. 存入任务单 ---
        task = {
            "id": i,
            "p_min": bbox[0], "p_max": bbox[1],
            "full_path": full_path,
            "media": calc_media,
            "rotation": target_rotation, # 使用修正后的 0 或 1
            "desc": f"{int(width_raw)}x{int(height_raw)}"
        }
        
        # 按图纸几何形状分组
        if dwg_is_landscape:
            tasks_landscape.append(task)
        else:
            tasks_portrait.append(task)

    sys_logger.info(f"✅ 分组完毕: 横向 {len(tasks_landscape)} 张 | 竖向 {len(tasks_portrait)} 张")
    
    # ==================== B. 执行逻辑 ====================
    total_success = 0
    
    def execute_batch(batch_list, group_name):
        nonlocal total_success
        if not batch_list: return
        
        print("-" * 100)
        sys_logger.info(f"▶️  开始打印【{group_name}】组...")
        for t in batch_list:
            sys_logger.info(f"   [ID={t['id']}] {t['desc']:<12} -> {os.path.basename(t['full_path'])[:40]}...")
            
            try:
                res = False
                # 根据模式调用底层函数
                if mode.lower() == "model":
                    res = export_model_window_lisp_fit(
                        point_a = t["p_min"],     
                        point_b = t["p_max"],     
                        pdf_fullpath = t["full_path"],
                        device = device,
                        media = t["media"], 
                        ctb = ctb,
                        rotation = t["rotation"],
                        xiubukuan = xiubukuan,

                    )
                else:
                    # 布局打印保持原有参数命名
                    try:
                        res = export_layout_window_lisp_fit(
                            point_a = t["p_min"],
                            point_b = t["p_max"],
                            pdf_fullpath = t["full_path"],
                            layout_name = layout_name,
                            device = device,
                            media = t["media"],
                            ctb = ctb,
                            rotation = t["rotation"]
                        )
                    except:
                        # 兼容性尝试 (旧版可能是 lower_left_xy)
                        pass
                
                if res: total_success += 1

                # ---------------------------------------------------------
                # WPS 窗口清理逻辑 (增强版：重试3次 + 先最大化唤醒)
                # ---------------------------------------------------------
                if wps_close_threshold > 0 and total_success % wps_close_threshold == 0:
                    # 尝试 3 次
                    for attempt in range(3):
                        try:
                            import win32gui, win32con
                            
                            # 使用 nonlocal 标记是否在本次扫描中找到了窗口
                            wps_found = False

                            def cb_maximize_and_close(hwnd, ex):
                                nonlocal wps_found
                                # 获取窗口标题
                                title = win32gui.GetWindowText(hwnd)
                                
                                # 判断条件：标题包含 WPS 且 窗口可见
                                if "WPS Office" in title and win32gui.IsWindowVisible(hwnd):
                                    wps_found = True
                                    try:
                                        # 窗口管理
                                        minimize_all_windows()
                                        time.sleep(0.5)
                                        activate_window_by_title("WPS Office", click_titlebar=True)
                                        time.sleep(0.5)

                                        # 1. 先最大化 (唤醒窗口，确保它能接收消息)
                                        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                                        
                                        # 2. 发送关闭指令
                                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                                    except:
                                        pass

                            # 执行遍历
                            win32gui.EnumWindows(cb_maximize_and_close, None)
                            
                            # 如果这一轮扫描没发现任何 WPS 窗口，说明已经清理干净了，提前退出循环
                            if not wps_found:
                                break
                            
                            # 如果发现了并处理了，休息 0.5 秒等待窗口响应关闭，再进行下一轮确认
                            time.sleep(0.5)

                        except Exception as e:
                            # sys_logger.info(f"清理 WPS 出错: {e}") # 调试时可打开
                            pass

                    
            except Exception as e:
                sys_logger.info(f"   ❌ 打印异常: {e}")

    # 1. 执行横向
    execute_batch(tasks_landscape, "横向")
    
    # 2. 中场休息 (给打印机缓冲时间)
    if len(tasks_landscape) > 0 and len(tasks_portrait) > 0:
        print("\n" + "="*50)
        sys_logger.info(f"⏸️  横向结束。等待 {safety_delay} 秒调整打印机方向...")
        print("="*50 + "\n")
        time.sleep(safety_delay)
        
    # 3. 执行竖向
    execute_batch(tasks_portrait, "竖向")

    sys_logger.info(f"\n🏁 全部完成: {total_success}/{len(polylines_list)}")
    return True


#&&&% ===（十三）图纸空间文件打印 ===



def print_dwg_file_layout(
        file_path=None,               # 目标文件路径 (None 则处理当前打开的文件)
        layout_name="布局1",          # 必须指定布局名称
        *,
        # --- 命名与序号控制 ---

        start_index=0,                # 起始序号
        digit_width=2,                # 序号位数 (如 01, 02)

        # --- 路径与设备配置 ---
        output_folder_root=None,      # 输出根目录
        device="DWG To PDF.pc3",      # 打印驱动
        media="ISO_A3_(420.00_x_297.00_MM)", # 默认纸张 (备用)
        ctb="monochrome.ctb",         # 打印样式

        # --- 智能与安全控制 ---
        force_fixed_media=False,      # 是否强制使用固定纸张
        safety_delay=10,              # 横竖分组切换延时
        wps_close_threshold=6,         # 每打几张清理一次 PDF 预览进程

        # --- 空间定向 ---
        operate_target = "Layout",
        select_config = 1,                   #1为小比例模式0为大比例模式元组为自定义
        use_cache = False,
        

):
    """
    【功能】: 布局空间批量打印主管理器 (V7 - Polyline适配版)
    """
    # 0. 路径初始化
    userpath = os.environ.get('USERPATH') 
    if output_folder_root is None:
        output_folder_root = os.path.join(userpath, "输出pdf") if userpath else r"D:/Myprogramsystem/XT/dayinSHUCHU"

    # 1. 环境准备
    doc=C.doc
    


    if file_path:
        from CAD_file_operations import open_file
        open_file(file_path)
        doc=C.doc        

    # 2. 准备输出子目录
    try:
        file_pure_name = os.path.splitext(doc.Name)[0]
    except:
        file_pure_name = "Unnamed"
        
    target_folder = os.path.join(output_folder_root, f"{file_pure_name}_{layout_name}")
    
    # 清理旧文件夹 (可选，根据需求决定是否保留)
    if os.path.exists(target_folder): 
        try: shutil.rmtree(target_folder)
        except: pass 
    os.makedirs(target_folder, exist_ok=True)

    # 3. 提取打印区域与图签映射 (核心侦察 - 修改点1)
    sys_logger.info(f"🔍 [Layout] 正在分析布局 '{layout_name}' 的多段线区域...")
    
    polylines, titles, _ = smart_rebuild_print_info(
    layout_name=layout_name, 
    operate_target=operate_target,
    select_config=select_config,
    use_cache=use_cache,   
    )

    if not polylines:
        return f"❌ 错误: 在布局 '{layout_name}' 中未找到有效的【矩形多段线】打印区域"

    # 4. 执行批量打印任务 (修改点2)
    # 🔥🔥🔥 改为调用新的 Polyline 打印列表函数 🔥🔥🔥
    res = print_layout_polylines_list(
        polylines_list=polylines,     # 传入多段线列表
        title_blocks_list=titles,     # 传入对应的图签块
        layout_name=layout_name,
        folderpath=target_folder,
        start_index=start_index,
        digit_width=digit_width,
        device=device,
        media=media,
        ctb=ctb,
        force_fixed_media=force_fixed_media,
        safety_delay=safety_delay,
        wps_close_threshold=wps_close_threshold,
        # 传递文档元数据用于命名
        dwg_name=file_pure_name,
        dwg_num="" # 如果有需要，可以从这里传递额外的编号
    )
    
    return f"✅ [Layout] 打印完成: {len(polylines)} 张图纸已输出至 {target_folder}"



def print_layout_polylines_list(
        polylines_list,       
        title_blocks_list=None,
        subproject=None,       
        dwg_num=None,          
        dwg_name=None,         
        *,
        layout_name="布局1",
        folderpath=os.path.join(userpath,"输出pdf"),
        start_index=0,
        digit_width=2,
        force_fixed_media=False,
        safety_delay=10,
        wps_close_threshold=6,
        device="DWG To PDF.pc3",
        media="ISO_A3_(420.00_x_297.00_MM)", 
        ctb="monochrome.ctb"
):
    """
    【函数编号】: PRINT-LAYOUT-ENGINE (V7.1 - 侦察版)
    【功能】: 接收多段线列表进行打印，并输出详细的匹配调试信息。
    """
    from  CAD_file_operations   import  switch_to_layout

    doc=C.doc
    
    if not polylines_list: return False
    if not os.path.exists(folderpath): os.makedirs(folderpath, exist_ok=True)

    try: current_doc_name = os.path.splitext(doc.Name)[0]
    except: current_doc_name = "Unnamed"
    
    # 1. 切换布局
    if not switch_to_layout(layout_name):
        sys_logger.info(f"❌ 无法切换到布局: {layout_name}")
        return False
    time.sleep(1.0)
    # ==================== A. 数据预读取 ====================
    sys_logger.info(f"🚀 [Layout引擎] 正在分析 {layout_name} 中的 {len(polylines_list)} 个打印区域...")
    
    # 读取图签数据的逻辑
    titles_data = []
    if title_blocks_list:
        sys_logger.info(f"📋 正在读取图签属性...")
        for idx, blk in enumerate(title_blocks_list):
            try:
                if blk is None:
                    titles_data.append(("", "", ""))
                    continue
                attrs = get_block_attributes_dict(blk, ignore_empty=False, upper_tag=True)
                s_p = attrs.get("子项目名称") or attrs.get("子项名称") or attrs.get("SUB_TITLE") or ""
                d_n = attrs.get("图纸名称") or attrs.get("图名") or attrs.get("TITLE") or attrs.get("DWG_NAME") or ""
                d_u = attrs.get("图纸编号") or attrs.get("图号") or attrs.get("DWG_NO") or attrs.get("DRAWING_NO") or ""
                titles_data.append((s_p, d_n, d_u))
                sys_logger.info(f"   [图块{idx}] {d_u} {d_n}")
            except:
                titles_data.append(("", "", ""))
    
    tasks_landscape = [] 
    tasks_portrait = []  
    
    # 遍历多段线列表
    for i, pl_obj in enumerate(polylines_list):
        
        # 1. Geometry
        bbox = safe_get_bbox(pl_obj) 
        if not bbox: 
            sys_logger.info(f"   ⚠️ 第 {i} 个区域获取包围盒失败，跳过。")
            continue
            
        p_min, p_max = bbox
        width_raw = float(abs(p_max[0] - p_min[0]))
        height_raw = float(abs(p_max[1] - p_min[1]))
        
        dwg_is_landscape = width_raw > height_raw 
        
        # 2. 图幅匹配逻辑
        try:
            print_info = generate_name_and_ratio_from_com(pl_obj, A3dy=0)
        except:
            print_info = 0

        # 🔥🔥🔥🔥🔥 【侦察探针】 START 🔥🔥🔥🔥🔥
        sys_logger.info(f"   🔎 [侦察 ID={i}] 尺寸: {int(width_raw)}x{int(height_raw)}")
        if print_info != 0:
            # 这里的 print_info[0] 就是导致后面报错的“嫌疑犯”
            sys_logger.info(f"      -> 匹配到的纸张名: '{print_info[0]}'") 
            sys_logger.info(f"      -> 匹配到的比例: '{print_info[1]}'")
        else:
            sys_logger.info(f"      -> 匹配失败 (将使用默认 A3)")
        # 🔥🔥🔥🔥🔥 【侦察探针】 END 🔥🔥🔥🔥🔥

        if print_info == 0:
            calc_orientation = 0 if dwg_is_landscape else 1
            calc_media = media 
        else:
            calc_media, _, _, calc_orientation = print_info

        target_rotation = calc_orientation 

        # 3. Filename Generation
        idx_str = f"{i + start_index:0{digit_width}d}"
        final_s_p = subproject
        final_d_n = dwg_name
        final_d_u = dwg_num

        # 如果有图签数据，优先使用图签数据覆盖
        if i < len(titles_data):
            t_sp, t_dn, t_du = titles_data[i]
            if t_sp: final_s_p = t_sp
            if t_dn: final_d_n = t_dn
            if t_du: final_d_u = t_du

        # --- 🔥 核心修改逻辑开始 ---
        # 收集非空的字段
        valid_parts = [p for p in [final_s_p, final_d_u, final_d_n] if p]

        if valid_parts:
            # 【情况1】：获取到了有效信息 -> 拼接名称，不带序号
            # 例如：子项-图号-图名.pdf
            fname = f"{'-'.join(valid_parts)}.pdf"
        else:
            # 【情况2】：完全没有信息 -> 使用默认兜底格式，必须带序号防止重名
            # 例如：文件名-布局名-01.pdf
            fname = f"{current_doc_name}-{layout_name}-{idx_str}.pdf"
        # --- 🔥 核心修改逻辑结束 ---

        # 文件名字符清洗
        fname = "".join([c if c not in '<>:"/\\|?*\n\r\t' else '_' for c in fname])
        full_path = os.path.join(folderpath, fname)


        # 4. Packaging
        task = {
            "id": i,
            "p_min": p_min, "p_max": p_max,
            "full_path": full_path,
            "media": calc_media,
            "rotation": target_rotation,
            "desc": f"{int(width_raw)}x{int(height_raw)}"
        }
        
        if dwg_is_landscape: tasks_landscape.append(task)
        else: tasks_portrait.append(task)

    sys_logger.info(f"✅ 分组完毕: 横向 {len(tasks_landscape)} | 竖向 {len(tasks_portrait)}")

    # ==================== B. 执行逻辑 ====================
    total_success = 0
    

    def execute_batch(batch_list, group_name):
            nonlocal total_success
            if not batch_list: return
            
            sys_logger.info(f"▶️  开始打印【{group_name}】组...")
            
            # 引入 time 模块 (如果外部没引入，这里保险起见引入一下)
            import time 
    
            for t in batch_list:
                sys_logger.info(f"   [ID={t['id']}] {t['desc']:<12} -> {os.path.basename(t['full_path'])[:40]}")
                
                try:
                    # 1. 执行打印指令（使用v1版本 - LISP命令方式）
                    res = export_layout_window_lisp_fit_v1(
                        point_a = t["p_min"],
                        point_b = t["p_max"],
                        pdf_fullpath = t["full_path"],
                        layout_name = layout_name,
                        device = device,
                        media = t["media"],
                        ctb = ctb,
                        rotation = t["rotation"]
                    )
                    
                    if res: total_success += 1
    
                    # 🔥🔥🔥【位置 1：打印冷却期】(关键！) 🔥🔥🔥
                    # 原因：AutoCAD 刚收到指令正在生成 PDF，此时若立即发下一条指令或操作窗口，容易造成“消化不良”卡死。
                    # 建议：最少 1.0 秒，推荐 1.5 秒
                    time.sleep(1.5)
    
                    # ---------------------------------------------------------
                    # WPS 窗口清理逻辑
                    # ---------------------------------------------------------
                    if wps_close_threshold > 0 and total_success > 0 and total_success % wps_close_threshold == 0:
                        
                        sys_logger.info("🧹 触发 WPS 内存清理...")
                        
                        # 🔥🔥🔥【位置 2：操作前缓冲】🔥🔥🔥
                        # 原因：即将进行窗口最小化/最大化的大动作，先让 CPU 喘口气
                        time.sleep(0.5)
    
                        # 尝试 3 次清理
                        for attempt in range(3):
                            try:
                                import win32gui, win32con
                                wps_found = False
    
                                def cb_maximize_and_close(hwnd, ex):
                                    nonlocal wps_found
                                    title = win32gui.GetWindowText(hwnd)
                                    if "WPS Office" in title and win32gui.IsWindowVisible(hwnd):
                                        wps_found = True
                                        try:
                                            # 窗口操作
                                            minimize_all_windows() # 慎用：这会把 CAD 也最小化
                                            time.sleep(0.5) 
                                            activate_window_by_title("WPS Office", click_titlebar=True)
                                            time.sleep(0.5)
                                            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                                            
                                            # 发送关闭
                                            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                                        except: pass
    
                                win32gui.EnumWindows(cb_maximize_and_close, None)
                                
                                if not wps_found:
                                    break
                                
                                time.sleep(0.5) # 等待窗口响应关闭
    
                            except Exception as e:
                                pass
                        
                        # 🔥🔥🔥【位置 3：回归 CAD 焦点】(非常重要！) 🔥🔥🔥
                        # 原因：WPS 清理完后，焦点可能丢失。
                        # 如果不加延迟直接进入下一次循环发送 SendCommand，命令可能发到虚空里。
                        sys_logger.info("🔙 正在恢复 CAD 焦点...")
                        try:
                            # 尝试把 CAD 激活回前台 (防止刚才 minimize_all_windows 把 CAD 也收起来了)
                            activate_window_by_title("AutoCAD", click_titlebar=False) 
                        except:
                            pass
                        
                        # 给 CAD 重新获取焦点的时间
                        time.sleep(1.0) 
    
                except Exception as e:
                    sys_logger.info(f"   ❌ 打印异常: {e}")
    
    
    
    
    
    






    execute_batch(tasks_landscape, "横向")
    if len(tasks_landscape) > 0 and len(tasks_portrait) > 0:
        print("\n" + "="*50)
        sys_logger.info(f"⏸️  横向结束。等待 {safety_delay} 秒调整打印机方向...")
        print("="*50 + "\n")
        time.sleep(safety_delay)
    execute_batch(tasks_portrait, "竖向")

    sys_logger.info(f"\n🏁 [Layout] 打印结束: {total_success}/{len(polylines_list)}")
    return True




