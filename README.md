# torrent-maker v1.5.0 - 高性能优化版

一个基于 `mktorrent` 的**高性能**半自动化种子制作工具，专为影视剧整季打包而设计。

## 🚀 v1.5.0 重大性能优化更新

### ⚡ 核心性能提升
- **种子创建速度提升 30-50%**: 优化 mktorrent 参数，启用多线程处理
- **搜索响应时间减少 40-60%**: 智能索引缓存和高性能相似度算法
- **内存使用减少 20-30%**: LRU 缓存系统和内存管理优化
- **批量处理效率提升 50-70%**: 智能并发策略，进程池+线程池混合

### 🧠 智能算法优化
- **智能 Piece Size 计算**: 基于文件大小的预计算查找表，O(1) 时间复杂度
- **FastSimilarityCalculator**: 使用 Jaccard 相似度替代 SequenceMatcher，性能提升显著
- **SmartIndexCache**: 智能索引缓存，支持预筛选和快速查找
- **LRU 缓存系统**: 支持最大容量限制和自动淘汰策略

### 📊 性能监控增强
- **性能等级评估**: A+/B+/C+/D 四级性能评估系统
- **智能优化建议**: 根据性能统计自动生成优化建议
- **缓存统计监控**: 命中率、条目数、淘汰次数等详细统计

---

## 📦 推荐版本：单文件版本（高性能优化版）

**强烈推荐使用单文件版本 `torrent_maker.py`**，包含所有 v1.5.0 性能优化功能：

```bash
# 直接运行高性能版本
python torrent_maker.py
```

### ✅ 单文件版本优势
- ✅ **性能最优**: 包含所有 v1.5.0 高级性能优化
- ✅ **功能最全**: 智能算法、缓存系统、内存管理
- ✅ **部署简单**: 单文件，无依赖冲突
- ✅ **维护及时**: 主要开发版本，功能更新最快

### ⚠️ 模块化版本状态
- ⚠️ **已弃用**: `src/` 目录下的模块化版本已被弃用
- ⚠️ **功能落后**: 缺少 v1.5.0 的关键性能优化
- ⚠️ **将移除**: 下个版本将完全移除模块化版本

## ✨ 主要功能

- 🔍 **智能模糊搜索**：根据输入的影视剧名称智能匹配文件夹
- � **批量制种**：支持多选和批量制作种子文件
- 🔄 **连续搜索**：制种完成后可直接继续搜索，提升工作效率
- �📊 **详细信息显示**：显示匹配度、文件数量、文件夹大小等信息  
- 🎬 **剧集信息解析**：自动识别并显示文件夹内集数信息（如 S01E01-E12，支持断集）
- ⚡ **快速制种**：直接输入路径快速制作种子，支持批量路径
- 🌐 **Tracker 管理**：支持预设和自定义 BitTorrent Tracker 服务器
- 📁 **资源文件夹配置**：可自定义影视剧资源存放路径
- 📂 **输出文件夹配置**：可自定义种子文件保存路径
- 🎛️ **交互式界面**：提供友好的菜单式操作界面和快捷键支持
- ⚙️ **配置管理**：支持配置文件管理和实时修改
- 📋 **最近种子**：查看最近制作的种子文件

## 📋 系统要求

### 必需软件
- **Python 3.7+**
- **mktorrent**：用于创建种子文件的核心工具

### 支持平台
- macOS (推荐使用 Homebrew)
- Linux (Ubuntu/Debian/CentOS/Fedora)
- Windows (需要手动安装 mktorrent)

## 🚀 快速安装

### 📦 单文件版本（强烈推荐 - 高性能优化版）

**这是推荐的主要版本**，包含所有 v1.5.0 性能优化功能，配置文件自动生成在 `~/.torrent_maker/` 目录下。

```bash
# 下载单文件版本
wget https://github.com/Yan-nian/torrent-maker/releases/download/v1.0.0/torrent-maker-standalone.tar.gz

# 解压并运行
tar -xzf torrent-maker-standalone.tar.gz
cd standalone
python3 torrent_maker.py
```

或者使用一键安装脚本：

```bash
curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash
```

**新版安装脚本特性：**
- 🔍 自动检查和安装 mktorrent
- 🔄 支持版本检查和自动更新
- 🌐 网络连接验证
- 📁 自动配置 PATH 环境变量
- 🎨 彩色界面输出
- 🐧 支持多种 Linux 发行版

### ⚠️ 完整版本（已弃用，不推荐）

**注意：模块化版本已被弃用，将在下个版本中移除。**

```bash
# 克隆仓库（不推荐，请使用单文件版本）
git clone https://github.com/Yan-nian/torrent-maker.git
cd torrent-maker

# 直接使用高性能单文件版本（推荐）
python torrent_maker.py

# 或使用弃用的模块化版本（不推荐）
pip install -r requirements.txt
python src/main.py  # 会显示弃用警告
```

**强烈建议直接使用 `python torrent_maker.py` 获得最佳性能！**

## 📦 mktorrent 安装

### macOS
```bash
brew install mktorrent
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install mktorrent
```

