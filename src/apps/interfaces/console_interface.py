"""
控制台接口实现
"""
import asyncio
from google.genai import types
from google.adk.sessions import Session

from ..core.base_app import BaseApp
from ..core.config import AppConfig


class ConsoleInterface(BaseApp):
    """控制台接口"""
    
    def __init__(self, config: AppConfig):
        super().__init__(config)
        self.session = None
    
    async def run(self):
        """运行控制台应用"""
        try:
            await self.initialize()
            
            print(f"🤖 {self.config.app_name} 控制台启动")
            print("输入 'exit'、'quit' 或 '退出' 来结束对话")
            print("输入 'help' 或 '帮助' 查看可用命令")
            print("-" * 50)
            
            # 创建会话
            self.session = await self.runner.session_service.create_session(
                app_name=self.config.app_name,
                user_id='console_user'
            )
            
            while True:
                try:
                    user_input = input("\n👤 您: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['exit', 'quit', '退出']:
                        print("👋 再见!")
                        break
                    
                    if user_input.lower() in ['help', '帮助']:
                        self._show_help()
                        continue
                    
                    if user_input.lower() in ['clear', '清屏']:
                        print("\n" * 50)
                        continue
                    
                    await self._process_message(user_input)
                    
                except KeyboardInterrupt:
                    print("\n👋 再见!")
                    break
                except EOFError:
                    # 处理 EOF（例如管道输入结束或 Ctrl+D）
                    print("\n👋 再见!")
                    break
                except Exception as e:
                    print(f"❌ 错误: {e}")
                    if self.config.debug:
                        import traceback
                        traceback.print_exc()
                    # 如果是致命错误，退出循环
                    if "EOF" in str(e):
                        break
        
        finally:
            print("\n🧹 正在清理资源...")
            await self.cleanup()
    
    async def _process_message(self, message: str):
        """处理用户消息"""
        content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=message)]
        )
        
        print("🤖 助手: ", end="", flush=True)
        
        try:
            response_parts = []
            async for event in self.runner.run_async(
                user_id=self.session.user_id,
                session_id=self.session.id,
                new_message=content
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end="", flush=True)
                            response_parts.append(part.text)
            
            if not response_parts:
                print("(没有响应)")
            
        except Exception as e:
            print(f"\n❌ 处理消息时出错: {e}")
            if self.config.debug:
                import traceback
                traceback.print_exc()
        
        print()  # 换行
    
    def _show_help(self):
        """显示帮助信息"""
        help_text = """
📖 可用命令:
  help/帮助    - 显示此帮助信息
  clear/清屏   - 清除屏幕
  exit/quit/退出 - 退出程序

💡 功能介绍:
  - 智能对话：直接输入您的问题或需求
  - 时间查询：询问当前时间
  - 数学计算：进行加法、乘法等运算
  - 随机生成：生成随机字符串

🔧 示例:
  "现在几点了？"
  "帮我计算 123 + 456"
  "生成一个 8 位的随机字符串"
        """
        print(help_text) 