#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
版本管理器 - 统一管理项目中所有文件的版本号
确保版本号在所有相关文件中保持同步

作者：Torrent Maker Team
许可证：MIT
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class VersionManager:
    """版本管理器 - 统一管理项目版本号"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.version_config_file = self.project_root / "version_config.json"
        self.load_config()
    
    def load_config(self):
        """加载版本配置"""
        default_config = {
            "current_version": "1.2.0",
            "version_files": [
                {
                    "file": "torrent_maker.py",
                    "patterns": [
                        {
                            "pattern": r'版本：(\d+\.\d+\.\d+)',
                            "replacement": "版本：{version}"
                        },
                        {
                            "pattern": r'Torrent Maker - 单文件版本 v(\d+\.\d+\.\d+)',
                            "replacement": "Torrent Maker - 单文件版本 v{version}"
                        },
                        {
                            "pattern": r'Created by Torrent Maker v(\d+\.\d+\.\d+)',
                            "replacement": "Created by Torrent Maker v{version}"
                        },
                        {
                            "pattern": r'🚀 v(\d+\.\d+\.\d+) 重大更新:',
                            "replacement": "🚀 v{version} 重大更新:"
                        },
                        {
                            "pattern": r'Torrent Maker v(\d+\.\d+\.\d+) - 高性能优化版',
                            "replacement": "Torrent Maker v{version} - 高性能优化版"
                        }
                    ]
                },
                {
                    "file": "setup.py",
                    "patterns": [
                        {
                            "pattern": r"version='(\d+\.\d+\.\d+)'",
                            "replacement": "version='{version}'"
                        }
                    ]
                },
                {
                    "file": "src/main.py",
                    "patterns": [
                        {
                            "pattern": r'版本：(\d+\.\d+\.\d+)',
                            "replacement": "版本：{version}"
                        }
                    ]
                },
                {
                    "file": "README.md",
                    "patterns": [
                        {
                            "pattern": r'# Torrent Maker v(\d+\.\d+\.\d+)',
                            "replacement": "# Torrent Maker v{version}"
                        },
                        {
                            "pattern": r'当前版本：v(\d+\.\d+\.\d+)',
                            "replacement": "当前版本：v{version}"
                        }
                    ]
                }
            ],
            "changelog_file": "CHANGELOG.md",
            "release_notes_file": "RELEASE_NOTES.md"
        }
        
        if self.version_config_file.exists():
            try:
                with open(self.version_config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                # 合并默认配置
                for key, value in default_config.items():
                    if key not in self.config:
                        self.config[key] = value
            except Exception as e:
                print(f"❌ 加载版本配置失败: {e}")
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """保存版本配置"""
        try:
            with open(self.version_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"❌ 保存版本配置失败: {e}")
    
    def get_current_version(self) -> str:
        """获取当前版本号"""
        return self.config.get("current_version", "1.0.0")
    
    def set_version(self, new_version: str) -> bool:
        """设置新版本号并更新所有相关文件"""
        if not self._validate_version(new_version):
            print(f"❌ 无效的版本号格式: {new_version}")
            return False
        
        old_version = self.get_current_version()
        print(f"🔄 更新版本号: {old_version} -> {new_version}")
        
        # 更新所有文件
        success_count = 0
        total_files = len(self.config["version_files"])
        
        for file_config in self.config["version_files"]:
            if self._update_file_version(file_config, new_version):
                success_count += 1
            else:
                print(f"⚠️ 更新文件失败: {file_config['file']}")
        
        if success_count == total_files:
            # 更新配置中的版本号
            self.config["current_version"] = new_version
            self.save_config()
            
            # 更新变更日志
            self._update_changelog(old_version, new_version)
            
            print(f"✅ 版本号更新完成: {success_count}/{total_files} 个文件更新成功")
            return True
        else:
            print(f"❌ 版本号更新失败: 只有 {success_count}/{total_files} 个文件更新成功")
            return False
    
    def _validate_version(self, version: str) -> bool:
        """验证版本号格式 (语义化版本)"""
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version))
    
    def _update_file_version(self, file_config: Dict, new_version: str) -> bool:
        """更新单个文件的版本号"""
        file_path = self.project_root / file_config["file"]
        
        if not file_path.exists():
            print(f"⚠️ 文件不存在: {file_path}")
            return False
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 应用所有模式替换
            updated_content = content
            replacements_made = 0
            
            for pattern_config in file_config["patterns"]:
                pattern = pattern_config["pattern"]
                replacement = pattern_config["replacement"].format(version=new_version)
                
                new_content, count = re.subn(pattern, replacement, updated_content)
                if count > 0:
                    updated_content = new_content
                    replacements_made += count
            
            if replacements_made > 0:
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"✅ 更新文件: {file_config['file']} ({replacements_made} 处替换)")
                return True
            else:
                print(f"⚠️ 文件中未找到版本号模式: {file_config['file']}")
                return False
                
        except Exception as e:
            print(f"❌ 更新文件失败 {file_config['file']}: {e}")
            return False
    
    def _update_changelog(self, old_version: str, new_version: str):
        """更新变更日志"""
        changelog_path = self.project_root / self.config.get("changelog_file", "CHANGELOG.md")
        
        if not changelog_path.exists():
            print(f"⚠️ 变更日志文件不存在: {changelog_path}")
            return
        
        try:
            # 读取现有内容
            with open(changelog_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 准备新的版本条目
            today = datetime.now().strftime("%Y-%m-%d")
            new_entry = f"""
