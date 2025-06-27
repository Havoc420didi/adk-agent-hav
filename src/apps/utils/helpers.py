"""
工具函数
"""
import re
from typing import Any, Optional


def format_response(text: str) -> str:
    """格式化响应文本"""
    if not text:
        return ""
    
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text.strip())
    return text


def validate_input(user_input: str) -> bool:
    """验证用户输入"""
    if not user_input or not user_input.strip():
        return False
    
    # 检查是否包含危险字符
    dangerous_patterns = [
        r'<script',
        r'javascript:',
        r'data:text/html',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return False
    
    return True


def truncate_text(text: str, max_length: int = 1000) -> str:
    """截断过长的文本"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def extract_code_blocks(text: str) -> list[str]:
    """从文本中提取代码块"""
    pattern = r'```(?:python|py)?\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches 