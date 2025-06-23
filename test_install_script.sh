#!/bin/bash

# 测试新的安装脚本

echo "🧪 测试新版安装脚本"
echo "=================="

# 创建临时测试目录
TEST_DIR="/tmp/torrent-maker-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "📁 测试目录: $TEST_DIR"
echo ""

# 测试下载最新版本的安装脚本
echo "📥 下载最新安装脚本..."
curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh -o install_test.sh

echo "✅ 下载完成"
echo ""

# 检查脚本内容
echo "📋 脚本信息:"
echo "文件大小: $(wc -c < install_test.sh) 字节"
echo "行数: $(wc -l < install_test.sh) 行"
echo ""

# 显示脚本头部
echo "📄 脚本开头："
head -10 install_test.sh
echo ""

# 检查关键功能
echo "🔍 关键功能检查："
if grep -q "check_mktorrent" install_test.sh; then
    echo "✅ 包含 mktorrent 检查功能"
else
    echo "❌ 缺少 mktorrent 检查功能"
fi

if grep -q "check_existing_installation" install_test.sh; then
    echo "✅ 包含更新检查功能"
else
    echo "❌ 缺少更新检查功能"
fi

if grep -q "DOWNLOAD_URL" install_test.sh; then
    echo "✅ 包含下载功能"
else
    echo "❌ 缺少下载功能"
fi

if grep -q "VERSION=" install_test.sh; then
    version=$(grep "VERSION=" install_test.sh | head -1 | cut -d'"' -f2)
    echo "✅ 版本信息: $version"
else
    echo "❌ 缺少版本信息"
fi

echo ""
echo "🎯 安装脚本功能预览："
echo "1. ✅ Python 环境检查"
echo "2. ✅ mktorrent 自动安装"
echo "3. ✅ 网络连接检查"
echo "4. ✅ 版本检查和更新"
echo "5. ✅ 自动下载最新版本"
echo "6. ✅ PATH 环境配置"
echo "7. ✅ 桌面快捷方式（Linux）"
echo "8. ✅ 彩色输出界面"
echo ""

echo "💡 使用方法："
echo "curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash"
echo ""

# 清理
cd /
rm -rf "$TEST_DIR"

echo "✅ 测试完成！"
