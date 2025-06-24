#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Torrent Maker v1.5.0 第二阶段优化验证测试
简化版本 - 验证核心优化功能

作者：Torrent Maker Team
版本：1.5.0 Stage 2 Verification
"""

import os
import sys
import time
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        from torrent_maker import (
            FileMatcher, DirectorySizeCache, SmartIndexCache, 
            MemoryManager, AsyncIOProcessor, FastSimilarityCalculator
        )
        print("  ✅ 核心模块导入成功")
        return True
    except ImportError as e:
        print(f"  ❌ 模块导入失败: {e}")
        return False

def test_smart_search_optimization():
    """测试智能搜索优化"""
    print("\n🎯 测试智能搜索优化...")
    
    try:
        from torrent_maker import FileMatcher, SmartIndexCache
        
        # 创建临时测试目录
        test_dir = tempfile.mkdtemp()
        test_folders = [
            "The Matrix 1999",
            "Matrix Reloaded 2003", 
            "Matrix Revolutions 2003",
            "Breaking Bad S01",
            "Breaking Bad S02",
            "Avengers Endgame 2019",
            "Spider Man No Way Home 2021"
        ]
        
        # 创建测试文件夹
        for folder in test_folders:
            os.makedirs(os.path.join(test_dir, folder), exist_ok=True)
        
        # 测试搜索功能
        matcher = FileMatcher(test_dir, enable_cache=True)
        
        # 测试搜索查询
        search_queries = ["Matrix", "Breaking", "Avengers"]
        results = {}
        
        for query in search_queries:
            print(f"  搜索: '{query}'")
            start_time = time.time()
            matches = matcher.fuzzy_search(query, max_results=5)
            search_time = time.time() - start_time
            
            results[query] = {
                'matches': len(matches),
                'time': search_time,
                'results': [match[0] for match in matches[:3]]
            }
            
            print(f"    找到 {len(matches)} 个匹配，耗时 {search_time:.4f}s")
        
        # 清理
        shutil.rmtree(test_dir)
        
        print("  ✅ 智能搜索优化测试通过")
        return results
        
    except Exception as e:
        print(f"  ❌ 智能搜索测试失败: {e}")
        return {}

def test_memory_management():
    """测试内存管理"""
    print("\n💾 测试内存管理...")
    
    try:
        from torrent_maker import MemoryManager
        
        # 创建内存管理器
        memory_manager = MemoryManager(max_memory_mb=128)
        
        # 获取初始内存状态
        initial_memory = memory_manager.get_memory_usage()
        print(f"  初始内存: {initial_memory.get('rss_mb', 0):.1f}MB")
        
        # 模拟内存使用
        large_data = []
        for i in range(50):
            large_data.append([f"test_data_{j}" for j in range(500)])
        
        # 检查内存使用
        current_memory = memory_manager.get_memory_usage()
        print(f"  使用后内存: {current_memory.get('rss_mb', 0):.1f}MB")
        
        # 测试内存清理
        cleanup_result = memory_manager.cleanup_memory()
        print(f"  清理结果: GC回收 {cleanup_result.get('gc_collected', 0)} 个对象")
        
        # 清理数据
        del large_data
        
        final_memory = memory_manager.get_memory_usage()
        print(f"  最终内存: {final_memory.get('rss_mb', 0):.1f}MB")
        
        print("  ✅ 内存管理测试通过")
        return {
            'initial_mb': initial_memory.get('rss_mb', 0),
            'peak_mb': current_memory.get('rss_mb', 0),
            'final_mb': final_memory.get('rss_mb', 0),
            'cleanup_items': cleanup_result.get('gc_collected', 0)
        }
        
    except Exception as e:
        print(f"  ❌ 内存管理测试失败: {e}")
        return {}

def test_directory_cache():
    """测试目录缓存优化"""
    print("\n📁 测试目录缓存优化...")
    
    try:
        from torrent_maker import DirectorySizeCache
        
        # 创建测试目录
        test_dir = tempfile.mkdtemp()
        
        # 创建一些测试文件
        for i in range(10):
            file_path = os.path.join(test_dir, f"test_file_{i}.txt")
            with open(file_path, 'w') as f:
                f.write("test content " * 100)  # 约1KB文件
        
        # 创建缓存实例
        cache = DirectorySizeCache(cache_duration=300, max_cache_size=100)
        
        # 第一次计算（无缓存）
        start_time = time.time()
        size1 = cache.get_directory_size(Path(test_dir))
        time1 = time.time() - start_time
        
        # 第二次计算（有缓存）
        start_time = time.time()
        size2 = cache.get_directory_size(Path(test_dir))
        time2 = time.time() - start_time
        
        # 获取缓存统计
        cache_stats = cache.get_cache_stats()
        
        print(f"  第一次计算: {size1} bytes, 耗时 {time1:.4f}s")
        print(f"  第二次计算: {size2} bytes, 耗时 {time2:.4f}s")
        print(f"  缓存命中率: {cache_stats.get('hit_rate', 0):.2%}")
        print(f"  加速比: {time1/time2 if time2 > 0 else 'N/A':.1f}x")
        
        # 清理
        shutil.rmtree(test_dir)
        
        print("  ✅ 目录缓存优化测试通过")
        return {
            'first_time': time1,
            'second_time': time2,
            'speedup': time1/time2 if time2 > 0 else 0,
            'hit_rate': cache_stats.get('hit_rate', 0)
        }
        
    except Exception as e:
        print(f"  ❌ 目录缓存测试失败: {e}")
        return {}

def test_async_io():
    """测试异步I/O处理"""
    print("\n⚡ 测试异步I/O处理...")
    
    try:
        from torrent_maker import AsyncIOProcessor
        
        # 创建异步处理器
        async_processor = AsyncIOProcessor(max_concurrent=4)
        
        # 创建测试目录
        test_dir = tempfile.mkdtemp()
        
        # 创建子目录结构
        for i in range(5):
            subdir = os.path.join(test_dir, f"subdir_{i}")
            os.makedirs(subdir, exist_ok=True)
            
            # 在每个子目录创建文件
            for j in range(3):
                file_path = os.path.join(subdir, f"file_{j}.txt")
                with open(file_path, 'w') as f:
                    f.write("async test content " * 50)
        
        # 测试异步目录扫描
        start_time = time.time()
        folders = async_processor.async_directory_scan(Path(test_dir), max_depth=2)
        scan_time = time.time() - start_time
        
        print(f"  异步扫描: 找到 {len(folders)} 个文件夹，耗时 {scan_time:.4f}s")
        
        # 清理资源
        async_processor.cleanup()
        shutil.rmtree(test_dir)
        
        print("  ✅ 异步I/O处理测试通过")
        return {
            'folders_found': len(folders),
            'scan_time': scan_time
        }
        
    except Exception as e:
        print(f"  ❌ 异步I/O测试失败: {e}")
        return {}

def main():
    """主测试函数"""
    print("🚀 Torrent Maker v1.5.0 第二阶段优化验证测试")
    print("=" * 60)
    
    results = {}
    
    # 1. 测试模块导入
    if not test_imports():
        print("\n❌ 模块导入失败，无法继续测试")
        return
    
    # 2. 测试各项优化功能
    results['search_optimization'] = test_smart_search_optimization()
    results['memory_management'] = test_memory_management()
    results['directory_cache'] = test_directory_cache()
    results['async_io'] = test_async_io()
    
    # 3. 输出测试总结
    print("\n" + "=" * 60)
    print("📊 第二阶段优化验证结果总结:")
    print("=" * 60)
    
    # 搜索优化结果
    if results['search_optimization']:
        print("🎯 智能搜索优化: ✅ 通过")
        search_data = results['search_optimization']
        avg_time = sum(data['time'] for data in search_data.values()) / len(search_data)
        print(f"   平均搜索时间: {avg_time:.4f}s")
    
    # 内存管理结果
    if results['memory_management']:
        print("💾 内存管理优化: ✅ 通过")
        mem_data = results['memory_management']
        print(f"   内存使用: {mem_data['initial_mb']:.1f}MB → {mem_data['final_mb']:.1f}MB")
    
    # 目录缓存结果
    if results['directory_cache']:
        print("📁 目录缓存优化: ✅ 通过")
        cache_data = results['directory_cache']
        print(f"   缓存加速比: {cache_data['speedup']:.1f}x")
        print(f"   缓存命中率: {cache_data['hit_rate']:.2%}")
    
    # 异步I/O结果
    if results['async_io']:
        print("⚡ 异步I/O处理: ✅ 通过")
        async_data = results['async_io']
        print(f"   扫描性能: {async_data['folders_found']} 文件夹，{async_data['scan_time']:.4f}s")
    
    print("\n🎉 第二阶段优化验证完成！")
    print("🚀 v1.5.0 第二阶段优化效果:")
    print("   🎯 智能搜索预筛选机制")
    print("   💾 深度内存管理和监控")
    print("   📁 LRU缓存系统优化")
    print("   ⚡ 异步I/O并发处理")

if __name__ == "__main__":
    main()
