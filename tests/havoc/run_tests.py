#!/usr/bin/env python3
"""
Havoc 测试套件入口脚本

提供统一的测试入口，支持运行单个或多个测试。
"""
import sys
import asyncio
import argparse
from pathlib import Path

# 确保可以导入项目模块
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

# 导入测试模块
from test_setup import main as run_setup_test
from test_cleanup import main as run_cleanup_test
from quick_start import main as run_quick_start


def print_banner():
    """打印测试横幅"""
    print("""
🧪 Havoc 测试套件
==================

可用的测试:
- setup: 项目验证测试
- cleanup: 清理功能测试  
- quickstart: 快速开始脚本
- all: 运行所有测试
    """)


async def run_all_tests():
    """运行所有测试"""
    print("🚀 运行所有测试...\n")
    
    tests = [
        ("项目验证测试", lambda: run_setup_test()),
        ("清理功能测试", lambda: asyncio.run(run_cleanup_test())),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"📋 运行 {test_name}...")
        try:
            result = test_func()
            if result == 0 or result is None:
                print(f"✅ {test_name} 通过\n")
                passed += 1
            else:
                print(f"❌ {test_name} 失败\n")
        except Exception as e:
            print(f"❌ {test_name} 异常: {e}\n")
    
    print(f"📊 总体结果: {passed}/{total} 测试通过")
    return passed == total


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Havoc 测试套件")
    parser.add_argument(
        'test', 
        nargs='?', 
        choices=['setup', 'cleanup', 'quickstart', 'all'],
        default='all',
        help='要运行的测试 (默认: all)'
    )
    parser.add_argument(
        '--list', 
        action='store_true',
        help='列出所有可用测试'
    )
    
    args = parser.parse_args()
    
    if args.list:
        print_banner()
        return 0
    
    print_banner()
    
    try:
        if args.test == 'setup':
            print("🔧 运行项目验证测试...")
            return run_setup_test()
            
        elif args.test == 'cleanup':
            print("🧹 运行清理功能测试...")
            return asyncio.run(run_cleanup_test())
            
        elif args.test == 'quickstart':
            print("🚀 运行快速开始脚本...")
            run_quick_start()
            return 0
            
        elif args.test == 'all':
            success = asyncio.run(run_all_tests())
            return 0 if success else 1
            
    except KeyboardInterrupt:
        print("\n👋 测试被中断")
        return 1
    except Exception as e:
        print(f"❌ 测试运行异常: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main()) 