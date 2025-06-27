"""
my_custom_app Agent
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from apps.core.config import AppConfig
from apps.tools.custom_tools import get_custom_tools


class MyCustomAppAgent(Agent):
    """自定义应用 Agent"""
    
    def __init__(self):
        # 加载配置
        config = AppConfig.from_env()
        
        # 配置 LLM 模型
        llm_model = LiteLlm(
            model=config.model_name,
            api_key=config.api_key,
            api_base=config.api_base
        )
        
        # 初始化父类
        super().__init__(
            name="my_custom_app",
            instruction="""
你是一个智能助手，可以帮助用户完成各种任务。
请用中文回答用户的问题，保持友好和专业的态度。

你拥有以下能力：
- 获取当前时间
- 进行数学计算
- 回答各种问题

请根据用户的需求提供帮助。
            """.strip(),
            model=llm_model,
            tools=get_custom_tools()
        )


# 导出 root_agent
root_agent = MyCustomAppAgent() 