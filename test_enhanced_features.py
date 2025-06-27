#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强功能测试脚本
测试新集成的用户体验优化功能
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from torrent_maker import PathCompleter, TorrentProgressMonitor, SearchHistory, SmartSearchSuggester
    print("✅ 所有增强功能模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

def test_path_completer():
    """测试路径补全功能"""
    print("\n🔍 测试路径补全功能...")
    try:
        completer = PathCompleter()
        print("✅ PathCompleter 初始化成功")
        
        # 测试路径历史记录
        test_paths = ["/Users/test", "/Applications", "/System"]
        for path in test_paths:
            completer.add_to_history(path)
        
        recent_paths = completer.get_recent_paths(5)
        print(f"✅ 路径历史记录功能正常，记录数: {len(recent_paths)}")
        
        return True
    except Exception as e:
        print(f"❌ PathCompleter 测试失败: {e}")
        return False

def test_progress_monitor():
    """测试进度监控功能"""
    print("\n📊 测试进度监控功能...")
    try:
        monitor = TorrentProgressMonitor()
        print("✅ TorrentProgressMonitor 初始化成功")
        
        # 测试任务创建和更新
        task_id = "test_task"
        monitor.create_task(task_id, "测试任务", "/test/path")
        monitor.start_task(task_id)
        monitor.update_progress(task_id, progress=50.0, current_step="测试进度更新")
        monitor.complete_task(task_id, success=True)
        print("✅ 进度监控启动/停止功能正常")
        
        return True
    except Exception as e:
        print(f"❌ TorrentProgressMonitor 测试失败: {e}")
        return False

def test_search_history():
    """测试搜索历史功能"""
    print("\n📝 测试搜索历史功能...")
    try:
        # 使用临时目录测试
        temp_dir = os.path.join(os.getcwd(), f'test_history_{os.getpid()}')
        
        try:
            history = SearchHistory(config_dir=temp_dir)
            print("✅ SearchHistory 初始化成功")
            
            # 测试添加搜索记录
            test_queries = ["测试电影1", "测试剧集2", "测试动漫3"]
            for i, query in enumerate(test_queries):
                history.add_search(query, i + 1, 0.5)
            
            # 测试获取搜索记录
            recent = history.get_recent_queries(5)
            popular = history.get_popular_queries(5)
            stats = history.get_statistics()
            
            print(f"✅ 搜索历史功能正常，最近搜索: {len(recent)}, 热门搜索: {len(popular)}")
            print(f"✅ 搜索统计功能正常，总搜索次数: {stats['total_searches']}")
            
            return True
        finally:
            # 清理临时目录
            try:
                if os.path.exists(temp_dir):
                    import shutil
                    shutil.rmtree(temp_dir)
            except OSError:
                pass
                
    except Exception as e:
        print(f"❌ SearchHistory 测试失败: {e}")
        return False

def test_smart_search_suggester():
    """测试智能搜索建议功能"""
    print("\n💡 测试智能搜索建议功能...")
    try:
        # 使用临时目录测试
        temp_dir = os.path.join(os.getcwd(), f'test_suggester_{os.getpid()}')
        
        try:
            history = SearchHistory(config_dir=temp_dir)
            suggester = SmartSearchSuggester(history)
            print("✅ SmartSearchSuggester 初始化成功")
            
            # 添加一些测试数据
            test_queries = ["复仇者联盟", "钢铁侠", "蜘蛛侠", "美国队长"]
            for query in test_queries:
                history.add_search(query, 5, 0.3)
            
            # 测试搜索建议
            suggestions = suggester.get_related_queries("复仇者联盟")
            print(f"✅ 智能搜索建议功能正常，建议数: {len(suggestions)}")
            
            return True
        finally:
            # 清理临时目录
            try:
                if os.path.exists(temp_dir):
                    import shutil
                    shutil.rmtree(temp_dir)
            except OSError:
                pass
                
    except Exception as e:
        print(f"❌ SmartSearchSuggester 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试增强功能模块...")
    print("=" * 50)
    
    tests = [
        ("路径补全", test_path_completer),
        ("进度监控", test_progress_monitor),
        ("搜索历史", test_search_history),
        ("智能建议", test_smart_search_suggester)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有增强功能测试通过！")
        return True
    else:
        print(f"⚠️ {total - passed} 个功能测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)