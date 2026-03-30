#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


VERSION = "2026-03-21.print-meta-v1"


SCRIPT_OVERRIDES: dict[str, dict[str, Any]] = {
    "print_area_analysis.py": {
        "script_role": "打印区域识别与标准图幅匹配脚本",
        "core_problem": "从 CAD 文档中识别候选打印区域，清理伪极大矩形，并与标准图幅、方向和比例规则进行匹配。",
        "layer_name": "打印区域分析层",
        "works_with": ["system.licad", "system.CAD_selection", "print_policy.py", "print_batch_dispatch.py"],
        "public_api": [
            "get_print_area_polylines",
            "get_pseudo_maximal_polylines",
            "match_standard_print_by_mode",
            "remove_pseudo_maxima_in_space",
        ],
        "applicable_scenarios": [
            "需要从模型空间或布局空间抽取矩形打印框",
            "需要按 basic/adaptive/purified_adaptive 模式做图幅匹配",
            "需要识别伪极大外包矩形并为后续净化链提供候选区域",
        ],
        "workflow": [
            "先收集多段线并筛选矩形候选。",
            "再计算标准图幅缓存、方向与比例匹配分数。",
            "随后去重并剔除伪极大矩形。",
            "最后输出打印区域与伪极大区域供后续策略层消费。",
        ],
        "must_keep_experience": [
            "矩形识别、标准图幅匹配与伪极大过滤不能割裂处理。",
            "purified_adaptive 依赖本脚本输出的候选区域和伪极大范围。",
        ],
        "known_limits": [
            "矩形和标准图幅判断包含经验阈值，后续仍需靠案例回归持续收束。",
        ],
        "domains": ["cad-com", "geometry", "print-analysis"],
    },
    "print_area_content_analysis.py": {
        "script_role": "打印区域内容净化分析脚本",
        "core_problem": "对候选打印区域内部内容做实体密度、文字、块与边框信息分析，识别伪打印区域，为 purified_adaptive 模式提供过滤依据。",
        "layer_name": "打印区域内容分析层",
        "works_with": ["print_area_analysis.py", "print_policy.py", "system.licad", "system.CAD_selection"],
        "public_api": [
            "collect_area_content_metrics",
            "classify_pseudo_print_area_candidates",
            "analyze_jobs_content",
            "run_content_analysis_case",
            "main",
        ],
        "applicable_scenarios": [
            "需要识别伪打印区域",
            "需要为打印计划提供内容风险标签",
            "需要针对 plan.json 批量生成 content_analysis.json",
        ],
        "workflow": [
            "先收集空间内实体快照。",
            "再按 bbox 汇总块、文字、线框等内容指标。",
            "随后对候选 job 分类，标记疑似伪打印区域。",
            "最后以 case 形式输出结构化分析结果。",
        ],
        "must_keep_experience": [
            "内容分析必须和打印计划按 handle 对齐，不能脱离 job 上下文。",
            "伪区域分类是 purified_adaptive 的辅助证据，不应直接替代最终范围判断。",
        ],
        "known_limits": [
            "内容指标依赖静态阈值和启发式判断，新案例可能需要继续调参。",
        ],
        "domains": ["cad-com", "content-analysis", "print-analysis"],
    },
    "print_area_scope_analysis.py": {
        "script_role": "伪极大打印范围二次收束脚本",
        "core_problem": "在伪极大矩形候选已知的前提下，判断最终保留的最大伪极大范围，并据此过滤打印 job。",
        "layer_name": "打印范围收束层",
        "works_with": ["print_area_analysis.py", "print_area_content_analysis.py", "print_policy.py"],
        "public_api": [
            "analyze_pseudo_maximal_scopes",
            "filter_jobs_by_largest_pseudo_scope",
            "run_scope_analysis_case",
            "main",
        ],
        "applicable_scenarios": [
            "purified_adaptive 命中伪极大矩形时需要二次范围分析",
            "需要按最大伪极大范围过滤最终打印 job",
        ],
        "workflow": [
            "先按 plan/job 和伪极大矩形建立范围候选。",
            "再计算面积与包含关系确定最大伪极大范围。",
            "随后过滤落在该范围之外的 job。",
            "最后输出 scope_analysis.json 供调度器消费。",
        ],
        "must_keep_experience": [
            "范围过滤必须建立在已有 job 集合上，不能重新发明区域识别逻辑。",
        ],
        "known_limits": [
            "当前只做单次最大范围收束，不覆盖更复杂的多片区策略。",
        ],
        "domains": ["cad-com", "scope-analysis", "print-analysis"],
    },
    "print_batch_dispatch.py": {
        "script_role": "打印目录级统一调度脚本",
        "core_problem": "对单文件或目录任务统一组织打印计划、执行、空白页修补、打印信息分析与最终结果汇总。",
        "layer_name": "打印调度层",
        "works_with": ["print_runner.py", "print_info_analysis.py", "print_policy.py", "print_verifier.py", "system.CAD_core"],
        "public_api": ["detect_blank_pdfs", "run_directory_dispatch", "main"],
        "applicable_scenarios": [
            "需要批量遍历目录中的 DWG 并按统一规则交付结果",
            "需要在打印后检测空白 PDF 并生成 blankfix 可视化副本",
            "需要复制最终 PDF/analysis/prosess 产物到公共输出目录",
        ],
        "workflow": [
            "先识别有效 DWG 输入并准备公共输出目录。",
            "再调用单文件打印主链，必要时追加 print info 与 blank fix。",
            "随后复制最终结果并关闭案例文档。",
            "最后汇总 batch_summary.json。",
        ],
        "must_keep_experience": [
            "目录级调度不能跳过单文件 run_print_case 主链。",
            "空白 PDF 检测与 blankfix 可视化是当前打印闭环的重要补救措施。",
        ],
        "known_limits": [
            "该脚本职责较重，后续可继续收束，但不能破坏目录级交付组织规则。",
        ],
        "domains": ["cad-com", "filesystem", "pdf", "dispatch"],
    },
    "print_executor.py": {
        "script_role": "打印计划执行器脚本",
        "core_problem": "根据打印计划逐 job 执行模型空间或布局空间导出，处理文档就绪、WPS 清理和 PDF 落盘等待。",
        "layer_name": "打印执行层",
        "works_with": ["print_policy.py", "print_verifier.py", "system.CAD_coordination", "system.licad"],
        "public_api": [
            "export_model_window_lisp_fit",
            "export_layout_window_lisp_fit",
            "cleanup_wps_windows",
            "execute_print_plan",
        ],
        "applicable_scenarios": [
            "需要对单个打印计划执行真实导出",
            "需要区分模型空间窗口打印和布局空间打印",
            "需要在执行后等待 PDF 文件稳定可读",
        ],
        "workflow": [
            "先确保目标文档与空间状态就绪。",
            "再按 job 类型走模型空间或布局空间导出分支。",
            "随后做 WPS 清理与 PDF 就绪等待。",
            "最后汇总执行结果。",
        ],
        "must_keep_experience": [
            "模型空间和布局空间的导出分支不能混淆。",
            "打印执行必须包含外部 PDF 稳定等待，而不是只发命令就认为完成。",
        ],
        "known_limits": [
            "直接依赖本地 CAD/WPS 环境，真实执行仍需串行独占。",
        ],
        "domains": ["cad-com", "pdf", "process-control"],
    },
    "print_info_analysis.py": {
        "script_role": "打印信息结构化分析脚本",
        "core_problem": "围绕打印区域提取图签块、文字、内框等页面信息，并输出 JSON 与 Excel 结果供人工复查和后续治理使用。",
        "layer_name": "打印信息分析层",
        "works_with": ["print_policy.py", "system.licad", "system.CAD_selection", "print_batch_dispatch.py"],
        "public_api": [
            "analyze_print_job_info",
            "analyze_print_info_jobs",
            "write_print_info_excel",
            "run_print_info_case",
            "main",
        ],
        "applicable_scenarios": [
            "需要为打印区域生成结构化页面信息",
            "需要输出可读 Excel 供人工复查",
            "需要配合目录级调度批量分析 plan.json 中的 job",
        ],
        "workflow": [
            "先激活目标文档和空间上下文。",
            "再提取图签块、内框与文字候选。",
            "随后按 job 生成页面级信息结果。",
            "最后写出 JSON 与 Excel。",
        ],
        "must_keep_experience": [
            "图签、内框与文字提取必须以打印区域为边界，不能脱离 job 独立分析。",
            "JSON 和 Excel 双输出都要保留，分别服务程序复用与人工复查。",
        ],
        "known_limits": [
            "图签字段和文字分类规则仍以启发式为主，需靠案例持续修补。",
        ],
        "domains": ["cad-com", "excel", "content-analysis"],
    },
    "print_policy.py": {
        "script_role": "打印计划构建与路径分配脚本",
        "core_problem": "把候选打印区域组织成稳定的 PrintPlan，完成模式归一、排序、路径分配与按 handle 过滤。",
        "layer_name": "打印策略层",
        "works_with": ["print_area_analysis.py", "print_executor.py", "print_runner.py"],
        "public_api": [
            "normalize_print_mode",
            "collect_print_jobs",
            "reindex_jobs_by_space",
            "assign_output_paths",
            "filter_jobs_by_handles",
            "build_print_plan",
            "plan_to_dict",
            "save_plan_json",
        ],
        "applicable_scenarios": [
            "需要从打印区域构造 job 列表和 plan.json",
            "需要控制 job 排序和输出命名",
            "需要在已有计划上按 handle 做再过滤",
        ],
        "workflow": [
            "先归一打印模式与区域匹配模式。",
            "再收集模型空间与布局空间 job。",
            "随后排序、重排索引并分配输出路径。",
            "最后生成 PrintPlan 并保存为 JSON。",
        ],
        "must_keep_experience": [
            "打印计划必须保持 job handle、空间与输出路径的稳定对应关系。",
            "模式归一和排序规则是主链稳定性的基础，不能随意漂移。",
        ],
        "known_limits": [
            "当前仍以内存对象和 JSON 为主，后续如拆分仍要保留 PrintPlan 的语义边界。",
        ],
        "domains": ["planning", "filesystem", "print-analysis"],
    },
    "print_runner.py": {
        "script_role": "单文件打印主链脚本",
        "core_problem": "围绕单个 DWG 组织 run 目录、构建打印计划、执行打印、校验结果并输出过程产物。",
        "layer_name": "单文件打印编排层",
        "works_with": ["print_policy.py", "print_executor.py", "print_verifier.py", "system.CAD_core"],
        "public_api": ["run_print_case", "main"],
        "applicable_scenarios": [
            "需要对单个 DWG 完成完整打印闭环",
            "需要产出 print_plan.json、print_summary.json 等过程文件",
        ],
        "workflow": [
            "先生成 process token 与 run 目录。",
            "再准备并激活目标文档，构建打印计划。",
            "随后执行打印并校验 PDF。",
            "最后写出 plan/summary 并收尾关闭文档。",
        ],
        "must_keep_experience": [
            "run 目录组织和过程文件落盘是后续回归分析的重要依据。",
            "单文件主链不能省略 plan、execute、verify 这三段。",
        ],
        "known_limits": [
            "对外仍主要服务单 DWG 场景，目录级批量调度应由 print_batch_dispatch.py 负责。",
        ],
        "domains": ["cad-com", "filesystem", "pdf", "orchestration"],
    },
    "print_verifier.py": {
        "script_role": "PDF 打印结果校验脚本",
        "core_problem": "读取计划中的页面尺寸与生成 PDF 的实际页面尺寸，输出验证结果并标记异常页面。",
        "layer_name": "打印校验层",
        "works_with": ["print_policy.py", "print_executor.py", "fitz"],
        "public_api": ["verify_generated_pdfs"],
        "applicable_scenarios": [
            "需要校验生成 PDF 的页数与尺寸是否符合计划",
            "需要把校验结果回写到打印 summary",
        ],
        "workflow": [
            "先从 plan/job 提取期望纸张尺寸。",
            "再读取 PDF 实际页面尺寸。",
            "随后按页做误差校验。",
            "最后输出整体验证结果与异常明细。",
        ],
        "must_keep_experience": [
            "计划尺寸和 PDF 实际尺寸必须逐页对齐比较，不能只看总页数。",
        ],
        "known_limits": [
            "当前聚焦页面尺寸，不覆盖更深层的内容质量校验。",
        ],
        "domains": ["pdf", "verification"],
    },
}


