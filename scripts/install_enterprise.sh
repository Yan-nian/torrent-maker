#!/usr/bin/env bash
# shellcheck shell=bash
# shellcheck disable=SC2039

# =============================================================================
# Torrent Maker 企业级安装脚本 v2.0
#
# 基于现代化 shell 编程最佳实践，参考 nvm、uv 等优秀项目
# 支持多平台、多版本、错误恢复、状态管理等高级功能
# =============================================================================

# 严格模式：遇到错误立即退出，管道中任何命令失败都报错
# 注意：暂时不使用 -u 选项以避免未定义变量问题
set -eo pipefail

# =============================================================================
# 全局配置和常量定义
# =============================================================================

# 应用信息
readonly APP_NAME="torrent-maker"
readonly APP_DISPLAY_NAME="Torrent Maker"
readonly SCRIPT_NAME="torrent_maker.py"
readonly REPO_OWNER="Yan-nian"
readonly REPO_NAME="torrent-maker"
readonly GITHUB_REPO="${REPO_OWNER}/${REPO_NAME}"

# 默认配置
readonly DEFAULT_VERSION="1.9.18"
readonly DEFAULT_INSTALL_DIR="$HOME/.local/bin"
readonly DEFAULT_CONFIG_DIR="$HOME/.torrent_maker"

# 网络配置
readonly GITHUB_API_BASE="https://api.github.com"
readonly GITHUB_RAW_BASE="https://raw.githubusercontent.com"
readonly DOWNLOAD_TIMEOUT=30
readonly MAX_RETRIES=3

# 日志级别
readonly LOG_LEVEL_DEBUG=0
readonly LOG_LEVEL_INFO=1
readonly LOG_LEVEL_WARN=2
readonly LOG_LEVEL_ERROR=3

# 颜色定义（支持 NO_COLOR 环境变量）
if [[ -z "${NO_COLOR:-}" ]] && [[ -t 1 ]]; then
    COLOR_RED='\033[0;31m'
    COLOR_GREEN='\033[0;32m'
    COLOR_YELLOW='\033[1;33m'
    COLOR_BLUE='\033[0;34m'
    COLOR_PURPLE='\033[0;35m'
    COLOR_CYAN='\033[0;36m'
    COLOR_WHITE='\033[1;37m'
    COLOR_RESET='\033[0m'
    COLOR_BOLD='\033[1m'
else
    COLOR_RED=''
    COLOR_GREEN=''
    COLOR_YELLOW=''
    COLOR_BLUE=''
    COLOR_PURPLE=''
    COLOR_CYAN=''
    COLOR_WHITE=''
    COLOR_RESET=''
    COLOR_BOLD=''
fi

# 全局变量（运行时设置）
INSTALL_DIR=""
CONFIG_DIR=""
TARGET_VERSION=""
FORCE_INSTALL=false
QUIET_MODE=false
DEBUG_MODE=false
CURRENT_LOG_LEVEL=$LOG_LEVEL_INFO
TEMP_DIR=""
INSTALL_LOCK_FILE=""

# =============================================================================
# 日志和输出函数
# =============================================================================

# 日志函数
log_debug() {
    [[ $CURRENT_LOG_LEVEL -le $LOG_LEVEL_DEBUG ]] && echo -e "${COLOR_PURPLE}[DEBUG]${COLOR_RESET} $*" >&2
}

log_info() {
    [[ $CURRENT_LOG_LEVEL -le $LOG_LEVEL_INFO ]] && echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET} $*" >&2
}

log_warn() {
    [[ $CURRENT_LOG_LEVEL -le $LOG_LEVEL_WARN ]] && echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $*" >&2
}

log_error() {
    [[ $CURRENT_LOG_LEVEL -le $LOG_LEVEL_ERROR ]] && echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $*" >&2
}

# 用户友好的输出函数
print_header() {
    if [[ $QUIET_MODE == false ]]; then
        echo -e "${COLOR_CYAN}${COLOR_BOLD}"
        echo "🎬 ============================================================"
        echo "   $APP_DISPLAY_NAME 企业级安装器 v2.0"
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
        echo "▶ $*"
    fi
    return 0
}

# =============================================================================
# 进度显示和状态管理
# =============================================================================

# 进度显示函数
show_progress() {
    local current="$1"
    local total="$2"
    local message="${3:-}"

    if [[ $QUIET_MODE == false ]]; then
        local percentage=$((current * 100 / total))
        local filled=$((percentage / 5))  # 简化为20个字符宽度
        local empty=$((20 - filled))

        # 使用兼容 bash 3.2 的方式构建进度条
        local bar=""
        if [[ $filled -gt 0 ]]; then
            bar=$(printf "%*s" $filled | tr ' ' '=')
        fi
        if [[ $empty -gt 0 ]]; then
            bar="$bar$(printf "%*s" $empty | tr ' ' '-')"
        fi

        echo -e "\r${COLOR_BLUE}[$bar] $percentage% $message${COLOR_RESET}"

        if [[ $current -eq $total ]]; then
            echo  # 额外换行
        fi
    fi
}

