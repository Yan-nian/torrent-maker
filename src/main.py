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
from search_history import SearchHistory
from statistics_manager import StatisticsManager


class TorrentMakerApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.search_history = SearchHistory()
        self.statistics_manager = StatisticsManager()
        self.running = True

    def display_banner(self):
        """显示程序横幅"""
        print("=" * 60)
        print("           🎬 种子制作工具 Torrent Maker 🎬")
        print("=" * 60)
        print("   用于半自动化制作影视剧整季种子文件")
        print("   版本：1.4.0 | 许可证：MIT")
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
        print("8. 📚 搜索历史管理           [history]")
        print("9. 📊 性能统计和监控          [stats]")
        print("10. 🔧 高级配置管理          [advanced]")
        print("11. ❓ 帮助                  [h/help]")
        print("0. 🚪 退出                   [exit/quit]")
        print("-" * 50)

    def search_and_create_torrent(self):
        """搜索文件夹并创建种子 - 支持连续搜索和多选制种"""
        resource_folder = self.config_manager.get_resource_folder()
        
        if not os.path.exists(resource_folder):
            print(f"❌ 资源文件夹不存在: {resource_folder}")
            print("请先设置正确的资源文件夹路径（输入 r 或选项 3）")
            return

        # 搜索循环 - 允许连续搜索
        while True:
            print(f"\n📁 当前搜索目录: {resource_folder}")

            # 显示搜索历史选项
            self._show_search_options()

            # 获取用户输入
            series_name = input("\n🎭 请输入影视剧名称（支持模糊搜索）: ").strip()

            # 处理特殊命令
            if series_name.lower() in ['back', 'b', '返回', '0']:
                return
            elif series_name.lower() in ['history', 'h', '历史']:
                self._show_search_history_menu()
                continue
            elif series_name.startswith('h') and len(series_name) > 1:
                # 快速选择历史记录 (h1, h2, etc.)
                try:
                    history_index = int(series_name[1:]) - 1
                    recent_searches = self.search_history.get_recent_searches(10)
                    if 0 <= history_index < len(recent_searches):
                        series_name = recent_searches[history_index]['query']
                        print(f"🔄 使用历史搜索: {series_name}")
                    else:
                        print(f"❌ 历史记录索引超出范围 (1-{len(recent_searches)})")
                        continue
                except ValueError:
                    print("❌ 无效的历史记录索引格式")
                    continue

            if not series_name:
                print("❌ 请输入有效的影视剧名称")
                continue

            print(f"\n🔍 正在搜索包含 '{series_name}' 的文件夹...")
            
            # 搜索匹配的文件夹
            file_matcher = FileMatcher(resource_folder)
            matched_folders = file_matcher.match_folders(series_name)

            # 记录搜索历史和统计
            self.search_history.add_search(series_name, len(matched_folders), resource_folder)
            self.statistics_manager.record_search(len(matched_folders))

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
            print("=" * 100)

            for i, folder_info in enumerate(matched_folders, 1):
                # 导入路径格式化函数
                try:
                    from utils.helpers import format_path_display
                except ImportError:
                    def format_path_display(path, base_path=None, max_length=80):
                        if len(path) <= max_length:
                            return path
                        return f"{path[:37]}...{path[-37:]}"

                # 格式化路径显示
                formatted_path = format_path_display(folder_info['path'], resource_folder, max_length=70)

                print(f"{i:2d}. 📂 {folder_info['name']}")
                print(f"     📍 完整路径: {folder_info['path']}")
                print(f"     📁 相对路径: {formatted_path}")
                print(f"     📊 匹配度: {folder_info['score']}%")
                print(f"     📄 文件数: {folder_info['file_count']}")
                print(f"     💾 大小: {folder_info['size']}")
                # 显示剧集信息
                if folder_info.get('episodes') and folder_info.get('video_count', 0) > 0:
                    print(f"     🎬 剧集: {folder_info['episodes']}")
                print("-" * 100)

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
            print(f"\n📋 选择操作 (共 {len(matched_folders)} 个匹配项):")
            print("=" * 60)
            print("🎯 制种操作:")
            print(f"  数字 (1-{len(matched_folders)}) - 选择单个文件夹制种")
            print(f"  多个数字用逗号分隔 (如: 1,3,5) - 批量制种")
            print(f"  'all' 或 'a' - 选择所有文件夹批量制种")
            print()
            print("🔍 查看详情:")
            print(f"  'info' 或 'i' - 查看所有匹配项详细信息")
            print(f"  'd数字' - 查看详细剧集列表 (如: d1)")
            print()
            print("🧭 导航选项:")
            print(f"  'search' 或 's' - 继续搜索其他内容")
            print(f"  'history' 或 'h' - 查看搜索历史")
            print(f"  'back' 或 'b' - 返回上一步")
            print(f"  'menu' 或 'm' - 返回主菜单")
            print(f"  'quit' 或 'q' - 退出程序")
            print("=" * 60)

            choice_input = input("🎯 请选择操作: ").strip().lower()
            
            # 处理导航命令
            if choice_input in ['0', 'menu', 'm', '主菜单']:
                return None
            elif choice_input in ['search', 's', '搜索']:
                return 'continue_search'
            elif choice_input in ['back', 'b', '返回']:
                return 'continue_search'  # 返回到搜索
            elif choice_input in ['history', 'h', '历史']:
                self._show_search_history_menu()
                continue
            elif choice_input in ['quit', 'q', '退出']:
                print("\n👋 感谢使用种子制作工具！")
                sys.exit(0)
            elif choice_input in ['info', 'i', 'a']:
                self.show_detailed_folder_info(matched_folders)
                continue
            elif choice_input in ['all', '全选']:
                # 选择所有文件夹
                print(f"✅ 已选择所有 {len(matched_folders)} 个文件夹进行批量制种")
                return matched_folders
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
                # 记录统计信息
                file_count = folder_info.get('file_count', 0)
                folder_size = self._get_folder_size_bytes(folder_info['path'])
                self.statistics_manager.record_torrent_creation(file_count, folder_size)
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
        print("=" * 80)
        print("🔍 1. 搜索并制作种子 [s/search]:")
        print("   - 输入影视剧名称进行智能模糊搜索")
        print("   - 🆕 显示完整文件路径和相对路径")
        print("   - 🆕 支持搜索历史快捷方式 (h1, h2, h3...)")
        print("   - 🆕 支持多选制种：用逗号分隔选择多个文件夹 (如: 1,3,5)")
        print("   - 🆕 支持全选制种：输入 'all' 选择所有匹配项")
        print("   - 🆕 支持连续搜索：制种完成后可继续搜索其他内容")
        print("   - 预览文件夹内容后再决定是否制种")
        print()
        print("📚 8. 搜索历史管理 [history]:")
        print("   - 🆕 自动记录搜索历史，最多保存50条")
        print("   - 🆕 快速重复搜索：h1, h2, h3... 快捷方式")
        print("   - 🆕 查看搜索统计：总次数、热门搜索、最近活动")
        print("   - 🆕 历史管理：清空历史、删除特定记录")
        print("   - 🆕 智能过期：自动清理30天前的记录")
        print()
        print("📊 9. 性能统计和监控 [stats]:")
        print("   - 🆕 实时性能监控：搜索耗时、制种耗时统计")
        print("   - 🆕 缓存统计：搜索缓存、大小缓存命中率")
        print("   - 🆕 会话统计：本次使用的详细统计信息")
        print("   - 🆕 综合报告：完整的性能分析报告")
        print("   - 🆕 统计导出：支持导出统计数据到文件")
        print()
        print("🔧 10. 高级配置管理 [advanced]:")
        print("   - 🆕 配置验证和自动修复：检测并修复配置问题")
        print("   - 🆕 配置备份恢复：自动备份和一键恢复")
        print("   - 🆕 配置导入导出：支持配置文件的迁移")
        print("   - 🆕 完整性检查：全面的配置状态检查")
        print("   - 🆕 重置功能：一键恢复默认配置")
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
        print("🎛️ 快捷键和导航:")
        print("   s/search  - 搜索制种    q/quick   - 快速制种")
        print("   c/config  - 查看配置    l/list    - 最近种子")
        print("   r/resource- 资源目录    o/output  - 输出目录")
        print("   t/tracker - 管理tracker history  - 搜索历史")
        print("   stats     - 性能统计    advanced - 高级配置")
        print("   h/help    - 显示帮助    exit/quit - 退出程序")
        print()
        print("🧭 搜索界面导航:")
        print("   🆕 back/b    - 返回上一步    menu/m   - 返回主菜单")
        print("   🆕 history/h - 查看搜索历史  quit/q   - 退出程序")
        print("   🆕 info/i    - 查看详细信息  all      - 选择全部")
        print()
        print("🆕 新功能亮点:")
        print("   📍 完整路径显示: 同时显示完整路径和相对路径")
        print("   📚 智能搜索历史: 自动记录，快速重复搜索")
        print("   🧭 增强导航: 多种返回和导航选项")
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
        print("   - 使用搜索历史快捷方式提高效率")
        print("   - 善用导航快捷键快速切换功能")
        print("=" * 80)

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
                choice = input("请选择操作 (0-11 或快捷键): ").strip().lower()

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
                # 搜索历史管理
                elif choice in ['8', 'history']:
                    self._show_search_history_menu()
                # 性能统计和监控
                elif choice in ['9', 'stats']:
                    self.show_statistics_menu()
                # 高级配置管理
                elif choice in ['10', 'advanced']:
                    self.show_advanced_config_menu()
                # 帮助
                elif choice in ['11', 'h', 'help']:
                    self.show_help()
                else:
                    print("❌ 无效选择，请重新输入")
                    print("💡 提示：您可以输入数字 (0-11) 或使用快捷键")
                    
            except KeyboardInterrupt:
                print("\n\n👋 程序被用户中断，再见！")
                self.running = False
            except Exception as e:
                print(f"\n❌ 发生未知错误: {e}")
                print("程序将继续运行...")

    def quick_torrent_creation(self):
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
                    from utils.helpers import get_directory_info
                    dir_info = get_directory_info(folder_path)
                    
                    print(f"   ✅ 有效文件夹: {folder_name}")
                    print(f"   📄 总文件数: {dir_info['total_files']}")
                    print(f"   🎬 视频文件数: {dir_info['video_files']}")
                    print(f"   💾 大小: {dir_info['total_size_formatted']}")
                    
                    valid_folders.append({
                        'name': folder_name,
                        'path': folder_path,
                        'info': dir_info
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
            print(f"\n📋 找到 {len(valid_folders)} 个有效文件夹:")
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
            
            for root, _, files in os.walk(folder_path):
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

    def _show_search_options(self):
        """显示搜索选项和快捷方式"""
        recent_searches = self.search_history.get_recent_searches(5)

        if recent_searches:
            print("\n📚 最近搜索 (快捷方式):")
            for i, item in enumerate(recent_searches, 1):
                print(f"  h{i}. {item['query']} ({item.get('last_results_count', 0)} 个结果)")

        print("\n💡 搜索提示:")
        print("  • 直接输入影视剧名称进行搜索")
        print("  • 输入 'h数字' 快速使用历史搜索 (如: h1, h2)")
        print("  • 输入 'history' 或 'h' 查看完整搜索历史")
        print("  • 输入 'back' 或 '0' 返回主菜单")

    def _show_search_history_menu(self):
        """显示搜索历史菜单"""
        while True:
            print("\n📚 搜索历史管理")
            print("=" * 60)

            recent_searches = self.search_history.get_recent_searches(15)

            if not recent_searches:
                print("📝 暂无搜索历史")
                input("\n按回车键返回...")
                return

            # 显示历史记录
            for i, item in enumerate(recent_searches, 1):
                from datetime import datetime
                timestamp = datetime.fromisoformat(item['timestamp'])
                time_str = timestamp.strftime("%m-%d %H:%M")

                print(f"{i:2d}. 🔍 {item['query']}")
                print(f"     ⏰ {time_str} | 📊 {item.get('last_results_count', 0)} 个结果 | "
                      f"🔄 搜索 {item.get('count', 1)} 次")

            print("\n📋 操作选项:")
            print("  数字 - 使用该历史记录进行搜索")
            print("  'stats' - 查看搜索统计")
            print("  'clear' - 清空搜索历史")
            print("  'back' - 返回搜索")

            choice = input("\n选择操作: ").strip().lower()

            if choice in ['back', 'b', '返回']:
                return
            elif choice == 'stats':
                self._show_search_statistics()
                continue
            elif choice == 'clear':
                if input("确认清空所有搜索历史? (y/N): ").strip().lower() in ['y', 'yes']:
                    if self.search_history.clear_history():
                        print("✅ 搜索历史已清空")
                    else:
                        print("❌ 清空搜索历史失败")
                continue
            else:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(recent_searches):
                        selected_query = recent_searches[index]['query']
                        print(f"🔄 使用历史搜索: {selected_query}")
                        # 这里可以直接执行搜索，但为了简化，我们返回让用户手动输入
                        print("💡 请在搜索框中输入上述关键词")
                        input("按回车键返回搜索...")
                        return
                    else:
                        print(f"❌ 请输入 1-{len(recent_searches)} 之间的数字")
                except ValueError:
                    print("❌ 请输入有效的选项")

    def _show_search_statistics(self):
        """显示搜索统计信息"""
        stats = self.search_history.get_statistics()

        print("\n📊 搜索统计信息")
        print("=" * 50)
        print(f"📈 总搜索次数: {stats['total_searches']}")
        print(f"🔍 不同关键词: {stats['unique_queries']}")
        print(f"📊 平均结果数: {stats['average_results']}")
        print(f"🔥 最近7天活动: {stats['recent_activity']} 次搜索")

        if stats['most_searched']:
            most = stats['most_searched']
            print(f"🏆 最常搜索: {most['query']} ({most.get('count', 1)} 次)")

        # 显示热门搜索
        popular = self.search_history.get_popular_searches(5)
        if popular:
            print(f"\n🔥 热门搜索:")
            for i, item in enumerate(popular, 1):
                print(f"  {i}. {item['query']} ({item.get('count', 1)} 次)")

        input("\n按回车键返回...")

    def show_statistics_menu(self):
        """显示性能统计菜单"""
        while True:
            print("\n📊 性能统计和监控")
            print("=" * 60)
            print("1. 📈 查看性能统计")
            print("2. 💾 查看缓存统计")
            print("3. 🎯 查看会话统计")
            print("4. 📊 查看综合统计")
            print("5. 📤 导出统计报告")
            print("6. 🔄 重置会话统计")
            print("7. 🧹 清空所有缓存")
            print("0. 🔙 返回主菜单")
            print("=" * 60)

            choice = input("请选择操作 (0-7): ").strip()

            try:
                if choice == '0':
                    break
                elif choice == '1':
                    self.statistics_manager.display_performance_stats()
                elif choice == '2':
                    self.statistics_manager.display_cache_stats()
                elif choice == '3':
                    self.statistics_manager.display_session_stats()
                elif choice == '4':
                    self.statistics_manager.display_comprehensive_stats()
                elif choice == '5':
                    self._export_statistics_report()
                elif choice == '6':
                    self.statistics_manager.reset_session_stats()
                    print("✅ 会话统计已重置")
                elif choice == '7':
                    self.statistics_manager.clear_all_caches()
                    print("✅ 所有缓存已清空")
                else:
                    print("❌ 无效选择，请输入 0-7 之间的数字")

            except Exception as e:
                print(f"❌ 操作过程中发生错误: {e}")

            if choice != '0':
                input("\n按回车键继续...")

    def _export_statistics_report(self):
        """导出统计报告"""
        import time
        default_filename = f"torrent_maker_stats_{time.strftime('%Y%m%d_%H%M%S')}.json"
        filename = input(f"请输入导出文件名 (回车使用默认: {default_filename}): ").strip()

        if not filename:
            filename = default_filename

        if self.statistics_manager.export_stats(filename):
            print(f"✅ 统计报告已导出到: {filename}")
        else:
            print("❌ 导出统计报告失败")

    def show_advanced_config_menu(self):
        """显示高级配置管理菜单"""
        while True:
            print("\n🔧 高级配置管理")
            print("=" * 60)
            print("1. 📋 查看配置状态")
            print("2. 🔍 验证并修复配置")
            print("3. 💾 备份当前配置")
            print("4. 🔄 恢复备份配置")
            print("5. 📤 导出配置")
            print("6. 📥 导入配置")
            print("7. 🔄 重置为默认配置")
            print("8. 📊 配置完整性检查")
            print("0. 🔙 返回主菜单")
            print("=" * 60)

            choice = input("请选择操作 (0-8): ").strip()

            try:
                if choice == '0':
                    break
                elif choice == '1':
                    self._show_config_status()
                elif choice == '2':
                    self._validate_and_repair_config()
                elif choice == '3':
                    self._backup_config()
                elif choice == '4':
                    self._restore_config()
                elif choice == '5':
                    self._export_config()
                elif choice == '6':
                    self._import_config()
                elif choice == '7':
                    self._reset_config()
                elif choice == '8':
                    self._check_config_integrity()
                else:
                    print("❌ 无效选择，请输入 0-8 之间的数字")

            except Exception as e:
                print(f"❌ 操作过程中发生错误: {e}")

            if choice != '0':
                input("\n按回车键继续...")

    def _show_config_status(self):
        """显示配置状态"""
        print("\n📋 配置状态信息")
        print("=" * 60)

        status = self.config_manager.get_config_status()

        if status:
            print("📄 设置文件:")
            settings_file = status.get('settings_file', {})
            print(f"  路径: {settings_file.get('path', 'N/A')}")
            print(f"  存在: {'是' if settings_file.get('exists', False) else '否'}")
            print(f"  大小: {settings_file.get('size', 0)} 字节")
            print(f"  修改时间: {settings_file.get('modified', 'N/A')}")

            print("\n🌐 Tracker文件:")
            trackers_file = status.get('trackers_file', {})
            print(f"  路径: {trackers_file.get('path', 'N/A')}")
            print(f"  存在: {'是' if trackers_file.get('exists', False) else '否'}")
            print(f"  大小: {trackers_file.get('size', 0)} 字节")
            print(f"  修改时间: {trackers_file.get('modified', 'N/A')}")

            print(f"\n📊 配置统计:")
            print(f"  设置项数量: {status.get('settings_count', 0)}")
            print(f"  Tracker数量: {status.get('trackers_count', 0)}")
            print(f"  有效Tracker: {status.get('valid_trackers', 0)}")
            print(f"  备份目录: {status.get('backup_dir', 'N/A')}")
            print(f"  有备份: {'是' if status.get('has_backups', False) else '否'}")
        else:
            print("❌ 无法获取配置状态信息")

    def _validate_and_repair_config(self):
        """验证并修复配置"""
        print("\n🔍 正在验证配置...")

        if hasattr(self.config_manager, 'validate_and_repair'):
            report = self.config_manager.validate_and_repair()

            print("\n📋 验证结果:")
            if report.get('issues_found'):
                print("❌ 发现的问题:")
                for issue in report['issues_found']:
                    print(f"  • {issue}")

            if report.get('repairs_made'):
                print("✅ 已修复:")
                for repair in report['repairs_made']:
                    print(f"  • {repair}")

            if report.get('warnings'):
                print("⚠️ 警告:")
                for warning in report['warnings']:
                    print(f"  • {warning}")

            if not report.get('issues_found') and not report.get('warnings'):
                print("✅ 配置验证通过，未发现问题")
        else:
            print("❌ 当前配置管理器不支持自动验证和修复")

    def _backup_config(self):
        """备份配置"""
        print("\n💾 正在备份配置...")

        if hasattr(self.config_manager, 'backup_config'):
            if self.config_manager.backup_config():
                print("✅ 配置备份成功")
            else:
                print("❌ 配置备份失败")
        else:
            print("❌ 当前配置管理器不支持备份功能")

    def _restore_config(self):
        """恢复配置"""
        print("\n🔄 配置恢复")
        print("⚠️ 警告：此操作将覆盖当前配置")

        confirm = input("确认恢复最新备份配置？(y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("❌ 已取消恢复操作")
            return

        if hasattr(self.config_manager, 'restore_backup'):
            if self.config_manager.restore_backup():
                print("✅ 配置恢复成功")
                print("💡 建议重启程序以确保配置生效")
            else:
                print("❌ 配置恢复失败")
        else:
            print("❌ 当前配置管理器不支持恢复功能")

    def _export_config(self):
        """导出配置"""
        import time
        default_filename = f"torrent_maker_config_{time.strftime('%Y%m%d_%H%M%S')}.json"
        filename = input(f"请输入导出文件名 (回车使用默认: {default_filename}): ").strip()

        if not filename:
            filename = default_filename

        if self.config_manager.export_config(filename):
            print(f"✅ 配置已导出到: {filename}")
        else:
            print("❌ 导出配置失败")

    def _import_config(self):
        """导入配置"""
        print("\n📥 导入配置")
        print("⚠️ 警告：导入配置将覆盖当前所有设置")

        filename = input("请输入配置文件路径: ").strip()
        if not filename:
            print("❌ 文件路径不能为空")
            return

        confirm = input("确认导入配置？这将覆盖当前设置 (y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("❌ 已取消导入")
            return

        if self.config_manager.import_config(filename):
            print("✅ 配置导入成功")
            print("💡 建议重启程序以确保配置生效")
        else:
            print("❌ 导入配置失败")

    def _reset_config(self):
        """重置配置"""
        print("\n🔄 重置配置")
        print("⚠️ 警告：此操作将重置所有配置为默认值")

        confirm = input("确认重置配置为默认值？(y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("❌ 已取消重置操作")
            return

        if hasattr(self.config_manager, 'reset_to_default'):
            if self.config_manager.reset_to_default():
                print("✅ 配置已重置为默认值")
                print("💡 建议重启程序以确保配置生效")
            else:
                print("❌ 重置配置失败")
        else:
            if self.config_manager.reset_to_defaults():
                print("✅ 配置已重置为默认值")
                print("💡 建议重启程序以确保配置生效")
            else:
                print("❌ 重置配置失败")

    def _check_config_integrity(self):
        """检查配置完整性"""
        print("\n📊 配置完整性检查")
        print("=" * 50)

        # 检查配置文件存在性
        settings_exists = self.config_manager.settings_path.exists()
        trackers_exists = self.config_manager.trackers_path.exists()

        print(f"📄 设置文件: {'✅ 存在' if settings_exists else '❌ 不存在'}")
        print(f"🌐 Tracker文件: {'✅ 存在' if trackers_exists else '❌ 不存在'}")

        # 检查必需配置项
        required_settings = ['resource_folder', 'output_folder']
        missing_settings = [key for key in required_settings if key not in self.config_manager.settings]

        if missing_settings:
            print(f"❌ 缺少必需配置项: {', '.join(missing_settings)}")
        else:
            print("✅ 所有必需配置项都存在")

        # 检查tracker有效性
        valid_trackers = len([t for t in self.config_manager.trackers if self.config_manager._is_valid_tracker_url(t)])
        total_trackers = len(self.config_manager.trackers)

        print(f"🌐 Tracker状态: {valid_trackers}/{total_trackers} 个有效")

        # 检查路径有效性
        resource_folder = self.config_manager.get_resource_folder()
        output_folder = self.config_manager.get_output_folder()

        import os
        print(f"📁 资源文件夹: {'✅ 存在' if os.path.exists(resource_folder) else '❌ 不存在'} ({resource_folder})")
        print(f"📂 输出文件夹: {'✅ 存在' if os.path.exists(output_folder) else '⚠️ 不存在'} ({output_folder})")

        print("=" * 50)

    def _get_folder_size_bytes(self, folder_path: str) -> int:
        """
        获取文件夹大小（字节）

        Args:
            folder_path: 文件夹路径

        Returns:
            文件夹大小（字节）
        """
        try:
            from pathlib import Path
            total_size = 0
            for file_path in Path(folder_path).rglob('*'):
                if file_path.is_file():
                    try:
                        total_size += file_path.stat().st_size
                    except (OSError, IOError):
                        continue
            return total_size
        except Exception:
            return 0

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