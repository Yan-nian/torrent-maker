#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
搜索历史管理器
提供搜索历史记录、快速重复搜索和历史管理功能
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta


class SearchHistory:
    """搜索历史管理器"""
    
    def __init__(self, config_dir: str = None, max_history: int = 50):
        """
        初始化搜索历史管理器
        
        Args:
            config_dir: 配置目录路径
            max_history: 最大历史记录数量
        """
        if config_dir is None:
            config_dir = os.path.expanduser("~/.torrent_maker")
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.history_file = self.config_dir / "search_history.json"
        self.max_history = max_history
        self.history: List[Dict[str, Any]] = []
        
        self._load_history()
    
    def _load_history(self):
        """加载搜索历史"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])
                    
                    # 清理过期的历史记录（超过30天）
                    self._cleanup_old_history()
            else:
                self.history = []
        except Exception as e:
            print(f"⚠️ 加载搜索历史失败: {e}")
            self.history = []
    
    def _save_history(self):
        """保存搜索历史"""
        try:
            data = {
                'history': self.history,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 保存搜索历史失败: {e}")
    
    def _cleanup_old_history(self):
        """清理过期的历史记录"""
        try:
            cutoff_time = datetime.now() - timedelta(days=30)
            
            # 过滤掉过期的记录
            self.history = [
                item for item in self.history
                if datetime.fromisoformat(item.get('timestamp', '1970-01-01'))
                > cutoff_time
            ]
            
            # 限制历史记录数量
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
                
        except Exception as e:
            print(f"⚠️ 清理历史记录失败: {e}")
    
    def add_search(self, query: str, results_count: int = 0, 
                   resource_folder: str = None) -> None:
        """
        添加搜索记录
        
        Args:
            query: 搜索关键词
            results_count: 搜索结果数量
            resource_folder: 搜索的资源文件夹
        """
        if not query or not query.strip():
            return
        
        query = query.strip()
        
        # 检查是否已存在相同的搜索（最近10条记录内）
        recent_queries = [item['query'] for item in self.history[-10:]]
        if query in recent_queries:
            # 更新现有记录的时间戳
            for item in reversed(self.history):
                if item['query'] == query:
                    item['timestamp'] = datetime.now().isoformat()
                    item['count'] = item.get('count', 0) + 1
                    item['last_results_count'] = results_count
                    if resource_folder:
                        item['resource_folder'] = resource_folder
                    break
        else:
            # 添加新记录
            record = {
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'results_count': results_count,
                'count': 1,
                'last_results_count': results_count
            }
            
            if resource_folder:
                record['resource_folder'] = resource_folder
            
            self.history.append(record)
        
        # 限制历史记录数量
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        self._save_history()
    
    def get_recent_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取最近的搜索记录
        
        Args:
            limit: 返回记录数量限制
        
        Returns:
            最近的搜索记录列表
        """
        # 按时间戳倒序排列
        sorted_history = sorted(
            self.history,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        
        return sorted_history[:limit]
    
    def get_popular_searches(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        获取热门搜索记录（按搜索次数排序）
        
        Args:
            limit: 返回记录数量限制
        
        Returns:
            热门搜索记录列表
        """
        # 按搜索次数倒序排列
        sorted_history = sorted(
            self.history,
            key=lambda x: x.get('count', 0),
            reverse=True
        )
        
        return sorted_history[:limit]
    
    def search_in_history(self, keyword: str) -> List[Dict[str, Any]]:
        """
        在历史记录中搜索
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的历史记录列表
        """
        keyword = keyword.lower()
        matches = []
        
        for item in self.history:
            if keyword in item['query'].lower():
                matches.append(item)
        
        # 按时间戳倒序排列
        matches.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return matches
    
    def clear_history(self) -> bool:
        """
        清空搜索历史
        
        Returns:
            清空成功返回True，否则返回False
        """
        try:
            self.history = []
            self._save_history()
            return True
        except Exception as e:
            print(f"❌ 清空搜索历史失败: {e}")
            return False
    
    def remove_search(self, query: str) -> bool:
        """
        删除指定的搜索记录
        
        Args:
            query: 要删除的搜索关键词
        
        Returns:
            删除成功返回True，否则返回False
        """
        try:
            original_length = len(self.history)
            self.history = [item for item in self.history if item['query'] != query]
            
            if len(self.history) < original_length:
                self._save_history()
                return True
            else:
                return False
        except Exception as e:
            print(f"❌ 删除搜索记录失败: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取搜索历史统计信息
        
        Returns:
            统计信息字典
        """
        if not self.history:
            return {
                'total_searches': 0,
                'unique_queries': 0,
                'average_results': 0,
                'most_searched': None,
                'recent_activity': 0
            }
        
        total_searches = sum(item.get('count', 1) for item in self.history)
        unique_queries = len(self.history)
        
        # 计算平均结果数
        results_counts = [item.get('last_results_count', 0) for item in self.history]
        average_results = sum(results_counts) / len(results_counts) if results_counts else 0
        
        # 找出最常搜索的关键词
        most_searched = max(self.history, key=lambda x: x.get('count', 0))
        
        # 计算最近7天的活动
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_activity = sum(
            1 for item in self.history
            if datetime.fromisoformat(item.get('timestamp', '1970-01-01')) > recent_cutoff
        )
        
        return {
            'total_searches': total_searches,
            'unique_queries': unique_queries,
            'average_results': round(average_results, 1),
            'most_searched': most_searched,
            'recent_activity': recent_activity
        }
    
    def display_history(self, limit: int = 10) -> None:
        """
        显示搜索历史
        
        Args:
            limit: 显示记录数量限制
        """
        recent_searches = self.get_recent_searches(limit)
        
        if not recent_searches:
            print("📝 暂无搜索历史")
            return
        
        print(f"\n📚 最近 {len(recent_searches)} 次搜索:")
        print("=" * 80)
        
        for i, item in enumerate(recent_searches, 1):
            timestamp = datetime.fromisoformat(item['timestamp'])
            time_str = timestamp.strftime("%m-%d %H:%M")
            
            print(f"{i:2d}. 🔍 {item['query']}")
            print(f"     ⏰ {time_str} | 📊 {item.get('last_results_count', 0)} 个结果 | "
                  f"🔄 搜索 {item.get('count', 1)} 次")
            
            if item.get('resource_folder'):
                print(f"     📁 {item['resource_folder']}")
            
            print("-" * 80)
