# CAD_selection API MANIFEST

```
1. 核心工具 (Core & Utils)
--------------------------------------------------------------------------------
[CORE-000]   com_retry(fn, retries=30, delay=0.05)
             : COM调用重试装饰器，自动处理 RPC_BUSY (-2147417846) 等错误。
             
[CORE-002-1] cast_object(obj)
             : [入口] 智能类型转换，将 IAcadEntity 转为具体接口 (如 IAcadLine)。
             
[CORE-002]   _maybe_cast(ent)
             : [核心] 转换核心，混合了查表(CastTo)、动态封装(Dynamic)和兜底策略。
             
[UTILS-001]  to_vt_int(seq)
             : 列表 -> COM 整数变体数组 (VT_I2)。
             
[UTILS-002]  to_vt_variant(seq)
             : 列表 -> COM 变体数组 (VT_VARIANT)。
             
[UTILS-003]  _to_vt_point(pt_tuple)
             : (x,y,z) -> COM 浮点变体数组 (VT_R8)。
             
[UTILS-004]  normalize_rect(x1, y1, x2, y2)
             : 坐标标准化，返回 ((min_x, min_y), (max_x, max_y))。
             
[UTILS-005]  expand_rectangle(p1, p2, offset)
             : 矩形向外扩充 offset 距离。

2. 基础选择引擎 (Selection Engine)
--------------------------------------------------------------------------------
[SEL-001]    ss_select(mode="all", p1=None, p2=None, filter_types=None, filter_data=None, autocast=True, prompt=None)
             : 通用选择集构造器。
             : mode: "all"|"window"|"crossing"|"onscreen"
             : filter_types/data: DXF 组码过滤 (如 [0], ["INSERT"])

3. 几何与空间选择 (Geometric Selection)
--------------------------------------------------------------------------------
[SEL-GEO-001] select_entities_through_point(p, tol=0.1)
              : 点选。通过构造 tol 大小的窗交区域模拟鼠标点击。
              
[SEL-GEO-002] select_objects_in_window_area(x1, y1, x2, y2, max_retry=5)
              : 隐性窗口选择。自动 Zoom 到区域防止选不中，支持重试。
              
[SEL-GEO-003] select_paperspace_objects_in_window(x1, y1, x2, y2)
              : 布局空间区域选择。结合 Window 选择和 BoundingBox 遍历。
              
[SEL-GEO-004] pmxz(prompt="\n请在屏幕拾取图元，以Enter键结束：", autocast=True)
              : 屏幕交互框选 (GetSelection)。
              
[SEL-GEO-005] get_last_n_objects(n=1, autocast=True)
              : 获取模型空间最后生成的 N 个对象。
              
[SEL-GEO-006] last_obj()
              : 获取最后一个对象 (快捷方式)。

4. 类型与图层选择 (Type & Layer Selection)
--------------------------------------------------------------------------------
[SEL-TYPE-001] select_tuceng(layer_names, max_retries=5, delay=0.5, autocast=True)
               : 按图层名选择 (支持 str 或 list[str])。
               
[SEL-ALIAS]    stc(layer_names, **kwargs)
               : select_tuceng 的简写别名。
               
[SEL-TYPE-002] select_kuai(max_retries=5, autocast=True)
               : 全选普通块引用 (INSERT)。
               
[SEL-TYPE-003] select_text(autocast=True) / select_mtext(autocast=True)
               : 全选单行文字 (TEXT) / 多行文字 (MTEXT)。
               
[SEL-TYPE-004] select_line(autocast=True) / select_circle(autocast=True) / select_ellipse(autocast=True)
               : 全选直线 / 圆 / 椭圆。
               
[SEL-TYPE-005] select_polyline(autocast=True)
               : 全选轻量多段线 (LWPOLYLINE)。
               
[SEL-TYPE-006] select_polyline_chuantong(autocast=True)
               : 全选二维多段线 (POLYLINE)。
               
[SEL-TYPE-007] select_spline(autocast=True)
               : 全选样条曲线 (SPLINE)。
               
[SEL-TYPE-011] select_all_texts_mixed(target_space="Model")
               : 混合全选。包含 CAD 文字(*TEXT) 和 天正文字(TDb*)。
               
[SEL-TYPE-012] select_pub_text_entities()
               : 专选 "PUB_TEXT" 图层上的 TDbText 和 TDbMText。
               
[SEL-TYPE-013] select_group_entities(group_obj)
               : 选择组 (Group) 内的所有对象。

5. 可视化与交互 (Visualization & Interaction)
--------------------------------------------------------------------------------
[VIS-001]    yin_to_xian_xuanze(LB, wait_s=0.6)
             : 隐转显 (Delete/Undo法)。强制将 LB 列表放入当前选择集 (兼容性好但慢)。
             
[VIS-002]    yin_to_xian_safe(LB, wait_s=0.1)
             : [推荐] 隐转显 (LISP sssetfirst法)。无副作用高亮选中对象。
             
[VIS-003]    xian_to_yin_pickfirst(clear_grips=True, autocast=True)
             : 获取当前编辑器选中的对象 (Pickfirst)。
             
[VIS-004]    select_entities_in_window(x1, y1, x2, y2, ty=1.0, select_mode="_W")
             : 区域高亮并返回对象。Zoom -> Select -> Pickfirst -> Return。
             
[VIS-005]    highlight_entities_in_window(x1, y1, x2, y2)
             : 仅高亮区域 (视觉提示)。
             
[VIS-006]    highlight_entity_by_bbox(entity)
             : 高亮单个对象 (基于包围盒，对 TDbWall 有额外偏移优化)。
             
[VIS-007]    set_entity_grip_state_precise(ent)
             : 独占式高亮。清除其他选中，仅显示该对象的夹点。
             
[VIS-008]    isolate_modelspace_area(x1, y1, x2, y2)
             : 隔离显示。仅显示区域内对象，隐藏其他 (IsolateObjects)。
             
[VIS-009]    unhide_all(space=None, filter_names=None, highlight=False)
             : 显示隐藏对象 (Visible = True)。

6. 属性与天正支持 (Properties & TArch)
--------------------------------------------------------------------------------
[PROP-000]   _resolve_attr_case_insensitive(obj, attr_name)
             : 属性名大小写智能解析 (PascalCase 优先，缓存加速)。
             
[PROP-001]   get_attr(obj, name)
             : [万能] 获取属性。自动判断天正(Invoke DISPID) 或 普通CAD对象。
             
[PROP-002]   set_attr(obj, name, value)
             : [万能] 设置属性。自动判断天正(Invoke DISPID) 或 普通CAD对象。
             
[PROP-OLD]   get_object_property(obj, property_name) / set_object_property(obj, property_name, value)
             : 兼容旧代码的属性读写接口。
             
[PROP-003]   brute_dump_tarch_props(ent, max_dispid=64)
             : [调试] 暴力扫描天正对象属性 ID (1~max_dispid)。
```