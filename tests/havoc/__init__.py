"""
Havoc 测试模块

这个模块包含了项目的自定义测试脚本和工具。

主要测试脚本：
- test_setup.py: 项目验证脚本
- test_cleanup.py: 清理功能测试脚本  
- quick_start.py: 快速开始脚本
"""

__version__ = "1.0.0"
__author__ = "Havoc"

# 导出主要测试函数，方便其他模块使用
from .test_setup import main as run_setup_test
from .test_cleanup import test_cleanup
from .quick_start import main as run_quick_start

__all__ = [
    'run_setup_test',
    'test_cleanup', 
    'run_quick_start'
] 