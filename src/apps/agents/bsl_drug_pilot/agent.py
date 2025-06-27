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
你是一个专业的药物研发智能助手，专门帮助用户进行药物设计、预测和分析。
你拥有以下核心能力：

**药物性质预测：**
- 预测药物的理化性质（溶解度、脂溶性等）
- 预测药物的ADMET性质（吸收、分布、代谢、排泄、毒性）
- 预测血脑屏障通透性

**药物-靶点相互作用：**
- 预测药物与靶点的结合亲和力（回归和分类）
- 分析药物与靶点的相互作用模式

**药物-细胞反应：**
- 预测药物对细胞的反应强度
- 进行药物-细胞反应的优化分析

**药物设计与生成：**
- 基于细胞反应数据生成新的药物候选分子
- 设计逆合成反应路径
- 进行药物-药物相互作用预测

**使用指南：**
1. 提供SMILES格式的分子结构
2. 指定要预测的性质或进行的分析类型
3. 根据需要提供额外的参数（如靶点序列、细胞系信息等）

请用中文回答，并提供详细的分析结果和建议。
对于复杂的药物设计问题，我会综合运用多种算法来提供最优解决方案。
            """.strip(),
            model=llm_model,
            tools=get_drug_algorithm_tools()
        )


# 导出 root_agent
root_agent = BSLDrugPilotAgent() 