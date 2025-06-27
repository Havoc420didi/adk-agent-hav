# DeepSeek API 配置指南

本项目已配置为使用 DeepSeek API，这是一个高性能且经济实惠的中文 AI 模型服务。

## 🔧 配置信息

### 当前配置

项目已预配置以下 DeepSeek 设置：

```bash
# DeepSeek API 配置
MODEL_NAME=deepseek/deepseek-chat
API_KEY=sk-9c8e30190b2543bbacf7dc47d38df19e
API_BASE=https://api.deepseek.com
```

### 模型特点

- **模型名称**: `deepseek/deepseek-chat`
- **API 端点**: `https://api.deepseek.com`
- **语言支持**: 中文优化，支持多语言
- **性能**: 高质量对话生成
- **成本**: 相对经济实惠

## 🚀 使用方式

### 1. 直接运行（已配置好）

```bash
# 控制台模式
python main.py --mode console

# Web 模式
python main.py --mode web --port 8000
```

### 2. 验证配置

```bash
# 运行测试验证
python test_setup.py
```

### 3. 快速开始

```bash
# 一键设置和启动
python quick_start.py
```

## 🛠️ 技术实现

### LiteLLM 配置

代码中的 DeepSeek 配置如下：

```python
# src/apps/agents/my_agent.py
llm_model = LiteLlm(
    model="deepseek/deepseek-chat",
    api_key="sk-9c8e30190b2543bbacf7dc47d38df19e",
    api_base="https://api.deepseek.com"
)
```

### 配置类支持

```python
# src/apps/core/config.py
@dataclass
class AppConfig:
    model_name: str = "deepseek/deepseek-chat"
    api_key: Optional[str] = None
    api_base: Optional[str] = "https://api.deepseek.com"
```

## 📝 环境变量

项目支持通过 `.env` 文件配置：

```env
# 应用配置
APP_NAME=my_custom_app
DEBUG=true

# DeepSeek API 配置
MODEL_NAME=deepseek/deepseek-chat
API_KEY=sk-9c8e30190b2543bbacf7dc47d38df19e
API_BASE=https://api.deepseek.com

# 可选配置
# MAX_TOKENS=2000
# TEMPERATURE=0.7
```

## 🔄 切换到其他模型

如需切换到其他模型提供商，只需修改 `.env` 文件：

### OpenAI
```env
MODEL_NAME=gpt-4o-mini
API_KEY=your_openai_api_key
API_BASE=https://api.openai.com/v1
```

### Anthropic Claude
```env
MODEL_NAME=anthropic/claude-3-sonnet-20240229
API_KEY=your_anthropic_api_key
API_BASE=https://api.anthropic.com
```

### 其他支持的模型
参考 [LiteLLM 文档](https://docs.litellm.ai/docs/providers) 查看支持的模型列表。

## 🎯 DeepSeek 优势

1. **中文优化**: 对中文理解和生成效果优秀
2. **成本效益**: 相比 GPT-4 等模型更经济
3. **高性能**: 响应速度快，质量稳定
4. **易集成**: 兼容 OpenAI API 格式

## 🔍 故障排除

### 常见问题

1. **API 密钥错误**
   - 检查 `.env` 文件中的 `API_KEY` 是否正确
   - 确认 API 密钥有效且有足够余额

2. **网络连接问题**
   - 确认能访问 `https://api.deepseek.com`
   - 检查防火墙和代理设置

3. **模型调用失败**
   - 验证 `MODEL_NAME` 格式正确
   - 检查 `API_BASE` URL 是否正确

### 调试命令

```bash
# 查看当前配置
python -c "
import sys
sys.path.insert(0, 'src')
from apps.core.config import AppConfig
config = AppConfig.from_env()
print(f'模型: {config.model_name}')
print(f'API Base: {config.api_base}')
print(f'API Key: {config.api_key[:10]}...')
"

# 测试模型创建
python -c "
import sys
sys.path.insert(0, 'src')
from apps.agents.my_agent import create_my_agent
from apps.core.config import AppConfig
agent = create_my_agent(AppConfig.from_env())
print(f'代理创建成功: {agent.name}')
"
```

## 📚 参考资源

- [DeepSeek 官网](https://www.deepseek.com/)
- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [LiteLLM DeepSeek 集成](https://docs.litellm.ai/docs/providers/deepseek)
- [项目主文档](README.md)

## 🤝 获取 API 密钥

如需获取自己的 DeepSeek API 密钥：

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册账户并完成认证
3. 创建 API 密钥
4. 将密钥替换到 `.env` 文件中

---

**注意**: 当前配置中的 API 密钥仅用于演示，建议在生产环境中使用自己的密钥。 