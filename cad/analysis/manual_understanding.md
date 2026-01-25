# 函数人工深读记录（持续补充）

说明：本文件是人工深读的函数级理解记录。每条记录包含：作用、关键步骤、输入/输出、依赖/副作用、风险与测试点。

## scripts/CAD_basic.py

### bianmulu_func1_h(layout_name=None, operate_target="Model", mulu_xuhao=1, select_config=None, use_cache=False, verbose=1)
- 作用：目录编制 Step1，扫描主图纸生成独立“目录 DWG”文件并注入模板。
- 关键步骤：
  1) 根据 operate_target/layout_name 推断 select_config；
  2) 调用 smart_rebuild_print_info 扫描图框数量；
  3) 根据主文件名 + layout_name 生成唯一目录文件名；
  4) new_file 创建目录文件 -> 关闭 -> copy_file_content_pywin32 注入模板；
  5) 重新打开目录文件，根据图纸数量剪裁第2页内容（删除窗口内对象）；
  6) 保存并切回主文件，必要时切换布局或 TILEMODE。
- 输入/输出：输入主文件当前文档状态（C.doc），输出 bool 成功/失败。
- 依赖/副作用：
  - 依赖 CAD_file_operations 的 open/new/save/close；
  - 依赖 select_maxrect_polylines_1 与 select_entities_in_window；
  - 文件系统写入：创建/覆盖“_目录.dwg”；
  - 会切换/关闭 CAD 文档，影响当前状态。
- 风险：模板路径依赖 USERPATH；文件占用导致 copy 失败；窗口删除可能误删页面内容。
- 测试点：主文件未保存；模板缺失；图纸数量边界（<=58/<=28）；布局与模型切换。

### bianmulu_func2_h(layout_name=None, operate_target="Model", select_config=None, use_cache=False, verbose=1)
- 作用：目录编制 Step2，打开目录文件并生成/填充目录图签映射（可读取 Excel）。
- 关键步骤：
  1) 从主文件推导目录 DWG 与 Excel 路径（严格后缀规则）；
  2) 打开目录文件并关闭其他文档（净室环境）；
  3) 若图签不存在，复制模板线条并调用 insert_and_scale_labels_area_power 插入图签；
  4) 修复线宽、合并线为多段线、迁移图层；
  5) rebuild_print_area_title_mapping 生成 ctq 映射；
  6) 若 Excel 存在则调用 update_catalog_titleblocks_from_excel 写入。
- 输入/输出：输入主文件与目录模板/Excel；输出 bool。
- 依赖/副作用：
  - 强依赖 CAD_basic 里的选择/插图签/修复函数；
  - 关闭除目录文件以外的所有文档；
  - 可能修改图层/对象/块。
- 风险：环境隔离失败会导致写入错误文件；Excel 缺失时仅生成结构但不填写。
- 测试点：无图签场景；Excel 严格匹配；图层不存在/锁定；插入后 Regen 时序。

### bianmulu_func3_h(layout_name=None, operate_target="Model", mubanxuhao=1, ...)
- 作用：目录编制 Step3，读取 Excel 并写入目录 DWG 表格（目录文字）。
- 关键步骤：
  1) 推导并严格校验目录 DWG 与 Excel 路径；
  2) 打开目录文件并关闭其他文档；
  3) rebuild_print_area_title_mapping 获取 ctq_mulu_local；
  4) write_catalog_from_excel_to_cad 写入表格内容；
  5) 保存并关闭目录文件；finally 恢复主文件/布局。
- 输入/输出：输入 Excel 路径/样式参数；输出 bool。
- 依赖/副作用：
  - 修改目录 DWG 内容；
  - 会强制关闭其他文档；
  - 依赖 write_catalog_from_excel_to_cad。
- 风险：Excel 不存在直接失败；ctq 映射失败导致终止；异常处理较多。
- 测试点：Excel 严格匹配；ctq 为空；布局恢复逻辑。

### bianmulu_func4_h(layout_name=None, operate_target="Model", select_config=None, verbose=1, tol=0.01)
- 作用：目录编制 Step4，将目录 DWG 合并回主文件（布局/模型两种模式）。
- 关键步骤：
  - 布局模式：打开目录文件 -> 计算边界 -> 可能缩放 -> COPYBASE -> 关闭源文件；回主文件定位并 PASTECLIP（左移 3 倍宽）；
  - 模型模式：打开目录文件 -> 计算范围 -> 关闭源 -> 打开主文件 -> 插入块 -> 炸开 -> 删除块定义。
- 输入/输出：输入 layout_name/operate_target；输出 bool。
- 依赖/副作用：
  - 依赖 SendCommand、InsertBlock、Explode；
  - 会修改主文件图元与块定义；
  - 可能缩放目录文件内容（临时）。
- 风险：布局定位依赖图框识别；剪贴板粘贴受焦点/命令状态影响；炸开失败时保留块。
- 测试点：空目录文件；布局为空；比例缩放分支（>5000）；块删除失败。

## library/cad_blocks.py

### redefine_block_with_entities(block_ref, entities, ty=0.5, debug_log_path="C:\\cad_debug_log.txt")
- 作用：将指定实体集合“重定义”进块定义（覆盖模式），并验证更新结果。
- 关键步骤：
  1) 获取块名/Handle/插入点，记录旧块定义实体数量；
  2) 过滤输入实体（排除目标块自身），写入调试日志；
  3) 构造 LISP 选择集变量并批量 ssadd；
  4) 发送 -BLOCK 覆盖命令（Y 覆盖 + 选择集）；
  5) Regen + Update，比较块定义实体数量变化。
- 输入/输出：输入块引用 + 实体列表；输出 bool。
- 依赖/副作用：
  - 强依赖 COM SendCommand 与 USERI1 变量握手；
  - 重定义会移除模型空间对象并写入块定义；
  - 写入本地 debug_log。
- 风险：选择集构造失败/握手失败；块名解析失败；可能误覆盖同名块定义。
- 测试点：空实体/包含自身；动态块 EffectiveName；LISP 选择集长度校验；块定义数量未变。


## scripts/CAD_basic.py (续)

### build_full_print_dict_and_export_excel(ctq, layout_target=None, template_path=None, output_path=None, start_index=1)
- 作用：从 CAD 中提取图框/图签信息，生成项目图纸信息 Excel（支持无图签“纯框线模式”）。
- 关键步骤：
  1) 根据 layout_target 切换布局（若为布局模式）；
  2) 确定模板路径与输出 Excel 路径（按文件名 + 布局后缀规则）；
  3) ctq 解包：polys 与 blocks；无 blocks 时构造 (poly, None) 配对；
  4) 从图签块提取属性（get_block_attributes_dict）并清洗换行；
  5) 调用 generate_name_and_ratio_from_com 估算图幅/比例；
  6) 预扫描全局专业代号并构建 print_infos 列表；
  7) 启动 Excel COM：若输出已存在则继承历史字段；加载模板并增删行；
  8) 写入明细与项目头信息，保存到 output_path。
- 输入/输出：输入 ctq (polys, blocks, mapping)；输出 bool（成功/失败）。
- 依赖/副作用：
  - 强依赖 Excel COM（win32com）；
  - 输出 Excel 文件（可能覆盖同名）；
  - 依赖 CAD 当前文档路径与 USERPATH。
- 风险：Excel COM 无法启动、模板缺失、文档未保存导致路径失败；blocks 与 polys 长度不一致。
- 测试点：无图签模式；布局/模型路径规则；模板行数增删；历史继承逻辑。

### read_excel_and_update_cad_titleblocks(ctq, layout_target=None, excel_path=None, start_index=1)
- 作用：从 Excel 读取项目信息并写回 CAD 图签块（模型/布局双模式）。
- 关键步骤：
  1) 若 layout_target 指定则切换布局；
  2) 推断 Excel 路径（文件名或带布局后缀），并校验存在；
  3) 校验 ctq 与图签块列表；
  4) Excel COM 读取第2行项目通用字段；
  5) 遍历明细行，根据 start_index 计算图签索引；
  6) 组合属性并调用 set_attribute_mtext 写入图签块；
  7) 保存 CAD 文件并等待命令完成。
- 输入/输出：输入 ctq 与 Excel；输出 bool。
- 依赖/副作用：
  - Excel COM 读取；
  - 修改 CAD 图签块属性，保存当前 DWG。
- 风险：Excel 行号与图签数量不一致；布局切换失败；写入异常吞掉。
- 测试点：start_index 偏移；Excel 缺失；空图签列表；布局模式写入。

### write_catalog_from_excel_to_cad(ctq, data_excel_path=None, mubanxuhao=1, start_index=0, ...)
- 作用：将目录 Excel 内容写入目录 DWG 的表格/文字对象。
- 关键步骤（概览）：
  - 读取 Excel 并解析目录行；
  - 结合 ctq 定位目录图签/表格区域；
  - 根据模板序号与样式参数设置文字（高度/宽度因子/对齐等）。
- 输入/输出：输入 ctq 与 Excel；输出 bool（推断）。
- 依赖/副作用：修改目录 DWG 文本对象；依赖 Excel COM。
- 风险：目录结构映射失败；文字样式/行高不匹配。
- 测试点：空 Excel/空 ctq；不同模板序号；文字溢出处理。


## scripts/CAD_basic.py (打印相关)

### export_model_window_lisp_fit(point_a, point_b, pdf_fullpath, device=..., media=..., ctb=..., rotation=0, xiubukuan=25)
- 作用：模型空间窗口打印（LISP 命令版），输出 PDF。
- 关键步骤：
  1) 标准化窗口坐标；
  2) 若纸张为 A0 则自动调整旋转；
  3) 构造 -plot LISP 命令（Window + Fit + Center + CTB）；
  4) SendCommand 执行并等待 PDF 生成。