## [v{new_version}] - {today}

### 🚀 新功能
- 性能优化和改进

### 🔧 优化
- 代码质量提升
- 错误处理改进

### 🐛 修复
- 修复已知问题

"""
            
            # 在文件开头插入新条目（在标题后）
            lines = content.split('\n')
            insert_index = 0
            
            # 找到合适的插入位置（通常在第一个 ## 标题前）
            for i, line in enumerate(lines):
                if line.startswith('## ') and i > 0:
                    insert_index = i
                    break
            
            if insert_index > 0:
                lines.insert(insert_index, new_entry.strip())
                updated_content = '\n'.join(lines)
                
                with open(changelog_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"✅ 更新变更日志: {changelog_path}")
            
        except Exception as e:
            print(f"❌ 更新变更日志失败: {e}")
    
    def check_version_consistency(self) -> Dict[str, List[str]]:
        """检查版本号一致性"""
        current_version = self.get_current_version()
        inconsistent_files = {}
        
        for file_config in self.config["version_files"]:
            file_path = self.project_root / file_config["file"]
            
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                found_versions = []
                for pattern_config in file_config["patterns"]:
                    pattern = pattern_config["pattern"]
                    matches = re.findall(pattern, content)
                    found_versions.extend(matches)
                
                # 检查是否所有版本都与当前版本一致
                inconsistent_versions = [v for v in found_versions if v != current_version]
                if inconsistent_versions:
                    inconsistent_files[file_config["file"]] = inconsistent_versions
                    
            except Exception as e:
                print(f"❌ 检查文件失败 {file_config['file']}: {e}")
        
        return inconsistent_files
    
    def list_versions_in_files(self) -> Dict[str, List[str]]:
        """列出所有文件中找到的版本号"""
        versions_by_file = {}
        
        for file_config in self.config["version_files"]:
            file_path = self.project_root / file_config["file"]
            
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                found_versions = []
                for pattern_config in file_config["patterns"]:
                    pattern = pattern_config["pattern"]
                    matches = re.findall(pattern, content)
                    found_versions.extend(matches)
                
                if found_versions:
                    versions_by_file[file_config["file"]] = list(set(found_versions))
                    
            except Exception as e:
                print(f"❌ 读取文件失败 {file_config['file']}: {e}")
        
        return versions_by_file


def main():
    """主函数 - 命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Torrent Maker 版本管理器")
    parser.add_argument("--set", metavar="VERSION", help="设置新版本号 (例如: 1.3.0)")
    parser.add_argument("--check", action="store_true", help="检查版本号一致性")
    parser.add_argument("--list", action="store_true", help="列出所有文件中的版本号")
    parser.add_argument("--current", action="store_true", help="显示当前版本号")
    
    args = parser.parse_args()
    
    vm = VersionManager()
    
    if args.set:
        vm.set_version(args.set)
    elif args.check:
        inconsistent = vm.check_version_consistency()
        if inconsistent:
            print("❌ 发现版本号不一致:")
            for file, versions in inconsistent.items():
                print(f"  {file}: {versions}")
        else:
            print("✅ 所有文件版本号一致")
    elif args.list:
        versions = vm.list_versions_in_files()
        print("📋 文件中的版本号:")
        for file, versions in versions.items():
            print(f"  {file}: {versions}")
    elif args.current:
        print(f"当前版本: {vm.get_current_version()}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
