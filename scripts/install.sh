#!/bin/bash
# shellcheck shell=bash
# shellcheck disable=SC2039

# =============================================================================
# Torrent Maker 统一安装脚本 v3.0
#
# 支持多种安装模式：basic（基础）、stable（稳定）、enterprise（企业级）
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
readonly DEFAULT_VERSION="1.9.19"
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

# 安装模式
readonly MODE_BASIC="basic"
readonly MODE_STABLE="stable"
readonly MODE_ENTERPRISE="enterprise"

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

# 安装模式控制
INSTALL_MODE="$MODE_ENTERPRISE"  # 默认企业模式

# 功能开关（根据模式动态设置）
ENABLE_STEP_TRACKING=true
ENABLE_INSTALL_HISTORY=true
ENABLE_NETWORK_CHECK=true
ENABLE_SYSTEM_INFO=true
ENABLE_INSTALL_LOCK=true
ENABLE_EXISTING_CHECK=true

# 安装步骤跟踪
CURRENT_STEP=0
TOTAL_STEPS=6

# =============================================================================
# 模式配置函数
# =============================================================================

# 根据安装模式设置功能开关
setup_mode_features() {
    case "$INSTALL_MODE" in
        "$MODE_BASIC")
            ENABLE_STEP_TRACKING=false
            ENABLE_INSTALL_HISTORY=false
            ENABLE_NETWORK_CHECK=false
            ENABLE_SYSTEM_INFO=false
            ENABLE_INSTALL_LOCK=false
            ENABLE_EXISTING_CHECK=false
            CURRENT_LOG_LEVEL=$LOG_LEVEL_WARN
            ;;
        "$MODE_STABLE")
            ENABLE_STEP_TRACKING=false
            ENABLE_INSTALL_HISTORY=false
            ENABLE_SYSTEM_INFO=false
            ENABLE_INSTALL_LOCK=false
            CURRENT_LOG_LEVEL=$LOG_LEVEL_INFO
            ;;
        "$MODE_ENTERPRISE")
            # 保持所有功能开启
            CURRENT_LOG_LEVEL=$LOG_LEVEL_DEBUG
            ;;
        *)
            log_error "未知的安装模式: $INSTALL_MODE"
            exit 1
            ;;
    esac
    
    # 调试模式覆盖日志级别
    if [[ $DEBUG_MODE == true ]]; then
        CURRENT_LOG_LEVEL=$LOG_LEVEL_DEBUG
    fi
    
    # 静默模式覆盖日志级别
    if [[ $QUIET_MODE == true ]]; then
        CURRENT_LOG_LEVEL=$LOG_LEVEL_ERROR
    fi
}

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
        echo "═══════════════════════════════════════════════════════════════════════════════"
        echo "  🚀 $APP_DISPLAY_NAME 安装脚本 v3.0"
        echo "  📦 模式: $INSTALL_MODE"
        echo "  🔗 项目地址: https://github.com/$GITHUB_REPO"
        echo "═══════════════════════════════════════════════════════════════════════════════"
        echo -e "${COLOR_RESET}"
    fi
}

print_success() {
    [[ $QUIET_MODE == false ]] && echo -e "${COLOR_GREEN}✅ $*${COLOR_RESET}"
}

print_error() {
    echo -e "${COLOR_RED}❌ $*${COLOR_RESET}" >&2
}

print_warning() {
    [[ $QUIET_MODE == false ]] && echo -e "${COLOR_YELLOW}⚠️  $*${COLOR_RESET}"
}

print_info() {
    [[ $QUIET_MODE == false ]] && echo -e "${COLOR_BLUE}ℹ️  $*${COLOR_RESET}"
}

print_step() {
    [[ $QUIET_MODE == false ]] && echo -e "${COLOR_CYAN}🔄 $*${COLOR_RESET}"
}