- 输入/输出：输入两点与 pdf_fullpath；输出 bool。
- 依赖/副作用：
  - SendCommand 驱动 AutoCAD；
  - 会删除同名 PDF 并重新生成。
- 风险：命令执行受 CAD 状态影响；生成超时或文件为空。
- 测试点：A0 旋转逻辑；路径含中文；输出文件已存在。

### export_layout_window_lisp_fit(layout_name, point_a, point_b, pdf_fullpath, ...)
- 作用：布局空间窗口打印（LISP 命令版），输出 PDF。
- 关键步骤：
  1) 切换到 layout_name 并 MSpace=False；
  2) 标准化坐标；
  3) 构造并发送 -plot 命令（Layout/Window/Fit/CTB）；
  4) 等待生成文件。
- 输入/输出：输入 layout_name 与窗口坐标；输出 bool。
- 依赖/副作用：修改当前布局与打印设置；删除同名 PDF。
- 风险：布局切换失败；命令执行时序问题。
- 测试点：布局不存在/空布局；多页布局；输出文件占用。

### export_layout_window_lisp_fit_v1(point_a, point_b, pdf_fullpath, layout_name, ...)
- 作用：旧版布局空间 LISP 打印（绕过部分 COM 打印 BUG），输出 PDF。
- 关键步骤：
  1) 尝试预切换到目标布局（COM）；失败则继续；
  2) 标准化坐标，A0 纸张旋转修正；
  3) 构造完整 -plot LISP 命令（Window + Fit + Center + CTB）；
  4) 发送命令并轮询等待 PDF 生成（最长 60s）。
- 输入/输出：输入布局名/窗口坐标/输出路径；输出 bool。
- 依赖/副作用：SendCommand 驱动打印；删除同名 PDF；可能影响当前命令状态。
- 风险：布局打印交互提示差异导致卡死；超时等待过长。
- 测试点：不同 CAD 版本提示；A0 旋转；路径含空格/中文。

## scripts/CAD_basic.py (目录模板配置)

### read_catalog_template_config(excel_path)
- 作用：读取目录模板 Excel 的“数学定义参数”，支持单元格为 “x1,x2” 或 “x1,y1,x2,y2” 格式。
- 关键步骤：
  1) DispatchEx 启动 Excel，ReadOnly 打开；读取第2行全局参数（Y 起点/行数/行距）；  
  2) 第2-5行读取列坐标（idx/name/no/spec），用 _smart_float 解析范围并取中心；  
  3) 形成 config 字典并返回。
- 输入/输出：输入 Excel 路径；输出 config dict 或 None。
- 依赖/副作用：Excel COM；读取第1工作表；不会改写文件。
- 风险：单元格字符串解析失败被重置为 0；Excel COM 启动失败。
- 测试点：中文逗号；4 值坐标格式；缺失行/列。

### get_my_template_config_from_excel(config_path)
- 作用：读取目录结构 Excel 并生成完整坐标字典（通过 CatalogConfigBuilder）。
- 关键步骤：
  1) 读取第2行全局参数（Y_START_1/Y_START_2/行数）；  
  2) 初始化 CatalogConfigBuilder（行高固定 800）；  
  3) 读取第2-5行的 idx/name/no/spec X 范围；  
  4) builder.generate 生成每排每行的坐标字符串配置。
- 输入/输出：输入 Excel 路径；输出 template_config dict 或 None。
- 依赖/副作用：Excel COM；打印成功日志。
- 风险：行高固定 800 假设不匹配；X 范围解析失败返回 (0,0)。
- 测试点：缺列/空单元格；自定义行高；4 排数据不全。

## scripts/CAD_basic.py (打印引擎/批量)

### export_model_window_pure(point_a, point_b, pdf_fullpath, device=..., media=..., ctb=..., rotation=0, xiubukuan=25)
- 作用：模型空间窗口打印（COM 版），带边界标记和 A0 旋转修正。
- 关键步骤：
  1) 标准化坐标；绘制临时边界标记线（dy_zhuanyong 图层）；  
  2) 配置 ActiveLayout 打印机/纸张/样式；A0 旋转反转；  
  3) SetWindowToPlot -> PlotToFile；清理同名 PDF。
- 输出：bool。
- 副作用：绘制边界标记线（不自动删除）；改变打印设置；写 PDF。
- 风险：标记线污染图面；A0 旋转判断固定。
- 测试点：A0 纸张；pdf 覆盖；无 CAD 连接。

### export_layout_window_pure(point_a, point_b, pdf_fullpath, layout_name, ...)
- 作用：布局空间窗口打印（COM 版），强调“先注入窗口后切换 PlotType”。
- 关键步骤：切换布局 -> 设置窗口 -> PlotType=acWindow -> 设置纸张/样式 -> PlotToFile。
- 输出：bool。
- 副作用：切换布局；修改打印设置；删除同名 PDF。
- 风险：布局切换失败；SetWindowToPlot 顺序不正确会失效。
- 测试点：布局不存在；A0 旋转；坐标反向输入。

### export_layout_window_pure_bianju(point_a, point_b, pdf_fullpath, layout_name, ...)
- 作用：布局打印“边距修正版”，通过 pad_L/R/T/B 微调窗口范围。
- 关键步骤：坐标标准化+边距修正 -> 设置窗口 -> 打印参数 -> PlotToFile。
- 输出：bool。
- 副作用：改变打印窗口；修改打印设置；删除同名 PDF。
- 风险：边距参数固定为 0，需手工调整；A0 修正同上。
- 测试点：边距非零；A0 旋转；布局切换失败。

### print_dwg_file_model(file_path=None, ..., force_fixed_media=False, select_config=0, xiubukuan=25)
- 作用：模型空间批量打印主管理器，打开文件->提取打印框->调用 print_polylines_list。
- 关键步骤：
  1) 设定输出目录并清理旧目录；  
  2) TILEMODE=1，smart_rebuild_print_info 获取打印框/图签；  
  3) 调用 print_polylines_list（传入图签用于命名）。
- 输出：字符串（成功/失败信息）。
- 副作用：删除输出目录；可能打开/切换/保存文档。
- 风险：ctq 为空直接失败；强制模型空间影响当前状态。
- 测试点：file_path 为空/存在；无打印框；select_config=1。

### print_polylines_list(polylines_list, title_blocks_list=None, ..., mode="Model", layout_name="布局1", xiubukuan=25)
- 作用：批量打印引擎（V14），按几何方向分组打印，支持图签命名与 WPS 清理。
- 关键步骤：
  1) 生成任务单：bbox -> generate_name_and_ratio_from_com -> rotation_flag；  
  2) 依据图签属性/外部参数生成文件名并清洗非法字符；  
  3) 横向/竖向分组，分别调用 export_model_window_lisp_fit 或 export_layout_window_lisp_fit；  
  4) 每打印 wps_close_threshold 张尝试关闭 WPS 预览窗口；组间等待 safety_delay。
- 输出：bool（内部统计 total_success）。
- 副作用：打印输出大量 PDF；强制关闭 WPS 窗口；改变 CAD 状态。
- 风险：generate_name_and_ratio_from_com 识别失败；WPS 关闭误杀用户窗口；命名冲突覆盖。
- 测试点：无图签/有图签；横竖混合；wps_close_threshold=0。

## scripts/CAD_basic.py (重复封装/同名实现)

### fix_com_cache / set_current_dimstyle_via_command / shitu_region / shitu_entity / transfer_props_by_matchprop / srhd / srhd_p
- 说明：与 `library/cad_control.py` 同名函数逻辑基本一致，为拷贝/重复实现。
- 建议参考：`library/cad_control.py` 对应函数理解。

### get_spline_length_by_conversion / find_fake_intersection_regions / lines_daduan / delete_duplicate_lines / delete_redundant_lines / get_room_outline_from_point / draw_polyline / TDbMText_content
- 说明：与 `library/cad_geometry.py` 同名函数逻辑基本一致，为拷贝/重复实现。
- 建议参考：`library/cad_geometry.py` 对应函数理解。

### update_block_def_attributes_v7 / get_bounding_box_of_block / delete_block_instances_and_definition_optimized / insert_standard_block / add_entities_to_block_direct / extract_specific_entities_from_block / _atomic_explode_and_delete / safe_explode_retry
- 说明：与 `library/cad_blocks.py` 同名函数逻辑基本一致（含重复定义覆盖）。
- 建议参考：`library/cad_blocks.py` 对应函数理解。

### add_objects_to_group / copy_group_S1_from_doc1_to_doc2 / sc_objs_to_layer / create_layers_from_list / dim_by_points / ensure_layer_model_only / force_layer_objects_color
- 说明：与 `library/cad_objects.py` 同名函数逻辑基本一致，为拷贝/重复实现。
- 建议参考：`library/cad_objects.py` 对应函数理解。

## scripts/CAD_basic.py (目录图签填写)

### update_catalog_titleblocks_from_excel(ctq, excel_path, catalog_name="图纸目录", custom_suffixes=None)
- 作用：读取 Excel 项目信息并写入“目录图签”块属性（包含图幅与比例）。
- 关键步骤：
  1) 校验 ctq 结构与图签块列表；
  2) Excel COM 读取项目字段；
  3) 根据 generate_name_and_ratio_from_com 计算比例/图幅；
  4) 生成图纸编号并调用 set_attribute_mtext 写入。
- 输入/输出：输入 ctq 与 Excel 路径；输出 bool。
- 依赖/副作用：Excel COM；修改 CAD 块属性。
- 风险：Excel 路径推断不稳定；属性写入失败。
- 测试点：ctq 长度不匹配；Excel 缺失；计算比例异常。