FUNCTION_OVERRIDES: dict[str, dict[str, dict[str, Any]]] = {
    "print_batch_dispatch.py": {
        "detect_blank_pdfs": {
            "purpose": "渲染已生成 PDF 的页面像素密度，识别视觉上近似空白的 PDF，供 blank-fix 补救链使用。",
            "outputs": ["返回疑似空白 PDF 列表，每项包含 pdf_path、reason、ratios 等证据。"],
            "returns": ["列表；为空表示当前 PDF 集合未发现空白页嫌疑。"],
            "steps": [
                "遍历待检查 PDF 路径。",
                "逐文件渲染页面并计算非白像素比例。",
                "把无页、渲染失败或最大非白比例低于阈值的 PDF 标记为嫌疑项。",
            ],
            "failure_paths": ["PDF 无法渲染时返回 render_failed 记录，而不是直接中断整批任务。"],
            "success_conditions": ["结果可直接驱动 blank-fix 和最终 PDF 过滤逻辑。"],
            "must_keep_experience": ["空白页判断依赖视觉非白比例，而不是只看文件存在或页数。"],
            "risk_level": "medium",
        },
        "run_directory_dispatch": {
            "purpose": "围绕目录或单文件输入组织完整批量打印闭环：初次打印、空白修补、print info 分析、最终复制、再过滤和清理。",
            "outputs": ["返回 batch_summary 结构，包含每个 DWG 的状态、过程路径、分析结果和最终交付路径。"],
            "returns": ["字典，至少包含 input_dir、output_root、mode、items、summary_json。"],
            "side_effects": ["创建批次输出目录、process 目录、公共 PDF/analysis 目录，并可能打开/关闭多个 CAD 文档。", "写出 batch_summary.json 与各单 DWG 过程文件。"],
            "dependencies": ["run_print_case", "run_print_info_case", "_copy_final_outputs", "_make_blank_fix_copy", "_make_print_area_visual_copy", "detect_blank_pdfs"],
            "preconditions": ["dwg_files 已经筛成有效 DWG 列表。", "output_root 所在磁盘路径可写。", "CAD 环境可被单文件主链接管。"],
            "steps": [
                "逐 DWG 准备公共输出目录并调用 run_print_case 执行初次打印。",
                "对已生成 PDF 做空白检测，必要时生成 blankfix 副本并重跑打印主链。",
                "基于 print_plan 和 content_analysis 调用 run_print_info_case 生成结构化页面信息。",
                "复制最终可交付 PDF，过滤最终仍为空白的结果，并生成打印区域可视化 DWG。",
                "按最终交付情况判定 success、failed 或 completed_no_valid_print_areas，并持续刷新 batch_summary.json。",
                "在 finally 中关闭工作 DWG 和案例 DWG，记录 cleanup 结果。",
            ],
            "failure_paths": [
                "任一 DWG 处理出错时，当前行会写成 failed，但不会中断整个批次。",
                "若已有打印计划但最终没有可交付 PDF，则标记 failed。",
            ],
            "success_conditions": ["每个 DWG 都形成清晰的状态行，并且 batch_summary.json 可用于后续回归或人工复查。"],
            "must_keep_experience": [
                "目录级调度必须复用 run_print_case 单文件主链，而不是另写一套打印实现。",
                "blank-fix、最终空白过滤和 print info 分析都应围绕同一批次过程目录组织。",
                "即使单文件失败，也要继续落 summary 并做收尾关图。",
            ],
            "risk_level": "high",
        },
        "main": {
            "purpose": "提供目录级调度 CLI，统一接收 --input-dir 或 --dwg，并打印最终 batch 结果 JSON。",
            "steps": [
                "配置 stdout/stderr 为 utf-8。",
                "解析输入目录、单文件路径、输出根目录和模式参数。",
                "校验 --input-dir 与 --dwg 只能二选一。",
                "构造 dwg_files 与 summary_root 后调用 run_directory_dispatch。",
                "把返回结果打印为 JSON。",
            ],
            "failure_paths": ["输入参数非法时直接 SystemExit。"],
            "success_conditions": ["CLI 输出的 JSON 与 batch_summary.json 一致并可直接复用。"],
        },
    },
    "print_runner.py": {
        "run_print_case": {
            "purpose": "围绕单个 DWG 完成打印主链：准备工作副本、可选 scope/content 分析、构建计划、执行打印、校验 PDF，并落盘 summary。",
            "outputs": ["返回单文件 print summary，包含 work_dwg、plan_json、content_analysis_json、scope_analysis_json、execution、verification 等信息。"],
            "returns": ["字典，作为 print_batch_dispatch 和人工调试的统一单文件结果对象。"],
            "side_effects": ["复制源 DWG 到工作目录、打开并激活 CAD 文档、写出 plan/content/scope/summary JSON，并可能生成 PDF。"],
            "dependencies": ["launch_cad_guardians", "assert_runtime_guard_ok", "run_scope_analysis_case", "build_print_plan", "analyze_jobs_content", "filter_jobs_by_largest_pseudo_scope", "filter_jobs_by_handles", "execute_print_plan", "verify_generated_pdfs"],
            "preconditions": ["输入 DWG 路径存在。", "CAD 与 runtime guard 可正常工作。", "输出根目录可写。"],
            "steps": [
                "归一化打印模式并启动 guardians/runtime guard 检查。",
                "创建 run_root/work_dir/pdf_dir，把源 DWG 复制成工作副本并打开激活。",
                "在 purified_adaptive 下先做 scope_analysis，再构建打印计划。",
                "如为 purified_adaptive，则对计划执行内容分析、按最大伪极大范围和 pseudo handles 二次收束，并重新分配输出路径。",
                "写出 print_plan.json 并在非 dry_run 且有 job 时执行打印与 PDF 校验。",
                "把 execution、verification 与过程路径整理进 print_summary.json，必要时关闭工作 DWG。",
            ],
            "failure_paths": [
                "工作 DWG 不存在、打开失败或无法激活时直接抛错。",
                "runtime guard 触发时由上层 CLI 转成结构化 guard error。",
            ],
            "success_conditions": ["summary 中的 plan、execution、verification 字段可完整支持后续目录级调度和回归分析。"],
            "must_keep_experience": [
                "必须先在工作副本上执行，而不是直接污染源 DWG。",
                "purified_adaptive 的 scope/content 两段收束必须发生在 execute_print_plan 之前。",
                "summary 要同时保存 plan_json 路径和展开后的 plan 字典，便于机器和人工双重复用。",
            ],
            "risk_level": "high",
        },
        "main": {
            "purpose": "提供单文件打印 CLI，负责把命令行参数映射到 run_print_case 并处理 runtime guard 异常输出。",
            "steps": [
                "配置 utf-8 输出。",
                "解析 dwg、output-root、mode、layout、dry-run、keep-open 等参数。",
                "调用 run_print_case。",
                "正常时打印 summary JSON，guard 触发时打印结构化错误并以退出码 2 结束。",
            ],
            "failure_paths": ["RuntimeGuardTriggered 时不会返回正常 summary，而是转换为 guard error JSON。"],
            "success_conditions": ["CLI 输出可直接被总管或人工消费。"],
        },
    },
    "print_executor.py": {
        "export_model_window_lisp_fit": {
            "purpose": "在模型空间中根据窗口点位构造 -plot LISP 命令，导出指定 PDF，并等待落盘完成。",
            "outputs": ["返回布尔值，表示模型空间导出是否成功。"],
            "returns": ["True 表示 PDF 已成功落盘；False 表示预备失败或等待超时。"],
            "side_effects": ["激活模型空间文档、删除已存在 PDF、向 CAD 发送 plot 命令。"],
            "dependencies": ["_ensure_model_doc_ready", "C.doc.SendCommand", "_wait_for_pdf_ready"],
            "preconditions": ["dwg_path 指向的工作 DWG 已可被当前 CAD 会话访问。", "point_a/point_b 构成有效窗口范围。"],
            "steps": [
                "归一窗口坐标并推导 Portrait/Landscape 方向。",
                "确保模型空间文档处于可打印状态。",
                "删除同名旧 PDF，构造 -plot 命令字符串并发送到 CAD。",
                "等待 PDF 就绪，失败时记录错误日志。",
            ],
            "failure_paths": ["模型空间预备失败或 PDF 就绪超时会返回 False。"],
            "success_conditions": ["目标 PDF 文件存在且可被 _wait_for_pdf_ready 判定为稳定。"],
            "must_keep_experience": ["发完 plot 命令后必须等待 PDF 稳定，不能立即视为成功。"],
            "risk_level": "high",
        },
        "export_layout_window_lisp_fit": {
            "purpose": "在指定布局中按窗口范围执行 -plot 命令导出 PDF，并等待结果落盘。",
            "outputs": ["返回布尔值，表示布局打印是否成功。"],
            "returns": ["True 表示布局 PDF 已稳定生成；False 表示布局预备失败或导出失败。"],
            "side_effects": ["切换目标布局、删除已存在 PDF、向 CAD 发送布局 plot 命令。"],
            "dependencies": ["_ensure_layout_doc_ready", "C.doc.SendCommand", "_wait_for_pdf_ready"],
            "preconditions": ["layout_name 对应布局存在并可被激活。"],
            "steps": [
                "确保目标布局文档已激活且就绪。",
                "删除同名旧 PDF，构造布局 plot 命令。",
                "发送命令并等待 PDF 就绪。",
                "失败时写日志，成功时返回 True。",
            ],
            "failure_paths": ["布局预备失败或 PDF 等待失败时返回 False。"],
            "success_conditions": ["目标布局的 PDF 文件成功生成且可读。"],
            "must_keep_experience": ["布局打印与模型空间打印的命令参数序列不同，不能混用。"],
            "risk_level": "high",
        },
        "cleanup_wps_windows": {
            "purpose": "清理 WPS Office/WPS PDF 残留窗口，减少批量打印过程中外部窗口对 CAD 焦点和资源的干扰。",
            "outputs": ["无显式返回，主要通过副作用清理外部窗口。"],
            "returns": ["无显式返回。"],
            "side_effects": ["枚举桌面窗口、关闭 WPS 窗口、必要时 taskkill wpspdf.exe，并尝试把焦点切回 AutoCAD。"],
            "steps": [
                "枚举窗口，识别 WPS Office/WPS PDF 可见窗口。",
                "尝试激活并关闭这些窗口。",
                "若仍残留则强制结束 wpspdf.exe。",
                "最后尝试把焦点切回 AutoCAD。",
            ],
            "failure_paths": ["缺少 win32 模块或窗口关闭失败时静默跳过。"],
            "success_conditions": ["WPS 残留窗口数量下降，并尽量恢复 CAD 焦点。"],
            "must_keep_experience": ["批量打印期间要周期性清理 WPS，避免窗口堆积干扰后续导出。"],
            "risk_level": "medium",
        },
        "execute_print_plan": {
            "purpose": "按空间和横竖方向批量执行 PrintPlan 中的所有 job，并记录成功、失败与生成文件列表。",
            "outputs": ["返回 PrintExecutionSummary，包含 total_jobs、success_count、failure_count、generated_files 和 failures。"],
            "returns": ["PrintExecutionSummary 数据类实例。"],
            "side_effects": ["逐 job 调用真实打印导出，期间可能等待、清理 WPS、触发 runtime guard 检查。"],
            "dependencies": ["_run_job", "_cleanup_wps_if_needed", "assert_runtime_guard_ok", "PrintExecutionSummary"],
            "preconditions": ["plan.jobs_by_space 已完成排序和输出路径分配。"],
            "steps": [
                "按 layout_name 遍历 jobs，并拆成 landscapes 与 portraits 两个批次。",
                "每个批次开始前执行 runtime guard 检查。",
                "逐 job 调用 _run_job；成功则累计 generated_files，失败则记录 failures。",
                "在横向批和竖向批之间强制清理 WPS 并等待 safety_delay。",
                "每个 layout 完成后再次强制清理 WPS，最后返回执行汇总。",
            ],
            "failure_paths": [
                "_run_job 抛异常时会被捕获并记录为失败项，不中断整个计划。",
                "runtime guard 触发时由 assert_runtime_guard_ok 向上抛出阻塞执行。",
            ],
            "success_conditions": ["返回的 execution summary 能直接被 verify_generated_pdfs 和 print_summary 消费。"],
            "must_keep_experience": [
                "横向和竖向 job 要分批执行，中间插入 WPS 清理和安全延时。",
                "单 job 失败不能中断整个计划，必须继续处理剩余 job。",
            ],
            "risk_level": "high",
        },
    },
    "print_info_analysis.py": {
        "analyze_print_job_info": {
            "purpose": "围绕单个打印 job 提取内框、右下角图签块、属性字段和文字候选，形成页面级结构化信息。",
            "outputs": ["返回单页分析字典，包含 drawing_title、drawing_no、project_name、title_block_*、inner_frame_* 等字段。"],
            "returns": ["字典；即使未找到内框或图签，也会返回 stop_reason 说明停在何处。"],
            "dependencies": ["_make_page_key", "_choose_inner_frame", "_choose_corner_block", "_match_field_from_attrs", "select_texts_in_bbox", "_classify_text_candidates"],
            "steps": [
                "先计算 page_key，并选择最合适的 inner frame。",
                "若找到 inner frame，则继续在右下角区域选择图签块。",
                "若图签块是属性块，则直接按 tag hints 读取标题、图号和项目名。",
                "若图签块是普通块，则在其 bbox 内提取文字并分类。",
                "把候选结果、stop_reason 和页面基础信息整合成单页记录。",
            ],
            "failure_paths": [
                "未找到 inner frame 时 stop_reason=no_inner_frame。",
                "找到 inner frame 但未找到角部图签块时 stop_reason=no_corner_block。",
            ],
            "success_conditions": ["返回结果可直接汇总到 print_info_dict、Excel 和后续统计。"],
            "must_keep_experience": [
                "页面分析必须先找 inner frame，再找角部图签块，不能颠倒顺序。",
                "属性块和普通块必须走不同提取分支。",
            ],
            "risk_level": "high",
        },
        "analyze_print_info_jobs": {
            "purpose": "按空间批量分析多个打印 job，复用矩形和块快照缓存，并生成 print_info_dict/page_info_dict 等总结果。",
            "outputs": ["返回总统计、rows_by_space、print_info_dict、print_info_dict_by_space 和 page_info_dict。"],
            "returns": ["字典，供 JSON 输出、Excel 写入和目录级调度复用。"],
            "dependencies": ["_collect_rectangles_by_owner", "collect_space_block_snapshots", "analyze_print_job_info", "_resolve_owner_btr_name"],
            "steps": [
                "先按 owner_btr 收集矩形集合，并建立 blocks_cache。",
                "逐空间遍历 jobs，为同一 owner_btr 复用 block snapshots。",
                "调用 analyze_print_job_info 生成单页记录，并同步构建 info_rows/page_info_dict。",
                "最后计算总页数、找到内框/图签/标题/图号/项目名的统计计数。",
            ],
            "failure_paths": ["某页局部信息不足时仍保留该页记录，只通过 stop_reason 表达缺失。"],
            "success_conditions": ["统计结果与分页字典可同时服务机器复用和人工复查。"],
            "must_keep_experience": ["同一空间的 block snapshots 应缓存复用，避免重复遍历 CAD 实体。"],
            "risk_level": "high",
        },
        "write_print_info_excel": {
            "purpose": "把 print info 分析结果写成 summary、print_info、text_records 三个工作表，供人工复查。",
            "outputs": ["返回已保存的 Excel 路径。"],
            "returns": ["Path，指向生成的 xlsx 文件。"],
            "side_effects": ["创建工作簿并写出 Excel 文件。"],
            "steps": [
                "创建 workbook，并写入 summary 页的总体统计。",
                "写入 print_info 明细页，按 sequence_no/page_key 排序页面记录。",
                "写入 text_records 页，展开每页采集到的文字记录。",
                "统一设置冻结窗格、列宽和自动换行，最后保存文件。",
            ],
            "failure_paths": ["openpyxl 不可用或输出路径不可写时会抛异常给上层。"],
            "success_conditions": ["Excel 可直接用于人工核对页面信息。"],
            "must_keep_experience": ["JSON 结果和 Excel 结果必须保持同一批数据口径。"],
            "risk_level": "medium",
        },
        "run_print_info_case": {
            "purpose": "围绕单个 DWG 组织 print info 分析闭环：准备文档、获取 jobs、处理 pseudo 区域排除、输出 JSON 和 Excel。",
            "outputs": ["返回完整 print info 结果字典，并在磁盘上生成 print_info_analysis.json 与同名 xlsx。"],
            "returns": ["字典，包含 print_mode、requested_handles、excluded_handle_count、excel_path 和分析统计。"],
            "side_effects": ["可能打开/激活/关闭 DWG，可能补建 content_analysis.json，并写出 JSON/Excel。"],
            "dependencies": ["launch_cad_guardians", "assert_runtime_guard_ok", "build_print_plan", "analyze_jobs_content", "_load_excluded_handles", "_filter_jobs_by_requested_handles", "_exclude_handles_and_reindex", "analyze_print_info_jobs", "write_print_info_excel"],
            "preconditions": ["dwg_path 存在。", "输出路径可写。", "若提供 plan_json_path，应与目标 DWG 匹配。"],
            "steps": [
                "启动 guardians 并确保目标 DWG 已打开激活。",
                "优先从现有 plan_json 读取 jobs；若没有则临时构建打印计划。",
                "在 purified_adaptive 且缺少 content_json 时，补做 content analysis 以获得 pseudo handles。",
                "读取 excluded handles，并按 requested_handles 和 pseudo handles 过滤、重排 jobs。",
                "调用 analyze_print_info_jobs 生成结构化结果，随后写出 JSON 和 Excel。",
                "若本次是临时打开文档且 keep_open=False，则在结束时关闭 DWG。",
            ],
            "failure_paths": [
                "DWG 打开或激活失败时直接抛错。",
                "runtime guard 触发时由 CLI 分支转换为 guard error JSON。",
            ],
            "success_conditions": ["结果 JSON 与 Excel 同时生成，且统计字段能支撑目录级汇总。"],
            "must_keep_experience": [
                "print info 分析必须与 plan/jobs 保持同一 handle 与 sequence 口径。",
                "requested_handles 过滤和 pseudo handles 排除都必须在 reindex 之后保持稳定序号。",
            ],
            "risk_level": "high",
        },
        "main": {
            "purpose": "提供 print info CLI，接收 dwg/plan/content/output/mode/handle 参数并输出结构化 JSON。",
            "steps": [
                "配置 utf-8 输出。",
                "解析 dwg、plan-json、content-json、output、layout、handle 等参数。",
                "推导默认 output_path 并调用 run_print_info_case。",
                "正常时打印结果 JSON，guard 触发时打印 guard error 并退出码 2。",
            ],
            "failure_paths": ["RuntimeGuardTriggered 时改走 guard error 输出。"],
            "success_conditions": ["CLI 输出与落盘 JSON 口径一致。"],
        },
    },
    "print_policy.py": {
        "normalize_print_mode": {
            "purpose": "把用户输入的打印模式统一成 basic/adaptive/purified_adaptive 三种受支持值，并拒绝非法模式。",
            "outputs": ["返回规范化后的模式字符串。"],
            "returns": ["字符串；非法模式时抛 ValueError。"],
            "failure_paths": ["模式不在 PRINT_MODES 中时抛 ValueError。"],
            "success_conditions": ["后续所有策略与执行模块都使用统一模式值。"],
            "must_keep_experience": ["打印主链只允许三种模式，不能再引入旧 analysis 模式。"],
        },
        "collect_print_jobs": {
            "purpose": "从模型空间和布局空间收集打印区域，生成按空间分组且已排序的 PrintJob 列表。",
            "outputs": ["返回 jobs_by_space 字典，key 为 layout 名，value 为 PrintJob 列表。"],
            "returns": ["字典；空字典表示未收集到可打印区域。"],
            "dependencies": ["get_print_area_polylines", "_layout_name_map", "_make_job", "_collect_layout_viewports", "_sort_jobs", "get_layout_names"],
            "steps": [
                "归一 mode，并读取打印区域与布局映射。",
                "在 include_model 下从模型空间候选区域生成 model jobs。",
                "在 include_layouts 下，先从纸空间候选区域生成布局 jobs，再补充布局视口 jobs。",
                "按布局顺序和行列规则排序，并为每个 job 赋 sequence_no。",
            ],
            "failure_paths": ["某个候选区域无法匹配标准图幅时会跳过并记 warning。"],
            "success_conditions": ["返回的 jobs_by_space 已完成基本排序，可直接进入路径分配。"],
            "must_keep_experience": [
                "模型空间和布局空间都可能输出，不应默认二选一。",
                "布局 jobs 要同时考虑纸空间打印框和布局视口候选。",
            ],
            "risk_level": "high",
        },
        "assign_output_paths": {
            "purpose": "按 layout 名和 sequence_no 为每个 PrintJob 分配稳定的 PDF 输出路径。",
            "outputs": ["无显式返回，直接更新各 job.output_path。"],
            "returns": ["无显式返回。"],
            "side_effects": ["修改 PrintJob.output_path。"],
            "steps": [
                "按 layout_name 构造布局目录名。",
                "按 source_stem、layout_name、sequence_no 生成文件名。",
                "回写到每个 job.output_path。",
            ],
            "success_conditions": ["所有 job 都获得稳定、可预测的输出路径。"],
            "must_keep_experience": ["输出命名必须稳定，便于目录级调度复制和后续校验。"],
            "risk_level": "medium",
        },
        "build_print_plan": {
            "purpose": "把 DWG 路径、模式和输出根目录整理成完整 PrintPlan 对象，是执行器和分析器的统一输入。",
            "outputs": ["返回 PrintPlan 数据类实例。"],
            "returns": ["PrintPlan。"],
            "dependencies": ["normalize_print_mode", "collect_print_jobs", "assign_output_paths", "PrintPlan"],
            "steps": [
                "归一输入路径、输出根目录和模式。",
                "调用 collect_print_jobs 收集并排序 jobs。",
                "调用 assign_output_paths 为所有 jobs 分配 PDF 路径。",
                "返回包含 dwg_path/output_root/source_stem/mode/jobs_by_space 的 PrintPlan。",
            ],
            "success_conditions": ["PrintPlan 可直接被 execute_print_plan、plan_to_dict 和 print info 分析复用。"],
            "must_keep_experience": ["计划层和执行层要通过 PrintPlan 解耦，不能在执行器里重新发明计划逻辑。"],
            "risk_level": "high",
        },
        "save_plan_json": {
            "purpose": "把 PrintPlan 以结构化 JSON 落盘，作为后续执行、分析和回归的权威计划文件。",
            "outputs": ["返回 plan.json 路径。"],
            "returns": ["Path。"],
            "side_effects": ["写入磁盘 JSON 文件。"],
            "steps": [
                "确保目标目录存在。",
                "把 PrintPlan 转成可序列化字典。",
                "写出 JSON 并返回路径。",
            ],
            "success_conditions": ["plan.json 可被 print_runner、print_batch_dispatch 和 print_info_analysis 复用。"],
            "must_keep_experience": ["plan.json 是主链的重要中间契约文件，不应省略。"],
            "risk_level": "medium",
        },
    },
    "print_area_content_analysis.py": {
        "classify_pseudo_print_area_candidates": {
            "purpose": "基于复杂度、中值基线、实体数量和填充率，把候选区域判定为 pseudo candidate 或 valid area。",
            "outputs": ["返回带 pseudo_candidate 和 reasons 的指标列表。"],
            "returns": ["列表；每项都补充 baselines、reasons 和 pseudo_candidate 标记。"],
            "steps": [
                "先计算 complexity/entity 的中位数基线。",
                "逐候选计算 very_low_complexity、very_few_entities、simple_content_only、low_fill 等条件。",
                "综合条件给出 pseudo_candidate 标记和 reasons。",
            ],
            "must_keep_experience": ["伪区域判断要基于相对基线，而不是只用固定绝对阈值。"],
            "risk_level": "medium",
        },
        "analyze_jobs_content": {
            "purpose": "按空间批量分析 job 的内容复杂度，并输出 pseudo candidates、lowest12_by_complexity 和 rows_by_space。",
            "outputs": ["返回 content analysis 总结果字典。"],
            "returns": ["字典，包含 snapshot_count、total_areas、pseudo_candidates、jobs_by_space 等。"],
            "steps": [
                "逐空间收集实体快照并转换 job 字典。",
                "调用 analyze_job_content_candidates 生成每个 job 的内容指标。",
                "汇总 all_rows，并筛出 pseudo_candidates 与最低复杂度样本。",
            ],
            "must_keep_experience": ["content analysis 输出必须保留 pseudo_candidates 和按空间 rows，供后续过滤与调试。"],
            "risk_level": "high",
        },
        "run_content_analysis_case": {
            "purpose": "围绕单个 DWG 执行内容分析闭环，必要时临时构建打印计划，并写出 content_analysis.json。",
            "outputs": ["返回 content analysis 结果字典，并写出 output_path。"],
            "returns": ["字典。"],
            "steps": [
                "确保 DWG 已打开激活，并通过 runtime guard 检查。",
                "优先读取现有 plan_json；否则临时构建打印计划。",
                "调用 analyze_jobs_content 生成分析结果。",
                "写出 output_path，并按 need_open/keep_open 决定是否关图。",
            ],
            "must_keep_experience": ["内容分析既能消费现有 plan.json，也能在独立模式下自己补建临时计划。"],
            "risk_level": "high",
        },
    },
}


