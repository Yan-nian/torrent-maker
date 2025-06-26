#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Torrent Maker - 队列管理模块
任务队列、进度监控和批量控制系统
"""

import os
import time
import json
import uuid
import threading
from enum import Enum
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, PriorityQueue
import logging


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
        data['status'] = TaskStatus(data['status'])
        data['priority'] = TaskPriority(data['priority'])
        return cls(**data)


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
            
            # 从队列中移除
            del self.tasks[task_id]
            
            # 从运行任务中移除
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
            
            self.logger.info(f"任务已移除: {task.name} (ID: {task_id})")
            self._save_queue()
            return True
    
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
            
            # 执行制种
            success = self.torrent_creator.create_torrent(
                task.path,
                output_path,
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
        name = os.path.basename(file_path)
        return self.add_task(name, file_path, priority, preset, output_path)
    
    def batch_add_tasks(self, file_paths: List[str], preset: str = "standard",
                       priority: TaskPriority = TaskPriority.NORMAL) -> List[str]:
        """批量添加制种任务"""
        task_ids = []
        for file_path in file_paths:
            task_id = self.add_torrent_task(file_path, preset, priority)
            task_ids.append(task_id)
        
        self.logger.info(f"批量添加了 {len(task_ids)} 个制种任务")
        return task_ids