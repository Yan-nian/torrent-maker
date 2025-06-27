# BUGFIX v1.9.14 - 队列管理修复版本

## 问题描述
用户报告队列功能不正常，具体表现为：
- 队列状态显示有3个等待任务
- 但查看队列详情时显示"队列为空"
- 队列管理功能数据不一致

## 问题分析
通过代码分析发现问题根源：

### 1. 队列文件路径不一致
- **主队列管理器初始化**：使用相对路径 `"torrent_queue.json"`
- **QueueManager默认路径**：使用绝对路径 `"~/.torrent_maker/queue.json"`
- **批量制种队列管理器**：未指定save_file，使用默认路径

### 2. 数据持久化问题
- 队列状态统计从内存中读取（显示正确的任务数量）
- 队列详情从文件中加载（因路径不一致导致加载失败）
- 造成数据显示不一致的问题

## 修复方案

### 1. 统一队列文件路径
```python
# 修复前
self.queue_manager = TorrentQueueManager(
    self.creator,
    max_concurrent=max_workers,
    save_file="torrent_queue.json"  # 相对路径
)

# 修复后
queue_file = os.path.expanduser("~/.torrent_maker/torrent_queue.json")
self.queue_manager = TorrentQueueManager(
    self.creator,
    max_concurrent=max_workers,
    save_file=queue_file  # 绝对路径
)
```

### 2. 修复批量制种队列管理器
```python
# 修复前
queue_manager = TorrentQueueManager(
    torrent_creator=self.creator,
    max_concurrent=max_concurrent
)  # 未指定save_file

# 修复后
queue_file = os.path.expanduser("~/.torrent_maker/torrent_queue.json")
queue_manager = TorrentQueueManager(
    torrent_creator=self.creator,
    max_concurrent=max_concurrent,
    save_file=queue_file  # 使用统一路径
)
```

## 修复效果

### ✅ 解决的问题
1. **队列详情显示正常**：队列详情和状态显示数据一致
2. **数据持久化稳定**：队列数据正确保存和加载
3. **多队列管理器同步**：所有队列管理器使用相同的数据文件
4. **用户体验改善**：队列管理功能完全可用

### 🔧 技术改进
1. **路径管理规范化**：统一使用绝对路径
2. **数据一致性保证**：确保内存和文件数据同步
3. **错误处理增强**：避免路径不一致导致的数据丢失

## 测试验证

### 测试场景
1. **队列恢复测试**：重启程序后队列数据正确恢复
2. **任务添加测试**：新添加的任务在队列详情中正确显示
3. **批量制种测试**：批量制种使用的队列管理器数据同步
4. **状态一致性测试**：队列状态和详情显示数据一致

### 预期结果
- ✅ 队列状态显示：3个等待任务
- ✅ 队列详情显示：3个具体任务信息
- ✅ 数据持久化：重启后数据不丢失
- ✅ 功能完整性：所有队列管理功能正常

## 版本信息
- **修复版本**：v1.9.14
- **修复日期**：2025-06-27
- **影响范围**：队列管理系统
- **兼容性**：向后兼容，无需额外配置

## 相关文件
- `torrent_maker.py`：主程序文件
- `~/.torrent_maker/torrent_queue.json`：队列数据文件

---

**注意**：此修复确保了队列管理系统的数据一致性和稳定性，用户无需进行任何额外配置即可享受修复后的功能。