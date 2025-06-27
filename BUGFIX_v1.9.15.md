# BUGFIX v1.9.15 - 制种失败问题修复版本

## 修复概述

本版本主要修复了制种失败的两个核心问题：tracker URL格式错误和文件名冲突问题，显著提升了制种成功率和系统稳定性。

## 问题分析

### 问题1：Tracker URL格式错误
**错误现象：**
```bash
-a ' `https://tracker.qingwapt.org` '
```

**根本原因：**
- `_load_trackers` 方法读取 `trackers.txt` 时未对URL格式进行清理
- tracker URL被意外加上了反引号等非法字符
- 导致 mktorrent 命令参数格式错误

### 问题2：文件名冲突
**错误现象：**
```bash
mktorrent: /root/pack/_root_pack_20250627_090411.torrent: File exists
```

**根本原因：**
- 时间戳精度只到秒级（`%Y%m%d_%H%M%S`）
- 并发任务或快速连续任务产生相同文件名
- 缺少文件冲突检测机制

## 修复方案

### 1. 修复 Tracker URL 处理

**文件位置：** `torrent_maker.py` - `_load_trackers` 方法（第2346行）

**修改前：**
```python
for line in f:
    line = line.strip()
    if line and not line.startswith('#'):
        trackers.append(line)
```

**修改后：**
```python
for line in f:
    line = line.strip()
    if line and not line.startswith('#'):
        # 清理URL格式，移除可能的反引号和其他非法字符
        cleaned_line = line.strip('`"\'')
        # 基本URL格式验证
        if cleaned_line.startswith(('http://', 'https://', 'udp://')):
            trackers.append(cleaned_line)
        else:
            print(f"⚠️  跳过无效的tracker URL: {line}")
```

**改进效果：**
- 自动清理URL中的反引号、双引号、单引号
- 添加基本URL格式验证
- 跳过无效URL并给出警告提示

### 2. 改进时间戳精度

**文件位置：** `torrent_maker.py` - 第4797行和6189行

**修改前：**
```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = self.output_dir / f"{torrent_name}_{timestamp}.torrent"
```

**修改后：**
```python
# 使用微秒级时间戳确保文件名唯一性
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
output_file = self.output_dir / f"{torrent_name}_{timestamp}.torrent"

# 文件冲突检测和重试机制
retry_count = 0
while output_file.exists() and retry_count < 5:
    retry_count += 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_file = self.output_dir / f"{torrent_name}_{timestamp}_retry{retry_count}.torrent"
```

**改进效果：**
- 时间戳精度从秒级提升到微秒级
- 添加文件存在检测和重试机制
- 最多重试5次，确保文件名唯一性

### 3. 版本信息更新

**修改内容：**
- 版本号：`v1.9.14` → `v1.9.15`
- 添加版本更新说明
- 更新版本历史记录

## 测试验证

### 测试用例1：Tracker URL格式
**输入：** `trackers.txt` 包含带反引号的URL
```
`https://tracker.qingwapt.com`
`https://tracker.qingwapt.org`
```

**预期结果：** 自动清理格式，生成正确的mktorrent命令
```bash
-a 'https://tracker.qingwapt.com'
-a 'https://tracker.qingwapt.org'
```

### 测试用例2：文件名唯一性
**场景：** 快速连续创建多个种子文件
**预期结果：** 每个文件都有唯一的文件名
```
_root_pack_20250627_090411_123456.torrent
_root_pack_20250627_090411_234567.torrent
_root_pack_20250627_090411_345678.torrent
```

## 兼容性说明

- ✅ **向后兼容**：不影响现有功能
- ✅ **配置兼容**：现有配置文件无需修改
- ✅ **API兼容**：不改变对外接口

## 性能影响

- **微秒级时间戳**：性能影响可忽略不计
- **URL格式验证**：轻微增加启动时间（<1ms）
- **文件冲突检测**：仅在冲突时触发，正常情况无影响

## 风险评估

- **风险等级**：低
- **影响范围**：制种功能优化
- **回滚方案**：可直接回退到v1.9.14

## 部署建议

1. **测试环境验证**：先在测试环境验证修复效果
2. **备份配置**：部署前备份现有配置文件
3. **监控制种**：部署后监控制种成功率
4. **日志检查**：关注tracker URL警告信息

## 后续优化

1. **增强URL验证**：添加更严格的URL格式检查
2. **配置文件检查**：启动时检查配置文件格式
3. **错误统计**：添加制种失败原因统计
4. **自动修复**：自动修复常见的配置文件格式问题

---

**修复版本**：v1.9.15  
**修复日期**：2024年12月27日  
**修复类型**：Bug修复  
**优先级**：高  
**测试状态**：待验证