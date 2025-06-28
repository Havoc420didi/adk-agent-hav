"""
BSL Drug Pilot Agent
用于药物研发的智能助手，集成多种药物算法工具
"""
import sys
import os
from pathlib import Path

# 添加项目根目录和算法目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent.parent
algorithm_root = Path(__file__).parent / "algorithm"
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(algorithm_root))

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from apps.agents.bsl_drug_pilot.config import BSLDrugPilotConfig
from apps.agents.bsl_drug_pilot.tools.drug_tools import get_drug_algorithm_tools


class BSLDrugPilotAgent(Agent):
    """BSL 药物试点 Agent"""
    
    def __init__(self):
        # 加载配置
        config = BSLDrugPilotConfig.from_env()
        
        # 设置CUDA环境
        config.setup_cuda_environment()
        
        # 配置 LLM 模型
        llm_model = LiteLlm(
            model=config.model_name,
            api_key=config.api_key,
            api_base=config.api_base
        )
        
        # 初始化父类
        super().__init__(
            name="bsl_drug_pilot",
            instruction="""
你是一个专业的药物研发智能助手，专门帮助用户进行药物性质预测和分析。
你拥有以下核心能力：

**药物性质预测：**
- 预测药物的理化性质（溶解度、脂溶性等）
- 预测药物的ADMET性质（吸收、分布、代谢、排泄、毒性）
- 预测血脑屏障通透性
- 预测对BACE1的抑制活性

**支持的性质类型：**
- 'Class': 预测对BACE1的抑制活性
- 'p_np': 预测血脑屏障通透性
- 'logSolubility': 预测水溶性
- 'freesolv': 预测自由能
- 'lipo': 预测脂溶性

**使用指南：**
1. 提供SMILES格式的分子结构（支持单个分子或用逗号分隔的多个分子）
2. 指定要预测的性质类型（从上述支持的类型中选择）
3. 我会为您进行准确的药物性质预测

请用中文回答，并提供详细的分析结果和建议。
我专注于药物性质预测，能为您的药物研发工作提供可靠的分子性质分析。
            """.strip(),
            model=llm_model,
            tools=get_drug_algorithm_tools()
        )

# 导出 root_agent
root_agent = BSLDrugPilotAgent() 