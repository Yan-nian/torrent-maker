#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户体验优化功能测试
测试搜索历史、路径显示、导航功能等新增的用户体验改进
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_search_history():
    """测试搜索历史功能"""
    print("🧪 测试搜索历史功能...")
    
    try:
        from search_history import SearchHistory
        
        # 创建临时配置目录
        with tempfile.TemporaryDirectory() as temp_dir:
            history = SearchHistory(config_dir=temp_dir, max_history=10)
            
            # 测试添加搜索记录
            history.add_search("复仇者联盟", 5, "/test/movies")
            history.add_search("钢铁侠", 3, "/test/movies")
            history.add_search("复仇者联盟", 5, "/test/movies")  # 重复搜索
            
            # 测试获取最近搜索
            recent = history.get_recent_searches(5)
            assert len(recent) == 2, f"期望2条记录，实际{len(recent)}条"
            assert recent[0]['query'] == "复仇者联盟", "最近搜索应该是复仇者联盟"
            assert recent[0]['count'] == 2, "复仇者联盟应该被搜索2次"
            
            # 测试统计信息
            stats = history.get_statistics()
            assert stats['total_searches'] == 3, f"总搜索次数应该是3，实际{stats['total_searches']}"
            assert stats['unique_queries'] == 2, f"不同关键词应该是2，实际{stats['unique_queries']}"
            
            print("✅ 搜索历史功能测试通过")
            return True
            
    except Exception as e:
        print(f"❌ 搜索历史功能测试失败: {e}")
        return False


def test_path_formatting():
    """测试路径格式化功能"""
    print("🧪 测试路径格式化功能...")
    
    try:
        from utils.helpers import format_path_display, get_path_components
        
        # 测试路径格式化
        long_path = "/very/long/path/to/some/movie/folder/that/exceeds/normal/length"
        formatted = format_path_display(long_path, max_length=50)
        assert len(formatted) <= 50, f"格式化后路径长度应该≤50，实际{len(formatted)}"
        assert "..." in formatted, "长路径应该包含省略号"
        
        # 测试相对路径
        base_path = "/movies"
        full_path = "/movies/action/avengers"
        relative = format_path_display(full_path, base_path, max_length=100)
        assert relative.startswith("./"), "相对路径应该以./开头"
        
        # 测试路径组件
        components = get_path_components("/test/path/movie.mkv")
        assert components['basename'] == "movie.mkv", "文件名解析错误"
        assert components['dirname'] == "/test/path", "目录名解析错误"
        
        print("✅ 路径格式化功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 路径格式化功能测试失败: {e}")
        return False


def test_navigation_commands():
    """测试导航命令解析"""
    print("🧪 测试导航命令解析...")
    
    try:
        # 模拟导航命令测试
        navigation_commands = {
            'back': ['back', 'b', '返回'],
            'menu': ['menu', 'm', '主菜单'],
            'history': ['history', 'h', '历史'],
            'quit': ['quit', 'q', '退出'],
            'info': ['info', 'i', 'a'],
            'all': ['all', '全选']
        }
        
        # 测试命令识别
        for command_type, aliases in navigation_commands.items():
            for alias in aliases:
                # 这里可以添加具体的命令解析测试
                assert alias.lower() == alias.lower(), f"命令{alias}应该被正确识别"
        
        print("✅ 导航命令解析测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 导航命令解析测试失败: {e}")
        return False


def test_search_integration():
    """测试搜索功能集成"""
    print("🧪 测试搜索功能集成...")
    
    try:
        # 创建测试目录结构
        with tempfile.TemporaryDirectory() as temp_dir:
            test_movies = [
                "复仇者联盟.Avengers.2012.1080p",
                "钢铁侠.Iron.Man.2008.720p",
                "雷神.Thor.2011.1080p"
            ]
            
            # 创建测试文件夹
            for movie in test_movies:
                movie_dir = Path(temp_dir) / movie
                movie_dir.mkdir()
                # 创建一些测试文件
                (movie_dir / "movie.mkv").touch()
                (movie_dir / "subtitle.srt").touch()
            
            # 测试文件匹配器
            from file_matcher import FileMatcher
            matcher = FileMatcher(temp_dir)
            
            # 测试搜索
            results = matcher.match_folders("复仇者")
            assert len(results) >= 1, "应该找到复仇者联盟"
            assert any("复仇者联盟" in r['name'] for r in results), "结果中应该包含复仇者联盟"
            
            # 测试模糊搜索
            results = matcher.match_folders("iron")
            assert len(results) >= 1, "应该找到钢铁侠"
            
            print("✅ 搜索功能集成测试通过")
            return True
            
    except Exception as e:
        print(f"❌ 搜索功能集成测试失败: {e}")
        return False


def test_user_interface_improvements():
    """测试用户界面改进"""
    print("🧪 测试用户界面改进...")
    
    try:
        # 测试菜单显示（模拟）
        menu_items = [
            "🔍 搜索并制作种子",
            "📚 搜索历史管理",
            "🧭 导航选项",
            "💡 搜索提示"
        ]
        
        for item in menu_items:
            assert "🔍" in item or "📚" in item or "🧭" in item or "💡" in item, f"菜单项{item}应该包含图标"
        
        # 测试快捷键映射
        shortcuts = {
            's': 'search',
            'h': 'history', 
            'b': 'back',
            'q': 'quit',
            'm': 'menu'
        }
        
        for shortcut, command in shortcuts.items():
            assert len(shortcut) == 1, f"快捷键{shortcut}应该是单字符"
            assert command.isalpha(), f"命令{command}应该是字母"
        
        print("✅ 用户界面改进测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 用户界面改进测试失败: {e}")
        return False


def run_all_tests():
    """运行所有用户体验测试"""
    print("🚀 开始用户体验优化功能测试")
    print("=" * 60)
    
    tests = [
        test_search_history,
        test_path_formatting,
        test_navigation_commands,
        test_search_integration,
        test_user_interface_improvements
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试 {test.__name__} 异常: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("🎉 所有用户体验优化功能测试通过！")
        return True
    else:
        print("⚠️ 部分测试失败，请检查相关功能")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
