#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Progress Monitor Module - 制种进度监控模块
为 Torrent Maker 提供实时进度显示和监控功能

功能特性:
- 实时进度条显示
- 制种过程可视化
- 性能监控和统计
- 进度取消和暂停
- 多任务进度管理
"""

import os
import sys
import time
import threading
import subprocess
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ProgressInfo:
    """进度信息数据类"""
    task_id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0  # 0-100
    current_step: str = ""
    total_steps: int = 0
    completed_steps: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: str = ""
    file_path: str = ""
    file_size: int = 0
    processed_size: int = 0
    speed: float = 0.0  # MB/s
    eta: Optional[timedelta] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ProgressDisplay:
    """进度显示器"""
    
    def __init__(self, width: int = 50):
        self.width = width
        self.last_line_length = 0
    
    def draw_progress_bar(self, progress: float, prefix: str = "", suffix: str = "") -> str:
        """绘制进度条"""
        filled_length = int(self.width * progress / 100)
        bar = '█' * filled_length + '░' * (self.width - filled_length)
        return f"\r{prefix} |{bar}| {progress:6.2f}% {suffix}"
    
    def clear_line(self):
        """清除当前行"""
        print("\r" + " " * self.last_line_length, end="\r")
    
    def print_progress(self, progress_info: ProgressInfo, show_details: bool = True):
        """打印进度信息"""
        # 基本进度条
        prefix = f"📦 {progress_info.name[:20]:<20}"
        
        # 构建后缀信息
        suffix_parts = []
        
        if progress_info.speed > 0:
            if progress_info.speed >= 1:
                suffix_parts.append(f"{progress_info.speed:.1f} MB/s")
            else:
                suffix_parts.append(f"{progress_info.speed*1024:.1f} KB/s")
        
        if progress_info.eta:
            eta_str = str(progress_info.eta).split('.')[0]  # 移除微秒
            suffix_parts.append(f"ETA: {eta_str}")
        
        if progress_info.file_size > 0:
            size_mb = progress_info.file_size / (1024 * 1024)
            processed_mb = progress_info.processed_size / (1024 * 1024)
            suffix_parts.append(f"{processed_mb:.1f}/{size_mb:.1f} MB")
        
        suffix = " | ".join(suffix_parts)
        
        # 绘制进度条
        progress_line = self.draw_progress_bar(progress_info.progress, prefix, suffix)
        print(progress_line, end="")
        self.last_line_length = len(progress_line)
        
        # 显示详细信息
        if show_details and progress_info.current_step:
            print(f"\n   └─ {progress_info.current_step}")
        
        sys.stdout.flush()
    
    def print_status(self, progress_info: ProgressInfo):
        """打印状态信息"""
        status_icons = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.RUNNING: "🔄",
            TaskStatus.PAUSED: "⏸️",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.FAILED: "❌",
            TaskStatus.CANCELLED: "🚫"
        }
        
        icon = status_icons.get(progress_info.status, "❓")
        print(f"{icon} {progress_info.name} - {progress_info.status.value}")
        
        if progress_info.error_message:
            print(f"   ❌ 错误: {progress_info.error_message}")


class ProgressMonitor:
    """进度监控器"""
    
    def __init__(self):
        self.tasks: Dict[str, ProgressInfo] = {}
        self.display = ProgressDisplay()
        self.update_interval = 0.5  # 更新间隔(秒)
        self.running = False
        self.display_thread: Optional[threading.Thread] = None
        self.callbacks: Dict[str, List[Callable]] = {
            'on_start': [],
            'on_progress': [],
            'on_complete': [],
            'on_error': [],
            'on_cancel': []
        }
        self._lock = threading.Lock()
    
    def add_callback(self, event: str, callback: Callable):
        """添加回调函数"""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
    
    def _trigger_callbacks(self, event: str, progress_info: ProgressInfo):
        """触发回调函数"""
        for callback in self.callbacks.get(event, []):
            try:
                callback(progress_info)
            except Exception as e:
                print(f"⚠️ 回调函数执行失败: {e}")
    
    def create_task(self, task_id: str, name: str, file_path: str = "", 
                   total_steps: int = 0, file_size: int = 0) -> ProgressInfo:
        """创建新任务"""
        with self._lock:
            progress_info = ProgressInfo(
                task_id=task_id,
                name=name,
                file_path=file_path,
                total_steps=total_steps,
                file_size=file_size
            )
            self.tasks[task_id] = progress_info
            return progress_info
    
    def start_task(self, task_id: str) -> bool:
        """开始任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            progress_info = self.tasks[task_id]
            progress_info.status = TaskStatus.RUNNING
            progress_info.start_time = datetime.now()
            
            self._trigger_callbacks('on_start', progress_info)
            return True
    
    def update_progress(self, task_id: str, progress: float = None, 
                       current_step: str = None, completed_steps: int = None,
                       processed_size: int = None, **kwargs) -> bool:
        """更新任务进度"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            progress_info = self.tasks[task_id]
            
            if progress is not None:
                progress_info.progress = min(100.0, max(0.0, progress))
            
            if current_step is not None:
                progress_info.current_step = current_step
            
            if completed_steps is not None:
                progress_info.completed_steps = completed_steps
                if progress_info.total_steps > 0:
                    progress_info.progress = (completed_steps / progress_info.total_steps) * 100
            
            if processed_size is not None:
                progress_info.processed_size = processed_size
                if progress_info.file_size > 0:
                    progress_info.progress = (processed_size / progress_info.file_size) * 100
            
            # 更新其他属性
            for key, value in kwargs.items():
                if hasattr(progress_info, key):
                    setattr(progress_info, key, value)
            
            # 计算速度和ETA
            self._calculate_speed_and_eta(progress_info)
            
            self._trigger_callbacks('on_progress', progress_info)
            return True
    
    def _calculate_speed_and_eta(self, progress_info: ProgressInfo):
        """计算速度和预计完成时间"""
        if not progress_info.start_time or progress_info.processed_size == 0:
            return
        
        elapsed = datetime.now() - progress_info.start_time
        elapsed_seconds = elapsed.total_seconds()
        
        if elapsed_seconds > 0:
            # 计算速度 (MB/s)
            progress_info.speed = (progress_info.processed_size / (1024 * 1024)) / elapsed_seconds
            
            # 计算ETA
            if progress_info.progress > 0 and progress_info.progress < 100:
                remaining_progress = 100 - progress_info.progress
                eta_seconds = (elapsed_seconds / progress_info.progress) * remaining_progress
                progress_info.eta = timedelta(seconds=int(eta_seconds))
    
    def complete_task(self, task_id: str, success: bool = True, error_message: str = "") -> bool:
        """完成任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            progress_info = self.tasks[task_id]
            progress_info.end_time = datetime.now()
            progress_info.error_message = error_message
            
            if success:
                progress_info.status = TaskStatus.COMPLETED
                progress_info.progress = 100.0
                self._trigger_callbacks('on_complete', progress_info)
            else:
                progress_info.status = TaskStatus.FAILED
                self._trigger_callbacks('on_error', progress_info)
            
            return True
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            progress_info = self.tasks[task_id]
            progress_info.status = TaskStatus.CANCELLED
            progress_info.end_time = datetime.now()
            
            self._trigger_callbacks('on_cancel', progress_info)
            return True
    
    def pause_task(self, task_id: str) -> bool:
        """暂停任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            progress_info = self.tasks[task_id]
            if progress_info.status == TaskStatus.RUNNING:
                progress_info.status = TaskStatus.PAUSED
                return True
            return False
    
    def resume_task(self, task_id: str) -> bool:
        """恢复任务"""
        with self._lock:
            if task_id not in self.tasks:
                return False
            
            progress_info = self.tasks[task_id]
            if progress_info.status == TaskStatus.PAUSED:
                progress_info.status = TaskStatus.RUNNING
                return True
            return False
    
    def get_task(self, task_id: str) -> Optional[ProgressInfo]:
        """获取任务信息"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[ProgressInfo]:
        """获取所有任务"""
        return list(self.tasks.values())
    
    def get_running_tasks(self) -> List[ProgressInfo]:
        """获取运行中的任务"""
        return [task for task in self.tasks.values() if task.status == TaskStatus.RUNNING]
    
    def start_display(self, show_completed: bool = False):
        """开始显示进度"""
        if self.running:
            return
        
        self.running = True
        self.display_thread = threading.Thread(target=self._display_loop, args=(show_completed,))
        self.display_thread.daemon = True
        self.display_thread.start()
    
    def stop_display(self):
        """停止显示进度"""
        self.running = False
        if self.display_thread:
            self.display_thread.join(timeout=1.0)
    
    def _display_loop(self, show_completed: bool):
        """显示循环"""
        while self.running:
            try:
                with self._lock:
                    running_tasks = self.get_running_tasks()
                    
                    if running_tasks:
                        # 清屏并显示当前任务
                        os.system('clear' if os.name == 'posix' else 'cls')
                        print("🔄 制种进度监控")
                        print("=" * 60)
                        
                        for task in running_tasks:
                            self.display.print_progress(task, show_details=True)
                            print()  # 换行
                        
                        print("\n💡 按 Ctrl+C 取消当前任务")
                    
                    # 显示已完成的任务
                    if show_completed:
                        completed_tasks = [t for t in self.tasks.values() 
                                         if t.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]]
                        if completed_tasks:
                            print("\n📋 已完成的任务:")
                            for task in completed_tasks[-5:]:  # 只显示最近5个
                                self.display.print_status(task)
                
                time.sleep(self.update_interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"⚠️ 显示更新失败: {e}")
                time.sleep(1)
    
    def clear_completed_tasks(self):
        """清除已完成的任务"""
        with self._lock:
            self.tasks = {
                task_id: task for task_id, task in self.tasks.items()
                if task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            total_tasks = len(self.tasks)
            status_counts = {}
            
            for status in TaskStatus:
                status_counts[status.value] = sum(
                    1 for task in self.tasks.values() if task.status == status
                )
            
            # 计算平均完成时间
            completed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED and t.start_time and t.end_time]
            avg_duration = None
            if completed_tasks:
                total_duration = sum((t.end_time - t.start_time).total_seconds() for t in completed_tasks)
                avg_duration = total_duration / len(completed_tasks)
            
            return {
                'total_tasks': total_tasks,
                'status_counts': status_counts,
                'average_duration': avg_duration,
                'success_rate': status_counts.get('completed', 0) / max(1, total_tasks) * 100
            }


