# PM2：进程管理器

> **学习目标**：理解进程管理器的概念和 PM2 的作用，学会用 PM2 启动、监控、管理 Python 和 Node.js 应用，掌握生产环境下的配置和部署。

---

## 1. PM2 是什么？

**PM2**（Process Manager 2）是一个**生产级进程管理器**。它的核心职责是：确保你的应用**永远在运行**——崩溃了自动重启，服务器重启了自动拉起。

### 1.1 为什么需要进程管理器？

你写好了一个 FastAPI 应用，用 `python main.py` 启动，看起来没问题。但生产环境中会遇到这些问题：

| 问题 | 说明 |
|------|------|
| 进程崩溃 | 代码有 bug 导致进程退出，服务中断 |
| 服务器重启 | 部署新代码或系统更新后需要重启，手动启动太慢 |
| 日志丢失 | 终端关了就看不到日志了 |
| 无法监控 | 不知道 CPU、内存使用情况 |
| 多应用管理 | 同时跑 Python API + Node.js 前端，管理麻烦 |

PM2 解决了所有这些问题。

### 1.2 PM2 和 Gunicorn 是什么关系？

这是初学者最常见的困惑。它们**不是同类工具**，可以搭配使用：

| 维度 | PM2 | Gunicorn |
|------|-----|----------|
| **本质** | 通用**进程管理器** | Python **应用服务器** |
| **做什么** | 管理进程的启停、监控、日志 | 接收 HTTP 请求，调用 Python 代码 |
| **支持语言** | 任何语言（Python、Node.js、Go...） | 仅 Python |
| **类比** | 餐厅经理（管理员工上下班） | 厨房灶台（真正做菜） |

```
场景一（纯 Python 项目）：
  Nginx → Gunicorn → FastAPI
  进程管理：用 systemd 或 Docker

场景二（Python + Node.js 混合）：
  Nginx → PM2 统一管理
            ├── Gunicorn → FastAPI
            └── Next.js（Node.js）
```

### 1.3 什么时候选 PM2？

| 场景 | 推荐方案 |
|------|---------|
| 纯 Python 项目 | Gunicorn + systemd/Docker |
| 纯 Node.js 项目 | **PM2** |
| Python + Node.js 混合 | **PM2** 统一管理 |
| 需要漂亮的监控面板 | **PM2 Plus** |
| Docker 容器部署 | 通常不需要 PM2，Docker 本身管理进程 |

---

## 2. 安装

### 2.1 前置条件：安装 Node.js

PM2 基于 Node.js，所以需要先安装它：

**Windows：**
```powershell
# 方式一：从官网下载安装包
# https://nodejs.org/

# 方式二：用 winget 安装
winget install OpenJS.NodeJS.LTS
```

**macOS：**
```bash
brew install node
```

**Linux（Ubuntu/Debian）：**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

验证安装：
```powershell
node --version    # 应显示 v20.x.x 或更高
npm --version     # 应显示 10.x.x 或更高
```

### 2.2 安装 PM2

```powershell
npm install -g pm2
```

`-g` 表示全局安装，安装后 `pm2` 命令在任何目录都能使用。

验证安装：
```powershell
pm2 --version
```

---

## 3. 基本使用

### 3.1 启动应用

```powershell
# 启动一个 Python 脚本
pm2 start main.py --name my-api

# 启动一个 Node.js 应用
pm2 start server.js --name my-frontend

# 指定 Python 解释器（重要：用虚拟环境的 Python）
pm2 start main.py --name my-api --interpreter .venv/Scripts/python

# 给应用传参数
pm2 start main.py --name my-api -- --host 0.0.0.0 --port 8000
```

逐行解读：
- `pm2 start main.py` —— PM2 自动识别 `.py` 文件，用 Python 运行
- `--name my-api` —— 给应用取个名字，后续用名字管理
- `--interpreter .venv/Scripts/python` —— 指定用哪个 Python（Windows 虚拟环境路径）
- `--` —— 之后的参数会传给你的 Python 脚本

> **Windows 注意**：虚拟环境的 Python 路径是 `.venv/Scripts/python`（Linux/Mac 是 `.venv/bin/python`）。

### 3.2 查看应用状态

```powershell
# 查看所有应用列表
pm2 list
# 或简写
pm2 ls
```

输出示例：

