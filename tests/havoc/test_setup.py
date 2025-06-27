"""
测试脚本 - 验证项目设置是否正确
运行此脚本来检查是否所有组件都能正常工作

适配直接调用下方的代码。
"""
import sys
import os
from pathlib import Path

# 添加 src 目录到路径
project_root = Path(__file__).parent.parent.parent  # 从 tests/havoc/ 回到项目根目录
sys.path.insert(0, str(project_root / "src"))

def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试 ADK 核心模块
        from google.adk.runners import Runner, InMemoryRunner
        from google.adk.agents import Agent
        from google.adk.models.lite_llm import LiteLlm
        from google.adk.tools.function_tool import FunctionTool
        print("✅ ADK 核心模块导入成功")
        
        # 测试自定义模块
        from apps.core.config import AppConfig
        from apps.core.app_factory import AppFactory
        from apps.core.base_app import BaseApp
        print("✅ 核心模块导入成功")
        
        from apps.tools.custom_tools import get_custom_tools
        print("✅ 工具模块导入成功")
        
        from apps.interfaces.console_interface import ConsoleInterface
        print("✅ 接口模块导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_config():
    """测试配置加载"""
    print("\n🔧 测试配置加载...")
    
    try:
        from apps.core.config import AppConfig
        
        # 测试默认配置
        config = AppConfig()
        print(f"✅ 默认配置创建成功: {config.app_name}")
        
        # 测试环境变量加载
        os.environ['APP_NAME'] = 'test_app'
        os.environ['DEBUG'] = 'true'
        config = AppConfig.from_env('.env.example')
        print(f"✅ 环境配置加载成功: {config.app_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_tools():
    """测试自定义工具"""
    print("\n🛠️ 测试自定义工具...")
    
    try:
        from apps.tools.custom_tools import get_custom_tools, get_current_time, add_numbers, generate_random_string
        
        # 测试工具列表创建
        tools = get_custom_tools()
        print(f"✅ 工具列表创建成功: {len(tools)} 个工具")
        
        # 测试个别工具功能
        current_time = get_current_time()
        print(f"✅ 获取时间: {current_time}")
        
        result = add_numbers(3, 5)
        print(f"✅ 加法计算: 3 + 5 = {result}")
        
        random_str = generate_random_string(8)
        print(f"✅ 随机字符串: {random_str}")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具测试失败: {e}")
        return False

def test_agent_creation():
    """测试代理创建（不实际调用 API）"""
    print("\n🤖 测试代理创建...")
    
    try:
        from apps.core.config import AppConfig
        from apps.agents.my_agent import create_my_agent
        
        # 使用测试配置
        config = AppConfig(api_key="test-key", model_name="gpt-4o-mini")
        
        # 创建代理对象
        agent = create_my_agent(config)
        print(f"✅ 代理创建成功: {agent.name}")
        print(f"✅ 代理工具数量: {len(agent.tools) if hasattr(agent, 'tools') and agent.tools else 0}")
        
        return True
        
    except Exception as e:
        print(f"❌ 代理创建测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("🚀 开始项目设置验证...\n")
    
    tests = [
        test_imports,
        test_config,
        test_tools,
        test_agent_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！项目设置正确。")
        print("\n💡 接下来的步骤:")
        print("1. 复制 .env.example 为 .env")
        print("2. 在 .env 中设置您的 API_KEY")
        print("3. 运行: python main.py")
    else:
        print("❌ 部分测试失败，请检查项目设置。")
        sys.exit(1)

if __name__ == '__main__':
    main() 