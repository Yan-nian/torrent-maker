#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from typing import Optional

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from torrent_creator import TorrentCreator
from file_matcher import FileMatcher
from config_manager import ConfigManager


class TorrentMakerApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.running = True

    def display_banner(self):
        """显示程序横幅"""
        print("=" * 60)
        print("           🎬 种子制作工具 Torrent Maker 🎬")
        print("=" * 60)
        print("   用于半自动化制作影视剧整季种子文件")
        print("=" * 60)

    def display_menu(self):
        """显示主菜单"""
        print("\n🔧 请选择操作:")
        print("1. 🔍 搜索并制作种子          [s/search]")
        print("2. ⚙️  查看当前配置           [c/config]")
        print("3. 📁 设置资源文件夹          [r/resource]")
        print("4. 📂 设置输出文件夹          [o/output]")
        print("5. 🌐 管理 Tracker          [t/tracker]")
        print("6. 🎯 快速制种 (直接输入路径)  [q/quick]")
        print("7. 📋 查看最近制作的种子       [l/list]")
        print("8. ❓ 帮助                   [h/help]")
        print("0. 🚪 退出                   [exit/quit]")
        print("-" * 50)

    def search_and_create_torrent(self):
        """搜索文件夹并创建种子"""
        resource_folder = self.config_manager.get_resource_folder()
        
        if not os.path.exists(resource_folder):
            print(f"❌ 资源文件夹不存在: {resource_folder}")
            print("请先设置正确的资源文件夹路径（输入 r 或选项 3）")
            return

        print(f"\n📁 当前搜索目录: {resource_folder}")
        
        # 获取用户输入
        while True:
            series_name = input("\n🎭 请输入影视剧名称（支持模糊搜索，输入 'back' 返回）: ").strip()
            
            if series_name.lower() in ['back', 'b', '返回']:
                return
                
            if not series_name:
                print("❌ 请输入有效的影视剧名称")
                continue
            
            break

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

        # 让用户选择文件夹
        while True:
            try:
                choice_input = input(f"\n请选择要制作种子的文件夹 (1-{len(matched_folders)}) 或输入:\n"
                                   f"  'a' 查看所有匹配项\n"
                                   f"  'r' 重新搜索\n"
                                   f"  'd数字' 查看详细剧集列表 (如 d1)\n"
                                   f"  '0' 返回主菜单\n"
                                   f"选择: ").strip().lower()
                
                if choice_input == '0':
                    return
                elif choice_input == 'r':
                    self.search_and_create_torrent()  # 递归调用重新搜索
                    return
                elif choice_input == 'a':
                    # 显示所有匹配项的详细信息
                    self.show_detailed_folder_info(matched_folders)
                    continue
                elif choice_input.startswith('d') and len(choice_input) > 1:
                    # 显示详细剧集列表
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
                
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(matched_folders):
                    selected_folder = matched_folders[choice_num - 1]
                    break
                else:
                    print(f"❌ 请输入 1-{len(matched_folders)} 之间的数字")
            except ValueError:
                print("❌ 请输入有效的选项")

        # 确认选择
        print(f"\n✅ 已选择: {selected_folder['name']}")
        print(f"📍 路径: {selected_folder['path']}")
        
        # 显示更多选项
        print("\n请选择操作:")
        print("1. 🎬 立即制作种子")
        print("2. 📁 查看文件夹详细内容")
        print("3. 🔙 重新选择")
        
        action = input("选择 (1-3): ").strip()
        
        if action == '1':
            confirm = input("确认制作种子? (Y/n): ").strip().lower()
            if confirm in ['', 'y', 'yes', '是']:
                self.create_torrent_file(selected_folder['path'], selected_folder['name'])
            else:
                print("❌ 取消制作种子")
        elif action == '2':
            self.show_folder_contents(selected_folder['path'])
            # 查看完内容后询问是否制作种子
            if input("\n查看完毕，是否制作种子? (y/N): ").strip().lower() in ['y', 'yes', '是']:
                self.create_torrent_file(selected_folder['path'], selected_folder['name'])
        elif action == '3':
            self.search_and_create_torrent()  # 重新搜索

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
        else:
            print("\n❌ 种子制作失败")

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
            self.config_manager.add_tracker(tracker_url)
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
                self.config_manager.remove_tracker(tracker_to_remove)
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效数字")

    def set_resource_folder(self):
        """设置资源文件夹"""
        current_folder = self.config_manager.get_resource_folder()
        print(f"\n📁 当前资源文件夹: {current_folder}")
        
        # 检查当前文件夹状态
        if os.path.exists(current_folder):
            from utils.helpers import get_directory_info
            info = get_directory_info(current_folder)
            print(f"📊 文件夹状态: 存在, {info['total_files']} 个文件")
        else:
            print("⚠️  当前文件夹不存在!")
        
        print("\n选择操作:")
        print("1. 📝 输入新路径")
        print("2. 📁 常用路径快捷选择")
        print("0. 🔙 返回")
        
        choice = input("请选择 (0-2): ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            new_folder = input("请输入新的资源文件夹路径 (支持拖拽，留空保持不变): ").strip()
            new_folder = new_folder.strip('"\'')  # 移除引号
            
            if new_folder:
                expanded_path = os.path.expanduser(new_folder)
                if os.path.exists(expanded_path):
                    self.config_manager.set_resource_folder(expanded_path)
                else:
                    create = input(f"路径不存在: {expanded_path}\n是否创建? (y/N): ").strip().lower()
                    if create in ['y', 'yes', '是']:
                        try:
                            os.makedirs(expanded_path, exist_ok=True)
                            self.config_manager.set_resource_folder(expanded_path)
                            print(f"✅ 已创建并设置资源文件夹: {expanded_path}")
                        except OSError as e:
                            print(f"❌ 创建文件夹失败: {e}")
                    else:
                        print("❌ 路径不存在，未更改设置")
            else:
                print("⚡ 路径未更改")
                
        elif choice == '2':
            self.show_common_paths_for_resource()

    def set_output_folder(self):
        """设置种子输出文件夹"""
        current_folder = self.config_manager.get_output_folder()
        print(f"\n📂 当前输出文件夹: {current_folder}")
        
        # 检查当前文件夹状态
        if os.path.exists(current_folder):
            torrent_count = len([f for f in os.listdir(current_folder) if f.endswith('.torrent')])
            print(f"📊 文件夹状态: 存在, 包含 {torrent_count} 个种子文件")
        else:
            print("⚠️  当前文件夹不存在，将在制种时自动创建")
        
        print("\n选择操作:")
        print("1. 📝 输入新路径")
        print("2. 📁 常用路径快捷选择")
        print("3. 📂 打开当前输出文件夹")
        print("0. 🔙 返回")
        
        choice = input("请选择 (0-3): ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            new_folder = input("请输入新的种子输出文件夹路径 (支持拖拽，留空保持不变): ").strip()
            new_folder = new_folder.strip('"\'')  # 移除引号
            
            if new_folder:
                expanded_path = os.path.expanduser(new_folder)
                self.config_manager.set_output_folder(expanded_path)
                
                # 尝试创建目录
                try:
                    os.makedirs(expanded_path, exist_ok=True)
                    print(f"✅ 输出文件夹设置成功并已创建: {expanded_path}")
                except OSError as e:
                    print(f"⚠️  输出文件夹设置成功，但创建失败: {e}")
                    print("程序运行时会自动尝试创建该目录")
            else:
                print("⚡ 路径未更改")
                
        elif choice == '2':
            self.show_common_paths_for_output()
            
        elif choice == '3':
            self.open_folder(current_folder)

    def show_help(self):
        """显示帮助信息"""
        print("\n❓ 帮助信息")
        print("=" * 60)
        print("🔍 1. 搜索并制作种子 [s/search]:")
        print("   - 输入影视剧名称进行智能模糊搜索")
        print("   - 查看匹配文件夹的详细信息")
        print("   - 预览文件夹内容后再决定是否制种")
        print()
        print("🎯 6. 快速制种 [q/quick]:")
        print("   - 直接输入或拖拽文件夹路径")
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
        print("📋 系统要求:")
        print("   - 需要安装 mktorrent 工具")
        print("   - macOS: brew install mktorrent")
        print("   - Ubuntu: sudo apt-get install mktorrent")
        print()
        print("💡 使用技巧:")
        print("   - 支持文件夹拖拽到终端")
        print("   - 支持路径自动补全 (Tab键)")
        print("   - 支持相对路径和 ~ 家目录符号")
        print("=" * 60)

    def run(self):
        """运行主程序"""
        self.display_banner()
        
        # 检查配置
        if not os.path.exists(self.config_manager.get_resource_folder()):
            print("\n⚠️  首次使用，请先设置资源文件夹")
            self.set_resource_folder()

        while self.running:
            try:
                self.display_menu()
                choice = input("请选择操作 (0-8 或快捷键): ").strip().lower()
                
                # 处理退出命令
                if choice in ['0', 'exit', 'quit', 'q']:
                    print("\n👋 感谢使用种子制作工具！")
                    self.running = False
                # 搜索并制作种子
                elif choice in ['1', 's', 'search']:
                    self.search_and_create_torrent()
                # 查看配置
                elif choice in ['2', 'c', 'config']:
                    self.config_manager.display_current_config()
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
                elif choice in ['6', 'quick']:
                    self.quick_torrent_creation()
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

    def quick_torrent_creation(self):
        """快速制种 - 直接输入路径"""
        print("\n🎯 快速制种模式")
        print("直接输入文件夹路径来快速制作种子")
        print("-" * 40)
        
        folder_path = input("请输入文件夹完整路径 (或拖拽文件夹到此处): ").strip()
        
        # 处理拖拽文件夹的情况，移除引号
        folder_path = folder_path.strip('"\'')
        
        if not folder_path:
            print("❌ 请输入有效的文件夹路径")
            return
        
        # 展开路径
        folder_path = os.path.expanduser(folder_path)
        
        if not os.path.exists(folder_path):
            print(f"❌ 文件夹不存在: {folder_path}")
            return
        
        if not os.path.isdir(folder_path):
            print(f"❌ 不是文件夹: {folder_path}")
            return
        
        # 显示文件夹信息
        folder_name = os.path.basename(folder_path)
        from utils.helpers import get_directory_info
        dir_info = get_directory_info(folder_path)
        
        print(f"\n📂 文件夹: {folder_name}")
        print(f"📍 路径: {folder_path}")
        print(f"📄 总文件数: {dir_info['total_files']}")
        print(f"🎬 视频文件数: {dir_info['video_files']}")
        print(f"💾 大小: {dir_info['total_size_formatted']}")
        
        # 询问是否制作种子
        confirm = input("\n是否制作种子? (Y/n): ").strip().lower()
        if confirm in ['', 'y', 'yes', '是', 'ok']:
            self.create_torrent_file(folder_path, folder_name)
        else:
            print("❌ 取消制作种子")

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

    def show_detailed_folder_info(self, folders):
        """显示文件夹的详细信息"""
        print("\n📊 详细信息:")
        print("=" * 100)
        
        for i, folder_info in enumerate(folders, 1):
            from utils.helpers import get_directory_info
            detailed_info = get_directory_info(folder_info['path'])
            
            print(f"{i:2d}. 📂 {folder_info['name']}")
            print(f"     📍 完整路径: {folder_info['path']}")
            print(f"     📊 匹配度: {folder_info['score']}%")
            print(f"     📄 总文件数: {detailed_info['total_files']}")
            print(f"     🎬 视频文件数: {detailed_info['video_files']}")
            print(f"     💾 文件夹大小: {detailed_info['total_size_formatted']}")
            print(f"     🔒 可读取: {'是' if detailed_info['readable'] else '否'}")
            
            # 显示剧集信息
            if folder_info.get('episodes') and folder_info.get('video_count', 0) > 0:
                print(f"     🎭 剧集信息: {folder_info['episodes']}")
                
                # 提供详细剧集列表的选项
                file_matcher = FileMatcher(self.config_manager.get_resource_folder())
                detailed_episodes = file_matcher.get_folder_episodes_detail(folder_info['path'])
                if detailed_episodes != "无剧集信息":
                    print(f"     📋 详细集数: 输入 'd{i}' 查看详细列表")
            
            print("-" * 100)

    def show_folder_contents(self, folder_path):
        """显示文件夹内容"""
        print(f"\n📁 查看文件夹内容: {os.path.basename(folder_path)}")
        print(f"📍 完整路径: {folder_path}")
        print("-" * 60)
        
        try:
            from utils.helpers import is_video_file
            
            # 获取文件列表
            all_files = []
            video_files = []
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path)
                    file_size = os.path.getsize(file_path)
                    
                    all_files.append((relative_path, file_size))
                    
                    if is_video_file(file):
                        video_files.append((relative_path, file_size))
            
            # 显示视频文件
            if video_files:
                print(f"🎬 视频文件 ({len(video_files)} 个):")
                video_files.sort()  # 按文件名排序
                
                for i, (file_path, file_size) in enumerate(video_files[:20], 1):  # 最多显示20个
                    from utils.helpers import format_file_size
                    print(f"  {i:2d}. {file_path}")
                    print(f"       💾 {format_file_size(file_size)}")
                
                if len(video_files) > 20:
                    print(f"       ... 还有 {len(video_files) - 20} 个视频文件")
            else:
                print("🎬 未找到视频文件")
            
            print()
            print(f"📊 统计信息:")
            print(f"   📄 总文件数: {len(all_files)}")
            print(f"   🎬 视频文件数: {len(video_files)}")
            
            total_size = sum(size for _, size in all_files)
            from utils.helpers import format_file_size
            print(f"   💾 总大小: {format_file_size(total_size)}")
            
        except Exception as e:
            print(f"❌ 无法读取文件夹内容: {e}")

    def show_common_paths_for_resource(self):
        """显示资源文件夹的常用路径选择"""
        print("\n📁 常用资源文件夹路径:")
        
        common_paths = [
            ("~/Downloads", "用户下载文件夹"),
            ("~/Movies", "用户影片文件夹"), 
            ("~/Videos", "用户视频文件夹"),
            ("~/Desktop", "桌面"),
            ("/Volumes", "外接存储设备 (macOS)"),
        ]
        
        for i, (path, desc) in enumerate(common_paths, 1):
            expanded = os.path.expanduser(path)
            exists = "✅" if os.path.exists(expanded) else "❌"
            print(f"{i}. {exists} {path} - {desc}")
        
        choice = input(f"\n选择路径 (1-{len(common_paths)}) 或按回车返回: ").strip()
        
        try:
            if choice:
                idx = int(choice) - 1
                if 0 <= idx < len(common_paths):
                    selected_path = os.path.expanduser(common_paths[idx][0])
                    if os.path.exists(selected_path):
                        self.config_manager.set_resource_folder(selected_path)
                    else:
                        print(f"❌ 路径不存在: {selected_path}")
        except ValueError:
            print("❌ 无效选择")

    def show_common_paths_for_output(self):
        """显示输出文件夹的常用路径选择"""
        print("\n📂 常用输出文件夹路径:")
        
        common_paths = [
            ("~/Downloads/Torrents", "下载文件夹下的种子目录"),
            ("~/Desktop/Torrents", "桌面种子目录"),
            ("./output", "当前目录下的output文件夹"),
            ("~/Documents/Torrents", "文档文件夹下的种子目录"),
        ]
        
        for i, (path, desc) in enumerate(common_paths, 1):
            expanded = os.path.expanduser(path)
            exists = "✅" if os.path.exists(expanded) else "🆕"
            print(f"{i}. {exists} {path} - {desc}")
        
        choice = input(f"\n选择路径 (1-{len(common_paths)}) 或按回车返回: ").strip()
        
        try:
            if choice:
                idx = int(choice) - 1
                if 0 <= idx < len(common_paths):
                    selected_path = os.path.expanduser(common_paths[idx][0])
                    self.config_manager.set_output_folder(selected_path)
                    
                    # 创建目录
                    try:
                        os.makedirs(selected_path, exist_ok=True)
                        print(f"✅ 输出文件夹设置并创建成功: {selected_path}")
                    except OSError as e:
                        print(f"❌ 创建目录失败: {e}")
        except ValueError:
            print("❌ 无效选择")

    def open_folder(self, folder_path):
        """打开文件夹"""
        if not os.path.exists(folder_path):
            print(f"❌ 文件夹不存在: {folder_path}")
            return
            
        try:
            import subprocess
            import platform
            
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder_path])
            elif platform.system() == "Windows":  # Windows
                subprocess.run(["explorer", folder_path])
            else:  # Linux
                subprocess.run(["xdg-open", folder_path])
                
            print(f"✅ 已打开文件夹: {folder_path}")
        except Exception as e:
            print(f"❌ 无法打开文件夹: {e}")

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

def main():
    """主函数"""
    app = TorrentMakerApp()
    app.run()


if __name__ == "__main__":
    main()