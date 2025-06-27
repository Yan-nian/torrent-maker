#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Torrent Maker Web Interface 启动脚本
v2.1.0 - Web界面版本

快速启动Web界面的便捷脚本
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    required_packages = [
        'flask',
        'flask_socketio',
        'paramiko',
        'celery',
        'redis',
        'psutil',
        'pyyaml',
        'coloredlogs',
        'watchdog'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(packages):
    """安装缺失的依赖"""
    print(f"\n📦 检测到缺失依赖: {', '.join(packages)}")
    print("正在自动安装...")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def check_redis():
    """检查Redis服务"""
    try:
        import redis
        client = redis.Redis(host='localhost', port=6379, db=0)
        client.ping()
        return True
    except Exception:
        return False

def start_redis():
    """尝试启动Redis服务"""
    print("\n🔄 尝试启动Redis服务...")
    
    # macOS使用brew启动Redis
    if sys.platform == 'darwin':
        try:
            subprocess.run(['brew', 'services', 'start', 'redis'], check=True)
            time.sleep(2)
            if check_redis():
                print("✅ Redis服务启动成功")
                return True
        except subprocess.CalledProcessError:
            pass
    
    # Linux使用systemctl启动Redis
    elif sys.platform.startswith('linux'):
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'redis'], check=True)
            time.sleep(2)
            if check_redis():
                print("✅ Redis服务启动成功")
                return True
        except subprocess.CalledProcessError:
            pass
    
    print("❌ 无法自动启动Redis服务")
    print("请手动启动Redis服务后重试")
    return False

def create_directories():
    """创建必要的目录"""
    directories = [
        'web',
        'web/static',
        'web/static/css',
        'web/static/js',
        'web/templates',
        'web/api',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def show_banner():
    """显示启动横幅"""
    print("\n" + "="*60)
    print("🌐 Torrent Maker Web Interface v2.1.0")
    print("="*60)
    print("基于Flask + WebSocket的现代化Web界面")
    print("支持多服务器SSH连接和实时进度监控")
    print("="*60)

def show_usage():
    """显示使用说明"""
    print("\n📖 使用说明:")
    print("1. 访问 http://localhost:5001 打开Web界面")
    print("2. 在'服务器管理'中添加SSH服务器")
    print("3. 在'创建种子'中制作新的种子文件")
    print("4. 在'任务管理'中查看制作进度")
    print("5. 按 Ctrl+C 停止服务")
    print("\n🔧 故障排除:")
    print("- 确保Redis服务正在运行")
    print("- 检查防火墙设置允许5001端口")
    print("- 查看logs目录下的日志文件")

def main():
    """主函数"""
    show_banner()
    
    # 检查当前目录
    if not Path('torrent_maker.py').exists():
        print("❌ 错误: 请在torrent-maker项目根目录下运行此脚本")
        sys.exit(1)
    
    # 创建必要目录
    create_directories()
    
    # 检查依赖
    print("\n🔍 检查依赖...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        if not install_dependencies(missing_packages):
            print("\n💡 请手动安装依赖:")
            print(f"pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("✅ 所有依赖已安装")
    
    # 检查Redis服务
    print("\n🔍 检查Redis服务...")
    if not check_redis():
        print("❌ Redis服务未运行")
        if not start_redis():
            print("\n💡 请手动启动Redis服务:")
            print("macOS: brew services start redis")
            print("Linux: sudo systemctl start redis")
            print("Windows: 下载并启动Redis服务")
            sys.exit(1)
    else:
        print("✅ Redis服务正常")
    
    # 显示使用说明
    show_usage()
    
    # 启动Web应用
    print("\n🚀 启动Web界面...")
    try:
        # 导入并启动web应用
        from web_app import main as start_web_app
        start_web_app()
    except KeyboardInterrupt:
        print("\n\n👋 Web界面已停止")
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保web_app.py文件存在且格式正确")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()