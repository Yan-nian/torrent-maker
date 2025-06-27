#!/usr/bin/env bash

# =============================================================================
# Torrent Maker 一键安装脚本 - 标准版
# 版本: 2.0
# 功能: 检查mktorrent、安装依赖、安装最新程序
# 支持: macOS, Ubuntu, Debian, CentOS, RHEL
# =============================================================================

set -eo pipefail

# =============================================================================
# 配置和常量
# =============================================================================

readonly APP_NAME="torrent-maker"
readonly SCRIPT_NAME="torrent_maker.py"
readonly REPO_OWNER="Yan-nian"
readonly REPO_NAME="torrent-maker"
readonly GITHUB_REPO="${REPO_OWNER}/${REPO_NAME}"
readonly INSTALL_DIR="${HOME}/.local/bin"
readonly CONFIG_DIR="${HOME}/.torrent_maker"
readonly GITHUB_API="https://api.github.com/repos/${GITHUB_REPO}"
readonly GITHUB_RAW="https://raw.githubusercontent.com/${GITHUB_REPO}"

# 颜色定义
if [[ -t 1 ]] && [[ -z "${NO_COLOR:-}" ]]; then
    readonly RED='\033[0;31m'
    readonly GREEN='\033[0;32m'
    readonly YELLOW='\033[1;33m'
    readonly BLUE='\033[0;34m'
    readonly CYAN='\033[0;36m'
    readonly BOLD='\033[1m'
    readonly RESET='\033[0m'
else
    readonly RED='' GREEN='' YELLOW='' BLUE='' CYAN='' BOLD='' RESET=''
fi

# 全局变量
FORCE_INSTALL=false
QUIET_MODE=false
TARGET_VERSION=""

# =============================================================================
# 输出函数
# =============================================================================

log_info() {
    [[ $QUIET_MODE == false ]] && echo -e "${BLUE}[INFO]${RESET} $*" >&2
}

log_success() {
    [[ $QUIET_MODE == false ]] && echo -e "${GREEN}[SUCCESS]${RESET} $*" >&2
}

log_warn() {
    echo -e "${YELLOW}[WARN]${RESET} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${RESET} $*" >&2
}

print_header() {
    [[ $QUIET_MODE == false ]] && cat << EOF
${CYAN}${BOLD}
═══════════════════════════════════════════════════════════════
  🚀 Torrent Maker 一键安装脚本 v2.0
  📦 项目地址: https://github.com/${GITHUB_REPO}
═══════════════════════════════════════════════════════════════
${RESET}
EOF
}

# =============================================================================
# 工具函数
# =============================================================================

has_command() {
    command -v "$1" >/dev/null 2>&1
}

get_os_type() {
    case "$(uname -s)" in
        Darwin) echo "macos" ;;
        Linux)
            if [[ -f /etc/os-release ]]; then
                . /etc/os-release
                case "$ID" in
                    ubuntu|debian) echo "debian" ;;
                    centos|rhel|fedora) echo "redhat" ;;
                    *) echo "linux" ;;
                esac
            else
                echo "linux"
            fi
            ;;
        *) echo "unknown" ;;
    esac
}

get_latest_version() {
    local version=""
    
    # 优先从本地文件获取版本
    if [[ -f "./torrent_maker.py" ]]; then
        # 从VERSION变量获取版本号
        version=$(grep -E '^VERSION\s*=\s*"v[0-9]+\.[0-9]+\.[0-9]+"' "./torrent_maker.py" | sed -E 's/.*"v([0-9]+\.[0-9]+\.[0-9]+)".*/\1/' | head -1 2>/dev/null || echo "")
    fi
    
    # 如果本地没有找到版本，尝试从 GitHub API 获取
    if [[ -z "$version" ]]; then
        if has_command curl; then
            local api_response
            api_response=$(curl -s "${GITHUB_API}/releases/latest" 2>/dev/null || echo "")
            if [[ -n "$api_response" ]]; then
                version=$(echo "$api_response" | grep '"tag_name"' | sed -E 's/.*"tag_name":[[:space:]]*"v?([^"]+)".*/\1/' | head -1 2>/dev/null || echo "")
            fi
        elif has_command wget; then
            local api_response
            api_response=$(wget -qO- "${GITHUB_API}/releases/latest" 2>/dev/null || echo "")
            if [[ -n "$api_response" ]]; then
                version=$(echo "$api_response" | grep '"tag_name"' | sed -E 's/.*"tag_name":[[:space:]]*"v?([^"]+)".*/\1/' | head -1 2>/dev/null || echo "")
            fi
        fi
    fi
    
    # 如果仍然没有找到版本，使用默认版本
    if [[ -z "$version" ]]; then
        version="2.0.0"
    fi
    
    echo "$version"
}

