def generate_name_and_ratio_from_com(
    comobj,
    A3dy=0,
    Fandy=("ISO_A3_(420.00_x_297.00_MM)", "0:0", "A3", 0),
    tol=10, 
):
    """
    【V5.0 强制兜底版】
    逻辑：
    1. 严格筛选：排除非多段线、非矩形、尺寸过小(<100)的对象 -> return 0
    2. 优先匹配：在 tol 容差范围内寻找标准图框。
    3. 强制兜底：如果找不到标准图框，直接返回“最接近”的那个（将就模式），绝不返回 0。
    """
    import math

    # =========================================================================
    # 第一阶段：严格的合法性校验 (不合格直接踢出)
    # =========================================================================
    
    # 1. 类型检查
    try:
        obj_name = getattr(comobj, "ObjectName", "")
        if "Polyline" not in obj_name:
            return 0
    except: return 0

    # 2. 几何尺寸获取
    try:
        min_pt, max_pt = comobj.GetBoundingBox()
        dx = abs(max_pt[0] - min_pt[0])
        dy = abs(max_pt[1] - min_pt[1])
        
        # 3. 极小尺寸过滤 (短边小于100直接扔)
        if dx < 100 or dy < 100: 
            return 0

        # 4. 矩形形状校验 (防止三角形、L型)
        # 允许 2% 的面积误差
        try:
            real_area = abs(getattr(comobj, "Area", 0))
            box_area = dx * dy
            if box_area > 0 and abs(real_area - box_area) / box_area > 0.02:
                return 0 
        except: pass

        # 统一长宽方向
        length = max(dx, dy)
        width = min(dx, dy)
        orientation_flag = 1 if dy > dx else 0

    except Exception:
        return 0

    # 到这里，说明它肯定是一个合格的矩形多段线。
    # 接下来必须给它返回一个值，不能再 return 0 了。

    # —————————— 强制指定A3模式 ——————————
    if A3dy == 1:
        return (Fandy[0], Fandy[1], Fandy[2], orientation_flag)

    # —————————— 设定动态容差 ——————————
    if length > 1783.5:
        dynamic_tol = 10.0
    else:
        dynamic_tol = 1.0

    # —————————— 数据定义 ——————————
    LB_dayingkuang = [
        (118900, 84100, 100),  (178350, 126150, 150),   (59450, 42050, 50),    (29725, 21025, 25), 
        (133800, 84100, 100),  (200700, 126150, 150),   (66900, 42050, 50),    (33450, 21025, 25), 
        (148600, 84100, 100),  (222900, 126150, 150),   (74300, 42050, 50),    (37150, 21025, 25), 
        (84100,  59400, 100),  (126150, 89100,  150),   (42050, 29700, 50),    (21025, 14850, 25), 
        (105100, 59400, 100),  (157650, 89100,  150),   (52550, 29700, 50),    (26275, 14850, 25), 
        (126100, 59400, 100),  (189150, 89100,  150),   (63050, 29700, 50),    (31525, 14850, 25), 
        (147100, 59400, 100),  (220650, 89100,  150),   (73550, 29700, 50),    (36775, 14850, 25), 
        (59400,  42000, 100),  (89100,  63000,  150),   (29700, 21000, 50),    (14850, 10500, 25), 
        (74300,  42000, 100),  (111450, 63000,  150),   (37150, 21000, 50),    (18575, 10500, 25), 
        (89100,  42000, 100),  (133650, 63000,  150),   (44550, 21000, 50),    (22275, 10500, 25), 
        (104100, 42000, 100),  (156150, 63000,  150),   (52050, 21000, 50),    (26025, 10500, 25), 
        (42000,  29700, 100),  (63000,  44550,  150),   (21000, 14850, 50),    (10500, 7425,  25), 
    ]
    
    drawing_map_ml = [
        ("A0", "1:100"), ("A0", "1:150"), ("A0", "1:50"),  ("A0", "1:25"),
        ("A0+1/8", "1:100"), ("A0+1/8", "1:150"), ("A0+1/8", "1:50"),  ("A0+1/8", "1:25"),
        ("A0+1/4", "1:100"), ("A0+1/4", "1:150"), ("A0+1/4", "1:50"),  ("A0+1/4", "1:25"),
        ("A1", "1:100"), ("A1", "1:150"), ("A1", "1:50"), ("A1", "1:25"),
        ("A1+1/4", "1:100"), ("A1+1/4", "1:150"), ("A1+1/4", "1:50"),  ("A1+1/4", "1:25"),
        ("A1+1/2", "1:100"), ("A1+1/2", "1:150"), ("A1+1/2", "1:50"),  ("A1+1/2", "1:25"),
        ("A1+3/4", "1:100"), ("A1+3/4", "1:150"), ("A1+3/4", "1:50"),  ("A1+3/4", "1:25"),
        ("A2", "1:100"), ("A2", "1:150"), ("A2", "1:50"),  ("A2", "1:25"),
        ("A2+1/4", "1:100"), ("A2+1/4", "1:150"), ("A2+1/4", "1:50"),  ("A2+1/4", "1:25"),
        ("A2+1/2", "1:100"), ("A2+1/2", "1:150"), ("A2+1/2", "1:50"),  ("A2+1/2", "1:25"),
        ("A2+3/4", "1:100"), ("A2+3/4", "1:150"), ("A2+3/4", "1:50"),  ("A2+3/4", "1:25"),
        ("A3", "1:100"), ("A3", "1:150"), ("A3", "1:50"),  ("A3", "1:25")
    ]

    drawing_map = [
        "ISO_A0_(841.00_x_1189.00_MM)", "ISO_A0_(841.00_x_1189.00_MM)", "ISO_A0_(841.00_x_1189.00_MM)", "ISO_A0_(841.00_x_1189.00_MM)",
        "UserDefinedMetric (1338.00 x 841.00毫米)", "UserDefinedMetric (1338.00 x 841.00毫米)", "UserDefinedMetric (1338.00 x 841.00毫米)", "UserDefinedMetric (1338.00 x 841.00毫米)",
        "UserDefinedMetric (1486.00 x 841.00毫米)", "UserDefinedMetric (1486.00 x 841.00毫米)", "UserDefinedMetric (1486.00 x 841.00毫米)", "UserDefinedMetric (1486.00 x 841.00毫米)",
        "ISO_A1_(841.00_x_594.00_MM)", "ISO_A1_(841.00_x_594.00_MM)", "ISO_A1_(841.00_x_594.00_MM)", "ISO_A1_(841.00_x_594.00_MM)",
        "UserDefinedMetric (1051.00 x 594.00毫米)", "UserDefinedMetric (1051.00 x 594.00毫米)", "UserDefinedMetric (1051.00 x 594.00毫米)", "UserDefinedMetric (1051.00 x 594.00毫米)",
        "UserDefinedMetric (1261.00 x 594.00毫米)", "UserDefinedMetric (1261.00 x 594.00毫米)", "UserDefinedMetric (1261.00 x 594.00毫米)", "UserDefinedMetric (1261.00 x 594.00毫米)",
        "UserDefinedMetric (1471.00 x 594.00毫米)", "UserDefinedMetric (1471.00 x 594.00毫米)", "UserDefinedMetric (1471.00 x 594.00毫米)", "UserDefinedMetric (1471.00 x 594.00毫米)",
        "ISO_A2_(594.00_x_420.00_MM)", "ISO_A2_(594.00_x_420.00_MM)", "ISO_A2_(594.00_x_420.00_MM)", "ISO_A2_(594.00_x_420.00_MM)",
        "UserDefinedMetric (743.00 x 420.00毫米)", "UserDefinedMetric (743.00 x 420.00毫米)", "UserDefinedMetric (743.00 x 420.00毫米)", "UserDefinedMetric (743.00 x 420.00毫米)",
        "UserDefinedMetric (891.00 x 420.00毫米)", "UserDefinedMetric (891.00 x 420.00毫米)", "UserDefinedMetric (891.00 x 420.00毫米)", "UserDefinedMetric (891.00 x 420.00毫米)",
        "UserDefinedMetric (1041.00 x 420.00毫米)", "UserDefinedMetric (1041.00 x 420.00毫米)", "UserDefinedMetric (1041.00 x 420.00毫米)", "UserDefinedMetric (1041.00 x 420.00毫米)",
        "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)", "ISO_A3_(420.00_x_297.00_MM)"
    ]

    # =========================================================================
    # 第二阶段：双轨匹配 (优先命中 -> 否则兜底)
    # =========================================================================
    draw_factors = [1.0, 0.5, 0.25, 1.5]
    multipliers = [1.0, 1.1, 1.2]
    
    # 追踪器 1: 完美匹配 (Difference <= dynamic_tol)
    strict_best_index = None
    strict_min_diff = float('inf')

    # 追踪器 2: 兜底匹配 (Global Minimum Difference)
    approx_best_index = None
    approx_min_diff = float('inf')
    
    for i, (std_len, std_wid, scale_val) in enumerate(LB_dayingkuang):
        for df in draw_factors:
            for mult in multipliers:
                
                # --- 计算两种模式的误差 ---
                # A. 模型空间模式
                tgt_len_m = std_len * df * mult
                tgt_wid_m = std_wid * df * mult
                diff_m = abs(length - tgt_len_m) + abs(width - tgt_wid_m)
                
                # B. 布局空间模式
                tgt_len_l = (std_len / scale_val) * df * mult
                tgt_wid_l = (std_wid / scale_val) * df * mult
                diff_l = abs(length - tgt_len_l) + abs(width - tgt_wid_l)
                
                # 取两者中较优的那个误差
                current_diff = min(diff_m, diff_l)
                
                # --- 逻辑 A: 记录全局最小误差 (用于兜底) ---
                if current_diff < approx_min_diff:
                    approx_min_diff = current_diff
                    approx_best_index = i
                
                # --- 逻辑 B: 记录严格匹配 (优先选择) ---
                # 判断标准：长宽误差都在容差内 (这里用总误差简化判断，或者沿用长宽独立判断均可)
                # 为了简化且有效，这里使用总误差 <= 2 * dynamic_tol 近似判断，
                # 或者严格判断: (dL <= tol and dW <= tol)。这里沿用之前的严格逻辑。
                
                # 重新计算单边误差用于严格判定
                if diff_m <= diff_l:
                     d_len = abs(length - tgt_len_m)
                     d_wid = abs(width - tgt_wid_m)
                else:
                     d_len = abs(length - tgt_len_l)
                     d_wid = abs(width - tgt_wid_l)
                
                if d_len <= dynamic_tol and d_wid <= dynamic_tol:
                    if current_diff < strict_min_diff:
                        strict_min_diff = current_diff
                        strict_best_index = i

    # =========================================================================
    # 第三阶段：决策输出
    # =========================================================================
    
    # 1. 优先返回严格匹配的结果
    if strict_best_index is not None:
        final_index = strict_best_index
    
    # 2. 如果没有严格匹配，返回兜底结果 (将就模式)
    elif approx_best_index is not None:
        final_index = approx_best_index
        # sys_logger.info(f"⚠️ [将就匹配] 未找到标准框，已匹配最近似标准 (误差 {approx_min_diff:.1f})")
    
    # 3. 理论上不应该发生 (除非列表为空)，防止 crash
    else:
        return 0

    res_name = drawing_map[final_index]
    res_ratio = drawing_map_ml[final_index][1]
    res_code = drawing_map_ml[final_index][0]
    
    return (res_name, res_ratio, res_code, orientation_flag)
