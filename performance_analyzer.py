#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
性能分析器 - 分析和监控 Torrent Maker 的性能
提供详细的性能报告和优化建议

作者：Torrent Maker Team
许可证：MIT
版本：1.3.0
"""

import os
import sys
import time
import json
import psutil
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class PerformanceMetric:
    """性能指标数据类"""
    name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    memory_start: Optional[float] = None
    memory_end: Optional[float] = None
    memory_peak: Optional[float] = None
    cpu_usage: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class PerformanceAnalyzer:
    """性能分析器"""
    
    def __init__(self, enable_memory_tracking: bool = True, enable_cpu_tracking: bool = True):
        self.enable_memory_tracking = enable_memory_tracking
        self.enable_cpu_tracking = enable_cpu_tracking
        self.metrics: List[PerformanceMetric] = []
        self.active_metrics: Dict[str, PerformanceMetric] = {}
        self.lock = threading.Lock()
        self.process = psutil.Process()
        
    def start_metric(self, name: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """开始记录性能指标"""
        with self.lock:
            current_time = time.time()
            
            metric = PerformanceMetric(
                name=name,
                start_time=current_time,
                metadata=metadata or {}
            )
            
            if self.enable_memory_tracking:
                try:
                    memory_info = self.process.memory_info()
                    metric.memory_start = memory_info.rss / 1024 / 1024  # MB
                except Exception:
                    pass
            
            self.active_metrics[name] = metric
    
    def end_metric(self, name: str) -> Optional[PerformanceMetric]:
        """结束记录性能指标"""
        with self.lock:
            if name not in self.active_metrics:
                return None
            
            metric = self.active_metrics.pop(name)
            current_time = time.time()
            
            metric.end_time = current_time
            metric.duration = current_time - metric.start_time
            
            if self.enable_memory_tracking:
                try:
                    memory_info = self.process.memory_info()
                    metric.memory_end = memory_info.rss / 1024 / 1024  # MB
                except Exception:
                    pass
            
            if self.enable_cpu_tracking:
                try:
                    metric.cpu_usage = self.process.cpu_percent()
                except Exception:
                    pass
            
            self.metrics.append(metric)
            return metric
    
    def get_metrics_by_name(self, name: str) -> List[PerformanceMetric]:
        """获取指定名称的所有指标"""
        return [m for m in self.metrics if m.name == name]
    
    def get_summary_stats(self, name: str) -> Dict[str, Any]:
        """获取指定指标的统计摘要"""
        metrics = self.get_metrics_by_name(name)
        if not metrics:
            return {}
        
        durations = [m.duration for m in metrics if m.duration is not None]
        memory_usage = [m.memory_end - m.memory_start for m in metrics 
                       if m.memory_start is not None and m.memory_end is not None]
        
        stats = {
            'count': len(metrics),
            'total_duration': sum(durations),
            'avg_duration': sum(durations) / len(durations) if durations else 0,
            'min_duration': min(durations) if durations else 0,
            'max_duration': max(durations) if durations else 0,
        }
        
        if memory_usage:
            stats.update({
                'avg_memory_delta': sum(memory_usage) / len(memory_usage),
                'max_memory_delta': max(memory_usage),
                'min_memory_delta': min(memory_usage)
            })
        
        return stats
    
    def generate_report(self) -> Dict[str, Any]:
        """生成性能报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_metrics': len(self.metrics),
            'metric_names': list(set(m.name for m in self.metrics)),
            'summary': {},
            'recommendations': []
        }
        
        # 为每个指标名称生成统计
        for name in report['metric_names']:
            report['summary'][name] = self.get_summary_stats(name)
        
        # 生成优化建议
        report['recommendations'] = self._generate_recommendations(report['summary'])
        
        return report
    
    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """生成性能优化建议"""
        recommendations = []
        
        # 检查种子创建性能
        if 'total_torrent_creation' in summary:
            stats = summary['total_torrent_creation']
            avg_duration = stats.get('avg_duration', 0)
            
            if avg_duration > 30:  # 超过30秒
                recommendations.append(
                    f"种子创建平均耗时 {avg_duration:.1f}s 较长，建议："
                    "1. 检查磁盘I/O性能；2. 考虑使用SSD存储；3. 减少文件数量"
                )
        
        # 检查目录扫描性能
        if 'folder_scanning' in summary:
            stats = summary['folder_scanning']
            avg_duration = stats.get('avg_duration', 0)
            
            if avg_duration > 5:  # 超过5秒
                recommendations.append(
                    f"文件夹扫描平均耗时 {avg_duration:.1f}s 较长，建议："
                    "1. 减少扫描深度；2. 使用更快的存储设备；3. 启用缓存"
                )
        
        # 检查搜索性能
        if 'fuzzy_search' in summary:
            stats = summary['fuzzy_search']
            avg_duration = stats.get('avg_duration', 0)
            
            if avg_duration > 2:  # 超过2秒
                recommendations.append(
                    f"模糊搜索平均耗时 {avg_duration:.1f}s 较长，建议："
                    "1. 增加缓存时间；2. 减少搜索范围；3. 优化搜索算法"
                )
        
        # 检查内存使用
        for name, stats in summary.items():
            if 'avg_memory_delta' in stats:
                memory_delta = stats['avg_memory_delta']
                if memory_delta > 100:  # 超过100MB
                    recommendations.append(
                        f"{name} 操作平均内存增长 {memory_delta:.1f}MB，建议优化内存使用"
                    )
        
        if not recommendations:
            recommendations.append("性能表现良好，无需特别优化")
        
        return recommendations
    
    def save_report(self, filename: str = None) -> str:
        """保存性能报告到文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
        
        report = self.generate_report()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            return filename
        except Exception as e:
            print(f"❌ 保存性能报告失败: {e}")
            return ""
    
    def print_report(self) -> None:
        """打印性能报告到控制台"""
        report = self.generate_report()
        
        print("\n" + "=" * 60)
        print("📊 性能分析报告")
        print("=" * 60)
        print(f"生成时间: {report['timestamp']}")
        print(f"总指标数: {report['total_metrics']}")
        print()
        
        print("📈 性能统计:")
        for name, stats in report['summary'].items():
            print(f"\n🔹 {name}:")
            print(f"  执行次数: {stats['count']}")
            print(f"  平均耗时: {stats['avg_duration']:.3f}s")
            print(f"  最大耗时: {stats['max_duration']:.3f}s")
            print(f"  总耗时: {stats['total_duration']:.3f}s")
            
            if 'avg_memory_delta' in stats:
                print(f"  平均内存变化: {stats['avg_memory_delta']:.1f}MB")
        
        print("\n💡 优化建议:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print("=" * 60)
    
    def clear_metrics(self) -> None:
        """清除所有指标数据"""
        with self.lock:
            self.metrics.clear()
            self.active_metrics.clear()


class PerformanceProfiler:
    """性能分析器上下文管理器"""
    
    def __init__(self, analyzer: PerformanceAnalyzer, metric_name: str, 
                 metadata: Optional[Dict[str, Any]] = None):
        self.analyzer = analyzer
        self.metric_name = metric_name
        self.metadata = metadata
    
    def __enter__(self):
        self.analyzer.start_metric(self.metric_name, self.metadata)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.analyzer.end_metric(self.metric_name)


def benchmark_torrent_creation(torrent_maker_path: str = "torrent_maker.py") -> None:
    """对种子创建进行基准测试"""
    print("🚀 开始种子创建性能基准测试...")
    
    analyzer = PerformanceAnalyzer()
    
    # 这里可以添加实际的基准测试代码
    # 例如创建测试文件夹，运行种子创建等
    
    print("📊 基准测试完成")
    analyzer.print_report()


def main():
    """主函数 - 命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Torrent Maker 性能分析器")
    parser.add_argument("--benchmark", action="store_true", help="运行基准测试")
    parser.add_argument("--report", metavar="FILE", help="生成性能报告文件")
    
    args = parser.parse_args()
    
    if args.benchmark:
        benchmark_torrent_creation()
    elif args.report:
        analyzer = PerformanceAnalyzer()
        # 这里可以加载历史数据或运行测试
        filename = analyzer.save_report(args.report)
        if filename:
            print(f"✅ 性能报告已保存: {filename}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
