# BSL Drug Pilot Agent

BSL药物试点智能助手，集成多种药物算法工具，为药物研发提供全方位的智能支持。

## 功能特性

### 1. 药物性质预测
- **血脑屏障通透性预测**: 预测药物是否能够通过血脑屏障
- **水溶性预测**: 预测药物在水中的溶解度
- **脂溶性预测**: 预测药物的脂溶性（logP值）
- **自由能预测**: 预测溶剂化自由能
- **BACE1抑制活性**: 预测对β-分泌酶的抑制活性

### 2. 药物-靶点相互作用
- **结合亲和力预测**: 预测药物与靶点蛋白的结合强度
- **分类预测**: 判断药物是否能够与特定靶点结合
- **相互作用模式分析**: 分析药物与靶点的相互作用机制

### 3. 药物-细胞反应
- **细胞反应强度预测**: 预测药物对特定细胞系的影响
- **细胞毒性评估**: 评估药物的细胞毒性
- **反应优化**: 优化药物对细胞的反应效果

### 4. 药物设计与生成
- **药物候选分子生成**: 基于目标特性生成新的药物候选分子
- **逆合成路径设计**: 设计药物分子的合成路径
- **药物-药物相互作用预测**: 预测多药联用的相互作用

## 安装要求

### 系统要求
- Python 3.8+
- CUDA支持的GPU（推荐）
- 足够的内存和存储空间

### 依赖包
```bash
# 核心依赖
pip install torch torchvision torchaudio
pip install torch-geometric
pip install rdkit-pypi
pip install numpy pandas scipy
pip install scikit-learn
pip install transformers

# ADK框架依赖
# (根据项目根目录的requirements.txt安装)
```

## 配置说明

### 环境变量配置
```bash
# 模型配置
export BSL_MODEL_NAME="gpt-3.5-turbo"  # 或其他支持的模型
export BSL_API_KEY="your-api-key"
export BSL_API_BASE="https://api.openai.com/v1"

# CUDA配置
export CUDA_VISIBLE_DEVICES="0"  # 指定使用的GPU
export BSL_CUDA_DEVICE="cuda:0"

# 算法配置
export BSL_BATCH_SIZE="32"
export BSL_REQUEST_TIMEOUT="120.0"
```

### 算法模型文件
确保以下算法模型文件已正确放置：
- `algorithm/drug_property/pretrained_models/`
- `algorithm/drug_cell_response_regression/pretrained_models/`
- `algorithm/drug_target_affinity_regression/pretrained_models/`
- 其他算法的预训练模型目录

## 使用方法

### 1. 作为Python模块使用
```python
from apps.agents.bsl_drug_pilot.agent import root_agent

# 药物性质预测
response = root_agent.chat("请预测阿司匹林（CC(=O)OC1=CC=CC=C1C(=O)O）的血脑屏障通透性")
print(response)

# 药物-靶点相互作用预测
response = root_agent.chat("预测布洛芬与COX-2的结合亲和力")
print(response)
```

### 2. 命令行交互模式
```bash
cd src/apps/agents/bsl_drug_pilot
python main.py --interactive
```

### 3. 演示模式
```bash
cd src/apps/agents/bsl_drug_pilot
python main.py --demo
```

## 使用示例

### 药物性质预测示例
```
用户: 请预测阿司匹林（CC(=O)OC1=CC=CC=C1C(=O)O）的水溶性

Agent: 我将为您预测阿司匹林的水溶性。

[调用药物性质预测工具...]

根据预测结果，阿司匹林的水溶性为...
预测值表明该化合物具有中等水溶性，适合口服给药...
```

### 药物设计示例
```
用户: 我需要设计一个能够穿越血脑屏障的抗阿尔茨海默病药物

Agent: 我将帮您设计一个能够穿越血脑屏障的抗阿尔茨海默病药物。

首先，让我为您生成一些候选分子...
[调用药物生成工具...]

然后预测这些分子的血脑屏障通透性...
[调用药物性质预测工具...]

最后优化分子结构以提高效果...
[调用优化工具...]
```

## 支持的输入格式

### SMILES格式分子
- 标准SMILES格式，如：`CC(=O)OC1=CC=CC=C1C(=O)O` (阿司匹林)
- 支持带立体化学信息的SMILES
- 支持分子列表输入

### 蛋白质序列
- 标准氨基酸单字母代码序列
- 支持FASTA格式

### 细胞系信息
- 标准细胞系名称，如：HeLa, A549, MCF-7等
- 支持自定义细胞系参数

## 工具列表

| 工具名称 | 功能描述 | 输入格式 |
|---------|---------|----------|
| predict_drug_properties | 预测药物理化性质 | SMILES, 性质类型 |
| predict_drug_cell_response | 预测药物-细胞反应 | SMILES, 细胞系 |
| predict_drug_target_affinity_regression | 预测药物-靶点亲和力（回归） | SMILES, 靶点序列 |
| predict_drug_target_affinity_classification | 预测药物-靶点亲和力（分类） | SMILES, 靶点序列 |
| predict_drug_drug_interaction | 预测药物-药物相互作用 | 两个SMILES |
| generate_drug_candidates | 生成药物候选分子 | 细胞系, 目标反应 |
| design_synthesis_pathway | 设计合成路径 | 目标分子SMILES |
| optimize_drug_cell_response | 优化药物-细胞反应 | SMILES, 优化目标 |

## 注意事项

1. **GPU要求**: 部分算法需要GPU支持，建议使用CUDA兼容的显卡
2. **内存要求**: 大分子预测可能需要较大内存
3. **模型文件**: 确保所有预训练模型文件已正确下载和配置
4. **网络连接**: LLM调用需要稳定的网络连接
5. **输入验证**: 确保输入的SMILES格式正确有效

## 故障排除

### 常见问题

**Q: 算法模块导入失败**
A: 检查Python路径设置和算法依赖包是否正确安装

**Q: CUDA内存不足**
A: 减小批处理大小或使用CPU模式

**Q: 预测结果异常**
A: 检查输入SMILES格式是否正确，确保分子结构有效

### 日志调试
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 贡献指南

欢迎提交问题和改进建议！请确保：
1. 遵循代码规范
2. 添加适当的测试
3. 更新相关文档

## 许可证

请参考项目根目录的LICENSE文件。 