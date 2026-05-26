# Gunicorn：Python 应用服务器

> **学习目标**：理解 Gunicorn 的作用和架构，学会用它部署 FastAPI/Django/Flask 应用，掌握生产环境的配置和调优。

---

## 1. Gunicorn 是什么？

**Gunicorn**（Green Unicorn，绿色独角兽）是一个 Python **WSGI/ASGI HTTP 服务器**，用来在生产环境中运行 Python Web 应用。

### 1.1 为什么需要 Gunicorn？

开发时你用的是 Flask 自带的 `flask run` 或 FastAPI 的 `uvicorn main:app --reload`，但这些**不能用于生产环境**：

| 问题 | 说明 |
|------|------|
| 单进程 | 同时只能处理一个请求，多个用户访问会排队 |
| 不稳定 | 进程崩溃后不会自动恢复 |
| 无并发优化 | 没有针对大量连接做优化 |
| 有安全风险 | 开发服务器不处理慢速连接攻击等问题 |

Gunicorn 解决了这些问题：它启动多个工作进程，自动管理进程的生死，让你的应用能稳定、高效地处理大量请求。

### 1.2 Gunicorn 在整个架构中的位置

```
客户端（浏览器/APP）
        ↓
   Nginx（反向代理，处理静态文件、SSL、负载均衡）
        ↓
   Gunicorn（应用服务器，管理多个 Python 工作进程）
        ↓
   FastAPI / Django / Flask（你的业务代码）
```

Gunicorn 不是直接面向用户的，它通常在 Nginx 后面，专门负责运行 Python 代码。

### 1.3 WSGI vs ASGI

Gunicorn 原生支持 **WSGI**（同步），通过 Worker 插件也支持 **ASGI**（异步）：

| 接口 | 同步/异步 | 适用框架 | Gunicorn Worker |
|------|-----------|----------|-----------------|
| **WSGI** | 仅同步 | Flask、Django（传统） | `sync`（默认） |
| **ASGI** | 支持异步 | FastAPI、Starlette | `uvicorn.workers.UvicornWorker` |

> 对于 FastAPI 项目，Gunicorn 使用 UvicornWorker 来处理异步请求，相当于"Gunicorn 管进程 + Uvicorn 跑请求"。

### 1.4 ⚠️ Gunicorn 不支持 Windows

Gunicorn 使用了 Unix 专属的 `fork()` 系统调用和 `fcntl` 模块，**无法在 Windows 上运行**。如果在 Windows 上执行 `gunicorn` 会报错：

```
ModuleNotFoundError: No module named 'fcntl'
```

| 平台 | 能否运行 Gunicorn |
|------|-------------------|
| Linux | ✅ 原生支持 |
| macOS | ✅ 原生支持 |
| Windows | ❌ 不支持 |
| WSL2（Windows 子系统） | ✅ 完美运行 |
| Docker（Linux 容器） | ✅ 完美运行 |

**Windows 上的替代方案：**

| 方案 | 说明 |
|------|------|
| **直接用 Uvicorn** | `uvicorn main:app --reload`，Windows 完全支持，开发够用 |
| **WSL2** | 在 Windows Subsystem for Linux 中运行 Gunicorn |
| **Docker Desktop** | 用 Linux 容器运行，生产环境推荐 |

> 对于 FastAPI 项目，Windows 开发时直接用 Uvicorn 就行。Gunicorn 只在 **Linux 生产部署** 时才需要。

### 1.5 安装

```bash
# Linux / macOS / WSL2
uv add gunicorn
```

---

## 2. 核心架构：Master-Worker 模型

Gunicorn 采用 **Pre-fork Worker** 模型，这是理解 Gunicorn 的关键：

```
                Master 进程
               /     |     \
          Worker1  Worker2  Worker3   ← 实际处理请求的进程
            |        |        |
          你的App   你的App   你的App
```

### 2.1 Master 进程做什么？

- **不处理请求**，只做管理工作
- 启动时 fork 出多个 Worker 进程
- 监控 Worker 状态，如果某个 Worker 挂了，自动拉起一个新的
- 处理信号（如收到 `HUP` 信号时优雅重启）

