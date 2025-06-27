"""
清理助手模块 - 处理异步资源清理
"""
import asyncio
import gc
import warnings
import os
import logging
from typing import Optional


class CleanupHelper:
    """异步资源清理助手"""
    
    @staticmethod
    def configure_litellm_transport():
        """配置 LiteLLM 传输设置以避免 aiohttp 会话问题"""
        try:
            # 禁用 LiteLLM 的 aiohttp 传输（如果可能）
            # 这可以避免 aiohttp 客户端会话未关闭的问题
            os.environ["DISABLE_AIOHTTP_TRANSPORT"] = "True"
            
            # 或者使用旧版本的传输方式
            import litellm
            if hasattr(litellm, 'disable_aiohttp_transport'):
                litellm.disable_aiohttp_transport = True
                
        except Exception as e:
            print(f"⚠️ 配置 LiteLLM 传输时出现警告: {e}")
    
    @staticmethod
    async def safe_sleep(duration: float, step: float = 0.01):
        """安全的异步等待，不会被取消中断"""
        try:
            elapsed = 0.0
            while elapsed < duration:
                try:
                    sleep_time = min(step, duration - elapsed)
                    await asyncio.sleep(sleep_time)
                    elapsed += sleep_time
                except asyncio.CancelledError:
                    # 被取消时不抛出异常，而是直接返回
                    break
        except Exception:
            # 忽略所有其他异常
            pass
    
    @staticmethod
    async def cleanup_aiohttp_sessions():
        """清理所有未关闭的 aiohttp 客户端会话"""
        try:
            import aiohttp
            import weakref
            
            # 尝试获取所有活跃的 aiohttp 客户端会话
            closed_sessions = 0
            
            # 检查是否有全局的 aiohttp 会话注册表
            if hasattr(aiohttp, '_sessions'):
                sessions = list(aiohttp._sessions)
                for session_ref in sessions:
                    session = session_ref() if isinstance(session_ref, weakref.ref) else session_ref
                    if session and not session.closed:
                        try:
                            await session.close()
                            closed_sessions += 1
                            print(f"✅ 已关闭 aiohttp 客户端会话")
                        except Exception as e:
                            print(f"⚠️ 关闭会话时出现警告: {e}")
            
            # 强制垃圾回收，清理未引用的对象
            gc.collect()
            
            # 等待一小段时间让连接正常关闭
            await CleanupHelper.safe_sleep(0.2)
            
            # 再次垃圾回收
            gc.collect()
            
            if closed_sessions > 0:
                print(f"✅ 共关闭了 {closed_sessions} 个 aiohttp 客户端会话")
            
        except ImportError:
            # aiohttp 未安装，跳过
            pass
        except Exception as e:
            # 清理过程中的错误不应该阻止程序退出
            print(f"⚠️ aiohttp 清理过程中出现警告: {e}")
    
    @staticmethod
    async def cleanup_litellm_resources():
        """清理 LiteLLM 相关资源"""
        try:
            # 尝试关闭 LiteLLM 的内部客户端会话
            import litellm
            
            # 查找并关闭所有可能的 aiohttp 客户端会话
            # 检查 LiteLLM 的各种可能的会话属性
            session_attrs = ['_client_session', '_session', 'session', '_aiohttp_session']
            
            for attr in session_attrs:
                if hasattr(litellm, attr):
                    session = getattr(litellm, attr)
                    if session and hasattr(session, 'close'):
                        try:
                            await session.close()
                            print(f"✅ 已关闭 LiteLLM {attr}")
                        except Exception as e:
                            print(f"⚠️ 关闭 {attr} 时出现警告: {e}")
            
            # 尝试访问 LiteLLM 内部的 aiohttp 客户端
            try:
                # 检查是否有活跃的 aiohttp 连接器
                import aiohttp
                
                # 获取当前事件循环中的所有 aiohttp 连接器
                loop = asyncio.get_event_loop()
                
                # 强制关闭所有 aiohttp 连接器
                for task in asyncio.all_tasks(loop):
                    if hasattr(task, '_coro') and task._coro:
                        coro_name = str(task._coro)
                        if 'aiohttp' in coro_name and not task.done():
                            task.cancel()
                
                # 等待被取消的任务完成
                await CleanupHelper.safe_sleep(0.1)
                
            except Exception as e:
                print(f"⚠️ 清理 aiohttp 连接器时出现警告: {e}")
            
            # 强制垃圾回收
            gc.collect()
            
            # 等待一小段时间让 LiteLLM 的内部清理完成
            await CleanupHelper.safe_sleep(0.1)
            
        except Exception as e:
            print(f"⚠️ LiteLLM 清理过程中出现警告: {e}")
    
    @staticmethod
    async def comprehensive_cleanup():
        """执行全面的资源清理（原始版本，可能被取消）"""
        # 1. 清理 LiteLLM 资源
        await CleanupHelper.cleanup_litellm_resources()
        
        # 2. 清理 aiohttp 会话
        await CleanupHelper.cleanup_aiohttp_sessions()
        
        # 3. 最终垃圾回收
        gc.collect()
        
        # 4. 短暂等待，让所有异步清理完成
        await asyncio.sleep(0.1)
    
    @staticmethod
    async def safe_comprehensive_cleanup():
        """执行全面的资源清理（安全版本，不会被取消中断）"""
        try:
            # 1. 清理 LiteLLM 资源
            await CleanupHelper.cleanup_litellm_resources()
            
            # 2. 清理 aiohttp 会话
            await CleanupHelper.cleanup_aiohttp_sessions()
            
            # 3. 最终垃圾回收
            gc.collect()
            
            # 4. 短暂等待，让所有异步清理完成
            await CleanupHelper.safe_sleep(0.1)
            
        except Exception as e:
            print(f"⚠️ 安全清理过程中出现警告: {e}")
            # 继续执行紧急清理
            await CleanupHelper.emergency_cleanup()
    
    @staticmethod
    async def emergency_cleanup():
        """紧急清理 - 同步版本，最小化异步操作"""
        try:
            print("🚨 执行紧急清理...")
            
            # 1. 同步垃圾回收
            gc.collect()
            
            # 2. 尝试清理一些基本资源
            try:
                import litellm
                # 重置 litellm 的一些状态
                if hasattr(litellm, 'reset'):
                    litellm.reset()
            except Exception:
                pass
            
            # 3. 最终垃圾回收
            gc.collect()
            
            print("✅ 紧急清理完成")
            
        except Exception as e:
            print(f"⚠️ 紧急清理失败: {e}")
    
    @staticmethod
    def suppress_aiohttp_warnings():
        """抑制 aiohttp 相关的警告信息（仅在需要时使用）"""
        # 只抑制一些不重要的警告，保留重要的错误信息
        warnings.filterwarnings("ignore", message=".*coroutine.*was never awaited.*")
        
        # 设置 asyncio 日志级别为 WARNING，这样仍能看到重要错误
        logging.getLogger('asyncio').setLevel(logging.WARNING) 