# 安装步骤跟踪（企业模式）
update_install_step() {
    if [[ $ENABLE_STEP_TRACKING == true ]]; then
        ((CURRENT_STEP++))
        local step_name="$1"
        log_debug "安装步骤 $CURRENT_STEP/$TOTAL_STEPS: $step_name"
        print_step "[$CURRENT_STEP/$TOTAL_STEPS] $step_name"
    fi
}

# =============================================================================
# 工具函数
# =============================================================================

# 检查命令是否存在
has_command() {
    command -v "$1" >/dev/null 2>&1
}

# 安全创建目录
safe_mkdir() {
    local dir="$1"
    local mode="${2:-755}"
    
    if [[ ! -d "$dir" ]]; then
        log_debug "创建目录: $dir (权限: $mode)"
        mkdir -p "$dir"
        chmod "$mode" "$dir"
    fi
}

# 安全删除文件/目录
safe_remove() {
    local path="$1"
    if [[ -e "$path" ]]; then
        log_debug "删除: $path"
        rm -rf "$path"
    fi
}

# 网络连接检查（企业模式）
check_network() {
    if [[ $ENABLE_NETWORK_CHECK == false ]]; then
        return 0
    fi
    
    local test_url="https://api.github.com"
    log_debug "检查网络连接: $test_url"
    
    if has_command curl; then
        if ! curl -s --connect-timeout 10 "$test_url" >/dev/null; then
            print_error "网络连接失败，请检查网络设置"
            return 1
        fi
    elif has_command wget; then
        if ! wget -q --timeout=10 --tries=1 "$test_url" -O /dev/null; then
            print_error "网络连接失败，请检查网络设置"
            return 1
        fi
    else
        print_warning "无法检查网络连接（缺少 curl 或 wget）"
    fi
    
    return 0
}

# 重试执行命令
retry_command() {
    local max_attempts="$1"
    shift
    local cmd=("$@")
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        log_debug "执行命令 (尝试 $attempt/$max_attempts): ${cmd[*]}"
        
        if "${cmd[@]}"; then
            return 0
        fi
        
        if [[ $attempt -lt $max_attempts ]]; then
            log_warn "命令执行失败，等待重试... ($attempt/$max_attempts)"
            sleep $((attempt * 2))
        fi
        
        ((attempt++))
    done
    
    log_error "命令执行失败，已达最大重试次数: ${cmd[*]}"
    return 1
}

# =============================================================================
# 版本管理函数
# =============================================================================

# 从 GitHub API 获取最新版本
get_latest_version_from_api() {
    local api_url="${GITHUB_API_BASE}/repos/${GITHUB_REPO}/releases/latest"
    local version=""
    
    log_debug "获取最新版本: $api_url"
    
    # 尝试使用 curl
    if has_command curl; then
        local response
        if response=$(curl -s --connect-timeout "$DOWNLOAD_TIMEOUT" "$api_url" 2>/dev/null); then
            # 尝试多种方法解析 JSON
            if has_command python3; then
                version=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['tag_name'])" 2>/dev/null | sed 's/^v//' || echo "")
            elif has_command jq; then
                version=$(echo "$response" | jq -r '.tag_name' 2>/dev/null | sed 's/^v//' || echo "")
            else
                # 使用 grep 和 sed 作为备用方案
                version=$(echo "$response" | grep -o '"tag_name"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\".*/\1/' | sed 's/^v//' || echo "")
            fi
        fi
    # 尝试使用 wget
    elif has_command wget; then
        local response
        if response=$(wget -qO- --timeout="$DOWNLOAD_TIMEOUT" "$api_url" 2>/dev/null); then
            # 尝试多种方法解析 JSON
            if has_command python3; then
                version=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['tag_name'])" 2>/dev/null | sed 's/^v//' || echo "")
            elif has_command jq; then
                version=$(echo "$response" | jq -r '.tag_name' 2>/dev/null | sed 's/^v//' || echo "")
            else
                # 使用 grep 和 sed 作为备用方案
                version=$(echo "$response" | grep -o '"tag_name"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\".*/\1/' | sed 's/^v//' || echo "")
            fi
        fi
    fi
    
    echo "$version"
}

