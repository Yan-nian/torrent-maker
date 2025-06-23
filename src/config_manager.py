import json
import os
from typing import Dict, List, Any


class ConfigManager:
    def __init__(self, settings_path: str = 'config/settings.json', trackers_path: str = 'config/trackers.txt'):
        self.settings_path = settings_path
        self.trackers_path = trackers_path
        self.ensure_config_files()
        self.settings = self.load_settings()
        self.trackers = self.load_trackers()

    def ensure_config_files(self):
        """确保配置文件和目录存在"""
        # 确保配置目录存在
        config_dir = os.path.dirname(self.settings_path)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir)

        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(self.settings_path):
            self.create_default_settings()
        
        if not os.path.exists(self.trackers_path):
            self.create_default_trackers()

    def create_default_settings(self):
        """创建默认设置文件"""
        default_settings = {
            "resource_folder": os.path.expanduser("~/Downloads"),  # 默认下载文件夹
            "output_folder": "output",
            "default_piece_size": "auto",
            "private_torrent": False,
            "file_search_tolerance": 60,
            "max_search_results": 10,
            "auto_create_output_dir": True
        }
        
        with open(self.settings_path, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=4)
        
        print(f"已创建默认配置文件: {self.settings_path}")

    def create_default_trackers(self):
        """创建默认 tracker 文件"""
        default_trackers = [
            "udp://tracker.openbittorrent.com:80",
            "udp://tracker.opentrackr.org:1337/announce",
            "udp://tracker.coppersurfer.tk:6969/announce",
            "udp://exodus.desync.com:6969/announce",
            "udp://tracker.torrent.eu.org:451/announce"
        ]
        
        with open(self.trackers_path, 'w', encoding='utf-8') as f:
            for tracker in default_trackers:
                f.write(f"{tracker}\n")
        
        print(f"已创建默认 tracker 文件: {self.trackers_path}")

    def load_settings(self) -> Dict[str, Any]:
        """加载设置"""
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # 展开用户目录路径
                if 'resource_folder' in settings:
                    settings['resource_folder'] = os.path.expanduser(settings['resource_folder'])
                return settings
        except FileNotFoundError:
            print(f"设置文件未找到: {self.settings_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"设置文件格式错误: {e}")
            return {}

    def load_trackers(self) -> List[str]:
        """加载 tracker 列表"""
        try:
            with open(self.trackers_path, 'r', encoding='utf-8') as f:
                trackers = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # 忽略空行和注释
                        trackers.append(line)
                return trackers
        except FileNotFoundError:
            print(f"Tracker 文件未找到: {self.trackers_path}")
            return []

    def get_resource_folder(self) -> str:
        """获取资源文件夹路径"""
        return self.settings.get('resource_folder', os.path.expanduser("~/Downloads"))

    def set_resource_folder(self, path: str):
        """设置资源文件夹路径"""
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            self.settings['resource_folder'] = expanded_path
            self.save_settings()
            print(f"资源文件夹已设置为: {expanded_path}")
        else:
            print(f"警告：路径不存在: {expanded_path}")

    def get_output_folder(self) -> str:
        """获取种子输出文件夹路径"""
        return self.settings.get('output_folder', 'output')

    def set_output_folder(self, path: str):
        """设置种子输出文件夹路径"""
        expanded_path = os.path.expanduser(path)
        # 不需要检查路径是否存在，因为程序会自动创建
        self.settings['output_folder'] = expanded_path
        self.save_settings()
        print(f"种子输出文件夹已设置为: {expanded_path}")

    def get_trackers(self) -> List[str]:
        """获取 tracker 列表"""
        return self.trackers.copy()

    def add_tracker(self, tracker_url: str):
        """添加新的 tracker"""
        if tracker_url not in self.trackers:
            self.trackers.append(tracker_url)
            self.save_trackers()
            print(f"已添加 tracker: {tracker_url}")
        else:
            print(f"Tracker 已存在: {tracker_url}")

    def remove_tracker(self, tracker_url: str):
        """移除 tracker"""
        if tracker_url in self.trackers:
            self.trackers.remove(tracker_url)
            self.save_trackers()
            print(f"已移除 tracker: {tracker_url}")
        else:
            print(f"Tracker 不存在: {tracker_url}")

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
                for tracker in self.trackers:
                    f.write(f"{tracker}\n")
        except Exception as e:
            print(f"保存 tracker 时出错: {e}")

    def update_settings(self, new_settings: Dict[str, Any]):
        """更新设置"""
        self.settings.update(new_settings)
        self.save_settings()

    def display_current_config(self):
        """显示当前配置"""
        print("=== 当前配置 ===")
        print(f"资源文件夹: {self.get_resource_folder()}")
        print(f"种子输出文件夹: {self.get_output_folder()}")
        print(f"Tracker 数量: {len(self.trackers)}")
        print("Tracker 列表:")
        for i, tracker in enumerate(self.trackers, 1):
            print(f"  {i}. {tracker}")
        print("===============")