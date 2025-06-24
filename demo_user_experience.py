#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户体验优化演示脚本
展示新增的用户体验改进功能
"""

import os
import sys
import tempfile
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_search_history():
    """演示搜索历史功能"""
    print("🎬 演示：搜索历史功能")
    print("=" * 50)
    
    try:
        from search_history import SearchHistory
        
        # 创建临时配置目录
        with tempfile.TemporaryDirectory() as temp_dir:
            history = SearchHistory(config_dir=temp_dir)
            
            # 模拟一些搜索记录
            searches = [
                ("复仇者联盟", 5, "/movies/action"),
                ("钢铁侠", 3, "/movies/action"),
                ("蜘蛛侠", 4, "/movies/action"),
                ("复仇者联盟", 5, "/movies/action"),  # 重复搜索
                ("黑寡妇", 2, "/movies/action")
            ]
            
            print("📝 添加搜索记录...")
            for query, count, folder in searches:
                history.add_search(query, count, folder)
                print(f"   🔍 搜索: {query} (找到 {count} 个结果)")
            
            print("\n📚 最近搜索记录:")
            recent = history.get_recent_searches(5)
            for i, item in enumerate(recent, 1):
                print(f"   h{i}. {item['query']} ({item.get('last_results_count', 0)} 个结果, "
                      f"搜索 {item.get('count', 1)} 次)")
            
            print("\n📊 搜索统计:")
            stats = history.get_statistics()
            print(f"   📈 总搜索次数: {stats['total_searches']}")
            print(f"   🔍 不同关键词: {stats['unique_queries']}")
            print(f"   📊 平均结果数: {stats['average_results']}")
            print(f"   🏆 最常搜索: {stats['most_searched']['query']} "
                  f"({stats['most_searched']['count']} 次)")
            
    except Exception as e:
        print(f"❌ 演示失败: {e}")
    
    print()


def demo_path_formatting():
    """演示路径格式化功能"""
    print("🎬 演示：路径格式化功能")
    print("=" * 50)
    
    try:
        from utils.helpers import format_path_display, get_path_components
        
        # 测试各种路径格式化
        test_paths = [
            "/Users/username/Movies/Action/复仇者联盟.Avengers.Endgame.2019.2160p.UHD.BluRay.x265-TERMINAL",
            "/very/long/path/to/some/movie/folder/that/definitely/exceeds/normal/display/length",
            "~/Downloads/Movies/钢铁侠.Iron.Man.2008.1080p.BluRay.x264",
            "/movies/action/short"
        ]
        
        base_path = "/Users/username/Movies"
        
        print("📁 路径格式化示例:")
        for path in test_paths:
            print(f"\n   原始路径: {path}")
            
            # 完整路径显示
            formatted = format_path_display(path, max_length=60)
            print(f"   格式化后: {formatted}")
            
            # 相对路径显示
            if base_path in path:
                relative = format_path_display(path, base_path, max_length=60)
                print(f"   相对路径: {relative}")
            
            # 路径组件
            components = get_path_components(path)
            print(f"   文件名: {components['basename']}")
            print(f"   目录: {components['dirname']}")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
    
    print()


def demo_navigation_features():
    """演示导航功能"""
    print("🎬 演示：导航功能增强")
    print("=" * 50)
    
    navigation_help = """
🧭 新增导航选项:

📋 搜索结果界面:
   数字 (1-N)     - 选择单个文件夹制种
   1,3,5          - 批量选择多个文件夹
   all/a          - 选择所有文件夹
   info/i         - 查看详细信息
   
🔄 导航命令:
   back/b         - 返回上一步
   menu/m         - 返回主菜单
   history/h      - 查看搜索历史
   search/s       - 继续搜索
   quit/q         - 退出程序

📚 搜索历史快捷方式:
   h1, h2, h3...  - 快速使用历史搜索
   history        - 打开历史管理菜单

💡 搜索提示:
   • 显示最近5次搜索的快捷方式
   • 支持模糊搜索和智能匹配
   • 自动记录搜索历史，最多保存50条
   • 30天自动清理过期记录
"""
    
    print(navigation_help)


def demo_search_interface():
    """演示搜索界面改进"""
    print("🎬 演示：搜索界面改进")
    print("=" * 50)
    
    # 模拟搜索结果显示
    mock_results = [
        {
            'name': '复仇者联盟.Avengers.Endgame.2019.2160p',
            'path': '/Users/username/Movies/Action/复仇者联盟.Avengers.Endgame.2019.2160p.UHD.BluRay.x265',
            'score': 95,
            'file_count': 15,
            'size': '25.6 GB',
            'episodes': '1 部电影'
        },
        {
            'name': '复仇者联盟.Avengers.2012.1080p',
            'path': '/Users/username/Movies/Action/复仇者联盟.Avengers.2012.1080p.BluRay.x264',
            'score': 90,
            'file_count': 12,
            'size': '18.2 GB',
            'episodes': '1 部电影'
        }
    ]
    
    print("🔍 搜索结果显示示例:")
    print("✅ 找到 2 个匹配的文件夹:")
    print("=" * 100)
    
    for i, folder_info in enumerate(mock_results, 1):
        # 模拟路径格式化
        full_path = folder_info['path']
        relative_path = f"./Action/{folder_info['name']}"
        
        print(f"{i:2d}. 📂 {folder_info['name']}")
        print(f"     📍 完整路径: {full_path}")
        print(f"     📁 相对路径: {relative_path}")
        print(f"     📊 匹配度: {folder_info['score']}%")
        print(f"     📄 文件数: {folder_info['file_count']}")
        print(f"     💾 大小: {folder_info['size']}")
        print(f"     🎬 剧集: {folder_info['episodes']}")
        print("-" * 100)
    
    print("\n📋 选择操作 (共 2 个匹配项):")
    print("=" * 60)
    print("🎯 制种操作:")
    print("  数字 (1-2) - 选择单个文件夹制种")
    print("  多个数字用逗号分隔 (如: 1,2) - 批量制种")
    print("  'all' 或 'a' - 选择所有文件夹批量制种")
    print()
    print("🔍 查看详情:")
    print("  'info' 或 'i' - 查看所有匹配项详细信息")
    print("  'd数字' - 查看详细剧集列表 (如: d1)")
    print()
    print("🧭 导航选项:")
    print("  'search' 或 's' - 继续搜索其他内容")
    print("  'history' 或 'h' - 查看搜索历史")
    print("  'back' 或 'b' - 返回上一步")
    print("  'menu' 或 'm' - 返回主菜单")
    print("  'quit' 或 'q' - 退出程序")
    print("=" * 60)


def main():
    """主演示函数"""
    print("🎉 Torrent Maker 用户体验优化演示")
    print("=" * 80)
    print("本演示展示了新增的用户体验改进功能：")
    print("• 📍 完整文件路径显示")
    print("• 📚 智能搜索历史管理")
    print("• 🧭 增强的导航功能")
    print("• 🎯 改进的交互界面")
    print("=" * 80)
    print()
    
    # 运行各个演示
    demo_search_history()
    demo_path_formatting()
    demo_navigation_features()
    demo_search_interface()
    
    print("🎊 演示完成！")
    print("💡 这些改进大大提升了用户体验：")
    print("   • 更直观的路径显示")
    print("   • 更便捷的历史搜索")
    print("   • 更灵活的导航选项")
    print("   • 更友好的交互界面")


if __name__ == "__main__":
    main()
