#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试监测模块
用于测试前后的状态监测和对比
"""

# 路径引导
import sys
from pathlib import Path
current = Path(__file__).resolve()
while current.name != 'cad':
    if current.parent == current: raise Exception("找不到根目录")
    current = current.parent
sys.path.insert(0, str(current))

import os
import json
from datetime import datetime
from system.CAD_com_utils import sys_logger
from system.CAD_selection import ss_select


class TestMonitor:
    """测试监测器 - 用于测试前后的状态对比"""

    def __init__(self, test_name):
        """
        初始化测试监测器

        Args:
            test_name: 测试名称
        """
        self.test_name = test_name
        self.before_state = {}
        self.after_state = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def capture_dwg_state(self, description=""):
        """
        捕获当前DWG文件状态

        Args:
            description: 状态描述（before/after）

        Returns:
            dict: DWG文件状态信息
        """
        sys_logger.info(f"[监测] 捕获DWG状态 - {description}")

        state = {
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'objects': {}
        }

        try:
            # 统计各类对象数量
            lines = ss_select(mode="all", filter_types=[0], filter_data=["LINE"])
            state['objects']['lines'] = {
                'count': len(lines) if lines else 0,
                'handles': [obj.Handle for obj in lines] if lines else []
            }

            polylines = ss_select(mode="all", filter_types=[0], filter_data=["LWPOLYLINE"])
            state['objects']['polylines'] = {
                'count': len(polylines) if polylines else 0,
                'handles': [obj.Handle for obj in polylines] if polylines else []
            }

            circles = ss_select(mode="all", filter_types=[0], filter_data=["CIRCLE"])
            state['objects']['circles'] = {
                'count': len(circles) if circles else 0,
                'handles': [obj.Handle for obj in circles] if circles else []
            }

            blocks = ss_select(mode="all", filter_types=[0], filter_data=["INSERT"])
            state['objects']['blocks'] = {
                'count': len(blocks) if blocks else 0,
                'handles': [obj.Handle for obj in blocks] if blocks else []
            }

            # 计算总数
            state['total_objects'] = sum(
                state['objects'][key]['count']
                for key in state['objects']
            )

            sys_logger.info(f"  总对象数: {state['total_objects']}")

        except Exception as e:
            sys_logger.error(f"  捕获DWG状态失败: {e}")
            state['error'] = str(e)

        return state

    def capture_folder_state(self, folder_path, description=""):
        """
        捕获文件夹状态

        Args:
            folder_path: 文件夹路径
            description: 状态描述

        Returns:
            dict: 文件夹状态信息
        """
        sys_logger.info(f"[监测] 捕获文件夹状态 - {description}")

        state = {
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'folder_path': folder_path,
            'exists': False,
            'files': []
        }

        try:
            if os.path.exists(folder_path):
                state['exists'] = True

                # 列出所有文件
                files = []
                for root, dirs, filenames in os.walk(folder_path):
                    for filename in filenames:
                        file_path = os.path.join(root, filename)
                        file_info = {
                            'name': filename,
                            'path': file_path,
                            'size': os.path.getsize(file_path),
                            'ext': os.path.splitext(filename)[1]
                        }
                        files.append(file_info)

                state['files'] = files
                state['file_count'] = len(files)

                # 按扩展名统计
                ext_counts = {}
                for f in files:
                    ext = f['ext']
                    ext_counts[ext] = ext_counts.get(ext, 0) + 1

                state['ext_counts'] = ext_counts

                sys_logger.info(f"  文件数量: {state['file_count']}")
                sys_logger.info(f"  扩展名分布: {ext_counts}")
            else:
                sys_logger.info(f"  文件夹不存在: {folder_path}")

        except Exception as e:
            sys_logger.error(f"  捕获文件夹状态失败: {e}")
            state['error'] = str(e)

        return state

    def before_test(self, dwg_file=None, output_folders=None):
        """
        测试前监测

        Args:
            dwg_file: DWG文件路径（可选）
            output_folders: 输出文件夹列表（可选）
        """
        sys_logger.info("=" * 60)
        sys_logger.info(f"[测试前监测] {self.test_name}")
        sys_logger.info("=" * 60)

        self.before_state = {
            'test_name': self.test_name,
            'timestamp': self.timestamp
        }

        # 监测DWG文件状态
        if dwg_file:
            self.before_state['dwg'] = self.capture_dwg_state("测试前")

        # 监测输出文件夹状态
        if output_folders:
            self.before_state['folders'] = {}
            for folder in output_folders:
                folder_name = os.path.basename(folder)
                self.before_state['folders'][folder_name] = self.capture_folder_state(
                    folder, "测试前"
                )

        sys_logger.info("=" * 60)

    def after_test(self, dwg_file=None, output_folders=None):
        """
        测试后监测

        Args:
            dwg_file: DWG文件路径（可选）
            output_folders: 输出文件夹列表（可选）
        """
        sys_logger.info("=" * 60)
        sys_logger.info(f"[测试后监测] {self.test_name}")
        sys_logger.info("=" * 60)

        self.after_state = {
            'test_name': self.test_name,
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
        }

        # 监测DWG文件状态
        if dwg_file:
            self.after_state['dwg'] = self.capture_dwg_state("测试后")

        # 监测输出文件夹状态
        if output_folders:
            self.after_state['folders'] = {}
            for folder in output_folders:
                folder_name = os.path.basename(folder)
                self.after_state['folders'][folder_name] = self.capture_folder_state(
                    folder, "测试后"
                )

        sys_logger.info("=" * 60)

    def compare_and_judge(self, expected_changes):
        """
        对比测试前后状态并判断是否成功

        Args:
            expected_changes: 预期变化字典
                {
                    'dwg_objects_added': 10,  # 预期增加的对象数
                    'output_files_count': 15,  # 预期生成的文件数
                    'output_file_ext': '.pdf',  # 预期文件扩展名
                    ...
                }

        Returns:
            dict: {
                'status': 'EXECUTION_SUCCESS' | 'EXECUTION_FAILED',
                'passed': True/False,
                'details': {...},
                'message': '...'
            }
        """
        sys_logger.info("=" * 60)
        sys_logger.info("[判定] 对比测试前后状态")
        sys_logger.info("=" * 60)

        result = {
            'status': 'EXECUTION_SUCCESS',
            'passed': True,
            'details': {},
            'message': ''
        }

        checks = []

        # ========== 检查1：DWG对象变化 ==========
        if 'dwg' in self.before_state and 'dwg' in self.after_state:
            before_count = self.before_state['dwg'].get('total_objects', 0)
            after_count = self.after_state['dwg'].get('total_objects', 0)
            actual_added = after_count - before_count

            result['details']['dwg_objects'] = {
                'before': before_count,
                'after': after_count,
                'added': actual_added
            }

            if 'dwg_objects_added' in expected_changes:
                expected_added = expected_changes['dwg_objects_added']
                check_passed = (actual_added == expected_added)

                checks.append({
                    'name': 'DWG对象增加数量',
                    'expected': expected_added,
                    'actual': actual_added,
                    'passed': check_passed
                })

                sys_logger.info(f"  DWG对象: 预期增加{expected_added}, 实际增加{actual_added} - {'✓' if check_passed else '✗'}")

        # ========== 检查2：输出文件数量 ==========
        if 'folders' in self.after_state:
            for folder_name, folder_state in self.after_state['folders'].items():
                actual_count = folder_state.get('file_count', 0)

                result['details'][f'folder_{folder_name}'] = {
                    'file_count': actual_count,
                    'files': folder_state.get('files', [])
                }

                if 'output_files_count' in expected_changes:
                    expected_count = expected_changes['output_files_count']
                    check_passed = (actual_count == expected_count)

                    checks.append({
                        'name': f'输出文件数量 ({folder_name})',
                        'expected': expected_count,
                        'actual': actual_count,
                        'passed': check_passed
                    })

                    sys_logger.info(f"  输出文件: 预期{expected_count}个, 实际{actual_count}个 - {'✓' if check_passed else '✗'}")

                # 检查文件扩展名
                if 'output_file_ext' in expected_changes:
                    expected_ext = expected_changes['output_file_ext']
                    ext_counts = folder_state.get('ext_counts', {})
                    actual_ext_count = ext_counts.get(expected_ext, 0)

                    check_passed = (actual_ext_count > 0)

                    checks.append({
                        'name': f'输出文件扩展名 ({folder_name})',
                        'expected': expected_ext,
                        'actual': ext_counts,
                        'passed': check_passed
                    })

                    sys_logger.info(f"  文件扩展名: 预期{expected_ext}, 实际{ext_counts} - {'✓' if check_passed else '✗'}")

        # ========== 汇总判定 ==========
        all_passed = all(check['passed'] for check in checks)

        if all_passed:
            result['status'] = 'EXECUTION_SUCCESS'
            result['passed'] = True
            result['message'] = f"所有检查通过 ({len(checks)}/{len(checks)})"
            sys_logger.info(f"\n✓ 判定结果: 成功 - {result['message']}")
        else:
            result['status'] = 'EXECUTION_FAILED'
            result['passed'] = False
            failed_checks = [c for c in checks if not c['passed']]
            result['message'] = f"部分检查失败 ({len(checks)-len(failed_checks)}/{len(checks)})"
            sys_logger.error(f"\n✗ 判定结果: 失败 - {result['message']}")

            for check in failed_checks:
                sys_logger.error(f"  失败项: {check['name']}")
                sys_logger.error(f"    预期: {check['expected']}")
                sys_logger.error(f"    实际: {check['actual']}")

        result['checks'] = checks

        sys_logger.info("=" * 60)

        return result

    def save_report(self, result, output_path=None):
        """
        保存测试报告

        Args:
            result: 判定结果
            output_path: 输出路径（可选）
        """
        if output_path is None:
            output_path = f"tests/reports/{self.test_name}_{self.timestamp}.json"

        report = {
            'test_name': self.test_name,
            'timestamp': self.timestamp,
            'before_state': self.before_state,
            'after_state': self.after_state,
            'result': result
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        sys_logger.info(f"[报告] 已保存到: {output_path}")
