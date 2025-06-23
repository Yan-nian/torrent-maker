# 贡献指南

感谢您对 torrent-maker 项目的兴趣！我们欢迎所有形式的贡献。

## 如何贡献

### 报告 Bug
1. 查看 [Issues](https://github.com/your-username/torrent-maker/issues) 确认是否已有相同问题
2. 如果没有，请创建新的 Issue，使用 Bug Report 模板
3. 提供详细的重现步骤和环境信息

### 提出功能建议
1. 查看 [Issues](https://github.com/your-username/torrent-maker/issues) 确认是否已有相同建议
2. 如果没有，请创建新的 Issue，使用 Feature Request 模板
3. 详细描述您的需求和使用场景

### 贡献代码

#### 开发环境设置
```bash
# 1. Fork 并克隆仓库
git clone https://github.com/your-username/torrent-maker.git
cd torrent-maker

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行测试
python test.py
```

#### 提交流程
1. 从 main 分支创建新的功能分支
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 进行开发并添加测试

3. 确保所有测试通过
   ```bash
   python test.py
   python test_episodes.py
   python test_enhanced_search.py
   ```

4. 提交更改
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. 推送分支并创建 Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

#### 代码规范
- 使用 4 个空格缩进
- 函数和变量使用 snake_case 命名
- 类名使用 PascalCase 命名
- 添加适当的注释和文档字符串
- 遵循 PEP 8 编码规范

#### 提交信息规范
使用以下前缀：
- `feat:` 新功能
- `fix:` bug 修复
- `docs:` 文档更新
- `test:` 测试相关
- `refactor:` 代码重构
- `style:` 代码格式调整

## 项目结构

```
torrent-maker/
├── src/                  # 源代码
│   ├── main.py          # 主程序
│   ├── config_manager.py # 配置管理
│   ├── file_matcher.py   # 文件匹配
│   └── torrent_creator.py # 种子创建
├── config/              # 配置文件
├── tests/               # 测试文件
└── docs/                # 文档
```

## 测试

项目包含多个测试模块：

- `test.py` - 基本功能测试
- `test_episodes.py` - 剧集解析测试
- `test_enhanced_search.py` - 搜索算法测试
- `test_episode_gaps.py` - 断集处理测试

运行测试时请确保所有测试都通过。

## 发布流程

1. 更新版本号（setup.py、README.md 等）
2. 更新 CHANGELOG.md
3. 创建 git tag
4. GitHub Actions 会自动构建和发布

## 疑问？

如果您有任何疑问，请：
- 查看现有的 [Issues](https://github.com/your-username/torrent-maker/issues)
- 创建新的 [Discussion](https://github.com/your-username/torrent-maker/discussions)
- 发送邮件给维护者

感谢您的贡献！
