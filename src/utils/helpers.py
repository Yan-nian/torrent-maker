"""
辅助函数模块
提供各种实用的辅助函数
"""

import os
import re
import shutil
from typing import List, Optional, Dict, Any


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小为人类可读的格式
    
    Args:
        size_bytes: 文件大小（字节）
    
    Returns:
        格式化后的文件大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(size_bytes)
    i = 0
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除或替换不安全的字符
    
    Args:
        filename: 原始文件名
    
    Returns:
        清理后的安全文件名
    """
    # 移除或替换不安全的字符
    unsafe_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(unsafe_chars, '_', filename)
    
    # 移除前后空格和点
    sanitized = sanitized.strip(' .')
    
    # 确保文件名不为空
    if not sanitized:
        sanitized = "unnamed"
    
    return sanitized


def is_video_file(filename: str) -> bool:
    """
    检查文件是否为视频文件
    
    Args:
        filename: 文件名
    
    Returns:
        如果是视频文件返回 True，否则返回 False
    """
    video_extensions = {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
        '.webm', '.m4v', '.3gp', '.ogv', '.ts', '.m2ts'
    }
    
    _, ext = os.path.splitext(filename.lower())
    return ext in video_extensions


def count_video_files(directory: str) -> int:
    """
    统计目录中的视频文件数量
    
    Args:
        directory: 目录路径
    
    Returns:
        视频文件数量
    """
    if not os.path.exists(directory):
        return 0
    
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if is_video_file(file):
                count += 1
    
    return count


def check_command_available(command: str) -> bool:
    """
    检查系统中是否可用指定的命令
    
    Args:
        command: 命令名称
    
    Returns:
        如果命令可用返回 True，否则返回 False
    """
    return shutil.which(command) is not None


def validate_tracker_url(url: str) -> bool:
    """
    验证 Tracker URL 格式是否正确
    
    Args:
        url: Tracker URL
    
    Returns:
        如果 URL 格式正确返回 True，否则返回 False
    """
    # 简单的 URL 格式验证
    pattern = r'^(https?|udp)://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url, re.IGNORECASE))


def get_directory_info(directory: str) -> dict:
    """
    获取目录的详细信息
    
    Args:
        directory: 目录路径
    
    Returns:
        包含目录信息的字典
    """
    if not os.path.exists(directory):
        return {
            'exists': False,
            'total_files': 0,
            'video_files': 0,
            'total_size': 0,
            'readable': False
        }
    
    total_files = 0
    video_files = 0
    total_size = 0
    readable = True
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                total_files += 1
                file_path = os.path.join(root, file)
                
                if is_video_file(file):
                    video_files += 1
                
                try:
                    total_size += os.path.getsize(file_path)
                except (OSError, IOError):
                    pass  # 忽略无法访问的文件
    
    except PermissionError:
        readable = False
    
    return {
        'exists': True,
        'total_files': total_files,
        'video_files': video_files,
        'total_size': total_size,
        'total_size_formatted': format_file_size(total_size),
        'readable': readable
    }


def create_directory_if_not_exists(directory: str) -> bool:
    """
    如果目录不存在则创建它
    
    Args:
        directory: 目录路径
    
    Returns:
        如果目录创建成功或已存在返回 True，否则返回 False
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except OSError as e:
        print(f"创建目录失败: {e}")
        return False


def truncate_path(path: str, max_length: int = 50) -> str:
    """
    截断过长的路径，在中间添加省略号
    
    Args:
        path: 原始路径
        max_length: 最大长度
    
    Returns:
        截断后的路径
    """
    if len(path) <= max_length:
        return path
    
    # 计算两端保留的字符数
    side_length = (max_length - 3) // 2  # 减去省略号的长度
    
    return f"{path[:side_length]}...{path[-side_length:]}"


def get_relative_path(path: str, base_path: str) -> str:
    """
    获取相对于基础路径的相对路径
    
    Args:
        path: 完整路径
        base_path: 基础路径
    
    Returns:
        相对路径
    """
    try:
        return os.path.relpath(path, base_path)
    except ValueError:
        # 如果无法计算相对路径（例如在不同的驱动器上），返回原路径
        return path


# 兼容旧版本的函数

