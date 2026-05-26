# Uvicorn：Python ASGI 服务器

> **学习目标**：理解 Uvicorn 的作用和工作原理，学会启动、配置和部署 FastAPI 应用。

---

## 1. Uvicorn 是什么？

**Uvicorn** 是一个基于 Python 的 **ASGI（Asynchronous Server Gateway Interface）Web 服务器**。

### Web 框架 vs Web 服务器

初学者常混淆这两个概念，它们的关系是：

```
客户端（浏览器）  ←→  Web 服务器（Uvicorn）  ←→  Web 框架（FastAPI）
     请求/响应           接收请求、转发              处理业务逻辑
```

| 角色                      | 职责                               | 类比                 |
| ------------------------- | ---------------------------------- | -------------------- |
| **Web 服务器**（Uvicorn） | 监听端口、接收 HTTP 请求、返回响应 | 餐厅服务员，负责传菜 |
| **Web 框架**（FastAPI）   | 路由分发、数据验证、业务逻辑       | 厨师，负责做菜       |

> 没有 Uvicorn，FastAPI 就无法接收网络请求。就像没有服务员，厨师的菜端不到客人桌上。

### 为什么 FastAPI 需要 Uvicorn？

Python Web 框架有两种标准接口：

| 标准     | 同步/异步 | 代表框架              | 代表服务器             |
| -------- | --------- | --------------------- | ---------------------- |
| **WSGI** | 仅同步    | Flask、Django（传统） | Gunicorn、uWSGI        |
| **ASGI** | 支持异步  | FastAPI、Starlette    | **Uvicorn**、Hypercorn |

FastAPI 是异步框架，需要 ASGI 服务器来运行。Uvicorn 是目前最流行的选择。

### 安装

```powershell
uv add uvicorn
```

如果你已经安装了 FastAPI，Uvicorn 通常也一起安装了（`uv add fastapi uvicorn`）。

---

## 2. 启动 FastAPI 应用

### 命令行启动

```powershell
uvicorn app.main:app --reload
```

这个命令各部分的含义：

| 部分       | 含义                                     |
| ---------- | ---------------------------------------- |
| `app.main` | Python 模块路径，对应 `app/main.py` 文件 |
| `:app`     | 该模块中 `FastAPI()` 实例的变量名        |
| `--reload` | 开发模式，代码修改后自动重启             |

### 用 Python 模块方式启动

```powershell
# 效果相同，但能确保使用当前虚拟环境的 Python
uv run python -m uvicorn app.main:app --reload
```

> 推荐在 `uv` 管理的项目中使用这种方式，确保环境一致。

### 在代码中启动

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}

# 直接运行此文件即可启动
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
```

```powershell
uv run python main.py
```

---

## 3. 常用命令行参数

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

| 参数           | 默认值      | 说明                                       |
| -------------- | ----------- | ------------------------------------------ |
| `--host`       | `127.0.0.1` | 监听的地址。`0.0.0.0` 表示允许外部访问     |
| `--port`       | `8000`      | 监听的端口号                               |
| `--reload`     | 关闭        | 代码变更后自动重启（仅开发环境）           |
| `--reload-dir` | 当前目录    | 监听哪个目录的文件变化                     |
| `--workers`    | 1           | 工作进程数（生产环境用）                   |
| `--log-level`  | `info`      | 日志级别：`debug`/`info`/`warning`/`error` |
| `--access-log` | 开启        | 是否记录访问日志                           |

### `--reload` 与 `--workers` 互斥

- `--reload`：开发时用，自动重启
- `--workers N`：生产环境用，多进程提升性能

两者**不能同时使用**。

---

## 4. 开发环境 vs 生产环境

### 开发环境

```powershell
# 单进程 + 自动重载，方便调试
uvicorn app.main:app --reload --log-level debug
```

### 生产环境

```powershell
# 多进程 + 指定端口，不启用 reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

> `--workers 4` 表示启动 4 个进程，每个进程独立处理请求，能充分利用多核 CPU。

### 用 Gunicorn 管理 Uvicorn（推荐的生产部署方式）

```powershell
uv add gunicorn

# Gunicorn 做进程管理，Uvicorn 的 worker 处理请求
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

这种方式的好处：Gunicorn 成熟的进程管理 + Uvicorn 高性能的 ASGI 处理。

---

## 5. 访问地址

启动后，默认可以访问以下地址：

| 地址                               | 说明                 |
| ---------------------------------- | -------------------- |
| http://127.0.0.1:8000              | API 根路径           |
| http://127.0.0.1:8000/docs         | Swagger 交互式文档   |
| http://127.0.0.1:8000/redoc        | ReDoc 文档           |
| http://127.0.0.1:8000/openapi.json | OpenAPI 规范（JSON） |

---

## 6. Uvicorn 的工作流程

```
1. 启动：加载你的 FastAPI 应用
2. 监听：在指定端口等待 HTTP 请求
3. 接收：收到客户端请求
4. 转交：把请求交给 ASGI 应用（FastAPI）处理
5. 返回：把 FastAPI 的响应返回给客户端
6. 循环：继续等待下一个请求
```

如果是 `--reload` 模式，Uvicorn 还会额外监听文件变化，一旦检测到代码修改就自动重启应用。

---

## 本章小结

| 概念                | 说明                                           |
| ------------------- | ---------------------------------------------- |
| ASGI                | 异步服务器网关接口，Web 服务器与框架之间的协议 |
| `uvicorn main:app`  | 启动命令：模块路径:实例名                      |
| `--reload`          | 开发模式，自动重载（不能与 `--workers` 同用）  |
| `--workers N`       | 生产模式，多进程处理                           |
| `--host` / `--port` | 监听地址和端口                                 |
| Gunicorn + Uvicorn  | 推荐的生产部署方式                             |

---

## 相关章节

- [FastAPI：Web 框架](../fastapi/README.md)
- [Gunicorn：应用服务器](../gunicorn/README.md) —— 生产部署推荐搭配
- [PM2：进程管理器](../pm2/README.md) —— 多语言混合项目可用 PM2 统一管理
- [Pydantic：数据验证](../pydantic/README.md)
