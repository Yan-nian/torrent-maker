#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Torrent Maker - 单文件版本
基于 mktorrent 的半自动化种子制作工具

使用方法：
    python torrent_maker.py

作者：Torrent Maker Team
许可证：MIT
版本：1.0.0
"""

import os
import sys
import json
import subprocess
import shutil
from datetime import datetime
from difflib import SequenceMatcher
from typing import List, Dict, Any, Tuple, Optional
import tempfile


# ================== 配置管理器 ==================
class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.torrent_maker")
        self.settings_path = os.path.join(self.config_dir, "settings.json")
        self.trackers_path = os.path.join(self.config_dir, "trackers.txt")
        
        self.ensure_config_files()
        self.settings = self.load_settings()
        self.trackers = self.load_trackers()

    def ensure_config_files(self):
        """确保配置文件和目录存在"""
        # 确保配置目录存在
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(self.settings_path):
            self.create_default_settings()
        
        if not os.path.exists(self.trackers_path):
            self.create_default_trackers()

    def create_default_settings(self):
        """创建默认设置文件"""
        default_settings = {
            "resource_folder": os.path.expanduser("~/Downloads"),
            "output_folder": os.path.expanduser("~/Desktop/torrents"),
            "file_search_tolerance": 60,
            "max_search_results": 10,
            "auto_create_output_dir": True
        }
        
        with open(self.settings_path, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=4)

    def create_default_trackers(self):
        """创建默认 tracker 文件"""
        default_trackers = [
            "udp://tracker.openbittorrent.com:80",
            "udp://tracker.opentrackr.org:1337/announce",
            "udp://exodus.desync.com:6969/announce",
            "udp://tracker.torrent.eu.org:451/announce"
        ]
        
        with open(self.trackers_path, 'w', encoding='utf-8') as f:
            f.write("# BitTorrent Tracker 列表\n")
            f.write("# 每行一个 tracker URL，以 # 开头的行为注释\n\n")
            for tracker in default_trackers:
                f.write(f"{tracker}\n")

    def load_settings(self) -> Dict[str, Any]:
        """加载设置"""
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # 展开用户目录路径
                for key in ['resource_folder', 'output_folder']:
                    if key in settings:
                        settings[key] = os.path.expanduser(settings[key])
                return settings
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def load_trackers(self) -> List[str]:
        """加载 tracker 列表"""
        try:
            with open(self.trackers_path, 'r', encoding='utf-8') as f:
                trackers = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        trackers.append(line)
                return trackers
        except FileNotFoundError:
            return []

    def get_resource_folder(self) -> str:
        """获取资源文件夹路径"""
        return self.settings.get('resource_folder', os.path.expanduser("~/Downloads"))

    def set_resource_folder(self, path: str):
        """设置资源文件夹路径"""
        expanded_path = os.path.expanduser(path)
        self.settings['resource_folder'] = expanded_path
        self.save_settings()

    def get_output_folder(self) -> str:
        """获取输出文件夹路径"""
        return self.settings.get('output_folder', os.path.expanduser("~/Desktop/torrents"))

    def set_output_folder(self, path: str):
        """设置输出文件夹路径"""
        expanded_path = os.path.expanduser(path)
        self.settings['output_folder'] = expanded_path
        self.save_settings()

    def get_trackers(self) -> List[str]:
        """获取 tracker 列表"""
        return self.trackers.copy()

    def add_tracker(self, tracker_url: str):
        """添加新的 tracker"""
        if tracker_url not in self.trackers:
            self.trackers.append(tracker_url)
            self.save_trackers()
            return True
        return False

    def remove_tracker(self, tracker_url: str):
        """移除 tracker"""
        if tracker_url in self.trackers:
            self.trackers.remove(tracker_url)
            self.save_trackers()
            return True
        return False

    def save_settings(self):
        """保存设置"""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存设置时出错: {e}")

    def save_trackers(self):
        """保存 tracker 列表"""
        try:
            with open(self.trackers_path, 'w', encoding='utf-8') as f:
                f.write("# BitTorrent Tracker 列表\n")
                f.write("# 每行一个 tracker URL，以 # 开头的行为注释\n\n")
                for tracker in self.trackers:
                    f.write(f"{tracker}\n")
        except Exception as e:
            print(f"保存 tracker 时出错: {e}")


# ================== 文件匹配器 ==================
class FileMatcher:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory
        self.min_score = 0.6

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
            
            if similarity_score >= self.min_score:
                matches.append((folder_path, similarity_score))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:10]

    def get_folder_info(self, folder_path: str) -> Dict[str, Any]:
        """获取文件夹详细信息"""
        if not os.path.exists(folder_path):
            return {'exists': False}
        
        total_files = 0
        total_size = 0
        
        try:
            for root, dirs, files in os.walk(folder_path):
                total_files += len(files)
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except (OSError, IOError):
                        pass
        except PermissionError:
            return {'exists': True, 'readable': False}
        
        # 格式化大小
        size_str = self.format_size(total_size)
        
        return {
            'exists': True,
            'readable': True,
            'total_files': total_files,
            'total_size': total_size,
            'size_str': size_str
        }

    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def match_folders(self, search_name: str) -> List[Dict[str, Any]]:
        """搜索并返回匹配的文件夹信息"""
        matches = self.fuzzy_search(search_name)
        result = []
        
        for folder_path, score in matches:
            folder_info = self.get_folder_info(folder_path)
            if folder_info['exists']:
                # 获取剧集信息
                episode_info = self.extract_episode_info_simple(folder_path)
                season_info = episode_info.get('season_info', '')
                total_episodes = episode_info.get('total_episodes', 0)
                
                result.append({
                    'path': folder_path,
                    'name': os.path.basename(folder_path),
                    'score': int(score * 100),
                    'file_count': folder_info.get('total_files', 0),
                    'size': folder_info.get('size_str', '未知'),
                    'readable': folder_info.get('readable', True),
                    'episodes': season_info,
                    'video_count': total_episodes
                })
        
        return result

    def is_video_file(self, filename: str) -> bool:
        """判断是否为视频文件"""
        video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.m4v', '.ts', '.m2ts'}
        return any(filename.lower().endswith(ext) for ext in video_extensions)

    def extract_episode_info_simple(self, folder_path: str) -> Dict[str, Any]:
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
        
        # 生成摘要信息
        season_info = self.generate_season_summary(episodes, seasons)
        
        return {
            'episodes': episodes,
            'season_info': season_info,
            'total_episodes': len(episodes)
        }

    def parse_episode_from_filename(self, filename: str) -> Dict[str, Any]:
        """从文件名解析剧集信息"""
        import re
        
        # 常见的剧集命名模式
        patterns = [
            # Season Episode 格式: S01E01, S1E1, s01e01
            (r'[Ss](\d{1,2})[Ee](\d{1,3})', 'season_episode'),
            # 单独 Episode 格式: E01, EP01, ep01
            (r'(?:^|[^a-zA-Z])[Ee][Pp]?(\d{1,3})(?:[^0-9]|$)', 'episode_only'),
            # 数字格式: 101, 1001 (第一个数字是季，后面是集)
            (r'(?:^|[^0-9])(\d)(\d{2})(?:[^0-9]|$)', 'season_episode_concat'),
            # 纯数字格式: 01, 02 等
            (r'(?:^|[^0-9])(\d{1,3})(?:[^0-9]|$)', 'episode_only'),
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
                elif pattern_type == 'season_episode_concat':
                    season = int(match.group(1))
                    episode = int(match.group(2))
                    return {
                        'season': season,
                        'episode': episode,
                        'filename': filename,
                        'pattern_type': pattern_type
                    }
                elif pattern_type == 'episode_only':
                    episode = int(match.group(1))
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
        for i in range(1, len(episode_numbers)):
            if episode_numbers[i] != episode_numbers[i-1] + 1:
                is_continuous = False
                break
        
        if is_continuous:
            # 连续集数，使用范围格式
            return f"E{episode_numbers[0]:02d}-E{episode_numbers[-1]:02d}"
        else:
            # 有断集，检查断集的情况
            min_ep = episode_numbers[0]
            max_ep = episode_numbers[-1]
            total_count = len(episode_numbers)
            
            if total_count <= 3:
                # 集数较少，直接列出所有集数
                episode_list = [f"E{ep:02d}" for ep in episode_numbers]
                return "+".join(episode_list)
            else:
                # 集数较多但有断集，显示范围和实际数量
                return f"E{min_ep:02d}-E{max_ep:02d}({total_count}集)"

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
            details.append(f"第{season}季详细信息:")
            
            for ep in season_episodes:
                if ep['episode']:
                    details.append(f"  S{season:02d}E{ep['episode']:02d}: {ep['filename']}")
                else:
                    details.append(f"  第{season}季: {ep['filename']}")
        
        # 显示没有季度信息的剧集
        if no_season_episodes:
            details.append("其他剧集:")
            for ep in sorted(no_season_episodes, key=lambda x: x['episode'] or 0):
                if ep['episode']:
                    details.append(f"  E{ep['episode']:02d}: {ep['filename']}")
                else:
                    details.append(f"  {ep['filename']}")
        
        return '\n'.join(details) if details else "无剧集信息"


# ================== 种子创建器 ==================
class TorrentCreator:
    def __init__(self, tracker_links: List[str], output_dir: str):
        self.tracker_links = tracker_links
        self.output_dir = output_dir

    def check_mktorrent(self) -> bool:
        """检查系统是否安装了 mktorrent"""
        return shutil.which('mktorrent') is not None

    def ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_torrent(self, source_path: str, custom_name: str = None) -> Optional[str]:
        """创建种子文件"""
        if not self.check_mktorrent():
            return None

        if not os.path.exists(source_path):
            return None

        self.ensure_output_dir()
        
        # 生成种子文件名
        if custom_name:
            torrent_name = custom_name
        else:
            torrent_name = os.path.basename(source_path)
        
        # 清理文件名
        torrent_name = self.sanitize_filename(torrent_name)
        
        # 添加时间戳避免重名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"{torrent_name}_{timestamp}.torrent")

        # 构建 mktorrent 命令
        command = ['mktorrent']
        
        # 添加 tracker 链接
        for tracker in self.tracker_links:
            command.extend(['-a', tracker])
        
        # 设置输出文件
        command.extend(['-o', output_file])
        
        # 设置注释
        command.extend(['-c', f"Created by Torrent Maker on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
        
        # 添加源路径
        command.append(source_path)

        try:
            subprocess.run(command, capture_output=True, text=True, check=True)
            return output_file
        except subprocess.CalledProcessError:
            return None

    def sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        import re
        unsafe_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(unsafe_chars, '_', filename)
        return sanitized.strip(' .')


# ================== 主应用程序 ==================
class TorrentMakerApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.running = True

    def display_banner(self):
        """显示程序横幅"""
        print("=" * 60)
        print("           🎬 种子制作工具 Torrent Maker 🎬")
        print("=" * 60)
        print("   基于 mktorrent 的半自动化种子制作工具")
        print("   配置文件位置：" + self.config_manager.config_dir)
        print("=" * 60)

    def display_menu(self):
        """显示主菜单"""
        print("\n🔧 请选择操作:")
        print("1. 🔍 搜索并制作种子")
        print("2. ⚙️  查看当前配置")
        print("3. 📁 设置资源文件夹")
        print("4. 📂 设置输出文件夹")
        print("5. 🌐 管理 Tracker")
        print("6. 💫 快速制种（直接输入路径）")
        print("7. ❓ 帮助")
        print("0. 🚪 退出")
        print("-" * 40)

    def check_requirements(self) -> bool:
        """检查系统要求"""
        # 检查 mktorrent
        if not shutil.which('mktorrent'):
            print("❌ 未找到 mktorrent 工具！")
            print("\n安装方法：")
            print("macOS: brew install mktorrent")
            print("Ubuntu/Debian: sudo apt-get install mktorrent")
            print("CentOS/RHEL: sudo yum install mktorrent")
            return False
        
        # 检查资源文件夹
        resource_folder = self.config_manager.get_resource_folder()
        if not os.path.exists(resource_folder):
            print(f"⚠️  资源文件夹不存在: {resource_folder}")
            print("请先设置正确的资源文件夹（选项 3）")
        
        return True

    def search_and_create_torrent(self):
        """搜索文件夹并创建种子"""
        resource_folder = self.config_manager.get_resource_folder()
        
        if not os.path.exists(resource_folder):
            print(f"❌ 资源文件夹不存在: {resource_folder}")
            print("请先设置正确的资源文件夹路径（选项 3）")
            return

        print(f"\n📁 搜索目录: {resource_folder}")
        
        # 获取用户输入
        series_name = input("\n🎭 请输入影视剧名称（支持模糊搜索）: ").strip()
        
        if not series_name:
            print("❌ 请输入有效的名称")
            return

        print(f"\n🔍 正在搜索包含 '{series_name}' 的文件夹...")
        
        # 搜索匹配的文件夹
        file_matcher = FileMatcher(resource_folder)
        matched_folders = file_matcher.match_folders(series_name)

        if not matched_folders:
            print("❌ 未找到匹配的文件夹")
            return

        # 显示搜索结果
        print(f"\n✅ 找到 {len(matched_folders)} 个匹配的文件夹:")
        print("-" * 80)
        
        for i, folder_info in enumerate(matched_folders, 1):
            status = "✅" if folder_info['readable'] else "⚠️ "
            print(f"{i:2d}. {status} 📂 {folder_info['name']}")
            print(f"     📍 路径: {folder_info['path']}")
            print(f"     📊 匹配度: {folder_info['score']}%")
            print(f"     📄 文件数: {folder_info['file_count']}")
            print(f"     💾 大小: {folder_info['size']}")
            # 显示剧集信息
            if folder_info.get('episodes') and folder_info.get('video_count', 0) > 0:
                print(f"     🎬 剧集: {folder_info['episodes']}")
            print("-" * 80)

        # 让用户选择文件夹
        while True:
            try:
                choice = input(f"\n请选择要制作种子的文件夹 (1-{len(matched_folders)}) 或输入:\n"
                             f"  'd数字' 查看详细剧集列表 (如 d1)\n"
                             f"  '0' 返回主菜单\n"
                             f"选择: ").strip().lower()
                
                if choice == '0':
                    return
                elif choice.startswith('d') and len(choice) > 1:
                    # 显示详细剧集列表
                    try:
                        folder_index = int(choice[1:]) - 1
                        if 0 <= folder_index < len(matched_folders):
                            folder_info = matched_folders[folder_index]
                            self.show_detailed_episodes(folder_info)
                        else:
                            print(f"❌ 请输入 d1-d{len(matched_folders)} 之间的选项")
                    except ValueError:
                        print("❌ 请输入有效的选项格式，如 d1, d2 等")
                    continue
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(matched_folders):
                    selected_folder = matched_folders[choice_num - 1]
                    break
                else:
                    print(f"❌ 请输入 1-{len(matched_folders)} 之间的数字")
            except ValueError:
                print("❌ 请输入有效的数字")

        # 确认选择
        print(f"\n✅ 已选择: {selected_folder['name']}")
        print(f"📍 路径: {selected_folder['path']}")
        
        confirm = input("是否确认制作种子? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("❌ 取消制作种子")
            return

        # 创建种子
        self.create_torrent_file(selected_folder['path'], selected_folder['name'])

    def quick_create_torrent(self):
        """快速制种 - 直接输入路径"""
        print("\n💫 快速制种模式")
        folder_path = input("请输入要制种的文件夹完整路径: ").strip()
        
        if not folder_path:
            print("❌ 路径不能为空")
            return
        
        # 展开路径
        folder_path = os.path.expanduser(folder_path)
        
        if not os.path.exists(folder_path):
            print(f"❌ 路径不存在: {folder_path}")
            return
        
        if not os.path.isdir(folder_path):
            print(f"❌ 不是有效的文件夹: {folder_path}")
            return
        
        folder_name = os.path.basename(folder_path)
        print(f"\n📂 文件夹: {folder_name}")
        print(f"📍 路径: {folder_path}")
        
        # 获取文件夹信息
        file_matcher = FileMatcher(os.path.dirname(folder_path))
        folder_info = file_matcher.get_folder_info(folder_path)
        
        if folder_info['exists']:
            print(f"📄 文件数: {folder_info.get('total_files', '未知')}")
            print(f"💾 大小: {folder_info.get('size_str', '未知')}")
        
        confirm = input("\n是否确认制作种子? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("❌ 取消制作种子")
            return
        
        self.create_torrent_file(folder_path, folder_name)

    def show_detailed_episodes(self, folder_info):
        """显示文件夹的详细剧集信息"""
        print(f"\n🎭 详细剧集信息: {folder_info['name']}")
        print("=" * 80)
        
        file_matcher = FileMatcher(self.config_manager.get_resource_folder())
        detailed_episodes = file_matcher.get_folder_episodes_detail(folder_info['path'])
        
        print(f"📍 路径: {folder_info['path']}")
        print(f"🎬 剧集摘要: {folder_info.get('episodes', '无剧集信息')}")
        print(f"📊 总集数: {folder_info.get('video_count', 0)}集")
        print("\n📋 详细集数列表:")
        print(detailed_episodes)
        print("=" * 80)
        
        input("\n按回车键返回...")

    def create_torrent_file(self, folder_path: str, folder_name: str):
        """创建种子文件"""
        trackers = self.config_manager.get_trackers()
        output_dir = self.config_manager.get_output_folder()
        
        if not trackers:
            print("❌ 没有配置 Tracker，无法创建种子")
            print("请先添加 Tracker（选项 5）")
            return

        print(f"\n🛠️  开始制作种子...")
        print(f"📁 源文件夹: {folder_path}")
        print(f"📂 输出目录: {output_dir}")
        print(f"🌐 使用 {len(trackers)} 个 Tracker")

        torrent_creator = TorrentCreator(trackers, output_dir)
        torrent_file = torrent_creator.create_torrent(folder_path, folder_name)

        if torrent_file:
            print(f"\n🎉 种子制作成功!")
            print(f"📂 种子文件: {torrent_file}")
            
            # 显示种子文件大小
            if os.path.exists(torrent_file):
                size = os.path.getsize(torrent_file)
                print(f"📏 文件大小: {size} bytes")
        else:
            print("\n❌ 种子制作失败")
            print("请检查：")
            print("1. mktorrent 是否正确安装")
            print("2. 源文件夹是否可访问")
            print("3. 输出目录是否有写入权限")

    def manage_config(self):
        """管理配置"""
        print("\n=== 当前配置 ===")
        print(f"📁 资源文件夹: {self.config_manager.get_resource_folder()}")
        print(f"📂 输出文件夹: {self.config_manager.get_output_folder()}")
        print(f"🌐 Tracker 数量: {len(self.config_manager.get_trackers())}")
        
        trackers = self.config_manager.get_trackers()
        if trackers:
            print("Tracker 列表:")
            for i, tracker in enumerate(trackers, 1):
                print(f"  {i}. {tracker}")
        else:
            print("⚠️  暂无 Tracker 配置")
        
        print("=" * 40)

    def set_resource_folder(self):
        """设置资源文件夹"""
        current_folder = self.config_manager.get_resource_folder()
        print(f"\n📁 当前资源文件夹: {current_folder}")
        
        new_folder = input("请输入新的资源文件夹路径 (留空保持不变): ").strip()
        
        if new_folder:
            expanded_path = os.path.expanduser(new_folder)
            if os.path.exists(expanded_path):
                self.config_manager.set_resource_folder(expanded_path)
                print(f"✅ 资源文件夹已设置为: {expanded_path}")
            else:
                print(f"❌ 路径不存在: {expanded_path}")
        else:
            print("⚡ 路径未更改")

    def set_output_folder(self):
        """设置输出文件夹"""
        current_folder = self.config_manager.get_output_folder()
        print(f"\n📂 当前输出文件夹: {current_folder}")
        
        new_folder = input("请输入新的输出文件夹路径 (留空保持不变): ").strip()
        
        if new_folder:
            expanded_path = os.path.expanduser(new_folder)
            self.config_manager.set_output_folder(expanded_path)
            
            try:
                os.makedirs(expanded_path, exist_ok=True)
                print(f"✅ 输出文件夹设置成功: {expanded_path}")
            except OSError as e:
                print(f"⚠️  输出文件夹设置成功，但创建失败: {e}")
        else:
            print("⚡ 路径未更改")

    def manage_trackers(self):
        """管理 Tracker"""
        while True:
            print("\n🌐 Tracker 管理")
            print("1. 📋 查看当前 Tracker")
            print("2. ➕ 添加新 Tracker")
            print("3. ➖ 删除 Tracker")
            print("0. 🔙 返回主菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.show_trackers()
            elif choice == '2':
                self.add_tracker()
            elif choice == '3':
                self.remove_tracker()
            else:
                print("❌ 无效选择")

    def show_trackers(self):
        """显示当前 Tracker"""
        trackers = self.config_manager.get_trackers()
        if not trackers:
            print("❌ 暂无配置的 Tracker")
            return
        
        print(f"\n📋 当前 Tracker 列表 ({len(trackers)} 个):")
        for i, tracker in enumerate(trackers, 1):
            print(f"  {i:2d}. {tracker}")

    def add_tracker(self):
        """添加新 Tracker"""
        tracker_url = input("\n🌐 请输入新的 Tracker URL: ").strip()
        if tracker_url:
            if self.config_manager.add_tracker(tracker_url):
                print(f"✅ 已添加 Tracker: {tracker_url}")
            else:
                print(f"⚠️  Tracker 已存在: {tracker_url}")
        else:
            print("❌ 请输入有效的 URL")

    def remove_tracker(self):
        """删除 Tracker"""
        trackers = self.config_manager.get_trackers()
        if not trackers:
            print("❌ 暂无 Tracker 可删除")
            return
        
        self.show_trackers()
        
        try:
            choice = int(input(f"\n请选择要删除的 Tracker (1-{len(trackers)}): "))
            if 1 <= choice <= len(trackers):
                tracker_to_remove = trackers[choice - 1]
                if self.config_manager.remove_tracker(tracker_to_remove):
                    print(f"✅ 已删除 Tracker: {tracker_to_remove}")
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效数字")

    def show_help(self):
        """显示帮助信息"""
        print("\n❓ 帮助信息")
        print("=" * 50)
        print("1. 🔍 搜索并制作种子:")
        print("   - 输入影视剧名称进行模糊搜索")
        print("   - 选择匹配的文件夹")
        print("   - 自动创建种子文件")
        print()
        print("2. 💫 快速制种:")
        print("   - 直接输入完整文件夹路径")
        print("   - 跳过搜索步骤，快速制作种子")
        print()
        print("3. ⚙️ 配置管理:")
        print("   - 设置影视剧资源存放的文件夹")
        print("   - 设置种子文件输出文件夹")
        print("   - 管理 BitTorrent Tracker 服务器")
        print()
        print("4. 📋 系统要求:")
        print("   - 需要安装 mktorrent 工具")
        print("   - macOS: brew install mktorrent")
        print("   - Ubuntu: sudo apt-get install mktorrent")
        print()
        print("5. 📁 配置文件位置:")
        print(f"   - {self.config_manager.config_dir}")
        print("=" * 50)

    def run(self):
        """运行主程序"""
        self.display_banner()
        
        # 检查系统要求
        if not self.check_requirements():
            input("\n按回车键退出...")
            return

        while self.running:
            try:
                self.display_menu()
                choice = input("请选择操作 (0-7): ").strip()
                
                if choice == '0':
                    print("\n👋 感谢使用种子制作工具！")
                    self.running = False
                elif choice == '1':
                    self.search_and_create_torrent()
                elif choice == '2':
                    self.manage_config()
                elif choice == '3':
                    self.set_resource_folder()
                elif choice == '4':
                    self.set_output_folder()
                elif choice == '5':
                    self.manage_trackers()
                elif choice == '6':
                    self.quick_create_torrent()
                elif choice == '7':
                    self.show_help()
                else:
                    print("❌ 无效选择，请重新输入")
                    
            except KeyboardInterrupt:
                print("\n\n👋 程序被用户中断，再见！")
                self.running = False
            except Exception as e:
                print(f"\n❌ 发生未知错误: {e}")
                print("程序将继续运行...")


# ================== 主函数 ==================
def main():
    """主函数"""
    print("🎬 Torrent Maker - 单文件版本")
    print("基于 mktorrent 的半自动化种子制作工具")
    print("版本：1.0.0 | 许可证：MIT")
    print()
    
    app = TorrentMakerApp()
    app.run()


if __name__ == "__main__":
    main()
