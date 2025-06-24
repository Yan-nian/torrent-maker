#!/bin/bash

# GitHub Release 自动发布脚本
# 使用 GitHub CLI (gh) 自动创建 Release

set -e  # 遇到错误时退出

echo "🚀 GitHub Release 自动发布脚本"
echo "================================="

# 检查是否安装了 GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ 错误：未找到 GitHub CLI (gh)"
    echo ""
    echo "📥 请先安装 GitHub CLI："
    echo "  macOS: brew install gh"
    echo "  Ubuntu: sudo apt install gh"
    echo "  其他: https://cli.github.com/"
    echo ""
    echo "安装后运行: gh auth login"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "❌ 错误：未登录 GitHub"
    echo "请运行: gh auth login"
    exit 1
fi

# 检查是否在 git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 错误：不在 Git 仓库中"
    exit 1
fi

# 获取当前版本号
VERSION="v1.2.0"
REPO="Yan-nian/torrent-maker"

echo "📝 发布信息："
echo "   仓库: $REPO"
echo "   版本: $VERSION"
echo "   标题: Torrent Maker $VERSION"

# 确认发布
read -p "🤔 确认要发布 $VERSION 版本吗？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 取消发布"
    exit 1
fi

echo ""
echo "🏗️  准备发布..."

# 创建新的 tag
echo "📌 创建 Git tag: $VERSION"
git tag $VERSION
git push origin $VERSION

echo "📦 重新生成发布包..."
./release.sh

echo "🌐 创建 GitHub Release..."

# 发布说明
RELEASE_NOTES="# Torrent Maker $VERSION 🚀

一个基于 \`mktorrent\` 的半自动化种子制作工具，专为影视剧整季打包而设计。

## 🆕 更新内容

- 🐛 **修复剧集显示问题**：修正剧集范围和实际文件数量的显示逻辑
- ✨ **优化显示格式**：移除重复的集数信息显示
- 📦 **简化发布包**：只保留 .tar.gz 格式，减少文件数量
- 🚀 **全新安装脚本**：支持自动更新、mktorrent 检查、PATH 配置等
- 🧪 **增强测试覆盖**：添加剧集显示修复的专项测试
- 📚 **完善文档**：更新 README 和贡献指南

## ✨ 主要功能

- 🔍 **智能模糊搜索**：支持点号、下划线、连字符等分隔符智能处理
- 📊 **详细信息显示**：显示匹配度、文件数量、文件夹大小
- 🎬 **剧集信息解析**：自动识别 S01E01-E12 格式，支持断集检测
- 🌐 **Tracker 管理**：内置常用 Tracker，支持自定义添加
- 📁 **路径配置**：可自定义资源文件夹和输出文件夹
- 🎛️ **交互式界面**：友好的菜单式操作
- ⚙️ **配置管理**：支持运行时配置修改

## 🚀 快速开始

### 单文件版本（推荐普通用户）
\`\`\`bash
# 下载并解压
wget https://github.com/Yan-nian/torrent-maker/releases/download/$VERSION/torrent-maker-standalone.tar.gz
tar -xzf torrent-maker-standalone.tar.gz
cd standalone

# 运行
python3 torrent_maker.py
\`\`\`

### 完整版本（推荐开发者）
\`\`\`bash
# 下载并解压
wget https://github.com/Yan-nian/torrent-maker/releases/download/$VERSION/torrent-maker-full.tar.gz
tar -xzf torrent-maker-full.tar.gz
cd full

# 安装并运行
./install.sh
python3 run.py
\`\`\`

## 📋 系统要求

- Python 3.7+
- mktorrent (用于创建种子文件)

### mktorrent 安装
\`\`\`bash
# macOS
brew install mktorrent

# Ubuntu/Debian
sudo apt install mktorrent

# CentOS/RHEL
sudo yum install mktorrent
\`\`\`

## 🌟 核心特性

### 智能搜索算法
- 支持首字母缩写匹配（\"GoT\" → \"Game of Thrones\"）
- 智能分隔符处理（点号、下划线、连字符）
- 关键词重叠检测
- 模糊匹配打分

### 剧集信息解析
- **连续剧集**：\`S01E01-E12\`
- **断集处理**：\`S02E02-E12(8集)\` - 自动识别缺失集数
- **少数集数**：\`E01+E03+E07\` - 显示具体集数

### 配置管理
- 资源文件夹自定义
- 输出文件夹自定义
- Tracker 列表管理
- 实时配置修改

## 🐛 Bug 修复

此版本修复了以下问题：
- 剧集信息显示重复集数的问题
- 断集检测算法的逻辑错误
- 搜索结果格式化的显示问题

## 🙏 致谢

感谢 [mktorrent](https://github.com/Rudde/mktorrent) 项目提供的核心功能支持。

---

**⭐ 如果这个项目对您有帮助，请给它一个 Star！**"

# 使用 GitHub CLI 创建 Release
gh release create $VERSION \
    --title "Torrent Maker $VERSION" \
    --notes "$RELEASE_NOTES" \
    --latest \
    release/torrent-maker-standalone.tar.gz \
    release/torrent-maker-full.tar.gz

echo ""
echo "🎉 Release 创建成功！"
echo "🌐 查看 Release: https://github.com/$REPO/releases/tag/$VERSION"
echo "📦 发布包已自动上传"
echo ""
echo "✅ 发布完成！"
