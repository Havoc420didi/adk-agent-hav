"""
药物算法工具封装
将原有的算法函数封装为ADK工具
"""
import sys
import os
from pathlib import Path
from typing import List, Optional

# 添加bsl_drug_pilot目录到Python路径，这样algorithm包就可以被正确导入
bsl_root = Path(__file__).parent.parent
sys.path.insert(0, str(bsl_root))

# 同时也添加algorithm目录到路径（备用）
algorithm_root = bsl_root / "algorithm"
sys.path.insert(0, str(algorithm_root))

# 设置工作目录以匹配原始算法的预期路径
original_cwd = os.getcwd()
os.chdir(str(bsl_root))

from google.adk.tools.function_tool import FunctionTool
from ..algorithm.drug_property.main import drug_property_prediction
from ..algorithm.drug_cell_response_regression.main import drug_cell_response_regression_predict
from ..algorithm.drug_target_affinity_regression.main import drug_target_affinity_regression_predict
from ..algorithm.drug_target_affinity_classification.main import drug_target_classification_prediction
from ..algorithm.drug_drug_response.main import drug_drug_response_predict
from ..algorithm.drug_generation.main import drug_cell_response_regression_generation
from ..algorithm.drug_synthesis_design.scripts.main import Retrosynthetic_reaction_pathway_prediction
from ..algorithm.drug_cell_response_regression_optimization.main import drug_cell_response_regression_optimization
        
def _process_smiles_input(drug_smiles: str):
    """统一处理SMILES输入格式，将逗号分隔的字符串转换为列表"""
    if ',' in drug_smiles:
        return [s.strip() for s in drug_smiles.split(',')]
    else:
        return drug_smiles


def predict_drug_properties(drug_smiles: str, property_type: str) -> str:
    """
    预测药物的理化性质和ADMET性质
    
    Args:
        drug_smiles: 药物的SMILES字符串，支持单个分子字符串或用逗号分隔的多个SMILES字符串
        property_type: 要预测的性质类型，支持以下选项：
            - 'Class': 预测对BACE1的抑制活性
            - 'p_np': 预测血脑屏障通透性
            - 'logSolubility': 预测水溶性
            - 'freesolv': 预测自由能
            - 'lipo': 预测脂溶性
    
    Returns:
        预测结果的描述
    """
    try:
        # 统一处理SMILES输入格式
        smiles_list = _process_smiles_input(drug_smiles)
        result = drug_property_prediction(smiles_list, property_type)
        return f"药物性质预测完成。结果：{result}"
    except Exception as e:
        return f"药物性质预测失败：{str(e)}"


def predict_drug_cell_response(drug_smiles: str, cell_line: Optional[str] = None) -> str:
    """
    预测药物对细胞的反应强度
    
    Args:
        drug_smiles: 药物的SMILES字符串，支持单个分子字符串或用逗号分隔的多个SMILES字符串
        cell_line: 细胞系名称（可选）
    
    Returns:
        预测结果的描述
    """
    try:
        # 统一处理SMILES输入格式
        smiles_list = _process_smiles_input(drug_smiles)
        result = drug_cell_response_regression_predict(smiles_list, cell_line)
        return f"药物-细胞反应预测完成。结果：{result}"
    except Exception as e:
        return f"药物-细胞反应预测失败：{str(e)}"


def predict_drug_target_affinity_regression(drug_smiles: str, target_sequence: Optional[str] = None) -> str:
    """
    预测药物与靶点的结合亲和力（回归预测）
    
    Args:
        drug_smiles: 药物的SMILES字符串，支持单个分子字符串或用逗号分隔的多个SMILES字符串
        target_sequence: 靶点蛋白序列（可选）
    
    Returns:
        预测结果的描述
    """
    try:
        # 统一处理SMILES输入格式
        smiles_list = _process_smiles_input(drug_smiles)
        result = drug_target_affinity_regression_predict(smiles_list, target_sequence)
        return f"药物-靶点亲和力（回归）预测完成。结果：{result}"
    except Exception as e:
        return f"药物-靶点亲和力预测失败：{str(e)}"


