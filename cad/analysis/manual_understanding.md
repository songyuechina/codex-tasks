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


## scripts/CAD_basic.py (块重定义)

### redefine_block_with_entities(block_ref, entities, ty=0.5, debug_log_path="C:\\cad_debug_log.txt")
- 说明：与 `library/cad_blocks.py::redefine_block_with_entities` 基本一致，为调试版重定义块内容（使用 -BLOCK 覆盖）。
- 依赖/副作用：同库版本（LISP 选择集 + -BLOCK 覆盖 + Regen）。
- 风险/测试点：同库版本；注意该函数在 CAD_basic 中重复定义来源。

