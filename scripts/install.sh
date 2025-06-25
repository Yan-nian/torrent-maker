#!/bin/bash

# Torrent Maker v1.6.1 单文件版本安装脚本
# 极简安装，一键完成所有配置

set -e  # 遇到错误时退出

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# 打印函数
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 获取最新版本号
get_latest_version() {
    if command_exists curl; then
        latest_version=$(curl -s "https://api.github.com/repos/Yan-nian/torrent-maker/releases/latest" | \
            python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tag = data.get('tag_name', '')
    version = tag.lstrip('v') if tag else '1.6.1'
    print(version)
except:
    print('1.6.1')
" 2>/dev/null)
        echo "${latest_version:-1.6.1}"
    else
        echo "1.6.1"
    fi
}

# 配置变量
REPO="Yan-nian/torrent-maker"
VERSION=$(get_latest_version)
INSTALL_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.torrent_maker"
SCRIPT_NAME="torrent_maker.py"
DOWNLOAD_URL="https://raw.githubusercontent.com/$REPO/main/torrent_maker.py"

# 显示欢迎信息
echo "🎬 Torrent Maker v$VERSION 单文件版本安装器"
echo "=============================================="
echo "真正的单文件种子制作工具 - 下载即用，无需配置"
echo ""

# 检查 Python 版本
check_python() {
    print_info "检查 Python 环境..."

    if ! command_exists python3; then
        print_error "Python 3 未安装，请先安装 Python 3.7 或更高版本"
        echo "安装指南："
        echo "  macOS: brew install python3"
        echo "  Ubuntu: sudo apt install python3"
        echo "  CentOS: sudo yum install python3"
        exit 1
    fi

    python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    print_success "检测到 Python 版本: $python_version"

    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"; then
        print_success "Python 版本符合要求 (>= 3.7)"
    else
        print_error "Python 版本过低，需要 Python 3.7 或更高版本"
        exit 1
    fi
}

# 检查 mktorrent
check_mktorrent() {
    print_info "检查 mktorrent..."

    if command_exists mktorrent; then
        print_success "mktorrent 已安装"
        return 0
    fi

    print_warning "mktorrent 未安装，正在尝试自动安装..."

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install mktorrent
        else
            print_error "需要 Homebrew 来安装 mktorrent: brew install mktorrent"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            sudo apt-get update && sudo apt-get install -y mktorrent
        elif command_exists yum; then
            sudo yum install -y mktorrent
        elif command_exists dnf; then
            sudo dnf install -y mktorrent
        elif command_exists pacman; then
            sudo pacman -S mktorrent
        else
            print_error "请手动安装 mktorrent"
            exit 1
        fi
    else
        print_error "不支持的操作系统，请手动安装 mktorrent"
        exit 1
    fi

    if ! command_exists mktorrent; then
        print_error "mktorrent 安装失败，请手动安装后重新运行此脚本"
        exit 1
    fi

    print_success "mktorrent 安装成功"
}

# 下载并安装
download_and_install() {
    print_info "下载 Torrent Maker v$VERSION..."

    # 创建目录
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$CONFIG_DIR"

    target_file="$INSTALL_DIR/$SCRIPT_NAME"

    # 优先使用本地文件（如果在项目目录运行）
    if [ -f "./torrent_maker.py" ]; then
        print_info "使用本地文件"
        cp "./torrent_maker.py" "$target_file"
    else
        # 从GitHub下载
        print_info "从GitHub下载最新版本..."
        if command_exists curl; then
            curl -fsSL "$DOWNLOAD_URL" -o "$target_file"
        elif command_exists wget; then
            wget -q "$DOWNLOAD_URL" -O "$target_file"
        else
            print_error "需要 curl 或 wget 来下载文件"
            exit 1
        fi
    fi

    # 验证文件
    if [ ! -f "$target_file" ] || [ ! -s "$target_file" ]; then
        print_error "下载失败或文件为空"
        exit 1
    fi

    # 设置执行权限
    chmod +x "$target_file"

    # 保存版本信息
    echo "v$VERSION" > "$CONFIG_DIR/version"

    print_success "安装完成"
}

# 显示使用说明
show_usage() {
    echo ""
    print_success "🎉 Torrent Maker v$VERSION 安装成功！"
    echo "=============================================="
    echo ""
    echo "📋 使用方法："
    echo "  python3 $INSTALL_DIR/$SCRIPT_NAME"
    echo ""
    echo "📁 配置目录: $CONFIG_DIR"
    echo "📄 程序位置: $INSTALL_DIR/$SCRIPT_NAME"
    echo ""
    echo "🚀 现在可以开始使用了！"
    echo ""
    echo "💡 提示："
    echo "  - 首次运行会自动创建配置文件"
    echo "  - 支持智能搜索和批量制种"
    echo "  - 所有功能都集成在单个文件中"
}

# 主函数
main() {
    check_python
    check_mktorrent
    download_and_install
    show_usage
}

# 运行主函数
main "$@"