# 安装步骤管理
declare -a INSTALL_STEPS=(
    "初始化环境"
    "检查现有安装"
    "检查系统依赖"
    "下载程序文件"
    "验证安装"
    "完成安装"
)

CURRENT_STEP=0
TOTAL_STEPS=${#INSTALL_STEPS[@]}

# 更新安装步骤
update_install_step() {
    local step_name="$1"
    CURRENT_STEP=$((CURRENT_STEP + 1))

    log_debug "安装步骤 $CURRENT_STEP/$TOTAL_STEPS: $step_name"

    # 临时禁用进度条，使用简单的步骤显示
    if [[ $QUIET_MODE == false ]]; then
        print_info "步骤 $CURRENT_STEP/$TOTAL_STEPS: $step_name"
    fi
}

# =============================================================================
# 核心工具函数
# =============================================================================

# 检查命令是否存在
has_command() {
    command -v "$1" >/dev/null 2>&1
}

# 确保命令存在，否则报错退出
ensure_command() {
    local cmd="$1"
    local install_hint="${2:-}"

    if ! has_command "$cmd"; then
        print_error "缺少必需命令: $cmd"
        [[ -n "$install_hint" ]] && echo "  安装提示: $install_hint"
        exit 1
    fi
    log_debug "命令检查通过: $cmd"
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

# 安全地删除文件或目录
safe_remove() {
    local path="$1"

    if [[ -e "$path" ]]; then
        log_debug "删除: $path"
        rm -rf "$path" || {
            log_warn "无法删除: $path"
            return 1
        }
    fi
}

# 检查网络连接
check_network() {
    local test_url="https://api.github.com"
    local timeout=5

    log_debug "检查网络连接: $test_url"

    if has_command curl; then
        if curl -sSf --connect-timeout "$timeout" "$test_url" >/dev/null 2>&1; then
            return 0
        fi
    elif has_command wget; then
        if wget -q --timeout="$timeout" --spider "$test_url" >/dev/null 2>&1; then
            return 0
        fi
    fi

    return 1
}

# 重试执行函数
retry_command() {
    local max_attempts="$1"
    local delay="$2"
    shift 2
    local cmd=("$@")

    local attempt=1
    while [[ $attempt -le $max_attempts ]]; do
        log_debug "执行命令 (尝试 $attempt/$max_attempts): ${cmd[*]}"

        if "${cmd[@]}"; then
            return 0
        fi

        if [[ $attempt -lt $max_attempts ]]; then
            log_warn "命令执行失败，${delay}秒后重试..."
            sleep "$delay"
        fi

        ((attempt++))
    done

    log_error "命令执行失败，已重试 $max_attempts 次: ${cmd[*]}"
    return 1
}

# 获取系统信息
get_os_info() {
    local os_name
    local os_version
    local arch

    # 检测操作系统
    case "$(uname -s)" in
        Darwin*)
            os_name="macOS"
            os_version="$(sw_vers -productVersion 2>/dev/null || echo "unknown")"
            ;;
        Linux*)
            os_name="Linux"
            if [[ -f /etc/os-release ]]; then
                # 安全地读取 os-release 文件
                local pretty_name=""
                local name=""

                # 使用 grep 而不是 source 来避免潜在问题
                if pretty_name=$(grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null | cut -d'=' -f2- | tr -d '"'); then
                    os_version="$pretty_name"
                elif name=$(grep '^NAME=' /etc/os-release 2>/dev/null | cut -d'=' -f2- | tr -d '"'); then
                    os_version="$name"
                else
                    os_version="Linux"
                fi
            else
                os_version="Unknown Linux"
            fi
            ;;
        CYGWIN*|MINGW*|MSYS*)
            os_name="Windows"
            os_version="$(uname -r)"
            ;;
        *)
            os_name="$(uname -s)"
            os_version="$(uname -r)"
            ;;
    esac

    # 检测架构
    arch="$(uname -m)"
    case "$arch" in
        x86_64|amd64) arch="x86_64" ;;
        i386|i686) arch="i386" ;;
        arm64|aarch64) arch="arm64" ;;
        armv7l) arch="armv7" ;;
        *) arch="$arch" ;;
    esac

    echo "$os_name|$os_version|$arch"
}

