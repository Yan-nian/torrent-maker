# 🎬 Torrent Maker - 单文件版本

## 📦 简介
这是 Torrent Maker 的**单文件版本**，将所有功能打包到一个 Python 文件中，方便下载和使用。无需安装任何依赖包，只需要 Python 3.7+ 和 mktorrent 工具。

## ✨ 优势
- 📦 **零依赖**：无需安装任何第三方 Python 包
- 🚀 **即下即用**：下载一个文件就能运行
- 💾 **自动配置**：首次运行自动创建配置文件
- 🔧 **完整功能**：包含原版的所有功能
- 📁 **独立配置**：配置文件保存在 `~/.torrent_maker/`

## 🚀 快速开始

### 1. 下载文件
```bash
# 下载单文件版本
wget https://raw.githubusercontent.com/your-repo/torrent-maker/main/torrent_maker.py

# 或者使用 curl
curl -O https://raw.githubusercontent.com/your-repo/torrent-maker/main/torrent_maker.py
```

### 2. 安装依赖（仅 mktorrent）
**macOS:**
```bash
brew install mktorrent
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install mktorrent
```

**CentOS/RHEL:**
```bash
sudo yum install mktorrent
# 或者
sudo dnf install mktorrent
```

### 3. 运行程序
```bash
python3 torrent_maker.py
```

就这么简单！🎉

## 📖 使用方法

### 主菜单
```
🔧 请选择操作:
1. 🔍 搜索并制作种子          # 智能搜索文件夹
2. ⚙️  查看当前配置           # 查看所有设置
3. 📁 设置资源文件夹          # 设置影视剧存放位置
4. 📂 设置输出文件夹          # 设置种子保存位置
5. 🌐 管理 Tracker           # 添加/删除 Tracker
6. 💫 快速制种（直接输入路径）  # 跳过搜索，直接制种
7. ❓ 帮助                   # 查看帮助信息
0. 🚪 退出                   # 退出程序
```

### 核心功能

#### 1. 🔍 智能搜索制种
- 输入影视剧名称（支持中文、英文、部分关键词）
- 自动模糊匹配文件夹
- 显示匹配度、文件数量、大小等信息
- 选择文件夹后一键制种

#### 2. 💫 快速制种
- 直接输入完整文件夹路径
- 跳过搜索步骤
- 适合已知路径的快速操作

#### 3. ⚙️ 配置管理
- **资源文件夹**：存放影视剧的根目录
- **输出文件夹**：种子文件保存位置
- **Tracker 管理**：添加/删除 BitTorrent 追踪器

### 典型使用流程

1. **首次运行**：程序自动创建配置文件
2. **设置路径**：配置资源文件夹和输出文件夹
3. **添加 Tracker**：根据需要添加 Tracker 服务器
4. **制作种子**：使用搜索或快速制种功能

## 📁 配置文件

单文件版本的配置文件保存在用户目录下：
```
~/.torrent_maker/
├── settings.json    # 程序设置
└── trackers.txt     # Tracker 列表
```

### settings.json 示例
```json
{
    "resource_folder": "~/Downloads",
    "output_folder": "~/Desktop/torrents",
    "file_search_tolerance": 60,
    "max_search_results": 10,
    "auto_create_output_dir": true
}
```

### trackers.txt 示例
```
# BitTorrent Tracker 列表
# 每行一个 tracker URL，以 # 开头的行为注释

udp://tracker.openbittorrent.com:80
udp://tracker.opentrackr.org:1337/announce
udp://exodus.desync.com:6969/announce
udp://tracker.torrent.eu.org:451/announce
```

## 🎯 使用场景

### 场景1：影视剧整季打包
```
1. 将整季影视剧放在一个文件夹中
2. 运行程序，选择"搜索并制作种子"
3. 输入剧名，如"权力的游戏"
4. 选择匹配的文件夹，确认制种
```

### 场景2：快速制种已知路径
```
1. 选择"快速制种"
2. 输入完整路径，如"/Users/user/Movies/Game.of.Thrones.S01"
3. 确认制种
```

### 场景3：批量制种多个文件夹
```
1. 使用快速制种功能
2. 逐个输入不同文件夹路径
3. 快速生成多个种子文件
```

## 🔧 高级功能

### 智能匹配算法
- 使用相似度算法进行模糊匹配
- 支持中英文混合搜索
- 自动排序显示最佳匹配

### 自动文件名清理
- 自动处理特殊字符
- 生成安全的种子文件名
- 添加时间戳避免重名

### 详细信息显示
- 文件夹大小计算
- 文件数量统计
- 匹配度百分比显示

## 🐛 故障排除

### 常见问题

**Q: 提示"mktorrent 未安装"？**
A: 请根据系统安装 mktorrent：
- macOS: `brew install mktorrent`
- Ubuntu: `sudo apt-get install mktorrent`

**Q: 找不到配置文件？**
A: 配置文件在 `~/.torrent_maker/` 目录，首次运行会自动创建。

**Q: 搜索结果为空？**
A: 检查：
1. 资源文件夹路径是否正确
2. 搜索关键词是否准确
3. 文件夹是否有读取权限

**Q: 种子创建失败？**
A: 可能原因：
1. mktorrent 未正确安装
2. 源文件夹不可访问
3. 输出目录无写入权限
4. Tracker 列表为空

**Q: 如何备份配置？**
A: 复制 `~/.torrent_maker/` 整个目录即可。

## 📊 与原版对比

| 特性 | 原版 | 单文件版本 |
|------|------|------------|
| 安装复杂度 | 需要多个文件 | 单个文件 |
| 依赖包 | 需要安装 | 无需安装 |
| 配置位置 | 项目目录 | 用户目录 |
| 功能完整性 | ✅ | ✅ |
| 更新方式 | git pull | 下载新文件 |
| 适用场景 | 开发/定制 | 简单使用 |

## 💡 使用技巧

1. **路径设置**：使用绝对路径避免混淆
2. **Tracker 选择**：添加多个 Tracker 提高下载速度
3. **文件夹组织**：规范命名便于搜索匹配
4. **定期备份**：备份配置文件避免重新设置

## 🚀 高级用法

### 命令行集成
可以将 `torrent_maker.py` 放到 PATH 中：
```bash
# 复制到系统路径
sudo cp torrent_maker.py /usr/local/bin/torrent-maker
sudo chmod +x /usr/local/bin/torrent-maker

# 然后就可以直接运行
torrent-maker
```

### 配置模板
为不同用途创建配置模板：
```bash
# 备份当前配置
cp -r ~/.torrent_maker ~/.torrent_maker_backup

# 为不同项目创建不同配置
cp -r ~/.torrent_maker ~/.torrent_maker_movies
cp -r ~/.torrent_maker ~/.torrent_maker_tv
```

## 📜 许可证
MIT License - 自由使用、修改和分发

## 🙏 致谢
- [mktorrent](https://github.com/Rudde/mktorrent) - 核心种子创建工具
- Python 标准库 - 提供所有必需功能

---
**💡 提示**: 单文件版本适合普通用户快速使用，如需定制开发请使用完整版本。