class TorrentProgressMonitor(ProgressMonitor):
    """专门用于Torrent制种的进度监控器"""
    
    def __init__(self):
        super().__init__()
        self.mktorrent_processes: Dict[str, subprocess.Popen] = {}
    
    def start_torrent_creation(self, task_id: str, name: str, file_path: str, 
                              output_path: str, mktorrent_cmd: List[str]) -> bool:
        """开始Torrent创建任务"""
        try:
            # 获取文件大小
            file_size = self._get_path_size(file_path)
            
            # 创建任务
            self.create_task(task_id, name, file_path, file_size=file_size)
            
            # 启动mktorrent进程
            process = subprocess.Popen(
                mktorrent_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.mktorrent_processes[task_id] = process
            self.start_task(task_id)
            
            # 启动监控线程
            monitor_thread = threading.Thread(
                target=self._monitor_mktorrent_process,
                args=(task_id, process, output_path)
            )
            monitor_thread.daemon = True
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            self.complete_task(task_id, success=False, error_message=str(e))
            return False
    
    def _get_path_size(self, path: str) -> int:
        """获取路径大小"""
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
        except Exception:
            pass
        return 0
    
    def _monitor_mktorrent_process(self, task_id: str, process: subprocess.Popen, output_path: str):
        """监控mktorrent进程"""
        try:
            start_time = time.time()
            last_update = start_time
            
            while process.poll() is None:
                current_time = time.time()
                
                # 每秒更新一次进度
                if current_time - last_update >= 1.0:
                    # 检查输出文件大小来估算进度
                    if os.path.exists(output_path):
                        output_size = os.path.getsize(output_path)
                        task = self.get_task(task_id)
                        if task and task.file_size > 0:
                            # 简单估算：输出文件大小通常是源文件的1-5%
                            estimated_progress = min(95.0, (output_size / (task.file_size * 0.02)) * 100)
                            self.update_progress(
                                task_id,
                                progress=estimated_progress,
                                current_step="正在计算哈希值...",
                                processed_size=int(task.file_size * estimated_progress / 100)
                            )
                    
                    last_update = current_time
                
                time.sleep(0.1)
            
            # 进程结束，检查结果
            return_code = process.returncode
            
            if return_code == 0:
                self.update_progress(task_id, progress=100.0, current_step="制种完成")
                self.complete_task(task_id, success=True)
            else:
                stderr_output = process.stderr.read() if process.stderr else ""
                self.complete_task(task_id, success=False, error_message=f"mktorrent失败 (退出码: {return_code}): {stderr_output}")
            
        except Exception as e:
            self.complete_task(task_id, success=False, error_message=f"监控进程失败: {e}")
        finally:
            # 清理进程引用
            if task_id in self.mktorrent_processes:
                del self.mktorrent_processes[task_id]
    
    def cancel_torrent_creation(self, task_id: str) -> bool:
        """取消Torrent创建"""
        try:
            # 终止mktorrent进程
            if task_id in self.mktorrent_processes:
                process = self.mktorrent_processes[task_id]
                process.terminate()
                
                # 等待进程结束
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                
                del self.mktorrent_processes[task_id]
            
            # 更新任务状态
            self.cancel_task(task_id)
            return True
            
        except Exception as e:
            print(f"⚠️ 取消任务失败: {e}")
            return False
    
    def cancel_all_tasks(self):
        """取消所有任务"""
        running_tasks = self.get_running_tasks()
        for task in running_tasks:
            self.cancel_torrent_creation(task.task_id)


def test_progress_monitor():
    """测试进度监控功能"""
    print("🧪 测试进度监控功能")
    
    monitor = TorrentProgressMonitor()
    monitor.start_display(show_completed=True)
    
    # 模拟任务
    task_id = "test_task_1"
    monitor.create_task(task_id, "测试制种任务", "/tmp/test", file_size=1024*1024*100)  # 100MB
    monitor.start_task(task_id)
    
    try:
        # 模拟进度更新
        for i in range(101):
            monitor.update_progress(
                task_id,
                progress=i,
                current_step=f"处理步骤 {i}/100",
                processed_size=1024*1024*i
            )
            time.sleep(0.1)
        
        monitor.complete_task(task_id, success=True)
        
    except KeyboardInterrupt:
        print("\n❌ 用户取消")
        monitor.cancel_task(task_id)
    
    finally:
        monitor.stop_display()
        
        # 显示统计信息
        stats = monitor.get_statistics()
        print(f"\n📊 统计信息: {stats}")


if __name__ == "__main__":
    test_progress_monitor()