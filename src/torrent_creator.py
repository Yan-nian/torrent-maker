#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
种子创建模块

提供种子文件创建、验证和管理功能。
支持多种配置选项、进度回调和错误处理。

作者：Torrent Maker Team
版本：1.2.0
"""

import os
import subprocess
import shutil
import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable, Union
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logger = logging.getLogger(__name__)


class TorrentCreationError(Exception):
    """种子创建错误"""
    pass


class TorrentValidationError(Exception):
    """种子验证错误"""
    pass


class TorrentCreator:
    """
    种子创建器类

    提供种子文件创建、验证和管理功能。
    支持多种配置选项、进度回调和错误处理。
    """

    # 默认配置
    DEFAULT_PIECE_SIZE = "auto"  # 自动选择piece大小
    DEFAULT_COMMENT = "Created by Torrent Maker"

    # 支持的piece大小 (KB)
    PIECE_SIZES = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]

    def __init__(self, tracker_links: List[str], output_dir: str = "output",
                 piece_size: Union[str, int] = "auto", private: bool = False,
                 comment: str = None, max_workers: int = 4):
        """
        初始化种子创建器

        Args:
            tracker_links: tracker URL列表
            output_dir: 输出目录
            piece_size: piece大小，可以是"auto"或具体数值(KB)
            private: 是否创建私有种子
            comment: 种子注释
            max_workers: 最大并发工作线程数
        """
        self.tracker_links = list(tracker_links) if tracker_links else []
        self.output_dir = Path(output_dir)
        self.piece_size = piece_size
        self.private = private
        self.comment = comment or self.DEFAULT_COMMENT
        self.max_workers = max_workers

        # 验证tracker列表
        if not self.tracker_links:
            logger.warning("未提供tracker链接")

        # 验证mktorrent可用性
        if not self._check_mktorrent():
            raise TorrentCreationError("系统未安装mktorrent工具")

    def _check_mktorrent(self) -> bool:
        """
        检查系统是否安装了mktorrent

        Returns:
            如果mktorrent可用返回True，否则返回False
        """
        return shutil.which('mktorrent') is not None

    def _ensure_output_dir(self) -> None:
        """
        确保输出目录存在

        Raises:
            TorrentCreationError: 当无法创建输出目录时
        """
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.error(f"创建输出目录失败: {e}")
            raise TorrentCreationError(f"无法创建输出目录: {e}")

    def _calculate_piece_size(self, total_size: int) -> int:
        """
        根据文件总大小自动计算合适的piece大小

        Args:
            total_size: 文件总大小（字节）

        Returns:
            piece大小（KB）
        """
        # 目标：生成的种子文件中piece数量在1000-2000之间
        target_pieces = 1500
        optimal_piece_size = total_size // (target_pieces * 1024)  # 转换为KB

        # 选择最接近的标准piece大小
        for size in self.PIECE_SIZES:
            if size >= optimal_piece_size:
                return size

        # 如果文件太大，使用最大的piece大小
        return self.PIECE_SIZES[-1]

    def _get_directory_size(self, path: Path) -> int:
        """
        计算目录的总大小

        Args:
            path: 目录路径

        Returns:
            总大小（字节）
        """
        total_size = 0
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except (OSError, PermissionError) as e:
            logger.warning(f"计算目录大小时出错: {e}")

        return total_size

    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除不安全的字符

        Args:
            filename: 原始文件名

        Returns:
            清理后的文件名
        """
        import re
        # 移除或替换不安全的字符
        unsafe_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(unsafe_chars, '_', filename)

        # 移除前后空格和点
        sanitized = sanitized.strip(' .')

        # 确保文件名不为空
        if not sanitized:
            sanitized = "torrent"

        return sanitized

    def _build_command(self, source_path: Path, output_file: Path,
                      piece_size: int = None) -> List[str]:
        """
        构建mktorrent命令

        Args:
            source_path: 源文件/目录路径
            output_file: 输出文件路径
            piece_size: piece大小（KB）

        Returns:
            命令参数列表
        """
        command = ['mktorrent']

        # 添加tracker链接
        for tracker in self.tracker_links:
            command.extend(['-a', tracker])

        # 设置输出文件
        command.extend(['-o', str(output_file)])

        # 设置注释
        comment = f"{self.comment} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        command.extend(['-c', comment])

        # 设置piece大小
        if piece_size:
            command.extend(['-l', str(piece_size)])

        # 私有种子标记
        if self.private:
            command.append('-p')

        # 显示详细信息
        command.append('-v')

        # 添加源路径
        command.append(str(source_path))

        return command

    def create_torrent(self, source_path: Union[str, Path],
                      custom_name: str = None,
                      progress_callback: Callable[[str], None] = None) -> Optional[str]:
        """
        创建种子文件

        Args:
            source_path: 源文件或目录路径
            custom_name: 自定义种子名称
            progress_callback: 进度回调函数

        Returns:
            成功时返回种子文件路径，失败时返回None

        Raises:
            TorrentCreationError: 当创建失败时
        """
        try:
            source_path = Path(source_path)

            # 验证源路径
            if not source_path.exists():
                raise TorrentCreationError(f"源路径不存在: {source_path}")

            # 确保输出目录存在
            self._ensure_output_dir()

            # 生成输出文件名
            if custom_name:
                torrent_name = self._sanitize_filename(custom_name)
            else:
                torrent_name = self._sanitize_filename(source_path.name)

            # 添加时间戳避免重名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"{torrent_name}_{timestamp}.torrent"

            # 计算piece大小
            piece_size = None
            if self.piece_size == "auto":
                if source_path.is_dir():
                    total_size = self._get_directory_size(source_path)
                else:
                    total_size = source_path.stat().st_size
                piece_size = self._calculate_piece_size(total_size)
            elif isinstance(self.piece_size, int):
                piece_size = self.piece_size

            # 构建命令
            command = self._build_command(source_path, output_file, piece_size)

            # 记录信息
            logger.info(f"开始创建种子文件")
            logger.info(f"源路径: {source_path}")
            logger.info(f"输出文件: {output_file}")
            logger.info(f"Tracker数量: {len(self.tracker_links)}")
            if piece_size:
                logger.info(f"Piece大小: {piece_size}KB")

            if progress_callback:
                progress_callback(f"正在创建种子文件: {torrent_name}")

            # 执行命令
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=3600  # 1小时超时
            )

            # 验证输出文件
            if not output_file.exists():
                raise TorrentCreationError("种子文件创建失败：输出文件不存在")

            # 记录成功信息
            file_size = output_file.stat().st_size
            logger.info(f"种子文件创建成功: {output_file}")
            logger.info(f"种子文件大小: {file_size} bytes")

            if progress_callback:
                progress_callback(f"种子文件创建成功: {output_file.name}")

            return str(output_file)

        except subprocess.CalledProcessError as e:
            error_msg = f"mktorrent执行失败: {e}"
            if e.stderr:
                error_msg += f"\n错误信息: {e.stderr}"
            logger.error(error_msg)
            raise TorrentCreationError(error_msg)

        except subprocess.TimeoutExpired:
            error_msg = "种子创建超时"
            logger.error(error_msg)
            raise TorrentCreationError(error_msg)

        except Exception as e:
            error_msg = f"创建种子文件时发生未知错误: {e}"
            logger.error(error_msg)
            raise TorrentCreationError(error_msg)

    def create_batch_torrents(self, source_paths: List[Union[str, Path]],
                             progress_callback: Callable[[str, int, int], None] = None) -> List[Optional[str]]:
        """
        批量创建种子文件

        Args:
            source_paths: 源路径列表
            progress_callback: 进度回调函数，参数为(当前文件名, 当前索引, 总数)

        Returns:
            种子文件路径列表，失败的项目为None
        """
        results = []
        total_count = len(source_paths)

        logger.info(f"开始批量创建 {total_count} 个种子文件")

        for i, source_path in enumerate(source_paths, 1):
            try:
                if progress_callback:
                    progress_callback(f"处理: {Path(source_path).name}", i, total_count)

                result = self.create_torrent(source_path)
                results.append(result)

                logger.info(f"批量创建进度: {i}/{total_count}")

            except Exception as e:
                logger.error(f"批量创建失败 {source_path}: {e}")
                results.append(None)

        success_count = sum(1 for r in results if r is not None)
        logger.info(f"批量创建完成: 成功 {success_count}/{total_count}")

        return results

    def validate_torrent(self, torrent_path: Union[str, Path]) -> bool:
        """
        验证种子文件的有效性

        Args:
            torrent_path: 种子文件路径

        Returns:
            如果种子文件有效返回True，否则返回False
        """
        try:
            torrent_path = Path(torrent_path)

            if not torrent_path.exists():
                logger.error(f"种子文件不存在: {torrent_path}")
                return False

            # 简单的文件格式验证
            if not torrent_path.suffix.lower() == '.torrent':
                logger.error(f"文件扩展名不正确: {torrent_path}")
                return False

            # 检查文件大小（种子文件通常不会太大）
            file_size = torrent_path.stat().st_size
            if file_size == 0:
                logger.error(f"种子文件为空: {torrent_path}")
                return False

            if file_size > 10 * 1024 * 1024:  # 10MB
                logger.warning(f"种子文件异常大: {torrent_path} ({file_size} bytes)")

            # 尝试读取文件头部，检查是否为有效的bencoded数据
            try:
                with open(torrent_path, 'rb') as f:
                    header = f.read(10)
                    if not header.startswith(b'd'):
                        logger.error(f"种子文件格式无效: {torrent_path}")
                        return False
            except Exception as e:
                logger.error(f"读取种子文件失败: {e}")
                return False

            logger.info(f"种子文件验证通过: {torrent_path}")
            return True

        except Exception as e:
            logger.error(f"验证种子文件时出错: {e}")
            return False

    def get_torrent_info(self, torrent_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        获取种子文件信息

        Args:
            torrent_path: 种子文件路径

        Returns:
            种子信息字典，失败时返回None
        """
        try:
            torrent_path = Path(torrent_path)

            if not self.validate_torrent(torrent_path):
                return None

            # 使用mktorrent的-s选项显示种子信息
            command = ['mktorrent', '-s', str(torrent_path)]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )

            # 解析输出信息
            info = {
                'file_path': str(torrent_path),
                'file_size': torrent_path.stat().st_size,
                'created_time': datetime.fromtimestamp(torrent_path.stat().st_mtime),
                'raw_info': result.stdout
            }

            return info

        except subprocess.CalledProcessError as e:
            logger.error(f"获取种子信息失败: {e}")
            return None
        except Exception as e:
            logger.error(f"获取种子信息时出错: {e}")
            return None

    def set_output_dir(self, output_dir: Union[str, Path]) -> None:
        """
        设置输出目录

        Args:
            output_dir: 新的输出目录路径
        """
        self.output_dir = Path(output_dir)
        logger.info(f"输出目录已设置为: {self.output_dir}")

    def add_tracker(self, tracker_url: str) -> bool:
        """
        添加新的tracker

        Args:
            tracker_url: tracker URL

        Returns:
            添加成功返回True，否则返回False
        """
        if not tracker_url or not tracker_url.strip():
            logger.error("Tracker URL不能为空")
            return False

        tracker_url = tracker_url.strip()

        if tracker_url not in self.tracker_links:
            self.tracker_links.append(tracker_url)
            logger.info(f"已添加tracker: {tracker_url}")
            return True
        else:
            logger.warning(f"Tracker已存在: {tracker_url}")
            return False

    def remove_tracker(self, tracker_url: str) -> bool:
        """
        移除tracker

        Args:
            tracker_url: 要移除的tracker URL

        Returns:
            移除成功返回True，否则返回False
        """
        if tracker_url in self.tracker_links:
            self.tracker_links.remove(tracker_url)
            logger.info(f"已移除tracker: {tracker_url}")
            return True
        else:
            logger.warning(f"Tracker不存在: {tracker_url}")
            return False

    def get_trackers(self) -> List[str]:
        """
        获取当前的tracker列表

        Returns:
            tracker URL列表的副本
        """
        return self.tracker_links.copy()

    def set_piece_size(self, piece_size: Union[str, int]) -> None:
        """
        设置piece大小

        Args:
            piece_size: piece大小，可以是"auto"或具体数值(KB)
        """
        if piece_size == "auto" or (isinstance(piece_size, int) and piece_size in self.PIECE_SIZES):
            self.piece_size = piece_size
            logger.info(f"Piece大小已设置为: {piece_size}")
        else:
            logger.error(f"无效的piece大小: {piece_size}")
            raise ValueError(f"无效的piece大小: {piece_size}")

    def set_private(self, private: bool) -> None:
        """
        设置是否创建私有种子

        Args:
            private: 是否为私有种子
        """
        self.private = private
        logger.info(f"私有种子标记已设置为: {private}")

    def set_comment(self, comment: str) -> None:
        """
        设置种子注释

        Args:
            comment: 种子注释
        """
        self.comment = comment or self.DEFAULT_COMMENT
        logger.info(f"种子注释已设置为: {self.comment}")

    def get_config(self) -> Dict[str, Any]:
        """
        获取当前配置信息

        Returns:
            配置信息字典
        """
        return {
            'tracker_count': len(self.tracker_links),
            'trackers': self.tracker_links.copy(),
            'output_dir': str(self.output_dir),
            'piece_size': self.piece_size,
            'private': self.private,
            'comment': self.comment,
            'max_workers': self.max_workers,
            'mktorrent_available': self._check_mktorrent()
        }