# =============================================================================
# 依赖检查和安装
# =============================================================================

check_python() {
    log_info "检查 Python 环境..."
    
    if has_command python3; then
        local python_version
        python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
        log_success "Python 3 已安装 (版本: $python_version)"
        return 0
    else
        log_error "未找到 Python 3，请先安装 Python 3.6+"
        return 1
    fi
}

install_mktorrent() {
    local os_type
    os_type=$(get_os_type)
    
    log_info "在 $os_type 系统上安装 mktorrent..."
    
    case "$os_type" in
        "macos")
            if has_command brew; then
                brew install mktorrent
            else
                log_error "需要 Homebrew 来安装 mktorrent，请先安装 Homebrew"
                return 1
            fi
            ;;
        "debian")
            sudo apt-get update && sudo apt-get install -y mktorrent
            ;;
        "redhat")
            if has_command dnf; then
                sudo dnf install -y mktorrent
            elif has_command yum; then
                sudo yum install -y mktorrent
            else
                log_error "无法找到包管理器 (dnf/yum)"
                return 1
            fi
            ;;
        *)
            log_error "不支持的操作系统，请手动安装 mktorrent"
            return 1
            ;;
    esac
}

check_mktorrent() {
    log_info "检查 mktorrent 工具..."
    
    if has_command mktorrent; then
        log_success "mktorrent 已安装"
        return 0
    else
        log_warn "mktorrent 未安装，正在安装..."
        if install_mktorrent; then
            log_success "mktorrent 安装完成"
            return 0
        else
            log_error "mktorrent 安装失败"
            return 1
        fi
    fi
}

install_python_deps() {
    log_info "安装 Python 依赖..."
    
    # 检查是否存在 requirements.txt
    local req_file="./requirements.txt"
    if [[ ! -f "$req_file" ]]; then
        log_warn "未找到 requirements.txt，跳过依赖安装"
        return 0
    fi
    
    # 安装依赖
    if python3 -m pip install -r "$req_file" --user; then
        log_success "Python 依赖安装完成"
        return 0
    else
        log_error "Python 依赖安装失败"
        return 1
    fi
}

# =============================================================================
# 程序安装
# =============================================================================

download_program() {
    local version="$1"
    local download_url="${GITHUB_RAW}/main/${SCRIPT_NAME}"
    local target_file="${INSTALL_DIR}/${SCRIPT_NAME}"
    
    log_info "下载 Torrent Maker v$version..."
    
    # 创建安装目录
    mkdir -p "$INSTALL_DIR"
    
    # 检查本地文件
    if [[ -f "./${SCRIPT_NAME}" ]]; then
        log_info "使用本地文件"
        cp "./${SCRIPT_NAME}" "$target_file"
    else
        # 从网络下载
        if has_command curl; then
            if curl -fsSL "$download_url" -o "$target_file"; then
                log_success "下载完成"
            else
                log_error "下载失败"
                return 1
            fi
        elif has_command wget; then
            if wget -q "$download_url" -O "$target_file"; then
                log_success "下载完成"
            else
                log_error "下载失败"
                return 1
            fi
        else
            log_error "需要 curl 或 wget 来下载文件"
            return 1
        fi
    fi
    
    # 设置可执行权限
    chmod +x "$target_file"
    
    # 保存版本信息
    mkdir -p "$CONFIG_DIR"
    echo "$version" > "${CONFIG_DIR}/version"
    
    return 0
}