```
┌─────┬──────────┬─────────────┬─────────┬───────────┬──────────┬────────────┐
│ id  │ name     │ mode        │ ↺       │ status    │ cpu      │ memory     │
├─────┼──────────┼─────────────┼─────────┼───────────┼──────────┼────────────┤
│ 0   │ my-api   │ fork        │ 1       │ online    │ 0%       │ 45.2mb     │
│ 1   │ frontend │ fork        │ 0       │ online    │ 2.3%     │ 62.1mb     │
└─────┴──────────┴─────────────┴─────────┴───────────┴──────────┴────────────┘
```

字段说明：
- **id** —— 应用编号，管理时可以用 id 或 name
- **↺** —— 重启次数（如果数字不断增长，说明应用在反复崩溃）
- **status** —— `online`（运行中）、`stopping`（停止中）、`errored`（出错）
- **cpu / memory** —— 实时资源占用

### 3.3 管理应用

```powershell
# 停止应用（保留在列表中）
pm2 stop my-api

# 重启应用
pm2 restart my-api

# 删除应用（从列表中移除）
pm2 delete my-api

# 停止所有应用
pm2 stop all

# 重启所有应用
pm2 restart all

# 删除所有应用
pm2 delete all
```

`stop` vs `delete` 的区别：
- `stop`：应用暂停，还在列表里，随时可以 `pm2 start my-api` 恢复
- `delete`：彻底从 PM2 中移除，需要重新 `pm2 start`

### 3.4 查看详细信息

```powershell
# 查看某个应用的详细信息
pm2 show my-api

# 或用 id
pm2 show 0
```

会显示：启动时间、运行时长、脚本路径、日志路径、环境变量等。

---

## 4. 日志管理

### 4.1 查看日志

```powershell
# 实时查看所有应用的日志
pm2 logs

# 查看指定应用的日志
pm2 logs my-api

# 只看最近 100 行
pm2 logs --lines 100

# 只看错误日志
pm2 logs --err

# 只看输出日志
pm2 logs --out
```

### 4.2 日志文件位置

PM2 会把日志保存到文件中：

| 系统 | 日志路径 |
|------|---------|
| Linux/Mac | `~/.pm2/logs/` |
| Windows | `%USERPROFILE%\.pm2\logs\` |

每个应用有两个日志文件：
- `my-api-out.log` —— 标准输出（`print()` 的内容）
- `my-api-error.log` —— 错误输出（异常信息）

### 4.3 清空日志

```powershell
# 清空所有日志文件
pm2 flush

# 清空指定应用的日志
pm2 flush my-api
```

### 4.4 日志自动轮转

日志文件会越来越大。安装 `pm2-logrotate` 插件自动管理：

```powershell
pm2 install pm2-logrotate
```

安装后自动生效，默认：
- 每天轮转一次
- 总日志大小超过 10MB 时轮转
- 保留最近 30 个日志文件

---

## 5. 配置文件：ecosystem.config.js

当应用变多、参数变复杂时，用配置文件管理比命令行方便得多。

### 5.1 创建配置文件

```powershell
# 在项目根目录生成模板
pm2 init simple
```

这会创建一个 `ecosystem.config.js` 文件。

### 5.2 配置文件详解

```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      // 基本设置
      name: "fastapi-api",               // 应用名称
      script: "main.py",                  // 启动脚本
      interpreter: ".venv/Scripts/python", // Python 解释器路径
      args: "--host 0.0.0.0 --port 8000", // 传给脚本的参数
      cwd: "./",                          // 工作目录

      // 进程管理
      autorestart: true,                  // 崩溃后自动重启
      max_restarts: 10,                   // 最大重启次数（防止无限重启）
      restart_delay: 3000,                // 重启间隔（毫秒）
      min_uptime: "10s",                  // 进程运行不到 10 秒就崩溃，视为异常启动

      // 资源限制
      max_memory_restart: "500M",         // 内存超过 500MB 自动重启

      // 环境变量
      env: {                              // 默认环境（开发）
        ENVIRONMENT: "development",
        PORT: 8000
      },
      env_production: {                   // 生产环境
        ENVIRONMENT: "production",
        PORT: 8080
      },

      // 日志配置
      error_file: "./logs/error.log",     // 错误日志路径
      out_file: "./logs/out.log",         // 输出日志路径
      merge_logs: true,                   // 合并集群模式下的日志
      log_date_format: "YYYY-MM-DD HH:mm:ss Z", // 日志中加上时间戳

      // 高级设置
      watch: false,                       // 文件变化时自动重启（开发时用）
      ignore_watch: ["logs", ".venv"],    // 忽略监听的目录
    },
    {
      // 第二个应用（示例：Node.js 前端）
      name: "frontend",
      script: "npm",
      args: "start",
      cwd: "./frontend",
      autorestart: true,
      max_memory_restart: "300M",
      env_production: {
        PORT: 3000
      }
    }
  ]
};
```

### 5.3 使用配置文件

```powershell
# 用配置文件启动所有应用
pm2 start ecosystem.config.js

