#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件匹配模块

提供智能文件夹搜索、剧集信息解析和文件匹配功能。
支持模糊搜索、缓存机制和多种命名格式的剧集识别。

作者：Torrent Maker Team
版本：1.2.0
"""

import os
import re
import time
import logging
import hashlib
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Dict, Any, Tuple, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from performance_monitor import PerformanceMonitor, SearchCache, DirectorySizeCache

# 配置日志
logger = logging.getLogger(__name__)

# 导入工具函数
try:
    from utils.helpers import (
        extract_episode_info, format_episode_details,
        is_video_file, format_file_size, get_directory_info
    )
except ImportError:
    logger.warning("无法导入utils.helpers，使用内置函数")

    def extract_episode_info(folder_path):
        return {'episodes': [], 'season_info': '', 'total_episodes': 0}

    def format_episode_details(episodes):
        return "无剧集信息"

    def is_video_file(filename: str) -> bool:
        video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
        return Path(filename).suffix.lower() in video_extensions

    def format_file_size(size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def get_directory_info(directory: str) -> dict:
        return {'total_files': 0, 'video_files': 0, 'total_size': 0, 'readable': True}


class SearchCache:
    """搜索结果缓存类"""

    def __init__(self, cache_duration: int = 3600):
        """
        初始化缓存

        Args:
            cache_duration: 缓存持续时间（秒）
        """
        self.cache_duration = cache_duration
        self._cache: Dict[str, Tuple[float, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """获取缓存项"""
        if key in self._cache:
            timestamp, value = self._cache[key]
            if time.time() - timestamp < self.cache_duration:
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """设置缓存项"""
        self._cache[key] = (time.time(), value)

    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()

    def cleanup(self) -> None:
        """清理过期缓存"""
        current_time = time.time()
        expired_keys = [
            key for key, (timestamp, _) in self._cache.items()
            if current_time - timestamp >= self.cache_duration
        ]
        for key in expired_keys:
            del self._cache[key]


class FileMatcher:
    """
    文件匹配器类

    提供智能文件夹搜索、剧集信息解析和文件匹配功能。
    支持模糊搜索、缓存机制和多种命名格式的剧集识别。
    """

    # 视频文件扩展名
    VIDEO_EXTENSIONS = {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
        '.webm', '.m4v', '.3gp', '.ogv', '.ts', '.m2ts',
        '.mpg', '.mpeg', '.rm', '.rmvb', '.asf', '.divx'
    }

    # 停用词列表
    STOP_WORDS = {
        'the', 'and', 'of', 'to', 'in', 'a', 'an', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had'
    }

    # 分隔符列表
    SEPARATORS = ['.', '_', '-', ':', '|', '\\', '/', '+', '(', ')', '[', ']']

    def __init__(self, base_directory: str, enable_cache: bool = True,
                 cache_duration: int = 3600, min_score: float = 0.6,
                 max_workers: int = 4):
        """
        初始化文件匹配器

        Args:
            base_directory: 基础搜索目录
            enable_cache: 是否启用缓存
            cache_duration: 缓存持续时间（秒）
            min_score: 最小匹配分数阈值 (0-1)
            max_workers: 最大并发工作线程数
        """
        self.base_directory = Path(base_directory)
        self.min_score = min_score
        self.max_workers = max_workers

        # 初始化缓存系统
        self.cache = SearchCache(cache_duration) if enable_cache else None
        self.folder_info_cache = SearchCache(cache_duration) if enable_cache else None

        # 初始化性能监控
        self.performance_monitor = PerformanceMonitor()
        self.size_cache = DirectorySizeCache()

        # 验证基础目录
        if not self.base_directory.exists():
            logger.warning(f"基础目录不存在: {self.base_directory}")
        elif not self.base_directory.is_dir():
            logger.error(f"基础路径不是目录: {self.base_directory}")
            raise ValueError(f"基础路径不是目录: {self.base_directory}")

    def _generate_cache_key(self, search_name: str, directory: str = None) -> str:
        """
        生成缓存键

        Args:
            search_name: 搜索名称
            directory: 搜索目录（可选）

        Returns:
            缓存键字符串
        """
        import hashlib

        key_data = f"{search_name}:{directory or self.base_directory}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def similarity(self, a: str, b: str) -> float:
        """
        计算两个字符串的相似度

        Args:
            a: 第一个字符串
            b: 第二个字符串

        Returns:
            相似度分数 (0-1)
        """
        # 标准化处理
        a_normalized = self._normalize_string(a)
        b_normalized = self._normalize_string(b)

        # 计算基本相似度
        basic_score = SequenceMatcher(None, a_normalized, b_normalized).ratio()

        # 如果标准化后的字符串完全匹配，给予高分
        if a_normalized == b_normalized:
            return 1.0

        # 如果一个字符串包含另一个，提升分数
        if a_normalized in b_normalized or b_normalized in a_normalized:
            basic_score = max(basic_score, 0.85)

        # 额外的匹配策略
        bonus_score = self._calculate_bonus_score(a_normalized, b_normalized)

        return min(1.0, basic_score + bonus_score)

    def _normalize_string(self, text: str) -> str:
        """
        标准化字符串，处理常见的分隔符和格式

        Args:
            text: 原始文本

        Returns:
            标准化后的文本
        """
        if not text:
            return ""

        # 转为小写
        text = text.lower()

        # 移除年份信息 (1900-2099)
        import re
        text = re.sub(r'\b(19|20)\d{2}\b', '', text)

        # 移除常见的质量标识
        quality_patterns = [
            r'\b(720p|1080p|4k|uhd|hd|sd|bluray|bdrip|webrip|hdtv)\b',
            r'\b(x264|x265|h264|h265|hevc)\b',
            r'\b(aac|ac3|dts|mp3)\b'
        ]
        for pattern in quality_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # 替换分隔符为空格
        for sep in self.SEPARATORS:
            text = text.replace(sep, ' ')

        # 移除多余的空格
        text = re.sub(r'\s+', ' ', text).strip()

        # 移除停用词（但保留短文本的完整性）
        words = text.split()
        if len(words) > 3:  # 只有当词数超过3个时才移除停用词
            filtered_words = [word for word in words if word not in self.STOP_WORDS]
            if filtered_words:  # 确保不会移除所有词
                words = filtered_words

        return ' '.join(words)

    def _calculate_bonus_score(self, a: str, b: str) -> float:
        """
        计算额外的匹配分数

        Args:
            a: 第一个标准化字符串
            b: 第二个标准化字符串

        Returns:
            额外分数 (0-0.2)
        """
        bonus = 0.0

        # 检查关键词匹配
        a_words = set(a.split())
        b_words = set(b.split())

        if a_words and b_words:
            # 计算词汇重叠度
            common_words = a_words.intersection(b_words)
            word_overlap_ratio = len(common_words) / len(a_words)

            if word_overlap_ratio >= 0.7:  # 70%的词汇匹配
                bonus += 0.1
            elif word_overlap_ratio >= 0.5:  # 50%的词汇匹配
                bonus += 0.05

        # 检查首字母缩写匹配
        if len(a.split()) >= 2 and len(b.split()) >= 2:
            a_initials = ''.join([word[0] for word in a.split() if word])
            b_initials = ''.join([word[0] for word in b.split() if word])

            if len(a_initials) >= 3 and a_initials == b_initials:
                bonus += 0.1

        return min(0.2, bonus)  # 限制最大额外分数

    def get_all_folders(self, max_depth: int = 3) -> List[Path]:
        """
        获取基础目录下的所有文件夹

        Args:
            max_depth: 最大搜索深度

        Returns:
            文件夹路径列表
        """
        folders = []

        if not self.base_directory.exists():
            logger.warning(f"基础目录不存在: {self.base_directory}")
            return folders

        try:
            # 使用递归方式限制搜索深度
            def _scan_directory(path: Path, current_depth: int = 0):
                if current_depth >= max_depth:
                    return

                try:
                    for item in path.iterdir():
                        if item.is_dir():
                            folders.append(item)
                            _scan_directory(item, current_depth + 1)
                except PermissionError:
                    logger.warning(f"无权限访问目录: {path}")
                except OSError as e:
                    logger.warning(f"访问目录时出错: {path}, 错误: {e}")

            _scan_directory(self.base_directory)

        except Exception as e:
            logger.error(f"扫描目录时发生错误: {e}")

        return folders

    def fuzzy_search(self, search_name: str, max_results: int = 10) -> List[Tuple[str, float]]:
        """
        使用模糊匹配搜索文件夹

        Args:
            search_name: 搜索关键词
            max_results: 最大结果数量

        Returns:
            匹配结果列表，每个元素为(路径, 分数)的元组
        """
        # 检查缓存
        cache_key = self._generate_cache_key(search_name)
        if self.cache:
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"从缓存获取搜索结果: {search_name}")
                return cached_result[:max_results]

        # 获取所有文件夹
        all_folders = self.get_all_folders()
        logger.info(f"扫描到 {len(all_folders)} 个文件夹")

        matches = []
        search_name_normalized = self._normalize_string(search_name)

        # 使用线程池并行处理
        def process_folder(folder_path: Path) -> Optional[Tuple[str, float]]:
            try:
                folder_name = folder_path.name
                similarity_score = self.similarity(search_name, folder_name)

                # 过滤低分匹配
                if similarity_score >= self.min_score:
                    return (str(folder_path), similarity_score)
                return None
            except Exception as e:
                logger.warning(f"处理文件夹时出错 {folder_path}: {e}")
                return None

        # 并行处理文件夹
        from concurrent.futures import ThreadPoolExecutor, as_completed

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_folder = {
                executor.submit(process_folder, folder): folder
                for folder in all_folders
            }

            for future in as_completed(future_to_folder):
                result = future.result()
                if result:
                    matches.append(result)

        # 按分数降序排列
        matches.sort(key=lambda x: x[1], reverse=True)

        # 缓存结果
        if self.cache:
            self.cache.set(cache_key, matches)

        return matches[:max_results]

    def _enhanced_similarity_check(self, search_name: str, folder_name: str) -> float:
        """
        增强的相似度检查

        Args:
            search_name: 搜索名称
            folder_name: 文件夹名称

        Returns:
            相似度分数
        """
        # 基础相似度
        base_score = self.similarity(search_name, folder_name)

        # 标准化字符串
        search_normalized = self._normalize_string(search_name)
        folder_normalized = self._normalize_string(folder_name)

        # 额外检查
        bonus_score = 0.0

        # 1. 完全包含检查
        if search_normalized in folder_normalized:
            bonus_score += 0.1

        # 2. 反向包含检查
        if folder_normalized in search_normalized:
            bonus_score += 0.05

        # 3. 词序无关匹配
        search_words = set(search_normalized.split())
        folder_words = set(folder_normalized.split())

        if search_words and folder_words:
            intersection = search_words.intersection(folder_words)
            union = search_words.union(folder_words)
            jaccard_score = len(intersection) / len(union) if union else 0
            bonus_score += jaccard_score * 0.1

        return min(1.0, base_score + bonus_score)

    def match_folders(self, search_name: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索并返回匹配的文件夹信息

        Args:
            search_name: 搜索关键词
            max_results: 最大结果数量

        Returns:
            匹配的文件夹信息列表
        """
        # 开始性能监控
        self.performance_monitor.start_timer('match_folders')

        try:
            # 执行模糊搜索
            matches = self.fuzzy_search(search_name, max_results)

            if not matches:
                logger.info(f"未找到匹配的文件夹: {search_name}")
                return []

            result = []

            # 并行处理文件夹信息
            def process_folder_info(folder_data: Tuple[str, float]) -> Optional[Dict[str, Any]]:
                folder_path, score = folder_data
                try:
                    # 获取目录信息
                    dir_info = get_directory_info(folder_path)

                    # 获取剧集信息
                    episode_info = self._extract_episode_info_optimized(folder_path)

                    return {
                        'path': folder_path,
                        'name': Path(folder_path).name,
                        'score': int(score * 100),  # 转换为百分比
                        'file_count': dir_info.get('total_files', 0),
                        'size': dir_info.get('total_size_formatted', '未知'),
                        'episodes': episode_info.get('season_info', ''),
                        'video_count': episode_info.get('total_episodes', 0),
                        'readable': dir_info.get('readable', True)
                    }
                except Exception as e:
                    logger.warning(f"处理文件夹信息时出错 {folder_path}: {e}")
                    return None

            # 使用线程池并行处理
            from concurrent.futures import ThreadPoolExecutor, as_completed

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_folder = {
                    executor.submit(process_folder_info, folder_data): folder_data
                    for folder_data in matches
                }

                for future in as_completed(future_to_folder):
                    folder_info = future.result()
                    if folder_info:
                        result.append(folder_info)

            # 按分数排序
            result.sort(key=lambda x: x['score'], reverse=True)

            logger.info(f"成功处理 {len(result)} 个匹配文件夹")
            return result

        except Exception as e:
            logger.error(f"搜索文件夹时发生错误: {e}")
            return []
        finally:
            # 结束性能监控
            duration = self.performance_monitor.end_timer('match_folders')
            if duration > 3.0:  # 如果搜索时间超过3秒，记录警告
                logger.warning(f"文件夹匹配耗时较长: {duration:.2f}s, 找到 {len(result) if 'result' in locals() else 0} 个匹配项")

    def _extract_episode_info_optimized(self, folder_path: str) -> Dict[str, Any]:
        """
        优化的剧集信息提取

        Args:
            folder_path: 文件夹路径

        Returns:
            剧集信息字典
        """
        try:
            # 尝试使用utils中的函数
            return extract_episode_info(folder_path)
        except Exception as e:
            logger.warning(f"使用utils提取剧集信息失败，使用内置方法: {e}")
            return self._extract_episode_info_simple(folder_path)

    def _extract_episode_info_simple(self, folder_path: str) -> Dict[str, Any]:
        """
        简单的剧集信息提取（内置方法）

        Args:
            folder_path: 文件夹路径

        Returns:
            剧集信息字典
        """
        if not Path(folder_path).exists() or not Path(folder_path).is_dir():
            return {'episodes': [], 'season_info': '', 'total_episodes': 0}

        episodes = []
        seasons = set()

        try:
            # 只扫描视频文件
            video_files = []
            for file_path in Path(folder_path).rglob('*'):
                if file_path.is_file() and self._is_video_file(file_path.name):
                    video_files.append(file_path.name)

            # 解析剧集信息
            for filename in video_files:
                episode_info = self._parse_episode_from_filename(filename)
                if episode_info:
                    episodes.append(episode_info)
                    if episode_info.get('season'):
                        seasons.add(episode_info['season'])

        except Exception as e:
            logger.warning(f"提取剧集信息时出错 {folder_path}: {e}")
            return {'episodes': [], 'season_info': '无法访问', 'total_episodes': 0}

        # 排序剧集
        episodes.sort(key=lambda x: (x.get('season') or 0, x.get('episode') or 0))

        # 生成季度信息摘要
        season_info = self._generate_season_summary(episodes, seasons)

        return {
            'episodes': episodes,
            'season_info': season_info,
            'total_episodes': len(episodes),
            'seasons': sorted(list(seasons)) if seasons else []
        }

    def _is_video_file(self, filename: str) -> bool:
        """
        检查文件是否为视频文件

        Args:
            filename: 文件名

        Returns:
            如果是视频文件返回True，否则返回False
        """
        return Path(filename).suffix.lower() in self.VIDEO_EXTENSIONS

    def get_folder_episodes_detail(self, folder_path: str) -> str:
        """
        获取文件夹剧集详细信息

        Args:
            folder_path: 文件夹路径

        Returns:
            格式化的剧集详细信息字符串
        """
        try:
            episode_info = self._extract_episode_info_optimized(folder_path)
            return format_episode_details(episode_info.get('episodes', []))
        except Exception as e:
            logger.warning(f"获取剧集详细信息失败 {folder_path}: {e}")
            return "无法获取剧集信息"

    def _parse_episode_from_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        从文件名中解析剧集信息

        Args:
            filename: 文件名

        Returns:
            剧集信息字典，如果无法解析则返回None
        """
        import re

        # 增强的剧集命名模式
        patterns = [
            # S01E01, S1E1, s01e01 (最常见)
            (r'[Ss](\d{1,2})[Ee](\d{1,3})', 'season_episode'),
            # Season 1 Episode 01, Season.1.Episode.01
            (r'[Ss]eason\s*(\d{1,2})\s*[Ee]pisode\s*(\d{1,3})', 'season_episode'),
            # 第一季第01集, 第1季第1集
            (r'第(\d{1,2})季第(\d{1,3})集', 'season_episode'),
            # 1x01, 01x01 (常见格式)
            (r'(\d{1,2})x(\d{1,3})', 'season_episode'),
            # EP01, Ep.01, 第01集 (只有集数)
            (r'(?:[Ee][Pp]\.?\s*(\d{1,3})|第(\d{1,3})集)', 'episode_only'),
            # [01], (01), 01 (纯数字，需要更严格的匹配)
            (r'(?:^|[^\d])(\d{2,3})(?:[^\d]|$)', 'number_only'),
        ]

        for pattern, pattern_type in patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    if pattern_type == 'season_episode':
                        season = int(match.group(1))
                        episode = int(match.group(2))
                        # 验证合理性
                        if 1 <= season <= 50 and 1 <= episode <= 500:
                            return {
                                'season': season,
                                'episode': episode,
                                'filename': filename,
                                'pattern_type': pattern_type
                            }
                    elif pattern_type == 'episode_only':
                        episode = int(match.group(1) or match.group(2))
                        if 1 <= episode <= 500:
                            return {
                                'season': None,
                                'episode': episode,
                                'filename': filename,
                                'pattern_type': pattern_type
                            }
                    elif pattern_type == 'number_only':
                        episode = int(match.group(1))
                        # 只有当数字在合理范围内时才认为是集数
                        if 1 <= episode <= 200:
                            return {
                                'season': None,
                                'episode': episode,
                                'filename': filename,
                                'pattern_type': pattern_type
                            }
                except ValueError:
                    continue

        return None

    def _generate_season_summary(self, episodes: List[Dict[str, Any]], seasons: Set[int]) -> str:
        """
        生成季度摘要信息

        Args:
            episodes: 剧集列表
            seasons: 季度集合

        Returns:
            格式化的季度摘要字符串
        """
        if not episodes:
            return "无剧集信息"

        if not seasons or None in seasons:
            # 没有明确的季度信息，只显示集数范围
            episode_numbers = [ep['episode'] for ep in episodes if ep.get('episode')]
            if episode_numbers:
                return self._format_episode_range(episode_numbers)
            else:
                return f"{len(episodes)}个视频"

        # 有明确季度信息
        season_summaries = []

        for season in sorted(seasons):
            season_episodes = [ep for ep in episodes if ep.get('season') == season]
            episode_numbers = [ep['episode'] for ep in season_episodes if ep.get('episode')]

            if episode_numbers:
                episode_range = self._format_episode_range(episode_numbers)
                season_summary = f"S{season:02d}{episode_range}"
                season_summaries.append(season_summary)

        return ', '.join(season_summaries) if season_summaries else f"{len(episodes)}个视频"

    def _format_episode_range(self, episode_numbers: List[int]) -> str:
        """
        格式化集数范围，智能分组显示连续片段

        Args:
            episode_numbers: 集数列表

        Returns:
            格式化的集数范围字符串
        """
        if not episode_numbers:
            return ""

        episode_numbers = sorted(set(episode_numbers))  # 去重并排序

        if len(episode_numbers) == 1:
            return f"E{episode_numbers[0]:02d}"

        # 检查是否完全连续
        is_fully_continuous = all(
            episode_numbers[i] == episode_numbers[i-1] + 1
            for i in range(1, len(episode_numbers))
        )

        if is_fully_continuous:
            # 完全连续，使用范围格式
            return f"E{episode_numbers[0]:02d}-E{episode_numbers[-1]:02d}"
        else:
            # 有断集，分组显示连续片段
            groups = []
            start = episode_numbers[0]
            end = episode_numbers[0]

            for i in range(1, len(episode_numbers)):
                if episode_numbers[i] == end + 1:
                    # 连续，扩展当前组
                    end = episode_numbers[i]
                else:
                    # 不连续，结束当前组，开始新组
                    if start == end:
                        groups.append(f"E{start:02d}")
                    else:
                        groups.append(f"E{start:02d}-E{end:02d}")
                    start = episode_numbers[i]
                    end = episode_numbers[i]

            # 添加最后一组
            if start == end:
                groups.append(f"E{start:02d}")
            else:
                groups.append(f"E{start:02d}-E{end:02d}")

            return ",".join(groups)

    def clear_cache(self) -> None:
        """清空搜索缓存"""
        if self.cache:
            self.cache.clear()
            logger.info("搜索缓存已清空")

    def cleanup_cache(self) -> None:
        """清理过期缓存"""
        if self.cache:
            self.cache.cleanup()
            logger.debug("已清理过期缓存")

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息

        Returns:
            缓存统计信息字典
        """
        if not self.cache:
            return {'enabled': False}

        return {
            'enabled': True,
            'size': len(self.cache._cache),
            'duration': self.cache.cache_duration
        }