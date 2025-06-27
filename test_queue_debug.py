#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
队列管理器调试测试脚本
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("开始调试队列管理器...")

try:
    print("1. 导入 queue_manager 模块...")
    from queue_manager import TorrentQueueManager
    print("✅ queue_manager 模块导入成功")
    
    print("2. 导入 TorrentCreator 类...")
    from torrent_maker import TorrentCreator
    print("✅ TorrentCreator 类导入成功")
    
    print("3. 创建 TorrentCreator 实例...")
    creator = TorrentCreator(
        tracker_links=["http://tracker.example.com:8080/announce"],
        output_dir="./output",
        max_workers=2
    )
    print("✅ TorrentCreator 实例创建成功")
    
    print("4. 创建 TorrentQueueManager 实例...")
    queue_manager = TorrentQueueManager(
        creator,
        max_concurrent=2,
        save_file="test_queue.json"
    )
    print("✅ TorrentQueueManager 实例创建成功")
    
    print("5. 测试 set_callbacks 方法...")
    def dummy_callback(*args, **kwargs):
        pass
    
    queue_manager.set_callbacks(
        on_task_start=dummy_callback,
        on_task_complete=dummy_callback,
        on_task_failed=dummy_callback,
        on_progress_update=dummy_callback
    )
    print("✅ set_callbacks 方法调用成功")
    
    print("\n🎉 所有测试通过！队列管理器功能正常。")
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ 其他错误: {e}")
    import traceback
    traceback.print_exc()