### 2.2 Worker 进程做什么？

- 每个 Worker 是一个独立的 Python 进程
- 真正接收和处理 HTTP 请求
- Worker 之间互不干扰，一个崩溃不影响其他

### 2.3 为什么用多进程而不是多线程？

Python 有 **GIL（全局解释器锁）**，同一时刻只有一个线程在执行 Python 代码。多线程无法充分利用多核 CPU。而多进程每个进程有独立的 GIL，能真正并行处理请求。

---

## 3. 基本使用

### 3.1 启动一个 WSGI 应用（Flask）

假设你的 Flask 应用在 `app.py` 中：

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
```

启动命令：

```powershell
# 最简单的启动方式
gunicorn app:app

# 完整参数
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

命令解读：
- `app:app` —— `app` 是文件名（`app.py`），`:` 后面的 `app` 是 Flask 实例的变量名
- `--bind 0.0.0.0:8000` —— 监听所有网络接口的 8000 端口
- `--workers 4` —— 启动 4 个工作进程

### 3.2 启动一个 ASGI 应用（FastAPI）

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}
```

启动命令：

```powershell
# 需要先安装 uvicorn
uv add uvicorn

# 使用 UvicornWorker 启动
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

逐个解读：
- `-w 4` —— `--workers` 的简写，启动 4 个工作进程
- `-k uvicorn.workers.UvicornWorker` —— `--worker-class` 的简写，指定使用 Uvicorn 的 Worker 类来处理 ASGI 请求
- `--bind 0.0.0.0:8000` —— 监听地址和端口

> **与直接用 Uvicorn 的区别**：`uvicorn main:app --workers 4` 也能多进程，但 Gunicorn 提供了更成熟的进程管理（如 Worker 崩溃自动重启、优雅重启、信号处理等）。

---

## 4. 命令行参数详解

### 4.1 常用参数

```powershell
gunicorn main:app \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --timeout 30 \
  --graceful-timeout 30 \
  --max-requests 1000 \
  --max-requests-jitter 50 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--bind` / `-b` | `127.0.0.1:8000` | 监听地址和端口 |
| `--workers` / `-w` | `1` | 工作进程数 |
| `--worker-class` / `-k` | `sync` | Worker 类型（见下表） |
| `--threads` | `1` | 每个 Worker 的线程数 |
| `--timeout` | `30` | Worker 超时时间（秒），超时会被杀掉重启 |
| `--graceful-timeout` | `30` | 优雅关闭的超时时间 |
| `--max-requests` | `0`（不限） | Worker 处理多少个请求后重启（防止内存泄漏） |
| `--max-requests-jitter` | `0` | 在 max-requests 基础上加减的随机值（避免所有 Worker 同时重启） |
| `--preload-app` | `false` | 在 fork Worker 之前加载应用代码 |
| `--access-logfile` | 无 | 访问日志文件路径，`-` 表示输出到终端 |
| `--error-logfile` | `-` | 错误日志文件路径 |
| `--log-level` | `info` | 日志级别 |
| `--daemon` | `false` | 是否以守护进程运行 |

### 4.2 Worker 类型选择

| Worker 类型 | 说明 | 适用场景 |
|-------------|------|---------|
| `sync`（默认） | 每个 Worker 同步处理一个请求 | CPU 密集型任务 |
| `gthread` | 每个 Worker 用线程池处理多个请求 | IO 密集型，需要一定并发 |
| `gevent` | 基于协程的异步 Worker | 高并发 IO 密集型 |
| `uvicorn.workers.UvicornWorker` | 使用 Uvicorn 处理 ASGI 请求 | **FastAPI 等异步框架** |

### 4.3 Worker 数量怎么定？

官方推荐的公式：

```
Workers = (2 × CPU 核心数) + 1
```

例如 4 核 CPU：`(2 × 4) + 1 = 9` 个 Worker。

为什么是这个数？
- 任何时刻，大约一半的 Worker 在做 CPU 运算，另一半在等 IO（数据库、网络）
- `+1` 提供一点缓冲，确保总有 Worker 可以接受新请求

