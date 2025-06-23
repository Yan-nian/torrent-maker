# 紧急安装说明 - 绕过缓存问题

## 问题说明
你遇到的 "gzip: stdin: not in gzip format" 错误是因为使用了缓存的旧版本安装脚本。

## 立即解决方案

### 方案一：强制绕过缓存
```bash
curl -fsSL "https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh?$(date +%s)" | bash
```

### 方案二：直接下载单文件（推荐）
```bash
# 创建安装目录
mkdir -p ~/.local/bin

# 下载单文件
curl -o ~/.local/bin/torrent_maker.py https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/torrent_maker.py

# 设置执行权限
chmod +x ~/.local/bin/torrent_maker.py

# 运行
python3 ~/.local/bin/torrent_maker.py
```

### 方案三：临时下载到当前目录
```bash
# 下载到当前目录
curl -o torrent_maker.py https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/torrent_maker.py

# 运行
python3 torrent_maker.py
```

## 验证安装脚本版本
如果仍要使用安装脚本，请确认看到以下信息：
```
🎬 Torrent Maker 单文件版本安装器
==================================
版本: v1.0.2 (安装脚本: v1.0.2-fix)
仓库: https://github.com/Yan-nian/torrent-maker

ℹ️  检查 Python 环境...
ℹ️  使用直接下载模式 (v1.0.2-fix)
ℹ️  下载地址: https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/torrent_maker.py
ℹ️  跳过解压步骤 (直接下载单文件)
```

如果没有看到 "v1.0.2-fix" 标识，说明使用的是缓存版本。

## 添加到PATH（可选）
```bash
# 添加到shell配置文件
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc  # 或 ~/.zshrc
source ~/.bashrc  # 或 source ~/.zshrc

# 现在可以直接使用
torrent_maker.py
```

推荐使用方案二，最直接有效！
