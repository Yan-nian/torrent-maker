#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Torrent Maker - 单文件版本 v2.1.0
基于 mktorrent 的高性能半自动化种子制作工具

🌐 v2.1.0 Web界面增强版本:
- 🌐 全新Web界面：基于Flask + WebSocket的现代化界面
- 🖥️ 多服务器SSH连接：支持远程服务器制种管理
- 📊 实时进度监控：WebSocket推送制种进度和系统状态
- 🎯 任务队列管理：可视化任务队列和批量操作
- 📱 移动端适配：响应式设计支持手机平板访问
- 🔐 安全连接：SSH密钥和密码认证支持
- 🚀 启动脚本：一键启动Web界面和依赖检查
- 📋 配置管理：YAML格式的服务器配置文件

🎯 v2.0.2 批量制种修复版本:
- 🔧 修复TorrentProgressMonitor缺失start_monitoring方法
- 🔧 修复TorrentProgressMonitor缺失stop_monitoring方法
- 📊 增强进度监控功能和状态管理
- ✅ 解决批量制种失败问题
- 📦 自动生成发布包和安装说明
- 🛠️ 增加手动发布备用流程
- ✨ 优化发布流程的用户体验

🎯 v2.0.0 一键安装脚本重构版本:
- 🔧 完全重构安装脚本，从1186行简化为150行标准版
- ✨ 统一安装流程：检查mktorrent、安装依赖、安装最新程序
- 🚀 支持macOS、Ubuntu、Debian、CentOS、RHEL多平台
- 📋 增强错误处理和用户友好的彩色输出
- 🛡️ 提升安装脚本的稳定性和维护性
- ⚡ 优化版本检测逻辑，支持本地和远程版本获取

🎯 v1.9.19 制种命名修复版本:
- 🔧 修复队列制种时文件命名错误问题（从-root_pack_时间戳修复为正确的文件夹名_时间戳）
- ✅ 修正TorrentQueueManager中create_torrent参数传递错误
- 🔄 正确设置TorrentCreator输出目录，确保文件保存到指定位置
- 📋 优化队列任务执行逻辑，提升制种文件命名准确性
- 🚀 确保批量制种和队列管理功能的文件命名正确性

🎯 v1.9.16 队列管理类型错误修复版本:
- 🔧 修复队列管理中字符串与整数比较的类型错误
- 🛡️ 增强任务数据序列化/反序列化的安全性
- 📋 改进枚举类型转换的容错处理
- 🚀 提升队列管理系统的稳定性

🎯 v1.9.15 制种失败问题修复版本:
- 🔧 修复tracker URL格式错误（移除反引号等非法字符）
- ✅ 改进时间戳精度到微秒级，解决文件名冲突问题
- 🔄 添加文件冲突检测和重试机制
- 📋 增强URL格式验证，提升制种成功率
- 🚀 提升制种系统的稳定性和可靠性

🎯 v1.9.14 队列管理修复版本:
- 🔧 修复队列详情显示为空的问题
- ✅ 修正队列文件保存路径不一致导致的数据丢失
- 🔄 确保队列状态和任务数据同步显示
- 📋 修复队列管理功能的数据持久化问题
- 🚀 提升队列管理系统的稳定性和可靠性

🎯 v1.9.13 搜索历史快捷键增强版本:
- ✨ 新增搜索历史快捷键选择功能（输入数字1-5直接选择历史搜索）
- 🔍 优化搜索界面提示信息，支持快捷键和手动输入双模式
- 🎯 增强用户体验，快速重复搜索更加便捷
- 📋 兼容现有搜索历史数据结构，无缝升级
- 🚀 提升搜索效率和操作便捷性

🎯 v1.9.10 搜索历史兼容性修复版本:
- 🔧 修复搜索历史显示中的 'str' object has no attribute 'query' 错误
- ✅ 增强搜索历史数据结构兼容性处理
- 🔄 修复主菜单和搜索历史管理中的显示问题
- 📋 确保不同 SearchHistory 实现的兼容性
- 🚀 提升程序稳定性和用户体验

🎯 v1.9.9 PathCompleter修复版本:
- 🔧 修复 PathCompleter 缺少 get_input 方法的问题
- ✅ 添加支持路径补全的用户输入功能
- 🔄 完善路径历史记录和自动补全机制
- 📋 确保智能搜索和批量制种功能正常
- 🚀 提升用户交互体验和操作便捷性

🎯 v1.9.8 增强功能测试修复版本:
- 🔧 修复增强功能模块测试问题
- ✅ 完善 PathCompleter、TorrentProgressMonitor 功能
- 🔄 修复 SearchHistory 和 SmartSearchSuggester 兼容性
- 📋 解决文件权限和方法缺失问题
- 🚀 确保所有增强功能正常工作

🎯 v1.9.4 队列管理功能修复版本:
- 🔧 修复队列管理功能不可用问题
- ✅ 修复 TorrentCreator 与 ConfigManager 集成
- 🔄 恢复队列管理系统完整功能
- 📋 修复任务状态跟踪和进度监控
- 🚀 确保批量制种和队列控制正常工作

🎯 v1.9.2 队列管理与预设优化版本:
- 🔄 队列管理系统（任务队列、进度监控、批量控制）
- ⚡ 预设模式管理（内置预设、自定义预设、自动检测）
- 📋 任务状态跟踪（等待、运行、完成、失败状态管理）
- 🎛️ 高级配置界面（预设选择、队列控制、统计报告）
- 🚀 批量制种优化（并发处理、智能调度、性能监控）

🎯 v1.9.1 用户体验优化版本:
- 🔍 智能路径补全功能（Tab键补全、历史记录、智能建议）
- 📊 实时制种进度监控（进度条、可视化、性能统计）
- 📝 搜索历史管理（历史记录、热门搜索、智能建议）
- ⚡ 制种过程控制（进度取消、暂停恢复、多任务管理）
- 🎨 用户界面全面优化（交互体验、视觉提示、操作便捷性）

🎯 v1.9.0 性能监控增强版本:
- ⏰ 新增制种时间显示功能（开始时间、完成时间、总耗时）
- 🧵 智能多线程检测与优化（自动检测最优线程数）
- 📊 详细性能信息展示（制种速度、效率分析、性能建议）
- 🎨 用户界面优化（清晰的信息布局和视觉提示）
- 💡 智能性能建议系统（根据系统状态提供优化建议）

🎯 v1.6.0 彻底重构版本:
- 🗂️ 项目结构彻底简化，移除所有模块化组件
- 📦 单文件架构，下载即用，无需复杂配置
- 🧹 删除 80% 冗余文件，项目体积减少 80%
- 📖 文档完全重写，专注单文件版本使用
- ⚡ 安装流程简化，一键完成所有配置
- 🎨 用户体验优化，操作更加直观简洁

🚀 继承 v1.5.1 所有性能优化:
- ⚡ 种子创建速度提升 30-50%
- 🧠 智能 Piece Size 计算，减少计算时间 80%
- 💾 目录大小缓存优化，支持 LRU 淘汰策略
- 🔧 mktorrent 参数优化，启用多线程处理
- 🔄 批量处理并发优化，支持进程池处理
- 📊 增强性能监控和统计分析
- 🎯 智能查找表，O(1) 时间复杂度优化

🛡️ 继承 v1.5.1 所有稳定性修复:
- 🐛 修复 macOS 内存使用计算错误
- ⚡ 优化文件夹扫描性能，添加超时和数量限制
- 🔍 修复搜索功能，恢复文件夹匹配能力
- 🛡️ 增强扫描稳定性，防止大文件夹导致的卡死

项目特点:
- 📦 真正的单文件应用，包含所有功能
- 🚀 极简安装，一个命令完成
- 📖 清晰文档，专注核心功能
- 🔧 易于维护，单一代码路径

使用方法：
    python torrent_maker.py

作者：Torrent Maker Team
许可证：MIT
版本：1.9.0
"""

import os
import sys
import json
import subprocess
import shutil
import time
import logging
import hashlib
import threading
import re
from datetime import datetime

from typing import List, Dict, Any, Tuple, Optional, Union, Set
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

# 所有功能已内置到单文件中
ENHANCED_FEATURES_AVAILABLE = True

# 配置日志
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# ================== 版本信息 ==================
VERSION = "v2.2.0"
VERSION_NAME = "远程文件浏览器版"
FULL_VERSION_INFO = f"Torrent Maker {VERSION} - {VERSION_NAME}"
# 触发GitHub Actions自动发布 - 2025-06-27


# ================== 队列管理模块 ==================
import uuid
from enum import Enum
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, PriorityQueue

class TaskStatus(Enum):
    """任务状态枚举"""
    WAITING = "waiting"      # 等待执行
    RUNNING = "running"      # 正在执行
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 执行失败
    PAUSED = "paused"        # 已暂停
    CANCELLED = "cancelled"  # 已取消


class TaskPriority(Enum):
    """任务优先级枚举"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0


@dataclass
class QueueTask:
    """队列任务数据类"""
    id: str
    name: str
    path: str
    status: TaskStatus = TaskStatus.WAITING
    priority: TaskPriority = TaskPriority.NORMAL
    progress: float = 0.0
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error_message: str = ""
    preset: str = "standard"
    output_path: str = ""
    file_size: int = 0
    created_time: float = None
    estimated_duration: float = 0.0
    actual_duration: float = 0.0
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if self.created_time is None:
            self.created_time = time.time()
    
    def __lt__(self, other):
        """用于优先级队列排序"""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.created_time < other.created_time
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        data = asdict(self)
        data['status'] = self.status.value
        data['priority'] = self.priority.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueueTask':
        """从字典创建任务对象"""
        # 安全转换状态枚举
        try:
            if isinstance(data['status'], str):
                data['status'] = TaskStatus[data['status']]
            else:
                data['status'] = TaskStatus(data['status'])
        except (KeyError, ValueError):
            data['status'] = TaskStatus.WAITING
        
        # 安全转换优先级枚举
        try:
            if isinstance(data['priority'], str):
                # 如果是字符串，尝试按名称查找
                data['priority'] = TaskPriority[data['priority']]
            else:
                # 如果是数字，按值查找
                data['priority'] = TaskPriority(int(data['priority']))
        except (KeyError, ValueError, TypeError):
            data['priority'] = TaskPriority.NORMAL
        
        return cls(**data)


class QueueStatusDisplay:
    """队列状态显示管理类"""
    
    def __init__(self):
        self.last_display_time = 0
        self.last_status_hash = None
        self.display_interval = 1.0  # 最小显示间隔（秒）
    
    def display_status(self, queue_manager, mode: str = "standard", force_update: bool = False):
        """统一的队列状态显示接口
        
        Args:
            queue_manager: 队列管理器实例
            mode: 显示模式 ('compact', 'standard', 'detailed')
            force_update: 强制更新显示
        """
        if not queue_manager:
            print("❌ 队列管理器不可用")
            return
        
        # 获取状态信息
        status = queue_manager.get_queue_status()
        current_time = time.time()
        
        # 生成状态哈希，用于检测变化
        status_hash = self._generate_status_hash(status)
        
        # 检查是否需要更新显示
        if not force_update:
            if (current_time - self.last_display_time < self.display_interval and 
                status_hash == self.last_status_hash):
                return
        
        # 根据模式显示信息
        if mode == "compact":
            self._display_compact_status(status)
        elif mode == "detailed":
            self._display_detailed_status(status, queue_manager)
        else:  # standard
            self._display_standard_status(status)
        
        # 更新显示记录
        self.last_display_time = current_time
        self.last_status_hash = status_hash
    
    def _generate_status_hash(self, status: dict) -> str:
        """生成状态哈希值用于变化检测"""
        import hashlib
        key_info = {
            'running': status.get('running', False),
            'paused': status.get('paused', False),
            'current_running': status.get('current_running', 0),
            'waiting_tasks': status.get('waiting_tasks', 0),
            'total_tasks': status.get('total_tasks', 0),
            'completed': status.get('statistics', {}).get('completed_tasks', 0),
            'failed': status.get('statistics', {}).get('failed_tasks', 0)
        }
        return hashlib.md5(str(key_info).encode()).hexdigest()
    
    def _display_compact_status(self, status: dict):
        """简洁模式显示"""
        running_status = "🟢 运行中" if status['running'] and not status['paused'] else "🟡 暂停" if status['paused'] else "🔴 已停止"
        print(f"📊 队列: {running_status} | 任务: {status['current_running']}/{status['max_concurrent']} | 等待: {status['waiting_tasks']}")
    
    def _display_standard_status(self, status: dict):
        """标准模式显示"""
        print(f"\n📊 队列状态: {'🟢 运行中' if status['running'] and not status['paused'] else '🟡 暂停' if status['paused'] else '🔴 已停止'}")
        print(f"⚡ 并发数: {status['current_running']}/{status['max_concurrent']}")
        print(f"📋 等待任务: {status['waiting_tasks']} | 总任务: {status['total_tasks']}")
        
        stats = status['statistics']
        print(f"✅ 已完成: {stats['completed_tasks']} | ❌ 失败: {stats['failed_tasks']}")
        if stats['average_processing_time'] > 0:
            print(f"⏱️ 平均处理时间: {stats['average_processing_time']:.1f}秒")
    
    def _display_detailed_status(self, status: dict, queue_manager):
        """详细模式显示"""
        print("\n" + "="*60)
        print("           📊 队列详细状态")
        print("="*60)
        
        # 基本状态
        self._display_standard_status(status)
        
        # 正在运行的任务
        running_tasks = [task for task in queue_manager.get_all_tasks() 
                        if task.status == TaskStatus.RUNNING]
        if running_tasks:
            print(f"\n🔄 正在处理 ({len(running_tasks)} 个任务):")
            for task in running_tasks:
                progress_str = f" ({task.progress*100:.1f}%)" if task.progress > 0 else ""
                print(f"  • {task.name}{progress_str}")
        
        # 等待队列
        waiting_tasks = [task for task in queue_manager.get_all_tasks() 
                        if task.status == TaskStatus.WAITING]
        if waiting_tasks:
            print(f"\n⏳ 等待队列 ({len(waiting_tasks)} 个任务):")
            for i, task in enumerate(waiting_tasks[:5], 1):
                print(f"  {i}. {task.name}")
            if len(waiting_tasks) > 5:
                print(f"     ... 还有 {len(waiting_tasks) - 5} 个任务")
        
        # 性能统计
        stats = status['statistics']
        if stats['completed_tasks'] > 0 or stats['failed_tasks'] > 0:
            print(f"\n📈 性能统计:")
            print(f"  总处理时间: {stats['total_processing_time']:.1f}秒")
            if stats['completed_tasks'] > 0:
                success_rate = (stats['completed_tasks'] / (stats['completed_tasks'] + stats['failed_tasks'])) * 100
                print(f"  成功率: {success_rate:.1f}%")
        
        print("="*60)


class QueueManager:
    """队列管理器"""
    
    def __init__(self, max_concurrent: int = 4, save_file: Optional[str] = None):
        self.max_concurrent = max_concurrent
        self.save_file = save_file or os.path.expanduser("~/.torrent_maker/queue.json")
        
        # 任务存储
        self.tasks: Dict[str, QueueTask] = {}
        self.priority_queue = PriorityQueue()
        self.running_tasks: Dict[str, QueueTask] = {}
        
        # 线程管理
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent)
        self.worker_threads: Dict[str, Any] = {}
        
        # 同步锁
        self._lock = threading.RLock()
        self._running = False
        self._paused = False
        
        # 统计信息
        self.stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'total_processing_time': 0.0,
            'average_processing_time': 0.0
        }
        
        # 回调函数
        self.on_task_start: Optional[Callable[[QueueTask], None]] = None
        self.on_task_complete: Optional[Callable[[QueueTask], None]] = None
        self.on_task_failed: Optional[Callable[[QueueTask, str], None]] = None
        self.on_progress_update: Optional[Callable[[QueueTask], None]] = None
        
        # 设置日志
        self.logger = self._setup_logger()
        
        # 加载保存的队列
        self._load_queue()
    
    def set_callbacks(self, on_task_start=None, on_task_complete=None, 
                     on_task_failed=None, on_progress_update=None):
        """设置回调函数"""
        if on_task_start:
            self.on_task_start = on_task_start
        if on_task_complete:
            self.on_task_complete = on_task_complete
        if on_task_failed:
            self.on_task_failed = on_task_failed
        if on_progress_update:
            self.on_progress_update = on_progress_update
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('queue_manager')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def add_task(self, name: str, path: str, priority: TaskPriority = TaskPriority.NORMAL, 
                 preset: str = "standard", output_path: str = "") -> str:
        """添加任务到队列"""
        with self._lock:
            task_id = str(uuid.uuid4())
            
            # 获取文件大小
            file_size = 0
            try:
                if os.path.isfile(path):
                    file_size = os.path.getsize(path)
                elif os.path.isdir(path):
                    file_size = self._calculate_directory_size(path)
            except OSError:
                pass
            
            task = QueueTask(
                id=task_id,
                name=name,
                path=path,
                priority=priority,
                preset=preset,
                output_path=output_path,
                file_size=file_size
            )
            
            self.tasks[task_id] = task
            self.priority_queue.put(task)
            self.stats['total_tasks'] += 1
            
            self.logger.info(f"任务已添加: {name} (ID: {task_id})")
            self._save_queue()
            
            # 如果队列正在运行，尝试启动新任务
            if self._running:
                self._try_start_next_task()
            
            return task_id
    
    def _calculate_directory_size(self, path: str) -> int:
        """计算目录大小"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(file_path)
                    except OSError:
                        continue
        except OSError:
            pass
        return total_size
    
    def remove_task(self, task_id: str) -> bool:
        """移除任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            # 如果任务正在运行，先取消它
            if task.status == TaskStatus.RUNNING:
                self.cancel_task(task_id)
            
            # 从任务字典中移除
            del self.tasks[task_id]
            
            # 从运行任务中移除
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
            
            # 重建优先级队列（移除已删除的任务）
            self._rebuild_priority_queue()
            
            self.logger.info(f"任务已移除: {task.name} (ID: {task_id})")
            self._save_queue()
            return True
    
    def _rebuild_priority_queue(self):
        """重建优先级队列，移除已删除的任务"""
        # 创建新的优先级队列
        new_queue = queue.PriorityQueue()
        
        # 将现有队列中的有效任务重新加入
        while not self.priority_queue.empty():
            try:
                task = self.priority_queue.get_nowait()
                # 只有在tasks字典中存在的任务才重新加入队列
                if task.id in self.tasks:
                    new_queue.put(task)
            except queue.Empty:
                break
        
        # 替换旧队列
        self.priority_queue = new_queue
    
    def pause_task(self, task_id: str) -> bool:
        """暂停任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            if task.status == TaskStatus.RUNNING:
                # 取消正在运行的任务
                self._cancel_running_task(task_id)
                task.status = TaskStatus.PAUSED
                self.logger.info(f"任务已暂停: {task.name} (ID: {task_id})")
            elif task.status == TaskStatus.WAITING:
                task.status = TaskStatus.PAUSED
                self.logger.info(f"等待中的任务已暂停: {task.name} (ID: {task_id})")
            else:
                return False
            
            self._save_queue()
            return True
    
    def resume_task(self, task_id: str) -> bool:
        """恢复任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            if task.status == TaskStatus.PAUSED:
                task.status = TaskStatus.WAITING
                self.priority_queue.put(task)
                self.logger.info(f"任务已恢复: {task.name} (ID: {task_id})")
                
                # 如果队列正在运行，尝试启动任务
                if self._running:
                    self._try_start_next_task()
                
                self._save_queue()
                return True
            
            return False
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            if task.status == TaskStatus.RUNNING:
                self._cancel_running_task(task_id)
            
            task.status = TaskStatus.CANCELLED
            task.end_time = time.time()
            
            self.logger.info(f"任务已取消: {task.name} (ID: {task_id})")
            self._save_queue()
            return True
    
    def _cancel_running_task(self, task_id: str) -> None:
        """取消正在运行的任务"""
        if task_id in self.worker_threads:
            future = self.worker_threads[task_id]
            future.cancel()
            del self.worker_threads[task_id]
        
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]
    
    def retry_task(self, task_id: str) -> bool:
        """重试失败的任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            if task.status != TaskStatus.FAILED:
                return False
            
            if task.retry_count >= task.max_retries:
                self.logger.warning(f"任务重试次数已达上限: {task.name} (ID: {task_id})")
                return False
            
            # 重置任务状态
            task.status = TaskStatus.WAITING
            task.progress = 0.0
            task.error_message = ""
            task.retry_count += 1
            task.start_time = None
            task.end_time = None
            
            self.priority_queue.put(task)
            
            self.logger.info(f"任务重试: {task.name} (ID: {task_id}, 第{task.retry_count}次重试)")
            
            # 如果队列正在运行，尝试启动任务
            if self._running:
                self._try_start_next_task()
            
            self._save_queue()
            return True
    
    def set_task_priority(self, task_id: str, priority: TaskPriority) -> bool:
        """设置任务优先级"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            if task.status in [TaskStatus.RUNNING, TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
                return False
            
            task.priority = priority
            
            # 如果任务在等待队列中，需要重新排序
            if task.status == TaskStatus.WAITING:
                # 重建优先级队列
                self._rebuild_priority_queue()
            
            self.logger.info(f"任务优先级已更新: {task.name} (ID: {task_id}, 优先级: {priority.name})")
            self._save_queue()
            return True
    
    def _rebuild_priority_queue(self) -> None:
        """重建优先级队列"""
        # 清空当前队列
        while not self.priority_queue.empty():
            try:
                self.priority_queue.get_nowait()
            except:
                break
        
        # 重新添加等待中的任务
        for task in self.tasks.values():
            if task.status == TaskStatus.WAITING:
                self.priority_queue.put(task)
    
    def start_queue(self) -> None:
        """启动队列处理"""
        with self._lock:
            if self._running:
                return
            
            self._running = True
            self._paused = False
            
            self.logger.info("队列处理已启动")
            
            # 启动可用的任务
            for _ in range(self.max_concurrent):
                self._try_start_next_task()
    
    def stop_queue(self) -> None:
        """停止队列处理"""
        with self._lock:
            if not self._running:
                return
            
            self._running = False
            
            # 取消所有正在运行的任务
            for task_id in list(self.running_tasks.keys()):
                self._cancel_running_task(task_id)
                task = self.tasks[task_id]
                task.status = TaskStatus.WAITING
                self.priority_queue.put(task)
            
            self.logger.info("队列处理已停止")
            self._save_queue()
    
    def pause_queue(self) -> None:
        """暂停队列处理"""
        with self._lock:
            self._paused = True
            self.logger.info("队列处理已暂停")
    
    def resume_queue(self) -> None:
        """恢复队列处理"""
        with self._lock:
            if not self._running:
                self.start_queue()
                return
            
            self._paused = False
            self.logger.info("队列处理已恢复")
            
            # 启动可用的任务
            for _ in range(self.max_concurrent - len(self.running_tasks)):
                self._try_start_next_task()
    
    def is_running(self) -> bool:
        """检查队列是否正在运行"""
        return self._running
    
    def is_paused(self) -> bool:
        """检查队列是否已暂停"""
        return self._paused
    
    def _try_start_next_task(self) -> bool:
        """尝试启动下一个任务"""
        if not self._running or self._paused:
            return False
        
        if len(self.running_tasks) >= self.max_concurrent:
            return False
        
        if self.priority_queue.empty():
            return False
        
        try:
            task = self.priority_queue.get_nowait()
            
            # 检查任务状态
            if task.status != TaskStatus.WAITING:
                return self._try_start_next_task()
            
            # 启动任务
            self._start_task(task)
            return True
            
        except:
            return False
    
    def _start_task(self, task: QueueTask) -> None:
        """启动单个任务"""
        task.status = TaskStatus.RUNNING
        task.start_time = time.time()
        task.progress = 0.0
        
        self.running_tasks[task.id] = task
        
        # 提交任务到线程池
        future = self.executor.submit(self._execute_task, task)
        self.worker_threads[task.id] = future
        
        # 添加完成回调
        future.add_done_callback(lambda f: self._task_completed(task.id, f))
        
        self.logger.info(f"任务开始执行: {task.name} (ID: {task.id})")
        
        # 调用回调函数
        if self.on_task_start:
            try:
                self.on_task_start(task)
            except Exception as e:
                self.logger.error(f"任务开始回调失败: {e}")
    
    def _execute_task(self, task: QueueTask) -> bool:
        """执行任务的实际逻辑（需要子类实现）"""
        # 这里是一个示例实现，实际使用时需要根据具体需求实现
        try:
            # 模拟任务执行
            for i in range(100):
                if task.status != TaskStatus.RUNNING:
                    return False
                
                time.sleep(0.1)  # 模拟工作
                task.progress = (i + 1) / 100.0
                
                # 调用进度更新回调
                if self.on_progress_update:
                    try:
                        self.on_progress_update(task)
                    except Exception as e:
                        self.logger.error(f"进度更新回调失败: {e}")
            
            return True
            
        except Exception as e:
            task.error_message = str(e)
            self.logger.error(f"任务执行失败: {task.name} - {e}")
            return False
    
    def _task_completed(self, task_id: str, future) -> None:
        """任务完成处理"""
        with self._lock:
            if task_id not in self.tasks:
                return
            
            task = self.tasks[task_id]
            task.end_time = time.time()
            task.actual_duration = task.end_time - (task.start_time or task.end_time)
            
            # 从运行任务中移除
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
            
            if task_id in self.worker_threads:
                del self.worker_threads[task_id]
            
            try:
                success = future.result()
                
                if success and task.status == TaskStatus.RUNNING:
                    task.status = TaskStatus.COMPLETED
                    task.progress = 1.0
                    self.stats['completed_tasks'] += 1
                    
                    self.logger.info(f"任务完成: {task.name} (ID: {task_id})")
                    
                    # 调用完成回调
                    if self.on_task_complete:
                        try:
                            self.on_task_complete(task)
                        except Exception as e:
                            self.logger.error(f"任务完成回调失败: {e}")
                else:
                    task.status = TaskStatus.FAILED
                    self.stats['failed_tasks'] += 1
                    
                    self.logger.error(f"任务失败: {task.name} (ID: {task_id})")
                    
                    # 调用失败回调
                    if self.on_task_failed:
                        try:
                            self.on_task_failed(task, task.error_message)
                        except Exception as e:
                            self.logger.error(f"任务失败回调失败: {e}")
                
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error_message = str(e)
                self.stats['failed_tasks'] += 1
                
                self.logger.error(f"任务异常: {task.name} (ID: {task_id}) - {e}")
                
                # 调用失败回调
                if self.on_task_failed:
                    try:
                        self.on_task_failed(task, str(e))
                    except Exception as e:
                        self.logger.error(f"任务失败回调失败: {e}")
            
            # 更新统计信息
            self.stats['total_processing_time'] += task.actual_duration
            if self.stats['completed_tasks'] > 0:
                self.stats['average_processing_time'] = (
                    self.stats['total_processing_time'] / self.stats['completed_tasks']
                )
            
            self._save_queue()
            
            # 尝试启动下一个任务
            if self._running:
                self._try_start_next_task()
    
    def get_task(self, task_id: str) -> Optional[QueueTask]:
        """获取任务信息"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[QueueTask]:
        """获取所有任务"""
        return list(self.tasks.values())
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[QueueTask]:
        """根据状态获取任务"""
        return [task for task in self.tasks.values() if task.status == status]
    
    def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        with self._lock:
            status_counts = {}
            for status in TaskStatus:
                status_counts[status.value] = len(self.get_tasks_by_status(status))
            
            return {
                'running': self._running,
                'paused': self._paused,
                'max_concurrent': self.max_concurrent,
                'current_running': len(self.running_tasks),
                'waiting_tasks': status_counts[TaskStatus.WAITING.value],
                'total_tasks': len(self.tasks),
                'status_counts': status_counts,
                'statistics': self.stats.copy()
            }
    
    def clear_completed_tasks(self) -> int:
        """清理已完成的任务"""
        with self._lock:
            completed_tasks = self.get_tasks_by_status(TaskStatus.COMPLETED)
            count = len(completed_tasks)
            
            for task in completed_tasks:
                del self.tasks[task.id]
            
            self.logger.info(f"已清理 {count} 个已完成的任务")
            self._save_queue()
            return count
    
    def clear_failed_tasks(self) -> int:
        """清理失败的任务"""
        with self._lock:
            failed_tasks = self.get_tasks_by_status(TaskStatus.FAILED)
            count = len(failed_tasks)
            
            for task in failed_tasks:
                del self.tasks[task.id]
            
            self.logger.info(f"已清理 {count} 个失败的任务")
            self._save_queue()
            return count
    
    def _save_queue(self) -> None:
        """保存队列到文件"""
        try:
            os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
            
            queue_data = {
                'tasks': {task_id: task.to_dict() for task_id, task in self.tasks.items()},
                'stats': self.stats,
                'settings': {
                    'max_concurrent': self.max_concurrent,
                    'running': self._running,
                    'paused': self._paused
                },
                'save_time': time.time()
            }
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(queue_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"保存队列失败: {e}")
    
    def _load_queue(self) -> None:
        """从文件加载队列"""
        try:
            if not os.path.exists(self.save_file):
                return
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)
            
            # 恢复任务
            tasks_data = queue_data.get('tasks', {})
            for task_id, task_data in tasks_data.items():
                try:
                    task = QueueTask.from_dict(task_data)
                    self.tasks[task_id] = task
                    
                    # 将等待中的任务重新加入队列
                    if task.status == TaskStatus.WAITING:
                        self.priority_queue.put(task)
                    # 将运行中的任务重置为等待状态
                    elif task.status == TaskStatus.RUNNING:
                        task.status = TaskStatus.WAITING
                        task.start_time = None
                        task.progress = 0.0
                        self.priority_queue.put(task)
                        
                except Exception as e:
                    self.logger.error(f"恢复任务失败: {task_id} - {e}")
            
            # 恢复统计信息
            self.stats.update(queue_data.get('stats', {}))
            
            # 恢复设置
            settings = queue_data.get('settings', {})
            self.max_concurrent = settings.get('max_concurrent', self.max_concurrent)
            
            self.logger.info(f"队列已恢复: {len(self.tasks)} 个任务")
            
        except Exception as e:
            self.logger.error(f"加载队列失败: {e}")
    
    def shutdown(self) -> None:
        """关闭队列管理器"""
        self.stop_queue()
        self.executor.shutdown(wait=True)
        self._save_queue()
        self.logger.info("队列管理器已关闭")


class TorrentQueueManager(QueueManager):
    """Torrent制种队列管理器"""
    
    def __init__(self, torrent_creator, max_concurrent: int = 4, save_file: Optional[str] = None):
        super().__init__(max_concurrent, save_file)
        self.torrent_creator = torrent_creator
    
    def _execute_task(self, task: QueueTask) -> bool:
        """执行Torrent制种任务"""
        try:
            # 应用预设配置
            if hasattr(self.torrent_creator, 'config_manager'):
                config_manager = self.torrent_creator.config_manager
                if hasattr(config_manager, 'apply_preset'):
                    config_manager.apply_preset(task.preset)
            
            # 设置输出路径
            output_path = task.output_path or self.torrent_creator.config_manager.get_output_folder()
            
            # 更新TorrentCreator的输出目录
            from pathlib import Path
            self.torrent_creator.output_dir = Path(output_path)
            
            # 执行制种
            success = self.torrent_creator.create_torrent(
                task.path,
                custom_name=None,  # 使用默认命名（基于文件夹名）
                progress_callback=lambda p: self._update_task_progress(task, p)
            )
            
            return success
            
        except Exception as e:
            task.error_message = str(e)
            self.logger.error(f"制种任务执行失败: {task.name} - {e}")
            return False
    
    def _update_task_progress(self, task: QueueTask, progress: float) -> None:
        """更新任务进度"""
        task.progress = progress
        
        # 调用进度更新回调
        if self.on_progress_update:
            try:
                self.on_progress_update(task)
            except Exception as e:
                self.logger.error(f"进度更新回调失败: {e}")
    
    def add_torrent_task(self, file_path: str, preset: str = "standard", 
                        priority: TaskPriority = TaskPriority.NORMAL,
                        output_path: str = "") -> str:
        """添加制种任务"""
        name = self._generate_smart_task_name(file_path)
        return self.add_task(name, file_path, priority, preset, output_path)
    
    def _generate_smart_task_name(self, file_path: str) -> str:
        """生成智能任务名称"""
        try:
            from pathlib import Path
            path_obj = Path(file_path)
            
            # 如果是文件夹，显示更有意义的路径
            if path_obj.is_dir():
                # 尝试获取相对于资源文件夹的路径
                try:
                    if hasattr(self.torrent_creator, 'config_manager'):
                        resource_folder = self.torrent_creator.config_manager.get_resource_folder()
                        if resource_folder:
                            resource_path = Path(resource_folder)
                            relative_path = path_obj.relative_to(resource_path)
                            name = str(relative_path)
                        else:
                            raise ValueError("No resource folder")
                    else:
                        raise ValueError("No config manager")
                except (ValueError, AttributeError):
                    # 如果不在资源文件夹内或无法获取，显示最后两级目录
                    parts = path_obj.parts
                    if len(parts) >= 2:
                        name = os.path.join(parts[-2], parts[-1])
                    else:
                        name = path_obj.name
            else:
                name = path_obj.name
            
            # 限制名称长度，避免界面显示问题
            if len(name) > 50:
                name = name[:47] + "..."
            
            return name
            
        except Exception as e:
            # 如果出现任何错误，回退到简单命名
            self.logger.warning(f"智能命名失败，使用简单命名: {e}")
            return os.path.basename(file_path)
    
    def batch_add_tasks(self, file_paths: List[str], preset: str = "standard",
                       priority: TaskPriority = TaskPriority.NORMAL) -> List[str]:
        """批量添加制种任务"""
        task_ids = []
        for file_path in file_paths:
            task_id = self.add_torrent_task(file_path, preset, priority)
            task_ids.append(task_id)
        
        self.logger.info(f"批量添加了 {len(task_ids)} 个制种任务")
        return task_ids


# ================== 路径补全模块 ==================
import glob
try:
    import readline
except ImportError:
    readline = None

class PathCompleter:
    """路径自动补全类 - 为 Torrent Maker 提供 Tab 键补全功能"""
    
    def __init__(self, history_file: str = None):
        self.history_file = history_file or os.path.expanduser("~/.torrent_maker_path_history.json")
        self.path_history: List[str] = []
        self.load_history()
        
        # 设置 readline 补全
        if readline:
            readline.set_completer(self.complete)
            readline.parse_and_bind("tab: complete")
            readline.set_completer_delims(' \t\n`!@#$%^&*()=+[{]}\\|;:\'\",<>?')
    
    def complete(self, text: str, state: int) -> Optional[str]:
        """Tab 补全回调函数"""
        if state == 0:
            self.matches = self._get_matches(text)
        
        try:
            return self.matches[state]
        except IndexError:
            return None
    
    def _get_matches(self, text: str) -> List[str]:
        """获取匹配的路径"""
        matches = []
        
        # 如果文本为空，返回历史记录
        if not text.strip():
            return self.path_history[-10:]  # 最近10个
        
        # 展开用户目录
        expanded_text = os.path.expanduser(text)
        
        # 获取目录和文件名部分
        if os.path.isdir(expanded_text):
            search_dir = expanded_text
            prefix = ""
        else:
            search_dir = os.path.dirname(expanded_text) or "."
            prefix = os.path.basename(expanded_text)
        
        try:
            # 使用 glob 进行匹配
            pattern = os.path.join(search_dir, prefix + "*")
            glob_matches = glob.glob(pattern)
            
            for match in sorted(glob_matches):
                # 如果是目录，添加斜杠
                if os.path.isdir(match):
                    match += os.sep
                matches.append(match)
            
            # 添加历史记录中的匹配项
            for hist_path in self.path_history:
                if hist_path.startswith(text) and hist_path not in matches:
                    matches.append(hist_path)
        
        except (OSError, PermissionError):
            pass
        
        return matches[:20]  # 限制返回数量
    
    def add_to_history(self, path: str) -> None:
        """添加路径到历史记录"""
        if not path or not os.path.exists(path):
            return
        
        # 规范化路径
        normalized_path = os.path.abspath(path)
        
        # 移除重复项
        if normalized_path in self.path_history:
            self.path_history.remove(normalized_path)
        
        # 添加到开头
        self.path_history.insert(0, normalized_path)
        
        # 限制历史记录大小
        if len(self.path_history) > 100:
            self.path_history = self.path_history[:100]
        
        self.save_history()
    
    def get_suggestions(self, partial_path: str, limit: int = 10) -> List[str]:
        """获取路径建议"""
        suggestions = []
        
        # 从历史记录中查找
        for path in self.path_history:
            if partial_path.lower() in path.lower():
                suggestions.append(path)
                if len(suggestions) >= limit:
                    break
        
        return suggestions
    
    def get_recent_paths(self, limit: int = 10) -> List[str]:
        """获取最近使用的路径"""
        return self.path_history[:limit]
    
    def load_history(self) -> None:
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.path_history = data.get('paths', [])
        except (json.JSONDecodeError, OSError):
            self.path_history = []
    
    def save_history(self) -> None:
        """保存历史记录"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'paths': self.path_history,
                    'last_updated': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
        except OSError:
            pass
    
    def get_input(self, prompt: str) -> str:
        """获取用户输入，支持路径补全"""
        try:
            if readline:
                # 设置当前补全器
                old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                
                # 获取用户输入
                user_input = input(prompt).strip()
                
                # 恢复原补全器
                readline.set_completer(old_completer)
                
                # 如果输入的是路径，添加到历史记录
                if user_input and (os.path.exists(user_input) or os.path.dirname(user_input)):
                    self.add_to_history(user_input)
                
                return user_input
            else:
                # 没有 readline 支持时的降级处理
                return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return ""


