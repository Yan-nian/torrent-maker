#!/usr/bin/env python3
"""
远程服务器性能测试脚本
用于验证 torrent-maker v1.7.3 的优化效果
"""

import sys
import time
import subprocess
from pathlib import Path

def test_mktorrent_availability():
    """测试mktorrent是否可用"""
    print("🔍 检查mktorrent可用性...")
    try:
        result = subprocess.run(['mktorrent', '--help'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("  ✅ mktorrent已安装")
            return True
        else:
            print("  ❌ mktorrent不可用")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ❌ mktorrent未安装")
        print("  💡 安装命令: apt-get install mktorrent")
        return False

def test_hardware_detection():
    """测试硬件检测"""
    print("\n🔍 测试硬件检测...")
    try:
        result = subprocess.run([sys.executable, 'torrent_maker.py', '--test-performance'], 
                              capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print(f"错误信息: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("  ⏰ 硬件检测超时")
        return False
    except Exception as e:
        print(f"  ❌ 硬件检测失败: {e}")
        return False

def create_test_file(size_mb=100):
    """创建测试文件"""
    test_file = Path("test_file.bin")
    print(f"\n🔧 创建{size_mb}MB测试文件...")
    
    try:
        with open(test_file, 'wb') as f:
            # 写入随机数据
            chunk_size = 1024 * 1024  # 1MB chunks
            for i in range(size_mb):
                f.write(b'0' * chunk_size)
        
        print(f"  ✅ 测试文件创建成功: {test_file}")
        return test_file
    except Exception as e:
        print(f"  ❌ 创建测试文件失败: {e}")
        return None

def test_torrent_creation_speed(test_file):
    """测试种子创建速度"""
    if not test_file or not test_file.exists():
        print("  ❌ 测试文件不存在")
        return False
    
    print(f"\n🚀 测试种子创建速度...")
    
    # 测试mktorrent引擎
    print("  🔧 测试mktorrent引擎...")
    start_time = time.time()
    try:
        # 使用简单的mktorrent命令测试
        result = subprocess.run([
            'mktorrent', 
            '-o', 'test_mktorrent.torrent',
            '-a', 'http://test.tracker.com/announce',
            str(test_file)
        ], capture_output=True, text=True, timeout=120)
        
        mktorrent_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"    ✅ mktorrent完成，耗时: {mktorrent_time:.2f}秒")
            # 清理
            Path('test_mktorrent.torrent').unlink(missing_ok=True)
        else:
            print(f"    ❌ mktorrent失败: {result.stderr}")
            mktorrent_time = None
    except subprocess.TimeoutExpired:
        print("    ⏰ mktorrent超时")
        mktorrent_time = None
    except Exception as e:
        print(f"    ❌ mktorrent测试失败: {e}")
        mktorrent_time = None
    
    return mktorrent_time

def cleanup_test_files():
    """清理测试文件"""
    print("\n🧹 清理测试文件...")
    test_files = [
        'test_file.bin',
        'test_mktorrent.torrent',
        'test_python.torrent'
    ]
    
    for file_path in test_files:
        Path(file_path).unlink(missing_ok=True)
    
    print("  ✅ 清理完成")

def main():
    """主测试函数"""
    print("🚀 Torrent Maker v1.7.3 - 远程服务器性能测试")
    print("=" * 60)
    
    # 1. 检查mktorrent
    mktorrent_available = test_mktorrent_availability()
    
    # 2. 硬件检测测试
    hardware_ok = test_hardware_detection()
    
    if not hardware_ok:
        print("\n❌ 硬件检测失败，请检查torrent_maker.py是否正常")
        return
    
    # 3. 性能测试（如果mktorrent可用）
    if mktorrent_available:
        test_file = create_test_file(50)  # 50MB测试文件
        if test_file:
            mktorrent_time = test_torrent_creation_speed(test_file)
            
            print(f"\n📊 性能测试结果:")
            if mktorrent_time:
                print(f"  🚀 mktorrent: {mktorrent_time:.2f}秒")
                speed_mb_s = 50 / mktorrent_time
                print(f"  📈 处理速度: {speed_mb_s:.1f}MB/s")
                
                if speed_mb_s > 10:
                    print("  ✅ 性能优秀！")
                elif speed_mb_s > 5:
                    print("  ⚠️  性能一般，可能需要进一步优化")
                else:
                    print("  ❌ 性能较差，建议检查系统配置")
            
            cleanup_test_files()
    else:
        print("\n⚠️  mktorrent不可用，无法进行完整性能测试")
        print("建议安装mktorrent以获得最佳性能")
    
    print("\n🎉 测试完成！")

if __name__ == "__main__":
    main()
