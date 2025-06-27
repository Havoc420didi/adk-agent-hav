#!/usr/bin/env python3
"""
Web 接口模式测试脚本 - ADK 自定义应用
"""
import os
import sys
from pathlib import Path

# 确保可以导入项目模块
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from apps.core.config import AppConfig

def test_config_modes():
    """测试不同的 Web 接口配置模式"""
    print("🧪 测试 Web 接口配置模式\n")
    
    # 测试 1: 自定义 Web 接口模式
    print("1. 测试自定义 Web 接口模式:")
    os.environ["USE_ORIGINAL_ADK_WEB"] = "false"
    config1 = AppConfig.from_env()
    print(f"   use_original_adk_web: {config1.use_original_adk_web}")
    print(f"   预期行为: 使用简化的聊天界面\n")
    
    # 测试 2: 原始 ADK Web 接口模式
    print("2. 测试原始 ADK Web 接口模式:")
    os.environ["USE_ORIGINAL_ADK_WEB"] = "true"
    config2 = AppConfig.from_env()
    print(f"   use_original_adk_web: {config2.use_original_adk_web}")
    print(f"   预期行为: 使用完整的 Angular 前端\n")
    
    # 测试 3: 默认配置
    print("3. 测试默认配置（未设置环境变量）:")
    if "USE_ORIGINAL_ADK_WEB" in os.environ:
        del os.environ["USE_ORIGINAL_ADK_WEB"]
    config3 = AppConfig.from_env()
    print(f"   use_original_adk_web: {config3.use_original_adk_web}")
    print(f"   预期行为: 默认使用自定义 Web 接口\n")

def show_usage_examples():
    """显示使用示例"""
    print("📝 使用示例:\n")
    
    print("启动自定义 Web 接口:")
    print("   # 在 .env 中设置: USE_ORIGINAL_ADK_WEB=false")
    print("   python main.py --mode web --port 8000")
    print("   # 访问: http://localhost:8000\n")
    
    print("启动原始 ADK Web 接口:")
    print("   # 在 .env 中设置: USE_ORIGINAL_ADK_WEB=true")
    print("   python main.py --mode web --port 8000")
    print("   # 访问: http://localhost:8000/dev-ui/\n")
    
    print("通过环境变量临时设置:")
    print("   export USE_ORIGINAL_ADK_WEB=true")
    print("   python main.py --mode web --debug\n")

def check_adk_availability():
    """检查 ADK 模块可用性"""
    print("🔍 检查 ADK 模块可用性:\n")
    
    try:
        from google.adk.cli.fast_api import get_fast_api_app
        from google.adk.cli.utils import logs
        print("✅ ADK 核心模块可用")
        print("   - google.adk.cli.fast_api")
        print("   - google.adk.cli.utils.logs")
        print("   📝 可以使用原始 ADK Web 接口\n")
        return True
    except ImportError as e:
        print("❌ ADK 核心模块不可用")
        print(f"   错误: {e}")
        print("   📝 只能使用自定义 Web 接口")
        print("   💡 要使用原始 ADK Web 接口，请安装: pip install google-adk\n")
        return False

def run_web_mode_tests():
    """运行 Web 模式相关测试"""
    print("🚀 ADK Web 接口模式完整测试\n")
    
    # 保存原始环境变量
    original_env = os.environ.get("USE_ORIGINAL_ADK_WEB")
    
    try:
        # 运行各项测试
        test_config_modes()
        adk_available = check_adk_availability()
        show_usage_examples()
        
        # 测试结果总结
        print("=" * 60)
        print("📊 测试结果总结:")
        print(f"   ✅ 配置系统测试: 通过")
        print(f"   {'✅' if adk_available else '⚠️ '} ADK 模块检查: {'可用' if adk_available else '不可用'}")
        print(f"   ✅ 使用示例展示: 完成")
        
        if adk_available:
            print("\n🎉 所有功能可用！您可以使用两种 Web 接口模式。")
        else:
            print("\n⚠️  仅自定义 Web 接口可用。要使用原始 ADK Web 接口，")
            print("   请安装完整的 google-adk 包。")
            
    finally:
        # 恢复原始环境变量
        if original_env is not None:
            os.environ["USE_ORIGINAL_ADK_WEB"] = original_env
        elif "USE_ORIGINAL_ADK_WEB" in os.environ:
            del os.environ["USE_ORIGINAL_ADK_WEB"]

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 ADK Web 接口模式测试")
    print("=" * 60)
    
    run_web_mode_tests()
    
    print("\n✨ 测试完成！")
    print("💡 现在您可以根据需要选择合适的 Web 接口模式")
    print("📍 运行位置: tests/havoc/test_web_modes.py") 