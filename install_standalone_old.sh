#!/bin/bash

# Torrent Maker 单文件版本安装脚本
# 适用于 macOS 和 Linux 系统

echo "🎬 Torrent Maker 单文件版本安装"
echo "================================"

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装，请先安装 Python 3.7 或更高版本"
    exit 1
fi

python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "📍 检测到 Python 版本: $python_version"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"; then
    echo "✅ Python 版本符合要求 (>= 3.7)"
else
    echo "❌ Python 版本过低，需要 Python 3.7 或更高版本"
    exit 1
fi

# 检查操作系统并安装 mktorrent
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "📱 检测到 macOS 系统"
    
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew 未安装，请先安装 Homebrew: https://brew.sh/"
        exit 1
    fi
    
    if ! command -v mktorrent &> /dev/null; then
        echo "📦 正在安装 mktorrent..."
        brew install mktorrent
    else
        echo "✅ mktorrent 已安装"
    fi
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "🐧 检测到 Linux 系统"
    
    if command -v apt-get &> /dev/null; then
        echo "📦 使用 apt-get 安装 mktorrent..."
        sudo apt-get update
        sudo apt-get install -y mktorrent
    elif command -v yum &> /dev/null; then
        echo "📦 使用 yum 安装 mktorrent..."
        sudo yum install -y mktorrent
    elif command -v dnf &> /dev/null; then
        echo "📦 使用 dnf 安装 mktorrent..."
        sudo dnf install -y mktorrent
    else
        echo "❌ 未找到支持的包管理器，请手动安装 mktorrent"
        exit 1
    fi
else
    echo "❌ 不支持的操作系统: $OSTYPE"
    echo "请手动安装 mktorrent 工具"
    exit 1
fi

# 验证 mktorrent 安装
if command -v mktorrent &> /dev/null; then
    mktorrent_version=$(mktorrent -h 2>&1 | head -n 1)
    echo "✅ mktorrent 安装成功: $mktorrent_version"
else
    echo "❌ mktorrent 安装失败"
    exit 1
fi

# 下载单文件版本（如果不存在）
if [ ! -f "torrent_maker.py" ]; then
    echo "📥 正在下载 torrent_maker.py..."
    # 这里可以添加下载链接，目前假设文件已存在
    echo "⚠️  请确保 torrent_maker.py 文件在当前目录"
fi

# 设置执行权限
if [ -f "torrent_maker.py" ]; then
    chmod +x torrent_maker.py
    echo "✅ 权限设置完成"
else
    echo "❌ 未找到 torrent_maker.py 文件"
    exit 1
fi

echo ""
echo "🎉 安装完成！"
echo "================================"
echo "使用方法："
echo "  python3 torrent_maker.py"
echo ""
echo "单文件版本优势："
echo "- 📦 无需安装依赖包"
echo "- 🚀 一个文件包含所有功能"
echo "- 💾 配置文件自动保存到 ~/.torrent_maker/"
echo "- 🔧 首次运行会自动创建配置"
echo ""
echo "开始使用吧！🎬"
