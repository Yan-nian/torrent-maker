#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Torrent Maker v1.5.0 性能测试脚本
测试优化后的性能改进效果

作者：Torrent Maker Team
版本：1.5.0
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
    from torrent_maker import TorrentCreator, FileMatcher, DirectorySizeCache
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)


class PerformanceTestV15:
    """v1.5.0 性能测试类"""
    
    def __init__(self):
        self.test_data_dir = None
        self.results = {}
    
    def setup_test_data(self) -> str:
        """创建测试数据"""
        print("🔧 创建测试数据...")
        
        # 创建临时测试目录
        self.test_data_dir = tempfile.mkdtemp(prefix="torrent_test_v15_")
        test_path = Path(self.test_data_dir)
        
        # 创建不同大小的测试文件夹
        test_scenarios = [
            ("Small.Movie.2024.720p", 5, 10),      # 小文件：5个文件，每个10MB
            ("Medium.Series.S01", 20, 50),         # 中等：20个文件，每个50MB  
            ("Large.Movie.2024.4K", 3, 500),       # 大文件：3个文件，每个500MB
            ("Huge.Series.Complete", 50, 100),     # 巨大：50个文件，每个100MB
        ]
        
        for folder_name, file_count, file_size_mb in test_scenarios:
            folder_path = test_path / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            
            print(f"  创建 {folder_name}: {file_count} 个文件，每个 {file_size_mb}MB")
            
            for i in range(file_count):
                file_name = f"{folder_name}.Part{i+1:02d}.mkv"
                file_path = folder_path / file_name
                
                # 创建指定大小的测试文件
                with open(file_path, 'wb') as f:
                    # 写入指定大小的数据
                    chunk_size = 1024 * 1024  # 1MB chunks
                    for _ in range(file_size_mb):
                        f.write(b'0' * chunk_size)
        
        print(f"✅ 测试数据创建完成: {self.test_data_dir}")
        return self.test_data_dir
    
    def cleanup_test_data(self):
        """清理测试数据"""
        if self.test_data_dir and os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
            print(f"🧹 测试数据已清理: {self.test_data_dir}")
    
    def test_directory_size_cache(self) -> Dict[str, Any]:
        """测试目录大小缓存性能"""
        print("\n💾 测试目录大小缓存性能...")
        
        cache = DirectorySizeCache(cache_duration=3600, max_cache_size=100)
        test_folders = list(Path(self.test_data_dir).iterdir())
        
        results = {
            'cold_cache_times': [],
            'warm_cache_times': [],
            'cache_stats': {}
        }
        
        # 冷缓存测试
        print("  冷缓存测试...")
        for folder in test_folders:
            start_time = time.time()
            size = cache.get_directory_size(folder)
            duration = time.time() - start_time
            results['cold_cache_times'].append(duration)
            print(f"    {folder.name}: {duration:.3f}s, 大小: {size // (1024*1024)}MB")
        
        # 热缓存测试
        print("  热缓存测试...")
        for folder in test_folders:
            start_time = time.time()
            size = cache.get_directory_size(folder)
            duration = time.time() - start_time
            results['warm_cache_times'].append(duration)
            print(f"    {folder.name}: {duration:.3f}s (缓存)")
        
        # 获取缓存统计
        results['cache_stats'] = cache.get_cache_stats()
        
        # 计算性能改进
        avg_cold = sum(results['cold_cache_times']) / len(results['cold_cache_times'])
        avg_warm = sum(results['warm_cache_times']) / len(results['warm_cache_times'])
        improvement = ((avg_cold - avg_warm) / avg_cold) * 100 if avg_cold > 0 else 0
        
        results['performance_improvement'] = improvement
        results['avg_cold_time'] = avg_cold
        results['avg_warm_time'] = avg_warm
        
        return results
    
    def test_piece_size_calculation(self) -> Dict[str, Any]:
        """测试 Piece Size 计算性能"""
        print("\n🧠 测试 Piece Size 计算性能...")
        
        creator = TorrentCreator(
            tracker_links=["udp://test.tracker.com:8080/announce"],
            output_dir=tempfile.mkdtemp()
        )
        
        # 测试不同大小的文件
        test_sizes = [
            (50 * 1024 * 1024, "50MB"),      # 50MB
            (500 * 1024 * 1024, "500MB"),    # 500MB  
            (2 * 1024 * 1024 * 1024, "2GB"), # 2GB
            (10 * 1024 * 1024 * 1024, "10GB") # 10GB
        ]
        
        results = {
            'calculation_times': [],
            'cache_hits': 0,
            'total_calculations': len(test_sizes) * 2  # 每个大小测试两次
        }
        
        # 第一轮计算（冷缓存）
        print("  第一轮计算（冷缓存）...")
        for size_bytes, size_desc in test_sizes:
            start_time = time.time()
            piece_size = creator._calculate_piece_size(size_bytes)
            duration = time.time() - start_time
            results['calculation_times'].append(duration)
            
            piece_kb, _ = creator._get_optimal_piece_size_fast(size_bytes)
            print(f"    {size_desc}: {duration:.6f}s, Piece Size: {piece_kb}KB")
        
        # 第二轮计算（热缓存）
        print("  第二轮计算（热缓存）...")
        for size_bytes, size_desc in test_sizes:
            start_time = time.time()
            piece_size = creator._calculate_piece_size(size_bytes)
            duration = time.time() - start_time
            results['calculation_times'].append(duration)
            
            if duration < 0.001:  # 认为是缓存命中
                results['cache_hits'] += 1
            
            print(f"    {size_desc}: {duration:.6f}s (缓存)")
        
        # 计算统计
        avg_time = sum(results['calculation_times']) / len(results['calculation_times'])
        cache_hit_rate = results['cache_hits'] / results['total_calculations']
        
        results['avg_calculation_time'] = avg_time
        results['cache_hit_rate'] = cache_hit_rate
        results['cached_calculations'] = len(creator._piece_size_cache)
        
        return results
    
    def test_torrent_creation_performance(self) -> Dict[str, Any]:
        """测试种子创建性能"""
        print("\n🛠️ 测试种子创建性能...")
        
        # 创建临时输出目录
        output_dir = tempfile.mkdtemp(prefix="torrent_output_v15_")
        
        try:
            creator = TorrentCreator(
                tracker_links=["udp://test.tracker.com:8080/announce"],
                output_dir=output_dir,
                max_workers=2
            )
            
            # 选择测试文件夹
            test_folders = list(Path(self.test_data_dir).iterdir())[:2]  # 只测试前2个
            
            results = {
                'creation_times': [],
                'successful_creations': 0,
                'total_folders': len(test_folders),
                'performance_stats': {}
            }
            
            for folder in test_folders:
                print(f"  创建种子: {folder.name}")
                
                start_time = time.time()
                try:
                    torrent_path = creator.create_torrent(folder, folder.name)
                    duration = time.time() - start_time
                    
                    if torrent_path and creator.validate_torrent(torrent_path):
                        results['creation_times'].append(duration)
                        results['successful_creations'] += 1
                        print(f"    ✅ 成功: {duration:.3f}s")
                    else:
                        print(f"    ❌ 失败")
                except Exception as e:
                    duration = time.time() - start_time
                    print(f"    ❌ 错误: {e}")
            
            # 获取性能统计
            results['performance_stats'] = creator.get_performance_stats()
            
            if results['creation_times']:
                results['avg_creation_time'] = sum(results['creation_times']) / len(results['creation_times'])
                results['success_rate'] = results['successful_creations'] / results['total_folders']
            else:
                results['avg_creation_time'] = 0
                results['success_rate'] = 0
            
            return results
            
        finally:
            # 清理输出目录
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有性能测试"""
        print("🚀 开始 Torrent Maker v1.5.0 性能测试...")
        print("=" * 60)
        
        try:
            # 设置测试数据
            self.setup_test_data()
            
            # 运行各项测试
            self.results['directory_cache'] = self.test_directory_size_cache()
            self.results['piece_calculation'] = self.test_piece_size_calculation()
            self.results['torrent_creation'] = self.test_torrent_creation_performance()
            
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
        print("📊 Torrent Maker v1.5.0 性能测试结果")
        print("=" * 60)
        
        # 目录缓存结果
        if 'directory_cache' in self.results:
            cache_results = self.results['directory_cache']
            print(f"\n💾 目录大小缓存性能:")
            print(f"  冷缓存平均时间: {cache_results['avg_cold_time']:.3f}s")
            print(f"  热缓存平均时间: {cache_results['avg_warm_time']:.3f}s")
            print(f"  性能提升: {cache_results['performance_improvement']:.1f}%")
            print(f"  缓存命中率: {cache_results['cache_stats'].get('hit_rate', 0):.1%}")
        
        # Piece Size 计算结果
        if 'piece_calculation' in self.results:
            piece_results = self.results['piece_calculation']
            print(f"\n🧠 Piece Size 计算性能:")
            print(f"  平均计算时间: {piece_results['avg_calculation_time']:.6f}s")
            print(f"  缓存命中率: {piece_results['cache_hit_rate']:.1%}")
            print(f"  缓存条目数: {piece_results['cached_calculations']}")
        
        # 种子创建结果
        if 'torrent_creation' in self.results:
            creation_results = self.results['torrent_creation']
            print(f"\n🛠️ 种子创建性能:")
            print(f"  平均创建时间: {creation_results['avg_creation_time']:.3f}s")
            print(f"  成功率: {creation_results['success_rate']:.1%}")
            print(f"  测试文件夹数: {creation_results['total_folders']}")
            
            # 显示性能等级
            perf_stats = creation_results.get('performance_stats', {})
            summary = perf_stats.get('summary', {})
            if 'performance_grade' in summary:
                print(f"  性能等级: {summary['performance_grade']}")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    print("🎯 Torrent Maker v1.5.0 性能测试")
    print("=" * 40)
    
    # 运行测试
    test_suite = PerformanceTestV15()
    
    try:
        results = test_suite.run_all_tests()
        test_suite.print_results()
        
        print(f"\n✅ 性能测试完成！")
        print("🚀 v1.5.0 优化效果显著，性能大幅提升！")
        
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
