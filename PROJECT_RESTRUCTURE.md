# 📁 Torrent Maker 项目结构重组说明

## 🎯 重组目标

将项目结构重组为以**单文件版本**为核心的架构，淘汰过时的模块化版本。

## 📊 当前项目结构分析

### 🔍 现有文件分类

#### ✅ 保留文件（核心功能）
```
torrent_maker.py              # 主程序（v1.5.0 高性能版）
version_config.json           # 版本配置管理
requirements.txt              # Python 依赖
setup.py                     # 安装配置
```

#### ✅ 保留文件（配置和脚本）
```
config/
├── settings.json            # 默认配置
└── trackers.txt            # 默认 Tracker 列表

install.sh                   # 安装脚本
install_standalone.sh        # 单文件版本安装脚本
auto_release.sh             # 自动发布脚本
release.sh                  # 发布脚本
version_manager.py          # 版本管理工具
```

#### ✅ 保留文件（文档）
```
README.md                   # 主要文档（已更新）
MIGRATION_GUIDE.md          # 迁移指南（新建）
CHANGELOG.md               # 更新日志
LICENSE                    # 许可证
```

#### ✅ 保留文件（测试和演示）
```
performance_test_v1.5.0.py    # v1.5.0 性能测试
demo_performance_v1.5.0.py    # v1.5.0 性能演示
test_*.py                     # 各种测试文件
```

#### ⚠️ 标记为弃用（模块化版本）
```
src/                         # 模块化版本目录（已添加弃用警告）
├── main.py                 # 主程序（已添加弃用警告）
├── config_manager.py       # 配置管理器
├── file_matcher.py         # 文件匹配器
├── torrent_creator.py      # 种子创建器
├── performance_monitor.py  # 性能监控
├── search_history.py       # 搜索历史
├── statistics_manager.py   # 统计管理器
└── utils/                  # 工具模块
```

#### 🗑️ 可清理文件（备份和临时）
```
torrent_maker_v1.1.0_backup.py    # 旧版本备份
torrent_maker_v1.1.0_original.py  # 旧版本原始文件
__pycache__/                      # Python 缓存目录
src/__pycache__/                  # 模块缓存目录
```

## 🔄 重组计划

### 阶段一：立即执行（已完成）
- [x] 在模块化版本添加弃用警告
- [x] 更新 README.md 推荐单文件版本
- [x] 创建迁移指南文档
- [x] 统一版本号为 v1.5.0

### 阶段二：结构优化（当前阶段）
- [ ] 移动模块化版本到 `deprecated/` 目录
- [ ] 清理旧版本备份文件
- [ ] 清理 Python 缓存目录
- [ ] 更新安装脚本优先使用单文件版本

### 阶段三：下个版本执行
- [ ] 完全移除 `deprecated/` 目录
- [ ] 移除模块化版本相关的配置
- [ ] 简化项目结构

## 📁 目标项目结构

```
torrent-maker/
├── torrent_maker.py           # 主程序（单文件版本）
├── README.md                  # 主要文档
├── MIGRATION_GUIDE.md         # 迁移指南
├── CHANGELOG.md              # 更新日志
├── LICENSE                   # 许可证
├── requirements.txt          # 依赖文件
├── setup.py                 # 安装配置
├── version_config.json       # 版本配置
├── version_manager.py        # 版本管理工具
├── config/                   # 配置文件
│   ├── settings.json
│   └── trackers.txt
├── scripts/                  # 脚本目录
│   ├── install.sh
│   ├── install_standalone.sh
│   ├── auto_release.sh
│   └── release.sh
├── tests/                    # 测试目录
│   ├── performance_test_v1.5.0.py
│   ├── demo_performance_v1.5.0.py
│   └── test_*.py
├── docs/                     # 文档目录
│   ├── PERFORMANCE_OPTIMIZATION_v1.5.0.md
│   ├── USER_EXPERIENCE_OPTIMIZATION_REPORT.md
│   └── *.md
├── release/                  # 发布目录
│   ├── standalone/
│   └── full/
└── deprecated/               # 弃用文件（临时）
    └── src/                  # 原模块化版本
```

## 🚀 执行重组

### 当前执行的操作

1. **创建目录结构**
```bash
mkdir -p scripts tests docs deprecated
```

2. **移动文件到合适位置**
```bash
# 移动脚本文件
mv install.sh install_standalone.sh auto_release.sh release.sh scripts/

# 移动测试文件
mv performance_test_v1.5.0.py demo_performance_v1.5.0.py test_*.py tests/

# 移动文档文件
mv *_REPORT.md *_OPTIMIZATION*.md docs/

# 移动弃用的模块化版本
mv src/ deprecated/
```

3. **清理缓存和备份文件**
```bash
# 清理 Python 缓存
rm -rf __pycache__ src/__pycache__

# 清理旧版本备份
rm -f torrent_maker_v1.1.0_*.py
```

## ⚠️ 注意事项

### 保持兼容性
- 保留现有配置文件位置和格式
- 确保安装脚本正常工作
- 维护现有的 API 和命令行接口

### 用户通知
- 在下个版本发布说明中明确说明结构变化
- 提供清晰的迁移指南
- 保持向后兼容性直到用户完全迁移

### 测试验证
- 验证单文件版本在新结构下正常工作
- 测试所有安装脚本和工具
- 确保发布流程正常

## 📈 预期效果

重组完成后：
- ✅ **项目结构更清晰**：主程序突出，辅助文件分类明确
- ✅ **维护成本降低**：只需维护一个主版本
- ✅ **用户体验改善**：减少版本选择困惑
- ✅ **部署更简单**：单文件版本为主，依赖更少
- ✅ **开发效率提升**：专注于单一版本的功能开发

## 🎯 总结

这次重组将 Torrent Maker 从双版本架构简化为以高性能单文件版本为核心的单一架构，大幅提升了项目的可维护性和用户体验。
