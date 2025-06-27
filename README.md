# Agent Development Kit (ADK)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Unit Tests](https://github.com/google/adk-python/actions/workflows/python-unit-tests.yml/badge.svg)](https://github.com/google/adk-python/actions/workflows/python-unit-tests.yml)
[![r/agentdevelopmentkit](https://img.shields.io/badge/Reddit-r%2Fagentdevelopmentkit-FF4500?style=flat&logo=reddit&logoColor=white)](https://www.reddit.com/r/agentdevelopmentkit/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/google/adk-python)

<html>
    <h2 align="center">
      <img src="https://raw.githubusercontent.com/google/adk-python/main/assets/agent-development-kit.png" width="256"/>
    </h2>
    <h3 align="center">
      An open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control.
    </h3>
    <h3 align="center">
      Important Links:
      <a href="https://google.github.io/adk-docs/">Docs</a>, 
      <a href="https://github.com/google/adk-samples">Samples</a>,
      <a href="https://github.com/google/adk-java">Java ADK</a> &
      <a href="https://github.com/google/adk-web">ADK Web</a>.
    </h3>
</html>

Agent Development Kit (ADK) is a flexible and modular framework for developing and deploying AI agents. While optimized for Gemini and the Google ecosystem, ADK is model-agnostic, deployment-agnostic, and is built for compatibility with other frameworks. ADK was designed to make agent development feel more like software development, to make it easier for developers to create, deploy, and orchestrate agentic architectures that range from simple tasks to complex workflows.


---

## ✨ Key Features

- **Rich Tool Ecosystem**: Utilize pre-built tools, custom functions,
  OpenAPI specs, or integrate existing tools to give agents diverse
  capabilities, all for tight integration with the Google ecosystem.

- **Code-First Development**: Define agent logic, tools, and orchestration
  directly in Python for ultimate flexibility, testability, and versioning.

- **Modular Multi-Agent Systems**: Design scalable applications by composing
  multiple specialized agents into flexible hierarchies.

- **Deploy Anywhere**: Easily containerize and deploy agents on Cloud Run or
  scale seamlessly with Vertex AI Agent Engine.

## 🤖 Agent2Agent (A2A) Protocol and ADK Integration

For remote agent-to-agent communication, ADK integrates with the
[A2A protocol](https://github.com/google-a2a/A2A/).
See this [example](https://github.com/google-a2a/a2a-samples/tree/main/samples/python/agents/google_adk)
for how they can work together.

## 🚀 Installation

### Stable Release (Recommended)

You can install the latest stable version of ADK using `pip`:

```bash
pip install google-adk
```

The release cadence is weekly.

This version is recommended for most users as it represents the most recent official release.

### Development Version
Bug fixes and new features are merged into the main branch on GitHub first. If you need access to changes that haven't been included in an official PyPI release yet, you can install directly from the main branch:

```bash
pip install git+https://github.com/google/adk-python.git@main
```

Note: The development version is built directly from the latest code commits. While it includes the newest fixes and features, it may also contain experimental changes or bugs not present in the stable release. Use it primarily for testing upcoming changes or accessing critical fixes before they are officially released.

## 📚 Documentation

Explore the full documentation for detailed guides on building, evaluating, and
deploying agents:

* **[Documentation](https://google.github.io/adk-docs)**

## 🏁 Feature Highlight

### Define a single agent:

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash", # Or your preferred Gemini model
    instruction="You are a helpful assistant. Answer user questions using Google Search when needed.",
    description="An assistant that can search the web.",
    tools=[google_search]
)
```

### Define a multi-agent system:

Define a multi-agent system with coordinator agent, greeter agent, and task execution agent. Then ADK engine and the model will guide the agents works together to accomplish the task.

```python
from google.adk.agents import LlmAgent, BaseAgent

# Define individual agents
greeter = LlmAgent(name="greeter", model="gemini-2.0-flash", ...)
task_executor = LlmAgent(name="task_executor", model="gemini-2.0-flash", ...)

# Create parent agent and assign children via sub_agents
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    description="I coordinate greetings and tasks.",
    sub_agents=[ # Assign sub_agents here
        greeter,
        task_executor
    ]
)
```

### Development UI

A built-in development UI to help you test, evaluate, debug, and showcase your agent(s).

<img src="https://raw.githubusercontent.com/google/adk-python/main/assets/adk-web-dev-ui-function-call.png"/>

###  Evaluate Agents

```bash
adk eval \
    samples_for_testing/hello_world \
    samples_for_testing/hello_world/hello_world_eval_set_001.evalset.json
```

## 🤝 Contributing

We welcome contributions from the community! Whether it's bug reports, feature requests, documentation improvements, or code contributions, please see our
- [General contribution guideline and flow](https://google.github.io/adk-docs/contributing-guide/).
- Then if you want to contribute code, please read [Code Contributing Guidelines](./CONTRIBUTING.md) to get started.

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

*Happy Agent Building!*

# ADK 自定义应用框架

这是一个基于 Google ADK (Agent Development Kit) 构建的自定义应用框架，完全绕过 CLI 工具，直接使用 ADK 核心模块进行开发。

## 🚀 项目特性

- **完全绕过 CLI**: 直接使用 ADK 核心模块，无需依赖 `adk web` 等命令
- **模块化设计**: 清晰的代码组织结构，易于扩展和维护
- **多接口支持**: 支持控制台、Web、API 等多种交互方式
- **高度可定制**: 所有组件都可根据需求进行定制
- **易于调试**: 可在 IDE 中直接调试，便于开发

## 📁 项目结构

```
src/apps/
├── core/                   # 核心应用逻辑
│   ├── app_factory.py     # 应用工厂
│   ├── base_app.py        # 基础应用类
│   └── config.py          # 配置管理
├── agents/                # 自定义代理
│   └── my_agent.py        # 示例代理
├── tools/                 # 自定义工具
│   └── custom_tools.py    # 示例工具
├── interfaces/            # 用户接口
│   ├── console_interface.py  # 控制台接口
│   └── web_interface.py      # Web 接口
├── services/              # 自定义服务
└── utils/                 # 工具函数
```

## 🛠️ 安装和设置

### 1. 环境准备

```bash
# 创建并激活 conda 环境
conda create -n adk-hav python=3.11
conda activate adk-hav

# 安装依赖
pip install litellm
```

### 2. 项目验证

```bash
# 运行测试脚本验证项目设置
python test_setup.py
```

### 3. 配置环境变量

创建 `.env` 文件并配置：

```bash
# 应用配置
APP_NAME=my_custom_app
DEBUG=true

# LLM 配置
MODEL_NAME=gpt-4o-mini
API_KEY=your_openai_api_key_here

# 可选配置
# MAX_TOKENS=2000
# TEMPERATURE=0.7
```

## 🎯 使用方式

### 控制台模式

```bash
python main.py --mode console
```

### Web 模式

```bash
python main.py --mode web --host 127.0.0.1 --port 8000
```

### API 模式

```bash
python main.py --mode api --port 8080
```

### 调试模式

```bash
python main.py --debug
```

## 🔧 核心组件

### 1. 配置管理 (AppConfig)

- 支持环境变量加载
- 配置验证和默认值
- 灵活的配置来源

### 2. 应用工厂 (AppFactory)

- 创建和配置各种服务
- 统一的组件管理
- 依赖注入模式

### 3. 自定义代理 (Agent)

- 基于 LiteLLM 的模型支持
- 内置工具集成
- 中文对话优化

### 4. 自定义工具

- 时间查询工具
- 数学计算工具
- 随机字符串生成
- 易于扩展新工具

### 5. 多接口支持

- **控制台接口**: 交互式命令行对话
- **Web 接口**: 基于 FastAPI 和 WebSocket
- **API 接口**: RESTful API 服务

## 📝 开发指南

### 添加新工具

1. 在 `src/apps/tools/custom_tools.py` 中定义新函数
2. 使用 `FunctionTool` 包装函数
3. 在 `get_custom_tools()` 中添加工具

```python
def my_new_tool(param: str) -> str:
    """新工具的描述"""
    return f"处理结果: {param}"

# 在 get_custom_tools() 中添加
def get_custom_tools():
    return [
        # ... 现有工具
        FunctionTool(my_new_tool),
    ]
```

### 自定义代理

修改 `src/apps/agents/my_agent.py` 中的代理配置：

```python
def create_my_agent(config: AppConfig) -> Agent:
    agent = Agent(
        name='MyCustomAgent',
        instruction="你的自定义指令",
        model=LiteLlm(model=config.model_name, api_key=config.api_key),
        tools=get_custom_tools()
    )
    return agent
```

### 添加新接口

1. 在 `src/apps/interfaces/` 中创建新接口类
2. 继承适当的基类
3. 在 `AppFactory` 中添加创建方法

## 🚦 API 参考

### 主要类

- `AppConfig`: 应用配置管理
- `AppFactory`: 组件工厂
- `BaseApp`: 基础应用类
- `ConsoleInterface`: 控制台接口
- `WebInterface`: Web 接口

### 命令行参数

- `--mode`: 运行模式 (console/web/api)
- `--config`: 配置文件路径
- `--debug`: 启用调试模式
- `--host`: 服务器主机地址
- `--port`: 服务器端口

## 🔧 问题解决

### aiohttp 客户端会话清理

我们已经解决了 LiteLLM 中 aiohttp 客户端会话未正确关闭的问题：

- **根本原因**: LiteLLM v1.72.0+ 默认使用 aiohttp 传输以提高性能，但内部会话管理存在问题
- **解决方案**: 
  - 禁用 LiteLLM 的 aiohttp 传输 (`DISABLE_AIOHTTP_TRANSPORT=True`)
  - 实现智能资源清理，主动关闭所有 aiohttp 客户端会话
  - 在应用退出时执行全面的异步资源清理

### 清理机制

项目包含完整的资源清理机制：

```python
from apps.utils.cleanup_helper import CleanupHelper

# 配置 LiteLLM 传输（在应用启动时）
CleanupHelper.configure_litellm_transport()

# 执行全面清理（在应用退出时）
await CleanupHelper.comprehensive_cleanup()
```

## 🔍 故障排除

### 常见问题

1. **导入错误**: 确保已安装所有依赖
2. **API 密钥**: 检查 `.env` 文件中的 API_KEY 配置
3. **端口占用**: 使用 `--port` 参数指定其他端口
4. **aiohttp 错误**: 项目已自动处理，无需手动干预

### 调试技巧

1. 使用 `--debug` 参数启用详细日志
2. 运行测试验证项目状态（详见下方测试部分）
3. 检查环境变量加载是否正确

## 🧪 测试套件

项目包含完整的测试套件，位于 `tests/havoc/` 目录：

### 测试文件说明

- **`test_setup.py`** - 项目验证脚本，验证配置、依赖和组件
- **`test_cleanup.py`** - 清理功能测试，验证资源管理
- **`quick_start.py`** - 快速开始脚本，一键设置环境
- **`run_tests.py`** - 统一测试入口，支持运行单个或多个测试

### 测试调用方式

#### 1. 从根目录运行

```bash
# 项目验证测试
python tests/havoc/test_setup.py

# 清理功能测试
python tests/havoc/test_cleanup.py

# 快速开始脚本
python tests/havoc/quick_start.py

# 统一测试入口
python tests/havoc/run_tests.py [setup|cleanup|quickstart|all]
```

#### 2. 从 tests/havoc 目录运行

```bash
cd tests/havoc

# 单独运行测试
python test_setup.py
python test_cleanup.py
python quick_start.py

# 使用统一入口
python run_tests.py --list  # 列出所有测试
python run_tests.py setup   # 运行项目验证
python run_tests.py all     # 运行所有测试
```

#### 3. 使用 Python 模块方式

```bash
# 从根目录运行
python -m tests.havoc.test_setup
python -m tests.havoc.test_cleanup  
python -m tests.havoc.quick_start
python -m tests.havoc.run_tests
```

#### 4. 作为模块导入

```python
from tests.havoc import run_setup_test, test_cleanup, run_quick_start

# 运行测试
await run_setup_test()
await test_cleanup()
await run_quick_start()
```

### 推荐测试流程

1. **首次使用**：`python tests/havoc/quick_start.py`
2. **验证项目**：`python tests/havoc/test_setup.py`
3. **测试清理**：`python tests/havoc/test_cleanup.py`
4. **运行所有测试**：`python tests/havoc/run_tests.py all`

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

本项目遵循 Apache 2.0 许可证。

## 🙏 致谢

- Google ADK 团队提供的优秀框架
- LiteLLM 项目的多模型支持
- 社区贡献者的宝贵建议