def fuzzy_search(folder_path, search_name):
    """
    旧版本兼容：简单的模糊搜索
    """
    import os
    from difflib import get_close_matches

    if not os.path.exists(folder_path):
        return []

    # Get all files in the folder
    files = os.listdir(folder_path)
    
    # Use get_close_matches to find files that closely match the search_name
    matches = get_close_matches(search_name, files, n=5, cutoff=0.5)
    
    return matches


def count_files_in_folder(folder_path):
    """
    旧版本兼容：计算文件夹中的文件数量
    """
    import os

    # Count the number of files in the folder
    if os.path.isdir(folder_path):
        return len(os.listdir(folder_path))
    return 0


def read_trackers(file_path):
    """
    旧版本兼容：读取 tracker 文件
    """
    trackers = []
    try:
        with open(file_path, 'r') as f:
            trackers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Tracker file not found: {file_path}")
    return trackers


def read_settings(file_path):
    """
    旧版本兼容：读取设置文件
    """
    import json

    try:
        with open(file_path, 'r') as f:
            settings = json.load(f)
            return settings
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading settings: {e}")
        return {}


def extract_episode_info(folder_path: str) -> Dict[str, Any]:
    """
    解析文件夹中的剧集信息
    
    Args:
        folder_path: 文件夹路径
    
    Returns:
        包含剧集信息的字典
    """
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return {'episodes': [], 'season_info': '', 'total_episodes': 0}
    
    episodes = []
    seasons = set()
    
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if is_video_file(file):
                    episode_info = parse_episode_from_filename(file)
                    if episode_info:
                        episodes.append(episode_info)
                        if episode_info['season']:
                            seasons.add(episode_info['season'])
    except (PermissionError, OSError):
        return {'episodes': [], 'season_info': '无法访问', 'total_episodes': 0}
    
    # 排序剧集
    episodes.sort(key=lambda x: (x['season'] or 0, x['episode'] or 0))
    
    # 生成季度信息摘要
    season_info = generate_season_summary(episodes, seasons)
    
    return {
        'episodes': episodes,
        'season_info': season_info,
        'total_episodes': len(episodes),
        'seasons': sorted(list(seasons)) if seasons else []
    }


def parse_episode_from_filename(filename: str) -> Optional[Dict[str, Any]]:
    """
    从文件名中解析剧集信息
    
    Args:
        filename: 文件名
    
    Returns:
        包含季度和集数信息的字典，如果无法解析则返回None
    """
    # 常见的剧集命名模式
    patterns = [
        # S01E01, S1E1, s01e01
        r'[Ss](\d{1,2})[Ee](\d{1,3})',
        # Season 1 Episode 01, Season.1.Episode.01
        r'[Ss]eason\s*(\d{1,2})\s*[Ee]pisode\s*(\d{1,3})',
        # 第一季第01集, 第1季第1集
        r'第(\d{1,2})季第(\d{1,3})集',
        # 1x01, 01x01
        r'(\d{1,2})x(\d{1,3})',
        # EP01, Ep.01, 第01集
        r'(?:[Ee][Pp]\.?\s*(\d{1,3})|第(\d{1,3})集)',
        # 直接的数字 01, 001 (假设为集数)
        r'(?:^|[^\d])(\d{2,3})(?:[^\d]|$)'
    ]
    
    for i, pattern in enumerate(patterns):
        match = re.search(pattern, filename)
        if match:
            if i == 0 or i == 1 or i == 2 or i == 3:  # 有季度和集数
                season = int(match.group(1))
                episode = int(match.group(2))
                return {
                    'season': season,
                    'episode': episode,
                    'filename': filename,
                    'pattern_type': 'season_episode'
                }
            elif i == 4:  # EP01 或 第01集
                episode = int(match.group(1) or match.group(2))
                return {
                    'season': None,
                    'episode': episode,
                    'filename': filename,
                    'pattern_type': 'episode_only'
                }
            elif i == 5:  # 纯数字
                episode = int(match.group(1))
                # 只有当数字在合理范围内时才认为是集数
                if 1 <= episode <= 200:
                    return {
                        'season': None,
                        'episode': episode,
                        'filename': filename,
                        'pattern_type': 'number_only'
                    }
    
    return None


