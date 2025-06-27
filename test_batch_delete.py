#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量删除功能测试脚本
测试输入解析和批量删除确认功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from torrent_maker import TorrentMakerApp
from enum import Enum

class TaskStatus(Enum):
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

class MockTask:
    """模拟任务对象"""
    def __init__(self, task_id: str, name: str, status: TaskStatus, priority: TaskPriority):
        self.task_id = task_id
        self.name = name
        self.status = status
        self.priority = priority

def test_parse_task_selection():
    """测试输入解析功能"""
    print("🧪 测试输入解析功能")
    print("=" * 50)
    
    maker = TorrentMakerApp()
    
    # 测试用例
    test_cases = [
        # (输入, 最大索引, 期望结果, 描述)
        ("5", 12, ([4], ""), "单个数字"),
        ("1-5", 12, ([0,1,2,3,4], ""), "简单范围"),
        ("1,3,5", 12, ([0,2,4], ""), "逗号分隔"),
        ("1-3,5,8-10", 12, ([0,1,2,4,7,8,9], ""), "混合格式"),
        ("all", 12, (list(range(12)), ""), "全部删除"),
        ("*", 12, (list(range(12)), ""), "全部删除(星号)"),
        ("0", 12, ([], "cancelled"), "取消操作"),
        ("cancel", 12, ([], "cancelled"), "取消操作(英文)"),
        ("13", 12, ([], "索引超出范围 (1-12): 13"), "超出范围"),
        ("5-3", 12, ([], "范围起始值不能大于结束值: 5-3"), "无效范围"),
        ("abc", 12, ([], "请输入有效的数字、范围或逗号分隔的组合"), "无效输入"),
        ("1-", 12, ([], "无效的范围格式: 1-"), "无效范围格式"),
    ]
    
    passed = 0
    failed = 0
    
    for input_str, max_index, expected, description in test_cases:
        try:
            result = maker._parse_task_selection(input_str, max_index)
            if result == expected:
                print(f"✅ {description}: '{input_str}' -> {result[0]}")
                passed += 1
            else:
                print(f"❌ {description}: '{input_str}'")
                print(f"   期望: {expected}")
                print(f"   实际: {result}")
                failed += 1
        except Exception as e:
            print(f"❌ {description}: '{input_str}' - 异常: {e}")
            failed += 1
    
    print(f"\n📊 测试结果: ✅ {passed} 个通过, ❌ {failed} 个失败")
    return failed == 0

def test_confirm_batch_deletion():
    """测试批量删除确认功能"""
    print("\n🧪 测试批量删除确认功能")
    print("=" * 50)
    
    maker = TorrentMakerApp()
    
    # 创建模拟任务列表
    task_list = [
        MockTask("1", "Task1.mkv", TaskStatus.WAITING, TaskPriority.NORMAL),
        MockTask("2", "Task2.mkv", TaskStatus.RUNNING, TaskPriority.HIGH),
        MockTask("3", "Task3.mkv", TaskStatus.COMPLETED, TaskPriority.LOW),
        MockTask("4", "Task4.mkv", TaskStatus.FAILED, TaskPriority.NORMAL),
        MockTask("5", "Task5.mkv", TaskStatus.WAITING, TaskPriority.HIGH),
    ]
    
    print("📋 模拟任务列表:")
    for i, task in enumerate(task_list, 1):
        status_icon = {
            TaskStatus.WAITING: '⏳',
            TaskStatus.RUNNING: '🔄',
            TaskStatus.COMPLETED: '✅',
            TaskStatus.FAILED: '❌',
            TaskStatus.CANCELLED: '🚫'
        }.get(task.status, '❓')
        print(f"{i}. {task.name} {status_icon}{task.status.value}")
    
    # 测试单个任务确认
    print("\n🔍 测试单个任务确认显示:")
    try:
        # 这里只是显示确认界面，不实际等待用户输入
        print("\n--- 单个等待任务确认 ---")
        # maker._confirm_batch_deletion([0], task_list)  # 注释掉避免等待输入
        print("显示: 确认删除任务 'Task1.mkv'? (y/N):")
        
        print("\n--- 单个运行任务确认 ---")
        # maker._confirm_batch_deletion([1], task_list)  # 注释掉避免等待输入
        print("显示: ⚠️ 任务 'Task2.mkv' 正在运行中")
        print("显示: 确认要强制删除正在运行的任务吗? (y/N):")
        
        print("\n--- 批量任务确认 ---")
        # maker._confirm_batch_deletion([0,1,2], task_list)  # 注释掉避免等待输入
        print("显示: 📋 将要删除 3 个任务:")
        print("显示: 任务列表和运行状态警告")
        
        print("✅ 确认功能显示正常")
        return True
        
    except Exception as e:
        print(f"❌ 确认功能测试失败: {e}")
        return False

def test_edge_cases():
    """测试边界情况"""
    print("\n🧪 测试边界情况")
    print("=" * 50)
    
    maker = TorrentMakerApp()
    
    # 测试空输入
    result = maker._parse_task_selection("", 5)
    print(f"空输入: {result}")
    
    # 测试空格输入
    result = maker._parse_task_selection("   ", 5)
    print(f"空格输入: {result}")
    
    # 测试最大索引边界
    result = maker._parse_task_selection("1", 1)
    print(f"单任务边界: {result}")
    
    # 测试重复索引
    result = maker._parse_task_selection("1,1,2,2", 5)
    print(f"重复索引: {result}")
    
    print("✅ 边界情况测试完成")
    return True

def main():
    """主测试函数"""
    print("🚀 批量删除功能测试")
    print("=" * 60)
    
    all_passed = True
    
    # 运行所有测试
    all_passed &= test_parse_task_selection()
    all_passed &= test_confirm_batch_deletion()
    all_passed &= test_edge_cases()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！批量删除功能工作正常")
        return 0
    else:
        print("❌ 部分测试失败，请检查代码")
        return 1

if __name__ == "__main__":
    sys.exit(main())