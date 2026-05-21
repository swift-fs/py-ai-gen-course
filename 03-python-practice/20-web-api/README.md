# 第 20 章：实战——Web API

> **学习目标**：用 FastAPI 构建一个 RESTful API，学习路由、数据验证、Swagger 文档。

---

## 1. FastAPI 简介

FastAPI 是一个现代、快速的 Web 框架，特点：
- 自动生成 API 文档（Swagger）
- 基于 Pydantic 的数据验证
- 高性能

### 安装

```powershell
uv add fastapi uvicorn
```

---

## 2. 最简单的 API

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI(title="待办 API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "欢迎使用待办 API"}

@app.get("/health")
def health():
    return {"status": "ok"}
```

### 运行

```powershell
uvicorn app.main:app --reload
```

访问：
- http://127.0.0.1:8000 —— API
- http://127.0.0.1:8000/docs —— Swagger 文档
- http://127.0.0.1:8000/redoc —— ReDoc 文档

---

## 3. 数据模型和 CRUD

```python
from pydantic import BaseModel
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
```

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="待办 API")

# 内存存储（实际项目用数据库）
todos: dict[int, dict] = {}
next_id = 1

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.post("/todos", response_model=dict)
def create_todo(data: TodoCreate):
    global next_id
    todo = {"id": next_id, "title": data.title, "description": data.description, "done": False}
    todos[next_id] = todo
    next_id += 1
    return todo

@app.get("/todos")
def list_todos():
    return list(todos.values())

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="任务不存在")
    return todos[todo_id]

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="任务不存在")
    todo = todos[todo_id]
    if data.title is not None:
        todo["title"] = data.title
    if data.done is not None:
        todo["done"] = data.done
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="任务不存在")
    del todos[todo_id]
    return {"message": "已删除"}
```

---

## 4. 测试 API

```powershell
# 启动服务
uvicorn app.main:app --reload

# 用 curl 测试（或用浏览器访问 /docs）
curl -X POST http://localhost:8000/todos -H "Content-Type: application/json" -d "{\"title\": \"学习 FastAPI\"}"
curl http://localhost:8000/todos
curl -X PUT http://localhost:8000/todos/1 -H "Content-Type: application/json" -d "{\"done\": true}"
curl -X DELETE http://localhost:8000/todos/1
```

---

## 本章小结

| 概念 | 说明 |
|------|------|
| `FastAPI()` | 创建应用 |
| `@app.get/post/put/delete` | 定义路由 |
| `BaseModel` | Pydantic 数据验证 |
| `HTTPException` | 返回错误响应 |
| `/docs` | 自动生成的 API 文档 |
| `uvicorn` | ASGI 服务器 |

---

## 下一步

进入 [第 21 章：代码质量](../21-code-quality/README.md)。
