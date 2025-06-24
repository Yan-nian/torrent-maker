#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块

提供配置文件的读取、写入、验证和管理功能。
支持设置文件和tracker列表的管理。

作者：Torrent Maker Team
版本：1.2.0
"""

import json
import os
import logging
import shutil
import time
import re
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# 配置日志
logger = logging.getLogger(__name__)


class ConfigValidationError(Exception):
    """配置验证错误"""
    pass


class ConfigManager:
    """
    配置管理器

    负责管理应用程序的配置文件，包括设置文件和tracker列表。
    提供配置的读取、写入、验证和自动修复功能。
    """

    # 默认配置模板
    DEFAULT_SETTINGS = {
        "resource_folder": "~/Downloads",
        "output_folder": "output",
        "default_piece_size": "auto",
        "private_torrent": False,
        "file_search_tolerance": 60,
        "max_search_results": 10,
        "auto_create_output_dir": True,
        "enable_cache": True,
        "cache_duration": 3600,  # 缓存时长（秒）
        "max_concurrent_operations": 5,
        "log_level": "INFO"
    }

    DEFAULT_TRACKERS = [
        "udp://tracker.openbittorrent.com:80",
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://exodus.desync.com:6969/announce",
        "udp://tracker.torrent.eu.org:451/announce",
        "udp://tracker.coppersurfer.tk:6969/announce"
    ]

    def __init__(self, settings_path: str = 'config/settings.json',
                 trackers_path: str = 'config/trackers.txt'):
        """
        初始化配置管理器

        Args:
            settings_path: 设置文件路径
            trackers_path: tracker文件路径
        """
        self.settings_path = Path(settings_path)
        self.trackers_path = Path(trackers_path)

        # 确保配置文件存在
        self._ensure_config_files()

        # 加载配置
        self.settings = self._load_settings()
        self.trackers = self._load_trackers()

        # 验证配置
        self._validate_config()

    def _ensure_config_files(self) -> None:
        """
        确保配置文件和目录存在

        如果配置目录或文件不存在，则创建默认配置。
        """
        try:
            # 确保配置目录存在
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)

            # 如果配置文件不存在，创建默认配置
            if not self.settings_path.exists():
                self._create_default_settings()

            if not self.trackers_path.exists():
                self._create_default_trackers()

        except OSError as e:
            logger.error(f"创建配置文件失败: {e}")
            raise ConfigValidationError(f"无法创建配置文件: {e}")

    def _create_default_settings(self) -> None:
        """
        创建默认设置文件

        Raises:
            ConfigValidationError: 当无法创建设置文件时
        """
        try:
            # 展开用户目录路径
            settings = self.DEFAULT_SETTINGS.copy()
            settings['resource_folder'] = os.path.expanduser(settings['resource_folder'])

            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)

            logger.info(f"已创建默认配置文件: {self.settings_path}")

        except (OSError, json.JSONEncodeError) as e:
            logger.error(f"创建默认设置文件失败: {e}")
            raise ConfigValidationError(f"无法创建默认设置文件: {e}")

    def _create_default_trackers(self) -> None:
        """
        创建默认tracker文件

        Raises:
            ConfigValidationError: 当无法创建tracker文件时
        """
        try:
            with open(self.trackers_path, 'w', encoding='utf-8') as f:
                f.write("# BitTorrent Tracker 列表\n")
                f.write("# 每行一个 tracker URL，以 # 开头的行为注释\n\n")
                for tracker in self.DEFAULT_TRACKERS:
                    f.write(f"{tracker}\n")

            logger.info(f"已创建默认tracker文件: {self.trackers_path}")

        except OSError as e:
            logger.error(f"创建默认tracker文件失败: {e}")
            raise ConfigValidationError(f"无法创建默认tracker文件: {e}")

    def _load_settings(self) -> Dict[str, Any]:
        """
        加载设置文件

        Returns:
            设置字典，如果加载失败则返回默认设置
        """
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)

            # 展开用户目录路径
            if 'resource_folder' in settings:
                settings['resource_folder'] = os.path.expanduser(settings['resource_folder'])

            # 合并默认设置（确保所有必需的键都存在）
            merged_settings = self.DEFAULT_SETTINGS.copy()
            merged_settings.update(settings)

            return merged_settings

        except FileNotFoundError:
            logger.warning(f"设置文件未找到: {self.settings_path}，使用默认设置")
            return self.DEFAULT_SETTINGS.copy()

        except json.JSONDecodeError as e:
            logger.error(f"设置文件格式错误: {e}，使用默认设置")
            return self.DEFAULT_SETTINGS.copy()

        except Exception as e:
            logger.error(f"加载设置文件时发生未知错误: {e}，使用默认设置")
            return self.DEFAULT_SETTINGS.copy()

    def _load_trackers(self) -> List[str]:
        """
        加载tracker列表

        Returns:
            tracker URL列表，如果加载失败则返回默认tracker列表
        """
        try:
            with open(self.trackers_path, 'r', encoding='utf-8') as f:
                trackers = []
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # 简单验证URL格式
                        if self._is_valid_tracker_url(line):
                            trackers.append(line)
                        else:
                            logger.warning(f"跳过无效的tracker URL (行 {line_num}): {line}")

                return trackers if trackers else self.DEFAULT_TRACKERS.copy()

        except FileNotFoundError:
            logger.warning(f"Tracker文件未找到: {self.trackers_path}，使用默认tracker")
            return self.DEFAULT_TRACKERS.copy()

        except Exception as e:
            logger.error(f"加载tracker文件时发生错误: {e}，使用默认tracker")
            return self.DEFAULT_TRACKERS.copy()

    def _validate_config(self) -> None:
        """
        验证配置的有效性

        Raises:
            ConfigValidationError: 当配置无效时
        """
        # 验证必需的配置项
        required_keys = ['resource_folder', 'output_folder']
        for key in required_keys:
            if key not in self.settings:
                logger.error(f"缺少必需的配置项: {key}")
                raise ConfigValidationError(f"缺少必需的配置项: {key}")

        # 验证数值类型的配置
        numeric_configs = {
            'file_search_tolerance': (0, 100),
            'max_search_results': (1, 100),
            'cache_duration': (60, 86400),  # 1分钟到1天
            'max_concurrent_operations': (1, 20)
        }

        for key, (min_val, max_val) in numeric_configs.items():
            if key in self.settings:
                value = self.settings[key]
                if not isinstance(value, (int, float)) or not (min_val <= value <= max_val):
                    logger.warning(f"配置项 {key} 的值 {value} 无效，使用默认值")
                    self.settings[key] = self.DEFAULT_SETTINGS[key]

        # 验证布尔类型的配置
        boolean_configs = ['auto_create_output_dir', 'enable_cache', 'private_torrent']
        for key in boolean_configs:
            if key in self.settings and not isinstance(self.settings[key], bool):
                logger.warning(f"配置项 {key} 的值 {self.settings[key]} 不是布尔类型，使用默认值")
                self.settings[key] = self.DEFAULT_SETTINGS.get(key, False)

        # 验证字符串类型的配置
        string_configs = ['default_piece_size', 'log_level']
        for key in string_configs:
            if key in self.settings and not isinstance(self.settings[key], str):
                logger.warning(f"配置项 {key} 的值 {self.settings[key]} 不是字符串类型，使用默认值")
                self.settings[key] = self.DEFAULT_SETTINGS.get(key, "")

        # 验证tracker URL的有效性
        valid_trackers = []
        for tracker in self.trackers:
            if self._is_valid_tracker_url(tracker):
                valid_trackers.append(tracker)
            else:
                logger.warning(f"无效的tracker URL: {tracker}")

        if len(valid_trackers) != len(self.trackers):
            self.trackers = valid_trackers
            if not self.trackers:  # 如果没有有效的tracker，使用默认值
                logger.warning("没有有效的tracker，使用默认tracker列表")
                self.trackers = self.DEFAULT_TRACKERS.copy()
                self.save_trackers()

    def _is_valid_tracker_url(self, url: str) -> bool:
        """
        验证tracker URL的有效性

        Args:
            url: tracker URL

        Returns:
            URL是否有效
        """
        if not isinstance(url, str) or not url.strip():
            return False

        # 简单的URL格式验证
        pattern = r'^(https?|udp)://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url.strip(), re.IGNORECASE))



    def get_resource_folder(self) -> str:
        """
        获取资源文件夹路径

        Returns:
            资源文件夹的绝对路径
        """
        return os.path.abspath(self.settings.get('resource_folder', os.path.expanduser("~/Downloads")))

    def set_resource_folder(self, path: str) -> bool:
        """
        设置资源文件夹路径

        Args:
            path: 新的资源文件夹路径

        Returns:
            设置成功返回True，否则返回False
        """
        try:
            expanded_path = os.path.expanduser(path)
            expanded_path = os.path.abspath(expanded_path)

            # 检查路径是否存在或可以创建
            if not os.path.exists(expanded_path):
                logger.warning(f"路径不存在: {expanded_path}")
                return False

            if not os.path.isdir(expanded_path):
                logger.error(f"路径不是目录: {expanded_path}")
                return False

            self.settings['resource_folder'] = expanded_path
            self._save_settings()
            logger.info(f"资源文件夹已设置为: {expanded_path}")
            return True

        except Exception as e:
            logger.error(f"设置资源文件夹失败: {e}")
            return False

    def get_output_folder(self) -> str:
        """
        获取种子输出文件夹路径

        Returns:
            输出文件夹的绝对路径
        """
        output_path = self.settings.get('output_folder', 'output')
        return os.path.abspath(os.path.expanduser(output_path))

    def set_output_folder(self, path: str) -> bool:
        """
        设置种子输出文件夹路径

        Args:
            path: 新的输出文件夹路径

        Returns:
            设置成功返回True，否则返回False
        """
        try:
            expanded_path = os.path.expanduser(path)
            expanded_path = os.path.abspath(expanded_path)

            self.settings['output_folder'] = expanded_path
            self._save_settings()
            logger.info(f"种子输出文件夹已设置为: {expanded_path}")
            return True

        except Exception as e:
            logger.error(f"设置输出文件夹失败: {e}")
            return False

    def get_trackers(self) -> List[str]:
        """
        获取tracker列表的副本

        Returns:
            tracker URL列表
        """
        return self.trackers.copy()

    def add_tracker(self, tracker_url: str) -> bool:
        """
        添加新的tracker

        Args:
            tracker_url: tracker URL

        Returns:
            添加成功返回True，否则返回False
        """
        try:
            tracker_url = tracker_url.strip()

            if not tracker_url:
                logger.error("Tracker URL不能为空")
                return False

            if not self._is_valid_tracker_url(tracker_url):
                logger.error(f"无效的tracker URL: {tracker_url}")
                return False

            if tracker_url in self.trackers:
                logger.warning(f"Tracker已存在: {tracker_url}")
                return False

            self.trackers.append(tracker_url)
            self._save_trackers()
            logger.info(f"已添加tracker: {tracker_url}")
            return True

        except Exception as e:
            logger.error(f"添加tracker失败: {e}")
            return False

    def remove_tracker(self, tracker_url: str) -> bool:
        """
        移除tracker

        Args:
            tracker_url: 要移除的tracker URL

        Returns:
            移除成功返回True，否则返回False
        """
        try:
            if tracker_url in self.trackers:
                self.trackers.remove(tracker_url)
                self._save_trackers()
                logger.info(f"已移除tracker: {tracker_url}")
                return True
            else:
                logger.warning(f"Tracker不存在: {tracker_url}")
                return False

        except Exception as e:
            logger.error(f"移除tracker失败: {e}")
            return False

    def _save_settings(self) -> None:
        """
        保存设置到文件

        Raises:
            ConfigValidationError: 当保存失败时
        """
        try:
            # 创建备份
            backup_path = self.settings_path.with_suffix('.bak')
            if self.settings_path.exists():
                import shutil
                shutil.copy2(self.settings_path, backup_path)

            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)

            logger.debug("设置已保存")

        except Exception as e:
            logger.error(f"保存设置失败: {e}")
            # 尝试恢复备份
            if backup_path.exists():
                try:
                    import shutil
                    shutil.copy2(backup_path, self.settings_path)
                    logger.info("已从备份恢复设置文件")
                except Exception as restore_error:
                    logger.error(f"恢复备份失败: {restore_error}")
            raise ConfigValidationError(f"保存设置失败: {e}")

    def _save_trackers(self) -> None:
        """
        保存tracker列表到文件

        Raises:
            ConfigValidationError: 当保存失败时
        """
        try:
            # 创建备份
            backup_path = self.trackers_path.with_suffix('.bak')
            if self.trackers_path.exists():
                import shutil
                shutil.copy2(self.trackers_path, backup_path)

            with open(self.trackers_path, 'w', encoding='utf-8') as f:
                f.write("# BitTorrent Tracker 列表\n")
                f.write("# 每行一个 tracker URL，以 # 开头的行为注释\n\n")
                for tracker in self.trackers:
                    f.write(f"{tracker}\n")

            logger.debug("Tracker列表已保存")

        except Exception as e:
            logger.error(f"保存tracker列表失败: {e}")
            # 尝试恢复备份
            if backup_path.exists():
                try:
                    import shutil
                    shutil.copy2(backup_path, self.trackers_path)
                    logger.info("已从备份恢复tracker文件")
                except Exception as restore_error:
                    logger.error(f"恢复备份失败: {restore_error}")
            raise ConfigValidationError(f"保存tracker列表失败: {e}")

    def update_settings(self, new_settings: Dict[str, Any]) -> bool:
        """
        批量更新设置

        Args:
            new_settings: 新的设置字典

        Returns:
            更新成功返回True，否则返回False
        """
        try:
            # 验证新设置
            old_settings = self.settings.copy()
            self.settings.update(new_settings)

            try:
                self._validate_config()
                self._save_settings()
                logger.info("设置已更新")
                return True
            except ConfigValidationError:
                # 恢复旧设置
                self.settings = old_settings
                logger.error("新设置验证失败，已恢复原设置")
                return False

        except Exception as e:
            logger.error(f"更新设置失败: {e}")
            return False

    def get_setting(self, key: str, default=None):
        """
        获取单个设置项

        Args:
            key: 设置项键名
            default: 默认值

        Returns:
            设置项的值
        """
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> bool:
        """
        设置单个配置项

        Args:
            key: 设置项键名
            value: 设置项的值

        Returns:
            设置成功返回True，否则返回False
        """
        try:
            old_value = self.settings.get(key)
            self.settings[key] = value

            try:
                self._validate_config()
                self._save_settings()
                logger.info(f"设置项 {key} 已更新: {old_value} -> {value}")
                return True
            except ConfigValidationError:
                # 恢复旧值
                if old_value is not None:
                    self.settings[key] = old_value
                else:
                    self.settings.pop(key, None)
                logger.error(f"设置项 {key} 验证失败，已恢复原值")
                return False

        except Exception as e:
            logger.error(f"设置配置项失败: {e}")
            return False

    def reset_to_defaults(self) -> bool:
        """
        重置所有设置为默认值

        Returns:
            重置成功返回True，否则返回False
        """
        try:
            self.settings = self.DEFAULT_SETTINGS.copy()
            self.trackers = self.DEFAULT_TRACKERS.copy()

            # 展开用户目录路径
            self.settings['resource_folder'] = os.path.expanduser(self.settings['resource_folder'])

            self._save_settings()
            self._save_trackers()

            logger.info("配置已重置为默认值")
            return True

        except Exception as e:
            logger.error(f"重置配置失败: {e}")
            return False

    def display_current_config(self) -> None:
        """显示当前配置信息"""
        print("=" * 50)
        print("           📋 当前配置信息")
        print("=" * 50)
        print(f"📁 资源文件夹: {self.get_resource_folder()}")
        print(f"📂 输出文件夹: {self.get_output_folder()}")
        print(f"🔍 搜索容忍度: {self.settings.get('file_search_tolerance', 60)}%")
        print(f"📊 最大搜索结果: {self.settings.get('max_search_results', 10)}")
        print(f"🌐 Tracker数量: {len(self.trackers)}")
        print(f"💾 启用缓存: {'是' if self.settings.get('enable_cache', True) else '否'}")
        print(f"⚡ 最大并发操作: {self.settings.get('max_concurrent_operations', 5)}")

        print("\n🌐 Tracker列表:")
        if self.trackers:
            for i, tracker in enumerate(self.trackers, 1):
                print(f"  {i:2d}. {tracker}")
        else:
            print("  暂无配置的Tracker")
        print("=" * 50)

    def export_config(self, export_path: str) -> bool:
        """
        导出配置到指定文件

        Args:
            export_path: 导出文件路径

        Returns:
            导出成功返回True，否则返回False
        """
        try:
            export_data = {
                'settings': self.settings,
                'trackers': self.trackers,
                'export_time': str(Path(__file__).stat().st_mtime),
                'version': '1.2.0'
            }

            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=4)

            logger.info(f"配置已导出到: {export_path}")
            return True

        except Exception as e:
            logger.error(f"导出配置失败: {e}")
            return False

    def import_config(self, import_path: str) -> bool:
        """
        从文件导入配置

        Args:
            import_path: 导入文件路径

        Returns:
            导入成功返回True，否则返回False
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            # 备份当前配置
            backup_settings = self.settings.copy()
            backup_trackers = self.trackers.copy()

            try:
                # 导入新配置
                if 'settings' in import_data:
                    self.settings = import_data['settings']
                if 'trackers' in import_data:
                    self.trackers = import_data['trackers']

                # 验证配置
                self._validate_config()

                # 保存配置
                self._save_settings()
                self._save_trackers()

                logger.info(f"配置已从 {import_path} 导入")
                return True

            except Exception as e:
                # 恢复备份
                self.settings = backup_settings
                self.trackers = backup_trackers
                logger.error(f"导入配置失败，已恢复原配置: {e}")
                return False

        except Exception as e:
            logger.error(f"读取导入文件失败: {e}")
            return False

    def backup_config(self) -> bool:
        """
        备份当前配置

        Returns:
            备份成功返回True，否则返回False
        """
        try:
            backup_dir = Path(self.settings_path).parent / "backups"
            backup_dir.mkdir(exist_ok=True)

            timestamp = time.strftime('%Y%m%d_%H%M%S')

            # 备份设置文件
            if self.settings_path.exists():
                backup_settings = backup_dir / f"settings_{timestamp}.json"
                shutil.copy2(self.settings_path, backup_settings)

            # 备份tracker文件
            if self.trackers_path.exists():
                backup_trackers = backup_dir / f"trackers_{timestamp}.txt"
                shutil.copy2(self.trackers_path, backup_trackers)

            logger.info(f"配置已备份到: {backup_dir}")
            return True

        except Exception as e:
            logger.error(f"备份配置失败: {e}")
            return False

    def restore_backup(self, backup_timestamp: str = None) -> bool:
        """
        恢复备份配置

        Args:
            backup_timestamp: 备份时间戳，None表示恢复最新备份

        Returns:
            恢复成功返回True，否则返回False
        """
        try:
            backup_dir = Path(self.settings_path).parent / "backups"
            if not backup_dir.exists():
                logger.error("备份目录不存在")
                return False

            if backup_timestamp:
                # 恢复指定时间戳的备份
                settings_backup = backup_dir / f"settings_{backup_timestamp}.json"
                trackers_backup = backup_dir / f"trackers_{backup_timestamp}.txt"
            else:
                # 查找最新的备份文件
                settings_backups = list(backup_dir.glob("settings_*.json"))
                trackers_backups = list(backup_dir.glob("trackers_*.txt"))

                if not settings_backups:
                    logger.error("没有找到设置文件备份")
                    return False

                settings_backup = max(settings_backups, key=lambda x: x.stat().st_mtime)
                trackers_backup = max(trackers_backups, key=lambda x: x.stat().st_mtime) if trackers_backups else None

            # 恢复设置文件
            if settings_backup.exists():
                shutil.copy2(settings_backup, self.settings_path)
                logger.info(f"已恢复设置文件: {settings_backup}")

            # 恢复tracker文件
            if trackers_backup and trackers_backup.exists():
                shutil.copy2(trackers_backup, self.trackers_path)
                logger.info(f"已恢复tracker文件: {trackers_backup}")

            # 重新加载配置
            self.settings = self._load_settings()
            self.trackers = self._load_trackers()

            return True

        except Exception as e:
            logger.error(f"恢复备份配置失败: {e}")
            return False

    def get_config_status(self) -> Dict[str, Any]:
        """
        获取配置状态信息

        Returns:
            配置状态信息字典
        """
        try:
            status = {
                'settings_file': {
                    'path': str(self.settings_path),
                    'exists': self.settings_path.exists(),
                    'size': self.settings_path.stat().st_size if self.settings_path.exists() else 0,
                    'modified': time.ctime(self.settings_path.stat().st_mtime) if self.settings_path.exists() else None
                },
                'trackers_file': {
                    'path': str(self.trackers_path),
                    'exists': self.trackers_path.exists(),
                    'size': self.trackers_path.stat().st_size if self.trackers_path.exists() else 0,
                    'modified': time.ctime(self.trackers_path.stat().st_mtime) if self.trackers_path.exists() else None
                },
                'settings_count': len(self.settings),
                'trackers_count': len(self.trackers),
                'valid_trackers': len([t for t in self.trackers if self._is_valid_tracker_url(t)]),
                'backup_dir': str(Path(self.settings_path).parent / "backups"),
                'has_backups': (Path(self.settings_path).parent / "backups").exists()
            }

            return status

        except Exception as e:
            logger.error(f"获取配置状态失败: {e}")
            return {}

    def validate_and_repair(self) -> Dict[str, Any]:
        """
        验证并修复配置

        Returns:
            修复结果报告
        """
        repair_report = {
            'issues_found': [],
            'repairs_made': [],
            'warnings': []
        }

        try:
            # 检查配置文件完整性
            if not self.settings_path.exists():
                repair_report['issues_found'].append("设置文件不存在")
                self._create_default_settings()
                repair_report['repairs_made'].append("已创建默认设置文件")

            if not self.trackers_path.exists():
                repair_report['issues_found'].append("Tracker文件不存在")
                self._create_default_trackers()
                repair_report['repairs_made'].append("已创建默认Tracker文件")

            # 检查必需的配置项
            required_keys = ['resource_folder', 'output_folder']
            for key in required_keys:
                if key not in self.settings:
                    repair_report['issues_found'].append(f"缺少必需配置项: {key}")
                    self.settings[key] = self.DEFAULT_SETTINGS[key]
                    repair_report['repairs_made'].append(f"已添加默认配置项: {key}")

            # 检查tracker有效性
            invalid_trackers = [t for t in self.trackers if not self._is_valid_tracker_url(t)]
            if invalid_trackers:
                repair_report['issues_found'].append(f"发现 {len(invalid_trackers)} 个无效tracker")
                self.trackers = [t for t in self.trackers if self._is_valid_tracker_url(t)]
                repair_report['repairs_made'].append(f"已移除 {len(invalid_trackers)} 个无效tracker")

            # 检查目录是否存在
            resource_folder = self.get_resource_folder()
            if not os.path.exists(resource_folder):
                repair_report['warnings'].append(f"资源文件夹不存在: {resource_folder}")

            # 保存修复后的配置
            if repair_report['repairs_made']:
                self._save_settings()
                self._save_trackers()

            return repair_report

        except Exception as e:
            logger.error(f"配置验证和修复失败: {e}")
            repair_report['issues_found'].append(f"验证过程出错: {e}")
            return repair_report