check_existing_installation() {
    local target_file="${INSTALL_DIR}/${SCRIPT_NAME}"
    
    if [[ -f "$target_file" ]] && [[ $FORCE_INSTALL == false ]]; then
        local installed_version="unknown"
        if [[ -f "${CONFIG_DIR}/version" ]]; then
            installed_version=$(cat "${CONFIG_DIR}/version" 2>/dev/null || echo "unknown")
        fi
        
        local latest_version
        latest_version=$(get_latest_version)
        
        if [[ "$installed_version" == "$latest_version" ]]; then
            log_warn "检测到相同版本 v$installed_version 已安装"
            log_info "如需重新安装，请使用 --force 参数"
            log_info "安装位置: $target_file"
            return 1
        else
            log_info "检测到已安装版本 v$installed_version，将升级到 v$latest_version"
        fi
    fi
    
    return 0
}

verify_installation() {
    local target_file="${INSTALL_DIR}/${SCRIPT_NAME}"
    
    log_info "验证安装..."
    
    if [[ -f "$target_file" ]] && [[ -x "$target_file" ]]; then
        log_success "安装验证成功"
        return 0
    else
        log_error "安装验证失败"
        return 1
    fi
}

show_usage() {
    local target_file="${INSTALL_DIR}/${SCRIPT_NAME}"
    
    [[ $QUIET_MODE == false ]] && cat << EOF

${GREEN}${BOLD}🎉 安装完成！${RESET}

${BOLD}使用方法:${RESET}
  python3 $target_file [选项]

${BOLD}添加到 PATH (可选):${RESET}
  echo 'export PATH="\$HOME/.local/bin:\$PATH"' >> ~/.bashrc
  source ~/.bashrc

${BOLD}快速开始:${RESET}
  cd /path/to/your/files
  python3 $target_file

EOF
}

# =============================================================================
# 参数解析
# =============================================================================

show_help() {
    cat << EOF
Torrent Maker 一键安装脚本 v2.0

用法: $0 [选项]

选项:
  -f, --force     强制重新安装
  -q, --quiet     静默模式
  -v, --version   指定安装版本
  -h, --help      显示帮助信息

示例:
  $0                    # 标准安装
  $0 --force           # 强制重新安装
  $0 --version 1.9.19  # 安装指定版本

EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -f|--force)
                FORCE_INSTALL=true
                shift
                ;;
            -q|--quiet)
                QUIET_MODE=true
                shift
                ;;
            -v|--version)
                if [[ -n "${2:-}" ]]; then
                    TARGET_VERSION="$2"
                    shift 2
                else
                    log_error "--version 需要指定版本号"
                    exit 1
                fi
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# =============================================================================
# 主函数
# =============================================================================

main() {
    print_header
    
    # 检查现有安装
    if ! check_existing_installation; then
        exit 0
    fi
    
    # 检查依赖
    log_info "检查系统依赖..."
    check_python || exit 1
    check_mktorrent || exit 1
    
    # 安装 Python 依赖
    install_python_deps
    
    # 获取目标版本
    local version="${TARGET_VERSION:-$(get_latest_version)}"
    
    # 下载和安装程序
    if download_program "$version"; then
        if verify_installation; then
            show_usage
            log_success "Torrent Maker v$version 安装完成！"
        else
            exit 1
        fi
    else
        exit 1
    fi
}

# =============================================================================
# 脚本入口
# =============================================================================

# 检查 Bash 版本 (兼容 macOS 默认 Bash 3.2+)
bash_major="${BASH_VERSION%%.*}"
bash_minor="${BASH_VERSION#*.}"
bash_minor="${bash_minor%%.*}"

if [[ "$bash_major" -lt 3 ]] || [[ "$bash_major" -eq 3 && "$bash_minor" -lt 2 ]]; then
    echo "错误: 需要 Bash 3.2 或更高版本 (当前: $BASH_VERSION)" >&2
    exit 1
fi

# 解析参数并运行
parse_args "$@"
main