### update_catalog_titleblocks_from_excel_y(ctq, excel_path=..., catalog_name="图纸目录", custom_suffixes=None)
- 作用：目录专用版本，仅读取 Excel 项目头信息，自动生成目录图号并写入图签块。
- 关键步骤：
  1) 校验 ctq/块列表与 Excel 路径（缺失则尝试按 doc 名推断固定目录下的 Excel）；  
  2) 仅读取 Excel 第2行项目通用字段（G列起）；  
  3) 以“专业代号”为前缀生成图号：默认 00/00-1.. 或按 custom_suffixes；  
  4) 组装属性并用 set_attribute_mtext 写入；支持多行字段分割。
- 输入/输出：输入 ctq 与 Excel 路径；输出 bool。
- 依赖/副作用：Excel COM；修改 CAD 块属性。
- 风险：固定路径推断失败；多页目录时编号规则固定；Excel 头字段顺序必须一致。
- 测试点：custom_suffixes 长度不足；只有 1 张目录；Excel 缺失。 


## library/cad_objects.py

### ensure_layer(layer_name="jizhunwall")
- 作用：确保图层存在并设为当前图层，然后清空该图层所有对象（最多 5 次重试）。
- 关键步骤：创建/获取图层 -> ActiveLayer 切换 -> select_tuceng 获取对象 -> Delete -> RE/ZE 刷新。
- 输入/输出：输入图层名；无显式返回（None）。
- 依赖/副作用：删除图层内所有对象；发送 RE/ZE 命令；依赖 CAD 连接与选择。
- 风险：误删图层内容；删除失败时残留；需要 CAD 空闲。
- 测试点：图层不存在；对象被锁定/不可删除；空图层。

### set_layer_properties(layer_name, color_index=9, linetype="Continuous", on=True, frozen=False)
- 作用：设置图层颜色、线型、开关、冻结状态（不存在则创建）。
- 关键步骤：获取/创建图层 -> 设置颜色/线型 -> Load 线型 -> LayerOn/Frozen -> RE 刷新。
- 输入/输出：输入图层参数；无显式返回。
- 依赖/副作用：修改图层属性；可能加载线型；发送 RE 命令。
- 风险：线型加载失败；CAD 忙碌导致属性设置失败。
- 测试点：无该线型；冻结/解冻切换；图层已存在。

## system/cad_command_monitor.py

### send_nuclear_esc(hwnd, acad_doc)
- 作用：强制取消 CAD 卡死命令（抢焦点 + 物理 ESC + 消息 ESC + COM SendCommand）。
- 关键步骤：force_bring_to_front 抢焦点；循环 keybd_event 发送 ESC；PostMessage 发送 ESC；doc.SendCommand(chr(27))。
- 输入/输出：输入窗口句柄与文档对象；返回 bool。
- 依赖/副作用：控制系统焦点与键盘；可能影响用户前台操作。
- 风险：窗口焦点失败导致取消无效；后台运行可能触发安全限制。
- 测试点：无 hwnd；CAD doc 为 None；多实例 CAD。

### analyze_state(acad)
- 作用：分析 CAD 忙碌状态，区分空闲/等待输入/异常。
- 关键步骤：读取 ActiveDocument/HWND；GetVariable(CMDACTIVE/CMDNAMES/LASTPROMPT)；Call Rejected 视为忙；关键词检测提示语。
- 输出：(status, display_name, hwnd, doc)，status=0/1/2。
- 风险：COM 异常导致误判；LASTPROMPT 语言差异导致漏检。
- 测试点：命令等待输入；Call Rejected；无文档。


## system/CAD_coordination.py

### CADGuard.__enter__/__exit__
- 作用：事务守卫，支持嵌套与独立回滚（UndoMark）。
- 关键步骤：
  - __enter__: 记录嵌套深度；连接 CAD；wait_quiescent；按需 StartUndoMark；根事务可控制 UI。
  - __exit__: 异常时 EndUndoMark + SendCommand "_U" 回滚；根事务刷新并重置深度；正常时 EndUndoMark + wait_quiescent。
- 输入/输出：作为上下文管理器，异常时返回 False 以继续抛出。
- 副作用：发送 Undo 命令；可能更新 UI；改变 CAD 状态。
- 风险：嵌套深度不一致可能导致撤销范围错误；回滚依赖命令成功发送。
- 测试点：嵌套事务/independent_undo=True；异常抛出路径；CAD 忙碌。

### send_cmd_with_sync(cmd, wait_after=0.3, timeout=30.0)
- 作用：向 CAD 发送命令并同步等待空闲。
- 关键步骤：确保 CAD 可见 -> C.raw_doc.SendCommand -> sleep -> wait_quiescent。
- 输入/输出：输入命令字符串；输出 bool。
- 依赖/副作用：SendCommand 驱动 CAD；可能改变文档状态。
- 风险：命令未执行或被拒绝；wait_quiescent 超时。
- 测试点：CAD 无文档；忙碌状态；命令不带换行。

### wait_quiescent(min_quiet=0.5, timeout=60.0)
- 作用：等待 CAD 命令队列空闲（V3.2 版本，文件内后定义覆盖前定义）。
- 关键步骤：循环读取 C.raw_doc 的 CMDACTIVE/CMDNAMES；异常视为忙碌；持续空闲 >= min_quiet 即通过；超时返回 False。
- 输出：bool。
- 副作用：记录 info 级等待报告（busy_hits 统计）。
- 风险：COM 异常被视为忙碌可能导致长等待；C.raw_doc 为空直接失败。
- 测试点：CAD 忙碌/空闲；超时路径；无文档连接。

### wait_document_opened(path, timeout=120.0)
- 作用：等待指定路径/文件名的文档加载完成。
- 关键步骤：轮询 C.acad.Documents，比较 FullName 或文件名匹配；超时退出。
- 输出：bool。
- 副作用：无。
- 风险：路径大小写/解析差异；文档未完全打开但已列出。
- 测试点：同名不同路径；超时未打开。

## system/common_logger.py

### set_debug_mode(mode=1, who="AI", wait_time=30)
- 作用：更新调试模式与暂停策略（全局 DEBUG_CONFIG）。
- 副作用：影响 checkpoint/CriticalSection 的行为；写日志。
- 风险：全局状态污染；并发场景不隔离。

### record_test_result(script_name=None, func_name=None, is_pass=False, **variables)
- 作用：将测试结果写入 `tests/testfunc.xlsx`。
- 关键步骤：推断调用者脚本/函数名 -> append 行 -> save。
- 副作用：写入 Excel 文件。
- 风险：openpyxl 不可用则跳过；Excel 文件被占用。

### checkpoint(desc, is_pass=True, **variables)
- 作用：记录单次检查点结果（写 Excel + 可选人工暂停）。
- 关键步骤：取调用者信息 -> record_test_result -> 若 HUMAN 模式则 sleep。
- 副作用：写 Excel；可能阻塞等待。
- 风险：误设 HUMAN 模式导致脚本停顿。

### CriticalSection(description="关键操作", script_name=None, func_name=None)
- 作用：关键流程上下文管理器，自动记录 PASS/FAIL 与指标。
- 关键步骤：__enter__ 写日志；__exit__ 写 Excel、处理异常、可选人工暂停。
- 副作用：记录 Excel；可能阻塞等待。
- 风险：异常信息被简化；并发写 Excel。

### node(msg, *args, **kwargs)
- 作用：格式化日志输出的轻量封装。
- 副作用：写日志。

## system/CAD_com_utils.py

### LoggerHotSwapper
- 作用：通过“方法指针替换”实现日志静音（info/debug 置为 no-op）。
- 关键点：warning/error/critical 始终保留；sys_logger 被反向注入 common_logger。
- 风险：并发修改 logger 状态影响全局输出。

### silent_mode()
- 作用：上下文静音模式（进入 mute、退出 unmute）。
- 副作用：抑制 info/debug 输出。
- 风险：嵌套使用时状态恢复依赖正确退出。

### retry_on_busy(func_or_retries=None, max_retries=10, base_delay=0.5)
- 作用：通用 COM 忙碌重试装饰器，指数退避并 PumpWaitingMessages。
- 判据：RPC Busy 错误码或字符串；RPC Down 直接抛错。
- 风险：长时间重试导致阻塞。

### SafeCOM.call / SafeCOM.list_selection
- 作用：在无法装饰器的场景下安全调用 COM；稳定转换选择集为列表。
- 风险：SelectionSet.Count 变化导致空结果。

### alias(*names)
- 作用：为函数添加模块级别别名（设置属性）。
- 副作用：污染模块命名空间。

### node(msg, *args, **kwargs)
- 作用：调试输出控制（仅 DEBUG 且栈底函数允许输出）。
- 风险：DEBUG/栈状态不一致导致无输出。

### timeit(func)
- 作用：耗时统计装饰器（info 开始、warning 结束）。
- 副作用：写日志；异常时写 error 并抛出。

### debuggable(func)
- 作用：调试标记装饰器（当前实现不改变行为）。

## system/project_setup.py

### PathConfig
- 作用：统一项目路径配置与 USERPATH 解析。
- 关键步骤：基于 __file__ 推断项目根目录；注入 sys.path；导出 SCRIPTS/TESTS/LOGS 等路径；从 USERPATH 环境变量解析用户根目录。
- 副作用：修改 sys.path；自动创建 logs/tests 目录。
- 风险：USERPATH 未设置时 fallback 固定路径；路径权限问题。

## system/CAD_basic_operations.py

### close_current_dwg_paradigm(save_option="prompt")
- 作用：关闭当前 DWG（API Close 版，不弹保存对话框）。
- 关键步骤：GetActiveObject -> ActiveDocument.Close(True/False)；prompt 模式若未保存则自动保存。
- 输出：bool。
- 副作用：关闭当前文档，可能强制保存。
- 风险：未命名文件 SaveAs 失败；Close(True) 触发异常。

