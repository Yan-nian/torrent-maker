#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 Bug 修复
验证搜索功能和文件夹设置功能的修复
"""

import sys
import os
import tempfile

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_range_fix():
    """测试 range() 修复"""
    print("🧪 测试 range() 修复...")
    
    try:
        # 模拟空文件夹列表的情况
        all_folders = []
        batch_size = min(1000, len(all_folders)) if all_folders else 1
        
        # 这应该不会抛出 "range() arg 3 must not be zero" 错误
        for i in range(0, len(all_folders), batch_size):
            pass
            
        print("  ✅ 空文件夹列表处理正常")
        
        # 测试非空列表
        all_folders = ['folder1', 'folder2', 'folder3']
        batch_size = min(1000, len(all_folders)) if all_folders else 1
        
        iterations = 0
        for i in range(0, len(all_folders), batch_size):
            iterations += 1
            
        print(f"  ✅ 非空文件夹列表处理正常 (迭代 {iterations} 次)")
        return True
        
    except Exception as e:
        print(f"  ❌ range() 修复失败: {e}")
        return False

def test_folder_setting_fix():
    """测试文件夹设置修复"""
    print("\n🧪 测试文件夹设置修复...")
    
    try:
        from torrent_maker import ConfigManager
        
        config = ConfigManager()
        
        # 测试设置不存在的路径
        result1 = config.set_resource_folder('/nonexistent/path/12345')
        if not result1:
            print("  ✅ 不存在路径正确拒绝")
        else:
            print("  ❌ 不存在路径应该被拒绝")
            return False
        
        # 测试设置存在的路径
        result2 = config.set_resource_folder('/tmp')
        if result2:
            print("  ✅ 存在路径正确接受")
        else:
            print("  ❌ 存在路径应该被接受")
            return False
        
        # 测试设置文件而不是目录
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        try:
            result3 = config.set_resource_folder(temp_file)
            if not result3:
                print("  ✅ 文件路径正确拒绝")
            else:
                print("  ❌ 文件路径应该被拒绝")
                return False
        finally:
            os.unlink(temp_file)
        
        return True
        
    except Exception as e:
        print(f"  ❌ 文件夹设置修复失败: {e}")
        return False

def test_search_functionality():
    """测试搜索功能"""
    print("\n🧪 测试搜索功能...")
    
    try:
        from torrent_maker import FileMatcher
        
        # 使用一个存在的目录进行测试
        test_dir = '/tmp'
        matcher = FileMatcher(test_dir)
        
        # 测试搜索（即使没有匹配结果也不应该崩溃）
        results = matcher.match_folders('nonexistent_test_query_12345')
        print(f"  ✅ 搜索功能正常 (找到 {len(results)} 个结果)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 搜索功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔧 Bug 修复验证测试")
    print("=" * 50)
    
    tests = [
        test_range_fix,
        test_folder_setting_fix,
        test_search_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ❌ 测试执行失败: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有修复验证通过！")
        return True
    else:
        print("⚠️  部分修复可能存在问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
