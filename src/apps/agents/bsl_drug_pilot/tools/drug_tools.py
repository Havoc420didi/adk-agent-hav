"""
药物算法工具封装
将原有的算法函数封装为ADK工具
"""
import sys
import os
from pathlib import Path
from typing import List, Optional

# 添加算法目录到Python路径
algorithm_root = Path(__file__).parent.parent / "algorithm"
sys.path.insert(0, str(algorithm_root))

# 设置工作目录以匹配原始算法的预期路径
original_cwd = os.getcwd()
bsl_root = algorithm_root.parent

from google.adk.tools.function_tool import FunctionTool

# 导入算法函数
def _import_algorithm_functions():
    """动态导入算法函数，处理路径问题"""
    try:
        # 确保算法路径在sys.path中
        if str(algorithm_root) not in sys.path:
            sys.path.insert(0, str(algorithm_root))
            
        from apps.agents.bsl_drug_pilot.algorithm.drug_property.main import drug_property_prediction
        from apps.agents.bsl_drug_pilot.algorithm.drug_cell_response_regression.main import drug_cell_response_regression_predict
        from apps.agents.bsl_drug_pilot.algorithm.drug_target_affinity_regression.main import drug_target_affinity_regression_predict
        from apps.agents.bsl_drug_pilot.algorithm.drug_target_affinity_classification.main import drug_target_classification_prediction
        from apps.agents.bsl_drug_pilot.algorithm.drug_drug_response.main import drug_drug_response_predict
        from apps.agents.bsl_drug_pilot.algorithm.drug_generation.main import drug_cell_response_regression_generation
        from apps.agents.bsl_drug_pilot.algorithm.drug_synthesis_design.scripts.main import Retrosynthetic_reaction_pathway_prediction
        from apps.agents.bsl_drug_pilot.algorithm.drug_cell_response_regression_optimization.main import drug_cell_response_regression_optimization
        
        return {
            'drug_property_prediction': drug_property_prediction,
            'drug_cell_response_regression_predict': drug_cell_response_regression_predict,
            'drug_target_affinity_regression_predict': drug_target_affinity_regression_predict,
            'drug_target_classification_prediction': drug_target_classification_prediction,
            'drug_drug_response_predict': drug_drug_response_predict,
            'drug_cell_response_regression_generation': drug_cell_response_regression_generation,
            'Retrosynthetic_reaction_pathway_prediction': Retrosynthetic_reaction_pathway_prediction,
            'drug_cell_response_regression_optimization': drug_cell_response_regression_optimization,
        }
    except ImportError as e:
        print(f"警告：无法导入算法模块: {e}")
        print(f"算法路径: {algorithm_root}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"Python路径: {sys.path[:3]}...")
        
        # 定义占位符函数
        def placeholder_func(*args, **kwargs):
            return f"算法模块未正确安装或配置。错误: {e}"
        
        return {
            'drug_property_prediction': placeholder_func,
            'drug_cell_response_regression_predict': placeholder_func,
            'drug_target_affinity_regression_predict': placeholder_func,
            'drug_target_classification_prediction': placeholder_func,
            'drug_drug_response_predict': placeholder_func,
            'drug_cell_response_regression_generation': placeholder_func,
            'Retrosynthetic_reaction_pathway_prediction': placeholder_func,
            'drug_cell_response_regression_optimization': placeholder_func,
        }

# 动态导入算法函数
_algorithm_functions = _import_algorithm_functions()

# 将函数分配到全局命名空间
drug_property_prediction = _algorithm_functions['drug_property_prediction']
drug_cell_response_regression_predict = _algorithm_functions['drug_cell_response_regression_predict']
drug_target_affinity_regression_predict = _algorithm_functions['drug_target_affinity_regression_predict']
drug_target_classification_prediction = _algorithm_functions['drug_target_classification_prediction']
drug_drug_response_predict = _algorithm_functions['drug_drug_response_predict']
drug_cell_response_regression_generation = _algorithm_functions['drug_cell_response_regression_generation']
Retrosynthetic_reaction_pathway_prediction = _algorithm_functions['Retrosynthetic_reaction_pathway_prediction']
drug_cell_response_regression_optimization = _algorithm_functions['drug_cell_response_regression_optimization']


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
        result = drug_drug_response_predict(drug1_smiles, drug2_smiles)
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


def optimize_drug_cell_response(drug_smiles: str, cell_line: Optional[str] = None, optimization_target: Optional[str] = None) -> str:
    """
    优化药物-细胞反应
    
    Args:
        drug_smiles: 药物的SMILES字符串，支持单个分子字符串或用逗号分隔的多个SMILES字符串
        cell_line: 细胞系名称（可选）
        optimization_target: 优化目标（可选）
    
    Returns:
        优化结果的描述
    """
    try:
        # 统一处理SMILES输入格式
        smiles_list = _process_smiles_input(drug_smiles)
        result = drug_cell_response_regression_optimization(smiles_list, cell_line, optimization_target)
        return f"药物-细胞反应优化完成。结果：{result}"
    except Exception as e:
        return f"药物-细胞反应优化失败：{str(e)}"


def get_drug_algorithm_tools():
    """获取所有药物算法工具列表"""
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