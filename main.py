"""
主应用入口点 - 绕过 CLI 直接使用 ADK 核心模块
"""
import asyncio
import argparse
import sys
import signal
from pathlib import Path

# 确保可以导入 src 目录下的模块
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from apps.core.config import AppConfig
from apps.interfaces.console_interface import ConsoleInterface
from apps.utils.cleanup_helper import CleanupHelper


class GracefulKiller:
    """优雅退出处理器"""
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def _exit_gracefully(self, signum, frame):
        print(f"\n🛑 接收到退出信号 ({signum})，正在安全退出...")
        self.kill_now = True


async def safe_cleanup(interface):
    """安全的资源清理函数"""
    cleanup_tasks = []
    
    try:
        print("🧹 开始清理资源...")
        
        # 1. 清理接口资源
        if interface and hasattr(interface, 'cleanup'):
            try:
                await asyncio.wait_for(interface.cleanup(), timeout=5.0)
                print("✅ 接口资源清理完成")
            except asyncio.TimeoutError:
                print("⚠️ 接口清理超时，继续其他清理步骤")
            except Exception as e:
                print(f"⚠️ 接口清理过程中出现警告: {e}")
        
        # 2. 执行全面的资源清理
        try:
            await asyncio.wait_for(CleanupHelper.safe_comprehensive_cleanup(), timeout=10.0)
            print("✅ 全面资源清理完成")
        except asyncio.TimeoutError:
            print("⚠️ 全面清理超时，执行紧急清理")
            await CleanupHelper.emergency_cleanup()
        except Exception as e:
            print(f"⚠️ 全面清理过程中出现警告: {e}")
            await CleanupHelper.emergency_cleanup()
            
    except Exception as e:
        print(f"⚠️ 清理过程中出现异常: {e}")
        await CleanupHelper.emergency_cleanup()
    
    print("🧹 资源清理完成")


async def main():
    parser = argparse.ArgumentParser(description='自定义 ADK 应用')
    parser.add_argument(
        '--mode', 
        choices=['console', 'web', 'api'], 
        default='console', 
        help='运行模式'
    )
    parser.add_argument(
        '--config', 
        help='配置文件路径', 
        default='.env'
    )
    parser.add_argument(
        '--debug', 
        action='store_true', 
        help='启用调试模式'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='服务器主机地址'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='服务器端口'
    )
    
    args = parser.parse_args()
    
    # 设置优雅退出处理器
    killer = GracefulKiller()
    
    # 在程序开始时配置 LiteLLM 和抑制 aiohttp 警告
    CleanupHelper.configure_litellm_transport()
    CleanupHelper.suppress_aiohttp_warnings()
    
    interface = None
    try:
        # 加载配置
        config = AppConfig.from_env(args.config)
        
        # 命令行参数覆盖配置文件
        if args.debug:
            config.debug = True
        if args.host != '127.0.0.1':
            config.host = args.host
        if args.port != 8000:
            config.port = args.port
        
        print(f"🔧 配置加载完成:")
        print(f"   应用名称: {config.app_name}")
        print(f"   调试模式: {config.debug}")
        print(f"   模型: {config.model_name}")
        print(f"   内存模式: {config.use_in_memory}")
        
        # 根据模式启动不同接口
        if args.mode == 'console':
            interface = ConsoleInterface(config)
            
            # 运行接口，并监控退出信号
            task = asyncio.create_task(interface.run())
            while not killer.kill_now and not task.done():
                await asyncio.sleep(0.1)
            
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
        elif args.mode == 'web':
            # 使用 ADK 的 Web 服务器
            from google.adk.cli.fast_api import get_fast_api_app
            import uvicorn
            
            print(f"🌐 启动 ADK Web 服务器 http://{config.host}:{config.port}")
            
            # 使用 src/apps/agents 作为 agents 目录
            agents_dir = str(project_root / "src" / "apps" / "agents")
            
            app = get_fast_api_app(
                agents_dir=agents_dir,
                web=True,
                host=config.host,
                port=config.port
            )
            
            server_config = uvicorn.Config(
                app,
                host=config.host,
                port=config.port,
                reload=False
            )
            server = uvicorn.Server(server_config)
            
            # 创建服务器任务
            task = asyncio.create_task(server.serve())
            
            try:
                while not killer.kill_now and not task.done():
                    await asyncio.sleep(0.1)
            finally:
                if not task.done():
                    print("\n🛑 正在停止 Web 服务...")
                    server.should_exit = True
                    await server.shutdown()
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
            
        elif args.mode == 'api':
            # 使用 ADK 的 API 服务器
            from google.adk.cli.fast_api import get_fast_api_app
            import uvicorn
            
            print(f"🔌 启动 ADK API 服务器 http://{config.host}:{config.port}")
            
            # 使用 src/apps/agents 作为 agents 目录
            agents_dir = str(project_root / "src" / "apps" / "agents")
            
            app = get_fast_api_app(
                agents_dir=agents_dir,
                web=False,  # API 模式，不包含 Web UI
                host=config.host,
                port=config.port
            )
            
            server_config = uvicorn.Config(
                app,
                host=config.host,
                port=config.port,
                reload=False
            )
            server = uvicorn.Server(server_config)
            
            # 创建服务器任务
            task = asyncio.create_task(server.serve())
            
            try:
                while not killer.kill_now and not task.done():
                    await asyncio.sleep(0.1)
            finally:
                if not task.done():
                    print("\n🛑 正在停止 API 服务...")
                    server.should_exit = True
                    await server.shutdown()
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
    finally:
        # 确保接口被正确清理
        await safe_cleanup(interface)
        print("👋 应用已安全退出")
    
    return 0


if __name__ == '__main__':
    # 设置事件循环策略，避免在某些系统上的问题
    try:
        import platform
        if platform.system() == 'Windows':
            # Windows 上使用 ProactorEventLoop 可能更稳定
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass  # 忽略设置失败，使用默认策略
    
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        # 这种情况下说明信号处理器没有正常工作
        print("\n👋 应用已强制退出")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 程序异常退出: {e}")
        sys.exit(1) 