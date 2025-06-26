#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Torrent Maker - 错误处理模块
智能错误分析、分类和恢复系统
"""

import os
import re
import time
import logging
import traceback
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path


class ErrorType(Enum):
    """错误类型枚举"""
    FILE_SYSTEM = "file_system"
    PERMISSION = "permission"
    DISK_SPACE = "disk_space"
    MKTORRENT = "mktorrent"
    NETWORK = "network"
    CONFIG = "config"
    SYSTEM_RESOURCE = "system_resource"
    ENCODING = "encoding"
    UNKNOWN = "unknown"


class ErrorSeverity(Enum):
    """错误严重程度"""
    LOW = "low"          # 可忽略的警告
    MEDIUM = "medium"    # 需要注意但不影响主要功能
    HIGH = "high"        # 影响功能，需要处理
    CRITICAL = "critical" # 严重错误，必须立即处理


@dataclass
class ErrorInfo:
    """错误信息数据类"""
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    original_error: str
    file_path: Optional[str] = None
    suggested_solutions: List[str] = None
    auto_recoverable: bool = False
    retry_count: int = 0
    max_retries: int = 3
    timestamp: float = None
    
    def __post_init__(self):
        if self.suggested_solutions is None:
            self.suggested_solutions = []
        if self.timestamp is None:
            self.timestamp = time.time()


class ErrorHandler:
    """智能错误处理器"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.error_patterns = self._init_error_patterns()
        self.solution_database = self._init_solution_database()
        self.error_history: List[ErrorInfo] = []
        self.retry_delays = [1, 2, 5, 10]  # 重试延迟（秒）
        
        # 设置日志
        self.logger = self._setup_logger(log_file)
    
    def _setup_logger(self, log_file: Optional[str]) -> logging.Logger:
        """设置错误日志记录器"""
        logger = logging.getLogger('torrent_maker_errors')
        logger.setLevel(logging.DEBUG)
        
        # 避免重复添加处理器
        if logger.handlers:
            return logger
        
        # 文件处理器
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        # 控制台处理器（仅错误和严重错误）
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _init_error_patterns(self) -> Dict[ErrorType, List[Tuple[str, ErrorSeverity]]]:
        """初始化错误模式匹配规则"""
        return {
            ErrorType.FILE_SYSTEM: [
                (r"No such file or directory", ErrorSeverity.HIGH),
                (r"File not found", ErrorSeverity.HIGH),
                (r"Is a directory", ErrorSeverity.MEDIUM),
                (r"Not a directory", ErrorSeverity.MEDIUM),
                (r"Directory not empty", ErrorSeverity.MEDIUM),
                (r"File exists", ErrorSeverity.LOW),
            ],
            ErrorType.PERMISSION: [
                (r"Permission denied", ErrorSeverity.HIGH),
                (r"Access denied", ErrorSeverity.HIGH),
                (r"Operation not permitted", ErrorSeverity.HIGH),
                (r"Insufficient privileges", ErrorSeverity.HIGH),
            ],
            ErrorType.DISK_SPACE: [
                (r"No space left on device", ErrorSeverity.CRITICAL),
                (r"Disk full", ErrorSeverity.CRITICAL),
                (r"Not enough space", ErrorSeverity.HIGH),
                (r"Insufficient disk space", ErrorSeverity.HIGH),
            ],
            ErrorType.MKTORRENT: [
                (r"mktorrent.*not found", ErrorSeverity.CRITICAL),
                (r"mktorrent.*command not found", ErrorSeverity.CRITICAL),
                (r"Invalid piece size", ErrorSeverity.MEDIUM),
                (r"Invalid announce URL", ErrorSeverity.MEDIUM),
                (r"mktorrent.*failed", ErrorSeverity.HIGH),
            ],
            ErrorType.NETWORK: [
                (r"Connection refused", ErrorSeverity.MEDIUM),
                (r"Network unreachable", ErrorSeverity.MEDIUM),
                (r"Timeout", ErrorSeverity.LOW),
                (r"DNS resolution failed", ErrorSeverity.MEDIUM),
            ],
            ErrorType.CONFIG: [
                (r"Invalid configuration", ErrorSeverity.MEDIUM),
                (r"Configuration file not found", ErrorSeverity.MEDIUM),
                (r"Invalid JSON", ErrorSeverity.MEDIUM),
                (r"Missing required setting", ErrorSeverity.HIGH),
            ],
            ErrorType.SYSTEM_RESOURCE: [
                (r"Out of memory", ErrorSeverity.CRITICAL),
                (r"Memory allocation failed", ErrorSeverity.CRITICAL),
                (r"Too many open files", ErrorSeverity.HIGH),
                (r"Resource temporarily unavailable", ErrorSeverity.MEDIUM),
            ],
            ErrorType.ENCODING: [
                (r"UnicodeDecodeError", ErrorSeverity.MEDIUM),
                (r"UnicodeEncodeError", ErrorSeverity.MEDIUM),
                (r"codec can't decode", ErrorSeverity.MEDIUM),
                (r"invalid start byte", ErrorSeverity.MEDIUM),
            ]
        }
    
    def _init_solution_database(self) -> Dict[ErrorType, List[str]]:
        """初始化解决方案数据库"""
        return {
            ErrorType.FILE_SYSTEM: [
                "检查文件路径是否正确",
                "确认文件是否存在",
                "检查文件名是否包含特殊字符",
                "尝试使用绝对路径",
                "检查文件是否被其他程序占用"
            ],
            ErrorType.PERMISSION: [
                "检查文件和目录的读写权限",
                "尝试使用管理员权限运行",
                "修改文件所有者和权限设置",
                "检查父目录的权限设置",
                "确认当前用户有足够的权限"
            ],
            ErrorType.DISK_SPACE: [
                "清理磁盘空间，删除不必要的文件",
                "选择其他有足够空间的磁盘",
                "压缩或移动大文件到其他位置",
                "清空回收站和临时文件",
                "检查磁盘配额设置"
            ],
            ErrorType.MKTORRENT: [
                "安装 mktorrent 工具",
                "检查 mktorrent 是否在系统 PATH 中",
                "验证 mktorrent 版本兼容性",
                "检查命令行参数是否正确",
                "尝试重新安装 mktorrent"
            ],
            ErrorType.NETWORK: [
                "检查网络连接状态",
                "验证 tracker URL 是否有效",
                "尝试使用其他 tracker",
                "检查防火墙设置",
                "稍后重试网络操作"
            ],
            ErrorType.CONFIG: [
                "检查配置文件格式是否正确",
                "恢复默认配置设置",
                "验证配置参数的有效性",
                "重新生成配置文件",
                "检查配置文件权限"
            ],
            ErrorType.SYSTEM_RESOURCE: [
                "关闭不必要的程序释放内存",
                "减少并发操作数量",
                "重启应用程序",
                "检查系统资源使用情况",
                "升级系统硬件配置"
            ],
            ErrorType.ENCODING: [
                "检查文件名编码格式",
                "使用 UTF-8 编码保存文件",
                "重命名包含特殊字符的文件",
                "检查系统区域设置",
                "尝试使用英文路径和文件名"
            ]
        }
    
    def analyze_error(self, error: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
        """分析错误并返回错误信息"""
        error_str = str(error)
        error_type = self._classify_error(error_str)
        severity = self._determine_severity(error_type, error_str)
        
        # 生成用户友好的错误消息
        friendly_message = self._generate_friendly_message(error_type, error_str)
        
        # 获取建议解决方案
        solutions = self.solution_database.get(error_type, [])
        
        # 判断是否可以自动恢复
        auto_recoverable = self._is_auto_recoverable(error_type, severity)
        
        error_info = ErrorInfo(
            error_type=error_type,
            severity=severity,
            message=friendly_message,
            original_error=error_str,
            file_path=context.get('file_path') if context else None,
            suggested_solutions=solutions.copy(),
            auto_recoverable=auto_recoverable
        )
        
        # 记录错误
        self._log_error(error_info, context)
        self.error_history.append(error_info)
        
        return error_info
    
    def _classify_error(self, error_str: str) -> ErrorType:
        """根据错误信息分类错误类型"""
        for error_type, patterns in self.error_patterns.items():
            for pattern, _ in patterns:
                if re.search(pattern, error_str, re.IGNORECASE):
                    return error_type
        return ErrorType.UNKNOWN
    
    def _determine_severity(self, error_type: ErrorType, error_str: str) -> ErrorSeverity:
        """确定错误严重程度"""
        patterns = self.error_patterns.get(error_type, [])
        for pattern, severity in patterns:
            if re.search(pattern, error_str, re.IGNORECASE):
                return severity
        return ErrorSeverity.MEDIUM
    
    def _generate_friendly_message(self, error_type: ErrorType, error_str: str) -> str:
        """生成用户友好的错误消息"""
        friendly_messages = {
            ErrorType.FILE_SYSTEM: "文件系统错误：无法访问指定的文件或目录",
            ErrorType.PERMISSION: "权限错误：没有足够的权限执行此操作",
            ErrorType.DISK_SPACE: "磁盘空间不足：无法完成文件操作",
            ErrorType.MKTORRENT: "制种工具错误：mktorrent 执行失败",
            ErrorType.NETWORK: "网络错误：无法连接到指定的服务器",
            ErrorType.CONFIG: "配置错误：配置文件存在问题",
            ErrorType.SYSTEM_RESOURCE: "系统资源不足：内存或其他资源耗尽",
            ErrorType.ENCODING: "编码错误：文件名或路径包含不支持的字符",
            ErrorType.UNKNOWN: "未知错误：发生了意外的问题"
        }
        
        base_message = friendly_messages.get(error_type, "发生了未知错误")
        
        # 添加更具体的信息
        if "Permission denied" in error_str:
            return f"{base_message}，请检查文件权限设置"
        elif "No space left" in error_str:
            return f"{base_message}，请清理磁盘空间后重试"
        elif "not found" in error_str:
            return f"{base_message}，请检查文件路径是否正确"
        
        return base_message
    
    def _is_auto_recoverable(self, error_type: ErrorType, severity: ErrorSeverity) -> bool:
        """判断错误是否可以自动恢复"""
        # 严重错误通常不能自动恢复
        if severity == ErrorSeverity.CRITICAL:
            return False
        
        # 某些类型的错误可以尝试自动恢复
        recoverable_types = {
            ErrorType.NETWORK,      # 网络错误可以重试
            ErrorType.SYSTEM_RESOURCE,  # 资源不足可以等待后重试
        }
        
        return error_type in recoverable_types
    
    def _log_error(self, error_info: ErrorInfo, context: Dict[str, Any] = None) -> None:
        """记录错误到日志"""
        log_message = f"[{error_info.error_type.value.upper()}] {error_info.message}"
        
        if error_info.file_path:
            log_message += f" | 文件: {error_info.file_path}"
        
        if context:
            log_message += f" | 上下文: {context}"
        
        log_message += f" | 原始错误: {error_info.original_error}"
        
        # 根据严重程度选择日志级别
        if error_info.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message)
        elif error_info.severity == ErrorSeverity.HIGH:
            self.logger.error(log_message)
        elif error_info.severity == ErrorSeverity.MEDIUM:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def handle_error_with_retry(self, func, *args, max_retries: int = 3, **kwargs) -> Tuple[bool, Any, Optional[ErrorInfo]]:
        """带重试机制的错误处理"""
        last_error_info = None
        
        for attempt in range(max_retries + 1):
            try:
                result = func(*args, **kwargs)
                if attempt > 0:
                    print(f"✅ 重试成功（第 {attempt} 次尝试）")
                return True, result, None
                
            except Exception as e:
                error_info = self.analyze_error(e, {'attempt': attempt + 1})
                last_error_info = error_info
                
                if not error_info.auto_recoverable or attempt >= max_retries:
                    break
                
                # 计算重试延迟
                delay = self.retry_delays[min(attempt, len(self.retry_delays) - 1)]
                print(f"⚠️ 操作失败，{delay} 秒后重试（第 {attempt + 1}/{max_retries + 1} 次）")
                print(f"   错误: {error_info.message}")
                
                time.sleep(delay)
        
        return False, None, last_error_info
    
    def display_error_report(self, error_info: ErrorInfo) -> None:
        """显示详细的错误报告"""
        print("\n" + "="*60)
        print("❌ 错误报告")
        print("="*60)
        
        # 错误基本信息
        print(f"🔍 错误类型: {error_info.error_type.value}")
        print(f"⚠️  严重程度: {error_info.severity.value}")
        print(f"📝 错误描述: {error_info.message}")
        
        if error_info.file_path:
            print(f"📁 相关文件: {error_info.file_path}")
        
        # 建议解决方案
        if error_info.suggested_solutions:
            print("\n💡 建议解决方案:")
            for i, solution in enumerate(error_info.suggested_solutions, 1):
                print(f"   {i}. {solution}")
        
        # 技术详情（可选）
        print(f"\n🔧 技术详情: {error_info.original_error}")
        
        print("="*60)
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """获取错误统计信息"""
        if not self.error_history:
            return {"total_errors": 0}
        
        # 按类型统计
        type_counts = {}
        severity_counts = {}
        
        for error in self.error_history:
            error_type = error.error_type.value
            severity = error.severity.value
            
            type_counts[error_type] = type_counts.get(error_type, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # 最近的错误
        recent_errors = sorted(self.error_history, key=lambda x: x.timestamp, reverse=True)[:5]
        
        return {
            "total_errors": len(self.error_history),
            "by_type": type_counts,
            "by_severity": severity_counts,
            "recent_errors": [
                {
                    "type": e.error_type.value,
                    "message": e.message,
                    "timestamp": e.timestamp
                } for e in recent_errors
            ]
        }
    
    def clear_error_history(self) -> None:
        """清空错误历史记录"""
        self.error_history.clear()
        print("✅ 错误历史记录已清空")
    
    def export_error_report(self, file_path: str) -> bool:
        """导出错误报告到文件"""
        try:
            import json
            from datetime import datetime
            
            report_data = {
                "export_time": datetime.now().isoformat(),
                "statistics": self.get_error_statistics(),
                "detailed_errors": [
                    {
                        "timestamp": datetime.fromtimestamp(e.timestamp).isoformat(),
                        "type": e.error_type.value,
                        "severity": e.severity.value,
                        "message": e.message,
                        "original_error": e.original_error,
                        "file_path": e.file_path,
                        "suggested_solutions": e.suggested_solutions,
                        "auto_recoverable": e.auto_recoverable,
                        "retry_count": e.retry_count
                    } for e in self.error_history
                ]
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 错误报告已导出到: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ 导出错误报告失败: {e}")
            return False


# 全局错误处理器实例
_global_error_handler = None

def get_error_handler(log_file: Optional[str] = None) -> ErrorHandler:
    """获取全局错误处理器实例"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler(log_file)
    return _global_error_handler


def handle_error(error: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
    """便捷的错误处理函数"""
    handler = get_error_handler()
    return handler.analyze_error(error, context)


def handle_with_retry(func, *args, max_retries: int = 3, **kwargs) -> Tuple[bool, Any, Optional[ErrorInfo]]:
    """便捷的重试处理函数"""
    handler = get_error_handler()
    return handler.handle_error_with_retry(func, *args, max_retries=max_retries, **kwargs)