"""
自定义工具实现
"""
import datetime
import random
import string
from google.adk.tools.function_tool import FunctionTool


def get_current_time() -> str:
    """获取当前时间"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_numbers(a: float, b: float) -> float:
    """计算两个数字的和
    
    Args:
        a: 第一个数字
        b: 第二个数字
        
    Returns:
        两个数字的和
    """
    return a + b


def multiply_numbers(a: float, b: float) -> float:
    """计算两个数字的乘积
    
    Args:
        a: 第一个数字
        b: 第二个数字
        
    Returns:
        两个数字的乘积
    """
    return a * b


def generate_random_string(length: int = 10) -> str:
    """生成指定长度的随机字符串
    
    Args:
        length: 字符串长度，默认为10
        
    Returns:
        随机字符串
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# 创建工具实例
def get_custom_tools():
    """获取自定义工具列表"""
    return [
        FunctionTool(get_current_time),
        FunctionTool(add_numbers),
        FunctionTool(multiply_numbers),
        FunctionTool(generate_random_string),
    ] 