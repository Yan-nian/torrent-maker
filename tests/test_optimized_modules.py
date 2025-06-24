#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
优化模块测试

测试改进后的配置管理器、文件匹配器和种子创建器的功能。

作者：Torrent Maker Team
版本：1.2.0
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from config_manager import ConfigManager, ConfigValidationError
    from file_matcher import FileMatcher, SearchCache
    from torrent_creator import TorrentCreator, TorrentCreationError
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)


class TestConfigManager(unittest.TestCase):
    """配置管理器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.settings_path = os.path.join(self.temp_dir, "settings.json")
        self.trackers_path = os.path.join(self.temp_dir, "trackers.txt")
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_config_manager_initialization(self):
        """测试配置管理器初始化"""
        config = ConfigManager(self.settings_path, self.trackers_path)
        
        # 检查配置文件是否创建
        self.assertTrue(os.path.exists(self.settings_path))
        self.assertTrue(os.path.exists(self.trackers_path))
        
        # 检查默认设置
        self.assertIn('resource_folder', config.settings)
        self.assertIn('output_folder', config.settings)
        self.assertTrue(len(config.trackers) > 0)
    
    def test_setting_operations(self):
        """测试设置操作"""
        config = ConfigManager(self.settings_path, self.trackers_path)
        
        # 测试设置资源文件夹
        test_path = self.temp_dir
        result = config.set_resource_folder(test_path)
        self.assertTrue(result)
        self.assertEqual(config.get_resource_folder(), os.path.abspath(test_path))
        
        # 测试设置输出文件夹
        output_path = os.path.join(self.temp_dir, "output")
        result = config.set_output_folder(output_path)
        self.assertTrue(result)
        self.assertEqual(config.get_output_folder(), os.path.abspath(output_path))
    
    def test_tracker_operations(self):
        """测试tracker操作"""
        config = ConfigManager(self.settings_path, self.trackers_path)
        
        # 测试添加tracker
        test_tracker = "udp://test.tracker.com:8080/announce"
        result = config.add_tracker(test_tracker)
        self.assertTrue(result)
        self.assertIn(test_tracker, config.get_trackers())
        
        # 测试重复添加
        result = config.add_tracker(test_tracker)
        self.assertFalse(result)
        
        # 测试移除tracker
        result = config.remove_tracker(test_tracker)
        self.assertTrue(result)
        self.assertNotIn(test_tracker, config.get_trackers())
    
    def test_config_validation(self):
        """测试配置验证"""
        config = ConfigManager(self.settings_path, self.trackers_path)
        
        # 测试无效设置
        invalid_settings = {'file_search_tolerance': 150}  # 超出范围
        result = config.update_settings(invalid_settings)
        self.assertTrue(result)  # 应该自动修正
        
        # 验证设置被修正
        self.assertEqual(config.get_setting('file_search_tolerance'), 60)  # 默认值


class TestSearchCache(unittest.TestCase):
    """搜索缓存测试"""
    
    def test_cache_operations(self):
        """测试缓存操作"""
        cache = SearchCache(cache_duration=1)
        
        # 测试设置和获取
        cache.set("test_key", "test_value")
        self.assertEqual(cache.get("test_key"), "test_value")
        
        # 测试过期
        import time
        time.sleep(1.1)
        self.assertIsNone(cache.get("test_key"))
        
        # 测试清空
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))


class TestFileMatcher(unittest.TestCase):
    """文件匹配器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试目录结构
        test_dirs = [
            "Game of Thrones Season 1",
            "Breaking Bad S01",
            "The Office US S01E01-E09",
            "Friends 1994"
        ]
        
        for dir_name in test_dirs:
            dir_path = os.path.join(self.temp_dir, dir_name)
            os.makedirs(dir_path)
            
            # 创建一些测试文件
            for i in range(1, 4):
                file_path = os.path.join(dir_path, f"episode_{i:02d}.mp4")
                with open(file_path, 'w') as f:
                    f.write("test video content")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_file_matcher_initialization(self):
        """测试文件匹配器初始化"""
        matcher = FileMatcher(self.temp_dir)
        self.assertEqual(matcher.base_directory, Path(self.temp_dir))
        self.assertIsNotNone(matcher.cache)
    
    def test_string_normalization(self):
        """测试字符串标准化"""
        matcher = FileMatcher(self.temp_dir)
        
        test_cases = [
            ("Game.of.Thrones.S01E01", "game thrones s01e01"),
            ("Breaking_Bad-2008", "breaking bad"),
            ("The Office (US)", "the office us"),  # 修正期望结果
        ]
        
        for input_str, expected in test_cases:
            result = matcher._normalize_string(input_str)
            self.assertEqual(result, expected)
    
    def test_similarity_calculation(self):
        """测试相似度计算"""
        matcher = FileMatcher(self.temp_dir)
        
        # 测试完全匹配
        self.assertEqual(matcher.similarity("test", "test"), 1.0)
        
        # 测试部分匹配
        score = matcher.similarity("Game of Thrones", "Game.of.Thrones.S01")
        self.assertGreater(score, 0.8)
        
        # 测试不匹配
        score = matcher.similarity("Game of Thrones", "Breaking Bad")
        self.assertLess(score, 0.5)
    
    @patch('file_matcher.get_directory_info')
    def test_folder_matching(self, mock_get_dir_info):
        """测试文件夹匹配"""
        # 模拟目录信息
        mock_get_dir_info.return_value = {
            'total_files': 10,
            'video_files': 3,
            'total_size': 1024*1024*100,  # 100MB
            'total_size_formatted': '100.0 MB',
            'readable': True
        }
        
        matcher = FileMatcher(self.temp_dir, enable_cache=False)
        
        # 测试搜索
        results = matcher.match_folders("Game of Thrones")
        self.assertGreater(len(results), 0)
        
        # 检查结果格式
        for result in results:
            self.assertIn('path', result)
            self.assertIn('name', result)
            self.assertIn('score', result)
            self.assertIn('file_count', result)
            self.assertIn('size', result)


