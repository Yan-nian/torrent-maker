#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
性能基准测试

比较优化前后的性能差异，测试搜索速度、内存使用等指标。

作者：Torrent Maker Team
版本：1.2.0
"""

import os
import sys
import time
import tempfile
import tracemalloc
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from file_matcher import FileMatcher
    from config_manager import ConfigManager
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)


class PerformanceBenchmark:
    """性能基准测试类"""
    
    def __init__(self):
        self.temp_dir = None
        self.test_dirs = []
        
    def setup_test_environment(self, num_dirs: int = 100, files_per_dir: int = 10):
        """
        设置测试环境
        
        Args:
            num_dirs: 创建的目录数量
            files_per_dir: 每个目录中的文件数量
        """
        print(f"创建测试环境: {num_dirs} 个目录，每个目录 {files_per_dir} 个文件")
        
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试目录和文件
        for i in range(num_dirs):
            # 生成多样化的目录名
            dir_names = [
                f"Game of Thrones Season {i % 8 + 1}",
                f"Breaking Bad S{i % 5 + 1:02d}",
                f"The Office US Season {i % 9 + 1}",
                f"Friends 1994 Season {i % 10 + 1}",
                f"Stranger Things S{i % 4 + 1:02d}",
                f"House of Cards Season {i % 6 + 1}",
                f"Narcos S{i % 3 + 1:02d}",
                f"The Crown Season {i % 4 + 1}",
                f"Westworld S{i % 3 + 1:02d}",
                f"Black Mirror Season {i % 5 + 1}"
            ]
            
            dir_name = dir_names[i % len(dir_names)]
            if i >= len(dir_names):
                dir_name += f" Copy {i // len(dir_names)}"
            
            dir_path = os.path.join(self.temp_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            self.test_dirs.append(dir_path)
            
            # 创建视频文件
            for j in range(files_per_dir):
                file_name = f"S{i % 5 + 1:02d}E{j + 1:02d}.mp4"
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'w') as f:
                    f.write(f"test video content {i}-{j}")
        
        print(f"测试环境创建完成: {self.temp_dir}")
    
    def cleanup_test_environment(self):
        """清理测试环境"""
        if self.temp_dir:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            print("测试环境已清理")
    
    def benchmark_search_performance(self):
        """基准测试搜索性能"""
        print("\n" + "="*50)
        print("搜索性能基准测试")
        print("="*50)
        
        # 测试查询
        test_queries = [
            "Game of Thrones",
            "Breaking Bad",
            "Office",
            "Friends",
            "Stranger",
            "House",
            "Narcos",
            "Crown",
            "Westworld",
            "Black Mirror"
        ]
        
        # 测试不同配置
        configs = [
            {"enable_cache": False, "max_workers": 1, "name": "无缓存单线程"},
            {"enable_cache": False, "max_workers": 4, "name": "无缓存多线程"},
            {"enable_cache": True, "max_workers": 1, "name": "有缓存单线程"},
            {"enable_cache": True, "max_workers": 4, "name": "有缓存多线程"},
        ]
        
        results = {}
        
        for config in configs:
            print(f"\n测试配置: {config['name']}")
            
            # 创建文件匹配器
            matcher = FileMatcher(
                self.temp_dir,
                enable_cache=config['enable_cache'],
                max_workers=config['max_workers']
            )
            
            # 预热（如果有缓存）
            if config['enable_cache']:
                matcher.match_folders("warmup")
            
            # 开始性能测试
            tracemalloc.start()
            start_time = time.time()
            
            total_results = 0
            for query in test_queries:
                search_start = time.time()
                matches = matcher.match_folders(query, max_results=5)
                search_time = time.time() - search_start
                total_results += len(matches)
                
                print(f"  查询 '{query}': {len(matches)} 个结果, {search_time:.3f}s")
            
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            total_time = end_time - start_time
            avg_time = total_time / len(test_queries)
            
            results[config['name']] = {
                'total_time': total_time,
                'avg_time': avg_time,
                'total_results': total_results,
                'peak_memory': peak / 1024 / 1024,  # MB
                'current_memory': current / 1024 / 1024  # MB
            }
            
            print(f"  总时间: {total_time:.3f}s")
            print(f"  平均时间: {avg_time:.3f}s")
            print(f"  总结果数: {total_results}")
            print(f"  峰值内存: {peak / 1024 / 1024:.2f} MB")
            print(f"  当前内存: {current / 1024 / 1024:.2f} MB")
        
        # 显示性能对比
        print(f"\n{'='*50}")
        print("性能对比总结")
        print(f"{'='*50}")
        
        print(f"{'配置':<20} {'总时间(s)':<12} {'平均时间(s)':<12} {'峰值内存(MB)':<12}")
        print("-" * 60)
        
        for name, result in results.items():
            print(f"{name:<20} {result['total_time']:<12.3f} {result['avg_time']:<12.3f} {result['peak_memory']:<12.2f}")
        
        return results
    
    def benchmark_config_performance(self):
        """基准测试配置管理性能"""
        print("\n" + "="*50)
        print("配置管理性能基准测试")
        print("="*50)
        
        # 创建临时配置文件
        config_dir = tempfile.mkdtemp()
        settings_path = os.path.join(config_dir, "settings.json")
        trackers_path = os.path.join(config_dir, "trackers.txt")
        
        try:
            # 测试配置加载性能
            tracemalloc.start()
            start_time = time.time()
            
            # 创建多个配置管理器实例
            configs = []
            for i in range(100):
                config = ConfigManager(settings_path, trackers_path)
                configs.append(config)
            
            load_time = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            print(f"创建100个配置管理器实例:")
            print(f"  总时间: {load_time:.3f}s")
            print(f"  平均时间: {load_time/100:.3f}s")
            print(f"  峰值内存: {peak / 1024 / 1024:.2f} MB")
            
            # 测试配置操作性能
            config = configs[0]
            
            # 测试tracker操作
            start_time = time.time()
            for i in range(1000):
                tracker = f"udp://test{i}.tracker.com:8080/announce"
                config.add_tracker(tracker)
            
            add_time = time.time() - start_time
            print(f"\n添加1000个tracker:")
            print(f"  总时间: {add_time:.3f}s")
            print(f"  平均时间: {add_time/1000:.6f}s")
            
            # 测试设置操作
            start_time = time.time()
            for i in range(1000):
                config.set_setting(f"test_key_{i}", f"test_value_{i}")
            
            set_time = time.time() - start_time
            print(f"\n设置1000个配置项:")
            print(f"  总时间: {set_time:.3f}s")
            print(f"  平均时间: {set_time/1000:.6f}s")
            
        finally:
            # 清理
            import shutil
            shutil.rmtree(config_dir, ignore_errors=True)
    
    def run_all_benchmarks(self):
        """运行所有基准测试"""
        print("Torrent Maker 性能基准测试")
        print("="*50)
        
        try:
            # 设置测试环境
            self.setup_test_environment(num_dirs=200, files_per_dir=15)
            
            # 运行搜索性能测试
            search_results = self.benchmark_search_performance()
            
            # 运行配置管理性能测试
            self.benchmark_config_performance()
            
            # 生成性能报告
            self.generate_performance_report(search_results)
            
        finally:
            # 清理测试环境
            self.cleanup_test_environment()
    
    def generate_performance_report(self, search_results):
        """生成性能报告"""
        print(f"\n{'='*50}")
        print("性能优化建议")
        print(f"{'='*50}")
        
        # 分析搜索结果
        if search_results:
            best_config = min(search_results.items(), key=lambda x: x[1]['avg_time'])
            worst_config = max(search_results.items(), key=lambda x: x[1]['avg_time'])
            
            improvement = (worst_config[1]['avg_time'] - best_config[1]['avg_time']) / worst_config[1]['avg_time'] * 100
            
            print(f"最佳配置: {best_config[0]}")
            print(f"  平均搜索时间: {best_config[1]['avg_time']:.3f}s")
            print(f"  峰值内存使用: {best_config[1]['peak_memory']:.2f} MB")
            
            print(f"\n最差配置: {worst_config[0]}")
            print(f"  平均搜索时间: {worst_config[1]['avg_time']:.3f}s")
            print(f"  峰值内存使用: {worst_config[1]['peak_memory']:.2f} MB")
            
            print(f"\n性能提升: {improvement:.1f}%")
            
            # 提供优化建议
            print(f"\n优化建议:")
            if best_config[1]['avg_time'] < 0.1:
                print("✅ 搜索性能良好")
            else:
                print("⚠️  考虑启用缓存和多线程以提升搜索性能")
            
            if best_config[1]['peak_memory'] < 50:
                print("✅ 内存使用合理")
            else:
                print("⚠️  内存使用较高，考虑优化数据结构")


def main():
    """主函数"""
    benchmark = PerformanceBenchmark()
    benchmark.run_all_benchmarks()


if __name__ == '__main__':
    main()