# 显示系统信息
show_system_info() {
    local info
    if ! info="$(get_os_info)"; then
        log_warn "无法获取系统信息"
        return 1
    fi

    # 使用更兼容的方式解析信息
    local os_name
    local os_version
    local arch

    # 分割字符串（兼容 bash 3.2）
    os_name=$(echo "$info" | cut -d'|' -f1)
    os_version=$(echo "$info" | cut -d'|' -f2)
    arch=$(echo "$info" | cut -d'|' -f3)

    log_info "系统信息: $os_name $os_version ($arch)"
}

# =============================================================================
# 版本管理函数
# =============================================================================

# 从 GitHub API 获取最新版本
get_latest_version_from_api() {
    local api_url="$GITHUB_API_BASE/repos/$GITHUB_REPO/releases/latest"
    local response

    log_debug "获取最新版本: $api_url"

    if has_command curl; then
        response=$(curl -sSf --connect-timeout "$DOWNLOAD_TIMEOUT" "$api_url" 2>/dev/null || echo "")
    elif has_command wget; then
        response=$(wget -qO- --timeout="$DOWNLOAD_TIMEOUT" "$api_url" 2>/dev/null || echo "")
    else
        log_warn "缺少 curl 或 wget，无法获取最新版本"
        return 1
    fi

    if [[ -z "$response" ]]; then
        log_warn "无法获取版本信息，使用默认版本"
        return 1
    fi

    # 使用多种方法解析 JSON
    local version=""

    # 方法1: 使用 python3
    if has_command python3 && [[ -z "$version" ]]; then
        version=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tag = data.get('tag_name', '')
    print(tag.lstrip('v') if tag else '')
except:
    pass
" 2>/dev/null || echo "")
    fi

    # 方法2: 使用 jq
    if has_command jq && [[ -z "$version" ]]; then
        version=$(echo "$response" | jq -r '.tag_name // ""' 2>/dev/null | sed 's/^v//' || echo "")
    fi

    # 方法3: 使用 grep 和 sed
    if [[ -z "$version" ]]; then
        version=$(echo "$response" | grep -o '"tag_name"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' | sed 's/^v//' || echo "")
    fi

    if [[ -n "$version" ]]; then
        echo "$version"
        return 0
    else
        return 1
    fi
}

# 获取目标版本
get_target_version() {
    if [[ -n "$TARGET_VERSION" ]]; then
        echo "$TARGET_VERSION"
        return 0
    fi

    local latest_version
    if latest_version=$(get_latest_version_from_api); then
        echo "$latest_version"
    else
        log_warn "无法获取最新版本，使用默认版本: $DEFAULT_VERSION"
        echo "$DEFAULT_VERSION"
    fi
}

# 验证版本格式
validate_version() {
    local version="$1"

    # 简单的版本格式验证 (x.y.z)
    if [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        return 0
    else
        log_error "无效的版本格式: $version"
        return 1
    fi
}

# =============================================================================
# 下载和网络函数
# =============================================================================

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

    # 带重试的下载
    if retry_command "$MAX_RETRIES" 2 "${download_cmd[@]}"; then
        # 验证下载的文件
        if [[ ! -f "$output" ]] || [[ ! -s "$output" ]]; then
            print_error "下载的文件无效: $output"
            safe_remove "$output"
            return 1
        fi
        log_debug "下载成功: $output ($(wc -c < "$output") 字节)"
        return 0
    else
        print_error "下载失败: $description"
        safe_remove "$output"
        return 1
    fi
}

# 获取下载 URL
get_download_url() {
    local version="$1"
    echo "$GITHUB_RAW_BASE/$GITHUB_REPO/main/$SCRIPT_NAME"
}

# =============================================================================
# 依赖检查和安装函数
# =============================================================================

# 检查 Python 环境
check_python() {
    print_step "检查 Python 环境"

    # 检查 Python 3 是否安装
    if ! has_command python3; then
        print_error "Python 3 未安装"
        echo
        echo "请安装 Python 3.7 或更高版本："
        echo "  macOS:    brew install python3"
        echo "  Ubuntu:   sudo apt install python3"
        echo "  CentOS:   sudo yum install python3"
        echo "  Fedora:   sudo dnf install python3"
        echo "  Arch:     sudo pacman -S python"
        exit 1
    fi

    # 检查 Python 版本
    local python_version
    python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>/dev/null || echo "0.0")

    print_info "检测到 Python 版本: $python_version"

    # 验证版本是否满足要求 (>= 3.7)
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)" 2>/dev/null; then
        print_success "Python 版本符合要求 (>= 3.7)"
    else
        print_error "Python 版本过低，需要 Python 3.7 或更高版本"
        echo "当前版本: $python_version"
        exit 1
    fi

    log_debug "Python 检查完成: $python_version"
}

