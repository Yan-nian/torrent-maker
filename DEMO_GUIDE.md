# Torrent Maker 使用演示指南

## 🎯 演示目标

本指南将展示 `torrent-maker` 的完整功能和使用流程，帮助用户快速上手。

## 📦 一键安装演示

### 1. 基础安装
```bash
# 一键安装（推荐）
curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash
```

### 2. 强制重新安装
```bash
# 如果已安装，强制重新安装
curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash -s -- --force
```

### 3. 静默安装
```bash
# 静默模式安装（减少输出）
curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash -s -- --quiet
```

## 🚀 使用流程演示

### 1. 启动程序
```bash
# 启动单文件版本
python3 ~/.local/bin/torrent_maker.py

# 或者如果已添加到 PATH
torrent_maker.py
```

### 2. 主界面演示
```
🎬 Torrent Maker - 单文件版本
基于 mktorrent 的半自动化种子制作工具
版本：1.0.0 | 许可证：MIT

============================================================
           🎬 种子制作工具 Torrent Maker 🎬
============================================================
   基于 mktorrent 的半自动化种子制作工具
   配置文件位置：/Users/用户名/.torrent_maker
============================================================

🔧 请选择操作:
1. 🔍 搜索并制作种子
2. ⚙️  查看当前配置
3. 📁 设置资源文件夹
4. 📂 设置输出文件夹
5. 🌐 管理 Tracker
6. 💫 快速制种（直接输入路径）
7. ❓ 帮助
0. 🚪 退出
```

### 3. 智能搜索演示

输入 `1` 选择搜索功能，然后输入影视剧名称：

#### 示例：搜索 "权力的游戏"
```
🔍 请输入影视剧名称进行搜索: game of thrones

🎯 找到 3 个匹配项:
════════════════════════════════════════════════════════

📁 1. Game.of.Thrones.S01.1080p.BluRay.x264-Group
   📊 匹配度: 95%
   📂 大小: 15.2 GB
   📄 文件数: 10 个文件
   🎬 剧集信息: S01E01-E10 (共10集)

📁 2. Game.of.Thrones.S02.1080p.WEB-DL.x264-Group  
   📊 匹配度: 92%
   📂 大小: 18.7 GB
   📄 文件数: 10 个文件
   🎬 剧集信息: S02E01-E10 (共10集)

📁 3. Game.of.Thrones.Complete.Series.1080p.BluRay
   📊 匹配度: 89%
   📂 大小: 156.3 GB
   📄 文件数: 73 个文件
   🎬 剧集信息: S01-S08 完整系列
```

### 4. 详细信息查看演示

输入 `d1` 查看第一个匹配项的详细剧集信息：

```
📺 剧集详细信息 - Game.of.Thrones.S01.1080p.BluRay.x264-Group
════════════════════════════════════════════════════════

🎬 第一季 (Season 01) - 共10集:
  📄 Game.of.Thrones.S01E01.Winter.Is.Coming.1080p.BluRay.x264.mkv
  📄 Game.of.Thrones.S01E02.The.Kingsroad.1080p.BluRay.x264.mkv
  📄 Game.of.Thrones.S01E03.Lord.Snow.1080p.BluRay.x264.mkv
  📄 Game.of.Thrones.S01E04.Cripples.Bastards.and.Broken.Things.1080p.BluRay.x264.mkv
  📄 Game.of.Thrones.S01E05.The.Wolf.and.the.Lion.1080p.BluRay.x264.mkv
  📄 Game.of.Thrones.S01E06.A.Golden.Crown.1080p.BluRay.x264.mkv
  📄 Game.of.Thrones.S01E07.You.Win.or.You.Die.1080p.BluRay.x264.mkv
  📄 Game.of.Thrones.S01E08.The.Pointy.End.1080p.BluRay.x264.mkv
  📄 Game.of.Thrones.S01E09.Baelor.1080p.BluRay.x264.mkv
  📄 Game.of.Thrones.S01E10.Fire.and.Blood.1080p.BluRay.x264.mkv

📊 统计信息:
  🗂️  文件夹大小: 15.2 GB
  📁 文件数量: 10 个视频文件
  🎯 剧集范围: S01E01-E10
```

### 5. 断集处理演示

如果遇到断集情况，程序会智能处理：

