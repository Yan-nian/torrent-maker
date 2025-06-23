import subprocess
import os
import shutil
from datetime import datetime
from typing import List, Optional


class TorrentCreator:
    def __init__(self, tracker_links: List[str], output_dir: str = "output"):
        self.tracker_links = tracker_links
        self.output_dir = output_dir

    def ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def check_mktorrent(self) -> bool:
        """检查系统是否安装了 mktorrent"""
        return shutil.which('mktorrent') is not None

    def create_torrent(self, source_path: str, custom_name: str = None) -> Optional[str]:
        """创建种子文件"""
        if not self.check_mktorrent():
            print("错误：系统未安装 mktorrent。请先安装 mktorrent。")
            print("macOS 安装命令：brew install mktorrent")
            print("Ubuntu 安装命令：sudo apt-get install mktorrent")
            return None

        if not os.path.exists(source_path):
            print(f"错误：源路径不存在：{source_path}")
            return None

        self.ensure_output_dir()
        
        # 生成种子文件名
        if custom_name:
            torrent_name = custom_name
        else:
            torrent_name = os.path.basename(source_path)
        
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
        command.extend(['-c', f"Created by torrent-maker on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
        
        # 启用私有种子标记（可选）
        # command.append('-p')
        
        # 添加源路径
        command.append(source_path)

        print(f"正在创建种子文件...")
        print(f"源路径: {source_path}")
        print(f"输出文件: {output_file}")
        print(f"Tracker 数量: {len(self.tracker_links)}")

        try:
            # 执行命令
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(f"种子文件创建成功: {output_file}")
            
            # 显示种子文件大小
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"种子文件大小: {size} bytes")
            
            return output_file
            
        except subprocess.CalledProcessError as e:
            print(f"创建种子文件时出错: {e}")
            if e.stderr:
                print(f"错误信息: {e.stderr}")
            return None
        except Exception as e:
            print(f"未知错误: {e}")
            return None

    def set_output_dir(self, output_dir: str):
        """设置输出目录"""
        self.output_dir = output_dir

    def add_tracker(self, tracker_url: str):
        """添加新的 tracker"""
        if tracker_url not in self.tracker_links:
            self.tracker_links.append(tracker_url)

    def remove_tracker(self, tracker_url: str):
        """移除 tracker"""
        if tracker_url in self.tracker_links:
            self.tracker_links.remove(tracker_url)

    def get_trackers(self) -> List[str]:
        """获取当前的 tracker 列表"""
        return self.tracker_links.copy()