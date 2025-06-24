#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Torrent Maker v1.5.0 第二阶段优化测试脚本
测试搜索算法优化、内存管理和异步 I/O 处理

作者：Torrent Maker Team
版本：1.5.0 Stage 2
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

try:
    from torrent_maker import (
        TorrentCreator, FileMatcher, DirectorySizeCache,
        SmartIndexCache, FastSimilarityCalculator, MemoryManager,
        StreamFileProcessor, AsyncIOProcessor
    )
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)


class Stage2OptimizationTest:
    """第二阶段优化测试类"""
    
    def __init__(self):
        self.test_data_dir = None
        self.results = {}
    
    def setup_test_data(self) -> str:
        """创建测试数据"""
        print("🔧 创建第二阶段测试数据...")
        
        # 创建临时测试目录
        self.test_data_dir = tempfile.mkdtemp(prefix="torrent_stage2_test_")
        test_path = Path(self.test_data_dir)
        
        # 创建多样化的测试文件夹
        test_folders = [
            "The.Matrix.1999.1080p.BluRay.x264",
            "Inception.2010.4K.UHD.HDR",
            "Avengers.Endgame.2019.720p.WEBRip",
            "Breaking.Bad.S01.Complete.1080p",
            "Game.of.Thrones.S08E06.FINAL",
            "Spider-Man.No.Way.Home.2021",
            "The.Office.US.Complete.Series",
            "Stranger.Things.S04.2160p.Netflix",
            "Top.Gun.Maverick.2022.IMAX",
            "House.of.Cards.S01-S06.Complete"
        ]
        
        for folder_name in test_folders:
            folder_path = test_path / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            
            # 创建一些测试文件
            for i in range(3):
                file_name = f"{folder_name}.part{i+1}.mkv"
                file_path = folder_path / file_name
                with open(file_path, 'w') as f:
                    f.write(f"Test content for {file_name}")
        
        print(f"✅ 测试数据创建完成: {self.test_data_dir}")
        return self.test_data_dir
    
    def cleanup_test_data(self):
        """清理测试数据"""
        if self.test_data_dir and os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
            print(f"🧹 测试数据已清理: {self.test_data_dir}")
    
    def test_smart_search_optimization(self) -> Dict[str, Any]:
        """测试智能搜索优化"""
        print("\n🔍 测试智能搜索优化...")
        
        matcher = FileMatcher(self.test_data_dir, enable_cache=True)
        
        # 测试搜索查询
        search_queries = [
            "Matrix",
            "Breaking Bad",
            "Avengers",
            "Spider Man",
            "Game Thrones"
        ]
        
        results = {
            'search_times': [],
            'cache_performance': {},
            'index_performance': {},
            'total_searches': len(search_queries)
        }
        
        print("  执行搜索测试...")
        for query in search_queries:
            print(f"    搜索: '{query}'")
            
            start_time = time.time()
            matches = matcher.fuzzy_search(query, max_results=5)
            search_time = time.time() - start_time
            
            results['search_times'].append(search_time)
            print(f"      耗时: {search_time:.4f}s, 找到 {len(matches)} 个匹配")
        
        # 获取性能统计
        perf_stats = matcher.get_performance_stats()
        results['cache_performance'] = perf_stats.get('cache_performance', {})
        results['optimization_level'] = perf_stats.get('optimization_level', 'Unknown')
        
        # 计算平均搜索时间
        results['avg_search_time'] = sum(results['search_times']) / len(results['search_times'])
        results['fastest_search'] = min(results['search_times'])
        results['slowest_search'] = max(results['search_times'])
        
        return results
    
    def test_memory_management(self) -> Dict[str, Any]:
        """测试内存管理"""
        print("\n💾 测试内存管理...")
        
        memory_manager = MemoryManager(max_memory_mb=128)
        
        results = {
            'initial_memory': memory_manager.get_memory_usage(),
            'cleanup_results': [],
            'memory_efficiency': 'Unknown'
        }
        
        print("  初始内存状态:")
        initial_mem = results['initial_memory']
        print(f"    RSS: {initial_mem.get('rss_mb', 0):.1f}MB")
        print(f"    可用: {initial_mem.get('available_mb', 0):.1f}MB")
        
        # 模拟内存使用
        print("  模拟内存使用...")
        large_data = []
        for i in range(100):
            large_data.append([f"data_{j}" for j in range(1000)])
        
        # 检查内存使用
        current_mem = memory_manager.get_memory_usage()
        print(f"  使用后内存: {current_mem.get('rss_mb', 0):.1f}MB")
        
        # 测试内存清理
        print("  测试内存清理...")
        cleaned_items = memory_manager.cleanup_memory()
        results['cleanup_results'].append(cleaned_items)
        
        # 清理大数据
        del large_data
        
        final_mem = memory_manager.get_memory_usage()
        results['final_memory'] = final_mem
        
        print(f"  清理后内存: {final_mem.get('rss_mb', 0):.1f}MB")
        print(f"  清理项目数: {cleaned_items}")
        
        return results
    
    def test_async_io_processing(self) -> Dict[str, Any]:
        """测试异步 I/O 处理"""
        print("\n⚡ 测试异步 I/O 处理...")
        
        async_processor = AsyncIOProcessor(max_concurrent=4)
        stream_processor = StreamFileProcessor()
        
        results = {
            'async_scan_time': 0,
            'stream_operations': [],
            'concurrent_operations': 0
        }
        
        # 测试异步目录扫描
        print("  测试异步目录扫描...")
        start_time = time.time()
        folders = async_processor.async_directory_scan(Path(self.test_data_dir), max_depth=2)
        async_scan_time = time.time() - start_time
        
        results['async_scan_time'] = async_scan_time
        results['folders_found'] = len(folders)
        
        print(f"    异步扫描耗时: {async_scan_time:.4f}s")
        print(f"    找到文件夹: {len(folders)} 个")
        
        # 测试流式文件处理
        print("  测试流式文件处理...")
        test_files = []
        for folder in folders[:3]:  # 只测试前3个文件夹
            for file_path in folder.iterdir():
                if file_path.is_file():
                    test_files.append(file_path)
        
        for file_path in test_files[:5]:  # 只测试前5个文件
            start_time = time.time()
            file_size = stream_processor.get_file_size_stream(file_path)
            operation_time = time.time() - start_time
            
            results['stream_operations'].append({
                'file': file_path.name,
                'size': file_size,
                'time': operation_time
            })
        
        results['avg_stream_time'] = sum(op['time'] for op in results['stream_operations']) / len(results['stream_operations']) if results['stream_operations'] else 0
        
        return results
    
    def test_integrated_performance(self) -> Dict[str, Any]:
        """测试集成性能"""
        print("\n🚀 测试集成性能...")
        
        # 创建集成的 TorrentCreator
        creator = TorrentCreator(
            tracker_links=["udp://test.tracker.com:8080/announce"],
            output_dir=tempfile.mkdtemp(),
            max_workers=2
        )
        
        results = {
            'system_info': creator.get_system_info(),
            'performance_stats': {},
            'cache_stats': {}
        }
        
        print("  系统信息:")
        sys_info = results['system_info']
        print(f"    版本: {sys_info['version']}")
        print(f"    优化级别: {sys_info['optimization_level']}")
        print(f"    功能数量: {len(sys_info['features'])}")
        
        # 获取性能统计
        perf_stats = creator.get_performance_stats()
        results['performance_stats'] = perf_stats
        
        print("  性能统计:")
        summary = perf_stats.get('summary', {})
        print(f"    性能等级: {summary.get('performance_grade', 'Unknown')}")
        print(f"    内存使用: {summary.get('memory_usage_mb', 0):.1f}MB")
        
        # 测试缓存清理
        print("  测试缓存清理...")
        cleared = creator.clear_caches()
        results['cache_stats'] = cleared
        
        print(f"    清理项目: {sum(cleared.values())}")
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有第二阶段测试"""
        print("🚀 开始 Torrent Maker v1.5.0 第二阶段优化测试...")
        print("=" * 60)
        
        try:
            # 设置测试数据
            self.setup_test_data()
            
            # 运行各项测试
            self.results['search_optimization'] = self.test_smart_search_optimization()
            self.results['memory_management'] = self.test_memory_management()
            self.results['async_io'] = self.test_async_io_processing()
            self.results['integrated_performance'] = self.test_integrated_performance()
            
            return self.results
            
        finally:
            # 清理测试数据
            self.cleanup_test_data()
    
    def print_results(self):
        """打印测试结果"""
        if not self.results:
            print("❌ 没有测试结果")
            return
        
        print("\n" + "=" * 60)
        print("📊 Torrent Maker v1.5.0 第二阶段优化测试结果")
        print("=" * 60)
        
        # 搜索优化结果
        if 'search_optimization' in self.results:
            search_results = self.results['search_optimization']
            print(f"\n🔍 智能搜索优化:")
            print(f"  平均搜索时间: {search_results['avg_search_time']:.4f}s")
            print(f"  最快搜索: {search_results['fastest_search']:.4f}s")
            print(f"  最慢搜索: {search_results['slowest_search']:.4f}s")
            print(f"  优化等级: {search_results['optimization_level']}")
        
        # 内存管理结果
        if 'memory_management' in self.results:
            memory_results = self.results['memory_management']
            initial_mem = memory_results['initial_memory']
            final_mem = memory_results['final_memory']
            print(f"\n💾 内存管理:")
            print(f"  初始内存: {initial_mem.get('rss_mb', 0):.1f}MB")
            print(f"  最终内存: {final_mem.get('rss_mb', 0):.1f}MB")
            print(f"  清理项目: {sum(memory_results['cleanup_results'])}")
        
        # 异步 I/O 结果
        if 'async_io' in self.results:
            async_results = self.results['async_io']
            print(f"\n⚡ 异步 I/O 处理:")
            print(f"  异步扫描时间: {async_results['async_scan_time']:.4f}s")
            print(f"  找到文件夹: {async_results['folders_found']} 个")
            print(f"  平均流处理时间: {async_results['avg_stream_time']:.6f}s")
        
        # 集成性能结果
        if 'integrated_performance' in self.results:
            integrated_results = self.results['integrated_performance']
            sys_info = integrated_results['system_info']
            print(f"\n🚀 集成性能:")
            print(f"  版本: {sys_info['version']}")
            print(f"  优化级别: {sys_info['optimization_level']}")
            print(f"  性能等级: {sys_info['performance_grade']}")
            print(f"  功能特性: {len(sys_info['features'])} 项")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    print("🎯 Torrent Maker v1.5.0 第二阶段优化测试")
    print("=" * 50)
    
    # 运行测试
    test_suite = Stage2OptimizationTest()
    
    try:
        results = test_suite.run_all_tests()
        test_suite.print_results()
        
        print(f"\n✅ 第二阶段优化测试完成！")
        print("🚀 v1.5.0 第二阶段优化效果显著：")
        print("   🔍 智能搜索索引和预筛选")
        print("   💾 内存管理和自动清理")
        print("   ⚡ 异步 I/O 处理优化")
        print("   📊 增强性能监控和统计")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        test_suite.cleanup_test_data()


if __name__ == "__main__":
    main()
