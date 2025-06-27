# Havoc 测试套件

这个目录包含了项目的自定义测试脚本和工具。

## 📁 文件说明

### 核心测试脚本

- **`test_setup.py`** - 项目验证脚本
  - 验证项目配置和依赖
  - 测试代理创建和工具功能
  - 检查环境变量配置

- **`test_cleanup.py`** - 清理功能测试脚本
  - 测试异步资源清理
  - 验证 aiohttp 会话管理
  - 检查内存泄漏问题

- **`test_web_modes.py`** - Web 接口模式测试脚本
  - 测试自定义 Web 接口配置
  - 验证原始 ADK Web 接口集成
  - 检查模式切换和回退机制
  - ADK 模块可用性检测

- **`quick_start.py`** - 快速开始脚本
  - 一键设置项目环境
  - 自动创建配置文件
  - 安装必要依赖

### 工具脚本

- **`run_tests.py`** - 批量测试运行器
  - 运行所有测试脚本
  - 生成综合测试报告
  - 自动化测试流程

## 🚀 使用方式

### 1. 从根目录运行

```bash
# 项目验证
python tests/havoc/test_setup.py

# 清理功能测试
python tests/havoc/test_cleanup.py

# Web 接口模式测试
python tests/havoc/test_web_modes.py

# 快速开始
python tests/havoc/quick_start.py

# 运行所有测试
python tests/havoc/run_tests.py
```

### 2. 从 tests/havoc 目录运行

```bash
cd tests/havoc

# 项目验证
python test_setup.py

# 清理功能测试
python test_cleanup.py

# Web 接口模式测试
python test_web_modes.py

# 快速开始
python quick_start.py

# 运行所有测试
python run_tests.py
```

### 3. 作为模块导入

```python
# 从项目根目录
from tests.havoc import run_setup_test, test_cleanup, run_quick_start

# 运行测试
await run_setup_test()
await test_cleanup()
await run_quick_start()
```

### 4. 使用 Python 模块方式

```bash
# 从根目录运行
python -m tests.havoc.test_setup
python -m tests.havoc.test_cleanup
python -m tests.havoc.test_web_modes
python -m tests.havoc.quick_start
```

## 🎯 测试场景

### test_setup.py - 项目验证
- ✅ 配置文件加载测试
- ✅ 环境变量验证
- ✅ 代理创建测试
- ✅ 工具功能验证
- ✅ 依赖检查

### test_cleanup.py - 清理功能测试
- ✅ aiohttp 会话清理
- ✅ LiteLLM 资源管理
- ✅ 异步任务清理
- ✅ 内存泄漏检测

### test_web_modes.py - Web 接口模式测试
- ✅ 自定义 Web 接口配置测试
- ✅ 原始 ADK Web 接口配置测试
- ✅ 默认配置行为验证
- ✅ ADK 模块可用性检查
- ✅ 配置切换和回退机制测试
- ✅ 使用示例和故障排除指南

### quick_start.py - 快速开始
- ✅ 环境检查
- ✅ 依赖安装
- ✅ 配置文件创建
- ✅ 项目初始化

## 🌐 Web 接口测试详解

### 配置模式测试
`test_web_modes.py` 提供了完整的 Web 接口模式测试：

```bash
# 测试所有 Web 接口模式
python tests/havoc/test_web_modes.py
```

**测试内容**：
1. **自定义模式**：`USE_ORIGINAL_ADK_WEB=false`
2. **原始 ADK 模式**：`USE_ORIGINAL_ADK_WEB=true`
3. **默认配置**：未设置环境变量时的行为
4. **模块可用性**：检查 google-adk 包是否正确安装
5. **使用示例**：提供详细的配置和启动说明

### 预期输出示例

```
============================================================
🚀 ADK Web 接口模式测试
============================================================
🧪 测试 Web 接口配置模式

1. 测试自定义 Web 接口模式:
   use_original_adk_web: False
   预期行为: 使用简化的聊天界面

2. 测试原始 ADK Web 接口模式:
   use_original_adk_web: True
   预期行为: 使用完整的 Angular 前端

3. 测试默认配置（未设置环境变量）:
   use_original_adk_web: False
   预期行为: 默认使用自定义 Web 接口

🔍 检查 ADK 模块可用性:

✅ ADK 核心模块可用
   - google.adk.cli.fast_api
   - google.adk.cli.utils.logs
   📝 可以使用原始 ADK Web 接口

📊 测试结果总结:
   ✅ 配置系统测试: 通过
   ✅ ADK 模块检查: 可用
   ✅ 使用示例展示: 完成

🎉 所有功能可用！您可以使用两种 Web 接口模式。

✨ 测试完成！
💡 现在您可以根据需要选择合适的 Web 接口模式
📍 运行位置: tests/havoc/test_web_modes.py
```

## 🔧 开发指南

### 添加新测试

1. 在 `tests/havoc/` 目录创建新的测试文件
2. 按照现有模式编写测试函数
3. 在 `__init__.py` 中导出测试函数
4. 更新此 README 文档

### 测试最佳实践

1. **异步测试**: 使用 `asyncio.run()` 运行异步测试
2. **错误处理**: 包含完整的异常处理逻辑
3. **清理资源**: 确保测试后正确清理资源
4. **日志输出**: 提供清晰的测试进度和结果信息
5. **环境隔离**: 测试完成后恢复原始环境变量

### Web 接口测试开发

对于 Web 接口相关的测试：

1. **配置测试**: 验证不同配置选项的行为
2. **模块检查**: 检查必要依赖的可用性
3. **回退机制**: 测试自动回退功能
4. **示例验证**: 确保使用示例的准确性

## 📊 测试报告

运行测试后，您将看到详细的测试报告：

```
🧪 开始项目验证...
✅ 配置加载成功: my_custom_app
✅ 代理创建成功，包含 4 个工具
✅ 时间查询工具测试通过
✅ 数学计算工具测试通过
✅ 随机字符串工具测试通过
✅ 文件操作工具测试通过
🎉 所有测试通过 (4/4)
```

## 📚 相关文档

- **Web 接口使用指南**: `docs/WEB_INTERFACE_GUIDE.md`
- **ADK 集成说明**: `docs/ADK_WEB_INTEGRATION.md`
- **项目配置说明**: `src/apps/core/config.py`
- **Web 接口实现**: `src/apps/interfaces/web_interface.py`

## 🤝 贡献

如果您发现测试问题或想要添加新的测试用例，请：

1. 创建新的测试文件
2. 遵循现有的代码风格
3. 添加适当的文档说明
4. 更新相关的 README 文档
5. 确保测试的环境隔离和清理 