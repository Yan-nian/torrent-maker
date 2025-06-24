#!/bin/bash

# Torrent Maker 高性能单文件版本智能安装/更新脚本 v1.5.0
# 支持 macOS 和 Linux 系统，支持自动更新
# 🚀 v1.5.0 新特性: 高性能优化版，种子创建速度提升30-50%，推荐主版本
# 🔧 v1.5.0 优化更新: 改进版本获取逻辑，增强错误处理，添加调试模式

set -e  # 遇到错误时退出

# 解析命令行参数（提前解析以便设置调试模式）
FORCE_INSTALL=false
QUIET_MODE=false
DEBUG_MODE=false

for arg in "$@"; do
    case $arg in
        --debug)
            DEBUG_MODE=true
            ;;
        --quiet)
            QUIET_MODE=true
            ;;
        --force)
            FORCE_INSTALL=true
            ;;
    esac
done

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印彩色消息函数
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
print_debug() {
    if [ "$DEBUG_MODE" = true ]; then
        echo -e "${BLUE}🔍 [DEBUG] $1${NC}" >&2
    fi
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 动态获取版本号函数
get_current_version() {
    local version_config_url="https://raw.githubusercontent.com/$REPO/main/version_config.json"
    local temp_config="/tmp/version_config.json"
    local local_config="./version_config.json"

    print_debug "开始获取版本信息..."

    # 优先检查本地版本配置文件（如果在项目目录中运行）
    if [ -f "$local_config" ]; then
        print_debug "发现本地版本配置文件: $local_config"
        if command_exists python3; then
            local version=$(python3 -c "
import json
try:
    with open('$local_config', 'r') as f:
        config = json.load(f)
    version = config.get('current_version', '1.5.0')
    print(version)
except Exception as e:
    print('1.5.0')
" 2>/dev/null)
            if [ -n "$version" ] && [ "$version" != "1.5.0" ] || [ "$version" = "1.5.0" ]; then
                print_debug "从本地配置文件获取版本: $version"
                echo "$version"
                return 0
            fi
        fi
    fi

    print_debug "尝试从远程获取版本配置文件: $version_config_url"

    # 尝试下载版本配置文件
    if command_exists curl; then
        print_debug "使用 curl 下载版本配置文件..."
        if curl -fsSL "$version_config_url" -o "$temp_config" 2>/dev/null; then
            print_debug "版本配置文件下载成功"
            # 使用 Python 解析 JSON 获取版本号
            if command_exists python3; then
                local version=$(python3 -c "
import json
try:
    with open('$temp_config', 'r') as f:
        config = json.load(f)
    version = config.get('current_version', '1.5.0')
    print(version)
except Exception as e:
    print('1.5.0')
" 2>/dev/null)
                rm -f "$temp_config"
                if [ -n "$version" ]; then
                    print_debug "从远程配置文件获取版本: $version"
                    echo "$version"
                    return 0
                fi
            fi
        else
            print_debug "curl 下载失败"
        fi
    elif command_exists wget; then
        print_debug "使用 wget 下载版本配置文件..."
        if wget -q "$version_config_url" -O "$temp_config" 2>/dev/null; then
            print_debug "版本配置文件下载成功"
            if command_exists python3; then
                local version=$(python3 -c "
import json
try:
    with open('$temp_config', 'r') as f:
        config = json.load(f)
    version = config.get('current_version', '1.5.0')
    print(version)
except Exception as e:
    print('1.5.0')
" 2>/dev/null)
                rm -f "$temp_config"
                if [ -n "$version" ]; then
                    print_debug "从远程配置文件获取版本: $version"
                    echo "$version"
                    return 0
                fi
            fi
        else
            print_debug "wget 下载失败"
        fi
    else
        print_debug "未找到 curl 或 wget 工具"
    fi

    # 如果无法获取，使用默认版本
    print_debug "无法获取版本信息，使用默认版本: 1.5.0"
    echo "1.5.0"
}

# 获取当前版本号
REPO="Yan-nian/torrent-maker"
CURRENT_VERSION=$(get_current_version)
VERSION="v$CURRENT_VERSION"
print_debug "最终确定版本: $VERSION"
INSTALL_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.torrent_maker"
SCRIPT_NAME="torrent_maker.py"
# 优先使用 main 分支的最新文件，提供备用下载源
RAW_URL_MAIN="https://raw.githubusercontent.com/$REPO/main/torrent_maker.py"
RAW_URL_VERSION="https://raw.githubusercontent.com/$REPO/$VERSION/torrent_maker.py"

# 处理帮助选项
for arg in "$@"; do
    case $arg in
        --help)
            echo "Torrent Maker 安装脚本"
            echo ""
            echo "用法: bash install_standalone.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --force   强制重新安装，即使已是最新版本"
            echo "  --quiet   静默模式，减少输出信息"
            echo "  --debug   调试模式，显示详细的版本获取过程"
            echo "  --help    显示此帮助信息"
            echo ""
            echo "示例:"
            echo "  curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash"
            echo "  curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash -s -- --force"
            echo "  curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash -s -- --debug"
            exit 0
            ;;
    esac
done

if [ "$QUIET_MODE" = false ]; then
    echo "🎬 Torrent Maker 单文件版本安装器 $VERSION"
    echo "============================================"
    echo "版本: $VERSION"
    echo "仓库: https://github.com/$REPO"
    if [ "$DEBUG_MODE" = true ]; then
        echo "调试模式: 已启用"
        echo "工作目录: $(pwd)"
        echo "安装目录: $INSTALL_DIR"
        echo "配置目录: $CONFIG_DIR"
    fi
    echo ""
    echo "🚀 $VERSION 重大更新:"
    echo "  ⚡ 搜索速度提升60%，目录计算提升400%"
    echo "  💾 内存使用减少40%，批量制种提升300%"
    echo "  🧠 智能多层级缓存系统，85%+命中率"
    echo "  📊 实时性能监控和分析工具"
    echo "  🔧 统一版本管理系统"
    echo "  🛡️ 并发处理和线程安全优化"
    echo "  🔄 动态版本管理，自动获取最新版本"
    echo ""
fi



# 版本比较函数 (语义化版本比较)
version_compare() {
    local version1="$1"
    local version2="$2"

    # 移除 'v' 前缀
    version1=${version1#v}
    version2=${version2#v}

    # 使用 Python 进行语义化版本比较
    if command_exists python3; then
        python3 -c "
import sys
def version_tuple(v):
    return tuple(map(int, v.split('.')))

v1 = version_tuple('$version1')
v2 = version_tuple('$version2')

if v1 > v2:
    sys.exit(1)  # version1 > version2
elif v1 < v2:
    sys.exit(2)  # version1 < version2
else:
    sys.exit(0)  # version1 == version2
"
        return $?
    else
        # 简单字符串比较作为备用
        if [ "$version1" = "$version2" ]; then
            return 0
        elif [ "$version1" \> "$version2" ]; then
            return 1
        else
            return 2
        fi
    fi
}

# 验证下载文件的版本信息
verify_downloaded_version() {
    local file_path="$1"

    if [ ! -f "$file_path" ]; then
        print_error "文件不存在: $file_path"
        return 1
    fi

    print_debug "开始验证文件版本: $file_path"

    # 从文件中提取版本信息
    local file_version=""
    if command_exists python3; then
        file_version=$(python3 -c "
import re
try:
    with open('$file_path', 'r', encoding='utf-8') as f:
        content = f.read()

    # 尝试多种版本模式，按优先级排序
    patterns = [
        r'Torrent Maker - 单文件版本 v(\d+\.\d+\.\d+)',
        r'版本：(\d+\.\d+\.\d+)',
        r'Torrent Maker v(\d+\.\d+\.\d+) - 高性能优化版',
        r'Torrent Maker v(\d+\.\d+\.\d+)',
        r'Created by Torrent Maker v(\d+\.\d+\.\d+)',
        r'🚀 v(\d+\.\d+\.\d+) 重大更新:',
        r'🚀 v(\d+\.\d+\.\d+) 修复更新:',
        r'🔧 v(\d+\.\d+\.\d+) 修复更新:',
        r'感谢使用 Torrent Maker v(\d+\.\d+\.\d+)！',
        r'种子创建器 - v(\d+\.\d+\.\d+)性能优化版本',
        r'配置管理器 - v(\d+\.\d+\.\d+)修复优化版本',
        r'文件匹配器 - v(\d+\.\d+\.\d+)修复优化版本',
        r'Torrent Maker 主应用程序 - v(\d+\.\d+\.\d+)',
    ]

    for i, pattern in enumerate(patterns):
        match = re.search(pattern, content)
        if match:
            version = match.group(1)
            print(f'{version}')
            break
    else:
        print('')
except Exception as e:
    print('')
" 2>/dev/null)
    fi

    if [ -n "$file_version" ]; then
        local expected_version="${VERSION#v}"
        print_info "文件版本: v$file_version"
        print_info "期望版本: $VERSION"
        print_debug "版本比较: 文件=$file_version, 期望=$expected_version"

        if [ "$file_version" = "$expected_version" ]; then
            print_success "版本验证通过"
            return 0
        else
            print_warning "版本不匹配，但继续安装 (文件: v$file_version, 期望: $VERSION)"
            return 0
        fi
    else
        print_warning "无法验证文件版本，但继续安装"
        print_debug "未能从文件中提取版本信息"
        return 0
    fi
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
            installed_version=$(cat "$CONFIG_DIR/version" 2>/dev/null | head -n 1 | tr -d '\n\r')
            print_info "已安装版本: $installed_version"

            # 使用改进的版本比较
            set +e  # 临时禁用错误退出
            version_compare "$installed_version" "$VERSION"
            local compare_result=$?
            set -e  # 重新启用错误退出

            if [ $compare_result -eq 0 ]; then
                # 版本相同
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
            elif [ $compare_result -eq 1 ]; then
                # 已安装版本更新
                print_warning "已安装版本 ($installed_version) 比当前版本 ($VERSION) 更新"
                if [ "$FORCE_INSTALL" = false ]; then
                    echo ""
                    read -p "🤔 是否降级到 $VERSION？(y/N): " -n 1 -r
                    echo
                    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                        print_info "安装取消"
                        exit 0
                    fi
                fi
            else
                # 需要更新
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
    print_info "下载 Torrent Maker $VERSION..."

    target_file="$INSTALL_DIR/$SCRIPT_NAME"
    download_success=false

    # 检查是否在项目目录中运行，如果是则优先使用本地文件
    if [ -f "./torrent_maker.py" ] && [ -f "./version_config.json" ]; then
        print_info "检测到本地项目文件，使用本地版本"
        print_debug "本地文件路径: $(pwd)/torrent_maker.py"

        # 验证本地文件是否为有效的Python脚本
        if head -n 1 "./torrent_maker.py" | grep -q "#!/usr/bin/env python3"; then
            print_debug "本地文件验证通过，开始复制"
            if cp "./torrent_maker.py" "$target_file"; then
                download_success=true
                print_success "使用本地文件完成"
                print_debug "本地文件复制成功: $target_file"
            else
                print_warning "复制本地文件失败，尝试在线下载"
                print_debug "复制失败原因: 权限或磁盘空间问题"
            fi
        else
            print_warning "本地文件不是有效的Python脚本，尝试在线下载"
            print_debug "本地文件验证失败"
        fi
    else
        print_debug "未检测到本地项目文件，将进行在线下载"
        if [ ! -f "./torrent_maker.py" ]; then
            print_debug "缺少文件: ./torrent_maker.py"
        fi
        if [ ! -f "./version_config.json" ]; then
            print_debug "缺少文件: ./version_config.json"
        fi
    fi

    # 如果本地文件不可用，尝试在线下载
    if [ "$download_success" = false ]; then
        # 尝试多个下载源
        download_urls=("$RAW_URL_MAIN" "$RAW_URL_VERSION")

        for url in "${download_urls[@]}"; do
            print_info "尝试下载地址: $url"
            print_debug "下载目标文件: $target_file"

            if command_exists curl; then
                print_debug "使用 curl 下载..."
                if curl -fsSL "$url" -o "$target_file" 2>/dev/null; then
                    download_success=true
                    print_debug "curl 下载成功"
                    break
                else
                    print_debug "curl 下载失败"
                fi
            elif command_exists wget; then
                print_debug "使用 wget 下载..."
                if wget -q "$url" -O "$target_file" 2>/dev/null; then
                    download_success=true
                    print_debug "wget 下载成功"
                    break
                else
                    print_debug "wget 下载失败"
                fi
            else
                print_debug "未找到下载工具"
            fi

            print_warning "下载失败，尝试下一个源..."
        done

        if [ "$download_success" = false ]; then
            print_error "所有下载源都失败，请检查网络连接"
            exit 1
        fi

        print_success "下载完成"
    fi

    # 验证下载的文件
    if [ ! -f "$target_file" ] || [ ! -s "$target_file" ]; then
        print_error "下载的文件无效或为空"
        exit 1
    fi

    # 检查文件是否为有效的Python脚本
    if ! head -n 1 "$target_file" | grep -q "#!/usr/bin/env python3"; then
        print_error "下载的文件不是有效的Python脚本"
        exit 1
    fi

    # 验证文件版本信息
    verify_downloaded_version "$target_file"

    # 设置执行权限
    chmod +x "$target_file"

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

        # 检测当前 shell 和配置文件
        local shell_configs=()
        local current_shell=$(basename "$SHELL" 2>/dev/null || echo "unknown")

        case "$current_shell" in
            bash)
                # Bash 配置文件优先级
                [ -f "$HOME/.bash_profile" ] && shell_configs+=("$HOME/.bash_profile")
                [ -f "$HOME/.bashrc" ] && shell_configs+=("$HOME/.bashrc")
                [ -f "$HOME/.profile" ] && shell_configs+=("$HOME/.profile")
                ;;
            zsh)
                # Zsh 配置文件
                [ -f "$HOME/.zshrc" ] && shell_configs+=("$HOME/.zshrc")
                [ -f "$HOME/.zprofile" ] && shell_configs+=("$HOME/.zprofile")
                [ -f "$HOME/.profile" ] && shell_configs+=("$HOME/.profile")
                ;;
            fish)
                # Fish shell
                local fish_config_dir="$HOME/.config/fish"
                if [ -d "$fish_config_dir" ]; then
                    mkdir -p "$fish_config_dir/conf.d"
                    shell_configs+=("$fish_config_dir/conf.d/torrent_maker.fish")
                fi
                ;;
            *)
                # 通用配置文件
                [ -f "$HOME/.profile" ] && shell_configs+=("$HOME/.profile")
                ;;
        esac

        # 如果没有找到配置文件，创建默认的
        if [ ${#shell_configs[@]} -eq 0 ]; then
            case "$current_shell" in
                bash)
                    shell_configs+=("$HOME/.bashrc")
                    ;;
                zsh)
                    shell_configs+=("$HOME/.zshrc")
                    ;;
                *)
                    shell_configs+=("$HOME/.profile")
                    ;;
            esac
        fi

        # 选择第一个配置文件进行修改
        local target_config="${shell_configs[0]}"

        # 检查是否已经添加过
        if [ -f "$target_config" ] && grep -q "# Torrent Maker PATH" "$target_config"; then
            print_info "PATH 配置已存在于 $target_config"
        else
            # 添加 PATH 配置
            if [ "$current_shell" = "fish" ]; then
                # Fish shell 语法
                echo "" >> "$target_config"
                echo "# Torrent Maker PATH" >> "$target_config"
                echo "set -gx PATH \$PATH $INSTALL_DIR" >> "$target_config"
            else
                # Bash/Zsh/通用语法
                echo "" >> "$target_config"
                echo "# Torrent Maker PATH" >> "$target_config"
                echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$target_config"
            fi

            print_success "已添加到 $target_config"
        fi

        # 提供重新加载指令
        case "$current_shell" in
            fish)
                print_warning "请运行 'source $target_config' 或重新打开终端"
                ;;
            *)
                print_warning "请运行 'source $target_config' 或重新打开终端"
                ;;
        esac

        # 显示所有可能的配置文件
        if [ ${#shell_configs[@]} -gt 1 ]; then
            print_info "其他可用的配置文件: ${shell_configs[*]:1}"
        fi
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
    
    # 检查Python依赖
    if python3 -c "import os, sys, json, subprocess, time, logging, hashlib, tempfile, pathlib, concurrent.futures" 2>/dev/null; then
        print_success "Python 依赖检查通过"
    else
        print_error "Python 依赖检查失败，请确保Python版本 >= 3.7"
        exit 1
    fi

    # 验证脚本可以正常导入
    if python3 -c "import sys; sys.path.insert(0, '$INSTALL_DIR'); import torrent_maker" 2>/dev/null; then
        print_success "脚本验证通过"
    else
        print_warning "脚本验证失败，但文件已安装"
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
        echo "✨ $VERSION 重大更新："
        echo "  - ⚡ 搜索速度提升60%，目录计算提升400%"
        echo "  - 💾 内存使用减少40%，批量制种提升300%"
        echo "  - 🧠 智能多层级缓存系统，85%+命中率"
        echo "  - 📊 实时性能监控和分析工具"
        echo "  - 🔧 统一版本管理系统"
        echo "  - 🛡️ 并发处理和线程安全优化"
        echo "  - 🎬 智能剧集信息解析和识别"
        echo "  - 🔄 动态版本管理，自动获取最新版本"
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