### save_current_dwg_paradigm()
- 作用：保存当前 DWG（三级策略：COM Save -> QSAVE -> SaveAs 覆盖）。
- 关键步骤：检查 ReadOnly/未命名；强制 Saved=False；尝试 Save；失败则 SendCommand _qsave；最后 SaveAs 覆盖。
- 输出：bool。
- 副作用：写磁盘；可能触发命令执行等待。
- 风险：RPC Busy；SaveAs 覆盖失败。

### save_as_dwg_paradigm(output_path)
- 作用：另存为 DWG（优化版）。
- 关键步骤：检查占用；创建目录；可用短路径；SaveAs 阻塞保存并验证文件存在。
- 输出：bool。
- 风险：路径只读/被占用；短路径获取失败。

## system/cad_dialog_killer.py

### read_delay()
- 作用：从控制文件读取对话框关闭延迟秒数。
- 输出：int（失败返回 0）。
- 风险：控制文件缺失或内容非法。

### get_cad_pids()
- 作用：获取 CAD 进程 PID 集合。
- 关键步骤：psutil.process_iter 过滤 acad.exe/tarcht20v9.exe。
- 风险：psutil 权限不足或进程名变更。

### enum_and_maybe_close(hwnd, cad_pids, delay, now)
- 作用：枚举窗口，筛选 CAD 对话框并按延迟发送 ESC 关闭。
- 关键步骤：可见窗口 + #32770 + PID 属于 CAD；记录首次出现时间；超时则 PostMessage ESC。
- 副作用：关闭对话框；更新 _first_seen。
- 风险：误关闭合法对话框；窗口类名变化。

### is_already_running() / create_lock() / remove_lock()
- 作用：单实例锁机制（lock 文件记录 PID）。
- 副作用：创建/删除锁文件。
- 风险：锁文件残留导致误判。

### main()
- 作用：主循环，周期性扫描对话框并按配置关闭。
- 关键步骤：读取 delay -> 获取 CAD PIDs -> EnumWindows -> enum_and_maybe_close -> sleep。
- 风险：无限循环；错误处理依赖 KeyboardInterrupt。

## system/CAD_enhanced_functions.py

### open_dwg_enhanced(path, visible=True)
- 作用：增强版 DWG 打开（集成协同等待）。
- 关键步骤：ensure_single_process -> Dispatch AutoCAD -> Open -> wait_document_opened -> wait_quiescent。
- 输出：(acad, doc) 或 (None, None)。
- 风险：COM 初始化失败；打开超时。

### open_dwg_sync(path, visible=True)
- 作用：同步打开 DWG（先启用弹窗治理与协同）。
- 关键步骤：start_cad_with_dialog_killer -> ensure_single_process -> open_dwg_enhanced。
- 输出：bool。
- 风险：CAD 未启动导致失败；依赖 start_cad_with_dialog_killer。

### start_cad_session_with_coordination()
- 作用：启动 CAD 并激活协同机制。
- 关键步骤：start_cad_with_dialog_killer -> ensure_single_process -> wait_quiescent。
- 输出：bool（空闲失败也返回 True）。
- 风险：启动失败被掩盖。

### test_cad_coordination()
- 作用：自测协同机制（启动、发送命令、等待空闲）。
- 副作用：发送 LINE 命令；修改图面。


## system/CAD_selection.py

### select_objects_in_window_area(x1, y1, x2, y2)
- 作用：隐性窗口选择，先自动 Zoom 到范围，再使用 ss_select 获取窗口内对象。
- 关键步骤：计算中心与 margin -> ZoomWindow 或 Zoom 命令 -> ss_select("window").
- 输入/输出：输入窗口坐标；返回对象列表。
- 依赖/副作用：改变视图缩放；依赖 CAD COM 与 ss_select。
- 风险：Zoom 失败时依赖 SendCommand；坐标顺序错误需 normalize。
- 测试点：小窗口/极大窗口；无对象场景；CAD 忙碌。

### yin_to_xian_xuanze(LB, wait_s=0.6)
- 作用：将“隐性选择集”转为显性选择（Delete/Undo 法）。
- 关键步骤：StartUndoMark -> 删除对象 -> _U 撤销 -> SELECT P。
- 输入/输出：输入对象列表；无显式返回。
- 副作用：触发撤销栈与选择集状态。
- 风险：删除失败导致撤销不完整；命令堆栈受干扰。
- 测试点：空列表；对象不可删除。

### xian_to_yin_pickfirst(clear_grips=True, autocast=True)
- 作用：从 PickfirstSelectionSet 获取当前显性选择并返回对象列表。
- 关键步骤：读取 PickfirstSelectionSet -> SafeCOM.list_selection -> 可选清空 grips。
- 输入/输出：返回对象列表。
- 风险：选择集正被用户操作时返回空；清空影响用户交互。
- 测试点：无选择集；autocast 开关。

### select_entities_in_window(x1, y1, x2, y2, ty=1.0, select_mode="_W")
- 作用：通过命令方式窗口选择，并返回 PickfirstSelectionSet。
- 关键步骤：ZOOM 到范围 -> SELECT Window -> SafeCOM.list_selection。
- 副作用：改变视图；影响当前选择集。
- 风险：SendCommand 时序问题；时间等待不足导致空集。
- 测试点：不同 select_mode（_W/_C）；窗口极小；ty=0。

### set_entity_grip_state_precise(ent)
- 作用：通过 sssetfirst 将单个实体设置为抓手激活状态。
- 关键步骤：清空 sssetfirst -> handent 选中指定 Handle。
- 副作用：改变当前选择集/抓手显示。
- 风险：Handle 不可用；命令执行失败。
- 测试点：无 ent；实体已被删除。

### ss_select(mode="all", p1=None, p2=None, filter_types=None, filter_data=None, autocast=True, prompt=None)
- 作用：通用选择集构造器（重构版），支持 all/window/crossing/onscreen。
- 关键步骤：创建唯一 SelectionSet -> 按模式 Select -> SafeCOM.list_selection 拉取 -> autocast。
- 副作用：触发选择集；最终删除 SelectionSet。
- 风险：mode 传参错误；过滤器类型/数据不匹配。
- 测试点：window/crossing/onscreen；过滤器为空；大批量对象。

### select_paperspace_objects_in_window(x1, y1, x2, y2)
- 作用：在图纸空间窗口选择对象（优先 Select，失败则遍历 BoundingBox）。
- 关键步骤：TILEMODE=0；normalize_rect；ss_select(window)；否则遍历 C.sp 判断相交。
- 输出：对象列表。
- 副作用：切换到布局空间。
- 风险：大对象量遍历较慢；GetBoundingBox 失败对象被跳过。
- 测试点：空布局；大量对象；极小窗口。

### get_last_n_objects(n=1, autocast=True)
- 作用：获取 ModelSpace 中最后生成的 N 个对象。
- 关键步骤：从 mp.Count - n 开始遍历 Item(i)；可选 autocast。
- 输出：对象列表。
- 风险：ModelSpace.Count 变化导致结果不稳定。
- 测试点：n 大于 Count；autocast=False。

### unhide_all(space=None, filter_names=None, highlight=False)
- 作用：批量将隐藏对象 Visible=True，可按类型过滤并高亮。
- 关键步骤：SafeCOM.list_selection 获取空间对象；若 Visible=False 且类型匹配则设置 Visible=True；可 Highlight。
- 输出：被揭示对象列表。
- 副作用：改变对象可见性；可高亮对象。
- 风险：大量对象遍历耗时；特殊对象 Visible 属性不可写。
- 测试点：filter_names 为空/指定；highlight=True。


## scripts/CAD_basic.py (块重定义)

### redefine_block_with_entities(block_ref, entities, ty=0.5, debug_log_path="C:\\cad_debug_log.txt")
- 说明：与 `library/cad_blocks.py::redefine_block_with_entities` 基本一致，为调试版重定义块内容（使用 -BLOCK 覆盖）。
- 依赖/副作用：同库版本（LISP 选择集 + -BLOCK 覆盖 + Regen）。
- 风险/测试点：同库版本；注意该函数在 CAD_basic 中重复定义来源。


## scripts/CAD_file_operations.py

### new_file(output_path=None, close_after=False)
- 作用：在确保天正/ CAD 环境稳定的前提下新建 DWG（可选择关闭）。
- 关键步骤：
  1) 若目标路径已打开则激活并返回；若存在同名文件则删除；
  2) 控制打开文件数量（<=3），多余则关闭；
  3) 天正环境自检：绘制墙体确认可用，不可用则 cad_zt_zero + cad_zt_oneb 重新初始化；
  4) 调用 new_dwg_enhanced 创建文件；可按 close_after 关闭。
- 输入/输出：output_path 为空则创建未保存文档；返回 bool。
- 副作用：可能删除同名文件；关闭其他文档；重启 CAD 环境；绘制/删除临时墙体。
- 风险：误删同名文件；cad_zt_* 会重置环境；绘墙自检对文档有短暂污染。
- 测试点：目标文件已打开/锁定；CAD 忙碌；打开文档数>3。

### open_file(file_path)
- 作用：安全打开 DWG（单例进程 + 负载控制 + 幂等激活）。
- 关键步骤：li 连接 -> 必要时 litz 初始化 -> 若已打开则激活；若打开数量过多则关闭非活跃；最后打开目标文件。
- 输入/输出：file_path；返回 bool。
- 副作用：可能关闭其他文档、重启 CAD 环境、切换激活文档。
- 风险：路径解析失败；文件占用导致无法打开；多进程清理误杀。
- 测试点：文件已打开；文件不存在；多进程场景。

### save_file()/save_file_as(output_path)/close_file(save_option="auto_save")
- 作用：当前活动文档保存、另存为与关闭。
- 关键步骤：调用 CAD_basic_operations 的 save_current/save_as/close_current 相关范式；处理 auto_save。
- 副作用：写磁盘，关闭文档。
- 风险：只读文件/权限问题；保存时 CAD 忙碌。
- 测试点：未保存文档；只读状态；save_option="no_save"。

