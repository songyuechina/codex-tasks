# CAD 脚本函数级理解记录（自动生成初稿）

说明：本文件基于 AST + 关键字启发式生成，为每个函数提供初步理解、风险与测试点。
后续将结合逐函数深读进行修订与细化。

## library/cad_annotation.py
- 模块说明: CAD注释与文字函数库
### vtpnt(x, y, z)
- 说明: 将三维坐标转换为VARIANT类型
- 邻近注释: ================= 辅助函数 =================
- 参数: x, y, z
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于处理相关逻辑。依据注释：将三维坐标转换为VARIANT类型。邻近注释提示：================= 辅助函数 =================。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### write_cad_text(text_content, insertion_point, height, rotation, style, layer_name, color_index)
- 说明: 在CAD中写入单行文字
- 邻近注释: &&&&%% 注释文字模块 | &&&% 单行文字操作
- 参数: text_content, insertion_point, height, rotation, style, layer_name, color_index
- 返回: 新创建的文字对象；失败时返回 None
- 关注点: 文件, 日志/测试
- 调用概览: AddText, str, vtpnt, info
- 理解: 主要用于保存/写入相关逻辑。依据注释：在CAD中写入单行文字。邻近注释提示：&&&&%% 注释文字模块；&&&% 单行文字操作。实现特征：创建文字对象。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### write_mtext(text_content, insertion_point, width, height, attachment_point, layer_name)
- 说明: 在CAD中写入多行文字
- 邻近注释: &&&% 多行文字操作
- 参数: text_content, insertion_point, width, height, attachment_point, layer_name
- 返回: 新创建的多行文字对象；失败时返回 None
- 关注点: 几何, 文件, 日志/测试
- 调用概览: AddMText, vtpnt, str, info
- 理解: 主要用于保存/写入相关逻辑。依据注释：在CAD中写入多行文字。邻近注释提示：&&&% 多行文字操作。实现特征：创建文字对象。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### add_dim_aligned(p1, p2, p3)
- 说明: 添加对齐标注
- 邻近注释: &&&% 标注操作 | &&% 对齐标注
- 参数: p1, p2, p3
- 返回: 新创建的标注对象；失败时返回 None
- 关注点: 日志/测试
- 调用概览: AddDimAligned, vtpnt, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：添加对齐标注。邻近注释提示：&&&% 标注操作；&&% 对齐标注。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### add_dim_rotated(p1, p2, p3, angle)
- 说明: 添加旋转标注
- 邻近注释: &&% 旋转标注
- 参数: p1, p2, p3, angle
- 返回: 新创建的标注对象；失败时返回 None
- 关注点: 几何, 日志/测试
- 调用概览: AddDimRotated, vtpnt, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：添加旋转标注。邻近注释提示：&&% 旋转标注。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### add_dim_angular(vertex, p1, p2, p3)
- 说明: 【新增】添加角度标注
- 邻近注释: &&% 角度标注
- 参数: vertex, p1, p2, p3
- 返回: 标注对象
- 关注点: 日志/测试
- 调用概览: AddDimAngular, vtpnt, error
- 理解: 主要用于创建/插入相关逻辑。依据注释：【新增】添加角度标注。邻近注释提示：&&% 角度标注。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### add_dim_radial(center, chord_point, leader_length)
- 说明: 【新增】添加半径标注
- 邻近注释: &&% 半径标注
- 参数: center, chord_point, leader_length
- 返回: 标注对象
- 关注点: 日志/测试
- 调用概览: AddDimRadial, vtpnt, error
- 理解: 主要用于创建/插入相关逻辑。依据注释：【新增】添加半径标注。邻近注释提示：&&% 半径标注。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### add_dim_diametric(chord_point, far_chord_point, leader_length)
- 说明: 【新增】添加直径标注
- 邻近注释: &&% 直径标注
- 参数: chord_point, far_chord_point, leader_length
- 返回: 标注对象
- 关注点: 日志/测试
- 调用概览: AddDimDiametric, vtpnt, error
- 理解: 主要用于创建/插入相关逻辑。依据注释：【新增】添加直径标注。邻近注释提示：&&% 直径标注。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### add_leader(points, annotation)
- 说明: 添加引线
- 邻近注释: &&&% 引线操作 | &&% 添加引线
- 参数: points, annotation
- 返回: 新创建的引线对象；失败时返回 None
- 关注点: COM, 日志/测试
- 调用概览: VARIANT, AddLeader, extend, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：添加引线。邻近注释提示：&&&% 引线操作；&&% 添加引线。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_text_content(text_obj)
- 说明: 获取文字对象的内容
- 参数: text_obj
- 返回: 文字内容字符串；失败时返回 None
- 关注点: 日志/测试
- 调用概览: info
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取文字对象的内容。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_text_content(text_obj, new_content)
- 说明: 设置文字对象的内容
- 参数: text_obj, new_content
- 返回: 成功返回 True，失败返回 False
- 关注点: 日志/测试
- 调用概览: str, info
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置文字对象的内容。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_text_height(text_obj)
- 说明: 获取文字高度
- 参数: text_obj
- 返回: 文字高度；失败时返回 None
- 关注点: 日志/测试
- 调用概览: info
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取文字高度。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_text_height(text_obj, height)
- 说明: 设置文字高度
- 参数: text_obj, height
- 返回: 成功返回 True，失败返回 False
- 关注点: 日志/测试
- 调用概览: info
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置文字高度。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_text_rotation(text_obj)
- 说明: 【新增】获取文字旋转角度
- 邻近注释: &&&% 文字查询与修改 | &&% 获取文字旋转角度
- 参数: text_obj
- 返回: 旋转角度(弧度)
- 关注点: 日志/测试
- 调用概览: error
- 理解: 主要用于获取/选择相关逻辑。依据注释：【新增】获取文字旋转角度。邻近注释提示：&&&% 文字查询与修改；&&% 获取文字旋转角度。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_text_rotation(text_obj, rotation)
- 说明: 【新增】设置文字旋转角度
- 邻近注释: &&% 设置文字旋转角度
- 参数: text_obj, rotation
- 返回: 成功返回True
- 关注点: 日志/测试
- 调用概览: error
- 理解: 主要用于更新/设置相关逻辑。依据注释：【新增】设置文字旋转角度。邻近注释提示：&&% 设置文字旋转角度。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### batch_modify_text(text_objs, **kwargs)
- 说明: 【新增】批量修改文字属性
- 邻近注释: &&% 批量修改文字
- 参数: text_objs, **kwargs
- 返回: 成功修改的数量
- 关注点: 日志/测试
- 调用概览: set_text_height, set_text_rotation, set_text_content, error
- 理解: 主要用于更新/设置相关逻辑。依据注释：【新增】批量修改文字属性。邻近注释提示：&&% 批量修改文字。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### create_table(insertion_point, rows, cols, row_height, col_width)
- 说明: 【新增】创建表格
- 邻近注释: &&&% 表格操作 | &&% 创建表格
- 参数: insertion_point, rows, cols, row_height, col_width
- 返回: 表格对象
- 关注点: 日志/测试
- 调用概览: AddTable, vtpnt, error
- 理解: 主要用于创建/插入相关逻辑。依据注释：【新增】创建表格。邻近注释提示：&&&% 表格操作；&&% 创建表格。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_table_cell_text(table_obj, row, col, text)
- 说明: 【新增】设置表格单元格文字
- 邻近注释: &&% 设置表格单元格文字
- 参数: table_obj, row, col, text
- 返回: 成功返回True
- 关注点: 日志/测试
- 调用概览: SetText, str, error
- 理解: 主要用于更新/设置相关逻辑。依据注释：【新增】设置表格单元格文字。邻近注释提示：&&% 设置表格单元格文字。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_table_cell_text(table_obj, row, col)
- 说明: 【新增】获取表格单元格文字
- 邻近注释: &&% 获取表格单元格文字
- 参数: table_obj, row, col
- 返回: 单元格文字内容
- 关注点: 日志/测试
- 调用概览: GetText, error
- 理解: 主要用于获取/选择相关逻辑。依据注释：【新增】获取表格单元格文字。邻近注释提示：&&% 获取表格单元格文字。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## library/cad_blocks.py
- 模块说明: 第六部分 图块操作
### get_block_name(obj)
- 说明: 获取块名，兼容动态块(EffectiveName)
- 邻近注释: &&&% 原块处理 | &&&% 块属性 | &&% 获取块实例块名
- 参数: obj
- 返回推断: object
- 调用概览: getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取块名，兼容动态块(EffectiveName)。邻近注释提示：&&&% 原块处理；&&&% 块属性；&&% 获取块实例块名。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### huoqukuai_shuxing_zhi(XX)
- 说明: （无）
- 邻近注释: &&% 获取块属性值
- 参数: XX
- 返回推断: tuple
- 调用概览: GetAttributes, append
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 获取块属性值。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### update_block_def_attributes_safe(block_ref_or_name, target_tag)
- 说明: 【函数编号】: BLK-007-Safe
- 邻近注释: &&% 属性块标签编辑
- 参数: block_ref_or_name, target_tag
- 返回推断: bool
- 关注点: 几何, 文件, 日志/测试
- 关键调用: C.doc
- 调用概览: isinstance, get_attr, info, Item, cast_object, set_attr, print, int, str, float, len, globals...
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: BLK-007-Safe。邻近注释提示：&&% 属性块标签编辑。实现特征：涉及块定义/块实例操作。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### update_block_def_attributes_v7(block_ref_or_name, target_tag)
- 说明: 【函数编号】: BLK-007
- 参数: block_ref_or_name, target_tag
- 返回推断: bool
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.li
- 调用概览: li, isinstance, info, Item, str, float, vtpnt, Move, print, CastTo, int, len...
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: BLK-007。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### attsync_block_instance(block_ref_obj)
- 说明: 【函数编号】: CMD-001
- 邻近注释: &&% 属性块标签编辑生效
- 参数: block_ref_obj
- 返回推断: object
- 关注点: 日志/测试, 时间/等待
- 调用概览: info, range, get_attr, attsync_block_instance_base, sleep
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: CMD-001。邻近注释提示：&&% 属性块标签编辑生效。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### attsync_block_instance_base(block_ref_obj)
- 说明: 【函数编号】: CMD-001
- 参数: block_ref_obj
- 返回推断: bool
- 关注点: COM, 日志/测试
- 关键调用: C.li, C.doc
- 调用概览: li, hasattr, info, getattr, print, SendCommand
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: CMD-001。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_attribute_mtext(block, tags, new_texts, keep_prefix, verbose)
- 说明: set_attribute_mtext(p[0],"图纸规格","A0")
- 邻近注释: &&% 设置属性块的标签值
- 参数: block, tags, new_texts, keep_prefix, verbose
- 返回推断: object
- 关注点: COM, 日志/测试, 进程
- 关键调用: C.li
- 调用概览: li, isinstance, cast_object, zip, list, GetAttributes, get_attr, Update, get, set_attr, len, extend...
- 理解: 主要用于更新/设置相关逻辑。依据注释：set_attribute_mtext(p[0],"图纸规格","A0")。邻近注释提示：&&% 设置属性块的标签值。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_block_attributes_dict(block_ref, ignore_empty, upper_tag)
- 说明: 获取块参照 block_ref 的所有属性，返回 {标签: 纯文本值} 的字典。
- 邻近注释: &&% 获取属性块标签及标签值
- 参数: block_ref, ignore_empty, upper_tag
- 返回: dict，如:
- 调用概览: getattr, str, GetAttributes, strip, _clean_value, isinstance, startswith, split, upper
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取块参照 block_ref 的所有属性，返回 {标签: 纯文本值} 的字典。。邻近注释提示：&&% 获取属性块标签及标签值。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### separate_entities_by_block_names(entities, target_names)
- 说明: 将实体列表分为两组：
- 邻近注释: &&% 筛选出指定块名外的对象
- 参数: entities, target_names
- 返回: (kept_entities, target_blocks) 元组
- 调用概览: isinstance, set, get_attr, append
- 理解: 主要用于处理相关逻辑。依据注释：将实体列表分为两组：。邻近注释提示：&&% 筛选出指定块名外的对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### huoqu_kuai_pl(blocka)
- 说明: （无）
- 邻近注释: &&% 获取块内多段线
- 参数: blocka
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, Item, list, str, print
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 获取块内多段线。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### create_block_with_basepoint()
- 说明: （无）
- 邻近注释: &&&% 块定义 | 定义基点的块 | &&% 创建带基点块
- 参数: （无）
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, vtpnt, Add, AddCircle
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：&&&% 块定义；定义基点的块；&&% 创建带基点块。实现特征：创建圆对象；涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### create_block_with_triangle_and_text()
- 说明: （无）
- 邻近注释: 块的添加 | &&% 创建三角形文字块
- 参数: （无）
- 关注点: COM, 几何, 进程
- 调用概览: EnsureDispatch, vtpnt, Add, AddLine, AddText, print
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：块的添加；&&% 创建三角形文字块。实现特征：创建文字对象；创建直线对象；涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### huoqu_kuai_pl(blocka)
- 说明: （无）
- 参数: blocka
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, Item, list, str, print
- 理解: 主要用于处理相关逻辑。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_bounding_box_of_block(block_name)
- 说明: （无）
- 邻近注释: 块的边界 | &&% 获取块包围盒
- 参数: block_name
- 返回推断: tuple
- 关注点: COM, 几何, 进程
- 调用概览: EnsureDispatch, Item, float, GetBoundingBox, min, max
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：块的边界；&&% 获取块包围盒。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### create_new_block_with_insert_and_line()
- 说明: （无）
- 邻近注释: &&% 创建含插入和直线的块
- 参数: （无）
- 返回推断: None
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, vtpnt, Add, InsertBlock, AddLine, print
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：&&% 创建含插入和直线的块。实现特征：创建直线对象；涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### copy_and_move_blocks_from_layer(layer_name, block_prefix)
- 说明: （无）
- 邻近注释: &&% 复制并移动图层块
- 参数: layer_name, block_prefix
- 关注点: COM, 文件, 日志/测试, 选择集
- 调用概览: select_tuceng, VARIANT, info, Copy, Move, len
- 理解: 主要用于移动/复制相关逻辑。邻近注释提示：&&% 复制并移动图层块。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### delete_block_instances_and_definition_retry(target_block_name, max_rounds)
- 说明: 删除指定名称的块实例和块定义，带重试机制。
- 邻近注释: 块名的清除 | &&&% 删除指定块名的实例及块 | &&% 旧版
- 参数: target_block_name, max_rounds
- 返回推断: None,bool
- 关注点: 日志/测试, 时间/等待, 选择集
- 调用概览: get_acad_doc, info, range, print, select_kuai, len, Item, Delete, sleep, upper, append, safe_delete...
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除指定名称的块实例和块定义，带重试机制。。邻近注释提示：块名的清除；&&&% 删除指定块名的实例及块；&&% 旧版。实现特征：涉及块定义/块实例操作。包含选择集构造或过滤。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；超时与重试次数边界

### delete_block_instances_and_definition_optimized(target_name, max_retries)
- 说明: 【函数编号】: CLEAN-ROBUST-V34 (核验版)
- 邻近注释: &&% 极速清理
- 参数: target_name, max_retries
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: range, info, Item, Add, VARIANT, Select, Delete, Erase, wait_command_done, sleep, Regen
- 理解: 主要用于删除/清理相关逻辑。依据注释：【函数编号】: CLEAN-ROBUST-V34 (核验版)。邻近注释提示：&&% 极速清理。实现特征：涉及块定义/块实例操作；涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### delete_block_instances_and_definition_optimized(target_name, max_retries)
- 说明: 【最终推荐版】
- 邻近注释: &&% 再次优化
- 参数: target_name, max_retries
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: info, range, error, Item, Add, VARIANT, Select, Delete, Erase, Regen, sleep
- 理解: 主要用于删除/清理相关逻辑。依据注释：【最终推荐版】。邻近注释提示：&&% 再次优化。实现特征：涉及块定义/块实例操作；涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### rename_block_entity(ent, new_name)
- 说明: 将给定块参照实体 ent 的块名改为 new_name。
- 邻近注释: &&% 重命名块实体
- 参数: ent, new_name
- 调用概览: Item
- 理解: 主要用于更新/设置相关逻辑。依据注释：将给定块参照实体 ent 的块名改为 new_name。。邻近注释提示：&&% 重命名块实体。实现特征：涉及块定义/块实例操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_block_instances(block_name, max_retries)
- 说明: 根据给定的块定义名，检索当前图形中所有对应的块参照实例（BlockReference），
- 邻近注释: &&&% 块查询 | &&% 由块名选择实例
- 参数: block_name, max_retries
- 返回: instances     – 包含所有匹配块参照的列表（如果未找到或者出错，返回空列表）
- 关注点: 日志/测试, 选择集
- 调用概览: info, select_kuai, append, len, getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：根据给定的块定义名，检索当前图形中所有对应的块参照实例（BlockReference），。邻近注释提示：&&&% 块查询；&&% 由块名选择实例。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### get_entities_from_block_reference(block_ref)
- 说明: 获取块引用对象中的所有子实体（COM对象形式）。
- 邻近注释: &&% 从块实体对象获取其内部com对象 | &&% 获取块引用实体
- 参数: block_ref
- 返回: entities: 子实体列表
- 关注点: 日志/测试
- 调用概览: Item, info, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取块引用对象中的所有子实体（COM对象形式）。。邻近注释提示：&&% 从块实体对象获取其内部com对象；&&% 获取块引用实体。实现特征：涉及块定义/块实例操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### insert_block_into_autocad(block_file_path, insertion_point, scale, rotation)
- 说明: 以块的方式插入 DWG 文件到 AutoCAD 中
- 邻近注释: 以块的方式插入文件 | &&&% 块插入 | &&% 插入块到CAD
- 参数: block_file_path, insertion_point, scale, rotation
- 关注点: 日志/测试
- 调用概览: InsertBlock, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：以块的方式插入 DWG 文件到 AutoCAD 中。邻近注释提示：以块的方式插入文件；&&&% 块插入；&&% 插入块到CAD。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### insert_standard_block(block_dwg, insertion_point, scale, rotation, wait)
- 说明: 不炸开，
- 邻近注释: 不炸开 | &&% 插入标准块
- 参数: block_dwg, insertion_point, scale, rotation, wait
- 返回推断: list,object
- 关注点: COM, 文件, 时间/等待, 选择集
- 调用概览: select_kuai, replace, SendCommand, sleep, isfile, FileNotFoundError, print, GetBoundingBox, append, abspath
- 理解: 主要用于创建/插入相关逻辑。依据注释：不炸开，。邻近注释提示：不炸开；&&% 插入标准块。实现特征：通过命令发送驱动 CAD 行为。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### insert_and_explode_dwg(block_dwg, insertion_point, scale, rotation, wait)
- 说明: 将一个 WBLOCK 导出的标准块 DWG 插入到当前图，
- 邻近注释: 炸开 | &&% 插入并炸开DWG
- 参数: block_dwg, insertion_point, scale, rotation, wait
- 返回推断: list,tuple
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 选择集
- 调用概览: select_kuai, replace, SendCommand, sleep, info, isfile, FileNotFoundError, print, append, abspath, safe_get_bbox, basename...
- 理解: 主要用于创建/插入相关逻辑。依据注释：将一个 WBLOCK 导出的标准块 DWG 插入到当前图，。邻近注释提示：炸开；&&% 插入并炸开DWG。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### insert_and_explode_dwg(block_dwg, insertion_point, scale, rotation, wait)
- 说明: 【V3.0 重构版】插入并炸开 DWG
- 参数: block_dwg, insertion_point, scale, rotation, wait
- 返回推断: tuple
- 关注点: COM, 文件, 日志/测试, 选择集
- 关键调用: SafeCOM, C.doc
- 调用概览: info, replace, basename, isfile, select_kuai, CADGuard, SendCommand, print, abspath, call, append, getattr
- 理解: 主要用于创建/插入相关逻辑。依据注释：【V3.0 重构版】插入并炸开 DWG。实现特征：通过命令发送驱动 CAD 行为。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### get_large_block_instances(area_threshold, tol, max_retries)
- 说明: 获取模型空间中所有块实例，筛选出“包围盒面积大于 area_threshold” 的块，
- 邻近注释: &&% 获取面积足够大的全部非同名块实例 | &&% 获取大块实例
- 参数: area_threshold, tol, max_retries
- 返回推断: list,object
- 关注点: 日志/测试, 选择集
- 调用概览: select_kuai, info, GetBoundingBox, abs, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取模型空间中所有块实例，筛选出“包围盒面积大于 area_threshold” 的块，。邻近注释提示：&&% 获取面积足够大的全部非同名块实例；&&% 获取大块实例。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### get_large_block_instances_with_tolerance(max_retries, area_threshold)
- 说明: 获取当前 DWG 中所有大尺寸块实例
- 邻近注释: 从com对象中，根据其外包盒的矩形的长边与短边的比值和面积在160000000到1000000000两个条件筛算 | &&% 确定合乎标准打印要求的自建多段线区域
- 参数: max_retries, area_threshold
- 返回推断: list,object
- 关注点: 日志/测试, 选择集
- 调用概览: select_kuai, info, GetBoundingBox, abs, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取当前 DWG 中所有大尺寸块实例。邻近注释提示：从com对象中，根据其外包盒的矩形的长边与短边的比值和面积在160000000到1000000000两个条件筛算；&&% 确定合乎标准打印要求的自建多段线区域。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### transform_point_by_block(block_ref, local_pt)
- 说明: 将块内部坐标 local_pt = (lx, ly, lz) 转换为世界坐标：
- 邻近注释: &&% 块内坐标转换成世界坐标（适合平面上的一般块）
- 参数: block_ref, local_pt
- 返回推断: tuple
- 关注点: 几何
- 调用概览: cos, sin
- 理解: 主要用于转换/解析相关逻辑。依据注释：将块内部坐标 local_pt = (lx, ly, lz) 转换为世界坐标：。邻近注释提示：&&% 块内坐标转换成世界坐标（适合平面上的一般块）。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### select_block_by_name(block_name, max_retries)
- 说明: 从 *模型空间* 快速选出指定块名的所有实例，返回实体列表。
- 邻近注释: &&% 按名称选择块
- 参数: block_name, max_retries
- 返回推断: list,object
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 调用概览: range, info, time, Add, vtInt, vtVariant, Select, list, suppress, Delete, sleep, Item...
- 理解: 主要用于获取/选择相关逻辑。依据注释：从 *模型空间* 快速选出指定块名的所有实例，返回实体列表。。邻近注释提示：&&% 按名称选择块。实现特征：涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### get_all_block_definitions(max_retry, quiet)
- 说明: 返回当前 DWG 中所有块定义（BlockTableRecord）对象列表。
- 邻近注释: &&&% 块管理 | &&% 获取所有块定义
- 参数: max_retry, quiet
- 返回: list[COM block object]
- 关注点: COM, 文件, 时间/等待
- 调用概览: range, log, li, RuntimeError, clear, print, PumpWaitingMessages, sleep, len, suppress, Item, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：返回当前 DWG 中所有块定义（BlockTableRecord）对象列表。。邻近注释提示：&&&% 块管理；&&% 获取所有块定义。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### get_all_block_names()
- 说明: 使用全局 li()/doc 获取当前 DWG 中所有块定义的名字列表。
- 邻近注释: &&% 获取所有块名
- 参数: （无）
- 返回推断: object
- 关注点: COM
- 调用概览: get_all_block_definitions, append, str
- 理解: 主要用于获取/选择相关逻辑。依据注释：使用全局 li()/doc 获取当前 DWG 中所有块定义的名字列表。。邻近注释提示：&&% 获取所有块名。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### purge_block(block_name, quiet)
- 说明: 删除指定块的所有实例，并彻底清除该块定义。
- 邻近注释: &&% 块清理
- 参数: block_name, quiet
- 关注点: COM, 文件, 日志/测试, 时间/等待, 进程
- 调用概览: EnsureDispatch, list, sleep, info, suppress, PurgeAll, Item, Delete, print, getattr
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除指定块的所有实例，并彻底清除该块定义。。邻近注释提示：&&% 块清理。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### purge_unused_blocks(quiet)
- 说明: 一次性清除所有未被任何 INSERT 实例引用的块定义。
- 邻近注释: &&% 清理未使用块
- 参数: quiet
- 返回推断: object
- 关注点: COM, 文件, 日志/测试, 进程, 选择集
- 调用概览: EnsureDispatch, range, time, suppress, PurgeAll, info, append, print, Item, len
- 理解: 主要用于删除/清理相关逻辑。依据注释：一次性清除所有未被任何 INSERT 实例引用的块定义。。邻近注释提示：&&% 清理未使用块。实现特征：涉及块定义/块实例操作；涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### purge_block_1(block_name, quiet, max_delete_attempts)
- 说明: 删除指定块的所有实例，并尽可能彻底清除该块定义。
- 邻近注释: &&% 清理块1
- 参数: block_name, quiet, max_delete_attempts
- 返回推断: None,bool,object
- 关注点: COM, 文件, 时间/等待
- 调用概览: node, sleep, range, strftime, li, log, suppress, list, PurgeAll, print, getattr, Item...
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除指定块的所有实例，并尽可能彻底清除该块定义。。邻近注释提示：&&% 清理块1。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### purge_unused_blocks_1(quiet, protect_names, max_delete_attempts, rename_prefix)
- 说明: 一次性清除“当前文件中没有任何实例引用”的块定义。
- 邻近注释: &&% 清理未使用块1
- 参数: quiet, protect_names, max_delete_attempts, rename_prefix
- 返回推断: bool,list,object
- 关注点: COM, 文件, 时间/等待
- 调用概览: node, Counter, time, log, startswith, strftime, li, suppress, PurgeAll, range, print, getattr...
- 理解: 主要用于删除/清理相关逻辑。依据注释：一次性清除“当前文件中没有任何实例引用”的块定义。。邻近注释提示：&&% 清理未使用块1。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### reserve_block_names_for_new_insert(block_names, rename_prefix, verbose)
- 说明: 【核心目标】在插入新块之前，为一组块名“预留新定义空间”。
- 邻近注释: &&% 预留新插入块名
- 参数: block_names, rename_prefix, verbose
- 返回: dict: { 原名 -> 新名 }，没有被占用的块名不会出现在返回字典中。
- 关注点: COM, 文件
- 调用概览: isinstance, node, strftime, li, log, print, Item, make_legacy_name, items, now
- 理解: 主要用于创建/插入相关逻辑。依据注释：【核心目标】在插入新块之前，为一组块名“预留新定义空间”。。邻近注释提示：&&% 预留新插入块名。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### get_selected_blockreference_names()
- 说明: 使用 pmxz() 选择实体，并返回所有块引用（AcDbBlockReference）的块名列表。
- 邻近注释: &&% 获取选定块引用名
- 参数: （无）
- 返回推断: list,object
- 关注点: 日志/测试
- 调用概览: pmxz, info, getattr, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：使用 pmxz() 选择实体，并返回所有块引用（AcDbBlockReference）的块名列表。。邻近注释提示：&&% 获取选定块引用名。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### create_block_from_region_cad(x1, y1, x2, y2, insert_point_option, block_name_prefix, base_point, ty)
- 说明: 【纯 CAD 重绘版】从矩形区域创建块（重画为标准 CAD 实体），
- 邻近注释: &&% 从区域创建CAD块
- 参数: x1, y1, x2, y2, insert_point_option, block_name_prefix, base_point, ty
- 返回推断: NoneType,bool,object,tuple
- 关注点: COM, 几何, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: select_entities_in_window, info, group_bbox_corners, get, VARIANT, Add, list, print, InsertBlock, Item, GetBoundingBox, com_retry...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【纯 CAD 重绘版】从矩形区域创建块（重画为标准 CAD 实体），。邻近注释提示：&&% 从区域创建CAD块。实现特征：创建圆对象；创建文字对象；创建点对象；创建直线对象；涉及块定义/块实例操作。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### create_block_from_region_cmd(x1, y1, x2, y2, insert_point_option, block_name_prefix, base_point, ty)
- 说明: 【命令行版】通过 -BLOCK 从矩形区域创建块（保留天正对象），
- 参数: x1, y1, x2, y2, insert_point_option, block_name_prefix, base_point, ty
- 返回推断: NoneType,object,tuple
- 关注点: COM, 几何, 日志/测试, 时间/等待, 选择集
- 关键调用: SafeCOM, C.doc
- 调用概览: _normalize_rect, Add, VARIANT, print, list_selection, info, group_bbox_corners, get, SendCommand, sleep, range, GetVariable...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【命令行版】通过 -BLOCK 从矩形区域创建块（保留天正对象），。实现特征：涉及块定义/块实例操作；涉及系统变量读取/设置；涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### create_block_from_list_cmd(entities, insert_point_option, block_name_prefix, base_point, ty)
- 说明: 【命令行版】将指定的 Python 对象列表封装成块。
- 参数: entities, insert_point_option, block_name_prefix, base_point, ty
- 返回推断: NoneType,object
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 关键调用: C.doc
- 调用概览: ensure_list, group_bbox_corners, info, SendCommand, range, sleep, print, get, len, VARIANT, Item, append...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【命令行版】将指定的 Python 对象列表封装成块。。实现特征：涉及块定义/块实例操作；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### get_block_contents_at_same_location(block_ref)
- 说明: 【函数2】获取块内图形并在原位置复制,它的作用是获取到实体内部对象
- 邻近注释: &&&% 块编辑 | &&% 获取块内实体
- 参数: block_ref
- 返回推断: list,object
- 关注点: COM, 日志/测试
- 关键调用: C.li
- 调用概览: li, Copy, print, Explode, list, info, Delete, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数2】获取块内图形并在原位置复制,它的作用是获取到实体内部对象。邻近注释提示：&&&% 块编辑；&&% 获取块内实体。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### add_entities_to_block_direct(block_ref, entities, delete_original)
- 说明: 【函数】进入块定义内部添加对象（强类型修正版）
- 参数: block_ref, entities, delete_original
- 返回推断: bool,object
- 关注点: COM, 几何, 日志/测试
- 调用概览: ensure_list, info, get_attr, Update, VARIANT, Item, CopyObjects, com_point, float, len, append, isinstance...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数】进入块定义内部添加对象（强类型修正版）。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### add_entities_to_block_definition_explode(block_ref, new_entities, ty)
- 说明: 【函数】向块定义中追加对象（独立版）
- 参数: block_ref, new_entities, ty
- 返回推断: bool
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 关键调用: C.doc
- 调用概览: ensure_list, get_attr, info, SendCommand, range, print, sleep, Explode, list, len, Regen, Update...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数】向块定义中追加对象（独立版）。实现特征：涉及系统变量读取/设置；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### redefine_block_with_entities(block_ref, entities, ty, debug_log_path)
- 说明: 【调试专用版 V2】redefine_block_with_entities
- 参数: block_ref, entities, ty, debug_log_path
- 返回推断: bool
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 进程
- 调用概览: info, len, SetVariable, SendCommand, range, print, GetActiveObject, getattr, Item, append, sleep, GetVariable...
- 理解: 主要用于处理相关逻辑。依据注释：【调试专用版 V2】redefine_block_with_entities。实现特征：涉及块定义/块实例操作；涉及系统变量读取/设置；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### extract_specific_entities_from_block(block_ref, mode, keep_in_block)
- 说明: 【函数】从块中提取指定类型的对象（筛选版）
- 参数: block_ref, mode, keep_in_block
- 返回推断: list,object
- 关注点: COM, 几何, 日志/测试
- 调用概览: lower, info, hasattr, Explode, print, len, get_attr, Update, Regen, append, Delete, Item
- 理解: 主要用于处理相关逻辑。依据注释：【函数】从块中提取指定类型的对象（筛选版）。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### safe_explode(block_entity)
- 说明: 【原子操作】
- 参数: block_entity
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: retry_on_busy, Explode
- 理解: 主要用于处理相关逻辑。依据注释：【原子操作】。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _atomic_explode_and_delete(block_entity)
- 说明: 【原子操作】
- 参数: block_entity
- 返回推断: object
- 关注点: 时间/等待
- 关键调用: wait_quiescent, retry_on_busy
- 调用概览: retry_on_busy, Explode, Delete, wait_quiescent, sleep
- 理解: 主要用于删除/清理相关逻辑。依据注释：【原子操作】。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### safe_explode_retry(entity, max_retries, rescue_retries, interval, verbose)
- 说明: 【通用原子函数 - 深度搜救修正版 (V5.0)】
- 参数: entity, max_retries, rescue_retries, interval, verbose
- 返回推断: NoneType,bool,list,object
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: wait_quiescent, retry_on_busy
- 调用概览: range, ObjectIdToObject, is_entity_alive, info, hasattr, _atomic_explode_and_delete, print, list, max, sleep, len, wait_quiescent...
- 理解: 主要用于等待/守护相关逻辑。依据注释：【通用原子函数 - 深度搜救修正版 (V5.0)】。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### explode_single_object_marker(ent)
- 说明: 【主函数】炸开单个对象（辅助线回溯版）
- 邻近注释: &&% 炸开对象并回溯
- 参数: ent
- 返回推断: list,object
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: li, info, VARIANT, SendCommand, range, AddLine, set_entity_grip_state_precise, print, wait_command_done, sleep, Item, append...
- 理解: 主要用于处理相关逻辑。依据注释：【主函数】炸开单个对象（辅助线回溯版）。邻近注释提示：&&% 炸开对象并回溯。实现特征：创建直线对象；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### safe_explode_and_delete(bk, ci, delay)
- 说明: 对块对象 bk 执行安全的 Explode 与 Delete 操作：
- 邻近注释: &&% 安全炸开并删除
- 参数: bk, ci, delay
- 返回推断: object
- 关注点: 时间/等待
- 调用概览: range, sleep, RuntimeError, Explode, len, Delete, list
- 理解: 主要用于删除/清理相关逻辑。依据注释：对块对象 bk 执行安全的 Explode 与 Delete 操作：。邻近注释提示：&&% 安全炸开并删除。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### count_blocks_by_name(block_name)
- 说明: # 【新增】统计指定块数量
- 邻近注释: &&&% 块统计 | &&% count_blocks_by_name
- 参数: block_name
- 返回: int: 块实例数量
- 关注点: 日志/测试, 选择集
- 调用概览: ss_select, info, len, error
- 理解: 主要用于处理相关逻辑。依据注释：# 【新增】统计指定块数量。邻近注释提示：&&&% 块统计；&&% count_blocks_by_name。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### count_blocks_by_type()
- 说明: # 【新增】按类型统计块
- 邻近注释: &&% count_blocks_by_type
- 参数: （无）
- 返回: dict: {块名: 数量}
- 关注点: 日志/测试, 选择集
- 调用概览: ss_select, info, get_block_name, error, get, len
- 理解: 主要用于处理相关逻辑。依据注释：# 【新增】按类型统计块。邻近注释提示：&&% count_blocks_by_type。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### generate_block_report(output_path)
- 说明: # 【新增】生成块统计报告
- 邻近注释: &&% generate_block_report
- 参数: output_path
- 返回: bool: 成功返回True
- 关注点: 文件, 日志/测试
- 调用概览: count_blocks_by_type, endswith, info, DataFrame, to_excel, error, list, open, write, sorted, items
- 理解: 主要用于处理相关逻辑。依据注释：# 【新增】生成块统计报告。邻近注释提示：&&% generate_block_report。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### batch_replace_blocks(old_name, new_name)
- 说明: # 【新增】批量替换块
- 邻近注释: &&&% 块替换 | &&% batch_replace_blocks
- 参数: old_name, new_name
- 返回: int: 替换数量
- 关注点: 日志/测试, 选择集
- 调用概览: ss_select, info, error, warning
- 理解: 主要用于处理相关逻辑。依据注释：# 【新增】批量替换块。邻近注释提示：&&&% 块替换；&&% batch_replace_blocks。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### smart_replace_blocks(criteria, new_name)
- 说明: # 【新增】智能替换块
- 邻近注释: &&% smart_replace_blocks
- 参数: criteria, new_name
- 返回: int: 替换数量
- 关注点: 日志/测试, 选择集
- 调用概览: ss_select, info, error, criteria, warning
- 理解: 主要用于处理相关逻辑。依据注释：# 【新增】智能替换块。邻近注释提示：&&% smart_replace_blocks。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

## library/cad_control.py
- 模块说明: 第七部分 综合控制
### fix_com_cache()
- 说明: 【急救】清理 win32com 的 gen_py 缓存
- 参数: （无）
- 关注点: COM, 文件, 日志/测试
- 调用概览: print, info, exists, hasattr, getsitepackages, GetGeneratePath, join, rmtree, get
- 理解: 主要用于处理相关逻辑。依据注释：【急救】清理 win32com 的 gen_py 缓存。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### delete_all_nul_under_folder(folder_path)
- 说明: 输入文件夹路径（如 D:\claude-tasks），
- 邻近注释: &&% 清除nul
- 参数: folder_path
- 返回推断: None
- 关注点: 文件, 日志/测试, 选择集
- 调用概览: abspath, info, walk, exists, print, lower, join, remove
- 理解: 主要用于删除/清理相关逻辑。依据注释：输入文件夹路径（如 D:\claude-tasks），。邻近注释提示：&&% 清除nul。包含选择集构造或过滤。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### kill_dialog_killer()
- 说明: 查找并终止名为 'cad_dialog_killer.py' 的 Python 进程
- 邻近注释: &&% 终止弹窗程序
- 参数: （无）
- 关注点: 文件, 日志/测试, 进程, 选择集
- 调用概览: print, Popen, communicate, decode, split, info, strip, isdigit, system
- 理解: 主要用于关闭/终止相关逻辑。依据注释：查找并终止名为 'cad_dialog_killer.py' 的 Python 进程。邻近注释提示：&&% 终止弹窗程序。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### kill_python_script_by_name(target_script_name)
- 说明: 【推荐】使用 psutil 精准终止指定名称的 Python 脚本。
- 邻近注释: &&% 终止指定py脚本 (psutil版)
- 参数: target_script_name
- 返回推断: object
- 关注点: 日志/测试, 进程
- 调用概览: info, getpid, lower, process_iter, kill, join
- 理解: 主要用于关闭/终止相关逻辑。依据注释：【推荐】使用 psutil 精准终止指定名称的 Python 脚本。。邻近注释提示：&&% 终止指定py脚本 (psutil版)。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### kill_wps(verbose)
- 说明: 结束所有 WPS/金山办公相关进程，特别是 wpspdf.exe。
- 邻近注释: &&% 结束WPS进程
- 参数: verbose
- 关注点: 进程
- 调用概览: set, call, add, print, join, sorted
- 理解: 主要用于关闭/终止相关逻辑。依据注释：结束所有 WPS/金山办公相关进程，特别是 wpspdf.exe。。邻近注释提示：&&% 结束WPS进程。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### close_all_excel_processes()
- 说明: 【函数编号】: SYS-KILL-XLS
- 邻近注释: &&%关闭excel进程
- 参数: （无）
- 返回推断: bool,int,object
- 关注点: 日志/测试, 时间/等待, 进程, 选择集
- 调用概览: range, print, run, _get_excel_count, info, sleep, count, lower
- 理解: 主要用于关闭/终止相关逻辑。依据注释：【函数编号】: SYS-KILL-XLS。邻近注释提示：&&%关闭excel进程。包含选择集构造或过滤。
- 风险: 涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；超时与重试次数边界

### safe_delete(ob, retries, delay)
- 说明: 安全删除 CAD 对象。
- 邻近注释: &&&% 确保安全删除
- 参数: ob, retries, delay
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: range, Delete, sleep
- 理解: 主要用于删除/清理相关逻辑。依据注释：安全删除 CAD 对象。。邻近注释提示：&&&% 确保安全删除。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### move_entities_in_region(coms, target, ty, max_iter)
- 说明: 将 `coms` 对象的包围盒内所有实体，沿向量 (target - 左下角) 移动，
- 邻近注释: &&% 区域实体移动
- 参数: coms, target, ty, max_iter
- 关注点: COM, 文件, 日志/测试, 时间/等待, 选择集
- 调用概览: GetBoundingBox, range, min, max, highlight_entities_in_window, info, sleep, print, Clear, hasattr, len, list...
- 理解: 主要用于移动/复制相关逻辑。依据注释：将 `coms` 对象的包围盒内所有实体，沿向量 (target - 左下角) 移动，。邻近注释提示：&&% 区域实体移动。实现特征：涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### 圆点(tz)
- 说明: 控制点的显示
- 邻近注释: &&&% 显示控制 | &&% 设置点样式
- 参数: tz
- 关注点: COM
- 调用概览: SetVariable
- 理解: 主要用于处理相关逻辑。依据注释：控制点的显示。邻近注释提示：&&&% 显示控制；&&% 设置点样式。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### 图纸背景(zhi)
- 说明: （无）
- 邻近注释: &&% 设置图纸背景色
- 参数: zhi
- 关注点: COM
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 设置图纸背景色。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### shitu_region(x1, y1, x2, y2)
- 说明: 按按对象外包盒调整视图
- 邻近注释: &&&%  *** 按区域调整视图 | &&% 视图区域缩放
- 参数: x1, y1, x2, y2
- 关注点: COM
- 调用概览: SendCommand, abs
- 理解: 主要用于处理相关逻辑。依据注释：按按对象外包盒调整视图。邻近注释提示：&&&%  *** 按区域调整视图；&&% 视图区域缩放。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### shitu_entity(obj)
- 说明: 按按对象外包盒调整视图
- 邻近注释: 按对象外包盒调整视图 | &&% 视图实体缩放
- 参数: obj
- 关注点: COM
- 调用概览: GetBoundingBox, SendCommand, abs
- 理解: 主要用于处理相关逻辑。依据注释：按按对象外包盒调整视图。邻近注释提示：按对象外包盒调整视图；&&% 视图实体缩放。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### record_screen_gif(output_path, duration, fps, region)
- 说明: 录制屏幕并保存为 GIF。
- 邻近注释: &&% 录制屏幕GIF
- 参数: output_path, duration, fps, region
- 关注点: 日志/测试, 时间/等待
- 调用概览: info, mimsave, time, screenshot, append, sleep, len
- 理解: 主要用于保存/写入相关逻辑。依据注释：录制屏幕并保存为 GIF。。邻近注释提示：&&% 录制屏幕GIF。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### minimize_all_windows()
- 说明: 模拟按下 Win+M，将所有窗口最小化。
- 邻近注释: &&&% 窗口控制 | &&% 最小化所有窗口
- 参数: （无）
- 关注点: 时间/等待, 窗口/输入
- 调用概览: keybd_event, sleep
- 理解: 主要用于处理相关逻辑。依据注释：模拟按下 Win+M，将所有窗口最小化。。邻近注释提示：&&&% 窗口控制；&&% 最小化所有窗口。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### set_autocad_window_to_top_left(resize_half)
- 说明: 将 AutoCAD 窗口还原并移动到屏幕左上角，可选将其调整为半屏大小。
- 邻近注释: &&%#控制CAD屏幕窗口在左上角 | &&% CAD窗口置左上
- 参数: resize_half
- 返回推断: None
- 关注点: 文件, 日志/测试, 时间/等待, 选择集
- 调用概览: sleep, moveTo, print, restore, activate, size, resizeTo, info, getWindowsWithTitle
- 理解: 主要用于更新/设置相关逻辑。依据注释：将 AutoCAD 窗口还原并移动到屏幕左上角，可选将其调整为半屏大小。。邻近注释提示：&&%#控制CAD屏幕窗口在左上角；&&% CAD窗口置左上。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### l()
- 说明: （无）
- 邻近注释: &&% CAD窗口置左上别名
- 参数: （无）
- 调用概览: set_autocad_window_to_top_left
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% CAD窗口置左上别名。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### minimize_all_windows_d()
- 说明: 模拟 Win + D，将所有窗口最小化（切换）。
- 邻近注释: &&% 更合理控制窗口函数 | — — — — -- -- -- -- --  — — — — -- -- -- -- -- — — — — -- -- -- -- --  — — — — -- -- | &&% 最小化窗口Win+D
- 参数: （无）
- 关注点: 时间/等待, 窗口/输入
- 调用概览: keybd_event, sleep
- 理解: 主要用于处理相关逻辑。依据注释：模拟 Win + D，将所有窗口最小化（切换）。。邻近注释提示：&&% 更合理控制窗口函数；— — — — -- -- -- -- --  — — — — -- -- -- -- -- — — — — -- -- -- -- --  — — — — -- --；&&% 最小化窗口Win+D。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### minimize_all_windows_m()
- 说明: 模拟按下 Win+M，将所有窗口最小化。
- 邻近注释: &&% 最小化窗口Win+M
- 参数: （无）
- 关注点: 时间/等待, 窗口/输入
- 调用概览: keybd_event, sleep
- 理解: 主要用于处理相关逻辑。依据注释：模拟按下 Win+M，将所有窗口最小化。。邻近注释提示：&&% 最小化窗口Win+M。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### restore_and_position(name, width_ratio, height_ratio, x, y)
- 说明: 将第一个标题中包含 name 的窗口恢复、激活，并调整到指定位置和大小。
- 邻近注释: &&% 恢复并定位窗口
- 参数: name, width_ratio, height_ratio, x, y
- 返回推断: bool
- 关注点: 文件, 日志/测试, 时间/等待, 选择集
- 调用概览: sleep, size, max, int, info, activate, moveTo, min, resizeTo, getWindowsWithTitle, restore
- 理解: 主要用于处理相关逻辑。依据注释：将第一个标题中包含 name 的窗口恢复、激活，并调整到指定位置和大小。。邻近注释提示：&&% 恢复并定位窗口。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### list_open_window_titles()
- 说明: 获取当前所有可见窗口的标题列表包括子窗口。
- 邻近注释: &&% 列出打开窗口标题
- 参数: （无）
- 返回推断: object
- 关注点: 选择集
- 调用概览: getAllWindows, strip, append
- 理解: 主要用于打开/读取相关逻辑。依据注释：获取当前所有可见窗口的标题列表包括子窗口。。邻近注释提示：&&% 列出打开窗口标题。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### ceshubiao_weizhi()
- 说明: 提示用户 5 秒内将鼠标移动到 AutoCAD 命令栏输入位置，
- 邻近注释: &&% 测鼠标位置
- 参数: （无）
- 返回推断: tuple
- 关注点: 日志/测试, 时间/等待
- 调用概览: print, sleep, position, info
- 理解: 主要用于处理相关逻辑。依据注释：提示用户 5 秒内将鼠标移动到 AutoCAD 命令栏输入位置，。邻近注释提示：&&% 测鼠标位置。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### run_idle_background(script_path)
- 说明: 用后台模式启动 IDLE 去运行某个脚本，返回 Popen 实例。
- 邻近注释: &&% 后台运行IDLE
- 参数: script_path
- 返回推断: object
- 关注点: 文件, 进程, 选择集
- 调用概览: Popen
- 理解: 主要用于处理相关逻辑。依据注释：用后台模式启动 IDLE 去运行某个脚本，返回 Popen 实例。。邻近注释提示：&&% 后台运行IDLE。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### click_and_drag(x, y, juli)
- 说明: 在屏幕坐标 (x, y) 按下左键，然后向纵向拖动距离 juli。
- 邻近注释: &&% 点击并拖动
- 参数: x, y, juli
- 关注点: 文件, 时间/等待
- 调用概览: moveTo, sleep, mouseDown, mouseUp
- 理解: 主要用于处理相关逻辑。依据注释：在屏幕坐标 (x, y) 按下左键，然后向纵向拖动距离 juli。。邻近注释提示：&&% 点击并拖动。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### click_and_find_image_shape(x, y, tupian_path, timeout)
- 说明: 在 (x, y) 单击一次，然后不断在整个屏幕上查找与 tupian_path 对应的图片形状，
- 邻近注释: &&% 点击并找图
- 参数: x, y, tupian_path, timeout
- 返回推断: NoneType,tuple
- 关注点: 文件, 时间/等待
- 调用概览: moveTo, click, sleep, time, isfile, FileNotFoundError, locateCenterOnScreen, print, int
- 理解: 主要用于获取/选择相关逻辑。依据注释：在 (x, y) 单击一次，然后不断在整个屏幕上查找与 tupian_path 对应的图片形状，。邻近注释提示：&&% 点击并找图。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### right_click_and_move(x, y, x_xiangdui, y_xiangdui)
- 说明: 在屏幕坐标 (x, y) 处执行右键点击，然后将鼠标相对于 (x, y) 
- 邻近注释: &&% 右键点击并移动
- 参数: x, y, x_xiangdui, y_xiangdui
- 关注点: 文件, 时间/等待
- 调用概览: moveTo, click, sleep
- 理解: 主要用于移动/复制相关逻辑。依据注释：在屏幕坐标 (x, y) 处执行右键点击，然后将鼠标相对于 (x, y) 。邻近注释提示：&&% 右键点击并移动。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### kill_all_idle()
- 说明: 终止所有名为 'idle' 或 'idle.exe' 的进程（不再需要任务管理器）。
- 邻近注释: &&% 结束所有IDLE进程
- 参数: （无）
- 关注点: 进程
- 调用概览: process_iter, lower, startswith, terminate
- 理解: 主要用于关闭/终止相关逻辑。依据注释：终止所有名为 'idle' 或 'idle.exe' 的进程（不再需要任务管理器）。。邻近注释提示：&&% 结束所有IDLE进程。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### set_idle_window_to_top_right()
- 说明: （无）
- 邻近注释: &&% IDLE窗口置右上
- 参数: （无）
- 返回推断: None
- 关注点: 文件, 日志/测试, 选择集
- 调用概览: size, moveTo, resizeTo, info, print, getWindowsWithTitle
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：&&% IDLE窗口置右上。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### r()
- 说明: （无）
- 参数: （无）
- 调用概览: set_idle_window_to_top_right
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### place_obs_bottom_right()
- 说明: 将 OBS Studio 主窗口移动到屏幕右下角，并缩放为屏幕宽高的一半。
- 邻近注释: 控制OBS窗口在右下角 | &&% OBS窗口置右下
- 参数: （无）
- 返回推断: None
- 关注点: 文件, 时间/等待, 选择集
- 调用概览: print, size, moveTo, sleep, resizeTo, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：将 OBS Studio 主窗口移动到屏幕右下角，并缩放为屏幕宽高的一半。。邻近注释提示：控制OBS窗口在右下角；&&% OBS窗口置右下。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### r2()
- 说明: （无）
- 参数: （无）
- 调用概览: place_obs_bottom_right
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### minimize_window(window_keyword)
- 说明: 通用：最小化第一个标题包含 window_keyword 的可见窗口。
- 邻近注释: &&% 最小化指定窗口
- 参数: window_keyword
- 返回推断: bool
- 关注点: 选择集
- 调用概览: print, minimize, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：通用：最小化第一个标题包含 window_keyword 的可见窗口。。邻近注释提示：&&% 最小化指定窗口。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### maximize_autocad_window(window_keyword)
- 说明: 强制最大化第一个标题包含 window_keyword 的可见窗口。
- 邻近注释: &&% 最大化CAD窗口
- 参数: window_keyword
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待, 窗口/输入, 选择集
- 调用概览: sleep, info, ShowWindow, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：强制最大化第一个标题包含 window_keyword 的可见窗口。。邻近注释提示：&&% 最大化CAD窗口。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### start_obs_recording_by_click(x, y, button, clicks, move_duration)
- 说明: 通过鼠标点击屏幕上 (x,y) 坐标来控制 OBS 开始/停止录制。
- 邻近注释: &&% 点击开始OBS录制
- 参数: x, y, button, clicks, move_duration
- 关注点: 文件, 日志/测试
- 调用概览: moveTo, click, info
- 理解: 主要用于保存/写入相关逻辑。依据注释：通过鼠标点击屏幕上 (x,y) 坐标来控制 OBS 开始/停止录制。。邻近注释提示：&&% 点击开始OBS录制。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### fs(x1, y1)
- 说明: 微信调到0.5窗口
- 邻近注释: &&&% *** 录屏 | &&% 发送微信
- 参数: x1, y1
- 关注点: 文件
- 调用概览: moveTo, click, press
- 理解: 主要用于处理相关逻辑。依据注释：微信调到0.5窗口。邻近注释提示：&&&% *** 录屏；&&% 发送微信。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### xuanqun(x1, y1, neirong)
- 说明: （无）
- 邻近注释: &&% 选微信群
- 参数: x1, y1, neirong
- 关注点: 文件, 时间/等待
- 调用概览: copy_to_clipboard, moveTo, click, sleep, activate_window_by_title, hotkey, press
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 选微信群。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### copy_to_clipboard(text)
- 说明: 将传入的 text 文本写入系统剪贴板，供后续右键→粘贴使用。
- 邻近注释: &&% 复制到剪贴板
- 参数: text
- 关注点: UI/Tk, 文件
- 调用概览: Tk, withdraw, clipboard_clear, clipboard_append, update, destroy
- 理解: 主要用于移动/复制相关逻辑。依据注释：将传入的 text 文本写入系统剪贴板，供后续右键→粘贴使用。。邻近注释提示：&&% 复制到剪贴板。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### xieweixin(x1, y1, neirong)
- 说明: （无）
- 邻近注释: &&% 写微信
- 参数: x1, y1, neirong
- 关注点: 文件, 时间/等待
- 调用概览: copy_to_clipboard, sleep, moveTo, activate_window_by_title, click, hotkey
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 写微信。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### 主操作函数()
- 说明: （无）
- 邻近注释: &&% 主操作函数
- 参数: （无）
- 关注点: 时间/等待
- 调用概览: restore_and_position, sleep, activate_window_by_title, xuanqun, click_and_find_image_shape, click, xieweixin, fs
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 主操作函数。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### main_func(folder_path)
- 说明: （无）
- 邻近注释: &&% 主函数入口
- 参数: folder_path
- 调用概览: 打印输出PDF
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 主函数入口。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### luping(main_func, *args, **kwargs)
- 说明: 1) 开始 OBS 录制  
- 邻近注释: &&% 录屏
- 参数: main_func, *args, **kwargs
- 关注点: 文件, 时间/等待
- 调用概览: minimize_all_windows_d, restore_and_position, sleep, activate_window_by_title, moveTo, click, main_func, print
- 理解: 主要用于处理相关逻辑。依据注释：1) 开始 OBS 录制  。邻近注释提示：&&% 录屏。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### 魔方()
- 说明: （无）
- 邻近注释: &&% 魔方
- 参数: （无）
- 调用概览: 魔方控制台
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 魔方。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### run_py(pyname)
- 说明: （无）
- 邻近注释: &&% 运行Python脚本
- 参数: pyname
- 关注点: 日志/测试, 进程
- 调用概览: run, info
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 运行Python脚本。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### focus_cmdline(cmd_x, cmd_y, delay)
- 说明: 把鼠标移到命令行并单击，确保焦点回到 AutoCAD 命令栏。
- 邻近注释: &&% 聚焦命令行
- 参数: cmd_x, cmd_y, delay
- 关注点: 文件
- 调用概览: moveTo, click
- 理解: 主要用于处理相关逻辑。依据注释：把鼠标移到命令行并单击，确保焦点回到 AutoCAD 命令栏。。邻近注释提示：&&% 聚焦命令行。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### activate_window_by_title(title, click_titlebar)
- 说明: 激活一个指定标题的窗口。
- 邻近注释: &&% 激活窗口和子窗口
- 参数: title, click_titlebar
- 返回推断: bool,tuple
- 关注点: 日志/测试, 时间/等待, 窗口/输入, 选择集
- 调用概览: info, restore, sleep, activate, click, getWindowsWithTitle, ShowWindow, SetForegroundWindow, max, min
- 理解: 主要用于处理相关逻辑。依据注释：激活一个指定标题的窗口。。邻近注释提示：&&% 激活窗口和子窗口。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### click_in_window(title, offset_x, offset_y, click_titlebar)
- 说明: 在指定窗口的某个相对像素位置点击一次（相对于窗口左上角的偏移量）。
- 邻近注释: &&% 窗口内点击
- 参数: title, offset_x, offset_y, click_titlebar
- 返回推断: bool
- 关注点: 文件, 日志/测试, 时间/等待, 窗口/输入, 选择集
- 调用概览: int, moveTo, click, sleep, info, restore, activate, getWindowsWithTitle, ShowWindow, SetForegroundWindow
- 理解: 主要用于处理相关逻辑。依据注释：在指定窗口的某个相对像素位置点击一次（相对于窗口左上角的偏移量）。。邻近注释提示：&&% 窗口内点击。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### activate_and_click_aikeyun()
- 说明: （无）
- 邻近注释: &&% 激活并点击艾可云
- 参数: （无）
- 关注点: 文件, 时间/等待
- 调用概览: activate_window_by_title, moveTo, click, sleep
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 激活并点击艾可云。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### drag_in_window_simple(title, start, offset, duration, button, absolute_start)
- 说明: 拖拽函数，支持相对或绝对起点：
- 邻近注释: &&% 窗口内简单拖拽
- 参数: title, start, offset, duration, button, absolute_start
- 关注点: 文件, 日志/测试, 时间/等待
- 调用概览: activate_window_by_title, moveTo, mouseDown, mouseUp, sleep, info
- 理解: 主要用于处理相关逻辑。依据注释：拖拽函数，支持相对或绝对起点：。邻近注释提示：&&% 窗口内简单拖拽。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### run_auto_explode_area(x1, y1, x2, y2, cmd_x, cmd_y, delay)
- 说明: 这是一个未使用pywin32API控制天正CAD的典型函数
- 邻近注释: &&% 纯窗口操作炸开区域内对象
- 参数: x1, y1, x2, y2, cmd_x, cmd_y, delay
- 关注点: 文件, 进程
- 调用概览: with_name, str, run, print, Path
- 理解: 主要用于计算/测量相关逻辑。依据注释：这是一个未使用pywin32API控制天正CAD的典型函数。邻近注释提示：&&% 纯窗口操作炸开区域内对象。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### list_all_windows()
- 说明: （无）
- 邻近注释: &&% 列出所有窗口
- 参数: （无）
- 关注点: 日志/测试, 选择集
- 调用概览: getWindowsWithTitle, print, info
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 列出所有窗口。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### minimize_window(window_keyword)
- 说明: 通用：最小化第一个标题包含 window_keyword 的可见窗口。
- 邻近注释: 最小、最大化窗口
- 参数: window_keyword
- 返回推断: bool
- 关注点: 选择集
- 调用概览: print, minimize, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：通用：最小化第一个标题包含 window_keyword 的可见窗口。。邻近注释提示：最小、最大化窗口。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### maximize_autocad_window(window_keyword)
- 说明: 强制最大化第一个标题包含 window_keyword 的可见窗口。
- 参数: window_keyword
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待, 窗口/输入, 选择集
- 调用概览: sleep, info, ShowWindow, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：强制最大化第一个标题包含 window_keyword 的可见窗口。。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### set_dwg_units_precision()
- 说明: 设置当前 DWG 文件的单位及精度：
- 邻近注释: &&&% 文字样式 | &&% 设置单位精度
- 参数: （无）
- 关注点: COM, 日志/测试
- 关键调用: C.doc
- 调用概览: SetVariable, print, info
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置当前 DWG 文件的单位及精度：。邻近注释提示：&&&% 文字样式；&&% 设置单位精度。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### jd()
- 说明: （无）
- 参数: （无）
- 调用概览: set_dwg_units_precision
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### list_dim_styles()
- 说明: 列出当前 DWG 文件中所有标注样式名称。
- 邻近注释: &&% 列出标注样式
- 参数: （无）
- 返回推断: list,object
- 关注点: 日志/测试
- 调用概览: print, info, Item, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：列出当前 DWG 文件中所有标注样式名称。。邻近注释提示：&&% 列出标注样式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_current_dimstyle_via_command(style_name)
- 说明: 使用命令行方式设置当前标注样式，兼容天正。
- 邻近注释: &&% 设置当前标注样式
- 参数: style_name
- 关注点: COM, 日志/测试
- 调用概览: SendCommand, info
- 理解: 主要用于更新/设置相关逻辑。依据注释：使用命令行方式设置当前标注样式，兼容天正。。邻近注释提示：&&% 设置当前标注样式。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_current_text_style(style_name)
- 说明: 设置当前文字样式（通过 COM 接口方式）。
- 邻近注释: &&% 设置当前文字样式
- 参数: style_name
- 关注点: 日志/测试
- 调用概览: Item, info
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置当前文字样式（通过 COM 接口方式）。。邻近注释提示：&&% 设置当前文字样式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### huoqu_ziti_style()
- 说明: （无）
- 邻近注释: &&% 获取字体样式
- 参数: （无）
- 返回推断: object
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 获取字体样式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### create_text_style(sty_name, ziti)
- 说明: 在当前 DWG 中创建（或更新）一个中文文字样式。
- 邻近注释: &&% 创建文字样式
- 参数: sty_name, ziti
- 关注点: COM, 日志/测试
- 调用概览: Item, info, SetFont, Add
- 理解: 主要用于创建/插入相关逻辑。依据注释：在当前 DWG 中创建（或更新）一个中文文字样式。。邻近注释提示：&&% 创建文字样式。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_text_style_onlyshx(style_name, font_file, big_font_file)
- 说明: C:/Program Files/Autodesk/AutoCAD 2021/Fonts查找可用shx字体    
- 邻近注释: &&% 设置SHX文字样式
- 参数: style_name, font_file, big_font_file
- 返回推断: bool
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, info, Item, Add, isinstance
- 理解: 主要用于更新/设置相关逻辑。依据注释：C:/Program Files/Autodesk/AutoCAD 2021/Fonts查找可用shx字体    。邻近注释提示：&&% 设置SHX文字样式。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_text_style(style_name, font_file, big_font_file)
- 说明: 设置CAD中文字样式：英文shx文件 + 中文大字体文件
- 邻近注释: &&% 设置文字样式
- 参数: style_name, font_file, big_font_file
- 返回推断: bool
- 关注点: 日志/测试
- 调用概览: info, Item, Add
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置CAD中文字样式：英文shx文件 + 中文大字体文件。邻近注释提示：&&% 设置文字样式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### rename_conflicting_text_styles(file1_path, file2_path, suffix, retry_delay, max_retries)
- 说明: 在两个 DWG 中找出同名（用户）文字样式，
- 邻近注释: &&% 重命名冲突文字样式
- 参数: file1_path, file2_path, suffix, retry_delay, max_retries
- 返回推断: None
- 关注点: COM, 文件, 日志/测试, 时间/等待, 进程
- 调用概览: EnsureDispatch, Open, abspath, info, Save, Close, print, SendCommand, range, discard, add, sleep...
- 理解: 主要用于更新/设置相关逻辑。依据注释：在两个 DWG 中找出同名（用户）文字样式，。邻近注释提示：&&% 重命名冲突文字样式。实现特征：执行 DWG 打开；执行保存；执行关闭文档；通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### transfer_props_by_matchprop(entity, Ob, max_try, delay)
- 说明: （无）
- 邻近注释: 将一个对象属性传给多个对象 | &&% 格式刷属性传递
- 参数: entity, Ob, max_try, delay
- 返回推断: None,bool,tuple
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 调用概览: chr, li, GetBoundingBox, expand_rectangle, range, info, sleep, SendCommand, wait_idle, GetAcadState, abs, highlight_entity_by_bbox...
- 理解: 主要用于处理相关逻辑。邻近注释提示：将一个对象属性传给多个对象；&&% 格式刷属性传递。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### run_dual_threads_1(f1, f2, f1_args, f1_kwargs, f2_args, f2_kwargs, timeout_sec)
- 说明: 通用“双线程-GUI”调度器
- 邻近注释: &&% 双线程生成器 | &&% 双线程运行1
- 参数: f1, f2, f1_args, f1_kwargs, f2_args, f2_kwargs, timeout_sec
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 调用概览: Event, Thread, time, start, join, is_set, set, info, print
- 理解: 主要用于打开/读取相关逻辑。依据注释：通用“双线程-GUI”调度器。邻近注释提示：&&% 双线程生成器；&&% 双线程运行1。实现特征：通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### cancel_cad_selection(attempts, delay)
- 说明: （无）
- 邻近注释: &&% 取消CAD选择
- 参数: attempts, delay
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待
- 调用概览: range, print, highlight_entities_in_window, info, sleep
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 取消CAD选择。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### close_wps_window_by_click(title_keyword, offset_x, offset_y, pause_before)
- 说明: 在标题包含 title_keyword 的窗口右上角点击一次（×），尝试关闭该窗口。
- 邻近注释: &&&% 打印辅助
- 参数: title_keyword, offset_x, offset_y, pause_before
- 返回推断: bool
- 关注点: 时间/等待, 窗口/输入, 选择集
- 调用概览: EnumWindows, GetWindowRect, sleep, click, node, IsWindowVisible, GetWindowText, lower, append
- 理解: 主要用于关闭/终止相关逻辑。依据注释：在标题包含 title_keyword 的窗口右上角点击一次（×），尝试关闭该窗口。。邻近注释提示：&&&% 打印辅助。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### min_w()
- 说明: （无）
- 邻近注释: &&&% 测试辅助 | &&% 最小化窗口
- 参数: （无）
- 关注点: 窗口/输入
- 调用概览: keybd_event
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&&% 测试辅助；&&% 最小化窗口。
- 风险: 依赖窗口/输入焦点，易受环境影响
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境

### ql()
- 说明: （无）
- 邻近注释: &&% 清除测试图层
- 参数: （无）
- 调用概览: ensure_layer
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 清除测试图层。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### srhd(*args)
- 说明: 在模型空间绘制点并标注序号，支持以下调用形式：
- 邻近注释: &&% 模型空间画点
- 参数: *args
- 返回推断: None,str
- 关注点: COM, 几何, 日志/测试
- 调用概览: enumerate, Item, len, isinstance, Add, info, print, vtpnt, AddPoint, AddText, all, str
- 理解: 主要用于处理相关逻辑。依据注释：在模型空间绘制点并标注序号，支持以下调用形式：。邻近注释提示：&&% 模型空间画点。实现特征：创建文字对象；创建点对象；涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### srhd_p(*args)
- 说明: 在图纸空间绘制点和编号，支持：
- 邻近注释: &&% 图纸空间画点
- 参数: *args
- 返回推断: None,str
- 关注点: COM, 几何, 日志/测试
- 调用概览: enumerate, Item, len, isinstance, Add, info, print, vtpnt, AddPoint, AddText, all, str
- 理解: 主要用于处理相关逻辑。依据注释：在图纸空间绘制点和编号，支持：。邻近注释提示：&&% 图纸空间画点。实现特征：创建文字对象；创建点对象；涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### comtomath(LBcom)
- 说明: （无）
- 邻近注释: &&% COM点转数学点
- 参数: LBcom
- 返回推断: object
- 调用概览: range, len, append
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% COM点转数学点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### p()
- 说明: （无）
- 参数: （无）
- 返回推断: object
- 调用概览: li, pmxz, comtomath, print
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### fuzhi_chakan(LBcom, K)
- 说明: （无）
- 邻近注释: &&% 隔远查看 | &&% 复制查看
- 参数: LBcom, K
- 返回推断: object
- 关注点: COM, 文件, 日志/测试
- 调用概览: Copy, vtpnt, Move, append, info
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 隔远查看；&&% 复制查看。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### celiang_wenzichangdu(TEXTCOM)
- 说明: （无）
- 邻近注释: &&% 测量文字长度
- 参数: TEXTCOM
- 返回推断: object
- 关注点: 几何, 文件
- 调用概览: Copy, vtpnt, abs, Delete
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 测量文字长度。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### celiang_wenzichangdu_write(ZF, style, height, scalefactor)
- 说明: （无）
- 邻近注释: 测量新写文字长度 | &&% 写入并测量文字长度
- 参数: ZF, style, height, scalefactor
- 返回推断: object
- 关注点: COM, 文件
- 调用概览: AddText, celiang_wenzichangdu, Delete, vtpnt
- 理解: 主要用于保存/写入相关逻辑。邻近注释提示：测量新写文字长度；&&% 写入并测量文字长度。实现特征：创建文字对象。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### qingkong_wenjianjia(FolderPath)
- 说明: （无）
- 邻近注释: 清空文件夹 | &&% 清空文件夹
- 参数: FolderPath
- 关注点: 文件, 日志/测试
- 调用概览: listdir, join, isfile, info, remove
- 理解: 主要用于处理相关逻辑。邻近注释提示：清空文件夹；&&% 清空文件夹。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### get_bbox_info(com_obj)
- 说明: 获取传入 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）的外包盒信息，
- 邻近注释: &&&% 包围盒工具 | &&% 返回对象外包盒的长，宽，横竖向，角点信息 | &&% 获取包围盒信息
- 参数: com_obj
- 返回: (length, width, orientation)
- 关注点: 几何, 日志/测试
- 调用概览: max, min, GetBoundingBox, info
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取传入 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）的外包盒信息，。邻近注释提示：&&&% 包围盒工具；&&% 返回对象外包盒的长，宽，横竖向，角点信息；&&% 获取包围盒信息。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### bbox_orientation_flag(com_obj)
- 说明: 判断任意 COM 对象的外包盒是竖向、横向还是正方形：
- 邻近注释: &&% 包围盒方向标志
- 参数: com_obj
- 返回: int -- 竖向返回 1，横向或正方形返回 0
- 关注点: 几何
- 调用概览: GetBoundingBox, abs
- 理解: 主要用于处理相关逻辑。依据注释：判断任意 COM 对象的外包盒是竖向、横向还是正方形：。邻近注释提示：&&% 包围盒方向标志。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### group_bbox_corners(com_objs, max_retry, delay)
- 说明: 【通用加强版】计算一组 COM 对象的整体外包盒，并按顺序返回四个角点。
- 邻近注释: &&% 获取多个对象的外包盒数据
- 参数: com_objs, max_retry, delay
- 返回: 四元组：(左下, 右上, 左上, 右下)
- 关注点: COM, 几何, 文件, 时间/等待
- 调用概览: float, range, Update, GetBoundingBox, hasattr, list, sleep
- 理解: 主要用于处理相关逻辑。依据注释：【通用加强版】计算一组 COM 对象的整体外包盒，并按顺序返回四个角点。。邻近注释提示：&&% 获取多个对象的外包盒数据。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### bbox_center_2(e)
- 说明: （无）
- 邻近注释: &&% 从两点绘制矩形 | &&% 包围盒中心2D
- 参数: e
- 返回推断: tuple
- 关注点: 几何
- 调用概览: GetBoundingBox, tuple
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 从两点绘制矩形；&&% 包围盒中心2D。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### bbox_center_3(ent)
- 说明: 返回实体外包盒中心 (cx, cy, cz)
- 邻近注释: &&% 包围盒中心3D
- 参数: ent
- 返回推断: tuple
- 关注点: 几何
- 调用概览: GetBoundingBox
- 理解: 主要用于处理相关逻辑。依据注释：返回实体外包盒中心 (cx, cy, cz)。邻近注释提示：&&% 包围盒中心3D。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### safe_get_bbox(ent, max_retry, delay)
- 说明: 【通用加强版】安全获取 AutoCAD 图元外包盒 (GetBoundingBox)
- 邻近注释: &&% 安全获取包围盒
- 参数: ent, max_retry, delay
- 返回: (min_point, max_point) 元组，坐标为 (x, y, z)。
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 调用概览: range, Update, GetBoundingBox, hasattr, list, sleep
- 理解: 主要用于获取/选择相关逻辑。依据注释：【通用加强版】安全获取 AutoCAD 图元外包盒 (GetBoundingBox)。邻近注释提示：&&% 安全获取包围盒。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### analyze_dwg_objects_status()
- 说明: 分析当前激活DWG文件中的对象状态
- 邻近注释: &&% dwg状态分析函数
- 参数: （无）
- 返回: dict: {
- 关注点: COM, 几何, 日志/测试, 选择集
- 调用概览: info, ss_select, len, error, values, sorted, items, get
- 理解: 主要用于处理相关逻辑。依据注释：分析当前激活DWG文件中的对象状态。邻近注释提示：&&% dwg状态分析函数。实现特征：涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

## library/cad_geometry.py
- 模块说明: 第三部分 线面分析
### compute_line_angle(line)
- 说明: 计算直线的方向角（单位：度），基于 StartPoint / EndPoint。
- 邻近注释: &&&% 角度计算 | &&% 计算直线角度
- 参数: line
- 返回推断: NoneType,object
- 关注点: 几何
- 调用概览: atan2, degrees, print
- 理解: 主要用于计算/测量相关逻辑。依据注释：计算直线的方向角（单位：度），基于 StartPoint / EndPoint。。邻近注释提示：&&&% 角度计算；&&% 计算直线角度。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_point(pt)
- 说明: 在模型空间绘制一个 AutoCAD 点实体。
- 邻近注释: &&&% 基础绘图 | &&% 绘制点
- 参数: pt
- 返回: 新创建的 Point 对象；失败时返回 None
- 关注点: 几何, 日志/测试
- 调用概览: AddPoint, vtpnt, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：在模型空间绘制一个 AutoCAD 点实体。。邻近注释提示：&&&% 基础绘图；&&% 绘制点。实现特征：创建点对象。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_line(p1, p2)
- 说明: 在模型空间中绘制从 p1 到 p2 的直线段。
- 邻近注释: &&% 绘制直线
- 参数: p1, p2
- 返回: 新创建的直线对象（COM 对象）
- 关注点: 日志/测试
- 调用概览: AddLine, vtpnt, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：在模型空间中绘制从 p1 到 p2 的直线段。。邻近注释提示：&&% 绘制直线。实现特征：创建直线对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_circle(center, radius)
- 说明: 以 center 为圆心、radius 为半径绘制圆。
- 邻近注释: &&% 绘制圆
- 参数: center, radius
- 返回: 新创建的 Circle 对象；失败时返回 None
- 关注点: 日志/测试
- 调用概览: AddCircle, vtpnt, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：以 center 为圆心、radius 为半径绘制圆。。邻近注释提示：&&% 绘制圆。实现特征：创建圆对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_regular_polygon(center, radius, sides)
- 说明: 绘制正多边形（LWPolyline，已闭合）
- 邻近注释: &&% 绘制正多边形
- 参数: center, radius, sides
- 返回推断: NoneType,object
- 关注点: COM, 几何, 日志/测试
- 调用概览: range, print, extend, VARIANT, AddLightWeightPolyline, info, cos, sin
- 理解: 主要用于创建/插入相关逻辑。依据注释：绘制正多边形（LWPolyline，已闭合）。邻近注释提示：&&% 绘制正多边形。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### prioritize_horizontal(lines, tol)
- 说明: 将列表中所有“水平”直线段（起点和终点的 y 差小于 tol）放在最前面，
- 邻近注释: &&% 优先水平线
- 参数: lines, tol
- 返回推断: tuple
- 关注点: 几何
- 调用概览: abs, append
- 理解: 主要用于处理相关逻辑。依据注释：将列表中所有“水平”直线段（起点和终点的 y 差小于 tol）放在最前面，。邻近注释提示：&&% 优先水平线。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_spline_length_by_conversion(spline_entity)
- 说明: 将样条曲线对象复制、高亮并通过 _SPLINEDIT 转为多段线，
- 邻近注释: &&&% 曲线处理 | &&% 获取样条曲线长度
- 参数: spline_entity
- 返回: 样条曲线转换后的长度值（float）
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 调用概览: Copy, highlight_entity_by_bbox, SendCommand, sleep, Item, hasattr, Delete, print, info
- 理解: 主要用于获取/选择相关逻辑。依据注释：将样条曲线对象复制、高亮并通过 _SPLINEDIT 转为多段线，。邻近注释提示：&&&% 曲线处理；&&% 获取样条曲线长度。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### estimate_ellipse_length(ellipse)
- 说明: 估算椭圆对象的长度（周长），使用 Ramanujan 公式。
- 邻近注释: &&% 估算椭圆周长
- 参数: ellipse
- 返回推断: NoneType,object
- 关注点: 日志/测试
- 调用概览: sqrt, info
- 理解: 主要用于计算/测量相关逻辑。依据注释：估算椭圆对象的长度（周长），使用 Ramanujan 公式。。邻近注释提示：&&% 估算椭圆周长。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_entity_geometry_info(obj)
- 说明: 根据图元类型返回其关键几何信息：
- 邻近注释: &&% 获取几何信息
- 参数: obj
- 返回推断: dict
- 关注点: 几何
- 调用概览: lower, dist, str, sqrt, getattr, GetFitPoint, get_spline_length_by_conversion
- 理解: 主要用于获取/选择相关逻辑。依据注释：根据图元类型返回其关键几何信息：。邻近注释提示：&&% 获取几何信息。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### points_on_line_at_distance_3d(p1, p2, px, distance)
- 说明: 已知 px 在由 p1->p2 确定的直线上，返回在该直线上与 px 距离为 distance 的两个点。
- 邻近注释: 在两点确定的方向上，返回与对象点指定距离的点 | &&% 直线定距点
- 参数: p1, p2, px, distance
- 返回推断: list
- 关注点: 几何
- 调用概览: sqrt, ValueError
- 理解: 主要用于计算/测量相关逻辑。依据注释：已知 px 在由 p1->p2 确定的直线上，返回在该直线上与 px 距离为 distance 的两个点。。邻近注释提示：在两点确定的方向上，返回与对象点指定距离的点；&&% 直线定距点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_fake_intersection_regions(lines, tol, real_tol)
- 说明: 查找伪相交区域：对于任意线段 A 的端点 P，若：
- 邻近注释: &&&% 交点计算 | 找出一组直线段内的伪相交区域 | &&% 查找伪交点区域
- 参数: lines, tol, real_tol
- 返回推断: object
- 关注点: COM, 几何, 日志/测试
- 调用概览: ensure_layer, print, max, hypot, min, tuple, append, info, round, point_to_line_distance, AddCircle, vtpnt
- 理解: 主要用于获取/选择相关逻辑。依据注释：查找伪相交区域：对于任意线段 A 的端点 P，若：。邻近注释提示：&&&% 交点计算；找出一组直线段内的伪相交区域；&&% 查找伪交点区域。实现特征：创建圆对象。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### lines_daduan(start_point, end_point)
- 说明: 这个命令对于避免天正墙体没有出现不相交的覆盖是非常重要的，直接应用天正的tlinebk
- 邻近注释: &&&% 打断与删除 | 把区域内的直线段交点打断 | &&% 直线打断
- 参数: start_point, end_point
- 关注点: COM
- 调用概览: SendCommand, chr
- 理解: 主要用于处理相关逻辑。依据注释：这个命令对于避免天正墙体没有出现不相交的覆盖是非常重要的，直接应用天正的tlinebk。邻近注释提示：&&&% 打断与删除；把区域内的直线段交点打断；&&% 直线打断。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### delete_duplicate_lines(lines, tol)
- 说明: 删除重复的直线段，仅保留每组中一条。
- 邻近注释: 找出一组直线段中的所有直线段中所有重复的线段并删除 | &&% 删除重复直线
- 参数: lines, tol
- 返回推断: bool,object
- 关注点: 几何, 日志/测试
- 调用概览: enumerate, info, all, range, is_duplicate, append, Delete, len, abs, zip, is_same_point
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除重复的直线段，仅保留每组中一条。。邻近注释提示：找出一组直线段中的所有直线段中所有重复的线段并删除；&&% 删除重复直线。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### delete_redundant_lines(lines, tol)
- 说明: 删除重复线段和局部重复线段，只保留每组中的一条。
- 邻近注释: 删除完全或局部重复线段 | &&% 删除冗余直线
- 参数: lines, tol
- 返回推断: bool,object
- 关注点: COM, 几何, 日志/测试
- 调用概览: set, len, range, info, abs, is_completely_duplicate, point_on_segment, add, is_locally_duplicate, Delete, is_same_point
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除重复线段和局部重复线段，只保留每组中的一条。。邻近注释提示：删除完全或局部重复线段；&&% 删除冗余直线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_isolated_intersections(LB, tol)
- 说明: 找出线段列表 LB 中的孤立线段，并计算它们与其它线段的所有交点。
- 邻近注释: 找出一组直线段中的孤立线段产生的交点 | &&% 查找孤立交点
- 参数: LB, tol
- 返回: intersections: 交点列表，每个元素是 (x, y, z)
- 调用概览: enumerate, Delete, abs, append, segment_intersection, same_point
- 理解: 主要用于获取/选择相关逻辑。依据注释：找出线段列表 LB 中的孤立线段，并计算它们与其它线段的所有交点。。邻近注释提示：找出一组直线段中的孤立线段产生的交点；&&% 查找孤立交点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_inner_point_of_polygon(polygon)
- 说明: 获取给定 polygon 的一个保证在其内部的点。
- 邻近注释: doc.sendcommand("TSpOutline"+chr(13)+"41849.69465957, 12250.50102376, 0"+chr(13)+chr(13)+chr(13)) | doc.sendcommand("TRoflna"+chr(13)+"0"+chr(13)) | &&% 获取多边形内点
- 参数: polygon
- 返回: (x, y): 内部点坐标元组
- 关注点: 几何
- 调用概览: representative_point, isinstance, ValueError
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取给定 polygon 的一个保证在其内部的点。。邻近注释提示：doc.sendcommand("TSpOutline"+chr(13)+"41849.69465957, 12250.50102376, 0"+chr(13)+chr(13)+chr(13))；doc.sendcommand("TRoflna"+chr(13)+"0"+chr(13))；&&% 获取多边形内点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_room_outline_from_point(x, y, z)
- 说明: 自动发送 TSpOutline 命令，从指定点获取房间轮廓。
- 邻近注释: &&% 获取房间轮廓
- 参数: x, y, z
- 关注点: COM, 日志/测试
- 调用概览: SendCommand, info, chr
- 理解: 主要用于获取/选择相关逻辑。依据注释：自动发送 TSpOutline 命令，从指定点获取房间轮廓。。邻近注释提示：&&% 获取房间轮廓。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### connect_lines_to_polyline_if_closed(lines, tol)
- 说明: 判断线段是否首尾连接成闭合多边形，如果是，则绘制PL多段线。
- 邻近注释: &&% 连接闭合多段线
- 参数: lines, tol
- 返回: 多段线对象，或 None。
- 关注点: COM, 几何, 日志/测试
- 调用概览: set, add, append, AddLightWeightPolyline, print, enumerate, distance, extend, vtFloat, info, Point
- 理解: 主要用于关闭/终止相关逻辑。依据注释：判断线段是否首尾连接成闭合多边形，如果是，则绘制PL多段线。。邻近注释提示：&&% 连接闭合多段线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### is_closed_polygon_from_lines(lines, tol)
- 说明: 判断一组 AutoCAD 直线段是否首尾连接形成闭合多边形。
- 邻近注释: &&% 判断闭合多边形
- 参数: lines, tol
- 返回: True 表示首尾闭合形成多边形，False 否则
- 关注点: 几何, 日志/测试
- 调用概览: set, add, enumerate, info, append, distance, len, Point
- 理解: 主要用于关闭/终止相关逻辑。依据注释：判断一组 AutoCAD 直线段是否首尾连接形成闭合多边形。。邻近注释提示：&&% 判断闭合多边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### same_point(p1, p2, tol)
- 说明: 判断两个点是否在容差范围内相同（只比较 X、Y 坐标）
- 邻近注释: &&% 判断同点
- 参数: p1, p2, tol
- 返回推断: object
- 调用概览: abs
- 理解: 主要用于处理相关逻辑。依据注释：判断两个点是否在容差范围内相同（只比较 X、Y 坐标）。邻近注释提示：&&% 判断同点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### same_line(ln1, ln2, tol)
- 说明: 判断两条线段 ln1 和 ln2 是否“相同”
- 邻近注释: &&% 判断同线
- 参数: ln1, ln2, tol
- 返回推断: object
- 关注点: 几何
- 调用概览: tuple, same_point
- 理解: 主要用于处理相关逻辑。依据注释：判断两条线段 ln1 和 ln2 是否“相同”。邻近注释提示：&&% 判断同线。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### calculate_absolute_angle(line, P, tol)
- 说明: 计算线段（line）从点 P 出发的绝对角度（0-360°）
- 邻近注释: &&% 计算绝对角度
- 参数: line, P, tol
- 返回推断: object
- 关注点: 几何
- 调用概览: tuple, same_point, degrees, atan2
- 理解: 主要用于计算/测量相关逻辑。依据注释：计算线段（line）从点 P 出发的绝对角度（0-360°）。邻近注释提示：&&% 计算绝对角度。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### calculate_relative_angle(line, P, current_line, tol)
- 说明: 计算当前参考线（current_line）与候选线段（line）之间的相对角度，
- 邻近注释: &&% 计算相对角度
- 参数: line, P, current_line, tol
- 返回推断: object
- 关注点: 几何
- 调用概览: tuple, same_point, angle, degrees, atan2
- 理解: 主要用于计算/测量相关逻辑。依据注释：计算当前参考线（current_line）与候选线段（line）之间的相对角度，。邻近注释提示：&&% 计算相对角度。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_lines_angle(lines, P, tol)
- 说明: 查找与指定点 P 共端点的所有线段，并按从 P 出发离开的绝对几何角度排序。
- 邻近注释: 函数：查找给定点P经过的线段，按照绝对角度排序 | &&% 按角度查找线段
- 参数: lines, P, tol
- 返回: 按绝对角度从小到大排序的共点线段列表。
- 关注点: COM, 几何, 日志/测试
- 调用概览: tuple, info, sort, print, abs, append, calculate_absolute_angle, getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：查找与指定点 P 共端点的所有线段，并按从 P 出发离开的绝对几何角度排序。。邻近注释提示：函数：查找给定点P经过的线段，按照绝对角度排序；&&% 按角度查找线段。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_lines_sharing_point(lines, P, current_line, tol)
- 说明: 查找与指定点 P 共端点的所有线段，并按从 current_line 逆时针旋转到其他线段的相对角度排序。
- 邻近注释: 函数：查找与P共点的线段，按照与当前线段的相对角度排序 | &&% 查找共点线段
- 参数: lines, P, current_line, tol
- 返回: 按相对角度从小到大排序的经过 P 的线段列表（current_line 亦包括其中）。
- 关注点: COM, 几何, 日志/测试
- 调用概览: tuple, sort, append, info, calculate_relative_angle, abs, getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：查找与指定点 P 共端点的所有线段，并按从 current_line 逆时针旋转到其他线段的相对角度排序。。邻近注释提示：函数：查找与P共点的线段，按照与当前线段的相对角度排序；&&% 查找共点线段。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_successor_line_max(current_line, lines, P, tol)
- 说明: 在给定共点 P 处，排除当前线段（current_line）后，
- 邻近注释: 函数：根据当前线段和共点 P，选择下一条后继线段（选择相对角度最大的那条），返回 (后继线段, 新共点) | &&% 查找最大转角后继线
- 参数: current_line, lines, P, tol
- 返回: (后继线段, 新共点)，若找不到合适的后继线段，则返回 (None, P)。
- 关注点: COM, 几何, 日志/测试
- 调用概览: find_lines_sharing_point, info, calculate_relative_angle, same_point, tuple
- 理解: 主要用于获取/选择相关逻辑。依据注释：在给定共点 P 处，排除当前线段（current_line）后，。邻近注释提示：函数：根据当前线段和共点 P，选择下一条后继线段（选择相对角度最大的那条），返回 (后继线段, 新共点)；&&% 查找最大转角后继线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_rightbottom_point(lines, tol)
- 说明: 从所有线段端点中，找出 y 值最小的点；若有多个，则选 x 最大的点作为最右下角点。
- 邻近注释: &&%##################### | 辅助函数：从所有线段中找出最右下角的点 | &&% 查找右下角点
- 参数: lines, tol
- 返回推断: NoneType,object
- 关注点: 几何, 日志/测试
- 调用概览: min, max, info, hasattr, append, tuple, abs
- 理解: 主要用于获取/选择相关逻辑。依据注释：从所有线段端点中，找出 y 值最小的点；若有多个，则选 x 最大的点作为最右下角点。。邻近注释提示：&&%#####################；辅助函数：从所有线段中找出最右下角的点；&&% 查找右下角点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_rightbottom_closed_polygon(lines, tol, max_steps)
- 说明: 利用所有线段构造封闭多边形：
- 邻近注释: &&% 查找右下角闭合多边形
- 参数: lines, tol, max_steps
- 返回: 构成封闭多边形的点列表（依次为每条边的终点），若无法构成则返回 None。
- 关注点: COM, 几何, 日志/测试
- 调用概览: find_rightbottom_point, find_lines_angle, info, tuple, same_point, print, find_successor_line_max, append, add, calculate_absolute_angle
- 理解: 主要用于关闭/终止相关逻辑。依据注释：利用所有线段构造封闭多边形：。邻近注释提示：&&% 查找右下角闭合多边形。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### draw_polygon_as_polyline(polygon, layer_name, tol)
- 说明: 将构造的多边形（polygon）转换为顶点序列，并在当前 AutoCAD 文档 doc 的 ModelSpace 中添加
- 邻近注释: 从com边或顶点坐标列表用PL复线绘制多边形 | &&% 绘制多边形
- 参数: polygon, layer_name, tol
- 返回: 成功时返回创建的多段线对象（PLINE），否则返回 None。
- 关注点: COM, 几何, 日志/测试
- 调用概览: isinstance, print, enumerate, tuple, VARIANT, same_point, append, info, extend, Item, AddPolyline, Update...
- 理解: 主要用于创建/插入相关逻辑。依据注释：将构造的多边形（polygon）转换为顶点序列，并在当前 AutoCAD 文档 doc 的 ModelSpace 中添加。邻近注释提示：从com边或顶点坐标列表用PL复线绘制多边形；&&% 绘制多边形。实现特征：涉及图层操作。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### is_nearly_equal(p1, p2, tol)
- 说明: （无）
- 邻近注释: ----------------------------------------------------- | 辅助函数：判断两个点是否近似相等（仅比较 x 和 y 坐标） | &&% 近似相等
- 参数: p1, p2, tol
- 返回推断: object
- 调用概览: abs
- 理解: 主要用于处理相关逻辑。邻近注释提示：-----------------------------------------------------；辅助函数：判断两个点是否近似相等（仅比较 x 和 y 坐标）；&&% 近似相等。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_successor_line_min(current_line, lines, P, tol)
- 说明: （无）
- 邻近注释: ----------------------------------------------------- | 寻找后继线段：在共点 P 处，从当前边之外的候选边中选择相对角度最小的边 | &&% 查找最小转角后继线
- 参数: current_line, lines, P, tol
- 返回推断: tuple
- 关注点: COM, 几何, 日志/测试
- 调用概览: tuple, info, calculate_relative_angle, is_nearly_equal, append, abs
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：-----------------------------------------------------；寻找后继线段：在共点 P 处，从当前边之外的候选边中选择相对角度最小的边；&&% 查找最小转角后继线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_outer_contour(lines, tol, max_steps)
- 说明: 获取一组直线段的外轮廓线
- 邻近注释: (3) | 获取一组直线段的外轮廓线 | &&% 获取外轮廓
- 参数: lines, tol, max_steps
- 返回: 外轮廓线构成的线段列表，如果无法构成封闭轮廓则返回空列表。
- 关注点: COM, 几何, 日志/测试
- 调用概览: find_rightbottom_point, info, find_lines_angle, tuple, is_nearly_equal, print, find_successor_line_min, append, add
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取一组直线段的外轮廓线。邻近注释提示：(3)；获取一组直线段的外轮廓线；&&% 获取外轮廓。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### deduplicate_vertices(vertices, tol)
- 说明: 去掉顶点列表中相邻重复的顶点：
- 邻近注释: &&% 顶点去重
- 参数: vertices, tol
- 返回: 处理后的顶点列表，只有中间连续重复的点被去除，保留闭合多边形的首尾重复。
- 调用概览: len, range, sqrt, append, same_point
- 理解: 主要用于移动/复制相关逻辑。依据注释：去掉顶点列表中相邻重复的顶点：。邻近注释提示：&&% 顶点去重。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### analyze_polygon_branches(PL, lines, p1, tol)
- 说明: 分析封闭多边形 PL 的分枝情况。PL 为封闭多边形的顶点列表（按逆时针顺序排列），
- 邻近注释: (4) | 获取最右下角的封闭多边形不影响其他封闭多边形的连续边的顶点列表 | &&% 分析多边形分支
- 参数: PL, lines, p1, tol
- 返回: 返回从 D1 到 D2（包含 D1 和 D2）的连续顶点序列，此序列包含了 LN 的顶点。
- 关注点: 几何
- 调用概览: len, is_multi_branch, print, deduplicate_vertices, index, list, any, append, reversed, tuple, same_point
- 理解: 主要用于处理相关逻辑。依据注释：分析封闭多边形 PL 的分枝情况。PL 为封闭多边形的顶点列表（按逆时针顺序排列），。邻近注释提示：(4)；获取最右下角的封闭多边形不影响其他封闭多边形的连续边的顶点列表；&&% 分析多边形分支。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### remove_lines_in_LBv(lines, LB_v, tol)
- 说明: 从 COM 线段列表 lines 中移除那些其两个顶点都在 LB_v 中的线段。
- 邻近注释: 根据输入的顶点列表判断，将lines的其顶点在该顶点列表的线段移出列表 | &&% 移除指定顶点线段
- 参数: lines, LB_v, tol
- 返回: 返回移除满足条件（即两端点都在 LB_v 中）的线段后剩余的线段列表。
- 关注点: COM, 几何, 文件, 日志/测试
- 调用概览: any, tuple, append, info, abs, same_point
- 理解: 主要用于删除/清理相关逻辑。依据注释：从 COM 线段列表 lines 中移除那些其两个顶点都在 LB_v 中的线段。。邻近注释提示：根据输入的顶点列表判断，将lines的其顶点在该顶点列表的线段移出列表；&&% 移除指定顶点线段。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### process_polygons(lines, tol, max_steps, layer_name)
- 说明: 递归提取并绘制直线段集 lines 中所有封闭多边形。
- 邻近注释: (5) | &&% 获取全部封闭多边形，但不完全 | &&% 处理多边形
- 参数: lines, tol, max_steps, layer_name
- 返回: (LB, LBcom, LB_yc)，其中：
- 关注点: 几何, 文件, 日志/测试
- 调用概览: info, find_rightbottom_point, find_rightbottom_closed_polygon, append, print, analyze_polygon_branches, draw_polygon_as_polyline, remove_lines_in_LBv, len
- 理解: 主要用于处理相关逻辑。依据注释：递归提取并绘制直线段集 lines 中所有封闭多边形。。邻近注释提示：(5)；&&% 获取全部封闭多边形，但不完全；&&% 处理多边形。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### extract_polygon_from_lines(lines, tol)
- 说明: 将表示封闭多边形边缘的线段（COM对象列表）转换为顶点列表（按顺序排列），
- 邻近注释: &&% 提取多边形
- 参数: lines, tol
- 返回: 顶点列表，如 [p1, p2, ..., pn]，其中 p1 表示多边形的起点（不重复列出闭合顶点）。
- 关注点: 几何, 文件
- 调用概览: list, range, tuple, print, len, remove, same_point, append, deduplicate_vertices
- 理解: 主要用于处理相关逻辑。依据注释：将表示封闭多边形边缘的线段（COM对象列表）转换为顶点列表（按顺序排列），。邻近注释提示：&&% 提取多边形。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### explode_polylines(LB)
- 说明: 对多段线列表 LB 中的每一个多段线，调用 .Explode() 方法，
- 邻近注释: 将多段线列表炸开为线段，返回线段列表 | &&% 炸开多段线
- 参数: LB
- 返回: 一个包含所有炸开后直线段 COM 对象的列表。
- 关注点: COM, 几何, 日志/测试
- 调用概览: Explode, append, getattr, info
- 理解: 主要用于处理相关逻辑。依据注释：对多段线列表 LB 中的每一个多段线，调用 .Explode() 方法，。邻近注释提示：将多段线列表炸开为线段，返回线段列表；&&% 炸开多段线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### subtract_line_sets(lines1, lines2, tol)
- 说明: 比较两个线段集合 lines1 和 lines2，返回 lines1 中那些不在 lines2 中的线段。
- 邻近注释: lines1 中那些不在 lines2 中的线段 | &&% 线段集相减
- 参数: lines1, lines2, tol
- 返回: lines1 中所有不与 lines2 中任意线段相同的线段构成的列表。
- 关注点: 几何
- 调用概览: same_line, append
- 理解: 主要用于更新/设置相关逻辑。依据注释：比较两个线段集合 lines1 和 lines2，返回 lines1 中那些不在 lines2 中的线段。。邻近注释提示：lines1 中那些不在 lines2 中的线段；&&% 线段集相减。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### process_final(lines, tol, max_steps, layer_name)
- 说明: （无）
- 邻近注释: (6) | &&% 获取全部封闭多边形 | &&% 最终处理
- 参数: lines, tol, max_steps, layer_name
- 返回推断: tuple
- 关注点: 几何, 日志/测试
- 调用概览: print, process_polygons, info, explode_polylines, subtract_line_sets, extract_polygon_from_lines, draw_polygon_as_polyline, append, len, Delete
- 理解: 主要用于处理相关逻辑。邻近注释提示：(6)；&&% 获取全部封闭多边形；&&% 最终处理。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_lwpolyline(coords3d, layer_name, width, color, closed)
- 说明: 根据一组 (x, y, z) 坐标点绘制轻量级多段线（LWPOLYLINE）。
- 参数: coords3d, layer_name, width, color, closed
- 返回推断: object
- 关注点: COM, 几何, 日志/测试
- 调用概览: alias, VARIANT, Item, extend, AddLightWeightPolyline, bool, info, Add, print
- 理解: 主要用于创建/插入相关逻辑。依据注释：根据一组 (x, y, z) 坐标点绘制轻量级多段线（LWPOLYLINE）。。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### draw_lwpolyline(coords3d, layer_name, width, color, closed)
- 说明: 【通用版】支持在 模型空间 或 任意布局空间 绘制。
- 参数: coords3d, layer_name, width, color, closed
- 返回推断: NoneType,object
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.doc
- 调用概览: alias, VARIANT, Item, extend, AddLightWeightPolyline, bool, Add, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：【通用版】支持在 模型空间 或 任意布局空间 绘制。。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_unique_vertices_from_pl_com(pl_com)
- 说明: 提取多段线的顶点列表，不重复连续线段的公共顶点，返回顶点列表。
- 邻近注释: 1 从com复线获取标准顶点坐标列表 | &&% 获取唯一顶点
- 参数: pl_com
- 返回: 顶点列表，每两个点构成一条线段，格式：[ (x1, y1, z1), (x2, y2, z2), ... ]
- 调用概览: range, append, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：提取多段线的顶点列表，不重复连续线段的公共顶点，返回顶点列表。。邻近注释提示：1 从com复线获取标准顶点坐标列表；&&% 获取唯一顶点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### convert_lines_to_points(segments)
- 说明: 将com线段列表转换为顶点列表，每条线段的两个端点作为一个独立的列表。
- 邻近注释: 2 将com线段转成顶点坐标列表，一根线段一个列表 | &&% 线段转点集
- 参数: segments
- 返回: 包含多个线段顶点的列表，每个线段是一个包含两个端点坐标的列表。
- 关注点: 几何
- 调用概览: tuple, append
- 理解: 主要用于转换/解析相关逻辑。依据注释：将com线段列表转换为顶点列表，每条线段的两个端点作为一个独立的列表。。邻近注释提示：2 将com线段转成顶点坐标列表，一根线段一个列表；&&% 线段转点集。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### merge_segments_new(LB, tol)
- 说明: 使用convert_lines_to_points 将线段实体转成顶点列表表达式后就可以使用此命令
- 邻近注释: 3 合并顶点列表表示的连续线段，允许多根断开的连续线段 | &&% 合并线段
- 参数: LB, tol
- 返回推断: object,tuple
- 调用概览: defaultdict, enumerate, append, len, deque, grow, round, next, list, abs, pop, key...
- 理解: 主要用于创建/插入相关逻辑。依据注释：使用convert_lines_to_points 将线段实体转成顶点列表表达式后就可以使用此命令。邻近注释提示：3 合并顶点列表表示的连续线段，允许多根断开的连续线段；&&% 合并线段。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_polyline(vertices, layer_name, tol, width, color, target_space)
- 说明: 【修正版 V3】绘制轻量多段线 (LWPolyline)
- 参数: vertices, layer_name, tol, width, color, target_space
- 返回推断: NoneType,object
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.doc
- 调用概览: retry_if_busy, getattr, error, same_point, VARIANT, AddLightWeightPolyline, len, extend, tuple, abs
- 理解: 主要用于创建/插入相关逻辑。依据注释：【修正版 V3】绘制轻量多段线 (LWPolyline)。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### lines_to_polylines(Lc, tol, layer_name, width, color)
- 说明: 将直线段合并为多段线 (空间自适应版)
- 邻近注释: 6 将多条直线段（允许不连续）连接成PL复线 | &&% 线段转多段线
- 参数: Lc, tol, layer_name, width, color
- 返回推断: list,object
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.li, C.doc
- 调用概览: info, convert_lines_to_points, merge_segments_new, li, stc, draw_polyline, error, len, append, get_attr, safe_delete, ObjectIDToObject
- 理解: 主要用于处理相关逻辑。依据注释：将直线段合并为多段线 (空间自适应版)。邻近注释提示：6 将多条直线段（允许不连续）连接成PL复线；&&% 线段转多段线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_min_point(obj)
- 说明: 获取任意对象的左下角坐标（通过其外包盒）。
- 邻近注释: 7 找到多段线的最左下角的点 | &&% 查找最小点
- 参数: obj
- 返回推断: tuple
- 关注点: 日志/测试
- 调用概览: GetBoundingBox, info
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取任意对象的左下角坐标（通过其外包盒）。。邻近注释提示：7 找到多段线的最左下角的点；&&% 查找最小点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_max_point(obj)
- 说明: 获取任意对象的右上角坐标（通过其外包盒）。
- 邻近注释: 8 找到多段线的最右上角的点 | &&% 查找最大点
- 参数: obj
- 返回推断: tuple
- 关注点: 日志/测试
- 调用概览: GetBoundingBox, info
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取任意对象的右上角坐标（通过其外包盒）。。邻近注释提示：8 找到多段线的最右上角的点；&&% 查找最大点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### distance(point1, point2)
- 说明: 计算两点之间的距离
- 邻近注释: &&% 计算距离
- 参数: point1, point2
- 返回推断: object
- 关注点: 几何
- 理解: 主要用于计算/测量相关逻辑。依据注释：计算两点之间的距离。邻近注释提示：&&% 计算距离。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### define_rectangle_by_diagonal(p1, p2)
- 说明: 使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。
- 邻近注释: 10 定义矩形 | &&% 定义矩形
- 参数: p1, p2
- 返回推断: tuple
- 关注点: 几何
- 调用概览: abs, max, min
- 理解: 主要用于计算/测量相关逻辑。依据注释：使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。。邻近注释提示：10 定义矩形；&&% 定义矩形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### define_rectangle_by_diagonal_x(p1, p2)
- 说明: 使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。
- 邻近注释: &&% 定义矩形X
- 参数: p1, p2
- 返回推断: object
- 关注点: 几何
- 调用概览: abs, max, min
- 理解: 主要用于计算/测量相关逻辑。依据注释：使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。。邻近注释提示：&&% 定义矩形X。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### expand_rectangle(p1, p2, offset)
- 说明: 给定矩形框的两个对角点（p1 和 p2），
- 参数: p1, p2, offset
- 返回推断: tuple
- 关注点: 几何
- 调用概览: sorted
- 理解: 主要用于计算/测量相关逻辑。依据注释：给定矩形框的两个对角点（p1 和 p2），。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### parse_rectangle_points(*args)
- 说明: 接收多种坐标格式输入，统一解析为矩形四角点：
- 参数: *args
- 返回: (左下, 右上, 左上, 右下)，每个为三元组 (x, y, z)
- 关注点: 几何, 日志/测试
- 调用概览: min, max, isinstance, all, info, len, ValueError
- 理解: 主要用于转换/解析相关逻辑。依据注释：接收多种坐标格式输入，统一解析为矩形四角点：。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_rectangular_polylines(min_side, area_tolerance)
- 说明: 【智能筛选】获取所有“矩形”多段线 (兼容轻量线和老式线)。
- 邻近注释: &&&% 模型空间选出矩形多段线
- 参数: min_side, area_tolerance
- 返回: List[COMObject]: 筛选出的矩形多段线列表
- 关注点: 几何, 日志/测试, 选择集
- 调用概览: info, select_polyline, extend, select_polyline_chuantong, GetBoundingBox, abs, len, get_obj_loc, getattr, append, max, min
- 理解: 主要用于获取/选择相关逻辑。依据注释：【智能筛选】获取所有“矩形”多段线 (兼容轻量线和老式线)。。邻近注释提示：&&&% 模型空间选出矩形多段线。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### get_layout_rectangular_polylines_coords(layout_name, min_side)
- 说明: 【早期绑定专用】基于 get_attr 的矩形分析 (已集成 sys_logger)
- 邻近注释: continue | sys_logger.info(f"\n✅ [扫描结束] 最终找到 {len(results)} 个矩形") | return results
- 参数: layout_name, min_side
- 返回推断: list,object
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.doc
- 调用概览: info, enumerate, Item, error, get_attr, list, len, min, max, append, warning, str...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【早期绑定专用】基于 get_attr 的矩形分析 (已集成 sys_logger)。邻近注释提示：continue；sys_logger.info(f"\n✅ [扫描结束] 最终找到 {len(results)} 个矩形")；return results。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### generate_name_and_ratio_from_com(comobj, A3dy, Fandy, tol)
- 说明: 【V5.0 强制兜底版】
- 邻近注释: &&&% 打印分析 | &&&%  分析打印线20260110
- 参数: comobj, A3dy, Fandy, tol
- 返回推断: int,tuple
- 关注点: 日志/测试
- 调用概览: float, enumerate, getattr, GetBoundingBox, abs, max, min
- 理解: 主要用于处理相关逻辑。依据注释：【V5.0 强制兜底版】。邻近注释提示：&&&% 打印分析；&&&%  分析打印线20260110。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_cad_app()
- 说明: 连接 CAD
- 邻近注释: &&% 打印数据分析
- 参数: （无）
- 返回推断: NoneType,object
- 关注点: COM, 进程
- 调用概览: GetActiveObject, print
- 理解: 主要用于获取/选择相关逻辑。依据注释：连接 CAD。邻近注释提示：&&% 打印数据分析。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_dimensions(ent)
- 说明: 获取实体长宽（长边在前）
- 参数: ent
- 返回推断: tuple
- 调用概览: GetBoundingBox, abs, max, min
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取实体长宽（长边在前）。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_llcorner(com_list, cha_Y)
- 说明: 按 BoundingBox 左下角坐标排序：
- 参数: com_list, cha_Y
- 返回推断: object
- 调用概览: sort, append, len, GetBoundingBox, sorted, float, abs
- 理解: 主要用于处理相关逻辑。依据注释：按 BoundingBox 左下角坐标排序：。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### main()
- 说明: （无）
- 参数: （无）
- 返回推断: None
- 关注点: COM, 日志/测试, 选择集
- 调用概览: get_cad_app, print, Add, sort_coms_by_llcorner, info, enumerate, Delete, SelectOnScreen, Item, get_dimensions, rstrip, range...
- 理解: 主要用于处理相关逻辑。实现特征：涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### generate_relation_list(data_list)
- 说明: （无）
- 参数: data_list
- 返回推断: object
- 调用概览: enumerate, float, append, abs, min
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### check_strict_standard_size(comobj, tol)
- 说明: 【函数编号】: MAP-CHECK-SIZE-004
- 邻近注释: &&&% 选择标准打印区域
- 参数: comobj, tol
- 返回推断: int,object
- 关注点: 几何, 日志/测试
- 调用概览: enumerate, find_min_point, find_max_point, define_rectangle_by_diagonal, abs, info
- 理解: 主要用于测试/校验相关逻辑。依据注释：【函数编号】: MAP-CHECK-SIZE-004。邻近注释提示：&&&% 选择标准打印区域。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### check_strict_standard_size(comobj, tol)
- 说明: 【修正版 V5.0】
- 参数: comobj, tol
- 返回推断: int,tuple
- 调用概览: enumerate, GetBoundingBox, abs, max, min, float, split
- 理解: 主要用于测试/校验相关逻辑。依据注释：【修正版 V5.0】。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### polyline_sort(polyline_list)
- 说明: 对com多段线按照特定规则进行排序
- 邻近注释: &&% 多段线排序
- 参数: polyline_list
- 返回推断: object
- 关注点: 几何
- 调用概览: sort, find_min_point, len, sorted, abs
- 理解: 主要用于处理相关逻辑。依据注释：对com多段线按照特定规则进行排序。邻近注释提示：&&% 多段线排序。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### plcom_to_coor(plines)
- 说明: 接受多根轻量级多段线或常规多段线的 COM 对象列表，返回它们的坐标列表及闭合状态。
- 邻近注释: &&&%  *** 3 将PLcom线列表的坐标信息存储 | &&% 多段线转坐标
- 参数: plines
- 返回推断: object
- 关注点: COM, 日志/测试
- 调用概览: ensure_list, list, append, range, getattr, len, info
- 理解: 主要用于处理相关逻辑。依据注释：接受多根轻量级多段线或常规多段线的 COM 对象列表，返回它们的坐标列表及闭合状态。。邻近注释提示：&&&%  *** 3 将PLcom线列表的坐标信息存储；&&% 多段线转坐标。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### plcoor_to_com(coord_info, layer_name, width, color)
- 说明: 在当前 DWG 中根据坐标和封闭标志绘制多条轻量级多段线。
- 邻近注释: 4 从坐标信息列表返回PLcom线列表 | &&% 坐标转多段线
- 参数: coord_info, layer_name, width, color
- 返回推断: object
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, ZoomExtents, info, Item, VARIANT, AddLightWeightPolyline, bool, append, Add, extend, len
- 理解: 主要用于处理相关逻辑。依据注释：在当前 DWG 中根据坐标和封闭标志绘制多条轻量级多段线。。邻近注释提示：4 从坐标信息列表返回PLcom线列表；&&% 坐标转多段线。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### panduan_shuxiangkuang(polyline)
- 说明: （无）
- 邻近注释: 5 确定多段线打印框是否竖向 | &&% 判断竖向框
- 参数: polyline
- 返回推断: bool
- 关注点: 几何
- 调用概览: find_min_point, find_max_point, abs
- 理解: 主要用于处理相关逻辑。邻近注释提示：5 确定多段线打印框是否竖向；&&% 判断竖向框。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### tongyi_tufu(LB, TFname)
- 说明: 将打印线列表的每根线对应的图纸尺寸统一为一个TFname
- 邻近注释: 6 统一为A2的图幅打印 | &&% 统一图幅
- 参数: LB, TFname
- 返回推断: object
- 调用概览: append
- 理解: 主要用于处理相关逻辑。依据注释：将打印线列表的每根线对应的图纸尺寸统一为一个TFname。邻近注释提示：6 统一为A2的图幅打印；&&% 统一图幅。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### simplify_polygon(poly, tol)
- 说明: 简化多边形顶点列表：如果某顶点 P 与其前后两点共线（在容差 tol 范围内），则将其移除。
- 邻近注释: 消除多边形的伪边点 | &&% 简化多边形
- 参数: poly, tol
- 返回: 简化后的顶点列表（同样保留首尾是否闭合的形式，不会自动去重首尾）
- 关注点: 几何
- 调用概览: len, range, abs, is_colinear
- 理解: 主要用于处理相关逻辑。依据注释：简化多边形顶点列表：如果某顶点 P 与其前后两点共线（在容差 tol 范围内），则将其移除。。邻近注释提示：消除多边形的伪边点；&&% 简化多边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### normalize_polygon(polygon)
- 说明: 标准化多边形顶点列表：  
- 邻近注释: 1. 标准化多边形顶点列表，去掉相邻和首尾重复点 | &&% 标准化多边形
- 参数: polygon
- 返回: 去重后的顶点列表
- 关注点: 几何
- 调用概览: pop, append, len
- 理解: 主要用于处理相关逻辑。依据注释：标准化多边形顶点列表：  。邻近注释提示：1. 标准化多边形顶点列表，去掉相邻和首尾重复点；&&% 标准化多边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_adjacent_points(polygon, p)
- 说明: 在多边形 polygon 中返回顶点 p 的前后相邻点（支持循环）。
- 邻近注释: 2. 找到某顶点的前驱/后继（按循环多边形） | &&% 获取相邻点
- 参数: polygon, p
- 返回推断: tuple
- 关注点: 几何
- 调用概览: normalize_polygon, ValueError, index, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：在多边形 polygon 中返回顶点 p 的前后相邻点（支持循环）。。邻近注释提示：2. 找到某顶点的前驱/后继（按循环多边形）；&&% 获取相邻点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### point_in_polygon(pt, polygon)
- 说明: 判断三维点 pt=(x,y,z) 在多边形 polygon 的 XY 投影内否。
- 邻近注释: 3. 点是否在多边形内部（射线法，仅在 XY 平面判断） | &&% 点在多边形内
- 参数: pt, polygon
- 返回推断: object
- 关注点: 几何
- 调用概览: len, range, normalize_polygon
- 理解: 主要用于处理相关逻辑。依据注释：判断三维点 pt=(x,y,z) 在多边形 polygon 的 XY 投影内否。。邻近注释提示：3. 点是否在多边形内部（射线法，仅在 XY 平面判断）；&&% 点在多边形内。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### line_segment_intersection_2d(p, d, a, b, tol)
- 说明: 计算射线 L(t)=p + t·d 与线段 AB 在 XY 平面上的交点。
- 邻近注释: 4. 无穷直线 vs 线段在 XY 平面相交 | &&% 线段相交
- 参数: p, d, a, b, tol
- 返回推断: NoneType,tuple
- 调用概览: abs
- 理解: 主要用于处理相关逻辑。依据注释：计算射线 L(t)=p + t·d 与线段 AB 在 XY 平面上的交点。。邻近注释提示：4. 无穷直线 vs 线段在 XY 平面相交；&&% 线段相交。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_auxiliary_point(p, p_prev, p_next, polygon, tol)
- 说明: 对于多边形顶点 p 及其前后相邻点 p_prev, p_next，
- 邻近注释: 5. 计算 p 和其相邻点中点 c，如果 c 内部则返回 c，否则沿 p->c 的射线找到第一个交点 | &&% 获取辅助点
- 参数: p, p_prev, p_next, polygon, tol
- 返回推断: object,tuple
- 关注点: 几何
- 调用概览: point_in_polygon, hypot, normalize_polygon, range, sort, RuntimeError, len, line_segment_intersection_2d, abs, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：对于多边形顶点 p 及其前后相邻点 p_prev, p_next，。邻近注释提示：5. 计算 p 和其相邻点中点 c，如果 c 内部则返回 c，否则沿 p->c 的射线找到第一个交点；&&% 获取辅助点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### concavity_measure(p, p_prev, p_next, q)
- 说明: 给定 p, p_prev, p_next, q（均为 (x,y,z)），
- 邻近注释: 6. 计算 p 点的“凹凸度量角” | &&% 凹凸度量
- 参数: p, p_prev, p_next, q
- 返回推断: object
- 关注点: 几何
- 调用概览: angle_of, degrees, atan2
- 理解: 主要用于计算/测量相关逻辑。依据注释：给定 p, p_prev, p_next, q（均为 (x,y,z)），。邻近注释提示：6. 计算 p 点的“凹凸度量角”；&&% 凹凸度量。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### concavity_angle(p, polygon)
- 说明: 直接计算多边形 polygon 上顶点 p 的凹凸度量角。
- 邻近注释: 7. 直接给出 p 在多边形上的度量角 | &&% 凹凸角
- 参数: p, polygon
- 返回推断: object
- 关注点: 几何
- 调用概览: get_adjacent_points, get_auxiliary_point, concavity_measure
- 理解: 主要用于计算/测量相关逻辑。依据注释：直接计算多边形 polygon 上顶点 p 的凹凸度量角。。邻近注释提示：7. 直接给出 p 在多边形上的度量角；&&% 凹凸角。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### split_orthogonal_hexagon(polygon, tol)
- 说明: 将正交六边形 polygon 按凹顶点所在水平线切成两个矩形。
- 邻近注释: 8.合理分割PL正交六边形 | &&% 水平分割六边形
- 参数: polygon, tol
- 返回推断: object
- 关注点: 几何
- 调用概览: normalize_polygon, len, range, index, ValueError, RuntimeError, append, area2d, abs, concavity_angle
- 理解: 主要用于处理相关逻辑。依据注释：将正交六边形 polygon 按凹顶点所在水平线切成两个矩形。。邻近注释提示：8.合理分割PL正交六边形；&&% 水平分割六边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### split_orthogonal_hexagon_vertical(polygon, tol)
- 说明: 将正交六边形 polygon 按凹顶点所在竖线切成两个矩形。
- 邻近注释: &&% 竖向分割六边形
- 参数: polygon, tol
- 返回: (rect1, rect2)，面积小的放前面。
- 关注点: 几何
- 调用概览: normalize_polygon, len, range, index, ValueError, RuntimeError, append, area2d, abs, concavity_angle
- 理解: 主要用于处理相关逻辑。依据注释：将正交六边形 polygon 按凹顶点所在竖线切成两个矩形。。邻近注释提示：&&% 竖向分割六边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### area_of(verts)
- 说明: 多边形面积计算（顶点首尾闭合或不闭合均可）
- 邻近注释: 合理分割PL正交六边形 | &&% 计算面积
- 参数: verts
- 返回推断: object
- 调用概览: len, range, abs
- 理解: 主要用于计算/测量相关逻辑。依据注释：多边形面积计算（顶点首尾闭合或不闭合均可）。邻近注释提示：合理分割PL正交六边形；&&% 计算面积。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### split_hexagon_combined(polygon, tol, simplify_tol)
- 说明: 合理分割一个正交（近似）六边形 PL：
- 邻近注释: &&% 综合分割六边形
- 参数: polygon, tol, simplify_tol
- 返回: 四个矩形的顶点列表：最小矩形、其同组矩形、次小矩形、其同组矩形
- 关注点: 几何
- 调用概览: simplify_polygon, split_orthogonal_hexagon, split_orthogonal_hexagon_vertical, isinstance, get_unique_vertices_from_pl_com, area_of
- 理解: 主要用于处理相关逻辑。依据注释：合理分割一个正交（近似）六边形 PL：。邻近注释提示：&&% 综合分割六边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_bbox_edge_segments(pl, tol)
- 说明: 获取对象 pl 的包围盒四条边，分别作为独立的列表返回：
- 邻近注释: 获取多段线的上下左右边界的直线段，返回线段端点列表 | 该函数系列包括如下一些函数 | &&% 获取包围盒边
- 参数: pl, tol
- 返回: top    = [(xmin, ymax, z), (xmax, ymax, z)]
- 关注点: COM, 几何, 日志/测试
- 调用概览: info, print, enumerate, GetBoundingBox, VARIANT, tuple
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取对象 pl 的包围盒四条边，分别作为独立的列表返回：。邻近注释提示：获取多段线的上下左右边界的直线段，返回线段端点列表；该函数系列包括如下一些函数；&&% 获取包围盒边。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_texts_in_polyline(com_pl, tol)
- 说明: 在多段线 com_pl 内部筛选文字，并返回文字对象列表和对应的文字内容列表。
- 邻近注释: &&%  获取多段线的内部的文字 | 该函数系列包括如下一些函数 | &&% 获取多段线内文字
- 参数: com_pl, tol
- 返回: inside:   落在 com_pl 内部的文字 COM 对象列表
- 关注点: 几何, 日志/测试
- 调用概览: get_unique_vertices_from_pl_com, collect_all_texts, info, GetBoundingBox, point_in_polygon, append, getattr, len, TDbMText_content
- 理解: 主要用于获取/选择相关逻辑。依据注释：在多段线 com_pl 内部筛选文字，并返回文字对象列表和对应的文字内容列表。。邻近注释提示：&&%  获取多段线的内部的文字；该函数系列包括如下一些函数；&&% 获取多段线内文字。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### TDbMText_content(comobj, separator)
- 说明: 【函数】获取天正多行文字内容（副本炸开版，支持换行识别）
- 邻近注释: 获取单独一行的天正多行文字内容 | &&% 获取天正多行文字
- 参数: comobj, separator
- 返回推断: object,str,tuple
- 关注点: 几何, 文件, 日志/测试
- 调用概览: li, explode_single_object_marker, sort, enumerate, Copy, get_attr, round, get_sort_info, info, GetBoundingBox, Delete
- 理解: 主要用于处理相关逻辑。依据注释：【函数】获取天正多行文字内容（副本炸开版，支持换行识别）。邻近注释提示：获取单独一行的天正多行文字内容；&&% 获取天正多行文字。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### distribute_points_on_entity(entity, n, block, scale_factor, ys)
- 说明: （无）
- 邻近注释: &&% 实体均分点
- 参数: entity, n, block, scale_factor, ys
- 返回推断: object
- 关注点: COM, 几何
- 调用概览: sqrt, range, InsertBlock, vtpnt, sum, cos, sin, distance, len
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 实体均分点。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### is_segment_contained(seg_a, seg_b, tol)
- 说明: 判断 seg_a 是否完全位于 seg_b 上（包含端点）。
- 邻近注释: 该函数系列包括如下一些函数 | 1 判断一条直线是否完全在另一条直线上 | &&% 判断线段包含
- 参数: seg_a, seg_b, tol
- 返回推断: bool,object,tuple
- 关注点: 几何
- 调用概览: get_endpoints, dot, proj_param, hasattr, hypot, abs, colinear, tuple
- 理解: 主要用于处理相关逻辑。依据注释：判断 seg_a 是否完全位于 seg_b 上（包含端点）。。邻近注释提示：该函数系列包括如下一些函数；1 判断一条直线是否完全在另一条直线上；&&% 判断线段包含。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### common_segments_between_polylines(pl1, pl2, tol)
- 说明: 返回 pl1 中与 pl2 “共线且有重叠”的区段列表，每个区段用
- 邻近注释: &&% 2 返回 PL线pl1 中与 pl2 “共线且有重叠”的区段列表 | &&% 公共线段
- 参数: pl1, pl2, tol
- 返回推断: NoneType,object,tuple
- 关注点: 几何, 日志/测试
- 调用概览: coords_to_xy_pairs, build_segments, print, enumerate, range, hypot, interp, getattr, append, len, info, abs...
- 理解: 主要用于处理相关逻辑。依据注释：返回 pl1 中与 pl2 “共线且有重叠”的区段列表，每个区段用。邻近注释提示：&&% 2 返回 PL线pl1 中与 pl2 “共线且有重叠”的区段列表；&&% 公共线段。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### is_rect_inside_rect(rect_outer, rect_inner, tol)
- 说明: 判定 axis‑aligned 的矩形 rect_inner 是否被（含边界）完全包在 rect_outer 内。
- 邻近注释: 1 判断矩形是否包含另一个矩形 | &&% 矩形包含判断
- 参数: rect_outer, rect_inner, tol
- 返回推断: object
- 理解: 主要用于处理相关逻辑。依据注释：判定 axis‑aligned 的矩形 rect_inner 是否被（含边界）完全包在 rect_outer 内。。邻近注释提示：1 判断矩形是否包含另一个矩形；&&% 矩形包含判断。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### two_plines_making_rectangle(pl1, pl2, tol)
- 说明: 判断两条正交多段线拼在一起后是否正好是一个矩形。
- 邻近注释: 2 判断两条正交多段线拼在一起后是否正好是一个矩形 | &&% 两多段线组矩形
- 参数: pl1, pl2, tol
- 返回推断: bool,object
- 关注点: 几何
- 调用概览: pline_vertices, poly_area, range, hypot, sort, min, max, abs, collect_segments, covers_edge, len, append...
- 理解: 主要用于计算/测量相关逻辑。依据注释：判断两条正交多段线拼在一起后是否正好是一个矩形。。邻近注释提示：2 判断两条正交多段线拼在一起后是否正好是一个矩形；&&% 两多段线组矩形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### are_all_vertices_inside(pl1, pl2)
- 说明: 判断多段线 pl2 的所有顶点是否都在多段线 pl1 构成的多边形内部。
- 邻近注释: 判断多段线PL2是否在多段线PL1多边形中 | 该函数系列包括如下一些函数 | &&% 顶点全在内部
- 参数: pl1, pl2
- 返回: (all_inside, outside_pts)
- 关注点: 几何, 日志/测试
- 调用概览: get_unique_vertices_from_pl_com, len, print, info, point_in_polygon, append
- 理解: 主要用于处理相关逻辑。依据注释：判断多段线 pl2 的所有顶点是否都在多段线 pl1 构成的多边形内部。。邻近注释提示：判断多段线PL2是否在多段线PL1多边形中；该函数系列包括如下一些函数；&&% 顶点全在内部。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## library/cad_objects.py
- 模块说明: 第四部分 一般对象
### ensure_list(input_data)
- 说明: 【通用工具】将输入参数统一转换为列表。
- 邻近注释: &&&&%% 第四部分 一般对象
- 参数: input_data
- 返回推断: bool,list,object
- 关注点: 选择集
- 调用概览: is_list_like, isinstance, hasattr, list, len, ensure_list
- 理解: 主要用于获取/选择相关逻辑。依据注释：【通用工具】将输入参数统一转换为列表。。邻近注释提示：&&&&%% 第四部分 一般对象。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### sort_tuples(lst, cha_Y)
- 说明: 这是很有用的一个双值排序函数，对于COM对象，可以先将其转换为元组，即可使用这个函数
- 邻近注释: 按com实体对象中提取的坐标排序 | &&&%  排序 | &&% 元组排序
- 参数: lst, cha_Y
- 返回推断: object
- 调用概览: sort, len, sorted, abs
- 理解: 主要用于处理相关逻辑。依据注释：这是很有用的一个双值排序函数，对于COM对象，可以先将其转换为元组，即可使用这个函数。邻近注释提示：按com实体对象中提取的坐标排序；&&&%  排序；&&% 元组排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### multi_dim_tolerance_sort(lst, key_index, tolerances)
- 说明: 对 lst 列表中的元组按多维坐标字段排序，考虑每个维度的容差进行逐层排序。
- 邻近注释: &&% 多维容差排序
- 参数: lst, key_index, tolerances
- 返回: 排好序的新列表
- 调用概览: len, sort, recursive_sort, sorted, abs
- 理解: 主要用于处理相关逻辑。依据注释：对 lst 列表中的元组按多维坐标字段排序，考虑每个维度的容差进行逐层排序。。邻近注释提示：&&% 多维容差排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_ll_pt(ent)
- 说明: （无）
- 参数: ent
- 返回推断: tuple
- 调用概览: GetBoundingBox
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_center(ent)
- 说明: （无）
- 参数: ent
- 返回推断: tuple
- 调用概览: GetBoundingBox
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_entities_by_position(entity_list, extract_func, cha_Y)
- 说明: 对实体列表根据其坐标（通过 extract_func 获取）进行排序：
- 邻近注释: &&% 实体位置排序
- 参数: entity_list, extract_func, cha_Y
- 返回: 按坐标顺序排列的新实体对象列表
- 调用概览: sort, sorted, len, extract_func, abs
- 理解: 主要用于处理相关逻辑。依据注释：对实体列表根据其坐标（通过 extract_func 获取）进行排序：。邻近注释提示：&&% 实体位置排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_line_start(ent)
- 说明: 提取一条直线的起点 (x, y)
- 参数: ent
- 返回推断: tuple
- 关注点: 几何
- 理解: 主要用于获取/选择相关逻辑。依据注释：提取一条直线的起点 (x, y)。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_llcorner(com_list, cha_Y)
- 说明: 按 BoundingBox 左下角坐标排序：
- 邻近注释: &&% * 对列表实体进行从上到下、从左到右的排序 | &&% 左下角排序
- 参数: com_list, cha_Y
- 返回推断: object
- 调用概览: sort, append, GetBoundingBox, len, sorted, float, abs
- 理解: 主要用于处理相关逻辑。依据注释：按 BoundingBox 左下角坐标排序：。邻近注释提示：&&% * 对列表实体进行从上到下、从左到右的排序；&&% 左下角排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_rbcorner(com_list)
- 说明: 竖向图框（或已整体旋转 -90° 的图纸）使用 ——  
- 邻近注释: &&% 右上角排序
- 参数: com_list
- 返回推断: object
- 调用概览: sort, append, sorted, GetBoundingBox, len, float, abs
- 理解: 主要用于处理相关逻辑。依据注释：竖向图框（或已整体旋转 -90° 的图纸）使用 ——  。邻近注释提示：&&% 右上角排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_llcorner_custom(objs, tol_x)
- 说明: 按左下角 x, y 坐标对 COM 对象列表 objs 排序：
- 邻近注释: &&% 自定义左下角排序
- 参数: objs, tol_x
- 返回推断: object
- 调用概览: sort, append, sorted, GetBoundingBox, extend, abs
- 理解: 主要用于处理相关逻辑。依据注释：按左下角 x, y 坐标对 COM 对象列表 objs 排序：。邻近注释提示：&&% 自定义左下角排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_center(objs, tol_x)
- 说明: 按外包盒中心坐标对 COM 对象列表 objs 排序：
- 邻近注释: &&% 中心点排序
- 参数: objs, tol_x
- 返回推断: list,object
- 关注点: 几何
- 调用概览: sort, append, sorted, GetBoundingBox, extend, abs
- 理解: 主要用于处理相关逻辑。依据注释：按外包盒中心坐标对 COM 对象列表 objs 排序：。邻近注释提示：&&% 中心点排序。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### number_entities_by_order(entity_list, prefix, start, k)
- 说明: 对排序好的 COM 实体对象列表进行编号。
- 邻近注释: 对列表实体进行正序或逆序编号 | &&% 实体编号
- 参数: entity_list, prefix, start, k
- 返回: 编号字符串列表（如 ["1", "2", "3"] 或 ["图1", "图2", "图3"]）
- 调用概览: len, enumerate, range, reversed, append
- 理解: 主要用于处理相关逻辑。依据注释：对排序好的 COM 实体对象列表进行编号。。邻近注释提示：对列表实体进行正序或逆序编号；&&% 实体编号。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### pr_list(P, f, *args, **kwargs)
- 说明: args:  位置参数元组 (例如: 10, 20)
- 邻近注释: 重复操作列表对象 | &&&% 列表处理 | &&% 列表遍历操作
- 参数: P, f, *args, **kwargs
- 返回推断: object
- 关注点: 日志/测试
- 调用概览: info, enumerate, f, append, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：args:  位置参数元组 (例如: 10, 20)。邻近注释提示：重复操作列表对象；&&&% 列表处理；&&% 列表遍历操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### apply_to_each2(obj_list, extract_func, action_func)
- 说明: 对 obj_list 中的每个对象，先通过 extract_func 提取值，
- 邻近注释: &&% 列表提取操作
- 参数: obj_list, extract_func, action_func
- 调用概览: extract_func, action_func
- 理解: 主要用于处理相关逻辑。依据注释：对 obj_list 中的每个对象，先通过 extract_func 提取值，。邻近注释提示：&&% 列表提取操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_boundingbox_from_objects(objs)
- 说明: 从一组图形对象（如 LB）中获取整体包围盒
- 邻近注释: 建立全部列表com对象的最小边界框 | &&&% 边界框 | &&% 获取对象群包围盒
- 参数: objs
- 返回推断: tuple
- 关注点: 几何, 日志/测试
- 调用概览: tuple, GetBoundingBox, info, list, min, max, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：从一组图形对象（如 LB）中获取整体包围盒。邻近注释提示：建立全部列表com对象的最小边界框；&&&% 边界框；&&% 获取对象群包围盒。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### chuangjian_zu(group_name)
- 说明: （无）
- 邻近注释: 建立组的最小边界框 | &&% 创建组
- 参数: group_name
- 返回推断: object
- 调用概览: Add
- 理解: 主要用于处理相关逻辑。邻近注释提示：建立组的最小边界框；&&% 创建组。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### nametogroup(group_name)
- 说明: （无）
- 邻近注释: &&% 获取组对象
- 参数: group_name
- 返回推断: object
- 调用概览: Item
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 获取组对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_all_group_names()
- 说明: 获取当前 DWG 文档中所有组的名称列表。
- 邻近注释: 获取所有组 | &&% 获取所有组名
- 参数: （无）
- 返回: List[str] — 包含所有组名称的列表
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, Item, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取当前 DWG 文档中所有组的名称列表。。邻近注释提示：获取所有组；&&% 获取所有组名。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_all_groups()
- 说明: 获取当前 DWG 文档中所有组的 COM 对象列表及其名称。
- 邻近注释: &&% 获取所有组
- 参数: （无）
- 返回: List[Tuple[str, COMObject]] — 每项为 (组名称, 组对象)
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, range, Item, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取当前 DWG 文档中所有组的 COM 对象列表及其名称。。邻近注释提示：&&% 获取所有组。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### add_objects_to_group(group_name, obj_list)
- 说明: 将 obj_list 中的所有图形对象加入名为 group_name 的组中
- 邻近注释: 将多个com对象对象加入名为group_name的组 | &&% 添加对象到组
- 参数: group_name, obj_list
- 返回: Group 对象
- 调用概览: AppendItems, Item, vtlist, Add
- 理解: 主要用于创建/插入相关逻辑。依据注释：将 obj_list 中的所有图形对象加入名为 group_name 的组中。邻近注释提示：将多个com对象对象加入名为group_name的组；&&% 添加对象到组。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### add_object_to_group(group_name, obj)
- 说明: 将单个图形对象 obj 加入名为 group_name 的组中。
- 邻近注释: 将单独com对象对象加入名为group_name的组中 | &&% 添加单对象到组
- 参数: group_name, obj
- 返回: COM Group 对象
- 调用概览: AppendItems, Item, vtlist, Add
- 理解: 主要用于创建/插入相关逻辑。依据注释：将单个图形对象 obj 加入名为 group_name 的组中。。邻近注释提示：将单独com对象对象加入名为group_name的组中；&&% 添加单对象到组。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### remove_object_from_group(group_name, obj)
- 说明: 将单个 COM 对象 obj 从名为 group_name 的组中移出。
- 邻近注释: 将单独com对象对象移出名为group_name的组 | &&% 移除组内对象
- 参数: group_name, obj
- 返回: 如果组存在，返回该 Group 对象；否则返回 None。
- 关注点: COM, 文件, 日志/测试
- 调用概览: VARIANT, Item, RemoveItems, info
- 理解: 主要用于删除/清理相关逻辑。依据注释：将单个 COM 对象 obj 从名为 group_name 的组中移出。。邻近注释提示：将单独com对象对象移出名为group_name的组；&&% 移除组内对象。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### remove_objects_from_group(group_name, obj_list)
- 说明: 将 obj_list 中的所有图形对象从名为 group_name 的组中移出。
- 邻近注释: 将多个com对象对象移出名为group_name的组 | &&% 批量移除组内对象
- 参数: group_name, obj_list
- 返回推断: NoneType,object
- 关注点: COM, 文件, 日志/测试
- 调用概览: VARIANT, Item, RemoveItems, info, len
- 理解: 主要用于删除/清理相关逻辑。依据注释：将 obj_list 中的所有图形对象从名为 group_name 的组中移出。。邻近注释提示：将多个com对象对象移出名为group_name的组；&&% 批量移除组内对象。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### get_com_from_groupname(group_name)
- 说明: 根据组名获取对应实体列表。
- 邻近注释: &&% 从名为group_name的组获取内部包含的实体对象 | &&% 获取组内实体
- 参数: group_name
- 返回推断: list,object
- 调用概览: nametogroup, Item, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：根据组名获取对应实体列表。。邻近注释提示：&&% 从名为group_name的组获取内部包含的实体对象；&&% 获取组内实体。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_com_from_groupname_by_type(group_name)
- 说明: 根据组名获取对应实体，并按类型名分类返回。
- 邻近注释: 从名为group_name的组返回按类型分类的字典 | &&% 获取组内实体分类
- 参数: group_name
- 返回推断: dict,object
- 关注点: 日志/测试
- 调用概览: nametogroup, range, items, info, Item, append, getattr, setdefault, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：根据组名获取对应实体，并按类型名分类返回。。邻近注释提示：从名为group_name的组返回按类型分类的字典；&&% 获取组内实体分类。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_group_entities_sorted(group_name, type_extractors, cha_Y)
- 说明: 从组中按类型获取实体，并对指定类型按坐标排序。
- 邻近注释: 从名为group_name的组返回按类型分类的字典，且类型按各自位置提取函数排好序 | &&% 获取组内实体排序
- 参数: group_name, type_extractors, cha_Y
- 返回推断: object,tuple
- 关注点: 几何, 日志/测试
- 调用概览: get_com_from_groupname_by_type, items, float, sort_entities_by_position, info, list, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：从组中按类型获取实体，并对指定类型按坐标排序。。邻近注释提示：从名为group_name的组返回按类型分类的字典，且类型按各自位置提取函数排好序；&&% 获取组内实体排序。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_group_entities_sorted_by_type_and_bbox(group_name, cha_Y)
- 说明: 将组 group_name 中的实体按类型分类，并对每种类型内部按包围盒中心排序：
- 邻近注释: 从名为group_name的组返回按类型分类的字典，各类型统一按boundingbox中心排好序 | &&% 组内实体按中心排序
- 参数: group_name, cha_Y
- 返回: 一个 dict，key=类型名(ObjectName)，value=排序后的实体列表
- 关注点: 几何
- 调用概览: nametogroup, items, Item, append, sort, range, getattr, sorted, setdefault, len, bbox_center_2, abs
- 理解: 主要用于获取/选择相关逻辑。依据注释：将组 group_name 中的实体按类型分类，并对每种类型内部按包围盒中心排序：。邻近注释提示：从名为group_name的组返回按类型分类的字典，各类型统一按boundingbox中心排好序；&&% 组内实体按中心排序。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### common_group_entities_sorted(group_name1, group_name2, cha_Y)
- 说明: 获取两个组中共有的实体，按类型分类并按包围盒中心排序。
- 邻近注释: 获取两个组中共有的实体，按类型分类并按包围盒中心排序 | &&% 共有组实体排序
- 参数: group_name1, group_name2, cha_Y
- 返回: dict => key: ObjectName 类型名, value: 排序后的实体列表
- 关注点: COM, 几何
- 调用概览: nametogroup, items, Item, set, append, GetBoundingBox, tuple, sort, range, keys, getattr, sorted...
- 理解: 主要用于处理相关逻辑。依据注释：获取两个组中共有的实体，按类型分类并按包围盒中心排序。。邻近注释提示：获取两个组中共有的实体，按类型分类并按包围盒中心排序；&&% 共有组实体排序。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_boundingbox_from_group(group)
- 说明: 并非组的实际BoundingBOX数据
- 邻近注释: &&% 获取组包围盒
- 参数: group
- 返回推断: tuple
- 关注点: 几何
- 调用概览: get_boundingbox_from_objects, Item, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：并非组的实际BoundingBOX数据。邻近注释提示：&&% 获取组包围盒。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### copy_group_S1_from_doc1_to_doc2(doc1, doc2, group_name)
- 说明: 将 doc1 中名为 group_name 的组复制到 doc2 中，并重新组装组。
- 邻近注释: &&% 复制组S1
- 参数: doc1, doc2, group_name
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 调用概览: set_active_doc, li, Item, yin_to_xian_xuanze, SendCommand, sleep, get_handle_object_map, info, add_objects_to_group, set, chr, len
- 理解: 主要用于移动/复制相关逻辑。依据注释：将 doc1 中名为 group_name 的组复制到 doc2 中，并重新组装组。。邻近注释提示：&&% 复制组S1。实现特征：通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### HandleToObject(ZF)
- 说明: 对连接在墙上的门窗测试无效
- 邻近注释: &&% 句柄转对象
- 参数: ZF
- 返回推断: object
- 关注点: COM
- 调用概览: alias, HandleToObject
- 理解: 主要用于处理相关逻辑。依据注释：对连接在墙上的门窗测试无效。邻近注释提示：&&% 句柄转对象。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### print_coms_handle(LB)
- 说明: （无）
- 参数: LB
- 关注点: COM, 日志/测试
- 调用概览: info, append
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### handles_to_coms(LB_handles)
- 说明: 对连接在墙上的门窗测试无效
- 邻近注释: &&% 批量句柄转对象
- 参数: LB_handles
- 返回推断: object
- 关注点: COM
- 调用概览: alias, HandleToObject, append
- 理解: 主要用于处理相关逻辑。依据注释：对连接在墙上的门窗测试无效。邻近注释提示：&&% 批量句柄转对象。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_all_handles()
- 说明: 获取当前图纸中所有对象（通常在 ModelSpace）的 Handle 值列表。
- 邻近注释: &&% 获取所有句柄
- 参数: （无）
- 返回: handle_list: 所有图元的 Handle 字符串列表
- 关注点: COM, 日志/测试
- 调用概览: info, append, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取当前图纸中所有对象（通常在 ModelSpace）的 Handle 值列表。。邻近注释提示：&&% 获取所有句柄。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_entity_by_handle(handle_str)
- 说明: 遍历当前图纸所有对象，手动比对 Handle 值，找到指定的实体对象。
- 邻近注释: &&% 查找实体
- 参数: handle_str
- 返回: 对象（若找到），否则 None
- 关注点: COM
- 理解: 主要用于获取/选择相关逻辑。依据注释：遍历当前图纸所有对象，手动比对 Handle 值，找到指定的实体对象。。邻近注释提示：&&% 查找实体。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### group_objects_by_type_and_handle(LB)
- 说明: 将com对象列表 LB 中的对象按 ObjectName 分类，并存储其 Handle。
- 邻近注释: &&% 按类型句柄分组
- 参数: LB
- 返回: ZD - dict 格式 {ObjectName: [Handle1, Handle2, ...]}
- 关注点: COM, 日志/测试, 选择集
- 调用概览: items, info, append, len
- 理解: 主要用于处理相关逻辑。依据注释：将com对象列表 LB 中的对象按 ObjectName 分类，并存储其 Handle。。邻近注释提示：&&% 按类型句柄分组。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### record_handle_with_type(LB, typename, prefix)
- 说明: 替代 XData 方法：记录对象 Handle、类型名、编号，返回结构化字典。
- 邻近注释: 通过名称存储对象信息反回溯对象 | &&% 记录类型句柄
- 参数: LB, typename, prefix
- 返回推断: object
- 关注点: COM, 日志/测试
- 调用概览: enumerate, info, len
- 理解: 主要用于保存/写入相关逻辑。依据注释：替代 XData 方法：记录对象 Handle、类型名、编号，返回结构化字典。。邻近注释提示：通过名称存储对象信息反回溯对象；&&% 记录类型句柄。实现特征：涉及扩展数据 XData 读写。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### convert_named_dict(ZD, typename)
- 说明: 将 ZD["门"] 的结构由 Handle: 编号 转换为 编号: COM对象
- 邻近注释: &&% 转换命名字典
- 参数: ZD, typename
- 返回: 新的字典 {编号: COM实体}
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, get, items, HandleToObject, info
- 理解: 主要用于转换/解析相关逻辑。依据注释：将 ZD["门"] 的结构由 Handle: 编号 转换为 编号: COM对象。邻近注释提示：&&% 转换命名字典。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_named_object(tag, ZD, typename)
- 说明: （无）
- 邻近注释: &&% 获取命名对象
- 参数: tag, ZD, typename
- 返回推断: object
- 调用概览: convert_named_dict, get
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 获取命名对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_tags_on_objects_fixed(named_dict, height, offset)
- 说明: 在每个对象的中心点附近绘制标注文字。
- 邻近注释: &&% 绘制固定标签
- 参数: named_dict, height, offset
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, items, GetBoundingBox, VARIANT, AddText, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：在每个对象的中心点附近绘制标注文字。。邻近注释提示：&&% 绘制固定标签。实现特征：创建文字对象。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### label_tarch_doors(LB1, typename, prefix)
- 说明: 从对象列表 LB1 中筛选出天正门 (ObjectName == 'TDbOpening')，
- 邻近注释: 给天正对象打上标签存入字典，用于以名称反向回溯操作 | &&% 标记天正门
- 参数: LB1, typename, prefix
- 返回: ZD = {typename: {编号: 对象}}
- 关注点: 日志/测试
- 调用概览: enumerate, info, hasattr, append, len
- 理解: 主要用于处理相关逻辑。依据注释：从对象列表 LB1 中筛选出天正门 (ObjectName == 'TDbOpening')，。邻近注释提示：给天正对象打上标签存入字典，用于以名称反向回溯操作；&&% 标记天正门。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_handle_object_map(ms)
- 说明: 返回 {handle: object} 映射
- 邻近注释: &&% 获取句柄映射
- 参数: ms
- 返回推断: object
- 关注点: COM
- 理解: 主要用于获取/选择相关逻辑。依据注释：返回 {handle: object} 映射。邻近注释提示：&&% 获取句柄映射。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_xdata(com_obj, app_name, data_types, data_values)
- 说明: 向任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）附加 XData。
- 邻近注释: &&% 设置扩展数据
- 参数: com_obj, app_name, data_types, data_values
- 返回推断: object
- 关注点: COM
- 调用概览: vtint, vtvariant, SetXData, VARIANT
- 理解: 主要用于更新/设置相关逻辑。依据注释：向任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）附加 XData。。邻近注释提示：&&% 设置扩展数据。实现特征：涉及扩展数据 XData 读写。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_xdata(com_obj, app_name)
- 说明: 从任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）读取 XData。
- 邻近注释: &&% 获取扩展数据
- 参数: com_obj, app_name
- 返回: (type_codes, data_values) 二元组，其中
- 关注点: COM
- 调用概览: VARIANT, GetXData, list
- 理解: 主要用于获取/选择相关逻辑。依据注释：从任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）读取 XData。。邻近注释提示：&&% 获取扩展数据。实现特征：涉及扩展数据 XData 读写。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_xdata_tab(entitycom)
- 说明: （无）
- 邻近注释: &&% Xdata标记 | &&% 设置打印标记
- 参数: entitycom
- 返回推断: None
- 调用概览: set_xdata
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：&&% Xdata标记；&&% 设置打印标记。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### is_printApp_xdata_com(entitycom)
- 说明: （无）
- 邻近注释: &&% 检查打印标记
- 参数: entitycom
- 返回推断: bool
- 调用概览: get_xdata
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 检查打印标记。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### write_cad_text(p, text, alignment, height, width_factor, rotation, oblique, style, layer)
- 说明: 【架构适配版】在指定位置写入 CAD 单行文字。
- 邻近注释: &&&% 文字 | &&% 写CAD单行文字
- 参数: p, text, alignment, height, width_factor, rotation, oblique, style, layer
- 返回推断: None,NoneType,object
- 关注点: COM, 几何, 文件, 日志/测试, 进程
- 关键调用: C.li
- 调用概览: li, print, VARIANT, float, AddText, setattr, Update, GetBoundingBox, lower, Move, len, append...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【架构适配版】在指定位置写入 CAD 单行文字。。邻近注释提示：&&&% 文字；&&% 写CAD单行文字。实现特征：创建文字对象。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### write_tianzheng_text(p, text, alignment, height, width_factor, rotation, oblique, style, system_layer, system_file_name, delete_system_text)
- 说明: 在当前激活图中写入一段“天正单行文字”（通过系统模板 Copy 实现），
- 邻近注释: &&% 写天正单行文字
- 参数: p, text, alignment, height, width_factor, rotation, oblique, style, system_layer, system_file_name, delete_system_text
- 返回推断: None,NoneType,object
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待
- 关键调用: C.doc, C.acad
- 调用概览: info, lower, VARIANT, Move, stc, getattr, _align_entity_by_bbox, GetBoundingBox, len, float, Copy, set_object_property...
- 理解: 主要用于保存/写入相关逻辑。依据注释：在当前激活图中写入一段“天正单行文字”（通过系统模板 Copy 实现），。邻近注释提示：&&% 写天正单行文字。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### align_text_to_vertical_line(text_obj, x_position, align_side)
- 说明: 将文字按 BoundingBox 边界对齐到指定垂直线的 X 坐标。
- 邻近注释: ====================  文字垂直对齐 ==================== | &&% 文字垂直对齐
- 参数: text_obj, x_position, align_side
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 关键调用: C.li
- 调用概览: li, isinstance, info, enumerate, print, list, float, GetBoundingBox, VARIANT, Move, len
- 理解: 主要用于处理相关逻辑。依据注释：将文字按 BoundingBox 边界对齐到指定垂直线的 X 坐标。。邻近注释提示：====================  文字垂直对齐 ====================；&&% 文字垂直对齐。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### align_text_to_horizontal_line(text_obj, y_position, align_side)
- 说明: 将文字按 BoundingBox 边界对齐到指定水平线的 Y 坐标。
- 邻近注释: ====================  文字水平对齐 ==================== | &&% 文字水平对齐
- 参数: text_obj, y_position, align_side
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 关键调用: C.li
- 调用概览: li, isinstance, info, enumerate, print, list, float, GetBoundingBox, VARIANT, Move, len
- 理解: 主要用于处理相关逻辑。依据注释：将文字按 BoundingBox 边界对齐到指定水平线的 Y 坐标。。邻近注释提示：====================  文字水平对齐 ====================；&&% 文字水平对齐。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### scale_tianzheng_text_to_cad(tianzheng_text_obj, cad_text_obj)
- 说明: 使用 ScaleEntity 将天正文字的 BoundingBox 高度缩放到 CAD 文字的高度。
- 邻近注释: ====================  缩放天正文字高度 ==================== | &&% 缩放天正文字
- 参数: tianzheng_text_obj, cad_text_obj
- 返回推断: bool
- 关注点: COM, 日志/测试
- 关键调用: C.li
- 调用概览: li, isinstance, info, enumerate, print, list, GetBoundingBox, float, VARIANT, ScaleEntity, len
- 理解: 主要用于处理相关逻辑。依据注释：使用 ScaleEntity 将天正文字的 BoundingBox 高度缩放到 CAD 文字的高度。。邻近注释提示：====================  缩放天正文字高度 ====================；&&% 缩放天正文字。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### sc_objs_to_layer(layer_name, cl)
- 说明: （无）
- 参数: layer_name, cl
- 返回推断: list,object
- 关注点: 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: alias, pmxz_new, Item, Add, SelectOnScreen, Delete, info, print, range
- 理解: 主要用于处理相关逻辑。实现特征：涉及图层操作；涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### delete_layer(layername)
- 说明: 删除当前 DWG 文件中名为 layername 的图层。
- 邻近注释: &&% 删除图层
- 参数: layername
- 返回推断: None
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, Item, Delete, info
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除当前 DWG 文件中名为 layername 的图层。。邻近注释提示：&&% 删除图层。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### create_layers_from_list(layer_names)
- 说明: 创建列表中指定的图层，如果图层已存在则跳过。
- 邻近注释: &&% 从列表创建图层
- 参数: layer_names
- 关注点: 日志/测试
- 调用概览: get_acad_doc, info, print, Item, Add
- 理解: 主要用于创建/插入相关逻辑。依据注释：创建列表中指定的图层，如果图层已存在则跳过。。邻近注释提示：&&% 从列表创建图层。实现特征：涉及图层操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### delete_layers_from_list(layer_names)
- 说明: 删除列表中指定的图层
- 邻近注释: &&% 从列表删除图层
- 参数: layer_names
- 返回: dict: {'deleted': 删除成功的图层列表, 'failed': 删除失败的图层列表}
- 关注点: 日志/测试
- 调用概览: get_acad_doc, info, Item, Delete, append, len
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除列表中指定的图层。邻近注释提示：&&% 从列表删除图层。实现特征：涉及图层操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### dim_by_points(*args)
- 说明: 使用天正逐点标注命令对倾斜对象进行标注
- 邻近注释: &&% 逐点标注
- 参数: *args
- 返回: bool: 成功返回True
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: hotkey, sleep, activate_window_by_title, get_acad_doc, SendCommand, print, len, info
- 理解: 主要用于处理相关逻辑。依据注释：使用天正逐点标注命令对倾斜对象进行标注。邻近注释提示：&&% 逐点标注。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### ensure_layer(layer_name)
- 说明: 确保图层存在并设为当前图层，同时删除该图层上所有对象（最多重试 3 次）。
- 邻近注释: &&% 确保图层存在并清空
- 参数: layer_name
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 调用概览: li, info, range, Item, select_tuceng, sleep, SendCommand, len, print, Add, Delete
- 理解: 主要用于处理相关逻辑。依据注释：确保图层存在并设为当前图层，同时删除该图层上所有对象（最多重试 3 次）。。邻近注释提示：&&% 确保图层存在并清空。实现特征：涉及图层操作；通过命令发送驱动 CAD 行为。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### ensure_layer_model_only(layer_name)
- 说明: 确保图层存在并设为当前图层，同时【仅删除】该图层在模型空间（Model Space）中的对象。
- 邻近注释: &&% 只在模型空间上清理
- 参数: layer_name
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: info, range, Item, select_tuceng, sleep, SendCommand, sum, print, Add, get_obj_loc, Delete
- 理解: 主要用于处理相关逻辑。依据注释：确保图层存在并设为当前图层，同时【仅删除】该图层在模型空间（Model Space）中的对象。。邻近注释提示：&&% 只在模型空间上清理。实现特征：涉及图层操作；通过命令发送驱动 CAD 行为。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### ensure_layer_current(layer_name, max_retries)
- 说明: 确保图层存在并设为当前图层，失败时最多重试 max_retries 次。
- 参数: layer_name, max_retries
- 返回推断: bool
- 关注点: 日志/测试
- 调用概览: alias, range, info, Item, Add
- 理解: 主要用于处理相关逻辑。依据注释：确保图层存在并设为当前图层，失败时最多重试 max_retries 次。。实现特征：涉及图层操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_layer_properties(layer_name, color_index, linetype, on, frozen)
- 说明: 设置指定图层的颜色、线型、开关状态和冻结状态。
- 参数: layer_name, color_index, linetype, on, frozen
- 关注点: COM, 日志/测试
- 调用概览: alias, li, SendCommand, info, Item, Add, Load
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置指定图层的颜色、线型、开关状态和冻结状态。。实现特征：涉及图层操作；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_layer_with_retry(LB, layername, ci)
- 说明: 将给定 COM 对象列表 LB 中的每个对象的 Layer 属性设为 layername。
- 邻近注释: &&% 将列表中的对象图层设为目标图层
- 参数: LB, layername, ci
- 返回推断: tuple
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 调用概览: li, get, print, range, globals, list, Item, info, Add, setattr, append, getattr...
- 理解: 主要用于更新/设置相关逻辑。依据注释：将给定 COM 对象列表 LB 中的每个对象的 Layer 属性设为 layername。。邻近注释提示：&&% 将列表中的对象图层设为目标图层。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### force_layer_objects_color(layer_name, target_color, max_retries)
- 说明: [最终修正版] 强制改色
- 邻近注释: &&% 强制改图层对象颜色
- 参数: layer_name, target_color, max_retries
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: info, list, range, stc, print, enumerate, sleep, set_attr, get_attr, len, Update, append
- 理解: 主要用于处理相关逻辑。依据注释：[最终修正版] 强制改色。邻近注释提示：&&% 强制改图层对象颜色。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

## library/execution_result.py
- 模块说明: 函数执行状态规范
### ExecutionResult.__init__(self, status, data, message, details, error)
- 说明: 初始化执行结果
- 参数: self, status, data, message, details, error
- 理解: 主要用于处理相关逻辑。依据注释：初始化执行结果。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ExecutionResult.is_success(self)
- 说明: 判断是否成功
- 参数: self
- 返回推断: object
- 理解: 主要用于处理相关逻辑。依据注释：判断是否成功。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ExecutionResult.is_failed(self)
- 说明: 判断是否失败
- 参数: self
- 返回推断: object
- 理解: 主要用于处理相关逻辑。依据注释：判断是否失败。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ExecutionResult.is_partial(self)
- 说明: 判断是否部分成功
- 参数: self
- 返回推断: object
- 理解: 主要用于处理相关逻辑。依据注释：判断是否部分成功。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ExecutionResult.to_dict(self)
- 说明: 转换为字典
- 参数: self
- 返回推断: dict
- 调用概览: str
- 理解: 主要用于处理相关逻辑。依据注释：转换为字典。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ExecutionResult.__repr__(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ExecutionResult.__bool__(self)
- 说明: 支持布尔判断：if result: ...
- 参数: self
- 返回推断: object
- 调用概览: is_success
- 理解: 主要用于处理相关逻辑。依据注释：支持布尔判断：if result: ...。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### success(data, message, **details)
- 说明: 创建成功结果
- 邻近注释: ========== 便捷构造函数 ==========
- 参数: data, message, **details
- 返回: ExecutionResult: 成功结果
- 调用概览: ExecutionResult
- 理解: 主要用于处理相关逻辑。依据注释：创建成功结果。邻近注释提示：========== 便捷构造函数 ==========。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### failed(message, error, **details)
- 说明: 创建失败结果
- 参数: message, error, **details
- 返回: ExecutionResult: 失败结果
- 调用概览: ExecutionResult
- 理解: 主要用于处理相关逻辑。依据注释：创建失败结果。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### partial(data, message, **details)
- 说明: 创建部分成功结果
- 参数: data, message, **details
- 返回: ExecutionResult: 部分成功结果
- 调用概览: ExecutionResult
- 理解: 主要用于处理相关逻辑。依据注释：创建部分成功结果。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### error(message, exception, **details)
- 说明: 创建错误结果
- 参数: message, exception, **details
- 返回: ExecutionResult: 错误结果
- 调用概览: ExecutionResult
- 理解: 主要用于处理相关逻辑。依据注释：创建错误结果。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### with_execution_check(expected_conditions)
- 说明: 函数执行检查装饰器
- 邻近注释: ========== 函数内置判定标准装饰器 ==========
- 参数: expected_conditions
- 返回推断: object
- 调用概览: func, isinstance, get, append, join
- 理解: 主要用于测试/校验相关逻辑。依据注释：函数执行检查装饰器。邻近注释提示：========== 函数内置判定标准装饰器 ==========。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## library/tarch_building.py
- 模块说明: 天正建筑组件操作模块
### dim_by_points(p1, p2, p3)
- 说明: 使用天正逐点标注命令对任意两点进行标注
- 参数: p1, p2, p3
- 返回: bool: 成功返回True
- 关键调用: C.li
- 调用概览: li, _dim_by_points
- 理解: 主要用于处理相关逻辑。依据注释：使用天正逐点标注命令对任意两点进行标注。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_tarch_wall(p1, p2, thickness)
- 说明: 绘制天正墙体
- 邻近注释: &&% 绘制天正墙
- 参数: p1, p2, thickness
- 返回: bool: 成功返回True
- 关注点: 文件, 时间/等待
- 关键调用: send_cmd_with_sync, wait_quiescent, C.li
- 调用概览: li, append, str, send_cmd_with_sync, wait_quiescent, sleep, range, print, Path, last_obj, set_object_property
- 理解: 主要用于创建/插入相关逻辑。依据注释：绘制天正墙体。邻近注释提示：&&% 绘制天正墙。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### insert_tarch_door(p, width, height)
- 说明: 在墙体上插入天正门
- 邻近注释: &&% 插入天正门
- 参数: p, width, height
- 返回: dict: {'success': bool, 'door': 门对象, 'width': 实际宽度, 'height': 实际高度}
- 关注点: COM, 文件, 时间/等待
- 关键调用: send_cmd_with_sync, wait_quiescent, C.doc
- 调用概览: append, str, send_cmd_with_sync, wait_quiescent, get_object_property, print, time, sleep, range, set_object_property, print_exc, Path...
- 理解: 主要用于创建/插入相关逻辑。依据注释：在墙体上插入天正门。邻近注释提示：&&% 插入天正门。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### insert_tarch_window(p, width, height, window_type, delete_mc_yuan)
- 说明: 在墙体上插入天正窗
- 邻近注释: &&% 插入天正窗
- 参数: p, width, height, window_type, delete_mc_yuan
- 返回: dict: {'success': bool, 'window': 窗对象, 'width': 宽度, 'height': 高度}
- 关注点: COM, 文件, 时间/等待
- 关键调用: C.li
- 调用概览: append, mkdir, getLogger, setLevel, FileHandler, Formatter, setFormatter, addHandler, li, info, print, stc...
- 理解: 主要用于创建/插入相关逻辑。依据注释：在墙体上插入天正窗。邻近注释提示：&&% 插入天正窗。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### run_tupdspace_for_tz_room_in_rect(x1, y1, x2, y2, ty, center_z, insert_coord, require_tz_wall)
- 说明: 在矩形 (x1,y1)-(x2,y2) 范围内：
- 邻近注释: &&% 获取天正房间
- 参数: x1, y1, x2, y2, ty, center_z, insert_coord, require_tz_wall
- 返回: dict 示例：
- 关注点: COM, 选择集
- 关键调用: C.li
- 调用概览: print, li, normalize_rect, run_auto_TUPDSPACE_with_coord, select_entities_in_window, append, tuple, len, get, getattr, ValueError, repr...
- 理解: 主要用于处理相关逻辑。依据注释：在矩形 (x1,y1)-(x2,y2) 范围内：。邻近注释提示：&&% 获取天正房间。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### run_auto_TUPDSPACE_with_coord(coord, script_path)
- 说明: 调用 auto_TUPDSPACE.py 子程序，传入坐标，并等待其执行完成（无黑框弹出）。
- 参数: coord, script_path
- 返回: result: dict，例如
- 关注点: 文件, 进程
- 调用概览: getcwd, print, hasattr, run, ValueError, abspath, print_exc, isinstance, len, repr
- 理解: 主要用于处理相关逻辑。依据注释：调用 auto_TUPDSPACE.py 子程序，传入坐标，并等待其执行完成（无黑框弹出）。。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### TDb_single_line_variable_wall(x1, y1, x2, y2, width)
- 说明: 单线变墙函数：将区域内的线段转换为天正墙体
- 邻近注释: &&% 单线变墙
- 参数: x1, y1, x2, y2, width
- 返回: bool: 成功返回True
- 关注点: 几何, 时间/等待, 选择集
- 关键调用: wait_quiescent, C.li
- 调用概览: li, select_objects_in_window_area, print, wait_quiescent, draw_tarch_wall, sleep, getattr, len, Delete
- 理解: 主要用于处理相关逻辑。依据注释：单线变墙函数：将区域内的线段转换为天正墙体。邻近注释提示：&&% 单线变墙。实现特征：包含空闲等待以同步 CAD 状态。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；超时与重试次数边界

### convert_lines_to_walls(x1, y1, x2, y2)
- 说明: Convert lines to thin walls; return (detected_lines, success_walls, failed_walls).
- 参数: x1, y1, x2, y2
- 返回推断: tuple
- 关注点: 几何, 时间/等待, 选择集
- 关键调用: wait_quiescent, C.li
- 调用概览: range, select_objects_in_window_area, sum, print, set_walls_thickness, len, li, draw_tarch_wall, Delete, getattr, sleep, lower
- 理解: 主要用于转换/解析相关逻辑。依据注释：Convert lines to thin walls; return (detected_lines, success_walls, failed_walls).。实现特征：包含空闲等待以同步 CAD 状态。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；超时与重试次数边界

### set_walls_thickness(x1, y1, x2, y2, width)
- 说明: Adjust all TDbWall objects in window to desired thickness. Return count.
- 参数: x1, y1, x2, y2, width
- 返回推断: object
- 关注点: 选择集
- 关键调用: C.li
- 调用概览: li, select_objects_in_window_area, print, getattr, set_object_property
- 理解: 主要用于更新/设置相关逻辑。依据注释：Adjust all TDbWall objects in window to desired thickness. Return count.。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### activate_cad_middle_click(hwnd)
- 说明: 【纯物理激活】中键点击
- 邻近注释: &&&% 基本函数
- 参数: hwnd
- 返回推断: bool
- 关注点: 文件, 时间/等待, 窗口/输入, 选择集
- 调用概览: IsIconic, GetWindowRect, moveTo, click, sleep, ShowWindow, SetForegroundWindow
- 理解: 主要用于处理相关逻辑。依据注释：【纯物理激活】中键点击。邻近注释提示：&&&% 基本函数。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### insert_tarch_window_lisp_mode(wall_p1, wall_p2, cmd_name)
- 说明: 【函数编号】: TARCH-LISP-V20 (稳健等待版)
- 参数: wall_p1, wall_p2, cmd_name
- 返回推断: bool
- 关注点: 文件, 时间/等待, 窗口/输入, 选择集
- 关键调用: C.acad
- 调用概览: print, activate_cad_middle_click, press, write, range, sleep, FindWindow, IsWindowVisible
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: TARCH-LISP-V20 (稳健等待版)。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### _get_dynamic_cache_path()
- 说明: 【核心配置】动态获取当前用户的缓存文件路径
- 参数: （无）
- 返回推断: object
- 关注点: 文件
- 调用概览: get, join, dirname, abspath
- 理解: 主要用于获取/选择相关逻辑。依据注释：【核心配置】动态获取当前用户的缓存文件路径。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### _load_cache_from_disk()
- 说明: [内部] 从硬盘加载缓存到内存
- 参数: （无）
- 关注点: 文件
- 调用概览: _get_dynamic_cache_path, exists, print, open, load
- 理解: 主要用于打开/读取相关逻辑。依据注释：[内部] 从硬盘加载缓存到内存。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### _save_cache_to_disk()
- 说明: [内部] 将内存缓存保存到硬盘
- 参数: （无）
- 关注点: 文件
- 调用概览: _get_dynamic_cache_path, makedirs, print, dirname, open, dump
- 理解: 主要用于保存/写入相关逻辑。依据注释：[内部] 将内存缓存保存到硬盘。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### _activate_cad_safe(hwnd)
- 说明: 【物理激活】鼠标移至窗口中心点击中键
- 邻近注释: ----------------------------------------------------------------------------- | 辅助函数 | -----------------------------------------------------------------------------
- 参数: hwnd
- 返回推断: bool
- 关注点: 文件, 时间/等待, 窗口/输入, 选择集
- 调用概览: IsIconic, GetWindowRect, moveTo, click, sleep, ShowWindow, SetForegroundWindow
- 理解: 主要用于处理相关逻辑。依据注释：【物理激活】鼠标移至窗口中心点击中键。邻近注释提示：-----------------------------------------------------------------------------；辅助函数；-----------------------------------------------------------------------------。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### _wait_for_user_hover(prompt, dwell_time)
- 说明: 【示教捕获】等待用户悬停鼠标来获取坐标
- 参数: prompt, dwell_time
- 返回推断: object
- 关注点: 时间/等待
- 调用概览: print, position, sqrt, sleep, time
- 理解: 主要用于等待/守护相关逻辑。依据注释：【示教捕获】等待用户悬停鼠标来获取坐标。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### get_wall_thickness(wall_obj)
- 说明: # 【新增】获取墙体厚度
- 邻近注释: ----------------------------------------------------------------------------- | &&&% 墙体查询 | &&% get_wall_thickness
- 参数: wall_obj
- 返回: float: 墙体厚度（Thickness + Thickness2）
- 关注点: 日志/测试
- 调用概览: info, get_object_property, error
- 理解: 主要用于获取/选择相关逻辑。依据注释：# 【新增】获取墙体厚度。邻近注释提示：-----------------------------------------------------------------------------；&&&% 墙体查询；&&% get_wall_thickness。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_wall_length(wall_obj)
- 说明: # 【新增】获取墙体长度
- 邻近注释: &&% get_wall_length
- 参数: wall_obj
- 返回: float: 墙体长度
- 关注点: 日志/测试
- 调用概览: get_object_property, info, error
- 理解: 主要用于获取/选择相关逻辑。依据注释：# 【新增】获取墙体长度。邻近注释提示：&&% get_wall_length。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_wall_height(wall_obj)
- 说明: # 【新增】获取墙体高度
- 邻近注释: &&% get_wall_height
- 参数: wall_obj
- 返回: float: 墙体高度
- 关注点: 日志/测试
- 调用概览: get_object_property, info, error
- 理解: 主要用于获取/选择相关逻辑。依据注释：# 【新增】获取墙体高度。邻近注释提示：&&% get_wall_height。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### modify_wall_thickness(wall_obj, thickness)
- 说明: # 【新增】修改墙体厚度
- 邻近注释: &&&% 墙体修改 | &&% modify_wall_thickness
- 参数: wall_obj, thickness
- 返回: bool: 成功返回True
- 关注点: 日志/测试
- 调用概览: set_object_property, info, error
- 理解: 主要用于更新/设置相关逻辑。依据注释：# 【新增】修改墙体厚度。邻近注释提示：&&&% 墙体修改；&&% modify_wall_thickness。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### modify_wall_height(wall_obj, height)
- 说明: # 【新增】修改墙体高度
- 邻近注释: &&% modify_wall_height
- 参数: wall_obj, height
- 返回: bool: 成功返回True
- 关注点: 日志/测试
- 调用概览: set_object_property, info, error
- 理解: 主要用于更新/设置相关逻辑。依据注释：# 【新增】修改墙体高度。邻近注释提示：&&% modify_wall_height。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### modify_door_size(door_obj, width, height)
- 说明: # 【新增】修改门尺寸
- 邻近注释: &&&% 门窗修改 | &&% modify_door_size
- 参数: door_obj, width, height
- 返回: bool: 成功返回True
- 关注点: 日志/测试
- 调用概览: set_object_property, info, error
- 理解: 主要用于更新/设置相关逻辑。依据注释：# 【新增】修改门尺寸。邻近注释提示：&&&% 门窗修改；&&% modify_door_size。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### modify_window_size(window_obj, width, height)
- 说明: # 【新增】修改窗尺寸
- 邻近注释: &&% modify_window_size
- 参数: window_obj, width, height
- 返回: bool: 成功返回True
- 关注点: 日志/测试
- 调用概览: set_object_property, info, error
- 理解: 主要用于更新/设置相关逻辑。依据注释：# 【新增】修改窗尺寸。邻近注释提示：&&% modify_window_size。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### delete_door(door_obj)
- 说明: # 【新增】删除门
- 邻近注释: &&% delete_door
- 参数: door_obj
- 返回: bool: 成功返回True
- 关注点: 日志/测试
- 调用概览: Delete, info, error
- 理解: 主要用于删除/清理相关逻辑。依据注释：# 【新增】删除门。邻近注释提示：&&% delete_door。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### delete_window(window_obj)
- 说明: # 【新增】删除窗
- 邻近注释: &&% delete_window
- 参数: window_obj
- 返回: bool: 成功返回True
- 关注点: 日志/测试
- 调用概览: Delete, info, error
- 理解: 主要用于删除/清理相关逻辑。依据注释：# 【新增】删除窗。邻近注释提示：&&% delete_window。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### insert_tarch_column(p, width, height, column_type)
- 说明: # 【新增】插入天正柱子
- 邻近注释: &&&% 柱子操作 | &&% insert_tarch_column
- 参数: p, width, height, column_type
- 返回: dict: {'success': bool, 'column': 柱对象}
- 关注点: 日志/测试, 时间/等待
- 关键调用: send_cmd_with_sync, wait_quiescent
- 调用概览: send_cmd_with_sync, wait_quiescent, last_obj, info, error
- 理解: 主要用于创建/插入相关逻辑。依据注释：# 【新增】插入天正柱子。邻近注释提示：&&&% 柱子操作；&&% insert_tarch_column。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### modify_column_size(column_obj, width, height)
- 说明: # 【新增】修改柱子尺寸
- 邻近注释: &&% modify_column_size
- 参数: column_obj, width, height
- 返回: bool: 成功返回True
- 关注点: 日志/测试
- 调用概览: set_object_property, info, error
- 理解: 主要用于更新/设置相关逻辑。依据注释：# 【新增】修改柱子尺寸。邻近注释提示：&&% modify_column_size。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### insert_tarch_stair(p1, p2, stair_type)
- 说明: # 【新增】插入天正楼梯
- 邻近注释: &&&% 楼梯操作 | &&% insert_tarch_stair
- 参数: p1, p2, stair_type
- 返回: dict: {'success': bool, 'stair': 楼梯对象}
- 关注点: 日志/测试, 时间/等待
- 关键调用: send_cmd_with_sync, wait_quiescent
- 调用概览: send_cmd_with_sync, wait_quiescent, last_obj, info, error
- 理解: 主要用于创建/插入相关逻辑。依据注释：# 【新增】插入天正楼梯。邻近注释提示：&&&% 楼梯操作；&&% insert_tarch_stair。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### modify_stair_params(stair_obj, **params)
- 说明: # 【新增】修改楼梯参数
- 邻近注释: &&% modify_stair_params
- 参数: stair_obj, **params
- 返回: bool: 成功返回True
- 关注点: 日志/测试
- 调用概览: items, info, set_object_property, error
- 理解: 主要用于更新/设置相关逻辑。依据注释：# 【新增】修改楼梯参数。邻近注释提示：&&% modify_stair_params。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### label_room_name(room_point, name)
- 说明: # 【新增】标注房间名称
- 邻近注释: &&&% 房间标注 | &&% label_room_name
- 参数: room_point, name
- 返回: bool: 成功返回True
- 关注点: 日志/测试, 时间/等待
- 关键调用: send_cmd_with_sync, wait_quiescent
- 调用概览: send_cmd_with_sync, wait_quiescent, info, error
- 理解: 主要用于处理相关逻辑。依据注释：# 【新增】标注房间名称。邻近注释提示：&&&% 房间标注；&&% label_room_name。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### insert_tarch_door_universal(wall_p1, wall_p2, door_key, cmd_name, force_reteach)
- 说明: 【函数编号】: TARCH-UI-PRO-V2 (终极通用版)
- 参数: wall_p1, wall_p2, door_key, cmd_name, force_reteach
- 返回推断: bool
- 关注点: 文件, 时间/等待, 窗口/输入, 选择集
- 关键调用: C.acad
- 调用概览: print, _activate_cad_safe, press, write, sleep, click, moveTo, dragTo, doubleClick, _load_cache_from_disk, _wait_for_user_hover, input...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: TARCH-UI-PRO-V2 (终极通用版)。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

## library/test_monitor.py
- 模块说明: 测试监测模块
### TestMonitor.__init__(self, test_name)
- 说明: 初始化测试监测器
- 参数: self, test_name
- 调用概览: strftime, now
- 理解: 主要用于处理相关逻辑。依据注释：初始化测试监测器。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### TestMonitor.capture_dwg_state(self, description)
- 说明: 捕获当前DWG文件状态
- 参数: self, description
- 返回: dict: DWG文件状态信息
- 关注点: COM, 几何, 日志/测试, 选择集
- 调用概览: info, isoformat, ss_select, sum, error, str, now, len
- 理解: 主要用于处理相关逻辑。依据注释：捕获当前DWG文件状态。实现特征：涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### TestMonitor.capture_folder_state(self, folder_path, description)
- 说明: 捕获文件夹状态
- 参数: self, folder_path, description
- 返回: dict: 文件夹状态信息
- 关注点: 文件, 日志/测试
- 调用概览: info, isoformat, exists, walk, len, error, str, now, join, append, get, getsize...
- 理解: 主要用于处理相关逻辑。依据注释：捕获文件夹状态。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### TestMonitor.before_test(self, dwg_file, output_folders)
- 说明: 测试前监测
- 参数: self, dwg_file, output_folders
- 关注点: 文件, 日志/测试
- 调用概览: info, capture_dwg_state, basename, capture_folder_state
- 理解: 主要用于测试/校验相关逻辑。依据注释：测试前监测。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### TestMonitor.after_test(self, dwg_file, output_folders)
- 说明: 测试后监测
- 参数: self, dwg_file, output_folders
- 关注点: 文件, 日志/测试
- 调用概览: info, strftime, capture_dwg_state, basename, capture_folder_state, now
- 理解: 主要用于测试/校验相关逻辑。依据注释：测试后监测。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### TestMonitor.compare_and_judge(self, expected_changes)
- 说明: 对比测试前后状态并判断是否成功
- 参数: self, expected_changes
- 返回: dict: {
- 关注点: 日志/测试
- 调用概览: info, all, get, items, error, append, len
- 理解: 主要用于处理相关逻辑。依据注释：对比测试前后状态并判断是否成功。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### TestMonitor.save_report(self, result, output_path)
- 说明: 保存测试报告
- 参数: self, result, output_path
- 关注点: 文件, 日志/测试
- 调用概览: makedirs, info, dirname, open, dump
- 理解: 主要用于保存/写入相关逻辑。依据注释：保存测试报告。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

## scripts/apply_modifications.py
- 模块说明: 脚本导航14版修改应用工具
### create_backup(filepath)
- 说明: 创建文件备份
- 参数: filepath
- 返回推断: NoneType,object
- 关注点: 文件
- 调用概览: strftime, exists, copy2, print, now, basename
- 理解: 主要用于创建/插入相关逻辑。依据注释：创建文件备份。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### read_file(filepath)
- 说明: 读取文件内容
- 参数: filepath
- 返回推断: object
- 关注点: 文件
- 调用概览: open, read
- 理解: 主要用于打开/读取相关逻辑。依据注释：读取文件内容。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### write_file(filepath, content)
- 说明: 写入文件
- 参数: filepath, content
- 关注点: 文件
- 调用概览: open, write
- 理解: 主要用于保存/写入相关逻辑。依据注释：写入文件。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### find_function_range(lines, function_name)
- 说明: 查找函数的起始和结束行号
- 参数: lines, function_name
- 返回: (start_line, end_line) 或 None
- 调用概览: enumerate, strip, len, startswith, lstrip
- 理解: 主要用于获取/选择相关逻辑。依据注释：查找函数的起始和结束行号。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### apply_modifications()
- 说明: 应用修改
- 参数: （无）
- 返回推断: bool
- 关注点: 文件
- 调用概览: print, create_backup, read_file, split, find_function_range, join, write_file, exists, copy2, locals, len, basename
- 理解: 主要用于处理相关逻辑。依据注释：应用修改。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

## scripts/auto_TUPDSPACE.py
- 模块说明: （无）
### activate_autocad_window()
- 说明: （无）
- 邻近注释: 激活 AutoCAD 主窗口
- 参数: （无）
- 返回推断: bool
- 关注点: 时间/等待, 选择集
- 调用概览: activate, sleep, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。邻近注释提示：激活 AutoCAD 主窗口。包含选择集构造或过滤。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；超时与重试次数边界

### run_tupdspace_flow(coord_str)
- 说明: （无）
- 邻近注释: 执行 TUPDSPACE 命令流
- 参数: coord_str
- 关注点: 文件, 时间/等待
- 调用概览: print, write, press, sleep
- 理解: 主要用于处理相关逻辑。邻近注释提示：执行 TUPDSPACE 命令流。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### auto_tupdspace_with_repair(coord_str)
- 说明: （无）
- 邻近注释: 主逻辑
- 参数: coord_str
- 返回推断: None
- 关注点: 时间/等待
- 调用概览: print, run_tupdspace_flow, sleep, hotkey, activate_autocad_window
- 理解: 主要用于处理相关逻辑。邻近注释提示：主逻辑。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

## scripts/CAD_basic.py
- 模块说明: （无）
### _cad_safe_print(*args, **kwargs)
- 说明: Wrap built-in print to drop unsupported characters (emoji) on GBK consoles.
- 参数: *args, **kwargs
- 返回推断: NoneType,object
- 调用概览: _orig_print, isinstance, _sanitize, decode, encode
- 理解: 主要用于处理相关逻辑。依据注释：Wrap built-in print to drop unsupported characters (emoji) on GBK consoles.。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _log(func_name, args, kwargs, note)
- 说明: 将错误或超时信息写入 Excel 日志。如果工作表不存在则创建。
- 参数: func_name, args, kwargs, note
- 调用概览: load_workbook, append, save, create_sheet, strftime
- 理解: 主要用于处理相关逻辑。依据注释：将错误或超时信息写入 Excel 日志。如果工作表不存在则创建。。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _kill_acad()
- 说明: 强制结束所有以 acad 开头的 CAD 进程。
- 参数: （无）
- 关注点: 进程
- 调用概览: process_iter, get, startswith, kill, lower
- 理解: 主要用于关闭/终止相关逻辑。依据注释：强制结束所有以 acad 开头的 CAD 进程。。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### connect_database_task()
- 说明: （无）
- 参数: （无）
- 返回推断: str
- 关注点: 时间/等待
- 调用概览: func_set_timeout, print, sleep
- 理解: 主要用于处理相关逻辑。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### safe_save_cad(doc, filepath)
- 说明: （无）
- 参数: doc, filepath
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待
- 调用概览: func_timeout, print, info
- 理解: 主要用于保存/写入相关逻辑。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### timeout_and_log2(timeout_sec)
- 说明: 装饰器：对关键函数添加双重超时保护。
- 邻近注释: &&% 双重超时保护装饰器
- 参数: timeout_sec
- 返回推断: object
- 关注点: 文件, 时间/等待
- 调用概览: wraps, Event, start, func, set, wait, _kill_acad, _log, Thread, format_exc
- 理解: 主要用于处理相关逻辑。依据注释：装饰器：对关键函数添加双重超时保护。。邻近注释提示：&&% 双重超时保护装饰器。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### test_draw_circle_and_wait(center, radius, timeout_sec)
- 说明: 测试：在 CAD 中画圆并触发等待命令，
- 参数: center, radius, timeout_sec
- 返回推断: None,object
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 调用概览: timeout_and_log2, current_dwg_basename, draw_circle, SendCommand, start, print, time, info, sleep, Thread, getattr, _log
- 理解: 主要用于创建/插入相关逻辑。依据注释：测试：在 CAD 中画圆并触发等待命令，。实现特征：通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### wait_quiescent_ceshi()
- 说明: 详细拆解 "._ZOOM _E "片段含义解析.原生别理会用户是否修改过这个命令，
- 邻近注释: &&% 测试轮询等待
- 参数: （无）
- 关注点: 时间/等待
- 关键调用: wait_quiescent, C.doc
- 调用概览: open_file, wait_quiescent, PostCommand
- 理解: 主要用于等待/守护相关逻辑。依据注释：详细拆解 "._ZOOM _E "片段含义解析.原生别理会用户是否修改过这个命令，。邻近注释提示：&&% 测试轮询等待。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### complex_operation_demo()
- 说明: 不要用旧窗口
- 邻近注释: &&% 测试PostCommand
- 参数: （无）
- 关注点: 几何, 文件, 时间/等待
- 关键调用: wait_quiescent, C.li, C.doc
- 调用概览: append, print, li, join, Activate, PostCommand, sleep, wait_quiescent
- 理解: 主要用于处理相关逻辑。依据注释：不要用旧窗口。邻近注释提示：&&% 测试PostCommand。实现特征：包含空闲等待以同步 CAD 状态。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### draw_infinite_spiral()
- 说明: （无）
- 邻近注释: &&% 测试卡住状态
- 参数: （无）
- 返回推断: None,object
- 关注点: COM, 几何, 时间/等待, 进程
- 调用概览: print, retry_if_busy, GetActiveObject, AddLine, set_attr, Update, VARIANT, safe_add_line, sleep, cos, sin, safe_update
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：&&% 测试卡住状态。实现特征：创建直线对象。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### speak_msg(text)
- 说明: 后台线程播放语音，避免阻塞 CAD 主进程
- 参数: text
- 返回推断: None
- 关注点: 文件
- 调用概览: Thread, start, init, setProperty, say, runAndWait
- 理解: 主要用于处理相关逻辑。依据注释：后台线程播放语音，避免阻塞 CAD 主进程。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### com_to_handle(obj)
- 说明: 如果是 COM 对象，则返回它的 Handle（字符串）；否则原样返回 obj。
- 邻近注释: ———————— 加载指定 DWG 的打印字典 ————————
- 参数: obj
- 返回推断: object
- 关注点: COM
- 调用概览: hasattr
- 理解: 主要用于处理相关逻辑。依据注释：如果是 COM 对象，则返回它的 Handle（字符串）；否则原样返回 obj。。邻近注释提示：———————— 加载指定 DWG 的打印字典 ————————。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### serialize(obj)
- 说明: 递归地将 dict/list/tuple/COMObject 转为只含基础类型(包括 handle 字符串)的结构。
- 参数: obj
- 返回推断: object
- 调用概览: isinstance, com_to_handle, tuple, serialize, items
- 理解: 主要用于处理相关逻辑。依据注释：递归地将 dict/list/tuple/COMObject 转为只含基础类型(包括 handle 字符串)的结构。。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### save_print_dict_generic(dwg_name, bind_dict)
- 说明: 将 bind_dict 序列化并写入 JSON 文件，键为 dwg_name。
- 邻近注释: &&% 保存打印字典
- 参数: dwg_name, bind_dict
- 关注点: COM, 文件, 日志/测试
- 调用概览: serialize, join, info, open, dump
- 理解: 主要用于保存/写入相关逻辑。依据注释：将 bind_dict 序列化并写入 JSON 文件，键为 dwg_name。。邻近注释提示：&&% 保存打印字典。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### load(dwg_name)
- 说明: 从 JSON 文件加载之前保存的打印字典（只含基本类型 & handle 字符串）。
- 邻近注释: &&% 加载打印字典
- 参数: dwg_name
- 返回推断: dict,object
- 关注点: 文件, 日志/测试
- 调用概览: join, isfile, info, open, load
- 理解: 主要用于打开/读取相关逻辑。依据注释：从 JSON 文件加载之前保存的打印字典（只含基本类型 & handle 字符串）。。邻近注释提示：&&% 加载打印字典。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### current_dwg_basename()
- 说明: acad.ActiveDocument.Name 可能带路径或带 .dwg，
- 邻近注释: ———————— 辅助：获取当前 DWG 的纯文件名 ————————
- 参数: （无）
- 返回推断: object
- 关注点: COM, 文件
- 调用概览: splitext, basename
- 理解: 主要用于处理相关逻辑。依据注释：acad.ActiveDocument.Name 可能带路径或带 .dwg，。邻近注释提示：———————— 辅助：获取当前 DWG 的纯文件名 ————————。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### current_dwg_folder()
- 说明: 【V2.0 安全版】获取当前激活文档所在的文件夹路径。
- 参数: （无）
- 返回推断: NoneType,object
- 关注点: COM, 文件, 进程
- 关键调用: C.doc
- 调用概览: getattr, dirname, GetActiveObject
- 理解: 主要用于处理相关逻辑。依据注释：【V2.0 安全版】获取当前激活文档所在的文件夹路径。。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### vtpnt(x, y, z)
- 说明: 坐标点转化为浮点数
- 邻近注释: &&% 数据类型转换函数
- 参数: x, y, z
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于处理相关逻辑。依据注释：坐标点转化为浮点数。邻近注释提示：&&% 数据类型转换函数。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### vtobj(obj)
- 说明: 转化为对象数组
- 参数: obj
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于处理相关逻辑。依据注释：转化为对象数组。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### vtFloat(lst)
- 说明: 列表转化为浮点数
- 参数: lst
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于处理相关逻辑。依据注释：列表转化为浮点数。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### vtInt(lst)
- 说明: 列表转化为整数
- 参数: lst
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于处理相关逻辑。依据注释：列表转化为整数。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### vtVariant(lst)
- 说明: 列表转化为变体
- 参数: lst
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于处理相关逻辑。依据注释：列表转化为变体。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### ConvertArrays2Variant(inputdata, vartype)
- 说明: （无）
- 参数: inputdata, vartype
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于转换/解析相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### vtlist(obj_list)
- 说明: 将对象列表转为 VARIANT 类型以供 COM 接口使用
- 参数: obj_list
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于获取/选择相关逻辑。依据注释：将对象列表转为 VARIANT 类型以供 COM 接口使用。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### start_applicationV9(PTH, max_retries, retry_delay)
- 说明: 【核心启动器】
- 邻近注释: &&% 启动天正CAD及守护进程
- 参数: PTH, max_retries, retry_delay
- 返回: Popen 对象（CAD主进程），失败返回 None。
- 关注点: 文件, 日志/测试, 时间/等待, 进程
- 调用概览: join, dirname, range, info, abspath, exists, Popen, sleep, print, launch_helper_script, poll
- 理解: 主要用于处理相关逻辑。依据注释：【核心启动器】。邻近注释提示：&&% 启动天正CAD及守护进程。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### force_show_cad_interface()
- 说明: 【辅助函数】强制显示并最大化现有的 AutoCAD 窗口
- 参数: （无）
- 返回推断: bool
- 关注点: COM, 日志/测试, 窗口/输入, 进程, 选择集
- 调用概览: GetActiveObject, ShowWindow, SetForegroundWindow, print, info
- 理解: 主要用于处理相关逻辑。依据注释：【辅助函数】强制显示并最大化现有的 AutoCAD 窗口。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；依赖窗口/输入焦点，易受环境影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境

### st()
- 说明: （无）
- 邻近注释: &&% 常规启动
- 参数: （无）
- 返回推断: bool
- 关键调用: C.doc
- 调用概览: cad_zt_oneb, jd, jc, print
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 常规启动。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_acad_process_id(ming)
- 说明: （无）
- 参数: ming
- 返回推断: NoneType,object
- 关注点: 进程
- 调用概览: process_iter, str, lower
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### jingchengshu_wenjian()
- 说明: （无）
- 参数: （无）
- 返回推断: object
- 关注点: 进程
- 调用概览: alias, process_iter
- 理解: 主要用于处理相关逻辑。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### close_all_cad_processes()
- 说明: 强制关闭所有CAD进程
- 邻近注释: &&% 关闭所有CAD进程
- 参数: （无）
- 返回: True表示成功，False表示失败
- 关注点: 日志/测试, 时间/等待, 进程
- 调用概览: range, print, jingchengshu_wenjian, info, run, sleep
- 理解: 主要用于关闭/终止相关逻辑。依据注释：强制关闭所有CAD进程。邻近注释提示：&&% 关闭所有CAD进程。
- 风险: 涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### close_oldest_cad_process(process_name)
- 说明: （无）
- 邻近注释: &&% 关闭最早CAD进程
- 参数: process_name
- 关注点: 日志/测试, 进程
- 调用概览: len, print, process_iter, sorted, terminate, info, Process
- 理解: 主要用于关闭/终止相关逻辑。邻近注释提示：&&% 关闭最早CAD进程。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### ensure_typelib_from_running()
- 说明: 从正在运行的 AutoCAD 直接生成 makepy（不依赖注册表）
- 参数: （无）
- 关注点: 进程
- 调用概览: _coinit_once, EnsureDispatch, GetContainingTypeLib, GenerateFromTypeLibSpec, GetTypeInfo
- 理解: 主要用于处理相关逻辑。依据注释：从正在运行的 AutoCAD 直接生成 makepy（不依赖注册表）。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### _ComLiveProxy.__init__(self, getter)
- 说明: （无）
- 参数: self, getter
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _ComLiveProxy.__getattr__(self, name)
- 说明: （无）
- 参数: self, name
- 返回推断: object
- 调用概览: _getter, getattr
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _ComLiveProxy.__dir__(self)
- 说明: （无）
- 邻近注释: 可选：允许直接作为可迭代或 bool 使用时更自然
- 参数: self
- 返回推断: object
- 调用概览: dir, _getter
- 理解: 主要用于处理相关逻辑。邻近注释提示：可选：允许直接作为可迭代或 bool 使用时更自然。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### zoom_window(x1, y1, x2, y2, pad_ratio, doc)
- 说明: （无）
- 邻近注释: &&% 窗口缩放
- 参数: x1, y1, x2, y2, pad_ratio, doc
- 调用概览: normalize_rect, send_cmd
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 窗口缩放。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### aci_to_rgb(ci)
- 说明: （无）
- 邻近注释: &&&% RGB色彩
- 参数: ci
- 返回推断: object
- 调用概览: get, int
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&&% RGB色彩。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_entity_rgb(ent)
- 说明: 返回 (rgb_tuple_or_None, source_str)
- 邻近注释: &&% 获取实体RGB
- 参数: ent
- 返回推断: tuple
- 调用概览: getattr, Item, isinstance, aci_to_rgb, hasattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：返回 (rgb_tuple_or_None, source_str)。邻近注释提示：&&% 获取实体RGB。实现特征：涉及图层操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### chongfu_caozuo(Fx, dwg_instance, args, kwargs, max_retries, failure_value)
- 说明: 对指定函数/方法进行重复调用，直到成功或耗尽重试次数。
- 邻近注释: &&&%  * 重复多次调用函数 | &&% 重复操作
- 参数: Fx, dwg_instance, args, kwargs, max_retries, failure_value
- 返回推断: tuple
- 关注点: 日志/测试, 时间/等待
- 调用概览: range, Fx, getattr, info, sleep, print, li
- 理解: 主要用于处理相关逻辑。依据注释：对指定函数/方法进行重复调用，直到成功或耗尽重试次数。。邻近注释提示：&&&%  * 重复多次调用函数；&&% 重复操作。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### simple_timer(func)
- 说明: （无）
- 邻近注释: &&% 简单计时器
- 参数: func
- 返回推断: object
- 关注点: 日志/测试
- 调用概览: time, func, info
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 简单计时器。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _coinit_once()
- 说明: 线程初始化防呆设计
- 参数: （无）
- 关注点: COM
- 调用概览: CoInitialize
- 理解: 主要用于处理相关逻辑。依据注释：线程初始化防呆设计。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_acad_doc(max_wait)
- 说明: [底层原语] 获取/启动 AutoCAD 应用和文档 (安全修正版)暂时保留给引用20250106
- 参数: max_wait
- 返回推断: tuple
- 关注点: COM, 日志/测试, 时间/等待, 进程
- 调用概览: _coinit_once, time, GetActiveObject, EnsureDispatch, print, sleep, RuntimeError, info, Add, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：[底层原语] 获取/启动 AutoCAD 应用和文档 (安全修正版)暂时保留给引用20250106。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### normalize_rect(x1, y1, x2, y2)
- 说明: （无）
- 参数: x1, y1, x2, y2
- 返回推断: tuple
- 调用概览: sorted
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_pmxz_group_bbox()
- 说明: 使用 pmxz() 选择一组对象，计算它们的整体外包盒。
- 邻近注释: &&&% 属性 | &&% 获取选择集包围盒
- 参数: （无）
- 返回: (bbox_corners, rect_xy)
- 关注点: 几何, 日志/测试
- 调用概览: print, info, group_bbox_corners, pmxz, repr, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：使用 pmxz() 选择一组对象，计算它们的整体外包盒。。邻近注释提示：&&&% 属性；&&% 获取选择集包围盒。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### g()
- 说明: （无）
- 邻近注释: &&% 获取选择集包围盒别名
- 参数: （无）
- 关注点: 几何
- 调用概览: get_pmxz_group_bbox
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 获取选择集包围盒别名。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### align_last_ms_obj_lb_to_origin()
- 说明: 选择当前激活图中“模型空间最后一个对象”，
- 邻近注释: &&% 最后对象对齐原点
- 参数: （无）
- 返回推断: NoneType,object
- 关注点: COM, 日志/测试
- 关键调用: C.doc
- 调用概览: getattr, info, print, last_obj, GetBoundingBox, VARIANT, Move, float
- 理解: 主要用于处理相关逻辑。依据注释：选择当前激活图中“模型空间最后一个对象”，。邻近注释提示：&&% 最后对象对齐原点。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_entity_full_info(entity)
- 说明: 基于优化后的 get_attr，获取实体的完整位置信息和图层属性。
- 参数: entity
- 返回: dict: {
- 关注点: COM, 日志/测试
- 调用概览: get_attr, ObjectIdToObject, Item, Dispatch, info
- 理解: 主要用于获取/选择相关逻辑。依据注释：基于优化后的 get_attr，获取实体的完整位置信息和图层属性。。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### compute_line_angle(line)
- 说明: 计算直线的方向角（单位：度），基于 StartPoint / EndPoint。
- 邻近注释: 线段分析 | &&% 计算直线角度
- 参数: line
- 返回推断: NoneType,object
- 关注点: 几何
- 调用概览: atan2, degrees, print
- 理解: 主要用于计算/测量相关逻辑。依据注释：计算直线的方向角（单位：度），基于 StartPoint / EndPoint。。邻近注释提示：线段分析；&&% 计算直线角度。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_point(pt)
- 说明: 在模型空间绘制一个 AutoCAD 点实体。
- 邻近注释: &&% 绘制点
- 参数: pt
- 返回: 新创建的 Point 对象；失败时返回 None
- 关注点: 几何, 日志/测试
- 调用概览: AddPoint, vtpnt, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：在模型空间绘制一个 AutoCAD 点实体。。邻近注释提示：&&% 绘制点。实现特征：创建点对象。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_line(p1, p2)
- 说明: 在模型空间中绘制从 p1 到 p2 的直线段。
- 邻近注释: &&% 绘制直线
- 参数: p1, p2
- 返回: 新创建的直线对象（COM 对象）
- 关注点: 日志/测试
- 调用概览: AddLine, vtpnt, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：在模型空间中绘制从 p1 到 p2 的直线段。。邻近注释提示：&&% 绘制直线。实现特征：创建直线对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_circle(center, radius)
- 说明: 以 center 为圆心、radius 为半径绘制圆。
- 邻近注释: &&% 绘制圆
- 参数: center, radius
- 返回: 新创建的 Circle 对象；失败时返回 None
- 关注点: 日志/测试
- 调用概览: AddCircle, vtpnt, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：以 center 为圆心、radius 为半径绘制圆。。邻近注释提示：&&% 绘制圆。实现特征：创建圆对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_regular_polygon(center, radius, sides)
- 说明: 绘制正多边形（LWPolyline，已闭合）
- 邻近注释: &&% 绘制正多边形
- 参数: center, radius, sides
- 返回推断: NoneType,object
- 关注点: COM, 几何, 日志/测试
- 调用概览: range, print, extend, VARIANT, AddLightWeightPolyline, info, cos, sin
- 理解: 主要用于创建/插入相关逻辑。依据注释：绘制正多边形（LWPolyline，已闭合）。邻近注释提示：&&% 绘制正多边形。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### prioritize_horizontal(lines, tol)
- 说明: 将列表中所有“水平”直线段（起点和终点的 y 差小于 tol）放在最前面，
- 邻近注释: &&% 优先水平线
- 参数: lines, tol
- 返回推断: tuple
- 关注点: 几何
- 调用概览: abs, append
- 理解: 主要用于处理相关逻辑。依据注释：将列表中所有“水平”直线段（起点和终点的 y 差小于 tol）放在最前面，。邻近注释提示：&&% 优先水平线。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_spline_length_by_conversion(spline_entity)
- 说明: 将样条曲线对象复制、高亮并通过 _SPLINEDIT 转为多段线，
- 邻近注释: &&% 获取样条曲线长度
- 参数: spline_entity
- 返回: 样条曲线转换后的长度值（float）
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 调用概览: Copy, highlight_entity_by_bbox, SendCommand, sleep, Item, hasattr, Delete, print, info
- 理解: 主要用于获取/选择相关逻辑。依据注释：将样条曲线对象复制、高亮并通过 _SPLINEDIT 转为多段线，。邻近注释提示：&&% 获取样条曲线长度。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### estimate_ellipse_length(ellipse)
- 说明: 估算椭圆对象的长度（周长），使用 Ramanujan 公式。
- 邻近注释: &&% 估算椭圆周长
- 参数: ellipse
- 返回推断: NoneType,object
- 关注点: 日志/测试
- 调用概览: sqrt, info
- 理解: 主要用于计算/测量相关逻辑。依据注释：估算椭圆对象的长度（周长），使用 Ramanujan 公式。。邻近注释提示：&&% 估算椭圆周长。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_entity_geometry_info(obj)
- 说明: 根据图元类型返回其关键几何信息：
- 邻近注释: &&% 获取几何信息
- 参数: obj
- 返回推断: dict
- 关注点: 几何
- 调用概览: lower, dist, str, sqrt, getattr, GetFitPoint, get_spline_length_by_conversion
- 理解: 主要用于获取/选择相关逻辑。依据注释：根据图元类型返回其关键几何信息：。邻近注释提示：&&% 获取几何信息。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### points_on_line_at_distance_3d(p1, p2, px, distance)
- 说明: 已知 px 在由 p1->p2 确定的直线上，返回在该直线上与 px 距离为 distance 的两个点。
- 邻近注释: 在两点确定的方向上，返回与对象点指定距离的点 | &&% 直线定距点
- 参数: p1, p2, px, distance
- 返回推断: list
- 关注点: 几何
- 调用概览: sqrt, ValueError
- 理解: 主要用于计算/测量相关逻辑。依据注释：已知 px 在由 p1->p2 确定的直线上，返回在该直线上与 px 距离为 distance 的两个点。。邻近注释提示：在两点确定的方向上，返回与对象点指定距离的点；&&% 直线定距点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_fake_intersection_regions(lines, tol, real_tol)
- 说明: 查找伪相交区域：对于任意线段 A 的端点 P，若：
- 邻近注释: 找出一组直线段内的伪相交区域 | &&% 查找伪交点区域
- 参数: lines, tol, real_tol
- 返回推断: object
- 关注点: COM, 几何, 日志/测试
- 调用概览: ensure_layer, print, max, hypot, min, tuple, append, info, round, point_to_line_distance, AddCircle, vtpnt
- 理解: 主要用于获取/选择相关逻辑。依据注释：查找伪相交区域：对于任意线段 A 的端点 P，若：。邻近注释提示：找出一组直线段内的伪相交区域；&&% 查找伪交点区域。实现特征：创建圆对象。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### lines_daduan(start_point, end_point)
- 说明: 这个命令对于避免天正墙体没有出现不相交的覆盖是非常重要的，直接应用天正的tlinebk
- 邻近注释: 把区域内的直线段交点打断 | &&% 直线打断
- 参数: start_point, end_point
- 关注点: COM
- 调用概览: SendCommand, chr
- 理解: 主要用于处理相关逻辑。依据注释：这个命令对于避免天正墙体没有出现不相交的覆盖是非常重要的，直接应用天正的tlinebk。邻近注释提示：把区域内的直线段交点打断；&&% 直线打断。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### delete_duplicate_lines(lines, tol)
- 说明: 删除重复的直线段，仅保留每组中一条。
- 邻近注释: 找出一组直线段中的所有直线段中所有重复的线段并删除 | &&% 删除重复直线
- 参数: lines, tol
- 返回推断: bool,object
- 关注点: 几何, 日志/测试
- 调用概览: enumerate, info, all, range, is_duplicate, append, Delete, len, abs, zip, is_same_point
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除重复的直线段，仅保留每组中一条。。邻近注释提示：找出一组直线段中的所有直线段中所有重复的线段并删除；&&% 删除重复直线。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### delete_redundant_lines(lines, tol)
- 说明: 删除重复线段和局部重复线段，只保留每组中的一条。
- 邻近注释: 删除完全或局部重复线段 | &&% 删除冗余直线
- 参数: lines, tol
- 返回推断: bool,object
- 关注点: COM, 几何, 日志/测试
- 调用概览: set, len, range, info, abs, is_completely_duplicate, point_on_segment, add, is_locally_duplicate, Delete, is_same_point
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除重复线段和局部重复线段，只保留每组中的一条。。邻近注释提示：删除完全或局部重复线段；&&% 删除冗余直线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_isolated_intersections(LB, tol)
- 说明: 找出线段列表 LB 中的孤立线段，并计算它们与其它线段的所有交点。
- 邻近注释: 找出一组直线段中的孤立线段产生的交点 | &&% 查找孤立交点
- 参数: LB, tol
- 返回: intersections: 交点列表，每个元素是 (x, y, z)
- 调用概览: enumerate, Delete, abs, append, segment_intersection, same_point
- 理解: 主要用于获取/选择相关逻辑。依据注释：找出线段列表 LB 中的孤立线段，并计算它们与其它线段的所有交点。。邻近注释提示：找出一组直线段中的孤立线段产生的交点；&&% 查找孤立交点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_inner_point_of_polygon(polygon)
- 说明: 获取给定 polygon 的一个保证在其内部的点。
- 邻近注释: doc.sendcommand("TSpOutline"+chr(13)+"41849.69465957, 12250.50102376, 0"+chr(13)+chr(13)+chr(13)) | doc.sendcommand("TRoflna"+chr(13)+"0"+chr(13)) | &&% 获取多边形内点
- 参数: polygon
- 返回: (x, y): 内部点坐标元组
- 关注点: 几何
- 调用概览: representative_point, isinstance, ValueError
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取给定 polygon 的一个保证在其内部的点。。邻近注释提示：doc.sendcommand("TSpOutline"+chr(13)+"41849.69465957, 12250.50102376, 0"+chr(13)+chr(13)+chr(13))；doc.sendcommand("TRoflna"+chr(13)+"0"+chr(13))；&&% 获取多边形内点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_room_outline_from_point(x, y, z)
- 说明: 自动发送 TSpOutline 命令，从指定点获取房间轮廓。
- 邻近注释: &&% 获取房间轮廓
- 参数: x, y, z
- 关注点: COM, 日志/测试
- 调用概览: SendCommand, info, chr
- 理解: 主要用于获取/选择相关逻辑。依据注释：自动发送 TSpOutline 命令，从指定点获取房间轮廓。。邻近注释提示：&&% 获取房间轮廓。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### connect_lines_to_polyline_if_closed(lines, tol)
- 说明: 判断线段是否首尾连接成闭合多边形，如果是，则绘制PL多段线。
- 邻近注释: &&% 连接闭合多段线
- 参数: lines, tol
- 返回: 多段线对象，或 None。
- 关注点: COM, 几何, 日志/测试
- 调用概览: set, add, append, AddLightWeightPolyline, print, enumerate, distance, extend, vtFloat, info, Point
- 理解: 主要用于关闭/终止相关逻辑。依据注释：判断线段是否首尾连接成闭合多边形，如果是，则绘制PL多段线。。邻近注释提示：&&% 连接闭合多段线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### is_closed_polygon_from_lines(lines, tol)
- 说明: 判断一组 AutoCAD 直线段是否首尾连接形成闭合多边形。
- 邻近注释: &&% 判断闭合多边形
- 参数: lines, tol
- 返回: True 表示首尾闭合形成多边形，False 否则
- 关注点: 几何, 日志/测试
- 调用概览: set, add, enumerate, info, append, distance, len, Point
- 理解: 主要用于关闭/终止相关逻辑。依据注释：判断一组 AutoCAD 直线段是否首尾连接形成闭合多边形。。邻近注释提示：&&% 判断闭合多边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### same_point(p1, p2, tol)
- 说明: 判断两个点是否在容差范围内相同（只比较 X、Y 坐标）
- 邻近注释: &&% 判断同点
- 参数: p1, p2, tol
- 返回推断: object
- 调用概览: abs
- 理解: 主要用于处理相关逻辑。依据注释：判断两个点是否在容差范围内相同（只比较 X、Y 坐标）。邻近注释提示：&&% 判断同点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### same_line(ln1, ln2, tol)
- 说明: 判断两条线段 ln1 和 ln2 是否“相同”
- 邻近注释: &&% 判断同线
- 参数: ln1, ln2, tol
- 返回推断: object
- 关注点: 几何
- 调用概览: tuple, same_point
- 理解: 主要用于处理相关逻辑。依据注释：判断两条线段 ln1 和 ln2 是否“相同”。邻近注释提示：&&% 判断同线。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### calculate_absolute_angle(line, P, tol)
- 说明: 计算线段（line）从点 P 出发的绝对角度（0-360°）
- 邻近注释: &&% 计算绝对角度
- 参数: line, P, tol
- 返回推断: object
- 关注点: 几何
- 调用概览: tuple, same_point, degrees, atan2
- 理解: 主要用于计算/测量相关逻辑。依据注释：计算线段（line）从点 P 出发的绝对角度（0-360°）。邻近注释提示：&&% 计算绝对角度。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### calculate_relative_angle(line, P, current_line, tol)
- 说明: 计算当前参考线（current_line）与候选线段（line）之间的相对角度，
- 邻近注释: &&% 计算相对角度
- 参数: line, P, current_line, tol
- 返回推断: object
- 关注点: 几何
- 调用概览: tuple, same_point, angle, degrees, atan2
- 理解: 主要用于计算/测量相关逻辑。依据注释：计算当前参考线（current_line）与候选线段（line）之间的相对角度，。邻近注释提示：&&% 计算相对角度。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_lines_angle(lines, P, tol)
- 说明: 查找与指定点 P 共端点的所有线段，并按从 P 出发离开的绝对几何角度排序。
- 邻近注释: 函数：查找给定点P经过的线段，按照绝对角度排序 | &&% 按角度查找线段
- 参数: lines, P, tol
- 返回: 按绝对角度从小到大排序的共点线段列表。
- 关注点: COM, 几何, 日志/测试
- 调用概览: tuple, info, sort, print, abs, append, calculate_absolute_angle, getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：查找与指定点 P 共端点的所有线段，并按从 P 出发离开的绝对几何角度排序。。邻近注释提示：函数：查找给定点P经过的线段，按照绝对角度排序；&&% 按角度查找线段。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_lines_sharing_point(lines, P, current_line, tol)
- 说明: 查找与指定点 P 共端点的所有线段，并按从 current_line 逆时针旋转到其他线段的相对角度排序。
- 邻近注释: 函数：查找与P共点的线段，按照与当前线段的相对角度排序 | &&% 查找共点线段
- 参数: lines, P, current_line, tol
- 返回: 按相对角度从小到大排序的经过 P 的线段列表（current_line 亦包括其中）。
- 关注点: COM, 几何, 日志/测试
- 调用概览: tuple, sort, append, info, calculate_relative_angle, abs, getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：查找与指定点 P 共端点的所有线段，并按从 current_line 逆时针旋转到其他线段的相对角度排序。。邻近注释提示：函数：查找与P共点的线段，按照与当前线段的相对角度排序；&&% 查找共点线段。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_successor_line_max(current_line, lines, P, tol)
- 说明: 在给定共点 P 处，排除当前线段（current_line）后，
- 邻近注释: 函数：根据当前线段和共点 P，选择下一条后继线段（选择相对角度最大的那条），返回 (后继线段, 新共点) | &&% 查找最大转角后继线
- 参数: current_line, lines, P, tol
- 返回: (后继线段, 新共点)，若找不到合适的后继线段，则返回 (None, P)。
- 关注点: COM, 几何, 日志/测试
- 调用概览: find_lines_sharing_point, info, calculate_relative_angle, same_point, tuple
- 理解: 主要用于获取/选择相关逻辑。依据注释：在给定共点 P 处，排除当前线段（current_line）后，。邻近注释提示：函数：根据当前线段和共点 P，选择下一条后继线段（选择相对角度最大的那条），返回 (后继线段, 新共点)；&&% 查找最大转角后继线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_rightbottom_point(lines, tol)
- 说明: 从所有线段端点中，找出 y 值最小的点；若有多个，则选 x 最大的点作为最右下角点。
- 邻近注释: &&%##################### | 辅助函数：从所有线段中找出最右下角的点 | &&% 查找右下角点
- 参数: lines, tol
- 返回推断: NoneType,object
- 关注点: 几何, 日志/测试
- 调用概览: min, max, info, hasattr, append, tuple, abs
- 理解: 主要用于获取/选择相关逻辑。依据注释：从所有线段端点中，找出 y 值最小的点；若有多个，则选 x 最大的点作为最右下角点。。邻近注释提示：&&%#####################；辅助函数：从所有线段中找出最右下角的点；&&% 查找右下角点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_rightbottom_closed_polygon(lines, tol, max_steps)
- 说明: 利用所有线段构造封闭多边形：
- 邻近注释: &&% 查找右下角闭合多边形
- 参数: lines, tol, max_steps
- 返回: 构成封闭多边形的点列表（依次为每条边的终点），若无法构成则返回 None。
- 关注点: COM, 几何, 日志/测试
- 调用概览: find_rightbottom_point, find_lines_angle, info, tuple, same_point, print, find_successor_line_max, append, add, calculate_absolute_angle
- 理解: 主要用于关闭/终止相关逻辑。依据注释：利用所有线段构造封闭多边形：。邻近注释提示：&&% 查找右下角闭合多边形。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### draw_polygon_as_polyline(polygon, layer_name, tol)
- 说明: 将构造的多边形（polygon）转换为顶点序列，并在当前 AutoCAD 文档 doc 的 ModelSpace 中添加
- 邻近注释: 从com边或顶点坐标列表用PL复线绘制多边形 | &&% 绘制多边形
- 参数: polygon, layer_name, tol
- 返回: 成功时返回创建的多段线对象（PLINE），否则返回 None。
- 关注点: COM, 几何, 日志/测试
- 调用概览: isinstance, print, enumerate, tuple, VARIANT, same_point, append, info, extend, Item, AddPolyline, Update...
- 理解: 主要用于创建/插入相关逻辑。依据注释：将构造的多边形（polygon）转换为顶点序列，并在当前 AutoCAD 文档 doc 的 ModelSpace 中添加。邻近注释提示：从com边或顶点坐标列表用PL复线绘制多边形；&&% 绘制多边形。实现特征：涉及图层操作。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### is_nearly_equal(p1, p2, tol)
- 说明: （无）
- 邻近注释: ----------------------------------------------------- | 辅助函数：判断两个点是否近似相等（仅比较 x 和 y 坐标） | &&% 近似相等
- 参数: p1, p2, tol
- 返回推断: object
- 调用概览: abs
- 理解: 主要用于处理相关逻辑。邻近注释提示：-----------------------------------------------------；辅助函数：判断两个点是否近似相等（仅比较 x 和 y 坐标）；&&% 近似相等。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_successor_line_min(current_line, lines, P, tol)
- 说明: （无）
- 邻近注释: ----------------------------------------------------- | 寻找后继线段：在共点 P 处，从当前边之外的候选边中选择相对角度最小的边 | &&% 查找最小转角后继线
- 参数: current_line, lines, P, tol
- 返回推断: tuple
- 关注点: COM, 几何, 日志/测试
- 调用概览: tuple, info, calculate_relative_angle, is_nearly_equal, append, abs
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：-----------------------------------------------------；寻找后继线段：在共点 P 处，从当前边之外的候选边中选择相对角度最小的边；&&% 查找最小转角后继线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_outer_contour(lines, tol, max_steps)
- 说明: 获取一组直线段的外轮廓线
- 邻近注释: (3) | 获取一组直线段的外轮廓线 | &&% 获取外轮廓
- 参数: lines, tol, max_steps
- 返回: 外轮廓线构成的线段列表，如果无法构成封闭轮廓则返回空列表。
- 关注点: COM, 几何, 日志/测试
- 调用概览: find_rightbottom_point, info, find_lines_angle, tuple, is_nearly_equal, print, find_successor_line_min, append, add
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取一组直线段的外轮廓线。邻近注释提示：(3)；获取一组直线段的外轮廓线；&&% 获取外轮廓。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### deduplicate_vertices(vertices, tol)
- 说明: 去掉顶点列表中相邻重复的顶点：
- 邻近注释: &&% 顶点去重
- 参数: vertices, tol
- 返回: 处理后的顶点列表，只有中间连续重复的点被去除，保留闭合多边形的首尾重复。
- 调用概览: len, range, sqrt, append, same_point
- 理解: 主要用于移动/复制相关逻辑。依据注释：去掉顶点列表中相邻重复的顶点：。邻近注释提示：&&% 顶点去重。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### analyze_polygon_branches(PL, lines, p1, tol)
- 说明: 分析封闭多边形 PL 的分枝情况。PL 为封闭多边形的顶点列表（按逆时针顺序排列），
- 邻近注释: (4) | 获取最右下角的封闭多边形不影响其他封闭多边形的连续边的顶点列表 | &&% 分析多边形分支
- 参数: PL, lines, p1, tol
- 返回: 返回从 D1 到 D2（包含 D1 和 D2）的连续顶点序列，此序列包含了 LN 的顶点。
- 关注点: 几何
- 调用概览: len, is_multi_branch, print, deduplicate_vertices, index, list, any, append, reversed, tuple, same_point
- 理解: 主要用于处理相关逻辑。依据注释：分析封闭多边形 PL 的分枝情况。PL 为封闭多边形的顶点列表（按逆时针顺序排列），。邻近注释提示：(4)；获取最右下角的封闭多边形不影响其他封闭多边形的连续边的顶点列表；&&% 分析多边形分支。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### remove_lines_in_LBv(lines, LB_v, tol)
- 说明: 从 COM 线段列表 lines 中移除那些其两个顶点都在 LB_v 中的线段。
- 邻近注释: 根据输入的顶点列表判断，将lines的其顶点在该顶点列表的线段移出列表 | &&% 移除指定顶点线段
- 参数: lines, LB_v, tol
- 返回: 返回移除满足条件（即两端点都在 LB_v 中）的线段后剩余的线段列表。
- 关注点: COM, 几何, 文件, 日志/测试
- 调用概览: any, tuple, append, info, abs, same_point
- 理解: 主要用于删除/清理相关逻辑。依据注释：从 COM 线段列表 lines 中移除那些其两个顶点都在 LB_v 中的线段。。邻近注释提示：根据输入的顶点列表判断，将lines的其顶点在该顶点列表的线段移出列表；&&% 移除指定顶点线段。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### process_polygons(lines, tol, max_steps, layer_name)
- 说明: 递归提取并绘制直线段集 lines 中所有封闭多边形。
- 邻近注释: (5) | &&% 获取全部封闭多边形，但不完全 | &&% 处理多边形
- 参数: lines, tol, max_steps, layer_name
- 返回: (LB, LBcom, LB_yc)，其中：
- 关注点: 几何, 文件, 日志/测试
- 调用概览: info, find_rightbottom_point, find_rightbottom_closed_polygon, append, print, analyze_polygon_branches, draw_polygon_as_polyline, remove_lines_in_LBv, len
- 理解: 主要用于处理相关逻辑。依据注释：递归提取并绘制直线段集 lines 中所有封闭多边形。。邻近注释提示：(5)；&&% 获取全部封闭多边形，但不完全；&&% 处理多边形。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### extract_polygon_from_lines(lines, tol)
- 说明: 将表示封闭多边形边缘的线段（COM对象列表）转换为顶点列表（按顺序排列），
- 邻近注释: &&% 提取多边形
- 参数: lines, tol
- 返回: 顶点列表，如 [p1, p2, ..., pn]，其中 p1 表示多边形的起点（不重复列出闭合顶点）。
- 关注点: 几何, 文件
- 调用概览: list, range, tuple, print, len, remove, same_point, append, deduplicate_vertices
- 理解: 主要用于处理相关逻辑。依据注释：将表示封闭多边形边缘的线段（COM对象列表）转换为顶点列表（按顺序排列），。邻近注释提示：&&% 提取多边形。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### explode_polylines(LB)
- 说明: 对多段线列表 LB 中的每一个多段线，调用 .Explode() 方法，
- 邻近注释: 将多段线列表炸开为线段，返回线段列表 | &&% 炸开多段线
- 参数: LB
- 返回: 一个包含所有炸开后直线段 COM 对象的列表。
- 关注点: COM, 几何, 日志/测试
- 调用概览: Explode, append, getattr, info
- 理解: 主要用于处理相关逻辑。依据注释：对多段线列表 LB 中的每一个多段线，调用 .Explode() 方法，。邻近注释提示：将多段线列表炸开为线段，返回线段列表；&&% 炸开多段线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### subtract_line_sets(lines1, lines2, tol)
- 说明: 比较两个线段集合 lines1 和 lines2，返回 lines1 中那些不在 lines2 中的线段。
- 邻近注释: lines1 中那些不在 lines2 中的线段 | &&% 线段集相减
- 参数: lines1, lines2, tol
- 返回: lines1 中所有不与 lines2 中任意线段相同的线段构成的列表。
- 关注点: 几何
- 调用概览: same_line, append
- 理解: 主要用于更新/设置相关逻辑。依据注释：比较两个线段集合 lines1 和 lines2，返回 lines1 中那些不在 lines2 中的线段。。邻近注释提示：lines1 中那些不在 lines2 中的线段；&&% 线段集相减。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### process_final(lines, tol, max_steps, layer_name)
- 说明: （无）
- 邻近注释: (6) | &&% 获取全部封闭多边形 | &&% 最终处理
- 参数: lines, tol, max_steps, layer_name
- 返回推断: tuple
- 关注点: 几何, 日志/测试
- 调用概览: print, process_polygons, info, explode_polylines, subtract_line_sets, extract_polygon_from_lines, draw_polygon_as_polyline, append, len, Delete
- 理解: 主要用于处理相关逻辑。邻近注释提示：(6)；&&% 获取全部封闭多边形；&&% 最终处理。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_lwpolyline(coords3d, layer_name, width, color, closed)
- 说明: 根据一组 (x, y, z) 坐标点绘制轻量级多段线（LWPOLYLINE）。
- 参数: coords3d, layer_name, width, color, closed
- 返回推断: object
- 关注点: COM, 几何, 日志/测试
- 调用概览: alias, VARIANT, Item, extend, AddLightWeightPolyline, bool, info, Add, print
- 理解: 主要用于创建/插入相关逻辑。依据注释：根据一组 (x, y, z) 坐标点绘制轻量级多段线（LWPOLYLINE）。。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### draw_lwpolyline(coords3d, layer_name, width, color, closed)
- 说明: 【通用版】支持在 模型空间 或 任意布局空间 绘制。
- 参数: coords3d, layer_name, width, color, closed
- 返回推断: NoneType,object
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.doc
- 调用概览: alias, VARIANT, Item, extend, AddLightWeightPolyline, bool, Add, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：【通用版】支持在 模型空间 或 任意布局空间 绘制。。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_unique_vertices_from_pl_com(pl_com)
- 说明: 提取多段线的顶点列表，不重复连续线段的公共顶点，返回顶点列表。
- 邻近注释: 1 从com复线获取标准顶点坐标列表 | &&% 获取唯一顶点
- 参数: pl_com
- 返回: 顶点列表，每两个点构成一条线段，格式：[ (x1, y1, z1), (x2, y2, z2), ... ]
- 调用概览: range, append, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：提取多段线的顶点列表，不重复连续线段的公共顶点，返回顶点列表。。邻近注释提示：1 从com复线获取标准顶点坐标列表；&&% 获取唯一顶点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### convert_lines_to_points(segments)
- 说明: 将com线段列表转换为顶点列表，每条线段的两个端点作为一个独立的列表。
- 邻近注释: 2 将com线段转成顶点坐标列表，一根线段一个列表 | &&% 线段转点集
- 参数: segments
- 返回: 包含多个线段顶点的列表，每个线段是一个包含两个端点坐标的列表。
- 关注点: 几何
- 调用概览: tuple, append
- 理解: 主要用于转换/解析相关逻辑。依据注释：将com线段列表转换为顶点列表，每条线段的两个端点作为一个独立的列表。。邻近注释提示：2 将com线段转成顶点坐标列表，一根线段一个列表；&&% 线段转点集。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### merge_segments_new(LB, tol)
- 说明: 使用convert_lines_to_points 将线段实体转成顶点列表表达式后就可以使用此命令
- 邻近注释: 3 合并顶点列表表示的连续线段，允许多根断开的连续线段 | &&% 合并线段
- 参数: LB, tol
- 返回推断: object,tuple
- 调用概览: defaultdict, enumerate, append, len, deque, grow, round, next, list, abs, pop, key...
- 理解: 主要用于创建/插入相关逻辑。依据注释：使用convert_lines_to_points 将线段实体转成顶点列表表达式后就可以使用此命令。邻近注释提示：3 合并顶点列表表示的连续线段，允许多根断开的连续线段；&&% 合并线段。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_polyline(vertices, layer_name, tol, width, color, target_space)
- 说明: 【修正版 V3】绘制轻量多段线 (LWPolyline)
- 参数: vertices, layer_name, tol, width, color, target_space
- 返回推断: NoneType,object
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.doc
- 调用概览: retry_if_busy, getattr, error, same_point, VARIANT, AddLightWeightPolyline, len, extend, tuple, abs
- 理解: 主要用于创建/插入相关逻辑。依据注释：【修正版 V3】绘制轻量多段线 (LWPolyline)。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### lines_to_polylines(Lc, tol, layer_name, width, color)
- 说明: 将直线段合并为多段线 (空间自适应版)
- 邻近注释: 6 将多条直线段（允许不连续）连接成PL复线 | &&% 线段转多段线
- 参数: Lc, tol, layer_name, width, color
- 返回推断: list,object
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.li, C.doc
- 调用概览: info, convert_lines_to_points, merge_segments_new, li, stc, draw_polyline, error, len, append, get_attr, safe_delete, ObjectIDToObject
- 理解: 主要用于处理相关逻辑。依据注释：将直线段合并为多段线 (空间自适应版)。邻近注释提示：6 将多条直线段（允许不连续）连接成PL复线；&&% 线段转多段线。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_min_point(obj)
- 说明: 获取任意对象的左下角坐标（通过其外包盒）。
- 邻近注释: 7 找到多段线的最左下角的点 | &&% 查找最小点
- 参数: obj
- 返回推断: tuple
- 关注点: 日志/测试
- 调用概览: GetBoundingBox, info
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取任意对象的左下角坐标（通过其外包盒）。。邻近注释提示：7 找到多段线的最左下角的点；&&% 查找最小点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### find_max_point(obj)
- 说明: 获取任意对象的右上角坐标（通过其外包盒）。
- 邻近注释: 8 找到多段线的最右上角的点 | &&% 查找最大点
- 参数: obj
- 返回推断: tuple
- 关注点: 日志/测试
- 调用概览: GetBoundingBox, info
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取任意对象的右上角坐标（通过其外包盒）。。邻近注释提示：8 找到多段线的最右上角的点；&&% 查找最大点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### distance(point1, point2)
- 说明: 计算两点之间的距离
- 邻近注释: &&% 计算距离
- 参数: point1, point2
- 返回推断: object
- 关注点: 几何
- 理解: 主要用于计算/测量相关逻辑。依据注释：计算两点之间的距离。邻近注释提示：&&% 计算距离。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### define_rectangle_by_diagonal(p1, p2)
- 说明: 使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。
- 邻近注释: 10 定义矩形 | &&% 定义矩形
- 参数: p1, p2
- 返回推断: tuple
- 关注点: 几何
- 调用概览: abs, max, min
- 理解: 主要用于计算/测量相关逻辑。依据注释：使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。。邻近注释提示：10 定义矩形；&&% 定义矩形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### define_rectangle_by_diagonal_x(p1, p2)
- 说明: 使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。
- 邻近注释: &&% 定义矩形X
- 参数: p1, p2
- 返回推断: object
- 关注点: 几何
- 调用概览: abs, max, min
- 理解: 主要用于计算/测量相关逻辑。依据注释：使用两个对角顶点定义矩形，矩形的边与坐标轴平行或垂直。。邻近注释提示：&&% 定义矩形X。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### expand_rectangle(p1, p2, offset)
- 说明: 给定矩形框的两个对角点（p1 和 p2），
- 参数: p1, p2, offset
- 返回推断: tuple
- 关注点: 几何
- 调用概览: sorted
- 理解: 主要用于计算/测量相关逻辑。依据注释：给定矩形框的两个对角点（p1 和 p2），。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### parse_rectangle_points(*args)
- 说明: 接收多种坐标格式输入，统一解析为矩形四角点：
- 参数: *args
- 返回: (左下, 右上, 左上, 右下)，每个为三元组 (x, y, z)
- 关注点: 几何, 日志/测试
- 调用概览: min, max, isinstance, all, info, len, ValueError
- 理解: 主要用于转换/解析相关逻辑。依据注释：接收多种坐标格式输入，统一解析为矩形四角点：。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_rectangular_polylines(min_side, area_tolerance)
- 说明: 【智能筛选】获取所有“矩形”多段线 (兼容轻量线和老式线)。
- 邻近注释: &&&% 模型空间选出矩形多段线
- 参数: min_side, area_tolerance
- 返回: List[COMObject]: 筛选出的矩形多段线列表
- 关注点: 几何, 日志/测试, 选择集
- 调用概览: info, select_polyline, extend, select_polyline_chuantong, GetBoundingBox, abs, len, get_obj_loc, getattr, append, max, min
- 理解: 主要用于获取/选择相关逻辑。依据注释：【智能筛选】获取所有“矩形”多段线 (兼容轻量线和老式线)。。邻近注释提示：&&&% 模型空间选出矩形多段线。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### get_layout_rectangular_polylines_coords(layout_name, min_side)
- 说明: 【早期绑定专用】基于 get_attr 的矩形分析 (已集成 sys_logger)
- 邻近注释: continue | sys_logger.info(f"\n✅ [扫描结束] 最终找到 {len(results)} 个矩形") | return results
- 参数: layout_name, min_side
- 返回推断: list,object
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.doc
- 调用概览: info, enumerate, Item, error, get_attr, list, len, min, max, append, warning, str...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【早期绑定专用】基于 get_attr 的矩形分析 (已集成 sys_logger)。邻近注释提示：continue；sys_logger.info(f"\n✅ [扫描结束] 最终找到 {len(results)} 个矩形")；return results。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### generate_name_and_ratio_from_com(comobj, A3dy, Fandy, tol)
- 说明: 【V5.0 强制兜底版】
- 邻近注释: &&&%  分析打印线20260110
- 参数: comobj, A3dy, Fandy, tol
- 返回推断: int,tuple
- 关注点: 日志/测试
- 调用概览: float, enumerate, getattr, GetBoundingBox, abs, max, min
- 理解: 主要用于处理相关逻辑。依据注释：【V5.0 强制兜底版】。邻近注释提示：&&&%  分析打印线20260110。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_cad_app()
- 说明: 连接 CAD
- 邻近注释: &&% 打印数据分析
- 参数: （无）
- 返回推断: NoneType,object
- 关注点: COM, 进程
- 调用概览: GetActiveObject, print
- 理解: 主要用于获取/选择相关逻辑。依据注释：连接 CAD。邻近注释提示：&&% 打印数据分析。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_dimensions(ent)
- 说明: 获取实体长宽（长边在前）
- 参数: ent
- 返回推断: tuple
- 调用概览: GetBoundingBox, abs, max, min
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取实体长宽（长边在前）。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_llcorner(com_list, cha_Y)
- 说明: 按 BoundingBox 左下角坐标排序：
- 参数: com_list, cha_Y
- 返回推断: object
- 调用概览: sort, append, len, GetBoundingBox, sorted, float, abs
- 理解: 主要用于处理相关逻辑。依据注释：按 BoundingBox 左下角坐标排序：。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### main()
- 说明: （无）
- 参数: （无）
- 返回推断: None
- 关注点: COM, 日志/测试, 选择集
- 调用概览: get_cad_app, print, Add, sort_coms_by_llcorner, info, enumerate, Delete, SelectOnScreen, Item, get_dimensions, rstrip, range...
- 理解: 主要用于处理相关逻辑。实现特征：涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### generate_relation_list(data_list)
- 说明: （无）
- 参数: data_list
- 返回推断: object
- 调用概览: enumerate, float, append, abs, min
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### check_strict_standard_size(comobj, tol)
- 说明: 【函数编号】: MAP-CHECK-SIZE-004
- 邻近注释: &&&% 选择标准打印区域
- 参数: comobj, tol
- 返回推断: int,object
- 关注点: 几何, 日志/测试
- 调用概览: enumerate, find_min_point, find_max_point, define_rectangle_by_diagonal, abs, info
- 理解: 主要用于测试/校验相关逻辑。依据注释：【函数编号】: MAP-CHECK-SIZE-004。邻近注释提示：&&&% 选择标准打印区域。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### check_strict_standard_size(comobj, tol)
- 说明: 【修正版 V5.0】
- 参数: comobj, tol
- 返回推断: int,tuple
- 调用概览: enumerate, GetBoundingBox, abs, max, min, float, split
- 理解: 主要用于测试/校验相关逻辑。依据注释：【修正版 V5.0】。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### polyline_sort(polyline_list)
- 说明: 对com多段线按照特定规则进行排序
- 邻近注释: &&% 多段线排序
- 参数: polyline_list
- 返回推断: object
- 关注点: 几何
- 调用概览: sort, find_min_point, len, sorted, abs
- 理解: 主要用于处理相关逻辑。依据注释：对com多段线按照特定规则进行排序。邻近注释提示：&&% 多段线排序。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### plcom_to_coor(plines)
- 说明: 接受多根轻量级多段线或常规多段线的 COM 对象列表，返回它们的坐标列表及闭合状态。
- 邻近注释: &&&%  *** 3 将PLcom线列表的坐标信息存储 | &&% 多段线转坐标
- 参数: plines
- 返回推断: object
- 关注点: COM, 日志/测试
- 调用概览: ensure_list, list, append, range, getattr, len, info
- 理解: 主要用于处理相关逻辑。依据注释：接受多根轻量级多段线或常规多段线的 COM 对象列表，返回它们的坐标列表及闭合状态。。邻近注释提示：&&&%  *** 3 将PLcom线列表的坐标信息存储；&&% 多段线转坐标。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### plcoor_to_com(coord_info, layer_name, width, color)
- 说明: 在当前 DWG 中根据坐标和封闭标志绘制多条轻量级多段线。
- 邻近注释: 4 从坐标信息列表返回PLcom线列表 | &&% 坐标转多段线
- 参数: coord_info, layer_name, width, color
- 返回推断: object
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, ZoomExtents, info, Item, VARIANT, AddLightWeightPolyline, bool, append, Add, extend, len
- 理解: 主要用于处理相关逻辑。依据注释：在当前 DWG 中根据坐标和封闭标志绘制多条轻量级多段线。。邻近注释提示：4 从坐标信息列表返回PLcom线列表；&&% 坐标转多段线。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### panduan_shuxiangkuang(polyline)
- 说明: （无）
- 邻近注释: 5 确定多段线打印框是否竖向 | &&% 判断竖向框
- 参数: polyline
- 返回推断: bool
- 关注点: 几何
- 调用概览: find_min_point, find_max_point, abs
- 理解: 主要用于处理相关逻辑。邻近注释提示：5 确定多段线打印框是否竖向；&&% 判断竖向框。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### tongyi_tufu(LB, TFname)
- 说明: 将打印线列表的每根线对应的图纸尺寸统一为一个TFname
- 邻近注释: 6 统一为A2的图幅打印 | &&% 统一图幅
- 参数: LB, TFname
- 返回推断: object
- 调用概览: append
- 理解: 主要用于处理相关逻辑。依据注释：将打印线列表的每根线对应的图纸尺寸统一为一个TFname。邻近注释提示：6 统一为A2的图幅打印；&&% 统一图幅。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### simplify_polygon(poly, tol)
- 说明: 简化多边形顶点列表：如果某顶点 P 与其前后两点共线（在容差 tol 范围内），则将其移除。
- 邻近注释: 消除多边形的伪边点 | &&% 简化多边形
- 参数: poly, tol
- 返回: 简化后的顶点列表（同样保留首尾是否闭合的形式，不会自动去重首尾）
- 关注点: 几何
- 调用概览: len, range, abs, is_colinear
- 理解: 主要用于处理相关逻辑。依据注释：简化多边形顶点列表：如果某顶点 P 与其前后两点共线（在容差 tol 范围内），则将其移除。。邻近注释提示：消除多边形的伪边点；&&% 简化多边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### normalize_polygon(polygon)
- 说明: 标准化多边形顶点列表：  
- 邻近注释: 1. 标准化多边形顶点列表，去掉相邻和首尾重复点 | &&% 标准化多边形
- 参数: polygon
- 返回: 去重后的顶点列表
- 关注点: 几何
- 调用概览: pop, append, len
- 理解: 主要用于处理相关逻辑。依据注释：标准化多边形顶点列表：  。邻近注释提示：1. 标准化多边形顶点列表，去掉相邻和首尾重复点；&&% 标准化多边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_adjacent_points(polygon, p)
- 说明: 在多边形 polygon 中返回顶点 p 的前后相邻点（支持循环）。
- 邻近注释: 2. 找到某顶点的前驱/后继（按循环多边形） | &&% 获取相邻点
- 参数: polygon, p
- 返回推断: tuple
- 关注点: 几何
- 调用概览: normalize_polygon, ValueError, index, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：在多边形 polygon 中返回顶点 p 的前后相邻点（支持循环）。。邻近注释提示：2. 找到某顶点的前驱/后继（按循环多边形）；&&% 获取相邻点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### point_in_polygon(pt, polygon)
- 说明: 判断三维点 pt=(x,y,z) 在多边形 polygon 的 XY 投影内否。
- 邻近注释: 3. 点是否在多边形内部（射线法，仅在 XY 平面判断） | &&% 点在多边形内
- 参数: pt, polygon
- 返回推断: object
- 关注点: 几何
- 调用概览: len, range, normalize_polygon
- 理解: 主要用于处理相关逻辑。依据注释：判断三维点 pt=(x,y,z) 在多边形 polygon 的 XY 投影内否。。邻近注释提示：3. 点是否在多边形内部（射线法，仅在 XY 平面判断）；&&% 点在多边形内。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### line_segment_intersection_2d(p, d, a, b, tol)
- 说明: 计算射线 L(t)=p + t·d 与线段 AB 在 XY 平面上的交点。
- 邻近注释: 4. 无穷直线 vs 线段在 XY 平面相交 | &&% 线段相交
- 参数: p, d, a, b, tol
- 返回推断: NoneType,tuple
- 调用概览: abs
- 理解: 主要用于处理相关逻辑。依据注释：计算射线 L(t)=p + t·d 与线段 AB 在 XY 平面上的交点。。邻近注释提示：4. 无穷直线 vs 线段在 XY 平面相交；&&% 线段相交。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_auxiliary_point(p, p_prev, p_next, polygon, tol)
- 说明: 对于多边形顶点 p 及其前后相邻点 p_prev, p_next，
- 邻近注释: 5. 计算 p 和其相邻点中点 c，如果 c 内部则返回 c，否则沿 p->c 的射线找到第一个交点 | &&% 获取辅助点
- 参数: p, p_prev, p_next, polygon, tol
- 返回推断: object,tuple
- 关注点: 几何
- 调用概览: point_in_polygon, hypot, normalize_polygon, range, sort, RuntimeError, len, line_segment_intersection_2d, abs, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：对于多边形顶点 p 及其前后相邻点 p_prev, p_next，。邻近注释提示：5. 计算 p 和其相邻点中点 c，如果 c 内部则返回 c，否则沿 p->c 的射线找到第一个交点；&&% 获取辅助点。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### concavity_measure(p, p_prev, p_next, q)
- 说明: 给定 p, p_prev, p_next, q（均为 (x,y,z)），
- 邻近注释: 6. 计算 p 点的“凹凸度量角” | &&% 凹凸度量
- 参数: p, p_prev, p_next, q
- 返回推断: object
- 关注点: 几何
- 调用概览: angle_of, degrees, atan2
- 理解: 主要用于计算/测量相关逻辑。依据注释：给定 p, p_prev, p_next, q（均为 (x,y,z)），。邻近注释提示：6. 计算 p 点的“凹凸度量角”；&&% 凹凸度量。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### concavity_angle(p, polygon)
- 说明: 直接计算多边形 polygon 上顶点 p 的凹凸度量角。
- 邻近注释: 7. 直接给出 p 在多边形上的度量角 | &&% 凹凸角
- 参数: p, polygon
- 返回推断: object
- 关注点: 几何
- 调用概览: get_adjacent_points, get_auxiliary_point, concavity_measure
- 理解: 主要用于计算/测量相关逻辑。依据注释：直接计算多边形 polygon 上顶点 p 的凹凸度量角。。邻近注释提示：7. 直接给出 p 在多边形上的度量角；&&% 凹凸角。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### split_orthogonal_hexagon(polygon, tol)
- 说明: 将正交六边形 polygon 按凹顶点所在水平线切成两个矩形。
- 邻近注释: 8.合理分割PL正交六边形 | &&% 水平分割六边形
- 参数: polygon, tol
- 返回推断: object
- 关注点: 几何
- 调用概览: normalize_polygon, len, range, index, ValueError, RuntimeError, append, area2d, abs, concavity_angle
- 理解: 主要用于处理相关逻辑。依据注释：将正交六边形 polygon 按凹顶点所在水平线切成两个矩形。。邻近注释提示：8.合理分割PL正交六边形；&&% 水平分割六边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### split_orthogonal_hexagon_vertical(polygon, tol)
- 说明: 将正交六边形 polygon 按凹顶点所在竖线切成两个矩形。
- 邻近注释: &&% 竖向分割六边形
- 参数: polygon, tol
- 返回: (rect1, rect2)，面积小的放前面。
- 关注点: 几何
- 调用概览: normalize_polygon, len, range, index, ValueError, RuntimeError, append, area2d, abs, concavity_angle
- 理解: 主要用于处理相关逻辑。依据注释：将正交六边形 polygon 按凹顶点所在竖线切成两个矩形。。邻近注释提示：&&% 竖向分割六边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### area_of(verts)
- 说明: 多边形面积计算（顶点首尾闭合或不闭合均可）
- 邻近注释: 合理分割PL正交六边形 | &&% 计算面积
- 参数: verts
- 返回推断: object
- 调用概览: len, range, abs
- 理解: 主要用于计算/测量相关逻辑。依据注释：多边形面积计算（顶点首尾闭合或不闭合均可）。邻近注释提示：合理分割PL正交六边形；&&% 计算面积。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### split_hexagon_combined(polygon, tol, simplify_tol)
- 说明: 合理分割一个正交（近似）六边形 PL：
- 邻近注释: &&% 综合分割六边形
- 参数: polygon, tol, simplify_tol
- 返回: 四个矩形的顶点列表：最小矩形、其同组矩形、次小矩形、其同组矩形
- 关注点: 几何
- 调用概览: simplify_polygon, split_orthogonal_hexagon, split_orthogonal_hexagon_vertical, isinstance, get_unique_vertices_from_pl_com, area_of
- 理解: 主要用于处理相关逻辑。依据注释：合理分割一个正交（近似）六边形 PL：。邻近注释提示：&&% 综合分割六边形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_bbox_edge_segments(pl, tol)
- 说明: 获取对象 pl 的包围盒四条边，分别作为独立的列表返回：
- 邻近注释: 获取多段线的上下左右边界的直线段，返回线段端点列表 | 该函数系列包括如下一些函数 | &&% 获取包围盒边
- 参数: pl, tol
- 返回: top    = [(xmin, ymax, z), (xmax, ymax, z)]
- 关注点: COM, 几何, 日志/测试
- 调用概览: info, print, enumerate, GetBoundingBox, VARIANT, tuple
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取对象 pl 的包围盒四条边，分别作为独立的列表返回：。邻近注释提示：获取多段线的上下左右边界的直线段，返回线段端点列表；该函数系列包括如下一些函数；&&% 获取包围盒边。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_texts_in_polyline(com_pl, tol)
- 说明: 在多段线 com_pl 内部筛选文字，并返回文字对象列表和对应的文字内容列表。
- 邻近注释: &&%  获取多段线的内部的文字 | 该函数系列包括如下一些函数 | &&% 获取多段线内文字
- 参数: com_pl, tol
- 返回: inside:   落在 com_pl 内部的文字 COM 对象列表
- 关注点: 几何, 日志/测试
- 调用概览: get_unique_vertices_from_pl_com, collect_all_texts, info, GetBoundingBox, point_in_polygon, append, getattr, len, TDbMText_content
- 理解: 主要用于获取/选择相关逻辑。依据注释：在多段线 com_pl 内部筛选文字，并返回文字对象列表和对应的文字内容列表。。邻近注释提示：&&%  获取多段线的内部的文字；该函数系列包括如下一些函数；&&% 获取多段线内文字。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### TDbMText_content(comobj, separator)
- 说明: 【函数】获取天正多行文字内容（副本炸开版，支持换行识别）
- 邻近注释: 获取单独一行的天正多行文字内容 | &&% 获取天正多行文字
- 参数: comobj, separator
- 返回推断: object,str,tuple
- 关注点: 几何, 文件, 日志/测试
- 调用概览: li, explode_single_object_marker, sort, enumerate, Copy, get_attr, round, get_sort_info, info, GetBoundingBox, Delete
- 理解: 主要用于处理相关逻辑。依据注释：【函数】获取天正多行文字内容（副本炸开版，支持换行识别）。邻近注释提示：获取单独一行的天正多行文字内容；&&% 获取天正多行文字。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### distribute_points_on_entity(entity, n, block, scale_factor, ys)
- 说明: （无）
- 邻近注释: &&% 实体均分点
- 参数: entity, n, block, scale_factor, ys
- 返回推断: object
- 关注点: COM, 几何
- 调用概览: sqrt, range, InsertBlock, vtpnt, sum, cos, sin, distance, len
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 实体均分点。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### is_segment_contained(seg_a, seg_b, tol)
- 说明: 判断 seg_a 是否完全位于 seg_b 上（包含端点）。
- 邻近注释: 该函数系列包括如下一些函数 | 1 判断一条直线是否完全在另一条直线上 | &&% 判断线段包含
- 参数: seg_a, seg_b, tol
- 返回推断: bool,object,tuple
- 关注点: 几何
- 调用概览: get_endpoints, dot, proj_param, hasattr, hypot, abs, colinear, tuple
- 理解: 主要用于处理相关逻辑。依据注释：判断 seg_a 是否完全位于 seg_b 上（包含端点）。。邻近注释提示：该函数系列包括如下一些函数；1 判断一条直线是否完全在另一条直线上；&&% 判断线段包含。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### common_segments_between_polylines(pl1, pl2, tol)
- 说明: 返回 pl1 中与 pl2 “共线且有重叠”的区段列表，每个区段用
- 邻近注释: &&% 2 返回 PL线pl1 中与 pl2 “共线且有重叠”的区段列表 | &&% 公共线段
- 参数: pl1, pl2, tol
- 返回推断: NoneType,object,tuple
- 关注点: 几何, 日志/测试
- 调用概览: coords_to_xy_pairs, build_segments, print, enumerate, range, hypot, interp, getattr, append, len, info, abs...
- 理解: 主要用于处理相关逻辑。依据注释：返回 pl1 中与 pl2 “共线且有重叠”的区段列表，每个区段用。邻近注释提示：&&% 2 返回 PL线pl1 中与 pl2 “共线且有重叠”的区段列表；&&% 公共线段。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### is_rect_inside_rect(rect_outer, rect_inner, tol)
- 说明: 判定 axis‑aligned 的矩形 rect_inner 是否被（含边界）完全包在 rect_outer 内。
- 邻近注释: 1 判断矩形是否包含另一个矩形 | &&% 矩形包含判断
- 参数: rect_outer, rect_inner, tol
- 返回推断: object
- 理解: 主要用于处理相关逻辑。依据注释：判定 axis‑aligned 的矩形 rect_inner 是否被（含边界）完全包在 rect_outer 内。。邻近注释提示：1 判断矩形是否包含另一个矩形；&&% 矩形包含判断。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### two_plines_making_rectangle(pl1, pl2, tol)
- 说明: 判断两条正交多段线拼在一起后是否正好是一个矩形。
- 邻近注释: 2 判断两条正交多段线拼在一起后是否正好是一个矩形 | &&% 两多段线组矩形
- 参数: pl1, pl2, tol
- 返回推断: bool,object
- 关注点: 几何
- 调用概览: pline_vertices, poly_area, range, hypot, sort, min, max, abs, collect_segments, covers_edge, len, append...
- 理解: 主要用于计算/测量相关逻辑。依据注释：判断两条正交多段线拼在一起后是否正好是一个矩形。。邻近注释提示：2 判断两条正交多段线拼在一起后是否正好是一个矩形；&&% 两多段线组矩形。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### are_all_vertices_inside(pl1, pl2)
- 说明: 判断多段线 pl2 的所有顶点是否都在多段线 pl1 构成的多边形内部。
- 邻近注释: 判断多段线PL2是否在多段线PL1多边形中 | 该函数系列包括如下一些函数 | &&% 顶点全在内部
- 参数: pl1, pl2
- 返回: (all_inside, outside_pts)
- 关注点: 几何, 日志/测试
- 调用概览: get_unique_vertices_from_pl_com, len, print, info, point_in_polygon, append
- 理解: 主要用于处理相关逻辑。依据注释：判断多段线 pl2 的所有顶点是否都在多段线 pl1 构成的多边形内部。。邻近注释提示：判断多段线PL2是否在多段线PL1多边形中；该函数系列包括如下一些函数；&&% 顶点全在内部。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ensure_list(input_data)
- 说明: 【通用工具】将输入参数统一转换为列表。
- 邻近注释: &&&&%% 第四部分 一般对象
- 参数: input_data
- 返回推断: bool,list,object
- 关注点: 选择集
- 调用概览: is_list_like, isinstance, hasattr, list, len, ensure_list
- 理解: 主要用于获取/选择相关逻辑。依据注释：【通用工具】将输入参数统一转换为列表。。邻近注释提示：&&&&%% 第四部分 一般对象。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### sort_tuples(lst, cha_Y)
- 说明: 这是很有用的一个双值排序函数，对于COM对象，可以先将其转换为元组，即可使用这个函数
- 邻近注释: 按com实体对象中提取的坐标排序 | &&&%  排序 | &&% 元组排序
- 参数: lst, cha_Y
- 返回推断: object
- 调用概览: sort, len, sorted, abs
- 理解: 主要用于处理相关逻辑。依据注释：这是很有用的一个双值排序函数，对于COM对象，可以先将其转换为元组，即可使用这个函数。邻近注释提示：按com实体对象中提取的坐标排序；&&&%  排序；&&% 元组排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### multi_dim_tolerance_sort(lst, key_index, tolerances)
- 说明: 对 lst 列表中的元组按多维坐标字段排序，考虑每个维度的容差进行逐层排序。
- 邻近注释: &&% 多维容差排序
- 参数: lst, key_index, tolerances
- 返回: 排好序的新列表
- 调用概览: len, sort, recursive_sort, sorted, abs
- 理解: 主要用于处理相关逻辑。依据注释：对 lst 列表中的元组按多维坐标字段排序，考虑每个维度的容差进行逐层排序。。邻近注释提示：&&% 多维容差排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_ll_pt(ent)
- 说明: （无）
- 参数: ent
- 返回推断: tuple
- 调用概览: GetBoundingBox
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_center(ent)
- 说明: （无）
- 参数: ent
- 返回推断: tuple
- 调用概览: GetBoundingBox
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_entities_by_position(entity_list, extract_func, cha_Y)
- 说明: 对实体列表根据其坐标（通过 extract_func 获取）进行排序：
- 邻近注释: &&% 实体位置排序
- 参数: entity_list, extract_func, cha_Y
- 返回: 按坐标顺序排列的新实体对象列表
- 调用概览: sort, sorted, len, extract_func, abs
- 理解: 主要用于处理相关逻辑。依据注释：对实体列表根据其坐标（通过 extract_func 获取）进行排序：。邻近注释提示：&&% 实体位置排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_line_start(ent)
- 说明: 提取一条直线的起点 (x, y)
- 参数: ent
- 返回推断: tuple
- 关注点: 几何
- 理解: 主要用于获取/选择相关逻辑。依据注释：提取一条直线的起点 (x, y)。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_llcorner(com_list, cha_Y)
- 说明: 按 BoundingBox 左下角坐标排序：
- 邻近注释: &&% * 对列表实体进行从上到下、从左到右的排序 | &&% 左下角排序
- 参数: com_list, cha_Y
- 返回推断: object
- 调用概览: sort, append, GetBoundingBox, len, sorted, float, abs
- 理解: 主要用于处理相关逻辑。依据注释：按 BoundingBox 左下角坐标排序：。邻近注释提示：&&% * 对列表实体进行从上到下、从左到右的排序；&&% 左下角排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_rbcorner(com_list)
- 说明: 竖向图框（或已整体旋转 -90° 的图纸）使用 ——  
- 邻近注释: &&% 右上角排序
- 参数: com_list
- 返回推断: object
- 调用概览: sort, append, sorted, GetBoundingBox, len, float, abs
- 理解: 主要用于处理相关逻辑。依据注释：竖向图框（或已整体旋转 -90° 的图纸）使用 ——  。邻近注释提示：&&% 右上角排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_llcorner_custom(objs, tol_x)
- 说明: 按左下角 x, y 坐标对 COM 对象列表 objs 排序：
- 邻近注释: &&% 自定义左下角排序
- 参数: objs, tol_x
- 返回推断: object
- 调用概览: sort, append, sorted, GetBoundingBox, extend, abs
- 理解: 主要用于处理相关逻辑。依据注释：按左下角 x, y 坐标对 COM 对象列表 objs 排序：。邻近注释提示：&&% 自定义左下角排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_center(objs, tol_x)
- 说明: 按外包盒中心坐标对 COM 对象列表 objs 排序：
- 邻近注释: &&% 中心点排序
- 参数: objs, tol_x
- 返回推断: list,object
- 关注点: 几何
- 调用概览: sort, append, sorted, GetBoundingBox, extend, abs
- 理解: 主要用于处理相关逻辑。依据注释：按外包盒中心坐标对 COM 对象列表 objs 排序：。邻近注释提示：&&% 中心点排序。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### number_entities_by_order(entity_list, prefix, start, k)
- 说明: 对排序好的 COM 实体对象列表进行编号。
- 邻近注释: 对列表实体进行正序或逆序编号 | &&% 实体编号
- 参数: entity_list, prefix, start, k
- 返回: 编号字符串列表（如 ["1", "2", "3"] 或 ["图1", "图2", "图3"]）
- 调用概览: len, enumerate, range, reversed, append
- 理解: 主要用于处理相关逻辑。依据注释：对排序好的 COM 实体对象列表进行编号。。邻近注释提示：对列表实体进行正序或逆序编号；&&% 实体编号。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### pr_list(P, f, *args, **kwargs)
- 说明: args:  位置参数元组 (例如: 10, 20)
- 邻近注释: 重复操作列表对象 | &&% 列表遍历操作
- 参数: P, f, *args, **kwargs
- 返回推断: object
- 关注点: 日志/测试
- 调用概览: info, enumerate, f, append, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：args:  位置参数元组 (例如: 10, 20)。邻近注释提示：重复操作列表对象；&&% 列表遍历操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### apply_to_each2(obj_list, extract_func, action_func)
- 说明: 对 obj_list 中的每个对象，先通过 extract_func 提取值，
- 邻近注释: &&% 列表提取操作
- 参数: obj_list, extract_func, action_func
- 调用概览: extract_func, action_func
- 理解: 主要用于处理相关逻辑。依据注释：对 obj_list 中的每个对象，先通过 extract_func 提取值，。邻近注释提示：&&% 列表提取操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_boundingbox_from_objects(objs)
- 说明: 从一组图形对象（如 LB）中获取整体包围盒
- 邻近注释: 建立全部列表com对象的最小边界框 | &&% 获取对象群包围盒
- 参数: objs
- 返回推断: tuple
- 关注点: 几何, 日志/测试
- 调用概览: tuple, GetBoundingBox, info, list, min, max, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：从一组图形对象（如 LB）中获取整体包围盒。邻近注释提示：建立全部列表com对象的最小边界框；&&% 获取对象群包围盒。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### chuangjian_zu(group_name)
- 说明: （无）
- 邻近注释: 建立组的最小边界框 | &&% 创建组
- 参数: group_name
- 返回推断: object
- 调用概览: Add
- 理解: 主要用于处理相关逻辑。邻近注释提示：建立组的最小边界框；&&% 创建组。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### nametogroup(group_name)
- 说明: （无）
- 邻近注释: &&% 获取组对象
- 参数: group_name
- 返回推断: object
- 调用概览: Item
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 获取组对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_all_group_names()
- 说明: 获取当前 DWG 文档中所有组的名称列表。
- 邻近注释: 获取所有组 | &&% 获取所有组名
- 参数: （无）
- 返回: List[str] — 包含所有组名称的列表
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, Item, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取当前 DWG 文档中所有组的名称列表。。邻近注释提示：获取所有组；&&% 获取所有组名。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_all_groups()
- 说明: 获取当前 DWG 文档中所有组的 COM 对象列表及其名称。
- 邻近注释: &&% 获取所有组
- 参数: （无）
- 返回: List[Tuple[str, COMObject]] — 每项为 (组名称, 组对象)
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, range, Item, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取当前 DWG 文档中所有组的 COM 对象列表及其名称。。邻近注释提示：&&% 获取所有组。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### add_objects_to_group(group_name, obj_list)
- 说明: 将 obj_list 中的所有图形对象加入名为 group_name 的组中
- 邻近注释: 将多个com对象对象加入名为group_name的组 | &&% 添加对象到组
- 参数: group_name, obj_list
- 返回: Group 对象
- 调用概览: AppendItems, Item, vtlist, Add
- 理解: 主要用于创建/插入相关逻辑。依据注释：将 obj_list 中的所有图形对象加入名为 group_name 的组中。邻近注释提示：将多个com对象对象加入名为group_name的组；&&% 添加对象到组。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### add_object_to_group(group_name, obj)
- 说明: 将单个图形对象 obj 加入名为 group_name 的组中。
- 邻近注释: 将单独com对象对象加入名为group_name的组中 | &&% 添加单对象到组
- 参数: group_name, obj
- 返回: COM Group 对象
- 调用概览: AppendItems, Item, vtlist, Add
- 理解: 主要用于创建/插入相关逻辑。依据注释：将单个图形对象 obj 加入名为 group_name 的组中。。邻近注释提示：将单独com对象对象加入名为group_name的组中；&&% 添加单对象到组。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### remove_object_from_group(group_name, obj)
- 说明: 将单个 COM 对象 obj 从名为 group_name 的组中移出。
- 邻近注释: 将单独com对象对象移出名为group_name的组 | &&% 移除组内对象
- 参数: group_name, obj
- 返回: 如果组存在，返回该 Group 对象；否则返回 None。
- 关注点: COM, 文件, 日志/测试
- 调用概览: VARIANT, Item, RemoveItems, info
- 理解: 主要用于删除/清理相关逻辑。依据注释：将单个 COM 对象 obj 从名为 group_name 的组中移出。。邻近注释提示：将单独com对象对象移出名为group_name的组；&&% 移除组内对象。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### remove_objects_from_group(group_name, obj_list)
- 说明: 将 obj_list 中的所有图形对象从名为 group_name 的组中移出。
- 邻近注释: 将多个com对象对象移出名为group_name的组 | &&% 批量移除组内对象
- 参数: group_name, obj_list
- 返回推断: NoneType,object
- 关注点: COM, 文件, 日志/测试
- 调用概览: VARIANT, Item, RemoveItems, info, len
- 理解: 主要用于删除/清理相关逻辑。依据注释：将 obj_list 中的所有图形对象从名为 group_name 的组中移出。。邻近注释提示：将多个com对象对象移出名为group_name的组；&&% 批量移除组内对象。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### get_com_from_groupname(group_name)
- 说明: 根据组名获取对应实体列表。
- 邻近注释: &&% 从名为group_name的组获取内部包含的实体对象 | &&% 获取组内实体
- 参数: group_name
- 返回推断: list,object
- 调用概览: nametogroup, Item, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：根据组名获取对应实体列表。。邻近注释提示：&&% 从名为group_name的组获取内部包含的实体对象；&&% 获取组内实体。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_com_from_groupname_by_type(group_name)
- 说明: 根据组名获取对应实体，并按类型名分类返回。
- 邻近注释: 从名为group_name的组返回按类型分类的字典 | &&% 获取组内实体分类
- 参数: group_name
- 返回推断: dict,object
- 关注点: 日志/测试
- 调用概览: nametogroup, range, items, info, Item, append, getattr, setdefault, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：根据组名获取对应实体，并按类型名分类返回。。邻近注释提示：从名为group_name的组返回按类型分类的字典；&&% 获取组内实体分类。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_group_entities_sorted(group_name, type_extractors, cha_Y)
- 说明: 从组中按类型获取实体，并对指定类型按坐标排序。
- 邻近注释: 从名为group_name的组返回按类型分类的字典，且类型按各自位置提取函数排好序 | &&% 获取组内实体排序
- 参数: group_name, type_extractors, cha_Y
- 返回推断: object,tuple
- 关注点: 几何, 日志/测试
- 调用概览: get_com_from_groupname_by_type, items, float, sort_entities_by_position, info, list, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：从组中按类型获取实体，并对指定类型按坐标排序。。邻近注释提示：从名为group_name的组返回按类型分类的字典，且类型按各自位置提取函数排好序；&&% 获取组内实体排序。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_group_entities_sorted_by_type_and_bbox(group_name, cha_Y)
- 说明: 将组 group_name 中的实体按类型分类，并对每种类型内部按包围盒中心排序：
- 邻近注释: 从名为group_name的组返回按类型分类的字典，各类型统一按boundingbox中心排好序 | &&% 组内实体按中心排序
- 参数: group_name, cha_Y
- 返回: 一个 dict，key=类型名(ObjectName)，value=排序后的实体列表
- 关注点: 几何
- 调用概览: nametogroup, items, Item, append, sort, range, getattr, sorted, setdefault, len, bbox_center_2, abs
- 理解: 主要用于获取/选择相关逻辑。依据注释：将组 group_name 中的实体按类型分类，并对每种类型内部按包围盒中心排序：。邻近注释提示：从名为group_name的组返回按类型分类的字典，各类型统一按boundingbox中心排好序；&&% 组内实体按中心排序。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### common_group_entities_sorted(group_name1, group_name2, cha_Y)
- 说明: 获取两个组中共有的实体，按类型分类并按包围盒中心排序。
- 邻近注释: 获取两个组中共有的实体，按类型分类并按包围盒中心排序 | &&% 共有组实体排序
- 参数: group_name1, group_name2, cha_Y
- 返回: dict => key: ObjectName 类型名, value: 排序后的实体列表
- 关注点: COM, 几何
- 调用概览: nametogroup, items, Item, set, append, GetBoundingBox, tuple, sort, range, keys, getattr, sorted...
- 理解: 主要用于处理相关逻辑。依据注释：获取两个组中共有的实体，按类型分类并按包围盒中心排序。。邻近注释提示：获取两个组中共有的实体，按类型分类并按包围盒中心排序；&&% 共有组实体排序。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_boundingbox_from_group(group)
- 说明: 并非组的实际BoundingBOX数据
- 邻近注释: &&% 获取组包围盒
- 参数: group
- 返回推断: tuple
- 关注点: 几何
- 调用概览: get_boundingbox_from_objects, Item, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：并非组的实际BoundingBOX数据。邻近注释提示：&&% 获取组包围盒。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### copy_group_S1_from_doc1_to_doc2(doc1, doc2, group_name)
- 说明: 将 doc1 中名为 group_name 的组复制到 doc2 中，并重新组装组。
- 邻近注释: &&% 复制组S1
- 参数: doc1, doc2, group_name
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 调用概览: set_active_doc, li, Item, yin_to_xian_xuanze, SendCommand, sleep, get_handle_object_map, info, add_objects_to_group, set, chr, len
- 理解: 主要用于移动/复制相关逻辑。依据注释：将 doc1 中名为 group_name 的组复制到 doc2 中，并重新组装组。。邻近注释提示：&&% 复制组S1。实现特征：通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### HandleToObject(ZF)
- 说明: 对连接在墙上的门窗测试无效
- 邻近注释: &&% 句柄转对象
- 参数: ZF
- 返回推断: object
- 关注点: COM
- 调用概览: alias, HandleToObject
- 理解: 主要用于处理相关逻辑。依据注释：对连接在墙上的门窗测试无效。邻近注释提示：&&% 句柄转对象。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### print_coms_handle(LB)
- 说明: （无）
- 参数: LB
- 关注点: COM, 日志/测试
- 调用概览: info, append
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### handles_to_coms(LB_handles)
- 说明: 对连接在墙上的门窗测试无效
- 邻近注释: &&% 批量句柄转对象
- 参数: LB_handles
- 返回推断: object
- 关注点: COM
- 调用概览: alias, HandleToObject, append
- 理解: 主要用于处理相关逻辑。依据注释：对连接在墙上的门窗测试无效。邻近注释提示：&&% 批量句柄转对象。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_all_handles()
- 说明: 获取当前图纸中所有对象（通常在 ModelSpace）的 Handle 值列表。
- 邻近注释: &&% 获取所有句柄
- 参数: （无）
- 返回: handle_list: 所有图元的 Handle 字符串列表
- 关注点: COM, 日志/测试
- 调用概览: info, append, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取当前图纸中所有对象（通常在 ModelSpace）的 Handle 值列表。。邻近注释提示：&&% 获取所有句柄。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### find_entity_by_handle(handle_str)
- 说明: 遍历当前图纸所有对象，手动比对 Handle 值，找到指定的实体对象。
- 邻近注释: &&% 查找实体
- 参数: handle_str
- 返回: 对象（若找到），否则 None
- 关注点: COM
- 理解: 主要用于获取/选择相关逻辑。依据注释：遍历当前图纸所有对象，手动比对 Handle 值，找到指定的实体对象。。邻近注释提示：&&% 查找实体。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### group_objects_by_type_and_handle(LB)
- 说明: 将com对象列表 LB 中的对象按 ObjectName 分类，并存储其 Handle。
- 邻近注释: &&% 按类型句柄分组
- 参数: LB
- 返回: ZD - dict 格式 {ObjectName: [Handle1, Handle2, ...]}
- 关注点: COM, 日志/测试, 选择集
- 调用概览: items, info, append, len
- 理解: 主要用于处理相关逻辑。依据注释：将com对象列表 LB 中的对象按 ObjectName 分类，并存储其 Handle。。邻近注释提示：&&% 按类型句柄分组。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### record_handle_with_type(LB, typename, prefix)
- 说明: 替代 XData 方法：记录对象 Handle、类型名、编号，返回结构化字典。
- 邻近注释: 通过名称存储对象信息反回溯对象 | &&% 记录类型句柄
- 参数: LB, typename, prefix
- 返回推断: object
- 关注点: COM, 日志/测试
- 调用概览: enumerate, info, len
- 理解: 主要用于保存/写入相关逻辑。依据注释：替代 XData 方法：记录对象 Handle、类型名、编号，返回结构化字典。。邻近注释提示：通过名称存储对象信息反回溯对象；&&% 记录类型句柄。实现特征：涉及扩展数据 XData 读写。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### convert_named_dict(ZD, typename)
- 说明: 将 ZD["门"] 的结构由 Handle: 编号 转换为 编号: COM对象
- 邻近注释: &&% 转换命名字典
- 参数: ZD, typename
- 返回: 新的字典 {编号: COM实体}
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, get, items, HandleToObject, info
- 理解: 主要用于转换/解析相关逻辑。依据注释：将 ZD["门"] 的结构由 Handle: 编号 转换为 编号: COM对象。邻近注释提示：&&% 转换命名字典。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_named_object(tag, ZD, typename)
- 说明: （无）
- 邻近注释: &&% 获取命名对象
- 参数: tag, ZD, typename
- 返回推断: object
- 调用概览: convert_named_dict, get
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 获取命名对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_tags_on_objects_fixed(named_dict, height, offset)
- 说明: 在每个对象的中心点附近绘制标注文字。
- 邻近注释: &&% 绘制固定标签
- 参数: named_dict, height, offset
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, items, GetBoundingBox, VARIANT, AddText, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：在每个对象的中心点附近绘制标注文字。。邻近注释提示：&&% 绘制固定标签。实现特征：创建文字对象。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### label_tarch_doors(LB1, typename, prefix)
- 说明: 从对象列表 LB1 中筛选出天正门 (ObjectName == 'TDbOpening')，
- 邻近注释: 给天正对象打上标签存入字典，用于以名称反向回溯操作 | &&% 标记天正门
- 参数: LB1, typename, prefix
- 返回: ZD = {typename: {编号: 对象}}
- 关注点: 日志/测试
- 调用概览: enumerate, info, hasattr, append, len
- 理解: 主要用于处理相关逻辑。依据注释：从对象列表 LB1 中筛选出天正门 (ObjectName == 'TDbOpening')，。邻近注释提示：给天正对象打上标签存入字典，用于以名称反向回溯操作；&&% 标记天正门。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_handle_object_map(ms)
- 说明: 返回 {handle: object} 映射
- 邻近注释: &&% 获取句柄映射
- 参数: ms
- 返回推断: object
- 关注点: COM
- 理解: 主要用于获取/选择相关逻辑。依据注释：返回 {handle: object} 映射。邻近注释提示：&&% 获取句柄映射。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_xdata(com_obj, app_name, data_types, data_values)
- 说明: 向任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）附加 XData。
- 邻近注释: &&% 设置扩展数据
- 参数: com_obj, app_name, data_types, data_values
- 返回推断: object
- 关注点: COM
- 调用概览: vtint, vtvariant, SetXData, VARIANT
- 理解: 主要用于更新/设置相关逻辑。依据注释：向任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）附加 XData。。邻近注释提示：&&% 设置扩展数据。实现特征：涉及扩展数据 XData 读写。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_xdata(com_obj, app_name)
- 说明: 从任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）读取 XData。
- 邻近注释: &&% 获取扩展数据
- 参数: com_obj, app_name
- 返回: (type_codes, data_values) 二元组，其中
- 关注点: COM
- 调用概览: VARIANT, GetXData, list
- 理解: 主要用于获取/选择相关逻辑。依据注释：从任意 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）读取 XData。。邻近注释提示：&&% 获取扩展数据。实现特征：涉及扩展数据 XData 读写。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_xdata_tab(entitycom)
- 说明: （无）
- 邻近注释: &&% Xdata标记 | &&% 设置打印标记
- 参数: entitycom
- 返回推断: None
- 调用概览: set_xdata
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：&&% Xdata标记；&&% 设置打印标记。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### is_printApp_xdata_com(entitycom)
- 说明: （无）
- 邻近注释: &&% 检查打印标记
- 参数: entitycom
- 返回推断: bool
- 调用概览: get_xdata
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 检查打印标记。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### write_cad_text(p, text, alignment, height, width_factor, rotation, oblique, style, layer)
- 说明: 【架构适配版】在指定位置写入 CAD 单行文字。
- 邻近注释: &&&% 文字 | &&% 写CAD单行文字
- 参数: p, text, alignment, height, width_factor, rotation, oblique, style, layer
- 返回推断: None,NoneType,object
- 关注点: COM, 几何, 文件, 日志/测试, 进程
- 关键调用: C.li
- 调用概览: li, print, VARIANT, float, AddText, setattr, Update, GetBoundingBox, lower, Move, len, append...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【架构适配版】在指定位置写入 CAD 单行文字。。邻近注释提示：&&&% 文字；&&% 写CAD单行文字。实现特征：创建文字对象。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### write_tianzheng_text(p, text, alignment, height, width_factor, rotation, oblique, style, system_layer, system_file_name, delete_system_text)
- 说明: 在当前激活图中写入一段“天正单行文字”（通过系统模板 Copy 实现），
- 邻近注释: &&% 写天正单行文字
- 参数: p, text, alignment, height, width_factor, rotation, oblique, style, system_layer, system_file_name, delete_system_text
- 返回推断: None,NoneType,object
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待
- 关键调用: C.doc, C.acad
- 调用概览: info, lower, VARIANT, Move, stc, getattr, _align_entity_by_bbox, GetBoundingBox, len, float, Copy, set_object_property...
- 理解: 主要用于保存/写入相关逻辑。依据注释：在当前激活图中写入一段“天正单行文字”（通过系统模板 Copy 实现），。邻近注释提示：&&% 写天正单行文字。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### align_text_to_vertical_line(text_obj, x_position, align_side)
- 说明: 将文字按 BoundingBox 边界对齐到指定垂直线的 X 坐标。
- 邻近注释: ====================  文字垂直对齐 ==================== | &&% 文字垂直对齐
- 参数: text_obj, x_position, align_side
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 关键调用: C.li
- 调用概览: li, isinstance, info, enumerate, print, list, float, GetBoundingBox, VARIANT, Move, len
- 理解: 主要用于处理相关逻辑。依据注释：将文字按 BoundingBox 边界对齐到指定垂直线的 X 坐标。。邻近注释提示：====================  文字垂直对齐 ====================；&&% 文字垂直对齐。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### align_text_to_horizontal_line(text_obj, y_position, align_side)
- 说明: 将文字按 BoundingBox 边界对齐到指定水平线的 Y 坐标。
- 邻近注释: ====================  文字水平对齐 ==================== | &&% 文字水平对齐
- 参数: text_obj, y_position, align_side
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 关键调用: C.li
- 调用概览: li, isinstance, info, enumerate, print, list, float, GetBoundingBox, VARIANT, Move, len
- 理解: 主要用于处理相关逻辑。依据注释：将文字按 BoundingBox 边界对齐到指定水平线的 Y 坐标。。邻近注释提示：====================  文字水平对齐 ====================；&&% 文字水平对齐。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### scale_tianzheng_text_to_cad(tianzheng_text_obj, cad_text_obj)
- 说明: 使用 ScaleEntity 将天正文字的 BoundingBox 高度缩放到 CAD 文字的高度。
- 邻近注释: ====================  缩放天正文字高度 ==================== | &&% 缩放天正文字
- 参数: tianzheng_text_obj, cad_text_obj
- 返回推断: bool
- 关注点: COM, 日志/测试
- 关键调用: C.li
- 调用概览: li, isinstance, info, enumerate, print, list, GetBoundingBox, float, VARIANT, ScaleEntity, len
- 理解: 主要用于处理相关逻辑。依据注释：使用 ScaleEntity 将天正文字的 BoundingBox 高度缩放到 CAD 文字的高度。。邻近注释提示：====================  缩放天正文字高度 ====================；&&% 缩放天正文字。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### sc_objs_to_layer(layer_name, cl)
- 说明: （无）
- 参数: layer_name, cl
- 返回推断: list,object
- 关注点: 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: alias, pmxz_new, Item, Add, SelectOnScreen, Delete, info, print, range
- 理解: 主要用于处理相关逻辑。实现特征：涉及图层操作；涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### delete_layer(layername)
- 说明: 删除当前 DWG 文件中名为 layername 的图层。
- 邻近注释: &&% 删除图层
- 参数: layername
- 返回推断: None
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, Item, Delete, info
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除当前 DWG 文件中名为 layername 的图层。。邻近注释提示：&&% 删除图层。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### create_layers_from_list(layer_names)
- 说明: 创建列表中指定的图层，如果图层已存在则跳过。
- 邻近注释: &&% 从列表创建图层
- 参数: layer_names
- 关注点: 日志/测试
- 调用概览: get_acad_doc, info, print, Item, Add
- 理解: 主要用于创建/插入相关逻辑。依据注释：创建列表中指定的图层，如果图层已存在则跳过。。邻近注释提示：&&% 从列表创建图层。实现特征：涉及图层操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### delete_layers_from_list(layer_names)
- 说明: 删除列表中指定的图层
- 邻近注释: &&% 从列表删除图层
- 参数: layer_names
- 返回: dict: {'deleted': 删除成功的图层列表, 'failed': 删除失败的图层列表}
- 关注点: 日志/测试
- 调用概览: get_acad_doc, info, Item, Delete, append, len
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除列表中指定的图层。邻近注释提示：&&% 从列表删除图层。实现特征：涉及图层操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### dim_by_points(*args)
- 说明: 使用天正逐点标注命令对倾斜对象进行标注
- 邻近注释: &&% 逐点标注
- 参数: *args
- 返回: bool: 成功返回True
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: hotkey, sleep, activate_window_by_title, get_acad_doc, SendCommand, print, len, info
- 理解: 主要用于处理相关逻辑。依据注释：使用天正逐点标注命令对倾斜对象进行标注。邻近注释提示：&&% 逐点标注。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### ensure_layer(layer_name)
- 说明: 确保图层存在并设为当前图层，同时删除该图层上所有对象（最多重试 3 次）。
- 邻近注释: &&% 确保图层存在并清空
- 参数: layer_name
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 调用概览: li, info, range, Item, select_tuceng, sleep, SendCommand, len, print, Add, Delete
- 理解: 主要用于处理相关逻辑。依据注释：确保图层存在并设为当前图层，同时删除该图层上所有对象（最多重试 3 次）。。邻近注释提示：&&% 确保图层存在并清空。实现特征：涉及图层操作；通过命令发送驱动 CAD 行为。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### ensure_layer_model_only(layer_name)
- 说明: 确保图层存在并设为当前图层，同时【仅删除】该图层在模型空间（Model Space）中的对象。
- 邻近注释: &&% 只在模型空间上清理
- 参数: layer_name
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: info, range, Item, select_tuceng, sleep, SendCommand, sum, print, Add, get_obj_loc, Delete
- 理解: 主要用于处理相关逻辑。依据注释：确保图层存在并设为当前图层，同时【仅删除】该图层在模型空间（Model Space）中的对象。。邻近注释提示：&&% 只在模型空间上清理。实现特征：涉及图层操作；通过命令发送驱动 CAD 行为。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### ensure_layer_current(layer_name, max_retries)
- 说明: 确保图层存在并设为当前图层，失败时最多重试 max_retries 次。
- 参数: layer_name, max_retries
- 返回推断: bool
- 关注点: 日志/测试
- 调用概览: alias, range, info, Item, Add
- 理解: 主要用于处理相关逻辑。依据注释：确保图层存在并设为当前图层，失败时最多重试 max_retries 次。。实现特征：涉及图层操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_layer_properties(layer_name, color_index, linetype, on, frozen)
- 说明: 设置指定图层的颜色、线型、开关状态和冻结状态。
- 参数: layer_name, color_index, linetype, on, frozen
- 关注点: COM, 日志/测试
- 调用概览: alias, li, SendCommand, info, Item, Add, Load
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置指定图层的颜色、线型、开关状态和冻结状态。。实现特征：涉及图层操作；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_layer_with_retry(LB, layername, ci)
- 说明: 将给定 COM 对象列表 LB 中的每个对象的 Layer 属性设为 layername。
- 邻近注释: &&% 将列表中的对象图层设为目标图层
- 参数: LB, layername, ci
- 返回推断: tuple
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 调用概览: li, get, print, range, globals, list, Item, info, Add, setattr, append, getattr...
- 理解: 主要用于更新/设置相关逻辑。依据注释：将给定 COM 对象列表 LB 中的每个对象的 Layer 属性设为 layername。。邻近注释提示：&&% 将列表中的对象图层设为目标图层。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### force_layer_objects_color(layer_name, target_color, max_retries)
- 说明: [最终修正版] 强制改色
- 邻近注释: &&% 强制改图层对象颜色
- 参数: layer_name, target_color, max_retries
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: info, list, range, stc, print, enumerate, sleep, set_attr, get_attr, len, Update, append
- 理解: 主要用于处理相关逻辑。依据注释：[最终修正版] 强制改色。邻近注释提示：&&% 强制改图层对象颜色。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### build_J_points_from_selected_texts(LB, n_points, prefix_x, prefix_y)
- 说明: （无）
- 邻近注释: &&% 从文本构建J点
- 参数: LB, n_points, prefix_x, prefix_y
- 返回推断: object,tuple
- 调用概览: compile, sort, search, float, get_text_and_ip, replace, startswith, RuntimeError, str, ValueError, group, append...
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 从文本构建J点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### convert_pts_dict_to_latlon(pts_dict, central_lon)
- 说明: 输入: pts_dict = {'J1': (N, E), 'J2': (N, E), ...}
- 邻近注释: 从界点大地坐标计算经纬度 | &&% 坐标转经纬度
- 参数: pts_dict, central_lon
- 返回推断: object,tuple
- 调用概览: items, cos, tan, one_point, sqrt, degrees, sin, radians
- 理解: 主要用于转换/解析相关逻辑。依据注释：输入: pts_dict = {'J1': (N, E), 'J2': (N, E), ...}。邻近注释提示：从界点大地坐标计算经纬度；&&% 坐标转经纬度。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### xianshi_yincangtuxing()
- 说明: （无）
- 邻近注释: &&% 显示隐藏图形
- 参数: （无）
- 关注点: COM
- 调用概览: SendCommand, Save, chr
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 显示隐藏图形。实现特征：执行保存；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### run_cad_program(timeout_event, event)
- 说明: （无）
- 邻近注释: &&% 运行CAD程序
- 参数: timeout_event, event
- 关注点: COM, 日志/测试, 时间/等待, 进程
- 调用概览: CoInitialize, EnsureDispatch, print, SendCommand, wait, CoUninitialize, set, info, chr
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 运行CAD程序。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### automate_window_with_pywinauto_t7(timeout_event, event)
- 说明: （无）
- 邻近注释: &&% 自动化T7窗口
- 参数: timeout_event, event
- 关注点: COM, 日志/测试, 时间/等待, 窗口/输入
- 调用概览: CoInitialize, get_acad_process_id, connect, sleep, exists, child_window, print, CoUninitialize, set, find_windows, window, children...
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 自动化T7窗口。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### zhuancheng_t7()
- 说明: 在li()连接激活文件后，直接执行该命令即可转换
- 邻近注释: &&% # 天正转t7 | &&% 转成T7
- 参数: （无）
- 关注点: COM, 文件, 时间/等待, 窗口/输入
- 调用概览: time, Event, Thread, start, join, print, is_set, set
- 理解: 主要用于处理相关逻辑。依据注释：在li()连接激活文件后，直接执行该命令即可转换。邻近注释提示：&&% # 天正转t7；&&% 转成T7。依赖 CAD COM 对象与当前文档/模型空间。包含窗口/输入自动化。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### automate_window_with_pywinauto_t3(timeout_event, event)
- 说明: （无）
- 邻近注释: &&% 自动化T3窗口
- 参数: timeout_event, event
- 关注点: COM, 日志/测试, 时间/等待, 窗口/输入
- 调用概览: CoInitialize, get_acad_process_id, connect, sleep, exists, child_window, print, CoUninitialize, set, find_windows, window, children...
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 自动化T3窗口。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### zhuancheng_t3()
- 说明: 在li()连接激活文件后，直接执行该命令即可转换
- 邻近注释: &&% # 天正转t3 | &&% 转成T3
- 参数: （无）
- 关注点: COM, 文件, 时间/等待, 窗口/输入
- 调用概览: time, Event, Thread, start, join, print, is_set, set
- 理解: 主要用于处理相关逻辑。依据注释：在li()连接激活文件后，直接执行该命令即可转换。邻近注释提示：&&% # 天正转t3；&&% 转成T3。依赖 CAD COM 对象与当前文档/模型空间。包含窗口/输入自动化。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### ensure_file_absent(save_path, ty)
- 说明: 确保指定路径的文件不存在。如果存在，则删除并等待 ty 秒。
- 邻近注释: &&&% 新加 | &&% 确保文件被删除
- 参数: save_path, ty
- 关注点: 文件, 日志/测试, 时间/等待
- 调用概览: isfile, remove, sleep, info
- 理解: 主要用于处理相关逻辑。依据注释：确保指定路径的文件不存在。如果存在，则删除并等待 ty 秒。。邻近注释提示：&&&% 新加；&&% 确保文件被删除。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### traverse_with_os_walk(root_dir)
- 说明: 遍历 root_dir 及其所有子目录，打印每个目录和文件的完整路径。
- 邻近注释: &&% 遍历目录
- 参数: root_dir
- 关注点: 文件, 日志/测试
- 调用概览: walk, info, join
- 理解: 主要用于处理相关逻辑。依据注释：遍历 root_dir 及其所有子目录，打印每个目录和文件的完整路径。。邻近注释提示：&&% 遍历目录。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### find_files_with_extensions(directory, extensions)
- 说明: （无）
- 邻近注释: &&% 按后缀查找文件
- 参数: directory, extensions
- 返回推断: object
- 关注点: 文件
- 调用概览: walk, any, append, endswith, join, lower
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 按后缀查找文件。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### get_filename_without_extension(FileandPath)
- 说明: （无）
- 邻近注释: &&% 获取无后缀文件名
- 参数: FileandPath
- 返回推断: object
- 关注点: 文件
- 调用概览: basename, splitext
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 获取无后缀文件名。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### delete_files_with_patterns(folder_path, patterns)
- 说明: 删除文件夹中符合指定模式的文件。
- 邻近注释: &&% 按模式删除文件
- 参数: folder_path, patterns
- 返回: None
- 关注点: 文件, 日志/测试
- 调用概览: listdir, print, join, any, remove, info
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除文件夹中符合指定模式的文件。。邻近注释提示：&&% 按模式删除文件。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### clear_files_with_prefix(folder, filename_prefix, delay)
- 说明: 清除指定文件夹中所有文件名包含给定前缀的文件。若文件正在被占用或删除失败，会尝试重试一次。
- 邻近注释: 确保文件夹中名字含有特殊字符的文件被清空 | &&% 清除指定前缀文件
- 参数: folder, filename_prefix, delay
- 返回推断: None
- 关注点: 文件, 日志/测试, 时间/等待
- 调用概览: listdir, isdir, info, join, remove, isfile, sleep
- 理解: 主要用于删除/清理相关逻辑。依据注释：清除指定文件夹中所有文件名包含给定前缀的文件。若文件正在被占用或删除失败，会尝试重试一次。。邻近注释提示：确保文件夹中名字含有特殊字符的文件被清空；&&% 清除指定前缀文件。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### find_files_with_string(directory, search_string)
- 说明: （无）
- 邻近注释: &&% 按字符串查找文件
- 参数: directory, search_string
- 返回推断: object
- 调用概览: listdir, append
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 按字符串查找文件。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### join_paths(p1, p2)
- 说明: （无）
- 邻近注释: 使路径名和文件名合并后合乎预期 | &&% 路径拼接
- 参数: p1, p2
- 返回推断: object
- 关注点: 文件
- 调用概览: join, replace
- 理解: 主要用于处理相关逻辑。邻近注释提示：使路径名和文件名合并后合乎预期；&&% 路径拼接。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### get_block_name(obj)
- 说明: 获取块名，兼容动态块(EffectiveName)
- 邻近注释: &&&&%%  第六部分 图块操作 | &&&% 原块处理 | &&% 获取块实例块名
- 参数: obj
- 返回推断: object
- 调用概览: getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取块名，兼容动态块(EffectiveName)。邻近注释提示：&&&&%%  第六部分 图块操作；&&&% 原块处理；&&% 获取块实例块名。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### huoqukuai_shuxing_zhi(XX)
- 说明: （无）
- 邻近注释: &&% 获取块属性值
- 参数: XX
- 返回推断: tuple
- 调用概览: GetAttributes, append
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 获取块属性值。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### update_block_def_attributes_safe(block_ref_or_name, target_tag)
- 说明: 【函数编号】: BLK-007-Safe
- 邻近注释: &&% 属性块标签编辑
- 参数: block_ref_or_name, target_tag
- 返回推断: bool
- 关注点: 几何, 文件, 日志/测试
- 关键调用: C.doc
- 调用概览: isinstance, get_attr, info, Item, cast_object, set_attr, print, int, str, float, len, globals...
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: BLK-007-Safe。邻近注释提示：&&% 属性块标签编辑。实现特征：涉及块定义/块实例操作。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### update_block_def_attributes_v7(block_ref_or_name, target_tag)
- 说明: 【函数编号】: BLK-007
- 参数: block_ref_or_name, target_tag
- 返回推断: bool
- 关注点: COM, 几何, 日志/测试
- 关键调用: C.li
- 调用概览: li, isinstance, info, Item, str, float, vtpnt, Move, print, CastTo, int, len...
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: BLK-007。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### attsync_block_instance(block_ref_obj)
- 说明: 【函数编号】: CMD-001
- 邻近注释: &&% 属性块标签编辑生效
- 参数: block_ref_obj
- 返回推断: object
- 关注点: 日志/测试, 时间/等待
- 调用概览: info, range, get_attr, attsync_block_instance_base, sleep
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: CMD-001。邻近注释提示：&&% 属性块标签编辑生效。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### attsync_block_instance_base(block_ref_obj)
- 说明: 【函数编号】: CMD-001
- 参数: block_ref_obj
- 返回推断: bool
- 关注点: COM, 日志/测试
- 关键调用: C.li, C.doc
- 调用概览: li, hasattr, info, getattr, print, SendCommand
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: CMD-001。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_attribute_mtext(block, tags, new_texts, keep_prefix, verbose)
- 说明: set_attribute_mtext(p[0],"图纸规格","A0")
- 邻近注释: &&% 设置属性块的标签值
- 参数: block, tags, new_texts, keep_prefix, verbose
- 返回推断: object
- 关注点: COM, 日志/测试, 进程
- 关键调用: C.li
- 调用概览: li, isinstance, cast_object, zip, list, GetAttributes, get_attr, Update, get, set_attr, len, extend...
- 理解: 主要用于更新/设置相关逻辑。依据注释：set_attribute_mtext(p[0],"图纸规格","A0")。邻近注释提示：&&% 设置属性块的标签值。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_block_attributes_dict(block_ref, ignore_empty, upper_tag)
- 说明: 获取块参照 block_ref 的所有属性，返回 {标签: 纯文本值} 的字典。
- 邻近注释: &&% 获取属性块标签及标签值
- 参数: block_ref, ignore_empty, upper_tag
- 返回: dict，如:
- 调用概览: getattr, str, GetAttributes, strip, _clean_value, isinstance, startswith, split, upper
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取块参照 block_ref 的所有属性，返回 {标签: 纯文本值} 的字典。。邻近注释提示：&&% 获取属性块标签及标签值。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### separate_entities_by_block_names(entities, target_names)
- 说明: 将实体列表分为两组：
- 邻近注释: &&% 筛选出指定块名外的对象
- 参数: entities, target_names
- 返回: (kept_entities, target_blocks) 元组
- 调用概览: isinstance, set, get_attr, append
- 理解: 主要用于处理相关逻辑。依据注释：将实体列表分为两组：。邻近注释提示：&&% 筛选出指定块名外的对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### huoqu_kuai_pl(blocka)
- 说明: （无）
- 邻近注释: &&% 获取块内多段线
- 参数: blocka
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, Item, list, str, print
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 获取块内多段线。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### create_block_with_basepoint()
- 说明: （无）
- 邻近注释: 定义基点的块 | &&% 创建带基点块
- 参数: （无）
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, vtpnt, Add, AddCircle
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：定义基点的块；&&% 创建带基点块。实现特征：创建圆对象；涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### create_block_with_triangle_and_text()
- 说明: （无）
- 邻近注释: 块的添加 | &&% 创建三角形文字块
- 参数: （无）
- 关注点: COM, 几何, 进程
- 调用概览: EnsureDispatch, vtpnt, Add, AddLine, AddText, print
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：块的添加；&&% 创建三角形文字块。实现特征：创建文字对象；创建直线对象；涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### huoqu_kuai_pl(blocka)
- 说明: （无）
- 参数: blocka
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, Item, list, str, print
- 理解: 主要用于处理相关逻辑。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_bounding_box_of_block(block_name)
- 说明: （无）
- 邻近注释: 块的边界 | &&% 获取块包围盒
- 参数: block_name
- 返回推断: tuple
- 关注点: COM, 几何, 进程
- 调用概览: EnsureDispatch, Item, float, GetBoundingBox, min, max
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：块的边界；&&% 获取块包围盒。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### create_new_block_with_insert_and_line()
- 说明: （无）
- 邻近注释: &&% 创建含插入和直线的块
- 参数: （无）
- 返回推断: None
- 关注点: COM, 进程
- 调用概览: EnsureDispatch, vtpnt, Add, InsertBlock, AddLine, print
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：&&% 创建含插入和直线的块。实现特征：创建直线对象；涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### copy_and_move_blocks_from_layer(layer_name, block_prefix)
- 说明: （无）
- 邻近注释: &&% 复制并移动图层块
- 参数: layer_name, block_prefix
- 关注点: COM, 文件, 日志/测试, 选择集
- 调用概览: select_tuceng, VARIANT, info, Copy, Move, len
- 理解: 主要用于移动/复制相关逻辑。邻近注释提示：&&% 复制并移动图层块。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### delete_block_instances_and_definition_retry(target_block_name, max_rounds)
- 说明: 删除指定名称的块实例和块定义，带重试机制。
- 邻近注释: 块名的清除 | &&&% 删除指定块名的实例及块 | &&% 旧版
- 参数: target_block_name, max_rounds
- 返回推断: None,bool
- 关注点: 日志/测试, 时间/等待, 选择集
- 调用概览: get_acad_doc, info, range, print, select_kuai, len, Item, Delete, sleep, upper, append, safe_delete...
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除指定名称的块实例和块定义，带重试机制。。邻近注释提示：块名的清除；&&&% 删除指定块名的实例及块；&&% 旧版。实现特征：涉及块定义/块实例操作。包含选择集构造或过滤。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；超时与重试次数边界

### delete_block_instances_and_definition_optimized(target_name, max_retries)
- 说明: 【函数编号】: CLEAN-ROBUST-V34 (核验版)
- 邻近注释: &&% 极速清理
- 参数: target_name, max_retries
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: range, info, Item, Add, VARIANT, Select, Delete, Erase, wait_command_done, sleep, Regen
- 理解: 主要用于删除/清理相关逻辑。依据注释：【函数编号】: CLEAN-ROBUST-V34 (核验版)。邻近注释提示：&&% 极速清理。实现特征：涉及块定义/块实例操作；涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### delete_block_instances_and_definition_optimized(target_name, max_retries)
- 说明: 【最终推荐版】
- 邻近注释: &&% 再次优化
- 参数: target_name, max_retries
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: info, range, error, Item, Add, VARIANT, Select, Delete, Erase, Regen, sleep
- 理解: 主要用于删除/清理相关逻辑。依据注释：【最终推荐版】。邻近注释提示：&&% 再次优化。实现特征：涉及块定义/块实例操作；涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### rename_block_entity(ent, new_name)
- 说明: 将给定块参照实体 ent 的块名改为 new_name。
- 邻近注释: &&% 重命名块实体
- 参数: ent, new_name
- 调用概览: Item
- 理解: 主要用于更新/设置相关逻辑。依据注释：将给定块参照实体 ent 的块名改为 new_name。。邻近注释提示：&&% 重命名块实体。实现特征：涉及块定义/块实例操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_block_instances(block_name, max_retries)
- 说明: 根据给定的块定义名，检索当前图形中所有对应的块参照实例（BlockReference），
- 邻近注释: &&% 由块名选择实例
- 参数: block_name, max_retries
- 返回: instances     – 包含所有匹配块参照的列表（如果未找到或者出错，返回空列表）
- 关注点: 日志/测试, 选择集
- 调用概览: info, select_kuai, append, len, getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：根据给定的块定义名，检索当前图形中所有对应的块参照实例（BlockReference），。邻近注释提示：&&% 由块名选择实例。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### get_entities_from_block_reference(block_ref)
- 说明: 获取块引用对象中的所有子实体（COM对象形式）。
- 邻近注释: &&% 从块实体对象获取其内部com对象 | &&% 获取块引用实体
- 参数: block_ref
- 返回: entities: 子实体列表
- 关注点: 日志/测试
- 调用概览: Item, info, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取块引用对象中的所有子实体（COM对象形式）。。邻近注释提示：&&% 从块实体对象获取其内部com对象；&&% 获取块引用实体。实现特征：涉及块定义/块实例操作。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### insert_block_into_autocad(block_file_path, insertion_point, scale, rotation)
- 说明: 以块的方式插入 DWG 文件到 AutoCAD 中
- 邻近注释: 以块的方式插入文件 | &&% 插入块到CAD
- 参数: block_file_path, insertion_point, scale, rotation
- 关注点: 日志/测试
- 调用概览: InsertBlock, info
- 理解: 主要用于创建/插入相关逻辑。依据注释：以块的方式插入 DWG 文件到 AutoCAD 中。邻近注释提示：以块的方式插入文件；&&% 插入块到CAD。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### insert_standard_block(block_dwg, insertion_point, scale, rotation, wait)
- 说明: 不炸开，
- 邻近注释: 不炸开 | &&% 插入标准块
- 参数: block_dwg, insertion_point, scale, rotation, wait
- 返回推断: list,object
- 关注点: COM, 文件, 时间/等待, 选择集
- 调用概览: select_kuai, replace, SendCommand, sleep, isfile, FileNotFoundError, print, GetBoundingBox, append, abspath
- 理解: 主要用于创建/插入相关逻辑。依据注释：不炸开，。邻近注释提示：不炸开；&&% 插入标准块。实现特征：通过命令发送驱动 CAD 行为。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### insert_and_explode_dwg(block_dwg, insertion_point, scale, rotation, wait)
- 说明: 将一个 WBLOCK 导出的标准块 DWG 插入到当前图，
- 邻近注释: 炸开 | &&% 插入并炸开DWG
- 参数: block_dwg, insertion_point, scale, rotation, wait
- 返回推断: list,tuple
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 选择集
- 调用概览: select_kuai, replace, SendCommand, sleep, info, isfile, FileNotFoundError, print, append, abspath, safe_get_bbox, basename...
- 理解: 主要用于创建/插入相关逻辑。依据注释：将一个 WBLOCK 导出的标准块 DWG 插入到当前图，。邻近注释提示：炸开；&&% 插入并炸开DWG。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### insert_and_explode_dwg(block_dwg, insertion_point, scale, rotation, wait)
- 说明: 【V3.0 重构版】插入并炸开 DWG
- 参数: block_dwg, insertion_point, scale, rotation, wait
- 返回推断: tuple
- 关注点: COM, 文件, 日志/测试, 选择集
- 关键调用: SafeCOM, C.doc
- 调用概览: info, replace, basename, isfile, select_kuai, CADGuard, SendCommand, print, abspath, call, append, getattr
- 理解: 主要用于创建/插入相关逻辑。依据注释：【V3.0 重构版】插入并炸开 DWG。实现特征：通过命令发送驱动 CAD 行为。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### get_large_block_instances(area_threshold, tol, max_retries)
- 说明: 获取模型空间中所有块实例，筛选出“包围盒面积大于 area_threshold” 的块，
- 邻近注释: &&% 获取面积足够大的全部非同名块实例 | &&% 获取大块实例
- 参数: area_threshold, tol, max_retries
- 返回推断: list,object
- 关注点: 日志/测试, 选择集
- 调用概览: select_kuai, info, GetBoundingBox, abs, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取模型空间中所有块实例，筛选出“包围盒面积大于 area_threshold” 的块，。邻近注释提示：&&% 获取面积足够大的全部非同名块实例；&&% 获取大块实例。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### get_large_block_instances_with_tolerance(max_retries, area_threshold)
- 说明: 获取当前 DWG 中所有大尺寸块实例
- 邻近注释: 从com对象中，根据其外包盒的矩形的长边与短边的比值和面积在160000000到1000000000两个条件筛算 | &&% 确定合乎标准打印要求的自建多段线区域
- 参数: max_retries, area_threshold
- 返回推断: list,object
- 关注点: 日志/测试, 选择集
- 调用概览: select_kuai, info, GetBoundingBox, abs, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取当前 DWG 中所有大尺寸块实例。邻近注释提示：从com对象中，根据其外包盒的矩形的长边与短边的比值和面积在160000000到1000000000两个条件筛算；&&% 确定合乎标准打印要求的自建多段线区域。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### transform_point_by_block(block_ref, local_pt)
- 说明: 将块内部坐标 local_pt = (lx, ly, lz) 转换为世界坐标：
- 邻近注释: &&% 块内坐标转换成世界坐标（适合平面上的一般块）
- 参数: block_ref, local_pt
- 返回推断: tuple
- 关注点: 几何
- 调用概览: cos, sin
- 理解: 主要用于转换/解析相关逻辑。依据注释：将块内部坐标 local_pt = (lx, ly, lz) 转换为世界坐标：。邻近注释提示：&&% 块内坐标转换成世界坐标（适合平面上的一般块）。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### select_block_by_name(block_name, max_retries)
- 说明: 从 *模型空间* 快速选出指定块名的所有实例，返回实体列表。
- 邻近注释: &&% 按名称选择块
- 参数: block_name, max_retries
- 返回推断: list,object
- 关注点: COM, 日志/测试, 时间/等待, 选择集
- 调用概览: range, info, time, Add, vtInt, vtVariant, Select, list, suppress, Delete, sleep, Item...
- 理解: 主要用于获取/选择相关逻辑。依据注释：从 *模型空间* 快速选出指定块名的所有实例，返回实体列表。。邻近注释提示：&&% 按名称选择块。实现特征：涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### get_all_block_definitions(max_retry, quiet)
- 说明: 返回当前 DWG 中所有块定义（BlockTableRecord）对象列表。
- 邻近注释: &&% 获取所有块定义
- 参数: max_retry, quiet
- 返回: list[COM block object]
- 关注点: COM, 文件, 时间/等待
- 调用概览: range, log, li, RuntimeError, clear, print, PumpWaitingMessages, sleep, len, suppress, Item, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：返回当前 DWG 中所有块定义（BlockTableRecord）对象列表。。邻近注释提示：&&% 获取所有块定义。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### get_all_block_names()
- 说明: 使用全局 li()/doc 获取当前 DWG 中所有块定义的名字列表。
- 邻近注释: &&% 获取所有块名
- 参数: （无）
- 返回推断: object
- 关注点: COM
- 调用概览: get_all_block_definitions, append, str
- 理解: 主要用于获取/选择相关逻辑。依据注释：使用全局 li()/doc 获取当前 DWG 中所有块定义的名字列表。。邻近注释提示：&&% 获取所有块名。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### purge_block(block_name, quiet)
- 说明: 删除指定块的所有实例，并彻底清除该块定义。
- 邻近注释: &&% 块清理
- 参数: block_name, quiet
- 关注点: COM, 文件, 日志/测试, 时间/等待, 进程
- 调用概览: EnsureDispatch, list, sleep, info, suppress, PurgeAll, Item, Delete, print, getattr
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除指定块的所有实例，并彻底清除该块定义。。邻近注释提示：&&% 块清理。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### purge_unused_blocks(quiet)
- 说明: 一次性清除所有未被任何 INSERT 实例引用的块定义。
- 邻近注释: &&% 清理未使用块
- 参数: quiet
- 返回推断: object
- 关注点: COM, 文件, 日志/测试, 进程, 选择集
- 调用概览: EnsureDispatch, range, time, suppress, PurgeAll, info, append, print, Item, len
- 理解: 主要用于删除/清理相关逻辑。依据注释：一次性清除所有未被任何 INSERT 实例引用的块定义。。邻近注释提示：&&% 清理未使用块。实现特征：涉及块定义/块实例操作；涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### purge_block_1(block_name, quiet, max_delete_attempts)
- 说明: 删除指定块的所有实例，并尽可能彻底清除该块定义。
- 邻近注释: &&% 清理块1
- 参数: block_name, quiet, max_delete_attempts
- 返回推断: None,bool,object
- 关注点: COM, 文件, 时间/等待
- 调用概览: node, sleep, range, strftime, li, log, suppress, list, PurgeAll, print, getattr, Item...
- 理解: 主要用于删除/清理相关逻辑。依据注释：删除指定块的所有实例，并尽可能彻底清除该块定义。。邻近注释提示：&&% 清理块1。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### purge_unused_blocks_1(quiet, protect_names, max_delete_attempts, rename_prefix)
- 说明: 一次性清除“当前文件中没有任何实例引用”的块定义。
- 邻近注释: &&% 清理未使用块1
- 参数: quiet, protect_names, max_delete_attempts, rename_prefix
- 返回推断: bool,list,object
- 关注点: COM, 文件, 时间/等待
- 调用概览: node, Counter, time, log, startswith, strftime, li, suppress, PurgeAll, range, print, getattr...
- 理解: 主要用于删除/清理相关逻辑。依据注释：一次性清除“当前文件中没有任何实例引用”的块定义。。邻近注释提示：&&% 清理未使用块1。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### reserve_block_names_for_new_insert(block_names, rename_prefix, verbose)
- 说明: 【核心目标】在插入新块之前，为一组块名“预留新定义空间”。
- 邻近注释: &&% 预留新插入块名
- 参数: block_names, rename_prefix, verbose
- 返回: dict: { 原名 -> 新名 }，没有被占用的块名不会出现在返回字典中。
- 关注点: COM, 文件
- 调用概览: isinstance, node, strftime, li, log, print, Item, make_legacy_name, items, now
- 理解: 主要用于创建/插入相关逻辑。依据注释：【核心目标】在插入新块之前，为一组块名“预留新定义空间”。。邻近注释提示：&&% 预留新插入块名。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### get_selected_blockreference_names()
- 说明: 使用 pmxz() 选择实体，并返回所有块引用（AcDbBlockReference）的块名列表。
- 邻近注释: &&% 获取选定块引用名
- 参数: （无）
- 返回推断: list,object
- 关注点: 日志/测试
- 调用概览: pmxz, info, getattr, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：使用 pmxz() 选择实体，并返回所有块引用（AcDbBlockReference）的块名列表。。邻近注释提示：&&% 获取选定块引用名。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### create_block_from_region_cad(x1, y1, x2, y2, insert_point_option, block_name_prefix, base_point, ty)
- 说明: 【纯 CAD 重绘版】从矩形区域创建块（重画为标准 CAD 实体），
- 邻近注释: &&% 从区域创建CAD块
- 参数: x1, y1, x2, y2, insert_point_option, block_name_prefix, base_point, ty
- 返回推断: NoneType,bool,object,tuple
- 关注点: COM, 几何, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: select_entities_in_window, info, group_bbox_corners, get, VARIANT, Add, list, print, InsertBlock, Item, GetBoundingBox, com_retry...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【纯 CAD 重绘版】从矩形区域创建块（重画为标准 CAD 实体），。邻近注释提示：&&% 从区域创建CAD块。实现特征：创建圆对象；创建文字对象；创建点对象；创建直线对象；涉及块定义/块实例操作。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### create_block_from_region_cmd(x1, y1, x2, y2, insert_point_option, block_name_prefix, base_point, ty)
- 说明: 【命令行版】通过 -BLOCK 从矩形区域创建块（保留天正对象），
- 参数: x1, y1, x2, y2, insert_point_option, block_name_prefix, base_point, ty
- 返回推断: NoneType,object,tuple
- 关注点: COM, 几何, 日志/测试, 时间/等待, 选择集
- 关键调用: SafeCOM, C.doc
- 调用概览: _normalize_rect, Add, VARIANT, print, list_selection, info, group_bbox_corners, get, SendCommand, sleep, range, GetVariable...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【命令行版】通过 -BLOCK 从矩形区域创建块（保留天正对象），。实现特征：涉及块定义/块实例操作；涉及系统变量读取/设置；涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### create_block_from_list_cmd(entities, insert_point_option, block_name_prefix, base_point, ty)
- 说明: 【命令行版】将指定的 Python 对象列表封装成块。
- 参数: entities, insert_point_option, block_name_prefix, base_point, ty
- 返回推断: NoneType,object
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 关键调用: C.doc
- 调用概览: ensure_list, group_bbox_corners, info, SendCommand, range, sleep, print, get, len, VARIANT, Item, append...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【命令行版】将指定的 Python 对象列表封装成块。。实现特征：涉及块定义/块实例操作；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### get_block_contents_at_same_location(block_ref)
- 说明: 【函数2】获取块内图形并在原位置复制,它的作用是获取到实体内部对象
- 邻近注释: &&% 获取块内实体
- 参数: block_ref
- 返回推断: list,object
- 关注点: COM, 日志/测试
- 关键调用: C.li
- 调用概览: li, Copy, print, Explode, list, info, Delete, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数2】获取块内图形并在原位置复制,它的作用是获取到实体内部对象。邻近注释提示：&&% 获取块内实体。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### add_entities_to_block_direct(block_ref, entities, delete_original)
- 说明: 【函数】进入块定义内部添加对象（强类型修正版）
- 参数: block_ref, entities, delete_original
- 返回推断: bool,object
- 关注点: COM, 几何, 日志/测试
- 调用概览: ensure_list, info, get_attr, Update, VARIANT, Item, CopyObjects, com_point, float, len, append, isinstance...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数】进入块定义内部添加对象（强类型修正版）。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### add_entities_to_block_definition_explode(block_ref, new_entities, ty)
- 说明: 【函数】向块定义中追加对象（独立版）
- 参数: block_ref, new_entities, ty
- 返回推断: bool
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 关键调用: C.doc
- 调用概览: ensure_list, get_attr, info, SendCommand, range, print, sleep, Explode, list, len, Regen, Update...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数】向块定义中追加对象（独立版）。实现特征：涉及系统变量读取/设置；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### redefine_block_with_entities(block_ref, entities, ty, debug_log_path)
- 说明: 【调试专用版 V2】redefine_block_with_entities
- 参数: block_ref, entities, ty, debug_log_path
- 返回推断: bool
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 进程
- 调用概览: info, len, SetVariable, SendCommand, range, print, GetActiveObject, getattr, Item, append, sleep, GetVariable...
- 理解: 主要用于处理相关逻辑。依据注释：【调试专用版 V2】redefine_block_with_entities。实现特征：涉及块定义/块实例操作；涉及系统变量读取/设置；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### extract_specific_entities_from_block(block_ref, mode, keep_in_block)
- 说明: 【函数】从块中提取指定类型的对象（筛选版）
- 参数: block_ref, mode, keep_in_block
- 返回推断: list,object
- 关注点: COM, 几何, 日志/测试
- 调用概览: lower, info, hasattr, Explode, print, len, get_attr, Update, Regen, append, Delete, Item
- 理解: 主要用于处理相关逻辑。依据注释：【函数】从块中提取指定类型的对象（筛选版）。实现特征：涉及块定义/块实例操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### safe_explode(block_entity)
- 说明: 【原子操作】
- 参数: block_entity
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: retry_on_busy, Explode
- 理解: 主要用于处理相关逻辑。依据注释：【原子操作】。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _atomic_explode_and_delete(block_entity)
- 说明: 【原子操作】
- 参数: block_entity
- 返回推断: object
- 关注点: 时间/等待
- 关键调用: wait_quiescent, retry_on_busy
- 调用概览: retry_on_busy, Explode, Delete, wait_quiescent, sleep
- 理解: 主要用于删除/清理相关逻辑。依据注释：【原子操作】。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### safe_explode_retry(entity, max_retries, rescue_retries, interval, verbose)
- 说明: 【通用原子函数 - 深度搜救修正版 (V5.0)】
- 参数: entity, max_retries, rescue_retries, interval, verbose
- 返回推断: NoneType,bool,list,object
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: wait_quiescent, retry_on_busy
- 调用概览: range, ObjectIdToObject, is_entity_alive, info, hasattr, _atomic_explode_and_delete, print, list, max, sleep, len, wait_quiescent...
- 理解: 主要用于等待/守护相关逻辑。依据注释：【通用原子函数 - 深度搜救修正版 (V5.0)】。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### explode_single_object_marker(ent)
- 说明: 【主函数】炸开单个对象（辅助线回溯版）
- 邻近注释: &&% 炸开对象并回溯
- 参数: ent
- 返回推断: list,object
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: li, info, VARIANT, SendCommand, range, AddLine, set_entity_grip_state_precise, print, wait_command_done, sleep, Item, append...
- 理解: 主要用于处理相关逻辑。依据注释：【主函数】炸开单个对象（辅助线回溯版）。邻近注释提示：&&% 炸开对象并回溯。实现特征：创建直线对象；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### safe_explode_and_delete(bk, ci, delay)
- 说明: 对块对象 bk 执行安全的 Explode 与 Delete 操作：
- 邻近注释: &&% 安全炸开并删除
- 参数: bk, ci, delay
- 返回推断: object
- 关注点: 时间/等待
- 调用概览: range, sleep, RuntimeError, Explode, len, Delete, list
- 理解: 主要用于删除/清理相关逻辑。依据注释：对块对象 bk 执行安全的 Explode 与 Delete 操作：。邻近注释提示：&&% 安全炸开并删除。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### fix_com_cache()
- 说明: 【急救】清理 win32com 的 gen_py 缓存
- 参数: （无）
- 关注点: COM, 文件, 日志/测试
- 调用概览: print, info, exists, hasattr, getsitepackages, GetGeneratePath, join, rmtree, get
- 理解: 主要用于处理相关逻辑。依据注释：【急救】清理 win32com 的 gen_py 缓存。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### delete_all_nul_under_folder(folder_path)
- 说明: 输入文件夹路径（如 D:\claude-tasks），
- 邻近注释: &&% 清除nul
- 参数: folder_path
- 返回推断: None
- 关注点: 文件, 日志/测试, 选择集
- 调用概览: abspath, info, walk, exists, print, lower, join, remove
- 理解: 主要用于删除/清理相关逻辑。依据注释：输入文件夹路径（如 D:\claude-tasks），。邻近注释提示：&&% 清除nul。包含选择集构造或过滤。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### kill_dialog_killer()
- 说明: 查找并终止名为 'cad_dialog_killer.py' 的 Python 进程
- 邻近注释: &&% 终止弹窗程序
- 参数: （无）
- 关注点: 文件, 日志/测试, 进程, 选择集
- 调用概览: print, Popen, communicate, decode, split, info, strip, isdigit, system
- 理解: 主要用于关闭/终止相关逻辑。依据注释：查找并终止名为 'cad_dialog_killer.py' 的 Python 进程。邻近注释提示：&&% 终止弹窗程序。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### kill_python_script_by_name(target_script_name)
- 说明: 【推荐】使用 psutil 精准终止指定名称的 Python 脚本。
- 邻近注释: &&% 终止指定py脚本 (psutil版)
- 参数: target_script_name
- 返回推断: object
- 关注点: 日志/测试, 进程
- 调用概览: info, getpid, lower, process_iter, kill, join
- 理解: 主要用于关闭/终止相关逻辑。依据注释：【推荐】使用 psutil 精准终止指定名称的 Python 脚本。。邻近注释提示：&&% 终止指定py脚本 (psutil版)。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### kill_wps(verbose)
- 说明: 结束所有 WPS/金山办公相关进程，特别是 wpspdf.exe。
- 邻近注释: &&% 结束WPS进程
- 参数: verbose
- 关注点: 进程
- 调用概览: set, call, add, print, join, sorted
- 理解: 主要用于关闭/终止相关逻辑。依据注释：结束所有 WPS/金山办公相关进程，特别是 wpspdf.exe。。邻近注释提示：&&% 结束WPS进程。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### close_all_excel_processes()
- 说明: 【函数编号】: SYS-KILL-XLS
- 邻近注释: &&%关闭excel进程
- 参数: （无）
- 返回推断: bool,int,object
- 关注点: 日志/测试, 时间/等待, 进程, 选择集
- 调用概览: range, print, run, _get_excel_count, info, sleep, count, lower
- 理解: 主要用于关闭/终止相关逻辑。依据注释：【函数编号】: SYS-KILL-XLS。邻近注释提示：&&%关闭excel进程。包含选择集构造或过滤。
- 风险: 涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；超时与重试次数边界

### safe_delete(ob, retries, delay)
- 说明: 安全删除 CAD 对象。
- 邻近注释: &&&% 确保安全删除
- 参数: ob, retries, delay
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: range, Delete, sleep
- 理解: 主要用于删除/清理相关逻辑。依据注释：安全删除 CAD 对象。。邻近注释提示：&&&% 确保安全删除。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### move_entities_in_region(coms, target, ty, max_iter)
- 说明: 将 `coms` 对象的包围盒内所有实体，沿向量 (target - 左下角) 移动，
- 邻近注释: &&% 区域实体移动
- 参数: coms, target, ty, max_iter
- 关注点: COM, 文件, 日志/测试, 时间/等待, 选择集
- 调用概览: GetBoundingBox, range, min, max, highlight_entities_in_window, info, sleep, print, Clear, hasattr, len, list...
- 理解: 主要用于移动/复制相关逻辑。依据注释：将 `coms` 对象的包围盒内所有实体，沿向量 (target - 左下角) 移动，。邻近注释提示：&&% 区域实体移动。实现特征：涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### 圆点(tz)
- 说明: 控制点的显示
- 邻近注释: &&% 设置点样式
- 参数: tz
- 关注点: COM
- 调用概览: SetVariable
- 理解: 主要用于处理相关逻辑。依据注释：控制点的显示。邻近注释提示：&&% 设置点样式。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### 图纸背景(zhi)
- 说明: （无）
- 邻近注释: &&% 设置图纸背景色
- 参数: zhi
- 关注点: COM
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 设置图纸背景色。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### shitu_region(x1, y1, x2, y2)
- 说明: 按按对象外包盒调整视图
- 邻近注释: &&&%  *** 按区域调整视图 | &&% 视图区域缩放
- 参数: x1, y1, x2, y2
- 关注点: COM
- 调用概览: SendCommand, abs
- 理解: 主要用于处理相关逻辑。依据注释：按按对象外包盒调整视图。邻近注释提示：&&&%  *** 按区域调整视图；&&% 视图区域缩放。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### shitu_entity(obj)
- 说明: 按按对象外包盒调整视图
- 邻近注释: 按对象外包盒调整视图 | &&% 视图实体缩放
- 参数: obj
- 关注点: COM
- 调用概览: GetBoundingBox, SendCommand, abs
- 理解: 主要用于处理相关逻辑。依据注释：按按对象外包盒调整视图。邻近注释提示：按对象外包盒调整视图；&&% 视图实体缩放。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### record_screen_gif(output_path, duration, fps, region)
- 说明: 录制屏幕并保存为 GIF。
- 邻近注释: &&% 录制屏幕GIF
- 参数: output_path, duration, fps, region
- 关注点: 日志/测试, 时间/等待
- 调用概览: info, mimsave, time, screenshot, append, sleep, len
- 理解: 主要用于保存/写入相关逻辑。依据注释：录制屏幕并保存为 GIF。。邻近注释提示：&&% 录制屏幕GIF。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### minimize_all_windows()
- 说明: 模拟按下 Win+M，将所有窗口最小化。
- 邻近注释: &&% 最小化所有窗口
- 参数: （无）
- 关注点: 时间/等待, 窗口/输入
- 调用概览: keybd_event, sleep
- 理解: 主要用于处理相关逻辑。依据注释：模拟按下 Win+M，将所有窗口最小化。。邻近注释提示：&&% 最小化所有窗口。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### set_autocad_window_to_top_left(resize_half)
- 说明: 将 AutoCAD 窗口还原并移动到屏幕左上角，可选将其调整为半屏大小。
- 邻近注释: &&%#控制CAD屏幕窗口在左上角 | &&% CAD窗口置左上
- 参数: resize_half
- 返回推断: None
- 关注点: 文件, 日志/测试, 时间/等待, 选择集
- 调用概览: sleep, moveTo, print, restore, activate, size, resizeTo, info, getWindowsWithTitle
- 理解: 主要用于更新/设置相关逻辑。依据注释：将 AutoCAD 窗口还原并移动到屏幕左上角，可选将其调整为半屏大小。。邻近注释提示：&&%#控制CAD屏幕窗口在左上角；&&% CAD窗口置左上。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### l()
- 说明: （无）
- 邻近注释: &&% CAD窗口置左上别名
- 参数: （无）
- 调用概览: set_autocad_window_to_top_left
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% CAD窗口置左上别名。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### minimize_all_windows_d()
- 说明: 模拟 Win + D，将所有窗口最小化（切换）。
- 邻近注释: &&% 更合理控制窗口函数 | — — — — -- -- -- -- --  — — — — -- -- -- -- -- — — — — -- -- -- -- --  — — — — -- -- | &&% 最小化窗口Win+D
- 参数: （无）
- 关注点: 时间/等待, 窗口/输入
- 调用概览: keybd_event, sleep
- 理解: 主要用于处理相关逻辑。依据注释：模拟 Win + D，将所有窗口最小化（切换）。。邻近注释提示：&&% 更合理控制窗口函数；— — — — -- -- -- -- --  — — — — -- -- -- -- -- — — — — -- -- -- -- --  — — — — -- --；&&% 最小化窗口Win+D。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### minimize_all_windows_m()
- 说明: 模拟按下 Win+M，将所有窗口最小化。
- 邻近注释: &&% 最小化窗口Win+M
- 参数: （无）
- 关注点: 时间/等待, 窗口/输入
- 调用概览: keybd_event, sleep
- 理解: 主要用于处理相关逻辑。依据注释：模拟按下 Win+M，将所有窗口最小化。。邻近注释提示：&&% 最小化窗口Win+M。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### restore_and_position(name, width_ratio, height_ratio, x, y)
- 说明: 将第一个标题中包含 name 的窗口恢复、激活，并调整到指定位置和大小。
- 邻近注释: &&% 恢复并定位窗口
- 参数: name, width_ratio, height_ratio, x, y
- 返回推断: bool
- 关注点: 文件, 日志/测试, 时间/等待, 选择集
- 调用概览: sleep, size, max, int, info, activate, moveTo, min, resizeTo, getWindowsWithTitle, restore
- 理解: 主要用于处理相关逻辑。依据注释：将第一个标题中包含 name 的窗口恢复、激活，并调整到指定位置和大小。。邻近注释提示：&&% 恢复并定位窗口。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### list_open_window_titles()
- 说明: 获取当前所有可见窗口的标题列表包括子窗口。
- 邻近注释: &&% 列出打开窗口标题
- 参数: （无）
- 返回推断: object
- 关注点: 选择集
- 调用概览: getAllWindows, strip, append
- 理解: 主要用于打开/读取相关逻辑。依据注释：获取当前所有可见窗口的标题列表包括子窗口。。邻近注释提示：&&% 列出打开窗口标题。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### ceshubiao_weizhi()
- 说明: 提示用户 5 秒内将鼠标移动到 AutoCAD 命令栏输入位置，
- 邻近注释: &&% 测鼠标位置
- 参数: （无）
- 返回推断: tuple
- 关注点: 日志/测试, 时间/等待
- 调用概览: print, sleep, position, info
- 理解: 主要用于处理相关逻辑。依据注释：提示用户 5 秒内将鼠标移动到 AutoCAD 命令栏输入位置，。邻近注释提示：&&% 测鼠标位置。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### run_idle_background(script_path)
- 说明: 用后台模式启动 IDLE 去运行某个脚本，返回 Popen 实例。
- 邻近注释: &&% 后台运行IDLE
- 参数: script_path
- 返回推断: object
- 关注点: 文件, 进程, 选择集
- 调用概览: Popen
- 理解: 主要用于处理相关逻辑。依据注释：用后台模式启动 IDLE 去运行某个脚本，返回 Popen 实例。。邻近注释提示：&&% 后台运行IDLE。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### click_and_drag(x, y, juli)
- 说明: 在屏幕坐标 (x, y) 按下左键，然后向纵向拖动距离 juli。
- 邻近注释: &&% 点击并拖动
- 参数: x, y, juli
- 关注点: 文件, 时间/等待
- 调用概览: moveTo, sleep, mouseDown, mouseUp
- 理解: 主要用于处理相关逻辑。依据注释：在屏幕坐标 (x, y) 按下左键，然后向纵向拖动距离 juli。。邻近注释提示：&&% 点击并拖动。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### click_and_find_image_shape(x, y, tupian_path, timeout)
- 说明: 在 (x, y) 单击一次，然后不断在整个屏幕上查找与 tupian_path 对应的图片形状，
- 邻近注释: &&% 点击并找图
- 参数: x, y, tupian_path, timeout
- 返回推断: NoneType,tuple
- 关注点: 文件, 时间/等待
- 调用概览: moveTo, click, sleep, time, isfile, FileNotFoundError, locateCenterOnScreen, print, int
- 理解: 主要用于获取/选择相关逻辑。依据注释：在 (x, y) 单击一次，然后不断在整个屏幕上查找与 tupian_path 对应的图片形状，。邻近注释提示：&&% 点击并找图。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### right_click_and_move(x, y, x_xiangdui, y_xiangdui)
- 说明: 在屏幕坐标 (x, y) 处执行右键点击，然后将鼠标相对于 (x, y) 
- 邻近注释: &&% 右键点击并移动
- 参数: x, y, x_xiangdui, y_xiangdui
- 关注点: 文件, 时间/等待
- 调用概览: moveTo, click, sleep
- 理解: 主要用于移动/复制相关逻辑。依据注释：在屏幕坐标 (x, y) 处执行右键点击，然后将鼠标相对于 (x, y) 。邻近注释提示：&&% 右键点击并移动。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### kill_all_idle()
- 说明: 终止所有名为 'idle' 或 'idle.exe' 的进程（不再需要任务管理器）。
- 邻近注释: &&% 结束所有IDLE进程
- 参数: （无）
- 关注点: 进程
- 调用概览: process_iter, lower, startswith, terminate
- 理解: 主要用于关闭/终止相关逻辑。依据注释：终止所有名为 'idle' 或 'idle.exe' 的进程（不再需要任务管理器）。。邻近注释提示：&&% 结束所有IDLE进程。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### set_idle_window_to_top_right()
- 说明: （无）
- 邻近注释: &&% IDLE窗口置右上
- 参数: （无）
- 返回推断: None
- 关注点: 文件, 日志/测试, 选择集
- 调用概览: size, moveTo, resizeTo, info, print, getWindowsWithTitle
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：&&% IDLE窗口置右上。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### r()
- 说明: （无）
- 参数: （无）
- 调用概览: set_idle_window_to_top_right
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### place_obs_bottom_right()
- 说明: 将 OBS Studio 主窗口移动到屏幕右下角，并缩放为屏幕宽高的一半。
- 邻近注释: 控制OBS窗口在右下角 | &&% OBS窗口置右下
- 参数: （无）
- 返回推断: None
- 关注点: 文件, 时间/等待, 选择集
- 调用概览: print, size, moveTo, sleep, resizeTo, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：将 OBS Studio 主窗口移动到屏幕右下角，并缩放为屏幕宽高的一半。。邻近注释提示：控制OBS窗口在右下角；&&% OBS窗口置右下。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### r2()
- 说明: （无）
- 参数: （无）
- 调用概览: place_obs_bottom_right
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### minimize_window(window_keyword)
- 说明: 通用：最小化第一个标题包含 window_keyword 的可见窗口。
- 邻近注释: &&% 最小化指定窗口
- 参数: window_keyword
- 返回推断: bool
- 关注点: 选择集
- 调用概览: print, minimize, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：通用：最小化第一个标题包含 window_keyword 的可见窗口。。邻近注释提示：&&% 最小化指定窗口。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### maximize_autocad_window(window_keyword)
- 说明: 强制最大化第一个标题包含 window_keyword 的可见窗口。
- 邻近注释: &&% 最大化CAD窗口
- 参数: window_keyword
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待, 窗口/输入, 选择集
- 调用概览: sleep, info, ShowWindow, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：强制最大化第一个标题包含 window_keyword 的可见窗口。。邻近注释提示：&&% 最大化CAD窗口。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### start_obs_recording_by_click(x, y, button, clicks, move_duration)
- 说明: 通过鼠标点击屏幕上 (x,y) 坐标来控制 OBS 开始/停止录制。
- 邻近注释: &&% 点击开始OBS录制
- 参数: x, y, button, clicks, move_duration
- 关注点: 文件, 日志/测试
- 调用概览: moveTo, click, info
- 理解: 主要用于保存/写入相关逻辑。依据注释：通过鼠标点击屏幕上 (x,y) 坐标来控制 OBS 开始/停止录制。。邻近注释提示：&&% 点击开始OBS录制。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### fs(x1, y1)
- 说明: 微信调到0.5窗口
- 邻近注释: &&&% *** 录屏 | &&% 发送微信
- 参数: x1, y1
- 关注点: 文件
- 调用概览: moveTo, click, press
- 理解: 主要用于处理相关逻辑。依据注释：微信调到0.5窗口。邻近注释提示：&&&% *** 录屏；&&% 发送微信。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### xuanqun(x1, y1, neirong)
- 说明: （无）
- 邻近注释: &&% 选微信群
- 参数: x1, y1, neirong
- 关注点: 文件, 时间/等待
- 调用概览: copy_to_clipboard, moveTo, click, sleep, activate_window_by_title, hotkey, press
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 选微信群。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### copy_to_clipboard(text)
- 说明: 将传入的 text 文本写入系统剪贴板，供后续右键→粘贴使用。
- 邻近注释: &&% 复制到剪贴板
- 参数: text
- 关注点: UI/Tk, 文件
- 调用概览: Tk, withdraw, clipboard_clear, clipboard_append, update, destroy
- 理解: 主要用于移动/复制相关逻辑。依据注释：将传入的 text 文本写入系统剪贴板，供后续右键→粘贴使用。。邻近注释提示：&&% 复制到剪贴板。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### xieweixin(x1, y1, neirong)
- 说明: （无）
- 邻近注释: &&% 写微信
- 参数: x1, y1, neirong
- 关注点: 文件, 时间/等待
- 调用概览: copy_to_clipboard, sleep, moveTo, activate_window_by_title, click, hotkey
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 写微信。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### 主操作函数()
- 说明: （无）
- 邻近注释: &&% 主操作函数
- 参数: （无）
- 关注点: 时间/等待
- 调用概览: restore_and_position, sleep, activate_window_by_title, xuanqun, click_and_find_image_shape, click, xieweixin, fs
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 主操作函数。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### main_func(folder_path)
- 说明: （无）
- 邻近注释: &&% 主函数入口
- 参数: folder_path
- 调用概览: 打印输出PDF
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 主函数入口。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### luping(main_func, *args, **kwargs)
- 说明: 1) 开始 OBS 录制  
- 邻近注释: &&% 录屏
- 参数: main_func, *args, **kwargs
- 关注点: 文件, 时间/等待
- 调用概览: minimize_all_windows_d, restore_and_position, sleep, activate_window_by_title, moveTo, click, main_func, print
- 理解: 主要用于处理相关逻辑。依据注释：1) 开始 OBS 录制  。邻近注释提示：&&% 录屏。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### 魔方()
- 说明: （无）
- 邻近注释: &&% 魔方
- 参数: （无）
- 调用概览: 魔方控制台
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 魔方。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### run_py(pyname)
- 说明: （无）
- 邻近注释: &&% 运行Python脚本
- 参数: pyname
- 关注点: 日志/测试, 进程
- 调用概览: run, info
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 运行Python脚本。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### focus_cmdline(cmd_x, cmd_y, delay)
- 说明: 把鼠标移到命令行并单击，确保焦点回到 AutoCAD 命令栏。
- 邻近注释: &&% 聚焦命令行
- 参数: cmd_x, cmd_y, delay
- 关注点: 文件
- 调用概览: moveTo, click
- 理解: 主要用于处理相关逻辑。依据注释：把鼠标移到命令行并单击，确保焦点回到 AutoCAD 命令栏。。邻近注释提示：&&% 聚焦命令行。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### activate_window_by_title(title, click_titlebar)
- 说明: 激活一个指定标题的窗口。
- 邻近注释: &&% 激活窗口和子窗口
- 参数: title, click_titlebar
- 返回推断: bool,tuple
- 关注点: 日志/测试, 时间/等待, 窗口/输入, 选择集
- 调用概览: info, restore, sleep, activate, click, getWindowsWithTitle, ShowWindow, SetForegroundWindow, max, min
- 理解: 主要用于处理相关逻辑。依据注释：激活一个指定标题的窗口。。邻近注释提示：&&% 激活窗口和子窗口。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### click_in_window(title, offset_x, offset_y, click_titlebar)
- 说明: 在指定窗口的某个相对像素位置点击一次（相对于窗口左上角的偏移量）。
- 邻近注释: &&% 窗口内点击
- 参数: title, offset_x, offset_y, click_titlebar
- 返回推断: bool
- 关注点: 文件, 日志/测试, 时间/等待, 窗口/输入, 选择集
- 调用概览: int, moveTo, click, sleep, info, restore, activate, getWindowsWithTitle, ShowWindow, SetForegroundWindow
- 理解: 主要用于处理相关逻辑。依据注释：在指定窗口的某个相对像素位置点击一次（相对于窗口左上角的偏移量）。。邻近注释提示：&&% 窗口内点击。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### activate_and_click_aikeyun()
- 说明: （无）
- 邻近注释: &&% 激活并点击艾可云
- 参数: （无）
- 关注点: 文件, 时间/等待
- 调用概览: activate_window_by_title, moveTo, click, sleep
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 激活并点击艾可云。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### drag_in_window_simple(title, start, offset, duration, button, absolute_start)
- 说明: 拖拽函数，支持相对或绝对起点：
- 邻近注释: &&% 窗口内简单拖拽
- 参数: title, start, offset, duration, button, absolute_start
- 关注点: 文件, 日志/测试, 时间/等待
- 调用概览: activate_window_by_title, moveTo, mouseDown, mouseUp, sleep, info
- 理解: 主要用于处理相关逻辑。依据注释：拖拽函数，支持相对或绝对起点：。邻近注释提示：&&% 窗口内简单拖拽。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### run_auto_explode_area(x1, y1, x2, y2, cmd_x, cmd_y, delay)
- 说明: 这是一个未使用pywin32API控制天正CAD的典型函数
- 邻近注释: &&% 纯窗口操作炸开区域内对象
- 参数: x1, y1, x2, y2, cmd_x, cmd_y, delay
- 关注点: 文件, 进程
- 调用概览: with_name, str, run, print, Path
- 理解: 主要用于计算/测量相关逻辑。依据注释：这是一个未使用pywin32API控制天正CAD的典型函数。邻近注释提示：&&% 纯窗口操作炸开区域内对象。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### list_all_windows()
- 说明: （无）
- 邻近注释: &&% 列出所有窗口
- 参数: （无）
- 关注点: 日志/测试, 选择集
- 调用概览: getWindowsWithTitle, print, info
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 列出所有窗口。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### minimize_window(window_keyword)
- 说明: 通用：最小化第一个标题包含 window_keyword 的可见窗口。
- 邻近注释: 最小、最大化窗口
- 参数: window_keyword
- 返回推断: bool
- 关注点: 选择集
- 调用概览: print, minimize, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：通用：最小化第一个标题包含 window_keyword 的可见窗口。。邻近注释提示：最小、最大化窗口。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### maximize_autocad_window(window_keyword)
- 说明: 强制最大化第一个标题包含 window_keyword 的可见窗口。
- 参数: window_keyword
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待, 窗口/输入, 选择集
- 调用概览: sleep, info, ShowWindow, getWindowsWithTitle
- 理解: 主要用于处理相关逻辑。依据注释：强制最大化第一个标题包含 window_keyword 的可见窗口。。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### set_dwg_units_precision()
- 说明: 设置当前 DWG 文件的单位及精度：
- 邻近注释: &&% 设置单位精度
- 参数: （无）
- 关注点: COM, 日志/测试
- 关键调用: C.doc
- 调用概览: SetVariable, print, info
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置当前 DWG 文件的单位及精度：。邻近注释提示：&&% 设置单位精度。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### jd()
- 说明: （无）
- 参数: （无）
- 调用概览: set_dwg_units_precision
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### list_dim_styles()
- 说明: 列出当前 DWG 文件中所有标注样式名称。
- 邻近注释: &&% 列出标注样式
- 参数: （无）
- 返回推断: list,object
- 关注点: 日志/测试
- 调用概览: print, info, Item, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：列出当前 DWG 文件中所有标注样式名称。。邻近注释提示：&&% 列出标注样式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_current_dimstyle_via_command(style_name)
- 说明: 使用命令行方式设置当前标注样式，兼容天正。
- 邻近注释: &&% 设置当前标注样式
- 参数: style_name
- 关注点: COM, 日志/测试
- 调用概览: SendCommand, info
- 理解: 主要用于更新/设置相关逻辑。依据注释：使用命令行方式设置当前标注样式，兼容天正。。邻近注释提示：&&% 设置当前标注样式。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_current_text_style(style_name)
- 说明: 设置当前文字样式（通过 COM 接口方式）。
- 邻近注释: &&% 设置当前文字样式
- 参数: style_name
- 关注点: 日志/测试
- 调用概览: Item, info
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置当前文字样式（通过 COM 接口方式）。。邻近注释提示：&&% 设置当前文字样式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### huoqu_ziti_style()
- 说明: （无）
- 邻近注释: &&% 获取字体样式
- 参数: （无）
- 返回推断: object
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 获取字体样式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### create_text_style(sty_name, ziti)
- 说明: 在当前 DWG 中创建（或更新）一个中文文字样式。
- 邻近注释: &&% 创建文字样式
- 参数: sty_name, ziti
- 关注点: COM, 日志/测试
- 调用概览: Item, info, SetFont, Add
- 理解: 主要用于创建/插入相关逻辑。依据注释：在当前 DWG 中创建（或更新）一个中文文字样式。。邻近注释提示：&&% 创建文字样式。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_text_style_onlyshx(style_name, font_file, big_font_file)
- 说明: C:/Program Files/Autodesk/AutoCAD 2021/Fonts查找可用shx字体    
- 邻近注释: &&% 设置SHX文字样式
- 参数: style_name, font_file, big_font_file
- 返回推断: bool
- 关注点: COM, 日志/测试, 进程
- 调用概览: EnsureDispatch, info, Item, Add, isinstance
- 理解: 主要用于更新/设置相关逻辑。依据注释：C:/Program Files/Autodesk/AutoCAD 2021/Fonts查找可用shx字体    。邻近注释提示：&&% 设置SHX文字样式。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_text_style(style_name, font_file, big_font_file)
- 说明: 设置CAD中文字样式：英文shx文件 + 中文大字体文件
- 邻近注释: &&% 设置文字样式
- 参数: style_name, font_file, big_font_file
- 返回推断: bool
- 关注点: 日志/测试
- 调用概览: info, Item, Add
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置CAD中文字样式：英文shx文件 + 中文大字体文件。邻近注释提示：&&% 设置文字样式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### rename_conflicting_text_styles(file1_path, file2_path, suffix, retry_delay, max_retries)
- 说明: 在两个 DWG 中找出同名（用户）文字样式，
- 邻近注释: &&% 重命名冲突文字样式
- 参数: file1_path, file2_path, suffix, retry_delay, max_retries
- 返回推断: None
- 关注点: COM, 文件, 日志/测试, 时间/等待, 进程
- 调用概览: EnsureDispatch, Open, abspath, info, Save, Close, print, SendCommand, range, discard, add, sleep...
- 理解: 主要用于更新/设置相关逻辑。依据注释：在两个 DWG 中找出同名（用户）文字样式，。邻近注释提示：&&% 重命名冲突文字样式。实现特征：执行 DWG 打开；执行保存；执行关闭文档；通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### transfer_props_by_matchprop(entity, Ob, max_try, delay)
- 说明: （无）
- 邻近注释: 将一个对象属性传给多个对象 | &&% 格式刷属性传递
- 参数: entity, Ob, max_try, delay
- 返回推断: None,bool,tuple
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 调用概览: chr, li, GetBoundingBox, expand_rectangle, range, info, sleep, SendCommand, wait_idle, GetAcadState, abs, highlight_entity_by_bbox...
- 理解: 主要用于处理相关逻辑。邻近注释提示：将一个对象属性传给多个对象；&&% 格式刷属性传递。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### run_dual_threads_1(f1, f2, f1_args, f1_kwargs, f2_args, f2_kwargs, timeout_sec)
- 说明: 通用“双线程-GUI”调度器
- 邻近注释: &&% 双线程生成器 | &&% 双线程运行1
- 参数: f1, f2, f1_args, f1_kwargs, f2_args, f2_kwargs, timeout_sec
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 调用概览: Event, Thread, time, start, join, is_set, set, info, print
- 理解: 主要用于打开/读取相关逻辑。依据注释：通用“双线程-GUI”调度器。邻近注释提示：&&% 双线程生成器；&&% 双线程运行1。实现特征：通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### cancel_cad_selection(attempts, delay)
- 说明: （无）
- 邻近注释: &&% 取消CAD选择
- 参数: attempts, delay
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待
- 调用概览: range, print, highlight_entities_in_window, info, sleep
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：&&% 取消CAD选择。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### close_wps_window_by_click(title_keyword, offset_x, offset_y, pause_before)
- 说明: 在标题包含 title_keyword 的窗口右上角点击一次（×），尝试关闭该窗口。
- 邻近注释: &&&% 打印辅助
- 参数: title_keyword, offset_x, offset_y, pause_before
- 返回推断: bool
- 关注点: 时间/等待, 窗口/输入, 选择集
- 调用概览: EnumWindows, GetWindowRect, sleep, click, node, IsWindowVisible, GetWindowText, lower, append
- 理解: 主要用于关闭/终止相关逻辑。依据注释：在标题包含 title_keyword 的窗口右上角点击一次（×），尝试关闭该窗口。。邻近注释提示：&&&% 打印辅助。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### min_w()
- 说明: （无）
- 邻近注释: &&&% 测试辅助 | &&% 最小化窗口
- 参数: （无）
- 关注点: 窗口/输入
- 调用概览: keybd_event
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&&% 测试辅助；&&% 最小化窗口。
- 风险: 依赖窗口/输入焦点，易受环境影响
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境

### ql()
- 说明: （无）
- 邻近注释: &&% 清除测试图层
- 参数: （无）
- 调用概览: ensure_layer
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 清除测试图层。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### srhd(*args)
- 说明: 在模型空间绘制点并标注序号，支持以下调用形式：
- 邻近注释: &&% 模型空间画点
- 参数: *args
- 返回推断: None,str
- 关注点: COM, 几何, 日志/测试
- 调用概览: enumerate, Item, len, isinstance, Add, info, print, vtpnt, AddPoint, AddText, all, str
- 理解: 主要用于处理相关逻辑。依据注释：在模型空间绘制点并标注序号，支持以下调用形式：。邻近注释提示：&&% 模型空间画点。实现特征：创建文字对象；创建点对象；涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### srhd_p(*args)
- 说明: 在图纸空间绘制点和编号，支持：
- 邻近注释: &&% 图纸空间画点
- 参数: *args
- 返回推断: None,str
- 关注点: COM, 几何, 日志/测试
- 调用概览: enumerate, Item, len, isinstance, Add, info, print, vtpnt, AddPoint, AddText, all, str
- 理解: 主要用于处理相关逻辑。依据注释：在图纸空间绘制点和编号，支持：。邻近注释提示：&&% 图纸空间画点。实现特征：创建文字对象；创建点对象；涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### comtomath(LBcom)
- 说明: （无）
- 邻近注释: &&% COM点转数学点
- 参数: LBcom
- 返回推断: object
- 调用概览: range, len, append
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% COM点转数学点。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### p()
- 说明: （无）
- 参数: （无）
- 返回推断: object
- 调用概览: li, pmxz, comtomath, print
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### fuzhi_chakan(LBcom, K)
- 说明: （无）
- 邻近注释: &&% 隔远查看 | &&% 复制查看
- 参数: LBcom, K
- 返回推断: object
- 关注点: COM, 文件, 日志/测试
- 调用概览: Copy, vtpnt, Move, append, info
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 隔远查看；&&% 复制查看。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### celiang_wenzichangdu(TEXTCOM)
- 说明: （无）
- 邻近注释: &&% 测量文字长度
- 参数: TEXTCOM
- 返回推断: object
- 关注点: 几何, 文件
- 调用概览: Copy, vtpnt, abs, Delete
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 测量文字长度。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### celiang_wenzichangdu_write(ZF, style, height, scalefactor)
- 说明: （无）
- 邻近注释: 测量新写文字长度 | &&% 写入并测量文字长度
- 参数: ZF, style, height, scalefactor
- 返回推断: object
- 关注点: COM, 文件
- 调用概览: AddText, celiang_wenzichangdu, Delete, vtpnt
- 理解: 主要用于保存/写入相关逻辑。邻近注释提示：测量新写文字长度；&&% 写入并测量文字长度。实现特征：创建文字对象。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### qingkong_wenjianjia(FolderPath)
- 说明: （无）
- 邻近注释: 清空文件夹 | &&% 清空文件夹
- 参数: FolderPath
- 关注点: 文件, 日志/测试
- 调用概览: listdir, join, isfile, info, remove
- 理解: 主要用于处理相关逻辑。邻近注释提示：清空文件夹；&&% 清空文件夹。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### get_bbox_info(com_obj)
- 说明: 获取传入 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）的外包盒信息，
- 邻近注释: &&% 返回对象外包盒的长，宽，横竖向，角点信息 | &&% 获取包围盒信息
- 参数: com_obj
- 返回: (length, width, orientation)
- 关注点: 几何, 日志/测试
- 调用概览: max, min, GetBoundingBox, info
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取传入 AutoCAD COM 对象（如 Line、Circle、BlockReference 等）的外包盒信息，。邻近注释提示：&&% 返回对象外包盒的长，宽，横竖向，角点信息；&&% 获取包围盒信息。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### bbox_orientation_flag(com_obj)
- 说明: 判断任意 COM 对象的外包盒是竖向、横向还是正方形：
- 邻近注释: &&% 包围盒方向标志
- 参数: com_obj
- 返回: int -- 竖向返回 1，横向或正方形返回 0
- 关注点: 几何
- 调用概览: GetBoundingBox, abs
- 理解: 主要用于处理相关逻辑。依据注释：判断任意 COM 对象的外包盒是竖向、横向还是正方形：。邻近注释提示：&&% 包围盒方向标志。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### group_bbox_corners(com_objs, max_retry, delay)
- 说明: 【通用加强版】计算一组 COM 对象的整体外包盒，并按顺序返回四个角点。
- 邻近注释: &&% 获取多个对象的外包盒数据
- 参数: com_objs, max_retry, delay
- 返回: 四元组：(左下, 右上, 左上, 右下)
- 关注点: COM, 几何, 文件, 时间/等待
- 调用概览: float, range, Update, GetBoundingBox, hasattr, list, sleep
- 理解: 主要用于处理相关逻辑。依据注释：【通用加强版】计算一组 COM 对象的整体外包盒，并按顺序返回四个角点。。邻近注释提示：&&% 获取多个对象的外包盒数据。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### bbox_center_2(e)
- 说明: （无）
- 邻近注释: &&% 从两点绘制矩形 | &&% 包围盒中心2D
- 参数: e
- 返回推断: tuple
- 关注点: 几何
- 调用概览: GetBoundingBox, tuple
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 从两点绘制矩形；&&% 包围盒中心2D。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### bbox_center_3(ent)
- 说明: 返回实体外包盒中心 (cx, cy, cz)
- 邻近注释: &&% 包围盒中心3D
- 参数: ent
- 返回推断: tuple
- 关注点: 几何
- 调用概览: GetBoundingBox
- 理解: 主要用于处理相关逻辑。依据注释：返回实体外包盒中心 (cx, cy, cz)。邻近注释提示：&&% 包围盒中心3D。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### safe_get_bbox(ent, max_retry, delay)
- 说明: 【通用加强版】安全获取 AutoCAD 图元外包盒 (GetBoundingBox)
- 邻近注释: &&% 安全获取包围盒
- 参数: ent, max_retry, delay
- 返回: (min_point, max_point) 元组，坐标为 (x, y, z)。
- 关注点: COM, 几何, 日志/测试, 时间/等待
- 调用概览: range, Update, GetBoundingBox, hasattr, list, sleep
- 理解: 主要用于获取/选择相关逻辑。依据注释：【通用加强版】安全获取 AutoCAD 图元外包盒 (GetBoundingBox)。邻近注释提示：&&% 安全获取包围盒。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### resolve_log_level(local_setting)
- 说明: 解析日志等级: 参数 > 全局
- 参数: local_setting
- 返回推断: object
- 调用概览: int
- 理解: 主要用于处理相关逻辑。依据注释：解析日志等级: 参数 > 全局。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_data_root()
- 说明: 获取数据存储根目录
- 邻近注释: ======================================================== | 1. 基础配置与连接模块 | ========================================================
- 参数: （无）
- 返回推断: object,str
- 关注点: 文件
- 调用概览: get, exists
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取数据存储根目录。邻近注释提示：========================================================；1. 基础配置与连接模块；========================================================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### _resolve_json_path(file_input, folder_name)
- 说明: 统一路径解析工具
- 参数: file_input, folder_name
- 返回推断: object
- 关注点: COM, 文件
- 关键调用: C.doc
- 调用概览: get_data_root, join, exists, makedirs, str, endswith, splitext, lower, Dispatch
- 理解: 主要用于处理相关逻辑。依据注释：统一路径解析工具。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### extract_poly_data(poly_obj)
- 说明: 【存储】提取多段线数据 (改为 getattr 安全读取)
- 邻近注释: ======================================================== | 2. 核心数据处理：提取与自适应恢复 | ========================================================
- 参数: poly_obj
- 返回推断: NoneType,object
- 关注点: COM, 日志/测试
- 调用概览: getattr, endswith, list
- 理解: 主要用于处理相关逻辑。依据注释：【存储】提取多段线数据 (改为 getattr 安全读取)。邻近注释提示：========================================================；2. 核心数据处理：提取与自适应恢复；========================================================。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### restore_poly_adaptive(data_dict)
- 说明: 【加载】自适应恢复 (改为 set_attr 安全赋值)
- 参数: data_dict
- 返回推断: NoneType,object
- 关注点: COM, 文件, 日志/测试
- 关键调用: C.doc
- 调用概览: get, VARIANT, AddLightWeightPolyline, HandleToObject, getattr, float, pop, globals, set_attr, info, len, Dispatch
- 理解: 主要用于处理相关逻辑。依据注释：【加载】自适应恢复 (改为 set_attr 安全赋值)。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### save_poly_list(poly_list, file_name)
- 说明: 保存多段线列表到 JSON
- 邻近注释: ======================================================== | 3. 业务功能：多段线列表存取 | ========================================================
- 参数: poly_list, file_name
- 返回推断: bool
- 关注点: 文件, 日志/测试
- 调用概览: ensure_list, _resolve_json_path, extract_poly_data, info, append, open, dump, basename
- 理解: 主要用于保存/写入相关逻辑。依据注释：保存多段线列表到 JSON。邻近注释提示：========================================================；3. 业务功能：多段线列表存取；========================================================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### load_poly_list(file_name)
- 说明: 加载 JSON 并恢复多段线列表
- 参数: file_name
- 返回推断: list,object
- 关注点: 文件, 日志/测试
- 调用概览: _resolve_json_path, exists, print, info, open, load, restore_poly_adaptive, append, len
- 理解: 主要用于打开/读取相关逻辑。依据注释：加载 JSON 并恢复多段线列表。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### save_ctq(ctq_data, file_name)
- 说明: 【功能】: 保存 (polys, blocks, mapping) 到 JSON。
- 邻近注释: ======================================================== | 4. 业务功能：CTQ (图签系统) 存取 | ========================================================
- 参数: ctq_data, file_name
- 返回推断: bool
- 关注点: COM, 文件
- 调用概览: sorted, _resolve_json_path, getattr, keys, get, len, extract_poly_data, append, open, dump
- 理解: 主要用于保存/写入相关逻辑。依据注释：【功能】: 保存 (polys, blocks, mapping) 到 JSON。。邻近注释提示：========================================================；4. 业务功能：CTQ (图签系统) 存取；========================================================。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### load_ctq(file_name, verbose)
- 说明: 【功能】: 加载 JSON -> 恢复对象 -> 生成 CTQ
- 参数: file_name, verbose
- 返回推断: tuple
- 关注点: COM, 文件
- 关键调用: C.doc
- 调用概览: _resolve_json_path, enumerate, exists, globals, li, get, restore_poly_adaptive, sort_coms_by_llcorner, append, getattr, open, load...
- 理解: 主要用于打开/读取相关逻辑。依据注释：【功能】: 加载 JSON -> 恢复对象 -> 生成 CTQ。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### Redefine_standard_blocks(source_file, target_file)
- 说明: 【函数编号】: BLOCK-UPDATE-001
- 参数: source_file, target_file
- 关注点: 文件, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: get, info, print, ValueError, join, open_file, wait_command_done, insert_file_exploded, close_file, batch_attsync_loop, select_kuai, RuntimeError...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: BLOCK-UPDATE-001。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### get_sorted_titles_by_areas_final(layer_name)
- 说明: 【最终重命名版】
- 参数: layer_name
- 返回推断: object
- 关注点: COM, 几何, 文件, 日志/测试, 选择集
- 关键调用: C.li
- 调用概览: li, select_print_areas_maxrect_from_polylines, info, enumerate, select_entities_in_window, generate_name_and_ratio_from_com, print, GetBoundingBox, sort_coms_by_llcorner, len, set_attr, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：【最终重命名版】。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### get_sorted_titles_ce(layer_name)
- 说明: 【最终重命名版】
- 参数: layer_name
- 返回推断: object
- 关注点: COM, 几何, 文件, 日志/测试, 选择集
- 关键调用: C.li
- 调用概览: li, select_print_areas_maxrect_from_polylines, info, enumerate, select_objects_in_window_area, generate_name_and_ratio_from_com, print, GetBoundingBox, sort_coms_by_llcorner, len, set_attr, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：【最终重命名版】。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### batch_attsync_loop(rounds, delay_per_cmd)
- 说明: 【函数编号】: CMD-002 (Select版)
- 邻近注释: &&% 编辑块生效的强化
- 参数: rounds, delay_per_cmd
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: info, range, sleep, Regen, print, select_kuai, items, get_attr, attsync_block_instance
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: CMD-002 (Select版)。邻近注释提示：&&% 编辑块生效的强化。包含选择集构造或过滤。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；超时与重试次数边界

### smart_select_polylines(layout_name, operate_target, select_config, use_cache, min_side)
- 说明: 【函数编号】: CACHE-LAYER-001 (智能缓存选择器 - V12.1 参数优化版)
- 参数: layout_name, operate_target, select_config, use_cache, min_side
- 返回推断: object
- 关注点: 几何, 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: universal_select_polylines, info, log, load_poly_list, save_poly_list, splitext, int, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: CACHE-LAYER-001 (智能缓存选择器 - V12.1 参数优化版)。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### universal_select_polylines(layout_name, operate_target, select_config, min_side)
- 说明: 【函数编号】: SELECT-UNIFIED-002 (V12.1 - 综合分发器)
- 参数: layout_name, operate_target, select_config, min_side
- 返回推断: list,object
- 关注点: 几何, 日志/测试, 选择集
- 调用概览: info, select_print_areas_paperspace, print, select_maxrect_polylines_1
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-UNIFIED-002 (V12.1 - 综合分发器)。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_print_areas_maxrect_from_polylines(**kwargs)
- 说明: 【兼容层】旧参数 lm, duanbian, tol_single 等已被 kwargs 自动吃掉并忽略。
- 参数: **kwargs
- 返回推断: object
- 关注点: 几何, 选择集
- 调用概览: select_maxrect_polylines_1
- 理解: 主要用于获取/选择相关逻辑。依据注释：【兼容层】旧参数 lm, duanbian, tol_single 等已被 kwargs 自动吃掉并忽略。。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_maxrect_polylines_1(layer_name, precision_mode, width, color, min_side, **kwargs)
- 说明: 【V12.0 步进式审计版】
- 参数: layer_name, precision_mode, width, color, min_side, **kwargs
- 返回推断: tuple
- 关注点: COM, 几何, 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: get, set_space_mode, remove_duplicate_polylines, info, sort_coms_by_llcorner, get_rectangular_polylines, enumerate, Regen, globals, error, warning, max...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【V12.0 步进式审计版】。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### select_print_areas_paperspace(layout_name, layer_name, precision_mode, width, color, min_side, **kwargs)
- 说明: 【函数编号】: SEL-PAPER-002 (V16.4 - 抗干扰增强版)
- 邻近注释: &&% 图纸空间打印区域的选择 | 20260116
- 参数: layout_name, layer_name, precision_mode, width, color, min_side, **kwargs
- 返回推断: tuple
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: get, info, range, get_layout_rectangular_polylines_coords, enumerate, remove_duplicate_polylines, sort_coms_by_llcorner, set_space_mode, error, Item, warning, min...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SEL-PAPER-002 (V16.4 - 抗干扰增强版)。邻近注释提示：&&% 图纸空间打印区域的选择；20260116。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### select_standard_print_areas(lm, layer_name, tol_single, cha_Y, mute_logs)
- 说明: 【函数编号】: RECOG-002
- 参数: lm, layer_name, tol_single, cha_Y, mute_logs
- 返回推断: NoneType,list,object,tuple
- 关注点: COM, 几何, 文件, 选择集
- 调用概览: li, log, get, enumerate, ensure_layer, stc, len, print, isinstance, getattr, get_attr_safe, list...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: RECOG-002。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### select_print_areas_from_blocks(block_layers, rect_layer, width, color, z, cha_Y, debug)
- 说明: 【函数编号】: RECOG-003
- 参数: block_layers, rect_layer, width, color, z, cha_Y, debug
- 返回推断: tuple
- 关注点: COM, 几何, 文件, 选择集
- 调用概览: li, get, log, set, sort_coms_by_llcorner, ensure_layer, stc, len, print, isinstance, globals, select_kuai_func...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: RECOG-003。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### select_print_areas_from_layer(source_layer, rect_layer, width, color, z, cha_Y, debug)
- 说明: 【函数编号】: RECOG-004
- 参数: source_layer, rect_layer, width, color, z, cha_Y, debug
- 返回推断: tuple
- 关注点: COM, 几何, 文件, 选择集
- 调用概览: li, log, get, sort_coms_by_llcorner, stc, remove_duplicate_polylines, len, print, ensure_layer, isinstance, globals, draw_func...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: RECOG-004。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### select_print_areas_from_screen(rect_layer, width, color, z, cha_Y, debug)
- 说明: 【函数编号】: RECOG-005
- 参数: rect_layer, width, color, z, cha_Y, debug
- 返回推断: tuple
- 关注点: COM, 几何, 文件, 选择集
- 调用概览: li, log, get, sort_coms_by_llcorner, pmxz, len, ensure_layer, stc, print, isinstance, globals, draw_func...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: RECOG-005。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### check_valid_rect_pro(raw_ent, verbose)
- 说明: 【辅助函数】矩形有效性深度检查
- 参数: raw_ent, verbose
- 返回推断: tuple
- 关注点: 文件, 日志/测试
- 调用概览: getattr, log, int, info, _maybe_cast, globals, len
- 理解: 主要用于测试/校验相关逻辑。依据注释：【辅助函数】矩形有效性深度检查。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### remove_duplicate_polylines(polylines, tol, priority_layer)
- 说明: 【函数编号】: UTIL-CLEAN-001
- 邻近注释: &&% 对多段线去重处理
- 参数: polylines, tol, priority_layer
- 返回推断: object
- 关注点: 几何, 文件, 日志/测试
- 调用概览: lower, len, info, sort, range, GetBoundingBox, append, float, id, abs, safe_delete
- 理解: 主要用于删除/清理相关逻辑。依据注释：【函数编号】: UTIL-CLEAN-001。邻近注释提示：&&% 对多段线去重处理。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### universal_insert_labels_dispatch(layout_name, operate_target, Select_Config, manual_dy_list, filepath, layername, debug, ref_width, use_cache)
- 说明: （无）
- 参数: layout_name, operate_target, Select_Config, manual_dy_list, filepath, layername, debug, ref_width, use_cache
- 返回推断: bool
- 关注点: COM, 几何, 日志/测试, 时间/等待, 选择集
- 关键调用: wait_quiescent, C.doc, C.acad
- 调用概览: info, len, speak_msg, smart_select_polylines, isinstance, warning, float, insert_and_scale_labels_paper_space, insert_and_scale_labels_area_power, error, sleep, wait_quiescent...
- 理解: 主要用于创建/插入相关逻辑。实现特征：包含空闲等待以同步 CAD 状态。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### insert_and_scale_labels_area_power(coms_dayin, filepath, layername, timestamp, debug, layout_name, Ref_width, operate_target, **kwargs)
- 说明: 【函数编号】: BLOCK-INSERT-001 (V34 - 同文件直调版)
- 参数: coms_dayin, filepath, layername, timestamp, debug, layout_name, Ref_width, operate_target, **kwargs
- 返回推断: bool,object
- 关注点: 几何, 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: info, run_title_block_assembly_pipeline, join, select_maxrect_polylines_1, isinstance, error, get, str, warning, print_exc, Item, len
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: BLOCK-INSERT-001 (V34 - 同文件直调版)。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### insert_and_scale_labels_paper_space(dy, filepath, layername, layout_name, timestamp, debug, Ref_width, operate_target, **kwargs)
- 说明: 【函数编号】: BLOCK-INSERT-002 (V32 - 返回值解包修复版)
- 参数: dy, filepath, layername, layout_name, timestamp, debug, Ref_width, operate_target, **kwargs
- 返回推断: bool
- 关注点: 日志/测试, 选择集
- 关键调用: C.doc, C.acad
- 调用概览: info, wait_command_done, switch_to_layout, select_print_areas_paperspace, isinstance, insert_and_scale_labels_area_power, Regen, save_file, warning, print_exc, len
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: BLOCK-INSERT-002 (V32 - 返回值解包修复版)。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### clean_blocks_until_vanished(target_names, max_retry_loops)
- 说明: 【函数编号】: BLK-CLEAN-001
- 参数: target_names, max_retry_loops
- 返回推断: bool
- 关注点: 文件, 日志/测试, 选择集
- 调用概览: info, range, set, select_kuai, len, print, globals, delete_block_instances_and_definition_retry, get_attr, Item, add, list
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: BLK-CLEAN-001。实现特征：涉及块定义/块实例操作。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### plcoor_to_com(coord_info, layer_name, width, color)
- 说明: 根据坐标数据批量创建轻量多段线并返回 COM 对象列表。
- 邻近注释: &&% 坐标转多段线COM
- 参数: coord_info, layer_name, width, color
- 返回推断: object
- 关注点: COM
- 关键调用: C.doc
- 调用概览: set_attr, node, Item, VARIANT, AddLightWeightPolyline, append, len, Add, extend
- 理解: 主要用于处理相关逻辑。依据注释：根据坐标数据批量创建轻量多段线并返回 COM 对象列表。。邻近注释提示：&&% 坐标转多段线COM。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### draw_pl_and_extract_info(resu, layer_name, width, color)
- 说明: resu: List[(blk_entity, corners)]
- 邻近注释: &&% 绘制PL并提取信息
- 参数: resu, layer_name, width, color
- 返回推断: object
- 关注点: COM, 几何, 时间/等待
- 关键调用: C.doc
- 调用概览: enumerate, sleep, Item, set_attr, VARIANT, AddLightWeightPolyline, print_com_info, SendCommand, Add, extend, generate_name_and_ratio_from_polyline, get_attr...
- 理解: 主要用于创建/插入相关逻辑。依据注释：resu: List[(blk_entity, corners)]。邻近注释提示：&&% 绘制PL并提取信息。实现特征：涉及图层操作；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### draw_pl_and_extract_from_entities(entities, layer_name, width, color, A3dy, Fandy)
- 说明: 把 entities 统一转换为闭合多段线，并提取图幅 / 比例 / 规格信息。
- 邻近注释: &&% 从实体绘制PL并提取
- 参数: entities, layer_name, width, color, A3dy, Fandy
- 返回推断: object
- 关注点: COM, 时间/等待
- 关键调用: C.doc
- 调用概览: plcoor_to_com, enumerate, sleep, append, zip, print_com_info, SendCommand, hasattr, GetBoundingBox, get_attr, generate_name_and_ratio_from_com, len
- 理解: 主要用于创建/插入相关逻辑。依据注释：把 entities 统一转换为闭合多段线，并提取图幅 / 比例 / 规格信息。。邻近注释提示：&&% 从实体绘制PL并提取。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### insert_block_into_poly_area(block_name, poly_ent, k, max_retries)
- 说明: 在多段线/多边形 poly_ent 所定义区域内插入已定义块，
- 邻近注释: &&% 区域内插入块
- 参数: block_name, poly_ent, k, max_retries
- 返回推断: tuple
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 调用概览: li, GetBoundingBox, VARIANT, range, hasattr, TypeError, RuntimeError, InsertBlock, set_attr, info, sleep, print
- 理解: 主要用于创建/插入相关逻辑。依据注释：在多段线/多边形 poly_ent 所定义区域内插入已定义块，。邻近注释提示：&&% 区域内插入块。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### insert_block_into_poly_area(block_name, poly_ent, k, max_retries)
- 说明: 【修正版 V2】自动识别 poly_ent 所在空间（模型或布局），直接使用 C.doc。
- 邻近注释: &&% 区域内插入块20260109
- 参数: block_name, poly_ent, k, max_retries
- 返回推断: tuple
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 关键调用: C.doc
- 调用概览: GetBoundingBox, VARIANT, range, hasattr, TypeError, RuntimeError, ObjectIdToObject, info, InsertBlock, set_attr, sleep, print
- 理解: 主要用于创建/插入相关逻辑。依据注释：【修正版 V2】自动识别 poly_ent 所在空间（模型或布局），直接使用 C.doc。。邻近注释提示：&&% 区域内插入块20260109。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### compute_insert_factors(entities, res, result_dict)
- 说明: 根据 res 的 ratio/spec 与 result_dict（图签模板信息）的块定义，计算缩放系数 k。
- 邻近注释: &&% 计算插入因子
- 参数: entities, res, result_dict
- 返回推断: object
- 调用概览: match, get, next, append, int, values, _denom, group
- 理解: 主要用于创建/插入相关逻辑。依据注释：根据 res 的 ratio/spec 与 result_dict（图签模板信息）的块定义，计算缩放系数 k。。邻近注释提示：&&% 计算插入因子。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_factor_for_entity(entity, factors)
- 说明: 在 factors 中找到第一项为 entity 的元组。
- 邻近注释: &&% 获取实体因子
- 参数: entity, factors
- 返回推断: NoneType,object
- 理解: 主要用于获取/选择相关逻辑。依据注释：在 factors 中找到第一项为 entity 的元组。。邻近注释提示：&&% 获取实体因子。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### insert_company_label_common_block(insertion_point, filepath, scale, rotation, wait)
- 说明: 直接插入“公司通用图签块”DWG，并炸开，生成外包盒多段线信息。
- 邻近注释: 插入公司通用图签块（单线程） | ============================= | &&% 插入公司通用图签单线程
- 参数: insertion_point, filepath, scale, rotation, wait
- 返回: (coms_tuqian, names_tuqian, info_dict)
- 关注点: 时间/等待
- 关键调用: C.li
- 调用概览: li, insert_and_explode_dwg, draw_pl_and_extract_info, append, sleep, save_file, get_attr
- 理解: 主要用于创建/插入相关逻辑。依据注释：直接插入“公司通用图签块”DWG，并炸开，生成外包盒多段线信息。。邻近注释提示：插入公司通用图签块（单线程）；=============================；&&% 插入公司通用图签单线程。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### f1_insert_company_getwindow(timeout_event, done_event)
- 说明: 线程1：插入公司图签块，并将结果写入 result_box['data']。
- 邻近注释: 双线程：忽略 SHX 字体对话框 | ============================= | &&% 线程1:插入公司图签
- 参数: timeout_event, done_event
- 关注点: COM, 时间/等待
- 调用概览: CoInitialize, node, li, insert_company_label_common_block, wait, CoUninitialize, set, print, format_exc
- 理解: 主要用于创建/插入相关逻辑。依据注释：线程1：插入公司图签块，并将结果写入 result_box['data']。。邻近注释提示：双线程：忽略 SHX 字体对话框；=============================；&&% 线程1:插入公司图签。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### _find_shx_dialog(shx_titles)
- 说明: 查找“缺少 SHX 字体”对话框窗口句柄。
- 参数: shx_titles
- 返回推断: object
- 关注点: 窗口/输入, 选择集
- 调用概览: EnumWindows, GetWindowText, any, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：查找“缺少 SHX 字体”对话框窗口句柄。。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境

### _ignore_shx_dialog(hwnd)
- 说明: 向“缺少 SHX 字体”对话框发送 ESC 键关闭。
- 参数: hwnd
- 关注点: 窗口/输入
- 调用概览: PostMessage
- 理解: 主要用于处理相关逻辑。依据注释：向“缺少 SHX 字体”对话框发送 ESC 键关闭。。包含窗口/输入自动化。
- 风险: 依赖窗口/输入焦点，易受环境影响
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境

### f2_delwindow(timeout_event, done_event)
- 说明: 线程2：轮询“缺少 SHX”对话框并自动 ESC 关闭。
- 邻近注释: &&% 线程2:删除窗口
- 参数: timeout_event, done_event
- 关注点: COM, 时间/等待
- 调用概览: CoInitialize, node, time, CoUninitialize, set, is_set, _find_shx_dialog, sleep, print, _ignore_shx_dialog, format_exc
- 理解: 主要用于处理相关逻辑。依据注释：线程2：轮询“缺少 SHX”对话框并自动 ESC 关闭。。邻近注释提示：&&% 线程2:删除窗口。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### run_dual_threads(f1, f2, f1_args, f1_kwargs, f2_args, f2_kwargs)
- 说明: 启动 f1 / f2 协作：
- 参数: f1, f2, f1_args, f1_kwargs, f2_args, f2_kwargs
- 返回推断: bool
- 关注点: 文件, 时间/等待
- 调用概览: Event, Thread, start, join, node, f2, _run_f1, is_set, set, f1
- 理解: 主要用于打开/读取相关逻辑。依据注释：启动 f1 / f2 协作：。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### Insert_Company_Label_Common_Block(insertion_point, filepath, scale, rotation, wait)
- 说明: 高层：在忽略 SHX 对话框的前提下插入公司图签块。
- 邻近注释: &&% 插入公司通用图签(双线程)
- 参数: insertion_point, filepath, scale, rotation, wait
- 返回: (coms_tuqian, names_tuqian, info_dict) 或 (None, None, None)
- 关注点: 文件, 时间/等待
- 调用概览: run_dual_threads
- 理解: 主要用于创建/插入相关逻辑。依据注释：高层：在忽略 SHX 对话框的前提下插入公司图签块。。邻近注释提示：&&% 插入公司通用图签(双线程)。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### clean_internal_polylines(block_refs)
- 说明: 删除块定义内图层为 'tuqian_neibu_pl' 的多段线。
- 邻近注释: 图签块的清理/重命名/调试填属性 | ============================= | &&% 清理内部多段线
- 参数: block_refs
- 返回推断: object
- 关注点: COM, 几何, 文件, 时间/等待
- 调用概览: li, getattr, sleep, SendCommand, get_attr, Item, get_object_property, range, safe_delete, append
- 理解: 主要用于处理相关逻辑。依据注释：删除块定义内图层为 'tuqian_neibu_pl' 的多段线。。邻近注释提示：图签块的清理/重命名/调试填属性；=============================；&&% 清理内部多段线。实现特征：涉及块定义/块实例操作；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### fill_block_attributes_with_tag_name(blocks)
- 说明: 将块属性文字设置为对应的标签名（用于调试，直接在图签上显示 Tag）。
- 参数: blocks
- 调用概览: get_object_property, GetAttributes, get_attr, set_attr
- 理解: 主要用于处理相关逻辑。依据注释：将块属性文字设置为对应的标签名（用于调试，直接在图签上显示 Tag）。。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _make_bind_dict_serializable(bind_dict)
- 说明: 将 insert_and_scale_labels_area 生成的 bind_dict 压缩成
- 参数: bind_dict
- 返回推断: object
- 关注点: COM, 几何
- 调用概览: items, get, _handles_from_list, isinstance, get_attr, append, str, repr
- 理解: 主要用于创建/插入相关逻辑。依据注释：将 insert_and_scale_labels_area 生成的 bind_dict 压缩成。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### normalize_core_title_blocks_by_layer(core_layer, core_base_names, verbose)
- 说明: 【桥接函数】
- 参数: core_layer, core_base_names, verbose
- 返回推断: bool,object
- 关注点: 日志/测试
- 调用概览: normalize_core_title_blocks_by_layer_new1, info
- 理解: 主要用于处理相关逻辑。依据注释：【桥接函数】。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### explode_title_wrappers_to_core_layer(wrapper_layer, core_layer, core_base_names, verbose)
- 说明: 【步骤 1】炸开 "dy_quyu" 上的图签壳块，把内部的核心块 A?-H 释放到 "dy_quyu_H" 层。
- 参数: wrapper_layer, core_layer, core_base_names, verbose
- 返回: int: 实际炸开的壳块数量
- 关注点: COM, 文件
- 调用概览: node, stc, li, log_err, get_base_name, len, log_warn, SendCommand, print, getattr, str, split...
- 理解: 主要用于处理相关逻辑。依据注释：【步骤 1】炸开 "dy_quyu" 上的图签壳块，把内部的核心块 A?-H 释放到 "dy_quyu_H" 层。。实现特征：通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### repair_mp_insert(target_layout_name, operate_target)
- 说明: 【函数功能】: 修复模型空间插入对象的线宽与图层 (V2.1 - 纯净版)
- 邻近注释: ============================================================ | 1. 主修复入口 (已移除 width_factor) | ============================================================
- 参数: target_layout_name, operate_target
- 返回推断: bool
- 关注点: 几何, 日志/测试, 时间/等待
- 关键调用: wait_quiescent, C.doc
- 调用概览: info, set_space_mode, sleep, log, lines_to_polylines, wait_command_done, smart_repair_frame_polyline_widths_m, ensure_layer_model_only, wait_quiescent, ensure_layer, stc, set_layer_with_retry
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数功能】: 修复模型空间插入对象的线宽与图层 (V2.1 - 纯净版)。邻近注释提示：============================================================；1. 主修复入口 (已移除 width_factor)；============================================================。实现特征：包含空闲等待以同步 CAD 状态。涉及几何/多段线/包围盒处理。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### repair_sp_insert(target_layout_name)
- 说明: 【函数功能】: 直接在布局空间修复图签 (无需借道模型空间)
- 邻近注释: &&% 图纸空间样式修复插入
- 参数: target_layout_name
- 返回推断: bool
- 关注点: 几何, 日志/测试, 时间/等待
- 关键调用: wait_quiescent, C.doc
- 调用概览: info, switch_to_layout, sleep, log, lines_to_polylines, wait_command_done, smart_repair_frame_polyline_widths_p, set_space_mode, wait_quiescent, ensure_layer
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数功能】: 直接在布局空间修复图签 (无需借道模型空间)。邻近注释提示：&&% 图纸空间样式修复插入。实现特征：包含空闲等待以同步 CAD 状态。涉及几何/多段线/包围盒处理。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### smart_repair_frame_polyline_widths_m(verbose)
- 说明: 【函数编号】: FIX-002-Smart (V9.2 - 尺寸优先分流版)
- 邻近注释: &&% 线宽修复
- 参数: verbose
- 返回推断: bool,float,object
- 关注点: 几何, 日志/测试
- 关键调用: C.li, C.doc
- 调用概览: li, info, GetBoundingBox, abs, min, generate_name_and_ratio_from_com, stc, Regen, max, len, calculate_width_for_obj, error...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: FIX-002-Smart (V9.2 - 尺寸优先分流版)。邻近注释提示：&&% 线宽修复。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### smart_repair_frame_polyline_widths_p(verbose)
- 说明: 【函数编号】: FIX-002-Smart (V9.2 - 尺寸优先分流版)
- 参数: verbose
- 返回推断: bool,float,object
- 关注点: 几何, 日志/测试
- 关键调用: C.li, C.doc
- 调用概览: li, info, GetBoundingBox, abs, min, generate_name_and_ratio_from_com, stc, Regen, max, len, calculate_width_for_obj, error...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: FIX-002-Smart (V9.2 - 尺寸优先分流版)。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### cut_model_to_paper_and_switch(target_layout_name)
- 说明: 【函数编号】: MOVE-SPACE-V3.2 (自信版)
- 邻近注释: &&% 从模型空间剪切到图纸空间
- 参数: target_layout_name
- 返回推断: bool,object
- 关注点: COM, 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: log, join, info, Item, Add, VARIANT, Select, range, Delete, CopyObjects, len, append...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: MOVE-SPACE-V3.2 (自信版)。邻近注释提示：&&% 从模型空间剪切到图纸空间。实现特征：涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### _fallback_copy_method(doc, layout_name, layer_filter)
- 说明: （无）
- 邻近注释: ------------------------------------------------------------------ | 保底方案：如果 COM 还是不行，使用 COPYBASE (比 CUTCLIP 稳) | ------------------------------------------------------------------
- 参数: doc, layout_name, layer_filter
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 调用概览: print, Item, SendCommand, info
- 理解: 主要用于移动/复制相关逻辑。邻近注释提示：------------------------------------------------------------------；保底方案：如果 COM 还是不行，使用 COPYBASE (比 CUTCLIP 稳)；------------------------------------------------------------------。实现特征：通过命令发送驱动 CAD 行为。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### cut_screen_selection_to_paper(target_layout_name)
- 说明: 【功能】: 屏幕选择模型空间对象 -> 原坐标复制到指定布局空间
- 邻近注释: &&% 从模型空间屏幕选择对象复制到图纸空间
- 参数: target_layout_name
- 返回推断: None
- 关注点: COM, 文件, 日志/测试
- 调用概览: info, li, range, pmxz, print, list, vtobj, CopyObjects, Item, len, Regen, print_exc...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【功能】: 屏幕选择模型空间对象 -> 原坐标复制到指定布局空间。邻近注释提示：&&% 从模型空间屏幕选择对象复制到图纸空间。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### copy_layout_polylines_to_model(layout_name, polylines_list)
- 说明: 【函数编号】: MAP-COPY-LAYOUT-004 (布局切换+列表直传版)
- 邻近注释: &&% 从图纸空间复制打印区域到模型空间
- 参数: layout_name, polylines_list
- 返回推断: list,object
- 关注点: COM, 几何, 文件, 日志/测试
- 调用概览: info, log, switch_to_layout, li, get, ensure_layer, VARIANT, CopyObjects, range, globals, len, Item...
- 理解: 主要用于移动/复制相关逻辑。依据注释：【函数编号】: MAP-COPY-LAYOUT-004 (布局切换+列表直传版)。邻近注释提示：&&% 从图纸空间复制打印区域到模型空间。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### clear_layout_objects(layout_name, max_retries)
- 说明: 【函数编号】: MAP-CLEAR-LAYOUT-003 (多轮重试版)
- 邻近注释: &&% 清空图纸空间
- 参数: layout_name, max_retries
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待, 进程
- 调用概览: range, log, info, li, Regen, GetActiveObject, sleep, Item, Delete, str
- 理解: 主要用于删除/清理相关逻辑。依据注释：【函数编号】: MAP-CLEAR-LAYOUT-003 (多轮重试版)。邻近注释提示：&&% 清空图纸空间。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### clean_unused_blocks_global_scan(verbose)
- 说明: 【函数编号】: CLEAN-005 (精准概念版)
- 邻近注释: &&% 清除无实例块
- 参数: verbose
- 返回推断: None
- 关注点: 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: set, select_kuai, range, info, Item, startswith, Delete, get_attr, append, add, len
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: CLEAN-005 (精准概念版)。邻近注释提示：&&% 清除无实例块。实现特征：涉及块定义/块实例操作。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### smart_rebuild_print_info(layout_name, operate_target, select_config, use_cache, verbose, **kwargs)
- 说明: 【函数编号】: MAP-UNIFIED-001 (V2.1 - 终极简化版)
- 参数: layout_name, operate_target, select_config, use_cache, verbose, **kwargs
- 返回推断: object,tuple
- 关注点: 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: int, get, log, info, splitext, load_ctq, rebuild_print_area_title_mapping_paper, print_exc, save_ctq, globals, rebuild_print_area_title_mapping, len
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: MAP-UNIFIED-001 (V2.1 - 终极简化版)。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### rebuild_print_area_title_mapping(core_layer, final_poly_layer, select_config, verbose, **kwargs)
- 说明: 【函数编号】: MAP-MODEL-FINAL (V40 - 简化判定版)
- 参数: core_layer, final_poly_layer, select_config, verbose, **kwargs
- 返回推断: bool,tuple
- 关注点: COM, 几何, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: log, select_maxrect_polylines_1, set, enumerate, int, set_space_mode, list, info, stc, GetBoundingBox, is_center_in_poly, append...
- 理解: 主要用于计算/测量相关逻辑。依据注释：【函数编号】: MAP-MODEL-FINAL (V40 - 简化判定版)。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### rebuild_print_area_title_mapping_paper(layout_target, core_layer, final_poly_layer, select_config, verbose, **kwargs)
- 说明: 【函数编号】: MAP-PAPER-FINAL (V40 - 统一逻辑版)
- 参数: layout_target, core_layer, final_poly_layer, select_config, verbose, **kwargs
- 返回推断: bool,tuple
- 关注点: COM, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: log, select_print_areas_paperspace, set, enumerate, int, switch_to_layout, list, info, stc, GetBoundingBox, is_center_in_poly, append...
- 理解: 主要用于计算/测量相关逻辑。依据注释：【函数编号】: MAP-PAPER-FINAL (V40 - 统一逻辑版)。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### build_header_map(ws)
- 说明: 根据第 1 行表头构建 {表头文字: 列号} 的映射。
- 邻近注释: &&% 构建表头映射
- 参数: ws
- 返回推断: object
- 关注点: 日志/测试
- 调用概览: strip, str
- 理解: 主要用于处理相关逻辑。依据注释：根据第 1 行表头构建 {表头文字: 列号} 的映射。。邻近注释提示：&&% 构建表头映射。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### read_xlsx_to_dict(xlsx_path)
- 说明: 读取 Excel，转成统一的数据字典结构。
- 邻近注释: &&% 读取Excel到字典
- 参数: xlsx_path
- 返回推断: dict
- 关注点: 文件, 日志/测试
- 调用概览: items, load_workbook, range, info, cell, get, strip, append, str
- 理解: 主要用于打开/读取相关逻辑。依据注释：读取 Excel，转成统一的数据字典结构。。邻近注释提示：&&% 读取Excel到字典。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### write_dict_to_xlsx(data, output_xlsx_path, template_xlsx_path)
- 说明: 【最终修正版】将字典写回 Excel。
- 邻近注释: &&% 写入字典到Excel
- 参数: data, output_xlsx_path, template_xlsx_path
- 返回推断: None
- 关注点: 文件, 日志/测试
- 调用概览: build_header_map, items, range, get, join, load_workbook, iter_rows, len, save, info, print, cell...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【最终修正版】将字典写回 Excel。。邻近注释提示：&&% 写入字典到Excel。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### auto_export_excel_with_fallback(layout_name, operate_target, select_config, template_path, output_path, start_index, use_cache, verbose)
- 说明: 【函数编号】: XLS-AUTO-FORCE-001
- 邻近注释: &&&% ===（五）从Cad写入Excel === | &&% 自动导出
- 参数: layout_name, operate_target, select_config, template_path, output_path, start_index, use_cache, verbose
- 返回推断: bool,object
- 关注点: 日志/测试, 选择集
- 调用概览: smart_rebuild_print_info, build_full_print_dict_and_export_excel, info, print, len, extend
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: XLS-AUTO-FORCE-001。邻近注释提示：&&&% ===（五）从Cad写入Excel ===；&&% 自动导出。实现特征：涉及块定义/块实例操作。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### build_full_print_dict_and_export_excel(ctq, layout_target, template_path, output_path, start_index)
- 说明: 【函数编号】: XLS-001 (V3.9 - 极简回退版)
- 邻近注释: &&% 基础导出
- 参数: ctq, layout_target, template_path, output_path, start_index
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 关键调用: C.doc
- 调用概览: info, time, get, enumerate, exists, Path, join, print, min, list, len, append...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: XLS-001 (V3.9 - 极简回退版)。邻近注释提示：&&% 基础导出。实现特征：执行 DWG 打开；执行关闭文档；执行另存为。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### auto_process_drawing_names_by_style(layout_name, operate_target, select_config, layername, num1, num2, start_index, prefix, use_cache, verbose)
- 说明: 【函数编号】: XLS-AUTO-003 (V1.0 - 全自动图名抓取版)
- 邻近注释: &&&% ===（六）从图纸获取信息写入图签 === | &&% 自动_图名标注写入图签
- 参数: layout_name, operate_target, select_config, layername, num1, num2, start_index, prefix, use_cache, verbose
- 返回推断: bool,object
- 关注点: COM, 日志/测试, 进程, 选择集
- 调用概览: smart_rebuild_print_info, process_drawing_names_and_fill_titleblocks, info, print
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: XLS-AUTO-003 (V1.0 - 全自动图名抓取版)。邻近注释提示：&&&% ===（六）从图纸获取信息写入图签 ===；&&% 自动_图名标注写入图签。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### process_drawing_names_and_fill_titleblocks(ctq, layout_target, num1, num2, layername, start_index, prefix)
- 说明: 【函数编号】: XLS-003 (V3.1 - 双空间适配版)
- 邻近注释: &&% 基础_图名标注写入图签
- 参数: ctq, layout_target, num1, num2, layername, start_index, prefix
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 关键调用: C.doc
- 调用概览: min, info, range, print, len, save_file, stc, generate_name_and_ratio_from_com, isinstance, GetBoundingBox, strip, str...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: XLS-003 (V3.1 - 双空间适配版)。邻近注释提示：&&% 基础_图名标注写入图签。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### auto_import_excel_to_cad(layout_name, operate_target, select_config, excel_path, start_index, use_cache, verbose)
- 说明: 【函数编号】: XLS-AUTO-002 (V2.0 - 完整标准版)
- 邻近注释: &&&% ===（七）从Excel写入Cad === | &&% 自动写入
- 参数: layout_name, operate_target, select_config, excel_path, start_index, use_cache, verbose
- 返回推断: bool,object
- 关注点: 文件, 日志/测试, 选择集
- 调用概览: smart_rebuild_print_info, read_excel_and_update_cad_titleblocks, info, print
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: XLS-AUTO-002 (V2.0 - 完整标准版)。邻近注释提示：&&&% ===（七）从Excel写入Cad ===；&&% 自动写入。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### read_excel_and_update_cad_titleblocks(ctq, layout_target, excel_path, start_index)
- 说明: 【函数编号】: XLS-002 (V3.1 - 双空间适配版)
- 邻近注释: &&% 基础写入
- 参数: ctq, layout_target, excel_path, start_index
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 关键调用: C.doc
- 调用概览: time, info, wait_command_done, save_file, Path, exists, print, Dispatch, Open, enumerate, Item, isinstance...
- 理解: 主要用于打开/读取相关逻辑。依据注释：【函数编号】: XLS-002 (V3.1 - 双空间适配版)。邻近注释提示：&&% 基础写入。实现特征：执行 DWG 打开；执行关闭文档。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### auto_update_titleblock_format_by_style(att_config, layout_name, operate_target, select_config, use_cache, verbose)
- 说明: 【函数编号】: XLS-AUTO-004 (V1.0 - 格式刷)
- 邻近注释: &&% 自动_修改图块标签属性
- 参数: att_config, layout_name, operate_target, select_config, use_cache, verbose
- 返回推断: bool,object
- 关注点: 日志/测试, 进程, 选择集
- 调用概览: smart_rebuild_print_info, batch_update_block_attributes_config, info, print
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: XLS-AUTO-004 (V1.0 - 格式刷)。邻近注释提示：&&% 自动_修改图块标签属性。包含选择集构造或过滤。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### batch_update_block_attributes_config(ctq, att_config)
- 说明: 【函数编号】: BLK-008-Smart
- 邻近注释: &&% 基础_修改图块标签属性
- 参数: ctq, att_config
- 返回推断: bool,object
- 关注点: 文件, 日志/测试
- 关键调用: C.li
- 调用概览: li, info, set, print, wait_command_done, save_file, items, len, get_attr, isinstance, update_block_def_attributes_safe, get...
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: BLK-008-Smart。邻近注释提示：&&% 基础_修改图块标签属性。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### bianmulu_func1_h(layout_name, operate_target, mulu_xuhao, select_config, use_cache, verbose)
- 说明: 【函数编号】: CAT-UNIFIED-001 (V9.0 - 严格命名版)
- 参数: layout_name, operate_target, mulu_xuhao, select_config, use_cache, verbose
- 返回推断: bool
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc, C.acad
- 调用概览: smart_rebuild_print_info, len, info, new_file, wait_command_done, print, sleep, get, join, range, save_file, open_file...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: CAT-UNIFIED-001 (V9.0 - 严格命名版)。实现特征：执行关闭文档；涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### bianmulu_func2_h(layout_name, operate_target, select_config, use_cache, verbose)
- 说明: 【函数编号】: CAT-UNIFIED-002 (V9.0 - 严格寻址版)
- 参数: layout_name, operate_target, select_config, use_cache, verbose
- 返回推断: bool
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc, C.acad
- 调用概览: info, wait_command_done, lower, stc, save_file, open_file, Path, str, exists, print, len, rebuild_print_area_title_mapping...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: CAT-UNIFIED-002 (V9.0 - 严格寻址版)。实现特征：执行关闭文档；涉及图层操作；涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### bianmulu_func3_h(layout_name, operate_target, mubanxuhao, select_config, use_cache, verbose, start_index, text_height, text_style, text_alignment, text_rotation, text_oblique, text_width_factor, width_factors_map)
- 说明: 【函数编号】: CAT-UNIFIED-003 (V9.0 - 严格寻址版)
- 参数: layout_name, operate_target, mubanxuhao, select_config, use_cache, verbose, start_index, text_height, text_style, text_alignment, text_rotation, text_oblique, text_width_factor, width_factors_map
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试, 选择集
- 关键调用: C.doc, C.acad
- 调用概览: info, Path, str, open_file, wait_command_done, lower, print, rebuild_print_area_title_mapping, exists, globals, write_catalog_from_excel_to_cad, save_file...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: CAT-UNIFIED-003 (V9.0 - 严格寻址版)。实现特征：执行关闭文档。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### bianmulu_func4_h(layout_name, operate_target, select_config, verbose, tol)
- 说明: 【函数编号】: CAT-UNIFIED-004 (V9.8 - 规范展开版)
- 参数: layout_name, operate_target, select_config, verbose, tol
- 返回推断: bool
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 选择集
- 关键调用: send_cmd_with_sync, C.doc
- 调用概览: log, int, Path, str, open_file, sleep, select_maxrect_polylines_1, GetBoundingBox, Close, SetVariable, info, exists...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: CAT-UNIFIED-004 (V9.8 - 规范展开版)。实现特征：执行关闭文档；涉及块定义/块实例操作；涉及系统变量读取/设置；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### update_catalog_titleblocks_from_excel(ctq, excel_path, catalog_name, custom_suffixes)
- 说明: 【目录专用 - 修正版】读取 Excel 项目信息 -> 生成目录图签
- 邻近注释: &&% 写入目录图签
- 参数: ctq, excel_path, catalog_name, custom_suffixes
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 调用概览: print, min, info, Path, range, li, len, exists, Dispatch, Open, enumerate, get...
- 理解: 主要用于更新/设置相关逻辑。依据注释：【目录专用 - 修正版】读取 Excel 项目信息 -> 生成目录图签。邻近注释提示：&&% 写入目录图签。实现特征：执行 DWG 打开；执行关闭文档。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### update_catalog_titleblocks_from_excel_y(ctq, excel_path, catalog_name, custom_suffixes)
- 说明: 【目录专用】读取 Excel 项目信息 -> 生成目录图签
- 参数: ctq, excel_path, catalog_name, custom_suffixes
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 调用概览: len, Path, time, info, get, range, exists, Dispatch, Open, enumerate, copy, update...
- 理解: 主要用于更新/设置相关逻辑。依据注释：【目录专用】读取 Excel 项目信息 -> 生成目录图签。实现特征：执行 DWG 打开；执行关闭文档。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### write_catalog_from_excel_to_cad(ctq, data_excel_path, mubanxuhao, start_index, text_height, text_style, text_alignment, text_rotation, text_oblique, text_width_factor, width_factors_map)
- 说明: 【函数编号】: CAT-001
- 邻近注释: &&% 从excel写入目录dwg文件
- 参数: ctq, data_excel_path, mubanxuhao, start_index, text_height, text_style, text_alignment, text_rotation, text_oblique, text_width_factor, width_factors_map
- 返回推断: None,bool,float,object,tuple
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 调用概览: print, li, wait_cad, get, join, info, enumerate, generate_col_points, extend, range, len, force_color_256...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: CAT-001。邻近注释提示：&&% 从excel写入目录dwg文件。实现特征：创建文字对象；执行 DWG 打开；执行关闭文档；涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### read_catalog_template_config(excel_path)
- 说明: 【配置读取器 - 兼容增强版】
- 邻近注释: &&% 读取目录结构的excel文件
- 参数: excel_path
- 返回推断: NoneType,float,object
- 关注点: COM, 文件, 日志/测试
- 调用概览: isinstance, strip, DispatchEx, Open, Worksheets, _smart_float, int, range, info, float, str, append...
- 理解: 主要用于打开/读取相关逻辑。依据注释：【配置读取器 - 兼容增强版】。邻近注释提示：&&% 读取目录结构的excel文件。实现特征：执行 DWG 打开；执行关闭文档。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### CatalogConfigBuilder.__init__(self, row_height)
- 说明: （无）
- 参数: self, row_height
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### CatalogConfigBuilder.add_column_layout(self, top_y, row_count)
- 说明: 定义第 N 排的纵向布局
- 参数: self, top_y, row_count
- 调用概览: append, int
- 理解: 主要用于创建/插入相关逻辑。依据注释：定义第 N 排的纵向布局。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### CatalogConfigBuilder.set_field_x_ranges(self, field_key, x_ranges_list)
- 说明: 定义某个字段在每一排的 X 轴范围 [(min, max), (min, max)...]
- 参数: self, field_key, x_ranges_list
- 理解: 主要用于更新/设置相关逻辑。依据注释：定义某个字段在每一排的 X 轴范围 [(min, max), (min, max)...]。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### CatalogConfigBuilder.generate(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: items, enumerate, range, join, len, append
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_my_template_config_from_excel(config_path)
- 说明: 读取配置目录结构Excel，解析参数，返回 template_config 字典
- 参数: config_path
- 返回推断: NoneType,object,tuple
- 关注点: COM, 文件, 日志/测试
- 调用概览: Path, exists, info, DispatchEx, Open, float, int, CatalogConfigBuilder, add_column_layout, set_field_x_ranges, print, generate...
- 理解: 主要用于获取/选择相关逻辑。依据注释：读取配置目录结构Excel，解析参数，返回 template_config 字典。实现特征：执行 DWG 打开；执行关闭文档。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### rename_drawings(folderpath, split_prefix, gu1, gu2, tumings_path, naming_order)
- 说明: 功能：根据Excel内容和原有编号重命名图纸，支持自定义排序列表。
- 邻近注释: &&% 文件名修改1
- 参数: folderpath, split_prefix, gu1, gu2, tumings_path, naming_order
- 返回推断: None,object
- 关注点: 文件, 日志/测试
- 调用概览: join, sort, info, enumerate, exists, read_excel, tolist, splitext, listdir, endswith, findall, len...
- 理解: 主要用于创建/插入相关逻辑。依据注释：功能：根据Excel内容和原有编号重命名图纸，支持自定义排序列表。。邻近注释提示：&&% 文件名修改1。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### get_mouse_target_v3(step_idx, total_steps, prompt_text, prev_pos, dwell_time)
- 说明: 参数:
- 邻近注释: ============================================================================= | 1. 核心算法：带“防粘连”的双阶段捕获 | =============================================================================
- 参数: step_idx, total_steps, prompt_text, prev_pos, dwell_time
- 返回推断: tuple
- 关注点: 日志/测试, 时间/等待
- 调用概览: info, position, sqrt, sleep, int, time, print, split
- 理解: 主要用于获取/选择相关逻辑。依据注释：参数:。邻近注释提示：=============================================================================；1. 核心算法：带“防粘连”的双阶段捕获；=============================================================================。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### safe_input_text(coords, text, desc)
- 说明: （无）
- 邻近注释: ============================================================================= | 2. 安全输入逻辑 | =============================================================================
- 参数: coords, text, desc
- 关注点: 文件, 日志/测试, 时间/等待
- 调用概览: click, sleep, hotkey, press, write, str
- 理解: 主要用于处理相关逻辑。邻近注释提示：=============================================================================；2. 安全输入逻辑；=============================================================================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### auto_setup_custom_paper_sizes(data_list)
- 说明: auto_setup_custom_paper_sizes(dy_yonghu)
- 邻近注释: ============================================================================= | 3. 主流程 | =============================================================================
- 参数: data_list
- 关注点: 日志/测试, 时间/等待
- 调用概览: print, input, len, enumerate, sleep, get_mouse_target_v3, info, click, safe_input_text, press
- 理解: 主要用于更新/设置相关逻辑。依据注释：auto_setup_custom_paper_sizes(dy_yonghu)。邻近注释提示：=============================================================================；3. 主流程；=============================================================================。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### list_current_printer_papers(printer_name)
- 说明: 列出指定打印机的所有纸张名称 (内部名 vs 显示名)
- 邻近注释: &&% 获取当前图幅尺寸
- 参数: printer_name
- 返回推断: None
- 关注点: COM, 日志/测试, 进程
- 调用概览: info, GetCanonicalMediaNames, print, GetActiveObject, RefreshPlotDeviceInfo, GetLocaleMediaName, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：列出指定打印机的所有纸张名称 (内部名 vs 显示名)。邻近注释提示：&&% 获取当前图幅尺寸。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### replace_cad_fonts_incremental()
- 说明: （无）
- 邻近注释: &&% 配置字体
- 参数: （无）
- 返回推断: None
- 关注点: 文件, 日志/测试
- 调用概览: join, close_all_cad_processes, print, is_admin, exists, info, copytree, rename, basename
- 理解: 主要用于处理相关逻辑。邻近注释提示：&&% 配置字体。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### is_admin()
- 说明: 检查当前是否获得管理员权限
- 参数: （无）
- 返回推断: bool,object
- 关注点: 窗口/输入
- 调用概览: IsUserAnAdmin
- 理解: 主要用于处理相关逻辑。依据注释：检查当前是否获得管理员权限。包含窗口/输入自动化。
- 风险: 依赖窗口/输入焦点，易受环境影响
- 测试点: 参数合法性与边界值；窗口不可见/无焦点/多屏环境

### sanitize_filename(name)
- 说明: 【COMMON-001-AUX】文件名清洗
- 参数: name
- 返回推断: object,str
- 调用概览: sub, str
- 理解: 主要用于处理相关逻辑。依据注释：【COMMON-001-AUX】文件名清洗。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### export_model_window_pure(point_a, point_b, pdf_fullpath)
- 说明: 【函数编号】: PRINT-001 (A0修正版)
- 邻近注释: &&% 模型空间窗口打印
- 参数: point_a, point_b, pdf_fullpath
- 返回推断: bool
- 关注点: COM, 几何, 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: _draw_boundary_markers, RefreshPlotDeviceInfo, VARIANT, SetWindowToPlot, SetVariable, exists, PlotToFile, float, min, max, info, draw_lwpolyline...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: PRINT-001 (A0修正版)。邻近注释提示：&&% 模型空间窗口打印。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### export_model_window_lisp_fit(point_a, point_b, pdf_fullpath)
- 说明: 【函数编号】: PRINT-002 (LISP 强力修正版 - V2修复Bug)
- 邻近注释: &&% 模型空间LISP窗口打印export_model_window_lisp_fit
- 参数: point_a, point_b, pdf_fullpath
- 返回推断: bool
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: replace, exists, join, SendCommand, time, info, float, min, max, sleep, globals, draw_lwpolyline...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: PRINT-002 (LISP 强力修正版 - V2修复Bug)。邻近注释提示：&&% 模型空间LISP窗口打印export_model_window_lisp_fit。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### export_layout_window_pure(point_a, point_b, pdf_fullpath, layout_name)
- 说明: 【函数编号】: PRINT-002
- 邻近注释: &&% 图纸空间窗口打印
- 参数: point_a, point_b, pdf_fullpath, layout_name
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: RefreshPlotDeviceInfo, SetWindowToPlot, SetVariable, exists, PlotToFile, float, min, max, info, switch_to_layout, VARIANT, remove...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: PRINT-002。邻近注释提示：&&% 图纸空间窗口打印。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### export_layout_window_pure_bianju(point_a, point_b, pdf_fullpath, layout_name)
- 说明: 【函数编号】: PRINT-002-V3 (A0修正版)
- 邻近注释: &&% 图纸空间打印边距修正版备用
- 参数: point_a, point_b, pdf_fullpath, layout_name
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: RefreshPlotDeviceInfo, SetWindowToPlot, SetVariable, exists, PlotToFile, any, info, float, min, max, switch_to_layout, VARIANT...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: PRINT-002-V3 (A0修正版)。邻近注释提示：&&% 图纸空间打印边距修正版备用。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### export_layout_window_lisp_fit_v1(point_a, point_b, pdf_fullpath, layout_name)
- 说明: 【函数编号】: PRINT-004 (LISP-Layout 终极版 - 旧版本，已重命名)
- 邻近注释: &&% 布局空间LISP窗口打印
- 参数: point_a, point_b, pdf_fullpath, layout_name
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: replace, exists, join, SendCommand, time, info, Item, float, min, max, sleep, remove...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: PRINT-004 (LISP-Layout 终极版 - 旧版本，已重命名)。邻近注释提示：&&% 布局空间LISP窗口打印。实现特征：通过命令发送驱动 CAD 行为。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### export_layout_window_lisp_fit(point_a, point_b, pdf_fullpath, layout_name)
- 说明: 【函数编号】: PRINT-LAYOUT-ANTI-TARCH (天正穿透版)
- 参数: point_a, point_b, pdf_fullpath, layout_name
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试, 时间/等待, 选择集
- 关键调用: wait_quiescent, C.doc
- 调用概览: replace, info, sleep, time, Activate, wait_quiescent, warning, switch_to_layout, error, enumerate, exists, SendCommand...
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: PRINT-LAYOUT-ANTI-TARCH (天正穿透版)。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### print_batch_custom_list(files_list, global_config, file_interval)
- 说明: 【函数编号】: PRINT-006 (Router Version)
- 邻近注释: &&% 文件夹打印
- 参数: files_list, global_config, file_interval
- 返回推断: bool,object
- 关注点: 文件, 日志/测试, 时间/等待, 进程
- 调用概览: li, len, info, enumerate, print, isinstance, update, get, basename, copy, pop, range...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: PRINT-006 (Router Version)。邻近注释提示：&&% 文件夹打印。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### mark_print_areas_final(polylines_list, layer_name)
- 说明: 【函数编号】: DRAW-007 (最终版 - 瞄准镜样式)
- 邻近注释: &&% 典型文件的绘制
- 参数: polylines_list, layer_name
- 返回推断: None,object
- 关注点: 几何, 文件, 日志/测试
- 调用概览: info, enumerate, Regen, globals, li, Item, cast_object, safe_get_bbox, float, abs, min, draw_circle...
- 理解: 主要用于计算/测量相关逻辑。依据注释：【函数编号】: DRAW-007 (最终版 - 瞄准镜样式)。邻近注释提示：&&% 典型文件的绘制。实现特征：涉及图层操作。涉及几何/多段线/包围盒处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### generate_tarch_drawing_names_v5(source_obj, print_areas, layer_name)
- 说明: 【函数功能】: DRAW-008 (v5.0 - 网格自适应终极版)
- 邻近注释: &&% 生成图名标注
- 参数: source_obj, print_areas, layer_name
- 返回推断: object
- 关注点: COM, 几何, 日志/测试
- 调用概览: info, enumerate, VARIANT, Regen, safe_get_bbox, abs, vtpnt, range, float, len, Copy, Move...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数功能】: DRAW-008 (v5.0 - 网格自适应终极版)。邻近注释提示：&&% 生成图名标注。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### print_dwg_file_model(file_path)
- 说明: 【函数编号】: PRINT-MODEL-MANAGER (V1 - 模型空间专用)
- 邻近注释: &&&% ===（十二）模型空间文件打印 === | &&% 模型空间文件打印
- 参数: file_path
- 返回推断: object,str
- 关注点: COM, 几何, 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: print, print_polylines_list, join, exists, makedirs, SetVariable, smart_rebuild_print_info, info, open_file, splitext, rmtree, len...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: PRINT-MODEL-MANAGER (V1 - 模型空间专用)。邻近注释提示：&&&% ===（十二）模型空间文件打印 ===；&&% 模型空间文件打印。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### print_polylines_list(polylines_list, title_blocks_list, subproject, dwg_num, dwg_name)
- 说明: 【函数编号】: PRINT-FINAL (V14 - 旋转逻辑修复版)
- 邻近注释: &&% 模型空间批量打印
- 参数: polylines_list, title_blocks_list, subproject, dwg_num, dwg_name
- 返回推断: None,bool
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 窗口/输入, 选择集
- 关键调用: C.doc
- 调用概览: join, isinstance, info, enumerate, execute_batch, exists, makedirs, safe_get_bbox, float, generate_name_and_ratio_from_com, print, sleep...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: PRINT-FINAL (V14 - 旋转逻辑修复版)。邻近注释提示：&&% 模型空间批量打印。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### print_dwg_file_layout(file_path, layout_name)
- 说明: 【功能】: 布局空间批量打印主管理器 (V7 - Polyline适配版)
- 邻近注释: &&&% ===（十三）图纸空间文件打印 === | &&% 图纸空间文件打印
- 参数: file_path, layout_name
- 返回推断: object
- 关注点: 几何, 文件, 日志/测试, 选择集
- 关键调用: C.doc
- 调用概览: get, join, exists, makedirs, info, smart_rebuild_print_info, print_layout_polylines_list, open_file, splitext, rmtree, len
- 理解: 主要用于处理相关逻辑。依据注释：【功能】: 布局空间批量打印主管理器 (V7 - Polyline适配版)。邻近注释提示：&&&% ===（十三）图纸空间文件打印 ===；&&% 图纸空间文件打印。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### print_layout_polylines_list(polylines_list, title_blocks_list, subproject, dwg_num, dwg_name)
- 说明: 【函数编号】: PRINT-LAYOUT-ENGINE (V7.1 - 侦察版)
- 邻近注释: &&% 图纸空间列表打印
- 参数: polylines_list, title_blocks_list, subproject, dwg_num, dwg_name
- 返回推断: None,bool
- 关注点: COM, 几何, 文件, 日志/测试, 时间/等待, 窗口/输入, 选择集
- 关键调用: C.doc
- 调用概览: join, sleep, info, enumerate, execute_batch, exists, makedirs, switch_to_layout, safe_get_bbox, float, print, splitext...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: PRINT-LAYOUT-ENGINE (V7.1 - 侦察版)。邻近注释提示：&&% 图纸空间列表打印。实现特征：通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### print_layout_polylines_list_y(polylines_list, title_blocks_list, subproject, dwg_num, dwg_name)
- 说明: 【函数编号】: PRINT-LAYOUT-ENGINE (V7.2 - 稳健量产版)
- 参数: polylines_list, title_blocks_list, subproject, dwg_num, dwg_name
- 返回推断: bool
- 关注点: 几何, 文件, 日志/测试, 时间/等待
- 关键调用: C.doc
- 调用概览: join, enumerate, info, get, exists, makedirs, switch_to_layout, safe_get_bbox, abs, append, splitext, export_layout_window_lisp_fit...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: PRINT-LAYOUT-ENGINE (V7.2 - 稳健量产版)。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### smart_print_dispatch(file_path, operate_target, layout_name, select_config)
- 说明: 【函数编号】: PRINT-DISPATCHER (智能分发中心)
- 邻近注释: &&% 统一打印
- 参数: file_path, operate_target, layout_name, select_config
- 返回推断: object
- 关注点: 日志/测试, 选择集
- 调用概览: print_dwg_file_model, print_dwg_file_layout, info
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: PRINT-DISPATCHER (智能分发中心)。邻近注释提示：&&% 统一打印。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

## scripts/CAD_check_standards.py
- 模块说明: （无）
### bianmulu_func4_h(layout_name, operate_target, select_config, verbose, tol)
- 说明: 【函数编号】: CAT-UNIFIED-004 (V6.2 - 显式句柄版)
- 参数: layout_name, operate_target, select_config, verbose, tol
- 返回推断: bool
- 关注点: COM, 几何, 文件, 时间/等待, 选择集
- 关键调用: C.doc, C.acad
- 调用概览: print, Path, str, open_file, sleep, exists, select_print_areas_maxrect_from_polylines, SendCommand, Close, GetBoundingBox, SetVariable, isinstance...
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: CAT-UNIFIED-004 (V6.2 - 显式句柄版)。实现特征：执行关闭文档；涉及系统变量读取/设置；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

## scripts/CAD_dev_standards.py
- 模块说明: （无）
### docstring_standard_example(ctq, layout_target)
- 说明: 【函数编号】: DEMO-001 (V1.0 - 标准范例)
- 邻近注释: ============================================================================= | 模块二：文档注释规范 (Docstring Standard) | =============================================================================
- 参数: ctq, layout_target
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: DEMO-001 (V1.0 - 标准范例)。邻近注释提示：=============================================================================；模块二：文档注释规范 (Docstring Standard)；=============================================================================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### count_layers_demo(filter_name, verbose)
- 说明: [范例] 统计包含指定名称的图层数量
- 参数: filter_name, verbose
- 返回推断: int,object
- 关注点: 选择集
- 关键调用: C.doc
- 调用概览: log, int, print, _check_name_match
- 理解: 主要用于处理相关逻辑。依据注释：[范例] 统计包含指定名称的图层数量。实现特征：涉及图层操作。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### _check_name_match(name, keyword, verbose)
- 说明: [子函数] 配合主函数的 verbose 等级
- 参数: name, keyword, verbose
- 返回推断: object
- 调用概览: print
- 理解: 主要用于测试/校验相关逻辑。依据注释：[子函数] 配合主函数的 verbose 等级。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_circle_standard_example()
- 说明: [范例] 标准绘图函数
- 参数: （无）
- 返回推断: bool
- 关注点: COM
- 关键调用: retry_on_busy, C.doc
- 调用概览: VARIANT, AddCircle, print
- 理解: 主要用于创建/插入相关逻辑。依据注释：[范例] 标准绘图函数。实现特征：创建圆对象。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### architecture_full_demo()
- 说明: [范例] 集成所有架构要求的标准函数
- 参数: （无）
- 返回推断: bool
- 关注点: COM
- 关键调用: send_cmd_with_sync, retry_on_busy, C.doc
- 调用概览: print, VARIANT, AddCircle, send_cmd_with_sync
- 理解: 主要用于处理相关逻辑。依据注释：[范例] 集成所有架构要求的标准函数。实现特征：创建圆对象；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

## scripts/CAD_Legacy_Runner.py
- 模块说明: （无）
### LegacyCADRunner.__init__(self, root)
- 说明: （无）
- 参数: self, root
- 关注点: UI/Tk
- 调用概览: title, geometry, Style, theme_use, LabelFrame, pack, Button, grid, ScrolledText
- 理解: 主要用于处理相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### LegacyCADRunner.write(self, text)
- 说明: （无）
- 邻近注释: --- 日志重定向 ---
- 参数: self, text
- 关注点: 文件
- 调用概览: configure, insert, see, update_idletasks
- 理解: 主要用于保存/写入相关逻辑。邻近注释提示：--- 日志重定向 ---。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LegacyCADRunner.flush(self)
- 说明: （无）
- 参数: self
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LegacyCADRunner.run_in_thread(self, target_func, *args, **kwargs)
- 说明: （无）
- 邻近注释: --- 异步执行包装器 (防止界面卡死) ---
- 参数: self, target_func, *args, **kwargs
- 关注点: 文件
- 调用概览: start, print, target_func, Thread
- 理解: 主要用于打开/读取相关逻辑。邻近注释提示：--- 异步执行包装器 (防止界面卡死) ---。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LegacyCADRunner.gui_test_connection(self)
- 说明: 对应 CAD_basic.py 中的 li()
- 邻近注释: ========================================================================= | 3. 按钮功能映射 (这里是关键：如何把按钮对应到你的旧代码) | =========================================================================
- 参数: self
- 关注点: 文件
- 调用概览: run_in_thread, li, print
- 理解: 主要用于测试/校验相关逻辑。依据注释：对应 CAD_basic.py 中的 li()。邻近注释提示：=========================================================================；3. 按钮功能映射 (这里是关键：如何把按钮对应到你的旧代码)；=========================================================================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LegacyCADRunner.gui_new_file(self)
- 说明: 对应 CAD_file_operations.py 中的 new_file()
- 参数: self
- 返回推断: None
- 关注点: UI/Tk, 文件
- 调用概览: asksaveasfilename, askyesno, run_in_thread
- 理解: 主要用于创建/插入相关逻辑。依据注释：对应 CAD_file_operations.py 中的 new_file()。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LegacyCADRunner.gui_save_as(self)
- 说明: 对应 CAD_file_operations.py 中的 save_as (假设你有这个函数)
- 参数: self
- 返回推断: None
- 关注点: 文件
- 调用概览: li, asksaveasfilename, run_in_thread, print, hasattr, save_as, SaveAs
- 理解: 主要用于保存/写入相关逻辑。依据注释：对应 CAD_file_operations.py 中的 save_as (假设你有这个函数)。实现特征：执行另存为。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

## scripts/CAD_System_Queue - V30.py
- 模块说明: （无）
### LockManager.__init__(self, service_root, current_user)
- 说明: （无）
- 参数: self, service_root, current_user
- 关注点: 文件
- 调用概览: join
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.try_acquire(self)
- 说明: （无）
- 参数: self
- 返回推断: tuple
- 关注点: 文件
- 调用概览: exists, _write_lock
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager._write_lock(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: open, dump, str, now
- 理解: 主要用于保存/写入相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.release(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: exists, remove
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.check_waiters(self)
- 说明: （无）
- 参数: self
- 返回推断: list
- 理解: 主要用于等待/守护相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LockManager.add_to_wait_list(self)
- 说明: （无）
- 参数: self
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### MasterRunner.__init__(self, root, user_name, service_path)
- 说明: （无）
- 参数: self, root, user_name, service_path
- 关注点: UI/Tk, 文件, 窗口/输入, 选择集
- 调用概览: join, title, winfo_screenwidth, winfo_screenheight, geometry, LockManager, Style, theme_use, configure, _ensure_bootstrap, after, _init_ui...
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境

### MasterRunner._ensure_bootstrap(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: open, write
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.launch_idle(self)
- 说明: （无）
- 参数: self
- 返回推断: None
- 关注点: 文件, 进程, 选择集
- 调用概览: STARTUPINFO, str, Popen, poll
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### MasterRunner._init_ui(self)
- 说明: （无）
- 参数: self
- 关注点: UI/Tk
- 调用概览: Notebook, pack, create_tab, setup_dashboard, setup_title_block_tab, setup_catalog, setup_print, LabelFrame, ScrolledText
- 理解: 主要用于处理相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.create_tab(self, text)
- 说明: （无）
- 参数: self, text
- 返回推断: object
- 关注点: UI/Tk
- 调用概览: Frame, add
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.setup_dashboard(self)
- 说明: （无）
- 邻近注释: ================= Tab 1: 总看板 =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, LabelFrame, Combobox, current, Button, Label, run_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 1: 总看板 =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.setup_title_block_tab(self)
- 说明: （无）
- 邻近注释: ================= Tab 2: 插图签 =================
- 参数: self
- 关注点: UI/Tk, 几何
- 调用概览: Canvas, Scrollbar, Frame, bind, create_window, configure, pack, LabelFrame, add_dragon_btn, add_step_btn, Button, Label...
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 2: 插图签 =================。涉及几何/多段线/包围盒处理。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.setup_catalog(self)
- 说明: （无）
- 邻近注释: ================= Tab 3: 编目录 =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, Combobox, add_step_btn, Label, Radiobutton
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 3: 编目录 =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.setup_print(self)
- 说明: （无）
- 邻近注释: ================= Tab 4: 打印 (6种模式) =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, LabelFrame, Combobox, columnconfigure, grid, Label, Button, run_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 4: 打印 (6种模式) =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.add_step_btn(self, parent, text, func_key)
- 说明: （无）
- 邻近注释: ================= 辅助函数 =================
- 参数: self, parent, text, func_key
- 关注点: UI/Tk
- 调用概览: pack, Button, run_macro
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：================= 辅助函数 =================。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.add_dragon_btn(self, parent, text, macro_key)
- 说明: （无）
- 参数: self, parent, text, macro_key
- 关注点: UI/Tk
- 调用概览: pack, Button, run_macro
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.send_script_to_idle(self, code_str)
- 说明: （无）
- 参数: self, code_str
- 返回推断: bool
- 关注点: 文件, 时间/等待, 网络
- 调用概览: open, write, socket, settimeout, connect, sendall, log, encode
- 理解: 主要用于关闭/终止相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时；涉及网络请求，需考虑超时与异常
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### MasterRunner.ask_attribute_config(self)
- 说明: （无）
- 参数: self
- 返回推断: tuple
- 关注点: UI/Tk, 几何
- 调用概览: Toplevel, title, geometry, Canvas, Scrollbar, Frame, create_window, bind, configure, pack, grid, enumerate...
- 理解: 主要用于处理相关逻辑。涉及几何/多段线/包围盒处理。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.ask_detection_params(self, initial_style)
- 说明: （无）
- 参数: self, initial_style
- 返回推断: tuple
- 关注点: UI/Tk
- 调用概览: Toplevel, title, geometry, pack, StringVar, Combobox, wait_window, update, destroy, Label, get, Entry...
- 理解: 主要用于处理相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.run_macro(self, macro_name)
- 说明: （无）
- 邻近注释: ================= 宏逻辑分发 =================
- 参数: self, macro_name
- 返回推断: None,object
- 关注点: COM, UI/Tk, 几何, 文件, 时间/等待, 选择集
- 调用概览: start, range, replace, get, int, Toplevel, title, geometry, pack, StringVar, wait_window, send_script_to_idle...
- 理解: 主要用于处理相关逻辑。邻近注释提示：================= 宏逻辑分发 =================。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时；依赖图形界面环境
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### MasterRunner.refresh_workspace_paths(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: get, join, set, exists, current, log, walk, sorted, makedirs, endswith, listdir, len...
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.log(self, text)
- 说明: （无）
- 参数: self, text
- 调用概览: configure, insert, see
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### MasterRunner.monitor_waiters(self)
- 说明: （无）
- 参数: self
- 关注点: 文件, 时间/等待
- 调用概览: check_waiters, sleep
- 理解: 主要用于等待/守护相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### MasterRunner.on_close(self)
- 说明: （无）
- 参数: self
- 调用概览: release, destroy, terminate
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## scripts/CAD_System_Queue - V31.py
- 模块说明: （无）
### LockManager.__init__(self, service_root, current_user)
- 说明: （无）
- 参数: self, service_root, current_user
- 关注点: 文件
- 调用概览: join
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.try_acquire(self)
- 说明: （无）
- 参数: self
- 返回推断: tuple
- 关注点: 文件
- 调用概览: exists, _write_lock
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager._write_lock(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: open, dump, str, now
- 理解: 主要用于保存/写入相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.release(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: exists, remove
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.check_waiters(self)
- 说明: （无）
- 参数: self
- 返回推断: list
- 理解: 主要用于等待/守护相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LockManager.add_to_wait_list(self)
- 说明: （无）
- 参数: self
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### MasterRunner.__init__(self, root, user_name, service_path)
- 说明: （无）
- 参数: self, root, user_name, service_path
- 关注点: UI/Tk, 文件, 窗口/输入, 选择集
- 调用概览: join, title, winfo_screenwidth, winfo_screenheight, geometry, LockManager, Style, theme_use, configure, _ensure_bootstrap, after, _init_ui...
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境

### MasterRunner._ensure_bootstrap(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: open, write
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.launch_idle(self)
- 说明: （无）
- 参数: self
- 返回推断: None
- 关注点: 文件, 进程, 选择集
- 调用概览: STARTUPINFO, str, Popen, poll
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### MasterRunner._init_ui(self)
- 说明: （无）
- 参数: self
- 关注点: UI/Tk
- 调用概览: Notebook, pack, create_tab, setup_dashboard, setup_title_block_tab, setup_catalog, setup_print, LabelFrame, ScrolledText
- 理解: 主要用于处理相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.create_tab(self, text)
- 说明: （无）
- 参数: self, text
- 返回推断: object
- 关注点: UI/Tk
- 调用概览: Frame, add
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.setup_dashboard(self)
- 说明: （无）
- 邻近注释: ================= Tab 1: 总看板 =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, LabelFrame, Combobox, current, Button, Label, run_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 1: 总看板 =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.setup_title_block_tab(self)
- 说明: （无）
- 邻近注释: ================= Tab 2: 插图签 =================
- 参数: self
- 关注点: UI/Tk, 几何
- 调用概览: Canvas, Scrollbar, Frame, bind, create_window, configure, pack, LabelFrame, add_dragon_btn, add_step_btn, Button, Label...
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 2: 插图签 =================。涉及几何/多段线/包围盒处理。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.setup_catalog(self)
- 说明: （无）
- 邻近注释: ================= Tab 3: 编目录 =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, Combobox, add_step_btn, Label, Radiobutton
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 3: 编目录 =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.setup_print(self)
- 说明: （无）
- 邻近注释: ================= Tab 4: 打印 (6种模式) =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, LabelFrame, Combobox, columnconfigure, grid, Label, Button, run_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 4: 打印 (6种模式) =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.add_step_btn(self, parent, text, func_key)
- 说明: （无）
- 邻近注释: ================= 辅助函数 =================
- 参数: self, parent, text, func_key
- 关注点: UI/Tk
- 调用概览: pack, Button, run_macro
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：================= 辅助函数 =================。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.add_dragon_btn(self, parent, text, macro_key)
- 说明: （无）
- 参数: self, parent, text, macro_key
- 关注点: UI/Tk
- 调用概览: pack, Button, run_macro
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.send_script_to_idle(self, code_str)
- 说明: （无）
- 参数: self, code_str
- 返回推断: bool
- 关注点: 文件, 时间/等待, 网络
- 调用概览: open, write, socket, settimeout, connect, sendall, log, encode
- 理解: 主要用于关闭/终止相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时；涉及网络请求，需考虑超时与异常
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### MasterRunner.ask_attribute_config(self)
- 说明: （无）
- 参数: self
- 返回推断: tuple
- 关注点: UI/Tk, 几何
- 调用概览: Toplevel, title, geometry, Canvas, Scrollbar, Frame, create_window, bind, configure, pack, grid, enumerate...
- 理解: 主要用于处理相关逻辑。涉及几何/多段线/包围盒处理。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.ask_detection_params(self, initial_style)
- 说明: （无）
- 参数: self, initial_style
- 返回推断: tuple
- 关注点: UI/Tk
- 调用概览: Toplevel, title, geometry, pack, StringVar, Combobox, wait_window, update, destroy, Label, get, Entry...
- 理解: 主要用于处理相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.run_macro(self, macro_name)
- 说明: （无）
- 邻近注释: ================= 宏逻辑分发 =================
- 参数: self, macro_name
- 返回推断: None,object
- 关注点: COM, UI/Tk, 几何, 文件, 时间/等待, 选择集
- 调用概览: start, range, replace, get, int, Toplevel, title, geometry, pack, StringVar, wait_window, send_script_to_idle...
- 理解: 主要用于处理相关逻辑。邻近注释提示：================= 宏逻辑分发 =================。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时；依赖图形界面环境
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### MasterRunner.refresh_workspace_paths(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: get, join, set, exists, current, log, walk, sorted, makedirs, endswith, listdir, len...
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.log(self, text)
- 说明: （无）
- 参数: self, text
- 调用概览: configure, insert, see
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### MasterRunner.monitor_waiters(self)
- 说明: （无）
- 参数: self
- 关注点: 文件, 时间/等待
- 调用概览: check_waiters, sleep
- 理解: 主要用于等待/守护相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### MasterRunner.on_close(self)
- 说明: （无）
- 参数: self
- 调用概览: release, destroy, terminate
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## scripts/CAD_System_Queue - V33.py
- 模块说明: （无）
### LockManager.__init__(self, service_root, current_user)
- 说明: （无）
- 参数: self, service_root, current_user
- 关注点: 文件
- 调用概览: join
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.try_acquire(self)
- 说明: （无）
- 参数: self
- 返回推断: tuple
- 关注点: 文件
- 调用概览: exists, _write_lock
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager._write_lock(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: open, dump, str, now
- 理解: 主要用于保存/写入相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.release(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: exists, remove
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.check_waiters(self)
- 说明: （无）
- 参数: self
- 返回推断: list
- 理解: 主要用于等待/守护相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LockManager.add_to_wait_list(self)
- 说明: （无）
- 参数: self
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### MasterRunner.__init__(self, root, user_name, service_path)
- 说明: （无）
- 参数: self, root, user_name, service_path
- 关注点: UI/Tk, 文件, 窗口/输入, 选择集
- 调用概览: join, title, winfo_screenwidth, winfo_screenheight, geometry, LockManager, Style, theme_use, configure, _ensure_bootstrap, after, _init_ui...
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境

### MasterRunner._ensure_bootstrap(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: open, write
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.launch_idle(self)
- 说明: （无）
- 参数: self
- 返回推断: None
- 关注点: 文件, 进程, 选择集
- 调用概览: STARTUPINFO, str, Popen, poll
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### MasterRunner._init_ui(self)
- 说明: （无）
- 参数: self
- 关注点: UI/Tk
- 调用概览: Notebook, pack, create_tab, setup_dashboard, setup_datacenter, setup_title_block_tab, setup_catalog, setup_print, LabelFrame, ScrolledText
- 理解: 主要用于处理相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.create_tab(self, text)
- 说明: （无）
- 参数: self, text
- 返回推断: object
- 关注点: UI/Tk
- 调用概览: Frame, add
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.setup_dashboard(self)
- 说明: （无）
- 邻近注释: ================= Tab 1: 系统控制台 (原总看板) =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, LabelFrame, Combobox, Button, Label, run_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 1: 系统控制台 (原总看板) =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.setup_datacenter(self)
- 说明: （无）
- 邻近注释: ================= Tab 2: 数据中心 =================
- 参数: self
- 关注点: UI/Tk, 文件, 选择集
- 调用概览: LabelFrame, pack, Frame, columnconfigure, grid, Text, Label, Combobox, Entry, Checkbutton, Button, run_datacenter_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 2: 数据中心 =================。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### MasterRunner.setup_title_block_tab(self)
- 说明: （无）
- 邻近注释: ================= Tab 3: 插图签 (重构与重号) =================
- 参数: self
- 关注点: UI/Tk, 几何
- 调用概览: Canvas, Scrollbar, Frame, bind, create_window, configure, pack, LabelFrame, add_dragon_btn, add_step_btn, Button, Label...
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 3: 插图签 (重构与重号) =================。涉及几何/多段线/包围盒处理。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.setup_catalog(self)
- 说明: （无）
- 邻近注释: ================= Tab 4: 编目录 (保持原样) =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, Combobox, add_step_btn, Label, Radiobutton
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 4: 编目录 (保持原样) =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.setup_print(self)
- 说明: （无）
- 邻近注释: ================= Tab 5: 打印 (保持原样) =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, LabelFrame, Combobox, columnconfigure, grid, Label, Button, run_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 5: 打印 (保持原样) =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.add_step_btn(self, parent, text, func_key)
- 说明: （无）
- 邻近注释: ================= 辅助函数 =================
- 参数: self, parent, text, func_key
- 关注点: UI/Tk
- 调用概览: pack, Button, run_macro
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：================= 辅助函数 =================。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.add_dragon_btn(self, parent, text, macro_key)
- 说明: （无）
- 参数: self, parent, text, macro_key
- 关注点: UI/Tk
- 调用概览: pack, Button, run_macro
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.send_script_to_idle(self, code_str)
- 说明: （无）
- 参数: self, code_str
- 返回推断: bool
- 关注点: 文件, 时间/等待, 网络
- 调用概览: open, write, socket, settimeout, connect, sendall, log, encode
- 理解: 主要用于关闭/终止相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时；涉及网络请求，需考虑超时与异常
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### MasterRunner.ask_attribute_config(self)
- 说明: （无）
- 参数: self
- 返回推断: tuple
- 关注点: UI/Tk, 几何
- 调用概览: Toplevel, title, geometry, Canvas, Scrollbar, Frame, create_window, bind, configure, pack, grid, enumerate...
- 理解: 主要用于处理相关逻辑。涉及几何/多段线/包围盒处理。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.run_datacenter_macro(self, action)
- 说明: （无）
- 邻近注释: ================= 数据中心逻辑 (已修复反斜杠问题) =================
- 参数: self, action
- 关注点: 几何, 文件, 选择集
- 关键调用: C.doc
- 调用概览: strip, get, str, replace, isdigit, int, send_script_to_idle, lower, join
- 理解: 主要用于处理相关逻辑。邻近注释提示：================= 数据中心逻辑 (已修复反斜杠问题) =================。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### MasterRunner.run_macro(self, macro_name)
- 说明: （无）
- 邻近注释: ================= 宏逻辑分发 (旧版兼容/更新) =================
- 参数: self, macro_name
- 返回推断: None
- 关注点: COM, UI/Tk, 几何, 文件, 时间/等待
- 调用概览: start, range, replace, get, int, send_script_to_idle, sleep, Thread, attributes, ask_attribute_config, dumps, showerror
- 理解: 主要用于处理相关逻辑。邻近注释提示：================= 宏逻辑分发 (旧版兼容/更新) =================。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时；依赖图形界面环境
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### MasterRunner.refresh_workspace_paths(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: get, join, set, exists, current, log, walk, sorted, makedirs, endswith, listdir, len...
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.log(self, text)
- 说明: （无）
- 参数: self, text
- 调用概览: configure, insert, see
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### MasterRunner.monitor_waiters(self)
- 说明: （无）
- 参数: self
- 关注点: 文件, 时间/等待
- 调用概览: check_waiters, sleep
- 理解: 主要用于等待/守护相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### MasterRunner.on_close(self)
- 说明: （无）
- 参数: self
- 调用概览: release, destroy, terminate
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## scripts/CAD_System_Queue.py
- 模块说明: （无）
### LockManager.__init__(self, service_root, current_user)
- 说明: （无）
- 参数: self, service_root, current_user
- 关注点: 文件
- 调用概览: join
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.try_acquire(self)
- 说明: （无）
- 参数: self
- 返回推断: tuple
- 关注点: 文件
- 调用概览: exists, _write_lock
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager._write_lock(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: open, dump, str, now
- 理解: 主要用于保存/写入相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.release(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: exists, remove
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### LockManager.check_waiters(self)
- 说明: （无）
- 参数: self
- 返回推断: list
- 理解: 主要用于等待/守护相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LockManager.add_to_wait_list(self)
- 说明: （无）
- 参数: self
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### MasterRunner.__init__(self, root, user_name, service_path)
- 说明: （无）
- 参数: self, root, user_name, service_path
- 关注点: UI/Tk, 文件, 窗口/输入, 选择集
- 调用概览: join, title, winfo_screenwidth, winfo_screenheight, geometry, LockManager, Style, theme_use, configure, _ensure_bootstrap, after, _init_ui...
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境

### MasterRunner._ensure_bootstrap(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: open, write
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.launch_idle(self)
- 说明: （无）
- 参数: self
- 返回推断: None
- 关注点: 文件, 进程, 选择集
- 调用概览: STARTUPINFO, str, Popen, poll
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### MasterRunner._init_ui(self)
- 说明: （无）
- 参数: self
- 关注点: UI/Tk
- 调用概览: Notebook, pack, create_tab, setup_dashboard, setup_datacenter, setup_title_block_tab, setup_catalog, setup_print, LabelFrame, ScrolledText
- 理解: 主要用于处理相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.create_tab(self, text)
- 说明: （无）
- 参数: self, text
- 返回推断: object
- 关注点: UI/Tk
- 调用概览: Frame, add
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.setup_dashboard(self)
- 说明: （无）
- 邻近注释: ================= Tab 1: 系统控制台 (UI更新) =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, LabelFrame, Combobox, columnconfigure, grid, Button, Label, run_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 1: 系统控制台 (UI更新) =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.setup_datacenter(self)
- 说明: （无）
- 邻近注释: ================= Tab 2: 数据中心 =================
- 参数: self
- 关注点: UI/Tk, 文件, 选择集
- 调用概览: LabelFrame, pack, Frame, columnconfigure, grid, Text, Label, Combobox, Entry, Checkbutton, Button, run_datacenter_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 2: 数据中心 =================。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### MasterRunner.setup_title_block_tab(self)
- 说明: （无）
- 邻近注释: ================= Tab 3: 插图签 (重构与重号) =================
- 参数: self
- 关注点: UI/Tk, 几何
- 调用概览: Canvas, Scrollbar, Frame, bind, create_window, configure, pack, LabelFrame, add_dragon_btn, add_step_btn, Button, Label...
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 3: 插图签 (重构与重号) =================。涉及几何/多段线/包围盒处理。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.setup_catalog(self)
- 说明: （无）
- 邻近注释: ================= Tab 4: 编目录 (保持原样) =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, Combobox, add_step_btn, Label, Radiobutton
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 4: 编目录 (保持原样) =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.setup_print(self)
- 说明: （无）
- 邻近注释: ================= Tab 5: 打印 (保持原样) =================
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: Frame, pack, LabelFrame, Combobox, columnconfigure, grid, Label, Button, run_macro
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：================= Tab 5: 打印 (保持原样) =================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.add_step_btn(self, parent, text, func_key)
- 说明: （无）
- 邻近注释: ================= 辅助函数 =================
- 参数: self, parent, text, func_key
- 关注点: UI/Tk
- 调用概览: pack, Button, run_macro
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：================= 辅助函数 =================。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.add_dragon_btn(self, parent, text, macro_key)
- 说明: （无）
- 参数: self, parent, text, macro_key
- 关注点: UI/Tk
- 调用概览: pack, Button, run_macro
- 理解: 主要用于创建/插入相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.send_script_to_idle(self, code_str)
- 说明: （无）
- 参数: self, code_str
- 返回推断: bool
- 关注点: 文件, 时间/等待, 网络
- 调用概览: open, write, socket, settimeout, connect, sendall, log, encode
- 理解: 主要用于关闭/终止相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时；涉及网络请求，需考虑超时与异常
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### MasterRunner.ask_attribute_config(self)
- 说明: （无）
- 参数: self
- 返回推断: tuple
- 关注点: UI/Tk, 几何
- 调用概览: Toplevel, title, geometry, Canvas, Scrollbar, Frame, create_window, bind, configure, pack, grid, enumerate...
- 理解: 主要用于处理相关逻辑。涉及几何/多段线/包围盒处理。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### MasterRunner.run_datacenter_macro(self, action)
- 说明: （无）
- 邻近注释: ================= 数据中心逻辑 (已修复反斜杠问题) =================
- 参数: self, action
- 关注点: 几何, 文件, 选择集
- 关键调用: C.doc
- 调用概览: strip, get, str, replace, isdigit, int, send_script_to_idle, lower, join
- 理解: 主要用于处理相关逻辑。邻近注释提示：================= 数据中心逻辑 (已修复反斜杠问题) =================。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### MasterRunner.run_macro(self, macro_name)
- 说明: （无）
- 邻近注释: ================= 宏逻辑分发 (旧版兼容/更新) =================
- 参数: self, macro_name
- 返回推断: None
- 关注点: COM, UI/Tk, 几何, 文件, 时间/等待, 选择集
- 调用概览: start, strip, get, str, replace, range, int, send_script_to_idle, isdigit, sleep, Thread, lower...
- 理解: 主要用于处理相关逻辑。邻近注释提示：================= 宏逻辑分发 (旧版兼容/更新) =================。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时；依赖图形界面环境
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### MasterRunner.refresh_workspace_paths(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: get, join, set, exists, current, log, walk, sorted, makedirs, endswith, listdir, len...
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### MasterRunner.log(self, text)
- 说明: （无）
- 参数: self, text
- 调用概览: configure, insert, see
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### MasterRunner.monitor_waiters(self)
- 说明: （无）
- 参数: self
- 关注点: 文件, 时间/等待
- 调用概览: check_waiters, sleep
- 理解: 主要用于等待/守护相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### MasterRunner.on_close(self)
- 说明: （无）
- 参数: self
- 调用概览: release, destroy, terminate
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## scripts/IDLE_bootstrap.py
- 模块说明: （无）
### run_script_in_main(script_path)
- 说明: 模拟 IDLE 的 'Run Module' (F5)。
- 参数: script_path
- 返回推断: None
- 关注点: 文件
- 调用概览: dirname, basename, print, getcwd, write, flush, exists, insert, chdir, compile, exec, open...
- 理解: 主要用于处理相关逻辑。依据注释：模拟 IDLE 的 'Run Module' (F5)。。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### start_listener()
- 说明: 启动 Socket 监听线程
- 参数: （无）
- 关注点: 时间/等待, 网络
- 调用概览: socket, setsockopt, print, bind, listen, accept, decode, startswith, sleep, strip, run_script_in_main, recv
- 理解: 主要用于获取/选择相关逻辑。依据注释：启动 Socket 监听线程。
- 风险: 包含等待/阻塞逻辑，可能超时；涉及网络请求，需考虑超时与异常
- 测试点: 参数合法性与边界值；超时与重试次数边界

## scripts/Master_Orchestrator.py
- 模块说明: 【工程图纸自动化系统 - 总指挥中心】
### AssistantVoice.__init__(self, enabled)
- 说明: （无）
- 参数: self, enabled
- 关注点: 日志/测试
- 调用概览: init, getProperty, setProperty, warning, lower
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AssistantVoice.speak(self, text)
- 说明: 播报消息（非阻塞模式建议，这里简化为阻塞）
- 参数: self, text
- 返回推断: None
- 关注点: 日志/测试
- 调用概览: info, say, runAndWait
- 理解: 主要用于处理相关逻辑。依据注释：播报消息（非阻塞模式建议，这里简化为阻塞）。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### campaign_insert_labels(target_file)
- 说明: 【战役 1】插图签系统
- 邻近注释: ================= 4. 子系统封装 (Campaign Layer) =================
- 参数: target_file
- 返回推断: dict
- 关注点: 日志/测试
- 调用概览: info, run_title_block_assembly_pipeline, hasattr, ImportError, RuntimeError
- 理解: 主要用于创建/插入相关逻辑。依据注释：【战役 1】插图签系统。邻近注释提示：================= 4. 子系统封装 (Campaign Layer) =================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### campaign_build_catalog(prev_data)
- 说明: 【战役 2】编目录系统 (示例框架)
- 参数: prev_data
- 返回推断: dict
- 关注点: 日志/测试, 时间/等待
- 调用概览: info
- 理解: 主要用于处理相关逻辑。依据注释：【战役 2】编目录系统 (示例框架)。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### campaign_batch_print(prev_data)
- 说明: 【战役 3】自动打印系统 (示例框架)
- 参数: prev_data
- 返回推断: dict
- 关注点: 日志/测试
- 调用概览: info
- 理解: 主要用于处理相关逻辑。依据注释：【战役 3】自动打印系统 (示例框架)。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### run_project_master_control(dwg_file_path)
- 说明: 【战略总控】
- 邻近注释: ================= 5. 总控逻辑 (Strategy Layer) =================
- 参数: dwg_file_path
- 返回推断: bool
- 关注点: 日志/测试
- 调用概览: speak, run_safety_loop, ensure_single_process, warning, info, error, CriticalSection, campaign_insert_labels, record, get, campaign_build_catalog, campaign_batch_print...
- 理解: 主要用于处理相关逻辑。依据注释：【战略总控】。邻近注释提示：================= 5. 总控逻辑 (Strategy Layer) =================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## scripts/修复codex脚本.py
- 模块说明: （无）
### fix_and_copy_newlines(source_filename, target_txt_filename)
- 说明: （无）
- 参数: source_filename, target_txt_filename
- 关注点: 文件, 选择集
- 调用概览: replace, open, read, write
- 理解: 主要用于创建/插入相关逻辑。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### create_py_file_from_txt(txt_filename, py_filename)
- 说明: （无）
- 参数: txt_filename, py_filename
- 关注点: 文件
- 调用概览: open, read, write
- 理解: 主要用于创建/插入相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### fix_and_convert(source_filename)
- 说明: （无）
- 邻近注释: 主函数，处理文件转换
- 参数: source_filename
- 关注点: 文件
- 调用概览: fix_and_copy_newlines, create_py_file_from_txt, print, rsplit
- 理解: 主要用于转换/解析相关逻辑。邻近注释提示：主函数，处理文件转换。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

## scripts/函数编写规范.py
- 模块说明: 适用范围: AutoCAD Python Automation System (win32com based)
### li()
- 说明: 【函数编号】: COMMON-CONN-001
- 邻近注释: Level: L1 (Infrastructure) | ============================================================================== | 1 连接cad必须使用li()
- 参数: （无）
- 返回推断: bool
- 关注点: COM, 文件, 时间/等待, 选择集
- 调用概览: range, print, get_acad_doc, draw_line, get_object_property, RuntimeError, safe_delete, sleep, repr
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: COMMON-CONN-001。邻近注释提示：Level: L1 (Infrastructure)；==============================================================================；1 连接cad必须使用li()。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### get_acad_doc(max_wait)
- 说明: 【函数编号】: COMMON-CONN-002
- 参数: max_wait
- 返回推断: tuple
- 关注点: COM, 时间/等待, 进程
- 调用概览: _coinit_once, time, GetActiveObject, EnsureDispatch, sleep, RuntimeError, print, Add
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: COMMON-CONN-002。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### _coinit_once()
- 说明: 【函数编号】: COMMON-CONN-003-AUX
- 参数: （无）
- 关注点: COM
- 调用概览: CoInitialize
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: COMMON-CONN-003-AUX。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### com_retry(fn, retries, delay)
- 说明: 【函数编号】: COMMON-CONN-004-AUX
- 参数: fn, retries, delay
- 返回推断: object
- 关注点: 时间/等待
- 调用概览: range, fn, sleep
- 理解: 主要用于等待/守护相关逻辑。依据注释：【函数编号】: COMMON-CONN-004-AUX。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### select_tuceng(layer_names, max_retries, delay, autocast)
- 说明: 【函数编号】: SELECT-001
- 邻近注释: 2 选择不要使用遍历模型空间，应该使用图层选择，多段线选择，快选择等类型选择区域选择要用 | ===================== 选择函数（重写版） ===================== | &&% 按图层选择
- 参数: layer_names, max_retries, delay, autocast
- 返回推断: list,object
- 关注点: COM, 时间/等待, 选择集
- 调用概览: isinstance, range, print, list, ss_select, sleep, get_acad_doc, SendCommand, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-001。邻近注释提示：2 选择不要使用遍历模型空间，应该使用图层选择，多段线选择，快选择等类型选择区域选择要用；===================== 选择函数（重写版） =====================；&&% 按图层选择。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### stc(layer_names, **kwargs)
- 说明: 【函数编号】: SELECT-001-ALIAS
- 邻近注释: &&% 图层选择别名
- 参数: layer_names, **kwargs
- 返回推断: object
- 关注点: 选择集
- 调用概览: select_tuceng
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: SELECT-001-ALIAS。邻近注释提示：&&% 图层选择别名。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_kuai(max_retries, autocast)
- 说明: 【函数编号】: SELECT-002
- 邻近注释: &&% 选择所有块
- 参数: max_retries, autocast
- 返回推断: list,object
- 关注点: COM, 时间/等待, 选择集
- 调用概览: time, range, print, ss_select, sleep, get_acad_doc, SendCommand, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-002。邻近注释提示：&&% 选择所有块。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### select_text(autocast)
- 说明: 【函数编号】: SELECT-003
- 邻近注释: 4) 选择所有 TEXT | &&% 选择所有文本
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: time, ss_select, print
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-003。邻近注释提示：4) 选择所有 TEXT；&&% 选择所有文本。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_mtext(autocast)
- 说明: 【函数编号】: SELECT-004
- 邻近注释: 5) 选择所有 MTEXT | &&% 选择所有多行文本
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: time, ss_select, print
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-004。邻近注释提示：5) 选择所有 MTEXT；&&% 选择所有多行文本。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_pub_text_entities()
- 说明: 【函数编号】: SELECT-005
- 邻近注释: 6) PUB_TEXT 图层上的“天正文字”分类（按 ObjectName） | &&% 选择天正文本
- 参数: （无）
- 返回推断: tuple
- 关注点: 选择集
- 调用概览: select_tuceng, getattr, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-005。邻近注释提示：6) PUB_TEXT 图层上的“天正文字”分类（按 ObjectName）；&&% 选择天正文本。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### collect_all_texts()
- 说明: 【函数编号】: SELECT-006
- 邻近注释: &&% 收集所有文本
- 参数: （无）
- 返回推断: tuple
- 关注点: 选择集
- 调用概览: select_pub_text_entities, select_text, select_mtext
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-006。邻近注释提示：&&% 收集所有文本。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_line(autocast)
- 说明: 【函数编号】: SELECT-007 | 选择所有直线 (LINE)
- 邻近注释: 7) 选择 LINE / CIRCLE / ELLIPSE / SPLINE | &&% 选择直线
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: time, ss_select, print
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-007 | 选择所有直线 (LINE)。邻近注释提示：7) 选择 LINE / CIRCLE / ELLIPSE / SPLINE；&&% 选择直线。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_circle(autocast)
- 说明: 【函数编号】: SELECT-008 | 选择所有圆 (CIRCLE)
- 邻近注释: &&% 选择圆
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: time, ss_select, print
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-008 | 选择所有圆 (CIRCLE)。邻近注释提示：&&% 选择圆。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_ellipse(autocast)
- 说明: 【函数编号】: SELECT-009 | 选择所有椭圆 (ELLIPSE)
- 邻近注释: &&% 选择椭圆
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: time, ss_select, print
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-009 | 选择所有椭圆 (ELLIPSE)。邻近注释提示：&&% 选择椭圆。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_spline(autocast)
- 说明: 【函数编号】: SELECT-010 | 选择所有样条曲线 (SPLINE)
- 邻近注释: &&% 选择样条曲线
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: time, ss_select, print
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-010 | 选择所有样条曲线 (SPLINE)。邻近注释提示：&&% 选择样条曲线。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_polyline_chuantong(max_retries, autocast)
- 说明: 【函数编号】: SELECT-011
- 邻近注释: 8) 传统多段线（POLYLINE）与轻量多段线（LWPOLYLINE） | &&% 选择传统多段线
- 参数: max_retries, autocast
- 返回推断: list,object
- 关注点: COM, 几何, 时间/等待, 选择集
- 调用概览: time, range, print, ss_select, sleep, get_acad_doc, SendCommand, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-011。邻近注释提示：8) 传统多段线（POLYLINE）与轻量多段线（LWPOLYLINE）；&&% 选择传统多段线。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### select_polyline(max_retries, autocast)
- 说明: 【函数编号】: SELECT-012
- 邻近注释: &&% 选择轻量多段线
- 参数: max_retries, autocast
- 返回推断: list,object
- 关注点: COM, 几何, 时间/等待, 选择集
- 调用概览: time, range, print, ss_select, sleep, get_acad_doc, SendCommand, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-012。邻近注释提示：&&% 选择轻量多段线。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### normalize_rect(x1, y1, x2, y2)
- 说明: 【函数编号】: GEOM-UTIL-001
- 邻近注释: MODULE: GEOM-UTIL (几何计算工具) | Level: L2 (Geometry) | ==============================================================================
- 参数: x1, y1, x2, y2
- 返回推断: tuple
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: GEOM-UTIL-001。邻近注释提示：MODULE: GEOM-UTIL (几何计算工具)；Level: L2 (Geometry)；==============================================================================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### pt3(x, y, z)
- 说明: 【函数编号】: GEOM-UTIL-002
- 参数: x, y, z
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: GEOM-UTIL-002。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### select_entities_in_window(x1, y1, x2, y2, ty, select_mode)
- 说明: 【函数编号】: SELECT-013
- 邻近注释: &&% 隐显结合的区域选择（高亮选择并返回 PickfirstSelectionSet）
- 参数: x1, y1, x2, y2, ty, select_mode
- 返回推断: object
- 关注点: COM, 时间/等待, 选择集
- 调用概览: li, sorted, SendCommand, sleep, Clear
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: SELECT-013。邻近注释提示：&&% 隐显结合的区域选择（高亮选择并返回 PickfirstSelectionSet）。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### set_entity_grip_state_precise(ent)
- 说明: 【函数编号】: SELECT-014
- 邻近注释: &&% 让对象处于夹点编辑状态
- 参数: ent
- 返回推断: NoneType,object
- 关注点: COM, 时间/等待, 选择集
- 调用概览: li, GetBoundingBox, select_entities_in_window, SendCommand, sleep, print
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: SELECT-014。邻近注释提示：&&% 让对象处于夹点编辑状态。实现特征：通过命令发送驱动 CAD 行为。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### safe_get_bbox(ent, max_retry, delay)
- 说明: 【函数编号】: COMMON-UTIL-003
- 邻近注释: 3 获取外包盒 | &&% 安全获取包围盒
- 参数: ent, max_retry, delay
- 返回推断: NoneType,tuple
- 关注点: COM, 几何, 时间/等待
- 调用概览: range, Update, GetBoundingBox, hasattr, list, sleep
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: COMMON-UTIL-003。邻近注释提示：3 获取外包盒；&&% 安全获取包围盒。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### _maybe_cast(ent)
- 说明: 【函数编号】: COMMON-OBJ-001-AUX
- 邻近注释: &&% 安全转换COM对象
- 参数: ent
- 返回推断: object
- 调用概览: com_retry, get, CastTo
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: COMMON-OBJ-001-AUX。邻近注释提示：&&% 安全转换COM对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### cast_object(obj)
- 说明: 【函数编号】: COMMON-OBJ-001
- 邻近注释: &&% 转换对象
- 参数: obj
- 返回推断: object
- 调用概览: _maybe_cast
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: COMMON-OBJ-001。邻近注释提示：&&% 转换对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_object_property(obj, property_name)
- 说明: 【函数编号】: COMMON-OBJ-002
- 邻近注释: &&% 获取对象属性
- 参数: obj, property_name
- 返回推断: NoneType,object
- 关注点: COM
- 调用概览: com_retry, _maybe_cast, getattr, get, Invoke
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: COMMON-OBJ-002。邻近注释提示：&&% 获取对象属性。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_object_property(obj, property_name, value)
- 说明: 【函数编号】: COMMON-OBJ-003
- 邻近注释: &&% 设置对象属性
- 参数: obj, property_name, value
- 返回推断: bool
- 关注点: COM
- 调用概览: com_retry, _maybe_cast, setattr, get, Invoke
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: COMMON-OBJ-003。邻近注释提示：&&% 设置对象属性。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_attr(obj, name)
- 说明: 【函数编号】: COMMON-OBJ-004
- 邻近注释: &&% 安全获取属性
- 参数: obj, name
- 返回推断: object
- 调用概览: get_object_property, getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：【函数编号】: COMMON-OBJ-004。邻近注释提示：&&% 安全获取属性。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_attr(obj, name, value)
- 说明: 【函数编号】: COMMON-OBJ-005
- 邻近注释: &&% 安全设置属性
- 参数: obj, name, value
- 返回推断: bool
- 调用概览: set_object_property, setattr
- 理解: 主要用于更新/设置相关逻辑。依据注释：【函数编号】: COMMON-OBJ-005。邻近注释提示：&&% 安全设置属性。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### brute_dump_tarch_props(ent, max_dispid)
- 说明: 【函数编号】: DEBUG-TARCH-001
- 邻近注释: 属性探测器 | &&% 暴力获取天正属性
- 参数: ent, max_dispid
- 关注点: COM
- 调用概览: getattr, print, range, InvokeTypes, repr
- 理解: 主要用于保存/写入相关逻辑。依据注释：【函数编号】: DEBUG-TARCH-001。邻近注释提示：属性探测器；&&% 暴力获取天正属性。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### sort_coms_by_llcorner(com_list, cha_Y)
- 说明: 【函数编号】: COMMON-SORT-001
- 邻近注释: 5排序 | &&% * 对列表实体进行从上到下、从左到右的排序 | &&% 左下角排序
- 参数: com_list, cha_Y
- 返回推断: object
- 调用概览: sort, append, GetBoundingBox, len, sorted, float, abs
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: COMMON-SORT-001。邻近注释提示：5排序；&&% * 对列表实体进行从上到下、从左到右的排序；&&% 左下角排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_rbcorner(com_list)
- 说明: 【函数编号】: COMMON-SORT-002
- 邻近注释: &&% 右上角排序
- 参数: com_list
- 返回推断: object
- 调用概览: sort, append, sorted, GetBoundingBox, len, float, abs
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: COMMON-SORT-002。邻近注释提示：&&% 右上角排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### sort_coms_by_center(objs, tol_x)
- 说明: 【函数编号】: COMMON-SORT-003
- 邻近注释: &&% 中心点排序
- 参数: objs, tol_x
- 返回推断: list,object
- 调用概览: sort, append, sorted, GetBoundingBox, extend, abs
- 理解: 主要用于处理相关逻辑。依据注释：【函数编号】: COMMON-SORT-003。邻近注释提示：&&% 中心点排序。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_point(pt)
- 说明: 【函数编号】: DRAW-001
- 邻近注释: ============================================================================== | 6 基本绘图 | &&% 绘制点
- 参数: pt
- 返回推断: NoneType,object
- 关注点: 几何
- 调用概览: AddPoint, vtpnt, print
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: DRAW-001。邻近注释提示：==============================================================================；6 基本绘图；&&% 绘制点。实现特征：创建点对象。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_line(p1, p2)
- 说明: 【函数编号】: DRAW-002
- 邻近注释: &&% 绘制直线
- 参数: p1, p2
- 返回推断: NoneType,object
- 调用概览: AddLine, vtpnt, print
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: DRAW-002。邻近注释提示：&&% 绘制直线。实现特征：创建直线对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_circle(center, radius)
- 说明: 【函数编号】: DRAW-003
- 邻近注释: &&% 绘制圆
- 参数: center, radius
- 返回推断: NoneType,object
- 调用概览: AddCircle, vtpnt, print
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: DRAW-003。邻近注释提示：&&% 绘制圆。实现特征：创建圆对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### draw_regular_polygon(center, radius, sides)
- 说明: 【函数编号】: DRAW-004
- 邻近注释: &&% 绘制正多边形
- 参数: center, radius, sides
- 返回推断: NoneType,object
- 关注点: COM, 几何
- 调用概览: range, print, extend, VARIANT, AddLightWeightPolyline, cos, sin
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: DRAW-004。邻近注释提示：&&% 绘制正多边形。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### draw_lwpolyline(coords3d, layer_name, width, color, closed)
- 说明: 【函数编号】: DRAW-005
- 参数: coords3d, layer_name, width, color, closed
- 返回推断: object
- 关注点: COM, 几何
- 调用概览: alias, VARIANT, Item, extend, AddLightWeightPolyline, bool, print, Add
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: DRAW-005。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### draw_polyline(vertices, layer_name, tol, width, color)
- 说明: 【函数编号】: DRAW-006
- 邻近注释: &&% 绘制多段线
- 参数: vertices, layer_name, tol, width, color
- 返回推断: NoneType,object
- 关注点: COM, 几何
- 调用概览: same_point, print, enumerate, VARIANT, extend, tuple, Item, AddPolyline, Update, Regen, isinstance, len...
- 理解: 主要用于创建/插入相关逻辑。依据注释：【函数编号】: DRAW-006。邻近注释提示：&&% 绘制多段线。实现特征：涉及图层操作。依赖 CAD COM 对象与当前文档/模型空间。涉及几何/多段线/包围盒处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

## scripts/测试.py
- 模块说明: （无）
### generate_relation_list(data_list)
- 说明: （无）
- 参数: data_list
- 返回推断: object
- 调用概览: enumerate, float, append, abs, min
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## scripts/脚本导航14版.py
- 模块说明: Script Navigator (Tree Edition) - BOM Fixed
### clean_old_logs()
- 说明: （无）
- 邻近注释: ========================================================================== | 清理非当天的日志文件
- 参数: （无）
- 关注点: 文件
- 调用概览: glob, dirname, join, split, date, today, remove, debug, strptime, str
- 理解: 主要用于处理相关逻辑。邻近注释提示：==========================================================================；清理非当天的日志文件。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### _normalize_registry_path(path)
- 说明: （无）
- 参数: path
- 返回推断: NoneType,object
- 关注点: 文件
- 调用概览: str, resolve, abspath, Path
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### _pid_exists(pid)
- 说明: （无）
- 参数: pid
- 返回推断: bool
- 关注点: COM, 窗口/输入, 进程
- 调用概览: startswith, getpid, OpenProcess, kill, isinstance, CloseHandle
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。包含窗口/输入自动化。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；依赖窗口/输入焦点，易受环境影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；窗口不可见/无焦点/多屏环境

### _read_registry_data()
- 说明: （无）
- 参数: （无）
- 返回推断: dict,object
- 关注点: 文件
- 调用概览: exists, loads, isinstance, read_text, debug
- 理解: 主要用于打开/读取相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### _write_registry_data(data)
- 说明: （无）
- 参数: data
- 关注点: 文件
- 调用概览: write_text, dumps, debug
- 理解: 主要用于保存/写入相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### _cleanup_registry_data(data)
- 说明: （无）
- 参数: data
- 返回推断: object
- 调用概览: list, keys, get, set, isinstance, pop, add, append, _pid_exists
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _load_clean_registry()
- 说明: （无）
- 参数: （无）
- 返回推断: object
- 关注点: 文件
- 调用概览: _read_registry_data, _cleanup_registry_data, _write_registry_data
- 理解: 主要用于打开/读取相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### parse_mark_line(raw)
- 说明: （无）
- 邻近注释: ================== 解析器 ==================
- 参数: raw
- 返回推断: NoneType,tuple
- 调用概览: lstrip, startswith, strip, len
- 理解: 主要用于转换/解析相关逻辑。邻近注释提示：================== 解析器 ==================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### is_file_in_use(filepath)
- 说明: （无）
- 参数: filepath
- 返回推断: bool
- 关注点: 文件, 进程
- 调用概览: normcase, getpid, process_iter, warning, abspath, getattr, exists, debug, info
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### _tree_walk(tree, parent)
- 说明: （无）
- 参数: tree, parent
- 调用概览: get_children, _tree_walk
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator.__init__(self, script_path)
- 说明: （无）
- 参数: self, script_path
- 关注点: 文件
- 调用概览: __init__, debug, clean_old_logs, _ensure_idle_bootstrap, title, geometry, protocol, _build_ui, _bind_shortcuts, isfile, load_script, super...
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._ensure_idle_bootstrap(self)
- 说明: 检查并更新/创建 IDLE_bootstrap.py 文件
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: info, open, write, error, showwarning
- 理解: 主要用于处理相关逻辑。依据注释：检查并更新/创建 IDLE_bootstrap.py 文件。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._build_ui(self)
- 说明: （无）
- 邻近注释: ---------- UI ----------
- 参数: self
- 关注点: UI/Tk, 文件, 选择集
- 调用概览: debug, PanedWindow, pack, Frame, add, Treeview, Scrollbar, configure, bind, Text, tag_config, tag_bind...
- 理解: 主要用于处理相关逻辑。邻近注释提示：---------- UI ----------。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### ScriptNavigator._bind_shortcuts(self)
- 说明: （无）
- 邻近注释: ---------- 快捷键 ----------
- 参数: self
- 调用概览: bind_all, bind, _comment_selection, _uncomment_selection, _open_new_file, save_script, run_in_idle, _find_dialog, _find_next, _find_prev, goto_line_prompt, _unindent...
- 理解: 主要用于处理相关逻辑。邻近注释提示：---------- 快捷键 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._apply_fonts(self)
- 说明: （无）
- 邻近注释: ---------- 字体/缩放 ----------
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: nametofont, configure, copy, Style, tag_config, after, tag_configure
- 理解: 主要用于处理相关逻辑。邻近注释提示：---------- 字体/缩放 ----------。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._zoom_in(self)
- 说明: （无）
- 参数: self
- 调用概览: min, _apply_fonts, _refresh_nav
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._zoom_out(self)
- 说明: （无）
- 参数: self
- 调用概览: max, _apply_fonts, _refresh_nav
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._on_mousewheel_zoom(self, e)
- 说明: （无）
- 参数: self, e
- 返回推断: str
- 调用概览: _zoom_in, _zoom_out
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._on_mousewheel_sync(self, _)
- 说明: （无）
- 邻近注释: ---------- 滚动同步 ----------
- 参数: self, _
- 调用概览: after_idle
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：---------- 滚动同步 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._on_scrollbar(self, *args)
- 说明: （无）
- 参数: self, *args
- 调用概览: yview, update_line_numbers
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._on_code_yscroll(self, *args)
- 说明: （无）
- 参数: self, *args
- 关注点: 文件
- 调用概览: set, yview_moveto, after_idle
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._schedule_line_numbers(self)
- 说明: （无）
- 邻近注释: ---------- 行号 ----------
- 参数: self
- 调用概览: after_idle
- 理解: 主要用于处理相关逻辑。邻近注释提示：---------- 行号 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator.update_line_numbers(self)
- 说明: （无）
- 参数: self
- 返回推断: None
- 调用概览: int, min, max, join, config, delete, insert, len, split, str, range, index...
- 理解: 主要用于更新/设置相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._on_key_release_update(self, _)
- 说明: （无）
- 邻近注释: ---------- 内容修改 / 导航刷新 ----------
- 参数: self, _
- 调用概览: _schedule_line_numbers
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：---------- 内容修改 / 导航刷新 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._on_text_modified(self, _)
- 说明: （无）
- 参数: self, _
- 关注点: 文件
- 调用概览: edit_modified, _schedule_line_numbers, _schedule_nav_refresh, _scan_for_markers, _clear_nav_and_code_highlight, selection_remove, selection
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._schedule_nav_refresh(self, delay)
- 说明: （无）
- 参数: self, delay
- 调用概览: after, after_cancel
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._content_signature(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: get, hexdigest, md5, len, encode
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._maybe_refresh_nav(self)
- 说明: （无）
- 参数: self
- 调用概览: _content_signature, _refresh_nav
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._open_script(self)
- 说明: （无）
- 邻近注释: ---------- 文件 ----------
- 参数: self
- 调用概览: askopenfilename, load_script
- 理解: 主要用于打开/读取相关逻辑。邻近注释提示：---------- 文件 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._open_new_file(self)
- 说明: （无）
- 参数: self
- 调用概览: _open_script
- 理解: 主要用于打开/读取相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator.load_script(self, path)
- 说明: （无）
- 参数: self, path
- 返回推断: None
- 关注点: UI/Tk, 文件
- 调用概览: _normalize_registry_path, delete, insert, edit_reset, title, _content_signature, _refresh_nav, update_line_numbers, _scan_for_markers, _register_file_session, getmtime, hexdigest...
- 理解: 主要用于打开/读取相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._register_file_session(self, normalized_path)
- 说明: （无）
- 参数: self, normalized_path
- 返回推断: None
- 关注点: 文件
- 调用概览: _load_clean_registry, list, get, getpid, append, _write_registry_data
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._unregister_current_file(self)
- 说明: （无）
- 参数: self
- 返回推断: None
- 关注点: 文件
- 调用概览: _load_clean_registry, _write_registry_data, pop, getpid
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator.save_script(self)
- 说明: （无）
- 参数: self
- 返回推断: bool
- 关注点: UI/Tk, 文件
- 调用概览: _open_script, askyesno, get, getmtime, hexdigest, _content_signature, _refresh_nav, _scan_for_markers, showinfo, open, write, error...
- 理解: 主要用于保存/写入相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._format_nav_label(self, lineno, label)
- 说明: （无）
- 邻近注释: ---------- 导航 ----------
- 参数: self, lineno, label
- 返回推断: object
- 理解: 主要用于处理相关逻辑。邻近注释提示：---------- 导航 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._refresh_nav(self)
- 说明: （无）
- 参数: self
- 调用概览: set, _tree_walk, get_children, clear, splitlines, len, max, enumerate, _auto_resize_nav, get, item, delete...
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._collapse_all(self)
- 说明: （无）
- 参数: self
- 调用概览: get_children, item
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._expand_all(self)
- 说明: （无）
- 参数: self
- 调用概览: get_children, item, open_rec
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._on_tree_select(self, _)
- 说明: （无）
- 参数: self, _
- 返回推断: None
- 关注点: 选择集
- 调用概览: selection, get, _nav_select_and_highlight
- 理解: 主要用于获取/选择相关逻辑。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### ScriptNavigator._nav_select_and_highlight(self, iid, line_no)
- 说明: （无）
- 参数: self, iid, line_no
- 关注点: 选择集
- 调用概览: _clear_nav_highlight_only, _add_nav_tag, _highlight_line
- 理解: 主要用于获取/选择相关逻辑。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### ScriptNavigator._highlight_line(self, ln, source)
- 说明: （无）
- 参数: self, ln, source
- 关注点: 文件
- 调用概览: tag_remove, see, tag_add, update_line_numbers, update_idletasks, after
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._auto_resize_nav(self)
- 说明: （无）
- 参数: self
- 关注点: UI/Tk
- 调用概览: metrics, Style, configure, iter_nodes, measure, max, update_idletasks, nametofont, get_children, min, column, int...
- 理解: 主要用于处理相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### ScriptNavigator._indent(self, event)
- 说明: （无）
- 邻近注释: ---------- 缩进 ----------
- 参数: self, event
- 返回推断: str
- 调用概览: index, int, range, insert, split
- 理解: 主要用于处理相关逻辑。邻近注释提示：---------- 缩进 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._unindent(self, event)
- 说明: （无）
- 参数: self, event
- 返回推断: str
- 调用概览: range, index, int, get, min, delete, split, len, lstrip
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._comment_selection(self, event)
- 说明: （无）
- 邻近注释: ---------- 批量注释 ----------
- 参数: self, event
- 返回推断: str
- 调用概览: _get_selection_line_range, edit_separator, range, get, _leading_ws_len, insert
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：---------- 批量注释 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._uncomment_selection(self, event)
- 说明: （无）
- 参数: self, event
- 返回推断: str
- 关注点: 文件
- 调用概览: _get_selection_line_range, edit_separator, range, get, _leading_ws_len, delete
- 理解: 主要用于获取/选择相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._get_selection_line_range(self)
- 说明: （无）
- 参数: self
- 返回推断: NoneType,tuple
- 关注点: UI/Tk
- 调用概览: int, index, showinfo, split
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 依赖图形界面环境
- 测试点: 参数合法性与边界值

### ScriptNavigator._leading_ws_len(text)
- 说明: （无）
- 参数: text
- 返回推断: object
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._find_dialog(self, _)
- 说明: （无）
- 邻近注释: ---------- 查找/复制/跳转 ----------
- 参数: self, _
- 返回推断: str
- 调用概览: askstring, _do_find
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：---------- 查找/复制/跳转 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._do_find(self, key)
- 说明: （无）
- 参数: self, key
- 返回推断: None
- 关注点: UI/Tk, 文件
- 调用概览: tag_remove, clear, _go_to_match, search, append, tag_add, showinfo, len
- 理解: 主要用于获取/选择相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._go_to_match(self)
- 说明: （无）
- 参数: self
- 调用概览: int, _highlight_line, split
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._find_next(self, _)
- 说明: （无）
- 参数: self, _
- 返回推断: str
- 调用概览: _go_to_match, len
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._find_prev(self, _)
- 说明: （无）
- 参数: self, _
- 返回推断: str
- 调用概览: _go_to_match, len
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._copy_all(self)
- 说明: （无）
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: clipboard_clear, clipboard_append, showinfo, get
- 理解: 主要用于移动/复制相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._copy_sel(self)
- 说明: （无）
- 参数: self
- 关注点: UI/Tk, 文件
- 调用概览: get, showwarning, clipboard_clear, clipboard_append, showinfo
- 理解: 主要用于移动/复制相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator.goto_line_prompt(self)
- 说明: （无）
- 参数: self
- 调用概览: int, askinteger, float, _highlight_line, split, index
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator.run_in_idle(self)
- 说明: （无）
- 邻近注释: ---------- 运行 ----------
- 参数: self
- 返回推断: None
- 关注点: UI/Tk, 文件, 时间/等待, 进程, 选择集
- 调用概览: showwarning, save_script, _send_script_to_idle, debug, startswith, Popen, sleep, error, showerror, poll, exists, _ensure_idle_bootstrap...
- 理解: 主要用于处理相关逻辑。邻近注释提示：---------- 运行 ----------。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；超时与重试次数边界

### ScriptNavigator._send_script_to_idle(self, script_path)
- 说明: （无）
- 参数: self, script_path
- 返回推断: bool
- 关注点: UI/Tk, 时间/等待, 网络
- 调用概览: range, socket, settimeout, connect, sendall, debug, showerror, encode, sleep, str
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 包含等待/阻塞逻辑，可能超时；依赖图形界面环境；涉及网络请求，需考虑超时与异常
- 测试点: 参数合法性与边界值；超时与重试次数边界

### ScriptNavigator._on_close(self)
- 说明: （无）
- 邻近注释: ---------- 关闭 ----------
- 参数: self
- 调用概览: _unregister_current_file, destroy, exit, terminate, poll
- 理解: 主要用于关闭/终止相关逻辑。邻近注释提示：---------- 关闭 ----------。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._add_nav_tag(self, iid, tag)
- 说明: （无）
- 邻近注释: ================== 辅助函数 ==================
- 参数: self, iid, tag
- 调用概览: list, item, append, tuple
- 理解: 主要用于创建/插入相关逻辑。邻近注释提示：================== 辅助函数 ==================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._remove_nav_tag(self, iid, tag)
- 说明: （无）
- 参数: self, iid, tag
- 关注点: 文件
- 调用概览: item, tuple
- 理解: 主要用于删除/清理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._clear_nav_highlight_only(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: exists, _remove_nav_tag
- 理解: 主要用于删除/清理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._clear_nav_and_code_highlight(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: _clear_nav_highlight_only, tag_remove
- 理解: 主要用于删除/清理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._scan_for_markers(self)
- 说明: （无）
- 参数: self
- 关注点: 文件
- 调用概览: tag_remove, clear, get, splitlines, finditer, group, count, strip, start, tag_add, rfind, int...
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._on_click_image_marker(self, event)
- 说明: （无）
- 参数: self, event
- 关注点: 文件
- 调用概览: index, tag_names, startswith, get, isfile, _show_image_popup
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._show_image_popup(self, path, event)
- 说明: （无）
- 参数: self, path, event
- 返回推断: None
- 关注点: UI/Tk, 文件
- 调用概览: _hide_image_popup, open, winfo_screenwidth, winfo_screenheight, int, resize, PhotoImage, Toplevel, title, attributes, Frame, pack...
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._hide_image_popup(self)
- 说明: （无）
- 参数: self
- 调用概览: destroy
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._toggle_maximize(self, event)
- 说明: （无）
- 参数: self, event
- 返回推断: None
- 调用概览: update_idletasks, geometry, winfo_screenwidth, winfo_screenheight
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ScriptNavigator._on_popup_mousewheel(self, event)
- 说明: （无）
- 参数: self, event
- 返回推断: None
- 关注点: UI/Tk, 文件
- 调用概览: canvasx, canvasy, int, resize, PhotoImage, itemconfig, configure, winfo_width, winfo_height, max, xview_moveto, yview_moveto...
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖图形界面环境
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### ScriptNavigator._on_click_link(self, event)
- 说明: （无）
- 参数: self, event
- 关注点: 文件
- 调用概览: index, tag_names, get, startswith, isdigit, yview, _highlight_line, after, yview_moveto, len
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

## system/CAD_com_utils - V10.py
- 模块说明: （无）
### _retry_logic(max_retries, base_delay, func, *args, **kwargs)
- 说明: 实际执行重试的内部函数
- 邻近注释: ================= 2. 核心重试逻辑实现 =================
- 参数: max_retries, base_delay, func, *args, **kwargs
- 返回推断: object
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: range, critical, func, str, getattr, any, error, warning, sleep, PumpWaitingMessages
- 理解: 主要用于等待/守护相关逻辑。依据注释：实际执行重试的内部函数。邻近注释提示：================= 2. 核心重试逻辑实现 =================。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### retry_on_busy(func_or_retries, max_retries, base_delay)
- 说明: 【智能通用装饰器】
- 邻近注释: ================= 3. 智能装饰器 (修正版) =================
- 参数: func_or_retries, max_retries, base_delay
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: callable, isinstance, decorator_factory, wraps, _retry_logic
- 理解: 主要用于等待/守护相关逻辑。依据注释：【智能通用装饰器】。邻近注释提示：================= 3. 智能装饰器 (修正版) =================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### SafeCOM.call(func, *args, **kwargs)
- 说明: （无）
- 参数: func, *args, **kwargs
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: retry_on_busy
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### SafeCOM.list_selection(ss)
- 说明: （无）
- 参数: ss
- 返回推断: list,object
- 关注点: 日志/测试, 选择集
- 关键调用: retry_on_busy, SafeCOM
- 调用概览: retry_on_busy, list, _to_list, error
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### retry_if_busy(max_retries, delay)
- 说明: 【兼容补丁】旧接口：retry_if_busy
- 邻近注释: ================= 4. 向下兼容接口 =================
- 参数: max_retries, delay
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: retry_on_busy
- 理解: 主要用于等待/守护相关逻辑。依据注释：【兼容补丁】旧接口：retry_if_busy。邻近注释提示：================= 4. 向下兼容接口 =================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## system/CAD_com_utils.py
- 模块说明: 引入 silent_mode 上下文管理器。
### _dummy_func(*args, **kwargs)
- 说明: （无）
- 邻近注释: 定义空函数 (No-op)，用于静音时的极致性能
- 参数: *args, **kwargs
- 理解: 主要用于处理相关逻辑。邻近注释提示：定义空函数 (No-op)，用于静音时的极致性能。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LoggerHotSwapper.__init__(self, original_logger)
- 说明: （无）
- 参数: self, original_logger
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LoggerHotSwapper.mute(self)
- 说明: 开启静音：将 info/debug 指向空函数
- 参数: self
- 理解: 主要用于处理相关逻辑。依据注释：开启静音：将 info/debug 指向空函数。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LoggerHotSwapper.unmute(self)
- 说明: 解除静音：恢复原始函数
- 参数: self
- 理解: 主要用于处理相关逻辑。依据注释：解除静音：恢复原始函数。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LoggerHotSwapper.mute_mode(self)
- 说明: 获取当前静音状态 (True/False)
- 参数: self
- 返回推断: object
- 理解: 主要用于处理相关逻辑。依据注释：获取当前静音状态 (True/False)。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LoggerHotSwapper.mute_mode(self, value)
- 说明: 设置静音状态
- 参数: self, value
- 关注点: 日志/测试
- 调用概览: mute, unmute
- 理解: 主要用于处理相关逻辑。依据注释：设置静音状态。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### LoggerHotSwapper.__getattr__(self, name)
- 说明: （无）
- 参数: self, name
- 返回推断: object
- 调用概览: getattr
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### silent_mode()
- 说明: 【静音模式上下文】
- 参数: （无）
- 关注点: 日志/测试
- 调用概览: mute, unmute
- 理解: 主要用于处理相关逻辑。依据注释：【静音模式上下文】。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _retry_logic(max_retries, base_delay, func, *args, **kwargs)
- 说明: 实际执行重试的内部函数
- 邻近注释: ================= 3. 核心重试逻辑实现 =================
- 参数: max_retries, base_delay, func, *args, **kwargs
- 返回推断: object
- 关注点: COM, 日志/测试, 时间/等待
- 调用概览: range, critical, func, str, getattr, any, warning, sleep, error, PumpWaitingMessages
- 理解: 主要用于等待/守护相关逻辑。依据注释：实际执行重试的内部函数。邻近注释提示：================= 3. 核心重试逻辑实现 =================。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### retry_on_busy(func_or_retries, max_retries, base_delay)
- 说明: 【智能通用装饰器】
- 邻近注释: ================= 4. 智能装饰器 =================
- 参数: func_or_retries, max_retries, base_delay
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: callable, isinstance, decorator_factory, wraps, _retry_logic
- 理解: 主要用于等待/守护相关逻辑。依据注释：【智能通用装饰器】。邻近注释提示：================= 4. 智能装饰器 =================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### SafeCOM.call(func, *args, **kwargs)
- 说明: （无）
- 参数: func, *args, **kwargs
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: retry_on_busy
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### SafeCOM.list_selection(ss)
- 说明: （无）
- 参数: ss
- 返回推断: list,object
- 关注点: 日志/测试
- 关键调用: retry_on_busy, SafeCOM
- 调用概览: retry_on_busy, list, _to_list, error
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### retry_if_busy(max_retries, delay)
- 说明: （无）
- 邻近注释: ================= 5. 向下兼容接口 =================
- 参数: max_retries, delay
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: retry_on_busy
- 理解: 主要用于等待/守护相关逻辑。邻近注释提示：================= 5. 向下兼容接口 =================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### alias(*names)
- 说明: @alias("别名1","别名2",…)
- 邻近注释: &&% 函数别名
- 参数: *names
- 返回推断: object
- 调用概览: setattr
- 理解: 主要用于处理相关逻辑。依据注释：@alias("别名1","别名2",…)。邻近注释提示：&&% 函数别名。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### node(msg, *args, **kwargs)
- 说明: 只有 DEBUG = True 且当前帧属于【栈底】函数时才打印。
- 参数: msg, *args, **kwargs
- 返回推断: None
- 调用概览: currentframe, _orig_print, format
- 理解: 主要用于处理相关逻辑。依据注释：只有 DEBUG = True 且当前帧属于【栈底】函数时才打印。。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### timeit(func)
- 说明: 【耗时统计】
- 参数: func
- 返回推断: object
- 关注点: 文件, 日志/测试
- 调用概览: wraps, time, globals, info, func, warning, error
- 理解: 主要用于处理相关逻辑。依据注释：【耗时统计】。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### debuggable(func)
- 说明: 【调试标记】
- 参数: func
- 返回推断: object
- 调用概览: wraps, func
- 理解: 主要用于处理相关逻辑。依据注释：【调试标记】。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## system/cad_command_monitor.py
- 模块说明: （无）
### force_bring_to_front(hwnd)
- 说明: 【霸道操作】强制将窗口置顶并获取焦点
- 邻近注释: ================= 窗口控制增强 =================
- 参数: hwnd
- 返回推断: bool
- 关注点: 时间/等待, 窗口/输入, 选择集
- 调用概览: IsIconic, keybd_event, SetForegroundWindow, sleep, IsWindow, ShowWindow, error
- 理解: 主要用于处理相关逻辑。依据注释：【霸道操作】强制将窗口置顶并获取焦点。邻近注释提示：================= 窗口控制增强 =================。包含选择集构造或过滤。
- 风险: 依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### send_nuclear_esc(hwnd, acad_doc)
- 说明: 先抢焦点，再按 ESC
- 参数: hwnd, acad_doc
- 返回推断: bool
- 关注点: COM, 时间/等待, 窗口/输入
- 调用概览: warning, info, force_bring_to_front, range, keybd_event, sleep, PostMessage, error, SendCommand, chr
- 理解: 主要用于关闭/终止相关逻辑。依据注释：先抢焦点，再按 ESC。实现特征：通过命令发送驱动 CAD 行为。包含窗口/输入自动化。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；窗口不可见/无焦点/多屏环境；超时与重试次数边界

### get_active_cad_app()
- 说明: （无）
- 参数: （无）
- 返回推断: NoneType,object
- 关注点: COM, 进程
- 调用概览: CoInitialize, GetActiveObject
- 理解: 主要用于获取/选择相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### analyze_state(acad)
- 说明: V5.0+ 逻辑：吞掉 Call Rejected，判定为 BUSY
- 参数: acad
- 返回推断: tuple
- 关注点: COM
- 调用概览: GetVariable, str, strip
- 理解: 主要用于处理相关逻辑。依据注释：V5.0+ 逻辑：吞掉 Call Rejected，判定为 BUSY。实现特征：涉及系统变量读取/设置。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### is_already_running()
- 说明: （无）
- 参数: （无）
- 返回推断: bool
- 关注点: 文件, 进程
- 调用概览: unlink, exists, int, pid_exists, strip, Process, read_text, lower, join, cmdline, name
- 理解: 主要用于打开/读取相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### create_lock()
- 说明: （无）
- 参数: （无）
- 关注点: 文件
- 调用概览: write_text, str, getpid
- 理解: 主要用于创建/插入相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### remove_lock()
- 说明: （无）
- 参数: （无）
- 关注点: 文件
- 调用概览: unlink
- 理解: 主要用于删除/清理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### main()
- 说明: （无）
- 邻近注释: ================= 主循环 =================
- 参数: （无）
- 返回推断: None
- 关注点: 文件, 时间/等待, 窗口/输入, 选择集
- 调用概览: is_already_running, create_lock, print, info, remove_lock, time, get_active_cad_app, analyze_state, max, sleep, error, write...
- 理解: 主要用于处理相关逻辑。邻近注释提示：================= 主循环 =================。包含选择集构造或过滤。包含文件读写或路径处理。包含窗口/输入自动化。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；依赖窗口/输入焦点，易受环境影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；空选择集/选择集异常对象；窗口不可见/无焦点/多屏环境；超时与重试次数边界

## system/CAD_coordination - V33.py
- 模块说明: CAD运行协同机制模块 (Licad + Logger 集成终极版)
### wait_quiescent(min_quiet, timeout)
- 说明: 【等待空闲】基于 Licad.C 的智能检测 (增强版)
- 邻近注释: ================= 3. 核心协同函数 =================
- 参数: min_quiet, timeout
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: wait_quiescent
- 调用概览: time, warning, sleep, hasattr, stack, int, GetVariable, error, critical, debug, info, strip...
- 理解: 主要用于等待/守护相关逻辑。依据注释：【等待空闲】基于 Licad.C 的智能检测 (增强版)。邻近注释提示：================= 3. 核心协同函数 =================。实现特征：包含空闲等待以同步 CAD 状态；涉及系统变量读取/设置；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### CADGuard.__init__(self, task_name, wait_before, wait_after, timeout, disable_ui, independent_undo)
- 说明: （无）
- 参数: self, task_name, wait_before, wait_after, timeout, disable_ui, independent_undo
- 关注点: 时间/等待
- 理解: 主要用于处理相关逻辑。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### CADGuard.__enter__(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 关注点: 日志/测试, 时间/等待
- 关键调用: wait_quiescent, C.li, C.doc
- 调用概览: time, info, li, RuntimeError, wait_quiescent, StartUndoMark
- 理解: 主要用于处理相关逻辑。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### CADGuard.__exit__(self, exc_type, exc_val, exc_tb)
- 说明: （无）
- 参数: self, exc_type, exc_val, exc_tb
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: wait_quiescent
- 调用概览: time, error, info, warning, Regen, EndUndoMark, SendCommand, Update, wait_quiescent
- 理解: 主要用于处理相关逻辑。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### FileGuard.__init__(self, file_path)
- 说明: （无）
- 参数: self, file_path
- 关注点: 文件
- 调用概览: resolve, with_suffix, Path
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### FileGuard.__enter__(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 关注点: 文件, 日志/测试
- 调用概览: info, exists, FileNotFoundError, copy2, error
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### FileGuard.set_success(self)
- 说明: 显式标记为成功
- 参数: self
- 理解: 主要用于更新/设置相关逻辑。依据注释：显式标记为成功。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### FileGuard.__exit__(self, exc_type, exc_val, exc_tb)
- 说明: （无）
- 参数: self, exc_type, exc_val, exc_tb
- 关注点: 文件, 日志/测试, 时间/等待
- 调用概览: info, error, warning, sleep, exists, close_all_cad_processes, remove, critical, move, str
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### run_safety_loop(target_dwg, action_func, check_func, max_retries)
- 说明: 【核弹级安全执行循环】
- 邻近注释: ========================================================================= | 门神三号：安全循环 (把上面两个串起来) | =========================================================================
- 参数: target_dwg, action_func, check_func, max_retries
- 返回推断: bool
- 关注点: 几何, 文件, 日志/测试, 时间/等待
- 调用概览: Path, range, info, FileGuard, open_file, action_func, check_func, warning, str, set_success, RuntimeError, sleep...
- 理解: 主要用于处理相关逻辑。依据注释：【核弹级安全执行循环】。邻近注释提示：=========================================================================；门神三号：安全循环 (把上面两个串起来)；=========================================================================。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### send_cmd_with_sync(cmd, wait_after, timeout)
- 说明: 【发送命令】带同步等待
- 参数: cmd, wait_after, timeout
- 返回推断: bool,object
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: send_cmd_with_sync, wait_quiescent, C.acad
- 调用概览: wait_quiescent, error, SendCommand, info, sleep, endswith, strip
- 理解: 主要用于关闭/终止相关逻辑。依据注释：【发送命令】带同步等待。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### wait_document_opened(path, timeout)
- 说明: 等待文档加载
- 参数: path, timeout
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 关键调用: C.acad
- 调用概览: time, lower, info, warning, sleep, str, resolve, Path, range, Item
- 理解: 主要用于打开/读取相关逻辑。依据注释：等待文档加载。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### ensure_single_process()
- 说明: 进程清理
- 邻近注释: ================= 4. 进程与启动 =================
- 参数: （无）
- 返回推断: bool
- 关注点: 日志/测试, 进程
- 调用概览: sorted, len, warning, process_iter, terminate, lower
- 理解: 主要用于处理相关逻辑。依据注释：进程清理。邻近注释提示：================= 4. 进程与启动 =================。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### start_cad_with_dialog_killer()
- 说明: 启动 CAD
- 参数: （无）
- 返回推断: bool,object
- 关注点: 日志/测试, 时间/等待
- 关键调用: wait_quiescent
- 调用概览: info, start_applicationV9, wait_quiescent
- 理解: 主要用于关闭/终止相关逻辑。依据注释：启动 CAD。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### wait_command_done(timeout, poll_interval, quiet_time)
- 说明: （无）
- 邻近注释: ================= 5. 兼容接口 =================
- 参数: timeout, poll_interval, quiet_time
- 返回推断: object
- 关注点: 时间/等待
- 关键调用: wait_quiescent
- 调用概览: wait_quiescent
- 理解: 主要用于等待/守护相关逻辑。邻近注释提示：================= 5. 兼容接口 =================。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

## system/CAD_coordination.py
- 模块说明: CAD运行协同机制模块 (Licad + Logger 集成终极版)
### wait_quiescent(min_quiet, timeout)
- 说明: 【等待空闲】基于 Licad.C 的智能检测
- 邻近注释: ================= 3. 核心协同函数 =================
- 参数: min_quiet, timeout
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: wait_quiescent
- 调用概览: time, warning, sleep, stack, int, GetVariable, error, strip, str
- 理解: 主要用于等待/守护相关逻辑。依据注释：【等待空闲】基于 Licad.C 的智能检测。邻近注释提示：================= 3. 核心协同函数 =================。实现特征：包含空闲等待以同步 CAD 状态；涉及系统变量读取/设置。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### wait_quiescent(min_quiet, timeout)
- 说明: 【等待空闲】V3.2 稳健版 + 效能报告
- 邻近注释: &&% 20260114
- 参数: min_quiet, timeout
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: wait_quiescent
- 调用概览: time, warning, sleep, hasattr, stack, int, GetVariable, error, info, strip, str
- 理解: 主要用于等待/守护相关逻辑。依据注释：【等待空闲】V3.2 稳健版 + 效能报告。邻近注释提示：&&% 20260114。实现特征：包含空闲等待以同步 CAD 状态；涉及系统变量读取/设置。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### CADGuard.__init__(self, task_name, wait_before, wait_after, timeout, disable_ui, independent_undo)
- 说明: （无）
- 参数: self, task_name, wait_before, wait_after, timeout, disable_ui, independent_undo
- 关注点: 时间/等待
- 理解: 主要用于处理相关逻辑。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### CADGuard.__enter__(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 关注点: 日志/测试, 时间/等待
- 关键调用: wait_quiescent, C.li, C.doc
- 调用概览: time, info, li, RuntimeError, wait_quiescent, StartUndoMark
- 理解: 主要用于处理相关逻辑。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### CADGuard.__exit__(self, exc_type, exc_val, exc_tb)
- 说明: （无）
- 参数: self, exc_type, exc_val, exc_tb
- 返回推断: bool
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: wait_quiescent
- 调用概览: time, error, info, warning, Regen, EndUndoMark, SendCommand, Update, wait_quiescent
- 理解: 主要用于处理相关逻辑。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### FileGuard.__init__(self, file_path)
- 说明: （无）
- 参数: self, file_path
- 关注点: 文件
- 调用概览: resolve, with_suffix, Path
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### FileGuard.__enter__(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 关注点: 文件, 日志/测试
- 调用概览: info, exists, FileNotFoundError, copy2, error
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### FileGuard.set_success(self)
- 说明: 显式标记为成功
- 参数: self
- 理解: 主要用于更新/设置相关逻辑。依据注释：显式标记为成功。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### FileGuard.__exit__(self, exc_type, exc_val, exc_tb)
- 说明: （无）
- 参数: self, exc_type, exc_val, exc_tb
- 关注点: 文件, 日志/测试, 时间/等待
- 调用概览: info, error, warning, sleep, exists, close_all_cad_processes, remove, critical, move, str
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### run_safety_loop(target_dwg, action_func, check_func, max_retries)
- 说明: 【核弹级安全执行循环】
- 邻近注释: ========================================================================= | 门神三号：安全循环 (把上面两个串起来) | =========================================================================
- 参数: target_dwg, action_func, check_func, max_retries
- 返回推断: bool
- 关注点: 几何, 文件, 日志/测试, 时间/等待
- 调用概览: Path, range, info, FileGuard, open_file, action_func, check_func, warning, str, set_success, RuntimeError, sleep...
- 理解: 主要用于处理相关逻辑。依据注释：【核弹级安全执行循环】。邻近注释提示：=========================================================================；门神三号：安全循环 (把上面两个串起来)；=========================================================================。涉及几何/多段线/包围盒处理。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### send_cmd_with_sync(cmd, wait_after, timeout)
- 说明: 【发送命令】带同步等待
- 参数: cmd, wait_after, timeout
- 返回推断: bool,object
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: send_cmd_with_sync, wait_quiescent, C.acad
- 调用概览: wait_quiescent, error, SendCommand, info, sleep, endswith, strip
- 理解: 主要用于关闭/终止相关逻辑。依据注释：【发送命令】带同步等待。实现特征：包含空闲等待以同步 CAD 状态；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### wait_document_opened(path, timeout)
- 说明: 等待文档加载
- 参数: path, timeout
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试, 时间/等待
- 关键调用: C.acad
- 调用概览: time, lower, info, warning, sleep, str, resolve, Path, range, Item
- 理解: 主要用于打开/读取相关逻辑。依据注释：等待文档加载。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### ensure_single_process()
- 说明: 进程清理
- 邻近注释: ================= 4. 进程与启动 =================
- 参数: （无）
- 返回推断: bool
- 关注点: 日志/测试, 进程
- 调用概览: sorted, len, warning, process_iter, terminate, lower
- 理解: 主要用于处理相关逻辑。依据注释：进程清理。邻近注释提示：================= 4. 进程与启动 =================。
- 风险: 涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值

### start_cad_with_dialog_killer()
- 说明: 启动 CAD
- 参数: （无）
- 返回推断: bool,object
- 关注点: 日志/测试, 时间/等待
- 关键调用: wait_quiescent
- 调用概览: info, start_applicationV9, wait_quiescent
- 理解: 主要用于关闭/终止相关逻辑。依据注释：启动 CAD。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### wait_command_done(timeout, poll_interval, quiet_time)
- 说明: （无）
- 邻近注释: ================= 5. 兼容接口 =================
- 参数: timeout, poll_interval, quiet_time
- 返回推断: object
- 关注点: 时间/等待
- 关键调用: wait_quiescent
- 调用概览: wait_quiescent
- 理解: 主要用于等待/守护相关逻辑。邻近注释提示：================= 5. 兼容接口 =================。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

## system/CAD_selection - V10.py
- 模块说明: （无）
### com_retry(fn, retries, delay)
- 说明: （无）
- 参数: fn, retries, delay
- 返回推断: object
- 关注点: 时间/等待
- 调用概览: range, fn, sleep
- 理解: 主要用于等待/守护相关逻辑。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### cast_object(obj)
- 说明: 【CORE-002-1】智能类型转换 (终极混合模式)
- 参数: obj
- 返回推断: object
- 调用概览: _maybe_cast
- 理解: 主要用于处理相关逻辑。依据注释：【CORE-002-1】智能类型转换 (终极混合模式)。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _maybe_cast(ent)
- 说明: 【CORE-002】智能类型转换 (终极混合模式)
- 参数: ent
- 返回推断: NoneType,object
- 关注点: COM, 进程
- 调用概览: hasattr, EnsureDispatch, getattr, CastTo, startswith, Dispatch
- 理解: 主要用于处理相关逻辑。依据注释：【CORE-002】智能类型转换 (终极混合模式)。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### to_vt_int(seq)
- 说明: （无）
- 邻近注释: --- 内部辅助 ---
- 参数: seq
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT, list
- 理解: 主要用于处理相关逻辑。邻近注释提示：--- 内部辅助 ---。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### to_vt_variant(seq)
- 说明: （无）
- 参数: seq
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT, list
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### _to_vt_point(pt_tuple)
- 说明: （无）
- 参数: pt_tuple
- 返回推断: NoneType,object
- 关注点: COM
- 调用概览: VARIANT, float
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### pt3(x, y, z)
- 说明: （无）
- 参数: x, y, z
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### normalize_rect(x1, y1, x2, y2)
- 说明: （无）
- 参数: x1, y1, x2, y2
- 返回推断: tuple
- 调用概览: sorted
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### expand_rectangle(p1, p2, offset)
- 说明: （无）
- 参数: p1, p2, offset
- 返回推断: object
- 关注点: 几何
- 调用概览: normalize_rect, float
- 理解: 主要用于计算/测量相关逻辑。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### ss_select(mode, p1, p2, filter_types, filter_data, autocast, prompt)
- 说明: 【SEL-001】通用选择集构造器
- 邻近注释: ================================================================= | 3. 基础选择核心 (Selection Engine) | =================================================================
- 参数: mode, p1, p2, filter_types, filter_data, autocast, prompt
- 返回推断: object
- 关注点: 选择集
- 关键调用: C.doc
- 调用概览: Add, Delete, com_retry, SelectOnScreen, Item, Select, ValueError, range, _maybe_cast, uuid4, Prompt, _to_vt_point...
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-001】通用选择集构造器。邻近注释提示：=================================================================；3. 基础选择核心 (Selection Engine)；=================================================================。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_entities_through_point(p, tol)
- 说明: 【SEL-GEO-001】点选 (微小窗交法)
- 邻近注释: ================================================================= | 4. 几何与空间选择 (Geometric Selection) | =================================================================
- 参数: p, tol
- 返回推断: list,object
- 关注点: 选择集
- 调用概览: ss_select, any, print, getattr, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-GEO-001】点选 (微小窗交法)。邻近注释提示：=================================================================；4. 几何与空间选择 (Geometric Selection)；=================================================================。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_objects_in_window_area(x1, y1, x2, y2, max_retry)
- 说明: 【SEL-GEO-002】隐性窗口选择（带自动 Zoom）
- 参数: x1, y1, x2, y2, max_retry
- 返回推断: list,object
- 关注点: COM, 时间/等待, 选择集
- 关键调用: C.doc, C.acad
- 调用概览: array, range, abs, sleep, ss_select, ZoomWindow, SendCommand
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-GEO-002】隐性窗口选择（带自动 Zoom）。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### select_paperspace_objects_in_window(x1, y1, x2, y2)
- 说明: 【SEL-GEO-003】图纸空间区域选择
- 参数: x1, y1, x2, y2
- 返回推断: object
- 关注点: COM, 选择集
- 关键调用: C.doc
- 调用概览: normalize_rect, ss_select, com_retry, range, SetVariable, pt3, Item, GetBoundingBox, intersects, append, _maybe_cast
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-GEO-003】图纸空间区域选择。实现特征：涉及系统变量读取/设置；涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### pmxz(prompt, autocast)
- 说明: 【SEL-GEO-004】交互式屏幕选择
- 参数: prompt, autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于处理相关逻辑。依据注释：【SEL-GEO-004】交互式屏幕选择。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### get_last_n_objects(n, autocast)
- 说明: 【SEL-GEO-005】获取最后生成的 N 个图元
- 参数: n, autocast
- 返回推断: list,object
- 调用概览: com_retry, max, range, Item, append, _maybe_cast
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-GEO-005】获取最后生成的 N 个图元。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### last_obj()
- 说明: 【SEL-GEO-006】获取最后一个对象
- 参数: （无）
- 返回推断: NoneType,object
- 调用概览: Item
- 理解: 主要用于处理相关逻辑。依据注释：【SEL-GEO-006】获取最后一个对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### select_tuceng(layer_names, max_retries, delay, autocast)
- 说明: 【SEL-TYPE-001】按图层名选择
- 邻近注释: ================================================================= | 5. 类型与图层选择 (Type & Layer Selection) | =================================================================
- 参数: layer_names, max_retries, delay, autocast
- 返回推断: list,object
- 关注点: 时间/等待, 选择集
- 调用概览: range, isinstance, list, ss_select, sleep, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-TYPE-001】按图层名选择。邻近注释提示：=================================================================；5. 类型与图层选择 (Type & Layer Selection)；=================================================================。实现特征：涉及选择集构造/过滤。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象；超时与重试次数边界

### stc(layer_names, **kwargs)
- 说明: （无）
- 参数: layer_names, **kwargs
- 返回推断: object
- 关注点: 选择集
- 调用概览: select_tuceng
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_kuai(max_retries, autocast)
- 说明: （无）
- 参数: max_retries, autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_text(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_mtext(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_line(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_circle(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_ellipse(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_spline(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_polyline(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 几何, 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_polyline_chuantong(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 几何, 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_all_texts_mixed(target_space)
- 说明: 【SEL-TYPE-011】混合选择文本 (CAD+天正)
- 参数: target_space
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select, getattr, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-TYPE-011】混合选择文本 (CAD+天正)。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_pub_text_entities()
- 说明: 【SEL-TYPE-012】PUB_TEXT 图层天正文字
- 参数: （无）
- 返回推断: tuple
- 关注点: 选择集
- 调用概览: select_tuceng, getattr, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-TYPE-012】PUB_TEXT 图层天正文字。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_group_entities(group_obj)
- 说明: 【SEL-TYPE-013】选择组
- 参数: group_obj
- 返回推断: bool
- 关注点: COM, 选择集
- 关键调用: C.doc
- 调用概览: yin_to_xian_xuanze, print, append, HandleToObject
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-TYPE-013】选择组。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### yin_to_xian_xuanze(LB, wait_s)
- 说明: 【VIS-001】隐性->显性 (Delete/Undo法)
- 邻近注释: ================================================================= | 6. 可视化与交互 (Visualization) | =================================================================
- 参数: LB, wait_s
- 关注点: COM, 时间/等待
- 关键调用: C.doc
- 调用概览: com_retry, SendCommand, sleep, StartUndoMark, EndUndoMark, Delete
- 理解: 主要用于处理相关逻辑。依据注释：【VIS-001】隐性->显性 (Delete/Undo法)。邻近注释提示：=================================================================；6. 可视化与交互 (Visualization)；=================================================================。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### yin_to_xian_safe(LB, wait_s)
- 说明: 【VIS-002】隐性->显性 (LISP sssetfirst法，推荐)
- 参数: LB, wait_s
- 返回推断: None
- 关注点: COM, 时间/等待
- 关键调用: C.doc
- 调用概览: SendCommand, enumerate, sleep, print, getattr, randint
- 理解: 主要用于处理相关逻辑。依据注释：【VIS-002】隐性->显性 (LISP sssetfirst法，推荐)。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### xian_to_yin_pickfirst(clear_grips, autocast)
- 说明: 【VIS-003】获取 Pickfirst 选择集
- 参数: clear_grips, autocast
- 返回推断: list,object
- 关注点: COM, 选择集
- 关键调用: C.doc
- 调用概览: Item, SendCommand, range, _maybe_cast
- 理解: 主要用于处理相关逻辑。依据注释：【VIS-003】获取 Pickfirst 选择集。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### select_entities_in_window(x1, y1, x2, y2, ty, select_mode)
- 说明: 【VIS-004】区域高亮并返回对象
- 参数: x1, y1, x2, y2, ty, select_mode
- 返回推断: object
- 关注点: COM, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: normalize_rect, SendCommand, sleep, Clear
- 理解: 主要用于获取/选择相关逻辑。依据注释：【VIS-004】区域高亮并返回对象。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### highlight_entities_in_window(x1, y1, x2, y2)
- 说明: 【VIS-005】仅高亮区域
- 参数: x1, y1, x2, y2
- 关注点: 选择集
- 调用概览: select_entities_in_window
- 理解: 主要用于处理相关逻辑。依据注释：【VIS-005】仅高亮区域。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### highlight_entity_by_bbox(entity)
- 说明: 【VIS-006】高亮单个对象 (包围盒法)
- 参数: entity
- 关注点: 几何
- 调用概览: GetBoundingBox, expand_rectangle, highlight_entities_in_window, print, getattr
- 理解: 主要用于处理相关逻辑。依据注释：【VIS-006】高亮单个对象 (包围盒法)。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_entity_grip_state_precise(ent)
- 说明: 【VIS-007】独占式高亮
- 参数: ent
- 返回推断: None,object
- 关注点: COM, 时间/等待
- 关键调用: C.doc
- 调用概览: SendCommand, sleep
- 理解: 主要用于更新/设置相关逻辑。依据注释：【VIS-007】独占式高亮。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### isolate_modelspace_area(x1, y1, x2, y2)
- 说明: 【VIS-008】隔离显示区域
- 参数: x1, y1, x2, y2
- 关注点: COM, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: select_objects_in_window_area, yin_to_xian_xuanze, sleep, SendCommand
- 理解: 主要用于计算/测量相关逻辑。依据注释：【VIS-008】隔离显示区域。实现特征：通过命令发送驱动 CAD 行为。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### unhide_all(space, filter_names, highlight)
- 说明: 【VIS-009】显示隐藏对象
- 参数: space, filter_names, highlight
- 返回推断: object
- 调用概览: com_retry, range, Item, getattr, append, _maybe_cast, Highlight
- 理解: 主要用于处理相关逻辑。依据注释：【VIS-009】显示隐藏对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _resolve_attr_case_insensitive(obj, attr_name)
- 说明: 【PROP-000】属性名解析器 (带缓存与暴力回退)
- 参数: obj, attr_name
- 返回推断: NoneType,object
- 调用概览: hasattr, upper, dir, lower, str, type
- 理解: 主要用于处理相关逻辑。依据注释：【PROP-000】属性名解析器 (带缓存与暴力回退)。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_attr(obj, name)
- 说明: 【PROP-001】万能获取属性
- 参数: obj, name
- 返回推断: NoneType,object
- 关注点: COM
- 调用概览: getattr, _maybe_cast, _resolve_attr_case_insensitive, get, Invoke, lower
- 理解: 主要用于获取/选择相关逻辑。依据注释：【PROP-001】万能获取属性。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_attr(obj, name, value)
- 说明: 【PROP-002】万能设置属性
- 参数: obj, name, value
- 返回推断: bool
- 关注点: COM
- 调用概览: getattr, _maybe_cast, _resolve_attr_case_insensitive, setattr, get, Invoke, lower
- 理解: 主要用于更新/设置相关逻辑。依据注释：【PROP-002】万能设置属性。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_object_property(obj, property_name)
- 说明: 统一获取对象属性（自动识别CAD对象或天正对象）
- 邻近注释: &&% 兼容旧代码获取对象属性
- 参数: obj, property_name
- 返回推断: NoneType,object
- 关注点: COM
- 调用概览: com_retry, _maybe_cast, getattr, get, Invoke
- 理解: 主要用于获取/选择相关逻辑。依据注释：统一获取对象属性（自动识别CAD对象或天正对象）。邻近注释提示：&&% 兼容旧代码获取对象属性。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_object_property(obj, property_name, value)
- 说明: 统一设置对象属性（自动识别CAD对象或天正对象）
- 邻近注释: &&% 兼容旧代设置对象属性
- 参数: obj, property_name, value
- 返回推断: bool
- 关注点: COM
- 调用概览: com_retry, _maybe_cast, setattr, get, Invoke
- 理解: 主要用于更新/设置相关逻辑。依据注释：统一设置对象属性（自动识别CAD对象或天正对象）。邻近注释提示：&&% 兼容旧代设置对象属性。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### brute_dump_tarch_props(ent, max_dispid)
- 说明: 【PROP-003】天正属性扫描调试
- 参数: ent, max_dispid
- 关注点: COM
- 调用概览: print, range, Invoke, getattr, type
- 理解: 主要用于保存/写入相关逻辑。依据注释：【PROP-003】天正属性扫描调试。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

## system/CAD_selection.py
- 模块说明: （无）
### cast_object(obj)
- 说明: （无）
- 参数: obj
- 返回推断: object
- 调用概览: _maybe_cast
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _maybe_cast(ent)
- 说明: 【CORE-002】智能类型转换
- 参数: ent
- 返回推断: NoneType,object
- 关注点: COM, 进程
- 关键调用: retry_on_busy, SafeCOM
- 调用概览: hasattr, EnsureDispatch, getattr, CastTo, startswith, Dispatch
- 理解: 主要用于处理相关逻辑。依据注释：【CORE-002】智能类型转换。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### to_vt_int(seq)
- 说明: （无）
- 邻近注释: --- 内部辅助 (保持不变) ---
- 参数: seq
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT, list
- 理解: 主要用于处理相关逻辑。邻近注释提示：--- 内部辅助 (保持不变) ---。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### to_vt_variant(seq)
- 说明: （无）
- 参数: seq
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT, list
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### _to_vt_point(pt_tuple)
- 说明: （无）
- 参数: pt_tuple
- 返回推断: NoneType,object
- 关注点: COM
- 调用概览: VARIANT, float
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### pt3(x, y, z)
- 说明: （无）
- 参数: x, y, z
- 返回推断: object
- 关注点: COM
- 调用概览: VARIANT
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### normalize_rect(x1, y1, x2, y2)
- 说明: （无）
- 参数: x1, y1, x2, y2
- 返回推断: tuple
- 调用概览: sorted
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### expand_rectangle(p1, p2, offset)
- 说明: （无）
- 参数: p1, p2, offset
- 返回推断: object
- 关注点: 几何
- 调用概览: normalize_rect, float
- 理解: 主要用于计算/测量相关逻辑。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### com_retry(fn, retries, delay)
- 说明: 【兼容补丁】
- 邻近注释: --- 兼容旧代码接口 (关键修复) ---
- 参数: fn, retries, delay
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: wrapper, retry_on_busy
- 理解: 主要用于等待/守护相关逻辑。依据注释：【兼容补丁】。邻近注释提示：--- 兼容旧代码接口 (关键修复) ---。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### current_space_only(func)
- 说明: 【装饰器】过滤结果，只保留属于当前激活空间（模型或当前布局）的对象。
- 邻近注释: &&% 限定空间装饰器
- 参数: func
- 返回推断: list,object
- 关注点: COM, 日志/测试
- 关键调用: C.doc
- 调用概览: wraps, func, error, append
- 理解: 主要用于处理相关逻辑。依据注释：【装饰器】过滤结果，只保留属于当前激活空间（模型或当前布局）的对象。。邻近注释提示：&&% 限定空间装饰器。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### ss_select(mode, p1, p2, filter_types, filter_data, autocast, prompt)
- 说明: 【SEL-001】通用选择集构造器 (重构版)
- 参数: mode, p1, p2, filter_types, filter_data, autocast, prompt
- 返回推断: object
- 关注点: 选择集
- 关键调用: retry_on_busy, SafeCOM, C.doc
- 调用概览: Add, list_selection, SelectOnScreen, Delete, Select, ValueError, _maybe_cast, uuid4, Prompt, _to_vt_point, to_vt_int, to_vt_variant
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-001】通用选择集构造器 (重构版)。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_entities_through_point(p, tol)
- 说明: 【SEL-GEO-001】点选
- 参数: p, tol
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select, any, getattr, append
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-GEO-001】点选。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_objects_in_window_area(x1, y1, x2, y2)
- 说明: 【SEL-GEO-002】隐性窗口选择（带自动 Zoom）
- 参数: x1, y1, x2, y2
- 返回推断: object
- 关注点: COM, 时间/等待, 选择集
- 关键调用: C.doc, C.acad
- 调用概览: retry_on_busy, array, sleep, ss_select, abs, ZoomWindow, SendCommand
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-GEO-002】隐性窗口选择（带自动 Zoom）。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### select_paperspace_objects_in_window(x1, y1, x2, y2)
- 说明: 【SEL-GEO-003】图纸空间区域选择
- 参数: x1, y1, x2, y2
- 返回推断: object
- 关注点: COM, 选择集
- 关键调用: SafeCOM, C.doc
- 调用概览: normalize_rect, ss_select, list_selection, SetVariable, pt3, GetBoundingBox, intersects, append, _maybe_cast
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-GEO-003】图纸空间区域选择。实现特征：涉及系统变量读取/设置；涉及选择集构造/过滤。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### pmxz(prompt, autocast)
- 说明: （无）
- 参数: prompt, autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于处理相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### get_last_n_objects(n, autocast)
- 说明: 【SEL-GEO-005】获取最后生成的 N 个图元
- 参数: n, autocast
- 返回推断: list,object
- 关键调用: SafeCOM
- 调用概览: max, range, Item, append, _maybe_cast
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-GEO-005】获取最后生成的 N 个图元。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### last_obj()
- 说明: （无）
- 参数: （无）
- 返回推断: NoneType,object
- 调用概览: Item
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### select_tuceng(layer_names, delay, autocast)
- 说明: 【SEL-TYPE-001】按图层名选择
- 参数: layer_names, delay, autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: retry_on_busy, ss_select, isinstance, list, len
- 理解: 主要用于获取/选择相关逻辑。依据注释：【SEL-TYPE-001】按图层名选择。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### stc(layer_names, **kwargs)
- 说明: （无）
- 参数: layer_names, **kwargs
- 返回推断: object
- 关注点: 选择集
- 调用概览: select_tuceng
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_kuai(autocast)
- 说明: （无）
- 邻近注释: 以下均为快捷方式，自动继承 ss_select 的重试能力
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：以下均为快捷方式，自动继承 ss_select 的重试能力。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_text(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_mtext(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_line(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_circle(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_ellipse(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_spline(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_polyline(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 几何, 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_polyline_chuantong(autocast)
- 说明: （无）
- 参数: autocast
- 返回推断: object
- 关注点: 几何, 选择集
- 调用概览: ss_select
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_all_texts_mixed(target_space)
- 说明: （无）
- 参数: target_space
- 返回推断: object
- 关注点: 选择集
- 调用概览: ss_select, getattr
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_pub_text_entities()
- 说明: （无）
- 参数: （无）
- 返回推断: tuple
- 关注点: 选择集
- 调用概览: select_tuceng, getattr, append
- 理解: 主要用于获取/选择相关逻辑。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### select_group_entities(group_obj)
- 说明: （无）
- 参数: group_obj
- 返回推断: bool
- 关注点: COM, 选择集
- 关键调用: C.doc
- 调用概览: yin_to_xian_xuanze, print, append, HandleToObject
- 理解: 主要用于获取/选择相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### yin_to_xian_xuanze(LB, wait_s)
- 说明: 【VIS-001】隐转显 (Delete/Undo法)
- 参数: LB, wait_s
- 关注点: COM, 时间/等待
- 关键调用: SafeCOM, C.doc
- 调用概览: StartUndoMark, SendCommand, sleep, EndUndoMark, Delete
- 理解: 主要用于处理相关逻辑。依据注释：【VIS-001】隐转显 (Delete/Undo法)。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### yin_to_xian_safe(LB, wait_s)
- 说明: 【VIS-002】隐转显 (LISP sssetfirst法)
- 参数: LB, wait_s
- 返回推断: None
- 关注点: COM, 时间/等待
- 关键调用: C.doc
- 调用概览: SendCommand, enumerate, sleep, getattr, randint
- 理解: 主要用于处理相关逻辑。依据注释：【VIS-002】隐转显 (LISP sssetfirst法)。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### xian_to_yin_pickfirst(clear_grips, autocast)
- 说明: （无）
- 参数: clear_grips, autocast
- 返回推断: list,object
- 关注点: COM, 选择集
- 关键调用: SafeCOM, C.doc
- 调用概览: list_selection, SendCommand, _maybe_cast
- 理解: 主要用于处理相关逻辑。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象

### select_entities_in_window(x1, y1, x2, y2, ty, select_mode)
- 说明: （无）
- 参数: x1, y1, x2, y2, ty, select_mode
- 返回推断: object
- 关注点: COM, 时间/等待, 选择集
- 关键调用: SafeCOM, C.doc
- 调用概览: normalize_rect, SendCommand, sleep, list_selection, Clear
- 理解: 主要用于获取/选择相关逻辑。实现特征：涉及选择集构造/过滤；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### highlight_entities_in_window(x1, y1, x2, y2)
- 说明: （无）
- 参数: x1, y1, x2, y2
- 关注点: 选择集
- 调用概览: select_entities_in_window
- 理解: 主要用于处理相关逻辑。包含选择集构造或过滤。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值；空选择集/选择集异常对象

### highlight_entity_by_bbox(entity)
- 说明: （无）
- 参数: entity
- 关注点: 几何
- 调用概览: GetBoundingBox, expand_rectangle, highlight_entities_in_window, print, getattr
- 理解: 主要用于处理相关逻辑。涉及几何/多段线/包围盒处理。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_entity_grip_state_precise(ent)
- 说明: （无）
- 参数: ent
- 返回推断: None,object
- 关注点: COM, 时间/等待
- 关键调用: C.doc
- 调用概览: SendCommand, sleep
- 理解: 主要用于更新/设置相关逻辑。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### isolate_modelspace_area(x1, y1, x2, y2)
- 说明: （无）
- 参数: x1, y1, x2, y2
- 关注点: COM, 时间/等待, 选择集
- 关键调用: C.doc
- 调用概览: select_objects_in_window_area, yin_to_xian_xuanze, sleep, SendCommand
- 理解: 主要用于计算/测量相关逻辑。实现特征：通过命令发送驱动 CAD 行为。包含选择集构造或过滤。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；空选择集/选择集异常对象；超时与重试次数边界

### unhide_all(space, filter_names, highlight)
- 说明: （无）
- 参数: space, filter_names, highlight
- 返回推断: object
- 关键调用: SafeCOM
- 调用概览: list_selection, getattr, call, append, _maybe_cast, Highlight
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### _resolve_attr_case_insensitive(obj, attr_name)
- 说明: （无）
- 参数: obj, attr_name
- 返回推断: NoneType,object
- 调用概览: hasattr, upper, dir, lower, str, type
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### get_attr(obj, name)
- 说明: （无）
- 参数: obj, name
- 返回推断: NoneType,object
- 关注点: COM
- 关键调用: SafeCOM
- 调用概览: getattr, _maybe_cast, _resolve_attr_case_insensitive, get, Invoke, lower
- 理解: 主要用于获取/选择相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_attr(obj, name, default)
- 说明: 【修正版】安全获取对象属性 (支持默认值)
- 邻近注释: &&% 20261014
- 参数: obj, name, default
- 返回推断: object
- 关注点: COM
- 调用概览: getattr, _maybe_cast, _resolve_attr_case_insensitive, get, Invoke, lower
- 理解: 主要用于获取/选择相关逻辑。依据注释：【修正版】安全获取对象属性 (支持默认值)。邻近注释提示：&&% 20261014。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### set_attr(obj, name, value)
- 说明: （无）
- 参数: obj, name, value
- 返回推断: bool
- 关注点: COM
- 关键调用: SafeCOM
- 调用概览: getattr, _maybe_cast, _resolve_attr_case_insensitive, call, get, Invoke, lower
- 理解: 主要用于更新/设置相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_object_property(obj, property_name)
- 说明: （无）
- 邻近注释: 兼容旧代码接口
- 参数: obj, property_name
- 返回推断: object
- 调用概览: get_attr
- 理解: 主要用于获取/选择相关逻辑。邻近注释提示：兼容旧代码接口。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### set_object_property(obj, property_name, value)
- 说明: （无）
- 参数: obj, property_name, value
- 返回推断: object
- 调用概览: set_attr
- 理解: 主要用于更新/设置相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### brute_dump_tarch_props(ent, max_dispid)
- 说明: （无）
- 参数: ent, max_dispid
- 关注点: COM
- 调用概览: print, range, Invoke, getattr, type
- 理解: 主要用于保存/写入相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

## system/common_logger - V1.1.py
- 模块说明: （无）
### setup_logger(log_file)
- 说明: 配置全局唯一的日志记录器
- 参数: log_file
- 返回推断: object
- 关注点: COM, 文件, 选择集
- 调用概览: getLogger, setLevel, Formatter, dirname, join, StreamHandler, setFormatter, addHandler, abspath, exists, makedirs, RotatingFileHandler...
- 理解: 主要用于更新/设置相关逻辑。依据注释：配置全局唯一的日志记录器。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

## system/common_logger - V1.4.py
- 模块说明: （无）
### set_debug_mode(mode)
- 说明: 用于在其他脚本中动态修改调试状态
- 参数: mode
- 关注点: 文件, 日志/测试
- 调用概览: info
- 理解: 主要用于更新/设置相关逻辑。依据注释：用于在其他脚本中动态修改调试状态。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### set_debug_mode(mode, who, wait_time)
- 说明: 设置调试系统的运行模式
- 参数: mode, who, wait_time
- 关注点: 文件, 日志/测试
- 调用概览: upper, info, str
- 理解: 主要用于更新/设置相关逻辑。依据注释：设置调试系统的运行模式。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### record_test_result(script_name, func_name, is_pass, **variables)
- 说明: 将测试运行时的变量快照写入 Excel。
- 邻近注释: ========================================== | 3. Excel 测试记录功能 | ==========================================
- 参数: script_name, func_name, is_pass, **variables
- 关注点: 文件
- 调用概览: str, get, strftime, append, items, exists, save, load_workbook, Workbook, print, globals, now
- 理解: 主要用于保存/写入相关逻辑。依据注释：将测试运行时的变量快照写入 Excel。。邻近注释提示：==========================================；3. Excel 测试记录功能；==========================================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### setup_logger(log_file)
- 说明: 配置全局唯一的日志记录器
- 邻近注释: ========================================== | 4. 日志系统 (保持原有逻辑) | ==========================================
- 参数: log_file
- 返回推断: object
- 关注点: COM, 文件, 选择集
- 调用概览: getLogger, setLevel, Formatter, dirname, join, StreamHandler, setFormatter, addHandler, abspath, exists, makedirs, RotatingFileHandler...
- 理解: 主要用于更新/设置相关逻辑。依据注释：配置全局唯一的日志记录器。邻近注释提示：==========================================；4. 日志系统 (保持原有逻辑)；==========================================。依赖 CAD COM 对象与当前文档/模型空间。包含选择集构造或过滤。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；空选择集/选择集异常对象

### DebugContext.__init__(self, name)
- 说明: （无）
- 参数: self, name
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### DebugContext.is_ai(self)
- 说明: 是否为 AI 自动化模式
- 参数: self
- 返回推断: object
- 理解: 主要用于处理相关逻辑。依据注释：是否为 AI 自动化模式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### DebugContext.is_human(self)
- 说明: 是否为 人类 观察模式
- 参数: self
- 返回推断: object
- 理解: 主要用于处理相关逻辑。依据注释：是否为 人类 观察模式。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### DebugContext.__enter__(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 关注点: 日志/测试
- 调用概览: info
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### DebugContext.__exit__(self, exc_type, exc_val, exc_tb)
- 说明: （无）
- 参数: self, exc_type, exc_val, exc_tb
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待
- 调用概览: info, print, range, sleep
- 理解: 主要用于处理相关逻辑。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### node(msg, *args, **kwargs)
- 说明: 【简易日志包装器】
- 邻近注释: ========================================================= | 🆕 新增：节点日志辅助函数 (Node Logger) | =========================================================
- 参数: msg, *args, **kwargs
- 关注点: 日志/测试
- 调用概览: info, format
- 理解: 主要用于处理相关逻辑。依据注释：【简易日志包装器】。邻近注释提示：=========================================================；🆕 新增：节点日志辅助函数 (Node Logger)；=========================================================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## system/common_logger.py
- 模块说明: （无）
### set_debug_mode(mode, who, wait_time)
- 说明: （无）
- 参数: mode, who, wait_time
- 关注点: 文件, 日志/测试
- 调用概览: int, upper, globals, info, str
- 理解: 主要用于更新/设置相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### setup_logger(log_file)
- 说明: （无）
- 邻近注释: ========================================== | 2. 日志系统 | ==========================================
- 参数: log_file
- 返回推断: object
- 关注点: COM, 文件
- 调用概览: getLogger, setLevel, Formatter, join, StreamHandler, setFormatter, addHandler, dirname, RotatingFileHandler, abspath
- 理解: 主要用于更新/设置相关逻辑。邻近注释提示：==========================================；2. 日志系统；==========================================。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### record_test_result(script_name, func_name, is_pass, **variables)
- 说明: （无）
- 邻近注释: ========================================== | 3. Excel 记录 | ==========================================
- 参数: script_name, func_name, is_pass, **variables
- 返回推断: None
- 关注点: 文件, 日志/测试
- 调用概览: items, append, exists, save, str, load_workbook, Workbook, error, currentframe, basename, len, strftime...
- 理解: 主要用于保存/写入相关逻辑。邻近注释提示：==========================================；3. Excel 记录；==========================================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### checkpoint(desc, is_pass, **variables)
- 说明: （无）
- 邻近注释: ========================================== | 4. 核心工具 (修复版) | ==========================================
- 参数: desc, is_pass, **variables
- 关注点: 文件, 日志/测试, 时间/等待
- 调用概览: record_test_result, basename, currentframe, print, sleep
- 理解: 主要用于测试/校验相关逻辑。邻近注释提示：==========================================；4. 核心工具 (修复版)；==========================================。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径；超时与重试次数边界

### CriticalSection.__init__(self, description, script_name, func_name)
- 说明: （无）
- 参数: self, description, script_name, func_name
- 关注点: 文件
- 调用概览: currentframe, basename
- 理解: 主要用于处理相关逻辑。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### CriticalSection.record(self, **kwargs)
- 说明: （无）
- 参数: self, **kwargs
- 调用概览: update
- 理解: 主要用于保存/写入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### CriticalSection.__enter__(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 关注点: 日志/测试
- 调用概览: info
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### CriticalSection.__exit__(self, exc_type, exc_val, exc_tb)
- 说明: （无）
- 参数: self, exc_type, exc_val, exc_tb
- 返回推断: bool
- 关注点: 日志/测试, 时间/等待
- 调用概览: str, error, record_test_result, print, sleep
- 理解: 主要用于处理相关逻辑。
- 风险: 包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；超时与重试次数边界

### node(msg, *args, **kwargs)
- 说明: （无）
- 参数: msg, *args, **kwargs
- 关注点: 日志/测试
- 调用概览: info, format
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## system/licad - V10.py
- 模块说明: （无）
### _coinit_once()
- 说明: 线程初始化防呆设计
- 参数: （无）
- 关注点: COM
- 调用概览: CoInitialize
- 理解: 主要用于处理相关逻辑。依据注释：线程初始化防呆设计。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### _retry_on_busy(max_retries, base_delay)
- 说明: [装饰器工厂] 自动处理 CAD 忙碌 (RPC_E_CALL_REJECTED)。
- 邻近注释: ================================================================= | 2. 核心连接函数 (公开工具) | =================================================================
- 参数: max_retries, base_delay
- 返回推断: object
- 关注点: COM, 日志/测试, 时间/等待
- 关键调用: retry_on_busy
- 调用概览: wraps, range, critical, error, ValueError, func, str, getattr, any, warning, sleep, PumpWaitingMessages
- 理解: 主要用于等待/守护相关逻辑。依据注释：[装饰器工厂] 自动处理 CAD 忙碌 (RPC_E_CALL_REJECTED)。。邻近注释提示：=================================================================；2. 核心连接函数 (公开工具)；=================================================================。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### get_acad_doc(max_wait)
- 说明: [底层原语] 获取/启动 AutoCAD 应用和文档 (安全修正版)
- 参数: max_wait
- 返回推断: tuple
- 关注点: COM, 时间/等待, 进程
- 调用概览: _coinit_once, time, GetActiveObject, EnsureDispatch, print, sleep, RuntimeError, Add, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：[底层原语] 获取/启动 AutoCAD 应用和文档 (安全修正版)。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### AutoCadProxy.__init__(self)
- 说明: （无）
- 参数: self
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.li(self)
- 说明: [智能连接]
- 邻近注释: ------------------------------------------------------------- | 连接逻辑 (保留你的三层验证) | -------------------------------------------------------------
- 参数: self
- 返回推断: bool
- 关注点: COM
- 调用概览: print, get_acad_doc, VARIANT, AddLine, Delete, RuntimeError
- 理解: 主要用于处理相关逻辑。依据注释：[智能连接]。邻近注释提示：-------------------------------------------------------------；连接逻辑 (保留你的三层验证)；-------------------------------------------------------------。实现特征：创建直线对象。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### AutoCadProxy.acad(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.doc(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.mp(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.sp(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.save_file(self)
- 说明: （无）
- 参数: self
- 返回推断: bool
- 调用概览: Save, print
- 理解: 主要用于保存/写入相关逻辑。实现特征：执行保存。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.save_file_as(self, output_path)
- 说明: （无）
- 参数: self, output_path
- 返回推断: bool
- 关注点: 文件
- 调用概览: resolve, print, SaveAs, li, exists, str, Path
- 理解: 主要用于保存/写入相关逻辑。实现特征：执行另存为。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### AutoCadProxy.open_file(self, file_path)
- 说明: （无）
- 参数: self, file_path
- 返回推断: bool
- 关注点: COM, 文件
- 调用概览: lower, exists, print, Open, li, str, resolve, Activate, Path
- 理解: 主要用于打开/读取相关逻辑。实现特征：执行 DWG 打开。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### AutoCadProxy.close_file(self, save_option)
- 说明: （无）
- 参数: self, save_option
- 返回推断: bool
- 调用概览: print, save_file, Close, li
- 理解: 主要用于关闭/终止相关逻辑。实现特征：执行关闭文档。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.close_dwg_by_name(self, name)
- 说明: （无）
- 参数: self, name
- 返回推断: bool
- 关注点: COM, 进程
- 调用概览: GetActiveObject, Item, Close, print
- 理解: 主要用于关闭/终止相关逻辑。实现特征：执行关闭文档。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### li()
- 说明: （无）
- 邻近注释: ================================================================= | 5. 模块级函数导出 (提供给外部脚本调用) | =================================================================
- 参数: （无）
- 返回推断: object
- 关键调用: C.li
- 调用概览: li
- 理解: 主要用于处理相关逻辑。邻近注释提示：=================================================================；5. 模块级函数导出 (提供给外部脚本调用)；=================================================================。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### save_file()
- 说明: （无）
- 参数: （无）
- 返回推断: object
- 调用概览: save_file
- 理解: 主要用于保存/写入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### save_file_as(output_path)
- 说明: （无）
- 参数: output_path
- 返回推断: object
- 调用概览: save_file_as
- 理解: 主要用于保存/写入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### open_file(file_path)
- 说明: （无）
- 参数: file_path
- 返回推断: object
- 调用概览: open_file
- 理解: 主要用于打开/读取相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### close_file(save_option)
- 说明: （无）
- 参数: save_option
- 返回推断: object
- 调用概览: close_file
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### close_dwg_by_name(name)
- 说明: （无）
- 参数: name
- 返回推断: object
- 调用概览: close_dwg_by_name
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### retry_on_busy(func)
- 说明: （无）
- 邻近注释: 【新增】导出装饰器
- 参数: func
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: _retry_on_busy
- 理解: 主要用于等待/守护相关逻辑。邻近注释提示：【新增】导出装饰器。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## system/licad - V20.py
- 模块说明: （无）
### _coinit_once()
- 说明: （无）
- 邻近注释: ======================================================= | 2. 核心功能函数 (连接逻辑) | =======================================================
- 参数: （无）
- 关注点: COM
- 调用概览: CoInitialize
- 理解: 主要用于处理相关逻辑。邻近注释提示：=======================================================；2. 核心功能函数 (连接逻辑)；=======================================================。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_acad_doc(max_wait)
- 说明: 获取/启动 AutoCAD 应用和文档
- 参数: max_wait
- 返回推断: tuple
- 关注点: COM, 日志/测试, 时间/等待, 进程
- 调用概览: _coinit_once, time, sleep, GetActiveObject, EnsureDispatch, error, RuntimeError, info, Add
- 理解: 主要用于获取/选择相关逻辑。依据注释：获取/启动 AutoCAD 应用和文档。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### SafeDocumentWrapper.__init__(self, real_com_doc)
- 说明: （无）
- 参数: self, real_com_doc
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### SafeDocumentWrapper.SendCommand(self, cmd)
- 说明: 【拦截】劫持 SendCommand，转为同步安全模式
- 参数: self, cmd
- 返回推断: object
- 关注点: COM, 时间/等待
- 关键调用: send_cmd_with_sync
- 调用概览: send_cmd_with_sync, SendCommand, endswith
- 理解: 主要用于关闭/终止相关逻辑。依据注释：【拦截】劫持 SendCommand，转为同步安全模式。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### SafeDocumentWrapper.__getattr__(self, name)
- 说明: 【转发】除了 SendCommand 以外的所有属性/方法（如 Name, SaveAs, Layers），
- 参数: self, name
- 返回推断: object
- 关注点: COM
- 调用概览: getattr
- 理解: 主要用于获取/选择相关逻辑。依据注释：【转发】除了 SendCommand 以外的所有属性/方法（如 Name, SaveAs, Layers），。实现特征：涉及图层操作；通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### SafeDocumentWrapper.__dir__(self)
- 说明: 让 IDE 能自动提示真实对象的属性
- 参数: self
- 返回推断: object
- 关注点: COM
- 调用概览: dir
- 理解: 主要用于处理相关逻辑。依据注释：让 IDE 能自动提示真实对象的属性。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### AutoCadProxy.__init__(self)
- 说明: （无）
- 参数: self
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.li(self)
- 说明: 连接刷新
- 参数: self
- 返回推断: bool
- 关注点: COM, 日志/测试
- 调用概览: Exception, get_acad_doc, info, error
- 理解: 主要用于处理相关逻辑。依据注释：连接刷新。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### AutoCadProxy.doc(self)
- 说明: 【关键修改】
- 参数: self
- 返回推断: object
- 关注点: COM
- 调用概览: li, SafeDocumentWrapper
- 理解: 主要用于处理相关逻辑。依据注释：【关键修改】。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### AutoCadProxy.acad(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.mp(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 关注点: COM
- 调用概览: li
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### AutoCadProxy.sp(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 关注点: COM
- 调用概览: li
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### AutoCadProxy.save_file(self)
- 说明: （无）
- 参数: self
- 返回推断: bool
- 关注点: 日志/测试
- 调用概览: Save, info
- 理解: 主要用于保存/写入相关逻辑。实现特征：执行保存。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.save_file_as(self, output_path)
- 说明: （无）
- 参数: self, output_path
- 返回推断: bool
- 关注点: 文件, 日志/测试
- 调用概览: retry_on_busy, resolve, info, SaveAs, li, exists, error, str, Path
- 理解: 主要用于保存/写入相关逻辑。实现特征：执行另存为。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### AutoCadProxy.open_file(self, file_path)
- 说明: （无）
- 参数: self, file_path
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 调用概览: retry_on_busy, lower, info, Open, li, exists, error, str, resolve, Activate, Path
- 理解: 主要用于打开/读取相关逻辑。实现特征：执行 DWG 打开。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### AutoCadProxy.close_file(self, save_option)
- 说明: （无）
- 参数: self, save_option
- 返回推断: bool
- 关注点: 日志/测试
- 调用概览: Close, info, save_file
- 理解: 主要用于关闭/终止相关逻辑。实现特征：执行关闭文档。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.close_dwg_by_name(self, name)
- 说明: （无）
- 参数: self, name
- 返回推断: bool
- 关注点: COM, 日志/测试, 进程
- 调用概览: GetActiveObject, Close, info, Item
- 理解: 主要用于关闭/终止相关逻辑。实现特征：执行关闭文档。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### AutoCadProxy.SendCommand(self, cmd_str)
- 说明: 代理发送命令：
- 邻近注释: ============================================================== | 【必须补上】让 C.SendCommand 变为合法调用 | ==============================================================
- 参数: self, cmd_str
- 返回推断: object
- 关注点: COM, 时间/等待
- 关键调用: send_cmd_with_sync
- 调用概览: send_cmd_with_sync, SendCommand, endswith
- 理解: 主要用于关闭/终止相关逻辑。依据注释：代理发送命令：。邻近注释提示：==============================================================；【必须补上】让 C.SendCommand 变为合法调用；==============================================================。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### AutoCadProxy.force_update(self, new_acad, new_doc)
- 说明: 【灾难恢复专用】
- 参数: self, new_acad, new_doc
- 调用概览: print
- 理解: 主要用于更新/设置相关逻辑。依据注释：【灾难恢复专用】。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### li()
- 说明: （无）
- 参数: （无）
- 返回推断: object
- 关键调用: C.li
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### save_file()
- 说明: （无）
- 参数: （无）
- 返回推断: object
- 调用概览: save_file
- 理解: 主要用于保存/写入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### save_file_as(path)
- 说明: （无）
- 参数: path
- 返回推断: object
- 调用概览: save_file_as
- 理解: 主要用于保存/写入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### open_file(path)
- 说明: （无）
- 参数: path
- 返回推断: object
- 调用概览: open_file
- 理解: 主要用于打开/读取相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### close_file(opt)
- 说明: （无）
- 参数: opt
- 返回推断: object
- 调用概览: close_file
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### close_dwg_by_name(name)
- 说明: （无）
- 参数: name
- 返回推断: object
- 调用概览: close_dwg_by_name
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## system/licad.py
- 模块说明: （无）
### _coinit_once()
- 说明: （无）
- 参数: （无）
- 关注点: COM
- 调用概览: CoInitialize
- 理解: 主要用于处理相关逻辑。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### get_acad_doc(max_wait)
- 说明: [底层原语] 获取/启动 AutoCAD 应用和文档
- 邻近注释: ================================================================= | 2. 核心连接函数 | =================================================================
- 参数: max_wait
- 返回推断: tuple
- 关注点: COM, 日志/测试, 时间/等待, 进程
- 关键调用: wait_quiescent
- 调用概览: _coinit_once, time, RuntimeError, GetActiveObject, EnsureDispatch, sleep, info, Add, range
- 理解: 主要用于获取/选择相关逻辑。依据注释：[底层原语] 获取/启动 AutoCAD 应用和文档。邻近注释提示：=================================================================；2. 核心连接函数；=================================================================。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### get_acad_doc(max_wait)
- 说明: [底层原语] 获取/启动 AutoCAD 应用和文档
- 邻近注释: 新版
- 参数: max_wait
- 返回推断: bool,object,tuple
- 关注点: COM, 时间/等待, 进程
- 关键调用: wait_quiescent
- 调用概览: _coinit_once, time, print, GetObject, ExecQuery, len, GetActiveObject, EnsureDispatch, _is_acad_process_running, sleep, wait_quiescent, RuntimeError...
- 理解: 主要用于获取/选择相关逻辑。依据注释：[底层原语] 获取/启动 AutoCAD 应用和文档。邻近注释提示：新版。实现特征：包含空闲等待以同步 CAD 状态。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### get_acad_doc(max_wait)
- 说明: [底层原语] 获取/启动 AutoCAD 应用和文档
- 邻近注释: 清除缓存崩溃
- 参数: max_wait
- 返回推断: bool,object,tuple
- 关注点: COM, 文件, 时间/等待, 进程
- 调用概览: _coinit_once, time, print, GetObject, ExecQuery, len, append, GetActiveObject, EnsureDispatch, _is_acad_process_running, sleep, GetGeneratePath...
- 理解: 主要用于获取/选择相关逻辑。依据注释：[底层原语] 获取/启动 AutoCAD 应用和文档。邻近注释提示：清除缓存崩溃。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删；涉及进程控制，可能影响系统稳定；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径；超时与重试次数边界

### SafeDocumentWrapper.__init__(self, real_com_doc)
- 说明: （无）
- 参数: self, real_com_doc
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### SafeDocumentWrapper.SendCommand(self, cmd)
- 说明: （无）
- 参数: self, cmd
- 返回推断: object
- 关注点: COM, 时间/等待
- 关键调用: send_cmd_with_sync
- 调用概览: send_cmd_with_sync, endswith, SendCommand
- 理解: 主要用于关闭/终止相关逻辑。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；包含等待/阻塞逻辑，可能超时
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；超时与重试次数边界

### SafeDocumentWrapper.__getattr__(self, name)
- 说明: （无）
- 参数: self, name
- 返回推断: object
- 调用概览: getattr
- 理解: 主要用于获取/选择相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### SafeDocumentWrapper.__dir__(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 关注点: COM
- 调用概览: dir
- 理解: 主要用于处理相关逻辑。实现特征：通过命令发送驱动 CAD 行为。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### AutoCadProxy.__init__(self)
- 说明: （无）
- 参数: self
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.li(self)
- 说明: [智能连接] 三层验证
- 参数: self
- 返回推断: bool
- 关注点: COM, 日志/测试
- 调用概览: info, get_acad_doc, VARIANT, AddLine, Delete, error
- 理解: 主要用于处理相关逻辑。依据注释：[智能连接] 三层验证。实现特征：创建直线对象。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### AutoCadProxy.acad(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.doc(self)
- 说明: 【Wrapper】返回安全替身
- 参数: self
- 返回推断: object
- 调用概览: li, SafeDocumentWrapper
- 理解: 主要用于处理相关逻辑。依据注释：【Wrapper】返回安全替身。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.raw_doc(self)
- 说明: 【Raw】返回原始对象
- 参数: self
- 返回推断: object
- 调用概览: li
- 理解: 主要用于处理相关逻辑。依据注释：【Raw】返回原始对象。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.mp(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.sp(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.msp(self)
- 说明: （无）
- 参数: self
- 返回推断: object
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.save_file(self)
- 说明: （无）
- 参数: self
- 返回推断: bool
- 关注点: 日志/测试
- 调用概览: Save, info, error
- 理解: 主要用于保存/写入相关逻辑。实现特征：执行保存。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.save_file_as(self, path)
- 说明: （无）
- 参数: self, path
- 返回推断: bool
- 关注点: 文件, 日志/测试
- 调用概览: _tool_retry_on_busy, resolve, info, SaveAs, li, exists, str, error, Path
- 理解: 主要用于保存/写入相关逻辑。实现特征：执行另存为。包含文件读写或路径处理。
- 风险: 涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；文件不存在/权限不足/中文路径

### AutoCadProxy.open_file(self, path)
- 说明: （无）
- 参数: self, path
- 返回推断: bool
- 关注点: COM, 文件, 日志/测试
- 调用概览: _tool_retry_on_busy, lower, exists, info, Open, li, str, resolve, Activate, Path
- 理解: 主要用于打开/读取相关逻辑。实现特征：执行 DWG 打开。依赖 CAD COM 对象与当前文档/模型空间。包含文件读写或路径处理。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及文件读写/删除，需防止路径错误与误删
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景；文件不存在/权限不足/中文路径

### AutoCadProxy.close_file(self, opt)
- 说明: （无）
- 参数: self, opt
- 返回推断: bool
- 关注点: 日志/测试
- 调用概览: Close, info, Save, li
- 理解: 主要用于关闭/终止相关逻辑。实现特征：执行保存；执行关闭文档。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### AutoCadProxy.close_dwg_by_name(self, name)
- 说明: （无）
- 参数: self, name
- 返回推断: bool
- 关注点: COM, 进程
- 调用概览: Close, Item, GetActiveObject
- 理解: 主要用于关闭/终止相关逻辑。实现特征：执行关闭文档。依赖 CAD COM 对象与当前文档/模型空间。
- 风险: 依赖 CAD COM 状态，易受忙碌/断连影响；涉及进程控制，可能影响系统稳定
- 测试点: 参数合法性与边界值；CAD未启动/忙碌/无文档场景

### li()
- 说明: （无）
- 参数: （无）
- 返回推断: object
- 关键调用: C.li
- 调用概览: li
- 理解: 主要用于处理相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### save_file()
- 说明: （无）
- 参数: （无）
- 返回推断: object
- 调用概览: save_file
- 理解: 主要用于保存/写入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### save_file_as(p)
- 说明: （无）
- 参数: p
- 返回推断: object
- 调用概览: save_file_as
- 理解: 主要用于保存/写入相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### open_file(p)
- 说明: （无）
- 参数: p
- 返回推断: object
- 调用概览: open_file
- 理解: 主要用于打开/读取相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### close_file(o)
- 说明: （无）
- 参数: o
- 返回推断: object
- 调用概览: close_file
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### close_dwg_by_name(n)
- 说明: （无）
- 参数: n
- 返回推断: object
- 调用概览: close_dwg_by_name
- 理解: 主要用于关闭/终止相关逻辑。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

### retry_on_busy(func_or_args, **kwargs)
- 说明: 转发给 CAD_com_utils 的装饰器
- 邻近注释: 🔥【关键修复】直接使用别名调用，解决递归死锁
- 参数: func_or_args, **kwargs
- 返回推断: object
- 关键调用: retry_on_busy
- 调用概览: _tool_retry_on_busy
- 理解: 主要用于等待/守护相关逻辑。依据注释：转发给 CAD_com_utils 的装饰器。邻近注释提示：🔥【关键修复】直接使用别名调用，解决递归死锁。
- 风险: 逻辑分支较多时可能存在未覆盖路径
- 测试点: 参数合法性与边界值

## system/project_setup.py
- 模块说明: （无）