但这也只是起点，实际需要根据你的应用特点（CPU 密集还是 IO 密集）和可用内存来调整。

---

## 5. 配置文件

当参数越来越多，命令行会变得很长。Gunicorn 支持用 **Python 文件**做配置：

### 5.1 创建配置文件

```python
# gunicorn.conf.py
import multiprocessing

# 绑定地址
bind = "0.0.0.0:8000"

# Worker 数量：根据 CPU 核心数自动计算
workers = multiprocessing.cpu_count() * 2 + 1

# Worker 类型（FastAPI 用 UvicornWorker）
worker_class = "uvicorn.workers.UvicornWorker"

# 超时设置
timeout = 120
graceful_timeout = 30
keepalive = 5

# 防止内存泄漏：每处理 1000 个请求重启 Worker
max_requests = 1000
max_requests_jitter = 50

# 日志配置
accesslog = "-"
errorlog = "-"
loglevel = "info"

# 进程名称（方便在 ps/top 中识别）
proc_name = "my-fastapi-app"
```

### 5.2 使用配置文件启动

```powershell
gunicorn main:app -c gunicorn.conf.py
```

### 5.3 为什么用 Python 文件而不是 YAML/JSON？

Gunicorn 的配置文件是 Python 代码，这意味着你可以：
- 使用 `multiprocessing.cpu_count()` 动态计算 Worker 数量
- 使用 `os.environ.get()` 读取环境变量
- 使用条件判断（开发环境和生产环境不同配置）

```python
# gunicorn.conf.py
import multiprocessing
import os

workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")

# 开发环境启用热重载
if os.environ.get("ENV") == "development":
    reload = True
```

---

## 6. 服务器钩子（Hooks）

Gunicorn 提供了多个钩子函数，让你在特定事件发生时执行自定义逻辑：

```python
# gunicorn.conf.py

def on_starting(server):
    """服务器启动前调用。"""
    print("🚀 服务器正在启动...")

def when_ready(server):
    """服务器就绪，开始接受请求。"""
    print("✅ 服务器已就绪")

def pre_fork(server, worker):
    """每个 Worker 被 fork 之前调用。"""
    pass

def post_fork(server, worker):
    """每个 Worker 被 fork 之后调用。可以在这里初始化数据库连接。"""
    print(f"👷 Worker {worker.pid} 已启动")

def pre_exec(server):
    """优雅重启前调用。"""
    print("🔄 准备重启...")

def worker_int(server, worker):
    """Worker 被中断时调用。"""
    print(f"⚠️ Worker {worker.pid} 被中断")

def worker_abort(server, worker):
    """Worker 被强制终止时调用。"""
    print(f"❌ Worker {worker.pid} 被强制终止")
```

> 实际项目中，`post_fork` 常用于初始化数据库连接池、Redis 连接等，确保每个 Worker 有自己的连接。

---

## 7. 生产部署最佳实践

### 7.1 Nginx + Gunicorn 架构

**永远不要让 Gunicorn 直接暴露在公网上**。标准做法是在前面放一个 Nginx：

```
互联网 → Nginx（端口 80/443） → Gunicorn（端口 8000，仅本地监听）
```

Nginx 的职责：
1. **SSL 终止**：处理 HTTPS，Gunicorn 只需处理 HTTP
2. **静态文件**：图片、CSS、JS 由 Nginx 直接返回，不经过 Python
3. **安全防护**：过滤恶意请求、限制请求速率
4. **负载均衡**：把请求分发给多台 Gunicorn 服务器

Nginx 配置示例：

```nginx
# /etc/nginx/sites-available/myapp
server {
    listen 80;
    server_name example.com;

    # 静态文件由 Nginx 直接处理
    location /static/ {
        alias /app/static/;
    }

    # 其他请求转发给 Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 7.2 preload_app 节省内存

```python
# gunicorn.conf.py
preload_app = True
```

`preload_app = True` 会让 Gunicorn 在 fork Worker **之前**加载应用代码。这样：
- 所有 Worker 共享同一份代码的内存（利用操作系统的 Copy-on-Write 机制）
- 启动更快（Worker 不需要重新导入 Python 模块）

> ⚠️ 注意：`preload_app = True` 时，`post_fork` 钩子中的初始化操作（如数据库连接）尤为重要，因为每个 Worker 需要自己的连接，不能共享父进程的连接。

### 7.3 防止内存泄漏

长时间运行的 Python 进程可能因为代码问题导致内存持续增长。Gunicorn 提供了自动重启机制：

```python
# gunicorn.conf.py

