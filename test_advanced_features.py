#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
高级功能测试
测试从单文件版本移植的高级功能：性能监控、高级配置管理、实时统计显示
"""

import os
import sys
import tempfile
import time
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_performance_monitor():
    """测试性能监控功能"""
    print("🧪 测试性能监控功能...")
    
    try:
        from performance_monitor import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        # 测试计时功能
        monitor.start_timer('test_operation')
        time.sleep(0.1)  # 模拟操作
        duration = monitor.end_timer('test_operation')
        
        assert duration >= 0.1, f"计时不准确，期望>=0.1s，实际{duration}s"
        
        # 测试统计功能
        stats = monitor.get_stats('test_operation')
        assert stats is not None, "应该能获取统计信息"
        assert stats['count'] == 1, f"操作次数应该是1，实际{stats['count']}"
        assert stats['average'] >= 0.1, f"平均时间应该>=0.1s，实际{stats['average']}s"
        
        # 测试多次操作
        for i in range(3):
            monitor.start_timer('batch_test')
            time.sleep(0.05)
            monitor.end_timer('batch_test')
        
        batch_stats = monitor.get_stats('batch_test')
        assert batch_stats['count'] == 3, f"批量操作次数应该是3，实际{batch_stats['count']}"
        
        # 测试摘要
        summary = monitor.get_summary()
        assert summary['total_operations'] >= 4, "总操作数应该>=4"
        
        print("✅ 性能监控功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 性能监控功能测试失败: {e}")
        return False


def test_search_cache():
    """测试搜索缓存功能"""
    print("🧪 测试搜索缓存功能...")
    
    try:
        from performance_monitor import SearchCache
        
        cache = SearchCache(cache_duration=1)  # 1秒缓存
        
        # 测试缓存设置和获取
        cache.set('test_key', 'test_value')
        value = cache.get('test_key')
        assert value == 'test_value', f"缓存值不匹配，期望'test_value'，实际'{value}'"
        
        # 测试缓存过期
        time.sleep(1.1)
        expired_value = cache.get('test_key')
        assert expired_value is None, "过期的缓存应该返回None"
        
        # 测试缓存统计
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        stats = cache.get_stats()
        assert stats['total_items'] == 2, f"缓存项数量应该是2，实际{stats['total_items']}"
        
        # 测试清理过期缓存
        time.sleep(1.1)
        cleaned = cache.cleanup_expired()
        assert cleaned == 2, f"应该清理2个过期项，实际清理{cleaned}个"
        
        print("✅ 搜索缓存功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 搜索缓存功能测试失败: {e}")
        return False


def test_directory_size_cache():
    """测试目录大小缓存功能"""
    print("🧪 测试目录大小缓存功能...")
    
    try:
        from performance_monitor import DirectorySizeCache
        
        cache = DirectorySizeCache(cache_duration=1)
        
        # 创建测试目录
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = Path(temp_dir) / "test_folder"
            test_dir.mkdir()
            
            # 创建测试文件
            test_file = test_dir / "test.txt"
            test_file.write_text("Hello, World!" * 100)  # 约1300字节
            
            # 测试大小计算
            size1 = cache.get_directory_size(test_dir)
            assert size1 > 1000, f"目录大小应该>1000字节，实际{size1}字节"
            
            # 测试缓存命中
            size2 = cache.get_directory_size(test_dir)
            assert size1 == size2, "缓存命中时大小应该相同"
            
            # 测试缓存统计
            stats = cache.get_stats()
            assert stats['total_items'] >= 1, "应该有至少1个缓存项"
            
        print("✅ 目录大小缓存功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 目录大小缓存功能测试失败: {e}")
        return False


def test_statistics_manager():
    """测试统计管理器功能"""
    print("🧪 测试统计管理器功能...")
    
    try:
        from statistics_manager import StatisticsManager
        
        stats_manager = StatisticsManager()
        
        # 测试搜索记录
        stats_manager.record_search(5)
        stats_manager.record_search(3)
        
        session_stats = stats_manager.get_session_stats()
        assert session_stats['total_searches'] == 2, f"搜索次数应该是2，实际{session_stats['total_searches']}"
        
        # 测试种子创建记录
        stats_manager.record_torrent_creation(10, 1024*1024)  # 10个文件，1MB
        stats_manager.record_torrent_creation(5, 512*1024)   # 5个文件，512KB
        
        session_stats = stats_manager.get_session_stats()
        assert session_stats['total_torrents_created'] == 2, "种子创建次数应该是2"
        assert session_stats['total_files_processed'] == 15, "处理文件数应该是15"
        assert session_stats['total_data_processed'] == 1024*1024 + 512*1024, "处理数据量不正确"
        
        # 测试综合统计
        comprehensive = stats_manager.get_comprehensive_stats()
        assert 'session' in comprehensive, "综合统计应该包含会话信息"
        assert 'performance' in comprehensive, "综合统计应该包含性能信息"
        assert 'cache' in comprehensive, "综合统计应该包含缓存信息"
        
        # 测试重置
        stats_manager.reset_session_stats()
        reset_stats = stats_manager.get_session_stats()
        assert reset_stats['total_searches'] == 0, "重置后搜索次数应该是0"
        
        print("✅ 统计管理器功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 统计管理器功能测试失败: {e}")
        return False


def test_advanced_config_manager():
    """测试高级配置管理功能"""
    print("🧪 测试高级配置管理功能...")
    
    try:
        from config_manager import ConfigManager
        
        # 创建临时配置目录
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_path = os.path.join(temp_dir, 'settings.json')
            trackers_path = os.path.join(temp_dir, 'trackers.txt')
            config_manager = ConfigManager(settings_path=settings_path, trackers_path=trackers_path)
            
            # 测试配置状态
            status = config_manager.get_config_status()
            assert isinstance(status, dict), "配置状态应该是字典"
            assert 'settings_file' in status, "状态应该包含设置文件信息"
            
            # 测试配置导出
            export_file = Path(temp_dir) / "exported_config.json"
            success = config_manager.export_config(str(export_file))
            assert success, "配置导出应该成功"
            assert export_file.exists(), "导出文件应该存在"
            
            # 测试配置备份
            if hasattr(config_manager, 'backup_config'):
                backup_success = config_manager.backup_config()
                assert backup_success, "配置备份应该成功"
            
            # 测试配置验证
            if hasattr(config_manager, 'validate_and_repair'):
                repair_report = config_manager.validate_and_repair()
                assert isinstance(repair_report, dict), "修复报告应该是字典"
                assert 'issues_found' in repair_report, "报告应该包含发现的问题"
            
        print("✅ 高级配置管理功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 高级配置管理功能测试失败: {e}")
        return False


def test_file_matcher_integration():
    """测试文件匹配器的性能监控集成"""
    print("🧪 测试文件匹配器性能监控集成...")
    
    try:
        from file_matcher import FileMatcher
        
        # 创建测试目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建测试文件夹
            test_folders = ["复仇者联盟", "钢铁侠", "蜘蛛侠"]
            for folder in test_folders:
                folder_path = Path(temp_dir) / folder
                folder_path.mkdir()
                (folder_path / "test.mkv").touch()
            
            matcher = FileMatcher(temp_dir)
            
            # 验证性能监控器已初始化
            assert hasattr(matcher, 'performance_monitor'), "文件匹配器应该有性能监控器"
            assert hasattr(matcher, 'size_cache'), "文件匹配器应该有大小缓存"
            
            # 执行搜索
            results = matcher.match_folders("复仇者")
            assert len(results) >= 1, "应该找到匹配结果"
            
            # 检查性能统计
            stats = matcher.performance_monitor.get_all_stats()
            assert isinstance(stats, dict), "性能统计应该是字典"
            
        print("✅ 文件匹配器性能监控集成测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 文件匹配器性能监控集成测试失败: {e}")
        return False


def test_torrent_creator_integration():
    """测试种子创建器的性能监控集成"""
    print("🧪 测试种子创建器性能监控集成...")
    
    try:
        from torrent_creator import TorrentCreator
        
        trackers = ["http://test.tracker.com:8080/announce"]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            creator = TorrentCreator(trackers, temp_dir)
            
            # 验证性能监控器已初始化
            assert hasattr(creator, 'performance_monitor'), "种子创建器应该有性能监控器"
            assert hasattr(creator, 'size_cache'), "种子创建器应该有大小缓存"
            
        print("✅ 种子创建器性能监控集成测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 种子创建器性能监控集成测试失败: {e}")
        return False


def run_all_tests():
    """运行所有高级功能测试"""
    print("🚀 开始高级功能移植测试")
    print("=" * 80)
    
    tests = [
        test_performance_monitor,
        test_search_cache,
        test_directory_size_cache,
        test_statistics_manager,
        test_advanced_config_manager,
        test_file_matcher_integration,
        test_torrent_creator_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试 {test.__name__} 异常: {e}")
            failed += 1
        print()
    
    print("=" * 80)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("🎉 所有高级功能移植测试通过！")
        print("✅ 单文件版本的高级功能已成功移植到模块化版本")
        return True
    else:
        print("⚠️ 部分测试失败，请检查相关功能")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
