#!/bin/bash

# Torrent Maker 发布脚本
# 用于准备发布包

echo "🚀 Torrent Maker 发布脚本"
echo "========================"

# 创建发布目录
RELEASE_DIR="release"
STANDALONE_DIR="$RELEASE_DIR/standalone"
FULL_DIR="$RELEASE_DIR/full"

echo "📁 创建发布目录..."
rm -rf "$RELEASE_DIR"
mkdir -p "$STANDALONE_DIR"
mkdir -p "$FULL_DIR"

# 准备单文件版本
echo "📦 准备单文件版本..."
cp torrent_maker.py "$STANDALONE_DIR/"
cp README_STANDALONE.md "$STANDALONE_DIR/README.md"
cp LICENSE "$STANDALONE_DIR/"
cp install_standalone.sh "$STANDALONE_DIR/install.sh"

# 准备完整版本
echo "📦 准备完整版本..."
cp -r src "$FULL_DIR/"
cp -r config "$FULL_DIR/"
cp README.md "$FULL_DIR/"
cp LICENSE "$FULL_DIR/"
cp requirements.txt "$FULL_DIR/"
cp setup.py "$FULL_DIR/"
cp run.py "$FULL_DIR/"
cp install.sh "$FULL_DIR/"
cp test.py "$FULL_DIR/"

# 创建压缩包
echo "🗜️  创建压缩包..."
cd "$RELEASE_DIR"

# 单文件版本压缩包
echo "压缩单文件版本..."
tar -czf torrent-maker-standalone.tar.gz standalone/
zip -r torrent-maker-standalone.zip standalone/

# 完整版本压缩包
echo "压缩完整版本..."
tar -czf torrent-maker-full.tar.gz full/
zip -r torrent-maker-full.zip full/

cd ..

# 显示文件大小
echo ""
echo "📊 发布包信息:"
echo "=============="
ls -lh "$RELEASE_DIR"/*.tar.gz "$RELEASE_DIR"/*.zip

echo ""
echo "✅ 发布包准备完成！"
echo ""
echo "📁 发布目录: $RELEASE_DIR/"
echo "   ├── 📦 torrent-maker-standalone.tar.gz  (单文件版本)"
echo "   ├── 📦 torrent-maker-standalone.zip"
echo "   ├── 📦 torrent-maker-full.tar.gz        (完整版本)"
echo "   └── 📦 torrent-maker-full.zip"
echo ""
echo "🌐 使用建议:"
echo "   - 普通用户推荐下载: torrent-maker-standalone.*"
echo "   - 开发者推荐下载: torrent-maker-full.*"
echo ""
echo "📋 单文件版本使用方法:"
echo "   1. 下载并解压 torrent-maker-standalone.*"
echo "   2. 运行: python3 torrent_maker.py"
echo ""
echo "📋 完整版本使用方法:"
echo "   1. 下载并解压 torrent-maker-full.*"
echo "   2. 运行: ./install.sh && python3 run.py"
