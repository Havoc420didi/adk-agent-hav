"""
应用工厂 - 创建和配置不同类型的应用
"""
from typing import Optional
from google.adk.runners import Runner, InMemoryRunner
from google.adk import sessions, artifacts, memory
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService

from .config import AppConfig


class AppFactory:
    """应用工厂类"""
    
    def __init__(self, config: AppConfig):
        self.config = config
    
    def create_runner(self, app_name: Optional[str] = None) -> Runner:
        """创建 Runner 实例"""
        # 延迟导入以避免循环依赖
        from ..agents.my_custom_app.agent import root_agent
        
        agent = root_agent
        runner_app_name = app_name or self.config.app_name
        
        if self.config.use_in_memory:
            return InMemoryRunner(agent=agent, app_name=runner_app_name)
        else:
            # 根据配置选择不同的服务
            session_service = self._create_session_service()
            artifact_service = self._create_artifact_service()
            memory_service = self._create_memory_service()
            credential_service = self._create_credential_service()
            
            return Runner(
                app_name=runner_app_name,
                agent=agent,
                session_service=session_service,
                artifact_service=artifact_service,
                memory_service=memory_service,
                credential_service=credential_service
            )
    
    def _create_session_service(self):
        """创建会话服务"""
        if self.config.session_service_uri:
            if self.config.session_service_uri.startswith('sqlite://'):
                from sqlalchemy import create_engine
                engine = create_engine(self.config.session_service_uri)
                return sessions.DatabaseSessionService(engine)
        return sessions.InMemorySessionService()
    
    def _create_artifact_service(self):
        """创建工件服务"""
        if self.config.gcs_bucket:
            return artifacts.GcsArtifactService(bucket_name=self.config.gcs_bucket)
        return artifacts.InMemoryArtifactService()
    
    def _create_memory_service(self):
        """创建内存服务"""
        return memory.InMemoryMemoryService()
    
    def _create_credential_service(self):
        """创建凭证服务"""
        return InMemoryCredentialService()
    
    def create_console_interface(self):
        """创建控制台接口"""
        from ..interfaces.console_interface import ConsoleInterface
        return ConsoleInterface(self.config)
    
    def create_web_interface(self):
        """创建 Web 接口"""
        from ..interfaces.web_interface import WebInterface
        return WebInterface(self.config) 