### switch_to_layout(layout_name, retry=10, delay=0.5)
- 作用：切换到指定布局并等待激活。
- 关键步骤：doc.Layouts.Item(layout_name) -> ActiveLayout；重试直到成功。
- 副作用：改变当前布局与 MSpace 状态。
- 风险：布局不存在/被锁定；切换失败时影响后续操作。
- 测试点：无该布局；多次切换；CAD 忙碌。

## scripts/CAD_System_Queue.py

### LockManager._write_lock()
- 作用：写入 SYSTEM.lock，记录当前用户和时间。
- 关键步骤：json.dump({"user": self.user, "time": now}) 到 lock_file。
- 副作用：创建/覆盖锁文件。
- 风险：文件写入失败被吞掉；锁文件残留。
- 测试点：无写权限；已有锁文件。

### LockManager.release()
- 作用：释放锁与等待文件（SYSTEM.lock / WAITING.list）。
- 关键步骤：若存在则 os.remove。
- 副作用：删除锁文件。
- 风险：删除失败被吞掉；并发释放导致竞态。
- 测试点：文件不存在；权限不足。

### MasterRunner.__init__(root, user_name, service_path)
- 作用：GUI 主控制器初始化（路径、UI、IDLE 引擎、线程）。
- 关键步骤：
  1) 设置 USERPATH、窗口标题与几何；  
  2) 初始化 LockManager；配置 ttk 样式与配置变量；  
  3) 写入 IDLE 引导脚本并异步启动 IDLE；  
  4) 构建 UI 标签页并刷新路径；  
  5) 启动监控线程与关闭钩子。
- 副作用：设置环境变量；启动线程/子进程；写 bootstrap 文件。
- 风险：IDLE 启动失败；UI 线程阻塞。
- 测试点：不同用户目录；无权限写入 BOOTSTRAP_FILE。

### MasterRunner._ensure_bootstrap()
- 作用：生成/刷新 IDLE_bootstrap.py。
- 关键步骤：写入 IDLE_BOOTSTRAP_CODE 到 BOOTSTRAP_FILE。
- 副作用：覆盖 bootstrap 文件。
- 风险：写入失败被吞掉导致后续启动无脚本。
- 测试点：只读目录；编码异常。

## scripts/CAD_Legacy_Runner.py

### LegacyCADRunner.__init__(root)
- 作用：初始化 Tk GUI 控制台，绑定 CAD 基础功能按钮。
- 关键步骤：配置窗口与按钮；建立日志区域；重定向 stdout/stderr 到 UI；设置线程执行包装器。
- 副作用：覆盖 sys.stdout/sys.stderr；启动 UI 事件循环。
- 风险：UI 线程阻塞；print 重定向影响其他模块输出。
- 测试点：无 CAD 连接时按钮行为；多线程输出。

### LegacyCADRunner.gui_save_as()
- 作用：GUI 另存为当前 DWG。
- 关键步骤：cb.li() 确保连接 -> 文件对话框取路径 -> 线程内调用 cfo.save_as 或 doc.SaveAs。
- 输出：无返回（日志提示）。
- 副作用：保存/另存为文件；线程执行。
- 风险：未连接 CAD 时直接退出；路径为空/权限不足。
- 测试点：cfo.save_as 缺失分支；文件覆盖。

## Versioned snapshots (旧版脚本对照)

### system/CAD_coordination - V10.py / V20.py / V33.py
- 说明：历史版本快照，核心函数（CADGuard / wait_quiescent / send_cmd_with_sync / wait_document_opened）与 `system/CAD_coordination.py` 逻辑相近。
- 建议参考：以 `system/CAD_coordination.py` 最新版理解为准。

### system/CAD_selection - V10.py
- 说明：历史版本快照，选择函数与 `system/CAD_selection.py` 基本同构。
- 建议参考：以当前文件的 ss_select/select_* 逻辑为准。

### system/licad - V10.py / V20.py
- 说明：历史版本快照，AutoCadProxy 的 li/open/close 等接口与 `system/licad.py` 基本一致。
- 建议参考：以 `system/licad.py` 最新版理解为准。

### scripts/CAD_System_Queue - V30.py / V31.py / V33.py
- 说明：历史版本快照，LockManager/MasterRunner 逻辑与 `scripts/CAD_System_Queue.py` 大体一致。
- 建议参考：以 `scripts/CAD_System_Queue.py` 最新版理解为准。

## scripts/CAD_check_standards.py

### bianmulu_func4_h(layout_name=None, operate_target="Model", select_config=None, verbose=1, tol=0.01)
- 作用：目录编制 Step4 的“测试规范版”，显式使用 C.doc 与 CAD_file_operations。
- 关键步骤：
  1) 获取主文件路径并推导目录 DWG；  
  2) Layout 分支：打开目录文件 -> 选择范围 -> SCALE/COPYBASE -> 关闭源 -> 再粘贴回主文件；  
  3) Model 分支：打开目录文件 -> 计算区域 -> 关闭 -> 打开主文件 -> 计算目标位置 -> 调用 insert_region_between_files。
- 输出：bool。
- 副作用：打开/关闭文档；发送命令；可能缩放目录内容。
- 风险：路径推导失败；insert_region_between_files 缺失；命令执行时序问题。
- 测试点：布局/模型两分支；目录文件不存在；目标位置计算边界。

## scripts/脚本导航14版.py

### clean_old_logs()
- 作用：清理非当天的导航器日志文件。
- 关键步骤：遍历 script_navigator_*.log，解析日期，不是今天则删除。
- 副作用：删除旧日志文件。
- 风险：日期解析失败；文件被占用。
- 测试点：无日志文件；历史日志存在。

### _normalize_registry_path(path)
- 作用：将注册表路径标准化为绝对路径。
- 关键步骤：Path.resolve 或 os.path.abspath。
- 输出：规范化路径或原值/None。
- 风险：异常时回退到原值。

### _pid_exists(pid)
- 作用：检查进程是否存在（跨平台）。
- 关键步骤：Windows 用 OpenProcess；其他平台用 os.kill(pid,0)。
- 输出：bool。
- 风险：权限不足导致误判。

### _read_registry_data() / _write_registry_data(data)
- 作用：读取/写入脚本注册表 JSON。
- 关键步骤：读 REGISTRY_FILE -> dict；写入 JSON（indent=2）。
- 副作用：读写磁盘文件。
- 风险：JSON 解析失败；写入失败被吞掉。

### _cleanup_registry_data(data)
- 作用：清理注册表中过期 PID，去重并剔除无效进程。
- 输出：bool（是否发生修改）。
- 风险：_pid_exists 误判；数据结构异常被移除。

### _load_clean_registry()
- 作用：读取注册表并清理后回写。
- 关键步骤：_read_registry_data -> _cleanup_registry_data -> _write_registry_data。
- 输出：清理后的 dict。

### parse_mark_line(raw)
- 作用：解析脚本中的 #&& 标记层级。
- 输出：(level, text) 或 None。
- 风险：BOM/空白处理不一致。

### is_file_in_use(filepath)
- 作用：检测文件是否被其他进程占用（基于 psutil）。
- 关键步骤：遍历进程 open_files，匹配路径。
- 输出：bool。
- 风险：psutil 不可用则跳过；AccessDenied。

### _tree_walk(tree, parent="")
- 作用：遍历 Tk Treeview 的所有节点（生成器）。
- 输出：节点 id 迭代器。

### ScriptNavigator.__init__(script_path=None)
- 作用：脚本导航 GUI 初始化（IDLE 引导、树形视图、查找与运行）。
- 关键步骤：clean_old_logs -> _ensure_idle_bootstrap -> 初始化状态字段 -> 构建 UI/快捷键 -> 可选加载初始脚本。
- 副作用：启动 UI 线程；可能启动 IDLE 子进程；写注册表/日志。
- 风险：IDLE 引导失败；UI 过多状态导致内存压力。


## system/licad.py

### get_acad_doc(max_wait=15.0)
- 作用：获取或启动 AutoCAD 应用与文档（自愈版，V3 覆盖前版）。
- 关键步骤：
  1) 检测 acad.exe 进程；若存在但 COM 未就绪则等待；
  2) 若超时则尝试清理 win32com 缓存 gen_py 并提示重启；
  3) 若无进程则 EnsureDispatch 启动新实例；
  4) 获取 ActiveDocument，不存在则 Documents.Add。
- 输入/输出：max_wait 超时阈值；返回 (app, doc) 或抛异常。
- 副作用：可能清理 COM 缓存；可能启动新 CAD 实例。
- 风险：僵尸进程导致长等待；清缓存需要重启 Python/CAD 生效。
- 测试点：已有 CAD 未就绪；无进程；缓存损坏情形。

### AutoCadProxy.li()
- 作用：智能连接 CAD 并校验可用性；刷新 acad/doc/mp/sp。
- 关键步骤：
  1) 校验现有连接是否有效；
  2) 调用 get_acad_doc 获取 app/doc；
  3) 通过 ModelSpace 添加/删除线验证可写；
  4) 设置 Visible 并缓存 mp/sp。
- 输出：True/False。
- 风险：COM 忙碌/断连；校验写入失败。
- 测试点：ActiveDocument 切换；CAD 忙碌。

### AutoCadProxy.open_file(path)
- 作用：打开 DWG 文件，若已打开则激活。
- 关键步骤：遍历 Documents 比较 FullName；未打开则 Documents.Open；连接刷新。
- 输出：bool。
- 风险：路径不存在；Documents.Open 抛异常。
- 测试点：已打开/未打开；大小写路径。

### AutoCadProxy.save_file / save_file_as
- 作用：保存当前文档或另存为指定路径。
- 副作用：写磁盘；save_file_as 刷新连接。
- 风险：只读/权限不足。

