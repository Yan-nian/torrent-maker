#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search History Module - 搜索历史记录模块
为 Torrent Maker 提供智能搜索历史和建议功能

功能特性:
- 搜索历史记录管理
- 智能搜索建议
- 搜索统计和分析
- 快速搜索访问
- 搜索模式识别
"""

import os
import json
import re
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import Counter, defaultdict
import difflib


@dataclass
class SearchEntry:
    """搜索记录条目"""
    query: str
    timestamp: datetime
    results_count: int = 0
    selected_results: List[str] = field(default_factory=list)
    success: bool = True
    search_time: float = 0.0  # 搜索耗时(秒)
    category: str = ""  # 搜索分类(电影、电视剧、动漫等)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'query': self.query,
            'timestamp': self.timestamp.isoformat(),
            'results_count': self.results_count,
            'selected_results': self.selected_results,
            'success': self.success,
            'search_time': self.search_time,
            'category': self.category,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SearchEntry':
        """从字典创建"""
        return cls(
            query=data['query'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            results_count=data.get('results_count', 0),
            selected_results=data.get('selected_results', []),
            success=data.get('success', True),
            search_time=data.get('search_time', 0.0),
            category=data.get('category', ''),
            metadata=data.get('metadata', {})
        )


class SearchHistory:
    """搜索历史管理器"""
    
    def __init__(self, history_file: str = None, max_entries: int = 1000):
        self.history_file = history_file or os.path.expanduser("~/.torrent_maker_search_history.json")
        self.max_entries = max_entries
        self.entries: List[SearchEntry] = []
        self.load_history()
    
    def add_search(self, query: str, results_count: int = 0, 
                   selected_results: List[str] = None, success: bool = True,
                   search_time: float = 0.0, category: str = "",
                   **metadata) -> SearchEntry:
        """添加搜索记录"""
        # 清理查询字符串
        cleaned_query = self._clean_query(query)
        if not cleaned_query:
            return None
        
        # 检查是否是重复搜索(5分钟内的相同查询)
        recent_cutoff = datetime.now() - timedelta(minutes=5)
        for entry in reversed(self.entries):
            if (entry.timestamp > recent_cutoff and 
                entry.query.lower() == cleaned_query.lower()):
                # 更新现有记录
                entry.results_count = max(entry.results_count, results_count)
                if selected_results:
                    entry.selected_results.extend(selected_results)
                    entry.selected_results = list(set(entry.selected_results))  # 去重
                entry.success = entry.success and success
                entry.search_time = (entry.search_time + search_time) / 2  # 平均搜索时间
                if category:
                    entry.category = category
                entry.metadata.update(metadata)
                self.save_history()
                return entry
        
        # 创建新记录
        entry = SearchEntry(
            query=cleaned_query,
            timestamp=datetime.now(),
            results_count=results_count,
            selected_results=selected_results or [],
            success=success,
            search_time=search_time,
            category=category,
            metadata=metadata
        )
        
        self.entries.append(entry)
        
        # 限制历史记录大小
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
        
        self.save_history()
        return entry
    
    def _clean_query(self, query: str) -> str:
        """清理查询字符串"""
        if not query:
            return ""
        
        # 移除多余空格
        cleaned = re.sub(r'\s+', ' ', query.strip())
        
        # 移除特殊字符(保留中文、英文、数字、常用符号)
        cleaned = re.sub(r'[^\w\s\u4e00-\u9fff.\-_()\[\]]+', '', cleaned)
        
        return cleaned
    
    def get_suggestions(self, partial_query: str, limit: int = 10) -> List[Tuple[str, float]]:
        """获取搜索建议"""
        if not partial_query.strip():
            # 返回最近的搜索
            recent_queries = [entry.query for entry in reversed(self.entries[-limit:])]
            return [(query, 1.0) for query in recent_queries]
        
        partial_lower = partial_query.lower().strip()
        suggestions = []
        
        # 收集所有查询
        all_queries = [entry.query for entry in self.entries]
        
        # 计算相似度
        for query in set(all_queries):  # 去重
            query_lower = query.lower()
            
            # 精确匹配
            if query_lower.startswith(partial_lower):
                suggestions.append((query, 1.0))
            # 包含匹配
            elif partial_lower in query_lower:
                suggestions.append((query, 0.8))
            # 模糊匹配
            else:
                similarity = difflib.SequenceMatcher(None, partial_lower, query_lower).ratio()
                if similarity > 0.6:
                    suggestions.append((query, similarity))
        
        # 按相似度和使用频率排序
        query_counts = Counter(all_queries)
        suggestions.sort(key=lambda x: (x[1], query_counts[x[0]]), reverse=True)
        
        return suggestions[:limit]
    
    def get_popular_queries(self, limit: int = 10, days: int = 30) -> List[Tuple[str, int]]:
        """获取热门搜索"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_entries = [entry for entry in self.entries if entry.timestamp > cutoff_date]
        
        query_counts = Counter(entry.query for entry in recent_entries)
        return query_counts.most_common(limit)
    
    def get_recent_queries(self, limit: int = 10) -> List[str]:
        """获取最近搜索"""
        recent_queries = []
        seen = set()
        
        for entry in reversed(self.entries):
            if entry.query not in seen:
                recent_queries.append(entry.query)
                seen.add(entry.query)
                if len(recent_queries) >= limit:
                    break
        
        return recent_queries
    
    def get_successful_queries(self, limit: int = 10) -> List[str]:
        """获取成功的搜索(有结果且被选择)"""
        successful_queries = []
        seen = set()
        
        for entry in reversed(self.entries):
            if (entry.success and entry.results_count > 0 and 
                entry.selected_results and entry.query not in seen):
                successful_queries.append(entry.query)
                seen.add(entry.query)
                if len(successful_queries) >= limit:
                    break
        
        return successful_queries
    
    def search_history(self, keyword: str, limit: int = 20) -> List[SearchEntry]:
        """搜索历史记录"""
        keyword_lower = keyword.lower()
        matches = []
        
        for entry in self.entries:
            if (keyword_lower in entry.query.lower() or 
                keyword_lower in entry.category.lower() or
                any(keyword_lower in result.lower() for result in entry.selected_results)):
                matches.append(entry)
        
        # 按时间倒序排列
        matches.sort(key=lambda x: x.timestamp, reverse=True)
        return matches[:limit]
    
    def get_categories(self) -> List[Tuple[str, int]]:
        """获取搜索分类统计"""
        category_counts = Counter(entry.category for entry in self.entries if entry.category)
        return category_counts.most_common()
    
    def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """获取搜索统计"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_entries = [entry for entry in self.entries if entry.timestamp > cutoff_date]
        
        if not recent_entries:
            return {
                'total_searches': 0,
                'successful_searches': 0,
                'success_rate': 0.0,
                'average_search_time': 0.0,
                'average_results': 0.0,
                'most_active_day': None,
                'popular_categories': []
            }
        
        total_searches = len(recent_entries)
        successful_searches = sum(1 for entry in recent_entries if entry.success and entry.results_count > 0)
        success_rate = (successful_searches / total_searches) * 100 if total_searches > 0 else 0
        
        # 平均搜索时间
        search_times = [entry.search_time for entry in recent_entries if entry.search_time > 0]
        average_search_time = sum(search_times) / len(search_times) if search_times else 0
        
        # 平均结果数
        results_counts = [entry.results_count for entry in recent_entries if entry.results_count > 0]
        average_results = sum(results_counts) / len(results_counts) if results_counts else 0
        
        # 最活跃的日期
        daily_counts = defaultdict(int)
        for entry in recent_entries:
            date_key = entry.timestamp.date()
            daily_counts[date_key] += 1
        
        most_active_day = max(daily_counts.items(), key=lambda x: x[1]) if daily_counts else None
        
        # 热门分类
        category_counts = Counter(entry.category for entry in recent_entries if entry.category)
        popular_categories = category_counts.most_common(5)
        
        return {
            'total_searches': total_searches,
            'successful_searches': successful_searches,
            'success_rate': success_rate,
            'average_search_time': average_search_time,
            'average_results': average_results,
            'most_active_day': most_active_day,
            'popular_categories': popular_categories
        }
    
    def clear_history(self, older_than_days: int = None) -> int:
        """清空历史记录"""
        if older_than_days is None:
            # 清空所有
            count = len(self.entries)
            self.entries = []
        else:
            # 清空指定天数前的记录
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            old_count = len(self.entries)
            self.entries = [entry for entry in self.entries if entry.timestamp > cutoff_date]
            count = old_count - len(self.entries)
        
        self.save_history()
        return count
    
    def export_history(self, output_file: str, format: str = 'json') -> bool:
        """导出历史记录"""
        try:
            if format.lower() == 'json':
                data = {
                    'export_time': datetime.now().isoformat(),
                    'total_entries': len(self.entries),
                    'entries': [entry.to_dict() for entry in self.entries]
                }
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            elif format.lower() == 'csv':
                import csv
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['查询', '时间', '结果数', '成功', '搜索时间', '分类'])
                    for entry in self.entries:
                        writer.writerow([
                            entry.query,
                            entry.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                            entry.results_count,
                            '是' if entry.success else '否',
                            f"{entry.search_time:.2f}s",
                            entry.category
                        ])
            
            return True
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    entries_data = data.get('entries', data)  # 兼容旧格式
                    self.entries = [SearchEntry.from_dict(entry_data) for entry_data in entries_data]
        except (json.JSONDecodeError, OSError, KeyError) as e:
            print(f"⚠️ 加载搜索历史失败: {e}")
            self.entries = []
    
    def save_history(self):
        """保存历史记录"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            data = {
                'version': '1.0',
                'last_updated': datetime.now().isoformat(),
                'total_entries': len(self.entries),
                'entries': [entry.to_dict() for entry in self.entries]
            }
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"⚠️ 保存搜索历史失败: {e}")