PATTERN_PURPOSES = [
    ("_normalize_path", "归一化路径字符串，保证文档匹配、打开和关闭逻辑使用统一格式。"),
    ("_is_name_only_target", "判断输入目标是否只有文件名，用于兼容仅按文档名定位的场景。"),
    ("_find_document_by_path", "按路径或名称在当前 CAD 会话中定位目标文档。"),
    ("_activate_document_by_path", "按路径激活目标文档，并在必要时等待文档成为当前活动文档。"),
    ("_close_document_by_path", "按路径关闭目标文档，减少后续调度对会话的干扰。"),
    ("run_", "执行单次 case 或主链流程，并把结果写入结构化产物。"),
    ("main", "提供命令行入口，解析参数后调用主流程。"),
    ("collect_", "收集候选对象、空间数据或指标，并返回给上层流程。"),
    ("classify_", "按启发式规则对候选对象进行分类或打标签。"),
    ("analyze_", "围绕输入对象执行分析流程，并输出结构化结果。"),
    ("build_", "构造中间配置、缓存或计划对象，供主流程复用。"),
    ("match_", "执行匹配、评分或模式归一逻辑。"),
    ("filter_", "按范围、handle 或条件过滤已有候选集合。"),
    ("remove_", "删除重复、伪候选或不再需要的对象。"),
    ("select_", "按 CAD 条件选取目标实体集合。"),
    ("assign_", "为已有对象分配输出属性、路径或索引。"),
    ("save_", "把结构化结果保存到磁盘文件。"),
    ("write_", "把结构化结果写出到目标文件。"),
    ("verify_", "对生成结果执行校验，并输出通过/失败信息。"),
    ("execute_", "遍历计划并执行真实打印或导出动作。"),
    ("export_", "向外部文件导出 PDF 或布局结果。"),
    ("cleanup_", "清理外部窗口、临时对象或残留状态。"),
]


