# Torrent Maker v1.9.19 修复说明

## 版本信息
- **版本号**: v1.9.19
- **版本名称**: 制种命名修复版
- **修复日期**: 2025-06-27
- **修复类型**: 关键Bug修复

## 修复问题

### 1. 制种文件命名错误问题

**问题描述**:
- 队列制种时生成的种子文件名不正确
- 实际生成: `-root_pack_20250627_103753_646084.torrent`
- 期望生成: `Black.Butler.S05.2025.1080p.CR.WEB-DL.H.264.AAC_20250627_103753_646084.torrent`

**根本原因**:
在 `TorrentQueueManager._execute_task()` 方法中，调用 `create_torrent()` 时参数传递错误：
```python
# 错误的调用方式
success = self.torrent_creator.create_torrent(
    task.path,
    output_path,  # 这里错误地将输出路径当作自定义名称传入
    progress_callback=lambda p: self._update_task_progress(task, p)
)
```

**修复方案**:
1. **修正参数传递**: 将 `output_path` 参数移除，使用 `custom_name=None` 让系统根据文件夹名自动命名
2. **正确设置输出目录**: 在调用前更新 `TorrentCreator.output_dir` 属性

**修复代码**:
```python
# 修复后的调用方式
# 设置输出路径
output_path = task.output_path or self.torrent_creator.config_manager.get_output_folder()

# 更新TorrentCreator的输出目录
from pathlib import Path
self.torrent_creator.output_dir = Path(output_path)

# 执行制种
success = self.torrent_creator.create_torrent(
    task.path,
    custom_name=None,  # 使用默认命名（基于文件夹名）
    progress_callback=lambda p: self._update_task_progress(task, p)
)
```

### 2. 日志打印优化

**改进内容**:
- 保持现有的日志打印格式
- 确保任务名称正确显示在日志中
- 维持队列管理的状态跟踪功能

## 技术细节

### 修改文件
- `torrent_maker.py` (第884-890行)

### 修改内容
1. **参数传递修复**: 移除错误的 `output_path` 参数传递
2. **输出目录设置**: 正确设置 `TorrentCreator.output_dir`
3. **版本号更新**: v1.9.18 → v1.9.19

### 影响范围
- ✅ 队列制种功能
- ✅ 批量制种功能
- ✅ 文件命名逻辑
- ✅ 输出路径管理

## 测试验证

### 验证步骤
1. 启动程序并选择队列管理功能
2. 添加制种任务到队列
3. 启动队列处理
4. 检查生成的种子文件名是否正确
5. 验证文件是否保存到正确的输出目录

### 预期结果
- 种子文件名应基于源文件夹名称生成
- 文件名格式: `{文件夹名}_{时间戳}.torrent`
- 文件保存到配置的输出目录

## 兼容性

- ✅ 向后兼容现有配置
- ✅ 不影响单个制种功能
- ✅ 保持现有API接口
- ✅ 维持队列管理功能完整性

## 注意事项

1. **升级建议**: 建议立即升级到此版本以修复命名问题
2. **配置检查**: 升级后请检查输出目录配置是否正确
3. **队列清理**: 建议清理之前生成的错误命名文件

---

**修复完成**: 此版本已完全修复制种文件命名错误问题，确保队列制种功能正常工作。