# 从远程文件获取版本（备用方法）
get_remote_version() {
    local remote_url="${GITHUB_RAW_BASE}/${GITHUB_REPO}/main/${SCRIPT_NAME}"
    local version=""
    
    log_debug "从远程获取版本: $remote_url"
    
    if has_command curl; then
        version=$(curl -s --connect-timeout "$DOWNLOAD_TIMEOUT" "$remote_url" 2>/dev/null | 
                 grep -E '^__version__\s*=' | 
                 sed -E 's/^__version__\s*=\s*["'\''](.*)["'\'']/\1/' | 
                 head -1 || echo "")
    elif has_command wget; then
        version=$(wget -qO- --timeout="$DOWNLOAD_TIMEOUT" "$remote_url" 2>/dev/null | 
                 grep -E '^__version__\s*=' | 
                 sed -E 's/^__version__\s*=\s*["'\''](.*)["'\'']/\1/' | 
                 head -1 || echo "")
    fi
    
    if [[ -z "$version" ]]; then
        log_debug "无法从远程获取版本号"
        return 1
    fi
    
    echo "$version"
}

# 语义化版本比较
compare_versions() {
    local version1="$1"
    local version2="$2"
    
    # 移除 'v' 前缀
    version1=${version1#v}
    version2=${version2#v}
    
    # 使用 sort -V 进行版本比较
    if printf '%s\n%s\n' "$version1" "$version2" | sort -V -C 2>/dev/null; then
        # version1 <= version2
        if [[ "$version1" == "$version2" ]]; then
            echo "0"  # 相等
        else
            echo "-1" # version1 < version2
        fi
    else
        echo "1"     # version1 > version2
    fi
}

# 获取目标版本
get_target_version() {
    local version=""
    
    # 优先级1: 用户指定版本
    if [[ -n "$TARGET_VERSION" ]]; then
        version="$TARGET_VERSION"
        log_debug "使用用户指定版本: $TARGET_VERSION"
    else
        # 优先级2: GitHub API 最新版本（动态获取）
        version=$(get_latest_version_from_api)
        if [[ -n "$version" ]]; then
            log_debug "使用 GitHub API 最新版本: $version"
        else
            # 优先级3: 远程文件版本（备用方法）
            version=$(get_remote_version)
            if [[ -n "$version" ]]; then
                log_debug "使用远程文件版本: $version"
            else
                # 优先级4: 默认版本
                version="$DEFAULT_VERSION"
                log_debug "使用默认版本: $DEFAULT_VERSION"
            fi
        fi
    fi
    
    echo "$version"
}

# 获取下载URL
get_download_url() {
    local version="$1"
    echo "${GITHUB_RAW_BASE}/${GITHUB_REPO}/v${version}/${SCRIPT_NAME}"
}

# =============================================================================
# 系统检查函数
# =============================================================================

# 检查 Python
check_python() {
    print_step "检查 Python 环境"
    
    local python_cmd=""
    local python_version=""
    
    # 检查 Python 3
    if has_command python3; then
        python_cmd="python3"
        python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    elif has_command python; then
        # 检查是否为 Python 3
        local version_info
        version_info=$(python --version 2>&1)
        if [[ $version_info == *"Python 3"* ]]; then
            python_cmd="python"
            python_version=$(echo "$version_info" | cut -d' ' -f2)
        fi
    fi
    
    if [[ -z "$python_cmd" ]]; then
        print_error "未找到 Python 3，请先安装 Python 3.6 或更高版本"
        echo "安装方法:"
        echo "  macOS: brew install python3"
        echo "  Ubuntu/Debian: sudo apt install python3"
        echo "  CentOS/RHEL: sudo yum install python3"
        exit 1
    fi
    
    # 检查版本
    local major minor
    major=$(echo "$python_version" | cut -d. -f1)
    minor=$(echo "$python_version" | cut -d. -f2)
    
    if [[ $major -lt 3 ]] || [[ $major -eq 3 && $minor -lt 6 ]]; then
        print_error "Python 版本过低: $python_version，需要 3.6 或更高版本"
        exit 1
    fi
    
    log_debug "Python 检查完成: $python_version"
    print_success "Python 环境检查通过: $python_cmd $python_version"
}

# 检查 mktorrent
check_mktorrent() {
    print_step "检查 mktorrent 工具"
    
    if ! has_command mktorrent; then
        print_warning "未找到 mktorrent，正在尝试安装..."
        
        # 根据系统类型安装
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if has_command brew; then
                print_info "使用 Homebrew 安装 mktorrent..."
                if ! brew install mktorrent; then
                    print_error "mktorrent 安装失败，请手动安装"
                    exit 1
                fi
            else
                print_error "请先安装 Homebrew，然后运行: brew install mktorrent"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if has_command apt-get; then
                print_info "使用 apt 安装 mktorrent..."
                if ! sudo apt-get update && sudo apt-get install -y mktorrent; then
                    print_error "mktorrent 安装失败，请手动安装"
                    exit 1
                fi
            elif has_command yum; then
                print_info "使用 yum 安装 mktorrent..."
                if ! sudo yum install -y mktorrent; then
                    print_error "mktorrent 安装失败，请手动安装"
                    exit 1
                fi
            elif has_command dnf; then
                print_info "使用 dnf 安装 mktorrent..."
                if ! sudo dnf install -y mktorrent; then
                    print_error "mktorrent 安装失败，请手动安装"
                    exit 1
                fi
            else
                print_error "不支持的 Linux 发行版，请手动安装 mktorrent"
                exit 1
            fi
        else
            print_error "不支持的操作系统，请手动安装 mktorrent"
            exit 1
        fi
    fi
    
    log_debug "mktorrent 检查完成"
    print_success "mktorrent 工具检查通过"
}

# 系统依赖检查（企业模式）
check_dependencies() {
    if [[ $ENABLE_SYSTEM_INFO == false ]]; then
        check_python
        check_mktorrent
        return 0
    fi
    
    log_debug "开始检查系统依赖"
    
    # 显示系统信息
    if [[ $ENABLE_SYSTEM_INFO == true ]]; then
        log_debug "开始显示系统信息"
        show_system_info || {
            log_debug "系统信息显示失败，继续安装"
        }
        log_debug "系统信息显示完成"
    fi
    
    # 检查网络连接
    if [[ $ENABLE_NETWORK_CHECK == true ]]; then
        log_debug "开始检查网络连接"
        if check_network; then
            log_debug "网络连接正常"
        fi
        log_debug "网络连接检查完成"
    fi
    
    # 检查 Python
    log_debug "开始检查 Python"
    if check_python; then
        log_debug "Python 检查完成"
    else
        log_debug "Python 检查失败"
        exit 1
    fi
    
    # 检查 mktorrent
    log_debug "开始检查 mktorrent"
    if check_mktorrent; then
        log_debug "mktorrent 检查完成"
    fi
    
    log_debug "依赖检查函数完成"
}

# 显示系统信息（企业模式）
show_system_info() {
    if [[ $ENABLE_SYSTEM_INFO == false ]]; then
        return 0
    fi
    
    print_info "系统信息:"
    echo "  操作系统: $(uname -s)"
    echo "  架构: $(uname -m)"
    echo "  内核版本: $(uname -r)"
    
    if has_command lsb_release; then
        echo "  发行版: $(lsb_release -d | cut -f2)"
    elif [[ -f /etc/os-release ]]; then
        local pretty_name
        pretty_name=$(grep '^PRETTY_NAME=' /etc/os-release | cut -d'=' -f2 | tr -d '"')
        echo "  发行版: $pretty_name"
    fi
    
    echo
}

# =============================================================================
# 安装历史管理（企业模式）
# =============================================================================

# 记录安装历史
record_install_history() {
    if [[ $ENABLE_INSTALL_HISTORY == false ]]; then
        return 0
    fi
    
    local version="$1"
    local install_type="$2"
    local history_file="$CONFIG_DIR/install_history"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    safe_mkdir "$CONFIG_DIR"
    
    echo "$timestamp | $install_type | v$version" >> "$history_file"
    log_debug "记录安装历史: $install_type v$version"
}

# 获取安装历史
get_install_history() {
    if [[ $ENABLE_INSTALL_HISTORY == false ]]; then
        return 0
    fi
    
    local history_file="$CONFIG_DIR/install_history"
    if [[ -f "$history_file" ]]; then
        cat "$history_file"
    fi
}

# 检查更新提示
show_update_hint() {
    local current_version
    current_version=$(get_target_version)
    log_debug "检查更新: 当前版本 $current_version"
    
    local latest_version
    latest_version=$(get_latest_version_from_api)
    if [[ -n "$latest_version" ]] && [[ "$latest_version" != "$current_version" ]]; then
        log_debug "发现新版本: $latest_version"
        print_info "💡 发现新版本 v$latest_version，当前版本 v$current_version"
    else
        log_debug "已是最新版本"
    fi
    
    log_debug "无法检查更新"
}

# =============================================================================
# 安装锁管理（企业模式）
# =============================================================================

# 创建安装锁
create_install_lock() {
    if [[ $ENABLE_INSTALL_LOCK == false ]]; then
        return 0
    fi
    
    INSTALL_LOCK_FILE="$TEMP_DIR/install.lock"
    
    if [[ -f "$INSTALL_LOCK_FILE" ]]; then
        local lock_pid
        lock_pid=$(cat "$INSTALL_LOCK_FILE" 2>/dev/null || echo "")
        if [[ -n "$lock_pid" ]] && kill -0 "$lock_pid" 2>/dev/null; then
            print_error "检测到另一个安装进程正在运行 (PID: $lock_pid)"
            exit 1
        fi
    fi
    
    echo "$$" > "$INSTALL_LOCK_FILE"
    log_debug "创建安装锁文件: $INSTALL_LOCK_FILE (PID: $$)"
}

# 清理安装锁
cleanup_install_lock() {
    if [[ $ENABLE_INSTALL_LOCK == true ]] && [[ -f "$INSTALL_LOCK_FILE" ]]; then
        rm -f "$INSTALL_LOCK_FILE"
        log_debug "清理安装锁文件: $INSTALL_LOCK_FILE"
    fi
}

# 检查现有安装（企业模式）
check_existing_installation() {
    if [[ $ENABLE_EXISTING_CHECK == false ]]; then
        return 1  # 表示没有现有安装
    fi
    
    log_debug "检查现有安装: $INSTALL_DIR/$SCRIPT_NAME"
    
    local target_file="$INSTALL_DIR/$SCRIPT_NAME"
    
    if [[ -f "$target_file" ]]; then
        log_debug "发现已安装的文件: $target_file"
        
        # 尝试读取版本信息
        local installed_version
        if installed_version=$(grep -E '^__version__\s*=' "$target_file" 2>/dev/null | sed -E 's/^__version__\s*=\s*["'\''](.*)["'\'']/\1/' | head -1); then
            log_debug "读取到版本信息: $installed_version"
            
            # 保存版本信息到配置文件
            safe_mkdir "$CONFIG_DIR"
            echo "$installed_version" > "$CONFIG_DIR/version"
            
            # 检查是否需要强制安装
            if [[ $FORCE_INSTALL == false ]]; then
                log_debug "非强制安装模式，检查版本"
                
                local target_version
                target_version=$(get_target_version)
                log_debug "目标版本: $target_version"
                
                if [[ "$installed_version" == "$target_version" ]]; then
                    print_warning "检测到相同版本 v$installed_version 已安装"
                    print_info "如需重新安装，请使用 --force 参数"
                    print_info "安装位置: $target_file"
                    
                    # 显示使用说明
                    show_usage_info "$target_file"
                    exit 0
                else
                    print_info "检测到已安装版本 v$installed_version，将升级到 v$target_version"
                fi
            fi
        fi
        
        log_debug "已安装文件处理完成"
        return 0
    else
        log_debug "未发现已安装的文件"
        return 1
    fi
    
    log_debug "check_existing_installation 函数即将返回"
}

# =============================================================================
# 下载和安装函数
# =============================================================================

# 智能下载函数
smart_download() {
    local url="$1"
    local output="$2"
    local description="${3:-文件}"
    
    log_debug "下载 $description: $url -> $output"
    
    # 检查本地文件
    if [[ -f "./$SCRIPT_NAME" ]]; then
        print_info "发现本地文件，使用本地版本"
        cp "./$SCRIPT_NAME" "$output"
        log_debug "使用本地文件: ./$SCRIPT_NAME"
        return 0
    fi
    
    # 尝试下载
    local download_success=false
    
    if has_command curl; then
        if retry_command $MAX_RETRIES curl -fsSL --connect-timeout "$DOWNLOAD_TIMEOUT" "$url" -o "$output"; then
            download_success=true
        fi
    elif has_command wget; then
        if retry_command $MAX_RETRIES wget -q --timeout="$DOWNLOAD_TIMEOUT" "$url" -O "$output"; then
            download_success=true
        fi
    else
        print_error "需要 curl 或 wget 来下载文件"
        return 1
    fi
    
    if [[ $download_success == true ]] && [[ -f "$output" ]] && [[ -s "$output" ]]; then
        log_debug "下载成功: $output ($(wc -c < "$output") 字节)"
        return 0
    else
        print_error "下载失败: $description"
        return 1
    fi
}

# 下载和安装主程序
download_and_install() {
    local target_version
    target_version=$(get_target_version)
    
    local download_url
    download_url=$(get_download_url "$target_version")
    
    local temp_file="$TEMP_DIR/$SCRIPT_NAME"
    local target_file="$INSTALL_DIR/$SCRIPT_NAME"
    
    # 下载文件
    if ! smart_download "$download_url" "$temp_file" "$APP_DISPLAY_NAME v$target_version"; then
        return 1
    fi
    
    # 安装文件
    safe_mkdir "$INSTALL_DIR"
    cp "$temp_file" "$target_file"
    chmod +x "$target_file"
    
    # 保存版本信息
    safe_mkdir "$CONFIG_DIR"
    echo "$target_version" > "$CONFIG_DIR/version"
    
    log_debug "程序安装到: $target_file"
    print_success "安装完成: $target_file"
    
    return 0
}

# 验证安装
verify_installation() {
    local target_file="$INSTALL_DIR/$SCRIPT_NAME"
    
    log_debug "开始验证安装结果"
    
    # 检查文件是否存在
    if [[ ! -f "$target_file" ]]; then
        log_debug "检查文件存在性: $target_file"
        print_error "安装验证失败: 文件不存在"
        return 1
    fi
    
    # 检查文件是否可执行
    if [[ ! -x "$target_file" ]]; then
        log_debug "检查文件可执行性"
        print_error "安装验证失败: 文件不可执行"
        return 1
    fi
    
    # 检查文件大小
    local file_size
    file_size=$(wc -c < "$target_file")
    if [[ $file_size -lt 1000 ]]; then
        log_debug "文件大小: $file_size 字节"
        print_error "安装验证失败: 文件大小异常"
        return 1
    fi
    
    # Python 语法检查
    if has_command python3 && has_command timeout; then
        log_debug "开始 Python 语法检查"
        if timeout 10 python3 -m py_compile "$target_file" 2>/dev/null; then
            log_debug "Python 语法检查通过"
        else
            print_error "安装验证失败: Python 语法错误"
            return 1
        fi
    else
        log_debug "系统不支持 timeout，跳过语法检查"
    fi
    
    log_debug "安装验证完成"
    print_success "安装验证通过"
    return 0
}

# 显示使用说明
show_usage_info() {
    local target_file="$1"
    
    if [[ $QUIET_MODE == true ]]; then
        return 0
    fi
    
    log_debug "显示使用说明: $target_file"
    
    local version
    version=$(get_target_version)
    log_debug "使用版本: $version"
    
    echo
    print_success "🎉 $APP_DISPLAY_NAME v$version 安装成功！"
    echo
    echo -e "${COLOR_CYAN}📖 使用方法:${COLOR_RESET}"
    echo "  $target_file [选项] <文件或目录>"
    echo
    echo -e "${COLOR_CYAN}📝 使用示例:${COLOR_RESET}"
    echo "  # 制作单个文件的种子"
    echo "  $target_file /path/to/file.txt"
    echo
    echo "  # 制作目录的种子"
    echo "  $target_file /path/to/directory"
    echo
    echo "  # 查看帮助信息"
    echo "  $target_file --help"
    echo
    echo -e "${COLOR_CYAN}🔗 更多信息:${COLOR_RESET}"
    echo "  项目地址: https://github.com/$GITHUB_REPO"
    echo "  问题反馈: https://github.com/$GITHUB_REPO/issues"
    echo
    
    # 检查 PATH
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        print_warning "安装目录不在 PATH 中，建议添加到 shell 配置文件:"
        echo "  echo 'export PATH=\"$INSTALL_DIR:\$PATH\"' >> ~/.bashrc"
        echo "  echo 'export PATH=\"$INSTALL_DIR:\$PATH\"' >> ~/.zshrc"
        echo
    fi
}

# =============================================================================
# 清理函数
# =============================================================================

# 清理函数
cleanup() {
    local exit_code=$?
    
    log_debug "开始清理 (退出码: $exit_code)"
    
    # 清理安装锁
    cleanup_install_lock
    
    # 清理临时目录
    if [[ -n "$TEMP_DIR" ]] && [[ -d "$TEMP_DIR" ]]; then
        log_debug "清理临时目录: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
    fi
    
    exit $exit_code
}

# 注册清理函数
trap cleanup EXIT INT TERM

# =============================================================================
# 初始化函数
# =============================================================================

# 初始化环境
initialize() {
    # 设置模式功能
    setup_mode_features
    
    # 创建临时目录
    TEMP_DIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'torrent-maker-install')
    log_debug "创建临时目录: $TEMP_DIR"
    
    # 创建安装锁
    create_install_lock
    
    # 设置默认值
    INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"
    CONFIG_DIR="${CONFIG_DIR:-$DEFAULT_CONFIG_DIR}"
    
    # 确保目录存在
    safe_mkdir "$INSTALL_DIR"
    safe_mkdir "$CONFIG_DIR"
    
    log_debug "安装目录: $INSTALL_DIR"
    log_debug "配置目录: $CONFIG_DIR"
}

# =============================================================================
# 参数解析函数
# =============================================================================

# 显示帮助信息
show_help() {
    echo "$APP_DISPLAY_NAME 统一安装脚本 v3.0"
    echo
    echo "用法: $0 [选项]"
    echo
    echo "安装模式:"
    echo "  --mode=MODE        安装模式: basic|stable|enterprise (默认: enterprise)"
    echo "  --simple           等同于 --mode=basic"
    echo "  --enterprise       等同于 --mode=enterprise"
    echo
    echo "基础选项:"
    echo "  -h, --help         显示帮助信息"
    echo "  -v, --version VER  指定版本"
    echo "  -f, --force        强制重新安装"
    echo "  -q, --quiet        静默模式"
    echo "  --debug            调试模式"
    echo
    echo "企业级选项:"
    echo "  --no-history       禁用安装历史记录"
    echo "  --no-lock          禁用安装锁"
    echo "  --skip-network     跳过网络检查"
    echo "  --skip-system      跳过系统信息显示"
    echo
    echo "安装模式说明:"
    echo "  basic      - 基础模式: 最小功能集，快速安装"
    echo "  stable     - 稳定模式: 平衡功能和稳定性"
    echo "  enterprise - 企业模式: 完整功能，详细日志和错误处理"
    echo
    echo "示例:"
    echo "  $0                    # 企业模式安装"
    echo "  $0 --simple           # 基础模式安装"
    echo "  $0 --mode=stable      # 稳定模式安装"
    echo "  $0 -v 1.9.18 --force  # 强制安装指定版本"
    echo
}

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
                    print_error "--version 需要指定版本号"
                    exit 1
                fi
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
            --mode=*)
                INSTALL_MODE="${1#*=}"
                case "$INSTALL_MODE" in
                    "$MODE_BASIC"|"$MODE_STABLE"|"$MODE_ENTERPRISE")
                        # 有效模式
                        ;;
                    *)
                        print_error "无效的安装模式: $INSTALL_MODE"
                        print_error "支持的模式: basic, stable, enterprise"
                        exit 1
                        ;;
                esac
                shift
                ;;
            --simple)
                INSTALL_MODE="$MODE_BASIC"
                shift
                ;;
            --enterprise)
                INSTALL_MODE="$MODE_ENTERPRISE"
                shift
                ;;
            --no-history)
                ENABLE_INSTALL_HISTORY=false
                shift
                ;;
            --no-lock)
                ENABLE_INSTALL_LOCK=false
                shift
                ;;
            --skip-network)
                ENABLE_NETWORK_CHECK=false
                shift
                ;;
            --skip-system)
                ENABLE_SYSTEM_INFO=false
                shift
                ;;
            *)
                print_error "未知参数: $1"
                print_error "使用 --help 查看帮助信息"
                exit 1
                ;;
        esac
    done
}