def infer_root(start: Path) -> Path:
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent
    while True:
        if cur.name.lower() == "codex-tasks":
            return cur
        if cur.parent == cur:
            raise RuntimeError("Cannot find codex-tasks root")
        cur = cur.parent


ROOT = infer_root(Path.cwd())
PRINT_DIR = ROOT / "cad" / "scripts" / "drawing_basic_service" / "print"


@dataclass
class FuncInfo:
    name: str
    qualname: str
    symbol: str
    signature: str
    lineno: int
    end_lineno: int
    is_method: bool
    args: list[dict[str, Any]]
    dependencies: list[str]
    has_return_value: bool
    returns_none_only: bool


class CallCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.calls: list[str] = []

    def visit_Call(self, node: ast.Call) -> Any:
        name = self._name(node.func)
        if name:
            self.calls.append(name)
        self.generic_visit(node)

    def _name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = self._name(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        return ""


def function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    try:
        args_text = ast.unparse(node.args)
    except Exception:
        args_text = "..."
    signature = f"{prefix} {node.name}({args_text})"
    if node.returns is not None:
        try:
            signature += f" -> {ast.unparse(node.returns)}"
        except Exception:
            pass
    return signature + ":"


def parse_args(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, Any]]:
    args = node.args
    positional = list(args.posonlyargs) + list(args.args)
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    result: list[dict[str, Any]] = []
    for arg_node, default in zip(positional, defaults):
        raw = arg_node.arg
        if arg_node.annotation is not None:
            try:
                raw += f": {ast.unparse(arg_node.annotation)}"
            except Exception:
                pass
        if default is not None:
            try:
                raw += f" = {ast.unparse(default)}"
            except Exception:
                raw += " = <expr>"
        result.append({"name": arg_node.arg, "raw": raw, "required": default is None})
    if args.vararg:
        raw = f"*{args.vararg.arg}"
        if args.vararg.annotation is not None:
            try:
                raw += f": {ast.unparse(args.vararg.annotation)}"
            except Exception:
                pass
        result.append({"name": f"*{args.vararg.arg}", "raw": raw, "required": False})
    for kwarg_node, default in zip(args.kwonlyargs, args.kw_defaults):
        raw = kwarg_node.arg
        if kwarg_node.annotation is not None:
            try:
                raw += f": {ast.unparse(kwarg_node.annotation)}"
            except Exception:
                pass
        if default is not None:
            try:
                raw += f" = {ast.unparse(default)}"
            except Exception:
                raw += " = <expr>"
        result.append({"name": kwarg_node.arg, "raw": raw, "required": default is None})
    if args.kwarg:
        raw = f"**{args.kwarg.arg}"
        if args.kwarg.annotation is not None:
            try:
                raw += f": {ast.unparse(args.kwarg.annotation)}"
            except Exception:
                pass
        result.append({"name": f"**{args.kwarg.arg}", "raw": raw, "required": False})
    return result


