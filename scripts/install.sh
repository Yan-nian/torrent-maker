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
readonly DEFAULT_VERSION="1.7.1"
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

# 从文件中提取版本号
extract_version_from_file() {
    local file_path="$1"
    local version=""

    if [[ ! -f "$file_path" ]]; then
        log_debug "文件不存在: $file_path"
        return 1
    fi

    # 使用正则表达式提取 VERSION = "x.y.z" 格式的版本号
    version=$(grep -E '^[[:space:]]*VERSION[[:space:]]*=[[:space:]]*["\'"'"']([^"'"'"']+)["\'"'"']' "$file_path" 2>/dev/null | \
              sed -E 's/^[[:space:]]*VERSION[[:space:]]*=[[:space:]]*["\'"'"']([^"'"'"']+)["\'"'"'].*/\1/' | \
              head -1)

    if [[ -n "$version" ]]; then
        log_debug "从文件 $file_path 提取到版本: $version"
        echo "$version"
        return 0
    else
        log_debug "无法从文件 $file_path 提取版本号"
        return 1
    fi
}

# 从远程文件获取版本号
get_remote_version() {
    local remote_url="$GITHUB_RAW_BASE/$GITHUB_REPO/main/$SCRIPT_NAME"
    local temp_file
    temp_file=$(mktemp)

    log_debug "从远程获取版本: $remote_url"

    # 下载远程文件到临时位置
    if smart_download "$remote_url" "$temp_file" "远程版本检测"; then
        local version
        if version=$(extract_version_from_file "$temp_file"); then
            rm -f "$temp_file"
            echo "$version"
            return 0
        fi
    fi

    rm -f "$temp_file"
    log_debug "无法从远程获取版本号"
    return 1
}

# 版本比较函数 (语义化版本比较)
compare_versions() {
    local version1="$1"
    local version2="$2"

    # 移除可能的 'v' 前缀
    version1="${version1#v}"
    version2="${version2#v}"

    # 分割版本号
    IFS='.' read -ra v1_parts <<< "$version1"
    IFS='.' read -ra v2_parts <<< "$version2"

    # 补齐版本号位数
    while [[ ${#v1_parts[@]} -lt 3 ]]; do v1_parts+=(0); done
    while [[ ${#v2_parts[@]} -lt 3 ]]; do v2_parts+=(0); done

    # 逐位比较
    for i in {0..2}; do
        if [[ ${v1_parts[i]} -gt ${v2_parts[i]} ]]; then
            return 1  # version1 > version2
        elif [[ ${v1_parts[i]} -lt ${v2_parts[i]} ]]; then
            return 2  # version1 < version2
        fi
    done

    return 0  # version1 == version2
}

# 获取目标版本 (改进版)
get_target_version() {
    local version=""

    # 优先级1: 用户指定版本
    if [[ -n "$TARGET_VERSION" ]]; then
        log_debug "使用用户指定版本: $TARGET_VERSION"
        echo "$TARGET_VERSION"
        return 0
    fi

    # 优先级2: 本地文件版本
    if [[ -f "./$SCRIPT_NAME" ]] && version=$(extract_version_from_file "./$SCRIPT_NAME"); then
        log_debug "使用本地文件版本: $version"
        echo "$version"
        return 0
    fi

    # 优先级3: 远程文件版本
    if version=$(get_remote_version); then
        log_debug "使用远程文件版本: $version"
        echo "$version"
        return 0
    fi

    # 优先级4: 默认版本
    log_debug "使用默认版本: $DEFAULT_VERSION"
    echo "$DEFAULT_VERSION"
    return 0
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

# 检查已安装版本
get_installed_version() {
    local version_file="$CONFIG_DIR/version"

    if [[ -f "$version_file" ]]; then
        local installed_version
        installed_version=$(cat "$version_file" 2>/dev/null | sed 's/^v//')
        if [[ -n "$installed_version" ]]; then
            echo "$installed_version"
            return 0
        fi
    fi

    return 1
}

# 检查是否需要更新
check_for_updates() {
    local current_version="$1"
    local latest_version="$2"

    if [[ -z "$current_version" ]] || [[ -z "$latest_version" ]]; then
        return 1
    fi

    compare_versions "$current_version" "$latest_version"
    local result=$?

    if [[ $result -eq 2 ]]; then
        # current < latest，需要更新
        return 0
    else
        # current >= latest，不需要更新
        return 1
    fi
}

# 下载和安装主程序 (改进版)
download_and_install() {
    local version
    version=$(get_target_version)
    local actual_version=""

    print_step "准备安装 $APP_DISPLAY_NAME v$version"

    # 检查是否已安装以及是否需要更新
    local installed_version
    if installed_version=$(get_installed_version) && [[ "$FORCE_INSTALL" == false ]]; then
        print_info "检测到已安装版本: v$installed_version"

        if check_for_updates "$installed_version" "$version"; then
            print_info "发现新版本 v$version，准备更新..."
        else
            print_success "已安装最新版本 v$installed_version"
            if [[ $QUIET_MODE == false ]]; then
                echo
                echo "如需强制重新安装，请使用 --force 参数"
            fi
            return 0
        fi
    fi

    # 创建必要的目录
    safe_mkdir "$INSTALL_DIR"
    safe_mkdir "$CONFIG_DIR"

    local target_file="$INSTALL_DIR/$SCRIPT_NAME"

    # 优先使用本地文件
    if [[ -f "./$SCRIPT_NAME" ]] && [[ "$FORCE_INSTALL" == false ]]; then
        print_info "检测到本地文件，使用本地版本"
        cp "./$SCRIPT_NAME" "$target_file"

        # 从复制的文件中提取实际版本号
        if actual_version=$(extract_version_from_file "$target_file"); then
            version="$actual_version"
            print_info "本地文件版本: v$version"
        fi
    else
        # 从 GitHub 下载
        local download_url
        download_url=$(get_download_url "$version")

        print_info "从 GitHub 下载: $download_url"

        if ! smart_download "$download_url" "$target_file" "$APP_DISPLAY_NAME v$version"; then
            exit 1
        fi

        # 从下载的文件中提取实际版本号
        if actual_version=$(extract_version_from_file "$target_file"); then
            version="$actual_version"
            print_info "下载文件版本: v$version"
        fi
    fi

    # 设置执行权限
    chmod +x "$target_file"

    # 保存实际版本信息
    echo "v$version" > "$CONFIG_DIR/version"

    # 记录安装历史
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local install_method="本地文件"
    if [[ ! -f "./$SCRIPT_NAME" ]] || [[ "$FORCE_INSTALL" == true ]]; then
        install_method="GitHub下载"
    fi
    echo "[$timestamp] 安装 Torrent Maker v$version ($install_method)" >> "$CONFIG_DIR/install_history.log"

    print_success "安装完成: $APP_DISPLAY_NAME v$version"
    return 0
}

# 验证安装结果 (改进版)
verify_installation() {
    print_step "验证安装"

    local target_file="$INSTALL_DIR/$SCRIPT_NAME"

    # 检查文件存在性和可执行性
    if [[ ! -f "$target_file" ]] || [[ ! -x "$target_file" ]]; then
        print_error "安装验证失败: 文件不存在或无执行权限"
        return 1
    fi

    # 验证文件内容（检查是否为有效的Python文件）
    if ! head -1 "$target_file" | grep -q "python"; then
        print_warning "警告: 文件可能不是有效的Python脚本"
    fi

    # 验证版本信息
    local file_version
    if file_version=$(extract_version_from_file "$target_file"); then
        print_info "验证版本: v$file_version"
    else
        print_warning "警告: 无法从安装文件中提取版本信息"
    fi

    print_success "安装验证通过"
    return 0
}

# 显示使用说明 (改进版)
show_usage_info() {
    local target_file="$1"
    local installed_version

    # 获取实际安装的版本
    if installed_version=$(get_installed_version); then
        # 从安装文件中再次确认版本
        local file_version
        if file_version=$(extract_version_from_file "$target_file"); then
            installed_version="$file_version"
        fi
    else
        installed_version=$(get_target_version)
    fi

    if [[ $QUIET_MODE == false ]]; then
        echo
        print_success "🎉 $APP_DISPLAY_NAME v$installed_version 安装成功！"
        echo "=============================================="
        echo
        echo "📋 使用方法："
        echo "  python3 $target_file"
        echo
        echo "📁 配置目录: $CONFIG_DIR"
        echo "📄 程序位置: $target_file"
        echo "📊 安装版本: v$installed_version"
        echo
        echo "🚀 现在可以开始使用了！"
        echo

        # 显示版本历史（如果存在）
        local history_file="$CONFIG_DIR/install_history.log"
        if [[ -f "$history_file" ]]; then
            local history_count
            history_count=$(wc -l < "$history_file" 2>/dev/null || echo "0")
            if [[ $history_count -gt 1 ]]; then
                echo "📜 安装历史: 共 $history_count 次安装"
                echo "   最近安装: $(tail -1 "$history_file" 2>/dev/null | cut -d']' -f1 | tr -d '[')"
            fi
        fi

        # 显示系统信息
        echo
        echo "🖥️  系统信息:"
        echo "   操作系统: $(uname -s) $(uname -r)"
        echo "   Python版本: $(python3 --version 2>/dev/null | cut -d' ' -f2)"
        if has_command mktorrent; then
            local mktorrent_version
            mktorrent_version=$(mktorrent --help 2>&1 | head -1 | grep -o 'mktorrent [0-9.]*' || echo "mktorrent (版本未知)")
            echo "   mktorrent: $mktorrent_version"
        fi
    fi
}

# 显示更新提示
show_update_hint() {
    if [[ $QUIET_MODE == true ]]; then
        return 0
    fi

    local current_version
    if current_version=$(get_installed_version); then
        local latest_version
        if latest_version=$(get_remote_version); then
            if check_for_updates "$current_version" "$latest_version"; then
                echo
                print_info "💡 发现新版本 v$latest_version 可用！"
                echo "   运行以下命令更新："
                echo "   curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/scripts/install.sh | bash"
                echo
            fi
        fi
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

        # 如果不是强制安装，显示更新提示
        if [[ "$FORCE_INSTALL" == false ]]; then
            show_update_hint
        fi
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
