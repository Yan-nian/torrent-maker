import os
from difflib import SequenceMatcher
from typing import List, Tuple
import sys

# 添加 utils 目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(current_dir, 'utils')
sys.path.insert(0, utils_dir)

try:
    from helpers import extract_episode_info, format_episode_details
except ImportError:
    # 如果导入失败，提供简单的替代函数
    def extract_episode_info(folder_path):
        return {'episodes': [], 'season_info': '', 'total_episodes': 0}
    
    def format_episode_details(episodes):
        return "无剧集信息"


class FileMatcher:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory
        self.min_score = 0.6  # 最小匹配分数阈值 (0-1)

    def similarity(self, a: str, b: str) -> float:
        """计算两个字符串的相似度"""
        # 标准化处理
        a_normalized = self.normalize_string(a)
        b_normalized = self.normalize_string(b)
        
        # 计算基本相似度
        basic_score = SequenceMatcher(None, a_normalized, b_normalized).ratio()
        
        # 如果标准化后的字符串完全匹配，给予高分
        if a_normalized == b_normalized:
            return 1.0
        
        # 如果一个字符串包含另一个，提升分数
        if a_normalized in b_normalized or b_normalized in a_normalized:
            basic_score = max(basic_score, 0.85)
        
        return basic_score

    def normalize_string(self, text: str) -> str:
        """标准化字符串，处理常见的分隔符和格式"""
        import re
        
        # 转为小写
        text = text.lower()
        
        # 替换常见分隔符为空格
        separators = ['.', '_', '-', ':', '|', '\\', '/', '+']
        for sep in separators:
            text = text.replace(sep, ' ')
        
        # 移除多余的空格
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 移除常见的无意义词汇
        stop_words = ['the', 'and', 'of', 'to', 'in', 'a', 'an']
        words = text.split()
        filtered_words = [word for word in words if word not in stop_words or len(words) <= 3]
        
        return ' '.join(filtered_words)

    def get_all_folders(self) -> List[str]:
        """获取基础目录下的所有文件夹"""
        folders = []
        if not os.path.exists(self.base_directory):
            print(f"警告：资源文件夹不存在：{self.base_directory}")
            return folders
            
        for root, dirs, files in os.walk(self.base_directory):
            for dir_name in dirs:
                full_path = os.path.join(root, dir_name)
                folders.append(full_path)
        return folders

    def fuzzy_search(self, search_name: str) -> List[Tuple[str, float]]:
        """使用模糊匹配搜索文件夹"""
        all_folders = self.get_all_folders()
        
        matches = []
        search_name_normalized = self.normalize_string(search_name)
        
        for folder_path in all_folders:
            folder_name = os.path.basename(folder_path)
            
            # 计算相似度
            similarity_score = self.similarity(search_name, folder_name)
            
            # 额外的匹配策略
            folder_name_normalized = self.normalize_string(folder_name)
            
            # 1. 检查标准化后的包含关系
            if search_name_normalized in folder_name_normalized:
                similarity_score = max(similarity_score, 0.9)
            
            # 2. 检查关键词匹配
            search_words = set(search_name_normalized.split())
            folder_words = set(folder_name_normalized.split())
            
            if search_words and folder_words:
                # 计算词汇重叠度
                common_words = search_words.intersection(folder_words)
                word_overlap_ratio = len(common_words) / len(search_words)
                
                if word_overlap_ratio >= 0.7:  # 70%的词汇匹配
                    similarity_score = max(similarity_score, 0.8 + word_overlap_ratio * 0.1)
            
            # 3. 检查首字母缩写匹配
            search_initials = ''.join([word[0] for word in search_name_normalized.split() if word])
            folder_initials = ''.join([word[0] for word in folder_name_normalized.split() if word])
            
            if len(search_initials) >= 3 and search_initials == folder_initials:
                similarity_score = max(similarity_score, 0.75)
            
            # 过滤低分匹配
            if similarity_score >= self.min_score:
                matches.append((folder_path, similarity_score))
        
        # 按分数降序排列，限制结果数量
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:10]  # 最多返回10个结果

    def display_file_count(self, folder_path: str) -> int:
        """计算文件夹内的文件数量（包括子文件夹）"""
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return 0
        
        total_files = 0
        try:
            for root, dirs, files in os.walk(folder_path):
                total_files += len(files)
        except PermissionError:
            print(f"警告：无法访问文件夹 {folder_path}")
            return 0
        
        return total_files

    def get_folder_size(self, folder_path: str) -> str:
        """获取文件夹大小（格式化字符串）"""
        total_size = 0
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
        except (PermissionError, OSError):
            return "无法计算"
        
        # 格式化大小
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if total_size < 1024.0:
                return f"{total_size:.1f} {unit}"
            total_size /= 1024.0
        return f"{total_size:.1f} PB"

    def match_folders(self, search_name: str) -> List[dict]:
        """搜索并返回匹配的文件夹信息"""
        matches = self.fuzzy_search(search_name)
        
        result = []
        for folder_path, score in matches:
            file_count = self.display_file_count(folder_path)
            folder_size = self.get_folder_size(folder_path)
            
            # 获取剧集信息
            episode_info = self.extract_episode_info_simple(folder_path)
            season_info = episode_info.get('season_info', '')
            total_episodes = episode_info.get('total_episodes', 0)
            
            result.append({
                'path': folder_path,
                'name': os.path.basename(folder_path),
                'score': int(score * 100),  # 转换为百分比
                'file_count': file_count,
                'size': folder_size,
                'episodes': season_info,
                'video_count': total_episodes
            })
        
        return result

    def get_folder_episodes_detail(self, folder_path: str) -> str:
        """获取文件夹剧集详细信息"""
        episode_info = self.extract_episode_info_simple(folder_path)
        episodes = episode_info.get('episodes', [])
        
        if not episodes:
            return "无剧集信息"
        
        # 按季度分组显示详细信息
        seasons_dict = {}
        no_season_episodes = []
        
        for ep in episodes:
            if ep['season']:
                if ep['season'] not in seasons_dict:
                    seasons_dict[ep['season']] = []
                seasons_dict[ep['season']].append(ep)
            else:
                no_season_episodes.append(ep)
        
        details = []
        
        # 显示有季度信息的剧集
        for season in sorted(seasons_dict.keys()):
            season_episodes = sorted(seasons_dict[season], key=lambda x: x['episode'] or 0)
            episode_numbers = [ep['episode'] for ep in season_episodes if ep['episode']]
            
            if episode_numbers:
                min_ep = min(episode_numbers)
                max_ep = max(episode_numbers)
                if min_ep == max_ep:
                    details.append(f"  第{season}季: E{min_ep:02d}")
                else:
                    details.append(f"  第{season}季: E{min_ep:02d}-E{max_ep:02d} (共{len(episode_numbers)}集)")
        
        # 显示没有季度信息的剧集
        if no_season_episodes:
            episode_numbers = [ep['episode'] for ep in no_season_episodes if ep['episode']]
            if episode_numbers:
                min_ep = min(episode_numbers)
                max_ep = max(episode_numbers)
                if min_ep == max_ep:
                    details.append(f"  剧集: E{min_ep:02d}")
                else:
                    details.append(f"  剧集: E{min_ep:02d}-E{max_ep:02d} (共{len(episode_numbers)}集)")
            else:
                details.append(f"  其他视频: {len(no_season_episodes)}个")
        
        return '\n'.join(details) if details else f"  视频文件: {len(episodes)}个"

    def extract_episode_info_simple(self, folder_path: str) -> dict:
        """简单的剧集信息提取"""
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return {'episodes': [], 'season_info': '', 'total_episodes': 0}
        
        import re
        episodes = []
        seasons = set()
        
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if self.is_video_file(file):
                        episode_info = self.parse_episode_from_filename(file)
                        if episode_info:
                            episodes.append(episode_info)
                            if episode_info['season']:
                                seasons.add(episode_info['season'])
        except (PermissionError, OSError):
            return {'episodes': [], 'season_info': '无法访问', 'total_episodes': 0}
        
        # 排序剧集
        episodes.sort(key=lambda x: (x['season'] or 0, x['episode'] or 0))
        
        # 生成季度信息摘要
        season_info = self.generate_season_summary(episodes, seasons)
        
        return {
            'episodes': episodes,
            'season_info': season_info,
            'total_episodes': len(episodes),
            'seasons': sorted(list(seasons)) if seasons else []
        }

    def is_video_file(self, filename: str) -> bool:
        """检查文件是否为视频文件"""
        video_extensions = {
            '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
            '.webm', '.m4v', '.3gp', '.ogv', '.ts', '.m2ts'
        }
        _, ext = os.path.splitext(filename.lower())
        return ext in video_extensions

    def parse_episode_from_filename(self, filename: str) -> dict:
        """从文件名中解析剧集信息"""
        import re
        
        # 常见的剧集命名模式
        patterns = [
            # S01E01, S1E1, s01e01
            (r'[Ss](\d{1,2})[Ee](\d{1,3})', 'season_episode'),
            # Season 1 Episode 01
            (r'[Ss]eason\s*(\d{1,2})\s*[Ee]pisode\s*(\d{1,3})', 'season_episode'),
            # 第一季第01集
            (r'第(\d{1,2})季第(\d{1,3})集', 'season_episode'),
            # 1x01, 01x01
            (r'(\d{1,2})x(\d{1,3})', 'season_episode'),
            # EP01, Ep.01, 第01集
            (r'(?:[Ee][Pp]\.?\s*(\d{1,3})|第(\d{1,3})集)', 'episode_only'),
        ]
        
        for pattern, pattern_type in patterns:
            match = re.search(pattern, filename)
            if match:
                if pattern_type == 'season_episode':
                    season = int(match.group(1))
                    episode = int(match.group(2))
                    return {
                        'season': season,
                        'episode': episode,
                        'filename': filename,
                        'pattern_type': pattern_type
                    }
                elif pattern_type == 'episode_only':
                    episode = int(match.group(1) or match.group(2))
                    return {
                        'season': None,
                        'episode': episode,
                        'filename': filename,
                        'pattern_type': pattern_type
                    }
        
        return None

    def generate_season_summary(self, episodes: list, seasons: set) -> str:
        """生成季度摘要信息"""
        if not episodes:
            return "无剧集信息"
        
        if not seasons or None in seasons:
            # 没有明确的季度信息，只显示集数范围
            episode_numbers = sorted([ep['episode'] for ep in episodes if ep['episode']])
            if episode_numbers:
                return self._format_episode_range(episode_numbers)
            else:
                return f"{len(episodes)}个视频"
        
        # 有明确季度信息
        season_summaries = []
        
        for season in sorted(seasons):
            season_episodes = [ep for ep in episodes if ep['season'] == season]
            episode_numbers = sorted([ep['episode'] for ep in season_episodes if ep['episode']])
            
            if episode_numbers:
                episode_range = self._format_episode_range(episode_numbers)
                season_summary = f"S{season:02d}{episode_range}"
                season_summaries.append(season_summary)
        
        return ', '.join(season_summaries) if season_summaries else f"{len(episodes)}个视频"

    def _format_episode_range(self, episode_numbers: list) -> str:
        """格式化集数范围，智能处理断集情况"""
        if not episode_numbers:
            return ""
        
        episode_numbers = sorted(set(episode_numbers))  # 去重并排序
        
        if len(episode_numbers) == 1:
            return f"E{episode_numbers[0]:02d}"
        
        # 检查是否是连续的集数
        is_continuous = True
        expected = episode_numbers[0]
        for num in episode_numbers:
            if num != expected:
                is_continuous = False
                break
            expected += 1
        
        if is_continuous:
            # 连续集数，使用范围格式
            return f"E{episode_numbers[0]:02d}-E{episode_numbers[-1]:02d}"
        else:
            # 有断集，检查断集的情况
            min_ep = episode_numbers[0]
            max_ep = episode_numbers[-1]
            total_count = len(episode_numbers)
            expected_count = max_ep - min_ep + 1
            
            if total_count == expected_count:
                # 虽然不是从1开始，但在范围内是连续的
                return f"E{min_ep:02d}-E{max_ep:02d}"
            elif total_count <= 3:
                # 集数较少，直接列出所有集数
                episode_list = [f"E{ep:02d}" for ep in episode_numbers]
                return "+".join(episode_list)
            else:
                # 集数较多但有断集，显示范围和实际数量
                return f"E{min_ep:02d}-E{max_ep:02d}({total_count}集)"