# 安全退出指南

## 问题背景

在使用 `Ctrl+C` 停止 Web 服务时，可能会遇到以下错误：

```
asyncio.exceptions.CancelledError
KeyboardInterrupt
```

这些错误是由于在清理资源过程中，`asyncio.sleep()` 函数被键盘中断信号取消导致的。

## 解决方案

### 1. 信号处理机制

实现了 `GracefulKiller` 类来优雅地处理退出信号：

```python
class GracefulKiller:
    """优雅退出处理器"""
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def _exit_gracefully(self, signum, frame):
        print(f"\n🛑 接收到退出信号 ({signum})，正在安全退出...")
        self.kill_now = True
```

### 2. 安全的异步等待

引入了 `safe_sleep()` 方法来替代 `asyncio.sleep()`：

```python
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
```

### 3. 分层清理机制

实现了三层清理机制：

#### 第一层：安全清理
- `safe_comprehensive_cleanup()` - 正常情况下的全面清理
- 使用 `safe_sleep()` 避免被中断
- 有超时保护机制

#### 第二层：带超时的清理
- 在 `safe_cleanup()` 函数中使用 `asyncio.wait_for()` 设置超时
- 超时后自动降级到紧急清理

#### 第三层：紧急清理
- `emergency_cleanup()` - 最小化异步操作的清理
- 主要执行同步操作如垃圾回收
- 确保程序能正常退出

### 4. 主程序改进

- 使用任务监控机制，定期检查退出信号
- 取消长时间运行的任务而不是强制终止
- 分离清理逻辑到独立函数 `safe_cleanup()`

## 使用方法

### 启动应用

```bash
# Web 模式
python main.py --mode web

# 控制台模式
python main.py --mode console
```

### 安全退出

1. **推荐方式**: 按 `Ctrl+C` 一次，等待程序完成清理
2. **紧急退出**: 如果清理过程卡住，可以再次按 `Ctrl+C` 强制退出

### 测试安全退出机制

```bash
# 运行测试脚本
python test_safe_exit.py

# 选择测试模式
# 1. 测试安全清理功能
# 2. 测试中断处理
```

## 改进效果

### 之前的问题

```
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
🧹 正在清理资源...
Traceback (most recent call last):
  ...
  File "/path/to/cleanup_helper.py", line 110, in cleanup_litellm_resources
    await asyncio.sleep(0.1)
asyncio.exceptions.CancelledError
```

### 改进后的效果

```
^C
🛑 接收到退出信号 (2)，正在安全退出...

🛑 正在停止 Web 服务...
🧹 开始清理资源...
✅ 接口资源清理完成
✅ 全面资源清理完成
🧹 资源清理完成
👋 应用已安全退出
```

## 配置选项

可以通过环境变量调整清理行为：

```bash
# 设置接口清理超时时间（秒）
export INTERFACE_CLEANUP_TIMEOUT=5

# 设置全面清理超时时间（秒）
export COMPREHENSIVE_CLEANUP_TIMEOUT=10

# 禁用 aiohttp 传输（避免警告）
export DISABLE_AIOHTTP_TRANSPORT=True
```

## 故障排除

### 如果清理过程仍然卡住

1. 检查是否有其他进程占用相同端口
2. 确保没有未关闭的文件句柄
3. 查看是否有死锁的异步任务

### 如果出现资源泄漏警告

1. 确保所有异步上下文管理器都正确关闭
2. 检查是否有未 await 的协程
3. 考虑增加清理超时时间

## 最佳实践

1. **总是使用 Ctrl+C 一次**: 给程序时间执行清理
2. **避免强制终止**: 除非绝对必要，否则不要使用 `kill -9`
3. **监控清理时间**: 如果清理时间过长，考虑优化资源管理
4. **测试退出机制**: 定期运行测试脚本确保退出机制正常工作

## 技术细节

### 信号处理

- `SIGINT` (Ctrl+C): 用户中断信号
- `SIGTERM`: 终止信号（系统关闭时）
- 两个信号都会触发优雅退出流程

### 异步任务管理

- 使用 `asyncio.create_task()` 创建可取消的任务
- 监控任务状态，及时取消长时间运行的任务
- 避免阻塞性操作影响退出流程

### 资源清理顺序

1. 停止接受新请求
2. 完成正在处理的请求
3. 关闭网络连接
4. 清理内存资源
5. 执行垃圾回收 