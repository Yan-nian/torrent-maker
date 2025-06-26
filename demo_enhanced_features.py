#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强功能演示脚本
展示 Torrent Maker v1.9.1 用户体验优化版的新功能
"""

import os
import sys
import time
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from path_completer import PathCompleter
    from progress_monitor import TorrentProgressMonitor
    from search_history import SearchHistory, SmartSearchSuggester
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

def demo_path_completer():
    """演示路径补全功能"""
    print("\n" + "=" * 60)
    print("🔍 路径补全功能演示")
    print("=" * 60)
    
    completer = PathCompleter()
    
    # 添加一些示例路径
    demo_paths = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        "/Applications",
        "/System"
    ]
    
    print("📁 添加示例路径到历史记录...")
    for path in demo_paths:
        if os.path.exists(path):
            completer.add_to_history(path)
            print(f"  ✅ {path}")
    
    # 显示路径补全功能
    print("\n🔧 路径补全测试:")
    test_inputs = ["~/", "/App", "/Sys"]
    
    for test_input in test_inputs:
        completions = completer.get_completions(test_input)
        print(f"\n输入: '{test_input}'")
        print(f"补全选项 (前5个):")
        for i, completion in enumerate(completions[:5], 1):
            print(f"  {i}. {completion}")
    
    # 显示历史记录
    recent_paths = completer.get_recent_paths(5)
    print(f"\n📝 最近使用的路径:")
    for i, path in enumerate(recent_paths, 1):
        print(f"  {i}. {path}")
    
    # 显示统计信息
    stats = completer.get_statistics()
    print(f"\n📊 路径使用统计:")
    print(f"  总路径数: {stats['total_paths']}")
    print(f"  总使用次数: {stats['total_uses']}")
    print(f"  最近7天活动: {stats['recent_activity']}")

def demo_progress_monitor():
    """演示进度监控功能"""
    print("\n" + "=" * 60)
    print("📊 进度监控功能演示")
    print("=" * 60)
    
    monitor = TorrentProgressMonitor()
    
    # 创建演示任务
    task_id = "demo_task_1"
    task_name = "演示制种任务"
    file_path = "/demo/path/movie.mkv"
    file_size = 1024 * 1024 * 1024  # 1GB
    
    print(f"🎬 创建演示任务: {task_name}")
    monitor.create_task(task_id, task_name, file_path, file_size=file_size)
    monitor.start_task(task_id)
    
    print("\n🔄 模拟制种进度...")
    try:
        for i in range(0, 101, 5):
            progress = float(i)
            current_step = f"处理数据块 {i//5 + 1}/21"
            processed_size = int(file_size * progress / 100)
            
            monitor.update_progress(
                task_id,
                progress=progress,
                current_step=current_step,
                processed_size=processed_size
            )
            
            # 获取任务信息并显示
            task = monitor.get_task(task_id)
            if task:
                print(f"\r📦 {task.name[:20]:<20} |{'█' * int(progress//5)}{'░' * (20-int(progress//5))}| {progress:6.2f}% {current_step}", end="")
            
            time.sleep(0.1)
        
        print("\n✅ 任务完成!")
        monitor.complete_task(task_id, success=True)
        
    except KeyboardInterrupt:
        print("\n❌ 用户取消")
        monitor.cancel_task(task_id)
    
    # 显示统计信息
    stats = monitor.get_statistics()
    print(f"\n📊 监控统计:")
    print(f"  总任务数: {stats['total_tasks']}")
    print(f"  成功率: {stats['success_rate']:.1f}%")
    for status, count in stats['status_counts'].items():
        if count > 0:
            print(f"  {status}: {count}")

def demo_search_history():
    """演示搜索历史功能"""
    print("\n" + "=" * 60)
    print("📝 搜索历史功能演示")
    print("=" * 60)
    
    # 使用临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        history = SearchHistory(temp_file)
        suggester = SmartSearchSuggester(history)
        
        # 添加演示数据
        demo_searches = [
            ("复仇者联盟4 终局之战 2019 4K", 15, ["Avengers.Endgame.2019.4K.mkv"], True, 1.2, "电影"),
            ("权力的游戏 第八季 完整版", 8, ["Game.of.Thrones.S08.Complete.mkv"], True, 0.8, "电视剧"),
            ("鬼灭之刃 动漫 全集", 12, ["Demon.Slayer.Complete.mkv"], True, 0.9, "动漫"),
            ("复仇者联盟 2012", 25, ["Avengers.2012.mkv"], True, 1.5, "电影"),
            ("权力的游戏 第一季", 20, ["Game.of.Thrones.S01.mkv"], True, 1.1, "电视剧"),
            ("钢铁侠 2008", 18, ["Iron.Man.2008.mkv"], True, 1.0, "电影"),
            ("美国队长 2011", 16, ["Captain.America.2011.mkv"], True, 0.9, "电影"),
            ("雷神 2011", 14, ["Thor.2011.mkv"], True, 0.8, "电影")
        ]
        
        print("📚 添加演示搜索记录...")
        for query, count, results, success, search_time, category in demo_searches:
            history.add_search(query, count, results, success, search_time, category)
            print(f"  ✅ {query}")
        
        # 显示搜索建议
        print("\n🔍 智能搜索建议测试:")
        test_queries = ["复仇", "权力", "钢铁"]
        
        for query in test_queries:
            suggestions = history.get_suggestions(query, limit=3)
            print(f"\n输入: '{query}'")
            print("建议:")
            for suggestion, score in suggestions:
                print(f"  📌 {suggestion} (相似度: {score:.2f})")
        
        # 显示热门搜索
        print("\n🔥 热门搜索:")
        popular = history.get_popular_queries(5)
        for i, (query, count) in enumerate(popular, 1):
            print(f"  {i}. {query} ({count}次)")
        
        # 显示分类统计
        print("\n📊 分类统计:")
        categories = history.get_categories()
        for category, count in categories:
            print(f"  {category}: {count}次")
        
        # 智能建议演示
        print("\n💡 智能搜索改进建议:")
        test_query = "复仇者联盟"
        improvements = suggester.suggest_improvements(test_query)
        print(f"查询: '{test_query}'")
        for improvement in improvements:
            print(f"  💡 {improvement}")
        
        # 相关查询
        print("\n🔗 相关查询推荐:")
        related = suggester.get_related_queries("复仇者联盟4", limit=3)
        for query in related:
            print(f"  🔗 {query}")
        
        # 显示统计信息
        stats = history.get_statistics()
        print(f"\n📊 搜索统计:")
        print(f"  总搜索次数: {stats['total_searches']}")
        print(f"  成功搜索: {stats['successful_searches']}")
        print(f"  成功率: {stats['success_rate']:.1f}%")
        print(f"  平均搜索时间: {stats['average_search_time']:.2f}秒")
        print(f"  平均结果数: {stats['average_results']:.1f}")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def main():
    """主演示函数"""
    print("🎉 Torrent Maker v1.9.1 用户体验优化版")
    print("🚀 增强功能演示")
    print("=" * 60)
    
    print("\n本演示将展示以下新功能:")
    print("  1. 🔍 智能路径补全")
    print("  2. 📊 实时制种进度监控")
    print("  3. 📝 搜索历史管理")
    print("  4. 💡 智能搜索建议")
    
    input("\n按回车键开始演示...")
    
    try:
        # 演示路径补全
        demo_path_completer()
        input("\n按回车键继续下一个演示...")
        
        # 演示进度监控
        demo_progress_monitor()
        input("\n按回车键继续下一个演示...")
        
        # 演示搜索历史
        demo_search_history()
        
        print("\n" + "=" * 60)
        print("🎉 演示完成！")
        print("=" * 60)
        print("\n✨ 新功能亮点:")
        print("  🔍 智能路径补全 - 提高路径输入效率")
        print("  📊 实时进度监控 - 可视化制种过程")
        print("  📝 搜索历史管理 - 智能记录和建议")
        print("  💡 用户体验优化 - 更直观的操作界面")
        print("\n🚀 现在可以运行 python3 torrent_maker.py 体验完整功能！")
        
    except KeyboardInterrupt:
        print("\n❌ 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main()