# 检查 mktorrent
check_mktorrent() {
    print_step "检查 mktorrent"

    if has_command mktorrent; then
        local mktorrent_version
        mktorrent_version=$(mktorrent --help 2>&1 | head -1 | grep -o 'mktorrent [0-9.]*' || echo "mktorrent (版本未知)")
        print_success "mktorrent 已安装: $mktorrent_version"
        return 0
    fi

    print_warning "mktorrent 未安装，正在尝试自动安装..."

    local os_info
    os_info="$(get_os_info)"
    local os_name="${os_info%%|*}"

    case "$os_name" in
        macOS)
            if has_command brew; then
                print_info "使用 Homebrew 安装 mktorrent..."
                if brew install mktorrent; then
                    print_success "mktorrent 安装成功"
                else
                    print_error "Homebrew 安装 mktorrent 失败"
                    exit 1
                fi
            else
                print_error "需要 Homebrew 来安装 mktorrent"
                echo "请先安装 Homebrew: https://brew.sh"
                echo "然后运行: brew install mktorrent"
                exit 1
            fi
            ;;
        Linux)
            if has_command apt-get; then
                print_info "使用 apt 安装 mktorrent..."
                if sudo apt-get update && sudo apt-get install -y mktorrent; then
                    print_success "mktorrent 安装成功"
                else
                    print_error "apt 安装 mktorrent 失败"
                    exit 1
                fi
            elif has_command yum; then
                print_info "使用 yum 安装 mktorrent..."
                if sudo yum install -y mktorrent; then
                    print_success "mktorrent 安装成功"
                else
                    print_error "yum 安装 mktorrent 失败"
                    exit 1
                fi
            elif has_command dnf; then
                print_info "使用 dnf 安装 mktorrent..."
                if sudo dnf install -y mktorrent; then
                    print_success "mktorrent 安装成功"
                else
                    print_error "dnf 安装 mktorrent 失败"
                    exit 1
                fi
            elif has_command pacman; then
                print_info "使用 pacman 安装 mktorrent..."
                if sudo pacman -S --noconfirm mktorrent; then
                    print_success "mktorrent 安装成功"
                else
                    print_error "pacman 安装 mktorrent 失败"
                    exit 1
                fi
            elif has_command zypper; then
                print_info "使用 zypper 安装 mktorrent..."
                if sudo zypper install -y mktorrent; then
                    print_success "mktorrent 安装成功"
                else
                    print_error "zypper 安装 mktorrent 失败"
                    exit 1
                fi
            else
                print_error "不支持的 Linux 发行版，请手动安装 mktorrent"
                echo
                echo "请根据您的发行版安装 mktorrent："
                echo "  Ubuntu/Debian: sudo apt install mktorrent"
                echo "  CentOS/RHEL:   sudo yum install mktorrent"
                echo "  Fedora:        sudo dnf install mktorrent"
                echo "  Arch Linux:    sudo pacman -S mktorrent"
                echo "  openSUSE:      sudo zypper install mktorrent"
                exit 1
            fi
            ;;
        *)
            print_error "不支持的操作系统: $os_name"
            echo "请手动安装 mktorrent 后重新运行此脚本"
            exit 1
            ;;
    esac

    # 验证安装结果
    if ! has_command mktorrent; then
        print_error "mktorrent 安装失败，请手动安装后重新运行此脚本"
        exit 1
    fi

    log_debug "mktorrent 检查完成"
}

# 检查所有依赖
check_dependencies() {
    log_debug "开始检查系统依赖"
    print_step "检查系统依赖"

    # 显示系统信息
    log_debug "开始显示系统信息"
    if show_system_info; then
        log_debug "系统信息显示完成"
    else
        log_debug "系统信息显示失败，继续安装"
    fi

    # 检查网络连接
    log_debug "开始检查网络连接"
    if ! check_network; then
        print_warning "网络连接检查失败，可能影响下载"
    else
        log_debug "网络连接正常"
    fi
    log_debug "网络连接检查完成"

    # 检查必需的依赖
    log_debug "开始检查 Python"
    if check_python; then
        log_debug "Python 检查完成"
    else
        log_debug "Python 检查失败"
        return 1
    fi

    log_debug "开始检查 mktorrent"
    check_mktorrent
    log_debug "mktorrent 检查完成"

    print_success "所有依赖检查完成"
    log_debug "依赖检查函数完成"
}

# =============================================================================
# 安装历史和更新管理
# =============================================================================

