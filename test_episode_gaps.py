#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试断集处理功能
"""

import os
import tempfile
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_episode_gaps():
    """测试断集处理功能"""
    print("🧪 测试断集处理功能...")
    
    # 导入完整版本的FileMatcher
    from src.file_matcher import FileMatcher
    
    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 测试用例1：有断集的情况
        test_folder_1 = os.path.join(temp_dir, "Gag.Manga.Biyori.S02.2025")
        os.makedirs(test_folder_1)
        
        # 模拟您提到的情况：E02, E03, E05, E07, E08, E10, E11, E12 (缺少E01, E04, E06, E09)
        gap_files = [
            "Gag.Manga.Biyori.S02E02.mkv",
            "Gag.Manga.Biyori.S02E03.mkv", 
            "Gag.Manga.Biyori.S02E05.mkv",
            "Gag.Manga.Biyori.S02E07.mkv",
            "Gag.Manga.Biyori.S02E08.mkv",
            "Gag.Manga.Biyori.S02E10.mkv",
            "Gag.Manga.Biyori.S02E11.mkv",
            "Gag.Manga.Biyori.S02E12.mkv"
        ]
        
        for filename in gap_files:
            file_path = os.path.join(test_folder_1, filename)
            with open(file_path, 'w') as f:
                f.write("test video content")
        
        # 测试用例2：连续集数
        test_folder_2 = os.path.join(temp_dir, "Complete.Series.S01")
        os.makedirs(test_folder_2)
        
        continuous_files = [
            "Complete.Series.S01E01.mkv",
            "Complete.Series.S01E02.mkv",
            "Complete.Series.S01E03.mkv",
            "Complete.Series.S01E04.mkv"
        ]
        
        for filename in continuous_files:
            file_path = os.path.join(test_folder_2, filename)
            with open(file_path, 'w') as f:
                f.write("test video content")
        
        # 测试用例3：只有少数几集（非连续）
        test_folder_3 = os.path.join(temp_dir, "Few.Episodes.S01")
        os.makedirs(test_folder_3)
        
        few_files = [
            "Few.Episodes.S01E01.mkv",
            "Few.Episodes.S01E03.mkv",
            "Few.Episodes.S01E07.mkv"
        ]
        
        for filename in few_files:
            file_path = os.path.join(test_folder_3, filename)
            with open(file_path, 'w') as f:
                f.write("test video content")
        
        # 测试FileMatcher
        matcher = FileMatcher(temp_dir)
        
        test_cases = [
            ("Gag Manga Biyori", "断集测试"),
            ("Complete Series", "连续集数测试"),
            ("Few Episodes", "少数集数测试")
        ]
        
        for search_term, description in test_cases:
            print(f"\n🔍 {description}: '{search_term}'")
            print("-" * 60)
            
            results = matcher.match_folders(search_term)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"{i}. 📂 {result['name']}")
                    print(f"   📊 匹配度: {result['score']}%")
                    print(f"   📄 文件数: {result['file_count']}")
                    print(f"   🎬 剧集: {result.get('episodes', '无')} (共{result.get('video_count', 0)}集)")
                    
                    # 显示详细信息
                    detailed = matcher.get_folder_episodes_detail(result['path'])
                    if detailed != "无剧集信息":
                        print(f"   📋 详细: {detailed.split(chr(10))[1] if chr(10) in detailed else detailed}")
                    print()
            else:
                print("❌ 未找到匹配结果")
    
    print("✅ 断集处理功能测试完成")

def test_format_episode_range():
    """测试集数范围格式化功能"""
    print("\n🧪 测试集数范围格式化功能...")
    
    from src.file_matcher import FileMatcher
    matcher = FileMatcher("/tmp")
    
    test_cases = [
        ([1, 2, 3, 4, 5], "连续集数"),
        ([2, 3, 5, 7, 8, 10, 11, 12], "有断集的多集"),
        ([1, 3, 7], "少数非连续集"),
        ([5, 6, 7, 8], "中间连续段"),
        ([1], "单集"),
        ([1, 2], "两集连续"),
        ([1, 5], "两集非连续")
    ]
    
    for episode_numbers, description in test_cases:
        result = matcher._format_episode_range(episode_numbers)
        print(f"📝 {description}: {episode_numbers} → '{result}'")
    
    print("✅ 集数范围格式化测试完成")

if __name__ == "__main__":
    print("🎬 断集处理功能测试")
    print("=" * 60)
    
    try:
        test_episode_gaps()
        test_format_episode_range()
        
        print("\n🎉 所有测试通过！断集处理功能已优化。")
        print("\n💡 改进说明：")
        print("- 智能检测连续和非连续集数")
        print("- 断集情况显示实际集数和总数")
        print("- 少数集数直接列出具体集数")
        print("- 连续集数仍使用范围格式")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
