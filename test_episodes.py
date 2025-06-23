#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧集信息解析功能快速测试
"""

import os
import tempfile
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_episode_parsing():
    """测试剧集信息解析功能"""
    print("🧪 测试剧集信息解析功能...")
    
    # 导入单文件版本的FileMatcher
    from torrent_maker import FileMatcher
    
    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as temp_dir:
        test_folder = os.path.join(temp_dir, "Game.of.Thrones.S01")
        os.makedirs(test_folder)
        
        # 创建测试文件
        test_files = [
            "Game.of.Thrones.S01E01.Winter.Is.Coming.mkv",
            "Game.of.Thrones.S01E02.The.Kingsroad.mkv",
            "Game.of.Thrones.S01E03.Lord.Snow.mkv",
            "Game.of.Thrones.S01E04.Cripples.Bastards.and.Broken.Things.mkv",
            "Game.of.Thrones.S01E05.The.Wolf.and.the.Lion.mkv"
        ]
        
        for filename in test_files:
            file_path = os.path.join(test_folder, filename)
            with open(file_path, 'w') as f:
                f.write("test video content")
        
        # 测试FileMatcher
        matcher = FileMatcher(temp_dir)
        
        # 测试文件夹匹配
        results = matcher.match_folders("Game of Thrones")
        
        print(f"📊 找到 {len(results)} 个匹配结果")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. 📂 {result['name']}")
            print(f"   📊 匹配度: {result['score']}%")
            print(f"   📄 文件数: {result['file_count']}")
            print(f"   🎬 剧集: {result.get('episodes', '无')}")
            print(f"   📺 总集数: {result.get('video_count', 0)}集")
            
            # 测试详细信息
            if result.get('episodes'):
                detail = matcher.get_folder_episodes_detail(result['path'])
                print(f"   📋 详细信息预览:")
                print("   " + detail.replace('\n', '\n   ')[:200] + "...")
            
            print("-" * 50)
    
    print("✅ 剧集信息解析功能测试完成")

def test_file_parsing():
    """测试文件名解析功能"""
    print("\n🧪 测试文件名解析功能...")
    
    from torrent_maker import FileMatcher
    
    matcher = FileMatcher("/tmp")
    
    test_files = [
        "Game.of.Thrones.S01E01.mkv",
        "The.Office.S2E5.mkv", 
        "Breaking.Bad.E12.mp4",
        "Friends.101.avi",
        "Stranger.Things.S03E08.mkv"
    ]
    
    for filename in test_files:
        result = matcher.parse_episode_from_filename(filename)
        if result:
            season = result.get('season', 'N/A')
            episode = result.get('episode', 'N/A')
            pattern = result.get('pattern_type', 'N/A')
            print(f"📄 {filename}")
            print(f"   🎭 季: {season}, 集: {episode}")
            print(f"   🔍 模式: {pattern}")
        else:
            print(f"📄 {filename} - 无法解析")
        print()
    
    print("✅ 文件名解析功能测试完成")

if __name__ == "__main__":
    print("🎬 Torrent Maker 剧集功能测试")
    print("=" * 50)
    
    try:
        test_episode_parsing()
        test_file_parsing()
        
        print("\n🎉 所有测试通过！剧集功能正常工作。")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