# 记录安装历史
record_install_history() {
    local version="$1"
    local install_type="${2:-install}"  # install, upgrade, reinstall
    local history_file="$CONFIG_DIR/install_history.log"

    safe_mkdir "$CONFIG_DIR"

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local system_info
    system_info="$(get_os_info)"

    # 记录安装历史
    echo "[$timestamp] $install_type v$version on $system_info" >> "$history_file"

    log_debug "记录安装历史: $install_type v$version"
}

# 获取安装历史
get_install_history() {
    local history_file="$CONFIG_DIR/install_history.log"

    if [[ -f "$history_file" ]]; then
        tail -10 "$history_file" 2>/dev/null || echo ""
    fi
}

# 检查是否有可用更新
check_for_updates() {
    local current_version="$1"
    local latest_version

    log_debug "检查更新: 当前版本 $current_version"

    if latest_version=$(get_latest_version_from_api); then
        if [[ "$current_version" != "$latest_version" ]]; then
            log_debug "发现新版本: $latest_version"
            return 0
        else
            log_debug "已是最新版本"
            return 1
        fi
    else
        log_debug "无法检查更新"
        return 1
    fi
}

# 显示更新信息
show_update_info() {
    local current_version="$1"
    local latest_version="$2"

    if [[ $QUIET_MODE == false ]]; then
        echo
        print_info "发现新版本可用!"
        echo "  当前版本: v$current_version"
        echo "  最新版本: v$latest_version"
        echo
        echo "运行以下命令更新:"
        echo "  bash $0 --force"
        echo
    fi
}

# =============================================================================
# 安装状态管理
# =============================================================================

# 创建安装锁文件
create_install_lock() {
    INSTALL_LOCK_FILE="$TEMP_DIR/install.lock"

    if [[ -f "$INSTALL_LOCK_FILE" ]]; then
        local lock_pid
        lock_pid=$(cat "$INSTALL_LOCK_FILE" 2>/dev/null || echo "")

        if [[ -n "$lock_pid" ]] && kill -0 "$lock_pid" 2>/dev/null; then
            print_error "另一个安装进程正在运行 (PID: $lock_pid)"
            exit 1
        else
            log_warn "发现过期的锁文件，将其删除"
            safe_remove "$INSTALL_LOCK_FILE"
        fi
    fi

    echo "$$" > "$INSTALL_LOCK_FILE"
    log_debug "创建安装锁文件: $INSTALL_LOCK_FILE (PID: $$)"
}

# 清理安装锁文件
cleanup_install_lock() {
    if [[ -n "$INSTALL_LOCK_FILE" ]] && [[ -f "$INSTALL_LOCK_FILE" ]]; then
        safe_remove "$INSTALL_LOCK_FILE"
        log_debug "清理安装锁文件: $INSTALL_LOCK_FILE"
    fi
}

# 检查是否已安装
check_existing_installation() {
    log_debug "检查现有安装: $INSTALL_DIR/$SCRIPT_NAME"

    local target_file="$INSTALL_DIR/$SCRIPT_NAME"
    local version_file="$CONFIG_DIR/version"

    if [[ -f "$target_file" ]]; then
        log_debug "发现已安装的文件: $target_file"

        local installed_version=""
        if [[ -f "$version_file" ]]; then
            installed_version=$(cat "$version_file" 2>/dev/null | sed 's/^v//' || echo "")
            log_debug "读取到版本信息: $installed_version"
        fi

        if [[ -n "$installed_version" ]]; then
            print_info "检测到已安装版本: $installed_version"
        else
            print_info "检测到已安装的程序（版本未知）"
        fi

        if [[ "$FORCE_INSTALL" == false ]]; then
            log_debug "非强制安装模式，检查版本"

            local target_version
            if target_version=$(get_target_version); then
                log_debug "目标版本: $target_version"

                if [[ "$installed_version" == "$target_version" ]]; then
                    print_success "已安装最新版本 $target_version，无需重新安装"

                    # 检查是否有更新可用
                    if check_for_updates "$installed_version"; then
                        local latest_version
                        latest_version=$(get_latest_version_from_api)
                        show_update_info "$installed_version" "$latest_version"
                    fi

                    echo
                    show_usage_info "$target_file"
                    exit 0
                else
                    print_warning "将从 $installed_version 升级到 $target_version"
                fi
            else
                log_warn "无法获取目标版本，继续安装"
            fi
        else
            print_warning "强制重新安装模式"
        fi

        log_debug "已安装文件处理完成"
        return 0
    else
        log_debug "未发现已安装的文件"
    fi

    log_debug "check_existing_installation 函数即将返回"
    return 1
}

# =============================================================================
# 主要安装函数
# =============================================================================