class TestTorrentCreator(unittest.TestCase):
    """种子创建器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.trackers = [
            "udp://tracker.test.com:8080/announce",
            "udp://backup.tracker.com:8080/announce"
        ]
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_torrent_creator_initialization(self):
        """测试种子创建器初始化"""
        with patch('torrent_creator.shutil.which', return_value='/usr/bin/mktorrent'):
            creator = TorrentCreator(self.trackers, self.temp_dir)
            self.assertEqual(creator.tracker_links, self.trackers)
            self.assertEqual(creator.output_dir, Path(self.temp_dir))
    
    def test_piece_size_calculation(self):
        """测试piece大小计算"""
        with patch('torrent_creator.shutil.which', return_value='/usr/bin/mktorrent'):
            creator = TorrentCreator(self.trackers, self.temp_dir)

            # 测试小文件
            small_size = 10 * 1024 * 1024  # 10MB
            piece_size = creator._calculate_piece_size(small_size)
            self.assertIn(piece_size, creator.PIECE_SIZES)

            # 测试大文件
            large_size = 10 * 1024 * 1024 * 1024  # 10GB
            piece_size = creator._calculate_piece_size(large_size)
            self.assertIn(piece_size, creator.PIECE_SIZES)
    
    def test_filename_sanitization(self):
        """测试文件名清理"""
        with patch('torrent_creator.shutil.which', return_value='/usr/bin/mktorrent'):
            creator = TorrentCreator(self.trackers, self.temp_dir)

            test_cases = [
                ("Game of Thrones: Season 1", "Game of Thrones_ Season 1"),
                ("File<>Name", "File__Name"),
                ("", "torrent"),
                ("   .test.   ", "test"),
            ]

            for input_name, expected in test_cases:
                result = creator._sanitize_filename(input_name)
                self.assertEqual(result, expected)
    
    def test_tracker_management(self):
        """测试tracker管理"""
        with patch('torrent_creator.shutil.which', return_value='/usr/bin/mktorrent'):
            creator = TorrentCreator([], self.temp_dir)

            # 测试添加tracker
            test_tracker = "udp://new.tracker.com:8080/announce"
            result = creator.add_tracker(test_tracker)
            self.assertTrue(result)
            self.assertIn(test_tracker, creator.get_trackers())

            # 测试移除tracker
            result = creator.remove_tracker(test_tracker)
            self.assertTrue(result)
            self.assertNotIn(test_tracker, creator.get_trackers())


if __name__ == '__main__':
    # 设置日志级别
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    # 运行测试
    unittest.main(verbosity=2)
