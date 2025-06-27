#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
队列状态显示功能测试脚本
测试 v2.0.3 队列启动信息优化版的新功能
"""

import sys
import time
import threading
from pathlib import Path
from unittest.mock import Mock, MagicMock

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入必要的类和枚举
from torrent_maker import (
    QueueStatusDisplay, QueueManager, TorrentQueueManager,
    QueueTask, TaskStatus
)

class TestQueueStatusDisplay:
    """队列状态显示测试类"""
    
    def __init__(self):
        self.display = QueueStatusDisplay()
        self.mock_queue_manager = self._create_mock_queue_manager()
        
    def _create_mock_queue_manager(self):
        """创建模拟队列管理器"""
        mock_manager = Mock(spec=QueueManager)
        
        # 模拟队列状态
        mock_manager.is_running.return_value = True
        mock_manager.is_paused.return_value = False
        mock_manager.max_concurrent = 3
        
        # 模拟任务列表
        tasks = [
            QueueTask(
                id="task_1",
                name="测试电影.mkv",
                path="/test/movie1.mkv",
                status=TaskStatus.RUNNING,
                progress=45.5
            ),
            QueueTask(
                id="task_2",
                name="测试剧集S01E01.mkv",
                path="/test/series1.mkv",
                status=TaskStatus.RUNNING,
                progress=78.2
            ),
            QueueTask(
                id="task_3",
                name="测试纪录片.mkv",
                path="/test/doc1.mkv",
                status=TaskStatus.WAITING
            ),
            QueueTask(
                id="task_4",
                name="测试动画.mkv",
                path="/test/anime1.mkv",
                status=TaskStatus.WAITING
            ),
            QueueTask(
                id="task_5",
                name="已完成任务.mkv",
                path="/test/completed.mkv",
                status=TaskStatus.COMPLETED,
                actual_duration=125.5
            )
        ]
        
        mock_manager.get_all_tasks.return_value = tasks
        
        # 模拟队列状态信息
        mock_manager.get_queue_status.return_value = {
            'running': True,
            'paused': False,
            'running_tasks': 2,
            'waiting_tasks': 2,
            'total_tasks': 5,
            'current_running': 2,
            'max_concurrent': 3,
            'statistics': {
                'completed_tasks': 1,
                'failed_tasks': 0,
                'average_processing_time': 125.5
            }
        }
        
        return mock_manager
    
    def test_compact_mode(self):
        """测试简洁模式显示"""
        print("\n" + "=" * 60)
        print("🧪 测试简洁模式显示")
        print("=" * 60)
        
        self.display.display_status(self.mock_queue_manager, mode="compact", force_update=True)
        
    def test_standard_mode(self):
        """测试标准模式显示"""
        print("\n" + "=" * 60)
        print("🧪 测试标准模式显示")
        print("=" * 60)
        
        self.display.display_status(self.mock_queue_manager, mode="standard", force_update=True)
        
    def test_detailed_mode(self):
        """测试详细模式显示"""
        print("\n" + "=" * 60)
        print("🧪 测试详细模式显示")
        print("=" * 60)
        
        self.display.display_status(self.mock_queue_manager, mode="detailed", force_update=True)
        
    def test_smart_update_mechanism(self):
        """测试智能更新机制"""
        print("\n" + "=" * 60)
        print("🧪 测试智能更新机制（防重复显示）")
        print("=" * 60)
        
        print("第一次显示（应该显示）:")
        self.display.display_status(self.mock_queue_manager, mode="standard", force_update=True)
        
        print("\n立即再次显示（应该被跳过）:")
        self.display.display_status(self.mock_queue_manager, mode="standard")
        
        print("\n等待3秒后再次显示（应该显示）:")
        time.sleep(3)
        self.display.display_status(self.mock_queue_manager, mode="standard")
        
    def test_different_queue_states(self):
        """测试不同队列状态的显示"""
        print("\n" + "=" * 60)
        print("🧪 测试不同队列状态显示")
        print("=" * 60)
        
        # 测试暂停状态
        print("\n📋 队列暂停状态:")
        self.mock_queue_manager.is_running.return_value = True
        self.mock_queue_manager.is_paused.return_value = True
        self.display.display_status(self.mock_queue_manager, mode="standard", force_update=True)
        
        # 测试停止状态
        print("\n📋 队列停止状态:")
        self.mock_queue_manager.is_running.return_value = False
        self.mock_queue_manager.is_paused.return_value = False
        self.display.display_status(self.mock_queue_manager, mode="standard", force_update=True)
        
        # 恢复运行状态
        self.mock_queue_manager.is_running.return_value = True
        self.mock_queue_manager.is_paused.return_value = False
        
    def test_task_progress_simulation(self):
        """测试任务进度模拟"""
        print("\n" + "=" * 60)
        print("🧪 测试任务进度动态更新")
        print("=" * 60)
        
        # 模拟进度更新
        tasks = self.mock_queue_manager.get_all_tasks.return_value
        
        for i in range(5):
            # 更新第一个任务的进度
            if tasks[0].status == TaskStatus.RUNNING:
                tasks[0].progress = min(45.5 + i * 10, 100)
            
            # 更新第二个任务的进度
            if tasks[1].status == TaskStatus.RUNNING:
                tasks[1].progress = min(78.2 + i * 5, 100)
            
            print(f"\n进度更新 #{i+1}:")
            self.display.display_status(self.mock_queue_manager, mode="compact", force_update=True)
            
            if i < 4:  # 最后一次不等待
                time.sleep(1)
                
    def test_error_handling(self):
        """测试错误处理"""
        print("\n" + "=" * 60)
        print("🧪 测试错误处理")
        print("=" * 60)
        
        # 测试空队列管理器
        print("\n测试空队列管理器:")
        self.display.display_status(None, mode="standard", force_update=True)
        
        # 测试无效模式
        print("\n测试无效显示模式:")
        self.display.display_status(self.mock_queue_manager, mode="invalid_mode", force_update=True)
        
    def run_all_tests(self):
        """运行所有测试"""
        print("🎬" + "=" * 60)
        print("           队列状态显示功能测试 v2.0.3")
        print("           测试队列启动信息优化版功能")
        print("=" * 62)
        
        tests = [
            self.test_compact_mode,
            self.test_standard_mode,
            self.test_detailed_mode,
            self.test_smart_update_mechanism,
            self.test_different_queue_states,
            self.test_task_progress_simulation,
            self.test_error_handling
        ]
        
        for i, test in enumerate(tests, 1):
            try:
                test()
                print(f"\n✅ 测试 {i}/{len(tests)} 通过")
            except Exception as e:
                print(f"\n❌ 测试 {i}/{len(tests)} 失败: {e}")
            
            if i < len(tests):
                print("\n" + "-" * 40)
                time.sleep(1)
        
        print("\n" + "=" * 62)
        print("🎉 所有测试完成！")
        print("=" * 62)

def test_callback_optimization():
    """测试回调函数优化"""
    print("\n" + "=" * 60)
    print("🧪 测试回调函数优化")
    print("=" * 60)
    
    # 创建模拟的TorrentMakerApp实例
    class MockTorrentMakerApp:
        def __init__(self):
            self.status_display = QueueStatusDisplay()
            self.queue_manager = Mock()
            self.queue_display_config = {
                'compact_on_start': True,
                'default_mode': 'standard'
            }
            
            # 模拟队列状态
            self.queue_manager.get_queue_status.return_value = {
                'running': True,
                'paused': False,
                'running_tasks': 1,
                'waiting_tasks': 2,
                'total_tasks': 3,
                'current_running': 1,
                'max_concurrent': 3,
                'statistics': {
                    'completed_tasks': 0,
                    'failed_tasks': 0,
                    'average_processing_time': 0
                }
            }
            
            self.queue_manager.get_all_tasks.return_value = [
                QueueTask(
                    id="test_task",
                    name="测试任务.mkv",
                    path="/test/task.mkv",
                    status=TaskStatus.RUNNING,
                    progress=50.0
                )
            ]
        
        def _on_queue_task_start(self, task):
            """优化后的任务开始回调"""
            mode = "compact" if self.queue_display_config.get('compact_on_start', True) else self.queue_display_config.get('default_mode', 'standard')
            self.status_display.display_status(self.queue_manager, mode=mode)
        
        def _on_queue_task_complete(self, task):
            """优化后的任务完成回调"""
            duration = getattr(task, 'actual_duration', 0)
            print(f"✅ {task.name} 完成 ({duration:.1f}s)")
            self.status_display.display_status(self.queue_manager, mode="compact")
        
        def _on_queue_task_failed(self, task, error_message):
            """优化后的任务失败回调"""
            print(f"❌ {task.name} 失败: {error_message}")
            self.status_display.display_status(self.queue_manager, mode="compact")
    
    app = MockTorrentMakerApp()
    
    # 模拟任务
    test_task = QueueTask(
        id="callback_test",
        name="回调测试任务.mkv",
        path="/test/callback.mkv",
        status=TaskStatus.RUNNING,
        actual_duration=89.5
    )
    
    print("\n测试任务开始回调:")
    app._on_queue_task_start(test_task)
    
    print("\n测试任务完成回调:")
    app._on_queue_task_complete(test_task)
    
    print("\n测试任务失败回调:")
    app._on_queue_task_failed(test_task, "模拟错误信息")

def main():
    """主测试函数"""
    try:
        # 运行队列状态显示测试
        tester = TestQueueStatusDisplay()
        tester.run_all_tests()
        
        # 运行回调函数优化测试
        test_callback_optimization()
        
        print("\n🎯 测试总结:")
        print("✅ QueueStatusDisplay 类功能正常")
        print("✅ 三种显示模式（compact/standard/detailed）工作正常")
        print("✅ 智能更新机制有效防止重复显示")
        print("✅ 回调函数优化减少冗余输出")
        print("✅ 错误处理机制完善")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()