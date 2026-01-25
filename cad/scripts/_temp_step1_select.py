
import CAD_basic as cb
import sys

# 1. 执行选择
print("正在调用 select_print_areas_maxrect_from_polylines ...")
print("参数: lm=7000 (1:100), cha_Y=2000")

try:
    dy = cb.select_print_areas_maxrect_from_polylines(
        lm=7000,
        tol_single=0.01,
        layer_name="dy_zhuanyong",
        width=0.0,
        color=1,
        z=0.0,
        duanbian=7000,
        debug=True,  # 开启调试输出
        print_rejection_reason=False,
        cha_Y=2000
    )
    
    # 兼容返回值处理
    real_list = []
    if isinstance(dy, tuple): real_list = dy[0]
    elif isinstance(dy, list): real_list = dy
    
    count = len(real_list)
    if count > 0:
        print(f"✅ 成功锁定 {count} 个打印区域。")
        
        # === 关键：将结果存入全局容器 ===
        if 'GLOBAL_CTX' not in globals():
            GLOBAL_CTX = {} # 防御性编程
        
        GLOBAL_CTX['dy'] = dy  # 存入内存
        print("💾 数据已保存到内存变量 GLOBAL_CTX['dy']")
        print("👉 请在控制台点击 [Step 2] 继续。")
    else:
        print("⚠️ 未找到符合条件的区域。")
        GLOBAL_CTX['dy'] = None

except Exception as e:
    print(f"❌ Step 1 执行出错: {e}")
