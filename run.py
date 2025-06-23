#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Torrent Maker 运行脚本
用于快速启动种子制作工具
"""

import sys
import os

# 添加 src 目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from main import main
    
    if __name__ == "__main__":
        print("正在启动 Torrent Maker...")
        main()
        
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有依赖都已正确安装")
    sys.exit(1)
except Exception as e:
    print(f"程序运行时发生错误: {e}")
    sys.exit(1)
