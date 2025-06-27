#!/usr/bin/env python3
"""
快速开始脚本 - 一键设置和启动 ADK 自定义应用
"""
import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """打印欢迎横幅"""
    print("""
🚀 ADK 自定义应用框架 - 快速开始
=====================================

这个脚本将帮助您快速设置和启动 ADK 自定义应用。
    """)

def check_environment():
    """检查环境"""
    print("🔍 检查环境...")
    
    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ 需要 Python 3.8 或更高版本")
        return False
    
    print(f"✅ Python 版本: {sys.version}")
    return True

def install_dependencies():
    """安装依赖"""
    print("\n📦 安装依赖...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "litellm"], 
                      check=True, capture_output=True)
        print("✅ 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def run_tests():
    """运行测试"""
    print("\n🧪 运行项目验证...")
    
    try:
        # 运行测试（从项目根目录）
        project_root = Path(__file__).parent.parent.parent
        result = subprocess.run([sys.executable, str(project_root / "tests" / "havoc" / "test_setup.py")], 
                              capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ 所有测试通过")
            return True
        else:
            print("❌ 测试失败:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        return False

def create_env_file():
    """创建环境变量文件"""
    print("\n⚙️ 配置环境变量...")
    
    # 在项目根目录创建 .env 文件
    project_root = Path(__file__).parent.parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        print("✅ .env 文件已存在")
        return True
    
    try:
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("""# 应用配置
APP_NAME=my_custom_app
DEBUG=true

# DeepSeek API 配置
MODEL_NAME=deepseek/deepseek-chat
API_KEY=sk-9c8e30190b2543bbacf7dc47d38df19e
API_BASE=https://api.deepseek.com

# 可选配置
# MAX_TOKENS=2000
# TEMPERATURE=0.7
""")
        print("✅ 已创建 .env 文件")
        print("⚠️  请编辑 .env 文件并设置您的 API_KEY")
        return True
    except Exception as e:
        print(f"❌ 创建 .env 文件失败: {e}")
        return False

def show_usage():
    """显示使用说明"""
    print("""
🎯 使用方式:

1. 控制台模式:
   python main.py --mode console

2. Web 模式:
   python main.py --mode web --port 8000

3. API 模式:
   python main.py --mode api --port 8080

4. 调试模式:
   python main.py --debug

📝 重要提示:
- 请在 .env 文件中设置正确的 API_KEY
- 首次使用建议先运行控制台模式进行测试
- 更多信息请查看 README.md
    """)

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    if not check_environment():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        print("⚠️  请手动安装依赖: pip install litellm")
    
    # 运行测试
    if not run_tests():
        print("⚠️  项目验证失败，请检查设置")
    
    # 创建环境文件
    create_env_file()
    
    # 显示使用说明
    show_usage()
    
    print("🎉 快速开始完成！")
    
    # 询问是否立即启动
    try:
        choice = input("\n是否立即启动控制台模式？(y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            print("\n🚀 启动控制台模式...")
            project_root = Path(__file__).parent.parent.parent
            os.chdir(project_root)
            os.system(f"{sys.executable} main.py --mode console")
    except KeyboardInterrupt:
        print("\n👋 再见！")

if __name__ == "__main__":
    main() 