# 用生产环境变量启动
pm2 start ecosystem.config.js --env production

# 只启动其中一个应用
pm2 start ecosystem.config.js --only fastapi-api

# 重启（使用生产环境）
pm2 restart ecosystem.config.js --env production
```

### 5.4 环境变量切换

配置文件中的 `env` 和 `env_production` 让你轻松切换环境：

```powershell
# 开发环境（使用 env 中的变量）
pm2 start ecosystem.config.js

# 生产环境（使用 env_production 中的变量）
pm2 start ecosystem.config.js --env production
```

---

## 6. 监控

### 6.1 终端监控

```powershell
# 打开实时监控面板
pm2 monit
```

这会打开一个交互式面板，左侧显示日志，右侧显示 CPU 和内存使用情况。

### 6.2 Web 监控面板（PM2 Plus）

PM2 提供了一个付费的云监控服务 PM2 Plus：

```powershell
# 连接到 PM2 Plus
pm2 plus
```

功能包括：
- Web 仪表盘，远程查看所有服务器上的应用状态
- 实时性能指标（CPU、内存、事件循环延迟）
- 错误追踪和告警
- 分布式追踪

> 对于小型项目，终端的 `pm2 monit` 通常就够用了。

---

## 7. 集群模式

### 7.1 什么是集群模式？

默认情况下，PM2 以 **fork 模式**启动应用（单个实例）。集群模式可以启动多个实例，充分利用多核 CPU：

```powershell
# 启动 4 个实例
pm2 start main.py -i 4 --name my-api

# 根据 CPU 核心数自动启动最大实例数
pm2 start main.py -i max --name my-api
```

`-i` 是 `--instances` 的简写，指定实例数量。PM2 会在这些实例之间自动做负载均衡。

### 7.2 动态调整实例数

```powershell
# 增加到 6 个实例
pm2 scale my-api 6

# 减少到 2 个实例
pm2 scale my-api 2
```

### 7.3 零停机重载

```powershell
# 逐个重启实例，确保始终有实例在处理请求
pm2 reload my-api
```

`reload` vs `restart`：
- `restart`：同时杀掉所有实例再启动，会有短暂的服务中断
- `reload`：逐个重启，每个新实例就绪后才停掉旧实例，**零停机**

### 7.4 集群模式的配置文件写法

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: "my-api",
    script: "main.py",
    interpreter: ".venv/Scripts/python",
    instances: "max",        // 自动使用所有 CPU 核心
    exec_mode: "cluster",    // 集群模式
    autorestart: true,
    max_memory_restart: "500M"
  }]
};
```

> ⚠️ **注意**：如果你的应用使用了 WebSocket、共享文件等有状态的功能，集群模式可能需要额外配置（如 Redis 共享状态）。FastAPI 的普通 REST API 通常没有问题。

---

## 8. 开机自启

### 8.1 Linux 系统

```bash
# 生成开机自启脚本
pm2 startup

# 保存当前的应用列表（这样重启后会自动恢复）
pm2 save
```

`pm2 startup` 会输出一条命令，需要用 `sudo` 执行。执行后 PM2 会注册为系统服务，开机自动启动。

`pm2 save` 非常重要——它把当前运行的应用列表保存下来。下次开机时 PM2 会自动恢复这些应用。

### 8.2 Windows 系统

Windows 没有原生 `pm2 startup` 支持，需要通过**任务计划程序**配置：

```powershell
# 方式一：使用 pm2-windows-startup 插件
npm install -g pm2-windows-startup
pm2-startup install
pm2 save
```

或者手动创建任务计划：

1. 打开"任务计划程序"（Task Scheduler）
2. 创建基本任务 → 触发器选"计算机启动时"
3. 操作选"启动程序"，程序填 `pm2`，参数填 `resurrect`
4. 勾选"不管用户是否登录都要运行"

---

## 9. PM2 管理 Python 应用的完整示例

### 9.1 项目结构

```
my-project/
├── .venv/                    # Python 虚拟环境
├── main.py                   # FastAPI 应用
├── ecosystem.config.js       # PM2 配置文件
├── gunicorn.conf.py          # Gunicorn 配置（可选）
└── logs/                     # 日志目录
```