# 每个 Worker 处理 1000 个请求后自动重启
max_requests = 1000

# 加上随机偏移，避免所有 Worker 同时重启（会导致短暂的性能下降）
max_requests_jitter = 50
```

### 7.4 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

COPY . .

# Docker 中必须前台运行，不能开 daemon
CMD ["gunicorn", "main:app", "-c", "gunicorn.conf.py"]
```

> Docker 容器要求前台进程运行。如果 Gunicorn 以 daemon 模式运行（后台），容器会立即退出。

### 7.5 systemd 管理（Linux）

创建 systemd 服务文件，让 Gunicorn 开机自启、崩溃自动恢复：

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My FastAPI App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/app
Environment="PATH=/app/.venv/bin"
ExecStart=/app/.venv/bin/gunicorn main:app -c gunicorn.conf.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

管理命令：

```bash
# 启动服务
sudo systemctl start myapp

# 开机自启
sudo systemctl enable myapp

# 查看状态
sudo systemctl status myapp

# 重启（优雅重启 Worker）
sudo systemctl restart myapp

# 查看日志
sudo journalctl -u myapp -f
```

---

## 8. 常见问题排查

### 8.1 Worker 超时被杀

**现象**：日志中出现 `Worker failed to boot` 或 `Booting worker took too long`。

**原因**：Worker 启动时间超过了 `timeout`（默认 30 秒）。

**解决**：
```python
# 增加超时时间
timeout = 120
```

### 8.2 内存持续增长

**原因**：代码中存在内存泄漏（如全局列表不断增长、缓存未清理）。

**临时解决**：
```python
max_requests = 500
max_requests_jitter = 25
```

**根本解决**：排查代码中的内存泄漏。

### 8.3 Worker 启动失败

**现象**：日志中出现 `ImportError` 或 `ModuleNotFoundError`。

**原因**：Gunicorn 找不到你的应用模块。

**检查**：
- 确保在正确的目录下运行命令
- 确保虚拟环境已激活
- 检查 `main:app` 中的文件名和变量名是否正确

---

## 9. 性能调优参考

根据应用类型选择不同的配置策略：

```python
# gunicorn.conf.py
import multiprocessing

# ========== CPU 密集型（如图像处理、数据分析） ==========
workers = multiprocessing.cpu_count()      # Worker 数 = CPU 核心数
worker_class = "sync"
threads = 1
timeout = 30

# ========== IO 密集型（如数据库查询、调用外部 API） ==========
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 4
timeout = 60

# ========== 高并发（如大量 WebSocket 连接） ==========
workers = multiprocessing.cpu_count()
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120

# ========== 通用安全设置 ==========
max_requests = 1000
max_requests_jitter = 50
keepalive = 2
```

---

## 本章小结

| 概念 | 说明 |
|------|------|
| **Master-Worker** | Gunicorn 的核心架构，Master 管理，Worker 处理请求 |
| `--workers` | 工作进程数，推荐 `(2 × CPU核数) + 1` |
| `-k uvicorn.workers.UvicornWorker` | FastAPI 项目必须指定此 Worker 类型 |
| `gunicorn.conf.py` | Python 配置文件，比命令行参数更灵活 |
| `preload_app` | 预加载应用，节省内存 |
| `max_requests` | 防止内存泄漏，定期重启 Worker |
| Nginx + Gunicorn | 标准生产部署架构 |
| Docker / systemd | 生产环境的进程管理方式 |

---

## 相关章节

- [Uvicorn：ASGI 服务器](../uvicorn/README.md)
- [FastAPI：Web 框架](../fastapi/README.md)
- [PM2：进程管理器](../pm2/README.md)
