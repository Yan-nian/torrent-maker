#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试队列管理功能是否正常工作
"""

import sys
import os

def test_queue_management():
    """测试队列管理功能"""
    print("开始测试队列管理功能...")
    
    try:
        # 导入主程序
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from torrent_maker import TorrentMakerApp
        print("✅ TorrentMakerApp 导入成功")
        
        # 创建应用实例
        app = TorrentMakerApp()
        print("✅ TorrentMakerApp 实例创建成功")
        
        # 检查队列管理器是否正确初始化
        if app.queue_manager is None:
            print("❌ 队列管理器初始化失败")
            print(f"队列管理器状态: {app.queue_manager}")
            return False
        else:
            print("✅ 队列管理器初始化成功")
            print(f"队列管理器类型: {type(app.queue_manager)}")
            
        # 检查队列管理器的基本方法
        print("\n检查队列管理器方法...")
        methods = ['add_task', 'get_queue_status', 'start_processing', 'stop_processing']
        for method in methods:
            if hasattr(app.queue_manager, method):
                print(f"✅ 方法 {method} 存在")
            else:
                print(f"❌ 方法 {method} 不存在")
                
        # 测试队列状态
        try:
            status = app.queue_manager.get_queue_status()
            print(f"✅ 队列状态获取成功: {status}")
        except Exception as e:
            print(f"❌ 队列状态获取失败: {e}")
            
        return True
                
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_queue_management()
    if success:
        print("\n🎉 队列管理功能测试通过！")
    else:
        print("\n❌ 队列管理功能测试失败！")