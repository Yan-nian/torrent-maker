#!/bin/bash

# Torrent Maker 安装脚本
# 适用于 macOS 和 Linux 系统

echo "🎬 Torrent Maker 安装脚本"
echo "=========================="

# 检查 Python 版本
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "📍 检测到 Python 版本: $python_version"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"; then
    echo "✅ Python 版本符合要求 (>= 3.7)"
else
    echo "❌ Python 版本过低，需要 Python 3.7 或更高版本"
    exit 1
fi

# 检查操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "📱 检测到 macOS 系统"
    
    # 检查 Homebrew
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew 未安装，请先安装 Homebrew: https://brew.sh/"
        exit 1
    fi
    
    # 安装 mktorrent
    if ! command -v mktorrent &> /dev/null; then
        echo "📦 正在安装 mktorrent..."
        brew install mktorrent
    else
        echo "✅ mktorrent 已安装"
    fi
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "🐧 检测到 Linux 系统"
    
    # 检查包管理器并安装 mktorrent
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

# 安装 Python 依赖
echo "📦 正在安装 Python 依赖包..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt
    echo "✅ Python 依赖安装完成"
else
    echo "⚠️  requirements.txt 文件不存在，跳过依赖安装"
fi

# 创建输出目录
echo "📁 创建输出目录..."
mkdir -p output
echo "✅ 输出目录创建完成"

# 设置执行权限
echo "🔧 设置执行权限..."
chmod +x run.py
echo "✅ 权限设置完成"

echo ""
echo "🎉 安装完成！"
echo "=========================="
echo "使用方法："
echo "  python3 run.py"
echo "或者："
echo "  python3 src/main.py"
echo ""
echo "第一次运行时，程序会提示您设置资源文件夹路径。"
echo "请确保您的影视剧文件存放在该文件夹中。"