### AutoCadProxy.close_file(opt="auto_save") / close_dwg_by_name
- 作用：保存并关闭当前文档或按名称关闭文档。
- 副作用：关闭文档，可能触发保存。
- 风险：关闭目标错误；COM 忙碌导致失败。


## library/cad_blocks.py

### attsync_block_instance_base(block_ref_obj)
- 作用：对指定块执行 ATTSYNC 同步（刷新属性显示）。
- 关键步骤：获取块名（EffectiveName/Name）-> 发送 _ATTSYNC N 块名 命令。
- 输入/输出：输入块引用；返回 bool（命令发送成功与否）。
- 依赖/副作用：SendCommand 改变 CAD 命令状态；可能影响当前选择。
- 风险：动态块名解析失败；命令堆叠过快导致未知命令。
- 测试点：动态块；文档未连接；对象无 Document。

### set_attribute_mtext(block, tags, new_texts, keep_prefix=True, verbose=True)
- 作用：批量设置块属性值，支持多行文本（\P）与保留格式前缀。
- 关键步骤：
  1) 标准化 tags 与 new_texts；
  2) GetAttributes 建立 tag->attr 映射；
  3) 处理多行内容，必要时开启 MTextAttribute；
  4) set_attr(TextString) 更新并 Update。
- 输入/输出：返回 dict {tag: bool}。
- 依赖/副作用：修改块属性；可能改变 MText 模式。
- 风险：标签不存在；MTextAttribute 设置失败；编码/特殊符号。
- 测试点：单标签/多标签；多行列表；keep_prefix 前缀保留。

### get_block_attributes_dict(block_ref, ignore_empty=False, upper_tag=True)
- 作用：读取块属性并清洗 MTEXT 前缀（如 \W0.8;）。
- 关键步骤：校验块引用与 HasAttributes -> GetAttributes -> TagString/TextString -> 清洗。
- 输入/输出：返回 {tag: value} 字典。
- 风险：非 BlockReference；属性读取异常；分号清洗误伤。
- 测试点：无属性块；动态块；包含格式前缀。

### insert_and_explode_dwg(block_dwg, insertion_point=(0,0,0), scale=(1,1,1), rotation=0, wait=0.3)
- 作用：插入 DWG 块并炸开，返回新增块与包围盒角点；后定义版本（V3.0）生效。
- 关键步骤：
  1) 记录插入前块句柄；
  2) -INSERT 命令插入；
  3) EXPLODE Last；
  4) diff 计算新块；
  5) SafeCOM 获取包围盒，归零旋转。
- 返回：([ (blk, corners), ... ], last_blk)
- 副作用：插入/炸开实体；改变模型空间对象。
- 风险：炸开失败无新块；CADGuard 与 SendCommand 时序；路径不存在。
- 测试点：不存在 DWG；重复插入；CAD 忙碌。

### create_block_from_region_cmd(x1,y1,x2,y2, insert_point_option="左下", block_name_prefix="块", base_point=None, ty=1.0)
- 作用：通过 -BLOCK 命令按矩形区域创建块（保留天正对象），并插入块实例。
- 关键步骤：
  1) SelectionSet.Window 选择区域对象（SafeCOM list）；
  2) group_bbox_corners 计算基点；
  3) 生成唯一块名；
  4) -BLOCK W 窗口创建定义；
  5) InsertBlock 插入实例；
  6) 删除原对象残留。
- 返回：IAcadBlockReference 或 None。
- 副作用：删除区域内对象并替换为块实例。
- 风险：选择集为空；CMDACTIVE 忙碌；误删对象。
- 测试点：空区域；base_point 指定；天正对象存在。

### create_block_from_list_cmd(entities, insert_point_option="左下", block_name_prefix="块", base_point=None, ty=0.5)
- 作用：通过 LISP 选择集将任意对象列表封装为块。
- 关键步骤：
  1) ensure_list 预处理；
  2) group_bbox_corners 计算基点；
  3) 生成唯一块名；
  4) 将 Handle 批量 ssadd -> -BLOCK 覆盖创建块；
  5) InsertBlock 插入实例。
- 返回：IAcadBlockReference 或 None。
- 副作用：块定义创建；原对象可能被块化删除。
- 风险：Handle 无效；LISP 选择集为空；命令堆叠。
- 测试点：空列表；含天正对象；大量对象。

### add_entities_to_block_definition_explode(block_ref, new_entities, ty=0.5)
- 作用：追加对象到块定义（不清除原块对象），通过 Explode + -BLOCK 覆盖重定义。
- 关键步骤：
  1) Explode 原块生成图元；
  2) 合并 new_entities 与 exploded_list；
  3) LISP 选择集 -> -BLOCK 覆盖；
  4) Regen + Update。
- 返回：bool。
- 副作用：重定义块，模型空间对象会被吸入块定义。
- 风险：Explode 失败；LISP 选择集失败；重定义覆盖错误块名。
- 测试点：动态块/匿名块；追加对象为空；CMDACTIVE 忙碌。

### explode_single_object_marker(ent)
- 作用：炸开单个对象，并通过“辅助线回溯”收集新碎片。
- 关键步骤：
  1) 绘制 marker 线；
  2) set_entity_grip_state_precise 选中目标；
  3) SendCommand EXPLODE；
  4) 逆序遍历 ModelSpace 到 marker；
  5) 删除 marker。
- 返回：炸开碎片列表。
- 风险：选择失败导致无炸开；marker 未删除；模型空间顺序变化。
- 测试点：ent 为 None；爆炸生成大量对象；CAD 忙碌。

### update_block_def_attributes_v7(block_ref_or_name, target_tag, ...)
- 作用：修改块定义中的属性定义（高度/对正/宽度因子/旋转/MText 边界等）。
- 关键步骤：
  1) 解析块名（EffectiveName/Name）；遍历块定义锁定目标 Tag；  
  2) 先设置 Alignment（避免 MText 开启后锁死对正）；  
  3) 设置样式/高度/宽度因子/旋转；  
  4) 如设置 boundary_width 则启用 MText，并在对齐点或插入点基础上 Move 对齐。
- 输出：bool（是否发生变化）。
- 副作用：修改块定义属性；影响所有块实例显示。
- 风险：Tag 未找到；Alignment/MText 顺序错误导致报错。
- 测试点：动态块；Tag 不存在；对齐点移动。

### get_bounding_box_of_block(block_name)
- 作用：计算块定义的整体包围盒。
- 关键步骤：遍历块定义内对象 GetBoundingBox，聚合 min/max。
- 输出：((minx,miny,minz),(maxx,maxy,maxz))。
- 风险：对象无 BoundingBox 被跳过，可能低估范围。
- 测试点：空块；含无边界对象。

### delete_block_instances_and_definition_optimized(target_name, max_retries=5)
- 作用：删除指定块的所有实例与定义（文件内有多版定义，最后版本生效）。
- 关键步骤：
  1) SelectionSet 过滤 INSERT + 块名，Erase 实例；  
  2) 尝试删除 Blocks 表中的定义；  
  3) 反查 Blocks.Item 验尸，失败则 Regen+重试。
- 输出：bool。
- 副作用：删除实例与块定义。
- 风险：嵌套引用导致定义无法删除；选择集残留。
- 测试点：块不存在；被嵌套引用；大量实例。

### insert_standard_block(block_dwg, insertion_point=(0,0,0), scale=(1,1,1), rotation=0, wait=0.3)
- 作用：命令式插入标准块（不炸开），返回新插入块及包围盒。
- 关键步骤：记录插入前块句柄 -> -INSERT 命令 -> Regen/ZE -> 计算新块差集 -> 归零旋转并取 BoundingBox。
- 输出：[(blk_ref, corners), ...]。
- 副作用：插入块引用；发送命令；刷新视图。
- 风险：文件不存在；命令时序导致未检测到新块。
- 测试点：重复插入；路径含空格；rotation 非 0。

### add_entities_to_block_direct(block_ref, entities, delete_original=True)
- 作用：将外部实体复制进块定义，并逆向变换回块局部坐标。
- 关键步骤：
  1) CopyObjects(entities -> block_def)；  
  2) 使用 block_ref 的插入点/旋转/比例进行逆变换（Move/Rotate/Scale）；  
  3) 可选删除原实体；Update 块引用。
- 输出：bool。
- 副作用：修改块定义；可能删除原对象。
- 风险：CopyObjects 返回结构不稳定；逆变换点类型需 Variant。
- 测试点：动态块；非统一比例；delete_original=False。

### extract_specific_entities_from_block(block_ref, mode='all', keep_in_block=True)
- 作用：从块中提取指定类型对象（文字/块/多段线/全部）。
- 关键步骤：
  1) Explode 生成副本；  
  2) 按 ObjectName 过滤，非目标即删除；  
  3) keep_in_block=False 时，从块定义内删除对应对象并 Update/Regen。
- 输出：提取对象列表（位于模型空间）。
- 副作用：炸开产生临时对象；可修改块定义。
- 风险：MInsertBlock 不支持；all+keep_in_block=False 风险较高。
- 测试点：mode=text/block/polyline；keep_in_block=False。

### _atomic_explode_and_delete(block_entity)
- 作用：原子炸开+删除（带 retry_on_busy）。
- 关键步骤：Explode -> wait_quiescent -> Delete。
- 输出：Explode 返回对象列表。
- 风险：对象锁定导致失败；等待不足。
- 测试点：天正对象；CAD 忙碌。

### safe_explode_retry(entity, max_retries=5, rescue_retries=5, interval=1.0, verbose=True)
- 作用：带“深度搜救”的炸开，保证对象消失即视为成功。
- 关键步骤：
  1) _atomic_explode_and_delete；若有返回直接成功；  
  2) 若无返回但对象已消失，则通过 owner_space.Count 增量扫描搜救新对象；  
  3) 重试至成功；对象仍存活则返回 None。
