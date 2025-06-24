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
        """检查文件是否为视频文件"""
        video_extensions = {
            '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
            '.webm', '.m4v', '.3gp', '.ogv', '.ts', '.m2ts'
        }
        _, ext = os.path.splitext(filename.lower())
        return ext in video_extensions

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
        """格式化集数范围，智能分组显示连续片段"""
        if not episode_numbers:
            return ""
        
        episode_numbers = sorted(set(episode_numbers))  # 去重并排序
        
        if len(episode_numbers) == 1:
            return f"E{episode_numbers[0]:02d}"
        
        # 检查是否完全连续
        is_fully_continuous = True
        for i in range(1, len(episode_numbers)):
            if episode_numbers[i] != episode_numbers[i-1] + 1:
                is_fully_continuous = False
                break
        
        if is_fully_continuous:
            # 完全连续，使用范围格式
            return f"E{episode_numbers[0]:02d}-E{episode_numbers[-1]:02d}"
        else:
            # 有断集，分组显示连续片段
            groups = []
            start = episode_numbers[0]
            end = episode_numbers[0]
            
            for i in range(1, len(episode_numbers)):
                if episode_numbers[i] == end + 1:
                    # 连续，扩展当前组
                    end = episode_numbers[i]
                else:
                    # 不连续，结束当前组，开始新组
                    if start == end:
                        groups.append(f"E{start:02d}")
                    else:
                        groups.append(f"E{start:02d}-E{end:02d}")
                    start = episode_numbers[i]
                    end = episode_numbers[i]
            
            # 添加最后一组
            if start == end:
                groups.append(f"E{start:02d}")
            else:
                groups.append(f"E{start:02d}-E{end:02d}")
            
            return ",".join(groups)

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
        print("1. 🔍 搜索并制作种子 (支持多选)  [s/search]")
        print("2. ⚙️  查看当前配置           [c/config]")
        print("3. 📁 设置资源文件夹          [r/resource]")
        print("4. 📂 设置输出文件夹          [o/output]")
        print("5. 🌐 管理 Tracker          [t/tracker]")
        print("6. 🎯 快速制种 (支持批量)      [q/quick]")
        print("7. 📋 查看最近制作的种子       [l/list]")
        print("8. ❓ 帮助                   [h/help]")
        print("0. 🚪 退出                   [exit/quit]")
        print("-" * 50)

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
        """搜索文件夹并创建种子 - 支持连续搜索和多选制种"""
        resource_folder = self.config_manager.get_resource_folder()
        
        if not os.path.exists(resource_folder):
            print(f"❌ 资源文件夹不存在: {resource_folder}")
            print("请先设置正确的资源文件夹路径（选项 3）")
            return

        # 搜索循环 - 允许连续搜索
        while True:
            print(f"\n📁 当前搜索目录: {resource_folder}")
            
            # 获取用户输入
            series_name = input("\n🎭 请输入影视剧名称（支持模糊搜索，输入 'back' 返回主菜单）: ").strip()
            
            if series_name.lower() in ['back', 'b', '返回']:
                return
                
            if not series_name:
                print("❌ 请输入有效的影视剧名称")
                continue

            print(f"\n🔍 正在搜索包含 '{series_name}' 的文件夹...")
            
            # 搜索匹配的文件夹
            file_matcher = FileMatcher(resource_folder)
            matched_folders = file_matcher.match_folders(series_name)

            if not matched_folders:
                print("❌ 未找到匹配的文件夹")
                print("💡 提示：")
                print("   - 尝试使用更简单的关键词")
                print("   - 检查资源文件夹路径是否正确")
                print("   - 确认文件夹名称中包含您输入的关键词")
                
                retry = input("\n是否重新搜索? (Y/n): ").strip().lower()
                if retry in ['', 'y', 'yes', '是']:
                    continue
                else:
                    return

            # 显示搜索结果
            print(f"\n✅ 找到 {len(matched_folders)} 个匹配的文件夹:")
            print("=" * 80)
            
            for i, folder_info in enumerate(matched_folders, 1):
                print(f"{i:2d}. 📂 {folder_info['name']}")
                print(f"     📍 路径: {folder_info['path']}")
                print(f"     📊 匹配度: {folder_info['score']}%")
                print(f"     📄 文件数: {folder_info['file_count']}")
                print(f"     💾 大小: {folder_info['size']}")
                # 显示剧集信息
                if folder_info.get('episodes') and folder_info.get('video_count', 0) > 0:
                    print(f"     🎬 剧集: {folder_info['episodes']}")
                print("-" * 80)

            # 处理用户选择
            selected_folders = self.handle_folder_selection(matched_folders)
            
            if selected_folders is None:  # 用户选择返回主菜单
                return
            elif selected_folders == 'continue_search':  # 用户选择继续搜索
                continue
            elif selected_folders:  # 用户选择了文件夹
                # 处理制种
                self.process_selected_folders(selected_folders)
                
                # 询问是否继续搜索
                print("\n" + "=" * 60)
                next_action = input("选择下一步操作:\n"
                                  "  's' 或 'search' - 继续搜索其他内容\n"
                                  "  'm' 或 'menu' - 返回主菜单\n"
                                  "选择: ").strip().lower()
                
                if next_action in ['s', 'search', '搜索']:
                    continue
                else:
                    return

    def handle_folder_selection(self, matched_folders):
        """处理文件夹选择 - 支持单选和多选"""
        while True:
            print(f"\n📋 选择操作:")
            print(f"  数字 (1-{len(matched_folders)}) - 选择单个文件夹制种")
            print(f"  多个数字用逗号分隔 (如: 1,3,5) - 批量制种")
            print(f"  'a' - 查看所有匹配项详细信息")
            print(f"  'd数字' - 查看详细剧集列表 (如: d1)")
            print(f"  's' - 继续搜索其他内容")
            print(f"  '0' - 返回主菜单")
            
            choice_input = input("选择: ").strip().lower()
            
            if choice_input == '0':
                return None
            elif choice_input == 's':
                return 'continue_search'
            elif choice_input == 'a':
                self.show_detailed_folder_info(matched_folders)
                continue
            elif choice_input.startswith('d') and len(choice_input) > 1:
                try:
                    folder_index = int(choice_input[1:]) - 1
                    if 0 <= folder_index < len(matched_folders):
                        folder_info = matched_folders[folder_index]
                        self.show_detailed_episodes(folder_info)
                    else:
                        print(f"❌ 请输入 d1-d{len(matched_folders)} 之间的选项")
                except ValueError:
                    print("❌ 请输入有效的选项格式，如 d1, d2 等")
                continue
            
            # 处理数字选择（单选或多选）
            try:
                if ',' in choice_input:
                    # 多选模式
                    indices = [int(x.strip()) for x in choice_input.split(',')]
                    selected_folders = []
                    
                    for idx in indices:
                        if 1 <= idx <= len(matched_folders):
                            selected_folders.append(matched_folders[idx - 1])
                        else:
                            print(f"❌ 索引 {idx} 超出范围 (1-{len(matched_folders)})")
                            return self.handle_folder_selection(matched_folders)
                    
                    if selected_folders:
                        print(f"\n✅ 已选择 {len(selected_folders)} 个文件夹进行批量制种:")
                        for i, folder in enumerate(selected_folders, 1):
                            print(f"  {i}. {folder['name']}")
                        
                        confirm = input(f"\n确认批量制作这 {len(selected_folders)} 个种子? (Y/n): ").strip().lower()
                        if confirm in ['', 'y', 'yes', '是']:
                            return selected_folders
                        else:
                            print("❌ 取消批量制种")
                            continue
                else:
                    # 单选模式
                    choice_num = int(choice_input)
                    if 1 <= choice_num <= len(matched_folders):
                        selected_folder = matched_folders[choice_num - 1]
                        return self.handle_single_folder_actions(selected_folder)
                    else:
                        print(f"❌ 请输入 1-{len(matched_folders)} 之间的数字")
                        
            except ValueError:
                print("❌ 请输入有效的选项")

    def handle_single_folder_actions(self, selected_folder):
        """处理单个文件夹的操作选择"""
        print(f"\n✅ 已选择: {selected_folder['name']}")
        print(f"📍 路径: {selected_folder['path']}")
        
        while True:
            print("\n请选择操作:")
            print("1. 🎬 立即制作种子")
            print("2. 📁 查看文件夹详细内容")
            print("3. 🔙 重新选择文件夹")
            
            action = input("选择 (1-3): ").strip()
            
            if action == '1':
                confirm = input("确认制作种子? (Y/n): ").strip().lower()
                if confirm in ['', 'y', 'yes', '是']:
                    return [selected_folder]  # 返回列表格式以统一处理
                else:
                    print("❌ 取消制作种子")
                    continue
            elif action == '2':
                self.show_folder_contents(selected_folder['path'])
                if input("\n查看完毕，是否制作种子? (y/N): ").strip().lower() in ['y', 'yes', '是']:
                    return [selected_folder]
                else:
                    continue
            elif action == '3':
                return 'reselect'
            else:
                print("❌ 请输入 1-3 之间的数字")

    def process_selected_folders(self, selected_folders):
        """处理选中的文件夹制种"""
        if not selected_folders:
            return
            
        trackers = self.config_manager.get_trackers()
        if not trackers:
            print("❌ 没有配置 Tracker，无法创建种子")
            print("请先添加 Tracker（选项 5）")
            return

        output_dir = self.config_manager.get_output_folder()
        torrent_creator = TorrentCreator(trackers, output_dir)
        
        print(f"\n🛠️  开始批量制作 {len(selected_folders)} 个种子...")
        print(f"📂 输出目录: {output_dir}")
        print(f"🌐 使用 {len(trackers)} 个 Tracker")
        print("=" * 60)
        
        successful_count = 0
        failed_count = 0
        
        for i, folder_info in enumerate(selected_folders, 1):
            print(f"\n📦 正在处理 ({i}/{len(selected_folders)}): {folder_info['name']}")
            print(f"📁 路径: {folder_info['path']}")
            
            torrent_file = torrent_creator.create_torrent(folder_info['path'], folder_info['name'])
            
            if torrent_file:
                print(f"✅ 种子制作成功: {os.path.basename(torrent_file)}")
                successful_count += 1
            else:
                print(f"❌ 种子制作失败: {folder_info['name']}")
                failed_count += 1
        
        # 显示批量制种结果
        print("\n" + "=" * 60)
        print(f"🎉 批量制种完成!")
        print(f"✅ 成功: {successful_count} 个")
        if failed_count > 0:
            print(f"❌ 失败: {failed_count} 个")
        print(f"📂 种子保存位置: {output_dir}")
        print("=" * 60)

    def quick_create_torrent(self):
        """快速制种 - 直接输入路径，支持多个路径"""
        print("\n🎯 快速制种模式")
        print("直接输入文件夹路径来快速制作种子")
        print("💡 支持多个路径，用英文分号(;)分隔")
        print("-" * 40)
        
        while True:
            folder_input = input("请输入文件夹完整路径 (多个路径用;分隔，输入'back'返回): ").strip()
            
            if folder_input.lower() in ['back', 'b', '返回']:
                return
            
            if not folder_input:
                print("❌ 请输入有效的文件夹路径")
                continue
                
            # 处理多个路径的情况
            folder_paths = [path.strip().strip('"\'') for path in folder_input.split(';')]
            valid_folders = []
            
            print(f"\n🔍 检查 {len(folder_paths)} 个路径...")
            
            for i, folder_path in enumerate(folder_paths, 1):
                # 展开路径
                folder_path = os.path.expanduser(folder_path)
                
                print(f"\n{i}. 检查路径: {folder_path}")
                
                if not os.path.exists(folder_path):
                    print(f"   ❌ 文件夹不存在")
                    continue
                
                if not os.path.isdir(folder_path):
                    print(f"   ❌ 不是文件夹")
                    continue
                
                # 显示文件夹信息
                folder_name = os.path.basename(folder_path)
                try:
                    # 获取文件夹信息
                    total_files = 0
                    video_files = 0
                    total_size = 0
                    
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                size = os.path.getsize(file_path)
                                total_size += size
                                total_files += 1
                                
                                # 检查是否为视频文件
                                if any(file.lower().endswith(ext) for ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']):
                                    video_files += 1
                            except:
                                continue
                    
                    # 格式化大小
                    if total_size < 1024:
                        size_str = f"{total_size} B"
                    elif total_size < 1024**2:
                        size_str = f"{total_size/1024:.1f} KB"
                    elif total_size < 1024**3:
                        size_str = f"{total_size/(1024**2):.1f} MB"
                    else:
                        size_str = f"{total_size/(1024**3):.1f} GB"
                    
                    print(f"   ✅ 有效文件夹: {folder_name}")
                    print(f"   � 总文件数: {total_files}")
                    print(f"   🎬 视频文件数: {video_files}")
                    print(f"   💾 大小: {size_str}")
                    
                    valid_folders.append({
                        'name': folder_name,
                        'path': folder_path,
                        'info': {
                            'total_files': total_files,
                            'video_files': video_files,
                            'total_size_formatted': size_str
                        }
                    })
                except Exception as e:
                    print(f"   ⚠️  获取文件夹信息失败: {e}")
                    valid_folders.append({
                        'name': folder_name,
                        'path': folder_path,
                        'info': None
                    })
            
            if not valid_folders:
                print("\n❌ 没有找到有效的文件夹路径")
                retry = input("是否重新输入? (Y/n): ").strip().lower()
                if retry in ['', 'y', 'yes', '是']:
                    continue
                else:
                    return
            
            # 显示汇总信息
            print(f"\n� 找到 {len(valid_folders)} 个有效文件夹:")
            for i, folder in enumerate(valid_folders, 1):
                print(f"  {i}. {folder['name']}")
            
            # 询问是否制作种子
            if len(valid_folders) == 1:
                confirm = input(f"\n是否为 '{valid_folders[0]['name']}' 制作种子? (Y/n): ").strip().lower()
            else:
                confirm = input(f"\n是否为这 {len(valid_folders)} 个文件夹批量制作种子? (Y/n): ").strip().lower()
            
            if confirm in ['', 'y', 'yes', '是', 'ok']:
                # 使用统一的批量制种方法
                self.process_selected_folders(valid_folders)
                
                # 询问是否继续
                next_action = input("\n继续快速制种? (Y/n): ").strip().lower()
                if next_action in ['', 'y', 'yes', '是']:
                    continue
                else:
                    return
            else:
                print("❌ 取消制作种子")
                retry = input("是否重新输入路径? (Y/n): ").strip().lower()
                if retry in ['', 'y', 'yes', '是']:
                    continue
                else:
                    return

    def show_detailed_folder_info(self, folders):
        """显示文件夹的详细信息"""
        print("\n📊 详细信息:")
        print("=" * 100)
        
        for i, folder_info in enumerate(folders, 1):
            # 获取详细信息
            total_files = 0
            video_files = 0
            total_size = 0
            readable = True
            
            try:
                for root, dirs, files in os.walk(folder_info['path']):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            size = os.path.getsize(file_path)
                            total_size += size
                            total_files += 1
                            
                            # 检查是否为视频文件
                            if any(file.lower().endswith(ext) for ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']):
                                video_files += 1
                        except:
                            continue
            except:
                readable = False
            
            # 格式化大小
            if total_size < 1024:
                size_str = f"{total_size} B"
            elif total_size < 1024**2:
                size_str = f"{total_size/1024:.1f} KB"
            elif total_size < 1024**3:
                size_str = f"{total_size/(1024**2):.1f} MB"
            else:
                size_str = f"{total_size/(1024**3):.1f} GB"
            
            print(f"{i:2d}. 📂 {folder_info['name']}")
            print(f"     📍 完整路径: {folder_info['path']}")
            print(f"     📊 匹配度: {folder_info['score']}%")
            print(f"     📄 总文件数: {total_files}")
            print(f"     🎬 视频文件数: {video_files}")
            print(f"     💾 文件夹大小: {size_str}")
            print(f"     🔒 可读取: {'是' if readable else '否'}")
            
            # 显示剧集信息
            if folder_info.get('episodes') and folder_info.get('video_count', 0) > 0:
                print(f"     🎭 剧集信息: {folder_info['episodes']}")
                print(f"     📋 详细集数: 输入 'd{i}' 查看详细列表")
            
            print("-" * 100)

    def show_folder_contents(self, folder_path):
        """显示文件夹内容"""
        print(f"\n📁 查看文件夹内容: {os.path.basename(folder_path)}")
        print(f"📍 完整路径: {folder_path}")
        print("-" * 60)
        
        try:
            # 获取文件列表
            all_files = []
            video_files = []
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path)
                    file_size = os.path.getsize(file_path)
                    
                    all_files.append((relative_path, file_size))
                    
                    # 检查是否为视频文件
                    if any(file.lower().endswith(ext) for ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']):
                        video_files.append((relative_path, file_size))
            
            # 显示视频文件
            if video_files:
                print(f"🎬 视频文件 ({len(video_files)} 个):")
                video_files.sort()  # 按文件名排序
                
                for i, (file_path, file_size) in enumerate(video_files[:20], 1):  # 最多显示20个
                    # 格式化文件大小
                    if file_size < 1024**2:
                        size_str = f"{file_size/1024:.1f} KB"
                    elif file_size < 1024**3:
                        size_str = f"{file_size/(1024**2):.1f} MB"
                    else:
                        size_str = f"{file_size/(1024**3):.1f} GB"
                        
                    print(f"  {i:2d}. {file_path}")
                    print(f"       💾 {size_str}")
                
                if len(video_files) > 20:
                    print(f"       ... 还有 {len(video_files) - 20} 个视频文件")
            else:
                print("🎬 未找到视频文件")
            
            print()
            print(f"📊 统计信息:")
            print(f"   📄 总文件数: {len(all_files)}")
            print(f"   🎬 视频文件数: {len(video_files)}")
            
            total_size = sum(size for _, size in all_files)
            if total_size < 1024**3:
                size_str = f"{total_size/(1024**2):.1f} MB"
            else:
                size_str = f"{total_size/(1024**3):.1f} GB"
            print(f"   💾 总大小: {size_str}")
            
        except Exception as e:
            print(f"❌ 无法读取文件夹内容: {e}")

    def list_recent_torrents(self):
        """查看最近制作的种子"""
        print("\n📋 最近制作的种子文件")
        print("-" * 40)
        
        output_dir = self.config_manager.get_output_folder()
        
        if not os.path.exists(output_dir):
            print(f"❌ 输出文件夹不存在: {output_dir}")
            return
        
        # 获取所有 .torrent 文件
        torrent_files = []
        for file in os.listdir(output_dir):
            if file.endswith('.torrent'):
                file_path = os.path.join(output_dir, file)
                mtime = os.path.getmtime(file_path)
                torrent_files.append((file, file_path, mtime))
        
        if not torrent_files:
            print("📁 暂无种子文件")
            return
        
        # 按修改时间排序，最新的在前
        torrent_files.sort(key=lambda x: x[2], reverse=True)
        
        # 显示最近的10个种子文件
        from datetime import datetime
        print(f"📂 输出目录: {output_dir}")
        print(f"📊 共找到 {len(torrent_files)} 个种子文件")
        print()
        
        for i, (filename, filepath, mtime) in enumerate(torrent_files[:10], 1):
            modified_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            file_size = os.path.getsize(filepath)
            print(f"{i:2d}. 📄 {filename}")
            print(f"     🕒 {modified_time}")
            print(f"     💾 {file_size} bytes")
            print()
        
        if len(torrent_files) > 10:
            print(f"... 还有 {len(torrent_files) - 10} 个文件")
        
        # 询问是否打开输出文件夹
        if input("\n是否打开输出文件夹? (y/N): ").strip().lower() in ['y', 'yes', '是']:
            try:
                import subprocess
                import platform
                
                if platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", output_dir])
                elif platform.system() == "Windows":  # Windows
                    subprocess.run(["explorer", output_dir])
                else:  # Linux
                    subprocess.run(["xdg-open", output_dir])
                    
                print(f"✅ 已打开文件夹: {output_dir}")
            except Exception as e:
                print(f"❌ 无法打开文件夹: {e}")

    def show_help(self):
        """显示帮助信息"""
        print("\n❓ 帮助信息")
        print("=" * 60)
        print("🔍 1. 搜索并制作种子 [s/search]:")
        print("   - 输入影视剧名称进行智能模糊搜索")
        print("   - 查看匹配文件夹的详细信息")
        print("   - 🆕 支持多选制种：用逗号分隔选择多个文件夹 (如: 1,3,5)")
        print("   - 🆕 支持连续搜索：制种完成后可继续搜索其他内容")
        print("   - 预览文件夹内容后再决定是否制种")
        print()
        print("🎯 6. 快速制种 [q/quick]:")
        print("   - 直接输入或拖拽文件夹路径")
        print("   - 🆕 支持批量制种：用分号分隔多个路径 (如: path1;path2)")
        print("   - 跳过搜索步骤，快速制作种子")
        print()
        print("⚙️ 配置管理:")
        print("   - 📁 设置影视剧资源存放的文件夹")
        print("   - 📂 设置种子文件输出文件夹")
        print("   - 🌐 管理 BitTorrent Tracker 服务器")
        print("   - 📋 查看最近制作的种子文件")
        print()
        print("🎛️ 快捷键:")
        print("   s/search  - 搜索制种    q/quick   - 快速制种")
        print("   c/config  - 查看配置    l/list    - 最近种子")
        print("   r/resource- 资源目录    o/output  - 输出目录")
        print("   t/tracker - 管理tracker h/help    - 显示帮助")
        print("   exit/quit - 退出程序")
        print()
        print("🆕 新功能说明:")
        print("   📦 批量制种: 可一次选择多个文件夹批量制作种子")
        print("   🔄 连续搜索: 制种完成后无需返回主菜单即可继续搜索")
        print("   📊 进度显示: 批量制种时显示详细进度和结果统计")
        print()
        print("📋 系统要求:")
        print("   - 需要安装 mktorrent 工具")
        print("   - macOS: brew install mktorrent")
        print("   - Ubuntu: sudo apt-get install mktorrent")
        print()
        print("💡 使用技巧:")
        print("   - 支持文件夹拖拽到终端")
        print("   - 支持路径自动补全 (Tab键)")
        print("   - 支持相对路径和 ~ 家目录符号")
        print("   - 多选时可预览所有选中项再确认")
        print()
        print("📁 配置文件位置:")
        print(f"   - {self.config_manager.config_dir}")
        print("=" * 60)

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
                choice = input("请选择操作 (0-8 或快捷键): ").strip().lower()
                
                # 处理退出命令
                if choice in ['0', 'exit', 'quit']:
                    print("\n👋 感谢使用种子制作工具！")
                    self.running = False
                # 搜索并制作种子
                elif choice in ['1', 's', 'search']:
                    self.search_and_create_torrent()
                # 查看配置
                elif choice in ['2', 'c', 'config']:
                    self.manage_config()
                # 设置资源文件夹
                elif choice in ['3', 'r', 'resource']:
                    self.set_resource_folder()
                # 设置输出文件夹
                elif choice in ['4', 'o', 'output']:
                    self.set_output_folder()
                # 管理 Tracker
                elif choice in ['5', 't', 'tracker']:
                    self.manage_trackers()
                # 快速制种
                elif choice in ['6', 'q', 'quick']:
                    self.quick_create_torrent()
                # 查看最近种子
                elif choice in ['7', 'l', 'list']:
                    self.list_recent_torrents()
                # 帮助
                elif choice in ['8', 'h', 'help']:
                    self.show_help()
                else:
                    print("❌ 无效选择，请重新输入")
                    print("💡 提示：您可以输入数字 (0-8) 或使用快捷键")
                    
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
    print("版本：1.0.2 | 许可证：MIT")
    print()
    
    app = TorrentMakerApp()
    app.run()


if __name__ == "__main__":
    main()