def generate_season_summary(episodes: List[Dict[str, Any]], seasons: set) -> str:
    """
    生成季度摘要信息
    
    Args:
        episodes: 剧集列表
        seasons: 季度集合
    
    Returns:
        格式化的季度摘要字符串
    """
    if not episodes:
        return "无剧集信息"
    
    if not seasons or None in seasons:
        # 没有明确的季度信息，只显示集数范围
        episode_numbers = [ep['episode'] for ep in episodes if ep['episode']]
        if episode_numbers:
            min_ep = min(episode_numbers)
            max_ep = max(episode_numbers)
            if min_ep == max_ep:
                return f"E{min_ep:02d}"
            else:
                return f"E{min_ep:02d}-E{max_ep:02d}"
        else:
            return f"{len(episodes)}个文件"
    
    # 有明确季度信息
    season_summaries = []
    
    for season in sorted(seasons):
        season_episodes = [ep for ep in episodes if ep['season'] == season]
        episode_numbers = [ep['episode'] for ep in season_episodes if ep['episode']]
        
        if episode_numbers:
            min_ep = min(episode_numbers)
            max_ep = max(episode_numbers)
            
            if min_ep == max_ep:
                season_summary = f"S{season:02d}E{min_ep:02d}"
            else:
                # 检查是否连续
                if is_consecutive_episodes(episode_numbers):
                    season_summary = f"S{season:02d}E{min_ep:02d}-E{max_ep:02d}"
                else:
                    # 不连续，显示具体集数
                    ep_list = ','.join([f"E{ep:02d}" for ep in sorted(episode_numbers)])
                    if len(ep_list) > 20:  # 如果太长，就简化显示
                        season_summary = f"S{season:02d}E{min_ep:02d}-E{max_ep:02d}({len(episode_numbers)}集)"
                    else:
                        season_summary = f"S{season:02d}{ep_list}"
            
            season_summaries.append(season_summary)
    
    return ', '.join(season_summaries) if season_summaries else f"{len(episodes)}个文件"


def is_consecutive_episodes(episode_numbers: List[int]) -> bool:
    """
    检查集数是否连续
    
    Args:
        episode_numbers: 集数列表
    
    Returns:
        如果连续返回True，否则返回False
    """
    if len(episode_numbers) <= 1:
        return True
    
    sorted_episodes = sorted(episode_numbers)
    for i in range(1, len(sorted_episodes)):
        if sorted_episodes[i] - sorted_episodes[i-1] != 1:
            return False
    
    return True


def format_episode_details(episodes: List[Dict[str, Any]]) -> str:
    """
    格式化剧集详细信息用于显示
    
    Args:
        episodes: 剧集列表
    
    Returns:
        格式化的详细信息字符串
    """
    if not episodes:
        return "无剧集信息"
    
    # 按季度分组
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
            if is_consecutive_episodes(episode_numbers):
                min_ep = min(episode_numbers)
                max_ep = max(episode_numbers)
                if min_ep == max_ep:
                    details.append(f"第{season}季: E{min_ep:02d}")
                else:
                    details.append(f"第{season}季: E{min_ep:02d}-E{max_ep:02d} (共{len(episode_numbers)}集)")
            else:
                ep_list = ', '.join([f"E{ep:02d}" for ep in sorted(episode_numbers)])
                details.append(f"第{season}季: {ep_list} (共{len(episode_numbers)}集)")
    
    # 显示没有季度信息的剧集
    if no_season_episodes:
        episode_numbers = [ep['episode'] for ep in no_season_episodes if ep['episode']]
        if episode_numbers:
            if is_consecutive_episodes(episode_numbers):
                min_ep = min(episode_numbers)
                max_ep = max(episode_numbers)
                if min_ep == max_ep:
                    details.append(f"剧集: E{min_ep:02d}")
                else:
                    details.append(f"剧集: E{min_ep:02d}-E{max_ep:02d} (共{len(episode_numbers)}集)")
            else:
                ep_list = ', '.join([f"E{ep:02d}" for ep in sorted(episode_numbers)])
                details.append(f"剧集: {ep_list} (共{len(episode_numbers)}集)")
        else:
            details.append(f"其他文件: {len(no_season_episodes)}个")
    
    return '\n'.join(details) if details else f"视频文件: {len(episodes)}个"