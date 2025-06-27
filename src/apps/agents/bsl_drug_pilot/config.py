"""
BSL Drug Pilot Agent 配置
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class BSLDrugPilotConfig:
    """BSL药物试点Agent配置类"""
    
    # 模型配置
    model_name: str = "deepseek/deepseek-chat"
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    
    # 算法配置
    cuda_device: str = "cuda:0"
    batch_size: int = 32
    request_timeout: float = 120.0
    
    # CUDA配置
    cuda_visible_devices: str = "0"
    
    @classmethod
    def from_env(cls):
        """从环境变量加载配置"""
        return cls(
            model_name=os.getenv("MODEL_NAME", "deepseek/deepseek-chat"),
            api_key=os.getenv("API_KEY"),
            api_base=os.getenv("API_BASE"),
            cuda_device=os.getenv("BSL_CUDA_DEVICE", "cuda:0"),
            batch_size=int(os.getenv("BSL_BATCH_SIZE", "32")),
            request_timeout=float(os.getenv("BSL_REQUEST_TIMEOUT", "120.0")),
            cuda_visible_devices=os.getenv("CUDA_VISIBLE_DEVICES", "0"),
        )
    
    def setup_cuda_environment(self):
        """设置CUDA环境变量"""
        os.environ['CUDA_VISIBLE_DEVICES'] = self.cuda_visible_devices