#!/bin/bash

# 测试强制安装功能

echo "🧪 测试安装脚本的强制安装功能"
echo "=============================="

# 模拟测试环境
TEST_DIR="/tmp/torrent-maker-force-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "📁 测试目录: $TEST_DIR"
echo ""

echo "📥 下载最新安装脚本..."
curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh -o install_test.sh

echo "✅ 下载完成"
echo ""

echo "🔍 检查强制安装参数支持:"
if grep -q "\-\-force" install_test.sh; then
    echo "✅ 支持 --force 参数"
else
    echo "❌ 不支持 --force 参数"
fi

if grep -q "\-\-quiet" install_test.sh; then
    echo "✅ 支持 --quiet 参数"
else
    echo "❌ 不支持 --quiet 参数"
fi

if grep -q "\-\-help" install_test.sh; then
    echo "✅ 支持 --help 参数"
else
    echo "❌ 不支持 --help 参数"
fi

echo ""
echo "📋 帮助信息测试:"
bash install_test.sh --help 2>/dev/null | head -10

echo ""
echo "💡 现在用户可以这样强制重新安装:"
echo "curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash -s -- --force"
echo ""
echo "或者静默安装:"
echo "curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash -s -- --quiet"

# 清理
cd /
rm -rf "$TEST_DIR"

echo ""
echo "✅ 测试完成！"
