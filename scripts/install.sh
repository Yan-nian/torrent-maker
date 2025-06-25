#!/usr/bin/env bash
# shellcheck shell=bash

# =============================================================================
# Torrent Maker 安装脚本 v2.0
#
# 现代化、可靠、功能完善的单文件种子制作工具安装器
# =============================================================================

set -eo pipefail

# 应用信息
readonly APP_NAME="torrent-maker"
readonly APP_DISPLAY_NAME="Torrent Maker"
readonly SCRIPT_NAME="torrent_maker.py"
readonly REPO_OWNER="Yan-nian"
readonly REPO_NAME="torrent-maker"
readonly GITHUB_REPO="${REPO_OWNER}/${REPO_NAME}"

# 默认配置
readonly DEFAULT_VERSION="1.7.0"
readonly DEFAULT_INSTALL_DIR="$HOME/.local/bin"
readonly DEFAULT_CONFIG_DIR="$HOME/.torrent_maker"

# 网络配置
readonly GITHUB_API_BASE="https://api.github.com"
readonly GITHUB_RAW_BASE="https://raw.githubusercontent.com"
readonly DOWNLOAD_TIMEOUT=30
readonly MAX_RETRIES=3

# 颜色定义
if [[ -z "${NO_COLOR:-}" ]] && [[ -t 1 ]]; then
    COLOR_RED='\033[0;31m'
    COLOR_GREEN='\033[0;32m'
    COLOR_YELLOW='\033[1;33m'
    COLOR_BLUE='\033[0;34m'
    COLOR_CYAN='\033[0;36m'
    COLOR_WHITE='\033[1;37m'
    COLOR_RESET='\033[0m'
    COLOR_BOLD='\033[1m'
else
    COLOR_RED=''
    COLOR_GREEN=''
    COLOR_YELLOW=''
    COLOR_BLUE=''
    COLOR_CYAN=''
    COLOR_WHITE=''
    COLOR_RESET=''
    COLOR_BOLD=''
fi

# 全局变量
INSTALL_DIR=""
CONFIG_DIR=""
TARGET_VERSION=""
FORCE_INSTALL=false
QUIET_MODE=false
DEBUG_MODE=false

# 日志函数
log_debug() {
    [[ $DEBUG_MODE == true ]] && echo -e "[DEBUG] $*" >&2
}

log_info() {
    echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET} $*" >&2
}

log_warn() {
    echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $*" >&2
}

log_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $*" >&2
}

# 用户友好的输出函数
print_header() {
    if [[ $QUIET_MODE == false ]]; then
        echo -e "${COLOR_CYAN}${COLOR_BOLD}"
        echo "🎬 ============================================================"
        echo "   $APP_DISPLAY_NAME 安装器 v2.0"
        echo "   现代化、可靠、功能完善的单文件种子制作工具"
        echo "============================================================${COLOR_RESET}"
        echo
    fi
}

print_success() {
    [[ $QUIET_MODE == false ]] && echo -e "${COLOR_GREEN}✅ $*${COLOR_RESET}"
}

print_info() {
    [[ $QUIET_MODE == false ]] && echo -e "${COLOR_BLUE}ℹ️  $*${COLOR_RESET}"
}

print_warning() {
    [[ $QUIET_MODE == false ]] && echo -e "${COLOR_YELLOW}⚠️  $*${COLOR_RESET}"
}

print_error() {
    echo -e "${COLOR_RED}❌ $*${COLOR_RESET}" >&2
}

print_step() {
    if [[ "${QUIET_MODE:-false}" == "false" ]]; then
        echo -e "${COLOR_WHITE}${COLOR_BOLD}▶ $*${COLOR_RESET}"
    fi
    return 0
}

# 检查命令是否存在
has_command() {
    command -v "$1" >/dev/null 2>&1
}

# 安全地创建目录
safe_mkdir() {
    local dir="$1"
    local mode="${2:-755}"
    
    if [[ ! -d "$dir" ]]; then
        log_debug "创建目录: $dir (权限: $mode)"
        if ! mkdir -p "$dir"; then
            print_error "无法创建目录: $dir"
            exit 1
        fi
        chmod "$mode" "$dir" || {
            print_error "无法设置目录权限: $dir"
            exit 1
        }
    fi
}

# 智能下载函数
smart_download() {
    local url="$1"
    local output="$2"
    local description="${3:-文件}"
    
    log_debug "下载 $description: $url -> $output"
    
    # 确保输出目录存在
    local output_dir
    output_dir="$(dirname "$output")"
    safe_mkdir "$output_dir"
    
    # 选择下载工具
    local download_cmd=()
    if has_command curl; then
        download_cmd=(curl -sSfL --connect-timeout "$DOWNLOAD_TIMEOUT" -o "$output" "$url")
    elif has_command wget; then
        download_cmd=(wget -q --timeout="$DOWNLOAD_TIMEOUT" -O "$output" "$url")
    else
        print_error "需要 curl 或 wget 来下载文件"
        exit 1
    fi
    
    # 执行下载
    if "${download_cmd[@]}"; then
        # 验证下载的文件
        if [[ ! -f "$output" ]] || [[ ! -s "$output" ]]; then
            print_error "下载的文件无效: $output"
            rm -f "$output"
            return 1
        fi
        log_debug "下载成功: $output ($(wc -c < "$output") 字节)"
        return 0
    else
        print_error "下载失败: $description"
        rm -f "$output"
        return 1
    fi
}

