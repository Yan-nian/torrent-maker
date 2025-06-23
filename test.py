#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Torrent Maker 测试脚本
用于验证各个模块的基本功能
"""

import sys
import os
import tempfile

# 添加 src 目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def test_config_manager():
    """测试配置管理器"""
    print("🧪 测试配置管理器...")
    
    try:
        from config_manager import ConfigManager
        
        # 创建临时配置文件
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_path = os.path.join(temp_dir, 'settings.json')
            trackers_path = os.path.join(temp_dir, 'trackers.txt')
            
            config = ConfigManager(settings_path, trackers_path)
            
            # 测试基本功能
            assert isinstance(config.get_resource_folder(), str)
            assert isinstance(config.get_trackers(), list)
            
            print("✅ 配置管理器测试通过")
            return True
            
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {e}")
        return False

def test_file_matcher():
    """测试文件匹配器"""
    print("🧪 测试文件匹配器...")
    
    try:
        from file_matcher import FileMatcher
        
        # 创建临时测试目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建一些测试文件夹
            test_folders = [
                "权力的游戏.第一季.2011",
                "Game.of.Thrones.S01.2011",
                "权力的游戏.第二季.2012",
                "其他电影"
            ]
            
            for folder in test_folders:
                folder_path = os.path.join(temp_dir, folder)
                os.makedirs(folder_path)
                # 创建一些测试文件
                for i in range(3):
                    test_file = os.path.join(folder_path, f"test_file_{i}.txt")
                    with open(test_file, 'w') as f:
                        f.write("test content")
            
            matcher = FileMatcher(temp_dir)
            
            # 测试搜索功能
            results = matcher.match_folders("权力的游戏")
            assert len(results) > 0
            
            # 测试文件数量统计
            test_folder_path = os.path.join(temp_dir, test_folders[0])
            file_count = matcher.display_file_count(test_folder_path)
            assert file_count == 3
            
            print("✅ 文件匹配器测试通过")
            return True
            
    except Exception as e:
        print(f"❌ 文件匹配器测试失败: {e}")
        return False

def test_torrent_creator():
    """测试种子创建器"""
    print("🧪 测试种子创建器...")
    
    try:
        from torrent_creator import TorrentCreator
        import shutil
        
        # 检查 mktorrent 是否可用
        if not shutil.which('mktorrent'):
            print("⚠️  mktorrent 未安装，跳过种子创建器测试")
            return True
        
        trackers = ["http://tracker.example.com/announce"]
        output_dir = "/tmp/test_output"
        creator = TorrentCreator(trackers, output_dir)
        
        # 测试基本功能
        assert creator.check_mktorrent() == True
        assert len(creator.get_trackers()) == 1
        assert creator.output_dir == output_dir
        
        print("✅ 种子创建器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 种子创建器测试失败: {e}")
        return False

def test_helpers():
    """测试辅助函数"""
    print("🧪 测试辅助函数...")
    
    try:
        from utils.helpers import format_file_size, sanitize_filename, is_video_file
        
        # 测试文件大小格式化
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1024 * 1024) == "1.0 MB"
        
        # 测试文件名清理
        assert sanitize_filename("test<>file") == "test__file"
        
        # 测试视频文件检测
        assert is_video_file("movie.mp4") == True
        assert is_video_file("document.txt") == False
        
        print("✅ 辅助函数测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 辅助函数测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("🎬 Torrent Maker 功能测试")
    print("=" * 40)
    
    tests = [
        test_config_manager,
        test_file_matcher,
        test_torrent_creator,
        test_helpers
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！程序可以正常使用。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查相关功能。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
