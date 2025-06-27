"""
应用配置管理
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

@dataclass
class AppConfig:
    """应用配置"""
    # 基础配置
    app_name: str = "my_custom_app"
    debug: bool = False
    
    # 服务配置
    use_in_memory: bool = True
    session_service_uri: Optional[str] = None
    gcs_bucket: Optional[str] = None
    
    # Web 接口配置
    use_original_adk_web: bool = False
    
    # API 配置
    api_key: Optional[str] = None
    model_name: str = "deepseek/deepseek-chat"
    api_base: Optional[str] = "https://api.deepseek.com"
    
    # 服务器配置
    host: str = "127.0.0.1"
    port: int = 8000
    
    @classmethod
    def from_env(cls, env_file: str = ".env") -> "AppConfig":
        """从环境变量加载配置"""
        load_dotenv(env_file, override=True)
        
        return cls(
            app_name=os.getenv("APP_NAME", "my_custom_app"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            use_in_memory=os.getenv("USE_IN_MEMORY", "true").lower() == "true",
            session_service_uri=os.getenv("SESSION_SERVICE_URI"),
            gcs_bucket=os.getenv("GCS_BUCKET"),
            use_original_adk_web=os.getenv("USE_ORIGINAL_ADK_WEB", "false").lower() == "true",
            api_key=os.getenv("API_KEY"),
            model_name=os.getenv("MODEL_NAME", "deepseek/deepseek-chat"),
            api_base=os.getenv("API_BASE", "https://api.deepseek.com"),
            host=os.getenv("HOST", "127.0.0.1"),
            port=int(os.getenv("PORT", "8000"))
        )
    
    def validate(self) -> bool:
        """验证配置"""
        if not self.api_key:
            print("警告: 未设置 API_KEY")
            return False
        return True 