# 下载和安装主程序
download_and_install() {
    local version
    version=$(get_target_version)

    if ! validate_version "$version"; then
        exit 1
    fi

    print_step "下载 $APP_DISPLAY_NAME v$version"

    # 创建必要的目录
    safe_mkdir "$INSTALL_DIR"
    safe_mkdir "$CONFIG_DIR"

    local target_file="$INSTALL_DIR/$SCRIPT_NAME"
    local temp_file="$TEMP_DIR/$SCRIPT_NAME"

    # 优先使用本地文件（如果在项目目录运行）
    if [[ -f "./$SCRIPT_NAME" ]] && [[ "$FORCE_INSTALL" == false ]]; then
        print_info "检测到本地文件，使用本地版本"

        # 验证本地文件
        if [[ -s "./$SCRIPT_NAME" ]]; then
            cp "./$SCRIPT_NAME" "$temp_file"
            log_debug "使用本地文件: ./$SCRIPT_NAME"
        else
            print_error "本地文件无效: ./$SCRIPT_NAME"
            exit 1
        fi
    else
        # 从 GitHub 下载
        local download_url
        download_url=$(get_download_url "$version")

        print_info "从 GitHub 下载: $download_url"

        if ! smart_download "$download_url" "$temp_file" "$APP_DISPLAY_NAME v$version"; then
            exit 1
        fi
    fi

    # 验证下载的文件
    if [[ ! -f "$temp_file" ]] || [[ ! -s "$temp_file" ]]; then
        print_error "文件无效或为空: $temp_file"
        exit 1
    fi

    # 简单验证文件内容（检查是否是 Python 脚本）
    if ! head -1 "$temp_file" | grep -q "python"; then
        print_error "下载的文件不是有效的 Python 脚本"
        exit 1
    fi

    # 移动到最终位置
    if ! mv "$temp_file" "$target_file"; then
        print_error "无法移动文件到安装目录: $target_file"
        exit 1
    fi

    # 设置执行权限
    if ! chmod +x "$target_file"; then
        print_error "无法设置执行权限: $target_file"
        exit 1
    fi

    # 保存版本信息
    echo "v$version" > "$CONFIG_DIR/version"

    # 保存安装信息
    cat > "$CONFIG_DIR/install_info" << EOF
version=v$version
install_date=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
install_dir=$INSTALL_DIR
config_dir=$CONFIG_DIR
script_path=$target_file
EOF

    print_success "安装完成: $APP_DISPLAY_NAME v$version"
    log_debug "程序安装到: $target_file"

    return 0
}

# 验证安装结果
verify_installation() {
    print_step "验证安装"
    log_debug "开始验证安装结果"

    local target_file="$INSTALL_DIR/$SCRIPT_NAME"

    # 检查文件是否存在且可执行
    log_debug "检查文件存在性: $target_file"
    if [[ ! -f "$target_file" ]]; then
        print_error "安装验证失败: 文件不存在 $target_file"
        return 1
    fi

    log_debug "检查文件可执行性"
    if [[ ! -x "$target_file" ]]; then
        print_error "安装验证失败: 文件不可执行 $target_file"
        return 1
    fi

    # 检查文件大小
    local file_size
    file_size=$(wc -c < "$target_file" 2>/dev/null || echo "0")
    log_debug "文件大小: $file_size 字节"

    if [[ "$file_size" -lt 1000 ]]; then
        print_error "安装验证失败: 文件太小，可能下载不完整"
        return 1
    fi

    # 简单的 Python 语法检查（使用超时）
    log_debug "开始 Python 语法检查"
    if command -v timeout >/dev/null 2>&1; then
        # 使用 timeout 命令（如果可用）
        if ! timeout 10 python3 -m py_compile "$target_file" 2>/dev/null; then
            log_warn "Python 语法检查失败或超时，跳过此检查"
        else
            log_debug "Python 语法检查通过"
        fi
    else
        # 不使用 timeout，直接检查
        log_debug "系统不支持 timeout，跳过语法检查"
    fi

    print_success "安装验证通过"
    log_debug "安装验证完成"
    return 0
}

# =============================================================================
# 用户界面和帮助函数
# =============================================================================

# 显示使用说明
show_usage_info() {
    local target_file="$1"
    log_debug "显示使用说明: $target_file"

    local version
    log_debug "获取目标版本用于显示"
    if ! version=$(get_target_version); then
        log_warn "无法获取版本信息，使用默认版本"
        version="$DEFAULT_VERSION"
    fi
    log_debug "使用版本: $version"

    if [[ $QUIET_MODE == false ]]; then
        echo
        print_success "🎉 $APP_DISPLAY_NAME v$version 安装成功！"
        echo -e "${COLOR_CYAN}=============================================="
        echo
        echo "📋 使用方法："
        echo "  python3 $target_file"
        echo
        echo "📁 配置目录: $CONFIG_DIR"
        echo "📄 程序位置: $target_file"
        echo
        echo "🚀 现在可以开始使用了！"
        echo
        echo "💡 提示："
        echo "  - 首次运行会自动创建配置文件"
        echo "  - 支持智能搜索和批量制种"
        echo "  - 所有功能都集成在单个文件中"
        echo "  - 使用 --help 查看更多选项"
        echo -e "==============================================${COLOR_RESET}"
        echo
    fi
}

