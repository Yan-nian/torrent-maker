#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
性能监控系统
提供性能计时、统计分析和缓存管理功能
"""

import os
import time
import threading
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from statistics import mean

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """性能监控类 - 提供计时和统计功能"""

    def __init__(self):
        self._timers: Dict[str, float] = {}
        self._stats: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def start_timer(self, name: str) -> None:
        """
        开始计时
        
        Args:
            name: 计时器名称
        """
        with self._lock:
            self._timers[name] = time.time()

    def end_timer(self, name: str) -> float:
        """
        结束计时并记录统计
        
        Args:
            name: 计时器名称
            
        Returns:
            本次计时的持续时间（秒）
        """
        with self._lock:
            if name in self._timers:
                duration = time.time() - self._timers[name]
                if name not in self._stats:
                    self._stats[name] = []
                self._stats[name].append(duration)
                del self._timers[name]
                return duration
            return 0.0

    def get_stats(self, name: str) -> Optional[Dict[str, float]]:
        """
        获取指定计时器的统计信息
        
        Args:
            name: 计时器名称
            
        Returns:
            统计信息字典，包含count、total、average、min、max
        """
        with self._lock:
            if name not in self._stats or not self._stats[name]:
                return None
            
            times = self._stats[name]
            return {
                'count': len(times),
                'total': sum(times),
                'average': mean(times),
                'min': min(times),
                'max': max(times)
            }

    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """
        获取所有计时器的统计信息
        
        Returns:
            所有统计信息的字典
        """
        with self._lock:
            result = {}
            for name in self._stats:
                stats = self.get_stats(name)
                if stats:
                    result[name] = stats
            return result

    def clear_stats(self, name: str = None) -> None:
        """
        清除统计信息
        
        Args:
            name: 要清除的计时器名称，None表示清除所有
        """
        with self._lock:
            if name is None:
                self._stats.clear()
                self._timers.clear()
            else:
                if name in self._stats:
                    del self._stats[name]
                if name in self._timers:
                    del self._timers[name]

    def get_summary(self) -> Dict[str, Any]:
        """
        获取性能监控摘要
        
        Returns:
            性能摘要信息
        """
        with self._lock:
            total_operations = sum(len(times) for times in self._stats.values())
            total_time = sum(sum(times) for times in self._stats.values())
            
            return {
                'total_operations': total_operations,
                'total_time': total_time,
                'average_operation_time': total_time / total_operations if total_operations > 0 else 0,
                'active_timers': len(self._timers),
                'tracked_operations': len(self._stats)
            }


class SearchCache:
    """搜索结果缓存类 - 提供智能缓存管理"""

    def __init__(self, cache_duration: int = 3600):
        """
        初始化搜索缓存
        
        Args:
            cache_duration: 缓存持续时间（秒）
        """
        self.cache_duration = cache_duration
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存的值，如果不存在或已过期则返回None
        """
        with self._lock:
            if key in self._cache:
                timestamp, value = self._cache[key]
                if time.time() - timestamp < self.cache_duration:
                    return value
                else:
                    del self._cache[key]
            return None

    def set(self, key: str, value: Any) -> None:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 要缓存的值
        """
        with self._lock:
            self._cache[key] = (time.time(), value)

    def clear(self) -> None:
        """清空所有缓存"""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> int:
        """
        清理过期的缓存项
        
        Returns:
            清理的缓存项数量
        """
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, (timestamp, _) in self._cache.items()
                if current_time - timestamp >= self.cache_duration
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)

    def get_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息
        
        Returns:
            缓存统计信息字典
        """
        with self._lock:
            total_items = len(self._cache)
            current_time = time.time()
            expired_items = sum(1 for timestamp, _ in self._cache.values()
                              if current_time - timestamp >= self.cache_duration)
            
            return {
                'total_items': total_items,
                'valid_items': total_items - expired_items,
                'expired_items': expired_items,
                'cache_duration': self.cache_duration,
                'hit_rate': getattr(self, '_hit_count', 0) / max(getattr(self, '_access_count', 1), 1)
            }

    def get_hit_rate(self) -> float:
        """
        获取缓存命中率
        
        Returns:
            缓存命中率（0-1之间的浮点数）
        """
        hit_count = getattr(self, '_hit_count', 0)
        access_count = getattr(self, '_access_count', 0)
        return hit_count / max(access_count, 1)


class DirectorySizeCache:
    """目录大小缓存类 - 优化大目录的大小计算"""

    def __init__(self, cache_duration: int = 1800):  # 30分钟缓存
        """
        初始化目录大小缓存
        
        Args:
            cache_duration: 缓存持续时间（秒）
        """
        self.cache_duration = cache_duration
        self._cache: Dict[str, Tuple[float, int, float]] = {}  # path -> (timestamp, size, mtime)
        self._lock = threading.Lock()

    def get_directory_size(self, path: Path) -> int:
        """
        获取目录大小，使用缓存优化
        
        Args:
            path: 目录路径
            
        Returns:
            目录大小（字节）
        """
        path_str = str(path)
        current_time = time.time()

        try:
            # 获取目录的修改时间
            dir_mtime = path.stat().st_mtime
        except (OSError, PermissionError):
            return self._calculate_size_fallback(path)

        with self._lock:
            # 检查缓存
            if path_str in self._cache:
                timestamp, cached_size, cached_mtime = self._cache[path_str]
                # 如果缓存未过期且目录未修改，返回缓存值
                if (current_time - timestamp < self.cache_duration and
                    abs(dir_mtime - cached_mtime) < 1.0):  # 1秒容差
                    return cached_size

        # 计算目录大小
        total_size = self._calculate_size_optimized(path)

        # 更新缓存
        with self._lock:
            self._cache[path_str] = (current_time, total_size, dir_mtime)

        return total_size

    def _calculate_size_optimized(self, path: Path) -> int:
        """
        优化的目录大小计算方法
        
        Args:
            path: 目录路径
            
        Returns:
            目录大小（字节）
        """
        total_size = 0
        
        try:
            # 使用 os.scandir 替代 rglob，性能更好
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                    except (OSError, IOError):
                        # 忽略无法访问的文件
                        continue
        except (OSError, PermissionError):
            return self._calculate_size_fallback(path)
        
        return total_size

    def _calculate_size_fallback(self, path: Path) -> int:
        """
        备用的目录大小计算方法
        
        Args:
            path: 目录路径
            
        Returns:
            目录大小（字节）
        """
        try:
            total_size = 0
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    try:
                        total_size += file_path.stat().st_size
                    except (OSError, IOError):
                        continue
            return total_size
        except Exception:
            logger.warning(f"无法计算目录大小: {path}")
            return 0

    def clear_cache(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> int:
        """
        清理过期的缓存项
        
        Returns:
            清理的缓存项数量
        """
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, (timestamp, _, _) in self._cache.items()
                if current_time - timestamp >= self.cache_duration
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)

    def get_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息
        
        Returns:
            缓存统计信息字典
        """
        with self._lock:
            total_items = len(self._cache)
            current_time = time.time()
            expired_items = sum(1 for timestamp, _, _ in self._cache.values()
                              if current_time - timestamp >= self.cache_duration)
            
            total_cached_size = sum(size for _, size, _ in self._cache.values())
            
            return {
                'total_items': total_items,
                'valid_items': total_items - expired_items,
                'expired_items': expired_items,
                'total_cached_size': total_cached_size,
                'cache_duration': self.cache_duration
            }