# 获取目标版本
get_target_version() {
    if [[ -n "$TARGET_VERSION" ]]; then
        echo "$TARGET_VERSION"
        return 0
    fi
    
    echo "$DEFAULT_VERSION"
}

# 获取下载 URL
get_download_url() {
    local version="$1"
    echo "$GITHUB_RAW_BASE/$GITHUB_REPO/main/$SCRIPT_NAME"
}

# 检查 Python 环境
check_python() {
    print_step "检查 Python 环境"
    
    if ! has_command python3; then
        print_error "Python 3 未安装"
        echo "请安装 Python 3.7 或更高版本"
        exit 1
    fi
    
    local python_version
    python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>/dev/null || echo "0.0")
    
    print_info "检测到 Python 版本: $python_version"
    
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)" 2>/dev/null; then
        print_success "Python 版本符合要求 (>= 3.7)"
    else
        print_error "Python 版本过低，需要 Python 3.7 或更高版本"
        exit 1
    fi
}

# 检查 mktorrent
check_mktorrent() {
    print_step "检查 mktorrent"
    
    if has_command mktorrent; then
        print_success "mktorrent 已安装"
        return 0
    fi
    
    print_warning "mktorrent 未安装，正在尝试自动安装..."
    
    case "$(uname -s)" in
        Darwin*)
            if has_command brew; then
                print_info "使用 Homebrew 安装 mktorrent..."
                brew install mktorrent
            else
                print_error "需要 Homebrew 来安装 mktorrent"
                exit 1
            fi
            ;;
        Linux*)
            if has_command apt-get; then
                print_info "使用 apt 安装 mktorrent..."
                sudo apt-get update && sudo apt-get install -y mktorrent
            elif has_command yum; then
                print_info "使用 yum 安装 mktorrent..."
                sudo yum install -y mktorrent
            elif has_command dnf; then
                print_info "使用 dnf 安装 mktorrent..."
                sudo dnf install -y mktorrent
            else
                print_error "请手动安装 mktorrent"
                exit 1
            fi
            ;;
        *)
            print_error "不支持的操作系统，请手动安装 mktorrent"
            exit 1
            ;;
    esac
    
    if ! has_command mktorrent; then
        print_error "mktorrent 安装失败"
        exit 1
    fi
    
    print_success "mktorrent 安装成功"
}

# 下载和安装主程序
download_and_install() {
    local version
    version=$(get_target_version)
    
    print_step "下载 $APP_DISPLAY_NAME v$version"
    
    # 创建必要的目录
    safe_mkdir "$INSTALL_DIR"
    safe_mkdir "$CONFIG_DIR"
    
    local target_file="$INSTALL_DIR/$SCRIPT_NAME"
    
    # 优先使用本地文件
    if [[ -f "./$SCRIPT_NAME" ]] && [[ "$FORCE_INSTALL" == false ]]; then
        print_info "检测到本地文件，使用本地版本"
        cp "./$SCRIPT_NAME" "$target_file"
    else
        # 从 GitHub 下载
        local download_url
        download_url=$(get_download_url "$version")
        
        print_info "从 GitHub 下载: $download_url"
        
        if ! smart_download "$download_url" "$target_file" "$APP_DISPLAY_NAME v$version"; then
            exit 1
        fi
    fi
    
    # 设置执行权限
    chmod +x "$target_file"
    
    # 保存版本信息
    echo "v$version" > "$CONFIG_DIR/version"
    
    print_success "安装完成: $APP_DISPLAY_NAME v$version"
    return 0
}

# 验证安装结果
verify_installation() {
    print_step "验证安装"
    
    local target_file="$INSTALL_DIR/$SCRIPT_NAME"
    
    if [[ ! -f "$target_file" ]] || [[ ! -x "$target_file" ]]; then
        print_error "安装验证失败"
        return 1
    fi
    
    print_success "安装验证通过"
    return 0
}

# 显示使用说明
show_usage_info() {
    local target_file="$1"
    local version
    version=$(get_target_version)
    
    if [[ $QUIET_MODE == false ]]; then
        echo
        print_success "🎉 $APP_DISPLAY_NAME v$version 安装成功！"
        echo "=============================================="
        echo
        echo "📋 使用方法："
        echo "  python3 $target_file"
        echo
        echo "📁 配置目录: $CONFIG_DIR"
        echo "📄 程序位置: $target_file"
        echo
        echo "🚀 现在可以开始使用了！"
        echo
    fi
}

# 主函数
main() {
    print_header
    
    # 检查依赖
    check_python
    check_mktorrent
    
    # 下载和安装
    if download_and_install && verify_installation; then
        show_usage_info "$INSTALL_DIR/$SCRIPT_NAME"
    else
        print_error "安装失败"
        exit 1
    fi
}

# 参数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            echo "用法: $0 [选项]"
            echo "选项:"
            echo "  -h, --help     显示帮助信息"
            echo "  -v, --version  指定版本"
            echo "  -f, --force    强制重新安装"
            echo "  -q, --quiet    静默模式"
            echo "  --debug        调试模式"
            exit 0
            ;;
        -v|--version)
            TARGET_VERSION="$2"
            shift 2
            ;;
        -f|--force)
            FORCE_INSTALL=true
            shift
            ;;
        -q|--quiet)
            QUIET_MODE=true
            shift
            ;;
        --debug)
            DEBUG_MODE=true
            shift
            ;;
        *)
            print_error "未知参数: $1"
            exit 1
            ;;
    esac
done

# 设置默认值
INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"
CONFIG_DIR="${CONFIG_DIR:-$DEFAULT_CONFIG_DIR}"

# 运行主函数
main
