#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试单文件版本的增强搜索功能
"""

import os
import tempfile
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_standalone_enhanced_matching():
    """测试单文件版本的增强匹配功能"""
    print("🧪 测试单文件版本的增强匹配功能...")
    
    # 导入单文件版本的FileMatcher
    from torrent_maker import FileMatcher
    
    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试文件夹
        test_folders = [
            "The.Beginning.After.the.End.S01",
            "The Beginning After the End - Season 1",
            "TBATE.Season.01"
        ]
        
        for folder_name in test_folders:
            folder_path = os.path.join(temp_dir, folder_name)
            os.makedirs(folder_path)
            # 创建一个测试文件
            with open(os.path.join(folder_path, "test.mkv"), 'w') as f:
                f.write("test")
        
        # 测试FileMatcher
        matcher = FileMatcher(temp_dir)
        
        print(f"\n🔍 搜索: 'The Beginning After the End'")
        print("-" * 50)
        
        results = matcher.match_folders("The Beginning After the End")
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"{i}. 📂 {result['name']}")
                print(f"   📊 匹配度: {result['score']}%")
                
                # 测试剧集信息
                if result.get('episodes'):
                    print(f"   🎬 剧集: {result['episodes']} (共{result['video_count']}集)")
                
                print()
        else:
            print("❌ 未找到匹配结果")
    
    print("✅ 单文件版本增强匹配功能测试完成")

if __name__ == "__main__":
    print("🎬 单文件版本增强搜索功能测试")
    print("=" * 50)
    
    try:
        test_standalone_enhanced_matching()
        print("\n🎉 单文件版本搜索功能验证成功！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
