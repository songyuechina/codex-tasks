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
    


def generate_relation_list(data_list):
    result_list = []
    for i, current in enumerate(data_list):
        best_match = None
        min_metric = float('inf')
        
        for j, candidate in enumerate(data_list):
            if i == j: continue 
            
            dx = abs(current[0] - candidate[0])
            dy = abs(current[1] - candidate[1])
            current_metric = min(dx, dy) # x或y方向取最小差异
            
            if current_metric < min_metric:
                min_metric = current_metric
                best_match = candidate
        
        # 生成字符串格式
        result_list.append(f"{current} : {best_match}")
    return result_list

# 获取生成好的列表
new_list = generate_relation_list(LB_dayingkuang)

# —————————————— 打印部分 ——————————————
print("mapped_list = [")

# 每行打印 12 个
chunk_size = 12
for i in range(0, len(new_list), chunk_size):
    # 取出 12 个元素
    chunk = new_list[i : i + chunk_size]
    
    # 将它们转换成带引号的字符串代码形式，并用逗号连接
    # 例如: 'A:B', 'C:D', ...
    line_content = ", ".join([f"'{item}'" for item in chunk])
    
    print(f"    {line_content},")

print("]")
