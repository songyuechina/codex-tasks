python property_attribute_demo.py --folder .

说明：脚本先 cad_zt_oneb() → litz()，确保 prop_* 样例存在（可通过 property_draw_demo.py 生成）后依次打开 prop_polyline/prop_text/prop_wall，调用 get_object_property/set_object_property 调整属性，最后 cad_zt_oneb() 复位并写入 test_log.txt。
若需要重建样例文件，可运行 'python property_draw_demo.py --folder .'，该命令同样遵守 cad_zt_oneb → litz → 操作 → cad_zt_oneb 的流程。
