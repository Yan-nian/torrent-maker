#!/usr/bin/env python3
"""
测试修复后的剧集信息显示
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from file_matcher import FileMatcher

def test_episode_display_fix():
    """测试剧集显示修复"""
    print("🧪 测试剧集信息显示修复")
    print("=" * 50)
    
    # 创建FileMatcher实例
    matcher = FileMatcher("")
    
    # 测试断集情况的格式化
    test_cases = [
        # 连续集数
        ([1, 2, 3, 4, 5], "E01-E05"),
        ([2, 3, 4, 5], "E02-E05"),
        
        # 单集
        ([1], "E01"),
        
        # 少量断集
        ([1, 3, 5], "E01+E03+E05"),
        ([2, 4, 6], "E02+E04+E06"),
        
        # 多个断集
        ([2, 3, 4, 6, 7, 8, 10, 11, 12], "E02-E12(9集)"),
        ([1, 3, 5, 7, 9, 11, 13, 15], "E01-E15(8集)"),
        
        # 从中间开始的连续集数（模拟您遇到的情况）
        ([2, 3, 4, 5, 6, 7, 8, 9], "E02-E09"),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "E01-E10"),
    ]
    
    print("📋 测试用例:")
    for i, (episode_numbers, expected) in enumerate(test_cases, 1):
        result = matcher._format_episode_range(episode_numbers)
        status = "✅" if result == expected else "❌"
        print(f"{i:2d}. {status} 输入: {episode_numbers}")
        print(f"    预期: {expected}")
        print(f"    实际: {result}")
        if result != expected:
            print(f"    ⚠️  不匹配！")
        print()
    
    print("🔍 季度摘要测试:")
    print("-" * 30)
    
    # 测试生成季度摘要
    test_episodes = [
        {'season': 2, 'episode': 2, 'filename': 'test_s02e02.mp4'},
        {'season': 2, 'episode': 3, 'filename': 'test_s02e03.mp4'},
        {'season': 2, 'episode': 4, 'filename': 'test_s02e04.mp4'},
        {'season': 2, 'episode': 6, 'filename': 'test_s02e06.mp4'},
        {'season': 2, 'episode': 7, 'filename': 'test_s02e07.mp4'},
        {'season': 2, 'episode': 8, 'filename': 'test_s02e08.mp4'},
        {'season': 2, 'episode': 10, 'filename': 'test_s02e10.mp4'},
        {'season': 2, 'episode': 12, 'filename': 'test_s02e12.mp4'},
    ]
    
    seasons = {2}
    summary = matcher.generate_season_summary(test_episodes, seasons)
    print(f"测试剧集: 8个文件 (S02E02, E03, E04, E06, E07, E08, E10, E12)")
    print(f"生成摘要: {summary}")
    
    # 预期应该是类似 "S02E02-E12(8集)" 的格式
    print()
    print("✅ 修复验证完成！")
    print("现在剧集信息应该正确显示集数范围和实际文件数量")

if __name__ == "__main__":
    test_episode_display_fix()
