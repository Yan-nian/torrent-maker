# 🤖 GitHub CLI 安装和自动发布指南

## 📥 安装 GitHub CLI

### macOS (推荐使用 Homebrew)
```bash
brew install gh
```

### 其他安装方式
```bash
# 使用 MacPorts
sudo port install gh

# 使用 conda
conda install gh --channel conda-forge

# 手动下载
# 访问 https://github.com/cli/cli/releases
```

## 🔐 登录 GitHub

安装完成后，需要登录您的 GitHub 账户：

```bash
gh auth login
```

按照提示选择：
1. **GitHub.com** (不是 GitHub Enterprise Server)
2. **HTTPS** (推荐)
3. **Yes** (上传 SSH 公钥，如果需要)
4. **Login with a web browser** (网页登录)

## 🚀 自动发布 Release

登录完成后，运行自动发布脚本：

```bash
./auto_release.sh
```

脚本会自动：
- ✅ 创建新的 Git tag (v1.0.1)
- ✅ 重新生成发布包
- ✅ 创建 GitHub Release
- ✅ 上传所有发布文件
- ✅ 设置为最新版本

## 🎯 手动发布（如果不想安装 GitHub CLI）

如果您不想安装 GitHub CLI，也可以手动发布：

### 1. 创建新版本标签
```bash
git tag v1.0.1
git push origin v1.0.1
```

### 2. 在 GitHub 网页上创建 Release
1. 访问：https://github.com/Yan-nian/torrent-maker/releases
2. 点击 "Create a new release"
3. 选择标签：v1.0.1
4. 标题：Torrent Maker v1.0.1
5. 描述：复制 `auto_release.sh` 中的 RELEASE_NOTES 内容
6. 上传文件：
   - `release/torrent-maker-standalone.tar.gz`
   - `release/torrent-maker-full.tar.gz`
7. 勾选 "Set as the latest release"
8. 点击 "Publish release"

## 🎉 验证发布

发布完成后，检查：
- 📦 Release 页面：https://github.com/Yan-nian/torrent-maker/releases
- 🔗 下载链接是否工作正常
- ⭐ 为项目点 Star！

## 🔄 未来版本发布

对于后续版本，只需：
1. 修改 `auto_release.sh` 中的 `VERSION` 变量
2. 运行 `./auto_release.sh`

一键发布，简单快捷！
