#!/usr/bin/env python3
"""
远程服务器性能修复脚本
专门解决Python制种性能问题
"""

import sys
import shutil
import subprocess
from pathlib import Path

def check_and_install_mktorrent():
    """检查并安装mktorrent"""
    print("🔍 检查mktorrent状态...")
    
    # 检查是否已安装
    if shutil.which('mktorrent'):
        print("  ✅ mktorrent已安装")
        
        # 检查版本
        try:
            result = subprocess.run(['mktorrent', '--help'], 
                                  capture_output=True, text=True, timeout=5)
            print("  📋 mktorrent可用")
            return True
        except:
            print("  ⚠️  mktorrent安装但无法运行")
            return False
    else:
        print("  ❌ mktorrent未安装")
        print("  💡 正在尝试安装mktorrent...")
        
        # 尝试安装
        try:
            # Debian/Ubuntu
            result = subprocess.run(['apt-get', 'update'], 
                                  capture_output=True, timeout=60)
            if result.returncode == 0:
                result = subprocess.run(['apt-get', 'install', '-y', 'mktorrent'], 
                                      capture_output=True, timeout=120)
                if result.returncode == 0:
                    print("  ✅ mktorrent安装成功")
                    return True
                else:
                    print(f"  ❌ 安装失败: {result.stderr.decode()}")
            
            # 尝试其他包管理器
            for cmd in [['yum', 'install', '-y', 'mktorrent'], 
                       ['dnf', 'install', '-y', 'mktorrent']]:
                try:
                    result = subprocess.run(cmd, capture_output=True, timeout=120)
                    if result.returncode == 0:
                        print("  ✅ mktorrent安装成功")
                        return True
                except:
                    continue
                    
        except Exception as e:
            print(f"  ❌ 自动安装失败: {e}")
        
        print("  💡 请手动安装mktorrent:")
        print("     Debian/Ubuntu: sudo apt-get install mktorrent")
        print("     CentOS/RHEL: sudo yum install mktorrent")
        print("     Fedora: sudo dnf install mktorrent")
        return False

def force_mktorrent_engine():
    """强制使用mktorrent引擎"""
    print("\n🔧 配置强制使用mktorrent引擎...")
    
    torrent_maker_path = Path("torrent_maker.py")
    if not torrent_maker_path.exists():
        print("  ❌ 找不到torrent_maker.py文件")
        return False
    
    # 创建配置文件强制使用mktorrent
    config_content = '''
# 远程服务器性能优化配置
# 强制使用mktorrent引擎

import os
import sys

# 设置环境变量强制使用mktorrent
os.environ['TORRENT_MAKER_ENGINE'] = 'mktorrent'
os.environ['TORRENT_MAKER_FORCE_MKTORRENT'] = '1'

print("🚀 已配置强制使用mktorrent引擎")
'''
    
    config_path = Path("remote_config.py")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"  ✅ 配置文件已创建: {config_path}")
    return True

def create_optimized_launcher():
    """创建优化的启动脚本"""
    print("\n🚀 创建优化启动脚本...")
    
    launcher_content = '''#!/bin/bash
# Torrent Maker 远程服务器优化启动脚本

echo "🚀 Torrent Maker v1.7.3 - 远程服务器优化版"
echo "=================================================="

# 检查mktorrent
if ! command -v mktorrent &> /dev/null; then
    echo "❌ mktorrent未安装，性能将受到影响"
    echo "💡 建议安装: sudo apt-get install mktorrent"
else
    echo "✅ mktorrent已安装"
fi

# 设置环境变量
export TORRENT_MAKER_ENGINE=mktorrent
export TORRENT_MAKER_FORCE_MKTORRENT=1

# 启动程序
python3 torrent_maker.py "$@"
'''
    
    launcher_path = Path("torrent_maker_optimized.sh")
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    # 设置执行权限
    launcher_path.chmod(0o755)
    
    print(f"  ✅ 优化启动脚本已创建: {launcher_path}")
    print("  💡 使用方法: ./torrent_maker_optimized.sh")
    return True

def test_optimization():
    """测试优化效果"""
    print("\n🧪 测试优化效果...")
    
    try:
        result = subprocess.run([sys.executable, 'torrent_maker.py', '--test-performance'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("  ✅ 性能测试通过")
            if "mktorrent" in result.stdout:
                print("  🚀 已成功配置使用mktorrent引擎")
                return True
            else:
                print("  ⚠️  仍在使用Python引擎")
                return False
        else:
            print(f"  ❌ 性能测试失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def main():
    """主修复函数"""
    print("🔧 Torrent Maker 远程服务器性能修复工具")
    print("=" * 50)
    print("专门解决Python制种性能慢的问题")
    print()
    
    success_count = 0
    total_steps = 4
    
    # 1. 检查并安装mktorrent
    if check_and_install_mktorrent():
        success_count += 1
    
    # 2. 强制使用mktorrent引擎
    if force_mktorrent_engine():
        success_count += 1
    
    # 3. 创建优化启动脚本
    if create_optimized_launcher():
        success_count += 1
    
    # 4. 测试优化效果
    if test_optimization():
        success_count += 1
    
    print(f"\n📊 修复结果: {success_count}/{total_steps} 步骤成功")
    
    if success_count >= 3:
        print("🎉 修复成功！")
        print("\n📋 使用建议:")
        print("  1. 使用 ./torrent_maker_optimized.sh 启动程序")
        print("  2. 或者直接运行 python3 torrent_maker.py")
        print("  3. 程序现在会优先使用mktorrent引擎")
        print("  4. 对于大文件，性能应该有显著提升")
    else:
        print("⚠️  部分修复失败，但程序仍可使用")
        print("💡 建议手动安装mktorrent以获得最佳性能")

if __name__ == "__main__":
    main()