# 显示帮助信息
show_help() {
    cat << EOF
$APP_DISPLAY_NAME 企业级安装器 v2.0

用法: $0 [选项]

选项:
  -h, --help              显示此帮助信息
  -v, --version VERSION   安装指定版本 (默认: 最新版本)
  -d, --dir DIR          指定安装目录 (默认: $DEFAULT_INSTALL_DIR)
  -c, --config DIR       指定配置目录 (默认: $DEFAULT_CONFIG_DIR)
  -f, --force            强制重新安装
  -q, --quiet            静默模式
  --debug                启用调试模式
  --no-color             禁用彩色输出

环境变量:
  TORRENT_MAKER_INSTALL_DIR    安装目录
  TORRENT_MAKER_CONFIG_DIR     配置目录
  NO_COLOR                     禁用彩色输出

示例:
  $0                           # 安装最新版本
  $0 -v 1.6.0                 # 安装指定版本
  $0 -d /usr/local/bin        # 安装到指定目录
  $0 -f                       # 强制重新安装
  $0 -q                       # 静默安装

更多信息: https://github.com/$GITHUB_REPO
EOF
}

# =============================================================================
# 清理和错误处理
# =============================================================================

# 清理临时文件
cleanup() {
    local exit_code=$?

    log_debug "开始清理 (退出码: $exit_code)"

    # 清理安装锁
    cleanup_install_lock

    # 清理临时目录
    if [[ -n "$TEMP_DIR" ]] && [[ -d "$TEMP_DIR" ]]; then
        safe_remove "$TEMP_DIR"
        log_debug "清理临时目录: $TEMP_DIR"
    fi

    # 如果安装失败，提供帮助信息
    if [[ $exit_code -ne 0 ]] && [[ $QUIET_MODE == false ]]; then
        echo
        print_error "安装失败 (退出码: $exit_code)"
        echo
        echo "故障排除:"
        echo "  1. 检查网络连接"
        echo "  2. 确保有足够的磁盘空间"
        echo "  3. 检查目录权限"
        echo "  4. 使用 --debug 查看详细信息"
        echo "  5. 查看项目文档: https://github.com/$GITHUB_REPO"
        echo
    fi

    exit $exit_code
}

# 信号处理
handle_signal() {
    local signal="$1"
    log_warn "收到信号: $signal"
    print_warning "安装被中断"
    exit 130
}

# =============================================================================
# 参数解析
# =============================================================================

# 解析命令行参数
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--version)
                if [[ -n "$2" ]] && [[ "$2" != -* ]]; then
                    TARGET_VERSION="$2"
                    shift 2
                else
                    print_error "选项 $1 需要一个参数"
                    exit 1
                fi
                ;;
            -d|--dir)
                if [[ -n "$2" ]] && [[ "$2" != -* ]]; then
                    INSTALL_DIR="$2"
                    shift 2
                else
                    print_error "选项 $1 需要一个参数"
                    exit 1
                fi
                ;;
            -c|--config)
                if [[ -n "$2" ]] && [[ "$2" != -* ]]; then
                    CONFIG_DIR="$2"
                    shift 2
                else
                    print_error "选项 $1 需要一个参数"
                    exit 1
                fi
                ;;
            -f|--force)
                FORCE_INSTALL=true
                shift
                ;;
            -q|--quiet)
                QUIET_MODE=true
                CURRENT_LOG_LEVEL=$LOG_LEVEL_ERROR
                shift
                ;;
            --debug)
                DEBUG_MODE=true
                # 只有在非静默模式下才设置调试级别
                if [[ $QUIET_MODE == false ]]; then
                    CURRENT_LOG_LEVEL=$LOG_LEVEL_DEBUG
                fi
                shift
                ;;
            --no-color)
                # 重新定义颜色变量为空
                readonly COLOR_RED=''
                readonly COLOR_GREEN=''
                readonly COLOR_YELLOW=''
                readonly COLOR_BLUE=''
                readonly COLOR_PURPLE=''
                readonly COLOR_CYAN=''
                readonly COLOR_WHITE=''
                readonly COLOR_RESET=''
                readonly COLOR_BOLD=''
                shift
                ;;
            -*)
                print_error "未知选项: $1"
                echo "使用 --help 查看帮助信息"
                exit 1
                ;;
            *)
                print_error "未知参数: $1"
                echo "使用 --help 查看帮助信息"
                exit 1
                ;;
        esac
    done
}
# =============================================================================
# 初始化和主函数
# =============================================================================