# ================== 进度监控模块 ==================
from collections import defaultdict

@dataclass
class ProgressInfo:
    """进度信息数据类"""
    task_id: str
    status: TaskStatus
    progress: float = 0.0  # 0-100
    current_step: str = ""
    total_steps: int = 0
    completed_steps: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class ProgressDisplay:
    """进度条显示类"""
    
    def __init__(self, width: int = 50):
        self.width = width
        self.last_output_length = 0
    
    def show_progress(self, progress: float, message: str = "", show_percentage: bool = True) -> None:
        """显示进度条"""
        # 确保进度在 0-100 范围内
        progress = max(0, min(100, progress))
        
        # 计算进度条
        filled_width = int(self.width * progress / 100)
        bar = "█" * filled_width + "░" * (self.width - filled_width)
        
        # 构建输出字符串
        if show_percentage:
            output = f"\r[{bar}] {progress:6.2f}%"
        else:
            output = f"\r[{bar}]"
        
        if message:
            output += f" {message}"
        
        # 清除之前的输出
        if len(output) < self.last_output_length:
            output += " " * (self.last_output_length - len(output))
        
        print(output, end="", flush=True)
        self.last_output_length = len(output)
    
    def clear(self) -> None:
        """清除进度条"""
        if self.last_output_length > 0:
            print("\r" + " " * self.last_output_length + "\r", end="", flush=True)
            self.last_output_length = 0
    
    def finish(self, message: str = "完成!") -> None:
        """完成进度显示"""
        self.show_progress(100, message)
        print()  # 换行
        self.last_output_length = 0

