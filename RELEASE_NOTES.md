# Torrent Maker v1.0.0 🚀

一个基于 `mktorrent` 的半自动化种子制作工具，专为影视剧整季打包而设计。

## ✨ 主要功能

- 🔍 **智能模糊搜索**：支持点号、下划线、连字符等分隔符智能处理
- 📊 **详细信息显示**：显示匹配度、文件数量、文件夹大小
- 🎬 **剧集信息解析**：自动识别 S01E01-E12 格式，支持断集检测
- 🌐 **Tracker 管理**：内置常用 Tracker，支持自定义添加
- 📁 **路径配置**：可自定义资源文件夹和输出文件夹
- 🎛️ **交互式界面**：友好的菜单式操作
- ⚙️ **配置管理**：支持运行时配置修改

## 📦 下载

### 单文件版本（推荐普通用户）
- **Linux/macOS**: [torrent-maker-standalone.tar.gz](https://github.com/Yan-nian/torrent-maker/releases/download/v1.0.0/torrent-maker-standalone.tar.gz)
- **Windows**: [torrent-maker-standalone.zip](https://github.com/Yan-nian/torrent-maker/releases/download/v1.0.0/torrent-maker-standalone.zip)

### 完整版本（推荐开发者）
- **Linux/macOS**: [torrent-maker-full.tar.gz](https://github.com/Yan-nian/torrent-maker/releases/download/v1.0.0/torrent-maker-full.tar.gz)
- **Windows**: [torrent-maker-full.zip](https://github.com/Yan-nian/torrent-maker/releases/download/v1.0.0/torrent-maker-full.zip)

## 🚀 快速开始

### 单文件版本
```bash
# 下载并解压
tar -xzf torrent-maker-standalone.tar.gz
cd standalone

# 运行
python3 torrent_maker.py
```

### 完整版本
```bash
# 下载并解压
tar -xzf torrent-maker-full.tar.gz
cd full

# 安装并运行
./install.sh
python3 run.py
```

## 📋 系统要求

- Python 3.7+
- mktorrent (用于创建种子文件)

### mktorrent 安装
```bash
# macOS
brew install mktorrent

# Ubuntu/Debian
sudo apt install mktorrent

# CentOS/RHEL
sudo yum install mktorrent
```

## 🎯 使用示例

1. **启动程序**：`python3 torrent_maker.py`
2. **搜索影视剧**：输入名称，如 "破冰行动"
3. **查看详情**：使用数字选择，`d1` 查看详细剧集
4. **制作种子**：确认后自动生成种子文件

## 🌟 核心特性

### 智能搜索算法
- 支持首字母缩写匹配（"GoT" → "Game of Thrones"）
- 智能分隔符处理（点号、下划线、连字符）
- 关键词重叠检测
- 模糊匹配打分

### 剧集信息解析
- **连续剧集**：`S01E01-E12 (12集)`
- **断集处理**：`S02E02-E12 (8集)` - 自动识别缺失集数
- **少数集数**：`E01+E03+E07 (3集)` - 显示具体集数

### 配置管理
- 资源文件夹自定义
- 输出文件夹自定义
- Tracker 列表管理
- 实时配置修改

## 🧪 测试覆盖

项目包含完整的测试套件：
- 基本功能测试
- 剧集解析测试
- 搜索算法测试
- 断集处理测试

## 📚 文档

- [README.md](README.md) - 完整使用说明
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- [LICENSE](LICENSE) - MIT 许可证

## 🙏 致谢

感谢 [mktorrent](https://github.com/Rudde/mktorrent) 项目提供的核心功能支持。

## 🐛 问题反馈

如遇问题，请提交 [Issue](https://github.com/Yan-nian/torrent-maker/issues)。

---

**⭐ 如果这个项目对您有帮助，请给它一个 Star！**
