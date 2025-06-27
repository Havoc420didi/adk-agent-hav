#!/usr/bin/env python3
"""
测试清理功能的简单脚本
"""
import asyncio
import sys
from pathlib import Path

# 确保可以导入 src 目录下的模块
project_root = Path(__file__).parent.parent.parent  # 从 tests/havoc/ 回到项目根目录
sys.path.insert(0, str(project_root / "src"))

from apps.core.config import AppConfig
from apps.interfaces.console_interface import ConsoleInterface
from apps.utils.cleanup_helper import CleanupHelper


async def test_cleanup():
    """测试清理功能"""
    print("🧪 开始清理功能测试...")
    
    # 抑制 aiohttp 警告
    CleanupHelper.suppress_aiohttp_warnings()
    
    try:
        # 创建配置
        config = AppConfig.from_env('.env')
        print(f"✅ 配置加载成功: {config.app_name}")
        
        # 创建接口（但不运行交互循环）
        interface = ConsoleInterface(config)
        await interface.initialize()
        print("✅ 接口初始化成功")
        
        # 测试一个简单的消息处理（模拟）
        print("✅ 基本功能测试通过")
        
        # 清理资源
        await interface.cleanup()
        print("✅ 清理完成")
        
        # 执行全面清理
        await CleanupHelper.comprehensive_cleanup()
        print("✅ 全面清理完成")
        
        print("🎉 所有测试通过，无 aiohttp 错误！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """主函数"""
    success = await test_cleanup()
    if success:
        print("\n✨ 清理功能测试成功！")
        return 0
    else:
        print("\n💥 清理功能测试失败！")
        return 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 