# =============================================================================
# 主函数
# =============================================================================

# 主安装流程
main() {
    log_debug "开始主安装流程"
    
    # 步骤1: 初始化环境
    if [[ $ENABLE_STEP_TRACKING == true ]]; then
        update_install_step "初始化环境"
    fi
    print_header
    log_debug "头部信息显示完成"
    
    # 步骤2: 检查现有安装
    if [[ $ENABLE_STEP_TRACKING == true ]]; then
        update_install_step "检查现有安装"
    fi
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
    if [[ $ENABLE_STEP_TRACKING == true ]]; then
        update_install_step "检查系统依赖"
    fi
    check_dependencies
    log_debug "依赖检查完成"
    
    # 步骤4: 下载和安装
    if [[ $ENABLE_STEP_TRACKING == true ]]; then
        update_install_step "下载程序文件"
    fi
    local target_version
    target_version=$(get_target_version)
    
    if download_and_install; then
        log_debug "下载和安装完成"
        
        # 步骤5: 验证安装
        if [[ $ENABLE_STEP_TRACKING == true ]]; then
            update_install_step "验证安装"
        fi
        if verify_installation; then
            log_debug "安装验证完成"
            
            # 步骤6: 完成安装
            if [[ $ENABLE_STEP_TRACKING == true ]]; then
                update_install_step "完成安装"
            fi
            
            # 记录安装历史
            local install_type="install"
            if [[ $existing_installation == true ]]; then
                if [[ "$current_version" == "$target_version" ]]; then
                    install_type="reinstall"
                else
                    install_type="upgrade"
                fi
            fi
            
            record_install_history "$target_version" "$install_type"
            
            # 显示使用说明
            show_usage_info "$INSTALL_DIR/$SCRIPT_NAME"
            
            # 显示安装历史
            if [[ $QUIET_MODE == false ]] && [[ $existing_installation == true ]] && [[ $ENABLE_INSTALL_HISTORY == true ]]; then
                echo
                print_info "安装历史记录:"
                get_install_history | tail -3
            fi
            
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
