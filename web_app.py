#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Torrent Maker Web Interface
v2.1.0 - Web界面版本

基于Flask + WebSocket的现代化Web界面
支持多服务器SSH连接和实时进度监控
"""

import os
import sys
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import paramiko
from celery import Celery
import redis
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 导入核心torrent_maker模块
try:
    from torrent_maker import TorrentMakerApp, TaskStatus, TaskPriority
except ImportError:
    # 如果无法导入，尝试从当前目录导入
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from torrent_maker import TorrentMakerApp, TaskStatus, TaskPriority

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask应用配置
app = Flask(
    __name__,
    template_folder='web/templates',
    static_folder='web/static'
)
app.config['SECRET_KEY'] = 'torrent-maker-web-secret-key-2024'
app.config['DEBUG'] = False

# SocketIO配置
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    logger=False,
    engineio_logger=False
)

# Redis配置
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# Celery配置
celery_app = Celery(
    'torrent_maker_web',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

class SSHServerManager:
    """SSH服务器连接管理器"""
    
    def __init__(self):
        self.connections: Dict[str, paramiko.SSHClient] = {}
        self.server_configs: Dict[str, Dict] = {}
        self.load_server_configs()
    
    def load_server_configs(self):
        """加载服务器配置"""
        config_file = Path('web/servers.yaml')
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                self.server_configs = yaml.safe_load(f) or {}
    
    def save_server_configs(self):
        """保存服务器配置"""
        config_file = Path('web/servers.yaml')
        config_file.parent.mkdir(exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.server_configs, f, default_flow_style=False, allow_unicode=True)
    
    def add_server(self, server_id: str, config: Dict) -> bool:
        """添加服务器配置"""
        try:
            # 验证连接
            if self.test_connection(config):
                self.server_configs[server_id] = config
                self.save_server_configs()
                return True
            return False
        except Exception as e:
            logger.error(f"添加服务器失败: {e}")
            return False
    
    def test_connection(self, config: Dict) -> bool:
        """测试SSH连接"""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            connect_params = {
                'hostname': config['host'],
                'port': config.get('port', 22),
                'username': config['username'],
                'timeout': 10
            }
            
            if 'password' in config:
                connect_params['password'] = config['password']
            elif 'key_file' in config:
                connect_params['key_filename'] = config['key_file']
            
            client.connect(**connect_params)
            client.close()
            return True
        except Exception as e:
            logger.error(f"SSH连接测试失败: {e}")
            return False
    
    def get_connection(self, server_id: str) -> Optional[paramiko.SSHClient]:
        """获取SSH连接"""
        if server_id not in self.server_configs:
            return None
        
        if server_id not in self.connections:
            try:
                config = self.server_configs[server_id]
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                connect_params = {
                    'hostname': config['host'],
                    'port': config.get('port', 22),
                    'username': config['username'],
                    'timeout': 10
                }
                
                if 'password' in config:
                    connect_params['password'] = config['password']
                elif 'key_file' in config:
                    connect_params['key_filename'] = config['key_file']
                
                client.connect(**connect_params)
                self.connections[server_id] = client
            except Exception as e:
                logger.error(f"SSH连接失败: {e}")
                return None
        
        return self.connections[server_id]
    
    def execute_command(self, server_id: str, command: str) -> Dict:
        """在远程服务器执行命令"""
        client = self.get_connection(server_id)
        if not client:
            return {'success': False, 'error': '无法连接到服务器'}
        
        try:
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            exit_code = stdout.channel.recv_exit_status()
            
            return {
                'success': exit_code == 0,
                'output': output,
                'error': error,
                'exit_code': exit_code
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def browse_directory(self, server_id: str, path: str = '/') -> Dict:
        """浏览远程目录"""
        client = self.get_connection(server_id)
        if not client:
            return {'success': False, 'error': '无法连接到服务器'}
        
        try:
            # 使用ls -la命令获取详细文件信息
            command = f"ls -la '{path}' 2>/dev/null || echo 'ERROR: Directory not accessible'"
            result = self.execute_command(server_id, command)
            
            if not result['success'] or 'ERROR:' in result['output']:
                return {'success': False, 'error': '目录不存在或无权限访问'}
            
            files = []
            lines = result['output'].strip().split('\n')
            
            for line in lines[1:]:  # 跳过第一行总计信息
                if not line.strip():
                    continue
                    
                parts = line.split()
                if len(parts) < 9:
                    continue
                    
                permissions = parts[0]
                size = parts[4] if parts[4].isdigit() else 0
                name = ' '.join(parts[8:])
                
                # 跳过当前目录和上级目录
                if name in ['.', '..']:
                    continue
                
                file_info = {
                    'name': name,
                    'size': int(size) if str(size).isdigit() else 0,
                    'is_directory': permissions.startswith('d'),
                    'permissions': permissions,
                    'full_path': f"{path.rstrip('/')}/{name}"
                }
                
                # 如果是视频文件，解析剧集信息
                if self._is_video_file(name):
                    file_info['episode_info'] = self._parse_episode_info(name)
                    file_info['file_type'] = 'video'
                elif self._is_subtitle_file(name):
                    file_info['file_type'] = 'subtitle'
                else:
                    file_info['file_type'] = 'other'
                
                files.append(file_info)
            
            # 按目录优先，然后按名称排序
            files.sort(key=lambda x: (not x['is_directory'], x['name'].lower()))
            
            return {
                'success': True,
                'path': path,
                'files': files
            }
            
        except Exception as e:
            logger.error(f"浏览目录失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_directory_stats(self, server_id: str, path: str) -> Dict:
        """获取目录统计信息"""
        client = self.get_connection(server_id)
        if not client:
            return {'success': False, 'error': '无法连接到服务器'}
        
        try:
            # 获取文件数量统计
            count_cmd = f"find '{path}' -maxdepth 1 -type f | wc -l"
            count_result = self.execute_command(server_id, count_cmd)
            
            # 获取目录数量统计
            dir_count_cmd = f"find '{path}' -maxdepth 1 -type d | wc -l"
            dir_count_result = self.execute_command(server_id, dir_count_cmd)
            
            # 获取总大小
            size_cmd = f"du -sh '{path}' 2>/dev/null | cut -f1"
            size_result = self.execute_command(server_id, size_cmd)
            
            # 获取视频文件数量
            video_cmd = f"find '{path}' -maxdepth 1 -type f \\( -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.avi' -o -iname '*.mov' -o -iname '*.wmv' -o -iname '*.flv' -o -iname '*.webm' -o -iname '*.m4v' \\) | wc -l"
            video_result = self.execute_command(server_id, video_cmd)
            
            file_count = int(count_result['output'].strip()) if count_result['success'] else 0
            dir_count = max(0, int(dir_count_result['output'].strip()) - 1) if dir_count_result['success'] else 0  # 减1排除当前目录
            total_size = size_result['output'].strip() if size_result['success'] else '未知'
            video_count = int(video_result['output'].strip()) if video_result['success'] else 0
            
            return {
                'success': True,
                'file_count': file_count,
                'dir_count': dir_count,
                'total_size': total_size,
                'video_count': video_count
            }
            
        except Exception as e:
            logger.error(f"获取目录统计失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def _is_video_file(self, filename: str) -> bool:
        """判断是否为视频文件"""
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.ts', '.m2ts']
        return any(filename.lower().endswith(ext) for ext in video_extensions)
    
    def _is_subtitle_file(self, filename: str) -> bool:
        """判断是否为字幕文件"""
        subtitle_extensions = ['.srt', '.ass', '.ssa', '.vtt', '.sub', '.idx']
        return any(filename.lower().endswith(ext) for ext in subtitle_extensions)
    
    def _parse_episode_info(self, filename: str) -> Optional[Dict]:
        """解析剧集信息"""
        import re
        
        # 常见的剧集命名格式
        patterns = [
            r'[Ss](\d+)[Ee](\d+)',  # S01E01
            r'[Ss](\d+)\s*[Ee](\d+)',  # S01 E01
            r'(\d+)x(\d+)',  # 1x01
            r'第(\d+)季.*?第(\d+)集',  # 中文格式
            r'Season\s*(\d+).*?Episode\s*(\d+)',  # Season 1 Episode 1
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                season = int(match.group(1))
                episode = int(match.group(2))
                return {
                    'season': season,
                    'episode': episode,
                    'format': f'S{season:02d}E{episode:02d}'
                }
        
        return None
    
    def close_all_connections(self):
        """关闭所有SSH连接"""
        for client in self.connections.values():
            try:
                client.close()
            except:
                pass
        self.connections.clear()

class WebTorrentMaker:
    """Web界面的Torrent制作器包装类"""
    
    def __init__(self):
        self.core = TorrentMakerApp()
        self.ssh_manager = SSHServerManager()
        self.active_tasks: Dict[str, Dict] = {}
    
    def create_torrent_task(self, task_data: Dict) -> str:
        """创建种子制作任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.active_tasks)}"
        
        self.active_tasks[task_id] = {
            'id': task_id,
            'status': TaskStatus.PENDING.value,
            'progress': 0,
            'data': task_data,
            'created_at': datetime.now().isoformat(),
            'server_id': task_data.get('server_id'),
            'output': []
        }
        
        # 启动异步任务
        process_torrent_task.delay(task_id, task_data)
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        return self.active_tasks.get(task_id)
    
    def get_system_info(self) -> Dict:
        """获取系统信息"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used': memory.used,
                'memory_total': memory.total,
                'disk_percent': disk.percent,
                'disk_used': disk.used,
                'disk_total': disk.total
            }
        except Exception as e:
            logger.error(f"获取系统信息失败: {e}")
            return {}

# 全局实例
web_torrent_maker = WebTorrentMaker()

@celery_app.task
def process_torrent_task(task_id: str, task_data: Dict):
    """处理种子制作任务（异步）"""
    try:
        # 更新任务状态
        web_torrent_maker.active_tasks[task_id]['status'] = TaskStatus.RUNNING.value
        socketio.emit('task_update', {
            'task_id': task_id,
            'status': TaskStatus.RUNNING.value,
            'progress': 0
        })
        
        # 模拟进度更新
        for progress in range(0, 101, 10):
            web_torrent_maker.active_tasks[task_id]['progress'] = progress
            socketio.emit('task_update', {
                'task_id': task_id,
                'status': TaskStatus.RUNNING.value,
                'progress': progress
            })
            # 这里应该调用实际的torrent制作逻辑
            import time
            time.sleep(0.5)
        
        # 任务完成
        web_torrent_maker.active_tasks[task_id]['status'] = TaskStatus.COMPLETED.value
        web_torrent_maker.active_tasks[task_id]['progress'] = 100
        socketio.emit('task_update', {
            'task_id': task_id,
            'status': TaskStatus.COMPLETED.value,
            'progress': 100
        })
        
    except Exception as e:
        logger.error(f"任务处理失败: {e}")
        web_torrent_maker.active_tasks[task_id]['status'] = TaskStatus.FAILED.value
        socketio.emit('task_update', {
            'task_id': task_id,
            'status': TaskStatus.FAILED.value,
            'error': str(e)
        })

# Web路由
@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/servers', methods=['GET'])
def get_servers():
    """获取服务器列表"""
    return jsonify({
        'success': True,
        'servers': web_torrent_maker.ssh_manager.server_configs
    })

@app.route('/api/servers', methods=['POST'])
def add_server():
    """添加服务器"""
    data = request.get_json()
    server_id = data.get('id')
    config = data.get('config')
    
    if web_torrent_maker.ssh_manager.add_server(server_id, config):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': '服务器连接测试失败'})

@app.route('/api/servers/test', methods=['POST'])
def test_server_connection():
    """测试服务器连接"""
    data = request.get_json()
    
    try:
        # 构建配置字典
        config = {
            'host': data.get('host'),
            'port': data.get('port', 22),
            'username': data.get('username')
        }
        
        # 添加认证信息
        if data.get('password'):
            config['password'] = data.get('password')
        elif data.get('key_file'):
            config['key_file'] = data.get('key_file')
        
        # 使用SSH管理器测试连接
        success = web_torrent_maker.ssh_manager.test_connection(config)
        
        if success:
            return jsonify({'success': True, 'message': '连接测试成功'})
        else:
            return jsonify({'success': False, 'error': '连接失败'})
            
    except Exception as e:
        logger.error(f"测试连接失败: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """创建种子制作任务"""
    data = request.get_json()
    task_id = web_torrent_maker.create_torrent_task(data)
    return jsonify({'success': True, 'task_id': task_id})

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """获取任务状态"""
    task = web_torrent_maker.get_task_status(task_id)
    if task:
        return jsonify({'success': True, 'task': task})
    else:
        return jsonify({'success': False, 'error': '任务不存在'})

@app.route('/api/system', methods=['GET'])
def get_system_info():
    """获取系统信息"""
    try:
        import psutil
        
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 内存使用情况
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = memory.used / (1024**3)  # GB
        memory_total = memory.total / (1024**3)  # GB
        
        # 磁盘使用情况
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        disk_used = disk.used / (1024**3)  # GB
        disk_total = disk.total / (1024**3)  # GB
        
        return jsonify({
            'success': True,
            'data': {
                'cpu': {
                    'percent': cpu_percent
                },
                'memory': {
                    'percent': memory_percent,
                    'used': round(memory_used, 2),
                    'total': round(memory_total, 2)
                },
                'disk': {
                    'percent': round(disk_percent, 2),
                    'used': round(disk_used, 2),
                    'total': round(disk_total, 2)
                }
            }
        })
    except Exception as e:
        logger.error(f"获取系统信息失败: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/browse', methods=['POST'])
def browse_directory():
    """浏览远程目录"""
    try:
        data = request.get_json()
        server_id = data.get('server_id')
        path = data.get('path', '/')
        
        if not server_id:
            return jsonify({'success': False, 'error': '服务器ID不能为空'}), 400
        
        result = ssh_manager.browse_directory(server_id, path)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"浏览目录失败: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/directory-stats', methods=['POST'])
def get_directory_stats():
    """获取目录统计信息"""
    try:
        data = request.get_json()
        server_id = data.get('server_id')
        path = data.get('path')
        
        if not server_id or not path:
            return jsonify({'success': False, 'error': '服务器ID和路径不能为空'}), 400
        
        result = ssh_manager.get_directory_stats(server_id, path)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"获取目录统计失败: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# WebSocket事件
@socketio.on('connect')
def handle_connect():
    """客户端连接"""
    logger.info(f"客户端连接: {request.sid}")
    emit('connected', {'status': 'success'})

@socketio.on('disconnect')
def handle_disconnect():
    """客户端断开连接"""
    logger.info(f"客户端断开: {request.sid}")

@socketio.on('join_task')
def handle_join_task(data):
    """加入任务房间"""
    task_id = data.get('task_id')
    if task_id:
        join_room(task_id)
        logger.info(f"客户端 {request.sid} 加入任务房间: {task_id}")

@socketio.on('leave_task')
def handle_leave_task(data):
    """离开任务房间"""
    task_id = data.get('task_id')
    if task_id:
        leave_room(task_id)
        logger.info(f"客户端 {request.sid} 离开任务房间: {task_id}")

def main():
    """启动Web应用"""
    print("\n🌐 Torrent Maker Web Interface v2.1.0")
    print("="*50)
    print("启动Web界面...")
    
    # 检查Redis连接
    try:
        redis_client.ping()
        print("✅ Redis连接正常")
    except Exception as e:
        print(f"❌ Redis连接失败: {e}")
        print("请确保Redis服务正在运行")
        return
    
    # 启动应用
    try:
        print("\n🚀 Web界面已启动!")
        print(f"📱 访问地址: http://localhost:5001")
        print("\n按 Ctrl+C 停止服务")
        print("="*50)
        
        socketio.run(
            app,
            host='0.0.0.0',
            port=5001,
            debug=False,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 正在关闭Web界面...")
        web_torrent_maker.ssh_manager.close_all_connections()
        print("✅ Web界面已关闭")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == '__main__':
    main()