#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统计管理模块
提供性能统计、缓存统计和实时统计显示功能
"""

import time
import logging
from typing import Dict, Any, List, Optional
from performance_monitor import PerformanceMonitor, SearchCache, DirectorySizeCache

logger = logging.getLogger(__name__)


class StatisticsManager:
    """统计管理器 - 提供统一的统计信息管理和显示"""

    def __init__(self):
        """初始化统计管理器"""
        self.performance_monitor = PerformanceMonitor()
        self.search_cache = SearchCache()
        self.size_cache = DirectorySizeCache()
        self.session_stats = {
            'session_start_time': time.time(),
            'total_searches': 0,
            'total_torrents_created': 0,
            'total_files_processed': 0,
            'total_data_processed': 0  # 字节
        }

    def record_search(self, results_count: int = 0) -> None:
        """
        记录搜索操作
        
        Args:
            results_count: 搜索结果数量
        """
        self.session_stats['total_searches'] += 1

    def record_torrent_creation(self, file_count: int = 0, data_size: int = 0) -> None:
        """
        记录种子创建操作
        
        Args:
            file_count: 处理的文件数量
            data_size: 处理的数据大小（字节）
        """
        self.session_stats['total_torrents_created'] += 1
        self.session_stats['total_files_processed'] += file_count
        self.session_stats['total_data_processed'] += data_size

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        获取性能统计信息
        
        Returns:
            性能统计信息字典
        """
        return {
            'performance_monitor': self.performance_monitor.get_all_stats(),
            'performance_summary': self.performance_monitor.get_summary()
        }

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息
        
        Returns:
            缓存统计信息字典
        """
        return {
            'search_cache': self.search_cache.get_stats(),
            'size_cache': self.size_cache.get_stats()
        }

    def get_session_stats(self) -> Dict[str, Any]:
        """
        获取会话统计信息
        
        Returns:
            会话统计信息字典
        """
        current_time = time.time()
        session_duration = current_time - self.session_stats['session_start_time']
        
        return {
            'session_duration': session_duration,
            'session_duration_formatted': self._format_duration(session_duration),
            'total_searches': self.session_stats['total_searches'],
            'total_torrents_created': self.session_stats['total_torrents_created'],
            'total_files_processed': self.session_stats['total_files_processed'],
            'total_data_processed': self.session_stats['total_data_processed'],
            'total_data_processed_formatted': self._format_size(self.session_stats['total_data_processed']),
            'searches_per_minute': self.session_stats['total_searches'] / max(session_duration / 60, 1),
            'torrents_per_minute': self.session_stats['total_torrents_created'] / max(session_duration / 60, 1)
        }

    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """
        获取综合统计信息
        
        Returns:
            综合统计信息字典
        """
        return {
            'session': self.get_session_stats(),
            'performance': self.get_performance_stats(),
            'cache': self.get_cache_stats(),
            'timestamp': time.time(),
            'timestamp_formatted': time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def display_performance_stats(self) -> None:
        """显示性能统计信息"""
        print("\n📊 性能统计信息")
        print("=" * 60)
        
        perf_stats = self.get_performance_stats()
        monitor_stats = perf_stats.get('performance_monitor', {})
        summary = perf_stats.get('performance_summary', {})
        
        if summary:
            print("📈 总体性能:")
            print(f"  总操作数: {summary.get('total_operations', 0)}")
            print(f"  总耗时: {summary.get('total_time', 0):.2f}s")
            print(f"  平均操作时间: {summary.get('average_operation_time', 0):.3f}s")
            print(f"  活跃计时器: {summary.get('active_timers', 0)}")
            print(f"  跟踪操作类型: {summary.get('tracked_operations', 0)}")
            print()
        
        if monitor_stats:
            print("🔍 详细性能统计:")
            for operation, stats in monitor_stats.items():
                if stats and isinstance(stats, dict):
                    print(f"  {operation}:")
                    print(f"    执行次数: {stats.get('count', 0)}")
                    print(f"    平均耗时: {stats.get('average', 0):.3f}s")
                    print(f"    最大耗时: {stats.get('max', 0):.3f}s")
                    print(f"    最小耗时: {stats.get('min', 0):.3f}s")
                    print(f"    总耗时: {stats.get('total', 0):.3f}s")
                    print()
        
        print("=" * 60)

    def display_cache_stats(self) -> None:
        """显示缓存统计信息"""
        print("\n💾 缓存统计信息")
        print("=" * 60)
        
        cache_stats = self.get_cache_stats()
        
        # 搜索缓存统计
        search_cache = cache_stats.get('search_cache', {})
        if search_cache:
            print("🔍 搜索缓存:")
            print(f"  总缓存项: {search_cache.get('total_items', 0)}")
            print(f"  有效缓存项: {search_cache.get('valid_items', 0)}")
            print(f"  过期缓存项: {search_cache.get('expired_items', 0)}")
            print(f"  缓存命中率: {search_cache.get('hit_rate', 0):.1%}")
            print(f"  缓存持续时间: {search_cache.get('cache_duration', 0)}s")
            print()
        
        # 大小缓存统计
        size_cache = cache_stats.get('size_cache', {})
        if size_cache:
            print("📏 大小缓存:")
            print(f"  总缓存项: {size_cache.get('total_items', 0)}")
            print(f"  有效缓存项: {size_cache.get('valid_items', 0)}")
            print(f"  过期缓存项: {size_cache.get('expired_items', 0)}")
            print(f"  缓存数据总大小: {self._format_size(size_cache.get('total_cached_size', 0))}")
            print(f"  缓存持续时间: {size_cache.get('cache_duration', 0)}s")
            print()
        
        print("=" * 60)

    def display_session_stats(self) -> None:
        """显示会话统计信息"""
        print("\n🎯 会话统计信息")
        print("=" * 60)
        
        session = self.get_session_stats()
        
        print(f"⏰ 会话时长: {session.get('session_duration_formatted', '0s')}")
        print(f"🔍 总搜索次数: {session.get('total_searches', 0)}")
        print(f"📦 总制种数量: {session.get('total_torrents_created', 0)}")
        print(f"📄 总处理文件: {session.get('total_files_processed', 0)}")
        print(f"💾 总处理数据: {session.get('total_data_processed_formatted', '0 B')}")
        print()
        print(f"📈 搜索频率: {session.get('searches_per_minute', 0):.1f} 次/分钟")
        print(f"📈 制种频率: {session.get('torrents_per_minute', 0):.1f} 个/分钟")
        
        print("=" * 60)

    def display_comprehensive_stats(self) -> None:
        """显示综合统计信息"""
        print("\n📊 综合统计报告")
        print("=" * 80)
        print(f"📅 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # 显示会话统计
        self.display_session_stats()
        
        # 显示性能统计
        self.display_performance_stats()
        
        # 显示缓存统计
        self.display_cache_stats()
        
        print("=" * 80)
        print("📊 统计报告结束")
        print("=" * 80)

    def export_stats(self, export_path: str) -> bool:
        """
        导出统计信息到文件
        
        Args:
            export_path: 导出文件路径
            
        Returns:
            导出成功返回True，否则返回False
        """
        try:
            import json
            from pathlib import Path
            
            stats = self.get_comprehensive_stats()
            
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=4)
            
            logger.info(f"统计信息已导出到: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"导出统计信息失败: {e}")
            return False

    def reset_session_stats(self) -> None:
        """重置会话统计"""
        self.session_stats = {
            'session_start_time': time.time(),
            'total_searches': 0,
            'total_torrents_created': 0,
            'total_files_processed': 0,
            'total_data_processed': 0
        }
        logger.info("会话统计已重置")

    def clear_all_caches(self) -> None:
        """清空所有缓存"""
        self.search_cache.clear()
        self.size_cache.clear_cache()
        logger.info("所有缓存已清空")

    def _format_duration(self, seconds: float) -> str:
        """
        格式化时间持续时间
        
        Args:
            seconds: 秒数
            
        Returns:
            格式化的时间字符串
        """
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"

    def _format_size(self, size_bytes: int) -> str:
        """
        格式化文件大小
        
        Args:
            size_bytes: 字节数
            
        Returns:
            格式化的大小字符串
        """
        if size_bytes == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        size = float(size_bytes)
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.1f} {units[unit_index]}"
