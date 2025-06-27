# Web 接口使用指南

## 概述

本应用支持两种 Web 接口模式：

1. **自定义 Web 接口**：简化的聊天界面，基于 HTML/JavaScript
2. **原始 ADK Web 接口**：完整的 Angular 前端，具有丰富的开发者功能

## 配置方法

在 `.env` 文件中设置以下选项：

```bash
# 使用自定义 Web 接口（默认）
USE_ORIGINAL_ADK_WEB=false

# 使用原始 ADK Web 接口
USE_ORIGINAL_ADK_WEB=true
```

## 模式对比

### 自定义 Web 接口
- ✅ 简单易用的聊天界面
- ✅ 快速启动
- ✅ 轻量级实现
- ❌ 功能有限
- ❌ 无高级开发工具

### 原始 ADK Web 接口
- ✅ 完整的开发者 UI
- ✅ 多 Agent 支持
- ✅ 会话管理
- ✅ 评估工具
- ✅ 调试功能
- ❌ 需要更多依赖
- ❌ 启动稍慢

## 使用方法

### 1. 自定义 Web 接口

```bash
# 在 .env 中设置
USE_ORIGINAL_ADK_WEB=false

# 启动应用
python main.py --mode web --port 8000
```

访问: http://localhost:8000

### 2. 原始 ADK Web 接口

```bash
# 在 .env 中设置
USE_ORIGINAL_ADK_WEB=true

# 启动应用
python main.py --mode web --port 8000
```

访问: http://localhost:8000/dev-ui/

## 故障排除

### 原始 ADK Web 接口无法启动

如果原始 ADK Web 接口启动失败，系统会自动回退到自定义 Web 接口。

常见问题：
1. **缺少依赖模块**：确保安装了完整的 google-adk 包
2. **权限问题**：确保有创建临时目录的权限
3. **端口冲突**：尝试更换端口

### 自定义 Web 接口问题

1. **WebSocket 连接失败**：检查防火墙设置
2. **Agent 无响应**：检查 API_KEY 和模型配置
3. **页面无法加载**：检查端口是否被占用

## 高级配置

### 自定义 Agent 目录

原始 ADK Web 接口会在项目根目录创建 `temp_agents` 目录，包含：

```
temp_agents/
├── your_app_name/
│   ├── __init__.py
│   └── agent.py
```

您可以手动编辑 `agent.py` 来自定义 Agent 行为。

### 清理

应用退出时会自动清理临时文件。如需手动清理：

```bash
rm -rf temp_agents/
```

## 开发建议

- **开发阶段**：使用原始 ADK Web 接口，获得完整的开发工具
- **演示阶段**：使用自定义 Web 接口，界面更简洁
- **生产环境**：根据需求选择合适的模式 