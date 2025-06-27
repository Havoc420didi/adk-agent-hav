#!/usr/bin/env python3
"""
BSL Drug Pilot Agent 主程序
使用示例和测试入口
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from apps.agents.bsl_drug_pilot.agent import root_agent


def main():
    """主函数"""
    print("=== BSL 药物试点 Agent 启动 ===")
    print(f"Agent 名称: {root_agent.name}")
    print("可用工具:")
    for i, tool in enumerate(root_agent.tools, 1):
        print(f"  {i}. {tool.name}")
    
    # 示例对话
    print("\n=== 示例对话 ===")
    
    # 示例1：药物性质预测
    print("\n1. 药物性质预测示例：")
    try:
        response = root_agent.chat("请预测阿司匹林（CC(=O)OC1=CC=CC=C1C(=O)O）的血脑屏障通透性")
        print(f"回答: {response}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 示例2：药物-靶点相互作用预测
    print("\n2. 药物-靶点相互作用预测示例：")
    try:
        response = root_agent.chat("请预测布洛芬（CC(C)CC1=CC=C(C=C1)C(C(=O)O)C）与目标蛋白的结合亲和力")
        print(f"回答: {response}")
    except Exception as e:
        print(f"错误: {e}")


def interactive_mode():
    """交互模式"""
    print("=== BSL 药物试点 Agent 交互模式 ===")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'help' 查看帮助信息")
    
    while True:
        try:
            user_input = input("\n用户: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif not user_input:
                continue
            
            print("Agent 正在思考...")
            response = root_agent.chat(user_input)
            print(f"Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n\n操作被用户取消。再见！")
            break
        except Exception as e:
            print(f"错误: {e}")


def print_help():
    """打印帮助信息"""
    help_text = """
=== BSL 药物试点 Agent 帮助信息 ===

支持的功能：
1. 药物性质预测
   - 示例: "预测阿司匹林的水溶性"
   - 支持的性质: 血脑屏障通透性、水溶性、脂溶性、自由能等

2. 药物-细胞反应预测
   - 示例: "预测布洛芬对HeLa细胞的反应"

3. 药物-靶点相互作用预测
   - 示例: "预测青霉素与β-内酰胺酶的结合亲和力"

4. 药物-药物相互作用预测
   - 示例: "预测阿司匹林和华法林的相互作用"

5. 药物候选分子生成
   - 示例: "为治疗阿尔茨海默病生成候选分子"

6. 逆合成路径设计
   - 示例: "设计阿司匹林的合成路径"

7. 药物优化
   - 示例: "优化布洛芬对特定细胞系的反应"

输入格式：
- 使用SMILES格式提供分子结构，如: CC(=O)OC1=CC=CC=C1C(=O)O (阿司匹林)
- 可以使用中文或英文描述需求
- 支持复杂的多步骤药物设计任务

命令：
- help: 显示此帮助信息
- quit/exit/q: 退出程序
    """
    print(help_text)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="BSL Drug Pilot Agent")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="启动交互模式")
    parser.add_argument("--demo", "-d", action="store_true", 
                       help="运行演示")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.demo:
        main()
    else:
        print("使用 --help 查看使用说明")
        print("使用 --interactive 启动交互模式")
        print("使用 --demo 运行演示") 