def collect_functions(tree: ast.Module) -> list[FuncInfo]:
    result: list[FuncInfo] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result.append(build_func_info(node))
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    result.append(build_func_info(item, class_name=node.name))
    return result


def build_func_info(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    class_name: str | None = None,
) -> FuncInfo:
    collector = CallCollector()
    collector.visit(node)
    returns = [item for item in ast.walk(node) if isinstance(item, ast.Return)]
    has_return_value = any(ret.value is not None for ret in returns)
    returns_none_only = bool(returns) and not has_return_value
    qualname = f"{class_name}.{node.name}" if class_name else node.name
    return FuncInfo(
        name=qualname,
        qualname=qualname,
        symbol=node.name,
        signature=function_signature(node),
        lineno=getattr(node, "lineno", -1),
        end_lineno=getattr(node, "end_lineno", -1),
        is_method=class_name is not None,
        args=parse_args(node),
        dependencies=sorted(dict.fromkeys(name for name in collector.calls if name))[:8],
        has_return_value=has_return_value,
        returns_none_only=returns_none_only,
    )


def infer_purpose(func_name: str) -> str:
    short = func_name.split(".")[-1]
    for prefix, purpose in PATTERN_PURPOSES:
        if short.startswith(prefix):
            return purpose
    if short.startswith("_"):
        return "提供局部辅助步骤、转换或兼容逻辑，服务同脚本主流程。"
    return "承接脚本中的业务步骤、状态组织或结果转换逻辑。"


