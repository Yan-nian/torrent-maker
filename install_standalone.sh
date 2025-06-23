#!/bin/bash

# Torrent Maker 单文件版本智能安装/更新脚本
# 支持 macOS 和 Linux 系统，支持自动更新

set -e  # 遇到错误时退出

VERSION="v1.0.2"  # 当前版本
REPO="Yan-nian/torrent-maker"
INSTALL_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.torrent_maker"
SCRIPT_NAME="torrent_maker.py"
# 临时使用raw文件下载，直到GitHub Release创建完成
DOWNLOAD_URL="https://raw.githubusercontent.com/$REPO/main/torrent_maker.py"

# 解析命令行参数
FORCE_INSTALL=false
QUIET_MODE=false

for arg in "$@"; do
    case $arg in
        --force)
            FORCE_INSTALL=true
            shift
            ;;
        --quiet)
            QUIET_MODE=true
            shift
            ;;
        --help)
            echo "Torrent Maker 安装脚本"
            echo ""
            echo "用法: bash install_standalone.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --force   强制重新安装，即使已是最新版本"
            echo "  --quiet   静默模式，减少输出信息"
            echo "  --help    显示此帮助信息"
            echo ""
            echo "示例:"
            echo "  curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash"
            echo "  curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash -s -- --force"
            exit 0
            ;;
        *)
            ;;
    esac
done

if [ "$QUIET_MODE" = false ]; then
    echo "🎬 Torrent Maker 单文件版本安装器"
    echo "=================================="
    echo "版本: $VERSION (安装脚本: v1.0.2-fix)"
    echo "仓库: https://github.com/$REPO"
    echo ""