# 初始化环境
initialize() {
    # 设置信号处理
    trap 'handle_signal SIGINT' INT
    trap 'handle_signal SIGTERM' TERM
    trap 'cleanup' EXIT

    # 创建临时目录
    TEMP_DIR=$(mktemp -d -t "${APP_NAME}-install.XXXXXX") || {
        print_error "无法创建临时目录"
        exit 1
    }
    log_debug "创建临时目录: $TEMP_DIR"

    # 设置默认值
    INSTALL_DIR="${TORRENT_MAKER_INSTALL_DIR:-${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}}"
    CONFIG_DIR="${TORRENT_MAKER_CONFIG_DIR:-${CONFIG_DIR:-$DEFAULT_CONFIG_DIR}}"

    # 展开路径中的 ~ 和环境变量 (兼容 bash 3.2)
    if [[ "$INSTALL_DIR" =~ ^~/ ]]; then
        INSTALL_DIR="$HOME/${INSTALL_DIR#~/}"
    elif [[ "$INSTALL_DIR" == "~" ]]; then
        INSTALL_DIR="$HOME"
    fi

    if [[ "$CONFIG_DIR" =~ ^~/ ]]; then
        CONFIG_DIR="$HOME/${CONFIG_DIR#~/}"
    elif [[ "$CONFIG_DIR" == "~" ]]; then
        CONFIG_DIR="$HOME"
    fi

    log_debug "安装目录: $INSTALL_DIR"
    log_debug "配置目录: $CONFIG_DIR"

    # 创建安装锁
    create_install_lock
}

# 主安装流程
main() {
    log_debug "开始主安装流程"

    # 步骤1: 初始化环境
    update_install_step "初始化环境"
    print_header
    log_debug "头部信息显示完成"

    # 步骤2: 检查现有安装
    update_install_step "检查现有安装"
    local existing_installation=false
    local current_version=""

    if check_existing_installation; then
        existing_installation=true
        # 尝试读取当前版本
        if [[ -f "$CONFIG_DIR/version" ]]; then
            current_version=$(cat "$CONFIG_DIR/version" 2>/dev/null | sed 's/^v//' || echo "")
        fi
        log_debug "检测到现有安装: v$current_version"
    else
        log_debug "未检测到现有安装"
    fi

    # 步骤3: 检查系统依赖
    update_install_step "检查系统依赖"
    check_dependencies
    log_debug "依赖检查完成"

    # 步骤4: 下载和安装
    update_install_step "下载程序文件"
    local target_version
    target_version=$(get_target_version)

    if download_and_install; then
        log_debug "下载和安装完成"

        # 步骤5: 验证安装
        update_install_step "验证安装"
        if verify_installation; then
            log_debug "安装验证完成"

            # 步骤6: 完成安装
            update_install_step "完成安装"

            # 记录安装历史
            local install_type="install"
            if [[ $existing_installation == true ]]; then
                if [[ "$current_version" == "$target_version" ]]; then
                    install_type="reinstall"
                else
                    install_type="upgrade"
                fi
            fi

            # record_install_history "$target_version" "$install_type"  # 临时禁用

            # 显示使用说明
            show_usage_info "$INSTALL_DIR/$SCRIPT_NAME"

            # 显示安装历史（临时禁用）
            # if [[ $QUIET_MODE == false ]] && [[ $existing_installation == true ]]; then
            #     echo
            #     print_info "安装历史记录:"
            #     get_install_history | tail -3
            # fi

        else
            print_error "安装验证失败"
            exit 1
        fi
    else
        print_error "安装失败"
        exit 1
    fi

    log_debug "主安装流程完成"
}

# =============================================================================
# 脚本入口点
# =============================================================================

# 检查 Bash 版本 (需要 3.2+，兼容 macOS 默认版本)
bash_major="${BASH_VERSION%%.*}"
bash_minor="${BASH_VERSION#*.}"
bash_minor="${bash_minor%%.*}"

if [[ "$bash_major" -lt 3 ]] || [[ "$bash_major" -eq 3 && "$bash_minor" -lt 2 ]]; then
    echo "错误: 需要 Bash 3.2 或更高版本 (当前: $BASH_VERSION)" >&2
    echo "请升级 Bash 或使用更新的 shell" >&2
    exit 1
fi

# 解析命令行参数
parse_arguments "$@"

# 初始化环境
initialize

# 运行主函数
main

# 脚本结束
log_debug "安装脚本执行完成"
