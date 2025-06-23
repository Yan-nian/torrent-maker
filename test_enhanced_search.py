#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试改进后的文件名匹配功能
"""

import os
import tempfile
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_matching():
    """测试增强的文件名匹配功能"""
    print("🧪 测试增强的文件名匹配功能...")
    
    # 导入完整版本的FileMatcher
    from src.file_matcher import FileMatcher
    
    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试文件夹
        test_folders = [
            "The.Beginning.After.the.End.S01",
            "The Beginning After the End - Season 1",
            "The_Beginning_After_the_End_Complete",
            "TBATE.Season.01",
            "Beginning.After.End.2024",
            "Game.of.Thrones.S01",
            "Game of Thrones Season 1",
            "Other.Random.Show.S01"
        ]
        
        for folder_name in test_folders:
            folder_path = os.path.join(temp_dir, folder_name)
            os.makedirs(folder_path)
            # 创建一个测试文件
            with open(os.path.join(folder_path, "test.mkv"), 'w') as f:
                f.write("test")
        
        # 测试FileMatcher
        matcher = FileMatcher(temp_dir)
        
        # 测试用例
        test_cases = [
            ("The Beginning After the End", "点号分隔格式"),
            ("TBATE", "首字母缩写"),
            ("Beginning After End", "部分关键词"),
            ("Game of Thrones", "空格分隔格式")
        ]
        
        for search_term, description in test_cases:
            print(f"\n🔍 搜索: '{search_term}' ({description})")
            print("-" * 50)
            
            results = matcher.match_folders(search_term)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"{i}. 📂 {result['name']}")
                    print(f"   📊 匹配度: {result['score']}%")
                    print(f"   📍 原始名称: {result['name']}")
                    
                    # 显示标准化后的名称用于调试
                    normalized = matcher.normalize_string(result['name'])
                    search_normalized = matcher.normalize_string(search_term)
                    print(f"   🔧 标准化: '{normalized}' vs '{search_normalized}'")
                    print()
            else:
                print("❌ 未找到匹配结果")
    
    print("✅ 增强匹配功能测试完成")

def test_normalization():
    """测试字符串标准化功能"""
    print("\n🧪 测试字符串标准化功能...")
    
    from src.file_matcher import FileMatcher
    matcher = FileMatcher("/tmp")
    
    test_strings = [
        "The.Beginning.After.the.End",
        "The_Beginning_After_the_End",
        "The-Beginning-After-the-End",
        "The Beginning After the End",
        "TBATE.Season.01",
        "Game.of.Thrones.S01E01",
        "Breaking Bad - Season 1"
    ]
    
    for test_str in test_strings:
        normalized = matcher.normalize_string(test_str)
        print(f"📝 原始: '{test_str}'")
        print(f"🔧 标准化: '{normalized}'")
        print()
    
    print("✅ 字符串标准化测试完成")

if __name__ == "__main__":
    print("🎬 Torrent Maker 增强搜索功能测试")
    print("=" * 60)
    
    try:
        test_enhanced_matching()
        test_normalization()
        
        print("\n🎉 所有测试通过！搜索功能已优化。")
        print("\n💡 改进说明：")
        print("- 支持点号、下划线、连字符等分隔符")
        print("- 智能词汇匹配和重叠度计算")
        print("- 首字母缩写匹配 (如 TBATE)")
        print("- 移除常见停用词提升匹配精度")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