- 输出：list/[] 表示成功，None 表示失败。
- 副作用：可能 Regen；等待 CAD 同步。
- 风险：搜救索引假设失败；对象已删除但无新对象时返回空列表。
- 测试点：Explode 返回空；对象已删除；CAD 忙碌。

## library/cad_control.py

### fix_com_cache()
- 作用：清理 win32com 的 gen_py 缓存，修复 COM 接口损坏/AttributeError。
- 关键步骤：定位 gen_py 路径（win32com.__gen_path__ 或 gencache）；rmtree 删除；再扫描 site-packages/win32com/gen_py 并清理。
- 输入/输出：无输入；无返回（打印日志）。
- 副作用：删除缓存文件夹；需要重启 Python/AutoCAD 以重建缓存。
- 风险：权限不足导致清理失败；删除系统级缓存需管理员权限。
- 测试点：存在损坏缓存；无缓存路径；只读目录。

### shitu_region(x1, y1, x2, y2)
- 作用：按区域外包盒缩放视图。
- 关键步骤：计算 margin h=0.3*(dx+dy)/2；构造 ZOOM Window 命令并 SendCommand。
- 副作用：改变当前视图缩放。
- 风险：输入坐标异常导致缩放错位；CAD 忙碌。
- 测试点：极小/极大区域；反向坐标。

### shitu_entity(obj)
- 作用：按对象外包盒缩放视图。
- 关键步骤：GetBoundingBox -> 计算 margin -> 发送 ZOOM Window 命令。
- 副作用：改变当前视图缩放。
- 风险：对象无 BoundingBox；COM 异常。
- 测试点：无效对象；极细长对象。

### set_current_dimstyle_via_command(style_name="_TCH_ARCH")
- 作用：通过命令行设置当前标注样式（兼容天正）。
- 关键步骤：SendCommand("-DIMSTYLE\nR\n{style_name}\n")。
- 副作用：改变当前标注样式；进入命令栈。
- 风险：样式不存在时命令失败。
- 测试点：样式存在/不存在；CAD 忙碌。

### rename_conflicting_text_styles(file1_path, file2_path, suffix="_1", ...)
- 作用：找出两个 DWG 中同名的用户文字样式，并在 file1 中改名+更新实体引用。
- 关键步骤：
  1) 打开两个 DWG；收集 TextStyles 名称，排除系统样式；  
  2) 对冲突样式执行 -RENAME 命令，等待样式表更新；  
  3) 遍历 ModelSpace，将 Text/MText/TDbText/TDbMText 的旧样式替换为新样式；  
  4) 保存 file1，关闭两个文件（file2 不保存）。
- 输出：无显式返回。
- 副作用：修改 file1 文字样式与实体属性；保存文件。
- 风险：重命名未生效导致样式残留；处理大文件遍历慢。
- 测试点：冲突样式不存在；同名样式多次冲突；TDb* 对象。

### transfer_props_by_matchprop(entity, Ob, max_try=3, delay=0.4)
- 作用：用 MATCHPROP 将源对象属性批量复制到目标对象（重试直到 Layer 变化）。
- 关键步骤：
  1) 选择源对象为 Previous（优先 highlight_entity_by_bbox；失败则用 Handle LISP 选择）；  
  2) 对目标对象扩展窗口范围，发送 MATCHPROP P + Window；  
  3) 轮询 Ob.Layer 是否变为源图层，失败则重试。
- 输出：bool。
- 副作用：改变目标对象属性；发命令并依赖当前选择集。
- 风险：命令栈干扰导致 Previous 失效；目标 Layer 未变化误判失败。
- 测试点：源/目标同层；highlight_entity_by_bbox 失败；CAD 忙碌。

### srhd(*args)
- 作用：在模型空间绘制点并标注序号（测试辅助）。
- 关键步骤：确保“测试辅助”图层存在；解析输入点列表；AddPoint+AddText 编号。
- 输出：字符串提示。
- 副作用：创建图层并添加点/文字对象。
- 风险：输入格式异常；图层锁定。
- 测试点：单点/多点/列表输入；非数值坐标。

### srhd_p(*args)
- 作用：在图纸空间绘制点并标注序号（测试辅助）。
- 关键步骤：同 srhd，但写入 PaperSpace。
- 输出：字符串提示。
- 副作用：创建图层并添加点/文字对象到图纸空间。
- 风险：布局空间锁定；输入格式异常。
- 测试点：单点/多点/列表输入。

## library/cad_geometry.py

### get_spline_length_by_conversion(spline_entity)
- 作用：通过 SPLINEDIT 将样条转为多段线来估算长度。
- 关键步骤：复制样条 -> highlight_entity_by_bbox -> SendCommand _SPLINEDIT P -> 等待 -> 取 ModelSpace 最后对象 Length -> 删除临时多段线。
- 输出：float 或 None。
- 副作用：发送命令、添加并删除临时对象。
- 风险：命令时序导致最后对象非目标；CAD 忙碌。
- 测试点：无效样条；复杂样条；Length 属性缺失。

### find_fake_intersection_regions(lines, tol=10, real_tol=0.01)
- 作用：查找“伪相交点”（端点靠近线但未真正相交），并绘制标记圆。
- 关键步骤：对每条线端点计算到其他线的点线距离；若 < tol 且 >= real_tol 则为伪交点；在“测试辅助”图层画半径 1000 圆。
- 副作用：绘制辅助圆；确保图层存在。
- 风险：O(n^2) 对大集合较慢；容差误判。
- 测试点：密集线段；真实交点；重复端点。

### lines_daduan(start_point, end_point)
- 作用：调用天正 tlinebk 命令打断线段。
- 关键步骤：拼接命令字符串（含三维坐标）并 SendCommand。
- 副作用：修改几何；进入命令栈。
- 风险：命令不可用/被劫持；坐标格式错误。
- 测试点：三维坐标；天正未安装。

### delete_duplicate_lines(lines, tol=0.01)
- 作用：删除完全重复的线段（端点相同或反向相同）。
- 关键步骤：两两对比端点（容差）；保留首条，删除重复。
- 输出：保留的线段列表。
- 副作用：删除实体。
- 风险：容差过大误删；非 AcDbLine 输入。
- 测试点：反向线段；重合多条。

### delete_redundant_lines(lines, tol=0.01)
- 作用：删除完全重复或局部重叠的冗余线段。
- 关键步骤：判断完全重复或“短线段完全落在长线段上”；按 Handle 删除冗余。
- 输出：None（日志提示）。
- 副作用：删除实体。
- 风险：浮点容差导致误删；输入含非共线线段。
- 测试点：共线重叠；部分重叠；独立线段。

### get_room_outline_from_point(x, y, z=0)
- 作用：从内点触发 TSpOutline 命令获取房间轮廓。
- 关键步骤：构造命令 "TSpOutline" + 点坐标 + 回车确认。
- 副作用：生成轮廓对象；进入命令栈。
- 风险：命令不存在；点不在封闭区域。
- 测试点：不同房间封闭边界；非法点。

### draw_polyline(vertices, layer_name="tuqian_baobu", tol=0.5, width=50, color=256, target_space=None)
- 作用：绘制轻量多段线（V3，支持指定容器）。
- 关键步骤：选择绘制容器（target_space 或 ActiveLayout.Block/ModelSpace）；展平坐标并 AddLightWeightPolyline；设置 Layer/Color/Closed/Width。
- 输出：多段线对象或 None。
- 副作用：添加实体。
- 风险：坐标格式错误；C.doc 未初始化。
- 测试点：闭合/非闭合；目标容器为 Block；空点列表。

### TDbMText_content(comobj, separator="\\n")
- 作用：提取天正多行文字内容（复制+炸开+排序+重组）。
- 关键步骤：复制对象 -> explode_single_object_marker -> 按 Y 分桶、X 排序 -> 行变更插入 separator -> 清理碎片。
- 输出：字符串。
- 副作用：创建/删除临时碎片；依赖 li() 环境连接。
- 风险：炸开失败导致空文本；排序容差不适配。
- 测试点：多行/单行；含格式化字符；爆炸后无 TextString。

## library/tarch_building.py

### activate_cad_middle_click(hwnd)
- 作用：通过中键点击激活 CAD 窗口（物理操作）。
- 关键步骤：还原窗口 -> SetForegroundWindow -> 取窗口中心 -> pyautogui 中键点击。
- 输出：bool。
- 副作用：抢占焦点/鼠标位置；影响用户操作。
- 风险：窗口句柄无效；后台限制前置失败。
- 测试点：最小化窗口；多显示器；无窗口句柄。

### _activate_cad_safe(hwnd)
- 作用：内部版窗口激活，逻辑与 activate_cad_middle_click 类似。
- 关键步骤：还原窗口 -> SetForegroundWindow -> 中键点击中心点。
- 输出：bool。
- 副作用：抢焦点；移动鼠标。
- 风险：与用户操作冲突。
- 测试点：窗口不可见；权限限制。

## library/cad_objects.py

### add_objects_to_group(group_name, obj_list)
- 作用：将一批对象加入指定组（不存在则新建）。
- 关键步骤：doc.Groups.Item 取组 -> 不存在则 Add -> AppendItems(vtlist(obj_list))。
- 输出：Group 对象。
- 副作用：修改组内容。
- 风险：组名冲突；对象无效导致 Append 失败。
- 测试点：空列表；组已存在/不存在。

### copy_group_S1_from_doc1_to_doc2(doc1, doc2, group_name="S1")
- 作用：将 doc1 中指定组复制到 doc2 并重建组关系。
- 关键步骤：
  1) 激活 doc1，收集组内 Handle 对应对象；  
  2) 用复制粘贴命令（_copybase/_copyclip）复制；  
  3) 激活 doc2，记录粘贴前后 Handle 差集；  
  4) 将新对象加入同名组。