def function_override(script_name: str, func_name: str) -> dict[str, Any]:
    return FUNCTION_OVERRIDES.get(script_name, {}).get(func_name, {})


def apply_override(entry: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    if not override:
        return entry
    for key, value in override.items():
        entry[key] = value
    return entry


def classify_level(func: FuncInfo, public_api: list[str]) -> str:
    if func.qualname in public_api or func.symbol in public_api:
        return "core"
    short = func.symbol
    if short == "main":
        return "normal"
    if short.startswith("_"):
        return "utility"
    if short.startswith(("collect_", "analyze_", "build_", "match_", "filter_", "remove_", "select_", "assign_", "save_", "write_", "verify_")):
        return "normal"
    return "utility"


def infer_outputs(func: FuncInfo) -> list[str]:
    short = func.symbol
    if short.startswith(("save_", "write_")):
        return ["向磁盘写出 JSON、Excel 或其他结构化产物。"]
    if short.startswith(("export_", "execute_", "run_")):
        return ["产出执行结果、PDF 文件或结构化 summary。"]
    if short.startswith(("collect_", "analyze_", "build_", "match_", "filter_", "select_", "verify_")):
        return ["返回供上层流程继续消费的集合、字典、计划或校验结果。"]
    if func.returns_none_only:
        return ["主要通过副作用更新运行状态、当前文档或外部文件。"]
    if func.has_return_value:
        return ["返回局部计算结果、状态对象或结构化数据。"]
    return ["为同脚本主流程提供轻量辅助结果或副作用。"]


def infer_returns(func: FuncInfo) -> list[str]:
    if func.returns_none_only:
        return ["无显式业务返回值，主要依赖副作用。"]
    if func.has_return_value:
        return ["按分支返回结构化数据、布尔状态、路径或对象引用。"]
    return ["可能无显式返回，或由上层通过副作用感知结果。"]


def infer_side_effects(func: FuncInfo) -> list[str]:
    short = func.symbol
    effects: list[str] = []
    if any(short.startswith(prefix) for prefix in ("save_", "write_", "_write_json")):
        effects.append("写入磁盘文件。")
    if any(short.startswith(prefix) for prefix in ("open_", "close_", "activate_", "execute_", "export_", "cleanup_", "run_")):
        effects.append("改变当前 CAD 文档、外部进程窗口或导出状态。")
    if short in {"main"}:
        effects.append("解析命令行参数并触发 CLI 输出。")
    return effects


def infer_risk(func: FuncInfo) -> str:
    short = func.symbol
    if any(short.startswith(prefix) for prefix in ("run_", "execute_", "export_", "save_", "write_", "verify_", "cleanup_")):
        return "medium"
    if any(short.startswith(prefix) for prefix in ("_activate_", "_close_", "_find_document", "collect_", "analyze_", "build_")):
        return "medium"
    return "low"


def infer_preconditions(func: FuncInfo) -> list[str]:
    short = func.symbol
    preconditions: list[str] = []
    if "document" in short or "activate" in short or "close" in short:
        preconditions.append("当前 CAD 会话应可访问目标文档或文档名。")
    if short.startswith(("run_", "execute_", "export_")):
        preconditions.append("输入路径、计划或 job 集合应已准备完成。")
    if short.startswith(("save_", "write_")):
        preconditions.append("目标输出路径应可写。")
    return preconditions


def infer_steps(func: FuncInfo) -> list[str]:
    short = func.symbol
    if short == "main":
        return [
            "解析命令行参数。",
            "把参数整理为主流程所需输入。",
            "调用主流程函数并输出结果。",
        ]
    if short.startswith(("run_", "execute_")):
        return [
            "校验输入并准备运行上下文。",
            "调用同脚本或相邻模块的核心流程函数。",
            "汇总执行结果并写出结构化产物。",
        ]
    if short.startswith(("collect_", "analyze_", "build_", "match_", "filter_", "verify_")):
        return [
            "读取输入对象或候选集合。",
            "执行当前函数负责的分析、匹配或过滤逻辑。",
            "返回供上层继续消费的结果。",
        ]
    if short.startswith(("save_", "write_")):
        return [
            "整理待落盘的数据结构。",
            "写出目标文件。",
            "返回路径、状态或无显式返回。",
        ]
    return [
        "读取局部输入。",
        "执行当前 helper 逻辑。",
        "返回局部结果或通过副作用服务主流程。",
    ]


def infer_failure_paths(func: FuncInfo) -> list[str]:
    short = func.symbol
    failures: list[str] = []
    if short.startswith(("run_", "execute_", "export_")):
        failures.append("目标文档、计划或外部环境不可用时流程失败。")
    if short.startswith(("save_", "write_", "_write_json")):
        failures.append("输出路径不可写或磁盘文件被占用时写出失败。")
    if "document" in short or "activate" in short or "close" in short:
        failures.append("目标文档定位失败时只能返回空值、False 或抛出异常。")
    if not failures:
        failures.append("输入形态不满足预期时返回空结果、False 或抛出异常。")
    return failures


def infer_success_conditions(func: FuncInfo) -> list[str]:
    short = func.symbol
    if short.startswith(("run_", "execute_", "export_")):
        return ["目标产物已生成，且返回 summary、路径或状态对象。"]
    if short.startswith(("save_", "write_")):
        return ["目标文件已成功落盘。"]
    if short.startswith(("collect_", "analyze_", "build_", "match_", "filter_", "verify_")):
        return ["返回结果可被上层流程直接消费。"]
    return ["局部结果可被同脚本主流程继续使用。"]


def infer_must_keep(func: FuncInfo) -> list[str]:
    short = func.symbol
    keeps: list[str] = []
    if short.startswith(("run_", "execute_")):
        keeps.append("保持当前主链的顺序组织，不要跳过准备、执行和收尾阶段。")
    if short.startswith(("collect_", "analyze_", "filter_")):
        keeps.append("返回结构应与上层 plan/job/summary 消费接口保持兼容。")
    if short.startswith(("save_", "write_")):
        keeps.append("输出文件命名和目录组织应保持稳定。")
    return keeps


def build_script_quote(path: Path, funcs: list[FuncInfo], cfg: dict[str, Any]) -> dict[str, Any]:
    public_api = cfg["public_api"]
    listed = []
    for func in funcs:
        level = classify_level(func, public_api)
        listed.append(
            {
                "name": func.name,
                "role": infer_purpose(func.name),
                "level": level,
                "input_shape": "见源码签名与函数级 meta",
                "output_shape": "返回结构化结果、状态或通过副作用服务主链",
            }
        )
    return {
        "meta_version": "2.0",
        "meta_scope": "script",
        "script": {
            "name": path.name,
            "path": path.as_posix(),
            "encoding": "utf-8",
            "version": VERSION,
        },
        "quote": {
            "goal": cfg["core_problem"],
            "public_api": public_api,
            "script_role": cfg["script_role"],
            "system_position": {
                "layer_name": cfg["layer_name"],
                "works_with": cfg["works_with"],
                "main_entry_note": f"{path.name} 主要通过 {', '.join(public_api[:3])} 等入口服务打印主链。",
            },
            "must_keep_experience": cfg["must_keep_experience"],
            "known_limits": cfg["known_limits"],
        },
        "functions": listed,
        "dependencies": {
            "runtime_domains": cfg["domains"],
            "script_focus": cfg["script_role"],
        },
        "quality": {
            "todo": [
                "当前脚本级 meta 已覆盖主角色与 public_api，后续如职责明显变化应同步刷新。",
                "函数级语义摘要主要由 AST 与命名规则生成，复杂分支后续可按案例继续细化。",
            ],
            "function_count": len(funcs),
            "public_api_count": len(public_api),
        },
    }


def build_script_procedure(path: Path, funcs: list[FuncInfo], cfg: dict[str, Any]) -> dict[str, Any]:
    public_api = cfg["public_api"]
    public_funcs = []
    for func in funcs:
        level = classify_level(func, public_api)
        public_funcs.append(
            {
                "name": func.name,
                "level": level,
                "steps": [
                    "读取调用输入并校验关键前提。",
                    "执行本脚本负责的核心流程或调用链。",
                    "返回结果或写出当前阶段产物。",
                ],
            }
        )
    return {
        "meta_version": "2.0",
        "meta_scope": "script",
        "script": {
            "name": path.name,
            "path": path.as_posix(),
            "encoding": "utf-8",
            "version": VERSION,
        },
        "procedure": {
            "goal": f"说明 {path.name} 在打印主链中的整体工作流。",
            "workflow": cfg["workflow"],
            "applicable_scenarios": cfg["applicable_scenarios"],
            "resource_boundary": [
                "仅负责当前脚本所属阶段，不替代上游目录级治理文档。",
                "涉及 CAD 真机执行时仍需复用 system.licad、CAD_coordination 与打印主链其它模块。",
            ],
        },
        "functions": public_funcs,
        "dependencies": {
            "runtime_domains": cfg["domains"],
            "script_focus": cfg["core_problem"],
        },
        "quality": {
            "todo": [
                "workflow 已覆盖主流程骨架，局部阈值、启发式参数仍需结合案例回归细化。",
            ],
            "function_count": len(funcs),
            "public_api_count": len(public_api),
        },
    }


def build_functions_quote(path: Path, funcs: list[FuncInfo], cfg: dict[str, Any]) -> dict[str, Any]:
    public_api = cfg["public_api"]
    rows = []
    core_count = 0
    for func in funcs:
        level = classify_level(func, public_api)
        if level == "core":
            core_count += 1
        entry = {
            "name": func.name,
            "symbol": func.symbol,
            "qualname": func.qualname,
            "level": level,
            "signature": func.signature,
            "purpose": infer_purpose(func.name),
            "inputs": func.args,
            "outputs": infer_outputs(func),
            "returns": infer_returns(func),
            "side_effects": infer_side_effects(func),
            "dependencies": func.dependencies,
            "risk_level": infer_risk(func),
            "evidence": {
                "line_start": func.lineno,
                "line_end": func.end_lineno,
            },
        }
        rows.append(apply_override(entry, function_override(path.name, func.name)))
    return {
        "meta_version": "2.0",
        "meta_scope": "functions",
        "script": {
            "name": path.name,
            "path": path.as_posix(),
            "encoding": "utf-8",
            "version": VERSION,
        },
        "functions_quote": {
            "goal": cfg["core_problem"],
            "coverage": "graded-all",
            "grading": {
                "core": "公共入口、真实打印/分析执行函数、关键导出与主链编排函数。",
                "normal": "主要业务辅助函数、候选收集与计划/分析组织函数。",
                "utility": "局部 helper、路径归一、轻量转换与兼容性函数。",
            },
            "public_api": public_api,
        },
        "functions": rows,
        "dependencies": {
            "runtime_domains": cfg["domains"],
            "script_focus": cfg["script_role"],
        },
        "quality": {
            "todo": [
                "purpose/outputs/returns 为静态命名与 AST 归纳结果，复杂运行时分支后续可再细化。",
                "dependencies 仅记录直接调用名，不代表完整跨模块调用图。",
            ],
            "function_count": len(funcs),
            "public_api_count": len(public_api),
            "core_function_count": core_count,
        },
    }


def build_functions_procedure(path: Path, funcs: list[FuncInfo], cfg: dict[str, Any]) -> dict[str, Any]:
    public_api = cfg["public_api"]
    rows = []
    core_count = 0
    for func in funcs:
        level = classify_level(func, public_api)
        if level == "core":
            core_count += 1
        entry: dict[str, Any] = {
            "name": func.name,
            "signature": func.signature,
            "level": level,
            "role": infer_purpose(func.name),
            "preconditions": infer_preconditions(func),
            "failure_paths": infer_failure_paths(func),
            "success_conditions": infer_success_conditions(func),
            "must_keep_experience": infer_must_keep(func),
            "evidence": {
                "line_start": func.lineno,
                "line_end": func.end_lineno,
            },
        }
        steps = infer_steps(func)
        if level == "utility":
            entry["brief_flow"] = steps
        else:
            entry["steps"] = steps
        rows.append(apply_override(entry, function_override(path.name, func.name)))
    return {
        "meta_version": "2.0",
        "meta_scope": "functions",
        "script": {
            "name": path.name,
            "path": path.as_posix(),
            "encoding": "utf-8",
            "version": VERSION,
        },
        "functions_procedure": {
            "goal": f"描述 {path.name} 中每个函数在打印主链中的步骤骨架。",
            "step_style": "graded",
            "public_api": public_api,
        },
        "functions": rows,
        "dependencies": {
            "runtime_domains": cfg["domains"],
            "script_focus": cfg["core_problem"],
        },
        "quality": {
            "todo": [
                "steps 为静态骨架摘要，未展开每个 CAD/COM 细节分支。",
                "复杂阈值或外部环境异常处理仍建议结合真实案例进一步人工细化。",
            ],
            "function_count": len(funcs),
            "public_api_count": len(public_api),
            "core_function_count": core_count,
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def output_paths(py_path: Path) -> dict[str, Path]:
    stem = py_path.stem
    return {
        "quote": py_path.with_name(f"{stem}_quote.meta.json"),
        "procedure": py_path.with_name(f"{stem}_procedure.meta.json"),
        "functions.quote": py_path.with_name(f"{stem}_functions.quote.meta.json"),
        "functions.procedure": py_path.with_name(f"{stem}_functions.procedure.meta.json"),
    }


def build_for_script(py_path: Path) -> list[Path]:
    cfg = SCRIPT_OVERRIDES[py_path.name]
    tree = ast.parse(py_path.read_text(encoding="utf-8"), filename=str(py_path))
    funcs = collect_functions(tree)
    targets = output_paths(py_path)
    write_json(targets["quote"], build_script_quote(py_path, funcs, cfg))
    write_json(targets["procedure"], build_script_procedure(py_path, funcs, cfg))
    write_json(targets["functions.quote"], build_functions_quote(py_path, funcs, cfg))
    write_json(targets["functions.procedure"], build_functions_procedure(py_path, funcs, cfg))
    return [targets["quote"], targets["procedure"], targets["functions.quote"], targets["functions.procedure"]]


def main() -> int:
    generated: list[Path] = []
    for py_path in sorted(PRINT_DIR.glob("*.py")):
        if py_path.name not in SCRIPT_OVERRIDES:
            raise KeyError(f"Missing override for {py_path.name}")
        generated.extend(build_for_script(py_path))
    for path in generated:
        print(path.as_posix())
    print(f"[OK] generated {len(generated)} meta files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