### 9.2 FastAPI 应用

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from PM2!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### 9.3 方式一：PM2 直接启动 Uvicorn

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: "fastapi-api",
    script: ".venv/Scripts/python",    // Windows
    args: "-m uvicorn main:app --host 0.0.0.0 --port 8000",
    cwd: "./",
    autorestart: true,
    max_restarts: 10,
    restart_delay: 3000,
    max_memory_restart: "500M",
    env: {
      ENVIRONMENT: "development"
    },
    env_production: {
      ENVIRONMENT: "production"
    },
    error_file: "./logs/error.log",
    out_file: "./logs/out.log",
    log_date_format: "YYYY-MM-DD HH:mm:ss"
  }]
};
```

```powershell
pm2 start ecosystem.config.js
```

### 9.4 方式二：PM2 管理 Gunicorn + Uvicorn

这种方式让 Gunicorn 管理多 Worker，PM2 管理 Gunicorn 进程：

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: "fastapi-api",
    script: ".venv/Scripts/gunicorn",  // Windows
    args: "main:app -c gunicorn.conf.py",
    cwd: "./",
    autorestart: true,
    max_memory_restart: "1G",
    error_file: "./logs/error.log",
    out_file: "./logs/out.log",
    log_date_format: "YYYY-MM-DD HH:mm:ss"
  }]
};
```

```python
# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
max_requests = 1000
max_requests_jitter = 50
```

### 9.5 混合项目示例（Python API + Node.js 前端）

```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: "api",
      script: ".venv/Scripts/python",
      args: "-m uvicorn main:app --host 0.0.0.0 --port 8000",
      autorestart: true,
      max_memory_restart: "500M",
      env_production: {
        ENVIRONMENT: "production"
      }
    },
    {
      name: "frontend",
      script: "npm",
      args: "start",
      cwd: "./frontend",
      autorestart: true,
      max_memory_restart: "300M",
      env_production: {
        PORT: 3000
      }
    }
  ]
};
```

```powershell
# 同时启动 API 和前端
pm2 start ecosystem.config.js --env production

# 查看状态
pm2 ls

# 只重启 API
pm2 restart api

# 查看两个应用的日志
pm2 logs
```

---

## 10. 常用命令速查

| 命令 | 说明 |
|------|------|
| `pm2 start <file>` | 启动应用 |
| `pm2 stop <name>` | 停止应用 |
| `pm2 restart <name>` | 重启应用 |
| `pm2 reload <name>` | 零停机重载（集群模式） |
| `pm2 delete <name>` | 删除应用 |
| `pm2 list` / `pm2 ls` | 查看所有应用 |
| `pm2 show <name>` | 查看应用详情 |
| `pm2 logs` | 查看日志 |
| `pm2 logs <name>` | 查看指定应用日志 |
| `pm2 logs --err` | 只看错误日志 |
| `pm2 monit` | 实时监控面板 |
| `pm2 flush` | 清空日志 |
| `pm2 save` | 保存当前应用列表 |
| `pm2 startup` | 配置开机自启（Linux） |
| `pm2 scale <name> <n>` | 调整集群实例数 |
| `pm2 start ecosystem.config.js` | 用配置文件启动 |

---

## 11. PM2 vs Gunicorn vs systemd 对比

| 维度 | PM2 | Gunicorn | systemd |
|------|-----|----------|---------|
| **类型** | 进程管理器 | 应用服务器 | 系统服务管理 |
| **支持语言** | 所有语言 | 仅 Python | 所有程序 |
| **HTTP 处理** | 不处理 | 接收和转发 HTTP 请求 | 不处理 |
| **集群模式** | ✅ 内置 | ✅ 多 Worker | ❌ 需手动配置 |
| **零停机重载** | ✅ `pm2 reload` | ✅ 信号处理 | 需配置 |
| **监控面板** | ✅ `pm2 monit` | ❌ | ❌ |
| **日志管理** | ✅ 内置 | 基础 | ✅ journalctl |
| **需要 Node.js** | ✅ | ❌ | ❌ |
| **Linux 专属** | ❌ 跨平台 | ✅ 仅 Linux/Mac | ✅ 仅 Linux |
| **资源占用** | ~80-100MB | 很低 | 零额外开销 |

**如何选择：**

- **纯 Python API，Linux 部署**：Gunicorn + systemd（最轻量）
- **Node.js 应用**：PM2（最佳选择）
- **多语言混合项目**：PM2（统一管理）
- **Docker 部署**：通常不需要 PM2/Gunicorn 的进程管理，Docker 自己处理

---

## 相关章节

- [Uvicorn：ASGI 服务器](../uvicorn/README.md)
- [Gunicorn：应用服务器](../gunicorn/README.md)
- [FastAPI：Web 框架](../fastapi/README.md)