- 副作用：切换活动文档；执行剪贴板操作；新增组对象。
- 风险：剪贴板干扰；Handle 差集不稳定；组不存在报错。
- 测试点：组名不存在；多文档并行；空组。

### sc_objs_to_layer(layer_name, cl=256)
- 作用：屏幕交互选择对象并统一设置图层与颜色。
- 关键步骤：SelectionSets.SelectOnScreen -> 创建/获取图层 -> 设置 Layer/Color。
- 输出：所选对象列表。
- 副作用：弹出选择交互；修改对象图层和颜色。
- 风险：选择集残留；用户取消选择返回空。
- 测试点：图层不存在；颜色修改失败；无对象选择。

### create_layers_from_list(layer_names)
- 作用：批量创建图层（已存在则跳过）。
- 关键步骤：get_acad_doc -> doc.Layers -> 遍历 Item/ Add；统计创建/跳过数。
- 输出：None（日志提示）。
- 副作用：新增图层。
- 风险：CAD 未连接；图层名非法。
- 测试点：重复名称；空列表。

### dim_by_points(*args)
- 作用：通过天正 zdbz 命令对三点进行逐点标注。
- 关键步骤：最小化窗口 -> 激活 AutoCAD -> SendCommand zdbz + 三点坐标。
- 输出：bool。
- 副作用：操作窗口焦点；进入命令栈；生成标注。
- 风险：窗口激活失败；参数不足。
- 测试点：三点坐标；CAD 未就绪。

### ensure_layer_model_only(layer_name="jizhunwall")
- 作用：仅清理模型空间中的指定图层对象（保留图纸空间）。
- 关键步骤：获取/创建图层并设为当前层；select_tuceng 拉取对象；用 get_obj_loc 判定模型空间删除；重复尝试+刷新。
- 输出：None（日志提示）。
- 副作用：删除模型空间对象；切换当前图层。
- 风险：get_obj_loc 判定失误导致误删；对象锁定删除失败。
- 测试点：仅图纸空间对象；混合空间对象。

### force_layer_objects_color(layer_name, target_color=256, max_retries=3)
- 作用：强制将图层内对象改为指定颜色，带重试与“读不到颜色也算成功”的容错。
- 关键步骤：stc 选层对象 -> set_attr(color) -> obj.Update -> 读取 Color 验证；失败重试。
- 输出：bool（True/False）。
- 副作用：修改对象颜色。
- 风险：读取 Color 为 None 时信任写入可能掩盖失败；对象锁定。
- 测试点：空图层；颜色读回失败；多次重试。


## scripts/Insert_chart/insert_labels.py

### get_block_true_name(blk_obj)
- 作用：统一获取块“真实名称”。
- 关键步骤：优先取 Name（代码如此），若为空再取 EffectiveName；与注释“先 EffectiveName”存在轻微不一致。
- 输入/输出：输入块对象；输出字符串或 None。
- 依赖/副作用：依赖 get_attr；无副作用。
- 风险：动态块 Name/EffectiveName 可能为空或无属性。
- 测试点：普通块/动态块/匿名块。

### filter_blocks_by_list(all_blocks=None, target_names=Block_Names_0)
- 作用：从块实例中过滤指定块名集合。
- 关键步骤：缺省时调用 select_kuai 获取全体块；将 target_names 变集合；遍历 get_block_true_name 并筛选。
- 输入/输出：输入块列表与名字清单；输出命中的块列表。
- 副作用：打印筛选统计信息。
- 风险：select_kuai 返回异常或过慢；Name/EffectiveName 获取失败导致漏检。
- 测试点：空列表；含动态块；target_names 较大集合。

### block_name_from_spec(spec_str: str)
- 作用：将规格字符串（如 A1+1/4）规范为块名键。
- 关键步骤：剥空、直接识别 A0/A1/A2/A3；其余将 “+” “/” 替换为 “_”。
- 输入/输出：输入规格字符串；输出块名或 None。
- 风险：规格格式非预期（如小写、空白）导致 None。
- 测试点：标准规格、复合规格、空值。

### compute_k_from_info(info: dict) -> float
- 作用：根据 frame_info 估算几何修正因子 k_geom（模板 1:100 基准）。
- 关键步骤：
  1) 由 corners 或 entity BoundingBox 得到实际宽高；
  2) 解析 drawing_frame 中的纸张尺寸（mm）；
  3) 解析 ratio（1:n），算名义宽高 = mm * n；
  4) k = 平均(实际宽高 / 名义宽高)。
- 输入/输出：输入 frame_info；输出 k（默认 1.0）。
- 风险：drawing_frame/ratio 解析失败；corners 为空或顺序异常。
- 测试点：有 corners/无 corners；ratio 缺失；drawing_frame 无尺寸字符串。

### compute_insert_factors(entities, res, result_dict)
- 作用：根据识别规格与模板信息推算插入缩放系数 k。
- 关键步骤：
  1) 从 result_dict 构建 spec -> (block_name, ratio)；
  2) 对每个实体匹配 res 中的 spec/ratio；
  3) 解析比例分母 d1/d2 得出 k = d1 / d2。
- 输出：[(entity, block_name, spec, k), ...]。
- 风险：spec 未命中导致 block_name/k 为空；ratio 格式不符合 “1:n”。
- 测试点：spec 缺失；ratio 为 None；d2=0。

### adjust_block_to_frame(frame_ent, blk_com, tol_len=10.0)
- 作用：在统一缩放后做二次校正，使图签块外包盒更贴合图框。
- 关键步骤：
  1) 读取框/块 BoundingBox 宽高；
  2) 若差值在 tol_len 内则跳过；
  3) 根据旋转角 0/90 推算 X/Y 方向缩放因子；
  4) 设置 XScaleFactor/YScaleFactor。
- 副作用：修改块缩放；可能改变图签比例。
- 风险：BoundingBox 获取失败；Rotation 角度非 0/90 走均值回退。
- 测试点：横向/竖向块；极端比例图框；tol 边界。

### insert_and_scale_labels_area_any(coms_dayin=None, filepath=...)
- 作用：批量插入图签到图框区域，按规格信号匹配并缩放对齐（多版本迭代，最终为 V9.3）。
- 关键步骤（V9.3 最终版）：
  1) 窗口处理：最小化、激活 AutoCAD；初始化统计/日志变量；
  2) 预计算：无 coms_dayin 则 select_maxrect_polylines_1；去重、排序；计算动态识别容差；
  3) 识别：generate_name_and_ratio_from_com 得到 spec/ratio/drawing_frame；
  4) 事务：CADGuard 内 Insert_Company_Label_Common_Block 导入模板并炸开；
  5) 同步审计：wait_quiescent + Regen，多轮重试锁定 12 个真实块名（checkpoint）；
  6) 分发：按 spec→真实块名映射插入；compute_k_from_info 估算 k；adjust_block_to_frame 校正；
  7) 清理与收尾：删除模板实例，保存 DWG；finally 记录 record_test_result。
- 输入/输出：输入多段线列表或自动识别；输出 bind_dict（块 Handle -> frame_info/title_block）。
- 依赖/副作用：大量 COM 操作；窗口焦点切换；写日志/Excel；保存 DWG。
- 风险：块名审计不足 (<12) 直接抛错；窗口激活失败；CAD 忙碌导致点名失败。
- 测试点：无多段线；模板路径错误；不同规格信号；重试超时。

### normalize_core_title_blocks_by_layer_new1(core_layer="dy_quyu_H", core_base_names=None, verbose=True)
- 作用：将图签“壳块”炸开为内核块（-H），并重命名原块定义（多版本迭代，最终为 V3.2）。
- 关键步骤（V3.2 最终版）：
  1) 事务级重试（MAX_RETRIES=3），每次在 CADGuard 内执行；
  2) 扫描块实例（select_kuai + SelectionSet 回退），锁定壳块；
  3) 对每个壳块执行 safe_explode_retry（炸开+验证），记录失败警告；
  4) wait_quiescent + Regen 后审计：核块数 >= 初始数量且壳块为 0；checkpoint 记录；
  5) 成功则重命名块定义（时间戳 + 冲突规避），失败则抛异常触发回滚与重试。
- 输出：bool。
- 副作用：删除块实例；重命名块定义；写审计 checkpoint。
- 风险：safe_explode_retry 失败导致回滚；审计条件过严；命名冲突。
- 测试点：无目标块；CAD 忙碌；核块数量不足或壳块残留。

### run_title_block_assembly_pipeline(external_coms=None, external_filepath=None)
- 作用：图签总装流水线（最终版本有参/无参兼容）。
- 关键步骤：
  1) 数据源：外部 coms / 交互选择；外部路径 / 默认标准图签路径；
  2) Phase1：调用 insert_and_scale_labels_area_any，记录插入数量；
  3) Bridge：wait_quiescent + Regen 稳定数据库；
  4) Phase2：调用 normalize_core_title_blocks_by_layer_new1（目标壳块清单）；
  5) CriticalSection 记录阶段状态与人工提示。
- 输出：bool。
- 副作用：插入/炸开/重命名块定义；写日志。
- 风险：Phase1 返回 0 即终止；等待不足导致后续审计失败。
- 测试点：外部参数为空；交互选择为空；CAD 忙碌时的阶段切换。

### run_full_project_workflow()
- 作用：旗舰级入口，封装总装流水线并记录阶段状态。
- 关键步骤：CriticalSection 下调用 run_title_block_assembly_pipeline，失败即抛异常；预留后续步骤。
- 输出：无显式返回（异常表示失败）。
- 副作用：执行整套图签流程；记录日志。
- 风险：流水线失败导致异常中断。
- 测试点：流水线失败场景；CriticalSection 是否写入记录。