class ProgressMonitor:
    """进度监控器"""
    
    def __init__(self):
        self.tasks: Dict[str, ProgressInfo] = {}
        self.callbacks: Dict[str, List[callable]] = defaultdict(list)
        self.display = ProgressDisplay()
        self._lock = threading.Lock()
        self._running = False
        self._display_thread = None
    
    def create_task(self, task_id: str, total_steps: int = 0, metadata: Dict[str, Any] = None) -> ProgressInfo:
        """创建新任务"""
        with self._lock:
            task = ProgressInfo(
                task_id=task_id,
                status=TaskStatus.WAITING,
                total_steps=total_steps,
                start_time=datetime.now(),
                metadata=metadata or {}
            )
            self.tasks[task_id] = task
            return task
    
    def start_task(self, task_id: str) -> bool:
        """开始任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            task.status = TaskStatus.RUNNING
            task.start_time = datetime.now()
            
            self._notify_callbacks(task_id, "started")
            return True
    
    def update_progress(self, task_id: str, progress: float = None, 
                       current_step: str = None, completed_steps: int = None) -> bool:
        """更新任务进度"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            if progress is not None:
                task.progress = max(0, min(100, progress))
            
            if current_step is not None:
                task.current_step = current_step
            
            if completed_steps is not None:
                task.completed_steps = completed_steps
                if task.total_steps > 0:
                    task.progress = (completed_steps / task.total_steps) * 100
            
            self._notify_callbacks(task_id, "progress")
            return True
    
    def complete_task(self, task_id: str, success: bool = True, error_message: str = "") -> bool:
        """完成任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
            task.end_time = datetime.now()
            task.progress = 100 if success else task.progress
            
            if error_message:
                task.error_message = error_message
            
            self._notify_callbacks(task_id, "completed" if success else "failed")
            return True
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            task.status = TaskStatus.CANCELLED
            task.end_time = datetime.now()
            
            self._notify_callbacks(task_id, "cancelled")
            return True
    
    def get_task(self, task_id: str) -> Optional[ProgressInfo]:
        """获取任务信息"""
        with self._lock:
            return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, ProgressInfo]:
        """获取所有任务"""
        with self._lock:
            return self.tasks.copy()
    
    def add_callback(self, task_id: str, callback: callable) -> None:
        """添加回调函数"""
        self.callbacks[task_id].append(callback)
    
    def _notify_callbacks(self, task_id: str, event: str) -> None:
        """通知回调函数"""
        for callback in self.callbacks.get(task_id, []):
            try:
                callback(task_id, event, self.tasks[task_id])
            except Exception as e:
                print(f"⚠️ 回调函数执行失败: {e}")
    
    def start_display_loop(self, task_id: str, update_interval: float = 0.1) -> None:
        """开始显示循环"""
        if self._running:
            return
        
        self._running = True
        self._display_thread = threading.Thread(
            target=self._display_loop,
            args=(task_id, update_interval),
            daemon=True
        )
        self._display_thread.start()
    
    def stop_display_loop(self) -> None:
        """停止显示循环"""
        self._running = False
        if self._display_thread:
            self._display_thread.join(timeout=1.0)
    
    def _display_loop(self, task_id: str, update_interval: float) -> None:
        """显示循环"""
        while self._running:
            with self._lock:
                task = self.tasks.get(task_id)
                if not task or task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                    break
                
                message = task.current_step if task.current_step else f"任务: {task_id}"
                self.display.show_progress(task.progress, message)
            
            time.sleep(update_interval)
        
        # 清除显示
        self.display.clear()
    
    def clear_completed_tasks(self) -> int:
        """清除已完成的任务"""
        with self._lock:
            completed_statuses = {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}
            to_remove = [task_id for task_id, task in self.tasks.items() 
                        if task.status in completed_statuses]
            
            for task_id in to_remove:
                del self.tasks[task_id]
                if task_id in self.callbacks:
                    del self.callbacks[task_id]
            
            return len(to_remove)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            stats = {
                'total_tasks': len(self.tasks),
                'pending': 0,
                'running': 0,
                'completed': 0,
                'failed': 0,
                'cancelled': 0
            }
            
            for task in self.tasks.values():
                stats[task.status.value] += 1
            
            return stats

class TorrentProgressMonitor:
    """Torrent 制种进度监控器"""
    
    def __init__(self):
        self.monitor = ProgressMonitor()
        self.processes: Dict[str, subprocess.Popen] = {}
        self._lock = threading.Lock()
        self.current_task_id: Optional[str] = None
        self.is_monitoring = False
    
    def start_torrent_creation(self, task_id: str, command: List[str], 
                              input_path: str, output_path: str) -> bool:
        """开始制种任务"""
        try:
            # 创建任务
            file_size = self._get_file_size(input_path)
            self.monitor.create_task(task_id, metadata={
                'input_path': input_path,
                'output_path': output_path,
                'file_size': file_size,
                'command': command
            })
            
            # 启动进程
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            with self._lock:
                self.processes[task_id] = process
            
            # 开始监控
            self.monitor.start_task(task_id)
            
            # 启动监控线程
            monitor_thread = threading.Thread(
                target=self._monitor_process,
                args=(task_id, process),
                daemon=True
            )
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            self.monitor.complete_task(task_id, False, str(e))
            return False
    
    def _monitor_process(self, task_id: str, process: subprocess.Popen) -> None:
        """监控进程执行"""
        try:
            # 模拟进度更新（mktorrent 没有实时进度输出）
            start_time = time.time()
            
            while process.poll() is None:
                elapsed = time.time() - start_time
                # 基于时间估算进度（这是一个简化的实现）
                estimated_progress = min(90, elapsed * 10)  # 假设90%的进度基于时间
                
                self.monitor.update_progress(task_id, estimated_progress, "正在创建种子文件...")
                time.sleep(0.5)
            
            # 进程结束
            return_code = process.returncode
            
            if return_code == 0:
                self.monitor.update_progress(task_id, 100, "种子文件创建完成")
                self.monitor.complete_task(task_id, True)
            else:
                stderr_output = process.stderr.read() if process.stderr else ""
                self.monitor.complete_task(task_id, False, f"进程退出码: {return_code}, 错误: {stderr_output}")
            
        except Exception as e:
            self.monitor.complete_task(task_id, False, str(e))
        finally:
            with self._lock:
                if task_id in self.processes:
                    del self.processes[task_id]
    
    def cancel_torrent_creation(self, task_id: str) -> bool:
        """取消制种任务"""
        with self._lock:
            process = self.processes.get(task_id)
            if process:
                try:
                    process.terminate()
                    # 等待进程结束
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    
                    self.monitor.cancel_task(task_id)
                    del self.processes[task_id]
                    return True
                except Exception as e:
                    print(f"⚠️ 取消任务失败: {e}")
                    return False
        
        return False
    
    def _get_file_size(self, path: str) -> int:
        """获取文件或目录大小"""
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)
            elif os.path.isdir(path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            total_size += os.path.getsize(filepath)
                        except (OSError, IOError):
                            continue
                return total_size
        except (OSError, IOError):
            pass
        return 0
    
    def get_task_info(self, task_id: str) -> Optional[ProgressInfo]:
        """获取任务信息"""
        return self.monitor.get_task(task_id)
    
    def get_all_tasks(self) -> Dict[str, ProgressInfo]:
        """获取所有任务"""
        return self.monitor.get_all_tasks()
    
    def create_task(self, task_id: str, description: str = "", path: str = "", metadata: Dict[str, Any] = None) -> bool:
        """创建新任务"""
        try:
            task_metadata = metadata or {}
            if description:
                task_metadata['description'] = description
            if path:
                task_metadata['path'] = path
            self.monitor.create_task(task_id, task_metadata)
            return True
        except Exception as e:
            print(f"⚠️ 创建任务失败: {e}")
            return False
    
    def start_task(self, task_id: str) -> bool:
        """启动任务"""
        try:
            self.monitor.start_task(task_id)
            return True
        except Exception as e:
            print(f"⚠️ 启动任务失败: {e}")
            return False
    
    def update_progress(self, task_id: str, progress: float, current_step: str = "") -> bool:
        """更新任务进度"""
        try:
            self.monitor.update_progress(task_id, progress, current_step)
            return True
        except Exception as e:
            print(f"⚠️ 更新进度失败: {e}")
            return False
    
    def complete_task(self, task_id: str, success: bool, error_message: str = "") -> bool:
        """完成任务"""
        try:
            self.monitor.complete_task(task_id, success, error_message)
            return True
        except Exception as e:
            print(f"⚠️ 完成任务失败: {e}")
            return False
    
    def start_monitoring(self, task_name: str, task_path: str) -> bool:
        """开始监控制种任务"""
        try:
            # 生成任务ID
            task_id = f"torrent_{int(time.time())}_{task_name}"
            self.current_task_id = task_id
            
            # 创建监控任务
            file_size = self._get_file_size(task_path)
            self.monitor.create_task(task_id, metadata={
                'task_name': task_name,
                'task_path': task_path,
                'file_size': file_size,
                'start_time': time.time()
            })
            
            # 启动任务
            self.monitor.start_task(task_id)
            self.is_monitoring = True
            
            print(f"📊 开始监控制种任务: {task_name}")
            return True
            
        except Exception as e:
            print(f"⚠️ 启动监控失败: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """停止监控制种任务"""
        try:
            if self.current_task_id and self.is_monitoring:
                # 完成当前任务
                self.monitor.complete_task(self.current_task_id, True, "制种任务完成")
                print(f"📊 停止监控制种任务: {self.current_task_id}")
                
                # 重置状态
                self.current_task_id = None
                self.is_monitoring = False
                return True
            else:
                print("⚠️ 没有正在监控的任务")
                return False
                
        except Exception as e:
            print(f"⚠️ 停止监控失败: {e}")
            return False
    
    def update_progress(self, message: str, progress: float = None) -> bool:
        """更新监控进度"""
        try:
            if self.current_task_id and self.is_monitoring:
                if progress is not None:
                    self.monitor.update_progress(self.current_task_id, progress, message)
                else:
                    # 如果没有提供进度值，基于时间估算
                    task_info = self.monitor.get_task(self.current_task_id)
                    if task_info and task_info.metadata.get('start_time'):
                        elapsed = time.time() - task_info.metadata['start_time']
                        estimated_progress = min(90, elapsed * 5)  # 简单的时间估算
                        self.monitor.update_progress(self.current_task_id, estimated_progress, message)
                return True
            return False
            
        except Exception as e:
            print(f"⚠️ 更新进度失败: {e}")
            return False


# ================== 搜索历史模块 ==================
from collections import Counter
import difflib

@dataclass
class SearchEntry:
    """搜索记录条目"""
    query: str
    timestamp: datetime
    results_count: int = 0
    selected_results: List[str] = None
    success: bool = True
    search_time: float = 0.0
    category: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.selected_results is None:
            self.selected_results = []
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'query': self.query,
            'timestamp': self.timestamp.isoformat(),
            'results_count': self.results_count,
            'selected_results': self.selected_results,
            'success': self.success,
            'search_time': self.search_time,
            'category': self.category,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SearchEntry':
        """从字典创建"""
        return cls(
            query=data['query'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            results_count=data.get('results_count', 0),
            selected_results=data.get('selected_results', []),
            success=data.get('success', True),
            search_time=data.get('search_time', 0.0),
            category=data.get('category', ''),
            metadata=data.get('metadata', {})
        )

class SearchHistory:
    """搜索历史管理器"""
    
    def __init__(self, history_file: str = None, max_entries: int = 1000):
        self.history_file = history_file or os.path.expanduser("~/.torrent_maker_search_history.json")
        self.max_entries = max_entries
        self.entries: List[SearchEntry] = []
        self.load_history()
    
    def add_search(self, query: str, results_count: int = 0, 
                   selected_results: List[str] = None, success: bool = True,
                   search_time: float = 0.0, category: str = "",
                   **metadata) -> SearchEntry:
        """添加搜索记录"""
        cleaned_query = self._clean_query(query)
        if not cleaned_query:
            return None
        
        # 检查重复搜索
        from datetime import timedelta
        recent_cutoff = datetime.now() - timedelta(minutes=5)
        for entry in reversed(self.entries):
            if (entry.timestamp > recent_cutoff and 
                entry.query.lower() == cleaned_query.lower()):
                # 更新现有记录
                entry.results_count = max(entry.results_count, results_count)
                if selected_results:
                    entry.selected_results.extend(selected_results)
                    entry.selected_results = list(set(entry.selected_results))
                entry.success = entry.success and success
                entry.search_time = (entry.search_time + search_time) / 2
                if category:
                    entry.category = category
                entry.metadata.update(metadata)
                self.save_history()
                return entry
        
        # 创建新记录
        entry = SearchEntry(
            query=cleaned_query,
            timestamp=datetime.now(),
            results_count=results_count,
            selected_results=selected_results or [],
            success=success,
            search_time=search_time,
            category=category,
            metadata=metadata
        )
        
        self.entries.append(entry)
        
        # 限制历史记录大小
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
        
        self.save_history()
        return entry
    
    def _clean_query(self, query: str) -> str:
        """清理查询字符串"""
        if not query:
            return ""
        
        cleaned = re.sub(r'\s+', ' ', query.strip())
        cleaned = re.sub(r'[^\w\s\u4e00-\u9fff.\-_()\[\]]+', '', cleaned)
        return cleaned
    
    def get_suggestions(self, partial_query: str, limit: int = 10) -> List[Tuple[str, float]]:
        """获取搜索建议"""
        if not partial_query.strip():
            recent_queries = [entry.query for entry in reversed(self.entries[-limit:])]
            return [(query, 1.0) for query in recent_queries]
        
        partial_lower = partial_query.lower().strip()
        suggestions = []
        
        all_queries = [entry.query for entry in self.entries]
        
        for query in set(all_queries):
            query_lower = query.lower()
            
            if query_lower.startswith(partial_lower):
                suggestions.append((query, 1.0))
            elif partial_lower in query_lower:
                suggestions.append((query, 0.8))
            else:
                similarity = difflib.SequenceMatcher(None, partial_lower, query_lower).ratio()
                if similarity > 0.6:
                    suggestions.append((query, similarity))
        
        query_counts = Counter(all_queries)
        suggestions.sort(key=lambda x: (x[1], query_counts[x[0]]), reverse=True)
        
        return suggestions[:limit]
    
    def get_recent_queries(self, limit: int = 10) -> List[str]:
        """获取最近搜索"""
        recent_queries = []
        seen = set()
        
        for entry in reversed(self.entries):
            if entry.query not in seen:
                recent_queries.append(entry.query)
                seen.add(entry.query)
                if len(recent_queries) >= limit:
                    break
        
        return recent_queries
    
    def get_popular_queries(self, limit: int = 10) -> List[str]:
        """获取热门搜索"""
        query_counts = Counter(entry.query for entry in self.entries)
        popular_queries = [query for query, count in query_counts.most_common(limit)]
        return popular_queries
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取搜索统计信息"""
        if not self.entries:
            return {
                'total_searches': 0,
                'unique_queries': 0,
                'success_rate': 0.0,
                'average_results': 0.0
            }
        
        total_searches = len(self.entries)
        unique_queries = len(set(entry.query for entry in self.entries))
        successful_searches = sum(1 for entry in self.entries if entry.success)
        success_rate = successful_searches / total_searches if total_searches > 0 else 0.0
        average_results = sum(entry.results_count for entry in self.entries) / total_searches if total_searches > 0 else 0.0
        
        return {
            'total_searches': total_searches,
            'unique_queries': unique_queries,
            'success_rate': round(success_rate * 100, 1),
            'average_results': round(average_results, 1)
        }
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    entries_data = data.get('entries', data)
                    self.entries = [SearchEntry.from_dict(entry_data) for entry_data in entries_data]
        except (json.JSONDecodeError, OSError, KeyError) as e:
            print(f"⚠️ 加载搜索历史失败: {e}")
            self.entries = []
    
    def save_history(self):
        """保存历史记录"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            data = {
                'version': '1.0',
                'last_updated': datetime.now().isoformat(),
                'total_entries': len(self.entries),
                'entries': [entry.to_dict() for entry in self.entries]
            }
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"⚠️ 保存搜索历史失败: {e}")

class SmartSearchSuggester:
    """智能搜索建议器"""
    
    def __init__(self, search_history: SearchHistory):
        self.history = search_history
        self.patterns = {
            '电影': [r'\d{4}', r'(电影|movie|film)', r'(HD|4K|1080p|720p|BluRay|BDRip)', r'(中字|字幕|subtitle)'],
            '电视剧': [r'(第\d+季|S\d+|season)', r'(第\d+集|E\d+|episode)', r'(电视剧|TV|series)', r'(全集|完整版|complete)'],
            '动漫': [r'(动漫|anime|动画)', r'(第\d+话|第\d+集)', r'(OVA|OAD|剧场版)', r'(日语|中配|双语)'],
            '纪录片': [r'(纪录片|documentary)', r'(BBC|National Geographic|Discovery)', r'(自然|历史|科学)']
        }
    
    def suggest_improvements(self, query: str) -> List[str]:
        """建议查询改进"""
        suggestions = []
        
        detected_category = self._detect_category(query)
        if detected_category:
            suggestions.append(f"检测到类型: {detected_category}")
        
        if not re.search(r'\d{4}', query) and detected_category in ['电影', '电视剧']:
            suggestions.append("建议添加年份以获得更精确的结果")
        
        if not re.search(r'(HD|4K|1080p|720p|BluRay)', query, re.IGNORECASE):
            suggestions.append("可以添加画质信息 (如: 1080p, 4K)")
        
        if not re.search(r'(中字|字幕|subtitle)', query, re.IGNORECASE):
            suggestions.append("可以添加字幕信息 (如: 中字)")
        
        return suggestions
    
    def _detect_category(self, query: str) -> Optional[str]:
        """检测查询分类"""
        query_lower = query.lower()
        
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return category
        
        return None
    
    def get_related_queries(self, query: str, limit: int = 5) -> List[str]:
        """获取相关查询建议"""
        related_queries = []
        query_lower = query.lower()
        
        # 从历史记录中查找相似查询
        # 兼容两种SearchHistory实现
        history_data = getattr(self.history, 'entries', None) or getattr(self.history, 'history', [])
        
        for entry in history_data:
            # 兼容不同的数据结构
            entry_query = entry.query if hasattr(entry, 'query') else entry.get('query', '')
            entry_query_lower = entry_query.lower()
            
            # 检查是否包含相同关键词
            query_words = set(query_lower.split())
            entry_words = set(entry_query_lower.split())
            
            # 如果有共同词汇且不是完全相同的查询
            if (query_words & entry_words and 
                entry_query != query and 
                entry_query not in related_queries):
                related_queries.append(entry_query)
                
                if len(related_queries) >= limit:
                    break
        
        return related_queries
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """获取搜索建议（整合改进建议和相关查询）"""
        suggestions = []
        
        # 添加查询改进建议
        improvements = self.suggest_improvements(query)
        suggestions.extend(improvements)
        
        # 添加相关查询建议
        related = self.get_related_queries(query, limit=3)
        if related:
            suggestions.append("相关搜索历史:")
            for related_query in related:
                suggestions.append(f"  → {related_query}")
        
        return suggestions


# ================== 性能监控系统 ==================
class PerformanceMonitor:
    """简单的性能监控类"""

    def __init__(self):
        self._timers: Dict[str, float] = {}
        self._stats: Dict[str, Dict[str, float]] = {}
        self._lock = threading.Lock()

    def start_timer(self, name: str) -> None:
        """开始计时"""
        with self._lock:
            self._timers[name] = time.time()

    def end_timer(self, name: str) -> float:
        """结束计时并返回耗时"""
        with self._lock:
            if name not in self._timers:
                return 0.0

            duration = time.time() - self._timers[name]
            del self._timers[name]

            # 更新统计信息
            if name not in self._stats:
                self._stats[name] = {
                    'count': 0,
                    'total': 0.0,
                    'average': 0.0,
                    'max': 0.0,
                    'min': float('inf')
                }

            stats = self._stats[name]
            stats['count'] += 1
            stats['total'] += duration
            stats['average'] = stats['total'] / stats['count']
            stats['max'] = max(stats['max'], duration)
            stats['min'] = min(stats['min'], duration)

            return duration

    def get_stats(self, name: str) -> Dict[str, float]:
        """获取指定计时器的统计信息"""
        with self._lock:
            return self._stats.get(name, {})

    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """获取所有统计信息"""
        with self._lock:
            return self._stats.copy()


# ================== 缓存系统 ==================
class SearchCache:
    """搜索结果缓存类"""

    def __init__(self, cache_duration: int = 3600):
        self.cache_duration = cache_duration
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._cache:
                timestamp, value = self._cache[key]
                if time.time() - timestamp < self.cache_duration:
                    return value
                else:
                    del self._cache[key]
            return None

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._cache[key] = (time.time(), value)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            total_items = len(self._cache)
            current_time = time.time()
            expired_items = sum(1 for timestamp, _ in self._cache.values()
                              if current_time - timestamp >= self.cache_duration)
            return {
                'total_items': total_items,
                'valid_items': total_items - expired_items,
                'expired_items': expired_items
            }


# ================== 目录大小缓存 ==================
class DirectorySizeCache:
    """目录大小缓存类 - 高性能优化版本"""

    def __init__(self, cache_duration: int = 1800, max_cache_size: int = 1000):
        self.cache_duration = cache_duration
        self.max_cache_size = max_cache_size
        self._cache: Dict[str, Tuple[float, int, float, int]] = {}  # path -> (timestamp, size, mtime, access_count)
        self._access_order: List[str] = []  # LRU 访问顺序
        self._lock = threading.Lock()
        self._stats = {'hits': 0, 'misses': 0, 'evictions': 0}

    def get_directory_size(self, path: Path) -> int:
        """获取目录大小，使用高性能缓存优化"""
        path_str = str(path)
        current_time = time.time()

        try:
            # 获取目录的修改时间
            dir_mtime = path.stat().st_mtime
        except (OSError, PermissionError):
            return self._calculate_size_fallback(path)

        with self._lock:
            # 检查缓存
            if path_str in self._cache:
                timestamp, cached_size, cached_mtime, access_count = self._cache[path_str]
                # 如果缓存未过期且目录未修改，返回缓存值
                if (current_time - timestamp < self.cache_duration and
                    abs(dir_mtime - cached_mtime) < 1.0):  # 1秒容差
                    # 更新访问统计和 LRU 顺序
                    self._cache[path_str] = (timestamp, cached_size, cached_mtime, access_count + 1)
                    self._update_access_order(path_str)
                    self._stats['hits'] += 1
                    return cached_size
                else:
                    # 缓存过期，移除
                    self._remove_from_cache(path_str)

        self._stats['misses'] += 1

        # 计算目录大小
        total_size = self._calculate_size_optimized(path)

        # 更新缓存
        with self._lock:
            self._add_to_cache(path_str, current_time, total_size, dir_mtime)

        return total_size

    def _add_to_cache(self, path_str: str, timestamp: float, size: int, mtime: float) -> None:
        """添加到缓存，实现 LRU 淘汰"""
        # 如果缓存已满，移除最少使用的项
        if len(self._cache) >= self.max_cache_size:
            self._evict_lru()

        self._cache[path_str] = (timestamp, size, mtime, 1)
        self._access_order.append(path_str)

    def _remove_from_cache(self, path_str: str) -> None:
        """从缓存中移除项目"""
        if path_str in self._cache:
            del self._cache[path_str]
        if path_str in self._access_order:
            self._access_order.remove(path_str)

    def _update_access_order(self, path_str: str) -> None:
        """更新 LRU 访问顺序"""
        if path_str in self._access_order:
            self._access_order.remove(path_str)
        self._access_order.append(path_str)

    def _evict_lru(self) -> None:
        """淘汰最少使用的缓存项"""
        if self._access_order:
            lru_path = self._access_order.pop(0)
            if lru_path in self._cache:
                del self._cache[lru_path]
                self._stats['evictions'] += 1

    def _calculate_size_optimized(self, path: Path) -> int:
        """内存优化的目录大小计算"""
        # 检查目录大小，决定使用哪种策略
        try:
            # 快速估算目录复杂度
            complexity = self._estimate_directory_complexity(path)

            if complexity['estimated_files'] > 10000:
                # 大目录使用流式处理
                return self._calculate_size_streaming(path)
            elif complexity['estimated_files'] > 1000:
                # 中等目录使用批量处理
                return self._calculate_size_batch(path)
            else:
                # 小目录使用简单方法
                return self._scan_directory_simple(path)

        except Exception:
            # 回退到简单方法
            return self._scan_directory_simple(path)

    def _estimate_directory_complexity(self, path: Path) -> Dict[str, int]:
        """估算目录复杂度"""
        try:
            sample_count = 0
            dir_count = 0
            file_count = 0

            # 只扫描前几个子目录来估算
            with os.scandir(path) as entries:
                for entry in entries:
                    sample_count += 1
                    if entry.is_dir(follow_symlinks=False):
                        dir_count += 1
                    elif entry.is_file(follow_symlinks=False):
                        file_count += 1

                    # 只采样前 100 个项目
                    if sample_count >= 100:
                        break

            # 估算总文件数
            if dir_count > 0:
                estimated_files = file_count + dir_count * 50  # 假设每个子目录平均 50 个文件
            else:
                estimated_files = file_count

            return {
                'sample_count': sample_count,
                'dir_count': dir_count,
                'file_count': file_count,
                'estimated_files': estimated_files
            }

        except (OSError, PermissionError):
            return {'sample_count': 0, 'dir_count': 0, 'file_count': 0, 'estimated_files': 0}

    def _calculate_size_streaming(self, path: Path) -> int:
        """流式计算大目录大小 - 异步优化版本"""
        # 尝试使用异步处理器
        try:
            async_processor = AsyncFileProcessor(max_concurrent=4)

            # 先异步扫描目录树
            loop = async_processor.async_io._get_event_loop()
            if loop is not None:
                try:
                    import asyncio
                    if loop.is_running():
                        future = asyncio.ensure_future(
                            async_processor.async_directory_tree_scan(path, max_depth=10, include_files=True)
                        )
                        result = asyncio.run_coroutine_threadsafe(future, loop).result(timeout=30)
                    else:
                        result = loop.run_until_complete(
                            async_processor.async_directory_tree_scan(path, max_depth=10, include_files=True)
                        )

                    return result.get('total_size', 0)
                except Exception:
                    pass
        except Exception:
            pass

        # 回退到同步流式处理
        total_size = 0
        processed_count = 0

        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    try:
                        total_size += file_path.stat().st_size
                        processed_count += 1

                        # 每处理 1000 个文件检查一次内存
                        if processed_count % 1000 == 0:
                            # 这里可以添加内存检查逻辑
                            pass

                    except (OSError, IOError):
                        pass
        except (OSError, PermissionError):
            pass

        return total_size

    def _calculate_size_batch(self, path: Path) -> int:
        """批量计算中等目录大小"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import queue

        total_size = 0
        scan_queue = queue.Queue()
        scan_queue.put(path)

        def scan_directory_batch() -> int:
            """批量扫描目录"""
            batch_size = 0

            try:
                while not scan_queue.empty():
                    try:
                        current_path = scan_queue.get_nowait()

                        with os.scandir(current_path) as entries:
                            for entry in entries:
                                if entry.is_file(follow_symlinks=False):
                                    try:
                                        batch_size += entry.stat().st_size
                                    except (OSError, IOError):
                                        pass
                                elif entry.is_dir(follow_symlinks=False):
                                    scan_queue.put(Path(entry.path))
                    except queue.Empty:
                        break
                    except (PermissionError, OSError):
                        continue
            except Exception:
                pass

            return batch_size

        try:
            # 使用少量线程并行处理
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = []

                # 启动扫描任务
                for _ in range(2):
                    if not scan_queue.empty():
                        futures.append(executor.submit(scan_directory_batch))

                # 收集结果
                for future in as_completed(futures):
                    try:
                        total_size += future.result()
                    except Exception:
                        pass

                # 处理剩余目录
                while not scan_queue.empty():
                    try:
                        remaining_path = scan_queue.get_nowait()
                        total_size += self._scan_directory_simple(remaining_path)
                    except queue.Empty:
                        break

        except Exception:
            total_size = self._scan_directory_simple(path)

        return total_size

    def _scan_directory_simple(self, path: Path) -> int:
        """简单的目录扫描方法"""
        size = 0
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_file(follow_symlinks=False):
                        try:
                            size += entry.stat().st_size
                        except (OSError, IOError):
                            pass
                    elif entry.is_dir(follow_symlinks=False):
                        size += self._scan_directory_simple(Path(entry.path))
        except (PermissionError, OSError):
            pass
        return size

    def _calculate_size_fallback(self, path: Path) -> int:
        """回退的目录大小计算方法"""
        total_size = 0
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    try:
                        total_size += file_path.stat().st_size
                    except (OSError, IOError):
                        pass
        except (OSError, PermissionError):
            pass
        return total_size

    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self._lock:
            total_requests = self._stats['hits'] + self._stats['misses']
            hit_rate = self._stats['hits'] / total_requests if total_requests > 0 else 0

            return {
                'cache_size': len(self._cache),
                'max_cache_size': self.max_cache_size,
                'hit_rate': hit_rate,
                'hits': self._stats['hits'],
                'misses': self._stats['misses'],
                'evictions': self._stats['evictions'],
                'total_requests': total_requests
            }

    def clear_cache(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._stats = {'hits': 0, 'misses': 0, 'evictions': 0}

    def cleanup_expired(self) -> int:
        """清理过期的缓存项"""
        current_time = time.time()
        expired_count = 0

        with self._lock:
            expired_paths = []
            for path_str, (timestamp, _, _, _) in self._cache.items():
                if current_time - timestamp >= self.cache_duration:
                    expired_paths.append(path_str)

            for path_str in expired_paths:
                self._remove_from_cache(path_str)
                expired_count += 1

        return expired_count


# ================== 异常类 ==================
class ConfigValidationError(Exception):
    """配置验证错误"""
    pass


class TorrentCreationError(Exception):
    """种子创建错误"""
    pass


# ================== 配置管理器 ==================
class ConfigManager:
    """配置管理器 - v1.5.1修复优化版本"""
    
    DEFAULT_SETTINGS = {
        "resource_folder": "~/Downloads",
        "output_folder": "~/Desktop/torrents",
        "file_search_tolerance": 60,
        "max_search_results": 10,
        "auto_create_output_dir": True,
        "enable_cache": True,
        "cache_duration": 3600,
        "max_concurrent_operations": 4,
        "log_level": "WARNING",
        "max_scan_depth": 3,
        "max_scan_folders": 5000,
        "max_scan_time": 30
    }
    
    DEFAULT_TRACKERS = [
        "udp://tracker.openbittorrent.com:80",
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://exodus.desync.com:6969/announce",
        "udp://tracker.torrent.eu.org:451/announce"
    ]

    def __init__(self):
        self.config_dir = os.path.expanduser("~/.torrent_maker")
        self.settings_path = os.path.join(self.config_dir, "settings.json")
        self.trackers_path = os.path.join(self.config_dir, "trackers.txt")
        
        self._ensure_config_files()
        self.settings = self._load_settings()
        self.trackers = self._load_trackers()
        self._validate_config()

    def _ensure_config_files(self) -> None:
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            if not os.path.exists(self.settings_path):
                self._create_default_settings()
            if not os.path.exists(self.trackers_path):
                self._create_default_trackers()
            
            # 确保预设配置文件存在
            presets_path = os.path.join(self.config_dir, "presets.json")
            if not os.path.exists(presets_path):
                self._create_default_presets()
        except OSError as e:
            raise ConfigValidationError(f"无法创建配置文件: {e}")

    def _create_default_settings(self) -> None:
        settings = self.DEFAULT_SETTINGS.copy()
        settings['resource_folder'] = os.path.expanduser(settings['resource_folder'])
        settings['output_folder'] = os.path.expanduser(settings['output_folder'])
        
        with open(self.settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)

    def _create_default_trackers(self) -> None:
        with open(self.trackers_path, 'w', encoding='utf-8') as f:
            f.write("# BitTorrent Tracker 列表\n")
            f.write("# 每行一个 tracker URL，以 # 开头的行为注释\n\n")
            for tracker in self.DEFAULT_TRACKERS:
                f.write(f"{tracker}\n")
    
    def _create_default_presets(self) -> None:
        """创建默认预设配置文件"""
        presets_path = os.path.join(self.config_dir, "presets.json")
        
        # 尝试从项目config目录复制预设文件
        project_presets_path = os.path.join(os.path.dirname(__file__), "config", "presets.json")
        
        if os.path.exists(project_presets_path):
            try:
                import shutil
                shutil.copy2(project_presets_path, presets_path)
                return
            except Exception:
                pass
        
        # 如果复制失败，创建基本的预设配置
        default_presets = {
            "presets": {
                "fast": {
                    "name": "快速模式",
                    "description": "适用于小文件(<1GB)，优先制种速度",
                    "settings": {
                        "piece_size": "256k",
                        "max_concurrent_operations": "auto_x2",
                        "cache_enabled": False,
                        "cache_size_mb": 64,
                        "max_scan_depth": 3,
                        "file_search_tolerance": 0.7,
                        "auto_create_output_dir": True,
                        "log_level": "WARNING"
                    },
                    "recommended_for": [
                        "小文件批量制种",
                        "快速分享需求",
                        "网络带宽有限"
                    ]
                },
                "standard": {
                    "name": "标准模式",
                    "description": "平衡质量和速度，适用于大多数场景(1-10GB)",
                    "settings": {
                        "piece_size": "auto",
                        "max_concurrent_operations": "auto",
                        "cache_enabled": True,
                        "cache_size_mb": 256,
                        "max_scan_depth": 5,
                        "file_search_tolerance": 0.8,
                        "auto_create_output_dir": True,
                        "log_level": "INFO"
                    },
                    "recommended_for": [
                        "日常制种需求",
                        "中等大小文件",
                        "平衡性能要求"
                    ]
                },
                "quality": {
                    "name": "高质量模式",
                    "description": "适用于大文件(>10GB)，优先制种质量",
                    "settings": {
                        "piece_size": "2m",
                        "max_concurrent_operations": "auto_half",
                        "cache_enabled": True,
                        "cache_size_mb": 512,
                        "max_scan_depth": 10,
                        "file_search_tolerance": 0.9,
                        "auto_create_output_dir": True,
                        "log_level": "DEBUG"
                    },
                    "recommended_for": [
                        "大文件制种",
                        "高质量要求",
                        "服务器环境"
                    ]
                }
            },
            "preset_metadata": {
                "version": "1.0",
                "created_time": time.time(),
                "description": "Torrent Maker 默认预设配置"
            }
        }
        
        with open(presets_path, 'w', encoding='utf-8') as f:
            json.dump(default_presets, f, ensure_ascii=False, indent=2)

    def _load_settings(self) -> Dict[str, Any]:
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            for key in ['resource_folder', 'output_folder']:
                if key in settings:
                    settings[key] = os.path.expanduser(settings[key])
                    
            merged_settings = self.DEFAULT_SETTINGS.copy()
            merged_settings.update(settings)
            return merged_settings
            
        except (FileNotFoundError, json.JSONDecodeError):
            return self.DEFAULT_SETTINGS.copy()

    def _load_trackers(self) -> List[str]:
        try:
            with open(self.trackers_path, 'r', encoding='utf-8') as f:
                trackers = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # 清理URL格式，移除可能的反引号和其他非法字符
                        cleaned_line = line.strip('`"\'')
                        # 基本URL格式验证
                        if cleaned_line.startswith(('http://', 'https://', 'udp://')):
                            trackers.append(cleaned_line)
                        else:
                            print(f"⚠️  跳过无效的tracker URL: {line}")
                return trackers if trackers else self.DEFAULT_TRACKERS.copy()
        except FileNotFoundError:
            return self.DEFAULT_TRACKERS.copy()

    def _validate_config(self) -> None:
        numeric_configs = {
            'file_search_tolerance': (0, 100),
            'max_search_results': (1, 100),
            'cache_duration': (60, 86400),
            'max_concurrent_operations': (1, 20)
        }
        
        for key, (min_val, max_val) in numeric_configs.items():
            if key in self.settings:
                value = self.settings[key]
                if not isinstance(value, (int, float)) or not (min_val <= value <= max_val):
                    self.settings[key] = self.DEFAULT_SETTINGS[key]

    def get_resource_folder(self) -> str:
        return os.path.abspath(self.settings.get('resource_folder', os.path.expanduser("~/Downloads")))

    def get_output_folder(self) -> str:
        output_path = self.settings.get('output_folder', os.path.expanduser("~/Desktop/torrents"))
        return os.path.abspath(output_path)

    def get_trackers(self) -> List[str]:
        return self.trackers.copy()

    def save_settings(self):
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存设置时出错: {e}")

    def save_trackers(self):
        try:
            with open(self.trackers_path, 'w', encoding='utf-8') as f:
                f.write("# BitTorrent Tracker 列表\n")
                f.write("# 每行一个 tracker URL，以 # 开头的行为注释\n\n")
                for tracker in self.trackers:
                    f.write(f"{tracker}\n")
        except Exception as e:
            print(f"保存 tracker 时出错: {e}")

    def set_resource_folder(self, path: str) -> bool:
        """设置资源文件夹路径，并验证路径有效性"""
        try:
            expanded_path = os.path.expanduser(path)
            expanded_path = os.path.abspath(expanded_path)

            # 检查路径是否存在
            if not os.path.exists(expanded_path):
                print(f"❌ 路径不存在: {expanded_path}")
                return False

            # 检查是否为目录
            if not os.path.isdir(expanded_path):
                print(f"❌ 路径不是目录: {expanded_path}")
                return False

            self.settings['resource_folder'] = expanded_path
            self.save_settings()
            print(f"✅ 资源文件夹已设置为: {expanded_path}")
            return True

        except Exception as e:
            print(f"❌ 设置资源文件夹失败: {e}")
            return False

    def set_output_folder(self, path: str):
        expanded_path = os.path.expanduser(path)
        self.settings['output_folder'] = expanded_path
        self.save_settings()

    def add_tracker(self, tracker_url: str):
        if tracker_url not in self.trackers:
            self.trackers.append(tracker_url)
            self.save_trackers()
            return True
        return False

    def remove_tracker(self, tracker_url: str):
        if tracker_url in self.trackers:
            self.trackers.remove(tracker_url)
            self.save_trackers()
            return True
        return False

    def get_setting(self, key: str, default=None):
        """获取单个设置项

        Args:
            key: 设置项键名
            default: 默认值

        Returns:
            设置项的值
        """
        return self.settings.get(key, default)

    def set_setting(self, key: str, value):
        """设置单个配置项

        Args:
            key: 设置项键名
            value: 设置项的值

        Returns:
            设置成功返回True，否则返回False
        """
        try:
            self.settings[key] = value
            self.save_settings()
            return True
        except Exception as e:
            print(f"设置配置项失败: {e}")
            return False

    # ================== 预设模式管理 ==================
    
    def _load_presets(self) -> Dict[str, Any]:
        """加载预设配置"""
        presets_path = os.path.join(self.config_dir, "presets.json")
        try:
            with open(presets_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️ 加载预设配置失败: {e}")
            return {"presets": {}, "preset_metadata": {}}
    
    def get_available_presets(self) -> Dict[str, Dict[str, Any]]:
        """获取可用的预设模式"""
        presets_data = self._load_presets()
        return presets_data.get("presets", {})
    
    def get_preset_info(self, preset_name: str) -> Dict[str, Any]:
        """获取指定预设的详细信息"""
        presets = self.get_available_presets()
        return presets.get(preset_name, {})
    
    def apply_preset(self, preset_name: str) -> bool:
        """应用预设配置"""
        try:
            preset_info = self.get_preset_info(preset_name)
            if not preset_info:
                print(f"❌ 预设 '{preset_name}' 不存在")
                return False
            
            preset_settings = preset_info.get("settings", {})
            if not preset_settings:
                print(f"❌ 预设 '{preset_name}' 没有有效的设置")
                return False
            
            # 处理特殊的线程数配置
            if "max_concurrent_operations" in preset_settings:
                thread_config = preset_settings["max_concurrent_operations"]
                if isinstance(thread_config, str):
                    import multiprocessing
                    cpu_count = multiprocessing.cpu_count()
                    
                    if thread_config == "auto":
                        preset_settings["max_concurrent_operations"] = cpu_count
                    elif thread_config == "auto_x2":
                        preset_settings["max_concurrent_operations"] = cpu_count * 2
                    elif thread_config == "auto_half":
                        preset_settings["max_concurrent_operations"] = max(1, cpu_count // 2)
            
            # 应用预设设置
            for key, value in preset_settings.items():
                self.settings[key] = value
            
            self.save_settings()
            print(f"✅ 已应用预设: {preset_info.get('name', preset_name)}")
            print(f"   {preset_info.get('description', '')}")
            return True
            
        except Exception as e:
            print(f"❌ 应用预设失败: {e}")
            return False
    
    def save_custom_preset(self, preset_name: str, description: str = "") -> bool:
        """保存当前配置为自定义预设"""
        try:
            presets_path = os.path.join(self.config_dir, "presets.json")
            presets_data = self._load_presets()
            
            # 创建自定义预设
            custom_preset = {
                "name": preset_name,
                "description": description or f"用户自定义预设: {preset_name}",
                "settings": self.settings.copy(),
                "user_defined": True,
                "created_time": time.time(),
                "recommended_for": ["用户自定义配置"]
            }
            
            # 添加到预设列表
            if "presets" not in presets_data:
                presets_data["presets"] = {}
            
            presets_data["presets"][preset_name] = custom_preset
            
            # 保存预设文件
            with open(presets_path, 'w', encoding='utf-8') as f:
                json.dump(presets_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 自定义预设 '{preset_name}' 已保存")
            return True
            
        except Exception as e:
            print(f"❌ 保存自定义预设失败: {e}")
            return False
    
    def delete_custom_preset(self, preset_name: str) -> bool:
        """删除自定义预设"""
        try:
            presets_path = os.path.join(self.config_dir, "presets.json")
            presets_data = self._load_presets()
            
            presets = presets_data.get("presets", {})
            if preset_name not in presets:
                print(f"❌ 预设 '{preset_name}' 不存在")
                return False
            
            preset_info = presets[preset_name]
            if not preset_info.get("user_defined", False):
                print(f"❌ 无法删除系统预设 '{preset_name}'")
                return False
            
            del presets[preset_name]
            
            # 保存更新后的预设文件
            with open(presets_path, 'w', encoding='utf-8') as f:
                json.dump(presets_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 自定义预设 '{preset_name}' 已删除")
            return True
            
        except Exception as e:
            print(f"❌ 删除自定义预设失败: {e}")
            return False
    
    def auto_detect_preset(self, file_size_bytes: int = 0) -> str:
        """根据文件大小自动检测推荐的预设模式"""
        try:
            presets_data = self._load_presets()
            metadata = presets_data.get("preset_metadata", {})
            auto_detect_rules = metadata.get("auto_detect_rules", {})
            
            if not auto_detect_rules:
                return "standard"  # 默认返回标准模式
            
            thresholds = auto_detect_rules.get("file_size_thresholds", {})
            mapping = auto_detect_rules.get("auto_preset_mapping", {})
            
            # 根据文件大小确定类别
            if file_size_bytes < thresholds.get("small", 1073741824):  # < 1GB
                return mapping.get("small", "fast")
            elif file_size_bytes < thresholds.get("medium", 10737418240):  # < 10GB
                return mapping.get("medium", "standard")
            else:  # >= 10GB
                return mapping.get("large", "quality")
                
        except Exception as e:
            print(f"⚠️ 自动检测预设失败: {e}")
            return "standard"
    
    def display_presets_menu(self) -> None:
        """显示预设模式菜单"""
        presets = self.get_available_presets()
        if not presets:
            print("❌ 没有可用的预设模式")
            return
        
        print("\n" + "="*60)
        print("🎛️  配置预设模式")
        print("="*60)
        
        for i, (preset_key, preset_info) in enumerate(presets.items(), 1):
            name = preset_info.get("name", preset_key)
            description = preset_info.get("description", "")
            is_custom = preset_info.get("user_defined", False)
            custom_tag = " [自定义]" if is_custom else ""
            
            print(f"{i}. {name}{custom_tag}")
            print(f"   {description}")
            
            # 显示推荐场景
            recommended = preset_info.get("recommended_for", [])
            if recommended:
                print(f"   💡 推荐用于: {', '.join(recommended)}")
            print()
        
        print(f"{len(presets) + 1}. 保存当前配置为自定义预设")
        print(f"{len(presets) + 2}. 删除自定义预设")
        print(f"{len(presets) + 3}. 返回上级菜单")
        print("="*60)


# ================== 智能索引缓存 ==================
class SmartIndexCache:
    """智能索引缓存 - v1.5.1 搜索优化"""

    def __init__(self, cache_duration: int = 3600):
        self.cache_duration = cache_duration
        self._word_index: Dict[str, Set[str]] = {}  # word -> set of folder paths
        self._folder_words: Dict[str, Set[str]] = {}  # folder_path -> set of words
        self._last_update = 0
        self._lock = threading.Lock()

    def build_index(self, folders: List[Path], normalize_func) -> None:
        """构建智能索引"""
        with self._lock:
            self._word_index.clear()
            self._folder_words.clear()

            for folder in folders:
                folder_path = str(folder)
                normalized_name = normalize_func(folder.name)
                words = set(normalized_name.split())

                self._folder_words[folder_path] = words

                for word in words:
                    if word not in self._word_index:
                        self._word_index[word] = set()
                    self._word_index[word].add(folder_path)

            self._last_update = time.time()

    def get_candidate_folders(self, search_words: Set[str]) -> Set[str]:
        """根据搜索词获取候选文件夹"""
        if not search_words:
            return set()

        candidate_sets = []
        for word in search_words:
            if word in self._word_index:
                candidate_sets.append(self._word_index[word])

        if not candidate_sets:
            return set()

        # 返回包含任意搜索词的文件夹
        return set.union(*candidate_sets)

    def is_expired(self) -> bool:
        """检查索引是否过期"""
        return time.time() - self._last_update > self.cache_duration


# ================== 内存分析器 ==================
class MemoryAnalyzer:
    """内存分析器 - 深度内存使用分析"""

    @staticmethod
    def get_object_memory_usage() -> Dict[str, Any]:
        """获取对象内存使用情况"""
        import gc
        import sys

        # 统计不同类型对象的数量
        type_counts = {}
        total_objects = 0

        for obj in gc.get_objects():
            obj_type = type(obj).__name__
            type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
            total_objects += 1

        # 获取最占内存的对象类型
        top_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            'total_objects': total_objects,
            'top_memory_types': top_types,
            'gc_stats': {
                'collections': gc.get_stats(),
                'garbage_count': len(gc.garbage)
            }
        }

    @staticmethod
    def analyze_memory_leaks() -> Dict[str, Any]:
        """分析潜在的内存泄漏"""
        import gc
        import weakref

        # 强制垃圾回收
        collected = gc.collect()

        # 检查循环引用
        referrers_count = {}
        for obj in gc.get_objects():
            referrers = gc.get_referrers(obj)
            ref_count = len(referrers)
            if ref_count > 10:  # 被引用次数过多的对象
                obj_type = type(obj).__name__
                referrers_count[obj_type] = referrers_count.get(obj_type, 0) + 1

        return {
            'collected_objects': collected,
            'high_reference_objects': referrers_count,
            'unreachable_objects': len(gc.garbage)
        }


# ================== 增强内存管理器 ==================
class MemoryManager:
    """内存管理器 - v1.5.1 深度内存优化"""

    def __init__(self, max_memory_mb: int = 512):
        self.max_memory_mb = max_memory_mb
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self._memory_pools: Dict[str, List[Any]] = {}
        self._object_cache: Dict[str, Any] = {}
        self._memory_history: List[Dict[str, float]] = []
        self._lock = threading.Lock()
        self._analyzer = MemoryAnalyzer()
        self._cleanup_threshold = 0.8  # 80% 内存使用时触发清理

    def get_memory_usage(self) -> Dict[str, Any]:
        """获取详细内存使用情况"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            system_memory = psutil.virtual_memory()

            usage_data = {
                'rss_mb': memory_info.rss / (1024 * 1024),
                'vms_mb': memory_info.vms / (1024 * 1024),
                'percent': process.memory_percent(),
                'available_mb': system_memory.available / (1024 * 1024),
                'system_total_mb': system_memory.total / (1024 * 1024),
                'system_used_percent': system_memory.percent,
                'swap_mb': getattr(memory_info, 'swap', 0) / (1024 * 1024)
            }

            # 记录内存历史
            self._record_memory_history(usage_data)

            return usage_data

        except ImportError:
            # 回退到简单的内存估算
            import resource
            try:
                # 尝试使用 resource 模块
                usage = resource.getrusage(resource.RUSAGE_SELF)
                # 修复 macOS 内存计算错误：macOS 返回的是字节，不需要除以1024
                import platform
                if platform.system() == 'Darwin':  # macOS
                    rss_mb = usage.ru_maxrss / (1024 * 1024)  # 字节转MB
                else:  # Linux
                    rss_mb = usage.ru_maxrss / 1024  # KB转MB

                return {
                    'rss_mb': rss_mb,
                    'vms_mb': 0,
                    'percent': 0,
                    'available_mb': 1024,
                    'system_total_mb': 0,
                    'system_used_percent': 0,
                    'swap_mb': 0
                }
            except:
                return {
                    'rss_mb': 0,
                    'vms_mb': 0,
                    'percent': 0,
                    'available_mb': 1024,
                    'system_total_mb': 0,
                    'system_used_percent': 0,
                    'swap_mb': 0
                }

    def _record_memory_history(self, usage_data: Dict[str, float]) -> None:
        """记录内存使用历史"""
        with self._lock:
            self._memory_history.append({
                'timestamp': time.time(),
                'rss_mb': usage_data['rss_mb'],
                'percent': usage_data['percent']
            })

            # 只保留最近 100 条记录
            if len(self._memory_history) > 100:
                self._memory_history = self._memory_history[-100:]

    def should_cleanup(self) -> bool:
        """智能检查是否需要清理内存"""
        memory_info = self.get_memory_usage()
        current_usage = memory_info['rss_mb']

        # 多重检查条件
        conditions = [
            current_usage > self.max_memory_mb,  # 超过设定限制
            current_usage > self.max_memory_mb * self._cleanup_threshold,  # 超过阈值
            memory_info.get('system_used_percent', 0) > 85,  # 系统内存使用过高
            self._is_memory_growing_rapidly()  # 内存增长过快
        ]

        return any(conditions)

    def _is_memory_growing_rapidly(self) -> bool:
        """检查内存是否增长过快"""
        if len(self._memory_history) < 5:
            return False

        recent_usage = [entry['rss_mb'] for entry in self._memory_history[-5:]]
        if len(recent_usage) < 2:
            return False

        # 计算内存增长率
        growth_rate = (recent_usage[-1] - recent_usage[0]) / len(recent_usage)
        return growth_rate > 10  # 每次测量增长超过 10MB

    def cleanup_if_needed(self, force: bool = False) -> Dict[str, int]:
        """智能内存清理"""
        if force or self.should_cleanup():
            return self.cleanup_memory()
        return {'cleaned_items': 0, 'freed_mb': 0}

    def cleanup_memory(self) -> Dict[str, int]:
        """深度内存清理"""
        cleaned_stats = {
            'memory_pools_cleaned': 0,
            'object_cache_cleaned': 0,
            'gc_collected': 0,
            'freed_mb': 0
        }

        # 记录清理前的内存使用
        before_memory = self.get_memory_usage()['rss_mb']

        with self._lock:
            # 清理内存池
            for pool_name in list(self._memory_pools.keys()):
                pool = self._memory_pools[pool_name]
                if len(pool) > 10:  # 保留最近的 10 个项目
                    removed = len(pool) - 10
                    self._memory_pools[pool_name] = pool[-10:]
                    cleaned_stats['memory_pools_cleaned'] += removed

            # 清理对象缓存
            if len(self._object_cache) > 50:
                # 保留最近使用的 50 个对象
                cache_items = list(self._object_cache.items())
                self._object_cache = dict(cache_items[-50:])
                cleaned_stats['object_cache_cleaned'] = len(cache_items) - 50

        # 强制垃圾回收
        import gc
        collected = gc.collect()
        cleaned_stats['gc_collected'] = collected

        # 计算释放的内存
        after_memory = self.get_memory_usage()['rss_mb']
        cleaned_stats['freed_mb'] = max(0, before_memory - after_memory)

        return cleaned_stats

    def get_memory_analysis(self) -> Dict[str, Any]:
        """获取内存分析报告"""
        current_usage = self.get_memory_usage()
        object_analysis = self._analyzer.get_object_memory_usage()
        leak_analysis = self._analyzer.analyze_memory_leaks()

        # 计算内存趋势
        memory_trend = self._calculate_memory_trend()

        return {
            'current_usage': current_usage,
            'object_analysis': object_analysis,
            'leak_analysis': leak_analysis,
            'memory_trend': memory_trend,
            'pool_stats': {
                'total_pools': len(self._memory_pools),
                'total_cached_objects': sum(len(pool) for pool in self._memory_pools.values()),
                'object_cache_size': len(self._object_cache)
            },
            'recommendations': self._generate_memory_recommendations(current_usage)
        }

    def _calculate_memory_trend(self) -> Dict[str, Any]:
        """计算内存使用趋势"""
        if len(self._memory_history) < 3:
            return {'trend': 'insufficient_data', 'growth_rate': 0}

        recent_usage = [entry['rss_mb'] for entry in self._memory_history[-10:]]

        # 简单线性趋势计算
        if len(recent_usage) >= 2:
            growth_rate = (recent_usage[-1] - recent_usage[0]) / len(recent_usage)

            if growth_rate > 5:
                trend = 'increasing_rapidly'
            elif growth_rate > 1:
                trend = 'increasing'
            elif growth_rate < -1:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
            growth_rate = 0

        return {
            'trend': trend,
            'growth_rate': growth_rate,
            'history_points': len(self._memory_history)
        }

    def _generate_memory_recommendations(self, usage: Dict[str, Any]) -> List[str]:
        """生成内存优化建议"""
        recommendations = []
        rss_mb = usage.get('rss_mb', 0)

        if rss_mb > self.max_memory_mb * 0.9:
            recommendations.append("内存使用接近限制，建议立即清理缓存")
        elif rss_mb > self.max_memory_mb * 0.7:
            recommendations.append("内存使用较高，建议定期清理")

        if usage.get('system_used_percent', 0) > 80:
            recommendations.append("系统内存使用过高，建议减少并发操作")

        if self._is_memory_growing_rapidly():
            recommendations.append("检测到内存快速增长，可能存在内存泄漏")

        if len(self._memory_pools) > 20:
            recommendations.append("内存池过多，建议合并或清理")

        if not recommendations:
            recommendations.append("内存使用正常，无需特别优化")

        return recommendations


# ================== 真正的异步 I/O 处理器 ==================
class AsyncIOProcessor:
    """真正的异步 I/O 处理器 - v1.5.1 深度异步优化"""

    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.semaphore = threading.Semaphore(max_concurrent)
        self._loop = None
        self._executor = None

    def _get_event_loop(self):
        """获取或创建事件循环"""
        try:
            import asyncio
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            return loop
        except ImportError:
            return None

    def _get_executor(self):
        """获取线程池执行器"""
        if self._executor is None:
            self._executor = ThreadPoolExecutor(max_workers=self.max_concurrent)
        return self._executor

    async def async_directory_scan_native(self, base_path: Path, max_depth: int = 3) -> List[Path]:
        """原生异步目录扫描"""
        import asyncio

        folders = []
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def scan_directory(path: Path, depth: int):
            if depth >= max_depth:
                return

            async with semaphore:
                try:
                    # 异步扫描目录
                    entries = await asyncio.get_event_loop().run_in_executor(
                        self._get_executor(),
                        lambda: list(os.scandir(path))
                    )

                    subdirs = []
                    for entry in entries:
                        if entry.is_dir(follow_symlinks=False):
                            folder_path = Path(entry.path)
                            folders.append(folder_path)
                            if depth + 1 < max_depth:
                                subdirs.append(folder_path)

                    # 并发扫描子目录
                    if subdirs:
                        tasks = [scan_directory(subdir, depth + 1) for subdir in subdirs]
                        await asyncio.gather(*tasks, return_exceptions=True)

                except (PermissionError, OSError):
                    pass

        await scan_directory(base_path, 0)
        return folders

    def async_directory_scan(self, base_path: Path, max_depth: int = 3) -> List[Path]:
        """异步目录扫描 - 兼容接口"""
        loop = self._get_event_loop()
        if loop is None:
            # 回退到线程池实现
            return self._async_directory_scan_threaded(base_path, max_depth)

        try:
            import asyncio
            if loop.is_running():
                # 如果循环正在运行，使用 run_in_executor
                future = asyncio.ensure_future(self.async_directory_scan_native(base_path, max_depth))
                return asyncio.run_coroutine_threadsafe(future, loop).result(timeout=30)
            else:
                # 如果循环未运行，直接运行
                return loop.run_until_complete(self.async_directory_scan_native(base_path, max_depth))
        except Exception:
            # 异常时回退到线程池实现
            return self._async_directory_scan_threaded(base_path, max_depth)

    def _async_directory_scan_threaded(self, base_path: Path, max_depth: int = 3) -> List[Path]:
        """线程池版本的异步目录扫描"""
        import queue
        import threading

        result_queue = queue.Queue()
        scan_queue = queue.Queue()
        scan_queue.put((base_path, 0))

        def worker():
            while True:
                try:
                    path, depth = scan_queue.get(timeout=1)
                    if depth >= max_depth:
                        scan_queue.task_done()
                        continue

                    try:
                        with os.scandir(path) as entries:
                            for entry in entries:
                                if entry.is_dir(follow_symlinks=False):
                                    folder_path = Path(entry.path)
                                    result_queue.put(folder_path)
                                    if depth + 1 < max_depth:
                                        scan_queue.put((folder_path, depth + 1))
                    except (PermissionError, OSError):
                        pass

                    scan_queue.task_done()
                except queue.Empty:
                    break

        # 启动工作线程
        threads = []
        for _ in range(min(4, self.max_concurrent)):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
            threads.append(t)

        # 等待完成
        scan_queue.join()

        # 收集结果
        folders = []
        while not result_queue.empty():
            folders.append(result_queue.get())

        return folders

    async def async_file_operations_native(self, operations: List[Tuple[str, Path, Any]]) -> List[Any]:
        """原生异步文件操作"""
        import asyncio

        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def execute_operation(op_type: str, path: Path, params: Any) -> Any:
            async with semaphore:
                try:
                    # 使用线程池执行器处理 I/O 操作
                    loop = asyncio.get_event_loop()

                    if op_type == 'size':
                        return await loop.run_in_executor(
                            self._get_executor(),
                            lambda: path.stat().st_size
                        )
                    elif op_type == 'exists':
                        return await loop.run_in_executor(
                            self._get_executor(),
                            lambda: path.exists()
                        )
                    elif op_type == 'mtime':
                        return await loop.run_in_executor(
                            self._get_executor(),
                            lambda: path.stat().st_mtime
                        )
                    elif op_type == 'hash':
                        return await self._async_calculate_hash(path, params or 'md5')
                    elif op_type == 'read':
                        return await self._async_read_file(path, params)
                    else:
                        return None
                except (OSError, IOError):
                    return None

        # 并发执行所有操作
        tasks = [execute_operation(op_type, path, params) for op_type, path, params in operations]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理异常结果
        return [result if not isinstance(result, Exception) else None for result in results]

    async def _async_calculate_hash(self, file_path: Path, algorithm: str = 'md5') -> str:
        """异步计算文件哈希"""
        import hashlib
        import asyncio

        hash_obj = hashlib.new(algorithm)
        chunk_size = 64 * 1024  # 64KB chunks for async operations

        try:
            loop = asyncio.get_event_loop()

            # 异步读取文件
            def read_chunk(f, size):
                return f.read(size)

            with open(file_path, 'rb') as f:
                while True:
                    chunk = await loop.run_in_executor(
                        self._get_executor(),
                        read_chunk, f, chunk_size
                    )

                    if not chunk:
                        break

                    hash_obj.update(chunk)

                    # 让出控制权，允许其他协程运行
                    await asyncio.sleep(0)

            return hash_obj.hexdigest()

        except (OSError, IOError):
            return ""

    async def _async_read_file(self, file_path: Path, max_size: int = None) -> bytes:
        """异步读取文件"""
        import asyncio

        try:
            loop = asyncio.get_event_loop()

            def read_file():
                with open(file_path, 'rb') as f:
                    if max_size:
                        return f.read(max_size)
                    else:
                        return f.read()

            return await loop.run_in_executor(self._get_executor(), read_file)

        except (OSError, IOError):
            return b""

    def async_file_operations(self, operations: List[Tuple[str, Path, Any]]) -> List[Any]:
        """异步文件操作 - 兼容接口"""
        loop = self._get_event_loop()
        if loop is None:
            # 回退到线程池实现
            return self._async_file_operations_threaded(operations)

        try:
            import asyncio
            if loop.is_running():
                # 如果循环正在运行，使用 run_in_executor
                future = asyncio.ensure_future(self.async_file_operations_native(operations))
                return asyncio.run_coroutine_threadsafe(future, loop).result(timeout=60)
            else:
                # 如果循环未运行，直接运行
                return loop.run_until_complete(self.async_file_operations_native(operations))
        except Exception:
            # 异常时回退到线程池实现
            return self._async_file_operations_threaded(operations)

    def _async_file_operations_threaded(self, operations: List[Tuple[str, Path, Any]]) -> List[Any]:
        """线程池版本的异步文件操作"""
        results = []

        def execute_operation(op_type: str, path: Path, params: Any) -> Any:
            with self.semaphore:
                try:
                    if op_type == 'size':
                        return path.stat().st_size
                    elif op_type == 'exists':
                        return path.exists()
                    elif op_type == 'mtime':
                        return path.stat().st_mtime
                    else:
                        return None
                except (OSError, IOError):
                    return None

        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = [
                executor.submit(execute_operation, op_type, path, params)
                for op_type, path, params in operations
            ]

            for future in as_completed(futures):
                results.append(future.result())

        return results

    def cleanup(self):
        """清理资源"""
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None


# ================== 异步文件处理器 ==================
class AsyncFileProcessor:
    """异步文件处理器 - 专门处理文件相关的异步操作"""

    def __init__(self, max_concurrent: int = 8, chunk_size: int = 64 * 1024):
        self.max_concurrent = max_concurrent
        self.chunk_size = chunk_size
        self.async_io = AsyncIOProcessor(max_concurrent)

    async def async_batch_file_stats(self, file_paths: List[Path]) -> List[Dict[str, Any]]:
        """批量异步获取文件统计信息"""
        import asyncio

        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def get_file_stats(file_path: Path) -> Dict[str, Any]:
            async with semaphore:
                try:
                    loop = asyncio.get_event_loop()

                    # 异步获取文件状态
                    stat_info = await loop.run_in_executor(
                        None, lambda: file_path.stat()
                    )

                    return {
                        'path': str(file_path),
                        'size': stat_info.st_size,
                        'mtime': stat_info.st_mtime,
                        'is_file': file_path.is_file(),
                        'exists': True
                    }
                except (OSError, IOError):
                    return {
                        'path': str(file_path),
                        'size': 0,
                        'mtime': 0,
                        'is_file': False,
                        'exists': False
                    }

        # 并发处理所有文件
        tasks = [get_file_stats(path) for path in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 过滤异常结果
        return [result for result in results if isinstance(result, dict)]

    async def async_directory_tree_scan(self, base_path: Path,
                                      max_depth: int = 3,
                                      include_files: bool = True) -> Dict[str, Any]:
        """异步扫描目录树"""
        import asyncio

        result = {
            'directories': [],
            'files': [],
            'total_size': 0,
            'file_count': 0,
            'dir_count': 0,
            'errors': []
        }

        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def scan_directory(path: Path, depth: int):
            if depth >= max_depth:
                return

            async with semaphore:
                try:
                    loop = asyncio.get_event_loop()

                    # 异步扫描目录
                    entries = await loop.run_in_executor(
                        None, lambda: list(os.scandir(path))
                    )

                    subdirs = []
                    files = []

                    for entry in entries:
                        if entry.is_dir(follow_symlinks=False):
                            dir_path = Path(entry.path)
                            result['directories'].append(str(dir_path))
                            result['dir_count'] += 1

                            if depth + 1 < max_depth:
                                subdirs.append(dir_path)

                        elif entry.is_file(follow_symlinks=False) and include_files:
                            file_path = Path(entry.path)
                            try:
                                file_size = entry.stat().st_size
                                files.append({
                                    'path': str(file_path),
                                    'size': file_size
                                })
                                result['total_size'] += file_size
                                result['file_count'] += 1
                            except (OSError, IOError):
                                result['errors'].append(f"无法获取文件信息: {file_path}")

                    # 批量添加文件信息
                    if files:
                        result['files'].extend(files)

                    # 并发扫描子目录
                    if subdirs:
                        tasks = [scan_directory(subdir, depth + 1) for subdir in subdirs]
                        await asyncio.gather(*tasks, return_exceptions=True)

                except (PermissionError, OSError) as e:
                    result['errors'].append(f"扫描目录失败 {path}: {e}")

        await scan_directory(base_path, 0)
        return result

    async def async_file_hash_batch(self, file_paths: List[Path],
                                  algorithm: str = 'md5',
                                  progress_callback=None) -> Dict[str, str]:
        """批量异步计算文件哈希"""
        import asyncio
        import hashlib

        semaphore = asyncio.Semaphore(self.max_concurrent)
        results = {}
        completed = 0
        total = len(file_paths)

        async def calculate_hash(file_path: Path) -> Tuple[str, str]:
            nonlocal completed

            async with semaphore:
                try:
                    hash_obj = hashlib.new(algorithm)
                    loop = asyncio.get_event_loop()

                    def read_and_hash():
                        with open(file_path, 'rb') as f:
                            while chunk := f.read(self.chunk_size):
                                hash_obj.update(chunk)
                        return hash_obj.hexdigest()

                    file_hash = await loop.run_in_executor(None, read_and_hash)

                    completed += 1
                    if progress_callback:
                        progress_callback(completed / total, f"计算哈希: {file_path.name}")

                    return str(file_path), file_hash

                except (OSError, IOError):
                    completed += 1
                    return str(file_path), ""

        # 并发计算所有文件哈希
        tasks = [calculate_hash(path) for path in file_paths]
        hash_results = await asyncio.gather(*tasks, return_exceptions=True)

        # 整理结果
        for result in hash_results:
            if isinstance(result, tuple) and len(result) == 2:
                path, file_hash = result
                results[path] = file_hash

        return results

    def run_async_batch_file_stats(self, file_paths: List[Path]) -> List[Dict[str, Any]]:
        """运行批量文件统计 - 同步接口"""
        loop = self.async_io._get_event_loop()
        if loop is None:
            # 回退到同步实现
            return self._sync_batch_file_stats(file_paths)

        try:
            import asyncio
            if loop.is_running():
                future = asyncio.ensure_future(self.async_batch_file_stats(file_paths))
                return asyncio.run_coroutine_threadsafe(future, loop).result(timeout=60)
            else:
                return loop.run_until_complete(self.async_batch_file_stats(file_paths))
        except Exception:
            return self._sync_batch_file_stats(file_paths)

    def _sync_batch_file_stats(self, file_paths: List[Path]) -> List[Dict[str, Any]]:
        """同步版本的批量文件统计"""
        results = []
        for file_path in file_paths:
            try:
                stat_info = file_path.stat()
                results.append({
                    'path': str(file_path),
                    'size': stat_info.st_size,
                    'mtime': stat_info.st_mtime,
                    'is_file': file_path.is_file(),
                    'exists': True
                })
            except (OSError, IOError):
                results.append({
                    'path': str(file_path),
                    'size': 0,
                    'mtime': 0,
                    'is_file': False,
                    'exists': False
                })
        return results


# ================== 内存感知流式处理器 ==================
class StreamFileProcessor:
    """内存感知流式文件处理器 - 智能处理大文件避免内存溢出"""

    def __init__(self, chunk_size: int = 1024 * 1024, memory_manager: 'MemoryManager' = None):
        self.base_chunk_size = chunk_size
        self.memory_manager = memory_manager
        self._adaptive_chunk_size = chunk_size
        self._processed_bytes = 0

    def _get_adaptive_chunk_size(self) -> int:
        """根据内存使用情况自适应调整块大小"""
        if not self.memory_manager:
            return self.base_chunk_size

        memory_info = self.memory_manager.get_memory_usage()
        memory_usage_percent = memory_info.get('rss_mb', 0) / self.memory_manager.max_memory_mb

        if memory_usage_percent > 0.8:
            # 内存使用过高，减小块大小
            self._adaptive_chunk_size = max(64 * 1024, self.base_chunk_size // 4)
        elif memory_usage_percent > 0.6:
            # 内存使用较高，适度减小块大小
            self._adaptive_chunk_size = max(256 * 1024, self.base_chunk_size // 2)
        else:
            # 内存使用正常，使用标准块大小
            self._adaptive_chunk_size = self.base_chunk_size

        return self._adaptive_chunk_size

    def calculate_file_hash(self, file_path: Path, algorithm: str = 'md5',
                          progress_callback=None) -> str:
        """内存优化的流式文件哈希计算"""
        import hashlib

        hash_obj = hashlib.new(algorithm)
        processed_bytes = 0

        try:
            file_size = file_path.stat().st_size

            with open(file_path, 'rb') as f:
                while True:
                    # 动态调整块大小
                    chunk_size = self._get_adaptive_chunk_size()
                    chunk = f.read(chunk_size)

                    if not chunk:
                        break

                    hash_obj.update(chunk)
                    processed_bytes += len(chunk)

                    # 定期检查内存并清理
                    if processed_bytes % (10 * 1024 * 1024) == 0:  # 每 10MB 检查一次
                        if self.memory_manager and self.memory_manager.should_cleanup():
                            self.memory_manager.cleanup_if_needed()

                    # 进度回调
                    if progress_callback and file_size > 0:
                        progress = processed_bytes / file_size
                        progress_callback(progress)

            return hash_obj.hexdigest()

        except (OSError, IOError) as e:
            logger.warning(f"计算文件哈希失败: {file_path}, 错误: {e}")
            return ""

    def get_file_size_stream(self, file_path: Path) -> int:
        """安全获取文件大小"""
        try:
            return file_path.stat().st_size
        except (OSError, IOError):
            return 0

    def copy_file_stream(self, src: Path, dst: Path, progress_callback=None) -> bool:
        """内存优化的流式文件复制"""
        try:
            src_size = src.stat().st_size
            copied_bytes = 0

            with open(src, 'rb') as src_file, open(dst, 'wb') as dst_file:
                while True:
                    chunk_size = self._get_adaptive_chunk_size()
                    chunk = src_file.read(chunk_size)

                    if not chunk:
                        break

                    dst_file.write(chunk)
                    copied_bytes += len(chunk)

                    # 内存检查和清理
                    if copied_bytes % (20 * 1024 * 1024) == 0:  # 每 20MB 检查一次
                        if self.memory_manager and self.memory_manager.should_cleanup():
                            self.memory_manager.cleanup_if_needed()

                    # 进度回调
                    if progress_callback and src_size > 0:
                        progress = copied_bytes / src_size
                        progress_callback(progress)

            return True

        except (OSError, IOError) as e:
            logger.warning(f"流式复制文件失败: {src} -> {dst}, 错误: {e}")
            return False

    def process_large_directory(self, directory: Path,
                              operation: str = 'size') -> Dict[str, Any]:
        """内存优化的大目录处理"""
        results = {
            'total_size': 0,
            'file_count': 0,
            'processed_files': [],
            'errors': []
        }

        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    try:
                        if operation == 'size':
                            file_size = self.get_file_size_stream(file_path)
                            results['total_size'] += file_size
                            results['file_count'] += 1

                            # 记录大文件
                            if file_size > 100 * 1024 * 1024:  # 大于 100MB
                                results['processed_files'].append({
                                    'path': str(file_path),
                                    'size': file_size
                                })

                        # 定期内存检查
                        if results['file_count'] % 1000 == 0:
                            if self.memory_manager and self.memory_manager.should_cleanup():
                                cleaned = self.memory_manager.cleanup_if_needed()
                                if cleaned.get('freed_mb', 0) > 0:
                                    logger.info(f"处理大目录时清理内存: {cleaned['freed_mb']:.1f}MB")

                    except (OSError, IOError) as e:
                        results['errors'].append(f"处理文件失败 {file_path}: {e}")

        except Exception as e:
            results['errors'].append(f"目录处理失败: {e}")

        return results

    def async_calculate_directory_size(self, path: Path) -> int:
        """异步计算目录大小"""
        total_size = 0
        file_operations = []

        # 收集所有文件操作
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    file_operations.append(('size', file_path, None))
        except (OSError, PermissionError):
            return 0

        # 异步执行文件大小计算
        if file_operations:
            async_processor = AsyncIOProcessor(max_concurrent=8)
            sizes = async_processor.async_file_operations(file_operations)
            total_size = sum(size for size in sizes if size is not None)

        return total_size


# ================== 高性能相似度计算 ==================
class FastSimilarityCalculator:
    """高性能相似度计算器"""

    @staticmethod
    def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
        """Jaccard 相似度计算 - 比 SequenceMatcher 更快"""
        if not set_a or not set_b:
            return 0.0

        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))

        return intersection / union if union > 0 else 0.0

    @staticmethod
    def word_overlap_ratio(search_words: Set[str], target_words: Set[str]) -> float:
        """词汇重叠比例"""
        if not search_words:
            return 0.0

        overlap = len(search_words.intersection(target_words))
        return overlap / len(search_words)

    @staticmethod
    def substring_bonus(search_str: str, target_str: str) -> float:
        """子字符串匹配奖励 - 增强版本"""
        # 完全匹配
        if search_str in target_str:
            return 0.4  # 提高奖励
        elif target_str in search_str:
            return 0.3  # 提高奖励

        # 连续词匹配奖励（针对 "The Studio" 这类搜索）
        search_words = search_str.split()
        target_words = target_str.split()

        if len(search_words) >= 2:
            search_phrase = ' '.join(search_words)
            target_phrase = ' '.join(target_words)
            if search_phrase in target_phrase or target_phrase in search_phrase:
                return 0.35

        return 0.0


# ================== 文件匹配器 ==================
class FileMatcher:
    """文件匹配器 - v1.5.1 高性能搜索优化版本"""

    VIDEO_EXTENSIONS = {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
        '.webm', '.m4v', '.3gp', '.ogv', '.ts', '.m2ts',
        '.mpg', '.mpeg', '.rm', '.rmvb', '.asf', '.divx'
    }

    STOP_WORDS = {
        'the', 'and', 'of', 'to', 'in', 'a', 'an', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had'
    }

    SEPARATORS = ['.', '_', '-', ':', '|', '\\', '/', '+', '(', ')', '[', ']']

    def __init__(self, base_directory: str, enable_cache: bool = True,
                 cache_duration: int = 3600, min_score: float = 0.6,
                 max_workers: int = 4):
        self.base_directory = Path(base_directory)
        self.min_score = min_score
        self.max_workers = max_workers
        self.cache = SearchCache(cache_duration) if enable_cache else None
        self.folder_info_cache = SearchCache(cache_duration) if enable_cache else None

        # 初始化性能监控和内存管理
        self.performance_monitor = PerformanceMonitor()
        self.memory_manager = MemoryManager()

        # 初始化智能索引
        self.smart_index = SmartIndexCache(cache_duration)

        # 初始化异步处理器
        self.async_processor = AsyncIOProcessor(max_workers)

        # 简化的相似度计算
        self.similarity_calc = FastSimilarityCalculator()
        self._compiled_patterns = self._compile_quality_patterns()

        if not self.base_directory.exists():
            logger.warning(f"基础目录不存在: {self.base_directory}")

    def _compile_quality_patterns(self) -> List:
        """预编译正则表达式模式"""
        import re
        quality_patterns = [
            r'\b(720p|1080p|4k|uhd|hd|sd|bluray|bdrip|webrip|hdtv)\b',
            r'\b(x264|x265|h264|h265|hevc)\b',
            r'\b(aac|ac3|dts|mp3)\b'
        ]
        return [re.compile(pattern, re.IGNORECASE) for pattern in quality_patterns]

    def _generate_cache_key(self, search_name: str) -> str:
        key_data = f"{search_name}:{self.base_directory}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def _normalize_string(self, text: str) -> str:
        """高性能字符串标准化 - v1.5.1 优化版本"""
        if not text:
            return ""

        # 缓存标准化结果
        cache_key = f"normalize:{text}"
        if self.cache:
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                return cached_result

        text = text.lower()

        # 使用预编译的正则表达式
        text = re.sub(r'\b(19|20)\d{2}\b', '', text)

        # 使用预编译的质量标识模式
        for pattern in self._compiled_patterns:
            text = pattern.sub('', text)

        # 批量替换分隔符（更高效）
        for sep in self.SEPARATORS:
            text = text.replace(sep, ' ')

        text = re.sub(r'\s+', ' ', text).strip()

        # 优化停用词移除 - 搜索优化版本
        words = text.split()
        # 对于短搜索词（≤3个词），不移除停用词，提高匹配准确性
        if len(words) > 3:
            # 使用集合操作，更高效
            word_set = set(words)
            filtered_set = word_set - self.STOP_WORDS
            if filtered_set:
                # 保持原始顺序
                words = [word for word in words if word in filtered_set]

        result = ' '.join(words)

        # 缓存结果
        if self.cache:
            self.cache.set(cache_key, result)

        return result

    def similarity(self, a: str, b: str) -> float:
        """高性能相似度计算 - v1.5.1 优化版本"""
        # 缓存相似度计算结果
        cache_key = f"sim:{a}:{b}"
        if self.cache:
            cached_score = self.cache.get(cache_key)
            if cached_score is not None:
                return cached_score

        a_normalized = self._normalize_string(a)
        b_normalized = self._normalize_string(b)

        # 快速完全匹配检查
        if a_normalized == b_normalized:
            score = 1.0
        else:
            # 使用更快的算法组合
            a_words = set(a_normalized.split())
            b_words = set(b_normalized.split())

            # 1. Jaccard 相似度（比 SequenceMatcher 更快）
            jaccard_score = self.similarity_calc.jaccard_similarity(a_words, b_words)

            # 2. 词汇重叠比例
            overlap_ratio = self.similarity_calc.word_overlap_ratio(a_words, b_words)

            # 3. 子字符串匹配奖励
            substring_bonus = self.similarity_calc.substring_bonus(a_normalized, b_normalized)

            # 组合得分 - 优化权重分配
            score = jaccard_score * 0.5 + overlap_ratio * 0.3 + substring_bonus * 0.2

            # 如果词汇重叠度很高，给予额外奖励
            if overlap_ratio >= 0.8:
                score = max(score, 0.9)
            elif overlap_ratio >= 0.6:
                score = max(score, 0.8)
            elif overlap_ratio >= 0.4:  # 新增中等匹配奖励
                score = max(score, 0.7)

        score = min(1.0, score)

        # 缓存结果
        if self.cache:
            self.cache.set(cache_key, score)

        return score

    def get_all_folders(self, max_depth: int = 3) -> List[Path]:
        """获取基础目录下的所有文件夹 - 异步I/O优化版本"""
        # 检查缓存
        cache_key = f"all_folders:{self.base_directory}:{max_depth}"
        if self.cache:
            cached_folders = self.cache.get(cache_key)
            if cached_folders is not None:
                return cached_folders

        self.performance_monitor.start_timer('folder_scanning')
        folders = []

        if not self.base_directory.exists():
            return folders

        try:
            # 尝试使用异步目录扫描
            async_folders = self._try_async_folder_scan(max_depth)
            if async_folders is not None:
                folders = async_folders
            else:
                # 回退到同步扫描
                folders = self._sync_folder_scan(max_depth)

            # 缓存结果（如果内存允许）
            if self.cache and not self.memory_manager.should_cleanup():
                self.cache.set(cache_key, folders)

        finally:
            scan_duration = self.performance_monitor.end_timer('folder_scanning')
            memory_info = self.memory_manager.get_memory_usage()

            if scan_duration > 3.0:
                logger.warning(f"文件夹扫描耗时较长: {scan_duration:.2f}s, 找到 {len(folders)} 个文件夹")

            print(f"  📊 内存使用: {memory_info['rss_mb']:.1f}MB, 找到 {len(folders)} 个文件夹")

        return folders

    def _try_async_folder_scan(self, max_depth: int) -> Optional[List[Path]]:
        """尝试异步文件夹扫描 - 添加超时保护"""
        try:
            # 使用异步目录扫描，添加超时限制
            import signal

            def timeout_handler(signum, frame):
                # 忽略未使用的参数警告
                _ = signum, frame
                raise TimeoutError("异步扫描超时")

            # 设置15秒超时
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(15)

            try:
                async_folders = self.async_processor.async_directory_scan(self.base_directory, max_depth)
                signal.alarm(0)  # 取消超时
                print(f"  ⚡ 异步扫描完成: 找到 {len(async_folders)} 个文件夹")
                return async_folders
            except TimeoutError:
                signal.alarm(0)  # 取消超时
                print(f"  ⏰ 异步扫描超时，回退到同步模式")
                return None

        except Exception as e:
            logger.debug(f"异步扫描失败，回退到同步模式: {e}")
            return None

    def _sync_folder_scan(self, max_depth: int) -> List[Path]:
        """同步文件夹扫描 - 优化版本，添加限制和超时"""
        folders = []
        start_time = time.time()

        # 从配置中获取限制参数，如果没有配置则使用默认值
        try:
            # 尝试从全局配置获取
            from pathlib import Path as PathLib
            config_path = PathLib.home() / ".torrent_maker" / "settings.json"
            if config_path.exists():
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                max_scan_time = settings.get('max_scan_time', 30)
                max_folders = settings.get('max_scan_folders', 5000)
            else:
                max_scan_time = 30
                max_folders = 5000
        except:
            max_scan_time = 30  # 最大扫描时间30秒
            max_folders = 5000  # 最大文件夹数量限制

        def _scan_directory_memory_optimized(path: Path, current_depth: int = 0):
            # 检查时间和数量限制
            if (time.time() - start_time > max_scan_time or
                len(folders) >= max_folders or
                current_depth >= max_depth):
                return

            # 定期检查内存使用
            if len(folders) % 500 == 0 and len(folders) > 0:
                cleaned = self.memory_manager.cleanup_if_needed()
                if cleaned.get('freed_mb', 0) > 0:
                    print(f"  🧹 内存清理: 释放 {cleaned['freed_mb']:.1f}MB")

                # 检查扫描时间
                elapsed = time.time() - start_time
                if elapsed > 15:  # 15秒后开始警告
                    print(f"  ⏰ 扫描耗时: {elapsed:.1f}s, 已找到 {len(folders)} 个文件夹")

            try:
                with os.scandir(path) as entries:
                    batch_folders = []
                    subdirs_to_scan = []

                    for entry in entries:
                        # 检查是否超时或超量
                        if (time.time() - start_time > max_scan_time or
                            len(folders) >= max_folders):
                            break

                        try:
                            if entry.is_dir(follow_symlinks=False):
                                # 安全处理文件路径，避免编码问题
                                try:
                                    folder_path = Path(entry.path)
                                    # 验证路径可以正确编码/解码
                                    str(folder_path).encode('utf-8').decode('utf-8')
                                    batch_folders.append(folder_path)

                                    # 只有在深度允许的情况下才添加到递归列表
                                    if current_depth + 1 < max_depth:
                                        subdirs_to_scan.append(folder_path)

                                    # 批量添加，减少内存分配
                                    if len(batch_folders) >= 50:  # 减少批量大小
                                        folders.extend(batch_folders)
                                        batch_folders.clear()

                                except (UnicodeDecodeError, UnicodeEncodeError) as e:
                                    # 跳过有编码问题的文件夹
                                    print(f"  ⚠️ 跳过编码问题文件夹: {entry.name} ({e})")
                                    continue

                        except (OSError, IOError) as e:
                            # 跳过无法访问的条目
                            continue

                    # 添加剩余的文件夹
                    if batch_folders:
                        folders.extend(batch_folders)

                    # 递归扫描子目录（限制数量）
                    for subdir in subdirs_to_scan[:20]:  # 限制每个目录最多扫描20个子目录
                        if (time.time() - start_time > max_scan_time or
                            len(folders) >= max_folders):
                            break
                        _scan_directory_memory_optimized(subdir, current_depth + 1)

            except (PermissionError, OSError, UnicodeDecodeError, UnicodeEncodeError) as e:
                # 增强异常处理，包括编码错误
                if isinstance(e, (UnicodeDecodeError, UnicodeEncodeError)):
                    print(f"  ⚠️ 目录编码问题: {path} ({e})")
                pass

        _scan_directory_memory_optimized(self.base_directory)

        elapsed = time.time() - start_time
        status = ""
        if elapsed > max_scan_time:
            status = " (已超时)"
        elif len(folders) >= max_folders:
            status = " (已达到数量限制)"

        print(f"  🔄 同步扫描完成: 找到 {len(folders)} 个文件夹, 耗时 {elapsed:.1f}s{status}")
        return folders

    def fuzzy_search(self, search_name: str, max_results: int = 10) -> List[Tuple[str, float]]:
        """智能模糊搜索 - v1.5.1 高性能优化版本"""
        self.performance_monitor.start_timer('fuzzy_search')

        try:
            # 检查缓存
            cache_key = self._generate_cache_key(search_name)
            if self.cache:
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    return cached_result[:max_results]

            all_folders = self.get_all_folders()
            if not all_folders:
                return []

            # 预处理搜索名称
            normalized_search = self._normalize_string(search_name)
            search_words = set(normalized_search.split())

            # 构建或更新智能索引
            if self.smart_index.is_expired():
                self.smart_index.build_index(all_folders, self._normalize_string)

            # 使用智能索引进行预筛选
            candidate_folders = self.smart_index.get_candidate_folders(search_words)

            # 如果预筛选结果太少，回退到全量搜索
            if len(candidate_folders) < max_results * 2:
                candidate_paths = all_folders
                print(f"  🔍 预筛选结果较少({len(candidate_folders)})，使用全量搜索")
            else:
                candidate_paths = [Path(path) for path in candidate_folders]
                print(f"  🎯 智能预筛选: {len(all_folders)} → {len(candidate_paths)} 个候选")

            matches = []

            def process_folder_fast(folder_path: Path) -> Optional[Tuple[str, float]]:
                """快速文件夹处理 - 增强编码安全"""
                try:
                    folder_name = folder_path.name
                    # 验证文件夹名称可以正确编码/解码
                    folder_name.encode('utf-8').decode('utf-8')
                    str(folder_path).encode('utf-8').decode('utf-8')

                    similarity_score = self.similarity(search_name, folder_name)

                    if similarity_score >= self.min_score:
                        return (str(folder_path), similarity_score)
                    return None
                except (UnicodeDecodeError, UnicodeEncodeError) as e:
                    # 跳过有编码问题的文件夹
                    print(f"  ⚠️ 跳过编码问题文件夹: {folder_path} ({e})")
                    return None
                except Exception:
                    return None

            # 智能并发策略
            folder_count = len(candidate_paths)
            if folder_count <= 50:
                # 少量文件夹，使用串行处理
                for folder in candidate_paths:
                    result = process_folder_fast(folder)
                    if result:
                        matches.append(result)
            else:
                # 大量文件夹，使用并行处理
                batch_size = min(500, folder_count)

                for i in range(0, folder_count, batch_size):
                    batch_folders = candidate_paths[i:i + batch_size]

                    with ThreadPoolExecutor(max_workers=min(self.max_workers, 4)) as executor:
                        future_to_folder = {
                            executor.submit(process_folder_fast, folder): folder
                            for folder in batch_folders
                        }

                        for future in as_completed(future_to_folder):
                            result = future.result()
                            if result:
                                matches.append(result)

            # 智能排序：相似度 + 路径长度（更短的路径优先）
            matches.sort(key=lambda x: (x[1], -len(x[0])), reverse=True)

            # 缓存结果
            if self.cache:
                self.cache.set(cache_key, matches)

            return matches[:max_results]

        finally:
            search_duration = self.performance_monitor.end_timer('fuzzy_search')
            matches_count = len(matches) if 'matches' in locals() else 0
            print(f"  🔍 搜索耗时: {search_duration:.3f}s, 找到 {matches_count} 个匹配项")

    def get_folder_info(self, folder_path: str) -> Dict[str, Any]:
        """获取文件夹详细信息 - 带缓存优化"""
        if not os.path.exists(folder_path):
            return {'exists': False}

        # 检查缓存
        cache_key = f"folder_info:{folder_path}"
        if self.folder_info_cache:
            cached_info = self.folder_info_cache.get(cache_key)
            if cached_info is not None:
                return cached_info

        self.performance_monitor.start_timer('folder_info_calculation')

        try:
            total_files = 0
            total_size = 0

            try:
                # 使用更高效的方法计算文件信息
                path_obj = Path(folder_path)
                for file_path in path_obj.rglob('*'):
                    if file_path.is_file():
                        total_files += 1
                        try:
                            total_size += file_path.stat().st_size
                        except (OSError, IOError):
                            pass
            except PermissionError:
                result = {'exists': True, 'readable': False}
                if self.folder_info_cache:
                    self.folder_info_cache.set(cache_key, result)
                return result

            size_str = self.format_size(total_size)

            result = {
                'exists': True,
                'readable': True,
                'total_files': total_files,
                'total_size': total_size,
                'size_str': size_str
            }

            # 缓存结果
            if self.folder_info_cache:
                self.folder_info_cache.set(cache_key, result)

            return result

        finally:
            self.performance_monitor.end_timer('folder_info_calculation')

    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def is_video_file(self, filename: str) -> bool:
        """检查文件是否为视频文件"""
        return Path(filename).suffix.lower() in self.VIDEO_EXTENSIONS

    def match_folders(self, search_name: str) -> List[Dict[str, Any]]:
        """搜索并返回匹配的文件夹信息"""
        matches = self.fuzzy_search(search_name)
        result = []

        for folder_path, score in matches:
            folder_info = self.get_folder_info(folder_path)
            if folder_info['exists']:
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

    def get_performance_stats(self) -> Dict[str, Any]:
        """获取搜索性能统计 - v1.5.1 增强版"""
        stats = self.performance_monitor.get_all_stats()
        memory_info = self.memory_manager.get_memory_usage()

        # 计算搜索效率指标
        search_stats = stats.get('fuzzy_search', {})
        folder_scan_stats = stats.get('folder_scanning', {})

        return {
            'search_performance': {
                'average_search_time': search_stats.get('average', 0),
                'total_searches': search_stats.get('count', 0),
                'fastest_search': search_stats.get('min', 0),
                'slowest_search': search_stats.get('max', 0)
            },
            'folder_scanning': {
                'average_scan_time': folder_scan_stats.get('average', 0),
                'total_scans': folder_scan_stats.get('count', 0)
            },
            'memory_usage': memory_info,
            'cache_performance': {
                'smart_index_expired': self.smart_index.is_expired(),
                'cache_enabled': self.cache is not None
            },
            'optimization_level': self._calculate_optimization_level(search_stats, memory_info)
        }

    def _calculate_optimization_level(self, search_stats: Dict, memory_info: Dict) -> str:
        """计算优化等级"""
        avg_search_time = search_stats.get('average', 0)
        memory_usage = memory_info.get('rss_mb', 0)

        if avg_search_time < 0.5 and memory_usage < 200:
            return "优秀 (A+)"
        elif avg_search_time < 1.0 and memory_usage < 300:
            return "良好 (B+)"
        elif avg_search_time < 2.0 and memory_usage < 400:
            return "一般 (C+)"
        else:
            return "需要优化 (D)"

    def cleanup_resources(self) -> Dict[str, int]:
        """清理资源"""
        cleaned_stats = {}

        # 清理内存
        cleaned_stats['memory_items'] = self.memory_manager.cleanup_memory()

        # 清理缓存
        if self.cache:
            # 这里可以添加缓存清理逻辑
            cleaned_stats['cache_items'] = 0

        # 重建索引
        if self.smart_index.is_expired():
            cleaned_stats['index_rebuilt'] = 1
        else:
            cleaned_stats['index_rebuilt'] = 0

        return cleaned_stats

    def extract_episode_info_simple(self, folder_path: str) -> Dict[str, Any]:
        """简单的剧集信息提取"""
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return {'episodes': [], 'season_info': '', 'total_episodes': 0}

        episodes = []
        seasons = set()

        try:
            for _, _, files in os.walk(folder_path):
                for file in files:
                    if self.is_video_file(file):
                        episode_info = self.parse_episode_from_filename(file)
                        if episode_info:
                            episodes.append(episode_info)
                            if episode_info['season']:
                                seasons.add(episode_info['season'])
        except (PermissionError, OSError):
            return {'episodes': [], 'season_info': '无法访问', 'total_episodes': 0}

        episodes.sort(key=lambda x: (x['season'] or 0, x['episode'] or 0))
        season_info = self.generate_season_summary(episodes, seasons)

        return {
            'episodes': episodes,
            'season_info': season_info,
            'total_episodes': len(episodes)
        }

    def parse_episode_from_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """从文件名中解析剧集信息"""
        import re

        patterns = [
            (r'[Ss](\d{1,2})[Ee](\d{1,3})', 'season_episode'),
            (r'[Ss]eason\s*(\d{1,2})\s*[Ee]pisode\s*(\d{1,3})', 'season_episode'),
            (r'第(\d{1,2})季第(\d{1,3})集', 'season_episode'),
            (r'(\d{1,2})x(\d{1,3})', 'season_episode'),
            (r'(?:[Ee][Pp]\.?\s*(\d{1,3})|第(\d{1,3})集)', 'episode_only'),
        ]

        for pattern, pattern_type in patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    if pattern_type == 'season_episode':
                        season = int(match.group(1))
                        episode = int(match.group(2))
                        if 1 <= season <= 50 and 1 <= episode <= 500:
                            return {
                                'season': season,
                                'episode': episode,
                                'filename': filename,
                                'pattern_type': pattern_type
                            }
                    elif pattern_type == 'episode_only':
                        episode = int(match.group(1) or match.group(2))
                        if 1 <= episode <= 500:
                            return {
                                'season': None,
                                'episode': episode,
                                'filename': filename,
                                'pattern_type': pattern_type
                            }
                except ValueError:
                    continue

        return None

    def generate_season_summary(self, episodes: list, seasons: set) -> str:
        """生成季度摘要信息"""
        if not episodes:
            return "无剧集信息"

        if not seasons or None in seasons:
            episode_numbers = [ep['episode'] for ep in episodes if ep.get('episode')]
            if episode_numbers:
                return self._format_episode_range(episode_numbers)
            else:
                return f"{len(episodes)}个视频"

        season_summaries = []
        for season in sorted(seasons):
            season_episodes = [ep for ep in episodes if ep.get('season') == season]
            episode_numbers = [ep['episode'] for ep in season_episodes if ep.get('episode')]

            if episode_numbers:
                episode_range = self._format_episode_range(episode_numbers)
                season_summary = f"S{season:02d}{episode_range}"
                season_summaries.append(season_summary)

        return ', '.join(season_summaries) if season_summaries else f"{len(episodes)}个视频"

    def _format_episode_range(self, episode_numbers: List[int]) -> str:
        """格式化集数范围"""
        if not episode_numbers:
            return ""

        episode_numbers = sorted(set(episode_numbers))

        if len(episode_numbers) == 1:
            return f"E{episode_numbers[0]:02d}"

        is_fully_continuous = all(
            episode_numbers[i] == episode_numbers[i-1] + 1
            for i in range(1, len(episode_numbers))
        )

        if is_fully_continuous:
            return f"E{episode_numbers[0]:02d}-E{episode_numbers[-1]:02d}"
        else:
            groups = []
            start = episode_numbers[0]
            end = episode_numbers[0]

            for i in range(1, len(episode_numbers)):
                if episode_numbers[i] == end + 1:
                    end = episode_numbers[i]
                else:
                    if start == end:
                        groups.append(f"E{start:02d}")
                    else:
                        groups.append(f"E{start:02d}-E{end:02d}")
                    start = episode_numbers[i]
                    end = episode_numbers[i]

            if start == end:
                groups.append(f"E{start:02d}")
            else:
                groups.append(f"E{start:02d}-E{end:02d}")

            return ",".join(groups)


# ================== 种子创建器 ==================
class TorrentCreator:
    """种子创建器 - v1.7.0高性能Python引擎版本"""

    DEFAULT_PIECE_SIZE = "auto"
    DEFAULT_COMMENT = f"Created by Torrent Maker v{VERSION}"
    PIECE_SIZES = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]

    # Piece Size 查找表 - 极速优化版本（更大piece size）
    PIECE_SIZE_LOOKUP = {
        # 文件大小范围 (MB) -> (piece_size_kb, log2_value)
        (0, 50): (128, 17),          # 小文件: 128KB pieces
        (50, 200): (256, 18),        # 中小文件: 256KB pieces
        (200, 500): (512, 19),       # 中等文件: 512KB pieces
        (500, 1000): (1024, 20),     # 较大文件: 1MB pieces
        (1000, 2000): (2048, 21),    # 大文件: 2MB pieces
        (2000, 5000): (4096, 22),    # 很大文件: 4MB pieces
        (5000, 10000): (8192, 23),   # 超大文件: 8MB pieces
        (10000, 20000): (16384, 24), # 巨大文件: 16MB pieces
        (20000, 50000): (32768, 25), # 超巨大文件: 32MB pieces
        (50000, float('inf')): (65536, 26)  # 极大文件: 64MB pieces
    }

    def __init__(self, tracker_links: List[str], output_dir: str = "output",
                 piece_size: Union[str, int] = "auto", private: bool = False,
                 comment: str = None, max_workers: int = 4, config_manager=None):
        self.tracker_links = list(tracker_links) if tracker_links else []
        self.output_dir = Path(output_dir)
        self.piece_size = piece_size
        self.private = private
        self.comment = comment or self.DEFAULT_COMMENT
        self.max_workers = max_workers
        self.config_manager = config_manager

        # 初始化性能监控和内存管理
        self.performance_monitor = PerformanceMonitor()
        self.memory_manager = MemoryManager()

        # 目录大小缓存
        self.size_cache = DirectorySizeCache()

        # 初始化 piece size 缓存
        self._piece_size_cache = {}

        # 初始化异步处理器
        self.async_processor = AsyncIOProcessor(max_workers)
        self.stream_processor = StreamFileProcessor(memory_manager=self.memory_manager)

        # 检测 mktorrent 可用性
        self.mktorrent_available = self._check_mktorrent()
        if not self.mktorrent_available:
            raise TorrentCreationError("mktorrent 不可用，请安装 mktorrent: apt-get install mktorrent 或 brew install mktorrent")

    def _check_mktorrent(self) -> bool:
        return shutil.which('mktorrent') is not None







    def _ensure_output_dir(self) -> None:
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise TorrentCreationError(f"无法创建输出目录: {e}")

    def _calculate_piece_size(self, total_size: int) -> int:
        """智能计算合适的piece大小 - 高性能优化版本"""
        # 检查缓存
        size_mb = total_size // (1024 * 1024)
        cache_key = f"size_{size_mb}"

        if cache_key in self._piece_size_cache:
            return self._piece_size_cache[cache_key]

        # 使用查找表快速确定 piece size
        for (min_size, max_size), (_, log2_value) in self.PIECE_SIZE_LOOKUP.items():
            if min_size <= size_mb < max_size:
                self._piece_size_cache[cache_key] = log2_value
                return log2_value

        # 回退到传统计算方法（用于极端情况）
        target_pieces = 1500
        optimal_piece_size = total_size // (target_pieces * 1024)

        for size in self.PIECE_SIZES:
            if size >= optimal_piece_size:
                import math
                log2_value = int(math.log2(size * 1024))
                self._piece_size_cache[cache_key] = log2_value
                return log2_value

        # 返回最大piece大小的指数值
        import math
        log2_value = int(math.log2(self.PIECE_SIZES[-1] * 1024))
        self._piece_size_cache[cache_key] = log2_value
        return log2_value

    def _get_optimal_piece_size_fast(self, total_size: int) -> Tuple[int, int]:
        """快速获取最优 piece size（KB 和 log2 值）"""
        size_mb = total_size // (1024 * 1024)

        # 直接查表，O(1) 时间复杂度
        for (min_size, max_size), (piece_size_kb, log2_value) in self.PIECE_SIZE_LOOKUP.items():
            if min_size <= size_mb < max_size:
                return piece_size_kb, log2_value

        # 默认返回最大值
        return 4096, 22

    def _get_directory_size(self, path: Path) -> int:
        """获取目录大小 - 使用缓存优化"""
        self.performance_monitor.start_timer('directory_size_calculation')
        try:
            size = self.size_cache.get_directory_size(path)
            return size
        finally:
            duration = self.performance_monitor.end_timer('directory_size_calculation')
            if duration > 5.0:  # 如果计算时间超过5秒，记录警告
                logger.warning(f"目录大小计算耗时较长: {duration:.2f}s for {path}")

    def _sanitize_filename(self, filename: str) -> str:
        import re
        unsafe_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(unsafe_chars, '_', filename)
        sanitized = sanitized.strip(' .')
        return sanitized if sanitized else "torrent"

    def _format_duration(self, duration_seconds: float) -> str:
        """格式化时间显示（支持分钟:秒和小时:分钟:秒格式）"""
        total_seconds = int(duration_seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"

    def _format_file_size(self, size_bytes: int) -> str:
        """格式化文件大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def _calculate_creation_speed(self, file_size_bytes: int, duration_seconds: float) -> str:
        """计算制种速度"""
        if duration_seconds <= 0:
            return "N/A"

        speed_bytes_per_sec = file_size_bytes / duration_seconds

        # 转换为合适的单位
        if speed_bytes_per_sec >= 1024 * 1024 * 1024:  # GB/s
            speed = speed_bytes_per_sec / (1024 * 1024 * 1024)
            return f"{speed:.2f} GB/s"
        elif speed_bytes_per_sec >= 1024 * 1024:  # MB/s
            speed = speed_bytes_per_sec / (1024 * 1024)
            return f"{speed:.2f} MB/s"
        elif speed_bytes_per_sec >= 1024:  # KB/s
            speed = speed_bytes_per_sec / 1024
            return f"{speed:.2f} KB/s"
        else:  # B/s
            return f"{speed_bytes_per_sec:.2f} B/s"

    def _detect_optimal_threads(self, file_size_bytes: int = 0) -> dict:
        """智能检测最优线程数配置"""
        import os

        # 获取系统信息
        cpu_count = os.cpu_count() or 4
        load_avg = 0.0
        memory_usage_percent = 50.0  # 默认值

        if hasattr(os, 'getloadavg'):
            try:
                load_avg = os.getloadavg()[0]
            except OSError:
                pass  # 在某些容器环境下可能失败

        try:
            import psutil
            memory_usage_percent = psutil.virtual_memory().percent
        except (ImportError, AttributeError):
            try:
                # 当 psutil 不可用时，回退到读取 /proc/meminfo (仅限Linux)
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                total_mem_match = re.search(r'MemTotal:\s+(\d+)', meminfo)
                available_mem_match = re.search(r'MemAvailable:\s+(\d+)', meminfo)
                if total_mem_match and available_mem_match:
                    total_mem = int(total_mem_match.group(1))
                    available_mem = int(available_mem_match.group(1))
                    if total_mem > 0:
                        memory_usage_percent = (1 - available_mem / total_mem) * 100
            except (IOError, AttributeError, ValueError):
                pass # 无法获取内存信息，使用默认值

        # 1. 基础线程数
        base_threads = cpu_count

        # 2. 根据文件大小调整策略
        file_size_gb = file_size_bytes / (1024 * 1024 * 1024) if file_size_bytes > 0 else 0
        if file_size_gb > 0:
            if file_size_gb < 2:  # 小文件 (<2GB)
                thread_limit = max(4, cpu_count // 2)
                base_threads = min(base_threads, thread_limit, 8)
            elif file_size_gb < 50: # 中等文件 (2GB-50GB)
                thread_limit = max(6, int(cpu_count * 0.75))
                base_threads = min(base_threads, thread_limit)

        # 3. 根据系统负载动态调整
        load_per_core = load_avg / cpu_count if cpu_count > 0 else 0
        if load_per_core > 0.7:  # 当每核心的平均负载 > 0.7 时，认为系统繁忙
            reduction_factor = 1.0 - min(0.5, (load_per_core - 0.7))
            base_threads = max(2, int(base_threads * reduction_factor))

        # 4. 根据内存使用情况调整
        if memory_usage_percent > 85:  # 内存使用率过高
            base_threads = max(2, int(base_threads * 0.8))

        # 5. mktorrent 的最优线程数上限, 对于高性能机器放宽到16
        optimal_threads = min(base_threads, 16)
        optimal_threads = max(optimal_threads, 2) # 确保至少使用2个线程

        return {
            'cpu_count': cpu_count,
            'optimal_threads': int(optimal_threads),
            'load_avg': load_avg,
            'memory_usage_percent': memory_usage_percent,
            'file_size_gb': file_size_gb,
            'recommendation': self._get_thread_recommendation(int(optimal_threads), cpu_count, file_size_bytes, load_per_core)
        }

    def _get_thread_recommendation(self, optimal_threads: int, cpu_count: int, file_size_bytes: int, load_per_core: float) -> str:
        """获取线程配置建议"""
        file_size_gb = file_size_bytes / (1024 * 1024 * 1024) if file_size_bytes > 0 else 0

        if load_per_core > 0.7:
            return f"系统负载较高 (每核负载 {load_per_core:.2f})，已自动减少线程"
        elif optimal_threads >= cpu_count * 0.9:
            return "系统资源充足，使用最大化线程以提升性能"
        elif file_size_gb > 50:
            return "超大文件处理，已启用更多线程加速"
        elif file_size_gb > 2:
            return "文件较大，已智能分配较多线程"
        elif file_size_gb > 0:
            return "小文件制种，已优化线程数以平衡开销和性能"
        elif optimal_threads < cpu_count * 0.5 and optimal_threads < 8:
            return "根据系统综合状态，使用保守线程策略"
        else:
            return "根据系统状态和文件大小智能调整"

    def _show_performance_suggestions(self, file_size_bytes: int, total_duration: float, mktorrent_duration: float):
        """显示性能优化建议"""
        file_size_gb = file_size_bytes / (1024 * 1024 * 1024)
        suggestions = []

        # 基于制种速度的建议
        speed_mbps = (file_size_bytes / (1024 * 1024)) / total_duration if total_duration > 0 else 0

        if speed_mbps < 50:  # 低于50MB/s
            suggestions.append("制种速度较慢，建议检查磁盘性能或减少系统负载")
        elif speed_mbps > 500:  # 高于500MB/s
            suggestions.append("制种速度优秀！当前配置表现良好")

        # 基于文件大小的建议
        if file_size_gb > 50:
            suggestions.append("大文件制种，建议使用SSD存储以提升性能")
        elif file_size_gb < 0.1:
            suggestions.append("小文件制种，当前配置已足够")

        # 基于效率的建议
        efficiency = (mktorrent_duration / total_duration) * 100 if total_duration > 0 else 0
        if efficiency < 70:
            suggestions.append("准备阶段耗时较长，可能是磁盘I/O或文件扫描导致")
        elif efficiency > 95:
            suggestions.append("mktorrent执行效率很高，系统配置优秀")

        # 显示建议
        if suggestions:
            print(f"\n  💡 性能建议:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"     {i}. {suggestion}")
        else:
            print(f"\n  💡 性能表现良好，无特殊建议")

    def _build_command(self, source_path: Path, output_file: Path,
                      piece_size: int = None, file_size_bytes: int = 0) -> List[str]:
        """构建优化的 mktorrent 命令"""
        command = ['mktorrent']

        # 添加 tracker 链接
        for tracker in self.tracker_links:
            command.extend(['-a', tracker])

        # 设置输出文件
        command.extend(['-o', str(output_file)])

        # 设置注释（简化以减少开销）
        comment = f"{self.comment}"
        command.extend(['-c', comment])

        # 设置 piece 大小
        if piece_size:
            command.extend(['-l', str(piece_size)])

        # 智能多线程处理
        thread_info = self._detect_optimal_threads(file_size_bytes)
        thread_count = thread_info['optimal_threads']

        command.extend(['-t', str(thread_count)])
        
        # 显示详细的线程配置信息
        print(f"  🖥️  系统CPU核心数: {thread_info['cpu_count']}")
        print(f"  🧵 最优线程数: {thread_count}")
        if thread_info['load_avg'] > 0:
            print(f"  📊 系统负载: {thread_info['load_avg']:.2f}")
        print(f"  💾 内存使用率: {thread_info['memory_usage_percent']:.1f}%")
        if thread_info['file_size_gb'] > 0:
            print(f"  📁 文件大小: {thread_info['file_size_gb']:.2f} GB")
        print(f"  💡 配置建议: {thread_info['recommendation']}")
        
        # 私有种子标记
        if self.private:
            command.append('-p')

        # 减少输出信息以提高性能（移除 -v 参数）
        # command.append('-v')  # 注释掉详细输出

        # 添加源路径
        command.append(str(source_path))

        return command

    def _get_mktorrent_version(self) -> str:
        """获取 mktorrent 版本信息"""
        try:
            result = subprocess.run(['mktorrent', '--help'],
                                  capture_output=True, text=True, timeout=5)
            if result.stdout:
                # 从帮助信息中提取版本
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'mktorrent' in line and '(' in line:
                        return line.strip()
            return "mktorrent (version unknown)"
        except Exception:
            return "mktorrent (version unknown)"

    def create_torrent(self, source_path: Union[str, Path],
                      custom_name: str = None,
                      progress_callback = None) -> Optional[str]:
        """创建种子文件 - 使用 mktorrent"""
        # 记录制种开始时间
        creation_start_time = time.time()
        start_time_str = datetime.now().strftime("%H:%M:%S")

        try:
            source_path = Path(source_path)

            if not source_path.exists():
                raise TorrentCreationError(f"源路径不存在: {source_path}")

            self._ensure_output_dir()

            if custom_name:
                torrent_name = self._sanitize_filename(custom_name)
            else:
                torrent_name = self._sanitize_filename(source_path.name)

            # 使用微秒级时间戳确保文件名唯一性
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            output_file = self.output_dir / f"{torrent_name}_{timestamp}.torrent"
            
            # 文件冲突检测和重试机制
            retry_count = 0
            while output_file.exists() and retry_count < 5:
                retry_count += 1
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                output_file = self.output_dir / f"{torrent_name}_{timestamp}_retry{retry_count}.torrent"

            # 计算文件大小和piece大小
            if self.piece_size == "auto":
                if source_path.is_dir():
                    total_size = self._get_directory_size(source_path)
                else:
                    total_size = source_path.stat().st_size

                piece_size_log2 = self._calculate_piece_size(total_size)
                piece_size_kb = (2 ** piece_size_log2) // 1024
                print(f"  🎯 自动选择 Piece 大小: {piece_size_kb}KB (文件大小: {self._format_file_size(total_size)})")
            elif isinstance(self.piece_size, int):
                # 如果用户设置的是KB值，需要转换为log2
                import math
                piece_size_bytes = self.piece_size * 1024
                piece_size_log2 = int(math.log2(piece_size_bytes))
                # 获取文件大小用于性能统计
                if source_path.is_dir():
                    total_size = self._get_directory_size(source_path)
                else:
                    total_size = source_path.stat().st_size
            else:
                piece_size_log2 = 18  # 默认256KB
                # 获取文件大小用于性能统计
                if source_path.is_dir():
                    total_size = self._get_directory_size(source_path)
                else:
                    total_size = source_path.stat().st_size

            print(f"  ⏰ 制种开始时间: {start_time_str}")

            # 使用 mktorrent 创建种子
            result_path = self._create_torrent_mktorrent(source_path, output_file, piece_size_log2, progress_callback, total_size, creation_start_time)

            return result_path

        except Exception as e:
            # 即使出错也显示耗时
            creation_duration = time.time() - creation_start_time
            print(f"  ❌ 制种失败，耗时: {self._format_duration(creation_duration)}")
            raise TorrentCreationError(f"创建种子文件时发生未知错误: {e}")



    def _create_torrent_mktorrent(self, source_path: Path, output_file: Path,
                                 piece_size_log2: int, progress_callback,
                                 file_size_bytes: int = 0, creation_start_time: float = None) -> str:
        """使用 mktorrent 创建种子"""
        # 记录mktorrent执行开始时间
        mktorrent_start_time = time.time()

        command = self._build_command(source_path, output_file, piece_size_log2, file_size_bytes)

        # 记录调试信息
        if piece_size_log2:
            actual_piece_size = 2 ** piece_size_log2
            print(f"  🔧 Piece大小: 2^{piece_size_log2} = {actual_piece_size} bytes ({actual_piece_size // 1024} KB)")

        if progress_callback:
            progress_callback(f"正在使用mktorrent创建种子文件: {source_path.name}")

        print(f"  🚀 开始执行 mktorrent...")

        # 执行mktorrent命令
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=3600,
                env=dict(os.environ, LANG='C', LC_ALL='C')
            )

            # 记录执行结果（如果需要调试）
            if result.stderr:
                logger.warning(f"mktorrent stderr: {result.stderr}")

        except subprocess.CalledProcessError as e:
            error_msg = f"mktorrent执行失败: {e}"
            if e.stderr:
                error_msg += f"\n错误信息: {e.stderr}"
            raise TorrentCreationError(error_msg)

        except subprocess.TimeoutExpired:
            raise TorrentCreationError("种子创建超时")

        # 计算mktorrent执行时间
        mktorrent_duration = time.time() - mktorrent_start_time

        if not output_file.exists():
            raise TorrentCreationError("种子文件创建失败：输出文件不存在")

        # 验证种子文件
        if not self.validate_torrent(output_file):
            raise TorrentCreationError("种子文件验证失败")

        # 计算总制种时间和显示性能统计
        if creation_start_time:
            total_duration = time.time() - creation_start_time
            end_time_str = datetime.now().strftime("%H:%M:%S")

            # 获取种子文件大小
            torrent_file_size = output_file.stat().st_size if output_file.exists() else 0

            print(f"\n  🎉 制种完成！")
            print(f"  ✅ 完成时间: {end_time_str}")
            print(f"  ⏱️  总耗时: {self._format_duration(total_duration)}")
            print(f"  🔧 mktorrent耗时: {self._format_duration(mktorrent_duration)}")

            # 计算准备时间（总时间 - mktorrent时间）
            prep_duration = total_duration - mktorrent_duration
            if prep_duration > 0.1:  # 只有当准备时间超过0.1秒时才显示
                print(f"  ⚙️  准备耗时: {self._format_duration(prep_duration)}")

            # 显示详细性能统计信息
            if file_size_bytes > 0:
                file_size_str = self._format_file_size(file_size_bytes)
                creation_speed = self._calculate_creation_speed(file_size_bytes, total_duration)
                mktorrent_speed = self._calculate_creation_speed(file_size_bytes, mktorrent_duration)

                print(f"\n  📊 性能统计:")
                print(f"     📁 源文件大小: {file_size_str}")
                print(f"     📄 种子文件大小: {self._format_file_size(torrent_file_size)}")
                print(f"     🚀 总体制种速度: {creation_speed}")
                print(f"     ⚡ mktorrent速度: {mktorrent_speed}")

                # 计算效率指标
                efficiency = (mktorrent_duration / total_duration) * 100 if total_duration > 0 else 0
                print(f"     📈 制种效率: {efficiency:.1f}% (mktorrent占比)")

                # 提供性能建议
                self._show_performance_suggestions(file_size_bytes, total_duration, mktorrent_duration)

        if progress_callback:
            progress_callback(f"种子文件创建成功: {output_file.name}")

        return str(output_file)

    def create_torrents_batch(self, source_paths: List[Union[str, Path]],
                             progress_callback = None) -> List[Tuple[str, Optional[str], Optional[str]]]:
        """批量创建种子文件 - 高性能并发处理"""
        if not source_paths:
            return []

        results = []
        total_count = len(source_paths)

        # 根据任务数量选择最优并发策略
        if total_count <= 2:
            # 少量任务使用串行处理，避免并发开销
            for i, source_path in enumerate(source_paths):
                try:
                    if progress_callback:
                        progress_callback(f"正在处理 ({i + 1}/{total_count}): {Path(source_path).name}")
                    result_path = self.create_torrent(source_path)
                    results.append((str(source_path), result_path, None))
                except Exception as e:
                    results.append((str(source_path), None, str(e)))
            return results

        def create_single_with_error_handling(args):
            index, source_path = args
            try:
                if progress_callback:
                    progress_callback(f"正在处理 ({index + 1}/{total_count}): {Path(source_path).name}")

                result_path = self.create_torrent(source_path)
                return (str(source_path), result_path, None)
            except Exception as e:
                return (str(source_path), None, str(e))

        # 对于 CPU 密集型任务，优先使用进程池
        use_process_pool = total_count > 4 and self.max_workers > 2

        if use_process_pool:
            # 使用进程池处理大批量任务
            try:
                with ProcessPoolExecutor(max_workers=min(self.max_workers, total_count, 4)) as executor:
                    # 提交所有任务
                    future_to_path = {
                        executor.submit(create_single_with_error_handling, (i, path)): path
                        for i, path in enumerate(source_paths)
                    }

                    # 收集结果
                    for future in as_completed(future_to_path):
                        try:
                            result = future.result()
                            results.append(result)
                        except Exception as e:
                            source_path = future_to_path[future]
                            results.append((str(source_path), None, str(e)))
            except Exception as e:
                # 进程池失败时回退到线程池
                logger.warning(f"进程池执行失败，回退到线程池: {e}")
                use_process_pool = False

        if not use_process_pool:
            # 使用线程池处理中等批量任务
            with ThreadPoolExecutor(max_workers=min(self.max_workers, total_count)) as executor:
                # 提交所有任务
                future_to_path = {
                    executor.submit(create_single_with_error_handling, (i, path)): path
                    for i, path in enumerate(source_paths)
                }

                # 收集结果
                for future in as_completed(future_to_path):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        source_path = future_to_path[future]
                        results.append((str(source_path), None, str(e)))

        return results

    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计信息 - v1.5.1 第二阶段增强版"""
        stats = self.performance_monitor.get_all_stats()
        cache_stats = self.size_cache.get_cache_stats()
        memory_info = self.memory_manager.get_memory_usage()

        # 计算性能改进指标
        creation_stats = stats.get('total_torrent_creation', {})
        mktorrent_stats = stats.get('mktorrent_execution', {})
        piece_calc_stats = stats.get('piece_size_calculation', {})

        return {
            'performance': stats,
            'cache': cache_stats,
            'memory_management': {
                'current_usage_mb': memory_info.get('rss_mb', 0),
                'memory_limit_mb': self.memory_manager.max_memory_mb,
                'memory_efficiency': self._calculate_memory_efficiency(memory_info),
                'cleanup_needed': self.memory_manager.should_cleanup()
            },
            'piece_size_cache': {
                'cached_calculations': len(self._piece_size_cache),
                'cache_entries': list(self._piece_size_cache.keys())[:5]  # 显示前5个
            },
            'async_processing': {
                'max_concurrent_operations': self.async_processor.max_concurrent,
                'stream_chunk_size_mb': self.stream_processor.base_chunk_size / (1024 * 1024)
            },
            'summary': {
                'total_torrents_created': creation_stats.get('count', 0),
                'average_creation_time': creation_stats.get('average', 0),
                'average_mktorrent_time': mktorrent_stats.get('average', 0),
                'average_size_calculation_time': stats.get('directory_size_calculation', {}).get('average', 0),
                'average_piece_calculation_time': piece_calc_stats.get('average', 0),
                'cache_hit_rate': cache_stats.get('hit_rate', 0),
                'memory_usage_mb': memory_info.get('rss_mb', 0),
                'performance_grade': self._calculate_performance_grade_v2(creation_stats, cache_stats, memory_info)
            },
            'optimization_suggestions': self._generate_optimization_suggestions_v2(stats, cache_stats, memory_info)
        }

    def _calculate_memory_efficiency(self, memory_info: Dict) -> str:
        """计算内存使用效率"""
        usage_mb = memory_info.get('rss_mb', 0)
        limit_mb = self.memory_manager.max_memory_mb

        if usage_mb == 0:
            return "未知"

        efficiency = (limit_mb - usage_mb) / limit_mb
        if efficiency > 0.7:
            return "优秀"
        elif efficiency > 0.5:
            return "良好"
        elif efficiency > 0.3:
            return "一般"
        else:
            return "需要优化"

    def _calculate_performance_grade_v2(self, creation_stats: Dict, cache_stats: Dict, memory_info: Dict) -> str:
        """计算性能等级 - v1.5.1 第二阶段版本"""
        avg_time = creation_stats.get('average', 0)
        hit_rate = cache_stats.get('hit_rate', 0)
        memory_mb = memory_info.get('rss_mb', 0)

        # 综合评分系统
        time_score = 100 if avg_time < 10 else max(0, 100 - (avg_time - 10) * 3)
        cache_score = hit_rate * 100
        memory_score = max(0, 100 - memory_mb / 5)  # 500MB 为满分

        total_score = (time_score * 0.4 + cache_score * 0.3 + memory_score * 0.3)

        if total_score >= 90:
            return "优秀 (A+)"
        elif total_score >= 80:
            return "良好 (B+)"
        elif total_score >= 70:
            return "一般 (C+)"
        elif total_score >= 60:
            return "及格 (D+)"
        else:
            return "需要优化 (F)"

    def _generate_optimization_suggestions_v2(self, stats: Dict, cache_stats: Dict, memory_info: Dict) -> List[str]:
        """生成优化建议 - v1.5.1 第二阶段版本"""
        suggestions = []

        # 检查创建时间
        creation_avg = stats.get('total_torrent_creation', {}).get('average', 0)
        if creation_avg > 30:
            suggestions.append("种子创建时间较长，建议检查磁盘性能或减少文件数量")
        elif creation_avg > 15:
            suggestions.append("种子创建时间偏长，可以考虑调整 piece size 或启用更多并发")

        # 检查缓存命中率
        hit_rate = cache_stats.get('hit_rate', 0)
        if hit_rate < 0.3:
            suggestions.append("缓存命中率很低，建议增加缓存时间或检查重复操作模式")
        elif hit_rate < 0.6:
            suggestions.append("缓存命中率偏低，建议优化缓存策略")

        # 检查内存使用
        memory_mb = memory_info.get('rss_mb', 0)
        if memory_mb > 400:
            suggestions.append("内存使用较高，建议启用内存清理或减少缓存大小")
        elif memory_mb > 300:
            suggestions.append("内存使用偏高，建议监控内存使用情况")

        # 检查 mktorrent 执行时间 - 适应新的 piece size 策略
        mktorrent_avg = stats.get('mktorrent_execution', {}).get('average', 0)
        if mktorrent_avg > 60:  # 提高阈值，适应大 piece size
            suggestions.append("mktorrent 执行时间较长，建议检查 CPU 性能或磁盘 I/O 性能")

        # 检查目录扫描性能
        scan_avg = stats.get('directory_size_calculation', {}).get('average', 0)
        if scan_avg > 5:
            suggestions.append("目录扫描较慢，建议使用 SSD 或减少扫描深度")

        if not suggestions:
            suggestions.append("🎉 性能表现优秀！所有指标都在最佳范围内")

        return suggestions

    def _calculate_performance_grade(self, creation_stats: Dict, cache_stats: Dict) -> str:
        """计算性能等级 - 兼容性方法"""
        return self._calculate_performance_grade_v2(creation_stats, cache_stats, {'rss_mb': 0})

    def _generate_optimization_suggestions(self, stats: Dict, cache_stats: Dict) -> List[str]:
        """生成优化建议 - 兼容性方法"""
        return self._generate_optimization_suggestions_v2(stats, cache_stats, {'rss_mb': 0})

    def clear_caches(self) -> Dict[str, int]:
        """清理所有缓存 - v1.5.1 第二阶段增强版"""
        cleared_counts = {}

        # 清理目录大小缓存
        self.size_cache.clear_cache()
        cleared_counts['directory_size_cache'] = 0

        # 清理 piece size 缓存
        piece_cache_count = len(self._piece_size_cache)
        self._piece_size_cache.clear()
        cleared_counts['piece_size_cache'] = piece_cache_count

        # 清理过期缓存
        expired_count = self.size_cache.cleanup_expired()
        cleared_counts['expired_entries'] = expired_count

        # v1.5.1 新增：深度内存管理清理
        memory_cleaned = self.memory_manager.cleanup_memory()
        cleared_counts.update(memory_cleaned)

        # 获取内存分析
        memory_analysis = self.memory_manager.get_memory_analysis()
        cleared_counts['memory_analysis'] = {
            'freed_mb': memory_cleaned.get('freed_mb', 0),
            'trend': memory_analysis['memory_trend']['trend'],
            'recommendations': memory_analysis['recommendations'][:2]  # 只显示前2个建议
        }

        return cleared_counts

    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息 - v1.5.1 新增"""
        memory_info = self.memory_manager.get_memory_usage()

        return {
            'version': VERSION,
            'optimization_level': f'{VERSION_NAME} - Single File',
            'features': [
                'Smart Piece Size Calculation',
                'LRU Directory Cache',
                'Multi-threaded mktorrent',
                'Intelligent Search Index',
                'Memory Management',
                'Async I/O Processing',
                'Stream File Processing'
            ],
            'memory_info': memory_info,
            'performance_grade': self._calculate_performance_grade_v2({}, {}, memory_info),
            'cache_status': {
                'directory_cache_size': len(self.size_cache._cache) if hasattr(self.size_cache, '_cache') else 0,
                'piece_cache_size': len(self._piece_size_cache)
            }
        }

    def validate_torrent(self, torrent_path: Union[str, Path]) -> bool:
        """验证种子文件的有效性"""
        try:
            torrent_path = Path(torrent_path)

            if not torrent_path.exists():
                return False

            if not torrent_path.suffix.lower() == '.torrent':
                return False

            file_size = torrent_path.stat().st_size
            if file_size == 0:
                return False

            try:
                with open(torrent_path, 'rb') as f:
                    header = f.read(10)
                    if not header.startswith(b'd'):
                        return False
            except Exception:
                return False

            return True

        except Exception:
            return False


# ================== 搜索历史管理 ==================
class SearchHistory:
    """搜索历史管理器"""

    def __init__(self, config_dir: str = None, max_history: int = 50):
        """初始化搜索历史管理器"""
        if config_dir is None:
            config_dir = os.path.expanduser("~/.torrent_maker")

        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.history_file = self.config_dir / "search_history.json"
        self.max_history = max_history
        self.history: List[Dict[str, Any]] = []

        self._load_history()

    def _load_history(self):
        """加载搜索历史"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])
                    self._cleanup_old_history()
            else:
                self.history = []
        except Exception as e:
            print(f"⚠️ 加载搜索历史失败: {e}")
            self.history = []

    def _save_history(self):
        """保存搜索历史"""
        try:
            data = {
                'history': self.history,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 保存搜索历史失败: {e}")

    def _cleanup_old_history(self):
        """清理过期的历史记录"""
        try:
            from datetime import timedelta
            cutoff_time = datetime.now() - timedelta(days=30)

            self.history = [
                item for item in self.history
                if datetime.fromisoformat(item.get('timestamp', '1970-01-01'))
                > cutoff_time
            ]

            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]

        except Exception as e:
            print(f"⚠️ 清理历史记录失败: {e}")

    def add_search(self, query: str, results_count: int = 0,
                   resource_folder: str = None) -> None:
        """添加搜索记录"""
        if not query or not query.strip():
            return

        query = query.strip()

        # 检查是否已存在相同的搜索
        recent_queries = [item['query'] for item in self.history[-10:]]
        if query in recent_queries:
            for item in reversed(self.history):
                if item['query'] == query:
                    item['timestamp'] = datetime.now().isoformat()
                    item['count'] = item.get('count', 0) + 1
                    item['last_results_count'] = results_count
                    if resource_folder:
                        item['resource_folder'] = resource_folder
                    break
        else:
            record = {
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'results_count': results_count,
                'count': 1,
                'last_results_count': results_count
            }

            if resource_folder:
                record['resource_folder'] = resource_folder

            self.history.append(record)

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        self._save_history()

    def get_recent_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的搜索记录"""
        sorted_history = sorted(
            self.history,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        return sorted_history[:limit]

    def get_recent_queries(self, limit: int = 10) -> List[str]:
        """获取最近的搜索查询字符串"""
        recent_searches = self.get_recent_searches(limit)
        return [item['query'] for item in recent_searches]

    def get_statistics(self) -> Dict[str, Any]:
        """获取搜索历史统计信息"""
        if not self.history:
            return {
                'total_searches': 0,
                'unique_queries': 0,
                'average_results': 0,
                'most_searched': None,
                'recent_activity': 0
            }

        total_searches = sum(item.get('count', 1) for item in self.history)
        unique_queries = len(self.history)

        results_counts = [item.get('last_results_count', 0) for item in self.history]
        average_results = sum(results_counts) / len(results_counts) if results_counts else 0

        most_searched = max(self.history, key=lambda x: x.get('count', 0))

        from datetime import timedelta
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_activity = sum(
            1 for item in self.history
            if datetime.fromisoformat(item.get('timestamp', '1970-01-01')) > recent_cutoff
        )

        return {
            'total_searches': total_searches,
            'unique_queries': unique_queries,
            'average_results': round(average_results, 1),
            'most_searched': most_searched,
            'recent_activity': recent_activity
        }

    def get_popular_queries(self, limit: int = 10) -> List[str]:
        """获取热门搜索查询"""
        if not self.history:
            return []
        
        # 按搜索次数排序
        sorted_history = sorted(
            self.history,
            key=lambda x: x.get('count', 0),
            reverse=True
        )
        return [item['query'] for item in sorted_history[:limit]]

    def clear_history(self) -> bool:
        """清空搜索历史"""
        try:
            self.history = []
            self._save_history()
            return True
        except Exception as e:
            print(f"❌ 清空搜索历史失败: {e}")
            return False


# ================== 主程序 ==================
class TorrentMakerApp:
    """Torrent Maker 主应用程序 - v1.6.0 彻底重构版"""

    def __init__(self):
        self.config = ConfigManager()
        self.config_manager = self.config  # 为了兼容性添加别名
        self.matcher = None
        self.creator = None
        self.queue_manager = None  # 队列管理器
        self.status_display = QueueStatusDisplay()  # 队列状态显示管理器
        
        # 队列显示配置
        self.queue_display_config = {
            'default_mode': 'standard',  # compact, standard, detailed
            'auto_update_interval': 2.0,  # 自动更新间隔(秒)
            'show_progress': True,  # 是否显示进度信息
            'show_statistics': True,  # 是否显示统计信息
            'compact_on_start': True,  # 任务启动时使用简洁模式
        }
        
        # 初始化增强功能模块
        if ENHANCED_FEATURES_AVAILABLE:
            self.search_history = SearchHistory()
            self.search_suggester = SmartSearchSuggester(self.search_history)
            self.path_completer = PathCompleter()
            self.progress_monitor = None  # 将在需要时初始化
        else:
            self.search_history = None
            self.search_suggester = None
            self.path_completer = None
            self.progress_monitor = None
            
        self._init_components()

    def _init_components(self):
        """初始化组件"""
        try:
            # 初始化文件匹配器
            resource_folder = self.config.get_resource_folder()
            enable_cache = self.config.settings.get('enable_cache', True)
            cache_duration = self.config.settings.get('cache_duration', 3600)
            max_workers = self.config.settings.get('max_concurrent_operations', 4)

            self.matcher = FileMatcher(
                resource_folder,
                enable_cache=enable_cache,
                cache_duration=cache_duration,
                max_workers=max_workers
            )

            # 初始化种子创建器
            trackers = self.config.get_trackers()
            output_folder = self.config.get_output_folder()

            self.creator = TorrentCreator(
                tracker_links=trackers,
                output_dir=output_folder,
                max_workers=max_workers,
                config_manager=self.config
            )
            
            # 初始化队列管理器（已内置）
            try:
                # 使用绝对路径确保队列文件保存在正确位置
                queue_file = os.path.expanduser("~/.torrent_maker/torrent_queue.json")
                self.queue_manager = TorrentQueueManager(
                    self.creator,
                    max_concurrent=max_workers,
                    save_file=queue_file
                )
                # 设置回调函数
                self.queue_manager.set_callbacks(
                    on_task_start=self._on_queue_task_start,
                    on_task_complete=self._on_queue_task_complete,
                    on_task_failed=self._on_queue_task_failed,
                    on_progress_update=self._on_queue_progress_update
                )
            except Exception as e:
                print(f"⚠️ 队列管理功能初始化失败: {e}")
                self.queue_manager = None

        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            sys.exit(1)

    def _check_queue_status_before_operation(self, operation_name: str) -> bool:
        """在执行操作前检查队列运行状态"""
        if not self.queue_manager:
            return True  # 如果没有队列管理器，允许操作
            
        if self.queue_manager.is_running():
            print(f"\n⚠️ 队列正在运行中")
            print(f"当前正在执行制种任务，建议等待完成后再进行{operation_name}操作。")
            print("\n选择操作:")
            print("1. 🔄 继续操作（可能影响队列性能）")
            print("2. 📊 查看队列状态")
            print("3. ⏸️ 暂停队列后继续")
            print("4. 🔙 返回主菜单")
            
            while True:
                choice = input("\n请选择 (1-4): ").strip()
                if choice == '1':
                    print(f"\n⚡ 继续执行{operation_name}操作...")
                    return True
                elif choice == '2':
                    self._display_enhanced_queue_status()
                    continue
                elif choice == '3':
                    if self.queue_manager.pause_queue():
                        print("\n⏸️ 队列已暂停")
                        return True
                    else:
                        print("\n❌ 暂停队列失败")
                        return False
                elif choice == '4':
                    return False
                else:
                    print("❌ 无效选择，请重新输入")
        
        return True

    def _display_enhanced_queue_status(self):
        """显示增强的队列状态信息（使用详细模式）"""
        self.status_display.display_status(self.queue_manager, mode="detailed", force_update=True)
        
        # 显示统计信息
        stats = status['statistics']
        print(f"\n📊 统计信息:")
        print(f"  总任务数: {status['total_tasks']}")
        print(f"  已完成: {stats['completed_tasks']}")
        print(f"  失败: {stats['failed_tasks']}")
        print(f"  成功率: {stats['success_rate']:.1f}%")
        if stats['average_processing_time'] > 0:
            print(f"  平均处理时间: {stats['average_processing_time']:.1f}秒")
        
        print("\n" + "=" * 60)

    def _add_queue_task_interactive(self, queue_manager):
        """交互式添加队列任务"""
        print("\n" + "=" * 50)
        print("           ➕ 添加制种任务")
        print("=" * 50)
        
        # 获取文件路径
        if self.path_completer:
            file_path = self.path_completer.get_input("请输入文件或文件夹路径: ")
        else:
            file_path = input("请输入文件或文件夹路径: ").strip()
        
        if not file_path:
            print("❌ 路径不能为空")
            return
            
        # 检查路径是否存在
        if not os.path.exists(file_path):
            print(f"❌ 路径不存在: {file_path}")
            return
        
        # 选择预设配置
        print("\n选择预设配置:")
        presets = ['standard', 'high_quality', 'fast', 'custom']
        for i, preset in enumerate(presets, 1):
            print(f"{i}. {preset}")
        
        preset_choice = input("\n请选择预设 (1-4, 默认1): ").strip()
        try:
            preset_index = int(preset_choice) - 1 if preset_choice else 0
            if 0 <= preset_index < len(presets):
                preset = presets[preset_index]
            else:
                preset = 'standard'
        except ValueError:
            preset = 'standard'
        
        # 选择优先级
        print("\n选择任务优先级:")
        print("1. 低")
        print("2. 普通")
        print("3. 高")
        
        priority_choice = input("\n请选择优先级 (1-3, 默认2): ").strip()
        try:
            priority_index = int(priority_choice) - 1 if priority_choice else 1
            priorities = [TaskPriority.LOW, TaskPriority.NORMAL, TaskPriority.HIGH]
            if 0 <= priority_index < len(priorities):
                priority = priorities[priority_index]
            else:
                priority = TaskPriority.NORMAL
        except ValueError:
            priority = TaskPriority.NORMAL
        
        # 添加任务
        try:
            task_id = queue_manager.add_torrent_task(file_path, preset, priority)
            print(f"\n✅ 任务已添加到队列")
            print(f"📋 任务ID: {task_id}")
            print(f"📁 路径: {file_path}")
            print(f"⚙️ 预设: {preset}")
            print(f"🔥 优先级: {priority.value}")
        except Exception as e:
            print(f"❌ 添加任务失败: {e}")
    
    def _parse_task_selection(self, input_str: str, max_index: int) -> tuple[list[int], str]:
        """解析任务选择输入
        
        Args:
            input_str: 用户输入字符串
            max_index: 最大任务索引
            
        Returns:
            tuple: (索引列表, 错误信息)
        """
        input_str = input_str.strip().lower()
        
        # 处理特殊命令
        if input_str in ['0', 'cancel', '取消']:
            return [], "cancelled"
        if input_str in ['all', '*', '全部']:
            return list(range(max_index)), ""
            
        try:
            indices = set()
            
            # 分割逗号分隔的部分
            parts = [part.strip() for part in input_str.split(',')]
            
            for part in parts:
                if '-' in part:
                    # 处理范围 (如 1-5)
                    range_parts = part.split('-')
                    if len(range_parts) != 2 or not range_parts[0] or not range_parts[1]:
                        return [], f"无效的范围格式: {part}"
                    
                    try:
                        start = int(range_parts[0]) - 1  # 转换为0基索引
                        end = int(range_parts[1]) - 1
                    except ValueError:
                        return [], f"无效的范围格式: {part}"
                    
                    if start > end:
                        return [], f"范围起始值不能大于结束值: {part}"
                    if start < 0 or end >= max_index:
                        return [], f"范围超出有效索引 (1-{max_index}): {part}"
                        
                    indices.update(range(start, end + 1))
                else:
                    # 处理单个数字
                    index = int(part) - 1  # 转换为0基索引
                    if index < 0 or index >= max_index:
                        return [], f"索引超出范围 (1-{max_index}): {part}"
                    indices.add(index)
                    
            return sorted(list(indices)), ""
            
        except ValueError:
            return [], "请输入有效的数字、范围或逗号分隔的组合"
        except Exception as e:
            return [], f"解析输入时出错: {e}"
    
    def _confirm_batch_deletion(self, tasks_to_delete: list, task_list: list) -> bool:
        """确认批量删除操作
        
        Args:
            tasks_to_delete: 要删除的任务索引列表
            task_list: 完整任务列表
            
        Returns:
            bool: 用户是否确认删除
        """
        if len(tasks_to_delete) == 1:
            # 单个任务删除
            task = task_list[tasks_to_delete[0]]
            if task.status == TaskStatus.RUNNING:
                print(f"\n⚠️ 任务 '{task.name}' 正在运行中")
                confirm = input("确认要强制删除正在运行的任务吗? (y/N): ").strip().lower()
                return confirm in ['y', 'yes', '是']
            else:
                confirm = input(f"\n确认删除任务 '{task.name}'? (y/N): ").strip().lower()
                return confirm in ['y', 'yes', '是']
        else:
            # 批量删除确认
            print(f"\n📋 将要删除 {len(tasks_to_delete)} 个任务:")
            print("-" * 60)
            
            running_count = 0
            for i, task_index in enumerate(tasks_to_delete[:10], 1):  # 最多显示10个
                task = task_list[task_index]
                status_icon = {
                    TaskStatus.WAITING: '⏳',
                    TaskStatus.RUNNING: '🔄',
                    TaskStatus.COMPLETED: '✅',
                    TaskStatus.FAILED: '❌',
                    TaskStatus.CANCELLED: '🚫'
                }.get(task.status, '❓')
                
                if task.status == TaskStatus.RUNNING:
                    running_count += 1
                    
                print(f"{i:2d}. {task.name[:40]:<40} {status_icon}{task.status.value}")
                
            if len(tasks_to_delete) > 10:
                print(f"    ... 还有 {len(tasks_to_delete) - 10} 个任务")
                
            print("-" * 60)
            
            if running_count > 0:
                print(f"⚠️ 警告: 其中 {running_count} 个任务正在运行中，删除将强制停止")
                
            confirm = input(f"\n确认批量删除这 {len(tasks_to_delete)} 个任务? (y/N): ").strip().lower()
            return confirm in ['y', 'yes', '是']

    def _remove_queue_task_interactive(self, queue_manager):
        """交互式删除队列任务（支持批量删除）"""
        print("\n" + "=" * 50)
        print("           ➖ 删除队列任务")
        print("=" * 50)
        
        # 获取所有任务
        all_tasks = queue_manager.get_all_tasks()
        if not all_tasks:
            print("\n📭 队列为空，没有任务可删除")
            return
        
        # 显示任务列表
        print("\n📋 当前任务列表:")
        print("-" * 80)
        print(f"{'序号':<4} {'任务名称':<30} {'状态':<10} {'优先级':<8}")
        print("-" * 80)
        
        task_list = []
        for i, task in enumerate(all_tasks, 1):
            status_icon = {
                TaskStatus.WAITING: '⏳',
                TaskStatus.RUNNING: '🔄',
                TaskStatus.COMPLETED: '✅',
                TaskStatus.FAILED: '❌',
                TaskStatus.CANCELLED: '🚫'
            }.get(task.status, '❓')
            
            print(f"{i:<4} {task.name[:29]:<30} {status_icon}{task.status.value:<9} {task.priority.value:<8}")
            task_list.append(task)
        
        print("-" * 80)
        
        # 显示输入提示
        print("\n💡 支持的输入格式:")
        print("   单个: 5          删除第5个任务")
        print("   范围: 1-12       删除第1到12个任务")
        print("   列表: 1,3,5      删除第1、3、5个任务")
        print("   混合: 1-3,5,8-10 删除第1-3、5、8-10个任务")
        print("   全部: all 或 *   删除所有任务")
        print("   取消: 0 或 cancel")
        
        # 获取用户选择
        choice = input(f"\n请选择要删除的任务 (支持上述格式): ").strip()
        
        # 解析用户输入
        task_indices, error_msg = self._parse_task_selection(choice, len(task_list))
        
        if error_msg == "cancelled":
            print("❌ 已取消删除操作")
            return
        elif error_msg:
            print(f"❌ {error_msg}")
            return
        elif not task_indices:
            print("❌ 没有选择任何任务")
            return
            
        # 确认删除
        if not self._confirm_batch_deletion(task_indices, task_list):
            print("❌ 已取消删除操作")
            return
            
        # 执行批量删除
        success_count = 0
        failed_count = 0
        
        print(f"\n🔄 开始删除 {len(task_indices)} 个任务...")
        
        for i, task_index in enumerate(task_indices, 1):
            task = task_list[task_index]
            print(f"[{i}/{len(task_indices)}] 删除: {task.name[:40]}...", end=" ")
            
            try:
                if queue_manager.remove_task(task.id):
                    print("✅")
                    success_count += 1
                else:
                    print("❌")
                    failed_count += 1
            except Exception as e:
                print(f"❌ ({e})")
                failed_count += 1
                
        # 显示删除结果统计
        print(f"\n📊 删除完成:")
        print(f"   ✅ 成功: {success_count} 个")
        if failed_count > 0:
            print(f"   ❌ 失败: {failed_count} 个")
        print(f"   📋 总计: {len(task_indices)} 个")

    def display_header(self):
        """显示程序头部信息"""
        print("🎬" + "=" * 60)
        print(f"           {FULL_VERSION_INFO}")
        print("           基于 mktorrent 的种子制作工具")
        print("=" * 62)
        print()
        print(f"🎯 v{VERSION} {VERSION_NAME}更新:")
        print("  🎨 版本信息显示优化（简洁清晰的界面展示）")
        print("  🔧 预设配置文件自动初始化（解决文件缺失问题）")
        print("  ⚡ 队列管理参数修复（提升系统稳定性）")
        print("  📋 程序启动流程优化（更快的响应速度）")
        print("  🚀 用户体验持续改进（专注核心功能展示）")
        print()

    def display_menu(self):
        """显示主菜单"""
        print("📋 主菜单:")
        print("  1. 🔍 搜索并制作种子")
        print("  2. ⚡ 快速制种 (直接输入路径)")
        print("  3. 📁 批量制种")
        print("  4. ⚙️  配置管理")
        print("  5. 📊 查看性能统计")
        print("  6. 🔄 队列管理")
        if ENHANCED_FEATURES_AVAILABLE:
            print("  7. 📝 搜索历史管理")
            print("  8. ❓ 帮助")
            print("  0. 🚪 退出")
        else:
            print("  7. ❓ 帮助")
            print("  0. 🚪 退出")
        print()

    def search_and_create(self):
        """搜索并制作种子"""
        # 检查队列运行状态
        if not self._check_queue_status_before_operation("搜索并制种"):
            return
            
        while True:
            # 显示搜索建议（如果有增强功能）
            recent_searches = []
            if self.search_history:
                recent_searches = self.search_history.get_recent_queries(5)
                if recent_searches:
                    print("\n📝 最近搜索:")
                    for i, search in enumerate(recent_searches, 1):
                        # 兼容不同的数据结构
                        if isinstance(search, str):
                            print(f"  {i}. {search}")
                        elif hasattr(search, 'query'):
                            result_count = getattr(search, 'result_count', 0)
                            print(f"  {i}. {search.query} (结果: {result_count})")
                        else:
                            print(f"  {i}. {search}")
                    print()
            
            # 获取用户输入（支持路径补全和快捷键选择）
            if recent_searches:
                prompt = "🔍 请输入要搜索的影视剧名称 (输入数字1-5选择历史搜索，回车返回主菜单): "
            else:
                prompt = "🔍 请输入要搜索的影视剧名称 (回车返回主菜单): "
            
            if self.path_completer:
                search_name = self.path_completer.get_input(prompt)
            else:
                search_name = input(prompt).strip()
                
            if not search_name:
                break
            
            # 检查是否是快捷键选择（数字1-5）
            if search_name.isdigit() and recent_searches:
                choice_num = int(search_name)
                if 1 <= choice_num <= len(recent_searches):
                    selected_search = recent_searches[choice_num - 1]
                    # 兼容不同的数据结构
                    if isinstance(selected_search, str):
                        search_name = selected_search
                    elif hasattr(selected_search, 'query'):
                        search_name = selected_search.query
                    else:
                        search_name = str(selected_search)
                    print(f"\n✨ 已选择历史搜索: {search_name}")
                else:
                    print(f"❌ 无效选择，请输入1-{len(recent_searches)}之间的数字")
                    continue

            print(f"\n🔄 正在搜索 '{search_name}'...")
            start_time = time.time()

            try:
                results = self.matcher.match_folders(search_name)
                search_time = time.time() - start_time
                
                # 记录搜索历史
                if self.search_history:
                    self.search_history.add_search(search_name, len(results), search_time)

                if not results:
                    print(f"❌ 未找到匹配的文件夹 (搜索耗时: {search_time:.3f}s)")
                    
                    # 提供智能搜索建议
                    if self.search_suggester:
                        suggestions = self.search_suggester.get_search_suggestions(search_name)
                        if suggestions:
                            print("\n💡 搜索建议:")
                            for suggestion in suggestions:
                                print(f"  • {suggestion}")
                    
                    # 询问是否继续搜索
                    while True:
                        continue_choice = input("是否继续搜索其他内容？(y/n): ").strip().lower()
                        if continue_choice in ['n', 'no', '否']:
                            return  # 返回主菜单
                        elif continue_choice in ['y', 'yes', '是', '']:
                            break  # 继续搜索循环
                        else:
                            print("请输入 y(是) 或 n(否)")
                    continue

                print(f"✅ 找到 {len(results)} 个匹配结果 (搜索耗时: {search_time:.3f}s)")
                print()

                # 显示搜索结果
                for i, result in enumerate(results, 1):
                    status = "✅" if result['readable'] else "❌"
                    print(f"  {i:2d}. {status} {result['name']}")
                    print(f"      📊 匹配度: {result['score']}% | 📁 文件: {result['file_count']}个 | 💾 大小: {result['size']}")
                    if result['episodes']:
                        print(f"      🎬 剧集: {result['episodes']}")
                    # 显示文件夹路径
                    folder_path = result['path']
                    # 如果路径太长，显示相对路径或缩短路径
                    if len(folder_path) > 80:
                        # 尝试显示相对于资源文件夹的路径
                        resource_folder = self.config.get_resource_folder()
                        if folder_path.startswith(resource_folder):
                            relative_path = os.path.relpath(folder_path, resource_folder)
                            print(f"      📂 路径: .../{relative_path}")
                        else:
                            # 如果路径太长，显示开头和结尾
                            print(f"      📂 路径: {folder_path[:30]}...{folder_path[-30:]}")
                    else:
                        print(f"      📂 路径: {folder_path}")
                    print()

                # 选择文件夹
                choice = input("请选择要制作种子的文件夹编号 (支持多选，如: 1,3,5，回车跳过): ").strip()
                if not choice:
                    # 询问是否继续搜索
                    while True:
                        continue_choice = input("是否继续搜索其他内容？(y/n): ").strip().lower()
                        if continue_choice in ['n', 'no', '否']:
                            return  # 返回主菜单
                        elif continue_choice in ['y', 'yes', '是', '']:
                            break  # 继续搜索循环
                        else:
                            print("请输入 y(是) 或 n(否)")
                    continue

                # 解析选择并执行批量制种
                selected_results = self._parse_selection(choice, results)
                if selected_results:
                    self._execute_batch_creation(selected_results)
                else:
                    print("❌ 无效的选择格式")
                    # 询问是否继续搜索
                    while True:
                        continue_choice = input("是否继续搜索其他内容？(y/n): ").strip().lower()
                        if continue_choice in ['n', 'no', '否']:
                            return  # 返回主菜单
                        elif continue_choice in ['y', 'yes', '是', '']:
                            break  # 继续搜索循环
                        else:
                            print("请输入 y(是) 或 n(否)")
                    continue

                # 询问是否继续搜索
                while True:
                    continue_choice = input("\n是否继续搜索其他内容？(y/n): ").strip().lower()
                    if continue_choice in ['n', 'no', '否']:
                        return  # 返回主菜单
                    elif continue_choice in ['y', 'yes', '是', '']:
                        break  # 继续搜索循环
                    else:
                        print("请输入 y(是) 或 n(否)")

            except (UnicodeDecodeError, UnicodeEncodeError) as e:
                print(f"❌ 搜索过程中发生编码错误: {e}")
                print("💡 建议: 检查资源文件夹中是否有包含特殊字符的文件名")
                print("💡 解决方案: 可以尝试重命名有问题的文件夹，或清理缓存")

                # 提供清理缓存选项
                clear_cache = input("是否清理缓存并重试？(y/n): ").strip().lower()
                if clear_cache in ['y', 'yes', '是']:
                    try:
                        if hasattr(self.matcher, 'cache') and self.matcher.cache:
                            self.matcher.cache._cache.clear()
                            print("✅ 缓存已清理")
                        if hasattr(self.matcher, 'folder_info_cache') and self.matcher.folder_info_cache:
                            self.matcher.folder_info_cache._cache.clear()
                            print("✅ 文件夹信息缓存已清理")
                        continue  # 重新尝试搜索
                    except Exception as cache_e:
                        print(f"⚠️ 清理缓存时出错: {cache_e}")

                # 发生错误时也询问是否继续
                while True:
                    continue_choice = input("\n是否继续搜索其他内容？(y/n): ").strip().lower()
                    if continue_choice in ['n', 'no', '否']:
                        return  # 返回主菜单
                    elif continue_choice in ['y', 'yes', '是', '']:
                        break  # 继续搜索循环
                    else:
                        print("请输入 y(是) 或 n(否)")

            except Exception as e:
                print(f"❌ 搜索过程中发生未知错误: {e}")
                print(f"❌ 错误类型: {type(e).__name__}")

                # 发生错误时也询问是否继续
                while True:
                    continue_choice = input("\n是否继续搜索其他内容？(y/n): ").strip().lower()
                    if continue_choice in ['n', 'no', '否']:
                        return  # 返回主菜单
                    elif continue_choice in ['y', 'yes', '是', '']:
                        break  # 继续搜索循环
                    else:
                        print("请输入 y(是) 或 n(否)")

    def _create_single_torrent(self, folder_info: Dict[str, Any]) -> bool:
        """创建单个种子文件"""
        try:
            folder_path = folder_info['path']
            folder_name = folder_info['name']

            # 显示开始信息
            print(f"\n" + "="*60)
            print(f"🔄 开始制种: {folder_name}")
            print(f"📁 源路径: {folder_path}")
            print(f"⏰ 开始时间: {datetime.now().strftime('%H:%M:%S')}")
            print("="*60)

            # 初始化进度监控
            if ENHANCED_FEATURES_AVAILABLE and self.progress_monitor is None:
                self.progress_monitor = TorrentProgressMonitor()
            
            def progress_callback(message):
                print(f"  📈 {message}")
                if self.progress_monitor:
                    self.progress_monitor.update_progress(message)

            # 记录开始时间用于总体统计
            start_time = time.time()
            
            # 启动进度监控
            if self.progress_monitor:
                self.progress_monitor.start_monitoring(folder_name, folder_path)

            torrent_path = self.creator.create_torrent(
                folder_path,
                folder_name,
                progress_callback
            )
            
            # 停止进度监控
            if self.progress_monitor:
                self.progress_monitor.stop_monitoring()

            if torrent_path and self.creator.validate_torrent(torrent_path):
                # 计算总耗时
                total_time = time.time() - start_time

                print(f"\n🎉 制种成功完成!")
                print(f"✅ 种子文件: {os.path.basename(torrent_path)}")
                print(f"📍 保存位置: {os.path.dirname(torrent_path)}")
                print(f"⏱️  总耗时: {self.creator._format_duration(total_time)}")
                print("="*60)
                return True
            else:
                print(f"\n❌ 制种失败!")
                print(f"❌ 种子创建失败或验证失败")
                print("="*60)
                return False

        except Exception as e:
            print(f"\n❌ 制种过程中发生错误!")
            print(f"❌ 错误信息: {e}")
            print("="*60)
            return False

    def quick_create(self):
        """快速制种"""
        # 检查队列运行状态
        if not self._check_queue_status_before_operation("快速制种"):
            return
            
        print("\n" + "="*60)
        print("⚡ 快速制种模式")
        print("="*60)
        print("支持格式:")
        print("  - 单个路径: /path/to/folder")
        print("  - 多个路径: /path1;/path2;/path3")
        print("="*60)

        # 使用路径补全功能获取输入
        if self.path_completer:
            paths_input = self.path_completer.get_input("请输入文件夹路径: ")
        else:
            paths_input = input("请输入文件夹路径: ").strip()
            
        if not paths_input:
            return

        paths = [p.strip() for p in paths_input.split(';') if p.strip()]

        # 显示任务概览
        print(f"\n📋 任务概览:")
        print(f"   📁 待处理路径数: {len(paths)}")
        print(f"   ⏰ 开始时间: {datetime.now().strftime('%H:%M:%S')}")

        # 记录总开始时间
        total_start_time = time.time()
        success_count = 0

        for i, path in enumerate(paths, 1):
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                print(f"\n[{i}/{len(paths)}] 处理路径: {expanded_path}")
                folder_info = {
                    'path': expanded_path,
                    'name': os.path.basename(expanded_path)
                }
                if self._create_single_torrent(folder_info):
                    success_count += 1
            else:
                print(f"\n[{i}/{len(paths)}] ❌ 路径不存在: {expanded_path}")

        # 显示总结
        total_duration = time.time() - total_start_time
        print(f"\n" + "="*60)
        print(f"🎉 快速制种任务完成!")
        print(f"✅ 成功: {success_count}/{len(paths)}")
        if success_count < len(paths):
            print(f"❌ 失败: {len(paths) - success_count}/{len(paths)}")
        print(f"⏱️  总耗时: {self.creator._format_duration(total_duration)}")
        print(f"🏁 完成时间: {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)

    def batch_create(self):
        """统一的批量制种功能"""
        # 检查队列运行状态
        if not self._check_queue_status_before_operation("批量制种"):
            return
            
        print("\n📦 批量制种")
        print("=" * 50)
        print("选择批量制种方式:")
        print("1. 🔍 搜索并选择文件夹")
        print("2. 📁 直接输入文件夹路径")
        print("0. 🔙 返回主菜单")
        print()

        choice = input("请选择方式 (0-2): ").strip()

        if choice == '0':
            return
        elif choice == '1':
            self._batch_create_from_search()
        elif choice == '2':
            self._batch_create_from_paths()
        else:
            print("❌ 无效选择")

    def _batch_create_from_search(self):
        """从搜索结果中批量制种"""
        print("\n🔍 搜索文件夹进行批量制种")
        print("=" * 40)

        search_name = input("请输入要搜索的影视剧名称: ").strip()
        if not search_name:
            print("❌ 搜索名称不能为空")
            return

        print(f"\n🔄 正在搜索 '{search_name}'...")
        start_time = time.time()

        try:
            results = self.matcher.match_folders(search_name)
            search_time = time.time() - start_time

            if not results:
                print(f"❌ 未找到匹配的文件夹 (搜索耗时: {search_time:.3f}s)")
                return

            print(f"✅ 找到 {len(results)} 个匹配结果 (搜索耗时: {search_time:.3f}s)")
            print()

            # 显示搜索结果
            for i, result in enumerate(results, 1):
                status = "✅" if result['readable'] else "❌"
                print(f"  {i:2d}. {status} {result['name']}")
                print(f"      📊 匹配度: {result['score']}% | 📁 文件: {result['file_count']}个 | 💾 大小: {result['size']}")
                if result['episodes']:
                    print(f"      🎬 剧集: {result['episodes']}")
                print(f"      📂 路径: {self._format_path_display(result['path'])}")
                print()

            # 选择文件夹进行批量制种
            choice = input("请选择要制作种子的文件夹编号 (支持多选，如: 1,3,5 或 1-5，回车取消): ").strip()
            if not choice:
                print("❌ 已取消批量制种")
                return

            # 解析选择
            selected_results = self._parse_selection(choice, results)
            if not selected_results:
                print("❌ 无效的选择")
                return

            # 执行批量制种
            self._execute_batch_creation(selected_results)

        except Exception as e:
            print(f"❌ 搜索过程中发生错误: {e}")

    def _batch_create_from_paths(self):
        """从直接输入的路径批量制种"""
        print("\n📁 直接输入路径进行批量制种")
        print("=" * 40)
        print("💡 提示：输入多个文件夹路径，每行一个")
        print("💡 输入空行结束输入")
        print("💡 支持拖拽文件夹到终端")
        print()

        paths = []
        print("请输入文件夹路径（每行一个，空行结束）:")

        while True:
            path = input(f"路径 {len(paths) + 1}: ").strip()
            if not path:
                break

            # 清理路径
            path = path.strip('"\'')
            path = os.path.expanduser(path)

            if not os.path.exists(path):
                print(f"⚠️ 路径不存在，跳过: {path}")
                continue

            if not os.path.isdir(path):
                print(f"⚠️ 不是文件夹，跳过: {path}")
                continue

            paths.append(path)
            print(f"✅ 已添加: {os.path.basename(path)}")

        if not paths:
            print("❌ 没有有效的路径")
            return

        # 转换为结果格式以便统一处理
        results = []
        for path in paths:
            results.append({
                'path': path,
                'name': os.path.basename(path),
                'readable': True
            })

        # 执行批量制种
        self._execute_batch_creation(results)

    def _format_path_display(self, folder_path: str) -> str:
        """格式化路径显示"""
        # 如果路径太长，显示相对路径或缩短路径
        if len(folder_path) > 80:
            # 尝试显示相对于资源文件夹的路径
            resource_folder = self.config.get_resource_folder()
            if folder_path.startswith(resource_folder):
                relative_path = os.path.relpath(folder_path, resource_folder)
                return f".../{relative_path}"
            else:
                # 如果路径太长，显示开头和结尾
                return f"{folder_path[:30]}...{folder_path[-30:]}"
        else:
            return folder_path

    def _parse_selection(self, choice: str, results: list) -> list:
        """解析用户选择的文件夹"""
        selected_results = []
        try:
            selected_indices = []
            for part in choice.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    selected_indices.extend(range(start, end + 1))
                else:
                    selected_indices.append(int(part))

            # 验证选择并收集结果
            for idx in selected_indices:
                if 1 <= idx <= len(results):
                    selected_results.append(results[idx - 1])
                else:
                    print(f"⚠️ 忽略无效编号: {idx}")

        except ValueError:
            print("❌ 无效的选择格式")
            return []

        return selected_results

    def _execute_batch_creation(self, selected_results: list):
        """执行批量制种 - 集成队列管理"""
        if not selected_results:
            print("❌ 没有选择任何文件夹")
            return

        print(f"\n📋 将要处理 {len(selected_results)} 个文件夹:")
        for i, result in enumerate(selected_results, 1):
            print(f"  {i}. {result['name']}")

        # 预设模式选择
        print("\n🎯 选择制种预设模式:")
        if hasattr(self.config, 'display_presets_menu'):
            self.config.display_presets_menu()
            preset_choice = input("\n请选择预设模式 (回车使用标准模式): ").strip()
            
            available_presets = self.config.get_available_presets() if hasattr(self.config, 'get_available_presets') else ['standard']
            if preset_choice and preset_choice in available_presets:
                selected_preset = preset_choice
            else:
                selected_preset = 'standard'
        else:
            selected_preset = 'standard'
        
        print(f"✅ 已选择预设: {selected_preset}")

        # 队列管理选项
        print("\n⚙️ 队列管理选项:")
        print("1. 🚀 立即开始 (传统模式)")
        print("2. 📋 添加到队列 (推荐)")
        
        queue_choice = input("请选择处理方式 (1-2, 默认2): ").strip()
        use_queue = queue_choice != '1'
        
        if use_queue:
            self._execute_batch_with_queue(selected_results, selected_preset)
        else:
            self._execute_batch_traditional(selected_results, selected_preset)
    
    def _execute_batch_with_queue(self, selected_results: list, preset: str):
        """使用队列管理执行批量制种"""
        try:
            # 使用内部定义的队列管理器
            # TorrentQueueManager 和 TaskPriority 已在文件中定义
            
            # 初始化队列管理器
            max_concurrent = self.config.get_setting('max_concurrent_operations', 4) if hasattr(self.config, 'get_setting') else 4
            # 使用与主队列管理器相同的文件路径
            queue_file = os.path.expanduser("~/.torrent_maker/torrent_queue.json")
            queue_manager = TorrentQueueManager(
                torrent_creator=self.creator,
                max_concurrent=max_concurrent,
                save_file=queue_file
            )
            
            # 设置回调函数
            queue_manager.on_task_start = self._on_queue_task_start
            queue_manager.on_task_complete = self._on_queue_task_complete
            queue_manager.on_task_failed = self._on_queue_task_failed
            queue_manager.on_progress_update = self._on_queue_progress_update
            
            print(f"\n📋 添加 {len(selected_results)} 个任务到队列...")
            
            # 批量添加任务
            task_ids = []
            for result in selected_results:
                task_id = queue_manager.add_torrent_task(
                    file_path=result['path'],
                    preset=preset,
                    priority=TaskPriority.NORMAL
                )
                task_ids.append(task_id)
            
            print(f"✅ 已添加 {len(task_ids)} 个任务到队列")
            
            # 询问用户后续操作
            print("\n📋 任务已添加到队列，请选择后续操作:")
            print("1. 🔍 继续搜索")
            print("2. 🚀 启动队列")
            print("3. ⚙️ 进入队列管理")
            print("4. 🏠 返回主菜单")
            
            while True:
                choice = input("请选择操作 (1-4, 默认1): ").strip()
                if not choice:
                    choice = '1'
                
                if choice == '1':
                    print("🔍 继续搜索...")
                    return  # 返回到搜索流程
                elif choice == '2':
                    print("🚀 启动队列...")
                    queue_manager.start_queue()
                    print("✅ 队列已启动")
                    return
                elif choice == '3':
                    print("⚙️ 进入队列管理...")
                    self._show_queue_management_interface(queue_manager, task_ids)
                    return
                elif choice == '4':
                    print("🏠 返回主菜单")
                    return
                else:
                    print("❌ 无效选择，请输入 1-4")
            
        except ImportError:
            print("⚠️ 队列管理功能不可用，使用传统模式")
            self._execute_batch_traditional(selected_results, preset)
        except Exception as e:
            print(f"❌ 队列管理初始化失败: {e}")
            print("🔄 回退到传统模式")
            self._execute_batch_traditional(selected_results, preset)
    
    def _execute_batch_traditional(self, selected_results: list, preset: str):
        """传统批量制种模式"""
        confirm = input(f"\n确认批量制种这 {len(selected_results)} 个文件夹? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("❌ 已取消批量制种")
            return

        # 应用预设配置
        if hasattr(self.config, 'apply_preset'):
            self.config.apply_preset(preset)
            print(f"✅ 已应用预设配置: {preset}")

        print(f"\n🚀 开始批量制种...")
        print("=" * 50)

        # 批量创建种子
        success_count = 0
        for i, result in enumerate(selected_results, 1):
            print(f"\n[{i}/{len(selected_results)}] 正在处理: {result['name']}")
            if self._create_single_torrent(result):
                success_count += 1

        print(f"\n🎉 批量制种完成!")
        print(f"✅ 成功: {success_count}/{len(selected_results)}")
        if success_count < len(selected_results):
            print(f"❌ 失败: {len(selected_results) - success_count}")
        print(f"✅ 成功率: {success_count/len(selected_results)*100:.1f}%")
    

    
    def _display_queue_status(self, status: dict = None, mode: str = "standard"):
        """显示队列状态（统一接口）"""
        self.status_display.display_status(self.queue_manager, mode=mode, force_update=True)
    
    def _display_task_list(self, queue_manager, task_ids: list):
        """显示任务列表"""
        print("\n📋 任务列表:")
        print("-" * 80)
        print(f"{'序号':<4} {'任务名称':<25} {'状态':<10} {'进度':<8} {'预设':<10}")
        print("-" * 80)
        
        for i, task_id in enumerate(task_ids[:10], 1):  # 只显示前10个
            task = queue_manager.get_task(task_id)
            if task:
                status_icon = {
                    'waiting': '⏳',
                    'running': '🔄',
                    'completed': '✅',
                    'failed': '❌',
                    'paused': '⏸️',
                    'cancelled': '🚫'
                }.get(task.status.value, '❓')
                
                progress_str = f"{task.progress*100:.1f}%" if task.progress > 0 else "-"
                
                print(f"{i:<4} {task.name[:24]:<25} {status_icon}{task.status.value:<9} {progress_str:<8} {task.preset:<10}")
        
        if len(task_ids) > 10:
            print(f"... 还有 {len(task_ids) - 10} 个任务")
        print("-" * 80)
    
    def _show_detailed_statistics(self, queue_manager):
        """显示详细统计信息"""
        print("\n" + "=" * 50)
        print("           📊 详细统计信息")
        print("=" * 50)
        
        status = queue_manager.get_queue_status()
        stats = status['statistics']
        status_counts = status['status_counts']
        
        print("📋 任务状态分布:")
        for status_name, count in status_counts.items():
            if count > 0:
                icon = {
                    'waiting': '⏳',
                    'running': '🔄',
                    'completed': '✅',
                    'failed': '❌',
                    'paused': '⏸️',
                    'cancelled': '🚫'
                }.get(status_name, '❓')
                print(f"  {icon} {status_name}: {count}")
        
        print(f"\n⏱️ 性能统计:")
        print(f"  总处理时间: {stats['total_processing_time']:.1f}秒")
        if stats['completed_tasks'] > 0:
            print(f"  平均处理时间: {stats['average_processing_time']:.1f}秒")
            success_rate = (stats['completed_tasks'] / (stats['completed_tasks'] + stats['failed_tasks'])) * 100
            print(f"  成功率: {success_rate:.1f}%")
        
        print("=" * 50)
    
    def _export_queue_report(self, queue_manager):
        """导出队列报告"""
        try:
            import json
            from datetime import datetime
            
            # 生成报告数据
            report_data = {
                'export_time': datetime.now().isoformat(),
                'queue_status': queue_manager.get_queue_status(),
                'tasks': []
            }
            
            # 添加任务详情
            for task in queue_manager.get_all_tasks():
                task_data = task.to_dict()
                report_data['tasks'].append(task_data)
            
            # 保存报告
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            report_file = f"queue_report_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            print(f"📄 队列报告已导出: {report_file}")
            
        except Exception as e:
            print(f"❌ 导出报告失败: {e}")
    
    # 队列回调函数
    def _on_queue_task_start(self, task):
        """任务开始回调（简化输出）"""
        # 根据配置决定显示模式
        mode = "compact" if self.queue_display_config.get('compact_on_start', True) else self.queue_display_config.get('default_mode', 'standard')
        self.status_display.display_status(self.queue_manager, mode=mode)
    
    def _on_queue_task_complete(self, task):
        """任务完成回调（优化输出）"""
        duration = task.actual_duration if task.actual_duration > 0 else 0
        print(f"✅ {task.name} 完成 ({duration:.1f}s)")
        # 显示简洁状态更新
        self.status_display.display_status(self.queue_manager, mode="compact")
    
    def _on_queue_task_failed(self, task, error_message: str):
        """任务失败回调（优化输出）"""
        print(f"❌ {task.name} 失败: {error_message}")
        # 显示简洁状态更新
        self.status_display.display_status(self.queue_manager, mode="compact")
        
        # 使用错误处理器处理错误
        try:
            from error_handler import handle_error
            handle_error(Exception(error_message), f"制种任务失败: {task.name}")
        except ImportError:
            pass  # 错误处理器不可用
    
    def _on_queue_progress_update(self, task):
        """进度更新回调"""
        # 这里可以实现更复杂的进度显示逻辑
        # 为了避免输出过多，这里暂时不输出进度信息
        pass
    
    def _show_queue_management_interface(self, queue_manager=None, task_ids=None):
        """显示队列管理界面入口"""
        # 使用传入的队列管理器或默认的队列管理器
        if queue_manager is None:
            queue_manager = self.queue_manager
        
        # 检查队列管理器是否可用
        if queue_manager is None:
            print("❌ 队列管理功能不可用，初始化时出现错误")
            input("\n按回车键继续...")
            return
        
        print("\n" + "=" * 60)
        print("           🔄 队列管理")
        print("=" * 60)
        
        # 显示队列状态
        self._display_queue_status(mode="standard")
        
        print("\n🔧 队列管理选项:")
        print("1. 📋 查看队列详情")
        print("2. ⚡ 启动队列")
        print("3. ⏸️ 暂停队列")
        print("4. ⏹️ 停止队列")
        print("5. 🗑️ 清理已完成任务")
        print("6. 📊 查看详细统计")
        print("7. 💾 导出队列报告")
        print("8. ➕ 添加制种任务")
        print("9. ➖ 删除任务")
        print("0. 🔙 返回主菜单")
        print("=" * 60)
        
        choice = input("请选择操作 (0-9): ").strip()
        
        try:
            if choice == '0':
                return
            elif choice == '1':
                self._show_queue_details()
            elif choice == '2':
                queue_manager.start_queue()
                # 使用统一状态显示接口，避免重复信息
                self.status_display.display_status(queue_manager, mode="standard", force_update=True)
            elif choice == '3':
                queue_manager.pause_queue()
                print("⏸️ 队列已暂停")
            elif choice == '4':
                queue_manager.stop_queue()
                print("⏹️ 队列已停止")
            elif choice == '5':
                count = queue_manager.clear_completed_tasks()
                print(f"🗑️ 已清理 {count} 个已完成任务")
            elif choice == '6':
                self._show_detailed_statistics(queue_manager)
            elif choice == '7':
                self._export_queue_report(queue_manager)
            elif choice == '8':
                self._add_queue_task_interactive(queue_manager)
            elif choice == '9':
                self._remove_queue_task_interactive(queue_manager)
            else:
                print("❌ 无效选择")
        
        except Exception as e:
            print(f"❌ 队列管理出错: {e}")
        
        if choice != '0':
            input("\n按回车键继续...")
    
    def _show_queue_details(self):
        """显示队列详情"""
        if self.queue_manager is None:
            print("❌ 队列管理器不可用")
            return
        
        print("\n" + "=" * 60)
        print("           📋 队列详情")
        print("=" * 60)
        
        # 获取所有任务
        all_tasks = self.queue_manager.get_all_tasks()
        
        if not all_tasks:
            print("\n📭 队列为空")
            return
        
        # 按状态分组显示
        # TaskStatus 已在文件中定义
        
        status_groups = {
            TaskStatus.WAITING: "⏳ 等待中",
            TaskStatus.RUNNING: "🔄 运行中",
            TaskStatus.COMPLETED: "✅ 已完成",
            TaskStatus.FAILED: "❌ 失败",
            TaskStatus.CANCELLED: "🚫 已取消"
        }
        
        for status, status_name in status_groups.items():
            tasks = [task for task in all_tasks if task.status == status]
            if tasks:
                print(f"\n{status_name} ({len(tasks)} 个任务):")
                for i, task in enumerate(tasks[:10], 1):  # 最多显示10个
                    print(f"  {i}. {task.name}")
                    if hasattr(task, 'progress') and task.progress > 0:
                        print(f"     进度: {task.progress:.1f}%")
                if len(tasks) > 10:
                    print(f"     ... 还有 {len(tasks) - 10} 个任务")
        
        # 显示队列统计
        status = self.queue_manager.get_queue_status()
        stats = status['statistics']
        print(f"\n📊 队列统计:")
        print(f"  总任务数: {status['total_tasks']}")
        print(f"  已完成: {stats['completed_tasks']}")
        print(f"  失败: {stats['failed_tasks']}")
        print(f"  成功率: {stats['success_rate']:.1f}%")
        if stats['average_processing_time'] > 0:
            print(f"  平均处理时间: {stats['average_processing_time']:.1f}秒")
    
    def _preset_management(self):
        """预设模式管理界面"""
        while True:
            print("\n" + "=" * 50)
            print("           ⚡ 预设模式管理")
            print("=" * 50)
            
            # 显示当前可用预设
            presets = self.config_manager.get_available_presets()
            if presets:
                print("\n📋 可用预设模式:")
                self.config_manager.display_presets_menu()
            else:
                print("\n❌ 无可用预设模式")
            
            print("\n🔧 管理选项:")
            print("1. 📖 查看预设详情")
            print("2. ⚡ 应用预设")
            print("3. 💾 保存当前配置为预设")
            print("4. 🗑️ 删除自定义预设")
            print("5. 🔍 自动检测推荐预设")
            print("0. 🔙 返回配置管理")
            print("=" * 50)
            
            choice = input("请选择操作 (0-5): ").strip()
            
            try:
                if choice == '0':
                    break
                elif choice == '1':
                    self._view_preset_details()
                elif choice == '2':
                    self._apply_preset_interactive()
                elif choice == '3':
                    self._save_custom_preset()
                elif choice == '4':
                    self._delete_custom_preset()
                elif choice == '5':
                    self._auto_detect_preset()
                else:
                    print("❌ 无效选择，请输入 0-5 之间的数字")
            
            except Exception as e:
                print(f"❌ 操作过程中发生错误: {e}")
                print("请重试或联系技术支持")
            
            if choice != '0':
                input("\n按回车键继续...")
    
    def _view_preset_details(self):
        """查看预设详情"""
        presets = self.config_manager.get_available_presets()
        if not presets:
            print("\n❌ 无可用预设模式")
            return
        
        print("\n请选择要查看的预设:")
        for i, preset_name in enumerate(presets, 1):
            print(f"{i}. {preset_name}")
        
        try:
            choice = int(input("\n请输入预设编号: ").strip())
            if 1 <= choice <= len(presets):
                preset_name = presets[choice - 1]
                preset_info = self.config_manager.get_preset_info(preset_name)
                
                if preset_info:
                    print(f"\n📋 预设详情: {preset_name}")
                    print("=" * 40)
                    print(f"描述: {preset_info.get('description', '无描述')}")
                    print(f"类型: {'系统预设' if preset_info.get('is_system', True) else '自定义预设'}")
                    print(f"推荐场景: {preset_info.get('recommended_for', '通用')}")
                    
                    print("\n⚙️ 配置参数:")
                    settings = preset_info.get('settings', {})
                    for key, value in settings.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"❌ 无法获取预设 '{preset_name}' 的详情")
            else:
                print("❌ 无效的预设编号")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    def _apply_preset_interactive(self):
        """交互式应用预设"""
        presets = self.config_manager.get_available_presets()
        if not presets:
            print("\n❌ 无可用预设模式")
            return
        
        print("\n请选择要应用的预设:")
        for i, preset_name in enumerate(presets, 1):
            preset_info = self.config_manager.get_preset_info(preset_name)
            description = preset_info.get('description', '无描述') if preset_info else '无描述'
            print(f"{i}. {preset_name} - {description}")
        
        try:
            choice = int(input("\n请输入预设编号: ").strip())
            if 1 <= choice <= len(presets):
                preset_name = presets[choice - 1]
                
                # 确认应用
                confirm = input(f"\n确认应用预设 '{preset_name}'? (y/N): ").strip().lower()
                if confirm in ['y', 'yes', '是']:
                    if self.config_manager.apply_preset(preset_name):
                        print(f"✅ 预设 '{preset_name}' 应用成功")
                        print("💡 提示: 新配置将在下次制种时生效")
                    else:
                        print(f"❌ 预设 '{preset_name}' 应用失败")
                else:
                    print("❌ 操作已取消")
            else:
                print("❌ 无效的预设编号")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    def _save_custom_preset(self):
        """保存自定义预设"""
        print("\n💾 保存当前配置为自定义预设")
        print("=" * 40)
        
        preset_name = input("请输入预设名称: ").strip()
        if not preset_name:
            print("❌ 预设名称不能为空")
            return
        
        # 检查是否已存在
        existing_presets = self.config_manager.get_available_presets()
        if preset_name in existing_presets:
            confirm = input(f"预设 '{preset_name}' 已存在，是否覆盖? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes', '是']:
                print("❌ 操作已取消")
                return
        
        description = input("请输入预设描述 (可选): ").strip()
        recommended_for = input("请输入推荐使用场景 (可选): ").strip()
        
        if self.config_manager.save_custom_preset(preset_name, description, recommended_for):
            print(f"✅ 自定义预设 '{preset_name}' 保存成功")
        else:
            print(f"❌ 自定义预设 '{preset_name}' 保存失败")
    
    def _delete_custom_preset(self):
        """删除自定义预设"""
        presets = self.config_manager.get_available_presets()
        custom_presets = []
        
        # 筛选出自定义预设
        for preset_name in presets:
            preset_info = self.config_manager.get_preset_info(preset_name)
            if preset_info and not preset_info.get('is_system', True):
                custom_presets.append(preset_name)
        
        if not custom_presets:
            print("\n❌ 无自定义预设可删除")
            return
        
        print("\n🗑️ 可删除的自定义预设:")
        for i, preset_name in enumerate(custom_presets, 1):
            preset_info = self.config_manager.get_preset_info(preset_name)
            description = preset_info.get('description', '无描述') if preset_info else '无描述'
            print(f"{i}. {preset_name} - {description}")
        
        try:
            choice = int(input("\n请输入要删除的预设编号: ").strip())
            if 1 <= choice <= len(custom_presets):
                preset_name = custom_presets[choice - 1]
                
                # 确认删除
                confirm = input(f"\n确认删除预设 '{preset_name}'? (y/N): ").strip().lower()
                if confirm in ['y', 'yes', '是']:
                    if self.config_manager.delete_custom_preset(preset_name):
                        print(f"✅ 自定义预设 '{preset_name}' 删除成功")
                    else:
                        print(f"❌ 自定义预设 '{preset_name}' 删除失败")
                else:
                    print("❌ 操作已取消")
            else:
                print("❌ 无效的预设编号")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    def _auto_detect_preset(self):
        """自动检测推荐预设"""
        print("\n🔍 自动检测推荐预设")
        print("=" * 40)
        
        # 获取资源文件夹
        resource_folder = self.config_manager.get_resource_folder()
        if not resource_folder or not os.path.exists(resource_folder):
            print("❌ 请先设置有效的资源文件夹")
            return
        
        try:
            # 计算文件夹总大小
            total_size = 0
            file_count = 0
            
            print("正在分析资源文件夹...")
            for root, dirs, files in os.walk(resource_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                        file_count += 1
                    except (OSError, IOError):
                        continue
            
            if total_size == 0:
                print("❌ 资源文件夹为空或无法访问")
                return
            
            # 转换为可读格式
            size_gb = total_size / (1024 ** 3)
            
            print(f"📊 分析结果:")
            print(f"  文件总数: {file_count:,}")
            print(f"  总大小: {size_gb:.2f} GB")
            
            # 自动检测推荐预设
            recommended_preset = self.config_manager.auto_detect_preset(total_size)
            
            if recommended_preset:
                preset_info = self.config_manager.get_preset_info(recommended_preset)
                description = preset_info.get('description', '无描述') if preset_info else '无描述'
                
                print(f"\n💡 推荐预设: {recommended_preset}")
                print(f"   描述: {description}")
                
                # 询问是否应用
                confirm = input(f"\n是否应用推荐预设 '{recommended_preset}'? (y/N): ").strip().lower()
                if confirm in ['y', 'yes', '是']:
                    if self.config_manager.apply_preset(recommended_preset):
                        print(f"✅ 预设 '{recommended_preset}' 应用成功")
                    else:
                        print(f"❌ 预设 '{recommended_preset}' 应用失败")
                else:
                    print("❌ 操作已取消")
            else:
                print("\n❌ 无法确定推荐预设，建议手动选择")
        
        except Exception as e:
            print(f"❌ 分析过程中发生错误: {e}")

    def config_management(self):
        """配置管理"""
        while True:
            print("\n" + "=" * 50)
            print("           ⚙️ 配置管理")
            print("=" * 50)
            print("1. 📁 查看当前配置")
            print("2. 🔧 设置资源文件夹")
            print("3. 📂 设置输出文件夹")
            print("4. 🌐 管理 Tracker")
            print("5. 🔄 重新加载配置")
            print("6. 📤 导出配置")
            print("7. 📥 导入配置")
            print("8. 🧹 清理缓存")
            print("9. 🔄 重置为默认配置")
            print("10. ⚡ 预设模式管理")
            print("0. 🔙 返回主菜单")
            print("=" * 50)

            choice = input("请选择操作 (0-10): ").strip()

            try:
                if choice == '0':
                    break
                elif choice == '1':
                    self._show_current_config()
                elif choice == '2':
                    self._set_resource_folder()
                elif choice == '3':
                    self._set_output_folder()
                elif choice == '4':
                    self._manage_trackers()
                elif choice == '5':
                    self._reload_config()
                elif choice == '6':
                    self._export_config()
                elif choice == '7':
                    self._import_config()
                elif choice == '8':
                    self._clear_cache()
                elif choice == '9':
                    self._reset_config()
                elif choice == '10':
                    self._preset_management()
                else:
                    print("❌ 无效选择，请输入 0-10 之间的数字")

            except Exception as e:
                print(f"❌ 操作过程中发生错误: {e}")
                print("请重试或联系技术支持")

            if choice != '0':
                input("\n按回车键继续...")

    def _show_current_config(self):
        """显示当前配置"""
        print("\n" + "=" * 60)
        print("           📋 当前配置信息")
        print("=" * 60)

        # 基本路径配置
        resource_folder = self.config.get_resource_folder()
        output_folder = self.config.get_output_folder()

        print(f"📁 资源文件夹: {resource_folder}")
        print(f"   {'✅ 存在' if os.path.exists(resource_folder) else '❌ 不存在'}")

        print(f"📂 输出文件夹: {output_folder}")
        print(f"   {'✅ 存在' if os.path.exists(output_folder) else '⚠️ 将自动创建'}")

        # Tracker 配置
        trackers = self.config.get_trackers()
        print(f"🌐 Tracker 配置: {len(trackers)} 个")
        if trackers:
            print("   前3个 Tracker:")
            for i, tracker in enumerate(trackers[:3], 1):
                print(f"   {i}. {tracker}")
            if len(trackers) > 3:
                print(f"   ... 还有 {len(trackers) - 3} 个")
        else:
            print("   ❌ 未配置任何 Tracker")

        # 高级配置
        print("\n🔧 高级配置:")
        try:
            if hasattr(self.config, 'get_setting'):
                tolerance = self.config.get_setting('file_search_tolerance', 60)
                max_results = self.config.get_setting('max_search_results', 10)
                cache_enabled = self.config.get_setting('enable_cache', True)
                max_concurrent = self.config.get_setting('max_concurrent_operations', 4)
            else:
                # 如果 get_setting 方法不存在，直接从 settings 字典获取
                tolerance = self.config.settings.get('file_search_tolerance', 60)
                max_results = self.config.settings.get('max_search_results', 10)
                cache_enabled = self.config.settings.get('enable_cache', True)
                max_concurrent = self.config.settings.get('max_concurrent_operations', 4)

            print(f"   🔍 搜索容错率: {tolerance}%")
            print(f"   📊 最大搜索结果: {max_results}")
            print(f"   💾 缓存状态: {'启用' if cache_enabled else '禁用'}")
            print(f"   ⚡ 最大并发操作: {max_concurrent}")

        except Exception as e:
            print(f"   ⚠️ 获取详细配置信息时出错: {e}")
            print("   基本配置信息已显示")

        # 配置文件状态
        print("\n📄 配置文件状态:")
        if hasattr(self.config, 'settings_path'):
            settings_path = self.config.settings_path
            trackers_path = self.config.trackers_path
            print(f"   ⚙️ 设置文件: {settings_path}")
            print(f"      {'✅ 存在' if os.path.exists(settings_path) else '❌ 不存在'}")
            print(f"   🌐 Tracker文件: {trackers_path}")
            print(f"      {'✅ 存在' if os.path.exists(trackers_path) else '❌ 不存在'}")
        else:
            print("   📁 配置目录: ~/.torrent_maker/")

        print("=" * 60)

    def _set_resource_folder(self):
        """设置资源文件夹"""
        print(f"\n📁 当前资源文件夹: {self.config.get_resource_folder()}")
        new_path = input("请输入新的资源文件夹路径 (回车取消): ").strip()
        if new_path:
            if self.config.set_resource_folder(new_path):
                print("✅ 资源文件夹设置成功")
                # 重新初始化文件匹配器
                enable_cache = True
                cache_duration = 3600
                max_workers = 4

                if hasattr(self.config, 'get_setting'):
                    enable_cache = self.config.get_setting('enable_cache', True)
                    cache_duration = self.config.get_setting('cache_duration', 3600)
                    max_workers = self.config.get_setting('max_concurrent_operations', 4)
                elif hasattr(self.config, 'settings'):
                    enable_cache = self.config.settings.get('enable_cache', True)
                    cache_duration = self.config.settings.get('cache_duration', 3600)
                    max_workers = self.config.settings.get('max_concurrent_operations', 4)

                # 使用新设置的路径直接创建 FileMatcher
                new_resource_folder = self.config.settings['resource_folder']
                self.matcher = FileMatcher(
                    new_resource_folder,
                    enable_cache=enable_cache,
                    cache_duration=cache_duration,
                    max_workers=max_workers
                )
                print(f"🔄 文件匹配器已重新初始化，使用路径: {new_resource_folder}")
            else:
                print("❌ 设置失败，请检查路径是否存在")

    def _set_output_folder(self):
        """设置输出文件夹"""
        print(f"\n📂 当前输出文件夹: {self.config.get_output_folder()}")
        new_path = input("请输入新的输出文件夹路径 (回车取消): ").strip()
        if new_path:
            if self.config.set_output_folder(new_path):
                print("✅ 输出文件夹设置成功")
                # 重新初始化种子创建器
                self.creator = TorrentCreator(
                    self.config.get_trackers(),
                    self.config.get_output_folder()
                )
            else:
                print("❌ 设置失败")

    def _manage_trackers(self):
        """管理 Tracker"""
        while True:
            print("\n🌐 Tracker 管理")
            print("=" * 30)
            trackers = self.config.get_trackers()
            if trackers:
                for i, tracker in enumerate(trackers, 1):
                    print(f"  {i:2d}. {tracker}")
            else:
                print("  (无 Tracker)")

            print("\n操作选项:")
            print("1. ➕ 添加 Tracker")
            print("2. ➖ 删除 Tracker")
            print("0. 🔙 返回")

            choice = input("\n请选择操作 (0-2): ").strip()

            if choice == '0':
                break
            elif choice == '1':
                tracker_url = input("请输入 Tracker URL: ").strip()
                if tracker_url:
                    if self.config.add_tracker(tracker_url):
                        print("✅ Tracker 添加成功")
                        # 更新种子创建器的 tracker 列表
                        self.creator = TorrentCreator(
                            self.config.get_trackers(),
                            self.config.get_output_folder()
                        )
                    else:
                        print("❌ 添加失败，可能是无效URL或已存在")
            elif choice == '2':
                if not trackers:
                    print("❌ 没有可删除的 Tracker")
                    continue
                try:
                    idx = int(input("请输入要删除的 Tracker 编号: ").strip())
                    if 1 <= idx <= len(trackers):
                        tracker_to_remove = trackers[idx - 1]
                        if self.config.remove_tracker(tracker_to_remove):
                            print("✅ Tracker 删除成功")
                            # 更新种子创建器的 tracker 列表
                            self.creator = TorrentCreator(
                                self.config.get_trackers(),
                                self.config.get_output_folder()
                            )
                        else:
                            print("❌ 删除失败")
                    else:
                        print("❌ 无效的编号")
                except ValueError:
                    print("❌ 请输入有效的数字")
            else:
                print("❌ 无效选择")

    def _reload_config(self):
        """重新加载配置"""
        try:
            # 重新初始化配置管理器
            self.config = ConfigManager()

            # 重新初始化其他组件
            enable_cache = True
            if hasattr(self.config, 'get_setting'):
                enable_cache = self.config.get_setting('enable_cache', True)
            elif hasattr(self.config, 'settings'):
                enable_cache = self.config.settings.get('enable_cache', True)

            self.matcher = FileMatcher(
                self.config.get_resource_folder(),
                enable_cache=enable_cache
            )

            self.creator = TorrentCreator(
                self.config.get_trackers(),
                self.config.get_output_folder()
            )

            print("✅ 配置重新加载成功")
        except Exception as e:
            print(f"❌ 重新加载配置失败: {e}")

    def _export_config(self):
        """导出配置"""
        print("\n📤 导出配置")
        print("=" * 30)

        default_path = f"torrent_maker_config_{time.strftime('%Y%m%d_%H%M%S')}.json"
        export_path = input(f"请输入导出文件路径 (回车使用默认: {default_path}): ").strip()

        if not export_path:
            export_path = default_path

        try:
            if hasattr(self.config, 'export_config'):
                if self.config.export_config(export_path):
                    print(f"✅ 配置已导出到: {export_path}")
                else:
                    print("❌ 导出失败")
            else:
                # 手动导出配置
                export_data = {
                    'settings': self.config.settings,
                    'trackers': self.config.get_trackers(),
                    'export_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'version': VERSION
                }

                with open(export_path, 'w', encoding='utf-8') as f:
                    import json
                    json.dump(export_data, f, ensure_ascii=False, indent=4)

                print(f"✅ 配置已导出到: {export_path}")

        except Exception as e:
            print(f"❌ 导出配置失败: {e}")

    def _import_config(self):
        """导入配置"""
        print("\n📥 导入配置")
        print("=" * 30)
        print("⚠️ 警告：导入配置将覆盖当前所有设置")

        import_path = input("请输入配置文件路径: ").strip()
        if not import_path:
            print("❌ 路径不能为空")
            return

        if not os.path.exists(import_path):
            print(f"❌ 文件不存在: {import_path}")
            return

        confirm = input("确认导入配置？这将覆盖当前设置 (y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("❌ 已取消导入")
            return

        try:
            if hasattr(self.config, 'import_config'):
                if self.config.import_config(import_path):
                    print("✅ 配置导入成功")
                    self._reload_config()  # 重新加载配置
                else:
                    print("❌ 导入失败")
            else:
                # 手动导入配置
                with open(import_path, 'r', encoding='utf-8') as f:
                    import json
                    import_data = json.load(f)

                if 'settings' in import_data:
                    self.config.settings.update(import_data['settings'])
                    self.config.save_settings()

                if 'trackers' in import_data:
                    self.config.trackers = import_data['trackers']
                    self.config.save_trackers()

                print("✅ 配置导入成功")
                self._reload_config()  # 重新加载配置

        except Exception as e:
            print(f"❌ 导入配置失败: {e}")

    def _clear_cache(self):
        """清理缓存"""
        print("\n🧹 清理缓存")
        print("=" * 40)

        try:
            cleared_items = 0

            # 清理搜索缓存
            if hasattr(self.matcher, 'cache') and self.matcher.cache:
                cache_stats = self.matcher.cache.get_stats()
                if cache_stats:
                    cleared_items += cache_stats.get('total_items', 0)
                self.matcher.cache._cache.clear()
                print("✅ 搜索缓存已清理")

            # 清理文件夹信息缓存
            if hasattr(self.matcher, 'folder_info_cache') and self.matcher.folder_info_cache:
                cache_stats = self.matcher.folder_info_cache.get_stats()
                if cache_stats:
                    cleared_items += cache_stats.get('total_items', 0)
                self.matcher.folder_info_cache._cache.clear()
                print("✅ 文件夹信息缓存已清理")

            # 清理大小缓存
            if hasattr(self.matcher, 'size_cache') and self.matcher.size_cache:
                if hasattr(self.matcher.size_cache, '_cache'):
                    self.matcher.size_cache._cache.clear()
                    print("✅ 大小缓存已清理")

            # 清理智能索引缓存
            if hasattr(self.matcher, 'smart_index') and self.matcher.smart_index:
                if hasattr(self.matcher.smart_index, '_word_index'):
                    self.matcher.smart_index._word_index.clear()
                    print("✅ 智能索引缓存已清理")

            print(f"✅ 缓存清理完成，共清理 {cleared_items} 个缓存项")
            print("💡 建议: 清理缓存后首次搜索可能会稍慢，但可以解决编码问题")

        except Exception as e:
            print(f"❌ 清理缓存失败: {e}")

    def _reset_config(self):
        """重置配置为默认值"""
        print("\n🔄 重置配置")
        print("=" * 30)
        print("⚠️ 警告：这将重置所有配置为默认值")
        print("包括：资源文件夹、输出文件夹、Tracker列表等")

        confirm = input("确认重置所有配置为默认值？(y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("❌ 已取消重置")
            return

        try:
            if hasattr(self.config, 'reset_to_defaults'):
                if self.config.reset_to_defaults():
                    print("✅ 配置已重置为默认值")
                    self._reload_config()  # 重新加载配置
                else:
                    print("❌ 重置失败")
            else:
                # 手动重置配置
                self.config.settings = self.config.DEFAULT_SETTINGS.copy()
                self.config.trackers = self.config.DEFAULT_TRACKERS.copy()

                # 展开用户目录路径
                self.config.settings['resource_folder'] = os.path.expanduser(
                    self.config.settings['resource_folder']
                )
                self.config.settings['output_folder'] = os.path.expanduser(
                    self.config.settings['output_folder']
                )

                self.config.save_settings()
                self.config.save_trackers()

                print("✅ 配置已重置为默认值")
                self._reload_config()  # 重新加载配置

        except Exception as e:
            print(f"❌ 重置配置失败: {e}")

    def run(self):
        """运行主程序"""
        self.display_header()

        while True:
            try:
                self.display_menu()
                max_choice = 8 if ENHANCED_FEATURES_AVAILABLE else 7
                choice = input(f"请选择操作 (0-{max_choice}): ").strip()

                if choice == '0':
                    print(f"👋 感谢使用 {FULL_VERSION_INFO}！")
                    break
                elif choice == '1':
                    self.search_and_create()
                elif choice == '2':
                    self.quick_create()
                elif choice == '3':
                    self.batch_create()
                elif choice == '4':
                    self.config_management()
                elif choice == '5':
                    self.show_performance_stats()
                elif choice == '6':
                    self._show_queue_management_interface()
                elif choice == '7':
                    if ENHANCED_FEATURES_AVAILABLE:
                        self.search_history_management()
                    else:
                        self.show_help()
                elif choice == '8' and ENHANCED_FEATURES_AVAILABLE:
                    self.show_help()
                else:
                    print("❌ 无效选择，请重新输入")

                print()

            except KeyboardInterrupt:
                print("\n\n👋 程序已退出")
                break
            except Exception as e:
                print(f"❌ 程序运行时发生错误: {e}")
    
    def search_history_management(self):
        """搜索历史管理"""
        if not self.search_history:
            print("❌ 搜索历史功能不可用")
            return
            
        while True:
            print("\n📝 搜索历史管理")
            print("=" * 60)
            print("  1. 📋 查看搜索历史")
            print("  2. 🔥 查看热门搜索")
            print("  3. 📊 查看搜索统计")
            print("  4. 🗑️  清理搜索历史")
            print("  5. 📤 导出搜索历史")
            print("  0. 🔙 返回主菜单")
            print()
            
            choice = input("请选择操作 (0-5): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._show_search_history()
            elif choice == '2':
                self._show_popular_searches()
            elif choice == '3':
                self._show_search_statistics()
            elif choice == '4':
                self._clear_search_history()
            elif choice == '5':
                self._export_search_history()
            else:
                print("❌ 无效选择，请重新输入")
    
    def _show_search_history(self):
        """显示搜索历史"""
        # 尝试获取详细搜索记录，如果失败则使用简单查询列表
        try:
            recent_searches = self.search_history.get_recent_searches(20)
        except AttributeError:
            # 如果没有 get_recent_searches 方法，使用 get_recent_queries
            recent_queries = self.search_history.get_recent_queries(20)
            if not recent_queries:
                print("\n📝 暂无搜索历史")
                return
            print("\n📋 最近搜索历史:")
            for i, query in enumerate(recent_queries, 1):
                print(f"  {i}. {query}")
            return
            
        if not recent_searches:
            print("\n📝 暂无搜索历史")
            return
            
        print("\n📋 最近搜索历史:")
        print("-" * 80)
        print(f"{'序号':<4} {'搜索内容':<30} {'结果数':<8} {'搜索时间':<12} {'耗时':<8}")
        print("-" * 80)
        
        for i, search in enumerate(recent_searches, 1):
            # 兼容不同的数据结构
            if isinstance(search, dict):
                query = search.get('query', 'N/A')
                result_count = search.get('result_count', 0)
                timestamp = search.get('timestamp', 'N/A')
                duration = search.get('duration', 'N/A')
                if isinstance(timestamp, str):
                    timestamp_str = timestamp[:16] if len(timestamp) > 16 else timestamp
                else:
                    timestamp_str = timestamp.strftime('%m-%d %H:%M') if hasattr(timestamp, 'strftime') else 'N/A'
                duration_str = f"{duration:.3f}s" if isinstance(duration, (int, float)) else "N/A"
            elif hasattr(search, 'query'):
                query = search.query
                result_count = getattr(search, 'result_count', 0)
                timestamp_str = search.timestamp.strftime('%m-%d %H:%M') if hasattr(search, 'timestamp') else 'N/A'
                duration_str = f"{search.duration:.3f}s" if hasattr(search, 'duration') and search.duration else "N/A"
            else:
                query = str(search)
                result_count = 0
                timestamp_str = 'N/A'
                duration_str = 'N/A'
                
            print(f"{i:<4} {query[:28]:<30} {result_count:<8} {timestamp_str:<12} {duration_str:<8}")
    
    def _show_popular_searches(self):
        """显示热门搜索"""
        popular_searches = self.search_history.get_popular_queries(10)
        if not popular_searches:
            print("\n🔥 暂无热门搜索")
            return
            
        print("\n🔥 热门搜索 (按搜索次数排序):")
        print("-" * 50)
        print(f"{'排名':<4} {'搜索内容':<30} {'搜索次数':<8}")
        print("-" * 50)
        
        for i, (query, count) in enumerate(popular_searches, 1):
            print(f"{i:<4} {query[:28]:<30} {count:<8}")
    
    def _show_search_statistics(self):
        """显示搜索统计"""
        stats = self.search_history.get_statistics()
        if not stats:
            print("\n📊 暂无搜索统计")
            return
            
        print("\n📊 搜索统计信息:")
        print("-" * 40)
        print(f"总搜索次数: {stats['total_searches']}")
        print(f"成功搜索次数: {stats['successful_searches']}")
        print(f"成功率: {stats['success_rate']:.1f}%")
        print(f"平均搜索耗时: {stats['average_duration']:.3f}s")
        print(f"平均结果数: {stats['average_results']:.1f}")
        print(f"最早搜索: {stats['earliest_search'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"最近搜索: {stats['latest_search'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _clear_search_history(self):
        """清理搜索历史"""
        confirm = input("\n⚠️ 确认清理所有搜索历史？(y/N): ").strip().lower()
        if confirm in ['y', 'yes', '是']:
            self.search_history.clear_history()
            print("✅ 搜索历史已清理")
        else:
            print("❌ 操作已取消")
    
    def _export_search_history(self):
        """导出搜索历史"""
        try:
            filename = f"search_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(os.getcwd(), filename)
            self.search_history.export_history(filepath)
            print(f"✅ 搜索历史已导出到: {filepath}")
        except Exception as e:
            print(f"❌ 导出失败: {e}")

    def show_performance_stats(self):
        """显示性能统计信息"""
        print("\n📊 性能统计信息")
        print("=" * 60)

        # 获取文件匹配器的性能统计
        if hasattr(self.matcher, 'performance_monitor'):
            matcher_stats = self.matcher.performance_monitor.get_all_stats()
            if matcher_stats:
                print("🔍 搜索性能:")
                for name, stats in matcher_stats.items():
                    if stats:
                        print(f"  {name}:")
                        print(f"    执行次数: {stats['count']}")
                        print(f"    平均耗时: {stats['average']:.3f}s")
                        print(f"    最大耗时: {stats['max']:.3f}s")
                        print(f"    总耗时: {stats['total']:.3f}s")
                print()

        # 获取种子创建器的性能统计
        if hasattr(self.creator, 'performance_monitor'):
            creator_stats = self.creator.performance_monitor.get_all_stats()
            if creator_stats:
                print("🛠️ 种子创建性能:")
                for name, stats in creator_stats.items():
                    if stats:
                        print(f"  {name}:")
                        print(f"    执行次数: {stats['count']}")
                        print(f"    平均耗时: {stats['average']:.3f}s")
                        print(f"    最大耗时: {stats['max']:.3f}s")
                        print(f"    总耗时: {stats['total']:.3f}s")
                print()

        # 获取缓存统计
        if hasattr(self.matcher, 'cache') and self.matcher.cache:
            cache_stats = self.matcher.cache.get_stats()
            if cache_stats:
                print("💾 缓存统计:")
                print(f"  总缓存项: {cache_stats['total_items']}")
                print(f"  有效缓存项: {cache_stats['valid_items']}")
                print(f"  过期缓存项: {cache_stats['expired_items']}")
                print()

        # 显示优化建议
        print("💡 性能优化建议:")
        suggestions = self._generate_performance_suggestions()
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        else:
            print("  当前性能表现良好，无需特别优化")

        print("=" * 60)

    def _generate_performance_suggestions(self) -> List[str]:
        """生成性能优化建议"""
        suggestions = []

        # 检查搜索性能
        if hasattr(self.matcher, 'performance_monitor'):
            search_stats = self.matcher.performance_monitor.get_stats('fuzzy_search')
            if search_stats and search_stats.get('average', 0) > 2.0:
                suggestions.append("搜索耗时较长，建议增加缓存时间或减少搜索深度")

        # 检查种子创建性能
        if hasattr(self.creator, 'performance_monitor'):
            creation_stats = self.creator.performance_monitor.get_stats('total_torrent_creation')
            if creation_stats and creation_stats.get('average', 0) > 30.0:
                suggestions.append("种子创建耗时较长，建议检查磁盘性能或减少文件数量")

        # 检查缓存使用情况
        if hasattr(self.matcher, 'cache') and self.matcher.cache:
            cache_stats = self.matcher.cache.get_stats()
            if cache_stats and cache_stats.get('valid_items', 0) == 0:
                suggestions.append("缓存未被有效利用，建议检查缓存配置")

        return suggestions

    def show_help(self):
        """显示帮助信息"""
        print("\n❓ 帮助信息")
        print("=" * 50)
        print("🔍 搜索功能:")
        print("  - 支持模糊搜索，容错率高")
        print("  - 自动识别剧集信息")
        print("  - 智能缓存，重复搜索更快")
        print()
        print("⚡ 快速制种:")
        print("  - 直接输入文件夹路径")
        print("  - 支持批量路径 (用分号分隔)")
        print()
        print("🎯 性能优化:")
        print("  - 多线程并行处理")
        print("  - 智能缓存系统")
        print("  - 内存使用优化")
        print("  - 实时性能监控")
        print("=" * 50)


def main():
    """主函数"""
    try:
        app = TorrentMakerApp()
        app.run()
    except Exception as e:
        print(f"❌ 程序启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
