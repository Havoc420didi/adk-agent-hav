"""
Web 接口实现 - 支持原始 ADK 和自定义两种模式
"""
import os
import logging
import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from google.genai import types

from ..core.base_app import BaseApp
from ..core.config import AppConfig


class WebInterface(BaseApp):
    """Web 接口 - 支持多种模式"""
    
    def __init__(self, config: AppConfig):
        super().__init__(config)
        self.use_original_adk = getattr(config, 'use_original_adk_web', False)
        
        if self.use_original_adk:
            self._setup_original_adk_web()
        else:
            self.app = FastAPI(title=f"{config.app_name} Web Interface")
            self._setup_custom_routes()
    
    def _setup_original_adk_web(self):
        """设置原始 ADK Web 服务"""
        try:
            from google.adk.cli.fast_api import get_fast_api_app
            from google.adk.cli.utils import logs
            
            # 设置日志
            logs.setup_adk_logger(logging.INFO)
            
            # 创建 agents 目录结构
            agents_dir = self._create_agents_directory()
            
            @asynccontextmanager
            async def _lifespan(app: FastAPI):
                print(f"""
+-----------------------------------------------------------------------------+
| ADK Web 服务已启动                                                          |
|                                                                             |
| 访问地址: http://localhost:{self.config.port}                               |
+-----------------------------------------------------------------------------+
""")
                yield
                print("""
+-----------------------------------------------------------------------------+
| ADK Web 服务正在关闭...                                                     |
+-----------------------------------------------------------------------------+
""")
            
            # 使用原始 ADK 的 FastAPI 应用
            self.app = get_fast_api_app(
                agents_dir=agents_dir,
                session_service_uri=None,
                artifact_service_uri=None,
                memory_service_uri=None,
                eval_storage_uri=None,
                allow_origins=None,
                web=True,
                trace_to_cloud=False,
                lifespan=_lifespan,
                a2a=False,
                host=self.config.host,
                port=self.config.port,
            )
            
            print(f"✅ 原始 ADK Web 服务配置完成")
            print(f"📁 Agents 目录: {agents_dir}")
            
        except ImportError as e:
            print(f"❌ 无法导入 ADK 模块: {e}")
            print("💡 回退到自定义 Web 接口")
            self.use_original_adk = False
            self._setup_custom_web_fallback()
        except Exception as e:
            print(f"❌ ADK Web 服务初始化失败: {e}")
            print("💡 回退到自定义 Web 接口")
            self.use_original_adk = False
            self._setup_custom_web_fallback()
    
    def _create_agents_directory(self):
        """创建 agents 目录结构用于 ADK"""
        # 在项目根目录创建临时的 agents 目录
        project_root = Path(__file__).parent.parent.parent.parent
        agents_dir = project_root / "temp_agents"
        agent_dir = agents_dir / self.config.app_name
        
        # 确保目录存在
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 __init__.py
        init_file = agent_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("# Agent package\n")
        
        # 创建或复制 agent.py
        agent_file = agent_dir / "agent.py"
        if not agent_file.exists():
            # 创建一个简单的 agent.py
            agent_content = f'''"""
{self.config.app_name} Agent
"""
from google.adk.agents.base_agent import BaseAgent

class {self.config.app_name.title().replace("_", "")}Agent(BaseAgent):
    """基础 Agent 实现"""
    
    def __init__(self):
        super().__init__()
        self.name = "{self.config.app_name}"
    
    async def run(self, user_input: str) -> str:
        """处理用户输入"""
        return f"您好！我是 {{self.name}} 助手。您说: {{user_input}}"

# 导出 root_agent
root_agent = {self.config.app_name.title().replace("_", "")}Agent()
'''
            agent_file.write_text(agent_content)
        
        return str(agents_dir)
    
    def _setup_custom_web_fallback(self):
        """设置自定义 Web 接口作为回退"""
        self.app = FastAPI(title=f"{self.config.app_name} Web Interface")
        self._setup_custom_routes()
    
    def _setup_custom_routes(self):
        """设置自定义路由"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home():
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ADK Web 应用</title>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .header {{ background: #f0f0f0; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                    #chat {{ border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }}
                    #messageInput {{ width: 70%; padding: 10px; }}
                    button {{ padding: 10px 20px; }}
                    .message {{ margin: 5px 0; }}
                    .user {{ color: #0066cc; }}
                    .assistant {{ color: #009900; }}
                    .mode-info {{ color: #666; font-size: 0.9em; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🤖 {self.config.app_name} Web 应用</h1>
                    <p class="mode-info">模式: 自定义 Web 接口</p>
                    <p class="mode-info">💡 要使用原始 ADK Web UI，请在配置中设置 use_original_adk_web=true</p>
                </div>
                <div id="chat"></div>
                <input id="messageInput" type="text" placeholder="输入消息...">
                <button onclick="sendMessage()">发送</button>
                
                <script>
                    const ws = new WebSocket(`ws://localhost:${{window.location.port}}/ws`);
                    const chat = document.getElementById('chat');
                    
                    ws.onmessage = function(event) {{
                        const div = document.createElement('div');
                        div.className = 'message assistant';
                        div.innerHTML = `<strong>🤖:</strong> ${{event.data}}`;
                        chat.appendChild(div);
                        chat.scrollTop = chat.scrollHeight;
                    }};
                    
                    function sendMessage() {{
                        const input = document.getElementById('messageInput');
                        if (input.value) {{
                            const div = document.createElement('div');
                            div.className = 'message user';
                            div.innerHTML = `<strong>👤:</strong> ${{input.value}}`;
                            chat.appendChild(div);
                            chat.scrollTop = chat.scrollHeight;
                            ws.send(input.value);
                            input.value = '';
                        }}
                    }}
                    
                    document.getElementById('messageInput').addEventListener('keypress', function(e) {{
                        if (e.key === 'Enter') sendMessage();
                    }});
                </script>
            </body>
            </html>
            """
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            
            # 为每个连接创建会话
            session = await self.runner.session_service.create_session(
                app_name=self.config.app_name,
                user_id=f'web_user_{id(websocket)}'
            )
            
            try:
                while True:
                    message = await websocket.receive_text()
                    
                    content = types.Content(
                        role='user',
                        parts=[types.Part.from_text(text=message)]
                    )
                    
                    response_text = ""
                    async for event in self.runner.run_async(
                        user_id=session.user_id,
                        session_id=session.id,
                        new_message=content
                    ):
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                if part.text:
                                    response_text += part.text
                    
                    await websocket.send_text(response_text)
                    
            except WebSocketDisconnect:
                pass
    
    async def run(self):
        """运行 Web 应用"""
        if not self.use_original_adk:
            await self.initialize()
        
        mode_text = "原始 ADK Web 服务" if self.use_original_adk else "自定义 Web 接口"
        print(f"🌐 {mode_text} 启动: http://{self.config.host}:{self.config.port}")
        
        config = uvicorn.Config(
            self.app,
            host=self.config.host,
            port=self.config.port,
            reload=self.config.debug
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    async def cleanup(self):
        """清理资源"""
        await super().cleanup()
        
        # 清理临时 agents 目录
        if self.use_original_adk:
            try:
                import shutil
                project_root = Path(__file__).parent.parent.parent.parent
                temp_agents_dir = project_root / "temp_agents"
                if temp_agents_dir.exists():
                    shutil.rmtree(temp_agents_dir)
                    print("🧹 已清理临时 agents 目录")
            except Exception as e:
                print(f"⚠️ 清理临时目录时出现问题: {e}") 