fi

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印彩色消息
print_info() { 
    if [ "$QUIET_MODE" = false ]; then
        echo -e "${BLUE}ℹ️  $1${NC}"
    fi
}
print_success() { 
    if [ "$QUIET_MODE" = false ]; then
        echo -e "${GREEN}✅ $1${NC}"
    fi
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

# 检查并安装 mktorrent
check_mktorrent() {
    print_info "检查 mktorrent..."
    
    if command_exists mktorrent; then
        mktorrent_version=$(mktorrent -h 2>&1 | head -n 1 | grep -o '[0-9]\+\.[0-9]\+' || echo "未知版本")
        print_success "mktorrent 已安装 (版本: $mktorrent_version)"
        return 0
    fi
    
    print_warning "mktorrent 未安装，正在尝试自动安装..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        print_info "检测到 macOS 系统"
        
        if command_exists brew; then
            print_info "使用 Homebrew 安装 mktorrent..."
            brew install mktorrent
        else
            print_error "需要 Homebrew 来安装 mktorrent"
            echo "请先安装 Homebrew: https://brew.sh/"
            echo "然后运行: brew install mktorrent"
            exit 1
        fi
        
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        print_info "检测到 Linux 系统"
        
        if command_exists apt-get; then
            print_info "使用 apt 安装 mktorrent..."
            sudo apt-get update && sudo apt-get install -y mktorrent
        elif command_exists yum; then
            print_info "使用 yum 安装 mktorrent..."
            sudo yum install -y mktorrent
        elif command_exists dnf; then
            print_info "使用 dnf 安装 mktorrent..."
            sudo dnf install -y mktorrent
        elif command_exists pacman; then
            print_info "使用 pacman 安装 mktorrent..."
            sudo pacman -S --noconfirm mktorrent
        else
            print_error "未找到支持的包管理器"
            echo "请手动安装 mktorrent："
            echo "  Debian/Ubuntu: sudo apt install mktorrent"
            echo "  CentOS/RHEL: sudo yum install mktorrent"
            echo "  Fedora: sudo dnf install mktorrent"
            echo "  Arch: sudo pacman -S mktorrent"
            exit 1
        fi
    else
        print_error "不支持的操作系统: $OSTYPE"
        echo "请手动安装 mktorrent 工具"
        exit 1
    fi
    
    # 验证安装
    if command_exists mktorrent; then
        mktorrent_version=$(mktorrent -h 2>&1 | head -n 1 | grep -o '[0-9]\+\.[0-9]\+' || echo "未知版本")
        print_success "mktorrent 安装成功 (版本: $mktorrent_version)"
    else
        print_error "mktorrent 安装失败"
        exit 1
    fi
}

# 检查网络连接
check_network() {
    print_info "检查网络连接..."
    if command_exists curl; then
        if curl -s --head https://github.com >/dev/null; then
            print_success "网络连接正常"
        else
            print_error "无法连接到 GitHub，请检查网络"
            exit 1
        fi
    elif command_exists wget; then
        if wget -q --spider https://github.com; then
            print_success "网络连接正常"
        else
            print_error "无法连接到 GitHub，请检查网络"
            exit 1
        fi
    else
        print_warning "未找到 curl 或 wget，跳过网络检查"
    fi
}

# 检查是否已安装
check_existing_installation() {
    if [ -f "$INSTALL_DIR/$SCRIPT_NAME" ]; then
        print_info "检测到已安装的版本"
        
        # 检查版本
        if [ -f "$CONFIG_DIR/version" ]; then
            installed_version=$(cat "$CONFIG_DIR/version")
            print_info "已安装版本: $installed_version"
            
            if [ "$installed_version" = "$VERSION" ]; then
                if [ "$FORCE_INSTALL" = true ]; then
                    print_warning "强制重新安装模式，将覆盖现有安装"
                else
                    print_success "已是最新版本 ($VERSION)"
                    echo ""
                    echo "💡 选项："
                    echo "  1. 直接使用: python3 $INSTALL_DIR/$SCRIPT_NAME"
                    echo "  2. 强制重新安装: bash <(curl -fsSL https://raw.githubusercontent.com/$REPO/main/install_standalone.sh) --force"
                    echo "  3. 手动删除后重装:"
                    echo "     rm $INSTALL_DIR/$SCRIPT_NAME"
                    echo "     rm -rf $CONFIG_DIR"
                    echo ""
                    read -p "🤔 是否继续重新安装？(y/N): " -n 1 -r
                    echo
                    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                        print_info "安装取消"
                        echo ""
                        echo "🚀 开始使用: python3 $INSTALL_DIR/$SCRIPT_NAME"
                        exit 0
                    fi
                fi
            else
                print_warning "发现旧版本 ($installed_version)，将更新到 $VERSION"
            fi
        else
            print_warning "版本信息缺失，将重新安装"
        fi
    fi
}

# 创建安装目录
create_directories() {
    print_info "创建目录..."
    
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$CONFIG_DIR"
    
    print_success "目录创建完成"
}

# 下载并安装
download_and_install() {
    print_info "下载 Torrent Maker..."
    print_info "使用直接下载模式 (v1.0.2-fix)"
    
    # 直接下载单文件到安装目录
    if command_exists curl; then
        print_info "下载地址: $DOWNLOAD_URL"
        curl -L "$DOWNLOAD_URL" -o "$INSTALL_DIR/$SCRIPT_NAME"
    elif command_exists wget; then
        print_info "下载地址: $DOWNLOAD_URL"
        wget "$DOWNLOAD_URL" -O "$INSTALL_DIR/$SCRIPT_NAME"
    else
        print_error "需要 curl 或 wget 来下载文件"
        exit 1
    fi
    
    print_success "下载完成"
    print_info "跳过解压步骤 (直接下载单文件)"
    
    # 设置执行权限
    chmod +x "$INSTALL_DIR/$SCRIPT_NAME"
    
    # 保存版本信息
    echo "$VERSION" > "$CONFIG_DIR/version"
    
    print_success "安装完成"
}

# 设置 PATH
setup_path() {
    print_info "配置环境变量..."
    
    # 检查 PATH 中是否包含安装目录
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        print_warning "$INSTALL_DIR 不在 PATH 中"
        
        # 添加到 shell 配置文件
        shell_config=""
        if [ -n "$BASH_VERSION" ]; then
            shell_config="$HOME/.bashrc"
        elif [ -n "$ZSH_VERSION" ]; then
            shell_config="$HOME/.zshrc"
        else
            shell_config="$HOME/.profile"
        fi
        
        echo "" >> "$shell_config"
        echo "# Torrent Maker" >> "$shell_config"
        echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$shell_config"
        
        print_success "已添加到 $shell_config"
        print_warning "请运行 'source $shell_config' 或重新打开终端"
    else
        print_success "PATH 配置正确"
    fi
}

# 创建桌面快捷方式（可选）
create_shortcut() {
    if [[ "$OSTYPE" == "linux-gnu"* ]] && [ -d "$HOME/Desktop" ]; then
        read -p "是否创建桌面快捷方式？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cat > "$HOME/Desktop/torrent-maker.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Torrent Maker
Comment=半自动化种子制作工具
Exec=python3 $INSTALL_DIR/$SCRIPT_NAME
Icon=folder-downloads
Terminal=true
Categories=Utility;FileTools;
EOF
            chmod +x "$HOME/Desktop/torrent-maker.desktop"
            print_success "桌面快捷方式创建完成"
        fi
    fi
}

# 验证安装
verify_installation() {
    print_info "验证安装..."
    
    if [ -f "$INSTALL_DIR/$SCRIPT_NAME" ] && [ -x "$INSTALL_DIR/$SCRIPT_NAME" ]; then
        print_success "文件安装正确"
    else
        print_error "安装验证失败"
        exit 1
    fi
    
    if python3 -c "import os, sys, json, re, difflib, subprocess" 2>/dev/null; then
        print_success "Python 依赖检查通过"
    else
        print_error "Python 依赖检查失败"
        exit 1
    fi
}

# 显示使用说明
show_usage() {
    if [ "$QUIET_MODE" = false ]; then
        echo ""
        echo "🎉 安装成功！"
        echo "=================================="
        echo ""
        echo "📋 使用方法："
        echo "  方式1: python3 $INSTALL_DIR/$SCRIPT_NAME"
        if [[ ":$PATH:" == *":$INSTALL_DIR:"* ]]; then
            echo "  方式2: $SCRIPT_NAME"
        fi
        echo ""
        echo "📁 配置目录: $CONFIG_DIR"
        echo "📄 程序位置: $INSTALL_DIR/$SCRIPT_NAME"
        echo ""
        echo "✨ 特性："
        echo "  - 🔍 智能模糊搜索"
        echo "  - 🎬 剧集信息解析"
        echo "  - 🌐 Tracker 管理"
        echo "  - 📁 自定义路径配置"
        echo ""
        echo "🔄 更新/重装方法："
        echo "  普通安装: curl -fsSL https://raw.githubusercontent.com/$REPO/main/install_standalone.sh | bash"
        echo "  强制重装: curl -fsSL https://raw.githubusercontent.com/$REPO/main/install_standalone.sh | bash -s -- --force"
        echo "  静默安装: curl -fsSL https://raw.githubusercontent.com/$REPO/main/install_standalone.sh | bash -s -- --quiet"
        echo ""
        echo "🐛 问题反馈："
        echo "  https://github.com/$REPO/issues"
        echo ""
        echo "现在可以开始使用了！🚀"
    else
        echo "✅ 安装完成: $INSTALL_DIR/$SCRIPT_NAME"
    fi
}

# 主函数
main() {
    check_python
    check_mktorrent
    check_network
    check_existing_installation
    create_directories
    download_and_install
    setup_path
    create_shortcut
    verify_installation
    show_usage
}

# 运行主函数
main "$@"
