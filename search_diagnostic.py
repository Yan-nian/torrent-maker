#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
搜索功能诊断工具
检查 Torrent Maker 搜索功能的各个方面
"""

import os
import sys
import time
import traceback
from pathlib import Path

def test_basic_imports():
    """测试基本导入"""
    print("🔍 测试基本导入...")
    try:
        from torrent_maker import FileMatcher, ConfigManager
        print("  ✅ 成功导入 FileMatcher 和 ConfigManager")
        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        traceback.print_exc()
        return False

def test_config_loading():
    """测试配置加载"""
    print("\n⚙️ 测试配置加载...")
    try:
        from torrent_maker import ConfigManager
        config = ConfigManager()
        
        resource_folder = config.get_resource_folder()
        print(f"  📁 资源文件夹: {resource_folder}")
        print(f"  📁 文件夹存在: {os.path.exists(resource_folder)}")
        
        if os.path.exists(resource_folder):
            # 检查文件夹内容
            try:
                items = list(os.listdir(resource_folder))
                print(f"  📊 文件夹内容数量: {len(items)}")
                if len(items) > 0:
                    print(f"  📋 前5个项目: {items[:5]}")
            except PermissionError:
                print("  ⚠️ 无权限访问文件夹")
        
        return True
    except Exception as e:
        print(f"  ❌ 配置加载失败: {e}")
        traceback.print_exc()
        return False

def test_file_matcher_creation():
    """测试文件匹配器创建"""
    print("\n🔧 测试文件匹配器创建...")
    try:
        from torrent_maker import FileMatcher, ConfigManager
        
        config = ConfigManager()
        resource_folder = config.get_resource_folder()
        
        matcher = FileMatcher(
            resource_folder,
            enable_cache=True,
            cache_duration=3600,
            max_workers=2
        )
        print("  ✅ 成功创建 FileMatcher")
        print(f"  📁 基础目录: {matcher.base_directory}")
        print(f"  📊 最小分数: {matcher.min_score}")
        print(f"  👥 最大工作线程: {matcher.max_workers}")
        
        return matcher
    except Exception as e:
        print(f"  ❌ 文件匹配器创建失败: {e}")
        traceback.print_exc()
        return None

def test_folder_scanning(matcher):
    """测试文件夹扫描"""
    print("\n📂 测试文件夹扫描...")
    try:
        start_time = time.time()
        folders = matcher.get_all_folders()
        scan_time = time.time() - start_time
        
        print(f"  ✅ 扫描完成，耗时: {scan_time:.3f}s")
        print(f"  📊 找到文件夹数量: {len(folders)}")
        
        if len(folders) > 0:
            print(f"  📋 前5个文件夹:")
            for i, folder in enumerate(folders[:5]):
                print(f"    {i+1}. {folder}")
        
        return folders
    except Exception as e:
        print(f"  ❌ 文件夹扫描失败: {e}")
        traceback.print_exc()
        return []

def test_search_functionality(matcher, test_queries=None):
    """测试搜索功能"""
    print("\n🔍 测试搜索功能...")
    
    if test_queries is None:
        test_queries = ["test", "movie", "video", "download"]
    
    results = {}
    
    for query in test_queries:
        print(f"\n  🔍 搜索: '{query}'")
        try:
            start_time = time.time()
            matches = matcher.fuzzy_search(query, max_results=5)
            search_time = time.time() - start_time
            
            print(f"    ⏱️ 搜索耗时: {search_time:.3f}s")
            print(f"    📊 找到匹配: {len(matches)}")
            
            if matches:
                print(f"    📋 匹配结果:")
                for i, (path, score) in enumerate(matches[:3]):
                    print(f"      {i+1}. {os.path.basename(path)} (分数: {score:.2f})")
            
            results[query] = {
                'matches': len(matches),
                'time': search_time,
                'success': True
            }
            
        except Exception as e:
            print(f"    ❌ 搜索失败: {e}")
            results[query] = {
                'matches': 0,
                'time': 0,
                'success': False,
                'error': str(e)
            }
    
    return results

def test_match_folders_method(matcher):
    """测试 match_folders 方法"""
    print("\n📋 测试 match_folders 方法...")
    try:
        start_time = time.time()
        results = matcher.match_folders("test")
        match_time = time.time() - start_time
        
        print(f"  ✅ match_folders 完成，耗时: {match_time:.3f}s")
        print(f"  📊 找到结果: {len(results)}")
        
        if results:
            print(f"  📋 结果详情:")
            for i, result in enumerate(results[:3]):
                print(f"    {i+1}. {result['name']}")
                print(f"       匹配度: {result['score']}%")
                print(f"       文件数: {result['file_count']}")
                print(f"       大小: {result['size']}")
        
        return True
    except Exception as e:
        print(f"  ❌ match_folders 失败: {e}")
        traceback.print_exc()
        return False

def test_performance_components(matcher):
    """测试性能组件"""
    print("\n⚡ 测试性能组件...")
    try:
        # 检查性能监控器
        if hasattr(matcher, 'performance_monitor'):
            print("  ✅ 性能监控器存在")
        else:
            print("  ⚠️ 性能监控器不存在")
        
        # 检查缓存
        if hasattr(matcher, 'cache') and matcher.cache:
            print("  ✅ 搜索缓存启用")
        else:
            print("  ⚠️ 搜索缓存未启用")
        
        # 检查智能索引
        if hasattr(matcher, 'smart_index'):
            print("  ✅ 智能索引存在")
        else:
            print("  ⚠️ 智能索引不存在")
        
        # 检查内存管理器
        if hasattr(matcher, 'memory_manager'):
            print("  ✅ 内存管理器存在")
        else:
            print("  ⚠️ 内存管理器不存在")
        
        return True
    except Exception as e:
        print(f"  ❌ 性能组件检查失败: {e}")
        return False

def main():
    """主诊断函数"""
    print("🔍 Torrent Maker 搜索功能诊断")
    print("=" * 50)
    
    # 测试步骤
    tests = [
        ("基本导入", test_basic_imports),
        ("配置加载", test_config_loading),
    ]
    
    # 执行基础测试
    for test_name, test_func in tests:
        if not test_func():
            print(f"\n❌ {test_name} 失败，停止后续测试")
            return False
    
    # 创建文件匹配器
    matcher = test_file_matcher_creation()
    if not matcher:
        print("\n❌ 无法创建文件匹配器，停止测试")
        return False
    
    # 执行高级测试
    folders = test_folder_scanning(matcher)
    test_performance_components(matcher)
    search_results = test_search_functionality(matcher)
    test_match_folders_method(matcher)
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 诊断总结:")
    print(f"  📁 扫描到文件夹: {len(folders)}")
    
    successful_searches = sum(1 for r in search_results.values() if r['success'])
    print(f"  🔍 成功搜索: {successful_searches}/{len(search_results)}")
    
    if successful_searches == len(search_results):
        print("  ✅ 搜索功能正常")
    else:
        print("  ⚠️ 搜索功能存在问题")
        for query, result in search_results.items():
            if not result['success']:
                print(f"    ❌ '{query}': {result.get('error', '未知错误')}")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断诊断")
    except Exception as e:
        print(f"\n❌ 诊断过程中发生错误: {e}")
        traceback.print_exc()
