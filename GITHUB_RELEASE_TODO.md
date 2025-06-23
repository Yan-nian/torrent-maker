# GitHub Release 创建指南

## 问题说明

当前v1.0.2版本的代码已推送到GitHub，但Release还未创建，导致安装脚本无法下载发布包。

## 临时解决方案

安装脚本已修复，现在直接从main分支下载最新版本：

```bash
curl -fsSL https://raw.githubusercontent.com/Yan-nian/torrent-maker/main/install_standalone.sh | bash
```

## 创建GitHub Release的步骤

### 方式一：使用GitHub CLI（推荐）

1. 安装GitHub CLI：
   ```bash
   # macOS
   brew install gh
   
   # Ubuntu
   sudo apt install gh
   ```

2. 登录GitHub：
   ```bash
   gh auth login
   ```

3. 创建Release：
   ```bash
   cd /path/to/torrent-maker
   bash auto_release.sh v1.0.2
   ```

### 方式二：手动在GitHub网页创建

1. 访问：https://github.com/Yan-nian/torrent-maker/releases

2. 点击"Create a new release"

3. 填写信息：
   - **Tag version**: `v1.0.2`
   - **Release title**: `Release v1.0.2 - 断集显示算法智能优化`
   - **Description**: 复制`RELEASE_v1.0.2.md`的内容

4. 上传文件：
   - `release/torrent-maker-standalone.tar.gz`
   - `release/torrent-maker-full.tar.gz`

5. 点击"Publish release"

## 完成后需要做的

1. 恢复安装脚本使用Release下载：
   ```bash
   # 修改install_standalone.sh中的DOWNLOAD_URL
   DOWNLOAD_URL="https://github.com/$REPO/releases/download/$VERSION/torrent-maker-standalone.tar.gz"
   ```

2. 恢复下载和安装函数为解压模式

3. 提交更新

## 当前状态

- ✅ 代码已推送到GitHub main分支
- ✅ 标签v1.0.2已创建
- ✅ 发布包已生成在release/目录
- ✅ 安装脚本已临时修复
- ❌ GitHub Release未创建（需要手动创建）

用户现在可以正常使用一键安装命令获取最新版本！