```
🎬 剧集信息: S01E01-E05, E07-E12 (缺少第6集)
```

### 6. 种子制作演示

选择制作种子后：

```
✅ 选择了: Game.of.Thrones.S01.1080p.BluRay.x264-Group

🔧 开始制作种子文件...
🌐 使用 Tracker: 
   - http://tracker1.example.com:8080/announce
   - http://tracker2.example.com:8080/announce

⚙️  执行命令: mktorrent -a "http://tracker1.example.com:8080/announce" -a "http://tracker2.example.com:8080/announce" -o "/Users/用户名/Downloads/Game.of.Thrones.S01.1080p.BluRay.x264-Group.torrent" "/path/to/Game.of.Thrones.S01.1080p.BluRay.x264-Group"

✅ 种子文件创建成功！
📁 保存位置: /Users/用户名/Downloads/Game.of.Thrones.S01.1080p.BluRay.x264-Group.torrent
```

## 🔧 配置管理演示

### 1. 查看当前配置
选择 `2` 查看配置：

```
⚙️  当前配置
════════════════════════════════════════════════════════

📁 资源文件夹: /Users/用户名/Downloads/TV Shows
📂 输出文件夹: /Users/用户名/Downloads
🌐 Tracker 列表:
   1. http://tracker1.example.com:8080/announce
   2. http://tracker2.example.com:8080/announce
   3. udp://tracker3.example.com:1337/announce

📊 系统信息:
   🐍 Python 版本: 3.11.5
   🔧 mktorrent: 已安装 (v1.1)
   📁 配置文件: /Users/用户名/.torrent_maker/config.json
```

### 2. 设置资源文件夹
选择 `3` 设置资源文件夹：

```
📁 当前资源文件夹: /Users/用户名/Downloads/TV Shows
请输入新的资源文件夹路径 (直接回车保持不变): /path/to/media

✅ 资源文件夹已更新为: /path/to/media
```

### 3. 管理 Tracker
选择 `5` 管理 Tracker：

```
🌐 Tracker 管理
════════════════════════════════════════════════════════

当前 Tracker 列表:
1. http://tracker1.example.com:8080/announce
2. http://tracker2.example.com:8080/announce
3. udp://tracker3.example.com:1337/announce

请选择操作:
1. 添加 Tracker
2. 删除 Tracker
3. 清空所有 Tracker
4. 恢复默认 Tracker
0. 返回主菜单
```

## 🚀 快速制种演示

选择 `6` 快速制种功能：

```
💫 快速制种模式
════════════════════════════════════════════════════════

请输入要制种的文件或文件夹完整路径:
/path/to/video/folder

🔍 路径验证通过!
📁 目标: /path/to/video/folder
📊 大小: 25.6 GB
📄 文件数: 12 个文件

🎬 检测到剧集信息: S01E01-E12 (共12集)

确认制作种子? (y/N): y

🔧 开始制作种子文件...
✅ 种子文件创建成功！
📁 保存位置: /Users/用户名/Downloads/folder.torrent
```

## 🎨 特色功能演示

### 1. 智能搜索特色
- **多分隔符支持**：支持空格、点、下划线、连字符
- **首字母缩写**：输入 "GOT" 可匹配 "Game.of.Thrones"
- **关键词重叠**：智能计算关键词重叠度
- **评分排序**：按匹配度从高到低排序

### 2. 剧集解析特色
- **多格式支持**：S01E01、1x01、E01、第1集等
- **断集检测**：自动检测并显示缺失集数
- **连续合并**：连续集数自动合并显示
- **季度识别**：自动识别季数信息

### 3. 用户体验特色
- **彩色界面**：使用颜色增强可读性
- **图标美化**：使用 emoji 图标美化界面
- **实时反馈**：操作过程实时显示进度
- **错误处理**：友好的错误提示和处理

## 📝 总结

`torrent-maker` 提供了：

✅ **简单易用**：一键安装，直观操作界面
✅ **功能完整**：从搜索到制种的完整流程
✅ **智能高效**：先进的搜索算法和剧集解析
✅ **高度可配置**：支持自定义路径和 Tracker
✅ **跨平台支持**：支持 macOS 和 Linux
✅ **持续更新**：活跃的开发和维护

开始使用：
```bash
curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash
```