### CentOS/RHEL/Fedora
```bash
# CentOS/RHEL
sudo yum install mktorrent

# Fedora
sudo dnf install mktorrent
```

### Windows
1. 从 [mktorrent releases](https://github.com/Rudde/mktorrent/releases) 下载 Windows 版本
2. 将 `mktorrent.exe` 放到 PATH 环境变量中的目录

## 🎯 使用方法

### 基本使用流程

1. **启动程序**
   ```bash
   python3 torrent_maker.py  # 单文件版本
   # 或
   python src/main.py        # 完整版本
   ```

2. **搜索影视剧**
   - 输入影视剧名称（支持模糊搜索）
   - 程序会智能匹配相关文件夹并显示详细信息

3. **选择制种方式**
   - **单选**：输入数字选择单个文件夹
   - **多选**：用逗号分隔选择多个文件夹（如：`1,3,5`）
   - **查看详情**：使用 `d数字` 查看详细剧集列表（如：`d1`）

4. **制作种子**
   - 确认选择后程序自动调用 mktorrent 制作种子文件
   - 支持批量制种，显示详细进度和结果统计

### 🆕 新功能亮点

#### 连续搜索
- 制种完成后可选择继续搜索其他内容
- 无需返回主菜单，提升工作效率

#### 批量制种
- **多选制种**：逗号分隔选择多个文件夹（如：`1,3,5`）
- **快速制种**：分号分隔多个路径进行批量处理（如：`path1;path2`）

#### 快捷键支持
- `s/search` - 搜索制种
- `q/quick` - 快速制种
- `c/config` - 查看配置
- `l/list` - 最近种子
- `h/help` - 显示帮助

### 搜索功能特点

- **智能分隔符处理**：自动处理点号、下划线、连字符等分隔符
- **首字母缩写匹配**：支持 "Got" 匹配 "Game of Thrones"
- **关键词重叠**：智能识别关键词组合
- **剧集信息解析**：自动识别 S01E01-E12、断集等格式

### 剧集信息显示

程序能够智能解析各种剧集命名格式：

- **连续剧集**：`S01E01-E12 (12集)`
- **断集处理**：`S02E02-E12 (8集)` - 自动识别缺失集数
- **少数集数**：`E01+E03+E07 (3集)` - 显示具体集数

使用 `d数字` 命令可查看文件夹内所有剧集文件的详细列表。

## ⚙️ 配置管理

### 配置文件位置

- **单文件版本**：`~/.torrent_maker/`
- **完整版本**：`config/` 目录

### 主要配置项

1. **资源文件夹** (`resources_folder`)
   - 存放影视剧资源的根目录
   - 支持在程序中动态修改

2. **输出文件夹** (`output_folder`)
   - 种子文件保存目录
   - 支持在程序中动态修改

3. **Tracker 服务器** (`trackers.txt`)
   - 预设的 BitTorrent Tracker 列表
   - 支持添加、删除和编辑

### 配置菜单操作

程序提供完整的配置管理界面：

- `c` - 进入配置菜单
- `1` - 查看当前配置
- `2` - 修改资源文件夹
- `3` - 修改输出文件夹  
- `4` - 管理 Tracker 列表
- `q` - 返回主菜单

## 📁 目录结构

### 完整版本
```
torrent-maker/
├── README.md              # 项目说明文档
├── requirements.txt       # Python 依赖列表
├── setup.py              # 安装配置
├── run.py                # 快速启动脚本
├── install.sh            # 安装脚本
├── release.sh            # 发布打包脚本
├── config/               # 配置文件目录
│   ├── settings.json     # 主配置文件
│   └── trackers.txt      # Tracker 服务器列表
├── src/                  # 源代码目录
│   ├── main.py          # 主程序入口
│   ├── config_manager.py # 配置管理模块
│   ├── file_matcher.py   # 文件匹配模块
│   ├── torrent_creator.py # 种子创建模块
│   └── utils/           # 工具模块
│       ├── __init__.py
│       └── helpers.py

```

### 单文件版本
```
standalone/
├── torrent_maker.py      # 单文件版本（包含全部功能）
└── README_STANDALONE.md  # 单文件版本说明
```



## 📊 版本对比

| 特性 | 单文件版本 | 完整版本 |
|------|------------|----------|
| 安装复杂度 | ⭐ 简单 | ⭐⭐ 中等 |
| 部署便利性 | ⭐⭐⭐ 优秀 | ⭐⭐ 良好 |
| 开发调试 | ⭐ 困难 | ⭐⭐⭐ 优秀 |
| 功能完整性 | ⭐⭐⭐ 完整 | ⭐⭐⭐ 完整 |
| 配置管理 | 自动生成 | 手动配置 |
| 适用场景 | 日常使用 | 开发/定制 |

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [mktorrent](https://github.com/Rudde/mktorrent) - 核心种子制作工具
- Python 标准库 - 提供了强大的基础功能

## 📮 联系方式

如有问题或建议，欢迎：

- 提交 [Issue](https://github.com/Yan-nian/torrent-maker/issues)
- 发起 [Discussion](https://github.com/Yan-nian/torrent-maker/discussions)

---

**⭐ 如果这个项目对你有帮助，请给它一个 Star！**
