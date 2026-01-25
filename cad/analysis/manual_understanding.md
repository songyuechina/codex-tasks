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

