#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试修复后的功能
验证 ConfigManager 错误修复和批量制种功能重构
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_manager():
    """测试 ConfigManager 的 get_setting 方法"""
    print("🧪 测试 ConfigManager...")
    
    try:
        # 导入 torrent_maker 中的 ConfigManager
        from torrent_maker import ConfigManager
        
        # 创建 ConfigManager 实例
        config = ConfigManager()
        
        # 测试 get_setting 方法
        print("  ✅ ConfigManager 实例创建成功")
        
        # 测试基本方法
        resource_folder = config.get_resource_folder()
        output_folder = config.get_output_folder()
        trackers = config.get_trackers()
        
        print(f"  📁 资源文件夹: {resource_folder}")
        print(f"  📂 输出文件夹: {output_folder}")
        print(f"  🌐 Tracker 数量: {len(trackers)}")
        
        # 测试 get_setting 方法
        if hasattr(config, 'get_setting'):
            tolerance = config.get_setting('file_search_tolerance', 60)
            max_results = config.get_setting('max_search_results', 10)
            cache_enabled = config.get_setting('enable_cache', True)
            
            print(f"  🔧 搜索容错率: {tolerance}%")
            print(f"  📊 最大搜索结果: {max_results}")
            print(f"  💾 缓存状态: {'启用' if cache_enabled else '禁用'}")
            print("  ✅ get_setting 方法工作正常")
        else:
            print("  ❌ get_setting 方法不存在")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ ConfigManager 测试失败: {e}")
        return False

def test_torrent_maker_app():
    """测试 TorrentMakerApp 的配置管理功能"""
    print("\n🧪 测试 TorrentMakerApp...")
    
    try:
        from torrent_maker import TorrentMakerApp
        
        # 创建应用实例
        app = TorrentMakerApp()
        print("  ✅ TorrentMakerApp 实例创建成功")
        
        # 测试配置显示方法
        print("  🔍 测试配置显示功能...")
        app._show_current_config()
        print("  ✅ 配置显示功能正常")
        
        return True
        
    except Exception as e:
        print(f"  ❌ TorrentMakerApp 测试失败: {e}")
        return False

def test_batch_create_methods():
    """测试批量制种功能"""
    print("\n🧪 测试批量制种功能...")
    
    try:
        from torrent_maker import TorrentMakerApp
        
        app = TorrentMakerApp()
        
        # 检查批量制种相关方法是否存在
        methods_to_check = [
            'batch_create',
            '_batch_create_from_search',
            '_batch_create_from_paths',
            '_format_path_display',
            '_parse_selection',
            '_execute_batch_creation'
        ]
        
        for method_name in methods_to_check:
            if hasattr(app, method_name):
                print(f"  ✅ {method_name} 方法存在")
            else:
                print(f"  ❌ {method_name} 方法不存在")
                return False
        
        # 测试路径格式化功能
        test_path = "/very/long/path/to/some/folder/that/should/be/shortened/because/it/is/too/long"
        formatted = app._format_path_display(test_path)
        print(f"  🔧 路径格式化测试: {formatted}")
        
        # 测试选择解析功能
        test_results = [
            {'name': 'folder1', 'path': '/path1'},
            {'name': 'folder2', 'path': '/path2'},
            {'name': 'folder3', 'path': '/path3'}
        ]
        
        selected = app._parse_selection("1,3", test_results)
        if len(selected) == 2:
            print("  ✅ 选择解析功能正常")
        else:
            print("  ❌ 选择解析功能异常")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ 批量制种功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试修复后的功能")
    print("=" * 50)
    
    tests = [
        ("ConfigManager 功能", test_config_manager),
        ("TorrentMakerApp 配置管理", test_torrent_maker_app),
        ("批量制种功能", test_batch_create_methods)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} 测试通过")
        else:
            print(f"❌ {test_name} 测试失败")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！修复成功！")
        return True
    else:
        print("⚠️ 部分测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
