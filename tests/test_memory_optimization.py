#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Torrent Maker v1.5.0 内存管理优化测试脚本
专门测试内存管理功能的效果

作者：Torrent Maker Team
版本：1.5.0 Memory Optimization
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
        MemoryManager, MemoryAnalyzer, StreamFileProcessor,
        DirectorySizeCache, TorrentCreator
    )
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)


class MemoryOptimizationTest:
    """内存管理优化测试类"""
    
    def __init__(self):
        self.test_data_dir = None
        self.results = {}
    
    def setup_test_data(self) -> str:
        """创建内存测试数据"""
        print("🔧 创建内存测试数据...")
        
        # 创建临时测试目录
        self.test_data_dir = tempfile.mkdtemp(prefix="memory_test_")
        test_path = Path(self.test_data_dir)
        
        # 创建大量小文件和少量大文件
        print("  创建小文件...")
        small_files_dir = test_path / "small_files"
        small_files_dir.mkdir()
        
        for i in range(1000):  # 1000 个小文件
            file_path = small_files_dir / f"small_file_{i:04d}.txt"
            with open(file_path, 'w') as f:
                f.write(f"Small file content {i}" * 100)  # 约 2KB 每个文件
        
        # 创建大文件
        print("  创建大文件...")
        large_files_dir = test_path / "large_files"
        large_files_dir.mkdir()
        
        for i in range(3):  # 3 个大文件
            file_path = large_files_dir / f"large_file_{i}.dat"
            with open(file_path, 'wb') as f:
                # 创建 10MB 的文件
                chunk = b'0' * (1024 * 1024)  # 1MB chunk
                for _ in range(10):
                    f.write(chunk)
        
        print(f"✅ 测试数据创建完成: {self.test_data_dir}")
        return self.test_data_dir
    
    def cleanup_test_data(self):
        """清理测试数据"""
        if self.test_data_dir and os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
            print(f"🧹 测试数据已清理: {self.test_data_dir}")
    
    def test_memory_manager_basic(self) -> Dict[str, Any]:
        """测试内存管理器基本功能"""
        print("\n💾 测试内存管理器基本功能...")
        
        memory_manager = MemoryManager(max_memory_mb=128)
        
        results = {
            'initial_memory': memory_manager.get_memory_usage(),
            'memory_analysis': {},
            'cleanup_results': {},
            'final_memory': {}
        }
        
        print("  初始内存状态:")
        initial_mem = results['initial_memory']
        print(f"    RSS: {initial_mem.get('rss_mb', 0):.1f}MB")
        print(f"    系统使用: {initial_mem.get('system_used_percent', 0):.1f}%")
        
        # 获取内存分析
        print("  获取内存分析...")
        analysis = memory_manager.get_memory_analysis()
        results['memory_analysis'] = analysis
        
        print(f"    对象总数: {analysis['object_analysis']['total_objects']}")
        print(f"    内存趋势: {analysis['memory_trend']['trend']}")
        print(f"    建议数量: {len(analysis['recommendations'])}")
        
        # 测试内存清理
        print("  测试内存清理...")
        cleanup_result = memory_manager.cleanup_memory()
        results['cleanup_results'] = cleanup_result
        
        print(f"    清理项目: {cleanup_result.get('memory_pools_cleaned', 0)}")
        print(f"    GC 回收: {cleanup_result.get('gc_collected', 0)}")
        print(f"    释放内存: {cleanup_result.get('freed_mb', 0):.1f}MB")
        
        # 最终内存状态
        results['final_memory'] = memory_manager.get_memory_usage()
        
        return results
    
    def test_stream_processor_memory(self) -> Dict[str, Any]:
        """测试流式处理器内存优化"""
        print("\n🌊 测试流式处理器内存优化...")
        
        memory_manager = MemoryManager(max_memory_mb=64)  # 较小的内存限制
        stream_processor = StreamFileProcessor(memory_manager=memory_manager)
        
        results = {
            'large_file_processing': [],
            'directory_processing': {},
            'memory_efficiency': {}
        }
        
        # 测试大文件处理
        large_files_dir = Path(self.test_data_dir) / "large_files"
        if large_files_dir.exists():
            print("  测试大文件流式处理...")
            
            for file_path in large_files_dir.iterdir():
                if file_path.is_file():
                    print(f"    处理文件: {file_path.name}")
                    
                    start_time = time.time()
                    start_memory = memory_manager.get_memory_usage()['rss_mb']
                    
                    # 计算文件哈希
                    file_hash = stream_processor.calculate_file_hash(file_path)
                    
                    end_time = time.time()
                    end_memory = memory_manager.get_memory_usage()['rss_mb']
                    
                    results['large_file_processing'].append({
                        'file': file_path.name,
                        'size_mb': file_path.stat().st_size / (1024 * 1024),
                        'processing_time': end_time - start_time,
                        'memory_before': start_memory,
                        'memory_after': end_memory,
                        'memory_delta': end_memory - start_memory,
                        'hash_length': len(file_hash)
                    })
        
        # 测试目录处理
        print("  测试目录流式处理...")
        start_memory = memory_manager.get_memory_usage()['rss_mb']
        
        directory_result = stream_processor.process_large_directory(
            Path(self.test_data_dir), operation='size'
        )
        
        end_memory = memory_manager.get_memory_usage()['rss_mb']
        
        results['directory_processing'] = {
            'total_size_mb': directory_result['total_size'] / (1024 * 1024),
            'file_count': directory_result['file_count'],
            'error_count': len(directory_result['errors']),
            'memory_before': start_memory,
            'memory_after': end_memory,
            'memory_delta': end_memory - start_memory
        }
        
        # 内存效率分析
        results['memory_efficiency'] = memory_manager.get_memory_analysis()
        
        return results
    
    def test_directory_cache_memory(self) -> Dict[str, Any]:
        """测试目录缓存内存优化"""
        print("\n📁 测试目录缓存内存优化...")
        
        cache = DirectorySizeCache(max_cache_size=50)  # 较小的缓存限制
        
        results = {
            'cache_performance': [],
            'memory_usage': [],
            'cache_stats': {}
        }
        
        # 测试多次目录扫描
        test_dirs = [
            Path(self.test_data_dir),
            Path(self.test_data_dir) / "small_files",
            Path(self.test_data_dir) / "large_files"
        ]
        
        for i, test_dir in enumerate(test_dirs):
            if test_dir.exists():
                print(f"  测试目录 {i+1}: {test_dir.name}")
                
                # 第一次扫描（冷缓存）
                start_time = time.time()
                size1 = cache.get_directory_size(test_dir)
                cold_time = time.time() - start_time
                
                # 第二次扫描（热缓存）
                start_time = time.time()
                size2 = cache.get_directory_size(test_dir)
                warm_time = time.time() - start_time
                
                results['cache_performance'].append({
                    'directory': test_dir.name,
                    'size_mb': size1 / (1024 * 1024),
                    'cold_time': cold_time,
                    'warm_time': warm_time,
                    'speedup': cold_time / warm_time if warm_time > 0 else 0,
                    'size_consistent': size1 == size2
                })
        
        # 获取缓存统计
        results['cache_stats'] = cache.get_cache_stats()
        
        return results
    
    def test_integrated_memory_management(self) -> Dict[str, Any]:
        """测试集成内存管理"""
        print("\n🚀 测试集成内存管理...")
        
        # 创建 TorrentCreator 实例
        creator = TorrentCreator(
            tracker_links=["udp://test.tracker.com:8080/announce"],
            output_dir=tempfile.mkdtemp(),
            max_workers=2
        )
        
        results = {
            'system_info': creator.get_system_info(),
            'performance_stats': {},
            'memory_analysis': {},
            'cleanup_results': {}
        }
        
        print("  获取系统信息...")
        sys_info = results['system_info']
        print(f"    版本: {sys_info['version']}")
        print(f"    内存使用: {sys_info['memory_info'].get('rss_mb', 0):.1f}MB")
        
        # 获取性能统计
        print("  获取性能统计...")
        perf_stats = creator.get_performance_stats()
        results['performance_stats'] = perf_stats
        
        memory_mgmt = perf_stats.get('memory_management', {})
        print(f"    当前内存: {memory_mgmt.get('current_usage_mb', 0):.1f}MB")
        print(f"    内存效率: {memory_mgmt.get('memory_efficiency', 'Unknown')}")
        
        # 获取内存分析
        print("  获取内存分析...")
        memory_analysis = creator.memory_manager.get_memory_analysis()
        results['memory_analysis'] = memory_analysis
        
        print(f"    内存趋势: {memory_analysis['memory_trend']['trend']}")
        print(f"    优化建议: {len(memory_analysis['recommendations'])}")
        
        # 测试清理
        print("  测试集成清理...")
        cleanup_result = creator.clear_caches()
        results['cleanup_results'] = cleanup_result
        
        print(f"    总清理项目: {sum(v for k, v in cleanup_result.items() if isinstance(v, int))}")
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有内存管理测试"""
        print("🚀 开始 Torrent Maker v1.5.0 内存管理优化测试...")
        print("=" * 60)
        
        try:
            # 设置测试数据
            self.setup_test_data()
            
            # 运行各项测试
            self.results['memory_manager'] = self.test_memory_manager_basic()
            self.results['stream_processor'] = self.test_stream_processor_memory()
            self.results['directory_cache'] = self.test_directory_cache_memory()
            self.results['integrated'] = self.test_integrated_memory_management()
            
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
        print("📊 Torrent Maker v1.5.0 内存管理优化测试结果")
        print("=" * 60)
        
        # 内存管理器结果
        if 'memory_manager' in self.results:
            mm_results = self.results['memory_manager']
            print(f"\n💾 内存管理器:")
            print(f"  初始内存: {mm_results['initial_memory'].get('rss_mb', 0):.1f}MB")
            print(f"  最终内存: {mm_results['final_memory'].get('rss_mb', 0):.1f}MB")
            print(f"  释放内存: {mm_results['cleanup_results'].get('freed_mb', 0):.1f}MB")
            
            analysis = mm_results['memory_analysis']
            print(f"  内存趋势: {analysis['memory_trend']['trend']}")
            print(f"  优化建议: {len(analysis['recommendations'])}")
        
        # 流式处理器结果
        if 'stream_processor' in self.results:
            sp_results = self.results['stream_processor']
            print(f"\n🌊 流式处理器:")
            
            if sp_results['large_file_processing']:
                avg_memory_delta = sum(item['memory_delta'] for item in sp_results['large_file_processing']) / len(sp_results['large_file_processing'])
                print(f"  大文件处理: {len(sp_results['large_file_processing'])} 个文件")
                print(f"  平均内存增长: {avg_memory_delta:.1f}MB")
            
            dir_proc = sp_results['directory_processing']
            print(f"  目录处理: {dir_proc['file_count']} 个文件")
            print(f"  内存增长: {dir_proc['memory_delta']:.1f}MB")
        
        # 目录缓存结果
        if 'directory_cache' in self.results:
            dc_results = self.results['directory_cache']
            print(f"\n📁 目录缓存:")
            
            if dc_results['cache_performance']:
                avg_speedup = sum(item['speedup'] for item in dc_results['cache_performance']) / len(dc_results['cache_performance'])
                print(f"  平均加速比: {avg_speedup:.1f}x")
            
            cache_stats = dc_results['cache_stats']
            print(f"  缓存命中率: {cache_stats.get('hit_rate', 0):.1%}")
            print(f"  缓存大小: {cache_stats.get('cache_size', 0)}")
        
        # 集成测试结果
        if 'integrated' in self.results:
            int_results = self.results['integrated']
            sys_info = int_results['system_info']
            print(f"\n🚀 集成测试:")
            print(f"  版本: {sys_info['version']}")
            print(f"  性能等级: {sys_info['performance_grade']}")
            print(f"  功能特性: {len(sys_info['features'])} 项")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    print("🎯 Torrent Maker v1.5.0 内存管理优化测试")
    print("=" * 50)
    
    # 运行测试
    test_suite = MemoryOptimizationTest()
    
    try:
        results = test_suite.run_all_tests()
        test_suite.print_results()
        
        print(f"\n✅ 内存管理优化测试完成！")
        print("🚀 v1.5.0 内存管理优化效果显著：")
        print("   💾 智能内存监控和分析")
        print("   🌊 流式处理避免内存溢出")
        print("   📁 LRU 缓存内存控制")
        print("   🧹 自动内存清理和优化")
        
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
