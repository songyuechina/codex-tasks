
import CAD_basic as cb
import sys
import time

print("正在检查上一步的数据...")

# 1. 检查数据
if 'GLOBAL_CTX' not in globals() or GLOBAL_CTX.get('dy') is None:
    print("❌ 错误：内存中没有打印区域数据！")
    print("💡 请先执行 [Step 1]。")
else:
    dy_data = GLOBAL_CTX['dy']
    print(f"🔍 获取到待处理数据，准备插入...")
    
    try:
        # 2. 执行插入
        cb.insert_and_scale_labels_area_power(
            dy_data,
            filepath=None,
            layername="dy_quyu",
            timestamp=None,
            delpan=0,
            debug=True # 开启调试
        )
        
        print("⏳ 等待 CAD 完成指令...")
        cb.wait_command_done()
        time.sleep(1)
        print("✅ 图签插入操作完成！")
        
    except Exception as e:
        print(f"❌ Step 2 执行出错: {e}")
