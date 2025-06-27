#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 PathCompleter 的 get_input 方法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from torrent_maker import PathCompleter

def test_path_completer_input():
    """测试 PathCompleter 的 get_input 方法"""
    print("🔍 测试 PathCompleter 的 get_input 方法")
    print("=" * 50)
    
    # 创建 PathCompleter 实例
    completer = PathCompleter()
    
    # 测试 get_input 方法是否存在
    if hasattr(completer, 'get_input'):
        print("✅ PathCompleter 具有 get_input 方法")
        
        # 测试方法调用（模拟输入）
        print("📝 测试方法调用...")
        
        # 由于这是自动化测试，我们不能真正等待用户输入
        # 但我们可以验证方法存在且可调用
        try:
            # 模拟空输入（通过重定向stdin）
            import io
            old_stdin = sys.stdin
            sys.stdin = io.StringIO("\n")  # 模拟回车
            
            result = completer.get_input("测试提示: ")
            print(f"✅ get_input 方法调用成功，返回: '{result}'")
            
            sys.stdin = old_stdin
            
        except Exception as e:
            print(f"❌ get_input 方法调用失败: {e}")
            sys.stdin = old_stdin
            return False
    else:
        print("❌ PathCompleter 缺少 get_input 方法")
        return False
    
    print("\n🎉 PathCompleter get_input 方法测试完成！")
    return True

if __name__ == "__main__":
    success = test_path_completer_input()
    sys.exit(0 if success else 1)