#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
性能测试脚本 - 测试 Torrent Maker 的性能优化效果
对比优化前后的性能差异

作者：Torrent Maker Team
许可证：MIT
版本：1.3.0
"""

import os
import sys
import time
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any
import subprocess

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from torrent_maker import FileMatcher, TorrentCreator, ConfigManager
    from performance_analyzer import PerformanceAnalyzer, PerformanceProfiler
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)


class PerformanceTestSuite:
    """性能测试套件"""
    
    def __init__(self):
        self.analyzer = PerformanceAnalyzer()
        self.test_data_dir = None
        self.results = {}
    
    def setup_test_data(self) -> str:
        """创建测试数据"""
        print("🔧 创建测试数据...")
        
        # 创建临时测试目录
        self.test_data_dir = tempfile.mkdtemp(prefix="torrent_test_")
        test_path = Path(self.test_data_dir)
        
        # 创建模拟的影视剧文件夹结构
        test_folders = [
            "The.Matrix.1999.1080p.BluRay.x264",
            "Friends.S01.Complete.720p.WEB-DL",
            "Breaking.Bad.S01E01-E07.1080p.HDTV",
            "Game.of.Thrones.S08.Complete.4K.UHD",
            "Stranger.Things.S04.1080p.Netflix.WEB-DL",
            "The.Office.US.Complete.Series.720p",
            "Avengers.Endgame.2019.2160p.BluRay.HEVC",
            "Inception.2010.1080p.BluRay.x265",
            "Interstellar.2014.4K.UHD.BluRay.x265",
            "The.Dark.Knight.2008.1080p.BluRay"
        ]
        
        for folder_name in test_folders:
            folder_path = test_path / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            
            # 创建一些模拟视频文件
            for i in range(1, 6):  # 每个文件夹5个文件
                if "S01" in folder_name or "Complete" in folder_name:
                    # 剧集文件
                    file_name = f"{folder_name}.S01E{i:02d}.mkv"
                else:
                    # 电影文件
                    file_name = f"{folder_name}.Part{i}.mkv"
                
                file_path = folder_path / file_name
                # 创建小文件（1MB）用于测试
                with open(file_path, 'wb') as f:
                    f.write(b'0' * (1024 * 1024))  # 1MB
        
        print(f"✅ 测试数据创建完成: {self.test_data_dir}")
        return self.test_data_dir
    
    def cleanup_test_data(self):
        """清理测试数据"""
        if self.test_data_dir and os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
            print(f"🧹 测试数据已清理: {self.test_data_dir}")
    
    def test_file_search_performance(self) -> Dict[str, Any]:
        """测试文件搜索性能"""
        print("\n🔍 测试文件搜索性能...")
        
        # 创建文件匹配器
        matcher = FileMatcher(
            self.test_data_dir,
            enable_cache=True,
            cache_duration=3600,
            max_workers=4
        )
        
        search_terms = [
            "Matrix",
            "Friends",
            "Breaking Bad",
            "Game of Thrones",
            "Stranger Things",
            "Office",
            "Avengers",
            "Inception",
            "Interstellar",
            "Dark Knight"
        ]
        
        results = {
            'search_times': [],
            'cache_hits': 0,
            'total_searches': len(search_terms) * 2  # 每个搜索词测试两次
        }
        
        # 第一轮搜索（冷缓存）
        print("  第一轮搜索（冷缓存）...")
        for term in search_terms:
            with PerformanceProfiler(self.analyzer, f'search_{term}'):
                start_time = time.time()
                matches = matcher.fuzzy_search(term, max_results=5)
                duration = time.time() - start_time
                results['search_times'].append(duration)
                print(f"    {term}: {duration:.3f}s, 找到 {len(matches)} 个匹配")
        
        # 第二轮搜索（热缓存）
        print("  第二轮搜索（热缓存）...")
        for term in search_terms:
            with PerformanceProfiler(self.analyzer, f'search_cached_{term}'):
                start_time = time.time()
                matches = matcher.fuzzy_search(term, max_results=5)
                duration = time.time() - start_time
                results['search_times'].append(duration)
                if duration < 0.01:  # 认为是缓存命中
                    results['cache_hits'] += 1
                print(f"    {term}: {duration:.3f}s, 找到 {len(matches)} 个匹配")
        
        results['avg_search_time'] = sum(results['search_times']) / len(results['search_times'])
        results['cache_hit_rate'] = results['cache_hits'] / results['total_searches']
        
        return results
    
    def test_torrent_creation_performance(self) -> Dict[str, Any]:
        """测试种子创建性能"""
        print("\n🛠️ 测试种子创建性能...")
        
        # 创建临时输出目录
        output_dir = tempfile.mkdtemp(prefix="torrent_output_")
        
        try:
            # 创建种子创建器
            creator = TorrentCreator(
                tracker_links=["udp://test.tracker.com:8080/announce"],
                output_dir=output_dir,
                max_workers=2
            )
            
            # 选择几个测试文件夹
            test_folders = list(Path(self.test_data_dir).iterdir())[:3]
            
            results = {
                'creation_times': [],
                'total_folders': len(test_folders),
                'successful_creations': 0
            }
            
            for folder in test_folders:
                print(f"  创建种子: {folder.name}")
                
                with PerformanceProfiler(self.analyzer, f'torrent_creation_{folder.name}'):
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
    
    def test_memory_usage(self) -> Dict[str, Any]:
        """测试内存使用情况"""
        print("\n💾 测试内存使用...")
        
        try:
            import psutil
            process = psutil.Process()
            
            # 记录初始内存
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # 执行一些操作
            matcher = FileMatcher(self.test_data_dir, enable_cache=True)
            
            # 执行多次搜索
            for i in range(10):
                matcher.fuzzy_search(f"test_{i}", max_results=5)
            
            # 记录峰值内存
            peak_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            return {
                'initial_memory_mb': initial_memory,
                'peak_memory_mb': peak_memory,
                'memory_increase_mb': peak_memory - initial_memory
            }
            
        except ImportError:
            print("  ⚠️ psutil 未安装，跳过内存测试")
            return {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有性能测试"""
        print("🚀 开始性能测试套件...")
        
        try:
            # 设置测试数据
            self.setup_test_data()
            
            # 运行各项测试
            self.results['search_performance'] = self.test_file_search_performance()
            self.results['torrent_creation_performance'] = self.test_torrent_creation_performance()
            self.results['memory_usage'] = self.test_memory_usage()
            
            # 生成性能报告
            self.results['performance_report'] = self.analyzer.generate_report()
            
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
        print("📊 性能测试结果报告")
        print("=" * 60)
        
        # 搜索性能结果
        if 'search_performance' in self.results:
            search_results = self.results['search_performance']
            print(f"\n🔍 文件搜索性能:")
            print(f"  平均搜索时间: {search_results['avg_search_time']:.3f}s")
            print(f"  缓存命中率: {search_results['cache_hit_rate']:.1%}")
            print(f"  总搜索次数: {search_results['total_searches']}")
        
        # 种子创建性能结果
        if 'torrent_creation_performance' in self.results:
            creation_results = self.results['torrent_creation_performance']
            print(f"\n🛠️ 种子创建性能:")
            print(f"  平均创建时间: {creation_results['avg_creation_time']:.3f}s")
            print(f"  成功率: {creation_results['success_rate']:.1%}")
            print(f"  测试文件夹数: {creation_results['total_folders']}")
        
        # 内存使用结果
        if 'memory_usage' in self.results:
            memory_results = self.results['memory_usage']
            if memory_results:
                print(f"\n💾 内存使用:")
                print(f"  初始内存: {memory_results['initial_memory_mb']:.1f}MB")
                print(f"  峰值内存: {memory_results['peak_memory_mb']:.1f}MB")
                print(f"  内存增长: {memory_results['memory_increase_mb']:.1f}MB")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    print("🎯 Torrent Maker 性能测试")
    print("=" * 40)
    
    # 检查依赖
    try:
        import psutil
        print("✅ psutil 可用，将进行完整测试")
    except ImportError:
        print("⚠️ psutil 未安装，内存测试将被跳过")
        print("安装命令: pip install psutil")
    
    # 运行测试
    test_suite = PerformanceTestSuite()
    
    try:
        results = test_suite.run_all_tests()
        test_suite.print_results()
        
        # 保存详细报告
        report_file = test_suite.analyzer.save_report("performance_test_report.json")
        if report_file:
            print(f"\n📄 详细报告已保存: {report_file}")
        
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
