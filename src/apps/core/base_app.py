"""
基础应用类
"""
import asyncio
from abc import ABC, abstractmethod
from .config import AppConfig
from .app_factory import AppFactory
from ..utils.cleanup_helper import CleanupHelper


class BaseApp(ABC):
    """基础应用类"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.app_factory = AppFactory(config)
        self.runner = None
    
    async def initialize(self):
        """初始化应用"""
        if not self.config.validate():
            raise ValueError("配置验证失败")
        
        self.runner = self.app_factory.create_runner(self.config.app_name)
        print(f"🚀 {self.config.app_name} 初始化完成")
    
    @abstractmethod
    async def run(self):
        """运行应用 - 子类需要实现"""
        pass
    
    async def cleanup(self):
        """清理资源"""
        cleanup_success = False
        
        # 1. 清理 Runner 资源
        if self.runner:
            try:
                await asyncio.wait_for(self.runner.close(), timeout=3.0)
                print("✅ Runner 资源清理完成")
                cleanup_success = True
            except asyncio.TimeoutError:
                print("⚠️ Runner 清理超时")
            except Exception as e:
                print(f"⚠️ Runner 清理过程中出现警告: {e}")
        
        # 2. 使用清理助手进行全面清理
        try:
            if cleanup_success:
                # 如果 Runner 清理成功，使用安全的全面清理
                await asyncio.wait_for(CleanupHelper.safe_comprehensive_cleanup(), timeout=5.0)
                print("✅ 全面资源清理完成")
            else:
                # 如果 Runner 清理失败，直接使用紧急清理
                await CleanupHelper.emergency_cleanup()
        except asyncio.TimeoutError:
            print("⚠️ 全面清理超时，执行紧急清理")
            await CleanupHelper.emergency_cleanup()
        except Exception as e:
            print(f"⚠️ 全面清理过程中出现警告: {e}")
            await CleanupHelper.emergency_cleanup() 