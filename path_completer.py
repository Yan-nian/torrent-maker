#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Path Completer Module - 路径自动补全模块
为 Torrent Maker 提供智能路径补全功能

功能特性:
- Tab键路径自动补全
- 路径历史记录管理
- 智能路径建议
- 相对路径和绝对路径支持
- 路径验证和错误提示
"""

import os
import json
import glob
import readline
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime


class PathCompleter:
    """路径自动补全器"""
    
    def __init__(self, history_file: str = None):
        self.history_file = history_file or os.path.expanduser("~/.torrent_maker_path_history.json")
        self.path_history: List[Dict[str, Any]] = []
        self.common_paths: List[str] = []
        self.max_history_size = 100
        self.load_history()
        self._setup_readline()
    
    def _setup_readline(self):
        """设置readline自动补全"""
        try:
            import readline
            readline.set_completer(self._readline_completer)
            readline.parse_and_bind("tab: complete")
            # 设置补全分隔符
            readline.set_completer_delims(' \t\n`!@#$%^&*()=+[{]}\\|;:\'\",<>?')
        except ImportError:
            print("⚠️ readline模块不可用，路径补全功能受限")
    
    def _readline_completer(self, text: str, state: int) -> Optional[str]:
        """readline补全函数"""
        if state == 0:
            # 第一次调用，生成补全选项
            self._completion_matches = self.get_completions(text)
        
        try:
            return self._completion_matches[state]
        except IndexError:
            return None
    
    def get_completions(self, partial_path: str) -> List[str]:
        """获取路径补全选项"""
        completions = []
        
        # 如果输入为空，返回历史路径和常用路径
        if not partial_path.strip():
            completions.extend(self.get_recent_paths(5))
            completions.extend(self.common_paths[:5])
            return completions
        
        # 展开用户目录
        expanded_path = os.path.expanduser(partial_path)
        
        # 文件系统路径补全
        try:
            # 如果路径以/结尾，列出目录内容
            if expanded_path.endswith(os.sep):
                if os.path.isdir(expanded_path):
                    for item in os.listdir(expanded_path):
                        full_path = os.path.join(expanded_path, item)
                        if os.path.isdir(full_path):
                            completions.append(full_path + os.sep)
                        else:
                            completions.append(full_path)
            else:
                # 使用glob进行模糊匹配
                glob_pattern = expanded_path + '*'
                matches = glob.glob(glob_pattern)
                for match in matches:
                    if os.path.isdir(match):
                        completions.append(match + os.sep)
                    else:
                        completions.append(match)
        except (OSError, PermissionError):
            pass
        
        # 添加历史路径匹配
        history_matches = self._get_history_matches(partial_path)
        completions.extend(history_matches)
        
        # 去重并排序
        completions = list(set(completions))
        completions.sort()
        
        return completions[:20]  # 限制返回数量
    
    def _get_history_matches(self, partial_path: str) -> List[str]:
        """从历史记录中获取匹配的路径"""
        matches = []
        partial_lower = partial_path.lower()
        
        for entry in self.path_history:
            path = entry['path']
            if partial_lower in path.lower():
                matches.append(path)
        
        return matches
    
    def complete_path_interactive(self, prompt: str = "请输入路径: ") -> str:
        """交互式路径输入with补全"""
        print("💡 提示: 使用Tab键进行路径补全，输入'h'查看历史路径")
        
        while True:
            try:
                user_input = input(prompt).strip()
                
                if user_input.lower() == 'h':
                    self._show_history_menu()
                    continue
                elif user_input.lower() == 'c':
                    self._show_common_paths_menu()
                    continue
                elif user_input:
                    expanded_path = os.path.expanduser(user_input)
                    if self.validate_path(expanded_path):
                        self.add_to_history(expanded_path)
                        return expanded_path
                    else:
                        print(f"❌ 路径不存在或无法访问: {expanded_path}")
                        retry = input("是否重新输入？(y/n): ").strip().lower()
                        if retry not in ['y', 'yes', '是']:
                            return ""
                else:
                    return ""
            except KeyboardInterrupt:
                print("\n❌ 已取消")
                return ""
            except EOFError:
                print("\n❌ 已取消")
                return ""
    
    def _show_history_menu(self):
        """显示历史路径菜单"""
        recent_paths = self.get_recent_paths(10)
        if not recent_paths:
            print("📝 暂无历史路径")
            return
        
        print("\n📝 最近使用的路径:")
        for i, path in enumerate(recent_paths, 1):
            print(f"  {i:2d}. {path}")
        
        try:
            choice = input("\n请选择路径编号 (回车取消): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(recent_paths):
                    selected_path = recent_paths[idx]
                    print(f"✅ 已选择: {selected_path}")
                    return selected_path
        except (ValueError, IndexError):
            pass
        
        return None
    
    def _show_common_paths_menu(self):
        """显示常用路径菜单"""
        if not self.common_paths:
            self._init_common_paths()
        
        print("\n📁 常用路径:")
        for i, path in enumerate(self.common_paths, 1):
            print(f"  {i:2d}. {path}")
        
        try:
            choice = input("\n请选择路径编号 (回车取消): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.common_paths):
                    selected_path = self.common_paths[idx]
                    print(f"✅ 已选择: {selected_path}")
                    return selected_path
        except (ValueError, IndexError):
            pass
        
        return None
    
    def _init_common_paths(self):
        """初始化常用路径"""
        home = os.path.expanduser("~")
        self.common_paths = [
            os.path.join(home, "Downloads"),
            os.path.join(home, "Desktop"),
            os.path.join(home, "Documents"),
            os.path.join(home, "Movies"),
            os.path.join(home, "Videos"),
            "/Volumes",  # macOS外部驱动器
            "/Users",
            "/tmp"
        ]
        # 只保留存在的路径
        self.common_paths = [p for p in self.common_paths if os.path.exists(p)]
    
    def validate_path(self, path: str) -> bool:
        """验证路径是否有效"""
        try:
            return os.path.exists(path) and os.path.isdir(path)
        except (OSError, TypeError):
            return False
    
    def add_to_history(self, path: str):
        """添加路径到历史记录"""
        if not path or not self.validate_path(path):
            return
        
        # 规范化路径
        normalized_path = os.path.abspath(path)
        
        # 检查是否已存在
        for entry in self.path_history:
            if entry['path'] == normalized_path:
                # 更新访问时间和次数
                entry['last_used'] = datetime.now().isoformat()
                entry['use_count'] = entry.get('use_count', 0) + 1
                self.save_history()
                return
        
        # 添加新记录
        new_entry = {
            'path': normalized_path,
            'added_time': datetime.now().isoformat(),
            'last_used': datetime.now().isoformat(),
            'use_count': 1
        }
        
        self.path_history.append(new_entry)
        
        # 限制历史记录大小
        if len(self.path_history) > self.max_history_size:
            # 按使用频率和时间排序，移除最少使用的
            self.path_history.sort(key=lambda x: (x.get('use_count', 0), x.get('last_used', '')), reverse=True)
            self.path_history = self.path_history[:self.max_history_size]
        
        self.save_history()
    
    def get_recent_paths(self, limit: int = 10) -> List[str]:
        """获取最近使用的路径"""
        # 按最后使用时间排序
        sorted_history = sorted(
            self.path_history,
            key=lambda x: x.get('last_used', ''),
            reverse=True
        )
        
        return [entry['path'] for entry in sorted_history[:limit]]
    
    def get_frequent_paths(self, limit: int = 10) -> List[str]:
        """获取最常使用的路径"""
        # 按使用次数排序
        sorted_history = sorted(
            self.path_history,
            key=lambda x: x.get('use_count', 0),
            reverse=True
        )
        
        return [entry['path'] for entry in sorted_history[:limit]]
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.path_history = data.get('path_history', [])
                    self.common_paths = data.get('common_paths', [])
        except (json.JSONDecodeError, OSError) as e:
            print(f"⚠️ 加载路径历史失败: {e}")
            self.path_history = []
            self.common_paths = []
        
        # 初始化常用路径
        if not self.common_paths:
            self._init_common_paths()
    
    def save_history(self):
        """保存历史记录"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            data = {
                'path_history': self.path_history,
                'common_paths': self.common_paths,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"⚠️ 保存路径历史失败: {e}")
    
    def clear_history(self) -> bool:
        """清空历史记录"""
        try:
            self.path_history = []
            self.save_history()
            return True
        except Exception as e:
            print(f"❌ 清空路径历史失败: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取使用统计"""
        if not self.path_history:
            return {'total_paths': 0, 'most_used': None, 'recent_activity': 0}
        
        total_uses = sum(entry.get('use_count', 0) for entry in self.path_history)
        most_used = max(self.path_history, key=lambda x: x.get('use_count', 0))
        
        # 计算最近7天的活动
        from datetime import timedelta
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_activity = sum(
            1 for entry in self.path_history
            if datetime.fromisoformat(entry.get('last_used', '1970-01-01')) > recent_cutoff
        )
        
        return {
            'total_paths': len(self.path_history),
            'total_uses': total_uses,
            'most_used': most_used,
            'recent_activity': recent_activity
        }


def test_path_completer():
    """测试路径补全功能"""
    print("🧪 测试路径补全功能")
    completer = PathCompleter()
    
    # 测试补全功能
    test_paths = [
        "~/",
        "/Users",
        "~/Down",
        "/tmp"
    ]
    
    for path in test_paths:
        print(f"\n测试路径: {path}")
        completions = completer.get_completions(path)
        print(f"补全选项: {completions[:5]}...")  # 只显示前5个
    
    # 测试交互式输入
    print("\n🔧 交互式测试 (输入'quit'退出):")
    while True:
        result = completer.complete_path_interactive("测试路径输入: ")
        if result.lower() == 'quit' or not result:
            break
        print(f"✅ 选择的路径: {result}")
    
    # 显示统计信息
    stats = completer.get_statistics()
    print(f"\n📊 使用统计: {stats}")


if __name__ == "__main__":
    test_path_completer()