def predict_drug_target_affinity_classification(drug_smiles: str, target_sequence: Optional[str] = None) -> str:
    """
    预测药物与靶点的结合亲和力（分类预测）
    
    Args:
        drug_smiles: 药物的SMILES字符串，支持单个分子字符串或用逗号分隔的多个SMILES字符串
        target_sequence: 靶点蛋白序列（可选）
    
    Returns:
        预测结果的描述
    """
    try:
        # 统一处理SMILES输入格式
        smiles_list = _process_smiles_input(drug_smiles)
        result = drug_target_classification_prediction(smiles_list, target_sequence)
        return f"药物-靶点亲和力（分类）预测完成。结果：{result}"
    except Exception as e:
        return f"药物-靶点亲和力分类预测失败：{str(e)}"


def predict_drug_drug_interaction(drug1_smiles: str, drug2_smiles: str) -> str:
    """
    预测药物-药物相互作用
    
    Args:
        drug1_smiles: 第一个药物的SMILES字符串
        drug2_smiles: 第二个药物的SMILES字符串
    
    Returns:
        预测结果的描述
    """
    try:
        # 将两个SMILES字符串组合成数组格式
        smiles_pairs = [[drug1_smiles, drug2_smiles]]
        result = drug_drug_response_predict(smiles_pairs)
        return f"药物-药物相互作用预测完成。结果：{result}"
    except Exception as e:
        return f"药物-药物相互作用预测失败：{str(e)}"

def generate_drug_candidates(cell_line: Optional[str] = None, target_response: Optional[float] = None) -> str:
    """
    基于细胞反应数据生成新的药物候选分子
    
    Args:
        cell_line: 目标细胞系
        target_response: 目标反应强度
    
    Returns:
        生成的药物候选分子的描述
    """
    try:
        result = drug_cell_response_regression_generation(cell_line, target_response)
        return f"药物候选分子生成完成。结果：{result}"
    except Exception as e:
        return f"药物候选分子生成失败：{str(e)}"


def design_synthesis_pathway(target_smiles: str) -> str:
    """
    设计药物分子的逆合成反应路径
    
    Args:
        target_smiles: 目标分子的SMILES字符串
    
    Returns:
        合成路径的描述
    """
    try:
        result = Retrosynthetic_reaction_pathway_prediction(target_smiles)
        return f"逆合成路径设计完成。结果：{result}"
    except Exception as e:
        return f"逆合成路径设计失败：{str(e)}"


def optimize_drug_cell_response(drug_smiles: str, cell_line: Optional[str] = None, optimization_target: Optional[str] = None, mask: Optional[str] = None) -> str:
    """
    优化药物-细胞反应
    
    Args:
        drug_smiles: 药物的SMILES字符串，支持单个分子字符串或用逗号分隔的多个SMILES字符串
        cell_line: 细胞系名称（可选）
        optimization_target: 优化目标（可选）
        mask: 用于指定分子或数据中需要重点关注的掩码（可选）
    
    Returns:
        优化结果的描述
    """
    try:
        # 统一处理SMILES输入格式
        smiles_list = _process_smiles_input(drug_smiles)
        
        # 处理mask参数
        if mask is None:
            mask = []  # 默认空掩码
        
        # 调用优化函数，传入mask参数
        result = drug_cell_response_regression_optimization(optimization_target, cell_line, smiles_list[0], mask)
        return f"药物-细胞反应优化完成。结果：{result}"
    except Exception as e:
        return f"药物-细胞反应优化失败：{str(e)}"

def get_drug_algorithm_tools():
    """获取药物算法工具列表（简化版，只包含药物性质预测工具）"""
    return [
        FunctionTool(predict_drug_properties),
        FunctionTool(predict_drug_cell_response),
        FunctionTool(predict_drug_target_affinity_regression),
        FunctionTool(predict_drug_target_affinity_classification),
        FunctionTool(predict_drug_drug_interaction),
        FunctionTool(generate_drug_candidates),
        FunctionTool(design_synthesis_pathway),
        FunctionTool(optimize_drug_cell_response),
    ] 