class SmartSearchSuggester:
    """智能搜索建议器"""
    
    def __init__(self, search_history: SearchHistory):
        self.history = search_history
        self.patterns = self._load_search_patterns()
    
    def _load_search_patterns(self) -> Dict[str, List[str]]:
        """加载搜索模式"""
        return {
            '电影': [
                r'\d{4}',  # 年份
                r'(电影|movie|film)',
                r'(HD|4K|1080p|720p|BluRay|BDRip)',
                r'(中字|字幕|subtitle)'
            ],
            '电视剧': [
                r'(第\d+季|S\d+|season)',
                r'(第\d+集|E\d+|episode)',
                r'(电视剧|TV|series)',
                r'(全集|完整版|complete)'
            ],
            '动漫': [
                r'(动漫|anime|动画)',
                r'(第\d+话|第\d+集)',
                r'(OVA|OAD|剧场版)',
                r'(日语|中配|双语)'
            ],
            '纪录片': [
                r'(纪录片|documentary)',
                r'(BBC|National Geographic|Discovery)',
                r'(自然|历史|科学)'
            ]
        }
    
    def suggest_improvements(self, query: str) -> List[str]:
        """建议查询改进"""
        suggestions = []
        
        # 检测可能的分类
        detected_category = self._detect_category(query)
        if detected_category:
            suggestions.append(f"检测到类型: {detected_category}")
        
        # 建议添加年份
        if not re.search(r'\d{4}', query) and detected_category in ['电影', '电视剧']:
            suggestions.append("建议添加年份以获得更精确的结果")
        
        # 建议添加画质信息
        if not re.search(r'(HD|4K|1080p|720p|BluRay)', query, re.IGNORECASE):
            suggestions.append("可以添加画质信息 (如: 1080p, 4K)")
        
        # 建议添加字幕信息
        if not re.search(r'(中字|字幕|subtitle)', query, re.IGNORECASE):
            suggestions.append("可以添加字幕信息 (如: 中字)")
        
        return suggestions
    
    def _detect_category(self, query: str) -> Optional[str]:
        """检测查询分类"""
        query_lower = query.lower()
        
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return category
        
        return None
    
    def get_related_queries(self, query: str, limit: int = 5) -> List[str]:
        """获取相关查询"""
        # 提取关键词
        keywords = self._extract_keywords(query)
        
        related = []
        for entry in self.history.entries:
            if entry.query.lower() != query.lower():
                entry_keywords = self._extract_keywords(entry.query)
                # 计算关键词重叠度
                overlap = len(set(keywords) & set(entry_keywords))
                if overlap > 0:
                    related.append((entry.query, overlap))
        
        # 按重叠度排序
        related.sort(key=lambda x: x[1], reverse=True)
        return [query for query, _ in related[:limit]]
    
    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词"""
        # 移除常见停用词
        stop_words = {'的', '和', '与', '或', '在', '是', '有', '了', '中', '为', '从', '到'}
        
        # 分词(简单按空格和标点分割)
        words = re.findall(r'[\w\u4e00-\u9fff]+', query.lower())
        
        # 过滤停用词和短词
        keywords = [word for word in words if len(word) > 1 and word not in stop_words]
        
        return keywords


def test_search_history():
    """测试搜索历史功能"""
    print("🧪 测试搜索历史功能")
    
    history = SearchHistory()
    suggester = SmartSearchSuggester(history)
    
    # 添加测试数据
    test_queries = [
        ("复仇者联盟4 2019 4K", 15, ["Avengers.Endgame.2019.4K.mkv"], True, 1.2, "电影"),
        ("权力的游戏 第八季", 8, ["Game.of.Thrones.S08.mkv"], True, 0.8, "电视剧"),
        ("鬼灭之刃 动漫", 12, ["Demon.Slayer.anime.mkv"], True, 0.9, "动漫"),
        ("复仇者联盟", 25, [], True, 1.5, "电影"),
        ("权力的游戏", 20, ["Game.of.Thrones.S01.mkv"], True, 1.1, "电视剧")
    ]
    
    for query, count, results, success, time, category in test_queries:
        history.add_search(query, count, results, success, time, category)
    
    # 测试建议功能
    print("\n🔍 搜索建议测试:")
    suggestions = history.get_suggestions("复仇")
    for suggestion, score in suggestions:
        print(f"  {suggestion} (相似度: {score:.2f})")
    
    # 测试热门查询
    print("\n🔥 热门查询:")
    popular = history.get_popular_queries()
    for query, count in popular:
        print(f"  {query}: {count}次")
    
    # 测试智能建议
    print("\n💡 智能建议:")
    improvements = suggester.suggest_improvements("复仇者联盟")
    for improvement in improvements:
        print(f"  {improvement}")
    
    # 测试相关查询
    print("\n🔗 相关查询:")
    related = suggester.get_related_queries("复仇者联盟4")
    for query in related:
        print(f"  {query}")
    
    # 显示统计信息
    stats = history.get_statistics()
    print(f"\n📊 统计信息:")
    print(f"  总搜索次数: {stats['total_searches']}")
    print(f"  成功率: {stats['success_rate']:.1f}%")
    print(f"  平均搜索时间: {stats['average_search_time']:.2f}秒")
    print(f"  平均结果数: {stats['average_results']:.1f}")


if __name__ == "__main__":
    test_search_history()